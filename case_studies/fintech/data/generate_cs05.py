"""
SYNTHETIC DATA GENERATOR - CASE STUDY 5 (Razorpay "Bumblebee"-style automated merchant risk review)
==================================================================================================
THIS DATA IS SYNTHETIC. Merchant onboarding and review data are confidential.

Three months of new-merchant onboarding reviews (~12,000/month). Each merchant has evidence an analyst or
an agent system would gather: website (exists, SSL, load time, policy pages, content matches declared
business), WHOIS domain age, internal fraud-database hit, social presence, category risk, pricing anomalies.
A hidden TRUE risk status determines whether the merchant later turns fraudulent / violates policy.
Decisions:
  * ANALYST: one of 40 analysts reviews each merchant; analysts differ in strictness and attention (noise) -
    the documented inconsistency problem.
  * AGENT SYSTEM: a planner/fetcher/analyser pipeline producing approve/reject + a confidence score,
    with latency and token cost per review (two designs: v1 monolithic, v2 planner + parallel fetchers).
  * GOLD PANEL: a 3,000-merchant audit sample reviewed independently by 3 senior analysts.
  * OUTCOME: 6-month fraud / chargeback / policy-violation flag for APPROVED merchants.

Calibration anchors (reference file, Case Study 5): ~12,000 reviews/month, 20+ minutes each (~8,500 hours);
agent 8-12 s per evaluation; accuracy "99%+" up from 88%; 60% fewer tokens than the earlier design; how accuracy
was measured is ND. Rates are our assumptions (decision.md D-5-02). Hidden truth columns start with "_".

Outputs: data/cs05/reviews.csv.gz, data/cs05/gold_panel.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.special import expit

SEED = 42
CATS = ["retail", "food", "education", "services", "saas", "travel", "gaming", "forex_crypto", "nutraceuticals"]


def generate(seed=SEED, n=36_000):
    rng = np.random.default_rng(seed)
    month = rng.integers(1, 4, n)
    cat = rng.choice(CATS, n, p=[0.24, 0.16, 0.12, 0.16, 0.10, 0.07, 0.06, 0.04, 0.05])
    cat_risk = pd.Series(cat).map({"retail": 0, "food": -0.3, "education": -0.2, "services": 0, "saas": -0.4, "travel": 0.3, "gaming": 1.0, "forex_crypto": 1.6, "nutraceuticals": 1.2}).values
    z = rng.normal(0, 1, n)                                                               # latent riskiness
    risky = (rng.random(n) < expit(-3.0 + 1.3 * z + cat_risk)).astype(int)              # TRUE risk status
    site = (rng.random(n) < np.where(risky, 0.80, 0.93)).astype(int)
    ssl = np.where(site == 1, (rng.random(n) < np.where(risky, 0.70, 0.95)).astype(int), 0)
    load_s = np.where(site == 1, np.round(np.exp(rng.normal(np.log(np.where(risky, 3.2, 2.0)), 0.5, n)), 2), np.nan)
    policy_pages = np.where(site == 1, (rng.random(n) < np.where(risky, 0.45, 0.85)).astype(int), 0)
    content_match = np.where(site == 1, (rng.random(n) < np.where(risky, 0.55, 0.93)).astype(int), 0)
    domain_age_d = np.round(np.exp(rng.normal(np.log(np.where(risky, 60, 700)), 1.0, n)))
    fraud_db_hit = (rng.random(n) < np.where(risky, 0.22, 0.004)).astype(int)
    social = (rng.random(n) < np.where(risky, 0.35, 0.70)).astype(int)
    price_anom = (rng.random(n) < np.where(risky, 0.30, 0.04)).astype(int)
    ev = (1.6 * (1 - ssl) + 1.2 * (1 - policy_pages) + 1.4 * (1 - content_match) - 0.7 * np.log(domain_age_d / 300) + 3.5 * fraud_db_hit
          - 0.8 * social + 1.5 * price_anom + 0.9 * cat_risk + 1.0 * (1 - site))
    # analysts: 40 people with different strictness and attention
    a_id = rng.integers(0, 40, n); strict = rng.normal(0, 1.1, 40); attention = rng.uniform(0.35, 0.95, 40)
    a_sig = attention[a_id] * ev + (1 - attention[a_id]) * rng.normal(2, 4, n) + rng.normal(0, 1.8, n)
    analyst_reject = (a_sig + strict[a_id] > 4.1).astype(int)
    # agent system: sees all evidence consistently, small noise; confidence = |margin|
    a_score = 0.95 * ev + rng.normal(0, 0.3, n) + (rng.random(n) < 0.008) * rng.normal(0, 3, n)      # occasional fetch failure noise
    agent_p_reject = expit(1.8 * (a_score - 4.2)); agent_reject = (agent_p_reject > 0.5).astype(int)
    agent_conf = np.abs(agent_p_reject - 0.5) * 2
    lat_v2 = np.round(np.exp(rng.normal(np.log(10), 0.25, n)), 2); lat_v1 = np.round(np.exp(rng.normal(np.log(38), 0.4, n)), 2)
    tok_v2 = np.round(np.exp(rng.normal(np.log(9000), 0.3, n))); tok_v1 = np.round(np.exp(rng.normal(np.log(22500), 0.3, n)))
    analyst_min = np.round(np.exp(rng.normal(np.log(22), 0.35, n)), 1)
    # outcome for approved merchants (under the analyst decision in month 1-3 history)
    p_bad = np.where(risky == 1, 0.55, 0.012)
    bad_6m = (rng.random(n) < p_bad).astype(int)
    df = pd.DataFrame({"merchant_id": [f"MR{i:06d}" for i in range(n)], "month": month, "category": cat, "website_exists": site, "ssl_valid": ssl,
                       "page_load_s": load_s, "policy_pages": policy_pages, "content_matches_business": content_match, "domain_age_days": domain_age_d,
                       "fraud_db_hit": fraud_db_hit, "social_presence": social, "price_anomaly": price_anom, "analyst_id": [f"AN{x:02d}" for x in a_id],
                       "analyst_reject": analyst_reject, "analyst_minutes": analyst_min, "agent_reject": agent_reject, "agent_p_reject": agent_p_reject.round(4),
                       "agent_confidence": agent_conf.round(4), "agent_latency_s_v2": lat_v2, "agent_tokens_v2": tok_v2, "agent_latency_s_v1": lat_v1, "agent_tokens_v1": tok_v1,
                       "bad_6m_if_approved": bad_6m, "_risky": risky, "_ev": ev})
    # gold panel: 3,000 merchants, 3 senior analysts each (high attention, low noise)
    gi = rng.choice(n, 3000, replace=False); g = df.iloc[gi][["merchant_id", "_ev", "_risky"]].copy()
    for k in range(3):
        g[f"senior_{k + 1}_reject"] = (0.95 * g._ev + rng.normal(0, 0.3, len(g)) + rng.normal(0, 0.1) > 4.2).astype(int)
    g["gold_reject"] = (g[[f"senior_{k + 1}_reject" for k in range(3)]].sum(1) >= 2).astype(int)
    # data-quality defects
    df.loc[df.sample(n=400, random_state=seed).index, "agent_p_reject"] = np.nan                      # agent timeouts (no decision)
    df.loc[df.agent_p_reject.isna(), ["agent_reject", "agent_confidence"]] = np.nan
    df = pd.concat([df, df.sample(n=250, random_state=seed + 1)], ignore_index=True)
    return df, g.drop(columns=["_ev"])


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs05"), exist_ok=True)
    d, g = generate(); d.to_csv(os.path.join(here, "cs05", "reviews.csv.gz"), index=False); g.to_csv(os.path.join(here, "cs05", "gold_panel.csv.gz"), index=False)
    dd = d.drop_duplicates("merchant_id"); m = dd.merge(g[["merchant_id", "gold_reject"]], on="merchant_id")
    print(len(dd), "reviews | risky", dd._risky.mean().round(4), "| analyst reject", dd.analyst_reject.mean().round(4), "| agent reject", dd.agent_reject.mean().round(4))
    print("vs gold: analyst acc", (m.analyst_reject == m.gold_reject).mean().round(4), "agent acc", (m.agent_reject == m.gold_reject).mean().round(4), "always-approve", (m.gold_reject == 0).mean().round(4))
    print("vs truth: analyst", (dd.analyst_reject == dd._risky).mean().round(4), "agent", (dd.agent_reject == dd._risky).mean().round(4), "gold", (m.gold_reject == m._risky).mean().round(4))
