# Statistics for Data Science — A Real-World Case Study Book

> **A practical statistics playbook for data scientists.** Each chapter is a business problem with data, a full
> analysis in Python, and a deck for stakeholders. You learn statistics by working through the problems a data
> scientist in banking, fintech, insurance, marketing, product or operations is actually given.

---

## 1. Purpose

Most statistics material starts with a formula and looks for an example. This book does it the other way round.
Every case study starts with a request like the ones that land in a data scientist's inbox:

> *"Our risk team believes customers with higher income default less. Is that actually true?"*
>
> *"Marketing says the new email campaign lifted conversion by 0.4 points. Should we roll it out?"*
>
> *"Customers who use cashback churn less. Should we give cashback to everyone?"*

Each case then works through the questions an experienced analyst asks:

```text
What is the business really asking?  →  What is the statistical question?  →  Which method, and why?
→  Are the assumptions reasonable?  →  What does the result mean?  →  What can I say with confidence,
and what can't I say?  →  What should the business do?  →  How do I present it?
```

The goal is to take a **low/intermediate learner** to the point where they can take an unfamiliar business question,
choose sensible methods, defend their choices, and **present conclusions with the right amount of confidence**:
no more certainty than the data supports, and no less.

## 2. Who this book is for

| You are… | You will get… |
|---|---|
| A junior/intermediate data scientist or analyst | A structured path from descriptive statistics to regression, experiments and causal thinking, all on realistic data |
| A business/risk/marketing/product analyst moving into data science | The statistical reasoning behind the dashboards you already build |
| A student preparing for industry roles | Exposure to the messy data, ambiguous questions and stakeholder communication that textbooks skip |
| A senior who mentors others | A ready-made curriculum and a common vocabulary for reviewing analyses |

**Prerequisites:** basic Python (pandas, functions, plotting) and school-level algebra. Each concept is explained when
it is first needed.

## 3. How to use this repository

1. **Follow the learning path** in [Section 12](#12-learning-path). Cases build on each other. The 🔴 cases are the core.
2. **For each case, read the case README first.** It states the business problem, findings and recommendations in two
   pages, so you know where the analysis is heading.
3. **Work through the notebook** (`notebooks/01_analysis.ipynb`). Notebooks are written as a senior data scientist
   explaining their reasoning to a colleague. Read the markdown as carefully as the code.
4. **Pause at every "Method selection" and "What can we say?" section.** Before reading on, try to decide for yourself
   which method you would choose and what you would claim.
5. **Open the deck** (`presentation/case_study_presentation.pptx`) to see how the same analysis is told to a business
   head, without formulas.
6. **Re-run everything.** Data is synthetic and seeded, so you get identical numbers. Then change the data-generating
   assumptions in `src/generate_data.py` and see which conclusions survive.

## 4. Repository structure

```text
stats_case_study/
├── README.md                     ← you are here (roadmap)
├── PROGRESS.md                   ← build status of every case
├── requirements.txt / environment.yml
├── LICENSE
├── 00_shared_resources/          ← plotting style, stats helpers, deck builder used by every case
│   ├── utils.py
│   ├── plotting.py
│   ├── statistical_tests.py
│   ├── presentation.py
│   └── README.md
├── case_studies/
│   └── NN_case_name/
│       ├── README.md             ← business problem, findings, recommendations, limitations
│       ├── data/                 ← generated CSV(s) + data dictionary
│       ├── src/
│       │   ├── generate_data.py  ← documented, seeded synthetic data generator
│       │   └── build_presentation.py
│       ├── notebooks/
│       │   └── 01_analysis.ipynb ← the full, executed, educational analysis
│       ├── outputs/
│       │   ├── figures/          ← high-resolution PNGs used in notebook and deck
│       │   └── tables/           ← result tables as CSV
│       └── presentation/
│           └── case_study_presentation.pptx
└── final_summary/
    ├── statistics_cheat_sheet.md
    ├── decision_framework.md
    └── presentation/
```

## 5. Statistical concepts covered

The matrix shows where each concept is **taught in depth** (●) and where it is **used or revisited** (○).
Case numbers refer to the roadmap in Section 6.

| Concept area | Taught in depth (●) | Revisited (○) |
|---|---|---|
| Descriptive statistics: mean/median/mode, variance, SD, percentiles, IQR, CV, skewness, kurtosis, five-number summary | 01 | 02, 10, 16, 23, 27 |
| Distribution shape; normal, log-normal, uniform | 01 | 10, 16, 23 |
| Bernoulli and binomial | 03 | 04, 11, 24 |
| Poisson and exponential | 26 | 16 |
| Gamma and Beta | 10 (gamma), 24 (beta) | 26 |
| t, chi-square and F distributions | 02 (t, χ²), 14 (F) | 06, 07 |
| Probability: joint, marginal, conditional, independence | 02 | 20, 24 |
| Bayes' theorem, base rates, prior → posterior | 24 | 12, 27 |
| Sampling: population vs sample, sampling error, random/stratified/systematic/convenience, selection and survivorship bias | 18 | 01, 21 |
| Central Limit Theorem (simulation) | 01 | 02, 04, 23 |
| Confidence intervals for a mean, a proportion, and differences of means and proportions | 01 (mean, prop.), 02 (diff. means), 03 (diff. props.) | almost every case |
| Hypothesis testing: H0/H1, α, p-value, test statistic, critical value, Type I/II errors | 01, 02 | everywhere |
| Statistical power, sample size, minimum detectable effect | 04 | 22 |
| One-sample t-test, one-sample proportion test | 01 | 02 |
| Welch/Student t-test, Mann-Whitney U | 02 | 15, 23 |
| Paired t-test, Wilcoxon signed-rank | 15 | — |
| Two-proportion z-test, chi-square test of independence, Fisher's exact test | 03 (z, Fisher), 02 (χ²) | 04, 19, 20 |
| One-way ANOVA, Welch ANOVA, Tukey HSD, effect size η² | 14 | 27 |
| Kruskal-Wallis, Dunn post-hoc | 15 | 14 |
| Choosing between parametric and non-parametric tests (estimand, robustness, n, shape) | 15 | 02, 14, 23 |
| Effect sizes: Cohen's d, Cohen's h, risk difference/ratio, Cramér's V, rank-biserial, η² | 02, 03, 14, 15 | everywhere |
| Pearson and Spearman correlation, non-linearity, outliers creating or destroying correlation | 05 | 06, 08, 09, 21 |
| Correlation ≠ causation; confounding by a third variable; correlation changing within segments | 05, 21 | 08, 20 |
| Simple linear regression: slope, intercept, residuals, R², CI vs prediction interval | 06 | 07 |
| Multiple regression: individual vs conditional relationships | 07 | 08, 09, 10, 27 |
| Confounding, omitted-variable bias, suppression | 08 | 21, 27 |
| Multicollinearity, VIF, unstable coefficients, prediction vs interpretation | 09 | 27 |
| Regression assumptions and diagnostics: residual, Q-Q, scale-location and leverage plots, Cook's distance, robust standard errors | 10 | 06, 07 |
| Feature transformation: log, square root, polynomial, standardisation, normalisation | 10 (log, sqrt, poly), 07 (standardise) | 11, 12 |
| Categorical predictors: dummies, reference category, categorical × numeric interactions | 07 | 11, 27 |
| Logistic regression: probability, odds, log-odds, odds ratios, marginal effects | 11 | 27 |
| Classification metrics: confusion matrix, precision, recall, specificity, F1, ROC-AUC, PR-AUC | 12 | 11, 27 |
| Class imbalance: class weights, resampling, threshold tuning, cost-based decisions | 12 | 27 |
| A/B testing end to end: randomisation, SRM check, treatment effect, CI, practical significance, peeking | 04 | 03, 22 |
| Multiple testing: family-wise error, Bonferroni, Holm, Benjamini-Hochberg FDR | 19 | 14, 27 |
| Simpson's paradox and aggregation bias | 20 | 08 |
| Causality vs association: confounding, reverse causality, selection bias, experiments vs observational data | 21 | 08, 27 |
| Statistical vs practical significance (large n, tiny effect; small n, large uncertain effect) | 22 | 03, 04 |
| Bootstrap CIs (median, difference in medians, ratios, complex statistics) | 23 | 16 |
| Outliers: IQR, z-score, MAD/robust z, domain rules, influential points; error vs fraud vs VIP vs rare event | 16 | 05, 10 |
| Missing data: MCAR/MAR/MNAR, missingness analysis, simple/group imputation, missing indicators | 17 | 27 |
| Time series: trend, seasonality, decomposition, rolling statistics, autocorrelation/ACF, stationarity (ADF), differencing, baseline forecast | 25 | — |
| Time-to-event: censoring, Kaplan-Meier, Poisson arrivals, SLA breach probability | 26 | — |
| Model interpretation and communication: coefficients, CIs, odds ratios, marginal effects, feature importance | 07, 11 | 27 |
| Exploratory vs confirmatory analysis; prediction vs explanation | 05, 12 | 27 |
| ML vs statistical models: when non-linear models are worth it, comparing models with paired tests (corrected resampled t, DeLong, McNemar, bootstrap), calibration, leakage, out-of-time validation | 13 | 27 |
| End-to-end statistical workflow | 27 (capstone) | every case |

## 6. Case-study roadmap

**Importance labels**

| Label | Meaning |
|---|---|
| 🔴 **MUST GO THROUGH** | Core skill used almost every week by working data scientists |
| 🟠 **DEFINITELY SHOULD GO THROUGH** | Very important practical concept; mistakes here are common and costly |
| 🟡 **GOOD TO HAVE** | Valuable tool you will reach for regularly but less often |
| 🟢 **LESS COMMON** | Specialised situations; learn once you have the core |

### 6.1 Summary matrix

| # | Case study | Domain | Difficulty | Importance | Core techniques |
|---|---|---|---|---|---|
| 01 | **Personal-loan portfolio health check** | Lending | Beginner | 🔴 MUST | Descriptive stats, distribution shape, mean vs median, CLT, CIs, one-sample t and proportion tests |
| 02 | **Do higher earners default less?** | Credit risk | Beginner | 🔴 MUST | Probability tables, Welch t-test, Mann-Whitney, χ² test, effect sizes |
| 03 | **Did the email campaign increase conversions?** | Marketing | Beginner | 🔴 MUST | Binomial, two-proportion z-test, CI for difference, Fisher's exact, relative vs absolute lift |
| 04 | **Designing and reading a checkout A/B test** | Product / payments | Intermediate | 🔴 MUST | Power, sample size, MDE, SRM check, peeking, treatment effect CI |
| 05 | **Card utilisation and spending: what correlation can and cannot tell you** | Credit cards | Beginner | 🔴 MUST | Pearson vs Spearman, non-linearity, outliers, third variables, segment reversal |
| 06 | **Predicting loan amount from income** | Lending | Beginner–Intermediate | 🔴 MUST | Simple linear regression, slope/intercept, R², CI vs prediction interval, residuals |
| 07 | **What drives the loan amount a customer requests?** | Lending | Intermediate | 🔴 MUST | Multiple regression, individual vs conditional effects, dummies, interactions, standardisation |
| 08 | **Why did "work experience" stop mattering?** | Lending / HR-style data | Intermediate | 🔴 MUST | Confounding, omitted-variable bias, suppression, a variable hidden by a confounder |
| 09 | **Overlapping risk signals in a credit-limit model** | Credit cards | Intermediate | 🟠 SHOULD | Multicollinearity, correlation matrix, VIF, coefficient instability, prediction vs interpretation |
| 10 | **Modelling insurance claim cost** | Insurance | Intermediate–Advanced | 🟠 SHOULD | Regression assumptions, diagnostics, log/sqrt/polynomial transforms, heteroscedasticity, Cook's distance, robust SE, gamma shape |
| 11 | **Which customers are about to churn?** | Retail banking | Intermediate | 🔴 MUST | Logistic regression, odds, log-odds, odds ratios, marginal effects, thresholds |
| 12 | **Card transaction fraud detection** | Payments / fraud | Advanced | 🔴 MUST | Imbalanced data, confusion matrix, precision/recall, ROC vs PR curves, class weights, resampling, cost-based thresholds |
| 13 | **Is a machine-learning model worth it? Statistics for model selection** | Credit cards / risk | Advanced | 🔴 MUST | Univariate screening (numeric, ordinal, nominal), mutual information vs correlation, non-linearity and interaction tests (LRT), VIF, leakage detection, model ladder (baseline → logistic → spline GLM → gradient boosting), repeated CV, corrected resampled t-test, DeLong, bootstrap, McNemar, calibration, out-of-time stability, value-based decision, scenario lab |
| 14 | **Which acquisition channel brings the most valuable customers?** | Marketing | Intermediate | 🟠 SHOULD | One-way ANOVA, F-statistic, Welch ANOVA, Tukey HSD, η² |
| 15 | **Branch loan processing times and a new workflow** | Operations | Intermediate | 🟠 SHOULD | Kruskal-Wallis, Dunn, paired t vs Wilcoxon signed-rank, choosing parametric vs non-parametric |
| 16 | **Payment processing outliers: error, fraud, VIP or rare event?** | Payments / ops | Intermediate | 🟠 SHOULD | IQR, z-score, MAD, domain rules, robust statistics, four kinds of outlier |
| 17 | **The missing income problem** | Lending | Intermediate | 🟠 SHOULD | MCAR/MAR/MNAR, missingness analysis, imputation strategies and their bias, missing indicators |
| 18 | **Customer satisfaction survey: who did we actually hear from?** | Customer analytics | Beginner–Intermediate | 🟠 SHOULD | Sampling designs, sampling error, selection/non-response/survivorship bias, stratification, weighting |
| 19 | **Testing a campaign across 40 customer segments** | Marketing | Intermediate | 🟠 SHOULD | Multiple comparisons, FWER, Bonferroni, Holm, Benjamini-Hochberg FDR |
| 20 | **Did the new approval policy hurt approval rates?** | Lending | Intermediate | 🟠 SHOULD | Simpson's paradox, aggregation bias, stratified/standardised comparison |
| 21 | **Does cashback reduce churn?** | Customer retention | Intermediate–Advanced | 🔴 MUST | Association vs causation, confounding, reverse causality, selection bias, what an experiment adds, causal language |
| 22 | **Significant but irrelevant; non-significant but promising** | Product / pricing | Intermediate | 🔴 MUST | Statistical vs practical significance, large-n tests, underpowered tests, CI-based decisions |
| 23 | **Credit-limit increase and customer spend: bootstrapping skewed metrics** | Credit cards | Intermediate | 🟡 GOOD | Bootstrap CIs for median, difference in medians, ratio metrics; percentile vs BCa |
| 24 | **A fraud alert fired: how worried should we be?** | Fraud / risk | Intermediate | 🟡 GOOD | Bayes' theorem, base-rate fallacy, prior/likelihood/posterior, Beta-Binomial updating |
| 25 | **Monthly digital-payments volume** | Payments / finance | Intermediate | 🟡 GOOD | Trend, seasonality, decomposition, rolling stats, ACF, ADF stationarity test, differencing, baseline forecasts |
| 26 | **Collections and SLA: time until an event happens** | Collections / operations | Advanced | 🟢 LESS COMMON | Poisson arrivals, exponential waiting times, censoring, Kaplan-Meier, SLA breach probability |
| 27 | **Capstone: what drives loan default, and what should Risk do?** | Credit risk | Advanced | 🔴 MUST | End-to-end workflow: data quality, EDA, tests, logistic regression, confounding, multicollinearity, metrics, recommendation |

### 6.2 Grouped by importance

**🔴 MUST GO THROUGH / MOST COMMON:** 01, 02, 03, 04, 05, 06, 07, 08, 11, 12, 13, 21, 22, 27

**🟠 DEFINITELY SHOULD GO THROUGH:** 09, 10, 14, 15, 16, 17, 18, 19, 20

**🟡 GOOD TO HAVE:** 23, 24, 25

**🟢 LESS COMMON:** 26

### 6.3 Expected learning outcome of each case

| # | After this case you can… |
|---|---|
| 01 | Summarise a portfolio with the right statistics for skewed money data, explain dispersion to a business owner, put a confidence interval on a KPI, and test it against a policy target |
| 02 | Turn "group A is riskier" into a test, choose between t-test, Mann-Whitney and χ², and report effect sizes rather than only p-values |
| 03 | Analyse conversion-rate differences, explain absolute vs relative lift, and know when exact tests are needed |
| 04 | Size an experiment before it starts, catch broken randomisation, avoid peeking, and read the result as a decision |
| 05 | Compute and *distrust* correlations: spot non-linearity, outlier-driven correlation, third variables and segment reversals |
| 06 | Fit and interpret a simple regression, and explain the difference between "average customer" and "one customer" uncertainty |
| 07 | Interpret coefficients "holding other variables constant", use categorical variables and interactions, and explain why a coefficient changes between models |
| 08 | Diagnose why a variable's effect vanishes or appears after controlling for others (confounding vs suppression) |
| 09 | Detect multicollinearity, explain why coefficients become unstable, and decide when it matters (interpretation) and when it doesn't (prediction) |
| 10 | Check regression assumptions with diagnostic plots and fix violations with transformations, robust errors or different models |
| 11 | Build and explain a logistic model in odds-ratio and probability language that a business head understands |
| 12 | Evaluate a classifier on rare events, choose metrics and thresholds from the business cost of errors |
| 13 | Decide with statistical evidence whether an ML model beats a simple model by enough to justify its cost, and know which test result points to which modelling choice (simple, spline/interaction GLM, or non-linear ML) |
| 14 | Compare many groups without inflating error, and say which groups differ and by how much |
| 15 | Choose between parametric and non-parametric tests on purpose (estimand, robustness, n), including paired designs |
| 16 | Detect outliers several ways and, more importantly, decide what each outlier *is* before touching it |
| 17 | Diagnose why data is missing and choose an imputation strategy that doesn't bias the conclusion |
| 18 | Judge whether a sample can answer the question, and correct for known sampling biases |
| 19 | Run many tests responsibly and explain false discoveries to stakeholders who want "winning segments" |
| 20 | Recognise when aggregated numbers reverse at segment level and decide which comparison answers the question |
| 21 | Use precise causal language, identify confounding/reverse causality/selection, and recommend an experiment when needed |
| 22 | Separate "is it real?" from "does it matter?", and communicate an inconclusive result honestly |
| 23 | Get confidence intervals for any statistic via bootstrap, and know its limits |
| 24 | Reason with base rates and update beliefs with evidence |
| 25 | Describe a time series statistically and build an honest baseline forecast |
| 26 | Handle censored durations and estimate time-to-event and SLA breach probabilities |
| 27 | Run a complete, defensible analysis and recommendation on a realistic multi-variable problem |

### 6.4 The "individual vs combined variables" thread

Several cases are designed together to show how a variable's apparent relationship with the target depends on what
else is in the model:

| Scenario | What happens | Case |
|---|---|---|
| **A** | X1 → Y alone, then X1 + X2 + X3 → Y: coefficient changes | 06 → 07 |
| **B** | X1 strongly correlated with Y, becomes insignificant after adding X2 (confounding) | 08 |
| **C** | X1 weak alone, important in a multivariable model (suppression) | 08 |
| **D** | Two individually useful variables create multicollinearity together | 09 |
| **E** | High correlation, wrong causal story | 05, 21 |
| **F** | A variable looks unimportant because the sample contains a confounder | 08, 20 |

## 7. Dependencies between cases

```text
01 Descriptive + CIs ──┬──► 02 Two-group tests ──┬──► 14 ANOVA ──► 15 Non-parametric
                       │                          ├──► 19 Multiple testing
                       │                          └──► 23 Bootstrap
                       ├──► 03 Proportions ──► 04 A/B testing ──► 22 Stat vs practical significance
                       ├──► 16 Outliers      17 Missing data      18 Sampling & bias
                       └──► 05 Correlation ──► 06 Simple regression ──► 07 Multiple regression
                                                                         ├──► 08 Confounding/suppression ──► 20 Simpson ──► 21 Causality
                                                                         ├──► 09 Multicollinearity
                                                                         ├──► 10 Diagnostics & transforms
                                                                         └──► 11 Logistic regression ──► 12 Imbalanced classification ──► 13 Is ML worth it?
02 Probability tables ──► 24 Bayes          01 Distributions ──► 25 Time series, 26 Time-to-event
Everything ──► 27 Capstone
```

## 8. Python libraries

| Library | Used for |
|---|---|
| `numpy`, `pandas` | Data generation and manipulation |
| `scipy.stats` | Distributions, classical tests, bootstrap |
| `statsmodels` | Regression (OLS, logit) with full inference, ANOVA, Tukey, power analysis, proportion tests, time series, survival |
| `scikit-learn` | Classification metrics, cross-validation, class weights (cases 11–12, 27) |
| `matplotlib`, `seaborn` | Figures |
| `python-pptx` | Stakeholder decks |
| `jupyter`, `nbclient` | Running and validating notebooks |

We deliberately avoid specialised libraries when `scipy`/`statsmodels` can do the job clearly, so you can see what
is being computed.

## 9. How to run

```bash
# 1. Create an environment (either way works)
conda env create -f environment.yml && conda activate stats-case-studies
# or
python -m venv .venv && .venv/Scripts/activate        # Windows (use source .venv/bin/activate on macOS/Linux)
pip install -r requirements.txt

# 2. Regenerate a case's data (optional; the CSV is already committed)
python case_studies/01_loan_portfolio_health_check/src/generate_data.py

# 3. Open and run the notebook
jupyter lab case_studies/01_loan_portfolio_health_check/notebooks/01_analysis.ipynb
#    or execute headless (this is how every notebook is validated):
jupyter nbconvert --to notebook --execute --inplace case_studies/01_loan_portfolio_health_check/notebooks/01_analysis.ipynb

# 4. Rebuild the stakeholder deck from the notebook's saved figures and tables
python case_studies/01_loan_portfolio_health_check/src/build_presentation.py
```

All paths are resolved relative to the repository, so these commands work from any working directory.

## 10. How datasets are generated

Each case's data comes from `src/generate_data.py`. The generator:

- uses a **fixed random seed**, so every run produces the same data and the same results;
- documents **why each variable exists, how it is generated, the intended relationships, and the noise**;
- deliberately includes the mess real data has: **skewed distributions, missing values, outliers, data-entry errors,
  duplicates, class imbalance and correlated predictors**, wherever they fit the case;
- writes a CSV to `data/` and a data dictionary to `data/data_dictionary.md`.

> **All datasets in this book are synthetic.** They were generated to reproduce realistic business situations.
> They are not actual customer data. Parameter choices (default rates, income levels, conversion rates and so on)
> are set to plausible orders of magnitude for retail lending, cards and digital products. They are not
> benchmarks for any real institution.

Because you know the true data-generating process, you can check whether a method recovers the truth. That is not
possible with real data, and it is the main teaching benefit of synthetic data here.

## 11. How presentations are generated

Each case has `src/build_presentation.py`. It uses `python-pptx` and the shared styling in
`00_shared_resources/presentation.py` to assemble a deck from the figures and result tables the notebook saved in
`outputs/`. Decks are written for a **business head, not a statistician**. They answer: what did we look at, what did
we find, how sure are we, why does it matter, and what should we do. Run the notebook before rebuilding a deck so the
figures and tables are current.

## 12. Learning path

| Stage | Cases | You move from… → to… |
|---|---|---|
| **1. Foundations** | 01, 02, 03, 05 | "I can compute averages" → "I can summarise, quantify uncertainty and compare groups correctly" |
| **2. Experiments** | 04, 22, 19 | "p < 0.05 means ship it" → "I can design, size and read an experiment as a decision" |
| **3. Modelling relationships** | 06, 07, 08, 09, 10 | "Correlation matrix + regression" → "I understand conditional effects, confounding and diagnostics" |
| **4. Classification and model choice** | 11, 12, 13 | "Accuracy is 98%" → "I choose metrics and thresholds from business cost" |
| **5. Robustness and data problems** | 14, 15, 16, 17, 18, 23 | "Run the default test" → "I pick methods that fit the data and the estimand" |
| **6. Thinking clearly about causes** | 20, 21, 24 | "X drives Y" → "I know what my data can and cannot support" |
| **7. Specialised data** | 25, 26 | Time-dependent and censored data |
| **8. Integration** | 27 + `final_summary/` | Independent end-to-end analyst |

**Fast track (about 2 weeks):** 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 11 → 13 → 21 → 22 → 27.

## 13. The statistical workflow used in every case

```text
Business problem → Define the target → Understand the data → Data quality → EDA → Hypotheses
→ Method selection (with alternatives) → Assumption checks → Analysis → Validation → Interpretation
→ What can / cannot be said → Business recommendation → Limitations → Presentation
```

Rules enforced throughout the book:

- **Question first.** Start from the business question, never from "which test can I run?".
- **No causal language without a causal design.** "X is associated with Y" unless randomisation or a credible
  design supports "X causes Y".
- **A p-value is not the probability that the null is true.** And p > 0.05 does not mean "no effect".
- **Statistical significance ≠ business significance.** Always report effect sizes and confidence intervals.
- **Separate exploration from confirmation**, and prediction from explanation.

## 14. Progress

See [PROGRESS.md](PROGRESS.md). Cases are built strictly one at a time. A case is marked COMPLETE only after its
notebook has executed end-to-end, its outputs and deck have been regenerated, and its content has been reviewed.

## 15. License

Code is released under the MIT License (see [LICENSE](LICENSE)). All data is synthetic.
