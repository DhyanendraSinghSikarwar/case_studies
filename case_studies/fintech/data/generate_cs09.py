"""
SYNTHETIC DATA GENERATOR - CASE STUDY 9 (RBIH MuleHunter.AI-style cross-bank mule detection)
===========================================================================================
THIS DATA IS SYNTHETIC. Bank account and transaction data are confidential.

Six partner banks (2 large public-sector banks with rural/semi-urban books, 1 mid PSB, 1 private bank,
1 small finance bank, 1 late-joining regional bank) submit 90-day account aggregates. Mule accounts
follow 8 expert TYPOLOGIES (a subset of the documented "19 distinct patterns"):
  T1 rapid pass-through      T2 fan-in from many senders   T3 dormant-account reactivation
  T4 new account, big inflow T5 cash-out in round amounts  T6 device / SIM churn
  T7 late-night activity     T8 inflow far above declared income/occupation
Each mule shows 1-3 typologies; 30% are low-intensity "sleepers". Genuine hard negatives:
small traders (many senders), farmers/pensioners (cash withdrawals), gig workers (night activity),
students receiving from family, dormant accounts genuinely reactivated.
Labels: confirmed mule (investigation / I4C complaint); ~15% of true mules are never confirmed.

Calibration anchors (reference file, Case Study 9): "19 distinct patterns"; peak mule activity
"11 PM-1 AM"; rule systems "80 per cent false positives"; MuleHunter "90 per cent positive alerts";
mules "53% of the total fraud threats". Sizes/rates are our assumptions (decision.md D-9-02).
Hidden truth columns start with "_".

Outputs: data/cs09/accounts.csv.gz, data/cs09/txn_hour_sample.csv.gz
"""
import os
import numpy as np
import pandas as pd

SEED = 42
BANKS = {  # name: (accounts, mule_rate, occupation mix [salaried, trader, student, homemaker, farmer, gig, pensioner], typology weights T1..T8)
    "PSB-A (large, rural)":   (40_000, 0.010, [0.22, 0.14, 0.10, 0.14, 0.24, 0.06, 0.10], [1, 1, 3, 1, 3, 1, 1, 3]),
    "PSB-B (large, semi-urban)": (36_000, 0.012, [0.28, 0.16, 0.12, 0.12, 0.14, 0.08, 0.10], [2, 2, 2, 1, 2, 1, 1, 2]),
    "PSB-C (mid)":            (20_000, 0.011, [0.30, 0.15, 0.12, 0.10, 0.12, 0.10, 0.11], [2, 2, 2, 2, 2, 1, 1, 2]),
    "Private-D (urban)":      (22_000, 0.008, [0.45, 0.14, 0.14, 0.06, 0.02, 0.15, 0.04], [3, 3, 1, 2, 1, 2, 2, 1]),
    "SFB-E (small finance)":  (14_000, 0.016, [0.20, 0.28, 0.10, 0.12, 0.12, 0.12, 0.06], [2, 3, 1, 3, 2, 2, 1, 2]),
    "RRB-F (late joiner)":    (12_000, 0.014, [0.18, 0.12, 0.12, 0.16, 0.26, 0.08, 0.08], [1, 1, 2, 1, 2, 3, 3, 2]),
}
OCC = ["salaried", "trader", "student", "homemaker", "farmer", "gig_worker", "pensioner"]
INC = dict(zip(OCC, [45000, 60000, 3000, 5000, 15000, 22000, 25000]))


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    out = []
    for b, (n, mr, occ_p, tw) in BANKS.items():
        occ = rng.choice(OCC, n, p=np.array(occ_p) / sum(occ_p))
        is_m = rng.random(n) < mr
        # mules are recruited disproportionately among students, homemakers, farmers, gig workers
        rec = is_m & (rng.random(n) < 0.6); occ[rec] = rng.choice(["student", "homemaker", "farmer", "gig_worker"], rec.sum(), p=[0.4, 0.25, 0.2, 0.15])
        inc = np.array([INC[o] for o in occ]) * np.exp(rng.normal(0, 0.6, n))
        f = lambda o: (occ == o)
        mult = 3 * np.exp(rng.normal(0, 0.6, n)) * np.where(f("trader"), 2.5, 1) * np.where(rng.random(n) < 0.03, rng.uniform(4, 20, n), 1)   # 3%: one-off big credit (land sale, loan)
        credits = inc * mult
        n_cr = np.maximum(1, rng.poisson(np.select([f("trader"), f("gig_worker"), f("salaried")], [120, 55, 5], 8)))
        senders = np.maximum(1, rng.poisson(np.select([f("trader"), f("gig_worker"), f("student")], [38, 14, 2], 3) * np.exp(rng.normal(0, 0.5, n))))
        pass_thr = np.clip(rng.beta(9, 1.6, n) * np.where(f("trader") | f("gig_worker"), 1.0, 0.97), 0, 1.2)
        hold_h = np.exp(rng.normal(np.log(np.where(f("trader"), 40, 200)), 1.2))
        cash = np.clip(rng.beta(2, 8, n) + np.where(f("farmer") | f("pensioner"), 0.35, 0), 0, 1)
        round_sh = np.clip(rng.beta(2, 7, n) + np.where(f("farmer") | f("pensioner"), 0.2, 0), 0, 1)
        night = np.clip(rng.beta(1.5, 40, n) + np.where(f("gig_worker"), 0.10, 0), 0, 1)
        devices = 1 + rng.binomial(2, 0.15, n); sim = (rng.random(n) < 0.03).astype(int)
        dormant = np.where(rng.random(n) < 0.05, rng.uniform(180, 900, n), rng.uniform(0, 20, n))
        age_days = np.where(rng.random(n) < 0.08, rng.uniform(10, 180, n), rng.uniform(180, 6000, n))
        # ---------- mule typologies ----------
        typ = np.full(n, "", dtype=object); idx = np.flatnonzero(is_m)
        sleeper = rng.random(n) < 0.40
        w = np.array(tw, float) / sum(tw)
        for i in idx:
            k = rng.choice([1, 2, 3], p=[0.4, 0.4, 0.2]); ts_ = rng.choice(8, k, replace=False, p=w); typ[i] = "|".join(f"T{t + 1}" for t in sorted(ts_))
            s = 0.35 if sleeper[i] else 1.0                                   # sleepers show weaker patterns
            credits[i] *= 1 + s * rng.uniform(0.3, 2.5)
            for t in ts_:
                if t == 0: pass_thr[i] = 1 - s * rng.uniform(0.0, 0.03) - (1 - s) * 0.05; hold_h[i] = np.exp(np.log(hold_h[i]) * (1 - s) + s * np.log(rng.uniform(1, 8)))
                if t == 1: senders[i] = int(senders[i] + s * rng.uniform(15, 90)); n_cr[i] = int(n_cr[i] + s * rng.uniform(30, 200))
                if t == 2: dormant[i] = s * rng.uniform(200, 900) + (1 - s) * dormant[i]
                if t == 3: age_days[i] = s * rng.uniform(10, 90) + (1 - s) * age_days[i]
                if t == 4: cash[i] = cash[i] * (1 - s) + s * rng.uniform(0.6, 0.95); round_sh[i] = round_sh[i] * (1 - s) + s * rng.uniform(0.6, 0.9)
                if t == 5: devices[i] = devices[i] + int(round(s * rng.integers(2, 6))); sim[i] = int(rng.random() < 0.3 + 0.6 * s)
                if t == 6: night[i] = night[i] * (1 - s) + s * rng.uniform(0.25, 0.6)
                if t == 7: credits[i] = credits[i] * (1 + s * rng.uniform(2, 10))
        debits = credits * pass_thr
        bal = np.maximum(0, credits / 3 * (1.05 - pass_thr) * np.exp(rng.normal(0, 0.5, n)) + rng.uniform(0, 3000, n))
        # labels: 85% of true mules confirmed (investigation / I4C complaint), bank-specific
        conf = is_m & (rng.random(n) < 0.85)
        out.append(pd.DataFrame({"bank": b, "account_id": [f"{b[:5].replace(' ', '').replace('(', '')}-{i:06d}" for i in range(n)],
                                 "occupation": occ, "declared_income_monthly": np.round(inc, -2), "customer_age": np.clip(rng.normal(36, 13, n), 18, 85).round(),
                                 "kyc_type": np.where(rng.random(n) < np.where(is_m, 0.35, 0.12), "minimum_kyc", "full_kyc"),
                                 "account_age_days": age_days.round(), "dormant_days_before": dormant.round(),
                                 "credits_90d_inr": np.round(credits, -1), "debits_90d_inr": np.round(debits, -1), "n_credits_90d": n_cr,
                                 "avg_balance_inr": np.round(bal, -1), "distinct_senders_30d": senders, "median_hold_hours": hold_h.round(1),
                                 "cash_withdrawal_share": cash.round(3), "round_amount_share": round_sh.round(3), "night_share_23_01": night.round(3),
                                 "n_devices_30d": devices, "sim_change_30d": sim, "confirmed_mule": conf.astype(int),
                                 "_is_mule": is_m.astype(int), "_typologies": typ, "_sleeper": (sleeper & is_m).astype(int)}))
    df = pd.concat(out, ignore_index=True)
    # data-quality defects
    df.loc[df.sample(frac=0.05, random_state=seed).index, "declared_income_monthly"] = np.nan        # income not captured (old KYC)
    df = pd.concat([df, df[df.bank == "PSB-B (large, semi-urban)"].sample(n=600, random_state=seed + 1)], ignore_index=True)  # double submission
    df.loc[df.sample(n=200, random_state=seed + 2).index, "night_share_23_01"] = 1.7                 # impossible share (unit bug: % / 60)
    # transaction-hour sample for the "11 PM - 1 AM" analysis
    m = df[df._is_mule == 1].drop_duplicates("account_id").sample(1200, random_state=seed); g = df[df._is_mule == 0].drop_duplicates("account_id").sample(1200, random_state=seed)
    hrs = []
    for lab, d in ((1, m), (0, g)):
        for acc, ns in zip(d.account_id, d.night_share_23_01.clip(0, 1)):
            k = 12; night_n = rng.binomial(k, min(0.95, ns * 2.2 + (0.25 if lab else 0)))
            h_n = (np.round(rng.vonmises(0, 6.0, night_n) / (2 * np.pi) * 24 * 60) % 1440) / 60            # centred on midnight
            h_d = (np.round(rng.vonmises(np.pi * 13 / 12, 1.4, k - night_n) / (2 * np.pi) * 24 * 60) % 1440) / 60  # centred on 13:00
            for h in np.r_[h_n, h_d]: hrs.append((acc, lab, round(float(h), 3)))
    hours = pd.DataFrame(hrs, columns=["account_id", "_is_mule", "txn_hour_decimal"])
    return df, hours


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs09"), exist_ok=True)
    d, h = generate(); d.to_csv(os.path.join(here, "cs09", "accounts.csv.gz"), index=False); h.to_csv(os.path.join(here, "cs09", "txn_hour_sample.csv.gz"), index=False)
    dd = d.drop_duplicates("account_id")
    print(len(dd), "accounts | mules", dd._is_mule.sum(), "confirmed", dd.confirmed_mule.sum())
    print(dd.groupby("bank")._is_mule.mean().round(4).to_dict())
    print(len(h), "hour rows")
