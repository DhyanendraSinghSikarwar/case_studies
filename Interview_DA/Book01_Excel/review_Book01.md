# review_Book01.md — Book 1 (Excel) review summary (Wave C, plan.md Section 8.6)

Date: 2026-10-22. One reviewer per part re-executed each answer's formulas with `tools/xl_eval.py` (headless LibreOffice 24.2) and pandas, fixed errors in place, tried to resolve "from memory" claims from fetched Microsoft Support / Google Docs Editors Help pages, and wrote `review/review_PartNN.md` (every fix is listed there). Reviewer-reported counts are the reviewers' own and some are approximate.

## Pass criteria (plan.md 8.6)
| Check | Result |
|---|---|
| Completeness | 638 of 638 questions answered; 0 `ANSWER_PENDING` (script check) |
| Count | 638 vs target 600 (met); every part at or above its part target |
| Ordering / numbering | Q1..Qn continuous in every part; stars descending then 🟢→🔴 (script check) |
| Heading integrity | All 638 headings match the frozen question index exactly (script check run after review: see incident below) |
| Template fields | Base fields present in every answer (script check); formula answers carry Sample sheet / Formula / Alternative / Result / Version note, except concept, dialog and Google-Sheets-only answers where no sheet applies |
| Duplicates | 11 cross-part duplicates removed before answering (`research/dedupe_log_book01.md`); a token-overlap rescan after review shows only intentional overlaps (different tool or angle) |
| Markdown | Code fences balanced; blank line after every table (script check) |
| Accuracy | Every formula that LibreOffice 24.2 can run was re-executed by a reviewer and the printed Result matches; see limits below for what could not run |

## Per part
| Part | Answers | Edited in review | Formula results re-run | Main fix types |
|---|---|---|---|---|
| 1 Basics | 66 | 23 | 31 | sample data not matching example text, wrong cell references, circular VLOOKUP, wrong error claims, Example added Q12/Q16 |
| 2 Core functions | 74 | 19 | ~66 | wrong COUNTA/TEXTJOIN claims, wrong day count, WORKDAY.INTL mislabelled "not run", IFNA wording reconciled |
| 3 Lookups | 60 | 17 | 51 | placeholder phone numbers, missing #N/A demo, example/sample mismatch, wrong "#VALUE!" claim, Sheets-has-Tables claim |
| 4 Pivots | 74 | 16 | 24 groups + pandas | wrong lookup cell, Sheets slicer claim corrected, 5 thin answers completed (Q64, 65, 70, 71, 73) |
| 5 Cleaning | 50 | ~22 | ~33 | CHAR(160)/VALUE results corrected, REPLACE case claim, 5 thin answers completed (Q44, 45, 47, 49, 50) |
| 6 Dynamic arrays | 45 | 22 | ~45 (+pandas for 365-only) | sample sheet 7 vs 10 rows, tie order, LET speed claim, SUMIFS closed-workbook claim, Q27 EDATE mystery explained (Python type mismatch, not Excel) |
| 7 Power Query/Pivot | 64 | ~21 | 6 (+pandas replicas) | "six kinds" vs seven, default join conflict stated, rename of Microsoft page, missing sample data |
| 8 Charts/dashboards | 54 | 15 | 29 | truncated/mismatched sample sheets rebuilt, funnel/map availability resolved, unsupported claims removed (see incident) |
| 9 What-if/CF/validation | 46 | 16 | ~36 | wrong counts, macro/Result mismatch, Sheets multi-select outdated claim corrected (Q38), alert-label conflict documented |
| 10 Scenarios | 60 | 15 | 54 | sample/formula column mismatch, wrong example text, own-definition labels on attrition formulas |
| 11 VBA/Copilot | 21 | 15 | all runnable | COPILOT function retired from 14 Sep 2026 (confirmed on Microsoft page), macro-blocked-by-default example corrected, DATEDIF is documented (compatibility function) |
| 12 Skill development | 24 | 5 + plan sections | 39 | self-test key executed, quiz sizes, resource claims aligned to sources; all six plan items present |

## Incident during review (found and repaired by the coordinator)
A Part 8 reviewer's in-progress edit deleted answers Q3–Q9 from `Book01_Part08.md` (file dropped to 47 questions; numbering jumped from Q2 to Q10). Detected by the post-review structural check; Q3–Q9 were restored from the pre-review commit, and a targeted agent then re-applied the lost review fixes to those seven answers (see the Addendum in `review/review_Part08.md`). All other parts were checked for question count and heading integrity: no other loss found. Lesson recorded: after every wave, rerun the count and heading check against the frozen index.

## Known limits (not fixed; honest status)
- **Never run in Excel.** All pasted Results come from LibreOffice 24.2 or pandas. Text-to-number coercion, `DATEDIF` edge cases, `CHAR(160)` and error codes (`#REF!` vs `#VALUE!`) can differ in real Excel; answers flag the known differences and label Excel behaviour "from Microsoft documentation" only where a page was fetched, otherwise "from memory, unverified".
- **Cannot run here:** XLOOKUP, XMATCH, FILTER, UNIQUE, SORT, SORTBY, LET, TEXTSPLIT/TEXTBEFORE/TEXTAFTER, spill, pivots, slicers, charts, Power Query, Power Pivot/DAX, VBA, Office Scripts, Apps Script, Copilot/Gemini. Their expected values were reproduced with pandas or by hand and are labelled "not run here".
- **Microsoft pages conflict with themselves in places** and the answers state the conflict instead of choosing: XLOOKUP "not available in Excel 2016/2019" note vs Applies-to list (treated as 2021/365); Create-a-PivotTable Recommended PivotTables note; Data Model size limits (250 MB vs 10 MB figures); error-alert third label ("Important" vs "Information"); Merge default join.
- **Still unverified:** Power Pivot availability by Office edition; whether Unpivot folds on SQL sources; fuzzy merge in Excel 2016; Pareto/treemap introduction version; many Google Sheets behaviours (several Google help URLs returned 404); keyboard-shortcut and menu-path details not on fetched pages; Copilot/Gemini licence tiers; the Excel 2016/2019 end-of-support date.
- **Rebuilt/constructed sample data:** where the original sample sheet was truncated, reviewers rebuilt rows to reproduce the printed results (Part 8 Q4, Q6, Q9, Q27 and similar); those rows are constructed, not sourced.
- Interview-frequency stars are editorial (see `research/Book01_PartNN_sources.md`); "Asked at" is limited to what the research files support, which is mostly search-snippet level and candidate-reported.
- Beginner clarity: fully read for answers the reviewers edited; the rest scanned. A read-through by a non-technical reader is still advisable.
