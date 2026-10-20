"""Generate the synthetic data for Case Study 04: Designing and reading a checkout A/B test.

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business
scenario. It is not actual customer data.

Scenario
--------
A payments app wants to replace its 3-step bill-payment checkout with a "one-tap"
checkout. The test randomises USERS 50/50 to control (old flow) or treatment
(one-tap) for 14 days. The primary metric is checkout completion: did the user
complete the payment they started? Guardrail: payment error rate.

Files
-----
1. data/historical_baseline.csv: 28 pre-test days (one row per day):
   date, users_starting_checkout, users_completing. Used to plan the test.

2. data/experiment_users.csv: one row per user who started a checkout during
   the 14-day test (first checkout only):
   user_id, day (1-14), variant (control / treatment), platform (iOS / Android),
   app_version ("v5+" / "pre-v5"), completed (0/1), payment_error (0/1),
   payment_amount (Rs, blank if not completed).

True data-generating process
----------------------------
- Traffic: ~4,800 users start a checkout per day (weekly seasonality: weekends
  ~15% higher), split 50/50 at random.
- Baseline completion: iOS 74%, Android v5+ 70%, Android pre-v5 62%.
- True treatment effect on completion for v5+ users and iOS: +1.2 pp long-run plus a
  novelty boost of +1.8 pp that decays over days (about 3.0 pp on day 1, about 1.3 pp by
  day 7); about +1.45 pp averaged over the 14 days.
- BUG: on Android pre-v5 (about 10% of users) the one-tap screen crashes for 35% of
  treatment users BEFORE the exposure event is logged. Those users never
  appear in the treatment data (they abandon, i.e. would have been
  non-completions). Pre-v5 treatment users who do not crash get no benefit
  and see more payment errors (6% vs 2%). This produces a sample-ratio
  mismatch and biases the naive treatment completion rate upward.
- Payment errors: 2% baseline everywhere else, unaffected by treatment.
- Payment amount: lognormal, median ~Rs 850.

Run:  python case_studies/04_checkout_ab_test/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import SEED, case_paths  # noqa: E402

CASE_NUMBER = 4
DAILY_USERS = 4_800
TEST_DAYS = 14
# Random-stream choice (documented): with the default stream (0), the random 50/50
# assignment happened to be imbalanced even among unaffected (v5+) users
# (SRM p = 0.002, a 1-in-500 fluke). That would muddy the lesson that the SRM is
# caused by the pre-v5 bug. Rule applied: take the first later stream whose
# v5+ assignment passes an SRM check at p > 0.2 -> stream 1. The rule looks only at
# assignment balance, never at the outcome.
STREAM = 1
BASE_RATE = {("iOS", "v5+"): 0.74, ("Android", "v5+"): 0.70, ("Android", "pre-v5"): 0.62}


def daily_traffic(rng, n_days, start_weekday):
    weekday = (np.arange(n_days) + start_weekday) % 7
    mult = np.where(weekday >= 5, 1.15, 0.95)
    return rng.poisson(DAILY_USERS * mult)


def draw_users(rng, n):
    platform = rng.choice(["iOS", "Android"], n, p=[0.35, 0.65])
    pre_v5 = (platform == "Android") & (rng.random(n) < 0.155)   # ~10% of all users
    version = np.where(pre_v5, "pre-v5", "v5+")
    base = np.array([BASE_RATE[(p, v)] for p, v in zip(platform, version)])
    return platform, version, base


def historical(rng):
    days = 28
    users = daily_traffic(rng, days, start_weekday=0)
    rows = []
    for d, n in enumerate(users):
        _, _, base = draw_users(rng, n)
        rows.append((pd.Timestamp("2026-07-06") + pd.Timedelta(days=d), n, int((rng.random(n) < base).sum())))
    return pd.DataFrame(rows, columns=["date", "users_starting_checkout", "users_completing"])


def experiment(rng):
    users = daily_traffic(rng, TEST_DAYS, start_weekday=0)
    frames = []
    for d, n in enumerate(users, start=1):
        platform, version, base = draw_users(rng, n)
        variant = np.where(rng.random(n) < 0.5, "treatment", "control")
        lift = (0.012 + 0.018 * np.exp(-(d - 1) / 3.0))
        is_t = variant == "treatment"
        broken = (version == "pre-v5")
        p = base + np.where(is_t & ~broken, lift, 0.0)
        completed = (rng.random(n) < p).astype(int)
        err_p = np.where(is_t & broken, 0.06, 0.02)
        payment_error = (rng.random(n) < err_p).astype(int)
        completed = np.where(payment_error == 1, 0, completed)
        crashed = is_t & broken & (rng.random(n) < 0.35)          # never logged
        amount = np.where(completed == 1, np.round(np.exp(rng.normal(np.log(850), 0.8, n))), np.nan)
        frames.append(pd.DataFrame({"day": d, "variant": variant, "platform": platform, "app_version": version,
                                    "completed": completed, "payment_error": payment_error,
                                    "payment_amount": amount})[~crashed])
    df = pd.concat(frames, ignore_index=True)
    df.insert(0, "user_id", [f"U{7000000 + i}" for i in range(len(df))])
    return df


def main() -> None:
    paths = case_paths(CASE_DIR)
    rng = np.random.default_rng(SEED + CASE_NUMBER + 1000 * STREAM)
    hist = historical(rng)
    exp = experiment(rng)
    hist.to_csv(paths["data"] / "historical_baseline.csv", index=False)
    exp.to_csv(paths["data"] / "experiment_users.csv", index=False)
    print(f"Historical completion: {hist.users_completing.sum() / hist.users_starting_checkout.sum():.3%}, "
          f"avg daily users {hist.users_starting_checkout.mean():,.0f}")
    print(exp.groupby("variant")[["completed", "payment_error"]].agg(["size", "mean"]))
    print(exp.groupby(["app_version", "variant"])["completed"].agg(["size", "mean"]))


if __name__ == "__main__":
    main()
