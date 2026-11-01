# Book 4 — Power BI & Visualization | Part 1: Power BI basics: components, Desktop vs Service, workflow 🟢

**Target:** 55 questions | **Actual:** 55 questions
**Scope:** Power BI components and building blocks, Desktop vs Service vs Mobile, file types, licence types, connectivity modes and the end-to-end workflow from data to shared report.

### Q1 ⭐⭐⭐ 🟢 What is Power BI and what is it used for?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you describe the tool in one clear business sentence, not a feature list?
**Say this in the interview:** "Power BI is Microsoft's business analytics platform. I connect it to data such as Excel files or databases, clean and model that data, build interactive reports with charts, and share them so managers can make decisions without asking an analyst for a new Excel file every week."
**Explain simply:**
- It turns raw data (rows in Excel, tables in a database) into visuals such as bar charts, tables and maps that people can click, filter and drill into.
- It is not one program but a family: a Windows app to build reports (Desktop), an online site to share them (Service) and phone apps to read them (Mobile).
- Microsoft's overview page says it can connect to more than 100 data sources, and that the Service can schedule refresh, send email subscriptions, set alerts and apply security.
- Power BI is also a workload inside Microsoft Fabric (Microsoft's all-in-one analytics platform); existing Power BI content and workspaces stay as they are.
**Example:** The HR head wants a monthly attrition report. Today you paste the HRIS export into Excel, rebuild pivots and email a file. With Power BI you build the report once, publish it, set a daily refresh, and the HR head opens a link and filters by department or location.
**DAX / Steps:** Not a measure question. Typical path (not run here): Desktop > Home > Get data > pick source > Load > build visuals > Home > Publish > share from the Service.
**Alternative:** Say it by audience: for a manager it is "a live dashboard", for an analyst it is "a data model plus visuals".
**Version / licensing note:** Verified on Microsoft Learn: "What is Power BI?" (Desktop is described as a Windows app; more than 100 sources; Service features). Licence details are in Q19 and Q3.
**Edge cases:** Power BI is not a database and not a replacement for an HRIS; it reads from them.
**Likely follow-ups:**
1. *Is it only for big companies?* No. Desktop is free to build with; sharing needs licences (Q19).
2. *How is it different from Excel?* See Q12.
**Common mistakes:** Answering only "it makes dashboards"; forgetting data preparation and modelling; confusing "Power BI" with only the Desktop app.

### Q2 ⭐⭐⭐ 🟢 What are the main components of Power BI?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the core trio and how they connect?
**Say this in the interview:** "Three main parts: Power BI Desktop, a Windows application where I build reports and the data model; the Power BI Service, the online site where reports are published, shared and refreshed; and Power BI Mobile, the iOS and Android apps for viewing. Around these there are Report Builder for printable paginated reports and Report Server for on-premises use."
**Explain simply:**
- **Desktop** = the workshop (connect, clean, model, design).
- **Service** (app.powerbi.com) = the shop window (publish, share, schedule refresh, dashboards, security).
- **Mobile** = the phone view of what the Service holds.
- Microsoft's overview also lists **paginated reports** (pixel-perfect, printable, e.g. payslips or invoices, built in Power BI Report Builder) and **Power BI Report Server** (keeps reports on-premises).
- Many interview sites also list the **on-premises data gateway** as a component. It is a small bridge program that lets the Service reach data inside the company network. That gateway point is from memory, unverified on a page I fetched.
**Example:** HR analyst builds an attrition report in Desktop, publishes to the Service, a scheduled refresh keeps it current, and the CHRO reads it on a phone.
**DAX / Steps:** Not a measure question; no steps needed.
**Alternative:** Some candidates also name Power Query, DAX and the data model as "components". Those are engines inside Desktop, not separate products; mention that distinction.
**Version / licensing note:** Verified on Microsoft Learn: "What is Power BI?" (Desktop, Service, Mobile, paginated reports, Report Server).
**Edge cases:** The Power BI Windows app was retired on 31 December 2023 (Microsoft Learn: "What Are the Power BI Mobile Apps?"); Windows users use the Service in a browser.
**Likely follow-ups:**
1. *Which one costs money?* Desktop is free; sharing in the Service depends on licence.
2. *Is Report Server the same as the Service?* No, it is the on-premises option.
**Common mistakes:** Listing visuals (bar, pie) as components; forgetting Mobile; treating Desktop and Service as the same thing.

### Q3 ⭐⭐⭐ 🟢 What is the difference between Power BI Desktop and the Power BI Service?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand "build" versus "share and consume"?
**Say this in the interview:** "Desktop is the free Windows application where I connect to data, transform it, build the model with relationships and DAX, and design the report. The Service is the cloud site where I publish it, share it, schedule refresh, build dashboards and manage security."
**Explain simply:**
- Desktop (per Microsoft): full data modelling and design tools; Power Query Editor (data cleaning, Q8); DAX (Power BI's formula language) and relationships; performance analyzer; external tools; composite models (mixing Import and DirectQuery, Q15).
- Service (per Microsoft): workspaces, apps, dataflows, scheduled refresh, email subscriptions, alerts, row-level security (RLS, which limits which rows each person sees), sensitivity labels.
- **Dashboards are a Service feature**; Microsoft states they are not available in Desktop.
- Both can connect to data and make visuals, and the Service can also edit reports in the browser (lighter editing than Desktop).
**Example:** You build the "Headcount by Location" report in Desktop on your laptop. After Publish, the HR business partners open it in the Service, you set refresh at 7 am, and you pin one tile to an "HR Today" dashboard.
**Sample data:** Not meaningful for this question.
**DAX / Steps:** Desktop to Service (not run here): Desktop > Home > Publish > sign in > choose workspace > open in the Service.
**Alternative:** One-line memory aid: "Desktop = create, Service = collaborate."
**Version / licensing note:** Verified on Microsoft Learn: "What is Power BI?" and "Download Power BI Desktop" (Windows 10 / Windows Server 2016 or later) and "Intro to dashboards for Power BI designers". Desktop is free to download; sharing needs Pro/PPU or capacity (see Q19). A Mac Desktop is not described on the pages I fetched; "no native Mac version" is from vendor blogs, unverified.
**Edge cases:** Editing a published report in the Service does not change your local .pbix file, so keep one master copy to avoid two diverging versions.
**Likely follow-ups:**
1. *Can I build in the Service only?* Partly, see Q24 in this book.
2. *Where is DAX written?* Mainly Desktop; the Service has limited web modelling.
**Common mistakes:** Saying the Service is "the paid version of Desktop"; believing dashboards exist in Desktop.

### Q4 ⭐⭐⭐ 🟢 What are the building blocks of Power BI?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the vocabulary of Power BI content?
**Say this in the interview:** "The classic five are visuals, semantic models (earlier called datasets), reports, dashboards and tiles. A visual is one chart, a report is pages of visuals on one semantic model, a dashboard is a one-page collection of pinned tiles."
**Explain simply:**
- **Visual (visualization):** one chart, table, card or map.
- **Semantic model:** the data plus relationships and calculations that reports read (Q18).
- **Report:** one or more pages of visuals based on a single semantic model.
- **Dashboard:** a single page of tiles pinned from reports (Service only).
- **Tile:** one pinned item on a dashboard.
- Microsoft's concepts page also lists app, workspace, capacity (reserved computing power for a workspace) and dataflow (reusable data cleaning, Q45) as Service-side terms.
**Example:** Visual = "Attrition % by department" bar chart. Report = 4-page "HR Analytics" file. Dashboard = one screen with 6 tiles the CHRO checks daily.
**DAX / Steps:** Not a measure question.
**Alternative:** Some sources say the building blocks are data, model, visuals, report, dashboard; keep the Microsoft terms and explain.
**Version / licensing note:** Verified on Microsoft Learn: "Power BI service basics: key concepts and terms" (definitions of semantic model, report, dashboard, app, workspace) and "Intro to dashboards for Power BI designers" (tiles).
**Edge cases:** "Dataset" is the old word for semantic model; interviewers may still use it.
**Likely follow-ups:**
1. *Report vs dashboard?* See Q5.
2. *What is an app?* A bundle of dashboards and reports shared with a wider audience.
**Common mistakes:** Calling a report page a dashboard; listing Power Query or DAX as building blocks.

### Q5 ⭐⭐⭐ 🟢 What is the difference between a report and a dashboard in Power BI?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Precise knowledge; many candidates use the words interchangeably.
**Say this in the interview:** "A report can have many pages, is built on one semantic model and has full filtering and slicers. A dashboard is a single page in the Service made of tiles pinned from one or more reports and models, good for a quick monitoring view, and it can have alerts."
**Explain simply:**
- Pages: report has one or more; dashboard has one.
- Data: report uses a single semantic model; dashboard can combine tiles from many reports and models.
- Filtering/slicing: full in reports; not in dashboards (you can filter a tile in focus mode but cannot save it).
- Created where: reports in Desktop or Service; dashboards only in the Service (not on mobile either, though you can view them there).
- Alerts: available for dashboard tiles in certain cases; not for reports.
**Example:** The "Attendance" report has pages for daily, monthly and by location. The HR Head's dashboard shows three tiles pinned from it plus one tile from the "Hiring" report.
**DAX / Steps:** Pin a tile (not run here): open report in the Service > hover a visual > Pin visual > choose or create a dashboard.
**Alternative:** Analogy: a report is a book, a dashboard is the poster summarising it.
**Version / licensing note:** Verified on Microsoft Learn: "Intro to dashboards for Power BI designers" (comparison table). Creating dashboards in a workspace needs Pro or PPU; in My workspace it does not, per the same page.
**Edge cases:** Pinning an entire report page keeps drill-down working in that tile (from memory, unverified).
**Likely follow-ups:**
1. *Can a dashboard be built in Desktop?* No.
2. *What happens when data refreshes?* Tiles update as the underlying data changes.
**Common mistakes:** Saying a dashboard is "the fancier report"; claiming dashboards have slicers.

### Q6 ⭐⭐⭐ 🟢 What is the typical workflow of a Power BI project, from raw data to a shared dashboard?
**Asked at:** Deloitte USI Hyderabad, Sept 2025, round 2 included a Power BI project-workflow discussion (single candidate account in research/interview_processes.md; unverified at question level). Otherwise commonly asked.
**What the interviewer is checking:** Can you narrate the full pipeline in order, with the reason for each step?
**Say this in the interview:** "I get requirements first, connect to the source, clean it in Power Query, model it with a star schema and relationships, write DAX measures, design the visuals, publish to the Service, set refresh and access, then gather feedback and iterate."
**Explain simply:**
1. **Requirements:** which questions, who uses it, which KPIs (from memory, standard practice).
2. **Connect and prepare:** Get data, clean in Power Query (remove blanks, fix types).
3. **Model:** relationships between tables, ideally a star schema (small lookup tables such as Department around one central table of events); **DAX** (Power BI's formula language) measures.
4. **Build visuals:** cards, charts, slicers, tooltips.
5. **Explore and check:** validate numbers against the source.
6. **Publish and share:** workspace, app or share link; scheduled refresh; security (RLS, row-level security: each person sees only their rows).
7. **Administer/monitor.**
- Microsoft's own seven steps (get started; connect and prepare; model and combine; build; explore; share; administer and secure) match this.
**Example:** HR MIS: take the monthly HRIS export, clean department names, relate Employees to Departments and a Date table, create Headcount and Attrition % measures, publish, refresh daily at 6 am.
**DAX / Steps:** Not a single measure; see Q16 for hands-on steps.
**Alternative:** Short version for a fresher: "Get data, transform, model, visualise, publish, refresh."
**Version / licensing note:** Verified on Microsoft Learn: "What is Power BI?" (seven-step list). Scheduled refresh limits are in other books.
**Edge cases:** On-premises sources need a gateway (a small bridge program that lets the cloud reach data inside your network) for refresh in the Service (from memory, unverified).
**Likely follow-ups:**
1. *Where do you validate?* Compare totals with the source before publishing.
2. *Where is the time spent?* Usually data cleaning and modelling.
**Common mistakes:** Skipping requirements and validation; building visuals on unclean data; forgetting refresh after publishing.

### Q7 ⭐⭐⭐ 🟢 Which data sources can Power BI connect to?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Breadth of knowledge plus the ones you have actually used.
**Say this in the interview:** "Power BI Desktop connects to more than 100 sources: files like Excel, CSV, JSON and Parquet; databases such as SQL Server, PostgreSQL, MySQL, Oracle and Snowflake; Azure and Fabric sources; online services like Salesforce and Dynamics 365; and the web. I mostly use Excel, CSV and SQL Server."
**Explain simply:**
- Get Data dialog categories (legacy view): All, File, Database, Microsoft Fabric, Power Platform, Azure, Online Services, Other.
- Import copies the data in; some sources also support DirectQuery (Q15).
- The full, current connector list is on Microsoft's "Connectors in Power Query" page; I have not fetched that list, so do not recite exact counts beyond "100+".
- Beta or Preview connectors have limited support and should not be used in production.
- A folder connector can combine many files, useful for monthly HR exports.
**Example:** Attendance in monthly CSVs (Folder), employee master in SQL Server, hiring data in an ATS cloud service.
**DAX / Steps:** (not run here) Desktop > Home > Get data > choose category > Connect > Navigator > Load or Transform Data.
**Alternative:** Mention Web (URL) and Blank query for advanced users.
**Version / licensing note:** Verified on Microsoft Learn: "Data sources in Power BI Desktop" and "What is Power BI?". A new Power Query Get Data experience is in preview per the first page; the legacy dialog is described above.
**Edge cases:** Sources ask for credentials (login details, Q36); privacy levels (settings that stop data from one source leaking into another) and gateways (a bridge program for on-premises data) may also be needed.
**Likely follow-ups:**
1. *Excel or SQL, which is better?* SQL for scale and refresh; Excel for quick starts.
2. *Can you connect to a PDF?* From memory, yes via the PDF connector; unverified here.
**Common mistakes:** Saying only Excel; saying every source supports DirectQuery.

### Q8 ⭐⭐⭐ 🟢 What is Power Query, and where does it fit in the Power BI workflow?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you separate data preparation (Power Query) from calculation (DAX)?
**Say this in the interview:** "Power Query is the data preparation tool inside Power BI. It sits right after connecting to the source and before the model. I use it to clean and reshape data (remove columns, filter rows, fix data types, merge tables), and every step is recorded and replayed on each refresh."
**Explain simply:**
- Open it with Home > Transform data.
- Each action becomes an entry under **Applied steps**; underlying source data is not changed, only Power Query's view of it.
- Behind the clicks is a formula language called **M**; you can view it in the Advanced Editor (View tab).
- When done, **Close & Apply** loads the result into the model.
- Rule of thumb: Power Query prepares rows and columns before loading; DAX calculates answers after loading.
**Example:** Source Excel has "Emp ID" typed as text, blank rows and "Hyd"/"Hyderabad" inconsistencies. In Power Query you promote headers, remove blank rows, replace "Hyd" with "Hyderabad", set the type to whole number.
**DAX / Steps:** (not run here) Home > Transform data > use Transform / Add column tabs > Home > Close & Apply. Example M step generated by clicks (not run here):
```m
= Table.SelectRows(Source, each [Department] <> null)
```
**Alternative:** For small fixes you could change the source, but Power Query makes the fix repeatable at every refresh.
**Version / licensing note:** Verified on Microsoft Learn: "Query Overview in Power BI Desktop" (editor, applied steps, Advanced Editor, Close & Apply). A new Power Query editor is in preview per that page.
**Edge cases:** Step order matters; steps run top to bottom.
**Likely follow-ups:**
1. *Power Query vs DAX?* Prepare vs calculate.
2. *Does it change my Excel file?* No.
**Common mistakes:** Cleaning with DAX calculated columns instead of Power Query; forgetting Close & Apply.

### Q9 ⭐⭐⭐ 🟢 What are the different views in Power BI Desktop, and what is each one used for?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Familiarity with the Desktop interface.
**Say this in the interview:** "Report view is the canvas for building visuals. Table view shows loaded data row by row and is where I check columns and add measures. Model view shows tables and relationships. There is also DAX query view for writing and testing DAX queries, and Power Query Editor opens separately for cleaning."
**Explain simply:**
- **Report view:** design pages, drag fields, format visuals.
- **Table view:** see data after it is loaded into the model; the formula bar lets you write DAX for measures and calculated columns.
- **Model view:** drag lines between tables to manage relationships.
- **DAX query view:** an editor where you write queries (EVALUATE) and can test measures; icon on the left side.
- **Power Query Editor:** separate window (Home > Transform data).
- Microsoft's query overview page says there are three views (Report, Table, Model); a newer page documents DAX query view too. A TMDL view is also mentioned on that DAX page; I have not read its documentation.
**Example:** You notice a wrong total in Report view, switch to Table view to see raw rows, then Model view to find a missing relationship.
**DAX / Steps:** Click the icons on the left edge of Desktop (not run here).
**Alternative:** Mention that the icon for Table view is hidden when all sources are DirectQuery (per Microsoft).
**Version / licensing note:** Verified: Microsoft Learn "Query Overview in Power BI Desktop", "Table view in Power BI Desktop", "DAX Query View". Views vary by Desktop release.
**Edge cases:** Table view differs from Power Query: it shows data after loading.
**Likely follow-ups:**
1. *Where do you create relationships?* Model view.
2. *Where do you fix data types before loading?* Power Query.
**Common mistakes:** Saying Power Query Editor is a view in the left bar; saying only three views exist without mentioning DAX query view.

### Q10 ⭐⭐⭐ 🟢 What is a .pbix file and what does it contain?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Knowing what you are saving and sharing.
**Say this in the interview:** ".pbix is the file Power BI Desktop saves. It holds the whole project: the queries, the data model with relationships and measures, the report pages and visuals, and, for Import mode, a copy of the data."
**Explain simply:**
- Microsoft's query overview page confirms Desktop saves work as a .pbix (File > Save).
- Contents (queries, model, report, data cache) are from memory, unverified on a single page; the PBIP page does mention a local data cache for the semantic model.
- Because it can contain the data, a .pbix may hold salaries and other sensitive HR data: do not email it casually.
- Alternative save format: **Power BI Project (.pbip)** stores report and model as folders of text files, useful for Git version control; you can convert .pbix to .pbip and back via Save As.
- A **.pbit** template (same project without the data) is covered in Q41.
**Example:** An HR analyst saves "Attrition_Dashboard.pbix" (30 MB). It includes the cleaned data, so sharing it externally would leak employee details; instead publish to the Service with access control.
**DAX / Steps:** File > Save as > choose .pbix or Power BI project (not run here).
**Alternative:** Publishing from Desktop sends the model and report to the Service as a semantic model plus report.
**Version / licensing note:** Verified: Microsoft Learn "Query Overview in Power BI Desktop", "Power BI Desktop projects (PBIP)". Contents list: from memory, unverified. The .pbit point is in Q41.
**Edge cases:** A newer .pbix cannot be opened by older Desktop versions ("Download Power BI Desktop" page).
**Likely follow-ups:**
1. *File too big?* Reduce columns/rows or use better modelling.
2. *.pbix vs .pbip?* Binary bundle vs text folders.
**Common mistakes:** Thinking .pbix is only the report visuals; sending it to external parties with confidential data.

### Q11 ⭐⭐⭐ 🟢 When you load data into Power BI, what is the difference between Load and Transform Data?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the choice in the Navigator window?
**Say this in the interview:** "After I pick tables in the Navigator, Load brings the data into the model exactly as it is. Transform Data opens Power Query Editor first so I can clean it, and then I Close & Apply to load the cleaned data. With real HR data I almost always choose Transform Data."
**Explain simply:**
- Both buttons are at the bottom of the **Navigator** dialog (per Microsoft).
- **Load** = import as is. Good for already clean, simple tables.
- **Transform Data** = open Power Query Editor, apply steps, then Close & Apply.
- You can open Power Query later from Home > Transform data, so Load is not a one-way door.
**Example:** A leave file with dates stored as text: Load would give wrong date behaviour; Transform Data lets you set the type to Date first.
**DAX / Steps:** Home > Get data > Excel > select file > Navigator > Load, or Transform Data (not run here).
**Alternative:** Load first, then edit queries later via Home > Transform data.
**Version / licensing note:** Verified: Microsoft Learn "Data sources in Power BI Desktop" and "Get started with Power BI Desktop".
**Edge cases:** For DirectQuery sources, Load may only connect and not import.
**Likely follow-ups:**
1. *Does Transform Data change the source file?* No.
2. *What is Close & Apply?* It applies steps and returns to Desktop.
**Common mistakes:** Loading messy data and fixing in DAX; closing the editor without applying.

### Q12 ⭐⭐⭐ 🟢 How is Power BI different from Excel, and why would you use it for HR MIS reporting?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you justify the switch with real HR needs, without bashing Excel?
**Say this in the interview:** "Excel is great for ad-hoc analysis and small data. Power BI is built for repeatable reporting: it handles larger data, keeps cleaning steps repeatable, links several tables in a model, refreshes on a schedule and shares one interactive report with access control. For HR MIS that means no more monthly copy-paste."
**Explain simply:**
- **Refresh:** the report updates from the source; no rebuilding pivots (scheduled refresh is a Service feature).
- **Model:** relationships between tables (Employees, Departments, Dates) instead of lookup formulas.
- **Sharing and security:** publish once; RLS shows each HR partner only their business unit.
- **Interactivity:** click a bar to filter everything.
- Excel still wins for quick one-off calculations; many teams use both (Analyze in Excel connects a workbook to a Power BI model, per Microsoft).
- Specific row/size limits and speed claims: from memory, unverified.
**Example:** Monthly headcount pack takes 3 hours of Excel pivots across 5 sheets. In Power BI, new month's file goes in the folder, one refresh updates all pages.
**DAX / Steps:** Not a measure question.
**Alternative:** Frame it as: Excel = calculator and notebook, Power BI = reporting system.
**Version / licensing note:** Verified: Microsoft Learn "Get started with Power BI Desktop" (Analyze in Excel, Power Query shared with Excel workbook import) and "What is Power BI?". Excel size limits from memory.
**Edge cases:** Small, one-off data: Excel is enough.
**Likely follow-ups:**
1. *Can Power BI replace Excel?* Not entirely.
2. *Is Power BI harder to learn?* DAX takes practice.
**Common mistakes:** Claiming Excel cannot do anything useful; ignoring security and data privacy when moving HR data.

### Q13 ⭐⭐⭐ 🟢 Explain Power BI end to end to a non-technical HR manager in two minutes.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Communication: plain language, a story, no jargon.
**Say this in the interview:** "Think of Power BI as a smart notice board. We connect it to your HR files, clean them once, and build a page where you click 'Hyderabad' or 'Sales' and every number updates. It refreshes automatically, and you read it on your laptop or phone."
**Explain simply:**
- **Step 1, connect:** link to the employee file or HRIS export.
- **Step 2, clean:** fix spelling, blank rows and dates once; the fixes repeat every refresh.
- **Step 3, link tables:** employees, departments, months, so numbers agree.
- **Step 4, calculate:** headcount, attrition %, average tenure.
- **Step 5, show:** charts and filters.
- **Step 6, share:** publish; only permitted people see their data.
- **Step 7, refresh:** daily, so no monthly rebuilding.
**Example:** "Last month 18 people left from a headcount of 360, which is 5%. Click 'IT' and you see 8 of 90, which is 8.9%. Same page, no new file."
**DAX / Steps:** None.
**Alternative:** Use a pizza-restaurant analogy: ingredients (data), kitchen (prep), menu (report).
**Version / licensing note:** Seven-step flow matches Microsoft Learn "What is Power BI?".
**Edge cases:** Do not mention DAX or star schema unless asked.
**Likely follow-ups:**
1. *Is the data safe?* Access is controlled with permissions and RLS.
2. *How often does it update?* As scheduled.
**Common mistakes:** Jargon (DAX, ETL, semantic model) without explanation; no example; going over time.

### Q14 ⭐⭐⭐ 🟢 Employee ID is being added up (summed) in your table visual. Why does Power BI do that, and how do you stop it?
**Asked at:** commonly asked (no company-specific report found; a very common beginner task)
**What the interviewer is checking:** Understanding default aggregation and the difference between a number you add and a number that is only a label.
**Say this in the interview:** "Power BI treats numeric columns as things to add up, so it applies Sum by default. For an ID that is wrong. I set the column to Don't summarize in Column tools, or change it to Text in Power Query. If I need a count of employees I write a DISTINCTCOUNT measure."
**Explain simply:**
- Every column carries a "summarize by" setting. Numeric columns default to Sum. The TMDL sample on Microsoft's DAX query view page shows this as a column property (`summarizeBy: sum` for Quantity, `summarizeBy: none` for key columns).
- Fix 1, per visual: in the Values well, open the field's drop-down and choose Don't summarize (from memory, unverified; confirmed only by community posts surfaced in search, not fetched).
- Fix 2, permanent: select the column in Data pane > Column tools tab > Summarization > Don't summarize (from memory, unverified).
- Fix 3, cleanest: in Power Query set the type to Text, because IDs, phone numbers and pin codes are labels, not quantities.
**Example:** Five employees (IDs 1001 to 1005). A grand total of 5015 for "Employee ID" is meaningless; the real headcount is 5.
**Sample data:** Table: Employees

| EmployeeID | Name | Department | Salary |
|---|---|---|---|
| 1001 | Asha | HR | 52000 |
| 1002 | Ravi | IT | 78000 |
| 1003 | Meena | IT | 81000 |
| 1004 | Imran | Sales | 60000 |
| 1005 | Sneha | HR | 49000 |

**DAX / Steps:** Measure (not run here):
```dax
Employee Count = DISTINCTCOUNT ( Employees[EmployeeID] )
```
Click-path (not run here): select EmployeeID in the Data pane > Column tools > Summarization > Don't summarize.
**Alternative:** `Headcount = COUNTROWS ( Employees )` when each row is one employee.
**Result:** Reproduced with pandas (not run in DAX): summing EmployeeID gives 5015; Employee Count gives 5 overall, HR 2, IT 2, Sales 1.
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"EmployeeID":[1001,1002,1003,1004,1005],
  "Department":["HR","IT","IT","Sales","HR"]})
print(emp.EmployeeID.sum())          # 5015
print(emp.EmployeeID.nunique())      # 5
print(emp.groupby("Department").EmployeeID.nunique())
```
Output (run with pandas 3.0.5): `5015`, `5`, then HR 2, IT 2, Sales 1.
**Version / licensing note:** DISTINCTCOUNT and COUNTROWS verified on Microsoft Learn (DISTINCTCOUNT function (DAX); COUNTROWS function (DAX)). Menu names from memory, unverified.
**Edge cases:** DISTINCTCOUNT counts a blank as a value (use DISTINCTCOUNTNOBLANK to skip it), and (from memory, unverified) returns BLANK if there are no rows; distinct counts are not additive across categories, so totals can be smaller than the sum of parts.
**Likely follow-ups:**
1. *Why does a Name column not sum?* Text cannot be added.
2. *Will fixing it in one visual fix all?* No; the column-level setting does.
**Common mistakes:** Leaving IDs as numbers; using Count instead of Count (Distinct) when IDs repeat; fixing it per visual and forgetting new visuals.

### Q15 ⭐⭐⭐ 🟡 What is the difference between Import mode and DirectQuery mode?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the trade-off between speed and freshness?
**Say this in the interview:** "Import copies the data into Power BI's in-memory model, so visuals are fast and every feature works, but data is only as fresh as the last refresh. DirectQuery leaves data in the source and sends a query for each visual, so it is current but slower and has limits. I default to Import unless data is huge or must be near real time."
**Explain simply:**
- **Import:** data cached in the model; refresh to update; Microsoft says to use Import by default.
- **DirectQuery:** no data imported; each visual queries the source; speed depends on the source; one-million-row intermediate result limit per query (Premium can raise it).
- **Live connection:** connects to an existing semantic model or Analysis Services (Microsoft's server engine that hosts models); no Power Query.
- Newer options: hybrid tables (mix of both), Direct Lake (Fabric), composite models, aggregations.
- Refresh frequency (Pro 8 per day, Premium/PPU 48) is from the DirectQuery page.
**Example:** Quarterly HR report from Excel: Import. A live attendance feed where swipes must show within minutes: consider DirectQuery or a hybrid table.
**DAX / Steps:** (not run here) Get data > choose source > in the connection dialog choose Import or DirectQuery.
**Alternative:** Composite model: Import small dimension tables, DirectQuery the huge fact table.
**Version / licensing note:** Verified on Microsoft Learn: "DirectQuery in Power BI: When to Use, Limitations, Alternatives" (updated 2026-09-16). Refresh counts can change; cite the page.
**Edge cases:** You cannot flip a whole Import model to DirectQuery; DirectQuery loses automatic date hierarchy and some DAX/visual features.
**Likely follow-ups:**
1. *Which is faster?* Import.
2. *Which needs a gateway?* Both for on-premises sources.
**Common mistakes:** Choosing DirectQuery "to be real time" without checking the source speed; forgetting that Import data goes stale until refreshed.

### Q16 ⭐⭐⭐ 🟡 Walk me through building your first report from an Excel file in Power BI Desktop.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you actually do the basic workflow, in order?
**Say this in the interview:** "I open Desktop, Get data > Excel, pick the sheet or table in Navigator, choose Transform Data to clean it, Close & Apply, then drag fields to make visuals such as a headcount-by-department chart and a card, add a slicer, save the .pbix and publish."
**Explain simply:**
- Connect, clean, build, save, publish, matching Microsoft's tutorial.
- Add a measure rather than dragging raw columns when you need a count.
- Check totals against the Excel file.
**Example:** Employees.xlsx with 6 rows: Headcount 6, total salary 410,000.
**Sample data:** Table: Employees

| EmployeeID | Department | Salary |
|---|---|---|
| 1001 | HR | 52000 |
| 1002 | IT | 78000 |
| 1003 | IT | 81000 |
| 1004 | Sales | 60000 |
| 1005 | HR | 49000 |
| 1006 | IT | 90000 |

**DAX / Steps:** Click-path (not run here), following Microsoft's tutorial:
1. Home > Get data > Excel > select file > Open.
2. In Navigator, tick the table > Transform Data (or Load).
3. Power Query: set EmployeeID to Text, Salary to Whole number > Close & Apply.
4. Report view: create the two measures below (Home > New measure), then tick Department and Headcount in the Data pane (older name: Fields pane); change visual type in the Visualizations pane.
5. File > Save; Home > Publish > pick workspace.
Measures (not run here):
```dax
Headcount = COUNTROWS ( Employees )
Total Salary = SUM ( Employees[Salary] )
```
**Alternative:** Drag Salary into a visual and let default Sum work, but a named measure is reusable.
**Result:** Reproduced with pandas: HR 2 / 101,000; IT 3 / 249,000; Sales 1 / 60,000; grand total 6 / 410,000.
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"EmployeeID":range(1001,1007),
  "Department":["HR","IT","IT","Sales","HR","IT"],
  "Salary":[52000,78000,81000,60000,49000,90000]})
print(emp.groupby("Department").agg(Headcount=("EmployeeID","count"),TotalSalary=("Salary","sum")))
print(len(emp), emp.Salary.sum())
```
Output (run with pandas 3.0.5): HR 2, 101000; IT 3, 249000; Sales 1, 60000; then `6 410000`.
**Version / licensing note:** Verified: Microsoft Learn "Get started with Power BI Desktop"; DAX COUNTROWS and SUM function pages. Publishing to a workspace needs a Service account/licence (from the licence page, see Q19).
**Edge cases:** Excel file moved later gives a connection error; blank rows; headers not promoted.
**Likely follow-ups:**
1. *How do you refresh?* Home > Refresh.
2. *Where is the file saved?* As .pbix.
**Common mistakes:** Loading without checking data types; summing IDs; forgetting to save before publishing.

### Q17 ⭐⭐ 🟢 What is Power BI Mobile and who uses it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Awareness of consumption on phones and what can and cannot be done there.
**Say this in the interview:** "Power BI Mobile is the app for iOS and Android phones and tablets to view and interact with reports and dashboards from the Service. Managers use it to check KPIs on the go; creators design a phone layout in Desktop so reports fit a small screen."
**Explain simply:**
- Per Microsoft: you create reports in Desktop, create dashboards in the Service, and view both in the mobile apps.
- Features mentioned: phone layout view, data alerts, QR code scanning, geographic filtering, Apple Watch, favourites, Intune management for organisations.
- You cannot create dashboards on mobile, only view and share them.
- The Windows app was retired on 31 Dec 2023; use the Service in a browser on Windows.
**Example:** An HR head at an airport checks yesterday's attendance tile and sets an alert if absenteeism goes above 6%.
**DAX / Steps:** (not run here; menu path from memory, unverified) Desktop > View tab > Mobile layout > arrange visuals > publish.
**Alternative:** Use the browser version of the Service on a phone.
**Version / licensing note:** Verified: Microsoft Learn "What Are the Power BI Mobile Apps?" (dated 2025-10 and updated 2026-02) and "Intro to dashboards for Power BI designers". Which licence a mobile viewer needs: not on the pages I read; see Q3/Q19 for sharing rules.
**Edge cases:** A report without a mobile layout is shown the desktop layout.
**Likely follow-ups:**
1. *Can you edit on mobile?* Mainly view and interact.
2. *Who sees what?* Same permissions as the Service.
**Common mistakes:** Thinking the mobile app builds reports; skipping the phone layout.

### Q18 ⭐⭐ 🟢 What is a semantic model (formerly called a dataset) in Power BI?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Know the renamed term and what it holds.
**Say this in the interview:** "A semantic model is the data model that reports are built on: the tables, relationships and measures, plus the connection to the source. It used to be called a dataset. Many reports can use the same model so the numbers match everywhere."
**Explain simply:**
- Microsoft: semantic models represent a source of data ready for reporting and visualization; formerly known as dataset.
- A model developed in Desktop is effectively an Analysis Services tabular model (Microsoft's engine that stores and calculates models), and runs in Import, DirectQuery or Composite mode.
- It can be created by uploading a Desktop file, an Excel workbook or CSV, or by connecting to an external model.
- Models can enforce row-level security.
- Import models need refresh (scheduled or on demand); ownership matters for changing settings.
**Example:** One "HR Core" semantic model with Employees, Departments and Dates feeds three reports (Attrition, Headcount, Hiring) so Headcount means the same everywhere.
**DAX / Steps:** In the Service: workspace > semantic model "..." menu > settings / refresh (not run here).
**Alternative:** Think of it as a "data warehouse in a box" for reports.
**Version / licensing note:** Verified: Microsoft Learn "Semantic Models in the Power BI Service" and "Power BI service basics: key concepts and terms".
**Edge cases:** Docs sometimes use "model" and "semantic model" interchangeably; the older term "dataset" still appears in tools and interviews.
**Likely follow-ups:**
1. *Why share one model?* Consistency, fewer refreshes.
2. *Where is the data stored?* In Import mode, inside the model.
**Common mistakes:** Treating the term as a new thing; confusing semantic model with the report itself.

### Q19 ⭐⭐ 🟢 Is Power BI Desktop free, and how do you install it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Practical knowledge for getting started and the free vs paid boundary.
**Say this in the interview:** "Yes, Desktop is free. I install it from the Microsoft Store, which updates automatically, or download the 64-bit installer from the Microsoft Download Center. It needs Windows 10 or later. Sharing reports to other people in the Service needs a Pro or Premium Per User licence, or content in a capacity."
**Explain simply:**
- Microsoft: "Download Power BI Desktop for free"; Store or direct .exe.
- Store advantages: automatic updates, smaller updates, no admin rights needed, IT roll-out.
- Direct installer needs admin rights; the 32-bit version is no longer supported.
- Minimum: Windows 10 or Windows Server 2016 or later; .NET 4.7.2 or later; at least 2 GB RAM (4 GB recommended); display at least 1440x900 or 1600x900.
- Microsoft releases Desktop monthly and supports only the latest version.
- Mac: not covered on the pages I read (they describe Windows); people use a Windows VM or the browser Service (vendor blogs, unverified).
- Free licence cannot share or publish to others' workspaces; Pro/PPU can, and capacity (Fabric F64+ or Premium) lets free users consume.
**Example:** A fresher installs Desktop on a laptop from the Store and builds a practice report without paying; to share with a team lead, the company must give licences.
**DAX / Steps:** (not run here) Open the Microsoft Store > search Power BI Desktop > Install; or Download Center > Download > choose 64-bit > Next > run installer. Check version: Help > About.
**Alternative:** From the Service, the Download icon (top right) > Power BI Desktop (from memory, unverified).
**Version / licensing note:** Verified: Microsoft Learn "Download Power BI Desktop" (ms.date 2026-10-09) and "Power BI service features by license type" (ms.date 2026-08-24). Prices not quoted; they change.
**Edge cases:** Store and old .msi versions side by side are not supported; work laptops may block installs.
**Likely follow-ups:**
1. *Can a free-licence colleague open my report?* Not unless it is in a capacity workspace.
2. *Why can't I use a Mac?* Desktop is a Windows application.
**Common mistakes:** Saying Power BI is entirely free; installing the 32-bit version; assuming a Mac works.

### Q20 ⭐⭐ 🟢 What is a tile in Power BI, and how is one created?
**Asked at:** commonly asked (no company-specific report found); "building blocks" lists (visuals, datasets, reports, dashboards, tiles) on tutorial sites such as DataFlair.
**What the interviewer is checking:** Do you know a tile lives on a dashboard in the Power BI Service, not in a Desktop report page?
**Say this in the interview:** "A tile is one box on a dashboard. It is a snapshot of a visual, usually pinned from a report, such as a card showing attrition percent. Dashboards and tiles exist only in the Power BI Service, not in Desktop. I pin a visual from a published report to create one."
**Explain simply:**
- **Dashboard:** one screen that gathers the most important numbers from one or more reports. It is the "notice board" and the report is the "full file".
- **Tile:** one box on that dashboard. It can come from a report visual, Q&A, Excel, a paginated report, or be a standalone text box, image, video, web or streaming tile (Microsoft Learn: Introduction to Dashboard Tiles for Power BI Designers).
- Clicking a tile opens the report it came from, so a manager sees the headline and then drills in.
- If you later change the visual in the report (line to bar), the tile keeps its old type. The data refreshes; the chart type does not.
- A visual in a report is not a tile until you pin it.
**Example:** The HR head wants a dashboard with three tiles: Headcount (card), Attrition % (card) and Hires by month (column chart). All three are pinned from the "HR Monthly" report.
**Sample data:**

Table: Employees

| EmpID | Name | Dept | Status | Salary |
|---|---|---|---|---|
| 101 | Asha | Sales | Active | 40000 |
| 102 | Ravi | Sales | Left | 52000 |
| 103 | Meena | HR | Active | 35000 |
| 104 | Karan | HR | Active | 60000 |
| 105 | Divya | IT | Left | 48000 |
| 106 | Imran | IT | Active | 55000 |
| 107 | Sneha | IT | Active | 62000 |
| 108 | Tarun | Sales | Active | 45000 |

**DAX / Steps:** (not run here)
The measure behind the "Attrition %" card visual:
```dax
Attrition % =
DIVIDE (
    CALCULATE ( COUNTROWS ( Employees ), Employees[Status] = "Left" ),
    COUNTROWS ( Employees )
)
```
Steps (not run here): 1) Desktop: build the card visual, then Home > Publish to a workspace. 2) Service: open the report, hover the visual, select the pin icon (Pin visual), choose an existing or new dashboard, then Pin. 3) For a text box or image tile: open the dashboard > Edit > Add a tile (from memory, unverified; Learn names the "Add tile" control).
**Alternative:** Pin a whole report page as a live tile (from memory, unverified), or create the tile from Q&A by typing a question in the dashboard question box.
**Result:** Reproduced with pandas: 2 of 8 employees have Status "Left", so the card shows 0.25, formatted as 25.0%. DIVIDE, COUNTROWS and CALCULATE syntax checked on Microsoft Learn; the numbers are not from a DAX engine.
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"Status":["Active","Left","Active","Active","Left","Active","Active","Active"]})
att = (emp.Status == "Left").sum() / len(emp)
print("Attrition % =", round(att*100, 1))
```
Output (run with pandas 3.0.5): `Attrition % = 25.0`
**Version / licensing note:** Verified on Microsoft Learn ("Introduction to Dashboard Tiles for Power BI Designers"): dashboards and tiles are Power BI Service features, not in Desktop, and you cannot create dashboards on mobile but can view and share them. Sharing a dashboard needs a Pro or higher licence, unless content sits in Premium or Fabric F64+ capacity (Microsoft Learn: Power BI service features by license type).
**Edge cases:** If you never saved the report, clicking the tile does nothing. Some formatting (background colour, tooltip settings) does not carry to the tile. Tiles from import models refresh when the semantic model refreshes.
**Likely follow-ups:** 1) *Report vs dashboard?* Report: many pages, one semantic model, built in Desktop. Dashboard: one page of tiles, can mix several reports. 2) *Can a tile come from two reports?* Yes, the dashboard can hold tiles from several.
**Common mistakes:** Looking for "Add tile" in Desktop; thinking a tile and a visual are the same object; expecting the tile to follow later chart-type changes.

### Q21 ⭐⭐ 🟢 What are Power Query, Power Pivot and Power View, and how do they relate to Power BI today?
**Asked at:** commonly asked (no company-specific report found); the three names appear in component lists on Indian prep sites (AnalytixLabs, Jaro Education).
**What the interviewer is checking:** Can you separate the three Excel-era add-ins and say where each idea lives in Power BI now?
**Say this in the interview:** "Power Query is the data cleaning tool, Power Pivot is the data modelling engine with DAX, and Power View was the Excel tool for interactive charts. Power BI Desktop has all three ideas built in: the Power Query Editor, the model with DAX, and the report canvas."
**Explain simply:**
- **Power Query:** get and clean data and save the steps so they repeat on refresh. It writes a language called M behind the scenes. It exists in Excel and in Power BI (Microsoft Learn: What Is Power Query?).
- **Power Pivot:** Excel's data model: tables, relationships, calculated columns and measures in DAX. In Power BI Desktop this is the model view and DAX.
- **Power View:** Excel's interactive charts. Its job is now done by Power BI reports (retirement date: from memory, unverified).
- Excel workbooks that have these can be converted in one go: File > Import > Power Query, Power Pivot, Power View (Microsoft Learn: Import Excel workbooks into Power BI Desktop).
**Example:** An HR analyst already has an Excel file where Power Query merges attendance sheets and Power Pivot holds a Headcount measure. She imports it into Power BI Desktop and gets the queries, model and an auto-built report.
**DAX / Steps:** (not run here) Power BI Desktop > File > Import > Power Query, Power Pivot, Power View > pick the workbook > Start > Close. Desktop creates a .pbix; Learn says this is a one-time conversion and the .pbix no longer depends on the Excel file.
**Alternative:** Simple sheet only: Home > Get data > Excel instead.
**Version / licensing note:** Verified on Microsoft Learn (Import Excel workbooks into Power BI Desktop; What Is Power Query?). Hierarchies and binary columns do not import, per that page. Power View retirement status: from memory, unverified.
**Edge cases:** Named ranges used via Excel.CurrentWorkbook load as a connection to the Excel file, so the file must stay reachable. Analysis Services connections created in Excel must be rebuilt (per the same page).
**Likely follow-ups:** 1) *Is Power Query only in Power BI?* No: Excel, Power Apps, dataflows and more. 2) *What is M?* The formula language Power Query writes for every step.
**Common mistakes:** Saying Power Pivot is a separate Power BI product today; mixing up Power Query (clean) and DAX (calculate).

### Q22 ⭐⭐ 🟢 What are the main panes of the Power BI Desktop report canvas (Visualizations, Data, Filters)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic familiarity with the screen you will use daily.
**Say this in the interview:** "The big middle area is the report canvas. On the right I have the Visualizations pane to pick chart types and drop fields, the Data pane listing my tables and fields, and the Filters pane for page, report and visual filters. The ribbon sits on top."
**Explain simply:**
- **Report canvas:** the page where visuals are arranged.
- **Visualizations pane:** chart icons plus the wells (Axis, Values, Legend) and formatting.
- **Data pane:** tables, columns and measures. Older material and Microsoft's own text call it the Fields pane; Learn says Fields is "called the Data pane in current releases" (Microsoft Learn: Use the Field list in Power BI Desktop).
- **Filters pane:** filters at visual, page or all-pages level (not on the fetched pages; from memory, unverified).
- **Ribbon:** Home, Insert, Modeling and more (Microsoft Learn: Get started with Power BI Desktop).
**Example:** To show attrition by department, tick Dept and Status in the Data pane, change the visual to a stacked bar in the Visualizations pane, and filter to "Year = 2026" in the Filters pane.
**DAX / Steps:** (not run here) Panes show or hide from View ribbon (from memory, unverified); the view switcher on the left (Report, Table, Model) is also from memory, unverified.
**Alternative:** Use Selection and Bookmarks panes (View ribbon) for layering and navigation; both from memory, unverified.
**Version / licensing note:** Pane names verified on Microsoft Learn (Get started with Power BI Desktop; Use the Field list in Power BI Desktop). Filters pane and View-ribbon steps: from memory, unverified. Desktop is a free Windows application per Learn.
**Edge cases:** A filter set at visual level affects only that visual; page-level filters affect the page. Fields hidden in the model do not appear in the Data pane.
**Likely follow-ups:** 1) *Where do I change colours?* Format tab of the Visualizations pane. 2) *Slicer vs filter pane?* A slicer is on the canvas for viewers; the Filters pane is for the author, though viewers can use it if left visible.
**Common mistakes:** Calling the Data pane "dataset"; hunting for fields in the Visualizations pane.

### Q23 ⭐⭐ 🟢 How do you connect Power BI Desktop to an Excel file or a SQL Server database?
**Asked at:** commonly asked (no company-specific report found); Get Data appears in Keka's beginner Q&A.
**What the interviewer is checking:** Can you walk the Get data flow and mention Import vs DirectQuery and credentials?
**Say this in the interview:** "Home, Get data, choose Excel workbook or SQL Server database. For Excel I pick the file and tick the sheet or table in Navigator. For SQL Server I type server and database name, choose Import or DirectQuery, sign in, then choose tables. I click Load, or Transform Data if the data needs cleaning first."
**Explain simply:**
- **Navigator:** preview window where you tick the tables.
- **Load:** copy into the model. **Transform Data:** open Power Query first to clean it.
- **SQL Server:** also offers Import (copy, fast, refresh needed) or DirectQuery (query live) in Desktop only (Microsoft Learn: Power Query SQL Server connector).
- **Credentials:** first connection asks for Windows, Database (username and password) or Organizational account.
**Example:** HR loads `Attendance.xlsx` (sheet "Jan") and joins it with the `Employees` table from the company SQL Server.
**DAX / Steps:** (not run here)
Excel: 1) Home > Get data > Excel workbook. 2) Browse, Open. 3) In Navigator tick the sheet or table. 4) Load (Microsoft Learn: Get started with Power BI Desktop).
SQL Server: 1) Home > Get data > SQL Server database. 2) Enter Server and optional Database. 3) Choose Import or DirectQuery, OK. 4) First time: pick authentication, enter credentials, Connect. 5) Navigator > Load or Transform Data (Microsoft Learn: Power Query SQL Server connector).
Power Query M equivalent for the SQL step: `Sql.Database("ServerName", "HRDB")` (function named on the same Learn page; not run here).
**Alternative:** Paste data with Enter data, or use Get data > Text/CSV for CSV files. A CSV opened with the Excel connector gives errors; use Text/CSV (Learn: Power Query Excel connector).
**Version / licensing note:** Verified on Microsoft Learn (Get started with Power BI Desktop; Power Query SQL Server connector; Power Query Excel connector). Legacy .xls or .xlsb files need the Access Database Engine (ACE) provider. A new Power Query Get Data experience is in preview, per Learn (Data sources in Power BI Desktop), so screens may differ. Desktop is Windows-only per Learn.
**Edge cases:** Excel formatted as plain ranges (not tables) shows "suggested tables". An unencrypted SQL connection shows a warning dialog. Using Entra ID sign-in works only if the SQL server supports it.
**Likely follow-ups:** 1) *Import or DirectQuery?* Import by default (Q15). 2) *Can I connect to many Excel files?* Use the Folder connector, per Learn.
**Common mistakes:** Loading the whole sheet with title rows; choosing DirectQuery without needing it; storing source files on a personal laptop path and then scheduling refresh.

### Q24 ⭐⭐ 🟢 Can you create a report directly in the Power BI Service without Power BI Desktop?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the Service can author simple reports, and where Desktop is still needed?
**Say this in the interview:** "Yes. In the Service I can upload an Excel file as a semantic model, click Create report and drag visuals. It is good for quick reports or Mac users. For complex modelling, DAX-heavy work or heavy Power Query I still use Desktop."
**Explain simply:**
- **Semantic model:** the data container a report reads (formerly called a dataset).
- Path from Learn: My workspace > New > Semantic model > Excel > upload > More options (...) > Create report (Microsoft Learn: Create a report from an Excel file in the Power BI service).
- The Service editor has the same Data and Visualizations panes.
- Service can even edit DirectQuery models in the browser, so "Desktop only" is no longer absolute (Microsoft Learn: DirectQuery in Power BI).
**Example:** A recruiter on a Mac uploads `HiringFunnel.xlsx` and builds a funnel bar chart in the browser in ten minutes.
**DAX / Steps:** (not run here) Sign in at app.powerbi.com > My workspace > New > Semantic model > Excel > Browse this device > select file > open More options (...) next to the model > Create report > drag fields > Save.
**Alternative:** Edit an existing published report: open it > Edit. Or Create > Paste or manually enter data (from memory, unverified).
**Version / licensing note:** Verified: path and capabilities on the two Learn pages named above. A Free licence user can create content for personal use but cannot share or publish to others' workspaces (Learn: Power BI service features by license type). Which advanced features (full Power Query, all modelling) are missing in the browser: from memory, unverified.
**Edge cases:** Data uploaded from a local Excel file is a snapshot, not refreshed unless the file sits on OneDrive or SharePoint (Learn: Data refresh in Power BI describes OneDrive refresh).
**Likely follow-ups:** 1) *Can I download the .pbix?* From memory, unverified; depends on how it was created. 2) *Share with colleagues?* Needs Pro or capacity (Q30).
**Common mistakes:** Assuming service and Desktop are identical; uploading a local file and expecting it to update.

### Q25 ⭐⭐ 🟢 How do you export the data behind a visual to Excel or CSV?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the Export data menu and the summarized vs underlying difference?
**Say this in the interview:** "Hover the visual, More options, Export data. In the Service I can choose summarized data, which is what the visual shows, or underlying data, which is the detail rows. In Desktop it exports a CSV. The report owner or admin can switch export off."
**Explain simply:**
- **Summarized data:** the same numbers as the visual (grouped totals).
- **Underlying data:** row-level detail from the model; needs build permission.
- Service file options per Learn: .xlsx with live connection (up to 500,000 rows), .xlsx (up to 150,000 rows) or .csv (up to 30,000 rows). Desktop exports .csv only.
- Filters and slicers are respected; the export honours row-level security.
**Example:** The visual shows headcount by department (3 rows). Summarized export gives those 3 rows; underlying gives all 8 employee rows.
**Sample data:** Employees table as in Q20 (8 rows).
**DAX / Steps:** (not run here) Select the visual > More options (...) > Export data > pick Summarized or Underlying > pick file format > Export (Microsoft Learn: Export Data From a Power BI Visualization). Designer setting: File > Options and settings > Options > Current file > Report settings > Export data.
Measure behind the visual:
```dax
Headcount = COUNTROWS ( Employees )
```
**Alternative:** Analyze in Excel (Service > More options > Analyze in Excel) to get a live PivotTable (Microsoft Learn: Get started with Power BI Desktop).
**Result:** Reproduced with pandas: summarized = HR 2, IT 3, Sales 3 (3 rows); underlying = 8 rows. Not from a Power BI engine.
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"EmpID":range(101,109),
  "Dept":["Sales","Sales","HR","HR","IT","IT","IT","Sales"]})
s = emp.groupby("Dept", as_index=False).agg(Headcount=("EmpID","count"))
print(s); print("Underlying rows:", len(emp))
```
Output (run with pandas 3.0.5): HR 2, IT 3, Sales 3, then `Underlying rows: 8`.
**Version / licensing note:** Verified on the Learn export page: row limits above; custom visuals may not support export; admins can disable export and admin settings override report settings. Sensitivity labels carry to xlsx exports.
**Edge cases:** Grayed-out Export means the designer or admin disabled it. CSV has no total rows. With DirectQuery the export is limited to 16 MB uncompressed. Underlying export fails if "Show items with no data" is on or tables have no unique key.
**Likely follow-ups:** 1) *Why is my export truncated?* Row cap. 2) *Is sensitive HR data safe?* Labels and RLS apply; still restrict export for salary data.
**Common mistakes:** Exporting salary data without checking the policy; expecting more than 30,000 rows in CSV.

### Q26 ⭐⭐ 🟢 Where do you get custom visuals in Power BI?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the safe sources and the security caveat?
**Say this in the interview:** "From Microsoft AppSource through Get more visuals in the Visualizations pane, from my organisation's approved store, or by importing a .pbiviz file. I prefer certified visuals and I check with IT before using anything that sends data outside."
**Explain simply:**
- **Core visuals:** built-in ones already in the pane.
- **AppSource:** Microsoft marketplace; many are free, some paid (Microsoft Learn: Main sources for acquiring Power BI custom visuals).
- **Certified visuals:** pass Microsoft code checks, including no access to external services.
- **Organizational store:** admin-approved visuals under Get more visuals > My organization tab.
- **.pbiviz file:** a packaged visual you import from your computer; trust the author first.
**Example:** An HR analyst adds an org-chart visual from AppSource to show reporting lines.
**DAX / Steps:** (not run here) Visualizations pane > ellipsis (...) > Get more visuals > search > Add. For your org's list: same menu > My organization tab (both from Learn). Import from file: Visualizations pane > ellipsis > Import a visual from a file (from memory, unverified).
**Alternative:** Use built-in visuals or build a matrix with conditional formatting.
**Version / licensing note:** Verified on the Learn page above: visuals from AppSource may update automatically and may send data outside your tenant's boundary; licensed visuals are not supported in Report Server, government clouds, PaaS embed (app owns data) and Publish to web.
**Edge cases:** Admin may block custom visuals. Some custom visuals do not support export.
**Likely follow-ups:** 1) *Is AppSource free?* Download is free; licence model set by each publisher. 2) *Any risk?* Yes, code could carry privacy risk.
**Common mistakes:** Installing random .pbiviz files with confidential HR data; assuming all custom visuals work in the Service and Report Server alike.

### Q27 ⭐⭐ 🟢 How do you refresh the data in Power BI Desktop after the source Excel file has changed?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know Import mode is a snapshot and Refresh pulls new data?
**Say this in the interview:** "Home, Refresh. Because Import mode keeps a copy, the report does not change until I refresh. Desktop re-reads the file, picks up new rows and any column changes. After publishing, I set a scheduled refresh in the Service."
**Explain simply:**
- Three equivalent actions in Desktop: Home ribbon > Refresh; Home > Transform data > Close & Apply; right-click a table in the Data pane > Refresh data (Microsoft Learn: Data refresh in Power BI).
- Refresh in Desktop does schema sync then data refresh together.
- Service refresh is separate and needs the source reachable, through a gateway for local files (Learn: Data refresh in Power BI; On-premises data gateways in Power BI).
**Example:** `Headcount.xlsx` had 8 employees; HR adds Zoya in the Excel file. The report still shows 8 until Refresh, then shows 9.
**Sample data:** Employees (Q20 table, 8 rows) plus a new row: 109, Zoya, HR, Active, 38000.
**DAX / Steps:** (not run here) Save and close the Excel file first, then Desktop > Home > Refresh. No DAX needed; the measure `Headcount = COUNTROWS ( Employees )` updates automatically.
**Alternative:** Put the file in OneDrive or SharePoint so the Service syncs it about hourly (Learn: OneDrive refresh); or use a folder connector.
**Result:** Reproduced with pandas: before refresh 8, after refresh 9. Not a Power BI result.
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"EmpID":range(101,109)})        # the 8 rows already loaded
new_row = pd.DataFrame({"EmpID":[109]})              # Zoya, added in Excel
snap = emp.copy(); new = pd.concat([emp, new_row])
print(len(snap), "->", len(new))
```
Output (run with pandas 3.0.5): `8 -> 9` (the report keeps showing the snapshot of 8 until you click Refresh, then shows 9).
**Version / licensing note:** Verified on Learn: shared-capacity models get up to 8 scheduled refreshes per day; Premium, PPU and Fabric capacity up to 48 (Data refresh in Power BI). Refresh shows only changes saved in the file.
**Edge cases:** If a column is renamed or removed in Excel, visuals and measures that use it break; fix in Power Query. Service refresh fails after a schema change until you refresh in Desktop and republish.
**Likely follow-ups:** 1) *Why does the Service not update?* Needs schedule and gateway or cloud file. 2) *Refresh only visuals?* A Refresh visuals command exists on a ribbon (tab name from memory, unverified); it does not re-import data.
**Common mistakes:** Forgetting to save the Excel file; thinking opening the .pbix refreshes it.

### Q28 ⭐⭐ 🟢 How do you type a small list, such as departments and cost centres, straight into Power BI Desktop without an Excel file?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know Enter data and when a hand-typed lookup is appropriate?
**Say this in the interview:** "Home, Enter data. A small grid opens, I type or paste the list, name the table, and click Load. It becomes a normal table in the model. Changes need to be made in Desktop and the report republished, so I use it only for small, stable lists."
**Explain simply:**
- **Lookup table:** a short list (department and cost centre) joined to your main data.
- Enter data creates a new table in the Data pane; the first row can be promoted to headers (Microsoft Learn: Enter data directly into Power BI Desktop).
- Edit opens Power Query before loading.
- Updates cannot be made directly in the Service.
**Example:** A four-row table mapping Dept to CostCentre that you relate to the Employees table.
**Sample data:**

Table: Departments (typed)

| Dept | CostCentre |
|---|---|
| Sales | CC100 |
| HR | CC200 |
| IT | CC300 |
| Finance | CC400 |

**DAX / Steps:** (not run here)
Steps: Home > Enter data > type headers and rows > name the table Departments > Load (Learn).
DAX alternative as a calculated table (Modeling > New table), using the DATATABLE syntax on Learn:
```dax
Departments =
DATATABLE (
    "Dept", STRING,
    "CostCentre", STRING,
    { { "Sales", "CC100" }, { "HR", "CC200" }, { "IT", "CC300" }, { "Finance", "CC400" } }
)
```
**Alternative:** The DATATABLE calculated table above (a table made by a formula, not a measure), or keep the list in a SharePoint list or Excel so non-technical people can edit it.
**Result:** Reproduced with pandas: a 4-row, 2-column table as shown. Not from Power BI.
**Pandas check:**
```python
import pandas as pd
dep = pd.DataFrame({"Dept":["Sales","HR","IT","Finance"],"CostCentre":["CC100","CC200","CC300","CC400"]})
print(dep)
```
Output: the same 4 rows, index 0 to 3.
**Version / licensing note:** Verified on Learn (Enter data directly into Power BI Desktop; DATATABLE function). DATATABLE is unsupported in DirectQuery calculated columns or RLS, per Learn.
**Edge cases:** Typos in typed values break relationships; Finance has no employees so it shows blank in a headcount visual (COUNTROWS returns BLANK for no rows, per Learn).
**Likely follow-ups:** 1) *When not to use?* Large or changing lists. 2) *Can the Service edit it?* No.
**Common mistakes:** Leaving the default name "Table"; typing hundreds of rows; forgetting to relate it.

### Q29 ⭐⭐ 🟢 In the Data pane, how do you tell apart a normal column, a measure, a calculated column and a hierarchy by their icons?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you read the Data pane and explain stored vs calculated-on-the-fly?
**Say this in the interview:** "A measure has a calculator icon and calculates on the fly depending on the visual. A calculated column has its own column icon and is stored for every row. A normal column comes from the source, numeric ones show a sigma. A hierarchy has an arrow that expands to the levels."
**Explain simply:**
- **Normal column:** loaded from the source. Numeric fields can be summed or averaged.
- **Calculated column:** a new column you create with DAX; values stored per row, computed at refresh.
- **Measure:** has its own hard-coded formula; values are not stored in a column but calculated depending on location in a visual. Learn says report viewers cannot change the calculation (Microsoft Learn: Use the Field list in Power BI Desktop).
- **Hierarchy:** select the arrow to see the fields inside it.
- Icon glyphs are in images on Learn; the page text only describes them. Exact shapes change between versions, so click the field and read the ribbon (Measure tools vs Column tools).
**Example:** `SalaryBand` is a calculated column (each employee labelled High or Standard); `Total Salary` is a measure that changes by department.
**Sample data:** Employees (Q20 table).
**DAX / Steps:** (not run here)
```dax
SalaryBand = IF ( Employees[Salary] >= 50000, "High", "Standard" )   -- calculated column
Total Salary = SUM ( Employees[Salary] )                              -- measure
```
**Alternative:** High payroll as a measure:
```dax
High Salary Total =
CALCULATE ( SUM ( Employees[Salary] ), Employees[SalaryBand] = "High" )
```
**Result:** Reproduced with pandas: SalaryBand High for Ravi, Karan, Imran, Sneha. Total Salary all = 397000; by Dept HR 95000, IT 165000, Sales 137000; High Salary Total = 229000.
**Pandas check:**
```python
import pandas as pd
emp = pd.DataFrame({"Name":["Asha","Ravi","Meena","Karan","Divya","Imran","Sneha","Tarun"],
  "Dept":["Sales","Sales","HR","HR","IT","IT","IT","Sales"],
  "Salary":[40000,52000,35000,60000,48000,55000,62000,45000]})
emp["SalaryBand"] = emp.Salary.apply(lambda x: "High" if x >= 50000 else "Standard")
print(emp.Salary.sum()); print(emp.groupby("Dept").Salary.sum())
print(emp[emp.SalaryBand=="High"].Salary.sum())
```
Output (run with pandas 3.0.5): `397000`; HR 95000, IT 165000, Sales 137000; `229000`.
**Version / licensing note:** IF, SUM and CALCULATE syntax verified on Microsoft Learn. Field list wording verified on Learn. Icon shapes (calculator for a measure, sigma for a summable column, a column-with-fx style icon for a calculated column) are from memory, unverified; click the field and read the ribbon.
**Edge cases:** A numeric column with a sigma sum can be turned off (Q14). Hidden fields do not show. A measure inside a table shows the table's icon context but the calculator on the field.
**Likely follow-ups:** 1) *Column or measure for a ratio?* Measure; ratios do not add up per row. 2) *Cost?* Calculated columns use model memory.
**Common mistakes:** Using a calculated column for percentages; treating a measure like a column in a slicer.

### Q30 ⭐⭐ 🟡 You shared a report with a colleague who has a Free licence and they cannot open it. Why, and what are your options?
**Asked at:** commonly asked (no company-specific report found); gap-fill scenario for HR reporting.
**What the interviewer is checking:** Do you understand how Free, Pro, PPU and capacity decide who can view shared content?
**Say this in the interview:** "A Free user can only see content they create themselves, unless the report lives in a Premium or Fabric F64-or-higher capacity workspace. Otherwise both the sharer and the viewer need Pro. So I either move the workspace to capacity, get the colleague a Pro licence, or deliver a different format."
**Explain simply:**
- **Free per-user licence:** can build for yourself, but cannot use sharing or collaboration or publish to others' workspaces.
- **Pro:** needed to share and view others' content in shared capacity. **PPU:** viewers also need PPU in a PPU workspace.
- **Premium or Fabric F64+ capacity:** Pro or PPU users can share to free users when the workspace is on that capacity (Microsoft Learn: Power BI service features by license type).
- Options in order: (1) ask admin to assign Pro; (2) move content to a capacity workspace; (3) send an export, such as PDF, or an Excel from export-data (Q25) if policy allows.
**Example:** The CHRO has a Free licence. Moving the "HR Dashboard" workspace to a Fabric F64 capacity lets her view it without buying anything per user.
**DAX / Steps:** (not run here) Service > workspace Settings > License info > pick capacity (from memory, unverified); then Share. Ask admin to assign Pro in the Microsoft 365 admin centre (from memory).
**Alternative:** Publish an app from a capacity workspace; or scheduled email subscription needs Pro (Learn table lists "subscribe to dashboards" under Pro).
**Version / licensing note:** Verified on Learn page above (updated 2026-08-24). Prices not quoted; they change and vary by region. In the table the free licence is labelled "Fabric (free)".
**Edge cases:** Viewer in another tenant (guest) may need extra setup (from memory). RLS still applies.
**Likely follow-ups:** 1) *Does Desktop need a licence?* No, free (Q19). 2) *Can free users edit?* Not others' content.
**Common mistakes:** Assuming "Share" always works; sharing the .pbix by email, which exposes the whole model and data.

### Q31 ⭐⭐ 🟡 Can you run Power BI Desktop on a Mac, and what do you do if your work laptop is a Mac?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know Desktop is Windows-only and know the realistic workarounds?
**Say this in the interview:** "No, Power BI Desktop is a Windows application. On a Mac I can use the Power BI Service in the browser for viewing and light editing, or run Windows in a virtual machine or a cloud desktop for the full Desktop."
**Explain simply:**
- Microsoft's pages call Desktop a "Windows app" and list Windows 10 or Windows Server 2016 or later as minimum (Microsoft Learn: What is Power BI?; Download Power BI Desktop). They do not list macOS.
- **Browser:** app.powerbi.com on Mac works for viewing, creating and editing basic reports (Q24).
- **Virtual desktop:** Learn says Desktop is fully supported on Azure Virtual Desktop and Windows 365; running it as a published app such as Citrix is not supported.
- Other options (Parallels, Boot Camp, remote Windows PC): from memory, unverified as Microsoft-supported.
**Example:** An HR analyst on a MacBook gets a Windows 365 Cloud PC from IT and builds .pbix files there.
**DAX / Steps:** (not run here) Browser: app.powerbi.com > New > Semantic model. VM: install Windows 365 or Azure Virtual Desktop, then install Desktop from the Microsoft Store.
**Alternative:** Ask IT for a Windows laptop; or use a shared Windows jump box.
**Version / licensing note:** Windows-only and system requirements verified on the two Learn pages. A statement "no Mac support" is inferred from those pages plus community posts; not stated in so many words. Apple-silicon VM support: from memory, unverified.
**Edge cases:** Service editing does not equal Desktop features (Q32). Display scaling above 100 percent can hide dialogs on Windows, per Learn.
**Likely follow-ups:** 1) *Mobile app on iPad?* Viewing only (Q17). 2) *Is Excel on Mac enough?* Has Power Query but not the full Power BI model.
**Common mistakes:** Searching for a Mac installer; installing unofficial wrappers.

### Q32 ⭐⭐ 🟡 What can you do in the Power BI Service that you cannot do in Desktop, and the other way round?
**Asked at:** commonly asked (no company-specific report found); the creation-vs-consumption split appears in prep lists (Chandoo, Spreadsheeto).
**What the interviewer is checking:** Do you know the roles of the two tools?
**Say this in the interview:** "Desktop is for building: data cleaning, modelling, DAX and report design. The Service is for sharing and running: workspaces, apps, dashboards, scheduled refresh, subscriptions, alerts and security administration."
**Explain simply:**
- **Service only:** workspaces, apps, dashboards and tiles, scheduled refresh, email subscriptions, alerts, Q&A, embedding, usage metrics, sensitivity labels and audit logs (Microsoft Learn: What is Power BI?).
- **Desktop only:** the full Get data connector range (the Service connects to many sources too, so treat this as approximate), Power Query Editor, DAX models, calculated columns, relationships, performance analyzer, external tools, composite models (same page).
- Overlap: both connect to data and build visuals; the Service can also edit some models in the browser (Learn: DirectQuery in Power BI).
- Typical flow: build in Desktop > Publish > share from the Service.
**Example:** Analyst builds the attrition report in Desktop; the HR manager gets it in an app with daily refresh at 7 am.
**DAX / Steps:** (not run here) Desktop > Home > Publish > choose workspace. Service > Workspace > Semantic model > Schedule refresh.
**Alternative:** Build entirely in the Service for simple Excel-based reports (Q24).
**Version / licensing note:** Verified on the Learn overview (updated 2026-04-28). Which advanced modelling features have reached the web editor changes often; treat "Desktop only" as current at time of writing.
**Edge cases:** Row-level security roles are defined in the model; assigning people happens in the Service (from memory, unverified).
**Likely follow-ups:** 1) *Where do dashboards come from?* Service only (Q20). 2) *Where to schedule refresh?* Service.
**Common mistakes:** Saying "Service is only for viewing"; trying to create dashboards in Desktop.

### Q33 ⭐⭐ 🟡 What is a live connection in Power BI, and how does it differ from DirectQuery?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you separate "reuse a model" from "query a source live"?
**Say this in the interview:** "With a live connection my report connects to an already published semantic model or Analysis Services, so I only build visuals; the model and measures belong to someone else. With DirectQuery I connect to a data source, I own the model, and Power BI sends queries to the source each time."
**Explain simply:**
- **Live connection:** connects to an existing semantic model; no Power Query definition; full external field list appears; some modelling, such as calculated tables, is unavailable (Microsoft Learn: DirectQuery in Power BI).
- Identity of the viewer is passed to the upstream model, so its security applies.
- **DirectQuery:** no data imported; each visual triggers queries on the source; you can transform and model (with limits).
- Both avoid storing data in your report.
**Example:** A central HR team publishes a "HR Core" semantic model with a governed Headcount and Attrition measure. Five analysts live-connect to it and build their own reports with the same numbers.
**DAX / Steps:** (not run here) Live: Home > Get data > Power BI semantic models > select > Connect. DirectQuery: Get data > SQL Server database > choose DirectQuery (Learn: SQL Server connector).
**Alternative:** Composite model: DirectQuery over a published semantic model with local additions (from memory, unverified).
**Version / licensing note:** Verified on Learn page above (updated 2026-09-16). Authoring permission on the semantic model may be required (build permission), from memory.
**Edge cases:** You cannot add a relationship to your own table in a pure live connection; need composite. Changes to the source model show in all dependent reports.
**Likely follow-ups:** 1) *Why use it?* Single source of truth. 2) *Speed?* Depends on the upstream model.
**Common mistakes:** Treating them as the same; trying to add calculated columns in a live connection.

### Q34 ⭐⭐ 🟡 What is Microsoft Fabric, and how does it relate to Power BI?
**Asked at:** Microsoft Hyderabad (Jan 2024) mention of Power BI and Fabric in one candidate profile in `research/interview_processes.md` (single anecdote, unverified at question level); otherwise commonly asked.
**What the interviewer is checking:** Do you know Fabric is the bigger platform and Power BI is one of its workloads?
**Say this in the interview:** "Fabric is Microsoft's all-in-one analytics platform: data engineering, warehousing, real-time and Power BI on shared OneLake storage. Power BI is its reporting workload. Existing Power BI content and workspaces stay the same; Fabric adds more capabilities."
**Explain simply:**
- Fabric covers ingestion, transformation, real-time, analytics and reporting on one SaaS platform (Microsoft Learn: What is Microsoft Fabric).
- **OneLake:** the single logical data lake for all workloads.
- Power BI is a workload inside Fabric and its licensing is integrated; no migration needed (Microsoft Learn: What is Power BI?).
- **Direct Lake:** query OneLake data without import or traditional refresh.
- Capacity (F SKUs) now powers Copilot and sharing to free users at F64 or higher (Learn: Power BI service basics).
**Example:** HR data lands in a Fabric lakehouse; Power BI reads it in Direct Lake mode, so the dashboard updates without a nightly refresh.
**DAX / Steps:** (not run here) Service > New workspace > assign Fabric capacity > create lakehouse; in Desktop > Get data > OneLake catalog.
**Alternative:** Continue using Power BI alone with Import mode; Fabric is optional.
**Version / licensing note:** Verified on the Learn pages named above. Fabric IQ is labelled preview on the Fabric overview. Prices not quoted.
**Edge cases:** Fabric adds learning scope; a Free user's capabilities are unchanged unless content is in capacity.
**Likely follow-ups:** 1) *Do I need Fabric for Power BI?* No. 2) *Is Synapse replaced?* From memory, unverified.
**Common mistakes:** Saying Fabric replaces Power BI; mixing up Fabric and Azure.

### Q35 ⭐⭐ 🟡 What is Power BI Report Server, and how is it different from the Power BI Service?
**Asked at:** commonly asked (no company-specific report found); Report Server appears in component answers on prep sites (Keka, WSCubeTech).
**What the interviewer is checking:** Do you know the on-premises option exists and what it lacks?
**Say this in the interview:** "Report Server is an on-premises server where you host Power BI reports, paginated reports and Excel files inside your own network. The Service is Microsoft's cloud. Report Server needs a separate Desktop build and does not get all cloud-only features, so organisations choose it for data-residency or security reasons."
**Explain simply:**
- On-premises web portal for Power BI (.pbix), paginated (.rdl) and mobile reports and KPIs (Microsoft Learn: What Is Power BI Report Server?).
- Features are a superset of SQL Server Reporting Services (SSRS).
- Authors use the Report Server-optimized Power BI Desktop, a separate install (Learn: Download Power BI Desktop).
- Licensing: core-based; available through Fabric F64+ reserved instances and SQL Server licensing; a Pro licence is needed to publish Power BI reports there but not to view.
- Cloud-only items such as dashboards, apps, Copilot and Fabric workloads: from memory, unverified for this page; see the Learn comparison page.
**Example:** A bank's HR keeps payroll reports on its own server and cannot use the cloud.
**DAX / Steps:** (not run here) Install Report Server version of Desktop > Save report to Report Server (File > Save as > Power BI Report Server) (from memory, unverified).
**Alternative:** Power BI Service with a gateway to on-premises sources.
**Version / licensing note:** Verified on the Learn page named above (updated 2025-11-18). Learn says Report Server is included with Premium P SKUs, not EM SKUs or F SKUs below F64 reserved instance.
**Edge cases:** Release cadence differs from the monthly cloud Desktop; Report Server reports may need older Desktop.
**Likely follow-ups:** 1) *Cloud vs on-prem refresh?* Report Server schedules on its own. 2) *Same as SSRS?* No: includes pbix.
**Common mistakes:** Using the standard Desktop to publish to Report Server; calling it "Service installed locally".

### Q36 ⭐⭐ 🟡 What credential types does Power BI ask for when you connect to a source (Windows, Database, Organizational account, Anonymous), and where do you change them?
**Asked at:** commonly asked (no company-specific report found); gap-fill from standard practice.
**What the interviewer is checking:** Do you know the four credential types and where to edit saved ones?
**Say this in the interview:** "Windows uses my Windows login, Database uses a username and password stored in the database, Organizational account is single sign-on through Microsoft Entra (Microsoft's sign-in system, formerly Azure AD), and Anonymous is for public sources. I edit saved credentials in Data source settings in Desktop, and in the semantic model settings (formerly dataset) or gateway connection in the Service."
**Explain simply:**
- **SQL Server connector** supports Database/Basic, Windows, Organizational account and service principal (Microsoft Learn: Power Query SQL Server connector).
- **Excel** online-hosted file: Anonymous, Basic or Organizational account (Learn: Power Query Excel connector).
- **Gateway connections** offer Basic, Windows or OAuth2 (Learn: Add or remove a gateway data source).
- On the first connection you also choose the level to which the setting applies (such as the server or database).
- Desktop: File > Options and settings > Data source settings (Learn: Data sources in Power BI Desktop).
**Example:** The Employees SQL database uses Windows login in the office, but the refresh in the Service uses a service account through a gateway.
**DAX / Steps:** (not run here) Desktop: File > Options and settings > Data source settings > select source > Edit Permissions > Edit credentials (Edit Permissions, Clear Permissions: from third-party guides, unverified on Learn). Service: Settings > Manage connections and gateways, or dataset Settings > Data source credentials (from memory).
**Alternative:** Clear permissions and reconnect so Power BI asks again.
**Version / licensing note:** Verified: authentication lists on the Learn pages above. Entra sign-in works only if the SQL server supports it. Exact button names in Data source settings: unverified.
**Edge cases:** In the Service, Entra ID appears as OAuth2. Expired passwords break scheduled refresh. Privacy levels are separate from credentials.
**Likely follow-ups:** 1) *Why does refresh fail after a password change?* Update the stored credentials. 2) *Privacy levels?* From memory, set separately.
**Common mistakes:** Using personal credentials for a shared report; forgetting to update gateway credentials.

### Q37 ⭐⭐ 🟡 Your report shows "We couldn't connect to the data source" after the Excel file was moved to another folder. How do you fix it?
**Asked at:** commonly asked (no company-specific report found); gap-fill scenario.
**What the interviewer is checking:** Do you know to point the Source step to the new path, not rebuild the report?
**Say this in the interview:** "The query still points to the old file path. I open Transform data, go to Data source settings and Change Source to the new path, or edit the Source step in Power Query, then refresh. To avoid it again I use a path parameter or keep the file in SharePoint or OneDrive."
**Explain simply:**
- Power Query stores the file path in the Source step; a moved file breaks it.
- Fix does not require rebuilding visuals or measures.
- After publishing, a local path also needs a gateway for scheduled refresh (Microsoft Learn: Data refresh in Power BI; On-premises data gateways in Power BI).
- Use the fully qualified path for network shares, since short server names can cause refresh failures after publishing (Learn: Power Query Excel connector).
**Example:** `Headcount.xlsx` moved from `D:\HR\` to `D:\HR\Archive\`. After the fix, the report loads again.
**DAX / Steps:** (not run here)
1) Home > Transform data > Data source settings > select the file > Change Source (button name from third-party guides, unverified) > Browse > OK > Close & Apply.
2) Or Power Query Editor > Applied Steps > Source (gear icon) > edit path.
3) Or Advanced Editor:
```m
let
    Source = Excel.Workbook(File.Contents("D:\HR\Archive\Headcount.xlsx"), [DelayTypes = true]),
    Sheet = Source{[Item="Jan", Kind="Sheet"]}[Data],
    Promoted = Table.PromoteHeaders(Sheet)
in
    Promoted
```
(Excel.Workbook with an options record and Table.PromoteHeaders appear on the Excel connector Learn page.)
**Alternative:** Create a parameter FilePath (Home > Manage parameters) and use `File.Contents(FilePath)` (from memory), so one change fixes all queries.
**Result:** Not run here. No pandas reproduction, since this is a connection fix, not a calculation.
**Version / licensing note:** Data source settings menu path verified on Learn (Data sources in Power BI Desktop). Change Source and Edit Permissions button labels, and parameter steps: from memory or third-party, unverified.
**Edge cases:** The exact error text for a moved file is usually a "file not found" style message, so the quoted wording in the question is approximate (from memory, unverified). Sheet renamed gives a different error. File open in Excel can affect legacy .xls reads (Learn). A published model may need credentials re-entered.
**Likely follow-ups:** 1) *Refresh fails in the Service only?* Gateway or credentials. 2) *Many files?* Folder connector.
**Common mistakes:** Deleting the query and rebuilding everything; moving files without telling report owners.

### Q38 ⭐⭐ 🟡 What happens to your data and your report when you publish a .pbix file from Desktop to the Service?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know that publishing copies the model and report to the cloud, and that the .pbix on your laptop is not kept in sync?
**Say this in the interview:** "Publishing uploads two things to the chosen workspace: a semantic model (the data model, including imported data) and the report. Edits I later make in the Service are not saved back to my .pbix, and republishing replaces the model in the Service."
**Explain simply:**
- A **.pbix** is Power BI Desktop's single file: report pages, data model and (for Import mode) the loaded data. A **workspace** is a shared folder in the Service; a **semantic model** is the new name for "dataset".
- On publish you pick a workspace; you get a semantic model with the same name plus the report (Microsoft Learn: Publish from Power BI Desktop).
- Import-mode data is uploaded. DirectQuery tables are only links; if the source is on-premises you may need a **gateway** (a small program that lets the cloud reach in-house data).
- Republishing replaces the model; Desktop warns how many reports/dashboards may be affected. Renaming or deleting a column or measure can break visuals already built in the Service.
- If a refresh schedule exists, republishing starts a refresh, and new data sources need credentials entered before the next scheduled refresh.
**Example:** You publish "HR_Attrition.pbix" to the workspace "HR Analytics". Next day a colleague adds a chart in the Service. If you then fix a measure in Desktop and republish, the Service version of the report is overwritten by your file, so her chart is lost unless it also exists in your .pbix.
**DAX / Steps (not run here):**
1. Desktop > Home tab > Share group > Publish (or File > Publish > Publish to Power BI).
2. Sign in if asked, pick the workspace, select Select.
3. Open the link shown on success.
**Alternative:** Upload the .pbix in the Service (workspace > New/Upload > Upload a file); Microsoft says publishing has the same effect as using Get Data to upload a Desktop file.
**Version / licensing note:** Behaviour above is from Microsoft Learn: Publish from Power BI Desktop (ms.date 2025-12-01). Which workspaces you may publish to depends on licence; see Q53. Publishing into workspace folders is described there as a preview feature.
**Edge cases:** Storage-mode conversion on republish is not supported (an Import report cannot be overwritten by a DirectQuery or live-connection one). Two models in the workspace with the same name as the file can make publishing fail. Rarely, a flaky network produces duplicate reports; delete the extras. A sensitivity label on the file is inherited by the published model and report.
**Likely follow-ups:**
1. *Can I edit the report in the Service?* Yes, but changes do not flow back to the .pbix.
2. *Who can see it after publishing?* Only people given workspace access or an app/share link.
**Common mistakes:** Thinking the Service version auto-syncs with the file; publishing to the wrong workspace; renaming columns and then wondering why live visuals broke.

### Q39 ⭐⭐ 🟡 Can two analysts work on the same .pbix file at the same time, and how do teams manage this?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know a .pbix is a single binary file with no merge capability, and what teams do instead?
**Say this in the interview:** "Not safely. A .pbix is one file, so the last person to save wins. Teams split the work: one shared semantic model owned by one person, separate report files built on it, or they save as a Power BI project and use Git."
**Explain simply:**
- A .pbix cannot be merged like a text file, so two people editing copies means one set of changes is lost. (Stated from general knowledge; I did not find a Microsoft page that says this in one sentence, so treat as from memory, unverified.)
- **Option 1, split model and reports:** one analyst owns the semantic model; others create thin reports connected to it (see Q54).
- **Option 2, Power BI Project (.pbip):** saves the report and model as plain text files in folders, "source control ready" for Git (Microsoft Learn: Power BI Desktop projects (PBIP)). Git lets people work on branches and compare changes (Microsoft Learn: Git integration with Power BI Desktop projects).
- **Option 3, process:** keep the .pbix on OneDrive/SharePoint with a rule: one editor at a time; use the Service for light edits.
**Example:** Two analysts both edit "Headcount.pbix". Priya adds an attrition page, Karan fixes a measure. Both save to the shared folder; Karan saves last and Priya's page vanishes. With a .pbip in Git, each commits on a branch and the changes are reviewed and combined.
**DAX / Steps (not run here):** Desktop > File > Save as > choose "Power BI Project (*.pbip)" as the file type (Microsoft page shows Save as type); then open the folder in VS Code and initialise a repository.
**Alternative:** Fabric Git integration or deployment pipelines for workspace-level version control (named on the PBIP page as deployment mechanisms; licence details not verified).
**Version / licensing note:** PBIP saving and Git details are from the two Learn pages above. The PBIP page lists limits: path length 260 characters on Windows, cannot save directly to OneDrive/SharePoint, sensitivity labels unsupported with projects. I did not verify GA/preview status of PBIP beyond the page not calling it preview.
**Edge cases:** Editing project files by hand can stop Desktop from opening the project. Merge conflicts in text files still need a human to resolve.
**Likely follow-ups:**
1. *Is there co-authoring like Google Docs?* Not for a .pbix in Desktop (from memory, unverified).
2. *Why split model and reports?* One set of numbers, fewer file clashes.
**Common mistakes:** Emailing .pbix versions ("final_v3_REAL.pbix"); two people publishing the same-named file to one workspace and overwriting each other.

### Q40 ⭐⭐ 🟡 You change a step in Power Query and a yellow banner appears over the report. What does it mean, and what happens if you ignore it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand that Power Query changes are staged and do not reach the model or visuals until applied?
**Say this in the interview:** "The banner says there are pending query changes that have not been applied to the model. Until I click Apply changes, visuals still show the old data and shape. If I ignore it, the report keeps working on the old model, and anything I build on a new column will not exist yet."
**Explain simply:**
- **Power Query Editor** is the window where you clean data (rename, filter, change types). Every action is recorded as a step.
- Edits are staged. The model and visuals only update when you click **Close & Apply** or **Apply changes** on the banner; applying reloads the affected tables.
- Ignoring it is not dangerous, but you will see stale numbers, and a refresh or save may prompt you again.
- Community answers also mention the banner persisting after apply, often due to privacy-level or credential settings, or a Desktop bug fixed by updating (forum reports only).
**Example:** You filter out "Intern" from the Employees table in Power Query: headcount should drop from 520 to 505. Until you Apply, the card still shows 520.
**DAX / Steps (not run here):** Click Apply changes in the yellow bar, or Home > Transform data > Close & Apply. To drop staged edits: Discard changes on the bar.
**Alternative:** Home > Refresh also asks to apply pending changes.
**Version / licensing note:** From memory, unverified. The Microsoft Learn Power Query overview URL I tried returned 404 and my search found no Learn page for this banner (only Fabric Community threads).
**Edge cases:** Large tables take time to reload; applying with a broken step shows an error and keeps the banner.
**Likely follow-ups:**
1. *What is the difference between Apply changes and Refresh?* Apply loads edited queries; Refresh re-reads the sources.
2. *Does it affect the Service?* Only after you publish.
**Common mistakes:** Building visuals on a column that exists only in unapplied steps; closing without applying and losing the edit.

### Q41 ⭐ 🟢 What are .pbit template files and .pbip project files, and when would you use them?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Awareness of reusable starting points and source-control-friendly saving.
**Say this in the interview:** "A .pbit is a template: report pages, model definition and queries but no data. A .pbip is the project format that saves the report and model as readable text folders, good for Git and team work."
**Explain simply:**
- **.pbit** contains report pages and visuals, the data model definition (relationships, measures) and all query definitions, but not the data, so it is smaller. Opening it prompts for parameter values and the data location (Microsoft Learn: Create and Use Report Templates in Power BI Desktop).
- Create it: File > Export > Power BI template. Open it: double-click or File > Import > Power BI template.
- Filter values (for example Company = Contoso) can still be saved inside a template's metadata.
- **.pbip** saves a `.Report` folder, a `.SemanticModel` folder and a pointer file. You can convert .pbix to .pbip and back via Save as (Microsoft Learn: Power BI Desktop projects (PBIP)).
**Example:** HR has one "Monthly HR pack.pbit" with the same pages for each region. Each regional analyst opens it, types their region parameter, and points it at their own data, so all five regions look identical.
**DAX / Steps (not run here):** File > Export > Power BI template > add description > OK > choose location. For project: File > Save as > Power BI Project.
**Alternative:** Copy a .pbix and replace its data source (works but carries data and is easier to get wrong).
**Version / licensing note:** From the two Learn pages above. PBIP is not supported in the Desktop version optimised for Power BI Report Server, and editing a .pbit with external tools is unsupported (Learn: External Tools in Power BI Desktop).
**Edge cases:** Template files can still hold filter values; do not assume they are free of business info.
**Likely follow-ups:**
1. *Is a .pbit refreshable on its own?* No data inside; you reload after entering parameters.
2. *Why PBIP over PBIX?* Diffable text, Git, CI/CD.
**Common mistakes:** Sending a .pbit to someone without access to the data source; confusing it with a theme (.json) file.

### Q42 ⭐ 🟢 How often is Power BI Desktop updated, and why does your version matter when sharing files?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Practical awareness that Desktop ships monthly and that older versions cannot open newer files.
**Say this in the interview:** "Desktop gets a new release every month. Older versions are not serviced and cannot open files saved in newer versions, so everyone on a team should stay on a recent build."
**Explain simply:**
- Microsoft Learn's What's new page is titled "August 2026 Power BI Update" and links to a "monthly updates archive", so releases are monthly.
- Per that page: previous releases are not serviced; previous versions cannot open files created or saved in newer releases; saving a newer-release report in an older version can lose information about new features; only English versions are archived.
- Same page: from October, Desktop versions from March 2026 or earlier cannot save and share files to OneDrive/SharePoint, so update to keep that working.
**Example:** Your teammate on the June build gets an error opening your file saved in the August build. Fix: update Desktop, not re-send the file.
**DAX / Steps (not run here):** Download the latest Desktop from Microsoft (Store or Download Center). Check build via Help > About.
**Alternative:** Pin the whole team to one version through IT's deployment tool (the Learn note says you can download an earlier version if your organisation needs one).
**Version / licensing note:** From Microsoft Learn: See What's New in the August 2026 Power BI Update. Desktop is a Windows app per Microsoft Learn: What is Power BI?
**Edge cases:** The Report Server edition of Desktop is a separate, slower release track (from memory, unverified).
**Likely follow-ups:**
1. *Is Desktop on Mac?* Learn describes it as a Windows app; Mac users use the browser Service.
2. *Where are new features listed?* The monthly update post and change log.
**Common mistakes:** Mixing versions in a team; assuming an old file opens everywhere.

### Q43 ⭐ 🟢 Who are the typical users of Power BI: creators, consumers and administrators?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Understanding roles in the Power BI ecosystem and which tools each uses.
**Say this in the interview:** "Creators build reports and models in Desktop and publish them; consumers open and explore them in the Service or mobile app; administrators manage licences, security and settings."
**Explain simply:**
- **Creators / designers:** build reports and dashboards, organise workspaces, publish apps, share (Microsoft Learn: Power BI service basics).
- **Consumers / business users:** view and explore reports, monitor dashboards, use apps.
- **Administrators:** set up the organisation and manage access and security via the admin portal (What is Power BI? lists "Administrator" as its own audience).
- Workspace roles (Admin, Member, Contributor, Viewer) control what people can do inside a workspace.
**Example:** In an HR team: an analyst builds the attrition report (creator), 40 HR business partners read it (consumers), the IT admin decides who may publish and turns features on or off.
**DAX / Steps (not run here):** none; this is a roles question.
**Alternative:** Mention developers as a fourth group who embed or extend Power BI (listed on the same overview page).
**Version / licensing note:** Roles from the two Learn pages above. Licensing differences are in Q53.
**Edge cases:** One person is often both creator and consumer; consumers with Build permission can create reports on shared models.
**Likely follow-ups:**
1. *Which licence does a creator need to share?* Pro or PPU (Q53).
2. *Who sees admin settings?* Only people with the Fabric/Power BI admin role.
**Common mistakes:** Treating "viewer" and "admin" as licence types (they are roles).

### Q44 ⭐ 🟡 What is Power BI Report Builder, and what are paginated reports?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know when a normal Power BI report is wrong and a pixel-perfect printable report is needed.
**Say this in the interview:** "Report Builder is a free standalone tool for authoring paginated reports, which are made for printing and sharing: a table prints every row across as many pages as needed, with exact layout. Think payslips or invoices."
**Explain simply:**
- **Paginated report:** fixed-layout report; shows all rows of a table even across pages (Microsoft Learn: What Are Paginated Reports in Power Bi?).
- A normal Power BI report prints only the rows visible on screen.
- Authored in **Power BI Report Builder** (free download), saved as .rdl, published to the Service; exports to Excel, Word, PowerPoint, PDF, CSV and more.
- It has no data model of its own; data sources and datasets are embedded in the report, and a semantic model can be a source.
**Example:** A payslip run for 1,200 employees: one page per employee with repeating header and footer, emailed as PDF. A dashboard cannot do that.
**DAX / Steps (not run here):** Install Report Builder > Insert > Table wizard > choose data source/semantic model > design > File > Publish > select workspace.
**Alternative:** Use the Export feature on a normal report if only the visible summary is needed.
**Version / licensing note:** Per the Learn page: Report Builder download is free; with a free licence you can publish only to My Workspace; Pro or PPU lets you publish to other workspaces (contributor role needed); you also need Build permission on the dataset. Memory limits vary by licence and are not stated on the page.
**Edge cases:** Not supported: pinning to dashboards, shared data sources/datasets, document maps in the Service. On-premises data needs a gateway.
**Likely follow-ups:**
1. *Report Builder vs SSRS Builder?* Different downloads; the Learn page points on-premises users to Microsoft Report Builder.
2. *Can it be scheduled?* Email subscriptions (daily/weekly/hourly) with PDF attached are supported.
**Common mistakes:** Building a printable invoice in a normal report; forgetting the gateway redirect for on-premises sources.

### Q45 ⭐ 🟡 What is a dataflow, and how does it differ from Power Query inside Desktop?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Understanding of reusable cloud data preparation versus per-file preparation.
**Say this in the interview:** "A dataflow is Power Query run in the Service so the cleaning logic is stored once and reused by many models. Power Query in Desktop lives inside one .pbix and is used only by that file."
**Explain simply:**
- Dataflow: reusable transformation logic that many semantic models and reports can share, stored in the Service, with refresh scheduled in the workspace (Microsoft Learn: Introduction to Dataflows and Self-service Data Prep (legacy)).
- Benefit: one clean "Employees" table instead of five copies of the same steps; analysts need not touch the source system.
- Desktop Power Query: steps are saved inside the .pbix and refreshed with that model.
- Learn labels Dataflow Gen1 as legacy: no new feature investment; Dataflow Gen2 (Fabric) is recommended for Premium/Fabric customers, while Pro/PPU customers can continue with Gen1.
**Example:** HR master data (joiners, leavers, grades) is cleaned once in a dataflow; attrition, headcount and hiring-funnel reports all load from it.
**DAX / Steps (not run here):** Service > workspace > New > Dataflow (or Dataflow Gen2) > add source > transform in Power Query Online > Save and refresh. In Desktop: Home > Get data > Dataflows.
**Alternative:** A shared semantic model (Q54) when the reuse need is measures and relationships, not just clean tables.
**Version / licensing note:** From the Learn page above (ms.date 2025-10-01). Exact licence needs for Gen2 not verified here.
**Edge cases:** A change to a dataflow affects every model using it. Not all dataflow features are available in some US Government DoD environments per the page.
**Likely follow-ups:**
1. *Gen1 vs Gen2?* Gen1 is legacy; Gen2 is the recommended path in Fabric.
2. *Where is data stored?* In the Service's storage, or your own Azure Data Lake Gen2 if configured.
**Common mistakes:** Calling a dataflow a replacement for the data model; building new work on Gen1 without checking.

### Q46 ⭐ 🟡 What is Analyze in Excel in Power BI?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know how Excel users connect to certified Power BI numbers.
**Say this in the interview:** "Analyze in Excel makes an Excel workbook live-connected to a Power BI semantic model so people can build PivotTables on the same governed measures, and refresh them."
**Explain simply:**
- It creates a workbook with the entire semantic model available for PivotTables and PivotCharts (Microsoft Learn: Create Excel Workbooks with Refreshable Power BI Data).
- You need Build permission or at least Contributor role, a Fabric Free, Pro or PPU licence, and the tenant admin must enable the live-connection setting.
- Row-level security and object-level security are applied.
- Free-licence users can use it only with models in My workspace or on Premium/Fabric F64+ capacity.
**Example:** The finance analyst wants an Excel PivotTable of headcount by grade using the HR team's official "Headcount" measure. She clicks Analyze in Excel and gets the same number the report shows.
**DAX / Steps (not run here):** Service > open report > Export > Analyze in Excel (or workspace > More options "..." > Analyze in Excel). Open in Excel for the web or the desktop app, select Yes at the Query and Refresh Data prompt.
**Alternative:** Export data from a visual with live connection (.xlsx, 500,000 row maximum per the page), or the Excel add-in (Insert > PivotTable > From Power BI).
**Version / licensing note:** From the Learn page above (ms.date 2025-12-01). Mac users can only use Excel for the web. Only Import-mode models keep hierarchies. Data larger than 2 GB may error. Not available for external users, Report Server, or AAS/SSAS live connections.
**Edge cases:** Field parameters may not work as expected.
**Likely follow-ups:**
1. *Is the data copied into Excel?* No, it is a live connection; refresh pulls from the model.
2. *Is security preserved?* Yes, RLS/OLS apply.
**Common mistakes:** Copy-pasting values and losing the refresh; trying it without Build permission.

### Q47 ⭐ 🟡 What are external tools in Power BI Desktop, such as DAX Studio and Tabular Editor?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Awareness of the ecosystem used for performance tuning and advanced modelling.
**Say this in the interview:** "They are free third-party programs that connect to the model inside Desktop. DAX Studio is for writing and profiling DAX queries; Tabular Editor is for editing the model quickly in bulk; ALM Toolkit compares and deploys model changes."
**Explain simply:**
- Desktop runs a hidden Analysis Services engine; the External Tools ribbon passes its server name, port and model name so a tool connects automatically (Microsoft Learn: External Tools in Power BI Desktop).
- Featured: **DAX Studio** (DAX authoring, tracing, performance), **Tabular Editor** (hierarchical model editor), **ALM Toolkit** (schema compare), Metadata Translator.
- Tools can write to the model; Microsoft warns this may cause unexpected behaviour or rare inconsistencies.
- Microsoft does not support third-party tools except where the issue reproduces with Microsoft tools.
**Example:** A matrix takes 12 seconds. Copy its query with Performance Analyzer, run it in DAX Studio, and see which measure is slow.
**DAX / Steps (not run here):** Install the tool; if registered, Desktop > External Tools tab > click the tool. Custom tools register through a `.pbitool.json` file.
**Alternative:** Built-in Performance Analyzer and DAX query view inside Desktop for basic cases.
**Version / licensing note:** From the Learn page above (ms.date 2025-10-01). Not supported in the Report Server edition of Desktop; the ribbon can be disabled by group policy. Tool licences are the tools' own (not checked).
**Edge cases:** Editing a .pbit with external tools is unsupported; sending processing commands to a model in Desktop is unsupported.
**Likely follow-ups:**
1. *Is DAX Studio from Microsoft?* No, it is community open source.
2. *Do you need them as a fresher?* Rarely; knowing the names and use is a differentiator.
**Common mistakes:** Making risky edits without a backup; expecting Microsoft support for them.

### Q48 ⭐ 🟡 Where does Power BI store imported data, and what is the VertiPaq engine?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know Import mode copies data into a compressed in-memory model, which is why it is fast.
**Say this in the interview:** "Imported data is stored inside the semantic model: in the .pbix file on my laptop and in the Service after publishing. VertiPaq is the engine that stores it column by column in compressed form and answers queries quickly."
**Explain simply:**
- **VertiPaq storage engine:** Learn says Import models are loaded with data that is compressed and optimised and stored to disk by VertiPaq; about 10x compression in memory is possible, so about 10 GB source data may become about 1 GB (Microsoft Learn: Data reduction techniques for Import modeling). It depends on the data.
- Each column has its own data structure; numbers compress best (value encoding); text uses hash encoding.
- Few distinct values compress better than many unique values (for example Department compresses better than EmployeeID).
- Direct Lake and Import queries are processed by VertiPaq; DirectQuery sends queries to the source (Learn: Direct Lake overview).
**Example:** 1 million HR rows with a Department column of 3 distinct values: store a 3-entry dictionary plus small codes instead of a million repeated text strings.
**Sample data:** Table `Employees[Dept]`, 8 rows: Sales, Sales, Support, Sales, Tech, Support, Sales, Tech.
**DAX / Steps (not run here):** None. To see column sizes use an external tool such as DAX Studio (VertiPaq Analyzer view, from memory, unverified).
**Alternative:** DirectQuery keeps data at the source (slower queries, no copy); see Q55 for Direct Lake.
**Result:** reproduced with pandas (dictionary encoding means storing each distinct value once in a lookup and keeping only small codes per row): dictionary {0: Sales, 1: Support, 2: Tech}; stored codes [0, 0, 1, 0, 2, 1, 0, 2]. This is only a teaching sketch of dictionary encoding, not VertiPaq's real algorithm.
**Pandas check:**
```python
import pandas as pd
col = pd.Series(['Sales','Sales','Support','Sales','Tech','Support','Sales','Tech'])
codes, uniques = pd.factorize(col)
print('dictionary:', dict(enumerate(uniques.tolist())))
print('stored codes:', codes.tolist())
```
```
dictionary: {0: 'Sales', 1: 'Support', 2: 'Tech'}
stored codes: [0, 0, 1, 0, 2, 1, 0, 2]
```
**Version / licensing note:** Import size limits: see Q52. The Learn pages above carry dates 2024-12-30 (data reduction) and 2026-09-02 (Direct Lake).
**Edge cases:** High-cardinality columns (many unique values, such as IDs and timestamps) bloat the model. Calculated columns compress less well than Power Query columns, per the data-reduction page.
**Likely follow-ups:**
1. *Is data in memory only?* It is persisted to disk and loaded into memory for queries.
2. *How to shrink a model?* Remove unused columns/rows, summarise, use numeric types.
**Common mistakes:** Loading every column "just in case"; keeping datetime columns to the second.

### Q49 ⭐ 🟡 Which Power BI component would you use to give HR managers phone access to the monthly attrition numbers?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Matching the right component to the need: Desktop to build, Service to publish, Mobile app to view.
**Say this in the interview:** "I build the attrition report in Desktop, publish it to the Service, and managers view it in the Power BI mobile app on iOS or Android. I would also design a phone layout so it reads well on a small screen."
**Explain simply:**
- Desktop = create; Service = share; Mobile app = view (Microsoft Learn: What is Power BI?).
- Mobile apps exist for iOS and Android (iPhone, iPad, Android phone/tablet); the Windows app was retired on 31 Dec 2023 (Learn: What Are the Power BI Mobile Apps?).
- Reports can have a special mobile layout view; data alerts can notify when a number crosses a limit.
- Distribute with a workspace app so managers install one thing (Learn: Publish a workspace app). Viewer licences: Q53.
**Example:** Attrition for September 2026 is 6.0% overall (Sales 6.1%, Support 8.5%, Tech 4.9%). A manager opens the app on the phone and sees one card plus a department bar.
**Sample data:** Table `HR_Monthly` (one row per department per month).

| Month | Dept | OpeningHC | Leavers | ClosingHC |
|---|---|---|---|---|
| 2026-09 | Sales | 100 | 6 | 98 |
| 2026-09 | Support | 60 | 5 | 57 |
| 2026-09 | Tech | 140 | 7 | 145 |

**DAX / Steps (not run here):**
```dax
Attrition % =
DIVIDE (
    SUM ( HR_Monthly[Leavers] ),
    ( SUM ( HR_Monthly[OpeningHC] ) + SUM ( HR_Monthly[ClosingHC] ) ) / 2
)
```
Steps: Desktop > View tab > Mobile layout; drag a card and bar chart onto the phone canvas; Home > Publish. In the Service, create/update a workspace app and share its link. DIVIDE and SUM syntax checked on Microsoft Learn: DIVIDE function (DAX), SUM function (DAX). DIVIDE returns BLANK on division by zero.
**Alternative:** Email subscriptions with a report snapshot, or a data alert on a dashboard tile (alerts are listed for the mobile app on the Learn page).
**Result:** reproduced with pandas (leavers divided by average of opening and closing headcount): Sales 6.1%, Support 8.5%, Tech 4.9%, Total 6.0% (18 / 300).
**Pandas check:**
```python
import pandas as pd
hr = pd.DataFrame({"Dept":["Sales","Support","Tech"],"OpeningHC":[100,60,140],"Leavers":[6,5,7],"ClosingHC":[98,57,145]})
f = lambda d: d.Leavers.sum()/((d.OpeningHC.sum()+d.ClosingHC.sum())/2)
for n in hr.Dept: print(n, f"{f(hr[hr.Dept==n]):.1%}")
print("Total", f"{f(hr):.1%}")
```
```
Sales 6.1%
Support 8.5%
Tech 4.9%
Total 6.0%
```
**Version / licensing note:** App and mobile facts from the Learn pages cited; the mobile-layout menu path is from memory, unverified. Note the total is not the average of the three percentages.
**Edge cases:** Managers who should see only their team need row-level security (Q50). Phone access outside the company network may be restricted by IT (Intune can manage the app, per the mobile page).
**Likely follow-ups:**
1. *Do they need Desktop?* No.
2. *Can they edit on the phone?* They view and interact.
**Common mistakes:** Sending the .pbix file instead of publishing; no phone layout so visuals shrink; averaging department percentages for the total.

### Q50 ⭐ 🟡 Is it safe to load payroll data into Power BI, and what basic controls would you check first?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Data-protection mindset: access, row-level security, labelling, and who can export.
**Say this in the interview:** "It can be, if controls are in place. Before loading payroll I would confirm who may see what with row-level security, keep it in a restricted workspace, apply a sensitivity label, and check export and sharing settings with IT. I would also load only the columns needed."
**Explain simply:**
- **Row-level security (RLS):** DAX filters inside roles hide rows from users; it applies to people with the Viewer role, not to Admin, Member or Contributor (Microsoft Learn: Row-level security (RLS) with Power BI).
- **Workspace roles:** limit who is Contributor or above; they bypass RLS.
- **Sensitivity labels** (Microsoft Purview): tag content "Confidential"; the label and encryption follow exports to Excel, PowerPoint, PDF and .pbix, but in the Service a label does not itself change who can open the report (Learn: Sensitivity Labels in Power BI).
- RLS does not hide columns; for that use object-level security. Anyone with access to a report sees the entire underlying model unless RLS limits it.
- Data minimisation: drop bank account and PAN (India's tax ID number) columns that no one needs.
**Example:** Payroll table with managers' emails. Role "My Team" filters `ManagerEmail = USERPRINCIPALNAME()`. Asha sees her 2 staff (total salary 112,000); Ravi sees his 2 (84,000); an unmapped person sees nothing; an admin sees all 6 rows (381,000).
**Sample data:** Table `Payroll`.

| EmpID | Dept | Salary | ManagerEmail |
|---|---|---|---|
| 1 | Sales | 50000 | asha@co.com |
| 2 | Sales | 62000 | asha@co.com |
| 3 | Support | 41000 | ravi@co.com |
| 4 | Support | 43000 | ravi@co.com |
| 5 | Tech | 90000 | meena@co.com |
| 6 | Tech | 95000 | meena@co.com |

**DAX / Steps (not run here):** Role filter on `Payroll`:
```dax
[ManagerEmail] = USERPRINCIPALNAME()
```
Steps: Desktop > Modeling tab > Manage roles > New > pick Payroll > paste the filter (DAX editor) > Save. Publish. Service > workspace > semantic model > More options > Security > add members to the role > Test as role. USERPRINCIPALNAME() returns the user principal name at connection time (Learn: USERPRINCIPALNAME function (DAX)).
**Alternative:** Static roles (`[Dept] = "Sales"`) for small fixed groups; or keep salary out of the model and publish only aggregates.
**Result:** reproduced with pandas (not a DAX engine): asha@co.com sees 2 rows, 112,000; ravi@co.com 2 rows, 84,000; unmapped user 0 rows; no RLS (Admin/Contributor) 6 rows, 381,000.
**Pandas check:**
```python
import pandas as pd
pay = pd.DataFrame({"EmpID":[1,2,3,4,5,6],"Salary":[50000,62000,41000,43000,90000,95000],
 "ManagerEmail":["asha@co.com"]*2+["ravi@co.com"]*2+["meena@co.com"]*2})
for u in ["asha@co.com","ravi@co.com","unmapped@co.com"]:
    v = pay[pay.ManagerEmail==u]; print(u, len(v), v.Salary.sum())
print("no RLS", len(pay), pay.Salary.sum())
```
```
asha@co.com 2 112000
ravi@co.com 2 84000
unmapped@co.com 0 0
no RLS 6 381000
```
**Version / licensing note:** RLS and labels from the Learn pages cited. Sensitivity labels need Purview licensing and tenant enablement (page defers details; not verified). Microsoft 365 groups cannot be RLS members; Entra security and mail-enabled groups can.
**Edge cases:** Users in no role see no data. Users in several roles get the union. Service principals cannot be added to RLS roles. Exports to CSV are not label-protected. Payroll is also governed by company policy and local law; confirm with HR/IT/legal, which Microsoft docs cannot answer.
**Likely follow-ups:**
1. *Who bypasses RLS?* Workspace Admin, Member and Contributor.
2. *Can RLS hide a column?* No; use object-level security.
**Common mistakes:** Giving analysts Contributor on a payroll workspace and assuming RLS applies; testing only as yourself; sending the .pbix by email.

### Q51 ⭐ 🟡 What is Power BI Embedded, and who uses it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Awareness that Power BI content can live inside other apps, and the two embedding patterns.
**Say this in the interview:** "Embedded analytics puts Power BI reports inside a website or application. Software vendors use 'embed for your customers' so external users need no Power BI licence; companies use 'embed for your organization' for internal apps where users sign in with a licence."
**Explain simply:**
- Microsoft Learn: Power BI embedded analytics overview: embed reports, dashboards and tiles into web apps.
- **Embed for your customers (app owns data):** external users, your own authentication, app users need no licence; typically ISVs.
- **Embed for your organization (user owns data):** internal users sign in with Microsoft Entra ID, each needs a Power BI licence.
- **Secure embed** is the no-code option for a URL/iframe; viewers need the proper licence.
- Production use needs a purchased capacity (A, P/EM or Fabric F SKUs); the page says trial tokens are for development only. "Power BI Embedded" strictly means the Azure offer with A SKUs.
**Example:** An HR-software vendor shows each client company's own attrition dashboard inside its product; clients never see Power BI.
**DAX / Steps (not run here):** Service > report > File > Embed report > Secure embed (iframe) for the internal case; app-owns-data needs developer work with embed tokens.
**Alternative:** Publish to a workspace app or Teams/SharePoint embed (SharePoint enhancements appear on the August 2026 What's new page).
**Version / licensing note:** From Learn pages cited (ms.date 2025-12-15). Prices not quoted; they change.
**Edge cases:** R and Python visuals are not supported in embed-for-customers.
**Likely follow-ups:**
1. *Who pays?* The embedding organisation buys capacity.
2. *RLS in embedding?* Pass an effective identity in the embed token (Learn: Row-level security page).
**Common mistakes:** Mixing up "Power BI Embedded" (A SKU) with all embedding; putting Free users into an organisation-embed scenario.

### Q52 ⭐ 🟡 What is the size limit of a semantic model you can publish with a Pro licence?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Knowing the 1 GB default and how larger models are handled.
**Say this in the interview:** "A semantic model on shared (Pro) capacity is limited to 1 GB. Larger models need Premium or Fabric capacity with the large model storage format."
**Explain simply:**
- Microsoft Learn: Large semantic models in Power BI Premium: default size limit is 1 GB; for Pro workspaces assigned to Reserved Capacity for Pro workspaces it is also 1 GB.
- Learn: Data reduction techniques: shared capacity can host models up to 1 GB; Premium can host larger depending on SKU.
- With Fabric capacities, enabling Large semantic model storage format raises the limit to the capacity size (or an admin-set maximum). Desktop upload size remains limited to 10 GB.
- The 1 GB is the compressed model, not the source file (see Q48).
**Example:** Illustration only (compression depends on the data, Q48): a 6 GB CSV of attendance swipes might compress to roughly 0.6 GB, fine for Pro. But 40 GB would not fit; reduce it or use Premium/Fabric.
**DAX / Steps (not run here):** Service > semantic model > Settings > Large semantic model storage format > On > Apply (needs eligible capacity).
**Alternative:** Reduce the model (remove columns, summarise, DirectQuery), or use Direct Lake (Q55).
**Version / licensing note:** From the two Learn pages above (ms.date 2025-06-17 and 2024-12-30). Per-user storage quotas were not verified. Premium P SKUs are being retired in favour of Fabric F SKUs per Learn.
**Edge cases:** Premium models near half the capacity size can fail refresh for lack of memory.
**Likely follow-ups:**
1. *How to stay under 1 GB?* Remove unused columns, lower grain, numeric keys, incremental refresh.
2. *What if it is bigger?* Large storage format on Fabric/Premium.
**Common mistakes:** Quoting the source file size instead of the compressed model; forgetting that Desktop upload and Service limits differ.

### Q53 ⭐ 🔴 You must share an HR dashboard with 200 employees, most of whom have no Pro licence. What are your options?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Licensing judgement: capacity-backed workspaces versus per-user Pro, plus governance.
**Say this in the interview:** "Normally every viewer needs Pro. The standard fix is to put the content in a workspace on Fabric F64-or-larger or Premium capacity, so free users can view an app. The alternatives are giving all 200 Pro or PPU, a paginated/PDF export, or an embedded solution. I would also check security because it is HR data."
**Explain simply:**
- **Option 1:** Capacity workspace (Fabric F64+ or Premium P): Pro/PPU creators can share with free users, who can consume (Microsoft Learn: Power BI service features by license type).
- **Option 2:** Pro or PPU licences for all viewers if the workspace is on shared capacity (Learn: Publish a workspace app).
- **Option 3:** Publish a **workspace app** to the audience (up to 25 audiences, 10,000 users/groups per app per that page); creators need Pro or PPU.
- **Option 4:** Email subscriptions or exported PDF/Excel for a few people (check data sensitivity).
- **Option 5:** Embed for your customers / secure embed (see Q51), where viewers may not need licences in the app-owns-data pattern.
- Do not use "Publish to web" for HR data; Learn notes it does not work for shared-semantic-model reports, and it is public (public nature from memory, unverified).
**Example:** 200 employees, 15 already Pro. On shared capacity: 185 more licences. On an F64 workspace with an app: no per-viewer licence, but a capacity cost you must weigh. Compare using current Microsoft prices; I do not quote them as they change.
**DAX / Steps (not run here):** Service > workspace > Create app > Setup, Content, Audience (Entire organization or groups) > Publish app > Copy link. Workspace must be assigned to the capacity first (workspace settings).
**Alternative:** Move the numbers to Teams/SharePoint embed for convenience; viewers still need access rights.
**Version / licensing note:** Verified on the Learn pages cited (service-features-license-type ms.date 2026-08-24; apps page 2026-09-24): F64 or higher or Premium capacity lets free users consume; Free users with Build can create reports only in My workspace and cannot share them. Premium P SKUs are being retired in favour of F SKUs per the Direct Lake and data-reduction pages.
**Edge cases:** RLS for employees seeing only their own data; guests/external users need extra settings; app audiences must also have access to semantic models in other workspaces.
**Likely follow-ups:**
1. *Is F2 enough?* Learn says free-user consumption needs F64 or larger.
2. *What about PPU?* PPU-to-PPU only, unless content is on capacity.
**Common mistakes:** Assuming "app" alone removes licensing; sharing a workspace with 200 Viewers on shared capacity; ignoring RLS for HR data.

### Q54 ⭐ 🔴 How would you set up one shared semantic model so five analysts can build separate reports on the same HR numbers?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Hub-and-spoke design: one governed model, many thin reports, with permissions.
**Say this in the interview:** "I publish one certified semantic model in a central workspace, give analysts Build permission, and they connect to it from Desktop or the Service with a live connection to create their own reports. Measures like attrition are defined once, so every report shows the same number."
**Explain simply:**
- Microsoft Learn: Introduction to Semantic Models Across Workspaces: standardised models as "one source of truth"; Build permission controls who can build new content on a model; creators can promote or certify a model so others find it.
- Analysts open Desktop > Get data > Power BI semantic models (OneLake catalog) and create a report; no data is copied.
- Publishing the model and each report in separate .pbix files avoids file clashes (Q39).
- Free users can author on shared models only if the model sits on Premium/F64+ capacity and they can store reports only in My workspace; copying reports and certifying require Pro or PPU.
**Example:** The model owner defines `Attrition %` once. Five analysts (Recruiting, Payroll, L&D, Sales HR, Tech HR) build reports; every one shows 6.0% for September 2026.
**Sample data:** Same `HR_Monthly` table as Q49. Measures on the model: `Leavers = SUM(HR_Monthly[Leavers])` and `Attrition %`.
**DAX / Steps (not run here):**
```dax
Leavers = SUM ( HR_Monthly[Leavers] )

Attrition % =
DIVIDE (
    [Leavers],
    ( SUM ( HR_Monthly[OpeningHC] ) + SUM ( HR_Monthly[ClosingHC] ) ) / 2
)
```
1. Desktop: build and publish the model to workspace "HR Model" (Home > Publish).
2. Service: model > Manage permissions > grant Build to an analyst group; Settings > Endorsement > Promote/Certify.
3. Analyst, Desktop: Home > Get data > Power BI semantic models (or OneLake catalog) > select the model > Connect > build visuals > publish to their workspace.
**Alternative:** Analysts "copy a report" in the Service and modify it, since the data model is already built (Learn page). Or one workspace with Contributor access for all five, simpler but riskier.
**Result:** reproduced with pandas: every report using the shared measure returns Total 6.0% and Sales 6.1% (same output as Q49), because the logic exists in one place.
**Pandas check:** same snippet as Q49; run once, the result is shared by all reports.
**Version / licensing note:** From the Learn page above (ms.date 2025-06-04). App publishers must make sure audiences also have access to models outside the workspace. Publish to web does not work for reports on shared semantic models. Exact menu names change; from memory, unverified.
**Edge cases:** Changing or renaming a measure in the model can break every dependent report (Desktop warns on republish, Q38). RLS defined in the model applies to all reports. Only people with at least Read on the model can see it.
**Likely follow-ups:**
1. *Can analysts add their own measures?* Yes, report-level measures on a live connection, but they are not shared (from memory, unverified).
2. *Who owns changes?* A named model owner with a change process.
**Common mistakes:** Letting each analyst import the data separately (five versions of attrition); forgetting Build permission; no certification so no one trusts the model.

### Q55 ⭐ 🔴 What is Direct Lake mode, and when does it make sense compared with Import?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Fabric-era awareness: understanding storage modes and trade-offs, without overselling.
**Say this in the interview:** "Direct Lake is a storage mode in Microsoft Fabric where the model reads Delta tables from OneLake straight into memory, giving Import-like speed without copying all the data on every refresh. It suits large, lake-based data with IT-managed preparation; Import is still better for self-service analysts."
**Explain simply:**
- Microsoft Learn: Direct Lake overview: Direct Lake loads data from Delta tables (an open table file format used in the lake) in OneLake (Fabric's single data store) into memory; queries run on the VertiPaq engine, like Import, whereas DirectQuery sends queries to the source.
- Its refresh only copies metadata ("framing") and can finish in seconds, whereas Import refresh copies all data.
- Two flavours: Direct Lake on OneLake (no DirectQuery fallback) and Direct Lake on SQL endpoints (can fall back to DirectQuery).
- Use it when data is large, already in a Fabric lakehouse/warehouse, and freshness matters. Learn says Import often suits a self-service analyst who needs agility without IT dependency, and Power Query transformations only work with Import tables.
- Requires a Fabric capacity (F SKU/P SKU); Import and DirectQuery work with any Power BI/Fabric licence.
**Example:** A company logs 500 million daily attendance swipes in a Fabric lakehouse; refreshing a full Import copy takes hours. With Direct Lake the model re-points to the latest files quickly. A 12,000-row headcount table in Excel: Import is simpler.
**DAX / Steps (not run here):** In a Fabric workspace: lakehouse > New semantic model (select Delta tables) > then edit the model in the web or via Desktop live edit (menu names from memory, unverified).
**Alternative:** Import with scheduled/incremental refresh, or DirectQuery for live source data; composite model combining Direct Lake with Import tables (supported for Direct Lake on OneLake).
**Version / licensing note:** From Learn: Direct Lake overview (ms.date 2026-09-02): needs Fabric capacity; guardrails by SKU (for example F2 to F8: 300 million rows per table, 10 GB model size; F64: unlimited model size on disk). Calculated columns on Direct Lake on OneLake are in preview (August 2026 What's new). Direct Lake cannot refresh via a gateway and is not available in personal workspaces (Learn limitations list).
**Edge cases:** Exceeding guardrails makes Direct Lake on OneLake refresh fail until tables are optimised; on SQL endpoints it falls back to DirectQuery and gets slower. Delta table tuning matters.
**Likely follow-ups:**
1. *Is it replacing Import?* No; the page says Import and DirectQuery stay relevant.
2. *RLS?* Supported; fixed-identity cloud connection strongly recommended.
**Common mistakes:** Calling it "DirectQuery"; assuming it works on a Pro-only tenant; ignoring data preparation in the lake.
