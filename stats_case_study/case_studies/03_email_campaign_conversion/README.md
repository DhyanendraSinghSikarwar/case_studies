# Case Study 03 — Did the Email Campaign Increase Conversions?

| | |
|---|---|
| **Domain** | Marketing: personal-loan cross-sell campaign |
| **Difficulty** | Beginner |
| **Importance** | 🔴 MUST GO THROUGH |
| **Techniques** | Bernoulli / binomial outcomes · sample-ratio-mismatch and balance checks · two-proportion z-test (pooled vs unpooled SE) · Newcombe CI for a difference · χ² = z² · permutation test · absolute vs relative lift · Cohen's h · CI-vs-break-even decision · self-selection bias (openers) · CACE (preview) · Fisher's exact test · pilot sizing |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual
> customer data.

---

## 1. Business problem

Marketing emailed a pre-approved personal-loan offer to existing customers, with **15% of eligible customers randomly
held out**. The Head of Marketing writes:

> *"Great result! Customers who opened the email converted at almost 4%, nearly three times the rate of those who
> didn't open it. I want to roll this out to the whole base every quarter and double the email budget. Can
> Analytics sign off the result? Also, the Affluent team ran a small pilot where relationship managers phoned
> customers about the offer. It looks even better. Should we scale that too?"*

## 2. Business questions

1. Did the email increase personal-loan conversions, and by how much?
2. Is "openers converted 3× more" a valid measure of the campaign's effect?
3. Is the campaign worth repeating given the uncertainty?
4. Did the RM-call pilot work?

## 3. Dataset

| File | Rows | Contents |
|---|---|---|
| `data/campaign_results.csv` | 80,000 | `group` (email / holdout, random 85/15), `segment`, `tenure_years`, `digital_active`, `email_opened` (blank for holdout by design), `converted` (30-day loan) |
| `data/premium_rm_pilot.csv` | 360 | `arm` (rm_call / no_call, random 50/50), `converted` |

The generator ([`src/generate_data.py`](src/generate_data.py)) documents the hidden mechanism: a latent *engagement*
level drives both email opening and baseline conversion, while the email adds a true uplift of about +0.41 pp. It also
documents how the random stream was chosen (the one whose realised lift is most typical of the design).

## 4. Statistical questions

| Business question | Statistical question |
|---|---|
| Did the email work? | Is p(email) − p(holdout) ≠ 0? What is the CI for the difference and for the ratio? |
| Is the design intact? | Does the observed split match 85/15 (SRM)? Are the groups balanced on pre-campaign variables? |
| Openers claim | Is opening randomly assigned? Do engaged customers convert more without an email? |
| Worth it? | Does the CI for the lift clear the break-even lift? |
| RM pilot | Is there evidence of a difference with single-digit counts? |

## 5. Methods (and why)

| Method | Why |
|---|---|
| SRM binomial test + balance table | Any experiment readout starts by checking the randomisation |
| Two-proportion z-test + Newcombe CI | Binary outcome, two randomised groups, large counts. The CI gives the lift in percentage points |
| Permutation test | Assumption-free confirmation; makes the meaning of a p-value concrete |
| Relative-lift CI, Cohen's h | Communicate the effect both ways; show that textbook effect-size labels are not business thresholds |
| CI vs break-even | Turns the estimate into a decision |
| CACE (ITT ÷ open rate) | Unbiased answer to "what does the email do for readers?" |
| **Fisher's exact test** | Pilot expected counts ≈ 3.5 < 5, so the normal approximation is invalid |

## 6. Key findings

| Finding | Estimate (95% CI) |
|---|---|
| Randomisation | Holdout 15.0% of customers (SRM p ≈ 0.8); groups balanced |
| Conversion | Email 2.23% vs holdout 1.81% |
| **Absolute lift** | **+0.42 pp (≈ +0.14 to +0.67)**; z ≈ 2.9, p ≈ 0.003; permutation test agrees |
| Relative lift | +23% (≈ +7% to +42%) |
| Incremental loans | ≈ 290 (≈ 100 to 460), about 1 per 240 emails |
| Economics | Break-even lift ≈ 0.035 pp; net value ≈ ₹24 lakh (≈ ₹7–39 lakh) |
| Openers vs non-openers | 3.9% vs 1.4%, biased by self-selection. In the holdout, engaged customers convert ~1.5× more with no email |
| Effect among openers (CACE) | ≈ +1.3 pp, about half the naive 2.6 pp gap |
| RM pilot | 6/180 vs 1/180; **Fisher p ≈ 0.12** (the invalid z-test says ≈ 0.06); CI for difference ≈ −0.3 to +6.6 pp |

## 7. Business recommendations

1. **Repeat the campaign**, always with a random holdout. Report the effect as +0.4 pp (+23%), not "3×".
2. **Do not double the budget** on the openers comparison. Test frequency and targeting with holdouts first.
3. **Fix the dashboard**: email vs holdout with a CI.
4. **RM calls**: run a properly sized pilot before scaling.

## 8. Limitations

30-day window (possible pull-forward) · one campaign (fatigue/novelty) · Finance's value and cost assumptions · the
engagement subgroup finding is exploratory · CACE assumes no effect on non-openers · synthetic data.

## 9. Concepts learned

Bernoulli and binomial distributions · randomised holdout · SRM and balance checks · two-proportion z-test · pooled vs
unpooled SE · Newcombe CI · χ² = z² · permutation test · absolute vs relative lift · Cohen's h · CI-based decisions ·
selection bias from self-selected exposure · confounding · intent-to-treat · CACE · Fisher's exact test · small
expected counts · "not significant ≠ no effect".

## How to reproduce

```bash
python case_studies/03_email_campaign_conversion/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/03_email_campaign_conversion/notebooks/01_analysis.ipynb
python case_studies/03_email_campaign_conversion/src/build_presentation.py
```
