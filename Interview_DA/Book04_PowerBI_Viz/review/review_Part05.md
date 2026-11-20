# Review: Book 4, Part 05 (DAX Advanced), Wave C

Scope: Book04_PowerBI_Viz/Book04_Part05.md, Q1 to Q35 (headings, numbers, stars, order untouched). Nothing could be fetched (learn.microsoft.com unreachable); no DAX engine, so all DAX/M and click-paths are "not run here".

## Counts
- Answers checked: 35.
- Pandas snippets run: 33 check blocks plus 1 shared setup block (new); all 34 run OK on pandas 3.0.5 and their printed output matches the answer text and Result lines (all outputs also re-verified by hand).
- Answers fixed: 15 (Q2, Q12, Q13, Q14, Q18, Q20, Q21, Q23, Q24, Q25, Q27, Q30, Q31, Q33, Q34; Q23 and Q31 label or caveat only), plus one part-level addition (shared pandas setup).
- Template completeness: all 35 have all 9 mandatory fields; measure questions have Sample data / DAX / Alternative / Result / Pandas check. No fields missing after fixes.
- Markdown: code fences balanced, every table followed by a blank line.

## Fixes
| Q | What was wrong | How fixed |
|---|---|---|
| Part header | Q1 to Q18 pandas checks used undefined variables (S, M, E, T, P, m24); not runnable as written | Added one shared "Pandas setup" code block plus a "not run here / reproduced with pandas" statement before Q1 |
| Q2 | "Asked at" said date table is on the Weekday list; sources file does not list it. DAX/Steps line promised pandas values that do not exist | Asked at reworded to what the sources support (YTD/YoY depend on a date table); click-path labelled from memory, not run |
| Q12 | "Boolean filter" used without explanation | Added one plain-language bullet |
| Q13 | Pandas check was prose only ("output matches"), no code or output | Added a runnable snippet with the real results (320/570, 270/840, 300/300, 110/410) |
| Q14 | Second (supposedly correct) measure evaluated [Total Sales] in AVERAGEX outside the 3-month window (CALCULATETABLE affects only the table argument), so it would not average 3 months | Rewrote as `CALCULATE ( AVERAGEX ( VALUES ( Dates[YearMonth] ), [Total Sales] ), Win )`, labelled reasoned/not run, with a caveat about the visual axis column. Results unchanged (re-derived: 100.0, 110.0, 103.3, 120.0, 123.3, 150.0, 153.3, 170.0; 170.0, 150.0, 113.3, 133.3, 140.0, 170.0) |
| Q18 | Top 5 total stated as 1,720 (twice); 500+420+420+380+300 = 2,020 | Corrected to 2,020 in Example and Result; pandas check now prints the sum and actually computes the tie case (was a hard-coded comment) |
| Q20 | Alternative measure used an undefined EndD and no REMOVEFILTERS(Dates), so an active date relationship would cut it to one month, contradicting "same answer" | Added VAR EndD and REMOVEFILTERS(Dates) to both CALCULATEs, labelled not run |
| Q21 | Tenure formulas refer to Employees[JoinDate] with no aggregation, which is invalid as a measure | Stated they must be calculated columns |
| Q23 | Click-path in follow-ups unlabelled | Marked from memory, not run |
| Q24 | Result "FY YTD Jan 100, Feb 220, Mar 310" could mislead (real FY YTD in Jan to Mar includes the earlier April to December); FiscalYear formula not said to be a column | Added caveat to Result; named it a calculated column |
| Q25 | Alternative `RANKX ( ALLSELECTED ( Employees ), [Salary] ... )` ranks across all departments and [Salary] was undefined | Replaced with RANKX over `CALCULATETABLE ( VALUES ( Employees[Name] ), ALLEXCEPT ( Employees, Employees[Dept] ) )` and SUM; labelled reasoned, not run |
| Q27 | Sample data pointed to "as listed in the example" (no table) | Added a real sample table (2023 to 2025 totals, Jan to Mar) |
| Q30 | Said LASTDATE "is blank if no row that day"; LASTDATE returns the calendar date, the measure is what comes back blank | Reworded in Say-this and Explain bullets |
| Q31 | Speed claim stated flatly | Added "often small on recent engines (from memory, unverified)" |
| Q33 | Alternative suggested field parameters for time views (they swap fields, not shift dates) | Replaced with a disconnected slicer table plus SWITCH measures |
| Q34 | Moving-average Result shown as if real MOVINGAVERAGE edge behaviour | Noted the first two values are a partial-window assumption (min_periods=1), real behaviour unverified |

## Unresolved items
- Q14 rewrite and Q25 alternative are reasoned from DAX semantics, not executed; a DAX engine should confirm them.
- Q7 (visual-level filters count as outside filters for ALLSELECTED) is from memory; no label beyond the part-wide "from memory" note was added.
- Premise in Q8/Q29 ("REMOVEFILTERS added later than ALL") remains unverified.

## Claims left unverified (labelled "from memory, unverified" in the answers)
- All version/licensing facts: REMOVEFILTERS release, calculation-group and visual-calculation availability and preview/GA status, Performance analyzer and DAX Studio platform (Windows-only, free), DATEDIFF error when start > end, TODAY() time zone in the Service, USERELATIONSHIP with RLS, CALENDARAUTO fiscal-month argument, menu names (Mark as date table, New calculation, Calculation group, Performance analyzer tab).
- RANKX Skip/Dense and BLANK-as-0, TOTALYTD year_end_date "3/31", EARLIER, ISINSCOPE: from the Wave A sources file only, not re-read.

## Asked-at check
All "Asked at" lines are consistent with research/Book04_Part05_sources.md and research/interview_processes.md (Wipro DATEDIFF, ALL vs ALLEXCEPT, Deloitte USI optimisation, PracHub, Weekday list items); only Q2 needed correction.

## Ordering / numbering (report only)
Stars descending then green, yellow, red within each star: OK. Numbering Q1 to Q35 continuous: OK.

## Overlap with other parts (report only)
Q8 and Q29 overlap lightly with each other and with Q1 (ALL / REMOVEFILTERS / ALLEXCEPT); Q9 and Q4 share YTD. Part 4 already covers filter/row context basics (Q7, Q8, Q12 there), which Q1 to Q12 here build on without repeating. Part 9 Q37 (fiscal-year dashboard) touches Q24. No action taken.
