"""
SYNTHETIC DATA GENERATOR - CASE STUDY 17 (HDFC Bank-style 10-second pre-approved personal loans)
================================================================================================
THIS DATA IS SYNTHETIC. Bank customer and loan data are confidential.

Existing customers of a bank are scored by a layered "P27-style" framework:
  ability-to-pay (salary credits, balances), bureau, behaviour (card spend, repayment history) and a
  "social"/digital-engagement score. The top third by the combined score are ELIGIBLE for an instant,
  paperless pre-approved personal loan ("10-second loan").
Three loan populations, each followed for 12 months on book:
  * DIGITAL     - eligible customers who took the instant loan (observational)
  * PHYSICAL    - branch/DSA-sourced loans with documents and manual underwriting (observational; a
                  mix of existing customers - some eligible, many not - and a few new-to-bank)
  * PILOT       - eligible customers RANDOMISED to instant digital vs standard physical processing
                  (a design the bank could run to prove non-inferiority causally)
Delinquency depends on customer risk, loan size and a small CHANNEL effect: instant loans carry a
slightly higher risk for the same customer (no human check, more impulse borrowing) - so the raw
"on par" comparison hides a real but small difference, because digital borrowers are better on average.

Calibration anchors (reference file, Case Study 17): ~1/3 of ~30M customers eligible; loans up to Rs 15 lakh;
10-second loans ~1/3 of ~Rs 6,000 crore monthly PL disbursals; delinquency "on a par with loans disbursed
physically"; P27 layers (income, bureau, behavioural, social). Rates are our assumptions (decision.md D-17-02).
Hidden truth columns start with "_".

Outputs: data/cs17/customers.csv.gz, data/cs17/loans.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.special import expit

SEED = 42
CHANNEL_EFFECT = 0.12          # log-odds uplift of 30+ DPD for an instant digital loan vs physical, same customer (hidden truth)


def generate(seed=SEED, n_cust=200_000):
    rng = np.random.default_rng(seed)
    z = rng.normal(0, 1, n_cust)                                                    # latent creditworthiness
    salary = np.exp(rng.normal(np.log(55000), 0.55, n_cust) + 0.15 * z)
    salaried_acct = (rng.random(n_cust) < 0.7).astype(int)
    avg_bal = np.exp(rng.normal(np.log(60000), 0.9, n_cust) + 0.35 * z)
    bureau = np.clip(np.round(730 + 50 * z + rng.normal(0, 45, n_cust)), 300, 900)
    card_util = np.clip(rng.beta(2, 4, n_cust) - 0.06 * z, 0, 1)
    past_dpd = rng.poisson(np.exp(-1.6 - 0.6 * z))
    relationship_yrs = np.clip(rng.gamma(2.5, 2.5, n_cust), 0.5, 25)
    digital_eng = np.clip(rng.normal(50 + 4 * z, 18, n_cust), 0, 100)               # "social" / internet-usage score (weak signal)
    cust = pd.DataFrame({"customer_id": [f"C{i:07d}" for i in range(n_cust)], "salary_credit_monthly": np.round(salary, -2), "salaried_account": salaried_acct,
                         "avg_balance_6m": np.round(avg_bal, -2), "bureau_score": bureau, "card_utilisation": card_util.round(3), "past_dpd_events_24m": past_dpd,
                         "relationship_years": relationship_yrs.round(1), "digital_engagement_score": digital_eng.round(1), "_z": z})
    # layered scores (what the bank sees)
    s_ability = np.log(salary) * 0.8 + 0.25 * np.log(avg_bal) + 0.3 * salaried_acct
    s_bureau = (bureau - 730) / 50
    s_behav = -2.0 * card_util - 0.6 * past_dpd + 0.04 * relationship_yrs
    s_social = (digital_eng - 50) / 18
    combo = 0.45 * (s_ability - s_ability.mean()) / s_ability.std() + 0.35 * s_bureau / s_bureau.std() + 0.35 * (s_behav - s_behav.mean()) / s_behav.std() + 0.05 * s_social
    cust["p27_score"] = np.round(500 + 80 * combo, 0)
    cust["eligible"] = (cust.p27_score >= np.quantile(cust.p27_score, 2 / 3)).astype(int)
    elig = cust.eligible.values == 1

    def outcome(idx, channel, amount):
        zz = z[idx]; lg = -3.0 - 0.95 * zz + 0.25 * np.log(amount / 3e5) + np.where(channel == "digital", CHANNEL_EFFECT, 0.0)
        p30 = expit(lg); d30 = rng.random(len(idx)) < p30
        month = np.where(d30, np.clip(np.ceil(rng.exponential(5.5, len(idx))), 1, 12), np.nan)
        p90 = np.where(d30, expit(-0.6 - 0.6 * zz), 0); d90 = d30 & (rng.random(len(idx)) < p90)
        return p30, d30.astype(int), month, d90.astype(int)
    rows = []
    # DIGITAL (observational): eligible customers with higher digital engagement take up more
    take = elig & (rng.random(n_cust) < expit(-2.6 + 0.02 * (digital_eng - 50) + 0.2 * (z < 0)))
    idx = np.flatnonzero(take); amt = np.round(np.clip(salary[idx] * rng.uniform(4, 12, len(idx)), 5e4, 15e5), -3)
    p, d, mth, d90 = outcome(idx, "digital", amt)
    rows.append(pd.DataFrame({"customer_id": cust.customer_id.values[idx], "cohort": "observational", "channel": "digital", "loan_amount": amt, "_p30": p, "dpd30_12m": d, "dpd30_month": mth, "dpd90_12m": d90}))
    # PHYSICAL (observational): branch applicants - mostly non-eligible existing customers (riskier on average), screened by officers
    app = (~take) & (rng.random(n_cust) < np.where(elig, 0.06, 0.05) * expit(0.3 - 0.4 * z))
    screened = app & (rng.random(n_cust) < expit(1.2 + 2.2 * z))                     # manual underwriting rejects the obviously risky
    idx = np.flatnonzero(screened); amt = np.round(np.clip(salary[idx] * rng.uniform(3, 10, len(idx)), 5e4, 15e5), -3)
    p, d, mth, d90 = outcome(idx, "physical", amt)
    rows.append(pd.DataFrame({"customer_id": cust.customer_id.values[idx], "cohort": "observational", "channel": "physical", "loan_amount": amt, "_p30": p, "dpd30_12m": d, "dpd30_month": mth, "dpd90_12m": d90}))
    # PILOT (randomised): 16,000 eligible customers who asked for a loan, randomised 1:1
    pool = np.flatnonzero(elig & ~take & ~screened); idx = rng.choice(pool, 16_000, replace=False)
    ch = np.where(rng.random(len(idx)) < 0.5, "digital", "physical"); amt = np.round(np.clip(salary[idx] * rng.uniform(4, 12, len(idx)), 5e4, 15e5), -3)
    p, d, mth, d90 = outcome(idx, ch, amt)
    rows.append(pd.DataFrame({"customer_id": cust.customer_id.values[idx], "cohort": "pilot", "channel": ch, "loan_amount": amt, "_p30": p, "dpd30_12m": d, "dpd30_month": mth, "dpd90_12m": d90}))
    ln = pd.concat(rows, ignore_index=True)
    ln.insert(0, "loan_id", [f"PL{i:07d}" for i in range(len(ln))])
    ln["tat_minutes"] = np.where(ln.channel == "digital", np.round(rng.uniform(0.1, 0.3, len(ln)), 2), np.round(rng.gamma(2, 1100, len(ln))))   # ~2-3 days for physical
    # data-quality defects
    ln.loc[ln.sample(n=250, random_state=seed).index, "dpd30_month"] = np.nan                   # month missing although delinquent
    ln = pd.concat([ln, ln.sample(n=300, random_state=seed + 1)], ignore_index=True)
    cust.loc[cust.sample(n=1500, random_state=seed + 2).index, "digital_engagement_score"] = np.nan
    return cust, ln


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs17"), exist_ok=True)
    c, l = generate(); c.to_csv(os.path.join(here, "cs17", "customers.csv.gz"), index=False); l.to_csv(os.path.join(here, "cs17", "loans.csv.gz"), index=False)
    ll = l.drop_duplicates("loan_id").merge(c[["customer_id", "_z", "eligible"]], on="customer_id")
    print(ll.groupby(["cohort", "channel"]).agg(n=("loan_id", "size"), dpd30=("dpd30_12m", "mean"), dpd90=("dpd90_12m", "mean"), z=("_z", "mean"), elig=("eligible", "mean")).round(4))
