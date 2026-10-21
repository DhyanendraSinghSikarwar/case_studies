# Case Study 26 — Collections and SLA: Time Until an Event Happens

| | |
|---|---|
| **Domain** | Collections and operations |
| **Difficulty** | Advanced |
| **Importance** | 🟢 LESS COMMON |
| **Techniques** | Poisson arrivals and the dispersion test · exponential waiting times · Erlang C staffing · censoring · Kaplan-Meier with Greenwood intervals · log-rank test · Cox proportional hazards and a proportional-hazards check · Weibull survival model and extrapolation · SLA probability by segment |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual customer data.
> A teaching-only answer key (true 30-day resolution probability and median time per segment) is opened only in the grading section.

## 1. Business problem

Operations needs an hourly staffing plan for the collections call desk. The Head of Collections has an SLA ("70% of overdue accounts paid up within 30 days") and a report saying 61% of resolved accounts were paid within 30 days. Is the SLA being met, and does call-first help?

## 2. Dataset

`data/collections_accounts.csv`: 6,000 accounts (strategy, bucket, balance band, days observed, resolved or censored). `data/call_arrivals.csv`: calls per 15 minutes for 20 working days.

## 3. Key findings

| Finding | Value |
|---|---|
| Call arrivals | pooled variance ÷ mean 2.0, within each hour 0.80 to 1.18 (no hour rejects Poisson); rate peaks at about 14 calls per 15 min at 11:00 and 15:00 |
| Staffing (80% in 20 s, 6-minute handling) | 4 agents at 13:00 up to 9 at the peaks |
| Censoring | 65% resolved, 35% censored |
| Report's figures | 31.6 days mean, 60.6% of resolved accounts within 30 days |
| Kaplan-Meier | 41.9% resolved by day 30 (CI 40.6% to 43.2%), 61% by 60, 73% by 90; median 42 days |
| Groups | call-first 47.7% vs SMS-first 36.2% by day 30; early 47.4% vs late 34.0%; balance 46.7 / 41.2 / 35.1% |
| Cox hazard ratios | call-first 1.41, late bucket 0.65, balance mid 0.85, high 0.71; proportional hazards looks acceptable |
| Weibull | shape 0.88 (hazard falls over time); extrapolates 90% resolved by day 180 |
| SLA by segment | all 12 segments miss 70%; best 56.8%, worst 20.7% |
| Truth | 40.7% resolved by day 30; KM +1.2 pp, report +20 pp; KM intervals cover the truth in 12 of 12 segments; Cox intervals contain all four true hazard ratios |

## 4. Business recommendations

Report Kaplan-Meier probabilities with intervals by segment, not the share of resolved accounts · expand call-first (alone it lifts the portfolio to about 48% at 30 days) · revisit the 70%-in-30-days target · staff by hour with Erlang C · randomise strategy in the next cycle.

## 5. Limitations

Censoring assumed unrelated to the chance of paying · strategy was not randomised · exponential handling time assumed · the Weibull model is right here by construction · synthetic data.

## 6. Concepts learned

Poisson within a stable period, with a time-varying rate across the day · exponential gaps and the memoryless property · why staffing exceeds offered load · censoring and why averaging durations or dropping open cases is biased · Kaplan-Meier and Greenwood intervals · log-rank and Cox · hazard ratio is not a percentage of accounts · parametric extrapolation is a scenario.

## How to reproduce

```bash
python case_studies/26_collections_sla_time_to_event/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/26_collections_sla_time_to_event/notebooks/01_analysis.ipynb
python case_studies/26_collections_sla_time_to_event/src/build_presentation.py
```
