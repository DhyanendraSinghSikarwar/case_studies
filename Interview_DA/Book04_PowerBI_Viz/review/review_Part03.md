# Review: Book 4, Part 03 (Data modelling: star schema, relationships, cardinality)

File reviewed and edited in place: Book04_PowerBI_Viz/Book04_Part03.md (60 answers, Q1 to Q60). Reviewer: Wave C. No git commit made. Scratch: .../scratchpad/C04_Part03.

## Counts
- Answers checked: 60 of 60.
- Pandas snippets: 43 answers carry a Pandas check (the other 17 are concept or click-path answers where a calculation is not meaningful). All 43 now run standalone on pandas 3.0.5 (exit code 0) and the printed output in the file equals the real output (checked by script).
- Before my edits only 17 of the 43 ran. Q21 and Q25 to Q60 (26 snippets) were fragments that used undefined variables and quoted "Printed" values by hand.
- Answers fixed: 40 (31 snippets rewritten to be self-contained with real output, plus 9 other text/DAX fixes; some overlap).
- Result lines re-derived by hand against the sample data (Q3, Q12, Q16, Q20, Q26, Q28, Q34, Q40, Q41, Q55, Q57, Q58): all correct.

## Fixes
| Q | What was wrong | Fix |
|---|---|---|
| Q11 | Pandas never printed the `Depts With Absence` result claimed | Added the line; real output pasted |
| Q21 | Snippet printed pandas StringArray (not the quoted list); bad-pair "2" was only claimed; ties follow-up said "No, duplicates not allowed" (unverified); key-column claim unverified; Learn page not in fetched list | Snippet rewritten (prints lists, valid 1, bad pair 2); follow-up and edge case reworded or removed; version note labelled "from memory, unverified" |
| Q24 | No Result field | Added a pointer to Q26 (pandas-reproduced); "Power BI refuses or flags ambiguity" corrected to "second one is created inactive" |
| Q25, Q26, Q28 to Q35, Q40, Q41 | Pandas check was a fragment with undefined data; "Printed" values typed by hand | Self-contained snippets with the sample data and real printed output |
| Q33 | Sample data showed only the flattened output; inputs missing | Added the three input tables in the sample data |
| Q34 | Sample uses a Month text column while the DAX/relationships use a date | Added a note (month shown as yyyy-mm; model uses first-of-month date) |
| Q44 to Q50, Q54 to Q60 | Same fragment problem | Rewritten self-contained; real output |
| Q45 | Edge case said DISTINCTCOUNT blank handling is vague "in some versions" (contradicts Q1); measure named "Open Requisitions" for a distinct count | Edge case aligned with Q1 (blank counts as one value; DISTINCTCOUNTNOBLANK skips it, labelled from memory); measure renamed `Requisitions` |
| Q47 | `Not Enrolled` DAX ignored the course (returned a different number than the pandas E4, E5); alternative used a two-table boolean filter that is not valid CALCULATE shorthand | Measure rewritten as `Not Enrolled in POSH` with EXCEPT + CALCULATETABLE (result 2); alternative rewritten with FILTER; Result and Edge cases updated |
| Q49 | Text size claimed 64 MB; real pandas output is 63,000,000 bytes; no Sample data field | Changed to 63 MB; added Sample data |
| Q50 | Sample data mixed two tables; M referenced `Dept[Dept]` (no such query) | Split into `Cost` and `Department` tables; M now uses `Department[Dept]` |
| Q51 | No Result field | Added pointer to Q25/Q26 |
| Q14 | Claimed Microsoft says Power Query cannot create SCD Type 2 (not supported by a fetched page) | Reworded and labelled "from memory, unverified"; points to Q55 |
| Q17, Q18 | "75 tables warning" and Modeling-tab menu path presented as from fetched pages; inconsistent with Q4/Q17 (Home) | Labelled from memory, unverified; ribbon tab names flagged as build-dependent |
| Q22 | Claims about star-schema page and live connections not backed by fetched pages | Labelled from memory, unverified |
| Q30 | Case-sensitivity claim unlabelled | Labelled from memory, unverified |
| Q43 | "Boot Camp-style setups" (not available on Apple silicon) | Replaced by "virtualisation software such as Parallels" |

## Checks with no change needed
- Template: all 60 answers have Asked at, Interviewer checking, Say this, Explain simply, Example, Version/licensing, Edge cases, Follow-ups, Common mistakes. Measure/modelling answers have Sample data, DAX/Steps, Alternative, Result, Pandas check. Concept answers (Q2, Q9, Q17, Q18, Q22, Q23, Q24, Q36 to Q39, Q42, Q43, Q51 to Q53) legitimately omit calculation fields.
- Every DAX/M snippet and click-path is labelled "not run here"; results say "reproduced with pandas".
- DAX/M read-through (not run): syntax of USERELATIONSHIP, CROSSFILTER, TREATAS, RELATED/RELATEDTABLE, PATH/PATHITEM/LOOKUPVALUE, EXCEPT, ISFILTERED, SELECTEDVALUE, Table.NestedJoin, Table.TransformColumns/Distinct, DateTime.Date looks correct.
- Markdown: code fences balanced; every table is followed by a blank line.
- Order/numbering: stars descending and green to red within each star; numbering Q1 to Q60 continuous. Not changed.
- Headings, numbers, stars and order untouched. "Asked at" lines checked against research/Book04_Part03_sources.md and research/interview_processes.md (Deloitte Hyderabad optimisation, Flipkart/Amazon BIE star schema, Weekday list): supported; Deloitte-tagged Scribd flagged as unverified in-text.

## Unresolved / left unverified
- No Microsoft Learn page could be re-fetched. Citations to DAX function pages (DISTINCTCOUNT, COUNTROWS, SUM, CALCULATE, CALENDARAUTO, ISFILTERED, RELATED, RELATEDTABLE, USERELATIONSHIP, CROSSFILTER, TREATAS) and to Optimization guide, Data reduction, Bi-directional guidance, Auto date/time, Sort by column and Data types pages are not in the sources file's fetched list (only star schema, Model relationships and Many-to-many pages are). Statements match my knowledge but remain unverified here.
- Q12/Q58: Microsoft pages disagree on service-side many-to-many support; left labelled unresolved.
- Windows-only Desktop (Q1, Q17, Q43), free Desktop, 1 GB shared-capacity limit and Premium-to-Fabric note (Q38), calendar-based time intelligence preview status (Q13), menu paths (Home vs Modeling tab, New table, Mark as date table, What-if parameter, Performance analyzer): from memory, unverified; labelled as such in the part.
- Q49 pandas memory is not VertiPaq storage (stated in the answer).
- Q47, Q55, Q56 DAX/M not run; results reproduced by pandas logic only.

## Overlap with other parts (report only)
- USERELATIONSHIP/CALCULATE basics likely overlap the DAX parts (Parts 04 to 06). Q59 CROSSFILTER and Q60 TREATAS may overlap an advanced DAX part. Auto date/time and date table (Q13, Q36) may overlap a time-intelligence part. Q29 and Q50 (blank row / unknown member) overlap each other by design. Q12, Q28, Q58 overlap each other (bridge, many-to-many) by design.
