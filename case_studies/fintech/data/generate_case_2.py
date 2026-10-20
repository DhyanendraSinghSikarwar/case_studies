"""
SYNTHETIC DATA GENERATOR - CASE 2 (Lendingkart-style cash-flow MSME underwriting)
=================================================================================
THIS DATA IS SYNTHETIC. No public Indian MSME bank-statement + GST + bureau dataset
with loan outcomes exists, so we simulate ~50k applications over 24 months.

Calibration anchors (reference file, Case Study 11):
  * feature families: aggregates (min/avg closing balance, max credit months), trends,
    negative indicators (cheque returns, credit declines), momentum (QoQ/HoH/YoY),
    GST turnover, bureau score 300-900, key ratio EMI/ADB
  * outputs: score 300-900 and risk buckets A-F
  * "Model behaviour after COVID (when ITR and bureau data weakened)" -> the
    out-of-time (OOT) period Apr-2020..Mar-2021 carries a COVID-like shock
  * models "perform better for new-to-credit MSMEs that have CIBIL scores of 651-700"
Default-rate target (~6-10%), shares, effect sizes and the injected data-quality
issues are our own assumptions (decision.md D-2-02 ... D-2-07).

Usage:  python data/generate_case_2.py  -> data/case2_msme_applications_raw.csv
"""
import numpy as np
import pandas as pd
from scipy.special import expit

SEED = 42
N_APPS = 50_000
MONTHS = pd.period_range("2019-04", "2021-03", freq="M")          # 24 application months
SHOCK_START = pd.Period("2020-04", freq="M")                        # COVID-like shock -> OOT
# monthly application volume: growth pre-COVID, lockdown collapse, partial recovery
MONTH_WEIGHT = np.array([1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.5, 2.6, 2.6, 2.7, 2.8, 2.4,
                         0.6, 0.8, 1.2, 1.5, 1.7, 1.9, 2.0, 2.1, 2.1, 2.2, 2.2, 2.3])

INDUSTRY_DEV = {"Trading & Retail": .28, "Manufacturing": .16, "Services": .14, "Hospitality & Food": .09,
                "Textiles & Apparel": .10, "Pharma & Healthcare": .06, "E-commerce Sellers": .09, "Transport & Logistics": .08}
INDUSTRY_OOT = {"Trading & Retail": .30, "Manufacturing": .15, "Services": .13, "Hospitality & Food": .04,
                "Textiles & Apparel": .08, "Pharma & Healthcare": .10, "E-commerce Sellers": .15, "Transport & Logistics": .05}
INDUSTRY_QUALITY = {"Trading & Retail": 0.0, "Manufacturing": 0.10, "Services": 0.05, "Hospitality & Food": -0.20,
                    "Textiles & Apparel": -0.10, "Pharma & Healthcare": 0.20, "E-commerce Sellers": 0.0, "Transport & Logistics": -0.10}
INDUSTRY_SCALE = {"Trading & Retail": 1.2, "Manufacturing": 1.5, "Services": 0.8, "Hospitality & Food": 0.7,
                  "Textiles & Apparel": 1.0, "Pharma & Healthcare": 1.1, "E-commerce Sellers": 0.9, "Transport & Logistics": 1.0}
# extra default log-odds during the shock (hospitality/transport hit hardest; pharma/e-com resilient)
SHOCK_INDUSTRY = {"Trading & Retail": 0.20, "Manufacturing": 0.25, "Services": 0.25, "Hospitality & Food": 0.85,
                  "Textiles & Apparel": 0.35, "Pharma & Healthcare": -0.10, "E-commerce Sellers": 0.0, "Transport & Logistics": 0.60}
TIER = {"Tier 1": .35, "Tier 2": .40, "Tier 3": .25}
CONSTITUTION = {"Proprietorship": .65, "Partnership": .15, "Private Ltd": .20}
CHANNELS = {"Direct Web": .30, "Mobile App": .25, "DSA_Partner_03": .15, "DSA_Partner_07": .15, "Marketplace_Partner": .15}


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    n = N_APPS
    month = MONTHS[rng.choice(len(MONTHS), n, p=MONTH_WEIGHT / MONTH_WEIGHT.sum())]
    oot = np.array([m >= SHOCK_START for m in month])
    day = rng.integers(1, 29, n)
    app_date = pd.to_datetime([f"{m.year}-{m.month:02d}-{d:02d}" for m, d in zip(month, day)])

    ind = np.where(oot, rng.choice(list(INDUSTRY_OOT), n, p=list(INDUSTRY_OOT.values())),
                   rng.choice(list(INDUSTRY_DEV), n, p=list(INDUSTRY_DEV.values())))
    tier = rng.choice(list(TIER), n, p=list(TIER.values()))
    const = rng.choice(list(CONSTITUTION), n, p=list(CONSTITUTION.values()))
    channel = rng.choice(list(CHANNELS), n, p=list(CHANNELS.values()))
    vintage = np.clip(np.round(np.exp(rng.normal(np.log(5), 0.6, n)), 1), 1.0, 40.0)

    # latent business quality (never released): drives every feature + default
    q = (rng.normal(0, 1, n) + pd.Series(ind).map(INDUSTRY_QUALITY).to_numpy()
         + pd.Series(tier).map({"Tier 1": 0.10, "Tier 2": 0.0, "Tier 3": -0.15}).to_numpy()
         + pd.Series(const).map({"Proprietorship": -0.05, "Partnership": 0.0, "Private Ltd": 0.15}).to_numpy()
         + 0.25 * (np.log(vintage) - np.log(5)))
    shock = oot.astype(float)

    # ---- aggregates (12-month bank statement observation window) ----
    scale = pd.Series(ind).map(INDUSTRY_SCALE).to_numpy()
    credits = 6e5 * scale * np.exp(0.35 * q + rng.normal(0, 0.8, n)) * np.where(oot, 0.78, 1.0)
    avg_bal = credits * 0.18 * np.exp(0.30 * q + rng.normal(0, 0.5, n)) * np.where(oot, 0.85, 1.0)
    min_bal = avg_bal * expit(-1.0 + 0.3 * q + rng.normal(0, 0.5, n) - 0.3 * shock)       # correlated with avg
    max_credit = credits * (1.4 + np.exp(rng.normal(-0.7, 0.5, n)))
    credit_months = np.clip(12 - rng.poisson(np.exp(-0.6 - 0.6 * q + 0.5 * shock)), 3, 12)
    # ---- trends (slope of monthly series, % per month) ----
    bal_trend = rng.normal(0.5 + 1.0 * q - 2.0 * shock, 3.0, n)
    cred_trend = 0.6 * bal_trend + rng.normal(0.3 * q, 2.0, n)
    # ---- momentum (correlated on purpose: QoQ ~ HoH ~ YoY) ----
    yoy = rng.normal(8 + 6 * q - 15 * shock, 20, n)
    hoh = 0.6 * yoy + rng.normal(0, 9, n)
    qoq = 0.55 * hoh + rng.normal(0, 7, n)
    # ---- negative indicators ----
    bounces = rng.poisson(np.exp(-1.2 - 0.8 * q + 0.35 * shock))
    declines = rng.poisson(np.exp(-1.0 - 0.5 * q + 0.30 * shock))
    # ---- loan, EMI and the key EMI/ADB ratio ----
    loan = np.clip(np.round(credits * rng.uniform(0.5, 2.0, n), -3), 1e5, 5e6)
    emi = loan * 0.0509                                                # 24 months @ ~20% p.a.
    emi_to_adb = emi / avg_bal
    # ---- GST ----
    gst_reg = rng.random(n) < np.where(vintage < 2, 0.80, 0.93)
    gst_turnover = np.where(gst_reg, 12 * credits * np.exp(rng.normal(-0.05, 0.15, n)), np.nan)   # r~0.95 with credits
    gst_ontime = np.where(gst_reg, np.round(100 * expit(1.5 + 0.8 * q + rng.normal(0, 0.8, n) - 0.6 * shock), 1), np.nan)
    # ---- bureau ----
    ntc = rng.random(n) < np.clip(0.06 + 0.10 * (vintage < 3) + 0.05 * (const == "Proprietorship"), 0, 1)
    info = np.where(oot, 0.45, 0.60)                                   # bureau weakens in the shock (moratorium)
    bureau = np.clip(np.round(715 + 60 * (info * q + np.sqrt(1 - info ** 2) * rng.normal(0, 1, n)) + 12 * shock), 300, 900)
    bureau = np.where(ntc, np.nan, bureau)
    enquiries = rng.poisson(np.exp(0.3 - 0.3 * q + 0.2 * shock))

    # ---- default: 90+ DPD within 12 months of disbursal ----
    z = (-3.28 - 0.65 * q
         + 0.22 * np.minimum(bounces, 5) + 0.15 * np.minimum(declines, 4)
         + 0.45 * (emi_to_adb > 1.5) + 0.40 * (vintage < 2)
         - 0.004 * np.nan_to_num(bureau - 715) * np.where(oot, 0.4, 1.0) + 0.30 * ntc
         - 0.010 * np.clip(yoy, -60, 60) * np.where(oot, 1.6, 1.0)
         + 0.35 * (~gst_reg)
         + pd.Series(tier).map({"Tier 1": -0.10, "Tier 2": 0.0, "Tier 3": 0.15}).to_numpy()
         + shock * pd.Series(ind).map(SHOCK_INDUSTRY).to_numpy())
    default = (rng.random(n) < expit(z)).astype(int)

    df = pd.DataFrame({
        "business_id": [f"B{i:06d}" for i in range(1, n + 1)],
        "application_date": app_date, "source_channel": channel, "industry": ind, "city_tier": tier,
        "constitution": const, "vintage_years": vintage, "loan_amount_inr": loan,
        "bureau_score": bureau, "bureau_enquiries_6m": enquiries,
        "avg_monthly_credits_inr": np.round(credits, -2), "max_monthly_credit_inr": np.round(max_credit, -2),
        "credit_months_active": credit_months,
        "avg_closing_balance_inr": np.round(avg_bal, -2), "min_closing_balance_inr": np.round(min_bal, -2),
        "balance_trend_pct": np.round(bal_trend, 2), "credit_trend_pct": np.round(cred_trend, 2),
        "credit_growth_qoq_pct": np.round(qoq, 1), "credit_growth_hoh_pct": np.round(hoh, 1),
        "credit_growth_yoy_pct": np.round(yoy, 1),
        "cheque_bounces_6m": bounces, "credit_declines_6m": declines, "emi_to_adb": np.round(emi_to_adb, 3),
        "gst_registered": gst_reg.astype(int), "gst_turnover_12m_inr": np.round(gst_turnover, -3),
        "gst_filing_ontime_pct": gst_ontime, "default_90dpd_12m": default,
    })

    # ---- realistic messiness / data-quality issues ----
    # (1) MAIN DQ ISSUE: DSA_Partner_07 sent GST turnover in Rs lakh (not Rs) for Aug-Oct 2019
    bad = (df.source_channel == "DSA_Partner_07") & df.application_date.between("2019-08-01", "2019-10-31") & df.gst_registered.eq(1)
    df.loc[bad, "gst_turnover_12m_inr"] = np.round(df.loc[bad, "gst_turnover_12m_inr"] / 1e5, 2)
    # (2) statement-parser failures: trend/momentum blank for 1.5%
    parse_fail = rng.random(n) < 0.015
    for c in ["balance_trend_pct", "credit_trend_pct", "credit_growth_qoq_pct", "credit_growth_hoh_pct", "credit_growth_yoy_pct"]:
        df.loc[parse_fail, c] = np.nan
    # (3) sentinel values: vintage 99 (unknown) and bureau 0 (no-hit coded as zero)
    df.loc[df.sample(n=30, random_state=seed).index, "vintage_years"] = 99.0
    zero_idx = df.index[df.bureau_score.isna()]
    df.loc[rng.choice(zero_idx, 40, replace=False), "bureau_score"] = 0.0
    # (4) re-applications: same business applies again within 60 days (2%)
    re = df.sample(frac=0.02, random_state=seed + 1).copy()
    re["application_date"] = re.application_date + pd.to_timedelta(rng.integers(5, 60, len(re)), unit="D")
    re["loan_amount_inr"] = np.round(re.loan_amount_inr * rng.uniform(0.6, 0.9, len(re)), -3)
    df = pd.concat([df, re], ignore_index=True).sort_values("application_date", kind="stable").reset_index(drop=True)
    df.insert(0, "application_id", [f"APP{i:07d}" for i in range(1, len(df) + 1)])
    return df


if __name__ == "__main__":
    import os
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "case2_msme_applications_raw.csv")
    d = generate()
    d.to_csv(out, index=False)
    print(f"wrote {len(d):,} rows -> {out}; default rate = {d.default_90dpd_12m.mean():.4f}")
