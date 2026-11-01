# Book 4 — Power BI & Visualization | Part 4: DAX basics: calculated column vs measure, SUM vs SUMX, COUNT, CALCULATE 🟡

**Target:** 75 questions | **Actual:** 75 questions
**Scope:** DAX fundamentals for a beginner analyst: calculated column vs measure, SUM vs SUMX and iterators, the COUNT family, CALCULATE, row vs filter context basics, DIVIDE, and practical write-the-measure tasks. ALL/ALLEXCEPT, time intelligence and RANKX are Part 5.

### Q1 ⭐⭐⭐ 🟢 What is DAX, and where is it used in Power BI?
**Asked at:** Wipro (2023 Bangalore-Rural report: DAX SUM, SUMX, AVG) and Deloitte (Sept 2025 Power BI round: SUM vs SUMX), per the Part 4 sources file; both are single reports. Otherwise commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know DAX is the formula language of the data model, not a data-cleaning tool?
**Say this in the interview:** "DAX, Data Analysis Expressions, is the formula language Power BI uses to calculate numbers on top of the data model: measures like total sales or attrition rate, calculated columns, and calculated tables. Power Query (M) prepares the data; DAX analyses it."
**Explain simply:**
- DAX is like Excel formulas, but it works on whole tables and columns, not single cells like B2.
- Three places you write it: **measures** (calculated when a visual needs them), **calculated columns** (a new column stored in a table) and **calculated tables**. Row-level security rules also use DAX filters.
- DAX is also used in Excel's Power Pivot and in Analysis Services models, so the skill carries over.
- Typical shape: `Measure Name = FUNCTION(Table[Column])`.
**Example:** An HR dashboard shows "Attrition % by department". The data has only one row per employee. A DAX measure divides leavers by average headcount, and Power BI re-runs it for every department.
**DAX / Steps:** Not run here (no Power BI available). A tiny example:
```dax
Total Payroll Cost = SUM ( Payroll[PayrollCost] )
```
**Alternative:** For a one-off number you could drag the column into a visual and let Power BI auto-sum it (an implicit measure, see Q18), but a written DAX measure is reusable.
**Version / licensing note:** From memory, unverified (learn.microsoft.com could not be reached from this session). Power BI Desktop, where you write DAX, is believed to be free and Windows-only; check Microsoft's system-requirements page before quoting.
**Edge cases:** DAX does not clean or reshape source data (use Power Query for that); it cannot edit data, only calculate.
**Likely follow-ups:**
- *DAX vs M?* M shapes data before load; DAX calculates after load (Q22).
- *Is DAX a database query language like SQL?* It is a calculation language, though DAX queries exist.
**Common mistakes:** Saying DAX "cleans data", or treating it as Excel with cell references.

### Q2 ⭐⭐⭐ 🟢 What is the difference between a calculated column and a measure?
**Asked at:** Commonly asked (no company-specific report found); it tops the Weekday 2026 India prep list in the sources file.
**What the interviewer is checking:** Do you know when each is computed, where it is stored, and which to choose?
**Say this in the interview:** "A calculated column is computed row by row when the data refreshes and stored in the table. A measure is computed on the fly when a visual asks, using whatever filters are active, and stores nothing. Anything you sum or average goes in a measure; anything you slice or group by can be a column."
**Explain simply:**
- **Calculated column:** has a value for every row, uses *row context* (one row at a time, Q8), takes memory, can be used on a slicer, axis or filter.
- **Measure:** one value per cell of a visual, uses *filter context* (Q7), takes almost no memory, reacts to slicers.
- Rule of thumb: "Need it to filter or group? Column. Need it to total or compare? Measure."
**Example:** Column: `Salary Band` (Low/Mid/High) for each of 20,000 employees. Measure: `Average Salary`, which differs for each department, slicer click and month.
**DAX / Steps:** Not run here.
```dax
Line Total (column)  = Sales[Quantity] * Sales[UnitPrice]
Total Revenue (measure) = SUMX ( Sales, Sales[Quantity] * Sales[UnitPrice] )
```
**Alternative:** You can often avoid a column by using an iterator measure (SUMX, Q5); you can create a column in Power Query instead, which is usually better for the data model if the logic is row-level.
**Version / licensing note:** From memory, unverified.
**Edge cases:** A column's total is fixed at refresh; a measure re-evaluates with the filters. Do not average a stored "ratio" column across rows; compute ratios in a measure.
**Likely follow-ups:**
- *Which uses more memory?* Calculated columns (Q26).
- *Can a measure be on a slicer?* Not directly; only columns can.
**Common mistakes:** Creating `Total Sales` as a column and then wondering why it never changes with slicers.

### Q3 ⭐⭐⭐ 🟢 How do you create a calculated column and a measure in Power BI Desktop?
**Asked at:** Commonly asked (no company-specific report found).
**What the interviewer is checking:** Hands-on familiarity with Desktop.
**Say this in the interview:** "Select the table in the Data pane, choose New column or New measure on the Table tools or Home ribbon, then type `Name = formula` in the formula bar and press Enter."
**Explain simply:**
- Both start the same way: pick the table you want it to live in. A measure's home table does not change its result, but it organises your fields.
- The formula bar takes `Name = expression`. IntelliSense (auto-suggest) completes table and column names.
- New items appear in the Data pane (column icon vs calculator icon).
**Example:** Add `Is Late` to the Attendance table as a column; add `Late Count` as a measure and put it in a card.
**DAX / Steps:** Not run here; the click-path is from memory and the labels may differ slightly between Desktop releases.
1. Open Power BI Desktop, go to **Report view** or **Table view**.
2. Click the table in the **Data** pane.
3. Ribbon: **Home** tab > **Calculations** group > **New measure** (or **Table tools** / **Column tools** tab > **New column**). Right-clicking the table also shows both commands.
4. Type in the formula bar, e.g. `Headcount = COUNTROWS ( Employees )`, press **Enter**.
5. Drag the new field onto a visual.
**Alternative:** Create the column in Power Query (Home > Transform data > Add Column) instead of DAX, or use **Quick measure** (Q23).
**Version / licensing note:** From memory, unverified. Desktop is believed free; DAX authoring in the Power BI Service (web model editing) is unverified: do not claim it either way.
**Edge cases:** A measure with the same name as a column in the same table will clash. DirectQuery models restrict some column DAX.
**Likely follow-ups:**
- *Can I rename it?* Yes: edit the formula's name or rename in the Data pane.
- *Where do I see the DAX again?* Click the field; the formula bar shows it.
**Common mistakes:** Making a measure when the task is a slicer field; typing a measure into a visual's "Add data" instead of via New measure.

### Q4 ⭐⭐⭐ 🟢 Should "Salary Band" be a calculated column or a measure? Why?
**Asked at:** Commonly asked (no company-specific report found); a gap-fill style practical question.
**What the interviewer is checking:** Can you apply the column-vs-measure rule to a real field?
**Say this in the interview:** "A calculated column, because each employee belongs to exactly one band, and I want to use the band as a slicer, a chart axis and a filter. A measure cannot be placed on an axis or slicer."
**Explain simply:**
- The band is a property of one row (that employee's salary), so row-by-row logic fits.
- Columns are what you group and filter by; measures are what you total.
- If the band should change by filter (e.g. relative to the selected department's average), then a measure may be needed, but that is rare.
**Example:** Bands: Low below 25,000, Mid 25,000-49,999, High 50,000 and above. Headcount by band is then a simple COUNTROWS in a chart.
**Sample data:** Table `Employees`
| EmpID | Salary |
|---|---|
| E101 | 18000 |
| E102 | 32000 |
| E103 | 45000 |
| E104 | 60000 |
| E105 | 95000 |

**DAX / Steps:** Not run here.
```dax
Salary Band =
SWITCH (
    TRUE (),
    Employees[Salary] < 25000, "Low",
    Employees[Salary] < 50000, "Mid",
    "High"
)
```
**Alternative:** Build the band in Power Query with a Conditional Column (Add Column > Conditional Column), or create a small `Bands` lookup table.
**Result:** Reproduced with pandas (not a DAX engine): E101 Low, E102 Mid, E103 Mid, E104 High, E105 High.
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"EmpID":["E101","E102","E103","E104","E105"],"Salary":[18000,32000,45000,60000,95000]})
emp["SalaryBand"] = pd.cut(emp["Salary"], [0,24999,49999,float("inf")], labels=["Low","Mid","High"])
print(emp)
```
Output:
```
  EmpID  Salary SalaryBand
0  E101   18000        Low
1  E102   32000        Mid
2  E103   45000        Mid
3  E104   60000       High
4  E105   95000       High
```
**Version / licensing note:** From memory, unverified (SWITCH(TRUE(), ...) page not fetched).
**Edge cases:** A blank salary is, from memory (unverified), treated like 0 in a `<` comparison and would land in "Low"; add an explicit blank check. Boundary values (exactly 25,000) go to the next band.
**Likely follow-ups:**
- *Does the band update when data refreshes?* Yes, at refresh.
- *Why not a measure?* Cannot be a slicer/axis field.
**Common mistakes:** Writing `IF` with overlapping thresholds; forgetting a blank-salary rule.

### Q5 ⭐⭐⭐ 🟢 What is the difference between SUM and SUMX?
**Asked at:** Deloitte (Sept 2025 Power BI round: SUM vs SUMX) and Wipro (2023 Bangalore-Rural: SUM, SUMX), per the sources file; single reports each.
**What the interviewer is checking:** Do you understand aggregator vs iterator?
**Say this in the interview:** "SUM adds up one existing column. SUMX goes through a table row by row, evaluates an expression for each row, then adds the results. I use SUMX when the number I want does not exist as a column, like Quantity times Price."
**Explain simply:**
- **SUM(column):** quick, one column only.
- **SUMX(table, expression):** an *iterator*: it visits each row, calculates, then totals.
- SUM is really shorthand for SUMX over one column. Microsoft's guidance (per the sources file) says use SUM when you do not need row-level calculation or filtering.
**Example:** Orders have Quantity and UnitPrice but no Amount column. SUM cannot multiply; SUMX can.
**Sample data:** Table `Sales`
| Region | Quantity | UnitPrice | Amount |
|---|---|---|---|
| North | 2 | 500 | 1000 |
| North | 1 | 800 | 800 |
| South | 3 | 500 | 1500 |
| South | 10 | 20 | 200 |
| East | 2 | 800 | 1600 |

**DAX / Steps:** Not run here.
```dax
Total Amount  = SUM ( Sales[Amount] )
Total Revenue = SUMX ( Sales, Sales[Quantity] * Sales[UnitPrice] )
Big Order Revenue = SUMX ( FILTER ( Sales, Sales[Quantity] >= 3 ), Sales[Quantity] * Sales[UnitPrice] )
```
**Alternative:** Add a `LineTotal` calculated column and SUM it (more memory).
**Result:** Reproduced with pandas: Total Amount 5100; Total Revenue 5100; Big Order Revenue 1700.
**Pandas check:**
```python
import pandas as pd
sales = pd.DataFrame({"Region":["North","North","South","South","East"],
                      "Quantity":[2,1,3,10,2],"UnitPrice":[500,800,500,20,800]})
sales["Amount"] = sales["Quantity"] * sales["UnitPrice"]
print("SUM(Amount)             =", sales["Amount"].sum())
print("SUMX(Qty*Price)         =", (sales["Quantity"] * sales["UnitPrice"]).sum())
print("SUMX(FILTER Qty>=3)     =", (sales["Quantity"] * sales["UnitPrice"])[sales["Quantity"] >= 3].sum())
```
Output: `5100`, `5100`, `1700`.
**Version / licensing note:** The sources file records Microsoft Learn's SUMX page (fetched by the research phase, not re-fetched here). I could not reach learn.microsoft.com; behaviour on blanks/text is from memory, unverified.
**Edge cases:** SUMX ignores blank/text results for a row; rows where one input is blank may yield blank (not zero).
**Likely follow-ups:**
- *Is SUMX slower?* Marginally on huge tables; usually fine.
- *Other X functions?* AVERAGEX, MINX, MAXX, COUNTX (Q17).
**Common mistakes:** `SUM(Sales[Quantity] * Sales[Price])` (Q19); using SUMX where plain SUM works.

### Q6 ⭐⭐⭐ 🟢 What is the difference between COUNT, COUNTA, COUNTROWS and DISTINCTCOUNT?
**Asked at:** Commonly asked (no company-specific report found); the COUNT family is on the Weekday 2026 list in the sources file.
**What the interviewer is checking:** Do you know exactly what each one counts?
**Say this in the interview:** "COUNT counts non-blank numbers or dates in a column; COUNTA counts non-blank values of any type; COUNTROWS counts rows in a table; DISTINCTCOUNT counts the different values in a column."
**Explain simply:**
- **COUNT(column):** skips blanks and (from memory) does not count text-only columns.
- **COUNTA(column):** counts anything not blank: text, numbers, dates, TRUE/FALSE.
- **COUNTROWS(table):** counts rows, blank or not. Preferred for "how many records".
- **DISTINCTCOUNT(column):** counts each value once; from memory, a blank counts as one value if present.
**Example:** 6 employees; some have no bonus recorded.
**Sample data:** Table `Employees`
| EmpID | EmpName | Dept | Bonus |
|---|---|---|---|
| E101 | Asha | HR | 5000 |
| E102 | Ravi | IT | (blank) |
| E103 | Meena | IT | 3000 |
| E104 | Kiran | Sales | (blank) |
| E105 | Sana | Sales | 4000 |
| E106 | Vijay | Sales | 5000 |

**DAX / Steps:** Not run here.
```dax
Bonus Count  = COUNT ( Employees[Bonus] )
Name Count   = COUNTA ( Employees[EmpName] )
Employees    = COUNTROWS ( Employees )
Dept Count   = DISTINCTCOUNT ( Employees[Dept] )
```
**Alternative:** `COUNTROWS(VALUES(Employees[Dept]))` also counts distinct departments (VALUES includes a blank row if one exists).
**Result:** Reproduced with pandas: COUNT 4, COUNTA 6, COUNTROWS 6, DISTINCTCOUNT(Dept) 3.
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"EmpID":["E101","E102","E103","E104","E105","E106"],
    "EmpName":["Asha","Ravi","Meena","Kiran","Sana","Vijay"],
    "Dept":["HR","IT","IT","Sales","Sales","Sales"],
    "Bonus":[5000,None,3000,None,4000,5000]})
print("COUNT(Bonus)          =", emp["Bonus"].notna().sum())
print("COUNTA(EmpName)       =", emp["EmpName"].notna().sum())
print("COUNTROWS             =", len(emp))
print("DISTINCTCOUNT(Dept)   =", emp["Dept"].nunique())
print("DISTINCTCOUNT(Bonus)  =", emp["Bonus"].nunique(dropna=False), "(blank counted as a value)")
```
Output: 4, 6, 6, 3, and 4 (3 distinct bonus amounts plus blank, shown only to illustrate the blank rule).
**Version / licensing note:** From memory, unverified. The sources file flags that a community thread contradicted documented blank handling for DISTINCTCOUNT and says to verify; I could not (learn.microsoft.com unreachable), so treat the blank rule as unverified.
**Edge cases:** Blank vs zero: a bonus of 0 is counted by COUNT; blank is not. Duplicates inflate COUNTROWS but not DISTINCTCOUNT.
**Likely follow-ups:**
- *Why COUNTROWS over COUNT?* Q27 (clearer intent).
- *Unique employees?* DISTINCTCOUNT(EmpID) (Q11).
**Common mistakes:** Using COUNT on a text column and getting blank/zero; counting a fact table's employee column with COUNTROWS when employees repeat monthly.

### Q7 ⭐⭐⭐ 🟢 What is filter context in DAX?
**Asked at:** Commonly asked (no company-specific report found); the Weekday 2026 guide in the sources file calls it a deciding concept.
**What the interviewer is checking:** Do you understand why the same measure gives different numbers in different places?
**Say this in the interview:** "Filter context is the set of filters currently applied to the data when a measure runs: slicers, page and report filters, the row and column of the visual, and filters inside CALCULATE. The measure is evaluated on whatever rows survive those filters."
**Explain simply:**
- Every cell in a chart/table has its own filter context (e.g. Region = South).
- Slicer selections add to it; CALCULATE can change it (Q9).
- A measure itself never changes; the filters around it do.
**Example:** `Total Sales` shows 5,100 in a card, 1,700 in the South row, and 2,500 when the slicer is set to Tech.
**Sample data:** Table `Sales`
| Region | Category | Amount |
|---|---|---|
| North | Tech | 1000 |
| North | Furniture | 800 |
| South | Tech | 1500 |
| South | Stationery | 200 |
| East | Furniture | 1600 |

**DAX / Steps:** Not run here.
```dax
Total Sales = SUM ( Sales[Amount] )
```
**Alternative:** None needed; it is a concept. You can show it by dropping the same measure in a card, a table by Region and with a slicer.
**Result:** Reproduced with pandas: grand total 5100; East 1600, North 1800, South 1700; North+Tech 1000; slicer Tech 2500.
**Pandas check:**
```python
import pandas as pd
sales = pd.DataFrame({"Region":["North","North","South","South","East"],
                      "Category":["Tech","Furniture","Tech","Stationery","Furniture"],
                      "Amount":[1000,800,1500,200,1600]})
print("Grand total:", sales["Amount"].sum())
print(sales.groupby("Region")["Amount"].sum())
print("Region=North & Category=Tech:", sales.query("Region=='North' and Category=='Tech'")["Amount"].sum())
print("Slicer Category=Tech:", sales[sales.Category=="Tech"]["Amount"].sum())
```
Output: 5100; East 1600, North 1800, South 1700; 1000; 2500.
**Version / licensing note:** From memory, unverified.
**Edge cases:** Filters flow from dimension tables to the fact table through relationships; with no relationship nothing filters (Q16). Total rows have no row filter, so they use the overall context.
**Likely follow-ups:**
- *Row context vs filter context?* Q12.
- *How do you change it?* CALCULATE.
**Common mistakes:** Thinking the formula "remembers" a region; forgetting hidden page/report filters.

### Q8 ⭐⭐⭐ 🟢 What is row context in DAX?
**Asked at:** Commonly asked (no company-specific report found); named with filter context in the Weekday 2026 guide in the sources file.
**What the interviewer is checking:** Do you know when "the current row" exists in DAX?
**Say this in the interview:** "Row context means DAX is standing on one row of a table at a time. It exists inside a calculated column and inside iterator functions like SUMX, so `Sales[Quantity] * Sales[UnitPrice]` means this row's quantity times this row's price."
**Explain simply:**
- Calculated column: DAX evaluates the formula once per row, each time with that row as the context.
- Iterators (SUMX, AVERAGEX, FILTER...) create a row context for each row they walk through.
- A plain measure has no row context, which is why `Sales[Quantity] * Sales[UnitPrice]` inside a measure fails (Q19).
**Example:** `LineTotal` column on 3 orders computes 1000, 800 and 1500, one row at a time.
**Sample data:** Table `Sales`
| OrderID | Quantity | UnitPrice |
|---|---|---|
| 1 | 2 | 500 |
| 2 | 1 | 800 |
| 3 | 3 | 500 |

**DAX / Steps:** Not run here.
```dax
LineTotal = Sales[Quantity] * Sales[UnitPrice]   -- calculated column
```
**Alternative:** Same effect in a measure: `SUMX ( Sales, Sales[Quantity] * Sales[UnitPrice] )`.
**Result:** Reproduced with pandas: 1000, 800, 1500; sum 3300.
**Pandas check:**
```python
import pandas as pd
sales = pd.DataFrame({"OrderID":[1,2,3],"Quantity":[2,1,3],"UnitPrice":[500,800,500]})
sales["LineTotal"] = sales["Quantity"] * sales["UnitPrice"]   # one row at a time
print(sales)
print("Sum of LineTotal:", sales["LineTotal"].sum())
```
Output: LineTotal 1000, 800, 1500; sum 3300.
**Version / licensing note:** From memory, unverified.
**Edge cases:** Row context does not filter other tables by itself (needs RELATED, or CALCULATE for context transition, Q33).
**Likely follow-ups:**
- *Does row context filter?* No, it only picks the current row.
- *Which functions create it?* Calculated columns and X-functions.
**Common mistakes:** Referencing a column bare in a measure and expecting "the current row".

### Q9 ⭐⭐⭐ 🟢 What does the CALCULATE function do?
**Asked at:** Commonly asked (no company-specific report found); named a deciding concept in the Weekday 2026 guide in the sources file.
**What the interviewer is checking:** Do you know CALCULATE evaluates an expression under modified filters?
**Say this in the interview:** "CALCULATE evaluates an expression, usually a measure, after changing the filter context. I write the number I want first, then the filters to apply: `CALCULATE([Total Sales], Sales[Category] = "Tech")`."
**Explain simply:**
- Syntax: `CALCULATE(expression, filter1, filter2, ...)`.
- A filter on a column that already has a filter (e.g. a slicer on the same column) **replaces** it; a filter on another column is **added**. (Per the sources file's note on the Microsoft CALCULATE page; not re-fetched.)
- It is the single most used DAX function; most "conditional totals" use it.
**Example:** "Tech sales" stays 2,500 regardless of a Category slicer, but still respects the Region row.
**Sample data:** Table `Sales` (same as Q7).
| Region | Category | Amount |
|---|---|---|
| North | Tech | 1000 |
| North | Furniture | 800 |
| South | Tech | 1500 |
| South | Stationery | 200 |
| East | Furniture | 1600 |

**DAX / Steps:** Not run here.
```dax
Total Sales = SUM ( Sales[Amount] )
Tech Sales  = CALCULATE ( [Total Sales], Sales[Category] = "Tech" )
```
**Alternative:** `CALCULATE ( SUM ( Sales[Amount] ), FILTER ( Sales, Sales[Category] = "Tech" ) )`, more flexible but heavier (Q38).
**Result:** Reproduced with pandas: Tech Sales 2500; in the South row 1500; with a Furniture slicer still 2500 (the Category slicer is overwritten).
**Pandas check:**
```python
import pandas as pd
sales = pd.DataFrame({"Region":["North","North","South","South","East"],
                      "Category":["Tech","Furniture","Tech","Stationery","Furniture"],
                      "Amount":[1000,800,1500,200,1600]})
tech = sales[sales.Category=="Tech"]["Amount"].sum()
print("Tech Sales (no slicer):", tech)
print("Tech Sales in South  :", sales.query("Region=='South' and Category=='Tech'")["Amount"].sum())
print("Tech Sales, slicer=Furniture:", tech, "(slicer overwritten)")
```
Output: 2500; 1500; 2500.
**Version / licensing note:** The sources file records the Microsoft Learn CALCULATE page (fetched in the research phase, updated 2026-08, not re-fetched here). Everything else from memory, unverified.
**Edge cases:** CALCULATE also turns a row context into a filter context (context transition, Q33). Boolean filter arguments work on one column.
**Likely follow-ups:**
- *Can it take several filters?* Yes, combined with AND (Q36).
- *CALCULATE vs FILTER?* FILTER returns a table; CALCULATE evaluates (Q38).
**Common mistakes:** Putting the filter first; expecting the slicer on the same column to still apply.

### Q10 ⭐⭐⭐ 🟢 Write a DAX measure for total sales (or total payroll cost).
**Asked at:** Wipro (2023 Bangalore-Rural: DAX SUM) per the sources file; single report.
**What the interviewer is checking:** Can you write the simplest measure cleanly?
**Say this in the interview:** "`Total Payroll Cost = SUM ( Payroll[PayrollCost] )`. I make it a measure so it recalculates for every department, month and slicer."
**Explain simply:**
- SUM adds one numeric column.
- Name the measure clearly and store it in a sensible table.
- Reuse it inside other measures (Q30).
**Example:** Payroll lines for three employees across two months.
**Sample data:** Table `Payroll`
| EmpID | Month | Dept | PayrollCost |
|---|---|---|---|
| E101 | Jan | HR | 50000 |
| E102 | Jan | IT | 70000 |
| E101 | Feb | HR | 50000 |
| E102 | Feb | IT | 72000 |
| E103 | Feb | IT | 65000 |

**DAX / Steps:** Not run here.
```dax
Total Payroll Cost = SUM ( Payroll[PayrollCost] )
```
**Alternative:** `SUMX ( Payroll, Payroll[PayrollCost] )` gives the same, with no benefit.
**Result:** Reproduced with pandas: total 307000; HR 100000, IT 207000; Jan 120000, Feb 187000.
**Pandas check:**
```python
import pandas as pd
pay = pd.DataFrame({"EmpID":["E101","E102","E101","E102","E103"],
                    "Month":["Jan","Jan","Feb","Feb","Feb"],
                    "Dept":["HR","IT","HR","IT","IT"],
                    "PayrollCost":[50000,70000,50000,72000,65000]})
print("Total Payroll Cost:", pay["PayrollCost"].sum())
print(pay.groupby("Dept")["PayrollCost"].sum())
print(pay.groupby("Month")["PayrollCost"].sum())
```
Output: 307000; HR 100000, IT 207000; Feb 187000, Jan 120000.
**Version / licensing note:** From memory, unverified.
**Edge cases:** Blank costs are ignored; if the column is text, SUM will fail, so fix the data type in Power Query.
**Likely follow-ups:**
- *Per department?* Put Dept in the visual; the measure adapts.
- *Format?* Set Format in Measure tools (e.g. currency).
**Common mistakes:** Creating a calculated column instead; leaving cost as text.

### Q11 ⭐⭐⭐ 🟢 Write a DAX measure that counts unique employees.
**Asked at:** A Deloitte Bengaluru Glassdoor review (June 2025) reportedly had a "count unique customers across tables" DAX prompt (search snippet only, single anecdote, per the sources file); otherwise commonly asked.
**What the interviewer is checking:** Distinct vs total rows when an ID repeats.
**Say this in the interview:** "`Unique Employees = DISTINCTCOUNT ( Payroll[EmpID] )`. COUNTROWS would count every payroll line, so an employee paid in two months would be counted twice."
**Explain simply:**
- DISTINCTCOUNT counts each ID once.
- If you have a clean Employees dimension table, `COUNTROWS(Employees)` is another route.
- The result changes with filters (month, department).
**Example:** 5 payroll lines but only 3 people.
**Sample data:** Table `Payroll`
| EmpID | Month |
|---|---|
| E101 | Jan |
| E102 | Jan |
| E101 | Feb |
| E102 | Feb |
| E103 | Feb |

**DAX / Steps:** Not run here.
```dax
Unique Employees = DISTINCTCOUNT ( Payroll[EmpID] )
```
**Alternative:** `COUNTROWS ( VALUES ( Payroll[EmpID] ) )`.
**Result:** Reproduced with pandas: rows 5; unique employees 3; Jan 2, Feb 3.
**Pandas check:**
```python
import pandas as pd
pay = pd.DataFrame({"EmpID":["E101","E102","E101","E102","E103"],
                    "Month":["Jan","Jan","Feb","Feb","Feb"]})
print("COUNTROWS(payroll rows):", len(pay))
print("DISTINCTCOUNT(EmpID)   :", pay["EmpID"].nunique())
print(pay.groupby("Month")["EmpID"].nunique())
```
Output: 5; 3; Feb 3, Jan 2.
**Version / licensing note:** From memory, unverified; blank handling of DISTINCTCOUNT is unverified (Q6).
**Edge cases:** Totals: unique employees across Jan+Feb is 3, not 2+3=5, so the total row correctly does not add up the months. Same person with two IDs counts twice.
**Likely follow-ups:**
- *Active employees only?* Wrap in CALCULATE with a status filter.
- *Blank IDs?* Check data quality.
**Common mistakes:** Using COUNT/COUNTROWS on a repeating key.

### Q12 ⭐⭐⭐ 🟡 What is the difference between row context and filter context?
**Asked at:** Commonly asked (no company-specific report found); the Weekday 2026 guide in the sources file calls row vs filter context the deciding concept.
**What the interviewer is checking:** Can you contrast "current row" with "current filters"?
**Say this in the interview:** "Row context is 'which single row am I on', created by calculated columns and iterators. Filter context is 'which rows are currently visible', created by slicers, visuals and CALCULATE. Row context does not filter other rows; filter context does not point to one row."
**Explain simply:**
- Row context: one row at a time, lets you use column values directly.
- Filter context: a subset of rows, lets aggregators like SUM total them.
- They can exist together: SUMX iterates rows (row context) inside whatever filter context the visual gives.
- CALCULATE converts row context into filter context (Q33).
**Example:** In a table of 3 orders, `LineTotal` runs per row; `Total Sales` for Region = North only sees the 2 North orders.
**Sample data:** Table `Sales`
| Region | Quantity | UnitPrice |
|---|---|---|
| North | 2 | 500 |
| North | 1 | 800 |
| South | 3 | 500 |

**DAX / Steps:** Not run here.
```dax
LineTotal = Sales[Quantity] * Sales[UnitPrice]      -- row context (column)
Total Sales = SUM ( Sales[LineTotal] )              -- filter context (measure)
```
**Alternative:** Use a one-line comparison table: row context = "one row"; filter context = "set of rows".
**Result:** Reproduced with pandas: per row 1000, 800, 1500; Region North sum 1800; South 1500.
**Pandas check:**
```python
import pandas as pd
s = pd.DataFrame({"Region":["North","North","South"],"Quantity":[2,1,3],"UnitPrice":[500,800,500]})
s["LineTotal"] = s.Quantity*s.UnitPrice
print("Row context (calc column) per row:", s.LineTotal.tolist())
print("Filter context Region=North, SUM:", s[s.Region=="North"].LineTotal.sum())
print("Filter context Region=South, SUM:", s[s.Region=="South"].LineTotal.sum())
```
Output: [1000, 800, 1500]; 1800; 1500.
**Version / licensing note:** From memory, unverified; the sources file lists Microsoft's "Context in DAX Formulas" only as a search snippet.
**Edge cases:** Relationships: row context on the "one" side can reach "many" side only via aggregation; on the "many" side use RELATED.
**Likely follow-ups:**
- *What is context transition?* Q33.
- *Can a measure have row context?* Only inside an iterator.
**Common mistakes:** Saying they are the same thing; trying to use a column bare in a measure.

### Q13 ⭐⭐⭐ 🟡 Write a DAX measure for total sales of one product category using CALCULATE.
**Asked at:** Commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you apply a Boolean filter in CALCULATE?
**Say this in the interview:** "`Furniture Sales = CALCULATE ( SUM ( Sales[Amount] ), Sales[Category] = "Furniture" )`. It sums sales but only for Furniture rows, while still respecting other filters like Region."
**Explain simply:**
- First argument: what to calculate. Second: the filter.
- A Boolean filter such as `Sales[Category] = "Furniture"` is allowed (per the sources file's note on the Microsoft CALCULATE page).
- It overrides any Category slicer.
**Example:** Furniture sales by Region.
**Sample data:** Table `Sales`
| Region | Category | Amount |
|---|---|---|
| North | Tech | 1000 |
| North | Furniture | 800 |
| South | Tech | 1500 |
| South | Stationery | 200 |
| East | Furniture | 1600 |

**DAX / Steps:** Not run here.
```dax
Furniture Sales =
CALCULATE ( SUM ( Sales[Amount] ), Sales[Category] = "Furniture" )
```
**Alternative:** `CALCULATE ( [Total Sales], KEEPFILTERS ( Sales[Category] = "Furniture" ) )` respects a Category slicer instead of overriding it (KEEPFILTERS not verified).
**Result:** Reproduced with pandas: total 2400; East 1600, North 800 (South blank).
**Pandas check:**
```python
import pandas as pd
sales = pd.DataFrame({"Region":["North","North","South","South","East"],
                      "Category":["Tech","Furniture","Tech","Stationery","Furniture"],
                      "Amount":[1000,800,1500,200,1600]})
f = sales[sales.Category=="Furniture"]
print("Furniture Sales total:", f.Amount.sum())
print(f.groupby("Region").Amount.sum())
```
Output: 2400; East 1600, North 800.
**Version / licensing note:** From memory, unverified (page not re-fetched).
**Edge cases:** South shows blank, not 0, in a visual. Spelling and case in the text must match the data (DAX text comparison is case-insensitive).
**Likely follow-ups:**
- *Pass the category dynamically?* Use a slicer plus SELECTEDVALUE.
- *Why not FILTER?* Q38.
**Common mistakes:** Using single quotes; forgetting that the filter overrides a slicer on the same column.

### Q14 ⭐⭐⭐ 🟡 Write a DAX measure for total revenue when each row has Quantity and Unit Price columns.
**Asked at:** A Deloitte Bengaluru Glassdoor review (June 2025) reportedly asked for net sales from MRP, discount and net-sale columns (search snippet only, single anecdote, per the sources file); otherwise commonly asked.
**What the interviewer is checking:** Do you reach for SUMX (iterator) when the value is a row-level product?
**Say this in the interview:** "`Total Revenue = SUMX ( Sales, Sales[Quantity] * Sales[UnitPrice] )`. SUMX multiplies on each row and then adds, which gives the right revenue; summing quantity and price separately and multiplying would be wrong."
**Explain simply:**
- Revenue = quantity x price per row, then add.
- The multiplication needs a row context, which SUMX supplies.
- No calculated column needed, so the model stays small.
**Example:** A tiny order table.
**Sample data:** Table `Sales`
| Region | Quantity | UnitPrice |
|---|---|---|
| North | 2 | 500 |
| North | 1 | 800 |
| South | 3 | 500 |
| South | 10 | 20 |
| East | 2 | 800 |

**DAX / Steps:** Not run here.
```dax
Total Revenue = SUMX ( Sales, Sales[Quantity] * Sales[UnitPrice] )
```
**Alternative:** Add `Revenue` calculated column (`= Sales[Quantity] * Sales[UnitPrice]`) and `SUM` it.
**Result:** Reproduced with pandas: total 5100; East 1600, North 1800, South 1700. The wrong shortcut sum(Qty) x sum(Price) gives 47160.
**Pandas check:**
```python
import pandas as pd
s = pd.DataFrame({"Region":["North","North","South","South","East"],
                  "Quantity":[2,1,3,10,2],"UnitPrice":[500,800,500,20,800]})
s["Rev"] = s.Quantity*s.UnitPrice
print("Total Revenue:", s.Rev.sum())
print(s.groupby("Region").Rev.sum())
print("Wrong: sum(Qty)*sum(Price) =", s.Quantity.sum()*s.UnitPrice.sum())
```
Output: 5100; East 1600, North 1800, South 1700; 47160.
**Version / licensing note:** The sources file records Microsoft's SUMX page (fetched in the research phase, not re-fetched here); details from memory, unverified.
**Edge cases:** Discounts: `Quantity * UnitPrice * (1 - Discount)` inside SUMX. A blank price makes that row blank (ignored).
**Likely follow-ups:**
- *Average order value?* DIVIDE([Total Revenue], COUNTROWS(Sales)).
- *Net sales after discount?* Extend the SUMX expression.
**Common mistakes:** `SUM(Qty) * SUM(Price)`; `SUM(Qty * Price)` (Q19).

### Q15 ⭐⭐⭐ 🟡 Why should you use DIVIDE instead of the / operator in a measure?
**Asked at:** Commonly asked (no company-specific report found); DIVIDE is on the Weekday 2026 list in the sources file.
**What the interviewer is checking:** Do you handle divide-by-zero safely?
**Say this in the interview:** "DIVIDE handles a zero or blank denominator for you and returns BLANK, or an alternate value I choose, so the visual doesn't fill with errors or Infinity. With `/` I would need an IF check every time."
**Explain simply:**
- `DIVIDE(numerator, denominator [, alternateResult])`.
- Per the sources file (Microsoft Learn best-practice page, fetched in research, not re-fetched): DIVIDE returns BLANK for a zero or blank denominator; use `/` only when the denominator is a constant that cannot be zero.
- A new department with 0 headcount would otherwise break the attrition measure.
**Example:** Attrition rate = leavers / average headcount; Legal has 0 headcount.
**Sample data:** Table `Dept Summary`
| Dept | Leavers | AvgHeadcount |
|---|---|---|
| HR | 2 | 40 |
| IT | 9 | 120 |
| Sales | 12 | 200 |
| Legal | 0 | 0 |

**DAX / Steps:** Not run here.
```dax
Attrition % = DIVIDE ( SUM ( Dept[Leavers] ), SUM ( Dept[AvgHeadcount] ) )
```
**Alternative:** `IF ( SUM ( Dept[AvgHeadcount] ) = 0, BLANK(), SUM ( Dept[Leavers] ) / SUM ( Dept[AvgHeadcount] ) )`, longer and slower to read.
**Result:** Reproduced with pandas: HR 0.05, IT 0.075, Sales 0.06, Legal blank (NaN). A plain `/` in pandas also gives NaN for 0/0, so the pandas run cannot show DAX's own error display; in DAX, from memory (unverified), `/` shows NaN or Infinity instead of blank.
**Pandas check:**
```python
import pandas as pd
d = pd.DataFrame({"Dept":["HR","IT","Sales","Legal"],"Leavers":[2,9,12,0],"AvgHeadcount":[40,120,200,0]})
d["PlainSlash"] = d.Leavers/d.AvgHeadcount
d["DIVIDE"] = (d.Leavers/d.AvgHeadcount.where(d.AvgHeadcount!=0)).round(4)
print(d)
```
Output: HR 0.050/0.050, IT 0.075/0.075, Sales 0.060/0.060, Legal NaN/NaN.
**Version / licensing note:** Microsoft Learn DIVIDE page not fetched by me; the above rests on the sources file, plus memory.
**Edge cases:** Third argument gives a fallback, e.g. `DIVIDE(a, b, 0)`. A blank is not 0 in a chart (the point is skipped).
**Likely follow-ups:**
- *Is DIVIDE slower than `/`?* Per the sources file, `/` is fine for a constant denominator; the difference is minor.
- *Percentage format?* Set the measure's format to %.
**Common mistakes:** Using `/` on ratios; replacing blank with 0 and distorting averages.

### Q16 ⭐⭐⭐ 🟡 Why does my measure show the same number in every row of a table visual?
**Asked at:** Commonly asked (no company-specific report found); "same total in every row" is on the Weekday 2026 list in the sources file.
**What the interviewer is checking:** Can you debug missing filter flow?
**Say this in the interview:** "Usually the row's field cannot filter the table my measure sums: there is no relationship, or the field comes from an unrelated table. Other causes are ALL/REMOVEFILTERS in the measure or a measure that ignores context."
**Explain simply:**
- Each row of a visual supplies a filter; the measure only reacts if that filter reaches the table being summed.
- Check Model view: is there a relationship between the dimension and fact table, and is the right direction active?
- Check the measure for ALL() or a hard-coded constant.
- Check the visual uses the dimension's column, not an unrelated one.
**Example:** A `Departments` table with no link to `Sales`: every department row shows the 500 grand total.
**Sample data:** Table `Sales`
| Dept | Amount |
|---|---|
| IT | 100 |
| IT | 200 |
| HR | 50 |
| Sales | 150 |

Table `Departments`: IT, HR, Sales (one column `Dept`).
**DAX / Steps:** Not run here. Click-path to fix: **Model view** > drag `Departments[Dept]` onto `Sales[Dept]` (one-to-many) or **Home > Manage relationships > New**. Measure stays:
```dax
Total Amount = SUM ( Sales[Amount] )
```
**Alternative:** Use `Sales[Dept]` directly in the visual instead of the unrelated dimension column.
**Result:** Reproduced with pandas: no relationship gives 500 in every row; with a relationship IT 300, HR 50, Sales 150.
**Pandas check:**
```python
import pandas as pd
sales = pd.DataFrame({"Dept":["IT","IT","HR","Sales"],"Amount":[100,200,50,150]})
dept = pd.DataFrame({"Dept":["IT","HR","Sales"]})
print("No relationship:")
print(pd.DataFrame({"Dept":dept.Dept,"Total":sales.Amount.sum()}))
print("With relationship:")
print(sales.groupby("Dept").Amount.sum().reindex(dept.Dept).reset_index())
```
Output: 500, 500, 500; then IT 300, HR 50, Sales 150.
**Version / licensing note:** From memory, unverified (Desktop menu names may vary).
**Edge cases:** Inactive relationship; wrong cross-filter direction; a data-type mismatch on the key; a many-to-many link.
**Likely follow-ups:**
- *Same number only in total row?* That is normal for non-additive measures.
- *Measure shows one value for everything on a slicer?* Check ALL usage (Part 5).
**Common mistakes:** Blaming the measure when the relationship is missing.

### Q17 ⭐⭐ 🟢 What is an iterator function in DAX, and which ones do you know?
**Asked at:** Commonly asked (no company-specific report found); SUM vs SUMX style questions are in the Deloitte and Wipro reports in the sources file.
**What the interviewer is checking:** Do you know the "X" functions walk rows?
**Say this in the interview:** "An iterator goes through a table one row at a time, evaluates an expression on each row, and then aggregates the results. I know SUMX, AVERAGEX, MINX, MAXX, COUNTX, RANKX and also FILTER."
**Explain simply:**
- Each iterator needs a table and an expression: `SUMX(table, expression)`.
- They create row context (Q8).
- The table argument can be filtered, e.g. `SUMX(FILTER(...), ...)`.
- Plain SUM/AVERAGE are shortcuts for one column.
**Example:** Average order value across orders = `AVERAGEX(Sales, Sales[Quantity] * Sales[UnitPrice])`.
**DAX / Steps:** Not run here.
```dax
Avg Order Value = AVERAGEX ( Sales, Sales[Quantity] * Sales[UnitPrice] )
```
**Alternative:** `DIVIDE ( [Total Revenue], COUNTROWS ( Sales ) )` gives the same for non-blank rows.
**Version / licensing note:** From memory, unverified; only SUMX was documented in the sources file.
**Edge cases:** Large tables with nested iterators are slow; blanks in the expression are skipped.
**Likely follow-ups:**
- *Is FILTER an iterator?* Yes, it returns a table of rows that pass a test.
- *RANKX?* Covered in Part 5.
**Common mistakes:** Using an iterator when SUM is enough; nesting iterators unnecessarily.

### Q18 ⭐⭐ 🟢 What is the difference between an implicit measure and an explicit measure?
**Asked at:** Commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you create reusable named measures?
**Say this in the interview:** "An implicit measure is made automatically when I drag a numeric column into a visual and Power BI sums it. An explicit measure is one I write in DAX with a name. I prefer explicit ones: they are reusable, can be referenced in other measures, and give me control."
**Explain simply:**
- Implicit: tied to one visual, limited aggregation options (Sum, Average, Count...), cannot be reused in DAX.
- Explicit: named, formatted, tested, used anywhere.
- Explicit measures are the professional standard.
**Example:** Dragging `Salary` makes "Sum of Salary" (implicit); `Avg Salary = AVERAGE(Employees[Salary])` is explicit.
**DAX / Steps:** Not run here.
```dax
Avg Salary = AVERAGE ( Employees[Salary] )
```
Click-path (from memory): Home > Calculations > New measure.
**Alternative:** Mark the column "Don't summarize" in Column tools > Summarization to stop accidental implicit sums.
**Version / licensing note:** From memory, unverified.
**Edge cases:** Some tools (e.g. Excel PivotTables on a model, calculation groups) behave differently around implicit measures; unverified.
**Likely follow-ups:**
- *Why avoid implicit?* No reuse, hidden logic.
- *Quick measure?* It generates an explicit one (Q23).
**Common mistakes:** Summing IDs or years by accident.

### Q19 ⭐⭐ 🟢 Can you write SUM(Sales[Quantity] * Sales[Price]) in DAX? Why or why not?
**Asked at:** Commonly asked (no company-specific report found); a Deloitte Glassdoor review (June 2025) reported net-sales-from-columns DAX prompts (snippet only, single anecdote).
**What the interviewer is checking:** Do you know SUM accepts only one column?
**Say this in the interview:** "No. SUM takes a single column reference, not an expression, so the syntax is rejected. Use SUMX with the table to multiply on each row, or add a calculated column."
**Explain simply:**
- `SUM(Sales[Quantity])` works; `SUM(a * b)` does not.
- SUMX supplies the row context where `Quantity * Price` makes sense.
- Summing quantity and price separately and multiplying is wrong.
**Example:** 3 orders: (2 x 500) + (1 x 800) + (3 x 500) = 3,300.
**Sample data:** Table `Sales`
| Quantity | Price |
|---|---|
| 2 | 500 |
| 1 | 800 |
| 3 | 500 |

**DAX / Steps:** Not run here.
```dax
Total Revenue = SUMX ( Sales, Sales[Quantity] * Sales[Price] )
```
**Alternative:** Calculated column `LineTotal = Sales[Quantity] * Sales[Price]`, then `SUM ( Sales[LineTotal] )`.
**Result:** Reproduced with pandas: the right total is 3300; the wrong shortcut sum(Q) x sum(P) is 10800.
**Pandas check:**
```python
import pandas as pd
s = pd.DataFrame({"Quantity":[2,1,3],"Price":[500,800,500]})
print("Intended SUMX result:", (s.Quantity*s.Price).sum())
print("Calculated-column then SUM:", (s.Quantity*s.Price).sum())
print("Wrong shortcut sum(Q)*sum(P):", s.Quantity.sum()*s.Price.sum())
```
Output: 3300; 3300; 10800.
**Version / licensing note:** From memory, unverified: that SUM accepts only a column reference is not re-checked against Microsoft's SUM page (unreachable). Premise holds as stated.
**Edge cases:** Blank price rows are skipped by SUMX.
**Likely follow-ups:**
- *What error appears?* The editor reports a syntax or argument error; wording varies, unverified.
- *Faster option?* Pre-compute in Power Query.
**Common mistakes:** Copying Excel's SUMPRODUCT idea into SUM.

### Q20 ⭐⭐ 🟢 What is BLANK() in DAX, and how is it different from zero or empty text?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand that "no value" and "the value 0" are different things, and what each does to a visual?
**Say this in the interview:** "BLANK is DAX's way of saying there is no value, like an empty cell. It is not zero and not empty text. A measure that finds no rows returns BLANK, and Power BI usually hides that row in a visual, while a zero would show."
**Explain simply:**
- BLANK means "nothing here". SUM over zero matching rows returns BLANK, not 0.
- Zero is a real number. Empty text ("") is a real text value with no characters. Both are values; BLANK is the absence of one.
- Visuals often drop rows where every measure is BLANK. That is why a department with no exits can vanish from a chart.
- You can test with `ISBLANK()`, or force a zero with `SUM(...) + 0` or `COALESCE(..., 0)`.
**Example:** Exits by department. Finance and HR had no exits. With BLANK they are hidden from the table; if the CHRO wants to see "0 exits" for them, you force zero.
**Sample data:**

Table `Dept`:

| Dept |
|---|
| Finance |
| HR |
| IT |
| Sales |

Table `Exits`:

| Dept | Exits |
|---|---|
| IT | 2 |
| Sales | 1 |
| IT | 1 |

**DAX / Steps (not run here):**
```dax
Exits = SUM ( Exits[Exits] )                 -- BLANK when no rows
Exits (show 0) = SUM ( Exits[Exits] ) + 0    -- BLANK + 0 = 0
Exits (alt) = COALESCE ( SUM ( Exits[Exits] ), 0 )
Is Empty = ISBLANK ( [Exits] )
```
**Alternative:** `IF( ISBLANK([Exits]), 0, [Exits] )`, which is longer but easier to read.
**Result (reproduced with pandas, not a DAX engine):** Finance BLANK, HR BLANK, IT 3, Sales 1; with the zero-forcing version Finance 0, HR 0, IT 3, Sales 1.
**Pandas check:**
```python
import pandas as pd
dept = pd.DataFrame({"Dept": ["Finance","HR","IT","Sales"]})
exits = pd.DataFrame({"Dept": ["IT","Sales","IT"], "Exits": [2,1,1]})
s = exits.groupby("Dept")["Exits"].sum()
out = dept.set_index("Dept").join(s)          # no rows -> NaN = BLANK
out["Exits_or_0"] = out["Exits"].fillna(0)    # like  SUM(...) + 0
print(out)
```
```
         Exits  Exits_or_0
Dept                      
Finance    NaN         0.0
HR         NaN         0.0
IT         3.0         3.0
Sales      1.0         1.0
```
**Version / licensing note:** Microsoft Learn (learn.microsoft.com) could not be reached from this session, so the BLANK function page was not read. Everything here is from memory, unverified.
**Edge cases:** From memory, unverified: in DAX, `BLANK() = 0` and `BLANK() = ""` both evaluate to TRUE with the `=` operator, so test with `ISBLANK()` or the strict `==` operator. BLANK + number treats BLANK as 0. A blank denominator makes `/` fail but `DIVIDE` return BLANK (see Q15 area).
**Likely follow-ups:** 1) How do you show 0 instead of BLANK? Add `+ 0` or COALESCE, but be careful because it can make every row of a large table appear. 2) Is a blank in a text column the same as ""? No, they are different, though they can look alike.
**Common mistakes:** Assuming SUM returns 0 for no rows; adding `+ 0` to every measure and flooding a visual with empty categories; using `= 0` to test for blank.

### Q21 ⭐⭐ 🟢 What is the difference between DAX and Excel formulas?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you move from Excel thinking (cells) to Power BI thinking (columns and filters)?
**Say this in the interview:** "DAX looks like Excel, but it works on whole columns and tables, not cells, and its answer changes with the filters on the report. Excel formulas point to cell addresses like B2."
**Explain simply:**
- Excel: `=SUM(B2:B50)` refers to cells in a grid. DAX: `SUM(Sales[Amount])` refers to a column in a table.
- A DAX measure is calculated fresh for each cell of a visual, using that cell's filters (department, month). One Excel formula gives one fixed answer.
- DAX has no cell addresses and no "drag the formula down". Row-by-row work needs a calculated column or an iterator such as SUMX.
- Many names are shared (IF, SUM, AVERAGE, DATE), so Excel users pick it up quickly. DAX adds CALCULATE, filter functions and relationships between tables, which Excel formulas do not have.
**Example:** Total payroll. In Excel you write the formula once per cell for each department. In DAX one measure `Total Payroll` feeds every department row, every month column and the grand total.
**DAX / Steps (not run here):** Side by side:
```dax
-- Excel:  =SUMIF(B:B, "IT", C:C)
IT Payroll = CALCULATE ( SUM ( Payroll[Amount] ), Payroll[Dept] = "IT" )
```
**Alternative:** Say it as a table: cells vs columns; one answer vs answer per filter; no relationships vs relationships.
**Version / licensing note:** Microsoft Learn was not reachable from this session; from memory, unverified. DAX also runs inside Excel's Data Model and Power Pivot (see Q57 area).
**Edge cases:** Some Excel functions have no DAX twin, and DAX functions behave differently on blanks. DAX is strict about data types per column.
**Likely follow-ups:** 1) Can you use cell references in DAX? No. 2) Which is easier to audit? Excel for small data; DAX when data is large or shared.
**Common mistakes:** Writing `Sales[Amount] * 2` in a measure and expecting a single row's value; looking for the "fill down" handle.

### Q22 ⭐⭐ 🟢 What is the difference between DAX and M, the Power Query language?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know which language does which job and when each runs?
**Say this in the interview:** "M is the language behind Power Query. It cleans and reshapes data before it loads. DAX works after the data is in the model, to calculate results like totals and percentages that react to filters."
**Explain simply:**
- M (Power Query): runs at refresh time, step by step, on data coming in. It is where you remove columns, change types, merge and unpivot. Every click in the Power Query editor writes M for you.
- DAX: runs inside the loaded model, at report time for measures. It is where you build KPIs such as attrition rate.
- M is case-sensitive; DAX is not (from memory, unverified).
- Rule of thumb: shape and clean in M, calculate business numbers in DAX.
**Example:** Attendance file has "Present", "present " and "PRESENT". Fix with Text.Trim and Text.Proper in M. Then a DAX measure computes attendance %.
**DAX / Steps (not run here):**
```m
let
    Source = Excel.Workbook(File.Contents("C:\HR\attendance.xlsx"), null, true),
    Data = Source{[Item="Attendance",Kind="Sheet"]}[Data],
    Promoted = Table.PromoteHeaders(Data, [PromoteAllScalars=true]),
    Cleaned = Table.TransformColumns(Promoted, {{"Status", each Text.Proper(Text.Trim(_)), type text}})
in
    Cleaned
```
```dax
Attendance % = DIVIDE ( CALCULATE ( COUNTROWS ( Attendance ), Attendance[Status] = "Present" ), COUNTROWS ( Attendance ) )
```
Steps to see M: Power BI Desktop > Home > Transform data > Home > Advanced Editor (not run here).
**Alternative:** Compare in a table: when it runs (refresh vs query time), what it works on (source rows vs model tables), typical task (clean vs measure).
**Version / licensing note:** Microsoft Learn was not reachable here; from memory, unverified.
**Edge cases:** A calculated column can be made in either language. Prefer M where possible (see Q45 area), since it is processed before loading.
**Likely follow-ups:** 1) Can DAX clean data? Partly, but it is the wrong place. 2) Do you have to write M by hand? No, the editor writes it.
**Common mistakes:** Building every fix as DAX; assuming DAX and M share syntax.

### Q23 ⭐⭐ 🟢 What is a quick measure, and what are its limits?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the built-in shortcut and that you still need to understand the DAX it writes?
**Say this in the interview:** "A quick measure is a ready-made calculation template. I pick the type, drop in fields, and Power BI writes the DAX measure for me. It is handy for learning, but I always read and check the DAX it generates."
**Explain simply:**
- Templates include running total, percent difference, average per category, rank, weighted average and similar (from memory, unverified).
- The result is a normal explicit measure in the model that you can edit.
- Limits (from memory, unverified): it is not available for every data source type, such as some live connections; the list of calculations is fixed; the generated DAX can be long and may not match your exact business rule.
**Example:** Month-on-month change in headcount: use "Month over month change" instead of writing time-intelligence DAX yourself.
**DAX / Steps (not run here):**
1. Power BI Desktop > in the Data pane right-click a table > New quick measure (or Home > Calculations > Quick measure).
2. Choose the calculation, drag fields into the boxes.
3. Select OK, then read the DAX in the formula bar.
**Alternative:** Write the measure yourself; or use a calculation group (advanced).
**Version / licensing note:** Microsoft Learn: quick measures page could not be fetched here; menu names and availability are from memory, unverified.
**Edge cases:** A date table may be required for the time calculations. Generated measures can have odd names; rename them.
**Likely follow-ups:** 1) Is a quick measure implicit or explicit? Explicit. 2) Can you edit it? Yes.
**Common mistakes:** Trusting the output without checking; leaving default names.

### Q24 ⭐⭐ 🟢 Write a calculated column using IF to flag late arrivals in an attendance table.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you write a row-by-row IF, and do you handle a missing swipe-in?
**Say this in the interview:** "I add a calculated column that checks each row's in-time against the shift start. If in-time is after 9:30 it says Late. I also catch blanks first so an absent person is not called on time."
**Explain simply:**
- A calculated column is computed once per row when the data refreshes and stored in the table.
- IF(test, value if true, value if false) works just like in Excel.
- TIME(9,30,0) builds a time value of 9:30:00 to compare with.
- A blank in-time compares like zero, so without a blank check it would wrongly be "On time".
**Example:** Shift starts 9:30. Aarav swipes in at 09:45, so Late.
**Sample data:**

Table `Attendance`:

| Emp | In Time |
|---|---|
| E01 | 09:10 |
| E02 | 09:30 |
| E03 | 09:45 |
| E04 | (blank) |
| E05 | 10:05 |

**DAX / Steps (not run here):**
```dax
Is Late =
IF (
    ISBLANK ( Attendance[In Time] ), "Absent",
    IF ( Attendance[In Time] > TIME ( 9, 30, 0 ), "Late", "On time" )
)
```
Steps: Table view > select Attendance > Table tools > New column > paste (not run here).
**Alternative:** Boolean version: `Is Late Flag = IF ( Attendance[In Time] > TIME(9,30,0), 1, 0 )` so you can SUM it for a late count; or add a grace period: `TIME(9,40,0)`.
**Result (reproduced with pandas):** E01 On time, E02 On time, E03 Late, E04 Absent, E05 Late. Without the blank check, E04 becomes "On time".
**Pandas check:**
```python
import pandas as pd
att = pd.DataFrame({"Emp":["E01","E02","E03","E04","E05"],
  "InTime":["09:10","09:30","09:45",None,"10:05"]})
att["IsLate"] = att["InTime"].apply(lambda t: "Absent" if pd.isna(t) else ("Late" if t > "09:30" else "On time"))
att["Naive"]  = att["InTime"].apply(lambda t: "Late" if ("00:00" if pd.isna(t) else t) > "09:30" else "On time")
print(att)
```
```
   Emp InTime   IsLate    Naive
0  E01  09:10  On time  On time
1  E02  09:30  On time  On time
2  E03  09:45     Late     Late
3  E04    NaN   Absent  On time
4  E05  10:05     Late     Late
```
**Version / licensing note:** Microsoft Learn not reachable here; DAX functions IF, TIME, ISBLANK are from memory, unverified.
**Edge cases:** If In Time is a full date-time, compare only the time part. Night shifts crossing midnight need different logic. Different shifts need a lookup for shift start.
**Likely follow-ups:** 1) Column or measure? Column for the row flag, then a measure counting late rows. 2) Grace period? Compare against 9:40.
**Common mistakes:** Forgetting the blank check; comparing text "09:45" with a time; hard-coding shift times for all shifts.

### Q25 ⭐⭐ 🟢 Write a DAX formula to calculate the number of days between two dates, for example leave days.
**Asked at:** Wipro (2023, Bangalore-Rural candidate report) listed DATEDIFF among DAX topics per research/interview_processes.md as summarised in the sources file; single anecdote.
**What the interviewer is checking:** Do you know DATEDIFF and the "inclusive of both days" trap?
**Say this in the interview:** "I use DATEDIFF with the start date, end date and DAY as the unit. For leave I add 1, because someone on leave 2 March to 4 March took three days, not two."
**Explain simply:**
- DATEDIFF(start, end, unit) counts the boundaries crossed between two dates. Units include DAY, MONTH, YEAR.
- Subtracting dates also gives days, but DATEDIFF is clearer.
- Leave is usually inclusive of both ends, hence + 1.
**Example:** Leave from 31 March to 2 April = 3 days.
**Sample data:**

Table `Leave`:

| Emp | Start | End |
|---|---|---|
| E01 | 2026-03-02 | 2026-03-04 |
| E02 | 2026-03-10 | 2026-03-10 |
| E03 | 2026-03-31 | 2026-04-02 |
| E04 | 2026-04-01 | 2026-04-01 |

**DAX / Steps (not run here):**
```dax
Leave Days = DATEDIFF ( Leave[Start], Leave[End], DAY ) + 1       -- calculated column
Total Leave Days = SUMX ( Leave, DATEDIFF ( Leave[Start], Leave[End], DAY ) + 1 )   -- measure
```
**Alternative:** `INT ( Leave[End] - Leave[Start] ) + 1`.
**Result (reproduced with pandas):** E01 3, E02 1, E03 3, E04 1; total 8.
**Pandas check:**
```python
import pandas as pd
lv = pd.DataFrame({"Emp":["E01","E02","E03","E04"],
  "Start":pd.to_datetime(["2026-03-02","2026-03-10","2026-03-31","2026-04-01"]),
  "End":pd.to_datetime(["2026-03-04","2026-03-10","2026-04-02","2026-04-01"])})
lv["DATEDIFF_day"] = (lv["End"]-lv["Start"]).dt.days
lv["LeaveDaysInclusive"] = lv["DATEDIFF_day"]+1
print(lv)
```
```
  Emp      Start        End  DATEDIFF_day  LeaveDaysInclusive
0  E01 2026-03-02 2026-03-04             2                   3
1  E02 2026-03-10 2026-03-10             0                   1
2  E03 2026-03-31 2026-04-02             2                   3
3  E04 2026-04-01 2026-04-01             0                   1
```
**Version / licensing note:** Microsoft Learn DATEDIFF page not reachable here; from memory, unverified.
**Edge cases:** Weekends and holidays are counted; for working days you need a calendar table (see Part 5). From memory, unverified: end before start may error or return negative depending on version, so guard with IF. Blank dates give blank.
**Likely follow-ups:** 1) Working days only? Count rows of a Calendar table that are working days. 2) Half-day leave? Store a day-fraction column.
**Common mistakes:** Forgetting + 1; using MONTH when you mean DAY; swapping start and end.

### Q26 ⭐⭐ 🟢 Where are calculated columns stored, and how do they affect file size?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know columns cost memory but measures do not?
**Say this in the interview:** "A calculated column is calculated when the data refreshes and then stored inside the model, like any other column, so it adds to file size and memory. A measure is not stored; it is worked out only when a visual asks."
**Explain simply:**
- The model keeps data in a compressed, in-memory column store (VertiPaq, from memory, unverified).
- A column with few distinct values compresses well; one with many distinct values (such as a unique ID or a long decimal) is expensive.
- Every row of the table gets a stored value, so millions of rows multiply the cost.
- Measures cost almost no storage, only calculation time.
**Example:** `Salary Band` with 3 distinct values over 100,000 rows is cheap. A column mixing salary and ID with ~77,000 distinct values is not.
**DAX / Steps (not run here):** Check size: Power BI Desktop > Optimise ribbon? Not verified. Use the external tool DAX Studio > Advanced > View Metrics (from memory, unverified).
**Pandas check:**
```python
import pandas as pd, numpy as np
rng = np.random.default_rng(1)
n = 100000
emp = pd.DataFrame({"Salary": rng.integers(20000, 200000, n)})
emp["SalaryBand"] = pd.cut(emp["Salary"], [0,50000,100000,10**9], labels=["Low","Mid","High"])
print("rows:", n)
print("distinct Salary:", emp["Salary"].nunique(), "| distinct SalaryBand:", emp["SalaryBand"].nunique())
```
```
rows: 100000
distinct Salary: 76632 | distinct SalaryBand: 3
```
This only shows distinct counts (the idea behind compression); it does not measure Power BI file size, which was not run here.
**Alternative:** Create the column in Power Query or the source database; also stored, but processed earlier and usually compressed better.
**Version / licensing note:** Microsoft Learn not reachable here; all storage statements are from memory, unverified.
**Edge cases:** Calculated columns recalculate on every refresh. In DirectQuery they behave differently (see Q45 area).
**Likely follow-ups:** 1) Measure or column to cut size? Measure when it can aggregate. 2) Are they in the .pbix? Yes, as model data.
**Common mistakes:** Adding many text columns "just in case"; thinking calculated columns are free.

### Q27 ⭐⭐ 🟢 Why does Microsoft recommend COUNTROWS rather than COUNT to count rows?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know COUNT skips blanks while COUNTROWS counts every row?
**Say this in the interview:** "COUNTROWS counts rows of a table, so it is clearer and always right for 'how many records'. COUNT counts non-blank values in one column, so a blank in that column silently lowers the answer."
**Explain simply:**
- COUNT(Table[Col]) counts numeric cells that are not blank in that column.
- COUNTROWS(Table) counts the rows in the table or in a filtered table.
- It also expresses intent: you want rows, not a column.
- The sources file notes the COUNTROWS page was fetched earlier by another agent, and that the dedicated best-practice page was not fetched; so the exact Microsoft wording is not quoted here.
**Example:** 5 orders, 2 have no discount recorded. COUNT(Discount) says 3 orders; there are 5.
**Sample data:**

Table `Orders`:

| OrderID | Discount |
|---|---|
| 1 | 10 |
| 2 | (blank) |
| 3 | 5 |
| 4 | (blank) |
| 5 | 0 |

**DAX / Steps (not run here):**
```dax
Orders Count = COUNTROWS ( Orders )
Orders With Discount = COUNT ( Orders[Discount] )
```
**Alternative:** `COUNTA` (counts non-blank values of any type) or DISTINCTCOUNT of the ID column.
**Result (reproduced with pandas):** COUNT = 3, COUNTROWS = 5.
**Pandas check:**
```python
import pandas as pd
orders = pd.DataFrame({"OrderID":[1,2,3,4,5],"Discount":[10,None,5,None,0]})
print("COUNT(Discount)    =", orders["Discount"].count())
print("COUNTROWS(Orders)  =", len(orders))
print("blank discounts    =", orders["Discount"].isna().sum())
```
```
COUNT(Discount)    = 3
COUNTROWS(Orders)  = 5
blank discounts    = 2
```
**Version / licensing note:** Microsoft Learn: COUNTROWS function (DAX) was fetched by an earlier research pass (per research/Book04_Part04_sources.md), not re-fetched here; the best-practice page was not read. Learn was unreachable in this session.
**Edge cases:** A discount of 0 is counted by COUNT (it is not blank). COUNTROWS of an empty filtered table returns BLANK (from memory, unverified).
**Likely follow-ups:** 1) Counting text values? COUNTA. 2) Unique count? DISTINCTCOUNT.
**Common mistakes:** Using COUNT on a column with blanks; confusing zero with blank.

### Q28 ⭐⭐ 🟢 How do you refer to columns and measures in a DAX formula (syntax conventions)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you follow the Table[Column] and [Measure] habit that keeps formulas readable?
**Say this in the interview:** "Columns are written with the table name and the column in square brackets, like Employees[Salary]. Measures are written with just square brackets, like [Total Payroll], so you can tell them apart at a glance."
**Explain simply:**
- Column: `Table[Column]`. If the table name has spaces, put it in single quotes: `'Employee Master'[Salary]`.
- Measure: `[Measure Name]`, no table name by convention.
- Brackets can technically work without the table name for columns, but then it looks like a measure and can confuse readers.
- Strings use double quotes: "IT". Text is not case-sensitive for names.
**Example:**
```dax
Avg Pay = AVERAGE ( 'Employee Master'[Salary] )
High Payroll = CALCULATE ( [Total Payroll], 'Employee Master'[Salary] > 50000 )
```
**DAX / Steps (not run here):** Type the table name and Power BI's IntelliSense suggests columns; type `[` to see measures.
**Alternative:** Reserved/special characters in names may need quotes; keep names simple.
**Version / licensing note:** Microsoft Learn DAX syntax page not reachable here; from memory, unverified.
**Edge cases:** A measure and a column with the same name causes confusion; table names with spaces need quotes.
**Likely follow-ups:** 1) Why not put the table name on measures? Readability convention. 2) Case-sensitive? No (from memory).
**Common mistakes:** Forgetting quotes around spaced table names; writing a measure as Table[Measure].

### Q29 ⭐⭐ 🟢 Write a DAX measure for average salary.
**Asked at:** Wipro (2023, Bangalore-Rural candidate report) listed AVG among DAX topics, per the sources file; single anecdote.
**What the interviewer is checking:** Can you write a basic AVERAGE and explain how blanks and totals behave?
**Say this in the interview:** "Average Salary = AVERAGE(Employees[Salary]). It works for each department or for the whole company, depending on the filters, and it ignores blank salaries."
**Explain simply:**
- AVERAGE sums the non-blank values and divides by how many there are.
- A measure re-evaluates per department and for the grand total.
- Blank salaries are skipped (from memory, unverified), so they do not pull the average down.
**Example:** Six employees, one HR salary missing.
**Sample data:**

Table `Employees`:

| Emp | Dept | Salary |
|---|---|---|
| E01 | IT | 60000 |
| E02 | IT | 72000 |
| E03 | HR | 45000 |
| E04 | HR | (blank) |
| E05 | Sales | 52000 |
| E06 | Sales | 58000 |

**DAX / Steps (not run here):**
```dax
Average Salary = AVERAGE ( Employees[Salary] )
```
**Alternative:** `DIVIDE ( SUM ( Employees[Salary] ), COUNTROWS ( Employees ) )` counts blank-salary rows in the denominator, so it gives a different answer.
**Result (reproduced with pandas):** HR 45000, IT 66000, Sales 55000, grand total 57400. The alternative gives HR 22500 and total 47833.33.
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"Emp":["E01","E02","E03","E04","E05","E06"],
 "Dept":["IT","IT","HR","HR","Sales","Sales"],
 "Salary":[60000,72000,45000,None,52000,58000]})
g = emp.groupby("Dept")["Salary"].agg(Avg="mean", Total="sum", Rows="size")
g["SUM/COUNTROWS"] = g["Total"]/g["Rows"]
print(g)
print("Grand total AVERAGE:", emp["Salary"].mean(), "| SUM/COUNTROWS:", emp["Salary"].sum()/len(emp))
```
```
           Avg     Total  Rows  SUM/COUNTROWS
Dept                                         
HR       45000.0   45000.0     2        22500.0
IT       66000.0  132000.0     2        66000.0
Sales    55000.0  110000.0     2        55000.0
Grand total AVERAGE: 57400.0 | SUM/COUNTROWS: 47833.333333333336
```
**Version / licensing note:** Microsoft Learn AVERAGE page not reachable here; from memory, unverified.
**Edge cases:** The grand total is not the average of department averages (57400, not 55333). Zero salaries are counted. Add a filter for active employees if needed.
**Likely follow-ups:** 1) Average per employee when multiple pay rows each? AVERAGEX over employees. 2) Median? MEDIAN.
**Common mistakes:** Averaging the averages; treating blank as zero.

### Q30 ⭐⭐ 🟢 Can one measure refer to another measure?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you build measures in layers instead of repeating logic?
**Say this in the interview:** "Yes. I write [Payroll] and [Headcount] once, then build [Cost per Head] = DIVIDE([Payroll],[Headcount]). It keeps logic in one place and each measure keeps the current filters."
**Explain simply:**
- Refer to another measure with its name in square brackets.
- The inner measure is evaluated in the same filter context as the outer one.
- Change the base measure once and everything built on it updates.
- Avoid circular references (A uses B, B uses A).
**Example:** Payroll and headcount per department.
**Sample data:**

Table `Employees`:

| Dept | Salary |
|---|---|
| IT | 60000 |
| IT | 72000 |
| HR | 45000 |
| HR | 48000 |
| Sales | 52000 |
| Sales | 58000 |

**DAX / Steps (not run here):**
```dax
Payroll = SUM ( Employees[Salary] )
Headcount = COUNTROWS ( Employees )
Cost per Head = DIVIDE ( [Payroll], [Headcount] )
```
**Alternative:** Repeat the SUM and COUNTROWS inside one measure with VAR (Q51 area), fine for small cases.
**Result (reproduced with pandas):** HR 93000 / 2 = 46500; IT 132000 / 2 = 66000; Sales 110000 / 2 = 55000; total 335000 / 6 = 55833.33.
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"Dept":["IT","IT","HR","HR","Sales","Sales"],"Salary":[60000,72000,45000,48000,52000,58000]})
g = emp.groupby("Dept")["Salary"].agg(Payroll="sum", Headcount="count")
g["AvgCost"] = g["Payroll"]/g["Headcount"]
print(g)
print("Total:", emp["Salary"].sum(), len(emp), emp["Salary"].sum()/len(emp))
```
```
       Payroll  Headcount  AvgCost
Dept                              
HR       93000          2  46500.0
IT       132000          2  66000.0
Sales    110000          2  55000.0
Total: 335000 6 55833.333333333336
```
**Version / licensing note:** Microsoft Learn not reachable here; from memory, unverified.
**Edge cases:** Wrapping a measure in CALCULATE changes its filters. Renaming a measure in the model updates references automatically in Desktop (from memory).
**Likely follow-ups:** 1) Performance? Fine; measures are evaluated on demand. 2) Hidden helper measures? Hide them from the report view.
**Common mistakes:** Copy-pasting logic into many measures; creating circular references.

### Q31 ⭐⭐ 🟢 What is the difference between AVERAGE and AVERAGEX?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know when a column average is not enough and you must calculate row by row first?
**Say this in the interview:** "AVERAGE averages one existing column. AVERAGEX goes through a table row by row, calculates an expression for each row, and then averages those results. I use AVERAGEX when the thing I average does not exist as a column, like Quantity times Price."
**Explain simply:**
- AVERAGEX is an iterator (it loops over rows, see Q17).
- AVERAGE(Sales[Qty]) only averages quantities; it cannot multiply.
- Averaging two averages multiplied together is not the average of the products.
**Example:** Average order line value.
**Sample data:**

Table `Sales`:

| Order | Qty | Price |
|---|---|---|
| O1 | 2 | 100 |
| O1 | 1 | 200 |
| O2 | 5 | 50 |
| O3 | 1 | 400 |
| O3 | 3 | 100 |

**DAX / Steps (not run here):**
```dax
Avg Line Value = AVERAGEX ( Sales, Sales[Qty] * Sales[Price] )
```
**Alternative:** Add a calculated column Line = Qty * Price, then AVERAGE(Sales[Line]); costs storage (Q26).
**Result (reproduced with pandas):** 270. The wrong shortcut AVERAGE(Qty) * AVERAGE(Price) gives 408.
**Pandas check:**
```python
import pandas as pd
s = pd.DataFrame({"Order":["O1","O1","O2","O3","O3"],"Qty":[2,1,5,1,3],"Price":[100,200,50,400,100]})
s["Line"] = s["Qty"]*s["Price"]
print(s)
print("AVERAGEX(Sales, Qty*Price) =", s["Line"].mean())
print("AVERAGE(Qty)*AVERAGE(Price) =", s["Qty"].mean()*s["Price"].mean())
```
```
  Order  Qty  Price  Line
0    O1    2    100   200
1    O1    1    200   200
2    O2    5     50   250
3    O3    1    400   400
4    O3    3    100   300
AVERAGEX(Sales, Qty*Price) = 270.0
AVERAGE(Qty)*AVERAGE(Price) = 408.0
```
**Version / licensing note:** Microsoft Learn not reachable here; from memory, unverified (the sources file did fetch the SUMX page, whose behaviour of ignoring blanks mirrors AVERAGEX, but AVERAGEX itself was not read).
**Edge cases:** Rows where the expression is blank are skipped. "Average per order" (not per line) needs AVERAGEX over a table of orders, e.g. VALUES(Sales[Order]).
**Likely follow-ups:** 1) Average per order? See edge case. 2) Which is faster? AVERAGE on a plain column.
**Common mistakes:** Averaging a product of averages; using AVERAGEX when AVERAGE is enough.

### Q32 ⭐⭐ 🟢 Write a DAX measure that shows Target Met or Below Target by comparing total sales with a sales target.
**Asked at:** commonly asked (no company-specific report found); added as a gap-fill question from standard practice, not from a source.
**What the interviewer is checking:** Can you return text from a measure with IF and handle a missing target?
**Say this in the interview:** "I compare total sales with total target using IF and return 'Target Met' or 'Below Target'. I also handle a blank target so a region with no target is not marked as missed."
**Explain simply:**
- A measure can return text, useful for cards and colour rules.
- VAR stores a value so the formula reads clearly.
- Decide the rule: here sales equal to target counts as met (>=).
**Example:** North sold 120 against 100: Target Met.
**Sample data:**

Table `Sales` and `Targets` (by Region):

| Region | Sales | Target |
|---|---|---|
| North | 120 | 100 |
| South | 80 | 100 |
| East | 95 | 95 |
| West | 60 | (none) |

**DAX / Steps (not run here):**
```dax
Total Sales = SUM ( Sales[Sales] )
Total Target = SUM ( Targets[Target] )
Target Status =
VAR s = [Total Sales]
VAR t = [Total Target]
RETURN
    IF ( ISBLANK ( t ), "No target", IF ( s >= t, "Target Met", "Below Target" ) )
```
**Alternative:** `SWITCH ( TRUE(), ISBLANK(t), "No target", s >= t, "Target Met", "Below Target" )` (Q50).
**Result (reproduced with pandas):** North Target Met, South Below Target, East Target Met, West No target. Total row: 355 vs 295 = Target Met (West's 60 has no target, so it is in sales but not in target).
**Pandas check:**
```python
import pandas as pd
d = pd.DataFrame({"Region":["North","South","East","West"],"Sales":[120,80,95,60],"Target":[100,100,95,None]})
def status(r):
    if pd.isna(r.Target): return "No target"
    return "Target Met" if r.Sales >= r.Target else "Below Target"
d["Status"] = d.apply(status, axis=1)
print(d)
tot_s, tot_t = d.Sales.sum(), d.Target.sum()
print("Total row:", tot_s, tot_t, "Target Met" if tot_s>=tot_t else "Below Target")
```
```
  Region  Sales  Target        Status
0  North    120   100.0    Target Met
1  South     80   100.0  Below Target
2  East     95    95.0    Target Met
3  West     60     NaN     No target
Total row: 355 295.0 Target Met
```
**Version / licensing note:** Microsoft Learn not reachable here; from memory, unverified. For colouring a card use conditional formatting rules (Part 6).
**Edge cases:** The total row compares overall totals and can say Met even when some regions missed. Targets stored at a different grain (monthly vs yearly) need care.
**Likely follow-ups:** 1) Show % achieved? DIVIDE([Total Sales],[Total Target]). 2) Colour it? Conditional formatting on the text.
**Common mistakes:** Not handling a blank target; using > when the rule is >=.

### Q33 ⭐⭐ 🟡 What is context transition in DAX?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know how CALCULATE turns the current row into a filter?
**Say this in the interview:** "Context transition is when CALCULATE takes the current row, which is row context, and converts it into filters. That is why a measure used inside a calculated column returns that row's own total instead of the grand total."
**Explain simply:**
- Row context = "I am standing on one row". Filter context = "these filters are applied".
- Row context does not filter other tables by itself. CALCULATE copies the row's values into filters, so related rows are picked up.
- Referring to a measure inside a row context automatically wraps it in CALCULATE.
- The CALCULATE page (fetched by an earlier pass per the sources file, not re-fetched here) is the source for the context-transition rule.
**Example:** A Customers table; a column for each customer's total spend.
**Sample data:**

Table `Customers`: C1, C2, C3. Table `Sales` (related by Customer):

| Customer | Amount |
|---|---|
| C1 | 100 |
| C1 | 50 |
| C2 | 200 |
| C3 | 30 |
| C3 | 70 |

**DAX / Steps (not run here):**
```dax
Spend (wrong) = SUM ( Sales[Amount] )                 -- calculated column on Customers
Spend (right) = CALCULATE ( SUM ( Sales[Amount] ) )   -- context transition
```
**Alternative:** Use an existing measure in the column: `= [Total Sales]` (implicit CALCULATE).
**Result (reproduced with pandas):** wrong column 450 on every row; right column C1 150, C2 200, C3 100.
**Pandas check:**
```python
import pandas as pd
cust = pd.DataFrame({"Customer":["C1","C2","C3"]})
sales = pd.DataFrame({"Customer":["C1","C1","C2","C3","C3"],"Amount":[100,50,200,30,70]})
cust["SUM_no_CALCULATE"] = sales["Amount"].sum()          # no filter applied to Sales
cust["With_CALCULATE"] = cust["Customer"].map(sales.groupby("Customer")["Amount"].sum())
print(cust)
```
```
  Customer  SUM_no_CALCULATE  With_CALCULATE
0       C1               450             150
1       C2               450             200
2       C3               450             100
```
**Version / licensing note:** Learn unreachable here; the CALCULATE page was fetched earlier per the sources file (updated 2026-08). Detail beyond that is from memory, unverified.
**Edge cases:** Works through relationships. Inside iterators over big tables it can be slow. Duplicate rows in the iterated table are transitioned together (from memory).
**Likely follow-ups:** 1) Does it need a relationship? Yes, to filter another table. 2) Related Q44.
**Common mistakes:** Expecting plain SUM in a column to filter by row.

### Q34 ⭐⭐ 🟡 Write a DAX measure for the headcount of active employees using CALCULATE and COUNTROWS.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you combine CALCULATE, COUNTROWS and a Boolean filter for the most common HR measure?
**Say this in the interview:** "Active Headcount = CALCULATE(COUNTROWS(Employees), Employees[Status] = \"Active\"). COUNTROWS counts the employee rows and CALCULATE restricts them to Active."
**Explain simply:**
- COUNTROWS counts rows left after filters.
- CALCULATE adds the filter Status = "Active" to whatever the visual already filters (e.g. department).
- Assumes one row per employee.
**Example:** Seven rows, two resigned.
**Sample data:**

Table `Employees`:

| Emp | Dept | Status |
|---|---|---|
| E01 | IT | Active |
| E02 | IT | Resigned |
| E03 | HR | Active |
| E04 | HR | Active |
| E05 | Sales | Active |
| E06 | Sales | Resigned |
| E07 | IT | Active |

**DAX / Steps (not run here):**
```dax
Active Headcount =
CALCULATE ( COUNTROWS ( Employees ), Employees[Status] = "Active" )
```
**Alternative:** `COUNTROWS ( FILTER ( Employees, Employees[Status] = "Active" ) )`; same answer, usually less efficient (from memory).
**Result (reproduced with pandas):** HR 2, IT 2, Sales 1; total 5 (all rows 7).
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"Emp":["E01","E02","E03","E04","E05","E06","E07"],
 "Dept":["IT","IT","HR","HR","Sales","Sales","IT"],
 "Status":["Active","Resigned","Active","Active","Active","Resigned","Active"]})
act = emp[emp["Status"]=="Active"]
print(act.groupby("Dept").size())
print("Total active:", len(act), "| all rows:", len(emp))
```
```
Dept
HR       2
IT       2
Sales    1
dtype: int64
Total active: 5 | all rows: 7
```
**Version / licensing note:** Learn unreachable here; CALCULATE page fetched earlier per sources file. Rest from memory, unverified.
**Edge cases:** A Status slicer set to Resigned is overridden by this filter (see Q37). If employees repeat monthly, use DISTINCTCOUNT of Emp instead. Departments with none return BLANK.
**Likely follow-ups:** 1) Unique count? DISTINCTCOUNT. 2) Active on a date? Needs join date and exit date conditions.
**Common mistakes:** Counting a snapshot table with many months; typos in "Active".

### Q35 ⭐⭐ 🟡 Write a DAX measure for attendance percentage.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you build a ratio of two filtered counts and define the denominator clearly?
**Say this in the interview:** "Attendance % is present days divided by total working days. I use DIVIDE so a blank or zero denominator is safe, and I say clearly whether leave days count in the denominator."
**Explain simply:**
- Numerator: rows where Status = Present.
- Denominator: all rows, or rows excluding approved leave, a policy choice you must state.
- DIVIDE avoids divide-by-zero errors.
**Example:** E01 present 4 of 5 days = 80%.
**Sample data:**

Table `Attendance` (5 days each):

| Emp | Status |
|---|---|
| E01 | Present, Present, Present, Absent, Present |
| E02 | Present, Absent, Absent, Present, Leave |

**DAX / Steps (not run here):**
```dax
Present Days = CALCULATE ( COUNTROWS ( Attendance ), Attendance[Status] = "Present" )
Attendance % = DIVIDE ( [Present Days], COUNTROWS ( Attendance ) )
Attendance % (excl Leave) =
DIVIDE ( [Present Days], CALCULATE ( COUNTROWS ( Attendance ), Attendance[Status] <> "Leave" ) )
```
Format the measure as Percentage: Measure tools > Format (not run here).
**Alternative:** Mark each row 1 or 0 in a column and use AVERAGE.
**Result (reproduced with pandas):** E01 80.0%, E02 40.0%, overall 60.0%; excluding Leave overall 66.7% (by hand, E02 becomes 2/4 = 50%).
**Pandas check:**
```python
import pandas as pd
a = pd.DataFrame({"Emp":["E01"]*5+["E02"]*5,
 "Status":["Present","Present","Present","Absent","Present","Present","Absent","Absent","Present","Leave"]})
g = a.groupby("Emp")["Status"].agg(Days="size", Present=lambda x:(x=="Present").sum())
g["Pct"] = (g["Present"]/g["Days"]*100).round(1)
print(g)
print("Overall:", round((a["Status"]=="Present").mean()*100,1))
w = a[a["Status"]!="Leave"]
print("Excluding Leave, overall:", round((w["Status"]=="Present").mean()*100,1))
```
```
     Days  Present   Pct
Emp                     
E01     5        4  80.0
E02     5        2  40.0
Overall: 60.0
Excluding Leave, overall: 66.7
```
**Version / licensing note:** Learn unreachable here; DIVIDE behaviour (BLANK on zero denominator) is per the DIVIDE page fetched earlier (sources file). Rest from memory, unverified.
**Edge cases:** Holidays and weekends should not be rows or must be excluded. Half-days. Joiners mid-month have fewer working days.
**Likely follow-ups:** 1) Overall vs average of individuals? Differ; say which. 2) Late count? Q24.
**Common mistakes:** Not stating the denominator; dividing with `/`; averaging percentages.

### Q36 ⭐⭐ 🟡 How does CALCULATE treat several filter arguments?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know multiple filters combine with AND?
**Say this in the interview:** "Each filter argument narrows the data further, so several filters are combined with AND, and rows must satisfy all of them. If I need OR, I put both conditions in one filter, for example with IN or ||."
**Explain simply:**
- Separate arguments = AND (per the CALCULATE page, fetched earlier, as summarised in the sources file).
- Two different filters on the same column, like Dept = "IT" and Dept = "HR", leave nothing, so the result is blank.
- For OR on one column use `Dept IN {"IT","HR"}`.
**Example:** Headcount IT AND Hyderabad.
**Sample data:**

Table `Employees`:

| Emp | Dept | Location |
|---|---|---|
| E01 | IT | Hyderabad |
| E02 | IT | Bengaluru |
| E03 | HR | Hyderabad |
| E04 | IT | Hyderabad |
| E05 | Sales | Bengaluru |

**DAX / Steps (not run here):**
```dax
IT in Hyd = CALCULATE ( COUNTROWS ( Employees ), Employees[Dept] = "IT", Employees[Location] = "Hyderabad" )
IT and HR (empty) = CALCULATE ( COUNTROWS ( Employees ), Employees[Dept] = "IT", Employees[Dept] = "HR" )
IT or HR = CALCULATE ( COUNTROWS ( Employees ), Employees[Dept] IN { "IT", "HR" } )
```
**Alternative:** `FILTER` with `||` for OR across different columns.
**Result (reproduced with pandas):** IT AND Hyderabad = 2; IT AND HR = 0 (blank in DAX); IT OR HR = 4.
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"Emp":["E01","E02","E03","E04","E05"],
 "Dept":["IT","IT","HR","IT","Sales"],"Location":["Hyderabad","Bengaluru","Hyderabad","Hyderabad","Bengaluru"]})
print("IT AND Hyderabad:", len(emp[(emp.Dept=="IT")&(emp.Location=="Hyderabad")]))
print("IT AND HR (same column):", len(emp[(emp.Dept=="IT")&(emp.Dept=="HR")]))
print("IT OR HR:", len(emp[emp.Dept.isin(["IT","HR"])]))
```
```
IT AND Hyderabad: 2
IT AND HR (same column): 0
IT OR HR: 4
```
**Version / licensing note:** Microsoft Learn: CALCULATE function (DAX) as fetched earlier (per sources file); not re-fetched, Learn unreachable here.
**Edge cases:** In DAX the empty case returns BLANK, shown as 0 only in pandas. Existing slicers also apply (Q37).
**Likely follow-ups:** 1) OR across columns? FILTER with ||. 2) Order of filters matter? No for plain filters (from memory).
**Common mistakes:** Writing two filters on one column expecting OR.

### Q37 ⭐⭐ 🟡 What happens when a CALCULATE filter targets a column that already has a slicer selection?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know CALCULATE overwrites the existing filter on that column?
**Say this in the interview:** "CALCULATE replaces the existing filter on that same column, so the slicer is overridden for that column. Filters on other columns still apply. If I want both to apply, I wrap my filter in KEEPFILTERS."
**Explain simply:**
- Per the CALCULATE page (fetched earlier per the sources file): a filter on a column overwrites existing filters on that column; filters on other columns are added.
- Slicer = HR, measure forces Dept = "IT" -> the measure shows IT, ignoring the slicer.
- KEEPFILTERS keeps the slicer and intersects (from memory, unverified: the KEEPFILTERS page was not read).
**Example:** A card "IT headcount" next to a Department slicer. It keeps showing IT even if HR is selected, which is often intended.
**Sample data:**

Table `Employees`:

| Emp | Dept |
|---|---|
| E01 | IT |
| E02 | IT |
| E03 | HR |
| E04 | HR |
| E05 | Sales |

**DAX / Steps (not run here):**
```dax
IT HC = CALCULATE ( COUNTROWS ( Employees ), Employees[Dept] = "IT" )
IT HC (respect slicer) = CALCULATE ( COUNTROWS ( Employees ), KEEPFILTERS ( Employees[Dept] = "IT" ) )
```
**Alternative:** Use `ALL` (Part 5) to remove slicer on purpose, or `VALUES` plus `INTERSECT` for a custom mix.
**Result (reproduced with pandas):** Slicer = HR: plain CALCULATE gives 2; KEEPFILTERS gives 0 (blank). Slicer = HR+IT: KEEPFILTERS gives 2.
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"Emp":["E01","E02","E03","E04","E05"],"Dept":["IT","IT","HR","HR","Sales"]})
slicer = ["HR"]
plain = len(emp[emp.Dept=="IT"])                                   # filter replaces slicer
keep = len(emp[emp.Dept.isin(slicer) & (emp.Dept=="IT")])           # KEEPFILTERS: both apply
keep2 = len(emp[emp.Dept.isin(["HR","IT"]) & (emp.Dept=="IT")])
print("Slicer=HR  plain CALCULATE:", plain, "| KEEPFILTERS:", keep)
print("Slicer=HR+IT KEEPFILTERS:", keep2)
```
```
Slicer=HR  plain CALCULATE: 2 | KEEPFILTERS: 0
Slicer=HR+IT KEEPFILTERS: 2
```
**Version / licensing note:** Microsoft Learn: CALCULATE function (DAX) fetched earlier (sources file); KEEPFILTERS not read. Learn unreachable now.
**Edge cases:** A slicer on a different column (Location) combines normally. Cross-filtering from other visuals acts like slicers. Row-level security filters are not overwritten (from memory, unverified).
**Likely follow-ups:** 1) How to ignore the slicer fully? ALL. 2) KEEPFILTERS use? Respect user selection.
**Common mistakes:** Expecting the slicer and the measure to both apply; being surprised the card ignores the slicer.

### Q38 ⭐⭐ 🟡 What is the difference between a Boolean filter and the FILTER function inside CALCULATE?
**Asked at:** commonly asked (no company-specific report found); Weekday's 2026 India prep article lists it among its questions (per sources file).
**What the interviewer is checking:** Do you know when the simple filter is enough and when you need FILTER?
**Say this in the interview:** "A Boolean filter is a simple true/false test on one column, like Salary > 50000. FILTER lets me go row by row over a table and test several columns or a measure. I use the Boolean form whenever it works, and FILTER when I need more."
**Explain simply:**
- Boolean filter: `Employees[Salary] > 50000` inside CALCULATE. It can refer to one column only and cannot use a measure (per the CALCULATE page, fetched earlier per the sources file).
- FILTER(table, condition): returns a table of rows where the condition holds; the condition can compare two columns, or use a measure.
- Behind the scenes a Boolean filter is treated like a filter on that column's values, so it is simple and fast (from memory).
**Example:** Payroll of employees earning above 50,000 (Boolean) vs those whose bonus is above allowance (needs FILTER, two columns).
**Sample data:**

Table `Employees`:

| Emp | Salary | Bonus | Allowance |
|---|---|---|---|
| E01 | 60000 | 5000 | 6000 |
| E02 | 45000 | 2000 | 1500 |
| E03 | 72000 | 9000 | 8000 |
| E04 | 48000 | 1000 | 3000 |
| E05 | 52000 | 4000 | 3000 |

**DAX / Steps (not run here):**
```dax
High Earner Payroll = CALCULATE ( SUM ( Employees[Salary] ), Employees[Salary] > 50000 )
Bonus > Allowance Payroll =
CALCULATE ( SUM ( Employees[Salary] ), FILTER ( Employees, Employees[Bonus] > Employees[Allowance] ) )
```
**Alternative:** Or `SUMX ( FILTER ( ... ), Employees[Salary] )` (Q39).
**Result (reproduced with pandas):** Boolean: 184000 (E01, E03, E05). FILTER: 169000 (E02, E03, E05).
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"Emp":["E01","E02","E03","E04","E05"],"Salary":[60000,45000,72000,48000,52000],
 "Bonus":[5000,2000,9000,1000,4000],"Allowance":[6000,1500,8000,3000,3000]})
print("Boolean Salary>50000 :", emp[emp.Salary>50000].Salary.sum())
print("FILTER Bonus>Allowance:", emp[emp.Bonus>emp.Allowance].Salary.sum(), list(emp[emp.Bonus>emp.Allowance].Emp))
```
```
Boolean Salary>50000 : 184000
FILTER Bonus>Allowance: 169000 ['E02', 'E03', 'E05']
```
**Version / licensing note:** Microsoft Learn: CALCULATE function (DAX) fetched earlier per sources file; FILTER page not read; Learn unreachable here.
**Edge cases:** `FILTER(Employees, ...)` respects other filters on Employees; `FILTER(ALL(col), ...)` ignores them. A FILTER on a whole big table can be slower.
**Likely follow-ups:** 1) Why not FILTER always? Slower and more complex. 2) Can a Boolean filter use a measure? No; use FILTER.
**Common mistakes:** Comparing two columns in a Boolean filter; filtering a whole fact table when one column is enough.

### Q39 ⭐⭐ 🟡 What is the difference between SUMX(FILTER(...)) and CALCULATE(SUM(...), ...)?
**Asked at:** commonly asked (no company-specific report found). The Deloitte Sept 2025 Power BI round reportedly included SUM vs SUMX (research/interview_processes.md); that is a related, not identical, question.
**What the interviewer is checking:** Do you know when to iterate row by row and, above all, how each version treats the filters already on the report?
**Say this in the interview:** "Both can give the same number, but CALCULATE with a simple condition changes the filter on one column and is usually faster. SUMX over FILTER walks the table row by row and keeps whatever slicers are already applied, so it cannot widen the filter."
**Explain simply:**
- FILTER(table, condition) returns the rows that pass a test. SUMX adds up an expression over those rows, one row at a time (an iterator, meaning a function that loops over rows).
- CALCULATE(SUM(col), condition) changes the filter context (the set of filters currently applied by slicers, rows and columns of the visual) and then sums.
- A simple Boolean condition like Sales[Region] = "North" inside CALCULATE replaces any existing filter on Region. FILTER(Sales, ...) is evaluated inside the current filter context, so it only narrows further.
- Use SUMX when the sum needs a row-level calculation (Qty * Price); use CALCULATE for plain column sums with a condition.
**Example:** The Region slicer is on South, but a card should always show North revenue for comparison.
**Sample data:** Table `Sales`:

| OrderID | Region | Amount |
|---|---|---|
| O1 | North | 4,000 |
| O2 | North | 12,000 |
| O3 | South | 8,000 |
| O4 | South | 15,000 |
| O5 | East | 6,000 |
| O6 | North | 9,500 |

**DAX / Steps:** (not run here (no DAX engine in this environment))
```dax
-- Version 1: iterate over filtered rows
Big Orders SUMX = SUMX(FILTER(Sales, Sales[Amount] > 5000), Sales[Amount])

-- Version 2: change the filter, then sum
Big Orders CALC = CALCULATE(SUM(Sales[Amount]), Sales[Amount] > 5000)

-- Region test (slicer on South)
North SUMX = SUMX(FILTER(Sales, Sales[Region] = "North"), Sales[Amount])
North CALC = CALCULATE(SUM(Sales[Amount]), Sales[Region] = "North")
```
**Alternative:** For one text condition, CALCULATE with a Boolean filter is the simplest. Use FILTER inside CALCULATE only when the condition compares a measure or two columns.
**Result:** reproduced with pandas: with no slicer both Big Orders measures return 50,500. With the slicer on South, North SUMX returns blank (South rows filtered to North leaves nothing) and North CALC returns 25,500.
**Pandas check:**
```python
import pandas as pd
sales = pd.DataFrame({"OrderID":["O1","O2","O3","O4","O5","O6"],
 "Region":["North","North","South","South","East","North"],
 "Amount":[4000,12000,8000,15000,6000,9500]})
# A) amount > 5000, no slicer
a = sales[sales.Amount>5000].Amount.sum()
print("A) Amount>5000, no slicer: both measures =", a)
# B) slicer Region=South, measure asks for North
ctx = sales[sales.Region=="South"]                 # filter context from slicer
sumx_filter = ctx[ctx.Region=="North"].Amount.sum() if len(ctx[ctx.Region=="North"]) else None
calc = sales[sales.Region=="North"].Amount.sum()   # CALCULATE overwrites the Region filter
print("B) slicer=South | SUMX(FILTER(Sales,Region=North)):", sumx_filter, "| CALCULATE(SUM,Region=North):", calc)
```
Output (run):
```
A) Amount>5000, no slicer: both measures = 50500
B) slicer=South | SUMX(FILTER(Sales,Region=North)): None | CALCULATE(SUM,Region=North): 25500
```
**Version / licensing note:** Same in Power BI Desktop and Service models (Desktop is where you author; from memory, unverified). Microsoft Learn was unreachable from this session (learn.microsoft.com did not resolve), so I could not re-fetch function pages; DAX syntax is checked against my knowledge of the function pages, not freshly fetched. Earlier research (research/Book04_Part04_sources.md) fetched Microsoft Learn pages CALCULATE, DIVIDE vs / operator, COUNTROWS and SUMX; I did not re-read them.
**Edge cases:** FILTER over a whole big table is slower than a column filter. If nothing passes the filter, SUMX returns blank, not 0. Passing a whole table to FILTER keeps all columns, so it can also inherit filters from related columns.
**Likely follow-ups:** 1) *Which is faster?* Usually CALCULATE with a Boolean filter, because the engine filters one column. 2) *Can SUM take Qty * Price?* No, SUM takes one column; use SUMX.
**Common mistakes:** Assuming both always give the same result; using SUMX(FILTER()) when a plain CALCULATE would do; expecting SUMX(FILTER()) to override a slicer.

### Q40 ⭐⭐ 🟡 Write a DAX measure for profit margin percentage.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you divide totals (not average row percentages) and handle zero revenue safely?
**Say this in the interview:** "Profit margin is profit divided by revenue. I write it as a measure using DIVIDE so a zero or blank revenue shows blank instead of an error, and the grand total comes out right because it divides the totals."
**Explain simply:**
- Profit = Revenue minus Cost. Margin % = Profit / Revenue.
- A measure is a formula calculated on the fly for whatever the report is showing (rows, filters). That is why the total row divides total profit by total revenue.
- DIVIDE returns BLANK when the denominator is zero or blank (per the DIVIDE vs / operator page cited in my sources file).
- Format the measure as Percentage in Measure tools; do not multiply by 100 in the formula.
**Example:** A retail chain with three product categories.
**Sample data:** Table `Sales`, totals by category:

| Category | Revenue | Cost |
|---|---|---|
| Electronics | 100,000 | 80,000 |
| Apparel | 50,000 | 30,000 |
| Services | 0 | 500 |

**DAX / Steps:** (not run here (no DAX engine in this environment))
```dax
Total Revenue = SUM(Sales[Revenue])
Total Cost = SUM(Sales[Cost])
Profit Margin % = DIVIDE([Total Revenue] - [Total Cost], [Total Revenue])
```
Steps (from memory, unverified): Home > Calculations > New measure, paste, then Measure tools > Format > Percentage.
**Alternative:** Reuse a Profit measure: `Profit = [Total Revenue] - [Total Cost]` then `Profit Margin % = DIVIDE([Profit], [Total Revenue])`.
**Result:** reproduced with pandas: Electronics 20.0%, Apparel 40.0%, Services blank, grand total 26.33%. Averaging the row margins would wrongly give 30.0%.
**Pandas check:**
```python
import pandas as pd
d = pd.DataFrame({"Category":["Electronics","Apparel","Services"],"Revenue":[100000,50000,0],"Cost":[80000,30000,500]})
d["Margin %"] = ((d.Revenue-d.Cost)/d.Revenue.where(d.Revenue!=0)*100).round(1)
print(d)
rev, cost = d.Revenue.sum(), d.Cost.sum()
print("Total margin % (ratio of sums):", round((rev-cost)/rev*100,2))
print("Average of row margins (wrong):", round(d["Margin %"].mean(),2))
```
Output (run):
```
      Category  Revenue   Cost  Margin %
0  Electronics   100000  80000      20.0
1      Apparel    50000  30000      40.0
2     Services        0    500       NaN
Total margin % (ratio of sums): 26.33
Average of row margins (wrong): 30.0
```
**Version / licensing note:** Same in Power BI Desktop and Service models (Desktop is where you author; from memory, unverified). Microsoft Learn was unreachable from this session (learn.microsoft.com did not resolve), so I could not re-fetch function pages; DAX syntax is checked against my knowledge of the function pages, not freshly fetched. Earlier research (research/Book04_Part04_sources.md) fetched Microsoft Learn pages CALCULATE, DIVIDE vs / operator, COUNTROWS and SUMX; I did not re-read them.
**Edge cases:** Zero revenue returns blank (not 0%). Negative margin is valid for loss-making rows. Margin on revenue differs from markup on cost; confirm which the business wants.
**Likely follow-ups:** 1) *Why not use /?* It errors or shows infinity when revenue is 0. 2) *Why is the total not 30%?* Total margin is a ratio of sums, not an average of row margins.
**Common mistakes:** Averaging margin percentages; storing margin as a column and summing it; dividing by cost instead of revenue.

### Q41 ⭐⭐ 🟡 Write a DAX measure for each department's share of total headcount.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Percent of total: can you make the denominator ignore the row's own department filter?
**Say this in the interview:** "The numerator is the headcount in the current department. The denominator is the headcount with the department filter removed, using CALCULATE and ALL on the department column, then DIVIDE."
**Explain simply:**
- In a table with one row per department, each row filters Employees to that department. COUNTROWS alone gives that department only.
- ALL(Employees[Dept]) removes the filter on Dept only (ALL and ALLEXCEPT are covered in depth in Part 5). CALCULATE applies that change.
- Other filters (for example a Location slicer) still apply, so the shares always add to 100% of what you selected.
**Example:** A 10-person company: HR 2, IT 5, Sales 3.
**Sample data:** Table `Employees`:

| EmpID | Dept |
|---|---|
| 1-2 | HR |
| 3-7 | IT |
| 8-10 | Sales |

(10 rows, one per employee.)
**DAX / Steps:** (not run here (no DAX engine in this environment))
```dax
Headcount = COUNTROWS(Employees)
Dept Share % = DIVIDE([Headcount], CALCULATE([Headcount], ALL(Employees[Dept])))
```
Format as Percentage.
**Alternative:** Use ALLSELECTED(Employees[Dept]) so the share is out of the departments the user has selected in a slicer (from memory, unverified); or the visual's built-in "Show value as > Percent of grand total" (from memory, unverified).
**Result:** reproduced with pandas: HR 20.0%, IT 50.0%, Sales 30.0%, total 100.0%.
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"EmpID":range(1,11),"Dept":["HR"]*2+["IT"]*5+["Sales"]*3})
share = (emp.groupby("Dept").size()/len(emp)*100).round(1)
print(share.to_string()); print("Total:", share.sum())
```
Output (run):
```
Dept
HR       20.0
IT       50.0
Sales    30.0
Total: 100.0
```
**Version / licensing note:** Same in Power BI Desktop and Service models (Desktop is where you author; from memory, unverified). Microsoft Learn was unreachable from this session (learn.microsoft.com did not resolve), so I could not re-fetch function pages; DAX syntax is checked against my knowledge of the function pages, not freshly fetched. Earlier research (research/Book04_Part04_sources.md) fetched Microsoft Learn pages CALCULATE, DIVIDE vs / operator, COUNTROWS and SUMX; I did not re-read them.
**Edge cases:** The grand total row shows 100%. With no employees the denominator is blank and DIVIDE returns blank. Blank departments form their own group.
**Likely follow-ups:** 1) *ALL vs ALLSELECTED?* ALL ignores every filter on that column; ALLSELECTED respects the user's slicer choice. 2) *Why use DIVIDE?* Safe against zero.
**Common mistakes:** Using ALL(Employees), which removes every filter including Location slicers; dividing by a hard-coded number; forgetting percentage format.

### Q42 ⭐⭐ 🟡 Write a DAX measure for net sales when the table has MRP and discount percentage columns.
**Asked at:** Reported in one Deloitte Bengaluru Glassdoor review (June 2025, a 3-5 year role, single anecdote, seen as a search snippet only): a DAX prompt for net sales from MRP, discount and net-sale columns. Not verified further.
**What the interviewer is checking:** Can you do row-by-row arithmetic (price times quantity less discount) and then total it?
**Say this in the interview:** "Net sales is MRP times quantity times one minus the discount fraction, per row. SUM cannot multiply two columns, so I use SUMX, which does the maths on each row and then adds it up."
**Explain simply:**
- MRP (maximum retail price) is the list price. Net sale is what the customer actually pays after discount.
- SUMX is an iterator: it evaluates the expression for every row and then sums the results.
- If the discount is stored as 10 instead of 0.10, divide by 100 first.
- The question does not mention quantity. If each row is one unit, drop Qty.
**Example:** Four orders with different discounts.
**Sample data:** Table `Sales`:

| OrderID | MRP | Qty | DiscPct |
|---|---|---|---|
| A1 | 1,000 | 2 | 0.10 |
| A2 | 500 | 4 | 0.20 |
| A3 | 2,000 | 1 | 0.00 |
| A4 | 800 | 5 | 0.25 |

**DAX / Steps:** (not run here (no DAX engine in this environment))
```dax
Net Sales = SUMX(Sales, Sales[MRP] * Sales[Qty] * (1 - Sales[DiscPct]))
```
**Alternative:** Add a calculated column `NetSale = Sales[MRP] * Sales[Qty] * (1 - Sales[DiscPct])` and use `Net Sales = SUM(Sales[NetSale])`. It is stored in the model, so it uses more memory.
**Result:** reproduced with pandas: row net sales 1,800 / 1,600 / 2,000 / 3,000, total 8,400.
**Pandas check:**
```python
import pandas as pd
s = pd.DataFrame({"OrderID":["A1","A2","A3","A4"],"MRP":[1000,500,2000,800],"Qty":[2,4,1,5],"DiscPct":[0.10,0.20,0.0,0.25]})
s["NetSale"] = s.MRP*s.Qty*(1-s.DiscPct)
print(s); print("Net sales total:", s.NetSale.sum())
```
Output (run):
```
  OrderID   MRP  Qty  DiscPct  NetSale
0      A1  1000    2     0.10   1800.0
1      A2   500    4     0.20   1600.0
2      A3  2000    1     0.00   2000.0
3      A4   800    5     0.25   3000.0
Net sales total: 8400.0
```
**Version / licensing note:** Same in Power BI Desktop and Service models (Desktop is where you author; from memory, unverified). Microsoft Learn was unreachable from this session (learn.microsoft.com did not resolve), so I could not re-fetch function pages; DAX syntax is checked against my knowledge of the function pages, not freshly fetched. Earlier research (research/Book04_Part04_sources.md) fetched Microsoft Learn pages CALCULATE, DIVIDE vs / operator, COUNTROWS and SUMX; I did not re-read them.
**Edge cases:** Blank discount is treated as 0 in arithmetic (from memory, unverified), so full price is charged; check whether blank means missing. Returns are negative quantities. Discount over 100% gives negative sales.
**Likely follow-ups:** 1) *Why not SUM(MRP) * ...?* That multiplies totals, which is wrong when discounts differ per row. 2) *Measure or column?* Measure, to save memory.
**Common mistakes:** Applying the average discount to total MRP; treating 10 as 10 times; using SUM with a multiplication.

### Q43 ⭐⭐ 🟡 How would you count unique customers when customer IDs are spread across several tables?
**Asked at:** Reported in one Deloitte Bengaluru Glassdoor review (June 2025, single anecdote, search snippet only): count unique customers when IDs sit in different tables. Not verified further.
**What the interviewer is checking:** Do you know DISTINCTCOUNT only works on one column, and can you combine columns from two tables without double counting?
**Say this in the interview:** "I stack the customer ID columns from both tables with UNION, remove duplicates with DISTINCT, and count the rows. In a good model I would build one Customer table and count that instead."
**Explain simply:**
- A customer who bought online and in store appears in both tables; adding two distinct counts would count them twice.
- VALUES gives the distinct values of a column; UNION stacks tables with the same number of columns and keeps duplicates; DISTINCT then removes the repeats (UNION keeping duplicates is from memory, unverified).
- Best practice is a separate Customer dimension table with one row per customer, linked to both tables (modelling is covered in Part 3).
**Example:** Online sales and store sales both carry CustID.
**Sample data:** Table `Online`: C1, C2, C3, C2. Table `Store`: C3, C4, C5, C1.
**DAX / Steps:** (not run here (no DAX engine in this environment))
```dax
Unique Customers =
COUNTROWS(
    DISTINCT(
        UNION(
            VALUES(Online[CustID]),
            VALUES(Store[CustID])
        )
    )
)
```
**Alternative:** With a `Customers` dimension: `Unique Customers = DISTINCTCOUNT(Customers[CustID])`, with relationships to both fact tables.
**Result:** reproduced with pandas: unique customers 5 (C1 to C5). Adding the two separate distinct counts would give 7, which is wrong.
**Pandas check:**
```python
import pandas as pd
online = pd.DataFrame({"CustID":["C1","C2","C3","C2"]})
store  = pd.DataFrame({"CustID":["C3","C4","C5","C1"]})
union = pd.concat([online.CustID, store.CustID])
print("UNION rows (duplicates kept):", len(union))
print("Unique customers:", union.nunique())
print("Sum of separate distinct counts (wrong):", online.CustID.nunique()+store.CustID.nunique())
```
Output (run):
```
UNION rows (duplicates kept): 8
Unique customers: 5
Sum of separate distinct counts (wrong): 7
```
**Version / licensing note:** Same in Power BI Desktop and Service models (Desktop is where you author; from memory, unverified). Microsoft Learn was unreachable from this session (learn.microsoft.com did not resolve), so I could not re-fetch function pages; DAX syntax is checked against my knowledge of the function pages, not freshly fetched. Earlier research (research/Book04_Part04_sources.md) fetched Microsoft Learn pages CALCULATE, DIVIDE vs / operator, COUNTROWS and SUMX; I did not re-read them.
**Edge cases:** Blank IDs count as one extra value in DISTINCT. IDs stored as text in one table and numbers in the other will not match. Trailing spaces make "C1 " different from "C1".
**Likely follow-ups:** 1) *Why not DISTINCTCOUNT(Online[CustID]) + DISTINCTCOUNT(Store[CustID])?* Overlap double counts. 2) *Cleaner way?* A customer dimension.
**Common mistakes:** Adding two distinct counts; using UNION without DISTINCT; ignoring data type mismatch.

### Q44 ⭐⭐ 🟡 Why does a calculated column that uses SUM show the same total on every row?
**Asked at:** commonly asked (no company-specific report found). The Weekday 2026 prep guide lists "same total in every row" style questions (per sources file).
**What the interviewer is checking:** Do you understand that a calculated column has row context but no automatic filtering?
**Say this in the interview:** "In a calculated column, each row is processed one at a time, but SUM looks at the whole column because row context does not filter the table. To get a per-department total, I wrap it in CALCULATE, which turns the current row into a filter."
**Explain simply:**
- Row context means "the row being calculated right now". It lets you read this row's values, but does not filter other rows.
- SUM(Employees[Salary]) is an aggregation, so it uses filter context, which in a calculated column is empty, hence the whole-table total.
- CALCULATE converts the row context into filters (context transition), so the total is for rows matching this row.
- Safer: capture the department in a variable and filter explicitly.
**Example:** Show each employee's department payroll total.
**Sample data:** Table `Employees`:

| EmpID | Dept | Salary |
|---|---|---|
| 1 | HR | 40,000 |
| 2 | HR | 50,000 |
| 3 | IT | 60,000 |
| 4 | IT | 40,000 |

**DAX / Steps:** (calculated column; not run here (no DAX engine in this environment))
```dax
Wrong Total = SUM(Employees[Salary])
Dept Total = CALCULATE(SUM(Employees[Salary]))
```
Steps (from memory, unverified): Table view or Report view > Table tools > New column.
**Alternative:** Explicit and safer:
```dax
Dept Total 2 =
VAR d = Employees[Dept]
RETURN CALCULATE(SUM(Employees[Salary]), Employees[Dept] = d)
```
**Result:** reproduced with pandas: Wrong Total = 190,000 on all four rows; Dept Total = 90,000 for HR rows and 100,000 for IT rows.
**Pandas check:**
```python
import pandas as pd
e = pd.DataFrame({"EmpID":[1,2,3,4],"Dept":["HR","HR","IT","IT"],"Salary":[40000,50000,60000,40000]})
e["WrongCol (SUM)"] = e.Salary.sum()                       # no filter -> whole table
e["DeptTotal (CALCULATE)"] = e.groupby("Dept").Salary.transform("sum")
print(e)
```
Output (run):
```
   EmpID Dept  Salary  WrongCol (SUM)  DeptTotal (CALCULATE)
0      1   HR   40000          190000                  90000
1      2   HR   50000          190000                  90000
2      3   IT   60000          190000                 100000
3      4   IT   40000          190000                 100000
```
**Version / licensing note:** Same in Power BI Desktop and Service models (Desktop is where you author; from memory, unverified). Microsoft Learn was unreachable from this session (learn.microsoft.com did not resolve), so I could not re-fetch function pages; DAX syntax is checked against my knowledge of the function pages, not freshly fetched. Earlier research (research/Book04_Part04_sources.md) fetched Microsoft Learn pages CALCULATE, DIVIDE vs / operator, COUNTROWS and SUMX; I did not re-read them.
**Edge cases:** CALCULATE with context transition filters by all columns of the row, so identical duplicate rows merge into one filter and are summed together; use a unique key or the variable version. Calculated columns only refresh with the model.
**Likely follow-ups:** 1) *Would a measure show the same total?* No, a measure responds to filter context from the visual. 2) *What is context transition?* Row context turned into filter context by CALCULATE.
**Common mistakes:** Expecting SUM to see "this row"; using a calculated column for something that should be a measure.

### Q45 ⭐⭐ 🟡 Should you add a column in Power Query or as a DAX calculated column?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know where each column type is computed and which is better for model size and reuse?
**Say this in the interview:** "If it is a row-level fact that does not depend on report filters, I prefer Power Query, upstream, since it is clean and often foldable to the source. DAX calculated columns are for when I need other model tables (via RELATED) or measures. Anything that changes with slicers should be a measure."
**Explain simply:**
- Power Query (the "Transform data" editor, language M) runs when the data is refreshed, before it loads into the model.
- A DAX calculated column also runs at refresh, after load, and is stored in the model like any column (more memory).
- Query folding means Power Query pushes the step back to the source database to compute it; not every step folds (from memory, unverified).
- Power Query cannot see relationships in the model; DAX can.
**Example:** Splitting "Ananya Rao" into first and last name, or trimming employee codes, belongs in Power Query. Pulling the department's location via RELATED belongs in DAX.
**DAX / Steps:** (not run here (no DAX engine in this environment))
1. Power Query: Home > Transform data > Add Column > Custom Column (M), or Column From Examples.
2. DAX: Table view > Table tools > New column > type the formula.
**Alternative:** For anything that must respond to slicers, use a measure instead of either column.
**Version / licensing note:** from memory, unverified: both are available in Desktop and in the Service dataflows/semantic models. Microsoft Learn was unreachable from this session (learn.microsoft.com did not resolve), so I could not re-fetch function pages; no page on this was fetched.
**Edge cases:** Columns used as slicers or axes must be columns, not measures. A calculated column on a DirectQuery table is limited (from memory, unverified).
**Likely follow-ups:** 1) *Which is faster?* Power Query columns usually compress better and can fold. 2) *When must it be DAX?* When it needs relationships or measure logic.
**Common mistakes:** Building everything as calculated columns; adding columns in DAX that could be done in the source query; putting a ratio in a column and then summing it.

### Q46 ⭐⭐ 🟡 What does RELATED do, and why does it need row context?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand relationships, direction of lookup, and why row context is needed?
**Say this in the interview:** "RELATED brings in a value from the one-side table into the many-side table by following the relationship. It needs a row context because it must know which row to look up, so it works in calculated columns and inside iterators like SUMX, not directly in a measure."
**Explain simply:**
- A relationship links tables by a key (for example DeptID). The "one" side has unique keys (Departments); the "many" side repeats them (Employees).
- RELATED(Departments[Location]) written in Employees fetches the location of the current employee's department, like a VLOOKUP that uses the model relationship.
- Without a relationship, or with no current row, it errors. Going the other way (one to many) uses RELATEDTABLE.
**Example:** Add Location to each employee row.
**Sample data:** Table `Employees` (many side): EmpID 1-4 with DeptID 10, 20, 10, 30. Table `Departments` (one side):

| DeptID | Location |
|---|---|
| 10 | Hyderabad |
| 20 | Bengaluru |
| 30 | Pune |

**DAX / Steps:** (not run here (no DAX engine in this environment))
```dax
Location = RELATED(Departments[Location])   -- calculated column in Employees
```
In a measure use an iterator: `Hyd Staff = SUMX(Employees, IF(RELATED(Departments[Location]) = "Hyderabad", 1, 0))`.
**Alternative:** Filter by the dimension column instead: `CALCULATE(COUNTROWS(Employees), Departments[Location] = "Hyderabad")`. No RELATED is needed, because the relationship already filters Employees.
**Result:** reproduced with pandas (a merge, equivalent to the lookup): employees get Hyderabad, Bengaluru, Hyderabad, Pune.
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"EmpID":[1,2,3,4],"DeptID":[10,20,10,30]})
dept = pd.DataFrame({"DeptID":[10,20,30],"Location":["Hyderabad","Bengaluru","Pune"]})
out = emp.merge(dept, on="DeptID", how="left")  # RELATED = lookup on the one-side
print(out)
```
Output (run):
```
   EmpID  DeptID   Location
0      1      10  Hyderabad
1      2      20  Bengaluru
2      3      10  Hyderabad
3      4      30       Pune
```
**Version / licensing note:** Same in Power BI Desktop and Service models (Desktop is where you author; from memory, unverified). Microsoft Learn was unreachable from this session (learn.microsoft.com did not resolve), so I could not re-fetch function pages; DAX syntax is checked against my knowledge of the function pages, not freshly fetched. Earlier research (research/Book04_Part04_sources.md) fetched Microsoft Learn pages CALCULATE, DIVIDE vs / operator, COUNTROWS and SUMX; I did not re-read them.
**Edge cases:** Missing key gives blank. Many-to-many relationships make RELATED ambiguous (from memory, unverified). Inactive relationships are ignored.
**Likely follow-ups:** 1) *RELATED vs LOOKUPVALUE?* LOOKUPVALUE needs no relationship. 2) *Why not RELATED in a measure?* No row context there.
**Common mistakes:** Using RELATED from the one side; skipping the relationship; adding many lookup columns when a filter on the dimension would do.

### Q47 ⭐⭐ 🟡 Write a calculated column for employee tenure in years from the joining date.
**Asked at:** commonly asked (no company-specific report found). A Wipro 2023 Bangalore-Rural report mentioned DATEDIFF tasks (research/interview_processes.md); not a tenure question specifically.
**What the interviewer is checking:** Do you know DATEDIFF counts calendar boundaries crossed, not full elapsed years?
**Say this in the interview:** "The quick way is DATEDIFF with YEAR, but it counts year boundaries, so someone who joined on 31 December shows a year after one day. For real tenure I take the number of days and divide by 365.25, or use YEARFRAC."
**Explain simply:**
- DATEDIFF(start, end, YEAR) returns the difference of calendar years: 31 Dec 2020 to 1 Jan 2021 gives 1.
- Days divided by 365.25 (average year length) gives decimal tenure; round to 1 place.
- TODAY() changes each day; for audit reports use a fixed "as of" date.
**Example:** Joining dates against 31 Oct 2026 as the as-of date.
**Sample data:** Table `Employees`:

| EmpID | JoinDate |
|---|---|
| 1 | 2020-12-31 |
| 2 | 2022-03-15 |
| 3 | 2025-06-01 |

**DAX / Steps:** (calculated column; not run here (no DAX engine in this environment))
```dax
Tenure Years = ROUND(DATEDIFF(Employees[JoinDate], TODAY(), DAY) / 365.25, 1)
Tenure Years (boundary) = DATEDIFF(Employees[JoinDate], TODAY(), YEAR)
```
**Alternative:** `Tenure Years = YEARFRAC(Employees[JoinDate], TODAY(), 1)` for a fractional value (from memory, unverified, and not reproduced here). For whole years use INT of the result.
**Result:** reproduced with pandas using 2026-10-31 as the as-of date: boundary method gives 6, 4, 1; days/365.25 gives 5.8, 4.6, 1.4. The first employee shows how the boundary method overstates.
**Pandas check:**
```python
import pandas as pd
e = pd.DataFrame({"EmpID":[1,2,3],"JoinDate":pd.to_datetime(["2020-12-31","2022-03-15","2025-06-01"])})
asof = pd.Timestamp("2026-10-31")
e["DATEDIFF YEAR (boundaries)"] = asof.year - e.JoinDate.dt.year
e["Tenure (days/365.25, 1dp)"] = ((asof-e.JoinDate).dt.days/365.25).round(1)
print(e)
```
Output (run):
```
   EmpID   JoinDate  DATEDIFF YEAR (boundaries)  Tenure (days/365.25, 1dp)
0      1 2020-12-31                           6                        5.8
1      2 2022-03-15                           4                        4.6
2      3 2025-06-01                           1                        1.4
```
**Version / licensing note:** Same in Power BI Desktop and Service models (Desktop is where you author; from memory, unverified). Microsoft Learn was unreachable from this session (learn.microsoft.com did not resolve), so I could not re-fetch function pages; DAX syntax is checked against my knowledge of the function pages, not freshly fetched. Earlier research (research/Book04_Part04_sources.md) fetched Microsoft Learn pages CALCULATE, DIVIDE vs / operator, COUNTROWS and SUMX; I did not re-read them.
**Edge cases:** Blank join date returns blank. Future dates give negative tenure. A calculated column with TODAY() is only recalculated at refresh, so it ages between refreshes; a measure recalculates on query.
**Likely follow-ups:** 1) *Column or measure?* Measure if you need it current or averaged; column if you want to bucket by tenure. 2) *Whole years?* INT of the decimal.
**Common mistakes:** Trusting DATEDIFF YEAR as exact; using TODAY() in a report that needs a fixed date; showing Tenure as a date type.

### Q48 ⭐⭐ 🟡 Write a DAX measure for average order value.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you divide by the number of orders, not the number of rows?
**Say this in the interview:** "Average order value is total sales divided by the number of distinct orders. If the table is at order-line level, I use DISTINCTCOUNT on OrderID, with DIVIDE for safety."
**Explain simply:**
- One order can have several lines (items). Averaging the Amount column would give the average line, not the average order.
- DISTINCTCOUNT counts each OrderID once.
- If the table already has one row per order, AVERAGE of Amount is enough.
**Example:** 3 orders, 6 lines, Rs 2,700 in total.
**Sample data:** Table `OrderLines`:

| OrderID | Amount |
|---|---|
| O1 | 500 |
| O1 | 300 |
| O2 | 1,200 |
| O3 | 200 |
| O3 | 100 |
| O3 | 400 |

**DAX / Steps:** (not run here (no DAX engine in this environment))
```dax
AOV = DIVIDE(SUM(OrderLines[Amount]), DISTINCTCOUNT(OrderLines[OrderID]))
```
**Alternative:** With an Orders table at one row per order: `AOV = AVERAGE(Orders[Amount])` or `DIVIDE(SUM(Orders[Amount]), COUNTROWS(Orders))`.
**Result:** reproduced with pandas: 2,700 / 3 = Rs 900. AVERAGE of the line amounts gives 450, which is wrong for AOV.
**Pandas check:**
```python
import pandas as pd
l = pd.DataFrame({"OrderID":["O1","O1","O2","O3","O3","O3"],"Amount":[500,300,1200,200,100,400]})
print("Total:", l.Amount.sum(), "| distinct orders:", l.OrderID.nunique())
print("AOV =", round(l.Amount.sum()/l.OrderID.nunique(),2))
print("AVERAGE of line amounts (wrong for AOV):", round(l.Amount.mean(),2))
```
Output (run):
```
Total: 2700 | distinct orders: 3
AOV = 900.0
AVERAGE of line amounts (wrong for AOV): 450.0
```
**Version / licensing note:** Same in Power BI Desktop and Service models (Desktop is where you author; from memory, unverified). Microsoft Learn was unreachable from this session (learn.microsoft.com did not resolve), so I could not re-fetch function pages; DAX syntax is checked against my knowledge of the function pages, not freshly fetched. Earlier research (research/Book04_Part04_sources.md) fetched Microsoft Learn pages CALCULATE, DIVIDE vs / operator, COUNTROWS and SUMX; I did not re-read them.
**Edge cases:** Blank OrderID adds one distinct value (verify DISTINCTCOUNT blank handling; unverified here). Cancelled orders and returns need a filter. Total row divides total sales by total distinct orders, not an average of averages.
**Likely follow-ups:** 1) *Why DIVIDE?* No orders gives blank, not an error. 2) *Orders per customer?* DIVIDE of distinct orders by distinct customers.
**Common mistakes:** Using AVERAGE on a line-level table; COUNTROWS on lines; averaging the AOV column.

### Q49 ⭐⭐ 🟡 Write a DAX measure for total payroll cost when each row has basic pay and allowances columns.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Row-level addition across columns and blank handling.
**Say this in the interview:** "I use SUMX over the payroll table with Basic plus Allowances for each row. The same total also comes from adding SUM of each column, as long as the logic is purely additive."
**Explain simply:**
- Payroll cost per employee = basic pay + allowances. SUMX does that per row and adds up.
- For a purely additive formula, SUM(Basic) + SUM(Allowances) gives the same total; SUMX becomes necessary when you multiply or use IF per row.
- Blank allowance is treated as 0 when added (from memory, unverified), so the row still shows basic pay.
**Example:** Four employees; one has no allowance.
**Sample data:** Table `Payroll`:

| EmpID | Dept | Basic | Allowances |
|---|---|---|---|
| 1 | HR | 30,000 | 5,000 |
| 2 | HR | 35,000 | (blank) |
| 3 | IT | 50,000 | 8,000 |
| 4 | IT | 45,000 | 6,000 |

**DAX / Steps:** (not run here (no DAX engine in this environment))
```dax
Total Payroll Cost = SUMX(Payroll, Payroll[Basic] + Payroll[Allowances])
```
**Alternative:** `Total Payroll Cost = SUM(Payroll[Basic]) + SUM(Payroll[Allowances])` (identical here, and slightly simpler).
**Result:** reproduced with pandas (blank treated as 0): HR 70,000, IT 109,000, total 179,000.
**Pandas check:**
```python
import pandas as pd
import numpy as np
p = pd.DataFrame({"EmpID":[1,2,3,4],"Dept":["HR","HR","IT","IT"],"Basic":[30000,35000,50000,45000],"Allowances":[5000,np.nan,8000,6000]})
p["Row total"] = p.Basic + p.Allowances.fillna(0)    # DAX treats BLANK as 0 in +
print(p); print("Total payroll:", p["Row total"].sum())
print(p.groupby("Dept")["Row total"].sum().to_string())
```
Output (run):
```
   EmpID Dept  Basic  Allowances  Row total
0      1   HR  30000      5000.0    35000.0
1      2   HR  35000         NaN    35000.0
2      3   IT  50000      8000.0    58000.0
3      4   IT  45000      6000.0    51000.0
Total payroll: 179000.0
Dept
HR     70000.0
IT    109000.0
```
**Version / licensing note:** Same in Power BI Desktop and Service models (Desktop is where you author; from memory, unverified). Microsoft Learn was unreachable from this session (learn.microsoft.com did not resolve), so I could not re-fetch function pages; DAX syntax is checked against my knowledge of the function pages, not freshly fetched. Earlier research (research/Book04_Part04_sources.md) fetched Microsoft Learn pages CALCULATE, DIVIDE vs / operator, COUNTROWS and SUMX; I did not re-read them.
**Edge cases:** If blank were treated as blank (not 0) the row total would vanish; verify in your model. Deductions should be subtracted. Employer costs (PF) may be in another table.
**Likely follow-ups:** 1) *SUMX vs the SUM+SUM version?* Same here; SUMX if rows need extra logic. 2) *Add a bonus table?* Relate it and add another measure.
**Common mistakes:** Writing SUM(Payroll[Basic] + Payroll[Allowances]), which is invalid; forgetting blank cells; mixing monthly and annual figures.

### Q50 ⭐⭐ 🟡 What is SWITCH, and when do you use it instead of nested IF?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you write readable multi-way logic?
**Say this in the interview:** "SWITCH compares one expression with a list of values, or with SWITCH(TRUE(), ...) it tests several conditions in order and returns the first that is true. It is much easier to read than IFs nested inside IFs."
**Explain simply:**
- Nested IF: IF(a, x, IF(b, y, IF(c, z, w))) becomes hard to read with more than 2 levels.
- SWITCH(TRUE(), cond1, result1, cond2, result2, ..., default) stops at the first true condition.
- Order matters: put the strictest condition first.
- The last argument is the default if nothing matches.
**Example:** Performance bands for appraisal scores.
**Sample data:** Table `Appraisal`:

| EmpID | Score |
|---|---|
| 1 | 95 |
| 2 | 82 |
| 3 | 74 |
| 4 | 61 |
| 5 | 45 |
| 6 | (blank) |

**DAX / Steps:** (calculated column; not run here (no DAX engine in this environment))
```dax
Band =
SWITCH(
    TRUE(),
    Appraisal[Score] >= 90, "A",
    Appraisal[Score] >= 75, "B",
    Appraisal[Score] >= 60, "C",
    "D"
)
```
**Alternative:** Nested IF with the same thresholds; or for exact matches, `SWITCH(Emp[Grade], "L1", "Junior", "L2", "Mid", "Other")`.
**Result:** reproduced with pandas: A, B, C, C, D, D. The blank score lands in D because blank is compared like 0 (from memory, unverified); test ISBLANK first if that is wrong for you.
**Pandas check:**
```python
import pandas as pd
import numpy as np
s = pd.DataFrame({"EmpID":[1,2,3,4,5,6],"Score":[95,82,74,61,45,np.nan]})
def band(x):
    x = 0 if pd.isna(x) else x       # blank compared as 0
    return "A" if x>=90 else "B" if x>=75 else "C" if x>=60 else "D"
s["Band"] = s.Score.map(band); print(s)
```
Output (run):
```
   EmpID  Score Band
0      1   95.0    A
1      2   82.0    B
2      3   74.0    C
3      4   61.0    C
4      5   45.0    D
5      6    NaN    D
```
**Version / licensing note:** Same in Power BI Desktop and Service models (Desktop is where you author; from memory, unverified). Microsoft Learn was unreachable from this session (learn.microsoft.com did not resolve), so I could not re-fetch function pages; DAX syntax is checked against my knowledge of the function pages, not freshly fetched. Earlier research (research/Book04_Part04_sources.md) fetched Microsoft Learn pages CALCULATE, DIVIDE vs / operator, COUNTROWS and SUMX; I did not re-read them.
**Edge cases:** Missing default returns blank. Overlapping conditions: the first match wins. Blank vs 0.
**Likely follow-ups:** 1) *Why TRUE()?* So each condition is a true/false test. 2) *Can it return numbers?* Yes, but keep the return type consistent.
**Common mistakes:** Wrong order of conditions; no default; mixing text and number results.

### Q51 ⭐⭐ 🟡 What are VAR and RETURN in DAX, and why use them?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you write clean, reusable, debuggable measures?
**Say this in the interview:** "VAR stores a value or table under a name, and RETURN gives the final expression. I use it so each step has a name, a calculation is not repeated, and I can debug by returning one variable at a time."
**Explain simply:**
- A variable is a named calculation: VAR Leavers = ... defines it once; you use the name afterwards.
- It is calculated once where it is defined, and reused (from memory, unverified); this helps speed and readability.
- You can have many VARs, then a single RETURN.
- Debug trick: replace the RETURN expression with a variable name and check the number.
**Example:** Attrition rate with 12 employees, 3 of whom left.
**Sample data:** Table `Employees`: 12 rows, Status = "Left" for 3 and "Active" for 9.
**DAX / Steps:** (not run here (no DAX engine in this environment))
```dax
Attrition % =
VAR Leavers = CALCULATE(COUNTROWS(Employees), Employees[Status] = "Left")
VAR Total   = COUNTROWS(Employees)
RETURN DIVIDE(Leavers, Total)
```
**Alternative:** Separate measures `[Leavers]` and `[Total HC]` then `DIVIDE([Leavers], [Total HC])`, which are easier to reuse across reports.
**Result:** reproduced with pandas: 3 / 12 = 25.0%.
**Pandas check:**
```python
import pandas as pd
e = pd.DataFrame({"EmpID":range(1,13),"Status":["Left"]*3+["Active"]*9})
leavers=(e.Status=="Left").sum(); total=len(e)
print("Leavers",leavers,"Total",total,"Attrition %",round(leavers/total*100,1))
```
Output (run):
```
Leavers 3 Total 12 Attrition % 25.0
```
**Version / licensing note:** Same in Power BI Desktop and Service models (Desktop is where you author; from memory, unverified). Microsoft Learn was unreachable from this session (learn.microsoft.com did not resolve), so I could not re-fetch function pages; DAX syntax is checked against my knowledge of the function pages, not freshly fetched. Earlier research (research/Book04_Part04_sources.md) fetched Microsoft Learn pages CALCULATE, DIVIDE vs / operator, COUNTROWS and SUMX; I did not re-read them.
**Edge cases:** A variable keeps the filter context where it was defined, even if used later inside CALCULATE (from memory, unverified). Variables cannot be changed after definition.
**Likely follow-ups:** 1) *Does VAR improve speed?* Often, because repeated parts are calculated once. 2) *Can VAR hold a table?* Yes.
**Common mistakes:** Forgetting RETURN; naming a variable like a column; expecting a variable to re-evaluate in a new context.

### Q52 ⭐⭐ 🟡 How do you debug a DAX measure that returns a wrong number?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** A structured approach rather than guessing.
**Say this in the interview:** "I first check the number against a simple pivot or SQL on the raw data, then isolate whether the issue is the data, the filters on the visual, or the formula. I break the measure into VARs and test each piece."
**Explain simply:**
- Step 1: What is the expected value, and how did I get it (Excel pivot, source system)?
- Step 2: Check the data: text values with spaces, blanks, duplicates, wrong data types, wrong relationship.
- Step 3: Check the context: slicers, visual filters, page filters and relationships (direction, active/inactive).
- Step 4: Simplify the measure; show intermediate results in a table or card; return a VAR instead of the final value.
- Step 5: Use the DAX query view or Performance analyzer if available (availability from memory, unverified).
**Example:** "Active headcount" shows 4, but HR counts 5. Profiling the Status column shows one value typed as "Active " with a trailing space.
**Sample data:** Table `Employees`, Status values: Active x4, "Active " x1, Left x2.
**DAX / Steps:** (not run here) Debug measure: `Active Debug = CALCULATE(COUNTROWS(Employees), Employees[Status] = "Active")` returns 4, and a table visual with Status in rows shows the odd value. Fix in Power Query: Transform > Format > Trim.
**Alternative:** Test the same logic in another tool (SQL or pandas) on the same data and compare.
**Result:** reproduced with pandas: exact match 4; after trimming 5.
**Pandas check:**
```python
import pandas as pd
e = pd.DataFrame({"EmpID":range(1,8),"Status":["Active","Active","Active","Active ","Active","Left","Left"]})
print(e.Status.map(repr).value_counts().to_string())
print("Active (exact match):", (e.Status=="Active").sum(), "| after trimming:", (e.Status.str.strip()=="Active").sum())
```
Output (run):
```
Status
'Active'     4
'Left'       2
'Active '    1
Active (exact match): 4 | after trimming: 5
```
**Version / licensing note:** Same in Power BI Desktop and Service models (Desktop is where you author; from memory, unverified). Microsoft Learn was unreachable from this session (learn.microsoft.com did not resolve), so I could not re-fetch function pages; DAX syntax is checked against my knowledge of the function pages, not freshly fetched. Earlier research (research/Book04_Part04_sources.md) fetched Microsoft Learn pages CALCULATE, DIVIDE vs / operator, COUNTROWS and SUMX; I did not re-read them.
**Edge cases:** Many-to-many relationships, bidirectional filters and blank rows in dimensions create hidden mismatches. Cached visuals may be old: refresh first.
**Likely follow-ups:** 1) *What if the total is wrong but rows are right?* Totals use the total's context; see Q65. 2) *Where to test DAX?* DAX query view (Part 4 Q66).
**Common mistakes:** Changing the formula before checking data; trusting one visual; ignoring hidden filters.

### Q53 ⭐ 🟢 What is a calculated table, and when would you use one?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know a table can be created from a DAX expression and when that is appropriate?
**Say this in the interview:** "A calculated table is a new table created by a DAX formula, like a date table from CALENDAR. It is calculated on refresh and stored in the model. I use it for date tables, helper lists or a copy for a role-playing relationship."
**Explain simply:**
- "Calculated" means the result is saved in the file, not computed on the fly like a measure.
- Typical uses: a calendar table, a list of distinct departments, a small lookup table.
- If data can be prepared at source or in Power Query, that is usually preferred (simpler, smaller).
**Example:** A 2026 calendar table.
**Sample data:** `Calendar` = CALENDAR(DATE(2026,1,1), DATE(2026,12,31)); and a department list from the Employees table (HR, IT, Sales).
**DAX / Steps:** (not run here (no DAX engine in this environment))
```dax
Calendar = CALENDAR(DATE(2026, 1, 1), DATE(2026, 12, 31))
Dept List = DISTINCT(Employees[Dept])
```
Steps (from memory, unverified): Home > Calculations > New table, then type the formula.
**Alternative:** Create the table in Power Query (Enter data, or a query) or load it from a source.
**Result:** reproduced with pandas: 365 dates from 2026-01-01 to 2026-12-31; departments HR, IT, Sales.
**Pandas check:**
```python
import pandas as pd
cal = pd.date_range("2026-01-01","2026-12-31")
print("CALENDAR rows:", len(cal), "| first", cal[0].date(), "| last", cal[-1].date())
emp = pd.DataFrame({"Dept":["HR","IT","IT","Sales","HR"]})
print("DISTINCT(Emp[Dept]):", sorted(emp.Dept.unique()))
```
Output (run):
```
CALENDAR rows: 365 | first 2026-01-01 | last 2026-12-31
DISTINCT(Emp[Dept]): ['HR', 'IT', 'Sales']
```
**Version / licensing note:** Same in Power BI Desktop and Service models (Desktop is where you author; from memory, unverified). Microsoft Learn was unreachable from this session (learn.microsoft.com did not resolve), so I could not re-fetch function pages; DAX syntax is checked against my knowledge of the function pages, not freshly fetched. Earlier research (research/Book04_Part04_sources.md) fetched Microsoft Learn pages CALCULATE, DIVIDE vs / operator, COUNTROWS and SUMX; I did not re-read them.
**Edge cases:** Recomputed on every refresh; large calculated tables slow it. They are not available in some live-connection scenarios (from memory, unverified).
**Likely follow-ups:** 1) *Calculated table vs Power Query table?* Power Query for source data; DAX when it depends on the model. 2) *Mark as date table?* Yes, for time intelligence.
**Common mistakes:** Hard-coding date ranges that go out of date; loading huge tables as calculated tables.

### Q54 ⭐ 🟢 What happens if you use COUNT on a text column?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know COUNT is picky about data types and when to prefer COUNTROWS or DISTINCTCOUNT?
**Say this in the interview:** "I would avoid COUNT on text. Excel's COUNT only counts numbers, and I believe DAX's COUNT also expects numbers or dates, so for text I would use COUNTA or COUNTROWS, or DISTINCTCOUNT for unique names, and test it in my model."
**Explain simply:**
- Premise note: behaviour on text is the unclear part. Recall differs between sources, and a Microsoft page could not be fetched here, so treat any claim as unverified and test it on the actual column.
- COUNT is meant for numeric (and date) columns. COUNTA counts any non-blank value. COUNTROWS counts table rows. DISTINCTCOUNT counts unique values.
- To count employees, count rows of the employee table or distinct IDs, not a name column.
**Example:** A column of 5 employee names, one blank.
**Sample data:** Table `Employees`, Name: Asha, Ravi, (blank), Meena, Ravi.
**DAX / Steps:** (not run here (no DAX engine in this environment))
```dax
Names Filled = COUNTA(Employees[Name])
Rows = COUNTROWS(Employees)
Unique Names = DISTINCTCOUNT(Employees[Name])
```
**Alternative:** If you only need a number of people, `DISTINCTCOUNT(Employees[EmpID])`.
**Result:** reproduced with pandas (non-blank count, which is what COUNTA returns): 4 non-blank, 5 rows, 3 distinct names. What COUNT itself returns on text is unverified.
**Pandas check:**
```python
import pandas as pd
names = pd.Series(["Asha","Ravi",None,"Meena","Ravi"])
print("Non-blank count (what COUNT should return if it counts strings):", names.count())
print("Rows (COUNTROWS):", len(names), "| distinct non-blank:", names.nunique())
```
Output (run):
```
Non-blank count (what COUNT should return if it counts strings): 4
Rows (COUNTROWS): 5 | distinct non-blank: 3
```
**Version / licensing note:** Same in Power BI Desktop and Service models (Desktop is where you author; from memory, unverified). Microsoft Learn was unreachable from this session (learn.microsoft.com did not resolve), so I could not re-fetch function pages; DAX syntax is checked against my knowledge of the function pages, not freshly fetched. Earlier research (research/Book04_Part04_sources.md) fetched Microsoft Learn pages CALCULATE, DIVIDE vs / operator, COUNTROWS and SUMX; I did not re-read them. The exact COUNT-on-text behaviour is from memory, unverified; my sources file notes one community thread contradicted documented behaviour.
**Edge cases:** Blanks are skipped by COUNT/COUNTA, counted by COUNTROWS. Empty text "" is not blank for COUNTA.
**Likely follow-ups:** 1) *COUNT vs COUNTA?* Numbers vs any non-blank. 2) *Which to use for rows?* COUNTROWS.
**Common mistakes:** Counting a text column to get headcount; ignoring duplicates.

### Q55 ⭐ 🟢 Is DAX case-sensitive, and do spaces matter?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic familiarity with DAX syntax.
**Say this in the interview:** "DAX is not case-sensitive for function and column names, and text comparison with = is case-insensitive by default. Extra spaces and line breaks in formatting do not matter, but a table name with spaces needs single quotes and spaces inside text values do matter."
**Explain simply:**
- sum, SUM and Sum all work; [total sales] and [Total Sales] refer to the same measure.
- Whitespace between tokens is ignored, so you can break a formula across lines.
- Names with spaces or special characters need quotes: 'Sales Data'[Amount].
- Spaces inside text values count: "Active" and "Active " are different.
**Example:** `Region = "north"` matches "North" rows (from memory, unverified).
**DAX / Steps:** (not run here (no DAX engine in this environment))
```dax
North Sales = CALCULATE(sum(Sales[amount]), Sales[region] = "north")
```
**Alternative:** Follow the convention: UPPERCASE functions, Proper Case names, consistent formatting (try daxformatter style).
**Pandas check:** Contrast only (Python is case-sensitive, so this is not a DAX result):
```python
print("North" == "north", "|", "North".lower() == "north".lower())  # Python is case-sensitive; DAX '=' on text is not (by default)
```
Output (run):
```
False | True
```
**Version / licensing note:** Same in Power BI Desktop and Service models (Desktop is where you author; from memory, unverified). Microsoft Learn was unreachable from this session (learn.microsoft.com did not resolve), so I could not re-fetch function pages; DAX syntax is checked against my knowledge of the function pages, not freshly fetched. Earlier research (research/Book04_Part04_sources.md) fetched Microsoft Learn pages CALCULATE, DIVIDE vs / operator, COUNTROWS and SUMX; I did not re-read them.
**Edge cases:** Some data sources (such as SQL with a case-sensitive collation) can behave differently in DirectQuery (from memory, unverified). Case-insensitive grouping can merge "ABC" and "abc" in a column (from memory, unverified).
**Likely follow-ups:** 1) *Do I need quotes always?* Only with spaces/special characters (always quoting is allowed). 2) *Is M case-sensitive?* Yes, Power Query M is (Q22).
**Common mistakes:** Mixing up M (case-sensitive) and DAX; forgetting quotes around spaced table names.

### Q56 ⭐ 🟢 How do you write comments in DAX?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you document your measures.
**Say this in the interview:** "I use two slashes // or two dashes -- for a single-line comment, and /* ... */ for a block. Comments are ignored in the calculation and help the next person understand the measure."
**Explain simply:**
- // and -- comment out the rest of the line.
- /* ... */ can span several lines.
- Use them to explain business rules ("exclude contractors") and thresholds.
**Example:** A documented attrition measure.
**DAX / Steps:** (not run here (no DAX engine in this environment))
```dax
Attrition % =
// Leavers divided by headcount; contractors excluded in the model
VAR Leavers = CALCULATE(COUNTROWS(Employees), Employees[Status] = "Left")  -- exits only
RETURN DIVIDE(Leavers, COUNTROWS(Employees))
/* Block comment:
   reviewed by HR analytics */
```
**Alternative:** Add a description to the measure in the Properties pane (from memory, unverified); shown as a tooltip in the Fields list.
**Version / licensing note:** Same in Power BI Desktop and Service models (Desktop is where you author; from memory, unverified). Microsoft Learn was unreachable from this session (learn.microsoft.com did not resolve), so I could not re-fetch function pages; DAX syntax is checked against my knowledge of the function pages, not freshly fetched. Earlier research (research/Book04_Part04_sources.md) fetched Microsoft Learn pages CALCULATE, DIVIDE vs / operator, COUNTROWS and SUMX; I did not re-read them.
**Edge cases:** In the formula bar, Shift+Enter adds a new line (from memory, unverified). Comments inside quoted text are text, not comments.
**Likely follow-ups:** 1) *Do comments slow down the report?* No. 2) *Comments in M?* Same // and /* */.
**Common mistakes:** Using # or ' as comment markers (Excel/VBA habits); comments that repeat the formula instead of the reason.

### Q57 ⭐ 🟢 Does DAX work in Excel?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know DAX is shared across the Microsoft data tools?
**Say this in the interview:** "Yes. DAX started in Power Pivot, the Excel Data Model add-in. In Excel you can write DAX measures and calculated columns in the Data Model, and use them in PivotTables. It is not used in normal cell formulas."
**Explain simply:**
- Power Pivot is Excel's built-in data model: tables, relationships and DAX, behind PivotTables (we saw the Data Model in Book 1 distinct count).
- Same language, but the Power BI Desktop has more functions and features (from memory, unverified).
- You can also connect Excel to a Power BI semantic model with Analyze in Excel (from memory, unverified).
- DAX is not usable in worksheet cells like =SUM(); there you use Excel formulas.
**Example:** In a PivotTable built on the Data Model, a measure `Total Payroll = SUM(Payroll[Basic])` appears in the field list.
**DAX / Steps:** (not run here (no DAX engine in this environment))
1. Insert > PivotTable > tick Add this data to the Data Model.
2. Power Pivot > Manage (needs the add-in enabled on some versions) > Measures > New Measure.
3. Type the DAX; use it in the PivotTable.
**Alternative:** Build the model in Power BI Desktop, which has fuller DAX support and visuals.
**Version / licensing note:** Availability depends on the Excel edition, and Mac Excel has limited Power Pivot (from memory, unverified). Microsoft Learn was unreachable from this session (learn.microsoft.com did not resolve), so I could not re-fetch function pages; no Excel page was fetched.
**Edge cases:** Some newer DAX functions exist only in Power BI (from memory, unverified). Excel for the web has limited model authoring.
**Likely follow-ups:** 1) *Excel formulas vs DAX?* See Q21. 2) *Can I move the model to Power BI?* Yes, by importing the Excel workbook (from memory, unverified).
**Common mistakes:** Typing DAX in a cell; assuming every DAX function exists in every Excel version.

### Q58 ⭐ 🟢 Can you write DAX in Power BI Service, or on a Mac?
**Asked at:** commonly asked (no company-specific report found); a gap-fill question from standard practice.
**What the interviewer is checking:** Do you know where you can and cannot build models, so you do not promise something your laptop or licence cannot do?
**Say this in the interview:** "Power BI Desktop, where I normally write DAX, is a Windows program, so on a Mac I would use a Windows virtual machine or a cloud PC. In the Power BI Service (the website) you can edit a data model in the browser, including adding measures, but with fewer features than Desktop."
**Explain simply:**
- **DAX** (Data Analysis Expressions) is the formula language for measures. **Desktop** is the free authoring app; **Service** is the browser site where reports are shared.
- Desktop runs on Windows only. There is no native Mac version; Mac users use Windows in a virtual machine (VM) or a cloud PC, or use the browser.
- The Service has web modelling ("Edit data model" on a semantic model, the new name for a dataset), where you can add measures. Some features, such as Power Query transformations and many model settings, are mostly Desktop-side.
- What you can edit in the browser depends on the model's storage mode and your permissions on the workspace.
**Example:** An HR analyst on a MacBook needs to add an "Attrition %" measure to a report already published by a colleague. She opens the semantic model in the browser, adds the measure, and saves. A brand-new model with heavy data cleaning would need a Windows machine.
**DAX / Steps (not run here, from memory):**
1. Service: open your workspace > hover the semantic model > More options (...) > Open data model (or Edit data model) > New measure > type the DAX in the formula bar.
2. Mac: use a Windows VM or cloud PC, then install Power BI Desktop there.
**Alternative:** Ask a Windows colleague to author the model, or use the browser for light edits only.
**Version / licensing note:** from memory, unverified. I tried to fetch the Power BI Desktop system-requirements and "Edit data models in the Power BI service" pages on Microsoft Learn, but learn.microsoft.com was blocked in this session's network settings. Check both pages before quoting exact licence rules (editing a shared model normally needs a paid licence and write access, but verify).
**Edge cases:** Web editing may be unavailable for some models (for example live-connected ones). Menu names change between releases.
**Likely follow-ups:** 1) *Is Desktop free?* Yes to download and build; publishing and sharing need a work account and usually a paid licence (unverified here). 2) *Any Mac option?* Browser plus a Windows VM.
**Common mistakes:** Saying "Power BI does not work on Mac" (the Service works in any browser); claiming web editing equals Desktop.

### Q59 ⭐ 🟢 What naming and organisation habits make measures easier to maintain (measure table, display folders)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you build models other people can read six months later.
**Say this in the interview:** "I keep all measures in one dedicated measure table, group them into display folders such as Headcount and Attrition, give them clear business names, and add a short comment for any tricky logic."
**Explain simply:**
- **Measure table:** an empty table (often called `_Measures`) used only as a home for measures, so they are not scattered across data tables. You can create one by entering a blank table and then hiding its dummy column.
- **Display folders:** a folder label on a measure so the Fields pane groups them (type the name in Model view > Properties > Display folder).
- **Naming:** names that report users understand ("Attrition %", not "m_att2"); use the same pattern everywhere; units in the name if helpful.
- Build small base measures first (Total Leavers, Headcount) and reuse them (see Q30).
- Comments with `//` (Q56) and descriptions explain why, not what.
**Example:** `_Measures` table with folders "Headcount" (Active Headcount, Joiners), "Attrition" (Leavers, Attrition %), "Payroll" (Total Payroll). A new analyst finds anything in seconds.
**DAX / Steps (not run here, from memory):** Home > Enter data > create a table named `_Measures` > Load. Select a measure > Measure tools > Home table (move it) > Model view > Properties > Display folder. Then hide the dummy column.
**Alternative:** Keep each measure on the fact table it belongs to (the table it mainly summarises). It is acceptable for small models.
**Version / licensing note:** from memory, unverified (Microsoft Learn was not reachable in this session). Menu names may differ by Desktop version.
**Edge cases:** Moving a measure to another table does not change its result. A measure table with a hidden dummy column may show a different icon in the Fields pane.
**Likely follow-ups:** 1) *Why a separate table?* To find measures fast. 2) *Do display folders change calculations?* No, they are only labels.
**Common mistakes:** Names like "Measure 1"; the same logic copy-pasted in many measures.

### Q60 ⭐ 🟢 Write a DAX measure for the latest hiring date.
**Asked at:** commonly asked (no company-specific report found); the sources file lists "latest hire date" as a practical gap-fill.
**What the interviewer is checking:** Do you know MAX works on dates, not only numbers?
**Say this in the interview:** "I use MAX on the join-date column. Dates are stored as numbers, so MAX returns the most recent one. As a measure it respects any slicer, such as department."
**Explain simply:**
- A **measure** is a formula calculated on the fly for whatever the report is showing.
- `MAX(column)` returns the largest value; for dates that is the latest.
- With a department slicer on IT, you get the latest IT joiner.
**Example:** The recruiting head wants "last hire date" on a card.
**Sample data** (table `Employees`):

| EmpID | Name | Dept | JoinDate |
|---|---|---|---|
| E01 | Asha | HR | 2015-06-01 |
| E02 | Ravi | IT | 2019-03-15 |
| E03 | Meena | Sales | 2021-08-01 |
| E04 | Karan | IT | 2016-01-10 |
| E05 | Divya | HR | 2023-02-20 |
| E06 | Imran | Sales | 2020-11-01 |

**DAX (not run here):**
```dax
Latest Hire Date = MAX ( Employees[JoinDate] )
```
**Alternative:** `CALCULATE ( MAX ( Employees[JoinDate] ) )` is identical here; `LASTDATE` also works but returns a one-row table, so MAX is simpler.
**Result (reproduced with pandas):** 2023-02-20 (Divya) for all employees.
**Pandas check:**
```python
print(emp.JoinDate.max().date())   # 2023-02-20
```
**Version / licensing note:** MAX is a standard DAX function in all versions (from memory, unverified).
**Edge cases:** If no rows are in filter context, MAX returns blank. Format the measure as a date (Measure tools > Format) or it may show a number.
**Likely follow-ups:** 1) *Earliest date?* MIN. 2) *Latest hire per department?* Put the measure in a table by Dept.
**Common mistakes:** Using MAXX unnecessarily; leaving the format as a whole number.

### Q61 ⭐ 🟢 What data types does DAX support, and what is implicit conversion?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand why text-looking numbers or mixed columns cause odd results.
**Say this in the interview:** "DAX supports whole number, decimal, fixed decimal (currency), text, date/time, true/false, and also binary. Implicit conversion means DAX quietly changes one type to another when an operator needs it, for example text "5" plus 3 becoming 8."
**Explain simply:**
- Types you will meet: Whole Number, Decimal Number, Fixed Decimal Number (currency), Text, Date/Time (also Date, Time), True/False, Binary.
- **Implicit conversion** = automatic type change, such as turning text into number inside `+`.
- It can surprise you: `"10" & 5` joins text, but `"10" + 5` adds numbers. If the text cannot be converted (like "abc") you get an error.
- Safer: set the right column type in Power Query and convert on purpose with `VALUE`, `FORMAT`, `INT`, and so on.
**Example:** An `EmpCode` column loaded as text "007" loses its zeros if you turn it into a whole number. Keep ID columns as text.
**DAX (not run here, from memory):**
```dax
Test 1 = "10" + 5      // 15 (text converted to number)
Test 2 = "10" & 5      // "105" (number converted to text)
```
**Alternative:** Convert on purpose: `VALUE ( "10" ) + 5`.
**Version / licensing note:** from memory, unverified (the Microsoft Learn "Data types in DAX" page was not reachable). Exact type list and conversion table: check that page.
**Edge cases:** Blank behaves as 0 in arithmetic and as empty text in concatenation. Dates are stored as numbers.
**Likely follow-ups:** 1) *Where do you fix types?* In Power Query, before loading. 2) *Why is Fixed Decimal used for money?* It has fixed 4 decimals (from memory).
**Common mistakes:** Relying on implicit conversion; leaving numbers as text so SUM fails.

### Q62 ⭐ 🟡 How does DISTINCTCOUNT treat blanks, and what are the alternatives?
**Asked at:** commonly asked (no company-specific report found). The sources file flags that a community thread contradicted the docs; I could not re-check the Microsoft page (blocked here), so treat the blank rule as from memory.
**What the interviewer is checking:** Whether you know that a blank can count as one extra "value".
**Say this in the interview:** "DISTINCTCOUNT counts each different value once, and from what I remember of the Microsoft documentation it counts a blank as one value too. If I want to leave blanks out I use DISTINCTCOUNTNOBLANK, or filter the blanks out inside CALCULATE."
**Explain simply:**
- `DISTINCTCOUNT(col)` = number of different values in the column.
- If the column has at least one blank cell, that blank is counted as one distinct value (so 3 real IDs plus blanks = 4).
- `DISTINCTCOUNTNOBLANK(col)` ignores blanks.
- Alternative: `CALCULATE(DISTINCTCOUNT(col), NOT ISBLANK(col))`.
**Example:** An attendance log where two rows lost the employee ID.
**Sample data** (table `Attendance`):

| Row | EmpID |
|---|---|
| 1 | E01 |
| 2 | E02 |
| 3 | E02 |
| 4 | (blank) |
| 5 | E03 |
| 6 | (blank) |

**DAX (not run here):**
```dax
Employees Seen (with blank) = DISTINCTCOUNT ( Attendance[EmpID] )
Employees Seen = DISTINCTCOUNTNOBLANK ( Attendance[EmpID] )
Employees Seen v2 = CALCULATE ( DISTINCTCOUNT ( Attendance[EmpID] ), NOT ISBLANK ( Attendance[EmpID] ) )
```
**Alternative:** `COUNTROWS ( VALUES ( Attendance[EmpID] ) )` also includes the blank.
**Result (reproduced with pandas):** DISTINCTCOUNT gives 4; the no-blank versions give 3.
**Pandas check:**
```python
print(att.EmpID.nunique(dropna=False), att.EmpID.nunique())   # 4 3
```
**Version / licensing note:** from memory, unverified. DISTINCTCOUNTNOBLANK exists in current DAX (from memory).
**Edge cases:** A relationship with unmatched rows adds a blank row to the one-side table, which can silently inflate counts. Empty text "" is not the same as BLANK (Q20).
**Likely follow-ups:** 1) *Count unique across tables?* See Q43. 2) *COUNT vs DISTINCTCOUNT?* COUNT counts all non-blank, repeats included.
**Common mistakes:** Reporting 4 employees when there are 3; not checking for blank IDs.

### Q63 ⭐ 🟡 What is a circular dependency error in DAX, and how do you fix it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you read an error message and untangle logic?
**Say this in the interview:** "It means two or more formulas depend on each other, so DAX cannot decide which to calculate first. I fix it by breaking the loop: calculate one of them from a different source, use a measure instead of a column, or use a variable."
**Explain simply:**
- A **dependency** means "formula A needs the result of formula B".
- **Circular** = A needs B and B needs A (or A needs itself).
- Typical cause: calculated columns referring to each other, or a calculated column using a function that looks at the whole table including itself.
- Fixes: remove one link; turn one calculated column into a measure; compute from the source columns; move logic to Power Query.
**Example:** In `Employees`, column `Bonus = [Grade Score] * 0.1` and column `Grade Score = [Bonus] / 0.1` loop. Keep one real source (the rating) and derive the other from it.
**DAX (not run here, illustrative):**
```dax
// Loops: each column needs the other
Bonus       = Employees[GradeScore] * 0.1
GradeScore  = Employees[Bonus] / 0.1

// Fix: both come from a source column
Bonus       = Employees[Rating] * 0.1
```
**Alternative:** Change the second one to a measure; measures can be calculated without feeding columns.
**Version / licensing note:** from memory, unverified (not checked on Microsoft Learn; blocked here).
**Edge cases:** A relationship plus a calculated column can create loops indirectly. The error often appears when you edit an existing column.
**Likely follow-ups:** 1) *Can a measure be circular?* Yes if measures refer to each other in a loop. 2) *How to find it?* Look at the dependency chain in the formula bar.
**Common mistakes:** Making everything a calculated column; fixing by deleting random columns.

### Q64 ⭐ 🟡 What does the error "A single value for column cannot be determined" mean?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand that a measure needs one answer but a column has many values?
**Say this in the interview:** "I referred to a plain column in a measure, but the current filter leaves several rows with different values, so DAX does not know which one to return. I fix it by summarising the column with an aggregator like SUM, MAX or SELECTEDVALUE."
**Explain simply:**
- A measure must return one value per visual cell.
- `Employees[Salary]` alone means "all the salaries here", which may be many numbers.
- The error appears when the column cannot be reduced to one value in the current filter.
- Fix: aggregate (`SUM`, `AVERAGE`, `MAX`) or use `SELECTEDVALUE` (Q69).
**Example:** `Salary Check = Employees[Salary]` fails in a card showing all employees. `Avg Salary = AVERAGE ( Employees[Salary] )` works.
**DAX (not run here, illustrative):**
```dax
Salary Check = Employees[Salary]                         // error when many rows
Dept Label   = SELECTEDVALUE ( Employees[Dept], "Many" ) // fix for text
```
**Alternative:** `MAX ( Employees[Salary] )` if you truly want the highest.
**Version / licensing note:** the exact wording of the message may vary (from memory, unverified).
**Edge cases:** It works by luck when a slicer leaves just one row, which hides the bug until another selection. Calculated columns do not hit this because they have row context (Q8).
**Likely follow-ups:** 1) *Why does it work in a calculated column?* Row context gives one row. 2) *Text column?* SELECTEDVALUE or MAX.
**Common mistakes:** Adding a column reference without an aggregator; testing with one selection only.

### Q65 ⭐ 🟡 Why does a ratio or average show the wrong grand total, and how do you fix it?
**Asked at:** commonly asked (no company-specific report found); the Weekday guide lists "correct totals" among its DAX topics.
**What the interviewer is checking:** Whether you build ratios as "total divided by total", not "average of ratios".
**Say this in the interview:** "A ratio must be calculated again at the total level from the summed numerator and denominator. Averaging the row-level percentages gives a different, wrong total. I write a measure with DIVIDE of two sums and avoid percentage columns."
**Explain simply:**
- Every row and the total in a visual run the measure separately.
- If your measure is `AVERAGE` of a stored percentage column, the total averages the departments equally, whatever their size.
- `DIVIDE(SUM(leavers), SUM(headcount))` gives the true company rate at every level.
**Example:** Attrition (people who left divided by headcount).
**Sample data** (table `DeptStats`):

| Dept | Headcount | Leavers | Rate |
|---|---|---|---|
| HR | 10 | 2 | 20% |
| IT | 40 | 4 | 10% |
| Sales | 50 | 10 | 20% |

**DAX (not run here):**
```dax
Attrition % (wrong) = AVERAGE ( DeptStats[Rate] )
Attrition % = DIVIDE ( SUM ( DeptStats[Leavers] ), SUM ( DeptStats[Headcount] ) )
```
**Alternative:** `AVERAGEX ( VALUES ( DeptStats[Dept] ), [Attrition %] )` deliberately averages departments equally when the business wants that.
**Result (reproduced with pandas):** average of rates = 16.67% (wrong); total leavers / total headcount = 16.00% (correct). Row values stay 20%, 10%, 20% either way.
**Pandas check:**
```python
print(round(d.Rate.mean(),4), d.Leavers.sum()/d.Headcount.sum())   # 0.1667 0.16
```
**Version / licensing note:** DIVIDE behaviour as in Q15 (from Microsoft Learn "DIVIDE vs / operator" page fetched in the sources file; not re-fetched this session).
**Edge cases:** Totals for non-additive measures (distinct counts, ratios) never equal the sum of rows. Hiding totals is an alternative.
**Likely follow-ups:** 1) *Why not a calculated column for the rate?* It cannot be re-aggregated correctly. 2) *Weighted average?* Same idea, SUMX(price*qty) / SUM(qty).
**Common mistakes:** Using AVERAGE of a percentage; summing percentages.

### Q66 ⭐ 🟡 What is the DAX query view in Power BI Desktop?
**Asked at:** commonly asked (no company-specific report found); sources file marks availability as unverified.
**What the interviewer is checking:** Whether you know the modern tools for testing DAX.
**Say this in the interview:** "DAX query view is a screen in Power BI Desktop where I can write and run DAX queries against my model and see the results as a table. I use it to test and debug measures, and it can write measures back into the model."
**Explain simply:**
- A **DAX query** starts with `EVALUATE` and returns a table, unlike a measure which returns one value.
- The view is a separate tab on the left bar (alongside Report, Table, Model).
- It helps check numbers without building a visual, and can test a measure with different filters.
**Example:** Check Attrition % for IT only before trusting the report.
**DAX / Steps (not run here, from memory):**
1. Left navigation > DAX query view icon.
2. Type and press Run:
```dax
EVALUATE
SUMMARIZECOLUMNS ( Employees[Dept], "Headcount", COUNTROWS ( Employees ) )
```
**Alternative:** Build a table visual, or use DAX Studio (a free external tool).
**Version / licensing note:** from memory, unverified. I could not fetch the Microsoft Learn DAX query view page (network blocked), so I cannot confirm preview or GA status or any service-side availability. Check it.
**Edge cases:** Some model connection types may limit it. Results do not change the report unless you update the model.
**Likely follow-ups:** 1) *Query vs measure?* A query returns a table. 2) *Alternative tools?* DAX Studio.
**Common mistakes:** Forgetting `EVALUATE`; expecting a query to create a visual.

### Q67 ⭐ 🟡 What is a visual calculation, and how does it differ from a measure?
**Asked at:** commonly asked (no company-specific report found); the sources file says availability and licensing are unverified.
**What the interviewer is checking:** Whether you know recent features and when to pick them.
**Say this in the interview:** "A visual calculation is a DAX formula attached to one visual and calculated on that visual's data. A measure belongs to the model and works in any visual. Visual calculations are handy for running totals or percent of total within one chart."
**Explain simply:**
- **Measure:** stored in the model, reusable everywhere.
- **Visual calculation:** lives inside the visual, refers to the fields in that visual, and cannot be reused elsewhere.
- Typical functions: running sum, moving average, previous, percent of parent.
- Good for quick visual-only needs; use a measure when many reports need it.
**Example:** In a monthly joiners table, a "Running joiners" column.
**DAX / Steps (not run here, from memory):** Select the visual > Home (or Visual tools) > New calculation > enter e.g. `Running Joiners = RUNNINGSUM ( [Joiners] )`.
**Alternative:** Write a regular measure with CALCULATE and date logic (more work, reusable).
**Version / licensing note:** from memory, unverified. The Microsoft Learn visual calculations page could not be fetched here, so preview or GA status, requirements and DirectQuery limits are unconfirmed. Check the page.
**Edge cases:** It sees only what is in the visual. Changing the visual's fields can break the calculation.
**Likely follow-ups:** 1) *Can other visuals use it?* No. 2) *Performance?* Works on the visual's small result set (from memory).
**Common mistakes:** Treating it as a model-wide measure; not checking availability in your build.

### Q68 ⭐ 🟡 Are there DAX limitations in DirectQuery mode?
**Asked at:** commonly asked (no company-specific report found); the sources file notes Microsoft's CALCULATE page says some uses are unsupported in DirectQuery.
**What the interviewer is checking:** Whether you know that DirectQuery changes what you can do and how fast it is.
**Say this in the interview:** "In DirectQuery the data stays in the source and each visual sends a query, so every DAX measure must be translated to the source language. Some functions and patterns are restricted or slow, and CALCULATE with filters is not supported in calculated columns or row-level security in DirectQuery."
**Explain simply:**
- **DirectQuery** = Power BI does not import data; it asks the database each time.
- The prep notes say Microsoft's CALCULATE page lists "not supported in DirectQuery calculated columns or row-level security" (fetched earlier, per the sources file; not re-fetched here).
- Complex DAX can produce slow queries; models are often kept simpler.
- Other limits (some time-intelligence functions, calculated tables, transformations) exist, from memory, unverified.
**Example:** A payroll database with 50 million rows in DirectQuery: a heavy iterator measure might time out, while Import mode answers quickly.
**DAX / Steps (not run here):** Choose storage mode: Model view > select table > Properties > Advanced > Storage mode (Import, DirectQuery or Dual).
**Alternative:** Use Import mode, or a composite model, or pre-aggregate in the database.
**Version / licensing note:** from memory, unverified apart from the CALCULATE note above. The Microsoft Learn DirectQuery pages could not be fetched here; check them for the current limits.
**Edge cases:** Relational source dialects differ; Microsoft's list changes by release.
**Likely follow-ups:** 1) *When use DirectQuery?* Huge or near-real-time data. 2) *Why slow?* Every interaction fires queries.
**Common mistakes:** Assuming Import-mode DAX behaves identically; piling iterators on big tables.

### Q69 ⭐ 🟡 What does SELECTEDVALUE do, and when do you use it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can read a single slicer choice in DAX.
**Say this in the interview:** "SELECTEDVALUE returns the value of a column when the current filter leaves exactly one value, otherwise it returns blank or the alternative result I give it. I use it for dynamic titles and for what-if or measure-switching slicers."
**Explain simply:**
- Syntax: `SELECTEDVALUE ( column, alternateResult )`.
- One value in filter: returns it. Zero or many: returns the alternate result (blank if you give none).
- Common uses: a title that reads "Attrition for IT", and a slicer that picks which metric a chart shows.
**Example:** Title for a department page.
**Sample data** (table `Employees`):

| Name | Dept |
|---|---|
| Asha | HR |
| Ravi | IT |
| Karan | IT |
| Meena | Sales |

**DAX (not run here):**
```dax
Title = "Attrition for " & SELECTEDVALUE ( Employees[Dept], "all departments" )
```
**Alternative:** `IF ( HASONEVALUE ( Employees[Dept] ), VALUES ( Employees[Dept] ), "all departments" )` (the longer form; from memory it is equivalent in this case).
**Result (reproduced with pandas logic):** Slicer HR gives "HR"; slicer IT gives "IT"; nothing selected (4 rows, 3 depts) gives the alternate result, "all departments".
**Pandas check:**
```python
for dep in ["HR","IT"]:
    v = q[q.Dept==dep].Dept.unique(); print(dep, v[0] if len(v)==1 else "Multiple")
print("Multiple" if q.Dept.nunique()>1 else q.Dept.iloc[0])
# real output: HR / IT / Multiple (the last line stands for the alternate result)
```
**Version / licensing note:** from memory, unverified (Microsoft Learn SELECTEDVALUE page not reachable here).
**Edge cases:** Selecting two departments returns the alternate result. Cross-filtering from a relationship can leave one value even without a slicer.
**Likely follow-ups:** 1) *vs MAX?* MAX gives a number even with many values. 2) *With multi-select?* Use CONCATENATEX.
**Common mistakes:** Forgetting the alternate result; expecting it to list several values.

### Q70 ⭐ 🟡 When are measures calculated, and what does that mean for performance?
**Asked at:** commonly asked (no company-specific report found). Endjin's "measures vs calculated columns" article (search snippet only) supports the stored-at-refresh vs query-time point.
**What the interviewer is checking:** Do you understand that a measure runs when a visual needs it, not when data loads?
**Say this in the interview:** "A measure is calculated at query time, when someone opens or interacts with a visual, and it is not stored. So it does not grow the file, but a slow measure makes visuals slow. Calculated columns are computed at refresh and stored."
**Explain simply:**
- Measures run each time a visual, filter or slicer needs the answer, once for every cell.
- No storage cost, but heavy logic (nested iterators over large tables) affects report speed.
- Calculated columns cost memory but are ready (see Q26).
- Speed-ups: use variables (Q51), simple base measures, fewer visuals per page, avoid iterating big tables when SUM works (Q71).
**Example:** A matrix with 20 departments x 12 months x 3 measures asks for 720 measure calculations on every slicer click.
**DAX / Steps (not run here, from memory):** View tab > Performance analyzer > Start recording > refresh visuals > read DAX query time per visual.
**Alternative:** Pre-compute in Power Query or the database if a calculation is heavy and never changes.
**Version / licensing note:** from memory, unverified; Microsoft Learn was not reachable here.
**Edge cases:** Caching may make a second run faster. Import vs DirectQuery changes where the time goes.
**Likely follow-ups:** 1) *How to find a slow measure?* Performance analyzer. 2) *Measure or column for speed?* Depends: column = bigger file, measure = slower query.
**Common mistakes:** Believing measures are stored; putting everything in calculated columns "for speed".

### Q71 ⭐ 🟡 Is SUMX always slower than SUM?
**Asked at:** Deloitte (Sept 2025 Power BI round: SUM vs SUMX, per research/interview_processes.md) and a Wipro 2023 Bangalore-Rural report mention SUM and SUMX; both are single anecdotes and unverified.
**What the interviewer is checking:** Whether you know it is about need, not speed myths.
**Say this in the interview:** "Not always. Microsoft's guidance is to use SUM when you do not need row-by-row logic. But when the answer needs a calculation per row, like quantity times price, SUMX is the right tool, and for simple cases the engine often handles it efficiently."
**Explain simply:**
- SUM adds one column. SUMX goes row by row, evaluates an expression, and adds the results.
- Use SUM for a plain column; SUMX when you must multiply or filter first (Q5, Q14).
- Slowness comes from heavy expressions or huge tables, not from SUMX itself.
- `SUMX(Sales, Sales[Qty])` and `SUM(Sales[Qty])` give the same number.
**Example:** Two order lines: 2 x 100 and 3 x 50.
**DAX (not run here):**
```dax
Revenue = SUMX ( Sales, Sales[Qty] * Sales[Price] )
```
**Alternative:** Add a calculated column `LineValue` and use SUM (faster at query, but costs memory).
**Result (reproduced with pandas):** 2*100 + 3*50 = 350.
**Pandas check:**
```python
print(df.eval("Qty*Price").sum())   # 350
```
**Version / licensing note:** the "use SUM if you do not need to filter" remark comes from the Microsoft Learn SUMX page fetched earlier (per sources file, not re-fetched). Claims about engine speed are from memory, unverified.
**Edge cases:** Expressions inside SUMX that call measures trigger context transition for every row (Q33), which gets expensive.
**Likely follow-ups:** 1) *When is SUMX needed?* Row calculations. 2) *Faster alternative?* Pre-calculated column.
**Common mistakes:** Saying "never use SUMX"; wrapping a plain column in SUMX.

### Q72 ⭐ 🟡 Write a DAX measure that counts rows where a column is blank.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know ISBLANK and how to filter on blanks?
**Say this in the interview:** "I count rows with COUNTROWS, filtered to rows where the column is blank using ISBLANK. For an HR table, blank exit date means the person is still active."
**Explain simply:**
- **BLANK** means "no value" (Q20), different from 0 or "".
- `ISBLANK(x)` returns TRUE if x is blank.
- Filter inside CALCULATE, then COUNTROWS counts the surviving rows.
**Example:** Employees with no exit date are active.
**Sample data** (table `Employees`):

| EmpID | Name | JoinDate | ExitDate |
|---|---|---|---|
| E01 | Asha | 2015-06-01 | (blank) |
| E02 | Ravi | 2019-03-15 | 2024-05-31 |
| E03 | Meena | 2021-08-01 | (blank) |
| E04 | Karan | 2016-01-10 | (blank) |
| E05 | Divya | 2023-02-20 | (blank) |
| E06 | Imran | 2020-11-01 | 2025-12-31 |

**DAX (not run here):**
```dax
Rows With Blank Exit = CALCULATE ( COUNTROWS ( Employees ), ISBLANK ( Employees[ExitDate] ) )
```
**Alternative:** `COUNTROWS ( FILTER ( Employees, ISBLANK ( Employees[ExitDate] ) ) )`, or `COUNTBLANK ( Employees[ExitDate] )` (from memory, COUNTBLANK also counts empty text).
**Result (reproduced with pandas):** 4 (Asha, Meena, Karan, Divya).
**Pandas check:**
```python
print(emp.ExitDate.isna().sum())   # 4
```
**Version / licensing note:** from memory, unverified; the function pages were not reachable here.
**Edge cases:** Empty text "" is not BLANK, so ISBLANK misses it. Import often turns empty cells into blank, but check.
**Likely follow-ups:** 1) *Count non-blank?* `NOT ISBLANK`, or COUNTA. 2) *Why COUNTROWS?* Counts rows (Q27).
**Common mistakes:** Comparing `= 0` or `= ""` instead of ISBLANK; using COUNT, which counts non-blanks.

### Q73 ⭐ 🟡 Write a DAX measure for sales in the North or South region.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know OR logic in a CALCULATE filter?
**Say this in the interview:** "I use CALCULATE with the IN operator, or two conditions joined by the double pipe. Separate filter arguments in CALCULATE are combined as AND, so for OR on one column I must put both values in one condition."
**Explain simply:**
- `Sales[Region] IN { "North", "South" }` means region is North or South.
- `||` means OR inside one Boolean condition on the same column.
- Two separate arguments (`Region = "North", Region = "South"`) are AND and return nothing (Q36).
**Example:** Regional bonus pool based on two regions.
**Sample data** (table `Sales`):

| Region | Amount |
|---|---|
| North | 12000 |
| South | 8000 |
| East | 15000 |
| West | 9000 |
| North | 5000 |
| East | 7000 |

**DAX (not run here):**
```dax
North South Sales = CALCULATE ( SUM ( Sales[Amount] ), Sales[Region] IN { "North", "South" } )
```
**Alternative:** `CALCULATE ( SUM ( Sales[Amount] ), Sales[Region] = "North" || Sales[Region] = "South" )`.
**Result (reproduced with pandas):** 12000 + 8000 + 5000 = 25,000 (out of 56,000 total).
**Pandas check:**
```python
print(s[s.Region.isin(["North","South"])].Amount.sum())   # 25000
```
**Version / licensing note:** the Boolean filter rules come from the Microsoft Learn CALCULATE page fetched earlier (per sources file); IN usage is from memory, unverified.
**Edge cases:** A Region slicer is replaced by this filter, so with a slicer on East the measure still returns 25,000 (Q37). A slicer on another column, such as Year, still applies.
**Likely follow-ups:** 1) *Different columns with OR?* Use `FILTER` or `||` across columns with FILTER. 2) *Add more regions?* Add to the braces.
**Common mistakes:** Two comma-separated conditions (AND); writing `Region = "North" || "South"`.

### Q74 ⭐ 🟡 Write a DAX measure for the total of orders that are each above Rs 10,000.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you apply the filter per order, not on the grand total?
**Say this in the interview:** "I filter the order table to rows where the order value is above 10,000 and then sum. The condition is checked row by row, so only big orders are added."
**Explain simply:**
- Premise: this assumes one row per order. If the table is order lines, first group by order, using an iterator over distinct orders.
- Boolean filter in CALCULATE: `Orders[OrderValue] > 10000`.
- "Above" means strictly greater; an order of exactly 10,000 is excluded.
**Example:** Large-order revenue for a sales review.
**Sample data** (table `Orders`, one row per order):

| OrderID | OrderValue |
|---|---|
| O1 | 4,500 |
| O2 | 12,000 |
| O3 | 10,000 |
| O4 | 25,000 |
| O5 | 9,800 |

**DAX (not run here):**
```dax
Large Orders Total = CALCULATE ( SUM ( Orders[OrderValue] ), Orders[OrderValue] > 10000 )
```
**Alternative:** `SUMX ( FILTER ( Orders, Orders[OrderValue] > 10000 ), Orders[OrderValue] )` (Q39). For order lines, use `SUMX ( VALUES ( Orders[OrderID] ), IF ( [Order Value] > 10000, [Order Value] ) )` where `[Order Value]` is a measure summing lines (from memory, untested).
**Result (reproduced with pandas):** 12,000 + 25,000 = 37,000 from 2 orders.
**Pandas check:**
```python
print(o[o.OrderValue>10000].OrderValue.sum())   # 37000
```
**Version / licensing note:** Boolean filter behaviour from Microsoft Learn CALCULATE page (fetched earlier per sources file); the rest is from memory, unverified.
**Edge cases:** O3 at exactly 10,000 is excluded. If rows are lines, a single order may be split across rows and miss the threshold. A slicer on OrderValue is overwritten by the Boolean filter.
**Likely follow-ups:** 1) *Count of such orders?* `CALCULATE(COUNTROWS(Orders), ...)`, giving 2. 2) *Make the threshold changeable?* Use a what-if parameter.
**Common mistakes:** Filtering the total instead of each order; using `>=`.

### Q75 ⭐ 🟡 Write a DAX measure for the number of employees with more than 5 years of service.
**Asked at:** commonly asked (no company-specific report found). The Wipro 2023 report mentions DATEDIFF, but this question is a gap-fill.
**What the interviewer is checking:** Can you handle date arithmetic correctly, and know the limits of DATEDIFF?
**Say this in the interview:** "I find the cutoff date, five years before today, and count employees who joined before it. I avoid DATEDIFF with YEAR, because it counts calendar-year boundaries, so someone who joined in December would show a full year in January."
**Explain simply:**
- Cutoff = today minus 60 months, via `EDATE ( TODAY(), -60 )`.
- Joined before the cutoff means more than 5 years of service.
- `DATEDIFF(start, end, YEAR)` counts year-number changes (from memory), so 31 Dec 2020 to 1 Jan 2021 gives 1 year.
- Decide whether to count only active employees (Q34).
**Example:** Long-service award list, as of 1 Nov 2026 (the pandas check uses this fixed date; TODAY() changes daily).
**Sample data** (table `Employees`, the same six rows as Q72):

| Name | JoinDate | ExitDate |
|---|---|---|
| Asha | 2015-06-01 | (blank) |
| Ravi | 2019-03-15 | 2024-05-31 |
| Meena | 2021-08-01 | (blank) |
| Karan | 2016-01-10 | (blank) |
| Divya | 2023-02-20 | (blank) |
| Imran | 2020-11-01 | 2025-12-31 |

**DAX (not run here):**
```dax
Employees 5+ Years =
VAR Cutoff = EDATE ( TODAY (), -60 )
RETURN
    CALCULATE ( COUNTROWS ( Employees ), Employees[JoinDate] < Cutoff )
```
**Alternative:** An active-only version: add `ISBLANK ( Employees[ExitDate] )` as another filter.
**Result (reproduced with pandas, as of 2026-11-01, cutoff 2021-11-01):** 5 (Asha, Ravi, Meena, Karan, Imran). Divya is under 5 years. With active-only, Ravi and Imran drop out: 3.
**Pandas check:**
```python
cut = pd.Timestamp("2026-11-01") - pd.DateOffset(months=60)
print((emp.JoinDate < cut).sum())   # 5
```
**Version / licensing note:** EDATE and TODAY are standard DAX (from memory, unverified; Microsoft Learn pages not reachable here).
**Edge cases:** Leavers are counted unless filtered; TODAY() uses the PC or service time zone; a join date exactly on the cutoff is not "more than" 5 years.
**Likely follow-ups:** 1) *Why not DATEDIFF?* Boundary counting. 2) *Fixed as-of date?* Replace TODAY() with a date from a parameter.
**Common mistakes:** `DATEDIFF(..., YEAR) > 5`, which is off by up to a year; forgetting leavers.
