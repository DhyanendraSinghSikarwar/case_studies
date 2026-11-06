# Review: Book 1 Part 05 (Data Cleaning), Wave C

## Counts
- Answers checked: 50 of 50 (headings, numbers, stars, order untouched; no duplicate/ordering problems found in this part).
- Formula results re-executed with tools/xl_eval.py (LibreOffice 24.2): 33 answers (Q2, Q3, Q7, Q10, Q13-Q19, Q20-Q32, Q34-Q37, Q40-Q43, Q46-Q50; Q5, Q6, Q12, Q41 helper formulas) plus Q48 array formula via openpyxl ArrayFormula. All printed results now match the runs (after the fixes below).
- Not executable here, checked by pandas/by hand: Q1, Q8, Q11, Q28 (sort+dedupe), Q39, Q44, Q45, Q49 (counts), Q33 (no Sheets). Labelled "not run here".
- Answers edited: 22 (Q3, Q13, Q14, Q17, Q21, Q22, Q25, Q28, Q33, Q34, Q35, Q38, Q44, Q45, Q47, Q48, Q49, Q50, plus small Result/Version edits in Q47 and Q50).

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q13 | Result said the full recipe gave "Meena Nair" using CHAR(160); in LibreOffice it does not (needs UNICHAR(160)) | Result now states this and that CHAR(160) is Excel's standard recipe (from memory, unverified) |
| Q17 | Said plain VALUE(TRIM()) on the nbsp row returns an error; LibreOffice returned 61000 | Corrected; Excel difference labelled from memory, unverified |
| Q35 | Said VALUE("") gave 0 in LibreOffice; it returned #VALUE! | Corrected; Excel behaviour for "" stated as unconfirmed (MS page only says unrecognised text gives #VALUE!) |
| Q48 | Result "run in LibreOffice" for the TEXTJOIN digits formula was not reproducible as a normal formula | Re-run as an array formula: 45813, 771, 1200454 confirmed; noted; TEXTJOIN version cited from fetched page |
| Q34 | Claimed REPLACE is case-sensitive (it works by position) | Only SUBSTITUTE is case-sensitive; REPLACE-beyond-length behaviour tested (EMPX in LO) |
| Q3 | Wildcard sentence in Edge cases was muddled; 255-character claim unsourced | Rewritten; 255 limit labelled from memory, unverified |
| Q21, Q22 | "UNICODE/UNICHAR Excel 2013+" unqualified | Cited MS UNICODE page (lists 2016 and later); 2013 start unverified |
| Q25 | Flash Fill "from Excel 2013" unqualified | Cited MS Flash Fill page (2016-365, no limitations listed); 2013 unverified |
| Q28 | MAXIFS availability from memory | Confirmed by MS MAXIFS page (Office 2019 / 365; lists 2019 to 365) |
| Q38 | 15-digit precision from memory | Confirmed by "Excel specifications and limits" |
| Q14 | XLOOKUP mentioned without version note | Added the XLOOKUP note/applies-to conflict, treated as 2021/365 |
| Q33 | Wording on Google steps | Clarified: official page 404, only third-party tutorials; still unverified |
| Q44 | No Sample sheet, Result, thin edges/follow-ups | Added 5-row sample, pandas-reproduced result (5 -> 4 -> 3 rows, total 131,500), edge case that PQ Trim keeps inner double spaces (unverified), 3 follow-ups |
| Q45 | No Sample sheet/Result | Added two-file sample, pandas result (6 rows, Days total 100, 1 missing), richer edges/follow-ups |
| Q47 | Thin Example/edges/follow-ups | Expanded; Result labelled to cell order D1:D7 (7, 1, 1, 2, -500, 47000, 1), re-run confirmed |
| Q49 | Thin Example/edges/follow-ups | Expanded (pivot route, count-column caveat); counts 4,2,4,1,4,2,4 re-run and confirmed |
| Q50 | "Sample sheet: small test only", no table | Added table, steps with C2 LEN, Power Query alternative, edges (F9, row limit cited), follow-ups; results re-run (12 and 10 characters) |

## Newly verified from fetched pages
- Microsoft Support "MAXIFS function" (Office 2019 / 365; Applies-to 2019, 2021, 2024, 365).
- "TEXTJOIN function" (same availability).
- "UNICODE function" (Applies-to lists 2016 to 365; 2013 not mentioned).
- "Flash Fill in Excel" (Applies-to 2016 to 365; no limitations; does not state the introduction version).
- "VALUE function" (unrecognised text gives #VALUE!; empty text not covered).
- "Excel specifications and limits" (15-digit precision, 1,048,576 rows; no COUNTIF 255 entry).

## Still unverified
- Google Sheets Remove duplicates (Google Help URL 404; only third-party tutorials), Sheets case handling.
- Excel behaviour of CHAR(160), VALUE("") and VALUE on nbsp text (LibreOffice differs); Power Query Text.Trim keeping inner double spaces.
- Remove Duplicates case-insensitivity, Power Query from Excel 2016 (Q4, Q9, Q10, Q16) and the cited "Power Query data sources in Excel versions" page: it is cited in Q42, Q44, Q45, Q50 but absent from research/Book01_Part05_sources.md, and I could not re-fetch it (fetch quota ran out). Q5 and Q12 Text to Columns details (fixed width, single-character Other box) and COUNTIF 255 characters also unconfirmed.

## Unresolved
- "Asked at" lines citing Analytics Vidhya are consistent with the sources file (fetched summary); Scribd/Skillcure/Atlassian items are snippet-only and none were cited as company claims.
- Sources file says 52 questions were researched vs 50 delivered; harmless.
- Q8 "case-insensitivity from memory" and Q2/Q9 Version notes remain labelled unverified.
