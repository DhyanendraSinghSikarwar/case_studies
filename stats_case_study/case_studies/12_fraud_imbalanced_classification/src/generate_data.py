"""Generate the synthetic data for Case Study 12: Card transaction fraud detection.

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business
scenario. It is not actual customer data.

Scenario
--------
A card issuer scores every transaction for fraud. Today it uses two rules (amount above
Rs 50,000, or international e-commerce). The fraud team wants a statistical model, and
needs to decide which transactions to block or send to its analysts (about 300 reviews a
day).

File: data/card_transactions.csv: 120,000 transactions over 4 months (30,000 per month),
fraud rate about 0.4%.
  txn_id, month (1-4), amount (Rs), merchant_category (nominal, 8), channel (Chip / Contactless
  / E-commerce / ATM), hour, is_international (0/1), new_merchant (0/1), new_device (0/1,
  e-commerce only), txns_last_24h, amount_vs_avg (amount / customer's 90-day average),
  card_age_months, is_fraud (0/1, TARGET)

True data-generating process (log-odds of fraud)
------------------------------------------------
logit = -6.6 + 1.1*log(amount_vs_avg) + 0.9*new_merchant + 1.3*new_device + 1.0*is_international
        + 0.18*(txns_last_24h - 3) + 1.0*[hour 0-5] - 0.25*log(card_age_months + 1)
        + channel (E-commerce +1.1, ATM +0.6, Contactless -0.3 vs Chip)
        + merchant (Electronics +0.9, Jewellery +1.0, Online gaming +1.4, Travel +0.5,
                    Grocery -0.6, Utilities -0.8, Fuel -0.2 vs Restaurants)
        + drift: in month 4, a new e-commerce gaming scheme adds +0.6 to Online gaming
Fraud is concentrated in large, unusual, new-merchant, night-time, e-commerce transactions.

Run:  python case_studies/12_fraud_imbalanced_classification/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import case_paths, rng_for_case  # noqa: E402

CASE_NUMBER = 12
N_PER_MONTH = 30_000
MERCHANTS = {"Restaurants": 0.0, "Grocery": -0.6, "Fuel": -0.2, "Utilities": -0.8, "Travel": 0.5,
             "Electronics": 0.9, "Jewellery": 1.0, "Online gaming": 1.4}
MERCHANT_P = [0.17, 0.25, 0.12, 0.10, 0.07, 0.10, 0.04, 0.15]
MERCHANT_AMT = {"Restaurants": 1_200, "Grocery": 1_500, "Fuel": 2_000, "Utilities": 2_500, "Travel": 9_000,
                "Electronics": 12_000, "Jewellery": 25_000, "Online gaming": 800}
CHANNELS = {"Chip": 0.0, "Contactless": -0.3, "E-commerce": 1.1, "ATM": 0.6}
INTERCEPT = -6.6


def make_month(rng: np.random.Generator, month: int) -> pd.DataFrame:
    n = N_PER_MONTH
    merch = rng.choice(list(MERCHANTS), n, p=MERCHANT_P)
    ecom_p = pd.Series(merch).map({"Online gaming": 0.95, "Travel": 0.6, "Electronics": 0.45, "Utilities": 0.55}).fillna(0.12).to_numpy()
    u = rng.random(n)
    channel = np.where(u < ecom_p, "E-commerce", np.where(rng.random(n) < 0.08, "ATM", np.where(rng.random(n) < 0.45, "Contactless", "Chip")))
    typical = pd.Series(merch).map(MERCHANT_AMT).to_numpy()
    ratio = np.exp(rng.normal(0, 0.7, n))                                # amount relative to the customer's usual
    amount = np.round(np.clip(typical * ratio * np.exp(rng.normal(0, 0.4, n)), 50, 400_000), -1)
    hour = rng.choice(24, n, p=np.r_[np.full(6, 0.01), np.full(18, 0.94 / 18)])
    intl = (rng.random(n) < np.where(channel == "E-commerce", 0.08, 0.02)).astype(int)
    new_merchant = (rng.random(n) < 0.15).astype(int)
    new_device = ((channel == "E-commerce") & (rng.random(n) < 0.06)).astype(int)
    txns24 = rng.poisson(3, n)
    card_age = np.clip(np.round(rng.gamma(2.0, 24, n)), 1, 240).astype(int)

    logit = (INTERCEPT + 1.1 * np.log(ratio) + 0.9 * new_merchant + 1.3 * new_device + 1.0 * intl
             + 0.18 * (txns24 - 3) + 1.0 * (hour < 6) - 0.25 * np.log(card_age + 1)
             + pd.Series(channel).map(CHANNELS).to_numpy() + pd.Series(merch).map(MERCHANTS).to_numpy())
    if month == 4:
        logit = logit + 0.6 * (merch == "Online gaming")
    p = 1 / (1 + np.exp(-logit))
    fraud = (rng.random(n) < p).astype(int)
    # Fraudsters push amounts up and transact in bursts.
    amount = np.where(fraud == 1, np.round(amount * np.exp(rng.normal(0.6, 0.4, n)), -1), amount)
    txns24 = np.where(fraud == 1, txns24 + rng.poisson(2, n), txns24)
    ratio_obs = np.round(ratio * np.where(fraud == 1, np.exp(rng.normal(0.6, 0.4, n)), 1.0), 3)
    return pd.DataFrame({"month": month, "amount": amount, "merchant_category": merch, "channel": channel, "hour": hour,
                         "is_international": intl, "new_merchant": new_merchant, "new_device": new_device,
                         "txns_last_24h": txns24, "amount_vs_avg": ratio_obs, "card_age_months": card_age,
                         "is_fraud": fraud})


def generate(rng: np.random.Generator) -> pd.DataFrame:
    df = pd.concat([make_month(rng, m) for m in range(1, 5)], ignore_index=True)
    df.insert(0, "txn_id", [f"TX12{1000000 + i}" for i in range(len(df))])
    return df


def main() -> None:
    paths = case_paths(CASE_DIR)
    df = generate(rng_for_case(CASE_NUMBER))
    df.to_csv(paths["data"] / "card_transactions.csv", index=False)
    print(df.groupby("month").is_fraud.agg(["size", "sum", "mean"]))
    print(df.groupby("channel").is_fraud.mean().round(4))
    print(df.groupby("merchant_category").is_fraud.mean().round(4))
    print("rule hits:", ((df.amount > 50_000) | ((df.is_international == 1) & (df.channel == "E-commerce"))).mean())


if __name__ == "__main__":
    main()
