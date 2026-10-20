# Case Study 11 — Which Customers Are About to Churn?

| | |
|---|---|
| **Domain** | Retail banking: savings-account retention |
| **Difficulty** | Intermediate |
| **Importance** | 🔴 MUST GO THROUGH |
| **Techniques** | Linear probability model vs logistic regression · probability / odds / log-odds · odds ratio vs risk ratio · separation and penalised fits · Wald vs likelihood-ratio tests · binned-logit plots and splines · interaction testing · average marginal effects with bootstrap CIs · non-collapsibility of odds ratios · AUC, calibration, Hosmer-Lemeshow, Brier · out-of-fold scoring · expected-value threshold under capacity · gains chart |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual
> customer data.

## 1. Business problem

About one in ten savings customers leaves within six months. The Head of Retail Liabilities wants to know what drives
churn, whether "complaints triple churn" is true, and whom the retention team should call (1,000 calls; offer cost
₹600; retained customer worth ₹12,000; assumed offer success 35%).

## 2. Dataset

`data/savings_customers.csv`: 12,000 customers. Columns: age, tenure, segment (ordinal + NRI), region (nominal),
number of products, salary account, credit card, digital logins, 3-month balance change, complaints (0 / 1 / 2+),
churned in 6 months. In the generator ([`src/generate_data.py`](src/generate_data.py)), tenure acts non-linearly,
region has no effect, and the tiny NRI segment almost never churns.

## 3. Methods

Linear probability model vs logistic · 2×2 odds ratio vs risk ratio · separation (NRI) and a ridge-penalised fit ·
main-effects logistic with likelihood-ratio block tests · binned-logit plots, log and spline tenure · complaints ×
salary-account interaction (LR test) · average marginal effects with bootstrap CIs · raw vs adjusted effects
(non-collapsibility) · test-set AUC, calibration, Hosmer-Lemeshow and Brier · 5-fold out-of-fold scores for the call
list · expected-value threshold and capacity.

## 4. Key findings

| Finding | Value |
|---|---|
| Churn rate | 10.5% (1,255 of 12,000) |
| Linear probability model | 1,148 predictions outside 0–1 |
| Complaints (raw) | 8.8% → 16.8% (1) → 28.7% (2+): risk ratios 1.9 and 3.3 |
| Any complaint, 2×2 | risk ratio 2.3, odds ratio 2.6 (= e^β exactly) |
| Separation | NRI (0 of 58 churned): coefficient −20.9, SE 12,276; ridge gives −2.0 |
| Average marginal effects | 2+ complaints +20 pp · 1 complaint +8 pp · salary account −8 pp · tenure 1→5 yrs −6 pp · product −3 pp · card −2 pp · 5 logins −2 pp · balance −10 pts +2 pp |
| Non-collapsibility | 2+ complaints: pp effect unchanged by adjustment (+20), odds ratio 4.2 → 4.9 with no confounding |
| Not drivers | region LR p = 0.97 · segment LR p = 0.26 · complaints × salary interaction p = 0.09 (dropped) |
| Tenure | spline beats linear (LR p < 0.001) |
| Test performance | AUC 0.75 (0.72–0.78) · Hosmer-Lemeshow p = 0.29 · mean predicted 10.9% vs actual 10.5% |
| Call list | break-even p = 14.3% (2,807 customers above it); top 1,000 → 353 churners (28%), precision 35%, net ≈ ₹8.8 lakh; random 1,000 → −₹1.0 lakh; "p > 50%" → 86 calls |

## 5. Business recommendations

Score monthly and call the top 1,000 · run the offer as a randomised test before scaling · escalate repeat complaints
· watch new customers and falling balances · report effects in percentage points · treat NRI customers by rule.

## 6. Limitations

Risk is not persuadability (uplift needs an experiment) · offer success and customer value are assumptions · one
cohort · synthetic data.

## 7. Concepts learned

Why logistic regression · odds and log-odds · odds ratios are not "times as likely" · separation · Wald vs LR tests ·
checking linearity in the log-odds · interactions need evidence, not just a story · marginal effects in percentage
points · non-collapsibility · discrimination vs calibration · thresholds come from costs and capacity, not 0.5.

## How to reproduce

```bash
python case_studies/11_churn_logistic_regression/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/11_churn_logistic_regression/notebooks/01_analysis.ipynb
python case_studies/11_churn_logistic_regression/src/build_presentation.py
```
