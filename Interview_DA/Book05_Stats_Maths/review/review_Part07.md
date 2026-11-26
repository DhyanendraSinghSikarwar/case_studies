# Review: Book 5 Part 7 (Wave C)

Checked file: `Book05_Stats_Maths/Book05_Part07.md` (54 answers, Q1 to Q54). Scratch: C05_Part07 (run.py extracts and runs every snippet).

## Counts
- Answers checked: 54 of 54. Template fields present in all 54 (Asked at, Interviewer checking, Say this, Explain simply, Worked example, Likely follow-ups, Common mistakes).
- Python snippets run: 41 blocks, all OK after one fix (Q9 previously needed Q10 variables and failed standalone). Every pasted output and every number quoted in prose reproduces (seeds reproduce).
- Independently re-derived: r and R-squared for the 10-employee data (SST 638.1, SSE 32.62), Q33/Q34 by hand (r = 6/sqrt(60) = 0.7746; slope 0.6; intercept 2.2), adjusted R-squared formula (0.783, 0.731), Q22, Q45 (critical n = 44 for r = 0.3, two-sided 5%), Q10 p-values (3.3e-7, 2.1e-5), Q13 R-squared 0.971, Q1/Q8 correlations (0.876 and 0.787 quoted as 0.88 and 0.79).
- Answers edited: 14 (Q1, Q5, Q9, Q17, Q19, Q20, Q30, Q31, Q33, Q35, Q43, Q45, Q50, Q54).

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q1 | r and p used before explained | Added one-line plain definitions with pointers to Q2 and Q11 |
| Q5 | "control for" jargon unexplained | Added a bullet defining controlling for a factor |
| Q9 | Code used `model` and `predictors` from Q10, failed when run alone | Rebuilt the Q10 regression inside the block (same output 0.4, 0.94, 2.72) |
| Q17 | Confusing "Conversely, independence does imply r = 0" | Reworded the one-way rule clearly |
| Q19 | Confounder bullet and worked example contradicted each other (holiday travel vs appraisal season), unsupported claims | Made both say the season is the common driver; stated data are made up |
| Q20 | No Excel/Python field | Added pointer to Q4 and Q10 code |
| Q30 | Worked example looked like real data | Labelled illustrative |
| Q31 | Worked example muddled (what r does not tell you) | Rewrote: same r can pair with very different slopes (Q38) |
| Q33 | Textbook-example claim had no source | Labelled "from memory, unverified" |
| Q35 | Salary range "300 to 900" was wrong (simulated range is about 200 to 995) | Corrected to about 200 to 1,000 |
| Q43 | "Nudging" wording hid that the other parameter was held fixed | Stated what is held fixed (outputs unchanged, checked) |
| Q45 | p-value definition said only "this large" | Reworded to "at least this far from 0, in either direction" |
| Q50 | "headcount-based attrition" was vague | Renamed to attrition percentage |
| Q54 | "100,000 times stronger" understated (ratio about 128,000) | "more than 100,000 times" |

## Checked and left unchanged
- Statistical content: p-value, CI, SE vs SD, adjusted R-squared, VIF, Durbin-Watson, Breusch-Pagan, F equals t squared for one predictor, dummy trap, log interpretation, partial correlation all correct.
- Excel: all formulas labelled "not run in Excel here"; versions stated where needed (FORECAST.LINEAR 2016+, T.DIST.2T 2010+, STANDARDIZE/STDEV.S 2010+). Logic matches the Python results.
- Style: no em dashes in answer text (only the file title line), code fences balanced (154 markers), code readability rules met (descriptive names, comments, plain-words line after output).

## Unresolved / report only
- Ordering: Q7 and Q8 (3 stars) are rated yellow; correct within the star group. No numbering issue found.
- Overlap: Q8, Q5 and Q1 share the same simulated confounder example (intentional cross-references). Q28/Q32/Q40/Q53 overlap on confounders and reverse causation. Q37 and Q48 reuse the same 8-employee data. Q39/Q51 and Q26/Q27 pair on dummies and multicollinearity. Possible overlap with Book 5 Part 9 (outliers) and Part 11 (Excel/Python regression functions) not checked here.
- Q11 code depends on `model` from Q10 (one-line, comment says so); left as is.

## Claims left unverified
- All "Asked at" statements rest on the sources file, which is search-summary level only (Tiger Analytics BA/Glassdoor, Ericsson India DS 2020, Glassdoor statistician page, PracHub Uber prompt, Dataford, Interview Query). None opened in full; no frequency can be inferred. Everything else says "commonly asked (no company-specific report found)".
- Rule-of-thumb thresholds (r bands in Q7, VIF 5 to 10 in Q26) are conventions, labelled as such in the text.
- Q33 "classic textbook example" is from memory.
