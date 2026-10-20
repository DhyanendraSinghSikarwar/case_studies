# Case Study 18 — Customer Satisfaction Survey: Who Did We Actually Hear From?

| | |
|---|---|
| **Domain** | Customer analytics: satisfaction (NPS) measurement |
| **Difficulty** | Beginner–Intermediate |
| **Importance** | 🟠 SHOULD GO THROUGH |
| **Techniques** | Sampling frames and designs (simple random, stratified, cluster, voluntary) · coverage, selection, non-response and survivorship bias · representativeness checks · post-stratification, raking and inverse-propensity weights · design effect and effective sample size · non-response follow-up · tipping-point sensitivity · design simulation |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual
> customer data. A teaching-only answer key (`data/answer_key_teaching_only.csv`, with every customer's true score) is
> opened only in the grading section of the notebook.

## 1. Business problem

A one-question email survey ("how likely are you to recommend us, 0–10?") went to all 40,000 active customers and 5.1% answered. The mean is 7.9 and the Head of Retail Banking wants "a record 7.9" in the annual report. Is the number trustworthy?

## 2. Dataset

`data/customer_frame.csv` (40,000 active customers with age band, segment, tenure, app use, products, complaints, city tier, branch), `data/survey_responses.csv` (2,058 responses), `data/followup_sample.csv` (246 reached out of 400 non-respondents drawn at random).

## 3. Methods

Naive CIs · frame-versus-respondent comparison and response rates · post-stratification, raking and response-propensity weights with bootstrap CIs · Kish design effect · random-sample follow-up of non-respondents · tipping-point analysis · grading against the answer key · 1,000-sample simulation of four designs.

## 4. Key findings

| Finding | Value |
|---|---|
| Naive result | mean 7.87 (CI 7.80–7.94), NPS +19 |
| Response rates | 1.8% (aged 21–29) to 11.7% (60+); complaints and non-app users answer less |
| Weighted (raked) | 7.63 (CI 7.55–7.72), NPS +9; effective sample size 1,323 of 2,058 |
| Phone follow-up | 7.28 (n = 246) vs 7.87 for respondents; combined estimate 7.31 (7.10–7.51) |
| Truth | mean 7.07, NPS −13; customers who left scored 5.23, so everyone served this year: 6.83 |
| Bias | naive +0.80 · weighted +0.55 to +0.59 (about 30% removed) · follow-up +0.24; no interval contains the truth |
| Designs (n = 800) | simple random 95% coverage · stratified 96% · cluster 67% (design effect 3.8) · voluntary 0% (bias +0.80) |

## 5. Business recommendations

Do not publish 7.9 or NPS +19; if a number is needed give a range (about 7.3 to 7.6) with the response rate and who it covers · compare years only with the same method · use a stratified random sample with reminder waves and a random non-response follow-up next time · add an exit survey for leavers · monitor response rate by group.

## 6. Limitations

Weights use only variables on the frame; here response also depends on the score itself, which weighting cannot fix · the follow-up reaches 60% of its sample (the reachable non-respondents score 7.28 against 7.03 for all non-respondents) · simulated population and response mechanism.

## 7. Concepts learned

A confidence interval measures sampling error, not bias · more responses do not reduce bias · know who answered by comparing with the frame · weighting trades bias for variance and only corrects what the weighting variables explain · design effect and effective sample size · cluster designs need their own standard errors · a small random follow-up can beat thousands of volunteers · survivorship bias.

## How to reproduce

```bash
python case_studies/18_survey_sampling_bias/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/18_survey_sampling_bias/notebooks/01_analysis.ipynb
python case_studies/18_survey_sampling_bias/src/build_presentation.py
```
