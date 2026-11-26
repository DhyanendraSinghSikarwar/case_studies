# Review Part 12 (Book 9, How to Develop ML/AI Skills), Wave C

**Counts:** 24 answers checked; 5 Python blocks run in the original answers (Q4, Q7, Q14, Q16, plus the Q13 prose figures recomputed) plus 1 new generator block run and verified byte-identical to the scratch data; 8 answers changed (Q4, Q7, Q11, Q12, Q13, Q14, Q15, Q16). No headings, numbers, stars or order changed.

## Fixes
| Q | Wrong or missing | Fix |
|---|---|---|
| Q4 | Output came from a hidden generator that was not in the answer and could not be reproduced (accuracy 0.824, recall 0.321 not reproducible) | Added a short seeded generator ("Data used") that builds employees.csv (share left 0.214, baseline 0.788 match the original). Re-ran on sklearn 1.9.1: model accuracy 0.804, precision 0.70, recall 0.132. Output and prose updated (beats baseline by 1.6 points, catches about 13% of leavers) |
| Q7 | Output drops (0.052/0.046/0.059) not reproducible; prose "similar amount" | Re-ran: 0.011/0.014/0.037; prose now says satisfaction matters most, others small, may be noise |
| Q13 | Overfitting figures (98.5/73.2, 78.4/79.2) not reproducible | Recomputed on the Q4 data: full tree 94.4% train, 67.6% test; 3-level tree 78.4% and 79.6% |
| Q14 | 83.2% to 100% not reproducible | Re-ran: 0.796 to 1.0; prose and output updated |
| Q11 | No zero-to-job-ready roadmap (style_guide Section 7) | Added a 20-week roadmap line in the existing answer |
| Q12 | No practice datasets or mini-project list | Added datasets (labelled from memory, unverified, check link and licence) and four mini-project ideas |
| Q15 | No daily practice plan | Added a one-hour weekday routine |
| Q16 | No explicit self-check tests | Added a five-question self-check set (answers hand-checked: 30/40, 30/50) |

## Verified without change
Q2 (79%), Q5 (precision 75%, recall 60%, accuracy 97% vs 95%), Q9 (25 min, 41.7%), Q1/Q6/Q8/Q11/Q15/Q17/Q18/Q21/Q23/Q24 hour arithmetic (60, 120, 57, 90, 24, 35, 87, 46/72=64% and 2 hours behind, 60, 104=40+40+24). Q16 k-means labels and centres reproduced exactly (labels 0/1 may swap). Code fences balanced (18 after edit); no em dashes in answer text.

## Unresolved / notes
- Q4 onward outputs depend on the generator, not on any real data; the text says so. Other Book 9 parts use their own hidden attrition data, so numbers differ across parts (report only).
- Q18 "Days 61-90 = 5 weeks" is a rounding of 30 days to fit 13 weeks; left as an example.
- Q3, Q4 (Tiger Analytics project questions) and the Q8 resource list rest on snippet-level sources in research/Book09_Part12_sources.md; left labelled unverified.
- Overlap: learning-order and 30/90-day plans may overlap with Book 8 Part 9 and Book 7 Part 9 learning framing (sources file says only framing is shared); report only.

## Claims left unverified
Kaggle Learn, Google ML Crash Course (about 15 hours, TensorFlow, 2018 coverage), StatQuest, IBM HR and Telco churn datasets, UCI/Kaggle datasets, DPDP Act and GDPR mentions, certificate weighting, "SQL in almost every posting", prep-site and Tiger Analytics reports. All labelled from memory or unverified in the text.
