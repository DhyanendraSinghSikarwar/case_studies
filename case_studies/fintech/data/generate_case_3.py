"""
SEMI-SYNTHETIC DATA GENERATOR - CASE 3 (Axis-style omnichannel nudge experiment)
================================================================================
BASE: real customer attributes from the UCI "Bank Marketing" dataset (bank-full.csv,
45,211 customers of a Portuguese bank, CC BY 4.0), bootstrapped to 200,000 customers.
EVERYTHING ELSE IS SYNTHETIC: the Indian-context attributes (city tier, tenure, income
band, digital activity, pre-period behaviour), the randomised experiment (80% treatment /
20% control, random channel), and every outcome. The UCI data has no randomised
treatment/control, so the experiment is simulated on top of it.

Calibration anchors (reference file, Case Study 22 - Axis Bank):
  * BillPay registration "1.5x boost in test versus control"
  * personal-loan (PL) campaign effectiveness "+10%"
  * channels include SMS, email, push, WhatsApp
Effect heterogeneity, base rates, ticket sizes and the injected sample-ratio-mismatch
(SRM) are our own assumptions (decision.md D-3-02 ... D-3-07).

Usage:  python data/generate_case_3.py  -> data/case3_nudge_experiment.csv
"""
import os
import numpy as np
import pandas as pd
from scipy import stats
from scipy.special import expit

SEED = 42
N = 200_000
HERE = os.path.dirname(os.path.abspath(__file__))
UCI_PATH = os.path.join(HERE, "public", "bank-full.csv")
CHANNELS = ["SMS", "Email", "WhatsApp", "Push"]
CAMPAIGN_START, CAMPAIGN_DAYS = pd.Timestamp("2025-10-01"), 61       # 1 Oct - 30 Nov 2025 (Diwali 20-21 Oct)
BILLPAY_RR = {"SMS": 1.19, "Email": 1.19, "WhatsApp": 1.49}         # Push handled separately (needs the app)
PL_RR = {"SMS": 1.08, "Email": 1.03, "WhatsApp": 1.12}
INCOME_BANDS = ["<5L", "5-10L", "10-25L", ">25L"]


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    uci = pd.read_csv(UCI_PATH, sep=";")
    base = uci.sample(n=N, replace=True, random_state=seed).reset_index(drop=True)   # bootstrap real attributes
    df = pd.DataFrame({"customer_id": [f"C{i:07d}" for i in range(1, N + 1)]})
    for c in ["age", "job", "marital", "education"]:
        df[c] = base[c].values
    df["credit_default_flag"] = (base["default"] == "yes").astype(int).values
    df["has_home_loan"] = (base["housing"] == "yes").astype(int).values
    df["has_personal_loan"] = (base["loan"] == "yes").astype(int).values
    df["prior_campaign_success"] = (base["poutcome"] == "success").astype(int).values
    df["prior_deposit_response"] = (base["y"] == "yes").astype(int).values

    # Indian savings balance: rank-preserving map of UCI balance (EUR) to log-normal INR (median ~Rs 45k)
    r = stats.rankdata(base["balance"].values + rng.uniform(0, 1e-3, N)) / (N + 1)
    df["avg_balance_inr"] = np.round(np.exp(np.log(45_000) + 1.2 * stats.norm.ppf(r)), -1)
    z_bal = stats.norm.ppf(r)

    tertiary = (df.education == "tertiary").to_numpy()
    df["city_tier"] = np.where(rng.random(N) < 0.45 + 0.15 * tertiary, "Tier 1",
                               np.where(rng.random(N) < 0.62, "Tier 2", "Tier 3"))
    df["tenure_months"] = np.clip(np.round(np.exp(np.log(60) + 0.6 * rng.normal(0, 1, N) + 0.01 * (df.age - 40))), 3, 360)
    job_score = df.job.map({"management": 1.0, "entrepreneur": 0.8, "self-employed": 0.5, "technician": 0.4, "admin.": 0.2,
                            "services": -0.1, "retired": -0.2, "blue-collar": -0.3, "housemaid": -0.7, "unemployed": -0.8,
                            "student": -0.9, "unknown": 0.0}).to_numpy()
    inc_score = job_score + 0.6 * tertiary + 0.5 * z_bal + rng.normal(0, 0.6, N)
    df["income_band"] = pd.cut(inc_score, [-np.inf, -0.35, 0.45, 1.35, np.inf], labels=INCOME_BANDS).astype(str)
    inc_idx = df.income_band.map({b: i for i, b in enumerate(INCOME_BANDS)}).to_numpy()
    tier1 = (df.city_tier == "Tier 1").to_numpy()
    df["digital_active"] = (rng.random(N) < expit(0.9 - 0.06 * (df.age - 40) + 0.5 * tertiary + 0.3 * tier1)).astype(int)
    dig = df.digital_active.to_numpy()
    df["pre_digital_txns_90d"] = rng.poisson(np.exp(1.2 + 1.3 * dig + 0.25 * inc_idx + rng.normal(0, 0.5, N)))
    df["pre_revenue_inr_90d"] = np.round(np.exp(np.log(450) + 0.45 * z_bal + 0.25 * inc_idx + 0.4 * df.has_home_loan
                                                + rng.normal(0, 0.8, N)), 0)

    # ---- randomised experiment: 80% treatment / 20% control; channel random within treatment ----
    treat = rng.random(N) < 0.80
    df["group"] = np.where(treat, "treatment", "control")
    df["channel"] = np.where(treat, rng.choice(CHANNELS, N), "none")
    ch = df.channel.to_numpy()
    age = df.age.to_numpy()

    # BillPay registration (control ~4%); lift varies by channel and segment
    p_bp = expit(-5.30 + 0.55 * np.log1p(df.pre_digital_txns_90d) + 0.5 * dig - 0.01 * (age - 40) + 0.1 * inc_idx)
    rr_bp = np.ones(N)
    for c, v in BILLPAY_RR.items():
        rr_bp = np.where(ch == c, v, rr_bp)
    rr_bp = np.where(ch == "Push", 1 + 0.75 * dig, rr_bp)                       # push only reaches app users
    young, old = age < 35, age >= 55
    rr_bp = np.where(np.isin(ch, ["WhatsApp", "Push"]) & young, rr_bp * 1.15, rr_bp)
    rr_bp = np.where((ch == "SMS") & old, rr_bp * 1.20, rr_bp)
    df["billpay_registered"] = (rng.random(N) < np.minimum(p_bp * rr_bp, 0.95)).astype(int)

    # Personal-loan booking (control ~2.5%); +~10% relative lift
    mid_age = (age >= 25) & (age <= 50)
    p_pl = expit(-4.30 + 0.45 * mid_age + 0.20 * (inc_idx == 1) + 0.25 * (inc_idx == 2) - 0.6 * df.has_personal_loan
                 - 1.0 * df.credit_default_flag + 0.5 * df.prior_campaign_success + 0.3 * df.prior_deposit_response
                 + 0.20 * np.log(df.pre_revenue_inr_90d / 450))
    rr_pl = np.ones(N)
    for c, v in PL_RR.items():
        rr_pl = np.where(ch == c, v, rr_pl)
    rr_pl = np.where(ch == "Push", 1 + 0.15 * dig, rr_pl)
    df["pl_booked"] = (rng.random(N) < np.minimum(p_pl * rr_pl, 0.95)).astype(int)
    booked = df.pl_booked.to_numpy() == 1
    med = np.array([120_000, 250_000, 450_000, 800_000])[inc_idx]
    amt = med * np.exp(rng.normal(0, 0.55, N)) * np.where(treat, 1.02, 1.0)
    df["pl_amount_inr"] = np.where(booked, np.clip(np.round(amt, -3), 50_000, 4_000_000), np.nan)
    # booking date: campaign window with a Diwali-week spike (seasonality)
    days = np.arange(CAMPAIGN_DAYS)
    w = 1 + 1.2 * np.exp(-0.5 * ((days - 18) / 4.0) ** 2) - 0.004 * days
    bdate = CAMPAIGN_START + pd.to_timedelta(rng.choice(days, N, p=w / w.sum()), unit="D")
    df["pl_booking_date"] = np.where(booked, bdate.strftime("%Y-%m-%d"), None)

    # ---- realistic messiness ----
    # (1) SRM: campaign-tracking export silently dropped 25% of PUSH-treated customers whose app was
    #     inactive (expired push tokens). Outcomes still exist in core banking (full table).
    lost = (ch == "Push") & (dig == 0) & (rng.random(N) < 0.25)
    df["in_campaign_export"] = (~lost).astype(int)
    # (2) missing covariates
    df.loc[rng.random(N) < 0.015, "tenure_months"] = np.nan
    df.loc[rng.random(N) < 0.02, "income_band"] = "Unknown"
    # (3) PL amounts recorded in paise (x100) for 20 bookings -> exceed the Rs 40 lakh product cap
    bidx = np.flatnonzero(booked)
    df.loc[rng.choice(bidx, 20, replace=False), "pl_amount_inr"] *= 100
    # (4) engagement guardrail: digital transactions DURING the 61-day campaign. Strongly autocorrelated
    #     with the pre-period (good CUPED case); nudges add ~+3% (more for app users on Push/WhatsApp).
    #     Drawn last so that every earlier random draw is unchanged.
    eng = np.where(np.isin(ch, ["Push", "WhatsApp"]) & (dig == 1), 0.06, np.where(treat, 0.01, 0.0))
    lam = (df.pre_digital_txns_90d.to_numpy() * 61 / 90 + 0.5) * np.exp(rng.normal(0, 0.35, N)) * (1 + eng)
    df["post_digital_txns_60d"] = rng.poisson(lam)
    return df


if __name__ == "__main__":
    d = generate()
    out = os.path.join(HERE, "case3_nudge_experiment.csv")
    d.to_csv(out, index=False)
    print(f"wrote {len(d):,} rows -> {out}")
    print(d.groupby("group")[["billpay_registered", "pl_booked"]].mean())
