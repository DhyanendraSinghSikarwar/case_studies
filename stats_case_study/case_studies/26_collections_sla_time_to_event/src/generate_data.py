"""Generate the synthetic data for Case Study 26: Collections and SLA: time until an event happens.

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business scenario. It is not
actual customer data.

Scenario
--------
A bank's collections team contacts customers whose card payment is overdue. Management has an SLA: "70% of overdue accounts
should be resolved (paid up) within 30 days of entering collections". Two data sets are available:

data/collections_accounts.csv: 6,000 accounts that entered collections between Jan 2023 and Jun 2024, followed until the data
  cut-off on 30 Sep 2024 or until paid up. Columns: account_id, entry_date, strategy (sms_first / call_first),
  bucket (early = 1-29 days overdue at entry, late = 30-59), balance_band (low / mid / high),
  duration_days (days observed), resolved (1 = paid up, 0 = still open or transferred, i.e. CENSORED).
data/call_arrivals.csv: inbound customer calls to the collections desk, counted per 15-minute interval for 20 working days.
data/answer_key_teaching_only.csv: true parameters and true 30-day resolution probabilities by group (not available in real life).

True data-generating process
----------------------------
Time to resolution T ~ Weibull proportional hazards: S(t | x) = exp(-(t / 55)^0.85 * exp(x b)),
  call_first: +0.35 (hazard x1.42);  late bucket: -0.45 (x0.64);  balance band mid / high: -0.15 / -0.40.
Follow-up is cut off at 120 days, by the data cut-off date, or by transfer to an external agency (random, mean 160 days).
Call arrivals: Poisson with an hourly rate that peaks at 11:00 and 15:00 (about 14 calls per 15 minutes) and is low at open and lunch.

Run:  python case_studies/26_collections_sla_time_to_event/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import case_paths, rng_for_case  # noqa: E402

CASE_NUMBER = 26
N = 6000
SCALE, SHAPE = 55.0, 0.85
BETA = {"strategy": {"sms_first": 0.0, "call_first": 0.35}, "bucket": {"early": 0.0, "late": -0.45}, "balance_band": {"low": 0.0, "mid": -0.15, "high": -0.40}}
CUTOFF = pd.Timestamp("2024-09-30")
HOURLY = {9: 6, 10: 11, 11: 14, 12: 9, 13: 5, 14: 10, 15: 14, 16: 11, 17: 7}     # mean calls per 15 minutes


def true_s(t, strategy, bucket, band):
    xb = BETA["strategy"][strategy] + BETA["bucket"][bucket] + BETA["balance_band"][band]
    return np.exp(-((t / SCALE) ** SHAPE) * np.exp(xb))


def generate(rng: np.random.Generator):
    entry = pd.Timestamp("2023-01-01") + pd.to_timedelta(rng.integers(0, 546, N), unit="D")
    strategy = rng.choice(["sms_first", "call_first"], N, p=[0.5, 0.5])
    bucket = rng.choice(["early", "late"], N, p=[0.6, 0.4])
    band = rng.choice(["low", "mid", "high"], N, p=[0.40, 0.38, 0.22])
    xb = np.array([BETA["strategy"][s] + BETA["bucket"][b] + BETA["balance_band"][g] for s, b, g in zip(strategy, bucket, band)])
    u = rng.random(N)
    t_event = SCALE * (-np.log(u) / np.exp(xb)) ** (1 / SHAPE)
    c_admin = np.minimum(120.0, (CUTOFF - entry).days.to_numpy().astype(float))
    c_transfer = rng.exponential(160.0, N)
    c = np.minimum(c_admin, c_transfer)
    obs = np.minimum(t_event, c)
    resolved = (t_event <= c).astype(int)
    duration = np.maximum(1, np.ceil(obs)).astype(int)
    acc = pd.DataFrame({"account_id": [f"AC26{100000 + i}" for i in range(N)], "entry_date": entry.strftime("%Y-%m-%d"), "strategy": strategy,
                        "bucket": bucket, "balance_band": band, "duration_days": duration, "resolved": resolved})
    # call arrivals
    rows = []
    for d in pd.bdate_range("2024-09-02", periods=20):
        for h, lam in HOURLY.items():
            for q in range(4):
                rows.append({"date": d.strftime("%Y-%m-%d"), "interval_start": f"{h:02d}:{15 * q:02d}", "calls": int(rng.poisson(lam))})
    calls = pd.DataFrame(rows)
    key = pd.DataFrame([{"strategy": s, "bucket": b, "balance_band": g, "true_resolved_by_30_days": 1 - true_s(30, s, b, g), "true_median_days": SCALE * (np.log(2) / np.exp(BETA["strategy"][s] + BETA["bucket"][b] + BETA["balance_band"][g])) ** (1 / SHAPE)}
                        for s in BETA["strategy"] for b in BETA["bucket"] for g in BETA["balance_band"]])
    return acc, calls, key


def main() -> None:
    paths = case_paths(CASE_DIR)
    acc, calls, key = generate(rng_for_case(CASE_NUMBER))
    acc.to_csv(paths["data"] / "collections_accounts.csv", index=False)
    calls.to_csv(paths["data"] / "call_arrivals.csv", index=False)
    key.to_csv(paths["data"] / "answer_key_teaching_only.csv", index=False)
    print("accounts", len(acc), "resolved share", acc.resolved.mean().round(3), "calls rows", len(calls), "mean calls/15min", calls.calls.mean().round(2))


if __name__ == "__main__":
    main()
