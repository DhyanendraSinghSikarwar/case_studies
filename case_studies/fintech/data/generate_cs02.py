"""
SYNTHETIC DATA GENERATOR - CASE STUDY 2 (Cashfree-style card-decline diagnosis: authentication vs authorisation)
==============================================================================================================
THIS DATA IS SYNTHETIC. Processor-level card logs are confidential.

A food-delivery merchant routes card payments across two processors with similar volumes:
  P1 (premium) and P2 (cheaper, ~0.15% lower fee). Every card attempt passes two stages:
  1. AUTHENTICATION (3-D Secure / OTP): frictionless or challenge flow
  2. AUTHORISATION (issuer approves funds / risk)
P2's gap is built (as documented) into AUTHENTICATION - OTP delivery and ACS (issuer access-control
server) timeouts - while AUTHORISATION is almost the same on both processors. Customers retry
failed orders, so attempt-level and order-level success differ.

Calibration anchors (reference file, Case Study 2): "similar volumes but different success rates";
"Processor 2's gap was due to 'higher authentication failures', while authorisation declines were
about equal"; fix = authenticate on P1, authorise on P2; impact "2% increase in success rate";
FlowWise uses SR over "last 15 or 30 minutes" with threshold fallback (e.g., 70%).
Sizes are our assumptions (decision.md D-2b-02).

Output: data/cs02/card_attempts.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.special import expit

SEED = 42
N_ORDERS = 220_000
START = pd.Timestamp("2025-11-03"); DAYS = 28
ISSUERS = ["HDFC", "SBI", "ICICI", "Axis", "Kotak", "IndusInd", "Yes", "IDFC First", "AU SFB", "Others"]
ISS_P = [0.22, 0.20, 0.16, 0.11, 0.07, 0.05, 0.04, 0.04, 0.03, 0.08]
ACS_QUALITY = dict(zip(ISSUERS, [0.4, -0.6, 0.3, 0.1, 0.2, 0.0, -0.3, 0.1, -0.4, -0.5]))   # issuer ACS reliability (log-odds)


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    order_ts = START + pd.to_timedelta(rng.uniform(0, DAYS * 86400, N_ORDERS), unit="s")
    issuer = rng.choice(ISSUERS, N_ORDERS, p=ISS_P)
    network = rng.choice(["Visa", "Mastercard", "RuPay"], N_ORDERS, p=[0.48, 0.32, 0.20])
    ctype = rng.choice(["credit", "debit"], N_ORDERS, p=[0.45, 0.55])
    amount = np.round(np.exp(rng.normal(np.log(420), 0.6, N_ORDERS)), 0)
    frictionless_prob = expit(0.2 + 0.8 * (ctype == "credit") + 0.3 * (network == "Visa") - 0.002 * (amount - 420) / 10)
    rows = []
    done = np.zeros(N_ORDERS, bool)                                                        # order already paid
    alive = np.ones(N_ORDERS, bool); ts = order_ts
    for attempt in (1, 2, 3):
        if attempt > 1:
            alive = alive & ~done & (rng.random(N_ORDERS) < 0.55 - 0.1 * attempt)              # customers retry
            ts = ts + pd.to_timedelta(rng.uniform(20, 180, N_ORDERS), unit="s")
        idx = np.flatnonzero(alive)
        if len(idx) == 0: break
        proc = np.where(rng.random(N_ORDERS) < 0.5, "P1", "P2")
        fr = rng.random(N_ORDERS) < frictionless_prob
        hour = pd.DatetimeIndex(ts).hour.to_numpy()
        peak = (hour >= 19) & (hour <= 22)
        # authentication success
        z_a = (np.where(fr, 3.6, 1.9) + pd.Series(issuer).map(ACS_QUALITY).to_numpy()
               - np.where(proc == "P2", np.where(fr, 0.15, 0.85), 0.0) - 0.25 * peak * (proc == "P2"))
        auth_ok = rng.random(N_ORDERS) < expit(z_a)
        # authorisation success given authentication (issuer decision) - ~ same on both processors
        z_z = 2.4 + 0.3 * (ctype == "credit") - 0.25 * np.log(amount / 420) - 0.05 * (proc == "P2") - 0.2 * (issuer == "Others")
        authz_ok = rng.random(N_ORDERS) < expit(z_z)
        success = auth_ok & authz_ok
        a_reason = np.where(proc == "P2", rng.choice(["OTP not received", "OTP timeout / wrong OTP", "ACS error"], N_ORDERS, p=[0.45, 0.30, 0.25]),
                                                               rng.choice(["OTP not received", "OTP timeout / wrong OTP", "ACS error"], N_ORDERS, p=[0.25, 0.55, 0.20]))
        z_reason = rng.choice(["Insufficient funds", "Do not honour", "Risk decline", "Card expired / invalid"], N_ORDERS, p=[0.45, 0.30, 0.15, 0.10])
        reason = np.where(success, "none", np.where(~auth_ok, a_reason, z_reason))
        stage = np.where(success, "success", np.where(~auth_ok, "authentication", "authorisation"))
        rows.append(pd.DataFrame({"order_id": [f"O{i:07d}" for i in idx], "attempt_no": attempt, "timestamp": pd.DatetimeIndex(ts)[idx],
                                  "processor": proc[idx], "card_network": network[idx], "card_type": ctype[idx], "issuer_bank": issuer[idx],
                                  "amount_inr": amount[idx], "three_ds_flow": np.where(fr, "frictionless", "challenge")[idx],
                                  "auth_success": auth_ok[idx].astype(int), "authz_success": np.where(auth_ok, authz_ok, np.nan)[idx],
                                  "success": success[idx].astype(int), "failure_stage": stage[idx], "failure_reason": reason[idx]}))
        done[idx] |= success[idx]
    df = pd.concat(rows, ignore_index=True).sort_values("timestamp").reset_index(drop=True)
    df.insert(0, "attempt_id", [f"A{i:08d}" for i in range(1, len(df) + 1)])
    # data-quality issues: webhook replays (duplicate attempt rows) and missing issuer for some BINs
    df = pd.concat([df, df.sample(n=1500, random_state=seed)], ignore_index=True)
    df.loc[df.sample(frac=0.01, random_state=seed + 1).index, "issuer_bank"] = np.nan
    return df


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs02"), exist_ok=True)
    d = generate(); d.to_csv(os.path.join(here, "cs02", "card_attempts.csv.gz"), index=False)
    dd = d.drop_duplicates("attempt_id")
    print(len(dd), "attempts", dd.order_id.nunique(), "orders")
    print(dd.groupby("processor")[["auth_success", "authz_success", "success"]].mean().round(4))
