# Case Study 13 — Is a Machine-Learning Model Worth It?

| | |
|---|---|
| **Domain** | Credit cards: application scoring (credit risk) |
| **Difficulty** | Advanced |
| **Importance** | 🔴 MUST GO THROUGH |
| **Builds on** | 02, 05, 07, 09, 11, 12 (the notebook explains everything it uses, so it can be read on its own) |
| **Techniques** | Column-type-appropriate screening (numeric / ordinal / nominal) · target-leakage detection · structural missingness · out-of-time validation · events per parameter · mutual information vs correlation · Benjamini-Hochberg FDR · likelihood-ratio tests (drop-one, linear vs spline, ordinal trend vs categories, interactions) with Holm correction · VIF · splines in logistic regression · gradient boosting with fair tuning · repeated CV with the corrected resampled t-test · DeLong · bootstrap · McNemar · calibration · PSI · learning curves · value-based model selection · scenario simulation |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual
> customer data.

---

## 1. Business problem

A credit-card issuer approves applications with a logistic-regression scorecard. The ML team proposes replacing it with
a gradient-boosting model: *"AUC 0.93 vs 0.78 for the current scorecard."* The Chief Risk Officer asks for an independent
view:

> *"Is the improvement real? Is it big enough to matter in money? Would it hold up on new customers? Could we get the
> same benefit with a better version of our existing scorecard? Give me a recommendation I can defend: ML, improved
> scorecard, or no change."*

## 2. Business questions

1. Is the data fit for modelling, and is anything unusable at application time?
2. Which characteristics carry real risk information, and which are noise or proxies?
3. Are relationships simple, curved, threshold-like or interacting?
4. How much better does each model predict on **future** applicants?
5. Is any difference statistically real, and is it worth the money?
6. Under what conditions would the answer change?

## 3. Dataset

`data/card_applications.csv`: 40,025 rows (39,985 after cleaning), Jan-2023 to Dec-2024, bad rate 8.0%.

| Type | Columns |
|---|---|
| Numerical | age, monthly_income, bureau_score (blank = no bureau history), credit_utilization, enquiries_6m, months_since_delinquency (blank = never), dti, years_at_employer, num_credit_cards, requested_limit |
| Ordinal | education (4 levels), city_tier (4), income_verification (3) |
| Nominal | occupation (7), residence_type (4), acquisition_channel (5), state (12), marital_status (3) |
| Leakage trap | collections_contact_flag (recorded after account opening) |
| Target | bad_12m (90+ DPD within 12 months) |

The true data-generating process ([`src/generate_data.py`](src/generate_data.py)) includes: a U-shaped utilisation effect, an
enquiries threshold, a log-income effect, a DTI × self-employed interaction, a young-age step, a proxy variable (city tier),
pure noise (marital status), a redundant correlated variable (requested limit), mild 2024 drift, and injected
data-quality problems.

## 4. Statistical questions and methods

| Question | Methods |
|---|---|
| Leakage? | Timing review + single-feature AUC screen (flag > ~0.90) |
| Signal per variable? | Mann-Whitney + univariate AUC (numeric), trend test (ordinal), χ² + Cramér's V (nominal), mutual information; BH-FDR |
| Signal *given* the rest? | Drop-one likelihood-ratio tests in a multivariable logistic model (Holm) |
| Linear or curved? | LRT linear vs spline; AIC; binned log-odds plots |
| Ordinal coding? | LRT trend score vs dummy coding |
| Interactions? | LRT for 5 pre-specified, business-motivated interactions (Holm) |
| Redundancy? | Spearman correlations, VIF |
| Which model predicts best? | Model ladder M0 → M3; 5×3 repeated CV (corrected resampled t-test); out-of-time test (DeLong, bootstrap); McNemar at the operating point; calibration slope; Brier; PR-AUC; PSI; learning curves |
| Worth it? | Policy value at a 15% decline rate, bootstrap CI of value differences vs the ₹45 lakh/yr ML running cost |
| When does ML win? | Scenario lab: linear / strongly non-linear / no-signal / small-data worlds |

## 5. Key findings

| Finding | Evidence |
|---|---|
| **The ML claim relies on leakage** | `collections_contact_flag` alone: AUC 0.91. Leaky GBM on a random split: 0.96; without the flag: 0.77 vs current scorecard 0.77 |
| Low correlation ≠ no signal | Utilisation: Pearson r ≈ 0.04 but high mutual information (U-shape) |
| Proxies and noise identified | city_tier significant alone (q < 0.001) but not conditionally (Holm p ≈ 0.17); marital_status no signal; requested_limit redundant (ρ ≈ 0.88 with income, VIF < 5) |
| Shapes found by tests | Splines needed for utilisation, enquiries and age (Holm p < 0.01); score, log-income and DTI linear; ordinals linear trend; only the DTI × self-employed interaction survives Holm |
| Out-of-time AUC | Current 0.771 · full linear 0.781 · **specified GLM 0.787** · GBM 0.779 |
| Improved scorecard vs current | +0.017 AUC (DeLong p < 0.001); ≈ ₹245 lakh/yr value (CI ≈ −₹23 to +₹455 lakh; P(gain) ≈ 97%); ≈ ₹6 lakh one-off cost |
| GBM vs improved scorecard | AUC −0.009 (DeLong p ≈ 0.001; corrected CV p < 0.001); McNemar: no difference in decisions; value +₹39 lakh/yr (CI ≈ −₹170 to +₹230 lakh); P(gain > ₹45 lakh cost) ≈ 46% |
| Overfitting | GBM in-sample AUC 0.83 vs 0.78 out-of-time; GLM gap ≈ 0 |
| Naive vs corrected CV test | GBM vs full linear: naive p ≈ 0.01 ("significant"), corrected p ≈ 0.22 |
| Stability | All PSIs < 0.03; AUC stable Q3 → Q4 |
| Learning curve | GLM plateaus by ~20k applications; GBM still rising, so revisit with more data |
| Scenario lab | Linear world: GBM significantly worse · strongly non-linear world: GBM +0.17 AUC · no signal: nothing beats the permutation null · small data: logistic better (naive test "significant", corrected not) |

## 6. Decision playbook (summary; full version in the notebook, Section 15)

| If… | Then… |
|---|---|
| A feature has single-feature AUC > ~0.9 or is recorded after the decision | Treat as leakage; remove |
| No predictor survives FDR and the best CV AUC ≈ permutation null | Don't build a model; fix the data or the question |
| \|r\| is small but MI is high / binned log-odds curve | Keep it; spline/bin it (GLM) or use trees |
| Significant alone, not conditionally | Proxy: drop from the explanatory model |
| VIF > 10 / \|ρ\| > 0.8 between predictors | GLM: drop or combine; GBM: fine for prediction, don't over-read importances |
| Ordinal: dummies vs trend LRT not significant | Single ordinal score |
| Linear vs spline LRT significant for a few variables | GLM with splines (still a scorecard) |
| One or two interactions significant | Add them to the GLM |
| Many unknown higher-order interactions suspected | Tree ensembles become attractive |
| GBM − best GLM: CI includes 0 | Keep the simpler model |
| CI excludes 0 but value gain < cost | Keep the simpler model |
| CI excludes 0 and value CI mostly above cost | ML is worth it (subject to explainability and model-risk approval) |
| Naive and corrected CV tests disagree | Trust the corrected test / an OOT test |
| Learning curve of ML still rising | Revisit with more data |
| Events per parameter < 10 | Simple, regularised models only |

## 7. Business recommendations

1. **Reject the ML proposal as submitted.** Its headline result depends on a post-event field.
2. **Deploy the statistically-specified scorecard (M2).** Better on new customers, explainable, ≈ ₹6 lakh one-off.
3. **Run the GBM as a silent challenger** and compare monthly using this methodology. Revisit in 12 months.
4. **Adopt the playbook** as a model-governance standard for future ML proposals.
5. Flag post-decision fields in the data warehouse so leakage cannot recur.

## 8. Limitations

Approved-only outcomes (reject inference) · average loss/profit values · one 6-month OOT window (~800 bads), so value CIs
are wide · modest GBM tuning (8 configurations) · synthetic data whose real-world analogue may contain richer
interactions.

## 9. Concepts learned

See the notebook's concept list: column types and tests, leakage, structural missingness, OOT validation, events per
parameter, MI vs correlation, FDR and Holm, nested LRTs, VIF, splines, fair ML tuning, corrected resampled t-test,
DeLong, bootstrap, McNemar, calibration, PSI, learning curves, value-based selection, model risk, scenario simulation.

## How to reproduce

```bash
python case_studies/13_is_ml_worth_it/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/13_is_ml_worth_it/notebooks/01_analysis.ipynb   # ~15-30 min
python case_studies/13_is_ml_worth_it/src/build_presentation.py
```
