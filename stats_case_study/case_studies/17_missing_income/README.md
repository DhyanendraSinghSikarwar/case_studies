# Case Study 17 — The Missing Income Problem: Deleting, Filling or Imputing?

| | |
|---|---|
| **Domain** | Credit risk: personal-loan scorecard |
| **Difficulty** | Intermediate |
| **Importance** | 🟠 SHOULD GO THROUGH |
| **Techniques** | MCAR / MAR / MNAR diagnosis · missingness models · complete cases · mean, group-mean, regression, stochastic and multiple imputation (Rubin's rules) · outcome in the imputation model · delta-adjustment sensitivity analysis · repeated-sampling simulation · scoring with a missing-value indicator |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual
> customer data. A teaching-only answer key (`data/answer_key_teaching_only.csv`, with every applicant's true income)
> is opened only in the grading section of the notebook.

## 1. Business problem

23% of personal-loan applications have no income. Analysts delete them or fill them with the average. Which approach gives a trustworthy estimate of how income affects default, and which is best for scoring new applicants?

## 2. Dataset

`data/applications.csv`: 8,000 applications with age, employment type, channel, city tier, loan amount, employment years (4.8% missing), monthly income (23.4% missing), credit score (6.2% missing: thin files) and 12-month default.

## 3. Methods

Missingness patterns and drivers · comparison of missing vs present · logistic models of missingness · eight handling strategies · multiple imputation with 20 draws and Rubin's rules, with and without the outcome in the imputation model · delta sensitivity · grading against true income · 150-dataset repeated-sampling simulation · scoring comparison on a test set.

## 4. Key findings

| Finding | Value |
|---|---|
| Missingness | income 23.4%, score 6.2%, years 4.8%; default 31% when income is missing vs 15% when given |
| Truth (income coefficient) | −1.102 |
| One dataset | complete cases −0.96 (13% off), mean fill −0.66 (41%), MI excluding outcome −0.74 (33%), MI including outcome −0.98 (11%) |
| 150 simulated datasets: bias / CI coverage | complete cases 14% / 56% · mean fill 43% / 0% · mean + indicator 19% / 22% · one stochastic fill 32% / 0% · MI without outcome 32% / 0% · **MI with outcome 8% / 91%** |
| Sensitivity | the true MNAR gap is about 0.18 log points; the income effect stays between −1.07 and −0.99 for gaps up to 0.5 |
| Scoring (test AUC) | 0.729–0.767; fill plus missing-income flag is best |

## 5. Business recommendations

Use multiple imputation with the outcome in the imputation model for estimation · for production scoring use a simple fill plus a missing-income flag · report a sensitivity range · track the missing rate by channel and fix collection at source.

## 6. Limitations

Simple simulated mechanism · one imputed variable (real projects impute several jointly) · MNAR can be bounded but not tested · synthetic data.

## 7. Concepts learned

MCAR, MAR and MNAR · deleting and mean-filling bias estimates and shrink variance · the outcome must be in the imputation model · Rubin's rules and the fraction of missing information · one dataset can mislead, so simulate · estimation and prediction need different handling · missingness itself can be a signal.

## How to reproduce

```bash
python case_studies/17_missing_income/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/17_missing_income/notebooks/01_analysis.ipynb
python case_studies/17_missing_income/src/build_presentation.py
```
