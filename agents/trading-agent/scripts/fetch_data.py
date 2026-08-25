"""
Trading Agent — Data Fetcher
Downloads OHLCV data from yfinance for NSE/BSE stocks.
Usage: python fetch_data.py <SYMBOL> [start_date] [end_date]
Example: python fetch_data.py TCS.NS 2026-01-01 2026-08-09
"""

import sys
import os
from datetime import datetime, timedelta

def install_yfinance():
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance", "-q"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas", "-q"])

def fetch(symbol, start_date, end_date):
    try:
        import yfinance as yf
        import pandas as pd
    except ImportError:
        install_yfinance()
        import yfinance as yf
        import pandas as pd

    ticker = yf.Ticker(symbol)

    try:
        info = ticker.info
    except Exception:
        info = {}

    current_price = info.get("currentPrice") or info.get("regularMarketPrice") or info.get("previousClose")
    if current_price is None:
        try:
            hist_quick = ticker.history(period="5d")
            if not hist_quick.empty:
                current_price = float(hist_quick["Close"].iloc[-1])
        except Exception:
            current_price = None

    df = ticker.history(start=start_date, end=end_date)

    if df.empty:
        print(f"ERROR: No data found for {symbol} in range {start_date} to {end_date}")
        sys.exit(1)

    df = df.reset_index()
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    df.rename(columns={
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    }, inplace=True)

    cols = ["Date", "open", "high", "low", "close", "volume"]
    df = df[[c for c in cols if c in df.columns]]

    outdir = "/home/z/my-project/download/trading-agent/data"
    os.makedirs(outdir, exist_ok=True)

    csv_path = os.path.join(outdir, f"{symbol.replace('.', '_')}_{start_date}_{end_date}.csv")
    df.to_csv(csv_path, index=False)

    result = {
        "symbol": symbol,
        "current_price": round(current_price, 2) if current_price else None,
        "data_points": len(df),
        "start": start_date,
        "end": end_date,
        "csv_path": csv_path,
        "first_close": round(float(df["close"].iloc[0]), 2),
        "last_close": round(float(df["close"].iloc[-1]), 2),
        "high_52w": round(float(df["high"].max()), 2),
        "low_52w": round(float(df["low"].min()), 2),
        "avg_volume": int(df["volume"].mean()),
        "last_volume": int(df["volume"].iloc[-1])
    }

    import json
    json_path = csv_path.replace(".csv", "_meta.json")
    with open(json_path, "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))
    return csv_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_data.py <SYMBOL> [start_date] [end_date]")
        print("Example: python fetch_data.py TCS.NS 2026-01-01 2026-08-09")
        sys.exit(1)

    symbol = sys.argv[1].upper()
    if not (symbol.endswith(".NS") or symbol.endswith(".BO")):
        symbol = symbol + ".NS"

    end_date = sys.argv[3] if len(sys.argv) > 3 else datetime.now().strftime("%Y-%m-%d")
    start_date = sys.argv[2] if len(sys.argv) > 2 else (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

    fetch(symbol, start_date, end_date)
