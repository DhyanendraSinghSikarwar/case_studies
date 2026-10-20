# Case Study 07 — What Drives the Loan Amount a Customer Requests?

| | |
|---|---|
| **Domain** | Retail lending: offer tiers and disbursement forecasting |
| **Difficulty** | Intermediate |
| **Importance** | 🔴 MUST GO THROUGH |
| **Techniques** | Multiple regression on log(amount) · individual vs conditional coefficients · omitted-variable bias · proxies · sign flip · added-variable plot · dummies and reference categories · centring · categorical × numeric interaction · nested F-tests and partial R² · standardised coefficients · VIF · bad controls · holdout validation |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual
> customer data.

## 1. Business problem

Product and Finance want to know what drives requested loan amounts. Dashboard beliefs say metro customers, older
customers, "credit-hungry" customers with more EMIs, and high-score customers all ask for more. Which are real, and can
we forecast requests better than with income alone (Case 06)?

## 2. Dataset

`data/loan_applications.csv`: 5,000 applications. Columns: income, existing EMI, age, credit score, employment type
(3 levels), loan purpose (6), city tier (4), requested tenure, requested amount. The true process
([`src/generate_data.py`](src/generate_data.py)): income elasticity 0.90 (steeper for self-employed), affordability
penalty for existing EMIs, purpose effects, small score effect, **no** direct city-tier or age effect.

## 3. Methods

Simple vs stepwise multiple regressions (M1–M5) on log amount, with log income centred at ₹50k. Added-variable plot
for the EMI sign flip. Nested F-tests and partial R² for each block. Income × employment interaction with group
slopes. Standardised coefficients. VIF and residual checks. Holdout R², 80% PI coverage and width. A "bad control"
demonstration with requested tenure.

## 4. Key findings

| Finding | Value |
|---|---|
| Income elasticity, income only | 0.81 (biased down by omitting EMIs) |
| Income elasticity, full model | Salaried **0.87** (0.83–0.90); self-employed **1.03** (0.99–1.08); interaction p < 0.001 |
| Existing EMI per ₹1k | Individually **+0.6%** → conditionally **−1.2%** (sign flip; corr with income 0.53) |
| City tier | Tier-3 vs Metro −31% alone → −0.1% conditionally; block F p = 0.34 |
| Age | +1.3%/yr alone → ≈ 0 conditionally (p = 0.31) |
| Credit score | Shrinks by about 2/3; ≈ +5% per 50 points |
| Purpose (vs debt consolidation) | Wedding +45%, home renovation +34%, education +22%, medical −9%, travel −25% |
| Employment at ₹50k income | Professional +10%, self-employed +8% vs salaried |
| Unique contribution (partial R²) | income 0.51 · purpose 0.28 · existing EMI 0.13 · employment 0.02 · score 0.02 · city tier ≈ 0 · age ≈ 0 |
| Bad control | Adding tenure: R² 0.655 → 0.718, income elasticity 0.92 → 0.75 (misleading) |
| Holdout | R² 0.47 → 0.69; 80% PI width ×3.2 → ×2.5 with ≈ 80% coverage; median error 31% → 23% |

## 5. Business recommendations

Tier offers on income, EMI headroom, purpose and employment type · drop city tier and age · retire "credit-hungry"
targeting · give Finance the multi-driver model · keep tenure out of driver models.

## 6. Limitations

Associations, not causes · only observed variables · requested (not approved) amounts · synthetic data.

## 7. Concepts learned

Individual vs conditional relationships · holding constant · omitted-variable bias · proxies · sign flips · added-variable
plots · dummies and references · centring · interactions · nested F-tests · partial R² · standardised coefficients ·
VIF · bad controls · holdout validation.

## How to reproduce

```bash
python case_studies/07_loan_amount_drivers/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/07_loan_amount_drivers/notebooks/01_analysis.ipynb
python case_studies/07_loan_amount_drivers/src/build_presentation.py
```
