"""
SYNTHETIC DATA GENERATOR - CASE STUDY 15 (MobiKwik-style wallet-behaviour score for BNPL pre-approval and limits)
================================================================================================================
THIS DATA IS SYNTHETIC. Wallet and BNPL data are confidential.

Wallet users with 6 months of behaviour (spend patterns, bill payments, top-up habits, outstanding
amounts, channel preference, device/location stability, app usage) plus ENGAGEMENT signals
(contactability = verified reachable phone; responsiveness = reacts to in-app nudges).
Two cohorts receive BNPL ("ZIP") credit lines and are observed for 6 months:
  * HISTORICAL cohort - limits set by the old rule (better-looking users got higher limits): confounded
  * EXPERIMENT cohort - pre-approved users randomly assigned a limit of Rs 1k / 2k / 3k / 5k (credit-line test)
Outcomes: spend on the line, revenue (merchant fee + late fees), default (90+ DPD) and, for users who
become 30+ DPD, whether collections CURE them (where contactability/responsiveness matter most).
A higher limit raises spend for everyone but raises default mainly for low-quality users.

Calibration anchors (reference file, Case Study 15): "More than 500 raw and derived variables";
behavioural, device/location and engagement ("contactability, responsiveness") data feed MobiScore,
which drives pre-approval and limits. No metrics disclosed. Rates are our assumptions (decision.md
D-15-02). Hidden truth columns start with "_".

Output: data/cs15/users.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.special import expit

SEED = 42
LIMITS = [1000, 2000, 3000, 5000]


def generate(seed=SEED, n=140_000):
    rng = np.random.default_rng(seed)
    q = rng.normal(0, 1, n)                                                          # latent repayment quality
    need = rng.normal(0, 1, n)                                                       # latent credit appetite
    tenure_m = np.clip(rng.gamma(2.5, 9, n), 1, 96).round()
    txn_6m = rng.poisson(np.exp(3.2 + 0.25 * need + 0.15 * q))
    spend_6m = np.round(txn_6m * np.exp(rng.normal(np.log(420), 0.5, n) + 0.1 * need), -1)
    bill_pay_share = np.clip(rng.beta(2, 5, n) + 0.06 * q, 0, 1)                     # utilities / postpaid paid via wallet
    ontime_bill_rate = np.clip(rng.beta(8 + 2 * q.clip(-2, 2), 2, n), 0, 1)
    topup_regular = np.clip(rng.beta(3, 3, n) + 0.08 * q, 0, 1)                      # regular vs last-minute top-ups
    low_bal_days = np.clip(rng.poisson(np.exp(1.6 - 0.35 * q + 0.2 * need)), 0, 180)
    p2p_out_share = np.clip(rng.beta(2, 6, n) + 0.05 * need - 0.03 * q, 0, 1)
    gaming_share = np.clip(rng.beta(1, 15, n) + 0.03 * (q < -1), 0, 1)
    device_changes_6m = rng.poisson(np.exp(-1.5 - 0.3 * q))
    city_changes_6m = rng.poisson(np.exp(-1.8 - 0.2 * q))
    app_sessions_wk = np.clip(rng.gamma(2, 3, n) * np.exp(0.2 * need), 0.2, 80).round(1)
    contactable = (rng.random(n) < expit(1.6 + 0.3 * q)).astype(int)                 # verified, reachable phone
    responsive = np.clip(rng.beta(2, 3, n) + 0.05 * q, 0, 1)                         # share of nudges acted on
    income_proxy = np.exp(rng.normal(np.log(22000), 0.5, n) + 0.15 * q)
    cohort = np.where(rng.random(n) < 0.5, "historical", "experiment")
    # ---------- limit assignment ----------
    old_rule_score = 0.6 * q + 0.4 * (np.log(spend_6m + 1) - 9) + rng.normal(0, 0.6, n)        # old rule sees part of quality
    hist_lim = np.select([old_rule_score > 0.9, old_rule_score > 0.2, old_rule_score > -0.5], [5000, 3000, 2000], 1000)
    exp_lim = rng.choice(LIMITS, n)
    eligible = old_rule_score > -1.4                                                 # pre-approved (others not offered)
    limit = np.where(cohort == "historical", hist_lim, exp_lim)
    # ---------- outcomes over 6 months ----------
    demand = np.exp(rng.normal(np.log(1800), 0.6, n) + 0.45 * need)
    util = np.clip(demand / limit, 0.05, 1.0) * np.clip(rng.normal(1, 0.1, n), 0.6, 1.2)
    used = np.minimum(limit, np.round(util * limit, -1))
    spend_line = np.round(used * (1.6 + 0.3 * rng.random(n)), -1)                    # revolving use over 6 months
    lim_k = limit / 1000
    z_def = -3.5 - 0.95 * q + 0.25 * need + 0.32 * (lim_k - 2) * np.where(q < 0, 1.0 - 0.5 * q, 0.15) + 0.6 * (used / income_proxy) * 3
    p_def = expit(z_def); default = (rng.random(n) < p_def).astype(int)
    p_dpd30 = np.clip(p_def * 2.2 + 0.02, 0, 0.98); dpd30 = np.maximum(default, (rng.random(n) < p_dpd30).astype(int))
    p_cure = expit(-0.4 + 1.4 * contactable + 2.2 * (responsive - 0.4) + 0.3 * q)
    cured = np.where((dpd30 == 1) & (default == 0), (rng.random(n) < p_cure).astype(int), np.where(default == 1, 0, -1))
    late_fee = np.where(dpd30 == 1, 250, 0) * (rng.random(n) < 0.7)
    revenue = np.round(0.02 * spend_line + late_fee, 0)
    loss = np.round(np.where(default == 1, used * 0.85, 0), 0)
    df = pd.DataFrame({"user_id": [f"W{i:06d}" for i in range(n)], "cohort": cohort, "pre_approved": eligible.astype(int), "tenure_months": tenure_m,
                       "txn_count_6m": txn_6m, "wallet_spend_6m": spend_6m, "bill_pay_share": bill_pay_share.round(3), "ontime_bill_rate": ontime_bill_rate.round(3),
                       "topup_regularity": topup_regular.round(3), "low_balance_days_6m": low_bal_days, "p2p_out_share": p2p_out_share.round(3),
                       "gaming_share": gaming_share.round(3), "device_changes_6m": device_changes_6m, "city_changes_6m": city_changes_6m,
                       "app_sessions_per_week": app_sessions_wk, "contactable": contactable, "nudge_response_rate": responsive.round(3),
                       "credit_limit": limit, "line_spend_6m": spend_line, "max_utilised": used, "dpd30_6m": dpd30, "default_90dpd": default,
                       "cured_after_dpd30": cured, "revenue_inr": revenue, "loss_inr": loss, "_q": q, "_p_default": p_def})
    df = df[df.pre_approved == 1].drop(columns="pre_approved").reset_index(drop=True)
    # data-quality defects
    df.loc[df.sample(n=350, random_state=seed).index, "app_sessions_per_week"] = np.nan           # SDK opt-out
    df.loc[df.sample(n=120, random_state=seed + 1).index, "max_utilised"] = df.credit_limit * 1.4   # over-limit bug (merchant reversal posted late)
    df = pd.concat([df, df.sample(n=300, random_state=seed + 2)], ignore_index=True)
    return df


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs15"), exist_ok=True)
    d = generate(); d.to_csv(os.path.join(here, "cs15", "users.csv.gz"), index=False)
    dd = d.drop_duplicates("user_id")
    print(len(dd), "pre-approved users | default", dd.default_90dpd.mean().round(4), "| dpd30", dd.dpd30_6m.mean().round(4))
    print(dd.groupby(["cohort", "credit_limit"]).agg(n=("user_id", "size"), default=("default_90dpd", "mean"), q=("_q", "mean"), rev=("revenue_inr", "mean"), loss=("loss_inr", "mean")).round(3))
    print("cure rate by contactable", dd[dd.cured_after_dpd30 >= 0].groupby("contactable").cured_after_dpd30.mean().round(3).to_dict())
