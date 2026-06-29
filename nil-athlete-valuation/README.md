# NIL Athlete Valuation & Bidding Simulation

A live-auction simulation in which I acted as the analytics staff for a university athletic department, building a valuation model to identify and bid on NIL (Name, Image, and Likeness) athletes under a fixed budget and real roster constraints.

**Completed as part of a Sports Analytics course at Elon University, in partnership with Jack Dermody.** The course provided the assignment structure — a five-phase scenario, guiding questions, and a menu of visualization options at each phase — and assigned each pair a school, a budget, and a starting roster. Jack and I worked through the gap analysis, valuation approach, and bid strategy together and sat side-by-side through the live auction, but each wrote our own notebook independently; the modeling decisions, code, weights, multipliers, and written analysis below are my own write-up of that shared work.

---

## Overview

Assigned to the University of South Florida (USF) with a $510,000 starting NIL budget (later confirmed at $5.1M total program budget across the live auction) and a real starting roster with specific positional weaknesses, the project worked through five phases:

1. **Roster gap analysis** — identify USF's biggest positional weaknesses relative to the available athlete pool
2. **Athlete valuation model** — build a defensible valuation framework for a 25-athlete pool (14 football, 11 basketball)
3. **Bid strategy** — set target athletes, bid ceilings, and a fallback plan before the auction opened
4. **Live auction** — track real-time wins, losses, and unexpected events ("curveballs") as competing schools bid
5. **Post-auction audit** — evaluate whether the model actually led to better decisions than gut instinct would have

## Key Decisions & Findings

- **Chose a weighted composite model over regression**, deliberately. With only 14 football and 11 basketball athletes in the pool, a regression with 8+ features would overfit almost immediately — an R² near 1.0 on 11 observations means very little. Instead, I built a transparent, judgment-based weighted composite (performance, physical rating, recruiting profile, leadership/coachability, with penalties for injury history and academic risk), which is also closer to how real NIL valuation decisions get made in practice.
- **Tied positional need multipliers directly to the roster gap data.** USF's biggest weaknesses were quarterback (58 rated vs. a 79.5 pool average, a 21.5-point gap) and shooting guard (61 vs. 81, a 20-point gap) — these received the largest multipliers (1.5x), while positions where USF was already above the pool average (offensive line, defensive tackle, power forward, center) were discounted below 1.0x so the model wouldn't pay a premium where there was no real need.
- **The model's top targets won the auction.** Marcus DeLeon (QB) was the model's highest-valued athlete and was acquired for $500,000 against a model valuation near $1M — the single biggest value find of the auction. Shooting guard Andre Simms was paid above model value ($3M against a much lower model estimate) as a deliberate in-the-moment decision to fill a critical gap with budget still available.
- **The post-auction audit is the most useful part of this project.** The honest conclusion: the model was a strong baseline for *who* to target and *how much to be willing to pay*, but it could not predict competitor behavior once live bidding started — both the best value (DeLeon) and the worst overpay (a defensive end bid up far past model value by other schools) came from market dynamics the model never saw. That distinction — analytics as a disciplined starting point versus analytics as the final word — is the central takeaway of the project.

## Methodology

**1. Roster gap analysis** — compared USF's current position-by-position ratings against pool averages to identify the largest weaknesses, visualized as a side-by-side gap chart.

**2. Weighted composite valuation** (Python / pandas / scikit-learn for feature scaling) — normalized each athlete's stats to a common scale, applied sport-specific weights reflecting USF's roster needs and institutional priorities, and converted the composite score to a dollar valuation.

**3. Positional need multipliers** — scaled each athlete's valuation up or down (0.8x–1.5x) based on how far USF's current roster sat from the pool average at that position.

**4. Bid strategy & live tracking** — set bid ceilings for primary targets and fallback options, then tracked real wins/losses and unplanned events (e.g., an eligibility risk on a backup target) as the live auction unfolded.

**5. Post-auction radar chart** (Plotly) — compared USF's starting roster ratings against its final, post-auction roster to visualize which gaps actually closed.

## Tools Used

- **Python** — pandas, NumPy, scikit-learn (feature scaling), Plotly (interactive visualizations)
- **Jupyter Notebook**

## Repository Structure

```
nil-athlete-valuation/
├── README.md
├── nil_athlete_valuation.ipynb   # Full 5-phase analysis, model, and post-auction audit
└── aac_nil_athlete_pool.csv      # 25-athlete pool dataset (14 football, 11 basketball)
```

## Contact

**Kyle Murphy**
LinkedIn: [linkedin.com/in/kmurphy61](http://www.linkedin.com/in/kmurphy61)
Email: KyleMurphy02@icloud.com
