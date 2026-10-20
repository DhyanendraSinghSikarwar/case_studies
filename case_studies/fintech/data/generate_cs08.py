"""
SYNTHETIC DATA GENERATOR - CASE STUDY 8 (Paytm-style mule account detection)
============================================================================
THIS DATA IS SYNTHETIC. Bank account-level AML labels are confidential.

220,000 accounts (train 150k / validation 70k, mirroring the documented 1.5M / 700K split at
1/10 scale) with ~40 candidate account and 30-day transaction-behaviour features and a mule label.
Realism built in:
  * three mule typologies - purpose-made new accounts, rented/sold aged accounts (students),
    cash-out mules (ATM heavy) - each with a random INTENSITY (many mules are lightly used)
  * 15% of genuine customers are "busy traders / gig workers" whose volumes and pass-through
    look mule-like (hard negatives)
  * redundant and pure-noise candidate features, so pruning (documented: down to 17) matters
Calibration anchors (reference file, Case Study 8): imbalanced binary target; existing detection
"roughly 20% precision and 50% recall"; class weighting 1:5; Random Forest chosen; tiered response.
Rates and effect sizes are our assumptions (decision.md D-8-02, D-8-03).

Output: data/cs08/accounts.csv.gz
"""
import os
import numpy as np
import pandas as pd

SEED = 42
N = 220_000
MULE_RATE = 0.008


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    mule = rng.random(N) < MULE_RATE
    typ = np.where(mule, rng.choice(["purpose_made", "rented", "cash_out"], N, p=[0.40, 0.40, 0.20]), "genuine")
    pm, rt, co = typ == "purpose_made", typ == "rented", typ == "cash_out"
    u = np.where(mule, rng.beta(2, 2, N), 0.0)                                  # mule intensity 0..1
    trader = (~mule) & (rng.random(N) < 0.15)                                   # hard negatives
    student = rng.random(N) < np.where(rt, 0.6, 0.08)
    age_days = np.where(pm, np.exp(rng.normal(np.log(60), 0.9, N)), np.exp(rng.normal(np.log(700), 0.9, N)))
    in_cnt = rng.poisson(np.exp(rng.normal(np.log(9) + 1.2 * u + 0.9 * trader, 0.8, N)))
    in_snd = rng.binomial(in_cnt, np.clip(0.35 + 0.30 * u + 0.20 * trader, 0, 0.95))
    out_cnt = rng.poisson(np.exp(rng.normal(np.log(14) + 0.8 * u + 0.6 * trader, 0.6, N)))
    avg_in = np.exp(rng.normal(np.log(2500) + 0.6 * u, 0.9, N))
    pass_a = np.where(trader, 12, 6 + 14 * u); pass_b = np.where(trader, 2, 3 - 1.5 * u)
    df = pd.DataFrame({
        "account_id": [f"A{i:07d}" for i in range(1, N + 1)],
        "account_age_days": np.clip(age_days, 3, 4000).round(),
        "kyc_type": np.where(rng.random(N) < 0.15 + 0.30 * pm, "min-KYC", "full-KYC"),
        "holder_age": np.clip(np.round(np.where(student, rng.normal(21, 2, N), rng.normal(36, 11, N))), 18, 85),
        "occupation": np.where(student, "student", rng.choice(["salaried", "self-employed", "homemaker", "retired", "other"], N, p=[0.45, 0.25, 0.12, 0.08, 0.10])),
        "pincode_risk_tier": rng.choice(["low", "medium", "high"], N, p=[0.6, 0.3, 0.1]),
        "devices_linked_30d": rng.poisson(0.1 + 0.8 * u) + 1,
        "accounts_sharing_device": rng.poisson(0.15 + 0.5 * u + 1.5 * u * pm),
        "inbound_txn_30d": in_cnt,
        "inbound_distinct_senders_30d": in_snd,
        "inbound_count_7d": rng.binomial(in_cnt, 0.3),                                 # redundant with the 30-day count
        "outbound_txn_30d": out_cnt,
        "distinct_beneficiaries_30d": np.minimum(out_cnt, rng.poisson(out_cnt * (0.3 + 0.2 * u) + 1)),
        "avg_inbound_amount": np.round(avg_in, 0),
        "total_inflow_30d": np.round(in_cnt * avg_in, 0),                               # redundant
        "max_single_inbound": np.round(avg_in * np.exp(rng.gamma(2, 0.5, N)), 0),
        "pass_through_ratio": np.round(rng.beta(pass_a, pass_b), 3),
        "median_dwell_minutes": np.round(np.exp(rng.normal(np.log(4000) - 2.5 * u - 1.2 * trader, 1.2, N)), 0),
        "round_amount_share": np.round(rng.beta(2 + 2 * u, 5), 3),
        "night_txn_share": np.round(rng.beta(1.5 + 1.2 * u, 10 - 4 * u), 3),
        "atm_withdrawal_share": np.round(np.where(co, rng.beta(2 + 4 * u, 4), rng.beta(1.2, 8, N)), 3),
        "atm_distinct_locations_30d": rng.poisson(1 + 3 * co * u),
        "merchant_spend_share": np.round(rng.beta(4 - 2.5 * u, 4 + 3 * u), 3),
        "bill_payments_30d": rng.poisson(2.5 - 1.8 * u),
        "salary_like_credit": (rng.random(N) < np.where(trader, 0.20, 0.42 - 0.30 * u)).astype(int),
        "dormant_then_active": (rng.random(N) < np.where(rt, 0.40, 0.03)).astype(int),
        "upi_handle_changes_90d": rng.poisson(0.15 + 0.5 * u),
        "inbound_from_flagged_accounts": rng.poisson(0.03 + 0.45 * u),
        "avg_balance": np.round(np.exp(rng.normal(np.log(18000) - 1.8 * u - 0.7 * trader, 1.2, N)), 0),
        "max_daily_inflow_ratio": np.round(np.exp(rng.normal(0.8 + 0.6 * u, 0.5, N)), 2),
        "email_disposable": (rng.random(N) < 0.03 + 0.15 * pm * u).astype(int),
        "app_logins_30d": rng.poisson(18 + 6 * u),
        "profile_updates_30d": rng.poisson(0.3 + 0.4 * u),
        "failed_login_attempts_30d": rng.poisson(0.6 + 0.5 * u),
        "card_present_txn_30d": rng.poisson(4 - 3 * u),
    })
    for j in range(1, 6):                                                          # pure-noise candidates
        df[f"noise_feature_{j}"] = np.round(rng.normal(0, 1, N), 3)
    df["is_mule"] = mule.astype(int); df["mule_type"] = typ
    df["split"] = np.where(rng.random(N) < 150_000 / N, "train", "validation")
    # ---- data-quality issues ----
    df.loc[df.sample(frac=0.02, random_state=seed).index, "median_dwell_minutes"] = np.nan    # no outflow in window
    df.loc[df.sample(n=40, random_state=seed + 1).index, "holder_age"] = 0                    # KYC parse failure
    df.loc[df.sample(n=25, random_state=seed + 2).index, "pass_through_ratio"] = 1.7          # >1 impossible (reversal double count)
    return df


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs08"), exist_ok=True)
    d = generate(); d.to_csv(os.path.join(here, "cs08", "accounts.csv.gz"), index=False)
    print(len(d), round(d.is_mule.mean(), 4), d.mule_type.value_counts().to_dict())
