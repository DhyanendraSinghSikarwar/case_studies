# Book 1 — Excel | Part 1: Basics: cell refs, sorting, filtering, formatting, shortcuts 🟢

**Target:** 60 questions | **Actual:** 66 questions
**Scope:** Cell references, sorting, filtering, formatting, keyboard shortcuts and other first-week Excel basics asked of 0-3 year data/MIS/HR analysts.

### Q1 ⭐⭐⭐ 🟢 What is a cell reference in Excel, and what are the three types?
**Asked at:** commonly asked (no company-specific report found); appears in every beginner Excel list we found (DataCamp, Guru99).
**What the interviewer is checking:** Do you know that formulas point to cells by address, and that the dollar sign controls what happens on copying?
**Say this in the interview:** "A cell reference is the address of a cell, like B2, column letter plus row number. A formula uses it to read that cell's value. There are three types: relative (B2), absolute ($B$2) and mixed ($B2 or B$2)."
**Explain simply:**
- Column letter first, row number second: B2 is column B, row 2. A range like B2:B6 means all cells from B2 down to B6.
- **Relative (B2):** when you copy the formula, the address shifts with the move, like "the cell next to me".
- **Absolute ($B$2):** the dollar signs lock both column and row, so it always points at that exact cell.
- **Mixed ($B2 or B$2):** one part locked, the other free to move.
**Example:** A payroll sheet where C2 has `=B2*10%`. Copy it to C3 and it becomes `=B3*10%`. That is a relative reference in action.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Employee | Basic | Rate |
| 2 | Asha | 40000 | 10% |
| 3 | Ravi | 52000 | |

**Formula / Steps:** In a spare cell, `=B2` (relative), `=$B$2` (absolute), `=B$2` (row locked), `=$B2` (column locked).
**Alternative:** Click the cell while typing the formula instead of typing the address; Excel inserts the reference for you.
**Result:** Run in LibreOffice and copied down one row, all four forms return 40000 in the original cell. The difference only shows after copying (see Q2).
**Version note:** Same in all Excel versions and Google Sheets (from memory, unverified).
**Edge cases:** A reference to a blank cell returns 0. A reference to another sheet needs the sheet name (Q44).
**Likely follow-ups:** 1) *What is a range?* Several cells written as B2:B6. 2) *Which key adds the dollar signs?* F4 (Q4).
**Common mistakes:** Thinking `$` means currency; forgetting that copying shifts relative references.

### Q2 ⭐⭐⭐ 🟢 What is the difference between a relative and an absolute cell reference?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can predict what a formula does after copying it.
**Say this in the interview:** "A relative reference changes when I copy the formula, an absolute reference with dollar signs does not. I use absolute when every row must point at one fixed cell, like a bonus rate."
**Explain simply:**
- Relative: Excel remembers the position ("one column left"), not the address.
- Absolute `$G$2`: locked to that cell forever.
- Use absolute for single inputs: tax rate, bonus %, exchange rate.
**Example:** Bonus rate 10% sits in G2. Employees' basic pay is in B2:B5.
**Sample sheet:**

| | A | B | D | E | G |
|---|---|---|---|---|---|
| 1 | Employee | Basic | Bonus (relative) | Bonus (absolute) | Rate |
| 2 | Asha | 40000 | 4000 | 4000 | 0.1 |
| 3 | Ravi | 52000 | 0 | 5200 | |
| 4 | Meena | 35000 | 0 | 3500 | |
| 5 | Karan | 60000 | 0 | 6000 | |

**Formula / Steps:** D2 `=B2*G2` copied down (breaks). E2 `=B2*$G$2` copied down (works).
**Alternative:** Give G2 a name (Formulas > Defined Names > Define Name, call it BonusRate) and write `=B2*BonusRate`; names are always absolute.
**Result:** Run in LibreOffice. D3 became `=B3*G3`, pointing at an empty cell, so it returns 0. Column E returns 4000, 5200, 3500, 6000.
**Version note:** All versions and Google Sheets (from memory, unverified).
**Edge cases:** The relative version fails silently with 0, no error, so always spot-check the last row.
**Likely follow-ups:** 1) *Can you lock only the row?* Yes, mixed reference (Q3). 2) *How do you check?* Press F2 or Ctrl+` (Q19).
**Common mistakes:** Typing `$` on the wrong part (`B$2*G$2`); trusting the first row only.

### Q3 ⭐⭐⭐ 🟢 What is a mixed cell reference, and when would you use one?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can build a two-way table with a single formula.
**Say this in the interview:** "A mixed reference locks only the column ($A2) or only the row (A$1). I use it for grids where one input runs down the side and another across the top, so one formula fills the whole table."
**Explain simply:**
- `$A2`: column A is locked, row can change.
- `A$1`: row 1 is locked, column can change.
- Typical use: a what-if grid, such as pay hike % across the top and current salary down the side.
**Example:** Bonus amount for three basic salaries at 5%, 10%, 15%.
**Sample sheet:**

| | A | B | C | D |
|---|---|---|---|---|
| 1 | Basic | 5% | 10% | 15% |
| 2 | 40000 | 2000 | 4000 | 6000 |
| 3 | 52000 | 2600 | 5200 | 7800 |
| 4 | 60000 | 3000 | 6000 | 9000 |

**Formula / Steps:** B2 `=$A2*B$1`, then copy to B2:D4.
**Alternative:** Use a Data Table (Data > What-If Analysis > Data Table), or two absolute-reference formulas typed by hand (slow, error-prone).
**Result:** Run in LibreOffice; the nine cells above are the returned values.
**Version note:** All versions and Google Sheets (from memory, unverified).
**Edge cases:** If you lock the wrong half, the grid looks plausible but is wrong; check the corner cell D4 by hand.
**Likely follow-ups:** 1) *Why not use absolute?* It would repeat one value everywhere. 2) *Quick way to type it?* F4 cycling (Q4).
**Common mistakes:** Locking `$A$2` and `B$1` both fully; placing `$` on the wrong side of the letter.

### Q4 ⭐⭐⭐ 🟢 Which key toggles between relative, absolute and mixed references while editing a formula, and what does it cycle through?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Speed and shortcut fluency.
**Say this in the interview:** "F4. With the cursor on a reference inside the formula, each press cycles B2, then $B$2, then B$2, then $B2, and back to B2."
**Explain simply:**
- Press F4 while editing (F2 or typing a formula), with the reference selected or the cursor touching it.
- Order: relative > fully absolute > row locked > column locked > relative.
- Microsoft Support's shortcut page (Keyboard shortcuts in Excel) confirms F4 cycles through absolute and relative combinations.
**Example:** In E2 type `=B2*G2`, click on G2 in the formula bar, press F4 once: `=B2*$G$2`.
**Formula / Steps:** 1. Double-click the cell or press F2. 2. Put the cursor in the reference. 3. Press F4 repeatedly until the right form shows. 4. Press Enter.
**Alternative:** Type the `$` signs by hand. On many laptops use Fn+F4; on Mac use Cmd+T (per the same page).
**Version note:** Windows shortcut verified (Microsoft Support). On laptops, the Fn key may be needed.
**Edge cases:** Outside edit mode, F4 repeats the last action, which is a different feature.
**Likely follow-ups:** 1) *Does it work on a range?* Yes, B2:B6 cycles to $B$2:$B$6. 2) *Google Sheets?* Also F4 (from memory, unverified).
**Common mistakes:** Pressing F4 when not in edit mode; pressing it too many times and landing on the wrong form.

### Q5 ⭐⭐⭐ 🟢 Cell B2 holds a price and column D holds quantities. How do you calculate a total for every row in column E using the same price cell without it shifting when you copy the formula down?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Practical use of absolute references.
**Say this in the interview:** "I lock the price cell with dollar signs: `=$B$2*D5`, then drag down. The price stays on B2 while the quantity moves row by row."
**Explain simply:**
- Price is one fixed input, so it needs `$B$2`.
- Quantity changes per row, so it stays relative (D5).
- If the price changes later, edit B2 once and all totals update.
**Example:** Cost per training kit is 250 and different batches order 4, 10, 3, 8, 12 kits.
**Sample sheet:**

| | A | B | D | E |
|---|---|---|---|---|
| 2 | Unit price | 250 | | |
| 4 | | | Qty | Total |
| 5 | | | 4 | 1000 |
| 6 | | | 10 | 2500 |
| 7 | | | 3 | 750 |
| 8 | | | 8 | 2000 |
| 9 | | | 12 | 3000 |

**Formula / Steps:** E5 `=$B$2*D5`, then double-click the fill handle to copy down.
**Alternative:** `=PRODUCT($B$2,D5)`, or name B2 as Price and use `=Price*D5`.
**Result:** Run in LibreOffice: 1000, 2500, 750, 2000, 3000.
**Version note:** All versions and Google Sheets (from memory, unverified).
**Edge cases:** Blank quantity gives 0; text quantity like "10 " gives #VALUE!.
**Likely follow-ups:** 1) *What if the price is in a column?* Use mixed `$B2` style. 2) *Using a Table?* Use a structured reference, see Q32.
**Common mistakes:** Writing `=B2*D5` and getting wrong totals from row 6 on; locking D5 too.

### Q6 ⭐⭐⭐ 🟢 How do you sort data in Excel?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic data handling without breaking rows.
**Say this in the interview:** "I click inside the table, go to Data > Sort, choose the column and order, and make sure 'My data has headers' is ticked. For a quick sort I use the A to Z or Z to A buttons."
**Explain simply:**
- Sorting rearranges rows by one or more columns; it changes the order, not the data.
- A to Z / smallest to largest = ascending. Z to A / largest to smallest = descending.
- Click one cell inside the data and Excel selects the whole block automatically.
**Example:** Sorting 6 employees by salary, lowest first.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Emp | Dept | Salary |
| 2 | Asha | Sales | 40000 |
| 3 | Ravi | HR | 52000 |
| 4 | Meena | Sales | 35000 |
| 5 | Karan | IT | 60000 |
| 6 | Divya | HR | 48000 |
| 7 | Sam | Sales | 45000 |

**Formula / Steps:** 1. Click any cell in column C. 2. Data tab > Sort & Filter group > Sort. 3. Sort by Salary, Sort On Cell Values, Order Smallest to Largest. 4. OK.
**Alternative:** Formula route in Excel 365/2021: `=SORT(A2:C7,3,1)` (not run here; pandas gave Meena 35000, Asha 40000, Sam 45000, Divya 48000, Ravi 52000, Karan 60000).
**Result:** Order by Salary ascending (pandas, not Excel): Meena, Asha, Sam, Divya, Ravi, Karan.
**Version note:** Dialog works in all versions. SORT function needs Excel 365 or 2021 (from memory, unverified); not in 2016/2019.
**Edge cases:** Merged cells block sorting; blanks sort last; formulas with relative references to other rows may change after sorting.
**Likely follow-ups:** 1) *Multi-level?* Q8. 2) *Undo?* Ctrl+Z immediately; see Q64.
**Common mistakes:** Selecting one column only; not ticking headers.

### Q7 ⭐⭐⭐ 🟢 Why must you tick 'My data has headers' in the Sort dialog, and what goes wrong if you sort a single column without selecting the full table?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you protect row integrity?
**Say this in the interview:** "The tick tells Excel the first row is column names, not data. If it is off, the header gets sorted into the data. And if I sort one column alone, only that column moves and the names no longer match the salaries, which is silent data corruption."
**Explain simply:**
- Without the tick, the word "Salary" is treated as a value and sorted along with numbers.
- Each row is one employee. Sorting only one column breaks that link.
- Excel warns with "Sort Warning" when you select one column next to other data. Choose "Expand the selection".
**Example:** Sorting only the Salary column makes Asha earn 35000 instead of 40000.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | Emp | Salary |
| 2 | Asha | 35000 |
| 3 | Ravi | 40000 |
| 4 | Meena | 45000 |
| 5 | Karan | 52000 |

(Wrong: only column B sorted; names stayed in place.)
**Formula / Steps:** 1. Click one cell in the table (do not select a column). 2. Data > Sort. 3. Tick My data has headers. 4. Choose column and order. 5. OK.
**Alternative:** Convert to an Excel Table (Ctrl+T, Q32); sorting then always keeps rows together.
**Version note:** Dialog wording same across versions (from memory, unverified).
**Edge cases:** Blank row or blank column inside the data stops auto-selection, so part of the data is left out.
**Likely follow-ups:** 1) *How to recover?* Ctrl+Z at once (Q64). 2) *Prevent?* Tables, or a serial-number column.
**Common mistakes:** Highlighting one column and clicking A to Z, then choosing "Continue with the current selection".

### Q8 ⭐⭐⭐ 🟢 How do you sort employee data by Department first and then by Salary from highest to lowest?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Multi-level sorting.
**Say this in the interview:** "In the Sort dialog I add two levels: Department A to Z first, then Salary Largest to Smallest. Excel sorts by department and uses salary to order rows inside each department."
**Explain simply:**
- The first level is the main sort; later levels break ties.
- Order of levels matters: Dept first, Salary second.
**Example:** The 6-employee sheet from Q6.
**Sample sheet:** same as Q6 (A Emp, B Dept, C Salary, rows 2 to 7).
**Formula / Steps:** 1. Click inside data. 2. Data > Sort. 3. Sort by Dept, A to Z. 4. Add Level. 5. Then by Salary, Largest to Smallest. 6. Tick My data has headers. 7. OK.
**Alternative:** `=SORTBY(A2:C7,B2:B7,1,C2:C7,-1)` in Excel 365/2021 (not run here).
**Result:** pandas (not run in Excel): HR Ravi 52000, HR Divya 48000, IT Karan 60000, Sales Sam 45000, Sales Asha 40000, Sales Meena 35000.
**Version note:** Dialog in all versions; SORTBY is 365/2021 only (from memory, unverified).
**Edge cases:** Extra spaces in department names ("Sales " vs "Sales") split a group; clean with TRIM first.
**Likely follow-ups:** 1) *Custom order of departments?* Q46. 2) *Sort by colour?* Q34.
**Common mistakes:** Sorting Salary first then Dept (loses the salary order within groups); forgetting Add Level.

### Q9 ⭐⭐⭐ 🟢 How do you filter data in Excel?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you narrow a large list quickly?
**Say this in the interview:** "I click inside the data and press Ctrl+Shift+L or use Data > Filter. Each header gets a drop-down arrow; I untick what I don't want or use Text/Number/Date filters. Filtering hides rows, it does not delete them."
**Explain simply:**
- AutoFilter = the little drop-down arrows on headers.
- Filtering on several columns combines them with AND (every condition must hold).
- Row numbers turn blue and the status bar says "x of y records found".
**Example:** From 5,000 staff, show only Department = Sales.
**Sample sheet:** same as Q6 (Dept in column B).
**Formula / Steps:** 1. Click any cell in the data. 2. Data > Sort & Filter > Filter. 3. Click the arrow on Dept. 4. Untick Select All, tick Sales. 5. OK.
**Alternative:** Excel 365/2021 `=FILTER(A2:C7,B2:B7="Sales")` (not run here).
**Result:** pandas (not Excel): Asha, Meena, Sam are the Sales rows.
**Version note:** Filter button works in all versions; FILTER is 365/2021 only (from memory, unverified).
**Edge cases:** Blank rows break the data block; values with trailing spaces appear as separate items.
**Likely follow-ups:** 1) *Shortcut?* Ctrl+Shift+L (Q16). 2) *Clear it?* Q12.
**Common mistakes:** Thinking hidden rows are deleted; summing visible rows with SUM (it still counts hidden ones; use SUBTOTAL).

### Q10 ⭐⭐⭐ 🟢 What is the difference between sorting and filtering?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Conceptual clarity.
**Say this in the interview:** "Sorting changes the order of all rows. Filtering hides rows that don't match a condition, and the order stays the same."
**Explain simply:**
- Sort: everything stays visible, just rearranged.
- Filter: some rows are temporarily hidden, nothing is lost or reordered.
- They can be combined: filter Sales, then sort by salary.
**Example:** "Rank all employees by salary" is a sort. "Show only HR employees" is a filter.
**Formula / Steps:** Data > Sort & Filter group holds both: Sort A to Z, Sort Z to A, Sort, Filter, Advanced.
**Alternative:** Use `SORT` and `FILTER` functions in 365 to produce a separate result without touching the original (not run here).
**Version note:** Same in all versions (from memory, unverified).
**Edge cases:** Sorting changes the physical position of data; filtering does not.
**Likely follow-ups:** 1) *Can you do both?* Yes. 2) *Which is permanent?* Sort is, unless you undo or keep an index column (Q51).
**Common mistakes:** Saying filter removes data; forgetting that a filter stays on after saving.

### Q11 ⭐⭐⭐ 🟢 How do you show only the rows for the Sales department with a joining date in 2025 using a filter?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Filtering on two columns, one of them a date.
**Say this in the interview:** "I turn on Filter, filter Dept to Sales, then open the Join Date filter, choose Date Filters > Between, 01-Jan-2025 to 31-Dec-2025. The two filters combine."
**Explain simply:**
- Each column filter narrows the result further (AND logic).
- For dates, the grouped list also lets you tick the year 2025 directly.
**Example:** Find Sales hires made in 2025.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Emp | Dept | Join date |
| 2 | Asha | Sales | 10-Mar-2025 |
| 3 | Ravi | HR | 01-Jun-2025 |
| 4 | Meena | Sales | 20-Nov-2024 |
| 5 | Karan | Sales | 05-Sep-2025 |
| 6 | Divya | IT | 15-Jan-2025 |
| 7 | Sam | Sales | 31-Dec-2025 |

**Formula / Steps:** 1. Ctrl+Shift+L. 2. Dept arrow > tick only Sales. 3. Join date arrow > Date Filters > Between > on or after 01-01-2025 and before or on 31-12-2025. 4. OK.
**Alternative:** To verify the count: `=COUNTIFS(B2:B7,"Sales",C2:C7,">="&DATE(2025,1,1),C2:C7,"<="&DATE(2025,12,31))`.
**Result:** Run in LibreOffice: 3 (Asha, Karan, Sam). A SUMPRODUCT version also gave 3.
**Version note:** All versions (from memory, unverified).
**Edge cases:** Dates stored as text will not show date filters (Q41). Meena is excluded since 2024.
**Likely follow-ups:** 1) *Filter by month?* Q36. 2) *More conditions?* Advanced Filter, Q48.
**Common mistakes:** Using "after 2025" (that excludes 2025 itself); text dates.

### Q12 ⭐⭐⭐ 🟢 How do you clear a filter, and how do you remove the filter arrows completely?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know clear versus turn off?
**Say this in the interview:** "Clear shows all rows again but keeps the arrows: Data > Clear. To remove the arrows completely I toggle Filter off with Data > Filter or Ctrl+Shift+L."
**Explain simply:**
- Clear one column: click its arrow > Clear Filter From "Column".
- Clear all columns: Data > Sort & Filter > Clear.
- Remove arrows: Data > Filter again.
**Formula / Steps:** 1. Data tab. 2. Sort & Filter group. 3. Clear (rows return) or Filter (arrows gone).
**Alternative:** Shortcut Ctrl+Shift+L turns the arrows on or off. Reapply re-runs the filter after new data is typed.
**Version note:** Same in all versions (from memory, unverified).
**Edge cases:** On an Excel Table, the Filter button toggles arrows but the table stays a table.
**Likely follow-ups:** 1) *Why do some rows stay hidden?* They may be manually hidden (Q40). 2) *Does clearing remove sorting?* No.
**Common mistakes:** Clearing one column and thinking all filters are off; leaving a filter on and sharing the file.

### Q13 ⭐⭐⭐ 🟢 What is Freeze Panes, and how do you keep the header row visible while scrolling a long sheet?
**Asked at:** commonly asked (no company-specific report found); appears in DataCamp and Guru99 beginner lists.
**What the interviewer is checking:** Comfort with large sheets.
**Say this in the interview:** "Freeze Panes locks rows or columns so they stay on screen while the rest scrolls. For the header I use View > Freeze Panes > Freeze Top Row."
**Explain simply:**
- Panes are the screen sections; freezing pins the top or left part.
- Freeze Top Row pins only row 1. Freeze First Column pins column A.
- Freeze Panes (the general option) pins everything above and left of the selected cell.
**Example:** A 5,000-row attendance sheet; you scroll to row 3,000 and still see Employee, Date and Status.
**Formula / Steps:** 1. View tab > Window group > Freeze Panes. 2. Choose Freeze Top Row. 3. To undo: Freeze Panes > Unfreeze Panes.
**Alternative:** Convert to a Table; its headers replace column letters while scrolling, with no freezing needed.
**Version note:** Same in all versions and Google Sheets (View > Freeze) (from memory, unverified).
**Edge cases:** If the header is in row 3 not row 1, select A4 and use Freeze Panes. Freeze works from the current visible top, so scroll up first.
**Likely follow-ups:** 1) *Freeze row and column?* Q58. 2) *Print the header on every page?* Print Titles, Q42.
**Common mistakes:** Selecting the wrong cell before freezing; thinking freeze affects printing.

### Q14 ⭐⭐⭐ 🟢 How do you format data in Excel (number, currency, percentage, date)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Presentation basics without changing values.
**Say this in the interview:** "I select the cells and use Home > Number group, or Ctrl+1 for Format Cells. Formatting changes how a value looks, not what it is. For example 0.1875 displays as 18.8% but stays 0.1875."
**Explain simply:**
- Number: thousand separators, decimals. Currency: adds a symbol. Percentage: multiplies the shown value by 100 and adds %. Date: shows a serial number as a date.
- Shortcuts, per Microsoft Support (Keyboard shortcuts in Excel): Ctrl+Shift+~ General, Ctrl+Shift+$ Currency, Ctrl+Shift+% Percentage.
**Example:** Salary 1234567.891 shown as 1,234,567.89; attrition 0.1875 shown as 18.8%.
**Sample sheet:**

| | A | C (TEXT result) |
|---|---|---|
| 1 | 1234567.891 | 1,234,567.89 |
| 2 | 0.1875 | 18.8% |
| 3 | 21-Oct-2026 | 21-Oct-2026 |
| 4 | 1234.5 | $1,234.50 |

**Formula / Steps:** Select cells > Ctrl+1 > Number tab > pick category > set decimals/symbol > OK.
**Alternative:** `=TEXT(A2,"0.0%")` makes a text copy. Ran in LibreOffice: results above.
**Version note:** All versions; currency symbol follows your regional setting.
**Edge cases:** TEXT output is text and can't be summed. Percentage on 18 shows 1800%; type 18% instead.
**Likely follow-ups:** 1) *Does formatting change the value?* No. 2) *Custom formats?* Q65.
**Common mistakes:** Applying % to whole numbers; rounding by formatting and then summing displayed values.

### Q15 ⭐⭐⭐ 🟢 Name five keyboard shortcuts you use every day in Excel.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Real daily usage.
**Say this in the interview:** "Ctrl+C and Ctrl+V to copy and paste, Ctrl+Z to undo, Ctrl+Shift+L for filters, Ctrl+Arrow to jump across data, and Alt+= to add up a column."
**Explain simply:**
- Ctrl+Z undo; Ctrl+C / Ctrl+V copy, paste.
- Ctrl+Arrow: move to the edge of the data block.
- Ctrl+1: Format Cells. Ctrl+T: make a Table. Alt+=: AutoSum.
- Ctrl+Space selects a column, Shift+Space a row.
- All above confirmed in Microsoft Support, Keyboard shortcuts in Excel, except Ctrl+Shift+L (see Q16).
**Example:** Press Ctrl+Down on a 5,000-row list to reach the last record in one keystroke.
**Formula / Steps:** Use them while working; no menus needed.
**Version note:** Windows. On Mac many use Cmd instead of Ctrl (from memory).
**Edge cases:** Keyboard layouts can change Ctrl+` and Ctrl+Shift+~.
**Likely follow-ups:** 1) *Fastest to select the data?* Ctrl+A or Ctrl+Shift+Arrow. 2) *Insert row?* Q55.
**Common mistakes:** Naming shortcuts you can't demonstrate; naming only Ctrl+C/V.

### Q16 ⭐⭐⭐ 🟢 What is the shortcut to toggle AutoFilter on and off?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Shortcut recall.
**Say this in the interview:** "Ctrl+Shift+L. Press once to add the filter arrows, press again to remove them."
**Explain simply:**
- Click a cell inside the data first.
- Alt, A, T is the older ribbon key sequence for the same Filter command (from memory).
- Microsoft Support's shortcut page listed Ctrl+Shift+L for Mac and Excel for the web ("Toggle AutoFilter on and off"); that it works on Windows desktop is from my memory, unverified from that page.
**Formula / Steps:** Click inside data > Ctrl+Shift+L.
**Alternative:** Data > Filter.
**Version note:** Works in desktop Excel on Windows in my experience (from memory); Google Sheets uses a different shortcut.
**Edge cases:** If the sheet is not active in a data block, it filters the wrong range.
**Likely follow-ups:** 1) *Clear only?* Data > Clear (Q12).
**Common mistakes:** Pressing it twice by accident and wondering where the arrows went.

### Q17 ⭐⭐⭐ 🟢 How do you quickly sum a column of numbers without typing a formula?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** AutoSum and status bar.
**Say this in the interview:** "I click the cell under the numbers and press Alt+=, or use Home > AutoSum. For a quick look without writing anything, I select the cells and read the Sum in the status bar."
**Explain simply:**
- AutoSum writes `=SUM(...)` for you and guesses the range.
- Status bar (bottom right) shows Sum, Average and Count of the selection. Nothing is put in the sheet.
- Alt+= is confirmed in Microsoft Support, Keyboard shortcuts in Excel.
**Example:** Total basic pay of four employees.
**Sample sheet:**

| | A |
|---|---|
| 1 | Basic |
| 2 | 40000 |
| 3 | 52000 |
| 4 | 35000 |
| 5 | 60000 |
| 6 | |
| 7 | 187000 |

**Formula / Steps:** Click A7 > Alt+= > Enter. The formula is `=SUM(A2:A5)`.
**Alternative:** `=SUBTOTAL(109,A2:A5)` ignores filtered-out rows. Ran in LibreOffice.
**Result:** Both returned 187000.
**Version note:** All versions.
**Edge cases:** Blank row in the middle stops AutoSum's auto range. SUM ignores text; numbers stored as text are missed (Q20).
**Likely follow-ups:** 1) *Sum of filtered rows?* SUBTOTAL. 2) *Average quickly?* Status bar.
**Common mistakes:** Leaving a blank row between data and the total; not noticing text numbers.

### Q18 ⭐⭐⭐ 🟢 What is the difference between a workbook, a worksheet and a cell?
**Asked at:** commonly asked (no company-specific report found); opener-level question.
**What the interviewer is checking:** Vocabulary.
**Say this in the interview:** "A workbook is the whole Excel file. A worksheet is one tab inside it. A cell is one box at the crossing of a row and a column."
**Explain simply:**
- Workbook = a binder (.xlsx file); worksheets = pages; cells = boxes on a page.
- A worksheet has 1,048,576 rows and 16,384 columns (A to XFD) in current Excel (from memory, unverified).
- A cell holds a value, text or formula.
**Example:** The file "Attrition_2026.xlsx" (workbook) has tabs Jan, Feb, Summary (worksheets); cell B5 on Jan is one number.
**Version note:** Row/column limits apply to Excel 2007 and later (from memory, unverified).
**Edge cases:** A file can be "workbook" with chart sheets too.
**Likely follow-ups:** 1) *Max sheets?* Limited by memory.
**Common mistakes:** Saying "sheet" for the file.

### Q19 ⭐⭐⭐ 🟢 What is the difference between a value and a formula in a cell, and how do you view the formula behind a result?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Auditing habit.
**Say this in the interview:** "A value is a typed fixed entry. A formula starts with = and calculates. A formula's result changes when its inputs change. I see the formula in the formula bar, with F2, or by pressing Ctrl+` to show all formulas."
**Explain simply:**
- Typed 780 is a hard-coded value; `=A2/30*B2` is a formula and recalculates.
- Select the cell: formula bar shows the formula, cell shows the result.
- Formulas > Show Formulas, or Ctrl+` (Microsoft Support confirms the shortcut), switches the whole sheet.
**Example:** Pay for 26 days on 30000 basic.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Basic | Days | Pay |
| 2 | 30000 | 26 | 26000 |
| 3 | Fixed | | 780 |

**Formula / Steps:** C2 `=A2/30*B2`. C3 is just typed 780.
**Alternative:** `=FORMULATEXT(C2)` displays the formula as text (Excel 2013+, from memory; LibreOffice returned `=A2/30*B2` when run).
**Result:** C2 returned 26000 when run in LibreOffice; D2 FORMULATEXT returned `=A2/30*B2`.
**Version note:** FORMULATEXT from Excel 2013 (from memory, unverified).
**Edge cases:** A cell formatted as Text shows the formula itself instead of calculating (Q45).
**Likely follow-ups:** 1) *Why avoid hard-coded numbers?* They go stale. 2) *Convert formula to value?* Paste Special > Values (Q38).
**Common mistakes:** Overtyping a formula with a number; hard-coding 30 days inside formulas.

### Q20 ⭐⭐⭐ 🟡 Why does a sorted list put 10 before 2, and how do you sort numbers stored as text correctly?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Awareness of text versus number data types.
**Say this in the interview:** "Those numbers are stored as text, and text sorts character by character, so '10' comes before '2' because '1' is less than '2'. I convert them to real numbers, then sort."
**Explain simply:**
- Text-numbers often have a green corner triangle, left alignment, or come from imports.
- They don't sum: `=SUM(A1:A4)` ignored them.
- Fix: Data > Text to Columns > Finish, or multiply by 1, or VALUE.
**Example:** Employee IDs or days exported as text from an HR system.
**Sample sheet:**

| | A (text) | B (=VALUE) |
|---|---|---|
| 1 | 10 | 10 |
| 2 | 2 | 2 |
| 3 | 100 | 100 |
| 4 | 25 | 25 |

**Formula / Steps:** B1 `=VALUE(A1)` copied down, then Copy > Paste Special > Values over column A and sort. Or select column A > Data > Text to Columns > Finish.
**Alternative:** `=A1*1` or `=--A1`; also the warning icon > Convert to Number.
**Result:** Run in LibreOffice. `=SUM(A1:A4)` on text gave 0; `=SUM(B1:B4)` gave 137. Text order (Python): 10, 100, 2, 25; number order: 2, 10, 25, 100.
**Version note:** All versions (from memory, unverified).
**Edge cases:** Hidden spaces or non-breaking spaces make VALUE fail (#VALUE!); use TRIM or CLEAN first. Excel sometimes coerces text in `=A1*1` but LibreOffice behaviour can differ in edge cases.
**Likely follow-ups:** 1) *How do you detect it?* `=ISTEXT(A1)`. 2) *IDs with leading zeros?* Keep as text (Q63).
**Common mistakes:** Changing format to Number only (existing text stays text until re-entered); sorting without converting.

### Q21 ⭐⭐ 🟢 What is the Name Box, and how do you use it to jump to a cell or range?
**Asked at:** commonly asked (no company-specific report found); Name Box is in the Guru99 list.
**What the interviewer is checking:** Navigation knowledge.
**Say this in the interview:** "The Name Box is the small box left of the formula bar showing the active cell address. I type an address like D2500 or a range like B2:B500 and press Enter to jump or select."
**Explain simply:**
- It also lets you name a range: select cells, type a name like Salary, press Enter.
- Choosing a name from its drop-down jumps to that range.
- Typing A1:A5000 selects 5,000 cells with no dragging.
**Example:** Select all 5,000 salary cells by typing C2:C5001 into the Name Box.
**Formula / Steps:** Click the Name Box > type address > Enter.
**Alternative:** Go To dialog: F5 (Microsoft Support confirms F5 shows Go To).
**Version note:** Same in all versions.
**Edge cases:** Names cannot have spaces or look like cell addresses.
**Likely follow-ups:** 1) *Sheet-specific jump?* Type Sheet2!A1.
**Common mistakes:** Not pressing Enter; naming a range "Q1".

### Q22 ⭐⭐ 🟢 How do you select an entire row, an entire column and the whole sheet using the keyboard?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Keyboard fluency.
**Say this in the interview:** "Shift+Space selects the row, Ctrl+Space selects the column, Ctrl+A selects the whole sheet."
**Explain simply:**
- Click a cell first; the selection follows that cell.
- Ctrl+A inside a data block selects the block; press again for the whole sheet (per Microsoft Support it can select the current region).
- All three confirmed in Microsoft Support, Keyboard shortcuts in Excel.
**Example:** Press Ctrl+Space in column C, then Ctrl+Shift+Plus to insert a column (Q55).
**Formula / Steps:** Click cell > Shift+Space (row) / Ctrl+Space (column) / Ctrl+A (sheet).
**Alternative:** Click the row number, column letter, or the corner box above row 1.
**Version note:** Windows. Ctrl+Space can clash with input-language shortcuts on some PCs (from memory).
**Edge cases:** In a Table, Ctrl+A first selects the table data.
**Likely follow-ups:** 1) *Select to the end of data?* Q23.
**Common mistakes:** Mixing up which of Ctrl+Space and Shift+Space does what.

### Q23 ⭐⭐ 🟢 How do you move to the end of a data block or select a whole data block with the keyboard?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can work fast on big lists without scrolling with the mouse.
**Say this in the interview:** "Ctrl plus an arrow key jumps to the edge of the data block. Add Shift to select as you jump. Ctrl+Shift+* selects the whole block around the active cell."
**Explain simply:**
- A "data block" (Excel calls it the current region) is a stretch of filled cells with no completely empty row or column inside.
- Ctrl+Arrow: "Move to the edge of the current data region" (Microsoft Support, *Keyboard shortcuts in Excel*).
- Ctrl+Shift+Arrow extends the selection to the last non-blank cell in that direction (same page).
- Ctrl+Shift+* selects the current region (same page). Ctrl+A also works inside a block (from memory, unverified: pressing it a second time selects the whole sheet).
- Ctrl+End goes to the last used cell on the sheet; Ctrl+Home goes to A1.
**Example:** An attrition list has 5,000 employee rows. Click A1 of the list, press Ctrl+Shift+Down then Ctrl+Shift+Right, and the full table is selected in two key presses.
**Formula / Steps:**
1. Click any cell inside the list.
2. Ctrl+Down Arrow = jump to the last row of the block; Ctrl+Up = back to the top.
3. Ctrl+Shift+* (or Ctrl+Shift+Down, Ctrl+Shift+Right from the top-left cell) = select all of it.
**Alternative:** Click the first cell, then Shift+click the last cell; or type the range in the Name Box (Q21).
**Version note:** Same in all Excel versions on Windows. On Mac the key is Cmd instead of Ctrl for the arrows (from memory, unverified). Google Sheets also supports Ctrl+Arrow (from memory, unverified).
**Edge cases:**
- A blank cell inside the data stops the jump early. You land before the gap, not at the true end.
- Ctrl+Down on the last row of data jumps all the way to row 1,048,576.
- Hidden rows are still included in the selection.
**Likely follow-ups:**
1. *How do you select a whole column?* Ctrl+Space; a whole row is Shift+Space (Microsoft Support).
2. *Why did it stop in the middle?* A blank cell is inside the data.
**Common mistakes:** Scrolling with the mouse; forgetting that blank rows break the "block"; selecting whole columns (A:A) when a block would do.

### Q24 ⭐⭐ 🟢 How do you move to the previous and next worksheet using the keyboard?
**Asked at:** commonly asked (no company-specific report found); appears in the Guru99 Excel question list (sources file).
**What the interviewer is checking:** Basic keyboard speed in multi-sheet workbooks.
**Say this in the interview:** "Ctrl+Page Down goes to the next sheet and Ctrl+Page Up to the previous one."
**Explain simply:**
- A workbook is the file; a worksheet is one tab inside it.
- Ctrl+Page Down: "Move to the next sheet in a workbook." Ctrl+Page Up: "Move to the previous sheet" (Microsoft Support, *Keyboard shortcuts in Excel*).
- It does not wrap around: on the last sheet, Ctrl+Page Down does nothing (from memory, unverified).
**Example:** A payroll workbook has twelve month tabs, Jan to Dec. From Jan, hold Ctrl and tap Page Down three times to reach Apr.
**Formula / Steps:**
1. Hold Ctrl.
2. Press Page Down (next) or Page Up (previous).
3. To jump to a named sheet, right-click the small arrows at the bottom-left of the tab bar and pick the sheet.
**Alternative:** Click the tab with the mouse, or use the sheet list from the right-click menu.
**Version note:** All Windows versions. Mac uses Fn+Ctrl+Down/Up Arrow on laptops (from memory, unverified). Google Sheets uses Alt+Down/Up (from memory, unverified).
**Edge cases:**
- Hidden sheets are skipped.
- If several sheets are grouped, moving to another tab can ungroup them, so be careful before typing.
**Likely follow-ups:**
1. *Insert a new sheet?* Shift+F11 (Microsoft Support).
2. *Many sheets, hard to find one?* Right-click the tab arrows to see the list.
**Common mistakes:** Mixing up Page Up and Page Down; Ctrl+Tab (that switches between workbook windows or browser tabs, not sheets).

### Q25 ⭐⭐ 🟢 What is the quick way to return to a particular area of a worksheet?
**Asked at:** commonly asked (no company-specific report found); appears in the Guru99 list (sources file).
**What the interviewer is checking:** Whether you know Go To, the Name Box and named ranges.
**Say this in the interview:** "I press F5 to open Go To and type the cell or a named range. For areas I return to often, I give the range a name."
**Explain simply:**
- F5 "displays the Go To dialog box" (Microsoft Support, *Keyboard shortcuts in Excel*). Ctrl+G does the same (from memory, unverified; the Microsoft page did not list it for Windows).
- A named range is a label you give to cells, such as `Headcount`, so you jump with one word.
- The Name Box (left of the formula bar) also lets you type a cell or name and press Enter.
- Ctrl+Home goes to A1.
**Example:** The Summary sheet's attrition table is at H40:K55. Name it `AttritionTable` once; later F5 > AttritionTable lands you there and selects it.
**Formula / Steps:**
1. Select H40:K55.
2. Click the Name Box, type `AttritionTable`, press Enter (Formulas tab > Define Name also works).
3. Any time later: F5 > pick AttritionTable > OK.
**Alternative:** Insert a hyperlink to a cell (Ctrl+K > Place in This Document) so you can click to jump.
**Version note:** Works in all versions; Google Sheets uses the "Named ranges" panel and Ctrl+J for "jump to range" (from memory, unverified).
**Edge cases:**
- A name is workbook-wide by default, so it works from any sheet.
- Names cannot contain spaces or look like cell addresses (for example `AB12`).
**Likely follow-ups:**
1. *Can Go To select special cells?* Yes, F5 > Special lets you pick blanks, formulas, constants and more (from memory, unverified).
**Common mistakes:** Scrolling manually; typing a range name with a space; forgetting the sheet name when jumping to another sheet's cell (use `Jan!B5`).

### Q26 ⭐⭐ 🟢 How do you use AutoFill to copy a formula or create a series of dates or numbers down a column?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can fill formulas and series quickly and know why the references shift.
**Say this in the interview:** "I drag the small square at the corner of the cell, called the fill handle. For a long column I double-click it. Excel adjusts relative references as it goes."
**Explain simply:**
- AutoFill = Excel continues a pattern or copies a formula when you drag the fill handle (the small green square at the bottom-right of the selected cell).
- A formula such as `=B2*10%` becomes `=B3*10%` one row down because references are "relative" (they move).
- Type 1 and 2, select both, drag: Excel continues 3, 4, 5.
- Double-click the handle to fill down as far as the neighbouring column has data.
- The small icon after filling (Auto Fill Options) lets you switch between Copy Cells, Fill Series and Fill Formatting Only.
**Example:** Bonus is 10% of basic pay for 3 employees. Enter the formula once, fill down.
**Sample sheet:**
| | A | B | C | D | E |
|---|---|---|---|---|---|
| 1 | Emp | Basic | Bonus 10% | Month end | No. |
| 2 | E01 | 30000 | `=B2*10%` | 31-Jan-2026 | 1 |
| 3 | E02 | 45000 | `=B3*10%` | `=EOMONTH(D2,1)` | `=E2+1` |
| 4 | E03 | 28000 | `=B4*10%` | `=EOMONTH(D3,1)` | `=E3+1` |

**Formula / Steps:**
1. In C2 type `=B2*10%`, press Enter.
2. Click C2, double-click the fill handle (or drag to C4); or select C2:C4 and press Ctrl+D (Fill Down; Microsoft Support).
3. For a numeric series: Home tab > Editing group > Fill > Series, pick Linear, set Step value and Stop value.
**Alternative:** `=E2+1` filled down, or `=ROW()-1`, builds 1, 2, 3 without dragging two seed cells.
**Result (run in LibreOffice):** C2:C4 = 3000, 4500, 2800; E2:E4 = 1, 2, 3; D3 and D4 return the serials for 28-Feb-2026 and 31-Mar-2026 (the cells need a date format, see Q41).
**Version note:** All Excel versions. Google Sheets has the same fill handle (from memory, unverified).
**Edge cases:**
- Dragging a single number copies it; to count, hold Ctrl while dragging (from memory, unverified) or use Fill Series.
- Dragging a single date continues day by day; use the options icon for months or years.
- Double-click stops at the first blank cell in the neighbouring column.
- To stop a reference moving, lock it with F4 (`$B$2`).
**Likely follow-ups:**
1. *Fill without changing formatting?* Auto Fill Options > Fill Without Formatting.
2. *Weekdays only?* Auto Fill Options > Fill Weekdays.
**Common mistakes:** Dragging when the neighbouring column has gaps; forgetting absolute references; leaving calculation on Manual so filled formulas show old values.

### Q27 ⭐⭐ 🟢 What is Format Cells, and how do you open it quickly?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know where all formatting controls live.
**Say this in the interview:** "Format Cells is the dialog box that controls how a cell looks: number format, alignment, font, border, fill and protection. I open it with Ctrl+1."
**Explain simply:**
- Ctrl+1 will "Open the Format Cells dialog box" (Microsoft Support, *Keyboard shortcuts in Excel*).
- Tabs: Number, Alignment, Font, Border, Fill, Protection.
- Formatting changes only the display, not the stored value. A cell showing 12% still holds 0.12.
- Other routes: right-click > Format Cells, or the small arrow at the corner of the Number/Alignment/Font group on the Home tab.
**Example:** A joining date stored as 45678 becomes 21-Jan-2025 after choosing Date in the Number tab. The underlying number does not change.
**Formula / Steps:**
1. Select the cells.
2. Press Ctrl+1.
3. Pick a tab, choose options, click OK.
**Alternative:** Right-click > Format Cells, or Home tab > Number group > dialog launcher arrow.
**Version note:** Ctrl+1 works in all Windows versions; on Mac it is Cmd+1 (from memory, unverified). Google Sheets has a Format menu instead.
**Edge cases:**
- Changing a text-formatted cell to Number does not convert existing text. You must re-enter the value (see Q20).
- Custom formats (Number tab > Custom) only change what you see.
**Likely follow-ups:**
1. *Does formatting change the value?* No, only the display.
2. *Quick currency format?* Ctrl+Shift+$ (Microsoft Support).
**Common mistakes:** Thinking rounding by format changes the actual value in calculations; hunting through the ribbon instead of Ctrl+1.

### Q28 ⭐⭐ 🟢 What are the differences between the General, Number, Currency and Accounting formats?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you understand number display formats.
**Say this in the interview:** "General shows the number as typed. Number adds decimals and thousand separators. Currency adds a symbol next to the number. Accounting lines up the symbols and decimal points in a column."
**Explain simply:**
- General: the default, no special format; shows what you typed (long numbers may switch to scientific form).
- Number: you choose decimal places, thousand separator and how negatives look.
- Currency: symbol sits right next to the number (₹1,234.50); negatives can be red or in brackets.
- Accounting: symbol is pushed to the left edge of the cell and numbers line up on the decimal point; zero shows as a dash; no red negative option (from memory, unverified).
- All four only change display; the value stays the same.
**Example:** A payroll column of 1,234.5 and 98,000: Currency shows ₹1,234.50 and ₹98,000.00 side by side; Accounting puts all ₹ signs at the left edge, so totals are easy to read.
**Sample sheet:**
| | A | B | C | D | E |
|---|---|---|---|---|---|
| 1 | 1234.5 | `=TEXT(A1,"0.00")` | `=TEXT(A1,"#,##0.00")` | `=TEXT(A1,"$#,##0.00")` | `=ISNUMBER(A1)` |

**Formula / Steps:** Select cells > Ctrl+1 > Number tab > pick category. Shortcuts: Ctrl+Shift+$ = Currency with two decimals (Microsoft Support).
**Alternative:** Home tab > Number group > dropdown (General/Number/Currency/Accounting), or the ₹/$ button which applies Accounting (from memory, unverified).
**Result (run in LibreOffice, TEXT mimics the formats):** B1 `1234.50`, C1 `1,234.50`, D1 `$1,234.50`, E1 `TRUE`. TEXT returns text, so use it only for labels.
**Version note:** All versions. Currency symbol follows the computer's regional setting.
**Edge cases:**
- Number formats on text-numbers do nothing (Q20).
- Very long IDs (such as 16-digit numbers) lose digits in General or Number; store IDs as Text.
**Likely follow-ups:**
1. *Which for a financial report?* Accounting.
2. *Does the format change SUM?* No.
**Common mistakes:** Using TEXT() and then trying to add the results; storing phone numbers or employee IDs as Number.

### Q29 ⭐⭐ 🟢 How do you wrap text within a cell, and how is it different from merging cells?
**Asked at:** commonly asked; appears in the Guru99 Excel list (sources file).
**What the interviewer is checking:** Whether you handle long text without breaking the grid.
**Say this in the interview:** "Wrap Text breaks long text onto several lines inside the same cell. Merge joins several cells into one big cell. Wrap keeps the structure intact; merge does not."
**Explain simply:**
- Wrap Text: row height grows so all the text is visible; the cell count does not change.
- Merge: several cells become one; only the top-left value survives.
- Alt+Enter inserts a manual line break at the cursor while typing (from memory, unverified).
**Example:** A "Feedback comments" column in an exit-interview sheet has 120-character remarks. Wrap Text makes every comment readable in a column that is 30 characters wide.
**Formula / Steps:**
1. Select the cells.
2. Home tab > Alignment group > Wrap Text.
3. Double-click the row border to auto-fit the height if needed.
**Alternative:** Ctrl+1 > Alignment tab > tick Wrap text.
**Version note:** All versions; Google Sheets has Text wrapping > Wrap in the toolbar (from memory, unverified).
**Edge cases:**
- If the row height was set manually, wrapped text can be cut off; use AutoFit Row Height.
- Merged cells with wrapped text do not auto-fit height (from memory, unverified).
**Likely follow-ups:**
1. *Shrink to fit instead?* Alignment tab > Shrink to fit makes the font smaller.
**Common mistakes:** Merging cells to fit a long title; leaving a fixed row height.

### Q30 ⭐⭐ 🟢 What is the difference between Merge & Center and Center Across Selection, and why do analysts avoid merged cells in data tables?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you build tables that sort, filter and pivot properly.
**Say this in the interview:** "Merge & Center physically joins cells. Center Across Selection only centres the text visually over several cells and leaves them separate, so sorting and selecting still work. I avoid merging inside data."
**Explain simply:**
- Merge & Center: Home tab > Alignment group > Merge & Center. The cells become one; data in the other cells is deleted.
- Center Across Selection: Ctrl+1 > Alignment > Horizontal > Center Across Selection. The text sits in the leftmost cell but looks centred; each cell stays separate.
- Merged cells in a table break Sort (Excel shows an error saying cells need the same size), break filtering, and mess up Ctrl+Arrow, pivot tables and formulas that fill down (from memory, unverified).
**Example:** A monthly headcount report has the title "Q1 Headcount" over columns A to D. With Center Across Selection the title looks centred, and you can still sort the table below.
**Formula / Steps:**
1. Type the title in A1, select A1:D1.
2. Ctrl+1 > Alignment tab > Horizontal > Center Across Selection > OK.
3. To undo a merge: Home > Merge & Center (toggle off).
**Alternative:** Put the title in one cell and left-align it; no centring needed.
**Version note:** Both features exist in all versions. Google Sheets has Merge but no Center Across Selection (from memory, unverified).
**Edge cases:**
- Merged cells in a pivot-table source cause blank cells in the unmerged column.
- Unmerging leaves only the first cell filled; fill the rest down.
**Likely follow-ups:**
1. *How to fix merged cells in a table?* Unmerge, then fill blanks with the value above (Go To Special > Blanks, then `=` and Up Arrow, Ctrl+Enter).
**Common mistakes:** Merging header cells in a data table; merging rows of data; not knowing Center Across Selection exists.

### Q31 ⭐⭐ 🟢 What are left, right, fill and distributed alignments?
**Asked at:** commonly asked; alignments appear in the Guru99 list (sources file).
**What the interviewer is checking:** Familiarity with Format Cells > Alignment options.
**Say this in the interview:** "Left and right push content to that edge. Fill repeats the content to fill the cell width. Distributed spreads the characters evenly across the width."
**Explain simply:**
- By default, text sits left and numbers sit right (General alignment).
- Left (Indent) / Right (Indent): force the edge and let you indent.
- Fill: repeats the cell's text as many times as fit, for example `-` becomes `----------`. Handy for dividers.
- Distributed (Indent): spaces words or letters evenly from edge to edge.
- Other options in the same list: Center, Justify, Center Across Selection (Q30).
**Example:** In a muster sheet, `Present` set to Distributed fills the cell neatly; a `-` cell set to Fill makes a separator line.
**Formula / Steps:**
1. Select cells > Ctrl+1 > Alignment tab.
2. Open the Horizontal dropdown.
3. Choose Left (Indent), Right (Indent), Fill or Distributed (Indent) > OK.
**Alternative:** Home tab > Alignment group buttons for Left, Center, Right (Fill and Distributed are only in Format Cells).
**Version note:** All Excel versions (from memory, unverified). Google Sheets only has left, centre and right.
**Edge cases:**
- Fill alignment on a number repeats its digits visually but the value stays the same.
- Right-aligned text-numbers hint they are stored as text only if they were left-aligned by default (Q20).
**Likely follow-ups:**
1. *Why are my numbers left-aligned?* They are stored as text.
**Common mistakes:** Padding with spaces instead of using indent; using Fill on real data cells.

### Q32 ⭐⭐ 🟢 How do you convert a plain data range into an Excel Table, and what are its advantages?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you build maintainable data sets.
**Say this in the interview:** "I click inside the data and press Ctrl+T. A Table grows automatically when I add rows, copies formulas down, has built-in filter buttons and lets me use column names in formulas."
**Explain simply:**
- Ctrl+T "Display the Create Table dialog box" (Microsoft Support, *Keyboard shortcuts in Excel*).
- Advantages (from memory, unverified): automatic expansion; filter and sort buttons; banded rows; calculated columns that fill down; structured references such as `=SUM(Hires[Salary])`; pivot tables and charts update when the table grows; a Total Row option.
- A Table needs one header row with unique names and no merged cells.
**Example:** A hiring tracker named `Hires` has 200 rows. Next week you paste 20 new rows underneath. The Table expands, and a pivot table on it picks them up after a Refresh.
**Formula / Steps:**
1. Click any cell in the data.
2. Insert tab > Tables group > Table (or Ctrl+T).
3. Tick "My table has headers" > OK.
4. Table Design tab > Table Name box: give it a name like `Hires`.
**Alternative:** Home tab > Styles group > Format as Table.
**Result:** Not run here (LibreOffice cannot create Excel Tables). Example formula in a new column: `=[@Salary]*12` fills every row.
**Version note:** Tables exist since Excel 2007 (from memory, unverified). Google Sheets has a separate "Table" feature (from memory, unverified). The Microsoft "Create a table" page returned 404 so version facts are unconfirmed.
**Edge cases:**
- Converting back: Table Design > Convert to Range.
- Blank header cells get names like Column1.
- A Table cannot contain merged cells and has limits with some features (from memory, unverified).
**Likely follow-ups:**
1. *What is a structured reference?* A column name used instead of cell addresses.
2. *Table vs named range?* A Table grows on its own.
**Common mistakes:** Leaving blank rows in the data; forgetting to rename the table; typing totals under the Table instead of using the Total Row.

### Q33 ⭐⭐ 🟢 How do you filter for text that contains a word, for example every job title containing 'Analyst'?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Use of Text Filters and wildcards.
**Say this in the interview:** "I turn on the filter, open the dropdown on Job Title, choose Text Filters > Contains and type Analyst. Or I type Analyst straight into the search box."
**Explain simply:**
- Filter hides rows that do not match; it does not delete them.
- "Contains" matches the word anywhere in the cell and ignores capital letters.
- The same idea in formulas uses wildcards: `*` stands for "any number of characters".
**Example:** From a list of job titles, show every title containing Analyst.
**Sample sheet:**
| | A (Title) |
|---|---|
| 2 | Data Analyst |
| 3 | Senior Analyst |
| 4 | HR Executive |
| 5 | Analytics Manager |
| 6 | Payroll Analyst - II |
| 7 | analyst trainee |

**Formula / Steps:**
1. Click inside the data > Data tab > Filter (Ctrl+Shift+L).
2. Click the dropdown on Job Title > Text Filters > Contains.
3. Type `Analyst` > OK.
Counting the same rows by formula: `=COUNTIF(A2:A7,"*Analyst*")`.
**Alternative:** `=SUMPRODUCT(--ISNUMBER(SEARCH("Analyst",A2:A7)))` counts without needing wildcards.
**Result (run in LibreOffice):** both formulas return 4 (Data Analyst, Senior Analyst, Payroll Analyst - II, analyst trainee). "Analytics Manager" does not match, because "Analytics" does not contain "Analyst". `"Analyst*"` (starts with) returns 1; `"*Analyst"` (ends with) returns 2.
**Version note:** Text Filters exist in all versions; the formula route works in all versions too. Filter shortcut: Ctrl+Shift+L is listed for Excel for the web in the Microsoft page and works on desktop too (desktop from memory, unverified).
**Edge cases:**
- Contains is not case sensitive. Leading/trailing spaces can hide matches; use TRIM.
- Filters do not update automatically when data changes; reapply (Data > Reapply).
**Likely follow-ups:**
1. *Starts with?* Text Filters > Begins With.
2. *Two words?* Custom filter with Or.
**Common mistakes:** Forgetting that "Analytics" is a different word; filtering a range with blank rows so only part is filtered.

### Q34 ⭐⭐ 🟢 How do you filter by cell colour or font colour, and how do you sort by colour?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can use manual highlights from other people's sheets.
**Say this in the interview:** "In the filter dropdown I choose Filter by Color and pick the fill or font colour. For sorting I use Data > Sort, Sort On Cell Color, and choose which colour goes on top."
**Explain simply:**
- Filter by Color needs the filter turned on first.
- The dropdown lists only the colours actually used in that column.
- Sort by colour lets you place red rows first, then yellow, and so on, using extra sort levels.
- Colour is a visual mark only. Formulas such as SUMIF cannot read colour.
**Example:** A manager highlighted late-joiners in yellow in a 300-row onboarding list. Filter by yellow to count and list them.
**Formula / Steps:**
1. Data tab > Filter.
2. Dropdown on the column > Filter by Color > pick a cell colour or font colour.
Sort: Data tab > Sort > Sort On: Cell Color (or Font Color) > choose the colour and "On Top" > Add Level for the next colour.
**Alternative:** Add a helper column such as `Status` with text ("Late") so formulas can count it; better than relying on colour.
**Result:** Not run here (formatting is not a formula). Counting coloured rows needs the filter plus the status bar count or SUBTOTAL(103,...) on visible rows (from memory, unverified).
**Version note:** Filter and sort by colour exist since Excel 2007 (from memory, unverified). Google Sheets supports filter by colour too (from memory, unverified).
**Edge cases:**
- Colours from conditional formatting can also be filtered (from memory, unverified).
- Slightly different shades appear as separate colours.
**Likely follow-ups:**
1. *Can you sum by colour with a formula?* Not natively; use a helper column or VBA.
**Common mistakes:** Relying on colour as data; not clearing the filter before saving or sharing.

### Q35 ⭐⭐ 🟢 How do you filter numbers using greater than, between and Top 10 options?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Number Filters knowledge.
**Say this in the interview:** "In the dropdown I choose Number Filters, then Greater Than, Between or Top 10. Top 10 can be set to top or bottom, items or percent, and any number."
**Explain simply:**
- Greater Than: keep values above a limit. Between: keep values inside a range (inclusive).
- Top 10: despite the name, you can set any number, such as top 3 items or top 10 percent.
- Filters on different columns combine with AND; filters are additive (Microsoft Support, *Use AutoFilter to filter your data*, seen in search snippet only).
**Example:** Salaries of six employees; find those above 50,000, between 40,000 and 60,000 and the top 3.
**Sample sheet:**
| | A (Salary) |
|---|---|
| 2 | 35000 |
| 3 | 52000 |
| 4 | 61000 |
| 5 | 48000 |
| 6 | 75000 |
| 7 | 52000 |

**Formula / Steps:**
1. Data > Filter > dropdown on Salary > Number Filters.
2. Greater Than: enter 50000. Between: 40000 and 60000. Top 10: Top, 3, Items.
Formula checks: `=COUNTIF(A2:A7,">50000")`, `=COUNTIFS(A2:A7,">=40000",A2:A7,"<=60000")`, `=LARGE(A2:A7,3)`.
**Alternative:** `=SUMPRODUCT((A2:A7>=40000)*(A2:A7<=60000))` for the between count.
**Result (run in LibreOffice):** greater than 50,000: 4; between 40,000 and 60,000: 3 (52,000, 48,000, 52,000); third-largest: 52,000. Top 3 items filter shows 4 rows (75,000, 61,000 and both 52,000), because ties are all kept (`=COUNTIF(A2:A7,">="&LARGE(A2:A7,3))` returned 4; the tie behaviour of the filter itself is from memory, unverified).
**Version note:** All versions. In Google Sheets there is no Top 10 filter (from memory, unverified).
**Edge cases:**
- Text-numbers do not appear in Number Filters (Q20).
- Between is inclusive of both ends.
**Likely follow-ups:**
1. *Top 10 percent?* Choose Percent instead of Items.
**Common mistakes:** Thinking Top 10 means exactly 10; filtering numbers stored as text.

### Q36 ⭐⭐ 🟢 How do you filter dates by month, quarter or 'this week' using the date filter?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you use the date filter and know that dates are real numbers.
**Say this in the interview:** "In the dropdown, Date Filters has ready options like This Week, This Month and Next Quarter, plus All Dates in the Period for any month or quarter."
**Explain simply:**
- Excel stores a date as a serial number, so it can be compared and grouped.
- Date Filters offers Today, This Week, This Month, This Quarter, Last Year and more; "All Dates in the Period" lets you pick Quarter 1-4 or a month.
- The filter list can group dates into Year > Month > Day (from memory, unverified; can be switched off in Options).
- Filters on text-dates ("Jan 5" typed as text) do not show these options.
**Example:** Join dates of five hires; see who joined in Q2.
**Sample sheet:**
| | A (Join date) | B (Month) | C (Quarter) |
|---|---|---|---|
| 2 | 15-Jan-2026 | `=MONTH(A2)` | `="Q"&ROUNDUP(MONTH(A2)/3,0)` |
| 3 | 03-Feb-2026 | | |
| 4 | 20-Apr-2026 | | |
| 5 | 09-May-2026 | | |
| 6 | 01-Jul-2026 | | |

**Formula / Steps:**
1. Data > Filter > dropdown on Join date > Date Filters.
2. Pick This Month, This Week, or All Dates in the Period > Quarter 2.
Formula for Q2 count: `=COUNTIFS(A2:A6,">="&DATE(2026,4,1),A2:A6,"<="&DATE(2026,6,30))`.
**Alternative:** Add helper columns for month and quarter (columns B, C) and filter on those.
**Result (run in LibreOffice):** months 1, 2, 4, 5, 7; quarters Q1, Q1, Q2, Q2, Q3; Q2 count = 2.
**Version note:** Date Filters exist in all versions. "This Week" depends on the system date and week start (from memory, unverified). Quarter here means calendar quarter; Indian financial-year quarters start in April, so use a helper column for FY quarters.
**Edge cases:**
- Dates with time parts may fall outside a "between" filter.
- Text-dates need converting first (Q41).
**Likely follow-ups:**
1. *Financial year quarter?* Helper column with a formula that shifts months by 3.
**Common mistakes:** Filtering text-dates; confusing calendar and financial quarters.

### Q37 ⭐⭐ 🟢 What do the wildcard characters * and ? do when you type them in the filter search box?
**Asked at:** commonly asked; wildcards in filters are documented by Microsoft (search snippet only).
**What the interviewer is checking:** Pattern matching in filters.
**Say this in the interview:** "Star stands for any number of characters, question mark for exactly one character. And tilde lets me search for a real star or question mark."
**Explain simply:**
- `*` = zero or more characters; `?` = exactly one character; `~` placed before `*` or `?` makes it literal.
- In the filter search box, typed text already matches "contains"; wildcards let you anchor the pattern.
**Example:** Employee IDs: `EMP*` = starts with EMP; `EMP???` = EMP followed by exactly 3 characters; `*001` = ends with 001.
**Sample sheet:**
| | A (ID) |
|---|---|
| 2 | EMP001 |
| 3 | EMP02 |
| 4 | EMP0034 |
| 5 | TMP001 |
| 6 | EMP-001 |
| 7 | AB |

**Formula / Steps:** Filter dropdown > type the pattern in the Search box > OK. The same patterns work in `COUNTIF`: `=COUNTIF(A2:A7,"EMP*")`.
**Alternative:** Text Filters > Begins With / Ends With / Contains.
**Result (run in LibreOffice):** `"EMP*"` = 4; `"EMP???"` = 1 (EMP001); `"??"` = 1 (AB); `"*001"` = 3 (EMP001, TMP001, EMP-001); `"EMP~*"` = 0.
**Version note:** Works in all versions. Google Sheets uses `*` and `?` in COUNTIF but filter search differs (from memory, unverified).
**Edge cases:**
- Wildcards work on text, not on numbers.
- Matching is not case sensitive.
**Likely follow-ups:**
1. *Find a real question mark?* Use `~?`.
**Common mistakes:** Using `%` or `_` like SQL; forgetting a space counts as a character.

### Q38 ⭐⭐ 🟢 How do you use Paste Special to paste only values, only formats or transposed data?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Controlled pasting.
**Say this in the interview:** "I copy, then open Paste Special with Ctrl+Alt+V and choose Values, Formats or tick Transpose."
**Explain simply:**
- Normal paste brings everything: value, formula, format.
- Values: keeps only results, so formulas turn into fixed numbers.
- Formats: copies the look only.
- Transpose: flips rows to columns and columns to rows.
- Ctrl+Alt+V "Open the Paste Special dialog box" (Microsoft Support, *Keyboard shortcuts in Excel*).
**Example:** A headcount report has `=A1+A2` giving 350. Paste it as values to send a fixed 350 that will not change if inputs change.
**Sample sheet:**
| | A | B | C |
|---|---|---|---|
| 1 | 100 | `=A3*2` | `=SUM(A1:A3)` |
| 2 | 250 | | |
| 3 | `=A1+A2` | | |

**Formula / Steps:**
1. Select and copy (Ctrl+C).
2. Click the target cell > Home > Paste dropdown > Paste Special (or Ctrl+Alt+V).
3. Choose Values, Formats, or tick Transpose > OK.
**Alternative:** Transpose with a function: `=TRANSPOSE(A1:A3)` (array formula; live link; from memory, unverified on spill rules by version).
**Result:** The formulas return A3 = 350, B1 = 700, C1 = 700 in LibreOffice. Paste Special itself is a feature and was not run here.
**Version note:** All versions have Paste Special; Google Sheets has Paste special in the Edit menu (from memory, unverified).
**Edge cases:**
- After pasting values, links to the source are gone.
- Paste values keeps the destination's formats only if you choose Values (not "Values & Source Formatting").
**Likely follow-ups:**
1. *Paste column widths?* Paste Special > Column widths.
2. *Multiply all numbers by 1000?* Paste Special > Multiply.
**Common mistakes:** Pasting formulas to another workbook and getting broken links; pasting values over the original data.

### Q39 ⭐⭐ 🟢 How do you add a new worksheet, and how do you rename, move or copy one?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Workbook basics.
**Say this in the interview:** "Click the plus button or press Shift+F11 to add. Double-click the tab to rename. Drag to move, and hold Ctrl while dragging to copy."
**Explain simply:**
- Shift+F11 "inserts a new worksheet" (Microsoft Support, *Keyboard shortcuts in Excel*).
- Right-click a tab for Insert, Delete, Rename, Move or Copy, Tab Color, Hide.
- Move or Copy dialog can send the sheet to another open workbook.
- Sheet names: up to 31 characters, no `\ / ? * [ ] :` (from memory, unverified).
**Example:** Copy the "Jan" sheet to make "Feb", then rename it. The layout and formulas come with it.
**Formula / Steps:**
1. Add: click + beside the tabs or press Shift+F11.
2. Rename: double-click the tab, type the name, Enter.
3. Move: drag the tab left or right.
4. Copy: Ctrl+drag, or right-click > Move or Copy > tick "Create a copy".
**Alternative:** Home tab > Cells group > Insert > Insert Sheet; Format > Rename Sheet.
**Version note:** All versions; Google Sheets right-click tab > Duplicate (from memory, unverified).
**Edge cases:**
- Formulas that refer to a renamed sheet update automatically.
- Copying a sheet with named ranges can create duplicate names.
- A grouped selection of sheets applies edits to all of them.
**Likely follow-ups:**
1. *Copy to another workbook?* Move or Copy > To book.
**Common mistakes:** Leaving "Sheet1"-style names; typing while sheets are grouped.

### Q40 ⭐⭐ 🟢 How do you hide and unhide rows, columns and sheets?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Basic data hygiene and awareness of hidden content.
**Say this in the interview:** "Select the rows or columns, right-click and choose Hide. To unhide, select the neighbours on both sides and choose Unhide. Sheets work the same from the tab's right-click menu."
**Explain simply:**
- Ctrl+9 "Hide the selected rows", Ctrl+0 "Hide the selected columns" (Microsoft Support, *Keyboard shortcuts in Excel*).
- Ctrl+Shift+9 unhides rows (the Microsoft page lists it for Excel for the web; on desktop from memory, unverified). Ctrl+Shift+0 for columns often fails on Windows because of a system setting (from memory, unverified).
- Hidden data is still in the file and still counted by SUM; it is not security.
**Example:** Hide the salary column before sharing a sheet with a manager; unhide it later.
**Formula / Steps:**
1. Rows/columns: select > right-click > Hide. Unhide: select the rows/columns on each side > right-click > Unhide.
2. Sheets: right-click the tab > Hide; to restore, right-click any tab > Unhide > pick the sheet.
3. Ribbon: Home > Cells group > Format > Hide & Unhide.
**Alternative:** Drag a column border to zero width; or use Data > Group so you can expand with a + button.
**Version note:** All versions. "Very hidden" sheets can only be unhidden via the VBA editor (from memory, unverified).
**Edge cases:**
- Filters hide rows too, but they are removed by clearing the filter, not by Unhide.
- SUBTOTAL(109,...) ignores manually hidden rows; SUM does not.
- Row 1 or column A hidden is hard to unhide: click the Name Box, type A1, then Unhide.
**Likely follow-ups:**
1. *Is hiding secure?* No; protect with a password and remove sensitive data instead.
**Common mistakes:** Forgetting hidden columns still feed formulas; sharing files with hidden salary data.

### Q41 ⭐⭐ 🟢 How do you format a date column that shows as 45678 or ##### in the cells?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Knowing dates are serial numbers and diagnosing ##### .
**Say this in the interview:** "45678 is a date stored as a plain number. I apply a Date format with Ctrl+Shift+#. If I see #####, the column is too narrow, so I widen it; a negative date also shows ##### ."
**Explain simply:**
- Excel counts days from 1 January 1900 (serial 1). Serial 45678 is 21-Jan-2025 (checked by running TEXT in LibreOffice; Excel's 1900 calendar is the same for modern dates).
- The cell is just formatted as General or Number.
- Ctrl+Shift+# "Apply the Date format with the day, month, and year" (Microsoft Support).
- ##### means the column is too narrow, or the value is a negative date/time.
**Example:** Date of joining exported from an HRMS shows 45678. After formatting you see 21-Jan-2025.
**Sample sheet:**
| | A |
|---|---|
| 2 | 45678 |
| 3 | `=TEXT(A2,"dd-mmm-yyyy")` |
| 4 | `=TEXT(A2,"dddd")` |
| 5 | `=A2+30` |
| 6 | `=DATEVALUE("25-Jan-2025")` |

**Formula / Steps:**
1. Select the column.
2. Ctrl+1 > Number tab > Date (or Custom `dd-mmm-yyyy`) > OK, or Home > Number dropdown > Short Date.
3. For #####: double-click the column border to auto-fit.
**Alternative:** `=TEXT(A2,"dd-mmm-yyyy")` returns text (not a real date; use only for display).
**Result (run in LibreOffice):** A3 `21-Jan-2025`, A4 `Tuesday`, A5 45708 (= 20-Feb-2025), A6 45682. The `DATEVALUE` of text "25-Jan-2025" returns the serial 45682; text-date parsing depends on your regional settings.
**Version note:** All versions. Excel for Mac uses a different default date system in very old files (1904; from memory, unverified).
**Edge cases:**
- Dates imported as text (left-aligned) do not change with formatting; convert with DATEVALUE or Text to Columns.
- Day-month order depends on the regional setting (dd/mm vs mm/dd).
- Negative results show ##### in the 1900 system.
**Likely follow-ups:**
1. *Why did the date turn into a number when I changed the format to General?* Because it is stored as a serial.
**Common mistakes:** Re-typing the dates; using TEXT and then trying to calculate with the result; not checking the regional date order.

### Q42 ⭐⭐ 🟢 How do you set the print area, print titles (repeat header row) and fit a sheet to one page wide?
**Asked at:** commonly asked; print setup is standard for MIS roles (sources file).
**What the interviewer is checking:** Report presentation basics.
**Say this in the interview:** "On the Page Layout tab I set Print Area, then Print Titles to repeat row 1 on every page, and in Scale to Fit I set Width to one page and Height to automatic."
**Explain simply:**
- Print area = the range that prints; the rest is ignored.
- Print titles = rows (or columns) repeated at the top of every page.
- Fit to one page wide shrinks columns so none spill onto a second page.
**Example:** A 400-row attendance report prints on 9 pages; with row 1 repeated and width fit to 1 page, every page has headers and no column is cut.
**Formula / Steps:**
1. Select the range > Page Layout tab > Page Setup group > Print Area > Set Print Area.
2. Page Layout > Print Titles > Sheet tab > Rows to repeat at top: `$1:$1` > OK.
3. Page Layout > Scale to Fit group > Width: 1 page, Height: Automatic.
4. Check with File > Print (Ctrl+P) preview.
**Alternative:** File > Print > Settings > Fit All Columns on One Page; or View > Page Break Preview to drag the blue lines.
**Result:** Not run here (print settings are not formulas).
**Version note:** All versions (from memory, unverified). Google Sheets: File > Print has "Fit to width" and "Repeat frozen rows" (from memory, unverified).
**Edge cases:**
- Setting Height to 1 as well squeezes a long report into tiny print.
- Hidden rows and columns do not print.
- Clear Print Area removes the setting.
**Likely follow-ups:**
1. *Landscape?* Page Layout > Orientation > Landscape.
**Common mistakes:** Printing without a preview; forgetting to repeat headers; setting fit-to-one-page for everything.

### Q43 ⭐⭐ 🟢 What is the use of Find & Replace, and how do you find all cells with a particular value or format?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Cleaning and auditing data quickly.
**Say this in the interview:** "Ctrl+F finds, Ctrl+H replaces. Find All lists every match with its address, and Options lets me match case, whole cell, or even a format."
**Explain simply:**
- Find All shows a list of every matching cell; click an item to jump to it, or Ctrl+A in the list to select all matches.
- Options: Within (Sheet/Workbook), Look in (Formulas/Values/Comments), Match case, Match entire cell contents.
- Format button: find or replace by cell formatting such as fill colour.
- Wildcards `*` and `?` work here too.
- Ctrl+H: Mac section of the Microsoft page lists it; on Windows from memory, unverified. Ctrl+F is listed for Excel for the web (Microsoft Support).
**Example:** An HR export has "Attrition", "attrition rate", "Attr." and "ATTRITION". Replacing needs care.
**Sample sheet:**
| | A | B |
|---|---|---|
| 2 | Attrition | `=COUNTIF(A2:A5,"attrition")` |
| 3 | attrition rate | `=COUNTIF(A2:A5,"attrition*")` |
| 4 | Attr. | `=SUMPRODUCT(--EXACT(A2:A5,"attrition"))` |
| 5 | ATTRITION | |

**Formula / Steps:**
1. Ctrl+F > type value > Options > Find All.
2. Replace: Ctrl+H > Find what / Replace with > Replace All (check the preview first).
3. By format: Options > Format > choose format > Find All.
**Alternative:** `SUBSTITUTE(A3,"attrition","Exit")` returns `Exit rate` in LibreOffice and keeps the original untouched.
**Result (run in LibreOffice):** `COUNTIF(...,"attrition")` = 2 (case ignored: Attrition, ATTRITION); `"attrition*"` = 3; case-sensitive `EXACT` count = 0, because no cell is exactly lowercase "attrition".
**Version note:** All versions; Google Sheets has Find and replace with "Match case" (from memory, unverified).
**Edge cases:**
- Without "Match entire cell contents", "Attr" also matches "Attrition".
- Replace All cannot be undone selectively; save a copy first.
- Find in Formulas vs Values gives different results for calculated cells.
**Likely follow-ups:**
1. *Remove a character?* Replace with nothing.
**Common mistakes:** Replace All without checking; forgetting the search scope is the selection if cells are selected.

### Q44 ⭐⭐ 🟢 How do you refer to a cell in another worksheet in a formula (for example Jan!B5)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Cross-sheet references, the foundation of consolidation.
**Say this in the interview:** "I write the sheet name, an exclamation mark, then the cell, like `=Jan!B5`. If the name has spaces I put it in single quotes."
**Explain simply:**
- Easiest way: type `=`, click the other sheet's tab, click the cell, press Enter. Excel writes the reference.
- The `!` separates the sheet name from the cell address.
- Names with spaces or special characters need quotes: `='Jan 2026'!B5`.
- Ranges work too: `=SUM(Jan!B5:B6)`.
**Example:** A Summary sheet collects January payroll from the Jan sheet.
**Sample sheet:**
| | Jan: B | Summary: B |
|---|---|---|
| 5 | 1200 | `=Jan!B5` |
| 6 | 800 | `=SUM(Jan!B5:B6)` |
| 7 | | `=Jan!B5*2` |

**Formula / Steps:** On Summary, click B2, type `=`, click the Jan tab, click B5, press Enter.
**Alternative:** `=INDIRECT("Jan!B5")` (text-driven sheet name; volatile, slower). Also 3D references like `=SUM(Jan:Mar!B5)` add the same cell across consecutive sheets (from memory, unverified).
**Result (run in LibreOffice):** `=Jan!B5` = 1200; `=SUM(Jan!B5:B6)` = 2000; `='Jan'!B5*2` = 2400.
**Version note:** All versions. Google Sheets: `=Jan!B5` the same; across files use IMPORTRANGE (from memory, unverified).
**Edge cases:**
- Renaming the sheet updates formulas; deleting the sheet gives #REF!.
- Another workbook is written `=[Book2.xlsx]Jan!B5` (from memory, unverified).
**Likely follow-ups:**
1. *Same cell from 12 sheets?* 3D reference `Jan:Dec!B5`.
**Common mistakes:** Forgetting quotes around names with spaces; typing the name wrongly; deleting source sheets.

### Q45 ⭐⭐ 🟢 How do you stop formulas showing as text, and what does an apostrophe at the start of a cell do?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know that a cell's format and a leading apostrophe decide whether Excel calculates or just displays?
**Say this in the interview:** "If a formula shows as text, the cell is usually formatted as Text. I change it to General, then press F2 and Enter to re-enter it. An apostrophe at the start tells Excel 'treat this as plain text', and it is hidden in the cell but visible in the formula bar."
**Explain simply:**
- Excel decides what a cell holds when you press Enter. A cell formatted as **Text** keeps `=B2+5` as words instead of calculating.
- Other causes: a space or apostrophe before the `=`, or Show Formulas switched on (Formulas tab > Show Formulas, shortcut Ctrl+`).
- A leading apostrophe (`'0012`) forces text. It is not part of the value and does not print.
- Text-numbers (like '12) are not added by arithmetic functions such as SUM, so totals come out wrong.
**Example:** An HR export has days-worked "12" stored as text; `=B3+5` still gives 17 because the `+` operator converts it, but `=SUM(B2:B3)` would skip it.
**Sample sheet:**

| | A | B | D |
|---|---|---|---|
| 1 | Emp | Days | Check |
| 2 | E01 | 10 (number) | =B2+5 |
| 3 | E02 | '12 (text) | =B3+5 |

**Formula / Steps:**
1. Select the cell(s) > Home > Number group > change Text to General.
2. Press F2 then Enter on each cell (or Data > Text to Columns > Finish for a whole column).
3. Check with `=ISNUMBER(B3)` or `=ISFORMULA(D2)`.

**Alternative:** `=VALUE(B3)+5` converts text to a number inside a formula; `=FORMULATEXT(D2)` shows a formula as text on purpose.
**Result:** (run in LibreOffice) D2 = 15, D3 = 17, `ISNUMBER(B2)` = TRUE, `ISNUMBER(B3)` = FALSE, `VALUE(B3)+5` = 17, `FORMULATEXT(D2)` = =B2+5. The "cell formatted as Text shows the formula" behaviour is a display behaviour, not run here (from memory).
**Version note:** ISFORMULA and FORMULATEXT need Excel 2013 or later (from memory, unverified); Google Sheets has ISFORMULA and FORMULATEXT too (unverified).
**Edge cases:** Changing the format to General does not re-evaluate by itself; you must re-enter the cell. Apostrophe only works at the very start.
**Likely follow-ups:**
1. How do you keep leading zeros? Format as Text or use an apostrophe (see Q63).
2. How do you show all formulas? Ctrl+` or Formulas > Show Formulas.
**Common mistakes:** Re-typing the formatting but not pressing Enter again; assuming `'` is part of the data and trying to remove it with TRIM.

### Q46 ⭐⭐ 🟡 How do you create a custom sort order, for example High, Medium, Low, instead of alphabetical?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know sorting is not only A-Z, and can you handle ranked labels?
**Say this in the interview:** "I use Data > Sort, choose the column, set Order to Custom List and pick or type High, Medium, Low. If I need it formula-driven, I add a helper column with MATCH that gives each label a rank and sort on that."
**Explain simply:**
- Alphabetical order would give High, Low, Medium, which is wrong for priority.
- A **custom list** is an order you define yourself; Excel stores it and sorts by position.
- A **helper column** is an extra column you add only to support another step.
**Example:** A support-ticket or hiring-priority sheet with High/Medium/Low urgency.
**Sample sheet:**

| | A | B | C (helper) |
|---|---|---|---|
| 1 | Ticket | Priority | Rank |
| 2 | T1 | Low | 3 |
| 3 | T2 | High | 1 |
| 4 | T3 | Medium | 2 |
| 5 | T4 | High | 1 |
| 6 | T5 | Low | 3 |

**Formula / Steps:** (Microsoft Support, "Sort data in a range or table in Excel")
1. Click a cell in the column > Data tab > Sort.
2. Sort by: Priority; Order: Custom List.
3. Under List entries type High, Medium, Low (each on its own line) > Add > OK.
Helper route: `=MATCH(B2,{"High","Medium","Low"},0)` in C2, fill down, sort by C.
**Alternative:** Save the list permanently via File > Options > Advanced > General > Edit Custom Lists > Import. In 365: `=SORTBY(A2:B6,MATCH(B2:B6,{"High","Medium","Low"},0))` (not run here; expected order T2, T4, T3, T1, T5).
**Result:** (run) MATCH returns 3,1,2,1,3 for rows 2-6, so sorting ascending on C gives T2, T4, T3, T1, T5 (Excel sort is stable on ties, from memory).
**Version note:** Custom list sort works in all desktop versions; SORTBY needs 365/2021 (Microsoft Support UNIQUE page lists 2021/2024/365 for the dynamic-array family; SORTBY itself not fetched, so unverified). Google Sheets has no custom list; use a helper column (from memory, unverified).
**Edge cases:** A label not in the list (e.g. "Urgent") gives #N/A in MATCH (run) and goes to the bottom in a custom-list sort; trailing spaces break matches.
**Likely follow-ups:**
1. Sort by two levels? Data > Sort > Add Level (Team, then Priority).
2. Sort by colour? Same dialog, Sort On: Cell Color.
**Common mistakes:** Sorting with only the one column selected (see Q64); typos in the list.

### Q47 ⭐⭐ 🟡 What is the difference between AutoFilter and Advanced Filter, and when would you use each?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the quick tool and the powerful tool, and when each fits?
**Say this in the interview:** "AutoFilter is the quick drop-down filter on the header row for everyday questions. Advanced Filter uses a separate criteria range, so I can combine many AND/OR conditions and copy the result to a new place."
**Explain simply:**
- **AutoFilter**: Data > Filter (Ctrl+Shift+L on Windows desktop per common practice, unverified; Microsoft's shortcut page lists it for Excel for the web and Mac). Filters in place, one column at a time, conditions across columns are AND.
- **Advanced Filter**: Data > Sort & Filter > Advanced. You type criteria in cells above or beside your data.
- Advanced can copy results elsewhere and extract unique records only; AutoFilter only hides rows.
- Advanced Filter results do not refresh automatically; you re-apply.
**Example:** Quick look at Ops staff: AutoFilter. "Sales absent over 3 days OR HR absent over 5 days" report copied to a new sheet: Advanced Filter.
**Formula / Steps:**
1. AutoFilter: click in data > Data > Filter > use the header arrows.
2. Advanced: copy the header row to an empty area, type criteria beneath (same row = AND, different rows = OR) > Data > Advanced > choose List range, Criteria range, and optionally Copy to another location.
**Alternative:** In 365, `=FILTER()` gives a live filtered list (not run here); a Table with Slicers gives click-friendly filters.
**Version note:** Both exist in all desktop versions (from memory; the Microsoft advanced-filter page returned 404 when fetched, so unverified). FILTER needs 365/2021 (from memory, unverified).
**Edge cases:** Criteria headers must match the data headers exactly; blank criteria cells match everything.
**Likely follow-ups:**
1. Can Advanced Filter use formulas as criteria? Yes, with a header that is blank or not a field name.
2. Does either delete rows? No, they hide or copy.
**Common mistakes:** Misspelled criteria headers; putting AND conditions on different rows (that makes them OR).

### Q48 ⭐⭐ 🟡 What filter will you use if you want more than two conditions, or want to copy the filtered result to another place?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the limits of the AutoFilter drop-down (two conditions per column) and the Advanced Filter fix?
**Say this in the interview:** "I use Advanced Filter with a criteria range. It handles any number of conditions and has a 'Copy to another location' option."
**Explain simply:**
- The custom AutoFilter box allows only two conditions in one column (And/Or).
- Advanced Filter takes a **criteria range**: headers plus conditions typed in cells.
- Conditions on the same row mean AND; on separate rows mean OR.
- For many different values in one column, use the AutoFilter checkbox list.
**Example:** Show staff with Absent > 3 and Team not HR, copied to a new area for the manager.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Emp | Team | Absent |
| 2 | E01 | Sales | 5 |
| 3 | E02 | Ops | 2 |
| 4 | E03 | Ops | 4 |
| 5 | E04 | HR | 3 |
| 6 | E05 | Sales | 7 |
| 7 | E06 | HR | 9 |

Criteria area (E1:F2): E1 `Team`, F1 `Absent`; E2 `<>HR`, F2 `>3`.
**Formula / Steps:**
1. Data > Sort & Filter > Advanced.
2. Action: Copy to another location.
3. List range `A1:C7`, Criteria range `E1:F2`, Copy to `H1`.
4. OK.
**Alternative:** 365: `=FILTER(A2:C7,(B2:B7<>"HR")*(C2:C7>3))` (not run here).
**Result:** Not run here (Advanced Filter and FILTER cannot run in LibreOffice headless). By hand/pandas: E01 Sales 5, E03 Ops 4, E05 Sales 7.
**Version note:** FILTER is 365/2021 only (from memory, unverified); Advanced Filter is in all desktop versions.
**Edge cases:** Text-numbers in Absent will not match `>3`; copy-to range must have room.
**Likely follow-ups:**
1. How to remove duplicates in the result? Tick "Unique records only".
2. Where do wildcards work? `*` and `?` in text criteria.
**Common mistakes:** Leaving the criteria range with a blank row (matches everything).

### Q49 ⭐⭐ 🟡 What does a #REF! error mean, and how does deleting a row or column cause it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you diagnose broken references and avoid them?
**Say this in the interview:** "#REF! means a reference is no longer valid. If a formula pointed at a cell, row or column and I delete it, the formula has nothing to point at, so it shows #REF!."
**Explain simply:**
- A **reference** is a cell address in a formula, like B5.
- Deleting the cell the formula needs turns the address into `#REF!` inside the formula text.
- Also caused by a lookup column number larger than the table width in some versions, INDEX with a row beyond the range, or a closed workbook link that moved.
- Fix: press Ctrl+Z immediately; otherwise re-point the formula by hand.
**Example:** `=B2+C2` for total pay; delete column C and the formula becomes `=B2+#REF!`.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | 1 | `=INDEX(A1:A3,5)` |
| 2 | 2 | `=VLOOKUP(2,A1:B3,5,FALSE)` |
| 3 | 3 | `=SUM(A1:A3)` |

**Formula / Steps:** To prevent: use whole-range SUM (`=SUM(B2:B10)`) so deleting one row inside just shrinks the range; hide instead of delete; use Tables or named ranges.
**Alternative:** Trace the fault with Formulas > Error Checking or Trace Precedents.
**Result:** (run) INDEX beyond range gives #REF!; the SUM is 6. VLOOKUP with column 5 of a 2-column range gave #VALUE! in LibreOffice (Excel documents #REF! for this, from memory, unverified).
**Version note:** Same in all versions (from memory, unverified; Microsoft's #REF! page returned 404).
**Edge cases:** Deleting the last row inside `SUM(B2:B10)` ranges is safe; deleting the cell that is the single reference is not.
**Likely follow-ups:**
1. Does clearing a cell cause it? No, only deleting.
2. Can Undo fix it after saving? No; you must rebuild.
**Common mistakes:** Deleting instead of clearing; saving and closing before noticing.

### Q50 ⭐⭐ 🟡 What are the common Excel errors #DIV/0!, #VALUE!, #NAME?, #REF! and #N/A, and what causes each?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you read an error and name the likely cause quickly?
**Say this in the interview:** "#DIV/0! is divide by zero or blank, #VALUE! is the wrong type of data, #NAME? is a misspelled function or name, #REF! is a deleted or invalid reference, and #N/A is 'value not found' in a lookup."
**Explain simply:**
- **#DIV/0!**: dividing by 0 or an empty cell (e.g. attrition rate when headcount is blank).
- **#VALUE!**: text where a number is needed (`=A1+A3` where A3 is "abc").
- **#NAME?**: Excel does not recognise the word (typo `SUMM`, or a function the version lacks).
- **#REF!**: invalid reference (Q49).
- **#N/A**: lookup or MATCH finds nothing.
**Example:** Attrition% = leavers / headcount; for a new team with 0 headcount you get #DIV/0!.
**Sample sheet:**

| | A | C |
|---|---|---|
| 1 | 10 | `=A1/A2` |
| 2 | 0 | `=A1+A3` |
| 3 | abc | `=SUMM(A1:A4)` |
| 4 | 5 | `=INDEX(A1:A4,9)` |
| 5 | | `=MATCH("x",A1:A4,0)` |

**Formula / Steps:** Handle: `=IFERROR(A1/A2,0)` or `=IF(A2=0,"n/a",A1/A2)`; for lookups `=IFNA(MATCH("x",A1:A4,0),"Not found")`.
**Alternative:** Fix the cause instead of hiding it: clean data, correct spelling, use Error Checking.
**Result:** (run) C1 #DIV/0!, C2 #VALUE!, C3 #NAME?, C4 #REF!, C5 #N/A; IFERROR gives 0; IF version gives "n/a"; IFNA gives "Not found".
**Version note:** IFERROR from Excel 2007, IFNA from Excel 2013 (from memory, unverified). #NAME? also appears when you open a 365 file using XLOOKUP in Excel 2016/2019 (Microsoft Support XLOOKUP page says not available there).
**Edge cases:** IFERROR hides every error, including real mistakes; prefer IFNA for lookups.
**Likely follow-ups:**
1. Other errors? #NUM! (impossible number), #NULL! (bad range operator), ##### (column too narrow).
2. How to find all errors? Home > Find & Select > Go To Special > Formulas > Errors.
**Common mistakes:** Wrapping everything in IFERROR(…,0) and distorting averages.

### Q51 ⭐⭐ 🟡 How do you sort a list randomly, or restore the original order after sorting?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you plan ahead before sorting and know helper columns?
**Say this in the interview:** "For random order I add a helper column with RAND, sort by it, then paste as values if I want it fixed. To be able to restore order, I add a serial number column before sorting and sort back by it."
**Explain simply:**
- `RAND()` gives a random number between 0 and 1 and changes on every recalculation (called **volatile**).
- Excel has no built-in 'undo sort' once the file is saved and closed; Ctrl+Z works only straight after.
- A **serial/ID column** (1, 2, 3...) lets you return to the original order.
**Example:** Randomly pick the order of 200 candidates for interview slots; keep the original resume order too.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Seq | Name | Rand |
| 2 | 1 | a | `=RAND()` |
| 3 | 2 | b | `=RAND()` |
| 4 | 3 | c | `=RAND()` |

**Formula / Steps:**
1. Add Seq column (1,2,3...) first.
2. Add `=RAND()` in C, fill down.
3. Data > Sort > by Rand (smallest to largest).
4. Optional: copy Rand > Paste Special > Values so it stops changing.
5. To restore: Data > Sort > by Seq.
**Alternative:** 365: `=SORTBY(B2:B4,RANDARRAY(3))` (not run here); also RANDBETWEEN.
**Result:** (run) RAND returned values in [0,1) (e.g. 0.455, 0.781, 0.818, different every run), so the shuffled order differs each time; exact order cannot be quoted.
**Version note:** RAND works everywhere; RANDARRAY and SORTBY are 365/2021 (from memory, unverified). Google Sheets has RAND and SORT with RANDARRAY (unverified).
**Edge cases:** Sorting recalculates RAND, so the numbers change after the sort; ties are extremely unlikely.
**Likely follow-ups:**
1. Random sample of 50? Sort by RAND and take the top 50.
2. Can I restore without a Seq column? Only by Undo or from a backup copy.
**Common mistakes:** Forgetting the Seq column; leaving RAND live so the order keeps changing.

### Q52 ⭐ 🟢 How do you apply the same formatting to every sheet in a workbook?
**Asked at:** commonly asked (no company-specific report found); the Guru99 list in the research file includes this question.
**What the interviewer is checking:** Do you know sheet grouping and its risk?
**Say this in the interview:** "I group the sheets: click the first tab, Shift-click the last, and format once; it applies to all. Then I ungroup, because edits on grouped sheets affect every sheet."
**Explain simply:**
- **Group sheets** = select several tabs so whatever you do happens on all of them.
- Ctrl+click picks specific tabs; Shift+click picks a range.
- Right-click a tab > Select All Sheets is also available.
- Ungroup by clicking any ungrouped tab or right-click > Ungroup Sheets.
**Example:** Twelve monthly attendance sheets (Jan-Dec) all need bold blue headers and a frozen top row.
**Formula / Steps:**
1. Click the Jan tab, hold Shift, click the Dec tab.
2. Format headers (Home tab), freeze panes (View > Freeze Panes).
3. Right-click a tab > Ungroup Sheets.
**Alternative:** Format Painter per sheet; or save a formatted blank sheet as a template and copy it (Move or Copy > Create a copy); Home > Fill > Across Worksheets.
**Version note:** All versions (from memory, unverified). Google Sheets has no sheet grouping (unverified).
**Edge cases:** Typing data while grouped overwrites the same cell on every sheet; the title bar shows [Group].
**Likely follow-ups:**
1. How to confirm grouping? "[Group]" in the title bar.
2. Cell Styles help? Yes, define once and apply anywhere.
**Common mistakes:** Forgetting to ungroup and typing into all sheets.

### Q53 ⭐ 🟢 How do you use Format Painter, and what does double-clicking it do?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Basic formatting efficiency.
**Say this in the interview:** "Select a formatted cell, click Format Painter on the Home tab, then click or drag over the target. Double-click it to keep it switched on and paint many places; Esc turns it off."
**Explain simply:**
- Format Painter copies formatting (font, fill, borders, number format) but not the value.
- Single click = one use. Double-click = stays active until you press Esc or click it again.
- It is on Home > Clipboard group (the paintbrush).
**Example:** Copy the header style of a payroll sheet to five other header rows.
**Formula / Steps:**
1. Click the source cell.
2. Home > Clipboard > Format Painter (double-click for repeat).
3. Click or drag the target cells; press Esc to stop.
**Alternative:** Copy, then Paste Special > Formats; or Cell Styles.
**Version note:** All versions; Excel and Google Sheets both have a paint-format tool (from memory, unverified).
**Edge cases:** Copies conditional formatting and data validation of the source along with it in many cases (from memory); copies number formats, which can change how dates display.
**Likely follow-ups:**
1. Can it work across sheets? Yes, switch tabs while it is active.
**Common mistakes:** Single-clicking and expecting multiple uses.

### Q54 ⭐ 🟢 How do you use the Fill Handle's double-click shortcut, and when does it stop short?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Speed in copying formulas down long lists, and awareness of gaps.
**Say this in the interview:** "I double-click the small square at the bottom-right of the selected cell and Excel fills down as far as the neighbouring column has data. It stops at the first blank in that neighbouring column."
**Explain simply:**
- The **Fill Handle** is the small square at the corner of a selected cell.
- Double-click fills down to match the length of the adjacent column.
- It uses the nearest column with data on the left (or right if left is empty).
- It stops at a blank cell, so 5,000 rows with one gap in row 800 fills only 799 rows.
**Example:** Add a formula `=C2*D2` for 5,000 employees; double-click fills all rows.
**Formula / Steps:**
1. Enter the formula in the first row.
2. Select it, double-click the fill handle.
3. Check the last row.
**Alternative:** Select the range and press Ctrl+D (fill down); or convert to a Table so formulas auto-fill.
**Version note:** All versions; Google Sheets also supports double-click fill (from memory, unverified).
**Edge cases:** Blank cells in the neighbouring column; adjacent column used as the guide, not the one you are filling; filtered data.
**Likely follow-ups:**
1. Fill without formats? Auto Fill Options > Fill Without Formatting.
**Common mistakes:** Not scrolling to the end to check it stopped early.

### Q55 ⭐ 🟢 How do you insert and delete rows or columns, and what shortcut do you use?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Fluency with basic edits and keyboard use.
**Say this in the interview:** "I select the row or column, right-click > Insert or Delete. By keyboard, Ctrl+Space selects a column, Shift+Space selects a row, Ctrl+Shift+Plus inserts and Ctrl+Minus deletes."
**Explain simply:**
- Insert pushes existing data down or right; Delete pulls it up or left.
- Microsoft's shortcut page lists Ctrl+Spacebar (select column), Shift+Spacebar (select row), Ctrl+Shift+Plus (open Insert) and Ctrl+Minus (open Delete) (Microsoft Support, "Keyboard shortcuts in Excel").
- With a whole row selected, Insert adds a row at once without a dialog.
- Deleting can break formulas (Q49).
**Example:** Add a new joiner row in the middle of a headcount list.
**Formula / Steps:** Select row > Ctrl+Shift+Plus; or Home > Cells > Insert > Insert Sheet Rows.
**Alternative:** Right-click the row number > Insert; Ctrl+Y or F4 repeats the last action.
**Version note:** All versions; shortcuts listed on the Microsoft page above (Windows). Google Sheets has the same shortcuts in a different mapping (unverified).
**Edge cases:** Inserting rows inside a table extends the table; deleting entire rows removes hidden data too.
**Likely follow-ups:**
1. Insert multiple rows? Select that many rows first.
**Common mistakes:** Using Delete key (clears contents) instead of Delete rows (removes the row).

### Q56 ⭐ 🟢 How do you insert today's date and the current time as fixed values with the keyboard, and how is that different from the TODAY function?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Static versus dynamic values.
**Say this in the interview:** "Ctrl+; types today's date and Ctrl+Shift+; types the current time as fixed values. TODAY() and NOW() are formulas that change every time the workbook recalculates."
**Explain simply:**
- Microsoft lists Ctrl+; for "Enter the current date" and Ctrl+Shift+: for "Enter the current time" (Microsoft Support, "Keyboard shortcuts in Excel").
- Fixed values never change: perfect for a joining date or sign-in time.
- `=TODAY()` shows today's date and updates whenever you open the file; `=NOW()` includes time.
- A date in Excel is a serial number; the time is the decimal part.
**Example:** Joining date typed with Ctrl+; stays 21-Oct-2026; `=TODAY()-B2` gives days of service that grows daily.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | Joined | Tenure days |
| 2 | 01-Jan-2026 | `=TODAY()-A2` |

**Formula / Steps:** Select cell > Ctrl+; then Space then Ctrl+Shift+; for both in one cell.
**Alternative:** `=TODAY()` then Copy > Paste Special > Values to freeze it.
**Result:** (run on 21-Oct-2026) `=TODAY()-DATE(2026,1,1)` returned 293, matching the Python check; `TODAY()-INT(TODAY())` = 0 (no time part); the answer changes each day.
**Version note:** All versions (shortcuts per Microsoft page; Google Sheets uses Ctrl+; and Ctrl+Shift+; too, unverified).
**Edge cases:** TODAY is volatile: attendance records using it will change when reopened; time cells need a time number format.
**Likely follow-ups:**
1. Date and time together? Ctrl+; Space Ctrl+Shift+;.
**Common mistakes:** Using TODAY() for a record date, which then rewrites history.

### Q57 ⭐ 🟢 How do you protect a worksheet or a workbook with a password, and what is the difference between the two?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Awareness of safeguarding salary or HR data and its limits.
**Say this in the interview:** "Protect Sheet stops people changing locked cells on that sheet. Protect Workbook stops structure changes like adding, moving or hiding sheets. Neither is strong security, and a forgotten password cannot be recovered by Microsoft."
**Explain simply:**
- Sheet protection: first unlock the cells people may edit (Format Cells > Protection > clear Locked), then Review > Protect Sheet, choose allowed actions, set an optional password (Microsoft Support, "Protect a worksheet").
- Microsoft states worksheet protection is not a security feature; workbook protection prevents changes to sheet structure.
- A file-level password to open the file (File > Info > Protect Workbook > Encrypt with Password) is separate and stronger (from memory, unverified).
- "If you forget your password, Microsoft cannot retrieve it" (same page).
**Example:** Lock the salary formulas but leave the "Days absent" input cells editable for team leads.
**Formula / Steps:**
1. Select input cells > Ctrl+1 > Protection > untick Locked.
2. Review > Protect Sheet > enter password > OK.
3. Workbook structure: Review > Protect Workbook.
**Alternative:** Save a read-only copy or restrict sharing through OneDrive/SharePoint.
**Version note:** Desktop steps exist in all versions; the web version uses Review > Manage Protection (Microsoft Support page above).
**Edge cases:** Sheet passwords can be bypassed with tools, so don't rely on them for confidential payroll.
**Likely follow-ups:**
1. Hide formulas? Format Cells > Protection > Hidden, then protect.
**Common mistakes:** Protecting before unlocking input cells; losing the password.

### Q58 ⭐ 🟢 How do you freeze both the top row and the first column at the same time?
**Asked at:** commonly asked (no company-specific report found); freeze panes appears in the DataCamp and Guru99 beginner lists in the research file.
**What the interviewer is checking:** Basic navigation of big sheets.
**Say this in the interview:** "I click cell B2, then View > Freeze Panes > Freeze Panes. Everything above and to the left of the selected cell stays visible."
**Explain simply:**
- Freeze Panes locks rows above and columns left of the selected cell (Microsoft Support, "Freeze panes to lock rows and columns").
- B2 freezes row 1 and column A.
- To undo: View > Freeze Panes > Unfreeze Panes.
- Freeze Top Row / Freeze First Column freeze only one of them.
**Example:** Headers (row 1) and employee names (column A) stay visible while scrolling a 12-month attendance grid.
**Formula / Steps:** Click B2 > View > Window > Freeze Panes > Freeze Panes.
**Alternative:** Split (View > Split) gives two scrollable panes, not locked ones.
**Version note:** All versions; Google Sheets uses View > Freeze (from memory, unverified).
**Edge cases:** If a header spans two rows, select the cell below both.
**Likely follow-ups:**
1. Freeze first 3 rows? Select A4 first.
**Common mistakes:** Selecting A1 (freezes nothing useful) or the wrong cell.

### Q59 ⭐ 🟢 How do you check which version of Excel you use, and name two features that exist in Microsoft 365 but not in Excel 2016?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Compatibility awareness before sharing files.
**Say this in the interview:** "File > Account > About Excel shows the version. XLOOKUP and UNIQUE (dynamic array functions) are in Microsoft 365 but not in Excel 2016."
**Explain simply:**
- Check: File > Account > About Excel (from memory, unverified).
- Microsoft's XLOOKUP page says it is not available in Excel 2016 and 2019 and lists Excel 2021 and Microsoft 365 as available (the page's "Applies to" list contradicts its own note on 2016/2019; the note is taken as correct).
- Microsoft's UNIQUE page lists Microsoft 365, Excel 2024 and Excel 2021, not 2016.
- **Dynamic arrays** = one formula spilling results into several cells.
**Example:** A colleague on Excel 2016 sees #NAME? where your XLOOKUP sits.
**Formula / Steps:** File > Account > About Excel. Compatibility check: File > Info > Check for Issues > Check Compatibility.
**Alternative:** `=INFO("release")` gives limited info (unverified).
**Version note:** As above (Microsoft Support, "XLOOKUP function" and "UNIQUE function"). Other 365-only items (e.g. LET, Copilot) are from memory, unverified.
**Edge cases:** Perpetual versions (2016/2019/2021) do not receive new functions; 365 does.
**Likely follow-ups:**
1. Workaround for 2016? INDEX/MATCH instead of XLOOKUP.
**Common mistakes:** Sending 365-only formulas to users on older Excel.

### Q60 ⭐ 🟢 What are the key differences between Excel and Google Sheets for basic sorting, filtering and sharing?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Tool awareness for collaborative work.
**Say this in the interview:** "Both sort and filter similarly, but Sheets is web-first with real-time sharing by link, while desktop Excel is stronger for large data, pivots, Power Query and offline work." (All Google Sheets claims here are from memory, unverified; no Google help page was fetched.)
**Explain simply:**
- **Sorting:** both support multi-column sort; Excel has custom lists and sort by colour; Sheets has Data > Sort range and the `SORT` function.
- **Filtering:** Excel AutoFilter and Advanced Filter; Sheets filter views let each person filter without affecting others, and the `FILTER` function.
- **Sharing:** Sheets edits live by default with comments; Excel co-authoring needs OneDrive/SharePoint.
- Excel handles much larger files and has Power Query; Sheets limits are lower.
**Example:** A recruiter team shares one tracker; Sheets filter views let each recruiter view only their own candidates.
**Formula / Steps:** Excel: Data > Filter. Sheets: Data > Create a filter, or Create filter view.
**Alternative:** Excel for the web gives browser co-editing with fewer features.
**Version note:** Unverified from memory.
**Edge cases:** Formulas and macros may not convert perfectly between them.
**Likely follow-ups:**
1. When pick Excel? Heavy data, pivots, VBA.
**Common mistakes:** Claiming one is simply "better".

### Q61 ⭐ 🟡 How do you filter or sort only the visible rows, and why does copying a filtered range sometimes paste hidden rows?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand hidden versus filtered rows and visible-only operations?
**Say this in the interview:** "Filtering already works on visible rows. For totals I use SUBTOTAL or AGGREGATE, and to copy only visible cells, I select the range and press Alt+; before copying. Plain copying of a filtered range normally copies only visible rows, but hidden (not filtered) rows or odd selections can bring them along."
**Explain simply:**
- Rows hidden by a **filter** are skipped by copy in a normal contiguous selection (from memory).
- Rows hidden by **right-click > Hide** (or grouped) can be pasted if the selection includes them in some cases; Alt+; (Select Visible Cells) fixes that.
- `SUM` counts hidden rows; `SUBTOTAL(109,...)` ignores hidden rows.
- Sorting a filtered list sorts only the visible rows.
**Example:** Total absence days for only the visible Ops staff.
**Sample sheet:** Rows 3 and 5 hidden.

| | A | B | C |
|---|---|---|---|
| 1 | Emp | Team | Absent |
| 2 | E01 | Sales | 5 |
| 3 | E02 | Ops | 2 (hidden) |
| 4 | E03 | Ops | 4 |
| 5 | E04 | HR | 3 (hidden) |
| 6 | E05 | Sales | 7 |
| 7 | E06 | HR | 9 |

**Formula / Steps:** `=SUM(C2:C7)`, `=SUBTOTAL(109,C2:C7)`, `=SUBTOTAL(103,C2:C7)`. To copy visible only: select > Alt+; > Ctrl+C.
**Alternative:** Home > Find & Select > Go To Special > Visible cells only.
**Result:** (run, rows 3 and 5 hidden) SUM = 30, SUBTOTAL(109) = 25, SUBTOTAL(103) (count of visible) = 4, SUBTOTAL(9) = 30 (code 9 ignores filtered rows but not manually hidden ones; this run hid rows manually). The copy/paste behaviour is not run here.
**Version note:** SUBTOTAL works in all versions (from memory, unverified).
**Edge cases:** SUBTOTAL ignores other SUBTOTALs to avoid double counting.
**Likely follow-ups:**
1. Difference between 9 and 109? 109 also ignores manually hidden rows.
**Common mistakes:** Using SUM on a filtered list.

### Q62 ⭐ 🟡 How do you sort left to right (by columns instead of rows)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Awareness of sort options beyond top-to-bottom.
**Say this in the interview:** "Data > Sort > Options > Sort left to right, then choose the row to sort by."
**Explain simply:**
- Normal sort reorders rows by a column; left-to-right reorders columns by a row.
- Steps per Microsoft Support, "Sort data in a range or table in Excel": select a cell, Data > Sort > Options > "Sort left to right" > OK, choose the Row and Order.
- Tables do not support this; convert to a range first.
**Example:** Quarter totals across columns need ordering smallest to largest.
**Sample sheet:**

| | A | B | C | D |
|---|---|---|---|---|
| 1 | Q4 | Q2 | Q3 | Q1 |
| 2 | 40 | 20 | 30 | 10 |

**Formula / Steps:** Select A1:D2 > Data > Sort > Options > Sort left to right > Row 2, smallest to largest.
**Alternative:** `=SMALL($A$2:$D$2,k)` for the values only; or paste with Transpose, sort, transpose back.
**Result:** (run) SMALL across four columns returned 10, 20, 30, 40. After the sort, headers would read Q1, Q2, Q3, Q4 (UI step not run here).
**Version note:** Available in all desktop versions (Microsoft page; web version differs, so unverified).
**Edge cases:** Include header row in the selection so labels move with data.
**Likely follow-ups:**
1. Why is it greyed out? Data is in a Table.
**Common mistakes:** Forgetting to select the header row.

### Q63 ⭐ 🟡 How do you stop Excel from changing long numbers, such as an employee ID or phone number, into scientific notation or dropping leading zeros?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Treating identifiers as text, not numbers.
**Say this in the interview:** "IDs are labels, not quantities, so I format the column as Text before typing or importing, or type an apostrophe first. For fixed-length codes I can use a custom format like 000000."
**Explain simply:**
- Excel keeps only 15 significant digits for numbers (from memory, unverified); longer numbers lose digits and may show as 1.23E+11.
- A leading zero is dropped because 007 is the number 7.
- Text format or apostrophe keeps it exactly.
- Custom format `000000` only displays zeros; the value is still 42.
**Example:** Employee ID 000042 and a 12-digit Aadhaar-style or phone number.
**Sample sheet:**

| | A | B |
|---|---|---|
| 2 | 123456789012 | `=TEXT(A2,"0")` |
| 4 | 42 | `=TEXT(A4,"000000")` |

**Formula / Steps:**
1. Select column > Home > Number format box > Text, then type the IDs.
2. For import: Data > From Text/CSV > set column type to Text (Power Query).
3. For display only: Ctrl+1 > Custom > `000000`.
**Alternative:** Prefix an apostrophe (`'000042`); or `=TEXT(A4,"000000")`.
**Result:** (run) `TEXT(A2,"0")` = "123456789012"; `TEXT(42,"000000")` = "000042"; `LEN` = 6; adding 0 back gives 42 (shows text vs number).
**Version note:** Text and custom formats work in all versions; Data > From Text/CSV is 2016+ (Get & Transform; from memory, unverified).
**Edge cases:** Credit-card style 16+ digit numbers must be text from the start, or the last digits turn into zeros.
**Likely follow-ups:**
1. Fix already-damaged data? Leading zeros can be restored with TEXT, lost digits cannot.
**Common mistakes:** Formatting as Text after typing; that does not restore lost zeros.

### Q64 ⭐ 🟡 You receive a sheet where sorting scrambles the data because one column was left out of the selection. How do you recover, and how do you prevent it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Calm recovery thinking and data safety habits.
**Say this in the interview:** "If I have not saved or closed, I press Ctrl+Z straight away. If it is already saved, I look for an ID or serial column, an earlier version or backup (File > Info > Version History) to rebuild the order. To prevent it I click inside a clean data block, or convert it to a Table, so Excel sorts all columns together."
**Explain simply:**
- When one column is sorted alone, its values no longer line up with the rest, so each employee gets someone else's data.
- Recovery order: Undo, then version history or backup, then re-match using any untouched key column.
- Prevention: keep no blank columns in data, select one cell (not a single column) before sorting, use Tables, keep a Seq/ID column, work on a copy.
**Example:** Only the Salary column is sorted; every employee now shows another person's salary.
**Formula / Steps:**
1. Press Ctrl+Z immediately.
2. If saved: File > Info > Version History (OneDrive/SharePoint) or open the source export again.
3. Prevent: click any cell > Data > Sort and confirm the dialog shows "Expand the selection".
**Alternative:** Rebuild with `=VLOOKUP(ID, original, col, FALSE)` from the original file if you have the key.
**Version note:** Version History needs files on OneDrive/SharePoint (from memory, unverified). Undo works in all versions.
**Edge cases:** Without any key column and no backup, the original pairing cannot be recovered.
**Likely follow-ups:**
1. Why does Excel sometimes warn? It offers "Expand the selection" vs "Continue with the current selection".
**Common mistakes:** Choosing "Continue with the current selection"; saving over the original.

### Q65 ⭐ 🟡 How do you create and use a custom number format, for example showing 1500000 as 1.5M or adding 'days' after a number?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Formatting without changing underlying values.
**Say this in the interview:** "Ctrl+1 > Number > Custom, then type a code like `0.0,,"M"` for millions or `0 "days"` for units. The cell still holds the real number; only the display changes."
**Explain simply:**
- Steps per Microsoft Support, "Create or delete a custom number format": select data, Home > Number group dialog launcher > Custom > type the format > OK; text goes in quotation marks.
- Each trailing comma divides the display by 1,000, so `,,` gives millions (from memory; confirmed by the test below).
- `0` forces a digit; `#` shows a digit only if present.
- Custom formats cannot be created in Excel for the web (Microsoft Support page above).
**Example:** Payroll cost 1500000 shown as 1.5M on a dashboard; leave balance 5 shown as 5 days.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | 1500000 | `=TEXT(A1,"0.0,,""M""")` |
| 2 | | `=TEXT(5,"0 ""days""")` |

**Formula / Steps:** Select cells > Ctrl+1 > Custom > Type `0.0,,"M"` > OK. For days: `0 "days"`.
**Alternative:** The TEXT function does the same but returns text (cannot be summed).
**Result:** (run in LibreOffice) 1.5M; 5 days; `TEXT(1234567,"0.0,""K""")` = 1234.6K; `TEXT(2500,"#,##0")` = 2,500.
**Version note:** Same format codes in all desktop versions; LibreOffice matched here, Excel behaviour from memory.
**Edge cases:** Negative or zero values need extra sections separated by `;`; the number is only displayed rounded.
**Likely follow-ups:**
1. Does SUM still work? Yes, the real value is unchanged.
**Common mistakes:** Forgetting quotes around text; using TEXT and then trying to calculate.

### Q66 ⭐ 🟡 A manager asks for a quick attendance list: how would you filter a sheet of 5,000 employees to show only those absent more than 3 days in a month, sorted by team?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Combining filter and sort on a realistic HR task, and checking the "more than" boundary.
**Say this in the interview:** "I turn on filters, set Absent days to Greater Than 3, then sort by Team, and after that by days descending. 'More than 3' means 4 and above, so exactly 3 is excluded."
**Explain simply:**
- Clean first: blanks, text-numbers and duplicate employee rows.
- Data > Filter > Absent arrow > Number Filters > Greater Than > 3.
- Data > Sort > Team A-Z, then Absent days largest to smallest.
- Copy the visible rows to a new sheet for the manager (Alt+; first, see Q61).
**Example:** 5,000 rows shrink to the few dozen who need a conversation.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Emp | Team | Absent |
| 2 | E01 | Sales | 5 |
| 3 | E02 | Ops | 2 |
| 4 | E03 | Ops | 4 |
| 5 | E04 | HR | 3 |
| 6 | E05 | Sales | 7 |
| 7 | E06 | HR | 9 |

**Formula / Steps:**
1. Click any cell in the data > Data > Filter.
2. Absent > Number Filters > Greater Than > 3.
3. Data > Sort > Sort by Team (A to Z), Add Level > Absent (Largest to Smallest).
Check count: `=COUNTIF(C2:C7,">3")`.
**Alternative:** 365: `=SORT(FILTER(A2:C7,C2:C7>3),2)` (not run here).
**Result:** (pandas and run) `COUNTIF` = 4. Expected list: E06 HR 9; E03 Ops 4; E05 Sales 7; E01 Sales 5. E04 (exactly 3) is excluded. The filter and sort UI is not run here.
**Version note:** AutoFilter and Sort work in all versions; FILTER/SORT need 365/2021 (from memory, unverified).
**Edge cases:** Absent stored as text will not filter correctly (Q45); an employee with several rows needs totals first (SUMIFS or pivot); define "a month" clearly.
**Likely follow-ups:**
1. How to refresh next month? Reapply the filter (Data > Reapply).
2. Same list by percentage? Use days divided by working days.
**Common mistakes:** Using >=3; sorting only one column; forgetting to clear the filter before sending.

