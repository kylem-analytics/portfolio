"""
Generates a mock project pipeline dataset for the SWAT SteerCo Dashboard project.
Simulates ~70 initiatives moving through a 5-stage operating model:
Intake -> Build -> Governance -> Testing -> Deployment

Output: pipeline_data.csv
"""

import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)
random.seed(42)

NUM_PROJECTS = 72

TEAMS = ["Finance", "Reporting", "Investor Services", "Technology"]
STAGES = ["Intake", "Build", "Governance", "Testing", "Deployment"]
PRIORITIES = ["Low", "Medium", "High", "Critical"]
PRIORITY_WEIGHTS = [0.25, 0.40, 0.25, 0.10]
STATUSES = ["On Track", "At Risk", "Delayed", "Completed"]

# Realistic-sounding project name components
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

def days_in_stage(stage, status):
    # Typical healthy ranges per stage
    base_ranges = {
        "Intake": (1, 10),
        "Build": (5, 30),
        "Governance": (5, 45),  # bottleneck stage -> wider/longer range
        "Testing": (3, 20),
        "Deployment": (1, 10),
    }
    lo, hi = base_ranges[stage]
    days = random.randint(lo, hi)
    if status == "Delayed":
        days += random.randint(15, 40)
    elif status == "At Risk":
        days += random.randint(5, 15)
    return days

rows = []
today = datetime(2026, 7, 6)

for i in range(1, NUM_PROJECTS + 1):
    project_id = f"SWAT-{1000 + i}"
    project_name = f"{random.choice(PROJECT_SUBJECTS)} {random.choice(PROJECT_TYPES)}"
    team = random.choice(TEAMS)
    stage = weighted_stage()
    priority = random.choices(PRIORITIES, weights=PRIORITY_WEIGHTS)[0]
    owner = random.choice(ANALYSTS)

    # Status logic: Deployment stage items are more likely Completed
    if stage == "Deployment":
        status = random.choices(STATUSES, weights=[0.35, 0.15, 0.10, 0.40])[0]
    else:
        status = random.choices(STATUSES, weights=[0.55, 0.25, 0.20, 0.0])[0]

    stage_days = days_in_stage(stage, status)
    intake_date = today - timedelta(days=random.randint(20, 180))
    last_update_date = today - timedelta(days=random.randint(0, min(stage_days, 14)))
    target_deployment_date = intake_date + timedelta(days=random.randint(60, 150))

    steerco_flag = "Yes" if (priority in ["High", "Critical"] or status in ["At Risk", "Delayed"]) and status != "Completed" else "No"

    rows.append({
        "Project ID": project_id,
        "Project Name": project_name,
        "Submitting Team": team,
        "Owner": owner,
        "Current Stage": stage,
        "Priority": priority,
        "Status": status,
        "Intake Date": intake_date.strftime("%Y-%m-%d"),
        "Target Deployment Date": target_deployment_date.strftime("%Y-%m-%d"),
        "Last Update Date": last_update_date.strftime("%Y-%m-%d"),
        "Days In Current Stage": stage_days,
        "SteerCo Review Flag": steerco_flag,
    })

df = pd.DataFrame(rows)
df.to_csv("pipeline_data.csv", index=False)
print(f"Generated {len(df)} rows -> pipeline_data.csv")
print(df["Current Stage"].value_counts())
print(df["Status"].value_counts())
