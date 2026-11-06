# Review: Book 4 Part 4 (DAX basics), Q1-Q75

Reviewer: Wave C agent C04_Part04. Only Book04_Part04.md and this report were edited. No git commit.

## Counts
- Answers checked: 75 of 75 (headings, numbers, stars and order unchanged; numbering continuous).
- Pandas snippets run (pandas 3.0.5): 55 snippets extracted. First run: 45 OK, 9 failed (not self-contained: Q60, Q62, Q65, Q69, Q71, Q72, Q73, Q74, Q75). After fixes: 55 of 55 run OK.
- Printed outputs and Result lines compared to real runs: all matched, except Q43 (UNION row count) and Q69 (printed lines), fixed below.
- Every DAX result re-derived by hand on the sample data (filter context, totals, blanks); all agree with the Result lines.
- Answers fixed: 24 (Q3, Q6, Q9, Q15, Q17, Q20, Q22, Q26, Q32, Q34, Q36, Q38, Q43, Q45, Q57, Q60, Q62, Q65, Q69, Q71, Q72, Q73, Q74, Q75). Markdown: code fences balanced, tables followed by a blank line.

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| Q3 | Power Query path "Home > Transform data > Add Column" skipped the editor step | Reworded: Transform data opens the Power Query Editor, then Add Column tab; labelled from memory |
| Q6 | Measure named `Employees` clashed with table `Employees`; Common mistakes asserted COUNT on text "gives blank/zero" (unverified) | Renamed to `Headcount`; softened to "surprising result (Q54)" |
| Q9, Q38 | Claimed a Boolean filter "works on one column only", attributed to the CALCULATE page; the sources file does not say this and recent versions allow several columns of one table (from memory) | Replaced with: cannot call a measure; one-column rule is older, newer versions believed to allow same-table multi-column, labelled unverified; removed attribution |
| Q38 | Example said two-column comparison "needs FILTER" | Reframed: FILTER form is safe in every version; measure conditions are the sure case for FILTER; Alternative and Common mistakes aligned |
| Q36 | `||` across columns only via FILTER | Added "plain Boolean `||` may also work in recent versions, unverified" |
| Q15 | DAX referenced `Dept[...]` but sample table is `Dept Summary` | DAX and Alternative now use `'Dept Summary'[...]` |
| Q17 | Measure with no Sample data / Result / Pandas check | Added tiny sample, Result (1000, 800, 1500; mean 1100) and a run snippet |
| Q20 | Measure named `Exits` clashed with table/column `Exits`; no relationship stated | Renamed `Exit Count`; stated Dept-Exits relationship and visual field |
| Q22 | Click path "Home > Transform data > Home > Advanced Editor" confusing | Clarified editor step, labelled from memory |
| Q26 | "Optimise ribbon? Not verified" sloppy; example "~77,000 distinct" not tied to run | Removed the guess, DAX Studio only (unverified); example now matches run (76,632) |
| Q32 | Targets/Sales "by Region" with a West row but no Region table | Stated both tables relate to a Region table |
| Q34 | Say-text had backslash-escaped quotes (invalid DAX if copied) | Removed backslashes |
| Q43 | Pandas "UNION rows" printed 8 on raw columns, but DAX UNION runs after VALUES (7 rows) | Snippet and output now 7; blank-in-DISTINCT labelled unverified |
| Q45 | Path omitted the Power Query Editor step | Added; from memory |
| Q57 | "we saw the Data Model in Book 1 distinct count" unverifiable cross-claim; "Power Pivot > Manage > Measures" menu | Removed claim; path now Power Pivot tab > Measures > New Measure (from memory) |
| Q60, Q62, Q65, Q69, Q71-Q75 | Pandas snippets used undefined variables (could not run) | Made self-contained, ran, printed real output |
| Q69 | Stated output "HR / IT / Multiple" but snippet prints "HR HR / IT IT / Multiple" | Output corrected and explained |
| Q71 | Had Result but no Sample data | Added sample |

## Checks passed (no change needed)
- Template fields: all 75 have Asked at, What the interviewer is checking, Say this, Explain simply, Example, Alternative, Version / licensing note, Edge cases, Likely follow-ups, Common mistakes. Every DAX/M block or click-path carries "not run here"; results say "reproduced with pandas".
- "Asked at" matches research/Book04_Part04_sources.md (Wipro 2023 SUM/SUMX/DATEDIFF/AVG; Deloitte Sept 2025 SUM vs SUMX; Deloitte Glassdoor June 2025 snippet: net sales, unique customers). All others say "commonly asked".
- Recurring claims consistent: DISTINCTCOUNT counts a blank (unverified in Q6, Q11, Q43, Q48, Q62); Desktop Windows-only/free labelled unverified (Q1, Q58); DIVIDE returns BLANK on zero denominator (from Microsoft page per sources file).

## Unresolved / left unverified (nothing could be fetched; learn.microsoft.com unreachable)
- DISTINCTCOUNT blank handling (sources file notes a contradicting community thread). Reasoned from memory only.
- COUNT on a text column (Q6, Q54): behaviour unverified; Q54 says so explicitly.
- Boolean filter multi-column rule (Q9, Q38, Q36), COUNTROWS returning BLANK on empty table (Q27), BLANK compared as 0 in `<` and SWITCH (Q4, Q50), DATEDIFF end-before-start behaviour (Q25).
- All menu names and click-paths, Quick measure limits (Q23), DAX query view and visual calculation GA/preview status and licensing (Q66, Q67), Service web modelling and licence needs (Q58), DirectQuery limits beyond the CALCULATE note (Q68), Excel/Power Pivot edition support (Q57).
- Q4 SWITCH, Q41 ALL/ALLSELECTED, Q43 UNION/DISTINCT, Q69 SELECTEDVALUE: syntax checked by reading only.

## Observations (report only)
- Concept answers (Q1, Q2, Q18, Q21-Q23, Q28, Q45, Q55-Q59, Q61, Q63, Q64, Q66-Q68, Q70) have no Sample data / Result / Pandas check by design; Q56, Q61 style snippets are illustrative.
- Ordering: stars descending (3, 2, 1) and green then yellow within each star; no red in this part. Numbering Q1-Q75 continuous.
- Overlap: Q5/Q14/Q19/Q71 (SUM vs SUMX), Q6/Q27/Q54 (COUNT family), Q9/Q13/Q37 (CALCULATE), Q7/Q12 and Q8/Q12 (contexts), Q33/Q44 (context transition) overlap deliberately and cross-reference each other. Q41 touches ALL (Part 5 owns ALL/ALLEXCEPT); Q43 touches modelling (Part 3); Q22/Q45 touch Power Query (Part 2/3 if present). Boilerplate version notes repeated verbatim in Q39-Q52 are long but accurate.
- Q70's "720 calculations" ignores total rows (approximate).
