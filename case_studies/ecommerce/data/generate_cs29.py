"""
SYNTHETIC DATA GENERATOR - CASE STUDY 29 (food-delivery support automation: containment vs CSAT)
==============================================================================================
THIS DATA IS SYNTHETIC. Support tickets, chat logs and CSAT scores of Zomato or any other company are confidential.

Documented context (vendor-published, unaudited): the Zomato bot "Zia" uses larger Llama models for intent detection and
smaller ones for chat; with LLM-only escalation decisions daily containment is reported to have swung between roughly
50% and 80%, and a policy layer was added to stabilise it; first response time fell to under 10 seconds; the MongoDB
Nugget story quotes an 85% average query resolution rate and about 60% of tickets auto-resolved earlier.
None of these numbers is reproduced here; the simulation only borrows the structure.

Simulation: 56 days of order-support tickets (about 3,000 a day, a surge day with ~2x volume).
  * Phase 0 (days 0-13)  : legacy decision-tree bot for simple intents, everything else goes to humans.
  * Phase 1 (days 14-27) : LLM agent, escalation decided by the LLM alone (day-level drift in its threshold).
  * Phase 2 (days 28-55) : LLM agent + deterministic policy layer (safety keywords, payment risk, abuse score);
                           5% of tickets are randomly routed human-first (a randomised holdout).
Hidden truth (prefixed _): whether the ticket truly needs a human, abuse (refund fraud), safety issue, whether it was
actually resolved. Observed: intent, order data, LLM escalation score, fraud score, latency, CSAT survey (with
non-response), 72-hour re-contact.
Outputs: data/cs29/tickets.csv.gz
"""
import os
import numpy as np
import pandas as pd

SEED = 42
START = pd.Timestamp("2026-03-01"); DAYS = 56; SURGE_DAY = 36
INTENTS = ["where_is_order", "missing_item", "wrong_item", "food_quality", "refund_status", "payment_issue", "rider_behaviour", "cancel_order", "account_other"]
P_INT = np.array([0.30, 0.14, 0.08, 0.10, 0.12, 0.07, 0.05, 0.06, 0.08])
NH_BASE = np.array([-3.0, -1.2, -1.2, -0.9, -2.2, 0.0, 1.2, -2.4, -1.0])
TREE_SET = {"where_is_order", "cancel_order", "refund_status", "account_other", "missing_item"}
REFUND_INTENTS = {"missing_item", "wrong_item", "food_quality"}
TAU = 1.0


def sig(x): return 1 / (1 + np.exp(-x))


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    lat_day = np.exp(rng.normal(0, 0.22, DAYS)); lat_day[SURGE_DAY] = 1.9
    drift_day = rng.normal(0, 0.75, DAYS)                         # LLM threshold drift (shared within a day)
    vol = np.round(3000 * np.where(np.arange(DAYS) % 7 >= 5, 1.15, 1.0) * np.exp(rng.normal(0, 0.05, DAYS))).astype(int); vol[SURGE_DAY] *= 2
    day = np.repeat(np.arange(DAYS), vol); n = len(day)
    phase = np.where(day < 14, 0, np.where(day < 28, 1, 2))
    hw = np.ones(24) * 0.2; hw[[12, 13, 14]] = 1.6; hw[[19, 20, 21, 22]] = 2.0; hw[[8, 9, 10, 11, 15, 16, 17, 18, 23]] = 0.6; hw /= hw.sum()
    hour = rng.choice(24, n, p=hw); peak = np.isin(hour, [12, 13, 14, 19, 20, 21, 22]).astype(int)
    # intent mix drifts with the day's lateness
    w = np.tile(P_INT, (DAYS, 1)); w[:, 0] *= lat_day; w /= w.sum(1, keepdims=True)
    cw = w.cumsum(1); intent_i = (rng.random(n)[:, None] > cw[day]).sum(1); intent_i = np.minimum(intent_i, len(INTENTS) - 1); intent = np.array(INTENTS)[intent_i]
    order_value = np.round(np.exp(rng.normal(np.log(380), 0.6, n)), 0)
    late_min = np.round(rng.exponential(10 * lat_day[day]) + np.where(intent == "where_is_order", rng.exponential(12, n), 0), 1)
    abuse_user = rng.random(n) < 0.04
    prior_refund_ratio = np.where(abuse_user, rng.beta(4, 6, n), rng.beta(1, 12, n)); tenure = rng.geometric(0.04, n)
    n_tickets_30d = rng.poisson(0.8 + 3 * abuse_user)
    is_ref = np.isin(intent, list(REFUND_INTENTS))
    abuse = (is_ref & (rng.random(n) < 0.02 + 0.45 * abuse_user)).astype(int)
    abuse_score = np.round(sig(-2.2 + 2.0 * abuse + 4.0 * prior_refund_ratio + rng.normal(0, 0.8, n)), 3)
    safety = ((intent == "food_quality") & (rng.random(n) < 0.07)).astype(int)
    safety_kw = ((safety == 1) & (rng.random(n) < 0.85)) | ((intent == "food_quality") & (safety == 0) & (rng.random(n) < 0.01))
    cx = rng.normal(0, 1, n)
    nh_logit = NH_BASE[intent_i] + 0.7 * cx + 0.5 * (order_value > 1200) + 0.5 * abuse + 3.0 * safety + 0.02 * np.where(intent == "where_is_order", late_min, 0)
    needs = (rng.random(n) < sig(nh_logit)).astype(int); needs[safety == 1] = 1
    sentiment = np.round(rng.normal(-0.2 - 0.6 * needs - 0.01 * late_min, 0.8), 2)
    chat_turns = 2 + rng.poisson(1.5 + 2.0 * needs)
    llm_score = np.round(1.4 * needs + rng.normal(0, 1.0, n), 3)
    holdout = (phase == 2) & (rng.random(n) < 0.05)
    # routing
    tree_ok = np.isin(intent, list(TREE_SET)) & (rng.random(n) < 0.85)
    policy = ((intent == "rider_behaviour") | ((intent == "payment_issue") & (order_value > 1000)) | safety_kw | (is_ref & ((abuse_score > 0.5) | (order_value > 1500)))) & (phase == 2)
    drift = drift_day[day]
    esc_llm = (llm_score + np.where(phase == 1, drift, 0.12 * drift) + 0.2 * peak * (phase == 1)) > TAU
    contained = np.where(phase == 0, tree_ok, np.where(phase == 1, ~esc_llm, ~(esc_llm | policy)))
    contained = contained & ~holdout
    arm = np.where(holdout, "human_first", "bot_pipeline")
    handled_by = np.where(contained, "bot", "human")
    # outcomes
    u = rng.random((6, n))
    p_res_bot = np.where(needs == 1, np.where(phase == 0, 0.20, 0.30), np.where(phase == 0, 0.90, 0.94)); p_res_bot = np.where(safety == 1, 0.05, p_res_bot)
    resolved = np.where(contained, u[0] < p_res_bot, u[0] < 0.93).astype(int)
    abandoned = (contained & (resolved == 0) & (u[1] < 0.55)).astype(int)
    recontact = np.where(resolved == 1, u[2] < np.where(contained, 0.04, 0.05), u[2] < np.where(contained, 0.65, 0.40)).astype(int)
    # latency (seconds to the first meaningful response the customer sees)
    surge = (day == SURGE_DAY)
    bot_lat = np.exp(rng.normal(np.log(np.where(phase == 0, 28, 6)), 0.5, n)) * (1 + 0.4 * peak) * (1 + 1.5 * surge)
    human_wait = np.exp(rng.normal(np.log(180), 0.7, n)) * (1 + 1.3 * peak) * (1 + 1.2 * surge)
    first_response_s = np.round(np.where(holdout | ((phase == 0) & ~contained), human_wait, bot_lat), 1)   # escalated LLM tickets see the bot first
    handle_wait_s = np.round(np.where(~contained, np.where(holdout | (phase == 0), human_wait, bot_lat + human_wait), bot_lat), 1)
    # refunds
    refund_req = is_ref.astype(int); refund_inr = np.round(order_value * rng.uniform(0.3, 1.0, n) * refund_req, 0)
    appr_bot = np.where(phase == 0, prior_refund_ratio < 0.3, np.where(phase == 1, rng.random(n) < 0.95, (abuse_score < 0.5) & (order_value < 1500)))
    appr_human = np.where(abuse == 1, rng.random(n) < 0.35, rng.random(n) < 0.90)
    refund_approved = ((refund_req == 1) & np.where(contained, appr_bot, appr_human)).astype(int)
    leak_inr = refund_approved * abuse * refund_inr
    # CSAT latent (driven by outcome and the wait to full resolution) and survey response (non-response depends on the experience)
    latent = 2.4 + 1.6 * resolved - 0.35 * abandoned + 0.25 * (~contained) - 0.003 * np.minimum(handle_wait_s, 300) + rng.normal(0, 0.8, n)
    p_resp = 0.10 + 0.10 * (latent < 2.2) + 0.04 * (latent > 4.3) + 0.05 * (~contained); p_resp = np.where(abandoned == 1, p_resp * 0.3, p_resp)
    responded = rng.random(n) < p_resp
    csat = np.where(responded, np.clip(np.round(latent), 1, 5), np.nan)
    df = pd.DataFrame({
        "ticket_id": np.arange(n), "day": day, "hour": hour, "peak_hour": peak, "phase": phase, "arm": arm, "intent": intent,
        "order_value_inr": order_value, "late_min": late_min, "prior_refund_ratio": np.round(prior_refund_ratio, 3), "tenure_orders": tenure,
        "tickets_30d": n_tickets_30d, "chat_turns": chat_turns, "sentiment": sentiment, "llm_escalation_score": llm_score, "abuse_score": abuse_score,
        "safety_keyword": safety_kw.astype(int), "handled_by": handled_by, "first_response_s": first_response_s, "time_to_resolution_wait_s": handle_wait_s,
        "abandoned": abandoned, "recontact_72h": recontact, "refund_requested": refund_req, "refund_inr": refund_inr, "refund_approved": refund_approved, "csat": csat,
        "_needs_human": needs, "_abuse": abuse, "_safety": safety, "_resolved": resolved, "_leak_inr": leak_inr, "_complexity": np.round(cx, 3)})
    df["created_ts"] = START + pd.to_timedelta(df.day, unit="D") + pd.to_timedelta(df.hour * 3600 + rng.integers(0, 3600, n), unit="s")
    df["user_id"] = rng.integers(0, 150_000, n)
    # data-quality defects
    dup = df.sample(n=1200, random_state=seed); df = pd.concat([df, dup], ignore_index=True)
    bad = rng.choice(len(df), 150, replace=False); df.loc[bad, "csat"] = rng.choice([0, 6, 9], 150)
    neg = rng.choice(len(df), 50, replace=False); df.loc[neg, "first_response_s"] = -df.loc[neg, "first_response_s"]
    miss = rng.choice(len(df), int(0.008 * len(df)), replace=False); df.loc[miss, "intent"] = None
    qa = rng.choice(len(df), 300, replace=False); df.loc[qa, "user_id"] = -1
    return df


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs29"), exist_ok=True)
    d = generate(); d.to_csv(os.path.join(here, "cs29", "tickets.csv.gz"), index=False); print(len(d), "tickets")
