# Book 4 — Power BI & Visualization | Part 10: Tableau Basics and Power BI vs Tableau 🟢🟡

**Target:** 40 questions | **Actual:** 43 questions
**Scope:** Tableau fundamentals a 0-3 year analyst may be asked (fields, filters, LOD, connections, products) and Power BI vs Tableau comparisons.

### Q1 ⭐⭐⭐ 🟢 What is Tableau, and what is it used for?
**Asked at:** commonly asked (no company-specific report found); it is the opener in the Tableau prep lists we found (Hyring 2026, Interview Kickstart). research/interview_processes.md records Tableau rounds at Wells Fargo, Indium, LatentView and Infosys, but not this exact question.
**What the interviewer is checking:** Can you explain a BI tool in one clear sentence and name its main use?
**Say this in the interview:** "Tableau is a business intelligence tool. You connect it to data, drag fields onto a canvas to build charts, and combine charts into interactive dashboards that managers can filter and explore without writing code."
**Explain simply:**
- **BI (business intelligence)** means turning raw data into charts and tables that help decisions.
- You drag-and-drop fields; Tableau writes the query for you.
- Typical outputs: a headcount dashboard, an attrition trend, a sales-by-region map.
- It competes directly with Power BI; both do the same job with different strengths (Q3).
**Example:** An HR team loads an employee file of 5,000 rows and builds a one-page dashboard: headcount by department, monthly attrition line, and a filter for location.
**Sample data / DAX:** not applicable (concept question).
**Version / licensing note:** from memory, unverified (help.tableau.com could not be fetched in this session).
**Edge cases:** Tableau is for analysing and presenting data; it is not a database and not a data-cleaning tool (that is Tableau Prep, Q28 in this part).
**Likely follow-ups:** 1) *Name its products?* Desktop, Public, Cloud, Server, Prep (Q6). 2) *How is it different from Excel?* It handles bigger data and gives interactive dashboards, but has no cell-by-cell formulas.
**Common mistakes:** Calling it a "database" or a "programming language".

### Q2 ⭐⭐⭐ 🟢 What is the difference between a dimension and a measure in Tableau?
**Asked at:** commonly asked (no company-specific report found); appears in every prep list reviewed.
**What the interviewer is checking:** Do you know which fields slice the data and which get added up?
**Say this in the interview:** "A dimension is a category I use to split the data, like Department or Month. A measure is a number I calculate on, like Salary or Headcount. Dimensions make the rows and columns, measures fill in the values."
**Explain simply:**
- **Dimension:** descriptive, usually text or dates. Tableau lists them in the upper part of the Data pane.
- **Measure:** numeric and aggregated (SUM, AVG, COUNT). Listed in the lower part of the Data pane.
- Tableau guesses the role from the data type; you can override it, for example treat Employee ID as a dimension, not a measure.
- Dimension/measure is a different idea from blue/green (Q4).
**Example:** Rows = Department (dimension), values = AVG(Salary) (measure). Result: one bar per department showing average pay.
**Version / licensing note:** from memory, unverified. The sources file lists the Tableau Help "Dimensions and Measures, Blue and Green" page only as a search snippet, so I did not rely on it.
**Edge cases:** A numeric ID such as EmpID is stored as a number but should be a dimension; summing it is meaningless. A count of employees can be made by `COUNTD(EmpID)`.
**Likely follow-ups:** 1) *Can a dimension become a measure?* Yes, via Count or Count Distinct. 2) *What are "Measure Names/Values"?* Tableau's built-in fields for putting several measures in one view.
**Common mistakes:** Summing a numeric ID; thinking "number = measure" always.

### Q3 ⭐⭐⭐ 🟡 What are the main differences between Power BI and Tableau, and which would you pick for a company?
**Asked at:** commonly asked as a comparison question (Dataford, InterviewBit-type lists; no company-specific report found). One third-party snippet claimed Tableau uses "MDX" for measures; that is wrong or unverified and I did not use it.
**What the interviewer is checking:** Can you compare tools fairly and tie the choice to the company's situation, not personal taste?
**Say this in the interview:** "Both are strong. Power BI fits best if the company already uses Microsoft 365, Excel and Azure, and wants lower per-user cost. Tableau is often praised for flexible visual exploration and has a large public community. I would choose by existing stack, budget, skills in the team and governance needs."
**Explain simply:**
- **Ecosystem:** Power BI plugs into Excel, Teams, SharePoint; Tableau is vendor-neutral and now part of Salesforce.
- **Calculation language:** Power BI uses DAX (measures) plus Power Query (cleaning); Tableau uses calculated fields, LOD expressions and table calculations.
- **Data prep:** Power BI has Power Query built in; Tableau has a separate product, Tableau Prep.
- **Platform:** Power BI Desktop runs on Windows only (from memory, unverified); Tableau Desktop installs on Windows and macOS (from memory, unverified).
- **Cost:** per-user licences differ; check current price pages (Q38).
**Example:** A 300-person company with Microsoft 365 and Excel-trained HR staff: Power BI, because licences, sign-in and sharing through Teams are already there.
**Version / licensing note:** from memory, unverified (Tableau Help and Microsoft Learn were unreachable). No prices quoted; they change.
**Edge cases:** If half the company already has Tableau skills and licences, switching tools costs more than it saves.
**Likely follow-ups:** 1) *Which is easier to learn?* See Q14. 2) *Can they coexist?* Yes, but reconciling numbers needs care (Q42).
**Common mistakes:** Declaring a "winner" without asking about the company's stack; repeating marketing claims.

### Q4 ⭐⭐ 🟢 Why are some Tableau pills blue and some green (discrete vs continuous)?
**Asked at:** commonly asked (no company-specific report found); present in Hyring and Interview Kickstart lists.
**What the interviewer is checking:** Do you know how Tableau draws headers versus axes?
**Say this in the interview:** "Blue means discrete: separate, countable buckets that become headers or labels. Green means continuous: an unbroken range that becomes an axis. It is independent of dimension versus measure."
**Explain simply:**
- **Discrete (blue):** each value is its own box, like Department names or the month name "Jan".
- **Continuous (green):** values run along a scale, like salary or a true date line.
- A date can be either: "Month" (the name, blue) gives one bar per month; "Month" as a continuous date (green) gives a smooth line along a time axis.
- Right-click a pill and choose Discrete or Continuous to switch.
**Example:** Dragging Join Date to Columns as blue Month gives 12 separate columns across years merged by month name; as green Month gives a continuous timeline Jan 2024 ... Dec 2025.
**Version / licensing note:** from memory, unverified.
**Edge cases:** Blue pills in the Rows/Columns create headers; green pills create axes. A green measure with SUM is the usual case, but a measure can be made discrete (then it acts like a label).
**Likely follow-ups:** 1) *Which do dimensions usually default to?* Blue. 2) *Which do measures default to?* Green.
**Common mistakes:** Saying "blue = dimension, green = measure" as if it were a rule; it is only the default.

### Q5 ⭐⭐ 🟢 What is the difference between a worksheet, a dashboard and a story in Tableau?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know Tableau's three building layers?
**Say this in the interview:** "A worksheet is one chart or table. A dashboard arranges several worksheets on one page with filters and actions. A story is a sequence of sheets or dashboards that walks the viewer through a narrative, one step at a time."
**Explain simply:**
- **Worksheet:** a single view; where you build and test one chart.
- **Dashboard:** a canvas combining worksheets, text, images, filters and buttons.
- **Story:** ordered "story points", each holding a sheet or dashboard with a caption.
- Power BI equivalent: a visual on a report page, a report page, and bookmarks / report navigation (stories have no exact twin).
**Example:** Worksheet 1: attrition by department; Worksheet 2: monthly trend; Dashboard: both plus a location filter; Story: "Why attrition rose in Q3", four steps with comments.
**Version / licensing note:** from memory, unverified.
**Edge cases:** Dashboard filters can apply to all worksheets on the dashboard or only selected ones.
**Likely follow-ups:** 1) *Which do executives use?* Usually the dashboard. 2) *Are stories common?* Less than dashboards.
**Common mistakes:** Putting every chart on one dashboard instead of one message per dashboard.

### Q6 ⭐⭐ 🟢 What are the Tableau products (Desktop, Public, Cloud, Server, Prep) and when is each used?
**Asked at:** commonly asked (no company-specific report found); Interview Kickstart lists the products.
**What the interviewer is checking:** Can you place each tool in the build, publish, share chain?
**Say this in the interview:** "Desktop is where analysts build. Public is a free version that publishes to the open web, so only for non-sensitive data. Cloud is Tableau's hosted service for sharing; Server is the same idea hosted by the company itself. Prep is a separate tool for cleaning and reshaping data before analysis."
**Explain simply:**
- **Desktop:** author workbooks; paid.
- **Public:** free; everything you publish is visible to anyone on the internet (Q26 covers why that matters). The sources file records that Public Edition is non-commercial, per an earlier Tableau Help fetch summary; not re-verified by me.
- **Cloud:** SaaS (software run by the vendor) for sharing, scheduling refresh and permissions.
- **Server:** self-hosted on the company's own machines, so the IT team maintains it.
- **Prep:** visual data cleaning with flows.
**Example:** An analyst builds in Desktop, publishes to Cloud, and HR leaders view it in a browser. Messy attendance files go through Prep first.
**Version / licensing note:** from memory, unverified (product names and bundles change; Tableau Help not reachable).
**Edge cases:** Some products have been renamed over time (Cloud was formerly called Online), so say "Tableau Cloud (formerly Online)".
**Likely follow-ups:** 1) *Cloud vs Server?* Hosted vs self-hosted (Q39). 2) *Is there a Reader?* Older free viewer; not needed now.
**Common mistakes:** Treating Public as a trial of Desktop for company data.

### Q7 ⭐⭐ 🟢 What is the difference between a live connection and an extract in Tableau?
**Asked at:** commonly asked (no company-specific report found); Interview Kickstart includes extract topics.
**What the interviewer is checking:** Can you trade off freshness against speed?
**Say this in the interview:** "Live reads the database every time someone opens or filters the dashboard, so it is always current but depends on the database's speed. An extract is a compressed snapshot stored by Tableau that I refresh on a schedule; it is usually faster and works offline."
**Explain simply:**
- **Live:** real-time, slower if the database is slow; load lands on the source system.
- **Extract (.hyper file):** a snapshot; fast; data is only as fresh as the last refresh.
- Extracts can be filtered or aggregated before saving (Q33).
- Power BI parallel: DirectQuery vs Import.
**Example:** A daily attendance dashboard on a slow HR database: use an extract refreshed at 6 a.m. For a real-time hiring board that must show today's applications: live.
**Version / licensing note:** from memory, unverified. Scheduling extract refresh on Cloud/Server needs published workbooks (licence details not verified).
**Edge cases:** An extract can fail if the source schema changes (a renamed column); refresh then breaks.
**Likely follow-ups:** 1) *When live?* Needs real-time or data too big to extract. 2) *Import vs DirectQuery?* Same trade-off in Power BI.
**Common mistakes:** Believing extracts update by themselves.

### Q8 ⭐⭐ 🟢 What is a calculated field in Tableau? Give an example.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you write a basic formula in Tableau and know it makes a new field?
**Say this in the interview:** "A calculated field is a new column I define with a formula, like Excel but applied to every row or to aggregates. For attrition I would create a Left Flag: IF [Status]='Left' THEN 1 ELSE 0 END, and average it."
**Explain simply:**
- Created via Analysis > Create Calculated Field.
- Row-level fields compute per row; aggregate fields (SUM, AVG) compute after grouping.
- Types: number, string, date, boolean.
- Power BI parallel: calculated column or measure.
**Example:** Employee table: 8 people, 3 with Status = Left. Calculated field `Left Flag` gives 0/1; `AVG([Left Flag])` over a department gives its attrition rate.
**Sample data:** Table `Employees`

| EmpID | Dept | Salary | Status |
|---|---|---|---|
| E1 | Sales | 50000 | Active |
| E2 | Sales | 70000 | Left |
| E3 | Sales | 60000 | Active |
| E4 | HR | 40000 | Active |
| E5 | HR | 44000 | Left |
| E6 | IT | 90000 | Active |
| E7 | IT | 110000 | Active |
| E8 | IT | 100000 | Left |

**DAX / Steps:** Tableau calculated fields (not run here, Tableau is not available).
1. Analysis > Create Calculated Field, name `Left Flag`.
2. Formula: `IF [Status] = "Left" THEN 1 ELSE 0 END`
3. Second field `Attrition %`: `AVG([Left Flag])`, format as percentage.
**Alternative:** `SUM(IF [Status]="Left" THEN 1 END) / COUNTD([EmpID])`.
**Result:** Reproduced with pandas: HR 50.0%, IT 33.3%, Sales 33.3%.
**Pandas check:**
```python
emp["Left"]=(emp.Status=="Left").astype(int)
g=emp.groupby("Dept").agg(Total=("EmpID","count"),Left=("Left","sum"))
g["Attr%"]=(g.Left/g.Total*100).round(1)
```
Printed output:
```
       Total  Left  Attr%
HR         2     1   50.0
IT         3     1   33.3
Sales      3     1   33.3
```
**Version / licensing note:** from memory, unverified.
**Edge cases:** NULL in `[Status]` goes to ELSE (0), which undercounts if the real value is unknown. Division by zero in aggregate formulas when a department has no employees.
**Likely follow-ups:** 1) *Row-level vs aggregate?* Aggregates cannot mix with row-level unless wrapped in ATTR/LOD. 2) *Table calc?* Q20.
**Common mistakes:** Mixing aggregated and non-aggregated arguments (the "cannot mix aggregate and non-aggregate" error).

### Q9 ⭐⭐ 🟢 What is the difference between a filter and a parameter in Tableau?
**Asked at:** commonly asked (no company-specific report found); Wells Fargo accounts in research/interview_processes.md mention filters generally.
**What the interviewer is checking:** Do you know a filter removes data while a parameter is a user-chosen value that formulas can read?
**Say this in the interview:** "A filter removes rows from the view based on a field. A parameter is a single value the user picks, like a threshold or a measure choice, and it does nothing until a calculation or filter uses it."
**Explain simply:**
- **Filter:** works on a field; shows or hides records.
- **Parameter:** a standalone value (number, text, date, list); not tied to a field.
- Parameters let users switch the measure shown or set a cut-off, for example "show departments above X% attrition".
- Power BI parallel: slicer is like a filter; a what-if parameter or field parameter is like a Tableau parameter.
**Example:** Parameter `Attrition Threshold` = 10%. Calc field `[Attrition %] >= [Attrition Threshold]` highlights departments over 10%.
**Version / licensing note:** from memory, unverified.
**Edge cases:** A parameter's value is fixed on the workbook; it does not update when data changes unless you refresh it (newer versions can auto-update lists, unverified).
**Likely follow-ups:** 1) *Can a parameter filter?* Only via a calculated field. 2) *Parameter actions?* Let a click set the parameter.
**Common mistakes:** Making a parameter and expecting it to filter by itself.

### Q10 ⭐⭐ 🟢 What is the difference between sets and groups in Tableau?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you tell a fixed bundle of members from a rule-based in/out split?
**Say this in the interview:** "A group combines several members of one dimension into one named bucket, like putting South and West into 'Rest of India'. A set divides members into In and Out, and can be dynamic, for example 'top 10 employees by salary'."
**Explain simply:**
- **Group:** manual merging of members into new labels; static.
- **Set:** a Yes/No membership. It can be fixed (hand-picked) or computed by a condition or Top N.
- Sets can be compared (In vs Out) and combined; groups cannot.
- Power BI parallel: grouping (Data groups) vs a calculated column or measure with a condition.
**Example:** Group departments Finance + Admin into "Support". Set "High earners" = employees with Salary above 100,000 gives In/Out.
**Version / licensing note:** from memory, unverified. The sources file cites Tableau's order of operations as treating sets as an early step; I could not re-verify it.
**Edge cases:** Group members not listed are put in "Other" if you enable it.
**Likely follow-ups:** 1) *Dynamic set?* Re-evaluates as data changes. 2) *Combined set?* Union, intersection, difference of two sets.
**Common mistakes:** Using a group when a rule-based set is needed (breaks when new members arrive).

### Q11 ⭐⭐ 🟢 What is the difference between a join and a blend in Tableau?
**Asked at:** frequently asked; research/interview_processes.md records blending as a topic in the Wells Fargo Tableau account (not this exact question).
**What the interviewer is checking:** Do you know join combines rows before aggregation, blend combines results after aggregation?
**Say this in the interview:** "A join merges two tables at the row level inside one data source, using a key. A blend keeps two separate data sources, aggregates each, and then links the results on a linking field. Blending is useful when data lives in different sources that cannot be joined."
**Explain simply:**
- **Join:** row-level, inner/left/right/full, one combined table; risk: row duplication (Q43).
- **Blend:** the primary source drives the view; the secondary data is pulled in per matching value of the link field; looks like a left join of aggregates.
- A blend aggregates the secondary source, so it avoids fan-out but gives less flexibility.
- Newer Tableau favours relationships (Q32) over both for many cases.
**Example:** Headcount in an HR database, hiring targets in an Excel sheet by department. Blend on Department to show actual vs target without a join.
**Version / licensing note:** from memory, unverified.
**Edge cases:** A blend link field must exist in the view (or be marked), and the secondary source cannot be used for row-level calculations in the primary.
**Likely follow-ups:** 1) *Blend performance?* Fine for small secondary data, slow if it has many link values. 2) *When prefer join?* Same database, row-level need.
**Common mistakes:** Joining at a different grain and doubling numbers.

### Q12 ⭐⭐ 🟢 What is the difference between .twb and .twbx files in Tableau?
**Asked at:** commonly asked (no company-specific report found); Interview Kickstart includes file types.
**What the interviewer is checking:** Do you know when a workbook can be shared by itself?
**Say this in the interview:** ".twb is a small XML text file that holds the workbook's definition but not the data; it needs access to the original source. .twbx is a packaged workbook: it zips the .twb with local data files and images, so you can send it to someone and it opens."
**Explain simply:**
- **.twb:** workbook definition only.
- **.twbx:** workbook plus extracts, local files and images.
- Other file types you may mention: .tds / .tdsx (data sources), .hyper (extract), .tde (older extract).
- Power BI parallel: .pbix holds model and data together; .pbit is a template (from memory, unverified).
**Example:** Emailing an attendance dashboard built on a local Excel file: send .twbx, because a .twb would open with a broken connection.
**Version / licensing note:** from memory, unverified.
**Edge cases:** A .twbx with an extract can be large; the .twb for a live database connection is tiny.
**Likely follow-ups:** 1) *Which is better for version control?* .twb is text-based. 2) *Does .twbx contain database data?* Only an extract, not the whole database.
**Common mistakes:** Sending a .twb that points to a file on the author's laptop.

### Q13 ⭐⭐ 🟢 Which chart would you use to show attrition by department in Tableau, and how do you build it?
**Asked at:** gap-fill HR question (not seen in any source as phrased).
**What the interviewer is checking:** Can you pick a simple chart and build it fast, sorted and labelled?
**Say this in the interview:** "A sorted horizontal bar chart: one bar per department, length equals attrition percentage, sorted high to low, with a line for the company average. Bars are the clearest way to compare categories."
**Explain simply:**
- **Attrition %** = employees who left / total employees in the group.
- Use the calculated field from Q8 so the percentage is correct per department.
- Avoid pie charts: the slices are hard to compare.
- Add a reference line (Q31) at the company average (3 of 8 = 37.5%).
**Example:** Using the Q8 table: HR 50.0%, IT 33.3%, Sales 33.3%; company average 37.5%. HR stands out.
**Sample data:** Same `Employees` table as Q8.
**DAX / Steps:** Tableau click-path (not run here).
1. Connect to the data.
2. Create `Left Flag` (Q8) and `Attrition %` = `AVG([Left Flag])`.
3. Drag Department to Rows and Attrition % to Columns.
4. Sort descending (toolbar sort icon).
5. Format Attrition % as a percentage; add labels (Marks > Label).
6. Analytics pane > drag Reference Line > Per Pane > Average.
**Alternative:** A bar chart of `Left` and `Active` counts stacked, but the percentage is easier to compare when team sizes differ.
**Result:** Reproduced with pandas (Q8): HR 50.0, IT 33.3, Sales 33.3 percent.
**Pandas check:** same code and output as Q8.
**Version / licensing note:** from memory, unverified.
**Edge cases:** Tiny departments produce wild percentages (1 of 2 = 50%); show headcount in a tooltip. Average of department percentages is not the company rate unless sizes are equal.
**Likely follow-ups:** 1) *Trend over time?* Q25. 2) *Why bars not pie?* Easier length comparison.
**Common mistakes:** Showing counts only; averaging percentages across departments.

### Q14 ⭐⭐ 🟢 Which is easier to learn for an HR professional moving into analytics, Power BI or Tableau, and why?
**Asked at:** gap-fill style opinion question (commonly asked, no company-specific report found).
**What the interviewer is checking:** Honest, reasoned judgement without tool bias.
**Say this in the interview:** "For an HR professional who already uses Excel, I find Power BI easier to start with because the interface, Power Query and DAX feel like Excel. Tableau is very friendly for drag-and-drop charts, but its calculation ideas, like LOD expressions, take extra time. Either is learnable in a few months; I would start with what job ads in my target companies ask for."
**Explain simply:**
- Power BI: free Desktop, huge free learning content, Excel-like formulas; DAX has a learning curve.
- Tableau: very intuitive for charts; calculation model (LOD, table calcs, order of operations) is the steep part.
- In the market data from this project, Tableau appeared in 33% of pooled job posts (n=186) and 12.5% of the 0-2-year sample (5 of 40), mostly as "good to have" next to Power BI (research/market_skills_2026.md via the sources file).
- So: learn Power BI first, Tableau basics second.
**Example:** An HR analyst with strong pivot-table skills can build a Power BI headcount report in a week; the same person finds Tableau's pills and blue/green logic new.
**Version / licensing note:** from memory, unverified.
**Edge cases:** If your target employer uses Tableau, reverse the order.
**Likely follow-ups:** 1) *Which pays more?* Not supported by any source here. 2) *Can you do both?* Yes, the concepts transfer (Q22, Q23).
**Common mistakes:** Claiming one tool is "dead"; answering without referring to job requirements.

### Q15 ⭐⭐ 🟡 What is a dual-axis chart in Tableau, and how do you create one?
**Asked at:** commonly asked (no company-specific report found); Interview Kickstart includes dual axis.
**What the interviewer is checking:** Can you combine two measures with different scales in one chart?
**Say this in the interview:** "A dual-axis chart overlays two measures on one view with separate left and right axes, for example headcount as bars and attrition % as a line. I put both measures on Rows, right-click the second and choose Dual Axis, then change mark types and synchronise axes only if the scales mean the same thing."
**Explain simply:**
- Useful when two measures have very different scales (hundreds of people vs a percentage).
- Each measure keeps its own Marks card, so one can be a bar and the other a line.
- **Synchronise axis** forces both to use the same scale; do this only for same-unit measures.
- Power BI parallel: Line and clustered column chart.
**Example:** Monthly closing headcount (bars) and attrition % (line) for Jan-Apr.
**Sample data:** Table `Monthly` (attrition % = Leavers / average of opening and closing headcount)

| Month | Open | Joiners | Leavers | Close | Attrition % |
|---|---|---|---|---|---|
| Jan | 200 | 2 | 6 | 196 | 3.03 |
| Feb | 196 | 13 | 4 | 205 | 2.00 |
| Mar | 205 | 5 | 10 | 200 | 4.94 |
| Apr | 200 | 8 | 5 | 203 | 2.48 |

**DAX / Steps:** Tableau click-path (not run here).
1. Month (continuous or discrete) to Columns.
2. Drag Close headcount to Rows, then Attrition % next to it on Rows.
3. Right-click the second pill > Dual Axis.
4. In Marks, set the first to Bar and the second to Line.
5. Do not tick Synchronize Axis here (units differ).
**Alternative:** Two stacked worksheets sharing the Month axis (Rows stacked), which avoids misleading overlays.
**Result:** Reproduced with pandas: closing headcount 196, 205, 200, 203; attrition 3.03%, 2.00%, 4.94%, 2.48%.
**Pandas check:**
```python
m["Close"]=m.Open+m.Joiners-m.Leavers
m["Avg"]=(m.Open+m.Close)/2
m["Attr%"]=(m.Leavers/m.Avg*100).round(2)
```
Printed: Attr% = 3.03, 2.00, 4.94, 2.48; Close = 196, 205, 200, 203.
**Version / licensing note:** from memory, unverified.
**Edge cases:** Synchronising unlike scales squashes the smaller measure into a flat line. Dual axes can mislead; label both axes.
**Likely follow-ups:** 1) *Combined axis vs dual axis?* Combined shares one axis. 2) *Alternatives?* Separate charts.
**Common mistakes:** Synchronising axes for different units; forgetting to change the second mark type.

### Q16 ⭐⭐ 🟡 What are the types of filters in Tableau and in what order do they run (order of operations)?
**Asked at:** frequently asked; research/interview_processes.md notes filters among the Wells Fargo Tableau topics, and Hyring/Interview Kickstart list filter order.
**What the interviewer is checking:** Do you understand why some filters seem to be ignored?
**Say this in the interview:** "Order matters: extract filters, data source filters, context filters, then FIXED LOD expressions, then dimension filters (with Top N and conditional filters at the same stage), then INCLUDE/EXCLUDE LODs, measure filters, and finally table calculations. Each step works on what the earlier ones leave."
**Explain simply:**
- **Extract filter:** applied when creating an extract (Q33).
- **Data source filter:** applied to the whole data source before any sheet.
- **Context filter:** a dimension filter promoted to run first (Q17).
- **Dimension filter:** on a dimension field, e.g. Region.
- **Measure filter:** on an aggregated number, e.g. SUM(Revenue) > 1,000.
- **Table-calc filter:** on a table calculation; runs last, after the data is computed, so it only hides marks.
**Example:** Region filter = South removes 4 of 8 employee rows before the average is computed (normal AVG). A FIXED LOD average ignores that filter (Q34).
**Version / licensing note:** from memory, unverified. The sources file says the Tableau Help "Order of Operations" page was fetched earlier with the flowchart image missing; I could not fetch it, and the exact placement of sets and Top N should be checked on that page.
**Edge cases:** Quick filters and Top N need the right stage; see Q35.
**Likely follow-ups:** 1) *Why is my FIXED LOD not filtered?* Q34. 2) *Why does Top 10 break?* Q35.
**Common mistakes:** Reciting the order without being able to explain a symptom; confusing context filters with data source filters.

### Q17 ⭐⭐ 🟡 What is a context filter in Tableau, and when would you use one?
**Asked at:** frequently asked (Wells Fargo filter topics per research/interview_processes.md; this exact question not reported).
**What the interviewer is checking:** Do you know context filters change the order, not just the appearance?
**Say this in the interview:** "A context filter is a dimension filter that I promote so it runs before the other filters. Everything else, such as Top N or a FIXED LOD, is then calculated only on the rows that pass the context. I use it when a Top N has to be calculated within a chosen region."
**Explain simply:**
- Create: right-click the filter pill > Add to Context (the pill turns grey).
- Later filters work on the already-filtered data, like a pre-filter.
- Also promotes a dimension filter ahead of FIXED LODs (Q34).
- Downside: context filters can be slower because Tableau builds a temporary table.
**Example:** Show the top 3 sales reps in the South region only. Without context: Top 3 overall is [A, B, C]; the South filter then leaves only B. With South as context: [B, D, F].
**Sample data:** Table `Reps`

| Rep | Region | Revenue |
|---|---|---|
| A | North | 90 |
| B | South | 80 |
| C | North | 70 |
| D | South | 60 |
| E | North | 50 |
| F | South | 40 |

**DAX / Steps:** Tableau click-path (not run here).
1. Drag Rep to Rows, Revenue to Columns.
2. Drag Region to Filters, choose South.
3. Right-click Region in Filters > Add to Context.
4. Right-click Rep > Filter > Top tab > By field > Top 3 by SUM(Revenue).
**Alternative:** Calculated-field Top N with an INCLUDE LOD or a parameter; or rank with a table calculation (which runs after filters).
**Result:** Reproduced with pandas: top 3 overall A, B, C; then South leaves B; context first gives B, D, F.
**Pandas check:**
```python
top=r.nlargest(3,"Rev"); top[top.Region=="South"].Rep.tolist()   # ['B']
r[r.Region=="South"].nlargest(3,"Rev").Rep.tolist()               # ['B','D','F']
```
Printed: `['A','B','C']`, `['B']`, `['B','D','F']`.
**Version / licensing note:** from memory, unverified.
**Edge cases:** Too many context filters hurt performance; only one dimension filter needs promoting in most cases.
**Likely follow-ups:** 1) *Does context affect LODs?* Yes, FIXED sees context-filtered rows. 2) *Alternative to context?* Table calcs.
**Common mistakes:** Making every filter a context filter "just in case".

### Q18 ⭐⭐ 🟡 What is a Level of Detail (LOD) expression in Tableau, and what are FIXED, INCLUDE and EXCLUDE?
**Asked at:** frequently asked; Wells Fargo accounts in research/interview_processes.md mention LODs (not this exact wording).
**What the interviewer is checking:** Can you compute a number at a different level than the view shows?
**Say this in the interview:** "An LOD expression calculates an aggregate at a level of detail I choose, independent of or relative to the view. FIXED uses exactly the dimensions I list; INCLUDE adds dimensions to the view's level; EXCLUDE removes them."
**Explain simply:**
- **Level of detail** = the grain: what each row of a result represents.
- `{FIXED [Dept] : AVG([Salary])}` gives the department average whatever else is in the view.
- `{INCLUDE [Region] : AVG([Salary])}` computes at Dept + Region, then the view aggregates it up.
- `{EXCLUDE [Region] : AVG([Salary])}` ignores Region even if it is in the view.
- Power BI parallel: CALCULATE with ALLEXCEPT / REMOVEFILTERS, or AVERAGEX over VALUES (Q22).
**Example:** Use the Q19 employee table with Region added. View at Dept level, plain AVG salary: HR 42,000, IT 100,000, Sales 60,000. With INCLUDE [Region] then AVG: HR 42,000, IT 102,500, Sales 57,500 (average of region averages).
**Sample data:** Table `Employees` with Region (see Q19).
**DAX / Steps:** Tableau calculated fields (not run here).
```
{ FIXED [Dept] : AVG([Salary]) }
{ INCLUDE [Region] : AVG([Salary]) }
{ EXCLUDE [Region] : AVG([Salary]) }
```
**Alternative:** A table calculation (WINDOW_AVG), but it depends on the view layout.
**Result:** Reproduced with pandas: plain AVG per Dept {HR 42000, IT 100000, Sales 60000}; INCLUDE Region then AVG {HR 42000, IT 102500, Sales 57500}. EXCLUDE [Region] with a Dept+Region view returns the Dept average.
**Pandas check:**
```python
reg=emp.groupby(["Dept","Region"]).Salary.mean()
reg.groupby("Dept").mean()     # INCLUDE Region, then AVG
emp.groupby("Dept").Salary.mean()
```
Printed: `HR 42000.0, IT 102500.0, Sales 57500.0` and `HR 42000.0, IT 100000.0, Sales 60000.0`.
**Version / licensing note:** from memory, unverified.
**Edge cases:** FIXED is affected by context filters and data source filters, not by normal dimension filters (Q34).
**Likely follow-ups:** 1) *Why use FIXED?* Stable benchmark. 2) *Table-level FIXED?* `{ AVG([Salary]) }` with no dimension = one value for the whole table.
**Common mistakes:** Expecting INCLUDE/EXCLUDE to ignore filters the way FIXED does.

### Q19 ⭐⭐ 🟡 How would you calculate average salary per department regardless of the view's other dimensions using an LOD in Tableau?
**Asked at:** gap-fill HR question (not seen as phrased).
**What the interviewer is checking:** Do you pick FIXED and explain why?
**Say this in the interview:** "I would write `{FIXED [Department] : AVG([Salary])}`. FIXED keeps the department as the only level, so the value stays the same even if Region or Gender is added to the view."
**Explain simply:**
- The view can show Dept and Region; the FIXED field still returns the department average.
- Useful for comparing each employee or group with their department benchmark.
- Normal dimension filters do not change it (Q34).
- Power BI equivalent: `CALCULATE(AVERAGE(Employees[Salary]), ALLEXCEPT(Employees, Employees[Dept]))` (Q22).
**Example:** Sales: 50,000, 70,000, 60,000 average 60,000. In a Dept+Region view, Sales-South shows 50,000 normally but the FIXED field shows 60,000.
**Sample data:** Table `Employees` (see Q8 for the 8 rows); Region added: E1 South, E2 North, E3 North, E4 South, E5 North, E6 South, E7 North, E8 South.
**DAX / Steps:** Tableau (not run here).
1. Analysis > Create Calculated Field: `Dept Avg Salary` = `{ FIXED [Dept] : AVG([Salary]) }`.
2. Put Dept and Region on Rows; add AVG(Salary) and `Dept Avg Salary` to the view.
**Alternative:** `{ EXCLUDE [Region] : AVG([Salary]) }` when Region is the only extra dimension.
**Result:** Reproduced with pandas:

| Dept | Region | AVG in view | FIXED Dept avg |
|---|---|---|---|
| HR | North | 44000 | 42000 |
| HR | South | 40000 | 42000 |
| IT | North | 110000 | 100000 |
| IT | South | 95000 | 100000 |
| Sales | North | 65000 | 60000 |
| Sales | South | 50000 | 60000 |

**Pandas check:**
```python
v=emp.groupby(["Dept","Region"],as_index=False).Salary.mean()
v["FIXED"]=v.Dept.map(emp.groupby("Dept").Salary.mean())
```
Printed output matches the table above.
**Version / licensing note:** from memory, unverified.
**Edge cases:** A NULL salary is ignored by AVG. A department with different regions weighting gives a different answer from averaging region averages (INCLUDE).
**Likely follow-ups:** 1) *If I filter Region = South?* FIXED still shows the all-region average (Q34). 2) *Excel analogue?* AVERAGEIFS.
**Common mistakes:** Using plain AVG(Salary) and wondering why it changes with the view.

### Q20 ⭐⭐ 🟡 What is the difference between a calculated field and a table calculation in Tableau?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know table calculations depend on the layout of the view?
**Say this in the interview:** "A calculated field is computed from the data source (row-level or aggregate) before the view is laid out. A table calculation runs last, on the numbers already shown in the view, such as running totals, rank or percent difference, so it depends on which fields are in the view and how it is partitioned."
**Explain simply:**
- Calculated field: independent of layout; usable in filters and LODs.
- Table calculation: runs after aggregation and after most filters; "compute using" decides direction.
- **Partition:** the group the calculation restarts within; **addressing:** the direction it moves.
- Power BI parallel: measures behave like calculated fields; visual calculations / window functions are the closest match to table calcs (availability not verified).
**Example:** Monthly Sales-team hires 5, 8, 4, 6: running total 5, 13, 17, 23; percent difference from previous month: 60%, -50%, 50%.
**Sample data:** Table `Hires`

| Month | Dept | Hires |
|---|---|---|
| Jan | Sales | 5 |
| Feb | Sales | 8 |
| Mar | Sales | 4 |
| Apr | Sales | 6 |

**DAX / Steps:** Tableau (not run here).
- Table calc: `RUNNING_SUM(SUM([Hires]))`, Compute Using = Table (Across) or Month.
- Percent difference: right-click measure > Quick Table Calculation > Percent Difference From.
**Alternative:** Row-level calculated field for the same measure (for example `Hires` per employee flag) does not need the view at all.
**Result:** Reproduced with pandas: running totals 5, 13, 17, 23; percent difference NaN, 60.0, -50.0, 50.0.
**Pandas check:**
```python
t=h[h.Dept=="Sales"].copy()
t["Running"]=t.Hires.cumsum(); t["PctDiffPrev"]=(t.Hires.pct_change()*100).round(1)
```
Printed: PctDiffPrev NaN, 60.0, -50.0, 50.0.
**Version / licensing note:** from memory, unverified.
**Edge cases:** First period has no previous value (null). Table calcs cannot be used in data source filters.
**Likely follow-ups:** 1) *What changes the result?* Layout and partition (Q36). 2) *Can an LOD replace it?* Not for running totals.
**Common mistakes:** Treating a table calc as a stored column that never changes.

### Q21 ⭐⭐ 🟡 A Tableau dashboard is slow. What do you check, and how do you use the Performance Recorder?
**Asked at:** commonly asked (Hyring performance questions; no company-specific report found).
**What the interviewer is checking:** Do you diagnose with evidence before changing things?
**Say this in the interview:** "First I measure with the Performance Recorder to see whether time goes to queries, layout or rendering. Then I fix the biggest item: use an extract, cut filters and marks, simplify calculations, and use fewer sheets per dashboard."
**Explain simply:**
- **Performance Recorder:** a Tableau tool that records timing of each action and shows it in a summary workbook.
- Steps (from memory, unverified): Help > Settings and Performance > Start Performance Recording; interact with the dashboard; Help > Settings and Performance > Stop Performance Recording; a performance workbook opens, with a timeline and the slowest events (query execution, layout, rendering).
- Common fixes: switch live to extract (Q7), hide unused fields, reduce quick filters or use "Apply" buttons, avoid heavy calculated fields on millions of rows, limit marks, fixed dashboard size, fewer dashboard sheets, aggregate data.
- Power BI parallel: Performance Analyzer.
**Example:** A 12-sheet HR dashboard takes 20 seconds. Recorder shows one sheet's query takes 14 seconds on a live connection; moving to an extract with only needed columns cuts it sharply.
**Version / licensing note:** from memory, unverified (menu names may differ by version; Tableau Help could not be fetched).
**Edge cases:** Slow could be the network or the database, not Tableau; test with a different connection.
**Likely follow-ups:** 1) *Extract vs live?* Q7. 2) *What is a "mark"?* A single dot/bar/cell drawn in the view; thousands slow rendering.
**Common mistakes:** Adding filters "to make it faster" without testing; guessing instead of recording.

### Q22 ⭐⭐ 🟡 What is the Power BI equivalent of a Tableau LOD expression, and how do they compare?
**Asked at:** gap-fill Power BI-equivalence question (not seen as phrased).
**What the interviewer is checking:** Can you map a concept between tools and show you understand filter context?
**Say this in the interview:** "There is no one-word match, but CALCULATE with ALLEXCEPT or REMOVEFILTERS covers FIXED, and AVERAGEX over VALUES covers INCLUDE. Where Tableau LODs are explicit about the grain, DAX measures work through filter context and change with the visual's filters."
**Explain simply:**
- **Filter context:** the filters automatically applied to a measure by the visual, slicers and relationships.
- FIXED: `CALCULATE(AVERAGE(Salary), ALLEXCEPT(Employees, Employees[Dept]))` keeps only Dept filters.
- EXCLUDE: `CALCULATE(..., REMOVEFILTERS(Employees[Region]))`.
- INCLUDE: iterate with `AVERAGEX(VALUES(Employees[Region]), CALCULATE(AVERAGE(Employees[Salary])))`.
- Difference: a DAX measure will usually respect a slicer on Region, while a Tableau FIXED ignores a normal dimension filter. In DAX, `ALLEXCEPT` explicitly removes it, so the two can be made to match.
**Example:** Q19 data: Dept average salary regardless of Region: HR 42,000, IT 100,000, Sales 60,000.
**Sample data:** Table `Employees`: same 8 rows as Q8 plus Region (Q19).
**DAX / Steps:** DAX not run here; Microsoft Learn pages were unreachable, so syntax is from memory and unverified.
```dax
Dept Avg Salary (FIXED) =
CALCULATE(
    AVERAGE(Employees[Salary]),
    ALLEXCEPT(Employees, Employees[Dept])
)

Avg of Region Avgs (INCLUDE) =
AVERAGEX(
    VALUES(Employees[Region]),
    CALCULATE(AVERAGE(Employees[Salary]))
)
```
**Alternative:** `CALCULATE(AVERAGE(Employees[Salary]), REMOVEFILTERS(Employees[Region]))` to drop only Region.
**Result:** Reproduced with pandas (the intended output of the logic, not a DAX engine): FIXED Dept avg HR 42000, IT 100000, Sales 60000. When the visual is filtered to Dept = IT and Region = South, `INCLUDE`-style average of the filtered region values is 95,000, while the FIXED measure returns 100,000 (all-region average).
**Pandas check:**
```python
emp.groupby("Dept").Salary.mean()                    # ALLEXCEPT Dept
emp[emp.Region=="South"].groupby("Dept").Salary.mean()  # visual filtered to South
```
Printed: all-region `HR 42000, IT 100000, Sales 60000`; South-only `HR 40000, IT 95000, Sales 50000`.
**Version / licensing note:** from memory, unverified: DAX functions named here are long-standing; calculation groups and visual calculations were not checked.
**Edge cases:** In DAX, a slicer on Region changes a plain AVERAGE; with ALLEXCEPT on a table it removes slicer filters on that table's other columns, which may surprise report users.
**Likely follow-ups:** 1) *Equivalent of context filter?* Roughly, filters applied first via CALCULATE/KEEPFILTERS (loose analogy). 2) *Which is easier?* LODs read like a sentence; DAX is more flexible.
**Common mistakes:** Using ALL(Employees) when only one column should be cleared; forgetting the model relationship direction.

### Q23 ⭐⭐ 🟡 How do Tableau's calculated fields differ from Power BI's DAX measures and Power Query steps?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know which tool layer does which job (clean, calculate, present) in each product?
**Say this in the interview:** "In Power BI I split the work: Power Query cleans and shapes rows before load, and DAX measures calculate on the model at report time. Tableau has no separate DAX layer: calculated fields are written in the worksheet and Tableau Prep or the data source does the cleaning."
**Explain simply:**
- **Calculated field (Tableau)** = a formula you add to the data source, for example `[Salary] * 12`. It can work row by row or on totals (aggregates), depending on how you write it.
- **DAX measure (Power BI)** = a formula (DAX is the Power BI formula language) that is recalculated for whatever the user filters, so one measure serves every chart. A DAX *calculated column* is the row-by-row cousin.
- **Power Query step** = one recorded cleaning action (remove blanks, split a column) that runs at refresh, before the data reaches the model. Tableau's nearest match is Tableau Prep, or the data-source page for basic fixes.
- Biggest difference: DAX needs a model with relationships and reads filter context; Tableau calculations read the fields in the view (level of detail of the sheet).
**Example:** Attrition % = Leavers / Average headcount. In Power BI, a DAX measure that divides the two, so it works for any department or month. In Tableau, a calculated field `SUM([Leavers]) / AVG([Headcount])` whose answer depends on what is placed on the sheet.
**DAX / Steps:** **Not run here:** Tableau and Power BI were not available; steps are written from memory.
```dax
Attrition % = DIVIDE ( SUM ( Leavers[Count] ), AVERAGE ( Headcount[Employees] ) )
```
Tableau: right-click the Data pane > Create Calculated Field > `SUM([Leavers]) / AVG([Headcount])`. Power Query: Home > Transform data > Applied Steps pane.
**Alternative:** For one-off fixes, do it upstream in SQL; only calculations that must react to slicers belong in DAX or Tableau.
**Version / licensing note:** from memory, unverified (help.tableau.com and learn.microsoft.com were unreachable in this session).
**Edge cases:** Divide by zero (use DIVIDE in DAX, `IF` in Tableau); a calculation placed in Power Query is fixed at refresh and ignores slicers.
**Likely follow-ups:** "Measure vs calculated column?" Measure is calculated on demand and does not store values; a column stores a value per row. "Where would you clean data in Tableau?" Tableau Prep or the data-source page.
**Common mistakes:** Doing aggregate math in Power Query and wondering why slicers do not change it; treating a Tableau calculated field like a DAX measure that is independent of the sheet.

### Q24 ⭐⭐ 🟡 How do you handle null values in Tableau?
**Asked at:** commonly asked (no company-specific report found; null handling appears in at least one prep-site list per the sources file)
**What the interviewer is checking:** Do you know nulls are not zeros and can change averages?
**Say this in the interview:** "A null means 'unknown', not 'zero'. I first ask why it is empty, then choose: leave it out, replace it with `ZN()` or `IFNULL()`, filter it, or fix it at source. I always state the choice because it changes the average."
**Explain simply:**
- **Null** = a cell with no value at all. Tableau shows a grey "Null" in filters and an "N nulls" indicator at the bottom right of a view.
- `ISNULL([Salary])` tests for null; `IFNULL([Salary], 0)` swaps null for a value; `ZN([Salary])` swaps null for zero (shorter).
- Averages skip nulls by default, so replacing nulls with 0 pulls the average down.
- You can also filter nulls out, or show missing months using Show Missing Values on a date axis.
**Example:** 6 employees, 2 salaries missing (50, 60, null, 70, null, 80 thousand). Average ignoring nulls = 65. After `ZN` = 43.3, which understates pay.
**Sample data:** table `Employees`

| Emp | Salary (k) |
|---|---|
| E1 | 50 |
| E2 | 60 |
| E3 | null |
| E4 | 70 |
| E5 | null |
| E6 | 80 |

**DAX / Steps:** **Not run here:** Tableau and Power BI were not available; steps are written from memory. Create calculated field `Salary clean` = `IFNULL([Salary], 0)`; to exclude instead, drag Salary to Filters > select all except Null. In Power BI the same idea is `COALESCE` in DAX or Replace Values in Power Query.
```dax
Avg Salary = AVERAGE ( Employees[Salary] )   -- ignores blanks
Avg Salary Zero = AVERAGEX ( Employees, COALESCE ( Employees[Salary], 0 ) )
```
**Alternative:** Fill with a department median in Tableau Prep or SQL, if the business agrees.
**Result:** reproduced with pandas: ignoring nulls 65.0; nulls as zero 43.33; 2 nulls.
**Pandas check:**
```python
e.Salary.mean(), e.Salary.fillna(0).mean(), e.Salary.isna().sum()
# (65.0, 43.333333333333336, 2)
```
**Version / licensing note:** from memory, unverified (help.tableau.com and learn.microsoft.com were unreachable in this session).
**Edge cases:** Null is not equal to anything (`[x] = NULL` is not a test, use `ISNULL`); null dates break date axes; nulls in a dimension appear as a "Null" mark.
**Likely follow-ups:** "ZN vs IFNULL?" ZN only gives 0; IFNULL lets you pick any value. "Blank text vs null?" An empty string is not null.
**Common mistakes:** Replacing every null with 0; ignoring the "nulls" indicator, so missing data goes unnoticed.

### Q25 ⭐⭐ 🟡 How would you build a monthly attendance or attrition trend dashboard in Tableau and in Power BI?
**Asked at:** commonly asked (no company-specific report found; HR-flavoured gap-fill question)
**What the interviewer is checking:** Can you build a simple, correct trend view end to end in both tools?
**Say this in the interview:** "I prepare one row per month with leavers and average headcount, build a line chart of attrition %, add a department filter, a target line and a short title, then publish. In Power BI I make a Date table and a DAX measure; in Tableau a calculated field and a continuous month axis."
**Explain simply:**
- Define the metric first: monthly attrition % = leavers in month / average of start and end headcount.
- **Date table** (Power BI) = a calendar table with one row per day so time functions work.
- **Continuous month** (Tableau) = the green MONTH pill that draws a proper line over time.
- Add filters (department, location), a reference line for target, and a tooltip with leavers and headcount.
**Example:** Jan to Apr 2026 with a 200-person start.
**Sample data:** table `Monthly`

| Month | Start | Leavers | Joiners | End |
|---|---|---|---|---|
| Jan | 200 | 4 | 0 | 196 |
| Feb | 196 | 2 | 0 | 194 |
| Mar | 194 | 5 | 1 | 190 |
| Apr | 190 | 3 | 2 | 189 |

**DAX / Steps:** **Not run here:** Tableau and Power BI were not available; steps are written from memory.
Power BI: Home > Get data > load table; Model view mark Date table; Report view > Line chart: X = Month, Y = measure; Format > Analytics for a constant line.
```dax
Attrition % =
DIVIDE ( SUM ( Monthly[Leavers] ), AVERAGEX ( Monthly, ( Monthly[Start] + Monthly[End] ) / 2 ) )
```
Tableau: Connect to data > Sheet 1 > Columns: right-click Month > Month (continuous); Rows: calculated field `SUM([Leavers]) / AVG(([Start]+[End])/2)`; Analytics pane > drag Constant Line; Dashboard > New Dashboard > drag sheet and a department filter > Publish.
**Alternative:** Show leavers as bars with the attrition % line on a dual axis.
**Result:** reproduced with pandas: Jan 2.02%, Feb 1.03%, Mar 2.60%, Apr 1.58% (DAX not run here).
**Pandas check:**
```python
m["End"]=m.Start-m.Leavers+m.Joiners
(m.Leavers/((m.Start+m.End)/2)*100).round(2).tolist()
# [2.02, 1.03, 2.6, 1.58]
```
**Version / licensing note:** from memory, unverified (help.tableau.com and learn.microsoft.com were unreachable in this session). Publishing to share needs a paid licence in both tools (from memory).
**Edge cases:** A monthly average of department rates is not the company rate; months with no data vanish unless a Date table or Show Missing Values is used; define a leaver (resigned only, or all exits).
**Likely follow-ups:** "Annualise it?" Multiply a monthly rate by 12 or use 12-month leavers / average headcount. "Add forecast?" Tableau has a Forecast option in Analytics; Power BI line charts have one too (from memory).
**Common mistakes:** Using month-end headcount only; text month names that sort alphabetically (Apr, Feb, Jan).

### Q26 ⭐ 🟢 What is Tableau Public, and why should you not put company or employee data on it?
**Asked at:** commonly asked (no company-specific report found; gap-fill privacy framing)
**What the interviewer is checking:** Do you protect employee data?
**Say this in the interview:** "Tableau Public is the free version where everything you publish is visible to anyone on the internet. So I use it only for open data and never for company or employee data."
**Explain simply:**
- **Tableau Public** = a free tool and website for sharing visuals publicly; it is meant for portfolios and open data.
- Workbooks you save go to a public profile; anyone can view and, in general, download the underlying data.
- Company data may be confidential, and employee data (salary, attendance) is personal data: publishing it can breach policy and law.
- Safe use: public datasets (government, Kaggle) or fully made-up HR data for a portfolio.
**Example:** A candidate publishes "Our attrition by manager" with real names. Anyone can open it. The right fix is synthetic data such as 500 invented employees.
**DAX / Steps:** **Not run here:** Tableau and Power BI were not available; steps are written from memory. Tableau Public: File > Save to Tableau Public. For work data use Tableau Cloud or Server instead (Server > Publish Workbook).
**Alternative:** Power BI "Publish to web" is the same risk: public link, no sign-in.
**Version / licensing note:** from memory, unverified (help.tableau.com and learn.microsoft.com were unreachable in this session). The sources file records that the Desktop comparison page describes Public as non-commercial with publish limits, but I could not re-read it.
**Edge cases:** Aggregated, anonymised data may be fine, but get written approval; hidden sheets and extracts can still be downloadable.
**Likely follow-ups:** "Can you hide the data?" Treat anything published as public. "Alternative for portfolio?" Synthetic data.
**Common mistakes:** Thinking a long unlisted link is private; blurring names but leaving them in the data.

### Q27 ⭐ 🟢 Can Tableau Desktop and Power BI Desktop be installed on a Mac?
**Asked at:** commonly asked (no company-specific report found; gap-fill)
**What the interviewer is checking:** Practical awareness: can you do the job on your own laptop?
**Say this in the interview:** "Tableau Desktop has a Mac version; Power BI Desktop is Windows-only. On a Mac I would use Power BI Service in the browser or a Windows virtual machine."
**Explain simply:**
- **Tableau Desktop**: installs on both Windows and macOS (from memory).
- **Power BI Desktop**: Windows only; there is no native Mac app. The web **Power BI Service** works in any browser but has fewer modelling features (from memory).
- Mac workarounds: a Windows virtual machine, Windows 365 or a cloud PC, or work laptops provided by the employer.
**Example:** A Mac-owning learner practises Tableau Public on Mac and does Power BI via a company-provided Windows laptop or cloud PC.
**DAX / Steps:** **Not run here:** Tableau and Power BI were not available; steps are written from memory. Check requirements on each vendor's system-requirements page before installing.
**Alternative:** Boot Camp is not available on Apple-silicon Macs; use virtualisation software.
**Version / licensing note:** from memory, unverified (help.tableau.com and learn.microsoft.com were unreachable in this session). The sources file notes Tableau OS support was not stated on the fetched Tableau page and Microsoft's system-requirements page was not retrieved, so please verify.
**Edge cases:** Some Tableau connectors differ by OS; macOS versions drop out of support.
**Likely follow-ups:** "Can you build reports in the browser?" Yes, limited editing in the Service.
**Common mistakes:** Saying neither works on Mac; assuming Power BI Desktop runs through the Mac App Store.

### Q28 ⭐ 🟢 What is Tableau Prep, and how does it compare with Power Query in Power BI?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know where data cleaning belongs in each stack?
**Say this in the interview:** "Tableau Prep is Tableau's separate tool for cleaning and reshaping data visually, as a flow. Power Query does the same job inside Power BI, as recorded steps. Both are no-code or low-code; Prep is a separate product, Power Query is built in."
**Explain simply:**
- **Tableau Prep** = a visual tool where you drag steps (clean, join, union, pivot, aggregate) and output a file or data source for Tableau.
- **Power Query** = the Transform data window in Power BI with a list of Applied Steps, written in a language called M behind the scenes.
- Prep shows each step as a flow diagram and previews data profile at every step; Power Query is a table editor with a step list.
- Power Query also exists in Excel, so skills transfer.
**Example:** Merging monthly attendance files: in Prep use Union (drag files in); in Power Query use Get data > Folder > Combine.
**DAX / Steps:** **Not run here:** Tableau and Power BI were not available; steps are written from memory. Tableau Prep Builder: Connect > Add step > Clean/Join/Pivot > Output. Power BI: Home > Transform data.
**Alternative:** Do cleaning in SQL or Python; keep BI tools for modelling and visuals.
**Version / licensing note:** from memory, unverified (help.tableau.com and learn.microsoft.com were unreachable in this session). Prep licensing (bundled with Creator, from memory) needs verification.
**Edge cases:** Prep flows run on a schedule only with the right Tableau licence/add-on (from memory); Power Query refresh needs a gateway for on-premises sources.
**Likely follow-ups:** "Which is easier?" Prep for visual thinkers, Power Query for Excel users.
**Common mistakes:** Believing Prep is needed for all Tableau work; forgetting Power Query steps re-run on refresh.

### Q29 ⭐ 🟢 What is a hierarchy in Tableau, and how do you create a drill-down?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you build an interactive drill-down for managers?
**Say this in the interview:** "A hierarchy stacks fields from broad to detailed, like Region > Department > Employee. I drag one field onto another in the Data pane, and the plus icon on the view lets users drill down."
**Explain simply:**
- **Hierarchy** = fields in a parent-child order. Tableau creates date hierarchies (Year > Quarter > Month > Day) automatically.
- **Drill-down** = click the + on a pill (or header) to go one level deeper; click - to go back up.
- Custom hierarchies are limited to dimensions.
**Example:** Headcount by Business Unit (3 units) drills to 12 departments, then to 480 employees.
**DAX / Steps:** **Not run here:** Tableau and Power BI were not available; steps are written from memory. Data pane > drag Department onto Business Unit (or right-click a field > Hierarchy > Create Hierarchy) > name it > drag a lower field in; on the sheet, drag the top field to Rows and click the + sign.
**Alternative:** Power BI: add fields to one visual's Axis well in order and use the drill arrows.
**Version / licensing note:** from memory, unverified (help.tableau.com and learn.microsoft.com were unreachable in this session).
**Edge cases:** Order matters; unbalanced hierarchies show blanks; the + only appears with a hierarchy.
**Likely follow-ups:** "Hierarchy vs drill-through?" A drill-through jumps to another page.
**Common mistakes:** Mixing a measure into a hierarchy; reversing the order.

### Q30 ⭐ 🟢 What is a dashboard action in Tableau (filter, highlight, URL)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you make a dashboard interactive?
**Say this in the interview:** "Actions let one click change something else. A filter action filters other sheets, a highlight action dims everything except the selection, and a URL action opens a web page."
**Explain simply:**
- **Dashboard action** = a rule: "when the user selects marks here, do that there".
- **Filter action** = clicking a department bar filters the attrition trend chart.
- **Highlight action** = selected values stay bright, others fade.
- **URL action** = opens a link built from field values, such as an employee-profile page or a search.
- Triggers: Hover, Select or Menu.
**Example:** Click "Sales" in a bar of attrition by department and the monthly line shows only Sales.
**DAX / Steps:** **Not run here:** Tableau and Power BI were not available; steps are written from memory. Dashboard > Actions > Add Action > Filter / Highlight / Go to URL > choose source sheet, target sheet, run on Select. Quick way: on a dashboard sheet, click the funnel icon "Use as Filter".
**Alternative:** Power BI cross-filtering, cross-highlighting and drill-through.
**Version / licensing note:** from memory, unverified (help.tableau.com and learn.microsoft.com were unreachable in this session).
**Edge cases:** Clearing the selection can show all or nothing (set it in the action); URL actions need safe links.
**Likely follow-ups:** "Filter action vs quick filter?" Action is driven by clicks on marks; a quick filter is a control.
**Common mistakes:** Targeting the wrong sheet; leaving "Show all values" when clear.

### Q31 ⭐ 🟢 What is the difference between a reference line and a reference band in Tableau?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you show benchmarks on a chart?
**Say this in the interview:** "A reference line is one value, like the company average. A reference band is a shaded range between two values, like the normal range of attrition. A band marks a zone, a line marks a point."
**Explain simply:**
- **Reference line** = a line at a constant, average, median or other computed value.
- **Reference band** = a shaded area between two values (for example min to max or 25th to 75th percentile).
- Both are added from the Analytics pane and recalculated for the view.
**Example:** Attrition by department. Average of 5 departments = 11.6%; shaded band from 8% to 15% (the 25th to 75th percentile) marks the normal range, so Sales (18%) stands out.
**Sample data:** table `DeptAttrition`

| Dept | Attrition % |
|---|---|
| Sales | 18 |
| Support | 15 |
| IT | 11 |
| Finance | 8 |
| HR | 6 |

**DAX / Steps:** **Not run here:** Tableau and Power BI were not available; steps are written from memory. Analytics tab (left of the Data pane) > drag Reference Line or Reference Band to the chart > Table/Pane/Cell scope > Value > Average (line) or From/To (band).
**Alternative:** In Power BI use Analytics pane constant line or average line.
**Result:** reproduced with pandas: mean 11.6; quartiles 8.0 and 15.0; min 6, max 18.
**Pandas check:**
```python
d.Attr.mean(), d.Attr.quantile([.25,.75]).tolist()
# (11.6, [8.0, 15.0])
```
**Version / licensing note:** from memory, unverified (help.tableau.com and learn.microsoft.com were unreachable in this session). Percentile method may differ slightly from Tableau's.
**Edge cases:** Scope (whole table vs each pane) changes the value; a band on a dual axis may use the wrong axis.
**Likely follow-ups:** "Distribution band?" Shows percentiles or standard deviations.
**Common mistakes:** Putting a line on the wrong scope; reading the average of averages.

### Q32 ⭐ 🟡 What is the difference between Tableau relationships and joins?
**Asked at:** commonly asked (no company-specific report found; relationships vs joins appears in a 2026 prep-site list per the sources file)
**What the interviewer is checking:** Do you know modern Tableau data modelling and why it avoids duplicated numbers?
**Say this in the interview:** "A join merges two tables into one wide table up front, fixed at that level. A relationship keeps tables separate and Tableau joins them only for the fields in the view, at the right level of detail, which avoids duplicated numbers."
**Explain simply:**
- **Join** = combine tables row by row into one flat table (inner, left, right, full). Rows can multiply when the join key repeats.
- **Relationship** = a link between two tables on a key, resolved at query time (introduced in Tableau 2020.2, from memory). Keeps each table's own level of detail.
- Relationships behave more like Power BI's model relationships.
- Joins still suit one-to-one lookups or when you need a specific join type.
**Example:** Employees (500 rows) and Leave records (3,000 rows). A join gives 3,000 rows and repeats salary; a relationship keeps both and averages salary correctly.
**DAX / Steps:** **Not run here:** Tableau and Power BI were not available; steps are written from memory. Data Source tab > drag a second table beside the first (noodle = relationship) > edit the key; double-click the table to open the join canvas.
**Alternative:** Blend data on a shared field (see join vs blend).
**Version / licensing note:** from memory, unverified (help.tableau.com and learn.microsoft.com were unreachable in this session).
**Edge cases:** Relationships need matching data types; unmatched rows may drop out of the view; cardinality settings can be wrong.
**Likely follow-ups:** "When join instead?" Row-level flat output. "Does it fix duplication?" Largely, yes.
**Common mistakes:** Joining everything out of habit; ignoring performance options.

### Q33 ⭐ 🟡 What is the difference between a data source filter and an extract filter in Tableau?
**Asked at:** commonly asked (no company-specific report found; Wells Fargo reports mention Tableau filters in general)
**What the interviewer is checking:** Do you know where in the pipeline a filter acts?
**Say this in the interview:** "A data source filter limits what Tableau sees at all, for every sheet. An extract filter limits what goes into the extract file when it is created. Both reduce data; the extract filter only applies if you use an extract."
**Explain simply:**
- **Data source filter** = set on the Data Source page; applies to the whole workbook, live or extract.
- **Extract** = a compressed snapshot of the data stored in a .hyper file.
- **Extract filter** = set when creating the extract; rows not matching are never stored.
- Use them to cut size, hide sensitive rows (but not as security) and speed up queries.
**Example:** Keep only 2024 onward and only active employees: 800,000 rows become 120,000.
**DAX / Steps:** **Not run here:** Tableau and Power BI were not available; steps are written from memory. Data Source tab > Filters (top right) > Add. Extract: choose Extract > Edit > Add filter.
**Alternative:** Filter in SQL or Power Query upstream.
**Version / licensing note:** from memory, unverified (help.tableau.com and learn.microsoft.com were unreachable in this session).
**Edge cases:** Changing an extract filter requires a refresh; data source filters apply before FIXED LODs and context filters (order of operations, from memory).
**Likely follow-ups:** "Is it security?" No, use row-level security.
**Common mistakes:** Assuming extract filter works on live connections.

### Q34 ⭐ 🟡 Why is a FIXED LOD not affected by a normal dimension filter, and how do you fix that?
**Asked at:** Wells Fargo (Hyderabad) reviews mention Tableau LODs and filters generally (per research/interview_processes.md); no question-level match found
**What the interviewer is checking:** Do you know Tableau's order of operations?
**Say this in the interview:** "A FIXED LOD is calculated before normal dimension filters, so those filters do not change it. To make the filter apply, I add it to context; context filters run before FIXED."
**Explain simply:**
- **LOD (Level of Detail) expression** = a formula that calculates at a level you choose, such as per department, regardless of the view.
- Order, from memory: extract and data source filters, context filters, FIXED LODs, dimension filters, then INCLUDE/EXCLUDE LODs and measure filters, table calculations last.
- A normal dimension filter comes after FIXED, so it is ignored.
- Fixes: right-click the filter > Add to Context; or use INCLUDE/EXCLUDE; or put the condition inside the FIXED formula.
**Example:** Average salary per department, filtered to Hyderabad. The FIXED value stays at the all-location figure.
**Sample data:** table `Employees`

| Emp | Dept | Loc | Salary |
|---|---|---|---|
| 1 | IT | Hyd | 80 |
| 2 | IT | Hyd | 100 |
| 3 | IT | Blr | 60 |
| 4 | IT | Blr | 40 |
| 5 | HR | Hyd | 50 |
| 6 | HR | Blr | 30 |
| 7 | HR | Blr | 70 |
| 8 | HR | Hyd | 50 |

**DAX / Steps:** **Not run here:** Tableau and Power BI were not available; steps are written from memory.
```
{ FIXED [Dept] : AVG([Salary]) }
```
Right-click the Loc pill on Filters > Add to Context.
**Alternative:** `{ FIXED [Dept] : AVG(IF [Loc]="Hyd" THEN [Salary] END) }` bakes the condition in.
**Result:** reproduced with pandas: FIXED IT 70, HR 50 regardless of filter; with Loc = Hyd in context IT 90, HR 50.
**Pandas check:**
```python
s.groupby("Dept").Salary.mean().to_dict()      # {'HR': 50.0, 'IT': 70.0}
s[s.Loc=="Hyd"].groupby("Dept").Salary.mean()  # IT 90.0, HR 50.0
```
**Version / licensing note:** from memory, unverified (help.tableau.com and learn.microsoft.com were unreachable in this session).
**Edge cases:** Context filters make a temporary extract-like step and can slow big views; a FIXED with no dimension is a grand total.
**Likely follow-ups:** "INCLUDE/EXCLUDE?" They run after dimension filters.
**Common mistakes:** Expecting every filter to hit LODs; adding too many context filters.

### Q35 ⭐ 🟡 Your Tableau Top 10 filter shows fewer than 10 items after you add a region filter. Why, and how do you fix it?
**Asked at:** Wells Fargo (Hyderabad) reviews mention Tableau filters in general; a Top N plus region scenario appears in a prep-site snippet (PracHub), unverified
**What the interviewer is checking:** Can you reason about the order of filters?
**Say this in the interview:** "Top N and Region are both normal dimension filters, so they run at the same time. Tableau finds the top 10 over all regions, then the region filter removes some. I add the region filter to context so it runs first."
**Explain simply:**
- **Top N filter** = keep the N biggest members by a measure.
- Region filter and Top N are both dimension filters; neither sees the other's result.
- Add Region to Context so Top N is computed only inside the chosen region.
- Alternative: a set or a ranking table calculation filtered after Region.
**Example:** Top 3 products overall are A, B, C. Pick East: only A and C show (B is West). Should be A, C, F.
**Sample data:** table `Sales`

| Product | Region | Sales |
|---|---|---|
| A | East | 90 |
| B | West | 80 |
| C | East | 70 |
| D | West | 60 |
| E | West | 50 |
| F | East | 40 |
| G | West | 30 |
| H | East | 20 |

**DAX / Steps:** **Not run here:** Tableau and Power BI were not available; steps are written from memory. Right-click the Region filter pill > Add to Context (it turns grey); Top N on Product by SUM(Sales) is then computed after it.
**Alternative:** `RANK(SUM([Sales]))` table calculation filtered to <= 10; it runs after dimension filters.
**Result:** reproduced with pandas: top 3 overall A, B, C; after East filter A, C; with context first A, C, F.
**Pandas check:**
```python
p.nlargest(3,"Sales").Product.tolist()          # ['A','B','C']
p[p.Region=="East"].nlargest(3,"Sales").Product.tolist()  # ['A','C','F']
```
**Version / licensing note:** from memory, unverified (help.tableau.com and learn.microsoft.com were unreachable in this session).
**Edge cases:** Ties at rank N; a parameter-driven N.
**Likely follow-ups:** "Why not a table calc?" It also works but changes with partitioning.
**Common mistakes:** Applying the region filter after Top N and blaming the data.

### Q36 ⭐ 🟡 Your Tableau running total or rank changes when you add a field to the view. Why?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand table calculations and "compute using"?
**Say this in the interview:** "Running totals and ranks are table calculations: they run on the results in the view, after filters. Adding a field changes the partitions and direction, so the numbers change. I set Compute Using explicitly to the field I want."
**Explain simply:**
- **Table calculation** = a calculation on the table already shown in the view (running total, rank, percent of total).
- **Compute using** (Table Across, Down, Pane, or a specific dimension) says which direction and where it restarts.
- Adding a dimension adds columns or rows, so "Table (Across)" now runs through the new field too.
- Fix: edit the table calculation > Compute Using > Specific Dimensions > Month only.
**Example:** Monthly sales by region. Running total across the whole table gives 120 at the end; per region gives East 45 and West 75.
**Sample data:** table `Sales`

| Month | Region | Sales |
|---|---|---|
| Jan | East | 10 |
| Jan | West | 20 |
| Feb | East | 15 |
| Feb | West | 25 |
| Mar | East | 20 |
| Mar | West | 30 |

**DAX / Steps:** **Not run here:** Tableau and Power BI were not available; steps are written from memory. Right-click the green delta pill > Edit Table Calculation > Compute using > Specific Dimensions > tick Month, set "Restarting every" Region.
**Alternative:** In Power BI use a DAX running total with `CALCULATE ( SUM(...), FILTER ( ALLSELECTED ( Date ), Date[Date] <= MAX ( Date[Date] ) ) )`, which does not depend on layout.
**Result:** reproduced with pandas: running total across all 10, 30, 45, 70, 90, 120; per region East 10, 25, 45 and West 20, 45, 75.
**Pandas check:**
```python
r["RT_across_all"]=r.Sales.cumsum()
r["RT_by_region"]=r.groupby("Region").Sales.cumsum()
# last row: 120 and 75
```
**Version / licensing note:** from memory, unverified (help.tableau.com and learn.microsoft.com were unreachable in this session).
**Edge cases:** Ties in RANK; filters on the dimension being computed over change the result.
**Likely follow-ups:** "Why not LOD?" LODs ignore the view layout.
**Common mistakes:** Leaving the default Compute Using after restructuring the view.

### Q37 ⭐ 🟡 How do you implement row-level security in Tableau compared with Power BI RLS?
**Asked at:** commonly asked; Row-level security appears in a 2026 prep-site list (Hyring) and Power BI RLS in service-MNC reports, per the sources file
**What the interviewer is checking:** Do you know how to restrict who sees which rows?
**Say this in the interview:** "Row-level security means each user only sees their rows, like an HR business partner seeing only their department. In Tableau I use a user filter or a calculated field with USERNAME(), or a data policy; in Power BI I define roles with DAX filters and assign users in the Service."
**Explain simply:**
- **RLS** = same report, different rows for different people.
- **Tableau**: a calculated field such as `[Manager Email] = USERNAME()` as a data source filter; or a user filter (manual mapping); or entitlement tables. Published to Tableau Cloud/Server.
- **Power BI**: Modeling > Manage roles > add a DAX filter such as `[Email] = USERPRINCIPALNAME()`; then Service > semantic model > Security to add members.
- In both, test as the user (Tableau "Impersonate"/View as; Power BI "View as").
**Example:** 12 HRBPs each see only their 400 employees out of 4,800.
**DAX / Steps:** **Not run here:** Tableau and Power BI were not available; steps are written from memory.
```dax
-- Power BI role filter on the Employees table
[ManagerEmail] = USERPRINCIPALNAME ()
```
Tableau: Data > Create User Filter (or a calculated field with `USERNAME()`), then publish with the filter on the data source.
**Alternative:** Database-level security.
**Version / licensing note:** from memory, unverified (help.tableau.com and learn.microsoft.com were unreachable in this session). Sharing needs paid licences in both (from memory).
**Edge cases:** Extracts and embedded credentials can bypass user-level security; admins and workspace members with edit rights can bypass Power BI RLS.
**Likely follow-ups:** "Static vs dynamic?" Dynamic uses USERNAME/USERPRINCIPALNAME with a mapping table.
**Common mistakes:** Using a visible filter as security.

### Q38 ⭐ 🟡 How do licensing and cost differ between Power BI (Free, Pro, Premium) and Tableau (Creator, Explorer, Viewer)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Commercial awareness of who needs which licence.
**Say this in the interview:** "Power BI Desktop is free, but sharing needs Pro or Premium; Tableau is licensed per person by role: Creator builds, Explorer explores and edits, Viewer only views. Prices change, so I would check the current price list."
**Explain simply:**
- **Power BI**: Free (build in Desktop, little sharing), Pro (per user, share and collaborate), Premium/Fabric (capacity-based, larger models and wider viewing). Premium Per User (PPU) is a per-user premium tier (from memory).
- **Tableau**: Creator (Desktop, Prep, full authoring), Explorer (web editing on published data), Viewer (view and comment).
- Typical comparison: Power BI is cheaper for companies already on Microsoft 365; Tableau suits teams who want deep visual flexibility.
**Example:** A team of 5 builders and 100 viewers: Tableau needs 5 Creators plus 100 Viewers; Power BI needs Pro for everyone, or Premium capacity so viewers need no individual licence (check current rules).
**DAX / Steps:** **Not run here:** Tableau and Power BI were not available; steps are written from memory. Not applicable; check the vendors' pricing pages.
**Alternative:** Compare by total cost of ownership: licences, admin, training.
**Version / licensing note:** from memory, unverified; no prices quoted because they change and the pricing pages were not fetched.
**Edge cases:** Free viewing of Premium content has capacity conditions; regional prices differ.
**Likely follow-ups:** "Which is cheaper?" Depends on viewer count.
**Common mistakes:** Quoting stale prices; forgetting viewer licences.

### Q39 ⭐ 🟡 How do the two tools compare for sharing dashboards, refresh and governance (Power BI Service vs Tableau Cloud or Server)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you compare the publishing, refresh and governance layers?
**Say this in the interview:** "Both have a web service to publish and share: Power BI Service and Tableau Cloud or Server. Both schedule refresh, and need a gateway or bridge for on-premises data. Governance covers roles, workspaces or projects, certification and security."
**Explain simply:**
- **Sharing**: Power BI uses workspaces and apps; Tableau uses sites, projects and permissions.
- **Refresh**: Power BI scheduled refresh of semantic models; Tableau extract refresh schedules. On-premises sources need a gateway (Power BI) or Tableau Bridge (Tableau Cloud).
- **Governance**: Power BI has sensitivity labels, certified/promoted content, tenant settings; Tableau has certified data sources, project permissions, and Tableau Cloud Server admin.
- **Deployment**: Tableau Server is self-hosted; Tableau Cloud is hosted. Power BI Service is cloud only (Report Server is on-premises).
**Example:** An HR dashboard published to a Power BI workspace, refreshed nightly at 6 am via a gateway, shared as an app to 40 managers.
**DAX / Steps:** **Not run here:** Tableau and Power BI were not available; steps are written from memory. Power BI: Publish > workspace > semantic model > Settings > Scheduled refresh. Tableau: Server > Publish > Schedule extract refresh.
**Alternative:** Embed in Teams or a portal.
**Version / licensing note:** from memory, unverified (refresh limits per licence not checked).
**Edge cases:** Daily refresh caps vary by licence; time zones for schedules.
**Likely follow-ups:** "Gateway vs Bridge?" Same purpose, different products.
**Common mistakes:** Forgetting credentials; sharing the file instead of publishing.

### Q40 ⭐ 🟡 Your company uses Tableau but you only know Power BI. How would you get productive quickly?
**Asked at:** commonly asked (no company-specific report found; gap-fill)
**What the interviewer is checking:** Learning agility and honest mapping of skills.
**Say this in the interview:** "I would map concepts I know to Tableau: measures to calculated fields, Power Query to Prep, relationships to relationships, DAX context to LOD expressions. Then I rebuild a dashboard I already made in Power BI in Tableau, using the company's data."
**Explain simply:**
- Week 1: learn the interface, dimensions vs measures, blue vs green pills, and the Show Me panel.
- Week 2: calculations, filters and order of operations, LODs.
- Week 3: dashboards, actions, publishing.
- Practise by recreating one known report and ask a senior colleague to review it.
**Example:** Rebuild a 3-page Power BI HR dashboard in Tableau in about 2 to 3 weeks of focused practice.
**DAX / Steps:** **Not run here:** Tableau and Power BI were not available; steps are written from memory. Use Tableau Public with open data to practise; keep company data off it.
**Alternative:** Official free training videos.
**Version / licensing note:** from memory, unverified (help.tableau.com and learn.microsoft.com were unreachable in this session).
**Edge cases:** Do not claim expertise you lack; say what you know.
**Likely follow-ups:** "Biggest difference?" Layout-driven calculations vs model-driven.
**Common mistakes:** Expecting DAX behaviour; trying to model data upfront.

### Q41 ⭐ 🟡 How would you migrate an existing Tableau report to Power BI?
**Asked at:** commonly asked (no company-specific report found; gap-fill)
**What the interviewer is checking:** Structured approach to a migration.
**Say this in the interview:** "Migration is a rebuild, not an export. I list what the Tableau report does, check data sources, rebuild the data model and calculations in Power BI, recreate visuals, reconcile numbers, then get user sign-off."
**Explain simply:**
- No one-click converter that I know of (from memory), so assume rebuild.
- Steps: inventory (sheets, fields, filters, calculations); connect the same sources; clean in Power Query; build relationships; translate calculated fields and LODs into DAX measures; rebuild visuals; set up RLS and refresh; compare numbers side by side.
- Parallel run until both agree.
- Expect visual differences; confirm the must-haves.
**Example:** 6 sheets, 15 calculations, 3 filters: rebuild in about 2 weeks, then reconcile headcount for 12 months.
**DAX / Steps:** **Not run here:** Tableau and Power BI were not available; steps are written from memory. Power BI Desktop > Get data; Transform data; Model view; Report view; Publish.
**Alternative:** Keep Tableau and embed.
**Version / licensing note:** from memory, unverified (help.tableau.com and learn.microsoft.com were unreachable in this session).
**Edge cases:** Table calculations and LODs rarely translate one to one; user training.
**Likely follow-ups:** "How do you check?" Reconcile totals per month.
**Common mistakes:** Copying layout exactly; skipping reconciliation.

### Q42 ⭐ 🔴 A stakeholder says the Tableau and Power BI dashboards show different headcount for the same month. How do you investigate?
**Asked at:** commonly asked (no company-specific report found; gap-fill scenario)
**What the interviewer is checking:** Methodical debugging, not guessing.
**Say this in the interview:** "I would not pick a side. I compare definitions first, then data, then logic: same source, same date, same filters, same count method. Then I reconcile from a raw list of employee IDs."
**Explain simply:**
- Definition: headcount at month start, month end or average? Do exits on the last day count? Contractors included?
- Counting: rows vs distinct employee IDs (an internal transfer can create two rows for one person).
- Filters: hidden filters, different date ranges, time zones, extract not refreshed.
- Join/model: a join that duplicates rows (Tableau) vs relationships (Power BI).
- Export both lists of IDs and compare.
**Example:** March data.
**Sample data:** table `Headcount`

| Row | Emp | Type | Exit |
|---|---|---|---|
| 1 | E1 | Perm | |
| 2 | E2 | Perm | |
| 3 | E3 | Perm | |
| 4 | E3 | Perm | |
| 5 | E4 | Perm | 2026-03-10 |
| 6 | E5 | Perm | |
| 7 | E6 | Contract | |
| 8 | E7 | Perm | 2026-03-31 |

**DAX / Steps:** **Not run here:** Tableau and Power BI were not available; steps are written from memory.
```dax
Headcount = DISTINCTCOUNT ( Headcount[Emp] )
```
**Alternative:** Tableau `COUNTD([Emp])` vs `COUNT([Emp])`.
**Result:** reproduced with pandas: 8 rows; 7 distinct IDs; permanent distinct 6; active at 31 March excluding exits that day 5, counting the 31 March leaver 6. Five different "headcounts" from the same data.
**Pandas check:**
```python
len(h), h.Emp.nunique(), h[h.Type=="Perm"].Emp.nunique()   # 8 7 6
h[h.Exit.isna()].Emp.nunique()                              # 5
```
**Version / licensing note:** from memory, unverified (help.tableau.com and learn.microsoft.com were unreachable in this session).
**Edge cases:** Blanks in the exit date; time zones on dates; duplicate employees.
**Likely follow-ups:** "Who is right?" Whichever matches the agreed definition; document it.
**Common mistakes:** Comparing totals only, not IDs; changing a dashboard before agreeing a definition.

### Q43 ⭐ 🔴 A join to a targets table doubled the revenue in Tableau. What happened, and how do you fix it?
**Asked at:** commonly asked (no company-specific report found; gap-fill)
**What the interviewer is checking:** Do you recognise join fan-out (duplicated rows)?
**Say this in the interview:** "The join key was not unique in the targets table, so each sales row matched two target rows and was repeated. I confirm with row counts, then fix the grain: join on all keys, aggregate targets first, or use a relationship or blend."
**Explain simply:**
- **Fan-out** = a join that multiplies rows because one side has several matches.
- Sales (6 rows) joined to Targets on Month only: each month has two target rows (N and S), so every sale appears twice.
- Revenue is summed per row, so it doubles.
- Fixes: join on Month and Region; aggregate targets to one row per month; use relationships; or divide by a LOD count.
**Example:** January revenue is really 400 but shows 800.
**Sample data:** table `Sales`

| Sale | Month | Region | Rev |
|---|---|---|---|
| 1 | Jan | N | 100 |
| 2 | Jan | S | 200 |
| 3 | Jan | N | 100 |
| 4 | Feb | S | 150 |
| 5 | Feb | N | 150 |
| 6 | Feb | S | 100 |

Table `Targets`

| Month | Region | Target |
|---|---|---|
| Jan | N | 250 |
| Jan | S | 250 |
| Feb | N | 300 |
| Feb | S | 300 |

**DAX / Steps:** **Not run here:** Tableau and Power BI were not available; steps are written from memory. Data Source tab > edit the join > add Region as a second join clause; or replace the join with a relationship; or `{ FIXED [Month] : SUM([Rev]) }` for revenue.
**Alternative:** Blend: Sales primary, Targets secondary on Month and Region.
**Result:** reproduced with pandas: sales 800, 6 rows; join on Month gives 1,600 and 12 rows; join on Month and Region gives 800 and 6 rows. Jan 800 vs real 400.
**Pandas check:**
```python
sa.Rev.sum(), sa.merge(t,on="Month").Rev.sum()              # 800 1600
sa.merge(t,on=["Month","Region"]).Rev.sum()                 # 800
```
**Version / licensing note:** from memory, unverified (help.tableau.com and learn.microsoft.com were unreachable in this session).
**Edge cases:** Missing target rows in an inner join drop sales; left join keeps them.
**Likely follow-ups:** "How to spot it?" Compare row counts before and after.
**Common mistakes:** Fixing with AVG; not checking row counts.

