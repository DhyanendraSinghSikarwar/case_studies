# Book 4 — Power BI & Visualization | Part 2: Power Query transformations in Power BI 🟢🟡

**Target:** 60 questions | **Actual:** 61 questions
**Scope:** Power BI-specific Power Query: shaping, cleaning, merging, appending, unpivoting, folding, parameters, errors and refresh-related behaviour (not Excel basics, data modelling or DAX).

### Q1 ⭐⭐⭐ 🟢 What is Power Query in Power BI, and why do we use it before building reports?
**Asked at:** commonly asked (no company-specific report found); generic Power BI interview lists (FanRuan, Zero To Mastery) open with Power Query, but they name no company.
**What the interviewer is checking:** Whether you understand that data is cleaned and shaped before it reaches the report, and that this is repeatable.
**Say this in the interview:** "Power Query is the data-preparation tool inside Power BI. I connect to a source, clean and reshape the data step by step, and those steps are saved, so every refresh repeats them automatically. I do this before building visuals so the report sits on clean, correctly typed data."
**Explain simply:**
- Power Query is a data transformation and preparation engine with a point-and-click editor (Microsoft Learn: What Is Power Query?). It does ETL: **E**xtract (connect), **T**ransform (clean and reshape), **L**oad (send to the model).
- Every click is recorded as a **step**, and the steps are written in a language called **M** behind the scenes. The source file is not changed; only Power BI's view of it is.
- Because the steps are saved, next month's file gets the same cleaning with one Refresh. No manual repeat in Excel.
- Dirty data (extra spaces, text-numbers, duplicate rows) breaks totals and filters later, so you fix it here, once, at the start.
**Example:** The HR team emails a monthly headcount file with "HR", "hr " and "Human Resources" for the same department. In Power Query you standardise the names once; every future file is fixed on refresh, so the department chart shows one HR bar, not three.
**DAX / Steps (not run here):** Power BI Desktop > Home tab > Queries group > **Transform data** opens the editor. Left pane = list of queries, centre = data preview, right = Query Settings with Applied Steps.
**Alternative:** Do the same cleaning in the source system (SQL view) or in Excel by hand. A SQL view is good when the database team owns it; Excel by hand is not repeatable.
**Version / licensing note:** Power Query is also in Excel, Dataflows and Fabric, not only Power BI (Microsoft Learn: What Is Power Query?). That page's product table lists Excel for Windows and Mac. Microsoft's Power Query UI page says Power BI Desktop can be downloaded for free. Desktop being Windows-only: from memory, unverified.
**Edge cases:** Power Query only prepares data. Calculations that react to slicers (totals, ratios) belong in DAX, not here.
**Likely follow-ups:** 1) *Is it ETL?* Yes, it covers the transform stage and hands the result to the model. 2) *Does it change my Excel file?* No, the source stays as is.
**Common mistakes:** Cleaning data by hand in the source file and forgetting to repeat it next month; building charts first and discovering dirty data afterwards.

### Q2 ⭐⭐⭐ 🟢 How do you open the Power Query Editor in Power BI Desktop?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic hands-on familiarity with Power BI Desktop.
**Say this in the interview:** "In Power BI Desktop I go to the Home tab and click Transform data. That opens the Power Query Editor where I see my queries on the left and Applied Steps on the right."
**Explain simply:**
- **Transform data** (Home tab) opens the editor with your existing queries.
- When you first connect to a file, the Navigator window offers **Load** (send as is) or **Transform Data** (clean first). Choose Transform Data.
- The editor has a ribbon (tabs: Home, Transform, Add Column, View), a Queries pane, the data preview, and a Query Settings pane with Applied Steps (Microsoft Learn: Query Overview in Power BI Desktop).
- Right-click menus on columns repeat most ribbon commands.
**Example:** You loaded the leave-balance file yesterday and now spot blank departments. Home > Transform data takes you back to fix it, and the fix is added as a new step.
**DAX / Steps (not run here):** 1) Power BI Desktop > **Home** tab > **Queries** group > **Transform data**. 2) Or, when connecting: Get data > pick file > in the Navigator click **Transform Data**. 3) To close and save: **File** > **Close & Apply** (see Q8). 4) Advanced code view: **View** tab > **Advanced Editor**.
**Alternative:** Right-click a table in the Data pane (right-hand Fields list) and choose **Edit query** (from memory, unverified wording).
**Version / licensing note:** Microsoft's page (dated 2026-09-19) says Desktop has a **new Power Query experience in preview** (File > Options and settings > Options > Preview features) and the legacy editor. Transform data on the Home tab opens the editor in both. Your screen may therefore look different from older tutorials.
**Edge cases:** If the Transform data button is greyed out, no data has been loaded or you are in a view that does not support it (from memory, unverified).
**Likely follow-ups:** 1) *Can you edit queries in the Power BI Service?* Dataflows use an online Power Query editor, but a published .pbix report is edited in Desktop. 2) *Where are my steps?* Right-hand Applied Steps.
**Common mistakes:** Clicking Load when the data needs cleaning; closing the editor with the X instead of Close & Apply and losing pending changes.

### Q3 ⭐⭐⭐ 🟢 What is the difference between Merge Queries and Append Queries?
**Asked at:** commonly asked (no company-specific report found); merge vs append is a standard topic in Power BI exam-prep articles (Pragmatic Works PL-300 blog, RADACAD; seen as search snippets only).
**What the interviewer is checking:** Do you know that merge adds columns (like a lookup/join) and append adds rows (like stacking)?
**Say this in the interview:** "Merge joins two tables side by side on a matching key, so it adds columns, like a VLOOKUP or SQL join. Append stacks one table under another, so it adds rows, like SQL UNION ALL."
**Explain simply:**
- **Merge Queries** needs a key column on both sides (for example EmpID). The right table arrives as a column of tables that you expand.
- **Append Queries** needs similar column names. Power Query matches columns by name, not position, and fills missing ones with null (Microsoft Learn: Append Queries).
- Both are on the Home tab, Combine group.
**Example:** Employee list (3 rows) merged with Department list gives 3 rows with a Dept column. January attendance (2 rows) appended with February (1 row) gives 3 rows.
**Sample data:**

Table `Employees`:

| EmpID | Name | DeptID |
|---|---|---|
| 101 | Asha | 1 |
| 102 | Ravi | 2 |
| 103 | Meena | 1 |

Table `Departments`: (1, HR), (2, Finance). Tables `Jan` = Asha, Ravi; `Feb` = Meena.

**DAX / Steps (M code, not run here):**
```m
let
    Merged   = Table.NestedJoin(Employees, {"DeptID"}, Departments, {"DeptID"}, "Departments", JoinKind.LeftOuter),
    Expanded = Table.ExpandTableColumn(Merged, "Departments", {"Dept"}),
    Stacked  = Table.Combine({Jan, Feb})
in
    Stacked
```
Click-path: Home > Combine > **Merge Queries** (or Merge Queries as New); Home > Combine > **Append Queries** (or Append Queries as New).
**Alternative:** Instead of merging for a lookup column, load both tables and join them with a relationship in the model (Q38).
**Result:** Reproduced with pandas (not run in Power Query): the merge returns 3 rows with Dept = HR, Finance, HR; the append returns 3 rows: Asha, Ravi, Meena.
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"EmpID":[101,102,103],"Name":["Asha","Ravi","Meena"],"DeptID":[1,2,1]})
dept = pd.DataFrame({"DeptID":[1,2],"Dept":["HR","Finance"]})
# MERGE = add columns (join on a key)
print(emp.merge(dept, on="DeptID", how="left"))
jan = pd.DataFrame({"EmpID":[101,102],"Name":["Asha","Ravi"]})
feb = pd.DataFrame({"EmpID":[103],"Name":["Meena"]})
# APPEND = stack rows (same columns)
print(pd.concat([jan, feb], ignore_index=True))
```
Real printed output (pandas 3.0.5):
```text
   EmpID   Name  DeptID     Dept
0    101   Asha       1       HR
1    102   Ravi       2  Finance
2    103  Meena       1       HR
   EmpID   Name
0    101   Asha
1    102   Ravi
2    103  Meena
```
**Version / licensing note:** Both commands and the "as new" variants are described on the Microsoft Learn pages Merge Queries Overview (updated 2026-04) and Append Queries (2026-04). No licence needed beyond Power BI Desktop (free download per Microsoft's Power Query UI page).
**Edge cases:** Merge keys must have the same data type or matches fail (Q33). Append creates nulls where a column exists in only one table. A left outer merge can duplicate left rows if the right key repeats.
**Likely follow-ups:** 1) *Which join kind is default?* Left outer. 2) *Can you append more than two?* Yes, "Three or more tables".
**Common mistakes:** Appending tables with different column names and getting half-empty columns; merging on a text key against a number key.

### Q4 ⭐⭐⭐ 🟢 How do you remove duplicates in Power Query?
**Asked at:** commonly asked (no company-specific report found); appears in generic Power BI question lists (Zero To Mastery and similar), which name no company.
**What the interviewer is checking:** Can you remove duplicate rows safely, and do you know the traps (case, which row stays)?
**Say this in the interview:** "I select the column or columns that define a duplicate, say EmpID, then Home > Remove Rows > Remove Duplicates. Power Query is case-sensitive, so I standardise case first, and it doesn't guarantee which duplicate it keeps."
**Explain simply:**
- Select the column(s) first. Selecting all columns removes only fully identical rows; selecting EmpID keeps one row per EmpID.
- "Meena" and "MEENA" count as different values, so make text one case before removing duplicates (Microsoft Learn: Working with duplicate values).
- Microsoft warns that Power Query does not guarantee that the first instance is kept.
**Example:** An employee export has Ravi twice because he changed department. Removing duplicates on EmpID keeps one row, but you must decide which row (Q47 shows how to keep the latest).
**Sample data:**

Table `Staff`:

| EmpID | Name | Dept |
|---|---|---|
| 101 | Asha | HR |
| 102 | Ravi | Finance |
| 102 | Ravi | Finance |
| 103 | Meena | HR |
| 103 | MEENA | HR |

**DAX / Steps (M code, not run here):**
```m
= Table.Distinct(Source, {"EmpID"})
```
Click-path: select column(s) > Home > Reduce Rows group > **Remove Rows** > **Remove Duplicates**.
**Alternative:** Group By EmpID with a Max or "All rows" operation (Q22), which lets you choose which row survives.
**Result:** Reproduced with pandas: 5 rows before; removing duplicates on all columns leaves 4 (MEENA is different from Meena); on EmpID only leaves 3; after Proper Case on Name and all columns, 3.
**Pandas check:**
```python
import pandas as pd
df = pd.DataFrame({"EmpID":[101,102,102,103,103],
                   "Name":["Asha","Ravi","Ravi","Meena","MEENA"],
                   "Dept":["HR","Finance","Finance","HR","HR"]})
print("rows before:", len(df))
print("all columns :", len(df.drop_duplicates()))               # MEENA vs Meena are different (case-sensitive)
print("EmpID only  :", len(df.drop_duplicates(subset=["EmpID"])))
df["Name"] = df["Name"].str.title()                              # lower/upper/proper transform first
print("after Proper, all columns:", len(df.drop_duplicates()))
```
Real printed output (pandas 3.0.5):
```text
rows before: 5
all columns : 4
EmpID only  : 3
after Proper, all columns: 3
```
**Version / licensing note:** Behaviour and warnings are from Microsoft Learn: Working with duplicate values (updated 2026-08) and Table.Distinct (PowerQuery M). The same page notes duplicate removal can use much memory when it cannot fold (Q13).
**Edge cases:** Trailing spaces make "Asha" and "Asha " different (Q18). Blank keys all look duplicates of each other. Keep Duplicates (Home > Keep Rows) shows only the repeated rows, useful for auditing.
**Likely follow-ups:** 1) *How do you keep the latest?* Sort descending by date, Table.Buffer, then remove duplicates, or use Group By (Q47). 2) *How do you just see the duplicates?* Keep Rows > Keep Duplicates.
**Common mistakes:** Removing duplicates across all columns when one column differs slightly; forgetting case; assuming the top row is kept.

### Q5 ⭐⭐⭐ 🟢 How do you change a column's data type in Power Query, and why does it matter?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that the data type controls sorting, maths and which menu options appear?
**Say this in the interview:** "I click the small type icon at the left of the column header, or use Home > Data type, and pick the right type: Whole Number, Decimal, Date, Text. It matters because a number stored as text sorts alphabetically and can't be summed properly, and date tools only appear for real dates."
**Explain simply:**
- Data types are set per column (Microsoft Learn: Data Types in Power Query). A column with no type is **Any**, which Microsoft says to avoid in final output.
- Four places to change it: Home > Data type; Transform > Data type; the header icon; right-click > Change Type.
- Type-specific options (the Date menu, number filters) are greyed out if the type is wrong (Microsoft Learn: Best Practices).
**Example:** Salary arrives as text "9000", "45000", "120000", "7500". Sorted as text, 9000 comes first and 120000 lands near the bottom. As numbers, 120000 is the biggest.
**Sample data:**

Table `Pay` (Salary read as text):

| Emp | Salary |
|---|---|
| Asha | "9000" |
| Ravi | "45000" |
| Meena | "120000" |
| Karan | "7500" |

**DAX / Steps (M code, not run here):**
```m
= Table.TransformColumnTypes(Source, {{"Salary", Int64.Type}})
```
Click-path: right-click the Salary header > **Change Type** > **Whole Number**.
**Alternative:** Set the type later in Power BI's model view. Better in Power Query, so errors show early and the type is part of the repeatable steps.
**Result:** Reproduced with pandas: text sort gives 9000, 7500, 45000, 120000; number sort gives 120000, 45000, 9000, 7500; sum is 181500.
**Pandas check:**
```python
import pandas as pd
df = pd.DataFrame({"Emp":["Asha","Ravi","Meena","Karan"],"Salary":["9000","45000","120000","7500"]})
print("as text, sorted descending:  ", df.sort_values("Salary", ascending=False)["Salary"].tolist())
df["Salary"] = pd.to_numeric(df["Salary"])
print("as number, sorted descending:", df.sort_values("Salary", ascending=False)["Salary"].tolist())
print("sum as number:", df["Salary"].sum())
```
Real printed output (pandas 3.0.5):
```text
as text, sorted descending:   ['9000', '7500', '45000', '120000']
as number, sorted descending: [120000, 45000, 9000, 7500]
sum as number: 181500
```
**Version / licensing note:** Type list and menu locations from Microsoft Learn: Data Types in Power Query (updated 2026-08). Decimal Number is a 64-bit floating point; Fixed Decimal always has four decimal places (see Q28).
**Edge cases:** A value like "NA" makes the conversion produce a cell error (Q19, Q39). Dates stored as text need the right locale (Q41). Changing type before cleaning commas fails (Q7).
**Likely follow-ups:** 1) *Why not leave it as Any?* Microsoft recommends explicit types. 2) *Can Power Query guess types?* Yes, for files it adds a Changed Type step (Q52).
**Common mistakes:** Leaving numbers as text; converting before removing symbols like commas; forgetting types on new custom columns.

### Q6 ⭐⭐⭐ 🟢 How do you handle null or blank values in Power Query?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you tell a null from an empty text, and choose between fixing and removing blanks?
**Say this in the interview:** "First I check how many blanks there are with Column Quality. Then it depends on the business meaning: replace with a default like Unknown or 0, fill from neighbouring rows, or remove the rows. I also convert empty text to null first because they are different."
**Explain simply:**
- **null** means "no value". An **empty string** ("") looks blank but is text, and functions like Fill Up don't treat it as null (Microsoft Learn: Fill values in a column).
- Fix options: Replace Values (null to a value), Fill Down/Up (Q20), Remove Empty or filter out, or leave null and handle it in DAX.
- Choose by meaning: missing bonus is probably 0, missing department is "Unknown", missing employee ID means the row is useless.
**Example:** In a bonus file, Ravi's bonus is blank. Replacing with 0 keeps him in averages; deleting the row hides him.
**Sample data:**

Table `Bonus`:

| Emp | Dept | Bonus |
|---|---|---|
| Asha | HR | 5000 |
| Ravi | "" (empty text) | null |
| Meena | Finance | 0 |
| Karan | null | 2000 |

**DAX / Steps (M code, not run here):**
```m
let
    EmptyToNull = Table.ReplaceValue(Source, "", null, Replacer.ReplaceValue, {"Dept"}),
    DeptFixed   = Table.ReplaceValue(EmptyToNull, null, "Unknown", Replacer.ReplaceValue, {"Dept"}),
    BonusFixed  = Table.ReplaceValue(DeptFixed, null, 0, Replacer.ReplaceValue, {"Bonus"})
in
    BonusFixed
```
Click-path: Transform > Any Column > **Replace Values** (leave Value To Find blank, Replace With = null).
**Alternative:** Filter the column with the dropdown and untick (null) to drop those rows; or Home > Remove Rows > Remove Blank Rows.
**Result:** Reproduced with pandas: only Karan's Dept is a true null at the start; after converting "" to null Ravi's is too; dropping null Bonus would lose 1 of 4 rows; after replacements Ravi and Karan show Unknown and Ravi's bonus is 0.
**Pandas check:**
```python
import pandas as pd
df = pd.DataFrame({"Emp":["Asha","Ravi","Meena","Karan"],
                   "Dept":["HR","","Finance",None],
                   "Bonus":[5000,None,0,2000]})
print("Dept is null?      ", df["Dept"].isna().tolist())      # "" is NOT null
df["Dept"] = df["Dept"].replace("", None)                      # Replace Values: "" -> null
print("after '' -> null:  ", df["Dept"].isna().tolist())
kept = df.dropna(subset=["Bonus"])                             # Remove Empty / filter null
print("rows if we drop null Bonus:", len(kept), "of", len(df))
df["Dept"] = df["Dept"].fillna("Unknown")                      # Replace Values: null -> Unknown
df["Bonus"] = df["Bonus"].fillna(0)                            # null -> 0 (a business decision)
print(df.to_string(index=False))
```
Real printed output (pandas 3.0.5):
```text
Dept is null?       [False, False, False, True]
after '' -> null:   [False, True, False, True]
rows if we drop null Bonus: 3 of 4
  Emp    Dept  Bonus
 Asha      HR 5000.0
 Ravi Unknown    0.0
Meena Finance    0.0
Karan Unknown 2000.0
```
**Version / licensing note:** Replace Values menu locations from Microsoft Learn: Replace values and errors; the empty-vs-null note from Microsoft Learn: Fill values in a column.
**Edge cases:** Spaces-only cells are neither null nor empty; Trim first (Q18). A 0 is a real value, not blank. Average of a column ignores nulls but includes zeros.
**Likely follow-ups:** 1) *Null or zero?* Depends: zero means "known none", null means "unknown". 2) *Where do you see blanks quickly?* Column Quality bar (Q23).
**Common mistakes:** Treating "" as null; replacing nulls with 0 without asking whether that changes averages.

### Q7 ⭐⭐⭐ 🟢 What are Applied Steps in Power Query, and why does their order matter?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that steps run top to bottom and that reordering or inserting steps can break the query?
**Say this in the interview:** "Applied Steps is the recorded to-do list of my transformations, shown in the right pane. They run in order, so each step depends on the one before. If I move or delete a step that a later step relies on, the query can error."
**Explain simply:**
- Every transformation is saved as a step; click any step to see the data as it was at that point (Microsoft Learn: Applied Steps).
- You can rename, delete, reorder (Move before/after or drag) and insert steps. Microsoft shows a warning when inserting in the middle, because later steps may break.
- "All query steps are carried out in the order they appear" (Microsoft Learn: Query Overview in Power BI Desktop). The engine may reorder internally for folding, but don't rely on that.
- Good order for speed: remove rows and columns early, expensive operations last (Q45).
**Example:** Salary arrives as "40,000". Step 1 remove comma, step 2 change type to number gives 40000. Swap them and every salary becomes an error.
**Sample data:**

Table `Pay`: Asha "40,000", Ravi "52,000", Meena "35,000" (all text).

**DAX / Steps (not run here):** View tab > Query Settings (if the pane is hidden). Right-click a step: Rename, Delete, Delete Until End, Insert Step After, Move Before/After, Extract Previous, Properties. The gear icon beside a step reopens its dialog.
**Alternative:** Edit the same list as code in View > Advanced Editor (Q14).
**Result:** Reproduced with pandas: removing the comma first gives 40000, 52000, 35000; converting first gives errors for all three (shown as NaN in pandas).
**Pandas check:**
```python
import pandas as pd
df = pd.DataFrame({"Emp":["Asha","Ravi","Meena"],"Dept":["HR","HR","Finance"],"Salary":["40,000","52,000","35,000"]})
# Good order: remove comma, THEN convert to number
good = df.assign(Salary=pd.to_numeric(df["Salary"].str.replace(",","")))
print(good["Salary"].tolist())
# Wrong order: convert first -> errors (coerce shows them as NaN)
bad = pd.to_numeric(df["Salary"], errors="coerce")
print(bad.tolist())
```
Real printed output (pandas 3.0.5):
```text
[40000, 52000, 35000]
[nan, nan, nan]
```
**Version / licensing note:** Step menu items from Microsoft Learn: Applied Steps (updated 2026-04). The step icon and folding indicator exist only in Power Query Online, not Desktop, per that page.
**Edge cases:** A step that refers to a column by name fails if an earlier step renames or removes it. Deleting a step that created a column breaks later steps using it.
**Likely follow-ups:** 1) *Can I undo?* Delete the step. 2) *How to split a long query?* Right-click a step > Extract Previous.
**Common mistakes:** Inserting a step in the middle and ignoring the warning; leaving default names like "Changed Type3" that nobody understands (rename them).

### Q8 ⭐⭐⭐ 🟢 What does Close & Apply do in the Power Query Editor?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that the editor changes nothing in the report until you apply, and that applying loads data into the model?
**Say this in the interview:** "Close & Apply saves my Power Query steps, closes the editor, and loads the transformed data into the Power BI data model, so the report and measures use the new version."
**Explain simply:**
- While you are in the editor you work on a preview of the data. Nothing reaches the report until Close & Apply.
- Microsoft describes it as: select **Close & Apply** from the editor's File menu; it applies the changes and closes the editor, and Desktop shows a progress dialog (Microsoft Learn: Query Overview in Power BI Desktop).
- Related choices: **Close** (closes without loading changes), **Apply** (loads but stays in the editor) (from memory, unverified wording).
- Queries with **Enable load** switched off are not loaded (Q27).
**Example:** You fix department names in Power Query. The bar chart still shows old names until you click Close & Apply, then it refreshes with the clean names.
**DAX / Steps (not run here):** Power Query Editor > **File** > **Close & Apply**. Then save the report: Power BI Desktop > File > Save.
**Alternative:** Home tab > Refresh in the main window re-runs queries from the source and reloads (it does not replace Close & Apply for new steps).
**Version / licensing note:** Menu path from Microsoft Learn: Query Overview in Power BI Desktop (updated 2026-09). Home-tab button variants in some builds: from memory, unverified.
**Edge cases:** Large sources can take minutes to apply. If a step errors, apply may fail and show the error. Applying twice does not duplicate data.
**Likely follow-ups:** 1) *Does it change the source file?* No. 2) *How is it different from Refresh?* Refresh re-reads the source using the saved steps; Close & Apply loads after you change steps.
**Common mistakes:** Closing without applying and wondering why visuals are unchanged; forgetting to save the .pbix afterwards.

### Q9 ⭐⭐⭐ 🟡 What join kinds are available when merging queries in Power Query, and when would you use each?
**Asked at:** commonly asked (no company-specific report found); the same six kinds appear on Microsoft's Merge queries overview page.
**What the interviewer is checking:** Can you pick the right join and describe it by what rows survive?
**Say this in the interview:** "There are six: left outer, right outer, full outer, inner, left anti and right anti. I use left outer to keep all my main rows and look up extra data, inner for only matching rows, and the anti joins to find rows with no match, like employees with no attendance."
**Explain simply:**
- **Left outer:** all rows from the left table, plus matches from the right (default).
- **Right outer:** all rows from the right table, plus matches from the left.
- **Full outer:** all rows from both. **Inner:** only rows that match in both.
- **Left anti:** only left rows that have no match. **Right anti:** only right rows with no match (Microsoft Learn: Merge Queries Overview describes these).
- "Left" and "right" are the first and second table in the dialog, so order matters.
**Example:** Employee master (4 people) vs attendance file (3 records, including ID 5 who is not in the master).
**Sample data:**

Table `Employees` (left):

| EmpID | Name |
|---|---|
| 1 | Asha |
| 2 | Ravi |
| 3 | Meena |
| 4 | Karan |

Table `Attendance` (right):

| EmpID | DaysPresent |
|---|---|
| 2 | 20 |
| 3 | 18 |
| 5 | 22 |

**DAX / Steps (M code, not run here):** `Table.NestedJoin(Employees, {"EmpID"}, Attendance, {"EmpID"}, "Att", JoinKind.LeftOuter)`; other kinds are `JoinKind.RightOuter`, `FullOuter`, `Inner`, `LeftAnti`, `RightAnti`. Click-path: Home > Combine > Merge Queries > pick both tables and key columns > choose Join Kind.
**Alternative:** Use relationships in the model instead of joining (Q38), or SQL joins at the source.
**Result:** Reproduced with pandas: left outer gives 4 rows (Asha and Karan have no days); right outer gives 3 rows (ID 5 has no name); full outer 5 rows; inner 2 rows (Ravi, Meena); left anti gives Asha and Karan; right anti gives ID 5.
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"EmpID":[1,2,3,4],"Name":["Asha","Ravi","Meena","Karan"]})
att = pd.DataFrame({"EmpID":[2,3,5],"DaysPresent":[20,18,22]})
for name,how in [("Left outer","left"),("Right outer","right"),("Full outer","outer"),("Inner","inner")]:
    print(name); print(emp.merge(att,on="EmpID",how=how).to_string(index=False))
m = emp.merge(att,on="EmpID",how="left",indicator=True)
print("Left anti"); print(m[m["_merge"]=="left_only"][["EmpID","Name"]].to_string(index=False))
m = emp.merge(att,on="EmpID",how="right",indicator=True)
print("Right anti"); print(m[m["_merge"]=="right_only"][["EmpID","DaysPresent"]].to_string(index=False))
```
Real printed output (pandas 3.0.5):
```text
Left outer
 EmpID  Name  DaysPresent
     1  Asha          NaN
     2  Ravi         20.0
     3 Meena         18.0
     4 Karan          NaN
Right outer
 EmpID  Name  DaysPresent
     2  Ravi           20
     3 Meena           18
     5   NaN           22
Full outer
 EmpID  Name  DaysPresent
     1  Asha          NaN
     2  Ravi         20.0
     3 Meena         18.0
     4 Karan          NaN
     5   NaN         22.0
Inner
 EmpID  Name  DaysPresent
     2  Ravi           20
     3 Meena           18
Left anti
 EmpID  Name
     1  Asha
     4 Karan
Right anti
 EmpID  DaysPresent
     5           22
```
**Version / licensing note:** Join-kind list from Microsoft Learn: Merge Queries Overview (updated 2026-04).
**Edge cases:** Duplicate keys on the right multiply left rows. Nulls in keys match only each other, and keys must share a data type. The anti-join row description on the Microsoft page is terse ("only rows from the left table"); the practical meaning is "left rows with no match".
**Likely follow-ups:** 1) *Which is default?* Left outer. 2) *How to find missing-from-attendance employees?* Left anti (Q37).
**Common mistakes:** Picking inner and silently losing unmatched rows; swapping left and right.

### Q10 ⭐⭐⭐ 🟡 How do you clean a messy employee master (extra spaces, mixed case, inconsistent department names) in Power Query?
**Asked at:** commonly asked (no company-specific report found); a gap-filled HR scenario, not seen in a specific company report.
**What the interviewer is checking:** Practical cleaning skills on typical HR data.
**Say this in the interview:** "I trim spaces, collapse double spaces, apply Capitalize Each Word to names, and standardise departments with Replace Values or a small mapping table. Then I check the result with Column Distribution so I know no variants are left."
**Explain simply:**
- **Trim** removes leading and trailing spaces; **Clean** removes hidden control characters; **Capitalize Each Word** fixes case (Q18).
- Spaces inside a name ("asha  rao") need a small extra step.
- For department variants, a **mapping table** (Raw name, Standard name) merged in is easier to maintain than many Replace Values steps.
**Example:** Five employee rows with "hr", "H.R.", "Human Resources", "Finance ", "fin" become two clean departments: HR and Finance.
**Sample data:**

Table `EmpRaw`:

| EmpID | Name | Dept |
|---|---|---|
| 101 | "  asha  rao" | hr |
| 102 | "RAVI KUMAR " | H.R. |
| 103 | "meena  s" | "Finance " |
| 104 | Karan Shah | fin |
| 105 | "  priya nair" | Human Resources |

**DAX / Steps (M code, not run here):**
```m
let
    Names = Table.TransformColumns(Source, {{"Name", each Text.Proper(Text.Combine(List.Select(Text.Split(Text.Trim(_), " "), each _ <> ""), " ")), type text}}),
    Depts = Table.TransformColumns(Names, {{"Dept", each Text.Proper(Text.Trim(_)), type text}}),
    Fixed = Table.TransformColumns(Depts, {{"Dept", each
              if _ = "Hr" or _ = "H.R." or _ = "Human Resources" then "HR"
              else if _ = "Fin" then "Finance" else _, type text}})
in
    Fixed
```
Text.Trim, Text.Proper and Text.Clean were checked against their Microsoft Learn pages; the rest of the M above is from memory.
**Alternative:** Merge with a mapping table (columns Raw, Standard) using a left outer join, then expand Standard. New spelling variants then need a new row in the table, not new code.
**Result:** Reproduced with pandas: Names become Asha Rao, Ravi Kumar, Meena S, Karan Shah, Priya Nair; Dept counts are HR 3 and Finance 2.
**Pandas check:**
```python
import pandas as pd
raw = pd.DataFrame({"EmpID":[101,102,103,104,105],
  "Name":["  asha  rao","RAVI KUMAR ","meena  s","Karan Shah","  priya nair"],
  "Dept":["hr","H.R.","Finance ","fin","Human Resources"]})
df = raw.copy()
df["Name"] = df["Name"].str.strip().str.replace(r"\s+"," ",regex=True).str.title()
df["Dept"] = df["Dept"].str.strip().str.title()
fix = {"Hr":"HR","H.R.":"HR","Human Resources":"HR","Fin":"Finance"}
df["Dept"] = df["Dept"].replace(fix)
print(df.to_string(index=False)); print(df["Dept"].value_counts().to_dict())
```
Real printed output (pandas 3.0.5):
```text
 EmpID       Name    Dept
   101   Asha Rao      HR
   102 Ravi Kumar      HR
   103    Meena S Finance
   104 Karan Shah Finance
   105 Priya Nair      HR
{'HR': 3, 'Finance': 2}
```
**Version / licensing note:** Text function behaviour from Microsoft Learn: Text.Trim, Text.Clean, Text.Proper (PowerQuery M).
**Edge cases:** Text.Proper lowercases other letters, so "McDonald" becomes "Mcdonald" and "IT" becomes "It"; handle exceptions in the mapping step. Non-breaking spaces may survive Trim (not checked on the Microsoft page); test.
**Likely follow-ups:** 1) *How to see variants?* Column Distribution or Group By count. 2) *Fuzzy match?* Possible for text merges (Q53).
**Common mistakes:** Cleaning only the display, not the key columns used in merges; typing 20 Replace Values steps instead of using a mapping table.

### Q11 ⭐⭐⭐ 🟡 What is the difference between adding a custom column in Power Query and creating a calculated column in DAX?
**Asked at:** commonly asked (no company-specific report found); the Power Query vs DAX column question is one of the pairings the Part 2 sources highlight as core.
**What the interviewer is checking:** Do you know where each is calculated, and which to use when?
**Say this in the interview:** "A Power Query custom column is created during data loading, in M, before the data reaches the model. A DAX calculated column is created after loading, inside the model, and is calculated on refresh and stored. I prefer Power Query for cleaning and row-level shaping, and DAX for things that need the model, like using relationships or measures."
**Explain simply:**
- Custom column: Add Column > Custom Column, written in **M**. Microsoft: calculated columns, by contrast, are "based on data you've already loaded into the model" (Microsoft Learn: Using calculated columns in Power BI Desktop).
- DAX calculated column: Table tools > New column, written in **DAX**; it calculates a result for every row and is recalculated when data refreshes.
- Calculated columns in Import mode are "materialized" at refresh and can slow refresh (same page).
- Neither reacts to slicers. Only measures do.
**Example:** Tenure band from years of service. Same logic, two places. If the source is SQL, the Power Query version might fold to the database (Q13).
**Sample data:**

Table `Employee`:

| Emp | TenureYears |
|---|---|
| Asha | 0.5 |
| Ravi | 2.0 |
| Meena | 4.5 |
| Karan | 1.0 |

**DAX / Steps (not run here):**
```m
= Table.AddColumn(Source, "Band", each if [TenureYears] <= 1 then "0-1" else if [TenureYears] <= 3 then "1-3" else "3+", type text)
```
```dax
Band = IF ( Employee[TenureYears] <= 1, "0-1", IF ( Employee[TenureYears] <= 3, "1-3", "3+" ) )
```
The DAX shape follows the nested IF pattern on Microsoft Learn: IF function (DAX).
**Alternative:** Do the banding in a measure only if it must react to filters; otherwise add a column. Or use SWITCH instead of nested IF (Microsoft's IF page suggests it for many branches).
**Result:** Reproduced with pandas: Asha 0-1, Ravi 1-3, Meena 3+, Karan 0-1. Both the M and DAX versions are designed to return exactly this; neither was executed here.
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"Emp":["Asha","Ravi","Meena","Karan"],"TenureYears":[0.5,2.0,4.5,1.0]})
# same logic whether written in M (before load) or DAX (after load)
emp["Band"] = emp["TenureYears"].apply(lambda t: "0-1" if t<=1 else ("1-3" if t<=3 else "3+"))
print(emp.to_string(index=False))
```
Real printed output (pandas 3.0.5):
```text
  Emp  TenureYears Band
 Asha          0.5  0-1
 Ravi          2.0  1-3
Meena          4.5   3+
Karan          1.0  0-1
```
**Version / licensing note:** Column locations and materialization from Microsoft Learn: Using calculated columns in Power BI Desktop (updated 2026-08). Smaller model size for Power Query columns: from memory, unverified.
**Edge cases:** DAX can use RELATED to reach other tables; M cannot without a merge. A boundary value like exactly 1.0 must fall in one band only (here 0-1).
**Likely follow-ups:** 1) *Which loads faster?* Depends; Power Query columns need no extra DAX evaluation. 2) *Can a DAX column use a slicer?* No.
**Common mistakes:** Building a calculated column when a measure is needed (totals/ratios); doing text cleaning in DAX (Q46).

### Q12 ⭐⭐⭐ 🟡 How do you combine many monthly Excel or CSV files from one folder into a single table in Power BI?
**Asked at:** commonly asked (no company-specific report found); RADACAD publishes a "combine sheets" tutorial, indicating this is a standard technique.
**What the interviewer is checking:** Can you automate monthly consolidation without copy-paste?
**Say this in the interview:** "I use Get Data > Folder, point to the monthly folder, filter the file list to only the files I need, then Combine & Transform. Power Query builds a sample-file query and a function that is applied to every file, and stacks the results. Next month I drop a new file in the folder and refresh."
**Explain simply:**
- The Folder connector lists every file in the folder and its subfolders. The Content column holds each file's binary data.
- Combine uses the example file you pick to decide how all files are read, so all files need the **same format and structure** (Microsoft Learn: Folder connector, Combine files overview).
- It creates helper queries: Transform Sample File, a function query, and a group named "Transform file from ...".
- Filter unwanted files (like notes.txt or a temp file) **before** combining.
**Example:** Three monthly attendance CSVs (Jan, Feb, Mar) become one table of 6 rows, with a Source column showing the file name.
**Sample data:**

Files in folder: `attendance_Jan.csv` (EmpID 1,2), `attendance_Feb.csv` (1,2), `attendance_Mar.csv` (1,3), and `notes.txt` (ignored).

| File | Rows |
|---|---|
| attendance_Jan.csv | 2 |
| attendance_Feb.csv | 2 |
| attendance_Mar.csv | 2 |

**DAX / Steps (not run here):** Power BI Desktop > Home > Get data > **Folder** > Browse > OK > **Transform Data** > filter the Extension column to .csv (and by Folder Path or Name if needed) > select the Content column > Home > Combine > **Combine Files** > confirm the example file > OK > fix types > Close & Apply.
Simplified hand-written M equivalent (not run here; the UI builds helper queries instead):
```m
let
    Source   = Folder.Files("C:\HR\Attendance"),
    CsvOnly  = Table.SelectRows(Source, each [Extension] = ".csv"),
    Parsed   = Table.AddColumn(CsvOnly, "Data", each Table.PromoteHeaders(Csv.Document([Content], [Delimiter = ",", Encoding = 65001]), [PromoteAllScalars = true])),
    Slim     = Table.SelectColumns(Parsed, {"Name", "Data"}),
    Combined = Table.ExpandTableColumn(Slim, "Data", {"EmpID", "Days"})
in
    Combined
```
**Alternative:** Use a SharePoint folder (same feature). Or put months in one Excel workbook as separate sheets and combine sheets.
**Result:** Reproduced with pandas (reading real temporary CSV files): 6 rows, each tagged with its source file; notes.txt excluded by filtering first.
**Pandas check:**
```python
import pandas as pd, os, tempfile
d = tempfile.mkdtemp()
pd.DataFrame({"EmpID":[1,2],"Days":[20,21]}).to_csv(f"{d}/attendance_Jan.csv",index=False)
pd.DataFrame({"EmpID":[1,2],"Days":[19,22]}).to_csv(f"{d}/attendance_Feb.csv",index=False)
pd.DataFrame({"EmpID":[1,3],"Days":[18,20]}).to_csv(f"{d}/attendance_Mar.csv",index=False)
open(f"{d}/notes.txt","w").write("not a data file")
files = sorted(f for f in os.listdir(d) if f.endswith(".csv"))     # filter the file list FIRST
parts = [pd.read_csv(f"{d}/{f}").assign(Source=f) for f in files]
out = pd.concat(parts, ignore_index=True)
print(out.to_string(index=False))
print("rows:", len(out))
```
Real printed output (pandas 3.0.5):
```text
 EmpID  Days             Source
     1    19 attendance_Feb.csv
     2    22 attendance_Feb.csv
     1    20 attendance_Jan.csv
     2    21 attendance_Jan.csv
     1    18 attendance_Mar.csv
     3    20 attendance_Mar.csv
rows: 6
```
**Version / licensing note:** From Microsoft Learn: Folder connector (updated 2026-10; General availability; Power Query Online needs an on-premises data gateway for folders) and Combine files overview. The folder connector authenticates with Windows credentials per that page.
**Edge cases:** If one month has an extra column or different header, the combine may error or leave nulls. A file open in Excel can leave a ~$ temp file in the folder that breaks combine; filter it out. Microsoft notes adding a Changed Type step after combining can cause a step-level error if column names changed.
**Likely follow-ups:** 1) *What if file layouts differ?* Fix the sample query or standardise the files (Q48). 2) *Can you skip bad files?* The dialog has "Skip files with errors".
**Common mistakes:** Combining everything including non-data files; hard-coding a local path that other users don't have (use a parameter, Q42).

### Q13 ⭐⭐⭐ 🟡 What is query folding, and why does it matter?
**Asked at:** A Glassdoor Power BI question listing (crowd-sourced, undated; seen as a search snippet only) includes "What is query folding, how can we identify whether a query is folded"; recruiter and training blogs (KORE1, Simpliaxis) raise it too. No company is named.
**What the interviewer is checking:** Do you know that some steps are translated into the source database's own query, and why that is faster?
**Say this in the interview:** "Query folding means Power Query translates my steps, like filters and column selection, into the source's language, for example SQL, so the database does the work and sends back only the result. It matters because it is faster and reduces data moved, and it is needed for incremental refresh."
**Explain simply:**
- Power Query tries to push as much work as possible to the source; the rest runs in its own engine (Microsoft Learn: Query evaluation and query folding).
- Three outcomes: **full** folding, **partial** folding, or **none**.
- Sources with a query engine (SQL Server, OData) commonly fold. **CSV and Excel files do not fold**, because they have no query engine.
- Once a step cannot fold, later steps usually run in the Power Query engine too.
**Example:** Employees table with 2 million rows in SQL. Filter Joined >= 2025 and keep two columns. If folded, SQL returns maybe 40,000 narrow rows. If not folded, all 2 million come over first.
**Sample data:** Not meaningful here: folding depends on the source and cannot be simulated with a pandas table. Illustrative only (not run), the folded steps could become SQL like:
```sql
SELECT EmpID, Dept FROM dbo.Employees WHERE Joined >= '2025-01-01'
```
**DAX / Steps (not run here):** Right-click a step in Applied Steps. If **View Native Query** is enabled, that step folds; if greyed out, folding stopped at or before it (availability depends on the connector).
**Alternative:** In Power Query Online, folding indicators beside steps and the Query plan show folding visually (Microsoft says these exist only in Power Query Online).
**Version / licensing note:** Definition, outcomes, sources and the Online-only indicators are from Microsoft Learn: Understanding Query Evaluation and Query Folding in Power Query (updated 2026-08). The page says View Native Query availability depends on the connector.
**Edge cases:** Engine may reorder steps during optimisation. Merging tables from two different sources cannot fold the merge. Custom columns with complex M often break folding (see Q36).
**Likely follow-ups:** 1) *How do you check it?* View Native Query (Q35). 2) *Why does it matter for incremental refresh?* It needs folding so only new partitions are queried (Part 7).
**Common mistakes:** Expecting folding on Excel/CSV; putting a non-foldable step early so every later step runs locally.

### Q14 ⭐⭐ 🟢 What is the M language, and when would you edit it in the Advanced Editor?
**Asked at:** commonly asked (no company-specific report found); "M language" appears in generic Power BI question lists (Zero To Mastery, Imarticus, Analytics Vidhya) with no company named.
**What the interviewer is checking:** Do you know that every Power Query click is code, and when you would touch it?
**Say this in the interview:** "M is the Power Query formula language. Every step I click generates M code. I open the Advanced Editor when I need something the buttons don't offer, to copy a query, rename steps in bulk, or fix a hard-coded value."
**Explain simply:**
- A query is a `let ... in` script: each line is a step, and the last line after `in` is the result (Microsoft Learn: Query evaluation and query folding calls the M script "a recipe").
- Open it with View > Advanced Editor (also Home > Query > Advanced Editor).
- M is case-sensitive.
- You can write M by hand for custom logic, parameters, functions.
**Example:** Same pipeline as three clicks: keep salary >= 40000, standardise department text, drop Salary.
**Sample data:**

Table `Src`:

| EmpID | Dept | Salary |
|---|---|---|
| 1 | " hr" | 40000 |
| 2 | Finance | 52000 |
| 3 | "hr " | 38000 |
| 4 | IT | 60000 |

**DAX / Steps (M code, not run here):**
```m
let
    Source   = Src,
    Filtered = Table.SelectRows(Source, each [Salary] >= 40000),
    Cleaned  = Table.TransformColumns(Filtered, {{"Dept", each Text.Upper(Text.Trim(_)), type text}}),
    Slim     = Table.RemoveColumns(Cleaned, {"Salary"})
in
    Slim
```
**Alternative:** Edit just one step in the formula bar (View > Formula Bar) instead of opening the whole script.
**Result:** Reproduced with pandas: rows for EmpID 1, 2 and 4 remain, with Dept HR, FINANCE, IT and no Salary column.
**Pandas check:**
```python
import pandas as pd
src = pd.DataFrame({"EmpID":[1,2,3,4],"Dept":[" hr","Finance","hr ","IT"],"Salary":[40000,52000,38000,60000]})
step1 = src[src["Salary"]>=40000]                         # Table.SelectRows
step2 = step1.assign(Dept=step1["Dept"].str.strip().str.upper())   # Table.TransformColumns
step3 = step2.drop(columns=["Salary"])                    # Table.RemoveColumns
print(step3.to_string(index=False))
```
Real printed output (pandas 3.0.5):
```text
 EmpID    Dept
     1      HR
     2 FINANCE
     4      IT
```
**Version / licensing note:** Advanced Editor location and the let/in description from Microsoft Learn: Use Power Query to Transform Data, and Query Evaluation and Query Folding. Microsoft's Query Overview page says the editor is in both the new (preview) and legacy experience, with some controls differing.
**Edge cases:** Hand-editing can switch off the friendly dialog for a step. Step names with spaces appear as `#"Changed Type"`.
**Likely follow-ups:** 1) *Do you need to learn M?* Basic reading helps; most work is by clicks. 2) *Where to get help on a function?* Insert step, type `= FunctionName` in the formula bar (Microsoft's inline help).
**Common mistakes:** Typos in case (`table.selectrows` fails); pasting M without checking that source paths exist.

### Q15 ⭐⭐ 🟢 How do you promote the first row to headers, and how do you remove top rows from a messy Excel report?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you handle the typical "report with a title on top" Excel export?
**Say this in the interview:** "I use Remove Top Rows to delete the title lines, then Use First Row as Headers so the real column names become headers. If footers exist I use Remove Bottom Rows."
**Explain simply:**
- Remove top rows first, so the header row becomes row 1; then promote (Microsoft Learn: Promote or demote column headers).
- Remove Top Rows is under Home > Reduce Rows > Remove Rows, or the table menu (Microsoft Learn: Filter a table by row position).
- Promote makes column names unique by adding a dot-number suffix if a header repeats.
- Order matters: if you promote first, the title line becomes the header.
**Example:** A payroll export has 2 title lines, then the header EmpID, Name, Days, then data.
**Sample data:**

Table `Raw` (as Power Query first sees it):

| Column1 | Column2 | Column3 |
|---|---|---|
| Monthly Attendance Report | null | null |
| Generated 05-Oct | null | null |
| EmpID | Name | Days |
| 101 | Asha | 20 |
| 102 | Ravi | 18 |
| 103 | Meena | 22 |

**DAX / Steps (M code, not run here):**
```m
let
    Sheet    = Source{[Item = "Report", Kind = "Sheet"]}[Data],
    NoTop    = Table.Skip(Sheet, 2),
    Promoted = Table.PromoteHeaders(NoTop, [PromoteAllScalars = true])
in
    Promoted
```
Click-path: table menu (top-left of preview) > **Remove Top Rows** > 2 > OK; Home > Transform group > **Use First Row as Headers**.
**Alternative:** Keep Range of Rows if the header block has fixed start and length.
**Result:** Reproduced with pandas: after skipping 2 rows and promoting, columns are EmpID, Name, Days with 3 data rows.
**Pandas check:**
```python
import pandas as pd
raw = pd.DataFrame([["Monthly Attendance Report",None,None],
                    ["Generated 05-Oct",None,None],
                    ["EmpID","Name","Days"],
                    [101,"Asha",20],[102,"Ravi",18],[103,"Meena",22]])
step_a = raw.iloc[2:].reset_index(drop=True)          # Remove top rows = 2
step_b = step_a.iloc[1:].copy(); step_b.columns = step_a.iloc[0].tolist()   # Use first row as headers
step_b = step_b.reset_index(drop=True)
print(step_b.to_string(index=False)); print(list(step_b.columns))
```
Real printed output (pandas 3.0.5):
```text
EmpID  Name Days
  101  Asha   20
  102  Ravi   18
  103 Meena   22
['EmpID', 'Name', 'Days']
```
**Version / licensing note:** Menu locations from Microsoft Learn: Promote or demote column headers (2024) and Filter a table by row position (2022 date on page; updated 2024).
**Edge cases:** If the number of title lines changes, the fixed number breaks; use a filter on a column pattern instead. Excel connector can add its own Promoted Headers step automatically (Q52).
**Likely follow-ups:** 1) *How to remove footers?* Remove Bottom Rows. 2) *Demote?* Home > Transform > Use Headers as First Row.
**Common mistakes:** Promoting before removing the title rows; forgetting to reset data types afterwards.

### Q16 ⭐⭐ 🟢 What is the difference between Remove Columns and Choose Columns, and why remove unused columns before loading?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know choose = keep list, remove = drop list, and the effect on future columns?
**Say this in the interview:** "Remove Columns drops the ones I select; Choose Columns lets me tick the ones to keep. If the source adds a new column later, Remove Columns lets it in, while Choose Columns keeps it out. I remove unused columns before loading to keep the model small and fast."
**Explain simply:**
- **Remove Columns** = blacklist; **Remove Other Columns** = keep only selected; **Choose Columns** = a dialog with check boxes (Microsoft Learn: Choose or remove columns).
- Microsoft's best-practices page lists Choose Columns as the step for sources whose column count changes but you need only specific ones.
- Fewer columns means less memory and faster refresh and a cleaner field list (general principle; exact savings from memory, unverified).
**Example:** The HR export has Aadhaar and personal notes you do not need in a dashboard. Removing them also reduces privacy risk.
**Sample data:**

Table `Export` columns: EmpID, Name, Salary, Aadhaar, Notes. Next month the source adds Phone.

**DAX / Steps (M code, not run here):**
```m
= Table.RemoveColumns(Source, {"Aadhaar", "Notes"})
= Table.SelectColumns(Source, {"EmpID", "Name", "Salary"})
```
Click-path: Home > Manage Columns > **Choose Columns** or **Remove Columns** (drop-down: Remove Columns / Remove Other Columns).
**Alternative:** Hide columns in the model view; weaker, because the data is still loaded.
**Result:** Reproduced with pandas: next month the Remove version returns EmpID, Name, Salary, Phone; the Choose version returns only EmpID, Name, Salary.
**Pandas check:**
```python
import pandas as pd
v1 = pd.DataFrame({"EmpID":[1,2],"Name":["Asha","Ravi"],"Salary":[40000,52000],"Aadhaar":["x1","x2"],"Notes":["a","b"]})
v2 = v1.assign(Phone=["99","98"])            # source adds a column next month
remove = lambda d: d.drop(columns=["Aadhaar","Notes"])          # Remove Columns (blacklist)
choose = lambda d: d[["EmpID","Name","Salary"]]                  # Choose Columns (whitelist)
print("Remove cols, next month:", list(remove(v2).columns))
print("Choose cols, next month:", list(choose(v2).columns))
```
Real printed output (pandas 3.0.5):
```text
Remove cols, next month: ['EmpID', 'Name', 'Salary', 'Phone']
Choose cols, next month: ['EmpID', 'Name', 'Salary']
```
**Version / licensing note:** Menu locations from Microsoft Learn: Choose or remove columns, and Best Practices When Working with Power Query (2026-08).
**Edge cases:** Choose Columns errors if a chosen column disappears from the source (Q48). Sensitive columns should be removed, not just hidden.
**Likely follow-ups:** 1) *Hide vs remove?* Hide keeps data in the model. 2) *Remove Other Columns?* Same effect as choose.
**Common mistakes:** Loading every column "just in case"; using Remove Columns when the source layout keeps changing.

### Q17 ⭐⭐ 🟢 How do you split a column by a delimiter in Power Query (for example, splitting Full Name)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you split text sensibly and know the left-most vs each-occurrence choice?
**Say this in the interview:** "Select the column, Home > Split Column > By Delimiter, choose Space, pick Left-most delimiter for first name versus the rest, then rename the new columns, for example from FullName.1 and FullName.2."
**Explain simply:**
- Three entry points: Home > Split Column, Transform > Split Column, or right-click the column (Microsoft Learn: Split columns by delimiter).
- **Left-most delimiter** splits at the first space only; **Right-most** at the last; **Each occurrence** at every space.
- You can split into **columns** or **rows**.
- New columns are named like `FullName.1`, `FullName.2`.
**Example:** "Meena Iyer Nair": left-most gives First = Meena, Last = Iyer Nair; right-most gives Rest = Meena Iyer, Last = Nair.
**Sample data:**

Table `Names`:

| FullName |
|---|
| Asha Rao |
| Ravi Kumar |
| Meena Iyer Nair |
| Karan |

**DAX / Steps (M code, not run here):**
```m
= Table.SplitColumn(Source, "FullName", Splitter.SplitTextByEachDelimiter({" "}, QuoteStyle.None, false), {"First", "Last"})
```
The exact splitter function the UI generates is from memory, unverified. Click-path: select FullName > Home > **Split Column** > **By Delimiter** > Space > Left-most delimiter > OK.
**Alternative:** Column From Examples (Q49) or Text.BeforeDelimiter and Text.AfterDelimiter in a custom column.
**Result:** Reproduced with pandas: left-most split gives (Asha, Rao), (Ravi, Kumar), (Meena, "Iyer Nair"), (Karan, null); right-most gives (Asha, Rao), (Ravi, Kumar), ("Meena Iyer", Nair), (Karan, null).
**Pandas check:**
```python
import pandas as pd
df = pd.DataFrame({"FullName":["Asha Rao","Ravi Kumar","Meena Iyer Nair","Karan"]})
print(df["FullName"].str.split(" ",n=1,expand=True).rename(columns={0:"First",1:"Last"}))     # left-most delimiter
print(df["FullName"].str.rsplit(" ",n=1,expand=True).rename(columns={0:"Rest",1:"Last"}))     # right-most delimiter
```
Real printed output (pandas 3.0.5):
```text
   First       Last
0   Asha        Rao
1   Ravi      Kumar
2  Meena  Iyer Nair
3  Karan        NaN
         Rest   Last
0        Asha    Rao
1        Ravi  Kumar
2  Meena Iyer   Nair
3       Karan    NaN
```
**Version / licensing note:** Options and menu locations from Microsoft Learn: Split columns by delimiter (2025-07). Desktop and Online dialogs differ in layout, same options.
**Edge cases:** Single-word names leave Last null. Power Query decides how many columns from the data it sees; a later file with more pieces can lose them, so check column count when data changes (reported in community threads, not verified by Microsoft's page).
**Likely follow-ups:** 1) *Split into rows?* Choose Rows under Advanced (for lists like "Python; SQL"). 2) *Initials?* Use Column From Examples.
**Common mistakes:** Splitting at each space and getting 3-4 columns; forgetting to trim before splitting.

### Q18 ⭐⭐ 🟢 What do Trim, Clean and Capitalize Each Word do in Power Query?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you tell these three apart and apply them in the right order?
**Say this in the interview:** "Trim removes spaces from the start and end. Clean removes hidden non-printing characters like line breaks. Capitalize Each Word makes the first letter of every word upper-case and the rest lower-case. Together they fix most messy name columns."
**Explain simply:**
- **Trim** = Text.Trim: removes leading and trailing whitespace by default (not the spaces inside).
- **Clean** = Text.Clean: removes control characters such as a line feed, e.g. "ABC" + line feed + "D" becomes "ABCD". It does not remove normal spaces.
- **Capitalize Each Word** = Text.Proper: first letter of each word upper-case, "All other letters are returned in lowercase" (Microsoft Learn: Text.Proper).
- Menu: Transform > Format (Text column group) > lowercase, UPPERCASE, Capitalize Each Word, Trim, Clean.
**Example:** "  aSHA   rao " and "RAVI" + line break + "KUMAR" need different fixes.
**Sample data:**

Table `Names` values: "  aSHA   rao ", "RAVI(line break)KUMAR", "meena nair".

**DAX / Steps (M code, not run here):**
```m
= Table.TransformColumns(Source, {{"Name", Text.Trim, type text}})
= Table.TransformColumns(Source, {{"Name", Text.Clean, type text}})
= Table.TransformColumns(Source, {{"Name", Text.Proper, type text}})
```
**Alternative:** Combine them: `each Text.Proper(Text.Trim(Text.Clean(_)))`.
**Result:** Reproduced with pandas: Trim gives "aSHA   rao" (inner spaces stay), "RAVI line-break KUMAR", "meena nair"; Clean gives "RAVIKUMAR" for the second value and leaves spaces in the others; Trim + collapse spaces + Proper gives "Asha Rao", "Ravi Kumar", "Meena Nair". Note Clean removed the line break without leaving a space, so "RAVIKUMAR" is joined.
**Pandas check:**
```python
import pandas as pd
s = pd.Series(["  aSHA   rao ", "RAVI\nKUMAR", "meena nair"])
print(s.str.strip().tolist())                                   # Trim: ends only
print(s.str.replace(r"[\x00-\x1f]","",regex=True).tolist())     # Clean: control chars (the newline) removed
print(s.str.strip().str.replace(r"\s+"," ",regex=True).str.title().tolist())
```
Real printed output (pandas 3.0.5):
```text
['aSHA   rao', 'RAVI\nKUMAR', 'meena nair']
['  aSHA   rao ', 'RAVIKUMAR', 'meena nair']
['Asha Rao', 'Ravi Kumar', 'Meena Nair']
```
**Version / licensing note:** Behaviour from Microsoft Learn: Text.Trim, Text.Clean, Text.Proper (PowerQuery M); the ribbon label "Capitalize Each Word" maps to Text.Proper: from memory, unverified.
**Edge cases:** Text.Proper turns "IT" into "It" and "McDonald" into "Mcdonald". Replace line breaks with a space before Clean if words would stick together.
**Likely follow-ups:** 1) *Trim inner spaces?* Split and rejoin (Q10). 2) *Does Trim fix nulls?* Null stays null.
**Common mistakes:** Expecting Trim to remove double spaces in the middle; using Clean to remove normal spaces.

### Q19 ⭐⭐ 🟢 What is the difference between Replace Values and Replace Errors?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know one swaps matching values and the other swaps error cells?
**Say this in the interview:** "Replace Values finds a specific value I choose, like NA or -1, and swaps it. Replace Errors is for cells already showing Error, usually after a failed type conversion, and gives them a value. If I convert a column to number and NA becomes an error, I fix it with Replace Errors, or better, replace NA before converting."
**Explain simply:**
- **Replace Values**: Home > Transform > Replace Values, or right-click. For text columns it replaces instances of a string; for non-text it replaces whole cell contents; advanced option "Match entire cell contents" exists (Microsoft Learn: Replace values and errors).
- **Replace Errors**: Transform > Any Column > Replace Values drop-down > Replace Errors (Microsoft Learn: Dealing with errors).
- Related: Remove Errors (Home > Remove Rows) and Keep Errors for auditing.
**Example:** A Salary column has "NA" and "n/a" text. Changing type to number turns both into errors.
**Sample data:**

Table `Pay`:

| Emp | Salary (text) |
|---|---|
| Asha | 40000 |
| Ravi | NA |
| Meena | 35000 |
| Karan | n/a |

**DAX / Steps (M code, not run here):**
```m
= Table.ReplaceValue(Source, "NA", "0", Replacer.ReplaceText, {"Salary"})
= Table.ReplaceErrorValues(Typed, {{"Salary", 0}})
```
**Alternative:** Remove Errors to drop those rows when 0 would distort averages.
**Result:** Reproduced with pandas: replacing "NA" fixes only Ravi (Karan's "n/a" remains); converting to number produces 2 errors; replacing errors with 0 gives 40000, 0, 35000, 0.
**Pandas check:**
```python
import pandas as pd
df = pd.DataFrame({"Emp":["Asha","Ravi","Meena","Karan"],"Salary":["40000","NA","35000","n/a"]})
print("Replace Values (text->text) 'NA' -> '0':", df["Salary"].replace("NA","0").tolist())
num = pd.to_numeric(df["Salary"], errors="coerce")        # errors appear (shown as NaN here)
print("errors after type change:", int(num.isna().sum()))
print("Replace Errors with 0:", num.fillna(0).tolist())
```
Real printed output (pandas 3.0.5):
```text
Replace Values (text->text) 'NA' -> '0': ['40000', '0', '35000', 'n/a']
errors after type change: 2
Replace Errors with 0: [40000.0, 0.0, 35000.0, 0.0]
```
**Version / licensing note:** Menu paths from Microsoft Learn: Replace values and errors (2024) and Dealing with errors (2025-06).
**Edge cases:** Replace Values is case-sensitive and finds only the exact value. Replace Errors hides real problems; check Column Quality first (Q23). Replacing errors with 0 can distort averages.
**Likely follow-ups:** 1) *Why not just remove errors?* You lose rows. 2) *Step-level vs cell-level errors?* Step-level stops the query; cell-level shows Error in cells (Q39).
**Common mistakes:** Using Replace Values on a cell that is an error (it cannot match); replacing all errors with 0 without checking why.

### Q20 ⭐⭐ 🟢 How do you use Fill Down and Fill Up, and when are they needed?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you reshape "grouped header" reports where a value is written once and left blank below?
**Say this in the interview:** "Fill Down copies the last non-null value into the null cells below it. Fill Up does the reverse. I need them when a report shows a department or date once at the top of a block and leaves the rest of the rows blank."
**Explain simply:**
- Right-click the column > **Fill** > **Down** or **Up**, or Transform > Fill (Microsoft Learn: Fill values in a column).
- Fill only works on **null**. If cells look empty but are empty text, first Replace Values blank with null.
- Fill Down is the common one; Fill Up helps when the label is under the rows.
**Example:** Department appears once per block in an exported headcount sheet; Fill Down gives every employee a department.
**Sample data:**

Table `Report`:

| Dept | Emp | Note |
|---|---|---|
| HR | Asha | null |
| null | Ravi | null |
| null | Meena | Manager: Rao |
| Finance | Karan | null |
| null | Priya | Manager: Shah |

**DAX / Steps (M code, not run here):**
```m
let
    Down = Table.FillDown(Source, {"Dept"}),
    Up   = Table.FillUp(Down, {"Note"})
in
    Up
```
**Alternative:** Group By with an "All rows" operation, or add an index and compare, for harder layouts.
**Result:** Reproduced with pandas: Dept becomes HR, HR, HR, Finance, Finance; Note becomes Manager: Rao (rows 1-3) and Manager: Shah (rows 4-5).
**Pandas check:**
```python
import pandas as pd
df = pd.DataFrame({"Dept":["HR",None,None,"Finance",None],
                   "Emp":["Asha","Ravi","Meena","Karan","Priya"],
                   "Note":[None,None,"Manager: Rao",None,"Manager: Shah"]})
df["Dept"] = df["Dept"].ffill()          # Fill Down
df["Note"] = df["Note"].bfill()          # Fill Up
print(df.to_string(index=False))
```
Real printed output (pandas 3.0.5):
```text
   Dept   Emp          Note
     HR  Asha  Manager: Rao
     HR  Ravi  Manager: Rao
     HR Meena  Manager: Rao
Finance Karan Manager: Shah
Finance Priya Manager: Shah
```
**Version / licensing note:** Menu path and the null note from Microsoft Learn: Fill values in a column (page dated 2024-06).
**Edge cases:** Fill Down cannot fill the first rows if they start null. Sorting before filling scrambles the logic: fill first, then sort.
**Likely follow-ups:** 1) *Fill empty-looking cells?* Replace "" with null first. 2) *Fill between columns?* Not directly; use a custom column.
**Common mistakes:** Sorting before filling; forgetting to convert empty text to null.

### Q21 ⭐⭐ 🟢 What is the difference between a Custom Column and a Conditional Column in Power Query?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the no-code if/else dialog versus the free-form M formula?
**Say this in the interview:** "A Conditional Column is a point-and-click if-then-else builder, good for banding or labels. A Custom Column lets me write any M formula, like a calculation using several columns. Conditional is quicker for simple rules; custom is for anything the dialog cannot express."
**Explain simply:**
- **Conditional Column**: Add Column > General > Conditional Column. Clauses are tested top to bottom, then a final Else (Microsoft Learn: Add a conditional column).
- **Custom Column**: Add Column > Custom Column; you write an M formula, such as `[Units] * [Unit Price]` (Microsoft Learn: Add a custom column).
- New conditional columns have no data type; set one (same for Desktop custom columns, where the Data type picker is not available).
- Behind the scenes, a conditional column is just an `if ... then ... else` in M.
**Example:** Rating bands (Top/Good/Low) via conditional; bonus = salary x rating / 10 via custom.
**Sample data:**

Table `Perf`:

| Emp | Rating | Salary |
|---|---|---|
| Asha | 5 | 40000 |
| Ravi | 3 | 52000 |
| Meena | 4 | 35000 |
| Karan | 2 | 60000 |

**DAX / Steps (M code, not run here):**
```m
= Table.AddColumn(Source, "Band", each if [Rating] >= 5 then "Top" else if [Rating] >= 3 then "Good" else "Low", type text)
= Table.AddColumn(Source, "Bonus", each [Salary] * [Rating] / 10, type number)
```
**Alternative:** Write the conditional as a custom column directly (same M), or use DAX SWITCH in the model (Q11).
**Result:** Reproduced with pandas: Bands are Top, Good, Good, Low; bonuses are 20000, 15600, 14000, 12000.
**Pandas check:**
```python
import pandas as pd, numpy as np
df = pd.DataFrame({"Emp":["Asha","Ravi","Meena","Karan"],"Rating":[5,3,4,2],"Salary":[40000,52000,35000,60000]})
df["Band"] = np.select([df.Rating>=5, df.Rating>=3],["Top","Good"],default="Low")    # Conditional column
df["Bonus"] = df.Salary*df.Rating/10                                                 # Custom column: any formula
print(df.to_string(index=False))
```
Real printed output (pandas 3.0.5):
```text
  Emp  Rating  Salary Band   Bonus
 Asha       5   40000  Top 20000.0
 Ravi       3   52000 Good 15600.0
Meena       4   35000 Good 14000.0
Karan       2   60000  Low 12000.0
```
**Version / licensing note:** From Microsoft Learn: Add a conditional column (updated 2026-06) and Add a custom column (2025-08, updated 2026-08). Online has a Data type picker in the custom column dialog; Desktop does not, per that page.
**Edge cases:** Clause order matters (put the strictest first). Column names in M are case-sensitive. Null in a comparison gives null, so add a null check.
**Likely follow-ups:** 1) *Which folds better?* Simple conditional logic can fold; complex custom M may not (Q36). 2) *Can the dialog edit a custom step?* Microsoft says simple formulas become a friendly dialog.
**Common mistakes:** Wrong clause order giving everyone "Good"; forgetting to set the new column's type.

### Q22 ⭐⭐ 🟢 How do you use Group By in Power Query (for example, headcount by department)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can summarise rows into one row per category before loading.
**Say this in the interview:** "Group By collapses many rows into one row per group, and I pick the summary I want, for example Count Rows for headcount or Sum for salary. I use it when I want the summary table itself, not when a DAX measure on the detail data would do."
**Explain simply:**
- "Group" means rows with the same value in a column (the same Department) are bundled together.
- Each bundle becomes one row; you choose what to calculate for it: Count Rows, Count Distinct Rows, Sum, Average, Min, Max.
- The Advanced option lets you group by several columns (Department + Location) and add several summaries at once.
- The detail rows are gone after this step, so keep the original query if you still need them (see Q32, Reference).
**Example:** 6 employees, headcount and total salary per department.
**Sample data:** Table `Employees`

| EmpID | Dept | Salary |
|---|---|---|
| 101 | Sales | 40000 |
| 102 | Sales | 45000 |
| 103 | HR | 38000 |
| 104 | HR | 42000 |
| 105 | HR | 50000 |
| 106 | IT | 60000 |

**DAX / Steps:** Power Query M, **not run here**. Click-path: Transform tab > Table group > Group By > Basic: choose Dept, new column name Headcount, operation Count Rows > OK. For two results choose Advanced > Add aggregation.
```m
Table.Group(Employees, {"Dept"}, {
  {"Headcount", each Table.RowCount(_), Int64.Type},
  {"TotalSalary", each List.Sum([Salary]), type number}
})
```
**Alternative:** Skip the grouping and write a DAX measure `Headcount = COUNTROWS(Employees)` on the detail table; the report then groups by Dept automatically and stays flexible.
**Result:** Reproduced with pandas (not run in Power Query): HR 3 / 130000, IT 1 / 60000, Sales 2 / 85000.
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"EmpID":[101,102,103,104,105,106],
                    "Dept":["Sales","Sales","HR","HR","HR","IT"],
                    "Salary":[40000,45000,38000,42000,50000,60000]})
out = emp.groupby("Dept").agg(Headcount=("EmpID","count"), TotalSalary=("Salary","sum")).reset_index()
print(out.to_string(index=False))
```
Real printed output (pandas 3.0.5):
```text
 Dept  Headcount  TotalSalary
   HR          3       130000
   IT          1        60000
Sales          2        85000
```
**Version / licensing note:** Group By exists in Power Query in Desktop and the Service dataflows; menu names from memory, unverified (learn.microsoft.com could not be reached from this session).
**Edge cases:** Blank department values form their own group (null); Count Rows counts rows, Count Distinct counts unique values; Group By on a folding source usually folds to SQL GROUP BY (from memory, unverified).
**Likely follow-ups:** (1) "Count Rows vs Count Distinct?" Rows counts every row; Distinct counts unique values of a chosen column. (2) "Group By or DAX?" DAX if the report should slice it; Group By if you want a smaller table.
**Common mistakes:** Grouping and losing the detail you still need; forgetting that spelling variants ("hr", "HR ") create separate groups.

### Q23 ⭐⭐ 🟢 What are the Column Quality, Column Distribution and Column Profile tools in Power Query?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you profile (inspect) data before trusting it.
**Say this in the interview:** "They are the data-profiling switches on the View tab. Column Quality shows the percent Valid, Error and Empty; Column Distribution shows how many distinct and unique values there are; Column Profile gives full statistics and a value chart for one selected column."
**Explain simply:**
- Column Quality: a small bar under each header with Valid / Error / Empty percentages. It tells you at a glance if a column has blanks or errors.
- Column Distribution: a mini bar chart per column plus counts of Distinct (different values) and Unique (values appearing exactly once). A "unique" count equal to the row count suggests a key column such as EmpID.
- Column Profile: a large panel for the selected column with statistics (count, min, max, average, etc.) and a value-frequency chart.
- By default the profile looks only at the first 1,000 rows; the status bar at the bottom can switch it to the entire data set (from memory, unverified; the sources file lists this option as unconfirmed). Profiling the whole set is slower on big data.
**Example:** In an attendance extract, Column Quality shows 8% Empty in `ExitDate`; that is expected (active staff) but 8% Empty in `EmpID` is a problem.
**DAX / Steps:** Menu click-path, **not run here**: View tab > Data Preview group > tick Column quality, Column distribution, Column profile.
**Alternative:** Use Home > Keep Rows > ... or sort/filter to eyeball problems; or in Excel use a pivot table of counts. Profiling is quicker.
**Version / licensing note:** Available in Power BI Desktop's Power Query Editor; the Power Query best-practices page (per research/Book04_Part02_sources.md, fetched in the research wave) lists profiling tools. Exact menu text from memory, unverified.
**Edge cases:** Judging "100% valid" from the first 1,000 rows can miss errors further down.
**Likely follow-ups:** (1) "Where do errors come from?" Bad type conversions (Q39). (2) "Does profiling change the data?" No, it only displays.
**Common mistakes:** Trusting the default 1,000-row sample; confusing Distinct with Unique.

### Q24 ⭐⭐ 🟢 How do you extract the year, month name or day of week from a date column in Power Query?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know the Add Column > Date menu and the date type requirement.
**Say this in the interview:** "I make sure the column is typed as Date, then use Add Column > Date > Year, Month > Name of Month, Day > Name of Day. Using Add Column keeps the original date."
**Explain simply:**
- The column must have the Date (or Date/Time) data type, otherwise the Date menu is greyed out.
- Add Column > Date creates a new column; Transform > Date replaces the existing column. Prefer Add Column.
- "Day of Week" gives a number (0 or 1 based depending on which first day you choose in the dialog); "Name of Day" gives text such as Wednesday.
**Example:** Joining dates of new hires, to see hires by month.
**Sample data:** Table `Hires`

| EmpID | JoinDate |
|---|---|
| 101 | 2025-01-15 |
| 102 | 2024-07-04 |
| 103 | 2023-12-31 |

**DAX / Steps:** M, **not run here**. Click-path: select JoinDate > Add Column tab > From Date & Time group > Date > Year / Month > Name of Month / Day > Name of Day.
```m
Table.AddColumn(Hires, "Year", each Date.Year([JoinDate]), Int64.Type)
Table.AddColumn(Hires, "MonthName", each Date.MonthName([JoinDate]), type text)
Table.AddColumn(Hires, "DayName", each Date.DayOfWeekName([JoinDate]), type text)
```
(chain each AddColumn as its own step, or use `Date.DayOfWeek([JoinDate], Day.Sunday)` for a number).
**Alternative:** Do it in a DAX calculated column `YEAR(...)`, `FORMAT(...,"mmmm")`, but Power Query is preferred for fixed cleaning (Q46); best of all, use a calendar table (Q54).
**Result:** Reproduced with pandas: 2025-01-15 = 2025, January, Wednesday; 2024-07-04 = 2024, July, Thursday; 2023-12-31 = 2023, December, Sunday (Sunday-first numbering 0).
**Pandas check:**
```python
import pandas as pd
d = pd.DataFrame({"EmpID":[101,102,103], "JoinDate":pd.to_datetime(["2025-01-15","2024-07-04","2023-12-31"])})
d["Year"] = d.JoinDate.dt.year
d["MonthName"] = d.JoinDate.dt.month_name()
d["DayName"] = d.JoinDate.dt.day_name()
d["DayOfWeek_SundayFirst0"] = (d.JoinDate.dt.dayofweek + 1) % 7   # pandas Monday=0; shift so Sunday=0
print(d.to_string(index=False))
```
Real printed output (pandas 3.0.5):
```text
 EmpID   JoinDate  Year MonthName   DayName  DayOfWeek_SundayFirst0
   101 2025-01-15  2025   January Wednesday                       3
   102 2024-07-04  2024      July  Thursday                       4
   103 2023-12-31  2023  December    Sunday                       0
```
**Version / licensing note:** From memory, unverified (Microsoft Learn not reachable here). Month and day names follow the Power Query culture setting, from memory, unverified.
**Edge cases:** Text dates (Q41) fail until converted; nulls stay null; month names sort alphabetically in a report unless you add a month-number column and use Sort by Column.
**Likely follow-ups:** (1) "Why sort by month number?" Otherwise April comes before January. (2) "Fiscal year?" Add a custom column with a rule.
**Common mistakes:** Extracting from a text column; using Transform (which overwrites) instead of Add Column.

### Q25 ⭐⭐ 🟢 What is the difference between Pivot Column and Unpivot Columns?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand wide vs long tables.
**Say this in the interview:** "Pivot turns values of one column into new column headers (long to wide). Unpivot does the reverse: it turns many columns into rows of attribute and value (wide to long). Reports and the data model prefer the long form."
**Explain simply:**
- Long table: one row per employee per month. Wide table: one column per month. Excel users naturally make wide tables.
- Pivot Column needs a Values column and an aggregation (Sum, Count...) because several rows can land in one cell; "Don't Aggregate" works only if each combination is unique.
- Unpivot gives two columns: Attribute (old headers) and Value.
**Example:** Leaves taken per employee per month.
**Sample data:** Table `LeavesLong` (long) and the pivoted wide form

| Emp | Month | Leaves |
|---|---|---|
| Asha | Jan | 2 |
| Asha | Feb | 1 |
| Ravi | Jan | 0 |
| Ravi | Feb | 3 |

| Emp | Jan | Feb |
|---|---|---|
| Asha | 2 | 1 |
| Ravi | 0 | 3 |

**DAX / Steps:** M, **not run here**. Pivot: select Month > Transform tab > Any Column group > Pivot Column > Values Column = Leaves > Advanced > Sum. Unpivot: select Emp > right-click > Unpivot Other Columns.
```m
Table.Pivot(LeavesLong, List.Distinct(LeavesLong[Month]), "Month", "Leaves", List.Sum)
Table.UnpivotOtherColumns(Wide, {"Emp"}, "Month", "Leaves")
```
**Alternative:** For a report you rarely need Pivot; a matrix visual pivots at display time without changing the data.
**Result:** Reproduced with pandas: pivot gives Asha 2/1, Ravi 0/3; unpivot returns the 4 long rows back. With a duplicate row (Asha, Jan: 2 and 1) the Sum aggregation gives 3.
**Pandas check:**
```python
import pandas as pd
long = pd.DataFrame({"Emp":["Asha","Asha","Ravi","Ravi"],"Month":["Jan","Feb","Jan","Feb"],"Leaves":[2,1,0,3]})
w = long.pivot(index="Emp", columns="Month", values="Leaves")[["Jan","Feb"]]   # keep Jan, Feb order
print(w)
back = w.reset_index().melt(id_vars="Emp", var_name="Month", value_name="Leaves")
print("unpivot rows:", len(back))
dup = pd.concat([long, pd.DataFrame({"Emp":["Asha"],"Month":["Jan"],"Leaves":[1]})], ignore_index=True)
print(dup.pivot_table(index="Emp", columns="Month", values="Leaves", aggfunc="sum")[["Jan","Feb"]])
try:
    dup.pivot(index="Emp", columns="Month", values="Leaves")
except ValueError as e:
    print("no aggregation ->", type(e).__name__)
```
Real printed output (pandas 3.0.5):
```text
Month  Jan  Feb
Emp            
Asha     2    1
Ravi     0    3
unpivot rows: 4
Month  Jan  Feb
Emp            
Asha     3    1
Ravi     0    3
no aggregation -> ValueError
```
**Version / licensing note:** Both are core Power Query transforms; menu names from memory, unverified. Unpivot options are described on the Microsoft Learn "Unpivot columns" page (per sources file, fetched in the research wave).
**Edge cases:** Pivot with duplicates and no aggregation raises an error; null cells are dropped on unpivot.
**Likely follow-ups:** (1) "Which is better for a model?" Long. (2) "What happens to blanks?" Unpivot drops null values.
**Common mistakes:** Pivoting with the wrong Values column; leaving a wide month-per-column table in the model.

### Q26 ⭐⭐ 🟢 After merging two queries you see a column of Table values. What do you do next?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know the merge result must be expanded.
**Say this in the interview:** "Merge adds the matching rows of the second query as one nested Table column. I click the expand icon in its header, pick the columns I need, untick the prefix option if the names are already clear, and click OK. If I only need a summary I choose Aggregate instead."
**Explain simply:**
- The cell says "Table" because each row holds the matching rows of the other query, which could be one, many or none.
- Expand turns those nested rows into normal columns (a one-to-many match repeats the left row).
- Aggregate (the second option in the icon pop-up) collapses them with Sum, Count, etc.
- Untick "Use original column name as prefix" to avoid names like `Departments.DeptName`.
**Example:** Employees merged with Departments on DeptID.
**Sample data:** Tables `Employees` and `Departments`

| EmpID | DeptID |
|---|---|
| 1 | 10 |
| 2 | 20 |
| 3 | 30 |

| DeptID | DeptName |
|---|---|
| 10 | Sales |
| 20 | HR |

**DAX / Steps:** **Not run here.** Home tab > Combine group > Merge Queries > choose both tables and DeptID > Left Outer > OK > click the double-arrow icon on the new column > tick DeptName > OK.
```m
Table.ExpandTableColumn(Merged, "Departments", {"DeptName"}, {"DeptName"})
```
**Alternative:** Skip the merge and create a relationship in the model (Q38).
**Result:** Reproduced with pandas: EmpID 1 Sales, 2 HR, 3 null (no match).
**Pandas check:**
```python
import pandas as pd
e = pd.DataFrame({"EmpID":[1,2,3],"DeptID":[10,20,30]})
dp = pd.DataFrame({"DeptID":[10,20],"DeptName":["Sales","HR"]})
print(e.merge(dp, on="DeptID", how="left").to_string(index=False))
```
Real printed output (pandas 3.0.5):
```text
 EmpID  DeptID DeptName
     1      10    Sales
     2      20       HR
     3      30      NaN
```
**Version / licensing note:** Per the Merge queries overview page (in sources file, fetched in the research wave): six join kinds, matching types, expand or aggregate. UI wording from memory, unverified.
**Edge cases:** Duplicate keys in the right table multiply rows; a null result means no match (check Q33).
**Likely follow-ups:** (1) "Why did my row count grow?" Duplicate keys on the right. (2) "Aggregate vs expand?" Aggregate keeps one row per left row.
**Common mistakes:** Leaving the Table column unexpanded and loading it; expanding every column instead of the needed ones.

### Q27 ⭐⭐ 🟢 What does it mean to disable Enable Load on a query, and when would you do it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you keep helper queries out of the model.
**Say this in the interview:** "Enable Load decides whether a query's result is loaded into the data model. I turn it off for staging or helper queries, which still run inside Power Query and feed other queries, but do not show up as tables in the report."
**Explain simply:**
- A query with Enable Load off is shown in italics in the Queries pane.
- It still refreshes as needed when queries that reference it refresh.
- Benefits: smaller model, a cleaner field list, less memory.
**Example:** A raw `Raw_Attendance` query is cleaned by `Attendance_Clean`; only `Attendance_Clean` is loaded.
**DAX / Steps:** **Not run here.** In the Power Query Editor, right-click the query in the left Queries pane > untick Enable load (also under Include in report refresh). Close & Apply.
**Alternative:** Delete the query if no other query uses it; or keep it loaded for debugging, then hide the table in the model view.
**Version / licensing note:** From memory, unverified (Microsoft Learn not reachable here); the sources file marks the exact "Enable load" menu name as unconfirmed.
**Edge cases:** Disabling load on a query used in a relationship or measure breaks them; Enable load and Include in report refresh are separate options on the same right-click menu (their exact interaction: from memory, unverified).
**Likely follow-ups:** (1) "Staging pattern?" See Q59. (2) "Hide vs disable load?" Hiding keeps the table in the model; disabling removes it.
**Common mistakes:** Loading every helper query and bloating the model; disabling a query that visuals depend on.

### Q28 ⭐⭐ 🟢 What is the difference between Fixed Decimal Number, Decimal Number and Whole Number data types in Power Query?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you pick types that avoid rounding surprises.
**Say this in the interview:** "Whole Number holds integers with no decimals, good for counts and IDs. Decimal Number is a floating-point number, fast and flexible but can carry tiny binary rounding errors. Fixed Decimal Number (Currency) keeps exactly four decimal places, so I use it for salary and money."
**Explain simply:**
- Whole Number: 64-bit integer, like 12 employees; a decimal would be cut off or rounded.
- Decimal Number: stores very small fractions approximately, the way a calculator does (0.1 + 0.2 may display 0.30000000000000004).
- Fixed Decimal: always four digits after the decimal point, so sums of currency match exactly.
- Ranges and storage sizes: from memory, unverified.
**Example:** Monthly payroll of 1,000 rows; with Decimal Number a tiny float drift may make totals differ in the last digits; Fixed Decimal avoids that.
**DAX / Steps:** **Not run here.** Select column > Transform tab > Data Type > Fixed Decimal Number (or the icon in the header).
```m
Table.TransformColumnTypes(Payroll, {{"Salary", Currency.Type}, {"Days", Int64.Type}, {"Rating", type number}})
```
**Alternative:** Change the type in the model's Column tools after loading; but doing it in Power Query is better (Q46).
**Result:** Reproduced with plain Python as an illustration of float vs exact decimals (not Power Query): float 0.1 + 0.2 = 0.30000000000000004, exact decimal 0.3.
**Pandas check:**
```python
from decimal import Decimal
print(0.1+0.2, Decimal("0.1")+Decimal("0.2"))
print(round(1234.56789, 4))   # Fixed Decimal keeps 4 places
```
Real printed output (pandas 3.0.5):
```text
0.30000000000000004 0.3
1234.5679
```
**Version / licensing note:** From memory, unverified.
**Edge cases:** Fixed decimal keeps only four decimals (e.g., 1234.56789 becomes 1234.5679, reproduced above with Python's round; Power Query's own rounding rule: from memory, unverified); exchange-rate columns needing more precision should be Decimal Number.
**Likely follow-ups:** (1) "Which for IDs?" Text, not number, if leading zeros matter. (2) "Percentages?" Decimal, formatted as percent.
**Common mistakes:** Whole Number for averages; Decimal Number for money; numbers stored as text.

### Q29 ⭐⭐ 🟢 Your refresh fails because the source Excel file was moved. How do you fix the data source path?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know where source paths live and why parameters help.
**Say this in the interview:** "In Desktop I go to Home > Transform data > Data source settings, choose Change Source for that file and point it to the new path. Better still, my file path is a parameter, so I change it in one place. For a published report I fix it in the dataset's data source credentials and, if needed, the gateway."
**Explain simply:**
- Power Query stores the path inside the first step (Source) of the query.
- Data source settings lists every connection in the file, so one change updates all queries that use it.
- You can also open the Source step's gear icon, or edit the path in the Advanced Editor.
- A moved local file in a published report needs a gateway (a small program that lets the cloud service reach files on your own computer).
**Example:** `HR_Master.xlsx` moved from `C:\HR\2025` to `D:\HR\Master`; after Change Source, refresh works.
**DAX / Steps:** **Not run here.** Home tab > Queries group > Transform data (dropdown) > Data source settings > Change Source > browse the new file > OK > Close > Refresh.
**Alternative:** Create a parameter (Q42) `FilePath` and use it in Source; or store files in SharePoint/OneDrive so the URL does not change.
**Version / licensing note:** Desktop steps from memory, unverified. Gateway needs for local files are covered in Part 7; not re-verified here.
**Edge cases:** Sheet or table names inside the file must still exist; credentials may need re-entering.
**Likely follow-ups:** (1) "How to avoid this?" Parameter or SharePoint. (2) "Service refresh still fails?" Check gateway and credentials.
**Common mistakes:** Editing only one query when several use the same file; hard-coding a personal desktop path.

### Q30 ⭐⭐ 🟡 How would you unpivot an HR attendance sheet that has one column per day into a table with one row per employee per day?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** A classic wide-to-long reshape with the right unpivot option.
**Say this in the interview:** "I select the identifier columns, EmpID and Name, and use Unpivot Other Columns. All the day columns become rows with an Attribute (the day) and a Value (the status), which I rename. I choose Other Columns so new day columns added next month are included automatically."
**Explain simply:**
- Wide: one column per day (D1, D2...). Long: one row per employee per day. Long is what the model and slicers need.
- Selecting the ID columns and unpivoting the others makes the step future-proof.
- Afterwards, rename Attribute to Day and Value to Status, and convert Day to a proper date if the headers are dates.
**Example:** 2 employees, 3 days become 6 rows.
**Sample data:** Table `Attendance_Wide`

| EmpID | Name | D1 | D2 | D3 |
|---|---|---|---|---|
| 1 | Asha | P | A | P |
| 2 | Ravi | P | P | L |

**DAX / Steps:** M, **not run here**. Click-path: select EmpID and Name (Ctrl+click) > Transform tab > Any Column group > Unpivot Columns dropdown > Unpivot Other Columns.
```m
Table.UnpivotOtherColumns(Attendance_Wide, {"EmpID", "Name"}, "Day", "Status")
```
**Alternative:** Select the D1-D3 columns and use Unpivot Only Selected Columns (Q31); it works but a new day column is not included.
**Result:** Reproduced with pandas: 6 rows: Asha P/A/P, Ravi P/P/L.
**Pandas check:**
```python
import pandas as pd
att = pd.DataFrame({"EmpID":[1,2],"Name":["Asha","Ravi"],"D1":["P","P"],"D2":["A","P"],"D3":["P","L"]})
out = att.melt(id_vars=["EmpID","Name"], var_name="Day", value_name="Status")
print(out.sort_values(["EmpID","Day"]).to_string(index=False)); print("rows:", len(out))
```
Real printed output (pandas 3.0.5):
```text
 EmpID Name Day Status
     1 Asha  D1      P
     1 Asha  D2      A
     1 Asha  D3      P
     2 Ravi  D1      P
     2 Ravi  D2      P
     2 Ravi  D3      L
rows: 6
```
**Version / licensing note:** Unpivot options and their refresh behaviour with new columns: per Microsoft Learn "Unpivot columns" (summarised in research/Book04_Part02_sources.md, fetched in the research wave). Menu names from memory.
**Edge cases:** Null cells are removed in unpivot (absent days could vanish); header text like "01-Jan" must be converted to dates; merged header cells or top rows must be cleaned first (Q15).
**Likely follow-ups:** (1) "How to count absences?" `COUNTROWS(FILTER(Attendance_Long, Attendance_Long[Status] = "A"))` in DAX (not run here), where `Attendance_Long` is the unpivoted table. (2) "Why not leave it wide?" Hard to slice by date.
**Common mistakes:** Picking the day columns and unpivoting only those, which misses next month's columns; forgetting to rename Attribute/Value.

### Q31 ⭐⭐ 🟡 What is the difference between Unpivot Columns, Unpivot Other Columns and Unpivot Only Selected Columns?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand which option survives new columns.
**Say this in the interview:** "Unpivot Columns and Unpivot Only Selected Columns both unpivot just the columns I selected and keep that fixed list. Unpivot Other Columns unpivots everything except the selected ones, so columns added later are unpivoted automatically."
**Explain simply:**
- In Power Query, "Unpivot Columns" on the menu fixes the selected columns by name in the generated step (the Learn page describes it as unpivoting the selected columns); "Unpivot Only Selected Columns" does the same by name.
- "Unpivot Other Columns" fixes the columns you did not select as identifiers; every other current and future column is unpivoted.
- Choose Other Columns when the number of month/day columns will grow.
**Example:** Jan, Feb present now; Mar added next month.
**Sample data:** Table `Leaves_Wide`

| EmpID | Name | Jan | Feb |
|---|---|---|---|
| 1 | Asha | 20 | 19 |
| 2 | Ravi | 22 | 21 |

**DAX / Steps:** M, **not run here**.
```m
Table.UnpivotOtherColumns(Leaves_Wide, {"EmpID","Name"}, "Month", "Days")
Table.Unpivot(Leaves_Wide, {"Jan","Feb"}, "Month", "Days")
```
**Alternative:** Rename the columns and filter later; not recommended.
**Result:** Reproduced with pandas: today both give 4 rows. After a Mar column is added: Other Columns gives 6 rows (Mar included); Only Selected [Jan, Feb] gives 4 rows and Mar stays as a separate column.
**Pandas check:**
```python
import pandas as pd
a = pd.DataFrame({"EmpID":[1,2],"Name":["Asha","Ravi"],"Jan":[20,22],"Feb":[19,21]})
print("today, other columns:", a.melt(id_vars=["EmpID","Name"]).shape)
print("today, only selected:", a.melt(id_vars=["EmpID","Name"], value_vars=["Jan","Feb"]).shape)
a["Mar"] = [18, 20]                                                   # next month a column is added
print("after Mar, Other Columns  :", a.melt(id_vars=["EmpID","Name"]).shape)                          # (6, 4)
print("after Mar, Only Selected  :", a.melt(id_vars=["EmpID","Name","Mar"], value_vars=["Jan","Feb"]).shape)  # (4, 5)
```
Real printed output (pandas 3.0.5):
```text
today, other columns: (4, 4)
today, only selected: (4, 4)
after Mar, Other Columns  : (6, 4)
after Mar, Only Selected  : (4, 5)
```
**Version / licensing note:** Per Microsoft Learn "Unpivot columns" (via research/Book04_Part02_sources.md, fetched in the research wave): three options and refresh behaviour with new columns. I did not re-read the page.
**Edge cases:** If a selected column is renamed or removed at the source, Only Selected breaks (see Q48).
**Likely follow-ups:** (1) "Which is the default for a monthly file?" Other Columns. (2) "Does it keep nulls?" No, nulls are dropped.
**Common mistakes:** Assuming plain "Unpivot Columns" picks up new columns.

### Q32 ⭐⭐ 🟡 What is the difference between Reference and Duplicate for a query?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand dependency between queries.
**Say this in the interview:** "Duplicate copies all the steps into an independent new query. Reference makes a new query whose first step is the original query's output, so it depends on the original: change or refresh the original and the reference follows. I use Reference to build several tables from one cleaned source."
**Explain simply:**
- Duplicate: a full copy of the query's steps; later edits to the original do not affect the copy. The raw source is read again for each query.
- Reference: starts from the result of another query; edits upstream flow down. Think of a recipe that says "take the cleaned dough" instead of re-making it.
- Reference is the base of the staging pattern (Q59).
**Example:** `Employees_Clean` is referenced to make `Active_Employees` (filter) and `Exits` (filter), so cleaning is written once.
**DAX / Steps:** **Not run here.** In the Queries pane, right-click the query > Reference (or Duplicate). Check the result in View > Query Dependencies (Q50).
**Alternative:** Copy-paste the steps into a new query (manual duplicate), or use a custom function (Q55) for repeated logic.
**Version / licensing note:** From memory, unverified. The Towards Data Science blog snippet in the sources file mentions a circular-reference limit; I did not fetch it.
**Edge cases:** Do not make circular references. Whether the source is read once or several times depends on caching; for slow sources test refresh time (from memory, unverified).
**Likely follow-ups:** (1) "Which is better for performance?" Reference usually avoids repeated work, but not guaranteed. (2) "Can deleting the original break the reference?" Yes.
**Common mistakes:** Duplicating a query five times and then fixing a bug five times.

### Q33 ⭐⭐ 🟡 Your merge returns no matches or null values even though the keys look identical. What do you check?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Practical debugging of key mismatches.
**Say this in the interview:** "First data type: text 101 does not match number 101. Then hidden spaces, letter case, leading zeros, and finally the join kind and the right column pair. I Trim and Clean, make case consistent, set both keys to the same type, and re-check the merge preview."
**Explain simply:**
- Same data type is required on both sides (Merge queries overview, per the sources file).
- Matching in Power Query is case-sensitive and exact; "e003" and "E003" differ.
- Trailing spaces and non-printing characters make "E002 " different from "E002".
- Also check you picked the right key columns, the join kind (left outer shows nulls for non-matches), and that the other table is not filtered.
- Fuzzy matching (Q53) is only a last resort and works for text only.
**Example:** HR master vs attendance, EmpIDs typed by hand.
**Sample data:** Table `Master` and table `Attendance`

| EmpID (Master) | Name |
|---|---|
| E001 | A |
| E002 (trailing space) | B |
| e003 | C |
| E004 | D |

| EmpID (Attendance) | Days |
|---|---|
| E001 | 20 |
| E002 | 18 |
| E003 | 22 |
| E004 | 19 |

**DAX / Steps:** M, **not run here**. Fix before merging: select the key column > Transform tab > Format > Trim, then Format > Uppercase; set the same Data Type on both.
```m
Table.TransformColumns(Master, {{"EmpID", each Text.Upper(Text.Trim(_)), type text}})
```
**Alternative:** Merge on a cleaned helper column rather than altering the original key.
**Result:** Reproduced with pandas: before cleaning only E001 and E004 match (E002 and e003 get null); after Trim + Upper all four match (20, 18, 22, 19). A text "101" compared with number 101 is not equal (False).
**Pandas check:**
```python
import pandas as pd
m = pd.DataFrame({"EmpID":["E001","E002 ","e003","E004"],"Name":["A","B","C","D"]})
at = pd.DataFrame({"EmpID":["E001","E002","E003","E004"],"Days":[20,18,22,19]})
print("before cleaning:", m.merge(at, on="EmpID", how="left")["Days"].tolist())
m["EmpID"] = m.EmpID.str.strip().str.upper()
print("after Trim + Upper:", m.merge(at, on="EmpID", how="left")["Days"].tolist())
print('text "101" == number 101 ?', "101" == 101)
```
Real printed output (pandas 3.0.5):
```text
before cleaning: [20.0, nan, nan, 19.0]
after Trim + Upper: [20, 18, 22, 19]
text "101" == number 101 ? False
```
**Version / licensing note:** Merge type and matching rules per Microsoft Learn "Merge queries overview" (via sources file, fetched in the research wave); case-sensitivity detail from memory, unverified.
**Edge cases:** Leading zeros lost when numbers were typed as whole numbers ("007" vs 7); duplicate keys multiply rows.
**Likely follow-ups:** (1) "How to see mismatches?" Left anti join (Q37). (2) "Is the match case-sensitive?" Yes by default.
**Common mistakes:** Cleaning one side only; fixing the type after the merge step instead of before.

### Q34 ⭐⭐ 🟡 How do you append tables whose column names do not match exactly?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know append matches by column name, not position.
**Say this in the interview:** "Append matches columns by name. If names differ, I get extra columns with nulls. So I rename the columns in each query to a common name before appending, then append."
**Explain simply:**
- Append stacks rows of one table below another, like pasting more rows.
- Power Query lines up columns with identical names; a column that exists in only one table gets null for the other table's rows.
- Rename first (right-click header > Rename), or choose Transform > Use First Row as Headers where needed.
**Example:** Hyderabad file has `Dept`, Pune file has `Department` and an extra `City`.
**Sample data:** Tables `Hyd` and `Pune`

| EmpID | Dept |
|---|---|
| 1 | HR |
| 2 | IT |

| EmpID | Department | City |
|---|---|---|
| 3 | Sales | Pune |

**DAX / Steps:** M, **not run here**. Rename the Pune column in its query, then Home > Combine > Append Queries (as New).
```m
Table.Combine({Hyd, Table.RenameColumns(Pune, {{"Department","Dept"}})})
```
**Alternative:** `Table.Combine` with explicit column lists, or MissingField.UseNull in a rename to survive missing columns.
**Result:** Reproduced with pandas: without renaming, 3 rows and separate `Dept`/`Department` columns with nulls; after renaming, one `Dept` column: HR, IT, Sales, and `City` null for the first two.
**Pandas check:**
```python
import pandas as pd
q1 = pd.DataFrame({"EmpID":[1,2],"Dept":["HR","IT"]})
q2 = pd.DataFrame({"EmpID":[3],"Department":["Sales"],"City":["Pune"]})
print("no rename:"); print(pd.concat([q1, q2], ignore_index=True).to_string(index=False))
print("after rename:"); print(pd.concat([q1, q2.rename(columns={"Department":"Dept"})], ignore_index=True).to_string(index=False))
```
Real printed output (pandas 3.0.5):
```text
no rename:
 EmpID Dept Department City
     1   HR        NaN  NaN
     2   IT        NaN  NaN
     3  NaN      Sales Pune
after rename:
 EmpID  Dept City
     1    HR  NaN
     2    IT  NaN
     3 Sales Pune
```
**Version / licensing note:** From memory, unverified. Folder-combine structure requirement per the Folder connector page in the sources file (same structure needed).
**Edge cases:** Different data types in the same column turn it to Any or cause errors; column-name case differences also count as different names.
**Likely follow-ups:** (1) "Append vs merge?" Rows vs columns. (2) "Many files?" Use the folder connector (Q12).
**Common mistakes:** Appending before renaming and loading two near-identical columns.

### Q35 ⭐⭐ 🟡 How do you check whether a step in Power Query is folding to the source?
**Asked at:** crowd listing "what is query folding, how can we identify whether a query is folded" seen as a search snippet on a Glassdoor Power BI question list (undated; fetch not done); KORE1 and Simpliaxis snippets raise folding too.
**What the interviewer is checking:** That you can verify folding, not just define it.
**Say this in the interview:** "I right-click the applied step. If View Native Query is enabled, that step folds and I can read the SQL; if it is greyed out, folding stopped at or before that step. I can also open Query Diagnostics or the query plan. I keep folding steps first and non-folding steps last."
**Explain simply:**
- Query folding means Power Query translates your steps into one SQL statement that the database runs, instead of downloading everything and processing it locally.
- View Native Query greyed out means that step cannot be pushed to the source.
- Excel and CSV files do not fold (per Microsoft Learn "Query evaluation and query folding", from sources file, fetched in the research wave); folding is mainly for relational sources like SQL Server.
- Once a step breaks folding, all later steps usually run locally.
**Example:** SQL Server table with 5 million attendance rows: filter by year folds (the server sends only 1 year); adding an Index column afterwards does not.
**DAX / Steps:** **Not run here.** In Power Query Editor, Applied Steps pane > right-click a step > View Native Query. For more detail: View tab > Query plan (when available, from memory, unverified).
**Alternative:** Look at the status icons in the Applied Steps (newer builds show folding indicators, from memory, unverified) or run SQL Profiler / the database's trace to see queries.
**Version / licensing note:** View Native Query availability and folding rules: Microsoft Learn "Query evaluation and query folding" (per sources file). Query plan and indicator availability: from memory, unverified.
**Edge cases:** Native-query (hand-written SQL) sources may disable View Native Query yet still run on the server (Q58).
**Likely follow-ups:** (1) "Greyed out at step 5, what now?" Move foldable steps before it. (2) "Why care?" Speed.
**Common mistakes:** Assuming everything folds; checking only the last step.

### Q36 ⭐⭐ 🟡 Which Power Query transformations commonly break query folding?
**Asked at:** commonly asked (no company-specific report found); folding is a recurring theme in the Part 2 sources.
**What the interviewer is checking:** Whether you can name steps that cannot be translated to the source's language.
**Say this in the interview:** "Merging queries from two different sources, adding an index column, custom columns that call M functions with no SQL equivalent, pivot or unpivot on some sources, changing data type with locale, and Table.Buffer. Also data source privacy levels can stop folding. I put these at the end of the query."
**Explain simply:**
- Folding fails when a step has no equivalent in the source (SQL).
- Typical culprits: cross-source merges, custom columns using complex M, index columns, some text and date functions, Table.Buffer, hand-written native queries that you then keep transforming.
- This depends on the source and connector; test with View Native Query (Q35).
- Reordering steps, so foldable steps (filter, remove columns, sort, group) come first, often restores folding for them (steps can be reordered, per the folding basics page in the sources file).
**Example:** Filter FY2025 rows first (folds), then add a custom tenure column (does not fold): server filters, Power BI computes tenure on the 100k remaining rows instead of 5 million.
**DAX / Steps:** Concept, **not run here**. Test: right-click each step > View Native Query.
**Alternative:** Push the logic to the source: a SQL view with the custom column, then Power Query reads the view.
**Version / licensing note:** The list of exact breakers varies by connector and version: from memory, unverified; a Fabric Community thread in the sources file (not fetched) mentions custom columns and cross-source merges.
**Edge cases:** Files (Excel, CSV) never fold, so this question applies mostly to databases.
**Likely follow-ups:** (1) "Does a filter fold?" Usually yes. (2) "What if you must use a non-folding step?" Put it last, or filter first.
**Common mistakes:** Assuming "custom column" always breaks folding (not always; simple expressions can fold); not testing.

### Q37 ⭐⭐ 🟡 How do you find employees who are in the HR master but missing from the attendance data using Power Query?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Knowledge of Left Anti join.
**Say this in the interview:** "I merge the HR master with attendance on EmpID using Left Anti (rows only in first). The result has only master employees with no match in attendance."
**Explain simply:**
- Left Anti join keeps rows from the first (left) table that have no match in the second.
- The merged Table column in the result is empty for every row, so you can delete it.
- Reverse the tables or use Right Anti to find attendance IDs missing from the master (usually typos).
- Clean keys first (Q33), otherwise matching employees look missing.
**Example:** 5 on the HR master, attendance has 101, 102, 104 (twice) and 106.
**Sample data:** Tables `HR_Master` and `Attendance`

| EmpID |
|---|
| 101 |
| 102 |
| 103 |
| 104 |
| 105 |

| EmpID |
|---|
| 101 |
| 102 |
| 104 |
| 104 |
| 106 |

**DAX / Steps:** M, **not run here**. Home > Combine > Merge Queries > pick HR_Master on top, Attendance below, select EmpID in both > Join Kind: Left Anti (rows only in first) > OK > remove the Table column.
```m
Table.NestedJoin(HR_Master, {"EmpID"}, Attendance, {"EmpID"}, "Att", JoinKind.LeftAnti)
```
**Alternative:** Full Outer join and filter for nulls on the attendance side; or a DAX approach on loaded tables with `EXCEPT` (not used here).
**Result:** Reproduced with pandas: missing = 103 and 105. The full outer check also shows 106 only in attendance.
**Pandas check:**
```python
import pandas as pd
hr = pd.DataFrame({"EmpID":[101,102,103,104,105]})
at = pd.DataFrame({"EmpID":[101,102,104,104,106]})
print("left anti (in master, not in attendance):", hr[~hr.EmpID.isin(at.EmpID)].EmpID.tolist())
print("right anti (in attendance, not in master):", sorted(set(at.EmpID) - set(hr.EmpID)))
```
Real printed output (pandas 3.0.5):
```text
left anti (in master, not in attendance): [103, 105]
right anti (in attendance, not in master): [106]
```
**Version / licensing note:** Six join kinds including left anti per Microsoft Learn "Merge queries overview" (via sources file, fetched in the research wave).
**Edge cases:** Duplicate attendance rows (104 twice) do not matter for anti join; a blank (null) EmpID matches only another blank, so clean blanks first.
**Likely follow-ups:** (1) "Right Anti?" Attendance IDs not in master. (2) "Why not relationship?" Relationships do not list non-matches directly.
**Common mistakes:** Using Inner join; putting tables in the wrong order.

### Q38 ⭐⭐ 🟡 When would you use Merge Queries in Power Query instead of a relationship in the data model?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know when to physically combine tables and when to keep them separate.
**Say this in the interview:** "I use a relationship for normal star-schema reporting: it is lighter and filters flow dynamically from the lookup table (for example Department) to the data table. I merge when I need the columns physically in one table, to flatten a small lookup, to find non-matches with anti joins, to filter one table by another, or when there is no usable key for a relationship."
**Explain simply:**
- Relationship: tables stay separate; the model joins them at report time and filter context flows from the dimension to the fact table.
- Merge: a one-time join at refresh that creates a wider table (more columns, maybe more memory).
- Merge is also needed when you want to enrich rows (get department name on each row) and then load one table.
- Do not merge big facts into dimensions for no reason; it duplicates data and loses model flexibility.
**Example:** Merge for "employees missing from attendance" (Q37); relationship for Department-to-Employee reporting.
**DAX / Steps:** Concept, **not run here**. Merge: Home > Merge Queries. Relationship: Model view > drag key from one table to the other.
**Alternative:** A DAX calculated column with `RELATED` when a relationship exists.
**Version / licensing note:** From memory, unverified; relationships belong to Part 3.
**Edge cases:** Merging on a many-to-many key duplicates rows; a merge on a folding source may fold, a cross-source merge may not (Q36).
**Likely follow-ups:** (1) "Which is faster?" Relationships are usually leaner. (2) "Can I do both?" Yes.
**Common mistakes:** Merging everything into one giant flat table; merging then also creating a relationship on the same key.

### Q39 ⭐⭐ 🟡 How do you handle errors such as DataFormat.Error when converting a column to number or date?
**Asked at:** commonly asked (no company-specific report found); "error handling" appears in prep lists seen in the sources.
**What the interviewer is checking:** That you find and fix bad values rather than ignore them.
**Say this in the interview:** "I find the error rows with Keep Errors, look at what the values are, and fix the cause: clean the text, then convert again. For leftover values I use Replace Errors or a try ... otherwise, deliberately and with a count, so I never silently drop real data."
**Explain simply:**
- DataFormat.Error means a cell cannot be turned into the type, for example "N/A" into a number or "50,000" under a locale that does not accept commas.
- Steps: Home > Keep Rows > Keep Errors to see offenders; fix (Replace Values, remove commas/symbols, change locale); then convert.
- Replace Errors turns error cells into a value (null or 0); try ... otherwise does this inside a formula (Q43).
- Decide whether null or 0 is right: a null salary is not the same as 0.
**Example:** Salary column typed as text containing "N/A" and "50,000".
**Sample data:** Table `Payroll_Raw`

| EmpID | Salary (text) |
|---|---|
| 1 | 45000 |
| 2 | N/A |
| 3 | 52000 |
| 4 | 50,000 |

**DAX / Steps:** M, **not run here**.
```m
= Table.TransformColumns(Payroll_Raw, {{"Salary", each try Number.FromText(Text.Replace(_, ",", "")) otherwise null, type number}})
```
Click-path to inspect: select column > Home > Keep Rows > Keep Errors.
**Alternative:** Convert, then Transform > Replace Errors (null); simpler but hides the reason.
**Result:** Reproduced with pandas: naive conversion makes N/A and 50,000 errors (2 errors, sum of valid = 97,000); after removing commas only N/A is left null, giving 45000, null, 52000, 50000 (sum 147,000).
**Pandas check:**
```python
import pandas as pd
raw = pd.DataFrame({"EmpID":[1,2,3,4],"Salary":["45000","N/A","52000","50,000"]})
naive = pd.to_numeric(raw.Salary, errors="coerce")
print("naive:", naive.tolist(), "errors:", int(naive.isna().sum()), "sum of valid:", naive.sum())
fixed = pd.to_numeric(raw.Salary.str.replace(",",""), errors="coerce")
print("after removing commas:", fixed.tolist(), "sum:", fixed.sum())
```
Real printed output (pandas 3.0.5):
```text
naive: [45000.0, nan, 52000.0, nan] errors: 2 sum of valid: 97000.0
after removing commas: [45000.0, nan, 52000.0, 50000.0] sum: 147000.0
```
**Version / licensing note:** try/otherwise per Microsoft Learn "Error handling" (via sources file, fetched in the research wave).
**Edge cases:** Errors in rows that are filtered out do not fail the refresh; errors in rows loaded to the model stay as error cells (how the Service and visuals then behave: from memory, unverified), so fix or count them before loading.
**Likely follow-ups:** (1) "Replace with 0?" Only if 0 is meaningful. (2) "Locale issue?" See Q41.
**Common mistakes:** Replacing errors with 0 and hiding bad data; ignoring the Keep Errors check.

### Q40 ⭐⭐ 🟡 How do you create a tenure band column (0-1, 1-3, 3+ years) from a joining date in Power Query?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Date arithmetic plus conditional logic in a custom column.
**Say this in the interview:** "I first calculate tenure in years, today minus joining date, then use a Conditional Column or a custom column with if...then...else to assign the band. Because 'today' changes, I note the band moves on every refresh. I state the boundary rule: under 1 is 0-1, 1 to under 3 is 1-3, 3 and above is 3+."
**Explain simply:**
- Subtract two dates to get a duration; take the days and divide by 365.25 to get approximate years.
- The band order matters: test the smallest first.
- State boundaries explicitly so 1.00 year falls in one band only.
- For reporting as of a fixed date (month-end), use that date instead of today so history is reproducible.
**Example:** As of 2025-11-01.
**Sample data:** Table `Employees`

| EmpID | JoinDate |
|---|---|
| 1 | 2025-09-15 |
| 2 | 2024-10-01 |
| 3 | 2022-06-30 |
| 4 | 2025-11-01 |
| 5 | 2020-01-10 |

**DAX / Steps:** M, **not run here**. Add Column > Custom Column:
```m
let AsOf = #date(2025,11,1) in
Table.AddColumn(Employees, "TenureYears", each Duration.Days(AsOf - [JoinDate]) / 365.25, type number)
```
then Add Column > Conditional Column: Band = "0-1" if TenureYears < 1, "1-3" if < 3, else "3+". (For live data replace AsOf with `Date.From(DateTime.LocalNow())`.)
**Alternative:** A DAX calculated column with `DATEDIFF([JoinDate], TODAY(), YEAR)` (it counts year boundaries crossed, so results can differ slightly from days/365.25), or a DAX measure for average tenure.
**Result:** Reproduced with pandas (not run in Power Query): years 0.13, 1.08, 3.34, 0.00, 5.81, bands 0-1, 1-3, 3+, 0-1, 3+.
**Pandas check:**
```python
import pandas as pd, numpy as np
j = pd.DataFrame({"EmpID":[1,2,3,4,5],
                  "JoinDate":pd.to_datetime(["2025-09-15","2024-10-01","2022-06-30","2025-11-01","2020-01-10"])})
asof = pd.Timestamp("2025-11-01")
j["Years"] = ((asof - j.JoinDate).dt.days/365.25).round(2)
j["Band"] = np.select([j.Years<1, j.Years<3], ["0-1","1-3"], "3+")
print(j.to_string(index=False))
```
Real printed output (pandas 3.0.5):
```text
 EmpID   JoinDate  Years Band
     1 2025-09-15   0.13  0-1
     2 2024-10-01   1.08  1-3
     3 2022-06-30   3.34   3+
     4 2025-11-01   0.00  0-1
     5 2020-01-10   5.81   3+
```
**Version / licensing note:** From memory, unverified (Microsoft Learn not reachable here).
**Edge cases:** Null JoinDate gives a null band; future joining dates give negative tenure; leap years make days/365.25 approximate; exit dates for leavers should replace the as-of date.
**Likely follow-ups:** (1) "Power Query or DAX?" Power Query for a fixed band, DAX if as-of date should respond to filters. (2) "Why 365.25?" Averages leap years.
**Common mistakes:** Overlapping boundaries (`<=1` and `>=1`); ordering conditions largest first; using TODAY() in history reports.

### Q41 ⭐⭐ 🟡 How do you convert text dates such as 31/12/2025 correctly when your system uses US date settings?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Awareness of locale and day-month ambiguity.
**Say this in the interview:** "I use Change Type > Using Locale and choose Date with a locale such as English (India) or English (United Kingdom), which reads day/month/year. That avoids the wrong swap of day and month or errors on 31/12."
**Explain simply:**
- Locale = the regional setting that tells Power Query how to read dates and numbers.
- With US settings, 05/01/2025 is read as 1 May, not 5 January; 31/12/2025 errors because there is no month 31.
- Using Locale says: "this text was written in this culture, read it that way".
- Best to fix it once at load time, not in DAX.
**Example:** HR exports with day/month/year; the machine is set to US.
**Sample data:** Text column `JoinText`

| JoinText |
|---|
| 31/12/2025 |
| 05/01/2025 |
| 1/2/2025 |

**DAX / Steps:** **Not run here.** Select column > Transform tab > Data Type dropdown > Using Locale... > Data Type: Date, Locale: English (United Kingdom) (or English (India)) > OK.
```m
Table.TransformColumnTypes(Source, {{"JoinText", type date}}, "en-GB")
```
**Alternative:** Split by "/" and rebuild with `#date(year, month, day)`, or change the project's Regional Settings (File > Options > Regional Settings), but that affects the whole file (File > Options and settings > Options > Current File > Regional Settings; path from memory, unverified).
**Result:** Reproduced with pandas: parsing day-first gives 2025-12-31, 2025-01-05, 2025-02-01; parsing month-first gives NaT (error), 2025-05-01, 2025-01-02, which shows the silent swap.
**Pandas check:**
```python
import pandas as pd
t = pd.Series(["31/12/2025","05/01/2025","1/2/2025"])
print("day-first  :", pd.to_datetime(t, format="%d/%m/%Y").dt.strftime("%Y-%m-%d").tolist())
print("month-first:", pd.to_datetime(t, format="%m/%d/%Y", errors="coerce").dt.strftime("%Y-%m-%d").tolist())
```
Real printed output (pandas 3.0.5):
```text
day-first  : ['2025-12-31', '2025-01-05', '2025-02-01']
month-first: [nan, '2025-05-01', '2025-01-02']
```
**Version / licensing note:** The menu name "Using Locale" is listed as unconfirmed in the sources file; from memory, unverified.
**Edge cases:** Mixed formats in one column; two-digit years; ambiguous dates that parse without an error but give the wrong date (05/01).
**Likely follow-ups:** (1) "Which dates fail loudly?" Those with day over 12. (2) "Could DAX fix it?" Only awkwardly; do it in Power Query.
**Common mistakes:** Letting auto-detect type guess; trusting dates that did not error.

### Q42 ⭐⭐ 🟡 What are parameters in Power Query, and how would you use one for a file path or server name?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know how to avoid hard-coding values, so the same report can point at dev, test or production data by changing one value?
**Say this in the interview:** "A parameter is a named value I store once in Power Query and reuse in many steps. I create one for the folder path or server name, use it inside the Source step, and when the file moves or we switch from test to production I change that single value instead of editing every query."
**Explain simply:**
- A parameter has a name, a data type, and a current value. Microsoft recommends always setting the type.
- You make one in Power Query Editor: Home > Manage Parameters > New Parameter, or right-click a query that holds a simple constant (text, number, date) and choose Convert to Parameter.
- You can use it as an argument in a step (for example a filter) or inside a data-source function, such as the Server box of the SQL Server dialog.
- "Suggested values" can be Any value, a List of values (a dropdown) or a Query.
**Example:** The HR export sits in `C:\HR\Dev\` on your laptop but in `D:\HR\Prod\` on the office server. One parameter, `FolderPath`, holds the folder. Switching it changes which `employees.csv` is read.
**Sample data:** Parameter table.

| Parameter | Type | Current value |
|---|---|---|
| FolderPath | Text | src_dev |

**DAX / Steps (not run here):**
1. Home > Manage Parameters > New Parameter. Name `FolderPath`, Type Text, Current Value your folder. Repeat for `ServerName` if needed.
2. Open the query, Advanced Editor, and replace the hard-coded text:
```m
let
    Source = Csv.Document(File.Contents(FolderPath & "employees.csv"), [Delimiter=",", Encoding=1252, QuoteStyle=QuoteStyle.None]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true])
in
    Promoted
```
For a database, type the parameter name in the Server box of the SQL Server dialog (Microsoft's best-practices page shows this).
**Alternative:** Use a List-of-values parameter (Dev / Test / Prod) so a colleague picks from a dropdown instead of typing a path.
**Result:** Reproduced with pandas (M not run): pointing the "parameter" at the dev folder reads 2 rows, at the prod folder reads 5 rows. Same logic, different source.
**Pandas check:**
```python
import pandas as pd, os, tempfile
base = tempfile.mkdtemp()
for folder, n in [("src_dev", 2), ("src_prod", 5)]:      # make two small test folders
    os.makedirs(os.path.join(base, folder))
    pd.DataFrame({"EmpID": range(1, n+1)}).to_csv(os.path.join(base, folder, "employees.csv"), index=False)
def load(folder): return pd.read_csv(os.path.join(base, folder, "employees.csv"))
for p in ["src_dev", "src_prod"]:                         # p plays the role of the parameter FolderPath
    print(p, len(load(p)), "rows")
```
Real printed output (pandas 3.0.5):
```text
src_dev 2 rows
src_prod 5 rows
```
**Version / licensing note:** Parameters work in Power Query in Excel and Power BI Desktop; multi-value (list) parameters are only in Power Query Online (Microsoft Learn: Parameters - Power Query, updated 2026-04). The claim that a parameter used in a data source call does not trigger Formula.Firewall errors is from memory, unverified.
**Edge cases:** A parameter holding a path breaks if the new machine uses a different drive letter. After publishing, scheduled refresh still needs the service to reach that path (gateway; Part 7).
**Likely follow-ups:** 1) *Parameter vs query?* A parameter is one constant value you can edit in a dialog; a query returns a table. 2) *Can a parameter feed a custom function?* Yes (Q55).
**Common mistakes:** Leaving the type as Any; typing the path with a missing trailing backslash so `FolderPath & "file.csv"` joins wrongly.

### Q43 ⭐⭐ 🟡 How do you use try ... otherwise in Power Query?
**Asked at:** commonly asked (no company-specific report found); Zero To Mastery and similar lists mention error handling in M (snippet only).
**What the interviewer is checking:** Can you stop one bad cell from breaking the whole refresh and decide what the fallback should be?
**Say this in the interview:** "`try <expression> otherwise <fallback>` is Power Query's version of IFERROR. If the expression returns an error, I get the fallback value instead. I use it in a custom column when some values, like 'N/A' in a number column, would otherwise turn into errors."
**Explain simply:**
- Power Query errors can be at step level (the whole query fails) or cell level (just that cell shows Error).
- `try` evaluates something and catches any error. `otherwise` supplies the replacement.
- Plain `try [Col]` returns a record with HasError, Value and Error fields, handy when you want to log the reason.
- Newer syntax `try x catch (e) => ...` is equivalent but also lets you read the error message (introduced May 2022 per Microsoft).
**Example:** Bonus is typed as text. "N/A" and "abc" cannot become numbers, so you default them to 0 but leave truly empty (null) cells blank.
**Sample data:** Table `Bonus_Raw`.

| Emp | BonusText |
|---|---|
| Asha | 5000 |
| Ravi | N/A |
| Meena | 7500 |
| Karan | (null) |
| Divya | abc |

**DAX / Steps (not run here):** Add Column > Custom Column:
```m
Table.AddColumn(Bonus_Raw, "Bonus", each try Number.From([BonusText]) otherwise 0, type number)
```
**Alternative:** `try Number.From([BonusText]) catch (e) => 0`, or set the column to Number and use Home > Remove Rows > Remove Errors / Transform > Replace Errors.
**Result:** Reproduced with pandas (M not run): 5000, 0, 7500, null, 0.
**Pandas check:**
```python
import pandas as pd
df = pd.DataFrame({"Emp":["Asha","Ravi","Meena","Karan","Divya"],"BonusText":["5000","N/A","7500",None,"abc"]})
def try_otherwise(x):
    if x is None: return None          # assumption: Number.From(null) = null
    try: return float(x)
    except ValueError: return 0.0
df["Bonus"] = df.BonusText.map(try_otherwise)
print(df.to_string(index=False))
```
Real printed output (pandas 3.0.5):
```text
  Emp BonusText  Bonus
 Asha      5000 5000.0
 Ravi       N/A    0.0
Meena      7500 7500.0
Karan       NaN    NaN
Divya       abc    0.0
```
**Version / licensing note:** Syntax from Microsoft Learn: Error handling - Power Query (2025-07). Works in all Power Query hosts.
**Edge cases:** `otherwise` only fires on errors, not on nulls or on wrong-but-valid values. Silent defaulting to 0 can hide bad data, so count how many rows fell back.
**Likely follow-ups:** 1) *try vs Remove Errors?* Remove Errors deletes rows; try keeps them with a fallback. 2) *Where is the error text?* Use catch and read the Message field.
**Common mistakes:** Defaulting everything to 0 without checking; expecting `otherwise` to replace blanks.

### Q44 ⭐⭐ 🟡 Your Power Query refresh is slow. What do you check and change?
**Asked at:** commonly asked; a KORE1 article asks where each Power Query step executes and Glassdoor listings include query folding (snippets only, no company-specific report).
**What the interviewer is checking:** Do you have a calm checklist instead of guessing?
**Say this in the interview:** "First I find out whether the slowness is the source, the data volume or my steps. Then I filter early and drop unneeded columns so less data moves, check whether the steps fold back to the database, put expensive steps like sorts last, remove steps I do not need, and if the table keeps growing I look at incremental refresh."
**Explain simply:**
- Query folding means Power Query translates your steps into the source's own language (for example SQL) so the database does the work. CSV and Excel files do not fold. Check by right-clicking a step and looking for View Native Query (availability depends on connector).
- Filter rows and choose only needed columns as early as possible.
- Do expensive operations (sort, merge, group) last; Microsoft says a sort must read all rows before returning any.
- Use the right connector (SQL Server connector, not generic ODBC) and correct data types.
- During development, Keep First Rows to speed up preview, then remove it.
- Use Column quality / distribution / profile to spot junk.
**Example:** A 5-million-row attendance table loads every column from SQL and filters to this year only at the end. Moving the date filter to step 2 (which folds) lets the database return only the rows needed.
**Sample data:** Table `Employees_Raw` (8 rows): 5 are Active.
**DAX / Steps (not run here):** View tab > Column quality, Column distribution, Column profile (from memory, unverified path). Right-click a step > View Native Query. Home > Keep Rows / Remove Columns early.
**Alternative:** Move heavy cleaning upstream (a SQL view or a dataflow, Q60), or set up incremental refresh (Q56).
**Result:** Reproduced with pandas: a sort placed before the filter works on 8 rows, after the filter on 5. At scale this is the saving, but real timings were not measured here.
**Pandas check:**
```python
import pandas as pd
n = pd.DataFrame({"Emp":range(1,9),"Status":["Active","Left","Active","Active","Left","Active","Left","Active"]})
print("rows:", len(n), "active:", (n.Status=="Active").sum())
print("sort before filter sorts", len(n), "rows; sort after filter sorts", len(n[n.Status=="Active"]), "rows")
```
Real printed output (pandas 3.0.5):
```text
rows: 8 active: 5
sort before filter sorts 8 rows; sort after filter sorts 5 rows
```
**Version / licensing note:** Folding, "filter early", "expensive operations last" and the folding indicators (Power Query Online only) are from Microsoft Learn: Understanding Query Evaluation and Query Folding; Best Practices When Working with Power Query. Refresh time limits (2 h Pro, 5 h Premium) are from Microsoft Learn: Configure incremental refresh (2026-07).
**Edge cases:** Merging a folded SQL table with a CSV can force Power Query to pull the whole SQL table locally. Privacy levels can force buffering (Q57).
**Likely follow-ups:** 1) *How do you know a step folds?* View Native Query is available. 2) *When is a full refresh unavoidable?* Small tables or non-date-filterable sources.
**Common mistakes:** Adding many "Changed Type" and sort steps early; loading unused columns; testing only on the small preview.

### Q45 ⭐⭐ 🟡 Why does the order of steps matter for performance, and what should you filter first?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand that steps run in sequence, so order changes both speed and sometimes the answer?
**Say this in the interview:** "Each step works on the output of the previous one, so I shrink the data first: remove rows I will never use, especially by date or status, and drop unused columns, before sorts, merges and groupings. Order can also change the result, for example keeping the top rows before versus after a filter."
**Explain simply:**
- Filters "stream": Power Query can return results while reading. Sorts need every row first.
- Filter first on the most selective condition (date range, status, region), then remove columns.
- For folding sources, early filters are pushed to the database. Power Query may reorder steps when folding, but do not rely on that.
- Order can change correctness: "keep top 2" is not the same as "filter then keep top 2".
**Example:** Latest 2 employee IDs that are Active.
**Sample data:** Table `Employees_Raw` (Emp 1-8; Active: 1,3,4,6,8).
**DAX / Steps (not run here):** Right-click an applied step > Move before / Move after (steps list; Diagram view page documents these for Online). Put Filter Rows near the top, Sort and Merge near the bottom.
**Alternative:** Extract the early steps into a reference query (Extract Previous) so the cheap filters are separate and easy to inspect.
**Result:** Reproduced with pandas: keep top 2 by Emp (desc) then filter Active returns only Emp 8. Filter Active then keep top 2 returns Emp 8 and 6.
**Pandas check:**
```python
import pandas as pd
n = pd.DataFrame({"Emp":range(1,9),"Status":["Active","Left","Active","Active","Left","Active","Left","Active"]})
s = n.sort_values("Emp", ascending=False)
a = s.head(2); a = a[a.Status=="Active"]          # keep top 2, THEN filter
b = s[s.Status=="Active"].head(2)                 # filter, THEN keep top 2
print("keep top 2 then filter:", a.Emp.tolist())
print("filter then keep top 2:", b.Emp.tolist())
```
Real printed output (pandas 3.0.5):
```text
keep top 2 then filter: [8]
filter then keep top 2: [8, 6]
```
**Version / licensing note:** Streaming vs sort behaviour from Microsoft Learn: Best Practices When Working with Power Query. Step reordering by the engine from Microsoft Learn: Understanding Query Evaluation and Query Folding.
**Edge cases:** Moving a step can break later steps that depend on a column created earlier (error). Filtering on a computed column early can stop folding.
**Likely follow-ups:** 1) *What if I filter after the merge?* The merge processes more rows; filter both sides first. 2) *Does folding reorder?* The engine may, but the result stays equivalent.
**Common mistakes:** Sorting the whole table first; assuming order never changes results.

### Q46 ⭐⭐ 🟡 Why should you do date, text and number cleaning in Power Query rather than in DAX?
**Asked at:** commonly asked (no company-specific report found); "Power Query vs DAX column" is a repeated theme in the Part 2 sources.
**What the interviewer is checking:** Do you know which tool does what: Power Query shapes data before it loads; DAX calculates on loaded data.
**Say this in the interview:** "Cleaning belongs in Power Query because it happens once, before the data reaches the model. Types and text are fixed at the source of the pipeline, folding can push work to the database, and every report on that model gets the same clean values. DAX is for business calculations like measures that react to filters."
**Explain simply:**
- Power Query is the ETL (extract, transform, load) layer: connect, clean, reshape, then load.
- DAX (the formula language of the model) is best for measures that change with slicers.
- Cleaning in DAX means the dirty column still sits in the model and every formula must remember to clean it.
- Data type problems (text dates, text numbers) are best fixed before load.
**Example:** Department typed three ways ("Sales", " sales", "SALES") makes 3 rows in a headcount table instead of 1.
**Sample data:** Table `Employees_Raw` (Dept column).

| Emp | Dept |
|---|---|
| 1 | Sales |
| 2 | " sales" |
| 3 | SALES |
| 4 | Human Resources |
| 5 | "human resources " |
| 6 | HUMAN RESOURCES |
| 7 | Finance |

**DAX / Steps (not run here):**
```m
let
    Trimmed = Table.TransformColumns(Employees_Raw, {{"Dept", each Text.Proper(Text.Trim(_)), type text}})
in
    Trimmed
```
(Select column > Transform > Format > Trim, then Capitalize Each Word.)
**Alternative:** A DAX calculated column, which works but leaves the dirty column in the model:
```dax
Dept Clean = TRIM(Employees_Raw[Dept])
```
(not run here; TRIM only removes extra spaces, not case differences, per Microsoft Learn: TRIM function (DAX)).
**Result:** Reproduced with pandas: 7 raw rows give 7 distinct Dept values, after Trim + Title case only 3 (Sales 3, Human Resources 3, Finance 1).
**Pandas check:**
```python
import pandas as pd
r = pd.DataFrame({"Emp":range(1,8),"Dept":["Sales"," sales","SALES","Human Resources","human resources ","HUMAN RESOURCES","Finance"]})
r["DeptClean"] = r.Dept.str.strip().str.title()
print(r.Dept.nunique(), r.DeptClean.nunique())
print(r.DeptClean.value_counts().to_dict())
```
Real printed output (pandas 3.0.5):
```text
7 3
{'Sales': 3, 'Human Resources': 3, 'Finance': 1}
```
**Version / licensing note:** The Power Query = prepare, DAX = calculate split is from memory, unverified on a fetched page. Folding of early steps is from Microsoft Learn: Understanding Query Evaluation and Query Folding. `Text.Proper` and `Text.Trim` pages were not fetched.
**Edge cases:** DAX cannot change a column's type before load; a text date in the model must be converted with a formula. Non-breaking spaces (character 160) survive TRIM in DAX (Microsoft Learn: TRIM).
**Likely follow-ups:** 1) *Is there ever a reason to use DAX?* Yes: anything that depends on filters, like attrition rate. 2) *Calculated column vs measure?* Row-by-row stored vs calculated on the fly.
**Common mistakes:** Building many DAX columns to fix dirty text; leaving columns typed Any.

### Q47 ⭐⭐ 🔴 How do you keep only the latest record per employee in Power Query?
**Asked at:** commonly asked (no company-specific report found); a gap-fill HR scenario in the Part 2 sources.
**What the interviewer is checking:** Can you pick one row per group, deal with ties, and avoid the unreliable "sort then remove duplicates" trap?
**Say this in the interview:** "I group by employee ID and for each group take the row with the maximum effective date, then expand that row. I check for ties, because two records on the same date make 'latest' ambiguous, so I add a tie-breaker like RecordID."
**Explain simply:**
- Group By EmpID; the aggregation returns a whole row, not just a number.
- `Table.Max(_, {"EffectiveDate", "RecordID"})` returns the largest row in each group: latest date first, and RecordID breaks a tie (passing a list of columns as the comparison rule: from memory, unverified).
- Alternative: sort descending, then Remove Duplicates on EmpID. Microsoft warns there is no guarantee which duplicate stays; buffering the sorted table first is a widely used workaround (a forum recommendation in the sources file, not a Microsoft guarantee).
- Always test for ties.
**Example:** Salary history: employee 103 has two records on the same date.
**Sample data:** Table `Salary_History`.

| RecordID | EmpID | EffectiveDate | Dept | Salary |
|---|---|---|---|---|
| 1 | 101 | 2024-04-01 | Sales | 40000 |
| 2 | 101 | 2025-04-01 | Sales | 44000 |
| 3 | 101 | 2025-10-01 | Marketing | 52000 |
| 4 | 102 | 2023-04-01 | HR | 35000 |
| 5 | 102 | 2025-04-01 | HR | 38000 |
| 6 | 103 | 2025-06-01 | Finance | 60000 |
| 7 | 103 | 2025-06-01 | Finance | 61000 |

**DAX / Steps (not run here):** Home > Group By (Advanced), or in M:
```m
let
    Grouped = Table.Group(Salary_History, {"EmpID"}, {{"Latest", each Table.Max(_, {"EffectiveDate", "RecordID"}), type record}}),
    Expanded = Table.ExpandRecordColumn(Grouped, "Latest", {"RecordID","EffectiveDate","Dept","Salary"})
in
    Expanded
```
**Alternative:**
```m
let
    Sorted = Table.Buffer(Table.Sort(Salary_History, {{"EmpID", Order.Ascending}, {"EffectiveDate", Order.Descending}, {"RecordID", Order.Descending}})),
    Latest = Table.Distinct(Sorted, {"EmpID"})
in
    Latest
```
**Result:** Reproduced with pandas (M not run): EmpID 101 gets RecordID 3 (52000), 102 gets 5 (38000), 103 has 2 rows at the max date, so the tie-break on RecordID chooses 7 (61000). Both M versions are written to give this result; neither was run. Without the RecordID in the rule, which row `Table.Max` returns on a tie is not stated, so check ties explicitly.
**Pandas check:**
```python
import pandas as pd
h = pd.DataFrame({"RecordID":range(1,8),"EmpID":[101,101,101,102,102,103,103],
  "EffectiveDate":pd.to_datetime(["2024-04-01","2025-04-01","2025-10-01","2023-04-01","2025-04-01","2025-06-01","2025-06-01"]),
  "Dept":["Sales","Sales","Marketing","HR","HR","Finance","Finance"],"Salary":[40000,44000,52000,35000,38000,60000,61000]})
lat = h.sort_values(["EmpID","EffectiveDate","RecordID"], ascending=[True,False,False]).drop_duplicates("EmpID")
print(lat[["EmpID","RecordID","Dept","Salary"]].to_string(index=False))
mx = h.groupby("EmpID").EffectiveDate.transform("max")
print("rows at the max date per employee:", h[h.EffectiveDate==mx].groupby("EmpID").size().to_dict())
```
Real printed output (pandas 3.0.5):
```text
 EmpID  RecordID      Dept  Salary
   101         3 Marketing   52000
   102         5        HR   38000
   103         7   Finance   61000
rows at the max date per employee: {101: 1, 102: 1, 103: 2}
```
**Version / licensing note:** Table.Max, Table.Group, Table.Sort, Table.Distinct, Table.ExpandRecordColumn semantics from their Microsoft Learn PowerQuery M pages (fetched). Grouping with Table.Max may not fold on database sources (not verified).
**Edge cases:** Ties on date; null dates (how nulls sort); employees with a single record; text dates sorting alphabetically (convert to date first).
**Likely follow-ups:** 1) *Why not just Remove Duplicates after sorting?* Order is not guaranteed unless buffered (Q61). 2) *Earliest record instead?* Table.Min or sort ascending.
**Common mistakes:** Sorting by a text date; ignoring ties; using Group By with Max date only and losing the other columns.

### Q48 ⭐⭐ 🔴 A refresh breaks with 'The column of the table wasn't found' after the source file changed. Why does this happen and how do you make the query more resilient?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand that steps refer to columns by name, and can you design for changing sources?
**Say this in the interview:** "Power Query steps hard-code column names. If the source renames or drops a column, such as Dept becoming Department, the step that names it fails. I make it resilient by selecting only the columns I need with a missing-field option, renaming known variants first, and avoiding steps that depend on column position or that name every column."
**Explain simply:**
- Steps like Changed Type, Remove Columns and Rename store column names as text in M.
- Error wording is close to `Expression.Error: The column 'Dept' of the table wasn't found.` (exact text from memory).
- Defence: Choose Columns / `Table.SelectColumns(..., MissingField.UseNull)`, `Table.RenameColumns(..., MissingField.Ignore)`, `Table.TransformColumnTypes` with a culture record containing `MissingField` (from memory, unverified).
- Unpivot Other Columns / selected columns copes with new columns better than hard-coded unpivot lists.
**Example:** HR sends monthly headcount files. In October the "Dept" column becomes "Department".
**Sample data:** Table `Headcount_Oct` (renamed column).

| EmpID | Name | Department | Salary |
|---|---|---|---|
| 101 | Asha | HR | 40000 |
| 102 | Ravi | Finance | 35000 |

**DAX / Steps (not run here):**
```m
let
    Renamed = Table.RenameColumns(Source, {{"Department","Dept"}}, MissingField.Ignore),
    Selected = Table.SelectColumns(Renamed, {"EmpID","Name","Dept","Salary"}, MissingField.UseNull)
in
    Selected
```
**Alternative:** Ask the data owner to freeze headers, or load through a staging query that standardises names once (Q59).
**Result:** Reproduced with pandas: selecting `["EmpID","Name","Dept","Salary"]` on the new file raises KeyError for Dept. Renaming first gives Dept = HR, Finance. Without the rename, `UseNull` style gives Dept = NaN for both rows.
**Pandas check:**
```python
import pandas as pd
new = pd.DataFrame({"EmpID":[101,102],"Name":["Asha","Ravi"],"Department":["HR","Finance"],"Salary":[40000,35000]})
want = ["EmpID","Name","Dept","Salary"]
try: new[want]
except KeyError as e: print("KeyError:", e)
print(new.reindex(columns=want).to_string(index=False))                       # like MissingField.UseNull
print(new.rename(columns={"Department":"Dept"})[want].to_string(index=False))  # rename first
```
Real printed output (pandas 3.0.5):
```text
KeyError: "['Dept'] not in index"
 EmpID Name  Dept  Salary
   101 Asha   NaN   40000
   102 Ravi   NaN   35000
 EmpID Name    Dept  Salary
   101 Asha      HR   40000
   102 Ravi Finance   35000
```
**Version / licensing note:** MissingField behaviour from Microsoft Learn: Table.SelectColumns, Table.RenameColumns, Table.TransformColumnTypes. Resilience table (Choose columns, Remove bottom rows, unpivot selected) from Microsoft Learn: Best Practices When Working with Power Query.
**Edge cases:** `UseNull` hides the problem: the report loads with blank departments. Add a check, for example count of nulls. A changed header row position also breaks Promote Headers.
**Likely follow-ups:** 1) *Why not rename by position?* Fragile if columns reorder. 2) *How do you alert on silent nulls?* Add a validation query or data quality visual.
**Common mistakes:** Using "Remove Other Columns" without a missing-field option; fixing by editing the step names instead of the cause.

### Q49 ⭐ 🟢 What is Column From Examples in Power Query?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the shortcut for building a transformation by showing the result you want?
**Say this in the interview:** "Column From Examples lets me type the output I want for one or two rows and Power Query works out the transformation and fills the rest, which is useful when I know the result but not the function."
**Explain simply:**
- Path: Add Column tab > General group > Column From Examples, then From All Columns or From Selection.
- You type an example in the new column; Power Query suggests a transformation and shows its M formula above the preview.
- It only looks at the top 100 rows of the preview.
- It supports many text, date, time and number transforms, conditional columns and bucketing.
**Example:** Employee codes like `EMP-1042-HYD`: type `HYD` in the first row and the rest follow.
**Sample data:** Table `Employee_Codes`.

| Code |
|---|
| EMP-1042-HYD |
| EMP-1043-BLR |
| EMP-1050-HYD |

**DAX / Steps (not run here):** Select Code > Add Column > Column From Examples > From Selection. Type `HYD`, press Enter, review the filled rows, correct any wrong one, then OK.
**Alternative:** Transform > Split Column > By Delimiter, or Extract > Text After Delimiter.
**Result:** Expected output reproduced with pandas: Location = HYD, BLR, HYD. The exact M that Power Query would infer was not run here.
**Pandas check:**
```python
import pandas as pd
e = pd.DataFrame({"Code":["EMP-1042-HYD","EMP-1043-BLR","EMP-1050-HYD"]})
e["Location"] = e.Code.str.split("-").str[2]
print(e.to_string(index=False))
```
Real printed output (pandas 3.0.5):
```text
        Code Location
EMP-1042-HYD      HYD
EMP-1043-BLR      BLR
EMP-1050-HYD      HYD
```
**Version / licensing note:** Location, top-100-row limit and supported transformation list from Microsoft Learn: Add a column from examples - Power Query (2026-06).
**Edge cases:** Only the first 100 rows are examined, so a pattern that changes later may be wrong. Review the formula it writes.
**Likely follow-ups:** 1) *What if it infers the wrong rule?* Add more examples. 2) *Can you edit the result?* Yes, it becomes ordinary M.
**Common mistakes:** Trusting it without scanning later rows; using it on data with irregular patterns.

### Q50 ⭐ 🟢 What is the Query Dependencies view used for?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you navigate a file with many queries and know what breaks if one changes?
**Say this in the interview:** "It draws a map of which queries feed which. I use it to see the flow from raw sources to staging to final tables, and to check what depends on a query before I change it."
**Explain simply:**
- In Power BI Desktop it is under the View tab in Power Query Editor (path from memory, unverified).
- Each box is a query; arrows show "feeds into".
- Helps spot circular or unused queries and find which load to the model.
- The separate Diagram view (with "Highlight related queries") is described by Microsoft as Power Query Online only.
**Example:** `Stg_Employees` feeds three tables. If its column names change, those three break.
**Sample data:** Table `Query_Map`.

| Query | Reads from |
|---|---|
| Stg_Employees | Raw_HR_Export |
| Dim_Employee | Stg_Employees |
| Dim_Dept | Stg_Employees |
| Fact_Attendance | Raw_Attendance, Dim_Employee |

**DAX / Steps (not run here):** Power Query Editor > View tab > Query Dependencies. Use it before renaming or deleting a query.
**Alternative:** Check each query's Advanced Editor for references, slower and error-prone.
**Result:** Reproduced with pandas as a graph walk: if `Stg_Employees` changes, Dim_Dept, Dim_Employee and Fact_Attendance are affected; if `Raw_Attendance` changes, only Fact_Attendance.
**Pandas check:**
```python
deps = {"Stg_Employees":["Raw_HR_Export"], "Dim_Employee":["Stg_Employees"], "Dim_Dept":["Stg_Employees"],
        "Fact_Attendance":["Raw_Attendance","Dim_Employee"]}
def downstream(q):
    out = set()
    for k, v in deps.items():
        if q in v: out |= {k} | downstream(k)
    return out
print("Stg_Employees  ->", sorted(downstream("Stg_Employees")))
print("Raw_Attendance ->", sorted(downstream("Raw_Attendance")))
```
Real printed output (pandas 3.0.5):
```text
Stg_Employees  -> ['Dim_Dept', 'Dim_Employee', 'Fact_Attendance']
Raw_Attendance -> ['Fact_Attendance']
```
**Version / licensing note:** The Desktop menu location is from memory, unverified. Diagram view is "only available in Power Query Online" per Microsoft Learn: Diagram view - Power Query (2026-06).
**Edge cases:** Disabled-load queries still appear. Reference chains can make refresh evaluate a base query more than once (from memory, unverified).
**Likely follow-ups:** 1) *Reference vs Duplicate?* Reference follows changes in the original (Microsoft documents this). 2) *How to group queries?* Right-click > Move to Group.
**Common mistakes:** Deleting a "staging" query that others depend on; never looking at the view in big files.

### Q51 ⭐ 🟢 What is the difference between Power Query in Excel and Power Query in Power BI Desktop?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know it is the same engine with different hosts, destinations and extras?
**Say this in the interview:** "It is the same Power Query engine and M language. The difference is the host: Excel loads results to a sheet or the Excel data model, Power BI Desktop loads to a Power BI model for reports. Features such as connectors, destinations and scheduled refresh depend on the host."
**Explain simply:**
- Microsoft's table lists the M engine and Power Query Desktop in both Excel (Windows and Mac) and Power BI.
- Power BI also has Power Query Online and dataflows; Excel desktop does not.
- Microsoft states connectors, authentication, destinations and capabilities can differ by host.
- Power BI Desktop runs on Windows only (as in Q1: from memory, unverified; the sources file has this only from vendor blogs, not Microsoft); Excel for Mac has Power Query, but privacy levels are not supported on Excel for Mac.
**Example:** An HR analyst cleans a joiners list in Excel for a quick pivot; the same query pasted into Power BI feeds a shared dashboard.
**DAX / Steps (not run here):** Excel: Data tab > Get Data > Launch Power Query Editor. Power BI Desktop: Home > Transform data. M code can be copied via Advanced Editor.
**Alternative:** Use Dataflows (Q60) when many reports need the same prepared data.
**Version / licensing note:** Hosts, Online vs Desktop, dataflows table from Microsoft Learn: What Is Power Query? (2026-09-30). "Free" from Microsoft Learn: Download Power BI Desktop (2026-10-09); the Windows 10 or later requirement: from memory, unverified. Excel Mac privacy levels from Microsoft Learn: Privacy Levels in Power Query (2026-08).
**Edge cases:** Some connectors exist in one host only. A query copied between hosts may need credential setup and different privacy settings.
**Likely follow-ups:** 1) *Can I copy queries between them?* Yes via Advanced Editor or copy/paste. 2) *Does Excel refresh on a schedule?* Not on its own; Microsoft names Power BI as a product with scheduled refresh.
**Common mistakes:** Believing they use different languages; assuming every connector exists in both.

### Q52 ⭐ 🟢 Why does Power Query add a Changed Type step automatically, and when can that cause problems?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know it is a guess from a sample, not a guarantee?
**Say this in the interview:** "For unstructured sources such as CSV and Excel, Power Query inspects the first 200 rows and adds Promote Headers and Changed Type to assign data types. It can go wrong because it guesses: leading zeros in IDs vanish, a bad value later in the file becomes an error, and dates follow the machine's locale."
**Explain simply:**
- Type detection is on by default for unstructured sources; databases bring their own types.
- Turn it off in Options and settings > Options > Global (or Current file) > Data load > Type detection.
- Locale decides how text becomes dates; day/month text on a US-locale machine misreads silently or errors.
- Best practice: set types deliberately, ideally after cleaning.
**Example:** EmpID "00123" turned into number 123; "31/12/2025" fails but "05/06/2025" silently becomes 6 May.
**Sample data:** Table `Joiners_Raw` (all text).

| EmpID | Joined | Bonus |
|---|---|---|
| 00123 | 05/06/2025 | 5000 |
| 00456 | 31/12/2025 | N/A |
| 01789 | 10/02/2024 | 7500 |

**DAX / Steps (not run here):**
```m
Table.TransformColumnTypes(Promoted, {{"EmpID", type text}, {"Joined", type date}, {"Bonus", type number}}, "en-GB")
```
**Alternative:** Right-click column > Change Type > Using Locale; or disable auto detection and type each column yourself.
**Result:** Reproduced with pandas: EmpID as number gives 123, 456, 1789 (zeros lost). Bonus gives 5000, error/NaN, 7500. Month-first dates give 6 May 2025, an error for 31/12/2025, 2 Oct 2024; day-first gives 5 Jun 2025, 31 Dec 2025, 10 Feb 2024.
**Pandas check:**
```python
import pandas as pd
raw = pd.DataFrame({"EmpID":["00123","00456","01789"],"Joined":["05/06/2025","31/12/2025","10/02/2024"],"Bonus":["5000","N/A","7500"]})
print(pd.to_numeric(raw.EmpID).tolist())
print(pd.to_numeric(raw.Bonus, errors="coerce").tolist())
print(pd.to_datetime(raw.Joined, format="%m/%d/%Y", errors="coerce").dt.strftime("%Y-%m-%d").tolist())
print(pd.to_datetime(raw.Joined, format="%d/%m/%Y").dt.strftime("%Y-%m-%d").tolist())
```
Real printed output (pandas 3.0.5):
```text
[123, 456, 1789]
[5000.0, nan, 7500.0]
['2025-05-06', nan, '2024-10-02']
['2025-06-05', '2025-12-31', '2024-02-10']
```
**Version / licensing note:** 200-row detection, settings path and locale behaviour from Microsoft Learn: Data Types in Power Query (2026-08). Desktop only for the options path.
**Edge cases:** Only the first 200 rows are inspected, so later bad values error at refresh. Extra Changed Type steps pile up if you keep adding them.
**Likely follow-ups:** 1) *Fix a US/UK date?* Using Locale (Q41). 2) *Why Any type is bad?* It disables type-specific features.
**Common mistakes:** Letting IDs become numbers; accepting the auto step without checking errors.

### Q53 ⭐ 🟡 What is fuzzy matching in a Power Query merge, and when would you use it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know how to join messy text, and the risk of false matches?
**Say this in the interview:** "Fuzzy matching lets a merge join text that is similar rather than identical, for example 'Hydrabad' with 'Hyderabad'. I use it for free-typed fields such as city or company names, check the similarity score, and tune the threshold or add a transformation table for stubborn cases."
**Explain simply:**
- Tick "Use fuzzy matching to perform the merge" in the Merge dialog; only for text columns.
- Power Query uses Jaccard similarity (how much two words overlap in the small pieces they share); the default similarity threshold is 0.80, where 1.00 is exact.
- Options: Ignore case, Match by combining text parts, Show similarity scores, Number of matches, Transformation table.
- Review results; fuzzy joins can match wrongly.
**Example:** A candidate form where city is free text; match to a master list of cities.
**Sample data:** Table `Candidates` (City) and master `Cities`: Hyderabad, Bengaluru, Mumbai.

| Input | Best master | My illustrative score | Matched at 0.5 |
|---|---|---|---|
| Hyderabad | Hyderabad | 1.00 | Hyderabad |
| Hydrabad | Hyderabad | 0.67 | Hyderabad |
| Bangalore | Bengaluru | 0.23 | no match |
| Mumbay | Mumbai | 0.67 | Mumbai |
| Pune | (none close; best is Hyderabad) | 0.00 | no match |

**DAX / Steps (not run here):** Home > Merge Queries > pick both tables and the text columns > tick the fuzzy option > Fuzzy matching options. "Bangalore" would need a transformation table (From Bangalore, To Bengaluru).
**Alternative:** Clean the text first (Trim, Proper, Replace Values) or use a mapping table with a normal merge.
**Result:** Illustration only, reproduced with pandas using bigram Jaccard (my own approximation, Power Query's exact algorithm and scores differ): close spellings match, Bangalore does not.
**Pandas check:**
```python
import pandas as pd
def bg(s): s = s.lower(); return {s[i:i+2] for i in range(len(s)-1)}
def jac(a, b): A, B = bg(a), bg(b); return len(A & B)/len(A | B)
master = ["Hyderabad","Bengaluru","Mumbai"]
rows = []
for x in ["Hyderabad","Hydrabad","Bangalore","Mumbay","Pune"]:
    best = max(master, key=lambda m: jac(x, m)); sc = jac(x, best)
    rows.append((x, best, round(sc, 2), best if sc >= 0.5 else "no match"))
print(pd.DataFrame(rows, columns=["Input","Best master","Score","Matched at 0.5"]).to_string(index=False))
```
Real printed output (pandas 3.0.5):
```text
    Input Best master  Score Matched at 0.5
Hyderabad   Hyderabad   1.00      Hyderabad
 Hydrabad   Hyderabad   0.67      Hyderabad
Bangalore   Bengaluru   0.23       no match
   Mumbay      Mumbai   0.67         Mumbai
     Pune   Hyderabad   0.00       no match
```
**Version / licensing note:** Options, 0.80 default, text-only and Jaccard from Microsoft Learn: Fuzzy merge - Power Query (page dated 2024).
**Edge cases:** Lower threshold means more false matches; performance cost on big tables; blanks.
**Likely follow-ups:** 1) *How do you check quality?* Show similarity scores. 2) *Fix one known pair?* Transformation table.
**Common mistakes:** Trusting default matches blindly; using fuzzy matching on numeric keys.

### Q54 ⭐ 🟡 How do you build a date (calendar) table in Power Query?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you create a proper date dimension with year, month and financial-year columns?
**Say this in the interview:** "I generate a list of consecutive dates with `List.Dates`, turn it into a table, set the type to date, and add columns such as Year, Month number, Month name and an April-March financial year. Then I relate it to my fact tables and mark it as the date table."
**Explain simply:**
- A date table has one row per day with no gaps; time intelligence relies on it.
- `List.Dates(start, count, step)` returns `count` dates starting at `start`, adding `step` each time.
- Count = days between start and end plus 1.
- India's financial year runs April to March, so FY depends on month.
**Example:** Calendar for 2025: 365 rows.
**Sample data:** Result table `Calendar` (selected rows).

| Date | Year | MonthName | FY |
|---|---|---|---|
| 2025-01-01 | 2025 | January | FY2024-25 |
| 2025-03-31 | 2025 | March | FY2024-25 |
| 2025-04-01 | 2025 | April | FY2025-26 |
| 2025-12-31 | 2025 | December | FY2025-26 |

**DAX / Steps (not run here):**
```m
let
    StartDate = #date(2025,1,1),
    EndDate = #date(2025,12,31),
    DayCount = Duration.Days(EndDate - StartDate) + 1,
    Dates = List.Dates(StartDate, DayCount, #duration(1,0,0,0)),
    AsTable = Table.FromList(Dates, Splitter.SplitByNothing(), {"Date"}),
    Typed = Table.TransformColumnTypes(AsTable, {{"Date", type date}}),
    WithYear = Table.AddColumn(Typed, "Year", each Date.Year([Date]), Int64.Type),
    WithMonth = Table.AddColumn(WithYear, "MonthNo", each Date.Month([Date]), Int64.Type),
    WithName = Table.AddColumn(WithMonth, "MonthName", each Date.MonthName([Date], "en-US"), type text),
    WithFY = Table.AddColumn(WithName, "FY", each let y = if Date.Month([Date]) >= 4 then Date.Year([Date]) else Date.Year([Date]) - 1 in "FY" & Text.From(y) & "-" & Text.End(Text.From(y + 1), 2), type text)
in
    WithFY
```
Then Table tools > Mark as date table in the model (path from memory, unverified).
**Alternative:** DAX calculated table (not run here): `Calendar = CALENDAR(DATE(2025,1,1), DATE(2025,12,31))` (Microsoft Learn: CALENDAR function (DAX): inclusive range; error if start > end).
**Result:** Reproduced with pandas: 365 rows, first 2025-01-01 (FY2024-25), 2025-04-01 is the first FY2025-26 day.
**Pandas check:**
```python
import pandas as pd
cal = pd.DataFrame({"Date": pd.date_range("2025-01-01", periods=365)})
cal["FYStart"] = cal.Date.dt.year.where(cal.Date.dt.month>=4, cal.Date.dt.year-1)
cal["FY"] = "FY" + cal.FYStart.astype(str) + "-" + (cal.FYStart+1).astype(str).str[-2:]
print("rows:", len(cal), "| first:", cal.Date.min().date(), "| last:", cal.Date.max().date())
print(cal[cal.Date.isin(pd.to_datetime(["2025-01-01","2025-03-31","2025-04-01","2025-12-31"]))][["Date","FY"]].to_string(index=False))
```
Real printed output (pandas 3.0.5):
```text
rows: 365 | first: 2025-01-01 | last: 2025-12-31
      Date        FY
2025-01-01 FY2024-25
2025-03-31 FY2024-25
2025-04-01 FY2025-26
2025-12-31 FY2025-26
```
**Version / licensing note:** Functions from Microsoft Learn pages List.Dates, Table.FromList, Duration.Days, Date.Year, Date.Month, Date.MonthName, Table.AddColumn. `Text.From`, `Text.End` not individually fetched.
**Edge cases:** Calendar must cover all fact dates; leap years; week start day; the date column must be date type, not datetime with time.
**Likely follow-ups:** 1) *Why not use auto date/time?* A shared date table gives control (from memory). 2) *Dynamic end date?* Use `Date.From(DateTime.LocalNow())` (not verified).
**Common mistakes:** Gaps in dates; forgetting to mark as date table; hard-coding an end date that expires.

### Q55 ⭐ 🟡 What is a custom function in Power Query, and how do you create and invoke one?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you package repeated logic and apply it to many rows or files?
**Say this in the interview:** "A custom function is a reusable recipe: inputs go in, one output comes out. I can write one in the Advanced Editor or right-click a query and choose Create Function. Then I use Add Column > Invoke Custom Function, or call it in a column formula."
**Explain simply:**
- Basic shape: `(input) => output`.
- Right-click a query that uses parameters > Create Function; the parameters become the function's inputs.
- Invoke: Add Column > General > Invoke Custom Function, choose the function and map the column.
- The folder "Combine files" experience builds and uses a function behind the scenes.
**Example:** Tenure band from years of service.
**Sample data:** Table `Employees`.

| Emp | Years |
|---|---|
| Asha | 0.5 |
| Ravi | 1.0 |
| Meena | 2.9 |
| Karan | 4.2 |
| Divya | 7.0 |

**DAX / Steps (not run here):** New blank query `fnTenureBand`:
```m
(years as number) as text =>
    if years < 1 then "<1 yr"
    else if years < 3 then "1-3 yrs"
    else if years < 5 then "3-5 yrs"
    else "5+ yrs"
```
Then in Employees: `Table.AddColumn(Employees, "Band", each fnTenureBand([Years]), type text)`.
**Alternative:** A Conditional Column from the UI (Add Column > Conditional Column) when only one table needs it.
**Result:** Reproduced with pandas: <1 yr, 1-3 yrs, 1-3 yrs, 3-5 yrs, 5+ yrs.
**Pandas check:**
```python
import pandas as pd
def tenure_band(y):
    if y < 1: return "<1 yr"
    if y < 3: return "1-3 yrs"
    if y < 5: return "3-5 yrs"
    return "5+ yrs"
t = pd.DataFrame({"Emp":["Asha","Ravi","Meena","Karan","Divya"],"Years":[0.5,1.0,2.9,4.2,7.0]})
t["Band"] = t.Years.map(tenure_band)
print(t.to_string(index=False))
```
Real printed output (pandas 3.0.5):
```text
  Emp  Years    Band
 Asha    0.5   <1 yr
 Ravi    1.0 1-3 yrs
Meena    2.9 1-3 yrs
Karan    4.2 3-5 yrs
Divya    7.0  5+ yrs
```
**Version / licensing note:** Create Function / Invoke Custom Function and the warning that editing a function directly stops auto-updates from its sample query: Microsoft Learn: Use custom functions in Power Query (2026-04). Works in Power BI Desktop and Excel for Windows per that page.
**Edge cases:** Nulls in the input; changing a function's arguments breaks earlier invoke steps; functions invoked per row on a database source may not fold (not verified).
**Likely follow-ups:** 1) *Function vs parameter?* Parameter is a value; function is logic. 2) *Where used in folder combine?* Transform file function.
**Common mistakes:** Editing the generated function by hand and losing the link to the sample query; forgetting to update invoke arguments.

### Q56 ⭐ 🟡 What are RangeStart and RangeEnd, and how do they connect Power Query to incremental refresh?
**Asked at:** an EY intern review snippet mentions scheduled vs incremental refresh (one anecdote, content not detailed); no RangeStart-specific report found.
**What the interviewer is checking:** Do you know the reserved parameters and why the filter must fold?
**Say this in the interview:** "RangeStart and RangeEnd are two date/time parameters with those exact, case-sensitive names. I filter my date column with them, and the service overrides their values for each partition, so only recent partitions refresh. I keep one end inclusive and the other exclusive so rows are not duplicated, and I make sure the filter folds to the source."
**Explain simply:**
- Create both as Date/Time parameters in Manage Parameters.
- Filter manually with M (the standard custom filter UI cannot reference them).
- After publishing, the service replaces them per partition.
- Policy setup details are Part 7; this question is the Power Query side.
**Example:** Daily attendance table; refresh only the last 3 days.
**Sample data:** Table `Attendance`.

| Emp | Date | Hours |
|---|---|---|
| A | 2026-10-20 | 8 |
| B | 2026-10-21 | 8 |
| C | 2026-10-22 | 9 |
| D | 2026-10-22 | 7 |
| E | 2026-10-23 | 8 |
| F | 2026-10-24 | 8 |
| G | 2026-10-25 | 6 |
| H | 2026-10-26 | 8 |

**DAX / Steps (not run here):**
```m
Table.SelectRows(Source, each [Date] >= RangeStart and [Date] < RangeEnd)
```
Home > Manage Parameters > New: RangeStart, RangeEnd, type Date/Time. Then right-click table > Incremental refresh (policy, Part 7).
**Alternative:** Full scheduled refresh for small tables.
**Result:** Reproduced with pandas: RangeStart 22 Oct, RangeEnd 25 Oct returns C, D, E, F (4 rows, 32 hours). With both ends inclusive, two adjacent partitions return 7 rows but only 6 distinct, so 25 Oct is counted twice.
**Pandas check:**
```python
import pandas as pd
a = pd.DataFrame({"Emp":list("ABCDEFGH"),
                  "Date":pd.to_datetime(["2026-10-20","2026-10-21","2026-10-22","2026-10-22","2026-10-23","2026-10-24","2026-10-25","2026-10-26"]),
                  "Hours":[8,8,9,7,8,8,6,8]})
RS, RE = pd.Timestamp("2026-10-22"), pd.Timestamp("2026-10-25")
w = a[(a.Date>=RS)&(a.Date<RE)]                       # start inclusive, end exclusive
print(w.Emp.tolist(), "rows:", len(w), "hours:", w.Hours.sum())
p1 = a[(a.Date>=RS)&(a.Date<=RE)]                     # partition 1: 22-25 Oct, both ends inclusive
p2 = a[(a.Date>=RE)&(a.Date<=pd.Timestamp("2026-10-26"))]   # partition 2: 25-26 Oct, both ends inclusive
both = pd.concat([p1, p2])
print("both inclusive:", len(both), "rows,", len(both.drop_duplicates()), "distinct")
q1 = a[(a.Date>=RS)&(a.Date<RE)]; q2 = a[(a.Date>=RE)&(a.Date<pd.Timestamp("2026-10-27"))]
print("start inclusive/end exclusive:", len(pd.concat([q1,q2])), "rows,", len(pd.concat([q1,q2]).drop_duplicates()), "distinct")
```
Real printed output (pandas 3.0.5):
```text
['C', 'D', 'E', 'F'] rows: 4 hours: 32
both inclusive: 7 rows, 6 distinct
start inclusive/end exclusive: 6 rows, 6 distinct
```
**Version / licensing note:** From Microsoft Learn: Configure incremental refresh and real-time data (2026-07): reserved case-sensitive names, Date/Time type, manual filter, supported on Pro, PPU, Premium and Embedded; real-time DirectQuery partition Premium only; refresh limits 2 h Pro, 5 h Premium; "current date" is UTC unless a time zone is configured.
**Edge cases:** If the filter does not fold, import-mode refresh may fetch all rows and filter locally, defeating the purpose; the table needs a reliable date column; the model cannot be downloaded back as .pbix after publishing.
**Likely follow-ups:** 1) *Detect data changes?* Optional policy setting using a modified-date column. 2) *Which sources?* Best with SQL-type sources.
**Common mistakes:** Misspelling the names; using >= and <= on both partitions; filtering on a column other than the date.

### Q57 ⭐ 🟡 What are data source privacy levels (Private, Organizational, Public), and what causes a Formula.Firewall error?
**Asked at:** commonly asked (no company-specific report found); Adaface lists data-privacy questions (snippet only).
**What the interviewer is checking:** Do you understand the firewall's goal and the usual fixes?
**Say this in the interview:** "Privacy levels tell Power Query how sensitive each source is so it does not leak data from one source to another when it folds queries. A Formula.Firewall error appears when one step mixes sources with incompatible levels, or reads another query and a data source in the same step. I fix it by setting correct levels or restructuring queries, and I avoid ignoring privacy unless the data is safe."
**Explain simply:**
- Private: sensitive; data can't fold into other sources. Organizational: trusted group; can fold into Private and other Organizational, not Public. Public: anyone can see.
- The firewall splits queries into partitions (groups of steps checked together); a partition may access compatible sources or reference other partitions, not both.
- Within one partition, two sources are compatible only if both Public or both Organizational (per the firewall page).
- Fix: set levels, combine/rework steps, or the "Ignore privacy levels" (Fast Combine) option, with risk.
**Example:** Merging an employee-review workbook (Private) with a SQL table (Organizational) in one step blocks.
**Sample data:** Compatibility table (firewall page rule).

| Source A | Source B | Same step allowed? |
|---|---|---|
| Private | Private | error |
| Private | Organizational | error |
| Private | Public | error |
| Organizational | Organizational | OK |
| Organizational | Public | error |
| Public | Public | OK |

**DAX / Steps (not run here):** Power BI Desktop: File > Options and settings > Data source settings > Edit Permissions > Privacy Level. Options: File > Options and settings > Options > Privacy.
**Alternative:** Split the work into two queries so each accesses one source, or combine steps as Microsoft's example shows.
**Result:** Rule table reproduced with pandas from the firewall page; no Power Query run.
**Pandas check:**
```python
import pandas as pd
levels = ["Private","Organizational","Public"]
rows = []
for i, x in enumerate(levels):
    for y in levels[i:]:
        rows.append((x, y, "OK" if x==y and x!="Private" else "Formula.Firewall error"))
print(pd.DataFrame(rows, columns=["Source A","Source B","Same step"]).to_string(index=False))
```
Real printed output (pandas 3.0.5):
```text
      Source A       Source B              Same step
       Private        Private Formula.Firewall error
       Private Organizational Formula.Firewall error
       Private         Public Formula.Firewall error
Organizational Organizational                     OK
Organizational         Public Formula.Firewall error
        Public         Public                     OK
```
**Version / licensing note:** From Microsoft Learn: Behind the scenes of the Data Privacy Firewall (page notes privacy levels are unavailable in Power Platform dataflows; says some products relax a restriction) and Privacy Levels in Power Query (2026-08). The two pages describe folding at different levels of detail (privacy-levels page says Organizational can fold into Private; firewall page's same-partition rule requires both Public or both Organizational), so I treat the firewall page as the rule for the error. "Ignore" option does not apply to published semantic models per the privacy-levels page. The status of dataflows in Power BI service was not stated.
**Edge cases:** Parameters reportedly do not trigger the error (from memory, unverified); Excel for Mac does not support privacy levels.
**Likely follow-ups:** 1) *What is Fast Combine?* Ignore privacy levels. 2) *Why buffer?* Prevents further folding across zones.
**Common mistakes:** Turning off privacy to make the error vanish with sensitive data; marking everything Public.

### Q58 ⭐ 🟡 What is a native query, and how does writing a SQL statement in Get Data affect query folding?
**Asked at:** commonly asked; a Glassdoor listing includes "what is query folding" (snippet only).
**What the interviewer is checking:** Do you know the trade-off of hand-written SQL?
**Say this in the interview:** "A native query is SQL written directly in the connector's SQL statement box. The database runs it, but steps I add afterwards via that dialog route do not fold. If I need folding afterwards, I use Value.NativeQuery with EnableFolding set to true on supported connectors."
**Explain simply:**
- Get Data > SQL Server database > Advanced options > SQL statement.
- Microsoft says query folding on native queries via the dialog is limited, subsequent steps do not benefit.
- `Value.NativeQuery(Source, sql, null, [EnableFolding=true])` keeps folding for supported connectors (Redshift, Dataverse enhanced compute, BigQuery, PostgreSQL, SAP HANA, Snowflake, SQL Server).
- DDL (commands that create, change or delete tables, such as DROP, CREATE, ALTER) is not supported; you may be prompted to approve queries.
**Example:** `SELECT EmpID, Name, Dept FROM emp WHERE Status='Active'`, then filter Dept = HR.
**Sample data:** Table `emp` (6 rows, 4 Active).
**DAX / Steps (not run here):**
```m
let
    Source = Sql.Database("MyServer", "HRDB"),
    Active = Value.NativeQuery(Source, "SELECT EmpID, Name, Dept FROM emp WHERE Status = 'Active'", null, [EnableFolding = true]),
    HR = Table.SelectRows(Active, each [Dept] = "HR")
in
    HR
```
**Alternative:** A SQL view in the database, or build the filter with normal steps so folding is automatic.
**Result:** The SQL ran for real in SQLite here: native query returns 4 rows; wrapping a later filter as a subquery returns 2 (Asha, Meena); done locally it pulls 4 rows then keeps 2. Power Query itself was not run.
**Pandas check:**
```python
import sqlite3, pandas as pd
con = sqlite3.connect(":memory:")
pd.DataFrame({"EmpID":[1,2,3,4,5,6],"Name":["Asha","Ravi","Meena","Karan","Priya","Dev"],
              "Dept":["HR","IT","HR","Sales","IT","HR"],
              "Status":["Active","Active","Active","Active","Left","Left"]}).to_sql("emp", con, index=False)
native = pd.read_sql("select EmpID,Name,Dept from emp where Status='Active'", con)
print("native query rows:", len(native))
wrapped = pd.read_sql("select * from (select EmpID,Name,Dept from emp where Status='Active') where Dept='HR'", con)
print("filter pushed into SQL (folded):", wrapped.Name.tolist())
print("filter done locally:", native[native.Dept=="HR"].Name.tolist(), "(after pulling", len(native), "rows)")
```
Real printed output (pandas 3.0.5):
```text
native query rows: 4
filter pushed into SQL (folded): ['Asha', 'Meena']
filter done locally: ['Asha', 'Meena'] (after pulling 4 rows)
```
**Version / licensing note:** From Microsoft Learn: Import data from a database using native database query (2025-08) and Query folding on native queries (2026-06). Incremental refresh page shows a non-folding native query with range parameters in SQL.
**Edge cases:** Approval prompts for new query text; DDL unsupported; SQL injection risk when concatenating parameters.
**Likely follow-ups:** 1) *Folding on CSV?* No. 2) *Check folding?* View Native Query / query plan.
**Common mistakes:** Pasting a huge SQL then filtering locally; using SELECT * on wide tables.

### Q59 ⭐ 🟡 How would you structure queries into staging, dimension and fact queries in a Power BI file?
**Asked at:** commonly asked (no company-specific report found); gap-fill item.
**What the interviewer is checking:** Can you organise a clean pipeline and a star schema?
**Say this in the interview:** "I make one staging query per source that only connects and does basic cleaning, with load disabled. Dimension queries reference staging and keep one row per employee, department or date; fact queries reference staging and keep the measurable events with keys. Only dimensions and facts load into the model."
**Explain simply:**
- Staging = raw cleaned copy; dimensions = descriptive lists; facts = numbers/events.
- Use Reference so changes in staging flow downstream.
- Use groups (folders), meaningful names, Extract Previous to split long queries.
- Disable load on staging (right-click > Enable load) to keep the model small.
**Example:** Monthly attendance export.
**Sample data:** Staging `Stg_Attendance` (5 rows) -> `Dim_Employee` (3), `Dim_Dept` (2), `Fact_Attendance` (5).

| EmpID | Name | Dept | Month | DaysPresent |
|---|---|---|---|---|
| 101 | Asha | HR | 2026-08 | 21 |
| 101 | Asha | HR | 2026-09 | 20 |
| 102 | Ravi | Finance | 2026-08 | 22 |
| 102 | Ravi | Finance | 2026-09 | 19 |
| 103 | Meena | HR | 2026-09 | 18 |

`Dim_Dept` gives each department a key: HR = 1, Finance = 2.

**DAX / Steps (not run here):** Right-click Stg_Attendance > Reference; rename to Dim_Employee; Choose Columns EmpID, Name, Dept; Remove Duplicates. Repeat for Dim_Dept. Fact: reference staging, merge Dept to get DeptKey, keep EmpID, DeptKey, Month, DaysPresent. Right-click Stg_Attendance > uncheck Enable load.
**Alternative:** A single wide table (simple, but repeats text and is harder to filter).
**Result:** Reproduced with pandas: 5 raw rows split into 3 employees, 2 departments, 5 fact rows; all fact EmpIDs exist in Dim_Employee.
**Pandas check:**
```python
import pandas as pd
stg = pd.DataFrame({"EmpID":[101,101,102,102,103],"Name":["Asha","Asha","Ravi","Ravi","Meena"],
                    "Dept":["HR","HR","Finance","Finance","HR"],
                    "Month":["2026-08","2026-09","2026-08","2026-09","2026-09"],"DaysPresent":[21,20,22,19,18]})
dim_emp = stg[["EmpID","Name","Dept"]].drop_duplicates()
dim_dept = pd.DataFrame({"Dept":stg.Dept.drop_duplicates().tolist()}); dim_dept["DeptKey"] = range(1, len(dim_dept)+1)
fact = stg.merge(dim_dept, on="Dept")[["EmpID","DeptKey","Month","DaysPresent"]]
print("Dim_Employee:", len(dim_emp), "| Dim_Dept:", len(dim_dept), "| Fact_Attendance:", len(fact))
print("all fact EmpIDs in Dim_Employee:", fact.EmpID.isin(dim_emp.EmpID).all())
print(fact.to_string(index=False))
```
Real printed output (pandas 3.0.5):
```text
Dim_Employee: 3 | Dim_Dept: 2 | Fact_Attendance: 5
all fact EmpIDs in Dim_Employee: True
 EmpID  DeptKey   Month  DaysPresent
   101        1 2026-08           21
   101        1 2026-09           20
   102        2 2026-08           22
   102        2 2026-09           19
   103        1 2026-09           18
```
**Version / licensing note:** Split queries (Extract Previous), groups, Reference from Microsoft Learn: Best Practices When Working with Power Query and Diagram view (describes Enable load for Online; Desktop right-click is from memory, unverified).
**Edge cases:** Many references from one base source can read it multiple times at refresh (from memory, unverified); keys must be unique in dimensions; privacy firewall issues when mixing sources across references (Q57).
**Likely follow-ups:** 1) *Reference vs Duplicate?* Q50. 2) *Where does the star schema belong?* Part 3.
**Common mistakes:** Loading staging queries; dimensions with duplicate keys; hard-coding transformations in every query.

### Q60 ⭐ 🟡 What is a dataflow, and how does it relate to Power Query?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know dataflows are Power Query in the cloud for reuse?
**Say this in the interview:** "A dataflow is Power Query running as a cloud service. I build and schedule the cleaning once in the browser, store the result, and many reports and datasets reuse it, so everyone gets one consistent version of, say, the employee table."
**Explain simply:**
- Dataflows use Power Query Online, the browser experience.
- Goals: reusable logic, a single source of truth, less load on source systems, and (Gen1) storing data in Azure Data Lake Gen2.
- Power BI Dataflow Gen1 is legacy; Dataflow Gen2 (Fabric) is recommended where available and adds destinations and pipelines.
- Refresh is scheduled from the workspace.
**Example:** HR master data cleaned once in a dataflow; headcount, attrition and payroll reports all connect to it.
**DAX / Steps (not run here):** Service > workspace > New > Dataflow (menu names change; from memory, unverified); build queries in Power Query Online; schedule refresh; in Desktop Get Data > Dataflows.
**Alternative:** Keep Power Query inside each .pbix (simple, but duplicated logic).
**Version / licensing note:** From Microsoft Learn: Introduction to Dataflows and Self-service Data Prep (legacy) (2025-10): Gen1 is legacy; Premium customers with Fabric access are pointed to Gen2; Pro/PPU can continue Gen1. Microsoft Learn: Differences between Dataflow Gen1 and Dataflow Gen2 (2026-08): Gen2 requires Fabric capacity, a Fabric trial or Power BI Premium capacity; Gen1 stores in internal storage, Gen2 supports multiple destinations; Gen1 supports DirectQuery via the connector, Gen2 does not. Microsoft Learn: What Is Power Query? lists Power BI dataflows as Power Query Online hosts.
**Edge cases:** Privacy levels are stated as unavailable in Power Platform dataflows (the page does not say about Power BI dataflows). Gen1 vs Gen2 availability by licence changes.
**Likely follow-ups:** 1) *Dataflow vs semantic model (the Power BI data model)?* Dataflow prepares data; the model defines relationships and measures. 2) *Dataflow vs staging query?* Dataflow is shared across files.
**Common mistakes:** Treating dataflows as a replacement for modelling; using Gen2 on a Pro-only tenant without capacity.

### Q61 ⭐ 🔴 What does Table.Buffer do, and when might you use it?
**Asked at:** commonly asked (no company-specific report found); the sources found only a forum thread, not an interview report.
**What the interviewer is checking:** Do you know it freezes a table in memory, and the cost?
**Say this in the interview:** "Table.Buffer loads a table fully into memory and isolates it from changes during evaluation. I use it when a result must be stable, for example sort then remove duplicates, or to stop downstream folding on purpose. But it can make things slower, because it reads everything and blocks folding, so I use it sparingly."
**Explain simply:**
- Microsoft: buffers a table in memory, isolating it from external changes during evaluation; shallow buffering forces scalar cell values only.
- It may or may not help; it can slow queries because all data is read and stored, and it prevents downstream folding.
- If you only want to stop folding, use `Table.StopFolding` instead.
- Table.Sort and Table.Distinct pages recommend buffering for predictable ordering.
**Example:** Keep latest record per employee: sort descending, then remove duplicates; buffer the sorted table so which duplicate survives is predictable (Q47).
**Sample data:** The Q47 `Salary_History` table.
**DAX / Steps (not run here):**
```m
let
    Sorted = Table.Sort(Source, {{"EmpID", Order.Ascending}, {"EffectiveDate", Order.Descending}}),
    Buffered = Table.Buffer(Sorted),
    Latest = Table.Distinct(Buffered, {"EmpID"})
in
    Latest
```
**Alternative:** Table.Group with Table.Max (no buffer needed), or Table.StopFolding.
**Result:** Analogy only, reproduced with pandas: an unbuffered source referenced twice is read 2 times; buffered once. This models the idea, not Power Query's actual engine behaviour, which I did not verify.
**Pandas check:**
```python
import pandas as pd
reads = 0
def source():                      # stands for a slow source that is re-read every time it is evaluated
    global reads; reads += 1
    return pd.DataFrame({"EmpID":[1,2,3]})
a = source(); b = source()         # unbuffered: referenced twice, read twice
print("unbuffered reads:", reads)
reads = 0
buf = source().copy()              # buffered: one read, reused
a, b = buf, buf
print("buffered reads:", reads)
```
Real printed output (pandas 3.0.5):
```text
unbuffered reads: 2
buffered reads: 1
```
**Version / licensing note:** From Microsoft Learn: Table.Buffer (updated 2026-04), Table.StopFolding, Table.Distinct, Table.Sort, and the privacy-firewall page (buffering as a firewall tool). Works in all Power Query hosts.
**Edge cases:** Large tables exhaust memory; buffering early blocks folding for every later step; buffering is shallow (nested tables, lists, records stay as-is).
**Likely follow-ups:** 1) *Buffer vs StopFolding?* StopFolding avoids reading into memory. 2) *When is it a mistake?* Right after Source on a big SQL table.
**Common mistakes:** Sprinkling Table.Buffer everywhere hoping for speed; buffering before filters.
