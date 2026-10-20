# Case Study 24 — A Fraud Alert Fired: How Worried Should We Be?

| | |
|---|---|
| **Domain** | Banking: card and UPI fraud screening |
| **Difficulty** | Beginner to intermediate |
| **Importance** | 🟡 GOOD TO HAVE |
| **Techniques** | Sensitivity, specificity, PPV · base-rate neglect · natural frequencies · likelihood ratios and the odds form of Bayes · updating with a second alert and checking independence · cost-based decision thresholds · Beta-Binomial shrinkage and empirical-Bayes priors · credible intervals |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual
> customer data. A teaching-only answer key (true fraud rate per merchant group) is opened only in the grading section.

## 1. Business problem

"Our rule catches 85% of fraud, so when it alerts we block the card." Is that right? What if a second (ML) screen also fires, what should be done, and which small merchant groups are really worse than average?

## 2. Dataset

`data/transactions.csv` (150,000 transactions: channel, two alert flags, confirmed fraud) and `data/merchant_groups.csv` (14 groups).

## 3. Key findings

| Finding | Value |
|---|---|
| Rule engine | sensitivity 85%, specificity 97.4%, fraud prevalence 0.42%, so **PPV 12.0%** (CI 11.1% to 13.0%): 88% of alerts are false |
| Per 100,000 transactions | about 360 true alerts and 2,630 false alarms |
| PPV by channel | card present 6% · UPI 12% · card not present 17% (prevalence 0.16%, 0.38%, 0.93%) |
| Likelihood ratios | rule 32, ML 40; prior odds about 1 in 237 |
| Two alerts | both fire: 86.6% fraud (Bayes prediction 84.6%) · rule only 2.5% · ML only 2.5% · neither 0.013% |
| If screens overlap | only 70% independent evidence: P(fraud given both) falls from 85% to 39% |
| Decision (₹300 investigation, ₹12,000 loss, ₹1,500 wrong block) | investigate above 2.5%, block above 11.1% |
| Policy cost | pass all ₹76.1 lakh · block every rule alert ₹70.7 lakh (3,950 genuine blocked) · investigate every alert ₹24.9 lakh · probability-based ₹18.8 lakh (68 blocked) |
| Merchant groups | prior Beta(4.4, 740); P(rate above 1%): N 55%, J 44%, G 21% (G has the highest raw rate, 3 frauds in 189) |
| Shrinkage vs truth | on this one set it did not beat raw rates (squared error 5.6 vs 3.1 ×10⁻⁶); over 3,000 simulated sets it won 71% of the time |

## 4. Business recommendations

Report PPV and alert volume, not just the catch rate · investigate (not block) single alerts where the probability clears the threshold, block on combined evidence · use channel-specific thresholds · check independence before chaining screens · monitor merchant groups with posterior probabilities.

## 5. Limitations

Costs are assumptions · policy thresholds were set on the same data (advantage somewhat optimistic) · fraud rates drift · the screens are independent by construction here · synthetic data.

## 6. Concepts learned

Sensitivity is not predictive value · the base rate does as much work as the screen · natural frequencies · posterior odds = prior odds × likelihood ratio · multiply evidence only if conditionally independent · decisions need costs · shrinkage is better on average, not in every dataset · a flat prior is not neutral.

## How to reproduce

```bash
python case_studies/24_bayes_fraud_alert/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/24_bayes_fraud_alert/notebooks/01_analysis.ipynb
python case_studies/24_bayes_fraud_alert/src/build_presentation.py
```
