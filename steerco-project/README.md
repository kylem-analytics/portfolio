# SWAT Project Pipeline & SteerCo Dashboard

A mock Power BI dashboard simulating an internal project intake and delivery tracker, built to model how a firm might monitor initiatives moving through a five-stage operating model — **Intake → Build → Governance → Testing → Deployment** — and surface the right information for SteerCo (steering committee) review.

> All data in this project is synthetic and generated for demonstration purposes only. No real company data is used.

## Why this project

This project models the kind of tooling a project coordination/delivery function needs day to day: a live pipeline tracker, visibility into bottlenecks and aging items, and a reporting view built specifically for executive steering committee meetings.

## What it does

- Tracks ~70 mock initiatives across four submitting teams (Finance, Reporting, Investor Services, Technology)
- Models stage-by-stage progression through a 5-stage delivery pipeline
- Surfaces bottlenecks (e.g., items aging in Governance review)
- Flags at-risk and delayed items by priority
- Produces a SteerCo-ready summary view: what's new, what's stuck, what needs executive attention this cycle

## Tech stack

- **Python (pandas, Faker)** — synthetic data generation
- **Power BI Desktop** — data modeling (DAX measures) and dashboard visuals
- **Power Query** — data shaping/transformation within Power BI

## Repo structure

```
steerco-dashboard/
├── data/
│   └── pipeline_data.csv        # mock dataset (72 initiatives)
├── generate_data.py              # script used to generate the mock data
├── screenshots/                  # dashboard screenshots
├── SWAT_SteerCo_Dashboard.pbix   # Power BI file
└── README.md
```

## Dashboard views

1. **Pipeline Overview** — count of initiatives by stage, priority mix, status breakdown
2. **Aging & Bottleneck Analysis** — days-in-stage distribution, flags items stuck longest
3. **SteerCo Summary** — filtered view of only flagged/at-risk/high-priority items, formatted for executive review

*(Screenshots below once the dashboard is built)*

## Data dictionary

| Field | Description |
|---|---|
| Project ID | Unique identifier |
| Project Name | Mock initiative name |
| Submitting Team | Originating business function |
| Owner | Assigned analyst |
| Current Stage | Intake / Build / Governance / Testing / Deployment |
| Priority | Low / Medium / High / Critical |
| Status | On Track / At Risk / Delayed / Completed |
| Intake Date | Date the initiative entered the pipeline |
| Target Deployment Date | Planned completion date |
| Last Update Date | Most recent status update |
| Days In Current Stage | Time spent in current stage |
| SteerCo Review Flag | Whether the item is due for executive review this cycle |

## How it was built

1. Generated a synthetic dataset with Python (`generate_data.py`), deliberately weighting stages and statuses to create a realistic bottleneck pattern (Governance review taking longest) rather than an artificially clean dataset.
2. Imported into Power BI Desktop and built a data model with DAX measures for aging, SLA breaches, and stage-level counts.
3. Built dashboard visuals aimed at two audiences: day-to-day pipeline management and periodic SteerCo reporting.
