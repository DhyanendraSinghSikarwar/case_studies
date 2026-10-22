# Review Part 6 (Book 1, Excel: dynamic arrays) - Wave C

Date 2026-10-22. File: `Book01_Excel/Book01_Part06.md`. Scratch: `C1_Part06` in the session scratchpad.

## Counts
- Answers checked: 45 of 45 (all 7 base fields present in all 45; no code fences; blank line after every table).
- LibreOffice 24.2 re-runs (every runnable block in the part): about 45 formula/array checks (Q9, Q13, Q14, Q17, Q18, Q20, Q21, Q24, Q27, Q30, Q33, Q34, Q36, Q38, Q41, Q42, Q43, Q44, Q45) all matched the printed values. Plus Q9 blank-cell case newly run (#DIV/0!).
- Dynamic-array results (FILTER, UNIQUE, SORT, SORTBY, LET, TAKE, CHOOSECOLS, XMATCH, SEQUENCE, spill): not runnable here; expected values re-derived with pandas (stable sort, groupby, unique). All matched except the Q38 tie order (fixed).
- Answers edited: 22 (42 edits).

## Q27 investigation (EDATE vs DATE returned FALSE)
In-sheet check, 12 months: `=EDATE(DATE(2026,1,1),n)` equals `DATE(2026,n+1,1)` (TRUE, difference 0 for all). The FALSE came from the author's Python: LibreOffice gave the EDATE cells a plain number format, so they came back as serials (46023 ... 46357) while DATE cells came back as datetime; int == datetime is False. Not an Excel problem. Answer now states this; SEQUENCE form of the alternative labelled not run.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| 4 | HSTACK availability claimed with TAKE/CHOOSECOLS | TAKE and CHOOSECOLS confirmed (365, 2024); HSTACK marked unverified |
| 9 | #DIV/0! with blanks only "from memory" | Run in LibreOffice: #DIV/0! |
| 18, 32 | Said Microsoft's LET page gives no speed claim | Page says repeated expression recalculated each time; its example "twice as fast"; text corrected |
| 21 | TEXTJOIN 2019/limit claims | Confirmed from fetched page |
| 25 | Garbled edge-case sentence | Reworded, labelled unverified |
| 26 | XLOOKUP availability "ambiguous" | States the known note vs Applies-to conflict; XMATCH page confirmed 365/2024/2021; XLOOKUP/XMATCH premise note |
| 27 | Unexplained FALSE | Investigated and explained (above); EDATE run |
| 29 | Sample table undefined (pointed to Q32 later in file); Google facts all unverified | Full 10-row table inlined; FILTER/SORT/QUERY facts from fetched Google pages |
| 30 | Result mixed unrelated checks | Added the SUMPRODUCT/SUMIFS 95000 runs; "should no longer be used" quote confirmed |
| 31 | No sample sheet | Added; LET naming rules and 126 pairs confirmed |
| 33 | Sample sheet had 7 rows but formula/results used 10 | Rebuilt 10-row sheet consistent with the re-run TRUE/FALSE list |
| 37 | if_empty text inside CHOOSECOLS would give #VALUE! when nobody matches | Fallback moved outside with IFERROR (reasoned, not run); CHOOSECOLS page confirmed |
| 38 | Result listed Divya before Ravi (tie order contradicted Q35) | Corrected to Ravi, Divya; LARGE-filter output unsorted noted |
| 39 | Sheets claims unverified | QUERY clauses/headers/mixed types confirmed from Google help |
| 40 | SUMIFS claimed to read closed workbooks (wrong, known to fail) | Corrected, labelled from memory; Result line separated |
| 42, 43, 44 | Undefined cells (table, G1, F2/G2) | Defined in text |
| 45 | Cited SORTBY page that the sources file says 404'd | Cites fetched "Spilled range operator" and "SORTBY function" pages |

## Newly verified from fetched pages
Microsoft Support: SORTBY function; XLOOKUP function (note vs Applies-to conflict confirmed); XMATCH function; CHOOSECOLS function; TAKE function; TEXTJOIN function; FILTER function (#CALC! wording, include size, closed-workbook #REF!, no case statement); LET function (naming, 126, performance); Dynamic array formulas vs. legacy CSE array formulas (September 2018, CSE retained); Dynamic array formulas and spilled array behavior (tables, closed workbooks, "should no longer be used"); Spilled range operator; How to correct a #SPILL! error (causes, VLOOKUP @). Google Docs Editors Help: FILTER (#N/A, no if_empty), SORT, QUERY.

## Still unverified (labelled in text)
UNIQUE/SORT case-insensitivity and tie order; blank shown as 0; INDEX with `{1,3}` and `INDEX(s,r,{2,1,3})`; exact Excel 2019 display of FILTER; Power Query in Excel 2016; Sheets UNIQUE/ARRAYFORMULA/LET; HSTACK/VSTACK availability; Data Validation `#` source; chart series with `#` name; SUMIFS on closed workbooks. Google UNIQUE/ARRAYFORMULA/LET help URLs returned 404.

## Unresolved / report only
- The non-breaking list of Q-level overlaps: Q3/Q8 and Q16/Q25/Q45 share the UNIQUE spill example (kept). Order check: stars descending, numbering continuous.
- "Asked at" lines make no company claims (sources file has none).
- Excel-vs-LibreOffice: no pasted LibreOffice value depends on text-number coercion or CHAR(160); the Q27 serial/date display is the only LibreOffice artefact (explained).
