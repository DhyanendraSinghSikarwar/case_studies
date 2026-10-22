# Book 1 — Excel | Part 7: Power Query and Power Pivot 🟡

**Target:** 60 questions | **Actual:** 64 questions
**Scope:** Power Query (Get & Transform: clean, merge, append, unpivot, refresh) and Power Pivot (Data Model, relationships, DAX measures) in Excel.

### Q1 ⭐⭐⭐ 🟢 What is Power Query in Excel and what do you use it for?
**Asked at:** commonly asked (no company-specific report found). Our job-description samples list Power Query only as "good-to-have" (4 of 47 Hyderabad, 2 of 42 Bengaluru, 4 of 32 MIS/people postings; repo research), so it comes up mostly in MIS and reporting roles.
**What the interviewer is checking:** Can you say in one breath what it does and why it beats manual cleaning?
**Say this in the interview:** "Power Query is Excel's tool for connecting to data, cleaning and reshaping it, and loading the result into a sheet or the Data Model. It records every step, so next month I just click Refresh instead of repeating the clean-up by hand."
**Explain simply:**
- It imports from many places: Excel files, CSV, folders, databases, web pages. Microsoft describes it as letting you "import or connect to external data, and then shape that data" (Microsoft Support, "About Power Query in Excel").
- Each change you make (remove a column, change a type, merge tables) is saved as a step. Steps re-run on every refresh.
- The original source is not changed. Only the query output is.
- In Excel it is also called Get & Transform; you find it on the Data tab.
**Example:** HR gets a messy attendance export every month: blank rows, extra spaces in names, text instead of numbers. You clean it once in Power Query (about 6 steps). Each month you drop the new file in, press Refresh, and the clean table is ready.
**Formula / Steps:** Data > Get Data > choose a source > Transform Data (opens the Power Query Editor) > apply steps > Home > Close & Load (not run here; steps from Microsoft Support, "About Power Query in Excel").
**Alternative:** Formulas (TRIM, VLOOKUP) or manual copy-paste do the same job once, but must be redone every time.
**Version note:** Built in on Excel 2016, 2019, 2021, 2024 and Microsoft 365 (Microsoft Support, "About Power Query in Excel" and "Power Query data sources in Excel versions"). Excel for Mac: Microsoft 365 only, through Get Data (same page). Excel for the web is limited; Android/iOS not supported (same page). Google Sheets has no equivalent (from memory, unverified).
**Edge cases:** It needs data in a consistent layout; if the source changes shape (renamed column) the refresh can fail (see Q63).
**Likely follow-ups:** 1) *Does it change the source file?* No. 2) *Is it a formula?* No, it is a recorded list of steps written in a language called M (Q38).
**Common mistakes:** Calling it a macro; forgetting to Refresh; pasting results over the loaded table.

### Q2 ⭐⭐⭐ 🟢 What is the difference between Power Query and Power Pivot?
**Asked at:** commonly asked (no company-specific report found); the pair is named together in the prep material behind this part.
**What the interviewer is checking:** Do you know one prepares data and the other models and calculates on it?
**Say this in the interview:** "Power Query gets and cleans the data. Power Pivot takes the clean tables, links them with relationships and adds DAX calculations. Query is the kitchen prep; Pivot is the cooking."
**Explain simply:**
- Power Query = import and reshape. Microsoft: it lets you connect, reshape, combine and load to a worksheet or the Data Model (Microsoft Support, "How Power Query and Power Pivot work together").
- Power Pivot = "add richness" to the Data Model: relationships, calculated columns, measures, KPIs, hierarchies (same page).
- DAX is the formula language of Power Pivot (Q33). M is the language of Power Query (Q38).
- Typical flow: Power Query > Data Model > Power Pivot measures > PivotTable.
**Example:** Query combines 12 monthly attendance files and cleans them. Pivot then relates them to an Employee table and defines a measure "Attendance % = Present days / Working days".
**Formula / Steps:** Power Query: Data tab > Get Data. Power Pivot: Power Pivot tab > Manage (not run here).
**Alternative:** Do both jobs with plain formulas and PivotTables; slower and harder to refresh.
**Version note:** Power Query is in 2016 and later. Power Pivot's overview page lists Excel 365, 2024, 2021, 2019, 2016 as "applies to" (Microsoft Support, "Power Pivot - overview and learning"). Which Office editions actually include it could not be verified here (see Q19).
**Edge cases:** Power Query can load straight to a sheet without Power Pivot; Power Pivot needs the Data Model.
**Likely follow-ups:** 1) *Which comes first?* Query. 2) *Can a PivotTable use both?* Yes, via the Data Model.
**Common mistakes:** Saying Power Pivot cleans data; mixing up M and DAX.

### Q3 ⭐⭐⭐ 🟢 What is the difference between Merge and Append in Power Query?
**Asked at:** commonly asked; one Glassdoor EY intern review (Feb 2026, seen only as a search snippet, unverified) is reported to mention Merge vs Append.
**What the interviewer is checking:** Rows versus columns thinking.
**Say this in the interview:** "Append stacks tables on top of each other, adding rows, like January plus February attendance. Merge joins tables side by side on a matching column, adding columns, like attaching salary to an employee list. Append is like UNION; Merge is like a lookup or SQL JOIN."
**Explain simply:**
- Append: same columns, more rows.
- Merge: a key column (e.g. EmpID) matches rows between two tables and brings in columns.
- Merge needs a join kind (Left Outer is the usual one; see Q26).
**Example:** Jan (3 rows) + Feb (3 rows) appended = 6 rows. Master (5 rows) merged with Payroll on EmpID keeps 5 rows; E03 and E05 get blank salary.
**Sample sheet:** Jan/Feb tables (EmpID, Name, Dept, DaysPresent), Master (EmpID, Name, Dept), Payroll (EmpID, Salary). Output below came from pandas (run here); the Power Query step was not run.

Append (Jan + Feb):

| EmpID | Name | Dept | DaysPresent | Month |
|---|---|---|---|---|
| E01 | Asha | HR | 21 | Jan |
| E02 | Ravi | IT | 19 | Jan |
| E03 | Meena | HR | 22 | Jan |
| E01 | Asha | HR | 20 | Feb |
| E02 | Ravi | IT | 18 | Feb |
| E04 | Kiran | Sales | 19 | Feb |

Merge (Master left join Payroll on EmpID):

| EmpID | Name | Dept | Salary |
|---|---|---|---|
| E01 | Asha | HR | 40000 |
| E02 | Ravi | IT | 68000 |
| E03 | Meena | HR | blank |
| E04 | Kiran | Sales | 49000 |
| E05 | Tara | IT | blank |

**Formula / Steps:** Append: Home > Combine > Append Queries. Merge: Home > Combine > Merge Queries, pick key column in each table, choose Join Kind, OK, then expand the new column (not run here).
**Alternative:** Append ~ copy-paste rows; Merge ~ VLOOKUP/XLOOKUP, but refreshable.
**Result:** pandas: append gives 6 rows, left merge gives 5 rows with 2 blanks (run here); the Excel steps were not run.
**Version note:** Both available wherever Power Query exists (2016+). 
**Edge cases:** Append with different column names creates extra columns with nulls (Q30). Merge on a key with duplicates multiplies rows (Q21 shows the same effect).
**Likely follow-ups:** 1) *Which join by default?* Microsoft's "Merge queries (Power Query)" page says inner; Left Outer is the usual choice (conflict explained in Q26). 2) *Can you append more than two?* Yes, append can take more than two tables (from memory, unverified).
**Common mistakes:** Appending when you needed a merge; merging on a key that has spaces or different case, so nothing matches.

### Q4 ⭐⭐⭐ 🟢 How do you refresh a Power Query report when the source file changes?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know refresh is a click, not a rebuild, and its limits?
**Say this in the interview:** "I replace or update the source file and press Data > Refresh All. Every saved step runs again on the new data. If the file name or location changed I update the Source step."
**Explain simply:**
- Refresh pulls in "additions, changes, and deletes from the external data source" and re-runs each step (Microsoft Support, "About Power Query in Excel").
- Refresh All shortcut is Ctrl+Alt+F5; per-query refresh is on the Query tab > Refresh (Microsoft Support, "Refresh an external data connection in Excel").
- Refresh on open: Queries & Connections > right-click > Properties > Usage > "Refresh data when opening the file" (same page).
**Example:** March attendance sheet is added to the folder; click Refresh All and the summary PivotTable shows 3 months instead of 2. (PivotTables built on a query need their own refresh; Refresh All does both.)
**Formula / Steps:** 1. Update the source file. 2. Data > Refresh All. 3. If it errors, open the query and check the Source step (not run here).
**Alternative:** Right-click the query in the Queries & Connections pane > Refresh.
**Version note:** The refresh page applies to Excel 365, 2024, 2021, 2019, 2016 (Microsoft Support, "Refresh an external data connection in Excel").
**Edge cases:** Refresh fails if the file is moved, renamed, open and locked, or a column was renamed (Q47, Q63).
**Likely follow-ups:** 1) *Is it automatic?* Not unless you set refresh on open (Q62). 2) *Do formulas next to the table update?* Only if they refer to the table.
**Common mistakes:** Editing the loaded table by hand (changes are overwritten); forgetting to refresh the PivotTable.

### Q5 ⭐⭐⭐ 🟢 Why would you use Power Query instead of formulas or manual copy-paste to clean and prepare data?
**Asked at:** commonly asked; one Glassdoor EY intern review (Feb 2026, snippet only, unverified) reportedly covers transformation steps.
**What the interviewer is checking:** Do you think about repeatability and error risk?
**Say this in the interview:** "Because it is repeatable, auditable and does not touch the raw data. Manual cleaning takes 30 minutes every month and one slip can go unnoticed; Power Query does it in one click."
**Explain simply:**
- Repeatable: steps re-run on refresh.
- Auditable: the Applied Steps list shows exactly what was done (Q9).
- Handles bigger data and many files (Q6).
- Formulas still win for small one-off tweaks inside a sheet.
**Example:** Monthly payroll tidy-up takes 25 minutes by hand; with a query, 1 minute of refresh. Over 12 months that saves about 4.8 hours (24 min x 12 = 288 min; these are illustrative numbers).
**Formula / Steps:** Compare: manual = TRIM + remove duplicates + paste values each month; query = save once, refresh (not run here).
**Alternative:** VBA macro automates too, but is harder to read and maintain.
**Version note:** Power Query 2016+ (Microsoft Support, "About Power Query in Excel").
**Edge cases:** Not ideal when you need cell-by-cell manual judgement or the layout changes each month.
**Likely follow-ups:** 1) *Any downside?* Learning curve and refresh failures if layout changes. 2) *Formulas or Power Query for lookups?* Merge if refreshable matters.
**Common mistakes:** Saying "it is faster to type"; ignoring that raw data stays untouched.

### Q6 ⭐⭐⭐ 🟡 How would you combine 12 monthly attendance files from one folder into a single table using Power Query?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the From Folder route and its rules?
**Say this in the interview:** "Data > Get Data > From File > From Folder, point to the folder, Transform Data, then Combine Files on the Content column. Power Query stacks all 12 files into one table, and next month's file is picked up on refresh."
**Explain simply:**
- Put only the files you want in a dedicated folder (Microsoft Support, "Import data from a folder with multiple files (Power Query)").
- Files should have the same column headers, types and column count; column order may differ (same page).
- Power Query builds helper queries (Sample File, Transform File) and a final query named after the folder (same page).
- Add the file name as a column to know the month.
**Example:** Three files, Attendance_2025-01/02/03.csv, each with 3 rows, become 9 rows with a Source.Name column. Pandas replica (run here):

**Sample sheet:**

| EmpID | Name | Dept | DaysPresent | Source.Name |
|---|---|---|---|---|
| E01 | Asha | HR | 21 | Attendance_2025-01.csv |
| E02 | Ravi | IT | 19 | Attendance_2025-01.csv |
| E03 | Meena | HR | 22 | Attendance_2025-01.csv |
| E01 | Asha | HR | 20 | Attendance_2025-02.csv |
| E02 | Ravi | IT | 18 | Attendance_2025-02.csv |
| E04 | Kiran | Sales | 19 | Attendance_2025-02.csv |
| ... | ... | ... | ... | (3 more rows from March) |

**Formula / Steps:** 1. Data > Get Data > From File > From Folder. 2. Select folder > Open. 3. Transform Data. 4. Filter Extension if needed. 5. Select Content column > Home > Combine Files. 6. Check sample file > OK. 7. Optionally tick Skip files with errors. 8. Close & Load (not run here; Microsoft Support page above).
**Alternative:** Manual copy-paste of 12 sheets; or Append Queries one by one (not scalable).
**Result:** pandas: 3 files gave 9 rows (run here); the Excel combine was not run.
**Version note:** The folder page applies to Excel 365, 2024, 2021, 2019, 2016 (Microsoft Support, same page).
**Edge cases:** A file with a different header or a stray file in the folder breaks or pollutes the result; temporary files like ~$ lock files can show up in the list (from memory, unverified).
**Likely follow-ups:** 1) *Next month's file?* Drop it in the folder and refresh. 2) *Folder path differs on a colleague's PC?* Use a parameter (Q49).
**Common mistakes:** Mixed files in the folder; not keeping consistent headers; not keeping the file name column.

### Q7 ⭐⭐⭐ 🟡 What is the difference between a calculated column and a measure in Power Pivot?
**Asked at:** commonly asked; present in every prep source behind this part.
**What the interviewer is checking:** Do you understand row-level versus aggregated calculation?
**Say this in the interview:** "A calculated column computes a value for every row and stores it. A measure computes an answer on the fly for whatever the PivotTable is showing, such as total or average. Use a column when you need a field for rows, filters or slicers, and a measure for numbers in the Values area."
**Explain simply:**
- Calculated column: stored for every row, uses more memory (Microsoft Support, "Calculated Columns in Power Pivot").
- Measure: calculated only for the cells displayed, and changes with filters (Microsoft Support, "Measures in Power Pivot").
- Row example: Annual salary = Monthly x 12 per employee. Measure example: average monthly salary per department.
**Example:** pandas replica (run here): Annual column for 4 employees; measure average by Dept gives HR 40,500, IT 68,000, Sales 49,000; grand total 49,500; filtered to HR only 40,500.
**Sample sheet:**

| EmpID | Dept | Monthly | Annual (calc. column) |
|---|---|---|---|
| E01 | HR | 40000 | 480000 |
| E02 | IT | 68000 | 816000 |
| E03 | HR | 41000 | 492000 |
| E04 | Sales | 49000 | 588000 |

**Formula / Steps:** Calculated column (DAX, not run here): `Annual = [Monthly] * 12`. Measure: `Avg Monthly := AVERAGE(Emp[Monthly])`.
**Alternative:** Do the row calculation in Power Query as a custom column (computed at refresh).
**Result:** pandas values above (run here); DAX not run.
**Version note:** Power Pivot is in Excel 2016 and later on the Windows versions covered by Microsoft's pages (Microsoft Support pages above); edition availability unverified (Q19).
**Edge cases:** A measure that is a total never makes a good slicer; a calculated column cannot respond to the PivotTable filter.
**Likely follow-ups:** 1) *Which is lighter on memory?* Measure. 2) *Can a measure be used as a row label?* No.
**Common mistakes:** Making everything a calculated column; summing percentages stored per row.

### Q8 ⭐⭐ 🟢 Where do you find Power Query in Excel 2016, 2019 and Microsoft 365?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Version awareness.
**Say this in the interview:** "On Windows, in all three it is on the Data tab in the Get & Transform group. It is built in from Excel 2016; Microsoft 365 has the full feature set, perpetual versions a subset."
**Explain simply:**
- Microsoft: Power Query is included in "all Excel 2016 or later Windows stand alone versions and Microsoft 365 subscription plans"; ribbon location Data > Get & Transform (Microsoft Support, "Power Query data sources in Excel versions").
- 365 has all features; perpetual versions have a subset; for example fuzzy merge is in 365 but not 2019 (same page).
- Mac: Microsoft 365 only, via Get Data on the Data tab. Excel for the web: limited sources. Android/iOS: not supported (same page).
**Example:** A colleague on Excel 2019 cannot use fuzzy matching in Merge that you use on 365.
**Formula / Steps:** Data tab > Get & Transform Data group > Get Data (not run here).
**Alternative:** On Excel 2010/2013 it was a separate add-in (from memory, unverified).
**Version note:** As above, all from the cited Microsoft page. Its title when fetched on 2026-10-22 was "Power Query data sources in Excel versions"; the sources file recorded the same article (ID e9332067) as "Where is Get & Transform (Power Query)", so earlier wording of this part may use either title. Fuzzy merge in 2016 perpetual is not stated (see Q42).
**Edge cases:** Ribbon labels differ slightly between builds ("Get & Transform" vs "Get & Transform Data").
**Likely follow-ups:** 1) *Mac?* Yes with 365, with limited sources. 2) *Excel online?* Limited.
**Common mistakes:** Looking under Insert; assuming every feature is in every version.

### Q9 ⭐⭐ 🟢 What are Applied Steps in the Power Query Editor, and why do they matter?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know steps are the recipe that makes refresh work?
**Say this in the interview:** "Applied Steps are the recorded list of every transformation in order. They re-run on refresh, I can click any step to see the data at that point, and I can rename, reorder or delete steps."
**Explain simply:**
- Power Query records and labels each step in the Applied Steps list in the Query Settings pane (Microsoft Support, "About Power Query in Excel").
- Clicking a step shows the data as it was after that step.
- Steps run in order, so deleting an early step can break later ones.
- Rename steps clearly ("Removed blank rows") for the next person.
**Example:** 6 steps: Source, Promoted Headers, Changed Type, Removed Blank Rows, Trimmed Text, Filtered Hyderabad. Click "Changed Type" to see data before filtering.
**Formula / Steps:** View > Query Settings (if hidden) > Applied Steps; right-click a step > Rename / Delete / Move (not run here).
**Alternative:** Advanced Editor shows the same steps as M code (Q38).
**Version note:** Same Editor in 2016+ (Microsoft Support, "About Power Query in Excel").
**Edge cases:** Inserting a step in the middle can break later steps that depend on a column name.
**Likely follow-ups:** 1) *Where is it?* Right side, Query Settings. 2) *Can I undo?* Delete the step.
**Common mistakes:** Leaving default names like "Changed Type1"; deleting Source or Changed Type without checking.

### Q10 ⭐⭐ 🟢 How do you change data types of columns in Power Query, and what goes wrong if you skip it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know text-versus-number problems?
**Say this in the interview:** "Select the column, Home > Data Type (or the icon in the header) and choose Whole Number, Date and so on. If I skip it, numbers stored as text sort wrongly, do not sum, and dates can be read in the wrong day-month order."
**Explain simply:**
- Each header has a small icon showing type (ABC text, 123 number, calendar date).
- Wrong type = wrong sort, wrong totals, wrong date.
- For dates in dd/mm/yyyy, use Change Type > Using Locale to be safe.
**Example:** Salaries 9000, 55000, 100000, 40000 stored as text sort as 100000, 40000, 55000, 9000; as numbers 9000, 40000, 55000, 100000, sum 204000 (pandas, run here). Dates "03/04/2025" and "15/04/2025" parsed day-first give 2025-04-03 and 2025-04-15.
**Formula / Steps:** Select column > Transform (or Home) > Data Type > Whole Number. M (not run here): `Table.TransformColumnTypes(Source, {{"Salary", Int64.Type}})`.
**Alternative:** Excel VALUE() or Text to Columns for one-off fixes.
**Result:** Sorting and sum above from pandas (run here); the Power Query step was not run. In pandas, summing text concatenated it into "90005500010000040000".
**Version note:** Same in 2016+ (not separately verified).
**Edge cases:** Text like "N/A" in a number column becomes an Error after the type change (Q29).
**Likely follow-ups:** 1) *Change Type or Using Locale?* Locale for non-US dates. 2) *Automatic type detection?* Power Query adds a Changed Type step, check it.
**Common mistakes:** Trusting auto-detected types; changing type before cleaning text.

### Q11 ⭐⭐ 🟢 How do you remove duplicates and blank rows in Power Query?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic cleaning, and the difference between duplicate and blank.
**Say this in the interview:** "Home > Remove Rows > Remove Blank Rows, and select the key column(s) then Remove Rows > Remove Duplicates."
**Explain simply:**
- Remove Blank Rows deletes rows where all cells are empty.
- Remove Duplicates keeps the first row for each repeated value in the selected column(s).
- Duplicates are judged only on columns you selected.
**Example:** 5 rows: E01, E02, E02, an empty row, E03. After removing blanks: 4 rows. After removing duplicates: 3 rows (pandas, run here).
**Sample sheet:**

| EmpID | Name | Dept |
|---|---|---|
| E01 | Asha | HR |
| E02 | Ravi | IT |
| E02 | Ravi | IT |
| (empty) | (empty) | (empty) |
| E03 | Meena | HR |

**Formula / Steps:** Home > Reduce Rows > Remove Rows > Remove Blank Rows; select EmpID > Remove Rows > Remove Duplicates (not run here). M: `Table.Distinct(Source, {"EmpID"})`.
**Alternative:** Excel Data > Remove Duplicates, which is one-time.
**Result:** 5 > 4 > 3 rows (pandas, run here).
**Version note:** 2016+ (not separately verified).
**Edge cases:** Power Query duplicate matching is case-sensitive (from memory, unverified); pandas replica: "HR" vs "hr" were not duplicates (run here). Trim and fix case first (Q14). Rows with spaces only are not "blank".
**Likely follow-ups:** 1) *Which duplicate is kept?* The first. 2) *Duplicates on all columns?* Select all columns.
**Common mistakes:** Removing duplicates on all columns when only the ID matters; not trimming text first.

### Q12 ⭐⭐ 🟢 How do you replace null values with a default value (for example 0 or "Not Available") in Power Query?
**Asked at:** commonly asked; one Glassdoor EY review (snippet only, unverified) mentions errors/nulls.
**What the interviewer is checking:** Do you know null is not zero and not empty text?
**Say this in the interview:** "Select the column, Transform > Replace Values, put null as the value to find and 0 or Not Available as the replacement. A null means no value at all; that is different from zero or an empty string."
**Explain simply:**
- Type `null` (lower case) in the "Value To Find" box.
- Use 0 for number columns, text for text columns; replacement type must match the column.
- Empty text ("") is not null; clean it separately.
**Example:** Bonus: 5000, null, 2000 > 5000, 0, 2000; Manager null > "Not Available" (pandas replica, run here).
**Sample sheet:**

| Name | Bonus | Manager |
|---|---|---|
| Asha | 5000 | Rao |
| Ravi | null | null |
| Meena | 2000 | Rao |

**Formula / Steps:** Select column > Transform > Replace Values > Value To Find `null` > Replace With `0`. M: `Table.ReplaceValue(Source, null, 0, Replacer.ReplaceValue, {"Bonus"})` (not run here).
**Alternative:** Transform > Fill > Down to copy the previous value; or Replace Errors (Q29).
**Result:** Ravi's Bonus 0 and Manager "Not Available" (pandas, run here).
**Version note:** 2016+ (not separately verified).
**Edge cases:** Empty strings show as blank but are not null; pandas replica confirmed "" is not null (run here).
**Likely follow-ups:** 1) *Why not leave null?* Averages ignore nulls; zero lowers them. Choose deliberately. 2) *Fill Down?* For merged-cell style reports.
**Common mistakes:** Replacing null with 0 and distorting averages; typing "NULL" in capitals.

### Q13 ⭐⭐ 🟢 How do you split a "Full Name" column into first name and last name in Power Query?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Split Column by delimiter and its edge cases.
**Say this in the interview:** "Select the column, Home > Split Column > By Delimiter, choose Space and 'Left-most delimiter'. That gives the first name and the rest."
**Explain simply:**
- Delimiter = the character that separates parts (a space here).
- "Left-most" splits at the first space only, so middle names stay with the last name.
- Rename the new columns afterwards.
**Example:** "Asha Nair" > Asha | Nair; "Ravi Kumar Singh" > Ravi | Kumar Singh; "Meena" > Meena | blank (pandas, run here).
**Sample sheet:**

| Full Name | First | Last |
|---|---|---|
| Asha Nair | Asha | Nair |
| Ravi Kumar Singh | Ravi | Kumar Singh |
| Meena | Meena | null |

**Formula / Steps:** Select Full Name > Home > Split Column > By Delimiter > Space > Left-most delimiter > OK (not run here). 
**Alternative:** Excel formulas TEXTBEFORE/TEXTAFTER (365 only) or LEFT/FIND.
**Result:** Table above from pandas (run here).
**Version note:** Split Column is in 2016+ (not separately verified).
**Edge cases:** Double spaces create empty parts; trim first (Q14). Single names leave Last empty.
**Likely follow-ups:** 1) *Split into rows instead?* Yes, "Split into Rows" option. 2) *Last word as surname?* Use "Right-most delimiter".
**Common mistakes:** Using "Each occurrence" so a 3-part name makes 3 columns.

### Q14 ⭐⭐ 🟢 How do you trim spaces and fix text case (Clean, Trim, Proper) in Power Query?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know Format menu and what Trim does not fix.
**Say this in the interview:** "Select the column, Transform > Format > Trim, Clean, Capitalize Each Word. Trim removes extra spaces at the ends, Clean removes non-printing characters, and Capitalize Each Word is the same as Proper."
**Explain simply:**
- Trim: leading and trailing spaces only. It does not collapse spaces inside the text (from memory, unverified; the pandas replica below behaves the same way).
- Clean: removes invisible control characters such as tabs or line breaks (from memory, unverified).
- Capitalize Each Word = Proper case.
**Example:** "  asha  NAIR" > "Asha  Nair" (inner double space remains); after also replacing repeated spaces > "Asha Nair" (pandas, run here).
**Sample sheet:**

| Raw | Strip + title | After also collapsing inner spaces |
|---|---|---|
| "  asha  NAIR" | Asha  Nair | Asha Nair |
| "RAVI   kumar " | Ravi   Kumar | Ravi Kumar |
| "meena<tab>iyer" | Meena<tab>Iyer | Meena Iyer |

**Formula / Steps:** Select column > Transform > Format > Trim, then Clean, then Capitalize Each Word (not run here). M: `Table.TransformColumns(Source, {{"Name", each Text.Proper(Text.Trim(Text.Clean(_)))}})`.
**Alternative:** Excel TRIM, CLEAN and PROPER functions (TRIM there does collapse inner spaces).
**Result:** pandas outputs above (run here); Power Query not run.
**Version note:** 2016+ (not separately verified).
**Edge cases:** Non-breaking spaces (from web pages) are not removed by Trim; replace them explicitly (from memory, unverified). Proper turns "McDonald" into "Mcdonald".
**Likely follow-ups:** 1) *Do it for all columns?* Select all, then Format. 2) *Upper case?* Format > UPPERCASE.
**Common mistakes:** Cleaning case but not trimming; filtering before trimming (see Q15).

### Q15 ⭐⭐ 🟢 How do you filter rows in Power Query (for example keep only employees from the Hyderabad office)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you use the column filter and know about dirty values?
**Say this in the interview:** "Click the dropdown on the Location column, untick everything but Hyderabad, OK. For dirty data I trim and fix case first so 'hyderabad ' is not missed."
**Explain simply:**
- The dropdown lists only the first values it samples; use Text Filters > Equals for exactness.
- Filtering adds a step (Filtered Rows) that re-runs on refresh.
- Filter early to reduce data (Q31).
**Example:** Locations: Hyderabad, Bengaluru, hyderabad, "Hyderabad " (trailing space). Exact filter keeps 1 (Asha); after trim and lower-case, 3 (Asha, Meena, Kiran) (pandas, run here).
**Sample sheet:**

| Name | Location |
|---|---|
| Asha | Hyderabad |
| Ravi | Bengaluru |
| Meena | hyderabad |
| Kiran | Hyderabad (trailing space) |

**Formula / Steps:** Column dropdown > Text Filters > Equals > Hyderabad > OK (not run here). M: `Table.SelectRows(Source, each [Location] = "Hyderabad")`.
**Alternative:** Excel's AutoFilter (not refreshable) or FILTER() (365/2021 only; not available in LibreOffice here, not run).
**Result:** 1 row exact versus 3 rows cleaned (pandas, run here).
**Version note:** 2016+ (not separately verified). M text comparison is case-sensitive (from memory, unverified).
**Edge cases:** Nulls are excluded by an Equals filter; the dropdown may show "List may be incomplete" for big tables.
**Likely follow-ups:** 1) *Multiple offices?* Tick several, or use "or" conditions. 2) *Filter by date?* Date Filters submenu.
**Common mistakes:** Not trimming first; filtering using the dropdown tick-list when values may be missing from it.

### Q16 ⭐⭐ 🟢 How do you add a conditional column in Power Query (the equivalent of an IF formula)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Add Column > Conditional Column and order of conditions.
**Say this in the interview:** "Add Column > Conditional Column, fill in If / Then / Else rows. It is like IF or IFS, evaluated top to bottom, and the first true condition wins."
**Explain simply:**
- Each rule has column, operator, value and output.
- Add an Else for everything else.
- Handle nulls explicitly or they fall into Else.
**Example:** Attendance >= 95% Good; >= 90% Average; else Low; blank = Unknown (pandas replica, run here).
**Sample sheet:**

| Name | Attendance | Band |
|---|---|---|
| Asha | 0.97 | Good |
| Ravi | 0.88 | Low |
| Meena | 0.93 | Average |
| Kiran | blank | Unknown |

**Formula / Steps:** Add Column > Conditional Column; If Attendance >= 0.95 then Good; Else If >= 0.9 then Average; Else Low (not run here). M: `if [Attendance] = null then "Unknown" else if [Attendance] >= 0.95 then "Good" else if [Attendance] >= 0.9 then "Average" else "Low"` (Custom Column, not run here).
**Alternative:** Excel `=IF(...)` or `=IFS(...)` (IFS is 2019+, from memory, unverified).
**Result:** Bands above from pandas (run here); Power Query not run.
**Version note:** 2016+ (not separately verified).
**Edge cases:** In M, comparing null with >= does not give a clean true (the exact result, null or false, is from memory, unverified): handle nulls first, as the pandas replica does.
**Likely follow-ups:** 1) *More than the dialog allows?* Use Custom Column. 2) *Is "if" case-sensitive in M?* Yes, lower case.
**Common mistakes:** Wrong order of conditions; not setting the type of the new column.

### Q17 ⭐⭐ 🟢 What is Group By in Power Query, and how is it different from a PivotTable?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know it creates a table, not a layout?
**Say this in the interview:** "Group By summarises rows into a smaller table, for example headcount and average salary per department, as a step in the query. A PivotTable is an interactive report you rearrange; Group By is a fixed transformation that refreshes with the query."
**Explain simply:**
- Transform > Group By; choose the column(s) to group and the aggregations (Sum, Average, Count Rows...).
- Output is a normal table you can merge or load.
- PivotTable: drag-and-drop, slicers, subtotals, no step recording.
**Example:** Six employees by department (HR: 40000, 41000; IT: 68000 three times; Sales: 49000). Output (pandas, run here, rechecked in Wave C):

**Sample sheet:**

| Dept | Headcount | AvgSalary | Total |
|---|---|---|---|
| HR | 2 | 40500 | 81000 |
| IT | 3 | 68000 | 204000 |
| Sales | 1 | 49000 | 49000 |

**Formula / Steps:** Home or Transform > Group By > Dept > New column name Headcount, Operation Count Rows; Add aggregation > AvgSalary > Average of Salary (not run here).
**Alternative:** PivotTable (Insert > PivotTable) gives the same figures interactively.
**Result:** Table above from pandas (run here).
**Version note:** 2016+ (not separately verified).
**Edge cases:** Group By on a column with spaces or case differences creates separate groups.
**Likely follow-ups:** 1) *When Group By?* To feed another query. 2) *When Pivot?* For exploration.
**Common mistakes:** Grouping before cleaning text; using Group By for something a slicer should do.

### Q18 ⭐⭐ 🟢 What does "Close & Load To..." offer, and what is a "Connection only" query?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know where results can land and when not to load them?
**Say this in the interview:** "Close & Load To lets me choose Table, PivotTable report, PivotChart, or Only Create Connection, and whether to add the data to the Data Model. Connection only keeps the query without putting data on a sheet; I use it for helper queries and queries feeding other queries."
**Explain simply:**
- Table = data on a sheet. Connection only = nothing on a sheet, but the query exists and can be referenced.
- "Add this data to the Data Model" sends the data to Power Pivot (Microsoft Support, "Create, load, or edit a query in Excel (Power Query)" documents the Data Model option; the other option names are from memory, unverified).
- Home > Close & Load, or right-click a query in Queries & Connections > Load To (Microsoft Support, "About Power Query in Excel").
**Example:** A raw "Attendance" query is connection only; a "Dept Summary" query referencing it is loaded to a table. No duplicate raw data on a sheet.
**Formula / Steps:** Home > Close & Load drop-down > Close & Load To... > pick option > OK (not run here).
**Alternative:** Reload later by right-click > Load To.
**Version note:** Applies to 2016 to 365 (Microsoft Support, "About Power Query in Excel").
**Edge cases:** Connection-only queries still refresh when referenced; loaded worksheet tables are capped by sheet size (not verified here).
**Likely follow-ups:** 1) *Why connection only?* Save space and speed. 2) *Can I change later?* Yes.
**Common mistakes:** Loading the raw and the clean table both; deleting a query another one depends on.

### Q19 ⭐⭐ 🟢 What is Power Pivot, and how do you enable it in Excel?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know it is an add-in and where it lives?
**Say this in the interview:** "Power Pivot is Excel's Data Model engine and add-in: it lets me hold many tables, link them with relationships and write DAX measures. On Windows I turn it on if the Power Pivot tab is missing, then use Power Pivot > Manage."
**Explain simply:**
- Described by Microsoft as an Excel add-in for "powerful data analysis" and sophisticated data models (Microsoft Support, "Power Pivot - overview and learning").
- Open the window: Power Pivot tab > Manage (Microsoft Support, "Start the Power Pivot add-in for Excel").
- If the tab disappears: File > Options > Add-Ins > Manage: Disabled Items > Go > select Microsoft Office Power Pivot > Enable (same page).
- If it is not in the COM list at all, File > Options > Add-ins > Manage: COM Add-ins > Go > tick "Microsoft Power Pivot for Excel" (from memory; a search summary of a Microsoft page described this but I did not read the page, unverified).
**Example:** An HR analyst relates Employees, Attendance and Departments tables and builds a "Headcount" measure used in one PivotTable.
**Formula / Steps:** Power Pivot tab > Manage (not run here).
**Alternative:** The Data Model can also be used without opening Power Pivot, via Add to Data Model on a PivotTable.
**Version note:** The overview page lists Excel for Microsoft 365, 2024, 2021, 2019, 2016 (Microsoft Support, "Power Pivot - overview and learning"); the "Start" page lists 365, 2024, 2021. Which Office editions include it (for example Home & Student or Mac) is unverified: the "Where is Power Pivot?" page returned HTTP 403 earlier, and on re-fetch that address showed the overview page, which lists no exclusions. Microsoft Support, "Turn on Power Pivot" (fetched): "Power Pivot isn't currently available on Excel for Mac" or Excel for the web; it is available in the Excel desktop app (Windows). A search summary (page not read) said an older Microsoft article, "What versions of Office include Power Pivot?", excludes Office Home & Student 2016 and Home & Business 2016 and includes Office 2016 Professional Plus only through volume licensing, while Wikipedia says an April 2018 update added it to all Excel 2016 versions; both unverified. Check with the IT team.
**Edge cases:** Corporate laptops may block add-ins.
**Likely follow-ups:** 1) *Mac?* No: Microsoft Support, "Turn on Power Pivot", says it is not available on Excel for Mac or the web. 2) *Difference from Power Query?* Q2.
**Common mistakes:** Assuming every Excel install has the tab; confusing it with a PivotTable.

### Q20 ⭐⭐ 🟢 What is the Excel Data Model?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know it is an in-workbook relational store?
**Say this in the interview:** "The Data Model is a hidden database inside the workbook that holds several related tables, so one PivotTable can use fields from all of them without VLOOKUPs."
**Explain simply:**
- Microsoft: it lets you combine data from several tables into a relational data source inside the workbook (Microsoft Support, "Create a Data Model in Excel").
- A workbook can contain only one Data Model (same page).
- You see its tables in the PivotTable Field List.
- Fill it via Power Query (Load to Data Model) or Power Pivot > Add to Data Model.
**Example:** Employees (5,000 rows) and Attendance (60,000 rows) related by EmpID, summarised in one PivotTable.
**Formula / Steps:** Data > Get Data > select multiple tables > Transform; or Power Pivot > Add to Data Model (not run here; Microsoft Support page above).
**Alternative:** Worksheet-only approach with VLOOKUP columns (Q21).
**Version note:** The Data Model article applies to Excel 365, 2024, 2021; the relationships article also lists 2019 and 2016 (Microsoft Support pages above).
**Edge cases:** Source data should be in tables (same page). You cannot type new rows into a Power Pivot table; update the source and refresh.
**Likely follow-ups:** 1) *Size?* Limits not verified here (Q59). 2) *Who sees it?* Anyone with the file.
**Common mistakes:** Believing it is a separate file; loading data twice.

### Q21 ⭐⭐ 🟢 Why would you build a Data Model with relationships instead of using VLOOKUP to bring tables together?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Scalability and maintainability thinking.
**Say this in the interview:** "Relationships keep each table separate and join them only when the PivotTable needs it. There are no copied lookup columns, so it is faster on big data, easier to refresh and avoids the repeated data a flat table has."
**Explain simply:**
- Splitting data into related tables avoids repeating details on every row (Microsoft Support, "Relationships between tables in a Data Model").
- VLOOKUP creates one formula per row and widens the sheet.
- Changes made once in the lookup table flow through.
- Several fact tables can share the same lookup tables.
**Example:** Employees (EmpID, Dept, Salary: HR 40000 and 41000, IT 68000 three times, Sales 49000) and Department (Dept, Head). A relationship on Dept gives salary by department head: Das 49,000; Rao 81,000; Sen 204,000 (pandas join then group, run here).
**Sample sheet:**

| Dept | Head | Salary total |
|---|---|---|
| HR | Rao | 81000 |
| IT | Sen | 204000 |
| Sales | Das | 49000 |

**Formula / Steps:** VLOOKUP route: `=VLOOKUP(B2, Dept!A:B, 2, FALSE)` per row. Model route: Data > Relationships > New (Q22), then PivotTable from the model (not run here).
**Alternative:** Power Query Merge (Q46) when you want one flat table.
**Result:** pandas totals above (run here).
**Version note:** Data Model 2016+ per relationships page (Microsoft Support above).
**Edge cases:** A duplicated key in the lookup table breaks things: in the pandas replica, a duplicated HR row grew 6 rows to 8 and total salary from 334,000 to 415,000 (run here). Excel's relationship requires unique lookup values, so it refuses instead (Microsoft Support, "Create a relationship between tables in Excel").
**Likely follow-ups:** 1) *Is VLOOKUP ever better?* For tiny one-off sheets. 2) *Many-to-many?* Not directly supported (Microsoft Support, same page).
**Common mistakes:** Merging everything into one wide sheet; not checking the key is unique.

### Q22 ⭐⭐ 🟢 How do you create a relationship between two tables in the Power Pivot Data Model?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Click path and the unique-key rule.
**Say this in the interview:** "In Power Pivot, Manage > Diagram View, drag the key field from one table onto the matching field in the other. The lookup column must be unique and both columns need compatible types. From the worksheet it is Data > Relationships > New."
**Explain simply:**
- Diagram View: drag a primary key (e.g. Student ID) onto the matching field; names can differ but types must match (Microsoft Support, "Create a Data Model in Excel").
- Worksheet route: Data > Relationships > Manage Relationships > New; set Table (many side), Column (Foreign), Related Table, Related Column (Primary) (Microsoft Support, "Create a relationship between tables in Excel").
- Requirements: data formatted as named tables; lookup column unique, blanks count as one value (same pages).
- Excel does not check that values really match, so test with a PivotTable (from a search summary of that page, not fully read: unverified).
**Example:** Employees[Dept] (many) to Department[Dept] (one). Check before linking: Department key unique = True, orphan values in Employees = none (pandas, run here).
**Formula / Steps:** 1. Format both as tables and name them. 2. Confirm one column has no duplicates. 3. Data > Relationships > New. 4. Choose tables and columns > OK (not run here).
**Alternative:** Power Pivot > Manage > Diagram View drag-and-drop.
**Result:** pandas check above (run here); the relationship itself was not run.
**Version note:** The relationship page applies to Excel 365, 2024, 2021 (Microsoft Support, "Create a relationship between tables in Excel"); the "Relationships between tables in a Data Model" page also lists 2019 and 2016.
**Edge cases:** Many-to-many is not directly supported (same page); composite keys need a combined key column (from a search summary, unverified).
**Likely follow-ups:** 1) *Which side is "many"?* The table with repeated key values, e.g. Employees. 2) *Relationship greyed out?* The workbook has only one table.
**Common mistakes:** Duplicate keys in the lookup table; text key in one table and number in the other; creating the relationship in the wrong direction.

### Q23 ⭐⭐ 🟢 What is the difference between a one-to-many and a many-to-many relationship?
**Asked at:** commonly asked (no company-specific report found); Power BI prep guides list relationships as a frequent topic (Weekday and similar, 2025-26, snippet-level).
**What the interviewer is checking:** Do you understand how two tables link, and why one side needs unique values?
**Say this in the interview:** "One-to-many means one row on one side matches many rows on the other, like one department and many employees. Many-to-many means both sides repeat the key. Excel's Data Model does not support it directly, so I add a unique lookup table in the middle."
**Explain simply:**
- A relationship is a link between two tables through a shared column (the key), such as DeptID.
- One-to-many: the "one" table (Departments) has each DeptID once; the "many" table (Attendance) repeats it.
- Many-to-many: both tables repeat the key (employees with many skills, skills with many projects). Joining them multiplies rows.
- Microsoft: "Many-to-many relationships are not supported in a Data Model" and "the data values in the lookup column must be unique" (Microsoft Support, "Relationships between tables in a Data Model").
**Example:** Attendance has 5 rows over 3 departments. Joined to a unique Department table, totals stay correct. Joining a 3-row Skills list (a, a, b) to a 3-row Projects list (a, a, b) on Skill gives 5 rows, a row explosion.
**Sample sheet:**

| | A (Dept table) | B | | D (Attendance) | E | F |
|---|---|---|---|---|---|---|
| 1 | DeptID | Dept | | EmpID | DeptID | Days |
| 2 | 10 | HR | | 1 | 10 | 22 |
| 3 | 20 | Sales | | 2 | 20 | 20 |
| 4 | 30 | IT | | 3 | 20 | 18 |
| 5 | | | | 4 | 30 | 21 |
| 6 | | | | 5 | 20 | 19 |

**Formula / Steps:** (Not run here: Excel UI.) Data > Relationships (or Power Pivot > Diagram View), drag DeptID from Attendance onto DeptID in the Dept table; the line shows 1 and *.
**Alternative:** For many-to-many, build a "bridge" table of unique keys, or merge in Power Query first.
**Result:** pandas check (run): DeptID unique in Dept table = True, in Attendance = False; days by Dept: HR 22, IT 21, Sales 57. Skills x Projects many-to-many join = 5 rows from 3 + 3.
**Version note:** Data Model one-to-many works in Excel 2016+ Windows (Microsoft Support relationships page, "Applies to" not re-checked). Power BI later added many-to-many relationships (from memory, unverified).
**Edge cases:** Duplicate or blank keys in the "one" table break the relationship; text vs number keys do not match.
**Likely follow-ups:** 1) *Why not many-to-many?* It double counts. 2) *One-to-one?* Allowed; each key appears once on both sides.
**Common mistakes:** Making the transaction table the "one" side; ignoring duplicates in the lookup table.

### Q24 ⭐⭐ 🟢 How do you create a PivotTable from the Data Model, and how is it different from a normal PivotTable?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you build a report across several tables without VLOOKUP?
**Say this in the interview:** "I load tables into the Data Model, link them with relationships, then insert a PivotTable from the Data Model. It can use fields from all linked tables and DAX measures; a normal PivotTable uses one table."
**Explain simply:**
- Data Model = a hidden mini-database inside the workbook that holds related tables.
- Normal PivotTable: one range or table. Data Model PivotTable: many tables, shown in the field list together.
- It also allows Distinct Count and measures (see Q32, Q35).
**Example:** Salary table has only DeptID; the Department table has names. The Data Model PivotTable shows total salary by Dept name.
**Sample sheet:** Salary table: EmpID 1-5, DeptID 10,20,20,30,20, Salary 40,55,60,70,50 (in thousands); Dept table as in Q23.
**Formula / Steps:** (Not run here.) Per Microsoft Support, "Use multiple tables to create a PivotTable in Excel": 1) click any cell; 2) Insert > PivotTable dropdown > From External Data Source; 3) Choose Connection; 4) Tables tab > "Tables in Workbook Data Model"; 5) Open > OK. If Excel says a relationship is needed, click Create. Microsoft notes Data Models are not supported on Excel for Mac.
**Alternative:** Insert > PivotTable > From Table/Range and tick "Add this data to the Data Model" (from memory, unverified).
**Result:** pandas reproduction of the expected PivotTable (not Excel): HR 40, IT 70, Sales 165.
**Version note:** Windows desktop Excel 2016+; Mac not supported for Data Models (Microsoft Support page above).
**Edge cases:** Missing relationship gives a "relationships may be needed" prompt; the exact wording was not on the fetched page.
**Likely follow-ups:** 1) *Can I add a calculated field?* Not in a Data Model PivotTable; use a measure. 2) *Size?* Data Model is compressed (from memory).
**Common mistakes:** Using the normal "From Table/Range" and wondering why other tables are missing.

### Q25 ⭐⭐ 🟡 What is Unpivot in Power Query, and when would you use it? (for example, a sheet with one column per month)
**Asked at:** commonly asked (no company-specific report found); unpivot is a standard Power Query prep topic.
**What the interviewer is checking:** Can you turn a wide report into a tidy table that PivotTables and formulas can use?
**Say this in the interview:** "Unpivot turns columns into rows. A sheet with Jan, Feb, Mar columns becomes three columns: Employee, Month, Days. That tidy shape is what PivotTables need."
**Explain simply:**
- Wide layout: one column per month. Tidy layout: one row per employee per month.
- Microsoft: unpivoting (flattening) puts "all similar values in one column" for charts and reports (Microsoft Support, "Unpivot columns (Power Query)").
- The new Attribute column holds old headers; Value holds the numbers. Rename them to Month and Days.
**Example:** 2 employees x 3 months wide = 6 tidy rows.
**Sample sheet:**

| | A | B | C | D |
|---|---|---|---|---|
| 1 | Emp | Jan | Feb | Mar |
| 2 | Asha | 22 | 19 | 21 |
| 3 | Ravi | 20 | 21 | 22 |

**Formula / Steps:** (Not run here.) Data > From Table/Range > select column Emp > Transform > Unpivot Columns dropdown > Unpivot Other Columns > rename Attribute and Value > Close & Load. M: `Table.UnpivotOtherColumns(Source, {"Emp"}, "Month", "Days")`.
**Alternative:** Select Jan:Mar and use Unpivot Columns (see Q43).
**Result:** pandas melt (run): Asha-Jan 22, Ravi-Jan 20, Asha-Feb 19, Ravi-Feb 21, Asha-Mar 21, Ravi-Mar 22 (6 rows).
**Version note:** The "Unpivot columns (Power Query)" page applies to Excel 365, 2024 and 2021 (fetched). Power Query is in all Windows Excel 2016 or later (Microsoft Support, "Power Query data sources in Excel versions"; page title as fetched).
**Edge cases:** Blank cells become nulls and are dropped (from memory, unverified); headers must be text-like months, not dates you want to sort.
**Likely follow-ups:** 1) *Reverse?* Pivot Column (Q44). 2) *Does it fold on SQL?* Sources conflict; unverified.
**Common mistakes:** Unpivoting the key column too; leaving the Month column typed as text when sorting.

### Q26 ⭐⭐ 🟡 What are the different join kinds available in a Power Query merge?
**Asked at:** EY intern review (Glassdoor, reported Feb 2026, single report, search snippet only) mentions Merge vs Append; join kinds are an expected follow-up.
**What the interviewer is checking:** Do you know which rows each join keeps?
**Say this in the interview:** "There are seven kinds: inner, left outer, right outer, full outer, left anti, right anti and cross. I pick by asking which table's unmatched rows I still need."
**Explain simply:**
- Primary table = first table chosen; related = second.
- Inner: only matches. Left outer: all primary + matches. Right outer: all related + matches. Full outer: all rows from both. Left anti: primary rows with no match. Right anti: related rows with no match. Cross: every row paired with every row (Microsoft Support, "Merge queries (Power Query)").
- Conflict: Microsoft Support, "Merge queries (Power Query)" (fetched; applies to 365, 365 for Mac, 2024, 2021) says "The default join operation is an inner join". An earlier note said the fuzzy match page names Left Outer as default; that page returned 404 and could not be re-read. The preselected kind in today's dialog is Left Outer from memory, unverified, so always check it before clicking OK. The page lists exactly the seven kinds above.
- Matching columns must have the same data type.
**Example:** HR master (101-104) vs payroll (102-105).
**Sample sheet:** HR: 101 Asha, 102 Ravi, 103 Meena, 104 Karan. Payroll: 102 50, 103 48, 104 60, 105 45.
**Formula / Steps:** (Not run here.) Data > Get Data > Combine Queries > Merge > pick both tables and EmpID columns > choose Join Kind > OK > expand. M: `Table.NestedJoin(HR,{"EmpID"},Pay,{"EmpID"},"Pay",JoinKind.LeftOuter)`.
**Alternative:** Excel formulas such as XLOOKUP, but only for one lookup column at a time.
**Result:** pandas (run): left 4 rows (Asha's payroll value blank); right 4 rows (105 has no name); full outer 5 rows; inner 3 rows; left anti = 101 Asha; right anti = 105; cross = 16 rows.
**Version note:** Merge exists wherever Power Query does (2016+ Windows).
**Edge cases:** Duplicate keys multiply rows; trailing spaces stop matches.
**Likely follow-ups:** 1) *Merge vs Append?* Side-by-side vs stacked. 2) *Which for missing employees?* Left anti.
**Common mistakes:** Using inner join and silently losing unmatched employees.

### Q27 ⭐⭐ 🟡 How do you find employees present in the HR master list but missing from the payroll list using Power Query?
**Asked at:** commonly asked (no company-specific report found); a reconciliation scenario typical of MIS roles.
**What the interviewer is checking:** Do you know the Left Anti join?
**Say this in the interview:** "I merge HR master with payroll on EmployeeID using Left Anti. It returns only HR rows with no payroll match."
**Explain simply:**
- Left Anti = rows in the first table that have no partner in the second.
- Result is a ready-made exception list for payroll follow-up.
- Clean IDs first (Trim, same data type).
**Example:** 4 on the HR master, 3 paid; one unpaid.
**Sample sheet:** Same HR and Payroll data as Q26.
**Formula / Steps:** (Not run here.) 1) Load both tables as queries. 2) Home > Merge Queries > HR as primary, Payroll as secondary, select EmpID in both. 3) Join Kind: Left Anti (rows only in first). 4) OK. The result has an empty Payroll column; remove it. 5) Close & Load. M: `Table.NestedJoin(HR,{"EmpID"},Pay,{"EmpID"},"Pay",JoinKind.LeftAnti)`.
**Alternative:** Left Outer then filter the null column; or in-sheet `=COUNTIF(Payroll!A:A,A2)=0`.
**Result:** pandas (run): EmpID 101 Asha. The reverse (payroll only) via Right Anti: 105.
**Version note:** Join kinds are in Merge on all Power Query versions (see Q26).
**Edge cases:** IDs stored as text in one table and number in the other match nothing.
**Likely follow-ups:** 1) *Reverse check?* Right Anti. 2) *Refresh?* Data > Refresh All.
**Common mistakes:** Choosing Left Outer and forgetting to filter nulls.

### Q28 ⭐⭐ 🟡 What is the difference between Reference and Duplicate for a query?
**Asked at:** EY intern review (Glassdoor, Feb 2026, snippet only) reportedly included Reference vs Duplicate.
**What the interviewer is checking:** Do you know dependency vs independent copy?
**Say this in the interview:** "Reference makes a new query that starts from the output of the original, so changes upstream flow through. Duplicate copies all the steps into an independent query."
**Explain simply:**
- Reference: new query's Source step points at the original query. Edit the original, and both update. It also reads the source only once per refresh (from memory, unverified).
- Duplicate: full copy of the steps; later edits to one do not affect the other.
- Use Reference for branches from a cleaned base (e.g., Active and Left staff).
**Example:** Clean attendance once, then Reference it for a monthly summary and an absentee list.
**Formula / Steps:** (Not run here.) Right-click the query in the Queries pane (Data > Queries & Connections or the Editor pane) > Reference or Duplicate. In M, a Reference query is just `= CleanAttendance`.
**Alternative:** Copy-paste the query to get a Duplicate-like copy.
**Result:** Not applicable (no values).
**Version note:** Power Query 2016+ Windows; the commands are in the right-click menu (from memory, unverified).
**Edge cases:** Deleting or renaming the base query breaks the referenced one. Referencing a loaded query is fine.
**Likely follow-ups:** 1) *Which is safer to edit?* Duplicate. 2) *Which keeps one clean source?* Reference.
**Common mistakes:** Duplicating and then fixing the same cleaning step in five copies.

### Q29 ⭐⭐ 🟡 How do you handle errors in Power Query (for example Remove Errors, Replace Errors, try ... otherwise)?
**Asked at:** EY intern review (Glassdoor, Feb 2026, snippet only) reportedly mentions errors/nulls.
**What the interviewer is checking:** Can you stop a few bad cells from breaking a refresh?
**Say this in the interview:** "I first find why the error appears. Then I either Remove Errors, Replace Errors with a default, or wrap the step in try...otherwise so the refresh continues."
**Explain simply:**
- Error cell = a cell where a step failed, e.g. "N/A" converted to number. Different from null (blank).
- Remove Errors drops the whole row; Replace Errors keeps the row with a default.
- `try ... otherwise` is M's IF-ERROR.
**Example:** Salary column with text "N/A" and "#REF!".
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | EmpID | Salary |
| 2 | 1 | 42000 |
| 3 | 2 | N/A |
| 4 | 3 | 38500 |
| 5 | 4 | #REF! |

**Formula / Steps:** (Not run here.) Select column > Home > Remove Rows > Remove Errors; or Transform > Replace Values dropdown > Replace Errors. M: `Table.TransformColumns(Source,{{"Salary", each try Number.From(_) otherwise 0}})`.
**Alternative:** Custom column `= try [Salary]*1 otherwise null`.
**Result:** pandas analogue (run): converted values 42000, error, 38500, error. Remove Errors keeps 2 rows; replace with 0 gives 42000, 0, 38500, 0.
**Version note:** Power Query 2016+ Windows. Microsoft has a page "Handling data source errors (Power Query)" (seen in search results, not fetched).
**Edge cases:** Errors in a column you filter on can stop the preview; errors in unused columns still fail loads if loaded.
**Likely follow-ups:** 1) *Null vs error?* Null is empty, error is a failure. 2) *Keep errors?* Home > Keep Rows > Keep Errors to inspect.
**Common mistakes:** Removing errors silently and losing employees from the report.

### Q30 ⭐⭐ 🟡 What do you do when appending two tables whose column names do not match exactly?
**Asked at:** EY intern review (Glassdoor, Feb 2026, snippet only) mentions Merge vs Append; column mismatch is a common follow-up.
**What the interviewer is checking:** Do you know Append matches by column name, not position?
**Say this in the interview:** "Append lines up columns by name, so a mismatch creates extra columns full of nulls. I rename the columns in each query first so they match, then append."
**Explain simply:**
- Append = stack tables one under another.
- "Dept" vs "Department" become two columns, half empty.
- Fix before appending; do not fix after.
**Example:** Hyderabad file has Dept, Pune file has Department.
**Sample sheet:** Table1: EmpID 1,2; Dept HR, IT. Table2: EmpID 3,4; Department Sales, HR.
**Formula / Steps:** (Not run here.) 1) Open Table2 query > right-click header Department > Rename > Dept. 2) Home > Append Queries > Append Queries as New > pick both. M: `Table.Combine({T1,T2})`. Also `Table.RenameColumns(T2,{{"Department","Dept"}})`.
**Alternative:** Append first, then merge the two columns with Transform > Merge Columns, or Add Column > Conditional Column.
**Result:** pandas (run): without rename, columns EmpID, Dept, Department with nulls (4 rows, 3 columns); after rename, 4 rows with Dept HR, IT, Sales, HR.
**Version note:** Append is in Power Query on Excel 2016+ Windows.
**Edge cases:** Case differences count as different names; data types must also agree.
**Likely follow-ups:** 1) *Many files?* Folder combine (Q6). 2) *Extra column in one file?* It gets nulls in the other.
**Common mistakes:** Appending first and then wondering why Dept has blanks.

### Q31 ⭐⭐ 🟡 How do you reduce a table's columns and rows early in a query, and why does the order of steps matter?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you think about performance and clean steps?
**Say this in the interview:** "I remove unneeded columns and filter rows right after loading. Later steps then work on less data, and refresh is faster and easier to debug."
**Explain simply:**
- Choose Columns / Remove Other Columns keeps only what you need.
- Filter rows (Status = Active) near the top.
- Steps run in order; a later step cannot use a column you already removed.
- With databases, early filters can be pushed to the server (query folding, Q41). With CSV/Excel files, Microsoft says no folding, so less data still just means less processing.
**Example:** 100,000 payroll rows; you need Hyderabad active staff with EmpID and Salary.
**Sample sheet:** (EmpID, Office, Status, Salary): 1 Hyd Active 50; 2 Hyd Left 45; 3 Pune Active 40; 4 Hyd Active 60; 5 Blr Active 55; 6 Pune Left 42 (Notes column dropped by Choose Columns).
**Formula / Steps:** (Not run here.) Home > Choose Columns (or Remove Columns) > Filter Office > Filter Status. M: `Table.SelectRows(Cols, each [Office]="Hyd" and [Status]="Active")`.
**Alternative:** Filter first, then remove columns; same result.
**Result:** pandas (run): rows kept EmpID 1 and 4 (Salary 50 and 60), the same result whichever order you filter and remove columns.
**Version note:** All Power Query versions.
**Edge cases:** Do type changes after filtering; changing types on all columns early can add errors.
**Likely follow-ups:** 1) *Does order change the result?* Rarely, if later steps need a removed column. 2) *Sort?* Sort late (it is costly).
**Common mistakes:** Removing a column that a later merge needs; sorting 100,000 rows before filtering.

### Q32 ⭐⭐ 🟡 How do you create a measure in Power Pivot, and what is a simple example?
**Asked at:** commonly asked; Wipro/Deloitte DAX topics appear in repo notes (research/interview_processes.md, DAX in 5-7.5% of JDs).
**What the interviewer is checking:** Do you know a measure is a calculation that responds to the PivotTable?
**Say this in the interview:** "A measure is a named DAX formula, like Total Salary, that recalculates for whatever the PivotTable is showing. I create it from the Power Pivot calculation area or the Measures > New Measure command."
**Explain simply:**
- Measure = calculation done at report time, not stored per row.
- Microsoft: an explicit measure is one you write; it can be used by any PivotTable in the workbook. An implicit one is created when you drag a field into Values and works only in that PivotTable (Microsoft Support, "Measures in Power Pivot").
- Calculated columns (Q7) store a value per row instead.
**Example:** `Total Salary := SUM(Salary[Amount])`.
**Sample sheet:** Rows: HR 40+40, Sales 55+60+50, IT 70 (thousand).
**Formula / Steps:** (Not run here.) Power Pivot > Measures > New Measure (or PivotTable Analyze > Fields, Items & Sets > ... in some versions, from memory) > Name, formula `=SUM(Salary[Amount])` > OK. Microsoft's example formula: `=SUM('FactResellerSales'[SalesAmount])*1.06`.
**Alternative:** Type in the calculation area: `Total Salary:=SUM(...)`.
**Result:** pandas reproduction: HR 80, IT 70, Sales 165, total 315.
**Version note:** Power Pivot is in the Microsoft Support "Power Pivot - overview and learning" Applies-to list for Excel 365, 2024, 2021, 2019 and 2016. Edition-level availability (which Office SKUs include it) is not on that page: unverified. Check File > Options > Add-ins > COM Add-ins.
**Edge cases:** Measures do not appear as columns in tables; a KPI built from one cannot then be used in other calculations (Microsoft page).
**Likely follow-ups:** 1) *Implicit vs explicit?* See above. 2) *Where used?* Values area.
**Common mistakes:** Making a calculated column when a measure is needed.

### Q33 ⭐⭐ 🟡 What is DAX, and how is it different from an Excel formula?
**Asked at:** Wipro and Deloitte DAX topics noted in repo research (research/interview_processes.md); no first-hand report read.
**What the interviewer is checking:** Do you know DAX works on columns and tables, not cell addresses?
**Say this in the interview:** "DAX is Data Analysis Expressions, the formula language of Power Pivot and Power BI. It refers to table[column], not A2, and results change with filters in the PivotTable."
**Explain simply:**
- Excel formula: points at cells; result sits in that cell.
- DAX: points at columns; a measure is recalculated per PivotTable cell.
- Many names match Excel (SUM, IF, COUNT) but behave on whole columns; others are new (CALCULATE, RELATED, DISTINCTCOUNT).
- Context (row vs filter) decides the answer (Q54).
**Example:** Excel `=SUM(D2:D6)` is fixed; DAX `=SUM(Salary[Amount])` gives HR 80, IT 70, Sales 165 depending on the row.
**Formula / Steps:** (Not run here.) Microsoft's page shows DAX such as `=SUM('FactResellerSales'[SalesAmount])`.
**Alternative:** Calculated column in DAX: `=Salary[Amount]*1.1` (row by row).
**Result:** Reproduced in pandas (Q32): 80, 70, 165, total 315.
**Version note:** Power Pivot DAX: see Q32 note.
**Edge cases:** Some DAX works only in Power BI, not the Excel Data Model.
**Likely follow-ups:** 1) *Is it Excel-like?* Similar syntax, different logic. 2) *Where do I write it?* Power Pivot window or Measures dialog.
**Common mistakes:** Treating DAX as cell references.

### Q34 ⭐⭐ 🟡 What does the CALCULATE function do in DAX?
**Asked at:** Weekday Power BI prep guides (2025-26, snippet) list CALCULATE as frequent; Wipro/Deloitte DAX topics in repo notes.
**What the interviewer is checking:** Do you know it changes the filter context?
**Say this in the interview:** "CALCULATE evaluates an expression after I change the filters on it. For example, total salary for only people who left."
**Explain simply:**
- Syntax: `CALCULATE(expression, filter1, filter2...)`.
- It overrides or adds filters, then runs the expression.
- Often wraps SUM or COUNT; used for percent-of-total with ALL (Q51, Q53).
**Example:** Left-employee salary: `Left Salary = CALCULATE(SUM(F[Salary]), F[Status]="Left")`.
**Sample sheet:** Rows (EmpID, Dept, Status, Salary): 1 HR Active 40; 1 HR Active 40; 2 Sales Left 55; 3 Sales Active 60; 4 IT Active 70; 5 Sales Left 50.
**Formula / Steps:** (Not run here.) Measure: `=CALCULATE(SUM(F[Salary]), F[Status]="Left")`.
**Alternative:** `SUMX(FILTER(F, F[Status]="Left"), F[Salary])`.
**Result:** pandas (run): 105 (55 + 50).
**Version note:** Power Pivot DAX; see Q32 note.
**Edge cases:** Filter on a column overrides any existing filter on that same column in the PivotTable.
**Likely follow-ups:** 1) *CALCULATE with ALL?* Removes filters. 2) *Row context?* CALCULATE turns it into filter context.
**Common mistakes:** Forgetting the filter replaces the PivotTable's own filter on that column.

### Q35 ⭐⭐ 🟡 How do you count unique employees in Power Pivot (DISTINCTCOUNT), and why can a normal PivotTable not do this directly?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the difference between row count and unique count?
**Say this in the interview:** "I add a measure `=DISTINCTCOUNT(Table[EmpID])`. A normal PivotTable only counts rows; Distinct Count needs the Data Model."
**Explain simply:**
- Count = rows; Distinct Count = unique values.
- Microsoft lists DISTINCTCOUNT among the standard aggregations for implicit measures (Microsoft Support, "Measures in Power Pivot"). Distinct Count in Value Field Settings appears when the data is in the Data Model (from memory, unverified).
- Employees appearing in several months must be counted once.
**Example:** Monthly attendance has repeated EmpIDs.
**Sample sheet:** Same table as Q34.
**Formula / Steps:** (Not run here.) `=DISTINCTCOUNT(F[EmpID])`. Or tick "Add this data to the Data Model", then Value Field Settings > Distinct Count.
**Alternative:** Power Query Remove Duplicates; or 365 `=COUNTA(UNIQUE(A2:A7))` (UNIQUE not in LibreOffice, not run here).
**Result:** pandas (run): rows by Dept HR 2, IT 1, Sales 3; distinct employees HR 1, IT 1, Sales 3; total distinct 5.
**Version note:** Data Model needs Windows Excel 2016+ (see Q24).
**Edge cases:** Blank EmpIDs: DISTINCTCOUNT counts blank as one value; use DISTINCTCOUNTNOBLANK (from memory, unverified).
**Likely follow-ups:** 1) *Why distinct totals do not add up?* A person can appear in two departments. 2) *COUNTROWS?* Counts rows.
**Common mistakes:** Using Count and over-reporting headcount.

### Q36 ⭐⭐ 🟡 What is a star schema, and why is it recommended for a Data Model?
**Asked at:** Weekday and other Power BI prep guides list star schema (2025-26, snippet-level); less Excel-specific.
**What the interviewer is checking:** Can you design a tidy model with facts and dimensions?
**Say this in the interview:** "A star schema has one central fact table with the events, like attendance records, surrounded by small dimension tables like Employee, Department and Date. It keeps relationships simple one-to-many and measures easy."
**Explain simply:**
- Fact table: many rows, numbers (days, salary).
- Dimension table: one row per thing, descriptive columns, unique key.
- One-to-many from each dimension to the fact (Q23); no dimension-to-dimension chains.
- Benefits (from memory, unverified): faster, no double counting, simple filters.
**Example:** Fact_Attendance(EmpID, DateKey, Days) with Dim_Employee, Dim_Dept, Dim_Date.
**Formula / Steps:** (Not run here.) Power Pivot > Diagram View > drag key from fact to each dimension.
**Alternative:** One flat table (fine for small data; repeats text).
**Result:** pandas check (run): a unique dimension join keeps row count: 6 fact rows stay 6 rows after the join.
**Version note:** Design concept; Data Model per Q24.
**Edge cases:** Dimension keys must be unique; fact keys with no match show as "(Blank)".
**Likely follow-ups:** 1) *Snowflake?* Dimensions linked to other dimensions. 2) *Date table?* Q45.
**Common mistakes:** Importing one giant flat table and using VLOOKUP columns.

### Q37 ⭐⭐ 🟡 Why does a measure sometimes show the same value for every row in a PivotTable?
**Asked at:** commonly asked (no company-specific report found); a common Power Pivot troubleshooting question.
**What the interviewer is checking:** Do you understand relationships and filter context?
**Say this in the interview:** "Usually the row field comes from a table that has no relationship to the table the measure sums, so nothing filters it and every row shows the grand total. I fix the relationship."
**Explain simply:**
- A PivotTable row filters the measure only through relationships.
- No (or inactive) relationship: no filtering, same total everywhere.
- Other causes: measure uses ALL() or removes filters; fields from the wrong table; Microsoft says only one relationship between a pair of tables is active at a time (found in search snippet of relationships article, not confirmed).
**Example:** Dept names from the Dept table, salary from a Salary table not linked. Each dept shows 315.
**Formula / Steps:** (Not run here.) Power Pivot > Diagram View: create DeptID relationship; or Data > Relationships > Create.
**Alternative:** Use the Dept field from the same table as the numbers.
**Result:** pandas (run): linked: HR 80, IT 70, Sales 165; unlinked case displays 315 on every row.
**Version note:** Data Model Windows Excel 2016+.
**Edge cases:** Key data type mismatch or trailing spaces can break the link.
**Likely follow-ups:** 1) *Other cause?* ALL in the measure. 2) *Check?* Manage Relationships.
**Common mistakes:** Rebuilding the measure instead of checking relationships.

### Q38 ⭐ 🟢 How do you check what a query is doing from the Advanced Editor, and what is the M language?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know Power Query is code behind the clicks?
**Say this in the interview:** "M is the Power Query formula language. Every click creates a line of M, and I read it in the Advanced Editor."
**Explain simply:**
- Each Applied Step is one M line, in order (Microsoft Learn, "Understanding Query Evaluation and Query Folding in Power Query": M script is "a recipe").
- Open it: View tab > Advanced Editor, or Home > Query group > Advanced Editor (same page).
- Shape: `let Source = ..., Step2 = ... in Step2`.
- Step names with spaces appear as `#"Kept top rows"`.
**Example:** A cleaned attendance query: Source, Changed Type, Filtered Rows.
**Formula / Steps:** (Not run here.) Open the query > Advanced Editor > read top to bottom; the last line after `in` is the output.
**Alternative:** Click each Applied Step and read the formula bar.
**Result:** Not applicable.
**Version note:** Power Query 2016+ Windows.
**Edge cases:** Hand edits can break the visual steps.
**Likely follow-ups:** 1) *Case-sensitive?* Yes (from memory, unverified). 2) *Why edit?* Parameters and custom logic.
**Common mistakes:** Editing M without a backup copy.

### Q39 ⭐ 🟢 How do you pull data from a web page or a CSV file into Excel with Power Query?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you import external data repeatably?
**Say this in the interview:** "Data tab > Get Data > From File > From Text/CSV, or From Other Sources > From Web, preview, then Transform or Load."
**Explain simply:**
- CSV: choose the file, check delimiter and encoding, Transform Data.
- Web: paste URL, pick a detected table; works for HTML tables, not pages that need login.
- Both are saved as refreshable queries.
**Example:** Monthly attendance CSV from the biometric system.
**Formula / Steps:** (Not run here; menu names from memory, unverified because the Microsoft pages fetched did not list them.) 1) Data > Get Data > From File > From Text/CSV, or From Other Sources > From Web. 2) Select > Transform Data. 3) Home > Close & Load.
**Alternative:** Legacy Data > From Text (Legacy).
**Result:** Not applicable.
**Version note:** Get Data in Windows 2016+ and 365 (Microsoft Support, "Power Query data sources in Excel versions"; Mac via Get Data per the earlier source note).
**Edge cases:** Moved file path breaks refresh (Q48).
**Likely follow-ups:** 1) *Authentication?* Anonymous for public pages. 2) *Refresh?* Q4.
**Common mistakes:** Copy-pasting web tables instead of a query.

### Q40 ⭐ 🟢 What is the Power Query Editor "Query Settings" pane used for?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know where to rename, review and undo steps?
**Say this in the interview:** "Query Settings holds the query name and the Applied Steps list, where I review, rename, reorder or delete steps."
**Explain simply:**
- Properties: query Name, description, all properties.
- Applied Steps: ordered list; click a step to see data at that point (Microsoft Learn page above describes the Applied steps pane).
- Delete the X by a step to undo it.
**Example:** Delete a mistaken Filtered Rows step.
**Formula / Steps:** (Not run here.) Power Query Editor > View > Query Settings (toggle if hidden; from memory).
**Alternative:** Rename step by F2.
**Result:** Not applicable.
**Version note:** All Power Query versions.
**Edge cases:** Deleting an early step can break later ones.
**Likely follow-ups:** 1) *Reorder?* Drag; may break dependent steps. 2) *Rename query?* In Name box.
**Common mistakes:** Leaving the pane hidden and losing track of steps.

### Q41 ⭐ 🟡 What is query folding, and how can you tell whether a step folds?
**Asked at:** EY intern review (Glassdoor, Feb 2026, snippet only) reportedly included query folding.
**What the interviewer is checking:** Awareness that some work is pushed back to the data source.
**Say this in the interview:** "Query folding means Power Query translates my steps into the source's own language, such as SQL, so the database does the work. It does not happen with CSV or Excel file sources."
**Explain simply:**
- Folding translates supported steps into native queries; unsupported steps run in the Power Query engine (Microsoft Learn, "Understanding Query Evaluation and Query Folding in Power Query").
- Outcomes: full, partial or none.
- Databases (SQL Server, OData) commonly fold; "Sources without a query engine, such as CSV and Excel files, don't support query folding" (same page).
- How to check: step folding indicators and query plan are available only in Power Query Online (same page); otherwise right-click a step > View Native Query, which depends on the connector.
**Example:** Filtering 10 million SQL rows to Hyderabad: folded filter returns only the matching rows.
**Formula / Steps:** (Not run here.) Right-click a step > View Native Query: if greyed out, the step likely does not fold (greyed-out detail from memory, unverified).
**Alternative:** SQL Profiler / database logs (from memory).
**Result:** Not applicable.
**Version note:** Unpivot folding: neither the Microsoft Learn folding page nor the Support "Unpivot columns" page (both re-fetched in Wave C) mentions it; blog sources conflict, so unverified. Do not claim it either way.
**Edge cases:** Merging two different sources or adding an index column can stop folding (from memory, unverified).
**Likely follow-ups:** 1) *Does Excel file source fold?* No, per Microsoft. 2) *Order?* Put foldable steps first.
**Common mistakes:** Expecting folding on CSV.

### Q42 ⭐ 🟡 What is fuzzy matching in a Power Query merge, and which Excel versions support it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you join similar-but-not-identical text, and do you know version limits?
**Say this in the interview:** "Fuzzy matching joins text values that are similar, like Hyderabad and Hydrabad, using a similarity score. It is in Microsoft 365 but not in 2019 perpetual."
**Explain simply:**
- Only for merges on text columns; uses Jaccard similarity; default threshold 0.80 (0 matches everything, 1 exact only) (Microsoft Support, "Create a fuzzy match (Power Query)", applies to Excel for Microsoft 365).
- Options: ignore case, maximum matches, transformation table (From/To mapping like Microsoft/MSFT).
- Version: "fuzzy merge is supported in Microsoft 365, but not in 2019 perpetual" (Microsoft Support, "Power Query data sources in Excel versions"). Excel 2016 is not stated on that page (re-fetched 2026-10-22); it only adds that "More features were added to 2019 perpetual than were available in 2016 perpetual", which suggests 2016 lacks it but does not say so: unverified.
**Example:** Office names typed differently in two HR files.
**Formula / Steps:** (Not run here.) Merge Queries > pick text columns > tick "Use fuzzy matching to perform the merge" > Fuzzy matching options > Similarity Threshold > OK.
**Alternative:** Clean names with Replace Values or a transformation table.
**Result:** Illustration only, not Microsoft's exact algorithm: a two-letter-piece Jaccard in pandas script gives Hyderabad vs Hydrabad 0.67, Bangalore vs Bengaluru 0.23, Mumbai vs Delhi 0.0 (so a 0.80 threshold would miss the first).
**Version note:** As above.
**Edge cases:** Numbers and dates not supported; false matches at low thresholds.
**Likely follow-ups:** 1) *Threshold?* Test several and review. 2) *Fix known variants?* Transformation table.
**Common mistakes:** Lowering the threshold to 0 and matching everything.

### Q43 ⭐ 🟡 How do you unpivot only the selected columns versus the other columns, and what is the difference?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know how each command behaves when new columns appear after refresh?
**Say this in the interview:** "Unpivot Other Columns keeps the columns I select as is and unpivots everything else, including new columns later. Unpivot Only Selected Columns unpivots just the ones I chose, so new columns stay untouched."
**Explain simply:**
- Microsoft: Unpivot Other Columns unpivots the unselected columns; "new columns added during a refresh operation are also unpivoted." Unpivot Only Selected Columns is for when you do not know how many columns the source has and want selected columns to stay unpivoted after a refresh (Microsoft Support, "Unpivot columns (Power Query)").
- Plain Unpivot Columns: unpivots the columns you select.
- Choose Other when new months will keep being added; choose Selected when extra columns (e.g., Notes) must remain.
**Example:** Sheet gets a new Apr column next month.
**Sample sheet:** Emp, Jan, Feb, Mar, Apr (Asha 22,19,21,20; Ravi 20,21,22,18).
**Formula / Steps:** (Not run here.) Select Emp > Transform > Unpivot Columns dropdown > Unpivot Other Columns. Or select Jan:Mar > Unpivot Only Selected Columns. M: `Table.UnpivotOtherColumns(...)` vs `Table.Unpivot(Source,{"Jan","Feb","Mar"},"Month","Days")`.
**Alternative:** Rebuild after each new month (not recommended).
**Result:** pandas (run): with Apr present, Other-columns style gives 8 rows including Apr (Apr 2 rows); selected Jan:Mar gives 6 rows and Apr stays a column.
**Version note:** Power Query 2016+ Windows.
**Edge cases:** If Emp is renamed, Other still works; Selected fails if a selected column is removed (Q63).
**Likely follow-ups:** 1) *Folding?* Unverified. 2) *Pivot back?* Q44.
**Common mistakes:** Selecting the month columns and using "Unpivot Other Columns" (does the opposite).

### Q44 ⭐ 🟡 How do you pivot a column in Power Query (the reverse of unpivot)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that Pivot Column turns row values into column headings, and that it needs an aggregation choice?
**Say this in the interview:** "I select the column whose values should become headings, say Month, go to Transform > Pivot Column, choose the Values column, for example Days, and pick an aggregation such as Sum. If each employee-month pair appears once I can use 'Don't aggregate', but Sum is safer."
**Explain simply:**
- *Pivot* means turning the unique values of one column (Jan, Feb, Mar) into separate column headings. Unpivot does the opposite.
- You must say which column supplies the numbers that fill the new grid.
- Aggregation options are Don't aggregate, Count (all), Count (not blank), Minimum, Maximum, Median, Sum, Average (Microsoft Support, "Pivot columns (Power Query)").
- "Don't aggregate" fails with "There were too many elements in the enumeration" if one cell would receive two values, often only after a later refresh (same page).
**Example:** A long attendance list has one row per employee per month. Pivoting Month gives one row per employee with Jan, Feb, Mar columns, which is easier to read in a report.
**Sample sheet (input, long format):**

| | A | B | C |
|---|---|---|---|
| 1 | Emp | Month | Days |
| 2 | E1 | Jan | 22 |
| 3 | E1 | Feb | 20 |
| 4 | E1 | Mar | 21 |
| 5 | E2 | Jan | 18 |
| 6 | E2 | Feb | 19 |
| 7 | E2 | Mar | 22 |

**Formula / Steps (not run here, Power Query cannot run in this environment):**
1. Data > Get Data > From Table/Range, then Power Query Editor opens.
2. Select the Month column.
3. Transform tab > Pivot Column.
4. Values Column: Days. Advanced options > Aggregate Value Function: Sum. OK.
M code (not run here): `= Table.Pivot(Source, List.Distinct(Source[Month]), "Month", "Days", List.Sum)`
**Alternative:** A PivotTable on the same data gives the same grid, but it is a report, not a cleaned table you can feed to later steps.
**Result:** Reproduced with pandas (the Power Query step itself was not run here): E1 gives Jan 22, Feb 20, Mar 21; E2 gives Jan 18, Feb 19, Mar 22. If a duplicate row (E1, Jan, 1) is added, "Don't aggregate" would fail, while Sum gives E1 Jan = 23.
**Version note:** Power Query is in Excel 2016 and later for Windows and in Microsoft 365 (Microsoft Support, "Power Query data sources in Excel versions"). The Pivot Column steps above are from the Support page quoted in Explain simply.
**Edge cases:** Duplicates per cell (use an aggregation); a month with no row produces null; new months appearing later become new columns, which can break downstream steps that expect fixed columns.
**Likely follow-ups:** 1) *Why not just use a PivotTable?* Pivot Column changes the data shape inside the query, so later steps and loads see it. 2) *Which aggregation for text?* Don't aggregate or Count.
**Common mistakes:** Choosing "Don't aggregate" on data with duplicates; pivoting a column with hundreds of unique values and creating hundreds of columns.

### Q45 ⭐ 🟡 How do you add a Date table to the Data Model, and why is one needed for time intelligence?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that DAX time functions need a proper calendar table?
**Say this in the interview:** "I build a calendar table with one row for every date across the full years of my data, load it to the Data Model, link its Date column to the date column in my fact table, and mark it as the date table. Then functions like TOTALYTD work correctly."
**Explain simply:**
- A *Date table* is a list of consecutive dates with helper columns (Year, Month, Quarter).
- Microsoft says a date table is essential for working effectively with dates, and that time-intelligence DAX functions work across days, months, quarters and years (Microsoft Support, "Dates in Power Pivot"). That page does not list the exact requirements.
- From memory, unverified here: the Date column must hold unique dates with no gaps, and you should mark it as a date table (Power Pivot tab > Design > Mark as Date Table).
- Without it, a gap in your data (a month with no joiners) makes year-to-date and previous-period measures wrong.
**Example:** Joiners are on 15 Jan, 10 Feb and 25 Feb 2025. A 365-row calendar for 2025 lets you show March with 0 joiners instead of omitting it.
**Sample sheet (calendar, first rows):**

| | A | B | C |
|---|---|---|---|
| 1 | Date | Year | Month |
| 2 | 01-Jan-2025 | 2025 | Jan |
| 3 | 02-Jan-2025 | 2025 | Jan |
| 4 | 03-Jan-2025 | 2025 | Jan |

**Formula / Steps (not run here):**
1. Create a calendar: in Power Query, `= List.Dates(#date(2025,1,1), 365, #duration(1,0,0,0))`, convert to table, add Year and Month columns (from memory).
2. Close & Load To... > Add this data to the Data Model.
3. Power Pivot tab > Manage > Diagram View, drag Calendar[Date] onto Joiners[JoinDate].
4. Mark as Date Table (from memory, unverified).
**Alternative:** Excel formulas `=A2+1` filled down in a normal table, then Add to Data Model; or use a date table already supplied by the source (Microsoft Support page says one is often imported).
**Result:** pandas check (Power Query not run here): a 2025 calendar has 365 rows, 01-Jan to 31-Dec, all unique; joiners per month: Jan 1, Feb 2.
**Version note:** Page applies to Excel 2016 and later and Microsoft 365 per the Support page; I did not confirm the Mark as Date Table menu name in each version.
**Edge cases:** Time stamps in the date column break one-row-per-day uniqueness; fiscal years (April to March) need a custom Fiscal column.
**Likely follow-ups:** 1) *Can I use the fact table's dates?* Not reliably, gaps break time intelligence. 2) *How many date tables?* Normally one.
**Common mistakes:** Calendar covering only dates present in data; leaving the relationship out.

### Q46 ⭐ 🟡 What is the difference between Power Query "Merge" and an Excel VLOOKUP or XLOOKUP?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know a Merge is a repeatable database-style join, while lookups are cell formulas?
**Say this in the interview:** "VLOOKUP fetches one value per cell and returns only the first match. A Merge joins whole tables, can keep all matches, shows unmatched rows, and replays itself on refresh without formulas in thousands of cells."
**Explain simply:**
- *Merge* joins two tables on a key column (like EmpID); you choose a join kind (left outer, inner and so on).
- VLOOKUP/XLOOKUP return the first match only; a Merge can return every match as extra rows.
- A Merge handles big tables faster and leaves the source untouched; lookups recalculate every time the workbook does.
- A lookup is better for a quick, small, one-off check in the sheet.
**Example:** HR master has E1 to E4; payroll has E2 twice (two salary revisions) and E5. VLOOKUP gives E2 only the first salary. A left Merge returns both E2 rows.
**Sample sheet (lookup layout):**

| | A | B | C | E | F |
|---|---|---|---|---|---|
| 1 | EmpID | Name | Salary | PayEmp | Salary |
| 2 | E1 | Asha | | E1 | 50000 |
| 3 | E2 | Ravi | | E2 | 60000 |
| 4 | E3 | Meena | | E2 | 61000 |
| 5 | E4 | Karan | | E5 | 70000 |

**Formula / Steps:** `C2: =IFERROR(VLOOKUP(A2,$E$2:$F$5,2,FALSE),"missing")`, fill down. Merge route (not run here): Data > Get Data > Combine Queries > Merge, select EmpID in both, Join Kind: Left Outer, expand Salary.
**Alternative:** `=XLOOKUP(A2,E2:E5,F2:F5,"missing")` in 365/2021 (not run here, LibreOffice 24.2 lacks XLOOKUP).
**Result:** VLOOKUP run in LibreOffice: C2 50000, C3 60000, C4 missing, C5 missing. pandas left merge (not Power Query, so the merge itself is "not run here"): E1 50000; E2 60000 and E2 61000 (two rows); E3 and E4 blank.
**Version note:** XLOOKUP is treated as 2021/365 only: Microsoft's XLOOKUP page says it is not available in Excel 2016 and 2019 while its Applies-to list names them (conflict; not re-fetched here); Power Query is in Excel 2016+ for Windows (Microsoft Support, "Power Query data sources in Excel versions").
**Edge cases:** Text vs number keys do not match in either tool; trailing spaces break both. Exact-match VLOOKUP gives the same four values in Excel as in LibreOffice (from memory, unverified).
**Likely follow-ups:** 1) *Which is faster on 500k rows?* Merge, from experience (unverified). 2) *Does Merge auto-update?* After refresh.
**Common mistakes:** Expecting VLOOKUP to show all matches; forgetting a left merge multiplies rows when keys repeat.

### Q47 ⭐ 🟡 How do you stop a Power Query refresh from breaking when a column is renamed or removed at the source?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you build queries that survive messy sources?
**Say this in the interview:** "I can't fully stop it, because queries rely on column names. I reduce the risk by asking the owner to keep headers fixed, using Remove Columns instead of Choose Columns where suitable, and for must-have columns I add a safe step that checks the header list."
**Explain simply:**
- Microsoft notes that queries rely on table and column names in almost every step, so renaming causes refresh problems (Microsoft Support, "Handling data source errors (Power Query)").
- The same page says removing "other columns" can let new source columns slip through undetected, while removing a named column avoids this.
- Make the source a named Excel Table and keep headings locked.
- A defensive pattern in M (from memory, not run here) is `Table.SelectColumns(Source, {"EmpID","Dept"}, MissingField.UseNull)`, which gives nulls instead of an error.
**Example:** The HR export renames "Dept" to "Department". Your step on "Dept" fails. With MissingField.UseNull the refresh finishes but Dept is all null, so you add a check that counts nulls.
**Formula / Steps (not run here):** Home > Choose Columns keeps listed columns; edit the generated step in the formula bar or Advanced Editor to add `, MissingField.UseNull`.
**Alternative:** Rename to the new header inside the query using `Table.RenameColumns(Source, {{"Department","Dept"}}, MissingField.Ignore)` to accept both spellings.
**Result:** pandas analogy (Power Query not run here): selecting ["EmpID","Dept"] after the rename raises KeyError "['Dept'] not in index"; `reindex(columns=['EmpID','Dept'])` returns Dept as NaN.
**Version note:** MissingField options exist in M generally; I did not fetch a page confirming them, so treat as from memory, unverified.
**Edge cases:** Silent nulls can be worse than a loud error; add a validation count.
**Likely follow-ups:** 1) *Why not hard fail?* Sometimes you want that. 2) *Can I auto-detect columns?* Yes, with `Table.ColumnNames`.
**Common mistakes:** Hard-typing every column name; not telling the source owner about the dependency.

### Q48 ⭐ 🟡 How do you share a workbook with Power Query connections to a local file path with colleagues without refresh errors?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand that C:\ paths only exist on your machine?
**Say this in the interview:** "I move the source to a shared location everyone can open, such as a SharePoint or OneDrive folder or a network drive, and point the query at it through a parameter, so a colleague changes one cell or value instead of editing the query."
**Explain simply:**
- A path like `C:\Users\Priya\Attendance.xlsx` fails on another PC.
- A *parameter* is a stored value reused across steps, such as a file path or server name, kept separately from the data queries (Microsoft Support, "Create a parameter query (Power Query)").
- On that page, you point the Source step at the parameter via Edit Settings > File path > Parameter. Changing the Current Value then points the query to a new location.
- Colleagues also need permission to the file; credentials are stored per user.
**Example:** Payroll workbook reads `\\hrshare\attendance\`. A colleague in Pune opens it, sets the parameter to their mapped path, and presses Data > Refresh All.
**Formula / Steps (not run here):** Home > Manage Parameters > New Parameter (name FilePath, Text). Source step > gear icon > File path: Parameter > FilePath. Close & Load.
**Alternative:** Keep a path cell in an Excel table, load it as a query, and reference it (Support page shows loading a cell value as a query).
**Result:** Not run here (no workbook sharing possible). Behaviour: refresh fails on a machine where the old path does not exist; works after the parameter points to a reachable path.
**Version note:** Power Query is in Excel 2016+ for Windows and Microsoft 365; Excel for Mac supports Power Query in 365 and Excel for Android and iOS does not (Microsoft Support, "Power Query data sources in Excel versions").
**Edge cases:** Mapped drive letters differ between users (a UNC path or SharePoint URL is safer); privacy-level prompts may appear for each new user.
**Likely follow-ups:** 1) *Can the data be removed from the file?* Yes, via connection properties (not verified here). 2) *Why credentials errors?* Each user must sign in.
**Common mistakes:** Emailing the workbook with a personal path; hardcoding paths in several queries.

### Q49 ⭐ 🟡 What is a Power Query parameter, and how would you use one (for example a folder path or a cut-off date)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know how to avoid hard-coded values?
**Say this in the interview:** "A parameter is a named value, like CutOffDate or FolderPath, that I create once and reuse in query steps, so I change the value in one place and refresh."
**Explain simply:**
- Parameters can be used in any query step and set things like a file path or server name, not only filters. They do not prompt for input; you edit the value (Microsoft Support, "Create a parameter query (Power Query)").
- Created in Home > Manage Parameters > New Parameter with Name, Type, Suggested Values and Current Value.
- In Filter Rows, click the button left of the Value box and choose the parameter (same page).
- Update the Current Value, Close & Load, then Data > Refresh All.
**Example:** Headcount as at a cut-off date. With CutOffDate = 31-Mar-2025, employees E1 and E2 (joined 1-Dec-2024 and 1-Feb-2025) are kept; E3 (1-Apr-2025) is dropped. Change to 30-Jun-2025 and all three stay.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | Emp | JoinDate |
| 2 | E1 | 01-Dec-2024 |
| 3 | E2 | 01-Feb-2025 |
| 4 | E3 | 01-Apr-2025 |

**Formula / Steps (not run here):** M filter step using the parameter: `= Table.SelectRows(Source, each [JoinDate] <= CutOffDate)`.
**Alternative:** Load a cell from an Excel table as a query and reference it, so non-technical users change a cell (Support page).
**Result:** pandas reproduction (Power Query not run here): cut-off 31-Mar-2025 keeps E1, E2; 30-Jun-2025 keeps E1, E2, E3.
**Version note:** Page cited covers Power Query in Excel; I did not confirm menu names for every version.
**Edge cases:** Parameter type must be Date, otherwise comparison fails; no value means Required parameters error.
**Likely follow-ups:** 1) *Parameter vs variable?* Parameter is a query-level named value. 2) *Can a parameter feed a folder path?* Yes.
**Common mistakes:** Typing the date as text; forgetting to refresh after changing it.

### Q50 ⭐ 🟡 How do you calculate year-to-date headcount or salary cost with a time-intelligence function such as TOTALYTD or DATESYTD?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know DAX time intelligence and the Date table prerequisite?
**Say this in the interview:** "I write a measure `Salary YTD = TOTALYTD(SUM(Payroll[Cost]), Calendar[Date])`, with a proper Date table related to the payroll dates. In a PivotTable by month it shows a running total from 1 January."
**Explain simply:**
- *DAX* is the formula language of Power Pivot; *time intelligence* functions work on periods like year-to-date.
- TOTALYTD adds the values from the start of the year up to each month's last date.
- The Date table is required; see Q45 (Microsoft Support, "Dates in Power Pivot").
- For headcount, a year-to-date total of a snapshot is wrong; use the latest value instead (from memory).
**Example:** Monthly salary cost (lakhs) Jan to Jun: 100, 110, 105, 120, 115, 130. YTD by month: 100, 210, 315, 435, 550, 680.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | Month | Cost |
| 2 | Jan | 100 |
| 3 | Feb | 110 |
| 4 | Mar | 105 |
| 5 | Apr | 120 |
| 6 | May | 115 |
| 7 | Jun | 130 |

**Formula / Steps (DAX not run here):** Power Pivot > Measures > New Measure: `Salary YTD := TOTALYTD(SUM(Payroll[Cost]), 'Calendar'[Date])`. Add to PivotTable Values with Month in Rows.
**Alternative:** `CALCULATE(SUM(Payroll[Cost]), DATESYTD('Calendar'[Date]))`, same result (from memory).
**Result:** pandas cumulative sum (DAX not run here): 100, 210, 315, 435, 550, 680. Excel check on a normal sheet would be `=SUM($B$2:B2)`.
**Version note:** Power Pivot is listed for Excel 2016 to 2024 and Microsoft 365 (Microsoft Support, "Power Pivot: Powerful data analysis and data modeling in Excel"); the edition limits are unverified, see Q19 note.
**Edge cases:** Fiscal year ends other than December need the year-end date argument (from memory); without a Date table the measure errors or misleads.
**Likely follow-ups:** 1) *Why not a running SUM column?* A measure respects slicers. 2) *Previous year?* SAMEPERIODLASTYEAR.
**Common mistakes:** Using the fact table's date column instead of the Date table; summing headcount snapshots.

### Q51 ⭐ 🟡 How do you calculate each department's share of total headcount as a percentage in Power Pivot?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know to divide a filtered count by a count with filters removed?
**Say this in the interview:** "I create a headcount measure, then a second measure that divides it by the same count with ALL on the department column, using DIVIDE so there is no divide-by-zero error."
**Explain simply:**
- Row for HR shows HR's count only (filter context, see Q54). Dividing by the grand total needs the department filter removed.
- ALL removes filters from the column you give it (see Q53).
- DIVIDE returns blank instead of an error when the denominator is zero.
- Format the measure as Percentage.
**Example:** 10 employees: HR 3, IT 5, Sales 2. Shares are 30%, 50%, 20%.
**Sample sheet:**

| | A | B |
|---|---|---|
| 1 | Dept | Headcount |
| 2 | HR | 3 |
| 3 | IT | 5 |
| 4 | Sales | 2 |

**Formula / Steps (DAX not run here):**
`Headcount := COUNTROWS(Employees)`
`Share % := DIVIDE([Headcount], CALCULATE([Headcount], ALL(Employees[Dept])))`
**Alternative:** In a normal PivotTable: Show Values As > % of Column Total (no DAX needed, but it will not respect measure-level logic).
**Result:** pandas (DAX not run here): HR 30.0, IT 50.0, Sales 20.0, total 100.
**Version note:** Power Pivot DAX needs an Excel with the Data Model (see Q19 and the Microsoft Support Power Pivot page); Show Values As works in all desktop versions (from memory, unverified).
**Edge cases:** With a Dept slicer active, ALL ignores the slicer only if you use ALL, not ALLSELECTED; blank departments appear as their own row.
**Likely follow-ups:** 1) *Why DIVIDE?* Safe division. 2) *Share within a location?* Use ALLEXCEPT.
**Common mistakes:** Dividing by a column sum instead of a measure; forgetting percent formatting.

### Q52 ⭐ 🟡 What is the difference between SUM and SUMX in DAX?
**Asked at:** the Part 7 sources file notes SUMX among DAX topics in repo interview research for Wipro/Deloitte (not independently verified here).
**What the interviewer is checking:** Do you understand row-by-row calculation (iterator) versus a plain column total?
**Say this in the interview:** "SUM adds one column. SUMX goes row by row, calculates an expression for each row, then adds the results, so I use it when I need hours times rate per person before totalling."
**Explain simply:**
- SUM(column) is a shortcut that adds up one column.
- SUMX(table, expression) is an *iterator*: it evaluates the expression for every row of the table, then sums.
- Needed when the answer is a product or condition per row, such as Hours x Rate.
- Adding two column totals and multiplying them is wrong.
**Example:** E1 160 hrs at 200, E2 150 at 300, E3 170 at 250. Right total pay = 32,000 + 45,000 + 42,500 = 119,500.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Emp | Hours | Rate |
| 2 | E1 | 160 | 200 |
| 3 | E2 | 150 | 300 |
| 4 | E3 | 170 | 250 |

**Formula / Steps (DAX not run here):** `Total Pay := SUMX(Pay, Pay[Hours] * Pay[Rate])`. Wrong version: `SUM(Pay[Hours]) * SUM(Pay[Rate])`.
**Alternative:** Add a calculated column `Pay = Hours*Rate` then SUM it, but that stores a column in the model (see Q7 about columns vs measures).
**Result:** pandas (DAX not run here): SUM hours 480, SUM rate 750, wrong product 360,000, SUMX 119,500. Excel equivalent `=SUMPRODUCT(B2:B4,C2:C4)` run in LibreOffice 24.2: 119500; `=SUM(B2:B4)*SUM(C2:C4)` gave 360000 (both run here).
**Version note:** Same as other Power Pivot DAX; function details from memory, unverified.
**Edge cases:** SUMX over a filtered table respects filters; blanks multiply as zero.
**Likely follow-ups:** 1) *Other iterators?* AVERAGEX, COUNTX. 2) *Is SUM an iterator?* Internally it behaves like SUMX over one column (from memory).
**Common mistakes:** Multiplying totals; using SUMX when a plain SUM would do.

### Q53 ⭐ 🟡 What is the difference between ALL and ALLEXCEPT in DAX?
**Asked at:** the Part 7 sources file notes ALL/ALLEXCEPT among DAX topics in repo research for Wipro/Deloitte (not independently verified here).
**What the interviewer is checking:** Do you understand removing filters, fully or partly?
**Say this in the interview:** "ALL removes filters from a table or columns so I get a grand total. ALLEXCEPT removes all filters except the columns I name, so I get a subtotal within, say, the department."
**Explain simply:**
- Inside CALCULATE, ALL(Employees) or ALL(Employees[Dept]) clears the filter so each row sees the overall number.
- ALLEXCEPT(Employees, Employees[Dept]) clears every filter on the table except Dept.
- ALL is for percent of grand total; ALLEXCEPT is for percent within a group.
- Both are filter modifiers, not calculations on their own.
**Example:** 6 employees: HR Hyd 1, HR Blr 1, IT Hyd 2, IT Blr 1, Sales Hyd 1. For IT Hyd, share of all = 2/6 = 33.3%; share within IT = 2/3 = 66.7%.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Dept | Loc | Headcount |
| 2 | HR | Blr | 1 |
| 3 | HR | Hyd | 1 |
| 4 | IT | Blr | 1 |
| 5 | IT | Hyd | 2 |
| 6 | Sales | Hyd | 1 |

**Formula / Steps (DAX not run here):**
`% of total := DIVIDE([Headcount], CALCULATE([Headcount], ALL(Employees)))`
`% of dept := DIVIDE([Headcount], CALCULATE([Headcount], ALLEXCEPT(Employees, Employees[Dept])))`
**Alternative:** ALLSELECTED keeps outside slicer filters while removing row filters (from memory).
**Result:** pandas (DAX not run here): % of total 16.7, 16.7, 16.7, 33.3, 16.7; % of dept 50.0, 50.0, 33.3, 66.7, 100.0.
**Version note:** Power Pivot DAX; function semantics from memory, unverified.
**Edge cases:** ALLEXCEPT also removes filters from other tables' columns only if they filter via relationships on that table (from memory); slicers on Loc are ignored by ALLEXCEPT on Dept.
**Likely follow-ups:** 1) *ALL vs REMOVEFILTERS?* Same effect inside CALCULATE (from memory). 2) *Why Data Model?* Needed for DAX.
**Common mistakes:** Using ALL when a subtotal is wanted; forgetting that slicers can be removed too.

### Q54 ⭐ 🟡 What is row context versus filter context?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you grasp the two ways DAX decides which rows to use?
**Say this in the interview:** "Row context is 'the current row' inside a calculated column or iterator. Filter context is the set of filters from the PivotTable rows, columns and slicers that decide which rows a measure sees."
**Explain simply:**
- *Row context*: a calculated column computes one row at a time, so `Base * Bonus%` uses that row's values.
- *Filter context*: a measure like SUM(Salary) in a PivotTable row labelled HR only sees HR rows.
- CALCULATE changes filter context; iterators like SUMX create row context.
- A measure sums fresh each time; a calculated column is computed once and stored (see Q7).
**Example:** Bonus = Base x Bonus%. E1 5,000, E2 6,000, E3 16,000, E4 18,000 (row context). A measure summing the Bonus column gives HR 11,000, IT 34,000, total 45,000 (filter context).
**Sample sheet:**

| | A | B | C | D |
|---|---|---|---|---|
| 1 | Emp | Dept | Base | Bonus% |
| 2 | E1 | HR | 50000 | 10% |
| 3 | E2 | HR | 60000 | 10% |
| 4 | E3 | IT | 80000 | 20% |
| 5 | E4 | IT | 90000 | 20% |

**Formula / Steps (DAX not run here):** Calculated column: `Bonus = Employees[Base] * Employees[Bonus%]`. Measure: `Total Bonus := SUM(Employees[Bonus])`.
**Alternative:** Do it in one measure: `SUMX(Employees, Employees[Base]*Employees[Bonus%])`.
**Result:** pandas (DAX not run here): row-level bonus 5000, 6000, 16000, 18000; by Dept HR 11000, IT 34000; total 45000.
**Version note:** DAX concept; from memory, unverified against a Microsoft page.
**Edge cases:** Row context does not filter other tables unless a relationship and RELATED are used.
**Likely follow-ups:** 1) *Does row context become filter context?* Only via context transition, such as CALCULATE (from memory). 2) *Which makes a PivotTable total?* Filter context.
**Common mistakes:** Expecting a column reference inside a measure to know "the current row".

### Q55 ⭐ 🟡 How do you create a KPI or a hierarchy (Department > Team) in Power Pivot?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know these are Power Pivot extras beyond ordinary PivotTables?
**Say this in the interview:** "A KPI compares a base measure with a target and shows a status icon. I right-click the measure in the Calculation Area, choose Create KPI, set the target and thresholds. A hierarchy groups columns, like Department then Team, so users can drill down."
**Explain simply:**
- Excel has no KPIs or hierarchies of its own; Power Pivot lets you create KPIs for PivotTables and define hierarchies for use across the workbook (Microsoft Support, "Power Pivot: Powerful data analysis and data modeling in Excel").
- KPI steps (Microsoft Support, "Key Performance Indicators (KPIs) in Power Pivot"): in Data View, find the table with the base measure; in the Calculation Area right-click the calculated field > Create KPI; define the target (a measure or an absolute value); drag the status thresholds; choose icon style.
- Hierarchy: in Diagram View, select the columns, right-click > Create Hierarchy, or drag them into one (from memory, not on a page I fetched).
**Example:** Target monthly attrition 2%. Actual 2.01%. The status shows amber or red depending on your thresholds (for example green at or below 100% of target; amber to 110%).
**Sample sheet:** Not meaningful (feature steps, no cell grid).
**Formula / Steps (not run here):** KPI base: `Attrition % := DIVIDE([Exits], [Avg Headcount])`. Create KPI, absolute target 0.02, set thresholds, icon style. Then add KPI Value, Target and Status to a PivotTable.
**Alternative:** Use Conditional Formatting icon sets on PivotTable cells, simpler but not connected to a model KPI.
**Result:** Not run here. Arithmetic check: 2.01 / 2 = 1.005, so actual is 100.5% of target.
**Version note:** The fetched Power Pivot page lists Excel 2016, 2019, 2021, 2024 and Microsoft 365 under Applies To. Whether KPIs and hierarchies need a specific edition or Microsoft 365 was not confirmed on a fetched page, so unverified.
**Edge cases:** Hierarchy levels must come from the same table; a KPI needs a measure, not a plain column.
**Likely follow-ups:** 1) *KPI vs conditional formatting?* KPI lives in the model. 2) *Can hierarchies be reused?* Yes, in any PivotTable on the model.
**Common mistakes:** Setting thresholds backwards (for attrition lower is better).

### Q56 ⭐ 🟡 How do you use slicers to control several PivotTables built on the same Data Model?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know slicer connections and the same-source rule?
**Say this in the interview:** "I insert one slicer, for example Department, and connect it to every PivotTable through Slicer Settings or Report Connections. All of them must use the same data source, which is true when they sit on the same Data Model."
**Explain simply:**
- A *slicer* is a clickable filter button panel.
- Microsoft states slicers can only be connected to PivotTables that share the same data source (Microsoft Support, "Use slicers to filter data").
- Steps from that page: click the slicer; Slicer tab > Slicer Settings; under PivotTable Connections tick each PivotTable; OK. Older versions: Report Connections.
- Build the other PivotTables from the same Data Model first.
**Example:** One report with a headcount PivotTable and a salary PivotTable. Clicking IT in the slicer: headcount by location Hyd 2, Blr 1 and IT salary total 240.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Dept | Loc | Salary |
| 2 | HR | Hyd | 50 |
| 3 | HR | Blr | 60 |
| 4 | IT | Hyd | 80 |
| 5 | IT | Hyd | 90 |
| 6 | IT | Blr | 70 |

**Formula / Steps (not run here):** 1) PivotTable Analyze > Insert Slicer > Dept. 2) Select slicer > Slicer tab > Slicer Settings > tick PivotTable 1 and 2 > OK.
**Alternative:** A Timeline for dates, or a Report Filter per PivotTable (not synchronised).
**Result:** pandas check (slicer not run here): filter Dept = IT gives Hyd 2, Blr 1 headcount and salary 240.
**Version note:** Menu name differs by version (Slicer Settings vs Report Connections) per the cited page.
**Edge cases:** PivotTables built from separate ranges will not appear in the connection list.
**Likely follow-ups:** 1) *Why not listed?* Different source. 2) *Slicer vs filter?* Slicer is visible and shared.
**Common mistakes:** Making each PivotTable from a different copy of the table.

### Q57 ⭐ 🔴 How would you build a refreshable monthly attrition report using Power Query, a Data Model and a PivotTable?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you design an end-to-end, repeatable HR report?
**Say this in the interview:** "Power Query cleans the employee master and exit file, I load them with a Calendar table to the Data Model, write measures for exits, average headcount and attrition %, and put them in a PivotTable with Month and Department. Each month I just press Refresh All."
**Explain simply:**
- *Attrition rate* = exits in the month / average headcount x 100, where average headcount = (opening + closing) / 2.
- Power Query: connect to HR master (parameterised path), fix types, trim text, remove duplicates (see earlier answers).
- Data Model: load as Connection only plus Data Model, relate Calendar to Join and Exit dates.
- Power Pivot measures: Exits, Opening, Closing, Attrition %.
- PivotTable with a Department slicer; refresh updates everything (Microsoft Support, "How Power Query and Power Pivot work together" describes this pairing).
**Example:** 200 employees at start, 198 at end, 4 exits: average 199, attrition 2.01%.
**Sample sheet (10-person toy to show logic; closing = opening minus exits, assuming no joiners):**

| | A | B | C |
|---|---|---|---|
| 1 | Dept | Opening | Exits |
| 2 | HR | 2 | 1 |
| 3 | IT | 4 | 2 |
| 4 | Sales | 4 | 1 |

**Formula / Steps (not run here):**
1. Data > Get Data > From File; Power Query Editor: clean, set types.
2. Close & Load To... > Only Create Connection > Add to Data Model.
3. Power Pivot: relationships Calendar[Date] to Join/Exit dates.
4. Measures (DAX, not run here): `Exits := COUNTROWS(FILTER(Employees, ...))`, `Attrition % := DIVIDE([Exits], [Avg Headcount])`.
5. Insert > PivotTable > Use this workbook's Data Model; Data > Refresh All monthly.
**Alternative:** Do it all in one PivotTable on a single clean table with helper columns (simpler, less flexible), or move to Power BI.
**Result:** pandas toy data (not Power Query): March 2025 per department: HR opening 2, closing 1, exits 1, attrition 66.7%; IT 4, 2, 2, 66.7%; Sales 4, 3, 1, 28.6%; total opening 10, closing 6, exits 4, attrition 50.0% (a deliberately tiny team). The 200/198/4 example gives 2.01%, checked by calculation.
**Version note:** Power Query: Excel 2016+ for Windows and 365. Power Pivot/Data Model: Excel 2016 to 2024 and 365 per Microsoft Support; edition-level availability unverified.
**Edge cases:** Rejoiners, exits on the last day, duplicate IDs, different definitions of opening headcount.
**Likely follow-ups:** 1) *How do you avoid broken refresh?* Parameter path, fixed headers. 2) *Annualised?* Multiply monthly by 12 (simple method, state it).
**Common mistakes:** Using closing headcount only as the denominator; exits by resignation date but headcount by payroll date.

### Q58 ⭐ 🔴 When would you move from Excel Power Query and Power Pivot to Power BI?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Judgement, not tool loyalty.
**Say this in the interview:** "When the data is too big for a workbook, many people need an interactive dashboard with scheduled refresh and row-level access, or the Excel file has become slow and fragile. For a small team report I stay in Excel."
**Explain simply:**
- Power Query and the same modelling ideas appear in Power BI, so skills transfer (the Microsoft Support page "How Power Query and Power Pivot work together" says together they prepare data for PivotTables, PivotCharts and Power BI).
- Move when: files are slow or huge, you need shared web dashboards, scheduled refresh without opening Excel, or security by user.
- Stay in Excel when: audience is small, output is a spreadsheet, or it is one-off analysis.
- Limits in Excel; see Q59.
**Example:** A 30-line monthly attrition table for HR heads stays in Excel. A 20-lakh-row payroll history needing a live dashboard for 50 managers moves to Power BI.
**Formula / Steps:** Not a formula question. Path: Power BI Desktop > Get Data > import the same Excel/CSV; copy M code from the Advanced Editor (from memory, not run here).
**Alternative:** Publish the workbook to SharePoint/OneDrive and share it, for modest needs.
**Result:** Not applicable.
**Version note:** Power BI features and licences are from memory, unverified. Microsoft Support notes Data Model refresh is not supported in SharePoint Online or SharePoint On-Premises (page "How Power Query and Power Pivot work together").
**Edge cases:** Organisation may not have Power BI licences; governance rules may require Excel.
**Likely follow-ups:** 1) *Can M code be reused?* Largely yes (from memory). 2) *DAX the same?* Mostly.
**Common mistakes:** Saying Excel is "bad"; ignoring licence and skill constraints.

### Q59 ⭐ 🔴 What are the limits of Power Pivot and the Data Model when files get very large, and how would you handle them?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Awareness of size limits and practical remedies.
**Say this in the interview:** "A table can hold up to about 2 billion rows on paper, but real limits are memory, file size on SharePoint or the web, and speed. I reduce columns and rows on import, and move to Power BI or a database when needed."
**Explain simply:**
- Microsoft's specification page lists 1,999,999,997 rows per table, 5 connections, and a 250 MB total file size limit for Excel for the web in Microsoft 365 (Microsoft Support, "Data Model specification and limits", fetched again in Wave C; applies to 365, 2024, 2021). It gave no memory limit or 32-bit/64-bit figure.
- SharePoint Server 2013 upload default is 50 MB, rendering default is 10 MB, with a 2 GB maximum an admin must configure (same page).
- Remedies (Microsoft Support, "Create a memory-efficient Data Model using Excel and the Power Pivot add-in"): remove unneeded columns, filter unneeded rows, split datetime columns, round decimals, use DAX measures instead of derived columns, run the Workbook Size Optimizer. A model is typically 7 to 10 times smaller than its source.
- That page also quotes a 10 MB SharePoint Online/Excel Web App limit, which conflicts with the 250 MB figure; the 250 MB page (fetched, applies to 365/2024/2021) is the one re-read in Wave C, the 10 MB wording was seen only in a search summary; check the current docs before quoting either.
**Example:** A payroll export of 40 columns shrinks sharply if you import only EmpID, Month, Gross, Dept (4 columns).
**Formula / Steps (not run here):** Power Query: Home > Choose Columns; Filter Rows to current two years; load to Data Model only (no worksheet copy).
**Alternative:** Pre-aggregate in SQL, or move to Power BI/a database.
**Result:** Not applicable (limits, not calculation).
**Version note:** 32-bit Excel memory limits are not stated on the fetched pages; "from memory, unverified".
**Edge cases:** Columns with many unique values (IDs, timestamps) cost the most memory.
**Likely follow-ups:** 1) *Biggest quick win?* Remove unused columns. 2) *Is 64-bit better?* Generally yes (from memory).
**Common mistakes:** Loading all columns and also a copy to the sheet.

### Q60 ⭐ 🔴 How do you write a custom column in M using if...then...else, Text.Upper or Date functions?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic M syntax and case-sensitivity.
**Say this in the interview:** "Add Column > Custom Column, then write M. M is case-sensitive, so it is `if ... then ... else` in lower case and `Text.Upper`, `Date.Year` with capitals."
**Explain simply:**
- *M* is the language behind Power Query steps; column names go in square brackets, like `[Tenure]`.
- Conditions: `if [Tenure] >= 5 then "Senior" else "Junior"`.
- Text: `Text.Upper([Name])`. Date: `Date.Year([Join])`, `Date.MonthName([Join])`.
- Not run here: Power Query cannot run in this environment.
**Example:** Asha Rao, tenure 8, joined 15-Apr-2018 gives Senior, ASHA RAO, 2018, April. Ravi K, tenure 2, joined 01-Nov-2024 gives Junior, RAVI K, 2024, November.
**Sample sheet:**

| | A | B | C |
|---|---|---|---|
| 1 | Name | Tenure | Join |
| 2 | asha rao | 8 | 15-Apr-2018 |
| 3 | ravi k | 2 | 01-Nov-2024 |

**Formula / Steps (M, not run here):** Add Column > Custom Column; formulas: `if [Tenure] >= 5 then "Senior" else "Junior"`; `Text.Upper([Name])`; `Date.Year([Join])`; `Date.MonthName([Join])`.
**Alternative:** Add Column > Conditional Column (point and click) for simple if/else.
**Result:** pandas reproduction (M not run here): Band Senior/Junior; NameUp ASHA RAO, RAVI K; JoinYear 2018, 2024; Month April, November.
**Version note:** Custom Column is in Power Query in Excel 2016+; I did not confirm function availability on a Microsoft page.
**Edge cases:** Nulls: `null >= 5` is not true (from memory, unverified); handle with `if [Tenure] = null then ...`. Join must be a Date type for Date functions.
**Likely follow-ups:** 1) *Text.Proper?* Capitalises each word. 2) *Case error?* `If` fails; keywords are lower case.
**Common mistakes:** Using Excel syntax (`IF(...)`); comparing text with numbers; forgetting the column type.

### Q61 ⭐ 🔴 What are privacy levels in Power Query, and why can a merge of two sources show a "Formula.Firewall" error?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand the protection and the fix?
**Say this in the interview:** "Privacy levels (Private, Organizational, Public) tell Power Query how sensitive each source is. The Data Privacy Firewall stops data leaking from one source into another, and it errors when a step both reads a source and references another query or mixes incompatible levels. The safe fix is to restructure the query, not switch privacy off."
**Explain simply:**
- Microsoft says the firewall exists to prevent unintentional data leakage between sources, because folding could send one source's data to another (Microsoft Learn, "Behind the scenes of the Data Privacy Firewall").
- Rule: a partition (group of steps) can access compatible data sources, or reference other partitions, but not both.
- Compatible means both Public or both Organizational. Private with anything, or Public with Organizational, is incompatible (same page).
- Two error messages: "references other queries or steps, so it may not directly access a data source" and "accessing data sources that have privacy levels which cannot be used together".
- Fix: combine into one query, or stage data so references do not also read a source. Disabling checks (Privacy: Ignore the Privacy Levels) is an option but weakens protection (same page).
**Example:** HR Excel file (Organizational) merged with a public holiday web list (Public) can trigger the second error until levels are aligned or sources are loaded separately.
**Formula / Steps (not run here):** File > Options and settings > Query Options > Privacy; set levels per source from the prompt dialog.
**Alternative:** Load each source as its own query, then merge the two queries, which are separate partitions (from the Learn page's explanation of references and buffering).
**Result:** Not run here; the error cannot be reproduced without Power Query.
**Version note:** The Learn page says privacy levels are unavailable in Power Platform dataflows; the page does not address Excel versions.
**Edge cases:** Parameters in a source URL are trimmed to avoid the error (Learn page).
**Likely follow-ups:** 1) *Why does folding matter?* It can push data to another source. 2) *Is disabling safe?* Only on trusted data.
**Common mistakes:** Turning the firewall off first; marking everything Public without thinking.

### Q62 ⭐ 🔴 How do you make Power Query refresh automatically when the workbook opens, and what are the limits?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the connection property and its restrictions?
**Say this in the interview:** "In Connection Properties, Usage tab, I tick 'Refresh data when opening the file'. It needs the connections to be trusted, and it does not refresh if the file is closed."
**Explain simply:**
- Steps (Microsoft Support, "Refresh an external data connection in Excel"): select a cell in the data range; Data > Refresh All dropdown > Connection Properties; Usage tab > Refresh control > Refresh data when opening the file.
- To refresh on open you must enable data connections via the Trust Center bar or store the workbook in a trusted location (same page).
- "Refresh every n minutes" is on the same tab and only works while the workbook is open.
- Background refresh is not available for connections that retrieve Data Model data (same page).
**Example:** Monday 9am: opens the attendance workbook, Excel pulls the latest 12 files with no click needed.
**Formula / Steps:** Follow the Support-page steps above (Connection Properties). Not run here. The alternative route Data > Queries & Connections > right-click the query > Properties is from memory, unverified.
**Alternative:** Office Scripts / Power Automate or VBA `ThisWorkbook.RefreshAll` in Workbook_Open (from memory, unverified).
**Result:** Not run here.
**Version note:** Refresh for queries loaded to the Data Model is not yet supported in Excel for the web (Microsoft Support, "Power Query data sources in Excel versions"). Excel for Android and iOS do not support Power Query (same page).
**Edge cases:** Security prompt blocks refresh; credentials may be needed; a slow source delays opening.
**Likely follow-ups:** 1) *Overnight without opening?* Not in plain Excel. 2) *Disable on open?* Untick the box.
**Common mistakes:** Assuming it refreshes while closed; forgetting Trust Center.

### Q63 ⭐ 🔴 How do you troubleshoot a Power Query step that shows "Expression.Error: The column ... of the table wasn't found"?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** A calm debugging routine.
**Say this in the interview:** "It means a step refers to a column name that no longer exists at that point. I click the failing step, compare the headers in the previous step with the name in the formula bar, and fix a rename, a typo, a trailing space or a column that an earlier step removed."
**Explain simply:**
- Microsoft notes queries rely on table and column names in almost every step, so renamed source columns cause refresh problems (Microsoft Support, "Handling data source errors (Power Query)").
- Step-level errors are shown with a yellow background in the query; cell-level errors let the query load but show Error in the cell (same page).
- Checklist: source header changed; column removed earlier in the steps; extra space or different case; promoted headers missing.
- Fix by editing the step name, or inserting a rename step before it.
**Example:** The source changed "Dept" to "Department"; the step `Table.TransformColumnTypes(..., {{"Dept", type text}})` fails.
**Formula / Steps (not run here):** Applied Steps > click the red step > check the formula bar; click the previous step to see headers; edit or delete.
**Alternative:** Use `MissingField.UseNull` or `MissingField.Ignore` options in M (from memory; see Q47).
**Result:** pandas analogy (Power Query not run here): selecting ["EmpID","Dept"] after renaming gives KeyError "['Dept'] not in index".
**Version note:** Applies to Excel with Power Query (2016+ Windows, 365).
**Edge cases:** Wrong sheet loaded, or header row not promoted so columns are named Column1.
**Likely follow-ups:** 1) *Quick prevention?* Fixed headers. 2) *Error in one cell only?* Replace or Remove Errors.
**Common mistakes:** Deleting the step without understanding the cause; fixing downstream steps.

### Q64 ⭐ 🔴 What is the difference between Import mode and DirectQuery, and does Excel support both?
**Asked at:** the Part 7 sources file notes Import vs DirectQuery among Wipro/Deloitte DAX topics in repo research (not independently verified here).
**What the interviewer is checking:** Do you know these are Power BI storage modes and how they differ?
**Say this in the interview:** "Import copies the data into the model, so it is fast but needs refreshing. DirectQuery leaves data in the source and sends queries live, so it is current but slower. They are Power BI terms; Excel's Data Model is Import style, and I would not claim Excel has DirectQuery."
**Explain simply:**
- *Import*: data is loaded and compressed into the model; refresh updates it. Excel's Power Query and Data Model work this way (Microsoft Support, "Power Pivot: Powerful data analysis and data modeling in Excel" describes importing millions of rows into the workbook).
- *DirectQuery*: each visual sends a query to the source (usually a SQL database) at view time; nothing is stored. (From memory, unverified.)
- Trade-off: speed and full DAX versus freshness and no size limit in the file.
- I found no Microsoft Support page confirming DirectQuery in Excel, so treat "Excel does not support DirectQuery" as from memory, unverified.
**Example:** A daily-updated attendance table for a 2,000-person company: Import is fine. A 50-crore-row live transaction system: DirectQuery in Power BI.
**Formula / Steps:** Not applicable in Excel. Power BI Desktop: Get Data > SQL Server > choose Import or DirectQuery (from memory, not run here).
**Alternative:** In Excel, schedule or trigger refresh to approximate freshness (Q62).
**Result:** Not applicable.
**Version note:** Unverified; the Support page I read covers only import.
**Edge cases:** DirectQuery limits some DAX and Power Query steps (from memory).
**Likely follow-ups:** 1) *Composite models?* Mix both in Power BI. 2) *When Import?* Small data or heavy modelling.
**Common mistakes:** Saying Excel offers DirectQuery; assuming DirectQuery is always better because it is live.

