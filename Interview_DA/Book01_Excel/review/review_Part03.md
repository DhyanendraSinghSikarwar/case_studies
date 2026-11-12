# Review of Book 1, Part 03 (Lookups), Wave C

Date: 2026-10-22. File reviewed and fixed in place: `Book01_Excel/Book01_Part03.md` (60 answers). Scratch scripts: `/tmp/claude-0/-home-user-case-studies/65c5a153-2270-59c7-806a-2ca081fd6877/scratchpad/C1_Part03`.

## Counts
- Answers checked: 60 of 60. Answers edited: 17 (Q4, Q11, Q12, Q13, Q19, Q23, Q26, Q29, Q35, Q41, Q42, Q47, Q48, Q49, Q51, Q59, Q60). No heading, number, star or order was changed.
- Answers with a runnable formula and a printed Result: 51. Re-executed with `tools/xl_eval.py` (LibreOffice 24.2): 51; all printed results match after the fixes. Array formulas (Q48, Q51, Q57) were run as true array formulas.
- Not runnable here, expected values checked by hand or pandas-style reasoning and labelled "not run here": the XLOOKUP/XMATCH/FILTER forms in Q7, Q23-Q26, Q33, Q37, Q39, Q40, Q46, Q49, Q54, Q55, Q60; Table and spill answers Q41, Q42; Google Sheets answer Q47; the external-workbook form in Q16. Checked values: Q7 Pune, Q24 103/104/Not found, Q33 5, Q37 5/10/10/15, Q39 410, Q40 1 and 5, Q49 IT/HR/HR/Not found, Q60 140. All agree with the INDEX-MATCH or LOOKUP versions that were run.

## Fixes
| Q | Problem | Fix |
|---|---|---|
| Q4 | Concept answer had no Sample sheet or Result | Added a 3-row payroll sample and a run result (VLOOKUP gives #N/A, INDEX-MATCH gives 55000) |
| Q11 | No Result field; Sheets XLOOKUP claim unverified | Added Result (INDEX-MATCH run, IT); cited fetched Google page |
| Q12 | Result showed "97xxx" placeholder | Gave actual phone numbers in the sample; result `9700022222` (run) |
| Q13 | Result was only reasoning ("not run") for the failing case | Ran both orders: sorted IDs all correct; Q3 order gives IT, #N/A, Sales, #N/A, #N/A |
| Q19 | VLOOKUP error codes cited from an unread page; decimal index unverified | Quoted fetched page (#REF!; its #VALUE! line is a typo for col_index_num); LibreOffice used column 2 for 2.7, Excel still unverified |
| Q23 | Muddled edge case about `,,` | Reworded; labelled unverified |
| Q26 | Missing-ID spill behaviour stated as fact; Sheets claim unverified | Labelled untested; cited Google XLOOKUP page (returns entire row or column) |
| Q29 | "After" test used unnamed Grade values | Stated Grade values; result `L4` now run |
| Q35 | No Sample or Result; Power Query version from memory | Added a run check of the helper-MATCH pattern; Power Query verified from fetched page |
| Q41 | Table origin and Sheets difference unverified | Added Applies-to list; Sheets has own Tables (fetched) |
| Q42 | Example (A2:A20, E5) did not match sample (A2:A4, E3); unverified causes | Example aligned to sample; sourced the Table cause; labelled merged cells and `#` as from memory |
| Q47 | "Sheets has no Tables" outdated; IMPORTRANGE/ARRAYFORMULA from memory; no Sample sheet | Corrected; cited fetched Google pages; added Sample line |
| Q48 | FILTER #CALC! claim unverified; INDEX/SMALL needs array entry | Cited FILTER page; noted wrong values without array entry |
| Q49 | Sheets range-of-keys claim unverified | Reworded: page does not address it |
| Q51 | Said non-array nearest formula gave #VALUE! | Actual LibreOffice result is a wrong value (42000); array-entered gives 47000; text corrected |
| Q59 | Table not rendering (no blank line before it); sheet salaries not given | Added blank line and the salary data; volatility labelled unverified |
| Q60 | Reference behaviour uncited | Cited XLOOKUP page Example 6 (fetched) |

## Claims newly verified (pages fetched 2026-10-22)
- Microsoft Support: "XLOOKUP function" (note "not available in Excel 2016 and Excel 2019" vs Applies-to list naming them; if_not_found, match and search modes, binary-search warning, array return, Example 6 range-returning XLOOKUP), "IFNA function" (Applies to 2016 and later, no introduction date), "LOOKUP function", "MATCH function", "XMATCH function" (365/2024/2021 only), "VLOOKUP function", "FILTER function", "INDIRECT function" (closed workbook gives #REF!), "Using structured references with Excel tables", "Dynamic array formulas and spilled array behavior" (Tables block spills; page lists 2016/2019 but gives no version statement), "Power Query data sources in Excel versions" (all Excel 2016 or later Windows stand-alone versions).
- Google Docs Editors Help: "XLOOKUP function", "VLOOKUP" (is_sorted defaults to TRUE), "ARRAYFORMULA", "IMPORTRANGE" (title and gist), "Use tables in Google Sheets".
- XLOOKUP conflict kept consistent: treated as 2021/2024/365 across the part.

## Still unverified (labelled in the answers)
- Excel text-to-number coercion and the #REF! (not #VALUE!) result for a too-large column index: LibreOffice differs; the #REF! part is now sourced, the text-number part is "from memory".
- Decimal col_index_num truncation, XLOOKUP empty argument slot, XLOOKUP multi-column not-found spill, `E2#` operator, merged-cell #SPILL!, INDIRECT volatility and quoting, AGGREGATE-based nth match (does not run in LibreOffice), VSTACK/CHOOSECOLS/LET availability, Excel Tables from 2007, IFNA from 2013.
- Google Sheets: INDEX-MATCH, MATCH default, case sensitivity, XLOOKUP with a range of keys, XMATCH, CHOOSE with braces.
- Speed claims in Q35 (none measured). XLOOKUP linear modes not needing sorted data (page silent; labelled as understanding).
- "Asked at" lines: all are either "commonly asked (no company-specific report found)" or the JD mentions confirmed in `research/jd_sample_mis_people.md` (Ninjacart, Tata Advanced Systems, Vee Technologies). No change needed.

## Unresolved, report only
- Q22 and Q50 (case-sensitive lookup) and Q21/Q33/Q58 (last match) overlap on purpose; Q27 overlaps Q13 and Q3. Ordering within star groups follows the frozen list.
- Markdown: no code fences in the part; all tables now have a blank line before and after.
