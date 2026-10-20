"""Generate the synthetic data for Case Study 19: Testing a campaign across 40 customer segments.

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business scenario. It is not
actual customer data.

Scenario
--------
Marketing ran a cross-sell SMS campaign as a randomised test (treatment vs holdout control) across 40
customer segments (8 customer types x 5 regions). The campaign ran in two waves of two weeks each.
The head of marketing wants a list of "winning segments" to target next quarter and has circled every
segment with p < 0.05.

File
----
data/campaign_results.csv: one row per segment x wave x arm.
  segment_id (S01-S40), customer_type (8), region (5), wave (1 or 2), arm (treatment / control),
  customers, conversions
data/answer_key_teaching_only.csv: segment_id, baseline_rate, true_uplift (percentage points).
  NOT available in real life. Used only to grade the methods.

True data-generating process
----------------------------
Each segment has a baseline conversion rate (2% to 9%). Treatment effect (absolute uplift, in percentage
points): 8 segments truly respond (+1.0 to +2.2 pp), 3 segments are slightly harmed (-0.8 to -1.2 pp),
29 segments have NO effect. Arms are randomised 50:50. Segment sizes differ (700 to 2,400 customers
per arm per wave).

Run:  python case_studies/19_multiple_testing_segments/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import SEED, case_paths  # noqa: E402
from scipy.stats import norm  # noqa: E402

CASE_NUMBER = 19
TYPES = ["Salaried (mass)", "Salaried (affluent)", "Self-employed", "Gig worker", "Student", "Retired", "Homemaker", "Business owner"]
REGIONS = ["North", "South", "East", "West", "Central"]


def generate(rng: np.random.Generator):
    segs = [(f"S{i + 1:02d}", t, r) for i, (t, r) in enumerate([(t, r) for t in TYPES for r in REGIONS])]
    n_seg = len(segs)
    base = np.round(rng.uniform(0.02, 0.09, n_seg), 4)
    effect = np.zeros(n_seg)
    pos = rng.choice(n_seg, 8, replace=False)
    effect[pos] = rng.uniform(0.010, 0.022, 8)
    neg = rng.choice(np.setdiff1d(np.arange(n_seg), pos), 3, replace=False)
    effect[neg] = -rng.uniform(0.008, 0.012, 3)
    size = rng.integers(700, 2_400, n_seg)
    rows = []
    for i, (sid, t, r) in enumerate(segs):
        for wave in (1, 2):
            n_arm = int(size[i] * rng.uniform(0.9, 1.1))
            for arm, p in (("control", base[i]), ("treatment", base[i] + effect[i])):
                rows.append({"segment_id": sid, "customer_type": t, "region": r, "wave": wave, "arm": arm, "customers": n_arm,
                             "conversions": int(rng.binomial(n_arm, max(p, 0)))})
    key = pd.DataFrame({"segment_id": [s[0] for s in segs], "baseline_rate": base, "true_uplift_pp": np.round(100 * effect, 3)})
    return pd.DataFrame(rows), key


def segment_p_values(df: pd.DataFrame) -> pd.Series:
    g = df.groupby(["segment_id", "arm"])[["customers", "conversions"]].sum().unstack("arm")
    x1, n1 = g[("conversions", "treatment")].to_numpy(float), g[("customers", "treatment")].to_numpy(float)
    x0, n0 = g[("conversions", "control")].to_numpy(float), g[("customers", "control")].to_numpy(float)
    pbar = (x1 + x0) / (n1 + n0)
    z = (x1 / n1 - x0 / n0) / np.sqrt(pbar * (1 - pbar) * (1 / n1 + 1 / n0))
    return pd.Series(2 * norm.sf(np.abs(z)), index=g.index)


def main() -> None:
    paths = case_paths(CASE_DIR)
    # Random stream: with 29 null segments the number of uncorrected "false alarms" is Binomial(29, 0.05): mean 1.45,
    # but 0 about one time in four. So that the realised data show a TYPICAL multiplicity problem (not a lucky or unlucky
    # draw), the generator uses the first stream (STREAM = 0, 1, 2, ...) in which exactly 2 of the 29 null segments have
    # p < 0.05 and 5 to 7 of the 8 truly responsive segments do. The rule never looks at which corrected method wins.
    for stream in range(2000):
        df, key = generate(np.random.default_rng([SEED, CASE_NUMBER, stream]))
        p = segment_p_values(df)
        null = key.set_index("segment_id")["true_uplift_pp"].eq(0)
        pos = key.set_index("segment_id")["true_uplift_pp"].gt(0)
        if (p[null] < 0.05).sum() == 2 and 5 <= (p[pos] < 0.05).sum() <= 7:
            break
    else:
        raise RuntimeError("no suitable stream found")
    print(f"STREAM = {stream}")
    df.to_csv(paths["data"] / "campaign_results.csv", index=False)
    key.to_csv(paths["data"] / "answer_key_teaching_only.csv", index=False)
    print(df.groupby("arm")[["customers", "conversions"]].sum())
    print("true effects: positive", int((key.true_uplift_pp > 0).sum()), "negative", int((key.true_uplift_pp < 0).sum()), "zero", int((key.true_uplift_pp == 0).sum()))


if __name__ == "__main__":
    main()
