# Case Study 08 — Why Did "Work Experience" Stop Mattering?

| | |
|---|---|
| **Domain** | Retail lending: income estimation for pre-approved personal loans (HR-style data) |
| **Difficulty** | Intermediate |
| **Importance** | 🔴 MUST GO THROUGH |
| **Techniques** | Coefficient paths · confounding vs mediation vs suppression vs masking · causal diagrams (DAGs) · omitted-variable-bias formula and Gelbach decomposition · total / direct / indirect effects with bootstrap CI · stratified comparisons · added-variable plots · selection on the outcome · balance checks with standardised differences · 10-fold CV and nested F-tests · robustness values for unmeasured confounding · VIF |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual
> customer data.

## 1. Business problem

The bank's income-estimation model v1 said each year of experience adds about 4% to salary. Model v2 adds a
payroll-verified **job grade**, and experience drops to about 0.5% a year. The vendor wants experience removed from the
application form. The team also proposes a metro uplift (+12%), dropping years at the current employer (correlation
0.01) and dropping education (postgraduates earn the same as graduates). Credit Policy must sign off v2.

## 2. Business questions

1. Why did experience's effect collapse when grade was added? Does it still matter?
2. Is the metro uplift real?
3. Should tenure be dropped because its correlation with salary is near zero?
4. Should education be dropped?
5. Which variables should the model keep, with and without a verified grade?

## 3. Dataset

`data/salaried_customers.csv`: 6,000 customers. Columns: age, education (ordinal, 4 levels), years of experience,
years at current employer, job grade (ordinal 1–5), employer category (nominal, 5), metro city, grade-verified flag,
verified monthly salary. The known causal story ([`src/generate_data.py`](src/generate_data.py)): experience → grade
→ salary; employer → metro and employer → salary; tenure lowers pay at the same experience; postgraduates in this
customer base are younger.

## 4. Statistical questions and methods

| Question | Method |
|---|---|
| Why did the coefficient change? | Nested models M0–M5; OVB formula β_short = β_long + γ·δ; Gelbach decomposition |
| Confounder or mediator? | Time order / DAG; total = direct + indirect; bootstrap CI of the share mediated |
| Metro real? | Stratified within-employer comparisons; adjusted coefficient |
| Tenure useless? | Conditional coefficient, added-variable plot, nested F-test, partial R² |
| Education useless? | Comparison within experience bands; conditional coefficients |
| What to keep? | 10-fold CV error with variables removed one at a time; nested F-tests |
| How robust? | Robustness values (Cinelli & Hazlett) |

## 5. Key findings

| Finding | Value |
|---|---|
| Experience | +1.5%/yr alone; **+4.3%/yr** in v1; **+0.5%/yr** at the same grade (v2) |
| Share of experience's effect running through grade | **87%** (bootstrap 95% CI 84%–91%); OVB formula reproduces the change exactly |
| Metro | +12% alone → **−0.9%** in v2 (95% CI −2.2% to +0.3%), confounded by employer type |
| Tenure | +0.1%/yr alone (p = 0.54) → **−4.0%/yr** at the same experience (suppression); partial R² 0.21 in v2 |
| Postgraduate vs Graduate | −0.7% alone → **+21%** at the same experience → +9% at the same grade (masking, then mediation) |
| Prediction (median abs. error, 10-fold CV) | v1 19.0% · v2 14.6% · v2 without experience 14.5% · v2 without tenure 16.2% |
| Selection on outcome | Fitting on salary > ₹75k only: experience 4.3% → 1.3%, tenure −3.9% → −1.0% |
| Robustness value | experience total 0.47 · tenure 0.40 · postgraduate 0.21 · experience direct 0.08 (fragile) |
| Grade coverage balance | all standardised differences ≤ 0.055 (one t-test p = 0.04: a sample-size artefact) |

## 6. Business recommendations

Approve v2 for customers with verified grade and keep v1 for the rest · keep experience on the form · keep tenure and
education · reject the metro uplift · follow up on government/PSU metro customers (−6%, p = 0.006).

## 7. Limitations

Observational associations · ability and performance unmeasured · education masking specific to this customer mix ·
total/direct split assumes a linear model · synthetic data.

## 8. Concepts learned

Confounding vs mediation vs suppression vs masking · why the data cannot tell a confounder from a mediator (time order
and DAGs can) · OVB formula and direction-of-bias table · Gelbach decomposition · total, direct and indirect effects ·
precision variables · never screen variables on simple correlation · selection on the outcome · balance via
standardised differences · prediction vs explanation questions · robustness values.

## How to reproduce

```bash
python case_studies/08_work_experience_confounding/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/08_work_experience_confounding/notebooks/01_analysis.ipynb
python case_studies/08_work_experience_confounding/src/build_presentation.py
```
