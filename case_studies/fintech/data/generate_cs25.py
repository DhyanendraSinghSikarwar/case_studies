"""
SYNTHETIC DATA GENERATOR - CASE STUDY 25 (ICICI Lombard-style health-claims copilot: OCR + LLM decision support)
==============================================================================================================
THIS DATA IS SYNTHETIC. Health claim documents and adjudication data are confidential. We do not simulate
documents or LLM text; we simulate what an EVALUATION of such a copilot records.

Part A - extraction audit: 4,000 claims x 8 key fields (diagnosis code, admission date, discharge date, total bill,
room rent, ICU days, pre-existing flag, procedure code), each with the true value, the OCR+LLM extracted value,
and document quality (clean print / scan / handwritten). Handwriting and low-quality scans cause more errors.
Part B - adjudication productivity study: 6,000 claims adjudicated by 60 adjudicators; a RANDOMISED 50% got the
copilot summary (AI-assisted), 50% the manual process. Outcomes: handling minutes, the decision (approve/partial/
reject), the gold decision (panel of 3 senior adjudicators on a 600-claim audit subsample), and whether the claim
was later disputed. Complex claims (many pages, ICU, high value) take longer; the copilot saves more time on
long files but can anchor adjudicators on a wrong summary (automation bias).
Part C - guideline check: for 1,500 claims, whether the copilot flagged a treatment as deviating from NHA/disease
guidelines vs an expert's judgement.

Calibration anchors (reference file, Case Study 25): adjudicators read 20+ pages per claim, "several hours";
"2x productivity increase"; processing time cut "by over 50%"; adjudication "to just a few minutes"; humans
remain the decision-makers; no accuracy metrics disclosed. Rates are our assumptions (decision.md D-25-02).
Hidden truth columns start with "_".

Outputs: data/cs25/extraction_audit.csv.gz, data/cs25/adjudication.csv.gz, data/cs25/guideline_check.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.special import expit

SEED = 42
FIELDS = ["diagnosis_code", "admission_date", "discharge_date", "total_bill", "room_rent", "icu_days", "pre_existing_flag", "procedure_code"]
BASE_ERR = {"diagnosis_code": 0.07, "admission_date": 0.03, "discharge_date": 0.03, "total_bill": 0.04, "room_rent": 0.06, "icu_days": 0.05, "pre_existing_flag": 0.12, "procedure_code": 0.09}
QUAL_MULT = {"clean_print": 0.5, "scan": 1.4, "handwritten": 3.2}


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    # ---- Part A: extraction audit ----
    n = 4000; q = rng.choice(list(QUAL_MULT), n, p=[0.45, 0.38, 0.17]); pages = np.clip(rng.gamma(4, 5, n), 3, 90).round()
    rows = []
    for f in FIELDS:
        p_err = np.clip(BASE_ERR[f] * pd.Series(q).map(QUAL_MULT).values * (1 + 0.012 * (pages - 20)), 0.002, 0.7)
        err = rng.random(n) < p_err; conf = np.where(err, np.clip(rng.beta(3, 3, n), 0.2, 0.95), np.clip(rng.beta(7, 1.5, n), 0.3, 1.0))
        rows.append(pd.DataFrame({"claim_id": [f"CL{i:05d}" for i in range(n)], "field": f, "doc_quality": q, "pages": pages, "extraction_correct": (~err).astype(int), "model_confidence": conf.round(3)}))
    ext = pd.concat(rows, ignore_index=True)
    # ---- Part B: randomised productivity study ----
    m = 6000; adj = rng.integers(0, 60, m); speed = np.exp(rng.normal(0, 0.25, 60)); skill = rng.normal(0, 0.5, 60)
    pg = np.clip(rng.gamma(4, 5, m), 3, 90).round(); icu = (rng.random(m) < 0.14).astype(int); value = np.exp(rng.normal(np.log(110000), 0.8, m))
    complex_ = ((pg > 40) | (icu == 1) | (value > 300000)).astype(int)
    ai = (rng.random(m) < 0.5).astype(int)
    base_min = np.exp(rng.normal(np.log(75), 0.35, m)) * (0.6 + 0.02 * pg) * speed[adj] * np.where(icu == 1, 1.3, 1)
    save = np.where(ai == 1, np.clip(0.35 + 0.004 * pg + rng.normal(0, 0.08, m), 0.1, 0.8), 0.0)
    minutes = np.round(base_min * (1 - save), 1)
    # true correct decision; adjudicators have skill noise; AI summary has 9% wrong cases that can anchor
    truth = rng.choice(["approve", "partial", "reject"], m, p=[0.62, 0.26, 0.12])
    sum_wrong = (rng.random(m) < np.where(complex_ == 1, 0.14, 0.06)); sum_wrong = sum_wrong & (ai == 1)
    p_ok = expit(1.9 + 0.5 * skill[adj] - 0.6 * complex_ - 0.35 * (ai == 0) * (pg > 40) - 1.1 * sum_wrong * (rng.random(m) < 0.55) + 0.1 * (ai == 1))
    correct = rng.random(m) < p_ok
    wrong_choices = np.array([[c for c in ["approve", "partial", "reject"] if c != t][rng.integers(2)] for t in truth])
    decision = np.where(correct, truth, wrong_choices)
    disputed = ((~correct) & (rng.random(m) < 0.30)) | ((correct) & (rng.random(m) < 0.03))
    df = pd.DataFrame({"claim_id": [f"AD{i:05d}" for i in range(m)], "adjudicator_id": [f"ADJ{a:02d}" for a in adj], "pages": pg, "icu": icu, "claim_value_inr": np.round(value, -2),
                       "complex_claim": complex_, "ai_assisted": ai, "handling_minutes": minutes, "decision": decision, "disputed_later": disputed.astype(int), "_true_decision": truth, "_summary_wrong": sum_wrong.astype(int)})
    audit = rng.random(m) < 0.10
    gold = np.where(audit, truth, ""); df["gold_decision"] = gold
    # ---- Part C: guideline-deviation flags ----
    g = 1500; dev = (rng.random(g) < 0.18).astype(int); pdv = np.where(dev == 1, 0.78, 0.07); flag = (rng.random(g) < pdv).astype(int)
    gc = pd.DataFrame({"claim_id": [f"GC{i:05d}" for i in range(g)], "expert_deviation": dev, "copilot_flag": flag, "copilot_confidence": np.round(np.where(flag == 1, rng.beta(5, 2, g), rng.beta(2, 5, g)), 3)})
    # data-quality defects
    df.loc[df.sample(n=40, random_state=seed).index, "handling_minutes"] = 0.0                    # timer not stopped / test records
    df = pd.concat([df, df.sample(n=60, random_state=seed + 1)], ignore_index=True)
    return ext, df, gc


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs25"), exist_ok=True)
    e, d, g = generate(); e.to_csv(os.path.join(here, "cs25", "extraction_audit.csv.gz"), index=False); d.to_csv(os.path.join(here, "cs25", "adjudication.csv.gz"), index=False); g.to_csv(os.path.join(here, "cs25", "guideline_check.csv.gz"), index=False)
    dd = d.drop_duplicates("claim_id"); print("extraction accuracy", e.extraction_correct.mean().round(4)); print(dd.groupby("ai_assisted").handling_minutes.median().to_dict())
    print("decision correct by arm", dd.assign(ok=dd.decision == dd._true_decision).groupby("ai_assisted").ok.mean().round(4).to_dict())
