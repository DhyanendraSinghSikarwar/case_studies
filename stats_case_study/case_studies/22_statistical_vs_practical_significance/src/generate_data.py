"""Generate the synthetic data for Case Study 22: Significant but irrelevant; non-significant but promising.

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business scenario. It is not
actual customer data.

Scenario
--------
Two experiments land on the same desk in the same week.

A. A huge A/B test (about 3 million visitors over four weeks) of a redesigned online checkout page for a
   low-margin product. The result is "highly significant" (p < 0.001). The redesign costs Rs 60 lakh to build and
   Rs 12 lakh a year to run.
B. A small pilot (about 1,200 customers) of a card-fee waiver offer for a high-margin premium card. The result is
   "not significant" (p about 0.1-0.3). The analyst's note says "no effect, drop it".

File
----
data/experiment_a_checkout.csv: one row per day x arm for 28 days.
  date, arm (control / redesign), visitors, conversions
data/experiment_b_fee_waiver.csv: one row per customer.
  customer_id, arm (control / offer), converted (0/1)
data/answer_key_teaching_only.csv: the true lifts used to generate the data.

True data-generating process
----------------------------
A: control conversion 5.00%; the redesign adds +0.10 percentage points (+2% relative). 1,500,000 visitors
   per arm over 28 days (with weekday seasonality).
B: control conversion 8.0%; the offer adds +2.0 percentage points (+25% relative). 600 customers per arm.

Random stream: the sampling noise in experiment B is large (SE about 1.6 points), so a single stream can land
anywhere from "clearly significant" to "negative". To keep the teaching case about interpretation rather than luck, the
generator uses the FIRST random stream (STREAM = 0, 1, 2, ...) whose realised lifts are within 0.3 percentage points (B)
and 0.005 points (A) of the TRUE lifts. This rule looks only at how close the draw is to the truth, never at p-values.

Run:  python case_studies/22_statistical_vs_practical_significance/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import case_paths, SEED  # noqa: E402

CASE_NUMBER = 22
A_BASE, A_LIFT, A_PER_ARM, DAYS = 0.0500, 0.0010, 1_500_000, 28
B_BASE, B_LIFT, B_PER_ARM = 0.080, 0.020, 600
DOW = np.array([0.9, 1.0, 1.0, 1.05, 1.1, 1.0, 0.95]) / np.mean([0.9, 1.0, 1.0, 1.05, 1.1, 1.0, 0.95])


def draw(stream: int):
    rng = np.random.default_rng([SEED, CASE_NUMBER, stream])
    rows = []
    dates = pd.date_range("2026-01-05", periods=DAYS)
    vis_share = np.array([DOW[d.dayofweek] for d in dates]); vis_share = vis_share / vis_share.sum()
    for arm, p in (("control", A_BASE), ("redesign", A_BASE + A_LIFT)):
        v = np.round(A_PER_ARM * vis_share * (1 + rng.normal(0, 0.01, DAYS))).astype(int)
        # a 1% day-level wobble in the baseline conversion rate (shared by both arms through the same date seed below)
        c = rng.binomial(v, p)
        for d, vv, cc in zip(dates, v, c):
            rows.append({"date": d.date().isoformat(), "arm": arm, "visitors": int(vv), "conversions": int(cc)})
    a = pd.DataFrame(rows)
    b_rows = []
    for arm, p in (("control", B_BASE), ("offer", B_BASE + B_LIFT)):
        b_rows.append(pd.DataFrame({"arm": arm, "converted": (rng.random(B_PER_ARM) < p).astype(int)}))
    b = pd.concat(b_rows, ignore_index=True).sample(frac=1, random_state=int(rng.integers(1e9))).reset_index(drop=True)
    b.insert(0, "customer_id", [f"FW22{10000 + i}" for i in range(len(b))])
    return a, b


def lifts(a: pd.DataFrame, b: pd.DataFrame):
    g = a.groupby("arm")[["visitors", "conversions"]].sum()
    la = g.loc["redesign", "conversions"] / g.loc["redesign", "visitors"] - g.loc["control", "conversions"] / g.loc["control", "visitors"]
    gb = b.groupby("arm")["converted"].mean()
    return la, gb["offer"] - gb["control"]


def main() -> None:
    paths = case_paths(CASE_DIR)
    for stream in range(1000):
        a, b = draw(stream)
        la, lb = lifts(a, b)
        if abs(la - A_LIFT) <= 0.00005 and abs(lb - B_LIFT) <= 0.003:
            break
    else:
        raise RuntimeError("no suitable stream found")
    a.to_csv(paths["data"] / "experiment_a_checkout.csv", index=False)
    b.to_csv(paths["data"] / "experiment_b_fee_waiver.csv", index=False)
    pd.DataFrame({"experiment": ["A (checkout)", "B (fee waiver)"], "true_lift_pp": [100 * A_LIFT, 100 * B_LIFT],
                  "baseline_rate": [A_BASE, B_BASE]}).to_csv(paths["data"] / "answer_key_teaching_only.csv", index=False)
    print(f"STREAM = {stream};  realised lift A {100 * la:+.3f} pp (true {100 * A_LIFT:.3f}),  B {100 * lb:+.2f} pp (true {100 * B_LIFT:.2f})")


if __name__ == "__main__":
    main()
