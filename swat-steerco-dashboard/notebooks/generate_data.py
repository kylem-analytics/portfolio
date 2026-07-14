"""
Generates a mock project pipeline dataset for the SWAT project pipeline dashboard.
Simulates ~70 initiatives moving through a 5-stage operating model:
Intake -> Build -> Governance -> Testing -> Deployment

Output: data/pipeline_data.csv (written relative to this script's location)

DESIGN NOTE ON STATUS LOGIC:
Status is NOT assigned randomly. Each project gets a "planned total duration"
(how long it was expected to take from intake to deployment). Status is then
DERIVED by comparing today's date against intake_date + planned_duration:
  - past that planned date and not yet deployed  -> Delayed
  - within 10 days of that planned date           -> At Risk
  - otherwise                                     -> On Track
  - (Deployment-stage projects can additionally roll as Completed)
This keeps Status, Intake Date, and Target Deployment Date internally
consistent with each other, instead of being independently randomized.
"""

import os
import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

NUM_PROJECTS = 72
TODAY = datetime(2026, 7, 6)

TEAMS = ["Finance", "Reporting", "Investor Services", "Technology"]

# Ordered stages -- index in this list doubles as the "Stage Order" sort key
STAGES = ["Intake", "Build", "Governance", "Testing", "Deployment"]

# Ordered priorities -- index doubles as the "Priority Order" sort key
PRIORITIES = ["Low", "Medium", "High", "Critical"]
PRIORITY_WEIGHTS = [0.25, 0.40, 0.25, 0.10]

# Typical day ranges spent in EACH stage when a project passes through it.
# Used to derive both "days in current stage" and "how long since intake."
STAGE_DAY_RANGES = {
    "Intake": (1, 10),
    "Build": (5, 30),
    "Governance": (5, 45),   # bottleneck stage -> wider/longer range
    "Testing": (3, 20),
    "Deployment": (1, 10),
}

PLANNED_DURATION_RANGE = (25, 65)   # days a project is originally expected to take, end-to-end
AT_RISK_WINDOW_DAYS = 10             # within this many days of plan = "At Risk"

PROJECT_TYPES = [
    "Dashboard", "Automation Flow", "Reporting Tool", "Data Pipeline",
    "Approval Workflow", "Intake Form", "Reconciliation App", "Notification System",
    "Tracker", "Portal", "Integration", "Migration Tool"
]
PROJECT_SUBJECTS = [
    "Investor Onboarding", "Fund Reporting", "NAV Reconciliation", "Capital Call",
    "Distribution Notice", "Compliance Review", "Expense Allocation", "Portfolio Monitoring",
    "Vendor Invoice", "Quarterly Statement", "KYC Refresh", "Deal Pipeline",
    "Cash Management", "Audit Prep", "Investor Query", "LP Reporting"
]

ANALYSTS = [fake.first_name() + " " + fake.last_name()[0] + "." for _ in range(14)]


def weighted_stage():
    # Weight stages so there's a visible bottleneck in Governance (a common real bottleneck)
    return random.choices(STAGES, weights=[0.15, 0.25, 0.30, 0.20, 0.10])[0]


def days_in_current_stage(stage):
    lo, hi = STAGE_DAY_RANGES[stage]
    return random.randint(lo, hi)


def total_days_in_pipeline(stage, current_stage_days):
    """
    Total elapsed time since intake = time spent in current stage PLUS a
    plausible amount of time for each stage already passed through.
    Keeps Intake Date consistent with Current Stage.
    """
    stage_index = STAGES.index(stage)
    prior_days = sum(
        random.randint(*STAGE_DAY_RANGES[prior_stage])
        for prior_stage in STAGES[:stage_index]
    )
    return prior_days + current_stage_days


def get_output_dir():
    """
    Notebook-vs-script path detection: __file__ doesn't exist when running
    inside Jupyter, so fall back to the current working directory in that case.
    Writes to a 'data' subfolder next to wherever the script actually lives.
    """
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        base_dir = os.getcwd()
    return os.path.join(base_dir, "data")


def generate_projects():
    rows = []

    for i in range(1, NUM_PROJECTS + 1):
        project_id = f"SWAT-{1000 + i}"
        project_name = f"{random.choice(PROJECT_SUBJECTS)} {random.choice(PROJECT_TYPES)}"
        team = random.choice(TEAMS)
        stage = weighted_stage()
        priority = random.choices(PRIORITIES, weights=PRIORITY_WEIGHTS)[0]
        owner = random.choice(ANALYSTS)

        stage_days = days_in_current_stage(stage)
        pipeline_days = total_days_in_pipeline(stage, stage_days)
        intake_date = TODAY - timedelta(days=pipeline_days)

        planned_duration = random.randint(*PLANNED_DURATION_RANGE)
        target_date = intake_date + timedelta(days=planned_duration)
        days_until_target = (target_date - TODAY).days  # negative = already past target

        # Deployment-stage projects can be marked Completed; otherwise status is
        # derived from where we stand relative to the planned target date.
        if stage == "Deployment" and random.random() < 0.45:
            status = "Completed"
            # A completed project's target should be at/near its actual finish;
            # pull the target back to on-or-before today so it isn't shown
            # as "completed ahead of a target that hasn't arrived yet."
            if target_date > TODAY:
                target_date = TODAY - timedelta(days=random.randint(0, 20))
        elif days_until_target < 0:
            status = "Delayed"
        elif days_until_target <= AT_RISK_WINDOW_DAYS:
            status = "At Risk"
        else:
            status = "On Track"

        last_update_date = TODAY - timedelta(days=random.randint(0, min(stage_days, 14)))

        steerco_flag = "Yes" if (
            priority in ["High", "Critical"] or status in ["At Risk", "Delayed"]
        ) and status != "Completed" else "No"

        rows.append({
            "Project ID": project_id,
            "Project Name": project_name,
            "Submitting Team": team,
            "Owner": owner,
            "Current Stage": stage,
            "Stage Order": STAGES.index(stage) + 1,
            "Priority": priority,
            "Priority Order": PRIORITIES.index(priority) + 1,
            "Status": status,
            "Intake Date": intake_date.strftime("%Y-%m-%d"),
            "Target Deployment Date": target_date.strftime("%Y-%m-%d"),
            "Last Update Date": last_update_date.strftime("%Y-%m-%d"),
            "Days In Current Stage": stage_days,
            "Total Days In Pipeline": pipeline_days,
            "SteerCo Review Flag": steerco_flag,
        })

    return pd.DataFrame(rows)


def main():
    df = generate_projects()

    output_dir = get_output_dir()
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "pipeline_data.csv")
    df.to_csv(output_path, index=False)

    print(f"Generated {len(df)} rows -> {output_path}")
    print(df["Current Stage"].value_counts())
    print(df["Status"].value_counts())


if __name__ == "__main__":
    main()
