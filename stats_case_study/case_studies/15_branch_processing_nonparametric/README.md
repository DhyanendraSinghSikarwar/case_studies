# Case Study 15 — Branch Loan Processing Times and a New Workflow

| | |
|---|---|
| **Domain** | Retail lending operations |
| **Difficulty** | Intermediate |
| **Importance** | 🟠 SHOULD GO THROUGH |
| **Techniques** | ANOVA vs Welch vs log-ANOVA vs Kruskal-Wallis · ε² · Dunn's test with Holm correction (hand-built) · probability of superiority · bootstrap CI for a median · paired t vs Wilcoxon signed-rank vs sign test vs sign-flip permutation · Hodges-Lehmann estimate · power simulation under normal / heavy-tailed / outlier data · parametric vs non-parametric decision framework |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual
> customer data.

## 1. Business problem

(A) Do five branches differ in personal-loan processing time? (B) A new digital workflow was piloted with 20 loan
officers; the average change was under half a day and the analyst's paired t-test said "not significant". Should it be
dropped?

## 2. Dataset

`data/branch_processing_times.csv`: 190 loans (30–45 per branch), processing days. `data/workflow_pilot.csv`: 20
officers' average days before and after. Processing times are log-normal with about 6% "stuck" loans (+20–60 days);
one pilot officer was hit by an unrelated system migration (+16 days).
([`src/generate_data.py`](src/generate_data.py))

## 3. Methods

Medians with bootstrap CIs · four omnibus tests on the same data · Dunn's test with Holm correction and probability of
superiority · paired tests and Hodges-Lehmann estimate for the pilot · a simulation of type I error and power for the
three paired tests under three distributions.

## 4. Key findings

| Finding | Value |
|---|---|
| Medians (days) | Andheri 6.0 · Vashi 6.2 · Borivali 7.0 · Thane 7.8 · Panvel 10.4; means 8.1–14.4 (stuck loans) |
| Branch tests | ANOVA p = 0.096 · Welch p = 0.125 · log-ANOVA p = 0.0002 · **Kruskal-Wallis p < 0.001 (ε² = 0.16)** |
| Dunn + Holm | 6 of 10 pairs significant: Panvel and Thane slower than Andheri, Borivali, Vashi (loan slower 68–81% of the time) |
| Pilot | 18 of 20 officers faster; mean change −0.41 days, median −1.10, Hodges-Lehmann −1.10 (95% CI −1.65 to −0.55) |
| Paired tests | t p = 0.65 · permutation (mean) p = 0.86 · **Wilcoxon p = 0.003 · sign test p < 0.001** |
| Without the migration officer | t p = 4×10⁻⁵, Wilcoxon p = 3×10⁻⁴, mean −1.27 days |
| Power (n = 20, shift 0.6 SD) | normal: t 72%, Wilcoxon 70%, sign 53% · heavy tails: 33% / 44% / 42% · 5% outliers: 40% / 59% / 48% |

## 5. Business recommendations

Roll out the workflow after fixing the migration issue · review Panvel and Thane · report median processing time and
the share over 20 days separately · use rank-based tests for small skewed operational samples · stage the roll-out with
a comparison group.

## 6. Limitations

Branch case mix not controlled · pilot without a control group · 20 officers, one month each side · synthetic data.

## 7. Concepts learned

What rank tests do and do not test · same data, opposite verdicts, so choose the test before looking · Dunn + Holm ·
probability of superiority and ε² as effect sizes · paired t vs Wilcoxon vs sign vs permutation · Hodges-Lehmann ·
non-parametric tests can be more powerful than t-tests · matching the test to the estimand (mean vs typical value).

## How to reproduce

```bash
python case_studies/15_branch_processing_nonparametric/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/15_branch_processing_nonparametric/notebooks/01_analysis.ipynb
python case_studies/15_branch_processing_nonparametric/src/build_presentation.py
```
