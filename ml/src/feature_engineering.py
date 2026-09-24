"""
Sprint 2 - Behavioural feature engineering.

Produces two feature sets from the raw CRM activity (tasks.csv,
lead.csv):

1. Agent-lifetime features (one row per agent, 246 rows) - a simple
   summary view, useful for reporting and sanity checks.
2. Agent-month features (one row per agent per active month, ~12,000
   rows) - the primary dataset used for model training, since it
   gives far more rows to train/evaluate on (see the events-per-
   variable discussion in docs/data-preparation.md) and can capture
   a change in an agent's own behaviour over time, not just a
   lifetime average.

See docs/data-preparation.md for the underlying dataset inspection
and the agent population scope decision.

Usage:
    python ml/src/feature_engineering.py
"""

import pandas as pd


def load_raw_data():
    user = pd.read_csv("data/raw/user.csv")
    lead = pd.read_csv("data/raw/lead.csv")
    tasks = pd.read_csv("data/raw/tasks.csv")
    tasks["activity_date"] = pd.to_datetime(tasks["activity_date"])
    lead["created_date"] = pd.to_datetime(lead["created_date"])
    return user, lead, tasks


def _concentration(group: pd.Series) -> float:
    if len(group) > 1 and group.mean() > 0:
        return group.std() / group.mean()
    return 0.0


def build_lifetime_features(user: pd.DataFrame, lead: pd.DataFrame, tasks: pd.DataFrame) -> pd.DataFrame:
    """One row per agent, summarising their entire observed history."""
    agent_tasks = tasks.groupby("owner_id")

    activity_volume = agent_tasks.size().rename("activity_volume")
    active_days = (
        agent_tasks["activity_date"]
        .apply(lambda d: d.dt.normalize().nunique())
        .rename("active_days")
    )
    features = pd.concat([activity_volume, active_days], axis=1)
    features["task_frequency"] = features["activity_volume"] / features["active_days"]

    tenure_span = agent_tasks["activity_date"].apply(lambda d: (d.max() - d.min()).days + 1)
    features["activity_velocity"] = features["activity_volume"] / tenure_span

    leads_handled = lead.groupby("owner_id").size().rename("leads_handled")
    features = features.join(leads_handled, how="left")
    features["leads_handled"] = features["leads_handled"].fillna(0).astype(int)

    tasks_with_week = tasks.copy()
    tasks_with_week["activity_week"] = tasks_with_week["activity_date"].dt.to_period("W")
    weekly_counts = tasks_with_week.groupby(["owner_id", "activity_week"]).size()
    temporal_concentration = weekly_counts.groupby("owner_id").apply(_concentration).rename("temporal_concentration")
    features = features.join(temporal_concentration)

    role_lookup = user.set_index("id")["role"]
    features = features.join(role_lookup.rename("role"))

    return features


def build_monthly_features(user: pd.DataFrame, lead: pd.DataFrame, tasks: pd.DataFrame) -> pd.DataFrame:
    """One row per agent per active month - the primary dataset for model training."""
    tasks = tasks.copy()
    lead = lead.copy()
    tasks["month"] = tasks["activity_date"].dt.to_period("M")
    lead["month"] = lead["created_date"].dt.to_period("M")

    agent_month = tasks.groupby(["owner_id", "month"])

    activity_volume = agent_month.size().rename("activity_volume")
    active_days = (
        agent_month["activity_date"]
        .apply(lambda d: d.dt.normalize().nunique())
        .rename("active_days")
    )
    features = pd.concat([activity_volume, active_days], axis=1)
    features["task_frequency"] = features["activity_volume"] / features["active_days"]

    days_in_month = features.index.get_level_values("month").days_in_month
    features["activity_velocity"] = features["activity_volume"] / days_in_month

    leads_handled = lead.groupby(["owner_id", "month"]).size().rename("leads_handled")
    features = features.join(leads_handled, how="left")
    features["leads_handled"] = features["leads_handled"].fillna(0).astype(int)

    tasks["activity_week"] = tasks["activity_date"].dt.to_period("W")
    weekly_counts = tasks.groupby(["owner_id", "month", "activity_week"]).size()
    temporal_concentration = (
        weekly_counts.groupby(["owner_id", "month"]).apply(_concentration).rename("temporal_concentration")
    )
    features = features.join(temporal_concentration)

    role_lookup = user.set_index("id")["role"]
    features = features.join(role_lookup.rename("role"), on="owner_id")

    return features


if __name__ == "__main__":
    user, lead, tasks = load_raw_data()

    lifetime = build_lifetime_features(user, lead, tasks)
    print(f"Lifetime features: {len(lifetime)} agents")
    print(lifetime["role"].value_counts())
    lifetime.to_csv("data/processed/agent_features.csv")
    print("Saved to data/processed/agent_features.csv\n")

    monthly = build_monthly_features(user, lead, tasks)
    print(f"Monthly features: {len(monthly)} agent-month rows")
    print(monthly["role"].value_counts())
    print("\nNull check:")
    print(monthly.isnull().sum())
    monthly.to_csv("data/processed/agent_month_features.csv")
    print("Saved to data/processed/agent_month_features.csv")
