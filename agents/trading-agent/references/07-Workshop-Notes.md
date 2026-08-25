# SMAI Workshop Notes — Stock Market Using AI

**By SpringPad**

---

## Know Your Mentors

### Rahul Chandra (Co-Founder of SpringPad)
- 9+ years in global finance, expertise in Equity Research, Investment Banking, and Private Equity
- One of ~2,700 professionals globally to hold CFA, FRM, and CAIA charters
- Equity & Credit Research at TresVista and Moody's
- Investment Banking & Capital Markets at Goldman Sachs, Societe Generale, and EY
- Private Equity & VC Specialist at PwC
- Mentored 50,000+ students

### Pratik Chakraborty (Co-Founder of SpringPad)
- Trading Global Markets & Securities for 9+ Years
- Prop Trader at an Options desk in Mumbai (Managed 25 Cr)
- Futures Trader at a Global Hedge Fund in London (Managed $20 Million)
- Traded: Commodity futures (crude oil, Wheat, Soybean, Sugar, Copper), US/European Indices (S&P, Nasdaq, Dax, FTSE), Interest Rate Products, Indian Equities and F&O
- No prior coding knowledge — leveraged ChatGPT to create cutting-edge strategies

---

## Workshop Overview

The workshop covers AI-powered investing (Rahul Sir) and AI-powered trading (Pratik Sir), including live demonstrations of AI-built tools.

### Key Insight: The Rise of AI-Driven Trading
- Jane Street made $40 billion in trading revenue in 2024 (purely algorithmic) — more than all investment banks combined
- 80% of US retail investors use AI in investment research (BridgeWise Global survey)
- Graviton Research Capital (India) started with $1 million, now a unicorn valued at $1+ billion — built entirely on algorithmic/AI-driven trading
- India is still catching up — opportunity for early adopters

---

## Track 1: AI-Powered Investing (Rahul Sir)

### The Four-Step AI Investing Lifecycle

Professional investing follows a systematic process — not FOMO or news headlines. Goal: Build a five-stock growth portfolio using AI at every step.

### Step 1 — Identifying Growth Industries with Perplexity.ai

**Tool:** Perplexity.ai (Deep Research mode)

Using SpringPad's Growth Sector Deep Research Prompt, Perplexity:
- Analyzes macro indicators (GDP, inflation, repo rate, credit growth, government capex)
- Scores all 30-35 broad industries across 6 dimensions
- Ranks top 5 growth industries for the next 5 years
- Provides thesis, key players, catalysts, risks, CAGR estimates, valuation multiples, sector rotation heat maps, policy heat maps

**Steps:**
1. Go to perplexity.ai, create account
2. Copy the Growth Sector Deep Research Prompt
3. Change research type from "Auto" to "Deep Research"
4. Turn on "Academic" and "Social"
5. Paste and hit enter

### Step 2 — Industry Deep Dive & Stock Shortlisting

**Tool:** SpringPad's Industry Analysis & Stock Selector (Custom ChatGPT)
https://chatgpt.com/g/g-67d5fa2fc7088191be17bb6e680b4c04-springpads-industry-analysis-stock-selector-gpt

- Takes top 20 companies by market cap in each industry
- Scores across fundamentals, growth, technicals, sentiment, valuation, and risk
- Returns ranked shortlist of top 3 stocks per industry (15 total across 5 industries)

**Steps:**
1. Open the Market Analyst Pro by SpringPad
2. Type all five industry names together
3. Make sure Thinking Mode is on
4. Hit Enter — tool takes ~3-4 minutes

### Step 3 — Comparing & Selecting the Best Stock

**Tool:** Claude.ai (Sonnet or Opus + Web Search ON)

Uses a six-subject scoring matrix: Fundamentals, Financials, Price Performance & Track Record, Future Outlook, Technicals, Valuation. Each scored out of 5 (max 30).

Uses SpringPad's Company Comparison Deep Research Prompt (12-page structured prompt).

**Steps:**
1. Go to claude.ai, create account
2. Copy Company Comparison Deep Research Prompt
3. Set model to Sonnet or Opus, Web Search ON
4. Enter names of 3 stocks to compare
5. Claude generates full comparison report with scoring matrix, detailed analysis, quarterly financials, future outlook, technical trend analysis, valuation multiples
6. Stock with highest overall score = best pick
7. Repeat for all 5 industries → 5 best picks (one per industry)

### Step 4 — Valuation & Target Price Analysis

**Tool:** Claude.ai (Web Search ON)

Creates an equity research report with intrinsic value and target price — similar to JP Morgan analyst reports.

Uses SpringPad's Comprehensive Stock Analysis Prompt (14-page prompt).

**Steps:**
1. Go to claude.ai
2. Paste Comprehensive Stock Analysis Prompt
3. Enter stock name and author name
4. Ensure web search is on
5. Claude analyzes: business model, financial data (revenue, PAT, ROE, ROA, debt-to-equity, CAGR), cash flow, dividend history, shareholding pattern, peer comparison, qualitative outlook, management strategy
6. Outputs data-backed target price
7. If current market price < target price → right time to enter. If not → wait.

### Conclusion

By integrating these four AI-driven steps, you systematically build a five-stock growth portfolio with precision, data, and zero emotional bias.

---

## Track 2: AI-Powered Trading (Pratik Sir)

### Step 1 — Downloading Historical Data Without Coding

**Tools:** Claude.ai → Python → Google Colab

**Steps:**
1. Go to claude.ai
2. Copy Prompt 1 to Fetch Data, paste into Claude
3. Write the index/stock name + time horizon, hit enter
4. Copy the Python code Claude generates
5. Go to colab.research.google.com → New Notebook → Connect
6. Paste code → Run → Data downloaded as CSV/Excel

### Step 2 — Analyzing Historical Data with SpringPad ChatGPT

**Tool:** Market Analyst Pro by SpringPad (Custom ChatGPT)
https://chatgpt.com/g/g-SikxQaVjz-market-analyst-pro-by-springpad

**Steps:**
1. Open Market Analyst Pro by SpringPad
2. Copy Prompt 2 to Analyze Data
3. Paste into ChatGPT + upload Excel file
4. AI generates graphs, key market details, trends, volatility analysis, seasonality

### Step 3 — Identifying Market Trends with Seasonality Indicator

**Tool:** TradingView (Pine Script)

**Steps:**
1. Go to in.tradingview.com, create account
2. Copy SpringPad's Seasonality Indicator pine script code
3. Paste in Pine Editor → Add to Chart
4. Shows best/worst performing months for specific stocks

### Step 4 — Backtesting Trading Strategies

**Tool:** Claude.ai

**Steps:**
1. Go to claude.ai
2. Copy Prompt 3 to Backtest Data
3. Upload Excel file
4. Claude backtests strategy against historical data, shows P&L, trade list, equity curve, strategy stats

### Moving Average Crossover Strategy

- Pine Script code for TradingView
- Uses 9 & 21 period moving averages (configurable)
- Provides buy/sell signals on chart
- Options: SMA, EMA, WMA, VWMA

### BullsAi — Fully Automated Trading

- India's first AI-driven algo trading platform
- Operates under SpringPad Wealth Solutions Private Limited
- Registered with SEBI
- Ready-made pre-built strategies with thousands of active users
- Backtest any strategy before going live
- Paper trade with zero real money risk
- Deploy strategies with single click, integrated with brokerage
- AI No-Code Strategy Builder: describe rules in plain language → designs, backtests, deploys

---

## Advanced AI Dashboards (Built by Pratik Sir using Claude, no prior coding)

1. **Strategy Analytics Dashboard** — Year-wise P&L, trade logs, strategy strengths/weaknesses, improvement suggestions

2. **Options Strategy Selector** — Input market view, volatility expectation, time horizon, risk appetite → recommends best-fit options strategy with % match scores

3. **Mutual Fund Analyzer** — Monthly heat maps, portfolio manager performance, stock-level holdings

4. **War/Geopolitical News Tracker** — War timeline, historical Nifty behavior during past wars (Kargil, 9/11), sector outlooks, brokerage views, multiple Nifty scenario forecasts

5. **Personal Portfolio Tracker** — Short-term and long-term capital gains calculations year by year

---

## Key Links & Resources

### SpringPad GPTs:
- **Market Analyst Pro:** https://chatgpt.com/g/g-SikxQaVjz-market-analyst-pro-by-springpad
- **Trade Idea Generator:** https://chatgpt.com/g/g-67c31582ceb481919b81b38f63da10e8-trade-idea-generator-by-springpad
- **Industry Analysis & Stock Selector:** https://chatgpt.com/g/g-67d5fa2fc7088191be17bb6e680b4c04-springpads-industry-analysis-stock-selector-gpt

### TradingView Pine Script Codes:
- Seasonality Indicator
- Moving Average Crossover Strategy
- Steps to Install TradingView AI Chart Copilot

### Prompts:
- Growth Sector Deep Research Prompt
- Technical Analysis Prompt
- Company Comparison & Stock Selection Deep Research Prompt
- Comprehensive Stock Analysis Prompt
- News & Sentiment Analysis Prompt

---

## Takeaways from the Workshop

1. AI-Powered Mind-Blowing Strategies
2. AI in Stock Market with AI
3. Investing & Trading Bonuses
4. AI Building Advanced Dashboards

*"If one can master professional trading and automation using AI, it becomes possible to make consistent profits every month, invest money strategically to grow wealth exponentially, understand the financial secrets of the top 1%, know the right time to spend money, and ultimately achieve financial independence."*

— Rahul Sir and Pratik Sir, SpringPad
