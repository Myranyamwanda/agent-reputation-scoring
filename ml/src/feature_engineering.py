"""
Sprint 2 - Behavioural feature engineering.

Aggregates raw CRM activity (tasks.csv, lead.csv) up to one row per
agent, producing the six behavioural features used by the reputation
scoring model. See docs/data-preparation.md for the underlying dataset
inspection and the agent population scope decision.

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


def build_features(user: pd.DataFrame, lead: pd.DataFrame, tasks: pd.DataFrame) -> pd.DataFrame:
    agent_tasks = tasks.groupby("owner_id")

    activity_volume = agent_tasks.size().rename("activity_volume")
    active_days = (
        agent_tasks["activity_date"]
        .apply(lambda d: d.dt.normalize().nunique())
        .rename("active_days")
    )
    features = pd.concat([activity_volume, active_days], axis=1)

    features["task_frequency"] = features["activity_volume"] / features["active_days"]

    tenure_span = (
        agent_tasks["activity_date"]
        .apply(lambda d: (d.max() - d.min()).days + 1)
    )
    features["activity_velocity"] = features["activity_volume"] / tenure_span

    leads_handled = lead.groupby("owner_id").size().rename("leads_handled")
    features = features.join(leads_handled, how="left")
    features["leads_handled"] = features["leads_handled"].fillna(0).astype(int)

    tasks_with_week = tasks.copy()
    tasks_with_week["activity_week"] = tasks_with_week["activity_date"].dt.to_period("W")
    weekly_counts = tasks_with_week.groupby(["owner_id", "activity_week"]).size()

    def concentration(group: pd.Series) -> float:
        return group.std() / group.mean() if group.mean() > 0 else 0.0

    temporal_concentration = (
        weekly_counts.groupby("owner_id").apply(concentration).rename("temporal_concentration")
    )
    features = features.join(temporal_concentration)

    role_lookup = user.set_index("id")["role"]
    features = features.join(role_lookup.rename("role"))

    return features


if __name__ == "__main__":
    user, lead, tasks = load_raw_data()
    features = build_features(user, lead, tasks)

    print(f"Built features for {len(features)} agents")
    print(features["role"].value_counts())
    print("\nNull check:")
    print(features.isnull().sum())

    features.to_csv("data/processed/agent_features.csv")
    print("\nSaved to data/processed/agent_features.csv")
