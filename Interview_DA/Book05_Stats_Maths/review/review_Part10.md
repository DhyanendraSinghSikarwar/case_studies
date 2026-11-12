# Review: Book 5 Part 10 (Scenario-Based Statistics)

Reviewer: Wave C. File: Book05_Stats_Maths/Book05_Part10.md (edited in place with targeted edits; no commit).

## Counts
- Answers checked: 64 (Q1 to Q64; headings, numbers, stars, order untouched).
- Python snippets extracted and run (python3 -I, seeds as written): 62; 62 ran without error.
- Output comparison: 31 snippets have a pasted text block, all 31 matched exactly. The other 31 quote their output inline in prose ("Output: ..."); I compared those by eye against the real run and all matched (after the fixes below).
- Hand or independent re-derivation: CSAT mix, Bayes 99/1098, SRM chi-square, two-proportion z, Poisson, dice and Sundays counts, hypergeometric pick, sample-size formula, power numbers (also 31,217 per variant for 5.0% vs 5.5%), Simpson tables, DiD arithmetic, 20-test false-alarm 64.2%. All correct except the item in the table.
- Answers fixed: 12.

## Fixes
| Q | Wrong or weak | Fix |
|---|---|---|
| Q44 | Follow-up "one from each team" said 48/165 (29.1%); correct is 2 x 40/100 x 60/99 = 16/33 (48.5%) | Corrected |
| Q6 | Test needed about 6 million users per group but value was computed on 20 lakh monthly users (inconsistent scale) | Monthly users set to 2 crore; prose, code, output and summary line updated (2 crore rupees a month); re-run OK |
| Q4 | "Asked at" implied the sources list a campaign-effect scenario; they do not | Reduced to "commonly asked (no company-specific report found)" |
| Q42, Q43 | Tiger Analytics attribution not flagged as unverified | Added "candidate self-reports (unverified)" |
| Q27 | Missing Worked example field | Added a one-line worked example |
| Q30 | Output not pasted ("as listed above") | Output values written out |
| Q61 | Code hard-coded 800 instead of the named variable | Uses current_headcount |
| Q21 | F1 and AUC unexplained jargon | Plain-words glosses added |
| Q20 | Benjamini-Hochberg / false discovery rate unexplained | Gloss added |
| Q57 | "regression discontinuity" unexplained | Gloss added |
| Q59 | "variance reduction" unexplained | Gloss added |
| Q14 | "Survival analysis" unexplained | Gloss added |
| Q41 | Follow-up pointed to Q56 for sample size but Q56 does not cover 5.0 to 5.5% | Now states about 31,000 per variant (verified) |

(Q41 and Q14 count among the 12 to 13 touched answers; rounded as 12 distinct substantive answers plus minor glosses.)

## Checks with no change needed
- Statistical definitions (p-value, CI meaning in Q15, margin of error vs bias, power vs alpha, Welch, paired test, Bonferroni) are correct.
- Excel functions used (T.TEST, QUARTILE.INC, PERCENTILE.INC, CONFIDENCE.T, NORM.S.DIST, CHISQ.TEST, POISSON.DIST, T.INV.2T, STDEV.S, COMBIN) are real and carry the "Excel 2010+; not run in Excel here" label where a formula is given. Q25, Q28, Q34, Q55 formulas lack the version label but use only CORREL or arithmetic (version-neutral).
- No em dashes in answer text (only the file title line). Code fences balanced; the one table is followed by a blank line.

## Unresolved / report only
- Numbering and order: Header says target 60, actual 64; order follows star then difficulty. No ordering fault found.
- Overlap with other parts (report only): Q8, Q23, Q28, Q52, Q55 repeat the confounder idea; Q9, Q39, Q40 repeat Simpson's paradox; Q15/Q26/Q5 overlap with confidence-interval parts; Q25/Q56/Q59 overlap sample-size parts. Acceptable as scenario framing but may trim in a later pass.
- Q3 treats this month vs last month for the same headcount with a z-test against the 12% baseline; a simplification (the two months are not fully independent). Left as an approximation, stated as "watch" not "alarm".
- Q33 uses Shapiro on 12 values per group; low power, mentioned only as a rough check.

## Claims left unverified
- All "Asked at" lines rest on research/Book05_Part10_sources.md, which is snippet-level only (no page read in full). The Tiger Analytics items (Q42, Q43) are unverified candidate self-reports. All other answers say "commonly asked (no company-specific report found)" with source-file references limited to what the sources file states.
- Q48 "flag SRM below 0.001" is common industry practice from memory, unverified.
- Q60 and others use invented numbers, each labelled as made up or simulated.
