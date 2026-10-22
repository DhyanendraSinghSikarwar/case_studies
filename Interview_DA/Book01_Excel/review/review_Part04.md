# review_Part04.md: Book 1 Part 4 (pivot tables, pivot charts, slicers), Wave C

Date: 2026-10-22. Reviewer: Wave C agent. Scratch: scratchpad/C1_Part04 (v.py, p.py).

## Counts
- Answers checked: 74 of 74 (headings, numbers, stars, order unchanged; 74 `###` headings; 0 `ANSWER_PENDING`).
- Formula results re-executed in LibreOffice 24.2 (xl_eval) and matching the printed Result: 24 groups (Q13 helpers, Q15 COUNTIFS, Q16, Q28 COUNTIFS on a rebuilt 18-row set, Q38, Q39, Q40 x3, Q45 VLOOKUP, Q52, Q54 SUMIFS, Q59, Q60 RANK.EQ, Q61, Q68, Q69 TEXTJOIN array, Q71 INDEX/MATCH, Q72, Q74 DATEDIF/LOOKUP).
- Pivot results (cannot run here) re-derived with pandas or by hand and all match: Q1, 5, 6, 8, 11, 12, 13, 17, 18, 20-22, 25, 27, 29-36, 42, 49, 57, 58, 63, 66, 70, 72. No wrong number found. All are labelled "not run here" for the pivot step.
- Answers edited: 16 (Q7, Q12, Q15, Q28, Q45, Q54, Q60, Q61, Q63, Q64, Q65, Q69, Q70, Q71, Q73, Q74).
- Markdown: no code fences in the part; every table is followed by a blank line (script check).

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q7 | Alt+F5 and refresh-on-open marked unverified | Confirmed by fetched "Refresh PivotTable data"; label updated |
| Q12 | Change Data Source steps unverified | Cited fetched "Change the source data for a PivotTable" |
| Q15 | Dates had no year but COUNTIFS used 2026 | Year stated; COUNTIFS re-run (IT 1/2/1, 8 leavers) |
| Q28 | Result from an unprinted 18-row set | Printed the full grid; COUNTIFS alternative rewritten with ranges and run (matches pivot) |
| Q45 | Alternative VLOOKUP pointed at D2 (wrong cell) | Now A2; re-run on two sheets; #N/A without IFERROR noted |
| Q54 | SUMIFS referenced raw rows never shown | Raw rows listed; formula range fixed (C2:C5), run = 200 |
| Q60 | Example said offers, sheet says sales; tie example (4,4,6) arbitrary | Example fixed; tie run (5,5,3 gives 1,1,3) |
| Q61 | Lookup table E2:F6 not shown | Listed |
| Q63 | Example named Location/Year slicers not in the sample | Changed to Dept/Month |
| Q64 | Thin: no sample, results, edge cases, follow-ups | Rewritten: premise check, GETPIVOTDATA #REF! example, steps, edge cases |
| Q65 | Thin | Added example, sample scenario, steps, edge cases, follow-ups; versions from fetched page |
| Q69 | LibreOffice result needs array entry; not explained | Re-run both ways; stated |
| Q70 | Thin; claimed Sheets has no slicers on pivots (wrong) | Rewritten; corrected from Google "Filter charts and tables with Slicers"; sample, result, steps |
| Q71 | Thin; Data Model claim conflicted with Microsoft compat page | Rewritten with sample, INDEX/MATCH run, conflict stated, unverified items labelled |
| Q73 | Weakest: no example numbers, edge cases | Rewritten: limits table facts, row-limit arithmetic, distinct count 5 vs 8, steps, edge cases |
| Q74 | Group-by-3 alternative gives different bands, undisclosed; thin follow-ups | Difference stated; "ym" run (7 months), TODAY() follow-up |

## Newly verified from fetched pages
- Google Docs Editors Help: "Create & use pivot tables" (steps, auto refresh, calculated fields, suggestions); "Filter charts and tables with Slicers" (slicers filter pivots).
- Microsoft Support: "Refresh PivotTable data" (Alt+F5, Refresh All, external sources, refresh on open, applies 2016-365, Auto Refresh Insiders note); "Change the source data for a PivotTable" (steps, Data Model cannot change source; says nothing on renamed sheets); "Save an Excel workbook for compatibility with earlier versions of Excel" (Check Compatibility path; says Data Model features unsupported in versions like 2019); "Excel specifications and limits" (1,048,576 rows; 1,048,576 unique items per field; 256 value fields; 32-bit Data Model 500-700 MB).

## Still unverified
- Renaming a sheet auto-updates the pivot source; error wording for broken sources (Q64).
- What older Excel shows for XLOOKUP/UNIQUE (Q71); Excel for the web as workaround.
- Data Model row limit "about 2 billion" and Power Query/Power Pivot "millions of rows" are search-result summaries only (fetch of those pages returned 404 or a different page).
- Power Pivot edition availability: unresolved; the fetched "where-is-power-pivot" URL returned an overview page, not the edition list.
- Many "from memory" version and UI statements elsewhere (Q9, Q13, Q16-Q19, Q22, Q25, Q29, Q36, Q40, Q46-Q49, Q53, Q55-Q58). Microsoft "Create a PivotTable" Recommended PivotTables conflict (Q26) kept as stated.
- Google Sheets "Show as" and group-by-date features (not described on the fetched page).

## Unresolved / report-only
- No pivot, slicer, Power Query or chart step could be run here; every UI answer rests on documentation. Excel vs LibreOffice: Q38 DATEVALUE, Q69 array entry, Q74 DATEDIF are flagged in the text.
- Q67 keeps "Sample sheet: not meaningful" (scale question); its pandas timing is illustrative.
- Ordering: star groups are descending; 🟢 to 🔴 order inside groups is not strict (e.g. Q16 after Q15 is fine; Q26-Q29 mix) and was left unchanged. No duplicate questions; topical overlaps (Q38/Q13, Q43/Q47, Q56/Q57, Q30/Q58) are cross-referenced.
- Asked-at lines: all match research/Book01_Part04_sources.md (snippet-level candidate reports, unverified).
- Beginner-clarity: fully read for edited answers; the rest scanned.
