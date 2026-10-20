"""
SYNTHETIC DATA GENERATOR - CASE STUDY 16 (BharatPe-style merchant lending from QR data + KYC name matching)
==========================================================================================================
THIS DATA IS SYNTHETIC. Merchant QR settlements, loans and KYC documents are confidential.

Part A - merchants: 40,000 small merchants with 15 months of monthly QR aggregates (value, count, unique
payers, active days). Months 1-12 are history; months 13-15 are the "future" that a borrowing-capacity
model must anticipate. 12,000 merchants took a 6-month loan in month 12, repaid by an equated DAILY
instalment (EDI) deducted from QR settlements. Default (missed > 30 days of EDI) depends on the repayment
BURDEN (EDI / actual future daily QR inflow), merchant quality and cash-flow volatility.
The true default function is exposed as `true_default_prob` so the notebook can evaluate counterfactual
limit policies (a "digital twin"; clearly flagged).

Part B - KYC name matching: 30,000 (KYC name, bank-account holder name) pairs. Genuine pairs differ by
Indian name variants (initials, surname order, honorifics, Mohd/Mohammed, Kumar/Kr, transliteration,
typos, shop name instead of owner name). Mismatches are third-party / mule accounts; some share a surname.

Calibration anchors (reference file, Case Study 16): borrowing capacity "from transaction volume and
frequency"; "over 200 attributes"; FuzzyWuzzy name matching; TAT "from two days to just five seconds".
Rates are our assumptions (decision.md D-16-02). Hidden truth columns start with "_".

Outputs: data/cs16/merchant_monthly.csv.gz, data/cs16/loans.csv.gz, data/cs16/name_pairs.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.special import expit

SEED = 42
CATS = ["kirana", "pharmacy", "restaurant", "apparel", "mobile_shop", "salon", "fruit_veg", "hardware"]


def true_default_prob(burden, q, vol):
    """Hidden truth: P(default) of a 6-month EDI loan given burden = EDI / actual daily inflow."""
    return expit(-3.4 - 0.8 * q + 1.1 * vol + 7.0 * np.clip(burden - 0.10, 0, None) + 2.0 * burden)


def merchants(rng, n=40_000, months=15):
    q = rng.normal(0, 1, n); cat = rng.choice(CATS, n, p=[0.28, 0.10, 0.14, 0.10, 0.08, 0.08, 0.14, 0.08])
    base = np.exp(rng.normal(np.log(90_000), 0.8, n) + 0.15 * q)                     # monthly QR value
    trend = rng.normal(0.01 + 0.006 * q, 0.02, n)                                       # monthly growth
    vol = np.clip(rng.gamma(2, 0.08, n) * np.where(np.isin(cat, ["restaurant", "apparel"]), 1.5, 1.0) * np.exp(-0.15 * q), 0.03, 0.9)
    season = {"apparel": 0.25, "mobile_shop": 0.15, "restaurant": 0.1}
    rows = []
    shock = rng.random(n) < 0.06                                                      # 6%: business shock in the future months
    for m in range(months):
        s = np.array([season.get(c, 0.05) for c in cat]) * np.sin(2 * np.pi * (m + 3) / 12)
        val = base * np.exp(trend * m + s + rng.normal(0, vol, n)) * np.where(shock & (m >= 12), rng.uniform(0.3, 0.7, n), 1.0)
        cnt = np.maximum(1, rng.poisson(val / np.exp(rng.normal(np.log(180), 0.3, n))))
        payers = np.maximum(1, np.round(cnt * np.clip(rng.beta(3, 4, n) + 0.05 * q, 0.05, 1)))
        days = np.clip(np.round(26 + 2 * q + rng.normal(0, 2, n) - 6 * (shock & (m >= 12))), 5, 31)
        rows.append(pd.DataFrame({"merchant_id": [f"M{i:06d}" for i in range(n)], "month": m + 1, "qr_value_inr": np.round(val, -1),
                                  "qr_txn_count": cnt, "unique_payers": payers, "active_days": days}))
    mm = pd.concat(rows, ignore_index=True)
    prof = pd.DataFrame({"merchant_id": [f"M{i:06d}" for i in range(n)], "category": cat, "months_on_platform": np.clip(rng.gamma(3, 8, n), 12, 72).round(),
                         "owner_age": np.clip(rng.normal(38, 10, n), 21, 70).round(), "has_soundbox": (rng.random(n) < 0.55).astype(int),
                         "city_tier": rng.choice([1, 2, 3], n, p=[0.3, 0.4, 0.3]), "_q": q, "_vol": vol, "_shock": shock.astype(int)})
    return mm, prof


def loans(rng, mm, prof, n_loans=12_000):
    idx = rng.choice(len(prof), n_loans, replace=False); p = prof.iloc[idx].reset_index(drop=True)
    hist = mm[mm.month.between(10, 12)].groupby("merchant_id").qr_value_inr.mean()
    fut = mm[mm.month.between(13, 15)].groupby("merchant_id").qr_value_inr.mean()
    h = hist.reindex(p.merchant_id).values; f = fut.reindex(p.merchant_id).values
    mult = rng.uniform(0.25, 1.7, n_loans)                                             # legacy rule: loan = mult x avg monthly QR (varied by officer / campaign)
    amount = np.round(h * mult, -3)
    edi = amount * 1.12 / 180                                                          # 6-month tenure, 12% flat fee, daily instalment
    burden_true = edi / (f / 30)
    pdef = true_default_prob(burden_true, p._q.values, p._vol.values)
    default = (rng.random(n_loans) < pdef).astype(int)
    return pd.DataFrame({"loan_id": [f"LN{i:06d}" for i in range(n_loans)], "merchant_id": p.merchant_id, "loan_amount": amount, "edi_inr": np.round(edi, 0),
                         "default_30d_missed": default, "_burden_true": burden_true, "_p_default": pdef})


VARIANTS = {"Mohammed": ["Mohd", "Md", "Mohamed", "Muhammad"], "Kumar": ["Kr", "Kumaar"], "Lakshmi": ["Laxmi", "Lakshmy"], "Venkatesh": ["Venkatesan", "Venkatesha"],
            "Srinivas": ["Shrinivas", "Srinivasa"], "Sharma": ["Sarma"], "Chaudhary": ["Choudhary", "Chaudhari", "Chowdhury"], "Agarwal": ["Agrawal", "Aggarwal"]}
FIRST = ["Ramesh", "Suresh", "Mohammed", "Lakshmi", "Venkatesh", "Srinivas", "Anita", "Pooja", "Rajesh", "Imran", "Sunita", "Arjun", "Kavita", "Deepak", "Fatima",
         "Gurpreet", "Manoj", "Rekha", "Sanjay", "Priya", "Abdul", "Harish", "Meena", "Vijay", "Asha"]
MID = ["Kumar", "Lal", "Devi", "Prasad", "Singh", "", "", "", "", ""]
LAST = ["Sharma", "Patel", "Reddy", "Chaudhary", "Agarwal", "Khan", "Iyer", "Gupta", "Yadav", "Das", "Nair", "Shaikh", "Verma", "Rao", "Joshi", "Mehta", "Ansari", "Pillai"]
SHOPS = ["Traders", "General Store", "Medicals", "Enterprises", "Kirana", "Mobile Point", "Fashion"]


def _typo(rng, s):
    if len(s) < 4: return s
    i = rng.integers(1, len(s) - 1); op = rng.integers(3)
    return s[:i] + s[i + 1:] if op == 0 else s[:i] + s[i + 1] + s[i] + s[i + 2:] if op == 1 else s[:i] + rng.choice(list("aeiourn")) + s[i + 1:]


def name_pairs(rng, n=30_000):
    rows = []
    for k in range(n):
        f, m, l = rng.choice(FIRST), rng.choice(MID), rng.choice(LAST)
        kyc = " ".join(x for x in [f, m, l] if x)
        match = rng.random() < 0.85
        if match:
            parts = [f, m, l]; kind = rng.choice(["exact", "case_space", "initial", "order", "variant", "typo", "honorific", "drop_middle", "shop_name"],
                                                p=[0.25, 0.10, 0.12, 0.10, 0.12, 0.10, 0.07, 0.08, 0.06])
            if kind == "case_space": acc = "  ".join(x.upper() for x in parts if x)
            elif kind == "initial": acc = " ".join(x for x in [f[0], m[:1] if m else "", l] if x)
            elif kind == "order": acc = " ".join(x for x in [l, f, m] if x)
            elif kind == "variant": acc = " ".join(x for x in [rng.choice(VARIANTS.get(f, [f])), rng.choice(VARIANTS.get(m, [m])) if m else "", rng.choice(VARIANTS.get(l, [l]))] if x)
            elif kind == "typo": acc = " ".join(_typo(rng, x) for x in parts if x)
            elif kind == "honorific": acc = rng.choice(["Mr ", "Shri ", "Smt ", "Mrs "]) + kyc
            elif kind == "drop_middle": acc = f"{f} {l}"
            elif kind == "shop_name": acc = f"{f} {rng.choice(SHOPS)}"
            else: acc = kyc
        else:
            kind = rng.choice(["unrelated", "same_surname", "same_first"], p=[0.6, 0.25, 0.15])
            f2, l2 = rng.choice(FIRST), rng.choice(LAST)
            acc = f"{f2} {l2}" if kind == "unrelated" else f"{f2} {rng.choice(MID)} {l}".replace("  ", " ") if kind == "same_surname" else f"{f} {l2}"
            if acc.replace(" ", "").lower() == kyc.replace(" ", "").lower(): acc = f"{rng.choice(FIRST)} {rng.choice(LAST)}"
        rows.append((f"P{k:06d}", kyc, acc, int(match), kind))
    return pd.DataFrame(rows, columns=["pair_id", "kyc_name", "bank_account_name", "_is_same_person", "_variant"])


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    mm, prof = merchants(rng); ln = loans(rng, mm, prof); nm = name_pairs(rng)
    # data-quality defects
    mm.loc[mm.sample(n=900, random_state=seed).index, "qr_value_inr"] = np.nan              # settlement file gaps
    mm = pd.concat([mm, mm.sample(n=1200, random_state=seed + 1)], ignore_index=True)         # duplicated monthly rows
    nm.loc[nm.sample(n=150, random_state=seed + 2).index, "bank_account_name"] = ""            # blank name returned by the bank API
    return mm, prof, ln, nm


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs16"), exist_ok=True)
    mm, prof, ln, nm = generate()
    mm.to_csv(os.path.join(here, "cs16", "merchant_monthly.csv.gz"), index=False); prof.to_csv(os.path.join(here, "cs16", "merchant_profile.csv.gz"), index=False)
    ln.to_csv(os.path.join(here, "cs16", "loans.csv.gz"), index=False); nm.to_csv(os.path.join(here, "cs16", "name_pairs.csv.gz"), index=False)
    print(len(mm), "merchant-months |", len(ln), "loans | default", ln.default_30d_missed.mean().round(4), "| burden median", ln._burden_true.median().round(3))
    print(nm.groupby("_variant")._is_same_person.agg(["mean", "size"]))
    print(nm.sample(8, random_state=1)[["kyc_name", "bank_account_name", "_variant"]])
