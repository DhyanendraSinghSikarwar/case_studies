"""Generate the synthetic data for Case Study 09: Overlapping risk signals in a credit-limit model.

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business
scenario. It is not actual customer data.

Scenario
--------
Credit-card limits are set as a multiple of each customer's predicted "spending capacity"
(average monthly card spend). The model is refitted every quarter on about 1,000 new
customers. Its coefficients jump around from quarter to quarter, and salary credits
sometimes gets a negative sign. A digital pilot now brings in self-employed customers.

File: data/card_customers.csv: 4,000 existing salaried customers (Q1-Q4, 1,000 each)
      + 600 self-employed customers from the digital pilot (quarter "Pilot").
  customer_id, quarter, segment, age, months_with_bank, credit_score,
  declared_income   (Rs/month, from the application form)
  salary_credits    (Rs/month, average credits into the bank account)
  avg_balance       (Rs, average account balance)
  bureau_card_limits(Rs, total limits on cards with other banks; 0 if none)
  num_other_cards, existing_emi (Rs/month), rent (Rs/month),
  total_obligations (= existing_emi + rent, EXACTLY: a redundant feature-store column),
  avg_monthly_spend (Rs, TARGET: average card spend over 12 months)

True data-generating process
----------------------------
Every customer has an unobserved true income T (log-normal).
  declared_income  = T * exp(N(0, 0.03))
  salary_credits   = T * exp(N(0, 0.03))         salaried customers
                   = 0.55 T * exp(N(0, 0.30))     self-employed (much income is not credited)
  avg_balance      = 0.9 T * exp(N(0, 0.40))
  bureau_card_limits = 2.5 T * exp(N(0, 0.40)) for customers with other cards
log(spend) = log(0.25 * 70k) + 0.80 * (log T - log 70k)
             + 0.10 * (log balance - its mean) + 0.06 * num_other_cards
             - 0.60 * total_obligations / T + 0.002 * (credit_score - 720) + N(0, 0.30)
Spend depends on TRUE income. Declared income and salary credits are two noisy measures
of the same thing (correlation about 0.995 for salaried customers), so a regression
cannot tell them apart: the classic multicollinearity problem.

Run:  python case_studies/09_multicollinearity_credit_limit/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import case_paths, rng_for_case  # noqa: E402

CASE_NUMBER = 9
N_PER_QUARTER = 1_000
N_PILOT = 600


def make_block(rng: np.random.Generator, n: int, self_employed: bool) -> pd.DataFrame:
    log_t = rng.normal(np.log(70_000) + (0.05 if self_employed else 0.0), 0.45, n)
    t = np.exp(log_t)
    declared = t * np.exp(rng.normal(0, 0.03, n))
    if self_employed:
        credits = 0.55 * t * np.exp(rng.normal(0, 0.30, n))
    else:
        credits = t * np.exp(rng.normal(0, 0.03, n))
    balance = 0.9 * t * np.exp(rng.normal(0, 0.40, n))
    n_cards = rng.binomial(4, np.clip(0.15 + 0.25 * (log_t - np.log(70_000)), 0.02, 0.9))
    bureau = np.where(n_cards > 0, 2.5 * t * np.exp(rng.normal(0, 0.40, n)) * np.sqrt(n_cards), 0.0)
    age = np.clip(np.round(rng.normal(35, 8, n) + 4 * (log_t - np.log(70_000))), 21, 65).astype(int)
    months = np.clip(np.round(rng.gamma(2.0, 24, n)), 3, 240).astype(int)
    score = np.clip(np.round(730 + 40 * (log_t - np.log(70_000)) + rng.normal(0, 45, n)), 550, 900).astype(int)
    emi = np.round(np.where(rng.random(n) < 0.45, t * rng.beta(2, 8, n), 0.0), -2)
    rent = np.round(np.where(rng.random(n) < 0.5, t * rng.uniform(0.08, 0.25, n), 0.0), -2)
    oblig = emi + rent

    log_spend = (np.log(0.25 * 70_000) + 0.80 * (log_t - np.log(70_000))
                 + 0.10 * (np.log(balance) - np.log(0.9 * 70_000)) + 0.06 * n_cards
                 - 0.60 * oblig / t + 0.002 * (score - 720) + rng.normal(0, 0.30, n))
    return pd.DataFrame({
        "age": age, "months_with_bank": months, "credit_score": score,
        "declared_income": np.round(declared, -2), "salary_credits": np.round(credits, -2),
        "avg_balance": np.round(balance, -2), "bureau_card_limits": np.round(bureau, -3),
        "num_other_cards": n_cards, "existing_emi": emi, "rent": rent, "total_obligations": oblig,
        "avg_monthly_spend": np.round(np.exp(log_spend), -1),
    })


def generate(rng: np.random.Generator) -> pd.DataFrame:
    blocks = []
    for q in ["2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4"]:
        b = make_block(rng, N_PER_QUARTER, self_employed=False)
        b.insert(0, "segment", "Salaried (existing)")
        b.insert(0, "quarter", q)
        blocks.append(b)
    p = make_block(rng, N_PILOT, self_employed=True)
    p.insert(0, "segment", "Self-employed (digital pilot)")
    p.insert(0, "quarter", "Pilot")
    blocks.append(p)
    df = pd.concat(blocks, ignore_index=True)
    df.insert(0, "customer_id", [f"CC9{100000 + i}" for i in range(len(df))])
    return df


def main() -> None:
    paths = case_paths(CASE_DIR)
    df = generate(rng_for_case(CASE_NUMBER))
    df.to_csv(paths["data"] / "card_customers.csv", index=False)
    print(df.groupby("segment").describe().T.round(0).head(40))


if __name__ == "__main__":
    main()
