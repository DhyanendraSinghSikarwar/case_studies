"""Generate the synthetic data for Case Study 03: Did the email campaign increase conversions?

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business
scenario. It is not actual customer data.

Scenario
--------
A bank's Marketing team emailed a pre-approved personal-loan offer to existing
customers. Before sending, the CRM system randomly held out 15% of eligible
customers (no email) as a control group. Conversion = took a personal loan
within 30 days of the send date.

Two files are produced:

1. data/campaign_results.csv: 80,000 eligible customers, one row each.
   customer_id     ID
   group           "email" (85%) or "holdout" (15%), assigned at random
   segment         Mass (85%) / Affluent (15%)
   tenure_years    years with the bank (Gamma-distributed, 0.2-25)
   digital_active  1 if the customer logged into mobile banking last month
   email_opened    1/0 for the email group; blank for holdout (no email sent)
   converted       1 if a personal loan was disbursed within 30 days

   Hidden mechanism (not in the data): every customer has a latent
   "engagement" level. Engaged customers are more likely to (a) open emails
   AND (b) take a loan anyway. So openers convert much more than non-openers
   EVEN WITHOUT the email. The email itself adds a modest uplift, only for
   customers who open it. Baseline conversion is ~1.8%; the true average
   uplift across the whole email group is ~+0.41 percentage points (relative
   lift ~+23%). With a 15% holdout of 80,000 customers the design has ~86%
   power to detect this at alpha = 5% (two-sided), so roughly 1 run in 7 of
   this design would NOT reach significance even though the effect is real.

2. data/premium_rm_pilot.csv: a small pilot in which 360 Affluent customers
   were randomised 50/50 to receive a relationship-manager (RM) call or not.
   arm             "rm_call" / "no_call"
   converted       1/0
   True conversion: 5.5% with a call vs 1.5% without (small samples -> exact test).

Run:  python case_studies/03_email_campaign_conversion/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import SEED, case_paths  # noqa: E402

CASE_NUMBER = 3
N_CUSTOMERS = 80_000
HOLDOUT_SHARE = 0.15
# Random-stream choice (documented for transparency): ten candidate streams were
# generated and the one whose realised email-vs-holdout lift was closest to the
# TRUE design lift (+0.41 pp) was kept (stream 1: realised +0.42 pp). Across the ten
# streams the realised lift ranged from +0.10 to +0.52 pp. That is ordinary sampling
# variation, which the notebook discusses. The choice targets a *typical*
# sample, not a significant one; Case 22 deals with unlucky draws.
STREAM = 1


def logistic(x):
    return 1 / (1 + np.exp(-x))


def generate_campaign(rng: np.random.Generator) -> pd.DataFrame:
    n = N_CUSTOMERS
    df = pd.DataFrame({
        "customer_id": [f"C{3000000 + i}" for i in range(n)],
        "group": np.where(rng.random(n) < HOLDOUT_SHARE, "holdout", "email"),
        "segment": rng.choice(["Mass", "Affluent"], n, p=[0.85, 0.15]),
    })
    df["tenure_years"] = np.round(np.clip(rng.gamma(2.0, 3.0, n), 0.2, 25), 1)
    engagement = rng.normal(0, 1, n)                          # latent, never observed
    df["digital_active"] = (rng.random(n) < logistic(0.3 + 1.0 * engagement)).astype(int)

    affluent = df["segment"].eq("Affluent").to_numpy()
    base_logit = -4.12 + 0.65 * engagement + 0.25 * affluent - 0.02 * df["tenure_years"]
    p_open = logistic(-0.9 + 1.3 * engagement)
    is_email = df["group"].eq("email").to_numpy()
    opened = is_email & (rng.random(n) < p_open)
    # The email raises conversion odds only for customers who open it.
    logit = base_logit + 0.40 * opened
    df["email_opened"] = np.where(is_email, opened.astype(int), np.nan)
    df["converted"] = (rng.random(n) < logistic(logit)).astype(int)
    return df


def generate_pilot(rng: np.random.Generator) -> pd.DataFrame:
    n_arm = 180
    arm = np.repeat(["rm_call", "no_call"], n_arm)
    p = np.where(arm == "rm_call", 0.055, 0.015)
    return pd.DataFrame({
        "customer_id": [f"A{900000 + i}" for i in range(2 * n_arm)],
        "arm": arm,
        "converted": (rng.random(2 * n_arm) < p).astype(int),
    }).sample(frac=1, random_state=int(rng.integers(1e9))).reset_index(drop=True)


def main() -> None:
    paths = case_paths(CASE_DIR)
    rng = np.random.default_rng(SEED + CASE_NUMBER + 1000 * STREAM)
    camp = generate_campaign(rng)
    pilot = generate_pilot(rng)
    camp.to_csv(paths["data"] / "campaign_results.csv", index=False)
    pilot.to_csv(paths["data"] / "premium_rm_pilot.csv", index=False)
    print(camp.groupby("group")["converted"].agg(["size", "sum", "mean"]))
    print(camp[camp.group == "email"].groupby("email_opened")["converted"].agg(["size", "mean"]))
    print(pilot.groupby("arm")["converted"].agg(["size", "sum", "mean"]))


if __name__ == "__main__":
    main()
