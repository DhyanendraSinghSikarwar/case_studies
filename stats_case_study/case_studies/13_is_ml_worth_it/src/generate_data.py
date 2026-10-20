"""Generate the synthetic data for Case Study 13: Is a machine-learning model worth it?

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business
scenario. It is not actual customer data.

Scenario
--------
A credit-card issuer approves applications with a logistic-regression scorecard.
The ML team proposes a gradient-boosting model. The CRO asks the analyst to
establish, with statistical evidence, whether the ML model is worth it.

File: data/card_applications.csv: ~40,000 approved applications, Jan-2023 to Dec-2024,
each with a 12-month outcome `bad_12m` (1 = 90+ days past due within 12 months).

Columns by type
---------------
Identifier / time : application_id, application_month (YYYY-MM)
Numerical         : age, monthly_income, bureau_score (blank = no bureau history),
                    credit_utilization (share of existing card limits used, 0-1.2),
                    enquiries_6m (bureau enquiries in last 6 months, count),
                    months_since_delinquency (blank = never delinquent),
                    dti (existing EMIs / income), years_at_employer,
                    num_credit_cards, requested_limit
Ordinal           : education (Below 12th < 12th pass < Graduate < Postgraduate)
                    city_tier (Tier-3 < Tier-2 < Tier-1 < Metro)
                    income_verification (Self-declared < Payslip < Bank statement)
Nominal           : occupation (7 levels), residence_type (4), acquisition_channel (5),
                    state (12), marital_status (3)
LEAKAGE (trap)    : collections_contact_flag: 1 if the collections team contacted the
                    customer. This is recorded AFTER account opening, mostly for customers
                    already in arrears, so it cannot be used at application time.

True data-generating process (log-odds of bad_12m)
--------------------------------------------------
  -0.011 * (bureau_score - 720)               linear; no-hit customers +0.55
  +2.6 * (util - 0.35)^2 + 1.6 * max(util - 0.85, 0)   U-shaped; risk rises steeply above 85%
  +0.75 * 1[enquiries_6m > 3]                  step / threshold effect
  -0.45 * log(income / 45k)                    log effect (raw-scale linear is misspecified)
  +dti * (1.0 salaried / 2.6 self-employed or gig)   interaction with occupation
  +0.35 * 1[age < 25]                          young-age step
  +0.80 * 1[months_since_delinquency < 12]
  -0.10 * education level (0-3)                small monotone ordinal effect
  income_verification: +0.30 self-declared, 0 payslip, -0.15 bank statement
  occupation: gig +0.45, student +0.40, self-emp business +0.20, govt -0.40, ...
  channel: DSA +0.35, aggregator +0.20, partner-ecom +0.10
  residence: rented +0.15, company-provided -0.10
  state: two states +0.25, others 0
  +0.30 * (util > 0.85) * (bureau_score < 700)     a second, weaker interaction
  city_tier and marital_status: NO direct effect (city_tier correlates with income,
  so it looks associated on its own; marital_status is pure noise)
  num_credit_cards: tiny effect; strongly correlated with bureau_score and income
  requested_limit: no direct effect; ~0.85 correlated with income (multicollinearity)
Intercept calibrated for a ~8% bad rate. Mild drift in 2024: more aggregator-sourced
customers and higher utilisation.

Data-quality problems injected
------------------------------
- 25 duplicated rows; inconsistent occupation labels ("salaried - private",
  "Salaried-Private "); 9 impossible ages (< 18 or > 80); 6 negative incomes.

Run:  python case_studies/13_is_ml_worth_it/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import case_paths, rng_for_case  # noqa: E402

CASE_NUMBER = 13
N = 40_000
TARGET_BAD_RATE = 0.08

OCCUPATIONS = ["Salaried-Private", "Salaried-Govt", "Self-employed-Professional", "Self-employed-Business",
               "Gig/Freelance", "Student", "Retired"]
OCC_P = [0.42, 0.12, 0.10, 0.16, 0.10, 0.05, 0.05]
OCC_EFFECT = {"Salaried-Private": 0.0, "Salaried-Govt": -0.40, "Self-employed-Professional": 0.05,
              "Self-employed-Business": 0.20, "Gig/Freelance": 0.45, "Student": 0.40, "Retired": 0.10}
STATES = ["Maharashtra", "Karnataka", "Tamil Nadu", "Delhi", "Uttar Pradesh", "Gujarat", "West Bengal",
          "Telangana", "Rajasthan", "Kerala", "Punjab", "Madhya Pradesh"]
STATE_P = np.array([14, 11, 10, 10, 11, 8, 8, 7, 6, 5, 5, 5], float)
RISKY_STATES = {"Uttar Pradesh", "Madhya Pradesh"}
CHANNELS = ["Branch", "Online-Organic", "Online-Aggregator", "DSA", "Partner-Ecom"]
CHANNEL_EFFECT = {"Branch": 0.0, "Online-Organic": -0.05, "Online-Aggregator": 0.20, "DSA": 0.35, "Partner-Ecom": 0.10}
EDU = ["Below 12th", "12th pass", "Graduate", "Postgraduate"]
TIERS = ["Tier-3", "Tier-2", "Tier-1", "Metro"]
VERIF = ["Self-declared", "Payslip", "Bank statement"]


def generate(rng: np.random.Generator) -> pd.DataFrame:
    months = pd.period_range("2023-01", "2024-12", freq="M").astype(str)
    df = pd.DataFrame({"application_id": [f"CC{5_000_000 + i}" for i in range(N)],
                       "application_month": rng.choice(months, N)})
    late = df["application_month"].str.startswith("2024").to_numpy()

    df["occupation"] = rng.choice(OCCUPATIONS, N, p=OCC_P)
    occ = df["occupation"].to_numpy()
    self_emp = np.isin(occ, ["Self-employed-Professional", "Self-employed-Business", "Gig/Freelance"])
    age = np.where(occ == "Student", rng.normal(22, 2, N), np.where(occ == "Retired", rng.normal(63, 3, N), rng.normal(34, 8, N)))
    df["age"] = np.clip(np.round(age), 18, 75).astype(int)

    tier_idx = rng.choice(4, N, p=[0.22, 0.30, 0.23, 0.25])
    df["city_tier"] = np.array(TIERS)[tier_idx]
    edu_idx = np.clip(rng.choice(4, N, p=[0.10, 0.22, 0.48, 0.20]) + (tier_idx >= 2) * (rng.random(N) < 0.2), 0, 3)
    df["education"] = np.array(EDU)[edu_idx]

    log_inc = (np.log(45_000) + 0.12 * (tier_idx - 1.5) + 0.10 * (edu_idx - 1.5) + 0.25 * (occ == "Salaried-Govt")
               - 0.6 * (occ == "Student") + rng.normal(0, 0.55, N))
    df["monthly_income"] = np.round(np.clip(np.exp(log_inc), 8_000, None), -2)
    z_inc = (log_inc - log_inc.mean()) / log_inc.std()

    no_hit = rng.random(N) < np.where(occ == "Student", 0.35, 0.05)
    score = np.clip(720 + 20 * z_inc + rng.normal(0, 55, N), 300, 900).round()
    df["bureau_score"] = np.where(no_hit, np.nan, score)
    eff_score = np.where(no_hit, 690, score)

    util = np.clip(rng.beta(2, 3.2, N) + 0.05 * late - 0.0004 * (eff_score - 720), 0, 1.2)
    util = np.where(rng.random(N) < 0.06, 0.0, util)                 # dormant cards: 0% utilisation
    df["credit_utilization"] = np.round(np.where(no_hit, np.nan, util), 3)
    eff_util = np.where(no_hit, 0.3, util)

    df["enquiries_6m"] = rng.poisson(np.exp(0.4 + 0.5 * (eff_util > 0.7) + 0.3 * self_emp))
    delinq = rng.random(N) < 0.30 * (1 / (1 + np.exp((eff_score - 690) / 40)))
    df["months_since_delinquency"] = np.where(delinq & ~no_hit, rng.integers(1, 60, N), np.nan)

    df["dti"] = np.round(np.clip(rng.beta(2.5, 6, N) - 0.05 * z_inc, 0.0, 0.9), 3)
    df["years_at_employer"] = np.round(np.clip(rng.gamma(2, 2.2, N) * (occ != "Student"), 0, 35), 1)
    df["num_credit_cards"] = np.clip(np.round(0.8 + 0.9 * z_inc + 0.006 * (eff_score - 720) + rng.normal(0, 0.8, N)), 0, 8).astype(int)
    df.loc[no_hit, "num_credit_cards"] = 0
    df["requested_limit"] = np.round(np.clip(df["monthly_income"] * np.exp(rng.normal(np.log(2.2), 0.3, N)), 20_000, None), -3)

    verif_idx = rng.choice(3, N, p=[0.25, 0.45, 0.30])
    df["income_verification"] = np.array(VERIF)[verif_idx]
    df["residence_type"] = rng.choice(["Owned", "Rented", "Family", "Company-provided"], N, p=[0.35, 0.38, 0.22, 0.05])
    chan_p = np.where(late[:, None], [0.22, 0.20, 0.30, 0.16, 0.12], [0.28, 0.22, 0.20, 0.18, 0.12])
    df["acquisition_channel"] = [rng.choice(CHANNELS, p=pp) for pp in chan_p]
    df["state"] = rng.choice(STATES, N, p=STATE_P / STATE_P.sum())
    df["marital_status"] = rng.choice(["Single", "Married", "Other"], N, p=[0.40, 0.55, 0.05])

    msd = df["months_since_delinquency"].to_numpy()
    linear = (-0.011 * (eff_score - 720) + 0.55 * no_hit
              + 2.6 * (eff_util - 0.35) ** 2 + 1.6 * np.maximum(eff_util - 0.85, 0)
              + 0.75 * (df["enquiries_6m"] > 3)
              - 0.45 * np.log(df["monthly_income"] / 45_000)
              + df["dti"] * np.where(self_emp, 2.6, 1.0)
              + 0.35 * (df["age"] < 25)
              + 0.80 * (np.nan_to_num(msd, nan=99) < 12)
              - 0.10 * edu_idx
              + np.select([verif_idx == 0, verif_idx == 2], [0.30, -0.15], 0.0)
              + df["occupation"].map(OCC_EFFECT)
              + df["acquisition_channel"].map(CHANNEL_EFFECT)
              + df["residence_type"].map({"Rented": 0.15, "Company-provided": -0.10}).fillna(0)
              + 0.25 * df["state"].isin(RISKY_STATES)
              + 0.30 * ((eff_util > 0.85) & (eff_score < 700))
              - 0.03 * df["num_credit_cards"]).to_numpy()
    lo, hi = -12.0, 4.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if (1 / (1 + np.exp(-(mid + linear)))).mean() > TARGET_BAD_RATE:
            hi = mid
        else:
            lo = mid
    p = 1 / (1 + np.exp(-(lo + linear)))
    df["bad_12m"] = (rng.random(N) < p).astype(int)
    bad = df["bad_12m"].to_numpy() == 1
    df["collections_contact_flag"] = (rng.random(N) < np.where(bad, 0.86, 0.025)).astype(int)
    return df


def inject_issues(rng: np.random.Generator, df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    idx = rng.choice(d.index, 60, replace=False)
    d.loc[idx[:30], "occupation"] = d.loc[idx[:30], "occupation"].str.lower().str.replace("-", " - ")
    d.loc[idx[30:60], "occupation"] = d.loc[idx[30:60], "occupation"] + " "
    bad_age = rng.choice(d.index, 9, replace=False)
    d.loc[bad_age, "age"] = rng.choice([3, 11, 15, 99, 120, 214], 9)
    neg = rng.choice(d.index, 6, replace=False)
    d.loc[neg, "monthly_income"] = -d.loc[neg, "monthly_income"]
    d = pd.concat([d, d.sample(25, random_state=int(rng.integers(1e9)))], ignore_index=True)
    return d.sample(frac=1, random_state=int(rng.integers(1e9))).reset_index(drop=True)


COLUMN_ORDER = ["application_id", "application_month", "age", "monthly_income", "bureau_score", "credit_utilization",
                "enquiries_6m", "months_since_delinquency", "dti", "years_at_employer", "num_credit_cards",
                "requested_limit", "education", "city_tier", "income_verification", "occupation", "residence_type",
                "acquisition_channel", "state", "marital_status", "collections_contact_flag", "bad_12m"]


def main() -> None:
    paths = case_paths(CASE_DIR)
    rng = rng_for_case(CASE_NUMBER)
    df = inject_issues(rng, generate(rng))[COLUMN_ORDER]
    df.to_csv(paths["data"] / "card_applications.csv", index=False)
    print(f"{len(df):,} rows | bad rate {df['bad_12m'].mean():.2%} | "
          f"2023 {df.loc[df.application_month < '2024', 'bad_12m'].mean():.2%} vs 2024 {df.loc[df.application_month >= '2024', 'bad_12m'].mean():.2%}")


if __name__ == "__main__":
    main()
