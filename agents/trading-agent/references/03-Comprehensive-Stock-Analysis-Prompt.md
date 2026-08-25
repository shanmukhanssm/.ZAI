# SpringPad's Comprehensive Stock Analysis Prompt

**Tool to Use:** https://claude.ai/

---

## Prompt

### SpringPad's Comprehensive Stock Analysis Prompt

#### Objective
Conduct a thorough analysis of the stock, combining qualitative and quantitative approaches to provide a well-rounded investment recommendation.

#### Source & Outline of Analysis
Take financial statements and other data points on the company from Screener.in on the said company. Adhere STRICTLY to the sample output outline. Can add charts, and visualisations.

---

### Instructions

**[Stock Name] - Equity Analysis Report**

By [Author Name]

---

### 1. Company Overview
- Provide a brief introduction to the company, including its name, sector, and primary business activities.
- Mention any recent significant events or changes in the company's structure or operations.

**Investment Recommendation** (Quick reference from Step 8):
- Recommendation: BUY/SELL/HOLD
- Target Price: Rs x (y% upside/downside)
- Investment Horizon: X months

---

### 2. Quantitative Analysis

Use the provided financial data to analyze the following metrics. For each subtopic, provide:
- The current value and historical data for the past 5 years (where available)
- A clear trend analysis (e.g., improving, declining, stable)
- Analytical commentary on the reasons behind the observed trends
- Key takeaways and their implications for the company's financial health and future prospects

#### a) Market Valuation and Price Metrics:
- Market Capitalization
- Current Stock Price
- Price-to-Earnings (P/E) Ratio

#### b) Profitability and Returns:
- Return on Equity (ROE)
- Return on Capital Employed (ROCE)
- Net Profit Margin
- Operating Profit Margin

#### c) Growth Metrics:
- Revenue Growth Rate (5-year CAGR)
- Earnings Per Share (EPS) Growth Rate (5-year CAGR)

#### d) Balance Sheet Strength:
- Debt-to-Equity Ratio

#### e) Cash Flow Analysis:
- Cash Flow from Operations

#### f) Dividend Analysis:
- Dividend Yield
- Dividend Payout Ratio

#### g) Efficiency Ratios:
- Asset Turnover Ratio

#### h) Valuation Metrics:
- Compare P/E ratio with industry peers

For each metric, ensure that you:
- Highlight any significant year-over-year changes
- Discuss how the company's performance compares to industry benchmarks
- Identify any potential red flags or areas of concern
- Explain the implications of these metrics for potential investors

---

### 3. Qualitative Analysis

#### a) Business Model:
- Core products/services
- Revenue streams
- Competitive advantages

#### b) Management Quality:
- Experience and track record of key executives
- Corporate governance practices

#### c) Growth Strategy:
- Expansion plans
- Research and development initiatives

---

### 4. Shareholding Pattern Analysis

Analyze the company's shareholding pattern, focusing on:
- Promoter holding and any recent changes
- Institutional investor (FII and DII) holdings
- Public shareholding trends

---

### 5. Investment Thesis

Synthesize the qualitative and quantitative analyses to form a coherent investment thesis:
- Key drivers for future growth
- Potential catalysts for stock price movement
- How the company is positioned to handle industry trends and challenges

---

### 6. Valuation and Recommendation
- Provide a fair value estimate for the stock based on various valuation methods
- Offer a clear investment recommendation (Strong Buy, Buy, Hold, Sell, Strong Sell) with a detailed rationale
- Include a target price and the expected timeframe for achieving it

---

### 7. Conclusion
Summarize the key points of your analysis and restate your recommendation.

---

### Output Type

Produce a single standalone interactive HTML file that can be opened directly in any browser without a build step. Do not produce a markdown report. Do not produce a React JSX file. Design as a professional interactive report, with:

**Professional Design Elements:**
- Clean, corporate color scheme with professional typography
- Branded header with company and report information
- Recommendation box highlighting the BUY recommendation
- Color-coded trends (positive in green, negative in red, neutral in orange)
- Proper spacing and margins for readability
- Each segment should be a separate tab in the UI and not one single scrolling read

**Well-Structured Content:**
- All seven sections from the original report maintained
- Data presented in neatly formatted tables
- Clear hierarchical headings and subheadings
- Highlighted key metrics and recommendations
- Page breaks at logical points for PDF printing

**Enhanced Readability:**
- Key points highlighted in bold
- Important figures and recommendations emphasized
- Consistent formatting throughout
- Footer with disclaimer and publication information

---

### Important Notes

- For Indian markets, the financial year starts from April 1st and ends on March 31st. FY26 = April 1, 2025 to March 31, 2026.
- For all Balance Sheet, Income Statement, and Cash flow statement data, refer to the latest available annual period. For market metrics, refer to the latest available data from credible sources.
- For P/E Ratio comparison with peers, provide qualitative analysis rather than specific figures.
- Provide detailed financial metrics, market share figures, and growth rates to substantiate each point.
- No need to mention the report generation date.
- Focus on unique trends, challenges, and innovations shaping the specific industry.
- Ensure analysis leads to practical insights for decision-making.
- Maintain an objective tone throughout.
- Use bold formatting for headings and subheadings. Highlight important figures and final recommendation.
- If certain data points are not available, provide a qualitative assessment.
- Keep the lookback period as the last 5 fiscal years.
- In Quantitative Analysis, each subtopic must include clear trend analysis, commentary, and key takeaways.
- Refer to the reference Output below for structure, framework, style, and chronology.
- Cross reference screener.in, yahoo finance, and trading view for most recent price closes.

---

### Reference Output (Example: Reliance Industries Ltd)

**Reliance Industries Ltd - Equity Analysis Report**
By Rahul Chandra

#### 1. Company Overview
Reliance Industries Ltd (RIL) is India's largest private sector company and a global conglomerate headquartered in Mumbai. RIL operates across multiple sectors, including Oil-to-Chemicals (O2C) (~57% of revenues), Digital Services (Jio), Retail, and Oil & Gas Exploration.

Investment Recommendation: BUY | Target Price: Rs 1,850 (48% upside) | Horizon: 18-24 months

#### 2. Quantitative Analysis

**a) Market Valuation and Price Metrics:**
- Market Cap: Rs 16,88,704 Cr | Current Price: Rs 1,248 | P/E: 24.41 (above industry median of 20.55)

**b) Profitability and Returns:**
| Metric | FY24 | FY23 | FY22 | FY21 | FY20 | Trend |
|--------|------|------|------|------|------|-------|
| ROE | 9.25% | 9% | 8% | 8% | 11% | Slight improvement |
| ROCE | 9.61% | 9% | 8% | 8% | 11% | Slight improvement |
| Net Profit Margin | 8.97% | 8.46% | 9.77% | 11.53% | 6.68% | Fluctuating |
| Operating Profit Margin | 18% | 16% | 16% | 17% | 15% | Stable with improvement |

**c) Growth Metrics:**
- Revenue 5Y CAGR: 10% | 3Y CAGR: 24% (accelerating)
- EPS Growth 5Y CAGR: 12%
- PEG ratio: 2.04 (somewhat expensive relative to growth)

**d) Balance Sheet Strength:**
- Debt-to-Equity: 0.44 in FY24 (improved from 0.65 in FY20)

**e) Cash Flow Analysis:**
- CFO: Rs 110,654 Cr (FY22) -- strong but volatile

**f) Dividend Analysis:**
- Dividend Yield: ~0.40% (stable but low) | Payout Ratio: ~9%

**g) Efficiency Ratios:**
- Exceptional working capital management, negative cash conversion cycle

**h) Valuation vs Peers:**
| Company | P/E | ROCE | D/E |
|---------|-----|------|-----|
| RIL | 24.41 | 9.61% | 0.44 |
| IOCL | 18.28 | 21.14% | 0.90 |
| BPCL | 8.19 | 32.09% | 0.76 |
| HPCL | 11.42 | 21.26% | 1.58 |
| Industry Median | 20.55 | 21.45% | 0.78 |

#### 3. Qualitative Analysis
- Business Model: Integrated O2C, Digital (Jio), Retail, Oil & Gas
- Management: Mukesh Ambani leadership, demonstrated strategic foresight
- Growth Strategy: Green energy investment (Rs 75,000 Cr), retail expansion, digital ecosystem monetization, SpaceX Starlink partnership

#### 4. Shareholding Pattern
| Category | Jun 2024 | Trend |
|----------|----------|-------|
| Promoters | 50.33% | Stable |
| FII | 21.75% | Gradual decrease |
| DII | 17.30% | Increasing |
| Public | 10.43% | Stable |

#### 5. Investment Thesis
Key drivers: Digital services expansion, retail penetration, new energy transition, omnichannel convergence. Catalysts: Jio/Retail IPOs, green energy traction, O2C margin recovery, strategic partnerships.

#### 6. Valuation and Recommendation
Fair value (SOTP): O2C = Rs 820/sh, Jio = Rs 540/sh, Retail = Rs 420/sh, New Energy = Rs 70/sh = Rs 1,850 total. BUY with 48% upside, 18-24 month horizon.

#### 7. Conclusion
Compelling investment at current valuations. Transformation from petrochemical business to diversified conglomerate. ROE gradually improving. Strong promoter confidence with 50%+ holding.
