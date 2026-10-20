"""Generate the synthetic data for Case Study 07: What drives the loan amount a customer requests?

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business
scenario. It is not actual customer data.

Scenario
--------
Product and Finance want to understand what drives the amount customers REQUEST
on personal-loan applications (demand, before any credit decision), to design
tiered offers and to forecast disbursement volumes.

File: data/loan_applications.csv: 5,000 applications.
  application_id, monthly_income (Rs), existing_emi (Rs, other monthly debt payments),
  age, credit_score, employment_type (Salaried / Self-employed / Professional),
  loan_purpose (Debt consolidation / Home renovation / Wedding / Education / Medical / Travel),
  city_tier (Metro / Tier-1 / Tier-2 / Tier-3), requested_tenure_months, requested_amount (Rs)

True data-generating process (log scale)
----------------------------------------
log(requested_amount) = 1.75
    + 0.90 * log(income)                           [salaried]
    + 0.12 * (log(income) - log(50k)) extra slope  [self-employed: more income-sensitive]
    + 0.10 self-employed, +0.15 professional         (intercept shifts)
    - 1.30 * (existing_emi / income)                 (affordability: more existing debt -> smaller request)
    + purpose: home renovation +0.35, wedding +0.45, education +0.25,
               medical -0.10, travel -0.35 (vs debt consolidation)
    + 0.0012 * (credit_score - 720)                  (small)
    + Normal(0, 0.38) noise
NO direct effect of city tier or age. They are correlated with income (metro and older
customers earn more), so they look important on their own.
existing_emi is larger for higher earners (in rupees), so its SIMPLE correlation with the
request is positive even though its CONDITIONAL effect is negative.
requested_tenure_months is chosen together with the amount (bigger requests -> longer
tenures). It is an outcome-like variable, not a driver.

Run:  python case_studies/07_loan_amount_drivers/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import case_paths, rng_for_case  # noqa: E402

CASE_NUMBER = 7
N = 5_000
PURPOSE_EFFECT = {"Debt consolidation": 0.0, "Home renovation": 0.35, "Wedding": 0.45, "Education": 0.25,
                  "Medical": -0.10, "Travel": -0.35}


def generate(rng: np.random.Generator) -> pd.DataFrame:
    tier = rng.choice(["Metro", "Tier-1", "Tier-2", "Tier-3"], N, p=[0.35, 0.25, 0.25, 0.15])
    tier_shift = pd.Series(tier).map({"Metro": 0.30, "Tier-1": 0.12, "Tier-2": 0.0, "Tier-3": -0.15}).to_numpy()
    age = np.clip(np.round(rng.normal(36, 9, N)), 21, 60).astype(int)
    emp = rng.choice(["Salaried", "Self-employed", "Professional"], N, p=[0.62, 0.28, 0.10])
    emp_shift = pd.Series(emp).map({"Salaried": 0.0, "Self-employed": 0.05, "Professional": 0.35}).to_numpy()
    log_inc = np.log(48_000) + tier_shift + 0.018 * (age - 36) + emp_shift + rng.normal(0, 0.45, N)
    income = np.round(np.clip(np.exp(log_inc), 15_000, 600_000), -2)

    # Existing EMIs grow with income in rupees; the share of income varies independently.
    emi_share = np.clip(rng.beta(2, 7, N) * np.where(rng.random(N) < 0.25, 0, 1) + 0.03 * (age > 35), 0, 0.6)
    existing_emi = np.round(income * emi_share, -2)
    score = np.clip(np.round(715 + 30 * (log_inc - log_inc.mean()) + rng.normal(0, 50, N)), 400, 900).astype(int)
    purpose = rng.choice(list(PURPOSE_EFFECT), N, p=[0.30, 0.18, 0.12, 0.10, 0.12, 0.18])

    li = np.log(income)
    log_amt = (1.75 + 0.90 * li + 0.12 * (li - np.log(50_000)) * (emp == "Self-employed")
               + 0.10 * (emp == "Self-employed") + 0.15 * (emp == "Professional")
               - 1.30 * existing_emi / income
               + pd.Series(purpose).map(PURPOSE_EFFECT).to_numpy()
               + 0.0012 * (score - 720) + rng.normal(0, 0.38, N))
    amount = np.clip(np.round(np.exp(log_amt), -4), 50_000, 2_500_000).astype(int)
    tenure_options = np.array([12, 24, 36, 48, 60])
    tenure_idx = np.clip(np.round(1.2 * (np.log(amount) - np.log(150_000)) + 2 + rng.normal(0, 0.8, N)), 0, 4).astype(int)

    return pd.DataFrame({
        "application_id": [f"APP7{100000 + i}" for i in range(N)], "monthly_income": income, "existing_emi": existing_emi,
        "age": age, "credit_score": score, "employment_type": emp, "loan_purpose": purpose, "city_tier": tier,
        "requested_tenure_months": tenure_options[tenure_idx], "requested_amount": amount,
    })


def main() -> None:
    paths = case_paths(CASE_DIR)
    df = generate(rng_for_case(CASE_NUMBER))
    df.to_csv(paths["data"] / "loan_applications.csv", index=False)
    print(df.describe().round(1))


if __name__ == "__main__":
    main()
