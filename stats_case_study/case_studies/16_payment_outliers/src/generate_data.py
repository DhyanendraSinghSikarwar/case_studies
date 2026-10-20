"""Generate the synthetic data for Case Study 16: Payment processing outliers: error, fraud, VIP or rare event?

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business
scenario. It is not actual customer data.

Scenario
--------
A payments processor's monitoring dashboard flags every transaction more than 3 standard deviations
above the mean. Dozens are flagged each quarter, most are the wrong ones, and the ops team has stopped
looking. Risk wants a defensible outlier policy: which unusual payments are data errors, which are
fraud, which are legitimate high-value (VIP) customers, and which are rare-but-real events such as
festival shopping?

Files
-----
data/payments.csv: 20,230 payments over one quarter.
  txn_id, merchant_segment (7), payment_method (UPI / Card / NetBanking / Wallet),
  entry_channel (Online / POS chip / Manual keyed), hour, is_festival_week (0/1),
  customer_tier (Standard / Affluent / Privileged), customer_tenure_months,
  customer_avg_amount_90d (Rs), new_device (0/1), geo_mismatch (0/1), txns_last_24h, amount (Rs)
data/answer_key_teaching_only.csv: txn_id, true_type (normal / entry_error / fraud / vip / festival).
  NOT available in real life. Used only at the end to check how well each rule did.

True data-generating process
----------------------------
Normal payments: log-normal amounts around a segment-specific typical value, times a customer
"spending level". 20,000 transactions.
  entry_error (40): amount keyed 100x too large (a decimal slip), always Manual keyed, usually a
      regular customer on a known device whose amount is wildly out of line.
  fraud (60): new device, geo mismatch, bursts of transactions, night time, amounts 3-8x the
      customer's own average; card or wallet; Online channel.
  vip (50): customers with long tenure in the Privileged tier; high amounts that are in line with
      their own history; known device; ordinary hours.
  festival (80): in festival week, regular customers buy jewellery or electronics at 3-5x their
      usual amount; known device; ordinary hours.

Run:  python case_studies/16_payment_outliers/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import case_paths, rng_for_case  # noqa: E402

CASE_NUMBER = 16
SEGMENTS = {"Grocery": (450, 0.24), "Restaurant": (900, 0.16), "Fuel": (1_500, 0.15), "Utilities": (1_800, 0.10),
            "Electronics": (9_000, 0.12), "Jewellery": (40_000, 0.04), "B2B wholesale": (25_000, 0.19)}
N_NORMAL, N_ERR, N_FRAUD, N_VIP, N_FEST = 20_000, 40, 60, 50, 80


def customer_block(rng: np.random.Generator, n: int, vip: bool = False) -> pd.DataFrame:
    if vip:
        tier = np.full(n, "Privileged")
        tenure = rng.integers(72, 240, n)
        level = np.exp(rng.normal(np.log(6.0), 0.35, n))
    else:
        tier = rng.choice(["Standard", "Affluent", "Privileged"], n, p=[0.74, 0.22, 0.04])
        tenure = np.clip(np.round(rng.gamma(2.2, 22, n)), 1, 240).astype(int)
        level = np.exp(rng.normal(0, 0.45, n)) * pd.Series(tier).map({"Standard": 1.0, "Affluent": 1.7, "Privileged": 3.2}).to_numpy()
    return pd.DataFrame({"customer_tier": tier, "customer_tenure_months": tenure, "level": level})


def generate(rng: np.random.Generator) -> tuple[pd.DataFrame, pd.DataFrame]:
    seg_names = list(SEGMENTS)
    seg_p = np.array([SEGMENTS[s][1] for s in seg_names]); seg_p = seg_p / seg_p.sum()

    def base(n: int, segs=None, vip=False):
        c = customer_block(rng, n, vip)
        seg = rng.choice(seg_names, n, p=seg_p) if segs is None else rng.choice(segs, n)
        typical = pd.Series(seg).map({k: v[0] for k, v in SEGMENTS.items()}).to_numpy()
        c["merchant_segment"] = seg
        # The customer's own 90-day average payment (known before the transaction).
        c["customer_avg_amount_90d"] = np.round(typical * c["level"] * np.exp(rng.normal(0, 0.10, n)), 0)
        c["_typical"] = typical
        return c

    # ---- normal
    nrm = base(N_NORMAL)
    nrm["amount"] = np.round(nrm["customer_avg_amount_90d"] * np.exp(rng.normal(0, 0.55, N_NORMAL)), 0)
    nrm["payment_method"] = rng.choice(["UPI", "Card", "NetBanking", "Wallet"], N_NORMAL, p=[0.52, 0.30, 0.08, 0.10])
    nrm["entry_channel"] = np.where(nrm["payment_method"] == "Card", rng.choice(["POS chip", "Online"], N_NORMAL, p=[0.7, 0.3]),
                                    np.where(rng.random(N_NORMAL) < 0.02, "Manual keyed", "Online"))
    nrm["hour"] = rng.choice(24, N_NORMAL, p=np.r_[np.full(6, 0.012), np.full(18, (1 - 0.072) / 18)])
    nrm["is_festival_week"] = (rng.random(N_NORMAL) < 0.08).astype(int)
    nrm["new_device"] = (rng.random(N_NORMAL) < 0.04).astype(int)
    nrm["geo_mismatch"] = (rng.random(N_NORMAL) < 0.015).astype(int)
    nrm["txns_last_24h"] = rng.poisson(1.6, N_NORMAL)
    nrm["true_type"] = "normal"

    # ---- entry errors (decimal slip, manual keyed)
    err = base(N_ERR)
    err["amount"] = np.round(err["customer_avg_amount_90d"] * np.exp(rng.normal(0, 0.4, N_ERR)), 0) * 100
    err["payment_method"] = rng.choice(["UPI", "Card", "NetBanking"], N_ERR)
    err["entry_channel"] = "Manual keyed"
    err["hour"] = rng.choice(np.arange(9, 19), N_ERR)
    err["is_festival_week"] = 0
    err["new_device"] = 0; err["geo_mismatch"] = 0; err["txns_last_24h"] = rng.poisson(1.2, N_ERR)
    err["true_type"] = "entry_error"

    # ---- fraud
    fr = base(N_FRAUD)
    fr["amount"] = np.round(fr["customer_avg_amount_90d"] * rng.uniform(3, 8, N_FRAUD), 0)
    fr["payment_method"] = rng.choice(["Card", "Wallet"], N_FRAUD, p=[0.7, 0.3])
    fr["entry_channel"] = "Online"
    fr["hour"] = rng.choice(np.r_[np.arange(0, 6), np.arange(22, 24)], N_FRAUD)
    fr["is_festival_week"] = (rng.random(N_FRAUD) < 0.1).astype(int)
    fr["new_device"] = (rng.random(N_FRAUD) < 0.9).astype(int)
    fr["geo_mismatch"] = (rng.random(N_FRAUD) < 0.75).astype(int)
    fr["txns_last_24h"] = 4 + rng.poisson(3, N_FRAUD)
    fr["true_type"] = "fraud"

    # ---- VIP
    vp = base(N_VIP, segs=["Jewellery", "Electronics", "B2B wholesale"], vip=True)
    vp["amount"] = np.round(vp["customer_avg_amount_90d"] * np.exp(rng.normal(0.05, 0.3, N_VIP)), 0)
    vp["payment_method"] = rng.choice(["Card", "NetBanking", "UPI"], N_VIP, p=[0.5, 0.3, 0.2])
    vp["entry_channel"] = np.where(vp["payment_method"] == "Card", "POS chip", "Online")
    vp["hour"] = rng.choice(np.arange(9, 21), N_VIP)
    vp["is_festival_week"] = (rng.random(N_VIP) < 0.1).astype(int)
    vp["new_device"] = 0; vp["geo_mismatch"] = 0; vp["txns_last_24h"] = rng.poisson(1.2, N_VIP)
    vp["true_type"] = "vip"

    # ---- festival
    fs = base(N_FEST, segs=["Jewellery", "Electronics"])
    fs["amount"] = np.round(fs["customer_avg_amount_90d"] * rng.uniform(3, 5, N_FEST), 0)
    fs["payment_method"] = rng.choice(["Card", "UPI", "NetBanking"], N_FEST, p=[0.55, 0.3, 0.15])
    fs["entry_channel"] = np.where(fs["payment_method"] == "Card", rng.choice(["POS chip", "Online"], N_FEST), "Online")
    fs["hour"] = rng.choice(np.arange(10, 21), N_FEST)
    fs["is_festival_week"] = 1
    fs["new_device"] = 0; fs["geo_mismatch"] = 0; fs["txns_last_24h"] = rng.poisson(1.6, N_FEST)
    fs["true_type"] = "festival"

    df = pd.concat([nrm, err, fr, vp, fs], ignore_index=True)
    df = df.sample(frac=1, random_state=int(rng.integers(1e9))).reset_index(drop=True)
    df.insert(0, "txn_id", [f"PY16{1000000 + i}" for i in range(len(df))])
    cols = ["txn_id", "merchant_segment", "payment_method", "entry_channel", "hour", "is_festival_week", "customer_tier",
            "customer_tenure_months", "customer_avg_amount_90d", "new_device", "geo_mismatch", "txns_last_24h", "amount"]
    return df[cols], df[["txn_id", "true_type"]]


def main() -> None:
    paths = case_paths(CASE_DIR)
    df, key = generate(rng_for_case(CASE_NUMBER))
    df.to_csv(paths["data"] / "payments.csv", index=False)
    key.to_csv(paths["data"] / "answer_key_teaching_only.csv", index=False)
    print(len(df), df["amount"].describe().round(0).to_dict())
    print(key["true_type"].value_counts().to_dict())
    z = (df["amount"] - df["amount"].mean()) / df["amount"].std()
    print("flagged by z>3:", int((z > 3).sum()))


if __name__ == "__main__":
    main()
