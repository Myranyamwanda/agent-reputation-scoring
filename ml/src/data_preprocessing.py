"""
Sprint 1 - CRM dataset inspection.

Run this against the actual raw files (user.csv, lead.csv, tasks.csv)
before writing any feature-engineering code. The goal is to know
exactly which columns exist and how the three tables relate, not to
assume it.
"""

import pandas as pd


def inspect_dataset(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)

    print(f"\n{'=' * 70}\n{file_path}\n{'=' * 70}")

    print("\nShape:", df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:", df.duplicated().sum())

    print("\nFirst five rows:")
    print(df.head())

    return df


if __name__ == "__main__":
    user = inspect_dataset("data/raw/user.csv")
    lead = inspect_dataset("data/raw/lead.csv")
    tasks = inspect_dataset("data/raw/tasks.csv")

    print(f"\n{'=' * 70}\nRELATIONSHIP CHECKS\n{'=' * 70}")

    print("\nuser.role value counts:")
    print(user["role"].value_counts())

    print("\nleads with owner_id found in user.id:",
          lead["owner_id"].isin(user["id"]).sum(), "/", len(lead))

    print("\ntasks with owner_id found in user.id:",
          tasks["owner_id"].isin(user["id"]).sum(), "/", len(tasks))

    print("\ntasks.who_id prefix distribution (polymorphic reference):")
    print(tasks["who_id"].dropna().str[:3].value_counts())

    print("\ntasks.what_id prefix distribution (polymorphic reference):")
    print(tasks["what_id"].dropna().str[:3].value_counts())
