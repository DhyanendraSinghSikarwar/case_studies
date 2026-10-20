# Case Study 21 — Does Cashback Reduce Churn?

| | |
|---|---|
| **Domain** | Credit cards: customer retention |
| **Difficulty** | Intermediate to advanced |
| **Importance** | 🔴 MUST GO THROUGH |
| **Techniques** | Association vs causation · selection into treatment and balance (SMD) · reverse causality · confounders vs mediators ("bad controls") · adjustment ladder · propensity-score weighting and overlap · randomised pilot: intention-to-treat and complier (Wald) effects · E-values · break-even decision |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual
> customer data. A teaching-only answer key (each customer's churn probability with and without cashback) is opened only in the grading section.

## 1. Business problem

Customers who opted into cashback churn at 7% against 26%. Marketing wants to move budget into cashback and push enrolment to everyone. A randomised pilot (offer cashback to a random half) also exists. Does cashback cut churn, and by how much?

## 2. Dataset

`data/observational_customers.csv` (20,000 customers who chose whether to enrol) and `data/pilot_experiment.csv` (16,000 customers, a random half offered cashback, only the offered could enrol).

## 3. Key findings

| Finding | Value |
|---|---|
| Naive gap | −19.4 pp (7.0% vs 26.3%; CI −20.4 to −18.4) |
| Selection | enrolled customers have SMD 0.9 to 1.2 on logins, spend and spend trend; the pilot's SMDs are below 0.015 |
| Adjustment ladder (effect among enrolled) | −19.4 → −16.1 (tenure, income, complaints) → −9.6 (spend, logins) → −7.0 (spend trend) |
| Propensity weighting | −6.2 pp (CI −7.6 to −4.6) |
| Pilot | offer lowers churn by 2.3 pp (CI 1.1 to 3.4); take-up 55.8%; effect of enrolling −4.1 pp (CI −6.1 to −2.0); invalid enrolled-vs-not comparison inside the pilot −13.7 |
| Truth | −4.3 pp among enrolled (−6.4 across all customers); naive is 4.5 times too large; only the pilot's complier interval contains it |
| E-values | naive 7.0, adjusted 3.4 |
| Decision | break-even at ₹450 cost and ₹6,000 per churner is 7.5 pp: profitable on the naive number (+₹710 per enrolled customer), loss-making on the real effect (about −₹190 to −₹205) |

## 4. Business recommendations

Do not scale cashback on the 19-point gap · keep it voluntary and reduce its cost per customer · randomise the offer in further tests, with a holdout · use "associated with" for observational results and "reduces" only for experiments · test cheaper cashback levels and segment effects.

## 5. Limitations

Costs and margins are assumptions · the complier effect assumes the offer acts only through enrolment and describes customers who enrol when offered · 12-month follow-up · synthetic data in which the hidden confounder is known by construction.

## 6. Concepts learned

A large, precise gap can be entirely selection · adjusting for observed variables narrows the gap but gives confident, wrong intervals when something unobserved matters · do not control for mediators · reverse causality (a falling spend trend predicts both non-enrolment and churn) · randomise the offer, and read ITT and complier effects correctly · E-values state how much hidden bias a claim must survive · a biased estimate can flip a business decision.

## How to reproduce

```bash
python case_studies/21_cashback_churn_causality/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/21_cashback_churn_causality/notebooks/01_analysis.ipynb
python case_studies/21_cashback_churn_causality/src/build_presentation.py
```
