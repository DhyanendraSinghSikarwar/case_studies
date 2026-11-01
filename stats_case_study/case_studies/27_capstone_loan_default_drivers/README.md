# Case Study 27 (Capstone) — What Drives Loan Default, and What Should Risk Do?

| | |
|---|---|
| **Domain** | Credit risk: unsecured personal loans |
| **Difficulty** | Advanced |
| **Importance** | 🔴 MUST GO THROUGH |
| **Techniques** | Data profiling and cleaning · missingness analysis · univariate tests with Benjamini-Hochberg · raw vs adjusted odds ratios (confounding, proxies) · VIF · likelihood-ratio tests · logistic regression, odds ratios and marginal effects · linearity checks · AUC, PR-AUC, KS, Brier, calibration · out-of-time validation and PSI · cost-based approval policy · grading against an answer key |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual customer data.
> Teaching-only answer keys (true coefficients and every loan's true default probability) are opened only in the grading section.

## 1. Business problem

Default was 7.5% against 6% priced. The dashboard says agent-sourced loans default almost twice as often, higher-rate loans default more, and higher-income borrowers default less. Risk wants to stop agent lending, raise the minimum income and price harder on rate segments. What actually drives default, how well can it be predicted, and what policy should be adopted?

## 2. Dataset

`data/loan_applications.csv`: 24,060 rows (including 60 duplicates) of applications from 2022 and 2023 with borrower, loan and channel variables and a 12-month default flag.

## 3. Key findings

| Finding | Value |
|---|---|
| Data quality | 60 duplicates, nine spellings of three employment labels, 3 impossible ages, 25 incomes with two extra zeros, 6.5% income missing (more for agent and self-employed), 5.1% thin files (10.1% default against 7.3%) |
| Dashboard claims, raw to adjusted OR | agent channel 1.85 to 1.15 (CI 0.97 to 1.35) · interest rate 1.64 to 1.06 · income 0.89 to 0.98 · age 0.90 to 1.00 |
| Why | agent borrowers have a mean score of 627 vs 660; interest rate and credit score correlate −0.84 |
| Real drivers (odds ratios) | prior delinquency 1.7 / 4.1, gig 2.2, self-employed 1.4, loan-to-income 2.1, thin file 2.0, DTI 1.6 per 10 points, credit score 0.57 per 50 points, utilisation 1.015 per point |
| Effects on default probability | DTI +10 points +3.2 pp · credit score +50 −2.9 pp · gig +4.5 pp · agent channel +0.5 pp |
| Kitchen-sink model | interest rate, age, income, city tier add nothing (LR p = 0.92) |
| Out-of-time (2023) | AUC 0.793 (CI 0.777 to 0.808), KS 0.44, calibration slope 0.96; credit score alone 0.726; PSI of score 0.003; agent share 21.9% to 29.0% |
| Policy on 2023 loans | approve all ₹135 lakh · agent ban ₹191 lakh · score ≥ 650 ₹237 lakh · model (PD below 9.1%) ₹334 lakh |
| Truth | 9 of 10 coefficient intervals cover the truth (thin file misses); AUC ceiling 0.798; model captures about 95% of attainable profit |

## 4. Business recommendations

Decline the three proposed actions (they act on proxies) · adopt a probability-based approval rule with a cut-off of about 9% to 13% · recalibrate before pricing · cap DTI and utilisation, scale loan size to income, treat prior delinquency and thin files more strictly · monitor calibration, PSI, agent share and default by channel quarterly.

## 5. Limitations

Observational, so "driver" means "associated after adjustment" · cost assumptions drive the policy results · one out-of-time year · simple missing-data treatments · synthetic data with a known process.

## 6. Concepts learned

How the whole workflow fits together · raw associations can be proxies and confounding · a model is judged out of time, by calibration and by the decision it supports · significant is not important at n = 12,000 · a recommendation states what it would change if an assumption failed.

## How to reproduce

```bash
python case_studies/27_capstone_loan_default_drivers/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/27_capstone_loan_default_drivers/notebooks/01_analysis.ipynb
python case_studies/27_capstone_loan_default_drivers/src/build_presentation.py
```
