# Review: Book 5 Part 3 (Distributions), Wave C

## Counts
- Answers checked: 50 of 50 (Q1-Q50). Python snippets run: 50 of 50 ran OK (python3 -I, seeds reproduce).
- Pasted outputs matching a fresh run: 49 of 50 before edits; the one mismatch (Q22) is fixed.
- Answers with at least one edit: 22 (Q8, Q13, Q16, Q17, Q18-Q19 wording/labels, Q22, Q23, Q25, Q26, Q27, Q29, Q34, Q36, Q37, Q38, Q39, Q41, Q42, Q46, Q47, Q48, Q49, Q50). Heading lines, numbers, stars and order untouched.
- All hand-derivable numbers re-derived independently (Q7, Q12, Q17-Q21, Q23, Q24, Q29-Q33, Q35, Q38, Q40, Q44-Q47, Q49, Q50) and agree.

## Fixes
| Q | What was wrong | Fix |
|---|---|---|
| Q22 | Pasted output "4.9 5.16" and prose "mean 4.9, variance 5.16, ratio 1.05" did not match the code (actual 4.94, 5.04, ratio 1.02) | Output and prose corrected |
| Q50 | "76,444 (over 12,000 times the median)" misleading: median is 1.82, so about 42,000 times | Corrected |
| Q8, Q16, Q36, Q37, Q39, Q41, Q42, Q46, Q47, Q48, Q50, Q38 | Code readability: dense one-line prints, missing comments above steps, short names (`k`, `rng`) | Added comments, split long lines into named steps, renamed `rng` to `random_generator` and `k` to `number_of_sds` (Q36-Q50). Outputs unchanged (re-run diff identical) |
| Q13 | Output line had no plain-words line; "Poisson-binomial" unexplained | Added meaning line; explained the term |
| Q17 | "one step of average" vague for HR reader | Now says one standard deviation (one typical step) |
| Q18, Q19, Q22, Q25, Q26, Q27, Q29, Q34, Q48 | Excel formulas lacked "not run in Excel here" and/or version | Labels and versions added; Q29 now states expected results (2 and 0.5) |
| Q23 | "z-score questions appear in every stats list we found" overclaims the sources file | Reworded to "a standard item in generic stats question lists" |
| Q25 | "Excel has no built-in normality test" stated flatly | Labelled from memory, unverified |

## Checked and left as is
- Asked at lines: all say "commonly asked (no company-specific report found)" and only cite snippet-level sources listed in research/Book05_Part03_sources.md (Tiger Analytics snippet in Q1, DataCamp, Penn State, GeeksforGeeks, Pearson). No invented companies or statistics.
- Statistics: definitions of skew, kurtosis (excess), z, CDF/PDF/PMF, Chebyshev, empirical rule, CLT, continuity correction, Six Sigma 1.5 shift (3.4 per million vs 0.002 unshifted), overdispersion all correct.
- No em dashes in answer text (one remains in the file title, allowed). Code fences balanced (134). Every answer has all required template fields; Formula line present where meaningful.

## Unresolved / report only
- Ordering: stars descend 3 to 2 to 1 and difficulty is mixed within star bands (e.g. Q6-Q8 are 3-star yellow after green); fine, no change.
- Overlap with other parts: z-scores (Q5, Q23, Q29, Q9) overlap each other and likely a descriptive-stats or hypothesis-testing part; skewness/mean vs median (Q3, Q4, Q26, Q27, Q40) overlap heavily; Q16 (CLT) probably duplicates a sampling-distribution part; Q37 (t-distribution) likely overlaps inference parts. Q22 and Q34 overlap (overdispersion).
- Q36 follow-up mentions the log transform and Q8 points to Q26 rather than Q36 for it (cross-reference could be Q36); not changed.

## Claims left unverified
- All "Asked at" attributions rest on search-result snippets only (no page fetched in full per sources file); no company-specific evidence for any question.
- Sturges / Freedman-Diaconis rules (Q42), Six Sigma 1.5 SD convention (Q44), Excel function availability by version: standard knowledge, from memory; no Excel run here.
- Rules of thumb (n x p >= 10 for normal approximation, Poisson approximation thresholds in Q49, n=30 for CLT) are conventional guides and vary by textbook.
