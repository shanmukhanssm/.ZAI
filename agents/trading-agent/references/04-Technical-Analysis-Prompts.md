# SpringPad's Technical Analysis Prompts

Three prompts for fetching, analyzing, and backtesting stock market data.

---

## Prompt 1: Fetch Data

**Tool to use:** https://claude.ai/

**Prompt:**

```
Give me code to Download [INDEX] from [start date] to [end date] Historical Data
from yfinance Library into an excel sheet in csv format, define time using
timedelta function.
```

**Steps:**
1. Go to claude.ai and paste this prompt
2. Write the index or stock name along with the time horizon
3. Hit enter
4. Copy the Python code Claude generates
5. Go to colab.research.google.com -> New Notebook -> Paste code -> Run
6. The data will be downloaded in CSV/Excel format

---

## Prompt 2: Analyze Data

**Tool to use:** Market Analyst Pro by SpringPad (Custom ChatGPT)
https://chatgpt.com/g/g-SikxQaVjz-market-analyst-pro-by-springpad

**Prompt:**

```
Do the following analysis for [INDEX/STOCK NAME] with the data attached.

1. Introduction to the Dataset:
   - "Can you describe the dataset including its features and date range?"

2. Basic Data Analysis:
   - "Please provide summary statistics for the [INDEX] over the last [N] years."

3. Trend Analysis:
   - "Can you identify any trends in the [INDEX] data over the past [N] years?
     Plot a Line Chart"

4. Volatility Analysis:
   - "Assess the volatility of the [INDEX] based on the historical data provided.
     Also represent it graphically"

5. Advanced Analysis:
   - "Perform a moving average analysis on the [INDEX] data."

6. Comparative Analysis:
   - "Compare the yearly performance of the [INDEX] for the past [N] years."
   - "Give monthly % returns for [INDEX] using a heat map (positive with green
     and negative with red) for the past [N] years"

7. Seasonal Patterns:
   - "Analyze if there are any seasonal trends in the [INDEX] data that recur
     annually with the help of chart and also explain the possible reasons for it"
```

**Steps:**
1. Open Market Analyst Pro by SpringPad (custom ChatGPT)
2. Paste Prompt 2 along with the uploaded Excel file
3. Hit enter -- ChatGPT generates graphs and analysis

---

## Prompt 3: Backtest Data

**Tool to use:** https://claude.ai/

**Prompt:**

```
1) Take the past 8 years of historical data and calculate the 21 and 50 simple
   moving averages, representing the data in different columns.

2) We want to build a moving average crossover strategy for 21 and 50 DMA,
   implement the same and give the entry and exit signals.
   BUY signal = when 21 DMA crosses over 50 DMA from below
   SELL Signal = when 21 DMA crosses under 50 DMA from above
   Show the Buy signal with +1 and Sell Signal with -1, No signal means 0.

3) Now let's backtest this strategy, assuming we have a starting capital of
   Rs. 2,00,000. Show the Profit and Loss of each trade in the excel sheet.
   Trade with 1 lot of Nifty Futures = 50 shares.
   Take both long and short side trades.

4) Give the list of each trade. Also mention total number of trades, Number
   of profitable trades, Number of loss trades, Compounded returns.

In the end, Show me in detail in a dashboard the list of trades, equity curve,
strategy stats and also pros and cons of the strategy and possible ways of
improving it. Let me know if the Strategy is profitable and also how much
Profit/loss was made in both absolute and percentage terms.
```

**Steps:**
1. Go to claude.ai
2. Paste Prompt 3 along with the uploaded Excel file
3. Hit enter -- Claude backtests the strategy and generates a dashboard
