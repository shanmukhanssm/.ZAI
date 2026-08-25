"""
Trading Agent — Momentum Ranker v2 (improved)
Fixes the known flaws of v1:
  - Volume: smoothed 5-day average (not one noisy day)
  - RSI: adds DIRECTION (rising = building, falling = fading)
  - Adds ACCELERATION (is the move speeding up or coasting?)
  - Adds EXTENSION penalty (too far above 20/200 DMA = due for pullback)
  - Adds ATR volatility (risk context) and MARKET REGIME (risk-on/off)
  - Multi-horizon relative strength (1m + 3m vs Nifty)

Scoring (0-100, then penalties):
  TREND        25 pts  (above 20/50/200 DMA + 20-DMA slope rising)
  ACCELERATION 20 pts  (1-month return + is it faster than its own 3-month pace)
  REL STRENGTH 20 pts  (beating Nifty over 1m AND 3m)
  VOLUME       15 pts  (5-day vs 20-day average volume)
  RSI          20 pts  (sweet-spot position + direction)
  PENALTIES   -8/-20   (extension + parabolic)

Usage: python momentum_rank_v2.py CUPID.NS BAJAJHIND.NS ...   (or @file)
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
    if len(c) <= period:
        return None
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


def atr_pct(highs, lows, closes, period=14):
    h = np.asarray(highs, dtype=float)
    l = np.asarray(lows, dtype=float)
    c = np.asarray(closes, dtype=float)
    if len(c) <= period:
        return None
    tr = np.maximum(h[1:] - l[1:],
                    np.maximum(np.abs(h[1:] - c[:-1]), np.abs(l[1:] - c[:-1])))
    atr = float(tr[-period:].mean())
    return round(atr / c[-1] * 100.0, 2)  # ATR as % of price


def score_stock(closes, highs, lows, vols, b1m, b3m):
    """Return (score, metrics). Score 0-100 (can be reduced by penalties)."""
    score = 0.0
    flags = []
    last = float(closes[-1])

    ma20, ma50, ma200 = sma(closes, 20), sma(closes, 50), sma(closes, 200)
    r = rsi(closes)
    r_prev = rsi(closes[:-5]) if len(closes) > 19 else None

    # ---- 1. TREND (25 pts) ----
    if ma20 and last > ma20:
        score += 6; flags.append(">20dma")
    if ma50 and last > ma50:
        score += 6; flags.append(">50dma")
    if ma200 and last > ma200:
        score += 6; flags.append(">200dma")
    # 20-DMA slope: is the short-term trend itself RISING?
    ma20_10ago = sma(closes[:-10], 20) if len(closes) > 30 else None
    if ma20 and ma20_10ago and ma20 > ma20_10ago:
        score += 7; flags.append("20dma_rising")

    # ---- 2. ACCELERATION (20 pts) ----
    r1m, r3m = pct(closes, 21), pct(closes, 63)
    if r1m is not None:
        if r1m > 10:
            score += 10; flags.append(f"1m+{r1m}%")
        elif r1m > 5:
            score += 7; flags.append(f"1m+{r1m}%")
        elif r1m > 0:
            score += 4; flags.append(f"1m+{r1m}%")
    accel = None
    if r1m is not None and r3m is not None:
        accel = round(r1m - (r3m / 3.0), 2)  # is the last month FASTER than the 3-month pace?
        if accel > 0:
            score += 10; flags.append(f"accelerating+{accel}")
        elif accel < -5:
            score += 2; flags.append(f"decelerating{accel}")  # old momentum fading
        else:
            score += 5

    # ---- 3. RELATIVE STRENGTH vs Nifty (20 pts) ----
    rs1m = (r1m - b1m) if (r1m is not None and b1m is not None) else None
    rs3m = (r3m - b3m) if (r3m is not None and b3m is not None) else None
    if rs1m is not None:
        if rs1m > 0:
            score += 6; flags.append(f"RS1m+{rs1m}%")
        if rs1m > 5:
            score += 4; flags.append("RS1m_strong")
    if rs3m is not None:
        if rs3m > 0:
            score += 6; flags.append(f"RS3m+{rs3m}%")
        if rs3m > 10:
            score += 4; flags.append("RS3m_strong")

    # ---- 4. VOLUME (15 pts) — smoothed 5-day vs 20-day ----
    vols = np.asarray(vols, dtype=float)
    v5 = vols[-5:].mean()
    v20 = vols[-20:].mean()
    vratio = round(float(v5 / v20), 2) if v20 > 0 else 1.0
    if vratio > 1.5:
        score += 15; flags.append(f"vol5d_{vratio}x")
    elif vratio > 1.2:
        score += 10; flags.append(f"vol5d_{vratio}x")
    elif vratio > 0.8:
        score += 5; flags.append(f"vol5d_{vratio}x")
    else:
        flags.append(f"vol5d_{vratio}x_weak")

    # ---- 5. RSI POSITION + DIRECTION (20 pts) ----
    if r is not None:
        if 50 <= r <= 70:
            score += 14; flags.append(f"RSI{r}")
        elif (45 <= r < 50) or (70 < r <= 75):
            score += 7; flags.append(f"RSI{r}")
        # direction: RSI rising over last 5 sessions = momentum building
        if r_prev is not None and r > r_prev:
            score += 6; flags.append(f"RSI_rising({r_prev}->{r})")
        elif r_prev is not None and r < r_prev:
            flags.append(f"RSI_falling({r_prev}->{r})")

    # ---- PENALTIES (extension + parabolic) ----
    ext20 = round((last / ma20 - 1.0) * 100.0, 2) if ma20 else None
    ext200 = round((last / ma200 - 1.0) * 100.0, 2) if ma200 else None
    if ext20 is not None and ext20 > 15:
        score -= 8; flags.append(f"EXTENDED_{ext20}%>20dma")
    if ext200 is not None and ext200 > 40:
        score -= 8; flags.append(f"EXTENDED_{ext200}%>200dma")
    r1w = pct(closes, 5)
    if r1w is not None:
        if r1w > 30:
            score -= 20; flags.append(f"PARABOLIC_{r1w}%1w")
        elif r1w > 20:
            score -= 10; flags.append(f"parabolic-ish_{r1w}%1w")

    score = round(min(max(score, 0), 100), 1)
    vol = atr_pct(highs, lows, closes)

    # ---- VERDICT ----
    if r1w is not None and r1w > 30:
        verdict = "AVOID (parabolic)"
    elif r is not None and r > 78:
        verdict = "AVOID (overbought)"
    elif score >= 65:
        verdict = "BUY candidate"
    elif score >= 50:
        verdict = "WATCH"
    else:
        verdict = "AVOID (weak momentum)"

    return score, {
        "last_close": round(last, 2),
        "rsi_14": r, "rsi_5ago": r_prev,
        "ma20": ma20, "ma50": ma50, "ma200": ma200,
        "ret_1m": r1m, "ret_3m": r3m, "accel": accel,
        "rs_1m": rs1m, "rs_3m": rs3m,
        "vol_ratio_5d": vratio,
        "ext_above_20dma_pct": ext20, "ext_above_200dma_pct": ext200,
        "ret_1w": r1w, "atr_pct": vol,
        "verdict": verdict, "flags": flags,
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
        print(json.dumps({"error": "No symbols. Usage: momentum_rank_v2.py CUPID.NS ..."}))
        sys.exit(1)

    # benchmark (Nifty) + market regime (is Nifty above its own 50 DMA?)
    bench_rows, _ = fetch_ohlcv(BENCHMARK)
    b1m = b3m = None
    regime = "unknown"
    if bench_rows:
        bcloses = [r["close"] for r in bench_rows]
        b1m, b3m = pct(bcloses, 21), pct(bcloses, 63)
        bma50 = sma(bcloses, 50)
        regime = "RISK-ON" if (bma50 and bcloses[-1] > bma50) else "RISK-OFF"

    results = []
    for sym in symbols:
        rows, route = fetch_ohlcv(sym)
        if not rows:
            results.append({"symbol": sym, "error": "fetch failed"})
            continue
        closes = [r["close"] for r in rows]
        highs = [r["high"] for r in rows]
        lows = [r["low"] for r in rows]
        vols = [r["volume"] for r in rows]
        score, m = score_stock(closes, highs, lows, vols, b1m, b3m)
        m["route"] = route
        m["data_points"] = len(rows)
        m["last_date"] = rows[-1]["date"]
        results.append({"symbol": sym, "momentum_score": score, **m})
        time.sleep(0.25)

    results.sort(key=lambda x: x.get("momentum_score", -999), reverse=True)
    print(json.dumps({"benchmark": {"nifty_1m": b1m, "nifty_3m": b3m, "regime": regime},
                      "ranked": results}, indent=2))


if __name__ == "__main__":
    main()
