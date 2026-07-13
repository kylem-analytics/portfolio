# SWAT project pipeline dashboard

A Power BI dashboard for tracking initiatives moving through a five-stage delivery pipeline: intake, build, governance, testing, and deployment. It includes automated bottleneck detection, proportional aging analysis, and a steering-committee-ready review view.

> **This project uses entirely synthetic, randomly generated mock data. No real company data, project names, or confidential information is used anywhere in this repository. Any resemblance between the mock project names and real initiatives is coincidental.**

## Built with Claude

This project was built in active collaboration with Claude (Anthropic), used throughout as a technical sounding board, not a one-shot generator. The process looked less like "describe the dashboard, receive the dashboard" and more like pair-programming: Claude and I worked through the Python data model and every DAX measure line by line, with Claude explaining the mechanics of each function as we wrote it rather than just producing working code, so every measure in this project is one I can actually explain, not just one that runs.

That back-and-forth was also where most of the real thinking happened. More than once, my first version of a metric looked reasonable but was actually wrong. Claude pushed back with a direct question ("would this still hold if the data changed?") rather than accepting the plausible-looking answer, which is how the flat-threshold and raw-average bottleneck issues below got caught before they shipped, not after. In a few cases I was the one who caught an inconsistency in what Claude proposed (a hardcoded stage name that wouldn't adapt to new data, a safety-net rule quietly contradicting a status rule). The collaboration ran in both directions, which is the point: using an AI tool well here meant treating it as a partner to interrogate, not an answer key to accept.

## Why this exists

Most internal delivery-tracking dashboards eventually run into the same problem. Someone builds a nice-looking chart against one snapshot of data, and six months later nobody trusts it anymore because the thresholds don't reflect how the pipeline actually behaves, or the "bottleneck" everyone points to is just the stage that was slow that one time.

This project was built to avoid that failure mode from the start. The guiding constraint throughout was simple: nothing in this dashboard should be a one-time observation dressed up as a permanent conclusion. Every insight had to survive the question, "would this still be true if the underlying data changed?"

## How it's built, and how it's meant to be used

The pipeline has two halves.

1. **A Python layer that produces a clean, consistent dataset.** In this project, that means a script that generates realistic synthetic data with an internally consistent schedule model. A project's intake date, current stage, target date, and status are all mathematically tied together, not independently randomized (more on that below). In a real deployment, this layer's job would be different but structurally identical: take whatever raw export comes out of the actual source system, clean it, and reshape it into that same consistent schema. The Power BI side doesn't know or care whether the CSV it's reading came from a Python script generating mock data or a Python script cleaning a live export. It just expects the same column names and types every time.
2. **A Power BI model built entirely on DAX measures that calculate relationships in the data, rather than hardcoded values.** This is the more important half. Refresh the underlying CSV with a new dataset that has the same structure, hit Refresh in Power BI, and every card, chart, and table recalculates automatically, including which stage is currently the bottleneck, which items are proportionally aging, and how the flagged review list breaks down. Nothing about the dashboard itself needs to be rebuilt when the data changes.

The practical result: swap in a real data export that matches the expected schema, and the entire analytical layer, every measure, every visual, every threshold, runs against it without modification.

## Things that looked right at first but weren't

A few points where the "obvious" first version of a metric was actually wrong, and why the fix mattered:

- **A flat day-count threshold for "aging" projects only ever flagged one stage.** An early version flagged anything sitting more than 30 days in its current stage. Since governance's normal range runs up to 45 days while most other stages top out well under 30, that threshold could structurally never fire outside governance. It wasn't measuring risk, it was just re-describing which stage happens to be the longest by design. The fix was a proportional measure: how far a project has progressed through its own stage's typical duration, so a testing item running hot and a governance item running hot become genuinely comparable. Both metrics are kept visible side by side on the Pipeline Overview page (labeled "Aging Items (Flat 30-Day)" and "Aging Items (Relative)"), since different organizations track aging differently and some teams may still prefer a flat threshold that matches their own operating norms. That said, the stage-relative measure is generally the more accurate picture of where a pipeline is actually falling behind.
- **The same mistake reappeared one level up, at the stage level.** A "which stage is the bottleneck" measure built on raw average days will always crown whichever stage is naturally the longest, which again isn't a real finding. Recalculating it as an average of each project's proportional progress flipped the answer entirely in this dataset. Governance has the highest raw average, but testing is proportionally the furthest behind relative to its own expected pace. Those are two different, both defensible-sounding claims, and only one of them is actually correct.
- **A status-derived-from-date approach initially produced impossible combinations.** A project could be marked "delayed" with a target date that hadn't arrived yet, because a safety-net rule and a status-assignment rule were quietly fighting each other. The fix was to stop assigning status as an independent random label and instead derive it from a single, honest comparison: today's date against a planned target date calculated from intake. Once status became an output of that relationship instead of an input alongside it, the contradictions were structurally impossible rather than something to catch after the fact.
- **A single flagged-item count hid two different meanings.** Projects land on the executive review list for two distinct reasons: because they're inherently high-stakes (high or critical priority), or because something is actually going wrong (at-risk or delayed status). A project can qualify for both simultaneously. Reporting two overlapping counts side by side, which don't sum to the headline total, is the kind of thing that quietly erodes trust the moment someone checks the arithmetic in a live meeting. The fix was three mutually exclusive categories: priority-only, schedule-only, and both, that always add up cleanly to the total.

## What the data says

Looking at the dashboard as a whole, here's the story this particular mock dataset tells.

**The visible bottleneck and the real one aren't the same stage.** Governance has the longest average time-in-stage (around 23 days), which is what a quick glance would flag. But relative to each stage's own typical pace, testing is running at roughly 70% of its expected duration on average, the highest proportional figure of any stage, while governance sits closer to 50%. If this were a real pipeline, the actionable finding isn't "slow down governance." It's "figure out why testing is running consistently close to its ceiling," which is a different conversation and likely a different fix (capacity, tooling, handoff quality from build).

**A little over half the pipeline needs some form of executive visibility.** 41 of 72 mock projects are flagged for review, split roughly into thirds: about a quarter are flagged purely because they're strategically important, close to half purely because they're behind schedule, and the rest are both at once. That overlap group is the highest-concentration risk, combining importance and trouble in the same projects.

**Intake volume drops off toward the most recent month by design, not because of a real decline.** The mock dataset was generated to only extend into the beginning of the final month, so that month hasn't had a chance to accumulate a full period's worth of intake yet. In a live version of this dashboard, that final data point would simply reflect whatever volume has come in as of the most current date, and would keep updating as more time passes and more projects are logged. It's worth calling this out explicitly, since a trailing partial month is exactly the kind of pattern that can look alarming at a glance if it isn't understood as a timing artifact rather than a real trend.

**Next-step recommendations, if this were a live pipeline instead of mock data:**
- Investigate testing-stage capacity or handoff quality specifically, rather than assuming governance is the priority just because its raw numbers look largest
- Look at whether aging and flagged items cluster around specific analysts or teams rather than being evenly distributed. The underlying data model supports slicing by owner and team, which this dashboard doesn't yet surface as its own view but easily could
- Re-run the intake trend excluding the current partial month before treating any month-over-month change as signal
- Revisit the 80%-of-typical-duration aging threshold periodically. It's a reasonable starting point, not a permanent constant, and should move if the organization's actual delivery pace shifts over time

## Tech stack

- **Python** (pandas, Faker): mock data generation with an internally consistent scheduling model
- **Power BI Desktop**: data modeling, DAX measures, dashboard visuals
- **DAX**: all bottleneck detection, aging thresholds, and flag categorization are calculated dynamically, not hardcoded

## Repo structure

```
swat-steerco-dashboard/
├── data/
│   └── pipeline_data.csv        # mock dataset (72 initiatives)
├── generate_data.py              # generates the mock dataset
├── theme/
│   └── swat-steerco-navy-amber.json   # Power BI theme file
├── screenshots/                  # dashboard screenshots (all 3 pages)
└── README.md
```

## Using this with real data

Swap `data/pipeline_data.csv` for a real export that matches the same column names and types (see `generate_data.py` for the exact schema), then refresh the Power BI file. Every measure and visual recalculates automatically, no rebuilding required. If the real source system's raw export doesn't already match that schema, the Python layer is exactly where that cleanup step belongs, upstream of Power BI ever seeing the data.

## Contact

Kyle Murphy
LinkedIn: [linkedin.com/in/kmurphy61](http://www.linkedin.com/in/kmurphy61)
Email: [KyleMurphy02@icloud.com](mailto:KyleMurphy02@icloud.com)
