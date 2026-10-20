"""
SYNTHETIC DATA GENERATOR - CASE STUDY 20 (PhonePe-style home-screen category ranking: propensity x LTV)
=====================================================================================================
THIS DATA IS SYNTHETIC. Super-app user and conversion data is confidential.

Two user populations:
  1. EXPLORATION LOG (150,000 users, Jul-Aug 2025): each user was shown ONE masthead category chosen
     uniformly at random and we record whether they transacted in it within 7 days. Random exposure
     makes propensity estimates unbiased - the training data for acquisition and repeat models.
  2. EXPERIMENT POPULATION (200,000 users, Sep 2025): features only + hidden true conversion
     probabilities and values for all 8 categories, so the notebook can run a digital-twin A/B test of
     ranking policies (random / rule-based / propensity-only / propensity x LTV).
Categories and 12-month value (LTV, Rs margin) for a NEW category user: recharge 40, bill pay 60,
credit-card bill 80, gold 150, travel 300, mutual funds 900, insurance 1,200, personal loan 2,000.
A repeat transaction in an already-used category is worth 25% of that (incremental only).

Calibration anchors (reference file, Case Study 20): acquisition + repeat models per category;
utility = propensity x LTV; A/B vs random and rule-based; metrics CPC, LTV, conversions,
incremental revenue. Numbers are our assumptions (decision.md D-20-02).

Outputs: data/cs20/exploration_log.csv.gz, data/cs20/experiment_users.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.special import expit

SEED = 42
CATS = ["recharge", "bill_pay", "cc_bill", "gold", "travel", "mutual_funds", "insurance", "personal_loan"]
LTV = dict(zip(CATS, [40, 60, 80, 150, 300, 900, 1200, 2000]))
BASE_ACQ = dict(zip(CATS, [-1.6, -2.1, -3.0, -3.3, -3.4, -4.0, -4.2, -4.5]))      # log-odds of first use if shown
PRIOR_USE = dict(zip(CATS, [0.70, 0.45, 0.12, 0.10, 0.08, 0.06, 0.07, 0.04]))


def users(n, rng):
    age = rng.choice(["18-24", "25-34", "35-44", "45+"], n, p=[0.28, 0.40, 0.20, 0.12])
    tier = rng.choice(["Tier 1", "Tier 2", "Tier 3"], n, p=[0.38, 0.36, 0.26])
    ios = (rng.random(n) < np.where(tier == "Tier 1", 0.18, 0.06)).astype(int)
    stage = rng.choice(["new (<30 days)", "active", "power"], n, p=[0.20, 0.60, 0.20])
    txn30 = rng.poisson(np.select([stage == "new (<30 days)", stage == "active"], [4, 14], 45))
    salary = (rng.random(n) < np.select([age == "18-24", age == "25-34"], [0.25, 0.55], 0.50)).astype(int)
    aff = rng.normal(0, 1, n)                                                     # latent "financial engagement"
    d = pd.DataFrame({"age_band": age, "city_tier": tier, "ios": ios, "journey_stage": stage, "txn_count_30d": txn30,
                      "salary_credit_flag": salary, "p2m_share": np.round(rng.beta(2 + aff.clip(-1.5, 1.5), 3), 3)})
    for c in CATS:
        d[f"used_{c}"] = (rng.random(n) < np.clip(PRIOR_USE[c] * np.exp(0.4 * aff + 0.5 * (stage == "power") - 0.6 * (stage == "new (<30 days)")), 0, 0.97)).astype(int)
    return d, aff


def true_prob(d, aff, c):
    used = d[f"used_{c}"].to_numpy()
    lt = np.log1p(d.txn_count_30d.to_numpy())
    age25 = (d.age_band == "25-34").to_numpy(); age35 = d.age_band.isin(["35-44", "45+"]).to_numpy()
    eff = {"recharge": 0.1 * lt, "bill_pay": 0.25 * lt + 0.3 * d.salary_credit_flag.to_numpy(),
           "cc_bill": 0.6 * d.salary_credit_flag.to_numpy() + 0.4 * d.ios.to_numpy() + 0.3 * aff,
           "gold": 0.4 * age35 + 0.3 * (d.city_tier == "Tier 2").to_numpy(),
           "travel": 0.5 * d.ios.to_numpy() + 0.3 * age25 + 0.2 * aff,
           "mutual_funds": 0.6 * aff + 0.5 * d.salary_credit_flag.to_numpy() + 0.3 * age25,
           "insurance": 0.4 * aff + 0.6 * age35 + 0.3 * d.salary_credit_flag.to_numpy(),
           "personal_loan": 0.5 * d.salary_credit_flag.to_numpy() - 0.3 * aff + 0.3 * (d.journey_stage == "power").to_numpy()}[c]
    z_acq = BASE_ACQ[c] + eff
    z_rep = BASE_ACQ[c] + 2.2 + eff                                                   # repeat use far more likely
    p = expit(np.where(used == 1, z_rep, z_acq))
    v = np.where(used == 1, 0.25 * LTV[c], LTV[c]) * np.exp(0.3 * aff)                 # engaged users are worth more
    return p, v


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    ex, aff_e = users(150_000, rng)
    shown = rng.choice(CATS, len(ex))
    P = np.column_stack([true_prob(ex, aff_e, c)[0] for c in CATS]); Vv = np.column_stack([true_prob(ex, aff_e, c)[1] for c in CATS])
    j = np.array([CATS.index(c) for c in shown])
    conv = (rng.random(len(ex)) < P[np.arange(len(ex)), j]).astype(int)
    ex.insert(0, "user_id", [f"U{i:07d}" for i in range(1, len(ex) + 1)])
    ex["shown_category"] = shown; ex["converted_7d"] = conv
    ex["revenue_12m_inr"] = np.where(conv == 1, np.round(Vv[np.arange(len(ex)), j] * np.exp(rng.normal(0, 0.5, len(ex))), 0), 0)
    ex["date"] = pd.Timestamp("2025-07-01") + pd.to_timedelta(rng.integers(0, 62, len(ex)), unit="D")
    # data-quality issues: bot/test accounts with absurd activity; a logging bug duplicated some impressions
    bots = ex.sample(n=300, random_state=seed).index
    ex.loc[bots, "txn_count_30d"] = rng.integers(900, 5000, 300); ex.loc[bots, "converted_7d"] = 1
    ex = pd.concat([ex, ex.sample(n=1200, random_state=seed + 1)], ignore_index=True)
    xp, aff_x = users(200_000, rng)
    xp.insert(0, "user_id", [f"X{i:07d}" for i in range(1, len(xp) + 1)])
    for c in CATS:
        p, v = true_prob(xp, aff_x, c); xp[f"_p_{c}"] = np.round(p, 5); xp[f"_v_{c}"] = np.round(v, 1)
    return ex, xp


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs20"), exist_ok=True)
    e, x = generate()
    e.to_csv(os.path.join(here, "cs20", "exploration_log.csv.gz"), index=False); x.to_csv(os.path.join(here, "cs20", "experiment_users.csv.gz"), index=False)
    print(len(e), "exploration rows;", len(x), "experiment users")
    print(e.groupby("shown_category").converted_7d.mean().round(4).to_dict())
