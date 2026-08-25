"""
Trading Agent — NSE Historical Data Fetcher (fallback when yfinance is rate-limited)
Fetches daily OHLCV from NSE India's historical API.
Writes the SAME CSV format as fetch_data.py so indicators.py works unchanged.
Usage: python fetch_nse.py <SYMBOL> [start_YYYY-MM-DD] [end_YYYY-MM-DD]
Example: python fetch_nse.py BEL 2025-08-20 2026-08-20
"""
import sys
import os
import json
import time
from datetime import datetime, timedelta

import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/get-quotes/equity",
}


def get_session():
    s = requests.Session()
    s.headers.update(HEADERS)
    try:
        s.get("https://www.nseindia.com", timeout=15)
    except Exception:
        pass
    time.sleep(1)
    return s


def to_nse_dt(iso):
    # NSE wants DD-MM-YYYY
    return datetime.strptime(iso, "%Y-%m-%d").strftime("%d-%m-%Y")


def fetch(symbol, start_date, end_date):
    symbol = symbol.upper().replace(".NS", "").replace(".BO", "")
    session = get_session()

    url = "https://www.nseindia.com/api/historical/cm/equity"
    params = {
        "symbol": symbol,
        "series": '["EQ"]',
        "from": to_nse_dt(start_date),
        "to": to_nse_dt(end_date),
    }

    r = session.get(url, params=params, timeout=20)
    if r.status_code != 200:
        print(json.dumps({"error": f"NSE HTTP {r.status_code}", "body": r.text[:300]}))
        sys.exit(1)

    data = r.json()
    if "data" not in data:
        print(json.dumps({"error": "NSE returned no 'data' key", "keys": list(data.keys())}))
        sys.exit(1)

    rows = data["data"]
    if not rows:
        print(json.dumps({"error": f"No data for {symbol} in range"}))
        sys.exit(1)

    # rows come newest-first; reverse to oldest-first
    rows = list(reversed(rows))

    outdir = os.path.join(os.path.expanduser("~"), ".opencode", "trading", "data")
    os.makedirs(outdir, exist_ok=True)

    csv_path = os.path.join(outdir, f"{symbol}_NS_{start_date}_{end_date}.csv")
    lines = ["Date,open,high,low,close,volume"]
    for row in rows:
        meta = row.get("CH_TIMESTAMP", "")  # DD-MM-YYYY
        try:
            d = datetime.strptime(meta, "%d-%m-%Y").strftime("%Y-%m-%d")
        except Exception:
            d = meta
        o = row["CH_OPENING_PRICE"]
        h = row["CH_TRADE_HIGH_PRICE"]
        l = row["CH_TRADE_LOW_PRICE"]
        c = row["CH_CLOSING_PRICE"]
        v = row["CH_TOT_TRADED_QTY"]
        lines.append(f"{d},{o},{h},{l},{c},{v}")

    with open(csv_path, "w") as f:
        f.write("\n".join(lines))

    closes = [float(x["CH_CLOSING_PRICE"]) for x in rows]
    highs = [float(x["CH_TRADE_HIGH_PRICE"]) for x in rows]
    lows = [float(x["CH_TRADE_LOW_PRICE"]) for x in rows]
    vols = [float(x["CH_TOT_TRADED_QTY"]) for x in rows]

    result = {
        "symbol": symbol + ".NS",
        "current_price": round(closes[-1], 2),
        "data_points": len(rows),
        "start": start_date,
        "end": end_date,
        "csv_path": csv_path,
        "first_close": round(closes[0], 2),
        "last_close": round(closes[-1], 2),
        "high_52w": round(max(highs), 2),
        "low_52w": round(min(lows), 2),
        "avg_volume": int(sum(vols) / len(vols)),
        "last_volume": int(vols[-1]),
    }

    meta_path = csv_path.replace(".csv", "_meta.json")
    with open(meta_path, "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))
    return csv_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_nse.py <SYMBOL> [start_YYYY-MM-DD] [end_YYYY-MM-DD]")
        sys.exit(1)
    symbol = sys.argv[1].upper()
    end = sys.argv[3] if len(sys.argv) > 3 else datetime.now().strftime("%Y-%m-%d")
    start = sys.argv[2] if len(sys.argv) > 2 else (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    fetch(symbol, start, end)
