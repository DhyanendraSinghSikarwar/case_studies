# Review: Book 5 Part 9 (Outliers, Simpson's Paradox, Misleading Stats)

## Counts
- Answers checked: 41 of 41.
- Python snippets run: 38 (Q1, Q25, Q27 have none by design). All 38 run without error under `python3 -I` and reproduce the pasted numbers. 3 outputs differed only in whitespace/format (Q3, Q36, Q41) and were corrected.
- Answers fixed: 11 (Q2, Q3, Q15, Q20, Q17, Q21, Q23, Q33, Q36, Q38, Q41).
- Every worked number in prose (means, medians, fences, z-scores, Simpson tables, Wilson intervals, rates, Cook's D, Mahalanobis) was re-derived or matched to executed output.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q3 | Pasted output `25.0` but code prints `25.00` | Output corrected |
| Q2 | "standard deviations" used before explained | One-line definition added |
| Q15 | Prose and comment called Q2-24 (9.5) the "worst quarter" and Q4-25 "the best"; worst is actually Q2-25 (10.4) | Reworded to "a high quarter" and "the lowest of all" |
| Q20 | "a one-third drop" wrong: 3,936 to 2,936 is a 25% drop | Reworded: the one day is about a quarter of the month |
| Q17 | Winsorizing percentage guidance unsourced | Labelled rule of thumb, from memory, unverified |
| Q21 | Wald aeroplane story unlabelled | Labelled from memory, unverified |
| Q23 | CI described as range that "likely contains" true rate (loose) | "range of plausible values for the true rate" |
| Q33 | p-value definition omitted "or stronger" | Added "or stronger", "alone" |
| Q36 | Pasted pandas table header spacing did not match real output | Output replaced with real output |
| Q38 | Implied IQR is immune to masking | Added breakdown caveat (about a quarter of data extreme) and a common-mistake line |
| Q41 | pandas truncated columns with `...`; pasted output did not match | Code now prints `to_string()`; output alignment fixed |

## Checked and left unchanged
- Q6 masking numbers (z 1.65/1.74/1.86; IQR flags 95, 98, 102) confirmed. Q30 month-to-month correlation 0.48 confirmed. Q5 "1.5 x IQR flags about 0.7% of a normal" confirmed.
- Excel formulas (QUARTILE.INC, STANDARDIZE, STDEV.S, SUMPRODUCT, LN/EXP, box and whisker chart 2016+) are labelled not run in Excel; logic matches Python.
- No em dashes in answer text (only the file title line). Code fences balanced (152). All 41 answers have all 7 template parts. Q25 reuses Q24's code by design.

## Ordering / overlap (report only)
- Numbering Q1 to Q41 is sequential; stars descend 3, 2, 1 as planned. Header says target 40, actual 41 (fine).
- Overlap with other parts: Q4, Q26, Q28 (mean vs median, skew) likely overlap Book 5 descriptive-statistics part; Q22 (base rate/Bayes), Q23 (Wilson CI) and Q34 (multiple testing) overlap hypothesis-testing/probability parts; Q37 (leverage/Cook's D) overlaps the regression part. Q6, Q18, Q38 overlap each other (z-score masking) by design.

## Unresolved / unverified
- "Asked at" lines are all "commonly asked (no company-specific report found)" with Glassdoor/InterviewKickstart/Dataford/PracHub/Interview Query cited at snippet level per `research/Book05_Part09_sources.md`; none verified by full-page fetch.
- From memory, unverified: Iglewicz and Hoaglin 3.5 cut-off and 0.6745 constant, Tukey 1.5 rule attribution, Anscombe 1973 and Datasaurus mention, Campbell's law, hat-value 2 to 3 times rule, Wald story, winsorizing percentages.
- Q11 matplotlib box plot not run (matplotlib not installed).
