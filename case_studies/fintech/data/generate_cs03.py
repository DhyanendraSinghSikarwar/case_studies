"""
SYNTHETIC DATA GENERATOR - CASE STUDY 3 (Razorpay Vulcan-style shared payment representation, 4 tasks)
=====================================================================================================
THIS DATA IS SYNTHETIC. Payment-gateway logs are confidential.

One payment = a set of fields (customer, device, merchant, pincode, method, issuer, gateway, amount, time).
A hidden customer SEGMENT (K = 6) drives which merchants people buy from, where they live, which
methods they prefer and how risky their COD parcels are. Co-occurrence of fields therefore carries
information that a self-supervised representation can pick up without labels.

Four labelled tasks share the same payments:
  1. route_success - online payment succeeded on the (randomly logged) gateway G1/G2/G3
  2. is_fraud      - chargeback / confirmed fraud; label arrives 5-60 days later (label_date)
  3. rto           - COD parcel returned to origin (COD orders only)
  4. method        - payment method the shopper chose (checkout ordering)
Fraud has a ring that changes targets mid-period (concept drift) - why out-of-time tests matter.

Calibration anchors (reference file, Case Study 3): fraud labels "confirmed weeks later";
evaluation "out-of-time, per payment flow"; "fixed alert volumes"; calibration evaluated separately.
Rates are our assumptions (decision.md D-3-02). Hidden truth columns start with "_".

Output: data/cs03/payments.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.special import expit, softmax

SEED = 42
START = pd.Timestamp("2026-01-05"); DAYS = 84
K = 6
METHODS = ["upi", "card", "netbanking", "wallet", "cod"]
CATS = ["fashion", "electronics", "grocery", "home", "food", "travel", "digital_goods", "education"]
COD_OK = {"fashion", "electronics", "grocery", "home"}
BANKS = [f"B{i:02d}" for i in range(20)]
GWS = ["G1", "G2", "G3"]


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    # ---------- entities ----------
    seg_p = np.array([0.24, 0.20, 0.18, 0.15, 0.13, 0.10])
    n_cust, n_merch, n_pin = 40_000, 1_500, 600
    pin_seg = rng.integers(0, K, n_pin)
    pin_risk = np.array([-0.8, -0.4, 0.0, 0.3, 0.6, 0.9])[pin_seg] + rng.normal(0, 0.5, n_pin)
    m_seg = rng.integers(0, K, n_merch)
    m_cat = rng.choice(CATS, n_merch, p=[0.20, 0.14, 0.14, 0.10, 0.14, 0.08, 0.12, 0.08])
    m_pop = rng.gamma(0.8, 1.0, n_merch)
    c_seg = rng.choice(K, n_cust, p=seg_p)
    c_pin = np.array([rng.choice(np.flatnonzero(pin_seg == s)) for s in c_seg])
    seg_meth = np.array([[1.6, 0.4, -0.4, 0.2, -0.6], [1.2, 0.9, 0.2, -0.3, -1.2], [1.0, -0.2, -0.6, 0.4, 0.6],
                         [0.6, -0.6, -0.8, 0.0, 1.3], [0.4, 1.4, 0.6, -0.4, -1.0], [1.4, -0.4, -1.0, 0.9, 0.3]])
    c_meth = seg_meth[c_seg] + rng.normal(0, 0.8, (n_cust, 5))
    seg_bank = rng.dirichlet(np.ones(len(BANKS)) * 0.6, K)
    c_bank = np.array([rng.choice(len(BANKS), p=seg_bank[s]) for s in c_seg])
    c_rto = rng.normal(0, 0.7, n_cust)
    c_dev = np.array([f"D{i:06d}" for i in range(n_cust)])
    second = rng.random(n_cust) < 0.12
    c_dev2 = np.where(second, [f"D{i + 500000:06d}" for i in range(n_cust)], c_dev)
    n_pay = rng.poisson(rng.gamma(1.5, 5.0, n_cust)) + 1
    # ---------- legit payments ----------
    ci = np.repeat(np.arange(n_cust), n_pay); N = len(ci)
    seg = c_seg[ci]
    own = rng.random(N) < 0.70
    m_by_seg = [np.flatnonzero(m_seg == s) for s in range(K)]
    w_by_seg = [m_pop[m] / m_pop[m].sum() for m in m_by_seg]
    merch = np.empty(N, int)
    for s in range(K):
        idx = np.flatnonzero(own & (seg == s)); merch[idx] = rng.choice(m_by_seg[s], len(idx), p=w_by_seg[s])
    idx = np.flatnonzero(~own); merch[idx] = rng.choice(n_merch, len(idx), p=m_pop / m_pop.sum())
    cat = m_cat[merch]
    amt = np.round(np.exp(rng.normal(np.log(650), 0.9, N) + 0.6 * np.isin(cat, ["electronics", "travel"]) - 0.4 * (cat == "food")), 0)
    ts = START + pd.to_timedelta(rng.uniform(0, DAYS * 86400, N), unit="s")
    hour = pd.DatetimeIndex(ts).hour.to_numpy()
    lg = c_meth[ci] + np.c_[np.zeros(N), 0.35 * np.log(amt / 650), np.zeros(N), -0.3 * np.log(amt / 650), np.zeros(N)]
    lg[~np.isin(cat, list(COD_OK)), 4] = -np.inf
    P = softmax(lg, axis=1); u = rng.random(N)[:, None]
    meth = np.array(METHODS)[(P.cumsum(1) < u).sum(1).clip(0, 4)]
    dev = np.where(rng.random(N) < 0.85, c_dev[ci], c_dev2[ci])
    pay = pd.DataFrame({"ts": ts, "customer_id": [f"C{i:06d}" for i in ci], "device_id": dev, "merchant_id": [f"M{m:05d}" for m in merch],
                        "merchant_cat": cat, "pincode": [f"PIN{p:04d}" for p in c_pin[ci]], "method": meth, "amount_inr": amt,
                        "_segment": seg, "_cidx": ci, "_ring": 0})
    pay["issuer"] = np.where(pay.method.isin(["card", "netbanking", "upi"]), np.array(BANKS)[c_bank[ci]], "none")
    # ---------- fraud ring (A: weeks 1-8 digital goods/electronics; B: weeks 7-12 travel/new merchants) ----------
    rings = []
    for name, d0, d1, cats_, ndev in (("A", 0, 56, ["digital_goods", "electronics"], 30), ("B", 42, 84, ["travel", "digital_goods"], 30)):
        targets = rng.choice(np.flatnonzero(np.isin(m_cat, cats_)), 25, replace=False)
        for d in range(ndev):
            dv = f"RD{name}{d:03d}"; t0 = rng.uniform(d0, d1 - 7) * 86400
            for c in range(rng.integers(4, 12)):
                cid = f"CR{name}{d:03d}{c:02d}"; pin = rng.integers(n_pin)
                for _ in range(rng.integers(1, 3)):
                    rings.append((START + pd.Timedelta(seconds=t0 + rng.uniform(0, 7 * 86400)), cid, dv, f"M{rng.choice(targets):05d}", pin,
                                  rng.choice(["card", "upi"], p=[0.75, 0.25]), float(np.round(np.exp(rng.normal(np.log(3500), 0.5)))), name))
    r = pd.DataFrame(rings, columns=["ts", "customer_id", "device_id", "merchant_id", "pin", "method", "amount_inr", "_ring"])
    r["merchant_cat"] = m_cat[r.merchant_id.str[1:].astype(int)]; r["pincode"] = [f"PIN{p:04d}" for p in r.pin]
    r["issuer"] = rng.choice(BANKS, len(r)); r["_segment"] = -1; r["_cidx"] = -1
    pay = pd.concat([pay, r.drop(columns="pin")], ignore_index=True)
    N = len(pay); hour = pay.ts.dt.hour.to_numpy(); is_ring = pay._ring.astype(str).isin(["A", "B"]).to_numpy()
    pay["card_network"] = np.where(pay.method == "card", rng.choice(["Visa", "Mastercard", "RuPay"], N, p=[0.5, 0.33, 0.17]), "none")
    intl = (pay.method == "card") & (rng.random(N) < np.where(is_ring, 0.6, 0.02))
    pay["bin_country"] = np.where(pay.method == "card", np.where(intl, "international", "domestic"), "none")
    # ---------- task 2: fraud ----------
    night = (hour <= 4).astype(float)
    z_f = (-7.6 + 0.9 * np.log(pay.amount_inr / 650).clip(0) + 1.2 * night + 1.5 * intl + 0.8 * (pay.merchant_cat == "digital_goods")
           + 0.5 * pay.device_id.str.startswith("D5").astype(float))                       # second (newer) device
    p_f = np.where(is_ring, 0.75, expit(z_f))
    pay["_p_fraud"] = p_f; pay["is_fraud"] = (rng.random(N) < p_f).astype(int)
    pay["label_date"] = pd.NaT
    fr = pay.is_fraud == 1
    pay.loc[fr, "label_date"] = pay.loc[fr, "ts"] + pd.to_timedelta(np.exp(rng.normal(np.log(21), 0.6, fr.sum())).clip(3, 75), unit="D")
    # ---------- task 1: route success (online methods; gateway randomly logged) ----------
    online = pay.method != "cod"
    gw = rng.choice(GWS, N); pay["gateway"] = np.where(online, gw, "none")
    bank_i = pay.issuer.map({b: i for i, b in enumerate(BANKS)}).fillna(-1).astype(int).to_numpy()
    gx = rng.normal(0, 0.55, (len(BANKS) + 1, 3)); gx[-1] = 0
    base = pay.method.map({"upi": 1.7, "card": 1.9, "netbanking": 1.6, "wallet": 2.6, "cod": 0}).to_numpy()
    peak = ((hour >= 19) & (hour <= 22)).astype(float)
    netw = pay.card_network.map({"Visa": 0.0, "Mastercard": 0.1, "RuPay": -0.2, "none": 0}).to_numpy()
    seg_sr = np.r_[np.array([0.2, 0.1, 0.0, -0.2, 0.1, -0.1]), 0.0][pay._segment.to_numpy()]
    p_g = np.zeros((N, 3))
    for g in range(3):
        p_g[:, g] = expit(base + gx[bank_i, g] + [0.0, 0.15, -0.1][g] - [0.0, 0.5, 0.1][g] * peak + (g == 2) * 0.4 * (netw < 0) + seg_sr - 0.3 * intl)
        pay[f"_p_{GWS[g]}"] = np.where(online, p_g[:, g], np.nan)
    gi = pd.Series(gw).map({g: i for i, g in enumerate(GWS)}).to_numpy()
    pay["route_success"] = np.where(online, (rng.random(N) < p_g[np.arange(N), gi]).astype(float), np.nan)
    # ---------- task 3: RTO on COD ----------
    pin_i = pay.pincode.str[3:].astype(int).to_numpy()
    cidx = pay._cidx.to_numpy()
    z_r = (-1.5 + pin_risk[pin_i] + np.where(cidx >= 0, c_rto[cidx.clip(0)], 0.8) + 0.45 * (pay.merchant_cat == "fashion")
           + 0.3 * np.log(pay.amount_inr / 650))
    pay["_p_rto"] = np.where(pay.method == "cod", expit(z_r), np.nan)
    pay["rto"] = np.where(pay.method == "cod", (rng.random(N) < expit(z_r)).astype(float), np.nan)
    # ---------- tidy + data-quality defects ----------
    pay = pay.sort_values("ts").reset_index(drop=True)
    pay.insert(0, "payment_id", [f"PAY{i:08d}" for i in range(1, len(pay) + 1)])
    pay.loc[pay.sample(frac=0.015, random_state=seed).index, "pincode"] = np.nan          # missing pincode (digital orders)
    pay.loc[pay.sample(n=400, random_state=seed + 1).index, "amount_inr"] = 0              # zero-amount test pings
    pay = pd.concat([pay, pay.sample(n=900, random_state=seed + 2)], ignore_index=True)   # duplicate webhook rows
    pay["_ring"] = pay["_ring"].astype(str)
    return pay


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs03"), exist_ok=True)
    d = generate(); d.to_csv(os.path.join(here, "cs03", "payments.csv.gz"), index=False)
    print(len(d), "rows"); dd = d.drop_duplicates("payment_id")
    print(dd.method.value_counts(normalize=True).round(3).to_dict())
    print("fraud", dd.is_fraud.mean().round(5), dd.is_fraud.sum(), "| by ring", dd.groupby("_ring").is_fraud.sum().to_dict())
    print("route SR", dd.route_success.mean().round(3), "| RTO", dd.rto.mean().round(3), dd.rto.notna().sum())
