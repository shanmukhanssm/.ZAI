# SpringPad's Moving Average Crossover Strategy

**Paste the below code in TradingView Pine Editor**

**Steps:**
1. Go to in.tradingview.com and open any stock/index chart
2. Copy the code below
3. Paste it in the Pine Editor in TradingView
4. Click "Add to chart" -- this will overlay the strategy on your chart

---

## CODE

```pinescript
// @version=5
strategy("Moving Average Crossover Strategy", shorttitle="MA Crossover", overlay=true)

// --- INPUTS ---
fastLength = input.int(9, title="Fast MA Length", minval=1)
slowLength = input.int(21, title="Slow MA Length", minval=1)
maType     = input.string(title="MA Type", defval="SMA", options=["SMA", "EMA", "WMA", "VWMA"])

// --- FUNCTION TO RETURN SELECTED MA ---
f_ma(_source, _length, _type) => switch _type
    "SMA"  => ta.sma(_source, _length)
    "EMA"  => ta.ema(_source, _length)
    "WMA"  => ta.wma(_source, _length)
    "VWMA" => ta.vwma(_source, _length)

// --- CALCULATE FAST AND SLOW MAs ---
fastMA = f_ma(close, fastLength, maType)
slowMA = f_ma(close, slowLength, maType)

// --- PLOT THE MOVING AVERAGES ---
plot(fastMA, color=color.blue, linewidth=2, title="Fast MA")
plot(slowMA, color=color.red, linewidth=2, title="Slow MA")

// --- TRADING CONDITIONS ---
longCondition = ta.crossover(fastMA, slowMA)
exitCondition = ta.crossunder(fastMA, slowMA)

// --- EXECUTE TRADES ---
if longCondition
    strategy.entry("Long Entry", strategy.long)

if exitCondition
    strategy.close("Long Entry")

// --- PLOT BUY/SELL LABELS ---
if longCondition
    label.new(bar_index, low, style=label.style_label_up, color=color.new(color.green, 0), textcolor=color.white, text="Buy")

if exitCondition
    label.new(bar_index, high, style=label.style_label_down, color=color.new(color.red, 0), textcolor=color.white, text="Sell")
```

---

### Strategy Summary

| Parameter | Default Value |
|-----------|--------------|
| Fast MA Length | 9 periods |
| Slow MA Length | 21 periods |
| MA Type | SMA (options: SMA, EMA, WMA, VWMA) |
| Entry Signal | Fast MA crosses ABOVE Slow MA (BUY) |
| Exit Signal | Fast MA crosses BELOW Slow MA (SELL) |

### How It Works:
- When the fast moving average (blue line) crosses above the slow moving average (red line), a **BUY** signal is generated
- When the fast MA crosses below the slow MA, a **SELL** signal is generated
- Buy/Sell labels appear directly on the chart for visual confirmation
- The strategy can be backtested directly in TradingView using the Strategy Tester tab

### Customization:
- Adjust `fastLength` to make signals more/less sensitive (higher = fewer signals, lower = more signals)
- Adjust `slowLength` similarly
- Change `maType` to EMA for more responsive signals or WMA/VWMA for volume-weighted signals
