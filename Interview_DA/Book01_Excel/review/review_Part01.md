# Review of Book 1 Part 01 (Wave C)

Date: 2026-10-22. File: `Book01_Excel/Book01_Part01.md`. Edits were made in place, with no heading, number, star or order changes.

## Counts
- Answers checked: 66 of 66 (all read in full; the template-field check by script finds all 7 base fields in all 66).
- Formula results re-executed in LibreOffice 24.2 via `tools/xl_eval.py`: 31 answers (Q1, 2, 3, 5, 11, 14, 17, 19, 20, 26, 28, 33, 35, 36, 37, 38, 41, 43, 44, 45, 46, 49, 50, 56, 61, 62, 63, 65, 66, plus Q6/Q8/Q9/Q48 by hand/pandas-style calculation). All printed results match, after the fixes below. Q61's hidden-row SUBTOTAL values (30, 25, 4, 30) were re-run with rows hidden through openpyxl.
- Not runnable here, labelled "not run here" and checked by hand: Q6, 8, 9, 10, 32, 34, 46 (SORTBY), 47, 48, 51, 62 (UI part), 64, 66 (UI/SORT).
- Answers edited: 23 for content (Q1, 5, 7, 12, 16, 17, 18, 19, 20, 24, 25, 34, 38, 42, 44, 46, 49, 54, 56, 60, 63, 65, 66), plus blank-line-before-table spacing in every answer that has a sample table.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| 1 | "Asked at" said every beginner list incl. Guru99 had it; sources file lists only DataCamp | Narrowed to DataCamp |
| 5 | Edge case said text "10 " gives #VALUE!; run gave 2500 (only "ten" gives #VALUE!) | Corrected, labelled Excel behaviour as from memory |
| 7 | Sample salaries (45000, 52000) did not match the Q6 data and the example | Sample now 35000, 40000, 52000, 60000; example lists the original pay |
| 12 | No Example field | Added |
| 16 | No Example field | Added |
| 17 | Total in A7 below a blank A6, contradicting the "blank row stops AutoSum" edge case | Total moved to A6, steps and result updated |
| 18 | Row/column limits "from memory" | Confirmed from Microsoft page, cited |
| 19 | Result cited a D2 not on the sample sheet | Column D added to the sample |
| 20 | Vague "Excel sometimes coerces" | Replaced with what the run showed and a from-memory label |
| 24 | Google Sheets sheet-switch keys unverified | Confirmed from Google shortcuts page |
| 25 | Google Sheets "Ctrl+J jump to range" unsupported; the Google page lists Go to range as Ctrl+G on Mac only | Claim removed |
| various | Some sample tables had no blank line before them (render risk) | Blank line added everywhere |
| 34 | Google colour filter unverified | Confirmed from Google filter-views page |
| 38 | Google paste-values key missing | Added Ctrl+Shift+V (Google page) |
| 42 | "Print setup is standard for MIS roles (sources file)" overstated | Reworded to what the sources file says |
| 44 | Steps said click B2, sample uses B5 | Fixed |
| 46 | Custom-list "unlisted goes last" stated as fact | Labelled from memory, unverified |
| 49 | VLOOKUP sat inside its own lookup range (circular); #VALUE! in LibreOffice vs #REF! in Excel only "from memory" | Formulas moved to column D; Microsoft VLOOKUP page confirms Excel gives #REF!; LibreOffice difference stated |
| 54 | "Gap in row 800 fills 799 rows" miscounted | Reworded to "fills down to row 799" |
| 56 | Example used B2, sample uses A2; Google keys unverified | Fixed; re-run on 22-Oct-2026 gives 294 (21-Oct gave 293); Google keys confirmed |
| 60 | All Google claims unverified | Filter views confirmed from Google page; rest still from memory |
| 63 | 15-digit limit from memory | Confirmed from Microsoft specs page |
| 65 | "No custom formats in Excel for the web" from page "above" | Quoted from fetched Microsoft page |
| 66 | SORT alternative sorted by Team only, so Sales order differed from the stated result | Now `SORT(FILTER(...),{2,3},{1,-1})` (not run here) |

## Newly verified (fetched pages)
- Microsoft Support, *Keyboard shortcuts in Excel*: F4 cycling and Mac Cmd+T/F4, Ctrl+Shift+*, Ctrl+Shift+#, Ctrl+;, Ctrl+Shift+:, Ctrl+`, Ctrl+Y repeat, Ctrl+A (Windows). Ctrl+Shift+L, Ctrl+H, Ctrl+F, Ctrl+G, Ctrl+Shift+9/0 are listed only for Web and/or Mac, not Windows; Alt+; is not listed at all (answers already say so).
- Microsoft Support, *Excel specifications and limits*: 1,048,576 rows by 16,384 columns; 15-digit precision. Sheet-name length is not on the page (left from memory).
- Microsoft Support, *Create or delete a custom number format*: cannot create custom formats in Excel for the web.
- Microsoft Support, *VLOOKUP function*: #REF! when col_index_num exceeds the table width.
- Microsoft Support, *Protect a worksheet*: not a security feature; Microsoft cannot retrieve a forgotten password; web uses Review > Manage Protection.
- Microsoft Support, *XLOOKUP function*: note "not available in Excel 2016 and Excel 2019" versus Applies-to list naming them; Q59 states this conflict and treats XLOOKUP as 2021/365.
- Google Docs Editors Help (answer 181110, keyboard shortcuts) and (answer 3540681, filter views).

## Still unverified (labelled in the text)
- Microsoft "Sort data in a range or table" URL returned 404 (Q46, 62: sort left to right in Tables, custom-list ordering of unlisted labels). Create a table and Advanced Filter pages not re-tried (Q32, 47).
- Excel (not LibreOffice) behaviour of text-number coercion, Top 10 filter ties, copy of hidden rows, Format Painter copying validation.
- Google Sheets: Top 10 filter absence, merge/alignment options, table feature, Docs freeze/toggle-filter shortcuts (not on the Google page).
- Version availability of SORT, SORTBY, FILTER, RANDARRAY, FORMULATEXT, IFNA (from memory); UNIQUE page claim in Q59 carried from Wave B, not re-fetched.
- "Asked at" lines: no company-specific reports exist for this part (sources file); all say "commonly asked".

## Unresolved / report only
- Topical overlap: Q26 and Q54 (fill handle), Q7 and Q64 (sort scrambling), Q12 and Q9 (clearing filters), Q15 shortcut list repeats later shortcut answers. Kept, cross-referenced.
- Star/difficulty order: Q20 (yellow) sits among green three-star answers and Q46-51, 61-66 are yellow within their star group; the green-before-yellow rule holds only within groups. Not changed.
- Count is 66 against a target of 60 (met). Q10, Q18 and some concept answers have no Sample sheet/Result by design.
- Author's earlier "Q27 EDATE" to-do item belongs to Part 6, not this part.
