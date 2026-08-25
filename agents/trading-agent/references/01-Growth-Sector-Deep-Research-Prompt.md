# SpringPad's Growth Sector Deep Research Prompt

**AI Tool to Use:** https://www.perplexity.ai/

**HOW TO USE THIS PROMPT:**
Paste the full prompt below into Perplexity Deep Research. The prompt is self-contained — it instructs the AI to:
- Scan the full NSE/BSE sector universe (25–35 sectors)
- Score every sector on 6 dimensions using live data
- Select the top sectors objectively
- Build a full interactive HTML dashboard with all sourced data

Fill in `[CONFIGURABLE PARAMETERS]` before running if required.

---

## START COPYING FROM HERE

---

## SpringPad's Growth Sector Deep Research

### ROLE & FRAMING

You are a senior macro and sector research analyst at a top-tier Indian investment firm. You are producing a decision-ready, interactive investment briefing — not an essay. Every claim must be backed by a live data source fetched today. Today's date is [EXECUTION DATE — INSERT CURRENT DATE BEFORE RUNNING]. All data must be sourced as of this date.

Primary audience: Dual — a retail investor seeing markets for the first time AND a seasoned market veteran. Both must find value. The output must have lucidity and be striking through design, logical clarity, and actionable precision.

Output format: A single, self-contained, production-quality HTML file. No placeholders. No lorem ipsum. All data live and sourced.

### CONFIGURABLE PARAMETERS

```
GEOGRAPHY:           India (NSE/BSE listed equities only)
NUMBER OF SECTORS:   5 (selected by scoring — not pre-decided)
HORIZONS:            1-Year · 3-Year · 5-Year
BENCHMARK INDEX:     Nifty 50
MACRO FOCUS:         India domestic + global macro as relevant
ANALYSIS DATE:       [INSERT TODAY'S DATE — e.g., "17 May 2026"]
DISCLAIMER:          "For educational purposes only. Not investment advice."
BRANDING:            [SpringPad]
```

---

## STEP 1 — PRE-RESEARCH (Execute Before Writing Any Code)

Before writing a single line of HTML, complete ALL research tasks below. Every number in the final output must trace back to one of these steps. Do not use memory, prior training data, or estimates — fetch live.

### 1A. Fetch Live Macro Indicators (as of [EXECUTION DATE])

Search and record the LATEST available values for ALL of the following:

| Indicator | Source to Search |
|-----------|-----------------|
| India Real GDP growth rate (latest quarter + current FY forecast) | Trading Economics / IBEF / MoSPI |
| India CPI Inflation (latest available month) | RBI.org.in / Trading Economics / MOSPI |
| RBI Repo Rate (current) | RBI.org.in / Trading Economics |
| India Fiscal Deficit (% of GDP, current FY) | Union Budget documents / IBEF |
| INR/USD exchange rate (current) | Trading Economics / XE.com |
| Bank Credit Growth YoY % (latest RBI data) | RBI.org.in / IBEF |
| Nifty 50 P/E ratio (as of execution date) | IndexPE.in / Quantace.in / NSE India |
| Nifty 50 historical median P/E (5Y and 7Y) | IndexPE.in / Craytheon PE chart |
| Government Capex budget (current FY, Rs Crore) | Union Budget / IBEF |

### 1B. Sector Universe Scan — Discover, Then Shortlist

Do NOT start with a pre-defined sector list. Run a systematic screen across the full investable universe. The top sectors must emerge from data, not assumptions.

#### Stage 1 — Define the Full Universe

Begin with all NSE/BSE sector and thematic indices as the starting universe. Search the NSE India sectoral indices page and BSE sector indices page to confirm the current live list, then supplement with emerging sectors. The typical universe covers 25-35 identifiable sectors:

**NSE Sectoral Indices** (search NSE India for current list):
Nifty Auto · Nifty Bank · Nifty Financial Services · Nifty FMCG · Nifty IT · Nifty Media · Nifty Metal · Nifty Pharma · Nifty PSU Bank · Nifty Private Bank · Nifty Realty · Nifty Healthcare · Nifty Consumer Durables · Nifty Oil & Gas · Nifty Capital Markets

**NSE Thematic Indices** (search NSE India thematic indices):
Nifty India Defence · Nifty India Digital · Nifty India Manufacturing · Nifty Mobility · Nifty India Consumption · Nifty Commodities · Nifty Infrastructure · Nifty Energy · Nifty EV & New Age Automotive · Nifty India Renewable Energy · Nifty India Railways · Nifty India Tourism

**BSE Sectoral Indices** (cross-check for gaps):
BSE Telecom · BSE Utilities · BSE Industrials · BSE Consumer Discretionary · BSE Healthcare · BSE Teck

**Emerging sectors not covered by indices** (evaluate independently):
Specialty Chemicals · Agrochemicals · Semiconductor & Electronics Manufacturing · Quick Commerce / New Retail · Logistics & Warehousing · Water & Waste Management · Data Centers & AI Infrastructure · Exports / PLI Beneficiaries (cross-sector)

Action: Compile the complete list of all sectors found. Aim for 28-35. Record the list in the HTML comment block (Step 2).

#### Stage 2 — Score Every Sector on 6 Dimensions

For EACH sector in the full universe, fetch and score across all 6 dimensions. All scores are 1-5:

**Dimension 1 — Macro Alignment (Weight: 25%)**
Does the current macro environment (GDP trend, rate cycle, INR direction, credit growth, government capex) directly and materially benefit this sector?
- 5 = Multiple macro tailwinds directly flowing into sector
- 4 = One strong direct macro tailwind
- 3 = Indirect or partial tailwind
- 2 = Macro neutral — neither helps nor hurts
- 1 = Macro headwind (e.g., rate-sensitive sector in rising rate environment)

**Dimension 2 — Policy Support (Weight: 20%)**
Is there an active, funded government policy specifically supporting this sector in the current or most recent Union Budget?
- 5 = Multiple active policies (PLI + FDI liberalisation + tax incentive + procurement mandate)
- 4 = Two active, funded policies
- 3 = One active policy or legacy scheme
- 2 = General support, no sector-specific policy
- 1 = Regulatory headwind or active policy risk (e.g., price controls, import restrictions)

**Dimension 3 — Market CAGR 5Y (Weight: 20%)**
Projected sector market size CAGR over 5 years from analyst reports, IBEF, government targets, or Mordor Intelligence. Fetch the actual CAGR; do not estimate:
- 5 = CAGR > 22%
- 4 = CAGR 18-22%
- 3 = CAGR 14-18%
- 2 = CAGR 10-14%
- 1 = CAGR < 10%

**Dimension 4 — Relative Valuation (Weight: 15%)**
Sector P/E or index P/E vs Nifty 50 current P/E (fetched in Step 1A). Cheaper relative to benchmark scores higher:
- 5 = Sector P/E at discount to Nifty 50 (e.g., Banking at 10x vs Nifty 50 at 21x)
- 4 = 0-25% premium to Nifty 50
- 3 = 25-75% premium
- 2 = 75-150% premium
- 1 = >150% premium (extremely stretched valuation)

**Dimension 5 — Earnings Momentum (Weight: 10%)**
YoY earnings growth trend for leading companies in the sector (check Screener.in for latest quarterly results of 3-5 top stocks per sector):
- 5 = Earnings growth >25% YoY, accelerating
- 4 = Earnings growth 15-25% YoY
- 3 = Earnings growth 5-15% YoY, stable
- 2 = Earnings growth 0-5% or decelerating
- 1 = Earnings decline YoY

**Dimension 6 — 1Y Price Momentum (Weight: 10%)**
1-year index/sector return (fetch from NSE index performance page or 5paisa/Groww sector trackers):
- 5 = 1Y return > 25%
- 4 = 1Y return 15-25%
- 3 = 1Y return 5-15%
- 2 = 1Y return 0-5%
- 1 = 1Y return negative

**Weighted Score Formula:**
```
Total = (Macro x 0.25) + (Policy x 0.20) + (CAGR x 0.20) + (Valuation x 0.15) + (Earnings x 0.10) + (Momentum x 0.10)
```

#### Stage 3 — Rank All Sectors and Select the Top 10

Sort all 28-35 sectors by Total Score descending. Check for overlap: if two adjacent ranked sectors have >70% constituent overlap (e.g., "Capital Goods" and "Infrastructure"), merge them into one combined sector and elevate the next ranked sector. Select the top 10 non-overlapping sectors by weighted score.

### 1C. For Each of the Selected Sectors — Fetch Detailed Data

For every sector that makes the top 10, gather the following before building the HTML:

**A. Listed Domestic Key Players**
CRITICAL RULE: Every company listed as a "Key Player" MUST be currently listed on NSE or BSE. No foreign companies. No unlisted startups.

For each sector, identify 5-7 listed companies with:
- NSE/BSE ticker symbol (verify it is currently active)
- Approximate current market cap
- Current trailing P/E ratio (from Screener.in or Moneycontrol)
- One-line description of why this company is relevant to the sector theme

Sources: Screener.in · Moneycontrol · INDmoney · ETMoney · Zerodha Sectors · Dhan sector pages

**B. Market Size Data**
- Current market size (state in Rs or $, cite source and publication date)
- Projected size at 3Y horizon (from analyst/IBEF/government report — cite specifically)
- Projected size at 5Y horizon (same)
- Calculated or cited CAGR for each horizon

**C. 1-Year Price Momentum**
Fetch the 1Y return for the sector's NSE index (or proxy basket if no dedicated index). Source: NSE India · Groww · 5paisa · Moneycontrol sector tracker.

**D. Macro-to-Sector Causal Chain**
Write precisely: which macro indicator -> what sector mechanism -> what earnings/revenue effect. One causal sentence per macro driver that applies.

### 1D. Compile All Sources

Maintain a numbered list (S1-S25+) of every source used across all research steps:
- Source number (S1, S2, ...)
- Full article/page title
- Complete URL
- Specific data point sourced from it (one line)

Minimum 20 sources. Every data point in the dashboard must have a corresponding source in this list.

---

## STEP 2 — SECTOR SELECTION TRANSPARENCY BLOCK

Before proceeding to Step 3, embed the following as an HTML comment at the very top of the file (inside `<head>`, after `<!DOCTYPE html>`). This makes the analysis fully auditable:

```xml
<!--
+----------------------------------------------------------+
|  SECTOR SELECTION WORKING -- [EXECUTION DATE]              |
+----------------------------------------------------------+

FULL UNIVERSE SCREENED (list all sectors evaluated):
 Sector Name · Sector Name · ... (28-35 total)

SCORING MATRIX (sorted by Total Score descending):
Rank | Sector              | Macro | Policy | CAGR | Val. | Earn. | Mom. | TOTAL
1    | [Sector Name]       |  4.5  |  5.0   | 4.0  |  3.5 |  4.0  | 4.5  | 4.22
2    | [Sector Name]       |  ...
...
35   | [Sector Name]       |  1.5  |  1.0   | 1.5  |  2.0 |  2.0  | 1.5  | 1.57

TOP 10 SELECTED (and why):
1.  [Sector] -- Score X.XX -- [One sentence on why it ranked here]
2.  ...
10. ...

MERGED SECTORS (if any):
- [Sector A] merged with [Sector B]: reason + combined into [Final Name]

EXCLUDED (rank 11+) -- notable exclusions with reasoning:
- [Sector]: Score X.XX -- [One sentence]
... (list all excluded sectors)

SECTOR COLOR ASSIGNMENTS (sector -> hex colour, used consistently throughout):
1. [Sector] -> #e86030
2. [Sector] -> #3a7a1e
3. [Sector] -> #c88c00
4. [Sector] -> #1a5fa0
5. [Sector] -> #01696f
6. [Sector] -> #7a39bb
7. [Sector] -> #d19900
8. [Sector] -> #006494
9. [Sector] -> #437a22
10.[Sector] -> #a12c7b
-->
```

---

## STEP 3 — BUILD THE INTERACTIVE HTML DASHBOARD

Build a single HTML file replicating this architecture exactly. The 10 sectors populated throughout are those selected in Step 2 -- not any pre-defined list.

### DESIGN SYSTEM (Non-negotiable)

**Typography:**
- Display font: Syne (Google Fonts) -- headings, numbers, sector names
- Body font: Inter (Google Fonts) -- body text, labels, tables
- Scale: fluid clamp() -- never hardcode px font sizes

**Color System -- both light AND dark mode are mandatory:**
- Default: dark mode (data-theme="dark" on `<html>`)
- Toggle: light/dark button in top-right nav
- Accent: teal (#01696f light / #4f98a3 dark)
- Surfaces: warm near-black (#0f0e0d bg / #181716 surface / #211f1e surface-2)
- Text: warm off-white (#e8e6e2 primary / #8a8880 muted / #504e4c faint)

**Sector Colors -- assign one unique color per sector in ranked order:**
#e86030 · #3a7a1e · #c88c00 · #1a5fa0 · #01696f · #7a39bb · #d19900 · #006494 · #437a22 · #a12c7b
(Same color used for that sector in every chart, table, card, and badge)

- Border radius: 8-14px (cards), 20px (pills/chips), 6px (table badges)
- Card shadow: 0 2px 16px rgba(0,0,0,0.4), 0 1px 4px rgba(0,0,0,0.3) [dark]
- Transitions: 180ms cubic-bezier(0.16,1,0.3,1)

### COMPONENT SPECIFICATIONS

#### NAV BAR (sticky, height 56px)
- Left: SVG pulse/waveform logo + "India Growth Sectors" (Syne, 800 weight)
- Centre: anchor links -> Macro · Sectors · Rotation · Policy · Signals
- Right: light/dark toggle button (sun/moon icon + label) + "References" button (primary colour background)

#### HERO SECTION
- Eyebrow: "Macro-to-Sector Research · [EXECUTION DATE]" (primary colour, 0.72rem uppercase)
- H1: "India's Top 10 Growth Sectors / For the Next 5 Years" (Syne 800, 3-3.5rem clamp)
- "10 Growth Sectors" in primary colour
- Meta row (0.8rem, muted colour, separated by 4px dots):
  - Execution date
  - "Nifty 50 PE: [LIVE VALUE] · [Valuation Label: Fairly Valued / Overvalued / Undervalued]"
  - "India GDP FY[XX]E: [LIVE VALUE]%"
- Disclaimer badge: amber background, warning icon, "Not Investment Advice -- Educational Only"

#### MACRO KPI STRIP (immediately below hero, full-width)
6-card grid (auto-fit, min 140px). Cards: Real GDP · CPI Inflation · RBI Repo Rate · Credit Growth · Govt Capex · Nifty 50 P/E

Each card structure:
```
[LABEL -- 0.68rem uppercase muted]
[VALUE -- Syne 1.4rem bold, coloured: green=positive, red=risk, neutral=muted]
[SUB -- 0.7rem: trend arrow + context phrase]
```

Arrow colours: up green · down red (unless declining inflation/rate = good, then green) · right muted

#### SECTION: "Why Now?" -- Macro Linkage Cards (id="macro")
6 cards, 3-column grid. One card per major macro driver identified in Step 1A. Each card:
```
[Coloured top border, 3px]
[DRIVER LABEL]
[READING - large value] [TREND BADGE]
"Flows into ->"
[SECTOR CHIPS - small pill badges showing beneficiary sectors from top 10]
[WHY - 2 sentences: macro mechanism + earnings/revenue effect]
[Sources: [Source names]] -- clickable
```

#### MACRO SCORECARD TABLE
7 rows x 5 columns. Header: Indicator | Current Reading | Trend | YoY Change | Investment Signal

Signal pills: BULLISH (green) · NEUTRAL (teal) · WATCH (amber) · CAUTIOUS (red)

#### 10 SECTOR CARDS (id="sectors")
Grid: auto-fill, minmax(320px, 1fr). The 10 sectors are those selected by the scoring matrix.

Card structure:
```
CARD HEADER:
  [NN · Sector Name]              [conviction dots]

CARD BODY (stats row, 3 columns):
  [Current Market Size]   [CAGR 5Y]   [P/E Range]

HORIZON BADGES:
  [1Y: Strong/Moderate/Building]  [3Y: ...]  [5Y: ...]

CARD FOOTER:
  [NSE index]    [Anchor stock P/E]

On click -> Deep Dive Panel expands inline:
  LEFT COLUMN: Macro Thesis, Listed Key Players (NSE/BSE ONLY)
  RIGHT COLUMN: 1Y/3Y/5Y Catalysts, Key Risks, Export/Global Angle
```

---

## STEP 4 — JAVASCRIPT BEHAVIOUR

- **Theme Toggle:** Dark mode default, toggle light/dark, rebuild charts on toggle
- **Sector Card Deep Dive:** Click to expand, only one open at a time
- **Chart Tabs:** Three tabs (Market Size Growth, CAGR by Horizon, P/E vs Momentum Bubble) using Chart.js 4.x from CDN
- **Sector Toggle Chips:** Show/hide sectors in charts, minimum 2 active
- **References Modal:** Triggered by nav button or source links

---

## STEP 5 — DATA FRESHNESS RULES

- All macro figures sourced from publication dated within 30 days of execution date
- All sector P/E ratios must be current trailing P/E from Screener.in, NSE India, or Moneycontrol
- All market cap figures must be current (within 7 days)
- Sector CAGR estimates must cite specific report title, publication date, and source
- No synthetic data. If data unavailable, write "Data not available -- [source attempted]"
- All key players must be currently listed on NSE/BSE
- Each of 6 dimension scores must be derived from a fetched data point -- not intuition

---

## STEP 6 — QUALITY CHECKLIST

- All 9 macro indicators populated with live, sourced values
- Nifty 50 P/E is actual current trailing value
- All 10 sectors selected through scoring matrix
- Full scoring matrix (all 28-35 sectors) in HTML comment block
- All excluded sectors have one-line reason
- Every company has NSE/BSE ticker, no foreign companies
- Charts use real fetched data, not estimates
- Dark mode default, light/dark toggle works
- Only one deep-dive panel open at a time
- References modal with 20+ sources
- Single self-contained HTML file, all CSS/JS inline or CDN

---

## STEP 7 — OUTPUT INSTRUCTION

Deliver ONE file named: `india-growth-sectors-[YYYYMMDD].html`

The file must be:
- Fully self-contained (all CSS and JS inline, or from CDN)
- Openable in any modern browser without a server
- Between 80KB and 150KB
- HTML comment block with sector selection working at very top

---

## END OF PROMPT

---

## CUSTOMISATION GUIDE

| What to change | Location | How |
|---------------|----------|-----|
| Country / Exchange | CONFIGURABLE PARAMETERS + Step 1B universe | Replace "India (NSE/BSE)" with target market |
| Number of top sectors | CONFIGURABLE PARAMETERS | Change to desired number |
| Benchmark index | CONFIGURABLE PARAMETERS | Replace "Nifty 50" |
| Analysis horizons | CONFIGURABLE PARAMETERS | Change to desired horizons |
| Scoring weights | Step 1B, Stage 2 formula | Adjust 6 dimension weights to total 100% |
| Branding / firm name | CONFIGURABLE PARAMETERS + footer | Add firm name |
| Colour scheme | Step 3, Design System | Replace sector hex codes |
