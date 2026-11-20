# Book 4 — Power BI & Visualization | Part 9: Scenario Tasks (Build HR/Sales Dashboard, Fix a Slow Report, Reconcile Numbers) 🔴

**Target:** 70 questions | **Actual:** 70 questions
**Scope:** practical Power BI build, fix and reconcile tasks: HR and sales dashboards, slow-report diagnosis, number mismatches, refresh and sharing problems.

### Q1 ⭐⭐⭐ 🟢 Walk me through a Power BI dashboard you built, from raw data to published report.
**Asked at:** commonly asked (no company-specific report found); scenario lists in the Part 9 sources file (FanRuan, Medium snippets) include "walk me through a dashboard".
**What the interviewer is checking:** Whether you have really done the full cycle (ask, clean, model, measure, visualise, publish, maintain) and can tell it as a clear story with a business result.
**Say this in the interview:** "I start with the business question, load and clean the data in Power Query, build a star-schema model with a date table, write DAX measures, design one clear page per question, then publish to the Service, set refresh and access, and collect feedback." Then tell your own project: the problem, the data, one hard thing you fixed, the outcome.
**Explain simply:**
- **Power Query** = the cleaning step before data loads (fix types, remove duplicates, merge files).
- **Star schema** = one central table of events (sales, attendance) surrounded by small lookup tables (dates, employees, products). It keeps numbers correct and fast.
- **Measure** = a reusable formula (DAX) that recalculates for whatever the user filters.
- **Publish** = send the .pbix file from Desktop to the Power BI Service (the online site) so others can open it.
- Close with the outcome: "HR stopped spending two days a month on Excel."
**Example:** Monthly attendance report for 1,200 staff: 12 Excel files cleaned in Power Query, model with Employee and Date tables, measures for Present %, Absent %, page 1 summary, page 2 department drill-down, refreshed every morning.
**DAX / Steps:** Not run here (no Power BI available). Outline: 1) Home > Get data. 2) Home > Transform data (clean). 3) Model view (relationships). 4) Measures via Home > New measure. 5) Report view (visuals). 6) Home > Publish. 7) In the Service: semantic model > Settings > Scheduled refresh; Share/app for access.
**Alternative:** If you have no real project, walk through a public-dataset or HR practice dashboard honestly, naming it as a practice project.
**Version / licensing note:** From memory, unverified (learn.microsoft.com could not be reached from this session). Desktop is believed free and Windows-only; publishing and sharing need a work or school account and usually a Pro licence for both author and viewers.
**Edge cases:** Do not claim features you did not use. Be ready to say what you would do differently.
**Likely follow-ups:** 1) *Hardest part?* Pick one real issue (duplicate employees, date logic). 2) *How did users give feedback?* Review meeting, change log.
**Common mistakes:** Listing visuals instead of telling the story; skipping the business question; no mention of data checks.

### Q2 ⭐⭐⭐ 🟢 You are given an HR dataset and asked to build a dashboard in Power BI: what are your steps?
**Asked at:** commonly asked (no company-specific report found); HR scenario written from standard practice, not seen as a question in a source.
**What the interviewer is checking:** A structured method that starts with questions and data checks, not with dragging charts.
**Say this in the interview:** "First I confirm the questions and definitions (headcount, attrition), profile the data, clean it in Power Query, model it as employees plus a date table, write measures, build a summary page and a detail page, test against a known number, then publish and schedule refresh."
**Explain simply:**
- **Define:** who uses it, which decisions, and definitions agreed with HR (is a contractor headcount?).
- **Profile and clean:** check blanks, duplicates, text dates, department spellings.
- **Model:** Employees table, Department table, Date table, Attendance or Exits fact table, joined by IDs.
- **Measures:** Headcount, Leavers, Attrition % (Q6).
- **Visuals:** KPI cards on top, trend in the middle, breakdowns below (Q4).
- **Validate and publish:** match to HR's own count, then release (Q22).
**Example:** 1,500 employee rows. Before building, you find 12 employees listed twice and 40 blank departments; you fix these first, so the headcount card reads 1,488 and not 1,500.
**DAX / Steps:** Not run here. Click-path: Home > Get data > Excel > Transform data > (fix) > Close & Apply > Model view > Home > New measure > Report view > Home > Publish.
**Alternative:** Start from a sketch on paper or a wireframe with the requester so layout is agreed before any build.
**Version / licensing note:** From memory, unverified. Same Desktop/Service split as Q1.
**Edge cases:** Sensitive columns (salary, rating) need row-level security or exclusion before publishing (Q65). People who left must stay in the data for history.
**Likely follow-ups:** 1) *Which visuals?* See Q4. 2) *How do you know numbers are right?* Reconcile to HRIS or payroll totals.
**Common mistakes:** Building visuals first; ignoring blanks and duplicates; no agreed definition of attrition.

### Q3 ⭐⭐⭐ 🟢 Your manager asks for a sales dashboard: what questions do you ask before you open Power BI?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you gather requirements instead of guessing, which separates analysts from chart-makers.
**Say this in the interview:** "I ask who will use it and what decision it supports, which metrics and definitions count (gross or net sales, which date), what grain and filters they need, where the data lives and how fresh it must be, and who may see what."
**Explain simply:**
- **Audience and decision:** a sales head, a regional manager, finance? Each needs different detail.
- **Metric definitions:** is revenue before or after returns and tax; order date or invoice date?
- **Comparisons:** against target, last month, last year.
- **Data:** source system, file or database, owner, quality, how often it updates.
- **Access:** do regional managers see only their region (row-level security)?
- **Delivery:** deadline, device (laptop or phone), and how success is measured.
**Example:** A manager says "show sales". Your questions reveal she means net revenue by region by invoice month versus target, refreshed daily at 8 am, with each regional head seeing only their region. That is a very different build from one total.
**DAX / Steps:** Not applicable (a process answer, nothing run).
**Alternative:** Use a one-page requirements checklist or a quick mock-up in PowerPoint and get a sign-off.
**Version / licensing note:** Not applicable beyond: sharing to many viewers needs the right licence (from memory, unverified).
**Edge cases:** Conflicting definitions between sales and finance; agree one and write it down (see Q50).
**Likely follow-ups:** 1) *If they cannot answer?* Propose a definition and confirm in writing. 2) *What if the data is poor?* Flag it early with examples.
**Common mistakes:** Opening Power BI immediately; accepting "just show everything"; not asking about refresh timing.

### Q4 ⭐⭐⭐ 🟢 Which KPIs and visuals would you put on an HR headcount and attrition dashboard?
**Asked at:** commonly asked (no company-specific report found); written from standard HR-analytics practice.
**What the interviewer is checking:** Whether you pick KPIs HR leaders actually use and match each to a suitable visual.
**Say this in the interview:** "Top row of cards: headcount, joiners, leavers, attrition %. Then a line chart of headcount and attrition by month, bars by department, a tenure-band chart, and slicers for department, location and date. A table of leavers with reasons sits on a detail page."
**Explain simply:**
- **Headcount:** employees active on a date. **Attrition %:** leavers in a period divided by average headcount (Q6, Q27).
- **Cards** show one number; **line chart** shows trend over time; **bar chart** compares departments; **table** gives names for follow-up.
- Add useful extras: new-hire attrition (left within 90 days), tenure band, voluntary vs involuntary, gender or diversity mix if the company reports it.
- Keep it to about 5 to 7 visuals per page (see Q18).
**Example:** Headcount 1,200, joiners 40, leavers 25, monthly attrition 2.1%. Bars show IT at 3.5% and HR at 0.8%, so leadership asks why IT is high.
**DAX / Steps:** Not run here. Measures are in Q6. Click-path: Report view > Visualizations pane > Card, Line chart, Clustered bar; Insert > ... or Visualizations > Slicer.
**Alternative:** A headcount waterfall (opening + joiners - leavers = closing) explains movement in one visual.
**Version / licensing note:** From memory, unverified.
**Edge cases:** Quote the attrition period (monthly vs annualised) on the card; 2% monthly is not 2% yearly.
**Likely follow-ups:** 1) *Voluntary vs involuntary?* Needs an exit-reason column. 2) *Annualised attrition?* Last 12 months leavers divided by average headcount of those 12 months.
**Common mistakes:** Mixing monthly and annual rates; pie charts with many slices; no definition on the dashboard.

### Q5 ⭐⭐⭐ 🟢 Which KPI cards, charts and filters would you put on a monthly sales dashboard?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you design a useful, uncluttered sales view with comparisons, not just totals?
**Say this in the interview:** "Cards for net sales, target achievement %, units, average order value and growth versus last month and last year. A trend line by month, a column chart of sales versus target, top products and regions, and slicers for date, region and product category."
**Explain simply:**
- **KPI card:** a big single number, ideally with a comparison (vs last month, vs target).
- **Trend (line):** shows direction over time. **Bars:** rank products or regions.
- **Slicers:** buttons or dropdowns that let users filter the whole page.
- **Target achievement %:** actual divided by target (Q25).
- Keep one primary question per page: "Are we on track this month?"
**Example:** Net sales 4.2 crore, target achievement 96%, growth +8% versus last year, with the South region as the only one below target.
**DAX / Steps:** Not run here. Cards: Visualizations > Card. Combo chart: Line and clustered column chart (Q15). Slicers: Visualizations > Slicer, fields Date, Region, Category.
**Alternative:** Use a matrix with conditional formatting if users prefer a numbers-first view.
**Version / licensing note:** From memory, unverified.
**Edge cases:** A partial current month looks like a drop; compare month-to-date with the same days last month.
**Likely follow-ups:** 1) *Why not a pie chart?* Hard to compare similar slices. 2) *How many slicers?* Only those users really need.
**Common mistakes:** Too many KPIs; no target or prior-period comparison; mixing gross and net sales.

### Q6 ⭐⭐⭐ 🟡 Write the DAX measures for headcount, leavers and attrition rate for an HR dashboard.
**Asked at:** commonly asked (no company-specific report found); HR DAX designs in the Part 9 sources file are from general knowledge, not seen in a source.
**What the interviewer is checking:** Can you define a point-in-time headcount and divide leavers by average headcount with safe division?
**Say this in the interview:** "Headcount is employees who had joined on or before a date and had not left by it. Leavers are people whose leave date falls inside the period. Attrition is leavers divided by the average of opening and closing headcount, using DIVIDE to avoid divide-by-zero."
**Explain simply:**
- **Measure:** a formula recalculated for each cell of a visual. **Filter context:** the slicer, row or month a visual applies.
- I read the month with MIN and MAX of the Date table, then count employees by their own JoinDate and LeaveDate. REMOVEFILTERS('Date') stops the month from also filtering by join date.
- Opening headcount is the headcount on the day before the period starts.
- Department or slicer filters on the Employees table still apply automatically.
**Example:** March 2024 in the sample below: 6 people at the start, 5 at the end, 2 left, so attrition is 2 / 5.5 = 36.4% (a tiny sample, so the rate is huge).
**Sample data:** Table `Employees` (blank LeaveDate = still employed):

| EmpID | Dept | JoinDate | LeaveDate |
|---|---|---|---|
| 1 | Sales | 2022-03-01 | |
| 2 | Sales | 2023-06-15 | 2024-03-12 |
| 3 | Sales | 2024-02-10 | |
| 4 | IT | 2021-08-01 | 2024-02-20 |
| 5 | IT | 2023-01-20 | |
| 6 | IT | 2024-03-05 | |
| 7 | HR | 2022-11-01 | |
| 8 | HR | 2024-01-08 | 2024-03-28 |

**DAX / Steps:** Not run here (no DAX engine available). Assumes a marked Date table `'Date'` with a `[Date]` column, and no active relationship that makes the Date filter hit JoinDate.
```dax
Headcount (End) =
VAR EndDate = MAX ( 'Date'[Date] )
RETURN
    CALCULATE (
        COUNTROWS ( Employees ),
        REMOVEFILTERS ( 'Date' ),
        Employees[JoinDate] <= EndDate,
        OR ( ISBLANK ( Employees[LeaveDate] ), Employees[LeaveDate] > EndDate )
    )

Headcount (Start) =
VAR StartDate = MIN ( 'Date'[Date] ) - 1
RETURN
    CALCULATE (
        COUNTROWS ( Employees ),
        REMOVEFILTERS ( 'Date' ),
        Employees[JoinDate] <= StartDate,
        OR ( ISBLANK ( Employees[LeaveDate] ), Employees[LeaveDate] > StartDate )
    )

Leavers =
VAR StartDate = MIN ( 'Date'[Date] )
VAR EndDate = MAX ( 'Date'[Date] )
RETURN
    CALCULATE (
        COUNTROWS ( Employees ),
        REMOVEFILTERS ( 'Date' ),
        Employees[LeaveDate] >= StartDate,
        Employees[LeaveDate] <= EndDate
    )

Attrition % =
DIVIDE ( [Leavers], ( [Headcount (Start)] + [Headcount (End)] ) / 2 )
```
**Alternative:** Simpler but cruder: divide leavers by closing headcount only, or by a fixed opening headcount for annual reports. Say which you used.
**Result:** Reproduced with pandas (not run in DAX), March 2024:

| Dept | Opening | Closing | Leavers | Attrition % |
|---|---|---|---|---|
| HR | 2 | 1 | 1 | 66.7 |
| IT | 1 | 2 | 0 | 0.0 |
| Sales | 3 | 2 | 1 | 40.0 |
| Total | 6 | 5 | 2 | 36.4 |

**Pandas check:**
```python
s,e=pd.Timestamp("2024-03-01"),pd.Timestamp("2024-03-31")
def hc(d): return (emp.JoinDate<=d)&(emp.LeaveDate.isna()|(emp.LeaveDate>d))
emp["open"]=hc(s-pd.Timedelta(days=1)); emp["close"]=hc(e)
emp["leaver"]=(emp.LeaveDate>=s)&(emp.LeaveDate<=e)
g=emp.groupby("Dept").agg(Opening=("open","sum"),Closing=("close","sum"),Leavers=("leaver","sum"))
g.loc["Total"]=g.sum(); g["Attr%"]=(g.Leavers/((g.Opening+g.Closing)/2)*100).round(1)
```
Printed output matches the table above (Total 6, 5, 2, 36.4).
**Version / licensing note:** From memory, unverified (Microsoft Learn DAX pages could not be fetched; syntax of CALCULATE, REMOVEFILTERS, DIVIDE, COUNTROWS, MIN/MAX is from memory and not checked on the page).
**Edge cases:** Rehires (same person twice, see Q29); leave date before join date (bad data); total row uses the whole-table average, not the sum of department rates.
**Likely follow-ups:** 1) *Annual attrition?* Leavers in 12 months over average headcount of the period. 2) *Why DIVIDE?* It returns blank instead of an error on zero.
**Common mistakes:** Using COUNT of leave dates for headcount; forgetting REMOVEFILTERS so joiners vanish; dividing by closing headcount without saying so.

### Q7 ⭐⭐⭐ 🟡 Your Power BI report is slow: what do you check, in order?
**Asked at:** Deloitte (Sept 2025 Power BI round, slow report/optimisation) per research/interview_processes.md as cited in the Part 9 sources file; single, unverified report. Otherwise commonly asked.
**What the interviewer is checking:** Do you diagnose before changing things, starting with measurement?
**Say this in the interview:** "I measure first with Performance Analyzer to find the slow visual, then check whether time is in the DAX query, the visual drawing or elsewhere. Then I reduce visuals per page, fix heavy measures, slim the model (fewer columns, star schema, right data types), and finally check the source, gateway and capacity."
**Explain simply:**
- **Order:** 1) measure (Q8), 2) too many visuals or high-detail tables, 3) heavy DAX, 4) model size and shape, 5) data source or DirectQuery, 6) capacity and gateway.
- **Quick wins:** fewer visuals on a page, restrictive filters, Top N, hide unused columns, avoid very high-cardinality columns (like timestamps), turn off auto date/time.
- Test in Desktop first, then in the Service (Q70).
**Example:** A 14-visual page takes 12 s. Performance Analyzer shows one table with 50,000 rows takes 9 s. Replace it with a Top 20 table plus a drill-through page: load drops to 3 s.
**DAX / Steps:** Not run here. View tab > Performance analyzer > Start recording > Refresh visuals > expand each visual (Q8).
**Alternative:** DAX Studio (a free external tool) shows server timings for a copied query.
**Version / licensing note:** From memory, unverified (the Optimization guide page was not fetched in this session).
**Edge cases:** Slow only for some users points to row-level security or capacity; slow only at first open can be cold cache.
**Likely follow-ups:** 1) *Biggest model win?* Remove unused columns and reduce row granularity. 2) *Biggest DAX win?* Avoid row-by-row iterators on large tables when a simple aggregate works.
**Common mistakes:** Rewriting DAX without measuring; blaming Power BI when the source is slow; adding more visuals "to be complete".

### Q8 ⭐⭐⭐ 🟡 How do you use Performance Analyzer to find which visual is slow?
**Asked at:** commonly asked (no company-specific report found); SQLBits and Techcanvass snippets in the sources file describe this workflow (snippets only).
**What the interviewer is checking:** Do you know the tool and can you read its three timings?
**Say this in the interview:** "I open Performance Analyzer, start recording, refresh visuals, then expand the log. Each visual shows DAX query time, visual display time and other time. The biggest bar tells me where to work: a long DAX query means fix the measure or model; long display time means the visual is too heavy."
**Explain simply:**
- **Performance Analyzer** = a built-in stopwatch for each visual on a page.
- **DAX query:** time for the model to compute the answer. **Visual display:** time to draw it. **Other:** waiting for other visuals and overhead.
- You can copy a visual's query and run it elsewhere (DAX query view or DAX Studio) to tune it.
- Clear the cache by recording after changing a page or a slicer, so you time a realistic run.
**Example:** Results: Card 40 ms, Line chart 120 ms, Matrix 6,500 ms of which 6,200 ms DAX query. The matrix measure is the target.
**DAX / Steps:** Not run here. View tab > Show panes group > Performance analyzer > Start recording > Refresh visuals (or click a slicer) > expand a visual in the pane > Copy query. Stop recording when done.
**Alternative:** Use DAX query view or DAX Studio to time the copied query and try rewrites.
**Version / licensing note:** From memory, unverified. I believe it is also available when editing a report in the Service, but this is not confirmed here.
**Edge cases:** First run is slower (cold cache); results vary with the machine, so repeat two or three times.
**Likely follow-ups:** 1) *What if "Other" is large?* Too many visuals competing; reduce them. 2) *Does it show refresh speed?* No, only report interaction speed.
**Common mistakes:** Reading one run only; fixing the fastest visual; confusing report slowness with data refresh slowness.

### Q9 ⭐⭐⭐ 🟡 The total in your Power BI report does not match the Excel total: how do you find the reason?
**Asked at:** commonly asked (no company-specific report found); Fabric Community threads in the sources file (snippet only) list typical causes.
**What the interviewer is checking:** A calm, step-by-step reconciliation method rather than guessing.
**Say this in the interview:** "I compare like with like: same date range and filters first, then row counts, then split the difference by a key such as month or region until I find where it appears. Usual causes are filters, duplicates, text-typed numbers, blank or unmatched keys, and different definitions."
**Explain simply:**
- **Step 1:** make Excel and Power BI use identical filters and period; clear slicers.
- **Step 2:** compare row counts after Power Query, not just totals.
- **Step 3:** build a table visual with the key (month, region) and compare line by line to find the gap.
- **Step 4:** check Power Query steps for removed rows, errors, duplicates, and wrong types (numbers loaded as text become errors or blanks).
- **Step 5:** check relationships and measure logic (cancelled orders excluded in Power BI but not in the pivot?).
**Example:** Excel total 8,500; Power BI 6,700. Difference 1,800 equals the one cancelled order that the measure filters out. After agreeing the definition, both show 6,700.
**Sample data:** Table `Orders`:

| Order | Amount | Status |
|---|---|---|
| 1 | 1000 | Done |
| 2 | 2500 | Done |
| 3 | 1800 | Cancelled |
| 4 | 2500 | Done |
| 5 | 700 | Done |

**DAX / Steps:** Not run here. Click-path: Report view > add a Table visual with Order, Amount, Status > compare with Excel; Home > Transform data > check Applied Steps and Column quality/distribution (View tab).
**Alternative:** Load the Excel file as its own query and merge (anti-join) with the report data to list the rows that differ.
**Result:** Reproduced with pandas: Excel-style total of all rows = 8,500; total excluding Cancelled = 6,700; gap = 1,800 (order 3).
**Pandas check:**
```python
x.Amount.sum(), x[x.Status=="Done"].Amount.sum()   # (8500, 6700)
```
Printed 8500 6700 (the difference of 1,800 is order 3).
**Version / licensing note:** From memory, unverified.
**Edge cases:** Rounding or hidden rows in Excel; time zone shifting dates across month ends; many-to-many relationships duplicating values.
**Likely follow-ups:** 1) *Totals differ but rows match?* Measure logic or filter. 2) *Row counts differ?* Power Query step or source refresh date.
**Common mistakes:** Comparing before checking the date range; trusting the grand total of a measure instead of splitting it.

### Q10 ⭐⭐⭐ 🟡 How would you model the tables for a sales dashboard before building any visual?
**Asked at:** commonly asked (no company-specific report found); Medium scenario list (snippet) mentions star schema for multi-region sales.
**What the interviewer is checking:** Do you know the star schema, relationship direction and the date table?
**Say this in the interview:** "I build a star schema: one Sales fact table and separate Date, Product, Customer and Region dimension tables, each linked one-to-many to Sales by an ID, filtering from dimension to fact, plus a marked date table."
**Explain simply:**
- **Fact table:** one row per sale (many rows, numbers like amount, quantity). **Dimension table:** one row per thing (one row per product), used to slice.
- **Relationship:** a link between ID columns. One-to-many from dimension to fact, single direction.
- **Text diagram:** `Date, Product, Customer, Region --1 to many--> Sales`.
- Keep descriptive columns in dimensions, not repeated in Sales. Add a Date table (Q36).
**Example:** Sales has 2 million rows with ProductID. Product has 500 rows with Name and Category. Slicing by Category uses Product, which filters Sales; it stays fast.
**Sample data:** Table `Sales` (fact):

| OrderID | DateKey | ProductID | CustomerID | Amount |
|---|---|---|---|---|
| 1001 | 2024-04-02 | P1 | C1 | 5000 |
| 1002 | 2024-04-03 | P2 | C1 | 3000 |
| 1003 | 2024-05-01 | P1 | C2 | 4000 |

Table `Product` (dimension):

| ProductID | Name | Category |
|---|---|---|
| P1 | Laptop | Electronics |
| P2 | Chair | Furniture |

**DAX / Steps:** Not run here. Model view > drag Product[ProductID] onto Sales[ProductID] (or Home > Manage relationships > New) > cardinality One to many, cross filter Single > mark Date table (Table tools > Mark as date table).
**Result:** Reproduced with pandas (the relationship itself not run): slicing by Category through Product gives Electronics 9,000 and Furniture 3,000; total 12,000 equals Sales total.
**Pandas check:**
```python
import pandas as pd
sales=pd.DataFrame({"OrderID":[1001,1002,1003],"ProductID":["P1","P2","P1"],"Amount":[5000,3000,4000]})
prod=pd.DataFrame({"ProductID":["P1","P2"],"Category":["Electronics","Furniture"]})
print(sales.merge(prod,on="ProductID").groupby("Category").Amount.sum()); print("Total:",sales.Amount.sum())
```
Printed Electronics 9000, Furniture 3000, Total 12000.
**Alternative:** One wide flat table is quicker for tiny data but repeats text, bloats size and breaks easily; use only for quick prototypes.
**Version / licensing note:** From memory, unverified.
**Edge cases:** Duplicate IDs in a dimension block one-to-many; unmatched IDs create a (Blank) category (Q35); avoid both-direction filters unless needed.
**Likely follow-ups:** 1) *Why not one big table?* Size, speed and ambiguity. 2) *Snowflake vs star?* Star is simpler, preferred.
**Common mistakes:** Joining fact to fact; many-to-many everywhere; no date table.

### Q11 ⭐⭐⭐ 🟡 A manager says a number on your dashboard looks wrong: how do you investigate and respond?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Professionalism: do you listen, verify, explain and fix, rather than get defensive?
**Say this in the interview:** "I thank them, ask exactly which number and what they expected and why, reproduce it with the same filters, trace it back to the source rows, then reply with the cause and, if it is my error, the fix and the date it will be corrected."
**Explain simply:**
- **Clarify:** screenshot, filters, period, expected value and its source.
- **Reproduce** with the same slicers; check refresh time (may be stale).
- **Trace:** table visual of underlying rows, compare to source (Q9).
- **Decide:** error in data, logic, or definition difference.
- **Respond** within the day: cause, impact, fix, prevention.
**Example:** Manager expects 1,210 headcount, report shows 1,198. You find 12 employees with a blank join date excluded; you confirm with HR, add a rule, and send a short note.
**DAX / Steps:** Not run here. Report view > right-click visual > Show as a table (or Show data) to inspect rows; View > Performance analyzer is not needed.
**Alternative:** Add a "Data last refreshed" card and a definitions page to prevent repeat questions.
**Version / licensing note:** From memory, unverified.
**Edge cases:** Manager is correct but using a different definition; document both.
**Likely follow-ups:** 1) *What if you are wrong?* Admit, fix, notify all users. 2) *What if they are wrong?* Show the reconciliation politely.
**Common mistakes:** Defending without checking; fixing silently; no follow-up message.

### Q12 ⭐⭐ 🟢 How would you clean a messy attendance export in Power Query before building the report?
**Asked at:** commonly asked (no company-specific report found); written from standard practice for MIS/WFM reporting.
**What the interviewer is checking:** Familiarity with Power Query cleaning steps and keeping the process repeatable.
**Say this in the interview:** "I load the file into Power Query, fix headers, trim and standardise text, convert dates and numbers to proper types, replace placeholders like n/a with null, remove blanks and exact duplicates, and keep every step so refresh repeats it."
**Explain simply:**
- **Power Query** records each cleaning action as an *Applied Step*, so next month's file is cleaned automatically.
- Typical steps: Use First Row as Headers; Trim and Capitalize Each Word; set data types (using locale for day-month dates); Replace Values; Remove Blank Rows; Remove Duplicates.
- Check Column quality to see errors and empties.
**Example:** Attendance rows have " asha " and "Asha" as separate people, dates in two formats, "n/a" in hours and a repeated row. After cleaning: 3 clean rows, 1 null hours.
**Sample data:** Table `RawAttendance`:

| Emp | Date | Status | Hrs |
|---|---|---|---|
| " asha " | 01-03-2024 | P | 8.5 |
| Asha | 01/03/2024 | P | 8.5 |
| Ravi | 02-03-2024 | A | n/a |
| Ravi | 02-03-2024 | A | n/a |
| Meena | 03-03-2024 | L | 0 |
| (blank) | 03-03-2024 | P | 8 |

**DAX / Steps:** Not run here. Power Query M sketch:
```m
let
    Source = Excel.Workbook(File.Contents("C:\Data\attendance.xlsx"), null, true),
    Raw = Source{[Item="Attendance",Kind="Sheet"]}[Data],
    Promoted = Table.PromoteHeaders(Raw, [PromoteAllScalars=true]),
    Trimmed = Table.TransformColumns(Promoted, {{"Emp", each Text.Proper(Text.Trim(_)), type text}}),
    FixDate = Table.TransformColumns(Trimmed, {{"Date", each Text.Replace(Text.From(_), "/", "-"), type text}}),
    Dates = Table.TransformColumnTypes(FixDate, {{"Date", type date}}, "en-GB"),
    Hrs = Table.ReplaceValue(Dates, "n/a", null, Replacer.ReplaceValue, {"Hrs"}),
    Typed = Table.TransformColumnTypes(Hrs, {{"Hrs", type number}}),
    NoBlank = Table.SelectRows(Typed, each [Emp] <> null and [Emp] <> ""),
    Deduped = Table.Distinct(NoBlank)
in
    Deduped
```
**Alternative:** Do light cleanup in the source system or Excel template, but Power Query keeps it repeatable.
**Result:** Reproduced with pandas (the M code itself not run): 3 rows remain: Asha 2024-03-01 P 8.5; Ravi 2024-03-02 A with hours blank (NaN); Meena 2024-03-03 L 0.0. (The sample dates are day-month; 02-03-2024 reads as 2 March.)
**Pandas check:**
```python
c["Emp"]=c.Emp.str.strip().str.title()
c["Date"]=pd.to_datetime(c.Date.str.replace("/","-"),format="%d-%m-%Y")
c["Hrs"]=pd.to_numeric(c.Hrs,errors="coerce")
c=c.dropna(subset=["Emp"]).drop_duplicates()
```
Printed 3 rows: (Asha, 2024-03-01, P, 8.5), (Ravi, 2024-03-02, A, NaN), (Meena, 2024-03-03, L, 0.0).
**Version / licensing note:** From memory, unverified (exact menu names such as "Using Locale" were not checked).
**Edge cases:** Dates read in the wrong locale (month and day swapped); duplicates differing by a space; hidden rows in Excel.
**Likely follow-ups:** 1) *Remove Duplicates risk?* It can delete genuine repeats; choose key columns. 2) *Many monthly files?* Folder combine (Q43).
**Common mistakes:** Cleaning by hand in Excel each month; changing type before fixing text; wrong date locale.

### Q13 ⭐⭐ 🟢 How would you show the hiring funnel (applied, screened, interviewed, offered, joined) in Power BI?
**Asked at:** commonly asked (no company-specific report found); HR-flavoured, not seen as a question in a source.
**What the interviewer is checking:** Choosing a funnel visual and showing conversion at each stage, with stages in the right order.
**Say this in the interview:** "I use a funnel chart or a bar chart with stages in a fixed order, and show counts plus conversion from the previous stage and from the start, so recruiters see where candidates drop."
**Explain simply:**
- **Funnel chart:** bars shrinking from top to bottom, one per stage.
- Stages sort alphabetically by default, so give each stage a **sort order column** and sort by it.
- **Conversion %:** stage count divided by the previous stage (or by Applied).
- If each candidate has one row with a current stage, you need counts of "reached at least this stage"; a stage-history table makes it simple.
**Example:** 1,000 applied, 36 joined: overall conversion 3.6%. The lowest stage-to-stage conversion is Interviewed to Offered at 30%; Offered to Joined is 80%, so 9 of 45 offers did not join (offer drop-outs).
**Sample data:** Table `Funnel`:

| Stage | Order | Candidates |
|---|---|---|
| Applied | 1 | 1000 |
| Screened | 2 | 400 |
| Interviewed | 3 | 150 |
| Offered | 4 | 45 |
| Joined | 5 | 36 |

**DAX / Steps:** Not run here.
```dax
Candidates = SUM ( Funnel[Candidates] )

% of Applied =
DIVIDE ( [Candidates], CALCULATE ( [Candidates], Funnel[Stage] = "Applied", ALL ( Funnel[Stage] ) ) )

% of Previous Stage =
VAR cur = MAX ( Funnel[Order] )
RETURN
    DIVIDE (
        [Candidates],
        CALCULATE ( SUM ( Funnel[Candidates] ), ALL ( Funnel ), Funnel[Order] = cur - 1 )
    )
```
Click-path: Visualizations > Funnel; Axis = Stage, Values = Candidates; select Stage column > Column tools > Sort by column > Order.
**Alternative:** A bar chart plus a table of conversion percentages is easier to read when stages are many.
**Result:** Reproduced with pandas (DAX not run): % of Applied = 100, 40, 15, 4.5, 3.6; % of previous = blank, 40, 37.5, 30, 80.
**Pandas check:**
```python
f["% of Applied"]=(f.Cand/1000*100).round(1); f["% of prev"]=(f.Cand/f.Cand.shift()*100).round(1)
```
Printed the values listed above.
**Version / licensing note:** From memory, unverified.
**Edge cases:** Candidates who skip a stage; the first stage has no previous (blank); filter by role or source will re-scale the percentages. On the total row (no single stage in context) MAX of Order is 5, so `% of Previous Stage` would compare against stage 4; hide it there or wrap it in `IF ( HASONEVALUE ( Funnel[Stage] ), ... )`.
**Likely follow-ups:** 1) *Time between stages?* Needs dates per stage (Q47). 2) *Funnel vs bar?* Bars compare better.
**Common mistakes:** Stages alphabetically sorted; dividing by wrong base; counting current stage instead of reached-stage.

### Q14 ⭐⭐ 🟢 How would you show the top 5 products or regions by sales in a Power BI report?
**Asked at:** commonly asked (no company-specific report found); Telegram snippet in the sources file lists Top N tasks (low quality).
**What the interviewer is checking:** Whether you know the Top N visual filter and its limits.
**Say this in the interview:** "I put a bar chart of sales by product, then in the Filters pane set a Top N filter on product: Top 5 by the Sales measure. It stays correct as slicers change."
**Explain simply:**
- **Top N filter:** a built-in filter that keeps only the N biggest items by a chosen value.
- It recalculates for the current slicers, so the top 5 can change per region.
- Sort the bar chart descending so the biggest is on top.
- To show Others as well, see Q67.
**Example:** Eight products; Top 5 are C 300, E 210, H 180, F 150, A 120, total 960 of 1,170 (82%).
**Sample data:** Table `ProductSales`:

| Product | Sales |
|---|---|
| A | 120 |
| B | 95 |
| C | 300 |
| D | 40 |
| E | 210 |
| F | 150 |
| G | 75 |
| H | 180 |

**DAX / Steps:** Not run here. Click-path: Visualizations > Clustered bar chart > Axis = Product, Values = Sales > Filters pane > Product > Filter type Top N > Show items Top 5 > By value Sales > Apply filter.
```dax
Total Sales = SUM ( ProductSales[Sales] )
Product Rank = RANKX ( ALL ( ProductSales[Product] ), [Total Sales] )
Top 5 Sales = CALCULATE ( [Total Sales], FILTER ( VALUES ( ProductSales[Product] ), [Product Rank] <= 5 ) )
```
**Alternative:** A rank measure (above) used as a visual-level filter "is less than or equal to 5"; also usable in tables.
**Result:** Reproduced with pandas: top 5 = C, E, H, F, A; their sales 960 of 1,170 total.
**Pandas check:**
```python
p.nlargest(5,"Sales"), p.nlargest(5,"Sales").Sales.sum()   # 960, total 1170
```
Printed C 300, E 210, H 180, F 150, A 120; 960 and 1170.
**Version / licensing note:** From memory, unverified.
**Edge cases:** Ties at 5th place (Top N may include extras or cut one); RANKX with ALL ignores slicers on product but respects others only if you structure it so.
**Likely follow-ups:** 1) *Bottom 5?* Same filter, choose Bottom. 2) *Top 5 per region?* Rank within each region (use ALLEXCEPT).
**Common mistakes:** Applying Top N on the wrong field; forgetting sort; not realising totals show only visible items.

### Q15 ⭐⭐ 🟢 Which visual would you use to show monthly sales against target, and why?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Matching the visual to the message: actual versus a reference, over time.
**Say this in the interview:** "A clustered column for actual sales with a line for target, using the Line and clustered column chart, because it shows each month's gap and the trend in one view. I add achievement % in a tooltip or a table below."
**Explain simply:**
- **Columns** = actuals per month; **line** = target per month.
- Alternatives: a **bullet chart** or KPI visual for one period; a gauge only for a single month's number.
- Colour columns by whether they hit target (conditional formatting).
- Always add data labels for the key months.
**Example:** Jan 92 vs 100 (92.0%), Feb 110 vs 100 (110.0%), Mar 98 vs 105 (93.3%), Apr 125 vs 120 (104.2%). Year to date 425 vs 425, 100.0% overall even though two months missed.
**Sample data:** Table `SalesTarget` (in lakhs):

| Month | Sales | Target |
|---|---|---|
| Jan | 92 | 100 |
| Feb | 110 | 100 |
| Mar | 98 | 105 |
| Apr | 125 | 120 |

**DAX / Steps:** Not run here. Click-path: Visualizations > Line and clustered column chart > X-axis Month, Column y-axis Sales, Line y-axis Target. Measure: `Achievement % = DIVIDE ( SUM ( SalesTarget[Sales] ), SUM ( SalesTarget[Target] ) )`.
**Alternative:** KPI visual (shows value, target, trend) or a bar-in-bar for few periods.
**Result:** Reproduced with pandas: achievement 92.0, 110.0, 93.3, 104.2; variances -8, +10, -7, +5; overall 100.0%.
**Pandas check:**
```python
m["Ach%"]=(m.Sales/m.Target*100).round(1); m["Var"]=m.Sales-m.Target
```
Printed the values listed above; total ratio 100.0.
**Version / licensing note:** From memory, unverified.
**Edge cases:** Targets stored at a different grain (yearly) must be allocated; missing target months give a blank line.
**Likely follow-ups:** 1) *Why not a pie?* No time or target. 2) *Why not a gauge?* Shows a single value only.
**Common mistakes:** Dual axes with different scales; cluttered labels; target on a different unit.

### Q16 ⭐⭐ 🟢 How would you build a department-wise attendance summary showing present, absent and leave percentage?
**Asked at:** commonly asked (no company-specific report found); written for the HR reader, not seen in a source.
**What the interviewer is checking:** Counting rows by status and dividing by the right base.
**Say this in the interview:** "One row per employee per day with a status. For each department I count rows by status and divide by total marked days, using a matrix with department on rows and percentages on values."
**Explain simply:**
- **Matrix:** a pivot-style table in Power BI.
- Percentage = status days divided by all days for that department, using DIVIDE.
- Decide the base: total working days, or total rows marked (state it).
- Weekends and holidays should not count; filter them out (Q28).
**Example:** Sales has 3 attendance rows (2 present, 1 absent) so Present 66.7%, Absent 33.3%.
**Sample data:** Table `Attendance`:

| Dept | Emp | Status |
|---|---|---|
| Sales | a | Present |
| Sales | a | Absent |
| Sales | b | Present |
| IT | c | Present |
| IT | c | Leave |
| IT | d | Present |
| HR | e | Present |
| HR | e | Present |

**DAX / Steps:** Not run here.
```dax
Marked Days = COUNTROWS ( Attendance )
Present % = DIVIDE ( CALCULATE ( [Marked Days], Attendance[Status] = "Present" ), [Marked Days] )
Absent %  = DIVIDE ( CALCULATE ( [Marked Days], Attendance[Status] = "Absent" ), [Marked Days] )
Leave %   = DIVIDE ( CALCULATE ( [Marked Days], Attendance[Status] = "Leave" ), [Marked Days] )
```
Click-path: Visualizations > Matrix > Rows Dept, Values the three measures; Format > Cell elements for data bars if wanted.
**Alternative:** Put Status in matrix columns and show Values as "% of row total".
**Result:** Reproduced with pandas: HR present 100.0%; IT present 66.7%, leave 33.3%; Sales present 66.7%, absent 33.3%.
**Pandas check:**
```python
t=pd.crosstab(at.Dept,at.Status); t["Total"]=t.sum(axis=1); t["Present%"]=(t.Present/t.Total*100).round(1)
```
Printed values as listed.
**Version / licensing note:** From memory, unverified.
**Edge cases:** Half-days; missing days for absent staff (no row at all) cause inflated Present %; part-time staff.
**Likely follow-ups:** 1) *Overall total?* Total row recalculates over all rows. 2) *Late marks?* Add a status.
**Common mistakes:** Dividing by headcount instead of marked days; counting weekends; missing absent rows.

### Q17 ⭐⭐ 🟢 How do you make one slicer filter every visual on a page, and stop one visual from responding?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Knowing slicer behaviour, Edit interactions and sync slicers.
**Say this in the interview:** "A slicer filters every visual on its page by default if the field is related to the data. To stop one visual, I select the slicer, turn on Edit interactions, and click the None icon on that visual. To apply a slicer across pages I use Sync slicers."
**Explain simply:**
- **Slicer:** a filter control users click.
- **Edit interactions:** per-visual setting for Filter, Highlight, or None.
- A visual that ignores the slicer often is not related to the slicer's table (check the model).
- **Sync slicers** copies one slicer's selection across other pages.
**Example:** A Department slicer filters all charts, but the "Company total headcount" card should stay fixed; set None on the card.
**DAX / Steps:** Not run here. Click-path: select the slicer > Format tab > Edit interactions > on each other visual choose Filter (funnel icon) or None (circle slash). Sync: View tab > Sync slicers pane.
**Alternative:** Use ALL ( ) or REMOVEFILTERS inside the measure so a card always ignores the slicer.
**Version / licensing note:** From memory, unverified (menu names change between releases).
**Edge cases:** Slicer on a column from an unrelated table does nothing; hidden visuals still respond; filters pane filters differ from slicers.
**Likely follow-ups:** 1) *Slicer across pages?* Sync slicers. 2) *Keep a card unfiltered?* REMOVEFILTERS in the measure.
**Common mistakes:** Forgetting Edit interactions is per slicer; using a slicer field that is not in the model's related table.

### Q18 ⭐⭐ 🟢 A stakeholder says your dashboard is too cluttered: what would you change?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Design judgement and willingness to simplify.
**Say this in the interview:** "I ask what decision they make from it, then cut anything that does not support it: fewer visuals per page, one key message per page, consistent colours, clear titles, details moved to drill-through or tooltips, and filters tidied into a panel."
**Explain simply:**
- Keep about 5 to 7 visuals per page; split topics across pages.
- Put the most important KPIs top-left in cards.
- Use one or two colours with meaning (red only for bad).
- Remove gridlines, repeated labels, 3D and pie charts with many slices.
- Move detail to **drill-through** (a detail page opened by right-click) or **tooltip pages** (a mini-chart on hover).
**Example:** A page with 16 visuals becomes a 6-visual summary plus a detail page; viewers find the answer in seconds.
**DAX / Steps:** Not run here. Click-path: select visual > Format pane (turn off unneeded titles/gridlines); Page > duplicate > split content; Visualizations > Drill through fields.
**Alternative:** Bookmarks and buttons to toggle views on one page.
**Version / licensing note:** From memory, unverified (the Optimization guide mentions fewer visuals also helps speed, but that page was not fetched here).
**Edge cases:** Different stakeholders want different detail; create separate pages by audience.
**Likely follow-ups:** 1) *Remove without losing info?* Move it to drill-through. 2) *How do you test?* Ask a user to find a number in 10 seconds.
**Common mistakes:** Adding more explanations; shrinking visuals instead of removing; rainbow colours.

### Q19 ⭐⭐ 🟢 How would you schedule the report so the sales dashboard shows yesterday's data every morning?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Knowing scheduled refresh, gateways and timing relative to the source.
**Say this in the interview:** "After publishing, I open the semantic model settings in the Service, enter data source credentials, set a gateway if the source is on-premises, and schedule a daily refresh a bit after the source finishes its overnight load, say 6 am, with failure notifications on."
**Explain simply:**
- **Semantic model** (older name: dataset) = the data and model behind a report in the Service.
- **Gateway** = a small program on a company server that lets the cloud reach on-premises data.
- **Scheduled refresh** = a timer that reloads the data.
- Run the refresh after the source's data is ready; otherwise you load yesterday-minus-one.
- Show "last refreshed" on the report.
**Example:** Source database finishes nightly load by 3 am. Refresh at 5:30 am; managers open the dashboard at 9 am and see yesterday's sales.
**DAX / Steps:** Not run here. Click-path: Power BI Service > Workspace > semantic model > Settings > Data source credentials (sign in) > Gateway connection (if needed) > Scheduled refresh > turn On > Frequency Daily, Time, Time zone > Send refresh failure notifications > Apply.
**Alternative:** Incremental refresh (refresh only recent partitions) for large tables, or a Power Automate trigger after the source load.
**Version / licensing note:** From memory, unverified. I believe Pro allows fewer daily refreshes than Premium/Fabric capacity (commonly quoted as 8 and 48 per day) but notes in this repo flag these limits as unconfirmed; check Microsoft Learn before quoting.
**Edge cases:** Time zone settings; expired credentials; file on a personal laptop cannot refresh when it is off; a "yesterday" filter may be computed in UTC.
**Likely follow-ups:** 1) *Need hourly?* Check licence limits. 2) *Refresh fails?* Q32.
**Common mistakes:** Scheduling before the source loads; forgetting credentials; no gateway for on-premises data.

### Q20 ⭐⭐ 🟢 You are using a Mac: how can you build and publish Power BI reports?
**Asked at:** commonly asked (no company-specific report found); the Mac limitation was general knowledge in the sources file.
**What the interviewer is checking:** Awareness that Power BI Desktop is Windows-only and of the practical workarounds.
**Say this in the interview:** "Power BI Desktop runs on Windows only, so on a Mac I would use a Windows virtual machine or a cloud Windows desktop, or build in the Power BI Service in the browser, which has fewer features. Then publish from there."
**Explain simply:**
- **Desktop** is the full authoring app; I believe it is Windows-only (from memory).
- **Options:** 1) Windows in a virtual machine (Parallels or similar; Boot Camp is not available on newer Apple chips); 2) a cloud Windows PC (Windows 365 or Azure Virtual Desktop); 3) the Service in a browser: create or edit reports on an existing semantic model, with limited data modelling and Power Query.
- Publishing from the Service needs a work or school account.
**Example:** A Mac-using analyst keeps a company Windows virtual desktop to build the .pbix and uses the browser to review it.
**DAX / Steps:** Not run here. Browser path: app.powerbi.com > Workspace > New > Report (or semantic model upload) > pick data > build visuals > Save.
**Alternative:** Ask the team for a shared Windows machine, or use Excel/Power Pivot for light modelling.
**Version / licensing note:** From memory, unverified. Windows-only status, Service authoring limits and licence need to be checked on Microsoft's system-requirements and Service pages before quoting.
**Edge cases:** Some corporate policies block VMs; performance on Apple silicon VMs varies.
**Likely follow-ups:** 1) *Is there a Mac app?* Not for authoring, to my knowledge (unverified). 2) *Free licence?* Sharing needs a paid licence.
**Common mistakes:** Saying Desktop works natively on Mac; promising full modelling in the browser.

### Q21 ⭐⭐ 🟢 Your report is published but shows old data: what do you check?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** A logical checklist from refresh settings to the source.
**Say this in the interview:** "I check when the semantic model last refreshed and whether it failed, then whether a schedule exists, whether credentials or the gateway are working, whether the source itself has new data, and whether the user is viewing an old cached tile or a copy."
**Explain simply:**
- Check **Refresh history** in the Service for failures and the last time.
- Is a schedule set up and enabled? Did credentials expire?
- Is the **gateway** online?
- Is the source updated? (An old Excel file in SharePoint?)
- Is the visual fed by an **imported** copy (needs refresh) or DirectQuery (live)?
- Pinned dashboard tiles can show cached data; refresh the browser.
**Example:** Report shows Monday data on Wednesday: refresh history shows failures since Tuesday because the data-source password changed.
**DAX / Steps:** Not run here. Click-path: Service > Workspace > semantic model > Refresh > Refresh history; Settings > Scheduled refresh; Manage gateways.
**Alternative:** Add a "Last refreshed" card from a Power Query step using DateTime.LocalNow(). In the Service this is believed to return the service's time (UTC), not India time, so add 5.5 hours or label it UTC (from memory, unverified).
**Version / licensing note:** From memory, unverified.
**Edge cases:** Time zone differences; a different copy of the report (not the published one); filter on date set to last year.
**Likely follow-ups:** 1) *Fix?* Update credentials and refresh. 2) *Prevent?* Failure email alerts.
**Common mistakes:** Re-publishing instead of checking refresh; not looking at the refresh history.

### Q22 ⭐⭐ 🟢 What checks do you run on a dashboard before you release it to users?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Quality discipline: numbers, usability and access.
**Say this in the interview:** "I reconcile key totals to the source, test with filters and edge cases, check blanks and duplicates, test security as different users, check speed and layout on desktop and phone, confirm refresh works, and get a user to try it."
**Explain simply:**
- **Numbers:** compare headline totals with an independent source (Q9).
- **Filters:** click every slicer; check totals and blanks.
- **Security:** View as role (Q51).
- **Performance:** Performance Analyzer (Q8).
- **Usability:** titles, units, definitions, a last refreshed date, colour contrast.
- **Operations:** scheduled refresh succeeds; correct workspace and audience.
**Example:** Before release you find a (Blank) department of 40 people and fix the mapping, so department totals add to company headcount.
**DAX / Steps:** Not run here. Click-path: Modeling tab > View as (roles); View > Performance analyzer; Service: semantic model > Refresh now.
**Alternative:** Keep a short release checklist and a sign-off with the business owner.
**Version / licensing note:** From memory, unverified.
**Edge cases:** Different time zone users; first-time load slowness.
**Likely follow-ups:** 1) *Who signs off?* Business owner. 2) *Release process?* Dev to test to production workspace.
**Common mistakes:** Releasing without a reconciliation; testing only as the author, who sees everything.

### Q23 ⭐⭐ 🟢 How would you handle sales returns and cancellations so the dashboard shows net revenue?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you define net revenue and keep returns and cancellations out of or subtracted from sales?
**Say this in the interview:** "I agree the definition with finance, then model returns as negative lines (or a separate Returns table) and exclude cancelled orders, so Net Revenue equals gross sales plus returns, with cancellations never counted. Gross, returns and net each get a measure so the bridge is visible."
**Explain simply:**
- **Gross sales:** all valid sales lines. **Returns:** money given back, stored negative. **Cancelled:** orders that never completed, not revenue at all.
- Returns can fall in a later month than the sale; decide whether you show them in the return month (usual) or the original month.
- Keep a Type or Status column and filter on it in measures.
**Example:** Four sales lines total 14,000; one return of -1,200; one cancelled order of 2,000 is excluded. Net revenue = 12,800.
**Sample data:** Table `OrderLines`:

| Line | Type | Amount |
|---|---|---|
| 1 | Sale | 5000 |
| 2 | Sale | 3000 |
| 3 | Sale | 2000 |
| 4 | Sale | 4000 |
| 5 | Return | -1200 |
| 6 | Cancelled | 0 (original 2000) |

**DAX / Steps:** Not run here.
```dax
Gross Sales = CALCULATE ( SUM ( OrderLines[Amount] ), OrderLines[Type] = "Sale" )
Returns = CALCULATE ( SUM ( OrderLines[Amount] ), OrderLines[Type] = "Return" )
Net Revenue = [Gross Sales] + [Returns]
```
**Alternative:** One `Net Revenue = SUM ( OrderLines[Amount] )` measure if cancelled lines are zero or already removed in Power Query; filter them out upstream.
**Result:** Reproduced with pandas (DAX not run): Gross 14,000; Returns -1,200; Net 12,800; cancelled amounts excluded.
**Pandas check:**
```python
gross=o[o.Type=="Sale"].Amt.sum(); ret=o[o.Type=="Return"].Amt.sum(); print(gross, ret, gross+ret)
```
Printed 14000 -1200 12800 (return rate 8.6%).
**Version / licensing note:** From memory, unverified.
**Edge cases:** Partial returns; refunds in a later period; tax; cancelled after dispatch; currency.
**Likely follow-ups:** 1) *Return rate?* Returns divided by gross sales (here 8.6%). 2) *Which month?* Agree with finance.
**Common mistakes:** Counting cancelled orders; adding returns as positive; mixing gross and net on one chart.

### Q24 ⭐⭐ 🟢 How would you handle employees with a blank department or a missing joining date in your report?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you protect the headcount from silent data loss, and flag bad data instead of hiding it?
**Say this in the interview:** "I never drop those people. A blank department becomes an 'Unassigned' group so headcount still adds up, and a missing joining date is flagged on a data-quality list for HR to fix, and left out only of tenure calculations."
**Explain simply:**
- A blank (null) department makes a row show as "(Blank)" in charts, or vanish from a matrix, so department totals no longer add up to company headcount.
- Fix it in Power Query (the data-cleaning step before the model): replace null and empty or spaces-only text with "Unassigned". Do it once, in one place.
- A missing joining date breaks tenure, joiner counts and date relationships. Keep the row for headcount, but exclude it from tenure and show how many were excluded.
- Add a "Data issues" page or card so HR can correct the source. Cleaning the report is not a fix for the HRMS (HR system).
**Example:** 8 employees, 2 with no department, 2 with no joining date. Unassigned shows 2, so departments add up to 8; the average tenure is based on 6 people, and a card says "2 missing join dates".
**Sample data:**

Table `Employees` (blank = missing in source):

| EmpID | Dept | JoinDate |
|---|---|---|
| E1 | Sales | 2022-04-11 |
| E2 | Sales | 2023-01-05 |
| E3 | HR |  |
| E4 |  | 2021-07-19 |
| E5 | IT | 2024-02-12 |
| E6 |    | 2020-09-01 |
| E7 | IT | 2025-06-02 |
| E8 | HR |  |

**DAX / Steps (Power Query M, not run here):**
```m
// Power Query (Transform data > Employees): not run here
= Table.TransformColumns(
    Source,
    {{"Dept", each if _ = null or Text.Trim(_) = "" then "Unassigned" else Text.Trim(_), type text}}
  )
```
**DAX (not run here):**
```dax
Headcount = COUNTROWS ( Employees )
Missing Join Date = COUNTROWS ( FILTER ( Employees, ISBLANK ( Employees[JoinDate] ) ) )
Avg Tenure (Years) =
AVERAGEX (
    FILTER ( Employees, NOT ISBLANK ( Employees[JoinDate] ) ),
    DIVIDE ( DATEDIFF ( Employees[JoinDate], TODAY (), DAY ), 365.25 )
)
```
**Alternative:** Instead of "Unassigned", keep the null and filter it out (visual-level filter). Simpler, but headcount then no longer matches HR's total, so I only do this if the business agrees.
**Result (reproduced with pandas, not a DAX engine):** Unassigned 2, HR 2, IT 2, Sales 2 (total 8); missing join dates 2; average tenure 3.41 years over 6 people (reproduced with pandas, using 31-Mar-2026 as "today").
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({
 "EmpID": ["E1","E2","E3","E4","E5","E6","E7","E8"],
 "Dept": ["Sales","Sales","HR",None,"IT","  ","IT","HR"],
 "JoinDate": pd.to_datetime(["2022-04-11","2023-01-05",None,"2021-07-19","2024-02-12","2020-09-01","2025-06-02",None])})
blank = emp["Dept"].fillna("").str.strip() == ""
emp["DeptClean"] = emp["Dept"].mask(blank, "Unassigned")
print(emp.groupby("DeptClean").size().rename("Headcount"))
print("Missing join date:", emp["JoinDate"].isna().sum())
asof = pd.Timestamp("2026-03-31")
ten = ((asof - emp["JoinDate"]).dt.days / 365.25).dropna()
print("Avg tenure (rows with a date only):", round(ten.mean(), 2), "years over", len(ten), "people")
```
Printed output:
```
DeptClean
HR            2
IT            2
Sales         2
Unassigned    2
Name: Headcount, dtype: int64
Missing join date: 2
Avg tenure (rows with a date only): 3.41 years over 6 people
```
**Version / licensing note:** DAX and M are not run here. Microsoft Learn was unreachable from this session (one fetch of learn.microsoft.com was refused by the network proxy; not retried), so no Microsoft page was read. Everything here is from memory, unverified.
**Edge cases:** Empty text "" and null look the same on screen but are different; trim both. A department that exists only as "Unassigned" should not be hidden by a "remove blanks" slicer setting. Future joining dates (offer accepted, not yet joined) are valid, not errors.
**Likely follow-ups:** 1) Why not delete those rows? Headcount and payroll would silently drop real people. 2) Where do you fix the root cause? In the HR system, with a monthly list sent to the HR data owner.
**Common mistakes:** Filtering out blanks to make the chart "clean"; leaving "" and null as two different groups; using TODAY() on a missing date and getting a 100-year tenure.

### Q25 ⭐⭐ 🟡 Write a DAX measure for target achievement percentage (actual sales vs target).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you write a safe ratio, and do you know a total must be sum divided by sum, not an average of percentages?
**Say this in the interview:** "Target achievement is actual divided by target. I write it with DIVIDE so a zero or blank target does not give an error, and format it as a percentage."
**Explain simply:**
- Actual Sales and Target are two separate measures. The percentage is a third measure that divides them.
- DIVIDE(numerator, denominator) returns BLANK (or a value you choose) instead of an error when the denominator is zero.
- Because it is a measure, the grand total recalculates: total actual divided by total target, which is the correct overall figure.
- Format the measure as Percentage in Measure tools. Targets usually sit at a coarser grain (region and month) than orders, so relate both tables to a shared Region and Date table.
**Example:** North sold 350 against a target of 360 (97.2%), South 150 of 200 (75%), West 240 of 240 (100%). Company: 740 of 800 = 92.5%, not the 90.7% you get by averaging the three percentages.
**Sample data:**

Table `Sales` (one row per order line):

| Region | Month | Amount |
|---|---|---|
| North | Jan | 120 |
| North | Jan | 80 |
| North | Feb | 150 |
| South | Jan | 90 |
| South | Feb | 60 |
| West | Jan | 100 |
| West | Feb | 140 |

Table `Targets` (one row per region and month):

| Region | Month | Target |
|---|---|---|
| North | Jan | 200 |
| North | Feb | 160 |
| South | Jan | 100 |
| South | Feb | 100 |
| West | Jan | 90 |
| West | Feb | 150 |

**DAX / Steps (not run here):**
```dax
Actual Sales = SUM ( Sales[Amount] )
Target = SUM ( Targets[Target] )
Target Achievement % = DIVIDE ( [Actual Sales], [Target] )   -- format as 0.0%
```
**Alternative:** `IF ( [Target] > 0, [Actual Sales] / [Target] )` does the same but DIVIDE is shorter. Add a third argument, `DIVIDE([Actual Sales],[Target],0)`, if you want 0 rather than blank.
**Result (reproduced with pandas, not a DAX engine):** North 97.2%, South 75.0%, West 100.0%, Total 92.5%; averaging the regional percentages would wrongly give 90.7% (reproduced with pandas).
**Pandas check:**
```python
import pandas as pd
sales = pd.DataFrame({"Region":["North","North","North","South","South","West","West"],
 "Month":["Jan","Jan","Feb","Jan","Feb","Jan","Feb"],"Amount":[120,80,150,90,60,100,140]})
target = pd.DataFrame({"Region":["North","North","South","South","West","West"],
 "Month":["Jan","Feb","Jan","Feb","Jan","Feb"],"Target":[200,160,100,100,90,150]})
a = sales.groupby("Region")["Amount"].sum(); t = target.groupby("Region")["Target"].sum()
out = pd.DataFrame({"Actual":a,"Target":t}); out["Achievement %"] = (out.Actual/out.Target*100).round(1)
print(out)
print("Total achievement % (sum/sum):", round(a.sum()/t.sum()*100,1))
print("Wrong: average of region %:", round(out["Achievement %"].mean(),1))
```
Printed output:
```
        Actual  Target  Achievement %
Region                               
North      350     360           97.2
South      150     200           75.0
West       240     240          100.0
Total achievement % (sum/sum): 92.5
Wrong: average of region %: 90.7
```
**Version / licensing note:** DAX is not run here. Microsoft Learn was unreachable from this session (one fetch of learn.microsoft.com was refused by the network proxy; not retried), so no Microsoft page was read. Everything here is from memory, unverified.
**Edge cases:** Target missing for a region gives a BLANK percentage, which is honest; do not show 0%. If targets are yearly but sales are monthly, spread the target to months first. Do not put Actual and Target in one table by merging rows, or the target repeats per order.
**Likely follow-ups:** 1) Why is the total different from the average of rows? A measure divides total by total, which weights big regions properly. 2) How do you colour it red/amber/green? Conditional formatting on the card or table using the measure.
**Common mistakes:** Using `/` (errors on zero); averaging percentages; storing the target on every sales row so it adds up many times.

### Q26 ⭐⭐ 🟡 Write a DAX measure for the average tenure of employees in years.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you compute a duration row by row (an iterator) and handle people who have already left?
**Say this in the interview:** "For each employee I take days from joining date to exit date, or to today if still active, divide by 365.25, then average across employees with AVERAGEX."
**Explain simply:**
- Tenure means how long a person has worked here, here in years.
- AVERAGEX is an "iterator": it goes row by row through a table, calculates something for each row, then averages the results.
- DATEDIFF counts days between two dates. COALESCE returns the first non-blank value, so a blank exit date becomes today.
- Dividing days by 365.25 gives years (the .25 allows for leap years).
- A blank joining date must be excluded or it spoils the average.
**Example:** Five employees: 6.00, 3.25, 2.04, 1.23 years and one with no joining date. Average of the four known = 3.13 years; current employees only = 3.09 years.
**Sample data:**

Table `Employees`:

| EmpID | JoinDate | ExitDate |
|---|---|---|
| E1 | 2020-04-01 |  |
| E2 | 2022-10-01 | 2025-12-31 |
| E3 | 2024-03-15 |  |
| E4 | 2025-01-06 |  |
| E5 |  |  |

**DAX / Steps (not run here):**
```dax
Avg Tenure (Years) =
AVERAGEX (
    FILTER ( Employees, NOT ISBLANK ( Employees[JoinDate] ) ),
    DIVIDE (
        DATEDIFF ( Employees[JoinDate], COALESCE ( Employees[ExitDate], TODAY () ), DAY ),
        365.25
    )
)
```
**Alternative:** Use `DATEDIFF(..., MONTH) / 12`, simpler to explain but it counts whole months only. For current staff only, wrap the table in `FILTER(Employees, ISBLANK(Employees[ExitDate]))`.
**Result (reproduced with pandas, not a DAX engine):** All employees with a joining date: 3.13 years; current employees only: 3.09 years (reproduced with pandas, with 31-Mar-2026 standing in for TODAY()).
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"EmpID":["E1","E2","E3","E4","E5"],
 "JoinDate":pd.to_datetime(["2020-04-01","2022-10-01","2024-03-15","2025-01-06",None]),
 "ExitDate":pd.to_datetime([None,"2025-12-31",None,None,None])})
asof = pd.Timestamp("2026-03-31")           # stands in for TODAY()
end = emp["ExitDate"].fillna(asof)
emp["TenureYears"] = ((end - emp["JoinDate"]).dt.days / 365.25).round(2)
print(emp)
print("Average (blank join date skipped):", round(emp["TenureYears"].mean(),2))
cur = emp[emp.ExitDate.isna()]
print("Average, current employees only:", round(cur["TenureYears"].mean(),2))
```
Printed output:
```
  EmpID   JoinDate   ExitDate  TenureYears
0    E1 2020-04-01        NaT         6.00
1    E2 2022-10-01 2025-12-31         3.25
2    E3 2024-03-15        NaT         2.04
3    E4 2025-01-06        NaT         1.23
4    E5        NaT        NaT          NaN
Average (blank join date skipped): 3.13
Average, current employees only: 3.09
```
**Version / licensing note:** DAX is not run here. Microsoft Learn was unreachable from this session (one fetch of learn.microsoft.com was refused by the network proxy; not retried), so no Microsoft page was read. Everything here is from memory, unverified.
**Edge cases:** TODAY() changes daily, so a published number drifts; for a month-end report use a fixed as-of date from the date table. Exit date before joining date is bad data. Rehires may have two rows; decide whether tenure is continuous.
**Likely follow-ups:** 1) Why not AVERAGE on a column? There is no tenure column; the measure builds it per row. 2) How do you show tenure bands? A calculated column with SWITCH(TRUE(), ...), see the attrition-by-tenure question.
**Common mistakes:** Subtracting dates and forgetting the unit; using TODAY() for people who already left; dividing by 365 and calling it exact.

### Q27 ⭐⭐ 🟡 How do you calculate monthly attrition rate when people join and leave during the month?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know attrition needs an average headcount as denominator, and how to count joiners who leave in the same month?
**Say this in the interview:** "Monthly attrition is leavers in the month divided by average headcount, which is opening plus closing divided by two. I work out opening and closing from joining and exit dates, so someone who joins and leaves in the same month is still counted as a leaver."
**Explain simply:**
- Attrition rate means the share of people who left. "Opening headcount" is people on the first day of the month, "closing" is people on the last day.
- Using the average of the two avoids bias when many people join or leave mid-month.
- Opening: joined before month start and not exited before month start. Closing: joined by month end and not exited by month end. Leavers: exit date inside the month.
- A joiner who leaves in the same month is in leavers but in neither opening nor closing. Mention it and agree the rule with HR.
- Annual attrition is usually the sum of 12 monthly leavers divided by the average headcount of the year, not monthly % times 12 (that is only an approximation).
**Example:** March 2026: opening 27, 2 joiners, 3 leavers (one joined and left within March), closing 26. Average 26.5, attrition 3 / 26.5 = 11.3%. The sample is tiny, so the rate looks large; real monthly rates are far lower.
**Sample data:**

Table `Employees` (first 10 of 30 rows; E11 to E30 joined 2020-01-01 and are still active):

| EmpID | JoinDate | ExitDate |
|---|---|---|
| E1 | 2019-05-01 |  |
| E2 | 2020-02-10 | 2026-03-12 |
| E3 | 2021-08-01 |  |
| E4 | 2022-01-15 | 2026-02-20 |
| E5 | 2023-03-01 | 2026-03-28 |
| E6 | 2024-06-10 |  |
| E7 | 2025-11-03 |  |
| E8 | 2026-03-05 |  |
| E9 | 2026-03-09 | 2026-03-20 |
| E10 | 2018-12-01 |  |

**DAX / Steps (not run here):**
```dax
-- Date table is used only to get the month boundaries (no relationship needed)
Opening HC =
VAR MS = MIN ( 'Date'[Date] )
RETURN COUNTROWS ( FILTER ( Employees,
    Employees[JoinDate] < MS && ( ISBLANK ( Employees[ExitDate] ) || Employees[ExitDate] >= MS ) ) )

Closing HC =
VAR ME = MAX ( 'Date'[Date] )
RETURN COUNTROWS ( FILTER ( Employees,
    Employees[JoinDate] <= ME && ( ISBLANK ( Employees[ExitDate] ) || Employees[ExitDate] > ME ) ) )

Leavers =
VAR MS = MIN ( 'Date'[Date] )
VAR ME = MAX ( 'Date'[Date] )
RETURN COUNTROWS ( FILTER ( Employees,
    NOT ISBLANK ( Employees[ExitDate] ) && Employees[ExitDate] >= MS && Employees[ExitDate] <= ME ) )

Attrition % = DIVIDE ( [Leavers], DIVIDE ( [Opening HC] + [Closing HC], 2 ) )
```
**Alternative:** Use the simpler "leavers divided by opening headcount" if the company policy says so. Some companies also exclude involuntary exits; that needs an exit-type column.
**Result (reproduced with pandas, not a DAX engine):** Feb 2026: opening 28, joiners 0, leavers 1, closing 27, attrition 3.64%. Mar 2026: opening 27, joiners 2, leavers 3, closing 26, attrition 11.32% (reproduced with pandas).
**Pandas check:**
```python
import pandas as pd
rows = [("E1","2019-05-01",None),("E2","2020-02-10","2026-03-12"),("E3","2021-08-01",None),
 ("E4","2022-01-15","2026-02-20"),("E5","2023-03-01","2026-03-28"),("E6","2024-06-10",None),
 ("E7","2025-11-03",None),("E8","2026-03-05",None),("E9","2026-03-09","2026-03-20"),("E10","2018-12-01",None)]
rows += [(f"E{i}", "2020-01-01", None) for i in range(11, 31)]      # 20 more stayers
emp = pd.DataFrame(rows, columns=["EmpID","JoinDate","ExitDate"])
emp["JoinDate"] = pd.to_datetime(emp["JoinDate"]); emp["ExitDate"] = pd.to_datetime(emp["ExitDate"])
def month(ms, me):
    ms, me = pd.Timestamp(ms), pd.Timestamp(me)
    opening = ((emp.JoinDate < ms) & (emp.ExitDate.isna() | (emp.ExitDate >= ms))).sum()
    closing = ((emp.JoinDate <= me) & (emp.ExitDate.isna() | (emp.ExitDate > me))).sum()
    leavers = (emp.ExitDate.between(ms, me)).sum()
    joiners = (emp.JoinDate.between(ms, me)).sum()
    avg = (opening + closing) / 2
    return dict(Opening=opening, Joiners=joiners, Leavers=leavers, Closing=closing, AvgHC=avg, AttritionPct=round(leavers/avg*100,2))
print(pd.DataFrame({"Feb 2026": month("2026-02-01","2026-02-28"), "Mar 2026": month("2026-03-01","2026-03-31")}).T)
```
Printed output:
```
          Opening  Joiners  Leavers  Closing  AvgHC  AttritionPct
Feb 2026     28.0      0.0      1.0     27.0   27.5          3.64
Mar 2026     27.0      2.0      3.0     26.0   26.5         11.32
```
**Version / licensing note:** DAX is not run here. Variable names `MS` and `ME` are my choice; rename if the editor objects. Microsoft Learn was unreachable from this session (one fetch of learn.microsoft.com was refused by the network proxy; not retried), so no Microsoft page was read. Everything here is from memory, unverified.
**Edge cases:** In a year or quarter view MIN and MAX of the date table cover the whole period, so the same measures give period attrition. Blank exit dates must be tested with ISBLANK, since a blank compared with a date can silently be treated as 0. A rehired person needs one row per stint.
**Likely follow-ups:** 1) Why average headcount? Opening alone overstates the rate in a growing team. 2) Why not a relationship between Employees and Date? There are two date columns (join, exit), so the measure reads the boundaries instead.
**Common mistakes:** Dividing by closing headcount only; counting exit date in the next month; treating blank exit dates as zero; multiplying a monthly rate by 12 and reporting it as exact.

### Q28 ⭐⭐ 🟡 How would you count working days per employee while excluding weekends and holidays?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know DAX has no NETWORKDAYS and that a date table with a working-day flag is the standard fix?
**Say this in the interview:** "I add a Working Day flag to the date table: 1 when the day is Monday to Friday and not in a holiday list. Then I count date-table rows between each employee's start and end where the flag is 1."
**Explain simply:**
- Excel has NETWORKDAYS; DAX does not. We build the same thing from a calendar table.
- A Holidays table (company holidays, per location if needed) feeds the flag. Weekday rule: WEEKDAY(date, 2) gives Monday = 1 to Sunday = 7, so 1 to 5 are weekdays.
- The measure uses SUMX over employees so the total row adds each person, not one wide date range.
- Weekend rules differ (alternate Saturdays); put that rule in the flag, not in the measure.
**Example:** March 2026 with holidays on 4 and 19 March. E1 (1 to 31 March) = 20 working days, E2 (10 to 31 March) = 15, E3 (16 to 20 March) = 4. Total 39.
**Sample data:**

Table `Employees`:

| EmpID | StartDate | EndDate |
|---|---|---|
| E1 | 2026-03-01 | 2026-03-31 |
| E2 | 2026-03-10 | 2026-03-31 |
| E3 | 2026-03-16 | 2026-03-20 |

Table `Holidays` (fictional dates for the example):

| Date | Name |
|---|---|
| 2026-03-04 | Holiday 1 |
| 2026-03-19 | Holiday 2 |

**DAX / Steps (not run here):**
```dax
-- Calculated column in 'Date'
IsWorkingDay =
IF ( WEEKDAY ( 'Date'[Date], 2 ) <= 5 && NOT ( 'Date'[Date] IN VALUES ( Holidays[Date] ) ), 1, 0 )

-- Measure (works per employee and in the total row)
Working Days =
SUMX (
    Employees,
    CALCULATE (
        COUNTROWS ( 'Date' ),
        'Date'[IsWorkingDay] = 1,
        DATESBETWEEN ( 'Date'[Date], Employees[StartDate], Employees[EndDate] )
    )
)
```
**Alternative:** Do it in Power Query or the source SQL with a day list and filter; or, if the data is only in Excel, use `NETWORKDAYS(start, end, holidays)` there and import the number.
**Result (reproduced with pandas, not a DAX engine):** E1 = 20, E2 = 15, E3 = 4, total 39. Checked two ways in pandas (NumPy business-day count and a day-by-day calendar walk); both agree.
**Pandas check:**
```python
import pandas as pd, numpy as np
holidays = ["2026-03-04","2026-03-19"]
emp = pd.DataFrame({"EmpID":["E1","E2","E3"],"StartDate":["2026-03-01","2026-03-10","2026-03-16"],"EndDate":["2026-03-31","2026-03-31","2026-03-20"]})
emp["WorkingDays"] = [int(np.busday_count(s, (pd.Timestamp(e)+pd.Timedelta(days=1)).date(), holidays=holidays))
                      for s, e in zip(emp.StartDate, emp.EndDate)]
# independent check: walk the calendar day by day like the Date table does
cal = pd.DataFrame({"Date": pd.date_range("2026-03-01","2026-03-31")})
cal["IsWorkingDay"] = (cal.Date.dt.weekday < 5) & (~cal.Date.isin(pd.to_datetime(holidays)))
emp["Check"] = [int(cal[(cal.Date>=s)&(cal.Date<=e)].IsWorkingDay.sum()) for s, e in zip(emp.StartDate, emp.EndDate)]
print(emp); print("Total:", emp.WorkingDays.sum())
```
Printed output:
```
  EmpID   StartDate     EndDate  WorkingDays  Check
0    E1  2026-03-01  2026-03-31           20     20
1    E2  2026-03-10  2026-03-31           15     15
2    E3  2026-03-16  2026-03-20            4      4
Total: 39
```
**Version / licensing note:** DAX is not run here. Whether the measure behaves exactly as I describe (context transition inside SUMX) is from memory, unverified; test it on one employee against Excel NETWORKDAYS first. Microsoft Learn was unreachable from this session (one fetch of learn.microsoft.com was refused by the network proxy; not retried), so no Microsoft page was read. Everything here is from memory, unverified.
**Edge cases:** Start after end gives blank or zero. Holidays on a weekend are not double-removed (the flag already says 0). Leave and absence days are a separate subtraction. Multi-city companies need holiday tables per location.
**Likely follow-ups:** 1) How do you subtract approved leave? Count leave days that fall on working days and subtract. 2) Can the date table be inactive? Yes; the measure does not need a relationship.
**Common mistakes:** Counting calendar days; hard-coding holidays inside the measure; using the total row's overall MIN/MAX range.

### Q29 ⭐⭐ 🟡 How would you stop the same employee appearing twice and inflating headcount?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you diagnose duplicates (row count versus distinct count) and fix them at the source of the model, not with a patch measure?
**Say this in the interview:** "I compare row count to distinct employee IDs, find why the same ID repeats, keep one current row per employee in Power Query, and use a one-to-many relationship from a unique employee table. As a safety net the headcount measure uses DISTINCTCOUNT."
**Explain simply:**
- Duplicates usually come from a transfer history, a rehire, or an export that repeated rows. Decide what the correct unit is: one row per employee, or one per employee per period.
- In Power Query, sort by last-modified date (newest first) and remove duplicates on EmpID. That keeps the latest record.
- The employee dimension table must have a unique key, otherwise relationships go many-to-many and totals multiply.
- DISTINCTCOUNT counts different IDs. It hides the symptom but not the cause, so fix both.
**Example:** 7 rows for 5 people: Ravi (E102) appears twice after a transfer, Karan (E104) twice by repeated export. COUNTROWS says 7, true headcount 5; after keeping the latest row, IT has 2, Sales 2, HR 1.
**Sample data:**

Table `Employees` (raw export):

| EmpID | Name | Dept | ModifiedOn |
|---|---|---|---|
| E101 | Asha | Sales | 2025-01-01 |
| E102 | Ravi | Sales | 2025-01-01 |
| E102 | Ravi | IT | 2026-01-01 |
| E103 | Meena | HR | 2025-03-01 |
| E104 | Karan | IT | 2025-05-01 |
| E104 | Karan | IT | 2025-05-01 |
| E105 | Zoya | Sales | 2025-08-01 |

**DAX / Steps (Power Query M, not run here):**
```m
// Power Query: not run here
let
    Sorted  = Table.Sort(Source, {{"ModifiedOn", Order.Descending}}),
    Buffered = Table.Buffer(Sorted),                 // so the sort order is respected
    Unique  = Table.Distinct(Buffered, {"EmpID"})   // keeps the first (newest) row per EmpID
in Unique
```
**DAX (not run here):**
```dax
Headcount (safe) = DISTINCTCOUNT ( Employees[EmpID] )
Headcount (inflated) = COUNTROWS ( Employees )
```
**Alternative:** Keep the history table but add an `IsCurrent` column (1 for the latest row) and filter headcount with it. Useful when you need department-change history.
**Result (reproduced with pandas, not a DAX engine):** COUNTROWS = 7, DISTINCTCOUNT = 5; after keeping the latest row per EmpID: 5 employees (HR 1, IT 2, Sales 2). Reproduced with pandas.
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"EmpID":["E101","E102","E102","E103","E104","E104","E105"],
 "Name":["Asha","Ravi","Ravi","Meena","Karan","Karan","Zoya"],
 "Dept":["Sales","Sales","IT","HR","IT","IT","Sales"],
 "ModifiedOn":pd.to_datetime(["2025-01-01","2025-01-01","2026-01-01","2025-03-01","2025-05-01","2025-05-01","2025-08-01"])})
print("Row count (COUNTROWS):", len(emp), "| Distinct EmpID (DISTINCTCOUNT):", emp.EmpID.nunique())
clean = emp.sort_values("ModifiedOn").drop_duplicates("EmpID", keep="last")
print(clean.sort_values("EmpID").to_string(index=False))
print("Headcount after cleaning:", len(clean)); print(clean.groupby("Dept").size())
```
Printed output:
```
Row count (COUNTROWS): 7 | Distinct EmpID (DISTINCTCOUNT): 5
EmpID  Name  Dept ModifiedOn
 E101  Asha Sales 2025-01-01
 E102  Ravi    IT 2026-01-01
 E103 Meena    HR 2025-03-01
 E104 Karan    IT 2025-05-01
 E105  Zoya Sales 2025-08-01
Headcount after cleaning: 5
Dept
HR       1
IT       2
Sales    2
dtype: int64
```
**Version / licensing note:** DAX and M are not run here. That Table.Distinct keeps the first row after a sorted, buffered table is commonly relied on but from memory, unverified. Microsoft Learn was unreachable from this session (one fetch of learn.microsoft.com was refused by the network proxy; not retried), so no Microsoft page was read. Everything here is from memory, unverified.
**Edge cases:** If a transferred person must appear in both departments over time, keep both rows and count at a date. Case or spaces differences ("E102 " versus "E102") make IDs look distinct; trim and clean first. Blank IDs count as one blank group.
**Likely follow-ups:** 1) How do you find the duplicates? Group by EmpID and count rows greater than 1 in Power Query, or a table visual with the count. 2) Why not just DISTINCTCOUNT? It hides department splits and breaks relationships.
**Common mistakes:** Removing duplicates on the whole row when only a few columns differ; sorting then Remove Duplicates without buffering; ignoring that the relationship key is not unique.

### Q30 ⭐⭐ 🟡 Your model has a fact table of millions of rows and the report is slow: what do you change in the model?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you reach for model design (star schema, fewer columns, lower cardinality) before blaming DAX or hardware?
**Say this in the interview:** "I shrink and reshape the model: a star schema with a narrow fact table, remove unused columns, cut high-cardinality columns, use numeric keys, avoid calculated columns, and if it is still too big use aggregations or incremental refresh. I measure first with Performance Analyzer."
**Explain simply:**
- Cardinality means how many different values a column has; the compressed in-memory engine handles few distinct values well and many (long text, timestamps, GUIDs) badly.
- Star schema: one narrow fact table (numbers and keys) joined to small dimension tables (product, date, employee).
- Remove columns the report never uses, split date and time, round decimals, use whole-number keys.
- Create columns in Power Query or the source, not as DAX calculated columns; turn off Auto date/time.
- Aggregation tables (a pre-summarised copy used when possible) and incremental refresh (reload only recent data) help at scale. DirectQuery or composite models are the last resort.
**Example:** A 40-million-row attendance log with a punch timestamp to the second and a long text description. Split into date and time, drop the description, key the employee: file shrinks and visuals respond faster.
**DAX / Steps:** 1. Home > Transform data > check each column; delete unused ones. 2. File > Options and settings > Options > Current File > Data Load > untick Auto date/time. 3. Model view: confirm one-to-many relationships from small dimensions to the fact. 4. View > Performance analyzer to compare before and after. (Click-paths not run here; menu names may differ by build.)
**Alternative:** Keep the model but cut what each visual asks for: fewer visuals per page, Top N filters, drill-through for detail.
**Version / licensing note:** Features named (aggregations, incremental refresh, composite models) depend on licence and source: Microsoft Learn was unreachable from this session (one fetch of learn.microsoft.com was refused by the network proxy; not retried), so no Microsoft page was read. The Wave A source notes list Microsoft Learn pages on import data reduction and incremental refresh, but I did not read them here. Everything here is from memory, unverified.
**Edge cases:** Query folding (pushing steps back to the source) must be kept for incremental refresh to help. Bidirectional relationships and many-to-many slow queries. Reducing precision changes totals slightly; agree with finance.
**Likely follow-ups:** 1) How do you see what is large? DAX Studio / VertiPaq Analyzer or Tabular Editor show column sizes (external tools, from memory). 2) When would you use DirectQuery? When data must be near real time or too large to import; accept slower visuals.
**Common mistakes:** Importing every column "just in case"; one giant flat table; fixing speed with more visuals-level tweaks while the model is bloated.

### Q31 ⭐⭐ 🟡 The .pbix file has grown to 500 MB: how do you reduce its size?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you list practical size reducers in order of impact?
**Say this in the interview:** "I remove columns and rows I do not need, aggregate where detail is not used, fix data types, drop high-cardinality text, move work out of calculated columns, and consider incremental refresh. I check column sizes to see what actually dominates."
**Explain simply:**
- The .pbix file size mostly reflects the compressed data inside, so the lever is the data volume and column variety.
- Delete unused columns and old history rows (keep, say, 3 years). Filter in Power Query so the rows never load.
- Summarise to the lowest grain the report needs (daily instead of per transaction, if nobody drills down).
- Use integers instead of long text, split datetime, avoid images or large text stored in the model.
- Turn off Auto date/time (it creates a hidden date table for every date column).
**Example:** An attendance file of 30 million swipe rows. Keeping only the last 24 months, daily summary per employee, and deleting free-text remarks, takes it from about 500 MB to a fraction of that. (Illustrative; the real saving needs measuring.)
**DAX / Steps:** 1. Transform data > Choose columns / Remove columns. 2. Add a filter step on date to cut old rows. 3. Group By to summarise. 4. File > Options > Current File > Data Load > untick Auto date/time. 5. Save and compare the file size. (not run here)
**Alternative:** Keep the detail in the source with DirectQuery, or a composite model with a summarised imported table plus detail on demand.
**Version / licensing note:** Size limits for uploads and datasets depend on licence (Pro, Premium Per User, Fabric capacity): Microsoft Learn was unreachable from this session (one fetch of learn.microsoft.com was refused by the network proxy; not retried), so no Microsoft page was read. Everything here is from memory, unverified.
**Edge cases:** Removing a column used by a measure breaks that measure; test after each change. Incremental refresh keeps the Desktop file small only if you publish with a partitioned setup.
**Likely follow-ups:** 1) Does file size equal speed? Not directly, but a smaller model usually loads and queries faster. 2) Where to find the biggest columns? An external tool such as DAX Studio (from memory).
**Common mistakes:** Deleting columns that a measure or relationship needs; keeping 10 years of rows nobody opens; leaving Auto date/time on.

### Q32 ⭐⭐ 🟡 Your scheduled refresh in the Power BI service is failing: how do you troubleshoot it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you troubleshoot in a sensible order: error message, credentials, gateway, source change, timeout?
**Say this in the interview:** "I open the refresh history, read the error, then check credentials, gateway connection and the data source name, whether the source or a column changed, and whether it timed out. I fix the cause, refresh manually to confirm, then enable failure notifications."
**Explain simply:**
- Open the workspace, the semantic model (the data behind a report), then Refresh history. The failure message usually tells the category.
- Common causes: expired or changed password, gateway offline or not mapped to the source, source moved or renamed, a column or sheet renamed, timeout or capacity limits, or data now violating a type.
- A gateway is the small program that lets the cloud service reach on-premises data (for example an Excel file on a server share).
- Fix the cause, then use Refresh now to test, rather than waiting for the next scheduled time.
**Example:** Overnight refresh of the payroll report fails. Error says "credentials invalid": the service account password was rotated. Update the data source credentials in Settings, refresh now, success.
**DAX / Steps:** 1. Power BI service > Workspace > semantic model > Refresh history, read the error. 2. Settings > Data source credentials: sign in again. 3. Settings > Gateway connection: check the gateway is online and the data source is mapped. 4. Open the .pbix in Desktop and refresh to see if it works locally. 5. Refresh now, then set Refresh failure notifications. (Click-paths not run here.)
**Alternative:** If one step stopped folding or is slow, fix the query; if it is too large, move to incremental refresh.
**Version / licensing note:** Refresh frequency and time limits differ by licence (Pro versus Premium or Fabric): Microsoft Learn was unreachable from this session (one fetch of learn.microsoft.com was refused by the network proxy; not retried), so no Microsoft page was read. Everything here is from memory, unverified.
**Edge cases:** Desktop refresh working but Service failing points to credentials, gateway or privacy-level settings. Schedules in the wrong time zone confuse "yesterday's data". A refresh that succeeded with an empty source also looks fine.
**Likely follow-ups:** 1) Who gets told? Refresh failure notification emails go to the owner by default (from memory); add contacts. 2) What if a column was renamed? See the column-rename question.
**Common mistakes:** Re-publishing the file as a first reaction; not reading the error text; ignoring that the gateway machine is switched off.

### Q33 ⭐⭐ 🟡 A visual shows wrong or blank values after you add a slicer: how do you debug the measure?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand filter context: what a slicer does to a measure and what ALL, ALLSELECTED and missing relationships do?
**Say this in the interview:** "I click the slicer, then test the measure alone in a table. Common causes: the slicer's table has no relationship to the fact, the measure uses ALL which wipes the slicer filter, or the slicer value has no matching rows so the measure is BLANK. I fix the relationship or the filter function."
**Explain simply:**
- Filter context means the set of filters (slicer, row, column) that a measure sees when it calculates.
- Step 1: Drop the measure with the slicer field into a plain table; check each ingredient measure separately.
- Step 2: Check Model view for a relationship from the slicer's table to the fact table, and its direction.
- Step 3: Look for ALL, REMOVEFILTERS, ALLEXCEPT in the measure; ALL(Sales) ignores the slicer, ALLSELECTED respects it.
- Step 4: Use Performance Analyzer > Copy query, or Desktop DAX query view, to inspect the query (from memory, unverified).
**Example:** Region slicer on North. A "share of sales" measure with an ALL(Sales) denominator says North = 50%; with ALLSELECTED it says 100% of what the user selected. Neither is a bug; one answers "share of company", the other "share of selection".
**Sample data:**

Table `Sales`:

| Region | Amount |
|---|---|
| North | 300 |
| North | 200 |
| South | 150 |
| South | 150 |
| West | 200 |

**DAX / Steps (not run here):**
```dax
Total Sales = SUM ( Sales[Amount] )
Share of Company = DIVIDE ( [Total Sales], CALCULATE ( [Total Sales], ALL ( Sales ) ) )
Share of Selection = DIVIDE ( [Total Sales], CALCULATE ( [Total Sales], ALLSELECTED ( Sales ) ) )
```
**Alternative:** Use DAX query view or DAX Studio to evaluate the measure with a hard-coded filter and compare to your expectation.
**Result (reproduced with pandas, not a DAX engine):** With Region = North: share of company 50.0%, share of selection 100.0%. With nothing selected both give North 50%, South 30%, West 20%. Reproduced with pandas.
**Pandas check:**
```python
import pandas as pd
sales = pd.DataFrame({"Region":["North","North","South","South","West"],"Amount":[300,200,150,150,200]})
by = sales.groupby("Region")["Amount"].sum()
all_total = sales.Amount.sum()
print("Slicer = North")
print("Share using ALL(Sales) denominator :", round(by["North"]/all_total*100,1), "%")
sel_total = by[["North"]].sum()
print("Share using ALLSELECTED denominator:", round(by["North"]/sel_total*100,1), "%")
print("Share with nothing selected (both give):", (by/all_total*100).round(1).to_dict())
```
Printed output:
```
Slicer = North
Share using ALL(Sales) denominator : 50.0 %
Share using ALLSELECTED denominator: 100.0 %
Share with nothing selected (both give): {'North': 50.0, 'South': 30.0, 'West': 20.0}
```
**Version / licensing note:** DAX is not run here. Microsoft Learn was unreachable from this session (one fetch of learn.microsoft.com was refused by the network proxy; not retried), so no Microsoft page was read. Everything here is from memory, unverified.
**Edge cases:** A slicer on a column from a table with no relationship does nothing to the measure (everything looks "wrong"). Blank appears when no rows match, for example slicing Product on a Targets table that has no Product column. Hidden "cross-filter" settings (Edit interactions) may also stop a visual responding.
**Likely follow-ups:** 1) What is the difference between ALL and ALLSELECTED? ALL clears all filters; ALLSELECTED keeps slicer and page filters but clears the row/column ones. 2) Why total differs? Context in the total row has no row filter.
**Common mistakes:** Editing the measure before checking the model relationship; leaving ALL in a measure from a copy-paste; testing only in the card, never in a table.

### Q34 ⭐⭐ 🟡 Two tables have no usable relationship and your numbers are inflated: how do you fix it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you recognise the many-to-many or cross-join inflation and fix it with a shared dimension?
**Say this in the interview:** "Numbers inflate when two tables are joined on a column that repeats in both. I add a small dimension (for example Region) with unique values, relate both tables to it as one-to-many, and filter from the dimension. If needed I use TREATAS inside a measure."
**Explain simply:**
- A relationship is the link that lets a filter on one table affect another.
- Premise check: with no relationship at all, Power BI does not multiply anything; the inflation appears when targets are merged onto every order row (a flat table) or linked many-to-many, as in the pandas join below.
- If both tables have repeated values in the linking column (many-to-many), one target row gets matched to every order, so targets add up many times.
- Fix: create a dimension table with one row per value (Region), relate Sales and Targets to it, and use the dimension in visuals and slicers.
- TREATAS lets a measure "pretend" a column from one table filters another; good for a quick fix, but a proper model is better.
**Example:** 3 regions, targets total 1,150. Joined to 6 orders directly, North target repeats for each of 3 orders (1,500), the total becomes 2,450. Through a Region dimension it stays 1,150.
**Sample data:**

Table `Sales`:

| OrderID | Region | Amount |
|---|---|---|
| 1 | North | 100 |
| 2 | North | 200 |
| 3 | North | 300 |
| 4 | South | 150 |
| 5 | South | 50 |
| 6 | West | 400 |

Table `Targets`:

| Region | Target |
|---|---|
| North | 500 |
| South | 300 |
| West | 350 |

**DAX / Steps (not run here):**
```dax
Region = DISTINCT ( UNION ( VALUES ( Sales[Region] ), VALUES ( Targets[Region] ) ) )   -- calculated table

Target (no relationship) =
CALCULATE ( SUM ( Targets[Target] ), TREATAS ( VALUES ( Sales[Region] ), Targets[Region] ) )
```
**Alternative:** Aggregate the fact first (summarise Sales to region) in Power Query and relate on the unique key. Or build the dimension in Power Query by combining the unique Region values from both tables.
**Result (reproduced with pandas, not a DAX engine):** Correct target total 1,150; direct join per order gives North 1,500 + South 600 + West 350 = 2,450 (inflated); via a Region dimension 1,150. Reproduced with pandas.
**Pandas check:**
```python
import pandas as pd
sales = pd.DataFrame({"OrderID":[1,2,3,4,5,6],"Region":["North","North","North","South","South","West"],"Amount":[100,200,300,150,50,400]})
target = pd.DataFrame({"Region":["North","South","West"],"Target":[500,300,350]})
print("Correct target total:", target.Target.sum())
joined = sales.merge(target, on="Region")          # what a many-to-many / cross join does: target repeats per order
print(joined.groupby("Region").agg(Orders=("OrderID","count"), Target=("Target","sum")))
print("Inflated target total:", joined.Target.sum())
region = pd.DataFrame({"Region":["North","South","West"]})
fixed = target.merge(region, on="Region").Target.sum()
print("Via one Region dimension, each side filtered once:", fixed)
```
Printed output:
```
Correct target total: 1150
        Orders  Target
Region                
North        3    1500
South        2     600
West         1     350
Inflated target total: 2450
Via one Region dimension, each side filtered once: 1150
```
**Version / licensing note:** DAX is not run here. Many-to-many relationship support differs between Desktop and Service and by model type; I did not verify it here. Microsoft Learn was unreachable from this session (one fetch of learn.microsoft.com was refused by the network proxy; not retried), so no Microsoft page was read. Everything here is from memory, unverified.
**Edge cases:** Mismatched spellings ("North " versus "North") break the dimension; clean first. A calculated-table dimension via DAX refreshes with the model but cannot be filtered at the source. Bidirectional filtering can make it worse.
**Likely follow-ups:** 1) Why not a many-to-many relationship? It works but hides inflation; the dimension is clearer. 2) What if the grain differs (monthly targets, daily sales)? Relate both to Date at their own grain.
**Common mistakes:** Switching the relationship to "both directions" to make it look right; summing a repeated target; using the fact table as the slicer source.

### Q35 ⭐⭐ 🟡 A chart shows a (Blank) category: what does it mean and how do you fix it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know (Blank) comes from null keys or orphan keys, and that it is a model problem, not a chart problem?
**Say this in the interview:** "(Blank) means some rows have no matching category: either the key is empty, or it exists in the fact table but not in the dimension. I find those rows, fix or add the missing dimension row, and keep an Unknown row so totals still reconcile."
**Explain simply:**
- The fact table has a key (ProductID); the dimension has the category. If the key is missing from the dimension (an orphan) the category shows as (Blank).
- Power BI keeps these rows in totals, grouped under a blank, so totals are right but the breakdown is not.
- Find them: a table of Sales with ProductID where the related Category is blank, or a Power Query merge showing non-matching rows.
- Fix at the source, or add an "Unknown" dimension row and map orphan keys to it, rather than hiding the Blank with a filter.
**Example:** Orders worth 200 have product P9 (not in the Product table) or no product at all. The chart shows Laptop 500, Phone 500, (Blank) 200; total 1,200 is intact.
**Sample data:**

Table `Product`:

| ProductID | Category |
|---|---|
| P1 | Laptop |
| P2 | Phone |
| P3 | Phone |

Table `Sales`:

| OrderID | ProductID | Amount |
|---|---|---|
| 1 | P1 | 500 |
| 2 | P2 | 300 |
| 3 | P3 | 200 |
| 4 | P9 | 150 |
| 5 |  | 50 |

**DAX / Steps (Power Query M, not run here):**
```m
// Power Query: find orphans (Home > Merge Queries as New, Left Anti join on ProductID): not run here
= Table.NestedJoin(Sales, {"ProductID"}, Product, {"ProductID"}, "P", JoinKind.LeftAnti)
```
**Alternative:** In the model view, use a visual-level filter "Category is not blank" only when the business says those rows are junk, and say the total will no longer match.
**Result (reproduced with pandas, not a DAX engine):** (Blank) 200, Laptop 500, Phone 500; the orphan key is P9 and there is 1 null key. Reproduced with pandas.
**Pandas check:**
```python
import pandas as pd
product = pd.DataFrame({"ProductID":["P1","P2","P3"],"Category":["Laptop","Phone","Phone"]})
sales = pd.DataFrame({"OrderID":[1,2,3,4,5],"ProductID":["P1","P2","P3","P9",None],"Amount":[500,300,200,150,50]})
m = sales.merge(product, on="ProductID", how="left")
print(m.assign(Category=m.Category.fillna("(Blank)")).groupby("Category")["Amount"].sum())
print("Orphan keys (not in Product):", sorted(set(sales.ProductID.dropna()) - set(product.ProductID)))
print("Null keys in Sales:", sales.ProductID.isna().sum())
```
Printed output:
```
Category
(Blank)    200
Laptop     500
Phone      500
Name: Amount, dtype: int64
Orphan keys (not in Product): ['P9']
Null keys in Sales: 1
```
**Version / licensing note:** M and click-path are not run here. Microsoft Learn was unreachable from this session (one fetch of learn.microsoft.com was refused by the network proxy; not retried), so no Microsoft page was read. Everything here is from memory, unverified.
**Edge cases:** A null key and an orphan key both show as Blank, but the cures differ. A relationship with "assume referential integrity" off keeps them as blank; on, they can disappear in DirectQuery. Text categories that are empty strings show as a blank-looking bar, not (Blank).
**Likely follow-ups:** 1) Is the total wrong? No, the blank rows are still counted. 2) How do you stop it recurring? Validate keys in Power Query on every refresh.
**Common mistakes:** Hiding (Blank) with a filter so the chart no longer adds to the KPI; deleting rows; blaming the visual.

### Q36 ⭐⭐ 🟡 How do you build a proper date table, and why does a sales dashboard need one?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you build a contiguous date table, mark it, and know time intelligence needs it?
**Say this in the interview:** "A proper date table has one row for every day with no gaps, from the first to the last year in the data, with year, month and fiscal columns, related to the fact date and marked as the date table. Time-intelligence functions like YTD and same-period-last-year need it."
**Explain simply:**
- A date table is a separate table listing each calendar day once, so months and years sort and filter properly.
- Rules (from memory, unverified): unique dates, no blanks, no gaps, and it should cover full years. Mark it with Table tools > Mark as date table.
- Without a proper date table, functions such as TOTALYTD or SAMEPERIODLASTYEAR can give wrong or blank results (from memory, unverified), and month names sort alphabetically (April before January).
- Build it once in DAX (CALENDAR), or Power Query, and relate Date[Date] to Sales[OrderDate] (one-to-many). Use Sort by column for month names.
- Turn off Auto date/time so you do not get hidden duplicate tables.
**Example:** Sales from Jan 2025 to Dec 2026: the calendar has 730 rows, one per day, with unique and contiguous dates; Year, Month, YearMonth and DayOfWeek columns.
**Sample data:** One column, `Sales[OrderDate]`, with orders from 1 Jan 2025 to 31 Dec 2026 (illustrative; the pandas check builds the calendar directly).
**DAX / Steps (not run here):**
```dax
Date =
VAR StartDate = DATE ( YEAR ( MIN ( Sales[OrderDate] ) ), 1, 1 )
VAR EndDate  = DATE ( YEAR ( MAX ( Sales[OrderDate] ) ), 12, 31 )
RETURN
ADDCOLUMNS (
    CALENDAR ( StartDate, EndDate ),
    "Year", YEAR ( [Date] ),
    "MonthNo", MONTH ( [Date] ),
    "Month", FORMAT ( [Date], "MMM" ),
    "YearMonth", FORMAT ( [Date], "yyyy-MM" )
)
```
**Click-path:** 1. Modeling > New table > paste DAX. 2. Select Month, Sort by column > MonthNo. 3. Model view: drag Date[Date] to Sales[OrderDate]. 4. Select the table > Table tools > Mark as date table > choose Date. (Click-path not run here.)
**Alternative:** CALENDARAUTO() builds the range from the whole model but may extend to odd dates; or create the table in Power Query with List.Dates and import it.
**Result (reproduced with pandas, not a DAX engine):** 730 rows (2025 and 2026), dates unique, no nulls, contiguous; the rows at positions 0, 31 and 365 are 2025-01-01, 2025-02-01 and 2026-01-01. Reproduced with pandas.
**Pandas check:**
```python
import pandas as pd
d = pd.DataFrame({"Date": pd.date_range("2025-01-01","2026-12-31")})
d["Year"] = d.Date.dt.year; d["MonthNo"] = d.Date.dt.month; d["Month"] = d.Date.dt.strftime("%b")
d["YearMonth"] = d.Date.dt.strftime("%Y-%m"); d["DayOfWeek"] = d.Date.dt.weekday + 1   # Mon=1 like WEEKDAY(,2)
print("Rows:", len(d), "| unique dates:", d.Date.is_unique, "| nulls:", int(d.Date.isna().sum()))
print("Contiguous (every gap = 1 day):", bool((d.Date.diff().dropna() == pd.Timedelta(days=1)).all()))
print(d.iloc[[0, 31, 365]].to_string(index=False))
```
Printed output:
```
Rows: 730 | unique dates: True | nulls: 0
Contiguous (every gap = 1 day): True
      Date  Year  MonthNo Month YearMonth  DayOfWeek
2025-01-01  2025        1   Jan   2025-01          3
2025-02-01  2025        2   Feb   2025-02          6
2026-01-01  2026        1   Jan   2026-01          4
```
**Version / licensing note:** DAX and click-path are not run here. Microsoft Learn was unreachable from this session (one fetch of learn.microsoft.com was refused by the network proxy; not retried), so no Microsoft page was read. Everything here is from memory, unverified.
**Edge cases:** If the fact has a datetime, relate on the date part only. Multiple date columns in the fact (order, ship): one active relationship, others inactive and activated in measures. Future-dated rows beyond the table's end date vanish from time views.
**Likely follow-ups:** 1) CALENDAR versus CALENDARAUTO? CALENDAR takes a start and end you choose; CALENDARAUTO reads the model. 2) Why not use Auto date/time? One hidden table per date column; inflexible and harder to control.
**Common mistakes:** Using the fact's date column directly for time intelligence; leaving gaps; forgetting Sort by column; not marking the table.

### Q37 ⭐⭐ 🟡 How would you handle an April-to-March fiscal year in a sales or HR dashboard?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you build Indian fiscal-year columns and make YTD respect a 31 March year end?
**Say this in the interview:** "I add fiscal columns to the date table: FY label, fiscal month number (April = 1), and use a year-end of 31 March in YTD measures, so FY2026-27 runs April 2026 to March 2027."
**Explain simply:**
- FY means financial year. In India it usually runs 1 April to 31 March; January to March belong to the FY that started the previous April.
- Fiscal start year = year if month >= 4, else year - 1. Label "FY2026-27" is easy to read.
- Fiscal month number = MOD(month - 4, 12) + 1 (April 1, March 12). Use Sort by column so months run April to March.
- TOTALYTD and DATESYTD accept an optional year-end date such as "3/31" so YTD resets on 1 April.
- Same logic works for HR (headcount by FY, attrition per FY).
**Example:** 1 April 2026 is month 1 of FY2026-27; 10 January 2027 is month 10 of FY2026-27; 31 March 2026 belongs to FY2025-26. Sales of 570 from April 2026 to 28 Feb 2027 is the FY YTD, not the 120 you would get from calendar 2027.
**Sample data:** Five dates (31-Mar-2026, 1-Apr-2026, 15-Dec-2026, 10-Jan-2027, 31-Mar-2027) and `Sales` rows: 10-Apr-2026 100, 5-Jun-2026 150, 20-Dec-2026 200, 14-Feb-2027 120, 2-Apr-2027 90.
**DAX / Steps (not run here):**
```dax
-- Calculated columns in 'Date'
FY Start Year = IF ( MONTH ( 'Date'[Date] ) >= 4, YEAR ( 'Date'[Date] ), YEAR ( 'Date'[Date] ) - 1 )
FY = "FY" & 'Date'[FY Start Year] & "-" & RIGHT ( 'Date'[FY Start Year] + 1, 2 )
Fiscal Month No = MOD ( MONTH ( 'Date'[Date] ) - 4, 12 ) + 1

-- Measure
Sales FY YTD = TOTALYTD ( [Sales], 'Date'[Date], "3/31" )
```
**Alternative:** Power Query version: add a custom column with `if Date.Month([Date]) >= 4 then Date.Year([Date]) else Date.Year([Date]) - 1`. Or `DATESYTD('Date'[Date], "31-Mar")` style year-end text; the exact accepted formats depend on locale, so test.
**Result (reproduced with pandas, not a DAX engine):** 31-Mar-2026 FY2025-26 month 12; 01-Apr-2026 FY2026-27 month 1; 15-Dec-2026 month 9; 10-Jan-2027 month 10; 31-Mar-2027 month 12. FY YTD to 28-Feb-2027 = 570 versus 120 for calendar-year 2027. Reproduced with pandas.
**Pandas check:**
```python
import pandas as pd
d = pd.DataFrame({"Date": pd.to_datetime(["2026-03-31","2026-04-01","2026-12-15","2027-01-10","2027-03-31"])})
m = d.Date.dt.month; y = d.Date.dt.year
d["FYStartYear"] = (y).where(m >= 4, y - 1)
d["FY"] = "FY" + d.FYStartYear.astype(str) + "-" + (d.FYStartYear + 1).astype(str).str[-2:]
d["FiscalMonthNo"] = (m - 4) % 12 + 1
print(d.to_string(index=False))
sales = pd.DataFrame({"Date": pd.to_datetime(["2026-04-10","2026-06-05","2026-12-20","2027-02-14","2027-04-02"]),"Amt":[100,150,200,120,90]})
asof = pd.Timestamp("2027-02-28"); fy_start = pd.Timestamp("2026-04-01")
print("FY2026-27 YTD to 28-Feb-2027:", sales[(sales.Date>=fy_start)&(sales.Date<=asof)].Amt.sum())
print("Calendar-year 2027 YTD (wrong for FY):", sales[(sales.Date>='2027-01-01')&(sales.Date<=asof)].Amt.sum())
```
Printed output:
```
      Date  FYStartYear        FY  FiscalMonthNo
2026-03-31         2025 FY2025-26             12
2026-04-01         2026 FY2026-27              1
2026-12-15         2026 FY2026-27              9
2027-01-10         2026 FY2026-27             10
2027-03-31         2026 FY2026-27             12
FY2026-27 YTD to 28-Feb-2027: 570
Calendar-year 2027 YTD (wrong for FY): 120
```
**Version / licensing note:** DAX is not run here. The year-end argument format ("3/31") and its locale dependence are from memory, unverified. Microsoft Learn was unreachable from this session (one fetch of learn.microsoft.com was refused by the network proxy; not retried), so no Microsoft page was read. Everything here is from memory, unverified.
**Edge cases:** Sort FY label and Fiscal Month No properly. A 52-week retail calendar is different. Companies with an October year end need their own constant. Budgets keyed by FY label must use the same text.
**Likely follow-ups:** 1) How do you compare with last FY? SAMEPERIODLASTYEAR still works on the date table. 2) Why not just filter April to March? YTD and sorting would still be wrong.
**Common mistakes:** Using calendar Year as FY; sorting months alphabetically; hard-coding "FY2026" in measures.

### Q38 ⭐⭐ 🟡 The Excel pivot report is being replaced by Power BI: how do you migrate it and prove the numbers match?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you have a systematic migration and reconciliation plan instead of eyeballing totals?
**Say this in the interview:** "I list every number and filter in the Excel pivot, rebuild them as measures from the same source, then compare totals and row-level breakdowns side by side, investigating every difference until it is explained and signed off by the report owner."
**Explain simply:**
- Start by documenting the pivot: source, filters, calculated fields, grouping, number formats, refresh process.
- Rebuild with a clean model (fact plus dimensions) and one measure per number the pivot shows.
- Reconcile in layers: row counts first, then grand total, then by department, then by month. Differences are found fastest at the lowest level where they appear.
- Typical gaps: hidden filters in the pivot, text-numbers in Excel, duplicates, date or time zone cut-offs, blanks, and pivot totals of averages.
- Run both in parallel for one or two cycles and keep a sign-off note.
**Example:** Excel pivot versus Power BI by department: only IT differs, 845,000 versus 830,000 (diff 15,000). Drill into IT: 15,000 turns out to be one duplicated invoice that the Excel pivot filtered out manually.
**Sample data:**

Comparison table (Excel pivot versus Power BI):

| Dept | ExcelPivot | PowerBI | Diff |
|---|---|---|---|
| Sales | 1250000 | 1250000 | 0 |
| HR | 0 | 0 | 0 |
| IT | 830000 | 845000 | 15000 |
| Finance | 410000 | 410000 | 0 |

**DAX / Steps:** 1. Document the pivot (filters, grouping, calculated fields). 2. Build model and measures. 3. Table visual with the same rows as the pivot; Export data or Analyze in Excel (feature availability from memory, unverified) to compare. 4. Reconcile row counts, then totals, then each difference. 5. Parallel run, sign-off, retire the pivot. (Click-paths not run here.)
**Alternative:** Place the Power BI result in Excel with Analyze in Excel (connected pivot on the semantic model) so users keep the familiar pivot but on a trusted model.
**Result (reproduced with pandas, not a DAX engine):** IT differs by 15,000; the grand total difference is 15,000; every other department matches. Reproduced with pandas on illustrative numbers.
**Pandas check:**
```python
import pandas as pd
excel = pd.Series({"Sales":1250000,"HR":0,"IT":830000,"Finance":410000}, name="ExcelPivot")
pbi   = pd.Series({"Sales":1250000,"HR":0,"IT":845000,"Finance":410000}, name="PowerBI")
cmp = pd.concat([excel, pbi], axis=1); cmp["Diff"] = cmp.PowerBI - cmp.ExcelPivot
print(cmp); print("Grand total diff:", cmp.Diff.sum()); print("Rows to investigate:", list(cmp.index[cmp.Diff != 0]))
```
Printed output:
```
         ExcelPivot  PowerBI   Diff
Sales       1250000  1250000      0
HR                0        0      0
IT           830000   845000  15000
Finance      410000   410000      0
Grand total diff: 15000
Rows to investigate: ['IT']
```
**Version / licensing note:** Microsoft Learn was unreachable from this session (one fetch of learn.microsoft.com was refused by the network proxy; not retried), so no Microsoft page was read. Everything here is from memory, unverified.
**Edge cases:** Rounding (display versus stored decimals), time zones, pivot "Show values as" settings, and blank handling often explain small differences. Never "fix" by plugging a number.
**Likely follow-ups:** 1) How do you prove it to the business? A reconciliation sheet with each total from both, difference and reason. 2) What if Excel is wrong? Document it and get the owner to agree before the switch.
**Common mistakes:** Comparing only the grand total; forgetting hidden filters; migrating the logic but not the data cleaning steps.

### Q39 ⭐⭐ 🟡 How would you build a payroll cost dashboard (gross, deductions, net by department and month)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you model payroll as gross minus deductions at the right grain, with totals that reconcile?
**Say this in the interview:** "I keep payroll as a fact table at employee and month grain, build Gross and Deductions as sums, and Net as Gross minus Deductions, then slice by department and month from the dimension and date tables."
**Explain simply:**
- Gross pay is total earnings before deductions; deductions are items like PF (provident fund) and income tax; net is what the employee receives.
- Net should be a measure (Gross - Deductions), not summed from a column, so totals stay consistent.
- Relate payroll to an employee/department dimension and a date table; show a matrix of department by month, a trend line and a top-cost list.
- Restrict payroll access with row-level security or a hidden page; payroll data is highly sensitive.
**Example:** April: IT gross 160,000, deductions 30,600, net 129,400. Company total over the sample: gross 387,000, deductions 65,950, net 321,050.
**Sample data:**

Table `Payroll`:

| EmpID | Dept | Month | Gross | Deductions |
|---|---|---|---|---|
| E1 | IT | Apr | 90000 | 18000 |
| E2 | IT | Apr | 70000 | 12600 |
| E3 | HR | Apr | 50000 | 7500 |
| E4 | HR | May | 52000 | 7800 |
| E5 | Sales | Apr | 60000 | 9000 |
| E6 | Sales | May | 65000 | 11050 |

**DAX / Steps (not run here):**
```dax
Gross = SUM ( Payroll[Gross] )
Deductions = SUM ( Payroll[Deductions] )
Net Pay = [Gross] - [Deductions]
Deduction % = DIVIDE ( [Deductions], [Gross] )
```
**Alternative:** If the source has one row per pay component (basic, HRA, PF...), unpivot or use a component dimension and a sign column, then Gross = SUM of earning rows.
**Result (reproduced with pandas, not a DAX engine):** HR Apr 50,000 / 7,500 / 42,500; HR May 52,000 / 7,800 / 44,200; IT Apr 160,000 / 30,600 / 129,400; Sales Apr 60,000 / 9,000 / 51,000; Sales May 65,000 / 11,050 / 53,950; grand total 387,000 / 65,950 / 321,050 (gross / deductions / net). Reproduced with pandas.
**Pandas check:**
```python
import pandas as pd
p = pd.DataFrame({"EmpID":["E1","E2","E3","E4","E5","E6"],"Dept":["IT","IT","HR","HR","Sales","Sales"],
 "Month":["Apr","Apr","Apr","May","Apr","May"],"Gross":[90000,70000,50000,52000,60000,65000],"Deductions":[18000,12600,7500,7800,9000,11050]})
g = p.groupby(["Dept","Month"])[["Gross","Deductions"]].sum()
g["Net"] = g.Gross - g.Deductions; print(g)
print("Grand total:", g.sum().to_dict())
```
Printed output:
```
              Gross  Deductions     Net
Dept  Month                            
HR    Apr     50000        7500   42500
      May     52000        7800   44200
IT    Apr    160000       30600  129400
Sales Apr     60000        9000   51000
      May     65000       11050   53950
Grand total: {'Gross': 387000, 'Deductions': 65950, 'Net': 321050}
```
**Version / licensing note:** DAX is not run here. Row-level security availability by licence is from memory, unverified. Microsoft Learn was unreachable from this session (one fetch of learn.microsoft.com was refused by the network proxy; not retried), so no Microsoft page was read. Everything here is from memory, unverified.
**Edge cases:** Employer contributions are a cost to company but not in the employee's gross; define "payroll cost". Reversals and arrears can be negative. Mid-month joiners are part-paid; do not average blindly.
**Likely follow-ups:** 1) Who may see this? Restrict by role (RLS) and keep individual salaries out of general reports. 2) Net or CTC? Clarify: CTC (cost to company) includes employer costs.
**Common mistakes:** Summing net from a column that is not additive; mixing employee and employer contributions; showing individual pay without access control.

### Q40 ⭐⭐ 🟡 How would you analyse why employees leave, by tenure band, department and manager?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you segment attrition by band, department and manager, and watch for small numbers and survivor bias?
**Say this in the interview:** "I add a tenure band to each employee, then compute exit rate for each band, department and manager with the same measure, and look for where it clusters. I also check group sizes so I do not over-read small teams."
**Explain simply:**
- Tenure band: group people by time at the company, measured at exit for leavers and today for stayers (for example under 1 year, 1 to 3, 3+).
- Use one exit-rate measure and let the visual slice by band, department and manager so numbers are comparable.
- Add a second view: reason for leaving and manager-level counts with a minimum group size.
- Correlation is not cause: compare to the company average and avoid blaming a manager on 3 people.
**Example:** Of 10 employees, 4 left within a year (100% of that band), 2 of 3 in 1 to 3 years, none among 3+ years. IT 75%, Sales 50%, HR 50%. The sample is too small to conclude anything; in practice we want a larger base.
**Sample data:**

Table `Employees`:

| EmpID | Dept | Manager | JoinDate | ExitDate |
|---|---|---|---|---|
| E1 | IT | Mehta | 2022-01-10 | 2023-02-01 |
| E2 | IT | Mehta | 2024-05-02 | 2024-11-15 |
| E3 | IT | Rao | 2019-03-01 |  |
| E4 | Sales | Rao | 2025-01-06 | 2025-09-30 |
| E5 | Sales | Nair | 2023-07-01 | 2025-12-31 |
| E6 | Sales | Nair | 2020-08-01 |  |
| E7 | HR | Nair | 2024-09-01 | 2025-03-10 |
| E8 | HR | Mehta | 2018-04-01 |  |
| E9 | IT | Rao | 2025-02-03 | 2025-08-20 |
| E10 | Sales | Mehta | 2024-10-01 |  |

**DAX / Steps (not run here):**
```dax
Tenure Years (column) =
DIVIDE ( DATEDIFF ( Employees[JoinDate], COALESCE ( Employees[ExitDate], DATE ( 2026, 3, 31 ) ), DAY ), 365.25 )

Tenure Band (column) =
SWITCH ( TRUE (), Employees[Tenure Years] < 1, "<1 yr", Employees[Tenure Years] < 3, "1-3 yrs", "3+ yrs" )

Leavers = CALCULATE ( COUNTROWS ( Employees ), NOT ISBLANK ( Employees[ExitDate] ) )
People = COUNTROWS ( Employees )
Exit Rate % = DIVIDE ( [Leavers], [People] )
```
**Alternative:** Use a decomposition tree or key influencers visual to explore the drivers. For a proper rate use average headcount per group instead of a simple count.
**Result (reproduced with pandas, not a DAX engine):** By band: under 1 year 4 of 4 left (100%), 1-3 years 2 of 3 (66.7%), 3+ years 0 of 3. By department: HR 50%, IT 75%, Sales 50%. By manager: Mehta 50%, Nair 66.7%, Rao 66.7%. Reproduced with pandas.
**Pandas check:**
```python
import pandas as pd
rows = [("E1","IT","Mehta","2022-01-10","2023-02-01"),("E2","IT","Mehta","2024-05-02","2024-11-15"),
 ("E3","IT","Rao","2019-03-01",None),("E4","Sales","Rao","2025-01-06","2025-09-30"),
 ("E5","Sales","Nair","2023-07-01","2025-12-31"),("E6","Sales","Nair","2020-08-01",None),
 ("E7","HR","Nair","2024-09-01","2025-03-10"),("E8","HR","Mehta","2018-04-01",None),
 ("E9","IT","Rao","2025-02-03","2025-08-20"),("E10","Sales","Mehta","2024-10-01",None)]
e = pd.DataFrame(rows, columns=["EmpID","Dept","Manager","JoinDate","ExitDate"])
e["JoinDate"]=pd.to_datetime(e.JoinDate); e["ExitDate"]=pd.to_datetime(e.ExitDate)
e["Left"] = e.ExitDate.notna()
asof = pd.Timestamp("2026-03-31")
e["TenureYears"] = ((e.ExitDate.fillna(asof) - e.JoinDate).dt.days/365.25)
e["Band"] = pd.cut(e.TenureYears, [-1,1,3,100], labels=["<1 yr","1-3 yrs","3+ yrs"], right=False)
for k in ["Band","Dept","Manager"]:
    g = e.groupby(k, observed=True).agg(People=("EmpID","count"), Leavers=("Left","sum"))
    g["Exit rate %"] = (g.Leavers/g.People*100).round(1); print(g, "\n")
```
Printed output:
```
         People  Leavers  Exit rate %
Band                                 
<1 yr         4        4        100.0
1-3 yrs       3        2         66.7
3+ yrs        3        0          0.0 

       People  Leavers  Exit rate %
Dept                               
HR          2        1         50.0
IT          4        3         75.0
Sales       4        2         50.0 

         People  Leavers  Exit rate %
Manager                              
Mehta         4        2         50.0
Nair          3        2         66.7
Rao           3        2         66.7 
```
**Version / licensing note:** DAX is not run here. Availability of decomposition tree and key influencers by licence is from memory, unverified. Microsoft Learn was unreachable from this session (one fetch of learn.microsoft.com was refused by the network proxy; not retried), so no Microsoft page was read. Everything here is from memory, unverified.
**Edge cases:** Stayers' tenure is still growing, so young bands look worse; compare against a cohort rate for the same time window. Small groups produce extreme percentages. Hard-coded as-of date should become a parameter.
**Likely follow-ups:** 1) How do you avoid bias? Use the same period, a minimum group size and cohort survival. 2) Regretted attrition? Needs a flag from HR for good performers.
**Common mistakes:** Comparing band rates without noting the group size; blaming a manager from tiny numbers; bands computed with today's date for leavers.

### Q41 ⭐⭐ 🟡 How would you show current month against previous month with an up or down indicator?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you do a month-on-month comparison with DATEADD and display it with a clear indicator?
**Say this in the interview:** "A previous-month measure with DATEADD, a percentage change with DIVIDE, and a small measure that returns an up or down arrow, which I use in a card or table with conditional formatting."
**Explain simply:**
- DATEADD shifts the dates in the current filter by one month back, so [Sales] is evaluated for the previous month. It needs a proper date table.
- Change % = (current - previous) / previous. DIVIDE avoids errors if previous is zero or blank.
- The arrow: a text measure; colour it using Format > Conditional formatting > Font colour > Field value.
- Show the current month on the card with the percentage as a smaller subtitle.
**Example:** Sales: Jan 400, Feb 380, Mar 456, Apr 456. Feb is down 5%, Mar up 20%, Apr flat 0%. Jan has no previous month, so it shows blank rather than a misleading number.
**Sample data:**

Monthly Sales (from the Sales measure):

| Month | Sales |
|---|---|
| Jan | 400 |
| Feb | 380 |
| Mar | 456 |
| Apr | 456 |

**DAX / Steps (not run here):**
```dax
Sales PM = CALCULATE ( [Sales], DATEADD ( 'Date'[Date], -1, MONTH ) )
MoM % = DIVIDE ( [Sales] - [Sales PM], [Sales PM] )
MoM Icon = IF ( ISBLANK ( [MoM %] ), "", IF ( [MoM %] > 0, "▲", IF ( [MoM %] < 0, "▼", "▬" ) ) )
```
**Alternative:** Use `PREVIOUSMONTH` instead of DATEADD; or the built-in Card (new) / KPI visual which shows a trend and a goal. Add a conditional format from the field value for colour.
**Result (reproduced with pandas, not a DAX engine):** Feb -5.0% (DOWN), Mar +20.0% (UP), Apr 0.0% (FLAT), Jan blank. Reproduced with pandas.
**Pandas check:**
```python
import pandas as pd
s = pd.Series({"Jan":400,"Feb":380,"Mar":456,"Apr":456}, name="Sales")
out = pd.DataFrame({"Sales":s,"PrevMonth":s.shift(1)})
out["Change %"] = ((out.Sales/out.PrevMonth-1)*100).round(1)
out["Icon"] = out["Change %"].apply(lambda x: "n/a" if pd.isna(x) else ("UP" if x>0 else ("DOWN" if x<0 else "FLAT")))
print(out)
```
Printed output:
```
     Sales  PrevMonth  Change %  Icon
Jan    400        NaN       NaN   n/a
Feb    380      400.0      -5.0  DOWN
Mar    456      380.0      20.0    UP
Apr    456      456.0       0.0  FLAT
```
**Version / licensing note:** DAX is not run here. Visual names and options in the current Desktop (Card, KPI, conditional formatting) are from memory, unverified. Microsoft Learn was unreachable from this session (one fetch of learn.microsoft.com was refused by the network proxy; not retried), so no Microsoft page was read. Everything here is from memory, unverified.
**Edge cases:** DATEADD works with full months only if the date table covers them; partial months compare badly (day 15 of month versus full prior month). Use MTD versus same days. If a year has different working days, add a per-day comparison.
**Likely follow-ups:** 1) Same month last year? SAMEPERIODLASTYEAR. 2) Why blank for Jan? No earlier month in the data.
**Common mistakes:** Using the fact's date instead of the date table in DATEADD; comparing a partial current month with a full previous month.

### Q42 ⭐⭐ 🟡 How would you let users switch between Sales, Profit and Quantity in the same visual?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know field parameters or a disconnected table with SWITCH for a measure selector?
**Say this in the interview:** "I build a field parameter (or a small disconnected table of metric names with a SWITCH measure), put it on a slicer and in the visual's value, so the same chart shows Sales, Profit or Quantity."
**Explain simply:**
- A field parameter is a Power BI feature that lets a slicer choose which field or measure a visual uses.
- The older approach is a disconnected table (no relationships) holding the labels "Sales", "Profit", "Quantity". A measure reads the selection with SELECTEDVALUE and returns the matching measure through SWITCH.
- Put the selector on a slicer. The visual uses the selector measure (or the parameter field) as its value.
- Format: set each measure's format string to suit, or use dynamic format strings.
**Example:** Pen / Book / Bag chart: Sales 250 / 500 / 500; switch to Profit 100 / 180 / 150; switch to Quantity 25 / 10 / 5.
**Sample data:**

Table `Sales`:

| Product | Sales | Cost | Qty | Profit |
|---|---|---|---|---|
| Pen | 100 | 60 | 10 | 40 |
| Pen | 150 | 90 | 15 | 60 |
| Book | 300 | 200 | 6 | 100 |
| Book | 200 | 120 | 4 | 80 |
| Bag | 500 | 350 | 5 | 150 |

**DAX / Steps (not run here):**
```dax
Metric = DATATABLE ( "Metric", STRING, { { "Sales" }, { "Profit" }, { "Quantity" } } )   -- disconnected table

Selected Metric =
SWITCH (
    SELECTEDVALUE ( Metric[Metric], "Sales" ),
    "Sales",    [Total Sales],
    "Profit",   [Total Profit],
    "Quantity", [Total Quantity]
)

Total Sales = SUM ( Sales[Sales] )
Total Profit = SUM ( Sales[Profit] )
Total Quantity = SUM ( Sales[Qty] )
```
**Click-path:** Field parameter: Modeling tab > New parameter > Fields > add Sales, Profit, Quantity > tick "Add slicer to this page". Then use the parameter field in the visual. (Click-path not run here; the ribbon location may differ by build.)
**Alternative:** Field parameters are the easier route in current Desktop; SWITCH is the older, fully controllable one, and works in any version.
**Result (reproduced with pandas, not a DAX engine):** Sales: Bag 500, Book 500, Pen 250. Profit: Bag 150, Book 180, Pen 100. Quantity: Bag 5, Book 10, Pen 25. Reproduced with pandas.
**Pandas check:**
```python
import pandas as pd
sales = pd.DataFrame({"Product":["Pen","Pen","Book","Book","Bag"],"Sales":[100,150,300,200,500],"Cost":[60,90,200,120,350],"Qty":[10,15,6,4,5]})
sales["Profit"] = sales.Sales - sales.Cost
metrics = {"Sales":"Sales","Profit":"Profit","Quantity":"Qty"}
for choice in ["Sales","Profit","Quantity"]:
    print(choice, sales.groupby("Product")[metrics[choice]].sum().to_dict())
```
Printed output:
```
Sales {'Bag': 500, 'Book': 500, 'Pen': 250}
Profit {'Bag': 150, 'Book': 180, 'Pen': 100}
Quantity {'Bag': 5, 'Book': 10, 'Pen': 25}
```
**Version / licensing note:** Field parameters are a Desktop feature of newer builds; their exact availability and Service behaviour are from memory, unverified. Microsoft Learn was unreachable from this session (one fetch of learn.microsoft.com was refused by the network proxy; not retried), so no Microsoft page was read. Everything here is from memory, unverified.
**Edge cases:** Mixing metrics with different units in one axis misleads; use a title that shows the chosen metric (a dynamic title measure). If several values are selected SELECTEDVALUE falls back to its default.
**Likely follow-ups:** 1) What is the difference between the two ways? A field parameter swaps fields; SWITCH controls the logic in one measure. 2) How to show the selected metric in the title? A text measure with the same SELECTEDVALUE.
**Common mistakes:** Relating the selector table to the model; forgetting the default argument; leaving a mixed-unit axis without a title.

### Q43 ⭐⭐ 🟡 How would you combine monthly Excel files dropped into a folder so the report updates automatically?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the Folder connector, Combine files, and how to make the process robust?
**Say this in the interview:** "I use Get Data > Folder, point it at the folder, choose Combine and Transform, and Power Query builds a sample query and a function that is applied to every file. New files dropped in the folder are picked up on the next refresh."
**Explain simply:**
- The Folder connector reads the list of files in a folder; Combine appends all of them into one table.
- Filter the file list first (extension, name pattern) so temporary or backup files are ignored.
- Add a column with the source file name, handy for finding duplicates or the month.
- For the Service, the folder must be reachable: a local or network path needs an on-premises gateway; SharePoint or OneDrive folders work with the SharePoint folder connector (from memory, unverified).
- All files must share the same columns; otherwise one file can break the refresh.
**Example:** Monthly attendance files `Attendance_2026-01.xlsx`, `Attendance_2026-02.xlsx`... The report grows by one month when February's file lands.
**Sample data:** Folder `C:\HR\Attendance` holds `Attendance_2026-01.xlsx` (2 rows), `Attendance_2026-02.xlsx` (3 rows) and a lock file `~$Attendance_2026-02.xlsx` that Excel creates while the file is open (3 rows, to be ignored).
**DAX / Steps (Power Query M, not run here):**
```m
// Power Query (Home > Get data > Folder), not run here
let
    Source  = Folder.Files("C:\HR\Attendance"),
    Xlsx    = Table.SelectRows(Source, each [Extension] = ".xlsx" and not Text.StartsWith([Name], "~$")),
    Data    = Table.AddColumn(Xlsx, "Data", each Excel.Workbook([Content], true){0}[Data]),
    Keep    = Table.SelectColumns(Data, {"Name", "Data"}),
    Expand  = Table.ExpandTableColumn(Keep, "Data", {"EmpID", "Date", "Status"})
in Expand
```
**Alternative:** Use the built-in Combine > Combine and Transform dialog (generates the helper query and function for you) or ask IT to land the files in a database table.
**Result:** Reproduced with pandas (the M code not run): 5 rows after combining, 2 from January and 3 from February; the lock file is skipped.
**Pandas check:**
```python
import pandas as pd
jan=pd.DataFrame({"EmpID":["E1","E2"],"Status":["P","A"]}); feb=pd.DataFrame({"EmpID":["E1","E2","E3"],"Status":["P","P","P"]})
files={"Attendance_2026-01.xlsx":jan,"Attendance_2026-02.xlsx":feb,"~$Attendance_2026-02.xlsx":feb}
allr=pd.concat([v.assign(Name=k) for k,v in files.items() if not k.startswith("~$")],ignore_index=True)
print(allr.groupby("Name").size()); print("Total rows:",len(allr))
```
Printed January 2, February 3, total 5.
**Version / licensing note:** Connector, gateway and scheduled-refresh facts: Microsoft Learn was unreachable from this session (one fetch of learn.microsoft.com was refused by the network proxy; not retried), so no Microsoft page was read. Everything here is from memory, unverified.
**Edge cases:** Different sheet names across files, extra header rows, files open (lock files starting with ~$), duplicates or corrected re-sends of the same month (see the doubled sales question). Columns added later in new files are dropped unless expanded.
**Likely follow-ups:** 1) What if one file has a different column? That file errors or loses a column; standardise or select columns defensively. 2) Can it refresh online? Yes with the right gateway or SharePoint source.
**Common mistakes:** Using the first file's sample to hard-code sheet names; leaving a backup copy in the folder; no filter on extension.

### Q44 ⭐⭐ 🟡 A source column was renamed and the refresh now fails: how do you fix it without breaking the report?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you fix schema drift at the query step and make queries tolerant, not just re-point the report?
**Say this in the interview:** "I open Power Query, find the failing step (usually Changed Type or a Rename/Select step that names the old column), update the name, and make the query tolerant to future changes, then check the downstream measures still bind."
**Explain simply:**
- The refresh error reads "The column X of the table wasn't found". It is raised at a step that names the old column.
- Fix: edit that step to the new name, or insert a rename step first so the rest of the query still sees the old name (the model and measures do not change).
- Make it tolerant: Table.RenameColumns with MissingField.Ignore, or Table.SelectColumns with MissingField.UseNull.
- Where possible agree a stable layout with the data owner or add an alert if headers change.
**Example:** The HR system renames "Emp Code" to "Employee ID". The query step Changed Type fails. We add a rename back to "EmpID" at the top and refresh succeeds without touching any measure.
**Sample data:** Last month's file has columns `Emp Code`, `Dept`; this month's file has `Employee ID`, `Dept` (same data, one header renamed).
**DAX / Steps (Power Query M, not run here):**
```m
// not run here
let
    Source  = Excel.Workbook(File.Contents("C:\HR\Employees.xlsx"), true){0}[Data],
    // rename the NEW source name back to the name the report expects; ignore if the old name is still there
    Renamed = Table.RenameColumns(Source, {{"Employee ID", "EmpID"}, {"Emp Code", "EmpID"}}, MissingField.Ignore)
in Renamed
```
**Result:** Reproduced with pandas (the M code not run): both the old and the new file end with columns `EmpID`, `Dept`, so the rest of the query and the measures see no change.
**Pandas check:**
```python
import pandas as pd
m={"Employee ID":"EmpID","Emp Code":"EmpID"}   # unknown names are ignored, like MissingField.Ignore
new=pd.DataFrame({"Employee ID":["E1"],"Dept":["IT"]}); old=pd.DataFrame({"Emp Code":["E3"],"Dept":["IT"]})
print(list(new.rename(columns=m).columns), list(old.rename(columns=m).columns))
```
Printed `['EmpID', 'Dept'] ['EmpID', 'Dept']`.
**Alternative:** Position-based promote headers and rename by position (`Table.ToColumns`), or reading the data via a view in the database so the report never sees source renames.
**Version / licensing note:** M behaviour of MissingField options is from memory, unverified; Microsoft Learn was unreachable from this session (one fetch of learn.microsoft.com was refused by the network proxy; not retried), so no Microsoft page was read. Everything here is from memory, unverified.
**Edge cases:** Both names missing: the step still fails (or gives null with UseNull); watch for type changes caused by renamed columns. If the renamed column feeds a relationship the key must keep its model name.
**Likely follow-ups:** 1) Why rename in Power Query not in the model? Model measures and relationships are keyed to model names. 2) How to detect it earlier? A refresh failure alert and a header-check query.
**Common mistakes:** Editing every measure; deleting and re-adding the query (loses relationships); leaving the failing step in the middle of the query.

### Q45 ⭐⭐ 🟡 Your colleague cannot open the report you shared: what do you check?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know access, licence, workspace and RLS are separate gates?
**Say this in the interview:** "I check four things: do they have a licence that lets them view (Pro or Premium/Fabric capacity), are they in the workspace or app audience, does the semantic model share permissions or RLS block them, and are they using the right link or app?"
**Explain simply:**
- A licence decides whether a person can open shared content in a non-capacity workspace; content in a suitable capacity can be viewed more widely (from memory, unverified).
- Access is granted by workspace role, by app audience, or by direct share of the report; each has its own list.
- The underlying semantic model (data) needs Read/Build permission if they build their own reports.
- Row-level security (RLS) can make a report appear empty to someone not assigned to a role.
- Check the link (workspace versus app), tenant (guest users), and sensitivity labels.
**Example:** A new HR business partner gets "You don't have access". She has no Pro licence and is not in the app audience. We add her to the audience; the report opens but is empty because RLS has no role mapping for her.
**DAX / Steps:** 1. Workspace > report > Manage permissions (check person is listed). 2. Workspace > Access, or App > Manage audience. 3. Semantic model > Manage permissions. 4. Settings > Security (RLS): add the user to the role. 5. Confirm licence in the admin portal. (Click-paths not run here.)
**Alternative:** Publish as an app to an audience group (cleaner than sharing individual links).
**Version / licensing note:** Licence requirements (free, Pro, PPU, Premium or Fabric capacity) and guest-user rules: Microsoft Learn was unreachable from this session (one fetch of learn.microsoft.com was refused by the network proxy; not retried), so no Microsoft page was read. Do not quote prices here; they change. Everything here is from memory, unverified.
**Edge cases:** Guest or external users, a different tenant, a revoked license, a deleted workspace, and a link to a draft copy are classic causes. A "no access" message versus an empty report point to different problems.
**Likely follow-ups:** 1) Free user can view? Only in some capacity setups (from memory, unverified); check the licence page. 2) What is the best sharing method for many users? An app with audiences.
**Common mistakes:** Sending the workspace link instead of the app; granting workspace Contributor to viewers; forgetting RLS.

### Q46 ⭐⭐ 🟡 The numbers on the dashboard changed since yesterday though nobody edited the report: what could explain it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you consider data, refresh, filters, definitions and time-based logic, not only report edits?
**Say this in the interview:** "If nobody edited the report, the data changed: a scheduled refresh ran, the source was corrected, late records or backdated entries arrived, a source file was replaced, or the measure uses TODAY() or a rolling window. I compare yesterday's and today's numbers by source and date to find which."
**Explain simply:**
- Scheduled refresh updates the report with the latest source data; a "yesterday" number can legitimately change when late data lands.
- Source changes: corrected rows, new duplicate files, a master data change (employee moved departments), or a changed filter at the source.
- Time-based logic: TODAY()/NOW(), relative date filters (last 30 days), or as-of dates change numbers by themselves.
- Other causes: a model or gateway change by someone else, a sensitivity/RLS change, or a different user's view (RLS).
- Method: check refresh history times, compare a snapshot, filter by load date, and look at changed rows.
**Example:** Headcount fell from 1,204 to 1,198 overnight. Refresh history shows a 6 am refresh; HR corrected six exits dated last week. The report did not change, the data did.
**DAX / Steps:** Not applicable (a diagnosis answer; nothing run here). Click-path to start: Service > Workspace > semantic model > Refresh history, then compare row counts and sums by load date.
**Alternative:** Keep a daily snapshot table (date, headcount) so past numbers are fixed, and show "data as of" on the report.
**Version / licensing note:** Refresh behaviour and history: Microsoft Learn was unreachable from this session (one fetch of learn.microsoft.com was refused by the network proxy; not retried), so no Microsoft page was read. Everything here is from memory, unverified.
**Edge cases:** Time zone: the service runs in UTC but users in India; an end-of-day cut-off shifts. A different person opened it with RLS applied. Dashboard tiles cache and can show older values than the report.
**Likely follow-ups:** 1) How do you stop surprises? Add "Last refreshed" and keep snapshots for month-end figures. 2) How do you prove it was data? Compare row counts and sums by load date.
**Common mistakes:** Assuming the report is wrong; not checking refresh history; trusting a live headcount for a closed month.

### Q47 ⭐⭐ 🟡 Write the DAX for average time to hire (days from application to joining) and show it by department.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you write a date-difference measure at row grain and show it correctly by department?
**Say this in the interview:** "I take the average of days between application date and joining date across hires with AVERAGEX and DATEDIFF; because it is a measure it recalculates for each department in the visual. I exclude candidates who have not joined."
**Explain simply:**
- Time to hire here means calendar days from application to joining; define it clearly (some firms measure to offer acceptance).
- DATEDIFF(start, end, DAY) returns whole days between two dates.
- AVERAGEX goes through each hire row, computes the days, and averages them in the current filter (here, the department).
- Candidates still in process have no joining date; leave them out, or the average is wrong.
- Show it as a bar by department plus a card for the overall number.
**Example:** IT hires took 46, 50 and 44 days (average 46.7), HR 33 and 42 (37.5), Sales 34 and 38 (36.0; one Sales candidate has not joined yet). Overall average 41.0 days.
**Sample data:**

Table `Hires`:

| CandID | Dept | Applied | Joined |
|---|---|---|---|
| 1 | IT | 2026-01-05 | 2026-02-20 |
| 2 | IT | 2026-01-10 | 2026-03-01 |
| 3 | IT | 2026-01-20 | 2026-03-05 |
| 4 | HR | 2026-01-08 | 2026-02-10 |
| 5 | HR | 2026-02-01 | 2026-03-15 |
| 6 | Sales | 2026-01-12 | 2026-02-15 |
| 7 | Sales | 2026-01-15 |  |
| 8 | Sales | 2026-02-10 | 2026-03-20 |

**DAX / Steps (not run here):**
```dax
Avg Time to Hire (Days) =
AVERAGEX (
    FILTER ( Hires, NOT ISBLANK ( Hires[Joined] ) && NOT ISBLANK ( Hires[Applied] ) ),
    DATEDIFF ( Hires[Applied], Hires[Joined], DAY )
)
```
**Alternative:** Add a calculated column `DaysToHire = DATEDIFF(...)` then a plain `AVERAGE(Hires[DaysToHire])`; simpler to read, slightly bigger model.
**Result (reproduced with pandas, not a DAX engine):** HR 37.5, IT 46.7, Sales 36.0 days; overall 41.0 days (7 joined candidates; the 8th has no joining date). Reproduced with pandas.
**Pandas check:**
```python
import pandas as pd
h = pd.DataFrame({"CandID":range(1,9),"Dept":["IT","IT","IT","HR","HR","Sales","Sales","Sales"],
 "Applied":pd.to_datetime(["2026-01-05","2026-01-10","2026-01-20","2026-01-08","2026-02-01","2026-01-12","2026-01-15","2026-02-10"]),
 "Joined":pd.to_datetime(["2026-02-20","2026-03-01","2026-03-05","2026-02-10","2026-03-15","2026-02-15",None,"2026-03-20"])})
h["Days"] = (h.Joined - h.Applied).dt.days
print(h)
print(h.groupby("Dept")["Days"].mean().round(1))
print("Overall:", round(h.Days.mean(),2), "(mean of rows, skips the not-yet-joined row)")
```
Printed output:
```
   CandID   Dept    Applied     Joined  Days
0       1     IT 2026-01-05 2026-02-20  46.0
1       2     IT 2026-01-10 2026-03-01  50.0
2       3     IT 2026-01-20 2026-03-05  44.0
3       4     HR 2026-01-08 2026-02-10  33.0
4       5     HR 2026-02-01 2026-03-15  42.0
5       6  Sales 2026-01-12 2026-02-15  34.0
6       7  Sales 2026-01-15        NaT   NaN
7       8  Sales 2026-02-10 2026-03-20  38.0
Dept
HR       37.5
IT       46.7
Sales    36.0
Name: Days, dtype: float64
Overall: 41.0 (mean of rows, skips the not-yet-joined row)
```
**Version / licensing note:** DAX is not run here. Microsoft Learn was unreachable from this session (one fetch of learn.microsoft.com was refused by the network proxy; not retried), so no Microsoft page was read. Everything here is from memory, unverified.
**Edge cases:** Median is often better than average because a few very long hires skew it (DAX has MEDIANX). Negative days mean bad data. Averaging department averages gives a different overall figure than the measure.
**Likely follow-ups:** 1) Time to hire versus time to fill? Time to fill counts from job opening, time to hire from the candidate's application (definitions vary, state yours). 2) How to show the trend? Put the month of joining on the axis.
**Common mistakes:** Averaging rows that have no joining date; averaging department averages; mixing dates and datetimes.

### Q48 ⭐⭐ 🟡 Sales doubled after a colleague saved a corrected copy of a monthly file into the source folder: why, and how do you stop it happening?
**Asked at:** commonly asked (no company-specific report found); a practical failure mode, not seen as a question in any source.
**What the interviewer is checking:** Do you understand that a folder source loads every file in it, and can you find and prevent duplicates?
**Say this in the interview:** "A folder connection appends every file it finds. The corrected copy was loaded next to the original, so February was counted twice. I would filter to the right files, remove duplicate orders by their ID, and agree a naming and archive rule so corrections replace files rather than sit beside them."
**Explain simply:**
- The Folder connector (Get Data > Folder) reads all files in a folder and stacks them into one table (Power Query "Combine"). It does not know that `Sales_Feb_corrected` replaces `Sales_Feb`.
- Diagnose: in Power Query keep the `Source.Name` column and count rows per file; the two February files will show the same orders.
- Fix 1: process rule, with a `Corrected` or `Archive` sub-folder and only the live folder as the source.
- Fix 2: in Power Query, filter on file name, or remove duplicates on the business key (OrderID). Sort so the latest file wins before removing duplicates.
- Fix 3: add a check measure, rows loaded versus distinct OrderIDs, that goes red when they differ.
**Example:** January 3,000, February 4,000 (orders B1 1,500 and B2 2,500 plus the same two again in the corrected file), March 3,000. Report shows 14,000 instead of 10,000.
**Sample data:** Table `Combined` (after folder combine):

| File | Order | Amount |
|---|---|---|
| Sales_Jan.xlsx | A1 | 1,000 |
| Sales_Jan.xlsx | A2 | 2,000 |
| Sales_Feb.xlsx | B1 | 1,500 |
| Sales_Feb.xlsx | B2 | 2,500 |
| Sales_Feb_corrected.xlsx | B1 | 1,500 |
| Sales_Feb_corrected.xlsx | B2 | 2,500 |
| Sales_Mar.xlsx | C1 | 3,000 |

**DAX / Steps:** (Power Query M and DAX, not run here)
```m
// last step of the combined query: Table.Distinct keeps the FIRST row it meets per Order
// (to let the newest file win, sort by Date modified descending and Table.Buffer before this step)
= Table.Distinct(PreviousStep, {"Order"})
```
```dax
Rows Loaded = COUNTROWS(Combined)
Distinct Orders = DISTINCTCOUNT(Combined[Order])
Duplicate Rows = [Rows Loaded] - [Distinct Orders]
```
**Alternative:** Keep a strict rule on file names (for example, filter out any name containing "_corrected" and instead replace the original file), or move to a database or SharePoint list as the single source.
**Result:** reproduced with pandas: total with duplicates 14,000 (Feb shows 8,000); after removing duplicate OrderIDs 10,000.
**Pandas check:**
```python
import pandas as pd
rows=pd.DataFrame({"file":["Sales_Jan.xlsx"]*2+["Sales_Feb.xlsx"]*2+["Sales_Feb_corrected.xlsx"]*2+["Sales_Mar.xlsx"],
 "Order":["A1","A2","B1","B2","B1","B2","C1"],"Amount":[1000,2000,1500,2500,1500,2500,3000]})
rows["Month"]=rows.file.str.extract(r"Sales_(\w{3})")
print(rows.groupby("Month").Amount.sum(), "total", rows.Amount.sum())
print("deduped total", rows.drop_duplicates(["Order"],keep="last").Amount.sum())
```
Output (run): Feb 8000, Jan 3000, Mar 3000, total 14000; deduped total 10000.
**Version / licensing note:** from memory, unverified (Microsoft Learn was unreachable: learn.microsoft.com did not resolve, so no page was fetched). Folder connector works in Desktop; scheduled refresh in the Service on files needs a gateway for local folders (from memory, unverified).
**Edge cases:** A genuine correction may change amounts, so dedupe by key and keep the newest, not just any copy. Temp files like `~$Sales.xlsx` also get loaded. Date-in-filename conventions help.
**Likely follow-ups:** 1) *How to keep only the latest file?* Sort by Date modified, then Table.Distinct on the key. 2) *Why not just delete the file?* You can, but a data check protects you from the next one.
**Common mistakes:** Hiding the double count with a visual filter; removing duplicates on all columns when the correction changed an amount; never adding a row-count check.

### Q49 ⭐⭐ 🔴 Your DirectQuery report is slow: what options do you have?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know that DirectQuery sends a live query to the source on every click, and the usual ways around the slowness?
**Say this in the interview:** "In DirectQuery every visual fires a query at the database, so I first find which visual is slow with Performance Analyzer. Then I reduce queries, tune the source, summarise with aggregations, or move parts to Import in a composite model."
**Explain simply:**
- DirectQuery means Power BI leaves data in the source and asks it a question each time (opposite of Import, which copies data in).
- Cut the work: fewer visuals per page, Apply button for slicers, Top N filters, drill-through or tooltip pages for detail.
- Tune the source: indexes, views, a star schema, query folding (Power Query steps pushed back to the database as SQL).
- Aggregations: a small imported summary table answers most clicks; only detail hits the source.
- Composite model: Import dimensions and small tables, keep only the big fact table in DirectQuery.
- Consider whether live data is really needed; hourly Import refresh is often enough.
**Example:** A 200-million-row payroll table on SQL Server; a page with 15 visuals took 40 seconds. Reducing to 6 visuals and importing the department and date tables brought it to a few seconds (illustrative numbers).
**DAX / Steps:** (click-path, not run here)
1. View > Performance analyzer > Start recording > refresh visuals; read DAX query vs Direct query durations.
2. Copy the query for the slowest visual; check its SQL in the database.
3. Model view > table > Storage mode (Import / DirectQuery / Dual) for dimensions.
4. Model > Manage aggregations to map a summary table.
5. File > Options > Query reduction: add Apply buttons to slicers.
**Alternative:** Switch the whole model to Import with scheduled refresh, or incremental refresh if size is the reason for DirectQuery.
**Version / licensing note:** from memory, unverified (Microsoft Learn unreachable). Performance Analyzer is in Desktop; the option exists in the Service edit mode per the research notes in research/Book04_Part09_sources.md, a page I did not re-fetch.
**Edge cases:** Many-to-many and complex DAX can generate heavy SQL; some DAX functions and Power Query steps are not supported in DirectQuery; row-level security adds more filtering to every query.
**Likely follow-ups:** 1) *What is Dual mode?* A table that can act as Import or DirectQuery depending on the query. 2) *Does DirectQuery refresh?* No scheduled refresh for the data, results are live.
**Common mistakes:** Adding more visuals; blaming Power BI without checking the source database; building a flat wide table instead of a star schema.

### Q50 ⭐⭐ 🔴 Power BI revenue is 2 percent off the finance ledger: how do you reconcile it step by step?
**Asked at:** commonly asked (no company-specific report found); the sources list "inconsistent sources" as a general scenario theme only.
**What the interviewer is checking:** A calm, systematic method: agree definitions, then bisect the difference, not guess.
**Say this in the interview:** "First I agree what 'revenue' means with finance, then I compare totals at a coarse level and drill down until the gap sits in one month, one entity or one set of rows, and explain it row by row."
**Explain simply:**
- Step 1, definitions: gross or net of discounts, tax included or not, invoice date or booking date, currency and exchange rate, returns and credit notes.
- Step 2, scope: same date range, same entities (company codes, regions), same cut-off and time zone.
- Step 3, bisect: compare by month, then entity, then product or customer; find where the variance concentrates.
- Step 4, row-level: export both sides to a table and anti-join on invoice number to list items in one and missing in the other.
- Step 5, model causes: duplicates (see Q48), filters left on a visual, bad relationships, rows dropped in Power Query, blank dates falling outside the date table, rounding.
- Step 6, document the reconciliation and add a permanent check measure (Power BI total minus ledger total).
**Example:** Ledger 1,000,000; Power BI 980,000, so a gap of 20,000 (2%). By month the gap is all in March; by invoice, 12 credit notes totalling 20,000 were excluded by a Power Query filter "Amount > 0".
**Sample data:** Illustrative only: ledger revenue 1,000,000; Power BI revenue 980,000; gap in March, from 12 credit notes totalling 20,000.
**DAX / Steps:** (not run here; `[Power BI Revenue]` and `[Ledger Revenue]` stand for your two total measures)
```dax
Variance = [Power BI Revenue] - [Ledger Revenue]
Variance % = DIVIDE([Variance], [Ledger Revenue])
```
**Alternative:** Reverse the direction: start from the ledger and check which invoices exist in Power BI with an anti-join in Power Query (Merge > Left Anti).
**Result:** arithmetic only: 1,000,000 x 98% = 980,000; gap 20,000, which is 2.0% (checked with Python).
**Pandas check:** `print(1_000_000-980_000, (1_000_000-980_000)/1_000_000*100)` printed `20000 2.0` (plain arithmetic; no DataFrame needed).
**Version / licensing note:** no version dependency; from memory, unverified.
**Edge cases:** Rounding on thousands of small lines can explain a tiny gap; timing differences (ledger posts later) move revenue between months; multi-currency uses different rates.
**Likely follow-ups:** 1) *What if both are right?* Then the definitions differ; document and show both. 2) *How to prevent it?* A reconciliation page showing both totals.
**Common mistakes:** Changing measures until the number matches; not agreeing definitions first; ignoring credit notes and returns.

### Q51 ⭐⭐ 🔴 How do you test that row-level security works before publishing, and where does it not protect the data?
**Asked at:** Row-level security (RLS) was reportedly asked in a Deloitte round (Sept 2025) and in an older Cognizant report from 2022 (research/interview_processes.md, Glassdoor snippets, unverified). This exact testing question: no company-specific report found.
**What the interviewer is checking:** Do you know View as, dynamic RLS testing, and the limits of RLS (owners, exports, Build permission)?
**Say this in the interview:** "I use View as roles in Desktop with a test user, then test again in the Service after publishing and assigning members. RLS only filters rows in the model; people with edit or Build rights, workspace Admins/Members/Contributors, or those who see the raw file, are not restricted the same way."
**Explain simply:**
- RLS means a rule on a table such as `Department = "Sales"` so each person sees only their rows (a role holds the rules).
- Test in Desktop: Modeling > View as > pick role (and, for dynamic RLS, Other user to type an email). Check that totals change, and that a user in two roles sees both.
- Test in the Service: semantic model > Security > Test as role; then assign users or groups to the role.
- Not protected: workspace Admin, Member and Contributor roles bypass RLS (they can edit the model), anyone with Build permission can query the model through Analyze in Excel, and data already exported or emailed. The raw source and the .pbix file are not protected by RLS at all.
- RLS hides rows, not columns; to hide a column use object-level security (see Q65).
**Example:** HR report with `Region` rule: a Hyderabad manager should see 120 employees, not the company's 900. After View as, the headcount card must show 120.
**DAX / Steps:** (not run here)
```dax
-- dynamic RLS rule on table Employees (DAX filter expression)
[ManagerEmail] = USERPRINCIPALNAME()
```
1. Modeling tab > Manage roles > Create > pick table > enter the DAX filter > Save.
2. Modeling > View as > tick the role (and Other user) > OK; read the banner "Now viewing as".
3. Publish; in the Service open workspace > semantic model ... > Security; add members to the role.
**Alternative:** Use a security mapping table (User, Region) and filter with LOOKUPVALUE, easier for many users.
**Version / licensing note:** from memory, unverified (Microsoft Learn unreachable). Bypass roles and Build permission statements are from memory; verify on the RLS page.
**Edge cases:** A user with no role assigned sees nothing (or, if they are an editor, everything); DirectQuery RLS runs at the source; test with a user who has no matching row.
**Likely follow-ups:** 1) *Static vs dynamic?* Static hard-codes a value per role; dynamic uses USERPRINCIPALNAME. 2) *Does RLS work on a free licence?* Sharing needs paid licences or capacity (from memory, unverified).
**Common mistakes:** Testing only as the author (who sees everything); forgetting to assign members after publishing; believing RLS protects exported Excel files.

### Q52 ⭐⭐ 🔴 You get three raw Excel files of sales, products and customers: build a sales dashboard with a date slicer and a year-over-year comparison, and explain your steps.
**Asked at:** commonly asked (no company-specific report found); an end-to-end build task, not seen in a source.
**What the interviewer is checking:** Whether you can run the whole path: clean, model as a star, write measures, design the page.
**Say this in the interview:** "I load the three files, clean them in Power Query, create a date table, relate sales to products, customers and dates in a star shape, write a total sales and a prior-year measure, then build cards, a trend line and a date slicer."
**Explain simply:**
- Load and clean: Get Data > Excel; fix types, trim text, remove duplicates and blank rows; promote headers.
- Model: Sales is the fact table (transactions); Products and Customers are dimension tables (descriptions). One-to-many relationships from dimension to fact. Add a Date table (CALENDAR) and mark it as the date table.
- Measures: Total Sales, Sales Last Year with SAMEPERIODLASTYEAR, YoY %.
- Visuals: KPI cards, line chart by month with both years, bar by category, Date slicer (Between or relative date) from the Date table column, not the raw sales column.
- Check: reconcile card total with the Excel total.
**Example:** 2024 revenue 220 and 2025 revenue 280 (in lakhs) gives YoY of 27.3%.
**Sample data:** Table `Sales` (simplified, quarterly totals; a real Sales table would carry an order date related to the Date table, which SAMEPERIODLASTYEAR needs):

| Year | Quarter | Revenue |
|---|---|---|
| 2024 | 1 | 100 |
| 2024 | 2 | 120 |
| 2025 | 1 | 130 |
| 2025 | 2 | 150 |

**DAX / Steps:** (not run here)
```dax
Date = CALENDAR(DATE(2023,1,1), DATE(2026,12,31))
Total Sales = SUM(Sales[Revenue])
Sales LY = CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date'[Date]))
YoY % = DIVIDE([Total Sales] - [Sales LY], [Sales LY])
```
1. Home > Get data > Excel (three files) > Transform data.
2. Home > Close & Apply; Model view: drag Products[ProductID] to Sales[ProductID], same for customers and Date.
3. Table tools > Mark as date table.
4. Visualizations: slicer with Date[Date] (Between), card, line chart (Month on axis).
**Alternative:** Year-to-date comparison with TOTALYTD, or DATEADD('Date'[Date], -1, YEAR).
**Result:** reproduced with pandas: 2024 = 220, 2025 = 280, YoY = 27.3%. The DAX itself is not run here.
**Pandas check:**
```python
import pandas as pd
s=pd.DataFrame({'Year':[2024,2024,2025,2025],'Q':[1,2,1,2],'Rev':[100,120,130,150]})
y=s.groupby('Year').Rev.sum(); print(y.to_dict(), round((y[2025]-y[2024])/y[2024]*100,1))
```
Output (run): `{2024: 220, 2025: 280} 27.3`
**Version / licensing note:** from memory, unverified (Microsoft Learn unreachable). The build happens in Power BI Desktop (Windows); sharing needs a paid licence.
**Edge cases:** Date table must cover all dates and have no gaps; SAMEPERIODLASTYEAR needs a proper date column; a partial current year makes YoY misleading (compare year to date); blank prior year gives blank, not zero, with DIVIDE.
**Likely follow-ups:** 1) *Why a separate date table?* Time intelligence functions need a continuous date column. 2) *Why not one flat table?* Slower, error-prone, hard to extend.
**Common mistakes:** Slicing on the sales date column instead of the date table; many-to-many relationships; no check of totals against the source.

### Q53 ⭐ 🟢 How would you plan a dashboard project when the deadline is two weeks?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Prioritisation, scoping and communication, not tool tricks.
**Say this in the interview:** "I spend the first two days agreeing questions and KPIs, build a thin version end to end by the middle of week one, then iterate with the stakeholder and keep the last two days for testing and handover."
**Explain simply:**
- Days 1-2: who uses it, which 3-5 decisions it supports, KPI definitions, data sources, access.
- Days 3-5: load data, build the model, write core measures, reconcile with a known number.
- Days 6-8: first visual version, a quick review with the user.
- Days 9-10: feedback, performance check, RLS if needed, publish, schedule refresh, short guide.
- Write down what is out of scope (a "later" list) so scope does not grow.
**Example:** HR attrition dashboard: KPIs are headcount, leavers, attrition %, by department and month; later list: exit-reason text analysis.
**DAX / Steps:** (planning answer, no code)
1. Day 1 kick-off and KPI sign-off.
2. Week 1 data and model; week 2 visuals, review, publish.
**Alternative:** An Excel prototype or a wireframe on paper first, to settle the layout before building.
**Version / licensing note:** no version dependency; check early that users have a licence to view shared reports (from memory, unverified).
**Edge cases:** Data not ready or access delayed: ship with a sample and flag risk early. KPI definitions still disputed: write the definitions and get sign-off in writing.
**Likely follow-ups:** 1) *What if scope grows?* Trade-off: add it after launch or drop something. 2) *How do you prove it is right?* Reconcile to a finance or HR source number.
**Common mistakes:** Starting with visuals; skipping KPI definitions; leaving testing for the last hour.

### Q54 ⭐ 🟢 How would you present a new dashboard to non-technical stakeholders and handle change requests?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Storytelling for business users and a controlled way to handle requests.
**Say this in the interview:** "I open with the business question and the answer in one line, then walk through the page like a story, and I log every change request, rate it by value and effort, and agree a date instead of promising on the spot."
**Explain simply:**
- Start with the headline ("attrition rose from 12% to 15%, mostly in Sales"), then show where to look.
- Avoid technical words; show how to filter, how to read the colours.
- Use a request log: request, who, why, effort, priority, status.
- Separate bugs (fix now) from new wants (schedule).
- Version the report; tell users what changed.
**Example:** A manager asks for 10 new visuals; you log them, find only 2 affect a decision, and ship those next week.
**DAX / Steps:** (process answer)
1. Dry run with one friendly user.
2. Demo 15 minutes; leave a one-page guide.
3. Review the change log weekly.
**Alternative:** Use bookmarks or a guided navigation page to tour the report live.
**Version / licensing note:** no version dependency; Service sharing features depend on licence (from memory, unverified).
**Edge cases:** Conflicting requests from two leaders: ask the owner to decide; sensitive data: check access before screen sharing.
**Likely follow-ups:** 1) *What if the number disagrees with their Excel?* Reconcile together (see Q50). 2) *How do you measure adoption?* Usage metrics in the Service (from memory, unverified).
**Common mistakes:** Showing how it was built instead of what it says; accepting every request; changing numbers silently.

### Q55 ⭐ 🟢 What documentation would you hand over with a report you built for a colleague to maintain?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether others can maintain your work without calling you.
**Say this in the interview:** "A one-pager with purpose and owner, data sources and refresh schedule, a data dictionary and measure list with definitions, the model diagram, known issues, and steps for common changes."
**Explain simply:**
- Purpose, audience, owner, report URL, workspace.
- Sources: file paths or servers, credentials owner, gateway, refresh time.
- Model: table list, relationships (diagram), date table.
- Measures: name, plain definition, DAX, and who approved it.
- Transformations: key Power Query steps and why.
- Runbook: what to do when refresh fails; how to add a month; known limitations; change log.
**Example:** For an attrition report, state "Attrition % = leavers / average headcount, approved by HR head, 5 Jan".
**DAX / Steps:** (no code)
1. Add descriptions to measures in the model (Properties pane).
2. Add a hidden "About" page in the report.
3. Keep the pbix and notes in the shared folder.
**Alternative:** Use a template file (.pbit) so the colleague starts from a clean copy (from memory, unverified).
**Version / licensing note:** no version dependency.
**Edge cases:** Personal credentials in the data source break refresh when you leave; hand over ownership of the semantic model.
**Likely follow-ups:** 1) *What if you leave tomorrow?* The runbook covers it. 2) *Where do you store it?* A shared location with version history.
**Common mistakes:** Undocumented measure logic; documentation that is out of date; hard-coded personal paths.

### Q56 ⭐ 🟢 How would you set an alert in the Power BI service when sales fall below target?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know data alerts exist, which visuals they need, and their limits?
**Say this in the interview:** "I pin a card, gauge or KPI visual to a dashboard, then use Manage alerts on the tile to set 'below' a threshold and choose email or notification."
**Explain simply:**
- Alerts are set on dashboard tiles, not on report pages directly.
- They work on card, gauge and KPI tiles (single number).
- The alert checks the number when data refreshes, then notifies you.
- The threshold is a fixed number; it does not read a target column by itself.
**Example:** Sales card shows 8.2 lakh; alert "below 10 lakh" emails you at the next refresh.
**DAX / Steps:** (click-path, not run here)
1. In the report, pin the card to a dashboard.
2. Dashboard > tile ... > Manage alerts > Add alert rule.
3. Choose Below, enter 1000000, tick email, Save.
**Alternative:** For a dynamic target or richer logic, use Power Automate or a data-driven alert (from memory, unverified).
**Version / licensing note:** from memory, unverified: Microsoft Learn was unreachable, so the visual types, licence requirement and Mac/mobile behaviour were not verified.
**Edge cases:** Alerts fire after refresh, not live; RLS can change what a user sees; a target stored as a measure still needs a fixed number in the rule.
**Likely follow-ups:** 1) *Can you alert on a bar chart?* No, only single-value tiles. 2) *Can others get the alert?* It is per user (from memory, unverified).
**Common mistakes:** Looking for alerts in Desktop; expecting alerts for imported data with no scheduled refresh.

### Q57 ⭐ 🟡 How would you build a what-if parameter to model a salary hike scenario?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the What-if parameter feature and how to wire it into a measure?
**Say this in the interview:** "I create a numeric What-if parameter from 0 to 20 percent, which gives me a slicer and a measure holding the chosen value, then I write projected payroll as salary times one plus that value."
**Explain simply:**
- A What-if parameter is a generated table of values plus a slicer and a measure that returns the selected value.
- The parameter does nothing until a measure uses it.
- Total cost of the hike is projected payroll minus current payroll.
**Example:** Four employees, current payroll 24 lakh a year (2,400,000); a 5% hike costs 120,000.
**Sample data:** Table `Employees`:

| Dept | Salary |
|---|---|
| Sales | 600,000 |
| Tech | 900,000 |
| HR | 500,000 |
| Ops | 400,000 |

**DAX / Steps:** (not run here)
1. Modeling tab > New parameter > Numeric range: name `Hike %`, minimum 0, maximum 20, increment 1, Add slicer.
2. Power BI creates a table `Hike %` and a measure `Hike % Value` automatically (from memory, unverified), roughly `Hike % Value = SELECTEDVALUE('Hike %'[Hike %], 0)`.
```dax
Current Payroll = SUM(Employees[Salary])
Projected Payroll = SUMX(Employees, Employees[Salary] * (1 + [Hike % Value] / 100))
Hike Cost = [Projected Payroll] - [Current Payroll]
```
**Alternative:** A disconnected table typed in via Enter data with slicer values, plus SELECTEDVALUE.
**Result:** reproduced with pandas: 0% gives 2,400,000 / cost 0; 5% gives 2,520,000 / cost 120,000; 10% gives 2,640,000 / cost 240,000.
**Pandas check:**
```python
import pandas as pd
emp=pd.DataFrame({"Dept":["Sales","Tech","HR","Ops"],"Salary":[600000,900000,500000,400000]})
for h in [0,5,10]: print(h, (emp.Salary*(1+h/100)).sum(), (emp.Salary*(h/100)).sum())
```
Output (run): `0 2400000.0 0.0`, `5 2520000.0 120000.0`, `10 2640000.0 240000.0`.
**Version / licensing note:** from memory, unverified (Microsoft Learn unreachable). The menu wording ("New parameter" under Modeling) can differ in newer Desktop builds.
**Edge cases:** With a multi-select the SELECTEDVALUE falls back to the default 0; salary changes by department need a second parameter.
**Likely follow-ups:** 1) *Can a user type the value?* Use the numeric range slicer or an input field (from memory, unverified). 2) *Does it work in the Service?* Yes, the slicer is interactive after publishing (from memory, unverified).
**Common mistakes:** Forgetting to use the measure; dividing by 100 twice; using AVERAGE instead of SUMX.

### Q58 ⭐ 🟡 How would you build a Pareto (80/20) analysis of products in Power BI?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you compute a running (cumulative) share in descending order with a measure?
**Say this in the interview:** "I rank products by sales, calculate the cumulative percentage of total with a measure that sums every product at or above this one's sales, and show bars plus a cumulative-percent line."
**Explain simply:**
- Pareto principle: a small share of items (often about 20%) gives most of the result (about 80%).
- Bars = sales per product, sorted high to low; line = cumulative percent of total.
- The measure sums the sales of all products whose sales are at least this product's sales.
- Tag products as class A until the cumulative share passes 80%.
**Example:** Product A gives 50% of sales, B another 30%; A and B alone reach 80%.
**Sample data:** Table `Products` with total sales:

| Product | Sales |
|---|---|
| A | 500 |
| B | 300 |
| C | 80 |
| D | 50 |
| E | 30 |
| F | 20 |
| G | 12 |
| H | 8 |

**DAX / Steps:** (not run here)
```dax
Total Sales = SUM(Products[Sales])   -- Sales column of the sample table
All Sales = CALCULATE([Total Sales], ALLSELECTED(Products[Product]))
Cum % =
VAR cur = [Total Sales]
VAR cumul = SUMX(FILTER(ALLSELECTED(Products[Product]), [Total Sales] >= cur), [Total Sales])
RETURN DIVIDE(cumul, [All Sales])
Class = IF([Cum %] - DIVIDE([Total Sales], [All Sales]) < 0.8, "A", "Tail")
```
Visual: Line and clustered column chart; Product on X axis, Total Sales as column, Cum % as line; sort by Total Sales descending.
**Alternative:** Use RANKX to rank, then a cumulative measure with TOPN; or compute in Power Query with a running total column.
**Result:** reproduced with pandas: cumulative % is 50.0, 80.0, 88.0, 93.0, 96.0, 98.0, 99.2, 100.0; products A and B are class A, C to H are tail.
**Pandas check:**
```python
import pandas as pd, numpy as np
p=pd.DataFrame({"Product":list("ABCDEFGH"),"Sales":[500,300,80,50,30,20,12,8]}).sort_values("Sales",ascending=False)
p["cum"]=p.Sales.cumsum(); p["cum%"]=(p.cum/p.Sales.sum()*100).round(1)
p["Class"]=np.where(p["cum"]-p.Sales<0.8*p.Sales.sum(),"A","Tail"); print(p.to_string(index=False))
```
Output (run): cum% 50.0, 80.0, 88.0, 93.0, 96.0, 98.0, 99.2, 100.0; Class A for A and B, Tail for the rest.
**Version / licensing note:** from memory, unverified (Microsoft Learn unreachable).
**Edge cases:** The class test compares fractions like 0.88 - 0.08 with 0.8, where decimal rounding can flip a borderline product; compare in sales units or add a tiny tolerance. Products with equal sales get the same cumulative number (ties); add a tiebreaker such as product ID. Filters change the percentages, which is usually wanted.
**Likely follow-ups:** 1) *Why ALLSELECTED not ALL?* It respects slicers but ignores the visual's row filter. 2) *80/20 literally?* No, it is a pattern, not a law.
**Common mistakes:** Not sorting the visual; using ALL so slicers are ignored; a cumulative percent that exceeds 100% from ties.

### Q59 ⭐ 🟡 Write a DAX measure to count new versus repeat customers per month.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you define "new" as first order ever, not first order in the month?
**Say this in the interview:** "A customer is new in the month of their first-ever order. I store the first order date per customer, count customers whose first order falls in the visible month as new, and repeat is active customers minus new."
**Explain simply:**
- Active customers = distinct customers who ordered in the month.
- New = customers whose first-ever order date is inside that month.
- Repeat = active minus new (they ordered before this month).
- A customer who orders three times in January is still one new customer.
**Example:** C1 first buys in January, then again in February and March: new in January, repeat later.
**Sample data:** Table `Orders`:

| Cust | Date |
|---|---|
| C1 | 2025-01-05 |
| C2 | 2025-01-12 |
| C1 | 2025-02-03 |
| C3 | 2025-02-10 |
| C2 | 2025-02-20 |
| C1 | 2025-03-02 |
| C4 | 2025-03-15 |
| C3 | 2025-03-20 |

**DAX / Steps:** (not run here)
```dax
-- assumes a Customers table (one row per customer) related one-to-many to Orders, and Date[Date] related to Orders[Date]
-- calculated column on table Customers
FirstOrderDate = CALCULATE(MIN(Orders[Date]))

Active Customers = DISTINCTCOUNT(Orders[Cust])
New Customers =
VAR s = MIN('Date'[Date])
VAR e = MAX('Date'[Date])
RETURN COUNTROWS(FILTER(Customers, Customers[FirstOrderDate] >= s && Customers[FirstOrderDate] <= e))
Repeat Customers = [Active Customers] - [New Customers]
```
**Alternative:** Add an `IsFirstOrder` flag column in Power Query (rank by date per customer) and count flagged customers.
**Result:** reproduced with pandas: Jan 2 active, 2 new, 0 repeat; Feb 3 active, 1 new, 2 repeat; Mar 3 active, 1 new, 2 repeat.
**Pandas check:**
```python
import pandas as pd
o=pd.DataFrame({"Cust":["C1","C2","C1","C3","C2","C1","C4","C3"],"Date":pd.to_datetime(["2025-01-05","2025-01-12","2025-02-03","2025-02-10","2025-02-20","2025-03-02","2025-03-15","2025-03-20"])})
o["Month"]=o.Date.dt.to_period("M"); first=o.groupby("Cust").Date.min()
rs=[(str(m),g.Cust.nunique(),sum(first[c].to_period("M")==m for c in g.Cust.unique())) for m,g in o.groupby("Month")]
print(pd.DataFrame([(m,a,n,a-n) for m,a,n in rs],columns=["Month","Customers","New","Repeat"]))
```
Output (run): 2025-01: 2, 2, 0; 2025-02: 3, 1, 2; 2025-03: 3, 1, 2.
**Version / licensing note:** from memory, unverified (Microsoft Learn unreachable); the measure logic was checked only by the pandas reproduction.
**Edge cases:** Totals row: new customers over the whole year count each customer once, repeat is a different number than the sum of months. Customers with no order have a blank first date and are excluded. The calculated column ignores slicers on purpose.
**Likely follow-ups:** 1) *Why not use the date slicer for first order?* Filters would shrink history, wrongly making repeat customers look new. 2) *Returning after a long gap?* Define "reactivated" separately.
**Common mistakes:** Using the first order in the filtered range; counting orders instead of distinct customers.

### Q60 ⭐ 🟡 Write DAX for hires and leavers by month using one date table and two date columns.
**Asked at:** commonly asked (no company-specific report found); an HR measure written from standard practice.
**What the interviewer is checking:** Do you know an inactive relationship plus USERELATIONSHIP, so one date table serves two date columns?
**Say this in the interview:** "I relate the date table to join date as the active relationship, and to leave date as an inactive one. Hires use the active link; leavers activate the other with USERELATIONSHIP inside CALCULATE."
**Explain simply:**
- Only one relationship between two tables can be active (used by default); extra ones are dashed and inactive.
- USERELATIONSHIP temporarily switches a measure to the inactive relationship.
- People still employed have a blank leave date; they simply never match a month.
- Net change = hires minus leavers.
**Example:** March: 3 joined, 2 left, net plus 1.
**Sample data:** Table `Employees`:

| Emp | JoinDate | LeaveDate |
|---|---|---|
| E1 | 2025-01-10 | blank |
| E2 | 2025-01-20 | 2025-03-10 |
| E3 | 2025-02-05 | 2025-03-12 |
| E4 | 2025-03-01 | blank |
| E5 | 2025-03-15 | blank |
| E6 | 2025-03-25 | 2025-02-20 |

(E6 is deliberately odd: leaving before joining is a data error to check, see edge cases.)
**DAX / Steps:** (not run here)
```dax
Hires = COUNTROWS(Employees)   -- active relationship: Date[Date] -> Employees[JoinDate]
Leavers = CALCULATE(COUNTROWS(Employees), USERELATIONSHIP('Date'[Date], Employees[LeaveDate]))
Net Change = [Hires] - [Leavers]
```
Steps: Model view > drag Date[Date] to Employees[JoinDate] (active); drag Date[Date] to Employees[LeaveDate] (it becomes dashed/inactive).
**Alternative:** Two copies of the date table (Join Date, Leave Date role-playing), or a Dates-by-event table with a unioned hires/leavers events table.
**Result:** reproduced with pandas: Jan hires 2, leavers 0; Feb hires 1, leavers 1; Mar hires 3, leavers 2; net 2, 0, 1.
**Pandas check:**
```python
import pandas as pd
e=pd.DataFrame({"Emp":["E1","E2","E3","E4","E5","E6"],"Join":pd.to_datetime(["2025-01-10","2025-01-20","2025-02-05","2025-03-01","2025-03-15","2025-03-25"]),
 "Leave":pd.to_datetime([None,"2025-03-10","2025-03-12",None,None,"2025-02-20"])})
h=e.groupby(e.Join.dt.to_period("M")).size(); l=e.dropna(subset=["Leave"]).groupby(e.Leave.dt.to_period("M")).size()
t=pd.DataFrame({"Hires":h,"Leavers":l}).fillna(0).astype(int); t["Net"]=t.Hires-t.Leavers; print(t)
```
Output (run): 2025-01: 2, 0, 2; 2025-02: 1, 1, 0; 2025-03: 3, 2, 1.
**Version / licensing note:** from memory, unverified (Microsoft Learn unreachable): USERELATIONSHIP is a standard DAX function; the measure was not run here.
**Edge cases:** E6 has a leave date before the join date; flag such rows in a data-quality check. The leave date must be in the date table range. Blank leave dates are ignored.
**Likely follow-ups:** 1) *Why not two active relationships?* Power BI allows one active path. 2) *Headcount at month end?* Cumulative hires minus cumulative leavers up to that date.
**Common mistakes:** Making both relationships active; using the leave date column in the visual axis directly; forgetting leavers are filtered by a different date.

### Q61 ⭐ 🟡 How would you count employees who joined in the last 90 days and are still on probation?
**Asked at:** commonly asked (no company-specific report found); an HR measure from standard practice.
**What the interviewer is checking:** Combining date logic and status filters correctly in CALCULATE.
**Say this in the interview:** "I filter the employee table to join date within the last 90 days up to the reporting date, status equal to Probation, and no leave date, then count rows."
**Explain simply:**
- Last 90 days means join date after (reporting date minus 90) and up to the reporting date.
- Use a fixed as-of date or TODAY(); a fixed one is safer for reproducing numbers.
- A person who has left should not count, so check that the leave date is blank.
- COUNTROWS counts employee rows (one per employee).
**Example:** As of 30 June 2025, 90 days back is 1 April 2025.
**Sample data:** Table `Employees`:

| Emp | JoinDate | Status | Left |
|---|---|---|---|
| E1 | 2025-06-20 | Probation | No |
| E2 | 2025-05-15 | Probation | No |
| E3 | 2025-04-10 | Probation | No |
| E4 | 2025-06-01 | Confirmed | No |
| E5 | 2025-03-01 | Probation | No |
| E6 | 2025-05-02 | Probation | Yes |

**DAX / Steps:** (not run here)
```dax
Probation Joiners 90d =
VAR AsOf = TODAY()      -- or a fixed date, e.g. DATE(2025,6,30)
RETURN CALCULATE(
    COUNTROWS(Employees),
    Employees[JoinDate] > AsOf - 90,
    Employees[JoinDate] <= AsOf,
    Employees[Status] = "Probation",
    Employees[Left] = "No"
)
```
**Alternative:** Add a calculated column `IsNewProbation` in Power Query and sum it; or use DATESINPERIOD on the date table for a date-slicer-aware version.
**Result:** reproduced with pandas for as-of 30 June 2025: 3 (E1, E2, E3).
**Pandas check:**
```python
import pandas as pd
asof=pd.Timestamp("2025-06-30")
e=pd.DataFrame({"Emp":["E1","E2","E3","E4","E5","E6"],"Join":pd.to_datetime(["2025-06-20","2025-05-15","2025-04-10","2025-06-01","2025-03-01","2025-05-02"]),
 "Status":["Probation"]*3+["Confirmed","Probation","Probation"],"Left":[False]*5+[True]})
m=(e.Join>asof-pd.Timedelta(days=90))&(e.Join<=asof)&(e.Status=="Probation")&(~e.Left)
print(e[m].Emp.tolist(), m.sum())
```
Output (run): `['E1', 'E2', 'E3'] 3`
**Version / licensing note:** from memory, unverified (Microsoft Learn unreachable).
**Edge cases:** "Last 90 days" boundary (>= vs >) must be agreed; TODAY() changes daily, so a report that looks stable will change (see Q46); extended probations make the status column better than a date rule.
**Likely follow-ups:** 1) *Why not rely on 90 days alone?* Probation length differs by grade. 2) *Slicer-driven version?* Use the date table's MAX date as AsOf.
**Common mistakes:** Forgetting leavers; using >= on a boundary and counting 91 days; mixing a date-time column so the time part breaks the comparison.

### Q62 ⭐ 🟡 How would you flag overtime above a threshold in red in a table visual?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know conditional formatting and when to drive it from a measure?
**Say this in the interview:** "I use conditional formatting on the overtime column, a rule that says if the value is above 40 hours, red. If the threshold is dynamic I write a small measure that returns a colour and format by field value."
**Explain simply:**
- Conditional formatting changes colour of a cell based on its value (a rule or a field).
- Rules: simple, readable, set in the dialog.
- Field value: a DAX measure returns the colour code; flexible for per-person thresholds.
- Test on realistic data, and also check colour-blind visibility (add an icon).
**Example:** Overtime above 40 hours a month shows red; 38 stays plain.
**DAX / Steps:** (click-path, not run here)
1. Select the table visual > Format visual > Cells > Cell elements (or Visualizations pane > field dropdown > Conditional formatting).
2. Choose Background color or Font color > fx.
3. Format style: Rules; If value is greater than 40, then red; OK.
```dax
Overtime Colour = IF([Overtime Hours] > [Threshold], "#C00000", BLANK())
```
Then use Format style: Field value, based on `Overtime Colour`.
**Alternative:** Icons (a red flag) instead of a fill colour, or a KPI visual.
**Version / licensing note:** from memory, unverified (Microsoft Learn unreachable). Menu names change between Desktop releases.
**Edge cases:** A total row can also turn red if you do not restrict formatting; blank values should not be coloured; threshold stored in a measure follows filters.
**Likely follow-ups:** 1) *Can I colour a whole row?* Apply the same formatting to each column. 2) *Why the measure approach?* One place to change the threshold.
**Common mistakes:** Applying a rule to the sum when the rule should be on each row; relying on colour alone; hard-coding the threshold in several places.

### Q63 ⭐ 🟡 How would you build an executive summary page with drill-through to employee-level detail?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Layout of a summary page and the drill-through feature.
**Say this in the interview:** "The summary page has 4-5 KPI cards and two trend or breakdown charts. A separate detail page has a drill-through field, such as department, so a right-click on any department opens a table of employees filtered to it."
**Explain simply:**
- Executive page: headline KPIs (headcount, attrition %, open roles), a trend, one breakdown; little text.
- Drill-through: a hidden detail page that receives a filter when you right-click a data point.
- Add a Back button; keep detail pages hidden from the tab bar.
- Respect privacy: employee-level pages should be restricted (see Q65).
**Example:** Right-click the Sales bar showing 15% attrition, choose Drill through > Employee Detail, to see the 18 leavers listed.
**DAX / Steps:** (click-path, not run here)
1. Add a page "Employee Detail" with a table: name, ID, joined, status.
2. Drag Department into Drill through > Add drill-through fields here (Visualizations pane).
3. Insert > Buttons > Back.
4. Hide the page (right-click tab > Hide page).
5. On the summary page, right-click a bar > Drill through.
**Alternative:** Report page tooltips for a quick preview, or bookmarks for navigation buttons.
**Version / licensing note:** from memory, unverified (Microsoft Learn unreachable). A "Keep all filters" toggle exists in the drill-through settings (from memory, unverified), so confirm in Desktop.
**Edge cases:** The drill-through field must exist in the detail visuals' filter context; cross-report drill-through is a separate setup; RLS still applies.
**Likely follow-ups:** 1) *Drill-down vs drill-through?* Drill-down stays on the same visual; drill-through jumps to another page. 2) *How do users find it?* Use a visible hint or button.
**Common mistakes:** Cluttered summary; no Back button; exposing salaries on detail pages for everyone.

### Q64 ⭐ 🟡 How would you design one report that works on both desktop and phone?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the Phone layout feature and mobile-first design thinking?
**Say this in the interview:** "I design the desktop pages first, then use Phone layout in Desktop to arrange the key visuals in a single vertical column, KPIs on top, with fewer and larger visuals."
**Explain simply:**
- Phone layout (View > Phone layout) is a separate arrangement of the same visuals for portrait screens.
- Put 3-5 important visuals; drop detail tables.
- Use large cards, short labels, tap-friendly slicers.
- The Power BI mobile app shows the phone layout when available; otherwise users see a shrunk desktop page.
**Example:** Phone layout of the HR report: headcount card, attrition card, attrition by department bar.
**DAX / Steps:** (click-path, not run here)
1. View tab > Phone layout.
2. Drag visuals from the page visuals pane onto the phone canvas, top to bottom.
3. Resize; check in the Power BI mobile app after publishing.
**Alternative:** Build a separate, simpler report for phone users.
**Version / licensing note:** from memory, unverified (Microsoft Learn unreachable). Whether a free or paid licence is needed for the mobile app was not verified.
**Edge cases:** Visuals not placed on the phone canvas do not appear there; drill-through and complex slicers are awkward on a phone.
**Likely follow-ups:** 1) *Does Phone layout change the data?* No, same model. 2) *Test without a phone?* The Desktop canvas preview helps; test in the app too.
**Common mistakes:** Shrinking the full desktop page; too many visuals; tiny fonts.

### Q65 ⭐ 🟡 How would you hide salary details from some users while letting them see the rest of the HR report?
**Asked at:** RLS in general was reportedly asked in a Deloitte round (Sept 2025) and an older Cognizant report from 2022 (research/interview_processes.md, unverified); this exact question: no company-specific report found.
**What the interviewer is checking:** Row-level security vs object-level security vs designing the report to avoid exposure.
**Say this in the interview:** "RLS hides rows, so for a column I would use object-level security to hide the Salary column from a role, set up in Tabular Editor. If that is not available, I split salary into a separate report or dataset with its own access."
**Explain simply:**
- Hiding a visual or page is not security; anyone with edit access or Analyze in Excel can still reach the data.
- Object-level security (OLS) hides a table or column from a role (the column is invisible and queries on it fail for that role). It is set with external tools (Tabular Editor) not the Desktop menus (from memory, unverified).
- Alternative: separate semantic model for salary, shared only with HR leads.
- Aggregate salary bands rather than exact salaries for broader viewers.
**Example:** Managers see headcount, attrition and tenure; only HR Business Partners see salary cost.
**DAX / Steps:** (not run here)
1. Create role "Managers" in Manage roles (RLS rows as needed).
2. Open the model in Tabular Editor > role > Table Permissions > Employees[Salary] = None.
3. Publish; add managers to the role; test with Test as role.
**Alternative:** A second dataset only for payroll, or masking with salary bands via a calculated column.
**Version / licensing note:** from memory, unverified (Microsoft Learn unreachable); OLS support and the tool requirement should be checked on the OLS page.
**Edge cases:** Visuals using the hidden column show an error for restricted users; measures built on Salary may also fail; workspace editors bypass roles.
**Likely follow-ups:** 1) *Is a hidden visual secure?* No. 2) *Can RLS alone do it?* No, it filters rows, not columns.
**Common mistakes:** Hiding the column in the report view and calling it secure; testing only as the owner.

### Q66 ⭐ 🟡 How would you decide between a Power BI report and a paginated report for a 40-page monthly pack?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Matching the tool to need: interactive exploration vs fixed-layout printing.
**Say this in the interview:** "If people explore and filter, a Power BI report. If it must print or export as a fixed 40-page PDF with exact layout, repeating headers and long tables, a paginated report."
**Explain simply:**
- Power BI reports are interactive: slicers, cross-filtering, on screen.
- Paginated reports (built with Power BI Report Builder) are pixel-perfect and span pages, ideal for invoices, payslips, statements.
- Paginated reports are authored in Report Builder (a free separate tool) and, in the Service, need a capacity (Premium or Fabric) or PPU (from memory, unverified).
- Decide on: audience, export need, row volume, subscriptions by email.
**Example:** The monthly payroll pack per department with the same layout and a PDF per manager: paginated. The HR leadership dashboard: standard report.
**DAX / Steps:** (decision steps)
1. List requirements (print, exact layout, page count).
2. If fixed layout: Report Builder > connect to the semantic model > design > publish.
3. If exploration: Desktop report.
**Alternative:** Use both: a dashboard for exploration plus a paginated pack for the archive.
**Version / licensing note:** from memory, unverified: Microsoft Learn was unreachable; the licence and capacity requirement for paginated reports needs checking.
**Edge cases:** A 40-page pack may be better as one paginated report with subscriptions per recipient; very large exports have time and size limits.
**Likely follow-ups:** 1) *Can paginated reports be interactive?* Only a little (parameters, drill). 2) *Can Excel export do it?* Possible but not formatted.
**Common mistakes:** Forcing 40 pages into a normal report; ignoring licensing.

### Q67 ⭐ 🟡 How would you show the top 5 customers and group everyone else as Others so the chart still adds up to total sales?
**Asked at:** commonly asked (no company-specific report found); not seen in a source.
**What the interviewer is checking:** Can you build a disconnected group table and TOPN so the chart totals match?
**Say this in the interview:** "I create a small helper table with each customer name plus one row 'Others'. A measure returns the customer's sales if they are in the top 5, and for the 'Others' row it returns total sales minus the top 5 total, so the bars add to the total."
**Explain simply:**
- A normal Top N visual filter drops everyone else, so the total shrinks.
- A disconnected table has no relationship; it only supplies labels for the visual.
- TOPN returns the top 5 rows by a measure; Others is total minus top 5.
**Example:** Total 3,400; top five add up to 2,800; Others = 600.
**Sample data:** Table `Customers` with total sales:

| Customer | Sales |
|---|---|
| A | 900 |
| B | 700 |
| C | 500 |
| D | 400 |
| E | 300 |
| F | 250 |
| G | 200 |
| H | 150 |

**DAX / Steps:** (not run here)
```dax
-- helper (calculated table), no relationships
Group = UNION(SELECTCOLUMNS(ALL(Customers[Customer]), "Customer", Customers[Customer]), ROW("Customer", "Others"))

Grouped Sales =
VAR Top5 = TOPN(5, ALLSELECTED(Customers[Customer]), [Total Sales])
VAR Cur = SELECTEDVALUE('Group'[Customer])
VAR AllSales = CALCULATE([Total Sales], ALLSELECTED(Customers))
VAR Top5Sales = SUMX(Top5, [Total Sales])
RETURN
IF(Cur = "Others", AllSales - Top5Sales,
   IF(Cur IN SELECTCOLUMNS(Top5, "c", Customers[Customer]),
      CALCULATE([Total Sales], TREATAS({Cur}, Customers[Customer]))))
```
Visual: bar chart with `Group[Customer]` on the axis and `Grouped Sales` as the value.
**Alternative:** In Power Query, rank customers, and replace the name of rank > 5 with "Others" (static; does not follow slicers).
**Result:** reproduced with pandas: A 900, B 700, Others 600, C 500, D 400, E 300; sum 3,400 equals total 3,400. (Others is the sum of F, G, H.) Note: sorted order places Others in the middle, so sort manually to last in the chart.
**Pandas check:**
```python
import pandas as pd, numpy as np
c=pd.DataFrame({"Cust":list("ABCDEFGH"),"Sales":[900,700,500,400,300,250,200,150]}).sort_values("Sales",ascending=False)
c["Grp"]=np.where(np.arange(len(c))<5,c.Cust,"Others"); g=c.groupby("Grp").Sales.sum().sort_values(ascending=False)
print(g, g.sum(), c.Sales.sum())
```
Output (run): A 900, B 700, Others 600, C 500, D 400, E 300; 3400 3400.
**Version / licensing note:** from memory, unverified (Microsoft Learn unreachable); the DAX was not run here and the TOPN/TREATAS combination should be tested in Desktop.
**Edge cases:** Ties at rank 5 can return more than 5 rows from TOPN; slicers change who is in the top 5; the helper table has all customers, so filter out blanks.
**Likely follow-ups:** 1) *Why not a visual Top N filter?* It removes the rest. 2) *Static version?* Power Query ranking.
**Common mistakes:** Making a relationship on the helper table; forgetting the sort order; Others calculated from the filtered top list only.

### Q68 ⭐ 🔴 Refresh became slow because a Power Query step stopped folding: how do you find and fix it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand query folding and how to see where it breaks?
**Say this in the interview:** "Query folding means Power Query turns my steps into SQL that the database runs. I right-click each step and check View native query; the first step where it is greyed out is where folding stopped. I move foldable steps before it or replace the step."
**Explain simply:**
- Folding pushes work (filter, group, join) to the source so only the result is downloaded.
- When it breaks, Power Query pulls all rows and does the rest itself, which is slow.
- Find it: Applied Steps > right-click a step > View native query (greyed out means not folded).
- Common breakers: adding an index column, some custom columns, merging queries from different sources, changing type with locale, pivoting in some sources.
- Fix: reorder so folding steps come first, do the unfoldable step in the database (a view), or replace it with an equivalent foldable step.
**Example:** Filter to 2025 after an Index column step: the filter no longer folds, so 50 million rows download first. Moving the filter before the index cuts refresh from 40 to 5 minutes (illustrative).
**DAX / Steps:** (click-path, not run here)
1. Transform data > select the query > Applied Steps.
2. Right-click each step, check View native query.
3. Drag the filter and column-removal steps above the first non-folding step.
4. If needed, create a database view and connect to it.
**Alternative:** Incremental refresh to refresh only recent partitions; it requires foldable filters on RangeStart and RangeEnd (from the research notes' summary of the incremental refresh page, not re-fetched).
**Version / licensing note:** from memory, unverified (Microsoft Learn unreachable). Folding applies to relational sources and some others, not to Excel or CSV files.
**Edge cases:** Folding depends on the source; Excel files cannot fold. Query Diagnostics can show timings.
**Likely follow-ups:** 1) *Why does it matter?* Less data transferred and faster refresh. 2) *Can I force it?* Not really; you can write the SQL yourself as a native query, but later steps may then not fold, depending on the connector (from memory, unverified).
**Common mistakes:** Not checking each step; filtering late; assuming Excel sources fold.

### Q69 ⭐ 🔴 How would you build a joiner-cohort retention view showing how many of each month's hires remain after 3, 6 and 12 months?
**Asked at:** commonly asked (no company-specific report found); an HR measure from practice, verified only in pandas.
**What the interviewer is checking:** Cohort logic: defining a group by join month and a "still here after N months" test.
**Say this in the interview:** "A cohort is everyone hired in the same month. For each, I check whether they were still employed N months after their own join date, and I show the percent against the cohort's hires."
**Explain simply:**
- Cohort = group of people sharing a start month.
- Still employed after N months = leave date is blank or on/after join date plus N months.
- Only count a cohort at N months if that date has passed (otherwise show blank).
- Show as a matrix: cohort rows, columns 3, 6, 12 months.
**Example:** January 2025 cohort of 4: 3 remain after 3 months, 3 after 6, 2 after 12.
**Sample data:** Table `Employees` (as-of 2026-03-31):

| Emp | JoinDate | LeaveDate |
|---|---|---|
| 1 | 2025-01-10 | 2025-03-15 |
| 2 | 2025-01-20 | blank |
| 3 | 2025-01-25 | 2025-08-01 |
| 4 | 2025-01-30 | blank |
| 5 | 2025-02-05 | 2025-04-01 |
| 6 | 2025-02-12 | 2025-05-20 |
| 7 | 2025-02-20 | blank |
| 8 | 2025-02-28 | 2025-10-01 |

**DAX / Steps:** (not run here)
```dax
-- calculated columns on Employees
Retained 3M = IF(Employees[LeaveDate] = BLANK() || Employees[LeaveDate] >= EDATE(Employees[JoinDate], 3), 1, 0)
-- same for 6M and 12M
Hires = COUNTROWS(Employees)
Retained 3M Count = SUM(Employees[Retained 3M])
Retention 3M % = DIVIDE([Retained 3M Count], [Hires])
```
Visual: matrix with Join month (from the date table or EOMONTH(JoinDate,0)) on rows and the three retention measures as values.
**Alternative:** A measure-only version: CALCULATE(COUNTROWS(Employees), FILTER(Employees, Employees[LeaveDate]=BLANK() || Employees[LeaveDate] >= EDATE(Employees[JoinDate],3))). A long-form table with N as a disconnected "Months" slicer is also possible.
**Result:** reproduced with pandas: Jan 2025 cohort 4 hires, 3 / 3 / 2 remain at 3, 6, 12 months; Feb 2025 cohort 4 hires, 3 / 2 / 1 remain.
**Pandas check:**
```python
import pandas as pd
j=pd.DataFrame({"Emp":range(1,9),"Join":pd.to_datetime(["2025-01-10","2025-01-20","2025-01-25","2025-01-30","2025-02-05","2025-02-12","2025-02-20","2025-02-28"]),
 "Leave":pd.to_datetime(["2025-03-15",None,"2025-08-01",None,"2025-04-01","2025-05-20",None,"2025-10-01"])})
rows=[]
for cm,g in j.groupby(j.Join.dt.to_period("M")):
    r=[str(cm),len(g)]
    for k in (3,6,12):
        st=g.Join+pd.DateOffset(months=k); r.append(int((g.Leave.isna()|(g.Leave>=st)).sum()))
    rows.append(r)
print(pd.DataFrame(rows,columns=["Cohort","Hires","Rem3","Rem6","Rem12"]))
```
Output (run): 2025-01: 4, 3, 3, 2; 2025-02: 4, 3, 2, 1.
**Version / licensing note:** from memory, unverified (Microsoft Learn unreachable); EDATE exists in DAX (from memory, unverified).
**Edge cases:** A cohort too young for 12 months (join date plus 12 months after today) must return blank, not 100% (add a check against TODAY()); leavers exactly on the anniversary count as retained here (state your rule); rehires need an employee-level history.
**Likely follow-ups:** 1) *Why columns, not measures?* Per-employee tests are easier to read as columns; measures also work. 2) *Why percent of cohort?* Cohorts differ in size.
**Common mistakes:** Using the report date instead of each person's own join date; counting immature cohorts as fully retained.

### Q70 ⭐ 🔴 The report is fast in Power BI Desktop but users say it is slow in the Service: what do you check?
**Asked at:** commonly asked (no company-specific report found); the optimisation guide (capacity, gateway, RLS, tile caching) is related but I could not re-fetch it.
**What the interviewer is checking:** Do you know what differs between your laptop and shared cloud: capacity, load, network, RLS, data source location?
**Say this in the interview:** "I compare like with like: same filters, same user. Then I check capacity load, whether DirectQuery goes through a gateway, whether RLS is active, network latency and how many visuals load at once. I use Performance Analyzer in the Service."
**Explain simply:**
- Desktop uses your PC's memory with one user; the Service shares capacity (shared or Premium/Fabric) with many users.
- RLS adds filter work for each user and may disable some caching; test as the slow user.
- DirectQuery or live sources through an on-premises gateway add network hops.
- Users far from the data region add latency.
- A heavy page of visuals, or a large model near the memory limit, loads slowly when many open it together.
- Check the Capacity Metrics app (Premium/Fabric admins) for spikes (from memory, unverified).
**Example:** Desktop 2 seconds; Service 15 seconds for a manager with RLS across 300 departments, because the DirectQuery source sits behind a gateway on a busy server.
**DAX / Steps:** (click-path, not run here)
1. Open the report in the Service > Edit > View > Performance analyzer (from the research notes; not re-verified).
2. Test as the slow user (Test as role) and compare.
3. Check gateway server CPU/memory and connection mode.
4. Reduce visuals, add Apply buttons, summarise data (Q49).
5. Ask the admin about capacity load and data region.
**Alternative:** Schedule off-peak refresh, enable caching, or upgrade capacity.
**Version / licensing note:** from memory, unverified (Microsoft Learn unreachable). Performance Analyzer in the Service edit mode and capacity metrics are noted in research/Book04_Part09_sources.md from fetched pages, which I did not re-read here.
**Edge cases:** Refreshing during the day competes with queries; first open after idle is slower (cold cache); different browsers and VPN affect speed.
**Likely follow-ups:** 1) *Is Desktop speed a good test?* Only for the model and DAX. 2) *What about Import vs DirectQuery?* Import is usually faster in the Service.
**Common mistakes:** Testing only as the author; blaming the report when the gateway is the bottleneck; ignoring RLS.
