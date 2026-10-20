# Case Study 19 — Testing a Campaign Across 40 Customer Segments

| | |
|---|---|
| **Domain** | Marketing: cross-sell SMS campaign |
| **Difficulty** | Intermediate |
| **Importance** | 🟠 SHOULD GO THROUGH |
| **Techniques** | Multiple comparisons · family-wise error rate and false discovery rate · Bonferroni, Šidák, Holm, Benjamini-Hochberg · adjusted p-values and q-values · p-value histogram · all-null simulation · winner's curse and replication across waves · empirical-Bayes shrinkage · minimum detectable effect per segment · tiered decision list |
| **Notebook** | [`notebooks/01_analysis.ipynb`](notebooks/01_analysis.ipynb) |
| **Deck** | [`presentation/case_study_presentation.pptx`](presentation/case_study_presentation.pptx) |

> **This dataset is synthetic** and was generated to reproduce a realistic business scenario. It is not actual
> customer data. A teaching-only answer key (`data/answer_key_teaching_only.csv`, the true uplift of each segment) is
> opened only in the grading section of the notebook.

## 1. Business problem

A randomised SMS cross-sell test ran in 40 segments (8 customer types × 5 regions) over two waves. Marketing circled the segments significant at 5% and wants to focus on them and drop the rest. Does multiple testing matter, and how many winners are real?

## 2. Dataset

`data/campaign_results.csv`: 160 rows (40 segments × 2 waves × 2 arms) with customers and conversions, about 258,000 customers. Treatment and control are equal in size within every segment.

## 3. Methods

40 two-proportion z-tests with CIs · p-value histogram · 5,000-trial simulation of a campaign with no effect · Bonferroni, Holm and Benjamini-Hochberg · wave 1 as discovery and wave 2 as replication · normal-normal empirical-Bayes shrinkage · MDE per segment · grading against the answer key · tiered list.

## 4. Key findings

| Finding | Value |
|---|---|
| Marketing's winners | 7 of 40 at p < 0.05 |
| Overall effect (one pooled test) | +0.22 pp (95% CI +0.04 to +0.40, p = 0.017) |
| Campaign with no effect anywhere | at least one false "winner" in 87% of trials, about 2 on average; Holm and BH keep this near 5% |
| Corrections | Bonferroni 2, Holm 2, BH at 5% 2, BH at 10% 6 |
| Winner's curse | 6 wave-1 winners averaged +2.39 pp, then +0.88 pp in wave 2; only 1 still significant |
| Power | median MDE 1.65 pp at α = 0.05 and 2.4 pp with the Bonferroni α |
| Against the truth (8 real winners) | uncorrected: 5 real, 2 false · Holm/BH 5%: 2 real, 0 false · BH 10%: 4 real, 2 false |
| Size of winners | uncorrected winners estimated at +2.07 pp, truly +1.43; shrinkage cuts RMSE 0.75 → 0.62 |
| Tiers | 2 confirmed · 4 promising · 15 unsupported · 19 negative or zero estimate |

## 5. Business recommendations

Keep the campaign broad (overall effect is positive; nothing justifies dropping 34 segments) · target the 2 confirmed segments and confirm the 4 promising ones in a third wave · budget with shrunken uplifts · pre-register the primary test (overall effect) and the segment family · show BH q-values beside p-values in experiment reports.

## 6. Limitations

Segments overlap in practice, so the exact error rates differ · one simulated dataset (counts such as "2 of 6 false" are noisy; the all-null simulation shows the long-run behaviour) · wave 2 has the same power limits as wave 1 · simple normal prior for shrinkage.

## 7. Concepts learned

Each p-value is right on its own, the circled ones are survivors of a screen · FWER versus FDR and which to pick · Holm always beats Bonferroni · FDR is a long-run average, not a guarantee for one list · selected winners are overstated and fall back on replication · "not significant" in an underpowered segment means no evidence, not no effect · decide the family of tests before looking.

## How to reproduce

```bash
python case_studies/19_multiple_testing_segments/src/generate_data.py
jupyter nbconvert --to notebook --execute --inplace case_studies/19_multiple_testing_segments/notebooks/01_analysis.ipynb
python case_studies/19_multiple_testing_segments/src/build_presentation.py
```
