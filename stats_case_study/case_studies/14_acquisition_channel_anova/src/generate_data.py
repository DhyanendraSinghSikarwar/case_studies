"""Generate the synthetic data for Case Study 14: Which acquisition channel brings the most valuable customers?

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business
scenario. It is not actual customer data.

Scenario
--------
A credit-card business acquired about 6,000 new customers last year through five channels.
Marketing must decide how to split next year's acquisition budget. Each customer's
first-year net revenue (interchange + interest + fees - rewards - credit losses) is known,
together with the channel's cost per acquisition (CAC).

Files
-----
data/new_customers.csv: 6,000 customers.
  customer_id, channel (Branch / Search ads / Social media / Aggregator / Partner co-brand),
  age, monthly_income (Rs), first_year_net_revenue (Rs; can be negative), TARGET
data/channel_costs.csv: channel, cost_per_acquisition (Rs)

True data-generating process
----------------------------
Channels attract different customers: aggregator (comparison-site) customers have the
highest incomes, social-media customers the lowest.
net revenue = 3,000 + 2,600 * (log(income) - log(60k)) + channel direct effect + noise
direct effect (vs Branch): Search ads -150, Social media -350, Aggregator -500, Partner co-brand +250
noise SD by channel: Branch 3,000, Search 3,100, Social 2,700, Aggregator 5,200 (rate-chasers and
big spenders, more defaults), Partner 2,500
So the aggregator looks best on raw value (rich customers) but is worst once income is
held fixed, and most expensive to acquire.

Run:  python case_studies/14_acquisition_channel_anova/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import case_paths, rng_for_case  # noqa: E402

CASE_NUMBER = 14
CHANNELS = {  # n, mean log-income shift, direct effect, noise SD, CAC
    "Branch":           (1_800, 0.05, 0, 3_000, 2_200),
    "Search ads":       (1_500, 0.10, -150, 3_100, 1_800),
    "Social media":     (1_200, -0.20, -350, 2_700, 1_100),
    "Aggregator":       (900, 0.40, -500, 5_200, 2_900),
    "Partner co-brand": (600, -0.05, 250, 2_500, 900),
}


def generate(rng: np.random.Generator) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    for ch, (n, inc_shift, direct, sd, _) in CHANNELS.items():
        log_inc = np.log(60_000) + inc_shift + rng.normal(0, 0.45, n)
        age = np.clip(np.round(rng.normal(34 - 6 * (ch == "Social media") + 3 * (ch == "Branch"), 8, n)), 21, 70).astype(int)
        rev = 3_000 + 2_600 * (log_inc - np.log(60_000)) + direct + rng.normal(0, sd, n)
        rows.append(pd.DataFrame({"channel": ch, "age": age, "monthly_income": np.round(np.exp(log_inc), -2),
                                  "first_year_net_revenue": np.round(rev, -1)}))
    df = pd.concat(rows, ignore_index=True)
    df = df.sample(frac=1, random_state=int(rng.integers(1e9))).reset_index(drop=True)
    df.insert(0, "customer_id", [f"NC14{100000 + i}" for i in range(len(df))])
    costs = pd.DataFrame({"channel": list(CHANNELS), "cost_per_acquisition": [v[4] for v in CHANNELS.values()]})
    return df, costs


def main() -> None:
    paths = case_paths(CASE_DIR)
    df, costs = generate(rng_for_case(CASE_NUMBER))
    df.to_csv(paths["data"] / "new_customers.csv", index=False)
    costs.to_csv(paths["data"] / "channel_costs.csv", index=False)
    print(df.groupby("channel")["first_year_net_revenue"].agg(["size", "mean", "std", "median"]).round(0))
    print(df.groupby("channel")["monthly_income"].median())


if __name__ == "__main__":
    main()
