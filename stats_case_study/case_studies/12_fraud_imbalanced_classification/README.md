# Case Study 12 — Card Transaction Fraud Detection

| | |
|---|---|
| **Domain** | Payments: card fraud |
| **Difficulty** | Advanced |
| **Importance** | 🔴 MUST GO THROUGH |
| **Techniques** | Accuracy paradox · confusion matrix, precision, recall, specificity, F1/F2, MCC · ROC vs precision-recall curves and prevalence sensitivity · bootstrap CIs for AUC/PR-AUC · class weights, undersampling, oversampling, SMOTE (hand-built) · prior correction and calibration · F1-, cost- and capacity-based thresholds · amount-aware expected-loss rule · Wilson and bootstrap uncertainty · out-of-time validation and drift by segment |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual
> customer data.

## 1. Business problem

A vendor claims "99.6% accuracy, AUC 0.97". The issuer's two rules (amount > ₹50,000; international e-commerce)
catch little fraud and flood analysts, who can review about 1% of transactions. Missed fraud costs ~80% of the amount;
each alert costs ~₹150. How good is a model really, should the data be rebalanced, and where should the threshold be?

## 2. Dataset

`data/card_transactions.csv`: 120,000 transactions over 4 months (30,000 a month), fraud 0.4% (479 frauds). Columns:
amount, merchant category (nominal, 8), channel (nominal, 4), hour, international, new merchant, new device, transactions
in last 24 h, amount vs the customer's 90-day average, card age. The generator
([`src/generate_data.py`](src/generate_data.py)) adds a new online-gaming fraud pattern in month 4.

## 3. Methods

Train on months 1–3, test on month 4 · baselines ("flag nothing", current rules, random) · logistic regression and
gradient boosting with bootstrap CIs · ROC vs PR curves and a prevalence experiment · four rebalancing schemes vs the
standard fit, with prior correction · thresholds chosen on out-of-fold scores (F1, cost, capacity) and an amount-aware
expected-loss rule · policy comparison in ₹ · Wilson/bootstrap uncertainty · monthly and per-merchant calibration.

## 4. Key findings

| Finding | Value |
|---|---|
| "Flag nothing" | 99.48% accurate, catches 0 frauds |
| Current rules (month 4) | 1,256 alerts, precision 2.9%, recall 23%, 62% of fraud ₹ stopped; saving ₹7.1 lakh |
| Logistic model | ROC-AUC 0.966 (0.955–0.976) vs PR-AUC 0.43 (0.35–0.51); random PR-AUC = 0.005 |
| Gradient boosting | PR-AUC 0.25; reliably worse (difference +0.18, CI +0.13 to +0.22) |
| Prevalence experiment | ROC-AUC ≈ 0.96–0.97 at every fraud rate; PR-AUC 0.25 (0.1%) → 0.44 (0.5%) → 0.96 (50%) |
| Rebalancing | ranking unchanged (ROC-AUC 0.965–0.967); mean predicted fraud 2–17% vs actual 0.5%; prior correction restores calibration |
| Thresholds (from months 1–3) | F1-optimal 0.26 · cost-optimal 0.007 · top 1% ≈ 0.06 |
| Policies, month 4 saving | p > 0.5 ₹1.3 L · F1 ₹4.2 L · rules ₹7.1 L · cost-optimal ₹9.4 L · top-1% ₹9.6 L · amount-aware ₹10.8 L (890 alerts) · amount-aware on class-weighted model **−₹5.6 L** |
| Recommended (expected loss, top 1%) | 300 alerts · recall 33% (26–41%) · precision 17% (13–22%) · 72% of fraud ₹ · saving ₹9.9 L · +₹2.8 L vs rules (CI +₹0.8–4.7 L) |
| Drift | month 4 actual ÷ predicted = 1.39; excess almost all in online gaming (115 vs 68) |

## 5. Business recommendations

Replace the rules with the model · rank by expected loss and review the top 1% · do not rebalance (or prior-correct if
sampling for speed) · retrain monthly and monitor calibration by merchant · report precision, recall and ₹ stopped with
ranges.

## 6. Limitations

One test month (157 frauds) · assumed costs · no label delay or adaptive fraudsters · reviewed fraud assumed stopped ·
synthetic data.

## 7. Concepts learned

Accuracy paradox · precision vs recall vs specificity · ROC-AUC measures ranking, PR-AUC measures usefulness at the
real prevalence · rebalancing shifts thresholds and breaks calibration · prior correction · thresholds come from costs,
amounts and capacity · expected-loss ranking · few positives → wide CIs · out-of-time validation and drift.

## How to reproduce

```bash
python case_studies/12_fraud_imbalanced_classification/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/12_fraud_imbalanced_classification/notebooks/01_analysis.ipynb
python case_studies/12_fraud_imbalanced_classification/src/build_presentation.py
```
