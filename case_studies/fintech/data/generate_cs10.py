"""
SYNTHETIC DATA GENERATOR - CASE STUDY 10 (Simpl-style BNPL fraud rings found with graph communities)
====================================================================================================
THIS DATA IS SYNTHETIC. BNPL user and transaction data are confidential.

A checkout-credit (BNPL) provider onboards users over 13 weeks. Each user has identity attributes
(device, phone, email, delivery address, IP block, repayment bank account). Genuine users share some
attributes naturally (families share devices/addresses; hostels, PGs and offices are address HUBS
shared by dozens of unrelated people; carrier IP blocks are shared by thousands).
Fraud:
  * RINGS (bust-out / synthetic identity): groups of 4-40 accounts created by one gang, re-using a
    few devices, addresses, email patterns and bank accounts; they max out their limits within days
    and never repay. A ring is invisible one account at a time and obvious as a group.
  * Lone first-party fraud and account takeover (ATO): individual, no links.
Outcome observed by the lender: FIRST-PAYMENT DEFAULT (FPD) - not paid 30 days after the first due date.
FPD mixes fraud (intent never to pay) with genuine credit stress (~3% of good users).

Calibration anchors (reference file, Case Study 10): Simpl serves "26,000+ merchants"; fraud includes
"account takeover and identity theft"; "graph ML to find fraud communities"; real-time SLA 70-80 ms;
metrics "precision-recall trade-off and impact on good users" (no numbers disclosed).
Rates are our assumptions (decision.md D-10-02). Hidden truth columns start with "_".

Output: data/cs10/users.csv.gz
"""
import os
import numpy as np
import pandas as pd

SEED = 42
START = pd.Timestamp("2026-01-05"); DAYS = 91


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    n = 120_000
    day = np.sort(rng.uniform(0, DAYS, n))
    uid = np.array([f"U{i:06d}" for i in range(n)])
    # ---------- genuine attributes ----------
    dev = np.array([f"DV{i:06d}" for i in range(n)]); addr = np.array([f"AD{i:06d}" for i in range(n)])
    fam = rng.random(n) < 0.10                                                   # family members share device + address
    src = np.maximum(np.arange(n) - rng.integers(1, 40, n), 0)
    dev[fam] = dev[src[fam]]; addr[fam] = addr[src[fam]]
    hub = rng.random(n) < 0.12                                                   # hostels / PGs / offices
    hw = 1 / np.arange(1, 2001) ** 0.8; hw /= hw.sum()                              # hub sizes: few big hostels/offices, many small PGs
    addr[hub] = [f"HUB{h:04d}" for h in rng.choice(2000, hub.sum(), p=hw)]
    ipb = np.array([f"IPB{x:04d}" for x in rng.integers(0, 3000, n)])            # carrier IP blocks (huge hubs)
    phone = np.array([f"PH{i:06d}" for i in range(n)]); email_pat = np.array([f"EP{i:06d}" for i in range(n)])
    bank = np.array([f"BA{i:06d}" for i in range(n)]); famb = fam & (rng.random(n) < 0.5); bank[famb] = bank[src[famb]]   # spouses repay from one account
    age_days_phone = np.where(rng.random(n) < 0.15, rng.gamma(1.5, 30, n), rng.gamma(2.0, 400, n))   # SIM vintage; 15% of genuine users have new numbers
    limit = np.round(rng.choice([1500, 3000, 5000, 10000], n, p=[0.35, 0.35, 0.2, 0.1]), 0)
    spend7 = np.round(limit * np.clip(rng.beta(1.3, 4, n), 0.02, 1), 0)
    n_tx7 = 1 + rng.poisson(1.5, n)
    merchants7 = np.minimum(n_tx7, 1 + rng.poisson(0.7, n))
    night = rng.binomial(n_tx7, 0.06)
    kind = np.full(n, "genuine", dtype=object)
    fpd_p = np.full(n, 0.03)                                                     # genuine credit stress
    # ---------- fraud rings ----------
    ring_id = np.full(n, "", dtype=object)
    cand = np.flatnonzero(~fam & ~hub); used = set()
    for r in range(70):
        size = int(np.clip(rng.lognormal(np.log(10), 0.6), 4, 40)); d0 = rng.uniform(0, DAYS - 10)
        win = [i for i in cand[(day[cand] > d0) & (day[cand] < d0 + rng.uniform(3, 20))] if i not in used]      # members sign up over 3-20 days
        if len(win) < 4: continue
        pool = np.sort(rng.choice(win, min(size, len(win)), replace=False)); used.update(pool.tolist())
        ndev, naddr, nbank = max(1, size // 6), max(1, size // 5), max(1, size // 8)
        sharing = rng.uniform(0.5, 0.95)                                         # how much the gang re-uses attributes
        sh = rng.random(len(pool)) < sharing
        dev[pool[sh]] = rng.choice([f"RD{r:02d}{j}" for j in range(ndev)], sh.sum())
        sh2 = rng.random(len(pool)) < sharing; addr[pool[sh2]] = rng.choice([f"RA{r:02d}{j}" for j in range(naddr)], sh2.sum())
        sh3 = rng.random(len(pool)) < sharing; bank[pool[sh3]] = rng.choice([f"RB{r:02d}{j}" for j in range(nbank)], sh3.sum())
        sh4 = rng.random(len(pool)) < 0.6; email_pat[pool[sh4]] = f"REP{r:02d}"     # e.g., rahul.k1@, rahul.k2@ ... same pattern
        ipb[pool] = np.where(rng.random(len(pool)) < 0.5, f"IPB{rng.integers(3000):04d}", ipb[pool])
        age_days_phone[pool] = np.where(rng.random(len(pool)) < 0.6, rng.gamma(1.2, 40, len(pool)), rng.gamma(2.0, 250, len(pool)))   # mostly fresh SIMs; some bought aged
        spend7[pool] = np.round(limit[pool] * rng.uniform(0.75, 1.0, len(pool)), 0); n_tx7[pool] = 2 + rng.poisson(4, len(pool))
        merchants7[pool] = np.minimum(n_tx7[pool], 1 + rng.poisson(2.5, len(pool))); night[pool] = rng.binomial(n_tx7[pool], 0.2)
        kind[pool] = "ring"; ring_id[pool] = f"R{r:02d}"; fpd_p[pool] = 0.93
    # ---------- lone first-party fraud / ATO ----------
    lone = np.flatnonzero((kind == "genuine") & (rng.random(n) < 0.004))
    kind[lone] = "lone_fraud"; fpd_p[lone] = 0.85
    spend7[lone] = np.round(limit[lone] * rng.uniform(0.6, 1.0, len(lone)), 0); n_tx7[lone] = 2 + rng.poisson(3, len(lone)); night[lone] = rng.binomial(n_tx7[lone], 0.15)
    age_days_phone[lone] = rng.gamma(1.5, 150, len(lone))
    # genuine heavy users look a bit like fraud (hard negatives)
    heavy = (kind == "genuine") & (rng.random(n) < 0.05); spend7[heavy] = np.round(limit[heavy] * rng.uniform(0.7, 1.0, heavy.sum()), 0); n_tx7[heavy] += rng.poisson(3, heavy.sum())
    fpd = (rng.random(n) < fpd_p).astype(int)
    df = pd.DataFrame({"user_id": uid, "onboard_ts": START + pd.to_timedelta(day * 86400, unit="s"), "device_id": dev, "phone_id": phone, "email_pattern": email_pat,
                       "address_id": addr, "ip_block": ipb, "repay_bank_acct": bank, "sim_age_days": age_days_phone.round(), "credit_limit_inr": limit,
                       "spend_first7d_inr": spend7, "n_txn_first7d": n_tx7, "n_merchants_first7d": merchants7, "night_txn_first7d": night,
                       "fpd": fpd, "_kind": kind, "_ring": ring_id})
    # data-quality defects
    df.loc[df.sample(n=1500, random_state=seed).index, "device_id"] = "00000000"               # placeholder device id from an old SDK (a fake hub!)
    df.loc[df.sample(frac=0.01, random_state=seed + 1).index, "address_id"] = np.nan
    df = pd.concat([df, df.sample(n=500, random_state=seed + 2)], ignore_index=True)          # duplicated onboarding events
    return df


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs10"), exist_ok=True)
    d = generate(); d.to_csv(os.path.join(here, "cs10", "users.csv.gz"), index=False)
    dd = d.drop_duplicates("user_id")
    print(len(dd), "users |", dd._kind.value_counts().to_dict(), "| rings", dd._ring.replace("", np.nan).nunique())
    print("FPD by kind", dd.groupby("_kind").fpd.mean().round(3).to_dict(), "overall", dd.fpd.mean().round(4))
