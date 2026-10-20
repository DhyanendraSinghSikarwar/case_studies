"""
SYNTHETIC DATA GENERATOR - CASE STUDY 30 (PhonePe-style AI-first customer support: intent, resolution and CSAT)
==============================================================================================================
THIS DATA IS SYNTHETIC. Support tickets, chats and CSAT surveys are confidential.

120,000 support contacts over 8 weeks across 12 issue types (some routine, some high-stakes such as fraud
complaints or wrong-recipient transfers). 95% of customers are served AI-first (bot attempts, escalates to a
human when it is unsure or the intent is not automatable); a RANDOM 5% HOLDOUT is served human-only.
Recorded per contact: language, true intent, the bot's predicted intent and confidence, whether the bot CLAIMED
resolution (closed the ticket), whether it was ESCALATED, handling time, whether the customer RE-CONTACTED on the
same issue within 7 days (the real test of resolution), and a CSAT rating (1-5) that only ~12% of customers give.
Survey response depends on experience (unhappy and very happy customers respond more), so CSAT among responders
is a BIASED picture. A latent satisfaction drives the rating.
The bot over-claims resolution on a few intents (it closes with a generic article), which is the classic
"resolution rate vs reality" problem.

Calibration anchors (reference file, Case Study 30): "over 92%" of queries resolved by AI; "one support agent for
every 20 million transactions"; CSAT 70%; 30-50 seconds saved per interaction; AI is first line, agents escalate.
Rates are our assumptions (decision.md D-30-02). Hidden truth columns start with "_".

Output: data/cs30/contacts.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.special import expit

SEED = 42
INTENTS = ["payment_failed_debited", "refund_status", "kyc_update", "app_login_issue", "recharge_bill_failed", "transaction_history", "wrong_recipient_transfer",
           "fraud_complaint", "account_blocked", "autopay_mandate", "cashback_missing", "merchant_dispute"]
P = np.array([0.18, 0.12, 0.08, 0.10, 0.10, 0.07, 0.04, 0.03, 0.05, 0.07, 0.10, 0.06])
AUTOMATABLE = {"payment_failed_debited": 0.85, "refund_status": 0.95, "kyc_update": 0.80, "app_login_issue": 0.90, "recharge_bill_failed": 0.88, "transaction_history": 0.98,
               "wrong_recipient_transfer": 0.10, "fraud_complaint": 0.05, "account_blocked": 0.30, "autopay_mandate": 0.85, "cashback_missing": 0.55, "merchant_dispute": 0.25}   # P(bot CAN truly fix)
OVERCLAIM = {"cashback_missing": 0.55, "merchant_dispute": 0.50, "account_blocked": 0.35, "payment_failed_debited": 0.10}                                                      # P(bot closes anyway when it cannot fix)


def generate(seed=SEED, n=120_000):
    rng = np.random.default_rng(seed)
    week = rng.integers(1, 9, n); lang = rng.choice(["english", "hindi", "hinglish", "regional"], n, p=[0.28, 0.32, 0.28, 0.12])
    ti = rng.choice(len(INTENTS), n, p=P); intent = np.array(INTENTS)[ti]
    holdout = (rng.random(n) < 0.05).astype(int)
    lang_pen = pd.Series(lang).map({"english": 0.0, "hindi": 0.35, "hinglish": 0.20, "regional": 0.70}).values
    # intent classification
    conf = np.clip(rng.beta(7, 2.2, n) - 0.16 * lang_pen + rng.normal(0, 0.03, n), 0.05, 0.99); correct = rng.random(n) < np.clip(0.55 + 0.5 * conf, 0.3, 0.995)
    pred = np.where(correct, ti, rng.integers(0, len(INTENTS), n))
    can_fix = rng.random(n) < pd.Series(intent).map(AUTOMATABLE).values * np.where(lang_pen > 0.5, 0.88, 1.0)
    over = rng.random(n) < pd.Series(intent).map(OVERCLAIM).fillna(0.75).values
    ai = holdout == 0
    attempt_close = ai & (conf >= 0.20) & (can_fix | over)                                    # bot closes the ticket
    escalated = ai & ~attempt_close
    true_resolved_bot = attempt_close & can_fix & correct
    # human outcomes
    human_fix = rng.random(n) < expit(1.9 - 0.35 * pd.Series(intent).isin(["fraud_complaint", "wrong_recipient_transfer", "merchant_dispute"]).values + rng.normal(0, 0.3, n))
    handled_by_human = (~ai) | escalated
    resolved = np.where(attempt_close, true_resolved_bot | (rng.random(n) < 0.04), human_fix)
    recontact = ~resolved & (rng.random(n) < 0.72) | (resolved & (rng.random(n) < 0.04))
    minutes = np.where(attempt_close, np.round(rng.exponential(0.7, n) + 0.2, 2), np.where(escalated, np.round(np.exp(rng.normal(np.log(10.5), 0.5, n)) + 1.5, 2), np.round(np.exp(rng.normal(np.log(9.0), 0.5, n)), 2)))
    wait = np.where(attempt_close, 0.1, np.where(escalated, np.round(rng.exponential(6, n), 1), np.round(rng.exponential(9, n), 1)))
    # latent satisfaction -> CSAT rating; survey response depends on experience
    sat = 0.9 * np.where(resolved, 1.0, -1.1) - 0.04 * np.minimum(minutes, 30) - 0.03 * wait + 0.3 * attempt_close * resolved - 0.45 * (attempt_close & ~resolved) + rng.normal(0, 0.8, n) + 3.4
    csat = np.clip(np.round(sat), 1, 5)
    p_resp = expit(-2.5 + 0.55 * (csat <= 2) + 0.35 * (csat == 5) - 0.1 * attempt_close)
    responded = rng.random(n) < p_resp
    df = pd.DataFrame({"contact_id": [f"SC{i:06d}" for i in range(n)], "week": week, "language": lang, "served_ai_first": ai.astype(int), "predicted_intent": np.array(INTENTS)[pred],
                       "intent_confidence": conf.round(3), "bot_closed": attempt_close.astype(int), "escalated_to_human": escalated.astype(int), "handling_minutes": minutes, "wait_minutes": wait,
                       "recontact_7d": recontact.astype(int), "csat": np.where(responded, csat, np.nan), "_intent": intent, "_resolved": resolved.astype(int), "_csat_latent": csat})
    df.loc[df.sample(n=500, random_state=seed).index, "handling_minutes"] = np.nan                  # timer lost on abrupt chat close
    df = pd.concat([df, df.sample(n=700, random_state=seed + 1)], ignore_index=True)
    df.loc[df.sample(n=40, random_state=seed + 2).index, "csat"] = 0                                 # survey widget returns 0 (invalid rating)
    return df


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs30"), exist_ok=True)
    d = generate(); d.to_csv(os.path.join(here, "cs30", "contacts.csv.gz"), index=False)
    dd = d.drop_duplicates("contact_id"); a = dd[dd.served_ai_first == 1]
    print(len(dd), "contacts | bot-closed", a.bot_closed.mean().round(3), "| escalated", a.escalated_to_human.mean().round(3))
    print("true resolution: AI-first", a._resolved.mean().round(3), "holdout", dd[dd.served_ai_first == 0]._resolved.mean().round(3), "| bot-closed true res", a[a.bot_closed == 1]._resolved.mean().round(3))
    print("recontact", dd.groupby("served_ai_first").recontact_7d.mean().round(3).to_dict(), "| CSAT>=4 among responders", (dd[dd.csat.between(1, 5)].csat >= 4).mean().round(3), "response rate", dd.csat.notna().mean().round(3))
    print("handling min", dd.groupby("served_ai_first").handling_minutes.mean().round(2).to_dict())
