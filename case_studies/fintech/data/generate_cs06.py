"""
SYNTHETIC DATA GENERATOR - CASE STUDY 6 (PhonePe-style real-time P2P UPI fraud prevention)
==========================================================================================
THIS DATA IS SYNTHETIC. UPI transaction logs with fraud labels are confidential.

We simulate 8 weeks (1 Sep - 26 Oct 2025) of P2P UPI transfers with feature-store style
pre-computed features (sender / receiver / transaction families, as documented), a hidden
TRUE label (fraud / dispute / legit), and the NOISY label a team actually sees: user
complaints with a self-reported reason code. An investigator audit of 2,000 complaints
gives the "ground truth" sample used to engineer labels.

Calibration anchors (reference file, Case Study 6): "Many complaints are disputes (e.g.,
dissatisfaction with a product), not fraud"; features = sender / receiver / transaction
aggregates; documented outcomes: -40% fraud rate, -38% complaints (-50% high-value),
~1% reinstatement of blacklisted users. Rates and effect sizes are our assumptions
(decision.md D-6-02 ... D-6-04).

Output: data/cs06/upi_p2p_transactions.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.special import expit

SEED = 42
N_TXN = 600_000
START = pd.Timestamp("2025-09-01"); DAYS = 56
N_SENDERS, N_RECEIVERS, N_MULES, N_SELLERS = 120_000, 90_000, 700, 2_500


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    # ---- entities ----
    s_age_band = rng.choice(["18-25", "26-40", "41-55", "56+"], N_SENDERS, p=[0.25, 0.42, 0.23, 0.10])
    s_tenure = np.clip(np.exp(rng.normal(np.log(400), 1.0, N_SENDERS)), 1, 3000).round()
    s_tier = rng.choice(["Tier 1", "Tier 2", "Tier 3"], N_SENDERS, p=[0.40, 0.35, 0.25])
    s_med_amt = np.exp(rng.normal(np.log(700), 0.8, N_SENDERS))
    s_vuln = expit(-3.2 + 0.9 * (s_age_band == "56+") + 0.6 * (s_tenure < 60) + 0.3 * (s_tier == "Tier 3"))  # scam susceptibility
    n_r = N_RECEIVERS + N_MULES + N_SELLERS
    r_type = np.array(["individual"] * N_RECEIVERS + ["mule"] * N_MULES + ["small_seller"] * N_SELLERS)
    r_tenure = np.where(r_type == "mule", np.where(rng.random(n_r) < 0.5, np.exp(rng.normal(np.log(20), 0.8, n_r)), np.exp(rng.normal(np.log(300), 0.9, n_r))),  # half new, half rented/aged
                np.where(r_type == "small_seller", np.exp(rng.normal(np.log(500), 0.7, n_r)), np.exp(rng.normal(np.log(450), 1.0, n_r)))).clip(1, 3000).round()

    # ---- transactions ----
    ts = START + pd.to_timedelta(rng.uniform(0, DAYS * 86400, N_TXN), unit="s")
    hour = ts.hour.to_numpy()
    kind = rng.choice(["legit", "fraud", "dispute"], N_TXN, p=[0.9945, 0.0020, 0.0035])
    sender = np.where(kind == "fraud", rng.choice(N_SENDERS, N_TXN, p=s_vuln / s_vuln.sum()), rng.integers(0, N_SENDERS, N_TXN))
    recv = np.where(kind == "fraud", N_RECEIVERS + rng.integers(0, N_MULES, N_TXN),
            np.where(kind == "dispute", N_RECEIVERS + N_MULES + rng.integers(0, N_SELLERS, N_TXN),
                     np.where(rng.random(N_TXN) < 0.06, N_RECEIVERS + N_MULES + rng.integers(0, N_SELLERS, N_TXN), rng.integers(0, N_RECEIVERS, N_TXN))))
    f, dsp = kind == "fraud", kind == "dispute"
    base_amt = s_med_amt[sender] * np.exp(rng.normal(0, 0.9, N_TXN))
    amount = np.where(f, base_amt * np.exp(rng.normal(1.1, 0.9, N_TXN)), np.where(dsp, base_amt * np.exp(rng.normal(0.6, 0.6, N_TXN)), base_amt))
    amount = np.clip(np.round(amount, 0), 1, 100_000)          # UPI P2P cap Rs 1 lakh
    df = pd.DataFrame({
        "txn_id": [f"U{i:08d}" for i in range(1, N_TXN + 1)], "timestamp": ts,
        "sender_id": [f"S{i:06d}" for i in sender], "receiver_id": [f"R{i:06d}" for i in recv],
        "amount_inr": amount,
        "sender_age_band": s_age_band[sender], "sender_city_tier": s_tier[sender], "sender_tenure_days": s_tenure[sender],
        "sender_txn_count_7d": rng.poisson(np.where(f, 6, 9)),
        "amount_to_sender_median": np.round(amount / s_med_amt[sender], 3),
        "is_new_payee": (rng.random(N_TXN) < np.where(f, 0.85, np.where(dsp, 0.55, 0.22))).astype(int),
        "is_collect_request": (rng.random(N_TXN) < np.where(f, 0.45, np.where(dsp, 0.10, 0.04))).astype(int),
        "device_changed_24h": (rng.random(N_TXN) < np.where(f, 0.18, 0.02)).astype(int),
        # merchant-like naming / UPI handle: noisy - 25% of mules pose as sellers (fake-shop scams), 30% of real sellers look personal
        "receiver_type_hint": np.where(rng.random(N_TXN) < np.where(r_type[recv] == "small_seller", 0.70, np.where(r_type[recv] == "mule", 0.25, 0.02)),
                                       "business-like", "individual"),
        "receiver_tenure_days": r_tenure[recv],
        "receiver_distinct_senders_24h": rng.poisson(np.where(r_type[recv] == "mule", np.exp(rng.normal(np.log(4), 0.8, N_TXN)), np.where(r_type[recv] == "small_seller", 14, 1.2))),
        "receiver_prior_complaints_30d": rng.poisson(np.where(r_type[recv] == "mule", 0.4, np.where(r_type[recv] == "small_seller", 0.6, 0.02))),
        "hour": hour,
    })
    # ---- hidden truth and the noisy label actually observed ----
    df["true_label"] = kind
    p_complain = np.where(f, 0.72, np.where(dsp, 0.60, 0.00025))
    comp = rng.random(N_TXN) < p_complain
    reasons = np.array(["fraud/scam", "unauthorised debit", "product not received", "refund not processed", "wrong transfer"])
    pr_fraud = [0.62, 0.30, 0.03, 0.02, 0.03]; pr_disp = [0.30, 0.05, 0.40, 0.20, 0.05]; pr_legit = [0.15, 0.10, 0.10, 0.15, 0.50]
    reason = np.where(f, rng.choice(reasons, N_TXN, p=pr_fraud), np.where(dsp, rng.choice(reasons, N_TXN, p=pr_disp), rng.choice(reasons, N_TXN, p=pr_legit)))
    df["complaint_filed"] = comp.astype(int)
    df["complaint_reason"] = np.where(comp, reason, None)
    df["complaint_delay_days"] = np.where(comp, np.round(rng.gamma(2.0, 2.5, N_TXN), 1), np.nan)
    # investigator audit: random 2,000 complaints get a confirmed label
    comp_idx = np.flatnonzero(comp)
    audit = rng.choice(comp_idx, 2000, replace=False)
    df["audited"] = 0; df.loc[audit, "audited"] = 1
    df["audit_outcome"] = np.where(df.audited == 1, df.true_label, None)
    df = df.sort_values("timestamp").reset_index(drop=True)
    # ---- data-quality issues ----
    df.loc[df.sample(n=300, random_state=seed).index, "amount_inr"] = 0          # zero-amount test pings (UPI "verify VPA")
    df.loc[df.sample(frac=0.01, random_state=seed + 1).index, "receiver_tenure_days"] = np.nan   # feature-store miss
    late = df.complaint_filed.eq(1) & (df.timestamp > START + pd.Timedelta(days=DAYS - 10))
    df["complaint_received_by_cutoff"] = np.where(df.complaint_filed.eq(1), ((df.timestamp + pd.to_timedelta(df.complaint_delay_days.fillna(0), unit="D")) <= START + pd.Timedelta(days=DAYS + 3)).astype(int), np.nan)
    return df


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs06"), exist_ok=True)
    d = generate()
    d.to_csv(os.path.join(here, "cs06", "upi_p2p_transactions.csv.gz"), index=False)
    print(len(d), d.true_label.value_counts().to_dict(), "complaints", int(d.complaint_filed.sum()))
