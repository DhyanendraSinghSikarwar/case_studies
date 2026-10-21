# Statistics cheat sheet for data scientists

One page per topic, in the order a working analyst needs them. Each line points to the case that teaches it in depth.
All numbers quoted in the cases come from synthetic data; the rules below do not depend on them.

## 1. Which method for which question

| You want to… | Data | Use | Case |
|---|---|---|---|
| Summarise a skewed amount (income, loan size, spend) | one numeric variable | median, percentiles, IQR; mean only with its interval; log scale for plots | 01, 23 |
| Put an interval on a mean | numeric, n large or roughly symmetric | t-interval; bootstrap if skewed or small | 01, 23 |
| Put an interval on a proportion | binary | Wilson (or exact) interval, never the plain Wald at small n or near 0 or 1 | 01, 03 |
| Compare two group means | numeric, two groups | Welch t-test; Mann-Whitney if heavy tails and the question is about ranks | 02, 15 |
| Compare paired measurements | before/after on the same unit | paired t or Wilcoxon signed-rank | 15 |
| Compare two proportions | binary, two groups | two-proportion z (Fisher if counts are small), report the absolute and relative difference | 03, 04 |
| Association of two categoricals | contingency table | chi-square test of independence, Cramér's V | 02 |
| Compare 3+ groups | numeric | ANOVA (Welch ANOVA if variances differ), then Tukey; Kruskal-Wallis and Dunn for skewed data | 14, 15 |
| Many tests at once | any | Holm for "no false alarm"; Benjamini-Hochberg for screening lists; report how many were examined | 19 |
| Relationship of two numerics | numeric | Pearson (linear), Spearman (monotonic); always plot first | 05 |
| Predict a number | numeric target | linear regression; transform the target if skewed; check residuals | 06, 07, 10 |
| Predict a yes/no | binary target | logistic regression; judge by calibration and cost, not accuracy | 11, 12 |
| Time until an event, with unfinished cases | durations + censoring | Kaplan-Meier, log-rank, Cox, parametric survival | 26 |
| Counts per interval | counts | Poisson, check variance ÷ mean within a stable period | 26 |
| Forecast a series | ordered in time | log, decompose, seasonal naive baseline, rolling-origin test | 25 |
| Update a belief with evidence | rate or prior | Bayes' theorem, odds form, Beta-Binomial | 24 |

## 2. Intervals and tests: reading them correctly

- A **p-value** is the probability of data at least this extreme **if the null were true**. It is not the probability that the null is true, and p > 0.05 does not mean "no effect" (02, 22).
- A **confidence interval** is a statement about the procedure: 95% of intervals built this way contain the truth. It measures **sampling error only**, never bias (18).
- **Compare the interval with a decision threshold** (break-even, SLA, equivalence margin), not with zero (22, 26).
- **Effect sizes** belong next to every p-value: difference in means or proportions, Cohen's d or h, odds ratio, hazard ratio, Cramér's V, AUC (02, 03, 14, 15).
- **Sample size:** a tiny effect becomes "significant" with enough data, and a large effect hides in a small study; plan sample size for the smallest effect that matters (04, 22).
- **Peeking** at a running test inflates false positives; fix the sample size and the stopping rule in advance (04).
- **Intervals for odd statistics** (medians, ratios, percentiles): bootstrap. BCa for large samples; bootstrap-t for the mean of skewed small samples; resample the unit of randomisation (23).

## 3. Regression and logistic regression

| Topic | Rule | Case |
|---|---|---|
| Coefficient meaning | "holding the other variables constant"; it changes when you change the other variables | 07 |
| Confounding | a variable's effect can vanish, appear, or reverse once a related variable enters; decide controls from the causal story, not from p-values | 08 |
| Multicollinearity | VIF above about 5 to 10: coefficients are unstable, predictions are fine; drop a proxy or combine | 09 |
| Diagnostics | residual vs fitted, Q-Q, scale-location, leverage and Cook's distance; fix with a transform, a different model or robust standard errors | 10 |
| Log-odds, odds ratio, probability | odds ratios are not risk ratios and are not collapsible; report percentage-point effects for the business | 11 |
| Never use accuracy on rare events | use precision, recall, PR-AUC, calibration and a cost-based threshold | 12 |
| Prediction vs explanation | explaining needs a causal design; predicting needs out-of-sample validation | 13, 21 |
| Model comparison | rolling or repeated CV, a paired test of the difference, calibration, out-of-time stability | 13, 27 |

## 4. Study design and causality

1. **Association is not causation.** Enrolled customers churn less because engaged customers enrol (21).
2. **Confounders** are before the treatment and affect both; **mediators** are caused by the treatment (do not control for them); **colliders** and consequences of the outcome are traps.
3. **Adjusting for what you can measure gives narrow, confident, wrong intervals** if something unmeasured matters (21).
4. **Randomise the offer**; read the intention-to-treat effect as "the effect of offering" and ITT ÷ take-up as the effect on those who enrol (21).
5. **Check randomisation:** balance on pre-treatment variables, and the sample-ratio check (04).
6. **Segment results can reverse the overall result** (Simpson); compare like with like or standardise (20).
7. **Selected winners are overstated** (winner's curse): replicate, or shrink (19, 22).
8. **Who answered?** Compare respondents with the frame; weighting fixes only what the weighting variables explain; a random follow-up of non-respondents measures the rest (18).

## 5. Data problems

| Problem | First move | Case |
|---|---|---|
| Outliers | decide what they are (error, fraud, VIP, rare event) before touching them | 16 |
| Missing values | ask why (MCAR, MAR, MNAR); deleting and mean-filling bias; multiple imputation with the outcome in the model | 17 |
| Duplicates, label inconsistencies, impossible values | profile before modelling; log every change | 27 |
| Biased sample | frame, response-rate by group, weights, follow-up | 18 |
| Leakage | any variable that exists only because of the outcome; check feature timing | 13 |
| Drift | compare the development and the later sample (PSI, mix, calibration) | 27 |

## 6. Time, durations and counts

- **Time series:** log if the swings grow with the level; decompose into trend, seasonal and remainder; difference to reach stationarity (ADF); evaluate by **rolling origin**; the baseline to beat is seasonal naive, with drift if growing; a wide interval that contains the truth is not an accurate forecast (25).
- **Censored durations:** never average observed durations or drop unfinished cases; Kaplan-Meier uses every case for as long as it was observed (26).
- **Hazard ratio is not a percentage of accounts.** Report the probability by a fixed time (26).
- **Poisson counts:** variance equals the mean within a stable period; if the rate changes through the day, estimate it per period; staffing needs more than the offered load (26).
- **Extrapolation beyond the data** is a scenario, not a measurement (25, 26).

## 7. Reporting rules

1. State the **question** and the **population** the answer covers.
2. Give the **estimate, the interval and the effect size**, with units.
3. Say what the interval does **not** cover (bias, selection, model choice).
4. Use **"associated with"** unless a randomised or otherwise credible design supports "causes".
5. Say **how many things were looked at**.
6. Say **what would change the recommendation** (a threshold, an assumption).
7. Show the **decision**: the recommendation, its cost and its confidence.
