# Case Study 04 — Designing and Reading a Checkout A/B Test

| | |
|---|---|
| **Domain** | Product: payments app checkout |
| **Difficulty** | Intermediate |
| **Importance** | 🔴 MUST GO THROUGH |
| **Techniques** | Metric design · unit of randomisation/analysis · α, power, MDE, sample size · power curves · test duration in whole weeks · A/A simulation · peeking and sequential thresholds · sample-ratio mismatch (SRM) and its diagnosis · pre- vs post-treatment subgroup restriction · two-proportion test · CI vs zero and vs MDE · guardrail metrics · novelty effect and winner's curse · business impact |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual
> customer data.

---

## 1. Business problem

The Payments team built a **one-tap checkout** for bill payments. Leadership will only ship if it improves checkout
completion by **at least 1 percentage point**. The PM asks how long the test must run ("a week if possible"), then on
day 3 asks to stop because the dashboard shows "+1.8 points, p = 0.03". At the end, the dashboard flags a **sample
ratio mismatch**.

## 2. Business questions

1. What exactly should we measure, and on whom?
2. How many users and days are needed to detect a 1-point lift?
3. Can we stop on day 3?
4. Can we trust the experiment despite the SRM warning?
5. Did one-tap improve completion, and by at least 1 point?
6. Is it safe to ship to everyone?

## 3. Dataset

| File | Rows | Contents |
|---|---|---|
| `data/historical_baseline.csv` | 28 days | Daily users starting a checkout and completing: used for planning |
| `data/experiment_users.csv` | 66,329 users | `day`, `variant` (random 50/50), `platform`, `app_version` (v5+ / pre-v5), `completed`, `payment_error`, `payment_amount` |

The generator ([`src/generate_data.py`](src/generate_data.py)) documents the true effect (+1.2 pp long-run plus a
decaying novelty boost) and the hidden bug: one-tap crashes before logging for 35% of pre-v5 Android treatment users.
It also documents the outcome-neutral rule used to pick the random stream.

## 4. Statistical questions

| Business question | Statistical question |
|---|---|
| How long? | n per arm for 80% power to detect Δ = 1 pp at α = 5% (two-sided), baseline ≈ 71% |
| Stop on day 3? | False-positive rate of "test daily, stop at first p < 0.05" (A/A simulation) |
| Trust it? | Is the split consistent with 50/50 overall and within segments? |
| Did it work, enough? | Δ = p(T) − p(C) with CI, compared with 0 **and** with the 1 pp MDE |
| Safe? | Guardrail (payment errors), segment effects, effect stability over time |

## 5. Methods (and why)

| Method | Why |
|---|---|
| Power analysis (formula + statsmodels), MDE-by-duration table, power curves | Size the test before launch; show the cost of "one week" |
| A/A simulation with 14 looks; simulation-calibrated Pocock-style threshold | Make the peeking problem measurable, and show a valid alternative |
| SRM exact binomial test, overall and by platform × app version | Detect and localise broken randomisation or logging |
| Restriction to v5+ (a pre-treatment attribute, applied to both arms) | Keeps the comparison randomised once the bug is isolated |
| Two-proportion z-test + Newcombe CI; relative-lift CI | Binary metric, large randomised groups |
| Guardrail test; daily and cumulative lift curves | Safety and novelty/winner's-curse checks |

## 6. Key findings

| Finding | Value |
|---|---|
| Planned sample size | ≈ 32,000 users per arm (≈ 13.2 days) → **run 14 days**. One week gives only 53% power for 1 pp |
| Peeking | Daily look-and-stop → **22%** false positives (vs 5%). A 14-look sequential threshold is p < 0.008 per look |
| SRM | 48.9% treatment overall, p ≈ 10⁻⁸. All of it is in **pre-v5 Android** (38.7% treatment); ≈ 1,270 treatment users crashed out unlogged |
| Pre-v5 harm | Logged pre-v5 treatment users: 3× payment errors (5.9% vs 1.9%). Counting crashes as failures, completion ≈ 36% vs 60.5% |
| **v5+ result** | **70.3% → 71.4%: +1.04 pp (95% CI +0.32 to +1.76), p ≈ 0.005**; relative +1.5% |
| vs 1 pp threshold | CI spans 1 pp: a real gain, but "≥ 1 pp" is **not demonstrated** |
| Guardrail (v5+) | Payment errors −0.10 pp (CI −0.33 to +0.13): no harm |
| Novelty / early stopping | Day-3 cumulative estimate +1.8 pp vs final +1.0 pp (~70% overstated) |
| Value | ≈ ₹17 lakh/year net revenue (≈ ₹5–28 lakh) from v5+ rollout |
| Caution | The invalid naive all-user lift happens to equal the v5+ lift (+1.04 pp). That is luck, not validation |

## 7. Business recommendations

1. **Block one-tap for pre-v5 Android**, fix the crash, re-test; add automated SRM alerts.
2. **Ship to v5+ with a 5% long-term holdout** (recommended), accepting a likely ~1 pp gain, or extend the test 2 weeks
   to settle the 1-point question.
3. Process: pre-register metric/MDE/duration; whole weeks; no stopping on interim p-values.

## 8. Limitations

Two weeks may not show the settled effect · v5+ result only · first checkout only · revenue relies on Finance's
₹10/payment · synthetic data.

## 9. Concepts learned

Experiment design · unit of randomisation vs analysis · primary vs guardrail metrics · pre-registration · α, power,
MDE, sample size · power curves · weekly cycles · A/A tests · peeking / optional stopping · Pocock / O'Brien-Fleming /
mSPRT · SRM · pre- vs post-treatment restriction · CI vs MDE · novelty effect · winner's curse.

## How to reproduce

```bash
python case_studies/04_checkout_ab_test/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/04_checkout_ab_test/notebooks/01_analysis.ipynb
python case_studies/04_checkout_ab_test/src/build_presentation.py
```
