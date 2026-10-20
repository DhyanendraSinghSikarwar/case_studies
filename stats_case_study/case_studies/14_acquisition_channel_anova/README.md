# Case Study 14 — Which Acquisition Channel Brings the Most Valuable Customers?

| | |
|---|---|
| **Domain** | Marketing: credit-card customer acquisition |
| **Difficulty** | Intermediate |
| **Importance** | 🟠 SHOULD GO THROUGH |
| **Techniques** | Why not many t-tests (false-alarm simulation) · one-way ANOVA and sum-of-squares decomposition · η², ω² · Levene / Brown-Forsythe · Welch ANOVA · Tukey HSD vs Games-Howell (hand-built) · planned contrast · ANOVA as regression · ANCOVA (channel vs customer mix) · net value after acquisition cost with bootstrap CIs |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual
> customer data.

## 1. Business problem

Marketing wants to double the aggregator's budget (highest revenue per customer) and cut social media (lowest). Do the
five channels really differ, which ones, by how much, and is it the channel or the customers it attracts?

## 2. Dataset

`data/new_customers.csv`: 6,000 customers acquired through Branch, Search ads, Social media, Aggregator and Partner
co-brand (sizes 600–1,800): age, monthly income, first-year net revenue. `data/channel_costs.csv`: cost per
acquisition. In the generator ([`src/generate_data.py`](src/generate_data.py)), the aggregator attracts the
highest-income customers but has a negative direct effect and the highest variance.

## 3. Methods

Descriptives and CIs · simulation of 10 t-tests vs one ANOVA under H₀ · classic and Welch ANOVA · assumption checks ·
Tukey HSD and Games-Howell · planned contrast (digital vs offline) · ANCOVA with log income and HC3 SEs · net value
(revenue − CAC) and value per ₹ with bootstrap CIs.

## 4. Key findings

| Finding | Value |
|---|---|
| Mean first-year revenue | Aggregator ₹3,309 · Search ₹3,116 · Branch ₹3,054 · Partner ₹3,046 · Social ₹2,188 |
| False alarms under H₀ | 10 t-tests: 29.5% · one ANOVA: 4.1% |
| ANOVA | F(4, 5995) = 17.6, p < 0.001; Welch F = 21.8, p < 0.001 |
| Effect size | η² = 0.012, ω² = 0.011 |
| Equal variances | rejected (Levene p < 0.001); SD ratio 2.0 (aggregator 5,364 vs partner 2,642) |
| Post-hoc | Social media lower than all others (−₹860 to −₹1,120); no other pair significant; Tukey and Games-Howell agree |
| Planned contrast | digital − offline/partner −₹179, CI −₹369 to +₹12, p = 0.066 |
| ANCOVA vs Branch | Aggregator raw +₹256 → at the same income **−₹659** (p < 0.001); Social −₹866 → −₹227 (p = 0.03); Partner ≈ 0 → **+₹288** (p = 0.02) |
| Net of CAC (per customer) | Partner ₹2,146 · Search ₹1,316 · Social ₹1,088 · Branch ₹854 · Aggregator ₹409 (CI ₹58–770) |
| Value per ₹1 of CAC | Partner 3.38 · Social 1.99 · Search 1.73 · Branch 1.39 · Aggregator 1.14 |

## 5. Business recommendations

Do not double the aggregator · do not cut social media on revenue alone · grow the partner co-brand within capacity ·
test whether high-income customers can be reached more cheaply elsewhere · run a controlled budget-shift test before any
large reallocation.

## 6. Limitations

Observational channel assignment · average, not marginal, returns · first-year value only · synthetic data.

## 7. Concepts learned

Why ANOVA instead of repeated t-tests · F as between/within variance · η²/ω² and why a small η² can still matter ·
Welch ANOVA by default · Tukey vs Games-Howell · planned contrasts need no all-pairs correction · confounding by customer
mix (ANCOVA) · "most valuable" vs "best use of budget" · simultaneous CIs.

## How to reproduce

```bash
python case_studies/14_acquisition_channel_anova/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/14_acquisition_channel_anova/notebooks/01_analysis.ipynb
python case_studies/14_acquisition_channel_anova/src/build_presentation.py
```
