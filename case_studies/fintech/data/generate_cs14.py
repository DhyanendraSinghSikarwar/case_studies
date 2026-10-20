"""
SYNTHETIC DATA GENERATOR - CASE STUDY 14 (Kissht-style segment-specific underwriting)
=====================================================================================
THIS DATA IS SYNTHETIC. Lender application and performance data are confidential.

12 months of disbursed small-ticket loans (consumer-durable EMI and short personal loans). Applicants
fall into structurally different segments:
  bureau depth   : NTC (new to credit, no bureau score) / THIN (1-2 tradelines) / THICK
  employment     : salaried / self-employed
  relationship   : new customer / repeat customer (has prior loans with the lender)
What drives default DIFFERS by segment (the reason to segment):
  * THICK file: bureau score and recent delinquencies dominate
  * NTC / THIN: bank-statement cash-flow (inflow, volatility, bounces) and digital footprint matter
  * self-employed: inflow volatility and GST-turnover consistency matter more than for salaried
  * repeat: own repayment history with the lender dominates everything else
Target: bad = 60+ DPD within 6 months on book. A traditional bureau score exists for THIN/THICK only.

Calibration anchors (reference file, Case Study 14): "39 specialized ML sub-models" / "40+ models";
"~5.17x separation in default rates between highest and lowest risk segments" vs "2.13x for traditional
credit bureau scores"; GNPA 2.90%; ~85% of new customers get offers in 10 minutes; 26.46% of repeat
applicants declined. Rates are our assumptions (decision.md D-14-02). Hidden truth columns start "_".

Output: data/cs14/loans.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.special import expit

SEED = 42
START = pd.Timestamp("2025-04-01")


def generate(seed=SEED, n=120_000):
    rng = np.random.default_rng(seed)
    month = rng.integers(0, 12, n)
    depth = rng.choice(["NTC", "THIN", "THICK"], n, p=[0.30, 0.25, 0.45])
    emp = rng.choice(["salaried", "self_employed"], n, p=[0.62, 0.38])
    repeat = (rng.random(n) < np.where(month < 3, 0.15, 0.32)).astype(int)        # repeat share grows over the year (mix shift)
    product = rng.choice(["consumer_durable", "personal_loan"], n, p=[0.55, 0.45])
    age = np.clip(rng.normal(31, 7, n), 21, 60).round()
    city_tier = rng.choice([1, 2, 3], n, p=[0.35, 0.40, 0.25])
    income = np.exp(rng.normal(np.log(np.where(emp == "salaried", 32000, 28000)), 0.45))
    # latent creditworthiness (unobserved) drives everything a little
    z = rng.normal(0, 1, n)
    # bureau
    bureau = np.where(depth == "NTC", np.nan, np.clip(np.round(720 + 55 * z + rng.normal(0, 40, n) - 25 * (depth == "THIN")), 300, 900))
    n_trades = np.where(depth == "NTC", 0, np.where(depth == "THIN", rng.integers(1, 3, n), rng.integers(3, 15, n)))
    dpd30_12m = np.where(depth == "THICK", rng.poisson(np.exp(-1.2 - 0.6 * z)), np.where(depth == "THIN", rng.poisson(np.exp(-1.8 - 0.4 * z)), 0))
    enquiries_3m = rng.poisson(np.exp(0.4 - 0.25 * z + 0.3 * (depth != "NTC")))
    # bank statement / cash flow
    inflow_vol = np.clip(rng.gamma(2, 0.12, n) * np.where(emp == "self_employed", 1.8, 1.0) * np.exp(-0.2 * z), 0.02, 2.5)
    bounces_6m = rng.poisson(np.exp(-1.5 - 0.7 * z + 0.4 * (emp == "self_employed")))
    avg_bal_to_income = np.clip(np.exp(rng.normal(-1.2 + 0.35 * z, 0.6)), 0.01, 5)
    gst_consistency = np.where(emp == "self_employed", np.clip(rng.beta(4, 2, n) + 0.08 * z, 0, 1), np.nan)
    digital_score = np.clip(rng.normal(50 + 6 * z, 15), 0, 100)
    loan_amt = np.round(np.exp(rng.normal(np.log(np.where(product == "personal_loan", 25000, 18000)), 0.5)), -2)
    emi_to_income = loan_amt / np.where(product == "personal_loan", 9, 12) / income
    prior_loans = np.where(repeat == 1, 1 + rng.poisson(1.5, n), 0)
    prior_max_dpd = np.where(repeat == 1, rng.choice([0, 5, 15, 30, 60], n, p=[0.62, 0.18, 0.1, 0.06, 0.04]), np.nan)
    pd_ = prior_max_dpd.copy()
    # ---------- segment-specific default logit ----------
    zb = np.nan_to_num((bureau - 720) / 60)
    lg = -4.15 - 0.25 * z + 0.6 * np.clip(emi_to_income - 0.35, 0, None) * 3 + 0.12 * (city_tier == 3) + 0.15 * (product == "personal_loan")
    thick = depth == "THICK"; thin = depth == "THIN"; ntc = depth == "NTC"; se = emp == "self_employed"
    lg += thick * (-0.95 * zb + 0.45 * np.minimum(dpd30_12m, 4) + 0.10 * enquiries_3m)
    lg += thin * (-0.45 * zb + 0.35 * np.minimum(dpd30_12m, 3) + 0.55 * np.minimum(bounces_6m, 4) - 0.35 * np.log(avg_bal_to_income) - 0.02 * (digital_score - 50))
    lg += ntc * (0.75 * np.minimum(bounces_6m, 4) - 0.55 * np.log(avg_bal_to_income) - 0.035 * (digital_score - 50) + 0.25 * enquiries_3m + 0.1)
    lg += se * (1.4 * (inflow_vol - 0.4) - 1.6 * (np.nan_to_num(gst_consistency, nan=0.65) - 0.65) + 0.25)
    lg += (~se) * (0.4 * (inflow_vol - 0.25))
    rep = repeat == 1
    lg = np.where(rep, -4.4 + 0.045 * np.nan_to_num(pd_) - 0.25 * np.minimum(prior_loans, 4) + 0.4 * (lg + 4.15) * 0.5, lg)   # repeat: own history dominates
    p_bad = expit(lg)
    bad = (rng.random(n) < p_bad).astype(int)
    df = pd.DataFrame({"loan_id": [f"L{i:07d}" for i in range(n)], "disb_month": (START + pd.to_timedelta(month * 30.4, unit="D")).strftime("%Y-%m"),
                       "bureau_depth": depth, "employment": emp, "repeat_customer": repeat, "product": product, "age": age, "city_tier": city_tier,
                       "monthly_income": np.round(income, -2), "bureau_score": bureau, "n_tradelines": n_trades, "dpd30_last12m": dpd30_12m,
                       "enquiries_3m": enquiries_3m, "inflow_volatility": inflow_vol.round(3), "bounces_6m": bounces_6m, "avg_bal_to_income": avg_bal_to_income.round(3),
                       "gst_consistency": np.round(gst_consistency, 3), "digital_footprint_score": digital_score.round(1), "loan_amount": loan_amt,
                       "emi_to_income": emi_to_income.round(3), "prior_loans": prior_loans, "prior_max_dpd": prior_max_dpd, "bad_60dpd_6m": bad, "_p_bad": p_bad})
    # data-quality defects
    df.loc[df.sample(n=300, random_state=seed).index, "bureau_score"] = -1                 # bureau "no-hit" coded as -1 for some thick files
    df.loc[df.sample(frac=0.02, random_state=seed + 1).index, "monthly_income"] = np.nan
    df = pd.concat([df, df.sample(n=400, random_state=seed + 2)], ignore_index=True)       # duplicated disbursal records
    return df


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs14"), exist_ok=True)
    d = generate(); d.to_csv(os.path.join(here, "cs14", "loans.csv.gz"), index=False)
    dd = d.drop_duplicates("loan_id")
    print(len(dd), "loans | bad rate", dd.bad_60dpd_6m.mean().round(4))
    print(dd.groupby(["bureau_depth", "employment", "repeat_customer"]).bad_60dpd_6m.agg(["mean", "size"]).round(4))
