"""Generate the synthetic data for Case Study 23: Credit-limit increase and customer spend: bootstrapping skewed metrics.

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business scenario. It is not
actual customer data.

Scenario
--------
A card issuer randomly gave a 25% credit-limit increase to half of a large sample of customers and
compared their spending over the next three months. Spend is extremely skewed: a typical customer spends
around Rs 20,000 a month, 6% spend nothing, and a handful of "whale" customers spend lakhs.
Finance wants confidence intervals for several metrics (mean, median, ratios, a percentile, share of big
spenders, spend per rupee of limit), and a regional team wants the same from a tiny pilot of 60 vs 60 customers.

Files
-----
data/limit_increase_test.csv: 5,000 customers (2,500 per arm, randomised).
data/limit_increase_pilot.csv: 120 customers from a different region (60 per arm, randomised).
  customer_id, group (control / increase), tenure_months, prior_avg_spend_6m (Rs/month), limit_before (Rs),
  limit_after (Rs), avg_monthly_spend_next_3m (Rs/month, OUTCOME)
data/answer_key_teaching_only.csv: the true population values of each metric (from a 3-million-customer simulation).

True data-generating process
----------------------------
prior spend ~ log-normal(median Rs 16,000, sigma 0.9); limit_before = prior spend x U(3, 8), rounded;
next-3-month spend = prior spend x exp(Normal(0, 0.55) + 0.10 * increase) with 6% of customers dormant (spend 0)
and 0.5% "whales" whose spend is multiplied by 12. The 25% limit increase raises spend by about 10% for everybody
who is not dormant (a multiplicative effect on the log scale).

Run:  python case_studies/23_bootstrap_credit_limit_spend/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import case_paths, rng_for_case  # noqa: E402

CASE_NUMBER = 23
EFFECT = 0.10
BIG = 50_000


def sample(rng: np.random.Generator, n_per_arm: int, prefix: str) -> pd.DataFrame:
    n = 2 * n_per_arm
    group = np.r_[np.zeros(n_per_arm, int), np.ones(n_per_arm, int)]
    rng.shuffle(group)
    prior = np.exp(np.log(16_000) + rng.normal(0, 0.9, n))
    tenure = np.clip(np.round(rng.gamma(2.0, 22, n)), 3, 240).astype(int)
    limit_before = np.round(prior * rng.uniform(3, 8, n), -3)
    limit_after = np.where(group == 1, np.round(limit_before * 1.25, -3), limit_before)
    spend = prior * np.exp(rng.normal(0, 0.55, n) + EFFECT * group)
    spend = np.where(rng.random(n) < 0.06, 0.0, spend)
    spend = np.where(rng.random(n) < 0.005, spend * 12, spend)
    return pd.DataFrame({"customer_id": [f"{prefix}{100000 + i}" for i in range(n)], "group": np.where(group == 1, "increase", "control"),
                         "tenure_months": tenure, "prior_avg_spend_6m": np.round(prior, 0), "limit_before": limit_before,
                         "limit_after": limit_after, "avg_monthly_spend_next_3m": np.round(spend, 0)})


def truth(rng: np.random.Generator, n: int = 3_000_000) -> dict:
    out = {}
    arms = {}
    for g in (0, 1):
        prior = np.exp(np.log(16_000) + rng.normal(0, 0.9, n))
        lim = prior * rng.uniform(3, 8, n)
        spend = prior * np.exp(rng.normal(0, 0.55, n) + EFFECT * g)
        spend = np.where(rng.random(n) < 0.06, 0.0, spend)
        spend = np.where(rng.random(n) < 0.005, spend * 12, spend)
        arms[g] = (spend, lim * (1.25 if g else 1.0))
    s0, l0 = arms[0]; s1, l1 = arms[1]
    out["difference in means (Rs)"] = s1.mean() - s0.mean()
    out["ratio of means"] = s1.mean() / s0.mean()
    out["difference in medians (Rs)"] = np.median(s1) - np.median(s0)
    out["ratio of medians"] = np.median(s1) / np.median(s0)
    out["difference in 90th percentiles (Rs)"] = np.percentile(s1, 90) - np.percentile(s0, 90)
    out["difference in share spending over Rs 50,000 (pp)"] = 100 * ((s1 > BIG).mean() - (s0 > BIG).mean())
    out["difference in spend per rupee of limit (pp)"] = 100 * (s1.sum() / l1.sum() - s0.sum() / l0.sum())
    return out


def main() -> None:
    paths = case_paths(CASE_DIR)
    big = sample(rng_for_case(CASE_NUMBER), 2_500, "LI23")
    small = sample(np.random.default_rng([20260401, CASE_NUMBER, 99]), 60, "LP23")
    big.to_csv(paths["data"] / "limit_increase_test.csv", index=False)
    small.to_csv(paths["data"] / "limit_increase_pilot.csv", index=False)
    tr = truth(np.random.default_rng([20260401, CASE_NUMBER, 7]))
    pd.DataFrame({"metric": list(tr), "true_value": list(tr.values())}).to_csv(paths["data"] / "answer_key_teaching_only.csv", index=False)
    print(big.groupby("group")["avg_monthly_spend_next_3m"].agg(["mean", "median", "max", "std"]).round(0))
    print(small.groupby("group")["avg_monthly_spend_next_3m"].agg(["mean", "median", "max", "std"]).round(0))
    print({k: round(v, 3) for k, v in tr.items()})


if __name__ == "__main__":
    main()
