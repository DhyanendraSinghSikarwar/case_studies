# Book 10 — Domain Knowledge | Part 7: IT Services / GCC Reporting & MIS, plus Workday and Alteryx 🟢🟡🔴

**Target:** 65 questions | **Actual:** 76 questions
**Scope:** how IT services companies and GCCs run (utilisation, bench, billing, pyramid, SLAs, project health), the data behind MIS packs, and a mini-section on Workday HR reporting and Alteryx workflows.

### Q1 ⭐⭐⭐ 🟢 How does an IT services company make money, and what is the difference between time-and-materials and fixed-price contracts from a reporting point of view?
**Asked at:** commonly asked (no company-specific report found); the IT-services business model appears in prep guides (unverified).
**What the interviewer is checking:** Whether you know that revenue comes from people's time, and that the contract type changes how revenue and risk show up in reports.
**Say this in the interview:** "An IT services company sells its people's skills to clients and earns the gap between what it charges and what those people cost. Under time-and-materials, revenue follows hours worked; under fixed-price, revenue is agreed up front, so any overrun is the company's loss."
**Explain simply:**
- **How money is made:** think of a staffing agency that also delivers the work. A client pays for engineers (billing rate per hour or per month). The company pays those engineers a salary plus overheads (cost). The difference is *margin*.
- **Time-and-materials (T&M):** the client pays for hours (or days) actually worked at an agreed rate. Revenue = billable hours x rate. Reporting is simple: hours logged in timesheets become the invoice. The client carries the risk of overrun.
- **Fixed-price:** one agreed price for a defined scope. Revenue is usually recognised as the work progresses (for example by percentage of effort completed; this is an accounting choice, confirm with Finance). The company carries the risk: more hours do not mean more revenue.
- **Reporting difference:** for T&M, track hours and rate. For fixed-price, track effort spent against the budget and the estimated cost to finish, because margin can quietly disappear.
- **HR parallel:** T&M is like paying a contractor by the hour; fixed-price is like paying a flat fee for a finished job.
**Likely follow-ups:** 1) *Which is riskier for the vendor?* Fixed-price, because of overruns. 2) *What is a retainer or managed service?* A recurring monthly fee for running a service; often tracked against SLAs (see Q8).
**Common mistakes:** Assuming revenue always equals hours x rate; reporting fixed-price margin without an estimate of remaining effort; mixing contract types in one average.

### Q2 ⭐⭐⭐ 🟢 What does 'bench' mean in an IT services company, and why does management track bench strength every week?
**Asked at:** commonly asked (no company-specific report found); bench is standard IT-services vocabulary in prep guides (unverified).
**What the interviewer is checking:** That you know bench is a cost with no revenue against it.
**Say this in the interview:** "Bench means employees who are on the payroll but not assigned to a billable project. They are paid but earn nothing, so management watches the count weekly to redeploy people quickly or plan hiring."
**Explain simply:**
- **Bench:** like staff waiting for a posting after a project ends. They may be in training, between projects, or newly joined and waiting for allocation.
- **Why weekly:** salary is a fixed cost, so every idle week reduces margin. Weekly tracking spots people free soon, so new projects can be matched in time.
- **What the report shows:** bench headcount, bench as a percentage of total headcount, skills on the bench, how long each person has been there (ageing), and upcoming roll-offs (projects ending).
- **Definitions vary:** some firms count trainees or people in client-paid training separately; state your definition (assumption, confirm with the team).
- **Analyst angle:** ageing and skill mismatch matter more than the raw count; ten people with an in-demand skill is a different story from ten with an outdated one.
**Likely follow-ups:** 1) *Is bench always bad?* No, a small buffer lets the firm staff new deals quickly. 2) *Bench vs idle hours?* Bench is about people; idle hours is about time (see Q15).
**Common mistakes:** Counting everyone not billing as bench (leave and internal roles are different); showing only a count with no ageing or skills.

### Q3 ⭐⭐⭐ 🟢 What is the difference between gross utilisation and net utilisation, and which employees are usually excluded from the denominator?
**Asked at:** commonly asked (no company-specific report found); utilisation is the core metric on professional-services vendor pages (unverified).
**What the interviewer is checking:** That you ask "utilisation of what, over which hours?" before quoting a number.
**Say this in the interview:** "Utilisation is billable hours divided by available hours. Gross uses all standard hours as the denominator; net removes time the person could not work, such as leave and holidays. Management roles and people not expected to bill are usually left out."
**Explain simply:**
- **Gross utilisation:** billable hours / total standard hours (for example 8 hours x working days). Leave counts against the team.
- **Net utilisation:** billable hours / (standard hours minus holidays, leave and sometimes training). It shows how well *available* time was used.
- **Usually excluded from the denominator (varies by firm, confirm the policy):** senior management, sales, HR, finance and other support staff; people on long leave; sometimes trainees and bench in formal training.
- **Why it matters:** the same team can show, for example, 70% gross and 80% net (illustrative). Always state which one a report uses.
- **HR parallel:** like attendance rate, where you must decide whether approved leave counts as absence.
**Likely follow-ups:** 1) *Which is better?* Net for judging allocation, gross for judging total capacity use. 2) *Is higher always better?* No; very high utilisation leaves no time for training and risks burnout (see Q16).
**Common mistakes:** Comparing a gross number with a net target; including non-delivery staff; not using the same headcount in numerator and denominator.

### Q4 ⭐⭐⭐ 🟢 What is the onsite-offshore model, and why does the onsite-offshore mix matter for revenue and margin reporting?
**Asked at:** commonly asked (no company-specific report found); a standard part of IT-services business-model prep (unverified).
**What the interviewer is checking:** That you know cheaper offshore delivery drives margin, and mix changes both.
**Say this in the interview:** "Onsite means staff working at the client's location, usually in a high-cost country; offshore means staff working from the company's own centres, for example in India. Onsite earns a higher rate but costs more; offshore earns a lower rate but at much better margin. The mix therefore moves revenue and margin together."
**Explain simply:**
- **Onsite:** closer to the client, higher billing rate, also higher cost (salary, travel, visas, housing).
- **Offshore:** delivered from the vendor's home centres, lower rate per hour but lower cost, so margin percentage is typically higher.
- **Mix:** for example 20% onsite and 80% offshore by headcount. A shift toward offshore usually lowers revenue per person but can raise margin percentage; reports should show both.
- **What to report:** headcount and revenue split by location, rate by location, and cost by location.
- **HR parallel:** like comparing a posting in a metro (higher pay, higher allowances) with one at a regional office.
**Likely follow-ups:** 1) *Is the mix the same by headcount and revenue?* Usually not: onsite is often a smaller share of headcount but a larger share of revenue, because of the higher rate (a typical pattern; check the firm's own data). 2) *Why do clients accept offshore?* Cost savings.
**Common mistakes:** Quoting the mix by headcount when asked about revenue; ignoring that onsite staff carry extra costs that sit outside normal salary.

### Q5 ⭐⭐⭐ 🟢 What is a Global Capability Centre (GCC), and how does the reporting work of a GCC analyst differ from that of an analyst at an IT services vendor?
**Asked at:** commonly asked (no company-specific report found); no GCC-specific analyst interview report was found in the sources, so the contrast below is general reasoning.
**What the interviewer is checking:** That you understand a GCC serves its own parent company, not outside clients.
**Say this in the interview:** "A GCC is a centre set up in another country (often India) by a large company to do work for itself, such as technology, finance or analytics. A GCC analyst reports internally on cost, service quality and delivery to the parent; a vendor analyst reports on billing and margin from outside clients."
**Explain simply:**
- **GCC:** a captive unit; the parent company owns it and its "customers" are internal business teams.
- **Vendor analyst:** focuses on revenue, billable utilisation, client contracts and margin.
- **GCC analyst:** focuses on cost per employee or per service, SLA performance for internal customers, headcount plans, attrition, project delivery and value delivered to the parent. There may be no external invoice at all; costs are often recharged internally (called a chargeback or cost-plus arrangement, details vary).
- **Overlap:** both use timesheets, headcount, SLA and project-health reporting.
- **Practical point:** many GCC reporting packs go to leaders abroad, so time zones, currency and consistent definitions matter.
**Likely follow-ups:** 1) *Why do firms build GCCs?* Access to talent and cost control (general reasoning). 2) *Do GCCs track utilisation?* Often yes, but as capacity use, not billing.
**Common mistakes:** Assuming a GCC works like a vendor; ignoring internal recharge logic; treating a GCC as only a back office.

### Q6 ⭐⭐⭐ 🟢 What is MIS reporting, and how does it differ from a BI dashboard and from ad hoc analysis?
**Asked at:** commonly asked (no company-specific report found); MIS analyst interview pages (AmbitionBox, Hirist, unverified) centre on this.
**What the interviewer is checking:** That you can separate routine reporting from exploration.
**Say this in the interview:** "MIS, management information system, reporting is the regular, fixed-format set of numbers managers use to run the business, such as a monthly pack. A BI dashboard is an interactive view that lets users filter; ad hoc analysis answers a one-off question."
**Explain simply:**
- **MIS:** same structure every week or month, same definitions, delivered on a schedule (often Excel or PDF). Accuracy and consistency matter most. Example: monthly headcount, attrition and attendance report.
- **BI dashboard:** a live visual tool (for example Power BI or Tableau) where users slice by team or month. Good for self-service.
- **Ad hoc analysis:** a new question, for example "why did attrition jump in one team?" Answered once, then possibly turned into a regular report.
- **Link between them:** a good ad hoc finding may become an MIS line; MIS numbers feed dashboards.
**Likely follow-ups:** 1) *What makes MIS reliable?* Fixed definitions, checks and reconciliation (see Q18). 2) *Is MIS outdated?* No; many leaders still want a fixed pack.
**Common mistakes:** Treating MIS as just copy-paste; changing definitions silently between months; building a dashboard when a fixed pack was asked for.

### Q7 ⭐⭐⭐ 🟢 What does a typical monthly MIS pack for an IT delivery or shared-services unit contain?
**Asked at:** commonly asked (no company-specific report found); the contents below are common practice and vary by company.
**What the interviewer is checking:** Whether you can think like a delivery manager and list what leaders look at.
**Say this in the interview:** "A pack usually has headcount and attrition, utilisation and bench, revenue and margin or cost, SLA performance and ticket volumes, and project health, each against target and last month."
**Explain simply:**
- **People:** headcount, joiners, leavers, attrition rate, open positions, bench, pyramid mix (see Q25).
- **Utilisation:** billable or productive share by team (Q3).
- **Financial:** revenue, cost, margin by project or account; for a GCC, cost against budget.
- **Service quality:** SLA compliance by priority (Q9), ticket volume, backlog and ageing.
- **Projects:** RAG status (Q11), schedule and cost variance (Q20), top risks.
- **Format:** one summary page with the headline numbers, then detail pages, each with target, actual, last month and a short commentary on why numbers moved.
**Likely follow-ups:** 1) *How do you decide what goes in?* Ask who reads it and what decision they make. 2) *How do you prevent errors?* Reconcile totals to the source (Q18).
**Common mistakes:** Numbers with no target or comment; too many pages; mixing definitions between sections.

### Q8 ⭐⭐⭐ 🟢 What is an SLA in IT support, and what is the difference between response time and resolution time?
**Asked at:** commonly asked (no company-specific report found); service-desk metric pages (vendor blogs, unverified) describe these.
**What the interviewer is checking:** That you know SLA clocks measure different promises.
**Say this in the interview:** "An SLA, service level agreement, is the promise on how fast support will act. Response time is how soon someone first acknowledges the ticket; resolution time is how long until it is fixed."
**Explain simply:**
- **SLA:** a written target, for example "respond within 30 minutes and resolve within 8 hours" for a given priority (invented example).
- **Response time:** from ticket creation to the first *human* reply or action. An automatic acknowledgement email often does not count; check the agreement.
- **Resolution time:** from creation to the issue being resolved. Pauses may apply, for example while waiting for the customer; the pause rules must be known.
- **Why separate:** a team can reply fast but fix slowly, or the reverse.
- **HR parallel:** like an HR helpdesk promising a reply in one day and payroll corrections within three.
**Likely follow-ups:** 1) *What is MTTR?* Mean time to resolve; definitions vary (resolve vs repair). 2) *What is a breach?* A ticket that missed its target.
**Common mistakes:** Counting automated replies as response; averaging resolution times when the SLA is a percentage within target; forgetting clock-pause rules.

### Q9 ⭐⭐⭐ 🟢 What do P1, P2, P3 and P4 priorities mean in a ticketing system, and why must SLAs be reported by priority rather than as one blended figure?
**Asked at:** commonly asked (no company-specific report found); SLA by priority is standard in service-desk guides (unverified).
**What the interviewer is checking:** That you can see how a blended average can hide a serious failure.
**Say this in the interview:** "P1 is the most urgent, such as a full outage; P4 is the least, such as a minor question. Each has its own target, so one blended figure can look healthy while the few critical tickets are failing."
**Explain simply:**
- **P1 (critical):** business stopped or many users affected; fastest targets, often round the clock.
- **P2 (high):** major function impaired, workaround may exist.
- **P3 (medium):** limited impact.
- **P4 (low):** minor or cosmetic.
- Exact wording and targets vary by company.
- **Why not blended:** suppose most tickets are P4 and are mostly on time; the blended figure looks great even if every P1 missed. One missed P1 matters more than many P4s.
- **Report:** SLA percentage, ticket count and breaches per priority, plus an overall figure only as a secondary line.
**Likely follow-ups:** 1) *Who sets priority?* Usually impact times urgency, agreed with the customer. 2) *Priority changes?* Report on final priority, but keep the original for audit.
**Common mistakes:** One blended percentage; ignoring that priority can be changed mid-ticket.

### Q10 ⭐⭐⭐ 🟢 What is the difference between an incident, a service request, a problem and a change in IT service management?
**Asked at:** commonly asked (no company-specific report found); ITSM (IT service management) terms from common practice, for example ITIL (from memory, unverified).
**What the interviewer is checking:** That you can classify tickets correctly, which drives all counts.
**Say this in the interview:** "An incident is something broken that needs restoring; a service request is a routine ask such as a new laptop; a problem is the underlying cause behind repeated incidents; a change is a planned modification to a system."
**Explain simply:**
- **Incident:** an unplanned disruption. Example: email is down.
- **Service request:** a standard, pre-approved ask. Example: access to a shared folder.
- **Problem:** the root cause. If the same VPN failure creates 50 incidents, one problem record tracks the permanent fix.
- **Change:** planned alteration, for example a software upgrade, usually with approval and a schedule.
- **Why analysts care:** each type has different SLAs and different volume patterns, so mixing them distorts averages.
**Likely follow-ups:** 1) *Where does a failed change end up?* Often it creates incidents. 2) *Do all firms use the same names?* Mostly, but tool setup varies.
**Common mistakes:** Treating all tickets as incidents; counting a problem record as a separate customer issue.

### Q11 ⭐⭐⭐ 🟢 What is a RAG status on a project, and how can you make it objective rather than the project manager's opinion?
**Asked at:** commonly asked (no company-specific report found); RAG-status articles (Deltek, PMI, unverified) say thresholds vary and data-driven rules help.
**What the interviewer is checking:** That you prefer rules over opinions.
**Say this in the interview:** "RAG means Red, Amber, Green: a traffic-light view of project health. To make it objective, I set numeric rules, for example schedule and cost variance bands, and calculate the colour automatically."
**Explain simply:**
- **Green:** on track. **Amber:** at risk, needs attention. **Red:** off track, needs escalation.
- **Problem with opinion:** project managers may keep projects green too long ("watermelon" status: green outside, red inside).
- **Objective rules (thresholds below are invented examples; set your own with the PMO):** schedule index (SPI, see Q20) 0.95 or above green, 0.85 to 0.95 amber, below 0.85 red, and cost index (CPI) likewise, the same illustrative bands used in Q20; open critical risks above a count; milestones late by more than N days.
- **Worst-of rule:** overall colour is the worst of the individual measures.
- **Keep a comment column:** a manager can add context, but must not overwrite the calculated colour silently.
**Likely follow-ups:** 1) *What data do you need?* Plan dates, actual progress, cost and effort. 2) *Where do the numbers come from?* See Q20 for the formulas.
**Common mistakes:** Thresholds that differ by report; allowing manual overrides with no trace; judging only schedule and not cost.

### Q12 ⭐⭐⭐ 🟢 What is the difference between a calculated field and a report in Workday, and why do HR reporting analysts use calculated fields?
**Asked at:** commonly asked (no company-specific report found); Workday prep pages (training vendors, unverified). Tool features below: from memory, unverified.
**What the interviewer is checking:** Whether you grasp the building blocks of Workday reporting.
**Say this in the interview:** "A report is the output, a list or summary of HR data. A calculated field is a custom column you build from existing fields, such as tenure or an age band, and then use inside reports."
**Explain simply:**
- **Workday:** a cloud system where companies keep HR and payroll data (see Q13).
- **Report (from memory, unverified):** a saved definition of which data source to use, which columns to show, filters and sorting.
- **Calculated field (from memory, unverified):** a reusable formula that creates a new value from other fields, for example "years of service" from hire date, or "yes/no" for "joined in last 90 days".
- **Why analysts use them:** one definition, built once, can feed many reports, so attrition or tenure bands are identical everywhere. This avoids each person redoing logic in Excel.
- **HR parallel:** the report is the register; the calculated field is the rule such as "probation = first 6 months".
**Likely follow-ups:** 1) *Do you need coding?* Mostly configuration, with formula-like functions (from memory, unverified). 2) *What if one is wrong?* Every report using it changes, so test first.
**Common mistakes:** Copying logic into each report; no naming convention; confusing a calculated field with a report filter.

### Q13 ⭐⭐⭐ 🟢 What is Workday HCM, and which HR data does it hold that an analyst would report on?
**Asked at:** commonly asked (no company-specific report found); Workday was absent from in-scope 0-2 year JDs per the sources file, so treat as a possible bonus topic. Product details: from memory, unverified.
**What the interviewer is checking:** Whether you know what an HR system of record holds.
**Say this in the interview:** "Workday HCM, human capital management, is a cloud HR system that holds the employee record: who they are, job, manager, pay, absence and hiring history. Analysts report on headcount, hires, exits and similar measures."
**Explain simply:**
- **Core worker data:** employee ID, name, hire date, job, grade, location, cost centre, manager, status.
- **Organisation structure:** teams, departments and reporting lines (used for hierarchy roll-ups).
- **Time and absence:** leave balances and records (module availability varies by company).
- **Compensation:** salary and allowances. This is sensitive, so access is restricted.
- **Recruiting and talent:** requisitions, candidates, performance and skills data, if the modules are used.
- **Analyst use:** headcount by month, attrition, hiring funnel, diversity mix, span of control.
- **Privacy:** employee data needs role-based access; awareness only, confirm with HR and legal.
**Likely follow-ups:** 1) *Is Workday the only source?* Often not; timesheets and finance data are separate (Q17). 2) *What is a key?* Employee ID is the usual join field.
**Common mistakes:** Treating the HR system as the source for billable hours; sharing salary data too widely.

### Q14 ⭐⭐⭐ 🟢 What is Alteryx, and what kind of recurring MIS work is it used to automate?
**Asked at:** commonly asked (no company-specific report found); the sources show Alteryx in about 3% of broader skills data and 0 of the in-scope MIS JD sample. Product details: from memory, unverified.
**What the interviewer is checking:** That you know what a workflow tool is for and when it adds value.
**Say this in the interview:** "Alteryx is a drag-and-drop tool to build repeatable data workflows: pull files and databases, clean, join, calculate and output. It suits monthly MIS jobs that otherwise need hours of copy-paste."
**Explain simply:**
- **Workflow:** boxes (tools) joined by lines; data flows left to right (from memory, unverified).
- **Typical MIS jobs:** merging a timesheet extract with an HR file, cleaning names, calculating utilisation, producing the output Excel.
- **Benefit:** once built, you refresh by running it; steps are visible and repeatable, which cuts manual errors.
- **Limits:** it is a licensed product, and someone must maintain the workflow when source files change.
- **HR parallel:** like a payroll checklist that runs itself every month.
**Likely follow-ups:** 1) *Alternatives?* Power Query, SQL or Python (Q22). 2) *Does it replace Excel?* No, it often feeds Excel.
**Common mistakes:** Automating before the process is stable; building a workflow nobody else can read or maintain.

### Q15 ⭐⭐⭐ 🟡 A team of 40 people has 6,400 available hours in a month after holidays and leave. Billable hours logged were 4,480, internal and training hours were 640, and the rest was idle. Compute billable utilisation, non-billable share and bench (idle) share.
**Asked at:** commonly asked (no company-specific report found); utilisation calculations are standard in professional-services prep (unverified).
**What the interviewer is checking:** Clean arithmetic and that the three shares add up to 100%.
**Say this in the interview:** "Billable utilisation is 70%, non-billable (internal and training) is 10%, and idle is 20%. They add to 100% of available hours."
**Explain simply:**
- The denominator is *available hours* (6,400), so this is a net-style utilisation (leave and holidays already removed).
- 6,400 hours across 40 people is 160 hours each, which is a sensible month.
- Idle is what remains after billable and internal time.
**Worked example:** (inputs are invented exercise numbers; percentages are shares of available hours, rounded exactly, no rounding needed)
- Billable utilisation = 4,480 / 6,400 = **70%**
- Non-billable (internal and training) = 640 / 6,400 = **10%**
- Idle hours = 6,400 - 4,480 - 640 = 1,280; idle share = 1,280 / 6,400 = **20%**
- Check: 70% + 10% + 20% = 100%. Idle of 1,280 hours is the equivalent of 8 people (1,280 / 160) with no work all month.
**Likely follow-ups:** 1) *Is 70% good?* Depends on the company target and role mix; state that definitions vary. 2) *Would you count training as productive?* Say how it is defined, then keep it separate.
**Common mistakes:** Dividing by total hours before removing leave; leaving out the idle remainder; calling a percentage-point gap a percentage change (70% to 75% is 5 percentage points).

### Q16 ⭐⭐⭐ 🟡 A team's utilisation is 85% but the project margin is falling. Give three reasons this can happen and the data you would pull to check each.
**Asked at:** commonly asked (no company-specific report found); "high utilisation is not the same as profit" is a recurring theme in vendor blogs (unverified).
**What the interviewer is checking:** That you understand utilisation is volume of hours, not price or cost.
**Say this in the interview:** "Utilisation only says how busy people are. Margin depends on rate and cost too, so it can fall if rates drop, if costs rise, or if the work is billed below its true effort."
**Explain simply:**
- **1. Lower realised rate or discounting:** people are busy but billed at lower rates (discounts, junior people on senior rates). Check: billing rate by resource and contract, invoiced vs standard rate (realisation, see Q24).
- **2. Higher cost per person:** salary hikes, expensive onsite staff, subcontractors, or a more senior mix. Check: cost rate by person from HR and finance; mix by level and location (Q4, Q25).
- **3. Fixed-price overrun or unbilled effort:** hours are logged as "billable" but the client is not paying for them (scope creep, rework, free support). Check: logged hours vs invoiced hours (Q18), effort vs budget on fixed-price projects.
- **Another cause:** the 85% may count mostly low-rate work, so the revenue per hour is down. Compare revenue per billable hour month on month.
**Likely follow-ups:** 1) *First check?* Revenue per billable hour and cost per hour trend. 2) *Which cut helps?* By project and by level.
**Common mistakes:** Assuming high utilisation means health; looking only at team totals instead of by project and level; ignoring non-billed "billable" hours.

### Q17 ⭐⭐⭐ 🟡 Where does the data for an IT-services MIS pack usually come from (timesheet tool, HRMS, project-management or PSA tool, ERP/finance, ITSM tool), and what keys join them?
**Asked at:** commonly asked (no company-specific report found); MIS roles are described as Excel/SQL reporting over several systems (prep sites and job postings, unverified).
**What the interviewer is checking:** Whether you know that one pack stitches together several systems and that joins fail when the identifiers do not match.
**Say this in the interview:** "Hours come from the timesheet tool, people details from the HRMS, project setup and allocation from the project or PSA tool, money from the ERP, and tickets from the ITSM tool. I join them on employee ID and project code, plus month, and I check the keys first because that is where mismatches hide."
**Explain simply:**
- **HRMS (Human Resource Management System):** the employee master: employee ID, band (grade), location, joining and exit dates, manager. Your home turf as an HR person.
- **Timesheet tool:** hours per employee, per project, per day or week, with a status (submitted, approved).
- **Project or PSA tool (Professional Services Automation, software that plans projects and staffing):** project code, client, contract type, start and end dates, planned allocation, billing rate.
- **ERP or finance system:** invoices, revenue booked, costs, receivables. This is the official money record.
- **ITSM tool (IT Service Management, the ticketing system):** incidents, requests, priorities, timestamps, resolver team.
- **Keys:** employee ID (HRMS to timesheet to allocation), project code (timesheet to PSA to ERP), customer ID (PSA to ERP), and a month or period key. Ticket data usually joins through a project, team or customer code.
- **System names differ by company**; treat any named tool as an example.
**Likely follow-ups:** 1) *What if the keys do not match?* Build a small mapping table and agree an owner for it. 2) *Which system wins in a conflict?* Finance wins for money; HRMS wins for employee facts.
**Common mistakes:** Joining on employee name; ignoring that project codes get closed or renamed; mixing calendar month and fiscal month; not asking who owns each source.

### Q18 ⭐⭐⭐ 🟡 The utilisation report and the finance billing report show different billable hours for the same month. How do you reconcile them step by step?
**Asked at:** commonly asked (no company-specific report found); reconciliation of two reports is a standard MIS and data-accuracy theme (prep sites, unverified).
**What the interviewer is checking:** A calm, step-by-step method for finding a gap instead of guessing or picking a winner.
**Say this in the interview:** "I first align the definitions and the period, then compare totals, then break the gap down by project and employee until I can explain every hour. Usually it is timing, status or rules, not an error."
**Explain simply:**
1. **Pin down definitions:** utilisation counts hours employees *logged* as billable; finance counts hours *invoiced*. They are different on purpose.
2. **Align the period and cut-off:** same dates, same time zone, same extraction time. Late timesheets and approvals after the cut-off are a classic cause.
3. **Compare totals, then split by project:** sort the differences from biggest to smallest.
4. **Look for the usual suspects:** hours logged but not approved; hours marked billable but contractually free (fixed-price work, goodwill, warranty); hours capped or written off before invoicing; invoice raised in a later month; wrong project code or rate card.
5. **Drill to employee level** for the biggest projects and tick off hours against invoice lines.
6. **Write a bridge:** Utilisation hours, minus items, equals billed hours. Show it to both owners and agree the fix.
**Worked example:** Utilisation report 4,480 hours; finance 4,310 hours; gap of 170 hours (computed). The bridge might show 100 not yet approved, 50 capped by the client contract, 20 on a wrong project code; those three add to 170, so nothing is left unexplained. (Invented numbers.)
**Likely follow-ups:** 1) *Which report is right?* Both, for their own definition; document it. 2) *How do you stop it recurring?* A standing monthly bridge and a shared definition sheet.
**Common mistakes:** Forcing one number to match without explanation; comparing different cut-off dates; blaming the finance team before checking definitions.

### Q19 ⭐⭐⭐ 🟡 A support team closed 1,250 tickets last month. 1,075 were resolved within the SLA target and 90 were still open past their target. How do you compute SLA compliance, and what ambiguity must you resolve before reporting the number?
**Asked at:** commonly asked (no company-specific report found); SLA reporting and the ambiguity of "compliance" are covered in service-desk metric guides (vendor blogs, unverified).
**What the interviewer is checking:** Whether you notice that the denominator is a choice and that ignoring open breached tickets flatters the result.
**Say this in the interview:** "Closed-only compliance is 1,075 of 1,250, which is 86%. But 90 tickets are still open and already past target, so they have breached; counting them gives 1,075 of 1,340, about 80%. I would report one definition clearly and show the other beside it."
**Explain simply:**
- **SLA (Service Level Agreement):** the promise, for example "resolve within 8 hours".
- **Formula:** tickets meeting target divided by tickets that were due in the period.
- **Closed-only:** 1,075 / 1,250 = 86.0%. Breached closed tickets = 175.
- **Including open breached:** 1,075 / (1,250 + 90) = 80.2% (rounded to one decimal).
- **Open tickets not yet due** stay out of both; they have not had a chance to fail.
- **Other points to settle:** is the clock paused while waiting for the customer; is it business hours or 24x7; response or resolution target; and the numbers must be split by priority (see Q9).
**Likely follow-ups:** 1) *Why is the gap 6 points?* Because 90 breached tickets were hidden from the closed-only view. 2) *Which should you report?* The one the contract defines; otherwise the stricter one.
**Common mistakes:** Dropping open breached tickets; quoting percentage points as percent (86% to 80% is about 6 percentage points); one blended figure across priorities.

### Q20 ⭐⭐⭐ 🟡 A project has planned value 100, earned value 90 and actual cost 120 (all in INR lakh). Compute schedule variance, cost variance, SPI and CPI, and give the RAG story in plain words.
**Asked at:** commonly asked (no company-specific report found); earned-value formulas are standard project-management practice (PMI-style, from memory, unverified).
**What the interviewer is checking:** Whether you can apply the four formulas and translate them into a business message.
**Say this in the interview:** "Schedule variance is minus 10 lakh and SPI is 0.90: we are behind plan. Cost variance is minus 30 lakh and CPI is 0.75: we spent 120 to get 90 of value. Late and over budget: on the illustrative bands below, amber on schedule and red on cost."
**Explain simply:**
- **Planned value (PV):** the work we planned to finish by now, in money terms. **Earned value (EV):** the work actually finished, valued at plan. **Actual cost (AC):** what we really spent.
- **Schedule variance (SV) = EV minus PV** = 90 - 100 = -10 lakh. **SPI = EV / PV** = 0.90.
- **Cost variance (CV) = EV minus AC** = 90 - 120 = -30 lakh. **CPI = EV / AC** = 0.75.
- **Reading it:** below 1.0 is bad. SPI 0.90 means 90 paise of planned progress per rupee planned; CPI 0.75 means each rupee spent produced 75 paise of value.
- **RAG (Red, Amber, Green):** thresholds differ by company; for example green at 0.95 or above, amber 0.85 to 0.95, red below 0.85 (illustrative only). On that rule schedule is amber, cost is red.
**Likely follow-ups:** 1) *What would you do?* Find why cost is high: extra people, rework or scope creep. 2) *Can SPI mislead?* Yes, late in a project it drifts toward 1 even when late.
**Common mistakes:** Mixing up the sign of the variances; dividing by the wrong base; treating AC as the budget.

### Q21 ⭐⭐⭐ 🟡 In Alteryx, what is the difference between the Join tool and the Union tool, and what are the three outputs of Join?
**Asked at:** commonly asked (no company-specific report found); Join versus Union appears in Alteryx prep guides (DataCamp, InterviewBit, unverified). Tool details here are from memory, unverified.
**What the interviewer is checking:** That you know side-by-side combining versus stacking.
**Say this in the interview:** "Join matches records from two inputs on a key and adds columns side by side, like a lookup. Union stacks two inputs on top of each other and adds rows. Join has three outputs: L (left only), J (joined), R (right only)."
**Explain simply:**
- **Join:** like VLOOKUP or a SQL join. You pick the key (say employee ID). Output **J** has matched rows; **L** has rows only in the left input; **R** has rows only in the right input.
- **Union:** like pasting January's sheet under February's. Both need similar columns; you can match them by name or position.
- **Why the L and R outputs help:** they show unmatched records, perfect for reconciliation (employees in the timesheet but missing from the HRMS).
- **HR parallel:** Join adds salary to the employee list; Union combines the monthly attendance files into one year.
**Likely follow-ups:** 1) *Does Alteryx Join do an inner join?* The J output is effectively an inner join; adding L or R gives outer joins. 2) *What if keys repeat?* Rows multiply; check duplicates first.
**Common mistakes:** Using Union when a key match is needed; forgetting trailing spaces or case differences in keys; ignoring the L and R outputs.

### Q22 ⭐⭐⭐ 🟡 You are given a monthly Excel MIS that takes six hours of copy-paste to refresh. How would you decide whether to automate it with Power Query, SQL, Python or Alteryx?
**Asked at:** commonly asked (no company-specific report found); tool-choice and automation questions are typical in MIS rounds (prep sites, unverified).
**What the interviewer is checking:** Judgement: choosing the simplest tool that fits the data, skills and company rules, not the fanciest.
**Say this in the interview:** "I would first understand the sources, volume and who must maintain it, then pick the simplest tool that works. Often Power Query inside Excel; SQL if the data lives in a database; Python for heavy or custom logic; Alteryx only if the company already licenses it and the team uses it."
**Explain simply:**
- **Questions first:** where does the data come from (files or a database)? How big? Who runs it next month? Which tools are approved and licensed?
- **Power Query:** built into Excel, point-and-click, refreshes with one click. Best when sources are Excel or CSV files and the audience lives in Excel.
- **SQL:** best when data already sits in a database; fast, repeatable, easy to review.
- **Python:** best for messy logic, large files, or scheduling; needs coding skill and someone to maintain it.
- **Alteryx:** visual workflow tool, strong for repeated multi-source jobs, but paid and needs a licence (from memory, unverified).
- **Decide with a simple test:** time saved per month against build and maintenance effort, plus risk if the builder leaves. Six hours monthly is 72 hours a year, so automation is usually worth it if the build and upkeep take only a few days (my rough rule; judge by the case).
- **Always:** keep a manual check against the old pack for the first two cycles.
**Likely follow-ups:** 1) *What if IT blocks tools?* Use what is approved, usually Excel features. 2) *How do you prove it works?* Run old and new in parallel and compare totals.
**Common mistakes:** Picking a tool for CV value; building something only you understand; skipping documentation and validation.

### Q23 ⭐⭐ 🟢 What is the difference between billing rate and cost rate, and how do they combine into gross margin per resource?
**Asked at:** commonly asked (no company-specific report found); rate and margin basics are standard in professional-services metric guides (vendor blogs, unverified).
**What the interviewer is checking:** That you separate what the client pays from what the person costs the company.
**Say this in the interview:** "Billing rate is the price per hour the client pays; cost rate is what the employee costs the company per hour. The gap is the gross margin per hour; multiply by billed hours for margin per resource."
**Explain simply:**
- **Billing rate:** from the contract or rate card, usually set by role and band.
- **Cost rate:** annual employee cost (salary, benefits, perhaps bonus) divided by available hours. Companies differ on what they include.
- **Margin per hour = billing rate minus cost rate; margin % = margin / billing rate.**
- **Utilisation matters:** the cost is paid for all hours, but revenue arrives only for billed hours.
**Worked example:** billing rate INR 1,800/hour, cost rate INR 1,000/hour, 120 billed hours in the month. Revenue 216,000; direct cost 120,000; margin 96,000; margin per hour 800; margin 44.4% of revenue. (Invented numbers, rounded to one decimal; this ignores unbilled hours.)
**Likely follow-ups:** 1) *What if the person is only 60% billed?* Cost still runs for all hours, so true margin is lower. 2) *Is margin % or amount more useful?* Both; percentage for comparing, amount for total profit.
**Common mistakes:** Calculating cost only on billed hours; using salary without overheads without saying so; confusing margin with markup.

### Q24 ⭐⭐ 🟢 What is realisation in a professional-services firm, and how is it different from utilisation?
**Asked at:** commonly asked (no company-specific report found); utilisation versus realisation is a standard distinction in professional-services guides (vendor blogs, unverified).
**What the interviewer is checking:** That you know utilisation measures hours and realisation measures money.
**Say this in the interview:** "Utilisation asks how much of people's time was billable. Realisation asks how much of the value of that time we actually collected after discounts and write-offs. High utilisation with low realisation means busy but not paid."
**Explain simply:**
- **Utilisation = billable hours / available hours.** It is about effort.
- **Realisation = amount invoiced (or collected) / hours times standard rate.** It is about price. Define whether you use billed or collected; definitions vary.
- **Why realisation drops:** client discounts, hours written off because of overruns, rate cuts, or billing less than worked on fixed-price work.
- **HR parallel:** utilisation is attendance; realisation is how much of that attendance turned into paid output.
**Worked example:** 800 hours at a standard rate of INR 1,600 gives 12.8 lakh; invoice 11.52 lakh; realisation 90.0% (invented numbers, computed).
**Likely follow-ups:** 1) *Can utilisation be high and realisation low?* Yes, a loss-making fixed-price project. 2) *Who watches it?* Delivery heads and finance.
**Common mistakes:** Using the two terms interchangeably; mixing billed and collected amounts; forgetting write-offs happen after the hours were logged.

### Q25 ⭐⭐ 🟢 What is the employee pyramid in an IT services company, and why does a flat or inverted pyramid hurt margin?
**Asked at:** commonly asked (no company-specific report found); pyramid structure is standard IT-services industry vocabulary (research notes and media, unverified).
**What the interviewer is checking:** Whether you connect staffing mix to cost and margin.
**Say this in the interview:** "The pyramid shows headcount by seniority: many juniors at the base, fewer seniors at the top. Seniors cost more per hour, so more seniors per project raises cost, and if billing rates do not rise equally, margin falls."
**Explain simply:**
- **Layers:** juniors (freshers, analysts), middle (leads, managers), seniors (heads, directors). Band names vary.
- **Why a wide base works:** the bulk of delivery work is done by lower-cost people, supervised by fewer experts.
- **Flat or inverted:** too many seniors for the work; cost per head rises while revenue for the same work stays fixed.
- **Not always bad:** specialist or consulting-heavy work can need a flatter shape; AI-driven change is also reshaping it (from memory, unverified).
**Worked example:** a 100-person team with 60 juniors, 30 middle and 10 seniors, at invented monthly costs of 6, 12 and 24 (INR thousand); average cost per head 9.6. Shifting to 30, 40 and 30 raises average cost to 13.8, 44% higher (computed from the two averages).
**Likely follow-ups:** 1) *How do you track it?* Headcount share by band per project. 2) *What is the fixed-price risk?* Revenue is fixed, so a senior-heavy mix kills profit.
**Common mistakes:** Calling flat structures always wrong; ignoring attrition among juniors; measuring headcount only, not cost.

### Q26 ⭐⭐ 🟢 What is revenue per employee, and what are its weaknesses as a measure of productivity?
**Asked at:** commonly asked (no company-specific report found); revenue per employee is widely quoted as an IT industry figure (media, unverified).
**What the interviewer is checking:** That you can use a ratio and also challenge it.
**Say this in the interview:** "Revenue per employee is revenue divided by average headcount. It is a rough productivity indicator, but it ignores mix, pricing, location and profit, so I never compare it alone."
**Explain simply:**
- **Formula:** revenue for the period divided by average headcount; annualise if the period is shorter.
- **Weaknesses:** a high-priced consulting firm will look better than a high-volume operations firm; more offshore staff lowers it; contractors and acquisitions distort headcount; it says nothing about profit or quality.
- **Better companions:** margin, utilisation, revenue per billable employee.
**Worked example:** annual revenue INR 3,000 crore, average headcount 5,000: 3,000 crore = 30,000,000,000 rupees; divided by 5,000 is INR 6,000,000 or INR 60 lakh per employee (invented numbers).
**Likely follow-ups:** 1) *Headcount at year end or average?* Average, otherwise growth skews it. 2) *Are contractors included?* State your choice.
**Common mistakes:** Using year-end headcount; comparing across business models; unit errors between crore and lakh (1 crore = 100 lakh).

### Q27 ⭐⭐ 🟢 What are timesheets in a services company, and what data quality problems (late filing, wrong project code, default hours) do analysts typically find?
**Asked at:** commonly asked (no company-specific report found); data-accuracy questions are common in MIS interview reports (crowdsourced prep sites, unverified).
**What the interviewer is checking:** Whether you know the source data is human-entered and flawed.
**Say this in the interview:** "A timesheet records who worked how many hours on which project and task. It drives billing and utilisation, so errors flow straight into revenue and margin. I check late filing, wrong codes and copy-paste default hours."
**Explain simply:**
- **Late filing:** submitted after the cut-off, so the month's numbers move after the report is sent.
- **Wrong project code:** hours land on the wrong client or on a closed project, affecting billing and cost.
- **Default hours:** everyone shows exactly 8 hours daily regardless of leave or reality.
- **Other signs:** more than 24 hours in a day, hours on holidays or leave days, missing approvals, duplicates.
- **Analyst checks:** compare to HRMS leave and attendance, flag outliers, report compliance by team.
**Likely follow-ups:** 1) *Do you fix the data yourself?* No: flag it to the owner and keep an audit note. 2) *What is the impact?* Under-billing, wrong margins.
**Common mistakes:** Silently correcting entries; assuming approved means correct; not freezing a cut-off.

### Q28 ⭐⭐ 🟢 What is the role of the resource management group (RMG) and how does an analyst support allocation and demand-supply reporting?
**Asked at:** commonly asked (no company-specific report found); RMG is standard IT-services staffing vocabulary (job postings, unverified).
**What the interviewer is checking:** Whether you understand how people get matched to projects and what to report.
**Say this in the interview:** "The RMG matches people to project demand. The analyst reports open demand against available supply by skill, location and date, along with allocation percentage and bench."
**Explain simply:**
- **Demand:** project requests for a role, skill, count and start date.
- **Supply:** bench, people rolling off projects soon, and new joiners.
- **Allocation:** the percentage of a person's time assigned to a project.
- **Reports:** demand versus supply by skill, time to fill a request, aged open demand, bench ageing, pending allocations.
- **HR parallel:** like manpower planning against vacancies, but for projects and weekly.
**Likely follow-ups:** 1) *What is a skill gap?* Demand with no matching supply. 2) *How often?* Weekly is common.
**Common mistakes:** Counting only headcount, not skill match; ignoring notice-period leavers in supply; stale demand lists.

### Q29 ⭐⭐ 🟢 What is a statement of work (SOW) and a change request, and why does scope creep show up in MIS data as effort overrun?
**Asked at:** commonly asked (no company-specific report found); SOW and scope creep are standard project vocabulary (prep sites, unverified).
**What the interviewer is checking:** Whether you can link a contract concept to a number in a report.
**Say this in the interview:** "A SOW defines the work, deliverables, timeline and price. A change request is the formal route to add or change scope with extra time or fee. If extra work is done without one, hours rise but revenue does not, so it appears as effort overrun."
**Explain simply:**
- **SOW:** the agreed list of what will be delivered and for how much.
- **Change request:** a documented, approved change to that agreement.
- **Scope creep:** client asks for a little more; the team agrees informally.
- **In MIS:** actual hours exceed planned hours (effort variance, see Q39), margin falls on fixed-price work.
- **Analyst action:** compare planned and actual hours by project and look for projects with no approved change requests.
**Likely follow-ups:** 1) *How do you spot it early?* Weekly burn against plan. 2) *Is overrun always scope creep?* No: poor estimates and rework also cause it.
**Common mistakes:** Blaming the team; not checking whether requirements truly changed.

### Q30 ⭐⭐ 🟢 What do DSO, unbilled revenue (WIP) and invoice ageing mean for a services company, and who uses them?
**Asked at:** commonly asked (no company-specific report found); working-capital metrics are standard finance vocabulary (unverified).
**What the interviewer is checking:** That you understand cash timing, not just revenue.
**Say this in the interview:** "DSO is how many days on average it takes to collect payment after sale. Unbilled revenue or WIP is work done but not yet invoiced. Invoice ageing groups unpaid invoices by how overdue they are. Finance and delivery heads use them to manage cash."
**Explain simply:**
- **DSO (Days Sales Outstanding) = receivables / revenue x days in the period.** Definitions vary.
- **Unbilled revenue (WIP, work in progress):** effort delivered but invoice not yet raised; a build-up suggests billing delays.
- **Invoice ageing:** buckets such as 0-30, 31-60, 61-90 and over 90 days overdue.
- **Users:** finance for cash, delivery managers for follow-up, leadership for risk.
**Worked example:** receivables INR 24 lakh, revenue of the last 90 days INR 90 lakh: DSO = 24 / 90 x 90 = 24 days (invented numbers).
**Likely follow-ups:** 1) *High DSO means?* Slow collection or disputes. 2) *Is high WIP bad?* It delays cash and may signal billing problems.
**Common mistakes:** Mixing period lengths; counting unbilled work as receivables.

### Q31 ⭐⭐ 🟢 How do milestone-based and percentage-of-completion revenue recognition differ in plain words, and why does an MIS analyst care?
**Asked at:** commonly asked (no company-specific report found); a gap-fill topic not named by the sources. Accounting rules are from memory, unverified, confirm with the finance team.
**What the interviewer is checking:** That you know revenue is not always the invoice date.
**Say this in the interview:** "Milestone-based recognises revenue when a defined deliverable is achieved. Percentage-of-completion recognises a share of revenue as work progresses, based on effort or cost done. They give different monthly revenue for the same project, so an analyst must know which is used."
**Explain simply:**
- **Milestone:** revenue arrives in chunks; months with no milestone show none.
- **Percentage-of-completion:** smoother; the share often comes from cost or effort incurred versus estimated total.
- **Analyst care:** monthly revenue, margin and forecasts depend on the method; estimates change.
**Worked example:** contract INR 60 lakh; total estimated project cost INR 45 lakh and INR 18 lakh incurred so far: completion 18 / 45 = 40.0%, so 40% x 60 = INR 24 lakh recognised. Under a milestone contract where the first 30% milestone (INR 18 lakh) is not yet achieved, revenue so far is 0 (invented numbers, computed).
**Likely follow-ups:** 1) *Does invoicing equal revenue?* No. 2) *Risk?* Poor estimates distort the number.
**Common mistakes:** Treating invoice as revenue; ignoring estimate revisions.

### Q32 ⭐⭐ 🟢 Why do GCCs report cost per FTE, and what does the metric include and exclude?
**Asked at:** commonly asked (no company-specific report found); gap-fill topic. GCC cost metrics vary by company (from memory, unverified).
**What the interviewer is checking:** Whether you understand a GCC is a cost-and-value centre for its parent and how its cost is compared.
**Say this in the interview:** "A GCC serves its parent company, so leaders track how much each full-time-equivalent person costs to justify location and growth. I would state exactly what is included, because definitions differ."
**Explain simply:**
- **GCC (Global Capability Centre):** an in-house centre of a global company, often in India.
- **FTE (full-time equivalent):** one full-time person; two half-timers equal one FTE.
- **Usually included:** salary, benefits, bonus, facilities, IT and tools, and often allocated overheads.
- **Often excluded or reported separately:** one-time set-up costs, parent-company charges, severance, project capital spending.
- **Why it matters:** compares sites, supports budget, and shows efficiency over time.
**Worked example:** annual centre cost INR 48 crore, 400 FTE: 48 crore = 480 million rupees; divided by 400 is INR 12 lakh per FTE (invented numbers).
**Likely follow-ups:** 1) *Include contractors?* State the policy. 2) *Is lower always better?* No: talent quality and output matter.
**Common mistakes:** Using headcount instead of FTE; mixing cost definitions across sites.

### Q33 ⭐⭐ 🟢 How do time-zone handoffs, follow-the-sun support and a global stakeholder base affect the reporting calendar of a GCC analyst?
**Asked at:** commonly asked (no company-specific report found); GCC reporting questions appear in prep guides (unverified).
**What the interviewer is checking:** Whether you understand that a global team means one report has many deadlines and many readers in different time zones.
**Say this in the interview:** "A GCC serves stakeholders in several countries, so I plan the reporting calendar around their working hours: data refreshes land before the earliest reader's morning, cut-off times are stated in one agreed time zone, and the pack goes out on a fixed day so nobody receives numbers that are still changing."
**Explain simply:**
- **GCC (Global Capability Centre):** an offshore centre, often in India, owned by a multinational company to do work for its own business units (IT, finance, HR, analytics).
- **Time-zone handoff:** work passes from one team to another as the day ends in one place and begins in another. Reports must say clearly "as of" which time and which zone.
- **Follow-the-sun support:** a service desk run from three regions so a ticket is always worked in daylight. Your SLA report must count the ticket as one case across all shifts, not three.
- **Calendar effect:** month-end close, board reviews and weekly operations calls sit on different dates and holidays (India and the US have different holiday lists). A data refresh that finishes at 2 a.m. India time lands on the previous calendar date for a US reader, so the "as of" date must be stated.
- **Practical habits:** one reporting time zone (often UTC or India time), a published calendar of cut-off, refresh, review and release dates, and a named backup when the owner is on leave.
- **HR parallel:** attendance cut-off for payroll has the same logic; everyone needs to know the date and the time zone.
**Likely follow-ups:** 1) *How do you handle a late source file?* Release on time with a clear "provisional" note rather than silently delaying. 2) *What if two regions want different cut-offs?* Agree one official cut-off and offer a secondary view if needed.
**Common mistakes:** Quoting times without a zone; mixing local dates and UTC dates so tickets fall into the wrong day; ignoring regional holidays when planning refresh dates.

### Q34 ⭐⭐ 🟢 What does attrition look like in IT services (voluntary, by band, by tenure, campus hires), and why is last-twelve-months attrition the standard way to report it?
**Asked at:** commonly asked (no company-specific report found); attrition metrics are standard HR analytics vocabulary.
**What the interviewer is checking:** Whether you can slice attrition sensibly and explain why a rolling 12-month view is used.
**Say this in the interview:** "Attrition is the share of employees who leave. In IT services I split it into voluntary and involuntary, then by band (grade), tenure and hiring source such as campus joiners. I report it on a last-twelve-months basis because a single month is too jumpy and has seasonal peaks, such as the period after appraisals."
**Explain simply:**
- **Voluntary attrition:** people who choose to resign. **Involuntary:** dismissals, end of contract, redundancy. Management mostly worries about voluntary.
- **By band:** juniors usually leave in larger numbers than seniors, but losing a few seniors costs more, so both are watched.
- **By tenure:** people with under one or two years of service often leave at a higher rate; this shows whether onboarding is working.
- **Campus hires:** freshers recruited from colleges; their first-year attrition shows the quality of the campus programme.
- **LTM (last twelve months):** exits in the last 12 months divided by average headcount over those 12 months. It smooths seasonality and monthly noise, and a 12-month figure is directly comparable with an annual number.
- Definitions vary by company (for example, whether contractors or retirements are counted), so always state yours.
**Likely follow-ups:** 1) *Why not use monthly attrition?* Month to month it swings with appraisal and bonus cycles. 2) *Why average headcount?* Headcount changes during the year; the average is fairer than opening or closing headcount.
**Common mistakes:** Dividing exits by closing headcount only; mixing voluntary and involuntary; comparing one company's annualised monthly figure with another's LTM figure.

### Q35 ⭐⭐ 🟢 What does first response time measure, and why should it be measured to a human reply rather than an automated acknowledgement?
**Asked at:** commonly asked (no company-specific report found); human-reply measurement is stressed in service-desk metric guides (vendor blogs, unverified).
**What the interviewer is checking:** Whether you understand that a metric can look good while the customer experience is poor.
**Say this in the interview:** "First response time is the gap between a ticket being raised and the first real reply from a person who engages with the problem. An automatic 'we received your request' email arrives in seconds, so counting it would make the number look perfect while the customer is still waiting."
**Explain simply:**
- **Ticket:** a logged request or problem from a user. **Service desk:** the team that handles these tickets.
- **First response time:** the clock starts when the ticket is created and stops at the first human reply.
- **Why not the auto-acknowledgement:** it is a receipt, not help. Counting it hides slow teams and makes every team look the same.
- **Practical rule:** the ticket tool should record a field such as "first human response timestamp", and the report excludes system-generated messages.
- **Business hours vs calendar hours:** state which clock you use, since a ticket raised on Friday evening looks very different on each.
- **HR parallel:** an HR helpdesk "your query is received" email is not a response to the employee's question.
**Likely follow-ups:** 1) *Is first response the same as resolution time?* No; response is the first reply, resolution is when the issue is fixed. 2) *How do you report it?* Median and 90th percentile, by priority.
**Common mistakes:** Counting automated emails; averaging across priorities; ignoring business-hours rules.

### Q36 ⭐⭐ 🟢 What are first-contact resolution, reopen rate and CSAT in service-desk reporting, and how do they balance speed metrics?
**Asked at:** commonly asked (no company-specific report found); these metrics appear in service-desk KPI guides (vendor blogs, unverified).
**What the interviewer is checking:** Whether you know that speed metrics need quality metrics beside them.
**Say this in the interview:** "Speed alone can be gamed: a team can close tickets fast and badly. So I pair response and resolution times with first-contact resolution, reopen rate and CSAT, which show whether the problem was actually fixed and whether the user was happy."
**Explain simply:**
- **First-contact resolution (FCR):** share of tickets solved in the first interaction without follow-up. Higher is better; it shows knowledge and good routing.
- **Reopen rate:** share of closed tickets the user reopens because the fix did not hold. A low number says closures are genuine.
- **CSAT (customer satisfaction score):** a short survey after closure, often a 1 to 5 rating; the score is usually the share of positive ratings. Survey response rates are low, so show the count of responses too.
- **Balance:** fast resolution with a high reopen rate and low CSAT means tickets are being closed too early.
- Definitions vary by company, so write each one on the report.
**Likely follow-ups:** 1) *Can FCR be too high?* If simple tickets dominate it flatters the team; segment by priority and type. 2) *What if CSAT responses are few?* Say so; do not over-read a handful of ratings.
**Common mistakes:** Reporting only averages of speed; treating CSAT from ten responses as reliable; counting a ticket as FCR when the user had to chase.

### Q37 ⭐⭐ 🟢 How would you set up an MIS requirement conversation with a stakeholder who asks for 'a report on utilisation'? Which questions do you ask first?
**Asked at:** commonly asked (no company-specific report found); requirement gathering is a standard MIS interview theme (prep sites, unverified).
**What the interviewer is checking:** Whether you clarify before building, instead of delivering the wrong report quickly.
**Say this in the interview:** "I would not start building. I first ask what decision the report supports, who reads it, how often, and what exactly 'utilisation' means to them, then agree the definition, the data source and a sample layout before I do any work."
**Explain simply:**
- **Purpose:** what decision will this change? (Move people between projects? Justify hiring? Review a manager?)
- **Definition:** gross or net utilisation, billable hours only or billable plus certain internal work, which employees are excluded (new joiners, long leave, managers).
- **Scope and cuts:** which business units, which period, by team, by band or by project; weekly or monthly.
- **Source and timing:** timesheet data, HR data for headcount and leave, cut-off date, who owns each source.
- **Format and users:** Excel, PDF or dashboard; who gets it; how targets or colours (RAG) are set.
- **Agree and confirm:** write down the definition and send back a mock-up for sign-off.
**Likely follow-ups:** 1) *What if the stakeholder cannot define it?* Propose a standard definition and test it with last month's data. 2) *What if the request changes later?* Keep a version note and a change log.
**Common mistakes:** Starting with the data; assuming everyone defines utilisation alike; skipping the sample layout; no sign-off.

### Q38 ⭐⭐ 🟢 What controls do you apply before an MIS pack goes to leadership (reconciliation to source, totals check, previous-month comparison, sign-off)?
**Asked at:** commonly asked (no company-specific report found); report accuracy is a standard MIS interview topic (prep sites, unverified).
**What the interviewer is checking:** Whether you have a habit of checking numbers before anyone senior sees them.
**Say this in the interview:** "Before release I run a fixed checklist: reconcile totals to the source system, check that parts add up to the total, compare with last month and investigate any large swing, and get a named reviewer to sign off. I keep the checklist so the process is repeatable."
**Explain simply:**
- **Reconciliation to source:** the pack's headcount or hours must match the system of record (HRMS, timesheet tool, finance ledger) at the same cut-off date, or the gap must be explained.
- **Totals check:** sub-totals by team must add up to the grand total; percentages must be recomputed from the underlying counts.
- **Previous-month comparison:** big movements are either real events or errors (duplicate rows, a missing team, a changed filter). Find out which before release.
- **Sense checks:** no negative hours, no blank team names, no employee in two teams.
- **Sign-off:** a second person (maker and checker) reviews, and the sign-off is recorded with the date and data version.
- **Version control:** keep a copy of the exact data used so the number can be reproduced later.
**Likely follow-ups:** 1) *What if you find an error after release?* Inform readers promptly, send a corrected version and note what changed. 2) *Can the checks be automated?* Yes, as formulas or scripts flagging differences above a tolerance.
**Common mistakes:** Checking only formulas, not source agreement; no reviewer; overwriting last month's file so comparison is impossible.

### Q39 ⭐⭐ 🟢 What is effort variance and schedule variance on a software project, and how are they calculated?
**Asked at:** commonly asked (no company-specific report found); effort and schedule variance are standard project-management metrics (general practice, unverified for any specific company).
**What the interviewer is checking:** Whether you can state both formulas and the sign convention.
**Say this in the interview:** "Effort variance compares actual effort with planned effort: (actual minus planned) divided by planned, as a percentage. Schedule variance compares actual duration with planned duration the same way. Positive means overrun. Some companies use the earned-value version of schedule variance instead, so I state which one I use."
**Explain simply:**
- **Person-hours (effort):** hours worked by people on the project; the main cost in services.
- **Effort variance % = (actual effort minus planned effort) / planned effort x 100.** Positive is over budget in effort.
- **Schedule variance % = (actual duration minus planned duration) / planned duration x 100,** measured in days or weeks until the milestone is hit.
- **Earned-value version:** schedule variance = earned value minus planned value (a number, not a percentage). Same name, different formula; define yours.
- **Why both:** a project can finish on time by adding people (schedule fine, effort variance high).
- **HR parallel:** planned versus actual hours for a recruitment drive.
**Likely follow-ups:** 1) *Is a negative variance always good?* Not necessarily; it may mean work was skipped or estimates were padded. 2) *Which is used for RAG?* Often both, with thresholds agreed in advance.
**Common mistakes:** Flipping the sign; dividing by actual instead of planned; mixing the two schedule-variance formulas.

### Q40 ⭐⭐ 🟢 What are the Workday concepts of worker, position, supervisory organisation and business process, in plain words?
**Asked at:** commonly asked (no company-specific report found); Workday concepts appear in HRIS analyst prep pages from training vendors (unverified). Workday details below are from memory, unverified.
**What the interviewer is checking:** Whether you know the basic building blocks of the HR system you would report from.
**Say this in the interview:** "In Workday, a worker is the person, a position is a seat in the organisation that can be filled or vacant, a supervisory organisation is a reporting group under a manager, and a business process is the approval workflow for any change such as a hire or transfer. This is from memory; I would confirm with the company's own setup."
**Explain simply:**
- **Worker:** the person record, either an employee or a contingent (contract) worker. In companies that manage headcount by position, the worker fills a position.
- **Position:** a defined seat in the structure (job title, location, cost centre). It can be vacant, so it supports headcount-plan versus actual reporting.
- **Supervisory organisation:** the manager-led team structure; the tree of these shows who reports to whom and is the basis for team-level reports and security.
- **Business process:** a workflow for a change (hire, transfer, termination, compensation change) with initiation, approval steps and completion. Data changes only after the process completes.
- **Analyst's view:** reports by team come from supervisory organisation, vacancy reports from position, and "pending" changes from business process status.
**Likely follow-ups:** 1) *Is a position the same as a person?* No; a position can be empty. 2) *Why does business process status matter?* Half-approved changes are not yet effective in the data.
**Common mistakes:** Treating positions as headcount; ignoring contingent workers; assuming terminology is identical in every HRIS.

### Q41 ⭐⭐ 🟢 What does 'effective dating' mean in an HRIS like Workday, and how does it affect headcount-as-of-date and attrition reports?
**Asked at:** commonly asked (no company-specific report found); effective dating is a standard HRIS concept (training-vendor prep pages, unverified). Workday details are from memory, unverified.
**What the interviewer is checking:** Whether you understand why the same question can give different answers depending on the date you ask it.
**Say this in the interview:** "Effective dating means each change in an HR record has a date from which it applies, so the system keeps history. To get headcount as of a date, I must pick the record version effective on that date, otherwise I count people who had already left, or miss people who had not yet started."
**Explain simply:**
- **Effective date:** the date a change takes effect, which may differ from the date it was entered (a resignation entered on the 28th may be effective the 15th).
- **History is kept:** a worker may have several rows over time (hire, promotion, transfer, termination). Each row is valid from its effective date until the next.
- **Headcount as of date:** keep workers whose hire date is on or before the date and who have no termination effective on or before it. Use the version effective on that date for team and cost centre.
- **Attrition:** exits belong to the month of the termination effective date, not the entry date; late-entered terminations (back-dating) can change past months, so figures can restate.
- **Future-dated changes:** a hire dated next month exists in the system today but must not count in today's headcount.
- **HR parallel:** a back-dated salary revision in payroll arrears.
**Likely follow-ups:** 1) *Why do last month's numbers change?* Back-dated entries. Freeze snapshots at each month-end if you need stable reporting. 2) *As-of date versus entry date?* Use effective date for business truth, entry date for audit.
**Common mistakes:** Using the latest row only; counting future-dated hires; not saying which date a report uses.

### Q42 ⭐⭐ 🟢 What are the main Workday report types (simple, advanced, matrix, composite) and when would you choose each?
**Asked at:** commonly asked (no company-specific report found); report types appear on Workday training-vendor pages (unverified). Details below are from memory, unverified.
**What the interviewer is checking:** Whether you can pick a tool by the shape of the question.
**Say this in the interview:** "From memory: a simple report is a flat list from one data source, an advanced report is the full-featured list with filters and calculated fields, a matrix report is a pivot-style summary with counts or totals, and a composite report stitches several reports together. I choose by whether I need a list, a summary, or a combination."
**Explain simply:**
- **Simple report:** a quick list, such as workers in a team. Limited features.
- **Advanced report:** the workhorse; many fields, filters, sorting, grouping, calculated fields and sharing; used for most operational lists and for data feeding other tools.
- **Matrix report:** rows and columns with counts or sums, like a pivot table (headcount by location by gender).
- **Composite report:** combines several reports (for example, one built for each business unit) into one output; used for complex reporting needs.
- **Rule of thumb:** list of people, advanced; summary grid, matrix; one pack from many sources, composite.
- Available types and names can change with Workday releases, so verify in the tenant (the company's own Workday instance).
**Likely follow-ups:** 1) *Which would you use for a monthly headcount by department?* Matrix, or advanced with a grouping. 2) *Why advanced over simple?* Filters and calculated fields.
**Common mistakes:** Using simple reports for everything; building a pivot in Excel when a matrix report exists; not checking who has access to the report.

### Q43 ⭐⭐ 🟢 How does Workday Prism Analytics differ from standard Workday reporting, and when would an HR team need it?
**Asked at:** commonly asked (no company-specific report found); Prism versus standard reporting appears on training-vendor pages (unverified). Details below are from memory, unverified.
**What the interviewer is checking:** Whether you know when built-in reporting is enough and when you need to bring in outside data.
**Say this in the interview:** "From memory: standard Workday reporting works on Workday data in real time. Prism Analytics lets a team bring in external data, for example from a survey or finance system, blend it with Workday data and report on the combined set. An HR team needs it when a question spans Workday and another source, or when the data volume is large."
**Explain simply:**
- **Standard reporting:** quick, real-time, only Workday data, no extra licence needed beyond the base product (as I recall; confirm).
- **Prism Analytics:** an add-on to load, transform and combine outside data sets with Workday data into tables you can report on, with Workday security.
- **Example:** link engagement survey scores from a survey tool to Workday attrition and tenure.
- **Trade-offs:** extra cost, set-up time and governance effort; if the question is only about Workday fields, standard reporting is simpler.
- **Alternative:** export to a BI tool or warehouse (Power BI, SQL); this may be cheaper but must respect data privacy and security.
**Likely follow-ups:** 1) *Why not just use Excel?* Manual copies break security and go stale. 2) *Who should build Prism data sets?* A trained analyst with HR data-owner approval.
**Common mistakes:** Proposing Prism for a simple list; ignoring licence cost; forgetting that blended data still needs access controls.

### Q44 ⭐⭐ 🟢 What are the main Alteryx tools (Input, Select, Filter, Formula, Summarize, Cross Tab, Unique, Output) and what does each do?
**Asked at:** commonly asked (no company-specific report found); Alteryx tool lists appear in prep guides from DataCamp and others (unverified). Tool descriptions below are from memory, unverified.
**What the interviewer is checking:** Whether you know the basic vocabulary of the tool well enough to build a simple workflow.
**Say this in the interview:** "Input reads data, Select picks and renames columns and changes data types, Filter keeps rows meeting a condition, Formula creates or changes a column, Summarize groups and aggregates, Cross Tab pivots rows into columns, Unique removes duplicates, and Output writes the result. A workflow connects them left to right."
**Explain simply:**
- **Alteryx:** a drag-and-drop data preparation tool; each box is a "tool" and lines connect them.
- **Input Data:** reads Excel, CSV or database tables. **Output Data:** writes results to a file or table.
- **Select:** choose, rename, reorder columns and set data types (text, number, date).
- **Filter:** splits rows into true and false outputs by a condition, such as status = Active.
- **Formula:** adds a new column by calculation, such as hours divided by available hours.
- **Summarize:** like a pivot or GROUP BY: sums, counts, averages by group.
- **Cross Tab:** turns row values into columns (months across the top); the opposite is Transpose.
- **Unique:** keeps one record per key and sends duplicates to a separate output.
**Likely follow-ups:** 1) *Which tool replaces VLOOKUP?* Join. 2) *Which is the SQL GROUP BY?* Summarize.
**Common mistakes:** Forgetting to set data types in Select so joins fail; dropping duplicates without looking at them; not documenting the workflow.

### Q45 ⭐⭐ 🟢 What is data privacy awareness in a GCC context: why must you be careful with employee and client data, and what do the EU GDPR and India's DPDP Act mean for an analyst in plain words?
**Asked at:** commonly asked (no company-specific report found); privacy awareness is a common behavioural and domain topic for GCC roles (unverified).
**What the interviewer is checking:** Whether you treat personal and client data with care and know the basic ideas of the two main privacy laws.
**Say this in the interview:** "Employee and client data identify real people and confidential business, so I use only what I need, share it only with authorised people, and mask or aggregate it when I can. GDPR is the European Union's privacy law and India's DPDP Act is the Indian one; both are about lawful, limited use of personal data. This is awareness only; I would follow my company's compliance team."
**Explain simply:**
- **Personal data:** anything that identifies a person: name, employee ID, salary, health leave, performance rating.
- **GCC context:** the GCC often handles data of the parent company's staff and customers in other countries, so the rules of those countries may apply, and the client contract may add rules.
- **GDPR (from memory, unverified):** the EU law on personal data; principles include a lawful reason, collecting only what is needed, keeping it only as long as needed, and keeping it secure.
- **DPDP Act (India, from memory, unverified):** India's data protection law; centred on consent and notice, purpose limitation and responsibility of the organisation holding the data. Rules and dates are still being phased in as I recall; confirm.
- **Analyst habits:** minimum data, aggregate or anonymise, no data on personal email or chat, no downloads to unsecured devices, suppress tiny groups (a team of two shows an individual's salary).
**Regulation / privacy note (awareness only):** from memory, unverified, confirm with the compliance or legal team; this is not legal advice.
**Likely follow-ups:** 1) *You accidentally email salary data to the wrong person; what next?* Report it immediately through the company's incident process. 2) *Can you use production data for testing?* Only if masked or approved.
**Common mistakes:** Sharing a full extract when a summary would do; assuming internal data is not sensitive; hiding a mistake.

### Q46 ⭐⭐ 🟡 A consultant bills at INR 2,000 per hour and costs INR 1,100 per hour. If they bill 140 hours in a month, what are revenue, direct cost and gross margin percentage?
**Asked at:** commonly asked (no company-specific report found); billing versus cost rate is standard professional-services arithmetic.
**What the interviewer is checking:** Basic margin arithmetic and clean units.
**Say this in the interview:** "Revenue is rate times hours, direct cost is cost rate times hours, and gross margin is revenue minus cost, shown as a percentage of revenue. Here revenue is INR 2.80 lakh, cost INR 1.54 lakh and gross margin 45%."
**Explain simply:**
- **Billing rate:** what the client pays per hour. **Cost rate:** what the company spends per hour on that person (salary plus benefits, spread over hours).
- **Gross margin:** revenue left after direct people cost, before overheads such as rent and management.
- The percentage is of revenue, not of cost; the percentage on cost (markup) would be a different number.
**Worked example:** All figures computed by code; INR; 1 lakh = 100,000.
- Revenue = 140 x 2,000 = INR 280,000 (2.80 lakh).
- Direct cost = 140 x 1,100 = INR 154,000 (1.54 lakh).
- Gross margin = 280,000 - 154,000 = INR 126,000 (1.26 lakh).
- Gross margin % = 126,000 / 280,000 = 45.0% (exact, no rounding). Per hour the margin is INR 900 (2,000 - 1,100).
**Likely follow-ups:** 1) *What if only 120 of the 140 hours could be billed?* Revenue falls but cost stays, so margin shrinks. 2) *Margin versus markup?* Markup is 126,000 / 154,000 = 81.8% on cost.
**Common mistakes:** Dividing by cost instead of revenue; mixing rupees and lakh; using salary alone as cost rate.

### Q47 ⭐⭐ 🟡 A project logged 1,000 billable hours at a standard rate of INR 1,500. After client discounts and write-offs the invoice was INR 13.2 lakh. What is the realisation rate, and what do you check if it falls?
**Asked at:** commonly asked (no company-specific report found); realisation is a standard professional-services metric (vendor blogs, unverified).
**What the interviewer is checking:** That you can compute realisation and think about causes of leakage.
**Say this in the interview:** "Realisation is what we actually invoiced divided by what the hours were worth at standard rate. Here standard value is INR 15 lakh and the invoice is 13.2 lakh, so realisation is 88%. If it falls I look at discounts, write-offs, rate card exceptions and unbilled work."
**Explain simply:**
- **Standard rate (rack rate):** the company's list price per hour.
- **Realisation:** invoiced amount divided by standard value of hours worked. It measures pricing and billing leakage; utilisation measures how many hours are billable.
- **Gap of INR 1.8 lakh** here is discounts plus write-offs (hours done but not charged).
- **What to check when it falls:** negotiated discounts versus rate card; hours written off and the reason (rework, scope creep, client dispute); fixed-price effort overruns; wrong rate applied; billing delays.
**Worked example:** Computed by code; INR.
- Standard value = 1,000 x 1,500 = INR 15,00,000 (15 lakh).
- Invoice = INR 13,20,000 (13.2 lakh).
- Realisation = 13.2 / 15 = 88.0% (exact).
- Leakage = 15 - 13.2 = INR 1.8 lakh, which is 12.0% of standard value (12 percentage points below 100%).
**Likely follow-ups:** 1) *Is 88% good?* Depends on the contract mix and company targets; I would compare with its own history. 2) *Can realisation exceed 100%?* Yes, with premium rates or pass-through billing.
**Common mistakes:** Confusing realisation with utilisation; ignoring write-offs recorded in a different system; comparing across contract types.

### Q48 ⭐⭐ 🟡 Using the staffing below, compute the pyramid shares and the average cost per head, and say which direction you would move the mix for a fixed-price project.
Junior (cost INR 6 lakh): 50 | Mid (INR 12 lakh): 30 | Senior (INR 24 lakh): 15 | Lead (INR 40 lakh): 5
**Asked at:** commonly asked (no company-specific report found); pyramid analysis is standard IT-services vocabulary (research notes, unverified).
**What the interviewer is checking:** Weighted-average arithmetic and the cost logic of team mix.
**Say this in the interview:** "The mix is 50% junior, 30% mid, 15% senior and 5% lead, and the average cost is INR 12.2 lakh per head. For a fixed-price project I would shift the mix toward the cheaper levels, as far as quality and delivery risk allow, because the price is fixed and cost is what I control."
**Explain simply:**
- **Pyramid:** many juniors at the base and few leads at the top. Cheaper mix means higher margin on fixed-price work.
- **Fixed-price:** revenue is set in advance, so every rupee of staffing cost saved goes into margin. On time-and-materials work revenue grows with hours instead.
- **Limit:** too few seniors means rework, delays and review problems, which raise effort, so the saving can disappear.
**Worked example:** Total 100 people; INR lakh per year; computed by code.
- Shares: Junior 50 / 100 = 50%; Mid 30%; Senior 15%; Lead 5% (percent of headcount).
- Cost by level: 50 x 6 = 300; 30 x 12 = 360; 15 x 24 = 360; 5 x 40 = 200; total 1,220 lakh.
- Average cost per head = 1,220 / 100 = INR 12.2 lakh.
- Seniors and leads are 20% of heads but 45.9% of cost (560 of 1,220).
- Illustration: moving to 55 junior, 30 mid, 12 senior and 3 lead gives 10.98 lakh average, about 10% lower (my own made-up alternative mix).
**Likely follow-ups:** 1) *Which direction?* Toward more juniors per senior, with enough review capacity. 2) *What would you check first?* Rework and defect rates by level.
**Common mistakes:** Simple average of 6, 12, 24 and 40 instead of weighting by headcount; ignoring quality risk; mixing share of heads with share of cost.

### Q49 ⭐⭐ 🟡 A company with average headcount of 8,000 earned INR 1,200 crore revenue in a quarter. What is annualised revenue per employee in INR lakh, and what caveats apply when comparing it with another company?
**Asked at:** commonly asked (no company-specific report found); revenue per employee is standard IT-services vocabulary in industry notes (unverified).
**What the interviewer is checking:** Unit handling (crore vs lakh), annualising correctly, and knowing a ratio is not a like-for-like score.
**Say this in the interview:** "Annualised revenue is 4 x 1,200 = INR 4,800 crore. Divided by 8,000 people that is INR 60 lakh per employee per year. I would not compare it with another company until I know their definitions."
**Explain simply:**
- Units: 1 crore = 100 lakh, so INR 4,800 crore = 4,80,000 lakh; 4,80,000 / 8,000 = 60.
- Annualising means multiplying one quarter by 4. It assumes the quarter is typical; a seasonal quarter distorts it.
- Quarterly figure for reference: 1,200 crore / 8,000 = INR 15 lakh per employee per quarter.
**Worked example:** All figures computed by script. Annual revenue 4 x 1,200 = 4,800 crore; per employee 60.0 lakh (no rounding needed).
**Likely follow-ups:** 1) *Why use average headcount?* Headcount changes in the quarter; the average matches revenue earned over the whole period. 2) *Is higher always better?* No; it can mean high-value work or just fewer people carrying heavy load.
**Common mistakes:** Mixing crore and lakh; forgetting to multiply by 4; comparing companies that count subcontractors differently, have a different mix of onsite and offshore work, report in different currencies, or differ in how much of the work is product vs services (caveats to name).

### Q50 ⭐⭐ 🟡 Timesheet compliance is 78% on the cut-off date. How would you define compliance, find the defaulters by team, and report it without blaming individuals?
**Asked at:** commonly asked (no company-specific report found); timesheet compliance is a gap-fill topic, not named by sources.
**What the interviewer is checking:** That you define a metric precisely before reporting it, and handle people data with care.
**Say this in the interview:** "I would define compliance as people who submitted a complete timesheet by the cut-off, divided by people expected to submit. Then I would show it by team and report team-level numbers, with names going only to the managers who need to chase."
**Explain simply:**
- Denominator matters: expected people only (exclude those on approved leave, new joiners not yet onboarded, non-billable roles if policy says so). Say which rules you used.
- "Complete" can mean all working days filled, or hours matching the standard. Pick one and label it.
- Show the number by team, with the count of people behind each percentage, so a team of 3 is not read like a team of 300.
- Report gaps as a process view: "Team Beta is at 50%; the common reason is late project code approval" instead of naming individuals to leadership.
**Worked example:** SQL on a small invented table (billable people only, one week).
```sql
select e.team,
       count(*) as expected_people,
       sum(t.submitted) as submitted_on_time,
       round(100.0 * sum(t.submitted) / count(*), 1) as compliance_pct
from employee e
join timesheet_status t on t.emp_id = e.emp_id
where e.is_billable = 1 and t.week_end = '2026-11-13'
group by e.team
order by compliance_pct;
```
Sample rows: Alpha has 3 billable people (2 submitted), Beta has 4 (2 submitted). Output: Beta 4 expected, 2 submitted, 50.0%; Alpha 3 expected, 2 submitted, 66.7%. Plain words: lowest-compliance team first; the people list is a separate query shared only with managers.
**Likely follow-ups:** 1) *Does 78% mean 22% are lazy?* No; check leave, system access, approval delays first. 2) *Daily or weekly?* Whatever the policy cut-off is; state it.
**Common mistakes:** Counting people on leave as defaulters; changing the denominator between weeks; publishing a name list to the whole company.

### Q51 ⭐⭐ 🟡 Open demand is 120 roles against 35 people on bench. What first cuts of data would you make to see whether the bench can fill the demand?
**Asked at:** commonly asked (no company-specific report found); bench and demand matching appears in IT-services metric pages (unverified).
**What the interviewer is checking:** That you know supply and demand must match on skill, level, location and timing, not just on count.
**Say this in the interview:** "On count alone the bench covers 35 of 120 roles, about 29%, leaving 85 open. But I would cut both lists by skill, grade, location and start date to see how many of the 35 actually fit."
**Explain simply:**
- Bench means employees employed but not currently assigned to a billable project. Demand is open requests from projects for people.
- A matching table has the same columns on both sides: skill, grade, location, start date, client or clearance restrictions.
- Many of the 35 may be freshers in training, people on notice period or on long leave; count only deployable people.
- The gap by skill tells the business whether to hire, retrain or move people across locations.
**Worked example:** 35 / 120 = 29.2% coverage at best (computed); gap at best 120 - 35 = 85 roles. Real coverage is lower once skill and location filters apply.
**Data and tables involved:** Demand table (request ID, skill, grade, location, needed-by date, priority); bench table (employee ID, skills, grade, location, available-from, status); employee master. First cuts: count by skill, then grade, then location, then date.
**Likely follow-ups:** 1) *What if skills do not match?* Look at reskilling time and cost against hiring time. 2) *Which demand first?* Highest priority and earliest start date.
**Common mistakes:** Comparing headline counts only; including people who are not actually available; ignoring the timing of when demand starts.

### Q52 ⭐⭐ 🟡 Invoices outstanding are INR 9 crore and quarterly revenue is INR 30 crore (90 days). Compute DSO and say what an ageing bucket report adds.
**Asked at:** commonly asked (no company-specific report found); DSO is a gap-fill topic, not named by sources.
**What the interviewer is checking:** Whether you can compute DSO and know its blind spots.
**Say this in the interview:** "DSO is 9 / 30 x 90 = 27 days: on average we wait about 27 days to collect after billing. An ageing report shows how that is spread across old and new invoices."
**Explain simply:**
- DSO (days sales outstanding) = receivables divided by revenue, multiplied by days in the period. Receivables are money customers owe us.
- It is an average, so a few very old invoices can hide inside a healthy-looking number.
- An ageing bucket report groups unpaid invoices by days overdue (for example 0-30, 31-60, 61-90, 90+), usually by client. It shows who is late and how much is at risk.
- Companies differ on whether to use billed amount or revenue and on whether to include tax; state your definition.
**Worked example:** 9 / 30 = 0.3; x 90 days = 27.0 days (computed).
**Likely follow-ups:** 1) *DSO is rising; why?* Slower client payments, delayed invoicing, or disputes; the ageing report points to which. 2) *Why unbilled revenue?* Work done but not yet invoiced is a separate bucket worth tracking.
**Common mistakes:** Mixing crore with lakh; using 365 days with quarterly revenue; reporting only the average.

### Q53 ⭐⭐ 🟡 A delivery unit had 1,000 employees on average over the last 12 months and 180 left. Quarterly exits were 40, 50, 45 and 45. Compute LTM attrition and the annualised rate of the latest quarter.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Correct denominator use and annualising a quarterly figure.
**Say this in the interview:** "LTM (last twelve months) attrition is 180 / 1,000 = 18%. The latest quarter's 45 exits give 4.5% for the quarter, which annualises to 18%, so the recent pace matches the year."
**Explain simply:**
- Attrition rate = exits divided by average headcount over the same period. Check the data: 40+50+45+45 = 180, which matches the 180 leavers, so the inputs are consistent.
- Annualising a quarter: multiply by 4 (simple method). This assumes the quarter is typical.
- The quarterly rate uses the same 1,000 average (given for the year); in practice use that quarter's own average headcount.
- Definitions differ across firms (voluntary only, or all exits); state yours.
**Worked example:** LTM = 180 / 1,000 = 18.0%. Latest quarter = 45 / 1,000 = 4.5%; x 4 = 18.0% (both computed).
**Likely follow-ups:** 1) *Quarter 2 had 50 exits?* 50 / 1,000 x 4 = 20% annualised, the peak. 2) *Voluntary vs involuntary?* Split them; they need different actions.
**Common mistakes:** Dividing by closing headcount; adding quarterly percentages without matching denominators; calling 4.5% "attrition" without saying it is not annual.

### Q54 ⭐⭐ 🟡 Why is 'MTTR' ambiguous in service-desk reports, and how would you label and define it in your MIS so stakeholders do not argue?
**Asked at:** commonly asked (no company-specific report found); MTTR ambiguity is noted on service-desk metric pages (unverified).
**What the interviewer is checking:** Awareness that one acronym can hide several different measures.
**Say this in the interview:** "MTTR is used for mean time to repair, recover, resolve and respond, and each starts and ends the clock at different points. I would never publish 'MTTR' alone; I would label each one and write the start and stop events beside it."
**Explain simply:**
- Mean time to respond: ticket created to first human reply. Mean time to resolve: created to marked resolved. Mean time to restore/recover: from outage start to service back. (Standard usage; vendors vary.)
- Questions to settle: does the clock pause while waiting for the customer? Is it calendar or business hours? Is the end "resolved" or "closed"?
- Add a definitions box on the report: name, formula, clock start, clock stop, pauses, hours basis, priority covered.
- Prefer median or percentiles alongside the mean, because a few very long tickets inflate averages.
**Likely follow-ups:** 1) *Mean or median?* Show both; the gap tells you about outliers. 2) *Who owns the definition?* The service owner signs it off, I keep a data dictionary.
**Common mistakes:** Calling it just "MTTR"; changing the definition mid-year; averaging across priorities with very different targets.

### Q55 ⭐⭐ 🟡 Open tickets are 400 this week against 300 last week, while new tickets are flat. What does a ticket backlog and ageing report show, and what would you check next?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you reason with the flow identity and look past the headline number.
**Say this in the interview:** "Open backlog = last week's open + new tickets - closed tickets. New is flat, so the 100 extra open tickets mean we closed about 100 fewer than usual. I would check why closures fell, and how old the extra tickets are."
**Explain simply:**
- A backlog report counts tickets still open now; an ageing view splits them by how long they have been open (0-2 days, 3-7, 8-30, 30+).
- If the new 100 are mostly young, it is a temporary slowdown; if old, work is stuck.
- Next checks: closures by team and priority, staff on leave, tickets waiting on the customer, a reassignment pile-up, a new ticket type taking longer, or a system change.
- Also check the first-contact vs later-tier handoffs and reopened tickets.
**Worked example:** 400 - 300 = 100 net increase (computed), a 33.3% rise. With flat intake, the closure shortfall is also 100 versus last week's closures.
**Likely follow-ups:** 1) *Is flat intake definitely flat?* Check the definition (created vs reopened). 2) *What do you tell the manager?* Backlog grew by a third because closures dipped; here is where the oldest tickets sit.
**Common mistakes:** Blaming demand when intake is flat; not showing ageing; counting pending-customer tickets as stuck on the team.

### Q56 ⭐⭐ 🟡 Compute SLA compliance by priority and the blended figure, and say why the blended figure misleads.
P1: 20 tickets, 15 within SLA | P2: 100, 85 | P3: 400, 380 | P4: 480, 470
**Asked at:** commonly asked (no company-specific report found); SLA by priority is standard on service-desk metric pages (unverified).
**What the interviewer is checking:** Weighted averages and the habit of segmenting before summarising.
**Say this in the interview:** "P1 is 75%, P2 85%, P3 95%, P4 97.9%, and blended 95%. The blend looks healthy only because most tickets are low priority; the critical ones are failing."
**Explain simply:**
- SLA (service level agreement) is the promised time to respond or fix. Compliance = tickets within SLA / total tickets.
- Priority means business impact: P1 is the most urgent (for example a service outage).
- Blended = total within SLA / total tickets, weighted by volume, so P4's 480 tickets dominate P1's 20.
- Report by priority first; the blend is a footnote. With only 20 P1 tickets, 5 breaches swing it hard, so show counts.
**Worked example:** All computed: P1 15/20 = 75.0%; P2 85/100 = 85.0%; P3 380/400 = 95.0%; P4 470/480 = 97.9% (rounded to 1 decimal). Blended: (15+85+380+470) / 1,000 = 950 / 1,000 = 95.0%. The simple average of the four rates would be 88.2%, also not right, because it ignores volumes.
**Likely follow-ups:** 1) *Which would you fix first?* P1 (75% against a likely 95%+ target; targets vary). 2) *Weighted by importance?* Possible, but publish the rule.
**Common mistakes:** Averaging the percentages; reporting only the blend; ignoring small samples.

### Q57 ⭐⭐ 🟡 A monthly MIS shows headcount of 2,040 but the HRMS shows 2,015. List the likely reasons and how you would trace the 25-person difference.
**Asked at:** commonly asked (no company-specific report found); reconciliation is core MIS work in the sources.
**What the interviewer is checking:** Systematic reconciliation rather than guessing.
**Say this in the interview:** "A 25-person gap (about 1.2%) is almost always a definition or timing issue. I would compare the two employee ID lists, classify every mismatch, and fix the rule or the source."
**Explain simply:**
- Typical reasons: different snapshot dates; leavers still in MIS; joiners in one but not the other; contractors or interns counted in one; employees on leave or on notice period; duplicate IDs after rehire or transfer; manual overrides in the Excel.
- Method: pull both ID lists, do an outer join, and label each of the 25 as "only in MIS", "only in HRMS". Tag each with a reason.
- Then check that the sum of reasons equals 25, and agree one definition (for example "active employees on the last day of the month, excluding contractors").
- Document the bridge: MIS 2,040 - reason A - reason B = HRMS 2,015.
**Worked example:** 2,040 - 2,015 = 25 (computed), 1.23% of MIS headcount.
**Likely follow-ups:** 1) *Which system is right?* The system of record for the definition, but verify. 2) *Prevent it?* Automated monthly reconciliation and a refresh timestamp.
**Common mistakes:** Adjusting the total by 25 with no trace; comparing different dates; fixing only this month.

### Q58 ⭐⭐ 🟡 A project estimated 2,000 person-hours and logged 2,350 with 70% of the work complete. Compute effort variance, and the forecast hours at completion if the current pace continues.
**Asked at:** commonly asked (no company-specific report found); formulas are standard project-control practice (unverified in this book).
**What the interviewer is checking:** Whether you compare like with like (hours against work done), not hours against the full budget.
**Say this in the interview:** "Raw variance is 350 hours over, 17.5%. But we are only 70% done, so at this pace the project finishes at about 3,357 hours, roughly 68% over the estimate."
**Explain simply:**
- Effort variance = (actual - estimate) / estimate. That gives 17.5% but compares part of the work to the full budget, so it understates the problem.
- Fair comparison: planned hours for the work done = 70% of 2,000 = 1,400. We used 2,350, so 950 hours (67.9%) over on the work finished so far.
- Forecast at completion at the current pace = actual / % complete = 2,350 / 0.70 = 3,357 hours; extra beyond estimate about 1,357 hours.
- The pace assumption can be wrong; if the overrun was a one-off (a rework), forecast would be lower. State the assumption.
**Worked example:** All computed: 350 / 2,000 = 17.5%; earned 1,400 h; to-date overrun 950 h = 67.9%; forecast 3,357.1 h (rounded to 1 decimal), 1,357 h over = 67.9% above estimate. Remaining work at this pace: 3,357 - 2,350 = 1,007 hours.
**Likely follow-ups:** 1) *How reliable is the 70%?* Check how it is measured; self-reported percent complete is often optimistic. 2) *What to tell the client?* On a fixed-price deal this is cost leakage; discuss scope or revised plan.
**Common mistakes:** Stopping at 17.5%; forecasting by adding the same overrun again; trusting percent complete blindly.

### Q59 ⭐⭐ 🟡 A Workday headcount report shows 5% more people than payroll. What differences in definition (contingent workers, leave of absence, future-dated hires, terminations in the month) would you check?
**Asked at:** commonly asked (no company-specific report found); HRIS analyst prep pages exist (unverified).
**What the interviewer is checking:** That you know HR systems and payroll count people on different rules.
**Say this in the interview:** "Different systems answer different questions: the HR system counts people in employment relationships on a date, payroll counts people paid in a period. I would line up definitions first and then reconcile by ID."
**Explain simply:** (Workday behaviour from memory, unverified; the logic holds for any HRIS.)
- Contingent workers: the HR system may hold them as a separate worker type; payroll often does not pay them, since they are paid through vendors.
- Leave of absence: on unpaid leave they are still employees in the HRIS but may be off payroll that month.
- Future-dated hires: entered in the HR system with a joining date ahead, counted by a report that ignores the as-of date; payroll has no pay yet.
- Terminations in the month: HRIS reports as of month-end exclude them, payroll includes them if paid for part of the month (final settlement).
- Also check the as-of date, legal entity or country scope, and inter-company transfers.
**Worked example:** If payroll is 10,000, a 5% excess is 10,500, a gap of 500 people (illustrative, computed). Tag each of the 500 by reason; the buckets should sum to 500.
**Regulation / privacy note (awareness only):** Reports containing named employees should be shared only with those entitled to see them (from memory, unverified, confirm with the compliance/legal team).
**Likely follow-ups:** 1) *Which total is right?* Neither; they have different definitions, so publish a bridge. 2) *Report as-of date?* State it in the title.
**Common mistakes:** Trusting one system; ignoring the as-of date; forgetting contingent workers.

### Q60 ⭐⭐ 🟡 Why is employee data in an HRIS sensitive, and how do role-based security and anonymisation protect it when you build and share reports?
**Asked at:** commonly asked (no company-specific report found); privacy is a gap-fill topic.
**What the interviewer is checking:** Whether you treat people data responsibly in your daily work.
**Say this in the interview:** "HR data can harm people if it leaks or is misused: salary, health, performance, family details. I limit access by role and share aggregates, not names, unless there is a need."
**Explain simply:**
- Sensitive items: pay, appraisal ratings, medical leave, disciplinary history, ID numbers, bank details, home address, dependants.
- Role-based security: each user sees only what the role needs (a manager sees their team; payroll sees salary; an analyst may see anonymised data). Access is given by role, not person by person.
- Anonymisation: replace names or IDs with codes or remove them, and report groups. Watch for small groups: a team of 2 with an average salary reveals both salaries; hide groups below a minimum size (a common rule, for example 5, set by policy).
- Practical habits: share only what was requested, no personal data in emails or screenshots, mask columns, and log who gets what.
**Regulation / privacy note (awareness only):** Rules such as India's DPDP Act and GDPR set consent, purpose and security expectations for personal data (from memory, unverified, confirm with the compliance/legal team).
**Likely follow-ups:** 1) *Is anonymised data safe?* Not always; small groups or combined fields can re-identify. 2) *A manager asks for peer salaries?* Escalate to HR policy owners.
**Common mistakes:** Emailing raw extracts; pivot tables with tiny groups; reusing a file for a different purpose.

### Q61 ⭐⭐ 🟡 In Alteryx, how would you find records that appear in last month's file but not in this month's file, and how would you remove duplicates?
**Asked at:** commonly asked (no company-specific report found); Join and Unique topics appear on Alteryx prep pages (unverified).
**What the interviewer is checking:** That you know the Join tool's outputs and the Unique tool.
**Say this in the interview:** "I join last month's file to this month's on the employee ID and take the Left output of the Join tool, which holds records only in last month's file. For duplicates I use the Unique tool on the key."
**Explain simply:** (Alteryx details from memory, unverified.)
- Join tool has three outputs: L (left only: in file one, not in file two), J (matched in both), R (right only). Here: last month on left, this month on right, so the L output is the "dropped" records (for example leavers).
- Swap the inputs, or read the R output, to find new records.
- Unique tool: choose the fields that define a duplicate (employee ID); it gives a U output of first-seen records and a D output of the repeats you removed. Check the D output before discarding.
- Make sure the join key has the same data type and trimmed spaces on both sides, or good matches will fall into L and R.
**Likely follow-ups:** 1) *Same in Excel/SQL?* SQL: left join where right key is null, or `not exists`. 2) *Which duplicate is kept?* Sort first so the right record comes first.
**Common mistakes:** Joining on name instead of ID; forgetting that spaces or case break matches; deleting duplicates without looking at them.

### Q62 ⭐⭐ 🟡 Describe an Alteryx workflow that merges a timesheet extract with an HRMS employee file and produces utilisation by team, listing the tools in order.
**Asked at:** commonly asked (no company-specific report found); tool names are from prep pages (unverified).
**What the interviewer is checking:** That you can lay out a clean data pipeline in the right order.
**Say this in the interview:** "Two Input Data tools, clean both, join on employee ID, calculate utilisation, summarise by team, then output. I would check row counts after the join."
**Explain simply:** (Alteryx tool names and behaviour from memory, unverified.)
1. Input Data (timesheet extract) and Input Data (HRMS employee file).
2. Select: keep needed fields, fix data types.
3. Data Cleansing: trim spaces, fix case on the employee ID.
4. Unique on HRMS ID: one row per employee (check the duplicates output).
5. Summarize timesheet to employee: sum billable hours and total hours.
6. Join on employee ID: timesheet totals (left) with HRMS (right); inspect the L and R outputs for unmatched people.
7. Formula: utilisation = billable hours / available hours (state the definition; firms differ). Available hours are in neither file above: take standard hours for the month less holidays and leave, from a calendar or leave file joined in here.
8. Summarize by team: sum of billable hours and available hours, then divide again (so utilisation is weighted, not an average of percentages).
9. Sort, then Output Data (Excel or a table for Power BI).
**Data and tables involved:** Timesheet (employee ID, date, project, hours, billable flag); HRMS (employee ID, team, grade, joining date, status, location).
**Likely follow-ups:** 1) *Row count after join looks too high?* Duplicate IDs on the right created a fan-out. 2) *Leavers?* Prorate available hours.
**Common mistakes:** Averaging team percentages; skipping the unmatched-ID check; joining before aggregating.

### Q63 ⭐ 🟢 What is a subcontractor or contingent worker, and how should they be handled in headcount, utilisation and cost reports?
**Asked at:** commonly asked (no company-specific report found); gap-fill topic.
**What the interviewer is checking:** That you know not everyone working for a company is on its payroll, and why that changes reports.
**Say this in the interview:** "A contingent worker or subcontractor works for us but is not a regular employee, for example a freelancer or a vendor's staff. I report them as a separate category, never silently mixed into employee headcount."
**Explain simply:**
- Employee: on our payroll, with benefits and our employment contract. Contingent worker or subcontractor: hired for a project or a period, often paid by invoice.
- Headcount: show employees and contingent workers as two lines plus a total, labelled.
- Utilisation: decide whether they are in the base. They are often tracked on delivery capacity, but not in employee-attrition or bench metrics.
- Cost: their cost sits in vendor or subcontract cost, not salary cost; per-head cost comparisons need to separate the two.
- Each report states its rule so the numbers reconcile (see Q59).
**Likely follow-ups:** 1) *Attrition?* Usually excluded; show contract-end separately. 2) *Revenue per employee?* Say whether contractors are in the denominator.
**Common mistakes:** Merging them into employee counts; counting their cost as zero; using different rules in different reports.

### Q64 ⭐ 🟢 Why do GCC analyst roles often ask for stakeholder management and Power BI or Tableau along with Excel and SQL?
**Asked at:** commonly asked (no company-specific report found); GCC MIS-analyst interview reports were not found, so this reflects JD patterns only.
**What the interviewer is checking:** Whether you understand the analyst's job as the whole chain from data to a decision.
**Say this in the interview:** "A GCC (global capability centre, an India-based team serving a global parent company) analyst takes requests from busy business teams abroad, pulls data with SQL, prepares it in Excel, and presents it in a dashboard. So the technical tools and the people skills both matter."
**Explain simply:**
- SQL gets the data; Excel handles quick checks and ad hoc work; Power BI or Tableau makes recurring reports that others can read and filter without asking you.
- Stakeholder management means clarifying what they really need, setting deadlines, pushing back on vague requests, and explaining numbers in plain words.
- GCC work often means working with managers in other time zones, so written clarity and expectation setting matter.
- Your HR background helps: you know how business users ask questions and what they worry about.
**Likely follow-ups:** 1) *Give an example of managing a stakeholder.* A manager asked for "attrition"; I confirmed the definition, period and exclusions before building. 2) *Which tool first?* Excel and SQL, then a BI tool.
**Common mistakes:** Listing tools with no example of use; treating stakeholder management as just "communication"; promising dates without checking data availability.

### Q65 ⭐ 🟢 How do large batches of fresher campus joiners affect utilisation and bench reports in the first six months after they join, and how would you report them fairly?
**Asked at:** commonly asked (no company-specific report found); utilisation and bench are standard IT-services MIS vocabulary in vendor and prep pages (unverified). No source defines a separate "ex-trainee utilisation", so the split below is my suggested practice.
**What the interviewer is checking:** Whether you know that a big intake drags the headline number down for a reason that is not poor management, and can report it without hiding it.
**Say this in the interview:** "Freshers first spend weeks in training and then ramp up slowly on projects, so a large batch pulls blended utilisation down and can inflate bench. I would report the headline number as it is, and beside it show the same number excluding people still in training or ramp, with a clear label."
**Explain simply:**
- **Utilisation** = billable hours divided by available hours (definitions vary by company; I use this one). **Bench** = people with no project assignment (some companies count only trained, deployable people as bench).
- **Campus joiners** are fresh graduates hired in batches. They usually go through classroom training first, where nothing is billed to a client.
- **Fair reporting:** tag every person with a status (in training, ramping, deployable bench, billable) and show three views: all employees, excluding trainees, and a separate "ramp curve" for each batch (share billed at month 1 to 6).
- Never delete trainees from history; just label them. Compare batches with each other (batch of 2026 against batch of 2025) to see if ramp is slowing.
**Worked example:** 150 experienced staff bill 80% of 160 monthly hours. 50 freshers bill 0% in months 1 to 3 (training), then 40%, 60%, 80% in months 4 to 6 (invented ramp). Blended utilisation (rounded to 1 decimal, percent): months 1 to 3 = 60.0%, month 4 = 70.0%, month 5 = 75.0%, month 6 = 80.0%. The experienced team never moved from 80%; the 20-point dip is entirely the batch.
**Likely follow-ups:** 1) *Is training time bench?* Usually shown separately as training; confirm the company rule. 2) *How do you spot a real problem?* Experienced-staff utilisation falling, or a batch ramping slower than past batches.
**Common mistakes:** Blaming project managers for a dip caused by an intake; hiding trainees silently; mixing definitions of bench between months.

### Q66 ⭐ 🟡 What is the difference between a project's gross margin and contribution margin in an IT services MIS, and which overheads are normally excluded at project level?
**Asked at:** commonly asked (no company-specific report found); margin layers appear in professional-services finance pages (unverified).
**What the interviewer is checking:** Whether you know margins are layers and that company definitions differ, so you ask before quoting a number.
**Say this in the interview:** "Gross margin is revenue minus the direct cost of delivering the project. Contribution margin goes one step further and removes other costs that exist because of this project. Corporate overheads such as HR, finance and rent are normally kept out at project level. Exact definitions differ by company, so I would confirm them first."
**Explain simply:**
- **Direct cost:** salaries and benefits of the people on the project, subcontractors, project travel.
- **Gross margin** (my definition) = revenue minus direct cost. **Contribution margin** = gross margin minus further project-attributable costs, for example client-specific tools, sales commission on the deal, or a share of delivery-management time. Some companies swap these two names; check the finance manual.
- **Normally excluded at project level:** corporate overheads (HR, finance, legal, leadership), sales and marketing in general, facilities, bench cost of people not on any project, and training spend. Those appear in company-level profit instead (from memory, unverified; policy varies).
- HR link: the same payroll cost is "direct" when the person is on a project and "bench cost" when not.
**Worked example:** invented project, revenue 1,000, direct cost 620, other attributable cost 60. Gross margin = 380 (38.0%). Contribution margin = 320 (32.0%). Percent = margin divided by revenue.
**Likely follow-ups:** 1) *Why exclude overheads?* So project managers are judged on what they control. 2) *Is a high-margin project always good?* Not if it is tiny or the margin comes from under-staffing.
**Common mistakes:** Quoting a margin without saying which definition; allocating corporate overhead to projects and then comparing them unfairly.

### Q67 ⭐ 🟡 A project has 10 resources: 6 billable at 100%, 2 at 50% and 2 not allocated. What is the allocation-based utilisation for the project, and why can it differ from timesheet utilisation?
**Asked at:** commonly asked (no company-specific report found); allocation versus timesheet utilisation appears in resource-management vendor pages (unverified).
**What the interviewer is checking:** Basic weighted arithmetic and awareness that plans and actuals differ.
**Say this in the interview:** "Allocation-based utilisation is 7 full-time equivalents divided by 10 people, so 70%. If I only count the 8 people actually allocated it is 87.5%, so I would state the denominator. Timesheets can differ because allocation is a plan and timesheets are what people actually booked."
**Explain simply:**
- **FTE (full-time equivalent):** one person working full time = 1. A person at 50% = 0.5.
- **Allocation** is the planned share of a person's time put on this project, set by the resource manager.
- **Timesheet utilisation** uses hours actually booked as billable, so it moves with leave, holidays, overtime, late timesheets, and people working on tasks that are not billable.
- A person allocated 100% but on two weeks of leave will show lower on timesheets.
**Worked example:** 6 x 1.0 + 2 x 0.5 + 2 x 0 = 7.0 FTE. 7.0 / 10 = 70.0% (all resources). 7.0 / 8 = 87.5% (allocated people only). For comparison, an invented timesheet month of 160 hours where the six log 150 each and the two half-timers log 60 each gives 1,020 / 1,600 = 63.75% on all 10 people.
**Likely follow-ups:** 1) *Which denominator is right?* Whichever the company defines; show both when unsure. 2) *Is 100% allocation realistic?* Rarely, since leave and holidays reduce available hours.
**Common mistakes:** Averaging 100, 50 and 0 without weighting by headcount; forgetting the unallocated people; comparing a plan figure to an actual figure as if equal.

### Q68 ⭐ 🟡 How would you build an HR-systems data dictionary for Workday fields such as worker status, cost centre and job profile so that reports across teams agree?
**Asked at:** commonly asked (no company-specific report found); Workday and HRIS analyst topics appear in training-vendor prep pages (unverified). Workday was not named in the in-scope 0 to 2 year job descriptions reviewed.
**What the interviewer is checking:** That you treat definitions as a shared agreement, not each analyst's guess.
**Say this in the interview:** "I would list every field used in reports, and for each write a plain definition, the source field in Workday, the owner, allowed values, and how it is used in headcount. Then I agree it with HR, finance and IT, version it, and make all dashboards point to it."
**Explain simply:**
- **Data dictionary:** a table describing each field: name, plain meaning, source, owner, allowed values, example, update frequency.
- **Worker status** (active, on leave, terminated) must say whether people on leave count in headcount. **Cost centre** is the finance code a person's cost is booked to; say who can change it and when. **Job profile** is the standard job definition (title, level, family) that many positions share (Workday terms from memory, unverified).
- Record "as of" rules: effective dates matter, because a person's cost centre can change mid-month.
- Agree one headcount definition (for example, active employees on the last day of the month, excluding contingent workers) and write it in the dictionary.
- Keep a change log so that a shift in numbers can be explained.
**Likely follow-ups:** 1) *Who owns it?* Each field has a business owner; the analyst maintains the document. 2) *What if teams disagree?* Escalate to the data owner and document the decision.
**Common mistakes:** Writing the dictionary once and never updating it; ignoring effective dates; letting every team keep its own headcount definition.

### Q69 ⭐ 🟡 A Workday integration (EIB or RaaS) feeding the payroll vendor fails for 30 workers. What data checks would you do first as the reporting analyst?
**Asked at:** commonly asked (no company-specific report found). From memory, unverified: EIB is Workday's Enterprise Interface Builder for loading or extracting data in bulk, and RaaS is Report as a Service, where a custom report is exposed as a web feed.
**What the interviewer is checking:** A calm, ordered approach: find what the 30 have in common before touching anything.
**Say this in the interview:** "First I would get the error list and look for what the 30 workers share: hire or termination dates, country, pay group, missing mandatory fields, special characters. Then I would check those fields in the source report, and hand findings to the integration team rather than editing live data myself."
**Explain simply:**
- **Integration:** an automatic file or feed that sends data from one system (HR system) to another (the payroll vendor).
- **Check 1:** read the actual error messages and group them (missing value, wrong format, invalid code).
- **Check 2:** look for a pattern: new joiners, leavers, transfers, one country, one cost centre.
- **Check 3:** mandatory fields (bank details, tax ID, cost centre, pay group), field lengths, date formats, special characters in names, duplicate worker IDs.
- **Check 4:** effective dates (a change dated in the future or backdated can break a feed) and worker status.
- **Check 5:** compare against the last good run: what changed in the report definition or the data?
- Payroll data is sensitive: share only the worker IDs needed, and follow the company's access rules.
**Worked example (tiny sample):** `workers` is a 4-row table, W1 to W4, with the columns shown in the output.
```python
# Workers who are missing a mandatory field
mandatory_fields = ["bank_account", "cost_centre"]
workers["missing_fields"] = workers[mandatory_fields].isna().sum(axis=1)
workers_with_gaps = workers[workers["missing_fields"] > 0]
print(workers_with_gaps)
```
```
  worker_id bank_account cost_centre   hire_date  missing_fields
1        W2          NaN        CC10  2026-11-03               1
2        W3          456         NaN  2026-11-05               1
```
Plain words: two of four sample workers lack a bank account or cost centre, and both are recent hires, which is exactly the kind of pattern to look for.
**Likely follow-ups:** 1) *Do you fix it in Workday?* No; report to the data owner or HR operations. 2) *How do you prevent repeats?* A pre-run validation report of mandatory fields.
**Common mistakes:** Re-running blindly; fixing records without authority; ignoring the pattern across the 30.

### Q70 ⭐ 🟡 When would you not use Alteryx, and what are its licence-cost and governance drawbacks compared with Power Query and Python?
**Asked at:** commonly asked (no company-specific report found); Alteryx question lists exist on prep sites (unverified). Alteryx appeared in only a small share of the job descriptions reviewed. Tool pricing and features below are from memory, unverified.
**What the interviewer is checking:** Balanced tool judgement, not tool loyalty.
**Say this in the interview:** "I would avoid Alteryx for small, one-off or very simple jobs, when only a few people use it, or when the team already has Power Query or Python. It is a paid, licensed tool, so cost and who can open the workflows matter."
**Explain simply:**
- **Alteryx** is a drag-and-drop tool for cleaning and joining data and building repeatable workflows without much code.
- **Licence cost:** typically paid per user (from memory, unverified); Power Query comes inside Excel and Power BI, and Python is free.
- **Governance drawbacks:** workflows are files that few people can read; version control and peer review are harder than with Python code in a repository; scheduling and server components may cost extra; if the one licensed person leaves, the process may stall.
- **When it still fits:** a team of non-coders needs repeatable, visual, auditable data prep at medium scale.
- **Choose by need:** quick Excel clean-up, Power Query; heavy statistics or automation, Python; wide business-user prep with budget, Alteryx.
**Likely follow-ups:** 1) *Join versus union?* A join combines columns by a matching key; a union stacks rows. 2) *How do you document a workflow?* Annotations plus an owner and a change log.
**Common mistakes:** Calling one tool "best"; ignoring licence cost and key-person risk.

### Q71 ⭐ 🔴 Utilisation is 82% and bench is 9% but revenue is flat for three quarters. Lay out a structured analysis of what to examine (pricing, mix, leave, non-billable investment, realisation, demand).
**Asked at:** commonly asked (no company-specific report found); this is a constructed case, and vendor pages note that high utilisation does not equal profit or revenue (unverified).
**What the interviewer is checking:** Whether you can break revenue into drivers and test each, instead of guessing.
**Say this in the interview:** "I would write revenue as headcount times available hours times utilisation times rate times realisation, then see which driver moved while the others offset it. Utilisation is only one driver; rate, mix, realisation and demand can all hold revenue flat."
**Explain simply:**
- **Revenue = headcount x available hours x utilisation x average rate x realisation.** (**Realisation:** the share of billable work that is actually invoiced at full value, after discounts and write-offs.)
- **Pricing and rate:** are new contracts at lower rates, or rate cards unchanged for years?
- **Mix:** more offshore or junior people lowers the average rate; fixed-price versus time-and-material contracts behave differently.
- **Leave and holidays:** seasonal leave cuts available billable hours.
- **Non-billable investment:** internal projects, presales, training that is counted as work but not billed.
- **Realisation and demand:** discounts, write-offs, delayed invoicing, and pipeline or client budget cuts.
- Also check the 9% bench: is it concentrated in skills the market does not buy?
**Worked example:** invented quarter 1: headcount 1,000, 480 hours each, utilisation 82%, rate 30 per hour, realisation 97% = 11,453,760. Quarter 3: headcount 1,060 (+6%), utilisation 82%, rate 29.1 (-3%), realisation 95% = 11,533,936, only +0.7%. More people at the same utilisation produced almost no extra revenue because rate and realisation slipped.
**Likely follow-ups:** 1) *What data first?* Revenue, hours and rate by project, contract type and month. 2) *Is 82% good?* Benchmarks vary; do not quote one without a source.
**Common mistakes:** Stopping at utilisation; ignoring realisation and mix; mixing percentage and percentage points when describing change.

### Q72 ⭐ 🔴 A GCC finance-operations team's invoice-processing cost per transaction rose 12% while volume fell 8%. How would you analyse it, and what data do you need?
**Asked at:** commonly asked (no company-specific report found). A GCC (global capability centre) is an offshore centre a large company runs for its own back-office or specialist work.
**What the interviewer is checking:** Whether you separate fixed from variable cost and ask what drove the numerator.
**Say this in the interview:** "Cost per transaction is total cost divided by volume. A 12% rise with 8% lower volume means total cost went up about 3%, not down. Part of the rise is simply fixed cost spread over fewer invoices, so I would split fixed and variable cost and check what else got more expensive."
**Explain simply:**
- **Fixed cost:** does not change with volume in the short term (salaries, rent, licences). **Variable cost:** moves with volume (overtime, temporary staff).
- If all cost were fixed, an 8% volume fall alone would lift cost per transaction by about 8.7% (1 / 0.92). The actual 12% is more, so total cost also rose.
- Examine: headcount and pay changes, attrition and rehiring, overtime, tool or licence cost, rework and exceptions per invoice, invoice mix (complex versus simple), allocated overhead changes.
- Check that volume is measured the same way and was not cut by automation that also cost money.
**Data and tables involved:** monthly cost by category (people, tools, overhead); invoices processed by type and complexity; headcount and hours; exception and rework counts; allocation rules.
**Worked example:** invented base: 50,000 invoices at 4.00 = 200,000. New volume 46,000 at 4.48 = 206,080, so total cost +3.04%. Fixed-cost-only test: if fixed cost is 120,000 and variable 1.60 per invoice, cost per transaction would be 4.21 at 46,000 (+5.2%); the actual 4.48 is still about 6.4% above that 4.21 (ratios, not percentage points, so the 12% does not split as 5.2 + 6.8); that remainder comes from added cost or inefficiency.
**Likely follow-ups:** 1) *Should volume have lowered cost?* Only for variable cost. 2) *How do you present it?* A bridge from old to new cost per transaction by driver.
**Common mistakes:** Treating all cost as variable; ignoring overhead allocation changes; comparing percentage changes as if additive.

### Q73 ⭐ 🔴 A client's SLA says 95% of P1 tickets are resolved in 4 hours. The report shows 96%, but the client says it feels worse. How would you test the report?
**Asked at:** commonly asked (no company-specific report found); SLA clock rules and MTTR ambiguity are discussed in service-desk vendor pages (unverified).
**What the interviewer is checking:** Healthy suspicion of a green number, and knowing how an SLA metric can be technically right yet misleading.
**Say this in the interview:** "I would recompute from raw ticket data using the contract definition, then test what the report excludes or changes: priority downgrades, paused clocks, reopened tickets, and tickets still open. A percentage on a narrow population can look fine while the client's experience is worse."
**Explain simply:**
- **P1:** the highest priority (critical outage). **SLA:** the written service promise. **Clock pause:** many contracts stop the timer while waiting for the client, which is legitimate only if the contract says so.
- **Tests:** (1) is the denominator all P1 tickets, including ones downgraded to P2 and ones still open? (2) are paused hours allowed? (3) is "resolved" the time of the fix or the time the ticket was closed or reopened? (4) is the average hiding a long tail of very late tickets? (5) does the client count business hours or wall-clock hours?
- Also compare against client sentiment: reopen rate, escalations, repeat tickets.
**Worked example:** invented bridge: 90 reported tickets, 86 met = 95.6% (reported as 96%). Now add 10 tickets downgraded out of P1 (4 of them met) and remove 5 tickets that met the target only because the clock was paused: (86 - 5 + 4) / 100 = 85.0% on the client's view. Small SQL sample of 10 tickets (6 closed as P1, all met after pauses; 4 closed as P2; only 4 of the 10 met 4 wall-clock hours without being reopened):
```sql
-- reported view: P1 at close, paused hours removed
-- client view: all tickets opened as P1, wall-clock time, no reopened tickets
SELECT
  ROUND(100.0 * SUM(CASE WHEN priority_at_close = 'P1'
        AND wall_clock_hours - paused_hours <= 4 THEN 1 ELSE 0 END)
        / SUM(CASE WHEN priority_at_close = 'P1' THEN 1 ELSE 0 END), 1) AS reported_pct,
  ROUND(100.0 * SUM(CASE WHEN wall_clock_hours <= 4
        AND reopened = 0 THEN 1 ELSE 0 END) / COUNT(*), 1) AS customer_view_pct
FROM tickets;
```
Output: reported_pct 100.0, customer_view_pct 40.0. Plain words: same tickets, two definitions, very different stories.
**Likely follow-ups:** 1) *Is the report then wrong?* Not necessarily, it may follow the contract; the gap is a definition conversation. 2) *What do you add?* Percentile resolution times and reopen rate.
**Common mistakes:** Defending the number; never recomputing from raw timestamps; ignoring open tickets.

### Q74 ⭐ 🔴 A project is green on schedule and budget but its defect rate and attrition on the team are rising. How would you design an early-warning project health score?
**Asked at:** commonly asked (no company-specific report found); RAG (red, amber, green) status and its subjectivity are discussed in project-management pages (unverified).
**What the interviewer is checking:** Whether you design leading indicators, not only lagging ones.
**Say this in the interview:** "Schedule and budget are lagging, they turn red late. I would add leading signals such as defect trend, team attrition, overtime and open-risk age, give each a weight, set thresholds with delivery heads, and show the score with its parts so no signal gets hidden by an average."
**Explain simply:**
- **Lagging indicator:** reports what already happened (cost overrun). **Leading indicator:** hints at trouble ahead (rising defects, people leaving).
- **Design:** pick 5 to 8 signals; convert each to a 0 to 100 health value using agreed thresholds; weight them; add a rule that any single red signal caps the project at amber.
- **Candidate signals:** defect rate trend, rework hours, team attrition and resignations, overtime hours, key-person dependency, client escalations, aged risks.
- **Calibrate** on past projects that did go wrong, and review thresholds regularly. Team-level people data should be reported in aggregate, with small teams handled carefully for privacy.
**Worked example:** invented weights: defects 30%, attrition 30%, schedule 20%, budget 20%. Health values: defects 20, attrition 35, schedule 95, budget 92. Score = 0.30 x 20 + 0.30 x 35 + 0.20 x 95 + 0.20 x 92 = 53.9 out of 100 (amber or red), while schedule and budget alone average 93.5 (green).
**Likely follow-ups:** 1) *Why a cap rule?* A weighted average can hide one serious failure. 2) *How do you prove the score works?* Back-test against past project outcomes.
**Common mistakes:** Only lagging indicators; opaque weights; thresholds that are never recalibrated.

### Q75 ⭐ 🔴 A GCC wants to compare its reporting cost against an outsourced vendor. How would you build a fair cost-per-FTE and cost-per-transaction comparison?
**Asked at:** commonly asked (no company-specific report found); this is a constructed case.
**What the interviewer is checking:** That you compare full cost on both sides, with the same scope.
**Say this in the interview:** "I would define the same scope and volume for both, include all costs on each side (the GCC's overhead and the vendor's fee plus the client's own governance, transition and rework costs), and then compute cost per FTE and per transaction, with a sensitivity to volume."
**Explain simply:**
- **Cost per FTE** = total cost divided by full-time equivalents. **Cost per transaction** = total cost divided by transactions handled.
- **GCC side:** salaries, benefits, facilities, technology, management, allocated shared services, attrition and hiring cost.
- **Vendor side:** contract fee, plus the cost the parent still bears: vendor management team, transition, quality rework, exit risk.
- **Fairness:** same service levels, same quality, same hours; state the time horizon and amortise one-time costs.
- Cost per FTE can mislead if the two teams produce different output per person, so show both measures.
**Worked example:** invented annual figures in millions, 120,000 transactions. GCC: people 6.0 + overhead 1.5 + technology 0.6 = 8.1 for 30 FTE. Vendor: fee 6.6 + governance 0.7 + amortised transition 0.3 + rework 0.2 = 7.8 for 25 FTE. Per transaction: GCC 67.50, vendor 65.00 (currency units). Per FTE: GCC 270,000, vendor 312,000. The naive view (people cost and fee only) shows 50.00 versus 55.00, the opposite ranking, which shows why full cost matters.
**Likely follow-ups:** 1) *What if volume doubles?* Check which costs are fixed versus variable on each side. 2) *What non-cost factors matter?* Quality, control, data security, flexibility.
**Common mistakes:** Comparing vendor fee against GCC salaries only; ignoring retained governance cost; mismatched scope.

### Q76 ⭐ 🔴 Management wants one dashboard that shows utilisation, bench, SLA compliance and project RAG for 40 projects. How would you define the metrics, owners and refresh cycle before building anything?
**Asked at:** commonly asked (no company-specific report found); constructed case in the style of GCC and IT-services MIS roles.
**What the interviewer is checking:** Whether you agree definitions and ownership before building, which is the hardest part of MIS.
**Say this in the interview:** "Before touching a tool I would write a one-page metric sheet: for each metric, its formula, source system, owner, refresh time and known caveats, and get management to sign it off. Then I would build a thin first version and check it against existing reports."
**Explain simply:**
- **Metric sheet:** utilisation (billable hours divided by available hours, source: timesheet and HR system), bench (unassigned people, source: resource allocation), SLA compliance (tickets within target divided by tickets, source: ticket tool), project RAG (red, amber, green rules).
- **Owners:** one named business owner per metric, plus a data owner per source.
- **Refresh cycle:** timesheets weekly, tickets daily, RAG monthly or fortnightly; show "last refreshed" on the page.
- **RAG:** replace opinion with objective rules where possible (for example schedule variance beyond a set limit), with a manual override that must be explained.
- **Controls:** reconcile totals to finance and HR, define the 40-project list and how new ones join, and set access rules (sensitive people data at aggregate level).
- Build in phases and agree what the dashboard will not show.
**Likely follow-ups:** 1) *Who signs off?* Business owners, with the head of MIS as final reviewer. 2) *How do you stop numbers disagreeing with other reports?* One shared data dictionary (see Q68) and a reconciliation step.
**Common mistakes:** Building first and defining later; no owners; mixing refresh cycles without saying so; RAG set by opinion only.
