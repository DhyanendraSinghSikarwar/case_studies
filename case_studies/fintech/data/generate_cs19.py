"""
SYNTHETIC DATA GENERATOR - CASE STUDY 19 (Credgenics-style propensity-to-pay vs uplift for collections)
======================================================================================================
THIS DATA IS SYNTHETIC. Collections-platform data is confidential.

80,000 delinquent retail accounts (30-90 DPD) from three lender portfolios, observed in a randomised
channel experiment: each account was assigned at random (25% each) to
    SMS only (control) | voice bot | tele-caller | field visit
Outcome: resolved within 30 days (paid at least the overdue EMI) and Rs recovered.
Built-in truth: a large share of payers are "sure things" who pay with SMS alone; channel effects are
heterogeneous (bots work on forgetful but contactable customers, tele-callers on medium-risk contactable
customers, field visits on hard-to-reach large balances). This is what makes uplift differ from propensity.

Calibration anchors (reference file, Case Study 19): ~11 million accounts on platform; named methods
propensity-to-pay, resolution likelihood, segmentation, ML intent-to-pay for agent allocation, voice bots;
vendor-claimed impact "+20% resolution, +25% collections, -40% cost". Effect sizes are our assumptions
(decision.md D-19-02).

Output: data/cs19/collections_experiment.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.special import expit

SEED = 42
N = 80_000
ARMS = ["SMS only", "Voice bot", "Tele-caller", "Field visit"]


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    product = rng.choice(["Personal loan", "BNPL", "Credit card"], N, p=[0.45, 0.30, 0.25])
    dpd = rng.integers(30, 90, N)
    outstanding = np.round(np.exp(rng.normal(np.select([product == "Personal loan", product == "BNPL"], [np.log(60_000), np.log(8_000)], np.log(35_000)), 0.7, N)), -2)
    overdue = np.round(outstanding * np.clip(rng.normal(0.12, 0.04, N), 0.03, 0.4) * (dpd / 30), -1)
    paid_ratio_6m = np.round(rng.beta(4, 2, N), 3)                          # share of past 6 EMIs paid on time
    broken_ptp = rng.poisson(0.6, N)                                         # broken promises-to-pay
    contactability = np.round(rng.beta(3, 2, N), 3)                          # historical answer rate
    language = rng.choice(["Hindi", "English", "Tamil", "Telugu", "Marathi", "Bengali", "Kannada"], N, p=[0.38, 0.22, 0.09, 0.09, 0.08, 0.08, 0.06])
    tier = rng.choice(["Tier 1", "Tier 2", "Tier 3"], N, p=[0.40, 0.35, 0.25])
    age = np.clip(np.round(rng.normal(33, 8, N)), 21, 65)
    income_band = rng.choice(["<3L", "3-6L", "6-12L", ">12L"], N, p=[0.25, 0.40, 0.25, 0.10])
    forgetful = rng.random(N) < expit(-0.5 + 2.0 * paid_ratio_6m - 0.5 * broken_ptp)    # latent: would pay if reminded
    # baseline (SMS-only) propensity: "sure things" and self-cure
    z0 = -1.6 + 2.6 * paid_ratio_6m - 0.35 * broken_ptp - 0.015 * (dpd - 30) + 0.25 * (income_band == ">12L") - 0.2 * (tier == "Tier 3")
    p0 = expit(z0)
    # heterogeneous channel uplifts on the log-odds scale
    up = {
        "SMS only": np.zeros(N),
        "Voice bot": 0.55 * forgetful * contactability - 0.05,
        "Tele-caller": (0.9 * contactability) * (1 - np.abs(paid_ratio_6m - 0.55) * 1.4) + 0.1 * broken_ptp * contactability,
        "Field visit": 0.4 + 0.9 * (1 - contactability) + 0.25 * np.log(outstanding / 30_000) - 0.4 * (product == "BNPL"),
    }
    arm = rng.choice(ARMS, N)
    z = z0 + np.select([arm == a for a in ARMS], [up[a] for a in ARMS])
    resolved = (rng.random(N) < expit(z)).astype(int)
    rec_share = np.where(resolved == 1, np.clip(rng.beta(6, 2, N) + 0.1 * (arm == "Field visit"), 0, 1), np.clip(rng.beta(1, 12, N), 0, 1))
    recovered = np.round(overdue * rec_share, 0)
    df = pd.DataFrame({
        "account_id": [f"D{i:07d}" for i in range(1, N + 1)], "lender_portfolio": product, "dpd": dpd,
        "outstanding_inr": outstanding, "overdue_inr": overdue, "paid_ratio_6m": paid_ratio_6m, "broken_ptp_count": broken_ptp,
        "contactability": contactability, "preferred_language": language, "city_tier": tier, "age": age, "income_band": income_band,
        "assigned_channel": arm, "resolved_30d": resolved, "amount_recovered_inr": recovered,
        "experiment_month": rng.choice(["2025-07", "2025-08", "2025-09"], N),
    })
    # hidden truth for evaluation (simulation only): resolution probability under every channel
    for a, short in zip(ARMS, ["sms", "bot", "tele", "field"]):
        df[f"_p_{short}"] = np.round(expit(z0 + up[a]), 4)
    # data-quality issues
    df.loc[df.sample(n=400, random_state=seed).index, "contactability"] = np.nan          # new accounts, no call history
    df.loc[df.sample(n=30, random_state=seed + 1).index, "amount_recovered_inr"] = -df.loc[df.sample(n=30, random_state=seed + 1).index, "overdue_inr"]  # sign error
    field_lost = df[(df.assigned_channel == "Field visit")].sample(frac=0.03, random_state=seed + 2).index
    df = df.drop(field_lost)                                                                 # field app sync failures -> SRM
    return df.reset_index(drop=True)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs19"), exist_ok=True)
    d = generate(); d.to_csv(os.path.join(here, "cs19", "collections_experiment.csv.gz"), index=False)
    print(len(d), d.groupby("assigned_channel").resolved_30d.mean().round(3).to_dict())
