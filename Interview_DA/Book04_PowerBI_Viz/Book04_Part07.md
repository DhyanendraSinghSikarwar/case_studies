# Book 4 — Power BI & Visualization | Part 7: Power BI Service: Publishing, Refresh, Gateways, Incremental Refresh, RLS, Workspaces, Licensing 🟢🟡🔴

**Target:** 65 questions | **Actual:** 65 questions
**Scope:** publishing from Desktop, scheduled/on-demand/incremental refresh, gateways, row-level security, workspaces and roles, apps and sharing, licensing (Free/Pro/PPU/Fabric).

### Q1 ⭐⭐⭐ 🟢 What is row-level security (RLS) in Power BI, and why would you use it?
**Asked at:** RLS appears in one Deloitte USI Hyderabad Power BI round (Sept 2025 Glassdoor report, single anecdote, mapping unverified) and an older 2022 Cognizant report; otherwise commonly asked (no other company-specific report found).
**What the interviewer is checking:** Do you know RLS limits which rows a person sees, using one shared report instead of many copies?
**Say this in the interview:** "RLS means one report, but each person sees only the rows they are allowed to. I define a role with a DAX filter, for example Region = North, and assign people to it. It saves me from building and maintaining a separate report per team."
**Explain simply:**
- **Row-level security (RLS)** = a filter on the data that follows the user around, whatever visual they open.
- A **role** is a named rule. A **DAX filter** (DAX is Power BI's formula language) says which rows the role keeps.
- Used for confidentiality: an HR business partner must not see another region's salaries.
- One report, one refresh, many audiences.
**Example:** An employee table has 8 people across North, South and West. The "North" role keeps only North rows, so a North manager sees 3 employees and 113,000 total salary, not the company's 368,000.
**Sample data:** Table `Employee`

| EmpID | Name | Region | ManagerEmail | Salary |
|---|---|---|---|---|
| 101 | Asha | North | priya@corp.com | 40000 |
| 102 | Ravi | South | arun@corp.com | 52000 |
| 103 | Meena | North | priya@corp.com | 35000 |
| 104 | Karan | West | neha@corp.com | 60000 |
| 105 | Divya | South | arun@corp.com | 45000 |
| 106 | Imran | North | priya@corp.com | 38000 |
| 107 | Sneha | West | neha@corp.com | 50000 |
| 108 | Vikram | South | arun@corp.com | 48000 |

**DAX / Steps (not run here):** Desktop: Modeling tab > Security > Manage roles > Create > name `North` > table `Employee` > filter expression:
```dax
[Region] = "North"
```
**Alternative:** Build separate reports or filtered copies per region. It works but multiplies maintenance and risks leaks. A slicer is not security: users can clear it.
**Result:** Reproduced with pandas (not a DAX engine): the North role sees Asha, Meena, Imran: 3 of 8 rows.
**Pandas check:**
```python
n = emp[emp["Region"]=="North"]
print(n[["Name","Region"]].to_string(index=False)); print("Headcount seen:", len(n), "of", len(emp))
```
Output: Asha, Meena, Imran (all North); `Headcount seen: 3 of 8`.
**Version / licensing note:** From memory, unverified (learn.microsoft.com fetch failed from this session): RLS roles are defined in Desktop and enforced in the Service; it only restricts people with the Viewer workspace role (see Q23).
**Edge cases:** A user in no role (but with access via Viewer) sees no rows. Blank Region rows are hidden by the North filter.
**Likely follow-ups:** 1) *Static or dynamic?* See Q7. 2) *Does it hide columns?* No, see Q25.
**Common mistakes:** Using a slicer as security; testing only as the owner, who sees everything.

### Q2 ⭐⭐⭐ 🟢 How do you publish a report from Power BI Desktop to the Power BI Service?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the basic hand-off from building (Desktop) to sharing (Service)?
**Say this in the interview:** "In Desktop I save the file, click Publish on the Home tab, sign in with my work account, and pick the workspace. It uploads the report and its data model, then I open it in the Service from the link."
**Explain simply:**
- **Desktop** is the free Windows app where you build; the **Service** is the online site (app.powerbi.com) where you share and refresh.
- Publishing uploads two things: the **report** (pages and visuals) and the **semantic model** (formerly called dataset: the data plus measures).
- Publishing does not auto-refresh the data later; you set up a refresh (Q3).
**Example:** You build an attrition report on a monthly HR extract and publish it to the "HR Analytics" workspace so the CHRO can open it in a browser.
**DAX / Steps (not run here):** 1) Save the .pbix. 2) Ribbon: Home > Share group > Publish. 3) Sign in with your work or school account. 4) Select the destination workspace > Select. 5) Click "Open '<file>' in Power BI" in the success dialog.
**Alternative:** Upload the .pbix directly in the Service: workspace > New (or Upload) > Upload a file > Browse.
**Version / licensing note:** From memory, unverified: Desktop is free and Windows-only; publishing to shared workspaces generally needs a Pro or Premium Per User licence (or a capacity that allows it). Free-licence rules have shifted with Fabric, so check the current licence page.
**Edge cases:** If the model has an on-premises source, you must set up a gateway before refresh works (Q6). Republishing over an existing report overwrites it (Q17).
**Likely follow-ups:** 1) *Where does it go?* A workspace (Q4). 2) *Who can see it?* Only people given access (Q12).
**Common mistakes:** Publishing to My workspace and then wondering why the team cannot find it; forgetting to set credentials after the first publish.

### Q3 ⭐⭐⭐ 🟢 What is scheduled refresh in Power BI, and how do you set it up?
**Asked at:** commonly asked (no company-specific report found); named in generic prep lists (ConsoleFlare, Adaface snippets).
**What the interviewer is checking:** Do you know published data is a snapshot and must be refreshed on a schedule?
**Say this in the interview:** "An Import-mode report holds a copy of the data. Scheduled refresh re-pulls from the source at times I choose, so the report stays current. I set it in the Service under the semantic model's Refresh settings, after making sure credentials or a gateway are configured."
**Explain simply:**
- **Import mode** = data copied into Power BI; it goes stale until refreshed.
- **Scheduled refresh** = automatic reload at set times, e.g. 7:00 AM daily.
- Cloud sources (Azure SQL, SharePoint) need only credentials; on-premises ones need a **gateway** (a bridge program on a company machine).
- Daily cap: commonly 8 on Pro, 48 on Premium (Q16).
**Example:** An HR attendance file lands at 6:00 AM; you schedule refresh at 6:30 AM and 1:30 PM so the dashboard is fresh when managers log in.
**DAX / Steps (not run here):** Service > workspace > semantic model (three dots) > Settings > Data source credentials (sign in) > Gateway and cloud connections (if on-prem) > Refresh > turn on "Keep your data up to date" > set frequency, time zone, times > Apply. Optional: tick "Send refresh failure notifications".
**Alternative:** Refresh on demand (Q18), or an automated refresh through Power Automate or the REST API (from memory, unverified).
**Version / licensing note:** From memory, unverified: limits depend on licence and capacity (Q16).
**Edge cases:** Time zone in the schedule dialog is easy to mis-set. DirectQuery and Live Connection have no scheduled refresh of data (Q14).
**Likely follow-ups:** 1) *What if it fails?* Q8. 2) *How many times?* Q16.
**Common mistakes:** Forgetting to enter credentials; scheduling a dozen refreshes on Pro and hitting the cap.

### Q4 ⭐⭐⭐ 🟢 What is a Power BI workspace, and how is it different from My workspace?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand shared team space versus your private scratch space?
**Say this in the interview:** "A workspace is a shared folder in the Service where a team keeps reports, models and dashboards, with roles for who can do what. My workspace is every user's personal area, only for their own content, so team work should not live there."
**Explain simply:**
- **Workspace** = a collaboration container with members and roles (Q11).
- **My workspace** = personal, private by default, tied to one person. If they leave, their content is at risk.
- Workspaces can publish an **app** to a wider audience (Q31).
**Example:** The HR team creates "HR Analytics": two analysts as Members, a trainee as Contributor, the CHRO's office as Viewers.
**DAX / Steps (not run here):** Service > left nav Workspaces > New workspace (or Create a workspace) > name it > Advanced: choose licence mode if needed > Save > Access button to add people.
**Alternative:** Use My workspace only for drafts and experiments.
**Version / licensing note:** From memory, unverified: creating workspaces and adding others generally needs a Pro or PPU licence; the current "Workspaces" UI is the modern one (the old "classic" workspaces were retired).
**Edge cases:** Moving content from My workspace requires re-publishing or having a Pro licence and copying.
**Likely follow-ups:** 1) *Roles?* Q11. 2) *Why not share from My workspace?* Single owner risk.
**Common mistakes:** Keeping production reports in My workspace; giving everyone Admin.

### Q5 ⭐⭐⭐ 🟡 How do you implement row-level security in Power BI, end to end (Desktop to Service)?
**Asked at:** RLS is reported in the Sept 2025 Deloitte USI Hyderabad round (single Glassdoor anecdote, mapping unverified) and a 2022 Cognizant report; otherwise commonly asked.
**What the interviewer is checking:** Can you do the full chain: define roles, test, publish, assign users, and know the Viewer caveat?
**Say this in the interview:** "Four steps. In Desktop I create roles with DAX filters and test with View as. I publish. In the Service I open the model's Security page and add users or groups to each role. Then I test again with Test as role, and make sure end users are Viewers."
**Explain simply:**
- **Define:** Modeling > Manage roles; one DAX filter per table per role.
- **Test in Desktop:** Modeling > View as.
- **Publish** (Q2). Roles travel with the model, but members do not.
- **Assign:** Service > model > Security > pick role > add emails or security groups (a **security group** is a managed list of people in Microsoft Entra, the company directory).
- **Check:** only people with the Viewer workspace role are restricted (Q23).
**Example:** Roles North, South, West and CHRO (no filter). Headcount seen: North 3, South 3, West 2, CHRO 8.
**Sample data:** Same `Employee` table as Q1.
**DAX / Steps (not run here):**
```dax
-- Role North, on table Employee
[Region] = "North"
-- Role CHRO: leave filter empty (or TRUE())
-- Measure to check in a card:
Headcount = COUNTROWS ( Employee )
```
Click-path: Desktop: Modeling > Security > Manage roles. Service: workspace > model "..." > Security > select role > Add > Save.
**Alternative:** One dynamic role keyed on email (Q7, Q20) instead of one role per region.
**Result:** Reproduced with pandas: Headcount North 3, South 3, West 2, CHRO 8.
**Pandas check:**
```python
roles = {"North":emp["Region"]=="North","South":emp["Region"]=="South","West":emp["Region"]=="West","CHRO (no filter)":emp["Region"].notna()}
for r,m in roles.items(): print(r, int(m.sum()))
```
Output: `North 3`, `South 3`, `West 2`, `CHRO (no filter) 8`.
**Version / licensing note:** From memory, unverified: role assignment is in the Service; Desktop View as only simulates.
**Edge cases:** A person in several roles sees the union of rows. A Viewer in no role sees nothing.
**Likely follow-ups:** 1) *Who is not restricted?* Q23. 2) *Groups?* Q24.
**Common mistakes:** Adding users to the role in Desktop (it does not work); making end users Members.

### Q6 ⭐⭐⭐ 🟡 What is an on-premises data gateway, and when do you need one?
**Asked at:** gateways are listed as a recurring topic for service MNC rounds in the repo research (interview_processes.md); no company-specific report found.
**What the interviewer is checking:** Do you know how cloud Power BI reaches data inside the company network?
**Say this in the interview:** "A gateway is a small program installed on a company machine that lets the Power BI Service securely reach on-premises data, such as SQL Server or a shared-drive Excel file, for scheduled refresh or DirectQuery. I need one whenever the source is not reachable from the internet."
**Explain simply:**
- **On-premises** = inside the company's own network, not in the cloud.
- The gateway makes **outbound** connections to the Service, so the firewall need not open inbound ports (from memory, unverified).
- Not needed for cloud sources such as Azure SQL, SharePoint Online or OneDrive.
- Two kinds: standard and personal (Q15).
**Example:** HR payroll sits in a SQL Server in the Hyderabad office. A gateway on an always-on office server lets the dashboard refresh every morning.
**DAX / Steps (not run here):** Download the gateway installer from the Service (Download icon > Data Gateway) > install on an always-on machine > sign in > register > Service: Settings (gear) > Manage connections and gateways > add data source > then map the model to it in its Settings.
**Alternative:** Move data to a cloud store (OneDrive, Azure SQL) and avoid the gateway.
**Version / licensing note:** From memory, unverified. The sources file records the gateway overview page as read in earlier research (standard, personal, VNet types); I could not re-fetch it.
**Edge cases:** If the gateway machine is off, refresh fails (Q8). Install on a server, not a laptop.
**Likely follow-ups:** 1) *Personal vs standard?* Q15. 2) *Cluster?* Q46.
**Common mistakes:** Installing on a laptop that sleeps; thinking SharePoint Online needs a gateway.

### Q7 ⭐⭐⭐ 🟡 What is the difference between static and dynamic row-level security?
**Asked at:** commonly asked; the Deloitte USI and Cognizant RLS mentions (see Q1) do not say which type.
**What the interviewer is checking:** Can you choose between many fixed roles and one rule that adapts to the user?
**Say this in the interview:** "Static RLS hard-codes the value in each role, like Region = North, so you need one role per region. Dynamic RLS compares a column to the signed-in user's identity, so one role serves everyone and the data table drives access."
**Explain simply:**
- **Static:** simple, but 20 regions means 20 roles and 20 membership lists.
- **Dynamic:** uses `USERPRINCIPALNAME()`, a function that returns the signed-in user's login (an email-style name).
- Dynamic needs a column (or mapping table) holding who may see each row.
- Dynamic is easier to maintain; static is easier to explain.
**Example:** Priya, Arun and Neha each manage a region. Both approaches show them 3, 3 and 2 rows.
**Sample data:** Table `Employee` as in Q1 (ManagerEmail column used for dynamic).
**DAX / Steps (not run here):**
```dax
-- Static, role "North":
[Region] = "North"
-- Dynamic, one role "ManagerView":
[ManagerEmail] = USERPRINCIPALNAME ()
```
**Alternative:** Dynamic with a separate `Security` mapping table (UserEmail, Region) related to Employee, useful when one user covers many regions.
**Result:** Reproduced with pandas: priya 3/3 (static/dynamic), arun 3/3, neha 2/2.
**Pandas check:**
```python
users = {"priya@corp.com":"North","arun@corp.com":"South","neha@corp.com":"West"}
for u in users:
    static = (emp["Region"]==users[u]).sum()
    dyn = (emp["ManagerEmail"].str.lower()==u.lower()).sum()
    print(u, "static role rows:", static, "| dynamic rows:", dyn)
```
Output: priya 3 and 3; arun 3 and 3; neha 2 and 2.
**Version / licensing note:** From memory, unverified; same feature on all licences that support the Service.
**Edge cases:** A user absent from the mapping sees nothing (0 rows reproduced for `zed@corp.com`).
**Likely follow-ups:** 1) *Write it?* Q20. 2) *USERNAME vs UPN?* Q21.
**Common mistakes:** Still creating one role per user; mismatched email spelling between data and login.

### Q8 ⭐⭐⭐ 🟡 Your scheduled refresh failed overnight. How do you troubleshoot it?
**Asked at:** commonly asked (no company-specific report found); a standard scenario in prep lists.
**What the interviewer is checking:** Do you have a calm, ordered checklist rather than guesses?
**Say this in the interview:** "I open the refresh history to read the exact error first. Then I check the usual four: expired credentials, gateway offline, source changed (a column renamed or file moved), and timeouts or capacity limits. I fix it, run a manual refresh, and confirm."
**Explain simply:**
- **Refresh history** shows each run, status, time and error code.
- Credentials expired: re-sign in under Data source credentials.
- Gateway: is the machine on and the service running (Q6)?
- Source change: a renamed column breaks Power Query steps.
- Too slow: see Q34.
**Example:** The 6:30 AM HR refresh failed with "credentials invalid"; the service account password had been rotated. You update credentials, press Refresh now, and it succeeds in 4 minutes.
**DAX / Steps (not run here):** Service > workspace > model "..." > Refresh > Refresh history > click the failed row > read details > fix > Refresh now.
**Alternative:** Set failure emails (Q35) so you hear before the users do.
**Version / licensing note:** From memory, unverified (the sources file notes failure emails and a 2-hour limit on shared capacity from earlier research; I did not re-fetch).
**Edge cases:** Several consecutive failures can lead the service to pause the schedule (Q47).
**Likely follow-ups:** 1) *Who is told?* Q35. 2) *Slow, not failed?* Q34.
**Common mistakes:** Re-running blindly without reading the error; fixing the PBIX but not republishing.

### Q9 ⭐⭐⭐ 🟡 What is incremental refresh in Power BI, and why is it used?
**Asked at:** incremental refresh is listed as a recurring service-MNC topic in the repo research; no company-specific report found.
**What the interviewer is checking:** Do you know it reloads only recent data to save time on big tables?
**Say this in the interview:** "Incremental refresh keeps old data as-is and reloads only a recent window, say the last few days, instead of the whole table every time. It cuts refresh time and load on the source, and it makes huge tables practical."
**Explain simply:**
- The table is split into **partitions** (slices by date, like one per month).
- Old slices are **archived** and left alone; the recent slice is refreshed.
- Needs a date column and two parameters, `RangeStart` and `RangeEnd` (Q29).
- Works best when the source supports **query folding** (Power BI pushes the date filter into the source query).
**Example:** A daily attendance table has about 1,765 days since Jan 2022. Refreshing only October 2026 reloads 31 days, 1.8% of the data.
**DAX / Steps (not run here):** Define RangeStart/RangeEnd, filter the table on them, then right-click the table > Incremental refresh and real-time data > set "archive data starting" (e.g. 5 years) and "refresh data starting" (e.g. 10 days). See Q30.
**Alternative:** Partition the source and do a full refresh; or use a smaller extract table.
**Result:** Reproduced with pandas (one row per day assumption): 31 of 1,765 rows reloaded (1.8%).
**Pandas check:**
```python
days = pd.date_range("2022-01-01","2026-10-31"); fact = pd.DataFrame({"Date":days})
reloaded = fact[fact["Date"]>=pd.Timestamp("2026-10-01")]
print(len(fact), len(reloaded), f"{len(reloaded)/len(fact):.1%}")
```
Output: `1765 31 1.8%`.
**Version / licensing note:** From memory, unverified (sources file records the incremental-refresh overview page, with 2h/5h refresh limits, as read in earlier research; not re-fetched): the policy is defined in Desktop and applied in the Service.
**Edge cases:** Without query folding, Power BI may still pull everything each time. Rows changing in old partitions are missed unless "Detect data changes" is used.
**Likely follow-ups:** 1) *RangeStart rules?* Q29. 2) *Can I download the PBIX again?* No: the published model cannot be downloaded once incremental refresh is applied (from memory, unverified).
**Common mistakes:** Calling it "append only new rows" (it replaces recent partitions); not checking folding.

### Q10 ⭐⭐ 🟢 What is the difference between a report, a dashboard and an app in the Power BI Service?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the three Service objects and their purpose?
**Say this in the interview:** "A report is multi-page and interactive, built from one model. A dashboard is a single page of pinned tiles from many reports. An app is a packaged bundle of reports and dashboards that I publish to business users."
**Explain simply:**
- **Report:** pages, filters, slicers, built in Desktop or the Service.
- **Dashboard:** one canvas of **tiles** (pinned visuals); created only in the Service; can mix several reports.
- **App:** a read-only package of content for many people (Q31).
- Dashboards cannot be built in Desktop.
**Example:** The HR report has pages for headcount and attrition; the CHRO's dashboard pins the attrition card and a hiring funnel from another report; the HR app bundles both for managers.
**DAX / Steps (not run here):** Pin a visual: open a report > hover a visual > Pin icon > choose existing or new dashboard.
**Alternative:** Skip dashboards; use a one-page report as a "summary page".
**Version / licensing note:** From memory, unverified.
**Edge cases:** Dashboard tiles show the last refreshed state; deleting a source report breaks its tile.
**Likely follow-ups:** 1) *Can a dashboard use two models?* Yes. 2) *Mobile?* Q40.
**Common mistakes:** Saying dashboard and report are the same.

### Q11 ⭐⭐ 🟢 What are the four workspace roles (Admin, Member, Contributor, Viewer) and what can each do?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you grant the least access needed?
**Say this in the interview:** "Admin manages everything including access and deleting the workspace. Member can edit, add people with lower roles and publish apps. Contributor can create and edit content but not manage access or publish the app. Viewer can only view; RLS applies to Viewers."
**Explain simply:**
- **Admin:** full control, add any role.
- **Member:** edit, share, publish app (Admins can restrict this) (from memory).
- **Contributor:** build and edit, publish into the workspace, schedule refresh; cannot update the app.
- **Viewer:** consume only; the only role where RLS restricts rows (Q23).
**Example:** Lead analyst Admin, two analysts Members, a trainee Contributor, HR business partners Viewers.
**DAX / Steps (not run here):** Workspace > Access (or Manage access) > Add people or groups > pick role > Add.
**Alternative:** Skip workspace access; share the app instead and keep the workspace tight.
**Version / licensing note:** From memory, unverified (the sources file says the Roles in workspaces page was read in earlier research; not re-fetched). Exact permission matrix changes; check it.
**Edge cases:** Highest role wins across groups. Viewers still need a licence unless the capacity is large enough (Q12).
**Likely follow-ups:** 1) *Does RLS apply to Contributors?* Q23. 2) *Why Viewer for most?* Least privilege.
**Common mistakes:** Making everyone Member; expecting RLS to restrict Members.

### Q12 ⭐⭐ 🟢 How do you share a report with a colleague in the Power BI Service, and what licence do they need?
**Asked at:** commonly asked (no company-specific report found); licensing is a stated interview topic in the Withum snippet.
**What the interviewer is checking:** Do you know the share options and that licences gate access?
**Say this in the interview:** "Open the report, click Share, enter their email, choose whether they can reshare or build on the data, and send. For normal workspaces both of us need a Pro or PPU licence, unless the content is in a Premium or large Fabric capacity, where viewers can be on free licences."
**Explain simply:**
- Three routes: **Share** link, add to **workspace** as Viewer, or publish an **app**.
- Sharing a report also needs access to the underlying semantic model (the link handles that when allowed).
- Licences: Free, Pro, PPU (Premium Per User), or capacity-based.
- The commonly cited Fabric threshold for free viewers is capacity F64 or larger: not verified here; it changes.
**Example:** You share the attrition report with a colleague at priya@corp.com; she has Pro, so she opens it from the email link.
**DAX / Steps (not run here):** Report open in Service > Share (top bar) > People in your organization / specific people > type email > tick permissions (allow recipients to share, build content) > optional message > Send.
**Alternative:** Add her as a workspace Viewer (Q11) or give her the app (Q31).
**Version / licensing note:** From memory, unverified: free vs Pro/PPU/capacity rules and the F64 threshold; the earlier-research "service features by licence type" page was not re-fetched.
**Edge cases:** RLS still applies to link recipients if they get Viewer-type access; external guests need extra setup.
**Likely follow-ups:** 1) *Can free users view?* Only in capacity content (see note). 2) *Share vs app?* App for many people.
**Common mistakes:** Sharing from My workspace; forgetting the colleague's licence.

### Q13 ⭐⭐ 🟢 What is the difference between a semantic model (dataset) and a report in the Power BI Service?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you separate data/logic from visuals?
**Say this in the interview:** "The semantic model, previously called dataset, holds the data, relationships and measures, and it is what gets refreshed. The report is the visuals sitting on top. One model can serve many reports."
**Explain simply:**
- **Semantic model** = tables + relationships + DAX measures + refresh settings + RLS roles.
- **Report** = pages and charts that read from the model.
- Refresh, gateway and RLS are set on the model, not the report.
- "Dataset" is the older name; interviewers may use either.
**Example:** One "HR Core" model feeds an attrition report and a hiring report, so a measure fixed once is fixed in both.
**DAX / Steps (not run here):** In the workspace list, the model has a database icon, the report a bar-chart icon. Settings via model "..." > Settings.
**Alternative:** A thin report connected live to a shared model ("Live Connection", Q14).
**Version / licensing note:** From memory, unverified: the rename from dataset to semantic model happened with Fabric.
**Edge cases:** Deleting a model breaks its reports.
**Likely follow-ups:** 1) *Where do I set refresh?* On the model. 2) *Reuse a model?* Yes, via Live Connection.
**Common mistakes:** Trying to schedule refresh "on the report".

### Q14 ⭐⭐ 🟢 What is the difference between Import mode, DirectQuery and Live Connection from a refresh point of view?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know which modes need data refresh?
**Say this in the interview:** "Import copies data in, so it needs scheduled refresh. DirectQuery keeps data at the source and queries it live, so there is no data refresh but each click hits the source. Live Connection points a report at an existing published model, so the refresh is owned by that model."
**Explain simply:**
- **Import:** fastest visuals, data is a snapshot, scheduled refresh required.
- **DirectQuery:** always current, slower, load on the source; the Service may still refresh cached tile data (from memory).
- **Live Connection:** to a published semantic model or Analysis Services; no model of your own.
**Example:** A payroll snapshot (Import) vs a live ticket table (DirectQuery) vs a report using the shared HR Core model (Live).
**DAX / Steps (not run here):** Desktop > Home > Get data > pick source > choose Import or DirectQuery in the dialog; for a published model: Get data > Power BI semantic models.
**Alternative:** Composite model mixing Import and DirectQuery tables.
**Version / licensing note:** From memory, unverified.
**Edge cases:** DirectQuery on on-premises data still needs a gateway.
**Likely follow-ups:** 1) *Which is fastest?* Import. 2) *RLS with DirectQuery?* Q25.
**Common mistakes:** Choosing DirectQuery for "freshness" without testing speed.

### Q15 ⭐⭐ 🟢 What is the difference between a personal gateway and a standard (enterprise) gateway?
**Asked at:** gateway types are a named prep-list theme (ConsoleFlare snippet); no company-specific report found.
**What the interviewer is checking:** Do you pick the right gateway for a team versus a person?
**Say this in the interview:** "A personal gateway serves only one user, runs on their machine and supports Import refresh only. A standard gateway is installed by IT on a server, shared by many users and supports Import plus DirectQuery and live connections."
**Explain simply:**
- **Personal:** quick for an individual; stops when the laptop sleeps or logs off.
- **Standard:** central, can be clustered (Q46), managed by admins.
- Use standard for anything the team depends on.
**Example:** An analyst refreshing a personal Excel on a laptop uses personal mode; the shared payroll SQL Server uses standard mode.
**DAX / Steps (not run here):** Installer asks "On-premises data gateway (recommended)" or "personal mode".
**Alternative:** Move the source to the cloud (no gateway).
**Version / licensing note:** From memory, unverified; the sources file notes the gateway page lists standard, personal and VNet types, not re-fetched.
**Edge cases:** Personal mode cannot be shared between users.
**Likely follow-ups:** 1) *Cluster?* Q46. 2) *VNet gateway?* For sources in an Azure virtual network.
**Common mistakes:** Running production refresh on a personal gateway.

### Q16 ⭐⭐ 🟢 How often can a Power BI dataset be refreshed per day on Pro versus Premium?
**Asked at:** commonly asked; the 8 vs 48 figures appear in a ConsoleFlare snippet and the earlier research.
**What the interviewer is checking:** Do you know the scheduling limits by licence?
**Say this in the interview:** "On shared capacity, which Pro uses, a model can be scheduled up to 8 times a day. On Premium, PPU or Fabric capacity it is up to 48 times a day, about every 30 minutes."
**Explain simply:**
- Limits are on **scheduled** refreshes per model per day.
- 8 per day on Pro/shared; 48 on Premium/PPU/Fabric.
- Many more updates need DirectQuery, streaming, or API-triggered refresh on capacity.
- Refresh duration limits too: 2 hours shared, 5 hours Premium (Q34).
**Example:** Hourly updates 9 to 18 (10 runs) would exceed Pro's 8; you pick 8 key times.
**DAX / Steps (not run here):** Model Settings > Refresh > Add another time (greyed when you reach the limit).
**Alternative:** DirectQuery for near real-time.
**Version / licensing note:** From memory, unverified: numbers were recorded as 8 and 48 from the refresh-data page in earlier research (updated 2026-10) but I could not re-fetch it. Limits change; check the live page.
**Edge cases:** On-demand refreshes are counted differently from scheduled ones (from memory, unverified).
**Likely follow-ups:** 1) *Why does Pro cap?* Shared resources. 2) *Alternatives?* DirectQuery.
**Common mistakes:** Quoting 8 for all licences; mixing up refresh count and duration limit.

### Q17 ⭐⭐ 🟢 What happens when you publish a PBIX file again with the same name to the same workspace?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know republishing overwrites, and what survives?
**Say this in the interview:** "Power BI asks whether to replace. If I confirm, the model and report in that workspace are overwritten by my new file, while dashboard tiles, the app link and, generally, refresh settings stay connected."
**Explain simply:**
- Same name + same workspace = **replace**, not duplicate.
- Existing dashboard tiles keep working; changed visuals may break pins.
- Credentials and schedules usually persist, but check them (from memory, unverified).
- Edits made only in the Service to the report are lost.
**Example:** You fix a measure in Desktop and republish "HR Attrition"; the CHRO's dashboard tile now shows the corrected value.
**DAX / Steps (not run here):** Desktop > Home > Publish > select same workspace > Replace in the prompt.
**Alternative:** "Save as" a new name to keep both versions, or use deployment pipelines (Q45).
**Version / licensing note:** From memory, unverified.
**Edge cases:** Different workspace = a new copy, not a replacement. A model with incremental refresh may reject some changes.
**Likely follow-ups:** 1) *Lost the Service edits?* Yes. 2) *Safer way?* Pipelines.
**Common mistakes:** Editing in the Service then overwriting from an old PBIX.

### Q18 ⭐⭐ 🟢 How do you refresh a report on demand in the Power BI Service?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know "Refresh now" and that you refresh the model, not the report page?
**Say this in the interview:** "In the workspace, I click the Refresh now icon next to the semantic model. The report picks up new data once it finishes; I can see the result in refresh history."
**Explain simply:**
- **Refresh now** triggers an immediate refresh of the model.
- It needs credentials (and a gateway for on-prem).
- Browser reload (F5) does not refresh data; it only reloads visuals.
**Example:** Payroll finance fixed a file at 3 PM; you press Refresh now and managers see updated numbers at 3:10 PM.
**DAX / Steps (not run here):** Service > workspace > find the semantic model > Refresh now (circular arrow icon) or "..." > Refresh now. Check "..." > Refresh history.
**Alternative:** In Desktop, Home > Refresh then republish; or trigger via API.
**Version / licensing note:** From memory, unverified: on-demand refreshes may still count toward some limits.
**Edge cases:** DirectQuery models have nothing to refresh on demand.
**Likely follow-ups:** 1) *Does it count to 8?* Unverified. 2) *Failed?* Q8.
**Common mistakes:** Pressing F5 and expecting new data.

### Q19 ⭐⭐ 🟡 Write the DAX filter for a role so each manager sees only the rows of their own region (static RLS for one region).
**Asked at:** commonly asked; the RLS rounds in the repo research do not specify the DAX asked.
**What the interviewer is checking:** Can you write a simple table filter expression that returns TRUE/FALSE per row?
**Say this in the interview:** "In Manage roles I pick the Employee table and write `[Region] = "North"`. It is a true-or-false test per row; only TRUE rows survive. I create one role per region."
**Explain simply:**
- The expression is evaluated for every row of that table; rows returning TRUE are visible.
- No `CALCULATE`/`FILTER` needed: it is a condition only.
- Filters flow through relationships to related tables (for example, from Employee dimension to the Attendance fact).
**Example:** North manager Priya sees Asha, Meena, Imran only.
**Sample data:** Table `Employee`, as in Q1.
**DAX / Steps (not run here):**
```dax
[Region] = "North"
```
Click-path: Modeling > Manage roles > Create > name "North" > Employee > Table filter DAX expression.
**Alternative:** `Employee[Region] = "North"` (full name) or `FILTER`-style `Employee[Region] IN {"North","East"}` for several regions.
**Result:** Reproduced with pandas: 3 rows (Asha, Meena, Imran).
**Pandas check:**
```python
print(emp[emp["Region"]=="North"][["Name","Region"]].to_string(index=False))
```
Output: Asha, Meena, Imran with Region North.
**Version / licensing note:** From memory, unverified; DAX comparison of text is case-insensitive.
**Edge cases:** Spelling "north " with a trailing space matches nothing. Blank regions are excluded.
**Likely follow-ups:** 1) *Many regions?* Dynamic, Q20. 2) *Multiple tables?* One filter per table.
**Common mistakes:** Writing a measure instead of a filter; adding quotes around the column.

### Q20 ⭐⭐ 🟡 Write the DAX filter for dynamic RLS so each user sees only the rows linked to their own email address.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the USERPRINCIPALNAME pattern and a mapping column?
**Say this in the interview:** "One role with the filter `[ManagerEmail] = USERPRINCIPALNAME()`. When Priya opens the report, Power BI plugs in her login email, so she sees only rows tagged with her address."
**Explain simply:**
- `USERPRINCIPALNAME()` returns the current user's sign-in name, usually their work email.
- The data must contain that email in a column (here `ManagerEmail`).
- DAX text equality ignores upper/lower case.
**Example:** Priya sees her 3 reports; a user not in the data sees 0 rows.
**Sample data:** Table `Employee`, as in Q1.
**DAX / Steps (not run here):**
```dax
[ManagerEmail] = USERPRINCIPALNAME ()
```
Click-path: Modeling > Manage roles > Create > "Dynamic" > Employee > paste filter > Save; then assign users in the Service (Q24).
**Alternative:** Mapping table `Security[UserEmail]` related to the dimension, with filter `[UserEmail] = USERPRINCIPALNAME()` on the Security table, for users with many regions.
**Result:** Reproduced with pandas: `Priya@Corp.com` matches 3 rows; `zed@corp.com` matches 0.
**Pandas check:**
```python
u="Priya@Corp.com"
v = emp[emp["ManagerEmail"].str.lower()==u.lower()]
print(v[["Name","ManagerEmail"]].to_string(index=False)); print("rows:",len(v))
print("unmapped user rows:", (emp["ManagerEmail"].str.lower()=="zed@corp.com").sum())
```
Output: Asha, Meena, Imran; `rows: 3`; `unmapped user rows: 0`.
**Version / licensing note:** From memory, unverified.
**Edge cases:** Login name differs from mail address for some tenants. In Desktop the function returns your own account, so use View as (Q22).
**Likely follow-ups:** 1) *USERNAME?* Q21. 2) *CHRO sees all?* Q38.
**Common mistakes:** Using `USERNAME()` in the Service and mismatching; storing names, not emails.

### Q21 ⭐⭐ 🟡 What is the difference between USERNAME() and USERPRINCIPALNAME() in RLS, and how do they behave in Desktop versus the Service?
**Asked at:** commonly asked (no company-specific report found); named in earlier research.
**What the interviewer is checking:** Do you know which function is safe in both environments?
**Say this in the interview:** "Both return who is signed in. In the Service they usually give the same email-style value. In Desktop `USERNAME()` returns DOMAIN\user while `USERPRINCIPALNAME()` returns the email-style name. I prefer `USERPRINCIPALNAME()` because it matches the Service."
**Explain simply:**
- `USERNAME()` = login in the form DOMAIN\user in Desktop.
- `USERPRINCIPALNAME()` (UPN) = user@company.com style.
- In the Service, `USERNAME()` also returns the UPN, so Desktop tests can differ from live behaviour (from memory, unverified).
- Always test with View as and typed users.
**Example:** Data stores priya@corp.com. In Desktop `USERNAME()` returns CORP\priya, so no rows match; `USERPRINCIPALNAME()` matches.
**DAX / Steps (not run here):** Compare in a test measure `Who = USERPRINCIPALNAME()` in a card; Modeling > View as > Other user.
**Alternative:** Store both formats, or normalise in the mapping table.
**Version / licensing note:** From memory, unverified; the earlier research notes the RLS page covers this, but I could not re-fetch it.
**Edge cases:** Guest users have `#EXT#` style UPNs. On-prem Analysis Services differs.
**Likely follow-ups:** 1) *Which do you use?* UPN. 2) *Case?* DAX equality ignores case.
**Common mistakes:** Testing only in Desktop and assuming Service matches.

### Q22 ⭐⭐ 🟡 How do you test that RLS works before sharing the report (View as role / Test as role)?
**Asked at:** commonly asked; RLS reports exist for Deloitte USI and Cognizant (Q1), but testing is not reported specifically.
**What the interviewer is checking:** Do you verify security with real impersonation, not as the owner?
**Say this in the interview:** "In Desktop I use View as and pick the role, and for dynamic RLS also type a test user's email. In the Service I use the model's Security page, Test as role. I check row counts and totals against known numbers."
**Explain simply:**
- Owners and admins see everything, so normal viewing proves nothing.
- **View as** (Desktop) simulates a role.
- **Test as role** (Service) does the same on the published model.
- Compare each role's totals with expected values.
**Example:** North role should show 3 rows and 113,000 salary; neha@corp.com dynamic should show 2 rows and 110,000; the full model has 368,000.
**Sample data:** Table `Employee`, as in Q1.
**DAX / Steps (not run here):** Desktop: Modeling > Security > View as > tick role (and Other user for dynamic) > OK; a banner shows the active role; Stop viewing. Service: model "..." > Security > role "..." > Test as role.
**Alternative:** Ask a real colleague in the role to confirm what they see.
**Result:** Reproduced with pandas: North 3 rows / 113,000; Dynamic as neha@corp.com 2 rows / 110,000; full 368,000.
**Pandas check:**
```python
for role,m in [("North",emp["Region"]=="North"),("Dynamic as neha@corp.com",emp["ManagerEmail"]=="neha@corp.com")]:
    d=emp[m]; print(role,"-> rows",len(d),"| total salary",d["Salary"].sum())
print("Full model total salary:",emp["Salary"].sum())
```
Output: `North -> rows 3 | total salary 113000`; `Dynamic as neha@corp.com -> rows 2 | total salary 110000`; `Full model total salary: 368000`.
**Version / licensing note:** From memory, unverified; menu names vary by version.
**Edge cases:** Test every role and a user in no role. Test a user in two roles (union).
**Likely follow-ups:** 1) *Why can't I test as Admin?* Admins bypass RLS (Q23). 2) *Test in production?* Test as role on the published model.
**Common mistakes:** Declaring RLS "works" after viewing as the owner.

### Q23 ⭐⭐ 🟡 Does RLS apply to workspace Admins, Members and Contributors? What about Viewers?
**Asked at:** commonly asked (no company-specific report found); RLS is a standard Service topic in prep lists.
**What the interviewer is checking:** Do you know RLS (row-level security, which rows a person may see) is enforced only on people who cannot edit the content?
**Say this in the interview:** "RLS is enforced for Viewers. Admins, Members and Contributors have edit rights on the semantic model (the data model behind a report), so RLS does not restrict them and they see all rows. So I test with View as, and keep business users as Viewers or in an app."
**Explain simply:**
- Viewer: RLS applies. They only see rows their role allows.
- Admin, Member, Contributor: they can edit the model, so RLS is not applied to them.
- Practical effect: putting a manager in the workspace as Contributor "to be helpful" silently removes their restriction.
- Giving someone Build permission on the model or edit access is the other way RLS can be bypassed (see Q39).
**Example:** An HR report has 6 employees; HRBP Priya has a role limiting her to her 3. As Viewer she sees 3. As Contributor she sees all 6.
**DAX / Steps:** No measure. (Not run here: Service UI.) Workspace > Manage access > check the role column; change to Viewer; then dataset > Security to confirm role membership.
**Alternative:** Publish an app and give people app access only; app users behave as Viewers.
**Result:** Not a calculation; nothing to reproduce.
**Version / licensing note:** from memory, unverified (learn.microsoft.com could not be fetched from this session). The Part 7 sources file records "RLS applies only to Viewers" from the Microsoft Learn RLS page fetched earlier; I did not re-read it.
**Edge cases:** A person who is Viewer in the workspace but also has Build permission on the model can query it differently; check each route.
**Likely follow-ups:** 1) *How do you test?* View as role. 2) *Can a Member be restricted?* Not by RLS; demote to Viewer.
**Common mistakes:** Testing RLS while logged in as workspace Admin and concluding "RLS is broken".

### Q24 ⭐⭐ 🟡 How do you add users to an RLS role, and can you use groups?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know role membership is assigned in the Service, and that groups scale better than names?
**Say this in the interview:** "After publishing, I open the semantic model's Security page, pick the role, and add people or security groups. I prefer groups so joiners and leavers are managed by IT, not by me."
**Explain simply:**
- A role is a named rule (for example "HRBP-West" with a DAX filter). Membership says who gets that rule.
- You can add individual emails or Microsoft Entra security groups (Entra = Microsoft's company sign-in directory), and Microsoft 365 groups and mail-enabled security groups, from memory. Plain distribution lists are not supported.
- One person can be in many roles; they get the union (they see rows allowed by any of their roles).
- With dynamic RLS (Q20) you often need only one role, because the data table decides who sees what.
**Example:** 10 HR business partners in group "HRBP-All" assigned to one dynamic role: adding the 11th HRBP to the group is enough.
**DAX / Steps:** (Not run here.) Service > workspace > semantic model "..." > Security > pick role > type names or group > Add > Save.
**Alternative:** Skip groups by using a Security table (UserEmail, Region) with dynamic RLS and one role.
**Result:** Not a calculation.
**Version / licensing note:** from memory, unverified; group types supported should be confirmed on the Learn RLS page.
**Edge cases:** Nested groups and recently added members can take time to take effect; users with no role membership see nothing (Viewer) once RLS exists.
**Likely follow-ups:** 1) *Can a user be in two roles?* Yes, union. 2) *Where is it done?* Service, not Desktop.
**Common mistakes:** Adding a distribution list; forgetting to Save; adding people in Desktop (View as only simulates).

### Q25 ⭐⭐ 🟡 What are RLS limits: does it hide columns, and does it work with Import and DirectQuery?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know RLS filters rows only, not columns?
**Say this in the interview:** "RLS hides rows, never columns. To hide a column like Salary I use object-level security (OLS). RLS works with Import and DirectQuery; for a live connection to Analysis Services, RLS is defined in the source model."
**Explain simply:**
- RLS adds a filter on a table so unwanted rows vanish. Every column of the remaining rows is still visible.
- Hide a sensitive column: OLS (needs external tools such as Tabular Editor, from memory) or just do not load it.
- Import = data copied into Power BI; DirectQuery = each click queries the source. RLS works for both.
- RLS is not a defence against someone who can edit or has Build rights (Q23).
**Example:** Priya sees only her 3 employees but still sees their Salary column. If salary must be hidden, use OLS or a separate model.
**DAX / Steps:** No measure; see Q19 and Q20 for filters. (Not run here.)
**Alternative:** Separate reports or models for sensitive data.
**Result:** Not a calculation.
**Version / licensing note:** from memory, unverified; check the Learn RLS page limits section.
**Edge cases:** DirectQuery with single sign-on can use source-side security instead; some calculations (for example hiding totals) can leak the existence of other rows through averages.
**Likely follow-ups:** 1) *OLS vs RLS?* Columns/tables vs rows (Q55). 2) *Live connection?* Defined in SSAS/Azure AS.
**Common mistakes:** Believing RLS secures salary columns.

### Q26 ⭐⭐ 🟡 Does RLS defined in Desktop carry over when you publish to the Service? Where do you assign users?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know roles travel with the model but members do not?
**Say this in the interview:** "Yes, the roles and their DAX filters are saved in the model and published with it. But I must assign users to each role in the Service afterwards; Desktop has no user list."
**Explain simply:**
- Define: Desktop > Modeling > Manage roles. Roles and filters are part of the .pbix.
- Members are added only in the Service (Q24).
- Re-publishing keeps the members, as far as I recall; a changed role name may need re-assigning (unverified).
- Until you assign users, nobody (Viewer) is restricted properly: they are either blocked or you rely on edit rights.
**Example:** You build role "HRBP" in Desktop, publish, and then add group "HRBP-All" in the Service.
**DAX / Steps:** (Not run here.) Desktop: Modeling > Security > Manage roles > Create > pick table > filter DAX > Save. Then Publish; in Service: model "..." > Security.
**Alternative:** Use Tabular Editor or XMLA to script roles (from memory).
**Result:** Not a calculation.
**Version / licensing note:** from memory, unverified. Desktop is Windows-only per the Part 7/notes research (not re-checked).
**Edge cases:** View as in Desktop is only a simulation of the role.
**Likely follow-ups:** 1) *Do you lose users on republish?* Normally no. 2) *Who can assign?* Owner/editors of the model.
**Common mistakes:** Assuming "I tested in Desktop, so users are set".

### Q27 ⭐⭐ 🟡 How do you set up a refresh for a dataset that uses an on-premises SQL Server or Excel file on a shared drive?
**Asked at:** commonly asked (no company-specific report found); gateways and refresh are named as recurring topics in `research/interview_processes.md`.
**What the interviewer is checking:** Do you know the cloud Service cannot reach your office network without a gateway?
**Say this in the interview:** "I install a standard on-premises data gateway on an always-on machine, sign in, register it, then in the Service map the dataset's data source to the gateway, enter credentials, and set the schedule."
**Explain simply:**
- Gateway = a small Microsoft program that sits inside your network and carries data out to the Service, using outbound connections only.
- SQL Server and shared-drive (UNC path like \\server\hr\file.xlsx) files both need it. Cloud sources (SharePoint, Azure SQL) usually do not.
- The gateway machine must reach the source and have the same file path access.
- Personal mode is for one person's testing; standard mode is for teams (Q15).
**Example:** Monthly attendance.xlsx on \\hrserver\share. Gateway runs on that server; refresh at 7 am daily.
**DAX / Steps:** (Not run here.) 1) Install gateway (standard mode), sign in, name it. 2) Service > Settings (gear) > Manage connections and gateways > add data source (SQL Server or File) with credentials. 3) Dataset > Settings > Gateway and cloud connections > map to the gateway. 4) Data source credentials > Sign in. 5) Scheduled refresh > On > frequency and time > Apply.
**Alternative:** Move the file to OneDrive/SharePoint to avoid a gateway (Q32).
**Result:** Not a calculation.
**Version / licensing note:** from memory, unverified. The sources file records standard/personal/VNet gateway types and outbound connections from the Learn gateway page, fetched earlier.
**Edge cases:** Gateway PC off or asleep = failed refresh; the data source name in Desktop must match exactly.
**Likely follow-ups:** 1) *Gateway cluster?* Several gateways for failover (Q46). 2) *Who needs a licence?* Publishing/scheduling needs Pro or higher (from memory).
**Common mistakes:** Installing the gateway on a laptop that sleeps; mismatched file path or server name.

### Q28 ⭐⭐ 🟡 How do you configure data source credentials and privacy levels for a dataset in the Service?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you fix the "credentials invalid" refresh error and explain privacy levels?
**Say this in the interview:** "In the dataset's settings I open Data source credentials, choose the authentication type, and sign in. Privacy levels (Public, Organizational, Private) tell Power BI how carefully it must keep sources apart when combining them."
**Explain simply:**
- Credentials = the login the Service uses to read the source (Basic username/password, OAuth2 = sign in with your account, Windows).
- Privacy level: Private = never share with other sources; Organizational = share only within the company; Public = open data.
- When two sources are merged in one query, mismatched levels can block folding or raise a "formula firewall" error (from memory).
- Credentials expire (password changes), so refresh fails until re-entered.
**Example:** HR table from SQL (Organizational) merged with a public holiday list (Public): both are fine together; setting SQL to Private may slow or block combining.
**DAX / Steps:** (Not run here.) Workspace > semantic model "..." > Settings > Data source credentials > Edit credentials > choose auth method and Privacy level setting > Sign in. Behind a gateway: Manage connections and gateways.
**Alternative:** Use a service account or organisational dataflow so personal passwords are not tied to the model.
**Result:** Not a calculation.
**Version / licensing note:** from memory, unverified.
**Edge cases:** Ignore privacy levels is possible in Desktop options but not recommended; OAuth tokens expire periodically.
**Likely follow-ups:** 1) *Who can edit credentials?* The dataset owner (use Take over). 2) *Why does it fail after a password change?* Stored login is stale.
**Common mistakes:** Setting everything Public to silence errors; using a personal account that later leaves the company.

### Q29 ⭐⭐ 🟡 What are RangeStart and RangeEnd in incremental refresh, and what rules must they follow?
**Asked at:** commonly asked (no company-specific report found); incremental refresh is listed as a recurring topic in `research/interview_processes.md`.
**What the interviewer is checking:** Do you know the exact parameter names, type and filter pattern?
**Say this in the interview:** "RangeStart and RangeEnd are two Date/Time parameters, spelled exactly like that. I filter the date column with >= RangeStart and < RangeEnd, and the Service rewrites them for each partition."
**Explain simply:**
- Parameter = a named value you can change without editing the query. Power BI fills these in for each time slice (partition = a chunk of the table).
- Rules (from the Part 7 sources file, Microsoft Learn incremental refresh page, not re-read): names RangeStart and RangeEnd (case-sensitive); type Date/Time; filter on one date column; one end inclusive, one exclusive.
- Using >= and < on opposite ends stops a row on the boundary being loaded twice or never.
- The filter should fold (be translated to SQL by the source) for speed (Q60).
**Example:** RangeStart = 1 Oct 2026, RangeEnd = 1 Nov 2026.
**Sample data:** Table Sales (OrderDate, Amount)

| OrderID | OrderDate | Amount |
|---|---|---|
| 5 | 2026-10-01 | 200 |
| 6 | 2026-10-31 | 80 |
| 7 | 2026-11-01 | 60 |
| 8 | 2026-11-02 | 70 |

**DAX / Steps:** (Not run here: Power Query M.)
```m
= Table.SelectRows(Source, each [OrderDate] >= RangeStart and [OrderDate] < RangeEnd)
```
**Alternative:** Use an integer date key (YYYYMMDD) with a function that converts parameters, for sources without date types (from memory).
**Result:** Reproduced with pandas: October window returns OrderIDs 5 and 6, 2 rows, amount 280. Order 7 (1 Nov) falls in the next window; using <= RangeEnd would return 3 rows and double load order 7.
**Pandas check:**
```python
w=s[(s.OrderDate>=rs)&(s.OrderDate<re)]   # rs=2026-10-01, re=2026-11-01
print(len(w), w.Amount.sum())             # 2 280
print(len(s[(s.OrderDate>=rs)&(s.OrderDate<=re)]))  # 3 (wrong rule)
```
**Version / licensing note:** from memory, unverified here; the sources file says incremental refresh is supported on Pro and above (page dated 2025-09, updated 2026-07).
**Edge cases:** Wrong parameter type/name means the policy cannot be created; a column with time zone shifts can mis-assign boundary rows.
**Likely follow-ups:** 1) *Can users change them?* They only matter at refresh; Desktop uses them for the preview slice. 2) *Why exclusive end?* Avoid duplicates.
**Common mistakes:** Using >= on both ends; Text-type parameters; filtering a non-date column.

### Q30 ⭐⭐ 🟡 How do you set up incremental refresh in Power BI Desktop for a sales table?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you walk through the sequence: parameters, filter, policy, publish?
**Say this in the interview:** "I create RangeStart and RangeEnd, filter the OrderDate column with them, load, then right-click the table, Incremental refresh, set how many years to store and how many days to refresh, and publish. The first Service refresh builds all partitions; later ones touch only recent ones."
**Explain simply:**
- Incremental refresh = refresh only recent data instead of reloading the whole table every night.
- Store rows from last N years; refresh rows from last M days; older partitions stay untouched.
- It is configured in Desktop but works only after publishing and refreshing in the Service.
- After publish you cannot download the PBIX again from the Service (from the sources file; unverified by me).
**Example:** Sales has 5 years (about 40 million rows). Policy: store 3 years, refresh last 10 days. Nightly refresh reloads about 10 days of rows.
**Sample data:** Table Sales (above) with months: pandas count per month shows 2025-01:1, 2025-12:1, 2026-01:1, 2026-09:1, 2026-10:2, 2026-11:2; "refresh 1 month" would reload only the current-month partition.
**DAX / Steps:** (Not run here.)
1. Home > Transform data > Manage parameters > New: RangeStart (Date/Time, current value some start date); RangeEnd likewise.
2. Filter OrderDate: Date filters > Custom filter, is after or equal to RangeStart and is before RangeEnd.
3. Close & Apply.
4. Model/Data pane: right-click Sales > Incremental refresh and real-time data.
5. Switch on; set Archive data starting 3 years, Incrementally refresh 10 days.
6. Optional: Detect data changes (Q53), Only refresh complete days (Q54).
7. Publish; in Service run first refresh.
**Alternative:** Partition manually through XMLA (Premium, advanced).
**Result:** Reproduced with pandas only the partition count by month (above); the policy itself is not run here.
**Pandas check:**
```python
s["Month"]=s.OrderDate.dt.to_period("M"); print(s.groupby("Month").size())
# 2025-01 1, 2025-12 1, 2026-01 1, 2026-09 1, 2026-10 2, 2026-11 2
```
**Version / licensing note:** from memory, unverified; sources file: Pro, PPU, Premium and Fabric support it, refresh limits 2 h (shared) / 5 h (Premium).
**Edge cases:** Source must support query folding, else every partition downloads everything (Q60).
**Likely follow-ups:** 1) *First refresh slow?* Yes, it builds all history. 2) *Change policy later?* Republish.
**Common mistakes:** Forgetting the filter step; expecting Desktop to partition data.

### Q31 ⭐⭐ 🟡 What is a Power BI app, and how do you publish one from a workspace to business users?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know apps are the packaged way to give business users a read-only experience?
**Say this in the interview:** "An app bundles selected reports and dashboards from a workspace into a clean, read-only package for consumers. I choose the content, set navigation and audience, then publish it and share the link."
**Explain simply:**
- Workspace = the team's working area; app = the polished version for readers.
- Users get updates only when you update the app, so you can keep editing safely.
- Viewers inside an app cannot edit; RLS applies (Q23).
- Audiences let different groups see different content (Q37).
**Example:** HR analytics workspace publishes "HR Insights" app to 40 managers.
**DAX / Steps:** (Not run here.) Workspace > Create app (or Update app) > Setup (name, description) > Content (add items) > Audience (add people/groups, permissions) > Publish app > copy link.
**Alternative:** Share individual reports, which is harder to manage at scale.
**Result:** Not a calculation.
**Version / licensing note:** from memory, unverified; sources file: up to 25 audiences, Microsoft Learn "create and distribute apps" page, updated 2026-10, fetched earlier. Consumers generally need Pro or PPU unless the workspace is on Fabric/Premium capacity with enough size (see Q65).
**Edge cases:** Audience changes need an app update to take effect.
**Likely follow-ups:** 1) *App vs dashboard?* Q10. 2) *How do users get it?* Link or AppSource-style apps list.
**Common mistakes:** Sharing the workspace instead of the app.

### Q32 ⭐⭐ 🟡 How do you make a Power BI report refresh data automatically if the source is a file on OneDrive or SharePoint?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know cloud files need no gateway and can refresh automatically?
**Say this in the interview:** "I load the file in Desktop using its OneDrive or SharePoint web URL, publish, and then either schedule refresh or rely on OneDrive's automatic check about every hour."
**Explain simply:**
- Cloud storage is reachable by the Service directly, so no gateway.
- Use the web link (not a local synced path) in Get data > Web or SharePoint folder.
- Power BI checks OneDrive for work/school roughly hourly for changes (from memory, unverified); scheduled refresh adds fixed times.
- Credentials: sign in with OAuth2 in dataset settings.
**Example:** HR keeps attendance.xlsx in SharePoint; Monday edits appear in the report by Monday afternoon.
**DAX / Steps:** (Not run here.) Desktop: Home > Get data > Web > paste URL (remove the ?web=1 tail) > Publish. Service: dataset Settings > Data source credentials > OAuth2 > Sign in; Scheduled refresh > On.
**Alternative:** Get data > Excel workbook and import a local path, which needs a gateway.
**Result:** Not a calculation.
**Version / licensing note:** from memory, unverified.
**Edge cases:** Moving or renaming the file breaks the link; personal OneDrive behaves differently from work OneDrive.
**Likely follow-ups:** 1) *Why not a local path?* Needs gateway. 2) *Is it instant?* No.
**Common mistakes:** Using the local synced path; leaving the ?web=1 suffix.

### Q33 ⭐⭐ 🟡 A user says they cannot see your report in the Service. What do you check?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** A calm, ordered troubleshooting approach.
**Say this in the interview:** "I check access first: is it shared with them or are they in the workspace or app audience; then their licence; then RLS membership; then whether the model or report was actually published or the link is correct."
**Explain simply:**
- Access: workspace role, direct share, or app audience (Q37).
- Licence: Pro/PPU needed unless the content is in a large enough Fabric/Premium capacity (Q65).
- RLS: a Viewer not in any role may see an empty or error visual.
- Link/tenant: right account (personal vs work), guest user issues (Q63), app updated after audience changes?
- Source permission: DirectQuery with single sign-on needs the user to have source access.
**Example:** A new HRBP sees blanks: she was never added to the "HRBP" role. Fix: add her group.
**DAX / Steps:** (Not run here.) Workspace > Manage access; report > Manage permissions; model > Security; app > Update app > Audience.
**Alternative:** Ask them to share a screenshot of the error and use "View as" for their email.
**Result:** Not a calculation.
**Version / licensing note:** from memory, unverified.
**Edge cases:** Sensitivity labels or conditional access policies can block access.
**Likely follow-ups:** 1) *Blank not error?* RLS. 2) *Link opens login loop?* Wrong account/tenant.
**Common mistakes:** Adding them to the workspace as Contributor, which bypasses RLS.

### Q34 ⭐⭐ 🟡 Your refresh is slow or times out. What do you check, and what are the time limits on Pro and Premium?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you reduce refresh work and name the limits?
**Say this in the interview:** "Limits per the docs I last saw are 2 hours on shared capacity (Pro) and 5 hours on Premium. I check query folding, remove unused columns and rows, use incremental refresh, avoid heavy transformations, and check the source and gateway load."
**Explain simply:**
- Timeout = refresh cancelled when it runs past the limit (2 h shared, 5 h Premium; sources file, Learn pages dated 2026, I could not re-fetch).
- Query folding = the source database does the filtering/joining, much faster than Power BI doing it.
- Big wins: incremental refresh, fewer columns, no duplicate queries, staging data in a dataflow.
- Check the gateway machine (CPU/RAM) and slow source queries; schedule outside peak hours.
**Example:** 90-minute refresh with 40 columns; removing 25 unused columns and adding incremental refresh brings it to about 10 minutes (illustrative figures).
**DAX / Steps:** (Not run here.) Service > model > Settings > Refresh history to see duration and error; Desktop: right-click a step > View native query (enabled means folding).
**Alternative:** Switch to DirectQuery or split a large model.
**Result:** Not a calculation.
**Version / licensing note:** from memory, unverified; 2 h / 5 h limits recorded in the sources file; confirm before quoting.
**Edge cases:** Calculated columns and tables are computed during refresh and add time.
**Likely follow-ups:** 1) *Quick win?* Remove columns. 2) *Premium bigger?* Longer limit, more refreshes.
**Common mistakes:** Adding more refresh times instead of fixing the query.

### Q35 ⭐⭐ 🟡 Who gets an email when a scheduled refresh fails, and how can you change notifications?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know refresh failure alerts are configurable, not magic?
**Say this in the interview:** "The dataset owner gets a failure email by default. In Scheduled refresh settings I can add other contacts such as a team mailbox, and turn the notification on or off."
**Explain simply:**
- Owner = the person who published or took over the dataset.
- In the refresh settings you can tick "Send refresh failure notification emails to me" and add extra email addresses (from memory; wording unverified).
- Power BI may also disable refresh after repeated failures or inactivity (Q47).
**Example:** Add hr-analytics@company.com so the whole team sees the 6 am failure.
**DAX / Steps:** (Not run here.) Model > Settings > Scheduled refresh > Refresh failure notifications > tick owner box > add emails > Apply.
**Alternative:** Power Automate flow or Premium refresh APIs for custom alerts (from memory).
**Result:** Not a calculation.
**Version / licensing note:** from memory, unverified; sources file says failure emails are in the Learn refresh page (updated 2026-10), not re-read.
**Edge cases:** If the owner leaves, notifications go to a dead mailbox; Take over the dataset.
**Likely follow-ups:** 1) *Can workspace admins get them?* Add them as contacts. 2) *Success emails?* Not by default.
**Common mistakes:** Relying on a personal inbox.

### Q36 ⭐⭐ 🟡 Your manager asks which reports nobody opens anymore. How do you find out in the Power BI Service?
**Asked at:** commonly asked (no company-specific report found); a gap-fill question from the sources file.
**What the interviewer is checking:** Do you know the usage metrics report exists?
**Say this in the interview:** "I open the workspace's usage metrics report, which shows views per report over the last 30 days and lists unused reports; I note any with zero views and confirm with owners before archiving."
**Explain simply:**
- Usage metrics = a built-in report on views, viewers and trends.
- Per sources file (Learn usage-metrics page, dated 2025-12, updated 2026-05): Admin/Member/Contributor with Pro or PPU can run it, an admin tenant setting must allow it, it covers the last 30 days, it is not supported in My workspace, and the page was labelled preview. Not re-read by me.
- Beyond 30 days you need the Admin audit log (Q56).
**Example:** 5 reports; views in last 30 days: Attendance 3, Attrition 2, Headcount 1, Payroll 0, Hiring Funnel 0 → candidates to retire: Payroll, Hiring Funnel.
**Sample data:** Table ViewLog (one row per view)

| Report | Views30d |
|---|---|
| Attrition | 1 |
| Attrition | 1 |
| Headcount | 1 |
| Attendance | 1 |
| Attendance | 1 |
| Attendance | 1 |

**DAX / Steps:** (Not run here.) Workspace list > report row "..." > View usage metrics (or workspace > "..." > Usage metrics).
**Alternative:** Admin portal > Audit logs / Microsoft Purview search for ViewReport events.
**Result:** Reproduced with pandas: Attendance 3, Attrition 2, Headcount 1, Payroll 0, Hiring Funnel 0; unused = Payroll, Hiring Funnel.
**Pandas check:**
```python
v=log.groupby("Report").size().reindex(rep,fill_value=0); print(v[v==0].index.tolist())
# ['Payroll', 'Hiring Funnel']
```
**Version / licensing note:** from memory, unverified; see sources file notes above.
**Edge cases:** Seasonal reports (year-end payroll) look unused in a quiet month.
**Likely follow-ups:** 1) *Longer history?* Audit log. 2) *Who can run it?* Editors with Pro/PPU.
**Common mistakes:** Deleting on 30 days of data without asking owners.

### Q37 ⭐⭐ 🟡 You publish one app for HR, finance and sales teams. How do audiences let each team see different reports?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know one app can show different content per group?
**Say this in the interview:** "In the app's Audience tab I create an audience per team, show or hide each report for that audience, and add the team's security group. Same app, different view."
**Explain simply:**
- Audience = a group of people with a defined set of visible items.
- Per sources file (Learn page, updated 2026-10): up to 25 audiences, with a caveat that hidden content may still be reachable by direct link if the person has access to it elsewhere. Not re-read by me.
- Audiences control navigation, not data rows; use RLS for row restrictions.
**Example:** Audience "HR": Attrition, Headcount. "Finance": Payroll. "Sales": Pipeline.
**DAX / Steps:** (Not run here.) Workspace > Update app > Audience > New audience > name > hide/show items > add groups > Update app.
**Alternative:** Three separate apps (more upkeep).
**Result:** Not a calculation.
**Version / licensing note:** from memory, unverified (25 audiences from the sources file).
**Edge cases:** People in multiple audiences see the union.
**Likely follow-ups:** 1) *Is it security?* Not alone. 2) *Limit?* 25.
**Common mistakes:** Using audiences to protect salary data.

### Q38 ⭐⭐ 🔴 How would you design RLS for an HR dashboard where each HR business partner sees only their own employees and the CHRO sees everyone?
**Asked at:** commonly asked (no company-specific report found); RLS appears in Deloitte USI/Cognizant/Wipro-type reports in `research/interview_processes.md` (single unverified anecdotes).
**What the interviewer is checking:** Dynamic RLS design plus handling the "see everything" role.
**Say this in the interview:** "I put each employee's HRBP email on the Employees table and create a role filtering it to USERPRINCIPALNAME(). For the CHRO I create a second role with no filter and make sure HRBPs are not in it. I test with View as and keep users as Viewers."
**Explain simply:**
- Dynamic RLS = one rule that uses the logged-in person's email, instead of one role per person.
- HRBP role: [HRBPEmail] = USERPRINCIPALNAME().
- CHRO role: a role with no table filter, so all rows pass. Be careful: roles combine as a union.
- Never make HRBPs or the CHRO Contributors (Q23, Q39).
**Example:** 6 employees; Priya's 3 total salary 150, Arun's 3 total 195, CHRO sees 6 and 345.
**Sample data:** Table Employees

| EmpID | Name | Dept | HRBPEmail | Salary |
|---|---|---|---|---|
| 1 | Asha | Sales | priya@co.com | 50 |
| 2 | Ravi | Sales | priya@co.com | 60 |
| 3 | Meena | IT | arun@co.com | 70 |
| 4 | Kiran | IT | arun@co.com | 80 |
| 5 | Sana | Ops | priya@co.com | 40 |
| 6 | Dev | Ops | arun@co.com | 45 |

**DAX / Steps:** (Not run here.)
```dax
-- Role "HRBP", table filter on Employees
[HRBPEmail] = USERPRINCIPALNAME()
-- Role "CHRO": no filter expression
```
**Alternative:** A Security table (UserEmail, HRBPEmail) related to Employees, with CHRO listed once per HRBP, for many-to-many access.
**Result:** Reproduced with pandas: priya@co.com 3 rows, 150; arun@co.com 3 rows, 195; CHRO 6 rows, 345.
**Pandas check:**
```python
for u in ["priya@co.com","arun@co.com"]:
    r=emp[emp.HRBPEmail==u]; print(u,len(r),r.Salary.sum())
print("CHRO",len(emp),emp.Salary.sum())
# priya 3 150 / arun 3 195 / CHRO 6 345
```
**Version / licensing note:** from memory, unverified (RLS Viewer-only rule per Q23).
**Edge cases:** An HRBP with an email alias or case difference; employees with no HRBP are visible to nobody (except CHRO); a user in both roles sees everything.
**Likely follow-ups:** 1) *Salary hidden?* OLS (Q25). 2) *Hierarchy?* Q62.
**Common mistakes:** Hard-coding emails per role; adding the CHRO to the HRBP role.

### Q39 ⭐⭐ 🔴 You built RLS but a user in a Contributor role still sees all data. Why, and how do you fix it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know the Viewer-only rule.
**Say this in the interview:** "RLS does not apply to people with edit rights, and Contributor can edit. I would change them to Viewer, or give them access through an app, and also check for other roles or Build permission."
**Explain simply:**
- Contributor can edit content, so RLS is not enforced for them.
- Fix: change the workspace role to Viewer, or remove them and distribute through an app audience.
- Also check: are they in a second role with no filter (union), or have Build on the model?
- Confirm with View as role.
**Example:** Ravi, a Contributor, sees all 6 employees (345 salary). After switching to Viewer in role HRBP he sees 3.
**DAX / Steps:** (Not run here.) Workspace > Manage access > change role to Viewer; model > Security to verify roles.
**Alternative:** Keep the sensitive model in a separate restricted workspace.
**Result:** Not a calculation.
**Version / licensing note:** from memory, unverified.
**Edge cases:** Admins and Members behave the same way.
**Likely follow-ups:** 1) *Why is this by design?* Editors can change the model anyway. 2) *Can I force it?* Use Viewer.
**Common mistakes:** Debugging the DAX when the cause is the role.

### Q40 ⭐ 🟢 What is the Power BI mobile app, and how do you make a report mobile friendly?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic awareness of mobile layout.
**Say this in the interview:** "It is Microsoft's phone and tablet app to view reports. In Desktop I design a separate phone layout from the View tab so visuals fit a portrait screen."
**Explain simply:**
- Mobile app: iOS, Android; view and interact with published content.
- Mobile layout = a portrait canvas where you drag existing visuals into a tall arrangement.
- Keep few visuals, big cards, simple slicers.
**Example:** HR head checks attrition card and a trend line on the phone.
**DAX / Steps:** (Not run here.) Desktop: View > Mobile layout > drag visuals onto the phone canvas > Publish.
**Alternative:** Build dedicated mobile-friendly dashboard tiles in the Service.
**Result:** Not a calculation.
**Version / licensing note:** from memory, unverified.
**Edge cases:** Without a mobile layout, the desktop layout shrinks.
**Likely follow-ups:** 1) *Offline?* Limited. 2) *Free?* App is free; content needs access.
**Common mistakes:** Cramming ten visuals on the phone canvas.

### Q41 ⭐ 🟢 What are subscriptions and alerts in the Power BI Service?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know push options for insights?
**Say this in the interview:** "A subscription emails a snapshot of a report or dashboard on a schedule. An alert notifies when a dashboard tile value crosses a threshold."
**Explain simply:**
- Subscription: scheduled email with a picture and a link.
- Alert: set on card, gauge or KPI tiles of a dashboard, with an "above/below" limit.
- Both depend on data being fresh.
**Example:** Alert when attrition card goes above 12%; subscription every Monday 8 am.
**DAX / Steps:** (Not run here.) Report > Subscribe to report > Add > frequency; dashboard tile "..." > Manage alerts > Add rule.
**Alternative:** Power Automate flow on data alert.
**Result:** Not a calculation.
**Version / licensing note:** from memory, unverified; subscriptions need Pro/PPU or capacity (unverified).
**Edge cases:** Alerts check when data refreshes.
**Likely follow-ups:** 1) *Alerts on reports?* Tiles only (from memory). 2) *Others' subscriptions?* Some need rights.
**Common mistakes:** Expecting alerts without a refresh schedule.

### Q42 ⭐ 🟢 What does Export to Excel / Analyze in Excel do, and who can use it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the difference between exporting data and live connecting.
**Say this in the interview:** "Export to Excel downloads the visual's data as a file, a static copy. Analyze in Excel opens Excel connected live to the semantic model so you can build PivotTables on it."
**Explain simply:**
- Export: CSV/xlsx of visual data, limited by admin settings and RLS.
- Analyze in Excel: live PivotTable; needs Build permission on the model (from memory) and Excel desktop.
- Admins can disable exports.
**Example:** An analyst builds an attendance PivotTable from the published model.
**DAX / Steps:** (Not run here.) Visual "..." > Export data; or report > Export > Analyze in Excel.
**Alternative:** Paginated reports for formatted exports.
**Result:** Not a calculation.
**Version / licensing note:** from memory, unverified.
**Edge cases:** Exports respect RLS for Viewers.
**Likely follow-ups:** 1) *Row limit?* Exists, unverified. 2) *Mac?* Windows Excel desktop typically.
**Common mistakes:** Treating export as live data.

### Q43 ⭐ 🟡 What is the difference between Publish to web and Embed (secure) a report, and why is Publish to web risky?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Data-leak awareness.
**Say this in the interview:** "Publish to web creates a public link anyone on the internet can open, no sign-in, so it must never carry confidential data like HR. Embed (secure) requires sign-in and respects permissions and RLS."
**Explain simply:**
- Publish to web = public; the link can be shared or found.
- Secure embed = in SharePoint/Teams or portals for signed-in users.
- Many companies disable Publish to web in the tenant.
**Example:** Putting an employee salary report on Publish to web would expose all 6 rows to anyone.
**DAX / Steps:** (Not run here.) File > Embed report > Website or portal (public) vs SharePoint Online / Teams (secure).
**Alternative:** Share an app with named users.
**Result:** Not a calculation.
**Version / licensing note:** from memory, unverified.
**Edge cases:** RLS does not apply to Publish to web.
**Likely follow-ups:** 1) *Can you revoke?* Yes, admin can delete embed codes. 2) *Use case?* Public open data.
**Common mistakes:** Using it for internal dashboards.

### Q44 ⭐ 🟡 What are dataflows in the Power BI Service, and when would you use one?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand reusable shared data prep.
**Say this in the interview:** "A dataflow is Power Query running in the cloud, storing cleaned tables that many datasets can reuse. I use it when several reports need the same prepared employee or calendar table."
**Explain simply:**
- Power Query = tool for cleaning data. A dataflow holds those steps online with its own refresh.
- Benefits: one cleaning logic, less load on the source, shared across reports.
- Needs Pro or higher (from memory); Fabric adds newer Dataflow Gen2.
**Example:** A clean Employee master used by attrition, payroll and headcount reports; fix once, all update.
**DAX / Steps:** (Not run here.) Workspace > New > Dataflow > Define new tables > Power Query online > Save & close > refresh > in Desktop Get data > Dataflows.
**Alternative:** Do the cleaning in the source database or a data warehouse.
**Result:** Not a calculation.
**Version / licensing note:** from memory, unverified.
**Edge cases:** Dataflows need their own refresh and gateway for on-premises sources.
**Likely follow-ups:** 1) *Dataflow vs dataset?* Prep vs model. 2) *Gen2?* Fabric version.
**Common mistakes:** Duplicating the same cleaning in every report.

### Q45 ⭐ 🟡 What are deployment pipelines (Development, Test, Production), and who needs which licence?
**Asked at:** Commonly asked (no company-specific report found); the Part 7 sources file lists it only as a one-star differentiator.
**What the interviewer is checking:** Do you know how a team moves reports safely from build to live without editing the live copy?
**Say this in the interview:** "A deployment pipeline links up to three workspaces, Development, Test and Production. I build in Dev, promote to Test for checking, then to Production. Deployment rules swap things like the database server per stage, so the live report is never edited directly."
**Explain simply:**
- Each stage is a normal workspace (a shared folder in the Service). The pipeline compares them and copies content (reports, semantic models) forward.
- **Deployment rules** change a data source or parameter per stage, e.g. Dev points at a small test database, Production at the real HR database.
- Licence: the sources disagreed and I could not confirm it. My understanding: workspaces must sit on paid capacity (Premium, PPU or Fabric) and the person deploying needs a Pro/PPU licence plus Admin rights on the workspaces. Treat it as "check Microsoft's page before quoting".
**Example:** HR analyst builds the "Attrition Dashboard" in Dev, the HR head signs off in Test, then one click pushes it to Production for 200 viewers.
**DAX / Steps:** Not run here (no Power BI); click-path from memory.
1. Service > **Deployment pipelines** (left nav) > **Create pipeline**.
2. Assign a workspace to each stage.
3. **Deploy to test**, then **Deploy to production**; set **Deployment rules** (the lightning-bolt/rules icon) for data source and parameters.
**Alternative:** Without pipelines: keep three workspaces and republish the same PBIX from Desktop to each, changing parameters by hand.
**Version / licensing note:** From memory, unverified (learn.microsoft.com is not reachable from this session). Licence requirement flagged as unconfirmed in the sources file.
**Edge cases:** Credentials usually need re-entering after the first deploy; rules apply only for items that have that data source.
**Likely follow-ups:**
- *Can Desktop do this?* No, it is a Service feature.
- *What if Test and Prod differ?* The pipeline shows a "different" marker per item.
**Common mistakes:** Editing Production directly; forgetting rules so Test points to live data.

### Q46 ⭐ 🟡 What is a gateway cluster, and why is it used?
**Asked at:** Commonly asked (no company-specific report found); gateways are listed in interview_processes.md as a recurring service-MNC topic.
**What the interviewer is checking:** Do you understand high availability for on-premises refresh?
**Say this in the interview:** "A gateway is software on a company machine that lets the cloud Service reach on-premises data. A cluster is two or more gateway installations grouped together, so if one machine is down, another takes over and scheduled refreshes still run."
**Explain simply:**
- The gateway (standard mode) is a bridge from the Service to, say, an on-premises SQL Server holding payroll data.
- A single gateway machine is a single point of failure: patching or a crash means failed refreshes.
- In a cluster, the first install is the primary; later members are added using the same recovery key. Requests go to the primary and fail over to others; load balancing across members can also be turned on.
- Personal-mode gateways cannot be clustered.
**Example:** Two servers host the gateway; at 2 AM server A is rebooting, server B refreshes the payroll semantic model on time.
**DAX / Steps:** Not run here; from memory.
1. Install the standard gateway on a second machine.
2. In the installer choose **Add to an existing gateway cluster** and enter the primary's name and the **recovery key**.
3. Service > Settings > **Manage connections and gateways** to see members and balancing options.
**Alternative:** Use a cloud source or a VNet gateway so no on-premises machine is needed.
**Version / licensing note:** From memory, unverified. The sources file records the standard / personal / VNet gateway split from a fetched Learn page, but clustering was not checked.
**Edge cases:** Members need the same data-source access and software versions; keep them in the same network region.
**Likely follow-ups:**
- *Is a cluster faster?* Only with load balancing on.
- *Lost recovery key?* You cannot add members; migrate or restore needs it.
**Common mistakes:** Thinking a cluster means two separate gateways with different names; losing the recovery key.

### Q47 ⭐ 🟡 Why does the Power BI Service pause a scheduled refresh, and how do you turn it back on?
**Asked at:** Commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know refresh is not "set and forget" and how to troubleshoot silent stops?
**Say this in the interview:** "Power BI disables a schedule when nobody has opened the reports on that semantic model for about two months, to save capacity, and also after repeated consecutive failures. I fix the cause, then re-enable the schedule in the semantic model settings, or just open the report."
**Explain simply:**
- **Inactivity:** the refresh-data page summary in the sources file says refresh pauses after two months with no one visiting the dashboards or reports on it. Failure-based pausing (after several failures in a row) is from memory; I believe it is four, unverified.
- You usually get an email when it happens, if failure notifications are on.
- Fix first (credentials expired, gateway offline), otherwise it will pause again.
**Example:** The "Monthly Headcount" report is used only at quarter end; in a quiet stretch the schedule stops, and the first quarter-end report shows old numbers.
**DAX / Steps:** Not run here; labels may differ.
1. Service > workspace > semantic model **...** > **Settings**.
2. Expand **Refresh**; check the data source credentials/gateway.
3. Turn **Configure a refresh schedule** back on and **Apply**; click **Refresh now** to test.
**Alternative:** Trigger refresh from Power Automate or the REST API instead of the built-in schedule.
**Version / licensing note:** Inactivity rule per the fetched "Data refresh in Power BI" page (cited in the sources file, updated 2026-10); the failure count and menu labels are from memory, unverified.
**Edge cases:** Shared capacity allows 8 scheduled refreshes a day, Premium/PPU/Fabric 48 (per same source, re-check).
**Likely follow-ups:**
- *Who gets the email?* The semantic model owner, plus contacts you add.
**Common mistakes:** Re-enabling the toggle without fixing expired credentials.

### Q48 ⭐ 🟡 How do you refresh a dataset from a data source that changes only on the first of each month?
**Asked at:** Commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you match refresh to the data rhythm instead of wasting capacity?
**Say this in the interview:** "The built-in schedule works by days of the week and times, not by day of the month. So I'd either schedule a daily refresh in the early morning of the days after the first, or, better, use Power Automate with a monthly recurrence trigger and the Refresh a dataset action, and add incremental refresh if the table is large."
**Explain simply:**
- The Service schedule lets you pick days and up to a set number of times a day. There is no "1st of month" option (from memory).
- **Power Automate** (Microsoft's no-code scheduler) can run on the 1st/2nd at, say, 06:00 and call a dataset-refresh action.
- If the source lands late, refresh daily for the first three days: cheap and safe.
- **Incremental refresh** reloads only the latest month (Q53/Q54).
**Example:** HR payroll file lands on the 1st at 11 PM. A flow runs on the 2nd at 6 AM and refreshes the "Payroll" semantic model.
**DAX / Steps:** Not run here.
1. Power Automate > **Create > Scheduled cloud flow**, repeat every 1 month, start on day 2.
2. Add action **Power BI > Refresh a dataset**; choose workspace and semantic model.
3. Optionally add a failure email step.
**Alternative:** Daily schedule on all days with a small query; or call the Enhanced refresh REST API.
**Version / licensing note:** From memory, unverified; Power Automate connectors and licences vary.
**Edge cases:** Month-end falling on weekends; late files; time zone of the flow vs source.
**Likely follow-ups:**
- *Can I refresh when the file arrives?* Yes, trigger the flow from a file-created event.
**Common mistakes:** Refreshing every hour "just in case"; scheduling at midnight before data lands.

### Q49 ⭐ 🟡 What does sensitivity labelling and endorsement (certified, promoted) mean in the Power BI Service?
**Asked at:** Commonly asked (no company-specific report found); listed as a one-star topic in the sources file.
**What the interviewer is checking:** Do you separate data protection (labels) from trust signalling (endorsement)?
**Say this in the interview:** "Sensitivity labels, such as Confidential, come from Microsoft Purview and protect content, carrying along when data is exported. Endorsement is a badge: Promoted says the owner thinks it's ready to reuse; Certified means an authorised reviewer approved it as trusted."
**Explain simply:**
- **Sensitivity label:** a tag set by company policy; it can add restrictions or encryption and follows exports to Excel or PDF.
- **Promoted:** any content owner or editor can tag it.
- **Certified:** only reviewers the admin has authorised; used for official "single source of truth" datasets.
- Fabric also has a "Master data" endorsement (from memory).
**Example:** The "Employee Master" semantic model with salary is labelled **Highly Confidential**, and certified by the HR data team so analysts reuse it.
**DAX / Steps:** Not run here; from memory.
1. Semantic model/report **Settings** > **Endorsement and discovery** > choose **Promoted** or **Certified**.
2. Label: report **File/Settings** > **Sensitivity label**, or the label drop-down in the item's settings.
**Alternative:** Without Purview, use workspace access and RLS to limit access; endorsement is still available.
**Version / licensing note:** From memory, unverified; sensitivity labels need Microsoft Purview Information Protection and admin setup.
**Edge cases:** Labels inherit downstream from semantic model to reports (admin setting).
**Likely follow-ups:**
- *Does Certified restrict access?* No, it is only a signal.
**Common mistakes:** Believing a label or certified badge controls who can see rows.

### Q50 ⭐ 🟡 What is the Large semantic model storage format, and when is it needed?
**Asked at:** Commonly asked (no company-specific report found); gap-fill question, no source shows it asked.
**What the interviewer is checking:** Do you know the size limits and the remedy?
**Say this in the interview:** "It is a setting on a semantic model in Premium, PPU or Fabric capacity that lets it grow beyond the default size cap, up to what the capacity allows. It loads only the data a query needs into memory, and I'd turn it on for very large imported models or very big XMLA writes."
**Explain simply:**
- A semantic model is the data model behind reports (the old word was "dataset").
- Default limits (from memory): about 1 GB for a Pro model, and a larger default cap on capacities. The large format removes the fixed cap so the capacity memory is the limit.
- Needed when the PBIX would exceed the cap, or when partitions refresh slowly.
- It requires paid capacity; Pro-only workspaces do not have it.
**Example:** A 10-year attendance history, 800 million swipe rows, will not fit under the standard cap.
**DAX / Steps:** Not run here; from memory.
1. Workspace must be on Premium/PPU/Fabric capacity.
2. Semantic model **Settings** > **Large semantic model storage format** > **On** > **Apply**.
**Alternative:** Reduce size: remove columns, aggregate, incremental refresh, or Direct Lake/DirectQuery (Q52).
**Version / licensing note:** From memory, unverified; the Pro size figure is commonly cited and unconfirmed in the notes file.
**Edge cases:** Once turned on, it generally cannot be switched back (unverified).
**Likely follow-ups:**
- *Does it speed queries?* Not by itself.
**Common mistakes:** Turning it on instead of removing unused columns.

### Q51 ⭐ 🟡 What is the difference between Build permission and Viewer access on a dataset?
**Asked at:** Commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know viewing a report differs from building new content on its data?
**Say this in the interview:** "Viewer access lets someone open and use reports. Build permission on the semantic model also lets them create their own reports from it, use Analyze in Excel and see the underlying data. Viewers cannot edit anything."
**Explain simply:**
- **Viewer** is a workspace role: read reports, no editing. RLS applies to Viewers (per the RLS page in the sources file); it does not apply to Admin/Member/Contributor.
- **Build** is a permission on the semantic model, given by sharing it, via an app option, or via roles Contributor and above.
- Build holders can pull any table/column they can see; RLS still filters them if they are not workspace editors.
**Example:** An HR business partner has Build on "Headcount Model" to make her own Excel pivot; the CEO is only a Viewer of the dashboard.
**DAX / Steps:** Not run here; from memory.
1. Semantic model **...** > **Manage permissions** > **Add user**.
2. Tick **Allow recipients to build content with the data associated with this semantic model**.
**Alternative:** Give a workspace role of Contributor, which includes build (but also bypasses RLS).
**Version / licensing note:** RLS applies to Viewers: per fetched page in the sources file (RLS with Power BI, 2026-05). Menu wording from memory, unverified.
**Edge cases:** Granting Build to Contributors defeats RLS.
**Likely follow-ups:**
- *Can Build users edit the model?* No.
**Common mistakes:** Making everyone a Member and then wondering why RLS "does not work".

### Q52 ⭐ 🟡 What is Direct Lake mode, and when would a Fabric workspace use it?
**Asked at:** Commonly asked (no company-specific report found); a one-star differentiator in the sources file, Direct Lake was not fetched.
**What the interviewer is checking:** Awareness of Fabric and its trade-offs against Import and DirectQuery.
**Say this in the interview:** "Direct Lake is a Fabric storage mode where the semantic model reads Delta tables in OneLake directly, loading columns into memory when needed. It gives near-Import speed without a copy refresh, and I'd use it with big lakehouse data. If a query cannot be served, it may fall back to DirectQuery."
**Explain simply:**
- **OneLake** is Fabric's single storage; a **Lakehouse** stores tables as Delta files.
- **Import** copies data (fast, stale until refresh); **DirectQuery** asks the source every time (fresh, slower); **Direct Lake** reads the files in place and "refreshes" only by re-pointing at new data (framing).
- Needs a Fabric capacity (from memory, F2 and above or Premium) and data in a lakehouse/warehouse.
**Example:** Daily attendance events land in a Fabric lakehouse; the HR report shows today's data in seconds with no import job.
**DAX / Steps:** Not run here; from memory.
1. Fabric workspace > Lakehouse > **New semantic model**, choose tables.
2. Build the report on that model in the Service.
**Alternative:** Import mode with incremental refresh (Q53), or DirectQuery.
**Version / licensing note:** From memory, unverified.
**Edge cases:** Fallback to DirectQuery for some features/size limits; RLS may force fallback (unverified).
**Likely follow-ups:**
- *Is it free?* No; it needs paid Fabric capacity.
**Common mistakes:** Treating it as DirectQuery or as plain Import.

### Q53 ⭐ 🟡 What is the Detect data changes setting in incremental refresh, and when is it useful?
**Asked at:** Commonly asked (no company-specific report found); incremental refresh is named in interview_processes.md as a service-MNC topic.
**What the interviewer is checking:** Do you know how to skip refreshing partitions whose data has not changed?
**Say this in the interview:** "Detect data changes lets the Service run a small query for the maximum of a date-modified column per partition. If the value is the same as last refresh, it skips that partition. It is useful when old rows are occasionally updated but most periods are untouched."
**Explain simply:**
- **Incremental refresh** splits a big table into time partitions (e.g. months) and refreshes only the recent ones.
- Detect data changes adds a check: choose a column such as `LastUpdated` (not the same as the RangeStart/RangeEnd date column).
- Partitions where the max is unchanged are not reloaded.
**Example:** Payroll with 6 monthly partitions in the refresh window; only November was corrected.
**Sample data:** Partitions (stored max vs source max):

| Month | StoredMax | SourceMax |
|---|---|---|
| 2026-06 | 2026-06-30 | 2026-06-30 |
| 2026-10 | 2026-10-31 | 2026-10-31 |
| 2026-11 | 2026-11-10 | 2026-11-14 |

**DAX / Steps:** Not run here; from memory.
1. In Desktop, create `RangeStart`/`RangeEnd` parameters (type Date/Time) and filter the date column.
2. Right-click the table > **Incremental refresh** > set window > tick **Detect data changes** and pick the column.
3. Publish; the first Service refresh builds all partitions.
**Alternative:** Without it, every partition inside the refresh window is reloaded.
**Result:** Reproduced with pandas on 6 monthly partitions (the table above is a 3-row excerpt; 2026-07 to 2026-09 also unchanged): 1 of 6 partitions needs refresh (2026-11).
**Pandas check:**
```python
p["Refresh?"]=p.StoredMax!=p.SourceMax
print(p["Refresh?"].sum(),"of",len(p))   # prints: 1 of 6
```
**Version / licensing note:** Incremental refresh overview page (fetched earlier, per sources file) lists plans supported; I could not re-fetch it, so licence details are from memory, unverified.
**Edge cases:** The change column must reliably update; if it is unreliable you will miss changes. Source must support the polling query (usually needs query folding).
**Likely follow-ups:**
- *Same as RangeStart?* No, a different column.
**Common mistakes:** Picking a column that never changes, so stale data stays.

### Q54 ⭐ 🟡 How does the Only refresh complete days setting work, and why does the time zone matter?
**Asked at:** Commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand how incremental refresh decides "today" and the UTC trap?
**Say this in the interview:** "With this on, the refresh window ends at the last fully finished day, so half-loaded days are never stored. The Service works out 'today' in UTC, not in my local time zone, so a refresh at 2 AM India time is still the previous day in UTC and results can differ from what I expect."
**Explain simply:**
- Without it, the current (partial) day is included and refreshed again next time.
- With it, the incomplete day waits until it is complete.
- India is UTC+5:30, so a 2 AM IST refresh happens at 20:30 UTC the previous evening: the Service believes that day is not finished.
**Example:** Attendance data refreshed at 15 Nov 02:00 IST. Window = 3 days.
**Sample data:** Refresh run time:

| Item | Value |
|---|---|
| Run time IST | 2026-11-15 02:00 |
| Run time UTC | 2026-11-14 20:30 |

**DAX / Steps:** Not run here; same dialog as Q53.
1. Right-click table > **Incremental refresh**.
2. Tick **Only refresh complete days** (set the refresh window of 3 days).
**Alternative:** Schedule refresh after 05:30 IST (00:00 UTC) so the previous day is complete in both.
**Result:** Reproduced with pandas: flag OFF refreshes 12, 13, 14 Nov (14 Nov is partial in UTC); flag ON refreshes 11, 12, 13 Nov.
**Pandas check:**
```python
run_utc=pd.Timestamp("2026-11-14 20:30"); t=run_utc.normalize()
off=[(t-pd.Timedelta(days=i)).date() for i in (2,1,0)]
on =[(t-pd.Timedelta(days=i)).date() for i in (3,2,1)]
# off: 2026-11-12,13,14   on: 2026-11-11,12,13
```
**Version / licensing note:** Behaviour per the incremental refresh overview page cited in the sources file (not re-fetched); UTC reasoning from memory, unverified.
**Edge cases:** Daylight saving and local business days; an IST user sees 14 Nov "late" by one run.
**Likely follow-ups:**
- *Why on?* Avoids storing partial days if the source is still loading.
**Common mistakes:** Assuming "today" follows the user's time zone.

### Q55 ⭐ 🟡 What is object-level security, and how does it differ from row-level security?
**Asked at:** Commonly asked (no company-specific report found); the sources file lists OLS as a one-star topic.
**What the interviewer is checking:** Do you know OLS hides tables/columns, while RLS hides rows?
**Say this in the interview:** "Row-level security filters which rows a person sees. Object-level security hides whole tables or columns, such as Salary, from certain roles, so to them the field does not exist."
**Explain simply:**
- **RLS:** a DAX filter per role, e.g. `[Region] = "South"`; the same visual just shows fewer rows.
- **OLS:** you set a table/column to *None* for a role; visuals using it show an error for those users.
- OLS is set outside Desktop's normal role dialog, usually with the free **Tabular Editor** tool (from memory).
- Both are defined in the model and apply only to Viewers.
**Example:** HR analysts see all employees (rows) but only Payroll team sees the `Salary` column.
**DAX / Steps:** Not run here; from memory.
1. In Desktop **Modeling** > **Manage roles**, create role `Analysts` (RLS dialog).
2. Open **Tabular Editor** (external tool) > Roles > Table Permissions > set `Employee[Salary]` to **None**.
3. Save, publish, add members under semantic model **Security** in the Service.
**Alternative:** Separate "Salary" into its own table and secure it with RLS, or keep salary out of the model.
**Version / licensing note:** From memory, unverified.
**Edge cases:** A measure referring to a hidden column breaks for that role.
**Likely follow-ups:**
- *Does OLS hide the table name?* Yes, from those users.
**Common mistakes:** Hiding the column in the Report view and calling it security.

### Q56 ⭐ 🟡 How do you audit who viewed or changed reports in the Power BI Service?
**Asked at:** Commonly asked (no company-specific report found); gap-fill, no source shows it asked.
**What the interviewer is checking:** Do you know governance tools, not only visuals?
**Say this in the interview:** "The audit log: Power BI activities such as ViewReport or EditReport are recorded in the Microsoft Purview audit log, and admins can also pull them with the Get Activity Events API. For a quick popularity view, the usage metrics report works for report owners."
**Explain simply:**
- **Audit log:** a tenant-wide record of who did what and when; needs an admin-type role.
- **Activity events API:** returns the same events for scripts (limited look-back, believed 30 days; unverified).
- **Usage metrics report:** per report; shows views and viewers over 30 days; the sources file notes it needs edit access plus Pro/PPU and is labelled preview.
**Example:** The HR head asks "who opened the salary report last week?" The admin filters ViewReport events for that report.
**DAX / Steps:** Not run here; from memory.
1. Admin portal > **Audit logs** (opens the Purview portal), or Microsoft Purview > **Audit**.
2. Filter dates, activity "Viewed Power BI report", user.
3. Export CSV. For usage metrics: report **...** > **View usage metrics**.
**Alternative:** Admin monitoring workspace reports (Fabric).
**Version / licensing note:** Usage metrics details per the fetched page cited in the sources file; audit steps and 30-day look-back from memory, unverified.
**Edge cases:** Delays of minutes to hours; audit may need turning on.
**Likely follow-ups:**
- *Can a normal user do it?* Usually no.
**Common mistakes:** Confusing usage metrics (aggregate) with audit (per user).

### Q57 ⭐ 🟡 Why can a dataset refresh work in Desktop but fail in the Service?
**Asked at:** Commonly asked (no company-specific report found); refresh troubleshooting is three-star in the sources file.
**What the interviewer is checking:** A structured troubleshooting approach.
**Say this in the interview:** "Desktop runs on my laptop with my credentials and my network. The Service runs from the cloud, so it needs a gateway for on-premises sources, stored credentials, and privacy-level rules. I'd check gateway status, credentials, local file paths, and the error message."
**Explain simply:**
- **Gateway missing/offline:** on-premises SQL or file shares are unreachable from the cloud.
- **Credentials expired** or the wrong authentication method (e.g., Windows vs OAuth).
- **Local paths** like `C:\HR\data.xlsx` exist only on my PC.
- **Privacy levels/Firewall** errors when combining sources; **timeouts** (the sources file records a 2-hour limit on shared capacity, 5 hours Premium).
- Parameters or data source names differing between PBIX and the gateway.
**Example:** The attendance file sits on a laptop's Desktop folder; refresh works locally, fails in the Service with "can't connect".
**DAX / Steps:** Not run here; from memory.
1. Semantic model **Settings** > **Gateway and cloud connections**: map data sources.
2. **Data source credentials** > Edit credentials; **Refresh history** to read the error.
**Alternative:** Move files to SharePoint/OneDrive (cloud) so no gateway is needed.
**Version / licensing note:** Limits per refresh-data page cited in sources file (not re-fetched); rest from memory, unverified.
**Edge cases:** Dynamic data sources can make Service refresh fail.
**Likely follow-ups:**
- *Where is the error?* Refresh history details.
**Common mistakes:** Re-publishing repeatedly instead of reading the error.

### Q58 ⭐ 🟡 A source table is changing and you want to know which reports will break. How does lineage view help?
**Asked at:** Commonly asked (no company-specific report found); gap-fill question.
**What the interviewer is checking:** Impact analysis habit before changing sources.
**Say this in the interview:** "Lineage view shows a workspace as a map: data sources, semantic models, reports and dashboards, connected by arrows. I find the source and follow the arrows to see everything downstream that might break."
**Explain simply:**
- Each card is an item; arrows show dependency.
- Per the sources file (fetched Learn page, updated 2026-04), lineage view needs Admin/Member/Contributor (not Viewer) and Pro.
- Lineage stays inside the workspace unless reports use cross-workspace semantic models, which are shown as linked items.
- The separate "impact analysis" button was not on the fetched page, so I treat it as unverified.
**Example:** Source table `HR_Employee` will rename `DeptCode`. Lineage shows 1 semantic model feeding 4 reports and 1 dashboard; I notify those owners.
**DAX / Steps:** Not run here; from memory.
1. Open the workspace > **View** (top right) > **Lineage**.
2. Click an item to highlight its connections; open the item to check its owner.
**Alternative:** Admin Scanner API or an inventory spreadsheet.
**Version / licensing note:** Role/licence per the fetched lineage page in sources file; impact analysis unverified.
**Edge cases:** Does not tell you which exact column is used.
**Likely follow-ups:**
- *Does it show column usage?* No.
**Common mistakes:** Renaming first and checking later.

### Q59 ⭐ 🟡 A colleague only needs to look at one report: how do you share it with them, and what permissions must they have to see the data behind it?
**Asked at:** Commonly asked (no company-specific report found); gap-fill. Not verified on Microsoft Learn "Share reports" pages (unreachable here).
**What the interviewer is checking:** Sharing vs workspace roles vs semantic model access.
**Say this in the interview:** "I'd use the Share button on the report and type their email, or share from an app. Under the hood they need access to the report and read access to the semantic model; Share grants both automatically. On Pro, the recipient also generally needs a Pro licence unless the content is in Premium or Fabric capacity."
**Explain simply:**
- **Share** gives report access plus Read on the semantic model; optional Build.
- The **Link** can be for people in your organisation, people with existing access, or specific people.
- RLS still applies to them.
- Licence: free users can view only if the workspace is on suitable capacity (see Q65).
**Example:** Share the "Monthly Attrition" report to the CFO's email with "Send email" off, and a message.
**DAX / Steps:** Not run here; from memory.
1. Report (Service) > **Share**.
2. Pick link type; add name/email; choose permissions; **Send**.
**Alternative:** Add them as workspace **Viewer**, or add to an app audience.
**Version / licensing note:** From memory, unverified.
**Edge cases:** Sharing to external guests needs tenant settings; revoking via Manage permissions.
**Likely follow-ups:**
- *Why can't they see data?* Missing semantic model read, or RLS.
**Common mistakes:** Giving workspace Member to someone who only needs a view.

### Q60 ⭐ 🔴 Why can incremental refresh be slow or fail if query folding does not work?
**Asked at:** Commonly asked (no company-specific report found); incremental refresh is a recurring topic per interview_processes.md.
**What the interviewer is checking:** Do you know folding is what makes partitions cheap?
**Say this in the interview:** "Query folding means Power Query translates my steps into one SQL query that the source runs, so only the filtered rows are sent. If folding breaks, each partition downloads the whole table and filters it in Power BI's engine, so refresh gets slow, runs into the time limit or fails."
**Explain simply:**
- **RangeStart/RangeEnd** filters must fold, so each partition asks the source for just its date range.
- Folding breaks with steps like custom functions, merging with non-foldable sources, some column changes.
- Right-click a step > **View Native Query** greyed out is the hint.
**Example:** 3,000,000 rows over 36 months; a 3-partition refresh should read about 250,000 rows. Without folding it reads the whole table three times.
**Sample data:** Illustrative sizes:

| Item | Value |
|---|---|
| Total rows | 3,000,000 |
| Monthly partitions | 36 |
| Partitions refreshed | 3 |

**DAX / Steps:** Not run here; from memory.
1. Power Query > select the step > right-click > **View Native Query** (enabled = folds).
2. Move foldable filters first; fix or remove non-foldable steps.
**Alternative:** Push logic into a SQL view that supports the date filter.
**Result:** Reproduced with pandas arithmetic: folding reads 249,999 rows; no folding reads 9,000,000 (36 times more). Illustrative, not measured.
**Pandas check:**
```python
per=3_000_000//36
print(3*per, 3*3_000_000)   # 249999 9000000
```
**Version / licensing note:** Folding requirement and limits per the incremental refresh overview and refresh-data pages (cited in sources file, not re-fetched); rest from memory, unverified.
**Edge cases:** Non-SQL sources (Excel/CSV) never fold, so incremental refresh gives little benefit.
**Likely follow-ups:**
- *Does Power BI warn you?* It can warn that folding is not detected (unverified).
**Common mistakes:** Setting up incremental refresh on a CSV.

### Q61 ⭐ 🔴 A manager can see every employee because bi-directional filtering is on. How do RLS and Apply security filter in both directions interact?
**Asked at:** Commonly asked (no company-specific report found); RLS appears in the Deloitte, Cognizant and Wipro-class reports in interview_processes.md, but this bi-directional variant is a gap-fill.
**What the interviewer is checking:** Do you understand that RLS filters propagate along relationship direction?
**Say this in the interview:** "Premise check: bi-directional alone does not remove RLS. RLS filters the table I put the rule on and flows in each relationship's direction. By default security filters follow the single direction; **Apply security filter in both directions** makes them also travel the other way. I would check where the rule sits, that direction, role membership and whether the user is an editor."
**Explain simply:**
- Rule on `Employee`: dimension tables like `Department` are not shrunk unless security filtering flows both ways.
- Rule on `Department`: filter flows to `Employee` normally.
- Users in several roles get the union of rows; Admin/Member/Contributor see everything (RLS applies only to Viewers).
- Why a manager sees everyone: rule on the wrong table, the filter points the wrong way, or editor role.
**Example:** Manager m1 manages Sales/IT people.
**Sample data:** Employee table:

| Emp | DeptID | ManagerEmail |
|---|---|---|
| A | 1 | m1 |
| B | 1 | m2 |
| C | 2 | m1 |
| D | 2 | m1 |
| E | 3 | m3 |
| F | 3 | m3 |

Department table: 1 Sales, 2 IT, 3 HR.
**DAX / Steps:** Not run here.
```dax
-- Role "Manager" on Employee:
[ManagerEmail] = USERPRINCIPALNAME ()
```
Then Modeling > Manage relationships > Employee-Department > tick **Apply security filter in both directions** (only if needed).
**Alternative:** Put the rule on Department via a security table instead of using both directions (cleaner, less risk).
**Result:** Reproduced with pandas: m1 sees A, C, D. Department shows all 3 depts with single-direction security; Sales and IT only with both directions.
**Pandas check:**
```python
vis=emp[emp.ManagerEmail=="m1"]
dept[dept.DeptID.isin(vis.DeptID)].Dept.tolist()  # ['Sales','IT']
```
**Version / licensing note:** RLS applies only to Viewers per the fetched RLS page (sources file); the checkbox behaviour from memory, unverified.
**Edge cases:** Many-to-many relationships; USERPRINCIPALNAME vs USERNAME.
**Likely follow-ups:**
- *How to test?* **View as** role in Desktop and Service.
**Common mistakes:** Turning on both-directions to "fix" it, which can leak or loop.

### Q62 ⭐ 🔴 How do you manage RLS for managers in a parent-child hierarchy (each manager sees their whole reporting line)?
**Asked at:** Commonly asked (no company-specific report found); gap-fill.
**What the interviewer is checking:** DAX PATH functions for dynamic RLS.
**Say this in the interview:** "I add a PATH calculated column that stores each person's chain of managers, then the role filter checks whether the logged-in user's ID appears in that chain. A manager sees everyone below them, automatically as the org changes."
**Explain simply:**
- **PATH(EmpID, ManagerID)** returns text like `1|2|4`: top boss to the person.
- **PATHCONTAINS(path, id)** is TRUE if the id is in the chain.
- **LOOKUPVALUE** finds the user's own ID from their email, which comes from **USERPRINCIPALNAME()**.
**Example:** Asha is CEO; Bala manages Dev and Esha; Dev manages Gita.
**Sample data:** Employee table:

| EmpID | Name | ManagerID | Email |
|---|---|---|---|
| 1 | Asha | blank | asha@x.com |
| 2 | Bala | 1 | bala@x.com |
| 3 | Chitra | 1 | chitra@x.com |
| 4 | Dev | 2 | dev@x.com |
| 5 | Esha | 2 | esha@x.com |
| 6 | Farid | 3 | farid@x.com |
| 7 | Gita | 4 | gita@x.com |

**DAX / Steps:** Not run here; PATH, PATHCONTAINS, LOOKUPVALUE and USERPRINCIPALNAME are used from memory, not checked on Microsoft Learn.
```dax
Path = PATH ( Employee[EmpID], Employee[ManagerID] )   -- calculated column
```
```dax
-- Role filter on Employee:
PATHCONTAINS (
    Employee[Path],
    LOOKUPVALUE ( Employee[EmpID], Employee[Email], USERPRINCIPALNAME () )
)
```
**Alternative:** A separate security table (UserEmail, EmpID) with flattened reporting lines.
**Result:** Reproduced with pandas: Bala sees Bala, Dev, Esha, Gita; Dev sees Dev, Gita; Gita sees Gita; Asha sees all 7.
**Pandas check:**
```python
e["Path"]=e.EmpID.apply(path)        # '1|2|4|7' for Gita
e[e.Path.apply(lambda s: str(me) in s.split("|"))].Name.tolist()
```
**Version / licensing note:** From memory, unverified.
**Edge cases:** IDs must be unique; a loop breaks PATH; if a user's email is missing, LOOKUPVALUE returns blank and they see nothing; HR/admin roles need a separate "see all" role.
**Likely follow-ups:**
- *Do peers see each other?* No, only their own subtree.
**Common mistakes:** Filtering only `ManagerID = me`, which shows direct reports only.

### Q63 ⭐ 🔴 A report with RLS works in Desktop but shows no data for a guest user. What would you check?
**Asked at:** Commonly asked (no company-specific report found); gap-fill.
**What the interviewer is checking:** Systematic RLS debugging with external users.
**Say this in the interview:** "In Desktop RLS isn't enforced until I use View as. For a guest I'd check: are they added to the role? Does the role filter match the identity the Service sees, since guests' USERPRINCIPALNAME can look like `name_company.com#EXT#@tenant`? Do they have Viewer access, and does the semantic model allow external sharing?"
**Explain simply:**
- **Guest (B2B)** user: an external person invited into your Azure AD.
- The RLS page in the sources file mentions guests; the `#EXT#` format is from memory.
- Check role membership, filter matching, data columns, and the workspace role (editors bypass RLS).
**Example:** Partner recruiter has email `ravi@agency.com`, but the model's Email column has that value; the Service identity is a longer `#EXT#` string, so no rows match.
**DAX / Steps:** Not run here.
1. Service > semantic model **Security** > confirm guest in the role.
2. **...** > **Test as role** with "Other user" if available.
3. Compare `USERPRINCIPALNAME()` value (temporary card measure) against your data.
**Alternative:** Map guests with a security table that stores the Azure AD identity.
**Version / licensing note:** Guest support per the RLS page cited in sources file; `#EXT#` and tenant settings from memory, unverified.
**Edge cases:** Cross-tenant settings; guest licensing (Pro or capacity).
**Likely follow-ups:**
- *Why fine in Desktop?* No role applied by default.
**Common mistakes:** Testing as the owner (who bypasses RLS).

### Q64 ⭐ 🔴 How would you move a report from a Development workspace to Production without breaking the data source connection?
**Asked at:** Commonly asked (no company-specific report found); gap-fill.
**What the interviewer is checking:** Environment-safe release practice.
**Say this in the interview:** "I'd parameterise the server and database in Power Query, then use a deployment pipeline with a deployment rule, or change the parameter in the Production semantic model settings after publish. I'd then re-check credentials and refresh once."
**Explain simply:**
- Parameters (named values like `ServerName`) replace hard-coded server names in M.
- Deployment rules (Q45) switch parameters per stage.
- Without a pipeline: publish the PBIX to Production, then edit **Parameters** in the model settings.
**Example:** Dev uses `hr-dev-sql`; Prod uses `hr-prod-sql`. Parameter swap avoids editing queries.
**DAX / Steps:** Not run here.
```m
let
    Source = Sql.Database ( ServerName, DatabaseName ),
    Emp = Source{[Schema="dbo", Item="Employee"]}[Data]
in
    Emp
```
1. Desktop: **Home** > **Transform data** > **Manage parameters** > create `ServerName`, `DatabaseName`.
2. Publish; Service > semantic model **Settings** > **Parameters** (or pipeline rules).
3. Edit credentials; **Refresh now**.
**Alternative:** Use Power BI Project/Git with ALM tooling (unverified).
**Version / licensing note:** Parameters in Service from memory; pipeline licence unverified (Q45).
**Edge cases:** Gateway data source must exist for the Production server.
**Likely follow-ups:**
- *Do report visuals need changes?* No.
**Common mistakes:** Hard-coded server names; forgetting credentials after deploy.

### Q65 ⭐ 🔴 A Pro user is asked to share a report with 300 free-licence employees. What are the options?
**Asked at:** Commonly asked (no company-specific report found); gap-fill. Licence names change often.
**What the interviewer is checking:** Licensing awareness and cost-aware options.
**Say this in the interview:** "A free user cannot view shared content from a Pro-only workspace. The options are: put the content in a workspace on paid capacity, such as Fabric or Premium, so free users can view it; give everyone Pro; or use PPU for everyone; or send exports/subscriptions. I'd avoid Publish to web for HR data."
**Explain simply:**
- **Pro:** per-user licence to share and view in shared workspaces.
- **Capacity (Premium/Fabric):** content in a workspace on capacity can be viewed by free users, subject to size threshold. The sources file mentions an F64 note on the fetched licence page: sharing without Pro for viewers applies at F64 and above (re-check; thresholds change).
- **PPU:** each viewer needs PPU too.
- Cheap fallback: scheduled PDF/PowerPoint export by email.
- **Publish to web** makes data public: not for staff data.
**Example:** 300 shop-floor staff view attendance; a capacity-backed app costs less than 300 Pro seats, depending on price (not quoted; prices change).
**DAX / Steps:** Not run here; from memory.
1. Workspace **Settings** > **License info** > assign capacity.
2. Publish an **App** to the 300 people (or share the report).
**Alternative:** Embed in SharePoint/Teams (viewers still need a licence).
**Version / licensing note:** Licence rules per "Service features by licence type" cited in sources file (not re-fetched); anything else from memory, unverified.
**Edge cases:** Free users cannot create content or use My workspace sharing.
**Likely follow-ups:**
- *Cheapest?* Depends on user count versus capacity cost; do a calculation.
**Common mistakes:** Assuming "Share" works for free users in a Pro workspace.
