"""
 Synthetic suspicious-behaviour label generation.

There is no ground-truth fraud label in the source CRM data (user.csv,
lead.csv, tasks.csv), which is normal for this kind of problem - real
investigated-fraud labels are rarely available for student/academic
research. Following standard practice in fraud/anomaly-detection
research (e.g. the CERT Insider Threat Dataset, which also relies on
synthetically injected malicious behaviour), this script derives a
synthetic `is_suspicious` label from two simple, named behavioural
rules applied to the agent-month feature set produced by
feature_engineering.py:

1. "Bursty" behaviour - unusually high activity velocity combined with
   unusually concentrated (bursty, non-uniform) weekly activity.
   Flags agents whose activity_velocity and temporal_concentration are
   both at or above their 80th percentile.
2. "Padding" behaviour - a high volume of logged tasks with no leads
   actually handled in that month, which is consistent with activity
   being logged without real client-facing work behind it.
   Flags agents whose activity_volume is at or above its 75th
   percentile AND leads_handled is zero.

The two rules are combined with OR logic, giving a combined flag rate
of ~9.2% before noise. A small amount of random label noise (3%,
flipped independently of the rules) is then added so the label is not
a deterministic function of the features - this avoids an unrealistic
dataset where a model could learn the exact injection rule instead of
a genuinely predictive pattern, and more realistically simulates
imperfect real-world fraud labeling. The noise shifts the final
positive rate to ~11.5%.

This is an explicit, documented scope limitation of the project (see
docs/data-preparation.md) rather than a claim that these labels
reflect real investigated fraud.

Usage:
    python ml/src/label_generation.py
"""

import numpy as np
import pandas as pd

# Percentile thresholds used to derive the rules below. Chosen to
# target an approximate (not exact) 10% combined injection rate before
# noise - see docs/data-preparation.md for the calibration discussion.
VELOCITY_PERCENTILE = 0.80
CONCENTRATION_PERCENTILE = 0.80
VOLUME_PERCENTILE = 0.75

# Fraction of labels randomly flipped after rule-based labeling, to
# simulate imperfect real-world labeling and avoid a trivially
# learnable deterministic rule.
NOISE_RATE = 0.03

# Fixed seed so the noise step is reproducible across runs.
RANDOM_SEED = 42


def load_features(path: str = "data/processed/agent_month_features.csv") -> pd.DataFrame:
    return pd.read_csv(path, index_col=["owner_id", "month"])


def build_labels(features: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of `features` with an added `is_suspicious` column."""
    features = features.copy()

    velocity_cut = features["activity_velocity"].quantile(VELOCITY_PERCENTILE)
    concentration_cut = features["temporal_concentration"].quantile(CONCENTRATION_PERCENTILE)
    volume_cut = features["activity_volume"].quantile(VOLUME_PERCENTILE)

    rule_bursty = (
        (features["activity_velocity"] >= velocity_cut)
        & (features["temporal_concentration"] >= concentration_cut)
    )
    rule_padding = (
        (features["activity_volume"] >= volume_cut)
        & (features["leads_handled"] == 0)
    )

    combined = rule_bursty | rule_padding
    features["is_suspicious"] = combined.astype(int)

    rng = np.random.default_rng(RANDOM_SEED)
    noise_mask = rng.random(len(features)) < NOISE_RATE
    features.loc[noise_mask, "is_suspicious"] = 1 - features.loc[noise_mask, "is_suspicious"]

    return features


if __name__ == "__main__":
    features = load_features()
    labeled = build_labels(features)

    print(f"Labeled {len(labeled)} agent-month rows")
    print(labeled["is_suspicious"].value_counts(normalize=True))

    labeled.to_csv("data/processed/agent_month_labeled.csv")
    print("Saved to data/processed/agent_month_labeled.csv")