# Case Study 01 — Personal-Loan Portfolio Health Check

| | |
|---|---|
| **Domain** | Retail lending (unsecured personal loans) |
| **Difficulty** | Beginner |
| **Importance** | 🔴 MUST GO THROUGH |
| **Techniques** | Data-quality checks · descriptive statistics · distribution shape · sampling · Central Limit Theorem · confidence intervals (mean, median, proportion) · one-sample t-test · one-sample proportion / exact binomial test · Type I/II errors · power |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual
> customer data.

---

## 1. Business problem

A mid-sized Indian lender has a personal-loan book of about **60,000 loans** disbursed between January 2024 and
June 2025. After a core-system migration, Internal Audit re-verified a **simple random sample of 2,500 loan files**.
The Chief Risk Officer writes:

> *"The Board Risk Committee meets in three weeks. I need a clean, defensible picture of the personal-loan book:
> what a typical loan looks like, how spread out the book is, whether the average ticket size is in line with
> the ₹3.0 lakh we assumed in the business plan, and, most importantly, whether the 12-month 90+ DPD rate is
> within our 4% risk appetite. Please tell me how confident we can be in each number, because the Board will ask."*

## 2. Business questions

1. Is the audit extract clean enough to report from?
2. What does a typical loan look like?
3. How spread out is the book, and how concentrated is exposure in large loans?
4. Is the average ticket size in line with the ₹3.0 lakh plan?
5. Is the 12-month 90+ DPD rate within the 4% risk appetite?
6. Are DTI policy exceptions (DTI > 65%) within the 1% Board limit?
7. How confident can we be in each number?

## 3. Dataset

| File | Rows | Description |
|---|---|---|
| `data/loan_audit_sample.csv` | 2,506 (2,500 after de-duplication) | The audited extract, **including realistic data-quality problems** |
| `data/_population_answer_key.csv.gz` | 60,000 | The full clean book. **Teaching device only**, used to demonstrate sampling, the CLT and CI coverage, and to validate results. A real analyst would not have it. |

| Variable | Type | Notes |
|---|---|---|
| `loan_id` | ID | |
| `disbursal_month` | Date (YYYY-MM) | Jan-2024 … Jun-2025 |
| `region`, `channel`, `employment_type` | Categorical | Channel: Branch / Digital / DSA (direct selling agent) |
| `customer_age` | Numeric | Policy band 21–60 |
| `monthly_income` | Numeric (₹) | Right-skewed; ~4% missing (mostly self-employed) |
| `credit_score` | Numeric | 300–900; **−1 = no bureau history** (sentinel code) |
| `loan_amount` | Numeric (₹) | **Outcome for Q2–Q4**; ₹50k – ₹15 lakh, right-skewed, round-number heaping |
| `tenure_months` | Discrete | 12–60 |
| `interest_rate` | Numeric (% p.a.) | Approximately normal |
| `emi`, `existing_emi` | Numeric (₹) | Used to verify DTI and interest-rate entries |
| `dti` | Ratio | **Outcome for Q6** (DTI > 0.65 = policy exception) |
| `dpd90_12m` | Binary | **Outcome for Q5**: ever 90+ days past due within 12 months |

Generation logic, intended relationships, noise and injected data problems are documented in
[`src/generate_data.py`](src/generate_data.py).

## 4. Statistical questions

| Business question | Statistical question |
|---|---|
| Typical loan / spread | Centre, dispersion and shape of each distribution |
| Ticket vs plan | Is the population **mean** loan amount μ ≠ ₹300,000? (the plan is about total exposure = N × mean) |
| Risk appetite | Is the population proportion p of 90+ DPD loans **> 4%**? (one-sided, fixed in advance) |
| Policy exceptions | Is the proportion with DTI > 65% below 1%? |
| Confidence | What is the sampling error of each estimate? |

## 5. Methods (and why)

| Method | Why it was chosen | Alternatives considered |
|---|---|---|
| Rule-based data-quality checks, consistency checks (EMI formula, DTI identity) | Business rules identify errors; statistical rules only identify unusual values | Deleting IQR outliers (rejected: the large loans are legitimate) |
| Mean, median, mode, trimmed and geometric mean; SD, IQR, percentiles, CV, skewness, kurtosis | Money data is skewed: the right "centre" depends on the question (totals vs the typical customer) | `df.describe()` alone (rejected: hides shape and robustness) |
| Histograms, log-scale views, Q-Q plots, boxplots, ECDFs | Show the shape the summary statistics hide | Formal normality tests (rejected: reject trivially at n = 2,500) |
| CLT and CI-coverage simulations | Show *why* normal-based inference works for skewed data and what "95%" means | — |
| One-sample **t-test** and t-interval for the mean (+ bootstrap check) | Estimand is the mean; CLT makes it valid at n = 2,500 | Wilcoxon / sign test (rejected: wrong estimand, they target the median/pseudo-median) |
| **Bootstrap** CI for the median | No simple formula for a median's standard error | — |
| **Exact binomial test** (+ z-test for mechanics), **Wilson** CI | Exact for any n; Wilson keeps its coverage for small proportions | Wald interval (shown to under-cover for rare events) |
| Power calculation | Shows how likely a 2,500-loan audit is to detect a given breach | — |

## 6. Key findings

| Metric | Estimate | 95% CI | Benchmark | Conclusion |
|---|---|---|---|---|
| Mean ticket size | ₹3.25 lakh | ₹3.14 – ₹3.35 lakh | Plan ₹3.0 lakh | Above plan; t ≈ 4.5, p < 0.001; ≈ **₹150 crore** extra exposure |
| Median ticket size | ₹2.5 lakh | ₹2.4 – ₹2.5 lakh | — | The typical loan is ~23% smaller than the average loan |
| 12-month 90+ DPD rate | **5.4%** | **4.5% – 6.3%** | Appetite 4% | **Above appetite**; exact one-sided p ≈ 0.0005 |
| DTI policy exceptions | 0.44% | 0.25% – 0.79% | Limit 1% | Within limit |

- **Data quality:** 6 duplicate rows, 5 decimal-keyed interest rates, 4 annual-as-monthly incomes, 3 impossible
  ages and ~5% "−1" credit-score codes were found and fixed or flagged. Left in, the −1 codes alone would have
  lowered the average credit score by about 40 points.
- **Shape:** loan amount and income are right-skewed and heavy-tailed (approximately log-normal). Interest rate is
  approximately normal (15.7% ± 1.6 points). Credit score is left-skewed and truncated by policy.
- **Concentration:** loans ≥ ₹5 lakh are ~16% of loans but ~40% of exposure. The top 10% of loans hold ~30%.
- **Segments (descriptive only):** DSA-sourced loans show ~8.4% 90+ DPD vs ~4.6% for Branch/Digital.
- **Validation:** all four 95% intervals contain the true book values in the answer key.

## 7. Business recommendations

1. Report to the Board that the book is **very likely outside its 4% risk appetite** (5.4%, CI 4.5–6.3%).
2. **Diagnose before acting:** run a driver analysis (channel vs credit score vs DTI) before changing channel
   strategy. The DSA gap is an association, not a proven cause.
3. **Re-base the plan's average ticket** to about ₹3.25 lakh for capital and provisioning.
4. **Improve reporting:** show the median and percentiles alongside the mean, and give every sample-based KPI
   a confidence interval.
5. **Fix the data pipeline** issues before the next system-based report.

## 8. Limitations

- Sample-based estimates; segment estimates are much less precise than book-level ones.
- One delinquency definition (ever 90+ DPD within 12 months); loans under 12 months on book are out of scope.
- Income missing for ~4% (not at random); income statistics cover verified loans only.
- Approved loans only (a selected population); 18 months pooled (no trend analysis).
- All segment differences are associations, not causal effects.

## 9. Concepts learned

Mean · median · mode · trimmed/geometric mean · variance · SD · range · percentiles · quartiles · IQR ·
five-number summary · CV · skewness · kurtosis · normal / log-normal / left-skewed / discrete shapes ·
uniform distribution in random sampling · Q-Q plots · empirical rule · group-wise descriptives · ECDF ·
population vs sample · sampling error · representativeness · Central Limit Theorem · standard error ·
t-distribution · CIs for mean, median (bootstrap) and proportion (Wald / Wilson / exact) · correct CI
interpretation · H₀/H₁ · one- vs two-sided tests · test statistic · critical value · p-value · Type I/II errors
· power · effect size · statistical vs business significance.

## How to reproduce

```bash
python case_studies/01_loan_portfolio_health_check/src/generate_data.py        # regenerate data (optional)
jupyter nbconvert --to notebook --execute --inplace case_studies/01_loan_portfolio_health_check/notebooks/01_analysis.ipynb
python case_studies/01_loan_portfolio_health_check/src/build_presentation.py   # rebuild the deck
```
