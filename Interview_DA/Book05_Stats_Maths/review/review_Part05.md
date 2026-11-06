# Review: Book 5 Part 5 (Sampling, Bias, CLT, Confidence Intervals)

Reviewer: Wave C. File: Book05_Stats_Maths/Book05_Part05.md

## Counts
- Answers checked: 51 of 51 (Q1-Q51); no ANSWER_PENDING left; code fences balanced (150 markers).
- Python snippets run: 44 blocks, 44 OK, 0 errors. All pasted outputs reproduce exactly (seeds fixed) after edits, except Q5 which gained one new printed line.
- Hand/independent re-derivation: Q1, Q6, Q10-Q12, Q25, Q27-Q29, Q33, Q39, Q44-Q46, Q50, Q51 and the bias arithmetic in Q18-Q21, Q35 all agree with the text.
- Answers with at least one fix: 17 (Q5, Q20, Q22, Q26, Q28, Q29, Q30, Q31, Q32, Q45, Q46, Q48, Q50, Q51, Q11, Q25, plus the `rng`/`_` rename across 11 snippets).

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q5 (and Q8) | Prose quotes raw skewness 2.17 but the code never printed it | Added a print line and quoted its output (2.17 verified) |
| Q22 | Prose said gap "about 15,000" / "15,800"; output gives 56,740 - 41,008 = 15,732 | Changed to "about 15,700" in both places |
| Q32 | Say-this called 30% response a "wide margin of error", contradicting the bullet and code (about 5 points) | Reworded to "fairly small margin from luck alone" |
| Q48 | Log-scale coverage (94%) tests the log mean (geometric mean), not the ordinary mean, so it was presented as a like-for-like fix | Added caveat in worked example and result line |
| Q51 | Say-this said 5 to 10%, bullet said 5%; follow-up said "the correction goes to zero" (it is the corrected SE) | Aligned to 5%; reworded follow-up |
| Q31 | "null hypothesis" used unexplained | Explained as the "no effect" assumption |
| Q45 | p-value used unexplained | Added plain definition |
| Q50 | z and p used unexplained | Added plain meaning |
| Q20 | Called a special case of non-response bias (textbooks treat it as self-selection, a related type) | "closely related to" |
| Q28 | "Wilson or exact intervals" unexplained | Added short gloss |
| Q46 | "over-heard" unclear | "over-represented among respondents" |
| Q11, Q29, Q25 | No Excel equivalent in a Stats answer | Added CONFIDENCE.NORM / proportion formulas (2010+, labelled not run in Excel; logic matches Python: 1.96, 2.576, 0.0476) |
| Q30 | Magic number `/ 10` for sqrt(100) | `np.sqrt(100)` |
| Q26 | `lambda` one-liners | Replaced by two named `def` functions |
| Q22, Q24, Q26, Q30, Q36-Q38, Q43, Q47-Q49 | Cryptic names `rng`, `_`, `hits` (style guide Section 10) | Renamed to `random_generator`, `repeat`, `intervals_that_hit`; outputs re-verified identical |

## Checks with no change needed
- Definitions of CI, p-value usage, SD vs SE, n-1, t vs z, FPC, prediction interval, overlap rule, sample-size formula (1,067.1 -> 1,068; FPC 517; 2% -> 2,401) are correct.
- Question order and numbering: stars then difficulty are in order (Q1-12 three-star, Q13-39 two-star, Q40-51 one-star); no change.
- Em dashes: none in answer text (only the file title line).

## Overlap with other parts (report only)
- Q9 and Q30 both cover CI interpretation and use near-identical simulations; Q6 also states it. Q5, Q8, Q24, Q38 overlap on CLT/sampling distribution simulations. Q13/Q23 (stratified vs cluster) and Q13/Q42 (stratified vs quota) overlap. Q3 and Q36 both show biased-vs-random samples. Likely overlap with Part 6 (hypothesis testing) on Q31 and Q45; not checked against that file.
- Q14, Q15 snippets reuse the `employees` table built in Q13 (stated in a comment); they will not run standalone.

## Unresolved / limits
- Excel formulas not run in Excel (no Excel here); logic checked against Python only.
- Q16, Q40-Q42 have no code (conceptual); left as is.

## Claims left unverified
- Company attributions rest on the sources file only: Q5/Q8 "Dataford lists it as a Wells Fargo DA question" (search snippet, unverified). All other "Asked at" lines say "commonly asked (no company-specific report found)" or cite prep-site snippets; none supported by a first-hand interview report. Q44 poll scenario and all HR numbers are illustrative, not real data.
