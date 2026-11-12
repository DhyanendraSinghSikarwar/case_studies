# Book 4 — Power BI & Visualization | Part 3: Data Modelling: Star Schema, Relationships, Cardinality 🟡

**Target:** 60 questions | **Actual:** 60 questions
**Scope:** star schema, fact and dimension tables, relationships, cardinality, filter direction, date tables, role-playing dimensions and common modelling errors in Power BI.

### Q1 ⭐⭐⭐ 🟢 What is a data model in Power BI, and why do we build one instead of loading a single flat table?
**Asked at:** commonly asked (no company-specific report found for this exact question). Data modelling as a topic appears in the 2026 Weekday India Power BI list; our interview-process notes mention star-schema/data-modelling questions at Flipkart and Amazon BIE without giving the wording.
**What the interviewer is checking:** Whether you know Power BI is built on related tables, not one giant sheet.
**Say this in the interview:** "A data model is the set of tables in Power BI plus the relationships between them. I split data into small tables, such as Employee, Department and Attendance, and link them, so each fact is stored once and filters flow correctly. A single flat table repeats data, grows large and makes totals easy to get wrong."
**Explain simply:**
- **Table:** rows and columns of one subject (employees, attendance days). **Relationship:** a link between a column in one table and a column in another, so a filter on one table also filters the other.
- A flat table repeats text on every row (the department name appears once per attendance day), which is wasteful and hard to correct.
- A flat table also confuses counting: one employee appears on many rows, so "count of rows" is not headcount.
- Microsoft's guidance is to build tables that are either filter/group tables (dimensions) or summarise tables (facts), which is the star schema (Q2). Source: Microsoft Learn, "Understand star schema and the importance for Power BI".
**Example:** 4 employees, 2 attendance days each. The flat table has 8 rows; counting rows says "8 employees". The model has 4 Employee rows and 8 Attendance rows, and the correct headcount is 4.
**Sample data:** Table `Employee`:

| EmpID | Name | Dept |
|---|---|---|
| E1 | Asha | Sales |
| E2 | Ravi | Sales |
| E3 | Meena | Finance |
| E4 | Kiran | HR |

Table `Attendance` (one row per employee per day; first 4 of 8 rows shown):

| EmpID | Date | Status |
|---|---|---|
| E1 | 01-Jan | Present |
| E1 | 02-Jan | Present |
| E2 | 01-Jan | Present |
| E2 | 02-Jan | Absent |

**DAX / Steps (not run here):**
```dax
Headcount = DISTINCTCOUNT ( Employee[EmpID] )
```
Steps: Home > Get data > load both tables > Model view icon (left edge) > check the line from Employee[EmpID] to Attendance[EmpID] (Q17).
**Alternative:** `Headcount = COUNTROWS ( Employee )` on the model, because each employee is one row there. Syntax checked against Microsoft Learn: DISTINCTCOUNT function (DAX) and COUNTROWS function (DAX).
**Result:** Reproduced with pandas (not run in Power BI): headcount is 4 on the model; the flat table gives 8 if you count rows.
**Pandas check:**
```python
import pandas as pd
employee = pd.DataFrame({"EmpID": ["E1","E2","E3","E4"], "Name": ["Asha","Ravi","Meena","Kiran"],
                         "Dept": ["Sales","Sales","Finance","HR"]})
attendance = pd.DataFrame({"EmpID": ["E1","E1","E2","E2","E3","E3","E4","E4"],
                           "Date": ["01-Jan","02-Jan"]*4,
                           "Status": ["Present","Present","Present","Absent","Present","Present","Absent","Absent"]})
flat = attendance.merge(employee, on="EmpID")           # the one big flat table
print("Flat table rows (a naive 'headcount' by counting rows):", len(flat))
print("Distinct employees (what DISTINCTCOUNT gives):", flat["EmpID"].nunique())
print("Model: Employee rows =", len(employee), "| Attendance rows =", len(attendance))
```
Printed output:
```
Flat table rows (a naive 'headcount' by counting rows): 8
Distinct employees (what DISTINCTCOUNT gives): 4
Model: Employee rows = 4 | Attendance rows = 8
```
**Version / licensing note:** Model view and relationships are Power BI Desktop features (Microsoft Learn: "Model view in Power BI Desktop"). That Desktop is free and Windows-only is from memory, unverified.
**Edge cases:** A flat table is fine for a tiny one-off chart. DISTINCTCOUNT counts a BLANK as a value (Microsoft Learn: DISTINCTCOUNT function), so clean blank IDs.
**Likely follow-ups:** 1) *Does a model run faster?* Microsoft says well-designed models are optimised for performance and usability; I would not quote a number. 2) *How many tables?* As many as the business entities need, no more.
**Common mistakes:** Merging everything into one table in Power Query "to keep it simple"; counting rows and calling it headcount.

### Q2 ⭐⭐⭐ 🟢 What is a star schema?
**Asked at:** commonly asked (no company-specific report found for this exact question). Star schema is flagged in our interview-process notes at Flipkart (2022 senior report) and Amazon BIE (SQL plus data modelling round); wording not reported.
**What the interviewer is checking:** Can you describe the standard Power BI model shape in one breath?
**Say this in the interview:** "A star schema has one or more fact tables in the middle that hold the numbers and events, and dimension tables around them that describe things like employee, date and department. Each dimension links to the fact with a one-to-many relationship, so the picture looks like a star."
**Explain simply:**
- **Dimension tables** describe things (employees, products, time) and give you the columns to filter and group by. **Fact tables** store events or observations (payroll runs, attendance days) with numbers to add up.
- Dimensions have a unique key and usually relatively few rows; facts can be very large and keep growing (Microsoft Learn, star schema article).
- Rule of thumb from Microsoft: dimensions enable filtering and grouping, facts enable summarisation.
**Example:** HR payroll star.
```
        Department      Calendar
              \          /
               \        /
   Employee ---- Payroll (fact) ---- Location
        (each line is one-to-many: dimension 1 ---> * fact)
```
**DAX / Steps (not run here):** Model view > drag each dimension key (Employee[EmpID], Calendar[Date], Location[LocID]) onto the matching column in Payroll > confirm each line shows 1 at the dimension end and * at the fact end. Then `Total Net Pay = SUM ( Payroll[NetPay] )` (SUM function (DAX), checked).
**Alternative:** Snowflake schema (Q10), where dimensions are split into several linked tables.
**Version / licensing note:** The guidance is design theory from Microsoft Learn, "Understand star schema and the importance for Power BI" (page date 2026-04); it applies to Desktop and the Service alike (the page does not say otherwise).
**Edge cases:** Some models have several fact tables sharing dimensions (attendance and payroll sharing Employee and Calendar). Do not mix a fact and a dimension in one table, except for a degenerate dimension such as an order number kept in the fact (same page).
**Likely follow-ups:** 1) *Why not one big table?* Q1. 2) *How do I know which table is the fact?* The "many" side of one-to-many relationships.
**Common mistakes:** Calling any model with several tables a star; relating two fact tables directly.

### Q3 ⭐⭐⭐ 🟢 What is the difference between a fact table and a dimension table? Give an HR example.
**Asked at:** commonly asked (no company-specific report found for this exact question); "fact vs dimension" appears in the 2026 Weekday India Power BI list.
**What the interviewer is checking:** Do you place real tables into the right role?
**Say this in the interview:** "A dimension table describes who or what, like Employee or Department, with one row per thing. A fact table records what happened, like each monthly payroll line or each attendance day, with numbers I can sum. I filter by dimensions and summarise facts."
**Explain simply:**
- Dimension: unique key, descriptive text columns (name, department, grade), fewer rows.
- Fact: foreign keys that point to dimensions, plus numbers (net pay, hours); many rows, keeps growing.
- Power BI has no "table type" setting; the role comes from relationships: the "one" side is the dimension and the "many" side is the fact (Microsoft Learn, star schema article).
**Example:** `Department` and `Employee` are dimensions; `Payroll` (one row per employee per month) is the fact. Sales department net pay is 182,000 across two months.
**Sample data:** Table `Department` (dimension):

| DeptID | DeptName |
|---|---|
| D1 | Sales |
| D2 | Finance |
| D3 | HR |
| D4 | IT |

Table `Employee` (dimension): E1 and E2 in D1, E3 in D2, E4 in D3. Table `Payroll` (fact; Jan shown, Feb has the same employees):

| Month | EmpID | NetPay |
|---|---|---|
| Jan | E1 | 50000 |
| Jan | E2 | 40000 |
| Jan | E3 | 60000 |
| Jan | E4 | 45000 |

**DAX / Steps (not run here):**
```dax
Total Net Pay = SUM ( Payroll[NetPay] )
```
Put `Department[DeptName]` on the rows of a table visual and the measure in values. Relationships: Department[DeptID] 1 to * Employee[DeptID]; Employee[EmpID] 1 to * Payroll[EmpID].
**Alternative:** Implicit measure: drag Payroll[NetPay] and set it to Sum (works, but explicit measures are safer; Microsoft's star-schema page lists reasons).
**Result:** Reproduced with pandas: Finance 120,000; HR 90,000; Sales 182,000; grand total 392,000.
**Pandas check:**
```python
import pandas as pd
dept = pd.DataFrame({"DeptID": ["D1","D2","D3","D4"], "DeptName": ["Sales","Finance","HR","IT"]})
emp = pd.DataFrame({"EmpID": ["E1","E2","E3","E4"], "DeptID": ["D1","D1","D2","D3"]})
payroll = pd.DataFrame({"Month": ["Jan"]*4 + ["Feb"]*4, "EmpID": ["E1","E2","E3","E4"]*2,
                        "NetPay": [50000,40000,60000,45000,50000,42000,60000,45000]})
x = payroll.merge(emp, on="EmpID").merge(dept, on="DeptID")   # filter flows Department -> Employee -> Payroll
print(x.groupby("DeptName")["NetPay"].sum().to_string())
print("Grand total:", payroll["NetPay"].sum())
```
Printed output:
```
DeptName
Finance    120000
HR          90000
Sales      182000
Grand total: 392000
```
**Version / licensing note:** Concept applies to Desktop and Service; no licence dependency stated on the fetched page.
**Edge cases:** IT has no employees, so it has no payroll and does not appear. A dimension row with no facts shows nothing unless "Show items with no data" is on.
**Likely follow-ups:** 1) *Is Employee ever a fact?* Not normally; a "headcount snapshot" table by month would be a fact. 2) *What is a degenerate dimension?* An identifier like order number that lives in the fact table.
**Common mistakes:** Treating the table with the most columns as the fact; putting salary in the Employee dimension and summing it across months.

### Q4 ⭐⭐⭐ 🟢 What is a relationship in Power BI, and what does it do?
**Asked at:** commonly asked (no company-specific report found for this exact question); "relationship types" appear in the 2026 Weekday India list.
**What the interviewer is checking:** Do you understand that a relationship is what lets filters travel between tables?
**Say this in the interview:** "A relationship links one column in a table to one column in another, and its job is to pass filters from one table to the other. Without it, a department slicer cannot filter payroll, and every row shows the grand total."
**Explain simply:**
- It joins on one column on each side, typically a key (EmpID, DeptID). Filters pass along the line, and can cross several tables (Microsoft Learn: "Model relationships in Power BI Desktop").
- Relationships do not enforce data integrity; unmatched values do not raise an error (same page).
- Without a relationship, Microsoft's own tutorial shows the same hours total on every project row (Microsoft Learn: "Create and manage relationships in Power BI Desktop").
**Example:** `Training` has hours per DeptID. With no relationship to `Department`, every department row shows 36 hours. With Department[DeptID] one-to-many Training[DeptID], Sales shows 20.
**Sample data:** Table `Training`:

| DeptID | TrainingHours |
|---|---|
| D1 | 12 |
| D1 | 8 |
| D2 | 10 |
| D3 | 6 |

**DAX / Steps (not run here):**
```dax
Total Training Hours = SUM ( Training[TrainingHours] )
```
Steps: Home > Manage relationships > New > pick Department and DeptID, then Training and DeptID > OK. Or in Model view drag Department[DeptID] onto Training[DeptID].
**Alternative:** `Dept Name = RELATED ( Department[DeptName] )` as a calculated column in Training (RELATED function (DAX), checked: needs a many-to-one relationship), then group by it. Works, but duplicates data; the relationship is cleaner.
**Result:** Reproduced with pandas: without relationship 36 on every row; with it Finance 10, HR 6, Sales 20.
**Pandas check:**
```python
import pandas as pd
dept = pd.DataFrame({"DeptID": ["D1","D2","D3","D4"], "DeptName": ["Sales","Finance","HR","IT"]})
emp = pd.DataFrame({"EmpID": ["E1","E2","E3","E4"], "DeptID": ["D1","D1","D2","D3"]})
training = pd.DataFrame({"DeptID": ["D1","D1","D2","D3"], "TrainingHours": [12,8,10,6]})
print("No relationship -> every department row shows:", training["TrainingHours"].sum())
print("With Department[DeptID] 1-to-many Training[DeptID]:")
print(training.merge(dept, on="DeptID").groupby("DeptName")["TrainingHours"].sum().to_string())
```
Printed output:
```
No relationship -> every department row shows: 36
With Department[DeptID] 1-to-many Training[DeptID]:
DeptName
Finance    10
HR          6
Sales      20
```
**Version / licensing note:** Manage relationships path is from the fetched page (Modeling tab > Manage relationships); the same page notes ribbon locations differ by view.
**Edge cases:** Only one active relationship may exist between two tables. Data types of the two columns should match; DateTime columns carry a time portion that can break matches (relationships page).
**Likely follow-ups:** 1) *One column or two?* One on each side; for a two-column match you build a combined key column first. 2) *Can a table relate to itself?* No; use Parent and Child functions for hierarchies (relationships page).
**Common mistakes:** Using a free-text column with typos as the key; expecting a relationship to clean the data.

### Q5 ⭐⭐⭐ 🟢 What types of cardinality can a Power BI relationship have?
**Asked at:** commonly asked (no company-specific report found for this exact question); relationship types are in the 2026 Weekday India list.
**What the interviewer is checking:** Can you name all four and say which is normal?
**Say this in the interview:** "Cardinality is how rows on one side match rows on the other. There are four: one-to-many, many-to-one, one-to-one and many-to-many. One-to-many, dimension to fact, is the normal one."
**Explain simply:**
- The "one" side column has unique values; the "many" side may repeat values.
- One-to-many (1:*) and many-to-one (*:1) are the same thing viewed from opposite ends and are the most common.
- One-to-one (1:1) is uncommon and often signals a design that should be merged into one table. Many-to-many (*:*) is infrequent and for special cases (Q12).
- Power BI detects the cardinality from your data, but can get it wrong if tables are not loaded yet; you can change it as long as the "one" side is unique. If a refresh loads duplicates into a "one" side, the refresh fails. (All from Microsoft Learn: "Model relationships in Power BI Desktop".)
**Example:** Department to Employee is 1:*. Employee to EmployeeContact (one phone row each) is 1:1. Employee to a Budget table that repeats DeptID is *:*.
**Sample data:** Same `Department`, `Employee` tables as Q3, plus `Contact` (EmpID unique) and `Budget` (D1 twice, D2 once).
**DAX / Steps (not run here):** Model view > double-click the line > Edit relationship > Cardinality drop-down. Or Home > Manage relationships > Edit.
**Alternative:** Check uniqueness yourself first: in Power Query, Column profile / Remove Duplicates, or `DISTINCTCOUNT` vs `COUNTROWS` in a test measure.
**Result:** Reproduced with pandas by testing uniqueness: Department-Employee one-to-many; Employee-Contact one-to-one; Employee-Budget many-to-many.
**Pandas check:**
```python
import pandas as pd
dept = pd.DataFrame({"DeptID": ["D1","D2","D3","D4"], "DeptName": ["Sales","Finance","HR","IT"]})
emp = pd.DataFrame({"EmpID": ["E1","E2","E3","E4"], "DeptID": ["D1","D1","D2","D3"]})
contact = pd.DataFrame({"EmpID": ["E1","E2","E3","E4"], "Phone": ["98xxxx01","98xxxx02","98xxxx03","98xxxx04"]})
budget = pd.DataFrame({"DeptID": ["D1","D1","D2"], "Year": [2025,2026,2025], "Budget": [9,10,7]})
def kind(t1, c1, t2, c2):
    return {(True,False): "one-to-many", (False,True): "many-to-one",
            (True,True): "one-to-one", (False,False): "many-to-many"}[(t1[c1].is_unique, t2[c2].is_unique)]
print("Department[DeptID] -> Employee[DeptID]:", kind(dept, "DeptID", emp, "DeptID"))
print("Employee[EmpID] -> Contact[EmpID]:     ", kind(emp, "EmpID", contact, "EmpID"))
print("Employee[DeptID] -> Budget[DeptID]:    ", kind(emp, "DeptID", budget, "DeptID"))
```
Printed output:
```
Department[DeptID] -> Employee[DeptID]: one-to-many
Employee[EmpID] -> Contact[EmpID]:      one-to-one
Employee[DeptID] -> Budget[DeptID]:     many-to-many
```
**Version / licensing note:** Microsoft Learn notes many-to-many cardinality is supported for Power BI Report Server January 2024 and later; other service-side support is not restated here.
**Edge cases:** Many-to-many relationships are "limited": no blank-row compensation and RELATED cannot be used across them (same page).
**Likely follow-ups:** 1) *Which direction do filters go in 1:*?* From the one side to the many side. 2) *Which is fastest?* One-to-many within the same source (Microsoft's performance ranking).
**Common mistakes:** Choosing many-to-many to silence a "duplicate values" error instead of fixing the key.

### Q6 ⭐⭐⭐ 🟢 What is a one-to-many relationship? Explain it with Department and Employee tables.
**Asked at:** commonly asked (no company-specific report found for this exact question).
**What the interviewer is checking:** Can you explain the most common relationship with a concrete example?
**Say this in the interview:** "One department has many employees, but each employee belongs to one department. Department is the 'one' side with a unique DeptID; Employee is the 'many' side where DeptID repeats. Selecting a department filters its employees."
**Explain simply:**
- Unique key on the one side (Department[DeptID]); repeating foreign key on the many side (Employee[DeptID]).
- Filters flow from one to many by default, so a department slicer filters employees and everything linked to employees.
- If an employee's DeptID has no match in Department, Power BI adds a virtual blank row to Department to hold it (Microsoft Learn, relationships page).
**Example:** Sales has 2 employees, Finance 1, HR 1, IT 0. The headcount measure returns 4 overall.
**Sample data:** Tables `Department` and `Employee` as in Q3 (Employee: E1 D1, E2 D1, E3 D2, E4 D3).
**DAX / Steps (not run here):**
```dax
Headcount = COUNTROWS ( Employee )
```
Relationship: Department[DeptID] (1) to Employee[DeptID] (*), single direction.
**Alternative:** `DISTINCTCOUNT ( Employee[EmpID] )`, safer if the Employee table is ever a snapshot with repeated IDs.
**Result:** Reproduced with pandas: Sales 2, Finance 1, HR 1, IT blank (COUNTROWS returns BLANK for no rows, per Microsoft Learn: COUNTROWS function, so IT does not show unless Show items with no data is on), total 4.
**Pandas check:**
```python
import pandas as pd
dept = pd.DataFrame({"DeptID": ["D1","D2","D3","D4"], "DeptName": ["Sales","Finance","HR","IT"]})
emp = pd.DataFrame({"EmpID": ["E1","E2","E3","E4"], "DeptID": ["D1","D1","D2","D3"]})
headcount = emp.groupby("DeptID").size().reindex(dept["DeptID"]).astype("Int64")
headcount.index = dept["DeptName"]
print(headcount.to_string())          # <NA> = BLANK
print("Grand total:", len(emp))
```
Printed output:
```
DeptName
Sales         2
Finance       1
HR            1
IT         <NA>
Grand total: 4
```
**Version / licensing note:** Same in Desktop and Service; the "Show items with no data" option is mentioned in Microsoft Learn: "Many-to-many relationship guidance".
**Edge cases:** Duplicate DeptID in the Department table makes it impossible to be the "one" side (Q30). Employees with a missing DeptID fall under Blank.
**Likely follow-ups:** 1) *What if an employee is in two departments?* Many-to-many; use a bridge (Q28). 2) *Which side is the fact?* The many side.
**Common mistakes:** Reversing the sides; using DeptName (which can change) as the key.

### Q7 ⭐⭐⭐ 🟢 What are a primary key and a foreign key, and how do they relate to Power BI relationships?
**Asked at:** commonly asked (no company-specific report found for this exact question).
**What the interviewer is checking:** Do you connect database keys to the columns you choose for relationships?
**Say this in the interview:** "A primary key is a column with a unique value per row, like EmpID in the Employee table. A foreign key is a column in another table that holds those values, like EmpID in Attendance. In Power BI the primary key is the 'one' side and the foreign key the 'many' side of the relationship."
**Explain simply:**
- Primary key: unique, never blank. Foreign key: values that should exist in the primary key, but may repeat.
- Power BI does not enforce either rule: relationships "don't enforce data integrity" (Microsoft Learn). Unmatched foreign keys show up under a Blank row.
- Microsoft says relationships use a single unique column; if a dimension lacks one, add an index column in Power Query (star-schema article).
**Example:** Attendance has EmpID E9, who is not in Employee. Its 8 hours land on the (Blank) department, a data-quality flag.
**Sample data:** Table `Employee` (PK EmpID E1-E4 as Q3). Table `Attendance` (FK EmpID):

| EmpID | Hours |
|---|---|
| E1 | 8 |
| E2 | 8 |
| E9 | 8 |

**DAX / Steps (not run here):**
```dax
Dept Name = RELATED ( Department[DeptName] )   // calculated column in Employee
```
Steps: Power Query > select key column > Home > Remove rows > Remove duplicates, or Add column > Index column, when you need a unique key.
**Alternative:** No measure needed: a visual that groups by a dimension column and shows a (Blank) row already tells you some foreign keys have no match.
**Result:** Reproduced with pandas: PK unique True; unmatched FK ['E9']; 8 hours on Blank; `RELATED` gives E1 Sales, E2 Sales, E3 Finance, E4 HR.
**Pandas check:**
```python
import pandas as pd
dept = pd.DataFrame({"DeptID": ["D1","D2","D3","D4"], "DeptName": ["Sales","Finance","HR","IT"]})
emp = pd.DataFrame({"EmpID": ["E1","E2","E3","E4"], "DeptID": ["D1","D1","D2","D3"]})
att = pd.DataFrame({"EmpID": ["E1","E2","E9"], "Hours": [8,8,8]})
print("Primary key Employee[EmpID] is unique:", emp["EmpID"].is_unique)
print("Foreign-key values with no match in Employee:", sorted(set(att["EmpID"]) - set(emp["EmpID"])))
print("Hours that would land on the (Blank) row:", att.loc[~att["EmpID"].isin(emp["EmpID"]), "Hours"].sum())
print(emp.merge(dept, on="DeptID")[["EmpID","DeptName"]].to_string(index=False))   # what RELATED(Department[DeptName]) returns per employee
```
Printed output:
```
Primary key Employee[EmpID] is unique: True
Foreign-key values with no match in Employee: ['E9']
Hours that would land on the (Blank) row: 8
EmpID DeptName
   E1    Sales
   E2    Sales
   E3  Finance
   E4       HR
```
**Version / licensing note:** Behaviour documented in Microsoft Learn: "Model relationships in Power BI Desktop" (updated 2026-10).
**Edge cases:** Composite keys (EmpID plus Month) need one combined column, because a relationship uses one column on each side (Microsoft Learn: star-schema article).
**Likely follow-ups:** 1) *Natural vs surrogate key?* Business ID versus a made-up unique ID you add. 2) *Can the key be text?* Yes, but numbers are lighter.
**Common mistakes:** Keys with trailing spaces or mixed case; relating on names.

### Q8 ⭐⭐⭐ 🟢 What is cross-filter direction, and what is the difference between Single and Both?
**Asked at:** commonly asked (no company-specific report found for this exact question); "bi-directional" appears in the 2026 Weekday India list.
**What the interviewer is checking:** Do you know which way filters flow and the cost of changing it?
**Say this in the interview:** "Cross-filter direction decides which way a filter travels along a relationship. Single means from the one side to the many side only, which is the safe default. Both means filters also travel back from the many side to the one side."
**Explain simply:**
- Single: a department slicer filters employees, but an employee-level filter does not filter the department list.
- Both (bi-directional): the filter also flows backwards, so the department table is filtered by employee conditions.
- Microsoft recommends using Both only as needed because it can hurt performance and create ambiguity (Microsoft Learn: "Model relationships in Power BI Desktop"; "Bi-directional relationship guidance").
**Example:** A slicer picks `Grade = Senior`. A card `Departments` counts distinct departments. Single shows 4 (all departments); Both shows 1 (only Sales has a Senior).
**Sample data:** Table `Employee` with a Grade column:

| EmpID | DeptID | Grade |
|---|---|---|
| E1 | D1 | Senior |
| E2 | D1 | Junior |
| E3 | D2 | Junior |
| E4 | D3 | Junior |

**DAX / Steps (not run here):**
```dax
Departments = DISTINCTCOUNT ( Department[DeptName] )
```
Steps: Model view > double-click the Department-Employee line > Cross filter direction > Single or Both > OK.
**Alternative:** Leave the relationship on Single and switch it for one measure only: `CALCULATE ( DISTINCTCOUNT ( Department[DeptName] ), CROSSFILTER ( Employee[DeptID], Department[DeptID], Both ) )` (CROSSFILTER function, checked: only inside CALCULATE-type functions, overrides the model setting).
**Result:** Reproduced with pandas: Single 4; Both 1.
**Pandas check:**
```python
import pandas as pd
dept = pd.DataFrame({"DeptID": ["D1","D2","D3","D4"], "DeptName": ["Sales","Finance","HR","IT"]})
emp = pd.DataFrame({"EmpID": ["E1","E2","E3","E4"], "DeptID": ["D1","D1","D2","D3"]})
emp["Grade"] = ["Senior","Junior","Junior","Junior"]
senior = emp[emp["Grade"] == "Senior"]                 # slicer: Employee[Grade] = Senior
print("Single (Department -> Employee): Departments =", dept["DeptName"].nunique())
print("Both: Departments =", dept[dept["DeptID"].isin(senior["DeptID"])]["DeptName"].nunique())
```
Printed output:
```
Single (Department -> Employee): Departments = 4
Both: Departments = 1
```
**Version / licensing note:** Options per cardinality: 1:* offers Single or Both; 1:1 is always Both; *:* offers either direction or Both (Microsoft Learn relationships page).
**Edge cases:** Power BI may refuse Both if it creates ambiguous paths (two routes between tables). Both also adds an RLS option on the relationship.
**Likely follow-ups:** 1) *Default?* Single, from the one side. 2) *When is Both justified?* Many-to-many via a bridge (Q12), special slicer needs.
**Common mistakes:** Setting everything to Both "so it works"; not noticing the arrowhead (single arrow = one direction, double = both).

### Q9 ⭐⭐⭐ 🟡 Why is a star schema recommended for Power BI models?
**Asked at:** commonly asked (no company-specific report found for this exact question); star schema is flagged at Flipkart and Amazon BIE in our notes.
**What the interviewer is checking:** Can you give reasons, not just the name?
**Say this in the interview:** "Because every visual is a query that filters, groups and sums. A star gives dimension tables to filter and group by and fact tables to sum, with short one-to-many paths between them. That is faster, easier to understand and gives fewer wrong totals."
**Explain simply:**
- Fit with how visuals work: dimensions filter and group, facts summarise (Microsoft Learn, star schema article).
- Shorter filter paths and fewer tables than a snowflake; Microsoft says the benefits of a single dimension table generally outweigh a snowflake.
- Clear field list for report authors: columns to slice by live in obvious tables.
- Consistent grain in each fact table avoids double counting (Q20).
- Microsoft also says design is "part science and part art"; break the rules when it makes sense.
**Example:** An HR dashboard with Employee, Department, Calendar and Payroll answers "net pay by department by month" with simple one-to-many joins. A flat export repeats department names thousands of times.
**DAX / Steps (not run here):** Model view > arrange facts in the centre and dimensions around them > keep every relationship one-to-many and single direction.
**Alternative:** A flat denormalised table can work for a tiny single-purpose report; Microsoft's guidance is aimed at models, not one-off charts.
**Version / licensing note:** Guidance page updated 2026-04 (Microsoft Learn); no licence dependency stated.
**Edge cases:** Very large dimensions might justify a snowflake; some models legitimately have several facts.
**Likely follow-ups:** 1) *Does star schema reduce size?* Microsoft says a snowflake is less efficient for storage and performance; I would not give a figure. 2) *What if the source is a flat export?* Shape it in Power Query (Q19).
**Common mistakes:** Memorising "faster" without saying why; joining fact tables directly.

### Q10 ⭐⭐⭐ 🟡 What is the difference between a star schema and a snowflake schema?
**Asked at:** commonly asked (no company-specific report found for this exact question).
**What the interviewer is checking:** Do you know when dimensions are split and what Power BI prefers?
**Say this in the interview:** "In a star, each dimension is one table. In a snowflake, a dimension is split into several linked tables, for example Employee to Department to Division. Power BI generally prefers the star: fewer tables and shorter filter paths."
**Explain simply:**
- Snowflake dimension = normalised set of tables for one business entity (Microsoft Learn star-schema article).
- Downsides in Power BI: more tables loaded, longer filter chains, a busier field list, and a hierarchy cannot span several tables.
- Upside of a single table: you can build one hierarchy (Division > Department). Downside: some repeated text.
- Microsoft: you may mimic the snowflake or merge into one table; generally the single table wins, depending on data volume and usability.
**Example:** Department (3 rows) has a DivID pointing to Division. Merging gives Department with a Division column.
**Sample data:** Table `Division`:

| DivID | Division |
|---|---|
| V1 | Revenue |
| V2 | Support |

Table `Department` (snowflake):

| DeptID | DeptName | DivID |
|---|---|---|
| D1 | Sales | V1 |
| D2 | Finance | V2 |
| D3 | HR | V2 |

**DAX / Steps (not run here):** Power Query Editor > select Department query > Home > Merge Queries > pick DivID in both > Left Outer > OK > expand the new column to tick Division > remove DivID. Equivalent M (not run here, from memory, unverified against Microsoft Learn):
```m
let
    Merged = Table.NestedJoin ( Department, {"DivID"}, Division, {"DivID"}, "DivTable", JoinKind.LeftOuter ),
    Expanded = Table.ExpandTableColumn ( Merged, "DivTable", {"Division"} ),
    Dropped = Table.RemoveColumns ( Expanded, {"DivID"} )
in
    Dropped
```
**Alternative:** Keep the snowflake and add `Division = RELATED ( Division[Division] )` as a calculated column in Department.
**Result:** Reproduced with pandas: one Department table with Division: D1 Sales Revenue; D2 Finance Support; D3 HR Support.
**Pandas check:**
```python
import pandas as pd
division = pd.DataFrame({"DivID": ["V1","V2"], "Division": ["Revenue","Support"]})
dept_sn = pd.DataFrame({"DeptID": ["D1","D2","D3"], "DeptName": ["Sales","Finance","HR"], "DivID": ["V1","V2","V2"]})
star_dept = dept_sn.merge(division, on="DivID", how="left").drop(columns="DivID")
print(star_dept.to_string(index=False))
```
Printed output:
```
DeptID DeptName Division
    D1    Sales  Revenue
    D2  Finance  Support
    D3       HR  Support
```
**Version / licensing note:** Merge Queries is a Power Query feature in Desktop and in dataflows (not verified here, from memory).
**Edge cases:** Merging can multiply rows if the key in Division is not unique; check row counts before and after.
**Likely follow-ups:** 1) *When keep a snowflake?* Large dimension tables or special usability needs. 2) *Where is the merge done?* Power Query, before load.
**Common mistakes:** Forgetting to remove the key after expanding; a left merge that silently drops nothing but duplicates rows.

### Q11 ⭐⭐⭐ 🟡 What is a bi-directional relationship, and why should you avoid it unless needed?
**Asked at:** commonly asked (no company-specific report found for this exact question); bi-directional filtering appears in the 2026 Weekday India list.
**What the interviewer is checking:** Do you know the risks and the safer alternatives?
**Say this in the interview:** "A bi-directional relationship filters both ways. I avoid it by default because it can slow queries, create ambiguous filter paths and confuse report users. If I only need it for one calculation I use CROSSFILTER in that measure, or a visual-level filter on a slicer."
**Explain simply:**
- Microsoft: it can negatively affect performance and "possibly deliver confusing experiences" (Microsoft Learn: Bi-directional relationship guidance).
- Legitimate uses: one-to-one relationships (always bi-directional), many-to-many via a bridge, slicer options "with data", dimension-to-dimension analysis.
- It may be rejected, or allowed with ambiguous paths, in models with several routes between tables.
- Alternative for "with data" slicers: filter the slicer visual by a measure "is not blank".
**Example:** A Department slicer should list only departments with absences. Attendance has an absence only for E2 (Sales). Show Absent Days; filter the slicer by "Absent Days is not blank" and only Sales remains.
**Sample data:** Table `Attendance` (Status by EmpID; absences only for E2):

| EmpID | Status |
|---|---|
| E1 | Present |
| E2 | Absent |
| E3 | Present |
| E4 | Present |

(Two rows per employee in the full test; Employee and Department as in Q3.)
**DAX / Steps (not run here):**
```dax
Absent Days = CALCULATE ( COUNTROWS ( Attendance ), Attendance[Status] = "Absent" )
```
Slicer: Filters pane > Department slicer > Filters on this visual > Absent Days > is not blank.
**Alternative:** `Depts With Absence = CALCULATE ( DISTINCTCOUNT ( Department[DeptName] ), Attendance[Status] = "Absent", CROSSFILTER ( Attendance[EmpID], Employee[EmpID], Both ), CROSSFILTER ( Employee[DeptID], Department[DeptID], Both ) )`, two CROSSFILTERs because the chain has two relationships (CALCULATE and CROSSFILTER function pages, checked).
**Result:** Reproduced with pandas: Absent Days Sales 1, all others blank; a "with data" slicer should list only Sales; `Depts With Absence` = 1.
**Pandas check:**
```python
import pandas as pd
dept = pd.DataFrame({"DeptID": ["D1","D2","D3","D4"], "DeptName": ["Sales","Finance","HR","IT"]})
emp = pd.DataFrame({"EmpID": ["E1","E2","E3","E4"], "DeptID": ["D1","D1","D2","D3"]})
att = pd.DataFrame({"EmpID": ["E1","E1","E2","E2","E3","E3","E4","E4"],
                    "Status": ["Present","Present","Present","Absent","Present","Present","Present","Present"]})
m = att.merge(emp, on="EmpID").merge(dept, on="DeptID")
absent = m[m["Status"] == "Absent"].groupby("DeptName").size()
print("Absent Days by department (others are BLANK):"); print(absent.to_string())
print("Departments a 'with data' slicer should list:", list(absent.index))
print("Depts With Absence:", len(absent))
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
Absent Days by department (others are BLANK):
DeptName
Sales    1
Departments a 'with data' slicer should list: ['Sales']
Depts With Absence: 1
```
**Version / licensing note:** Guidance page updated 2026-01 (Microsoft Learn); applies to Desktop models.
**Edge cases:** Both plus RLS has its own checkbox; it applies bi-directional filtering when RLS is enforced.
**Likely follow-ups:** 1) *Many-to-many?* Q12. 2) *Does Both affect table expansion?* Microsoft says no.
**Common mistakes:** Setting Both on every relationship; blaming slicers when the real fix is a visual filter.

### Q12 ⭐⭐⭐ 🟡 What is a many-to-many relationship in Power BI, and how do you handle it?
**Asked at:** commonly asked (no company-specific report found for this exact question); many-to-many is in the 2026 Weekday India list. A Scribd file tagged "Deloitte" lists many-to-many risks, but the Deloitte attribution is unverified.
**What the interviewer is checking:** Do you know the safe pattern (bridge table) and why totals do not add up?
**Say this in the interview:** "Many-to-many means both sides can repeat values, like employees with several skills and skills shared by several employees. The robust way is a bridge table with one row per employee-skill pair and two one-to-many relationships, with one of them bi-directional. I also explain that totals by skill are not additive."
**Explain simply:**
- **Bridge table:** a table of pairs (EmpID, SkillID) that sits between two dimensions; with only keys it is a "factless fact table".
- Microsoft's steps: one table per entity with an ID, a bridge, one-to-many relationships, one bi-directional relationship, hide the bridge and the ID columns.
- Microsoft does not recommend relating two dimensions directly with a many-to-many cardinality.
- Customer-style totals are non-additive: one person is counted under each of their skills.
**Example:** Skill totals add to 245,000 but real payroll is 195,000, because Asha is under Excel and Power BI.
**Sample data:** Table `EmpSkill` (bridge):

| EmpID | SkillID |
|---|---|
| E1 | S1 |
| E1 | S2 |
| E2 | S1 |
| E3 | S2 |
| E4 | S1 |

Table `Skill`: S1 Excel, S2 Power BI. Payroll (Jan) as Q3.
**DAX / Steps (not run here):**
```dax
Total Net Pay = SUM ( Payroll[NetPay] )
```
Relationships: Skill[SkillID] 1:* EmpSkill[SkillID] (single); Employee[EmpID] 1:* EmpSkill[EmpID] set to Both; Employee[EmpID] 1:* Payroll[EmpID]. Hide EmpSkill.
**Alternative:** A direct many-to-many relationship (Edit relationship > Cardinality > Many to many), acceptable for higher-grain facts such as targets by category, not for two dimensions.
**Result:** Reproduced with pandas (Jan payroll): Excel 135,000; Power BI 110,000; sum of rows 245,000; total with no skill filter 195,000.
**Pandas check:**
```python
import pandas as pd
dept = pd.DataFrame({"DeptID": ["D1","D2","D3","D4"], "DeptName": ["Sales","Finance","HR","IT"]})
emp = pd.DataFrame({"EmpID": ["E1","E2","E3","E4"], "DeptID": ["D1","D1","D2","D3"]})
payroll = pd.DataFrame({"Month": ["Jan"]*4 + ["Feb"]*4, "EmpID": ["E1","E2","E3","E4"]*2,
                        "NetPay": [50000,40000,60000,45000,50000,42000,60000,45000]})
skill = pd.DataFrame({"SkillID": ["S1","S2"], "Skill": ["Excel","Power BI"]})
bridge = pd.DataFrame({"EmpID": ["E1","E1","E2","E3","E4"], "SkillID": ["S1","S2","S1","S2","S1"]})
jan = payroll[payroll["Month"] == "Jan"][["EmpID","NetPay"]]
by_skill = bridge.merge(jan, on="EmpID").merge(skill, on="SkillID").groupby("Skill")["NetPay"].sum()
print(by_skill.to_string())
print("Add up the skill rows:", by_skill.sum(), "| Visual total (no skill filter):", jan["NetPay"].sum())
```
Printed output:
```
Skill
Excel       135000
Power BI    110000
Add up the skill rows: 245000 | Visual total (no skill filter): 195000
```
**Version / licensing note:** Two Microsoft pages differ: "Model relationships in Power BI Desktop" lists many-to-many as a normal cardinality, while "Create and Manage Relationships in Power BI Desktop" ties it to composite models. I have not resolved which is current; check the live page before stating service support.
**Edge cases:** Many-to-many relationships are limited: no blank-row compensation, RELATED fails across them. Fixing grain issues beats forcing m:m.
**Likely follow-ups:** 1) *Why is the total less than the sum?* Q15 style; non-additive. 2) *Bridge vs m:m?* Bridge is the recommended pattern for two dimensions.
**Common mistakes:** Setting both bridge relationships to Both; leaving the bridge visible and unfiltered.

### Q13 ⭐⭐⭐ 🟡 Why do you need a separate date table, and how do you mark it as a date table?
**Asked at:** commonly asked (no company-specific report found for this exact question); date table is in the 2026 Weekday India list.
**What the interviewer is checking:** Do you know why a continuous calendar matters for time analysis?
**Say this in the interview:** "A date table is one row per day with year, month and so on. I need it because time-intelligence functions and clean month visuals work best on a complete, gap-free calendar. I create it with DAX or Power Query, relate it to my fact tables on the date, and mark it as a date table."
**Explain simply:**
- Power BI can auto-create hidden date tables, but analysts often build their own for control of hierarchies (Microsoft Learn: "Set and use date tables in Power BI Desktop").
- Marking validates: unique, no nulls, contiguous dates, same timestamp if Date/Time.
- You must mark it if you use classic time intelligence functions, or relate on non-datetime keys (for example 20241231), among other cases. Calendar-based time intelligence (labelled preview on that page) changes where the option appears.
- Marking removes the built-in auto date tables, so visuals based on them break.
**Example:** Absences on 10 Jan, 20 Jan, 5 Mar. Without a calendar you only see Jan and Mar; with a 2025 calendar you have all 12 months to slice and trend.
**Sample data:** Table `Absences`:

| Date | Absent |
|---|---|
| 2025-01-10 | 1 |
| 2025-01-20 | 1 |
| 2025-03-05 | 1 |

**DAX / Steps (not run here):**
```dax
DimDate = CALENDAR ( DATE ( 2025, 1, 1 ), DATE ( 2025, 12, 31 ) )
Year = YEAR ( DimDate[Date] )
Month No = MONTH ( DimDate[Date] )
Month = FORMAT ( DimDate[Date], "mmm" )
```
1) Modeling > New table (menu name from memory, unverified) and paste the first line; add the other three as New column. 2) Right-click DimDate in Fields > Mark as date table > Mark as date table (or Table tools > Mark as date table); choose the Date column. 3) Relate DimDate[Date] 1:* Absences[Date]. 4) Select Month column > Column tools > Sort by column > Month No (Q21).
**Alternative:** `CALENDARAUTO()` builds the range from dates in the model, covering whole calendar years when the fiscal year end is 12 (CALENDARAUTO function (DAX), checked).
**Result:** Reproduced with pandas: 365 rows, valid; a deleted day makes it invalid; months with data alone Jan, Mar; with the calendar Jan 2, Feb blank, Mar 1, Apr blank (pandas prints 0.0 where DAX shows BLANK, and blank rows hide unless Show items with no data is on).
**Pandas check:**
```python
import pandas as pd
cal = pd.DataFrame({"Date": pd.date_range("2025-01-01", "2025-12-31")})
cal["Year"] = cal["Date"].dt.year; cal["MonthNo"] = cal["Date"].dt.month; cal["Month"] = cal["Date"].dt.strftime("%b")
def valid(d):   # the checks Power BI Desktop makes when you mark a date table
    return d["Date"].is_unique and d["Date"].notna().all() and (d["Date"].diff().dropna() == pd.Timedelta(days=1)).all()
print("Rows:", len(cal), "| unique, no nulls, contiguous:", valid(cal))
print("Still valid after deleting one day:", valid(cal.drop(index=40)))
absences = pd.DataFrame({"Date": pd.to_datetime(["2025-01-10","2025-01-20","2025-03-05"]), "Absent": [1,1,1]})
print("Months that exist in the absence data alone:", absences["Date"].dt.strftime("%b").unique().tolist())
by_month = cal.merge(absences, on="Date", how="left").groupby(["MonthNo","Month"])["Absent"].sum().reset_index()
print(by_month.head(4).to_string(index=False))    # 0 here means BLANK in a DAX visual
```
Printed output:
```
Rows: 365 | unique, no nulls, contiguous: True
Still valid after deleting one day: False
Months that exist in the absence data alone: ['Jan', 'Mar']
 MonthNo Month  Absent
       1   Jan     2.0
       2   Feb     0.0
       3   Mar     1.0
       4   Apr     0.0
```
**Version / licensing note:** From Microsoft Learn: Set and use date tables (updated 2026-10): marking menu paths above; Calendar-based time intelligence is labelled preview on that page and may have changed.
**Edge cases:** Date/Time columns with time parts break relationships (match whole dates). Keep the range covering all data.
**Likely follow-ups:** 1) *Mark vs not mark?* Required for classic time intelligence. 2) *Auto date/time?* Hidden tables; fine for quick work.
**Common mistakes:** Calendar range that stops before the data; several date tables unmarked.

### Q14 ⭐⭐⭐ 🟡 How would you model HR data with employees, departments, attendance and payroll in Power BI?
**Asked at:** commonly asked (no company-specific report found for this exact question); a scenario question built around the topic in general lists.
**What the interviewer is checking:** Can you turn a business description into dimensions, facts and relationships?
**Say this in the interview:** "Employee, Department and Calendar are dimensions; Attendance (one row per employee per day) and Payroll (one row per employee per month) are facts. Department filters Employee, and Employee and Calendar filter both facts. I keep all relationships one-to-many and single direction."
**Explain simply:**
- Two facts at different grain: daily attendance and monthly payroll; do not join them directly (Q20).
- Shared dimensions (Employee, Calendar) let one slicer drive both.
- Payroll's date holds the first day of the month (Microsoft recommends this for facts at a higher grain than day).
- Measures live on the facts; descriptive columns live on the dimensions.
**Example:**
```
Department 1--* Employee 1--* Attendance *--1 Calendar
                   | 1
                   *
                Payroll *--1 Calendar
```
**Sample data:** Tables as Q1 and Q3: Employee (E1-E4 with DeptID), Attendance (Status per day), Payroll (NetPay per month).
**DAX / Steps (not run here):**
```dax
Headcount = COUNTROWS ( Employee )
Absent Days = CALCULATE ( COUNTROWS ( Attendance ), Attendance[Status] = "Absent" )
Total Net Pay = SUM ( Payroll[NetPay] )
```
**Alternative:** One merged fact table at employee-month grain (aggregate attendance in Power Query), simpler but loses daily detail.
**Result:** Reproduced with pandas: Sales headcount 2, absent 1, pay 182,000; Finance 1, blank, 120,000; HR 1, 2, 90,000; IT blank (no employees).
**Pandas check:**
```python
import pandas as pd
dept = pd.DataFrame({"DeptID": ["D1","D2","D3","D4"], "DeptName": ["Sales","Finance","HR","IT"]})
emp = pd.DataFrame({"EmpID": ["E1","E2","E3","E4"], "DeptID": ["D1","D1","D2","D3"]})
payroll = pd.DataFrame({"Month": ["Jan"]*4 + ["Feb"]*4, "EmpID": ["E1","E2","E3","E4"]*2,
                        "NetPay": [50000,40000,60000,45000,50000,42000,60000,45000]})
att = pd.DataFrame({"EmpID": ["E1","E1","E2","E2","E3","E3","E4","E4"],
                    "Status": ["Present","Present","Present","Absent","Present","Present","Absent","Absent"]})
j = emp.merge(dept, on="DeptID")
out = pd.DataFrame({"Headcount": j.groupby("DeptName").size()})
out["Absent Days"] = att[att["Status"] == "Absent"].merge(j, on="EmpID").groupby("DeptName").size()
out["Total Net Pay"] = payroll.merge(j, on="EmpID").groupby("DeptName")["NetPay"].sum()
print(out.reindex(dept["DeptName"]).astype("Int64").to_string())     # <NA> = BLANK
```
Printed output:
```
          Headcount  Absent Days  Total Net Pay
DeptName                                       
Sales             2            1         182000
Finance           1         <NA>         120000
HR                1            2          90000
IT             <NA>         <NA>           <NA>
```
**Version / licensing note:** Design guidance only (Microsoft Learn star-schema and many-to-many guidance pages).
**Edge cases:** Leavers and joiners (a Type 2 slowly changing dimension needs a surrogate key and start/end dates (Q55); it is usually built in the source or ETL, from memory, unverified). Time zones for attendance stamps.
**Likely follow-ups:** 1) *Employee-manager hierarchy?* Parent and Child functions. 2) *Sensitive pay?* Row-level security (not covered here).
**Common mistakes:** One giant table; linking Payroll to Attendance directly.

### Q15 ⭐⭐⭐ 🟡 A visual shows the same total against every row. What do you check in the data model?
**Asked at:** commonly asked (no company-specific report found for this exact question); "same total in every row" is in the 2026 Weekday India list.
**What the interviewer is checking:** A debugging routine for the classic modelling bug.
**Say this in the interview:** "First, is there a relationship between the table giving the rows and the table holding the numbers? Then I check that it is on the right columns with matching values and data types, that it is active, that the filter direction can reach the fact, and that the rows come from the dimension, not from the fact. Last, whether my measure removes filters."
**Explain simply:**
- No relationship: the filter cannot travel, so each row shows the grand total (Microsoft Learn tutorial in "Create and manage relationships").
- Key mismatch (spaces, text vs number, DateTime with time): rows fall under Blank.
- Inactive relationship, wrong direction, or ambiguous path.
- A measure using ALL/REMOVEFILTERS on the grouping column (not covered in the pages fetched).
**Example:** Payroll total 392,000 appears for every department because Payroll is not related to Department.
**Sample data:** Table `Fact` with key "D1 " (trailing space), D2, D3, D1 amounts 100, 200, 300, 50; Department as Q3.
**DAX / Steps (not run here):**
```dax
Total Net Pay = SUM ( Payroll[NetPay] )
```
Checklist: Model view > is there a line? > hover to see columns > Properties/Edit relationship > solid vs dashed > Power Query > Transform > Format > Trim.
**Alternative:** Show the key in a table visual with the fact's key column to spot Blank/unmatched values.
**Result:** Reproduced with pandas: (A) 392,000 on every row; (B) Blank 100, Finance 200, HR 300, Sales 50.
**Pandas check:**
```python
import pandas as pd
dept = pd.DataFrame({"DeptID": ["D1","D2","D3","D4"], "DeptName": ["Sales","Finance","HR","IT"]})
emp = pd.DataFrame({"EmpID": ["E1","E2","E3","E4"], "DeptID": ["D1","D1","D2","D3"]})
payroll = pd.DataFrame({"Month": ["Jan"]*4 + ["Feb"]*4, "EmpID": ["E1","E2","E3","E4"]*2,
                        "NetPay": [50000,40000,60000,45000,50000,42000,60000,45000]})
print("A) No relationship: every department row shows", payroll["NetPay"].sum())
fact = pd.DataFrame({"DeptID": ["D1 ","D2","D3","D1"], "Amount": [100,200,300,50]})   # first key has a trailing space
r = fact.merge(dept, on="DeptID", how="left")
print("B) Key mismatch (trailing space):")
print(r.assign(DeptName=r["DeptName"].fillna("(Blank)")).groupby("DeptName")["Amount"].sum().to_string())
```
Printed output:
```
A) No relationship: every department row shows 392000
B) Key mismatch (trailing space):
DeptName
(Blank)    100
Finance    200
HR         300
Sales       50
```
**Version / licensing note:** Behaviour from Microsoft Learn: "Create and Manage Relationships in Power BI Desktop" and "Model relationships in Power BI Desktop".
**Edge cases:** Totals the same after you add a relationship might mean Both direction ambiguity or a many-to-many issue.
**Likely follow-ups:** 1) *Wrong total vs blank?* Blank suggests key mismatch. 2) *Does it matter which table's column is in the rows?* Yes.
**Common mistakes:** Rebuilding the measure instead of checking the relationship; using a column from the fact table.

### Q16 ⭐⭐⭐ 🟡 How does a filter on a dimension table reach the fact table? Walk me through filter propagation.
**Asked at:** commonly asked (no company-specific report found for this exact question).
**What the interviewer is checking:** Do you understand the mechanics behind every visual?
**Say this in the interview:** "A filter on a dimension follows the relationship from the one side to the many side, step by step. A Department filter selects employees, those employees select payroll rows, and a month filter on the Calendar is applied as an AND at the same fact table."
**Explain simply:**
- Relationships propagate filters along a path, through several tables if needed (Microsoft Learn animation example: Category to Product to Sales).
- When several filters hit one table, they are ANDed.
- Paths are deterministic; DAX like CALCULATE can modify them.
**Example:** Department = Sales selects E1 and E2; they have 4 payroll rows worth 182,000; adding Month = Feb leaves 2 rows worth 92,000.
**Sample data:** Employee and Payroll tables as in Q3.
**DAX / Steps (not run here):**
```dax
Total Net Pay = SUM ( Payroll[NetPay] )
```
Steps: add slicers Department[DeptName] and Calendar[Month].
**Alternative:** Compute step by step with `CALCULATE ( [Total Net Pay], Department[DeptName] = "Sales", DimDate[Month] = "Feb" )` (CALCULATE function (DAX), checked).
**Result:** Reproduced with pandas: 2 employees, 4 payroll rows 182,000, then 2 rows 92,000.
**Pandas check:**
```python
import pandas as pd
dept = pd.DataFrame({"DeptID": ["D1","D2","D3","D4"], "DeptName": ["Sales","Finance","HR","IT"]})
emp = pd.DataFrame({"EmpID": ["E1","E2","E3","E4"], "DeptID": ["D1","D1","D2","D3"]})
payroll = pd.DataFrame({"Month": ["Jan"]*4 + ["Feb"]*4, "EmpID": ["E1","E2","E3","E4"]*2,
                        "NetPay": [50000,40000,60000,45000,50000,42000,60000,45000]})
s1 = emp[emp["DeptID"] == "D1"]                                  # slicer: Department = Sales
print("Step 1  Department=Sales -> Employee rows:", s1["EmpID"].tolist())
s2 = payroll[payroll["EmpID"].isin(s1["EmpID"])]
print("Step 2  -> Payroll rows:", len(s2), "| NetPay sum:", s2["NetPay"].sum())
s3 = s2[s2["Month"] == "Feb"]                                    # slicer: Month = Feb (AND)
print("Step 3  AND Month=Feb -> Payroll rows:", len(s3), "| NetPay sum:", s3["NetPay"].sum())
```
Printed output:
```
Step 1  Department=Sales -> Employee rows: ['E1', 'E2']
Step 2  -> Payroll rows: 4 | NetPay sum: 182000
Step 3  AND Month=Feb -> Payroll rows: 2 | NetPay sum: 92000
```
**Version / licensing note:** Described on Microsoft Learn: Model relationships in Power BI Desktop.
**Edge cases:** Direction Single stops at the fact; ambiguity resolved by priority and weight.
**Likely follow-ups:** 1) *Reverse direction?* Needs Both (Q8). 2) *What if two paths?* Ambiguity error.
**Common mistakes:** Thinking filters flow from fact to dimension.

### Q17 ⭐⭐ 🟢 What is Model view in Power BI Desktop, and how do you create or edit a relationship there?
**Asked at:** commonly asked (no company-specific report found for this exact question); a hands-on skill that a screen-share task could test.
**What the interviewer is checking:** Can you actually build and fix a model, not just describe it?
**Say this in the interview:** "Model view is the diagram of all tables, columns and relationships in Power BI Desktop. I create a relationship by dragging the key column from one table onto the matching column in the other, and edit it by double-clicking the line to change cardinality, direction or active status."
**Explain simply:**
- **Model view:** open it with the Model view icon at the side of the window; hover over a line to see the two columns it uses. An arrow in the middle shows filter direction; double arrows mean Both (Microsoft Learn: "Model view in Power BI Desktop").
- Drag-and-drop in Model view is one way to create a relationship; **Manage relationships > New** is the dialog way (Microsoft Learn: "Create and Manage Relationships in Power BI Desktop").
- Editing: double-click the line, right-click > Properties, or the Properties pane.
- Very large models get crowded; a custom layout helps (a Learn note about a warning above 75 tables is from memory, unverified).
**Example:** Link Department[DeptID] to Employee[DeptID] by dragging DeptID from Department onto DeptID in Employee, check 1 and * show, and rename nothing else.
**DAX / Steps (not run here):**
1. Click the Model view icon at the side of the window.
2. Drag Department[DeptID] onto Employee[DeptID], or Home > Manage relationships > New > choose tables and columns > OK.
3. Double-click the line > check Cardinality (One to many), Cross filter direction (Single), Make this relationship active (ticked) > OK.
4. Delete a wrong line: select it and press Delete (cannot be undone; a prompt asks to confirm).
**Alternative:** Manage relationships > Autodetect (Q18), then review each line. Ribbon tab names (Home or Modeling) vary by build, from memory, unverified.
**Version / licensing note:** From the fetched pages: the guided Edit relationship dialog and the Properties-pane editor are described with preview wording, and the Properties pane needs the "Relationship pane" preview feature enabled (File > Options and settings > Options > Preview features). The page may be out of date for your Desktop build. That Desktop runs only on Windows is from memory, unverified.
**Edge cases:** Ambiguous paths can block a change; a column cannot relate to another column in the same table.
**Likely follow-ups:** 1) *Where else can I manage relationships?* Report, Table, and Model views via ribbons. 2) *Why can't I create it?* Duplicates on both sides (Q30).
**Common mistakes:** Not checking cardinality after dragging; leaving autodetected relationships unchecked.

### Q18 ⭐⭐ 🟢 What does auto-detect relationships do, and should you rely on it?
**Asked at:** commonly asked (no company-specific report found for this exact question).
**What the interviewer is checking:** Healthy scepticism towards automation.
**Say this in the interview:** "Auto-detect looks at column names when tables load and creates relationships when it is confident they match, setting cardinality and direction too. It is a good starting point, but I always open Model view and verify every line, because it can pick the wrong column or the wrong active relationship."
**Explain simply:**
- It compares column names across tables during load; if it cannot decide with high confidence it creates nothing (Microsoft Learn: "Create and Manage Relationships in Power BI Desktop").
- You can run it later: Manage relationships > Autodetect (ribbon tab name from memory, unverified).
- Related options under File > Options and settings > Options > Data Load: import relationships from data sources on first load (on by default), update or delete relationships on refresh (off by default; avoid with RLS that relies on relationships), autodetect new relationships after load.
- It may set a 1:1 relationship because current data has no repeated values (Microsoft's example), or choose the wrong active relationship when two exist.
**Example:** Tables `Employee[EmpID]` and `Attendance[EmpID]` have identical names, so autodetect links them. `Dept` vs `DepartmentCode` have different names, so nothing is created.
**DAX / Steps (not run here):** Modeling > Manage relationships > Autodetect; then Model view > hover each line.
**Alternative:** Switch autodetect off in Data Load options and build every relationship by hand.
**Version / licensing note:** Option names from Microsoft Learn: Create and Manage Relationships in Power BI Desktop (updated 2026-05); labels may differ by build.
**Edge cases:** Equal names but different meaning (ID in two tables); nothing created for mismatched names; wrong cardinality on empty tables.
**Likely follow-ups:** 1) *Who sets cardinality?* Auto, from data; you can change if the one side is unique. 2) *Will refresh change my relationships?* Only if "Update or delete relationships when refreshing data" is on.
**Common mistakes:** Trusting every autodetected line; leaving a many-to-many created by accident.

### Q19 ⭐⭐ 🟢 What is the difference between normalized and denormalized data?
**Asked at:** commonly asked (no company-specific report found for this exact question).
**What the interviewer is checking:** Do you know the trade-off behind splitting tables?
**Say this in the interview:** "Normalised data stores each fact once and uses keys to link tables, so a department name lives in one row. Denormalised data repeats details on every row, like a flat export. Power BI models work best with normalised fact and dimension tables, and I use Power Query to reshape flat exports."
**Explain simply:**
- Normalised: a sales or payroll table keeps only keys (EmpID); descriptions live in dimension tables.
- Denormalised: the fact also stores details such as department and manager (Microsoft Learn star-schema article).
- Exports and extracts are usually denormalised, so shape them into multiple tables.
- Exception: a snowflake dimension may be denormalised into one dimension table.
**Example:** 6 flat rows repeat "Sales" 4 times. Renaming to "Sales & Marketing" edits 4 cells; in a Department table, 1.
**Sample data:** Flat table:

| EmpID | DeptName | Manager |
|---|---|---|
| E1 | Sales | Rao |
| E2 | Sales | Rao |
| E3 | Sales | Rao |
| E4 | Sales | Rao |
| E5 | Finance | Iyer |
| E6 | Finance | Iyer |

**DAX / Steps (not run here):** Power Query Editor > duplicate the query (right-click > Reference) > keep DeptName and Manager > Home > Remove rows > Remove duplicates; add an Index column as DeptID; merge back to the flat query to bring DeptID and remove the text columns.
**Alternative:** Do it upstream, in a SQL view or warehouse (Microsoft recommends a warehouse and ETL for heavy cases).
**Result:** Reproduced with pandas: 4 repeating cells; 4 rows to edit versus 1.
**Pandas check:**
```python
import pandas as pd
flat = pd.DataFrame({"EmpID": ["E1","E2","E3","E4","E5","E6"], "DeptName": ["Sales"]*4 + ["Finance"]*2,
                     "Manager": ["Rao"]*4 + ["Iyer"]*2})
print("Flat table cells repeating 'Sales':", (flat["DeptName"] == "Sales").sum())
flat.loc[flat["DeptName"] == "Sales", "DeptName"] = "Sales & Marketing"
print("Rows to edit to rename in the flat table:", (flat["DeptName"] == "Sales & Marketing").sum(),
      "| rows to edit in a Department table: 1")
```
Printed output:
```
Flat table cells repeating 'Sales': 4
Rows to edit to rename in the flat table: 4 | rows to edit in a Department table: 1
```
**Version / licensing note:** Concept from Microsoft Learn star-schema article; Power Query commands from memory, unverified.
**Edge cases:** Over-normalising hurts (Q10); the same entity may need a unique surrogate key.
**Likely follow-ups:** 1) *Which is faster to query?* Microsoft prefers normalised star models for Power BI. 2) *Where to reshape?* Power Query.
**Common mistakes:** Treating "denormalised" as always bad; normalising until the model is a maze.

### Q20 ⭐⭐ 🟢 What is the grain (granularity) of a fact table, and why does it matter?
**Asked at:** commonly asked (no company-specific report found for this exact question).
**What the interviewer is checking:** Do you know what one row represents and the damage of mixing grains?
**Say this in the interview:** "Grain is what one row of the fact table means, for example one employee per month for payroll or one employee per day for attendance. It matters because totals are only right if every row has the same grain and you never join facts at different grains in a way that repeats rows."
**Explain simply:**
- Dimension keys define the dimensions; the key values define the granularity, e.g. dates all set to the first of the month means month grain (Microsoft Learn star-schema article).
- Facts should load at a consistent grain.
- Joining a monthly table to a daily table repeats the monthly number on each day.
- Targets stored at a higher grain than the dimension need special handling (Microsoft Learn: Many-to-many relationship guidance).
**Example:** Jan salary 50,000 (E1) and 40,000 (E2) sum to 90,000. After joining to 5 daily attendance rows, SUM gives 230,000.
**Sample data:** Table `Payroll` (employee x month): E1 Jan 50000; E2 Jan 40000. Table `Attendance` (employee x day): E1 01, 02, 03 Jan; E2 01, 02 Jan.
**DAX / Steps (not run here):**
```dax
Total Net Pay = SUM ( Payroll[NetPay] )
```
Keep the two facts separate, connected only through the shared Employee and Calendar dimensions.
**Alternative:** Aggregate attendance to month level first: Power Query > Transform > Group By Employee and Month.
**Result:** Reproduced with pandas: correct 90,000; inflated join 230,000.
**Pandas check:**
```python
import pandas as pd
payroll_m = pd.DataFrame({"EmpID": ["E1","E2"], "Month": ["Jan","Jan"], "NetPay": [50000, 40000]})   # grain: employee x month
att_d = pd.DataFrame({"EmpID": ["E1"]*3 + ["E2"]*2, "Date": ["01-Jan","02-Jan","03-Jan","01-Jan","02-Jan"]})  # grain: employee x day
bad = att_d.merge(payroll_m, on="EmpID")          # joining different grains repeats salary on every day row
print("Correct payroll total:", payroll_m["NetPay"].sum())
print("Summed after joining to daily rows:", bad["NetPay"].sum())
```
Printed output:
```
Correct payroll total: 90000
Summed after joining to daily rows: 230000
```
**Version / licensing note:** Design theory only; no licence dependency.
**Edge cases:** Snapshot facts (month-end headcount); factless facts (events with no numbers); documenting the grain in the table description.
**Likely follow-ups:** 1) *How do you check grain?* Count rows vs distinct key combinations. 2) *Monthly targets vs daily sales?* Store the first day of the month and control summarisation with a measure.
**Common mistakes:** Summing a monthly column after a join; mixing daily and monthly rows in one table.

### Q21 ⭐⭐ 🟢 How do you sort the month name column by month number in Power BI?
**Asked at:** commonly asked (no company-specific report found); this question was a gap-fill from standard practice, not seen in a source list.
**What the interviewer is checking:** Do you know that text sorts alphabetically, and that you fix it with a helper number column instead of typing months by hand?
**Say this in the interview:** "Month names sort A to Z, so April comes before January. I keep a Month Number column (1 to 12) in the date table, select the Month Name column in Report view, and use Column tools > Sort by column > Month Number. Both columns must match one-to-one."
**Explain simply:**
- Power BI treats "January" as plain text, so it sorts alphabetically: April, August, December, February.
- A **sort-by column** is a second column that tells Power BI the correct order. Month Number holds 1 to 12.
- Each month name must map to exactly one number. If "Jan" has both 1 and 13, you get a "cannot use this column for sorting" error.
- The setting is saved in the model, so every visual that uses Month Name follows it.
**Example:** An attrition-by-month line chart shows Apr, Aug, Dec, Feb... After sorting by Month Number it reads Jan to Dec.
**Sample data:** Table `Date` (one row per month shown)

| MonthName | MonthNo |
|---|---|
| January | 1 |
| February | 2 |
| March | 3 |

**DAX / Steps (not run here):**
1. Make sure the date table has `MonthNo` as a Whole number (also load it in Power Query: Transform > Data Type > Whole Number).
2. Switch to **Report view** (the Column tools tab is not available in Model or Table view).
3. In the Data pane click `MonthName`; ribbon **Column tools > Sort by column > MonthNo**.
4. Optionally hide `MonthNo` (see Q22).
**Alternative:** Build a calculated column `Month Sort = MONTH('Date'[Date])` (from memory, not fetched), or in the Service sort the visual through a tooltip field and **More options > Sort axis** as the Learn page describes.
**Result:** reproduced with pandas: alphabetical order gives February, January, March; sorted by number gives January, February, March. A valid pair has at most 1 number per name; a bad pair has 2.
**Pandas check:**
```python
import pandas as pd
d = pd.DataFrame({"MonthName":["January","February","March","January","February"],"MonthNo":[1,2,3,1,2]})
print(sorted(d.MonthName.unique()))                              # alphabetical (default text sort)
print(d.drop_duplicates().sort_values("MonthNo").MonthName.tolist())   # sorted by MonthNo
print(d.groupby("MonthName").MonthNo.nunique().max())            # 1 -> valid sort-by pair
bad = pd.concat([d, pd.DataFrame({"MonthName":["January"],"MonthNo":[13]})])
print(bad.groupby("MonthName").MonthNo.nunique().max())          # 2 -> invalid pair
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
['February', 'January', 'March']
['January', 'February', 'March']
1
2
```
**Version / licensing note:** Microsoft Learn: Sort One Column by Another Column in Power BI says this applies to Desktop and the Service; the Column tools path is Desktop Report view only, and the Service uses the tooltip workaround. Free vs Pro not stated. That page is not in this part's fetched-pages list, so treat these platform details as from memory, unverified.
**Edge cases:** Month numbers stored as text sort wrongly ("10" before "2"). For fiscal years, use a fiscal month number.
**Likely follow-ups:** 1) *Can two month names share one number?* Avoid it: each name should map to one number, and I would keep the sort number unique per name (from memory, unverified whether Power BI allows shared numbers). 2) *Should year be included?* Month Name alone merges all years, so also filter or group by Year.
**Common mistakes:** Working in Model view and not finding Sort by column; sorting by a column at a different grain (Day Number); forgetting to hide the helper number.

### Q22 ⭐⭐ 🟢 Why should you hide foreign key and helper columns from Report view?
**Asked at:** commonly asked (no company-specific report found); this question was a gap-fill from standard practice.
**What the interviewer is checking:** Do you think about the report author who uses your model, not just the model itself?
**Say this in the interview:** "Keys and helper columns like EmployeeKey or Month Number are plumbing. I hide them so authors only see fields meant for slicers and axes, and use measures for numbers. Hiding does not break relationships or DAX."
**Explain simply:**
- A **foreign key** is the column in the fact table that points to a dimension (for example `DeptID` in an Employee table). It is useful for relationships but not useful on a chart.
- Visible keys tempt people to put an ID on an axis or sum it by accident.
- Microsoft's optimization guide lists hiding relationship ID columns, and hiding columns that already have a measure so authors use the measure.
- Hidden fields can still be used in relationships, DAX and sorting. They are hidden from the field list, not deleted, and a consumer can un-hide them.
**Example:** An HR model has `Unit Price`-style columns: `Salary` should not be summed across months blindly, so hide `Salary` and ship a measure `Avg Salary`.
**DAX / Steps (not run here):** In **Model view** (or the Data pane), right-click the column > **Hide in report view** (wording from memory, unverified). Do the same for the key columns and for `MonthNo`.
**Alternative:** Use **Properties** pane in Model view > **Is hidden** toggle (from memory, unverified), or hide a whole table such as a bridge table (Q28).
**Version / licensing note:** Behaviour is described on Microsoft Learn: Optimization guide for Power BI and Many-to-many relationship guidance. Menu wording is from memory, unverified, and neither page is in this part's fetched-pages list. Hiding is guidance, not security (from memory, unverified).
**Edge cases:** Hidden is not secure; use row-level security for protection. Do not hide a key you still want in a drill-through. If a visual used a column you later hide, the visual keeps working.
**Likely follow-ups:** 1) *Does hiding reduce model size?* No; removing the column does (Q38). 2) *Which side's key should stay visible, if any?* The "one" side.
**Common mistakes:** Deleting keys instead of hiding them (breaks relationships); leaving a summable ID visible so someone sums EmployeeID.

### Q23 ⭐⭐ 🟢 In Model view, what do the 1, the asterisk, the arrow, and a solid or dotted line on a relationship tell you?
**Asked at:** commonly asked (no company-specific report found); gap-fill, standard in live screen-share tasks.
**What the interviewer is checking:** Can you read a model diagram quickly and spot a wrong relationship?
**Say this in the interview:** "The 1 and the asterisk give the cardinality: 1 is the unique 'one' side, * is the 'many' side. The arrowhead shows which way filters flow: one arrow is single direction, two arrows is both. A solid line is an active relationship, a dashed line is inactive."
**Explain simply:**
- **1 and \*:** the "one" side holds unique values (a department list); the "many" side can repeat (employees). `*` on both ends means many-to-many.
- **Arrowhead:** filters travel in the arrow's direction. A normal one-to-many shows one arrow pointing from the dimension into the fact table. Two arrowheads means bi-directional.
- **Solid vs dashed:** Learn says a solid line is active and a dashed line is inactive. Only one active path can exist between two tables.
- **Parentheses ( ) after the indicators** mean a *limited* relationship (many-to-many or across data sources).
**Example:** `Department` 1 ---> * `Employee`: filtering Department = "HR" filters the Employee rows to HR staff.
**DAX / Steps (not run here):** Model view > hover or click the relationship line to highlight the two columns; double-click it to open **Edit relationship** and see Cardinality and Cross-filter direction.
**Alternative:** The Properties pane for the selected relationship shows the same settings in text.
**Version / licensing note:** All symbols are from Microsoft Learn: Model relationships in Power BI Desktop (tips on cardinality indicators, arrowheads, solid vs dashed line, limited relationship parentheses). Desktop only; no licence needed.
**Edge cases:** A one-to-one relationship shows 1 and 1 with double arrows. The arrow shows the filter direction, not "which table is bigger".
**Likely follow-ups:** 1) *What if the arrow points the wrong way?* Check cardinality; filters should run from dimension to fact. 2) *Why dashed?* Another path is already active (Q24).
**Common mistakes:** Reading the arrow as the lookup direction of a VLOOKUP; assuming a dashed line is broken.

### Q24 ⭐⭐ 🟡 What is the difference between an active and an inactive relationship?
**Asked at:** role-playing and USERELATIONSHIP topics appear in a 2026 India-oriented Power BI list (Weekday, fetched as a model summary of the page, not verbatim); no company-specific report found.
**What the interviewer is checking:** Do you know there can be only one active path between two tables, and how to use the others?
**Say this in the interview:** "An active relationship filters automatically. An inactive one sits idle until a measure switches it on with USERELATIONSHIP. Between two tables only one relationship can be active."
**Explain simply:**
- **Active (solid line):** a slicer on the dimension flows into the fact table automatically.
- **Inactive (dashed line):** exists, but filters do not flow unless a calculation activates it.
- Why only one active? Filter paths must be deterministic: Power BI must know exactly which way to filter.
- Learn recommends active relationships whenever possible; inactive ones suit cases where visuals never need two roles at once.
**Example:** `Sales` has `OrderDate` and `ShipDate` both linked to `Date`. Order Date is active (most reports use it); Ship Date is inactive.
**DAX / Steps (not run here):**
```dax
Sales by Ship Date =
CALCULATE ( SUM ( Sales[Amount] ), USERELATIONSHIP ( Sales[ShipDate], 'Date'[Date] ) )
```
Make a relationship inactive: Model view > double-click the line > untick **Make this relationship active**.
**Alternative:** Duplicate the Date table so each role has its own active relationship (Q27).
**Result:** concept question; the measure's numbers on sample data (reproduced with pandas, not run in a DAX engine) are in Q26.
**Version / licensing note:** Microsoft Learn: USERELATIONSHIP function (DAX), Active vs inactive relationship guidance. Learn also says row-level security filters never propagate through inactive relationships, even when USERELATIONSHIP is used.
**Edge cases:** Inactive relationships still cause a BLANK member to appear on the dimension if the many side has blanks (table expansion). USERELATIONSHIP errors if RLS is defined on the table involved.
**Likely follow-ups:** 1) *Can two slicers use different roles at once?* Not with one table; duplicate it. 2) *Does USERELATIONSHIP work in a visual filter?* It only works inside CALCULATE-type functions.
**Common mistakes:** Expecting two relationships between the same tables to be active (Power BI creates the second one inactive); writing USERELATIONSHIP outside CALCULATE.

### Q25 ⭐⭐ 🟡 What is a role-playing dimension? Give an example with Order Date and Ship Date, or Hire Date and Exit Date.
**Asked at:** role-playing dimensions appear in a 2026 India-oriented Power BI list (Weekday, fetched as a model summary); no company-specific report found.
**What the interviewer is checking:** Do you understand that one dimension can play several roles for one fact table?
**Say this in the interview:** "A role-playing dimension is one dimension table used in more than one way by the same fact table, like a Date table used as Hire Date and as Exit Date. The data is the same, the role is different."
**Explain simply:**
- One date table, many date columns in the fact: Order Date, Ship Date, Delivery Date.
- In a data warehouse you join the same table several times. In Power BI only one relationship can be active, so extra roles are inactive or the table is copied (Q27).
- Learn's examples: order, ship and delivery dates; departure and arrival airports.
**Example:** HR headcount. `Employee` has `HireDate` and `ExitDate`. Hires per month use Hire role; exits per month use Exit role.
**Sample data:** Table `Employee`

| EmpID | HireDate | ExitDate |
|---|---|---|
| E1 | 2025-01-10 | 2025-03-05 |
| E2 | 2025-01-25 | (blank) |
| E3 | 2025-02-14 | 2025-02-28 |
| E4 | 2025-03-02 | (blank) |

**DAX / Steps (not run here):**
```dax
Hires = COUNTROWS ( Employee )
Exits = CALCULATE ( COUNTROWS ( Employee ), USERELATIONSHIP ( Employee[ExitDate], 'Date'[Date] ) )
```
Hire Date is the active relationship; Exit Date is inactive.
**Alternative:** Create `Exit Date` as a copy of the Date table (calculated table `Exit Date = 'Date'`, as in Learn's refactor example) with its own active relationship.
**Result:** reproduced with pandas: Hires by month Jan 2, Feb 1, Mar 1; Exits Feb 1, Mar 1; the two unfilled exits go to a blank member.
**Pandas check:**
```python
import pandas as pd
e = pd.DataFrame({"EmpID":["E1","E2","E3","E4"],"HireDate":pd.to_datetime(["2025-01-10","2025-01-25","2025-02-14","2025-03-02"]),"ExitDate":pd.to_datetime(["2025-03-05",None,"2025-02-28",None])})
print("Hires :", e.groupby(e.HireDate.dt.strftime("%Y-%m")).size().to_dict())
print("Exits :", e.groupby(e.ExitDate.dt.strftime("%Y-%m")).size().to_dict())
print("Exit rows with no date (go to the blank member):", int(e.ExitDate.isna().sum()))
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
Hires : {'2025-01': 2, '2025-02': 1, '2025-03': 1}
Exits : {'2025-02': 1, '2025-03': 1}
Exit rows with no date (go to the blank member): 2
```
**Version / licensing note:** Microsoft Learn: Understand star schema and importance for Power BI; Active vs inactive relationship guidance.
**Edge cases:** Exit date is blank for current staff, which creates a BLANK date member. Hire and exit in the same month need both roles shown at once, which favours copies.
**Likely follow-ups:** 1) *One slicer for both roles?* Inactive design: slicer filters only the active role. 2) *Is it a different table in the source?* No, same source.
**Common mistakes:** Joining the same date column twice and expecting both to be active; calling two different dimensions "role-playing".

### Q26 ⭐⭐ 🟡 Write a DAX measure that calculates sales by Ship Date when the active relationship is on Order Date.
**Asked at:** USERELATIONSHIP appears in a 2026 India-oriented Power BI list (Weekday, fetched as a model summary); no company-specific report found.
**What the interviewer is checking:** Can you write USERELATIONSHIP inside CALCULATE correctly?
**Say this in the interview:** "I create the Ship Date relationship from Sales to Date as inactive, then write CALCULATE of the sum of Amount with USERELATIONSHIP on Ship Date. Inside that measure the Ship Date relationship takes over from Order Date."
**Explain simply:**
- **CALCULATE** runs a calculation after changing the filters. USERELATIONSHIP is one of its filter modifiers.
- USERELATIONSHIP takes two columns: the many-side column (Sales[ShipDate]) and the Date column. Learn says reversed order is swapped for you.
- Inside the measure the Ship Date relationship is used and the Order Date one is switched off for that calculation.
- A slicer on Month then means "shipped in that month".
**Example:** Order O2 is placed 20 January and shipped 2 February. By order date it counts in January; by ship date it counts in February.
**Sample data:** Table `Sales` (Date table has one row per day; Order Date relationship active, Ship Date inactive)

| OrderID | OrderDate | ShipDate | Amount |
|---|---|---|---|
| O1 | 2025-01-05 | 2025-01-08 | 1000 |
| O2 | 2025-01-20 | 2025-02-02 | 2000 |
| O3 | 2025-02-10 | 2025-02-12 | 1500 |
| O4 | 2025-02-25 | 2025-03-03 | 500 |
| O5 | 2025-03-15 | (blank) | 800 |

**DAX / Steps (not run here):**
```dax
Sales Amount = SUM ( Sales[Amount] )

Sales by Ship Date =
CALCULATE (
    [Sales Amount],
    USERELATIONSHIP ( Sales[ShipDate], 'Date'[Date] )
)
```
**Alternative:** A duplicated `Ship Date` table with its own active relationship, then plain `[Sales Amount]` filtered by it (Q27).
**Result:** reproduced with pandas (not from a DAX engine). By month: order date Jan 3000, Feb 2000, Mar 800; ship date Jan 1000, Feb 3500, Mar 500, plus 800 against a blank member (unshipped). Both columns total 5800.
**Pandas check:**
```python
import pandas as pd
sales = pd.DataFrame({"OrderID":["O1","O2","O3","O4","O5"],
  "OrderDate":pd.to_datetime(["2025-01-05","2025-01-20","2025-02-10","2025-02-25","2025-03-15"]),
  "ShipDate":pd.to_datetime(["2025-01-08","2025-02-02","2025-02-12","2025-03-03",None]),
  "Amount":[1000,2000,1500,500,800]})
by_order = sales.groupby(sales.OrderDate.dt.strftime("%Y-%m").fillna("(Blank)")).Amount.sum()
by_ship = sales.groupby(sales.ShipDate.dt.strftime("%Y-%m").fillna("(Blank)")).Amount.sum()
out = pd.DataFrame({"By Order Date": by_order, "By Ship Date": by_ship}).fillna(0).astype(int)
out.loc["Total"] = out.sum()
print(out.to_string())
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
         By Order Date  By Ship Date
(Blank)              0           800
2025-01           3000          1000
2025-02           2000          3500
2025-03            800           500
Total             5800          5800
```
**Version / licensing note:** Microsoft Learn: USERELATIONSHIP function (DAX) (its own example is this exact pattern); Active vs inactive relationship guidance (says a BLANK member can appear when ship date is blank). Not usable when RLS is defined on the table.
**Edge cases:** The blank member row (unshipped orders) depends on a blank in the many-side column; the Learn guidance notes it appears via table expansion. A Date table that stops before the last ship date drops sales.
**Likely follow-ups:** 1) *Which argument order?* Many-side first, but swapped if reversed. 2) *Need the relationship inactive?* It works whether active or not; but the Order Date one must exist.
**Common mistakes:** Writing it as a calculated column; forgetting the inactive relationship must already exist; using FILTER on dates and ignoring the relationship.

### Q27 ⭐⭐ 🟡 For a role-playing date dimension, when would you use inactive relationships and when would you duplicate the date table?
**Asked at:** role-playing dimensions appear in a 2026 India-oriented Power BI list (Weekday, fetched as a model summary); no company-specific report found.
**What the interviewer is checking:** Can you weigh the two designs and justify your choice?
**Say this in the interview:** "If one date role is used almost everywhere and another in only a few measures, I keep one Date table and an inactive relationship with USERELATIONSHIP. If users need both roles on screen at once, or I use row-level security, I duplicate the date table so every relationship is active."
**Explain simply:**
- **Inactive + USERELATIONSHIP:** less model size, but you write one extra measure per role per metric and cannot slice both roles together.
- **Duplicate table (one per role):** simple for report authors, allows both filters at once; costs a little size, which is rarely an issue since date tables are small.
- Learn recommends active relationships whenever possible and says to duplicate for role-playing tables. Inactive works when no visual needs different roles together and USERELATIONSHIP activates the right one.
- Name columns by role (Ship Year, Ship Month) so visuals have clear titles.
**Example:** HR dashboard: Join Date drives 95% of reports; Exit Date appears in one attrition measure. An inactive Exit relationship is fine. If HR wants a matrix of Join Month by Exit Month, duplicate the table.
**DAX / Steps (not run here):**
```dax
Ship Date = 'Date'
```
(calculated table copy, as in Learn's refactor steps). Then Model view > drag `Ship Date[Date]` to `Sales[ShipDate]` (active).
**Alternative:** In Power Query, create the copy with a referencing query (right-click query > Reference); use this for DirectQuery tables.
**Result:** Design decision, no calculation. Pandas reproduction of the blank-member risk is in Q26.
**Version / licensing note:** Microsoft Learn: Active vs inactive relationship guidance (updated 2026-01 per page header); Understand star schema and importance for Power BI. The Learn guidance also says RLS filters never propagate through inactive relationships.
**Edge cases:** With inactive design, a Ship Date slicer would need a disconnected table. Both designs create a blank member when the many side has blanks.
**Likely follow-ups:** 1) *Does the copy refresh slower?* A little; calculated table is small. 2) *Mark the copy as date table?* Only one table can be the model's main date table; check Q13.
**Common mistakes:** Duplicating but keeping identical column names ("Year" everywhere); using inactive relationships with RLS.

### Q28 ⭐⭐ 🟡 What is a bridge table, and when do you need one?
**Asked at:** many-to-many handling is a common topic in prep lists; one Scribd set tags many-to-many risks as Deloitte (attribution unverified). No confirmed company-specific report.
**What the interviewer is checking:** Do you know how to model a true many-to-many between two dimensions without ambiguous results?
**Say this in the interview:** "A bridge table sits between two dimensions that are many-to-many, for example employees and skills. It has one row per pair, and I connect it with two one-to-many relationships instead of a direct many-to-many."
**Explain simply:**
- **Many-to-many:** one employee has several skills, and one skill belongs to several employees.
- The bridge holds only keys (EmpID, SkillID). When it holds only IDs it is called a factless fact table.
- Learn's guidance: add each entity as a table with an ID, add the bridge, create one-to-many relationships, set one relationship bi-directional so filters reach the fact table, and hide the bridge.
- Totals become non-additive: one training hour can count under two skills.
**Example:** Training hours per employee, reported by skill. Asha (10 hours) knows SQL and Power BI, so her hours appear under both.
**Sample data:** `Employee`, `Skill`, `SkillBridge`, `Training` (fact)

| SkillBridge: EmpID | SkillID |
|---|---|
| 1 | S1 |
| 1 | S2 |
| 2 | S1 |
| 3 | S2 |

| Training: EmpID | Hours |
|---|---|
| 1 | 10 |
| 2 | 8 |
| 3 | 6 |

Skill S1 = SQL, S2 = Power BI.
**DAX / Steps (not run here):**
1. Relationships: `Skill[SkillID]` 1 to * `SkillBridge[SkillID]`; `Employee[EmpID]` 1 to * `SkillBridge[EmpID]` set to **Both**; `Employee[EmpID]` 1 to * `Training[EmpID]`.
2. Hide `SkillBridge`. Measure: `Training Hours = SUM ( Training[Hours] )`.
**Alternative:** A direct many-to-many relationship; Learn says it does not recommend relating many-to-many dimensions directly.
**Result:** reproduced with pandas: SQL 18, Power BI 16; the grand total of all employees is 24, but the skill rows add to 34.
**Pandas check:**
```python
import pandas as pd
skill = pd.DataFrame({"SkillID":["S1","S2"],"Skill":["SQL","Power BI"]})
bridge = pd.DataFrame({"EmpID":[1,1,2,3],"SkillID":["S1","S2","S1","S2"]})
ts = pd.DataFrame({"EmpID":[1,2,3],"TrainingHours":[10,8,6]})
j = bridge.merge(skill,on="SkillID").merge(ts,on="EmpID")
by = j.groupby("Skill").TrainingHours.sum()
print(by.to_string())
print("All employees:", ts.TrainingHours.sum(), "| skill rows add up to:", by.sum())
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
Skill
Power BI    16
SQL         18
All employees: 24 | skill rows add up to: 34
```
**Version / licensing note:** Microsoft Learn: Many-to-many relationship guidance (updated 2026-01); Understand star schema (bridging table = factless fact). Whether the Service differs was not verified on a fetched page.
**Edge cases:** Duplicate pairs in the bridge double-count. Employees with no skill vanish under skill slicers. Only one bi-directional relationship; more creates ambiguity.
**Likely follow-ups:** 1) *Why not just many-to-many cardinality?* Dimensions should have an ID on the "one" side; limited relationships behave differently. 2) *Why do totals look wrong?* Non-additive, explain it to users.
**Common mistakes:** Bi-directional on both sides; leaving the bridge visible; summing across the many-to-many and reporting the total.

### Q29 ⭐⭐ 🟡 Blank rows appear in a visual after you add a relationship. What is the likely cause and how do you fix it?
**Asked at:** commonly asked (no company-specific report found); blank row troubleshooting is a standard model-debug question.
**What the interviewer is checking:** Do you know the blank row means the many side has a key that the one side does not?
**Say this in the interview:** "A BLANK row in a dimension visual usually means some fact rows have a key with no matching dimension row. Power BI shows them as an unknown member so nothing disappears. I find the orphan keys and fix the data, or add an 'Unknown' row."
**Explain simply:**
- Learn calls it a **blank virtual row**: when a "many" side value has no match on the "one" side, a blank row is added to the "one" table. These are unknown members (a referential-integrity violation).
- Common triggers: new department code in the fact not in the Dept list; leading space ("D1 "); different case or data type; blank keys.
- Fix: clean in Power Query, add the missing member to the dimension, or add an "Unknown" row and map missing keys to it.
- Never hide the blank to make the report look clean; the numbers under it are real.
**Example:** Employee D9 works in a department missing from the Department table. The salary of 30 appears under (Blank).
**Sample data:** Table `Department` and `Employee`

| Dept: DeptID | Dept |
|---|---|
| D1 | Sales |
| D2 | HR |

| Emp: EmpID | DeptID | Salary |
|---|---|---|
| 1 | D1 | 50 |
| 2 | D2 | 40 |
| 3 | D1 | 60 |
| 4 | D9 | 30 |

**DAX / Steps (not run here):** Power Query: Home > Merge Queries (Employee with Department, join kind **Left Anti**) to list orphan keys, then fix or add them. Visual check: put Department[Dept] and `Total Salary = SUM ( Employee[Salary] )` in a table.
**Alternative:** Add `D9, Unknown` to the Department source (or a Power Query step) so the blank becomes a named row.
**Result:** reproduced with pandas: Sales 110, HR 40, (Blank) 30; the unmatched key is D9.
**Pandas check:**
```python
import pandas as pd
dept = pd.DataFrame({"DeptID":["D1","D2"],"Dept":["Sales","HR"]})
emp = pd.DataFrame({"EmpID":[1,2,3,4],"DeptID":["D1","D2","D1","D9"],"Salary":[50,40,60,30]})
j = emp.merge(dept,on="DeptID",how="left"); j["Dept"] = j.Dept.fillna("(Blank)")
print(j.groupby("Dept").Salary.sum().to_string())
print("Orphan keys:", sorted(set(emp.DeptID)-set(dept.DeptID)))
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
Dept
(Blank)     30
HR          40
Sales      110
Orphan keys: ['D9']
```
**Version / licensing note:** Microsoft Learn: Model relationships in Power BI Desktop (regular relationships, table expansion, blank virtual rows; blank rows apply only to regular, not limited, relationships). Desktop and Service share the engine; not separately verified.
**Edge cases:** A many-to-many (limited) relationship uses inner-join semantics, so orphans silently disappear instead of showing a blank. Blank rows also come from blank ship dates (Q26).
**Likely follow-ups:** 1) *Why not delete the rows?* The totals would drop; investigate first. 2) *Assume referential integrity?* It makes DirectQuery faster but hides orphans; use only if data is clean.
**Common mistakes:** Filtering out blanks in the visual; mismatched data types or trailing spaces in keys.

### Q30 ⭐⭐ 🟡 Power BI will not let you create a one-to-many relationship because the column contains duplicate values. What do you do?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you diagnose why a "one" side column is not unique and fix the cause rather than force many-to-many?
**Say this in the interview:** "The 'one' side must be unique. I find the duplicates, check whether they are true duplicates, spaces or case differences, or real different values, and clean or deduplicate the dimension. Only if the business truly needs it do I use many-to-many or a bridge table."
**Explain simply:**
- One-to-many means the "one" column has no repeats. Desktop detects cardinality from the data and may offer many-to-many if duplicates exist.
- Learn also warns: if a refresh loads duplicates into a "one" side column, the whole refresh fails.
- Check duplicates in Power Query: Home > Keep Rows > Keep Duplicates (from memory, unverified), or column quality tools.
- Learn's data-types page: leading spaces are not trimmed by the engine and can cause "duplicate" or invalid cardinality errors; use Transform > Format > Trim.
- If duplicates are real (two different names for one ID), decide the right value with the business.
**Example:** Department table has `D2, HR` and `D2, "HR "` (trailing space). After trimming, they collapse to one row.
**Sample data:** Table `Department`

| DeptID | Dept |
|---|---|
| D1 | Sales |
| D2 | HR |
| D2 | "HR " |
| D3 | Ops |

**DAX / Steps (not run here):** Power Query (M):
```m
let
    Source = Department,
    Trimmed = Table.TransformColumns(Source, {{"Dept", Text.Trim, type text}}),
    Deduped = Table.Distinct(Trimmed)
in
    Deduped
```
Then Home > Close & Apply and recreate the relationship.
**Alternative:** Build a clean dimension from the fact: copy the key column, Remove Duplicates, and relate to it; or a many-to-many via bridge (Q28).
**Result:** reproduced with pandas: `DeptID` is not unique (False); after trim and dedupe it has 3 unique rows (True). With two conflicting names for D2 two rows remain, so it needs a business decision.
**Pandas check:**
```python
import pandas as pd
dept = pd.DataFrame({"DeptID":["D1","D2","D2","D3"],"Dept":["Sales","HR","HR ","Ops"]})
print("DeptID unique before:", dept.DeptID.is_unique)
fixed = dept.assign(Dept=dept.Dept.str.strip()).drop_duplicates()
print("DeptID unique after trim + dedupe:", fixed.DeptID.is_unique, "| rows:", len(fixed))
conflict = pd.DataFrame({"DeptID":["D2","D2"],"Dept":["HR","People"]}).drop_duplicates()
print("Conflicting names for D2 leave", len(conflict), "rows -> business decision")
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
DeptID unique before: False
DeptID unique after trim + dedupe: True | rows: 3
Conflicting names for D2 leave 2 rows -> business decision
```
**Version / licensing note:** Microsoft Learn: Model relationships in Power BI Desktop; Data types in Power BI (trim guidance). The Power Query M functions (Table.TransformColumns, Table.Distinct, Text.Trim) were not fetched here; `Text.Trim` is mentioned on the Data types page; others from memory, unverified.
**Edge cases:** Case differences: the engine is case-insensitive but Power Query is case-sensitive, so "hr" and "HR" are different in Power Query and the same in the model. Blank keys also count as duplicates. The case-sensitivity point is from memory, unverified.
**Likely follow-ups:** 1) *Can I just pick many-to-many?* Possible but limited relationship; avoid for dimensions. 2) *What about an index column?* Add a surrogate key if no unique column exists.
**Common mistakes:** Forcing many-to-many to get past the error; deduplicating without checking which row is right.

### Q31 ⭐⭐ 🟡 What do the RELATED and RELATEDTABLE functions do, and which side of the relationship does each use?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know direction: RELATED goes many to one, RELATEDTABLE goes one to many?
**Say this in the interview:** "RELATED, from the many side, fetches one value from the one side, like pulling Department Name into each employee row. RELATEDTABLE, from the one side, returns all matching rows from the many side, like all employees of a department, and I wrap it in COUNTROWS or SUMX."
**Explain simply:**
- **RELATED(column):** follows an existing many-to-one relationship and returns a single value. It needs row context (calculated column or inside an iterator such as SUMX).
- **RELATEDTABLE(table):** returns a table of the related rows. Learn calls it a shortcut for CALCULATETABLE with no filter.
- **Row context** means "the current row being calculated".
- RELATED cannot fetch a column across a limited relationship.
**Example:** Add the department Region to each employee, and total salary to each department.
**Sample data:** Tables `Dept` and `Emp`

| Dept: DeptID | Dept | Region |
|---|---|---|
| D1 | Sales | South |
| D2 | HR | North |

| Emp: EmpID | DeptID | Salary |
|---|---|---|
| 1 | D1 | 50 |
| 2 | D2 | 40 |
| 3 | D1 | 60 |

**DAX / Steps (not run here):**
```dax
-- calculated column in Emp (many side)
Region = RELATED ( Dept[Region] )

-- calculated columns in Dept (one side)
Total Salary = SUMX ( RELATEDTABLE ( Emp ), Emp[Salary] )
Headcount = COUNTROWS ( RELATEDTABLE ( Emp ) )
```
**Alternative:** For reports, a measure `SUM ( Emp[Salary] )` with the Dept slicer needs neither function; relationships already filter.
**Result:** reproduced with pandas: Emp rows get Region South, North, South. Dept totals: Sales 110 (2 staff), HR 40 (1 staff).
**Pandas check:**
```python
import pandas as pd
dept = pd.DataFrame({"DeptID":["D1","D2"],"Dept":["Sales","HR"],"Region":["South","North"]})
emp = pd.DataFrame({"EmpID":[1,2,3],"DeptID":["D1","D2","D1"],"Salary":[50,40,60]})
emp["Region"] = emp.DeptID.map(dept.set_index("DeptID").Region)                 # RELATED
dept["TotalSalary"] = dept.DeptID.map(emp.groupby("DeptID").Salary.sum())       # SUMX(RELATEDTABLE)
dept["Headcount"] = dept.DeptID.map(emp.groupby("DeptID").size())               # COUNTROWS(RELATEDTABLE)
print(emp.to_string(index=False)); print(dept.to_string(index=False))
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
 EmpID DeptID  Salary Region
     1     D1      50  South
     2     D2      40  North
     3     D1      60  South
DeptID  Dept Region  TotalSalary  Headcount
    D1 Sales  South          110          2
    D2    HR  North           40          1
```
**Version / licensing note:** Microsoft Learn: RELATED function (DAX), RELATEDTABLE function (DAX). RELATEDTABLE is not supported in calculated columns or RLS in DirectQuery mode per its page.
**Edge cases:** RELATED looks at all values regardless of filters. With no matching row it returns blank. RELATED does not work without a relationship.
**Likely follow-ups:** 1) *RELATED in a measure?* Only inside an iterator (SUMX) that provides row context. 2) *Many-to-many?* Use limited relationships carefully; RELATED fails.
**Common mistakes:** Using RELATED from the one side (it returns the wrong thing or errors); using a calculated column where a measure is better.

### Q32 ⭐⭐ 🟡 You receive one flat Excel export with orders, customers and products in the same sheet. How would you convert it into a star schema?
**Asked at:** commonly asked (no company-specific report found); gap-fill from standard practice. Data modelling appears in some GCC and product-company reports (Amazon BIE and Flipkart mention star schema in research/interview_processes.md), without question wording.
**What the interviewer is checking:** Can you split one wide table into a fact table and dimensions, with keys?
**Say this in the interview:** "I load the sheet, then in Power Query I reference it to make a Customer table and a Product table with duplicates removed and an index key, merge those keys back into the order rows, and keep only keys and numbers in the fact table. Then I relate them one-to-many."
**Explain simply:**
- A flat export is **denormalized**: customer name and product name repeat on every order row.
- **Dimension** = one row per customer/product; **fact** = one row per order line with keys and numbers.
- If the data has no unique ID, create one with an index column (Learn: surrogate keys, Power Query index column), then merge it into the fact.
- Learn: export files are usually denormalized; use Power Query to reshape into normalized tables.
**Example:** 4 order lines, customers Asha (Hyderabad) and Ravi (Pune), products Laptop and Mouse.
**Sample data:** Flat export

| OrderID | OrderDate | CustomerName | City | ProductName | Category | Qty | Amount |
|---|---|---|---|---|---|---|---|
| O1 | 2025-01-05 | Asha | Hyderabad | Laptop | IT | 1 | 60000 |
| O1 | 2025-01-05 | Asha | Hyderabad | Mouse | IT | 2 | 1000 |
| O2 | 2025-01-09 | Ravi | Pune | Laptop | IT | 1 | 60000 |
| O3 | 2025-01-12 | Asha | Hyderabad | Mouse | IT | 3 | 1500 |

**DAX / Steps (not run here):**
1. Power Query: right-click the flat query > **Reference** twice, rename `Customer` and `Product`.
2. In each: keep only its columns (Home > Remove Columns > Remove Other Columns), **Remove Duplicates**, then Add Column > **Index Column** (from 1) as `CustomerKey` / `ProductKey`.
3. In the flat query: Home > **Merge Queries** to Customer on name+city, expand `CustomerKey`; same for Product; remove the descriptive columns.
4. Close & Apply; relate `Customer[CustomerKey]` 1 to * `Orders[CustomerKey]`, same for product; add a Date table (Q13).
**Alternative:** Do it in SQL or the source system before loading, if you have access (Q39).
**Result:** reproduced with pandas: Customer 2 rows, Product 2 rows, Orders fact 4 rows; Amount total 122500 in both flat and star.
**Pandas check:**
```python
import pandas as pd
flat = pd.DataFrame({"OrderID":["O1","O1","O2","O3"],
  "OrderDate":["2025-01-05","2025-01-05","2025-01-09","2025-01-12"],
  "CustomerName":["Asha","Asha","Ravi","Asha"],"City":["Hyderabad","Hyderabad","Pune","Hyderabad"],
  "ProductName":["Laptop","Mouse","Laptop","Mouse"],"Category":["IT"]*4,
  "Qty":[1,2,1,3],"Amount":[60000,1000,60000,1500]})
cust = flat[["CustomerName","City"]].drop_duplicates().reset_index(drop=True); cust.insert(0,"CustomerKey",cust.index+1)
prod = flat[["ProductName","Category"]].drop_duplicates().reset_index(drop=True); prod.insert(0,"ProductKey",prod.index+1)
fact = flat.merge(cust,on=["CustomerName","City"]).merge(prod,on=["ProductName","Category"])[["OrderID","OrderDate","CustomerKey","ProductKey","Qty","Amount"]]
print("Customer rows:", len(cust), "| Product rows:", len(prod), "| Fact rows:", len(fact))
print("Amount flat:", flat.Amount.sum(), "| Amount star:", fact.Amount.sum())
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
Customer rows: 2 | Product rows: 2 | Fact rows: 4
Amount flat: 122500 | Amount star: 122500
```
**Version / licensing note:** Microsoft Learn: Understand star schema and importance for Power BI (denormalized exports, index column, surrogate keys). Desktop menu names for Power Query from memory, unverified.
**Edge cases:** Same customer name in two cities (merge on name only would be wrong); mis-typed names create duplicate customers; the row counts and totals must match after the merge.
**Likely follow-ups:** 1) *Keep OrderID?* Yes as a degenerate dimension in the fact. 2) *Why not keep it flat?* Bigger model, repeated text, harder filtering (Q1, Q9).
**Common mistakes:** Merging on a non-unique column (row count grows); leaving descriptive columns in the fact; skipping the totals check.

### Q33 ⭐⭐ 🟡 What is a snowflake dimension, and would you flatten it in Power Query?
**Asked at:** star vs snowflake appears in prep sites and in Flipkart/Amazon BIE/Wipro mentions of star schema (research/interview_processes.md); no question-level company report.
**What the interviewer is checking:** Do you know the trade-off and Microsoft's default advice?
**Say this in the interview:** "A snowflake dimension is one business entity spread over several linked tables, like Product, Subcategory, Category. In Power BI I usually flatten it into one table in Power Query, because fewer tables and shorter filter paths are faster and simpler. I keep it snowflaked only when data is huge or the lookups are shared."
**Explain simply:**
- Snowflake: normalized tables positioned outward from the fact, each pointing to the next.
- Learn's drawbacks of keeping the snowflake: more tables to load, longer filter chains, a messier Data pane, and a hierarchy cannot span tables.
- Learn's benefit of flattening: one table, and one hierarchy from top to bottom; cost: repeated text in large dimensions.
- Learn says generally the benefits of a single table outweigh multiple tables, though the best decision depends on volume and usability.
**Example:** HR: Employee > Team > Department. Flatten to one `Employee` table that carries Team and Department names.
**Sample data:** Tables `Category`, `SubCategory`, `Product`

| Product | SubCategory | Category |
|---|---|---|
| Laptop X | Laptops | IT |
| Mouse M | Accessories | IT |
| Keyboard K | Accessories | IT |
| Chair C | Chairs | Furniture |

(this is the flattened result). The three input tables, as loaded: `Category` (C1 IT, C2 Furniture); `SubCategory` (S1 Laptops C1, S2 Accessories C1, S3 Chairs C2); `Product` (Laptop X S1, Mouse M S2, Keyboard K S2, Chair C S3).
**DAX / Steps (not run here):** In Power Query, select `Product` > Home > **Merge Queries** with `SubCategory` on SubID (Left Outer), expand the name; merge the result with `Category` on CatID, expand; remove key columns; disable load of the helper queries (right-click > untick **Enable load**).
**Alternative:** Create a calculated table with `RELATED` columns (Q31) or keep the snowflake and use a measure; flattening in Power Query or SQL is preferred.
**Result:** reproduced with pandas: 4 products in, 4 rows out after two left merges, each with SubCategory and Category.
**Pandas check:**
```python
import pandas as pd
cat = pd.DataFrame({"CatID":["C1","C2"],"Category":["IT","Furniture"]})
sub = pd.DataFrame({"SubID":["S1","S2","S3"],"SubCategory":["Laptops","Accessories","Chairs"],"CatID":["C1","C1","C2"]})
prod = pd.DataFrame({"ProdID":[1,2,3,4],"Product":["Laptop X","Mouse M","Keyboard K","Chair C"],"SubID":["S1","S2","S2","S3"]})
flat = prod.merge(sub,on="SubID",how="left").merge(cat,on="CatID",how="left")[["Product","SubCategory","Category"]]
print(flat.to_string(index=False))
print("Rows in:", len(prod), "| rows out:", len(flat))
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
   Product SubCategory  Category
  Laptop X     Laptops        IT
   Mouse M Accessories        IT
Keyboard K Accessories        IT
   Chair C      Chairs Furniture
Rows in: 4 | rows out: 4
```
**Version / licensing note:** Microsoft Learn: Understand star schema and importance for Power BI (snowflake dimensions section). "Enable load" menu name from memory, unverified; Learn's data-reduction page mentions the option.
**Edge cases:** A left merge never changes the row count unless the lookup key is duplicated; check row counts. Orphan products with no subcategory get blanks.
**Likely follow-ups:** 1) *Any case to keep snowflake?* Very large dimension or reuse. 2) *Hierarchy after flattening?* Yes, all levels live in one table (Q37).
**Common mistakes:** Flattening with an inner join (drops rows); leaving the helper tables loaded and visible.

### Q34 ⭐⭐ 🟡 How would you model Sales and Sales Target tables so that one Date slicer and one Product slicer filter both?
**Asked at:** commonly asked (no company-specific report found); Learn documents it as the higher-grain facts scenario.
**What the interviewer is checking:** Can you share dimensions across two fact tables, and handle targets stored at a higher grain?
**Say this in the interview:** "I put Date and Product dimensions in the middle, relate each fact table to them with one-to-many, and use the Date and Product slicers from the dimensions. If targets are stored by month and category, I store the first day of the month in Target, relate it to Date, and relate Category with a many-to-many or a small Category table. Then I control it with a measure."
**Explain simply:**
- Never slice with a column from a fact table: slicers must use **shared dimension** columns so one filter reaches both facts.
- Higher grain: Learn says to store the first date of the period (for example the 1st of the month) and relate Date one-to-many. Daily or monthly drill-down can show blanks, so measure logic should return BLANK at lower levels.
- Non-date higher grain (target by Category, products below category): Learn recommends many-to-many from Product to Target (single direction), and a measure that returns BLANK when a lower-level Product column is filtered.
- Hide the raw target column so only the measure is used.
**Example:** Monthly sales target per category (IT 550, HR Kit 120). A Product slicer on "Laptop" cannot split the IT target by product.
**Sample data:** Tables `Sales` and `Target`

| Sales: Month | Category | Product | Amount |
|---|---|---|---|
| 2025-01 | IT | Laptop | 500 |
| 2025-01 | HR Kit | Badge | 100 |
| 2025-02 | IT | Laptop | 600 |
| 2025-02 | HR Kit | Badge | 150 |

| Target: Month | Category | Target |
|---|---|---|
| 2025-01 | IT | 550 |
| 2025-01 | HR Kit | 120 |
| 2025-02 | IT | 550 |
| 2025-02 | HR Kit | 120 |

(Month is shown as yyyy-mm for readability; in the model it is the first day of the month as a date.)
**DAX / Steps (not run here):**
```dax
Target Quantity =
IF (
    NOT ISFILTERED ( 'Product'[ProductID] )
        && NOT ISFILTERED ( 'Product'[Product] ),
    SUM ( Target[Target] )
)
```
(Pattern adapted from Learn's Target Quantity example, which also tests Color.) Relationships: `Date[Date]` 1 to * `Sales[Date]` and `Target[Date]` (first of month); `Product[Category]` * to * `Target[Category]`, single direction from Product.
**Alternative:** Create a small `Category` dimension with unique categories and relate Product, Target and Sales Category through it (one-to-many everywhere). Cleaner than many-to-many. (Design choice, not from Learn.)
**Result:** reproduced with pandas: by month Sales 600 vs Target 670 (Jan), 750 vs 670 (Feb); by category IT 1100 vs 1100, HR Kit 250 vs 240. If Product = Laptop filters targets through Category, targets show 1100, the category target, not a laptop target.
**Pandas check:**
```python
import pandas as pd
sales = pd.DataFrame({"Month":["2025-01","2025-01","2025-02","2025-02"],"Category":["IT","HR Kit","IT","HR Kit"],
                      "Product":["Laptop","Badge","Laptop","Badge"],"Amount":[500,100,600,150]})
target = pd.DataFrame({"Month":["2025-01","2025-01","2025-02","2025-02"],"Category":["IT","HR Kit","IT","HR Kit"],"Target":[550,120,550,120]})
print(pd.DataFrame({"Sales":sales.groupby("Month").Amount.sum(),"Target":target.groupby("Month").Target.sum()}).to_string())
print(pd.DataFrame({"Sales":sales.groupby("Category").Amount.sum(),"Target":target.groupby("Category").Target.sum()}).to_string())
cats = sales[sales.Product=="Laptop"].Category.unique()
print("Target shown if Product = Laptop filters through Category:", target[target.Category.isin(cats)].Target.sum())
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
         Sales  Target
Month                 
2025-01    600     670
2025-02    750     670
          Sales  Target
Category               
HR Kit      250     240
IT         1100    1100
Target shown if Product = Laptop filters through Category: 1100
```
**Version / licensing note:** Microsoft Learn: Many-to-many relationship guidance (relate higher grain facts; ISFILTERED pattern); ISFILTERED function (DAX). Many-to-many is a limited relationship per Learn.
**Edge cases:** Month drill-down to days gives blanks without the measure. Targets at product level need no many-to-many.
**Likely follow-ups:** 1) *Allocate targets down to days?* Needs apportioning DAX; Learn mentions it as advanced. 2) *Two date slicers?* Only if different roles.
**Common mistakes:** Slicing on the fact table columns; relating Sales to Target directly; showing raw summed target at product level.

### Q35 ⭐⭐ 🟡 A relationship between two date columns does not work as expected. How can data types such as Date and DateTime cause this?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that "Date" in Power BI is just formatting on top of a DateTime stored with a time part?
**Say this in the interview:** "The engine stores everything as DateTime. A date column with a time part like 09:30 will not match a date table row at 00:00. Formatting a column as Date only changes the display. I remove the time in Power Query or add a pure date column."
**Explain simply:**
- Learn: the engine only uses DateTime; Date, Time and Date/Time/Timezone are formatting constructs, so relationships still see the time portion.
- Result: events at 09:30 and 14:10 on 5 Jan do not match a Date table row at 00:00, so rows become unmatched (blank members).
- Fix: in Power Query change the type to **Date** (removes the time) or create a separate date-only column.
- Both relationship columns should have the same data type.
**Example:** HR swipe log has a timestamp; the Calendar table has plain dates. A relationship on the raw timestamp matches nothing.
**Sample data:** Tables `Fact` and `Dim`

| EventTime | Hours |
|---|---|
| 2025-01-05 09:30 | 8 |
| 2025-01-05 14:10 | 7 |
| 2025-01-06 08:00 | 9 |

| Date | Weekday |
|---|---|
| 2025-01-05 | Sun |
| 2025-01-06 | Mon |

**DAX / Steps (not run here):** Power Query: add column **EventDate** with Add Column > Custom Column `DateTime.Date([EventTime])` (function from memory, unverified) or change type: Transform > Data Type > **Date**. Relate `Dim[Date]` to `Fact[EventDate]`; hide `EventTime`'s role in the relationship.
**Alternative:** Use a whole-number date key (yyyymmdd) in both tables; mark the date table (Q13). Learn notes that this case requires marking your own date table.
**Result:** reproduced with pandas: joining on the raw timestamp leaves 3 of 3 rows unmatched; after normalizing to date, 0 unmatched and hours total Sun 15, Mon 9.
**Pandas check:**
```python
import pandas as pd
fact = pd.DataFrame({"EventTime":pd.to_datetime(["2025-01-05 09:30","2025-01-05 14:10","2025-01-06 08:00"]),"Hours":[8,7,9]})
dim = pd.DataFrame({"Date":pd.to_datetime(["2025-01-05","2025-01-06"]),"Weekday":["Sun","Mon"]})
m = fact.merge(dim,left_on="EventTime",right_on="Date",how="left")
print("Unmatched on raw timestamp:", m.Weekday.isna().sum(), "of", len(m))
fact["EventDate"] = fact.EventTime.dt.normalize()
m2 = fact.merge(dim,left_on="EventDate",right_on="Date",how="left")
print("Unmatched after removing time:", m2.Weekday.isna().sum(), "| Hours by weekday:", m2.groupby("Weekday").Hours.sum().to_dict())
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
Unmatched on raw timestamp: 3 of 3
Unmatched after removing time: 0 | Hours by weekday: {'Mon': 9, 'Sun': 15}
```
**Version / licensing note:** Microsoft Learn: Model relationships in Power BI Desktop (data types of columns); Data types in Power BI (Date/time types); Set and use date tables in Power BI Desktop. Time zone: the model does not adjust time zones.
**Edge cases:** Date/Time/Timezone is converted to Date/Time and not shifted by user locale. A mixed column (some with time, some without) matches only partly.
**Likely follow-ups:** 1) *Why not just format as Date?* Formatting does not change stored values. 2) *Does it affect marking a date table?* Learn says Date/Time columns need the same timestamp on every value.
**Common mistakes:** Changing only the display format; joining a Date table to an event timestamp.

### Q36 ⭐⭐ 🟡 What is the Auto date/time feature, and why do many modellers turn it off?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the hidden-table behaviour and why a proper Date table is preferred?
**Say this in the interview:** "Auto date/time quietly builds a hidden date table for each date column so you get Year, Quarter, Month, Day drill-down for free. It is convenient for quick work, but it adds size, cannot be shared across tables or customised, so I turn it off and use one proper Date table."
**Explain simply:**
- Learn: it creates a hidden calculated table (built with CALENDAR) per date column, with Day, MonthNo, Month, QuarterNo, Quarter, Year and a hierarchy, when the table is Import, the column is Date or DateTime, and it is not on the "many" side of a relationship.
- Drawbacks listed by Learn: all or none; calendar periods only; no custom columns like weeks; months do not include the year; one hidden table per date column so filters do not propagate across facts; larger model and refresh time; not usable in Analyze in Excel.
- Learn's recommendation: keep it only for simple models, ad hoc exploration or profiling; otherwise use your own date table.
**Example:** A model with Join Date, Exit Date and Review Date gets three hidden tables, and no single Date slicer.
**DAX / Steps (not run here):** **File > Options and settings > Options**, then **Global** or **Current File** > **Data Load** > **Time intelligence** > untick Auto date/time (Learn gives this path). Turning it off in the current file removes the hidden tables, so repair visuals that used them.
**Alternative:** Create your own Date table with CALENDAR or CALENDARAUTO and mark it as the date table (Q13).
**Version / licensing note:** Microsoft Learn: Auto date/time in Power BI Desktop; Auto date/time guidance in Power BI Desktop. Both options default to on for a new installation. Desktop only.
**Edge cases:** Turning it off in an old file can break visuals using the date hierarchy. When you mark your own date table, Desktop removes the built-in tables.
**Likely follow-ups:** 1) *Does disabling reduce size?* Yes, hidden tables are calculated tables (Learn's data reduction page). 2) *Fiscal calendar?* Not possible with auto; build your own.
**Common mistakes:** Disabling globally but not for the file already open; not repairing broken visuals afterwards.

### Q37 ⭐⭐ 🟡 How do you create a hierarchy such as Year, Quarter, Month, or Department, Team, Employee?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know a hierarchy is a drill path inside one table?
**Say this in the interview:** "I right-click the top-level column in the Data pane and choose Create hierarchy, then add the lower levels in order, such as Department then Team then Employee. All levels must be in one table, so I flatten snowflaked tables first."
**Explain simply:**
- A **hierarchy** is a saved drill-down order of columns, so a visual can go from Department to Team to Employee with one click.
- Learn's optimization guide: hierarchies convey the order across multiple columns; right-click a column to create one.
- Levels must come from the same table; Learn's star schema page says a hierarchy cannot span more than one table.
- A true employee-manager chain (parent-child) is different: relationships cannot create it; Learn points to the DAX Parent and Child functions to flatten it into level columns.
**Example:** Year > Quarter > Month > Day on the Date table, and Department > Team > Employee on the Employee table. A bar chart of headcount drills from 4 departments into their teams.
**DAX / Steps (not run here):**
1. In the **Data** pane, right-click `Department` > **Create hierarchy** (wording from memory beyond "right-click a column").
2. Drag `Team` and `Employee` under it, or right-click each column > **Add to hierarchy** (from memory, unverified).
3. Rename the hierarchy `Org`. Add it to a visual and use the drill arrows.
**Alternative:** Drag the three fields into the **Axis** well in order; no saved hierarchy needed, and use "Expand all down one level". (Interface wording from memory, unverified.)
**Version / licensing note:** Microsoft Learn: Optimization guide for Power BI; Understand star schema and importance for Power BI; Model relationships in Power BI Desktop (parent-child functions pointer). Exact click labels beyond right-click not verified; the dedicated Create hierarchy page returned 404.
**Edge cases:** Unsorted months in the hierarchy (Q21). Blank team names appear as a blank level. Hierarchy columns must be unique per path (two teams called "Support" under different departments).
**Likely follow-ups:** 1) *Employee to manager chain?* Parent-child DAX functions (PATH family, from memory). 2) *Does the date table need a hierarchy?* Convenient, not required.
**Common mistakes:** Trying to build a hierarchy across two tables; wrong level order; forgetting to sort Month by number.

### Q38 ⭐⭐ 🟡 What affects the size and speed of a Power BI model, and how does the model design help?
**Asked at:** model optimization is reported as a Power BI topic at Deloitte (Hyderabad, 2025 Glassdoor reviewer reports summarized in research/interview_processes.md; exact mapping unverified).
**What the interviewer is checking:** Can you name the real levers: rows, columns, cardinality, data types, calculated columns and relationships?
**Say this in the interview:** "Model size mostly comes from how many columns and rows I load and how many unique values each column has. I keep only needed columns and rows, load numbers instead of long text where possible, use a star schema with one-to-many relationships, avoid bi-directional filters, and turn off auto date/time."
**Explain simply:**
- **Columns and rows:** Learn: remove unneeded columns (vertical filtering) and rows (horizontal filtering, such as only the last five years).
- **Cardinality (unique values):** high-cardinality text such as an order number takes more space. Numbers use value encoding; text uses hash encoding. Learn suggests converting text IDs to whole numbers where possible.
- **Summarise:** loading pre-summarised data is the most effective reduction but loses detail.
- **Calculated columns** compress worse and slow refresh; prefer Power Query columns.
- **Design:** star schema with dimensions that filter and facts that sum; bi-directional relationships can hurt performance; hidden auto date/time tables add size.
- Speed also depends on visuals (too many, unfiltered tables) and DAX, from memory beyond the optimization guide's visuals advice.
**Example:** An HR attendance fact with 10 years of daily rows and a text `EmployeeID`: load 3 years, convert the ID to whole number, and drop unused columns.
**DAX / Steps (not run here):** Power Query: remove columns (Home > Remove Columns); filter dates (column filter) or parameters; Transform > Data Type > Whole Number. Model: untick Auto date/time (Q36). Check: View > Performance analyzer in Desktop (from memory, unverified).
**Alternative:** DirectQuery or composite storage for the largest fact table, as Learn describes, with trade-offs.
**Version / licensing note:** Microsoft Learn: Data reduction techniques for Import modeling (shared capacity can host models up to 1 GB per the page; Premium sizes depend on SKU; page notes Premium per-capacity SKUs are being retired in favour of Fabric capacity); Optimization guide for Power BI; Model relationships in Power BI Desktop (performance order of relationship types).
**Edge cases:** Removing a column later can break reports; adding is easier. Summarising fact data removes drill-down.
**Likely follow-ups:** 1) *Biggest single win?* Reduce columns, rows and cardinality, or summarise. 2) *How compress?* VertiPaq, roughly 10x per Learn's example.
**Common mistakes:** Loading everything "just in case"; many calculated columns; bi-directional filters everywhere.

### Q39 ⭐⭐ 🟡 Where should you do a transformation: SQL, Power Query or DAX? How do you decide?
**Asked at:** commonly asked (no company-specific report found); the SUM vs SUMX style DAX topic is reported at Deloitte, but this exact question is not.
**What the interviewer is checking:** Do you push work as far upstream as practical, and keep DAX for things that depend on user selection?
**Say this in the interview:** "I do it as early as sensible: in the source or SQL if I can, then Power Query for cleaning and shaping, and DAX only for calculations that must react to slicers, like ratios, running totals and time intelligence. Row-level work belongs upstream; user-driven aggregation belongs in measures."
**Explain simply:**
- **SQL / source:** best for heavy joins, filtering large data and reuse by many reports. Learn: when the source is a database, calculations can be defined in SQL or materialised in the source for greater load efficiency.
- **Power Query (M):** cleaning, merging, splitting, unpivoting, type changes, one-time shaping before load.
- **DAX:** measures that change with filters; calculated columns only when they need model functions or measures. Learn: prefer Power Query columns over DAX calculated columns for efficiency.
- Ask: does the result depend on what the user selects? If yes DAX measure; if it is a fixed property of a row, do it upstream.
**Example:** Employee full name and tenure band: Power Query/SQL. Attrition rate for the selected department and month: DAX measure.
**DAX / Steps (not run here):** Decision list above. Example split: Power Query `Text.Combine({[First],[Last]}, " ")` for name (from memory); DAX `Attrition % = DIVIDE ( [Leavers], [Avg Headcount] )` for the rate (DIVIDE not fetched; from memory, unverified).
**Alternative:** Dataflows to centralise Power Query logic for many semantic models (Microsoft Learn: Power BI usage scenarios: Self-service data preparation (legacy) describes this, and notes Dataflow Gen1 is legacy).
**Version / licensing note:** Microsoft Learn: Data reduction techniques for Import modeling (preference for custom columns); Power BI usage scenarios: Self-service data preparation (legacy). Query folding behaviour was not fetched; from memory, unverified.
**Edge cases:** No source access means Power Query. In DirectQuery, some Power Query steps cannot be pushed to the source (from memory, unverified).
**Likely follow-ups:** 1) *Calculated column or measure?* Measure for values that respond to filters. 2) *Why not everything in DAX?* Larger model, slower refresh, harder to reuse.
**Common mistakes:** Building ratios as calculated columns (they do not respond to slicers); doing row cleaning repeatedly in DAX.

### Q40 ⭐⭐ 🟡 How do you check that your data model gives correct numbers before sharing the report?
**Asked at:** commonly asked (no company-specific report found); gap-fill from standard practice.
**What the interviewer is checking:** Do you reconcile to the source and test edge cases rather than trusting a pretty chart?
**Say this in the interview:** "I reconcile totals and row counts to the source, check for blank rows and duplicate keys, test filters on slicers, and compare a few numbers by hand or with a SQL or Excel query. Then I ask the business owner to confirm key figures."
**Explain simply:**
- **Reconcile:** report total vs source total; row counts per table before and after merges.
- **Blank members:** a (Blank) row in a dimension visual means orphan keys (Q29). The blank hides real money.
- **Key uniqueness:** the "one" side must be unique; Learn says a refresh with duplicates in a "one" side column fails.
- **Test slicers and totals:** non-additive cases such as many-to-many (Q28) and role-playing dates (Q26).
- **Spot-check** three known values with a different tool, and ask the business owner to sign off.
**Example:** Source Excel sales total is 2100. The product visual shows A 300, B 700, C 500 and (Blank) 600. The total ties to 2100, and the blank row is the orphan key 9 with 600.
**Sample data:** Tables `Sales` and `Product`

| Sales: OrderID | ProductKey | Amount |
|---|---|---|
| 1 | 1 | 100 |
| 2 | 1 | 200 |
| 3 | 2 | 300 |
| 4 | 2 | 400 |
| 5 | 3 | 500 |
| 6 | 9 | 600 |

| Product: ProductKey | Name |
|---|---|
| 1 | A |
| 2 | B |
| 3 | C |

**DAX / Steps (not run here):**
```dax
Sales Total = SUM ( Sales[Amount] )
Sales Rows = COUNTROWS ( Sales )
```
Put both in a card next to the source figures; then a table with `Product[Name]` and `[Sales Total]` and look for (Blank). Power Query: Merge Queries with **Left Anti** to list orphans (Q29).
**Alternative:** Use DAX query view or Analyze in Excel to compare a pivot to the source (availability not verified; from memory).
**Result:** reproduced with pandas: source total 2100; visual rows A 300, B 700, C 500, (Blank) 600, visual total 2100; orphan key 9 with amount 600; duplicate dimension keys 0; duplicate fact rows 0.
**Pandas check:**
```python
import pandas as pd
src = pd.DataFrame({"OrderID":[1,2,3,4,5,6],"ProductKey":[1,1,2,2,3,9],"Amount":[100,200,300,400,500,600]})
prod = pd.DataFrame({"ProductKey":[1,2,3],"Name":["A","B","C"]})
j = src.merge(prod,on="ProductKey",how="left")
by = j.assign(Name=j.Name.fillna("(Blank)")).groupby("Name").Amount.sum()
print(by.to_string())
print("Source total:", src.Amount.sum(), "| visual total:", by.sum())
print("Orphan keys:", sorted(set(src.ProductKey)-set(prod.ProductKey)), "| duplicate dimension keys:", prod.ProductKey.duplicated().sum(),
      "| duplicate fact rows:", src.duplicated().sum())
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
Name
(Blank)    600
A          300
B          700
C          500
Source total: 2100 | visual total: 2100
Orphan keys: [9] | duplicate dimension keys: 0 | duplicate fact rows: 0
```
**Version / licensing note:** Microsoft Learn: Model relationships in Power BI Desktop (blank virtual rows, one-side uniqueness, Assume referential integrity risk of understated results); COUNTROWS function (DAX); SUM function (DAX).
**Edge cases:** With Assume referential integrity or many-to-many (inner join), orphans vanish and totals fall short, with no blank row to warn you. Check filters, time zones, and incremental refresh gaps (from memory).
**Likely follow-ups:** 1) *What if totals differ?* Check orphan keys, duplicates, filters on the page, and blank dates. 2) *Who signs off?* The data owner for the key KPIs.
**Common mistakes:** Comparing only the grand total; ignoring (Blank); testing with no slicers applied.

### Q41 ⭐⭐ 🟡 Two tables can only be matched using two columns together, for example Employee ID plus Month. How do you build the relationship, since Power BI links one column to one column?
**Asked at:** commonly asked (no company-specific report found); gap-fill from standard practice.
**What the interviewer is checking:** Do you know a relationship uses one column per side, and can you create a single combined key?
**Say this in the interview:** "A relationship can only use one column on each side, so I build one combined key column in both tables, for example EmpID and Month joined with a separator, and relate on that. Better still, I add a proper Employee-Month dimension so both facts filter through it."
**Explain simply:**
- A **composite key** means two columns together identify a row (Employee E1 in January is unique, E1 alone is not).
- Power BI relationships take one column each side, so you glue the two into one text or number column, e.g. `E1|2026-01`.
- Build it in **Power Query** (before load) where possible; a DAX calculated column also works but costs model size.
- Use a separator so `E1`+`12` and `E11`+`2` cannot collide.
**Example:** Payroll (one row per employee per month) and Attendance (same grain). Joining on EmpID alone gives 8 rows instead of 4 and doubles the totals.
**Sample data:** Table `Payroll`, table `Attendance` (same 4 employee-month rows)

| EmpID | Month | NetPay | DaysPresent |
|---|---|---|---|
| E1 | 2026-01 | 50000 | 22 |
| E1 | 2026-02 | 50000 | 20 |
| E2 | 2026-01 | 42000 | 19 |
| E2 | 2026-02 | 43000 | 21 |

**DAX / Steps (not run here):**
```m
// Power Query, in both tables: Add Column > Custom Column
= Table.AddColumn(Source, "EmpMonthKey", each [EmpID] & "|" & [Month], type text)
```
Then Model view: drag `Payroll[EmpMonthKey]` to `Attendance[EmpMonthKey]`. Prefer relating both to a small `EmployeeMonth` dimension (one-to-many from it to each).
**Alternative:** Skip the relationship and use `LOOKUPVALUE` or `TREATAS` in a measure (Q60); or merge the two tables into one in Power Query if they share a grain.
**Result:** reproduced with pandas: joined on the combined key gives 4 rows, NetPay 185,000, DaysPresent 82. Joined on EmpID only gives 8 rows.
**Pandas check:**
```python
import pandas as pd
pay = pd.DataFrame({"EmpID":["E1","E1","E2","E2"],"Month":["2026-01","2026-02","2026-01","2026-02"],"NetPay":[50000,50000,42000,43000]})
att = pd.DataFrame({"EmpID":["E1","E1","E2","E2"],"Month":["2026-01","2026-02","2026-01","2026-02"],"DaysPresent":[22,20,19,21]})
pay["Key"] = pay.EmpID+"|"+pay.Month; att["Key"] = att.EmpID+"|"+att.Month
m = pay.merge(att[["Key","DaysPresent"]],on="Key")
print("Combined key: rows", len(m), "| NetPay", m.NetPay.sum(), "| DaysPresent", m.DaysPresent.sum())
print("EmpID only: rows", len(pay.merge(att,on="EmpID")))
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
Combined key: rows 4 | NetPay 185000 | DaysPresent 82
EmpID only: rows 8
```
**Version / licensing note:** from memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft page was read for this answer). Relationship rules (one column each side) are from memory.
**Edge cases:** Blank in either part makes the key partly empty; both key columns must have the same data type (text); a key that is not unique on the "one" side forces many-to-many.
**Likely follow-ups:** 1) *Why not relate on EmpID alone?* It is many-to-many and inflates totals. 2) *Calculated column or Power Query?* Power Query, it compresses better.
**Common mistakes:** No separator; building the key in only one table; relating on a non-unique key.

### Q42 ⭐ 🟢 What naming and documentation habits do you follow for tables, columns and measures in a model?
**Asked at:** commonly asked (no company-specific report found); gap-fill from standard practice.
**What the interviewer is checking:** Can others pick up your model without asking you what things mean?
**Say this in the interview:** "I use clear business names, fact and dimension tables named consistently, no spaces tricks or abbreviations, measures kept in one place with descriptions, helper columns hidden, and a short note on the model's purpose."
**Explain simply:**
- Name tables by what a row is: `Employee`, `Department`, `Attendance`, not `Sheet1` or `tbl_x_v2`.
- Use friendly column names (`Hire Date`, not `HDT`); hide keys and helper columns (Q22).
- Put measures in a dedicated **measures table** (an empty table that only holds measures) and group them in display folders.
- Add a **description** (Properties pane) to each measure explaining the logic, and use consistent units (`Attrition %`, `Headcount`).
- Keep one naming rule; a team convention beats a personal one.
**Example:** `Attrition %` described as "Leavers in period / average headcount, excludes interns" saves a long debate with an HR head.
**DAX / Steps (not run here):** Model view > select item > **Properties** pane > **Description**; **Display folder** box groups measures; **Home > Enter data** can create an empty `_Measures` table (names from memory, unverified).
**Alternative:** Document outside the model (a data dictionary sheet or wiki page), or use tools that read model metadata.
**Version / licensing note:** from memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft page was read for this answer). Menu wording changes between releases.
**Edge cases:** Renaming a column in Power Query after reports exist can break visuals; renaming in the model is safer. Measure names must be unique across the model.
**Likely follow-ups:** 1) *Prefix or no prefix for tables?* Pick one rule and keep it. 2) *Where do descriptions show?* In the field hover in report view (from memory).
**Common mistakes:** Names like `Measure 1`; leaving 40 raw columns visible; documenting only in your head.

### Q43 ⭐ 🟢 Which tool do you use to build a data model, and can you build one in Power BI Desktop on a Mac?
**Asked at:** commonly asked (no company-specific report found); gap-fill from standard practice.
**What the interviewer is checking:** Do you know Desktop is the authoring tool and its platform limit?
**Say this in the interview:** "I build the model in Power BI Desktop, using Power Query for cleaning and Model view for relationships. Desktop runs on Windows only, so on a Mac I would use a Windows virtual machine or cloud PC, or the Power BI web service for limited editing."
**Explain simply:**
- **Power BI Desktop** is the free app where you load data, clean it (Power Query), model it (Model view) and design reports.
- It is a Windows application. There is no Mac version (to my knowledge, unverified here).
- Mac options: Windows through virtualisation software such as Parallels, a Windows cloud PC or a company remote desktop. The browser **Power BI Service** can build reports and edit some model parts, but is not a full replacement.
- Other model tools exist (Tabular Editor, DAX Studio) but they also run on Windows.
**Example:** A recruiter analyst on a MacBook uses the company's Windows virtual desktop to open the `.pbix` file, then publishes to the Service.
**DAX / Steps (not run here):** Desktop: left rail has **Report**, **Table**, **Model** and (in newer builds) **DAX query** views; relationships are drawn in **Model view**.
**Alternative:** Build the model in the Service using a published semantic model and edit in the browser, accepting fewer features.
**Version / licensing note:** from memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft page was read for this answer). The Windows-only claim and Service editing limits are both from memory; the research notes flag the Windows-only claim for verification against Microsoft's system-requirements page, which was not read here.
**Edge cases:** Apple-silicon Macs running Windows under emulation can be slow; company policy may block personal VMs.
**Likely follow-ups:** 1) *Is Desktop free?* Yes, but sharing needs a licence (from memory). 2) *Can Mac users view reports?* Yes, in a browser.
**Common mistakes:** Saying "just install it on Mac"; confusing Desktop with the web Service.

### Q44 ⭐ 🟡 What is a one-to-one relationship, and when is it a sign of poor design?
**Asked at:** commonly asked (no company-specific report found); not seen in any source list.
**What the interviewer is checking:** Do you know both sides are unique, and that it usually means tables should be merged?
**Say this in the interview:** "In a one-to-one relationship each key appears at most once on both sides. It is often a sign the two tables describe the same thing and should be combined into one, unless there is a good reason such as security or very wide tables."
**Explain simply:**
- **Cardinality** is how many rows on one side match rows on the other. One-to-one means each employee has exactly one contact record.
- Filters flow both ways in a one-to-one relationship, so the two tables behave like one.
- Poor design when the split adds no value: more tables, more relationships, nothing gained.
- Valid when you split rarely used wide columns, keep sensitive columns apart, or load from two systems.
**Example:** `Employee` (4 rows) and `EmployeeContact` (4 rows), both keyed on EmpID. Merge them in Power Query into one `Employee` table.
**Sample data:** Table `Employee` and `EmployeeContact`

| EmpID | Phone (Contact) |
|---|---|
| 1 | a |
| 2 | b |
| 3 | c |
| 4 | d |

**DAX / Steps (not run here):** Merge: Power Query **Home > Merge Queries > Merge Queries as New**, join on EmpID, choose Left Outer, expand Phone. Or keep separate: Model view, drag EmpID to EmpID, Cardinality **One to one**.
**Alternative:** Fold the extra columns into the main table as columns, or keep the second table and hide it.
**Result:** reproduced with pandas: EmpID unique in both tables (`True True`), joined rows 4 = same as each table, so a merge is lossless.
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"EmpID":[1,2,3,4]})
con = pd.DataFrame({"EmpID":[1,2,3,4],"Phone":list("abcd")})
print(emp.EmpID.is_unique, con.EmpID.is_unique, len(emp.merge(con,on="EmpID")))
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
True True 4
```
**Version / licensing note:** from memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft page was read for this answer). Behaviour of one-to-one filtering both ways is from memory.
**Edge cases:** If one side has duplicates the relationship cannot be one-to-one; an employee with no contact row gives blanks after a merge.
**Likely follow-ups:** 1) *Does it need bi-directional?* It filters both ways automatically. 2) *Security reason?* Keep salary in a separate table for RLS.
**Common mistakes:** Splitting a table "to be tidy"; picking one-to-one when data actually has duplicates.

### Q45 ⭐ 🟡 What is a degenerate dimension?
**Asked at:** commonly asked (no company-specific report found); advanced modelling term, not in any India interview report seen.
**What the interviewer is checking:** Do you know the dimension vocabulary and when not to create a table?
**Say this in the interview:** "A degenerate dimension is an identifier that lives in the fact table, such as an invoice or requisition number. It has no attributes of its own, so I keep it in the fact table and do not build a separate dimension for it."
**Explain simply:**
- A **dimension** describes the thing being measured (who, what, where). A **fact** table holds the numbers.
- A requisition number groups rows (all offers for one job opening) but has no description columns, so a table would be one useless column.
- Use it to count or drill to detail: "how many requisitions".
**Example:** Hiring fact with `ReqNo`: R1 has 2 offers, R2 1, R3 3.
**Sample data:** Table `HiringFact`

| ReqNo | Dept | Offers |
|---|---|---|
| R1 | A | 1 |
| R1 | B | 1 |
| R2 | A | 1 |
| R3 | B | 1 |
| R3 | A | 1 |
| R3 | B | 1 |

**DAX / Steps (not run here):**
```dax
Requisitions = DISTINCTCOUNT ( HiringFact[ReqNo] )
Offers = SUM ( HiringFact[Offers] )
```
**Alternative:** Move it to a small `Requisition` dimension only if you need attributes (hiring manager, open date).
**Result:** reproduced with pandas: 3 distinct requisitions, 6 rows, offers per requisition R1=2, R2=1, R3=3.
**Pandas check:**
```python
import pandas as pd
f = pd.DataFrame({"ReqNo":["R1","R1","R2","R3","R3","R3"],"Dept":["A","B","A","B","A","B"],"Offers":[1]*6})
print(f.groupby("ReqNo").Offers.sum().to_dict(), "distinct requisitions:", f.ReqNo.nunique(), "| rows:", len(f))
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
{'R1': 2, 'R2': 1, 'R3': 3} distinct requisitions: 3 | rows: 6
```
**Version / licensing note:** from memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft page was read for this answer). Terminology is standard Kimball modelling; page not read here.
**Edge cases:** DISTINCTCOUNT counts a blank ReqNo as one extra value (DISTINCTCOUNTNOBLANK skips it; from memory, unverified), so clean blank IDs first.
**Likely follow-ups:** 1) *Is it a key?* It is an ID, not a foreign key. 2) *Hide it?* Hide it if only used inside measures.
**Common mistakes:** Building a one-column dimension; summing the ID.

### Q46 ⭐ 🟡 What is a junk dimension, and when would you build one?
**Asked at:** commonly asked (no company-specific report found); advanced modelling term.
**What the interviewer is checking:** Can you tidy a model cluttered with low-cardinality flags?
**Say this in the interview:** "A junk dimension combines several small flag columns, like gender, shift and remote yes/no, into one table with one row per combination. The fact table then carries a single key instead of many flag columns."
**Explain simply:**
- Each flag has only a few values, and a separate table for each would clutter the model.
- You list the combinations that actually occur (or all possible) and give each a key.
- Benefit: fewer columns in the big fact table, fewer tables than one per flag.
**Example:** 6 attendance rows with three flags only use 4 combinations (out of 2x2x2 = 8 possible). The junk table has 4 rows.
**Sample data:** Table `JunkAttendance` (key plus flags)

| JunkKey | Gender | Shift | Remote |
|---|---|---|---|
| 1 | M | Day | Y |
| 2 | F | Day | N |
| 3 | M | Night | N |
| 4 | F | Night | Y |

**DAX / Steps (not run here):**
```m
// Power Query: copy the fact query, keep the flag columns, then
// Home > Remove Rows > Remove Duplicates, then Add Column > Index Column (from 1)
// Merge the junk table back into the fact on the three flags to get JunkKey, then delete the flags.
```
**Alternative:** Leave the flags in the fact table if there are only one or two (simpler), or build a dimension per important flag.
**Result:** reproduced with pandas: 6 fact rows reduce to 4 junk rows (max 8 possible).
**Pandas check:**
```python
import pandas as pd
j = pd.DataFrame({"Gender":["M","F","M","F","M","F"],"Shift":["Day","Day","Night","Night","Day","Night"],"Remote":["Y","N","N","Y","Y","Y"]})
jd = j.drop_duplicates().reset_index(drop=True); jd.insert(0,"JunkKey",jd.index+1)
print(jd.to_string(index=False))
print("Fact rows:", len(j), "| junk rows:", len(jd), "| possible combinations:", 2*2*2)
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
 JunkKey Gender Shift Remote
       1      M   Day      Y
       2      F   Day      N
       3      M Night      N
       4      F Night      Y
Fact rows: 6 | junk rows: 4 | possible combinations: 8
```
**Version / licensing note:** from memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft page was read for this answer). Concept is from the Microsoft star schema guidance as listed in the sources file, but that page was not re-read here.
**Edge cases:** New combinations appear later, so refresh must add rows. Gender is sensitive, so check policy.
**Likely follow-ups:** 1) *Why not one table per flag?* Too many tiny tables. 2) *Junk vs degenerate?* Junk groups flags; degenerate is an ID.
**Common mistakes:** Putting high-cardinality columns in a junk dimension; forgetting the key merge.

### Q47 ⭐ 🟡 What is a factless fact table? Give an example such as employee attendance or training enrolment.
**Asked at:** commonly asked (no company-specific report found); advanced modelling term.
**What the interviewer is checking:** Do you understand that a fact table can record events with no numeric measure?
**Say this in the interview:** "A factless fact table records that something happened, like an employee enrolled in a course, with no numbers to add up. I measure it by counting rows, and I can also find what did not happen, such as who never enrolled."
**Explain simply:**
- A normal fact has numbers (salary, sales). A factless fact has only keys: who, what, when.
- The measure is `COUNTROWS` of that table.
- To find "no enrolment" you compare against the full dimension list.
**Example:** Table `TrainingEnrolment`: 5 enrolments; 3 employees in POSH training; of E1 to E5, E4 and E5 have not done POSH.
**Sample data:** Table `TrainingEnrolment`

| EmpID | Course | Month |
|---|---|---|
| E1 | POSH | Jan |
| E1 | Excel | Jan |
| E2 | POSH | Jan |
| E3 | POSH | Feb |
| E4 | Excel | Feb |

**DAX / Steps (not run here):**
```dax
Enrolments = COUNTROWS ( TrainingEnrolment )
Employees Enrolled = DISTINCTCOUNT ( TrainingEnrolment[EmpID] )
Not Enrolled in POSH =
COUNTROWS (
    EXCEPT (
        VALUES ( Employee[EmpID] ),
        CALCULATETABLE ( VALUES ( TrainingEnrolment[EmpID] ), TrainingEnrolment[Course] = "POSH" )
    )
)
```
**Alternative:** Add a column of 1 and `SUM` it (works but redundant), or use `COUNTROWS ( FILTER ( Employee, NOT ( Employee[EmpID] IN CALCULATETABLE ( VALUES ( TrainingEnrolment[EmpID] ), TrainingEnrolment[Course] = "POSH" ) ) ) )`.
**Result:** reproduced with pandas (the `Employee` table holds E1 to E5): 5 enrolments; 3 distinct POSH employees; not on POSH: E4, E5, so `Not Enrolled in POSH` = 2.
**Pandas check:**
```python
import pandas as pd
enr = pd.DataFrame({"EmpID":["E1","E1","E2","E3","E4"],"Course":["POSH","Excel","POSH","POSH","Excel"],"Month":["Jan","Jan","Jan","Feb","Feb"]})
allemp = ["E1","E2","E3","E4","E5"]
posh = enr[enr.Course=="POSH"].EmpID
print("Enrolments:", len(enr), "| distinct employees on POSH:", posh.nunique())
not_posh = [e for e in allemp if e not in posh.values]
print("Not enrolled in POSH:", not_posh, "| count:", len(not_posh))
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
Enrolments: 5 | distinct employees on POSH: 3
Not enrolled in POSH: ['E4', 'E5'] | count: 2
```
**Version / licensing note:** from memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft page was read for this answer). Function behaviours (`COUNTROWS`, `EXCEPT`, `VALUES`) are from memory; pages not read here.
**Edge cases:** The course is fixed to POSH inside the measure; to follow a slicer instead, filter `TrainingEnrolment[Course]` from the slicer and make sure the dimensions are related.
**Likely follow-ups:** 1) *Another example?* Daily attendance records. 2) *How is the grain stated?* One row per employee-course-month.
**Common mistakes:** Adding a fake numeric column; forgetting people with zero rows do not appear in the fact.

### Q48 ⭐ 🟡 What is a disconnected table, and how is it used with a What-if parameter or a slicer?
**Asked at:** commonly asked (no company-specific report found); not in any India interview report seen.
**What the interviewer is checking:** Can you let users pick a value and feed it into a measure without a relationship?
**Say this in the interview:** "A disconnected table has no relationship to the rest of the model. A slicer on it lets the user choose a value, and my measure reads that choice with SELECTEDVALUE. A What-if parameter creates exactly such a table for me."
**Explain simply:**
- Normally slicers filter data through relationships. A disconnected table filters nothing by itself.
- The measure reads the pick: `SELECTEDVALUE ( Hike[Hike %], 0 )` gives the single chosen value, or 0 if none or many.
- A **What-if parameter** (Modeling tab) makes a table of numbers, a slicer and a measure for you.
**Example:** Total salary 150,000. Slicer picks 5% hike, projected cost 157,500; 10% gives 165,000.
**Sample data:** Table `Salary`, disconnected table `Hike`

| EmpID | Salary |
|---|---|
| 1 | 40000 |
| 2 | 50000 |
| 3 | 60000 |

Table `Hike`: values 0, 0.05, 0.10 in column `Hike %`.
**DAX / Steps (not run here):**
```dax
Projected Salary Cost =
SUM ( Salary[Salary] ) * ( 1 + SELECTEDVALUE ( Hike[Hike %], 0 ) )
```
Steps: **Modeling tab (or Home) > New parameter > Numeric range**, set 0 to 0.10, step 0.05, add slicer; or **Enter data** to make `Hike`. Do not draw a relationship (menu path from memory).
**Alternative:** `MAX ( Hike[Hike %] )` instead of `SELECTEDVALUE` (picks the highest when several are chosen).
**Result:** reproduced with pandas: 150000 at 0, 157500 at 5%, 165000 at 10%.
**Pandas check:**
```python
import pandas as pd
sal = pd.DataFrame({"EmpID":[1,2,3],"Salary":[40000,50000,60000]})
for p in (0,0.05,0.10): print(f"Hike {p:.0%}: projected cost {sal.Salary.sum()*(1+p):,.0f}")
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
Hike 0%: projected cost 150,000
Hike 5%: projected cost 157,500
Hike 10%: projected cost 165,000
```
**Version / licensing note:** from memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft page was read for this answer). What-if parameter menu names and `SELECTEDVALUE` behaviour are from memory, unverified.
**Edge cases:** Multi-select returns the default (0); the parameter's measure is created for you; use the same trick for a measure-switching slicer.
**Likely follow-ups:** 1) *Can it filter data?* Only via a measure or `TREATAS`. 2) *Can it be in the Service?* Parameter is a Desktop authoring feature (from memory).
**Common mistakes:** Relating the table accidentally; using `VALUES` where more than one value is possible.

### Q49 ⭐ 🟡 Why do modellers prefer integer keys over text keys for relationships?
**Asked at:** commonly asked (no company-specific report found); gap-fill from standard practice.
**What the interviewer is checking:** Do you care about model size, speed and clean keys?
**Say this in the interview:** "Integer keys are smaller and faster to compare than long text, avoid spelling and case problems, and are safer when a business code changes. I use an integer surrogate key in the dimension and fact."
**Explain simply:**
- A **surrogate key** is a made-up whole number (1, 2, 3) with no business meaning, used only to link tables.
- Text takes more memory when stored and joined, mismatches on spaces, case or typos (`D01` vs `d01 `).
- Business codes can be reused or changed, a surrogate key is stable (and needed for history, Q55).
- Honest caveat: Power BI compresses columns well, so the gain depends on how many different values the column has.
**Sample data:** 1,000,000 fact rows whose department code is one of 5,000 different values, stored once as a whole number (for example 17) and once as text (for example `DEPT-00017-IND`).
**Example:** 1,000,000 fact rows, 5,000 different department codes. As plain Python data, the integer column takes 8 MB and the text column about 63 MB in pandas (15-character codes).
**DAX / Steps (not run here):** Power Query: add an **Index Column** to the dimension, **Merge** the fact on the business code to bring the key in, then remove the text code from the fact. Set key columns to **Whole Number**.
**Alternative:** Keep the natural key when it is already a short integer (e.g. EmployeeID 1001).
**Result:** reproduced with pandas memory use (not VertiPaq): integer 8,000,000 bytes, text 63,000,000 bytes. This shows the idea only; Power BI's stored size will differ.
**Pandas check:**
```python
import pandas as pd, numpy as np
codes = np.arange(5000)
ints = pd.Series(np.random.default_rng(1).choice(codes, 1_000_000))
strs = ints.map(lambda x: f"DEPT-{x:05d}-IND")
print("int64 bytes:", ints.memory_usage(index=False), "| text bytes (pandas, deep):", strs.astype(object).memory_usage(index=False, deep=True))
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
int64 bytes: 8000000 | text bytes (pandas, deep): 63000000
```
**Version / licensing note:** from memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft page was read for this answer). Performance claims are from memory, unverified; pandas memory is not the same as Power BI storage.
**Edge cases:** Leading zeros in codes (`007`) get lost when stored as numbers; relationships need matching data types on both sides.
**Likely follow-ups:** 1) *Do you hide the key?* Yes (Q22). 2) *Integer or GUID?* Integer.
**Common mistakes:** Claiming integers are always dramatically faster; mixing text and number types.

### Q50 ⭐ 🟡 How do you handle fact rows whose key has no match in the dimension, such as an unknown department code?
**Asked at:** commonly asked (no company-specific report found); gap-fill from standard practice.
**What the interviewer is checking:** Do you avoid silently hiding or mislabelling money?
**Say this in the interview:** "I find the orphan keys first, then fix the source if possible. Otherwise I add an Unknown row to the dimension and map unmatched keys to it, so totals stay complete and the gap is visible."
**Explain simply:**
- An **orphan** fact row has a key missing from the dimension.
- Power BI shows these under a **blank** group (from memory) so totals still match, but it looks like a missing label.
- Better: an explicit `Unknown` member so reports show "Unknown 75", and fix over time.
**Example:** Cost rows for D99 (50) and D77 (25) have no department. Without a fix 75 shows under blank; with Unknown it is labelled.
**Sample data:** Table `Cost` and `Department`

Table `Cost`:

| Dept | Cost |
|---|---|
| D1 | 100 |
| D2 | 200 |
| D99 | 50 |
| D1 | 150 |
| D77 | 25 |

Table `Department`:

| Dept | Name |
|---|---|
| D1 | HR |
| D2 | IT |

**DAX / Steps (not run here):**
```m
// Power Query on the fact: replace unmatched codes
= Table.TransformColumns(Cost, {"Dept", each if List.Contains(Department[Dept], _) then _ else "Unknown"})
```
Add a row `Unknown` to the department table (Enter data, then Append Queries).
**Alternative:** Leave the rows as they are and find the orphans with a Power Query anti-join (Home > Merge Queries > Left Anti), then fix the source.
**Result:** reproduced with pandas: before fix HR 250, IT 200, blank 75; after fix HR 250, IT 200, Unknown 75. Total 525 both times.
**Pandas check:**
```python
import pandas as pd
cost = pd.DataFrame({"Dept":["D1","D2","D99","D1","D77"],"Cost":[100,200,50,150,25]})
dim = pd.DataFrame({"Dept":["D1","D2"],"Name":["HR","IT"]})
before = cost.merge(dim,on="Dept",how="left")
print("Before:"); print(before.groupby("Name",dropna=False).Cost.sum().to_string())
cost["Dept"] = cost.Dept.where(cost.Dept.isin(dim.Dept),"Unknown")
dim2 = pd.concat([dim,pd.DataFrame({"Dept":["Unknown"],"Name":["Unknown"]})])
after = cost.merge(dim2,on="Dept",how="left")
print("After:"); print(after.groupby("Name").Cost.sum().to_string()); print("Total:", after.Cost.sum())
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
Before:
Name
HR     250
IT     200
NaN     75
After:
Name
HR         250
IT         200
Unknown     75
Total: 525
```
**Version / licensing note:** from memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft page was read for this answer). The blank virtual row behaviour is from memory (the sources file says the relationships page covers it, but the page was not read here).
**Edge cases:** Rows with an empty key behave the same; DirectQuery and referential integrity settings change how orphans show (Q54).
**Likely follow-ups:** 1) *Why not delete them?* Totals would no longer match finance. 2) *How do you catch them?* Anti-join in Power Query.
**Common mistakes:** Filtering out unmatched rows; leaving a blank bar nobody explains.

### Q51 ⭐ 🟡 What causes an ambiguous path or circular dependency error in a model, and how do you fix it?
**Asked at:** commonly asked (no company-specific report found); not in any India interview report seen.
**What the interviewer is checking:** Do you understand that filters need one clear route between tables?
**Say this in the interview:** "It happens when there are two or more routes between the same pair of tables, often from bi-directional filters or extra relationships. I fix it by removing loops, making filters single direction, keeping one active path, or using an inactive relationship with USERELATIONSHIP."
**Explain simply:**
- A **filter route** is the chain of relationships a slicer click travels along.
- If two routes exist, Power BI cannot tell which to use: that is **ambiguity**. Power BI makes one relationship inactive or refuses to create it.
- A **circular dependency** is a loop, A to B to C to A, in relationships or in calculated columns that refer to each other.
- Typical HR cause: `Employee` and `Manager` both link to `Department`, and `Department` links back through a second path.
**Example:** `Date` links to `Joining Date` and `Exit Date` in an `Employee` fact: two paths. One stays active, the other is inactive.
**DAX / Steps (not run here):**
```dax
Exits by Exit Date =
CALCULATE ( COUNTROWS ( Employee ), USERELATIONSHIP ( Employee[Exit Date], 'Date'[Date] ) )
```
Fix steps: Model view, find the loop, change **Cross filter direction** to **Single**, remove the redundant link, or mark one **Active** off.
**Alternative:** Create a second `Date` table copy (role-playing dimension), one per date role.
**Result:** concept question; the sample numbers for the USERELATIONSHIP pattern (reproduced with pandas, not a DAX engine) are in Q25 and Q26.
**Version / licensing note:** from memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft page was read for this answer). Behaviour of ambiguity handling and `USERELATIONSHIP` is from memory; pages not read here.
**Edge cases:** Calculated column loops give a circular dependency message even with no relationship issue.
**Likely follow-ups:** 1) *Can two relationships both be active?* Not between the same two tables. 2) *Why avoid bi-directional?* It causes the loops.
**Common mistakes:** Turning everything to bi-directional; deleting the wrong relationship.

### Q52 ⭐ 🟡 What is a composite model in Power BI?
**Asked at:** commonly asked (no company-specific report found); not in any India interview report seen.
**What the interviewer is checking:** Do you know you can mix storage modes and sources in one model?
**Say this in the interview:** "A composite model mixes storage modes, for example Import tables and DirectQuery tables, or adds your own tables to a published semantic model. It lets you keep large data live and small tables fast."
**Explain simply:**
- **Import** copies data into the model; **DirectQuery** leaves it at the source and queries it each time.
- A composite model uses both, and a table can be set to **Dual** (acts as either) so slicers stay quick.
- You can also extend a published semantic model with your own local tables.
- Relationships between tables in different storage modes are **limited** relationships (from memory, details unverified).
**Example:** A 200 million row attendance log stays in DirectQuery on the warehouse; the small `Department` list is Import/Dual.
**DAX / Steps (not run here):** Model view > select table > **Properties > Advanced > Storage mode** (Import, DirectQuery, Dual) (path from memory, unverified).
**Alternative:** Use fully Import with scheduled refresh if the data fits, or one DirectQuery source.
**Version / licensing note:** from memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft page was read for this answer). Storage-mode names are standard; behaviour and limits are from memory. The sources file lists the relationships page as covering composite models, but it was not read here.
**Edge cases:** Limited relationships do not enforce a one side and may skip blank-row handling; DirectQuery sources may need a gateway.
**Likely follow-ups:** 1) *Why Dual?* Slicers hit the cached copy. 2) *Downside?* Slower, more complex.
**Common mistakes:** Calling any two-source Import model composite; ignoring query load on the source.

### Q53 ⭐ 🟡 Why build one shared semantic model and connect several reports to it?
**Asked at:** commonly asked (no company-specific report found); gap-fill from standard practice.
**What the interviewer is checking:** Do you think in terms of one source of truth?
**Say this in the interview:** "One shared semantic model means the definitions, such as headcount or attrition, live once and every report uses them. We refresh one copy, secure it once and avoid reports that disagree."
**Explain simply:**
- A **semantic model** (formerly called a dataset) is the published data plus relationships and measures.
- Many reports connect to it ("live connection"), so nobody copies the data.
- One refresh schedule, one set of row-level security rules, one definition of each measure.
- Trade-off: report authors cannot freely change the model, and changes affect everyone, so test before publishing.
**Example:** HR, Finance and Recruiting each use `Attrition %` from the same `People` model: all three show 12.4% on the same day.
**DAX / Steps (not run here):** Publish the model from Desktop (**Home > Publish**). In another Desktop file: **Get data > Power BI semantic models**, select it, **Connect** (names from memory, unverified).
**Alternative:** Each team builds its own import model (fast to start, drifts apart); or a composite model extending the shared one (Q52).
**Version / licensing note:** from memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft page was read for this answer). Terminology (semantic model replaces dataset) and licence/permission details, such as Build permission, are from memory, unverified.
**Edge cases:** Authors need Build permission; changing a measure name breaks dependent reports.
**Likely follow-ups:** 1) *Can authors add measures?* Report-level measures yes (from memory). 2) *Where does RLS live?* In the model.
**Common mistakes:** Copying the .pbix per team; changing a shared measure without telling users.

### Q54 ⭐ 🟡 What does the Assume Referential Integrity setting do on a relationship, and when is it safe to turn on?
**Asked at:** commonly asked (no company-specific report found); documented option, mainly for DirectQuery, not in India interview reports seen.
**What the interviewer is checking:** Do you know it is a promise about clean data, used for speed?
**Say this in the interview:** "It tells Power BI that every key in the many side exists in the one side, so queries can use faster inner joins instead of outer joins. It is only safe when that is truly the case, otherwise rows silently disappear."
**Explain simply:**
- **Referential integrity** means no orphan keys (Q50).
- With the setting on, Power BI trusts you and uses inner joins, mainly helping **DirectQuery** sources (from memory).
- If any orphan exists, those fact rows are dropped from results that use the dimension.
**Example:** Costs of 100, 200 and 50 (D99 has no department). Inner join returns 300, left join returns 350.
**Sample data:** Table `Cost`: D1=100, D2=200, D99=50; table `Department`: D1, D2.
**DAX / Steps (not run here):** Model view > double-click relationship > tick **Assume referential integrity** (available for DirectQuery-type relationships; from memory).
**Alternative:** Leave it off (safe, slower), or fix orphans first with an Unknown member (Q50).
**Result:** reproduced with pandas: inner join total 300, left join 350, true total 350.
**Pandas check:**
```python
import pandas as pd
fa = pd.DataFrame({"Dept":["D1","D2","D99"],"Cost":[100,200,50]})
dim = pd.DataFrame({"Dept":["D1","D2"]})
print(fa.merge(dim,on="Dept",how="inner").Cost.sum(), fa.merge(dim,on="Dept",how="left").Cost.sum(), fa.Cost.sum())
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
300 350 350
```
**Version / licensing note:** from memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft page was read for this answer). Option availability and behaviour are from memory, unverified.
**Edge cases:** Later data loads may introduce orphans; add a check; the option applies to the relationship, not the table.
**Likely follow-ups:** 1) *Import mode?* Little or no benefit (from memory). 2) *Risk?* Silent drop of rows.
**Common mistakes:** Ticking it for speed without checking orphans.

### Q55 ⭐ 🔴 An employee changes department during the year. How would you model this so history stays correct (slowly changing dimension Type 2)?
**Asked at:** commonly asked (no company-specific report found); advanced topic, not in any India interview report seen.
**What the interviewer is checking:** Can you keep history, not overwrite it?
**Say this in the interview:** "I use a Type 2 slowly changing dimension: each change creates a new row with a surrogate key and start and end dates. Facts link to the row valid on their date, so past costs stay in the old department."
**Explain simply:**
- **Slowly changing dimension (SCD)** is a dimension whose attributes change occasionally. **Type 1** overwrites the value, losing history. **Type 2** adds a new row.
- Columns: surrogate key `EmpKey`, business ID `EmpID`, `Dept`, `From`, `To`; the current row has a far-future `To`.
- The fact table should store the correct `EmpKey` (assign it in the ETL or Power Query using the date range) so a normal relationship works.
**Example:** E1 moved Sales to Support on 1 Jul 2026. Payroll cost 60,000 in March and May stays under Sales; August 65,000 goes to Support.
**Sample data:** Table `EmployeeDim` and `Payroll`

| EmpKey | EmpID | Dept | From | To |
|---|---|---|---|---|
| 1 | E1 | Sales | 2025-01-01 | 2026-06-30 |
| 2 | E1 | Support | 2026-07-01 | 2099-12-31 |
| 3 | E2 | Sales | 2025-01-01 | 2099-12-31 |

Payroll rows: E1 2026-03-31 60000; E1 2026-05-31 60000; E2 2026-05-31 45000; E1 2026-08-31 65000.
**DAX / Steps (not run here):**
```m
// Power Query: bring the right EmpKey into the fact (range join)
= Table.AddColumn(Payroll, "EmpKey", each
    Table.SelectRows(EmployeeDim, (d) => d[EmpID] = [EmpID] and d[From] <= [Date] and d[To] >= [Date]){0}[EmpKey], Int64.Type)
```
Then relate `Payroll[EmpKey]` to `EmployeeDim[EmpKey]`, and use `DISTINCTCOUNT ( EmployeeDim[EmpID] )` for headcount so one person is not counted twice.
**Alternative:** Do the assignment in SQL at the source (usually faster), or Type 1 if history does not matter.
**Result:** reproduced with pandas: cost by department Sales 165,000, Support 65,000. If you overwrote (Type 1), E1 would be all Support: Sales 45,000, Support 185,000.
**Pandas check:**
```python
import pandas as pd
d = pd.DataFrame({"EmpKey":[1,2,3],"EmpID":["E1","E1","E2"],"Dept":["Sales","Support","Sales"],
  "From":pd.to_datetime(["2025-01-01","2026-07-01","2025-01-01"]),"To":pd.to_datetime(["2026-06-30","2099-12-31","2099-12-31"])})
pay2 = pd.DataFrame({"EmpID":["E1","E1","E2","E1"],"Date":pd.to_datetime(["2026-03-31","2026-05-31","2026-05-31","2026-08-31"]),"Cost":[60000,60000,45000,65000]})
x = pay2.merge(d,on="EmpID"); x = x[(x.Date>=x.From)&(x.Date<=x.To)]
print("Type 2:"); print(x.groupby("Dept").Cost.sum().to_string())
t1 = pay2.merge(pd.DataFrame({"EmpID":["E1","E2"],"Dept":["Support","Sales"]}),on="EmpID")
print("Type 1 (overwritten):"); print(t1.groupby("Dept").Cost.sum().to_string())
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
Type 2:
Dept
Sales      165000
Support     65000
Type 1 (overwritten):
Dept
Sales       45000
Support    185000
```
**Version / licensing note:** from memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft page was read for this answer). SCD Type 1/2 descriptions are from the Microsoft star schema guidance named in the sources file but not read here; the M code is not run here.
**Edge cases:** Overlapping date ranges duplicate rows; gaps lose rows; counting rows instead of distinct EmpID inflates headcount.
**Likely follow-ups:** 1) *Why a surrogate key?* EmpID repeats across versions. 2) *Type 3?* Adds a column for the previous value.
**Common mistakes:** Joining facts on EmpID (duplicates cost); counting rows as headcount.

### Q56 ⭐ 🔴 How would you model an employee and manager hierarchy where each employee reports to another employee?
**Asked at:** commonly asked (no company-specific report found); gap-fill from standard practice.
**What the interviewer is checking:** Do you know parent-child hierarchies need flattening with PATH?
**Say this in the interview:** "Power BI cannot follow a self-reference directly, so I build a PATH column from EmployeeID and ManagerID, then pull each level with PATHITEM into separate columns and make a hierarchy from them."
**Explain simply:**
- A **parent-child hierarchy** is one table where each row points to its manager's row.
- `PATH` returns the chain from the top to this person as text, such as `1|2|4`.
- `PATHITEM` picks the nth person from that chain; `LOOKUPVALUE` turns the ID into a name.
- Each level becomes a column; people with shorter chains get blanks at the lower levels.
**Example:** Asha (top), Ravi and Meena under Asha, Kiran under Ravi, Zoya under Kiran.
**Sample data:** Table `Employee`

| EmpID | Name | ManagerID |
|---|---|---|
| 1 | Asha | blank |
| 2 | Ravi | 1 |
| 3 | Meena | 1 |
| 4 | Kiran | 2 |
| 5 | Zoya | 4 |

**DAX / Steps (not run here):**
```dax
Path = PATH ( Employee[EmpID], Employee[ManagerID] )
Depth = PATHLENGTH ( Employee[Path] )
Level 1 = LOOKUPVALUE ( Employee[Name], Employee[EmpID], PATHITEM ( Employee[Path], 1, INTEGER ) )
Level 2 = LOOKUPVALUE ( Employee[Name], Employee[EmpID], PATHITEM ( Employee[Path], 2, INTEGER ) )
```
Steps: add calculated columns (**Table tools > New column**), then in the Data pane drag Level 2 onto Level 1 to build a hierarchy.
**Alternative:** Flatten in Power Query or SQL with a recursive query, or use a Manager name column for a one-level view.
**Result:** reproduced with pandas: paths `1`, `1|2`, `1|3`, `1|2|4`, `1|2|4|5`; Zoya has depth 4 with levels Asha, Ravi, Kiran, Zoya; Meena has levels Asha, Meena, blank.
**Pandas check:**
```python
import pandas as pd
e = pd.DataFrame({"EmpID":[1,2,3,4,5],"Name":["Asha","Ravi","Meena","Kiran","Zoya"],"ManagerID":[None,1,1,2,4]})
mgr = dict(zip(e.EmpID, e.ManagerID))
def path(i):                      # same idea as DAX PATH: top person first
    p = [i]
    while pd.notna(mgr[p[0]]): p.insert(0, int(mgr[p[0]]))
    return p
e["Path"] = e.EmpID.map(lambda i: "|".join(map(str, path(i)))); e["Depth"] = e.Path.str.count(r"\|")+1
name = dict(zip(e.EmpID, e.Name))
for n in (1,2,3,4): e[f"Level {n}"] = e.Path.map(lambda s: name[int(s.split("|")[n-1])] if len(s.split("|"))>=n else None)
print(e.drop(columns="ManagerID").to_string(index=False))
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
 EmpID  Name    Path  Depth Level 1 Level 2 Level 3 Level 4
     1  Asha       1      1    Asha     NaN     NaN     NaN
     2  Ravi     1|2      2    Asha    Ravi     NaN     NaN
     3 Meena     1|3      2    Asha   Meena     NaN     NaN
     4 Kiran   1|2|4      3    Asha    Ravi   Kiran     NaN
     5  Zoya 1|2|4|5      4    Asha    Ravi   Kiran    Zoya
```
**Version / licensing note:** from memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft page was read for this answer). `PATH`, `PATHITEM`, `LOOKUPVALUE` are from memory (not read here); `PATH` needs a unique ID column.
**Edge cases:** A cycle (A manages B, B manages A) makes `PATH` fail; the top person has a blank manager; unequal depths leave blank levels.
**Likely follow-ups:** 1) *How many levels?* Pick the max depth (`MAX ( Employee[Depth] )`). 2) *Why not recursion?* DAX has none.
**Common mistakes:** Hard-coding a depth smaller than the real one; forgetting `INTEGER` in `PATHITEM`.

### Q57 ⭐ 🔴 Sales targets are stored by category and year, but sales are stored by product and day. How do you relate them?
**Asked at:** commonly asked (no company-specific report found); advanced, from the many-to-many/higher-grain scenario in Microsoft guidance as listed in the sources file.
**What the interviewer is checking:** Can you relate tables at different grains through shared dimensions?
**Say this in the interview:** "I do not relate targets to sales directly. I add a Category dimension and a Year (or date) dimension, relate both Sales and Targets to them, and slicers use those shared tables. A measure guards against showing targets at a finer grain."
**Explain simply:**
- **Grain** is what one row means. Sales: one product on one day. Targets: one category in one year.
- Relate `Product` to `Category` (a category column on the product dimension), and relate Targets to the same Category dimension.
- For the date side, a `Year` table (or a date table used by year) relates to Targets at year level.
- Targets must not be shown by product or day, since it would be repeated or wrong.
**Example:** Laptops sold 1,100 against a 1,000 target (110%), Phones 400 against 500 (80%).
**Sample data:** Table `Sales` (Product P1, P2 = Laptops, P3 = Phones)

| Product | Date | Amt |
|---|---|---|
| P1 | 2026-01-05 | 300 |
| P2 | 2026-02-10 | 200 |
| P3 | 2026-03-12 | 400 |
| P1 | 2026-06-01 | 350 |
| P2 | 2026-07-04 | 250 |

Table `Targets`: Laptops 2026 = 1000; Phones 2026 = 500.
**DAX / Steps (not run here):**
```dax
Sales = SUM ( Sales[Amt] )
Target = SUM ( Targets[Target] )
Target (safe) = IF ( ISFILTERED ( Product[Product] ) || ISFILTERED ( 'Date'[Date] ), BLANK (), [Target] )
Achievement % = DIVIDE ( [Sales], [Target (safe)] )
```
Model: `Category` (one) to `Product` and to `Targets`; `Year` (one) to `Date` and to `Targets`.
**Alternative:** Spread the target evenly to product-day rows in Power Query (allocation, if the business agrees), or use `TREATAS` to push category and year onto Sales (Q60).
**Result:** reproduced with pandas: Laptops 1,100 vs 1,000 (1.1), Phones 400 vs 500 (0.8); grand totals 1,500 vs 1,500. Joining targets directly to sales rows would repeat the targets and total 4,500.
**Pandas check:**
```python
import pandas as pd
prodmap = pd.DataFrame({"Product":["P1","P2","P3"],"Category":["Laptops","Laptops","Phones"]})
sales = pd.DataFrame({"Product":["P1","P2","P3","P1","P2"],"Date":pd.to_datetime(["2026-01-05","2026-02-10","2026-03-12","2026-06-01","2026-07-04"]),"Amt":[300,200,400,350,250]})
sales = sales.merge(prodmap,on="Product"); sales["Year"] = sales.Date.dt.year
tg = pd.DataFrame({"Category":["Laptops","Phones"],"Year":[2026,2026],"Target":[1000,500]})
a = sales.groupby(["Category","Year"]).Amt.sum().reset_index().merge(tg,on=["Category","Year"])
a["Achievement"] = a.Amt/a.Target
print(a.to_string(index=False)); print("Totals:", a.Amt.sum(), a.Target.sum())
print("Naive row-level join, summed target:", sales.merge(tg,on=["Category","Year"]).Target.sum())
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
Category  Year  Amt  Target  Achievement
 Laptops  2026 1100    1000          1.1
  Phones  2026  400     500          0.8
Totals: 1500 1500
Naive row-level join, summed target: 4500
```
**Version / licensing note:** from memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft page was read for this answer). Guidance and DAX function behaviour from memory; the many-to-many page was not read here.
**Edge cases:** Month slicer on targets: the year target repeats for each month unless you allocate; fiscal vs calendar year.
**Likely follow-ups:** 1) *Why not a many-to-many relationship?* Q58. 2) *Quarterly targets?* Add them at a month or quarter grain.
**Common mistakes:** Relating on Category text in both fact tables; showing targets by product.

### Q58 ⭐ 🔴 Why is relating two fact tables directly with a many-to-many relationship not recommended, and what is the alternative?
**Asked at:** commonly asked (no company-specific report found); the many-to-many topic appears in Weekday's 2026 list and a Deloitte-tagged set whose attribution is unverified (per sources file).
**What the interviewer is checking:** Do you understand how many-to-many inflates numbers and how shared dimensions fix it?
**Say this in the interview:** "A direct many-to-many between facts matches every row with every matching row, so numbers multiply or become confusing. I relate both facts to shared dimension tables, or a bridge table, so each fact is filtered cleanly."
**Explain simply:**
- Both sides have repeated keys, so a department with 2 hire rows and 3 exit rows joins into 6 rows.
- Results depend on the filter you happen to apply, and are hard to explain.
- Alternative: a small `Department` dimension with one row per department; relate both facts to it (one-to-many each).
- For true many-to-many (an employee in several projects), use a **bridge table** of the valid pairs.
**Example:** Hires: A 2, B 1. Exits: A 3, B 1. A naive row-level join says 7 hires and 7 exits instead of 3 and 4.
**Sample data:** Tables `Hires` and `Exits`

| Dept | Hires |
|---|---|
| A | 1 |
| A | 1 |
| B | 1 |

| Dept | Exits |
|---|---|
| A | 1 |
| A | 1 |
| A | 1 |
| B | 1 |

**DAX / Steps (not run here):**
```dax
Hires = SUM ( Hires[Hires] )
Exits = SUM ( Exits[Exits] )
```
Model: `Department` (unique list, built in Power Query by appending both Dept columns and removing duplicates) to `Hires[Dept]` and `Exits[Dept]`, Single direction. Slicers use `Department[Dept]`.
**Alternative:** A bridge table, or `TREATAS` in measures (Q60).
**Result:** reproduced with pandas: row-level join returns 7 rows and sums of 7 and 7; correct totals are 3 hires and 4 exits; grouped by department: Hires A=2, B=1; Exits A=3, B=1.
**Pandas check:**
```python
import pandas as pd
hires = pd.DataFrame({"Dept":["A","A","B"],"Hires":[1,1,1]})
exits = pd.DataFrame({"Dept":["A","A","A","B"],"Exits":[1,1,1,1]})
mm = hires.merge(exits,on="Dept")
print("Row-level join: rows", len(mm), "| Hires", mm.Hires.sum(), "| Exits", mm.Exits.sum())
print("Correct:", hires.Hires.sum(), "hires,", exits.Exits.sum(), "exits")
print(hires.groupby("Dept").Hires.sum().to_dict(), exits.groupby("Dept").Exits.sum().to_dict())
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
Row-level join: rows 7 | Hires 7 | Exits 7
Correct: 3 hires, 4 exits
{'A': 2, 'B': 1} {'A': 3, 'B': 1}
```
**Version / licensing note:** from memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft page was read for this answer). Power BI's actual many-to-many engine behaves differently from a pandas row join (it filters by distinct keys). My pandas figure shows why row-level matching is risky, not exactly what Power BI would display; the sources file notes Microsoft pages disagree on service support for many-to-many, so I would re-check the live page before stating support. Not verified here.
**Edge cases:** Blank keys; totals in many-to-many may not add up.
**Likely follow-ups:** 1) *When is many-to-many acceptable?* Higher-grain data like targets, with care. 2) *Bridge direction?* Bridge to facts one-to-many.
**Common mistakes:** Turning on bi-directional filters to "fix" it; joining facts to each other.

### Q59 ⭐ 🔴 What does the CROSSFILTER function do, and when would you use it in a measure?
**Asked at:** commonly asked (no company-specific report found); advanced DAX, not in any India interview report seen.
**What the interviewer is checking:** Can you change filter direction for one measure instead of the whole model?
**Say this in the interview:** "CROSSFILTER sets the filter direction of an existing relationship inside CALCULATE for that measure only. I use it to turn on both-way filtering just where needed, instead of making the relationship bi-directional for everything."
**Explain simply:**
- **Cross-filter direction** is which way a filter travels along a relationship.
- Syntax: `CROSSFILTER ( column1, column2, direction )` with direction `Both`, `OneWay` or `None`. It works only inside functions that take a filter, like `CALCULATE`.
- The relationship must already exist.
- Use `None` to switch a relationship off for one measure.
**Example:** Departments: Sales, IT, HR. Employees only exist in Sales (2) and IT (2). A measure counting departments that have employees returns 2 of 3.
**Sample data:** Table `Department` (Sales, IT, HR) and `Employee`

| EmpID | Dept |
|---|---|
| 1 | Sales |
| 2 | Sales |
| 3 | IT |
| 4 | IT |

**DAX / Steps (not run here):**
```dax
Depts With Employees =
CALCULATE (
    DISTINCTCOUNT ( Department[Dept] ),
    CROSSFILTER ( Employee[Dept], Department[Dept], Both )
)
```
Click-path: none; this is typed as a measure (**Modeling > New measure**).
**Alternative:** Set the relationship to bi-directional in Model view (affects everything) or use `COUNTROWS ( FILTER ( VALUES ( Department[Dept] ), CALCULATE ( COUNTROWS ( Employee ) ) > 0 ) )`.
**Result:** reproduced with pandas logic: 2 departments have employees out of 3. (`Employee` rows 4, departments 3.)
**Pandas check:**
```python
import pandas as pd
dp = pd.DataFrame({"Dept":["Sales","IT","HR"]})
emp2 = pd.DataFrame({"EmpID":[1,2,3,4],"Dept":["Sales","Sales","IT","IT"]})
print("depts with employees:", emp2.Dept.nunique(), "of", len(dp))
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
depts with employees: 2 of 3
```
**Version / licensing note:** from memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft page was read for this answer). Syntax from memory; Microsoft Learn: CROSSFILTER function (DAX) could not be fetched, so unverified.
**Edge cases:** Fails for a missing relationship; does not work in DirectQuery with some settings (from memory); a one-to-one relationship already filters both ways.
**Likely follow-ups:** 1) *Difference from USERELATIONSHIP?* That activates an inactive relationship. 2) *Performance?* Both-way filters can be slower.
**Common mistakes:** Using it outside CALCULATE; passing columns in a relationship that does not exist.

### Q60 ⭐ 🔴 What does TREATAS do, and how does it create a virtual relationship?
**Asked at:** commonly asked (no company-specific report found); advanced DAX, not in any India interview report seen.
**What the interviewer is checking:** Can you apply a filter from one table to another without a physical relationship?
**Say this in the interview:** "TREATAS takes a list of values and says: treat these as values of that column in another table. Inside CALCULATE that filters the other table as if there were a relationship, only for that measure."
**Explain simply:**
- **Virtual relationship** means a filter connection that exists only inside one measure.
- Syntax: `TREATAS ( table_expression, column1 [, column2 ...] )`: the columns of the first argument are mapped in order to the target columns.
- Useful with disconnected tables, slicers, or two tables that cannot be related cleanly (different grain, many-to-many).
**Example:** A shortlist table of employee IDs 2, 4 and 9 filters a `Sales` table: 200 + 400 = 600. ID 9 has no sales and is ignored.
**Sample data:** Table `Sales`, disconnected table `Shortlist`

| EmpID | Amt |
|---|---|
| 1 | 100 |
| 2 | 200 |
| 3 | 300 |
| 4 | 400 |
| 5 | 500 |

`Shortlist[EmpID]` has 2, 4, 9.
**DAX / Steps (not run here):**
```dax
Sales for Shortlist =
CALCULATE (
    SUM ( Sales[Amt] ),
    TREATAS ( VALUES ( Shortlist[EmpID] ), Sales[EmpID] )
)
```
**Alternative:** A real relationship, or `INTERSECT`/`FILTER` with `CONTAINS` (older approach), or `KEEPFILTERS` variants.
**Result:** reproduced with pandas: 600.
**Pandas check:**
```python
import pandas as pd
sl = pd.DataFrame({"EmpID":[1,2,3,4,5],"Amt":[100,200,300,400,500]})
sel = [2,4,9]    # Shortlist[EmpID]; 9 has no sales row
print(sl[sl.EmpID.isin(sel)].Amt.sum())
```
Printed output (real run, pandas 3.0.5; reproduces the expected answer, not a DAX engine):
```
600
```
**Version / licensing note:** from memory, unverified (learn.microsoft.com could not be reached from this session, so no Microsoft page was read for this answer). Syntax from memory; Microsoft Learn: TREATAS function (DAX) could not be fetched, so unverified.
**Edge cases:** Data types must match; values not in the target are ignored; column order must match.
**Likely follow-ups:** 1) *TREATAS vs USERELATIONSHIP?* USERELATIONSHIP needs an existing inactive relationship, TREATAS does not. 2) *Cost?* Very large value lists can be slow.
**Common mistakes:** Wrong column order; mismatched types; expecting it to filter outside the measure.
