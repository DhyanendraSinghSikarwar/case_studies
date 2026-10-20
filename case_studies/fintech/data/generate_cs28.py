"""
SYNTHETIC DATA GENERATOR - CASE STUDY 28 (Policybazaar-style speed-to-lead with AI voice qualification and routing)
==================================================================================================================
THIS DATA IS SYNTHETIC. Lead and call data are confidential.

Part A - contact delay and conversion (the case for speed): 150,000 leads over 6 weeks, each with a form-fill
time, the delay until the first contact attempt, whether the lead was reached, and whether it converted. Intent
decays with time: the chance of REACHING a lead falls steeply in the first minutes and conversion given reach
falls too. Delay is mostly set by RM capacity (queues at peak hours), so it is confounded with hour of day and
lead quality: high-value leads were manually prioritised and called faster.
Part B - randomised speed test: in week 4-5 a RANDOM 30% of leads (all lead types) were first-touched by an AI
voice call within 60 seconds (the rest follow the existing RM queue). Outcomes: qualified, routed (AI-handled /
RM handoff / scheduled callback), converted.
Part C - capacity-constrained routing: 40 RMs, about 80 calls a day; the simulation lets us compare routing rules.

Calibration anchors (reference file, Case Study 28): RMs took "8-12 minutes" to reach a new lead; ~80 calls per RM
a day; 57,000+ connected calls a day; response time < 60 s; qualified-lead rate 5-7%; level-0 containment 67%;
routing 67% AI-handled, 7% RM, 26% scheduled callback. Rates are our assumptions (decision.md D-28-02).
Hidden truth columns start with "_".

Outputs: data/cs28/leads.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.special import expit

SEED = 42


def generate(seed=SEED, n=150_000):
    rng = np.random.default_rng(seed)
    day = rng.integers(0, 42, n); hour = np.clip(np.round(rng.normal(14, 4.2, n)), 8, 22).astype(int)
    q = rng.normal(0, 1, n)                                                           # latent lead intent / quality
    product = rng.choice(["motor", "health", "term_life", "travel"], n, p=[0.35, 0.30, 0.20, 0.15])
    value = np.where(product == "term_life", 1.0, np.where(product == "health", 0.7, np.where(product == "motor", 0.5, 0.2)))
    ai_arm = ((day >= 21) & (day < 35) & (rng.random(n) < 0.30)).astype(int)         # randomised AI-first-touch during weeks 4-5
    # RM delay (minutes): queue grows at peak hours; high-value / high-quality leads jump the queue (confounding)
    peak = np.exp(-((hour - 12) / 3.0) ** 2) + 0.7 * np.exp(-((hour - 18) / 2.5) ** 2)
    base_delay = np.exp(rng.normal(np.log(5 + 15 * peak), 0.7, n)) * np.exp(-0.35 * np.clip(q, -2, 2)) * np.exp(-0.5 * value)
    delay = np.where(ai_arm == 1, np.round(rng.uniform(0.3, 1.0, n), 2), np.round(base_delay, 2))
    # reach: decays with delay in minutes
    p_reach = expit(1.1 + 0.35 * q - 0.045 * np.minimum(delay, 60) - 0.0009 * np.maximum(delay - 60, 0) + 0.2 * (hour >= 10) - 0.25 * (hour >= 20))
    reached = (rng.random(n) < p_reach).astype(int)
    # conversion given reach: depends on intent, product value and speed (extra decay in first 30 min)
    p_conv = expit(-3.5 + 0.9 * q + 0.8 * value - 0.018 * np.minimum(delay, 40) - 0.15 * (ai_arm == 1) * 0)
    converted = ((reached == 1) & (rng.random(n) < p_conv)).astype(int)
    # AI qualification and routing for AI-touched leads
    qual_p = expit(-3.0 + 0.8 * q + 0.5 * value); qualified = ((ai_arm == 1) & (reached == 1) & (rng.random(n) < expit(-3.3 + 0.9 * q + 0.4 * value))).astype(int)
    r = rng.random(n)
    route = np.where(ai_arm == 0, "", np.where(reached == 0, "no_answer_retry", np.where(qualified == 1, "rm_handoff", np.where(r < 0.72, "ai_handled", "scheduled_callback"))))
    df = pd.DataFrame({"lead_id": [f"LD{i:06d}" for i in range(n)], "day": day + 1, "hour": hour, "product": product, "ai_first_touch": ai_arm, "first_contact_delay_min": delay,
                       "reached": reached, "qualified": qualified, "route": route, "converted": converted, "_q": q})
    # data-quality defects
    df.loc[df.sample(n=1500, random_state=seed).index, "first_contact_delay_min"] = np.nan             # call-attempt timestamp missing
    df.loc[df.sample(n=300, random_state=seed + 1).index, "first_contact_delay_min"] = -1.0            # clock skew between form and dialler servers
    df = pd.concat([df, df.sample(n=800, random_state=seed + 2)], ignore_index=True)
    return df


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs28"), exist_ok=True)
    d = generate(); d.to_csv(os.path.join(here, "cs28", "leads.csv.gz"), index=False)
    dd = d.drop_duplicates("lead_id"); dd = dd[dd.first_contact_delay_min.notna() & (dd.first_contact_delay_min >= 0)]
    print(len(dd), "leads | median RM delay", dd[dd.ai_first_touch == 0].first_contact_delay_min.median().round(1), "| reach", dd.groupby("ai_first_touch").reached.mean().round(3).to_dict(), "| conv", dd.groupby("ai_first_touch").converted.mean().round(4).to_dict())
    x = dd[dd.ai_first_touch == 0]; print(x.groupby(pd.cut(x.first_contact_delay_min, [0, 1, 5, 10, 30, 60, 1e4])).agg(reach=("reached", "mean"), conv=("converted", "mean"), n=("lead_id", "size")).round(4))
