# Case Study 23 — Credit-Limit Increase and Customer Spend: Bootstrapping Skewed Metrics

| | |
|---|---|
| **Domain** | Credit cards: credit-limit management |
| **Difficulty** | Intermediate |
| **Importance** | 🟡 GOOD TO HAVE |
| **Techniques** | Stratified two-sample bootstrap · percentile, basic and BCa intervals · bootstrap-t · differences and ratios of means and medians, percentiles, shares, ratio-of-sums metrics · coverage simulation · failure modes (extremes, tiny n, dependence) · permutation test |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual
> customer data. A teaching-only answer key (true population values from a 3-million-customer simulation) is opened only in the grading section.

## 1. Business problem

A random half of 5,000 customers got a 25% limit increase. Spend is very skewed (whales). Finance wants error bars for average spend, typical spend, ratios, the 90th percentile, the share over ₹50,000 and spend per rupee of limit, and the Western region wants the same from a 60 vs 60 pilot.

## 2. Dataset

`data/limit_increase_test.csv` (2,500 vs 2,500) and `data/limit_increase_pilot.csv` (60 vs 60).

## 3. Key findings

| Finding | Value |
|---|---|
| Shape | skewness 12; mean 1.9 times the median; top 1% hold 15% of spend |
| Mean difference | +₹2,003 (BCa −₹1,141 to +₹5,733): includes zero |
| Median difference | +₹1,382 (BCa ₹254 to ₹2,519); ratio 1.09 (1.02 to 1.18) |
| Tail | 90th percentile +₹6,664 and share over ₹50,000 +1.5 pp: both intervals include zero |
| Utilisation | spend per rupee of limit −3.2 pp (−5.2 to −1.1) |
| Pilot (60 vs 60) | mean difference +₹12,600, share over ₹50,000 +15 pp: several times too large; BCa covers the truth for 4 of 7 metrics (main test: 7 of 7) |
| Coverage, mean of lognormal data, n = 30 | t 86% · percentile 85% · BCa 88% · bootstrap-t 91% |
| Failures | maximum 0% · mean of 8 values 76% · autocorrelated series 58% (block bootstrap 88%) |
| Revenue | about ₹385 extra annual interchange per customer, interval −₹219 to +₹1,101 |

## 4. Business recommendations

Report the median effect (about +9%) and the utilisation fall as firm evidence · report the mean with its wide interval · do not use the 60 vs 60 pilot to decide · add a credit-loss outcome before rollout · bootstrap by customer within arm.

## 5. Limitations

Three-month outcome · revenue ignores credit-risk costs · customers assumed independent · synthetic data.

## 6. Concepts learned

The bootstrap gives an interval for any statistic · BCa for medians and ratios at large n; bootstrap-t for the mean of skewed small samples · interval width reflects the metric, not the method · a bootstrap cannot repair a sample that lacks the whales · resample the unit of randomisation.

## How to reproduce

```bash
python case_studies/23_bootstrap_credit_limit_spend/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/23_bootstrap_credit_limit_spend/notebooks/01_analysis.ipynb
python case_studies/23_bootstrap_credit_limit_spend/src/build_presentation.py
```
