"""
SYNTHETIC DATA GENERATOR - CASE STUDY 7 (Cashfree RiskShield-style real-time fraud screening)
=============================================================================================
THIS DATA IS SYNTHETIC. Merchant transaction and fraud logs are confidential.

8 weeks of card/UPI checkout transactions at merchants in three business lines
(online gaming, e-commerce, ed-tech subscriptions), screened in real time. Fraud types:
  * card_testing  - bots try many stolen cards in minutes with tiny amounts (datacenter IPs)
  * stolen_card   - high-value purchases on stolen cards; rings share devices/IPs; geo mismatch;
                    confirmed by chargeback 10-60 days later
  * promo_abuse   - one person creates many new accounts on a few devices with disposable
                    emails/phones to farm sign-up offers
Seven signal groups (as documented): negative lists, contact intelligence (disposable phone/email),
device intelligence (emulator, device age), geo/IP, anomaly scores, velocity, graph links.
Negative lists are partial (only some fraudsters listed) and stale (some legitimate users listed).

Calibration anchors (reference file, Case Study 7): fraud types "UPI collect-request scams,
chargeback fraud and promotion abuse"; velocity ">X distinct mobile numbers or devices within Y time";
rules "tuned by the merchant's line of business and transaction size"; no impact numbers disclosed.
Rates are our assumptions (decision.md D-7-02). Hidden columns start with "_".

Output: data/cs07/transactions.csv.gz
"""
import os
import numpy as np
import pandas as pd

SEED = 42
START = pd.Timestamp("2026-03-02"); DAYS = 56
LINES = ["gaming", "ecommerce", "edtech"]
STATES = ["MH", "KA", "DL", "TN", "TG", "UP", "GJ", "WB", "RJ", "KL"]


def _ts(rng, n, d0=0, d1=DAYS):
    day = rng.uniform(d0, d1, n); hr = rng.choice(24, n, p=np.r_[[0.6] * 6, [3] * 4, [5] * 8, [6] * 4, [2] * 2] / np.r_[[0.6] * 6, [3] * 4, [5] * 8, [6] * 4, [2] * 2].sum())
    return START + pd.to_timedelta(np.floor(day) * 86400 + hr * 3600 + rng.uniform(0, 3600, n), unit="s")


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    rows = []
    # ---------------- legitimate customers ----------------
    n_c = 60_000
    line_c = rng.choice(LINES, n_c, p=[0.3, 0.5, 0.2]); st = rng.choice(STATES, n_c)
    disp = rng.random(n_c) < 0.03
    k = rng.poisson(rng.gamma(1.2, 3.0, n_c)) + 1
    ci = np.repeat(np.arange(n_c), k); N = len(ci)
    first = np.r_[1, (np.diff(ci) != 0).astype(int)]
    ts = _ts(rng, N)
    cid = np.array([f"{i:06d}" for i in range(n_c)])[ci]
    hh = rng.random(n_c) < 0.08                                                            # households sharing a phone/laptop
    hh_of = np.where(hh, np.maximum(np.arange(n_c) - rng.integers(1, 4, n_c), 0), np.arange(n_c))
    hh_cid = np.array([f"{i:06d}" for i in range(n_c)])[hh_of][ci]
    second_card = (rng.random(n_c) < 0.2)[ci]
    leg = pd.DataFrame({"ts": ts, "customer_id": np.char.add("C", cid), "business_line": line_c[ci],
                        "device_id": np.where(rng.random(N) < 0.1, np.char.add(np.char.add("D", cid), "b"), np.char.add("D", hh_cid)),
                        "ip": np.where(rng.random(N) < 0.7, [f"IP{i % 9000:05d}" for i in ci], [f"IPM{x:06d}" for x in rng.integers(0, 400000, N)]),
                        "ip_type": np.where(rng.random(N) < 0.97, "residential_or_mobile", "datacenter_or_vpn"),
                        "ip_state": np.where(rng.random(N) < 0.80, st[ci], rng.choice(STATES, N)), "bin_state": st[ci],
                        "card_hash": np.where(second_card & (rng.random(N) < 0.5), np.char.add(np.char.add("K", cid), "x"), np.char.add("K", cid)),
                        "phone_hash": np.char.add("P", cid), "email_type": np.where(disp[ci], "disposable", "regular"),
                        "emulator": (rng.random(N) < 0.006).astype(int),
                        "device_age_days": np.where(rng.random(N) < 0.15, rng.uniform(0, 30, N), np.maximum(0, rng.normal(250, 150, N))).round(),
                        "new_account": first, "promo_used": (rng.random(N) < np.where(first == 1, 0.35, 0.06)).astype(int),
                        "amount_inr": np.round(np.exp(rng.normal(pd.Series(line_c[ci]).map({"gaming": np.log(350), "ecommerce": np.log(1100), "edtech": np.log(2600)}).to_numpy(), 0.8))),
                        "_type": "legit"})
    verify = rng.random(N) < 0.03                                                          # Rs 1 mandate / card verification charges
    leg.loc[verify, "amount_inr"] = rng.choice([1.0, 2.0, 5.0], verify.sum())
    # first transaction of each customer happens first in time
    leg["ts"] = leg.groupby("customer_id").ts.transform(np.sort)
    # ---------------- card-testing bots ----------------
    ct = []
    for b in range(45):
        t0 = _ts(rng, 1)[0]; ncard = rng.integers(15, 60); dev = f"BOT{b:03d}"; ip = f"IPDC{b % 15:03d}"
        line = rng.choice(["gaming", "ecommerce"], p=[0.6, 0.4]); proxy = rng.random() < 0.4; big = rng.random() < 0.3
        ct.append(pd.DataFrame({"ts": t0 + pd.to_timedelta(np.sort(rng.uniform(0, rng.uniform(900, 5400), ncard)), unit="s"),
                                "customer_id": [f"CT{b:03d}_{j:02d}" for j in range(ncard)], "business_line": line, "device_id": dev, "ip": ip,
                                "ip_type": "residential_or_mobile" if proxy else "datacenter_or_vpn", "ip_state": rng.choice(STATES), "bin_state": rng.choice(STATES, ncard),
                                "card_hash": [f"KS{b:03d}{j:02d}" for j in range(ncard)], "phone_hash": f"PB{b:03d}", "email_type": rng.choice(["regular", "disposable"]),
                                "emulator": int(rng.random() < 0.5), "device_age_days": 0.0, "new_account": 1, "promo_used": 0,
                                "amount_inr": (rng.choice([99, 149, 199, 499], ncard) if big else rng.choice([1, 2, 5, 10, 49], ncard)).astype(float), "_type": "card_testing"}))
    # ---------------- stolen-card rings ----------------
    sc = []
    for r in range(18):
        devs = [f"RDEV{r:02d}{j}" for j in range(3)]; ips = [f"IPR{r:02d}{j}" for j in range(4)]; t_ring = rng.uniform(0, DAYS - 10)
        for a in range(rng.integers(6, 14)):
            n = rng.integers(2, 7); ts = _ts(rng, n, t_ring, min(DAYS, t_ring + 14))
            sc.append(pd.DataFrame({"ts": ts, "customer_id": f"SC{r:02d}_{a:02d}", "business_line": rng.choice(LINES, p=[0.25, 0.45, 0.3]),
                                    "device_id": rng.choice(devs, n), "ip": np.where(rng.random(n) < 0.6, [f"IP{x:05d}" for x in rng.integers(0, 9000, n)], rng.choice(ips, n)), "ip_type": np.where(rng.random(n) < 0.45, "datacenter_or_vpn", "residential_or_mobile"),
                                    "ip_state": "SAME", "bin_state": rng.choice(STATES), "card_hash": [f"KR{r:02d}{a:02d}{x}" for x in rng.integers(0, 3, n)],
                                    "phone_hash": f"PR{r:02d}{a:02d}", "email_type": "disposable" if rng.random() < 0.4 else "regular",
                                    "emulator": (rng.random(n) < 0.15).astype(int), "device_age_days": rng.integers(0, 200, n).astype(float), "new_account": np.r_[1, np.zeros(n - 1, int)],
                                    "promo_used": 0, "amount_inr": np.round(np.exp(rng.normal(np.log(3000), 0.9, n))), "_type": "stolen_card"}))
    # lone stolen-card fraudsters (no ring)
    for a in range(250):
        n = rng.integers(1, 4); ts = _ts(rng, n)
        sc.append(pd.DataFrame({"ts": ts, "customer_id": f"SL{a:03d}", "business_line": rng.choice(LINES, p=[0.25, 0.45, 0.3]),
                                "device_id": f"LDEV{a:03d}", "ip": f"IP{rng.integers(0, 9000):05d}" if rng.random() < 0.6 else f"IPL{a:03d}", "ip_type": np.where(rng.random(n) < 0.3, "datacenter_or_vpn", "residential_or_mobile"),
                                "ip_state": "SAME", "bin_state": rng.choice(STATES), "card_hash": f"KL{a:03d}", "phone_hash": f"PL{a:03d}",
                                "email_type": "disposable" if rng.random() < 0.25 else "regular", "emulator": 0, "device_age_days": rng.integers(0, 365, n).astype(float),
                                "new_account": np.r_[1, np.zeros(n - 1, int)], "promo_used": 0, "amount_inr": np.round(np.exp(rng.normal(np.log(2500), 0.9, n))), "_type": "stolen_card"}))
    # ---------------- promo abusers ----------------
    pa = []
    for u in range(110):
        ndev = rng.integers(2, 4); t0 = rng.uniform(0, DAYS - 7); line = rng.choice(["ecommerce", "gaming"], p=[0.65, 0.35])
        for a in range(rng.integers(3, 13)):
            pa.append(pd.DataFrame({"ts": _ts(rng, 1, t0, t0 + 7), "customer_id": f"PA{u:03d}_{a:02d}", "business_line": line,
                                    "device_id": f"PDEV{u:03d}{rng.integers(ndev)}", "ip": f"IP{rng.integers(0, 9000):05d}" if rng.random() < 0.5 else f"IPP{u:03d}",
                                    "ip_type": "residential_or_mobile", "ip_state": rng.choice(STATES), "bin_state": rng.choice(STATES),
                                    "card_hash": f"KP{u:03d}{rng.integers(3)}", "phone_hash": f"PP{u:03d}{a:02d}", "email_type": "disposable" if rng.random() < 0.5 else "regular",
                                    "emulator": int(rng.random() < 0.15), "device_age_days": float(rng.integers(5, 400)), "new_account": 1, "promo_used": int(rng.random() < 0.85),
                                    "amount_inr": float(np.round(np.exp(rng.normal(np.log(450), 0.4)))), "_type": "promo_abuse"}))
    df = pd.concat([leg] + ct + sc + pa, ignore_index=True)
    df["is_fraud"] = (df._type != "legit").astype(int)
    same = df.ip_state == "SAME"                                                          # fraudsters on same-state proxies half the time
    df.loc[same, "ip_state"] = np.where(rng.random(same.sum()) < 0.5, df.loc[same, "bin_state"], rng.choice(STATES, same.sum()))
    n = len(df)
    # outcome of the payment attempt (card testing mostly declined)
    p_ok = np.where(df._type == "card_testing", 0.15, np.where(df._type == "stolen_card", 0.8, 0.95))
    df["payment_status"] = np.where(rng.random(n) < p_ok, "success", "declined")
    # label arrival: chargebacks late; card testing / promo abuse found by investigation within days
    delay = np.where(df._type == "stolen_card", rng.uniform(10, 60, n), rng.uniform(1, 5, n))
    df["label_date"] = np.where(df.is_fraud == 1, df.ts + pd.to_timedelta(delay, unit="D"), pd.NaT)
    df["label_date"] = pd.to_datetime(df.label_date)
    # negative lists: 25% of fraud actors' phone or device listed beforehand; 0.25% of legit phones listed (stale)
    actors = df[df.is_fraud == 1].customer_id.str.split("_").str[0].unique()
    listed_actor = set(rng.choice(actors, int(0.25 * len(actors)), replace=False))
    legit_ph = df.loc[df.is_fraud == 0, "phone_hash"].unique()
    listed_ph = set(rng.choice(legit_ph, int(0.0025 * len(legit_ph)), replace=False))
    df["negative_list_hit"] = (df.customer_id.str.split("_").str[0].isin(listed_actor) | df.phone_hash.isin(listed_ph)).astype(int)
    df["phone_type"] = np.where((df.is_fraud == 1) & (rng.random(n) < 0.35), "virtual_or_disposable", np.where(rng.random(n) < 0.02, "virtual_or_disposable", "regular"))
    df["merchant_id"] = [f"{l[:2].upper()}{m:03d}" for l, m in zip(df.business_line, rng.integers(0, 40, n))]
    df = df.sort_values("ts").reset_index(drop=True)
    df.insert(0, "txn_id", [f"T{i:08d}" for i in range(1, n + 1)])
    # data-quality defects
    df.loc[df.sample(frac=0.01, random_state=seed).index, "device_id"] = np.nan                # SDK did not send device id
    df = pd.concat([df, df.sample(n=800, random_state=seed + 1)], ignore_index=True)           # duplicate events from retries
    df.loc[df.sample(n=150, random_state=seed + 2).index, "amount_inr"] = -df.amount_inr         # sign error (refund rows mis-tagged)
    return df


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs07"), exist_ok=True)
    d = generate(); d.to_csv(os.path.join(here, "cs07", "transactions.csv.gz"), index=False)
    dd = d.drop_duplicates("txn_id")
    print(len(dd), "txns", dd.customer_id.nunique(), "customers | fraud rate", dd.is_fraud.mean().round(4))
    print(dd.groupby("_type").size().to_dict()); print(dd.groupby("business_line").is_fraud.mean().round(4).to_dict())
    print("neg list hit rate fraud/legit", dd.groupby("is_fraud").negative_list_hit.mean().round(4).to_dict())
