# Case Study 05 — What Correlation Can and Cannot Tell You

| | |
|---|---|
| **Domain** | Credit cards: spend growth strategy |
| **Difficulty** | Beginner |
| **Importance** | 🔴 MUST GO THROUGH |
| **Techniques** | Pearson r, Spearman ρ, Kendall τ · Fisher-z CIs and tests · r² · outliers creating/destroying correlation · log transforms · confounding and partial correlation · reverse causality · restriction of range · aggregation reversal (Simpson's paradox for correlations) · non-monotone relationships (binned plots, quadratic LRT, mutual information) · spurious correlation of trending time series · causal language |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual
> customer data.

## 1. Business problem

The Head of Cards proposes, from dashboard correlations: (1) raise every limit by 30% because limit correlates with
spend; (2) cut the app budget because app logins correlate *negatively* with spend; (3) stop age targeting because age
has zero correlation with spend. Marketing adds that marketing spend and card spend correlate at 0.91.

## 2. Business questions

How strong is the limit–spend relationship? Would +30% limits raise spend? Do app users spend less? Is age unrelated to
spend? Does marketing drive spend?

## 3. Dataset

| File | Rows | Contents |
|---|---|---|
| `data/cardholders.csv` | 6,000 | segment, age, income, credit limit, limit-increase flag, spend, utilisation, transactions, ticket size, app logins, tenure. Includes 15 unit errors (paise) and 12 corporate-style cards |
| `data/monthly_marketing_vs_spend.csv` | 36 | Monthly marketing spend and total card spend |
| `data/_answer_key_limit_effect.csv` | 5,973 | **Teaching only**: unobservable desired spend and spend under +30% limits |

The data-generating process is documented in [`src/generate_data.py`](src/generate_data.py). Income drives both limit
and spend; limit increases go to heavy spenders; the limit binds only for a minority (revolvers); age has an inverted-U
effect; logins rise with spend within segments but Mass customers log in most.

## 4. Statistical questions and methods

| Question | Method |
|---|---|
| Strength of limit ↔ spend | Pearson vs Spearman vs Pearson-on-logs; with/without outliers; Fisher-z CI |
| Causal reading? | Partial correlation given income; within-income-decile r; limit-increase profile (reverse causality); restriction of range; headroom bound; answer-key comparison |
| Logins ↔ spend | Pooled vs within-segment Spearman |
| Age ↔ spend | Pearson/Spearman vs binned plot, quadratic LRT, mutual information |
| Marketing ↔ spend | Correlation of levels vs month-on-month changes |

## 5. Key findings

| Finding | Value |
|---|---|
| Limit ~ spend, Pearson | 0.41 (raw, unit errors) → 0.86 (corporate cards in) → 0.73 (retail) |
| Limit ~ spend, Spearman | ≈ 0.70 in every version (robust) |
| Partial r (log limit, log spend \| log income) | 0.23 [0.20, 0.25] vs 0.74 unadjusted. Mostly confounding |
| Reverse causality | Customers given limit increases already spend 2.1× more |
| Restriction of range | r = 0.23 within the ₹40–60k limit band vs 0.73 overall |
| Near-limit customers (≥ 85% utilised) | 4.9% |
| Effect of +30% limits on total spend | Naive "correlation as causation" +27% · headroom upper bound +3.4% · **true (answer key) +1.5%** |
| Logins ~ spend | Pooled ρ = −0.12; within segments +0.35 to +0.58 (reversal) |
| Age ~ spend | r = 0.04 (p = 0.001, r² = 0.2%) but strong inverted U (quadratic LRT p < 0.001; peak ≈ 43) |
| Marketing ~ card spend | Levels r = 0.91; month-on-month changes r = 0.17 (CI −0.17 to 0.48), i.e. spurious |

## 6. Business recommendations

1. No blanket limit increase. Run a randomised limit-increase test on near-limit, low-risk customers.
2. Keep app investment; test app campaigns with holdouts.
3. Keep age/life-stage targeting.
4. Fix the dashboard (unit error, corporate cards separate, scatter plots + robust correlations).
5. Commission a marketing-mix analysis.

## 7. Limitations

Snapshot data · engagement measured only by logins · 36 monthly points · the answer key exists only because the data is
synthetic.

## 8. Concepts learned

Pearson · Spearman · Kendall · r² · Fisher-z CI · significance vs strength · outlier influence · log transform ·
confounding · partial correlation · reverse causality · restriction of range · Simpson's paradox for correlations ·
non-linear relationships · mutual information · spurious time-series correlation · autocorrelation · causal language.

## How to reproduce

```bash
python case_studies/05_correlation_card_spend/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/05_correlation_card_spend/notebooks/01_analysis.ipynb
python case_studies/05_correlation_card_spend/src/build_presentation.py
```
