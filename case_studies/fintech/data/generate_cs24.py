"""
SYNTHETIC DATA GENERATOR - CASE STUDY 24 (ICICI Lombard-style smartphone motor inspection with computer vision)
==============================================================================================================
THIS DATA IS SYNTHETIC. Inspection photos and claims data are confidential. We do NOT simulate images; we
simulate what a validation study records: per-part TRUE damage (from a surveyor re-inspection), the CV model's
predicted damage probabilities, photo quality, and repair-cost estimates.

Cases: customer self-inspections for (a) break-in policy renewals and (b) simple own-damage claims.
Parts: front_bumper, rear_bumper, bonnet, left_door, right_door, windshield, headlamp, tail_lamp, fender, mirror.
Damage classes: none / scratch / dent / crack (crack mainly glass and lamps).
Model accuracy depends on damage type (cracks on glass are easy, shallow dents are hard), photo quality
(blur, glare, night shots) and part. A claim is "simple" if total repair cost <= Rs 25,000 and no structural
part is dented; complex claims must go to a surveyor.

Calibration anchors (reference file, Case Study 24): "Split uploaded images into frames", "identify car
components", "detect damage types (scratch, dent, crack)"; accuracy "fit for purpose" (no figure);
150-200 cars a day; inspection time "days to mere minutes"; target ">80,000 simple claims every month".
Rates are our assumptions (decision.md D-24-02). Hidden truth columns start with "_".

Outputs: data/cs24/parts.csv.gz (case x part), data/cs24/cases.csv.gz
"""
import os
import numpy as np
import pandas as pd
from scipy.special import softmax

SEED = 42
PARTS = ["front_bumper", "rear_bumper", "bonnet", "left_door", "right_door", "windshield", "headlamp", "tail_lamp", "fender", "mirror"]
DMG = ["none", "scratch", "dent", "crack"]
COST = {"scratch": 2500, "dent": 6500, "crack": 9000}
PART_MULT = {"front_bumper": 1.0, "rear_bumper": 0.9, "bonnet": 1.6, "left_door": 1.3, "right_door": 1.3, "windshield": 1.5, "headlamp": 0.8, "tail_lamp": 0.5, "fender": 1.1, "mirror": 0.4}
GLASS = {"windshield", "headlamp", "tail_lamp", "mirror"}


def generate(seed=SEED, n=24_000):
    rng = np.random.default_rng(seed)
    kind = rng.choice(["renewal_breakin", "own_damage_claim"], n, p=[0.45, 0.55])
    quality = np.clip(rng.beta(5, 2, n), 0.05, 1)                                        # photo quality score (1 = sharp, well lit)
    night = (rng.random(n) < 0.12).astype(int); quality = np.where(night == 1, quality * 0.7, quality)
    car_value = np.round(np.exp(rng.normal(np.log(6e5), 0.5, n)), -3)
    rows = []
    for i in range(n):
        n_dmg = rng.poisson(0.3 if kind[i] == "renewal_breakin" else 1.6)
        hit = set(rng.choice(PARTS, min(n_dmg, len(PARTS)), replace=False)) if n_dmg else set()
        for p in PARTS:
            if p in hit:
                d = rng.choice(["scratch", "dent", "crack"], p=[0.15, 0.15, 0.70]) if p in GLASS else rng.choice(["scratch", "dent", "crack"], p=[0.55, 0.42, 0.03])
            else:
                d = "none"
            t = DMG.index(d)
            # model logits: correct class boosted by ease x quality; confusions scratch<->dent, none<->scratch
            ease = {"none": 3.2, "scratch": 1.9, "dent": 1.5, "crack": 2.6 if p in GLASS else 1.4}[d]
            lg = rng.normal(0, 0.9, 4); lg[t] += ease * (0.35 + 0.9 * quality[i])
            if d == "dent": lg[1] += 0.9
            if d == "scratch": lg[0] += 0.8
            if d == "none": lg[1] += 0.3 * (1 - quality[i]) * 3                              # glare looks like scratches
            pr = softmax(lg)
            cost = COST.get(d, 0) * PART_MULT[p] * np.exp(rng.normal(0, 0.25)) if d != "none" else 0.0
            rows.append((i, p, d, pr[0], pr[1], pr[2], pr[3], round(cost, -1)))
    parts = pd.DataFrame(rows, columns=["case_idx", "part", "_true_damage", "p_none", "p_scratch", "p_dent", "p_crack", "_true_cost"])
    parts["pred_damage"] = np.array(DMG)[parts[["p_none", "p_scratch", "p_dent", "p_crack"]].values.argmax(1)]
    # surveyor re-inspection on a validation sample (20% of cases): near-perfect but not perfect
    sv = rng.random(n) < 0.20
    parts["surveyor_checked"] = sv[parts.case_idx].astype(int)
    err = (rng.random(len(parts)) < 0.03) & (parts.surveyor_checked == 1)
    parts["surveyor_damage"] = np.where(parts.surveyor_checked == 1, np.where(err, np.where(parts._true_damage == "scratch", "dent", parts._true_damage), parts._true_damage), "")
    parts["surveyor_cost"] = np.where(parts.surveyor_checked == 1, np.round(parts._true_cost * np.exp(rng.normal(0, 0.08, len(parts))), -1), np.nan)
    # model cost estimate: expected cost under predicted probabilities, with its own error
    exp_cost = (parts.p_scratch * 2500 + parts.p_dent * 6500 + parts.p_crack * 9000) * parts.part.map(PART_MULT)
    parts["model_cost"] = np.round(np.where(parts.pred_damage == "none", 0, exp_cost * np.exp(rng.normal(0.05, 0.22, len(parts)))), -1)
    cases = parts.groupby("case_idx").agg(true_cost=("_true_cost", "sum"), model_cost=("model_cost", "sum"), surveyor_cost=("surveyor_cost", "sum"),
                                          n_true_damaged=("_true_damage", lambda s: (s != "none").sum()), structural_dent=("_true_damage", lambda s: 0)).reset_index()
    sd = parts[(parts._true_damage == "dent") & parts.part.isin(["bonnet", "left_door", "right_door", "fender"])].groupby("case_idx").size()
    cases["structural_dent"] = cases.case_idx.map(sd).fillna(0).gt(0).astype(int)
    cases["_complex"] = ((cases.true_cost > 25000) | (cases.structural_dent == 1)).astype(int)
    cases["case_id"] = [f"INS{i:06d}" for i in cases.case_idx]; cases["case_type"] = kind[cases.case_idx]; cases["photo_quality"] = quality[cases.case_idx].round(3)
    cases["night_shot"] = night[cases.case_idx]; cases["car_value_inr"] = car_value[cases.case_idx]; cases["surveyor_checked"] = sv[cases.case_idx].astype(int)
    cases.loc[cases.surveyor_checked == 0, "surveyor_cost"] = np.nan
    cases = cases.rename(columns={"true_cost": "_true_cost", "n_true_damaged": "_n_true_damaged"})
    parts.insert(0, "case_id", "INS" + parts.case_idx.astype(str).str.zfill(6))
    # data-quality defects
    parts = pd.concat([parts, parts.sample(n=500, random_state=seed)], ignore_index=True)                       # duplicate frames
    cases.loc[cases.sample(n=150, random_state=seed + 1).index, "photo_quality"] = np.nan                     # EXIF metadata missing
    return parts, cases


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(here, "cs24"), exist_ok=True)
    p, c = generate(); p.to_csv(os.path.join(here, "cs24", "parts.csv.gz"), index=False); c.to_csv(os.path.join(here, "cs24", "cases.csv.gz"), index=False)
    pp = p.drop_duplicates(["case_id", "part"])
    print(len(c), "cases |", len(pp), "parts | part accuracy", (pp.pred_damage == pp._true_damage).mean().round(4), "| complex share", c._complex.mean().round(4))
    print(pd.crosstab(pp._true_damage, pp.pred_damage, normalize="index").round(3))
