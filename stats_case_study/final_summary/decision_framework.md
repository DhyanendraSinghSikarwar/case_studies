# Decision framework: from a business request to a defensible answer

Use this when an unfamiliar question lands in your inbox. It is the workflow every case in the book follows (Section 13 of the README),
with the questions to ask at each step and the case that shows the step done well.

## 1. The workflow

```text
Business question → Statistical question → Data and its quality → Method (with alternatives) → Assumption checks
→ Analysis → Validation → Interpretation → What can and cannot be said → Recommendation → Limitations
```

| Step | Ask yourself | Typical trap | Case |
|---|---|---|---|
| 1. Business question | What decision will this change, and what would a "yes" and a "no" look like? | Starting from "which test can I run?" | every case |
| 2. Statistical question | Is it about an average, a proportion, a difference, a relationship, a prediction, a duration, a forecast? | Answering a different question than the one asked | 22 |
| 3. Define the outcome and the population | Observed for whom, measured when, over what window? | Dividing by the cases that finished (the 61% in case 26) | 26 |
| 4. Data quality | Duplicates, labels, impossible values, missingness mechanism, who is in the data? | Cleaning silently | 17, 18, 27 |
| 5. Look first | Plot every variable and every relationship before testing | Reporting a correlation or a mean you never plotted | 05, 16 |
| 6. Pick the method | What is the estimand? What are 2 alternatives and why not them? | Using the default test | 15 |
| 7. Check assumptions | Independence, shape, variance, randomisation, censoring, stationarity | Treating autocorrelated data as independent | 25 |
| 8. Analyse | Estimate, interval, effect size | A p-value alone | 02, 22 |
| 9. Validate | Out of sample, out of time, with a baseline to beat | Judging a model on the data that built it | 13, 25, 27 |
| 10. Interpret | Association or cause? Statistically or practically significant? | Causal language without a causal design | 21 |
| 11. Decide | What does the interval imply against the threshold or break-even? | "Not significant, so no effect" | 22 |
| 12. Communicate | What can we say, what can't we, what would change the answer? | Overconfidence, or hedging so much nothing is said | all |

## 2. Which question are you answering?

```text
Is the question about a difference between groups?
  ├─ Were units randomly assigned?
  │    ├─ yes → experiment: check balance and sample ratio, effect with CI, practical threshold (03, 04, 21, 22)
  │    └─ no  → observational: expect confounding; adjust, weight, or find a design; say "associated with" (08, 20, 21)
  └─ Many groups or many segments? → control the error rate (14, 19)

Is the question about prediction?
  ├─ Binary outcome? → logistic regression; calibration, cost-based cut-off, out-of-time (11, 12, 13, 27)
  ├─ Numeric outcome? → regression with diagnostics (06, 07, 10)
  ├─ Ordered in time? → rolling-origin forecast against a seasonal naive baseline (25)
  └─ Time until an event with unfinished cases? → survival analysis (26)

Is the question about a rate, a count or a probability of an event?
  ├─ Rare event or alert? → base rate and Bayes (24)
  └─ Arrivals per interval? → Poisson per stable period (26)

Is the data itself the problem?
  ├─ Missing? (17)   ├─ Outliers? (16)   ├─ Unrepresentative? (18)   └─ Skewed with no formula? → bootstrap (23)
```

## 3. Before you present: the 10-point check

1. Did I state the **question and the population**?
2. Did I look at the **data quality**, and say what I did?
3. Is every number reported with an **interval or its uncertainty**?
4. Is there an **effect size** and a **practical threshold**?
5. Did I check the **assumptions** that this method needs?
6. If I ran many tests, did I say **how many** and correct for it?
7. Is the result **validated** on data the method did not see?
8. Is my language **causal only where the design supports it**?
9. Did I say what the analysis **cannot** tell us?
10. Would the recommendation change if the main assumption were wrong, and did I say so?

## 4. Phrases to use and to avoid

| Say | Not |
|---|---|
| "Among respondents, the average was 7.9." | "Our customers' satisfaction is 7.9." (18) |
| "The offer reduced churn by about 2 points in a randomised pilot." | "Cashback cuts churn by two thirds." (21) |
| "The data are compatible with an effect from −1.4 to +5.4 points; the pilot was too small to be conclusive." | "No effect was found, so drop it." (22) |
| "Two segments are confirmed; four are promising and need a confirmation wave." | "Seven segments respond." (19) |
| "42% of accounts are paid within 30 days (CI 41% to 43%)." | "61% of resolved accounts were paid within 30 days." (26) |
| "A trend-plus-season model forecast 2025 within 0.1% in total; typical monthly error was about 4% in backtests." | "The forecast is exact." (25) |
| "Higher DTI, lower credit score and prior delinquency are associated with default after adjustment." | "The interest rate drives default." (27) |

## 5. One lesson per case

| # | Case | The lesson |
|---|---|---|
| 01 | Loan portfolio | Describe skewed money with medians and percentiles; a CI is about sampling error only |
| 02 | Income and default | Turn "A is riskier" into a test; report effect sizes with the p-value |
| 03 | Email campaign | Absolute and relative lift tell different stories; an engagement difference is not a campaign effect |
| 04 | Checkout A/B test | Size the test first, check the randomisation, do not peek |
| 05 | Card spend correlation | Plot it; outliers, non-linearity and a third variable can all fake or hide a correlation |
| 06 | Simple regression | The interval for an average and the interval for one customer are different |
| 07 | Loan amount drivers | A coefficient means "holding others constant" and changes with the model |
| 08 | Work experience | A confounder can hide or manufacture an effect |
| 09 | Multicollinearity | Redundant predictors wreck interpretation but not prediction |
| 10 | Insurance claims | Diagnose the residuals; transform or change the model |
| 11 | Churn | Odds ratios, probabilities and marginal effects are different statements |
| 12 | Fraud | Accuracy is useless on rare events; choose the cut-off by cost |
| 13 | Is ML worth it? | Test whether the extra model complexity beats a simple model by more than noise and cost |
| 14 | Channel ANOVA | Compare many groups without inflating the error rate |
| 15 | Branch processing times | Choose parametric or non-parametric on purpose |
| 16 | Payment outliers | Decide what an outlier is before you remove it |
| 17 | Missing income | Deleting and mean-filling bias the answer; the missingness itself can be a signal |
| 18 | Satisfaction survey | A precise number from the wrong people is still wrong; weighting fixes only what is measured |
| 19 | 40 segments | Corrected p-values, the winner's curse and a tiered list |
| 20 | Approval policy | Aggregates can reverse inside segments |
| 21 | Cashback and churn | Adjustment gives confident, wrong intervals; the randomised pilot gave the answer |
| 22 | Significant vs relevant | Compare the interval with the break-even; inconclusive is an honest result |
| 23 | Bootstrap | One algorithm gives an interval for any statistic, until the sample is too small or dependent |
| 24 | Fraud alert and Bayes | The base rate does as much work as the screen |
| 25 | Time series | Autocorrelation breaks ordinary methods; beat seasonal naive in a rolling test |
| 26 | Collections SLA | Censoring makes naive averages and shares wrong; Kaplan-Meier uses every account |
| 27 | Capstone | Real drivers, proxies and confounded variables look alike until you adjust, validate out of time and cost the decision |
