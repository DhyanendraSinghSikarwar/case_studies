# Review: Book04_Part06 (Visuals, slicers, drill-through, bookmarks, tooltips)

## Counts
- Answers checked: 61 (Q1-Q61), all read in full.
- Pandas snippets run (pandas 3.0.5): 30 answers with a Pandas check (Q11, 18, 22, 23, 25, 30-32, 34-36, 38, 45, 48, 50-52, 54, 56-58, 60, 61 and others). All 30 ran and reproduce the printed outputs and Result lines. Q36 and Q61 needed data or code added to be runnable.
- DAX measures re-derived by hand against the pandas logic (Q11, 22, 30, 31, 51, 54, 57, 58, 60): all match. Not run in a DAX engine.
- Answers edited: 26. No heading, number, star or order changed. Fences balanced (82 fence lines). Every table has a blank line after it.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| 5, 8 | Q8 said "Home > Insert > New page". Q5 said "Tooltip on", while Q26 and Q55 say "Allow use as tooltip". | Q8 changed to "Home > New page". Q5 reworded to match Q26. |
| 11 | Rules click-path was garbled ("If value >= 0.15..."). Pandas check had no data, so it could not run. | Rewrote the two rules and marked the menu names unverified. Added the data and a print of the total (0.1545). |
| 12 | "Asked at" claimed prep-blog snippets that the sources file does not support. | Changed to "gap-fill from standard practice". |
| 15 | "Returned 404 for the earlier agent" was unclear. | Reworded to "in the earlier research pass". |
| 18, 23, 25, 34, 35, 38 | Pandas checks used undefined variables (p, s, m, c, emp, sc). | Added the sample data and a print. All now run and match. |
| 22 | Said "Constant line or a Y-axis constant". The Analytics pane has X-axis and Y-axis constant lines. The pandas check lacked `import pandas`. | Now says "Y-axis constant line". Added the import. |
| 26, 29 | Cross-references "see Part 6, tooltip limitations" and "Part 6 Q49". | Changed to Q55 and Q49. |
| 30 | Pandas check defined the function but never called it. It also had no data. | Added data and the three test calls. They print IT, All departments, All departments. |
| 31 | DAX used `[Attendance %]` but never defined it. Pandas check used an undefined `col()`. | Added `Attendance %` as AVERAGE of the column, plus a runnable `col()` and data. |
| 32 | DAX referred to `Employee[Name]`, which is not in the sample. Pandas check used an undefined `att`. | Matrix rows now use `Attendance[Employee]`. Pandas check builds the long table from the sample and pivots it. |
| 33 | Said Legend can create drill levels. This contradicts the same answer's own example and "Common mistakes". | Removed Legend from the list of level-creating wells. |
| 36 | Pandas check had no 15-row data. | Built a 15-row table that reproduces both summary tables and the 33.3% overall rate. Ran it. |
| 45 | Edge case said the decomposition tree "cannot be a drillthrough or cross-filter source". This is an unverified claim. | Softened to "test in your build (from memory, unverified)". |
| 51 | The setup block said "emp = the 12-row table above". Eight later answers run it through `setup.py`, so it could not run as printed. | Added the actual 12-row loader. Noted that Headcount prints as 2.0, 3.0 and so on. |
| 54 | `TopN = {3,5,10}` creates a column called Value, but the measure uses `TopN[TopN]`. | Added a note to rename the column. |
| 56 | Pandas actually prints orphan key `[9.0]`. The answer said 9. | Result line now explains the `[9.0]`. |
| 60 | Follow-up said ALL inside CALCULATE removes a Filters-pane filter. It only does so for filters on the same column. | Corrected. |
| 61 | Pandas check was only a description. | Added a runnable loop over Dept, Location and Grade. Output matches the Result line. |

## Checks that passed (no change)
- Hand re-derivation: Q11 total 85/550 = 15.45%; Q18 top 10 = 1,560 of 1,625; Q22 mean 428.33; Q34 2.00/1.46/2.96; Q38 correlation 0.988; Q48 ON 2 / OFF 3; Q50 Bengaluru 5, Hyderabad 4 and the Dept x Location counts; Q52 `7 7` then `8 7`; Q54 285/355/385; Q57 3 rows off, 12 on, 9 blank; Q58 9+3-3=9 with per-department reconciliation; Q60 20.0% and 50.0%.
- Syntax read: RANKX argument order (table, expression, value, order, ties) is correct. SELECTEDVALUE, NAMEOF field-parameter shape, CONCATENATEX and the M `Table.ReplaceValue` call are correct. VAR/RETURN and brackets are balanced.
- Labelling: every DAX, M and click-path block carries "(not run here)". Results say "reproduced with pandas". Version notes say "from memory, unverified".
- "Asked at": Cognizant 2022 (slicers, filters) is supported by research/interview_processes.md. The Bajaj Auto Telegram post and the DataToBiz AmbitionBox report (Mar 2024) are supported by the sources file and flagged as unverified there. No invented company claims found.
- Template: all 61 have the core fields. Questions with measures or modelling also have Sample data, DAX/Steps, Alternative, Result and Pandas check. Q61 has no separate Sample data or Pandas data, but it references Q51 by design.

## Unresolved / left unverified (no Microsoft Learn access)
- Menu and pane names (Format page, Page information, Canvas settings, Sync slicers, Query reduction, Mobile layout) and the Keep all filters default (answer says "I believe On").
- Cross-report drillthrough: "Service only, same workspace" comes from the sources file only. The Report settings path is from memory.
- Certified visuals' export benefits, admin controls, the "1 in 12 men" colour-blindness figure, the 320x240 tooltip size, and whether hidden visuals still run queries are all marked from memory.
- Q57: Show items with no data only adds items that exist in the field's table or a related table. The answer already says dates should come from a proper date table.
- Q58: the "set as total" option on the waterfall is unverified.

## Overlap / ordering (report only)
- Stars descend (3 > 2 > 1) and green runs to yellow to red within each tier. Numbering is continuous 1-61.
- Overlap inside the part: Q9 / Q12 / Q60 (Edit interactions), Q8 / Q29 / Q35 (drill-through steps), and Q26 / Q55 (tooltip build). These are cross-referenced and intentional.
- Overlap with other parts: Q7 mentions Part 5 for the headcount measure design. Q36 points to Part 11 (decomposition tree). Not checked against those parts here.
