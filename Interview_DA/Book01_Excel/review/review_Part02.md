# review_Part02.md - Book 1 Part 02 (Wave C review)

Date: 2026-10-22. Reviewer: Wave C, Part 02 (74 answers, core functions). Scratch scripts: `.../scratchpad/C1_Part02/t1.py` to `t4.py`.

## Counts
- Answers checked: 74 of 74. `ANSWER_PENDING`: 0. Code fences balanced.
- Formula answers rebuilt and re-run with `tools/xl_eval.py` (LibreOffice 24.2): 66. All printed values now match the runs (after the fixes below). Re-run values for Q14/Q30 (TODAY/NOW) were logical checks only.
- Not run here (365-only or other tools), labelled in text: Q12 and Q45 TEXTBEFORE/TEXTAFTER, Q61 UNIQUE, Q66 TEXTSPLIT family, Q67 and Q69 Google Sheets formulas, Q68 TEXT* functions, pivot/Power Query routes.
- Answers edited: 17 content edits plus table spacing in 16 places (Q58 to Q74 mostly).

## Fixes
| Q | Problem | Fix |
|---|---|---|
| 1 | Result "by hand", pointed to Q2 | Ran IF and IFS on the sample; real values |
| 3 | Odd "fetched earlier ... not re-fetched" wording | Reworded |
| 6 | Alternative said ROWS-COUNTBLANK equals COUNTA (gives 5 vs 6) | Corrected with reason; COUNTIF "*" note: Excel text-only (memory) vs LibreOffice 6 |
| 13 | Said TEXTJOIN equals TRIM result; row 3 keeps double space | Corrected |
| 17 | Sample table had no D column for the as-of date | Table rebuilt |
| 25 | Blank-date result is Excel-only; LibreOffice gives 1899/12/30 | Difference stated |
| 27 | "31 calendar days" wrong (end minus start = 30) | Fixed |
| 40 | Excel #REF! was "memory" | Cited fetched VLOOKUP page; LibreOffice #VALUE! noted |
| 42 | Blank-denominator warning had no numbers | HR example 25333 vs 38000 added |
| 43 | MAXIFS version cite not fetched | Fetched, confirmed 2019+ |
| 46 | "MD may differ" with no numbers | EDATE method run: 1, 22, 21 vs MD 1, 22, 20 (row 4 differs) |
| 48 | WORKDAY.INTL labelled #NAME?/not run | It runs: 6-Nov-2026, matches hand count |
| 50 | 255-char claim cite not fetched | Fetched, wording aligned |
| 54 | SUMIF "quietly returns 4" not reproducible on the sample | Replaced with run COUNTIFS mismatch (#VALUE!) |
| 64 | WORKDAY.INTL alternative not run | Run, same date |
| 67, 69 | No Result field | Added "not run here" Result |
| 71 | Version claim | Narrowed to the fetched Applies-to list |
| Q58-Q74 | Tables glued to the label above (may not render) | Blank line inserted before 16 tables |

## Claims newly verified from fetched pages
- Microsoft Support "COUNTIF function": 255-character incorrect-result statement; Applies-to lists 365, 2024, 2021 only; page does not say wildcards are text-only.
- Microsoft Support "VLOOKUP function": #REF! when col_index_num exceeds table columns; Applies-to 2016 to 365.
- Microsoft Support "MAXIFS function": Excel 2019, 2021, 2024, 365.

## Still unverified (left labelled "from memory, unverified")
- Excel behaviour of COUNTIF(range,101) with text-numbers, COUNTIF "*" text-only, 15-digit COUNTIF matching (Q55, Q73, Q6); LibreOffice does not reproduce them.
- Excel #NUM! vs LibreOffice #VALUE! for DATEDIF start after end (Q17); real-Excel DATEDIF "MD" numbers (Q46, Q72).
- 64-level IF nesting, 32,767-character limit, YEARFRAC basis list, IFNA availability (Q11 says 2013, Q41 cites 2016), CHAR(10) on Mac, locale-dependent TEXT codes.
- All Google Sheets facts (Q67, Q69 and "Google Sheets has ..." lines): not fetched this pass.
- The IFS "not in 2016" statement rests on the sources file; XLOOKUP is not used in this part except in Q66/Q39 notes, which already state the Microsoft note vs Applies-to conflict.

## Unresolved / report only
- Asked-at lines: all "commonly asked" or snippet-level Glassdoor mentions, consistent with the sources file; no company-specific claims found.
- Ordering: stars descend; within-star difficulty order is not strictly green-yellow-red in places (left as is). Numbering continuous Q1 to Q74. No duplicate questions; topical overlaps (Q27/Q48/Q64 working days, Q13/Q35 joining text, Q26/Q70 TEXT, Q17/Q46/Q72 DATEDIF) are intentional.
- Thin spots not expanded: Q66 to Q74 lack a Sample sheet or some fields (concept/table answers); Q35 CONCATENATE with a range differs by program (labelled).
- Pasted LibreOffice results that may differ in real Excel are flagged in Q6, Q17, Q25, Q35, Q40, Q55, Q73.
