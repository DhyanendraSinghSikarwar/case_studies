# Book 1 — Excel | Part 6: Dynamic arrays: FILTER, UNIQUE, SORT, LET 🟡

**Target:** 40 questions | **Actual:** 45 questions
**Scope:** Dynamic array functions (FILTER, UNIQUE, SORT, SORTBY, SEQUENCE, LET), spill behaviour and #SPILL!, version availability (Excel 2016/2019/2021/365, Google Sheets).

### Q1 ⭐⭐⭐ 🟢 What are dynamic arrays in Excel, and what does it mean when a formula "spills"?
**Asked at:** commonly asked (no company-specific report found); FILTER/SORT/UNIQUE appear in community Excel interview lists (snippet-level evidence only).
**What the interviewer is checking:** Do you know that one formula can now return many values, and that Excel fills the neighbouring cells for you?
**Say this in the interview:** "A dynamic array formula is a formula that can return a whole list of values from one cell. When it does, the results 'spill' into the empty cells below or beside it, and Excel resizes that block automatically when the data changes."
**Explain simply:**
- An *array* is just a list or block of values. Old Excel needed one formula per cell; a dynamic array formula needs one formula for the whole block.
- The formula sits in the top-left cell. The filled block it creates is the *spill range* and Excel draws a thin blue border round it when you select any cell in it.
- Only the top-left cell holds the formula. The other cells show results and cannot be edited on their own; you edit the formula in its source cell (Microsoft Support, "Dynamic array formulas vs. legacy CSE array formulas").
- Spilling happens automatically when you press Enter; Microsoft's page says Excel sizes the output range for you.
**Example:** An HR sheet lists 8 employees with their department. Typing one formula in E2 gives the 3 distinct departments in E2:E4. If a 4th department appears in the data, the list grows to E5 without touching the formula.
**Sample sheet:**

| | A | B | C | D | E |
|---|---|---|---|---|---|
| 1 | Employee | Dept | Salary | | Departments |
| 2 | Asha | HR | 42000 | | HR (formula here) |
| 3 | Ravi | Sales | 55000 | | Sales (spilled) |
| 4 | Meena | IT | 72000 | | IT (spilled) |
| 5 | Karan | HR | 38000 | | |
| 6 | Priya | Sales | 61000 | | |
| 7 | Dev | IT | 68000 | | |
| 8 | Sana | Sales | 48000 | | |
| 9 | Tara | HR | 51000 | | |

**Formula / Steps:** In E2 type `=UNIQUE(B2:B9)` and press Enter.
**Alternative:** The old way was a legacy array formula: select E2:E4 first, type the formula and press Ctrl+Shift+Enter; the range was fixed in size.
**Result:** Not run here (expected result reproduced with pandas): `df.Dept.unique()` printed `['HR', 'Sales', 'IT']`, so E2:E4 = HR, Sales, IT.
**Version note:** Dynamic arrays arrived in Microsoft 365 in September 2018 (Microsoft Support, "Dynamic array formulas vs. legacy CSE array formulas"). The function pages for UNIQUE, FILTER and SORT list Microsoft 365, Excel 2024 and Excel 2021; they do not list 2019 or 2016.
**Edge cases:** If something is already sitting in the spill range, you get #SPILL! (see Q5). A spill cannot sit inside an Excel Table (Q23).
**Likely follow-ups:** 1) *Which functions spill?* FILTER, UNIQUE, SORT, SORTBY, SEQUENCE, RANDARRAY and any formula that returns several values. 2) *How do you refer to the whole spilled list?* With the # operator (Q16).
**Common mistakes:** Typing the formula in every cell of the block (only the first cell holds it); trying to delete one cell of the spill range; typing over the spill range.

### Q2 ⭐⭐⭐ 🟢 What does the FILTER function do, and what is its syntax?
**Asked at:** commonly asked (no company-specific report found); FILTER appears in community Excel interview lists (snippet-level evidence only).
**What the interviewer is checking:** Can you state the three arguments and explain "include" as a TRUE/FALSE list?
**Say this in the interview:** "FILTER returns only the rows that meet a condition. The syntax is `=FILTER(array, include, [if_empty])`: the data to filter, a TRUE/FALSE test for each row, and an optional message if nothing matches."
**Explain simply:**
- `array` is the block you want rows from (for example A2:C9).
- `include` is a list of TRUE/FALSE values with the same number of rows as the array. A test like `B2:B9="HR"` produces one TRUE/FALSE per row; Microsoft calls this "a Boolean array with the same height or width as the array" (Microsoft Support, "FILTER function").
- Rows where include is TRUE are returned; FALSE rows are dropped.
- `if_empty` is what you show if no row passes (Q10).
**Example:** From 8 employees, list the 3 who work in HR with their salary.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Employee | Dept | Salary |
| 2 | Asha | HR | 42000 |
| 3 | Ravi | Sales | 55000 |
| 4 | Meena | IT | 72000 |
| 5 | Karan | HR | 38000 |
| 6 | Priya | Sales | 61000 |
| 7 | Dev | IT | 68000 |
| 8 | Sana | Sales | 48000 |
| 9 | Tara | HR | 51000 |

**Formula / Steps:** `=FILTER(A2:C9,B2:B9="HR")`
**Alternative:** Data tab > Sort & Filter > Filter (AutoFilter) hides rows in place, but gives no separate live list. In 2016/2019 use a helper column or Advanced Filter (Q43).
**Result:** Not run here (expected result reproduced with pandas): `df[df.Dept=='HR']` printed Asha 42000 (row 2), Karan 38000 (row 5), Tara 51000 (row 9).

| Employee | Dept | Salary |
|---|---|---|
| Asha | HR | 42000 |
| Karan | HR | 38000 |
| Tara | HR | 51000 |

**Version note:** FILTER is listed for Microsoft 365, Excel 2024 and Excel 2021 (Microsoft Support, "FILTER function"); not in 2019 or 2016.
**Edge cases:** No match without if_empty gives #CALC! (Q10). The include array must match the array's size (Q42). Text comparison with `=` ignores upper/lower case (from memory, unverified).
**Likely follow-ups:** 1) *Can it use two conditions?* Yes, multiply for AND, add for OR (Q13, Q14). 2) *Does it change the source?* No, the source stays untouched.
**Common mistakes:** Passing a single cell as include; forgetting the ranges must have equal row counts; filtering a range that includes the header row.

### Q3 ⭐⭐⭐ 🟢 How do you get a list of unique values from a column using the UNIQUE function?
**Asked at:** commonly asked (no company-specific report found); UNIQUE appears in community Excel interview lists (snippet-level evidence only).
**What the interviewer is checking:** Can you produce a de-duplicated list without deleting data?
**Say this in the interview:** "I type `=UNIQUE(B2:B9)`. It returns each different value once, in the order it first appears, and spills them down. The original column is untouched, unlike Remove Duplicates."
**Explain simply:**
- Syntax: `=UNIQUE(array, [by_col], [exactly_once])` (Microsoft Support, "UNIQUE function").
- `by_col` TRUE compares columns instead of rows; leave it out for a normal column.
- `exactly_once` TRUE returns only values that appear a single time (Q19).
- If the array has several columns, UNIQUE compares whole rows.
**Example:** The Dept column has 8 rows but only 3 different departments.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Employee | Dept | Salary |
| 2 | Asha | HR | 42000 |
| 3 | Ravi | Sales | 55000 |
| 4 | Meena | IT | 72000 |
| 5 | Karan | HR | 38000 |
| 6 | Priya | Sales | 61000 |
| 7 | Dev | IT | 68000 |
| 8 | Sana | Sales | 48000 |
| 9 | Tara | HR | 51000 |

**Formula / Steps:** `=UNIQUE(B2:B9)`
**Alternative:** Copy the column to a new place and use Data tab > Data Tools > Remove Duplicates, or Data > Sort & Filter > Advanced > "Unique records only". Both are one-time actions that do not update.
**Result:** Not run here (expected result reproduced with pandas): `df.Dept.unique()` printed `['HR', 'Sales', 'IT']`.
**Version note:** UNIQUE: Microsoft 365, Excel 2024, Excel 2021 (Microsoft Support). Not in 2019/2016.
**Edge cases:** Blank cells in the source appear as a 0 in the list (from memory, unverified); filter blanks out first (Q34). Extra spaces make "HR " a different value, so TRIM first.
**Likely follow-ups:** 1) *Sorted too?* `=SORT(UNIQUE(B2:B9))` (Q8). 2) *Count them?* `=COUNTA(UNIQUE(B2:B9))` (Q9).
**Common mistakes:** Selecting the header too; expecting the list to be alphabetical (it keeps first-seen order); typing it in a cell that has data below.

### Q4 ⭐⭐⭐ 🟢 Which Excel versions support dynamic array functions such as FILTER, UNIQUE and SORT, and what happens if you open such a file in Excel 2019?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know compatibility limits before you share a workbook with a team?
**Say this in the interview:** "They work in Microsoft 365, Excel 2021 and Excel 2024. They are not in Excel 2019 or 2016, so a colleague on 2019 will see the formulas fail. I would check which version my audience has before building the report."
**Explain simply:**
- Microsoft's pages for FILTER, UNIQUE, SORT, SORTBY, SEQUENCE and RANDARRAY each list Microsoft 365, Excel 2024 and Excel 2021 (plus iPad, iPhone and Android). 2019 and 2016 are not listed.
- LET is the same list. TAKE, CHOOSECOLS and HSTACK are narrower: Microsoft 365 and Excel 2024 only, not 2021.
- XLOOKUP's page carries a note: "XLOOKUP is not available in Excel 2016 and Excel 2019" (Microsoft Support, "XLOOKUP function"). Its "Applies to" box still lists 2016/2019, so do not trust that box alone. The same happens on the dynamic array page, whose box lists 2019 and 2016; the function pages are the safer guide.
- In an older version, Microsoft says a formula that could return several values is shown as a legacy array formula that "cannot resize" and has no spill border (Microsoft Support, "Dynamic array formulas in non-dynamic aware Excel"). Where `@` was added, it shows as `_xlfn.SINGLE()` and returns #NAME? (Microsoft Support, "Implicit intersection operator: @").
**Example:** Your attrition dashboard uses FILTER. A colleague on Excel 2019 opens it: the filtered list shows an error rather than names.
**Formula / Steps:** Check your version: File > Account (or Help > About Excel). Before sharing: File > Info > Check for Issues > Check Compatibility.
**Alternative:** Paste the results as values, or use INDEX/SMALL formulas, Advanced Filter or Power Query, which work in 2016/2019 (Q43).
**Result:** Not a formula question; availability taken from the Microsoft Support pages named above.
**Version note:** See above. Exactly how FILTER itself displays in Excel 2019 (a `_xlfn._xlws.FILTER` name and #NAME?) is from memory, unverified; the pages I read describe only the legacy-array and `_xlfn.SINGLE` behaviour.
**Edge cases:** Saved results may still appear until the sheet recalculates (from memory, unverified). Google Sheets has FILTER and UNIQUE too (Q29).
**Likely follow-ups:** 1) *Does Excel Online work?* From memory, unverified: yes. 2) *Is dynamic array a subscription-only thing?* No, Excel 2021/2024 are one-time purchases that include it (Microsoft Support lists them).
**Common mistakes:** Assuming "Excel 2019" is newer than "2021"; relying on the "Applies to" box alone; sending the workbook without checking the recipient's version.

### Q5 ⭐⭐⭐ 🟡 What causes the #SPILL! error and how do you fix it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you troubleshoot the most common dynamic array error?
**Say this in the interview:** "#SPILL! means the formula has results to show but something is in the way. Most often, a cell in the spill area is not empty. I click the warning icon, choose 'Select Obstructing Cells', and clear or move what is there."
**Explain simply:**
- Causes and fixes from Microsoft Support, "How to correct a #SPILL! error":
  - **Spill range isn't blank:** delete or move the blocking entries (use Select Obstructing Cells).
  - **Indeterminate size:** RAND, RANDARRAY or RANDBETWEEN change size on each recalculation; use a fixed input.
  - **Extends beyond the worksheet edge:** whole-column references such as `A:A` make the result too tall; use a limited range or add `@`.
  - **Inside an Excel Table:** spills are not allowed; move the formula outside or Table Design > Convert to range.
  - **Out of memory:** use a smaller range.
  - **Merged cells in the spill path:** unmerge or move the formula.
**Example:** `=UNIQUE(B2:B9)` in E2 needs E2:E4. Someone typed "check" in E3, so E2 shows #SPILL!. Deleting E3 makes the list appear.
**Sample sheet:**

| | B | E |
|---|---|---|
| 2 | HR | `=UNIQUE(B2:B9)` shows #SPILL! |
| 3 | Sales | check (blocker) |
| 4 | IT | (needed by the spill) |

**Formula / Steps:** 1. Click the cell with #SPILL!. 2. Click the warning diamond. 3. Choose Select Obstructing Cells. 4. Delete or move them.
**Alternative:** Move the formula to a column with empty space below.
**Result:** Not run here (error behaviour of a dynamic array formula; described from the Microsoft page).
**Version note:** #SPILL! exists wherever dynamic arrays exist: Microsoft 365, 2021, 2024.
**Edge cases:** Cells that look empty but hold a space or `""` still block. Hidden rows or columns do not matter.
**Likely follow-ups:** 1) *Is it a bug?* No, it protects your data from being overwritten. 2) *Why #SPILL! with VLOOKUP(A:A,...)?* Whole column reference; use `A2:A7` or `@A:A`.
**Common mistakes:** Deleting the formula instead of the blocker; forgetting about stray spaces; typing under a spill range.

### Q6 ⭐⭐⭐ 🟡 Given an employee table with Department in column B and Salary in column C, how do you list all employees from the HR department using FILTER, showing a friendly message if there are none?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you write FILTER with a condition and the third argument.
**Say this in the interview:** "`=FILTER(A2:C9, B2:B9="HR", "No HR employees")`. The third argument is the message shown when nothing matches, so I never see an error."
**Explain simply:**
- `A2:C9` is the whole table; `B2:B9="HR"` tests each department; the text is the fallback.
- The question says Department in B and Salary in C, so I assume Employee name in A.
- The result spills across 3 columns and one row per match.
**Example:** 3 of 8 employees are in HR. Change "HR" to "Finance" and the cell shows the message.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Employee | Dept | Salary |
| 2 | Asha | HR | 42000 |
| 3 | Ravi | Sales | 55000 |
| 4 | Meena | IT | 72000 |
| 5 | Karan | HR | 38000 |
| 6 | Priya | Sales | 61000 |
| 7 | Dev | IT | 68000 |
| 8 | Sana | Sales | 48000 |
| 9 | Tara | HR | 51000 |

**Formula / Steps:** `=FILTER(A2:C9,B2:B9="HR","No HR employees")`. Put "HR" in a cell such as F1 and use `B2:B9=F1` to make it reusable.
**Alternative:** AutoFilter (Data > Filter, untick all but HR), or the legacy INDEX/SMALL formula in Q43.
**Result:** Not run here (expected result reproduced with pandas). HR: Asha 42000, Karan 38000, Tara 51000. For "Finance", pandas found 0 rows, so the cell shows "No HR employees" (message text here is just the one I typed).
**Version note:** Microsoft 365, 2021, 2024 only (Microsoft Support, "FILTER function").
**Edge cases:** "HR " with a trailing space would not match; the match ignores case (from memory, unverified).
**Likely follow-ups:** 1) *Only names?* `=FILTER(A2:A9,B2:B9="HR")`. 2) *Sorted?* Wrap in SORT (Q7).
**Common mistakes:** Leaving out the message and getting #CALC!; using `B:B` whole column; mismatched range sizes.

### Q7 ⭐⭐ 🟢 What is the syntax of the SORT function, and what do sort_index and sort_order mean?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that sort_index is a column number inside the array, not a column letter?
**Say this in the interview:** "`=SORT(array, [sort_index], [sort_order], [by_col])`. sort_index is which column of the array to sort by, counted from 1 inside the array. sort_order is 1 for A to Z or low to high, and -1 for the reverse."
**Explain simply:**
- Definitions (Microsoft Support, "SORT function"): sort_index is the number of the row or column to sort by, defaulting to the first; sort_order 1 = ascending (default), -1 = descending; by_col FALSE (default) sorts rows, TRUE sorts columns.
- The result has the same shape as the array you gave.
- Because it counts columns by number, inserting a column in the source can change which column is sorted. Microsoft recommends SORTBY for sorting data in the grid for that reason (Q15).
**Example:** Rank the 8 employees by salary, highest first. Salary is column 3 of A2:C9.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Employee | Dept | Salary |
| 2 | Asha | HR | 42000 |
| 3 | Ravi | Sales | 55000 |
| 4 | Meena | IT | 72000 |
| 5 | Karan | HR | 38000 |
| 6 | Priya | Sales | 61000 |
| 7 | Dev | IT | 68000 |
| 8 | Sana | Sales | 48000 |
| 9 | Tara | HR | 51000 |

**Formula / Steps:** `=SORT(A2:C9,3,-1)`
**Alternative:** `=SORTBY(A2:C9,C2:C9,-1)`, or the Data tab > Sort & Filter > Sort button (in place, one-time).
**Result:** Not run here (expected result reproduced with pandas): sorted by salary descending, Meena 72000, Dev 68000, Priya 61000, Ravi 55000, Tara 51000, Sana 48000, Asha 42000, Karan 38000.
**Version note:** Microsoft 365, 2021, 2024 (Microsoft Support, "SORT function").
**Edge cases:** Ties keep their original relative order (from memory, unverified). Numbers stored as text sort as text.
**Likely follow-ups:** 1) *Two sort columns?* `=SORT(A2:C9,{2,3},{1,-1})` (from memory, unverified) or SORTBY (Q35). 2) *Sort across columns?* by_col TRUE.
**Common mistakes:** Giving a column letter or a sheet column number (like 3 when the array starts at column B); mixing up 1 and -1.

### Q8 ⭐⭐ 🟢 How do you produce an alphabetically sorted list of unique departments from a column?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you nest two dynamic functions.
**Say this in the interview:** "I wrap UNIQUE inside SORT: `=SORT(UNIQUE(B2:B9))`. UNIQUE removes repeats, SORT puts the result in A to Z order."
**Explain simply:**
- Read it inside out: first UNIQUE, then SORT.
- With one column, SORT needs no other arguments; the default is ascending.
- It stays up to date when new departments appear.
**Example:** Departments appear as HR, Sales, IT, HR, Sales, IT, Sales, HR; the neat list is HR, IT, Sales.
**Sample sheet:**

| | B |
|---|---|
| 1 | Dept |
| 2 | HR |
| 3 | Sales |
| 4 | IT |
| 5 | HR |
| 6 | Sales |
| 7 | IT |
| 8 | Sales |
| 9 | HR |

**Formula / Steps:** `=SORT(UNIQUE(B2:B9))`
**Alternative:** `=UNIQUE(SORT(B2:B9))` gives the same list.
**Result:** Not run here (expected result reproduced with pandas): `sorted(df.Dept.unique())` printed `['HR', 'IT', 'Sales']`.
**Version note:** Both functions need Microsoft 365, 2021 or 2024.
**Edge cases:** Blanks sort and appear as 0 or blank entries; remove them with FILTER first (Q34).
**Likely follow-ups:** 1) *Z to A?* `=SORT(UNIQUE(B2:B9),,-1)`. 2) *Use in a drop-down?* Yes (Q25).
**Common mistakes:** Sorting first and expecting UNIQUE to re-sort; reversing the nesting order and misreading the error.

### Q9 ⭐⭐ 🟢 How do you count the number of distinct values in a column using dynamic array functions?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you combine UNIQUE with a counting function.
**Say this in the interview:** "`=COUNTA(UNIQUE(B2:B9))`. UNIQUE builds the list of different values and COUNTA counts how many items are in it. `ROWS(UNIQUE(...))` works too."
**Explain simply:**
- *Distinct* means each different value counted once, however many times it appears.
- COUNTA counts non-empty cells (Microsoft Support, "COUNTA function").
- If the column contains blanks, UNIQUE returns one blank (shown as 0), which would add 1 to the count. Remove blanks with FILTER first.
**Example:** 8 employees across 3 departments, so the answer is 3.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Employee | Dept | Salary |
| 2 | Asha | HR | 42000 |
| 3 | Ravi | Sales | 55000 |
| 4 | Meena | IT | 72000 |
| 5 | Karan | HR | 38000 |
| 6 | Priya | Sales | 61000 |
| 7 | Dev | IT | 68000 |
| 8 | Sana | Sales | 48000 |
| 9 | Tara | HR | 51000 |

**Formula / Steps:** `=COUNTA(UNIQUE(B2:B9))`. Blank-safe: `=COUNTA(UNIQUE(FILTER(B2:B9,B2:B9<>"")))`.
**Alternative (works in any version):** `=SUMPRODUCT(1/COUNTIF(B2:B9,B2:B9))`.
**Result:** UNIQUE version not run here (expected result reproduced with pandas): `df.Dept.nunique()` printed 3. The alternative was run in LibreOffice 24.2: 3.
**Version note:** UNIQUE: Microsoft 365, 2021, 2024. SUMPRODUCT/COUNTIF work in every version.
**Edge cases:** The SUMPRODUCT trick returns #DIV/0! if the range has blank cells (from memory, unverified). Text with different spacing counts as different values.
**Likely follow-ups:** 1) *Distinct but only for Sales?* `=COUNTA(UNIQUE(FILTER(...)))`. 2) *Pivot way?* Add to Data Model and use Distinct Count (from memory, unverified).
**Common mistakes:** Using COUNT (counts numbers only) on text; forgetting blanks; selecting the header.

### Q10 ⭐⭐ 🟢 What is the if_empty argument of FILTER for, and what error appears if you leave it out and nothing matches?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the specific error name and how to prevent it.
**Say this in the interview:** "if_empty is what FILTER shows when no row passes the test. If I leave it out and nothing matches, Excel returns #CALC!, because it does not support empty arrays. Many people expect #N/A, which is what Google Sheets gives."
**Explain simply:**
- Microsoft Support, "FILTER function": without if_empty, no result gives #CALC! "as Excel does not currently support empty arrays"; supplying `""` or a message avoids it.
- Google Sheets' FILTER has no if_empty argument and returns #N/A when nothing matches (Google Docs Editors Help, "FILTER").
- Good messages are specific: "No exits this quarter".
**Example:** Looking for employees who left in "Finance" when nobody did: with the message you see "None"; without it, #CALC!.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | Employee | Dept |
| 2 | Asha | HR |
| 3 | Ravi | Sales |
| 4 | Meena | IT |

**Formula / Steps:** `=FILTER(A2:B4,B2:B4="Finance","None")` shows None; `=FILTER(A2:B4,B2:B4="Finance")` shows #CALC!.
**Alternative:** `=IFERROR(FILTER(A2:B4,B2:B4="Finance"),"None")`, but that hides every other error too.
**Result:** Not run here. Expected: pandas `df[df.Dept=='Finance']` returned 0 rows, which in Excel is the empty case: "None" with if_empty, #CALC! without.
**Version note:** FILTER: Microsoft 365, 2021, 2024. The #CALC! error name is from the fetched Microsoft page.
**Edge cases:** If if_empty is `""`, the cell looks blank but is not empty, so COUNTA on it returns 1 (from memory, unverified).
**Likely follow-ups:** 1) *Can if_empty be a number?* Yes, such as 0. 2) *Is FILTER with #CALC! a bug?* No, it means empty result.
**Common mistakes:** Using IFERROR everywhere; expecting #N/A; writing the message without quotes.

### Q11 ⭐⭐ 🟢 When would you use FILTER instead of the AutoFilter on the Data tab?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand live formula output versus a manual view.
**Say this in the interview:** "AutoFilter is a quick way to look at data by hiding rows in the same sheet. I use FILTER when I want a separate result that updates by itself, can feed other formulas or a chart, and does not touch the original table."
**Explain simply:**
- AutoFilter (Data > Sort & Filter > Filter) hides rows in place; you must set it by hand and it only changes what you see.
- FILTER writes the matching rows somewhere else and keeps the source untouched.
- FILTER criteria can sit in cells (e.g. a department chosen from a drop-down), so a report can change without anyone touching the filter buttons.
- Pick AutoFilter for ad-hoc exploring, FILTER for reports and dashboards. If the audience uses 2016/2019, AutoFilter is the safe choice.
**Example:** A monthly headcount sheet needs a "Sales team" block that always shows current Sales employees. FILTER does it; AutoFilter would have to be re-applied each month.
**Formula / Steps:** AutoFilter: click inside the table > Data tab > Sort & Filter > Filter > open the arrow > untick all > tick HR. FILTER: `=FILTER(A2:C9,B2:B9=F1)` with the department in F1.
**Alternative:** Slicers on a Table, or a pivot table.
**Result:** No numeric result. Same HR rows (Asha, Karan, Tara) either way; pandas confirmed 3 HR rows.
**Version note:** AutoFilter works in all versions (from memory, unverified); FILTER needs 365/2021/2024.
**Edge cases:** AutoFilter results can be copied only as visible cells; FILTER output is formulas, so paste as values before sending if needed.
**Likely follow-ups:** 1) *Which updates automatically?* FILTER. 2) *Which is better for 2019 users?* AutoFilter.
**Common mistakes:** Forgetting AutoFilter hides rows (totals may still include them with SUM); building FILTER reports for people on old versions.

### Q12 ⭐⭐ 🟢 When would you use a pivot table instead of FILTER and UNIQUE formulas?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you tell listing rows from summarising numbers.
**Say this in the interview:** "FILTER and UNIQUE list or extract rows. A pivot table summarises: counts, sums and averages by group, with drag-and-drop and no formulas. If I need totals by department or a cross-tab, I use a pivot; if I need the actual matching rows, I use FILTER."
**Explain simply:**
- A *pivot table* is a tool (Insert > PivotTable) that groups data and calculates summaries.
- Pivot tables work in every desktop version and need a refresh when data changes (Data > Refresh All); formulas recalculate on their own.
- Pivots are better for big data and quick what-if grouping; dynamic array formulas are better when the result feeds other formulas.
**Example:** Headcount and pay by department: a pivot gives HR 3 people, Rs 131,000 total, average about Rs 43,667; IT 2, 140,000, 70,000; Sales 3, 164,000, about 54,667.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Employee | Dept | Salary |
| 2 | Asha | HR | 42000 |
| 3 | Ravi | Sales | 55000 |
| 4 | Meena | IT | 72000 |
| 5 | Karan | HR | 38000 |
| 6 | Priya | Sales | 61000 |
| 7 | Dev | IT | 68000 |
| 8 | Sana | Sales | 48000 |
| 9 | Tara | HR | 51000 |

**Formula / Steps:** Click in the data > Insert > PivotTable > OK; drag Dept to Rows, Employee (count) and Salary (sum, average) to Values. Formula equivalent: `=UNIQUE(B2:B9)` plus `SUMIFS`.
**Alternative:** `=GROUPBY` exists in newer 365, but I did not verify its availability, so I would not rely on it.
**Result:** A pivot table cannot run here. The grouped numbers were reproduced with pandas groupby: HR count 3, sum 131000, mean 43666.67; IT 2, 140000, 70000; Sales 3, 164000, 54666.67.
**Version note:** Pivot tables are in all desktop versions (from memory, unverified).
**Edge cases:** Pivots do not refresh automatically; blanks and text-numbers group wrongly.
**Likely follow-ups:** 1) *Can pivot and FILTER be combined?* Yes, GETPIVOTDATA or pivot slicers. 2) *Which for a dashboard?* Pivot plus slicers.
**Common mistakes:** Forgetting to refresh; using FILTER to total data; pivoting data with blank headers.

### Q13 ⭐⭐ 🟡 How do you filter rows that meet two conditions at the same time (for example Department = "Sales" and Salary greater than 50000)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know AND is a multiplication of tests inside FILTER.
**Say this in the interview:** "I multiply the two tests: `=FILTER(A2:C9,(B2:B9="Sales")*(C2:C9>50000),"No match")`. TRUE times TRUE is 1, anything else is 0, so only rows passing both are kept."
**Explain simply:**
- Each test gives a TRUE/FALSE per row; Excel treats TRUE as 1 and FALSE as 0 when you multiply.
- Brackets round each test are required.
- Do not use the AND function here: AND returns a single TRUE/FALSE for the whole range, not one per row (from memory, unverified).
**Example:** Sales staff paid more than 50,000: Ravi (55,000) and Priya (61,000); Sana (48,000) is excluded.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Employee | Dept | Salary |
| 2 | Asha | HR | 42000 |
| 3 | Ravi | Sales | 55000 |
| 4 | Meena | IT | 72000 |
| 5 | Karan | HR | 38000 |
| 6 | Priya | Sales | 61000 |
| 7 | Dev | IT | 68000 |
| 8 | Sana | Sales | 48000 |
| 9 | Tara | HR | 51000 |

**Formula / Steps:** `=FILTER(A2:C9,(B2:B9="Sales")*(C2:C9>50000),"No match")`
**Alternative:** `=FILTER(A2:C9,(B2:B9="Sales")*(C2:C9>50000))` without if_empty, or the older `SUMPRODUCT` for a count only.
**Result:** FILTER not run here (expected result reproduced with pandas): Ravi Sales 55000 (row 3), Priya Sales 61000 (row 6). Check run in LibreOffice 24.2: `=SUMPRODUCT((B2:B9="Sales")*(C2:C9>50000))` returned 2.
**Version note:** FILTER needs Microsoft 365, 2021 or 2024.
**Edge cases:** Text-numbers (such as "55000" typed as text) fail the `>` test (from memory, unverified).
**Likely follow-ups:** 1) *Three conditions?* Multiply a third bracket. 2) *OR instead?* Add (Q14).
**Common mistakes:** Using `&` or AND; missing brackets so operator order breaks; mismatched range sizes.

### Q14 ⭐⭐ 🟡 How do you filter rows that meet either of two conditions (OR logic) with FILTER?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know OR is addition of tests.
**Say this in the interview:** "I add the tests: `=FILTER(A2:C9,(B2:B9="HR")+(C2:C9>65000),"No match")`. A row is kept if the sum is 1 or more."
**Explain simply:**
- TRUE + FALSE = 1 and FALSE + FALSE = 0. FILTER treats any non-zero value as TRUE.
- If both are TRUE the sum is 2; the row is still kept once.
- For many values in one column, `ISNUMBER(MATCH(B2:B9,{"HR","IT"},0))` is shorter (from memory, unverified).
**Example:** List everyone in HR or anyone paid above 65,000: the 3 HR staff plus Meena and Dev.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Employee | Dept | Salary |
| 2 | Asha | HR | 42000 |
| 3 | Ravi | Sales | 55000 |
| 4 | Meena | IT | 72000 |
| 5 | Karan | HR | 38000 |
| 6 | Priya | Sales | 61000 |
| 7 | Dev | IT | 68000 |
| 8 | Sana | Sales | 48000 |
| 9 | Tara | HR | 51000 |

**Formula / Steps:** `=FILTER(A2:C9,(B2:B9="HR")+(C2:C9>65000),"No match")`
**Alternative:** Combine two FILTERs with VSTACK (365/2024, not verified here), or helper column with OR().
**Result:** FILTER not run here (expected result reproduced with pandas): Asha 42000, Meena 72000, Karan 38000, Dev 68000, Tara 51000 (5 rows). A count check was run in LibreOffice 24.2: `=SUMPRODUCT(--((B2:B9="HR")+(C2:C9>65000)>0))` returned 5.
**Version note:** Microsoft 365, 2021, 2024.
**Edge cases:** Rows meeting both conditions are not duplicated; no row did here.
**Likely follow-ups:** 1) *AND and OR together?* Brackets: `(A)*((B)+(C))`. 2) *Why not OR()?* It collapses to one value.
**Common mistakes:** Using the OR function; adding without brackets.

### Q15 ⭐⭐ 🟡 What is the difference between SORT and SORTBY, and when do you need SORTBY?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know SORTBY can sort by a column that is not in the output.
**Say this in the interview:** "SORT picks the sort column by its position number inside the array. SORTBY takes the actual range to sort by, so it can sort by a column you are not returning, and it keeps working if columns are added."
**Explain simply:**
- Syntax: `=SORTBY(array, by_array1, [sort_order1], [by_array2, sort_order2], …)` (Microsoft Support, "SORTBY function").
- SORT uses a column index, so it can break if columns are inserted; Microsoft recommends SORTBY for data in the grid (Microsoft Support, "SORT function").
- SORTBY allows several sort columns and an independent order for each.
**Example:** Show only names, ranked by salary.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Employee | Dept | Salary |
| 2 | Asha | HR | 42000 |
| 3 | Ravi | Sales | 55000 |
| 4 | Meena | IT | 72000 |
| 5 | Karan | HR | 38000 |
| 6 | Priya | Sales | 61000 |
| 7 | Dev | IT | 68000 |
| 8 | Sana | Sales | 48000 |
| 9 | Tara | HR | 51000 |

**Formula / Steps:** `=SORTBY(A2:A9,C2:C9,-1)`
**Alternative:** `=INDEX(SORT(A2:C9,3,-1),,1)` returns the same names.
**Result:** Not run here (expected result reproduced with pandas): Meena, Dev, Priya, Ravi, Tara, Sana, Asha, Karan.
**Version note:** Both need Microsoft 365, 2021 or 2024.
**Edge cases:** by_array must have the same number of rows as array.
**Likely follow-ups:** 1) *Two keys?* Q35. 2) *Which is shorter for sorting a whole table by one column?* SORT.
**Common mistakes:** Giving SORTBY a column number; ranges of different lengths.

### Q16 ⭐⭐ 🟡 What is the spill range operator (#), and how do you use it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you refer to a growing list without typing its address.
**Say this in the interview:** "Putting # after the top-left cell of a spill, like `E2#`, refers to the entire spilled list, however long it is today. So `=COUNTA(E2#)` keeps counting correctly when the list grows."
**Explain simply:**
- Microsoft Support, "Spilled range operator": `=SUM(A2#)` equals `=SUM(A2:A11)` when A2 holds `=SEQUENCE(10)` and spills to A2:A11, and it adjusts if the spill changes.
- Use it only on a cell that holds a spilling formula.
- It does not support closed workbooks: it returns #REF! (same page).
**Example:** E2 holds `=UNIQUE(B2:B9)` (3 departments). `=COUNTA(E2#)` returns 3.
**Sample sheet:**

| | B | E | F |
|---|---|---|---|
| 1 | Dept | Unique | Count |
| 2 | HR | HR | `=COUNTA(E2#)` |
| 3 | Sales | Sales | |
| 4 | IT | IT | |

**Formula / Steps:** `=COUNTA(E2#)`; `=SORT(E2#)`; or select the whole spill via Go To (F5) and type `E2#`.
**Alternative:** A fixed range `E2:E4`, which does not grow.
**Result:** Not run here (expected result reproduced with pandas): `len(df.Dept.unique())` printed 3.
**Version note:** The Microsoft page applies to Microsoft 365 (and Mac); the other pages list 2021/2024 for dynamic arrays.
**Edge cases:** If the source cell shows #SPILL!, the # reference errors too.
**Likely follow-ups:** 1) *Use in a drop-down?* Yes (Q25). 2) *In a chart?* Through a named range (Q45).
**Common mistakes:** Putting # after a non-spilling cell; using it in a closed workbook reference.

### Q17 ⭐⭐ 🟡 How does FILTER help when you need to return all matching rows, where VLOOKUP or XLOOKUP return only the first match?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know lookups stop at the first match.
**Say this in the interview:** "VLOOKUP and XLOOKUP return one answer, the first they find. FILTER returns every row that matches, so for 'all employees in HR' I use FILTER."
**Explain simply:**
- A lookup answers "what is the value for this key?"; one key, one answer.
- FILTER answers "give me every row where...".
- XLOOKUP is also not in 2016/2019 (Microsoft Support, "XLOOKUP function").
**Example:** Three HR employees exist; a lookup for "HR" finds only Asha.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | Employee | Dept |
| 2 | Asha | HR |
| 3 | Ravi | Sales |
| 4 | Meena | IT |
| 5 | Karan | HR |
| 6 | Priya | Sales |
| 7 | Dev | IT |
| 8 | Sana | Sales |
| 9 | Tara | HR |

**Formula / Steps:** All matches: `=FILTER(A2:A9,B2:B9="HR")`. First match only: `=INDEX(A2:A9,MATCH("HR",B2:B9,0))`.
**Alternative:** Join the names into one cell with TEXTJOIN (Q21).
**Result:** FILTER not run here (expected result reproduced with pandas): Asha, Karan, Tara. The first-match formula was run in LibreOffice 24.2 and returned Asha.
**Version note:** FILTER: 365/2021/2024; INDEX/MATCH: all versions.
**Edge cases:** No match: FILTER gives #CALC! unless if_empty; lookups give #N/A.
**Likely follow-ups:** 1) *Can XLOOKUP return several?* Only several columns of the first match. 2) *Older Excel?* INDEX/SMALL (Q43).
**Common mistakes:** Expecting VLOOKUP to list all matches; sorting in the hope that a lookup finds the right one.

### Q18 ⭐⭐ 🟡 What is the LET function, what is its syntax, and why would you use it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you name values inside a formula and explain the benefit.
**Say this in the interview:** "LET lets me give names to values or calculations inside a formula: `=LET(name1, value1, ..., final_calculation)`. It makes long formulas easier to read, and a repeated calculation is written once."
**Explain simply:**
- Syntax (Microsoft Support, "LET function"): `=LET(name1, name_value1, calculation_or_name2, [name_value2, calculation_or_name3...])`.
- The last item is the calculation that returns the result.
- Names work like temporary variables that exist only inside that formula.
- Speed benefit: I recall Microsoft says LET can improve performance by calculating once; I did not see that on the page I read, so treat it as from memory, unverified.
**Example:** Employees paid above the average salary. The average of the 8 salaries is 54,375, so the result is Ravi, Meena, Priya, Dev.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Employee | Dept | Salary |
| 2 | Asha | HR | 42000 |
| 3 | Ravi | Sales | 55000 |
| 4 | Meena | IT | 72000 |
| 5 | Karan | HR | 38000 |
| 6 | Priya | Sales | 61000 |
| 7 | Dev | IT | 68000 |
| 8 | Sana | Sales | 48000 |
| 9 | Tara | HR | 51000 |

**Formula / Steps:** `=LET(avg,AVERAGE(C2:C9),FILTER(A2:A9,C2:C9>avg))`
**Alternative:** `=FILTER(A2:A9,C2:C9>AVERAGE(C2:C9))`, same result, no LET.
**Result:** LET not run here (expected result reproduced with pandas): mean 54375.0, above-average employees `['Ravi', 'Meena', 'Priya', 'Dev']`. The average alone was run in LibreOffice 24.2: 54375.
**Version note:** LET: Microsoft 365, 2021, 2024 (Microsoft Support, "LET function"); not 2019.
**Edge cases:** A name cannot look like a cell address (Q31).
**Likely follow-ups:** 1) *How many names?* Up to 126 pairs (Q31). 2) *Can names be reused?* Later names can use earlier ones.
**Common mistakes:** Forgetting the final calculation; using names like "c" or "r1"; a name that starts with a number.

### Q19 ⭐⭐ 🟡 What does the exactly_once argument of UNIQUE do? Give a practical example.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know it returns values that occur once, not "distinct".
**Say this in the interview:** "With exactly_once set to TRUE, UNIQUE returns only the values that appear a single time in the list; anything repeated is dropped entirely. For example, which employees attended only one training session."
**Explain simply:**
- Microsoft Support, "UNIQUE function": TRUE returns only rows or columns that occur once, "the database concept of unique". FALSE/omitted returns each different value once.
- Normal UNIQUE keeps one copy of repeated values; exactly_once removes them completely.
- Syntax: `=UNIQUE(array,FALSE,TRUE)` (by_col FALSE).
**Example:** Training log of 7 rows: E101 three times, E102 twice, E103 once, E104 once.
**Sample sheet:**

| | A |
|---|---|
| 1 | EmpID (training log) |
| 2 | E101 |
| 3 | E102 |
| 4 | E101 |
| 5 | E103 |
| 6 | E102 |
| 7 | E104 |
| 8 | E101 |

**Formula / Steps:** `=UNIQUE(A2:A8,FALSE,TRUE)`
**Alternative:** `=FILTER(A2:A8,COUNTIF(A2:A8,A2:A8)=1)`.
**Result:** Not run here (expected result reproduced with pandas): plain unique `['E101','E102','E103','E104']`; exactly once `['E103','E104']`.
**Version note:** UNIQUE: 365/2021/2024.
**Edge cases:** If every value repeats, the result is empty and Excel shows #CALC! (same empty-array behaviour as FILTER; from memory, unverified). Wrap it with IFERROR.
**Likely follow-ups:** 1) *by_col?* Compares columns. 2) *Values appearing more than once?* FILTER with COUNTIF>1.
**Common mistakes:** Thinking TRUE means "distinct"; omitting the middle FALSE.

### Q20 ⭐⭐ 🟡 How do you sum or average the values returned by FILTER, and when is SUM(FILTER(...)) better or worse than SUMIFS?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know when each approach fits.
**Say this in the interview:** "I wrap FILTER inside SUM or AVERAGE: `=SUM(FILTER(C2:C9,B2:B9="Sales",0))`. For simple conditions SUMIFS is shorter and works in every version, so I use that. FILTER is better with complex logic or when I also need the list."
**Explain simply:**
- FILTER returns the matching numbers; SUM adds them.
- Use 0 as if_empty for SUM so an empty result gives 0 rather than an error.
- SUMIFS is limited to simple conditions on ranges; FILTER can use any formula-based test.
**Example:** Sales department payroll: 55,000 + 61,000 + 48,000 = 164,000 and average 54,666.67.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Employee | Dept | Salary |
| 2 | Asha | HR | 42000 |
| 3 | Ravi | Sales | 55000 |
| 4 | Meena | IT | 72000 |
| 5 | Karan | HR | 38000 |
| 6 | Priya | Sales | 61000 |
| 7 | Dev | IT | 68000 |
| 8 | Sana | Sales | 48000 |
| 9 | Tara | HR | 51000 |

**Formula / Steps:** `=SUM(FILTER(C2:C9,B2:B9="Sales",0))`; `=IFERROR(AVERAGE(FILTER(C2:C9,B2:B9="Sales")),0)`
**Alternative:** `=SUMIFS(C2:C9,B2:B9,"Sales")` and `=AVERAGEIFS(C2:C9,B2:B9,"Sales")`.
**Result:** FILTER versions not run here (expected result reproduced with pandas): sum 164000, mean 54666.67. SUMIFS run in LibreOffice 24.2: 164000; AVERAGEIFS: 54666.6666666667.
**Version note:** SUMIFS: all current versions (from memory, unverified); FILTER: 365/2021/2024.
**Edge cases:** AVERAGE of an empty result is an error; use IFERROR or if_empty. SUMIFS ignores case; FILTER's `=` also does (from memory, unverified).
**Likely follow-ups:** 1) *Which is faster on huge data?* SUMIFS (from memory, unverified). 2) *When is FILTER better?* Complex tests, e.g. above the average.
**Common mistakes:** Forgetting if_empty; using FILTER where SUMIFS would do.

### Q21 ⭐⭐ 🟡 How do you join all employee names in a department into one cell, separated by commas?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you combine FILTER with TEXTJOIN.
**Say this in the interview:** "`=TEXTJOIN(", ",TRUE,FILTER(A2:A9,B2:B9="HR",""))`. FILTER finds the HR names and TEXTJOIN glues them together with a comma and space."
**Explain simply:**
- TEXTJOIN(delimiter, ignore_empty, text1, ...) joins text with a separator (Microsoft Support, "TEXTJOIN function").
- ignore_empty TRUE skips blank items.
- Result is one text cell, not a list.
**Example:** HR team names in one cell for an email: Asha, Karan, Tara.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | Employee | Dept |
| 2 | Asha | HR |
| 3 | Ravi | Sales |
| 4 | Meena | IT |
| 5 | Karan | HR |
| 6 | Priya | Sales |
| 7 | Dev | IT |
| 8 | Sana | Sales |
| 9 | Tara | HR |

**Formula / Steps:** `=TEXTJOIN(", ",TRUE,FILTER(A2:A9,B2:B9="HR",""))`
**Alternative (Excel 2019 too):** array formula entered with Ctrl+Shift+Enter: `=TEXTJOIN(", ",TRUE,IF(B2:B9="HR",A2:A9,""))`.
**Result:** FILTER version not run here (expected result reproduced with pandas): `Asha, Karan, Tara`. The alternative was run in LibreOffice 24.2 as an array formula and returned `Asha, Karan, Tara`.
**Version note:** TEXTJOIN is listed for 365, 2024, 2021 and 2019 (Microsoft Support); not 2016.
**Edge cases:** Results over 32,767 characters give #VALUE! (from memory, unverified). Department with no match gives an empty cell.
**Likely follow-ups:** 1) *Sorted names?* Wrap FILTER in SORT. 2) *One cell per department?* LET plus MAP, 365 only (not verified).
**Common mistakes:** Using & with a range; forgetting the quotes round the delimiter; CSE in 2019.

### Q22 ⭐⭐ 🟡 What is the @ (implicit intersection) operator that Excel sometimes adds to a formula?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know why old formulas show @ in new Excel.
**Say this in the interview:** "@ marks the place where old Excel would quietly pick one value from a range or array, called implicit intersection. New Excel shows it so you can see it. Formulas calculate the same as before; removing @ may make the result spill."
**Explain simply:**
- Implicit intersection: for a range, it returns the value in the same row or column as the formula; for an array, the top-left value (Microsoft Support, "Implicit intersection operator: @").
- Excel adds @ to older formulas using functions that can return ranges, such as INDEX, OFFSET and user-defined functions.
- If what follows @ returns a single value, removing it changes nothing; if it returns a range, the result spills.
- In structured references `[@Column]` means "this row" in a Table.
**Example:** An old workbook has `=@INDEX(A2:A9,1)`; it is the same single value as before.
**Formula / Steps:** Edit the formula and delete `@` if you want the whole list to spill.
**Alternative:** Keep `@` to force one value (for example `=VLOOKUP(@A:A,A:C,2,FALSE)` to avoid #SPILL!, per Microsoft's #SPILL! page).
**Result:** Not a calculation question, nothing to run.
**Version note:** The page applies to Microsoft 365, 2024 and 2021. In older versions, @ appears as `_xlfn.SINGLE()` and returns #NAME? (Microsoft Support).
**Edge cases:** If you remove an auto-added @ and open in an older version, the formula shows as a legacy array formula in braces (Microsoft Support).
**Likely follow-ups:** 1) *Does @ change my results?* No. 2) *Why #SPILL! after removing it?* The result now needs room.
**Common mistakes:** Deleting @ without checking space; typing @ everywhere.

### Q23 ⭐⭐ 🟡 Can you use a spilling formula inside an Excel Table? What do you do instead?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know a Table limitation.
**Say this in the interview:** "No. Spilled array formulas are not supported inside Excel Tables, and give #SPILL!. I put the formula in a normal cell outside the table, pointing at the table's columns, or I use single-value formulas inside the table."
**Explain simply:**
- Microsoft Support, "Dynamic array formulas and spilled array behavior": spilled array formulas are not supported in Excel tables themselves; put them in the grid outside the table.
- The #SPILL! page also offers Table Design > Convert to range if you need the formula inside.
- Reading from a table is fine: `=FILTER(Employees[[Employee]:[Salary]],Employees[Dept]="HR")` placed outside is a normal pattern (from memory, unverified).
**Example:** Table Employees in A1:C9. Put the HR list in E2, outside the table; new rows added to the table are picked up.
**Sample sheet:**

| | A | B | C | D | E |
|---|---|---|---|---|---|
| 1 | Employee | Dept | Salary | | HR list |
| 2 | Asha | HR | 42000 | | (formula) |
| 3 | Ravi | Sales | 55000 | | |

**Formula / Steps:** Click a blank cell outside the table and enter the formula. To convert: click in the table > Table Design > Tools > Convert to Range.
**Alternative:** Inside the table, use per-row formulas such as `=IF([@Dept]="HR",[@Salary],"")`.
**Result:** Not run here (a Table behaviour; taken from the Microsoft pages).
**Version note:** Applies wherever dynamic arrays exist: 365, 2021, 2024.
**Edge cases:** A formula placed right next to a table can block the table growing.
**Likely follow-ups:** 1) *Why not convert to a range?* You lose table features such as auto-expansion. 2) *Can a table column refer to a spill?* Yes with `E2#`.
**Common mistakes:** Typing the formula in the table's header row; leaving no free space under the formula.

### Q24 ⭐⭐ 🟡 HR scenario: from a monthly attendance log with one row per employee per absence, how do you list the employees who were absent more than three times?
**Asked at:** commonly asked (no company-specific report found); HR-flavoured scenario written for this book.
**What the interviewer is checking:** Can you count how often each name appears, then keep only the names above a limit?
**Say this in the interview:** "Each row is one absence, so I first get the unique names, count how many rows each name has, and keep the names with a count above 3. In 365 that is one formula with UNIQUE, COUNTIF and FILTER."
**Explain simply:**
- *UNIQUE* gives each name once. *COUNTIF* counts how many rows match a name. *FILTER* keeps only rows where a test is TRUE.
- *LET* (a function that gives a name to a calculation so you can reuse it) keeps the formula readable.
- "More than three" means the test is `>3`, so exactly 3 absences is not listed.
**Example:** September log of 11 absence rows. Asha has 4, Meena 4, Ravi 2, Karan 1. Flagged: Asha and Meena.
**Sample sheet:**

| | A (Employee) | B (AbsenceDate) |
|---|---|---|
| 2 | Asha | 01-Sep-2026 |
| 3 | Ravi | 02-Sep-2026 |
| 4 | Asha | 08-Sep-2026 |
| 5 | Meena | 09-Sep-2026 |
| 6 | Asha | 15-Sep-2026 |
| 7 | Karan | 16-Sep-2026 |
| 8 | Meena | 17-Sep-2026 |
| 9 | Asha | 22-Sep-2026 |
| 10 | Ravi | 23-Sep-2026 |
| 11 | Meena | 24-Sep-2026 |
| 12 | Meena | 29-Sep-2026 |

**Formula / Steps:** `=LET(e,UNIQUE(A2:A12),n,COUNTIF(A2:A12,e),FILTER(e,n>3,"Nobody above 3"))`
**Alternative:** Works in every version: helper column C `=COUNTIF($A$2:$A$12,A2)`, then D `=IF(AND(C2>3,COUNTIF($A$2:A2,A2)=1),A2,"")` (shows each flagged name once). Or a PivotTable: Employee in Rows, count of AbsenceDate in Values, filter Count > 3.
**Result:** Dynamic formula: not run here (expected result reproduced with pandas): `['Asha', 'Meena']`. Helper-column alternative run in LibreOffice 24.2: counts 4,2,4,4,4,1,4,4,2,4,4 for rows 2-12, and column D shows "Asha" (row 2) and "Meena" (row 5) only.
**Version note:** FILTER, UNIQUE, LET need Excel 365, 2021 or 2024 (Microsoft Support, "FILTER function", "UNIQUE function", "LET function"). Excel 2016/2019: use the helper column or PivotTable.
**Edge cases:** Names with different spelling or trailing spaces count separately (TRIM first). If nobody qualifies, the third FILTER argument shows the message instead of an error. Count rows, not distinct days, if one person can have two rows on the same date.
**Likely follow-ups:** 1) *Absent 3 or more?* Use `>=3`. 2) *Count only unauthorised absences?* Use COUNTIFS with a Type column.
**Common mistakes:** Using FILTER on the raw column, which returns every row instead of each person once; writing `>=3`; forgetting to count inside the right month.

### Q25 ⭐⭐ 🟡 How do you create a dependent or dynamic drop-down list that updates automatically from a UNIQUE formula?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know how to point Data Validation at a spilled range so the list grows by itself?
**Say this in the interview:** "I put `=SORT(UNIQUE(...))` in a helper cell, then in Data Validation choose List and type the cell address followed by `#`, which means 'the whole spilled range'. When new departments appear, the drop-down grows."
**Explain simply:**
- *Data Validation* is the feature that restricts a cell to a list. The `#` (spill range operator) means "everything this formula spilled into".
- *Dependent* drop-down: a second list that depends on the first choice, built with FILTER on the chosen value.
**Example:** Column B of an employee sheet has departments with a blank row. List cell F2 holds the cleaned list; cell E2 has the drop-down.
**Sample sheet:**

| | A (Employee) | B (Dept) |
|---|---|---|
| 2 | Asha | HR |
| 3 | Ravi | IT |
| 4 | Meena | HR |
| 5 | Karan | Finance |
| 6 | (blank) | (blank) |
| 7 | Divya | IT |

**Formula / Steps:**
1. In F2 enter `=SORT(UNIQUE(FILTER(B2:B100,B2:B100<>"")))` (FILTER removes blanks first).
2. Click E2. Ribbon: Data tab > Data Tools group > Data Validation.
3. Allow: List. Source: `=$F$2#`. OK.
4. Dependent list: in H2 `=SORT(FILTER(A2:A100,B2:B100=E2,"None"))`, and its Data Validation source `=$H$2#`.
**Alternative:** Excel Table plus a named range pointing at the column (no spill needed, but duplicates remain), or a pre-365 `OFFSET`/`COUNTA` named range.
**Result:** Not run here (dynamic arrays and Data Validation). Expected list reproduced with pandas: `['Finance', 'HR', 'IT']`; without removing blanks UNIQUE would also return a blank entry (pandas: `['HR','IT','Finance',nan]`).
**Version note:** Spill functions: 365/2021/2024 (Microsoft Support, "UNIQUE function"). Using `#` inside the Data Validation source is from memory, unverified.
**Edge cases:** If something blocks the spill, F2 shows #SPILL! and the list breaks. A text-then-blank problem: UNIQUE returns 0 for blank cells unless removed. Never put the list inside an Excel Table (spills are not supported in tables, Microsoft Support, "Dynamic array formulas and spilled array behavior").
**Likely follow-ups:** 1) *Why not type the list?* It never updates. 2) *Where to keep the list?* On a hidden Lists sheet.
**Common mistakes:** Typing `F2:F10` instead of `F2#`; leaving blanks in the source; placing the helper in a Table.

### Q26 ⭐ 🟢 Name the dynamic array functions Microsoft introduced (FILTER, SORT, SORTBY, UNIQUE, SEQUENCE, RANDARRAY, XLOOKUP, XMATCH) and give one use for each.
**Asked at:** commonly asked (no company-specific report found); function lists like this appear in community interview lists (research note for this part, snippet only).
**What the interviewer is checking:** Do you know what each new function is for?
**Say this in the interview:** "FILTER keeps matching rows, SORT and SORTBY order them, UNIQUE removes duplicates, SEQUENCE makes number lists, RANDARRAY makes random numbers, and XLOOKUP and XMATCH are modern lookups."
**Explain simply:**
- FILTER: list all employees in HR. SORT: order by salary. SORTBY: order a table by a column you do not display. UNIQUE: list departments once.
- SEQUENCE: numbers 1-12 or month dates. RANDARRAY: random numbers, e.g. for sampling.
- XLOOKUP: look up a value and return the matching value from another column. XMATCH: return the position of an item.
- Premise note: XLOOKUP and XMATCH are lookup functions that *can* return arrays; I believe they arrived later than the first group (from memory, unverified).
**Example:** `=SEQUENCE(5,1,1001,1000)` gives 1001, 2001, 3001, 4001, 5001 (Microsoft's own GL-code example).
**Sample sheet / Result:** Not run here (expected result reproduced with pandas): `[1001, 2001, 3001, 4001, 5001]`.
**Formula / Steps:** `=FILTER(...)`, `=SORT(...)`, `=SORTBY(...)`, `=UNIQUE(...)`, `=SEQUENCE(rows,[columns],[start],[step])`, `=RANDARRAY([rows],[columns],[min],[max],[whole_number])`, `=XLOOKUP(...)`, `=XMATCH(lookup_value,lookup_array,[match_mode],[search_mode])`.
**Alternative:** Old equivalents: AutoFilter or Advanced Filter, Sort button, Remove Duplicates, ROW(), RAND(), VLOOKUP, MATCH.
**Version note:** FILTER, SORT, SORTBY, UNIQUE, SEQUENCE, RANDARRAY, XMATCH: Excel 365, 2024, 2021 (Microsoft Support pages for each). XLOOKUP: I fetched its page but its availability text was ambiguous, so "365/2021, not 2016/2019" is from memory, unverified.
**Edge cases:** In Excel 2016/2019 they show #NAME? (from memory, unverified).
**Likely follow-ups:** 1) *Which is the most useful?* FILTER. 2) *Is SORT the same as the Sort button?* No, the formula leaves the source untouched.
**Common mistakes:** Believing they work in Excel 2019; mixing up SORT (column number) and SORTBY (range).

### Q27 ⭐ 🟢 How do you generate a list of numbers 1 to 12, or the 12 month-start dates of a year, using SEQUENCE?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know SEQUENCE's four arguments and how to turn numbers into dates?
**Say this in the interview:** "`=SEQUENCE(12)` gives 1 to 12. For month starts I wrap it in DATE: `=DATE(2026,SEQUENCE(12),1)` and format as dates."
**Explain simply:**
- Syntax `=SEQUENCE(rows,[columns],[start],[step])`; missing optional arguments default to 1 (Microsoft Support, "SEQUENCE function").
- `DATE(year,month,day)` accepts a month number, so 12 month numbers give 12 dates.
- Excel stores dates as serial numbers, so format the result as a date or you will see numbers like 46023.
**Example:** A payroll calendar needing 1-Jan-2026 to 1-Dec-2026.
**Sample sheet:**

| | A |
|---|---|
| 1 | `=DATE(2026,SEQUENCE(12),1)` |
| 2 | (spills down to row 12) |

**Formula / Steps:** `=SEQUENCE(12)` or across `=SEQUENCE(1,12)`; dates: `=DATE(2026,SEQUENCE(12),1)`, then Home > Number > Short Date.
**Alternative:** `=EDATE(DATE(2026,1,1),SEQUENCE(12,1,0))`, or in older Excel type 1 and 2, drag the fill handle.
**Result:** SEQUENCE: not run here (expected result reproduced with pandas): 1..12 and 01-Jan-2026 ... 01-Dec-2026 (pandas `date_range(freq='MS')`). The same DATE(2026,n,1) logic was run in LibreOffice cell by cell for n=1..12 and gave 01-Jan-2026 through 01-Dec-2026.
**Version note:** SEQUENCE: 365/2021/2024 (Microsoft Support, "SEQUENCE function"). DATE and EDATE work in all versions.
**Edge cases:** Month 13 rolls into next year; leap years are handled by DATE.
**Likely follow-ups:** 1) *Month names?* `=TEXT(DATE(2026,SEQUENCE(12),1),"mmm")`. 2) *Last day of month?* `=EOMONTH(DATE(2026,SEQUENCE(12),1),0)`.
**Common mistakes:** Forgetting date formatting; hard-coding the year; putting something in the cells below, causing #SPILL!.

### Q28 ⭐ 🟢 Does UNIQUE treat "HR" and "hr" as the same value?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you test edge cases instead of assuming?
**Say this in the interview:** "As far as I know it ignores capital letters, so HR and hr count as one, and it keeps the first spelling. Microsoft's page does not say, so I would test it. It does treat 'HR ' with a trailing space as different."
**Explain simply:**
- Microsoft's UNIQUE page makes no statement about case sensitivity (fetched). The case-insensitive behaviour is from memory, unverified; Excel's `=` comparison also ignores case.
- Spaces are real characters, so "HR" and "HR " are different. Clean with TRIM.
**Example:** Values HR, hr, Finance, "HR ", IT.
**Sample sheet:**

| | A |
|---|---|
| 1 | HR |
| 2 | hr |
| 3 | Finance |
| 4 | HR (trailing space) |
| 5 | IT |

**Formula / Steps:** `=UNIQUE(A1:A5)`; cleaned: `=UNIQUE(TRIM(A1:A5))`.
**Alternative:** Case-sensitive uniqueness needs a helper using EXACT, or a different tool (Power Query is case-sensitive by default, from memory, unverified).
**Result:** Not run here (expected result reproduced with pandas): case-insensitive, Excel-like: `['HR','Finance','HR ','IT']`; with TRIM too: `['HR','Finance','IT']`. For contrast, pandas `drop_duplicates()` is case-sensitive and returns all 5.
**Version note:** UNIQUE: 365/2021/2024 (Microsoft Support, "UNIQUE function").
**Edge cases:** Non-breaking spaces from system exports survive TRIM; use SUBSTITUTE(x,CHAR(160),"").
**Likely follow-ups:** 1) *Which spelling is returned?* The first (from memory). 2) *How would you standardise?* PROPER/UPPER plus TRIM.
**Common mistakes:** Assuming pandas and Excel behave alike; ignoring trailing spaces.

### Q29 ⭐ 🟢 Do FILTER, UNIQUE and SORT work in Google Sheets, and what Sheets function is often used instead?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the tool differences if the team uses Sheets?
**Say this in the interview:** "Yes, Sheets has FILTER, UNIQUE and SORT, and they spill the same way. Sheets also has QUERY, which works like a small SQL statement, and ARRAYFORMULA to apply a formula to a whole column."
**Explain simply:**
- Premise note: nothing needs replacing; the functions exist. QUERY is just a popular extra.
- QUERY: `=QUERY(A1:C11,"select A,C where B='HR' order by C desc",1)`, with 1 meaning one header row.
- Sheets facts here are from memory, unverified (I did not fetch Google Docs Editors Help).
**Example:** HR employees by salary descending, Sheets QUERY versus Excel `=SORT(FILTER(...),2,-1)`.
**Sample sheet:** Uses the 10-person employee table; HR rows are Asha 48000, Meena 52000, Imran 90000, Pooja 41000.
**Formula / Steps:** Excel: `=SORT(FILTER(A2:C11,B2:B11="HR"),3,-1)`; Sheets: `=QUERY(A1:C11,"select A,C where B='HR' order by C desc",1)`.
**Alternative:** In Sheets the sort order argument is TRUE/FALSE rather than 1/-1: `=SORT(FILTER(A2:C11,B2:B11="HR"),3,FALSE)` (from memory, unverified).
**Result:** Not run here (expected result reproduced with pandas): Imran 90000, Meena 52000, Asha 48000, Pooja 41000.
**Version note:** Sheets features are from memory, unverified.
**Edge cases:** QUERY needs consistent data types per column; mixed text and numbers can drop values (from memory).
**Likely follow-ups:** 1) *Does Sheets have LET?* I believe yes (unverified). 2) *Can Excel run QUERY?* No; use Power Query.
**Common mistakes:** Forgetting the header-count argument in QUERY; copying Excel's `-1` order into Sheets.

### Q30 ⭐ 🟡 What is the difference between legacy array formulas (Ctrl+Shift+Enter) and dynamic array formulas?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you read old workbooks and know the modern approach?
**Say this in the interview:** "Old array formulas needed Ctrl+Shift+Enter and showed curly braces; the result stayed in a fixed block. In 365 you just press Enter and the result spills as far as needed."
**Explain simply:**
- An *array formula* is one formula that works on many values at once.
- Legacy ones are still supported but Microsoft says not to use them; you convert them by re-entering in the top-left cell (Microsoft Support, "Dynamic array formulas and spilled array behavior").
- Dynamic formulas resize on their own; legacy ones keep the block you selected.
**Example:** Total salary of HR staff earning over 35,000.
**Sample sheet:**

| | A (Dept) | B (Salary) |
|---|---|---|
| 2 | HR | 40000 |
| 3 | IT | 60000 |
| 4 | HR | 55000 |
| 5 | Finance | 50000 |
| 6 | HR | 30000 |

**Formula / Steps:** Legacy: select cell, type `=SUM(IF((A2:A6="HR")*(B2:B6>35000),B2:B6))`, press Ctrl+Shift+Enter. Modern: same formula, Enter.
**Alternative:** `=SUMIFS(B2:B6,A2:A6,"HR",B2:B6,">35000")`, no array needed.
**Result:** Expected total 95,000 (40,000 + 55,000), confirmed with pandas. In LibreOffice I ran `=SUMPRODUCT((A2:A6="HR")*B2:B6)` = 125000 (all HR) and the row count with salary above 35,000 = 2.
**Version note:** Dynamic arrays: 365/2021/2024; CSE works everywhere.
**Edge cases:** Editing a legacy formula without CSE breaks it in old Excel.
**Likely follow-ups:** 1) *How do I see braces?* They mark legacy arrays. 2) *Best non-array option?* SUMIFS.
**Common mistakes:** Pressing only Enter in Excel 2016; fear of curly braces typed by hand (you cannot type them).

### Q31 ⭐ 🟡 What are the rules for naming variables inside LET, and how many name/value pairs can you define?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know LET syntax limits?
**Say this in the interview:** "Names must start with a letter and be valid Name Manager names, and a LET can hold up to 126 pairs. The last argument must be the calculation that returns the answer."
**Explain simply:**
- Syntax: `=LET(name1, value1, [name2, value2, ...], calculation)` (Microsoft Support, "LET function").
- A name cannot clash with a cell reference or R1C1 style: "a" is fine, "c" is not (same page).
- Use readable names like `dept`, `pay`.
**Example:** `=LET(pay,C2:C11,AVERAGE(pay))` returns 60,300 for the sample salaries.
**Formula / Steps:** `=LET(pay,C2:C11,avg,AVERAGE(pay),COUNTIF(pay,">"&avg))`
**Alternative:** Named ranges via Name Manager (workbook-wide), at the cost of being hidden.
**Result:** Not run here (expected result reproduced with pandas): mean 60,300; 4 salaries above it.
**Version note:** LET: 365/2021/2024 (Microsoft Support, "LET function").
**Edge cases:** Names cannot start with a number; name_value cannot refer to a later name.
**Likely follow-ups:** 1) *Does LET recalculate?* It calculates the named value once (see Q32). 2) *Can a name be a range?* Yes.
**Common mistakes:** Ending LET with a name instead of a calculation; using names like `r` or `c`.

### Q32 ⭐ 🟡 How does LET make a FILTER formula shorter and faster? Give an example where the same range is used more than once.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you write maintainable formulas?
**Say this in the interview:** "Without LET I repeat the salary range in the test and in the AVERAGE. With LET I name it once, so the formula is shorter and easier to fix. Speed gains are usually small; I have not measured them."
**Explain simply:**
- Shorter: one range reference to edit instead of two.
- Faster: LET calculates a named value once, which can help with heavy repeated calculations (general claim, unmeasured; Microsoft's page does not state timings).
**Example:** Employees paid above the average salary of 60,300.
**Sample sheet:**

| | A (Employee) | B (Dept) | C (Salary) |
|---|---|---|---|
| 2 | Asha | HR | 48000 |
| 3 | Ravi | IT | 72000 |
| 4 | Meena | HR | 52000 |
| 5 | Karan | Finance | 45000 |
| 6 | Divya | IT | 72000 |
| 7 | Imran | HR | 90000 |
| 8 | Sneha | Finance | 58000 |
| 9 | Vikram | IT | 95000 |
| 10 | Pooja | HR | 41000 |
| 11 | Arjun | Finance | 30000 |

**Formula / Steps:** Without: `=FILTER(A2:C11,C2:C11>AVERAGE(C2:C11))`. With: `=LET(pay,C2:C11,FILTER(A2:C11,pay>AVERAGE(pay)))`.
**Alternative:** Put the average in a helper cell F1 and use `C2:C11>$F$1`.
**Result:** Not run here (expected result reproduced with pandas): Ravi 72000, Divya 72000, Imran 90000, Vikram 95000 (mean 60,300).
**Version note:** FILTER and LET: 365/2021/2024.
**Edge cases:** Blank salaries lower the AVERAGE; text salaries are ignored by AVERAGE.
**Likely follow-ups:** 1) *Is it always faster?* No; tiny data shows no difference. 2) *Can LET hold the FILTER result?* Yes.
**Common mistakes:** Naming with a cell-like name; claiming big speed-ups without testing.

### Q33 ⭐ 🟡 How do you filter rows where a text column contains a keyword (partial match), for example job titles containing "Analyst"?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know FILTER needs TRUE/FALSE tests and how to build a "contains" test?
**Say this in the interview:** "SEARCH finds the position of the word in the text; ISNUMBER turns that into TRUE or FALSE; FILTER keeps the TRUE rows."
**Explain simply:**
- SEARCH is not case-sensitive and returns #VALUE! when not found; ISNUMBER converts that to FALSE.
- FIND is the case-sensitive version.
**Example:** Titles in the 10-person table; 5 contain "Analyst".
**Sample sheet:**

| | A (Employee) | B (Title) |
|---|---|---|
| 2 | Asha | HR Analyst |
| 3 | Ravi | Data Analyst |
| 4 | Meena | HR Executive |
| 5 | Karan | Payroll Analyst |
| 6 | Divya | Developer |
| 7 | Vikram | Senior Analyst |
| 8 | Arjun | Analyst Intern |

**Formula / Steps:** `=FILTER(A2:B11,ISNUMBER(SEARCH("Analyst",B2:B11)),"No match")`
**Alternative:** Helper column C with `=COUNTIF(B2,"*Analyst*")>0` (COUNTIF accepts wildcards), then filter on column C; this also works in Excel 2016/2019 with AutoFilter.
**Result:** FILTER: not run here (expected result reproduced with pandas): Asha, Ravi, Karan, Vikram, Arjun. The include array was run in LibreOffice: `ISNUMBER(SEARCH("Analyst",...))` over the 10 titles gave TRUE,TRUE,FALSE,TRUE,FALSE,FALSE,FALSE,TRUE,FALSE,TRUE; `FIND("analyst",...)` gave all FALSE, proving it is case-sensitive.
**Version note:** FILTER: 365/2021/2024.
**Edge cases:** `?`, `*` inside SEARCH text act as wildcards; use `~*` to search for a literal star. Blank cells give FALSE.
**Likely follow-ups:** 1) *Starts with?* `LEFT(B2:B11,7)="Analyst"`. 2) *Several keywords?* Add tests with `+`.
**Common mistakes:** Using `="*Analyst*"` (no wildcards in `=`); using FIND and missing lowercase matches.

### Q34 ⭐ 🟡 How do you filter out blank rows or return only non-blank entries from a range?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you handle "looks blank but is not blank"?
**Say this in the interview:** "`=FILTER(A2:A8,A2:A8<>"")` keeps non-empty cells. If cells might hold only spaces I use `LEN(TRIM(...))>0`."
**Explain simply:**
- `<>""` means "not an empty string". A cell with one space passes this test.
- `LEN(TRIM(x))>0` treats spaces-only cells as blank.
**Example:** Seven cells: Asha, blank, Ravi, empty-text, Meena, a single space, Karan.
**Sample sheet:**

| | A |
|---|---|
| 2 | Asha |
| 3 | (empty) |
| 4 | Ravi |
| 5 | ="" (empty text) |
| 6 | Meena |
| 7 | (one space) |
| 8 | Karan |

**Formula / Steps:** `=FILTER(A2:A8,LEN(TRIM(A2:A8))>0,"All blank")`
**Alternative:** `=FILTER(A2:A8,A2:A8<>"")`; for whole rows: `=FILTER(A2:C8,A2:A8<>"")`.
**Result:** Dynamic formula not run here (expected result reproduced with pandas): Asha, Ravi, Meena, Karan. Tests run in LibreOffice: `<>""` gave TRUE,FALSE,TRUE,FALSE,TRUE,TRUE,TRUE (the space row passes); `LEN(TRIM())>0` gave TRUE,FALSE,TRUE,FALSE,TRUE,FALSE,TRUE.
**Version note:** FILTER: 365/2021/2024. Pre-365: Go To Special > Blanks, or Advanced Filter.
**Edge cases:** Zero is non-blank. UNIQUE on a range with blanks returns 0 for blank (from memory).
**Likely follow-ups:** 1) *Remove blank rows permanently?* Filter, then delete rows. 2) *Check a cell?* ISBLANK is TRUE only for truly empty cells.
**Common mistakes:** Using ISBLANK on formula results; ignoring space-only cells.

### Q35 ⭐ 🟡 How do you sort a table by Department A to Z and then by Salary high to low with one formula?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know multi-level sorting with SORT or SORTBY?
**Say this in the interview:** "`=SORT(A2:C11,{2,3},{1,-1})`: sort by column 2 ascending, then column 3 descending. SORTBY does the same with ranges."
**Explain simply:**
- `sort_index` = which column number to sort by; `sort_order` = 1 ascending, -1 descending (Microsoft Support, "SORT function").
- The curly-bracket list `{2,3}` is an *array constant*: two values in one argument.
**Example:** Finance first, highest salary at the top of each department.
**Sample sheet:** Uses the table in Q32 (A Employee, B Dept, C Salary).
**Formula / Steps:** `=SORT(A2:C11,{2,3},{1,-1})`
**Alternative:** `=SORTBY(A2:C11,B2:B11,1,C2:C11,-1)` (Microsoft Support, "SORTBY function").
**Result:** Not run here (expected result reproduced with pandas): Sneha 58000, Karan 45000, Arjun 30000 (Finance); Imran 90000, Meena 52000, Asha 48000, Pooja 41000 (HR); Vikram 95000, Ravi 72000, Divya 72000 (IT).
**Version note:** SORT, SORTBY: 365/2021/2024 (Microsoft Support). Older Excel: Data > Sort with two levels.
**Edge cases:** Ties (Ravi and Divya at 72000) keep original order (from memory, unverified).
**Likely follow-ups:** 1) *Sort left to right?* `by_col` TRUE. 2) *Headers?* Exclude them.
**Common mistakes:** Using column letters instead of numbers in SORT; including the header row.

### Q36 ⭐ 🟡 HR attrition scenario: given a table with Employee, Department and Exit Date, how do you list the employees who left between 1 April and 30 June?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Date-range filtering with AND logic, and blanks for active staff.
**Say this in the interview:** "Two tests multiplied together: exit date on or after 1 April, and on or before 30 June. Multiplying means AND."
**Explain simply:**
- FILTER tests give TRUE/FALSE (TRUE=1, FALSE=0). `(test1)*(test2)` is 1 only when both are TRUE (Microsoft Support, "FILTER function").
- Use `DATE(2026,4,1)`, not typed text, so Excel compares real dates. April-June is Q1 of the Indian financial year.
**Example:** Five exits qualify out of 7 who left.
**Sample sheet:**

| | A (Employee) | B (Dept) | C (Exit Date) |
|---|---|---|---|
| 2 | Asha | HR | 15-Apr-2026 |
| 3 | Ravi | IT | (active) |
| 4 | Meena | HR | 30-Jun-2026 |
| 5 | Karan | Finance | 31-Mar-2026 |
| 6 | Divya | IT | 01-Jul-2026 |
| 7 | Imran | HR | (active) |
| 8 | Sneha | Finance | 20-May-2026 |
| 9 | Vikram | IT | 01-Apr-2026 |
| 10 | Pooja | HR | (active) |
| 11 | Arjun | Finance | 10-Jun-2026 |

**Formula / Steps:** `=FILTER(A2:C11,(C2:C11>=DATE(2026,4,1))*(C2:C11<=DATE(2026,6,30)),"No exits")`
**Alternative:** `=FILTER(A2:C11,(C2:C11>=E1)*(C2:C11<=E2),"No exits")` with dates in E1 and E2.
**Result:** FILTER: not run here (expected result reproduced with pandas): Asha, Meena, Sneha, Vikram, Arjun. Include array run in LibreOffice: TRUE,FALSE,TRUE,FALSE,FALSE,FALSE,TRUE,TRUE,FALSE,TRUE (rows 2-11); boundary dates 1-Apr and 30-Jun are included.
**Version note:** FILTER: 365/2021/2024. Older Excel: helper column or PivotTable with a date filter.
**Edge cases:** Blank exit date counts as 0, so it fails `>=1-Apr` (good). Dates stored as text fail silently; Exit dates with a time part on 30-Jun would be excluded, so use `<DATE(2026,7,1)` (from reasoning).
**Likely follow-ups:** 1) *Count them?* `=ROWS(FILTER(...))` with if_empty care. 2) *By quarter?* Change dates.
**Common mistakes:** Using `+` (OR) instead of `*`; typing dates as text.

### Q37 ⭐ 🟡 How do you return only some columns (for example Name and Salary) from a FILTER result?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know FILTER returns all columns of the array you give it?
**Say this in the interview:** "FILTER returns whatever columns are in its first argument. To pick columns I wrap it in CHOOSECOLS, or INDEX in Excel 2021."
**Explain simply:**
- CHOOSECOLS(array, col_num1, ...) returns the chosen columns (Microsoft Support, "CHOOSECOLS function").
- INDEX with a blank row argument and `{1,3}` returns columns 1 and 3 of an array (from memory, unverified).
**Example:** HR staff, Name and Salary only (Dept column dropped).
**Sample sheet:** Table from Q32 (A Employee, B Dept, C Salary).
**Formula / Steps:** `=CHOOSECOLS(FILTER(A2:C11,B2:B11="HR","None"),1,3)`
**Alternative:** `=INDEX(FILTER(A2:C11,B2:B11="HR","None"),,{1,3})` for 2021; or rearrange so the wanted columns are adjacent.
**Result:** Not run here (expected result reproduced with pandas): Asha 48000, Meena 52000, Imran 90000, Pooja 41000.
**Version note:** CHOOSECOLS: Excel 365 and 2024 only (Microsoft Support page lists 365 and 2024, not 2021). FILTER: 365/2021/2024.
**Edge cases:** A negative col_num counts from the right; 0 or too large gives an error. If the if_empty text is one value, the CHOOSECOLS output may misbehave; test it.
**Likely follow-ups:** 1) *Reorder columns?* List numbers in the order wanted. 2) *Why not select cells?* Non-adjacent ranges cannot go in FILTER.
**Common mistakes:** Passing two separate ranges to FILTER; using CHOOSECOLS in 2021.

### Q38 ⭐ 🟡 How do you return the top 5 highest salaries with their employee names using dynamic arrays?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Sort descending then take the first five, and think about ties.
**Say this in the interview:** "I sort by salary high to low, then take the first five rows with TAKE. In Excel 2021, where TAKE does not exist, I use INDEX with SEQUENCE."
**Explain simply:**
- TAKE(array, rows) keeps the first rows (Microsoft Support, "TAKE function": 365 and 2024).
- `SEQUENCE(5)` makes 1,2,3,4,5 as row numbers.
**Example:** The 10-person table; Ravi and Divya tie at 72,000 in 3rd and 4th place.
**Sample sheet:** Columns A Employee and B Salary (see Q32 for values).
**Formula / Steps:** `=TAKE(SORT(A2:B11,2,-1),5)`
**Alternative:** 2021: `=INDEX(SORT(A2:B11,2,-1),SEQUENCE(5),{1,2})` (INDEX array form, from memory, unverified). Ties-inclusive: `=FILTER(A2:B11,B2:B11>=LARGE(B2:B11,5))`.
**Result:** Not run here (expected result reproduced with pandas): Vikram 95000, Imran 90000, Divya 72000, Ravi 72000, Sneha 58000. LibreOffice run: `LARGE(B2:B11,5)` = 58000 and 5 rows are >= it.
**Version note:** TAKE: 365/2024 only. SORT, FILTER: 365/2021/2024.
**Edge cases:** If the 5th and 6th salaries tie, FILTER with LARGE returns 6 rows; TAKE returns exactly 5, picking arbitrarily by original order.
**Likely follow-ups:** 1) *Bottom 5?* Sort ascending. 2) *Top 5 per dept?* Needs GROUPBY or per-dept FILTER.
**Common mistakes:** Sorting only the salary column and losing names; ignoring ties.

### Q39 ⭐ 🟡 How does ARRAYFORMULA in Google Sheets differ from Excel dynamic arrays, and what does the QUERY function add?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Awareness of Sheets vs Excel behaviour.
**Say this in the interview:** "In Sheets, a normal formula does not spill over a whole column unless wrapped in ARRAYFORMULA. In 365, every formula can spill by itself. QUERY adds SQL-like filtering, sorting and grouping in a single text command."
**Explain simply:**
- ARRAYFORMULA: tells Sheets to run a formula on a full range, e.g. `=ARRAYFORMULA(C2:C*1.1)`.
- QUERY: select, where, group by, order by in text (like SQL).
- All Sheets claims are from memory, unverified.
**Example:** Total salary by department with QUERY.
**Sample sheet:** Table from Q32.
**Formula / Steps:** `=QUERY(A1:C11,"select B,sum(C) where B is not null group by B order by sum(C) desc",1)`
**Alternative:** Excel: `=LET(d,UNIQUE(B2:B11),HSTACK(d,SUMIFS(C2:C11,B2:B11,d)))` (HSTACK: 365, not verified here).
**Result:** Not run here (expected result reproduced with pandas): IT 239000, HR 231000, Finance 133000.
**Version note:** Sheets features from memory, unverified.
**Edge cases:** QUERY labels default to "sum Salary" headers; mixed types in a column cause blanks.
**Likely follow-ups:** 1) *Excel counterpart of QUERY?* Power Query or PivotTable. 2) *Does Excel need ARRAYFORMULA?* No.
**Common mistakes:** Forgetting ARRAYFORMULA in Sheets; wrong header count in QUERY.

### Q40 ⭐ 🟡 Why does a formula referencing a closed workbook with FILTER or UNIQUE return #REF!?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the limits of dynamic arrays across files?
**Say this in the interview:** "Microsoft says dynamic array links between workbooks work only when both files are open. If the source is closed, the linked formula returns #REF! on refresh."
**Explain simply:**
- Stated on Microsoft Support pages for FILTER, SEQUENCE and "Dynamic array formulas and spilled array behavior": limited support, only with both workbooks open.
- The data is not corrupted; the formula just cannot read the closed file.
**Example:** A monthly HR dashboard file pulls `FILTER` results from Payroll.xlsx.
**Formula / Steps:** Open the source workbook, then recalculate (Ctrl+Alt+F9). Or paste values, or load the data with Power Query (Data > Get Data).
**Alternative:** Keep both tables in one workbook; or use SUMIFS/INDEX-MATCH, which can read closed files (from memory, unverified).
**Version note:** Applies in 365/2021/2024 (Microsoft Support).
**Edge cases:** Saving with the source open still breaks next time if the source is later closed. Result: not run here (cannot be reproduced in LibreOffice).
**Likely follow-ups:** 1) *Does the cached value stay?* Until refresh. 2) *Safer link?* Power Query.
**Common mistakes:** Blaming the formula syntax; sending the dashboard without the source.

### Q41 ⭐ 🔴 How do you count the distinct employees who joined in a given year using UNIQUE and FILTER, without getting an error when nobody joined?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Nesting functions and handling the empty-result error.
**Say this in the interview:** "`=IFERROR(ROWS(UNIQUE(FILTER(ids,YEAR(dates)=2025))),0)`. If nobody joined, FILTER returns #CALC! and IFERROR turns it into 0."
**Explain simply:**
- FILTER with no match and no if_empty gives #CALC! (Microsoft Support, "FILTER function").
- ROWS counts spilled rows. Setting if_empty to "" would make ROWS return 1, which is wrong.
- IFERROR hides every error, so use it only where 0 is the right fallback.
**Example:** Six rows; E2 appears twice.
**Sample sheet:**

| | A (Emp) | B (Join) |
|---|---|---|
| 2 | E1 | 01-Feb-2025 |
| 3 | E2 | 10-Mar-2025 |
| 4 | E2 | 10-Mar-2025 |
| 5 | E3 | 01-Jul-2024 |
| 6 | E4 | 15-Nov-2025 |
| 7 | E5 | 05-Jan-2026 |

**Formula / Steps:** `=IFERROR(ROWS(UNIQUE(FILTER(A2:A7,YEAR(B2:B7)=2025))),0)`
**Alternative:** Works everywhere: `=SUMPRODUCT((YEAR(B2:B7)=2025)/(COUNTIFS(A2:A7,A2:A7,B2:B7,">="&DATE(2025,1,1),B2:B7,"<="&DATE(2025,12,31))+(YEAR(B2:B7)<>2025)))`.
**Result:** Dynamic formula not run here (expected result reproduced with pandas): 2025 gives 3, 2030 gives 0. The SUMPRODUCT alternative was run in LibreOffice: 3 for 2025 and 0 for 2030.
**Version note:** FILTER, UNIQUE: 365/2021/2024.
**Edge cases:** Duplicate rows (E2); text dates make YEAR fail with #VALUE!, which IFERROR would also hide.
**Likely follow-ups:** 1) *Why not COUNTA?* It counts duplicates. 2) *Different year per cell?* Replace 2025 with a cell.
**Common mistakes:** Using if_empty "" then ROWS; forgetting UNIQUE.

### Q42 ⭐ 🔴 Why can FILTER return #VALUE!, and how do you check that the include array matches the data array?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Debugging skills.
**Say this in the interview:** "The include test must be the same height as the data. If I wrote B2:B10 against A2:C11, the sizes differ and FILTER fails. I check with ROWS on both."
**Explain simply:**
- Microsoft says: include must have the same height or width as array; an error value inside include makes FILTER return an error, though the page does not say which one (Microsoft Support, "FILTER function"). #VALUE! for mismatched sizes is from memory, unverified.
- Other triggers: an error cell in the tested column, or text that cannot convert to TRUE/FALSE.
**Example:** Data A2:C11 (10 rows) but test on B2:B10 (9 rows).
**Formula / Steps:**
1. Test: `=ROWS(A2:C11)=ROWS(B2:B10)` returns FALSE.
2. Paste the include test alone in a spare cell to see TRUE/FALSE list and any errors.
3. Formulas > Evaluate Formula to step through.
**Alternative:** Use a Table, so `Table[Dept]` and `Table[#Data]` stay aligned.
**Result:** LibreOffice run: `ROWS(A2:A11)`=10, `ROWS(A2:A10)`=9, equality FALSE. Expected FILTER error not run here; pandas gives a similar mismatch error (IndexingError for a boolean mask of 9 against 10 rows).
**Version note:** FILTER: 365/2021/2024.
**Edge cases:** Whole-column vs partial ranges; #N/A in the test column.
**Likely follow-ups:** 1) *#CALC! vs #VALUE!?* #CALC! means no matches. 2) *How to avoid?* Tables.
**Common mistakes:** Misaligned start rows; including the header in one range only.

### Q43 ⭐ 🔴 How would you give the same result as FILTER to colleagues who use Excel 2016 or 2019?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Backward-compatible thinking.
**Say this in the interview:** "I add a helper column that numbers matching rows 1, 2, 3, then pull each with INDEX and MATCH. Or I use a PivotTable, Advanced Filter or AutoFilter."
**Explain simply:**
- A *helper column* is an extra column used only for intermediate calculation.
- TEXTJOIN exists from Excel 2019 (Microsoft Support, "TEXTJOIN function"), but not 2016.
- Power Query is another option; "built into Excel 2016" is from memory, unverified.
**Example:** List HR staff: Asha, Meena, Imran, Pooja.
**Sample sheet:**

| | A (Employee) | B (Dept) | I (Helper) |
|---|---|---|---|
| 2 | Asha | HR | 1 |
| 3 | Ravi | IT | |
| 4 | Meena | HR | 2 |
| 5 | Karan | Finance | |
| 6 | Divya | IT | |
| 7 | Imran | HR | 3 |
| 8 | Sneha | Finance | |
| 9 | Vikram | IT | |
| 10 | Pooja | HR | 4 |
| 11 | Arjun | Finance | |

**Formula / Steps:** Helper I2 (copy down): `=IF(B2=$G$1,COUNTIF($B$2:B2,$G$1),"")` with G1 = HR. Output (copy down): `=IFERROR(INDEX($A$2:$A$11,MATCH(ROWS($1:1),$I$2:$I$11,0)),"")`.
**Alternative:** `AGGREGATE(15,6,(ROW(...)-ROW(first)+1)/(B2:B11=G1),k)` with INDEX needs no helper column (from memory, unverified: LibreOffice returned blanks, so I could not confirm it).
**Result:** Run in LibreOffice 24.2: helper column gave 1,"",2,"","",3,"","",4,"" and INDEX/MATCH gave Asha, Meena, Imran, Pooja, then blank. Matches pandas.
**Version note:** INDEX/MATCH works in all versions.
**Edge cases:** Copy the output formula down further than the maximum matches; blanks hide extras.
**Likely follow-ups:** 1) *Single-cell result?* TEXTJOIN in 2019+ (in 2019 needs Ctrl+Shift+Enter with IF). 2) *Refresh?* Formulas update automatically.
**Common mistakes:** Forgetting to anchor with $; hard-coding the list length.

### Q44 ⭐ 🔴 For each department, how do you return the highest salary and the employee who earns it using dynamic arrays and LET?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Combining SORT, UNIQUE, lookup inside LET.
**Say this in the interview:** "Sort everyone by salary high to low, so each department's top earner comes first, then for each unique department look up the first match."
**Explain simply:**
- XLOOKUP/XMATCH returns the first match by default, and after sorting that is the highest earner. XMATCH needs 365/2021/2024 (Microsoft Support, "XMATCH function").
- Ties: only the first listed of tied earners appears.
**Example:** Finance: Sneha 58000. HR: Imran 90000. IT: Vikram 95000.
**Sample sheet:** Table from Q32 (A Employee, B Dept, C Salary).
**Formula / Steps:** `=LET(s,SORT(A2:C11,3,-1),d,INDEX(s,,2),u,UNIQUE(d),r,XMATCH(u,d),SORT(INDEX(s,r,{2,1,3})))`
**Alternative:** Per department, no spill: `=MAXIFS(C2:C11,B2:B11,F2)` and `=INDEX(A2:A11,MATCH(1,INDEX((B2:B11=F2)*(C2:C11=G2),0),0))`.
**Result:** Dynamic formula: not run here (expected result reproduced with pandas; the exact formula itself was not executed, so test it in Excel): Finance Sneha 58000, HR Imran 90000, IT Vikram 95000. The alternative ran in LibreOffice: Finance 58000/Sneha, HR 90000/Imran, IT 95000/Vikram.
**Version note:** LET, SORT, UNIQUE, XMATCH: 365/2021/2024.
**Edge cases:** If two people tie for the top salary in a department, only the first one in sorted order appears (Ravi and Divya tie at 72,000 in IT but sit below Vikram, so no issue here). Blank department rows form their own group.
**Likely follow-ups:** 1) *Show all tied earners?* Use FILTER with MAXIFS. 2) *Without LET?* Use helper columns.
**Common mistakes:** UNIQUE on the whole table (not by department); forgetting to sort first.

### Q45 ⭐ 🔴 How do you build a chart or named range that expands automatically with a spilled FILTER or UNIQUE result?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the `#` operator in named ranges for self-updating charts?
**Say this in the interview:** "I create a name that refers to the spill cell with `#`, for example `=Sheet1!$F$2#`, and point the chart series at that name. As the spill grows or shrinks, the chart follows."
**Explain simply:**
- The spill range operator `#` means "all cells this formula spilled into" (Microsoft's SORTBY page shows `#` used with a spilled SEQUENCE range; fuller explanation is on the Exceljet page I read earlier in research).
- Using the name in a chart series: from memory, unverified.
- The spill cannot live in an Excel Table (Microsoft Support, "Dynamic array formulas and spilled array behavior").
**Example:** Headcount by department in F2:G4 grows when a new department appears.
**Formula / Steps:**
1. In F2: `=UNIQUE(FILTER(B2:B100,B2:B100<>""))`.
2. Formulas > Defined Names > Name Manager > New: Name `DeptList`, Refers to `=Sheet1!$F$2#`.
3. Create the chart, then Chart Design > Select Data > edit series values, type `=Book1.xlsx!DeptList` (use the real file name).
**Alternative:** Pre-365: `=OFFSET(Sheet1!$F$2,0,0,COUNTA(Sheet1!$F$2:$F$100),1)` as the named range.
**Result:** Not run here (charts and spill not supported). LibreOffice check of the fallback building block: `COUNTA(F2:F100)` returned 4 for a test list of 4 names (HR, IT, Finance, Admin), which is the height OFFSET would use. The OFFSET name itself and the chart were not run here.
**Version note:** Spill functions: 365/2021/2024.
**Edge cases:** #SPILL! or #CALC! in F2 empties the chart; use if_empty.
**Likely follow-ups:** 1) *Why not a Table?* No spills in Tables. 2) *Pivot chart?* Easier but needs refresh.
**Common mistakes:** Pointing the chart at fixed cells; forgetting the workbook name before the defined name.

