"""Generate the synthetic data for Case Study 15: Branch loan processing times and a new workflow.

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business
scenario. It is not actual customer data.

Scenario
--------
Operations wants to know (A) whether five branches in one region differ in how long they
take to disburse a personal loan, and (B) whether a new digital document workflow, piloted
with 20 loan officers, made processing faster.

Files
-----
data/branch_processing_times.csv: 190 loans from last quarter.
  loan_id, branch, processing_days (application to disbursement)
data/workflow_pilot.csv: 20 loan officers, average processing days in the month before and
  the month after switching to the new workflow.
  officer_id, days_before, days_after

True data-generating process
----------------------------
(A) processing_days ~ log-normal with branch medians Andheri 6.0, Borivali 6.5, Thane 8.0,
    Vashi 6.0, Panvel 9.5 (sigma 0.45); about 6% of loans get "stuck" (missing documents)
    and take an extra 20-60 days. Small groups, right skew, outliers: non-parametric territory.
(B) after = before x exp(-0.15 + Normal(0, 0.10)) (about 14% faster), except one officer
    whose cases were caught in a system migration: after = before + 16 days.

Run:  python case_studies/15_branch_processing_nonparametric/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import case_paths, rng_for_case  # noqa: E402

CASE_NUMBER = 15
BRANCHES = {"Andheri": (42, 6.0), "Borivali": (38, 6.5), "Thane": (45, 8.0), "Vashi": (30, 6.0), "Panvel": (35, 9.5)}


def generate(rng: np.random.Generator) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    for b, (n, med) in BRANCHES.items():
        days = med * np.exp(rng.normal(0, 0.45, n))
        stuck = rng.random(n) < 0.06
        days = days + stuck * rng.uniform(20, 60, n)
        rows.append(pd.DataFrame({"branch": b, "processing_days": np.round(days, 1)}))
    a = pd.concat(rows, ignore_index=True)
    a = a.sample(frac=1, random_state=int(rng.integers(1e9))).reset_index(drop=True)
    a.insert(0, "loan_id", [f"PL15{10000 + i}" for i in range(len(a))])

    n_off = 20
    before = np.round(8.0 * np.exp(rng.normal(0, 0.25, n_off)), 1)
    after = before * np.exp(-0.15 + rng.normal(0, 0.10, n_off))
    after[7] = before[7] + 16.0                      # officer caught in the system migration
    b_df = pd.DataFrame({"officer_id": [f"LO{101 + i}" for i in range(n_off)], "days_before": before,
                         "days_after": np.round(after, 1)})
    return a, b_df


def main() -> None:
    paths = case_paths(CASE_DIR)
    a, b = generate(rng_for_case(CASE_NUMBER))
    a.to_csv(paths["data"] / "branch_processing_times.csv", index=False)
    b.to_csv(paths["data"] / "workflow_pilot.csv", index=False)
    print(a.groupby("branch")["processing_days"].describe().round(1))
    print(b.assign(diff=b.days_after - b.days_before).describe().round(2))


if __name__ == "__main__":
    main()
