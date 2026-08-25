"""
Trading Agent — Momentum Ranker
Scores and ranks a list of NSE symbols by momentum strength, so we can catch
moves in their EARLY stage instead of chasing stocks that have already run.

Momentum score (0-100) = Trend + Relative Strength (vs Nifty) + RSI sweet spot
                         + Volume expansion + 52w-high proximity − parabolic penalty.

Usage:
  python momentum_rank.py CUPID.NS BAJAJHIND.NS WEL.NS BEL.NS ASHOKLEY.NS
  python momentum_rank.py @symbols.txt        (one symbol per line)

Output: JSON array ranked by momentum_score (best first), printed to stdout.
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
BENCHMARK = "^NSEI"  # Nifty 50 on Yahoo Finance


def chart_url(symbol, rng="1y"):
    return f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}?range={rng}&interval=1d&events=div%2Csplits"


def fetch_ohlcv(symbol, rng="1y"):
    """Return list of [date, open, high, low, close, volume] or None."""
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
                rows.append([dt, q["open"][i], q["high"][i], q["low"][i], c, q["volume"][i] or 0])
            if len(rows) >= 60:
                return rows, name
        except Exception:
            continue
    return None, None


def rsi(closes, period=14):
    closes = np.asarray(closes, dtype=float)
    deltas = np.diff(closes)
    gains = np.where(deltas > 0, deltas, 0.0)
    losses = np.where(deltas < 0, -deltas, 0.0)
    avg_gain = gains[:period].mean()
    avg_loss = losses[:period].mean()
    for i in range(period, len(deltas)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    if avg_loss == 0:
        return 100.0
    return round(100.0 - 100.0 / (1.0 + avg_gain / avg_loss), 2)


def sma(values, period):
    v = np.asarray(values, dtype=float)
    return round(float(v[-period:].mean()), 2) if len(v) >= period else None


def pct_return(closes, lookback):
    c = np.asarray(closes, dtype=float)
    if len(c) <= lookback:
        return None
    return round((c[-1] / c[-1 - lookback] - 1.0) * 100.0, 2)


def score_stock(closes, highs, vols, bench_1m, bench_3m):
    """Compute momentum score 0-100 for a single stock."""
    score = 0.0
    flags = []

    last = float(closes[-1])
    ma20 = sma(closes, 20)
    ma50 = sma(closes, 50)
    r = rsi(closes)

    # 1. Trend (20 pts): above 20/50 DMA
    if ma20 and last > ma20:
        score += 10; flags.append("above_20dma")
    if ma50 and last > ma50:
        score += 10; flags.append("above_50dma")

    # 2. Relative strength vs Nifty (20 pts)
    r1m = pct_return(closes, 21)
    r3m = pct_return(closes, 63)
    rs3m = (r3m - bench_3m) if (r3m is not None and bench_3m is not None) else None
    if rs3m is not None:
        if rs3m > 0:
            score += 10; flags.append(f"RS3m+{rs3m}%")
        if rs3m > 10:
            score += 10; flags.append("RS_strong")

    # 3. RSI sweet spot (20 pts)
    if 50 <= r <= 70:
        score += 20; flags.append(f"RSI_{r}")
    elif 40 <= r < 50 or 70 < r <= 75:
        score += 10; flags.append(f"RSI_{r}_edge")

    # 4. Volume expansion (20 pts)
    vols = np.asarray(vols, dtype=float)
    avg20 = vols[-20:].mean()
    last_vol = vols[-1]
    ratio = round(float(last_vol / avg20), 2) if avg20 > 0 else 1.0
    if ratio >= 1.5:
        score += 20; flags.append(f"vol_x{ratio}")
    elif ratio >= 1.0:
        score += 10; flags.append(f"vol_x{ratio}")

    # 5. 52w-high proximity + parabolic penalty (20 pts)
    hi52 = float(max(highs))
    prox = round((last / hi52 - 1.0) * 100.0, 2)  # negative = below high
    if prox >= -5:
        score += 20; flags.append(f"near_high_{prox}%")
    elif prox >= -10:
        score += 12; flags.append(f"near_high_{prox}%")
    r1w = pct_return(closes, 5)
    if r1w is not None and r1w > 30:
        score -= 15; flags.append(f"PARABOLIC_{r1w}%1w")

    return round(min(max(score, 0), 100), 1), {
        "last_close": round(last, 2),
        "rsi_14": r,
        "ma20": ma20, "ma50": ma50,
        "ret_1m": r1m, "ret_3m": r3m, "rs_3m": rs3m,
        "vol_ratio": ratio,
        "pct_from_52w_high": prox,
        "ret_1w": r1w,
        "flags": flags,
    }


def main():
    args = sys.argv[1:]
    symbols = []
    for a in args:
        if a.startswith("@"):
            with open(a[1:], encoding="utf-8") as f:
                symbols += [ln.strip() for ln in f if ln.strip()]
        else:
            symbols.append(a)
    symbols = [s.upper() if s.endswith((".NS", ".BO")) else s.upper() + ".NS" for s in symbols]
    if not symbols:
        print(json.dumps({"error": "No symbols given. Usage: momentum_rank.py CUPID.NS BAJAJHIND.NS ..."}))
        sys.exit(1)

    # benchmark (Nifty)
    bench_rows, _ = fetch_ohlcv(BENCHMARK)
    if bench_rows:
        bcloses = [r[4] for r in bench_rows]
        bench_1m = pct_return(bcloses, 21)
        bench_3m = pct_return(bcloses, 63)
    else:
        bench_1m = bench_3m = None

    results = []
    for sym in symbols:
        rows, route = fetch_ohlcv(sym)
        if not rows:
            results.append({"symbol": sym, "error": "fetch failed"})
            continue
        closes = [r[4] for r in rows]
        highs = [r[2] for r in rows]
        vols = [r[5] for r in rows]
        score, metrics = score_stock(closes, highs, vols, bench_1m, bench_3m)
        metrics["route"] = route
        metrics["data_points"] = len(rows)
        metrics["last_date"] = rows[-1][0]
        results.append({"symbol": sym, "momentum_score": score, **metrics})
        time.sleep(0.3)

    results.sort(key=lambda x: x.get("momentum_score", -999), reverse=True)
    print(json.dumps({"benchmark": {"nifty_1m": bench_1m, "nifty_3m": bench_3m},
                      "ranked": results}, indent=2))


if __name__ == "__main__":
    main()
