# Case Study 09 — Overlapping Risk Signals in a Credit-Limit Model

| | |
|---|---|
| **Domain** | Credit cards: credit-limit assignment |
| **Difficulty** | Intermediate |
| **Importance** | 🟠 SHOULD GO THROUGH |
| **Techniques** | Correlation matrix · VIF, tolerance, condition number and eigenvectors · quarterly refits · individual t-tests vs joint F-test · simulation of collinearity · bootstrap of a coefficient pair · cross-validation · prediction under a changed correlation structure · perfect and structural collinearity · centring · remedies: drop, index, PCA, ridge |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual
> customer data.

## 1. Business problem

Card limits are a multiple of predicted monthly spend. The spend model is refitted quarterly, and its coefficients
jump around: in Q2 neither income variable was significant, in Q4 salary credits came out negative. Is the model
broken, and can it be used for a new self-employed digital pilot?

## 2. Dataset

`data/card_customers.csv`: 4,000 salaried customers in four quarterly cohorts plus 600 self-employed pilot customers.
Columns: declared income, salary credits, average balance, card limits with other banks, number of other cards,
existing EMI, rent, total obligations (= EMI + rent exactly), credit score, age, months with bank, average monthly
spend. In the generator ([`src/generate_data.py`](src/generate_data.py)), spend depends on an unobserved true income;
declared income and salary credits are two noisy copies of it for salaried customers, while for self-employed
customers credits capture only about 55% of income.

## 3. Methods

Correlation matrix and VIF; condition number and smallest-eigenvalue eigenvector; quarterly refits with individual
t-tests, a t-test of the **sum** and a joint F-test; a simulation varying the correlation from 0 to 0.999; 1,000
bootstrap fits of the coefficient pair; 10-fold CV of alternative specifications; bias on the pilot segment; rank
check of a redundant column; centring a squared term; remedies compared (drop, index, PCA, ridge).

## 4. Key findings

| Finding | Value |
|---|---|
| Correlation of log declared income and log salary credits | 0.996 (salaried) vs 0.841 (self-employed pilot) |
| VIF of each | ≈ 116; standard errors × 11 |
| Quarterly coefficients | declared +0.24 to +0.86; credits +0.60 to **−0.04** |
| Their sum (income elasticity) | 0.74 to 0.84 each quarter, SE ≈ 0.035 |
| Q2 | individual p = 0.12 and 0.07; joint F = 225, p < 0.001 |
| Bootstrap | the two coefficients correlate −0.99; SD 0.12 each, 0.02 for the sum |
| Prediction (salaried) | All specifications with income: CV RMSE ≈ 0.298; without income 0.369 |
| Pilot | actual spend 18% above the full model's prediction (−3% to +43% depending on the quarter used); credits-only +60%; declared-only −1% |
| Ridge (CV-tuned) | predicts equally well, but coefficients still unstable (SD 0.18 across quarters) |
| Income index model | coefficient 0.80 (0.77–0.84), max VIF 4.2, stable across quarters (SD 0.04) |
| Redundant column | rank 3 of 4; statsmodels silently returns ±34-billion coefficients |

## 5. Business recommendations

Replace the two income columns with one income index · stop interpreting the separate income coefficients · remove
the duplicate obligations column · do not use the salaried model for the self-employed pilot (limits ≈ 15% too
low); build a segment model · add VIF and rank checks to every quarterly refit.

## 6. Limitations

Spend model only, not default risk · 600 pilot customers · declared income may be inflated in real digital journeys ·
synthetic data.

## 7. Concepts learned

Multicollinearity and its symptoms · VIF and √VIF · condition number · why the sum is precise but the split is not ·
individual vs joint tests · multicollinearity rarely hurts prediction **unless the correlation pattern changes** ·
perfect collinearity and the dummy trap · structural collinearity and centring · choosing a remedy · ridge is for
prediction, not interpretation.

## How to reproduce

```bash
python case_studies/09_multicollinearity_credit_limit/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/09_multicollinearity_credit_limit/notebooks/01_analysis.ipynb
python case_studies/09_multicollinearity_credit_limit/src/build_presentation.py
```
