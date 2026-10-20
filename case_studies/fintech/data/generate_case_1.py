"""
SYNTHETIC DATA GENERATOR - CASE 1 (Juspay-style dynamic gateway routing)
=======================================================================
THIS DATA IS SYNTHETIC. No public gateway-level routing dataset exists, so we
simulate 30 days of Indian e-commerce payments routed by today's fixed rules.

Calibration anchors (from the reference file, Case Study 1 and 2):
  * rule-based success rate (SR) ~ 82.6%  (Juspay 21-day avg: 82.60% rules vs 83.19% dynamic)
  * gateway SR gaps of ~1 percentage point (paper toy example: 80% vs 81%)
  * one ~2.5-hour gateway outage (Juspay: 2.5-hour outage, ~8,000 txns rerouted)
  * failure split authentication vs authorisation, with the cheaper processor
    losing more at authentication (Cashfree Case Study 2)
Everything else (shares, effect sizes, festive dates) is our own assumption and
is logged in decision.md (D-1-02 ... D-1-08).

Usage:  python data/generate_case_1.py   -> writes data/case1_transactions_raw.csv.gz
The function `success_probability()` is the hidden "ground truth" and is re-used
by the notebook's routing simulation (a digital twin of the gateways).
"""
import numpy as np
import pandas as pd
from scipy.special import expit, logit

SEED = 42
START = pd.Timestamp("2025-10-01")          # Navratri -> Dussehra -> Diwali month
DAYS = 30
TARGET_TXNS = 420_000

GATEWAYS = ["PG_A", "PG_B", "PG_C", "PG_D"]
METHOD_SHARE = {"UPI": 0.55, "Card": 0.28, "Netbanking": 0.10, "Wallet": 0.07}
BANK_SHARE = {"SBI": 0.25, "HDFC": 0.22, "ICICI": 0.18, "Axis": 0.12, "Kotak": 0.08, "Others": 0.15}
NETWORK_SHARE = {"Visa": 0.45, "Mastercard": 0.30, "RuPay": 0.25}
N_MERCHANTS = 120

# Today's fixed routing rules: traffic split per payment method (PG_D is the cheap
# processor, so cost-driven rules push a large share of cards to it).
RULES = {
    "UPI":        [0.40, 0.35, 0.15, 0.10],
    "Card":       [0.30, 0.25, 0.15, 0.30],
    "Netbanking": [0.25, 0.20, 0.40, 0.15],
    "Wallet":     [0.35, 0.30, 0.20, 0.15],
}

# ---- success model (log-odds scale) ---------------------------------------
METHOD_BASE = {"UPI": logit(0.855), "Card": logit(0.795), "Netbanking": logit(0.810), "Wallet": logit(0.893)}
BANK_EFFECT = {"SBI": -0.08, "HDFC": 0.06, "ICICI": 0.05, "Axis": 0.00, "Kotak": 0.03, "Others": -0.12}
NETWORK_EFFECT = {"Visa": 0.03, "Mastercard": 0.00, "RuPay": -0.06}
GATEWAY_EFFECT = {"PG_A": 0.08, "PG_B": 0.05, "PG_C": 0.00, "PG_D": -0.10}
GW_METHOD = {("PG_D", "Card"): -0.22, ("PG_C", "Netbanking"): 0.25, ("PG_B", "UPI"): 0.06,
             ("PG_A", "Wallet"): 0.10}
GW_BANK = {("PG_B", "SBI"): 0.30, ("PG_B", "HDFC"): -0.22, ("PG_C", "HDFC"): 0.28,
           ("PG_C", "ICICI"): 0.18, ("PG_A", "Kotak"): -0.25, ("PG_D", "Axis"): 0.22,
           ("PG_A", "Others"): -0.10, ("PG_D", "Others"): 0.12}
FESTIVE = {"2025-10-01": 1.35, "2025-10-02": 1.45, "2025-10-18": 1.90,
           "2025-10-19": 1.60, "2025-10-20": 1.75, "2025-10-21": 1.50}
OUTAGE = {"gateway": "PG_B", "start": pd.Timestamp("2025-10-17 19:00"),
          "end": pd.Timestamp("2025-10-17 21:30"), "logodds_drop": 2.5}
# hourly volume profile (Indian e-commerce: quiet night, lunch and late-evening peaks)
HOUR_PROFILE = np.array([0.35, 0.22, 0.15, 0.12, 0.12, 0.18, 0.35, 0.60, 0.85, 1.00, 1.10, 1.20,
                         1.30, 1.25, 1.10, 1.05, 1.05, 1.10, 1.25, 1.45, 1.60, 1.65, 1.40, 0.85])

MERCHANT_EFFECT = np.random.default_rng(SEED).normal(0, 0.15, N_MERCHANTS)


def hour_effect(hour):
    """Night-time issuer maintenance windows hurt SR; evening peak adds load."""
    h = np.asarray(hour)
    return np.select([(h >= 0) & (h < 5), (h >= 19) & (h < 23)], [-0.25, -0.05], 0.0)


def success_probability(df, gateway):
    """Ground-truth P(success) for each row of `df` if routed to `gateway` (array-like)."""
    gw = np.asarray(gateway)
    ts = pd.to_datetime(df["timestamp"])
    method = df["payment_method"].to_numpy()
    bank = df["issuer_bank"].fillna("NA").to_numpy()
    z = np.array(df["payment_method"].map(METHOD_BASE), dtype=float)  # explicit writable copy
    z += pd.Series(bank).map(BANK_EFFECT).fillna(0).to_numpy()
    z += df["card_network"].map(NETWORK_EFFECT).fillna(0).to_numpy()
    z += pd.Series(gw).map(GATEWAY_EFFECT).to_numpy()
    z += np.array([GW_METHOD.get((g, m), 0.0) for g, m in zip(gw, method)])
    z += np.array([GW_BANK.get((g, b), 0.0) for g, b in zip(gw, bank)])
    z += MERCHANT_EFFECT[df["merchant_id"].str[2:].astype(int).to_numpy() - 1]
    z += hour_effect(ts.dt.hour.to_numpy())
    festive = ts.dt.strftime("%Y-%m-%d").isin(list(FESTIVE)).to_numpy()
    z -= festive * (0.12 + 0.10 * (method == "Card"))
    z -= 0.10 * np.clip(np.log10(df["amount_inr"].abs().clip(lower=1).to_numpy()) - 4, 0, None)
    in_outage = (gw == OUTAGE["gateway"]) & (ts >= OUTAGE["start"]).to_numpy() & (ts < OUTAGE["end"]).to_numpy()
    z -= in_outage * OUTAGE["logodds_drop"]
    return expit(z)


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    # 1) volume: Poisson arrivals per hour with festive and weekend multipliers
    hours = pd.date_range(START, periods=DAYS * 24, freq="h")
    day_mult = np.array([FESTIVE.get(h.strftime("%Y-%m-%d"), 1.0) * (1.10 if h.dayofweek >= 5 else 1.0) for h in hours])
    lam = HOUR_PROFILE[hours.hour] * day_mult
    lam = lam / lam.sum() * TARGET_TXNS
    counts = rng.poisson(lam)
    ts = np.repeat(hours.values, counts) + pd.to_timedelta(rng.uniform(0, 3600, counts.sum()), unit="s").values
    n = len(ts)

    # 2) transaction attributes
    method = rng.choice(list(METHOD_SHARE), n, p=list(METHOD_SHARE.values()))
    bank = rng.choice(list(BANK_SHARE), n, p=list(BANK_SHARE.values())).astype(object)
    bank[method == "Wallet"] = np.nan                                  # structural: no issuer bank
    network = np.full(n, np.nan, dtype=object)
    is_card = method == "Card"
    network[is_card] = rng.choice(list(NETWORK_SHARE), is_card.sum(), p=list(NETWORK_SHARE.values()))
    mw = 1 / np.arange(1, N_MERCHANTS + 1) ** 0.8                      # Zipf-like merchant sizes
    merchant = np.array([f"M_{i:03d}" for i in range(1, N_MERCHANTS + 1)])[rng.choice(N_MERCHANTS, n, p=mw / mw.sum())]
    median = pd.Series(method).map({"UPI": 450, "Card": 1800, "Netbanking": 3500, "Wallet": 250}).to_numpy()
    sigma = pd.Series(method).map({"UPI": 1.10, "Card": 1.00, "Netbanking": 1.10, "Wallet": 0.90}).to_numpy()
    amount = np.round(median * np.exp(rng.normal(0, sigma)), 2)
    bulk = rng.random(n) < 0.0005                                      # rare B2B bulk orders (outliers)
    amount[bulk] *= 50

    df = pd.DataFrame({"timestamp": ts, "merchant_id": merchant, "payment_method": method,
                       "card_network": network, "issuer_bank": bank, "amount_inr": amount})
    # 3) routing by today's fixed rules
    gw = np.empty(n, dtype=object)
    for m, w in RULES.items():
        idx = np.where(method == m)[0]
        gw[idx] = rng.choice(GATEWAYS, len(idx), p=w)
    df["gateway"] = gw

    # 4) outcome, failure stage and latency
    p = success_probability(df, gw)
    df["success"] = (rng.random(n) < p).astype(int)
    auth_share = pd.Series(method).map({"UPI": 0.45, "Card": 0.55, "Netbanking": 0.60, "Wallet": 0.40}).to_numpy()
    auth_share = np.where((gw == "PG_D") & is_card, 0.78, auth_share)   # weak 3DS/ACS on cheap PG
    in_outage = (gw == OUTAGE["gateway"]) & (df["timestamp"] >= OUTAGE["start"]) & (df["timestamp"] < OUTAGE["end"])
    auth_share = np.where(in_outage, 0.10, auth_share)                  # outage = downstream timeouts
    stage = np.where(rng.random(n) < auth_share, "authentication", "authorisation")
    df["failure_stage"] = np.where(df["success"] == 1, "none", stage)
    lat_med = pd.Series(gw).map({"PG_A": 850, "PG_B": 950, "PG_C": 1100, "PG_D": 1300}).to_numpy()
    latency = lat_med * np.exp(rng.normal(0, 0.45, n)) * np.where(df["success"] == 1, 1.0, 1.3) * np.where(in_outage, 4.0, 1.0)
    df["latency_ms"] = np.round(latency).astype(float)

    df = df.sort_values("timestamp").reset_index(drop=True)
    df.insert(0, "txn_id", [f"T{i:08d}" for i in range(1, len(df) + 1)])

    # 5) realistic messiness / data-quality issues (to be detected in the notebook)
    dup = df.sample(frac=0.006, random_state=seed).copy()               # webhook replays -> duplicate txn_id
    dup["timestamp"] = dup["timestamp"] + pd.to_timedelta(rng.integers(1, 30, len(dup)), unit="s")
    df = pd.concat([df, dup], ignore_index=True)
    df.loc[df.sample(n=40, random_state=seed + 1).index, "amount_inr"] = 0.0     # test txns
    neg = df.sample(n=15, random_state=seed + 2).index
    df.loc[neg, "amount_inr"] = -df.loc[neg, "amount_inr"]                        # refund reversals mis-logged
    df.loc[df.sample(n=25, random_state=seed + 3).index, "timestamp"] = pd.Timestamp("1970-01-01")  # clock reset
    card_idx = df.index[df["payment_method"] == "Card"]
    df.loc[rng.choice(card_idx, int(0.01 * len(card_idx)), replace=False), "card_network"] = np.nan
    df.loc[df.sample(frac=0.015, random_state=seed + 4).index, "latency_ms"] = np.nan  # logging gap
    df = df.sort_values("timestamp", kind="stable").reset_index(drop=True)
    return df[["txn_id", "timestamp", "merchant_id", "payment_method", "card_network", "issuer_bank",
               "amount_inr", "gateway", "success", "failure_stage", "latency_ms"]]


if __name__ == "__main__":
    import os
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "case1_transactions_raw.csv.gz")
    data = generate()
    data.to_csv(out, index=False)
    print(f"wrote {len(data):,} rows -> {out}; raw SR = {data['success'].mean():.4f}")
