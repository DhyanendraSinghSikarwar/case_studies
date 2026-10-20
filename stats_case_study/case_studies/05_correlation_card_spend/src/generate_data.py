"""Generate the synthetic data for Case Study 05: What correlation can and cannot tell you.

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business
scenario. It is not actual customer data.

Scenario
--------
The Head of Cards has three proposals, each based on a correlation:
  1. "Customers with higher credit limits spend more, so raise everyone's limit by 30%."
  2. "Customers who log in more spend LESS, so the app is not worth investing in."
  3. "Age is uncorrelated with spend, so stop age-based targeting."

Files
-----
1. data/cardholders.csv: 6,000 active cardholders (one row each), averages over the
   last 6 months:
   customer_id, segment (Mass / Premium / Super-premium), age, monthly_income,
   credit_limit, limit_increase_12m (1 if the bank raised the limit in the last year),
   monthly_spend, utilization (spend / limit), txn_count (transactions per month),
   avg_ticket (spend per transaction), app_logins (per month), tenure_months

2. data/_answer_key_limit_effect.csv: TEACHING ONLY. Each customer's (unobservable)
   desired spend and the spend they would have with a 30% higher limit. Used once, at the
   end of the notebook, to show the true effect of the proposed limit increase.

3. data/monthly_marketing_vs_spend.csv: 36 months of total marketing spend and
   total card spend (both trending upwards for unrelated reasons).

True data-generating process (what the analyst does NOT know)
-------------------------------------------------------------
- Income: log-normal by segment. It drives BOTH the credit limit (bank policy:
  limit ~ 0.7-1.8x monthly income) AND desired spend (~30% of income), so limit and
  spend are correlated mainly through income (confounding).
- Age: desired spend follows an inverted U (peak around 40-45). The age-spend
  relationship is strong but non-linear, so Pearson r ~ 0.
- About 25% of customers are "revolvers" whose desired spend is ~2.8x a transactor's.
- Desired spend is capped by the limit: actual spend = min(desired, 0.92 * limit).
  Raising a limit only increases spend for customers who are at their limit
  (a minority, almost all revolvers). For everyone else the limit does not bind.
- Reverse causality: the bank's limit-increase programme targets customers
  with high past spend (limit_increase_12m), so high spend -> higher limit.
- Engagement: app_logins rise modestly with spend within each segment, but Mass
  customers log in far more (they check balances), so the overall login-spend
  correlation is weak.
- Transactions vs ticket size: within each segment, customers who transact more
  make smaller purchases (negative). But Super-premium customers have both more
  transactions and bigger tickets, so the pooled correlation is positive.
- Outliers: 12 corporate-style cards with very high limits and spend (they create
  correlation in subsets); 15 rows with spend keyed in paise (x100), a unit error
  that distorts Pearson correlations.
- Time series: marketing spend and card spend both trend upwards (business growth
  and inflation) with independent month-to-month noise: high correlation in levels,
  about zero in month-on-month changes.

Run:  python case_studies/05_correlation_card_spend/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import case_paths, rng_for_case  # noqa: E402

CASE_NUMBER = 5
N = 6_000


def cardholders(rng: np.random.Generator) -> pd.DataFrame:
    seg = rng.choice(["Mass", "Premium", "Super-premium"], N, p=[0.70, 0.25, 0.05])
    log_med = pd.Series(seg).map({"Mass": np.log(45_000), "Premium": np.log(110_000), "Super-premium": np.log(300_000)}).to_numpy()
    income = np.round(np.exp(log_med + rng.normal(0, 0.35, N)), -2)
    age = np.clip(np.round(rng.normal(40, 11, N)), 21, 72).astype(int)

    # Desired spend: ~30% of income, inverted U in age (peak ~42), lognormal noise.
    age_factor = np.exp(-((age - 42) / 14) ** 2 * 0.9)
    desired = 0.30 * income * (0.45 + 0.75 * age_factor) * np.exp(rng.normal(0, 0.30, N))
    # Revolvers (~25%) carry balances and want to spend far more relative to income than transactors.
    revolver = rng.random(N) < 0.25
    desired = desired * np.where(revolver, 2.8, 1.0)

    # Base limit set by policy from income; limit increases go to high past spenders (reverse causality).
    base_limit = income * np.exp(rng.normal(np.log(1.1), 0.30, N))
    past_spend_ratio = desired / base_limit
    p_increase = 1 / (1 + np.exp(-(-2.2 + 6 * (past_spend_ratio - 0.25))))
    increased = rng.random(N) < p_increase
    limit = np.round(base_limit * np.where(increased, 1.35, 1.0), -3)

    spend = np.minimum(desired, 0.92 * limit)                        # the limit binds only for some customers
    txn_mult = pd.Series(seg).map({"Mass": 1.0, "Premium": 1.3, "Super-premium": 2.2}).to_numpy()
    ticket_base = pd.Series(seg).map({"Mass": 900, "Premium": 1_600, "Super-premium": 4_500}).to_numpy()
    # Within a segment, the same spend is split into either many small or few large purchases.
    style = rng.normal(0, 0.45, N)
    txn = np.clip(np.round(txn_mult * 14 * np.exp(style) * (spend / (0.3 * income)) ** 0.4), 1, None)
    ticket = spend / txn
    logins_rate = pd.Series(seg).map({"Mass": 22, "Premium": 10, "Super-premium": 6}).to_numpy() * (spend / (0.3 * income)) ** 0.35
    logins = rng.poisson(logins_rate)

    df = pd.DataFrame({
        "customer_id": [f"CARD{100000 + i}" for i in range(N)], "segment": seg, "age": age,
        "monthly_income": income, "credit_limit": limit, "limit_increase_12m": increased.astype(int),
        "monthly_spend": np.round(spend, -1), "txn_count": txn.astype(int), "avg_ticket": np.round(ticket),
        "app_logins": logins, "tenure_months": rng.integers(6, 180, N),
    })
    # Corporate-style outliers: very high limits and spend.
    corp = rng.choice(np.where(df["segment"] == "Premium")[0], 12, replace=False)
    df.loc[corp, "credit_limit"] = rng.uniform(1.5e6, 2.5e6, 12).round(-3)
    df.loc[corp, "monthly_spend"] = (df.loc[corp, "credit_limit"] * rng.uniform(0.45, 0.7, 12)).round(-1)
    df.loc[corp, "avg_ticket"] = (df.loc[corp, "monthly_spend"] / df.loc[corp, "txn_count"]).round()
    # Unit error: spend keyed in paise (x100) for 15 Mass customers.
    err = rng.choice(np.where(df["segment"] == "Mass")[0], 15, replace=False)
    df.loc[err, "monthly_spend"] = df.loc[err, "monthly_spend"] * 100
    df["utilization"] = np.round(df["monthly_spend"] / df["credit_limit"], 4)
    # Teaching-only answer key: unobservable desired spend, and the spend each customer WOULD have
    # with a 30% higher limit (outliers excluded). A real analyst never has this.
    key = pd.DataFrame({"customer_id": df["customer_id"], "desired_spend": np.round(desired, -1),
                        "spend_if_limit_plus_30pct": np.round(np.minimum(desired, 0.92 * limit * 1.30), -1)})
    key = key[~key.index.isin(np.r_[corp, err])]
    return df, key


def monthly_series(rng: np.random.Generator) -> pd.DataFrame:
    months = pd.period_range("2022-01", "2024-12", freq="M")
    t = np.arange(len(months))
    marketing = 2.0 + 0.045 * t + rng.normal(0, 0.18, len(t))                 # ₹ crore / month
    season = 0.6 * np.sin(2 * np.pi * (t - 8) / 12)
    card = 380 + 6.0 * t + season * 12 + rng.normal(0, 9, len(t))            # ₹ crore / month
    return pd.DataFrame({"month": months.astype(str), "marketing_spend_cr": marketing.round(2), "card_spend_cr": card.round(1)})


def main() -> None:
    paths = case_paths(CASE_DIR)
    rng = rng_for_case(CASE_NUMBER)
    cards, key = cardholders(rng)
    ts = monthly_series(rng)
    cards.to_csv(paths["data"] / "cardholders.csv", index=False)
    key.to_csv(paths["data"] / "_answer_key_limit_effect.csv", index=False)
    ts.to_csv(paths["data"] / "monthly_marketing_vs_spend.csv", index=False)
    print(cards[["monthly_income", "credit_limit", "monthly_spend", "age", "app_logins", "txn_count", "avg_ticket"]].corr().round(2))


if __name__ == "__main__":
    main()
