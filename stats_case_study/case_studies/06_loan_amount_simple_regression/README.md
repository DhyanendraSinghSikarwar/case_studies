# Case Study 06 — Predicting Loan Amount from Income

| | |
|---|---|
| **Domain** | Retail lending: branch pre-offers |
| **Difficulty** | Beginner–Intermediate |
| **Importance** | 🔴 MUST GO THROUGH |
| **Techniques** | Simple linear regression · least squares by hand · slope/intercept interpretation · centring · SST = SSR + SSE, R², RMSE · SE, t-test, CI for the slope · CI for the mean vs prediction interval · LINE assumptions · residual / Q-Q / scale-location / leverage plots · Breusch-Pagan · HC3 robust SEs · leverage and Cook's distance · log-log model and elasticity · back-transformation (median vs mean) · holdout calibration of intervals · extrapolation |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual
> customer data.

## 1. Business problem

The Head of Personal Loans wants a simple branch rule: from verified monthly income, suggest a loan amount to pre-offer
with a realistic range, and state how much more customers borrow per extra ₹10,000 of income.

## 2. Business questions

How strong is the income–amount relationship? How much more per ₹10k? What should we suggest for a given income, with
what range? Is a straight-line rule good enough?

## 3. Dataset

`data/loans_income_amount.csv`: 3,000 disbursed personal loans (monthly income, loan amount, employment type,
month). It contains 2 annual-as-monthly income errors (excluded) and 4 capped high earners (₹20 lakh limit, high
leverage). True process: amount ∝ income^0.95 with multiplicative noise ([`src/generate_data.py`](src/generate_data.py)).
A 25% holdout is set aside before modelling.

## 4. Statistical questions and methods

| Question | Method |
|---|---|
| Strength | R² (= r²), RMSE |
| ₹ per ₹10k | OLS slope with classical and HC3 CIs |
| Suggested amount and range | CI for the mean vs prediction interval; log-log model with back-transformed 80% PIs |
| Is a straight line OK? | Diagnostic plots, Breusch-Pagan, Cook's distance; holdout PI coverage by income band |

## 5. Key findings

| Finding | Value |
|---|---|
| Raw model slope | **₹26,400 per ₹10k income** (HC3 95% CI ₹24,500–₹28,200); R² = 0.59; RMSE ≈ ₹86k |
| Raw model assumptions | Funnel-shaped residuals (Breusch-Pagan p < 0.001); heavy right tail; robust SE ≈ 2× classical |
| Capped high earners | 2 points raise R² from 0.51 to 0.59 (Cook's D up to ≈ 0.7) |
| Raw 95% PI | ≈ ±₹1.7 lakh everywhere; below zero at ₹30k income |
| Log-log elasticity | **0.92** (0.89–0.95): +10% income → ≈ +9% loan; typical customer within ×/÷ 1.5 |
| Holdout 80% PI coverage | Raw model 99% (lowest band) to 71% (top band), 90% overall; **log model 73–86% in every band** (81% overall) |
| Holdout accuracy | Log model MAE ₹52k vs raw ₹55k; median abs. % error 26% vs 28% |
| Extrapolation | Data barely extends past ₹2.5 lakh/month; above ~₹4 lakh, the product cap decides |

## 6. Business recommendations

1. Adopt the log-log pre-offer table (median suggestion + 80% range) for incomes up to ₹4 lakh/month.
2. Above ₹4 lakh/month, offer the cap and refer to an RM.
3. In planning decks: "≈ ₹26,000 more per ₹10,000 of income, on average", with its range.
4. Add other drivers next (Case 07).

## 7. Limitations

Income is the only predictor · approved loans only · censoring at floor and cap · six months of data · synthetic data.

## 8. Concepts learned

Regression equation · least squares · slope/intercept/centring · R² and RMSE · slope inference · CI vs PI · LINE
assumptions · diagnostics · heteroscedasticity and HC3 · leverage and Cook's distance · log-log and elasticity ·
back-transformation · interval calibration on holdout data · extrapolation.

## How to reproduce

```bash
python case_studies/06_loan_amount_simple_regression/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/06_loan_amount_simple_regression/notebooks/01_analysis.ipynb
python case_studies/06_loan_amount_simple_regression/src/build_presentation.py
```
