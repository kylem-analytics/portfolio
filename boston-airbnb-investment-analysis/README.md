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
- **Scope:** ~3,470 active listings after cleaning (2,742 used in the regression models, after also dropping listings with no review rating yet)
- **Key engineered features:**
  - `est_monthly_revenue` — trailing 12-month estimated revenue ÷ 12
  - `amenities_count` — parsed from the listing's amenities field
  - `host_years` — host tenure, derived from `host_since`
  - `neighbourhood_listing_count` / `competition_level` — listings per neighborhood, bucketed into Low / Medium / High competition tiers
  - `quality_index` — standardized composite of amenities count and review rating

The full cleaning and feature engineering pipeline is in [`notebooks/boston_airbnb_analysis.ipynb`](notebooks/boston_airbnb_analysis.ipynb).

## Methodology

**1. Data cleaning & feature engineering** (Python / pandas) — parsed price and amenities fields, derived host tenure, built neighborhood-level competition tiers, and constructed a composite quality index.

**2. Exploratory visualization** (Tableau) — eight visualizations covering revenue by location, revenue by neighborhood, amenities vs. reviews, host experience vs. revenue, revenue by competition level, revenue by quality index, amenities distribution, and superhost status vs. revenue, combined into a single interactive dashboard with a room-type filter. See [`tableau/boston_airbnb_dashboard.twbx`](tableau/boston_airbnb_dashboard.twbx).

**3. Statistical modeling** (OLS regression, `statsmodels`) — three nested models predicting estimated monthly revenue:

| | Model 1 | Model 2 | Model 3 |
|---|---|---|---|
| **Includes** | Controls only | + amenities, occupancy, competition | + interaction effects |
| **Adjusted R²** | 0.391 | 0.741 | 0.747 |
| **N** | 2,742 | 2,742 | 2,742 |

Controls: accommodates, beds, nightly price, review rating, host years, number of reviews.
Main variables: amenities count, estimated occupancy, neighborhood listing count.
Interactions: amenities × competition, amenities × occupancy, occupancy × competition.

*N drops from ~3,470 cleaned listings to 2,742 in the regression because `review_scores_rating` is missing for listings without reviews yet, and `statsmodels` excludes any row missing a model variable.*

## Key Findings

- **Demand and price are the strongest drivers of revenue.** Estimated occupancy and nightly price are the two most consistent, highly significant predictors of monthly revenue across all three models — listings that book often and price well outperform regardless of other features.
- **Amenities alone don't move revenue — but they interact with both demand and competition.** Amenities count is not significant on its own once demand and competition are controlled. However, two interaction effects are significant: amenities × neighborhood competition is **negative** (in more saturated neighborhoods, additional amenities show diminishing returns), while amenities × occupancy is **positive** (amenities pay off more for listings that are already booking well, likely because more guests see and benefit from them).
- **Review rating has a small negative association with revenue once demand is controlled.** This is counterintuitive on its face, but consistent with high-volume, lower-priced listings collecting more (and slightly lower) ratings than niche, high-revenue listings with fewer but more enthusiastic reviewers.
- **Host tenure is negatively associated with revenue.** Newer hosts outperform more tenured ones in this data, plausibly because they're entering the market with more current pricing and listing strategies, or because longer-tenured hosts are disproportionately running lower-value properties.
- **Revenue is geographically concentrated.** Downtown, the North End, Fenway, and Back Bay post the highest average monthly revenue; outer neighborhoods like Roxbury trail well behind. Location is a first-order driver of performance.
- **Higher-competition neighborhoods actually show higher average revenue**, not lower — likely because competitive neighborhoods are also the highest-demand ones (Downtown, North End). Competition and demand are intertwined in this market rather than purely substitutes.
- **Superhost listings earn meaningfully more on average** ($2,452/month vs. $1,405/month for non-superhosts), consistent with the signaling framework: status acts as a trust signal that guests reward.
- **There's an amenities "sweet spot" around 30–35 amenities** — the largest concentration of Boston listings falls in this range, and the composite quality index (amenities + rating) rises steadily with revenue, from ~$1,510/month in the bottom quartile to ~$2,919/month in the top quartile.
- **Entire homes substantially outperform private and shared rooms** — averaging roughly $2,226/month in estimated revenue versus $735/month for private rooms — directly answering the question of which listing type is the strongest investment in Boston.

## Practical Implications

For investors and hosts evaluating the Boston market:

1. **Prioritize demand and pricing strategy over feature accumulation.** Occupancy and nightly price dominate the revenue model, so dollars are generally better spent improving bookability (pricing strategy, listing quality, responsiveness) than piling on amenities alone.
2. **Treat amenities as a demand multiplier, not a standalone lever.** Amenities pay off most when a listing is already in demand, and pay off least in highly saturated neighborhoods — invest in amenities to reinforce a strong listing, not to rescue a weak one in a crowded market.
3. **Don't be deterred by competitive neighborhoods.** In this data, higher-competition areas posted *higher* average revenue, not lower — competition and demand move together in Boston rather than canceling each other out. Downtown, the North End, and Back Bay combine strong demand with strong competition, and still outperform.
4. **Favor entire-home listings.** Entire homes earn roughly 3x the average monthly revenue of private rooms in this market, making them the stronger investment type of the three compared in this analysis.
5. **Weight superhost status and review ratings carefully.** Superhost status correlates with meaningfully higher revenue, but raw review rating shows a small negative association once demand is controlled — a reminder to evaluate listings (or markets) on realized booking performance, not star ratings alone.

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
│   └── boston_airbnb_dashboard.twbx     # Packaged Tableau workbook: 8 visualizations + interactive dashboard
└── data/
    └── boston_airbnb_clean_for_tableau.csv   # Cleaned dataset used for visualization and modeling
```

## Contact

**Kyle Murphy**
LinkedIn: [linkedin.com/in/kmurphy61](http://www.linkedin.com/in/kmurphy61)
Email: KyleMurphy02@icloud.com
