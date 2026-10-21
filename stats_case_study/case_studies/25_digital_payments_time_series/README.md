# Case Study 25 — Monthly Digital-Payments Volume: A Time Series and an Honest Baseline

| | |
|---|---|
| **Domain** | Payments / finance: capacity and budget planning |
| **Difficulty** | Intermediate |
| **Importance** | 🟡 GOOD TO HAVE |
| **Techniques** | Trend and seasonality · STL decomposition · rolling statistics · ACF/PACF · ADF stationarity test and differencing · shocks and outliers · naive, seasonal naive, drift, damped Holt-Winters, SARIMA and trend-season regression · rolling-origin evaluation · MAPE and MASE · interval coverage |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual company data.
> The next 12 months (2025) and the true components are in teaching-only files opened only in the grading section.

## 1. Business problem

Finance proposes "take the 2024 total and add 20%". Is there a seasonal pattern to staff for, what did COVID do, and how wrong could a forecast be?

## 2. Dataset

`data/monthly_volume.csv`: 108 months (Jan 2016 to Dec 2024) of transaction volume in millions, with days in month.

## 3. Key findings

| Finding | Value |
|---|---|
| Trend | year-over-year trend growth 52% (Jan 2017) to 19% (Dec 2024); calendar-year growth 57, 50, 46, 29, 51, 27, 27, 24% |
| Seasonality | October ×1.09, November ×1.04, December ×1.06, February ×0.87 (short month), March ×1.04 |
| Stationarity | ADF p: raw 1.00, log 0.05, log first difference 0.014, first + seasonal difference 0.0002; STL remainder lag-1 autocorrelation 0.61 |
| Shocks | COVID about −0.31 log points (74% of expected); March 2023 outage −0.23 |
| Rolling-origin MAPE (9 origins) | regression 4.2% · damped Holt-Winters 6.7% · seasonal naive + drift 8.7% · SARIMA 9.8% (bias +8%) · naive 14.4% · seasonal naive 21.4% |
| Shock dummies | did not improve forecast MAPE (3.8% without, 4.2% with); they clean up the seasonal estimates |
| Interval coverage (95% nominal) | SARIMA 96%, regression 95% |
| 2025 (actual 4,822 million, +18.6%) | regression +0.1% · Holt-Winters +0.5% · seasonal naive + drift +5.1% · SARIMA +10.6% · seasonal naive −15.7% · "last year + 20%" +1.2% |

## 4. Business recommendations

Use a trend-plus-seasonal regression (or damped Holt-Winters) as the baseline, publish its interval, and compare any fancier model in a rolling-origin test · staff for the October to December peak and February trough · replace a fixed growth rule with scenarios (about 12% to 24%) · treat outages and pandemics as scenarios.

## 5. Limitations

108 months give nine seasonal cycles · rolling windows overlap · intervals checked on nine origins only · known, simple process · synthetic data.

## 6. Concepts learned

Autocorrelation breaks ordinary formulas and random splits · logs and differencing for stationarity · ADF has low power with trends and shocks · seasonal naive is a poor baseline for fast-growing series · simple models often win · a wide interval that contains the truth is not an accurate forecast · calendar effects are part of the seasonal estimate.

## How to reproduce

```bash
python case_studies/25_digital_payments_time_series/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/25_digital_payments_time_series/notebooks/01_analysis.ipynb
python case_studies/25_digital_payments_time_series/src/build_presentation.py
```
