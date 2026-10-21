"""Generate the synthetic data for Case Study 25: Monthly digital-payments volume.

THIS DATASET IS SYNTHETIC. It was generated to reproduce a realistic business scenario. It is not
actual company data.

Scenario
--------
A payments platform's finance team needs a baseline forecast of monthly transaction volume for next year's
capacity and budget plan. Ten years of monthly history are available (Jan 2016 to Dec 2024, 108 months).

Files
-----
data/monthly_volume.csv: month (YYYY-MM-01), transactions_m (millions of transactions), days_in_month.
data/future_actuals_teaching_only.csv: the next 12 months (2025), kept back for the grading section.
data/answer_key_teaching_only.csv: the true components (trend, seasonal, shock) behind every month.

True data-generating process (on the log scale)
-----------------------------------------------
log(volume) = 3.0 + 0.040 t - 0.00012 t^2            (growth slowing from about 40% to about 14% a year)
              + seasonal effect (festive peak Oct-Dec, short-month dip in Feb, fiscal year-end bump in Mar)
              + 0.8 log(days in month / 30.4)         (calendar effect)
              + COVID shock Apr-Jul 2020 (-0.45, -0.35, -0.20, -0.10)
              + one-off outage in Mar 2023 (-0.25)
              + AR(1) noise, rho = 0.5, sigma = 0.025
Run:  python case_studies/25_digital_payments_time_series/src/generate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from utils import case_paths, rng_for_case  # noqa: E402

CASE_NUMBER = 25
SEASONAL = {1: 0.00, 2: -0.07, 3: 0.04, 4: -0.02, 5: 0.01, 6: -0.03, 7: -0.02, 8: 0.00, 9: 0.02, 10: 0.10, 11: 0.07, 12: 0.05}
SHOCKS = {"2020-04": -0.45, "2020-05": -0.35, "2020-06": -0.20, "2020-07": -0.10, "2023-03": -0.25}


def generate(rng: np.random.Generator) -> pd.DataFrame:
    months = pd.date_range("2016-01-01", "2025-12-01", freq="MS")
    t = np.arange(len(months))
    trend = 3.0 + 0.040 * t - 0.00012 * t ** 2
    mean_seas = np.mean(list(SEASONAL.values()))
    seas = np.array([SEASONAL[m.month] - mean_seas for m in months])
    days = months.days_in_month.to_numpy()
    cal = 0.8 * np.log(days / 30.4)
    shock = np.array([SHOCKS.get(m.strftime("%Y-%m"), 0.0) for m in months])
    e = rng.normal(0, 0.025, len(months))
    noise = np.zeros(len(months))
    for i in range(len(months)):
        noise[i] = (0.5 * noise[i - 1] if i else 0) + e[i]
    logy = trend + seas + cal + shock + noise
    return pd.DataFrame({"month": months, "transactions_m": np.round(np.exp(logy), 2), "days_in_month": days,
                         "trend": trend, "seasonal": seas, "calendar": cal, "shock": shock, "noise": noise})


def main() -> None:
    paths = case_paths(CASE_DIR)
    df = generate(rng_for_case(CASE_NUMBER))
    hist, fut = df.iloc[:108], df.iloc[108:]
    hist[["month", "transactions_m", "days_in_month"]].to_csv(paths["data"] / "monthly_volume.csv", index=False)
    fut[["month", "transactions_m", "days_in_month"]].to_csv(paths["data"] / "future_actuals_teaching_only.csv", index=False)
    df.to_csv(paths["data"] / "answer_key_teaching_only.csv", index=False)
    print("history", len(hist), "future", len(fut), "first/last volume", hist.transactions_m.iloc[0], hist.transactions_m.iloc[-1],
          "2025 total", fut.transactions_m.sum().round(1), "2024 total", hist.transactions_m.iloc[-12:].sum().round(1))


if __name__ == "__main__":
    main()
