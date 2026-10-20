"""
SYNTHETIC DATA GENERATOR - CASE STUDY 27 (Policybazaar-style call analytics, intent frequency and dialler efficiency)
====================================================================================================================
THIS DATA IS SYNTHETIC. Call audio and dialler logs are confidential. We do not simulate audio; we simulate the
OUTPUTS and records an analytics team works with.

Part A - intent frequency: 60,000 inbound customer calls, each with a transcript-derived INTENT from an ASR+NLP
pipeline (with confusions, and Hindi-vs-English word error rates). The true intent mix includes "cashless hospital
network request" as a mid-ranked intent that is easy to under-count (rare in the pre-period, rising over 12 weeks).
Part B - compliance QA: 8,000 calls re-listened by QA (gold), with the model's compliance-breach / mis-selling flag.
Part C - dialler experiment: 8 weeks of outbound dialling by 120 agents in teams; a RANDOMISED switch from a
"static list" dialler to a "predictive / adaptive" dialler by team (cluster-randomised, 24 teams), plus callback
scheduling. Outcomes per agent-day: dials, connects, talk time, wrap time, idle time, sales, callbacks and
callback delay. Call efficiency = talk time share of logged-in time.

Calibration anchors (reference file, Case Study 27): "only 1-2% of ~10 million monthly call minutes could be
quality-checked"; cashless-hospital requests the "7th-8th most common"; dialler "50% increase in dial-out rates",
"call efficiency 40% -> 85%", "callback time 30-45 minutes"; WER ND. Rates are our assumptions (D-27-02).
Hidden truth columns start with "_".

Outputs: data/cs27/calls.csv.gz, data/cs27/qa_audit.csv.gz, data/cs27/dialler_agent_days.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.special import expit

SEED = 42
INTENTS = ["renewal_reminder", "premium_quote", "policy_status", "claim_status", "payment_issue", "document_request", "cashless_hospital", "coverage_query",
           "cancellation_refund", "portability", "endorsement", "agent_complaint", "other"]
P0 = np.array([0.20, 0.17, 0.12, 0.10, 0.08, 0.07, 0.035, 0.07, 0.05, 0.03, 0.04, 0.02, 0.045])


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    # ---- Part A: intents over 12 weeks ----
    n = 60_000; week = rng.integers(1, 13, n); lang = rng.choice(["hindi", "english", "hinglish"], n, p=[0.45, 0.25, 0.30])
    rows = []
    P = np.tile(P0, (12, 1)); P[:, INTENTS.index("cashless_hospital")] *= 1 + 0.13 * np.arange(12); P = P / P.sum(1, keepdims=True)           # cashless requests grow
    true_i = np.array([rng.choice(len(INTENTS), p=P[w - 1]) for w in week])
    wer = pd.Series(lang).map({"hindi": 0.22, "english": 0.09, "hinglish": 0.17}).values * np.exp(rng.normal(0, 0.3, n))
    p_ok = np.clip(0.93 - 1.3 * wer, 0.35, 0.99)
    ok = rng.random(n) < p_ok; confuse = np.array([rng.choice([j for j in range(len(INTENTS)) if j != t], p=None) if True else t for t in true_i])
    near = {"claim_status": "cashless_hospital", "cashless_hospital": "claim_status", "premium_quote": "coverage_query", "coverage_query": "premium_quote",
            "policy_status": "document_request", "document_request": "policy_status", "renewal_reminder": "premium_quote", "payment_issue": "policy_status", "portability": "coverage_query"}
    pred = np.where(ok, true_i, np.where(rng.random(n) < 0.55, [INTENTS.index(near.get(INTENTS[t], "other")) for t in true_i], confuse))
    dur = np.round(np.exp(rng.normal(np.log(5.5), 0.6, n)), 1)
    calls = pd.DataFrame({"call_id": [f"CALL{i:06d}" for i in range(n)], "week": week, "language": lang, "duration_min": dur, "asr_wer": wer.round(3),
                          "predicted_intent": np.array(INTENTS)[pred], "_true_intent": np.array(INTENTS)[true_i]})
    # ---- Part B: compliance QA ----
    m = 8000; breach = rng.random(m) < 0.06; sc = np.where(breach, rng.beta(4, 3, m), rng.beta(2, 6, m))
    qa = pd.DataFrame({"call_id": [f"QA{i:05d}" for i in range(m)], "qa_breach": breach.astype(int), "model_breach_score": sc.round(3), "language": rng.choice(["hindi", "english", "hinglish"], m, p=[0.45, 0.25, 0.30])})
    # ---- Part C: cluster-randomised dialler ----
    teams = np.repeat(np.arange(24), 5); arm = np.zeros(24, int); arm[rng.permutation(24)[:12]] = 1
    rows = []
    agent_skill = rng.normal(0, 0.25, 120)
    team_eff = rng.normal(0, 0.12, 24)
    for a in range(120):
        t = teams[a]; tr = arm[t]
        for d in range(40):
            logged = 480 * np.exp(rng.normal(0, 0.05))
            connect_rate = np.clip(0.26 + 0.04 * tr + 0.05 * agent_skill[a] + rng.normal(0, 0.03), 0.05, 0.6)
            dial_rate_h = np.exp(np.log(22) + 0.28 * tr * (1 + 0.1 * team_eff[t]) + 0.1 * agent_skill[a] + rng.normal(0, 0.1))            # dials per hour (+~32% with predictive dialler)
            dials = int(rng.poisson(dial_rate_h * 6.5)); conn = rng.binomial(dials, connect_rate)
            talk_share = np.clip(0.40 + 0.20 * tr + 0.08 * agent_skill[a] + team_eff[t] * 0.2 + rng.normal(0, 0.05), 0.15, 0.9)
            talk = logged * talk_share; sales = rng.binomial(conn, np.clip(0.055 + 0.012 * agent_skill[a] + 0.004 * tr, 0.01, 0.2))
            cb_delay = np.exp(rng.normal(np.log(260 if tr == 0 else 40), 0.5))                                                          # callback delay minutes
            rows.append((f"AG{a:03d}", f"T{t:02d}", tr, d + 1, round(logged), dials, conn, round(talk), sales, round(cb_delay, 1), round(logged - talk)))
    dl = pd.DataFrame(rows, columns=["agent_id", "team_id", "new_dialler", "day", "logged_in_min", "dials", "connects", "talk_min", "sales", "avg_callback_delay_min", "non_talk_min"])
    # data-quality defects
    calls.loc[calls.sample(n=250, random_state=seed).index, "predicted_intent"] = ""                    # ASR failed
    calls = pd.concat([calls, calls.sample(n=300, random_state=seed + 1)], ignore_index=True)
    dl.loc[dl.sample(n=60, random_state=seed + 2).index, "logged_in_min"] = 0                           # agents logged in via the wrong ID
    return calls, qa, dl


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs27"), exist_ok=True)
    c, q, d = generate(); c.to_csv(os.path.join(here, "cs27", "calls.csv.gz"), index=False); q.to_csv(os.path.join(here, "cs27", "qa_audit.csv.gz"), index=False); d.to_csv(os.path.join(here, "cs27", "dialler_agent_days.csv.gz"), index=False)
    cc = c.drop_duplicates("call_id"); print("intent accuracy", (cc.predicted_intent == cc._true_intent).mean().round(4))
    print(cc._true_intent.value_counts().rank(ascending=False)["cashless_hospital"], cc.predicted_intent.value_counts().rank(ascending=False).get("cashless_hospital"))
    print(d[d.logged_in_min > 0].groupby("new_dialler").agg(dials=("dials", "mean"), talk=("talk_min", "mean"), li=("logged_in_min", "mean"), sales=("sales", "mean")).round(2))
