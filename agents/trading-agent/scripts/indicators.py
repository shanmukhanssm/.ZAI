"""
Trading Agent — Technical Indicators Calculator
Calculates RSI, MACD, Moving Averages, ATR, Support/Resistance from OHLCV CSV.
Usage: python indicators.py <csv_path>
Example: python indicators.py data\TCS_NS_2026-01-01_2026-08-09.csv
"""

import sys
import json
import os


def install_deps():
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas", "numpy", "-q"])


def compute_indicators(csv_path):
    try:
        import pandas as pd
        import numpy as np
    except ImportError:
        install_deps()
        import pandas as pd
        import numpy as np

    if not os.path.exists(csv_path):
        print(json.dumps({"error": f"File not found: {csv_path}"}))
        sys.exit(1)

    df = pd.read_csv(csv_path)

    required = ["close", "high", "low"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        print(json.dumps({"error": f"CSV missing columns: {missing}. Found: {list(df.columns)}"}))
        sys.exit(1)

    close = df["close"].values.astype(float)
    high = df["high"].values.astype(float)
    low = df["low"].values.astype(float)
    volume = df["volume"].values.astype(float) if "volume" in df.columns else np.zeros_like(close)

    result = {}
    last_close = float(close[-1])

    def rsi(prices, period=14):
        deltas = np.diff(prices)
        seed = deltas[:period]
        up = seed[seed >= 0].sum() / period
        down = -seed[seed < 0].sum() / period
        if down == 0:
            rs = float('inf')
        else:
            rs = up / down
        rsi_values = np.full(len(prices), np.nan)
        rsi_values[period] = 100.0 - (100.0 / (1.0 + rs))
        for i in range(period + 1, len(prices)):
            delta = deltas[i - 1]
            upval = delta if delta > 0 else 0
            downval = -delta if delta < 0 else 0
            up = (up * (period - 1) + upval) / period
            down = (down * (period - 1) + downval) / period
            if down == 0:
                rs = float('inf')
            else:
                rs = up / down
            rsi_values[i] = 100.0 - (100.0 / (1.0 + rs))
        return round(float(rsi_values[-1]), 2)

    def sma(prices, period):
        if len(prices) < period:
            return None
        return round(float(np.mean(prices[-period:])), 2)

    def ema(prices, period):
        if len(prices) < period:
            return None
        alpha = 2.0 / (period + 1)
        ema_val = np.mean(prices[:period])
        for p in prices[period:]:
            ema_val = alpha * p + (1 - alpha) * ema_val
        return round(float(ema_val), 2)

    def macd(prices):
        ema12 = ema(prices, 12)
        ema26 = ema(prices, 26)
        if ema12 is None or ema26 is None:
            return None, None, None
        macd_line = ema12 - ema26

        prices_extended = list(prices) + [prices[-1]]
        macd_vals = []
        for i in range(26, len(prices_extended)):
            e12 = ema(prices_extended[:i+1], 12)
            e26 = ema(prices_extended[:i+1], 26)
            if e12 and e26:
                macd_vals.append(e12 - e26)

        if len(macd_vals) >= 9:
            signal_line = ema(np.array(macd_vals), 9)
        else:
            signal_line = macd_line

        histogram = round(macd_line - signal_line, 2) if signal_line else None
        return round(macd_line, 2), round(signal_line, 2) if signal_line else None, histogram

    def atr(high_prices, low_prices, close_prices, period=14):
        if len(close_prices) < period + 1:
            return None
        tr = []
        for i in range(1, len(close_prices)):
            h_l = high_prices[i] - low_prices[i]
            h_pc = abs(high_prices[i] - close_prices[i-1])
            l_pc = abs(low_prices[i] - close_prices[i-1])
            tr.append(max(h_l, h_pc, l_pc))
        return round(float(np.mean(tr[-period:])), 2)

    def find_support_resistance(prices, window=20):
        n = len(prices)
        if n < window * 2:
            return None, None
        supports = []
        resistances = []
        for i in range(window, n - window):
            is_support = low[i] == min(low[i-window:i+window+1])
            is_resistance = high[i] == max(high[i-window:i+window+1])
            if is_support:
                supports.append(round(float(low[i]), 2))
            if is_resistance:
                resistances.append(round(float(high[i]), 2))

        if supports:
            supports.sort()
            support = supports[-1] if supports else None
            support = round(float(np.mean([s for s in supports if s >= support - support * 0.02])), 2) if support else None
        else:
            support = None

        if resistances:
            resistances.sort()
            resistance = resistances[0] if resistances else None
            resistance = round(float(np.mean([r for r in resistances if r <= resistance + resistance * 0.02])), 2) if resistance else None
        else:
            resistance = None

        return support, resistance

    def volume_analysis(volumes, close_prices, period=20):
        if len(volumes) < period:
            return None, None, None
        avg_vol = np.mean(volumes[-period:])
        last_vol = volumes[-1]
        vol_ratio = round(float(last_vol / avg_vol), 2) if avg_vol > 0 else 1.0
        price_direction = "up" if close_prices[-1] > close_prices[-2] else "down" if close_prices[-1] < close_prices[-2] else "flat"
        return round(float(avg_vol), 0), round(float(last_vol), 0), {"ratio": vol_ratio, "direction": price_direction}

    def trend_analysis(prices, ma20, ma50, ma200):
        if ma20 is None:
            return "insufficient_data"

        above_20 = last_close > ma20
        above_50 = last_close > ma50 if ma50 else None
        above_200 = last_close > ma200 if ma200 else None

        if above_20 and (above_50 is not False) and (above_200 is not False):
            if ma50 and ma200 and ma20 > ma50 > ma200:
                return "strong_uptrend"
            return "uptrend"
        elif not above_20 and (above_50 is not True) and (above_200 is not True):
            if ma50 and ma200 and ma20 < ma50 < ma200:
                return "strong_downtrend"
            return "downtrend"
        elif above_20 and above_50 is False:
            return "recovering"
        elif not above_20 and (above_50 is not False):
            return "correcting"
        return "sideways"

    ma20_val = sma(close, 20)
    ma50_val = sma(close, 50)
    ma200_val = sma(close, 200)
    rsi_val = rsi(close, 14)
    macd_line, signal_line, histogram = macd(close)
    atr_val = atr(high, low, close, 14)
    support, resistance = find_support_resistance(close, 20)
    avg_vol, last_vol, vol_info = volume_analysis(volume, close, 20)
    trend = trend_analysis(close, ma20_val, ma50_val, ma200_val)

    result = {
        "symbol": os.path.basename(csv_path).split("_")[0] if "_" in csv_path else csv_path,
        "last_close": last_close,
        "data_points": len(close),
        "moving_averages": {
            "20_dma": ma20_val,
            "50_dma": ma50_val,
            "200_dma": ma200_val,
            "price_vs_20dma": round(last_close - ma20_val, 2) if ma20_val else None,
            "price_vs_20dma_pct": round(((last_close - ma20_val) / ma20_val) * 100, 2) if ma20_val else None,
        },
        "rsi_14": rsi_val,
        "macd": {
            "macd_line": macd_line,
            "signal_line": signal_line,
            "histogram": histogram,
            "signal": "bullish" if histogram and histogram > 0 else "bearish" if histogram and histogram < 0 else "neutral"
        },
        "atr_14": atr_val,
        "support_resistance": {
            "nearest_support": support,
            "nearest_resistance": resistance
        },
        "volume": {
            "avg_20d": int(avg_vol) if avg_vol else None,
            "last": int(last_vol) if last_vol else None,
            "ratio_vs_avg": vol_info.get("ratio") if vol_info else None,
            "last_day_direction": vol_info.get("direction") if vol_info else None
        },
        "trend": trend,
        "entry_zone": None,
        "stoploss_suggestion": None,
        "target_suggestion": None
    }

    if support and last_close > support:
        zone_width = atr_val * 0.5 if atr_val else support * 0.02
        result["entry_zone"] = [round(support + zone_width * 0.3, 2), round(support + zone_width * 2, 2)]
        result["stoploss_suggestion"] = round(support - atr_val * 0.5, 2) if atr_val else round(support * 0.97, 2)
    if resistance:
        result["target_suggestion"] = [resistance, round(resistance * 1.05, 2)] if resistance else None

    if result["stoploss_suggestion"] and result["entry_zone"]:
        entry_mid = (result["entry_zone"][0] + result["entry_zone"][1]) / 2
        risk = entry_mid - result["stoploss_suggestion"]
        reward = result["target_suggestion"][0] - entry_mid if result["target_suggestion"] else None
        result["risk_reward"] = round(reward / risk, 2) if risk > 0 and reward else None

    result["signals"] = []
    if rsi_val and rsi_val < 35:
        result["signals"].append("rsci_oversold")
    if rsi_val and rsi_val > 75:
        result["signals"].append("rsi_overbought")
    if histogram and histogram > 0:
        result["signals"].append("macd_bullish")
    if histogram and histogram < 0:
        result["signals"].append("macd_bearish")
    if trend and "uptrend" in trend:
        result["signals"].append("trend_bullish")
    if trend and "downtrend" in trend:
        result["signals"].append("trend_bearish")
    if vol_info and vol_info.get("ratio", 0) > 1.5 and vol_info.get("direction") == "up":
        result["signals"].append("high_volume_breakout")
    if ma20_val and ma50_val and ma20_val > ma50_val:
        result["signals"].append("golden_cross_20_50")
    if ma20_val and ma50_val and ma20_val < ma50_val:
        result["signals"].append("death_cross_20_50")

    outdir = os.path.dirname(csv_path)
    json_path = os.path.join(outdir, os.path.basename(csv_path).replace(".csv", "_indicators.json"))
    with open(json_path, "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python indicators.py <csv_path>")
        print("Example: python indicators.py data/TCS_NS_2026-01-01_2026-08-09.csv")
        sys.exit(1)

    compute_indicators(sys.argv[1])
