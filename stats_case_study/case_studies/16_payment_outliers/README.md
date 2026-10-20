# Case Study 16 — Payment Processing Outliers: Error, Fraud, VIP or Rare Event?

| | |
|---|---|
| **Domain** | Payments processing: transaction monitoring |
| **Difficulty** | Intermediate |
| **Importance** | 🟠 SHOULD GO THROUGH |
| **Techniques** | z-score, IQR, log-scale IQR, MAD / robust z · masking and swamping · segment-aware and customer-relative detection · context risk flags · rule-based triage into four outlier types · detector grading against an answer key · effect of each treatment on the mean, trimmed mean and median (bootstrap CIs) · outliers and correlation · robust location estimators (Huber) |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual
> customer data. A teaching-only answer key (`data/answer_key_teaching_only.csv`) gives each payment's true type; the
> notebook opens it only in Section 13.

## 1. Business problem

The monitoring dashboard flags payments more than 3 standard deviations above the mean. Operations reviews the flags
by hand, finds mostly harmless payments, and keeps missing keying errors and fraud. Finance's average ticket size is
unstable. Which unusual payments are errors, fraud, VIP or rare events, and what should be done with each?

## 2. Dataset

`data/payments.csv`: 20,230 payments (7 merchant segments) with amount, the customer's 90-day average payment, tier,
tenure, new-device / location-mismatch / burst / hour context, entry channel and festival-week flag. In the generator
([`src/generate_data.py`](src/generate_data.py)): 20,000 normal payments, 40 decimal-slip errors (×100, manually keyed),
60 frauds, 50 VIP payments and 80 festival payments.

## 3. Methods

Four detectors on the amount · iterated z-score (masking and swamping) · segment-aware and customer-relative robust z ·
context risk flags · profile of the dashboard queue · ordered triage rules · grading against the key · treatment
comparison (do nothing, delete flags, delete or correct identified errors, winsorise, trimmed mean, median) ·
correlations with and without errors · robust location estimates.

## 4. Key findings

| Finding | Value |
|---|---|
| Amount distribution | skewness 40; mean ÷ median 7.5; max 2,555× the median |
| Detectors on amount | z > 3: 58 · IQR (raw): **2,537** · IQR (log): 16 · MAD (log): 10 |
| Masking and swamping | SD ₹89.5k → ₹10.0k after 5 rounds; later rounds flag 470–583 ordinary payments each |
| Dashboard queue (58) | 21 errors, 14 payments in line with own history (86% Privileged), 23 at 2–10× usual; **60% harmless** |
| Dashboard recall | 52% of errors, **3% of fraud** |
| Customer-relative lens | 100% of errors, 17% of fraud; context flags (3+): 97% of fraud, 0% of errors |
| Combined screen | **100% of errors and fraud** with 130 flags (77% real); no VIP or festival payments |
| Triage rules | errors 40/40 (precision 100%); fraud 58/58 precise, 97% recall; VIP 8/9; festival 5/5 |
| Average ticket (truth ₹13,630) | do nothing **+17.5%** · delete dashboard flags **−3.5%** · winsorise −2.8% · delete or correct identified errors ≈ 0% · median +1.3% · trimmed mean +1.6% |
| Correlation (amount, customer's usual) | Pearson 0.30 with errors → 0.81 without; Spearman 0.93 → 0.94 |
| Robust estimators (log scale) | contamination effect 1.2–1.5% vs +17.5% for the raw mean |

## 5. Business recommendations

Retire the 3-SD rule · screen on the log scale with three lenses · route by type (correct errors, investigate fraud,
whitelist VIP and festival) · add keying controls · audit a random sample of flagged and unflagged payments quarterly.

## 6. Limitations

Rules tuned to a simulated mix · fraud confirmation lags in reality · thresholds are choices · synthetic data.

## 7. Concepts learned

Z-scores are damaged by the outliers they hunt (masking) and swamp on skewed data · log scale + MAD · detection
relative to segment and customer · unusual ≠ wrong: four kinds of outlier and their evidence · delete only what is
wrong · mean vs median depends on the question · robust estimators · outliers create and destroy Pearson correlations.

## How to reproduce

```bash
python case_studies/16_payment_outliers/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/16_payment_outliers/notebooks/01_analysis.ipynb
python case_studies/16_payment_outliers/src/build_presentation.py
```
