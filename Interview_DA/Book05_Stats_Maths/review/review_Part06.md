# Review: Book 5 Part 6 (Hypothesis testing), Wave C

Reviewer: Wave C. File: Book05_Stats_Maths/Book05_Part06.md (Q1-Q74, continuous, stars descending 3-2-1).

## Counts
- Answers checked: 74 of 74.
- Python snippets run: 60 of 60 ran without error (scratch: C05_06). Pasted outputs and prose numbers compared with fresh runs; all reproduce (seeded) except one rounding slip.
- Answers edited: 12 (Q4, Q9, Q19, Q44, Q50, Q58, Q59, Q60, Q68, Q69, Q71, Q74).
- Independent re-derivations done in Python/by hand: Q3 (two-sided exact p 0.059), Q29/Q30/Q31/Q57 hand formulas, Q39 Holm/Bonferroni adjusted p, Q42/Q45 theory 0.6415, Q56 Fisher, Q60 and Q71 prose figures, Q30 CI and one-sided p.

## Fixes
| Q | What was wrong | Fix |
|---|---|---|
| 19 | Pasted p for n=500 was 0.1141; run gives 0.1142 | Corrected output line |
| 4 | "popularised by R. A. Fisher" stated as fact | Labelled from memory, unverified |
| 9 | Cohen's d used without a plain-words definition | Added one-sentence explanation in Worked example |
| 44 | Dense nested print/call lines | Split into named variables (p and d), same output verified |
| 50 | Multi-assignment on one line | One assignment per line |
| 58 | No output shown for ANOVA table (only prose) | Added the printed table (rerun matches) |
| 59 | No printed output line | Added pasted output with skew and p-values |
| 60 | "scores vary from 34 to 93" ambiguous (that is the before range only) | Clarified |
| 68 | Nested list comprehensions hard for beginners | Replaced with loops and comments; draw order kept, results identical |
| 69 | Gelman and Carlin attribution from memory not flagged | Labelled from memory, unverified |
| 71 | Multi-assignment line; ToolPak df rounding and menu path unverified | One step per line; flagged from memory / not run in Excel here |
| 74 | Comment and example said "before and after" but code compares two separate groups | Reworded to without app / with app |

No statistical misconceptions were found: p-value, CI, Type I/II, one-/two-tailed, df, power, FDR/FWER, Fisher vs chi-square, Welch statements are correct.

## Checked, no change needed
- Template: all 74 answers have Asked at, interviewer check, Say this, Explain simply, Likely follow-ups, Common mistakes; 73 have a labelled Worked example (Q12 carries its numbers inside the numbered steps, which is a full walk-through, so no change).
- Excel formulas (T.TEST, T.INV.2T, T.DIST.2T, CHISQ.TEST, NORM.S.DIST, STANDARDIZE) all carry "not run in Excel here" and a version tag where needed; logic matches Python.
- Claims: Asked-at lines stay within research/Book05_Part06_sources.md (Fractal t vs z title; Tiger Analytics topics via third-party prep sites; Glassdoor snippet, company not stated). No other company named.
- No em dashes in answer text (only the file title line). Code fences balanced (even count). Tables followed by blank line.

## Report-only items
- Ordering/numbering: Q1-Q74 continuous; stars 3 (Q1-Q19), 2 (Q20-Q51), 1 (Q52-Q74), non-increasing. Difficulty tags are not sorted within a star band (accepted by plan).
- Overlap with other parts: Q44/Q50/Q74 (effect size vs large-n significance) and Q9 overlap each other within the part; Q25 and Q64 (CI-test link), Q43 (CLT) overlap Part 5; Q49/Q70 (sample size, MDE) overlap Part 8. Q31/Q33 repeat the "Q57" idea lightly. Not edited.
- Header says Target 70 / Actual 74; fine.

## Unresolved / unverified
- No company-specific interview report was found for any question beyond the sourced Fractal and Tiger mentions; all sources are search-snippet level.
- Excel ToolPak behaviour (df rounding, menu path) is from memory and not run in Excel.
- Fisher "popularised 0.05" and Gelman and Carlin (Type S/M) attributions are from memory.
- Q17 Rs 5 crore bonus and other rupee figures are illustrative, not data.
