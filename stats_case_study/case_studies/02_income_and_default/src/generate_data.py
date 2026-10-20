"""Generate the synthetic data for Case Study 02: Do higher earners default less?

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business
scenario. It is not actual customer data.

Scenario
--------
A lender's Risk Policy team proposes raising the minimum monthly income for
personal loans from Rs 20,000 to Rs 30,000, on the belief that "low earners
default more". The analyst receives a performance file of 6,000 personal loans
disbursed in 2024, each observed for 12 months, with the default outcome known.

How each variable is generated (and why it exists)
--------------------------------------------------
city_tier         Metro (40%) / Tier-2 (35%) / Tier-3 (25%). Incomes are higher in
                  metros (x1.25) and lower in Tier-3 (x0.80).
employment_type   Salaried (70%) / Self-employed (30%). Self-employed incomes are
                  more dispersed and their default risk is slightly higher.
monthly_income    Log-normal (money is right-skewed): median ~Rs 45k x city factor,
                  sigma 0.55 (salaried) / 0.75 (self-employed). Floor Rs 20k = the
                  current policy minimum. A handful of very high, genuine incomes.
credit_score      Bureau score, positively related to (log) income: richer
                  customers tend to have longer, cleaner credit histories.
                  score = 725 + 22 * z(log income) + Normal(0, 48), clipped to 300-900.
loan_amount       income x Lognormal(median 3.6, sigma 0.45), Rs 30k - Rs 10 lakh.
dti               Debt-to-income ratio. Lower-income customers carry relatively more
                  debt: Beta noise shifted down as income rises.
defaulted         1 = 90+ days past due within 12 months. True model (logit):
                  -0.40 * log(income / 45k)  (a modest direct income effect)
                  -0.011 * (score - 725)      (credit history)
                  +3.0 * (dti - 0.35)          (affordability)
                  +0.30 * self-employed
                  Intercept calibrated so the overall default rate is ~7%.
                  Note: income is ALSO linked to default through score and DTI,
                  so the raw income-default association is larger than the
                  direct income effect. Case 08 / 27 untangle this.

Data-quality problems injected
------------------------------
- 7 rows with monthly_income = 0 (a system default for "not captured")
- 52 rows with missing monthly_income (blank)

Run:  python case_studies/02_income_and_default/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import case_paths, rng_for_case  # noqa: E402

CASE_NUMBER = 2
N_LOANS = 6_000
TARGET_DEFAULT_RATE = 0.07


def generate(rng: np.random.Generator, n: int) -> pd.DataFrame:
    df = pd.DataFrame({
        "loan_id": [f"PL24{200000 + i}" for i in range(n)],
        "city_tier": rng.choice(["Metro", "Tier-2", "Tier-3"], n, p=[0.40, 0.35, 0.25]),
        "employment_type": rng.choice(["Salaried", "Self-employed"], n, p=[0.70, 0.30]),
    })
    city_factor = df["city_tier"].map({"Metro": 1.25, "Tier-2": 1.0, "Tier-3": 0.80}).to_numpy()
    salaried = df["employment_type"].eq("Salaried").to_numpy()
    sigma = np.where(salaried, 0.55, 0.75)
    log_inc = np.log(45_000 * city_factor) + rng.normal(0, 1, n) * sigma
    income = np.exp(log_inc)
    # Current policy floor: applicants below Rs 20k were not approved -> resample them above the floor.
    low = income < 20_000
    income[low] = 20_000 + rng.exponential(6_000, low.sum())
    df["monthly_income"] = np.round(income, -2)

    z_inc = (np.log(df["monthly_income"]) - np.log(df["monthly_income"]).mean()) / np.log(df["monthly_income"]).std()
    df["credit_score"] = np.clip(np.round(725 + 22 * z_inc + rng.normal(0, 48, n)), 300, 900).astype(int)

    amount = df["monthly_income"] * np.exp(rng.normal(np.log(3.6), 0.45, n))
    df["loan_amount"] = np.clip(np.round(amount, -4), 30_000, 1_000_000).astype(int)

    # Lower income -> relatively more debt burden.
    dti = rng.beta(4, 8, n) + 0.06 * (-z_inc)
    df["dti"] = np.round(np.clip(dti, 0.03, 0.80), 3)

    linear = (-0.40 * np.log(df["monthly_income"] / 45_000) - 0.011 * (df["credit_score"] - 725)
              + 3.0 * (df["dti"] - 0.35) + 0.30 * (~salaried))
    lo, hi = -10.0, 5.0
    for _ in range(60):  # calibrate intercept to the target default rate
        mid = (lo + hi) / 2
        if (1 / (1 + np.exp(-(mid + linear)))).mean() > TARGET_DEFAULT_RATE:
            hi = mid
        else:
            lo = mid
    p = 1 / (1 + np.exp(-(lo + linear)))
    df["defaulted"] = (rng.random(n) < p).astype(int)
    return df


def inject_quality_issues(rng: np.random.Generator, df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    idx = rng.choice(out.index, 59, replace=False)
    out.loc[idx[:7], "monthly_income"] = 0          # "not captured" coded as zero
    out.loc[idx[7:], "monthly_income"] = np.nan      # blank
    return out


def main() -> None:
    paths = case_paths(CASE_DIR)
    rng = rng_for_case(CASE_NUMBER)
    df = inject_quality_issues(rng, generate(rng, N_LOANS))
    df.to_csv(paths["data"] / "loan_performance_2024.csv", index=False)
    print(f"{len(df):,} loans | default rate {df['defaulted'].mean():.2%} | "
          f"median income {df['monthly_income'].median():,.0f}")


if __name__ == "__main__":
    main()
