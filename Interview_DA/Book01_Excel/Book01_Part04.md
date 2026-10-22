# Book 1 — Excel | Part 4: Pivot tables, pivot charts, slicers 🟢🟡

**Target:** 70 questions | **Actual:** 74 questions
**Scope:** Pivot tables, pivot charts, slicers and timelines: building, fields, grouping, calculated fields, refresh, GETPIVOTDATA, pivot-based reports (HR, attendance, sales).

### Q1 ⭐⭐⭐ 🟢 What is a pivot table, and why do analysts use it?
**Asked at:** commonly asked (no company-specific report found); "pivot table" is named in several MIS job descriptions in our sample (Material Depot, Ninjacart, Tata Advanced Systems, Bridgestone, Vee).
**What the interviewer is checking:** Can you explain it in one breath and name a business use?
**Say this in the interview:** "A pivot table is Excel's tool for summarising a long list of rows into a small report, such as headcount or average salary by department, using drag and drop instead of formulas. I use it to answer a business question in a minute and to refresh the answer when the data changes."
**Explain simply:**
- Raw data = a long list (one row per employee or sale). A pivot table groups those rows and calculates totals, counts or averages for each group.
- You do not write formulas; you drag fields (column headings) into boxes and Excel does the grouping.
- The source data is never changed, so it is safe to experiment.
- It can be rearranged in seconds: swap rows and columns, filter, add a second measure.
**Example:** 8 employees across 4 departments. The pivot turns the 8-row list into 4 rows: Finance 55,000, HR 40,500, IT 68,000, Sales 49,000 (average salary).
**Sample sheet:** Source data A1:D9 (EmpID, Dept, Location, Salary), see Q5 for the full grid. Pivot result checked with pandas (`pivot_table(index='Dept', values='Salary', aggfunc='mean')`):

| Dept | Average of Salary |
|---|---|
| Finance | 55000 |
| HR | 40500 |
| IT | 68000 |
| Sales | 49000 |

**Formula / Steps:** Insert > PivotTable, then drag Dept to Rows and Salary to Values (not run here; steps from Microsoft Support, "Create a PivotTable to analyze worksheet data").
**Alternative:** SUMIFS/AVERAGEIFS formulas give the same numbers but need one formula per cell (see Q16).
**Result:** pandas output above (run here); the Excel pivot itself was not run.
**Version note:** Available in Excel 2016, 2019, 2021, 2024 and Microsoft 365 (Microsoft Support, "Create a PivotTable to analyze worksheet data"). Google Sheets has pivot tables too (from memory, unverified).
**Edge cases:** Blank rows, merged cells or mixed text and numbers in a column spoil the result (see Q4).
**Likely follow-ups:** 1) *Does it change my data?* No. 2) *Does it update itself?* No, you must refresh (Q7).
**Common mistakes:** Calling it a "formula"; forgetting to refresh; building it on data with blank headers.

### Q2 ⭐⭐⭐ 🟢 How do you create a pivot table in Excel from a raw data sheet?
**Asked at:** commonly asked; one candidate report (Naukri Code360, KollegeApply Business Analyst, Sep 2025, seen only as a search snippet, unverified) mentions an online round to create a pivot table and explain the analysis.
**What the interviewer is checking:** Do you know the click path and the order of steps?
**Say this in the interview:** "I click inside the data, go to Insert > PivotTable, confirm the range, choose a new worksheet, and click OK. Then I tick or drag fields into Rows, Columns and Values."
**Explain simply:**
- Make sure the data has one header row and no blank rows first (Q4).
- The empty pivot and the PivotTable Fields pane appear; nothing shows until you add fields.
- Text fields go to Rows by default and numeric fields go to Values (Microsoft Support).
**Example:** HR sheet with Dept and Salary: put Dept in Rows, Salary in Values, and you get salary per department.
**Sample sheet:** none needed; see Q5 for a sheet.
**Formula / Steps (not run here; steps from Microsoft Support, "Create a PivotTable to analyze worksheet data"):**
1. Select any cell in the data (or the whole range).
2. Insert tab > PivotTable.
3. Confirm the table or range; choose New Worksheet or Existing Worksheet.
4. Click OK.
5. In the PivotTable Fields pane, drag fields into the areas.
**Alternative:** Insert > Recommended PivotTable and pick a layout Excel suggests (Microsoft 365 only per that page, see Q26).
**Result:** An empty pivot on a new sheet that fills as you add fields. Not run here.
**Version note:** Excel 2016 to 365 (Microsoft Support).
**Edge cases:** If you select just one cell, Excel guesses the range; a blank row inside the data makes it stop early.
**Likely follow-ups:** 1) *New sheet or existing?* New sheet keeps things tidy. 2) *Can you use an Excel Table as the source?* Yes, and new rows are then picked up on refresh (Microsoft Support).
**Common mistakes:** Selecting data with a blank column; having duplicate or blank headings; forgetting to refresh later.

### Q3 ⭐⭐⭐ 🟢 What are the four areas of the PivotTable Fields pane (Filters, Columns, Rows, Values), and what does each do?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand which box controls what?
**Say this in the interview:** "Rows are the labels down the side, Columns are the labels across the top, Values are the numbers being calculated, and Filters sit above the table and narrow the whole report."
**Explain simply:**
- **Rows:** each unique item becomes one row, e.g. each Department.
- **Columns:** each unique item becomes a column, e.g. each Month. Adds a second dimension (cross-tab).
- **Values:** the number crunching: sum, count, average of a field.
- **Filters:** fields placed here show a dropdown above the table; picking one item limits the entire report (Microsoft Support, "Design the layout and format of a PivotTable").
- Microsoft's "Create a PivotTable" page says non-numeric fields go to Rows and numeric fields go to Values by default.
**Example:** Dept in Rows, Location in Columns, Count of EmpID in Values, Filters empty: headcount by department and location. Put Location in Filters instead and you see one location at a time.
**Sample sheet:** Using the Q5 data, pandas check of Dept x Location headcount (not an Excel run): HR has Hyderabad 1 and Chennai 1; IT has Bengaluru 1, Hyderabad 1 and Pune 1.
**Formula / Steps:** Drag a field from the field list into the box, or right-click the field and choose Add to Row Labels / Column Labels / Report Filter / Values (not run here; Microsoft Support).
**Alternative:** Tick the checkbox next to a field and let Excel place it, then move it.
**Result:** Not applicable (concept question).
**Version note:** Same in 2016 to 365; Microsoft's page names them "Report Filter / Column Labels / Row Labels / Values", the pane in current Excel shows "Filters / Columns / Rows / Values".
**Edge cases:** A field can be in only one of Filters, Rows or Columns at a time (Microsoft Support); the same field can be in Values more than once.
**Likely follow-ups:** 1) *Rows vs Columns?* Same idea, different direction. 2) *Can Values hold text?* Only as a count.
**Common mistakes:** Putting a numeric ID in Values and getting a sum of IDs; dragging too many fields into Rows.

### Q4 ⭐⭐⭐ 🟢 What should your source data look like before you build a pivot table?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that pivot problems usually come from messy data?
**Say this in the interview:** "One header row, one record per row, no blank rows or columns, no merged cells, and one data type per column. I like to convert it to an Excel Table so new rows come in automatically."
**Explain simply:**
- Microsoft Support ("Create a PivotTable to analyze worksheet data") lists: columns with a single header row, no merged cells or double headers, no blank rows or columns, consistent data types per column, and formatting as an Excel table so refreshes pick up new rows.
- "One record per row" means each employee or sale has its own row, not one column per month.
- Numbers stored as text will be counted instead of summed (Q8).
**Example:** A payroll sheet with a title in row 1 and a blank row 2 breaks the header detection. Delete them so row 1 is the headings.
**Sample sheet:** Good layout:

| | A | B | C | D |
|---|---|---|---|---|
| 1 | EmpID | Dept | Location | Salary |
| 2 | 101 | HR | Hyderabad | 42000 |
| 3 | 102 | Finance | Pune | 55000 |

**Formula / Steps:** Select data > Ctrl+T to make a Table (my usual habit, from memory; the Table recommendation itself is from Microsoft Support). Not run here.
**Alternative:** Power Query to clean the data first (see Q45).
**Result:** Not applicable.
**Version note:** Tables and pivots in 2016 to 365 (Microsoft Support).
**Edge cases:** Dates typed as text will not group (Q38); trailing spaces make "HR" and "HR " two separate items.
**Likely follow-ups:** 1) *Why a Table?* Auto-expands. 2) *Wide vs long data?* Long is better for pivots.
**Common mistakes:** Subtotal rows inside the data; merged headers; blank headings.

### Q5 ⭐⭐⭐ 🟢 Given columns Employee ID, Department, Location and Salary, how do you build a pivot table that shows headcount by department?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know to use Count and a field with no blanks?
**Say this in the interview:** "I insert a pivot, put Department in Rows and Employee ID in Values. Because the ID is a number, Excel defaults to Sum, so I change it to Count. That gives headcount per department."
**Explain simply:**
- Headcount = number of employees, so we need Count, not Sum.
- Count a column that is never blank (Employee ID).
- Salary is not needed here.
**Example:** 8 employees; IT has 3.
**Sample sheet:** A1:D9

| | A | B | C | D |
|---|---|---|---|---|
| 1 | EmpID | Dept | Location | Salary |
| 2 | 101 | HR | Hyderabad | 42000 |
| 3 | 102 | Finance | Pune | 55000 |
| 4 | 103 | IT | Bengaluru | 68000 |
| 5 | 104 | HR | Chennai | 39000 |
| 6 | 105 | Sales | Mumbai | 47000 |
| 7 | 106 | IT | Hyderabad | 72000 |
| 8 | 107 | IT | Pune | 64000 |
| 9 | 108 | Sales | Mumbai | 51000 |

**Formula / Steps (not run here; Microsoft Support):**
1. Click in the data > Insert > PivotTable > OK.
2. Drag Dept to Rows.
3. Drag EmpID to Values.
4. Click the field in Values > Value Field Settings > Summarize Values By > Count > OK.
**Alternative:** Drag Dept to Rows and also to Values (text fields default to Count).
**Result:** Reproduced with pandas (`pivot_table(index='Dept', values='EmpID', aggfunc='count', margins=True)`), run here:

| Dept | Count of EmpID |
|---|---|
| Finance | 1 |
| HR | 2 |
| IT | 3 |
| Sales | 2 |
| Grand Total | 8 |

**Version note:** Excel 2016 to 365.
**Edge cases:** Duplicate Employee IDs inflate the count; for distinct count see Q40.
**Likely follow-ups:** 1) *Headcount by location too?* Add Location to Columns. 2) *Why not Sum?* Sum of IDs is 836, meaningless.
**Common mistakes:** Leaving it on "Sum of EmpID"; counting a column that has blanks.

### Q6 ⭐⭐⭐ 🟢 Given a sales sheet with Region, Product and Amount, how do you show total sales by region and product?
**Asked at:** commonly asked (no company-specific report found); a "sales by category and region" scenario appears in a prep blog listing (search snippet only).
**What the interviewer is checking:** Can you set up a two-way summary?
**Say this in the interview:** "Region in Rows, Product in Columns, Amount in Values as Sum. I get regions down the side, products across the top and totals at the edges."
**Explain simply:**
- Rows and Columns together make a cross-table.
- Sum is the default for numeric fields.
- Grand Totals appear automatically.
**Example:** North sold laptops worth 750 and phones worth 300.
**Sample sheet:** A1:C9

| | A | B | C |
|---|---|---|---|
| 1 | Region | Product | Amount |
| 2 | North | Laptop | 500 |
| 3 | North | Phone | 300 |
| 4 | South | Laptop | 400 |
| 5 | South | Phone | 350 |
| 6 | East | Laptop | 450 |
| 7 | North | Laptop | 250 |
| 8 | South | Phone | 150 |
| 9 | East | Phone | 200 |

**Formula / Steps (not run here; Microsoft Support):** Insert > PivotTable > OK; Region to Rows, Product to Columns, Amount to Values.
**Alternative:** One SUMIFS per cell: `=SUMIFS($C$2:$C$9,$A$2:$A$9,$E2,$B$2:$B$9,F$1)`.
**Result:** pandas reproduction, run here:

| Region | Laptop | Phone | Grand Total |
|---|---|---|---|
| East | 450 | 200 | 650 |
| North | 750 | 300 | 1050 |
| South | 400 | 500 | 900 |
| Grand Total | 1600 | 1000 | 2600 |

**Version note:** Excel 2016 to 365.
**Edge cases:** A combination with no sales shows blank (Q25 for zeros). Text amounts get counted (Q8).
**Likely follow-ups:** 1) *Percent of total?* Q18. 2) *Add months?* Group dates (Q13).
**Common mistakes:** Putting both fields in Rows (gives a long list, not a grid); wrong summary function.

### Q7 ⭐⭐⭐ 🟢 How do you refresh a pivot table after the source data changes?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know a pivot does not update itself?
**Say this in the interview:** "I right-click inside the pivot and choose Refresh, or use PivotTable Analyze > Refresh All for every pivot in the workbook. If the new rows are outside the original range, I also check the data source (Q12)."
**Explain simply:**
- A pivot stores a snapshot copy of your data (the "cache"); editing the source does not change it until refreshed.
- Refresh re-reads the source.
- Refresh All refreshes every pivot in the file.
**Example:** A new joiner is added to the HR sheet; headcount stays 8 until you refresh, then becomes 9.
**Sample sheet:** Not needed.
**Formula / Steps (not run here; Microsoft Support, "Create a PivotTable to analyze worksheet data"):** Right-click inside the pivot > Refresh. For several: click a cell > PivotTable Analyze > arrow under Refresh > Refresh All. Keyboard: Alt+F5 refreshes (from memory, unverified).
**Alternative:** Data > Refresh All; or VBA / "refresh on open" in PivotTable Options (from memory, unverified).
**Result:** Not applicable.
**Version note:** Same in 2016 to 365.
**Edge cases:** If source rows were added below an old fixed range, refresh alone will not include them; an Excel Table as source avoids this (Microsoft Support).
**Likely follow-ups:** 1) *Does it auto-refresh?* Not by default. 2) *Why did my formatting reset?* Q44.
**Common mistakes:** Editing numbers inside the pivot; not refreshing before sending a report.

### Q8 ⭐⭐⭐ 🟢 Why does a pivot table show the count of a field instead of the sum, and how do you change it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the classic cause: numbers stored as text?
**Say this in the interview:** "Excel defaults to Count when it thinks the column is text, usually because of text-numbers, or blank cells in the column. I fix the data to real numbers, or change Summarize Values By to Sum."
**Explain simply:**
- Microsoft Support: "By default, Values fields show a SUM. If Excel reads the data as text, it shows a COUNT."
- Text-numbers often show a green triangle or left-aligned values.
- A single text cell or blank in the column can flip the default to Count.
**Example:** Salaries imported from a payroll system as text "42000". Pivot shows Count 2 for HR; after converting, Sum is 81,000.
**Sample sheet:** A1:B4

| | A | B |
|---|---|---|
| 1 | Dept | Salary (text) |
| 2 | HR | '42000 |
| 3 | HR | '39000 |
| 4 | IT | '68000 |

**Formula / Steps (not run here; Microsoft Support):** Click the field in Values > Value Field Settings > Summarize Values By > Sum. Better: fix the source first (Data > Text to Columns > Finish, or multiply by 1) and refresh.
**Alternative:** Helper column `=VALUE(B2)` then pivot on it.
**Result:** pandas reproduction, run here: count of text salaries by Dept = HR 2, IT 1; after `pd.to_numeric`, sum = HR 81000, IT 68000.
**Version note:** Same in all versions.
**Edge cases:** Even after converting, you must refresh. Setting Sum on a text field gives 0.
**Likely follow-ups:** 1) *How do you spot text-numbers?* Left-aligned, green triangle. 2) *Count vs Count Numbers?* Count Numbers counts only numeric cells.
**Common mistakes:** Forcing Sum on text and getting zeros; not fixing the root cause in the data.

### Q9 ⭐⭐⭐ 🟢 What is a slicer, and how do you add one to a pivot table?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know slicers as button filters for dashboards?
**Say this in the interview:** "A slicer is a set of clickable buttons that filters a pivot table, and it shows which filters are active. I add it with Insert > Slicer while a cell in the pivot is selected."
**Explain simply:**
- Same job as a filter dropdown, but visible and friendly for non-technical viewers.
- Click a button to filter; Ctrl+click for several (Microsoft Support, "Use slicers to filter data").
- One slicer per field you pick.
**Example:** A Region slicer with North, South, East buttons on a sales pivot; click South and the table shows only South.
**Sample sheet:** Use the Q6 data; clicking South would leave Laptop 400, Phone 500, total 900 (pandas check of the Q6 output; the slicer itself was not run).
**Formula / Steps (not run here; Microsoft Support, "Use slicers to filter data"):**
1. Click anywhere in the pivot.
2. Insert tab > Slicer.
3. Tick the fields > OK.
4. Click buttons to filter; the Clear Filter icon removes it.
**Alternative:** Report Filter (Q14) or the Row Labels dropdown.
**Result:** Not run here.
**Version note:** The Microsoft page applies to Microsoft 365, 2024 and 2021; slicers for pivots exist in Excel 2010 onward (from memory, unverified). In Excel for the web only local PivotTable slicer creation is available (Microsoft Support). Formatting is on the Slicer tab in newer versions and the Design tab in 2016 and older (Microsoft Support).
**Edge cases:** A slicer can only connect to pivots with the same data source (Microsoft Support).
**Likely follow-ups:** 1) *Link to several pivots?* Q32. 2) *Slicer vs filter?* Q14.
**Common mistakes:** Inserting a slicer without selecting a pivot cell; leaving a slicer on a filter and forgetting.

### Q10 ⭐⭐⭐ 🟢 What is a pivot chart, and how do you create one?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know it is a chart linked to a pivot?
**Say this in the interview:** "A pivot chart is a chart tied to a pivot table; when the pivot changes or is filtered, the chart changes with it. I click in the pivot and choose Insert > PivotChart."
**Explain simply:**
- It visualises the pivot summary, e.g. a column chart of headcount by department.
- Filtering the pivot or using slicers also filters the chart (Microsoft Support, "Create a PivotChart").
- It has its own field buttons you can filter from.
**Example:** Chart of total sales by region for 1050 / 900 / 650.
**Sample sheet:** Pivot data from Q6 (pandas totals North 1050, South 900, East 650).
**Formula / Steps (not run here; Microsoft Support, "Create a PivotChart"):** Select a cell in the pivot > Insert > PivotChart > pick a chart type > OK. On Mac, insert a column, line, pie or radar chart from the pivot; treemap, statistical and combo types do not work with pivots (Microsoft Support).
**Alternative:** Create the pivot and chart together: select the data > Insert > PivotChart.
**Result:** Not run here.
**Version note:** Applies to Excel 2016 to 365 (Microsoft Support).
**Edge cases:** Changing the pivot layout changes the chart; some chart types are unavailable.
**Likely follow-ups:** 1) *Pivot chart vs normal chart?* Q41. 2) *Add a slicer?* Q37.
**Common mistakes:** Formatting the chart and losing it on refresh; picking a chart that suits neither the data nor the audience.

### Q11 ⭐⭐⭐ 🟢 How do you filter a pivot table to show only the top 5 items?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know Value Filters > Top 10?
**Say this in the interview:** "I open the Row Labels dropdown, choose Value Filters > Top 10, set Top, 5, Items, and pick the value field. The name says 10 but you can set any number."
**Explain simply:**
- Top 10 is just the name of the dialog; change 10 to 5.
- You can also choose Percent or Sum instead of Items (Microsoft Support, "Filter data in a PivotTable").
- It ranks by the value field you pick, not alphabetically.
**Example:** 7 products; show only the 5 best sellers.
**Sample sheet:** Product totals: Laptop 1600, Phone 1000, Tablet 870, Monitor 640, Mouse 310, Cable 120, Dock 90.
**Formula / Steps (not run here; Microsoft Support, "Filter data in a PivotTable"):** Click the Filter arrow > Value Filters > Top 10 > Top, 5, Items, "Sum of Amount" > OK.
**Alternative:** Sort descending and select the top 5 rows by hand, or filter the rows with a helper RANK column in the source.
**Result:** pandas (`nlargest(5)`), run here: Laptop 1600, Phone 1000, Tablet 870, Monitor 640, Mouse 310; those five add up to 4420 of 4630 in total. Excel's pivot was not run.
**Version note:** Applies to 2016 to 365 (Microsoft Support).
**Edge cases:** Ties at the cut-off can show more than 5 items (from memory, unverified). Grand Total still includes only the shown items by default unless set otherwise (from memory, unverified).
**Likely follow-ups:** 1) *Bottom 5?* Choose Bottom. 2) *Top 10 percent?* Switch Items to Percent.
**Common mistakes:** Applying Label Filters rather than Value Filters; not realising the filter is tied to a value field.

### Q12 ⭐⭐⭐ 🟢 Your pivot table does not show the new rows you added to the source. What do you check?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you have a troubleshooting order?
**Say this in the interview:** "First, I refresh. If rows are still missing I check the source range through Change Data Source, then look for filters, blank rows, or text-formatted values in the source. Long term, I make the source an Excel Table."
**Explain simply:**
- Step 1: Refresh (Q7); the pivot is a snapshot.
- Step 2: Check the range: new rows may be below a fixed range (PivotTable Analyze > Change Data Source).
- Step 3: A blank row can cut off the range.
- Step 4: Check the pivot itself for filters, slicers or items hidden by an old filter.
- An Excel Table source picks up new rows on refresh (Microsoft Support).
**Example:** One new sale of West, Laptop, 600 is added in row 10. Old total 2600; after refresh over the correct range 3200 (pandas check).
**Sample sheet:** Q6 data plus row 10: West | Laptop | 600.
**Formula / Steps (not run here; Change Data Source steps from memory, unverified):** PivotTable Analyze > Change Data Source > select the full range > OK > Refresh.
**Alternative:** Ctrl+T the source first so the range grows itself.
**Result:** pandas: total 2600 before, 3200 after (run here).
**Version note:** Same in all recent versions.
**Edge cases:** New text value "West" may stay hidden if a filter on Region excludes new items; new rows with dates as text will not group.
**Likely follow-ups:** 1) *Refresh did nothing?* Check the range. 2) *Prevent it?* Table source.
**Common mistakes:** Adding data and not refreshing; typing outside the range; ignoring active filters.

### Q13 ⭐⭐⭐ 🟡 How do you group dates in a pivot table into months, quarters or years?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the Group dialog and its limits?
**Say this in the interview:** "I put the date field in Rows, right-click a date, choose Group, and select Months, Quarters and Years. In recent versions Excel often groups dates automatically when you add them."
**Explain simply:**
- Daily dates produce a huge row list; grouping rolls them up.
- Microsoft Support ("Group or ungroup data in a PivotTable") describes right-click a date > Group, set Starting at / Ending at, and choose the period under By; automatic grouping also happens when time fields are added.
- Pick Years with Months or you will mix January of different years together.
**Example:** Sales dated Jan to Jul 2026.
**Sample sheet:** A1:B7 (Date, Amount): 10-Jan 100, 05-Feb 200, 20-Feb 150, 02-Apr 300, 15-May 120, 01-Jul 80.
**Formula / Steps (not run here; Microsoft Support):** Right-click any date in the pivot > Group > select Months, Quarters, Years > OK.
**Alternative:** Helper columns in the source: `=TEXT(A2,"mmm")` or `=ROUNDUP(MONTH(A2)/3,0)` and pivot on them (not run through the pivot; formula from memory).
**Result:** pandas, run here: Jan 100, Feb 350, Apr 300, May 120, Jul 80; by quarter: Qtr1 450, Qtr2 420, Qtr3 80.
**Version note:** Applies to Excel 2016 to 365 (Microsoft Support). Automatic date grouping began in Excel 2016 (from memory, unverified).
**Edge cases:** Blank cells or text dates in the date column block grouping (Q38).
**Likely follow-ups:** 1) *Group by weeks?* Choose Days and set 7 days. 2) *Fiscal year?* Use a helper column.
**Common mistakes:** Grouping only by Months across years; blank dates.

### Q14 ⭐⭐⭐ 🟡 What is the difference between a slicer and a report filter in a pivot table?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know when each is appropriate?
**Say this in the interview:** "Both filter the pivot. A report filter is a dropdown above the pivot and takes little space; a slicer is a button panel that shows the current selection and can be connected to several pivots. I use slicers for dashboards, report filters for quick analysis."
**Explain simply:**
- Microsoft Support says slicers "also indicate the current filtering state" (its page does not compare directly with report filters).
- Slicers are visual, work well for sharing, can be connected to other pivots with the same source (Report Connections).
- A report filter is a field in the Filters area: smaller, can be multi-select but its state is hidden in a dropdown; in Excel's pivot you can also "Show Report Filter Pages" (from memory, unverified).
**Example:** Department as a slicer: click IT and see its headcount. As a report filter: open dropdown, choose IT.
**Sample sheet:** Not needed.
**Formula / Steps (not run here; Microsoft Support):** Slicer: Insert > Slicer. Report filter: drag field to Filters area, then use the dropdown.
**Alternative:** Timeline for dates (Q33).
**Result:** Not applicable.
**Version note:** Both available in 2016 to 365; slicers connect across pivots with the same data source (Microsoft Support).
**Edge cases:** Slicers need more screen space; a report filter and a slicer on the same field both apply.
**Likely follow-ups:** 1) *Link to multiple pivots?* Report Connections (Q32). 2) *Which is better for viewers?* Slicers.
**Common mistakes:** Forgetting an active filter hides rows; hiding the slicer and leaving it filtered.

### Q15 ⭐⭐⭐ 🟡 How would you build a month-wise attrition (leavers) summary by department from an HR data sheet using a pivot table?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you turn a joiner/leaver sheet into a monthly report and filter out people who have not left?
**Say this in the interview:** "I use the Exit Date column. I filter out blanks, group exit dates by month and year, put Department in Rows, the months in Columns and a Count of Employee ID in Values. That gives leavers by department by month."
**Explain simply:**
- Leavers = rows with an exit date; staff still working have a blank exit date and must be excluded.
- Group the exit date to months (Q13).
- Count of Employee ID = number of leavers.
- To get attrition **rate** you also need headcount; the pivot gives the numerator only.
**Example:** 10 employees, 8 have left between January and March.
**Sample sheet:** A1:C11 (EmpID, Dept, ExitDate): 1 IT 15-Jan; 2 IT 10-Feb; 3 HR 20-Jan; 4 Sales blank; 5 IT 25-Feb; 6 Sales 05-Feb; 7 HR blank; 8 Sales 12-Mar; 9 IT 30-Mar; 10 Sales 08-Jan.
**Formula / Steps (not run here; Microsoft Support):**
1. Insert > PivotTable on the data.
2. Dept to Rows; ExitDate to Columns; EmpID to Values (Count).
3. Right-click an exit date > Group > Months (and Years).
4. In the ExitDate filter, untick (blank).
**Alternative:** COUNTIFS per cell: `=COUNTIFS($B:$B,"IT",$C:$C,">="&DATE(2026,1,1),$C:$C,"<"&DATE(2026,2,1))`.
**Result:** pandas reproduction, run here:

| Dept | Jan | Feb | Mar | Grand Total |
|---|---|---|---|---|
| HR | 1 | 0 | 0 | 1 |
| IT | 1 | 2 | 1 | 4 |
| Sales | 1 | 1 | 1 | 3 |
| Grand Total | 3 | 3 | 2 | 8 |

Without removing blanks the data has 10 rows, so only 8 are leavers.
**Version note:** Excel 2016 to 365.
**Edge cases:** Blank exit dates must be excluded; text dates won't group; rate = leavers / average headcount (needs separate data).
**Likely follow-ups:** 1) *Rate?* Divide by average headcount, calculated outside the pivot. 2) *Voluntary vs involuntary?* Add the reason to Columns or Filters.
**Common mistakes:** Counting everyone including active staff; no years in the grouping so Januaries merge.

### Q16 ⭐⭐⭐ 🟡 What is the difference between a pivot table and formulas such as SUMIFS or COUNTIFS? When would you use each?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you choose the tool on purpose, not by habit?
**Say this in the interview:** "A pivot is fast and flexible for exploring and summarising; I refresh it by hand. SUMIFS/COUNTIFS are live formulas, recalculate automatically and sit exactly where I want in a fixed report layout. I explore with a pivot and build final dashboards with formulas."
**Explain simply:**
- Pivot: drag and drop, quick, many summaries from one setup; needs refresh; layout is controlled by Excel.
- SUMIFS/COUNTIFS: one formula per cell; update immediately; full control over layout and extra logic.
- Large reports: formulas can slow a workbook; a pivot is usually faster.
**Example:** "How much did North sell in laptops?" A pivot gives it as part of a grid. A formula gives that one number.
**Sample sheet:** Q6 data in A1:C9; E1 = North, F1 = Laptop.
**Formula / Steps:** G1 `=SUMIFS(C2:C9,A2:A9,E1,B2:B9,F1)`; G2 `=COUNTIFS(A2:A9,E1)`.
**Alternative:** The pivot with Region in Rows and Product in Columns (Q6); or GETPIVOTDATA to read a pivot value.
**Result:** Run in LibreOffice: G1 = 750, G2 = 3. The pandas check of the pivot gives the same 750 for North/Laptop.
**Version note:** SUMIFS and COUNTIFS exist since Excel 2007; pivots are in all versions (from memory, unverified).
**Edge cases:** Formulas keep working when the data grows if ranges cover it; pivots need a refresh; text-numbers fail both.
**Likely follow-ups:** 1) *Which for a monthly dashboard?* Formulas for fixed layouts, pivot plus slicers for interactive ones. 2) *Which is faster on 500,000 rows?* Pivot (from memory, unverified).
**Common mistakes:** Hard-coding totals; using whole-column formulas on huge data; forgetting to refresh pivots.

### Q17 ⭐⭐ 🟢 How do you change a Values field from Sum to Average, Count, Max or Min?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know Value Field Settings?
**Say this in the interview:** "Right-click a number in the Values area, choose Summarize Values By, and pick Sum, Count, Average, Max or Min. Or open Value Field Settings for the full list."
**Explain simply:**
- Microsoft Support ("Change the summary function or custom calculation for a field in a PivotTable report") lists Sum, Count, Average, Max, Min, Product, Count Numbers, StDev, StDevp, Var, Varp and Distinct Count (needs the Data Model).
- It changes the calculation, not the source data.
- Rename the heading afterwards if wanted (Q24).
**Example:** Sales by region: total, average, number of sales, biggest and smallest.
**Sample sheet:** Q6 data.
**Formula / Steps (not run here; Microsoft Support):** Right-click a value > Summarize Values By > choose function. Or PivotTable Analyze > Field Settings > Summarize Values By tab.
**Alternative:** Add the same field to Values several times with different summaries.
**Result:** pandas reproduction, run here:

| Region | Sum | Average | Count | Max | Min |
|---|---|---|---|---|---|
| East | 650 | 325 | 2 | 450 | 200 |
| North | 1050 | 350 | 3 | 500 | 250 |
| South | 900 | 300 | 3 | 400 | 150 |

**Version note:** The Microsoft page lists Microsoft 365, 2024 and 2021 for Windows; the same menu has long existed in older versions (from memory, unverified).
**Edge cases:** You cannot change the summary function for calculated fields or OLAP data (Microsoft Support).
**Likely follow-ups:** 1) *Count vs Count Numbers?* Count Numbers ignores text. 2) *Distinct count?* Q40.
**Common mistakes:** Averages of averages; forgetting that the Count includes blank-looking text.

### Q18 ⭐⭐ 🟢 How do you show values as a percentage of the grand total or of the row total in a pivot table?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know Show Values As, not formulas?
**Say this in the interview:** "Right-click a value > Show Values As > % of Grand Total or % of Row Total. It divides each number by the chosen total, and I can keep the raw numbers alongside by adding the field twice."
**Explain simply:**
- Microsoft Support ("Show different calculations in PivotTable value fields"): % of Grand Total = share of everything; % of Row Total = share of its row; % of Column Total = share of its column.
- Drag the field into Values twice to see both the amount and the percentage.
**Example:** North's 750 laptop sales are 71.4% of North's 1050.
**Sample sheet:** Q6 pivot.
**Formula / Steps (not run here; Microsoft Support):** Right-click a value > Show Values As > % of Grand Total (or % of Row Total).
**Alternative:** A normal formula next to a GETPIVOTDATA value, or calculation in the source with SUMIFS.
**Result:** pandas reproduction, run here. % of Grand Total (2600):

| Region | Laptop | Phone | Total |
|---|---|---|---|
| East | 17.3 | 7.7 | 25.0 |
| North | 28.8 | 11.5 | 40.4 |
| South | 15.4 | 19.2 | 34.6 |
| Grand Total | 61.5 | 38.5 | 100.0 |

% of Row Total: East 69.2 / 30.8; North 71.4 / 28.6; South 44.4 / 55.6.
**Version note:** Applies to Excel 2016 to 365; Mac may need More Options (Microsoft Support).
**Edge cases:** Rounded percentages may not add to exactly 100.
**Likely follow-ups:** 1) *% of column?* Same menu. 2) *% of parent?* Also in Show Values As (from memory, unverified).
**Common mistakes:** Picking row total when you meant grand total; formatting the numbers as percent after already using Show Values As.

### Q19 ⭐⭐ 🟢 How do you sort a pivot table by the values column (largest to smallest)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you sort by the number, not alphabetically?
**Say this in the interview:** "I right-click a number in the Grand Total column, choose Sort, and pick Largest to Smallest. Or use the Row Labels dropdown > Sort by Value."
**Explain simply:**
- Default order is A to Z by label, which is rarely what you want.
- Microsoft Support ("Sort data in a PivotTable or PivotChart"): right-click any number in the Grand Total column and choose Sort, or use Sort by Value from the Row Labels filter arrow.
- The sort stays when you refresh.
**Example:** Regions sorted from highest to lowest sales.
**Sample sheet:** Q6 data.
**Formula / Steps (not run here; Microsoft Support):** Right-click a value in the Grand Total column > Sort > Sort Largest to Smallest.
**Alternative:** Row Labels dropdown > More Sort Options > Descending (by Sum of Amount).
**Result:** pandas reproduction, run here: North 1050, South 900, East 650.
**Version note:** Applies to Excel 2016 to 365 (Microsoft Support).
**Edge cases:** Sorting a column inside a cross-tab sorts by that column only. Ties keep label order (from memory, unverified).
**Likely follow-ups:** 1) *Top N only?* Q11. 2) *Custom order Jan-Dec?* Q49.
**Common mistakes:** Sorting the label column instead of the value; sorting copied static values.

### Q20 ⭐⭐ 🟢 How do you drill down into a number in a pivot table to see the rows behind it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know you can audit any pivot number back to the raw records?
**Say this in the interview:** "I double-click the number. Excel opens a new sheet listing exactly the source rows that add up to it, so I can check or explain the figure."
**Explain simply:**
- A pivot cell is a total. Drill down (Excel calls it Show Details) lists the individual rows inside that total.
- It copies the rows to a new sheet; the original data is not touched.
- Useful when a manager asks "why is IT payroll 1,98,000?"
**Example:** Salary by department; you double-click IT's total.
**Sample sheet (source data):**

| | A Employee | B Department | C Location | D Salary |
|---|---|---|---|---|
| 2 | E01 | IT | Hyderabad | 60000 |
| 3 | E02 | IT | Bengaluru | 72000 |
| 4 | E03 | HR | Hyderabad | 45000 |
| 5 | E04 | HR | Hyderabad | 48000 |
| 6 | E05 | Sales | Bengaluru | 52000 |
| 7 | E06 | Sales | Bengaluru | 58000 |
| 8 | E07 | IT | Hyderabad | 66000 |

**Formula / Steps (not run here; steps from Microsoft Support, "Expand, collapse, or show details in a PivotTable or PivotChart"):**
1. Double-click the value cell (for example IT's 198000).
2. Or right-click it > Show Details.
3. To remove the new sheet: right-click its tab > Hide or Delete.

**Alternative:** Filter the raw sheet on Department = IT yourself (Data > Filter).
**Result (pandas, run):** the pivot gives HR 93000, IT 198000, Sales 110000; the rows behind IT are E01 (60000), E02 (72000), E07 (66000), which sum to 198000. The double-click output itself is not run here.
**Version note:** Microsoft's page lists Microsoft 365, Excel 2024, 2021, 2019 and 2016 (Microsoft Support).
**Edge cases:** Switch it off under PivotTable Options > Data > "Enable show details" (Microsoft Support). Not available for OLAP sources. Each double-click creates a new sheet, so delete them to keep the file tidy.
**Likely follow-ups:** 1) Does editing that sheet change the pivot? No, it is a copy. 2) Can you drill on a Grand Total? Yes, it lists all rows.
**Common mistakes:** Double-clicking a row label (that expands or collapses it instead); forgetting to delete the spare sheets.

### Q21 ⭐⭐ 🟢 How do you move or remove a field from a pivot table?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you rearrange a pivot without rebuilding it?
**Say this in the interview:** "I drag the field from one area of the Fields pane to another, or drag it out or untick it to remove it. The pivot rebuilds instantly and the source data is unchanged."
**Explain simply:**
- A field is a column heading from your data (Department, Location, Salary).
- Move: drag it between Rows, Columns, Values and Filters in the PivotTable Fields pane.
- Remove: drag it out of the pane or untick its box. This only removes it from the report, never from the data.
**Example:** Headcount by Department (rows). You drag Location into Columns to get a cross-tab, then untick it to go back.
**Sample sheet:** same 7-row employee data as Q20.
**Formula / Steps (not run here; steps from Microsoft Support, "Create a PivotTable to analyze worksheet data"):**
1. Click inside the pivot so the PivotTable Fields pane shows.
2. To move: drag the field name to the target area.
3. To remove: drag it out of the area box, or untick it in the field list.

**Alternative:** Right-click a field in the pane > "Move to Column Labels / Row Labels" (from memory, unverified).
**Result (pandas, run):** Department only: HR 2, IT 3, Sales 2. After adding Location to columns: HR (Bengaluru -, Hyderabad 2), IT (1, 2), Sales (2, -); blanks show where no one exists.
**Version note:** The Microsoft page covers Microsoft 365, 2024, 2021, 2019 and 2016.
**Edge cases:** Order inside an area matters (Department above Location nests Location inside Department). Removing the only Values field leaves an empty pivot.
**Likely follow-ups:** 1) Drag the same field twice? Fine in Values (e.g. Sum and Count). 2) Undo? Ctrl+Z works.
**Common mistakes:** Deleting the pivot cells instead of removing the field; thinking removal deletes source data.

### Q22 ⭐⭐ 🟢 What are Grand Totals and Subtotals in a pivot table, and how do you turn them off?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand totals in a pivot and how to control them for a clean report?
**Say this in the interview:** "Grand totals are the overall row and column totals; subtotals are totals for each outer group when I have two row fields. I switch them off under Design > Grand Totals and Design > Subtotals."
**Explain simply:**
- Grand Total: total of everything, shown at the bottom (all rows) and right (all columns).
- Subtotal: a total per group, for example per Department when Location sits inside it. You need at least two row (or column) fields to see subtotals.
- Both are on by default and can be hidden without changing the numbers.
**Example:** Salary by Department and Location.
**Sample sheet:** same data as Q20.
**Formula / Steps (not run here; steps from Microsoft Support, "Subtotal and total fields in a PivotTable" and "Show or hide subtotals and totals in a PivotTable"):**
1. Grand totals: click the pivot > Design tab > Layout group > Grand Totals > choose Off for Rows and Columns (or only rows or only columns).
2. Subtotals: Design > Subtotals > Do Not Show Subtotals.
3. One field only: PivotTable Analyze > Active Field > Field Settings > Subtotals: None.

**Alternative:** PivotTable Analyze > Options > Totals & Filters tab > clear "Show grand totals for rows/columns".
**Result (pandas, run):** Grand total 401000 (Bengaluru 182000, Hyderabad 219000). Subtotals per Department: HR 93000, IT 198000, Sales 110000.
**Version note:** Microsoft's subtotal page lists Microsoft 365, 2024 and 2021; the show/hide page and Design-tab steps are the same in older versions from memory, unverified.
**Edge cases:** A grand total of averages is the average of all rows, not the average of the group averages. Turning totals off does not stop GETPIVOTDATA references from working.
**Likely follow-ups:** 1) Subtotals at top or bottom? Design > Subtotals. 2) Why no subtotals? Only one row field.
**Common mistakes:** Hiding the grand total and then quoting a wrong sum by eye; forgetting Design tab only appears when a pivot cell is selected.

### Q23 ⭐⭐ 🟢 How do you change the number format of values in a pivot table (for example currency or percent)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know to format via the value field, so formatting survives refresh?
**Say this in the interview:** "I right-click a value, choose Number Format, and pick Currency or Percentage there. Formatting through the field sticks when the pivot refreshes, unlike cell formatting."
**Explain simply:**
- Number format only changes how a number looks, not its value.
- Set it on the value field, so every cell of that field follows.
- Formatting cells by hand with the ribbon can be lost when the layout changes.
**Example:** Total salary shown as 245,000 with thousand separators, attrition shown as 18.3%.
**Formula / Steps (not run here; steps from Microsoft Support, "Design the layout and format of a PivotTable"):**
1. Select the value field in the pivot.
2. PivotTable Analyze > Active Field > Field Settings (opens Value Field Settings).
3. Click Number Format > pick category > OK twice.
4. Shortcut: right-click a value > Number Format.

**Alternative:** Write the format yourself in a normal sheet with TEXT.
**Result (LibreOffice, run, analogue of the format codes):** `=TEXT(245000,"#,##0")` returns 245,000; `=TEXT(0.1834,"0.0%")` returns 18.3%; `=TEXT(245000,"[$₹-4009]#,##0.00")` returns ₹245,000.00. The pivot dialog itself is not run here.
**Version note:** Microsoft's page covers Microsoft 365, 2024, 2021, 2019, 2016.
**Edge cases:** Percent needs the underlying value to be a fraction (0.1834) or a Show Values As percent. TEXT output is text, so do not feed it back into sums.
**Likely follow-ups:** 1) Format lost on refresh? Check "Preserve cell formatting on update" (Q44). 2) Indian lakh style? Needs a custom format; not verified here.
**Common mistakes:** Formatting cells by selecting them; formatting before dragging in a second value field.

### Q24 ⭐⭐ 🟢 How do you rename a field or the column heading in a pivot table?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you make a report readable ("Sum of Salary" to "Total Salary")?
**Say this in the interview:** "I click the heading cell, type the new name and press Enter, or use Value Field Settings > Custom Name. The data is not affected."
**Explain simply:**
- Excel auto-names value columns "Sum of Salary" or "Count of Employee ID".
- Renaming changes only the label in the pivot.
- A name cannot be identical to an existing field name.
**Example:** "Sum of Salary" becomes "Total Salary (INR)".
**Formula / Steps (not run here; Microsoft's layout page gave no rename steps, so these are from memory, unverified):**
1. Click the heading cell (e.g. "Sum of Salary"), type a new name, Enter.
2. Or right-click a value > Value Field Settings > Custom Name > OK.
3. Row labels: click the item and type over it.

**Alternative:** Rename the column in the source data before building the pivot.
**Result:** not run here; no calculation involved.
**Version note:** From memory, unverified: works the same in 2016 to 365.
**Edge cases:** If Excel says the name already exists, add a trailing space or choose a different word (from memory). Renaming a row item only changes that pivot.
**Likely follow-ups:** 1) Does renaming break formulas? A GETPIVOTDATA formula using the old name can break (Q54). 2) Rename the pivot itself? PivotTable Analyze > PivotTable Name box.
**Common mistakes:** Retyping a heading as an exact field name; editing the source header and expecting the pivot to follow without Refresh.

### Q25 ⭐⭐ 🟢 How do you show items with no data (zeros) instead of blank cells in a pivot table?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the "For empty cells show" option?
**Say this in the interview:** "In PivotTable Options on the Layout & Format tab I tick 'For empty cells show' and type 0. Blanks then display as zeros."
**Explain simply:**
- A blank means the combination (for example Sales in Hyderabad) has no rows.
- That option replaces blanks with text or a number you choose.
- It affects display only; the pivot does not add real rows.
**Example:** Headcount by Department and Location. HR in Bengaluru shows blank; HR has no one there, so show 0.
**Sample sheet:** employee data from Q20.
**Formula / Steps (not run here; steps from Microsoft Support, "Design the layout and format of a PivotTable"):**
1. Click in the pivot > PivotTable Analyze > PivotTable group > Options.
2. Layout & Format tab > under Format tick "For empty cells show".
3. Type 0 in the box > OK.

**Alternative:** Conditional formatting or a number format; not as clean.
**Result (pandas, run, fill_value=0):** before: HR Bengaluru NaN, Sales Hyderabad NaN. After: HR (0, 2), IT (1, 2), Sales (2, 0).
**Version note:** Microsoft's PivotTable options page lists 365, 2024, 2021; this option is old and exists in earlier versions (from memory).
**Edge cases:** The same dialog has "For error values show" for #DIV/0! (Microsoft Support, "PivotTable options"). Blanks in the source data itself are separate: an empty source cell is not an empty pivot cell.
**Likely follow-ups:** 1) Show missing items entirely? Field Settings > Layout & Print > Show items with no data (from memory). 2) Does the zero count in averages? No, it is only display.
**Common mistakes:** Typing "0" in the cell directly; confusing blank with zero in data.

### Q26 ⭐⭐ 🟢 What are Recommended PivotTables, and in which Excel versions can you use them?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know Excel can suggest ready-made pivots, and where it applies?
**Say this in the interview:** "Insert > Recommended PivotTables shows previews of suggested layouts for my data, and I pick one. Microsoft's help page says it is available to Microsoft 365 subscribers, so I would check older versions before relying on it."
**Explain simply:**
- Excel scans your data and proposes several pivots with sample thumbnails.
- It is a shortcut for beginners; you can still rearrange fields afterwards.
- It guesses, so always check it answers your question.
**Example:** A payroll sheet; Excel offers "Sum of Salary by Department". You click it and get the pivot.
**Formula / Steps (not run here; steps from Microsoft Support, "Create a PivotTable to analyze worksheet data"):**
1. Click a cell in the data.
2. Insert > Recommended PivotTable.
3. Pick a layout > OK. It opens on a new sheet (or choose Existing sheet).

**Alternative:** Insert > PivotTable and build manually.
**Result:** not run here; feature is a UI command.
**Version note:** The Microsoft page says "Recommended PivotTables are available only to Microsoft 365 subscribers", while the same page lists 2016 to 2024 for the general steps. My memory says the button existed since Excel 2013; that conflicts and is unverified, so check on the exact version.
**Edge cases:** Poorly structured data (merged cells, blank headers) gives poor suggestions. It is not in Excel for Google Sheets (Sheets has "Suggested" pivots, from memory, unverified).
**Likely follow-ups:** 1) Manual vs recommended? Manual gives control. 2) Can you edit it? Yes.
**Common mistakes:** Trusting a suggestion without checking field choice; clicking while a blank cell is selected.

### Q27 ⭐⭐ 🟢 How do you change the layout of a pivot table to Compact, Outline or Tabular form, and when would you use each?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the three layouts and why tabular is best for copying data out?
**Say this in the interview:** "Design > Report Layout, then Compact, Outline or Tabular. Compact is the default and saves space; Outline is the classic style; Tabular gives one column per field, so it is best when I copy cells to another sheet."
**Explain simply:**
- Compact: all row fields stacked in one indented column. Narrow, good for screens.
- Outline: each row field gets its own column, with subtotals above the group.
- Tabular: one column per field with headers, like a normal table. Subtotals at the bottom.
**Example:** Salary by Department and Location, same numbers, three shapes.
**Sample layout (drawn by hand from the verified totals; the click is not run here):**

| Tabular | Department | Location | Sum of Salary |
|---|---|---|---|
| | HR | Hyderabad | 93000 |
| | IT | Bengaluru | 72000 |
| | IT | Hyderabad | 126000 |
| | Sales | Bengaluru | 110000 |

Compact shows one "Row Labels" column with HR, then indented Hyderabad, then IT with Bengaluru and Hyderabad indented under it; Outline shows Department and Location in separate columns but the department total sits on the department's own row.
**Formula / Steps (not run here; steps from Microsoft Support, "Design the layout and format of a PivotTable"):**
1. Click the pivot > Design > Layout group > Report Layout.
2. Choose Show in Compact / Outline / Tabular Form.
3. Optional: Repeat All Item Labels (from memory) to fill every row in Tabular.

**Alternative:** Field Settings > Layout & Print for one field.
**Result (pandas, run):** the tabular rows above (HR/Hyderabad 93000; IT/Bengaluru 72000; IT/Hyderabad 126000; Sales/Bengaluru 110000).
**Version note:** Microsoft's page: 365, 2024, 2021, 2019, 2016.
**Edge cases:** In Compact form, the single column header says "Row Labels" instead of field names.
**Likely follow-ups:** 1) Which for a dashboard? Compact. 2) Which feeds another table or Power BI? Tabular with repeated labels.
**Common mistakes:** Copying a Compact pivot and wondering why Department and Location are merged in one column.

### Q28 ⭐⭐ 🟢 Given a daily attendance sheet with Employee, Date and Status (Present/Absent/Leave), how do you summarise days present per employee per month with a pivot table?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you combine grouping dates, a filter and Count in one HR report?
**Say this in the interview:** "Employee in Rows, Date grouped by Months in Columns, Status in Values as Count, and I filter Status to Present."
**Explain simply:**
- Each row is one day for one person. Counting rows with Status = Present gives days present.
- Status is text, so Excel will Count it by default (use Count, not Sum).
- Group the dates by month, otherwise every date becomes its own column.
**Example:** Three employees, three working days in Jan and three in Feb (shortened for illustration).
**Sample sheet:**

| | A Employee | B Date | C Status |
|---|---|---|---|
| 2 | E01 | 05-Jan-2026 | Present |
| 3 | E01 | 06-Jan-2026 | Present |
| 4 | E02 | 06-Jan-2026 | Leave |
| 5 | E03 | 05-Jan-2026 | Absent |
| 6 | E03 | 07-Jan-2026 | Present |
| 7 | E01 | 04-Feb-2026 | Absent |

(Full test set used for the result below: 18 rows, 3 employees x 6 days.)
**Formula / Steps (not run here; steps from Microsoft Support "Create a PivotTable to analyze worksheet data" and "Group or ungroup data in a PivotTable"):**
1. Insert > PivotTable on the table.
2. Employee to Rows; Date to Columns; Status to Values (it shows Count of Status).
3. Right-click a date > Group > Months (add Years if data spans years) > OK.
4. Put Status in Filters (or use the Status filter) and choose Present.

**Alternative:** `=COUNTIFS(A:A,E2,C:C,"Present",B:B,">="&F1,B:B,"<="&G1)` per employee and month (not run on this data).
**Result (pandas, run on the 18-row set):**

| Employee | Jan | Feb | Grand Total |
|---|---|---|---|
| E01 | 3 | 2 | 5 |
| E02 | 2 | 3 | 5 |
| E03 | 1 | 2 | 3 |
| Grand Total | 6 | 7 | 13 |

**Version note:** Date auto-grouping and the Group command per Microsoft page; Microsoft 365 may auto-group date fields on adding them (Microsoft Support).
**Edge cases:** Half-days or "WFH" statuses need their own filter value. If dates are text, grouping fails (Q38). Use a Year too, or Jan 2025 and Jan 2026 merge.
**Likely follow-ups:** 1) Percent present? Show Values As > % of Row Total with Status in Columns. 2) Include leave? Tick it in the filter.
**Common mistakes:** Not filtering Status, so the count includes absences; forgetting to group dates.

### Q29 ⭐⭐ 🟢 How do you apply a filter to a pivot table for one department only (using the Filters area)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the Filters area applies a whole-report filter?
**Say this in the interview:** "I drag Department into the Filters area, then use the dropdown above the pivot to pick the department. The whole report then shows only that department."
**Explain simply:**
- The Filters area (also called Report Filter) sits above the pivot as a dropdown.
- It limits the data feeding the pivot without taking up rows or columns.
- You can select one item or several.
**Example:** Salary by Location, filtered to IT.
**Sample sheet:** employee data from Q20.
**Formula / Steps (not run here; Microsoft's create page did not describe the Filters area, so steps are from memory, unverified):**
1. Drag Department from the field list into Filters.
2. Click the dropdown in cell B1 (above the pivot).
3. Choose IT > OK. For several: tick "Select Multiple Items".

**Alternative:** Put Department in Rows and use its label filter, or add a slicer (Q9, Q14).
**Result (pandas, run):** unfiltered Location totals Bengaluru 182000, Hyderabad 219000; filtered to IT: Bengaluru 72000, Hyderabad 126000.
**Version note:** Filters area exists in all pivot versions (from memory); the Microsoft page lists only Rows, Columns and Values, so say "Filters" as the pane label.
**Edge cases:** A filtered-out item is hidden, not deleted; grand totals reflect only visible items.
**Likely follow-ups:** 1) Show one page per department? Options > Show Report Filter Pages (from memory). 2) Filter vs slicer? Slicer is visual (Q14).
**Common mistakes:** Forgetting that a filter is active and quoting a partial total.

### Q30 ⭐⭐ 🟡 What is a calculated field in a pivot table, and how do you create one?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you add a formula column inside a pivot, and do you know how it totals?
**Say this in the interview:** "A calculated field is a new field built from existing fields, such as Revenue divided by Units. I add it under PivotTable Analyze > Fields, Items & Sets > Calculated Field."
**Explain simply:**
- It is a formula on the pivot's summed values, not on individual rows.
- It cannot use cell references or defined names (Microsoft Support).
- The grand total is calculated on grand totals (total revenue / total units), which is usually the correct blended figure.
**Example:** Average price = Revenue / Units by region.
**Sample sheet:**

| | A Region | B Revenue | C Units |
|---|---|---|---|
| 2 | East | 1000 | 10 |
| 3 | East | 1500 | 25 |
| 4 | West | 2000 | 40 |
| 5 | West | 900 | 9 |
| 6 | North | 700 | 7 |
| 7 | North | 1300 | 13 |

**Formula / Steps (not run here; steps from Microsoft Support, "Calculate values in a PivotTable"):**
1. Select the pivot > PivotTable Analyze > Calculations > Fields, Items & Sets > Calculated Field.
2. Name: Price. Formula: `=Revenue/Units`.
3. Add > OK.

**Alternative:** Add a helper column in the source data (`=B2/C2`), but that averages poorly; or a Power Pivot measure.
**Result (pandas, run):** East 2500/35 = 71.43; North 2000/20 = 100.00; West 2900/49 = 59.18; Grand Total 7400/104 = 71.15 (sum-based; not the 76.87 simple average of the three prices).
**Version note:** Microsoft page lists 365, 2024, 2021, 2019, 2016.
**Edge cases:** Division by zero shows #DIV/0!. Not allowed for OLAP sources (Microsoft Support).
**Likely follow-ups:** 1) Why not a helper column? Row-level ratios averaged are wrong. 2) Can you reference a cell? No.
**Common mistakes:** Expecting it to average row-level ratios; typing a name that clashes with an existing field.

### Q31 ⭐⭐ 🟡 What is the difference between a calculated field and a calculated item?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know one works across fields, the other within a field's items?
**Say this in the interview:** "A calculated field computes from other fields, like Revenue / Units. A calculated item computes from items inside one field, like East + West as a new region row. Fields are the common choice; items are fussier."
**Explain simply:**
- Field: new column built from other fields, calculated on sums.
- Item: new row inside a field built from its own items.
- Items can double count in totals and need ungrouped fields (Microsoft Support).
**Example:** Region items East 2500, West 2900, North 2000. Add item "East+West" = 5400.
**Formula / Steps (not run here; steps from Microsoft Support, "Calculate values in a PivotTable"):**
1. Calculated item: select a Region label (ungroup if grouped) > PivotTable Analyze > Fields, Items & Sets > Calculated Item.
2. Name `East+West`, formula `=East+West` > Add.

**Alternative:** Group items (Q61) or a helper column in the source such as a region-group column.
**Result (pandas, run):** East+West = 5400. Region sum was 7400; with the extra item it becomes 12800, double counting East and West.
**Version note:** Microsoft page: 365, 2024, 2021, 2019, 2016.
**Edge cases:** Neither can use cell references, array functions or totals; neither works on OLAP pivots (Microsoft Support). Microsoft's wording on how items sum in totals is limited to a commission example.
**Likely follow-ups:** 1) Why avoid items? Easy to inflate totals. 2) Which is more used? Calculated field.
**Common mistakes:** Mixing them up; forgetting to ungroup before adding an item; trusting the grand total with items present.

### Q32 ⭐⭐ 🟡 How do you connect one slicer to multiple pivot tables?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you build a dashboard where one click filters everything?
**Say this in the interview:** "Select the slicer, go to Report Connections and tick every pivot table. They must share the same source data."
**Explain simply:**
- A slicer is a set of clickable buttons that filter a pivot.
- Report Connections lists all pivots that can be linked.
- Pivots built from different sources will not appear in the list.
**Example:** Two pivots, Amount by Product and Amount by Region; one Region slicer drives both.
**Sample sheet:**

| | A Region | B Product | C Amount |
|---|---|---|---|
| 2 | East | A | 1000 |
| 3 | East | B | 1500 |
| 4 | West | A | 2000 |
| 5 | West | B | 900 |
| 6 | North | A | 700 |
| 7 | North | B | 1300 |

**Formula / Steps (not run here; steps from Microsoft Support, "Use slicers to filter data"):**
1. Make the second pivot from the same data.
2. Select the slicer > Slicer tab > Report Connections.
3. Tick each pivot > OK.

**Alternative:** Build every pivot from one pivot cache (copy the pivot) so they connect automatically (from memory, unverified).
**Result (pandas, run):** Slicer = East: Product pivot A 1000, B 1500; Region pivot East 2500. Slicer cleared: Product A 3700, B 3700; Region East 2500, North 2000, West 2900. The click itself is not run here.
**Version note:** Microsoft: slicers connect only to pivots with the same data source; web has local-pivot creation only; Mac uses the Slicer Settings pane (Microsoft Support).
**Edge cases:** Slicers for Data Model pivots need Windows or Mac Excel (Microsoft Support).
**Likely follow-ups:** 1) One slicer, many sheets? Yes. 2) Pivot missing from the list? Different source.
**Common mistakes:** Creating the second pivot from a copy of the data; forgetting to refresh.

### Q33 ⭐⭐ 🟡 What is a timeline slicer, and how is it different from a normal slicer?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the date-specific filter?
**Say this in the interview:** "A timeline is a slicer built for dates: a scrollbar where I pick a range of months, quarters, years or days. A normal slicer shows buttons for each text item."
**Explain simply:**
- Normal slicer: buttons for any field (Region, Department).
- Timeline: only date fields; drag across tiles for a range.
- It can switch between years, quarters, months and days (Microsoft Support).
**Example:** Show sales for Feb to Mar 2026 with one drag.
**Sample sheet:**

| | A Date | B Amount |
|---|---|---|
| 2 | 10-Jan-2026 | 100 |
| 3 | 15-Feb-2026 | 200 |
| 4 | 05-Mar-2026 | 300 |
| 5 | 20-Mar-2026 | 150 |
| 6 | 02-Apr-2026 | 400 |

**Formula / Steps (not run here; steps from Microsoft Support, "Create a PivotTable timeline to filter dates"):**
1. Click in the pivot > PivotTable Analyze > Insert Timeline.
2. Tick the date field > OK.
3. Pick months, drag the handles.
4. Link more pivots: Report Connections (same source).

**Alternative:** Group dates and use a normal slicer on Months.
**Result (pandas, run):** 01-Feb to 31-Mar selects 15-Feb, 05-Mar, 20-Mar, total 650.
**Version note:** Microsoft page lists 365, 2024, 2021, 2019, 2016. Not for Google Sheets pivots (from memory, unverified).
**Edge cases:** Needs a real date field; text dates will not offer a timeline (Q38).
**Likely follow-ups:** 1) Clear? Clear Filter button. 2) Several pivots? Report Connections.
**Common mistakes:** Using it on text "dates"; picking the wrong level (Days) and wondering why it is long.

### Q34 ⭐⭐ 🟡 How do you use Show Values As to show month-over-month change (difference and percentage) in a pivot table?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you compute growth inside a pivot without extra columns?
**Say this in the interview:** "I drop Sales in Values twice. On the second copy: Show Values As > Difference From, base field Month, base item Previous. A third copy with % Difference From gives the percentage."
**Explain simply:**
- Show Values As changes how a number is displayed relative to something else.
- Difference From subtracts the base item; % Difference From divides that gap by the base.
- The first month has nothing to compare, so it is blank.
**Example:** Monthly sales Jan to Apr.
**Sample sheet:**

| | A Month | B Sales |
|---|---|---|
| 2 | Jan | 200000 |
| 3 | Feb | 230000 |
| 4 | Mar | 207000 |
| 5 | Apr | 248400 |

**Formula / Steps (not run here; steps from Microsoft Support, "Show different calculations in PivotTable value fields"):**
1. Drag Month to Rows and Sales to Values twice.
2. Right-click the second copy > Show Values As > Difference From.
3. Base field Month, base item (previous).
4. Repeat on the third copy > % Difference From.

**Alternative:** In a sheet: `=B3-B2` and `=B3/B2-1`.
**Result (pandas, run):** Feb +30000 (15%), Mar -23000 (-10%), Apr +41400 (20%); Jan blank.
**Version note:** Microsoft page lists the options; the "(previous)" base item wording is from memory, unverified.
**Edge cases:** Missing months break the "previous" chain; sort months in calendar order (Q49).
**Likely follow-ups:** 1) YoY? Q35. 2) Show only the change? Hide the raw column.
**Common mistakes:** Applying Show Values As to the only value column, losing the raw figure; wrong base field.

### Q35 ⭐⭐ 🟡 How do you calculate year-over-year growth percentage with a pivot table?
**Asked at:** One candidate account of a Mahindra Finance MIS assignment mentions a pivot with YoY %; seen only in a search summary, attribution unverified. Otherwise commonly asked.
**What the interviewer is checking:** Can you compare the same period across years?
**Say this in the interview:** "Months in Rows, Year in Columns, Sales in Values twice, and on the second copy I use Show Values As > % Difference From with base field Year and base item Previous."
**Explain simply:**
- YoY compares a period with the same period last year.
- Layout: months down, years across, so each month sits beside its twin.
- Total-year growth uses the Grand Total row of the same pivot.
**Example:** Q1 sales 2024 vs 2025.
**Sample sheet:**

| | A Year | B Month | C Sales |
|---|---|---|---|
| 2 | 2024 | Jan | 100 |
| 3 | 2024 | Feb | 120 |
| 4 | 2024 | Mar | 150 |
| 5 | 2025 | Jan | 115 |
| 6 | 2025 | Feb | 114 |
| 7 | 2025 | Mar | 180 |

**Formula / Steps (not run here; steps from Microsoft Support, "Show different calculations in PivotTable value fields"):**
1. Month to Rows, Year to Columns, Sales to Values twice.
2. On the second Sales: Show Values As > % Difference From > base field Year, base item (previous).

**Alternative:** Next to the pivot: `=C2/B2-1`.
**Result (pandas, run):** Jan +15%, Feb -5%, Mar +20%; full year 370 to 409 = +10.54%.
**Version note:** Show Values As is in 2016 to 365 (Microsoft Support). Date grouping gives Year/Month fields if dates are real dates.
**Edge cases:** First year column is blank. If a month is missing in one year the percent is blank or wrong.
**Likely follow-ups:** 1) Dates instead of Year/Month columns? Group by Years and Months (Q13). 2) Fiscal year? Add a helper column.
**Common mistakes:** Comparing a partial year with a full year; showing the % column but not the raw one.

### Q36 ⭐⭐ 🟡 How do you group numbers in a pivot table, for example salary bands or age groups of 10 years?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you create bands without helper formulas?
**Say this in the interview:** "I put Age in Rows, right-click a value, choose Group, set Starting at, Ending at and By 10, then count employees in Values."
**Explain simply:**
- Grouping turns many individual numbers into ranges.
- You choose start, end and interval.
- Anything below start or above end goes into a "<start" or ">end" group (from memory, unverified).
**Example:** Age bands for headcount.
**Sample sheet:**

| | A Employee | B Age |
|---|---|---|
| 2 | A | 24 |
| 3 | B | 28 |
| 4 | C | 31 |
| 5 | D | 35 |
| 6 | E | 39 |
| 7 | F | 42 |
| 8 | G | 47 |
| 9 | H | 53 |

**Formula / Steps (not run here; steps from Microsoft Support, "Group or ungroup data in a PivotTable"):**
1. Age to Rows, Employee to Values (Count).
2. Right-click an age value > Group.
3. Tick Starting at / Ending at (20 / 60), By = 10 > OK.

**Alternative:** Helper column in the source: `=FLOOR(B2,10)` or a lookup table band.
**Result (pandas, run, bins 20-29, 30-39, 40-49, 50-59):** 2, 3, 2, 1 (total 8). Salary bands of 20000 on separate data (28k, 34k, 41k, 47k, 52k, 58k, 66k, 81k, with an extra top bin so 81k is not dropped): 20-40k 2; 40-60k 4; 60-80k 1; 80k+ 1.
**Version note:** Microsoft's grouping page; works across current versions.
**Edge cases:** Blank or text cells in the field stop grouping (Q38). In the pandas check each band includes its lower bound and excludes its upper bound (30 falls in 30-39); Excel's Group dialog labels bands like 20-29.
**Likely follow-ups:** 1) Uneven bands (0-5, 5-10 years)? Use a helper lookup column. 2) Percent per band? Show Values As > % of Column Total.
**Common mistakes:** Ending too low so the top earners disappear into one tail group; grouping a field that has text.

### Q37 ⭐⭐ 🟡 How do you build a pivot chart that updates when you click a slicer?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand that a slicer filters the pivot and the pivot chart follows it?
**Say this in the interview:** "I make the pivot, insert a PivotChart from it, and insert a slicer on the same pivot. Clicking the slicer filters the pivot and the chart redraws."
**Explain simply:**
- A pivot chart is a chart bound to a pivot, so it always mirrors it.
- A slicer filters the pivot; the chart changes because the pivot did.
- One slicer can drive several pivots and charts (Q32).
**Example:** Chart of Amount by Product; slicer on Region.
**Sample sheet:** data from Q32.
**Formula / Steps (not run here; steps from memory for PivotChart insertion, unverified; slicer steps from Microsoft Support "Use slicers to filter data"):**
1. Click in the pivot > PivotTable Analyze > PivotChart > choose a type.
2. Select the pivot > PivotTable Analyze > Insert Slicer > tick Region > OK.
3. Click a region button.

**Alternative:** Use the chart's own field buttons as filters.
**Result (pandas, run, charts not run here):** slicer = East gives A 1000, B 1500; no slicer gives A 3700, B 3700.
**Version note:** Slicers work in 2016 to 365 (Microsoft Support). In Excel for the web only local pivot slicer creation is available (Microsoft Support).
**Edge cases:** Slicer filters the whole pivot, so every chart on it changes. Chart formatting can reset on refresh unless you keep "Preserve cell formatting" settings.
**Likely follow-ups:** 1) Two charts, one slicer? Report Connections. 2) Hide the field buttons? Chart Analyze > Field Buttons.
**Common mistakes:** Building a normal chart on pivot cells instead of a PivotChart; placing the slicer on a different pivot.

### Q38 ⭐⭐ 🟡 Why does a pivot table not let you group dates, and how do you fix it (blank cells or text dates)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you diagnose bad data behind the "Cannot group that selection" error?
**Say this in the interview:** "Grouping needs a field made only of real dates. Blanks or text dates in the column block it, so I fill the blanks and convert text to dates, then refresh and group again."
**Explain simply:**
- Real dates are numbers underneath. A text "2026-01-12" looks like a date but is text.
- A blank row in the date column also blocks grouping (from memory; Microsoft's page does not say why grouping fails).
- Fix the source, not the pivot.
**Example:** Joining dates with one text entry and one blank.
**Sample sheet:**

| | A JoinDate |
|---|---|
| 2 | 05-Jan-2026 (real date) |
| 3 | '2026-01-12 (text) |
| 4 | (blank) |
| 5 | 03-Feb-2026 (real date) |

**Formula / Steps:**
1. Check: `=ISNUMBER(A2)`, `=ISBLANK(A2)`.
2. Convert text dates: `=IF(ISTEXT(A3),DATEVALUE(A3),A3)`, or Data > Text to Columns > Date.
3. Fill or remove blank rows (or give them a real placeholder date).
4. Refresh the pivot > right-click a date > Group (steps from Microsoft Support, "Group or ungroup data in a PivotTable"; not run here).

**Alternative:** Add a helper column `=TEXT(A2,"mmm-yyyy")` and pivot on it as text (loses date order).
**Result (LibreOffice, run):** ISNUMBER gives TRUE, FALSE, FALSE, TRUE; ISBLANK gives FALSE, FALSE, TRUE, FALSE; COUNT = 2, COUNTA = 3, COUNTBLANK = 1. DATEVALUE converts the text to serial 46034. The grouping error itself is not run here.
**Version note:** Microsoft says time-related fields can be auto-grouped when added to a pivot (Microsoft Support); that behaviour needs 2016 or later (from memory).
**Edge cases:** DATEVALUE depends on regional format (dd/mm vs mm/dd) and can differ between Excel and LibreOffice. Dates with errors (#N/A) also block grouping.
**Likely follow-ups:** 1) New rows keep failing? Convert the source to a Table. 2) Already grouped but wrong? Right-click > Ungroup.
**Common mistakes:** Fixing the pivot instead of the data; forgetting to Refresh after fixing.

### Q39 ⭐⭐ 🟡 How do you use a pivot table to find duplicate values in a column?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you use a pivot as a quick data-quality tool, not just a reporting tool?
**Say this in the interview:** "I put the column in Rows and the same column in Values as Count. Any item with a count above 1 is a duplicate. Then I filter Count greater than 1."
**Explain simply:**
- A pivot table (a drag-and-drop summary table) lists each distinct value once, so the count beside it tells you how many times it appears.
- Count = 1 means unique; 2 or more means duplicate.
- Use the Rows drop-down > Value Filters > Greater Than > 1 to show only duplicates.
**Example:** HR suspects an Employee ID was keyed twice in an 8-row attendance list.
**Sample sheet:** Column A (header in A1):

| | A |
|---|---|
| 1 | EmpID |
| 2 | 101 |
| 3 | 102 |
| 4 | 103 |
| 5 | 102 |
| 6 | 104 |
| 7 | 105 |
| 8 | 103 |
| 9 | 102 |

**Formula / Steps:** (pivot clicks: not run here, steps from Microsoft Support "Create a PivotTable to analyze worksheet data")
1. Select A1:A9 > Insert > PivotTable > OK.
2. Drag EmpID to Rows, then drag EmpID to Values (text or ID fields default to Count; numeric IDs may default to Sum, so set it via Value Field Settings > Count).
3. Rows drop-down > Value Filters > Greater Than > 1.
**Alternative:** Helper column B2: `=IF(COUNTIF($A$2:$A$9,A2)>1,"Duplicate","")`, or Home > Conditional Formatting > Highlight Cells Rules > Duplicate Values.
**Result:** pandas reproduction of the pivot (run): 101 = 1, 102 = 3, 103 = 2, 104 = 1, 105 = 1, so after the filter 102 (3 times) and 103 (2 times) remain. The helper formula, run in LibreOffice, marks rows 3, 4, 5, 8 and 9 as "Duplicate" (all rows of 102 and 103).
**Version note:** Works in all Excel versions with pivots; same idea in Google Sheets pivots (from memory, unverified).
**Edge cases:** Numeric IDs default to Sum, which hides duplicates, so switch to Count. "102" typed as text and 102 as a number show as two separate items. Trailing spaces make "Ravi" and "Ravi " look different.
**Likely follow-ups:** 1) *Then how do you remove them?* Data > Remove Duplicates, after checking. 2) *Which is better, pivot or COUNTIF?* Pivot for a quick list, COUNTIF to flag the rows.
**Common mistakes:** Leaving Sum instead of Count; forgetting to refresh; deleting duplicates without checking whether they are genuine repeats (for example, two real payments).

### Q40 ⭐⭐ 🟡 How do you find the distinct (unique) count of employees in a pivot table?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that normal Count counts rows, not people?
**Say this in the interview:** "A normal Count counts rows. For unique employees I add the data to the Data Model when creating the pivot, then set the value field to Distinct Count."
**Explain simply:**
- Distinct count = how many different values, ignoring repeats. An employee with 2 attendance rows counts once.
- The Data Model is Excel's built-in mini-database. The distinct count option only appears when the pivot is built on it.
- Without the Data Model, add a helper column (1 for the first occurrence of an ID, else 0) and Sum it.
**Example:** Attendance rows per department; HR has 3 rows but only 2 people.
**Sample sheet:** A = EmpID, B = Dept:

| | A | B |
|---|---|---|
| 1 | EmpID | Dept |
| 2 | 101 | HR |
| 3 | 101 | HR |
| 4 | 102 | HR |
| 5 | 102 | IT |
| 6 | 103 | IT |
| 7 | 104 | IT |
| 8 | 104 | IT |
| 9 | 105 | Sales |

**Formula / Steps:** (not run here, pivot steps)
1. Insert > PivotTable, tick **Add this data to the Data Model** (Microsoft Support "Create a PivotTable to analyze worksheet data" lists this checkbox in the Windows steps for Excel 2016 to 2024/365).
2. Dept to Rows, EmpID to Values.
3. Click the value > Value Field Settings > Summarize Values By > scroll to **Distinct Count** (steps for this option are from memory, unverified).
**Alternative:** `=SUMPRODUCT(1/COUNTIF(A2:A9,A2:A9))` for the whole list; per department `=SUMPRODUCT((B2:B9="IT")/COUNTIFS(A2:A9,A2:A9,B2:B9,B2:B9))`; in 365 `=COUNTA(UNIQUE(A2:A9))` (not run here).
**Result:** pandas (run): Count vs distinct: HR 3 vs 2, IT 4 vs 3, Sales 1 vs 1, All 8 vs 5. LibreOffice (run): the SUMPRODUCT formulas return 5 overall and 3 for IT.
**Version note:** Data Model distinct count: Windows Excel 2013 and later (from memory, unverified); Mac and Excel for the web may not offer the checkbox (from memory, unverified).
**Edge cases:** Blank cells can be counted as a value in the Data Model; clean the data first. Grand total of a distinct count is not the sum of the rows (an employee in two departments counts in both).
**Likely follow-ups:** 1) *Why not just Count?* It counts rows. 2) *Can I use a Table?* Yes, a Table can also go into the Data Model.
**Common mistakes:** Reporting row count as headcount; summing the per-department distinct counts and expecting the grand total to match.

### Q41 ⭐⭐ 🟡 What is the difference between a pivot chart and a normal chart?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know a pivot chart is tied live to a pivot table?
**Say this in the interview:** "A normal chart plots fixed cells. A pivot chart plots a pivot table, so it changes when I filter, slice, drag fields or refresh."
**Explain simply:**
- Normal chart: you pick cell ranges; add a new row and you must extend the range.
- Pivot chart: its data is the pivot table's summary. Change the pivot (new field in Rows) and the chart redraws.
- A pivot chart can show field buttons so viewers can filter on the chart itself, and slicers filter it too.
- A pivot chart cannot be built from the raw range alone; a pivot table always sits behind it.
**Example:** A monthly headcount column chart for HR: with a pivot chart, adding the slicer "Location" re-draws it for Pune only.
**Formula / Steps:** Select a cell in the pivot > PivotTable Analyze > PivotChart (or Insert > PivotChart) > pick a chart type. (Not run here. Microsoft Support "Create a PivotChart" says PivotCharts add data visualisations to your data and that filters and slicers applied to the PivotTable also filter the chart; its Mac section says only column, line, pie and radar chart types work.)
**Alternative:** A normal chart on a copied-as-values pivot output, if you need full freedom of chart types.
**Version note:** Available in Excel 2016 to 365 (the Microsoft page lists Windows and Mac; the Mac type limits are from that page). Which chart types are unsupported on Windows (XY scatter, bubble, stock) is from memory, unverified.
**Edge cases:** Formatting (for example custom colours) can reset after refresh unless "Preserve cell formatting on update" is kept on.
**Likely follow-ups:** 1) *Can you have a pivot chart without showing the pivot table?* Yes, move the pivot to another sheet. 2) *Scatter chart?* Not from a pivot chart.
**Common mistakes:** Building a normal chart on pivot cells (it can silently turn into a pivot chart when you click inside a pivot, or lose cells when the pivot shrinks).

### Q42 ⭐⭐ 🟡 What happens to a pivot chart when you filter or change the pivot table behind it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand the live link between pivot and chart?
**Say this in the interview:** "They are mirror images. Filter, slice, add a field or refresh the pivot and the chart updates; filter the chart's field buttons and the pivot changes too."
**Explain simply:**
- One data source, two views. Change either and the other follows.
- Microsoft Support "Create a PivotChart": filters and slicers applied to the PivotTable also filter the chart.
- Deleting the pivot table leaves the chart as an ordinary picture of its last values (from memory, unverified).
**Example:** Sales by region: filtering out East removes the East column and drops the total.
**Sample sheet:** Region totals (pivot output):

| Region | Sum of Sales |
|---|---|
| East | 130 |
| North | 220 |
| South | 170 |

**Formula / Steps:** Click a slicer item or use the Region filter drop-down. (Not run here.)
**Alternative:** Check Region filter's Select Multiple Items to hide one region.
**Result:** pandas (run): all regions: East 130, North 220, South 170; after excluding East: North 220, South 170. The chart would show two columns instead of three (chart behaviour not run here).
**Version note:** Same in Excel 2016 to 365.
**Edge cases:** Changing the layout (moving a field from Rows to Columns) changes the chart series. New items from refresh appear in the chart automatically.
**Likely follow-ups:** 1) *Chart axis not updating?* Refresh. 2) *Can the chart show a subset only?* Filter the pivot.
**Common mistakes:** Hiding rows manually instead of filtering; expecting the chart to keep an old item that was filtered out.

### Q43 ⭐⭐ 🟡 How do you turn a pivot table into static values and why might you do that before sharing it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you think about what the recipient will see and be able to break?
**Say this in the interview:** "I copy the pivot and Paste Special as Values. That removes the live link, so the numbers stay fixed and nobody can accidentally refresh or reshuffle them."
**Explain simply:**
- A pivot is live and tied to source data; refreshing it can change numbers.
- Static values are plain numbers: they won't change, and the file can drop the source data.
- Reasons to do it: send a clean report, hide the raw data, avoid refresh errors, or freeze month-end figures.
**Example:** Month-end attrition summary for the CHRO: I paste values so the figures stay as signed off.
**Formula / Steps:** (not run here; from memory, unverified, no fetched Microsoft page covers it)
1. Select the whole pivot (PivotTable Analyze > Select > Entire PivotTable).
2. Ctrl+C.
3. Right-click a cell in a new sheet > Paste Special > Values (or Home > Paste > Values).
**Alternative:** Copy the pivot, paste as picture; or save a PDF; or, with Data Model/OLAP pivots, PivotTable Analyze > OLAP Tools > Convert to Formulas.
**Version note:** Paste Special Values works in every version and in Google Sheets (from memory, unverified).
**Edge cases:** Number formats may paste as general; re-apply them. Grand totals paste as numbers, not formulas.
**Likely follow-ups:** 1) *Keep the pivot too?* Keep a master copy in a separate file. 2) *Can the recipient still drill down?* No.
**Common mistakes:** Pasting values over the pivot itself and losing it; forgetting hidden source sheets still travel with the file unless removed.

### Q44 ⭐⭐ 🟡 How do you stop column widths and formatting from resetting every time you refresh a pivot table?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Practical care about report appearance.
**Say this in the interview:** "In PivotTable Options, Layout and Format tab, I untick Autofit column widths on update and keep Preserve cell formatting on update ticked."
**Explain simply:**
- Autofit makes Excel resize columns after every refresh, undoing your width settings.
- Preserve cell formatting keeps your number formats and fills when you refresh or move fields.
- Microsoft Support "Design the layout and format of a PivotTable": **Autofit column widths on update** fits columns to the widest value; **Preserve cell formatting on update** saves layout and format so they are used each time you perform an operation on the PivotTable.
**Example:** You widen the Department column to 25 characters; after refresh it shrinks. Unticking Autofit stops that.
**Formula / Steps:** (not run here, steps from Microsoft Support)
1. Click inside the pivot.
2. PivotTable Analyze > Options (the PivotTable Options button).
3. Layout & Format tab: clear **Autofit column widths on update**; keep **Preserve cell formatting on update** ticked.
4. OK.
**Alternative:** Format via Value Field Settings > Number Format (stays with the field), and PivotTable Styles for look.
**Version note:** Excel 2016 to 365 (the page lists 2016, 2019, 2021, 2024, 365); not listed for the web version.
**Edge cases:** Long new text can be cut off once autofit is off.
**Likely follow-ups:** 1) *Does it apply to all pivots?* No, per pivot. 2) *Default for new pivots?* File > Options > Data > Edit Default Layout (from memory, unverified).
**Common mistakes:** Formatting with the plain Format Cells and then losing it when Preserve is off; hand-coloring cells instead of using styles.

### Q45 ⭐⭐ 🟡 How do you merge data from two raw sheets before building a pivot table (for example with Power Query or an Excel Table)?
**Asked at:** one candidate report mentions a Mahindra Finance MIS task with a pivot, YoY % and a Power Query merge (single anecdote, unverified); otherwise commonly asked.
**What the interviewer is checking:** Can you combine tables before summarising?
**Say this in the interview:** "I load both sheets as tables into Power Query and use Merge Queries on the common key, such as Employee ID, then expand the columns I need and build the pivot on the result. For a quick job I add a VLOOKUP column."
**Explain simply:**
- Power Query is Excel's data-cleaning tool (Data > Get & Transform); merge is like a lookup that joins two tables on a shared column.
- A left outer join keeps every row of the first table and brings matches from the second.
- Microsoft Support "Merge queries (Power Query)": Home > Merge Queries (inline) or Merge Queries as New; choose tables and matching columns, pick a join kind (inner is the default), then Expand to bring in columns.
**Example:** Employee master (ID, Name, Dept) plus Payroll (ID, Salary): merge to see salary by department.
**Sample sheet:** Sheet Emp: IDs 101 to 104; Sheet Pay: 101, 102, 103, 105.

| EmpID | Name | Dept | Salary |
|---|---|---|---|
| 101 | Asha | HR | 42000 |
| 102 | Ravi | Finance | 55000 |
| 103 | Meena | IT | 68000 |
| 104 | Karan | HR | blank |

**Formula / Steps:** (Power Query not run here, steps from Microsoft Support)
1. Select data > Data > From Table/Range for each sheet.
2. In the editor: Home > Merge Queries > pick Emp and Pay, click EmpID in both, Join Kind = Left Outer > OK.
3. Expand the new column, choose Salary > OK > Home > Close & Load.
4. Insert a PivotTable on the loaded table.
**Alternative:** Helper column `=IFERROR(VLOOKUP(D2,Pay!A$2:B$5,2,FALSE),"")`.
**Result:** pandas left-merge (run): salary column 42000, 55000, 68000, NaN; pivot salary by Dept: Finance 55000, HR 42000, IT 68000. LibreOffice (run): the VLOOKUP column returns 42000, 55000, 68000 and blank for 104.
**Version note:** Microsoft Support "About Power Query in Excel" lists Excel 2016, 2019, 2021, 2024 and 365 on Windows (Get & Transform under the Data tab); no Power Query for Excel 2016/2019 for Mac. The merge page's own applies-to line lists 365, 2024, 2021.
**Edge cases:** Unmatched keys (104, 105): inner join drops them, left join keeps blank. Duplicate keys multiply rows. Number vs text IDs fail to match.
**Likely follow-ups:** 1) *Why Power Query over VLOOKUP?* Repeatable on refresh. 2) *Append vs merge?* Append stacks rows; merge adds columns.
**Common mistakes:** Merging on names instead of IDs; ignoring unmatched rows.

### Q46 ⭐ 🟢 How do you make several pivot tables from one source without increasing the file size much?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Awareness of the pivot cache (the hidden stored copy of the data).
**Say this in the interview:** "I build the extra pivots from the first pivot's cache by copying and pasting the pivot table, or by choosing the existing pivot as the source, so they share one cache and the file doesn't store the data twice."
**Explain simply:**
- Microsoft Support "Create a PivotTable..." says PivotTables work on a snapshot of the data called the cache.
- Each separate cache stores another copy, so size grows; shared cache means one copy and Refresh updates all.
- Sharing details are from memory, unverified (the Microsoft page does not state it).
**Example:** A 2 lakh-row HR file with five pivots on separate caches could be several times larger than with one shared cache.
**Formula / Steps:** (not run here)
1. Select the whole first pivot > Ctrl+C.
2. Click an empty cell elsewhere > Ctrl+V.
3. Drag different fields into the copy.
**Alternative:** Insert > PivotTable > "Use an external data source" and choose the existing connection, or build all from a Table and use slicers connected through the same source.
**Version note:** Excel 2016 to 365 (from memory, unverified).
**Edge cases:** Changing grouping on one shared-cache pivot can affect others (from memory, unverified).
**Likely follow-ups:** 1) *Can slicers connect to both?* Microsoft Support "Use slicers to filter data": slicers connect only to PivotTables that share the same data source. 2) *Refresh?* Refresh All.
**Common mistakes:** Creating each pivot from scratch on a big file; thinking each copy is independent.

### Q47 ⭐ 🟢 How do you copy a pivot table to another sheet and keep it working?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know copy-paste keeps the link but values-paste breaks it?
**Say this in the interview:** "I select the whole pivot, Ctrl+C, and paste on the new sheet. It stays a live pivot. To relocate without duplicating, I use Move PivotTable."
**Explain simply:**
- Normal paste of a pivot creates another live pivot on the same cache.
- Paste Special as Values makes it static (see Q43).
- Move PivotTable shifts the same pivot, not a copy.
**Example:** The attrition pivot is on a data sheet; you want it on a Dashboard sheet.
**Formula / Steps:** (not run here)
1. Copy: PivotTable Analyze > Select > Entire PivotTable > Ctrl+C > click target cell > Ctrl+V (copy and paste is from memory, unverified).
2. Move: PivotTable Analyze > Move PivotTable > New Worksheet or Existing Worksheet > pick the cell (Microsoft Support "Move a PivotTable", Excel 2016 to 365).
**Alternative:** Cut and paste (Ctrl+X) the whole pivot to move it.
**Version note:** Excel 2016 to 365.
**Edge cases:** The destination area must be empty; a pivot cannot overlap another pivot.
**Likely follow-ups:** 1) *Copy to another workbook?* It carries its own data copy; refresh may need the source. 2) *Linked slicers?* Reconnect via Report Connections.
**Common mistakes:** Selecting only part of the pivot; pasting over another pivot.

### Q48 ⭐ 🟢 How do you hide or show the field list and the +/- expand buttons in a pivot table?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Report-polish knowledge.
**Say this in the interview:** "The Field List shows when I click inside the pivot; if it is closed I reopen it from PivotTable Analyze. The +/- buttons toggle in the same tab under Show."
**Explain simply:**
- Field List = the side pane where you drag fields. Microsoft Support "Use the Field List to arrange fields in a PivotTable": it should appear when you click anywhere in the PivotTable; if not, go to PivotTable Analyze > Field List.
- +/- buttons expand or collapse groups, such as months under a year. Microsoft's layout page describes them appearing in compact form but gives no Windows toggle.
- Toggle for +/- buttons is from memory, unverified.
**Example:** Before sending a report, hide the buttons and field list so it looks clean.
**Formula / Steps:** (not run here)
1. Show/hide Field List: click in the pivot > PivotTable Analyze > Field List (toggle). The close X on the pane also hides it.
2. +/- buttons: PivotTable Analyze > Show group > +/- Buttons (from memory, unverified).
**Alternative:** Right-click a pivot cell > Show Field List / Hide Field List (from memory, unverified).
**Version note:** Excel 2016 to 365 (the Field List page lists those).
**Edge cases:** The pane only shows while a pivot cell is selected.
**Likely follow-ups:** 1) *Collapse all years?* Right-click > Expand/Collapse > Collapse Entire Field.
**Common mistakes:** Thinking the pivot is gone when the pane is hidden.

### Q49 ⭐ 🟢 How do you add a custom sort order (for example Jan to Dec instead of alphabetical) to pivot items?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you control item order, not accept alphabetical?
**Say this in the interview:** "Month names written as text sort A to Z, so April comes first. Excel has built-in month and weekday lists it uses automatically; for my own order, I create a custom list or drag items manually."
**Explain simply:**
- Microsoft Support "Sort data in a PivotTable or PivotChart": Excel includes day-of-week and month-of-year lists, and you can create your own custom list for sorting; First key sort order is in the Sort dialog and only available when "Sort automatically every time the report is updated" is unchecked.
- Manual sort: choose Manual and drag items.
- The page warns a custom list sort order is not retained when you refresh.
**Example:** Hires per month; text months show Apr, Feb, Jan, Mar.
**Sample sheet:**

| Month | Hires |
|---|---|
| Apr | 5 |
| Jan | 3 |
| Mar | 4 |
| Feb | 2 |
| Jan | 4 |
| Mar | 6 |

**Formula / Steps:** (not run here, steps from Microsoft Support / memory)
1. File > Options > Advanced > General > Edit Custom Lists > type the order > Add (from memory, unverified).
2. In the pivot, sort the field A to Z so the list order applies, or Row Labels drop-down > More Sort Options > First key sort order.
**Alternative:** Right-click an item > Move > Move Up/Down/To Beginning; or use real dates grouped by month (Q13).
**Result:** pandas (run): default text sort gives Apr 5, Feb 2, Jan 7, Mar 10; with an ordered list Jan 7, Feb 2, Mar 10, Apr 5.
**Version note:** Excel 2016 to 365 (page applies-to list).
**Edge cases:** Custom lists apply workbook-wide on that computer, not inside the file (from memory, unverified).
**Likely follow-ups:** 1) *Fiscal year Apr to Mar?* Make a custom list starting April.
**Common mistakes:** Typing month names in the source as text and expecting date order; forgetting auto-sort overrides manual sort.

### Q50 ⭐ 🟢 How do you apply a pivot table style or banded rows for a cleaner report?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Presentation habits.
**Say this in the interview:** "On the Design tab I pick a PivotTable Style from the gallery and tick Banded Rows for alternate shading."
**Explain simply:**
- Style = a ready-made colour scheme; banded rows = alternating light and dark rows for readability.
- Microsoft Support "Change the style of your PivotTable" and "Design the layout and format of a PivotTable": Design > PivotTable Styles; Design > PivotTable Style Options > Banded Rows or Banded Columns; choose Clear at the bottom of the gallery to remove a style.
**Example:** A 30-row department report is easier to read with banding.
**Formula / Steps:** (not run here, steps from Microsoft Support)
1. Click inside the pivot.
2. Design > PivotTable Styles gallery > choose a style.
3. Design > PivotTable Style Options > tick Banded Rows.
**Alternative:** Create your own with New PivotTable Style at the bottom of the gallery.
**Version note:** Excel 2016 to 365; Excel for the web cannot change the style (Microsoft Support).
**Edge cases:** Styles survive refresh; hand-coloured cells may not (see Q44).
**Likely follow-ups:** 1) *Compact vs tabular?* Design > Report Layout.
**Common mistakes:** Colouring cells by hand; too many colours.

### Q51 ⭐ 🟡 How do you make a pivot table update automatically when the file opens?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you automate refreshing rather than trust memory?
**Say this in the interview:** "In PivotTable Options, Data tab, I tick Refresh data when opening the file. Pivots don't update live while I'm working, only on refresh."
**Explain simply:**
- Microsoft Support "Refresh PivotTable data": select the PivotTable, open PivotTable Options, Data tab, check "Refresh data when opening the file". Refresh is Alt+F5; Refresh All covers every PivotTable.
- Useful when the source is a daily-updated sheet or external data.
**Example:** A morning attendance report: open the file and the pivot is already current.
**Formula / Steps:** (not run here, steps from Microsoft Support)
1. Click in the pivot.
2. PivotTable Analyze > Options > Data tab.
3. Tick Refresh data when opening the file > OK.
**Alternative:** VBA `Workbook_Open` with `ActiveWorkbook.RefreshAll` (from memory, unverified).
**Version note:** The page applies to Excel 2016 through 365.
**Edge cases:** Protected View or disabled external connections may block refresh; refresh also resets column width if autofit is on (Q44).
**Likely follow-ups:** 1) *Automatically as data changes?* Not in classic Excel; use a macro.
**Common mistakes:** Assuming pivots refresh like formulas.

### Q52 ⭐ 🟡 Why is an Excel Table or a dynamic named range a better pivot source than a fixed range?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you prevent the "new rows missing" problem at the source?
**Say this in the interview:** "A fixed range such as A1:C7 stops at row 7, so new rows are ignored. A Table grows automatically, so a refresh picks them up."
**Explain simply:**
- Excel Table = a range turned into a smart object (Ctrl+T) that expands as you add rows.
- Microsoft Support "Create a PivotTable...": rows added to a table are included automatically on refresh; a table is an ideal source.
- Dynamic named range = a name defined by a formula whose size follows the data.
**Example:** Sales sheet with 7 rows; the pivot was built on the first 6.
**Sample sheet:** A = Region, B = Amt (rows 2 to 8): N 100, S 80, E 60, N 120, S 90, E 70, N 50.
**Formula / Steps:** Ctrl+T on the data > Insert > PivotTable (source shows as the table name).
**Alternative:** Name Manager name `=OFFSET($A$1,0,0,COUNTA($A:$A),2)` as the source (not directly usable as a Data Model source; from memory, unverified).
**Result:** Counting rows with the formula (LibreOffice, run): `=COUNTA(A:A)-1` returns 7; the OFFSET height returns 7; the sum of Amt through the last row returns 570. pandas pivot (run): fixed first 6 rows give E 130, N 220, S 170, total 520; all 7 rows give E 130, N 270, S 170, total 570.
**Version note:** Tables work in every modern Excel version.
**Edge cases:** Blank rows break COUNTA-based ranges. A Data Model pivot cannot change source (Microsoft Support "Change the source data for a PivotTable").
**Likely follow-ups:** 1) *Do you still refresh?* Yes. 2) *Change source manually?* PivotTable Analyze > Change Data Source.
**Common mistakes:** Selecting whole columns including blanks; forgetting to refresh.

### Q53 ⭐ 🟡 What is the pivot cache, and why do two pivot tables sometimes share it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Under-the-hood understanding.
**Say this in the interview:** "The pivot cache is a hidden copy of the source data stored inside the file. Pivots built from the same source can share one cache, which saves space and refreshes together."
**Explain simply:**
- Microsoft Support "Create a PivotTable...": PivotTables work on a snapshot of your data, called the cache. That is why a pivot doesn't change until you refresh.
- Which pivots share a cache is from memory, unverified: copy-pasting a pivot, or choosing an existing pivot as source, shares it; separate creation can create another.
- Shared cache means Refresh on one updates all; grouping changes can affect siblings.
**Example:** Two pivots, attrition by department and by month, from the same HR sheet: one cache, half the file size.
**Formula / Steps:** (not run here) Check by refreshing one and seeing the other update, or by the VBA `PivotCaches` count (from memory, unverified).
**Alternative:** Slicers can connect only to pivots on the same data source (Microsoft Support "Use slicers to filter data").
**Version note:** Concept in every version.
**Edge cases:** Cache stays after deleting the source sheet, so refresh fails.
**Likely follow-ups:** 1) *Delete saved data?* PivotTable Options > Data > uncheck Save source data with file (from memory, unverified).
**Common mistakes:** Believing the pivot reads the source live.

### Q54 ⭐ 🟡 What is GETPIVOTDATA, and why does Excel insert it when you click a pivot cell in a formula?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you recognise the formula Excel writes automatically?
**Say this in the interview:** "GETPIVOTDATA reads a value from a pivot by field and item names, not position. Excel inserts it when I click a pivot cell while typing a formula, so the link keeps working if the pivot layout changes."
**Explain simply:**
- Syntax (Microsoft Support "GETPIVOTDATA function"): `GETPIVOTDATA(data_field, pivot_table, [field1, item1], ...)`.
- `pivot_table` is any cell in the pivot; field/item pairs identify the number.
- If the item is hidden or doesn't exist, it returns #REF!.
**Example:** Microsoft's own example: `=GETPIVOTDATA("Sales", $A$3, "Month", "Mar")` returns March sales.
**Sample sheet:** Pivot at A3 (sum of Sales by Month):

| | A | B |
|---|---|---|
| 3 | Month | Sum of Sales |
| 4 | Feb | 120 |
| 5 | Jan | 180 |
| 6 | Mar | 200 |

**Formula / Steps:** `=GETPIVOTDATA("Sales",$A$3,"Month","Mar")`
**Alternative:** `=SUMIFS(C2:C7,A2:A7,"Mar")` on the raw data, or type `=B6`.
**Result:** Not run here (needs a real pivot). pandas pivot (run): Feb 120, Jan 180, Mar 200. The formula should return 200. SUMIFS on the raw data, run in LibreOffice, returns 200.
**Version note:** Excel 2016 to 365 (the page applies-to).
**Edge cases:** #REF! if the pivot is filtered so that item isn't visible, or the combination has no data (Microsoft Support).
**Likely follow-ups:** 1) *Why not just B6?* It breaks if sorting or adding rows moves cells. 2) *How to stop it?* Q55.
**Common mistakes:** Calling it an error; copying it across and not changing item names.

### Q55 ⭐ 🟡 How do you turn off the automatic GETPIVOTDATA formula?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the setting that controls it?
**Say this in the interview:** "Click any cell in a pivot, PivotTable Analyze > PivotTable Options dropdown > untick Generate GetPivotData. Then clicking pivot cells gives normal cell references."
**Explain simply:**
- Microsoft Support "GETPIVOTDATA function": select any cell in the PivotTable, go to PivotTable Analyze, then the PivotTable > Options dropdown, and clear **Generate GetPivotData**.
- The setting is global for the application, not per pivot (from memory, unverified).
- You can also just type the cell address instead of clicking.
**Example:** You want `=B6/B$9` for a share of total; with it off, clicking gives plain references.
**Formula / Steps:** (not run here, steps from Microsoft Support)
1. Click any cell in the pivot.
2. PivotTable Analyze > PivotTable (Options dropdown arrow).
3. Untick Generate GetPivotData.
**Alternative:** Type the reference manually, or select cells with the keyboard.
**Version note:** Excel 2016 to 365; Mac click path differs (from memory, unverified).
**Edge cases:** Already inserted GETPIVOTDATA formulas stay; only new ones change.
**Likely follow-ups:** 1) *Should you turn it off?* Keep it for reports; turn off for quick maths.
**Common mistakes:** Looking for it in File > Options.

### Q56 ⭐ 🟡 Why can the pivot show old items that no longer exist in the data, and how do you clear them?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the cache keeps deleted items?
**Say this in the interview:** "The cache remembers items even after they are deleted from the source. I set Retain items deleted from the data source to None in PivotTable Options, then refresh."
**Explain simply:**
- Old items show in filters and slicers although no rows remain.
- Exceljet "pivot table remove deleted items" (Excel 2019 and 365): right-click pivot > PivotTable Options > Data tab > Retain items deleted from the data source = None > OK > Refresh.
- Older Excel lacked this setting and needed a macro (same Exceljet page).
- The Microsoft page on this topic returned an error when fetched, so Microsoft documentation is not cited here.
**Example:** Department "Temp" was removed from the HR sheet but still appears in the filter.
**Sample sheet:** Source rows: HR 3, IT 4, Sales 2 (Temp row deleted).
**Formula / Steps:** (not run here, steps from Exceljet)
1. Right-click the pivot > PivotTable Options.
2. Data tab > Retain items deleted from the data source > None.
3. OK, then Refresh.
**Alternative:** Recreate the pivot; or in older Excel change the source and refresh twice.
**Result:** pandas (run): data after deleting Temp: HR 3, IT 4, Sales 2. With the stale category list kept (what the cache does), Temp shows with 0. The pivot behaviour itself was not run here.
**Version note:** Setting available in Excel 2019 and 365 per Exceljet; 2016 and 2021 presence is from memory, unverified.
**Edge cases:** Applies to every pivot sharing that cache; slicers keep ghosts until refreshed.
**Likely follow-ups:** 1) *Default for new pivots?* File > Options > Data > Edit Default Layout (Exceljet).
**Common mistakes:** Refreshing without changing the setting; forgetting the deleted rows are still in the source.

### Q57 ⭐ 🟡 What does "Retain items deleted from the data source" do in PivotTable Options?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know why "ghost" items stay in a pivot's filter lists, and how to control it?
**Say this in the interview:** "It decides how many old items the pivot remembers after they disappear from the source. The default is Automatic, so deleted items can still show in drop-downs. I set it to None and refresh to clear them."
**Explain simply:**
- A pivot table (a drag-and-drop summary table) keeps a hidden copy of your data called the pivot cache (its memory of the data and the items it has seen).
- With the setting on Automatic, an item such as department "Legal" can stay in the filter drop-down after every Legal row is deleted from the source, even though it has no data.
- Setting it to None and then refreshing removes those ghost items.
- It does not change any totals; it only affects which item names are remembered.
**Example:** The Legal team was merged into HR and its 3 rows were deleted from the payroll sheet. The pivot's Department filter still lists Legal until you fix the setting.
**Sample sheet:** Source after the deletion (A = Dept, B = Salary in thousands):

| | A | B |
|---|---|---|
| 1 | Dept | Salary |
| 2 | HR | 40 |
| 3 | HR | 50 |
| 4 | IT | 70 |
| 5 | Admin | 30 |

**Formula / Steps:** (not run here; steps from the Exceljet page "pivot table remove deleted items", which I fetched; Microsoft Support was not fetched for this setting)
1. Right-click the pivot > PivotTable Options > Data tab.
2. Under "Retain items deleted from the data source", choose **None**.
3. OK, then right-click the pivot > Refresh.
**Alternative:** Create a new pivot from the same source (a fresh cache has no ghost items), or use a macro in older Excel (per Exceljet).
**Result:** pandas (run) of the source gives Admin 30, HR 90, IT 70. Items still remembered by the old cache under Automatic: Admin, HR, IT, Legal. This is a simulation of the behaviour, not a pivot run here.
**Version note:** Exceljet states older Excel versions do not have the setting (from Exceljet, not Microsoft). I could not confirm the exact versions from Microsoft Support, so the version cut-off is unverified.
**Edge cases:** The option is greyed out for pivots built on the Data Model (from a Microsoft forum thread seen in search results, unverified). Changing it affects only that pivot.
**Likely follow-ups:** 1) *Where do ghost items show?* In filter and slicer lists. 2) *Do totals change?* No.
**Common mistakes:** Changing the setting but forgetting to refresh; assuming ghost items mean the source still has the data.

### Q58 ⭐ 🟡 Why does a calculated field give an unexpected result in the Grand Total row?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know a calculated field adds up the underlying columns first and then applies the formula, rather than adding up the row results?
**Say this in the interview:** "A calculated field is a formula built from other fields. In the totals, Excel sums each field first and then applies my formula. So a ratio's Grand Total is total divided by total, not the sum or average of the rows' ratios."
**Explain simply:**
- Calculated field = a custom column you create inside the pivot using its other fields, for example Absent / Days.
- For each department Excel does sum(Absent) / sum(Days). The Grand Total does sum of all Absent / sum of all Days.
- That is usually the correct weighted figure. It looks "wrong" only if you expected the rows' percentages to add or average to the total.
- Behaviour described from memory; I could not fetch Microsoft's calculated-field page (404), so it is unverified.
**Example:** Absence rate by department.
**Sample sheet:** (A = Dept, B = Absent days, C = Working days)

| | A | B | C |
|---|---|---|---|
| 2 | HR | 2 | 20 |
| 3 | HR | 6 | 10 |
| 4 | IT | 1 | 20 |
| 5 | IT | 9 | 10 |
| 6 | Sales | 3 | 20 |
| 7 | Sales | 3 | 10 |

**Formula / Steps:** (not run here; pivot clicks)
1. Select the pivot > PivotTable Analyze > Fields, Items & Sets > Calculated Field.
2. Name: AbsRate; Formula: `=Absent / Days`.
3. Add AbsRate to Values and format as %.
**Alternative:** If you want the average of row rates, add a helper column in the source (`=B2/C2`) and summarise it with Average.
**Result:** pandas (run): HR 8/30 = 26.7%, IT 10/30 = 33.3%, Sales 6/30 = 20.0%. Grand Total = 24/90 = 26.7%. Adding the three rates gives 80.0% and averaging the six row rates gives 35.0%, neither of which the pivot shows.
**Version note:** Calculated fields exist in all desktop Excel versions with pivots (from memory, unverified); not available on a Data Model pivot, where you write a DAX measure instead (from memory, unverified).
**Edge cases:** Division by zero shows #DIV/0!. A calculated field cannot use cell references or worksheet functions that look up ranges (from memory).
**Likely follow-ups:** 1) *How to avoid this?* Use a source helper column. 2) *Calculated field vs item?* Field works on columns, item on items inside one field.
**Common mistakes:** Averaging percentages instead of weighting them; expecting the Grand Total to equal the sum of the rate column.

### Q59 ⭐ 🟡 How do you show a running total in a pivot table?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you use Show Values As without writing formulas?
**Say this in the interview:** "I add the value field, open Value Field Settings, go to Show Values As and pick Running Total In, with Month as the base field."
**Explain simply:**
- A running total (cumulative total) adds each period to everything before it: Jan, Jan+Feb, Jan+Feb+Mar.
- Show Values As is a setting that re-displays the same numbers in a different way (Microsoft Support, "Show different calculations in PivotTable value fields").
- Base field = the field Excel moves along, here Month. Order follows the pivot's sort order, so months must be in calendar order.
**Example:** Cumulative hires through the year against an annual plan.
**Sample sheet:** (A = Month, B = Hires, C = running total check formula)

| | A | B | C |
|---|---|---|---|
| 2 | Jan | 12 | 12 |
| 3 | Feb | 9 | 21 |
| 4 | Mar | 15 | 36 |
| 5 | Apr | 7 | 43 |
| 6 | May | 11 | 54 |

**Formula / Steps:** (not run here; steps from Microsoft Support)
1. Drag Month to Rows and Hires to Values.
2. Click a Hires value > Value Field Settings > Show Values As tab.
3. Show Values As: **Running Total In**; Base field: Month > OK.
**Alternative:** Outside the pivot, `=SUM($B$2:B2)` filled down.
**Result:** pandas cumsum (run): 12, 21, 36, 43, 54. The formula `=SUM($B$2:B2)` run in LibreOffice returns 12, 21, 36, 43, 54.
**Version note:** Microsoft's page lists Excel 2016, 2019, 2021, 2024 and Microsoft 365. Google Sheets: from memory, unverified.
**Edge cases:** Months sorted alphabetically give a wrong running order (use a custom list or real dates). Filtering a month out changes the cumulative values.
**Likely follow-ups:** 1) *Percent of the year?* Choose % Running Total In. 2) *Show actual and running side by side?* Add the field twice.
**Common mistakes:** Wrong base field; unsorted months; reading the running column as monthly values.

### Q60 ⭐ 🟡 How do you rank items in a pivot table using Show Values As?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the built-in Rank options and which direction gives rank 1?
**Say this in the interview:** "Value Field Settings, Show Values As, Rank Largest to Smallest, with the item field as the base. The biggest value gets rank 1."
**Explain simply:**
- Rank Largest to Smallest lists the largest item as 1 and gives smaller values higher numbers; Rank Smallest to Largest does the opposite (Microsoft Support, "Show different calculations in PivotTable value fields").
- Add the value field twice if you want the amount and the rank next to each other.
- Rank is calculated against the base field, so keep that field in Rows.
**Example:** Rank recruiters by offers closed.
**Sample sheet:** (A = Rep, B = Sales, C = check formula)

| | A | B | C |
|---|---|---|---|
| 2 | Asha | 420 | 4 |
| 3 | Bala | 515 | 2 |
| 4 | Chitra | 380 | 5 |
| 5 | Dev | 610 | 1 |
| 6 | Esha | 455 | 3 |

**Formula / Steps:** (not run here; steps from Microsoft Support)
1. Rep to Rows, Sales to Values twice.
2. Click the second Sales > Value Field Settings > Show Values As > **Rank Largest to Smallest**, Base field: Rep.
**Alternative:** `=RANK.EQ(B2,$B$2:$B$6,0)` (0 = largest first); Excel 2010 and later.
**Result:** pandas rank (run): Asha 4, Bala 2, Chitra 5, Dev 1, Esha 3. `RANK.EQ` run in LibreOffice returns the same 4, 2, 5, 1, 3.
**Version note:** Rank options listed for Excel 2016 to 365 on Microsoft's page. RANK.EQ: from memory, unverified.
**Edge cases:** Ties: RANK.EQ gives equal ranks and skips the next number (4, 4, 6); the pivot is believed to behave similarly (from memory, unverified). Grand Total has no rank.
**Likely follow-ups:** 1) *Top 5 only?* Value Filters > Top 10. 2) *Rank within a group?* Use the inner field as base.
**Common mistakes:** Ranking with the wrong direction; sorting the pivot and thinking the order is the rank.

### Q61 ⭐ 🟡 How do you group text items in a pivot table, for example combine several cities into one region?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you create groups without altering the source data?
**Say this in the interview:** "In Rows I Ctrl+click the cities, right-click and choose Group, then rename the group. If the grouping needs to be permanent I add a Region column to the source with a lookup."
**Explain simply:**
- Grouping combines several items under one heading, such as Mumbai and Pune under West.
- Microsoft Support ("Group or ungroup data in a PivotTable") says: hold Ctrl, click two or more items, right-click and choose Group. Rename through Analyze > Field Settings > Custom Name.
- The grouping lives in the pivot only; the source sheet is unchanged.
**Example:** Hiring by city rolled up into West and South.
**Sample sheet:** (A = City, B = Hires, C = Region lookup)

| | A | B | C |
|---|---|---|---|
| 2 | Mumbai | 10 | West |
| 3 | Pune | 6 | West |
| 4 | Chennai | 8 | South |
| 5 | Bengaluru | 12 | South |
| 6 | Hyderabad | 9 | South |
| 7 | Mumbai | 4 | West |
| 8 | Chennai | 5 | South |

**Formula / Steps:** (not run here; steps from Microsoft Support)
1. City in Rows. Ctrl+click Mumbai and Pune > right-click > Group.
2. Repeat for the southern cities; rename Group1 to West and Group2 to South.
**Alternative:** Helper column C2 `=VLOOKUP(A2,$E$2:$F$6,2,FALSE)` using a city-to-region table in E:F, then put Region in Rows.
**Result:** pandas (run): South 34, West 20. City totals: Bengaluru 12, Chennai 13, Hyderabad 9, Mumbai 14, Pune 6. VLOOKUP, run in LibreOffice, returns West, West, South, South, South, West, South.
**Version note:** Microsoft's grouping page covers Excel 2016, 2019, 2021, 2024 and 365.
**Edge cases:** New cities added later do not join a group automatically and appear separately. A city that is not selected stays outside every group.
**Likely follow-ups:** 1) *How to ungroup?* Right-click > Ungroup. 2) *Why a helper column instead?* It survives rebuilds and handles new cities.
**Common mistakes:** Forgetting to rename "Group1"; grouping manually and missing new items.

### Q62 ⭐ 🟡 How do you apply conditional formatting to a pivot table so it follows the data when it refreshes?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the "apply rule to" scope choices?
**Say this in the interview:** "I select a value cell, add the rule, and then use the small Formatting options button to apply it to all cells showing that value field, so it follows the field as the pivot changes."
**Explain simply:**
- Conditional formatting colours cells based on rules (for example, red if attrition is above 15%).
- Microsoft Support ("Use conditional formatting to highlight information in Excel") says the default scope in the Values area is by selection. You can instead choose all cells showing a value label, or the version "for" a row label that excludes subtotals and the Grand Total.
- It says the format is kept when you filter, hide or collapse levels or move a field, as long as the underlying fields are not removed.
- The page does not say what happens when source numbers change, so I treat that as expected behaviour of a refresh (unverified).
**Example:** Highlight departments with attrition above 15%.
**Sample sheet:** (A = Dept, B = Attrition %)

| | A | B |
|---|---|---|
| 2 | HR | 8 |
| 3 | IT | 18 |
| 4 | Sales | 22 |
| 5 | Ops | 11 |

**Formula / Steps:** (not run here; steps from Microsoft Support)
1. Select a value cell in the pivot > Home > Conditional Formatting > Highlight Cells Rules > Greater Than > 15.
2. Click the Formatting Options button that appears beside the pivot and choose **All cells showing "Attrition %" values** (or the "for Dept" variant to skip totals).
**Alternative:** Use Data Bars or Color Scales from the same menu.
**Result:** pandas (run) of the rule: IT (18) and Sales (22) flag as True; HR and Ops do not. Not an actual Excel formatting run.
**Version note:** Scoping options per Microsoft's page for current Excel on Windows; the Mac steps differ (not verified).
**Edge cases:** Formatting by selection can miss new rows; Grand Total may be formatted unintentionally.
**Likely follow-ups:** 1) *Does it survive refresh?* Yes if the field stays in the pivot and the scope is by field. 2) *Why exclude totals?* Totals are much larger than rows.
**Common mistakes:** Formatting by plain selection, then adding a department and seeing it unformatted.

### Q63 ⭐ 🟡 How do you build a simple dashboard from pivot tables, pivot charts and slicers on one sheet?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you connect several pivots to common slicers and arrange a clean one-page view?
**Say this in the interview:** "I make one pivot per question, a pivot chart from each, put the charts on a Dashboard sheet, add slicers and use Report Connections so one click filters everything."
**Explain simply:**
- A pivot chart is a chart tied to a pivot (it changes when the pivot changes).
- A slicer is a clickable filter button box.
- Microsoft Support ("Use slicers to filter data") says a slicer can only be connected to pivots sharing the same data source.
- Keep one data source (ideally an Excel Table) and build all pivots from it.
**Example:** HR dashboard: leavers by department, leavers by month, with Location and Year slicers.
**Sample sheet:** Source rows (A = Dept, B = Month, C = Leavers):

| | A | B | C |
|---|---|---|---|
| 2 | HR | Jan | 1 |
| 3 | HR | Feb | 2 |
| 4 | IT | Jan | 3 |
| 5 | IT | Feb | 2 |
| 6 | Sales | Jan | 4 |
| 7 | Sales | Feb | 5 |

**Formula / Steps:** (not run here; steps from Microsoft Support)
1. Format the source as a Table; Insert > PivotTable for each view.
2. Select a pivot > PivotTable Analyze > PivotChart.
3. Insert > Slicer on Dept; then select the slicer > Report Connections (Slicer tab, or Slicer Settings in newer Windows builds) and tick all pivots.
4. Move charts and slicers onto one sheet, hide gridlines, add titles.
**Alternative:** A timeline for dates, or Power BI for a fuller dashboard.
**Result:** pandas (run) of the pivot behind the charts: HR 3, IT 5, Sales 9, total 17; Jan 8, Feb 9.
**Version note:** Microsoft's slicer page covers Excel 365, 2024 and 2021; the Excel 2016 UI labels differ (Design tab rather than Slicer tab).
**Edge cases:** Pivots from different sources cannot share a slicer. Charts need a refresh after data changes.
**Likely follow-ups:** 1) *Refresh?* Data > Refresh All. 2) *Why a Table?* The range grows automatically.
**Common mistakes:** Separate sources for each pivot; too many charts; forgetting to connect slicers.

### Q64 ⭐ 🟡 Your pivot shows #REF! after you renamed the source sheet. What happened and how do you fix it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you diagnose a broken source or broken formula?
**Say this in the interview:** "First I would check what shows #REF!. Renaming a sheet normally does not break the pivot source, so it is usually a deleted sheet or a GETPIVOTDATA formula pointing at something that is no longer visible. I would reset the source via Change Data Source."
**Explain simply:**
- Premise check: renaming an in-workbook sheet normally updates the pivot's source automatically (from memory, unverified). The cases I know that really break it are a deleted source sheet, or a source in another workbook that was renamed or moved.
- Microsoft Support ("GETPIVOTDATA function") says that function returns #REF! if the pivot_table argument does not reference a pivot, or if the field or item is not visible in the pivot (for example filtered out).
- So the #REF! could be in cells outside the pivot that use GETPIVOTDATA.
**Example:** A dashboard cell shows #REF! after someone filtered Legal out of the pivot it reads.
**Formula / Steps:** (not run here)
1. Click the pivot > PivotTable Analyze > Change Data Source and re-select the range or Table.
2. For GETPIVOTDATA cells, make sure the item is visible, or clear the filter.
3. Turn off auto-generation if you prefer normal cell references: PivotTable Analyze > Options dropdown > untick Generate GetPivotData (Microsoft Support).
**Alternative:** Use a named Table as source so the reference follows renames.
**Result:** Not run here; no reproducible computed value.
**Version note:** Applies to all current desktop Excel versions (Microsoft's GETPIVOTDATA page).
**Edge cases:** External-workbook sources need the file path updated.
**Likely follow-ups:** 1) *Prevent it?* Use Tables. 2) *Source deleted?* Rebuild the pivot from restored data.
**Common mistakes:** Assuming rename is the cause without checking; rebuilding the whole pivot unnecessarily.

### Q65 ⭐ 🟡 What is the difference between Refresh and Refresh All, and what happens to pivots linked to external data?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you refresh the right scope and know that external sources need a connection?
**Say this in the interview:** "Refresh updates the selected pivot; Refresh All updates every pivot and connection in the workbook. For external data, a refresh re-runs the query against the source."
**Explain simply:**
- Microsoft Support ("Refresh PivotTable data"): Refresh updates the selected pivot (Alt+F5 or right-click); Refresh All, from the Refresh arrow, updates every pivot in the workbook.
- External sources such as SQL Server, Oracle, Access, Analysis Services and data feeds can be refreshed from the same command.
- Refresh Status shows progress and Cancel Refresh stops a slow one.
- "Refresh data when opening the file" is in PivotTable Options > Data.
**Example:** The HRMS export refreshes nightly; the pivot reads the connected table on opening.
**Formula / Steps:** (not run here; steps from Microsoft Support)
1. One pivot: right-click > Refresh.
2. All: PivotTable Analyze > Refresh arrow > Refresh All (or Data > Refresh All).
**Alternative:** Refresh on open for shared reports.
**Result:** Not run here.
**Version note:** Microsoft's page covers Excel 2016 to 365; its Auto Refresh feature was described as for Microsoft 365 Insiders at the time of the fetch.
**Edge cases:** A pivot on external data needs credentials and network access. If two pivots share a cache, one refresh may update both (from memory).
**Likely follow-ups:** 1) *Why still stale?* Check source range. 2) *Auto-refresh?* On open.
**Common mistakes:** Refreshing one pivot while another dashboard pivot stays old.

### Q66 ⭐ 🟡 What is the difference between a pivot table built on a normal range and one built from the Data Model?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know when you need relationships between tables?
**Say this in the interview:** "A normal-range pivot uses one flat table. A Data Model pivot can use several related tables, so I can pivot payroll by department without merging them first."
**Explain simply:**
- The Data Model is Excel's built-in mini-database that holds tables and the relationships (links by a common ID column) between them.
- Microsoft Support ("Use multiple tables to create a PivotTable in Excel") says to add each table to the Data Model, link the tables by matching fields, and build the pivot from "Tables in Workbook Data Model".
- The same page says Data Models are not supported on Excel for Mac.
- Data Model pivots also allow distinct counts and DAX measures (from memory).
**Example:** An Employee table (EmpID, Dept) and a Payroll table (EmpID, Month, Pay).
**Sample sheet:** Employee table: A = EmpID, B = Dept. Payroll table: D = EmpID, E = Month, F = Pay.

| | A | B | D | E | F |
|---|---|---|---|---|---|
| 2 | 1 | HR | 1 | Jan | 50 |
| 3 | 2 | IT | 1 | Feb | 50 |
| 4 | 3 | IT | 2 | Jan | 70 |
| 5 | 4 | Sales | 3 | Jan | 60 |
| 6 | | | 4 | Jan | 40 |
| 7 | | | 4 | Feb | 40 |

**Formula / Steps:** (not run here; steps from Microsoft Support)
1. Make each range a Table (Ctrl+T).
2. Insert > PivotTable > From Data Model, or tick Add this data to the Data Model.
3. Data > Relationships > New: EmpID to EmpID.
4. Dept from Employee to Rows; Pay from Payroll to Values.
**Alternative:** Power Query merge or XLOOKUP into one flat table first.
**Result:** pandas merge then group (run, simulates the pivot): HR pay 100, IT 130, Sales 80; distinct people HR 1, IT 2, Sales 1.
**Version note:** Microsoft's page lists Excel 2016, 2019, 2021, 2024 and 365 (not Mac).
**Edge cases:** Missing relationships give repeated totals. Duplicate IDs in the lookup table break the relationship.
**Likely follow-ups:** 1) *One-to-many?* The lookup table must have unique IDs. 2) *Mac?* Not supported.
**Common mistakes:** Not creating the relationship; using text IDs in one table and numbers in the other.

### Q67 ⭐ 🔴 You are given 2,00,000 rows of HR data and the pivot table is very slow. What would you do?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Practical performance thinking, not panic.
**Say this in the interview:** "First I check that the file is not bloated: remove unused columns, use one shared pivot cache, and avoid auto-refresh. If it is still slow I load the data through Power Query into the Data Model, or move the heavy aggregation to SQL or Power BI."
**Explain simply:**
- 2,00,000 rows (200,000) fits within Excel's limit of 1,048,576 rows per sheet (Microsoft Support, "Excel specifications and limits"), so size alone is not the problem; wide files and many pivots are.
- Cut columns you do not need before building the pivot.
- Build further pivots from an existing one (they share a cache), which avoids storing the data several times.
- Load to the Data Model with Power Query; Microsoft says the tools handle "up to millions of rows" (Support, "Learn to use Power Query and Power Pivot in Excel").
- Pre-aggregate outside Excel if you only need monthly totals.
**Example:** Attendance for 8,000 employees over 25 days equals 2,00,000 rows; you need days present by department.
**Sample sheet:** Not meaningful (scale question).
**Formula / Steps:** (not run here)
1. Remove unused columns; convert to a Table.
2. Power Query > Data > Get Data > load as Connection Only/Data Model.
3. PivotTable from the Data Model; turn off "Refresh on open" if not needed.
**Alternative:** Pre-summarise with SQL or pandas.
**Result:** pandas (run) on 200,000 random rows groups by Dept and Location in about 0.06 seconds, so heavy aggregation is cheap in a proper engine. Timing is illustrative of this machine, not Excel.
**Version note:** Power Query is in Excel 2016 and later on Windows; Data Model features per Microsoft's learn page (Windows). 32-bit Excel Data Models are limited to about 500 to 700 MB (Microsoft Support, specifications page).
**Edge cases:** 32-bit Excel runs out of memory sooner; Mac lacks the Data Model.
**Likely follow-ups:** 1) *Why share cache?* Smaller file. 2) *More than 1,048,576 rows?* Data Model or database.
**Common mistakes:** Blaming Excel when 40 columns of unused text are loaded; building many separate pivots from separate caches.

### Q68 ⭐ 🔴 How would you reproduce a pivot table summary without using a pivot table, using SUMIFS or dynamic arrays?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Formula fluency and understanding of what a pivot does.
**Say this in the interview:** "I list the row and column labels, then use SUMIFS with both criteria. In 365 I can build the label list with UNIQUE and let it spill."
**Explain simply:**
- A pivot is distinct labels plus SUMIFS-style totals.
- SUMIFS adds numbers that meet several conditions. Use `$` anchors so one formula fills the grid.
- Formulas update instantly, unlike a pivot that needs refresh.
- Dynamic arrays (formulas that return many cells that "spill") are new in 365/2021.
**Example:** Sales by region and product.
**Sample sheet:** (A = Region, B = Prod, C = Amt; grid in E:H)

| | A | B | C | E | F | G | H |
|---|---|---|---|---|---|---|---|
| 1 | Region | Prod | Amt | Region | A | B | Total |
| 2 | N | A | 100 | E | | | |
| 3 | N | B | 50 | N | | | |
| 4 | S | A | 70 | S | | | |
| 5 | S | A | 30 | | | | |
| 6 | S | B | 80 | | | | |
| 7 | E | B | 20 | | | | |

**Formula / Steps:** F2: `=SUMIFS($C$2:$C$7,$A$2:$A$7,$E2,$B$2:$B$7,F$1)`, G2 is the same with G$1; H2: `=SUM(F2:G2)`; fill down.
**Alternative:** In 365: `=UNIQUE(A2:A7)` for the row labels and `=UNIQUE(B2:B7)` transposed for the column labels (not run here), then the same SUMIFS formula filled across the grid.
**Result:** Run in LibreOffice: E row 0, 20, total 20; N row 100, 50, 150; S row 100, 80, 180. pandas pivot (run) matches: A 200, B 150, grand total 350.
**Version note:** SUMIFS Excel 2007+. UNIQUE: Excel 365, 2024 and 2021 only, per Microsoft Support "UNIQUE function".
**Edge cases:** Text-numbers are ignored by SUMIFS; a new region needs a new label row unless using UNIQUE.
**Likely follow-ups:** 1) *Why still use pivots?* Speed and drag-and-drop. 2) *Averages?* AVERAGEIFS.
**Common mistakes:** Missing `$` anchors; mismatched range sizes.

### Q69 ⭐ 🔴 How do you show a text field (such as employee names) in the Values area of a pivot table?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know pivots only count text, and what the workarounds are?
**Say this in the interview:** "A normal pivot can only count a text field in Values. To show the names I either put the name in Rows under the department, or I use a formula such as TEXTJOIN, or a DAX measure in the Data Model."
**Explain simply:**
- Microsoft Support ("Create a PivotTable to analyze worksheet data"): when Excel reads data as text, it displays a COUNT.
- Option 1: Dept in Rows, then Name in Rows below it (Tabular layout) to list names.
- Option 2: Formula with TEXTJOIN beside the pivot.
- Option 3: Data Model measure using CONCATENATEX (from memory, unverified).
**Example:** List the employees of each department in one cell.
**Sample sheet:** (A = Name, B = Dept)

| | A | B |
|---|---|---|
| 2 | Asha | HR |
| 3 | Bala | IT |
| 4 | Chitra | HR |
| 5 | Dev | IT |
| 6 | Esha | Sales |

**Formula / Steps:** E2 for HR (D2 = "HR"), array-entered in older versions: `=TEXTJOIN(", ",TRUE,IF($B$2:$B$6=D2,$A$2:$A$6,""))`.
**Alternative:** Pivot with Name in Rows beneath Dept (not run here); or the Data Model measure.
**Result:** TEXTJOIN formula run in LibreOffice (as an array formula): "Asha, Chitra". pandas (run): HR Asha, Chitra; IT Bala, Dev; Sales Esha; the pivot's Count would be HR 2, IT 2, Sales 1.
**Version note:** TEXTJOIN: Excel 2019, 2021, 2024 and 365 (Microsoft Support "TEXTJOIN function"); not Excel 2016 per that page. Excel for the web: unverified.
**Edge cases:** Blank names are skipped with TRUE. In 2019 the formula must be entered with Ctrl+Shift+Enter (from memory).
**Likely follow-ups:** 1) *Why not Max?* Max works on numbers only. 2) *Number IDs?* They sum.
**Common mistakes:** Expecting names to show; forgetting array entry.

### Q70 ⭐ 🔴 How do you create a pivot table in Google Sheets, and how does it differ from Excel?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Awareness of Sheets, since many startups use it.
**Say this in the interview:** "Select the data with headers, Insert > Pivot table, then add Rows, Columns and Values in the side panel. It updates automatically when the source changes."
**Explain simply:**
- Google Docs Editors Help ("Create & use pivot tables"): select the data with a header for each column, Insert > Pivot table, then click Add next to Rows, Columns or Values.
- It refreshes automatically when source cells change (same page).
- Calculated fields: Values > Add > Calculated field.
- Sheets may suggest pivot tables; turn off under Tools > Suggestion controls.
- Differences from Excel: no manual refresh needed; no slicers on pivots like Excel's Report Connections (from memory, unverified); Excel has a Data Model and Power Pivot, Sheets does not (from memory, unverified).
**Example:** Total amount by region.
**Sample sheet:** (A = Region, B = Prod, C = Amt; same as Q68, A1:C7.)
**Formula / Steps:** (not run here; steps from Google Docs Editors Help)
1. Select A1:C7 > Insert > Pivot table > Create.
2. Rows: Region; Values: Amt (SUM).
**Alternative:** `=QUERY()` or SUMIFS formulas (from memory).
**Result:** pandas (run): E 20, N 150, S 180.
**Version note:** Google Sheets is always current; Google's page did not describe a Show as option, so I treat that comparison as unverified.
**Edge cases:** Header-less data; merged cells.
**Likely follow-ups:** 1) *Can Sheets filter?* Yes, pivot filters. 2) *Share?* Share the sheet.
**Common mistakes:** Selecting data without headers.

### Q71 ⭐ 🔴 How do you share a pivot-table report with someone who has Excel 2016 when you built it in Microsoft 365?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Compatibility awareness.
**Say this in the interview:** "I run the Compatibility Checker, avoid 365-only functions such as XLOOKUP and UNIQUE, and if in doubt send a values-only copy or a PDF."
**Explain simply:**
- Microsoft Support ("Save an Excel workbook for compatibility with earlier versions of Excel"): File > Info > Check for Issues > Check Compatibility lists features that might not be available in earlier versions.
- XLOOKUP is not available in Excel 2016 and 2019 (Microsoft Support "XLOOKUP function", which is itself inconsistent about 2016/2019 in its Applies To list); a file with XLOOKUP can still open there.
- UNIQUE is listed for 365, 2024 and 2021 only (Microsoft Support "UNIQUE function").
- Data Model pivots work on Windows Excel 2016 (Microsoft Support "Use multiple tables..."), but not on Mac.
- Pivot tables, slicers and pivot charts open in Excel 2016 (slicer page notes 2016 UI differences).
**Example:** Your dashboard uses XLOOKUP for a helper column; the 2016 user sees errors.
**Formula / Steps:** (not run here)
1. File > Info > Check for Issues > Check Compatibility.
2. Replace XLOOKUP with INDEX/MATCH; UNIQUE with Remove Duplicates or a pivot.
3. Paste values for fragile formulas, or Save As PDF.
**Alternative:** Ask them to use Excel for the web (from memory).
**Result:** Not run here.
**Version note:** As cited above.
**Edge cases:** Mac recipients cannot use Data Model pivots.
**Likely follow-ups:** 1) *Other option?* Share a PDF.
**Common mistakes:** Assuming the whole file works because it opens.

### Q72 ⭐ 🔴 How do you use a pivot table to compare actual against target and show the variance?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Calculated fields on top of two value columns.
**Say this in the interview:** "I put Actual and Target both in Values, then add a calculated field Variance = Actual - Target and Variance % = Variance / Target."
**Explain simply:**
- Variance = actual minus target. Negative means under target.
- Calculated fields compute on the summed fields, so totals are total variance over total target.
- Alternatively, Show Values As > Difference From works across items of one field, not between two columns.
**Example:** Hiring actuals versus targets by department.
**Sample sheet:** (A = Dept, B = Actual, C = Target)

| | A | B | C |
|---|---|---|---|
| 2 | HR | 4 | 5 |
| 3 | HR | 6 | 5 |
| 4 | IT | 10 | 10 |
| 5 | IT | 9 | 10 |
| 6 | Sales | 12 | 14 |
| 7 | Sales | 15 | 14 |

**Formula / Steps:** (not run here)
1. Dept in Rows; Actual and Target in Values.
2. PivotTable Analyze > Fields, Items & Sets > Calculated Field: `=Actual-Target`, then `=(Actual-Target)/Target`.
**Alternative:** Cell formulas: Sales row F2 `=SUMIFS($B$2:$B$7,$A$2:$A$7,E2)`, G2 same on C, H2 `=F2-G2`, I2 `=H2/G2`.
**Result:** pandas (run): HR 10 vs 10, 0 (0.0%); IT 19 vs 20, -1 (-5.0%); Sales 27 vs 28, -1 (-3.6%); Total 56 vs 58, -2 (-3.4%). LibreOffice (run) Sales: 27, 28, -1, -0.0357.
**Version note:** Calculated fields in desktop Excel (from memory, unverified).
**Edge cases:** Zero target gives #DIV/0!.
**Likely follow-ups:** 1) *Targets in another table?* Data Model.
**Common mistakes:** Averaging percentages.

### Q73 ⭐ 🔴 What are the limitations of pivot tables that make you reach for Power Pivot or Power Query?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know when to step up the tool.
**Say this in the interview:** "A normal pivot works on one flat table and needs clean data. Power Query cleans and combines sources; Power Pivot relates many tables and handles millions of rows with measures."
**Explain simply:**
- Microsoft Support ("Learn to use Power Query and Power Pivot in Excel"): Power Query imports, shapes and combines data; Power Pivot builds models from many sources; both handle "up to millions of rows".
- Excel's own limits: 1,048,576 rows per sheet (Support, "Excel specifications and limits").
- Normal pivots cannot join tables or do distinct counts (Data Model needed).
- Data Models are not supported on Mac (Support "Use multiple tables...").
- Calculated fields are limited compared with DAX (from memory).
**Example:** Joining HRMS, payroll and attendance exports monthly.
**Formula / Steps:** (not run here) Data > Get Data > Combine Queries > Merge; load to Data Model.
**Alternative:** Power BI or SQL.
**Result:** Not run here.
**Version note:** Per Microsoft page: full features in Windows Microsoft 365 Apps for enterprise; Excel 2024 and 2021 listed.
**Edge cases:** 32-bit Excel memory limits.
**Likely follow-ups:** 1) *Power Query vs Pivot?* Query prepares, pivot summarises.
**Common mistakes:** Treating Power Pivot as a separate product from Excel.

### Q74 ⭐ 🔴 How do you build a headcount-by-tenure-band report from joining dates using a pivot table?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Date arithmetic plus banding.
**Say this in the interview:** "I add a helper column for tenure in completed years with DATEDIF against a fixed as-of date, band it, then pivot Band against count of employees."
**Explain simply:**
- Tenure = time since joining. DATEDIF with "y" returns completed years.
- A fixed as-of date cell keeps the report repeatable (TODAY() changes daily).
- Band with LOOKUP, or group the tenure numbers in the pivot (Microsoft Support "Group or ungroup data in a PivotTable" covers grouping numbers).
**Example:** Headcount as of 22 Oct 2026.
**Sample sheet:** (A = Emp, B = Join date, C = Yrs, D = Band, G1 = as-of 22-Oct-2026; I1:L2 = band thresholds 0,1,3,6 with labels)

| | A | B | C | D |
|---|---|---|---|---|
| 2 | E1 | 01-Jun-2026 | 0 | <1 |
| 3 | E2 | 15-Mar-2025 | 1 | 1-2 |
| 4 | E3 | 01-Sep-2023 | 3 | 3-5 |
| 5 | E4 | 10-Jan-2021 | 5 | 3-5 |
| 6 | E5 | 01-Jul-2018 | 8 | 6+ |
| 7 | E6 | 01-Dec-2025 | 0 | <1 |

**Formula / Steps:** C2: `=DATEDIF(B2,$G$1,"y")`; D2: `=LOOKUP(C2,$I$1:$L$1,$I$2:$L$2)`. Pivot (not run here): Band to Rows, Emp to Values (Count).
**Alternative:** Pivot on Yrs, right-click > Group, Starting 0, Ending 10, By 3 (not run here).
**Result:** DATEDIF and LOOKUP run in LibreOffice: years 0, 1, 3, 5, 8, 0 and bands <1, 1-2, 3-5, 3-5, 6+, <1. pandas (run): <1 = 2, 1-2 = 1, 3-5 = 2, 6+ = 1.
**Version note:** DATEDIF works in Excel though undocumented in the function list (from memory, unverified).
**Edge cases:** Future join dates give errors; blanks.
**Likely follow-ups:** 1) *Months?* "ym".
**Common mistakes:** Using TODAY so history changes; band edges overlapping.

