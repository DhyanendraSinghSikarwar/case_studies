"""Generate the synthetic data for Case Study 24: A fraud alert fired: how worried should we be? (Bayes and base rates)

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business scenario. It is not
actual customer data.

Scenario
--------
A bank's fraud team runs two independent screens on card and UPI transactions: a rule engine (alert A) and a
machine-learning score (alert B). Every transaction later receives a confirmed outcome (fraud or genuine, from
chargebacks and customer confirmation after 60 days). The operations head says "the rule catches 85% of fraud, so
when it fires the transaction is probably fraud". Analysts also have a table of small merchant groups where a few
frauds have been seen, and need rates for them.

Files
-----
data/transactions.csv: 150,000 transactions.
  txn_id, channel (Card present / Card not present / UPI), alert_rule (0/1), alert_ml (0/1), confirmed_fraud (0/1)
data/merchant_groups.csv: 14 small merchant groups with transactions and confirmed frauds.
  group, transactions, frauds
data/answer_key_teaching_only.csv: the true fraud rate of each merchant group (NOT available in real life).

True data-generating process
----------------------------
Fraud prevalence by channel: Card present 0.15%, Card not present 1.0%, UPI 0.35% (channel shares 55/30/15%).
Rule engine: catches 85% of fraud; false-alarm rate 2% (card present), 4% (card not present), 2.5% (UPI).
ML score: catches 80% of fraud; false-alarm rate 2% in every channel.
Given the true status and the channel the two screens fire independently.
Merchant groups: true rates drawn from Beta(2, 400) (mean 0.5%), 150 to 2,500 transactions each.

Run:  python case_studies/24_bayes_fraud_alert/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import case_paths, rng_for_case  # noqa: E402

CASE_NUMBER = 24
CHANNELS = ["Card present", "Card not present", "UPI"]
SHARE = [0.55, 0.30, 0.15]
PREV = {"Card present": 0.0015, "Card not present": 0.010, "UPI": 0.0035}
RULE_FPR = {"Card present": 0.02, "Card not present": 0.04, "UPI": 0.025}


def main() -> None:
    paths = case_paths(CASE_DIR)
    rng = rng_for_case(CASE_NUMBER)
    n = 150_000
    channel = rng.choice(CHANNELS, n, p=SHARE)
    fraud = (rng.random(n) < pd.Series(channel).map(PREV).to_numpy()).astype(int)
    rule_p = np.where(fraud == 1, 0.85, pd.Series(channel).map(RULE_FPR).to_numpy())
    ml_p = np.where(fraud == 1, 0.80, 0.02)
    df = pd.DataFrame({"txn_id": [f"TX24{1000000 + i}" for i in range(n)], "channel": channel,
                       "alert_rule": (rng.random(n) < rule_p).astype(int), "alert_ml": (rng.random(n) < ml_p).astype(int),
                       "confirmed_fraud": fraud})
    df.to_csv(paths["data"] / "transactions.csv", index=False)

    k = 14
    true_rate = rng.beta(2, 400, k)
    size = rng.integers(150, 2_500, k)
    frauds = rng.binomial(size, true_rate)
    names = [f"Merchant group {chr(65 + i)}" for i in range(k)]
    pd.DataFrame({"group": names, "transactions": size, "frauds": frauds}).to_csv(paths["data"] / "merchant_groups.csv", index=False)
    pd.DataFrame({"group": names, "true_fraud_rate": true_rate}).to_csv(paths["data"] / "answer_key_teaching_only.csv", index=False)

    print(df.groupby("channel")["confirmed_fraud"].agg(["size", "mean"]))
    print("rule alert rate", df.alert_rule.mean().round(4), "| P(fraud | rule alert)", df.loc[df.alert_rule == 1, "confirmed_fraud"].mean().round(4))
    print("both alerts:", int(((df.alert_rule == 1) & (df.alert_ml == 1)).sum()), "P(fraud | both)", df.loc[(df.alert_rule == 1) & (df.alert_ml == 1), "confirmed_fraud"].mean().round(4))
    print(pd.DataFrame({"size": size, "frauds": frauds, "true": true_rate.round(4)}, index=names))


if __name__ == "__main__":
    main()
