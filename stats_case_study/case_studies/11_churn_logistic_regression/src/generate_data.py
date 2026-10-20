"""Generate the synthetic data for Case Study 11: Which customers are about to churn?

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business
scenario. It is not actual customer data.

Scenario
--------
A retail bank wants to know which savings-account customers will close their account (or
move their money out) in the next 6 months, why, and whom the retention team should call.

File: data/savings_customers.csv: 12,000 customers observed on 2025-12-31, with churn
measured over the following 6 months.
  customer_id, age, tenure_years, segment (Mass < Affluent < Privileged, plus NRI),
  region (North / South / East / West / Central), num_products (1-4), salary_account (0/1),
  has_credit_card (0/1), digital_logins_per_month, balance_change_3m_pct,
  complaints_6m (0 / 1 / 2+), churned_6m (0/1, TARGET)

True data-generating process (log-odds of churn)
------------------------------------------------
logit(p) = -1.35
           + 1.10 * exp(-tenure / 1.5)            (new customers churn more; non-linear)
           - 0.015 * (age - 40)
           - 0.45 * (num_products - 1)
           - 0.90 * salary_account
           - 0.30 * has_credit_card
           - 0.06 * digital_logins_per_month
           - 0.025 * balance_change_3m_pct          (draining balances -> churn)
           + 0.95 * [1 complaint] + 1.65 * [2+ complaints]
           - 0.55 * salary_account * [any complaint]   (complaints hurt less when salary is paid in)
           + segment: Affluent -0.10, Privileged -0.30, NRI -4.0 (locked-in FCNR deposits)
           + region: no effect
The NRI segment is tiny and almost never churns: it is there to show "separation".

Run:  python case_studies/11_churn_logistic_regression/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import case_paths, rng_for_case  # noqa: E402

CASE_NUMBER = 11
N = 12_000
SEGMENTS = {"Mass": 0.0, "Affluent": -0.10, "Privileged": -0.30, "NRI": -4.0}


def generate(rng: np.random.Generator) -> pd.DataFrame:
    seg = rng.choice(list(SEGMENTS), N, p=[0.695, 0.25, 0.05, 0.005])
    age = np.clip(np.round(rng.normal(40, 12, N)), 21, 78).astype(int)
    tenure = np.round(np.minimum(rng.exponential(5.0, N), np.maximum(age - 18, 0.5)), 1)
    region = rng.choice(["North", "South", "East", "West", "Central"], N, p=[0.24, 0.26, 0.15, 0.22, 0.13])
    seg_rich = pd.Series(seg).map({"Mass": 0, "Affluent": 1, "Privileged": 2, "NRI": 1}).to_numpy()
    n_prod = np.clip(1 + rng.poisson(0.6 + 0.5 * seg_rich + 0.04 * tenure), 1, 4)
    salary = (rng.random(N) < 0.45).astype(int)
    card = (rng.random(N) < np.clip(0.25 + 0.15 * seg_rich + 0.1 * salary, 0, 0.9)).astype(int)
    logins = rng.poisson(np.clip(9 - 0.12 * (age - 40), 1, 20))
    bal = np.clip(np.round(rng.normal(2, 22, N), 1), -100, 150)
    comp = rng.choice([0, 1, 2], N, p=[0.85, 0.11, 0.04])

    logit = (-1.35 + 1.10 * np.exp(-tenure / 1.5) - 0.015 * (age - 40) - 0.45 * (n_prod - 1)
             - 0.90 * salary - 0.30 * card - 0.06 * logins - 0.025 * bal
             + 0.95 * (comp == 1) + 1.65 * (comp == 2) - 0.55 * salary * (comp > 0)
             + pd.Series(seg).map(SEGMENTS).to_numpy())
    p = 1 / (1 + np.exp(-logit))
    churn = (rng.random(N) < p).astype(int)

    return pd.DataFrame({
        "customer_id": [f"SB11{100000 + i}" for i in range(N)], "age": age, "tenure_years": tenure,
        "segment": seg, "region": region, "num_products": n_prod, "salary_account": salary,
        "has_credit_card": card, "digital_logins_per_month": logins, "balance_change_3m_pct": bal,
        "complaints_6m": np.array(["0", "1", "2+"])[comp], "churned_6m": churn,
    })


def main() -> None:
    paths = case_paths(CASE_DIR)
    df = generate(rng_for_case(CASE_NUMBER))
    df.to_csv(paths["data"] / "savings_customers.csv", index=False)
    print(df.describe().round(2))
    print("churn rate:", df.churned_6m.mean().round(4))
    print(df.groupby("segment").churned_6m.agg(["size", "sum", "mean"]))
    print(df.groupby("complaints_6m").churned_6m.mean())


if __name__ == "__main__":
    main()
