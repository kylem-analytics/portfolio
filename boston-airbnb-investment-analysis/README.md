# Boston Airbnb Investment Analysis

A Python and Tableau-based analysis identifying what drives Airbnb revenue performance in Boston, built to support data-driven investment decisions for short-term rental properties.

**Completed as part of MSBA coursework at Elon University.**

---

## Overview

This project investigates which Boston neighborhoods, property attributes, and host strategies are associated with stronger Airbnb investment performance. It combines listing-level data from [Inside Airbnb](http://insideairbnb.com/get-the-data/) with statistical modeling and Tableau visualization to translate raw listing data into investment guidance.

**Motivation:** I'm interested in strategically investing in and managing short-term rental properties for passive income after graduation. This project was designed to answer the questions I'd actually want answered before putting money into a market: where to buy, what features are worth paying for, and how competition changes the calculus.

## Business Questions

1. Which Boston neighborhoods offer the highest Airbnb revenue potential (price × occupancy), and what listing characteristics drive that performance?
2. What host and property features (amenities, ratings, experience) meaningfully increase profitability and demand?
3. Are entire homes, private rooms, or studio apartments the most profitable Airbnb investment type in Boston?

## Theoretical Framing

Two theories guided the analysis:

- **Signaling Theory** — Airbnb guests can't physically inspect a property before booking, so they rely on signals (amenities, ratings, photos, host experience) to judge quality and trustworthiness. Stronger signals reduce booking uncertainty and should command higher prices and occupancy.
- **Resource-Based View** — hosts gain a competitive advantage when they control resources that are valuable, rare, and hard to imitate. This motivated looking at *which* resources (amenities, quality scores, superhost status) actually translate into a measurable edge, versus which are commoditized.

Working hypotheses going in:

- The relationship between amenities and occupancy is likely **non-linear** — amenities help up to a point, then show diminishing returns.
- Quality signals likely matter **more** in high-demand, centrally located neighborhoods than in less competitive ones.
- Host experience may interact with neighborhood competition rather than having a uniform effect.

## Data

- **Source:** [Inside Airbnb](http://insideairbnb.com/get-the-data/) — Boston listings snapshot
- **Scope:** ~2,800 active listings after cleaning
- **Key engineered features:**
  - `est_monthly_revenue` — trailing 12-month estimated revenue ÷ 12
  - `amenities_count` — parsed from the listing's amenities field
  - `host_years` — host tenure, derived from `host_since`
  - `neighbourhood_listing_count` / `competition_level` — listings per neighborhood, bucketed into Low / Medium / High competition tiers
  - `quality_index` — standardized composite of amenities count and review rating

The full cleaning and feature engineering pipeline is in [`notebooks/boston_airbnb_analysis.ipynb`](notebooks/boston_airbnb_analysis.ipynb).

## Methodology

**1. Data cleaning & feature engineering** (Python / pandas) — parsed price and amenities fields, derived host tenure, built neighborhood-level competition tiers, and constructed a composite quality index.

**2. Exploratory visualization** (Tableau) — eight visualizations covering revenue by location, revenue by neighborhood, amenities vs. reviews, host experience vs. revenue, revenue by competition level, revenue by quality index, amenities distribution, and superhost status vs. revenue. See [`tableau/boston_airbnb_dashboard.twbx`](tableau/boston_airbnb_dashboard.twbx).

**3. Statistical modeling** (OLS regression, `statsmodels`) — three nested models predicting estimated monthly revenue:

| | Model 1 | Model 2 | Model 3 |
|---|---|---|---|
| **Includes** | Controls only | + amenities, occupancy, competition | + interaction effects |
| **Adjusted R²** | 0.549 | 0.618 | 0.618 |
| **N** | 2,778 | 2,778 | 2,778 |

Controls: accommodates, beds, nightly price, review rating, host years, number of reviews.
Main variables: amenities count, estimated occupancy, neighborhood listing count.
Interactions: amenities × competition, amenities × occupancy, occupancy × competition.

## Key Findings

- **Demand beats features.** Estimated occupancy is, by a wide margin, the strongest and most consistent predictor of monthly revenue. Listings with higher booking frequency outperform regardless of amenities or reputation.
- **Amenities alone don't move revenue — but they interact with competition.** Amenities count is not independently significant once demand and competition are controlled. However, the interaction between amenities and neighborhood listing count is negative and significant (p < 0.05): in highly competitive neighborhoods, additional amenity investment shows diminishing — even negative — returns.
- **Reputation matters less once you control for actual bookings.** Review count and rating lose significance once occupancy is in the model, suggesting that realized demand captures more performance information than reputation signals alone.
- **Host tenure is negatively associated with revenue.** A counterintuitive result, plausibly explained by newer hosts pricing and optimizing more aggressively, or by long-tenured hosts disproportionately managing lower-value properties.
- **Revenue is geographically concentrated.** Back Bay, Beacon Hill, and the North End post the highest revenue, and denser neighborhoods generally outperform — location is a first-order driver of performance.
- **Superhost status is associated with higher average revenue**, consistent with the signaling framework: status acts as a trust signal that guests reward.
- **There's a "sweet spot" for amenities** — most Boston listings cluster around 25–30 amenities, and the relationship between amenity count and reviews flattens out beyond a moderate range rather than increasing indefinitely.

## Practical Implications

For investors and hosts evaluating the Boston market:

1. **Prioritize demand drivers over feature accumulation.** Since occupancy and pricing structure dominate the revenue model, investment dollars are generally better spent improving bookability (pricing strategy, listing quality, responsiveness) than piling on amenities.
2. **Make amenity investment market-specific.** Amenities pay off more in lower-competition neighborhoods. In saturated markets (e.g., Back Bay, Beacon Hill), differentiate through branding, guest experience, and niche positioning rather than amenity count alone.
3. **Don't over-index on reputation metrics in isolation.** A strong review score doesn't substitute for actual demand — evaluate listings (or markets) on realized occupancy, not just star ratings.
4. **Target high-density, high-demand neighborhoods first**, since location effects on revenue are large and consistent across the analysis.

## Tools Used

- **Python** — `pandas`, `numpy`, `statsmodels` for data cleaning, feature engineering, and OLS regression
- **Tableau** — exploratory data visualization and dashboarding
- **Inside Airbnb** — public listings data source

## Repository Structure

```
boston-airbnb-investment-analysis/
├── README.md
├── notebooks/
│   └── boston_airbnb_analysis.ipynb     # Data cleaning, feature engineering, and regression models
├── tableau/
│   └── boston_airbnb_dashboard.twbx     # Packaged Tableau workbook (8 visualizations)
└── data/
    └── boston_airbnb_clean_for_tableau.csv   # Cleaned dataset used for visualization and modeling
```

## Contact

**Kyle Murphy**
LinkedIn: [linkedin.com/in/kmurphy61](http://www.linkedin.com/in/kmurphy61)
Email: KyleMurphy02@icloud.com
