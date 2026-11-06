# Wave C review: Book 1, Part 11 (VBA basics, Copilot and Gemini)

Reviewed 2026-10-22 (after the 14 Sep 2026 date). Scratch: C1_Part11. VBA, Apps Script, Copilot and Gemini cannot run here; they were checked by careful reading and Python/Node mirrors and are labelled "not run here" in the part.

## Counts
- Answers checked: 21 of 21 (Q1-Q21 headings, numbers, stars, order unchanged).
- Executed checks re-run and matching: 6 LibreOffice 24.2 runs (xl_eval) with 29 values, plus 5 mirrors.
  - Q4 attendance formulas: F2:F8, G2:G8, COUNTIF = 3, Ops 93.2%, HR 77.3%. Matches.
  - Q5: attrition Sales 33.3%, HR 50%, Ops 0%. Q6: 8, 2, 0.25, 139000, 354000, 0. Match.
  - Q10: DATEDIF 2,1,0,5,6; Python mirror of the UDF gives the same.
  - Q14: DATEDIF formula and Python mirror both give Under 1 yr, OK, Under 1 yr, OK, blank, Check date, Under 1 yr, OK.
  - Q13: Node.js mirror of the Apps Script logic gives the same eight labels.
  - Q15: SUMPRODUCT/MATCH formulas return 8 and 4; the VBA expectations follow.
  - Q16: Python simulation of Resume Next gives 95.5, 77.3, 100, 86.4, 63.6, 90.9, 90.9.
- VBA/Apps Script code read line by line: Q1, Q3, Q4, Q8, Q9, Q10, Q13-Q17. No syntax or logic bug found; none run in Excel.
- Answers edited: 15 (Q1, Q2, Q4, Q5, Q6, Q7, Q10, Q11, Q12, Q14, Q15, Q16, Q17, Q18, Q19; Q18 and Q19 are label or verification-stamp changes only).

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q1 | "Web runs VBA?" was unverified; Office Scripts left undescribed | Cited Microsoft Learn "Differences between Office Scripts and VBA macros": VBA not supported on Excel on the web; added Office Scripts facts with a "page dated 2023" caveat |
| Q2 | Macro-name rule attributed to a page seen only in search; Alt+F11 and Personal Macro Workbook "from memory"; version note claimed 2016/2019 | First character must be a letter (search result; fetched page lists no rules); "no spaces" marked unverified; Alt+F11 and Personal.xlsb cited to "Copy your macros to a Personal Macro Workbook"; version note now follows the Quick start Applies-to list (365, 2024, 2021 Mac) |
| Q4 | Say-this line contained an instruction to the reader inside the quoted speech | Moved the honesty advice outside the quote; clarified formulas were executed, macro not |
| Q5 | Icon "on Home tab" (from memory) was wrong per Microsoft; modes incomplete; perpetual-version line vague | Icon is lower-right corner (Get started page); default mode Allow editing, plus Plan and Chat only; iPad/iPhone modes; perpetual versions: Applies-to lists name only 365/iPad/web, my reading |
| Q6 | Sample sheet did not show the salary data behind 139,000 / 354,000 (not reproducible) | Added the full 8-row A:D table; results re-run and match |
| Q7 | Example said a yellow bar with Enable Content for an emailed file; Microsoft says internet files are blocked with a red banner and no Enable Content; Save-a-macro and Personal.xlsb unverified | Corrected example (Unblock in Properties); version note now cites "Macros from the internet are blocked by default in Office" (Windows only, 2022 rollout); Save a macro wording confirmed (Excel 2013 page); PMW cited |
| Q10 | Called DATEDIF "hidden" | Microsoft documents it as a compatibility function (DATEDIF page); added #VALUE! edge for blank/text arguments; noted Excel DATEDIF agreement is from memory (only LibreOffice run) |
| Q11 | Fetched URL had 404ed in Wave B; GEMINI() status vague | Working URL support.google.com/docs/answer/14218565 recorded; page re-fetched and every cited claim holds; GEMINI() stays unverified (no official page found; third-party conflict) |
| Q12 | File-location/table requirement unresolved | Current FAQ states neither; an older FAQ version (search summary only) said OneDrive/SharePoint + AutoSave + tables to 2M cells; labelled; licence list re-confirmed against the current FAQ, flagged "as read 22 Oct 2026" |
| Q14 | DATEDIF called "undocumented" (wrong); as-of cell G1 not shown in sample | Now: documented, Excel 2016-365, compatibility function with MD warning, only "y" used; sample sheet notes G1 |
| Q15 | Variable `firstGapAbove` misleading and undeclared under Option Explicit | Renamed `lastBeforeGap`, declared with Dim |
| Q16 | Missed Microsoft's note on when Resume Next is preferred | Added as follow-up 3 (On Error page) |
| Q17 | "Results are identical" overclaimed (array version omits the yellow fill; VBA not run) | Reworded |
| Q18 | Retirement text from Wave B only | Re-fetched 22 Oct 2026 and recorded in Version note |
| Q19 | DPDP Act "from memory" | Act No. 22 of 2023 and Rules of 13 Nov 2025 now cited to search results, still marked unverified |

## Newly verified from fetched pages (fetched 2026-10-22)
- "COPILOT Function" (support.microsoft.com/en-us/excel/copilot-function): "Starting September 14, 2026, the COPILOT function is no longer available in Microsoft Excel"; recalculating cells return #NAME?; cached values stay; replacement is Copilot in Excel; Applies-to: 365, 365 Mac, web, iPhone; no licensing text; earlier Frontier only. Statement in Q18 is CONFIRMED.
- "Frequently asked questions about Copilot in Excel": licence list, .xlsx / Strict-format note, Automatic calculation, SharePoint check-out, "Review, edit, and verify...", sensitive-areas advice, coauthor visibility, cannot be turned off independently, English-trained. All as cited in Q5, Q6, Q12, Q19, Q21.
- "Get started with Copilot in Excel": modes, platform support (Android chat only), lower-right icon, licence caveat.
- "Collaborate with Gemini in Google Sheets"; "Google Sheets Macros" (Google for Developers): all cited claims hold (macros.gs, ten shortcut macros, bound scripts only, Import).
- "Enable or disable macros in Microsoft 365 files" (both quotes, four settings); "Macros from the internet are blocked by default in Office"; "Quick start: Create a macro"; "Copy your macros to a Personal Macro Workbook"; "Save a macro"; "DATEDIF function"; "Differences between Office Scripts and VBA macros".
- Microsoft Learn: Option Explicit statement, On Error statement, Function statement, Range.End, Application.ScreenUpdating, Application.RecordRelative: quotes match.

## Still unverified (labelled in the part)
- Copilot licence tiers and Gemini plan names (change often; only as read on the date).
- Whether Excel DATEDIF "y" equals LibreOffice for the leap-day rows (LibreOffice only).
- VBA recorder details: macro-name "no spaces", Use Relative References button location, toggle persistence, recorder output text; File > Options > Customize Ribbon; VBE Tools > Options > Require Variable Declaration; Excel steps on 2016/2019.
- Excel for the web UDF behaviour (follows from "VBA not supported on web", not stated for UDFs).
- GEMINI()/AI() cell function in Sheets; Apps Script quotas, Gmail/MailApp; Power Query built in from Excel 2016 (Part 7).
- DPDP Rules timeline; "Asked at" MIS-interview snippets (search results only); Office Scripts page is dated 2023.

## Unresolved / report only
- All VBA and Apps Script code is unexecuted in the real host (no Excel/Sheets here); expected values come from mirrors.
- Title line says "Target: 20 / Actual: 21"; 12 VBA + 1 Apps Script gap-fill + 8 AI = 21, consistent. Numbering, order and stars not changed. Markdown: fences balanced, blank line after every table.
