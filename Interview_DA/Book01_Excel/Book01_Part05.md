# Book 1 — Excel | Part 5: Data Cleaning (duplicates, TRIM, Text to Columns, Flash Fill) 🟢

**Target:** 50 questions | **Actual:** 50 questions
**Scope:** Cleaning messy data in Excel: duplicates, spaces and hidden characters, text-to-columns, Flash Fill, text and date type fixes, blanks, and cleaning workflow.

### Q1 ⭐⭐⭐ 🟢 How do you remove duplicate rows in Excel?
**Asked at:** commonly asked (no company-specific report found); "remove duplicates" appears in the Analytics Vidhya Excel interview list (Jan 2024).
**What the interviewer is checking:** Do you know the built-in tool and its dangers (permanent delete, which columns you tick)?
**Say this in the interview:** "I copy the data to a backup sheet first, click inside the table, go to Data > Remove Duplicates, tick the columns that define a duplicate, usually the Employee ID, and click OK. Excel keeps the first row and deletes the later ones."
**Explain simply:**
- A *duplicate* here means a row that matches an earlier row on every column you tick.
- Excel keeps the first match and deletes the rest. This is permanent: it is a deletion, not a hiding (Microsoft Support, "Filter for unique values or remove duplicate values").
- If a row is removed, the whole row goes, including columns you did not tick.
**Example:** An HR export has 6 rows, but Employee E102 was entered 3 times. Ticking only the ID column leaves 4 rows.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | EmpID | Name | Dept |
| 2 | E101 | Asha | HR |
| 3 | E102 | Ravi | Finance |
| 4 | E103 | Meena | IT |
| 5 | E102 | Ravi | Finance |
| 6 | E104 | Karan | HR |
| 7 | E102 | Ravi | Finance |

**Formula / Steps:**
1. Copy the sheet as a backup (right-click the tab > Move or Copy > Create a copy).
2. Click any cell in the data.
3. Ribbon: Data tab > Data Tools group > Remove Duplicates.
4. Tick "My data has headers", then tick only the columns that define a duplicate (here EmpID).
5. OK. Excel reports how many duplicates were removed and how many unique values remain.
**Alternative:** Keep the original and list unique values instead: Data > Advanced Filter > "Unique records only" (copy to another location), or `=UNIQUE(A2:A7)` in 365/2021. Both are not run here (a feature and a dynamic array function); by hand, the unique IDs are E101, E102, E103, E104.
**Result:** Not run here (feature, not a formula). By hand: after Remove Duplicates on EmpID, rows 2, 3, 4 and 6 remain (E101, E102, E103, E104); the rows 5 and 7 are deleted. Message: "2 duplicate values found and removed; 4 unique values remain."
**Version note:** Remove Duplicates is in all current desktop Excel versions (from memory, unverified; the Microsoft Support page describes the behaviour but I did not confirm its version list). UNIQUE needs 365/2021 (from memory, unverified).
**Edge cases:** Matching is on what the cell *shows*, not the stored value (Microsoft Support). Text with hidden spaces looks the same but may not match, so TRIM first. Case is ignored (from memory, unverified).
**Likely follow-ups:** 1) *Which row stays?* The first. 2) *Can you undo?* Ctrl+Z straight after, but not after saving and closing, so back up first.
**Common mistakes:** Ticking all columns when only the ID defines a duplicate, or ticking only one column and losing different people; forgetting the backup; leaving "My data has headers" unticked so the header is treated as data.

### Q2 ⭐⭐⭐ 🟢 What does the TRIM function do, and when would you use it?
**Asked at:** commonly asked (no company-specific report found); TRIM is named in the Analytics Vidhya Excel interview list (Jan 2024).
**What the interviewer is checking:** Do you know the most common cleaning function and why spaces break lookups?
**Say this in the interview:** "TRIM removes extra spaces from text: all spaces at the start and end, and it shrinks several spaces between words down to one. I use it before VLOOKUP, COUNTIF or Remove Duplicates, because 'Priya ' and 'Priya' look the same but Excel treats them as different."
**Explain simply:**
- Syntax: `=TRIM(text)`. It gives back a cleaned copy; the original cell is not changed.
- Why it matters: a stray trailing space makes a lookup return #N/A and makes two identical names count as two people.
- It only removes the normal space (character code 32). The web-style non-breaking space (code 160) stays (Microsoft Support, "TRIM function").
**Example:** Names typed by different recruiters, with spaces in odd places.
**Sample sheet:**

| | A | B | C | D |
|---|---|---|---|---|
| 1 | Raw name | TRIM | LEN raw | LEN trimmed |
| 2 | `  Priya   Sharma ` | | | |
| 3 | `Ravi Kumar  ` | | | |
| 4 | `  Meena Iyer` | | | |
| 5 | `Karan  Singh` | | | |

**Formula / Steps:** `B2: =TRIM(A2)`, `C2: =LEN(A2)`, `D2: =LEN(B2)`, fill down.
**Alternative:** `=SUBSTITUTE(A2," ","")` removes *all* spaces (too much for names); Power Query: Transform > Format > Trim. For non-breaking spaces: `=TRIM(SUBSTITUTE(A2,CHAR(160)," "))`.
**Result:** Run in LibreOffice: B2 `Priya Sharma`, B3 `Ravi Kumar`, B4 `Meena Iyer`, B5 `Karan Singh`. LEN raw 17, 12, 12, 12; LEN trimmed 12, 10, 10, 11.
**Version note:** TRIM works in all Excel versions and Google Sheets (from memory, unverified).
**Edge cases:** A number with spaces becomes text after TRIM. Cells showing a "space" that TRIM cannot remove usually contain CHAR(160). Blank cells give "".
**Likely follow-ups:** 1) *TRIM does not work, why?* Probably CHAR(160); use SUBSTITUTE. 2) *Does it change the original?* No, you need a helper column then paste as values.
**Common mistakes:** Expecting TRIM to edit the cell in place; forgetting to paste values before deleting the raw column; confusing TRIM with CLEAN.

### Q3 ⭐⭐⭐ 🟢 How do you find duplicates in Excel without deleting them?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you inspect duplicates safely before taking action?
**Say this in the interview:** "I highlight them with Conditional Formatting > Highlight Cells Rules > Duplicate Values, or I add a helper column with COUNTIF that counts how many times each ID appears. Anything above 1 is a duplicate. Nothing gets deleted, so I can review first."
**Explain simply:**
- *Conditional Formatting* = colouring cells automatically when a rule is true.
- *Helper column* = an extra column you add only to help your analysis.
- Duplicate Values highlights every copy, including the first one.
**Example:** A payroll list of employee IDs where E102 and E101 were entered more than once.
**Sample sheet:**

| | A | B | C | D |
|---|---|---|---|---|
| 1 | EmpID | Times seen | Flag | First or repeat |
| 2 | E101 | | | |
| 3 | E102 | | | |
| 4 | E103 | | | |
| 5 | E102 | | | |
| 6 | E104 | | | |
| 7 | E101 | | | |
| 8 | E102 | | | |

**Formula / Steps:**
- Colour route: select A2:A8 > Home tab > Styles group > Conditional Formatting > Highlight Cells Rules > Duplicate Values > OK.
- Formula route: `B2: =COUNTIF($A$2:$A$8,A2)`, `C2: =IF(B2>1,"Duplicate","")`, fill down. Then filter column C.
**Alternative:** To mark only the repeats and not the first occurrence: `D2: =IF(COUNTIF($A$2:A2,A2)>1,"Repeat","First")` (expanding range). Total rows involved in duplicates: `=SUMPRODUCT((COUNTIF(A2:A8,A2:A8)>1)*1)`.
**Result:** Run in LibreOffice: Times seen = 2, 3, 1, 3, 1, 2, 3. Flag shows "Duplicate" on rows 2, 3, 5, 7, 8. Repeat/First = First, First, First, Repeat, First, Repeat, Repeat. The SUMPRODUCT returns 5.
**Version note:** Conditional Formatting and COUNTIF work in all versions and Google Sheets (from memory, unverified); in Sheets the colour rule is Format > Conditional formatting with a custom formula `=COUNTIF(A:A,A1)>1`.
**Edge cases:** COUNTIF ignores case and treats `*` and `?` inside the criteria as wildcards (so an ID containing them can over-match; use `~*` to mean a real asterisk); IDs with trailing spaces will not match, so TRIM first. Criteria strings over 255 characters can fail in COUNTIF (from memory, unverified; the Excel specifications page I fetched does not mention it).
**Likely follow-ups:** 1) *How do you then remove them?* Filter on "Repeat" and delete those rows, or run Remove Duplicates. 2) *Why the dollar signs?* They lock the range while the formula is filled down.
**Common mistakes:** Forgetting `$` so the range slides down; checking only one column when a duplicate needs ID plus date; assuming the highlight marks only the extra copies.

### Q4 ⭐⭐⭐ 🟢 What steps do you follow when you receive a messy dataset and have to clean it before analysis?
**Asked at:** commonly asked (no company-specific report found); data cleaning is named in sampled job descriptions such as the TMI MIS Executive (Hyderabad), Tata Play Fiber MIS (Bengaluru) and OrbiTouch HR Junior Data Analyst (Hyderabad).
**What the interviewer is checking:** Do you have a repeatable, safe process, not just a bag of tricks?
**Say this in the interview:** "First I keep an untouched copy of the raw data. Then I look at it, fix structure, remove duplicates, trim spaces, fix data types for numbers and dates, standardise spellings, handle blanks, check totals against the source, and write down what I changed."
**Explain simply:**
- Raw copy: never clean the only copy.
- Look: scroll, filter each column, check counts of rows and blanks.
- Structure: one header row, no merged cells, no blank rows, one fact per column.
- Text: TRIM, CLEAN, PROPER, Find and Replace for spellings ("Hyd" vs "Hyderabad").
- Types: numbers stored as text, text dates (see Q17 and later parts).
- Duplicates and blanks: decide per column, do not delete blindly.
- Validate: row count and total before and after; spot-check ten rows.
- Document: a small "cleaning log" sheet.
**Example:** A 2,000-row attendance export: 12 duplicate IDs, 40 blank departments, "Hyd"/"Hyderabad" mixed, salaries as text. After cleaning I confirm the headcount equals the HRMS (HR system) headcount.
**Steps:**
1. Copy the raw sheet to `Raw` and work on `Clean`.
2. Convert the range to a Table (Ctrl+T) and filter each column to see odd values.
3. Fix structure: unmerge, delete blank rows, one header.
4. Text fixes (helper columns, then paste as values).
5. Type fixes; then Remove Duplicates (Data > Remove Duplicates) on the right key.
6. Handle blanks (Go To Special > Blanks).
7. Reconcile counts and totals; write the log.
**Alternative:** For repeating monthly files, do the same steps once in Power Query (Data > Get & Transform) so they replay with Refresh. Power Query is built in from Excel 2016 (from memory, unverified).
**Version note:** Everything above works in Excel 2016 onwards; UNIQUE/TEXTSPLIT shortcuts need 365/2021 or later.
**Edge cases:** Not run here (process question, no formula). Some "errors" are real data (a person truly has no manager), so ask the data owner before filling or deleting.
**Likely follow-ups:** 1) *How do you know cleaning worked?* Row and total reconciliation plus spot checks. 2) *What do you never do?* Overwrite the raw file.
**Common mistakes:** Cleaning without a backup; deleting blanks that carry meaning; no record of changes; cleaning by hand-typing instead of repeatable steps.

### Q5 ⭐⭐⭐ 🟢 What is Text to Columns, and how do you use it?
**Asked at:** commonly asked (no company-specific report found); not seen as an explicit question in the Analytics Vidhya list we read.
**What the interviewer is checking:** Can you split one column of combined text into several columns?
**Say this in the interview:** "Text to Columns splits one column into many using a separator such as a comma, space or hyphen. I select the column, go to Data > Text to Columns, choose Delimited, tick the separator, choose a safe destination, and click Finish."
**Explain simply:**
- *Delimiter* = the character that separates the pieces (comma, space, hyphen).
- It overwrites cells to the right if the destination is not changed, so make blank columns first or pick another destination.
- It changes your data in place; it is not a formula, so it does not update later.
**Example:** "Priya Sharma" in one cell becomes "Priya" and "Sharma".
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Full name | | |
| 2 | Priya Sharma | | |
| 3 | Ravi Kumar | | |
| 4 | Meena Iyer | | |

**Formula / Steps:**
1. Select A2:A4.
2. Ribbon: Data tab > Data Tools group > Text to Columns.
3. Step 1: choose Delimited > Next.
4. Step 2: tick Space (or the right delimiter); check the preview > Next.
5. Step 3: set Destination to `$B$2` so A is not overwritten; optionally set column format (Text for IDs with leading zeros) > Finish (steps from Microsoft Support, "Split text into different columns with the Convert Text to Columns Wizard").
**Alternative:** Flash Fill (Ctrl+E), or formulas `=LEFT(A2,FIND(" ",A2)-1)` and `=MID(A2,FIND(" ",A2)+1,50)`; in 365, TEXTSPLIT (not run here).
**Result:** Not run here (wizard). Expected: B2 `Priya`, C2 `Sharma`; B3 `Ravi`, C3 `Kumar`; B4 `Meena`, C4 `Iyer`.
**Version note:** The Microsoft Support page lists Excel for Microsoft 365, 2024, 2021, 2019 and 2016. Google Sheets equivalent is Data > Split text to columns (from memory, unverified).
**Edge cases:** Three-word names split into three columns; a leading zero ID turns into a number unless the column format is Text; dates can be re-interpreted.
**Likely follow-ups:** 1) *Delimited vs fixed width?* See Q12. 2) *Will it update when data changes?* No, rerun it or use formulas.
**Common mistakes:** Not leaving empty columns to the right and overwriting data; forgetting a backup; not setting Text format for IDs.

### Q6 ⭐⭐⭐ 🟢 What is Flash Fill, and how do you trigger it?
**Asked at:** commonly asked (no company-specific report found); Flash Fill appears in the Analytics Vidhya Excel interview list (Jan 2024).
**What the interviewer is checking:** Do you know the pattern-based shortcut and its basic use?
**Say this in the interview:** "Flash Fill spots a pattern from an example you type and fills the rest of the column. I type the first result by hand, then press Ctrl+E, or use Data > Flash Fill. I use it for splitting names, joining text or reformatting codes."
**Explain simply:**
- You show Excel one or two examples; it guesses the rule.
- The result is plain typed values, not formulas, so it will not update if the source changes.
- It needs the examples in the column right next to the source data.
**Example:** From "Priya Sharma" you want only the first name.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | Full name | First name |
| 2 | Priya Sharma | Priya |
| 3 | Ravi Kumar | |
| 4 | Meena Iyer | |
| 5 | Karan Singh | |

**Formula / Steps:**
1. Type `Priya` in B2.
2. Click B3 (or the range B2:B5).
3. Press Ctrl+E, or Ribbon: Data tab > Data Tools group > Flash Fill.
4. Check the preview; press Enter to accept (Microsoft Support, "Using Flash Fill in Excel").
**Alternative:** `=LEFT(A2,FIND(" ",A2)-1)`, a live formula that updates; or Text to Columns.
**Result:** Not run here (feature). Expected: B3 `Ravi`, B4 `Meena`, B5 `Karan`.
**Version note:** The Microsoft Support page lists Excel for Microsoft 365, 2024, 2021, 2019 and 2016. On Windows it can run automatically if "Automatically Flash Fill" is ticked under File > Options > Advanced > Editing options.
**Edge cases:** Inconsistent data (some names with middle names) may fill wrongly; always scan the result.
**Likely follow-ups:** 1) *Is it a formula?* No, static values. 2) *No preview appears?* Automatic option may be off; use Ctrl+E.
**Common mistakes:** Trusting every filled row without checking; expecting it to refresh when new rows arrive.

### Q7 ⭐⭐⭐ 🟢 Given a list of employee IDs in column A, how do you flag the rows whose ID appears more than once?
**Asked at:** commonly asked (no company-specific report found); typical MIS scenario.
**What the interviewer is checking:** Can you write a COUNTIF flag with a correctly locked range?
**Say this in the interview:** "In B2 I write `=IF(COUNTIF($A$2:$A$8,A2)>1,"Duplicate","")` and fill down. COUNTIF counts how many times that ID appears in the whole list; if more than once, the row is flagged."
**Explain simply:**
- `COUNTIF(range, criteria)` counts cells in `range` that equal `criteria`.
- `$A$2:$A$8` is locked (absolute reference) so it does not slide when you fill down; `A2` is relative so it moves to A3, A4...
- All copies are flagged, including the first.
**Example:** Payroll IDs where E101 appears twice and E102 three times.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | EmpID | Flag |
| 2 | E101 | |
| 3 | E102 | |
| 4 | E103 | |
| 5 | E102 | |
| 6 | E104 | |
| 7 | E101 | |
| 8 | E102 | |

**Formula / Steps:** `B2: =IF(COUNTIF($A$2:$A$8,A2)>1,"Duplicate","")`, then double-click the fill handle.
**Alternative:** Flag only the repeats: `=IF(COUNTIF($A$2:A2,A2)>1,"Repeat","")`; or Conditional Formatting > Duplicate Values.
**Result:** Run in LibreOffice: "Duplicate" on rows 2, 3, 5, 7, 8; blank on rows 4 and 6. The repeat-only version flags rows 5, 7 and 8.
**Version note:** All Excel versions and Google Sheets (from memory, unverified).
**Edge cases:** Trailing spaces and different cases are treated differently (case is ignored, spaces are not); numbers stored as text vs numbers can look equal yet may not match; COUNTIF fails on strings over 255 characters.
**Likely follow-ups:** 1) *Two-column duplicates?* `COUNTIFS($A$2:$A$8,A2,$B$2:$B$8,B2)>1`. 2) *Whole column?* Avoid `A:A` on huge data, it is slow.
**Common mistakes:** Not locking the range, so counts shrink down the list; comparing to 1 instead of >1; forgetting to clean spaces first.

### Q8 ⭐⭐⭐ 🟡 When you use Remove Duplicates, which row does Excel keep, and how do the selected columns decide what counts as a duplicate?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand the first-kept rule and column selection logic, not just the button?
**Say this in the interview:** "Excel keeps the first occurrence from the top and deletes later ones. Only the columns I tick are compared: a row is a duplicate only if all ticked columns match an earlier row. If I tick only ID, rows with the same ID but different salary are still removed."
**Explain simply:**
- Ticked columns together form the *key*. Two ticked columns means both must match.
- "First" means closest to the top of the current sort order, so sort first if you want the newest or highest to survive.
- Matching uses what is displayed, not the hidden stored value (Microsoft Support, "Filter for unique values or remove duplicate values").
- A deleted row loses all columns, including unticked ones.
**Example:** Asha has two rows with different salaries (an old and a revised one).
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | EmpID | Name | Salary |
| 2 | E101 | Asha | 42000 |
| 3 | E102 | Ravi | 55000 |
| 4 | E101 | Asha | 45000 |
| 5 | E103 | Meena | 68000 |

**Formula / Steps:**
1. Data tab > Data Tools > Remove Duplicates.
2. Tick EmpID only: the 42000 row survives and 45000 is deleted.
3. Tick EmpID, Name and Salary: nothing is deleted, since the salaries differ.
**Alternative:** To keep the latest, sort by date descending first, or avoid deletion by using Advanced Filter > Unique records only into a new location.
**Result:** Run by pandas `drop_duplicates` as a stand-in (the Excel button is not run here): key EmpID keeps rows 2, 3, 5 (E101 at 42000, E102, E103); key EmpID+Name+Salary keeps all four rows.
**Version note:** Behaviour as described by Microsoft Support; case-insensitivity is from memory, unverified.
**Edge cases:** Hidden or filtered rows are still considered; display formatting (for example a date shown as "Jan-26") is what is compared.
**Likely follow-ups:** 1) *How do you keep the latest row?* Sort descending by date first. 2) *Can you preview?* No, so back up or flag with COUNTIF first.
**Common mistakes:** Assuming Excel keeps the "best" row; ticking too few columns and deleting real different records; not sorting first.

### Q9 ⭐⭐⭐ 🟡 Names in column A have extra spaces in front, behind and between words. How do you clean the whole column and keep the result as values?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the helper-column then Paste Values workflow?
**Say this in the interview:** "I use `=TRIM(A2)` in a helper column and fill it down. Then I copy that column and Paste Special > Values over the original, and delete the helper. That way the cleaned names are real text, not formulas pointing to deleted cells."
**Explain simply:**
- A formula result depends on the cells it refers to. If you delete column A while column B still holds formulas, you get #REF! errors.
- Paste Values freezes the result as plain text.
- TRIM handles front, back and between spaces (leaves one between words).
**Example:** Recruiter-typed names.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | Name | Clean |
| 2 | `  Priya   Sharma ` | |
| 3 | `Ravi Kumar  ` | |
| 4 | `  Meena Iyer` | |
| 5 | `Karan  Singh` | |

**Formula / Steps:**
1. `B2: =TRIM(A2)`; fill down to the last row.
2. Select B2:B5 > Ctrl+C.
3. Select A2 > Home tab > Paste (dropdown) > Paste Values (or Ctrl+Alt+V > Values > OK).
4. Delete column B.
**Alternative:** Do it in place with no formulas: Data > Get & Transform > From Table/Range > select column > Transform > Format > Trim > Close & Load; or for non-breaking spaces `=TRIM(SUBSTITUTE(A2,CHAR(160)," "))`.
**Result:** Run in LibreOffice: B2 `Priya Sharma`, B3 `Ravi Kumar`, B4 `Meena Iyer`, B5 `Karan Singh`.
**Version note:** TRIM and Paste Values work in all versions and Google Sheets (from memory, unverified). Power Query is from memory, unverified for Excel 2016.
**Edge cases:** If a space is still visible afterwards, it is likely CHAR(160) (Microsoft Support, "TRIM function"). Values stored as text do not change appearance.
**Likely follow-ups:** 1) *Why not just replace spaces?* Find and Replace would also delete the single space between first and last name. 2) *Why Paste Values?* To break the link to the raw column.
**Common mistakes:** Deleting the raw column before pasting values; pasting formulas over themselves in a circular way; not noticing CHAR(160).

### Q10 ⭐⭐⭐ 🟡 How do you remove duplicates safely so that you can recover the original data if something goes wrong?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you protect the source data before a destructive step?
**Say this in the interview:** "Because Remove Duplicates permanently deletes rows, I keep the raw data. I copy the sheet, or flag duplicates with a formula and filter first, or write unique records to a new location with Advanced Filter. I also compare row counts before and after."
**Explain simply:**
- Removing is permanent; filtering for unique values only hides rows temporarily (Microsoft Support, "Filter for unique values or remove duplicate values"). The page also recommends copying the original data first.
- Undo helps only until you close the file.
- Reconcile: rows before minus duplicates removed = rows after.
**Example:** 2,000 employee rows; a COUNTIF flag shows 120 repeats. After cleaning there must be 1,880 rows.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | EmpID | Repeat? |
| 2 | E101 | First |
| 3 | E102 | First |
| 4 | E102 | Repeat |
| 5 | E103 | First |

**Formula / Steps:**
1. Right-click the sheet tab > Move or Copy > tick Create a copy (name it Raw).
2. On the working sheet: `B2: =IF(COUNTIF($A$2:A2,A2)>1,"Repeat","First")`; fill down.
3. Check the repeats with a filter, then run Data > Remove Duplicates.
4. Compare counts: `=ROWS(Raw!A2:A5)` vs the new row count.
**Alternative:** Data > Advanced Filter > "Copy to another location" + "Unique records only", leaving the original untouched; or Power Query > Remove Rows > Remove Duplicates, which keeps the source and is repeatable.
**Result:** Run in LibreOffice: the same expanding-range COUNTIF gave First/First/Repeat/First style output on the Q3 test list (rows 5, 7, 8 were Repeat). By hand here: 4 rows in, 1 repeat, 3 rows out.
**Version note:** Advanced Filter exists in all versions (from memory, unverified); Power Query from Excel 2016 (from memory, unverified).
**Edge cases:** Sort order decides which copy survives; save the file under a new name (with a date) before the step.
**Likely follow-ups:** 1) *Can you undo after saving?* Not reliably. 2) *Why flag first?* To see what will be deleted.
**Common mistakes:** Working on the only copy; no row-count check; closing the file before noticing a mistake.

### Q11 ⭐⭐ 🟢 What is the difference between Remove Duplicates and filtering for unique values?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know one deletes and the other only hides?
**Say this in the interview:** "Remove Duplicates permanently deletes the repeated rows. An Advanced Filter with 'Unique records only' just hides the repeats, so the data is still there. I use filtering when I want to look or copy the unique list out, and Remove Duplicates when I am sure."
**Explain simply:**
- Filter = temporary view. Clear the filter and all rows return (Microsoft Support: "Filtering for unique values temporarily hides duplicate values").
- Remove Duplicates = permanent deletion.
- Both treat the first occurrence as the unique one.
**Example:** 6 rows with 3 repeats: filter shows 3 rows and keeps 6; remove deletes to 3.
**Formula / Steps:**
- Filter: Data tab > Sort & Filter group > Advanced > tick "Unique records only" (optionally "Copy to another location") > OK.
- Remove: Data tab > Data Tools > Remove Duplicates.
**Alternative:** `=UNIQUE(range)` in 365/2021 (not run here) gives a live unique list without touching the original.
**Version note:** Per Microsoft Support above; UNIQUE needs 365/2021 (from memory, unverified).
**Edge cases:** Advanced Filter needs a header row; with "Unique records only" the comparison is across all columns of the selected range.
**Likely follow-ups:** 1) *Which is safer?* The filter. 2) *Which is repeatable?* Power Query or UNIQUE.
**Common mistakes:** Believing the hidden rows are gone; deleting visible filtered rows by mistake.

### Q12 ⭐⭐ 🟢 What is the difference between Text to Columns delimited and fixed width?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know when to use each splitting mode?
**Say this in the interview:** "Delimited splits at a separator character, like a comma or hyphen. Fixed width splits at set positions, for example the first 6 characters are the ID. I use delimited when pieces are separated and fixed width when every code has the same layout."
**Explain simply:**
- Delimited: Excel finds the separator and cuts there; pieces can have different lengths.
- Fixed width: you drag break lines in the preview; each piece must be the same length in every row.
- Fixed width suits old payroll exports like `EMP00145000`.
**Example:** `E1010042000`: first 4 characters = ID `E101`, next 7 = salary `0042000` (fixed). `E101,Asha,42000` is delimited by commas.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Raw | | |
| 2 | E101,Asha,42000 | | |
| 3 | E102,Ravi,55000 | | |
| 4 | E1010042000 | | |

**Formula / Steps:** Data tab > Data Tools > Text to Columns > choose **Delimited** (tick Comma) or **Fixed width** (click in the preview to place break lines) > Next > set Destination > Finish.
**Alternative:** Formulas: `=LEFT(A4,4)` and `=MID(A4,5,7)` for fixed positions.
**Result:** Not run here (wizard). Expected: delimited rows split into `E101 | Asha | 42000`; fixed width on A4 gives `E101 | 0042000`. The Microsoft Support page we fetched covers only the delimited method, so fixed-width steps are from memory, unverified.
**Version note:** Available in Excel 2016 onward (Microsoft Support); Google Sheets only splits by separator (from memory, unverified).
**Edge cases:** A delimiter inside the text (a comma in "Sharma, Priya") breaks delimited splits; fixed width fails if lengths vary.
**Likely follow-ups:** 1) *How do you keep leading zeros?* Set the column data format to Text in step 3. 2) *Which for CSV?* Delimited.
**Common mistakes:** Using fixed width on variable-length data; not changing the destination.

### Q13 ⭐⭐ 🟢 What does the CLEAN function do, and how is it different from TRIM?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the difference between spaces and invisible characters?
**Say this in the interview:** "CLEAN removes non-printing characters such as line breaks and control codes that sneak in from other systems. TRIM removes extra spaces. I often combine them as `=TRIM(CLEAN(A2))`, and add SUBSTITUTE for the web-style non-breaking space."
**Explain simply:**
- *Non-printing characters* = invisible codes such as line break (code 10). CLEAN removes ASCII codes 0 to 31 (Microsoft Support, "CLEAN function").
- Microsoft notes CLEAN does not remove certain extra Unicode codes (for example 127, 129, 141, 143, 144, 157).
- TRIM works on spaces only and leaves CHAR(160) (Microsoft Support, "TRIM function").
**Example:** A name copied from an email with a line break inside, plus one with a non-breaking space.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | Raw | |
| 2 | Asha⏎Rao (line break) | |
| 3 | Ravi + bell char + " Das" | |
| 4 | Meena + CHAR(160) + Nair | |
| 5 | `  Karan   Singh  ` | |

**Formula / Steps:** `B2: =CLEAN(A2)`; full recipe `=TRIM(CLEAN(SUBSTITUTE(A2,CHAR(160)," ")))`.
**Alternative:** Find and Replace with Ctrl+J for line breaks; Power Query Transform > Format > Clean.
**Result:** Run in LibreOffice: CLEAN gives `AshaRao`, `Ravi Das`, `Meena` + CHAR(160) + `Nair` (unchanged), and `  Karan   Singh  ` (unchanged). The full recipe gives `AshaRao`, `Ravi Das`, `Meena Nair`, `Karan Singh` only when the non-breaking space is written as `UNICHAR(160)`: with `CHAR(160)` LibreOffice left `Meena` + nbsp + `Nair` unchanged (in Excel for Windows `CHAR(160)` is the standard recipe, from memory, unverified). The bell and line-break test cells were built with `CHAR(7)` and `CHAR(10)`.
**Version note:** CLEAN is listed for Excel 2016 through 365 (Microsoft Support). Google Sheets has CLEAN (from memory, unverified).
**Edge cases:** CLEAN removes a line break without adding a space, so "Asha" and "Rao" join; replace with a space first: `SUBSTITUTE(A2,CHAR(10)," ")`.
**Likely follow-ups:** 1) *Why a space still shows after TRIM?* CHAR(160). 2) *How to see hidden characters?* `=CODE(MID(A2,n,1))`.
**Common mistakes:** Thinking CLEAN removes spaces; losing the gap between words after CLEAN.

### Q14 ⭐⭐ 🟢 How do you use Find and Replace to fix inconsistent spellings such as 'Hyd' and 'Hyderabad'?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know Ctrl+H and its "partial match" trap?
**Say this in the interview:** "I press Ctrl+H, type the wrong spelling in Find what and the correct one in Replace with, and tick 'Match entire cell contents' so cells already saying Hyderabad do not become Hyderabaderabad. Then I use Replace All and check the list."
**Explain simply:**
- By default Find and Replace changes any part of a cell, which can damage correct entries.
- "Match entire cell contents" replaces only cells that equal exactly `Hyd`.
- Find and Replace changes the cells in place; there is no preview, so work on a copy.
**Example:** A city column from several offices.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | City | Naive SUBSTITUTE | Safe formula |
| 2 | Hyd | | |
| 3 | Hyderabad | | |
| 4 | HYD | | |
| 5 | Hyd. | | |
| 6 | Pune | | |

**Formula / Steps:**
1. Select the City column.
2. Ctrl+H (Home tab > Find & Select > Replace).
3. Find what: `Hyd`; Replace with: `Hyderabad`.
4. Click Options >>, tick **Match entire cell contents**.
5. Replace All. Repeat for `HYD` and `Hyd.` (case is ignored unless "Match case" is ticked, from memory, unverified).
**Alternative:** A mapping table plus VLOOKUP (or XLOOKUP in 365/2021; Microsoft's XLOOKUP page has a note saying it is not available in Excel 2016 and 2019 while its Applies-to list names them, so I treat it as 2021/365 only; not run here), which is auditable: list wrong and right spellings and look up each city. Or `=IF(OR(TRIM(A2)="Hyd",TRIM(A2)="Hyd."),"Hyderabad",A2)`.
**Result:** Run in LibreOffice: naive `=SUBSTITUTE(A2,"Hyd","Hyderabad")` returns `Hyderabad`, `Hyderabaderabad`, `HYD`, `Hyderabad.`, `Pune`: it damages row 3. The safe IF formula returns `Hyderabad` for rows 2 to 5 and `Pune` for row 6 (the `=` test ignores case).
**Version note:** Ctrl+H works in all versions and Google Sheets (from memory, unverified).
**Edge cases:** Wildcards `*` and `?` in Find what act as wildcards; type `~*` to find a real asterisk.
**Likely follow-ups:** 1) *Many spellings?* Use a mapping table. 2) *Trailing spaces?* TRIM first.
**Common mistakes:** Replacing without "Match entire cell contents"; running on the whole sheet instead of one column.

### Q15 ⭐⭐ 🟢 How do you find and handle blank cells in a column of data?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you locate blanks and decide sensibly what to do with them?
**Say this in the interview:** "I count them with COUNTBLANK, and select them with Go To Special > Blanks. Then I decide: fill with a value like 'Unknown', fill from the cell above, delete the row, or leave them and exclude them in calculations. The right choice depends on what the blank means."
**Explain simply:**
- A *blank* is an empty cell; a cell with a formula returning "" or a space only looks blank.
- Filtering the column and choosing (Blanks) also isolates them.
**Example:** Department column in an HR list of 6 rows with 2 missing entries.
**Sample sheet:**

| | A |
|---|---|
| 1 | Dept |
| 2 | HR |
| 3 | Finance |
| 4 | (blank) |
| 5 | IT |
| 6 | (blank) |
| 7 | HR |

**Formula / Steps:**
- Count: `=COUNTBLANK(A2:A7)`; non-blank `=COUNTA(A2:A7)`; total rows `=ROWS(A2:A7)`.
- Select: select A2:A7 > Home > Find & Select > Go To Special > Blanks > OK.
- Fill with text: type `Unknown` and press Ctrl+Enter to fill all selected blanks.
**Alternative:** Filter dropdown > untick Select All > tick (Blanks); or `=SUMPRODUCT(--(LEN(TRIM(A2:A7))=0))` to also catch space-only cells.
**Result:** Run in LibreOffice: COUNTBLANK = 2, COUNTA = 4, ROWS = 6, SUMPRODUCT version = 2.
**Version note:** All versions (from memory, unverified); Go To Special is also under F5 > Special.
**Edge cases:** COUNTBLANK counts cells with `""` from a formula but not cells holding a single space. Zero is not blank.
**Likely follow-ups:** 1) *Delete or fill?* Ask what the blank means. 2) *How to fill from above?* See Q16.
**Common mistakes:** Treating zero and blank as the same; deleting rows that still hold useful data in other columns.

### Q16 ⭐⭐ 🟢 How do you fill blank cells in a column with the value from the cell above?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the Go To Special + formula trick for grouped reports?
**Say this in the interview:** "I select the column, use Go To Special > Blanks, type `=` and press the Up arrow, then Ctrl+Enter. Excel puts a formula in every blank pointing to the cell above. Then I copy the column and Paste Values so it becomes permanent."
**Explain simply:**
- Reports often show a city once and leave the next rows blank; analysis needs it on every row.
- `Ctrl+Enter` writes the same entry to all selected cells; relative references adjust per cell.
- Each blank copies the cell above, which may itself be a filled blank, so the value carries down.
**Example:** Region shown once per group.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | Region | Employee |
| 2 | Hyderabad | Asha |
| 3 | | Ravi |
| 4 | | Meena |
| 5 | Pune | Karan |
| 6 | | Divya |
| 7 | Chennai | Imran |

**Formula / Steps:**
1. Select A2:A7.
2. Home tab > Find & Select > Go To Special > Blanks > OK (only the empty cells are selected).
3. Type `=` then press the Up arrow (this writes `=A2` for A3), then press **Ctrl+Enter**.
4. Select A2:A7 > Copy > Paste Special > Values.
**Alternative:** Helper column with `C2: =A2`, `C3: =IF(A3="",C2,A3)`, fill down, then paste values; or Power Query > Transform > Fill > Down.
**Result:** Run in LibreOffice (helper-column version): C2:C7 = Hyderabad, Hyderabad, Hyderabad, Pune, Pune, Chennai. The Go To Special click path is not run here.
**Version note:** Go To Special works in all versions; Power Query Fill Down is built in from Excel 2016 (from memory, unverified).
**Edge cases:** If the first cell is blank there is nothing above it; hidden or filtered rows still receive values; merged cells must be unmerged first.
**Likely follow-ups:** 1) *Why paste values?* So sorting does not break the formulas. 2) *Fill from below?* Use the Down arrow instead.
**Common mistakes:** Forgetting Ctrl+Enter (only one cell is filled); sorting before converting formulas to values.

### Q17 ⭐⭐ 🟢 Numbers imported from another system are left-aligned and will not add up. What is the problem, and how do you fix it?
**Asked at:** commonly asked (no company-specific report found); VALUE appears in the Analytics Vidhya cleaning-related list (Jan 2024).
**What the interviewer is checking:** Do you recognise numbers stored as text and know several fixes?
**Say this in the interview:** "Those numbers are stored as text; the left alignment and a small green triangle give it away. I convert them using Text to Columns, or `=VALUE(TRIM(A2))`, or multiply by 1, and then paste as values. SUM ignores text, so the total comes out too low."
**Explain simply:**
- *Text number* = digits that Excel treats as words, so it cannot add them.
- Real numbers right-align by default; text left-aligns.
- Imports often add hidden spaces or CHAR(160), which also stop conversion.
**Example:** Basic salary column from an old payroll system.
**Sample sheet:**

| | A |
|---|---|
| 1 | Salary |
| 2 | `45000` (text) |
| 3 | `  52000` (text, leading spaces) |
| 4 | `38000 ` (text, trailing space) |
| 5 | CHAR(160) + `61000` (text) |
| 6 | 47000 (real number) |

**Formula / Steps:**
- Quick: select the column > Data tab > Text to Columns > Finish (without changing anything). Or click the yellow warning icon > Convert to Number.
- Formula: `B2: =VALUE(TRIM(A2))`; for the CHAR(160) row `=VALUE(TRIM(SUBSTITUTE(A2,CHAR(160)," ")))`; then Copy > Paste Special > Values.
**Alternative:** `=--A2` or `=A2*1`; Paste Special > Multiply by a cell containing 1; Power Query: Transform > Data Type > Whole Number.
**Result:** Run in LibreOffice: ISTEXT is TRUE for rows 2 to 5 and FALSE for row 6. `=SUM(A2:A6)` returns 47000 (only the real number). The CHAR(160)-aware VALUE formula returns 45000, 52000, 38000, 61000, 47000, and the total is 243000. Plain `VALUE(TRIM(A5))` on row 5 also returned 61000 in LibreOffice, because LibreOffice's VALUE tolerates the non-breaking space; Excel may return #VALUE! there (from memory, unverified), so keep the SUBSTITUTE in the formula. `VALUE(TRIM())` on rows 2 to 4 returned 45000, 52000, 38000.
**Version note:** All versions (from memory, unverified). Convert to Number prompt wording can differ by version.
**Edge cases:** Leading zeros (ID codes like 00123) should stay text. Decimal commas vs points depend on regional settings; `NUMBERVALUE` handles separators (from memory, unverified). In Excel, `+` arithmetic may coerce some text that SUM ignores; LibreOffice behaves similarly but not identically.
**Likely follow-ups:** 1) *Why does SUM show 0?* It skips text. 2) *How to check?* `=ISTEXT(A2)` or `=ISNUMBER(A2)`.
**Common mistakes:** Changing the cell format to Number without re-entering (text stays text); not removing CHAR(160); converting ID codes that should stay text.

### Q18 ⭐⭐ 🟢 How do you split a full name in one column into first name and last name in two columns?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you take text apart with simple functions, and do you think about names that do not fit the pattern?
**Say this in the interview:** "For a one-off I use Text to Columns with a space as the separator. If the list will be refreshed, I use LEFT and FIND for the first name and MID for the rest, wrapped in TRIM so extra spaces do not break it."
**Explain simply:**
- A *delimiter* is the character that separates the parts, here a space.
- `FIND(" ",text)` tells you the position of the first space; `LEFT` takes everything before it, `MID` takes everything after it.
- Adding `&" "` inside FIND means a one-word name like "Meena" does not give an error.
- Decide first what "last name" means: everything after the first word (Kumar Reddy) or only the last word (Reddy).
**Example:** An HR master list has 5 names typed by different people; one has only a first name, one has a middle name, one has extra spaces.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Full Name | First | Last |
| 2 | Priya Sharma | | |
| 3 | Ravi Kumar | | |
| 4 | Meena | | |
| 5 | Anil Kumar Reddy | | |
| 6 |   Divya   Nair  | | |

**Formula / Steps:** B2 `=LEFT(TRIM(A2),FIND(" ",TRIM(A2)&" ")-1)`; C2 `=TRIM(MID(TRIM(A2),FIND(" ",TRIM(A2)&" ")+1,100))`; fill down.
Feature route: select A2:A6 > Data tab > Data Tools > Text to Columns > Delimited > tick Space > choose a Destination such as $B$2 > Finish.
**Alternative:** Only the last word: `=TRIM(RIGHT(SUBSTITUTE(TRIM(A2)," ",REPT(" ",100)),100))`. Or in 365/2024, `=TEXTBEFORE(A2," ")` (not run here). Or Flash Fill (Ctrl+E).
**Result:** Run in LibreOffice. First: Priya, Ravi, Meena, Anil, Divya. Last (C): Sharma, Kumar, (blank), Kumar Reddy, Nair. The last-word formula gives Reddy for row 5 and Meena for row 4.
**Version note:** The LEFT/FIND/MID formulas work in all Excel versions and Google Sheets. TEXTBEFORE needs Excel 365/2024 (from memory, unverified; see Q41).
**Edge cases:** One-word names leave Last blank. Middle names, suffixes like "Jr" and surnames with spaces cannot be split reliably by any rule; check those rows by eye.
**Likely follow-ups:** 1) *What if Text to Columns overwrites the next column?* It does, so insert empty columns or set a Destination first. 2) *Why TRIM first?* Double spaces create empty pieces.
**Common mistakes:** Forgetting that Text to Columns replaces data to its right; no TRIM; not planning for one-word names.

### Q19 ⭐⭐ 🟢 How do you delete all blank rows from a dataset?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know a safe method that does not delete rows that only have one blank cell?
**Say this in the interview:** "I add a helper column that counts filled cells in each row, filter for zero, and delete those rows. The quick Go To Special > Blanks route deletes any row with a blank in the selected column, so I only use it on a column that is never blank in a real record."
**Explain simply:**
- A *blank row* means every cell in the row is empty. A row with only one gap (a missing department) is real data and must stay.
- `COUNTA` counts the cells that are not empty. Zero means the whole row is empty.
- Go To Special > Blanks selects empty cells; deleting their *sheet rows* removes every row that had a selected blank.
**Example:** An attendance export has gaps between daily blocks. Row 5 has no Name, but the other cells are filled, so it must stay.
**Sample sheet:**

| | A | B | C | D |
|---|---|---|---|---|
| 1 | EmpID | Name | Dept | Filled |
| 2 | 101 | Asha | HR | |
| 3 | | | | |
| 4 | 103 | Meena | IT | |
| 5 | 104 | | HR | |
| 6 | | | | |
| 7 | 106 | Divya | Sales | |

**Formula / Steps:** D2 `=COUNTA(A2:C2)`, fill down. Then: 1) Select the table > Data tab > Sort & Filter > Filter. 2) Filter column D to 0. 3) Select the visible rows > right-click row headers > Delete Row. 4) Clear the filter and delete column D.
**Alternative:** Select the one column that is always filled (EmpID) > Home > Find & Select > Go To Special > Blanks > OK > Home > Cells > Delete > Delete Sheet Rows. Or sort by the helper column so the empty rows sit at the bottom.
**Result:** Run in LibreOffice: D2:D7 = 3, 0, 3, 2, 0, 3. Delete rows 3 and 6 only; row 5 (count 2) stays.
**Version note:** Available in every Excel version and in Google Sheets (Sheets has Data > Create a filter; from memory, unverified).
**Edge cases:** Cells with a space or `""` from a formula look blank but are not counted as empty by COUNTA; use `=SUMPRODUCT(--(LEN(TRIM(A2:C2))>0))` instead. Never delete rows while rows are filtered without selecting only visible rows.
**Likely follow-ups:** 1) *Why not just sort?* Sorting changes the order; add a numbering column first if order matters. 2) *Faster in Power Query?* Yes, Remove Rows > Remove Blank Rows.
**Common mistakes:** Running Go To Special on the whole table and deleting rows that had a single gap; deleting without a backup.

### Q20 ⭐⭐ 🟢 How do you use Data Validation to stop bad data from entering a sheet in the first place?
**Asked at:** commonly asked (no company-specific report found); Data Validation appears in a fetched Analytics Vidhya Excel question list.
**What the interviewer is checking:** Do you prevent dirty data, not just clean it later?
**Say this in the interview:** "I use Data > Data Validation to set rules for a cell range: a drop-down list for department, whole numbers only for age, and a custom formula to block duplicate employee IDs. Excel then rejects or warns about wrong entries."
**Explain simply:**
- *Data Validation* = rules attached to cells that decide what can be typed.
- Allow types: Whole number, Decimal, List, Date, Text length, Custom (your own TRUE/FALSE formula).
- The Error Alert tab chooses the response: Stop (blocks), Warning or Information (allow after a prompt).
- Validation only checks new typing. It does not clean data already there, and pasting over a cell can bypass it.
**Example:** HR onboarding sheet: Dept must be one of HR, IT, Finance, Sales; EmpID must be unique; joining date cannot be in the future.
**Sample sheet:**

| | A (EmpID) | B (Check) |
|---|---|---|
| 2 | E101 | |
| 3 | E102 | |
| 4 | E103 | |
| 5 | E102 | |

**Formula / Steps:** 1) Select A2:A100. 2) Data tab > Data Tools > Data Validation. 3) Settings > Allow: Custom > Formula `=COUNTIF($A$2:$A$100,A2)=1`. 4) Error Alert tab > Style: Stop > type a clear message > OK. For a drop-down: Allow: List > Source `HR,IT,Finance,Sales`.
**Alternative:** For existing data: Data Validation > Circle Invalid Data (Data Tools group's drop-down arrow). Or use a drop-down list from a named range so the list can grow.
**Result:** The custom rule's test formula, run in LibreOffice for B2:B5 = TRUE, FALSE, TRUE, FALSE (E102 appears twice, so both fail). Typing the second E102 into a validated cell would be blocked. The pop-up itself is a feature, not run here.
**Version note:** Present in all Excel versions and in Google Sheets (Data > Data validation; from memory, unverified).
**Edge cases:** Copy-paste overwrites validation. A custom rule using COUNTIF on a range that includes the cell itself works as shown. Blank cells pass unless "Ignore blank" is unticked.
**Likely follow-ups:** 1) *Can validation fix old data?* No; use Circle Invalid Data then fix. 2) *Dependent drop-downs?* Use INDIRECT or a lookup-based list (advanced).
**Common mistakes:** Forgetting that pasting bypasses rules; leaving the alert style on Information so bad data still goes in.

### Q21 ⭐⭐ 🟡 Remove Duplicates does not remove two rows that look identical. What could be the reasons, and how do you find out?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that "looks the same" is not "is the same", and can you diagnose it?
**Say this in the interview:** "Usually one of the two has an invisible difference: a trailing space, a non-breaking space, a number stored as text, or a hidden character. I check with LEN, EXACT and ISNUMBER, clean with TRIM and SUBSTITUTE, then run Remove Duplicates again."
**Explain simply:**
- Remove Duplicates compares what is in the selected columns. If even one invisible character differs, the rows are different.
- Frequent reasons: trailing/leading spaces; non-breaking space (character 160, which TRIM cannot remove, Microsoft Support "TRIM function"); text "123" vs number 123; line breaks; dates with different hidden times; or you ticked a column that really differs.
- Microsoft says the comparison uses the *displayed* value (Microsoft Support "Filter for unique values or remove duplicate values"), so formatting can also matter.
**Example:** Two "Priya" rows for the same employee; one was typed with a space at the end.
**Sample sheet:**

| | A (Name) | B (LEN) | C (last char code) | D (EXACT vs A2) |
|---|---|---|---|---|
| 2 | Priya | | | |
| 3 | Priya␠ (space) | | | |
| 4 | Priya (nbsp) | | | |
| 5 | Priya | | | |

**Formula / Steps:** B2 `=LEN(A2)`; C2 `=UNICODE(RIGHT(A2,1))` (listed for Excel 2016 and later by Microsoft); D3 `=EXACT(A3,A$2)`. Fix: `=TRIM(SUBSTITUTE(A2,CHAR(160)," "))`, paste as values, run Data > Data Tools > Remove Duplicates.
**Alternative:** Conditional formatting > Duplicate Values highlights what Excel thinks matches; the rows that should but do not are your suspects. Or Power Query > Transform > Trim/Clean.
**Result:** Run in LibreOffice: LEN = 5, 6, 6, 5; last char code = 97, 32, 160, 97; EXACT = FALSE, FALSE, TRUE for rows 3, 4, 5. So rows 3 and 4 hide a space and a non-breaking space. Row 5 is a true duplicate.
**Version note:** Microsoft's UNICODE function page lists Excel 2016, 2019, 2021, 2024 and 365 (Microsoft Support, "UNICODE function"); that it arrived in Excel 2013 is from memory, unverified. The rest works everywhere.
**Edge cases:** `CHAR(160)` works in Excel on Windows; in LibreOffice it did not match, so I tested with UNICHAR(160), which does. ISNUMBER catches text numbers.
**Likely follow-ups:** 1) *Does case matter?* Remove Duplicates ignores case (from memory, unverified); see Q32. 2) *Why not just retype?* Does not scale.
**Common mistakes:** Trusting your eyes; using TRIM and assuming it fixed everything.

### Q22 ⭐⭐ 🟡 TRIM does not remove a space that is clearly visible in a cell. What is going on, and what formula fixes it?
**Asked at:** commonly asked (no company-specific report found); the CHAR(160) fix appears in study notes found in search.
**What the interviewer is checking:** Do you know TRIM only removes the ordinary space?
**Say this in the interview:** "That is probably a non-breaking space, character code 160, common in web-pasted data. TRIM only removes the normal space, code 32. I swap code 160 for a normal space with SUBSTITUTE and then TRIM."
**Explain simply:**
- Two characters look like spaces: normal (code 32) and non-breaking (code 160, an HTML space).
- TRIM handles only 32; the Microsoft page says TRIM "does not remove this nonbreaking space character" (Microsoft Support, "TRIM function").
- Check with `=UNICODE(RIGHT(A2,1))`: 160 confirms it.
- Wrap `CLEAN` as well to strip non-printing characters (see Q13).
**Example:** Names copied from an HR web portal; "Priya Sharma " will not match the master list in VLOOKUP.
**Sample sheet:**

| | A | B |
|---|---|---|
| 2 | `Priya`+nbsp+`Sharma`+nbsp | |

**Formula / Steps:** `=TRIM(SUBSTITUTE(A2,CHAR(160)," "))`. Safer on all platforms: `=TRIM(SUBSTITUTE(A2,UNICHAR(160)," "))`. With line breaks too: `=TRIM(CLEAN(SUBSTITUTE(A2,CHAR(160)," ")))`. Then copy > Paste Special > Values.
**Alternative:** Find & Replace: in Find what press Alt+0160 on the numeric keypad (or paste the character), leave Replace with empty or one space.
**Result:** Run in LibreOffice using UNICHAR(160): LEN before TRIM = 13 and LEN(TRIM) still = 13 (TRIM did nothing); after the fix the text is "Priya Sharma" with LEN 12; the last character code was 160.
**Version note:** CHAR and SUBSTITUTE work everywhere; UNICHAR and UNICODE are listed from Excel 2016 on Microsoft's UNICODE page (the 2013 start is from memory, unverified).
**Edge cases:** Other odd spaces exist (zero-width space, code 8203); check with UNICODE and substitute them too. LibreOffice's CHAR(160) did not match, hence UNICHAR in my test; Excel for Windows CHAR(160) is the standard recipe (from memory).
**Likely follow-ups:** 1) *How to detect?* LEN vs LEN(TRIM). 2) *Does CLEAN remove it?* No, CLEAN removes codes 0 to 31.
**Common mistakes:** Applying TRIM again and again; forgetting to paste as values.

### Q23 ⭐⭐ 🟡 Dates imported from a CSV file are stored as text. How do you convert them into real dates?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know a date is a number underneath and can convert text to one reliably?
**Say this in the interview:** "First I confirm they are text: they are left-aligned and ISNUMBER says FALSE. For a quick fix I use Text to Columns with the right Date order, or DATEVALUE. If the format is fixed, I rebuild the date with DATE, LEFT, MID and RIGHT, which does not depend on regional settings."
**Explain simply:**
- Excel stores a real date as a serial number (days since 1900). Text that looks like a date cannot be sorted or subtracted.
- `DATEVALUE` reads text using the computer's regional setting, so "03/04/2026" may come out as 3 April or 4 March.
- `DATE(year,month,day)` with pieces you cut out yourself always means what you intend.
**Example:** HRMS export gives joining dates as text; tenure calculation fails.
**Sample sheet:**

| | A (text) | B (real date) |
|---|---|---|
| 2 | 15/03/2026 | |
| 3 | 02/11/2026 | |
| 4 | 2026-03-15 | |

**Formula / Steps:** B2 `=DATE(RIGHT(A2,4),MID(A2,4,2),LEFT(A2,2))` (dd/mm/yyyy); B4 `=DATE(LEFT(A4,4),MID(A4,6,2),RIGHT(A4,2))` (yyyy-mm-dd). Then format B as Date.
Text to Columns route: select the column > Data > Data Tools > Text to Columns > Next > Next > Column data format: Date, choose DMY > Finish.
**Alternative:** `=DATEVALUE(A2)` when the text matches your regional format; `=A2*1` or `--A2` to coerce.
**Result:** Run in LibreOffice: B2 = 15-Mar-2026, B3 = 02-Nov-2026, B4 = 15-Mar-2026 (all numeric; ISNUMBER on column A = FALSE for all three).
**Version note:** All versions. DATEVALUE results depend on regional settings (from memory).
**Edge cases:** Mixed formats (Q24); two-digit years; text with times; spaces (TRIM first).
**Likely follow-ups:** 1) *Why not reformat the cell?* Formatting does not change text into a number. 2) *How to check?* ISNUMBER or right-aligned.
**Common mistakes:** Changing format to Date and expecting conversion; trusting DATEVALUE on a different computer.

### Q24 ⭐⭐ 🟡 A date column has some entries as dd/mm/yyyy and others as mm/dd/yyyy. How do you detect and fix this?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you recognise ambiguity and avoid guessing silently?
**Say this in the interview:** "I split each date into its two parts. If the first part is above 12 it must be the day; if the second is above 12 it must be the month. Dates where both are 12 or less are ambiguous, so I resolve them with the source system, the file's sort order, or the person who owns the data, and I tell my manager how many I could not prove."
**Explain simply:**
- 15/03 can only be 15 March. 04/05 could be 4 May or 5 April.
- A common symptom: Excel on a US setting turns 03/15 into a real date but leaves 15/03 as left-aligned text.
- No formula can decide an ambiguous date; you need a rule from the source.
**Example:** Attendance logs merged from a Hyderabad office (dd/mm) and a US vendor (mm/dd).
**Sample sheet:**

| | A (text) | B (verdict) |
|---|---|---|
| 2 | 15/03/2026 | |
| 3 | 03/15/2026 | |
| 4 | 04/05/2026 | |
| 5 | 28/02/2026 | |
| 6 | 02/28/2026 | |

**Formula / Steps:** B2 `=IF(VALUE(LEFT(A2,2))>12,"dd/mm",IF(VALUE(MID(A2,4,2))>12,"mm/dd","ambiguous"))`. Filter by verdict. Convert each group separately with DATE (Q23), e.g. mm/dd rows `=DATE(RIGHT(A3,4),LEFT(A3,2),MID(A3,4,2))`.
**Alternative:** Fix at source by re-exporting as yyyy-mm-dd; or in Power Query use Change Type with Locale per source file.
**Result:** Run in LibreOffice: dd/mm, mm/dd, ambiguous, dd/mm, mm/dd for rows 2 to 6. Row 4 stays ambiguous.
**Version note:** Works in all versions (text functions only).
**Edge cases:** If a whole file has one format, use that file's rule for all rows, even ambiguous ones. Single-digit days/months (5/3/2026) break the fixed positions; split on "/" instead.
**Likely follow-ups:** 1) *How do you prevent it?* Agree yyyy-mm-dd in exports. 2) *Can you guess by position?* Only with evidence, such as dates in sequence.
**Common mistakes:** Forcing one format on the whole column and silently swapping day and month.

### Q25 ⭐⭐ 🟡 What are the limitations of Flash Fill, and when would you use a formula instead?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know Flash Fill is a quick helper, not a repeatable process?
**Say this in the interview:** "Flash Fill guesses a pattern from my example and fills values, which is great for quick one-offs. But the results are static, it can guess wrong on irregular rows, and it will not update when the data changes. For anything repeatable or refreshed monthly I use formulas or Power Query."
**Explain simply:**
- *Flash Fill* (Ctrl+E or Data > Flash Fill) spots a pattern from what you typed next to the data. The limits below come from tutorials and practice, not from a Microsoft page I fetched.
- Limits: pasted values, not formulas; does not refresh; can guess wrong when rows differ; needs a clear example; often weaker on numbers and long mixed text; it must sit next to the source data.
- Always check the filled column row by row.
**Example:** Initials from names: one example "PS" works for "Priya Sharma", but "Meena" (no surname) and "Anil Kumar Reddy" (three words) may be guessed differently.
**Sample sheet:**

| | A (Name) | B (Initials formula) |
|---|---|---|
| 2 | Priya Sharma | |
| 3 | Ravi Kumar | |
| 4 | Anil Kumar Reddy | |
| 5 | Meena | |

**Formula / Steps:** `=LEFT(A2)&MID(A2,FIND(" ",A2&" ")+1,1)`; fill down. Flash Fill: type PS in B2, press Ctrl+E in B3 (Data > Data Tools > Flash Fill).
**Alternative:** Power Query (Data > Get & Transform) keeps the steps and replays them on new data.
**Result:** Formula run in LibreOffice: PS, RK, AK, M. The formula states its rule exactly; Flash Fill's output for the last two rows is "not run here" (I cannot run the feature) and is the kind of thing to verify.
**Version note:** Microsoft's Flash Fill page lists Excel 2016, 2019, 2021, 2024 and 365 and lists no limitations (Microsoft Support, "Using Flash Fill in Excel"); that it started in Excel 2013 is from memory, unverified.
**Edge cases:** Blank or inconsistent source rows; automatic fill may be switched off (File > Options > Advanced > Automatically Flash Fill).
**Likely follow-ups:** 1) *Does it update?* No. 2) *Is it reliable for dates?* Not always; use real date functions.
**Common mistakes:** Not checking the output; using it on data that will be refreshed.

### Q26 ⭐⭐ 🟡 A column holds 'EMP001 - Priya Sharma - Hyderabad'. How do you split it into three columns using Text to Columns, and what must you do before you run it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you protect neighbouring data and choose a delimiter that will not break names?
**Say this in the interview:** "Before running it I insert empty columns to the right, or set a destination, because Text to Columns overwrites whatever is there, and I keep a backup. The delimiter is ' - '. I replace it with a pipe sign first because Text to Columns takes a single character, then split on the pipe, so hyphens inside names like Anne-Marie are safe."
**Explain simply:**
- *Delimiter* = the character that separates pieces. A hyphen alone is risky because names can contain hyphens.
- Excel's "Other" box accepts one character (from memory, unverified), so replace ' - ' with '|' first.
- Text to Columns writes the results into the next columns, overwriting them without asking.
**Example:** An HR system export puts ID, name and city in one cell.
**Sample sheet:**

| | A |
|---|---|
| 2 | EMP001 - Priya Sharma - Hyderabad |
| 3 | EMP002 - Ravi Kumar - Pune |
| 4 | EMP003 - Anne-Marie Joseph - Chennai |

**Formula / Steps:** 1) Copy the sheet as backup. 2) Insert 2 blank columns right of A. 3) Select A2:A4 > Ctrl+H > Find ` - ` Replace with `|` > Replace All. 4) Data tab > Data Tools > Text to Columns > Delimited > Next > tick Other, type `|` > Next > set Destination `$B$2` and, if codes have leading zeros, set that column to Text > Finish.
**Alternative:** Formula, no overwrite risk: `=TRIM(MID(SUBSTITUTE($A2," - ",REPT(" ",100)),(1-1)*100+1,100))` and change 1 to 2 and 3 for the other pieces.
**Result:** Formula run in LibreOffice: row 2 = EMP001, Priya Sharma, Hyderabad; row 3 = EMP002, Ravi Kumar, Pune; row 4 = EMP003, Anne-Marie Joseph, Chennai. A hyphen-only split gave "Anne" for the name column, which shows the risk. The Text to Columns wizard itself is not run here.
**Version note:** Text to Columns exists in all Excel versions (Data tab); Google Sheets has Data > Split text to columns (from memory, unverified).
**Edge cases:** Extra spaces left over (TRIM); IDs such as 007 lose zeros unless the column format is Text.
**Likely follow-ups:** 1) *Undo?* Ctrl+Z works right after, not later. 2) *Repeatable?* Use the formula or Power Query.
**Common mistakes:** Not choosing a destination and overwriting data; splitting on "-" alone.

### Q27 ⭐⭐ 🟡 How do you count how many duplicate records exist in a dataset using formulas?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you count duplicates precisely and say which definition you used?
**Say this in the interview:** "First I define it: extra copies, or all rows that belong to a repeated ID. For extra copies I count rows minus distinct IDs. I also add a helper column using COUNTIF with an expanding range, which marks the second and later occurrences."
**Explain simply:**
- `COUNTIF(range,value)` counts how many times a value appears.
- Expanding range `$A$2:A2` counts only up to the current row, so the first occurrence is 1 and repeats are 2, 3...
- `SUMPRODUCT(1/COUNTIF(...))` counts distinct values: each value contributes 1 in total.
**Example:** Payroll IDs: E102 appears three times, E101 twice.
**Sample sheet:** A2:A9.

| | A (EmpID) | B (is repeat?) |
|---|---|---|
| 2 | E101 | |
| 3 | E102 | |
| 4 | E103 | |
| 5 | E102 | |
| 6 | E104 | |
| 7 | E102 | |
| 8 | E101 | |
| 9 | E105 | |

**Formula / Steps:** B2 `=COUNTIF($A$2:A2,A2)>1`, fill down. Extra copies: `=SUMPRODUCT(--B2:B9)` or `=ROWS(A2:A9)-SUMPRODUCT(1/COUNTIF(A2:A9,A2:A9))`. Rows involved in any repeat: `=SUMPRODUCT(--(COUNTIF(A2:A9,A2:A9)>1))`.
**Alternative:** Excel 365/2021: `=ROWS(A2:A9)-COUNTA(UNIQUE(A2:A9))` (not run here; expected 3).
**Result:** Run in LibreOffice: extra copies = 3; rows involved in a repeat = 5 (E101 x2, E102 x3); unique-once IDs = 3. Helper flags TRUE for rows 5, 7 and 8.
**Version note:** COUNTIF and SUMPRODUCT work in every version. UNIQUE needs Excel 2021/365 (Microsoft Support, "UNIQUE function": Excel 365, 2024, 2021).
**Edge cases:** Blank cells make the `1/COUNTIF` formula return #DIV/0!; clean blanks first. Text numbers and spaces count as different values. COUNTIF treats wildcards (* ?) in text as patterns.
**Likely follow-ups:** 1) *Duplicates on two columns?* See Q40. 2) *How to remove them?* Q1/Q8.
**Common mistakes:** Mixing the two definitions; using a fixed range so every row counts itself as a duplicate.

### Q28 ⭐⭐ 🟡 How do you keep only the latest record per employee ID when an HR list has several rows per employee?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know Remove Duplicates keeps the first row, so the sort order decides which survives?
**Say this in the interview:** "I sort by date, newest first, then run Remove Duplicates on EmpID only. Excel keeps the first occurrence, which is now the latest. If I want to see everything first, I mark the latest row with MAXIFS and filter."
**Explain simply:**
- Remove Duplicates keeps the first occurrence it meets (Microsoft Support, "Filter for unique values or remove duplicate values").
- Sort by UpdatedOn descending first; the newest row is then first for each ID.
- Tick *only* EmpID, otherwise rows with different departments count as different.
**Example:** Employee 101 changed department three times; the HR master should keep only the current one.
**Sample sheet:** A1:D7 with helper E.

| | A | B | C | D (UpdatedOn) |
|---|---|---|---|---|
| 2 | 101 | Asha | HR | 2025-04-01 |
| 3 | 102 | Ravi | Finance | 2025-01-10 |
| 4 | 101 | Asha | Admin | 2026-02-15 |
| 5 | 103 | Meena | IT | 2025-08-05 |
| 6 | 102 | Ravi | Sales | 2026-06-30 |
| 7 | 101 | Asha | Admin | 2025-12-01 |

**Formula / Steps:** Backup first. 1) Data > Sort & Filter > Sort: UpdatedOn, Newest to Oldest. 2) Data > Data Tools > Remove Duplicates, tick only EmpID. Or mark rows: E2 `=IF(D2=MAXIFS($D$2:$D$7,$A$2:$A$7,A2),"Keep","Old")`, filter for Old and delete.
**Alternative:** 365: `=SORT(...)` with `UNIQUE` on the sorted list (not run here). Or a pivot with Max of date.
**Result:** MAXIFS marker run in LibreOffice: Old, Old, Keep, Keep, Keep, Old for rows 2 to 7. Sorting plus de-duplication reproduced in pandas: 101 Asha Admin 2026-02-15; 102 Ravi Sales 2026-06-30; 103 Meena IT 2025-08-05.
**Version note:** Microsoft's MAXIFS page says the feature is available if you have Office 2019 or a Microsoft 365 subscription, and lists Excel 2019, 2021, 2024 and 365; Excel 2016 (non-subscription) is not listed (Microsoft Support, "MAXIFS function"). The marker formula was run in LibreOffice with the `_xlfn.` prefix. Sort and Remove Duplicates work everywhere.
**Edge cases:** Two rows with the same latest date both get "Keep"; add a tie-breaker. Dates stored as text sort wrongly (Q23).
**Likely follow-ups:** 1) *What if no date column?* Use row order or a version number. 2) *Can you undo?* Only right after, so keep a copy.
**Common mistakes:** Not sorting first; ticking all columns so nothing is removed.

### Q29 ⭐⭐ 🟡 How do you extract a list of unique values in Excel 2016 or 2019, and how does it differ from Excel 365?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the version gap and the older workarounds?
**Say this in the interview:** "In 2016 and 2019 there is no UNIQUE function. I copy the column and use Remove Duplicates, or Advanced Filter with Unique records only, or a formula with INDEX, MATCH and COUNTIF. In 365 and 2021, one cell with UNIQUE does it and it updates itself."
**Explain simply:**
- `UNIQUE` is a *dynamic array* function: one formula that fills several cells (a spill) and refreshes automatically.
- Microsoft's page lists UNIQUE for Microsoft 365, Excel 2024 and 2021 (Microsoft Support, "UNIQUE function"); it does not list 2016 or 2019.
- The older routes are manual (static) or use a longer formula.
**Example:** List the distinct cities in an employee file.
**Sample sheet:** A1:A8 (City), results from C2.

| | A (City) |
|---|---|
| 2 | Hyderabad |
| 3 | Pune |
| 4 | Hyderabad |
| 5 | Chennai |
| 6 | Pune |
| 7 | Hyderabad |
| 8 | Mumbai |

**Formula / Steps:** Cell C1 holds the heading "Unique". C2 `=IFERROR(INDEX($A$2:$A$8,MATCH(0,INDEX(COUNTIF($C$1:C1,$A$2:$A$8),0),0)),"")`, fill down 6 rows. Or: Data > Sort & Filter > Advanced > Copy to another location > tick Unique records only. Or copy the column, then Data > Remove Duplicates.
**Alternative:** 365/2021: `=UNIQUE(A2:A8)` (not run here; expected Hyderabad, Pune, Chennai, Mumbai).
**Result:** Older formula run in LibreOffice: Hyderabad, Pune, Chennai, Mumbai, then blanks.
**Version note:** UNIQUE: Excel 365, 2024, 2021 (Microsoft Support). Excel 2016 and 2019 not listed there (consistent with my prior knowledge).
**Edge cases:** UNIQUE is case-insensitive; blanks appear as 0. The COUNTIF trick treats case the same way.
**Likely follow-ups:** 1) *Unique count?* `=COUNTA(UNIQUE(range))` in 365. 2) *Pivot table?* Row labels give distinct values too.
**Common mistakes:** Using UNIQUE in a file shared with Excel 2016 users (they see #NAME?); starting the formula's expanding range at the first data row.

### Q30 ⭐⭐ 🟡 How do you use Go To Special to select blanks, errors or constants, and why is it useful in cleaning?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know how to act on a whole category of cells at once?
**Say this in the interview:** "Go To Special selects cells by type: blanks, constants, formulas, errors. I select the blanks in a column, type a value like 'Unknown' and press Ctrl+Enter to fill them all. I select errors to review or clear them in one go."
**Explain simply:**
- Open it with Home > Editing > Find & Select > Go To Special (or F5 > Special, or Ctrl+G).
- *Blanks*: empty cells. *Constants*: typed values (tick Numbers, Text, Logicals, Errors to narrow). *Formulas*: cells with formulas (and what they return). *Visible cells only*: ignores hidden or filtered rows.
- Ctrl+Enter writes the same entry into every selected cell.
**Example:** In a 5,000-row employee list, 120 blank Department cells need "Not Assigned" before a pivot table.
**Sample sheet:**

| | A (Dept) | B (Value) |
|---|---|---|
| 1 | Dept | Value |
| 2 | HR | 10 |
| 3 | (blank) | `=1/0` |
| 4 | IT | |
| 5 | (blank) | |

**Formula / Steps:** 1) Select A2:A5. 2) Home > Find & Select > Go To Special > Blanks > OK. 3) Type `Not Assigned`, press Ctrl+Enter. For errors: select B2:B5 > Go To Special > Formulas > tick only Errors > OK > press Delete (or type 0 and Ctrl+Enter).
**Alternative:** Filter on (Blanks) and fill down; Find & Replace; Power Query Replace Values.
**Result:** Feature, not run here. By hand: A3 and A5 become "Not Assigned"; B3's #DIV/0! is selected and cleared. The count of blanks by formula, run in LibreOffice, `=COUNTBLANK(A2:A5)` = 2.
**Version note:** Available in all Excel versions (from memory, unverified). Google Sheets has no Go To Special.
**Edge cases:** If no cell matches, Excel says "No cells were found". Cells containing "" from a formula are not "Blanks". After the replacement, convert any formula results to values if needed.
**Likely follow-ups:** 1) *Fill blanks with the value above?* Q16 uses the same dialog with `=A2`. 2) *Why Visible cells only?* To copy a filtered list without hidden rows.
**Common mistakes:** Deleting rows after selecting blanks in a wide table; forgetting Ctrl+Enter (Enter fills only one cell).

### Q31 ⭐⭐ 🟡 A phone number column has entries like '+91 98765-43210', '09876543210' and '98765 43210'. How do you standardise them to ten digits?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you chain simple text functions and check the result?
**Say this in the interview:** "I remove spaces, hyphens and the plus sign with SUBSTITUTE, then take the last 10 characters with RIGHT, which drops +91 and a leading 0. Then I check that LEN is 10 and keep the column as Text so zeros are not lost."
**Explain simply:**
- `SUBSTITUTE(text,old,new)` swaps characters; nested three times it strips space, hyphen and plus.
- `RIGHT(text,10)` keeps the last ten characters, which is the mobile number in Indian formats.
- This assumes every real number has ten digits; shorter or longer ones must be flagged, not guessed.
**Example:** A candidate list from three recruiters in different formats, to be uploaded into an HR system.
**Sample sheet:**

| | A (raw) | B (clean) | C (10 digits?) |
|---|---|---|---|
| 2 | +91 98765-43210 | | |
| 3 | 09876543210 | | |
| 4 | 98765 43210 | | |
| 5 | 9876543210 (a real number) | | |

**Formula / Steps:** B2 `=RIGHT(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(A2," ",""),"-",""),"+",""),10)`; C2 `=LEN(B2)=10`. Copy > Paste Special > Values; format as Text.
**Alternative:** Find & Replace to remove the characters; or Power Query: Replace Values then Text.End.
**Result:** Run in LibreOffice: all four rows return `9876543210` and TRUE.
**Version note:** Works in every version and in Google Sheets.
**Edge cases:** Brackets, dots, and a leading "00" need more SUBSTITUTEs. Numbers shorter than 10 digits would pass through unchanged, so the LEN check matters. A number typed as a true number loses a leading zero (not a problem here).
**Likely follow-ups:** 1) *Why not a number format?* Formats only change display, not content. 2) *Landlines?* They have area codes; do not apply RIGHT blindly.
**Common mistakes:** Keeping the result as numbers; not validating length; assuming all numbers are Indian.

### Q32 ⭐⭐ 🟡 Remove Duplicates treats "HYD" and "hyd" as the same value. How do you find or remove duplicates that must match case exactly?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the default is case-insensitive and how to use EXACT?
**Say this in the interview:** "Remove Duplicates ignores case, so I use EXACT, which is case-sensitive, inside SUMPRODUCT to number each occurrence. Rows numbered 2 or more are true case-sensitive duplicates. I filter on them and delete only those."
**Explain simply:**
- `EXACT(a,b)` returns TRUE only if the two texts match including capital letters.
- `SUMPRODUCT(--EXACT($A$2:A2,A2))` counts how many times this exact spelling appeared so far.
- Excel's own page does not state the case rule (Microsoft Support, "Filter for unique values or remove duplicate values"); that Remove Duplicates and COUNTIF ignore case is from memory and as the question states.
**Example:** Employee codes "ab12" and "AB12" are different keys in a case-sensitive payroll system.
**Sample sheet:**

| | A (City) | B (Exact count) | C (COUNTIF) |
|---|---|---|---|
| 2 | HYD | | |
| 3 | hyd | | |
| 4 | Pune | | |
| 5 | HYD | | |
| 6 | Pune | | |

**Formula / Steps:** B2 `=SUMPRODUCT(--EXACT($A$2:A2,A2))`, fill down; filter B for values greater than 1 and delete those rows. For comparison C2 `=COUNTIF($A$2:A2,A2)`.
**Alternative:** Helper key and sort; or Power Query, where text comparison is case-sensitive by default (from memory, unverified) so Remove Duplicates there keeps both "HYD" and "hyd".
**Result:** Run in LibreOffice: Exact count 1, 1, 1, 2, 2 (rows 5 and 6 are real repeats); COUNTIF gives 1, 2, 1, 3, 2, showing it treats HYD and hyd as the same.
**Version note:** EXACT and SUMPRODUCT work in all versions.
**Edge cases:** Spaces still matter; TRIM first. Business-wise, decide whether case differences are real or typing noise (usually noise; then standardise with UPPER).
**Likely follow-ups:** 1) *Is COUNTIF case-sensitive?* No. 2) *Easier option?* Normalise with UPPER or PROPER and then use the normal Remove Duplicates.
**Common mistakes:** Assuming COUNTIF can detect case; deleting both rows.

### Q33 ⭐ 🟢 How do you remove duplicates in Google Sheets, and how does it differ from Excel?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know Sheets as well as Excel, since many teams use both?
**Say this in the interview:** "In Google Sheets I select the range and use Data > Data cleanup > Remove duplicates, choose the columns and tick the header option. It is nearly the same as Excel, but Sheets has the UNIQUE function in every version, so I can also build a live de-duplicated list."
**Explain simply:**
- Steps: select range > Data menu > Data cleanup > Remove duplicates > tick "Data has header row" > choose columns > Remove duplicates. A message reports how many rows were removed.
- The Google Docs Editors Help page could not be fetched (404 on the URL tried; a search returned only third-party tutorials). The tutorials agree on the steps and that the checked columns together decide a duplicate, but this is not an official source, so the details below are from memory, unverified.
- Differences from Excel: menu location (Data cleanup, not Data Tools); UNIQUE and also QUERY available without a version problem; Excel has Advanced Filter and Power Query, Sheets does not.
- Both tools keep the first occurrence and delete the rest (the Excel behaviour is from Microsoft Support; the Sheets one is from memory).
**Example:** A shared candidate tracker with repeated entries.
**Sample sheet:** Not meaningful; same logic as Q1 and Q8.
**Formula / Steps:** Click-path above. Live version: `=UNIQUE(A2:C100)` in a new area.
**Alternative:** `=UNIQUE(range)`; highlight duplicates first with conditional formatting (Format > Conditional formatting > Custom formula `=COUNTIF($A$2:$A$100,A2)>1`).
**Result:** Not run here (no Sheets access).
**Version note:** Whether Remove duplicates in Sheets distinguishes upper and lower case: not verified; test on two sample rows before relying on it.
**Edge cases:** Trailing spaces and text/number mismatches block matching in both tools.
**Likely follow-ups:** 1) *Does UNIQUE change the source?* No. 2) *Can you undo?* Yes, Ctrl+Z, and version history.
**Common mistakes:** Forgetting the header checkbox so the header is treated as data.

### Q34 ⭐ 🟢 What is the difference between SUBSTITUTE and REPLACE when cleaning text?
**Asked at:** commonly asked (no company-specific report found); SUBSTITUTE appears in a fetched Analytics Vidhya Excel question list.
**What the interviewer is checking:** Do you know one works by matching text and the other by position?
**Say this in the interview:** "SUBSTITUTE replaces specific text wherever it appears, like swapping hyphens for nothing. REPLACE replaces characters at a fixed position and length, like changing the first three characters of a code. I use SUBSTITUTE when I know what to remove and REPLACE when I know where."
**Explain simply:**
- `SUBSTITUTE(text, old_text, new_text, [instance_num])`: all matches, or only the Nth match if you give instance_num.
- `REPLACE(old_text, start_num, num_chars, new_text)`: starts at a position, replaces that many characters. Using 0 characters inserts text.
- Both return new text, leaving the original unchanged. SUBSTITUTE matches text and is case-sensitive; REPLACE works by position, so case does not apply to it.
**Example:** Employee code EMP-001-A: remove all hyphens (SUBSTITUTE), or change the prefix EMP to STF (REPLACE).
**Sample sheet:**

| | A |
|---|---|
| 2 | EMP-001-A |
| 3 | Priya  Sharma (two spaces) |
| 4 | EMP001 |

**Formula / Steps:** `=SUBSTITUTE(A2,"-","")`; `=SUBSTITUTE(A2,"-","/",2)`; `=REPLACE(A2,1,3,"STF")`; `=REPLACE(A2,4,1,"_")`; `=SUBSTITUTE(A3,"  "," ")`; `=REPLACE(A4,4,0,"-")`.
**Alternative:** Find & Replace (Ctrl+H) for one-off, non-formula fixes; Power Query Replace Values.
**Result:** Run in LibreOffice: EMP001A; EMP-001/A (only the 2nd hyphen); STF-001-A; EMP_001-A; "Priya Sharma"; EMP-001.
**Version note:** Both exist in every Excel version and in Google Sheets.
**Edge cases:** SUBSTITUTE without a match returns the text unchanged; REPLACE with a start beyond the length appends (`REPLACE("EMP",10,0,"X")` gave `EMPX` in LibreOffice; Excel not checked). Only SUBSTITUTE is case-sensitive. They return text, so a number-like result needs VALUE if you want numbers.
**Likely follow-ups:** 1) *Remove all of several characters?* Nest SUBSTITUTE (see Q31). 2) *Why not TRIM for double spaces?* TRIM already does it, except for non-breaking spaces.
**Common mistakes:** Mixing up the arguments (REPLACE needs positions); using REPLACE when the position varies.

### Q35 ⭐ 🟢 What does the VALUE function do, and how is it different from multiplying the cell by 1?
**Asked at:** commonly asked (no company-specific report found); VALUE appears in prep-blog cleaning lists (Analytics Vidhya, Jan 2024).
**What the interviewer is checking:** Do you know how to turn text that looks like a number into a real number, and that there is more than one way?
**Say this in the interview:** "VALUE converts a text string that looks like a number into a real number. Multiplying by 1 gives the same answer in almost every case. I use whichever is clearer to the reader, and I always check the result with SUM or ISNUMBER."
**Explain simply:**
- Text-number = digits Excel stores as words, so it will not add up (SUM ignores it).
- `VALUE(text)` converts it. `A2*1`, `--A2` (two minus signs, "negative of negative") and `A2+0` do the same through arithmetic.
- Microsoft says VALUE is mainly kept so spreadsheets from other programs work; Excel often converts text on its own (Microsoft Support, "VALUE function").
- Real difference: VALUE reads as plain English and works on a text argument only; `*1` is shorter and also works on dates or TRUE/FALSE (TRUE*1 = 1).
**Example:** A payroll export has salaries as text. HR cannot total them until they are converted.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Text | VALUE | *1 |
| 2 | 42000 (text) | | |
| 3 | 38500 (text) | | |
| 4 | ` 51000 ` (spaces around) | | |
| 5 | N/A | | |

**Formula / Steps:** B2 `=VALUE(A2)` and C2 `=A2*1`, filled down to row 5. Check: `=SUM(A2:A4)` and `=SUM(B2:B4)`.
**Alternative:** `=--A2`, or Data > Text to Columns > Finish, or Paste Special > Multiply (see Q43).
**Result:** Run in LibreOffice: B2:B4 = 42000, 38500, 51000; C2:C4 = same; B5 and C5 = `#VALUE!`. `SUM(A2:A4)` = 0 but `SUM(B2:B4)` = 131500.
**Version note:** VALUE is listed for Excel 2016, 2019, 2021, 2024 and 365 (Microsoft Support, "VALUE function"). Google Sheets also has VALUE (from memory, unverified).
**Edge cases:** Unreadable text gives #VALUE! in both. A truly empty cell*1 gives 0 (run here); `VALUE("")` returned #VALUE! in LibreOffice here. Microsoft's VALUE page says text not in a recognised format returns #VALUE! but does not mention empty text directly, so Excel's result for `""` is unconfirmed. Reading "1,250" or dates depends on regional settings.
**Likely follow-ups:** 1) *Text with a non-breaking space?* Clean with SUBSTITUTE(A2,CHAR(160),"") first. 2) *Why not just reformat to Number?* Changing the format does not convert text already stored.
**Common mistakes:** Changing the cell format and expecting the text to turn numeric; leaving the converted column as formulas and then deleting the source column.

### Q36 ⭐ 🟢 How do you remove leading zeros, or add them back, in a column such as employee codes?
**Asked at:** commonly asked (no company-specific report found); employee-code cleaning is standard MIS practice.
**What the interviewer is checking:** Do you understand that Excel drops leading zeros from numbers and that text vs number decides what you see?
**Say this in the interview:** "To remove leading zeros I convert the text to a number with VALUE. To add them back I use TEXT with a pattern like 00000, or RIGHT with a string of zeros. The result of TEXT is text, so I keep it for display and IDs, not for maths."
**Explain simply:**
- A **number** has no leading zeros; 00123 and 123 are the same number. A **text** keeps every character.
- Removing: convert text to number (`VALUE`, `*1`).
- Adding: `TEXT(B2,"00000")` forces five digits. The pattern's zeros mean "show a digit here, even if it is 0".
- Alternative display-only trick: Format Cells > Custom > `00000` keeps the value a number but only changes how it looks.
**Example:** The payroll system wants employee codes as five digits (00123), but the exported file shows 123.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Code (text) | No zeros | 5 digits |
| 2 | 00123 | | |
| 3 | 007 | | |
| 4 | 0450 | | |
| 5 | 0098 | | |

**Formula / Steps:** B2 `=VALUE(A2)`; C2 `=TEXT(B2,"00000")`. Fill down.
**Alternative:** `=RIGHT("00000"&B2,5)` to add zeros; `=--A2` to remove them; custom number format `00000` for display only.
**Result:** Run in LibreOffice: B = 123, 7, 450, 98; C = 00123, 00007, 00450, 00098 (all text; `ISNUMBER(C2)` = FALSE).
**Version note:** VALUE, TEXT and RIGHT work in every Excel version and Google Sheets (from memory, unverified).
**Edge cases:** Codes longer than the pattern (e.g. 1234567 with "00000") are not cut by TEXT. If the code contains letters (EMP007), VALUE gives #VALUE!; use MID/SUBSTITUTE. Lookups fail if one table has text 00123 and the other number 123.
**Likely follow-ups:** 1) *Why does my VLOOKUP fail on codes?* One side is text, the other number. 2) *Custom format vs TEXT?* Custom format changes only the look; TEXT changes the stored value to text.
**Common mistakes:** Typing the zeros into a General cell (Excel strips them); trying to sum a TEXT result; forgetting to paste values before deleting the source.

### Q37 ⭐ 🟢 How do you remove unwanted characters such as '#', '-' or brackets from a column of text?
**Asked at:** commonly asked (no company-specific report found); SUBSTITUTE is named in prep-blog cleaning lists.
**What the interviewer is checking:** Can you replace characters in bulk, by formula and by feature?
**Say this in the interview:** "For a one-time fix I use Find and Replace and replace the character with nothing. If it must be repeatable I use SUBSTITUTE, nesting one per character, and I paste the result as values."
**Explain simply:**
- `SUBSTITUTE(text, old, new)` replaces every `old` with `new`. Using `""` (empty text) as `new` deletes it.
- One SUBSTITUTE handles one character, so for several characters you **nest** them (put one inside another).
- Find and Replace (Ctrl+H) does the same to the cells themselves, with no formula. Wildcards: `~` is needed before `*`, `?` and `~`.
**Example:** A new-hire list has codes like `#EMP-101` and departments like `(HR)-Pune`; the HRIS wants `EMP101` and `HRPune`.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | Raw | Clean |
| 2 | #EMP-101 | |
| 3 | (HR)-Pune | |
| 4 | Sales# | |
| 5 | [Ops] 22 | |

**Formula / Steps:** B2 `=SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(A2,"#",""),"-",""),"(",""),")",""),"[",""),"]","")`. Fill down, then copy > Paste Special > Values.
**Alternative:** Select the column > Home > Find & Select > Replace (Ctrl+H) > Find what `#` > Replace with (empty) > Replace All, repeated per character. In Power Query: Transform > Replace Values (not run here).
**Result:** Run in LibreOffice: EMP101, HRPune, Sales, Ops 22.
**Version note:** SUBSTITUTE works in all Excel versions and Google Sheets (from memory, unverified). Google Sheets also has REGEXREPLACE; Excel does not have a regex function (from memory, unverified).
**Edge cases:** SUBSTITUTE is case-sensitive. Removing `-` from a phone or negative number changes meaning. A space left behind (as in "Ops 22") may need TRIM.
**Likely follow-ups:** 1) *Many characters to remove?* Keep a list and use Power Query, or a long nest. 2) *Replace only the first one?* Use the 4th argument, instance_num.
**Common mistakes:** Using Replace All on the whole sheet and damaging other columns; forgetting to paste values; assuming SUBSTITUTE is not case-sensitive.

### Q38 ⭐ 🟢 A cell shows 1.2E+15 for a long ID number. What happened, and how do you prevent it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know Excel's number limits and that IDs should be text?
**Say this in the interview:** "Excel treated the ID as a number and showed it in scientific notation, 1.2E+15 meaning 1.2 times ten to the power 15. Worse, Excel keeps only 15 significant digits, so digits after the 15th become zeros. IDs are labels, not quantities, so I set the column to Text before pasting or importing."
**Explain simply:**
- **Scientific notation** = a short way to show very large numbers. A column that is too narrow triggers it.
- The bigger risk is **precision**: Microsoft's "Excel specifications and limits" page lists number precision as 15 digits, so Excel stores 15 digits exactly; a 16-digit ID 1234567890123456 becomes 1234567890123450 once it is a number. That change cannot be undone.
- Widening the column only fixes the display for up to 15 digits.
- Rule: if you never add or average it, it is text (Aadhaar-style numbers, bank accounts, phone numbers, employee codes).
**Example:** A 16-digit card or account number pasted from a payroll CSV shows 1.23457E+15; two different accounts could look identical after truncation.
**Sample sheet:**

| | A |
|---|---|
| 1 | AccountNo |
| 2 | 1234567890123456 |
| 3 | 1234567890123457 |

**Formula / Steps (prevent):** 1. Select the column > Home > Number group > Number Format box > **Text** (before pasting). 2. Or type an apostrophe first (`'1234567890123456`). 3. For a CSV: Data > From Text/CSV > Transform Data > set the column type to Text, then Close & Load.
**Alternative:** Format Cells > Custom `0` only fixes display up to 15 digits; it cannot restore lost digits.
**Result:** Not reproduced here: LibreOffice kept all 16 digits, so it does not show Excel's 15-digit behaviour. Run here only: `LEN(A2)` on the text version returns 16. Excel's truncation and the COUNTIF mismatch (COUNTIF treats long digit text as numbers, so the two IDs above can be counted as equal) are from memory, unverified.
**Version note:** The 15-digit precision is on Microsoft's "Excel specifications and limits" page; that it applies to every version is from memory, unverified. Google Sheets handles long digit strings differently (from memory, unverified).
**Edge cases:** If the data is already corrupted, you must get the original file again. Text-formatted IDs show a green triangle; ignore it.
**Likely follow-ups:** 1) *Can I fix it after the fact?* No, lost digits are gone. 2) *How to test uniqueness of long IDs?* Use SUMPRODUCT with `=` comparison, not COUNTIF.
**Common mistakes:** Widening the column and thinking it is fixed; formatting as Text after pasting (already converted); saving the CSV from Excel after opening it.

### Q39 ⭐ 🟡 How do you remove duplicates in Excel 365 using the UNIQUE function, and what are the pros and cons compared with the Remove Duplicates button?
**Asked at:** commonly asked (no company-specific report found); UNIQUE appears in fresher India lists (prep sites, snippet level).
**What the interviewer is checking:** Do you know the modern formula and the trade-off between a live formula and a one-off button?
**Say this in the interview:** "UNIQUE returns the list without repeats into a new area and leaves the source untouched. It updates when the data changes. The button deletes rows permanently and is one-time, but works in every version."
**Explain simply:**
- A **spill** is a formula that fills several cells by itself from one cell.
- `UNIQUE(array, [by_col], [exactly_once])`: by default it keeps the first of each repeated item. `exactly_once` TRUE returns only items that appear once.
- Pros: non-destructive, live, works on several columns (whole rows compared).
- Cons: 365/2021/2024 only; spill area must be clear (#SPILL!); the result is a formula, not editable values; ignores case.
- Remove Duplicates button: destructive, one-time, all versions (Microsoft Support, "Filter for unique values or remove duplicate values").
**Example:** Attendance export has E101, E102, E101, E103, E102 and HR needs the distinct employees.
**Sample sheet:**

| | A |
|---|---|
| 1 | EmpID |
| 2 | E101 |
| 3 | E102 |
| 4 | E101 |
| 5 | E103 |
| 6 | E102 |

**Formula / Steps:** In C2 `=UNIQUE(A2:A6)`. For whole rows: `=UNIQUE(A2:C100)`.
**Alternative:** Data > Remove Duplicates (copy the sheet first), or a COUNTIF flag column (see Q27).
**Result:** Not run here (LibreOffice 24.2 has no UNIQUE). Expected, confirmed with pandas `unique()`: E101, E102, E103.
**Version note:** UNIQUE applies to Excel for Microsoft 365, 2024 and 2021; Microsoft's page lists no Excel 2019 or earlier (Microsoft Support, "UNIQUE function"). Google Sheets has UNIQUE too (from memory, unverified).
**Edge cases:** Blank cells appear as 0 in the result. Case differences are treated as the same. Closed linked workbooks give #REF!.
**Likely follow-ups:** 1) *Sort too?* `=SORT(UNIQUE(A2:A6))`. 2) *Need static values?* Copy > Paste Special > Values.
**Common mistakes:** Typing something in the spill range; expecting UNIQUE to change the original list.

### Q40 ⭐ 🟡 How do you find duplicates based on a combination of two or more columns, such as employee ID plus month?
**Asked at:** commonly asked (no company-specific report found); a typical MIS scenario.
**What the interviewer is checking:** Can you define a duplicate on a key made of several columns?
**Say this in the interview:** "I use COUNTIFS with one pair of range and criteria per column. If the count for that ID and month is more than one, it is a duplicate. I use an expanding range if I want to flag only the second and later copies."
**Explain simply:**
- A **composite key** = two or more columns that together identify a record (an employee appears once per month).
- COUNTIFS counts rows where *all* conditions match.
- Fixed range `$A$2:$A$8` flags every copy; expanding range `$A$2:A2` flags only repeats after the first.
**Example:** Payroll must have one row per employee per month; two rows for E101 in Jan means double payment.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | EmpID | Month |
| 2 | E101 | Jan |
| 3 | E102 | Jan |
| 4 | E101 | Feb |
| 5 | E101 | Jan |
| 6 | E103 | Jan |
| 7 | E102 | Feb |
| 8 | E102 | Jan |

**Formula / Steps:** C2 `=COUNTIFS($A$2:$A$8,A2,$B$2:$B$8,B2)>1` (all copies); D2 `=COUNTIFS($A$2:A2,A2,$B$2:B2,B2)>1` (repeats only). Fill down.
**Alternative:** Helper key `=A2&"|"&B2` then `=COUNTIF($E$2:$E$8,E2)`; or Remove Duplicates with both columns ticked; or Conditional Formatting > Use a formula.
**Result:** Run in LibreOffice: C2:C8 = TRUE, TRUE, FALSE, TRUE, FALSE, FALSE, TRUE (4 rows involved); D flags only rows 5 and 8; `=SUMPRODUCT(1/COUNTIFS(A2:A8,A2:A8,B2:B8,B2:B8))` = 5 distinct combinations.
**Version note:** COUNTIFS works in Excel 2007 onwards and Google Sheets (from memory, unverified).
**Edge cases:** Use a delimiter in helper keys (E1|01 vs E10|1). Blanks match blanks. Trailing spaces make duplicates invisible (clean first).
**Likely follow-ups:** 1) *How many distinct pairs?* The SUMPRODUCT above. 2) *Delete them?* Filter on the flag, or Remove Duplicates on both columns.
**Common mistakes:** Checking only the ID column; mixing absolute and relative references.

### Q41 ⭐ 🟡 How do you use TEXTSPLIT and TEXTBEFORE or TEXTAFTER to clean text, and which Excel versions have them?
**Asked at:** commonly asked (no company-specific report found); a newer-function differentiator.
**What the interviewer is checking:** Do you know the modern split functions and their version limits?
**Say this in the interview:** "TEXTBEFORE and TEXTAFTER pull out the text before or after a delimiter, and TEXTSPLIT splits into many cells at once. They only exist in Excel 365 and 2024, so for older versions I use LEFT, MID and FIND."
**Explain simply:**
- **Delimiter** = the separating character(s), here " - ".
- `TEXTBEFORE(text, delimiter, [instance_num], ...)` and `TEXTAFTER(...)`: instance_num picks which occurrence; `if_not_found` avoids #N/A.
- `TEXTSPLIT(text, col_delimiter, [row_delimiter])` spills all parts across cells.
- Wrap in TRIM if spaces remain.
**Example:** `EMP001 - Priya Sharma - Hyderabad` split into ID, name and city.
**Sample sheet:**

| | A |
|---|---|
| 1 | Record |
| 2 | EMP001 - Priya Sharma - Hyderabad |
| 3 | EMP002 - Ravi Kumar - Pune |
| 4 | EMP003 - Meena Iyer - Bengaluru |

**Formula / Steps:** B2 `=TEXTBEFORE(A2," - ")`; C2 `=TEXTBEFORE(TEXTAFTER(A2," - ")," - ")`; D2 `=TEXTAFTER(A2," - ",-1)`. Or one cell: `=TEXTSPLIT(A2," - ")`.
**Alternative (all versions):** B2 `=LEFT(A2,FIND(" - ",A2)-1)`; C2 `=MID(A2,FIND(" - ",A2)+3,FIND(" - ",A2,FIND(" - ",A2)+3)-FIND(" - ",A2)-3)`; D2 `=MID(A2,FIND(" - ",A2,FIND(" - ",A2)+3)+3,99)`. Or Text to Columns with " - " as the "Other" delimiter (one character only; replace first if needed).
**Result:** TEXTSPLIT family not run here. The all-versions formulas were run in LibreOffice: EMP001 / Priya Sharma / Hyderabad, EMP002 / Ravi Kumar / Pune, EMP003 / Meena Iyer / Bengaluru; the TEXTBEFORE/TEXTAFTER results are the same by hand.
**Version note:** TEXTBEFORE's page lists Excel for Microsoft 365 and Excel 2024 only (Microsoft Support, "TEXTBEFORE function"); not 2016, 2019 or 2021. TEXTSPLIT and TEXTAFTER are the same family (TEXTSPLIT availability from an earlier Microsoft Support fetch noted elsewhere in this book; TEXTAFTER not fetched here, unverified).
**Edge cases:** Delimiter not found gives #N/A; text with the delimiter inside a name breaks the position count.
**Likely follow-ups:** 1) *Older Excel?* LEFT/MID/FIND or Power Query. 2) *Spill blocked?* Clear the cells to the right.
**Common mistakes:** Using it in 2019 and getting #NAME?; forgetting extra spaces.

### Q42 ⭐ 🟡 How do you find near-duplicates, such as 'Infosys Ltd' and 'Infosys Limited', in a company list?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know exact-match tools miss near-duplicates, and can you standardise first?
**Say this in the interview:** "Remove Duplicates only catches exact matches. I first standardise: lowercase, drop dots and suffixes like Ltd or Limited, trim spaces, in a helper column. Then I count matches on the cleaned key. For harder cases I use Power Query's fuzzy matching."
**Explain simply:**
- **Standardising** = making all spellings follow one pattern before comparing.
- **Fuzzy matching** = matching by similarity score, not exact text; it can be wrong, so a human should check.
- Abbreviations (TCS vs Tata Consultancy Services) need a lookup table of aliases.
**Example:** A candidate-source list has "Infosys Ltd", "Infosys Limited" and "INFOSYS LTD." counted as three employers.
**Sample sheet:**

| | A |
|---|---|
| 1 | Company |
| 2 | Infosys Ltd |
| 3 | Infosys Limited |
| 4 | INFOSYS LTD. |
| 5 | Wipro Ltd |
| 6 | wipro limited |
| 7 | Tata Consultancy Services |
| 8 | TCS |

**Formula / Steps:** B2 `=TRIM(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(LOWER(A2),".",""),"limited",""),"ltd",""))`; C2 `=COUNTIF($B$2:$B$8,B2)`. Filter C > 1.
**Alternative:** Power Query: Home > Merge Queries > tick "Use fuzzy matching" (not run here); Microsoft's Power Query page says fuzzy merge is in Microsoft 365 but not 2019 perpetual (Microsoft Support, "Power Query data sources in Excel versions").
**Result:** Run in LibreOffice: keys infosys, infosys, infosys, wipro, wipro, tata consultancy services, tcs; counts 3, 3, 3, 2, 2, 1, 1. TCS and Tata Consultancy Services are not matched without an alias table.
**Version note:** The formula works in all versions. Fuzzy merge: 365 only per above.
**Edge cases:** SUBSTITUTE "ltd" also hits names containing "ltd" inside a word (e.g. "Altdorf"); use a pattern with spaces for care.
**Likely follow-ups:** 1) *How sure are fuzzy matches?* Check the similarity score. 2) *Alias table?* Use VLOOKUP to a master company list.
**Common mistakes:** Trusting fuzzy matches blindly; deleting without review.

### Q43 ⭐ 🟡 How do you convert a column of numbers stored as text when green triangle warnings appear on the cells?
**Asked at:** commonly asked (no company-specific report found); Text-as-number is in prep lists (Analytics Vidhya, Jan 2024).
**What the interviewer is checking:** Can you use the quick fix, and know what to do when it does not work?
**Say this in the interview:** "The green triangle says 'Number Stored as Text'. I select the cells, click the warning icon and choose Convert to Number. If there are hidden characters I clean them with TRIM and SUBSTITUTE then VALUE, and I confirm with a SUM."
**Explain simply:**
- Green triangle = Excel's error-check flag.
- The fix works in place on the selected range.
- If no triangle appears (apostrophe or non-breaking space), use formulas.
**Example:** Salary export where SUM returns 0.
**Sample sheet:**

| | A |
|---|---|
| 1 | Salary (text) |
| 2 | 42000 |
| 3 | 38500 |
| 4 | `51000 ` (trailing space) |
| 5 | `47000` + non-breaking space |
| 6 | 39000 |

**Formula / Steps:** 1. Select the cells. 2. Click the yellow warning icon beside them. 3. Choose **Convert to Number**. Formula route: B2 `=VALUE(TRIM(SUBSTITUTE(A2,CHAR(160)," ")))`.
**Alternative:** Copy a blank cell > select data > Home > Paste > Paste Special > Add (or Multiply by 1); or Data > Text to Columns > Finish.
**Result:** Run in LibreOffice: B2:B6 = 42000, 38500, 51000, 47000, 39000; `SUM(A2:A6)` = 0, `SUM(B2:B6)` = 217500. Caveat: LibreOffice's `CHAR(160)` is not a non-breaking space, so row 5 only converted because LibreOffice's VALUE tolerates it; a re-run with `UNICHAR(160)` also gave 47000. Excel may return #VALUE! for `VALUE(A5)` without the SUBSTITUTE (from memory, unverified).
**Version note:** The warning-icon route exists in all desktop versions (from memory, unverified).
**Edge cases:** Turn-off of error checking hides the triangles; text with currency symbols or commas depends on regional settings.
**Likely follow-ups:** 1) *No triangle?* Cells formatted as Text hide it; check ISNUMBER. 2) *Many columns?* Power Query change type.
**Common mistakes:** Changing the format to Number only, with no re-entry; ignoring hidden spaces.

### Q44 ⭐ 🟡 Which cleaning steps would you do in Power Query instead of formulas, and why?
**Asked at:** commonly asked (no company-specific report found); Power Query appears in prep-blog lists (Analytics Vidhya, Jan 2024).
**What the interviewer is checking:** Do you know when a repeatable, no-formula tool is better?
**Say this in the interview:** "Anything repetitive or large: trimming, changing types, splitting columns, removing duplicates, merging files, unpivoting. Power Query records each step and replays it on Refresh, so next month's file takes one click."
**Explain simply:**
- **Power Query** = Excel's built-in data-cleaning tool (Data tab > Get & Transform). It records steps like a recipe.
- Good for: Trim/Clean, Replace Values, Split Column, Change Type, Remove Duplicates, Remove Blank Rows, Fill Down, Unpivot, merging a folder of files.
- Stay with formulas for: quick one-off fixes, results that must update live next to other formulas, or small sheets.
- Source data stays untouched.
**Example:** HR receives 12 monthly attendance files with blank rows and spaces; Power Query appends and cleans them in one query. For a small test, a 5-row employee list has one blank row, one exact duplicate and salaries typed as text.
**Sample sheet:**

| | A (Name) | B (Salary, text) | C (Dept) |
|---|---|---|---|
| 1 | Name | Salary | Dept |
| 2 | `  Priya Sharma ` | 42000 | HR |
| 3 | Ravi Kumar | `38500 ` | Finance |
| 4 | `  Priya Sharma ` | 42000 | HR |
| 5 | (blank row) | | |
| 6 | `Meena  Iyer` | 51000 | IT |

**Formula / Steps:** 1. Data > Get Data > From File > From Workbook / From Text/CSV. 2. Transform Data. 3. Apply steps: Transform > Format > Trim; Home > Remove Rows > Remove Duplicates; Transform > Data Type. 4. Home > Close & Load.
**Alternative:** Formulas (TRIM, SUBSTITUTE, VALUE) with paste-as-values for small jobs.
**Result:** Power Query itself is not run here. The same steps reproduced in pandas (strip spaces, drop the empty row, convert salary to number, drop exact duplicates): 5 rows in, 4 after dropping the blank row, 3 after de-duplication (Priya Sharma 42000 HR; Ravi Kumar 38500 Finance; Meena Iyer 51000 IT); salary total 131,500. Note: Power Query's Trim removes only leading and trailing spaces, so `Meena  Iyer` keeps its double space (unlike Excel's TRIM function), which is from memory, unverified; check it before relying on it.
**Version note:** Power Query is available in "all Excel 2016 or later Windows stand alone versions"; some features (fuzzy merge) are 365 only (Microsoft Support, "Power Query data sources in Excel versions"; that page is cited here from the original writing and was not re-fetched in review). Not run here.
**Edge cases:** Column names change in a new file and break steps; case matters in Replace Values; Power Query's Trim leaves inner double spaces; a text-to-number step errors on cells such as "N/A" (they show as Error in that column, to be handled with Replace Errors).
**Likely follow-ups:** 1) *Formulas faster?* Power Query handles big data better. 2) *Does it change the raw file?* No. 3) *When do you still use formulas?* Small one-offs or values that must recalculate beside other formulas.
**Common mistakes:** Hard-coding file paths; forgetting to refresh; doing steps in the wrong order (change type before trimming, so "38500 " errors).

### Q45 ⭐ 🟡 How do you clean data that arrives every month in the same messy format, so that you do not repeat the manual steps?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you automate repeatable work and keep it reliable?
**Say this in the interview:** "I build the cleaning once in Power Query, save it, and each month I drop in the new file and click Refresh All. If Power Query is not available, I use a recorded macro or a template workbook with formulas."
**Explain simply:**
- A query is a saved list of steps, so nothing is retyped.
- Use **From Folder** so new monthly files are picked up automatically.
- Keep a checks sheet (row counts, blanks) next to it (see Q47).
**Example:** Monthly payroll CSV with extra spaces, text numbers and blank rows becomes a clean table in seconds. Test case: January and February attendance files (3 employees each) have spaces in IDs and one missing day count.
**Sample sheet:** Folder `Attendance` holding two files.

| | Jan.csv: A (EmpID) | B (Days) | Feb.csv: A (EmpID) | B (Days) |
|---|---|---|---|---|
| 2 | E101 | 22 | `E101 ` | 21 |
| 3 | E102 | 20 | E102 | (blank) |
| 4 | `  E103` | 18 | E103 | 19 |

**Formula / Steps:** 1. Put each month's file in one folder. 2. Data > Get Data > From File > From Folder. 3. Combine > Combine & Transform Data. 4. Apply Trim, Change Type, Remove Duplicates. 5. Close & Load to a table. 6. Next month: save the file in the folder, then Data > Refresh All.
**Alternative:** Record a macro (VBA, Excel's built-in automation) via View > Macros > Record Macro; or a template with cleaning formulas.
**Result:** Not run here (Power Query). Pandas reproduction of the combine-and-clean steps: 6 rows (3 January + 3 February), IDs trimmed to E101, E102, E103, Days converted to numbers with 1 missing value, Days total 100. After a refresh with a March file the table should show 9 rows; that count is the check.
**Version note:** Power Query is built into Excel 2016 and later Windows versions (Microsoft Support, "Power Query data sources in Excel versions"; cited from the original writing, not re-fetched in review). From Folder and Combine & Transform are from memory, unverified for each version. Not run here.
**Edge cases:** If the vendor adds, renames or reorders columns the query errors; check the first step after a refresh. A file with a different header row, a locked or open file, or a moved folder also breaks the refresh.
**Likely follow-ups:** 1) *What breaks it?* Column renames. 2) *Share it?* Send the workbook, not just the output. 3) *No Power Query (older Mac, Google Sheets)?* Use a template with formulas, or in Sheets a saved set of formulas and UNIQUE/QUERY (from memory, unverified).
**Common mistakes:** Cleaning the same way by hand each month; no row-count check after refresh; testing the query only on one clean month.

### Q46 ⭐ 🟡 How do you standardise text with Flash Fill, for example turning 'priya sharma' into 'Sharma, Priya'?
**Asked at:** commonly asked (no company-specific report found); Flash Fill is in nearly every prep list.
**What the interviewer is checking:** Can you use Flash Fill and know its limits?
**Say this in the interview:** "I type the first result in the next column, say 'Sharma, Priya', then press Ctrl+E. Excel spots the pattern and fills the rest. I check the preview and a few rows, because it is a pattern guess, not a rule."
**Explain simply:**
- Flash Fill = Excel learns a pattern from your example(s).
- Steps: type the example, go to the next cell, Ctrl+E or Data > Flash Fill (Microsoft Support, "Using Flash Fill in Excel").
- Results are static values; they do not update if the source changes.
- Middle names, odd spacing and mixed cases can confuse it. Give a second or third example.
**Example:** Candidate names from a form in lower case need to be "Surname, Firstname".
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | Name | Standard |
| 2 | priya sharma | Sharma, Priya (typed) |
| 3 | RAVI KUMAR | |
| 4 | meena  iyer | |

**Formula / Steps:** B2: type `Sharma, Priya`. Click B3 and press Ctrl+E.
**Alternative:** `=PROPER(TRIM(MID(TRIM(A2),FIND(" ",TRIM(A2))+1,99)))&", "&PROPER(LEFT(TRIM(A2),FIND(" ",TRIM(A2))-1))`.
**Result:** Flash Fill not run here. Formula run in LibreOffice: Sharma, Priya / Kumar, Ravi / Iyer, Meena.
**Version note:** Flash Fill is in Excel 2013 and later (earlier Microsoft Support fetch lists 2016 to 365). Google Sheets has "Autofill suggestions" (from memory, unverified).
**Edge cases:** Three-word names; blank rows.
**Likely follow-ups:** 1) *Formula vs Flash Fill?* Formula updates. 2) *It filled wrongly?* Add more examples.
**Common mistakes:** Not checking outputs; expecting live updates.

### Q47 ⭐ 🟡 How do you check data quality after cleaning, so you can tell your manager the data is reliable?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you verify, not assume?
**Say this in the interview:** "I run a short checklist: row counts match the source, no unexpected blanks, no duplicate keys, numbers really are numbers, and minimum, maximum and totals look sensible. I keep the results on a checks sheet and mention any exceptions."
**Explain simply:**
- Reconcile: row count and total before vs after.
- Completeness: blanks in key columns.
- Uniqueness: duplicate IDs.
- Validity: text in number columns, negative or impossible values.
**Example:** Salary column after cleaning: 7 employee rows should be checked before the file goes to the payroll manager. The checks below should flag the blank, the text "abc", the repeated E101 row and the negative salary.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | EmpID | Salary |
| 2 | E101 | 42000 |
| 3 | E102 | (blank) |
| 4 | E103 | 38500 |
| 5 | E101 | 42000 |
| 6 | E104 | abc |
| 7 | E105 | 47000 |
| 8 | E106 | -500 |

**Formula / Steps:** Rows `=COUNTA(A2:A8)`; blanks `=COUNTBLANK(B2:B8)`; text `=SUMPRODUCT(--ISTEXT(B2:B8))`; duplicate rows `=SUMPRODUCT(--(COUNTIF(A2:A8,A2:A8)>1))`; `=MIN(B2:B8)`, `=MAX(B2:B8)`; negatives `=COUNTIF(B2:B8,"<0")`.
**Alternative:** Power Query: Home > Keep Rows / View > Column Quality, Column Distribution and Column Profile.
**Result:** Run in LibreOffice (cells D1:D7 in order): rows 7, blanks 1, text cells 1, duplicate rows 2, min -500, max 47000, negatives 1.
**Version note:** All formulas work in every version and Google Sheets (from memory, unverified); Column Quality/Profile are Power Query features (not run here).
**Edge cases:** MIN/MAX ignore text; COUNTBLANK counts empty text from formulas but not a cell holding a space; the duplicate check shows 2 *rows* (E101 twice), not 1 extra copy; a total can look right while two errors cancel out, so also compare the row count to the source. "Reliable" means checked against stated rules, so tell the manager which rules you used and which rows are exceptions.
**Likely follow-ups:** 1) *What else?* Compare totals to the payroll system. 2) *Rules at entry?* Data Validation. 3) *What do you report?* Counts checked, exceptions found, how each was handled, and any open questions to the data owner.
**Common mistakes:** Only eyeballing; no before/after counts; fixing exceptions silently without telling the owner.

### Q48 ⭐ 🔴 How do you extract the numbers from a mixed text string such as 'Invoice-4581-Q3' without Power Query?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you pick the right pattern: position-based or all-digits?
**Say this in the interview:** "First I clarify: do you want the invoice number 4581, or every digit, which would be 45813 because Q3 has a 3? If the format is fixed I take the part between the hyphens with MID and FIND. For all digits I use TEXTJOIN with an array formula."
**Explain simply:**
- Premise note: "the numbers" is ambiguous, so I show both.
- Delimiter version relies on a consistent pattern.
- All-digits version tests each character with `ISNUMBER(--MID(...))` and joins digits.
**Example:** Invoice reference codes in an expense list.
**Sample sheet:**

| | A |
|---|---|
| 1 | Ref |
| 2 | Invoice-4581-Q3 |
| 3 | Invoice-77-Q1 |
| 4 | INV-120045-Q4 |

**Formula / Steps:** Between hyphens: B2 `=MID(A2,FIND("-",A2)+1,FIND("-",A2,FIND("-",A2)+1)-FIND("-",A2)-1)`. All digits (array formula, Ctrl+Shift+Enter in older versions): C2 `=TEXTJOIN("",TRUE,IF(ISNUMBER(--MID(A2,ROW($1:$30),1)),MID(A2,ROW($1:$30),1),""))`.
**Alternative:** Excel 365: `=TEXTBEFORE(TEXTAFTER(A2,"-"),"-")` (not run); Flash Fill with an example (not run).
**Result:** Run in LibreOffice: B = 4581, 77, 120045. The all-digits formula was run as an array formula (it returns nothing in LibreOffice if entered as a normal formula): C = 45813, 771, 1200454 (as text; use `--C2` for a number). TEXTBEFORE/TEXTAFTER alternative not run here.
**Version note:** Microsoft's TEXTJOIN page says the feature is available with Office 2019 or Microsoft 365 and lists Excel 2019, 2021, 2024 and 365 (Microsoft Support, "TEXTJOIN function"); Excel 2016 needs a long legacy formula or VBA.
**Edge cases:** Strings over 30 characters need a larger ROW range; decimals and minus signs are not handled.
**Likely follow-ups:** 1) *Keep as number?* Wrap in `--`. 2) *Only letters?* Reverse the test.
**Common mistakes:** Not asking which number is wanted; forgetting array entry.

### Q49 ⭐ 🔴 How do you remove duplicates while keeping a count of how many times each record appeared?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you count before you delete?
**Say this in the interview:** "I add a COUNTIF column first, paste it as values, then run Remove Duplicates, which keeps the first row with its count. In 365 I can use UNIQUE next to COUNTIF, or a pivot table."
**Explain simply:**
- Counting must happen *before* deletion, because deleted rows cannot be counted.
- Paste the counts as values; formulas would change when rows vanish.
- Remove Duplicates keeps the first occurrence (Microsoft Support).
**Example:** Swipe records per employee: E101 appears 4 times, so after cleaning the HR report must still show "E101, 4 swipes", not just "E101".
**Sample sheet:**

| | A |
|---|---|
| 1 | EmpID |
| 2 | E101 |
| 3 | E102 |
| 4 | E101 |
| 5 | E103 |
| 6 | E101 |
| 7 | E102 |
| 8 | E101 |

**Formula / Steps:** 1. Copy the sheet as a backup. 2. B2 `=COUNTIF($A$2:$A$8,A2)`, fill down. 3. Copy B > Paste Special > Values. 4. Select A:B > Data > Remove Duplicates > tick only EmpID.
**Alternative:** 365: `=UNIQUE(A2:A8)` with `=COUNTIF(A2:A8,D2#)`; or Insert > PivotTable, EmpID in Rows and Count of EmpID in Values (not run here).
**Result:** Run in LibreOffice: counts 4, 2, 4, 1, 4, 2, 4. After removal: E101 4, E102 2, E103 1 (pandas `value_counts` confirms the same).
**Version note:** The COUNTIF route works in all versions; UNIQUE is 365/2021/2024 (Microsoft Support, "UNIQUE function"). The `D2#` spill reference and the PivotTable alternative are not run here.
**Edge cases:** Trim and case differences create separate rows; clean first. COUNTIF ignores case, but "E101 " with a trailing space counts separately. If you tick the count column too, Remove Duplicates compares IDs and counts together; it still works here because the count is the same for each ID, but it is the wrong habit. Blank IDs would be counted as a group of their own.
**Likely follow-ups:** 1) *Why values?* Formulas recalculate. 2) *Keep the latest?* See Q28. 3) *Easiest no-delete route?* A PivotTable with EmpID in Rows and Count of EmpID in Values, which also leaves the source untouched.
**Common mistakes:** Removing first, then counting; ticking the count column in Remove Duplicates; leaving the counts as formulas, so they change or break after rows are removed.

### Q50 ⭐ 🔴 A cleaning formula using TRIM, CLEAN and SUBSTITUTE is slow on 500,000 rows. How do you make the workflow faster and more reliable?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you think about scale and repeatability?
**Say this in the interview:** "I stop using formulas for the heavy lifting. I move the cleaning to Power Query, which handles large data better and is repeatable. If I must use formulas, I do it once, paste values and set calculation to manual while working."
**Explain simply:**
- Each formula recalculates when anything changes; 500,000 rows x several functions is heavy.
- Fix 1: Power Query (Transform > Format > Trim / Clean, Replace Values).
- Fix 2: one combined helper column, paste as values, delete formulas.
- Fix 3: Formulas > Calculation Options > Manual while editing.
- Fix 4: avoid whole-column references; save as .xlsb (binary workbook) if size matters.
- Reliability: keep raw data untouched, add row-count checks (Q47).
**Example:** A 500,000-row attendance log with spaces and non-breaking spaces. Three helper columns (TRIM, CLEAN, SUBSTITUTE) are 1.5 million formulas; one combined column is 500,000.
**Sample sheet:** A small correctness test only (speed is not tested):

| | A (Raw) | B (Clean) | C (LEN) |
|---|---|---|---|
| 2 | `  Priya`+nbsp+`Sharma`+line break+space | | |
| 3 | `Ravi   Kumar` | | |

**Formula / Steps:** B2 `=TRIM(CLEAN(SUBSTITUTE(A2,CHAR(160)," ")))`, C2 `=LEN(B2)`; then Copy > Paste Special > Values, and set Formulas > Calculation Options > Manual while working.
**Alternative:** Power Query: Transform > Format > Trim, then Clean, then Replace Values (nbsp to space), Close & Load (not run here); or process in chunks.
**Result:** Run in LibreOffice on a tiny sample, using `UNICHAR(160)` because LibreOffice's `CHAR(160)` does not return a non-breaking space (in Excel for Windows, `CHAR(160)` does; from memory, unverified): "  Priya[nbsp]Sharma[line break] " became "Priya Sharma" (12 characters), and "Ravi   Kumar" became "Ravi Kumar" (10). Speed claims are not benchmarked here (from experience and memory, unverified).
**Version note:** Power Query is in Excel 2016 and later Windows versions (Microsoft Support, "Power Query data sources in Excel versions"; cited from the original writing, not re-fetched in review). The .xlsb format and Manual calculation exist in all desktop versions (from memory, unverified).
**Edge cases:** Excel row limit 1,048,576 rows (Microsoft Support, "Excel specifications and limits"); Power Query loads to a table or the Data Model; in Manual mode, press F9 to recalculate or the numbers look stale; a file with more than 1,048,576 rows cannot be opened fully in a worksheet, so use Power Query or a database.
**Likely follow-ups:** 1) *Still slow?* Use SQL or Python. 2) *Why manual calc?* Prevents recalculation after each edit. 3) *How do you prove it is reliable?* Row count and total before and after, spot-check ten rows (see Q47).
**Common mistakes:** Whole-column formulas; leaving everything live; going manual and forgetting to recalculate before sending the file.

