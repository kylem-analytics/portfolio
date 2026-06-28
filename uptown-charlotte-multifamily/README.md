# Uptown Charlotte Multifamily Investment Analysis

A discounted cash flow underwriting analysis of Museum Tower Apartments, a Class A high-rise multifamily asset in Uptown Charlotte, built to assess whether the property's current asking price is supported by its projected cash flows.

**Completed as part of a Real Estate Finance course at Elon University, in collaboration with Noah Rubin and Mitch Ashberg.**

---

## Overview

This project evaluates the investment potential of **Museum Tower Apartments** (525 S Church Street, Charlotte, NC) — a five-star, 43-story high-rise built atop the Mint Museum in the Third Ward submarket of Uptown Charlotte. The analysis combines CoStar market and property data, comparable leasing and sales transactions, demographic research, and a three-scenario discounted cash flow model to determine whether the asset's asking price is justified by its underlying fundamentals.

**Investment question:** Does Museum Tower's projected cash flow support its current $190.0M asking price at a reasonable target return, or is the asset overvalued relative to fundamentals?

## Key Findings

- **The deal does not pencil at the current asking price.** Under base case assumptions, the unleveraged IRR is **4.78%** against an 8% target return, and the DCF-implied value of **$165.8M** sits well below the $190.0M asking price.
- **Even the best case falls short.** Assuming stronger rent growth, tighter vacancy, and no cap rate expansion over the hold period, the best case IRR reaches only **7.69%** — still short of the 8% hurdle.
- **The return barely clears the risk-free rate.** The 10-year U.S. Treasury yield is currently approximately 4.4%, meaning the base case IRR offers only a ~40 basis point premium over a risk-free asset for an illiquid, single-property investment — a thin premium for the risk involved.
- **This is a pricing problem, not a fundamentals problem.** Museum Tower is genuinely the newest, highest-rent, and most differentiated asset in its competitive set (commanding $2,619/unit versus a $2,244 weighted-average comp set), benefiting from a unique integration with the Mint Museum and strong Uptown submarket fundamentals. The issue is valuation, not asset quality.
- **Uptown outperforms the broader Charlotte market.** Uptown vacancy (8.0%) runs well below the citywide rate (12.8%), supported by a constrained new-supply pipeline (only 87 units delivered since 2021) even as the broader Charlotte market absorbs a historic construction wave.

## Methodology

**1. Market & submarket research** (CoStar) — analyzed Uptown Charlotte's supply/demand fundamentals, demographics, and broader Charlotte multifamily trends, including a citywide construction and absorption review.

**2. Comparable property analysis** — benchmarked Museum Tower against four leasing comparables and four recent sales transactions in the Uptown submarket to validate rent and pricing assumptions.

**3. Three-scenario DCF model** (Excel) — built a base/worst/best case pro forma projecting rent growth, vacancy, operating expenses, and a terminal sale, then solved for unleveraged IRR and present value under each scenario.

| | Base Case | Worst Case | Best Case |
|---|---|---|---|
| **Purchase Price** | $190.0M | $187.3M | $197.4M |
| **Going-in / Going-out Cap Rate** | 5.35% / 5.85% | 5.35% / 6.35% | 5.35% / 5.35% |
| **IRR** | 4.78% | 2.97% | 7.69% |
| **DCF Value** | $165.8M | $151.3M | $194.8M |

## Tools Used

- **Excel** — three-scenario DCF model with formula-driven assumptions, IRR/NPV calculations, and a fully cross-checked operating expense schedule
- **CoStar** — property data, comparable transactions, submarket and market-level demographic and supply/demand statistics

## Repository Structure

```
uptown-charlotte-multifamily/
├── README.md
├── uptown_charlotte_investment_analysis.pdf   # Full written report with market analysis, comps, and recommendation
└── uptown_charlotte_investment_analysis.xlsx  # Three-scenario DCF model (Pro Forma / Worst Case / Best Case)
```

## Contact

**Kyle Murphy**
LinkedIn: [linkedin.com/in/kmurphy61](http://www.linkedin.com/in/kmurphy61)
Email: KyleMurphy02@icloud.com
