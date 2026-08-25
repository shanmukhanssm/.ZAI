# SpringPad's Company Comparison Deep Research Prompt

**Tool to Use:** https://claude.ai/

**How to use:** Copy this entire prompt. Replace the stock names in the [INPUT] section. Paste into Claude. Make sure model is set to Sonnet or Opus and Web Search is toggled ON. You will receive a downloadable, self-contained interactive HTML dashboard.

---

## PROMPT

### SpringPad's Company Comparison Deep Research Prompt

#### [INPUT] -- Stocks to Compare
```
Stock 1: [COMPANY NAME 1]
Stock 2: [COMPANY NAME 2]
Stock 3: [COMPANY NAME 3]
```

(You may compare 2-4 stocks. If fewer than 3, collapse the extra company columns.)

#### [TASK] -- What to Produce
Conduct an institution-grade, multi-dimensional investment comparison of the stocks listed above, covering the Indian equity market (NSE/BSE). Research current data from the web, synthesise it across six analytical categories, score each company, and produce a single standalone interactive HTML file that can be opened directly in any browser without a build step.

Do not produce a markdown report. Do not produce a React JSX file. The final deliverable must be a .html file.

---

### [CONVENTIONS] -- Indian Fiscal Year & Data Freshness

#### Indian Fiscal Year Definition
This is non-negotiable. Indian companies report on an April-March fiscal year. The FY label refers to the year in which the fiscal year ends, not begins:

| FY Label | Period | Calendar Equivalent |
|----------|--------|---------------------|
| FY24 | 1 Apr 2023 - 31 Mar 2024 | ends March 2024 |
| FY25 | 1 Apr 2024 - 31 Mar 2025 | ends March 2025 |
| FY26 | 1 Apr 2025 - 31 Mar 2026 | ends March 2026 |
| FY27 | 1 Apr 2026 - 31 Mar 2027 | ends March 2026 |

**Rules to follow strictly:**
- Never write "FY24-25" and "FY25" to mean different things -- they are the same period
- Never write "FY25 (2025-26)" -- this is contradictory and wrong
- When a source writes "FY2024-25" or "2024-25", translate it internally as FY25 and use that label consistently
- Quarters: Q1 FY26 = April-June 2025. Q3 FY26 = October-December 2025. Q4 FY26 = January-March 2026

#### Data Freshness Rules
- Always identify the latest closed fiscal year (full-year audited results) and the latest available quarter
- Prefer quarterly results over annual where more recent
- When citing a metric, always note its period explicitly (e.g., "Revenue -- TTM as of Q3 FY26" or "ROE -- FY25 Annual")
- Do not mix periods across companies without flagging it clearly
- Cross reference screener.in, yahoo finance, and trading view for most recent price closes

---

### [ANALYTICAL FRAMEWORK] -- Research & Scoring

Research all three stocks thoroughly using web search before writing any content. Use at least 8-12 searches. Prioritise Screener.in, Trendlyne, StockAnalysis, BSE/NSE filings, PIB, company investor relations, and reputable financial news.

**Six Scoring Categories (1-5 each, max 30 total)**

#### Category 1 -- Fundamental Analysis (max 5 pts)
- Business model & competitive moat: What does the company do? What is its core competitive advantage? Is the moat durable?
- Market position: Market share, industry ranking, installed capacity or loan book size, geographic reach
- Corporate governance: Promoter quality, group brand, SEBI/rating agency signals, related-party risks
- Recent developments: Key announcements, expansions, partnerships in last 6-12 months
- Market sentiment: Analyst consensus, buy/sell/hold ratings, institutional ownership trends

Scoring: 5 = exceptional moat, best-in-class governance, strong catalysts. 1 = weak moat, governance concerns, no catalysts.

#### Category 2 -- Financial Analysis (max 5 pts)
Collect and present the following metrics (TTM / latest available). Create a colour-coded comparison table (green = best, amber = mid, red = weakest):

**Profitability:** Gross Margin (%), Operating Margin (%), Net Profit Margin (%)
**Returns:** Return on Equity -- ROE (%), Return on Assets -- ROA (%)
**Leverage:** Debt-to-Equity ratio, Interest Coverage Ratio
**Growth (5-year CAGR):** Revenue CAGR, EPS / PAT CAGR, Dividend Growth

Note: For NBFCs/financial companies, use NIM-equivalent and P/Loan Book as additional metrics.

**Quarterly Analysis Sub-Section** (required):
Research and present quarterly trend data for the most recent 6-8 quarters per company:
- Revenue (Rs Cr)
- EBITDA (Rs Cr) and EBITDA Margin (%)
- PAT / Net Profit (Rs Cr) and Net Margin (%)
- YoY change (%) and QoQ change (%)
- Label quarters using Indian convention: Q1 FY26 = Apr-Jun 2025, etc.
- Narrative interpretation per company (2-3 sentences): accelerating, decelerating, lumpy, recovering, or stable?

Scoring: 5 = top-quartile margins, strong ROE, healthy leverage, accelerating quarterly trajectory. 1 = deteriorating margins, weak returns, high leverage, decelerating quarterly trend.

#### Category 3 -- Price Performance (max 5 pts)
- Current stock price, 1-year return (%), 5-year return (%)
- 52-week High and Low, Market capitalisation
- Performance vs. Sensex/Nifty benchmark over 1Y
- Dividend yield
- Management Guidance vs. Actual table: guided, actual, verdict badge

Scoring: 5 = strong outperformance, guidance consistency, robust earnings track record.

#### Category 4 -- Forward Outlook (max 5 pts)
- Growth projections: Consensus revenue/PAT CAGR estimates (FY26-FY28 or 2-3 year forward)
- Capacity expansion / loan book targets
- Management's stated 2030 vision or CAPEX commitment
- Opportunities (green chips): Sector tailwinds, government policy support, product launches
- Risks (red chips): Execution risk, regulatory risk, leverage concerns, competition
- Macro & Regulatory backdrop: 6-8 data points relevant to the sector

Scoring: 5 = robust, de-risked 3-year growth path, strong policy tailwinds.

#### Category 5 -- Technical Analysis (max 5 pts)
Per company as of research date:
- Current price and signal (BULLISH / RECOVERING / BEARISH / NEUTRAL)
- RSI (14-day) and interpretation
- MACD -- signal type and direction
- 50-day SMA -- above or below?
- 200-day SMA -- above or below?
- Volume -- rising on up-days or down-days?
- Trend description -- channel, pattern, key support/resistance
- Technical Verdict (STRONG BUY / ACCUMULATE / HOLD / AVOID NEAR-TERM / SELL) with 2-3 sentence justification

Scoring: 5 = all MAs aligned bullishly, MACD buy signal, RSI neutral/rising.

#### Category 6 -- Valuation (max 5 pts)
- P/E ratio (TTM trailing, and forward estimate if available)
- P/B ratio
- EV/EBITDA (where applicable; note if not applicable for NBFCs)
- For NBFCs/lenders: P/Loan Book or P/AUM
- 3-4 sentence valuation commentary per company
- Identify best value per metric

Scoring: 5 = cheapest valuation with credible re-rating catalyst.

#### Final Score & Verdict
- Sum six category scores (max 30)
- Declare a winner
- 150-200 word verdict explaining why the winner is the best pick at current prices
- 4-bullet shortcomings section for each of the other companies

---

### [OUTPUT SPECIFICATION] -- Interactive HTML Dashboard

Produce a single, self-contained .html file. All libraries from CDN. Opens in Chrome/Firefox/Safari/Edge by double-clicking.

**Technology Stack:**
- Charts: Chart.js 4.4.0 from cdnjs.cloudflare.com
- Fonts: Google Fonts -- Cormorant Garamond (serif display), DM Mono (monospace data), Sora (sans body)
- Framework: Vanilla HTML + CSS + JavaScript only

**Design System:**
```
--bg:      #080D18   (deep navy)
--surface: #0F1729
--card:    #141E30
--border:  #1E3050
--text:    #E2E8F0   (primary)
--dim:     #94A3B8   (secondary)
--muted:   #4E5D73   (tertiary)
--gold:    #D4AF37   (winner accent)
--green:   #22C55E   (positive/best)
--amber:   #F59E0B   (neutral/mid)
--red:     #EF4444   (negative/worst)
```

Company colors: Co1=#3B82F6 (blue), Co2=#F97316 (orange), Co3=#10B981 (green), Co4=#A855F7 (purple)

**Layout Structure:**

1. **Header:** Dark gradient with gold glow, gold horizontal rule, report tag "Equity Research Report · [Sector Name]", title "Investment Comparison: [Co1] · [Co2] · [Co3]", metadata row

2. **Score Cards:** N-column grid, animated score counter, winner card with gold border and "Best Pick" badge

3. **Tab Navigation:** 8 tabs -- Overview | Fundamentals | Financials | Performance | Outlook | Technicals | Valuation | Verdict

   - **Tab 1 -- Overview:** Radar chart (6 categories, one polygon per company), horizontal bar chart (total scores), scoring table
   - **Tab 2 -- Fundamentals:** Company cards: Core Business, Recent Developments, Market Sentiment
   - **Tab 3 -- Financials:** Section A (Annual Metrics with bar chart + table, colour-coded), Section B (Quarterly Trends with chart, delta table, trend narrative cards)
   - **Tab 4 -- Performance:** Price cards, Management Guidance vs Actual table
   - **Tab 5 -- Outlook:** Projections table, Opportunities chips (green), Risks chips (red), Macro panel
   - **Tab 6 -- Technicals:** Technical indicator cards, RSI bar chart, Technical Verdict cards
   - **Tab 7 -- Valuation:** Metrics table with "Best Value" column, valuation commentary cards
   - **Tab 8 -- Verdict:** Gold gradient box, 150-200 word verdict, key factor cards, shortcomings section

4. **Footer:** DM Mono, 9px, disclaimer -- not investment advice, consult SEBI-registered advisor

**Interactive Behaviour:**
- Tab switching with chart destruction before re-rendering
- Score animation on page load (0 to final, easing, 1.2s)
- Fade-in animation on tab switch
- Cards lift on hover (translateY(-2px))
- Color-coded cells via rankStyles()
- Custom styled dark tooltip on charts

---

### [QUALITY STANDARDS]
- All data from real web searches -- no hallucinated numbers
- Every metric from named source (Screener.in, Trendlyne, company filing, etc.)
- FY labels strictly follow Indian convention (FY25 = Apr 2024-Mar 2025)
- Use latest available period for all financial data
- Quarterly data separate from annual, labeled with Q[n] FY[YY]
- Scoring rationale implied by content, not explicit
- Winner's verdict must be actionable
- HTML passes sanity check: all 8 tabs render, charts display, counters animate

### [DELIVERABLE]
Save final file as: `[Stock1]_vs_[Stock2]_vs_[Stock3]_Investment_Dashboard.html`
File size: 30-80 KB. Requires internet on first open for CDN fonts and Chart.js. All else self-contained.
