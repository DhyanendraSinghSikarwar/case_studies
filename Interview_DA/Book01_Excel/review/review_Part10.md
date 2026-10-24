# Wave C review: Book 1, Part 10 (scenario/practical tasks)

## Counts
- Answers checked: 60 of 60 (Q1-Q60).
- Formula answers re-executed with tools/xl_eval.py (LibreOffice 24.2): 54 (all except Q2, Q12, Q23, Q31, Q34, Q39 which are concept/UI answers; Q23 pandas-checked by hand, Q40 limit check run, Q29 3-D sum run). All 54 printed Results match the re-run.
- Answers edited: 15 (Q3, Q8, Q14, Q20, Q21, Q22, Q25, Q29, Q42, Q47, Q48, Q49, Q51, Q54, Q60).
- Not run here and labelled so: pivots/slicers (Q23), Power Query (Q29, Q34), XLOOKUP/FILTER/UNIQUE/MAXIFS alternatives (Q28, Q43, Q45, Q47), UI steps (Q12, Q39). Expected values hand-checked.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q22 | Formulas referenced F1/F2/F4-F6 but the sample sheet keeps inputs and results in column E | Formulas and alternatives rewritten to E1, E2, E4-E8; re-run gives 3, 2, 2, 3, 3 |
| Q42 | Example said "seven salaries ... plus one text" but sample has six normal, one outlier, one text | Example corrected (quartiles use 7 numbers) |
| Q21 | Rows E8-E10 were only described ("tenure 29, 2, 18"), sheet not reproducible | Added explicit dates; re-run gives headcount 3/0/3/4, leavers 3/0/2/2 as printed |
| Q3 | Claimed blank exit date makes DATEDIF "run to 1900" | Blank = 0, so DATEDIF gives #NUM! (end before start); LibreOffice gave #VALUE! for start > end, as the answer already says |
| Q8 | IFNA availability "Excel 2013, from memory" | Microsoft "IFNA function" fetched: lists 2016-365, silent on 2013; note that openpyxl needs the _xlfn. prefix to run IFNA in LibreOffice (first run returned #N/A without it) |
| Q14 | IFS version from memory | Confirmed by "IFS function" (Office 2019 or Microsoft 365) |
| Q47 | IFS label; "frozen as {=...}" claim unlabelled | IFS cited; dynamic-array-in-old-Excel claim marked from memory, unverified |
| Q20 | Cohort definition B could judge hires who have not had 12 months | Caveat added to Edge cases (author definition label already present) |
| Q25 | Open-requisitions formula was an incomplete fragment | Full COUNTIFS formula given |
| Q29 | Example total 14 vs 3-D sample total 15 looked contradictory | Example states they are two different samples |
| Q48 | Men:Women column K had no formula | Formula added, results listed (run) |
| Q49 | Row-count and difference cells had no formulas for H2:J2, H4, H5 | Formulas added (run) |
| Q51, Q54, Q60 | Own methods not labelled | Labelled as author's own illustrative/working definition (weighted score, retention milestone rule, annual/12 roll-forward) |

## Own-definition labelling (as requested)
- Q20 first-year attrition (definitions A and B): already labelled "my own working definitions, an inference, not a published standard"; AIHR gives no first-year formula. Kept.
- Q21 per-tenure-band rate: labelled as the author's own method; AIHR gives only departures / average headcount plus suggested bands. Kept.
- Q37 rolling 12-month rate: labelled "my own extension" of AIHR's formula. Kept.
- Q5, Q19, Q22, Q52 use AIHR's average-headcount formula and say so.

## Sample numbers vs example text
All other example-text numbers match the sheets (checked Q1, Q4-Q7, Q9-Q11, Q13, Q15-Q19, Q23-Q27, Q32-Q38, Q43-Q46, Q50-Q53, Q55-Q60). Q17 text "up 0.9 points" matches (0.85 rounds to 0.9 in LibreOffice; Excel TEXT rounding of 0.85 may print 0.9 too, not verified in Excel).

## Newly verified from fetched pages
- Microsoft Support "IFS function" (Excel 2019 and later, availability note).
- Microsoft Support "IFNA function" (Applies-to list 2016-365).

## Still unverified (left labelled "from memory, unverified" or "search summary")
- Excel for the web "Manage Protection" wording (Q12); hidden-formula option; Power Query built into 2016 (Q7, Q29, Q34, Q49, Q56).
- Table auto-expansion (Q7); Sheets features (Q1, Q46 and others); Microsoft performance-page claims (Q31); RANK.EQ 2010, ISFORMULA/FORMULATEXT 2013, Inquire add-in (Q16, Q51, Q58); MEDIAN(IF) array behaviour by version (Q18); consolidate/VSTACK availability (Q29); the Q40 32-bit Data Model figure relies on the earlier fetch, not re-fetched.
- Excel-vs-LibreOffice: TIMEVALUE parsing (Q56), text-number coercion (Q10), DATEDIF error code (Q3) are flagged in the answers; Excel behaviour not tested here. XLOOKUP conflict handled consistently in Q43/Q47 (treated as 2021/365).

## Unresolved / report only
- Asked-at lines are all "commonly asked" or snippet-based per the sources file; no change needed. Novartis claim (Q38) matches research/interview_processes.md.
- Several sample sheets compress rows ("2-5 | E1-E4") for space (Q18, Q26, Q36, Q37); not reproducible cell by cell but values were rebuilt and match.
- Ordering/numbering: no problems seen. Code fences: none in file; tables followed by blank lines.
