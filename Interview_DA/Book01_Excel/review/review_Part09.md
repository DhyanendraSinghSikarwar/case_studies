# Wave C review: Book 1 Part 09 (What-if, Goal Seek, conditional formatting, data validation)
Reviewer pass 2026-10-22. Edited only Book01_Part09.md; scratch in scratchpad/C1_Part09.

## Counts
- Answers checked: 46 of 46.
- Formula results re-executed with tools/xl_eval.py (LibreOffice 24.2) and matching printed Result: 36 answers (Q1, 3-7, 10, 12, 15, 17-29, 31-35, 37, 39 (run with hidden rows), 40, 42-45 count formula; plus Q6/Q10 profit and Q19 grid). All matched except the items fixed below.
- Python checks: Q30 brute force (26 hires, plans [14,9,3] and [15,8,3]; second costs 690k, first 700k) matches; Q36 Newton 5.0 / -5.0 matches; Q45 macro-logic simulation re-run.
- Not run here, labelled so: dialogs, Goal Seek, Solver, Scenario Manager, data tables, icon sets, VBA, Sheets, UNIQUE/FILTER (Q46, pandas values correct by hand: UNIQUE Sales, HR, IT, Finance; FILTER IT = Data Analyst, Developer, Tester).
- Answers edited: 16 (Q8, 11, 13, 14, 15, 16, 21, 24, 27, 30, 32, 33, 36, 38, 43, 45).

## Fixes
| Q | Problem | Fix |
|---|---|---|
| 24 | Text said 7 values above average 56.58; sheet gives 6 | Corrected to 6 and listed them |
| 45 | Result claimed "add or remove on click" but the macro only appends (repeat pick ignored) | Result rewritten to match the macro, re-simulated |
| 36 | Specific "stopped at x=0.81, gap 4.66" figure not reproducible | Replaced with hand argument; Newton 5/-5 re-run |
| 21 | INDIRECT claim not executed with real names | Re-run with defined names, header "Tamil Nadu": 2 items, second Coimbatore |
| 15 | "#VALUE! ... Excel would also reject" unsupported | Labelled unverified, added IF(ISNUMBER) wrapper |
| 38 | Needed chip multi-select reflected; wrong help-page title | Added chip explanation, quoted Google page, mobile limit, title fixed, other-sheet claim confirmed |
| 45 | Same wrong Google page title | Fixed to "Create an in-cell dropdown list" |
| 14 | Label conflict | Both Microsoft pages fetched; conflict stated, advice on what to say |
| 13 | Misquote of Manage Rules | Replaced with actual wording (create, edit, delete, view; Duplicate, Move Up/Down) |
| 11 | Quote slightly off, icon-set claim cited wrong page | Quote corrected, icon-set page cited |
| 8, 30 | Version claims inaccurate (scenarios page lists only 365/2024/2021; Solver page lists 2016-2024) | Corrected |
| 16 | Length limits | Noted fetched page states none; still unverified |
| 27 | Other-sheet rule claim unverified | Confirmed same workbook only, not other workbooks |
| 32 | "Not in Excel for the web" too strong | Softened to Microsoft wording "may not see" |
| 33 | Unsupported Format Painter claim | Replaced with fetched wording |
| 43 | Show Icon Only / Reverse Icon Order "unverified" | Confirmed on the CF page |

## Newly verified (fetched pages)
Create an in-cell dropdown list (Google Docs Editors Help); Use conditional formatting rules in Google Sheets; Apply data validation to cells; Create a drop-down list; Use conditional formatting to highlight information in Excel; Use data bars, color scales, and icon sets to highlight data; Define and solve a problem by using Solver (200 cells, constraints, no Excel for web); Use Goal Seek...; Calculate multiple results by using a data table; Switch between various sets of values by using scenarios (32 values, static reports).

## Still unverified
Excel UI label "Information"; no built-in Excel multi-select (Microsoft pages silent; search found none); title/message length limits; exact name "Automatic except for data tables" (page only describes it); same-sheet input-cell rule for data tables; spill reference `#` in validation (third-party only); Sheets Goal Seek/Solver add-ons; Scenario Manager in 2016/2019; Circle Invalid Data in Excel for the web (search snippet only); Excel's text-date and error-in-validation behaviour.

## Unresolved / report only
- Q11, Q13, Q14, Q16, Q41 have no Sample sheet or Result (concept/dialog questions); left as is.
- Header says Target 40, actual 46; part contains no duplicates. Order is by stars then difficulty; no renumbering needed.
- Asked-at lines all say "commonly asked" or cite sources file items; no unsupported company claims found.
- Markdown: 2 code fences balanced; blank line after every table checked.
