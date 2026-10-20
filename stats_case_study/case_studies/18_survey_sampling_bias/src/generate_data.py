"""Generate the synthetic data for Case Study 18: Customer satisfaction survey: who did we actually hear from?

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business scenario. It is not
actual customer data.

Scenario
--------
A retail bank emailed a "how likely are you to recommend us (0-10)?" survey to all 40,000 active
customers. About 5% answered. The reported satisfaction score is high and the head of retail
banking wants to put it in the annual report. Who actually answered, and can the number be trusted?

Files
-----
data/customer_frame.csv: the sampling frame: all 40,000 ACTIVE customers (known for everyone).
  customer_id, branch (40), age_band, segment (Mass / Affluent / Privileged), tenure_years, digital_user (0/1),
  products (1-4), complaints_12m (0/1/2+), city_tier (1-3)
data/survey_responses.csv: the ~2,050 customers who answered the email survey.
  customer_id, score (0-10)
data/followup_sample.csv: a phone follow-up of 400 customers drawn AT RANDOM from the non-respondents;
  about 60% could be reached. customer_id, score (0-10)
data/answer_key_teaching_only.csv: customer_id, true_score for every active customer, and the satisfaction of
  6,000 customers who LEFT during the year (not in the frame). NOT available in real life.

True data-generating process
----------------------------
true score = clip(round(7.1 + 0.025*(age-45) - 0.35*digital_user - 1.1*complaints (0/1/2) + 0.35*(city tier 3)
             + 0.05*tenure + 0.18*(products-1) + branch effect + Normal(0, 1.7)), 0, 10)
Response (MAR + MNAR mix): logit P(respond) = -3.55 + 0.045*(age-45) + 0.6*digital_user - 0.5*(any complaint)
             + 0.22*(true score - 7)   (older, digital and non-complaining customers respond more: all OBSERVED
             in the frame; and happier customers respond more: the score itself, NOT observed)
Customers who left during the year had a mean score about 1.7 points lower and are not in the frame
(survivorship).

Run:  python case_studies/18_survey_sampling_bias/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import case_paths, rng_for_case  # noqa: E402

CASE_NUMBER = 18
N = 40_000
N_LEFT = 6_000
N_BRANCH = 40


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def generate(rng: np.random.Generator):
    branch_idx = rng.integers(0, N_BRANCH, N)
    branch_eff = rng.normal(0, 0.35, N_BRANCH)
    age = np.clip(np.round(rng.normal(44, 13, N)), 21, 80).astype(int)
    tier = rng.choice([1, 2, 3], N, p=[0.40, 0.38, 0.22])
    seg = rng.choice(["Mass", "Affluent", "Privileged"], N, p=[0.72, 0.23, 0.05])
    tenure = np.round(np.minimum(rng.exponential(6.0, N), age - 18), 1)
    digital = (rng.random(N) < sigmoid(1.6 - 0.045 * (age - 40))).astype(int)
    products = np.clip(1 + rng.poisson(0.5 + 0.45 * (seg != "Mass") + 0.03 * tenure), 1, 4)
    comp = rng.choice([0, 1, 2], N, p=[0.80, 0.14, 0.06])
    score = np.clip(np.round(7.1 + 0.025 * (age - 45) - 0.35 * digital - 1.1 * comp + 0.35 * (tier == 3) + 0.05 * tenure
                             + 0.18 * (products - 1) + branch_eff[branch_idx] + rng.normal(0, 1.7, N)), 0, 10).astype(int)
    respond = rng.random(N) < sigmoid(-3.55 + 0.045 * (age - 45) + 0.6 * digital - 0.5 * (comp > 0) + 0.22 * (score - 7))
    age_band = pd.cut(age, [0, 29, 39, 49, 59, 100], labels=["21–29", "30–39", "40–49", "50–59", "60+"]).astype(str)
    frame = pd.DataFrame({"customer_id": [f"CU18{100000 + i}" for i in range(N)], "branch": [f"B{b + 1:02d}" for b in branch_idx],
                          "age_band": age_band, "segment": seg, "tenure_years": tenure, "digital_user": digital,
                          "products": products, "complaints_12m": np.array(["0", "1", "2+"])[comp], "city_tier": tier})
    resp = pd.DataFrame({"customer_id": frame.loc[respond, "customer_id"], "score": score[respond]})
    non = np.where(~respond)[0]
    pick = rng.choice(non, 400, replace=False)
    reached = pick[rng.random(400) < 0.60]
    follow = pd.DataFrame({"customer_id": frame.loc[reached, "customer_id"], "score": score[reached]})
    left_score = np.clip(np.round(rng.normal(5.2, 2.3, N_LEFT)), 0, 10).astype(int)
    key = pd.concat([pd.DataFrame({"customer_id": frame["customer_id"], "true_score": score, "status": "active"}),
                     pd.DataFrame({"customer_id": [f"CU18L{i:05d}" for i in range(N_LEFT)], "true_score": left_score, "status": "left"})],
                    ignore_index=True)
    return frame, resp, follow, key


def main() -> None:
    paths = case_paths(CASE_DIR)
    frame, resp, follow, key = generate(rng_for_case(CASE_NUMBER))
    frame.to_csv(paths["data"] / "customer_frame.csv", index=False)
    resp.to_csv(paths["data"] / "survey_responses.csv", index=False)
    follow.to_csv(paths["data"] / "followup_sample.csv", index=False)
    key.to_csv(paths["data"] / "answer_key_teaching_only.csv", index=False)
    act = key[key.status == "active"]
    print("respondents", len(resp), f"({len(resp) / len(frame):.1%})", "followup", len(follow))
    print("true mean (active)", act.true_score.mean().round(3), "respondent mean", resp.score.mean().round(3), "followup mean", follow.score.mean().round(3))
    print("true mean incl. left", key.true_score.mean().round(3))


if __name__ == "__main__":
    main()
