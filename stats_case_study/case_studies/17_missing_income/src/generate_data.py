"""Generate the synthetic data for Case Study 17: The missing income problem.

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business
scenario. It is not actual customer data.

Scenario
--------
A lender's personal-loan scorecard uses monthly income, but About a quarter of applications arrive
without it (customers skip the field, agents do not upload payslips, or income is "pending
verification"). The credit team plans to (a) delete those applications from the model
data, or (b) fill in the average income. Which strategy gives the right answers, and does
it matter?

Files
-----
data/applications.csv: 8,000 applications with known 12-month outcome.
  app_id, age, employment_type (Salaried / Self-employed / Gig), channel (Branch / Online / Agent),
  city_tier (1-3), loan_amount (Rs), employment_years (5% missing),
  monthly_income (about 23% missing), credit_score (about 6% missing: thin credit file),
  defaulted (0/1, TARGET)
data/answer_key_teaching_only.csv: app_id, true_income, income_missing (what really happened).
  NOT available in real life. Used only to grade the strategies.

True data-generating process
----------------------------
log(income) = log(45,000) + city tier effect (-0.25 per tier above 1) + employment shift
              (Self-employed +0.12, Gig -0.35) + 0.015*(age-35) + Normal(0, 0.45)
credit_score = 700 + 45*(log income - 10.7) + Normal(0, 55); about 6% thin files have no score
               (more likely for the young and for Gig workers).
default: logit = -2.5 - 1.0*(log income - 10.7) - 0.008*(score - 700) + 0.45*Gig + 0.7*thin_file
                 + 0.5*(loan_amount / (12*income))
Missingness:
  employment_years: Missing Completely At Random (MCAR), 5%.
  credit_score: MISSING = thin file (a real property of the customer, which is itself informative).
  income: logit P(missing) = -2.6 + 1.0*Self-employed + 0.8*Gig + 0.7*Agent + 0.5*Online
          - 1.4*(log income - 10.7) + 0.6*defaulted.
          The employment, channel and default terms depend only on OBSERVED variables (Missing At
          Random, MAR; note that the OUTCOME is one of them: applicants who later default are less
          likely to have provided income). The income term depends on the missing value itself
          (Missing Not At Random, MNAR): low earners are less likely to provide proof of income.

Run:  python case_studies/17_missing_income/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import case_paths, rng_for_case  # noqa: E402

CASE_NUMBER = 17
N = 8_000


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def generate(rng: np.random.Generator) -> tuple[pd.DataFrame, pd.DataFrame]:
    emp = rng.choice(["Salaried", "Self-employed", "Gig"], N, p=[0.60, 0.25, 0.15])
    channel = rng.choice(["Branch", "Online", "Agent"], N, p=[0.35, 0.40, 0.25])
    tier = rng.choice([1, 2, 3], N, p=[0.35, 0.40, 0.25])
    age = np.clip(np.round(rng.normal(35, 9, N)), 21, 62).astype(int)
    shift = pd.Series(emp).map({"Salaried": 0.0, "Self-employed": 0.12, "Gig": -0.35}).to_numpy()
    log_inc = np.log(45_000) - 0.25 * (tier - 1) + shift + 0.015 * (age - 35) + rng.normal(0, 0.45, N)
    income = np.round(np.exp(log_inc), -2)
    score_true = np.clip(np.round(700 + 45 * (log_inc - 10.7) + rng.normal(0, 55, N)), 450, 900)
    thin = rng.random(N) < sigmoid(-2.9 - 0.04 * (age - 35) + 0.8 * (emp == "Gig"))
    emp_years = np.clip(np.round(np.maximum(age - 21, 0) * rng.beta(2.0, 2.2, N), 1), 0, 40)
    loan = np.round(np.exp(np.log(300_000) + 0.7 * (log_inc - 10.7) + rng.normal(0, 0.5, N)), -3)
    score_used = np.where(thin, 650, score_true)

    logit = (-2.5 - 1.0 * (log_inc - 10.7) - 0.008 * (score_used - 700) + 0.45 * (emp == "Gig") + 0.7 * thin
             + 0.5 * (loan / (12 * income)))
    default = (rng.random(N) < sigmoid(logit)).astype(int)

    miss_logit = (-2.6 + 1.0 * (emp == "Self-employed") + 0.8 * (emp == "Gig") + 0.7 * (channel == "Agent")
                  + 0.5 * (channel == "Online") - 1.4 * (log_inc - 10.7) + 0.6 * default)
    inc_missing = rng.random(N) < sigmoid(miss_logit)

    df = pd.DataFrame({
        "app_id": [f"AP17{100000 + i}" for i in range(N)], "age": age, "employment_type": emp, "channel": channel,
        "city_tier": tier, "loan_amount": loan,
        "employment_years": np.where(rng.random(N) < 0.05, np.nan, emp_years),
        "monthly_income": np.where(inc_missing, np.nan, income),
        "credit_score": np.where(thin, np.nan, score_true),
        "defaulted": default,
    })
    key = pd.DataFrame({"app_id": df["app_id"], "true_income": income, "income_missing": inc_missing.astype(int)})
    return df, key


def main() -> None:
    paths = case_paths(CASE_DIR)
    df, key = generate(rng_for_case(CASE_NUMBER))
    df.to_csv(paths["data"] / "applications.csv", index=False)
    key.to_csv(paths["data"] / "answer_key_teaching_only.csv", index=False)
    print(df.isna().mean().round(3).to_dict())
    print("default rate", df["defaulted"].mean().round(4))
    print("true mean log income all vs observed:", np.log(key["true_income"]).mean().round(3),
          np.log(df["monthly_income"].dropna()).mean().round(3))


if __name__ == "__main__":
    main()
