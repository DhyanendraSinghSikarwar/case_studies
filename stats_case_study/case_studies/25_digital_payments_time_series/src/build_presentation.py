"""Build the stakeholder deck for Case Study 25 from the notebook's saved outputs.

Run the notebook first, then:
    python case_studies/25_digital_payments_time_series/src/build_presentation.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

CASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CASE_DIR.parents[1] / "00_shared_resources"))
from presentation import Deck  # noqa: E402
from utils import case_paths  # noqa: E402


def main() -> None:
    paths = case_paths(CASE_DIR)
    tables, figs = paths["tables"], paths["figures"]
    seas = pd.read_csv(tables / "seasonal_pattern.csv", index_col=0)
    acc = pd.read_csv(tables / "rolling_origin_accuracy.csv", index_col=0)
    cov = pd.read_csv(tables / "interval_coverage.csv", index_col=0)
    fin = pd.read_csv(tables / "final_holdout_grading.csv", index_col=0)
    tot = pd.read_csv(tables / "forecast_totals_2025.csv", index_col=0)

    mult = seas["multiplier vs average month"]
    best = acc.index[0]
    reg = fin.loc["Trend + season regression"]
    rule = fin.loc["Last year + 20% rule"]
    sarima = fin.loc["SARIMA"]

    deck = Deck("Case 25 · Monthly digital-payments volume · synthetic data")
    deck.title_slide("Is 'Last Year Plus 20%' a Good Forecast?",
                     "Describing a time series and building an honest baseline · Payments Finance",
                     "108 months of synthetic payment-volume history. Synthetic data created for training. Not actual company data.")
    deck.bullets(
        "Summary: growth is slowing, seasonality is stable, and a simple model beats the fancy ones",
        [
            "**Volume grew from about 20 to 390 million a month, but growth is slowing:** trend growth fell from 52% to 19% a year.",
            f"**Seasonality is stable:** October runs {mult['Oct'] - 1:.0%} above an average month, February {1 - mult['Feb']:.0%} below (a short month).",
            f"**Best baseline: trend plus seasonal-dummy regression** (rolling MAPE {acc.loc[best, 'MAPE (%)']:.1f}%). SARIMA was much worse "
            f"({acc.loc['SARIMA', 'MAPE (%)']:.1f}%, biased high); seasonal naive {acc.loc['Seasonal naive', 'MAPE (%)']:.0f}%.",
            f"**The 20% rule gave {rule['2025 total forecast']:,.0f} million for 2025**, within {abs(rule['total error (%)']):.1f}% of the {fin['2025 total forecast'].iloc[0] / (1 + fin['total error (%)'].iloc[0] / 100):,.0f} actual, "
            "but it has no way to reflect slowing growth.",
        ],
        takeaway="Recommendation: use a model-based baseline with an interval, and a growth scenario range instead of one percentage.",
        size=16,
    )
    deck.image("The history: a slowing exponential trend, a COVID dip and a one-month outage", figs / "fig01_series.png",
               takeaway="On the log scale growth is close to a straight line that flattens. Shaded: April to July 2020.")
    deck.image("Trend, seasonal pattern and remainder", figs / "fig02_decomposition.png",
               takeaway="The seasonal pattern repeats each year; the remainder is small except for 2020 and March 2023.")
    deck.image("Growth is not 20%: it fell every year after the 2021 rebound", figs / "fig03_rolling_growth.png",
               takeaway="Calendar-year growth: 57%, 50%, 46%, 29% (COVID), 51%, 27%, 27%, 24%.")
    deck.image("Why ordinary statistics fail: autocorrelation after differencing", figs / "fig04_acf.png",
               takeaway="The raw series is non-stationary (ADF p = 1.00). After first and seasonal differencing it is stationary (p = 0.0002). Months next to each other are correlated, so split by time.")
    rows = pd.DataFrame({"Model": list(acc.index), "MAPE (%)": [f"{v:.1f}" for v in acc["MAPE (%)"]], "MASE": [f"{v:.2f}" for v in acc["MASE"]],
                         "Bias (%)": [f"{v:+.1f}" for v in acc["bias (%)"]]})
    deck.table("Rolling-origin test: forecasting 12 months ahead from 9 different starting points", rows,
               takeaway="MASE below 1 beats the seasonal naive forecast made on the history. Seasonal naive ignores growth and loses badly.",
               col_widths=[3.2, 1.2, 1.0, 1.2], font_size=15, highlight_rows=[0])
    deck.image("Forecast for the next 12 months", figs / "fig06_forecast.png",
               takeaway="Forecast totals for the year range from 4,827 million (regression) to 5,331 million (SARIMA). The 20% rule gives 4,880.")
    deck.image("What happened in 2025", figs / "fig07_forecast_vs_actual.png",
               takeaway=f"Actual +18.6%. Regression {reg['total error (%)']:+.1f}% on the total, SARIMA {sarima['total error (%)']:+.1f}%. The SARIMA interval contained every month, but it was wide and biased high.")
    erows = pd.DataFrame({"Forecast": list(fin.index), "2025 total error": [f"{v:+.1f}%" for v in fin["total error (%)"]],
                          "Monthly MAPE": [("n/a" if pd.isna(v) else f"{v:.1f}%") for v in fin["MAPE (%)"]]})
    deck.table("Grading against the revealed 2025 actuals", erows,
               takeaway="The ranking from the backtests held in the real unseen year. A wide interval that contains the truth is not an accurate forecast.",
               col_widths=[3.4, 1.8, 1.6], font_size=15, highlight_rows=[list(fin.index).index("Trend + season regression")])
    deck.bullets("Recommendations",
                 ["**Plan on a trend-plus-seasonal baseline with its 95% interval;** expect about 4% typical monthly error.",
                  "**Staff for the October-December peak and the February trough.**",
                  "**Replace 'last year + 20%' with scenarios** (for example 12%, 18%, 24% growth).",
                  "**Treat outages and pandemics as scenarios,** not trend.",
                  "**Backtest every new model** with rolling origins and compare it with the baseline."],
                 takeaway="Decision needed: adopt the baseline model and quarterly review for the capacity plan.")
    deck.two_columns("Limitations and next steps", "Limitations",
                     ["Nine usable years of seasonality.", "Rolling windows overlap, so backtests are not independent.",
                      "Synthetic data with a simple, known process."],
                     "Next steps",
                     ["Add explanatory drivers.", "Forecast by channel and reconcile to the total.", "Build explicit shock scenarios."])
    out = deck.save(paths["presentation"] / "case_study_presentation.pptx")
    print(f"Saved {out} ({len(deck.prs.slides)} slides)")


if __name__ == "__main__":
    main()
