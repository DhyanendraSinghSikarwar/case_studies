"""Generate the synthetic data for Case Study 10: Modelling insurance claim cost.

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business
scenario. It is not actual customer data.

Scenario
--------
A health insurer needs (a) a claim-cost model for pricing and (b) reserves for claims that
have been pre-authorised but not yet settled. The analytics team fitted an ordinary
regression on the raw claim amount. The Appointed Actuary is unhappy: the model gives some
negative costs, its errors are huge for big claims, and a later log model "under-reserves".

File: data/health_claims.csv: 6,000 settled hospitalisation claims.
  claim_id, age, procedure_category (nominal, 7), room_type (ordinal: General ward <
  Semi-private < Private < Suite), hospital_type (Network-metro / Network-non-metro /
  Non-network), preauth_estimated_los (days, from the hospital's pre-authorisation request),
  smoker (0/1), diabetic (0/1), sum_insured (Rs), claim_amount (Rs, settled; TARGET)

True data-generating process
----------------------------
log(mean cost) = log(40,000) + procedure effect + room effect + hospital effect
                 + 0.35 * log(LOS) + 0.010 * (age - 45) + 0.00035 * (age - 45)^2   (curved in age)
                 + 0.08 * smoker + 0.10 * diabetic
procedure (vs Medical management): Day-care -0.40, Maternity +0.15, Surgical +0.50,
           Orthopaedic +0.70, Cardiac +1.10, Oncology +1.30
room (vs General ward): Semi-private +0.12, Private +0.25, Suite +0.45
hospital (vs Network-metro): Network-non-metro -0.15, Non-network +0.10
claim ~ Gamma(shape 2.5, mean = mean cost): variance proportional to mean^2.
Claims are paid up to the sum insured (capped); claims below Rs 1,000 are not filed (floored).
DATA ERRORS: 6 claims were keyed in PAISE instead of rupees (x100). They are impossible
(above the sum insured) and are meant to be found by the diagnostics.

Run:  python case_studies/10_insurance_claim_cost/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import case_paths, rng_for_case  # noqa: E402

CASE_NUMBER = 10
N = 6_000
SHAPE = 2.5
PROCEDURES = {"Medical management": 0.0, "Day-care": -0.40, "Maternity": 0.15, "Surgical": 0.50,
              "Orthopaedic": 0.70, "Cardiac": 1.10, "Oncology": 1.30}
PROC_P = [0.33, 0.10, 0.12, 0.19, 0.10, 0.10, 0.06]
PROC_LOS = {"Medical management": 4, "Day-care": 1, "Maternity": 3, "Surgical": 4, "Orthopaedic": 5,
            "Cardiac": 6, "Oncology": 7}
ROOMS = {"General ward": 0.0, "Semi-private": 0.12, "Private": 0.25, "Suite": 0.45}
HOSPITALS = {"Network-metro": 0.0, "Network-non-metro": -0.15, "Non-network": 0.10}
SUM_INSURED = np.array([300_000, 500_000, 1_000_000, 2_500_000])


def generate(rng: np.random.Generator) -> pd.DataFrame:
    proc = rng.choice(list(PROCEDURES), N, p=PROC_P)
    age = np.where(proc == "Maternity", rng.integers(22, 40, N),
                   np.clip(np.round(rng.normal(47, 15, N)), 18, 85)).astype(int)
    si_idx = rng.choice(4, N, p=[0.25, 0.40, 0.25, 0.10])
    si = SUM_INSURED[si_idx]
    # Higher sum insured -> better room entitlement.
    room_p = np.array([[0.50, 0.30, 0.18, 0.02], [0.30, 0.35, 0.30, 0.05],
                       [0.15, 0.30, 0.45, 0.10], [0.05, 0.20, 0.50, 0.25]])
    room = np.array([rng.choice(list(ROOMS), p=room_p[i]) for i in si_idx])
    hosp = rng.choice(list(HOSPITALS), N, p=[0.45, 0.35, 0.20])
    base_los = pd.Series(proc).map(PROC_LOS).to_numpy()
    los = np.clip(rng.poisson(base_los * np.exp(0.012 * (age - 45))) , 1, 30)
    los = np.where(proc == "Day-care", 1, los)
    smoker = (rng.random(N) < 0.15).astype(int)
    diabetic = (rng.random(N) < np.clip(0.05 + 0.006 * (age - 30), 0.02, 0.45)).astype(int)

    log_mu = (np.log(40_000) + pd.Series(proc).map(PROCEDURES).to_numpy() + pd.Series(room).map(ROOMS).to_numpy()
              + pd.Series(hosp).map(HOSPITALS).to_numpy() + 0.35 * np.log(los)
              + 0.010 * (age - 45) + 0.00035 * (age - 45) ** 2 + 0.08 * smoker + 0.10 * diabetic)
    mu = np.exp(log_mu)
    cost = rng.gamma(SHAPE, mu / SHAPE)
    claim = np.round(np.minimum(np.maximum(cost, 1_000), si), -1)   # minimum claimable Rs 1,000

    # Data-entry errors: amount keyed in paise.
    err_idx = rng.choice(N, 6, replace=False)
    claim[err_idx] = claim[err_idx] * 100

    return pd.DataFrame({
        "claim_id": [f"HC10{100000 + i}" for i in range(N)], "age": age, "procedure_category": proc,
        "room_type": room, "hospital_type": hosp, "preauth_estimated_los": los, "smoker": smoker,
        "diabetic": diabetic, "sum_insured": si, "claim_amount": claim.astype(np.int64),
    })


def main() -> None:
    paths = case_paths(CASE_DIR)
    df = generate(rng_for_case(CASE_NUMBER))
    df.to_csv(paths["data"] / "health_claims.csv", index=False)
    print(df.describe().round(0))
    print("capped share:", (df.claim_amount == df.sum_insured).mean())


if __name__ == "__main__":
    main()
