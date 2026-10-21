"""Generate the synthetic data for Case Study 27 (capstone): What drives loan default, and what should Risk do?

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business scenario. It is not
actual customer data.

Scenario
--------
A lender wants to understand why some unsecured personal loans default within 12 months, and to tighten its policy.
Applications from 2022 (development) and 2023 (out-of-time test) are available, with the usual mess of real data.

Files
-----
data/loan_applications.csv: one row per loan (about 24,000 rows, including 60 duplicate rows):
  loan_id, application_date, age, monthly_income, employment_type (messy labels), years_in_job, credit_score (missing for thin
  files), dti_pct (existing monthly obligations / income), loan_amount, term_months, interest_rate, channel
  (branch / online / agent), city_tier (1-3), prior_delinquency (0, 1, 2+), utilisation_pct, defaulted_12m (0/1)
data/answer_key_teaching_only.csv: the true log-odds coefficients and each loan's true default probability.

Data-quality problems built in
------------------------------
duplicate rows; employment labels with inconsistent case and spaces; monthly income missing for about 6% (more often for agent
channel and self-employed: MAR); a few incomes with two extra zeros (typing errors); a few impossible ages; credit score missing for
about 5% (thin files, who default more).

True default model (logit)
--------------------------
-3.55 + 0.045 (dti - 25) - 0.0125 (score - 650) + 0.55 prior_delinquency + 0.9 (loan_to_annual_income - 0.8)
 + 0.012 (term - 36) + 0.45 self_employed + 0.70 gig + 0.012 (utilisation - 40) + 0.15 agent_channel + 0.30 thin_file
Interest rate, city tier, age and income have NO direct effect: the rate is priced from the score (a proxy), age and income work only through other variables.
Agent-channel customers have lower scores, so the channel looks much riskier than it is (confounding).
The agent share rises in 2023 (drift).

Run:  python case_studies/27_capstone_loan_default_drivers/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import case_paths, rng_for_case  # noqa: E402

CASE_NUMBER = 27
N_PER_YEAR = 12_000
INTERCEPT = -3.55


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def year_frame(rng, year, agent_shift):
    n = N_PER_YEAR
    d = rng.normal(0, 1, n)
    age = np.clip(np.round(rng.normal(37, 10, n)), 21, 65)
    emp = rng.choice(["salaried", "self_employed", "gig"], n, p=[0.68, 0.22, 0.10])
    income = np.exp(10.55 + 0.012 * (age - 37) + 0.25 * (emp == "salaried") + 0.55 * rng.normal(0, 1, n) + 0.10 * d)
    income = np.round(income, -2)
    years_job = np.clip(np.round((age - 21) * rng.uniform(0.2, 0.8, n), 1), 0, 40)
    score = np.clip(np.round(650 + 35 * d + 22 * (np.log(income) - 10.6) + 0.8 * (age - 37) + rng.normal(0, 38, n)), 300, 900)
    dti = np.clip(25 + 8 * rng.normal(0, 1, n) - 5 * d, 2, 80)
    lti = rng.uniform(0.15, 1.6, n) * (1 + 0.1 * rng.normal(0, 1, n))
    lti = np.clip(lti, 0.1, 2.5)
    loan = np.round(lti * 12 * income, -3)
    term = rng.choice([12, 24, 36, 48, 60], n, p=[0.10, 0.22, 0.34, 0.20, 0.14])
    rate = np.clip(9.5 + (700 - score) / 40 + 0.02 * (term - 36) + rng.normal(0, 0.8, n), 8, 30)
    p_agent = sigmoid(-1.35 + agent_shift - 0.012 * (score - 650))
    u = rng.random(n)
    channel = np.where(u < p_agent, "agent", np.where(rng.random(n) < 0.55, "online", "branch"))
    tier = rng.choice([1, 2, 3], n, p=[0.40, 0.35, 0.25])
    prior = np.where(rng.random(n) < sigmoid(-1.9 - 0.9 * d), np.where(rng.random(n) < 0.3, 2, 1), 0)
    util = np.clip(40 - 10 * d + 15 * rng.normal(0, 1, n), 0, 100)
    thin = rng.random(n) < 0.05
    dates = pd.Timestamp(f"{year}-01-01") + pd.to_timedelta(rng.integers(0, 365, n), unit="D")
    return pd.DataFrame({"application_date": dates, "age": age, "monthly_income": income, "employment_type": emp, "years_in_job": years_job, "credit_score": score,
                         "dti_pct": np.round(dti, 1), "loan_amount": loan, "term_months": term, "interest_rate": np.round(rate, 2), "channel": channel, "city_tier": tier,
                         "prior_delinquency": prior, "utilisation_pct": np.round(util, 1), "thin": thin, "lti": lti})


def logit(df):
    return (INTERCEPT + 0.045 * (df.dti_pct - 25) - 0.0125 * (df.credit_score.fillna(650) - 650) + 0.55 * df.prior_delinquency + 0.9 * (df.lti - 0.8)
            + 0.012 * (df.term_months - 36) + 0.45 * (df.employment_type == "self_employed") + 0.70 * (df.employment_type == "gig")
            + 0.012 * (df.utilisation_pct - 40) + 0.15 * (df.channel == "agent") + 0.30 * df.thin)


def generate(rng):
    df = pd.concat([year_frame(rng, 2022, 0.0), year_frame(rng, 2023, 0.45)], ignore_index=True)
    df["true_p"] = sigmoid(logit(df))
    df["defaulted_12m"] = (rng.random(len(df)) < df["true_p"]).astype(int)
    df.insert(0, "loan_id", [f"LN27{100000 + i}" for i in range(len(df))])
    # thin files: no score
    df.loc[df.thin, "credit_score"] = np.nan
    # missing income (MAR: more likely for agent channel and self-employed)
    pm = sigmoid(-3.3 + 1.0 * (df.channel == "agent") + 0.8 * (df.employment_type == "self_employed"))
    df.loc[rng.random(len(df)) < pm, "monthly_income"] = np.nan
    # typos and impossible values
    idx = rng.choice(df.index[df.monthly_income.notna()], 25, replace=False); df.loc[idx, "monthly_income"] *= 100
    idx = rng.choice(df.index, 3, replace=False); df.loc[idx, "age"] = [5, 150, 0]
    # messy labels
    lab = df.employment_type.map({"salaried": "Salaried", "self_employed": "Self-employed", "gig": "Gig"})
    messy = rng.random(len(df)) < 0.10
    df["employment_type"] = np.where(messy, np.where(rng.random(len(df)) < 0.5, lab.str.upper(), lab.str.lower() + " "), lab)
    key = df[["loan_id", "true_p"]].copy()
    out = df.drop(columns=["thin", "lti", "true_p"])
    out["prior_delinquency"] = out["prior_delinquency"].map({0: "0", 1: "1", 2: "2+"})
    out["application_date"] = out["application_date"].dt.strftime("%Y-%m-%d")
    out = pd.concat([out, out.sample(60, random_state=1)], ignore_index=True)       # duplicates
    return out, key


def main() -> None:
    paths = case_paths(CASE_DIR)
    out, key = generate(rng_for_case(CASE_NUMBER))
    out.to_csv(paths["data"] / "loan_applications.csv", index=False)
    coefs = pd.DataFrame({"term": ["intercept", "dti_pct", "credit_score", "prior_delinquency", "loan_to_annual_income", "term_months", "self_employed", "gig", "utilisation_pct", "agent_channel", "thin_file"],
                          "true_logit_coefficient": [INTERCEPT, 0.045, -0.0125, 0.55, 0.9, 0.012, 0.45, 0.70, 0.012, 0.15, 0.30]})
    coefs.to_csv(paths["data"] / "answer_key_coefficients.csv", index=False)
    key.to_csv(paths["data"] / "answer_key_teaching_only.csv", index=False)
    print(len(out), "rows; default rate by year:", out.assign(y=out.application_date.str[:4]).groupby("y").defaulted_12m.mean().round(4).to_dict(),
          "agent share by year:", out.assign(y=out.application_date.str[:4]).groupby("y").channel.apply(lambda s: (s == "agent").mean()).round(3).to_dict())


if __name__ == "__main__":
    main()
