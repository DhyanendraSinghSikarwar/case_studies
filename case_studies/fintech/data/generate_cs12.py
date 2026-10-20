"""
SYNTHETIC DATA GENERATOR - CASE STUDY 12 (Navi-style personal-loan book + bucket-wise collections)
=================================================================================================
THIS DATA IS SYNTHETIC. Loan-level repayment data is confidential.

A personal-loan book of 60,000 loans originated monthly Jan-Dec 2024 (12 vintages) and observed
monthly to Dec 2025. Each month every live loan sits in a delinquency bucket:
  Current (0 DPD) | B1 (1-29) | B2 (30-59) | B3 (60-89) | NPA (90+) | Closed
Transitions depend on borrower risk, bucket, and the collections treatment (a delinquent account can
cure, stay in its bucket after a partial payment, or roll forward):
  * 0-29 DPD  : digital nudges for everyone (documented)
  * 30-89 DPD : tele-calling with limited capacity (documented "100+ tele-callers")
                - historical policy: call the OLDEST delinquency first (B3 before B2), capacity 45%
                - Apr-Sep 2025 PILOT: calls assigned AT RANDOM (50%) to measure the call effect
  * 90+       : field agencies + skip tracing (documented); small cure probability
Calibration anchors (reference file, Case Study 12): "over 85% had CIBIL scores greater than 725";
collection efficiency "96.63%"; bucket policy as documented. Effect sizes are our assumptions
(decision.md D-12-02 ... D-12-04).

Outputs: data/cs12/loans.csv and data/cs12/performance_monthly.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.special import expit

SEED = 42
N_LOANS = 60_000
VINTAGES = pd.period_range("2024-01", "2024-12", freq="M")
END = pd.Period("2025-12", freq="M")
PILOT = [pd.Period(m, freq="M") for m in ("2025-04", "2025-05", "2025-06", "2025-07", "2025-08", "2025-09")]
STATES = ["Current", "B1", "B2", "B3", "NPA", "Closed"]


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    vint = VINTAGES[rng.integers(0, 12, N_LOANS)]
    # credit quality improves slightly in later vintages after a policy tightening in Jul 2024
    tighten = np.array([v >= pd.Period("2024-07", freq="M") for v in vint])
    bureau = np.clip(np.round(rng.normal(765 + 10 * tighten, 38, N_LOANS)), 600, 900)
    income = rng.choice(["<3L", "3-6L", "6-12L", ">12L"], N_LOANS, p=[0.18, 0.40, 0.30, 0.12])
    emp = rng.choice(["salaried", "self-employed"], N_LOANS, p=[0.72, 0.28])
    tier = rng.choice(["Tier 1", "Tier 2", "Tier 3"], N_LOANS, p=[0.45, 0.35, 0.20])
    channel = rng.choice(["Organic app", "Performance marketing", "Partner / DSA"], N_LOANS, p=[0.45, 0.35, 0.20])
    principal = np.clip(np.round(np.exp(rng.normal(np.log(60_000), 0.7, N_LOANS)), -3), 10_000, 200_000)
    tenure = rng.choice([6, 12, 18, 24, 36], N_LOANS, p=[0.10, 0.30, 0.20, 0.25, 0.15])
    risk = (-(bureau - 765) / 40 + 0.35 * (income == "<3L") - 0.25 * (income == ">12L") + 0.30 * (emp == "self-employed")
            + 0.15 * (tier == "Tier 3") + 0.25 * (channel == "Partner / DSA") + rng.normal(0, 0.6, N_LOANS))
    apr = np.clip(np.round(0.16 + 0.025 * risk + rng.normal(0, 0.01, N_LOANS), 4), 0.12, 0.36)
    r_m = apr / 12
    emi = np.round(principal * r_m / (1 - (1 + r_m) ** (-tenure)), 0)
    cac = np.select([channel == "Organic app", channel == "Performance marketing"], [400, 1800], 2500) * np.exp(rng.normal(0, 0.2, N_LOANS))
    loans = pd.DataFrame({"loan_id": [f"L{i:06d}" for i in range(1, N_LOANS + 1)], "vintage": vint.astype(str), "bureau_score": bureau,
                          "income_band": income, "employment": emp, "city_tier": tier, "channel": channel, "principal_inr": principal,
                          "tenure_months": tenure, "apr": apr, "emi_inr": emi, "cac_inr": np.round(cac, 0), "_risk": risk})

    # ---- monthly state machine ----
    months = pd.period_range(VINTAGES[0] + 1, END, freq="M")
    state = np.zeros(N_LOANS, int)                    # 0 Current .. 4 NPA, 5 Closed; -1 not yet originated
    start = np.array([(v - VINTAGES[0]).n + 1 for v in vint])
    paid_inst = np.zeros(N_LOANS)
    outstanding = principal.astype(float)
    recs = []
    for mi, m in enumerate(months):
        live = (start <= mi) & (state < 5)
        if not live.any():
            continue
        mob = mi - start + 1
        s0 = state.copy()
        z = risk
        # P(miss this month's EMI) by state; cure/roll dynamics
        p_miss_cur = expit(-4.3 + 0.9 * z + 0.15 * (mob <= 6))
        p_cure = {1: expit(1.0 - 0.6 * z), 2: expit(-0.6 - 0.6 * z), 3: expit(-1.3 - 0.6 * z), 4: expit(-3.0 - 0.3 * z)}
        # tele-calling allocation in B2/B3
        in_b23 = live & np.isin(s0, [2, 3])
        called = np.zeros(N_LOANS, bool)
        if m in PILOT:
            called = in_b23 & (rng.random(N_LOANS) < 0.5)
        else:
            idx = np.flatnonzero(in_b23)
            cap = int(0.45 * len(idx))
            order = idx[np.lexsort((rng.random(len(idx)), -s0[idx]))]       # oldest bucket first, random within
            called[order[:cap]] = True
        call_effect = np.where(called, 0.55 - 0.08 * np.clip(z, -2, 2), 0.0)   # log-odds boost to cure, larger for lower risk
        u = rng.random(N_LOANS)
        new = s0.copy()
        cur = live & (s0 == 0)
        new[cur & (u < p_miss_cur)] = 1
        u2 = rng.random(N_LOANS)
        for b in (1, 2, 3):
            mask = live & (s0 == b)
            pc = expit(np.log(p_cure[b] / (1 - p_cure[b])) + call_effect)
            cure = mask & (u < pc)
            stay = mask & ~cure & (u2 < expit(-1.3 - 0.3 * z + 0.3 * called))     # partial payment keeps the bucket
            new[cure] = 0
            new[stay] = b
            new[mask & ~cure & ~stay] = b + 1
        npa = live & (s0 == 4)
        new[npa & (u < p_cure[4])] = 0
        # payments: current & cured pay EMI (cure pays all arrears)
        due = np.where(live, emi * np.minimum(np.where(s0 >= 1, s0, 0) + 1, 4), 0.0)
        pay = np.where(live & (new == 0), np.minimum(due, emi * (s0.clip(0, 3) + 1)), np.where(live & (new < s0 + 1) & (new > 0), emi, 0.0))
        partial = live & (new > 0) & (rng.random(N_LOANS) < 0.25)
        pay = np.where(partial & (pay == 0), np.round(emi * rng.uniform(0.2, 0.8, N_LOANS)), pay)
        paid_inst += np.where(live & (new == 0), np.minimum(s0.clip(0, 3) + 1, tenure - paid_inst), 0)
        prin_part = np.where(live, np.minimum(outstanding, pay * 0.8), 0)
        outstanding = np.maximum(outstanding - prin_part, 0)
        closed = live & ((paid_inst >= tenure) | (rng.random(N_LOANS) < np.where(new == 0, 0.012, 0)))   # maturity or prepayment
        new[closed] = 5
        rows = np.flatnonzero(live)
        recs.append(pd.DataFrame({"loan_id": loans.loan_id.values[rows], "month": str(m), "mob": mob[rows],
                                  "bucket_start": np.array(STATES)[s0[rows]], "bucket_end": np.array(STATES)[new[rows]],
                                  "emi_due_inr": due[rows], "amount_paid_inr": pay[rows].round(0), "outstanding_inr": outstanding[rows].round(0),
                                  "tele_called": called[rows].astype(int), "pilot_month": int(m in PILOT)}))
        state = new
    perf = pd.concat(recs, ignore_index=True)
    # ---- data-quality issues ----
    dup = perf.sample(n=600, random_state=seed)                                      # duplicated snapshot rows (re-run of a month's ETL)
    perf = pd.concat([perf, dup], ignore_index=True)
    perf.loc[perf.sample(n=80, random_state=seed + 1).index, "amount_paid_inr"] = -1  # reversal coded as -1
    loans.loc[loans.sample(n=50, random_state=seed + 2).index, "bureau_score"] = np.nan  # bureau no-hit
    return loans.drop(columns="_risk"), perf


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs12"), exist_ok=True)
    l, p = generate()
    l.to_csv(os.path.join(here, "cs12", "loans.csv"), index=False)
    p.to_csv(os.path.join(here, "cs12", "performance_monthly.csv.gz"), index=False)
    print(len(l), "loans;", len(p), "loan-months")
