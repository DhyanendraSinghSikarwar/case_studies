"""Generate the synthetic data for Case Study 20: Did the new approval policy hurt approval rates?

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business scenario. It is not
actual customer data.

Scenario
--------
In April the lender replaced its personal-loan approval policy. Quarterly reporting shows the overall approval rate
FELL after the change, and the Chief Risk Officer asks whether the new policy is too strict. The policy team
insists it is more generous at every risk level. At the same time, a new agent-network acquisition campaign
launched in April and brought many riskier applicants.

File
----
data/loan_applications.csv: 27,000 applications.
  app_id, period (Before / After the policy change), channel (Branch / Online / Agent),
  risk_band (A lowest risk ... D highest risk, from the application scorecard), approved (0/1)

True data-generating process
----------------------------
Channel mix: Before: Branch 50%, Online 40%, Agent 10%.  After: Branch 30%, Online 25%, Agent 45%.
Risk band given channel (the same in both periods):
    Branch / Online: A 48%, B 32%, C 15%, D 5%;   Agent: A 10%, B 25%, C 35%, D 30%.
Approval probability by risk band:
    Before the policy: A 90%, B 70%, C 40%, D 15%.
    After the policy:  A 95%, B 76%, C 46%, D 21%   (about 6 percentage points MORE generous in every band).
Approval depends only on the risk band and the period, not on the channel.
Before: 12,000 applications; After: 15,000.

Run:  python case_studies/20_simpsons_paradox_approvals/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import case_paths, rng_for_case  # noqa: E402

CASE_NUMBER = 20
N_BEFORE, N_AFTER = 12_000, 15_000
BANDS = ["A", "B", "C", "D"]
CHANNELS = ["Branch", "Online", "Agent"]
CHANNEL_MIX = {"Before": [0.50, 0.40, 0.10], "After": [0.30, 0.25, 0.45]}
BAND_MIX = {"Branch": [0.48, 0.32, 0.15, 0.05], "Online": [0.48, 0.32, 0.15, 0.05], "Agent": [0.10, 0.25, 0.35, 0.30]}
APPROVAL = {"Before": [0.90, 0.70, 0.40, 0.15], "After": [0.95, 0.76, 0.46, 0.21]}


def generate(rng: np.random.Generator) -> pd.DataFrame:
    rows = []
    for period, n in (("Before", N_BEFORE), ("After", N_AFTER)):
        channel = rng.choice(CHANNELS, n, p=CHANNEL_MIX[period])
        band = np.empty(n, dtype=object)
        for ch in CHANNELS:
            m = channel == ch
            band[m] = rng.choice(BANDS, m.sum(), p=BAND_MIX[ch])
        p_app = pd.Series(band).map(dict(zip(BANDS, APPROVAL[period]))).to_numpy()
        approved = (rng.random(n) < p_app).astype(int)
        rows.append(pd.DataFrame({"period": period, "channel": channel, "risk_band": band, "approved": approved}))
    df = pd.concat(rows, ignore_index=True)
    df.insert(0, "app_id", [f"LA20{100000 + i}" for i in range(len(df))])
    return df


def main() -> None:
    paths = case_paths(CASE_DIR)
    df = generate(rng_for_case(CASE_NUMBER))
    df.to_csv(paths["data"] / "loan_applications.csv", index=False)
    print(df.groupby("period")["approved"].agg(["size", "mean"]).round(4))
    print(df.groupby(["risk_band", "period"])["approved"].mean().unstack().round(3))


if __name__ == "__main__":
    main()
