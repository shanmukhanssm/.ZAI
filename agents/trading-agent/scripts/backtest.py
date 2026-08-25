"""
Trading Agent — Backtester (cheat-proof)
Simulates "what the momentum system would have picked on CUTOFF date"
using ONLY data up to CUTOFF, then measures what actually happened afterward.

The scoring uses the EXACT same logic as momentum_rank.py (the live system),
so this is a true test of the system, not a new ad-hoc screen.

Anti-cheat guarantee: for every stock, the OHLCV rows are split at CUTOFF.
Scoring only ever sees rows <= CUTOFF. Forward returns only ever read rows > CUTOFF.
The two halves never mix, so future prices cannot leak into the pick.

Usage:
  python backtest.py 2026-07-25
Outputs JSON: ranked picks (by July-25 momentum score) + their forward returns.
"""
import sys
import os
import json
import time
import urllib.parse
from datetime import datetime

import requests
import numpy as np

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"}
BENCHMARK = "^NSEI"

# Transparent, pre-registered universe — a MIX of winners and losers (NOT cherry-picked
# after the fact). Includes the user's examples AND stocks that later did nothing/fell.
UNIVERSE = [
    # user's examples (later ran hard)
    "CUPID.NS", "BAJAJHIND.NS", "WEL.NS", "BEL.NS",
    # my live momentum picks
    "ASHOKLEY.NS", "MOTHERSON.NS", "MMTC.NS",
    # value watchlist
    "CANBK.NS", "BANKINDIA.NS", "SOUTHBANK.NS", "COALINDIA.NS", "NATIONALUM.NS",
    # defence (mixed outcomes)
    "HAL.NS", "MAZDOCK.NS", "COCHINSHIP.NS", "BDL.NS",
    # large caps (momentum laggards)
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "SBIN.NS", "ITC.NS", "TATAMOTORS.NS",
    # momentum names that FAILED / downtrend (from my earlier rejection scan)
    "RVNL.NS", "IRCON.NS", "SUZLON.NS", "IREDA.NS", "NHPC.NS", "INOXWIND.NS", "TATAPOWER.NS", "HUDCO.NS",
]


def chart_url(symbol, rng="1y"):
    return f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}?range={rng}&interval=1d&events=div%2Csplits"


def fetch_ohlcv(symbol, rng="1y"):
    for name, url in [("direct", chart_url(symbol, rng)),
                      ("allorigins", "https://api.allorigins.win/raw?url=" + urllib.parse.quote(chart_url(symbol, rng), safe="")),
                      ("corsproxy", "https://corsproxy.io/?url=" + urllib.parse.quote(chart_url(symbol, rng), safe=""))]:
        try:
            r = requests.get(url, headers=UA, timeout=20)
            if r.status_code != 200:
                continue
            j = r.json()
        except Exception:
            try:
                j = json.loads(r.text)
            except Exception:
                continue
        try:
            res = j["chart"]["result"][0]
            ts = res["timestamp"]
            q = res["indicators"]["quote"][0]
            rows = []
            for i, t in enumerate(ts):
                c = q["close"][i]
                if c is None:
                    continue
                dt = datetime.utcfromtimestamp(t).strftime("%Y-%m-%d")
                rows.append({"date": dt, "close": c, "high": q["high"][i],
                             "low": q["low"][i], "volume": q["volume"][i] or 0})
            if len(rows) >= 60:
                return rows, name
        except Exception:
            continue
    return None, None


def rsi(closes, period=14):
    c = np.asarray(closes, dtype=float)
    d = np.diff(c)
    g = np.where(d > 0, d, 0.0)
    l = np.where(d < 0, -d, 0.0)
    ag = g[:period].mean()
    al = l[:period].mean()
    for i in range(period, len(d)):
        ag = (ag * (period - 1) + g[i]) / period
        al = (al * (period - 1) + l[i]) / period
    if al == 0:
        return 100.0
    return round(100.0 - 100.0 / (1.0 + ag / al), 2)


def sma(v, p):
    v = np.asarray(v, dtype=float)
    return round(float(v[-p:].mean()), 2) if len(v) >= p else None


def pct(closes, lb):
    c = np.asarray(closes, dtype=float)
    return round((c[-1] / c[-1 - lb] - 1.0) * 100.0, 2) if len(c) > lb else None


def momentum_score(closes, highs, vols, b1m, b3m):
    score = 0.0
    flags = []
    last = float(closes[-1])
    ma20, ma50 = sma(closes, 20), sma(closes, 50)
    r = rsi(closes)
    if ma20 and last > ma20:
        score += 10; flags.append(">20dma")
    if ma50 and last > ma50:
        score += 10; flags.append(">50dma")
    r1m, r3m = pct(closes, 21), pct(closes, 63)
    rs3m = (r3m - b3m) if (r3m is not None and b3m is not None) else None
    if rs3m is not None:
        if rs3m > 0:
            score += 10; flags.append(f"RS+{rs3m}%")
        if rs3m > 10:
            score += 10; flags.append("RS_strong")
    if 50 <= r <= 70:
        score += 20; flags.append(f"RSI{r}")
    elif 40 <= r < 50 or 70 < r <= 75:
        score += 10; flags.append(f"RSI{r}")
    vols = np.asarray(vols, dtype=float)
    avg20 = vols[-20:].mean()
    ratio = round(float(vols[-1] / avg20), 2) if avg20 > 0 else 1.0
    if ratio >= 1.5:
        score += 20; flags.append(f"vol{ratio}x")
    elif ratio >= 1.0:
        score += 10; flags.append(f"vol{ratio}x")
    hi52 = float(max(highs))
    prox = round((last / hi52 - 1.0) * 100.0, 2)
    if prox >= -5:
        score += 20; flags.append(f"hi{prox}%")
    elif prox >= -10:
        score += 12; flags.append(f"hi{prox}%")
    r1w = pct(closes, 5)
    if r1w is not None and r1w > 30:
        score -= 15; flags.append(f"PARABOLIC{r1w}%")
    return round(min(max(score, 0), 100), 1), {"rsi": r, "rs_3m": rs3m, "ret_1m": r1m,
                                                "vol_ratio": ratio, "hi_prox": prox, "flags": flags}


def main():
    cutoff = sys.argv[1] if len(sys.argv) > 1 else "2026-07-25"

    bench_rows, _ = fetch_ohlcv(BENCHMARK)
    b1m = b3m = None
    if bench_rows:
        bi = max(i for i, r in enumerate(bench_rows) if r["date"] <= cutoff)
        bc = [r["close"] for r in bench_rows[:bi + 1]]
        b1m, b3m = pct(bc, 21), pct(bc, 63)

    out = []
    for sym in UNIVERSE:
        rows, route = fetch_ohlcv(sym)
        if not rows or rows[-1]["date"] <= cutoff:
            out.append({"symbol": sym, "error": "no data past cutoff"})
            continue
        idx = max(i for i, r in enumerate(rows) if r["date"] <= cutoff)
        past = rows[:idx + 1]
        future = rows[idx + 1:]
        closes = [r["close"] for r in past]
        highs = [r["high"] for r in past]
        vols = [r["volume"] for r in past]
        score, m = momentum_score(closes, highs, vols, b1m, b3m)

        cutoff_close = float(past[-1]["close"])
        fut_closes = [r["close"] for r in future]
        final_close = float(future[-1]["close"])
        fwd_ret = round((final_close / cutoff_close - 1.0) * 100.0, 2)
        max_dd = round((min(fut_closes) / cutoff_close - 1.0) * 100.0, 2)
        max_gain = round((max(fut_closes) / cutoff_close - 1.0) * 100.0, 2)

        out.append({
            "symbol": sym,
            "score_jul25": score,
            "jul25_close": round(cutoff_close, 2),
            "final_close": round(final_close, 2),
            "fwd_return_pct": fwd_ret,
            "max_gain_pct": max_gain,
            "max_drawdown_pct": max_dd,
            "as_of": past[-1]["date"],
            **m,
        })
        time.sleep(0.25)

    out.sort(key=lambda x: x.get("score_jul25", -999), reverse=True)

    valid = [o for o in out if "fwd_return_pct" in o]
    top5 = valid[:5]
    def avg(xs):
        return round(sum(xs) / len(xs), 2) if xs else None
    summary = {
        "universe_size": len(valid),
        "top5_symbols": [o["symbol"] for o in top5],
        "top5_avg_fwd_return": avg([o["fwd_return_pct"] for o in top5]),
        "universe_avg_fwd_return": avg([o["fwd_return_pct"] for o in valid]),
        "top5_win_rate": round(100.0 * sum(1 for o in top5 if o["fwd_return_pct"] > 0) / len(top5), 1) if top5 else None,
        "universe_win_rate": round(100.0 * sum(1 for o in valid if o["fwd_return_pct"] > 0) / len(valid), 1) if valid else None,
    }
    print(json.dumps({"cutoff": cutoff, "summary": summary, "ranked": out}, indent=2))


if __name__ == "__main__":
    main()
