"""
Trading Agent — Fallback OHLCV Fetcher
Tries multiple routes to get daily OHLCV when yfinance is rate-limited:
  1. Direct Yahoo chart API (may be IP rate-limited)
  2. allorigins proxy -> Yahoo chart API
  3. corsproxy.io -> Yahoo chart API
Writes the SAME CSV format as fetch_data.py so indicators.py works unchanged.
Usage: python fetch_fallback.py <SYMBOL> [range]
Example: python fetch_fallback.py BEL.NS 6mo
"""
import sys
import os
import json
import time
from datetime import datetime

import requests

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"}


def yahoo_chart_url(symbol, rng):
    return f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={rng}&interval=1d&events=div%2Csplits"


def parse_chart(json_data):
    try:
        res = json_data["chart"]["result"][0]
        ts = res["timestamp"]
        q = res["indicators"]["quote"][0]
        o = q["open"]
        h = q["high"]
        l = q["low"]
        c = q["close"]
        v = q["volume"]
        rows = []
        for i, t in enumerate(ts):
            if c[i] is None:
                continue
            dt = datetime.utcfromtimestamp(t).strftime("%Y-%m-%d")
            rows.append((dt, o[i], h[i], l[i], c[i], v[i] if v[i] else 0))
        return rows
    except Exception as e:
        return None


def try_get(url, timeout=20):
    try:
        r = requests.get(url, headers=UA, timeout=timeout)
        if r.status_code == 200:
            return r
    except Exception:
        return None
    return None


def fetch(symbol, rng="6mo"):
    symbol = symbol.upper()
    if not (symbol.endswith(".NS") or symbol.endswith(".BO")):
        symbol += ".NS"

    import urllib.parse

    routes = [
        ("direct", yahoo_chart_url(symbol, rng)),
        ("allorigins", "https://api.allorigins.win/raw?url=" + urllib.parse.quote(yahoo_chart_url(symbol, rng), safe="")),
        ("corsproxy", "https://corsproxy.io/?url=" + urllib.parse.quote(yahoo_chart_url(symbol, rng), safe="")),
    ]

    rows = None
    used_route = None
    for name, url in routes:
        r = try_get(url)
        if r is None:
            continue
        try:
            j = r.json()
        except Exception:
            # corsproxy sometimes wraps in text
            try:
                j = json.loads(r.text)
            except Exception:
                continue
        parsed = parse_chart(j)
        if parsed and len(parsed) >= 30:
            rows = parsed
            used_route = name
            break
        time.sleep(0.5)

    if not rows:
        print(json.dumps({"error": f"All routes failed for {symbol}"}))
        sys.exit(1)

    outdir = "/home/z/my-project/download/trading-agent/data"
    os.makedirs(outdir, exist_ok=True)
    csv_path = os.path.join(outdir, f"{symbol.replace('.', '_')}_fallback_{rng}.csv")

    lines = ["Date,open,high,low,close,volume"]
    for dt, o, h, l, c, v in rows:
        lines.append(f"{dt},{o},{h},{l},{c},{v}")
    with open(csv_path, "w") as f:
        f.write("\n".join(lines))

    closes = [x[4] for x in rows]
    highs = [x[2] for x in rows]
    lows = [x[3] for x in rows]
    vols = [x[5] for x in rows]

    result = {
        "symbol": symbol,
        "route": used_route,
        "data_points": len(rows),
        "csv_path": csv_path,
        "last_close": round(float(closes[-1]), 2),
        "first_date": rows[0][0],
        "last_date": rows[-1][0],
        "high": round(float(max(highs)), 2),
        "low": round(float(min(lows)), 2),
        "avg_volume": int(sum(vols) / len(vols)),
        "last_volume": int(vols[-1]),
    }
    print(json.dumps(result, indent=2))
    return csv_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_fallback.py <SYMBOL> [range]")
        sys.exit(1)
    sym = sys.argv[1]
    rng = sys.argv[2] if len(sys.argv) > 2 else "6mo"
    fetch(sym, rng)
