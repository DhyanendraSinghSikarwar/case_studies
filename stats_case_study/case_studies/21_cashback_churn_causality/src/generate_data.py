"""Generate the synthetic data for Case Study 21: Does cashback reduce churn?

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business scenario. It is not
actual customer data.

Scenario
--------
A credit-card issuer offers a cashback programme that customers must opt into. Customers enrolled in it churn far
less. Marketing wants to move more budget into cashback. Separately, a small randomised pilot offered cashback to a
random half of 16,000 customers.

Files
-----
data/observational_customers.csv: 20,000 customers who could opt in during the year (self-selected enrolment).
  customer_id, tenure_months, income_band (1-4), digital_logins_per_month, spend_3m_before (Rs thousand),
  spend_trend_before (change in monthly spend over the 3 months before the enrolment decision, %), complaints_12m,
  enrolled (0/1), spend_3m_after (Rs thousand, measured AFTER enrolment), churned_12m (0/1, outcome)
data/pilot_experiment.csv: 16,000 customers from the same population. A random half were offered cashback
  (offered = 1). Control customers could not enrol.
  customer_id, tenure_months, income_band, digital_logins_per_month, spend_3m_before, spend_trend_before,
  complaints_12m, offered (0/1, RANDOMISED), enrolled (0/1; only possible if offered), churned_12m
data/answer_key_teaching_only.csv: true causal effect of cashback on churn probability (NOT available in real life).

True data-generating process
----------------------------
Latent "engagement" E ~ N(0, 1), unobserved. It raises opt-in, spending and digital logins and LOWERS churn.
  spend_3m_before = exp(2.3 + 0.35*E + 0.25*(income band-1)/1.5 + Normal(0, 0.45))
  digital logins = Poisson(exp(1.7 + 0.30*E));  spend trend before = 4*E - 3*churn_intent... (see code)
  logit P(churn | no cashback) = -1.55 - 0.85*E - 0.006*tenure + 0.30*complaints + 0.15*(income band 1)
  cashback lowers the churn log-odds by 0.55 for everyone (true average effect about -6 percentage points).
  P(opt in) depends on spend, tenure, digital logins, E (hidden) and the customer's churn intention
  (customers about to leave do not enrol): selection into treatment.
  spend_3m_after = spend_3m_before * exp(0.12*enrolled + noise): cashback raises spending, which is part of how it
  works (a MEDIATOR, not a confounder).

Run:  python case_studies/21_cashback_churn_causality/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import case_paths, rng_for_case  # noqa: E402

CASE_NUMBER = 21
N_OBS, N_PILOT = 20_000, 16_000
EFFECT = -0.55        # effect of cashback on the churn log-odds


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def population(rng: np.random.Generator, n: int) -> pd.DataFrame:
    e = rng.normal(0, 1, n)
    tenure = np.clip(np.round(rng.gamma(2.2, 18, n) + 1 + 6 * e), 1, 180).astype(int)
    income = np.clip(np.round(2.5 + 0.35 * rng.normal(0, 1, n) * 2 + 0.2 * e), 1, 4).astype(int)
    spend = np.round(np.exp(2.3 + 0.35 * e + 0.25 * (income - 1) / 1.5 + rng.normal(0, 0.45, n)), 1)
    logins = rng.poisson(np.exp(1.7 + 0.30 * e))
    comp = rng.choice([0, 1, 2], n, p=[0.82, 0.13, 0.05])
    lp0 = -1.55 - 0.85 * e - 0.006 * tenure + 0.30 * comp + 0.15 * (income == 1)
    p0 = sigmoid(lp0)
    p1 = sigmoid(lp0 + EFFECT)
    return pd.DataFrame({"E": e, "tenure_months": tenure, "income_band": income, "digital_logins_per_month": logins, "spend_3m_before": spend,
                         "complaints_12m": comp, "lp0": lp0, "p0": p0, "p1": p1})


def generate(rng: np.random.Generator):
    # --- observational: self-selected enrolment
    o = population(rng, N_OBS)
    churn_intent = rng.normal(0, 1, N_OBS) + 1.2 * (o["lp0"] - o["lp0"].mean()) / o["lp0"].std()       # latent propensity to leave
    o["spend_trend_before"] = np.round(4 * o["E"] - 4.5 * (churn_intent - churn_intent.mean()) + rng.normal(0, 6, N_OBS), 1)
    z = (-1.55 + 0.9 * (np.log(o["spend_3m_before"]) - 2.3) + 0.012 * o["tenure_months"] + 0.18 * o["digital_logins_per_month"]
         + 0.85 * o["E"] - 0.45 * (churn_intent - churn_intent.mean()) - 0.2 * o["complaints_12m"])
    o["enrolled"] = (rng.random(N_OBS) < sigmoid(z)).astype(int)
    p_churn = np.where(o["enrolled"] == 1, o["p1"], o["p0"])
    o["churned_12m"] = (rng.random(N_OBS) < p_churn).astype(int)
    o["spend_3m_after"] = np.round(o["spend_3m_before"] * np.exp(0.12 * o["enrolled"] + rng.normal(0, 0.15, N_OBS)), 1)
    o.insert(0, "customer_id", [f"CB21{100000 + i}" for i in range(N_OBS)])

    # --- randomised pilot
    p = population(rng, N_PILOT)
    churn_intent_p = rng.normal(0, 1, N_PILOT) + 1.2 * (p["lp0"] - p["lp0"].mean()) / p["lp0"].std()
    p["spend_trend_before"] = np.round(4 * p["E"] - 4.5 * (churn_intent_p - churn_intent_p.mean()) + rng.normal(0, 6, N_PILOT), 1)
    p["offered"] = rng.permutation(np.r_[np.ones(N_PILOT // 2, int), np.zeros(N_PILOT - N_PILOT // 2, int)])
    zp = (-1.20 + 0.9 * (np.log(p["spend_3m_before"]) - 2.3) + 0.012 * p["tenure_months"] + 0.18 * p["digital_logins_per_month"]
          + 0.85 * p["E"] - 0.45 * (churn_intent_p - churn_intent_p.mean()) - 0.2 * p["complaints_12m"])
    take = rng.random(N_PILOT) < sigmoid(zp)
    p["enrolled"] = ((p["offered"] == 1) & take).astype(int)
    p["churned_12m"] = (rng.random(N_PILOT) < np.where(p["enrolled"] == 1, p["p1"], p["p0"])).astype(int)
    p.insert(0, "customer_id", [f"CB21P{100000 + i}" for i in range(N_PILOT)])

    cols_o = ["customer_id", "tenure_months", "income_band", "digital_logins_per_month", "spend_3m_before", "spend_trend_before",
              "complaints_12m", "enrolled", "spend_3m_after", "churned_12m"]
    cols_p = ["customer_id", "tenure_months", "income_band", "digital_logins_per_month", "spend_3m_before", "spend_trend_before",
              "complaints_12m", "offered", "enrolled", "churned_12m"]
    key = pd.concat([o[["customer_id", "p0", "p1"]], p[["customer_id", "p0", "p1"]]], ignore_index=True)
    key["true_effect_pp"] = 100 * (key["p1"] - key["p0"])
    return o[cols_o], p[cols_p], key


def main() -> None:
    paths = case_paths(CASE_DIR)
    o, p, key = generate(rng_for_case(CASE_NUMBER))
    o.to_csv(paths["data"] / "observational_customers.csv", index=False)
    p.to_csv(paths["data"] / "pilot_experiment.csv", index=False)
    key.to_csv(paths["data"] / "answer_key_teaching_only.csv", index=False)
    print("obs: enrolled share", o.enrolled.mean().round(3), "churn by enrolled:", o.groupby("enrolled").churned_12m.mean().round(4).to_dict())
    print("pilot: take-up among offered", p.loc[p.offered == 1, "enrolled"].mean().round(3), "churn by offered:", p.groupby("offered").churned_12m.mean().round(4).to_dict())
    print("true mean effect (pp):", key.true_effect_pp.mean().round(3))


if __name__ == "__main__":
    main()
