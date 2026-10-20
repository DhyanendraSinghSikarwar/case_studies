"""Generate the synthetic data for Case Study 06: Predicting loan amount from income.

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business
scenario. It is not actual customer data.

Scenario
--------
The Personal Loans product team wants a simple tool for branch staff: given an
applicant's verified monthly income, suggest a loan amount to pre-offer, with a
realistic range. They also ask: "how much more do customers borrow for each extra
Rs 10,000 of monthly income?"

File: data/loans_income_amount.csv: 3,000 recently disbursed personal loans.
  loan_id, monthly_income (Rs), loan_amount (Rs), employment_type, disbursal_month

True data-generating process
----------------------------
  loan_amount = 4.3 * income^0.95 * exp(e),  e ~ Normal(0, 0.42)
That is, amount is roughly proportional to income (elasticity 0.95) with
MULTIPLICATIVE noise. The spread of loan amounts grows with income
(heteroscedasticity on the raw scale), and the relationship is linear on the
log-log scale. Self-employed applicants borrow ~10% more for the same income
(used in Case 07, not here). Amounts are rounded to Rs 10,000, floored at
Rs 50,000 and capped at the Rs 20 lakh product limit.

Injected features
-----------------
- 4 high-income applicants (Rs 6-9 lakh/month) whose loans hit the Rs 20 lakh cap.
  These are high-leverage points.
- 2 rows with income keyed as annual (x12): data errors with absurd incomes.

Run:  python case_studies/06_loan_amount_simple_regression/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import case_paths, rng_for_case  # noqa: E402

CASE_NUMBER = 6
N = 3_000


def generate(rng: np.random.Generator) -> pd.DataFrame:
    emp = rng.choice(["Salaried", "Self-employed"], N, p=[0.7, 0.3])
    income = np.round(np.clip(np.exp(rng.normal(np.log(55_000), 0.5, N)), 18_000, 400_000), -2)
    amount = 4.3 * income ** 0.95 * np.exp(rng.normal(0, 0.42, N)) * np.where(emp == "Self-employed", 1.10, 1.0)
    df = pd.DataFrame({
        "loan_id": [f"PL6{100000 + i}" for i in range(N)],
        "disbursal_month": rng.choice(pd.period_range("2025-01", "2025-06", freq="M").astype(str), N),
        "employment_type": emp,
        "monthly_income": income,
        "loan_amount": np.clip(np.round(amount, -4), 50_000, 2_000_000).astype(int),
    })
    # High-income applicants whose requests hit the product cap (high leverage, censored response).
    hni = rng.choice(df.index, 4, replace=False)
    df.loc[hni, "monthly_income"] = rng.uniform(600_000, 900_000, 4).round(-3)
    df.loc[hni, "loan_amount"] = 2_000_000
    # Data errors: annual income keyed as monthly.
    err = rng.choice(df.index.difference(hni), 2, replace=False)
    df.loc[err, "monthly_income"] = df.loc[err, "monthly_income"] * 12
    return df


def main() -> None:
    paths = case_paths(CASE_DIR)
    df = generate(rng_for_case(CASE_NUMBER))
    df.to_csv(paths["data"] / "loans_income_amount.csv", index=False)
    print(df.describe().round(0))


if __name__ == "__main__":
    main()
