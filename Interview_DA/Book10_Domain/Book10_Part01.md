# Book 10 — Domain Knowledge | Part 1: HR / People Analytics 🟢🟡🔴

**Target:** 120 questions | **Actual:** 150 questions
**Scope:** HR and people-analytics domain knowledge: headcount types, attrition mechanics, hiring funnel, engagement, DEI metrics, compensation, workforce planning, HRIS data and payroll basics, privacy of employee data.

### Q1 ⭐⭐⭐ 🟢 What is an HRIS, and which systems (core HR, applicant tracking, payroll, learning, performance, attendance) feed the data an HR analyst works with?
**Asked at:** commonly asked (no company-specific report found); "walk me through the HR systems and data" appears in prep-site People Analytics question guides (unverified).
**What the interviewer is checking:** Whether you know where HR data lives and that it sits in several separate systems that must be joined.
**Say this in the interview:** "An HRIS is the Human Resource Information System, the master record of every employee. An analyst's data usually comes from several connected systems: core HR, hiring, payroll, attendance, learning and performance, and I join them on employee ID."
**Explain simply:**
- **Core HR (the HRIS itself):** one row per employee with joining date, department, manager, grade, status. It is the "source of truth" for headcount.
- **Applicant tracking system (ATS):** tracks job openings and candidates (applied, interviewed, offered, joined). It feeds hiring metrics.
- **Payroll:** monthly salary calculation and payment. It holds pay components and deductions, and is the source for cost.
- **Attendance / leave system:** swipe-ins, leave taken, overtime. It feeds absence and working-hour analysis.
- **Learning management system (LMS):** course enrolments and completions.
- **Performance system:** goals, ratings, promotion cycles.
- In many companies these are different products (or modules of one suite such as Workday or SAP SuccessFactors; names from memory, unverified), so the same person can look slightly different in each.
**Data and tables involved:** `employee_master` (employee ID, dates, status), `candidates`/`requisitions` (ATS), `payroll_monthly`, `attendance_daily`, `course_completions`, `performance_ratings`. Typical first cut: check each table's row count against the HRIS headcount.
**Likely follow-ups:** 1) *Which system wins if they disagree?* The system that owns that fact: HRIS for status and dates, payroll for money paid. 2) *What links them?* Employee ID, which is why a clean ID matters.
**Common mistakes:** Treating the HRIS as the only source; assuming IDs match across systems without checking; forgetting contractors may sit outside the HRIS.

### Q2 ⭐⭐⭐ 🟢 What is the employee lifecycle ("hire to retire"), and what data is created at each stage that an analyst could use?
**Asked at:** commonly asked (no company-specific report found); the hire-to-retire view is named in HRIS and HR data analyst job posts (unverified).
**What the interviewer is checking:** That you see HR data as a story over time, and can name a metric for each stage.
**Say this in the interview:** "The lifecycle runs from attracting a candidate to the employee's exit. Every stage leaves a dated record, and each record supports a metric."
**Explain simply:**
- **Attract and hire:** requisition, applications, interviews, offer. Data: dates per stage, source. Metrics: time to fill, offer acceptance.
- **Onboard:** joining date, documents, probation. Data: onboarding survey, early exits.
- **Develop and perform:** training records, ratings, promotions, transfers. Metrics: promotion rate, training hours.
- **Reward:** salary revisions, bonus, benefits. Metrics: pay by grade, increment cost.
- **Engage:** surveys, leave, attendance. Metrics: engagement score, absence.
- **Exit:** resignation date, last working day, reason, notice served. Metrics: attrition, regretted attrition.
- "Retire" is only one kind of exit; most exits are resignations.
**Likely follow-ups:** 1) *Which stage is most useful?* Depends on the question; exits are usually first because attrition is costly. 2) *What links the stages?* Employee ID plus dates.
**Common mistakes:** Forgetting pre-hire data (candidate IDs often differ from employee IDs); analysing one stage in isolation; ignoring dates, which make the lifecycle a timeline.

### Q3 ⭐⭐⭐ 🟢 Who are the usual stakeholders of an HR analyst (HR business partners, talent acquisition, compensation and benefits, HR operations, learning and development, finance), and what kind of report does each typically ask for?
**Asked at:** commonly asked (no company-specific report found); stakeholder handling is a recurring theme in People Analyst prep guides (unverified).
**What the interviewer is checking:** That you know who uses your work and tailor reports to their decision.
**Say this in the interview:** "Each stakeholder has a different decision, so I ask what decision the report supports before building it."
**Explain simply:**
- **HR business partners (HRBPs):** HR people embedded in a business unit. They ask for headcount, attrition and engagement by team.
- **Talent acquisition (TA):** the recruiters. They ask for open requisitions, ageing, funnel conversion, source quality.
- **Compensation and benefits:** they ask for pay by grade, pay-range position, increment and bonus cost.
- **HR operations:** run the day-to-day records and payroll inputs. They ask for data-quality lists (missing managers, duplicate IDs) and process turnaround.
- **Learning and development (L&D):** training completion, hours per person, skill gaps.
- **Finance:** headcount cost, budgeted versus actual headcount, hiring plan. They need numbers that tie to payroll.
**Likely follow-ups:** 1) *What if two stakeholders want different numbers?* Agree one written definition per metric. 2) *Who do you trust for headcount?* Whatever reconciles to payroll and is signed off by HR operations.
**Common mistakes:** Sending the same dashboard to everyone; building without asking the decision; letting HR and finance each keep their own headcount.

### Q4 ⭐⭐⭐ 🟢 What is the difference between an employee ID, a position ID and a requisition ID, and why does an analyst need all three to join HR tables correctly?
**Asked at:** commonly asked (no company-specific report found); position-based HRIS design is common in Workday-style systems (from memory, unverified).
**What the interviewer is checking:** That you understand keys and the grain of each table, not just column names.
**Say this in the interview:** "Employee ID identifies the person, position ID identifies the seat in the org chart, and requisition ID identifies a request to fill a seat. They answer different questions, so joining on the wrong one gives wrong counts."
**Explain simply:**
- **Employee ID:** one per person (ideally for life, even across rehires). Used for pay, leave, performance.
- **Position ID:** a budgeted seat, for example "Payroll Analyst, Pune, reports to Manager X". A seat can be empty, and over time different people can fill it.
- **Requisition ID:** an approved request to hire into a position. One position can have many requisitions over the years (each time it is vacated); a requisition may later link to the employee who joined.
- Join path: candidate → requisition → position → employee. Vacancy and budget analysis needs position; hiring funnel needs requisition; people analysis needs employee.
**Data and tables involved:** `employees` (employee ID, position ID), `positions` (position ID, department, budget status), `requisitions` (requisition ID, position ID, open and close dates). First cut: count positions with no employee (vacancies) and requisitions with no position (data error).
**Likely follow-ups:** 1) *Can one employee hold two positions?* Yes, in some systems (dual roles), so count people with distinct employee ID. 2) *Why not join on name?* Names repeat and change.
**Common mistakes:** Counting positions as headcount; joining requisitions straight to employees and duplicating rows when a requisition is reopened; assuming one requisition equals one hire (it can be several openings).

### Q5 ⭐⭐⭐ 🟢 Which worker types (permanent, fixed-term contract, third-party or agency staff, consultants, interns, trainees, gig workers) are usually counted in company headcount, and which are not? Why must this rule be written down?
**Asked at:** commonly asked (no company-specific report found); definition consistency is flagged in HR-metrics vendor guides (unverified).
**What the interviewer is checking:** That you know headcount is a definition, not a fact, and you insist on documenting it.
**Say this in the interview:** "Practice varies by company. A common rule counts employees on the company's own payroll, and leaves out third-party staff, consultants and gig workers. Whatever the rule is, it must be written in the data dictionary."
**Explain simply:**
- **Usually counted:** permanent employees and fixed-term contract employees on the company payroll.
- **Often counted but varies:** interns and trainees (some firms count them as employees, some report them separately).
- **Usually not counted:** agency or third-party staff (paid by the vendor), consultants (paid on invoice), gig workers.
- Third-party staff may still matter for cost or capacity, so report them as a separate "contingent workforce" line.
- If sales counts interns and HR does not, two "headcount" numbers will circulate and meetings are spent arguing instead of deciding.
**Likely follow-ups:** 1) *How do you store this?* A `worker_type` column plus a `counts_in_headcount` flag. 2) *Does FTE solve it?* No; FTE (full-time equivalent) adjusts for part-time hours, not for who is included.
**Common mistakes:** Assuming a standard definition; changing the rule mid-year without restating history; dropping contractors from analysis completely when finance needs them.

### Q6 ⭐⭐⭐ 🟢 Why does "headcount" always need a date, and what is the difference between a point-in-time snapshot, a period-end figure and an average headcount?
**Asked at:** commonly asked (no company-specific report found); headcount basics are in every HR-metrics guide (unverified).
**What the interviewer is checking:** That you never quote a headcount without a date and know which version fits which purpose.
**Say this in the interview:** "Headcount changes every day with joiners and leavers, so the number means nothing without 'as of' a date. A snapshot is one chosen day, period-end is the snapshot on the last day of the period, and average headcount smooths the whole period."
**Explain simply:**
- **Point-in-time snapshot:** count on any chosen date, such as 15 May.
- **Period-end figure:** the snapshot on the last day of a month, quarter or year; the usual report number.
- **Average headcount:** the average of several snapshots (for example each month-end) across the period. Used as the denominator for rates such as attrition, because a rate compares exits with the people who were exposed across the period.
- Opening is the previous period's closing; closing equals opening plus joiners minus leavers.
**Worked example:** Headcount: 1 April 1,000; 30 April 1,020; 31 May 1,050; 30 June 1,100 (invented). Using opening and closing only: (1,000 + 1,100) / 2 = 1,050. Using all four points: (1,000 + 1,020 + 1,050 + 1,100) / 4 = 1,042.5. The two differ because the middle points are not on the straight line between opening and closing.
**Likely follow-ups:** 1) *Which do you use for a board slide?* Period-end. 2) *For attrition rate?* Average.
**Common mistakes:** Mixing a snapshot from one system with a period-end from another; forgetting to say the date; using closing headcount as the denominator in a fast-growing team.

### Q7 ⭐⭐⭐ 🟢 What does "effective-dated" HR data mean (for example, a salary change that applies from 1 July but is entered on 20 July), and what goes wrong in reports if you ignore effective dates?
**Asked at:** commonly asked (no company-specific report found); effective dating is a core idea in Workday-style HRIS (from memory, unverified).
**What the interviewer is checking:** That you understand history tables, and the difference between when something is true and when it was recorded.
**Say this in the interview:** "Effective-dated means every change carries the date from which it applies, separate from the date someone typed it in. Reports must be built on the effective date, or past numbers are wrong."
**Explain simply:**
- Each change (salary, department, manager, grade) is stored as a new row with an **effective date** (valid from) and often an end date; the old row is kept as history.
- There is also an **entry date** (when it was keyed in). In the example, effective 1 July, entry 20 July: June headcount-by-department must still show the old department, and July pay must include the back-dated difference (arrears).
- Ignoring effective dates means: using today's department for old months (the history rewrites itself), counting someone in two teams or none, and cost reports that do not match payroll.
- To report "as of" a date: pick the row where effective start is on or before that date and the next change is after it.
**Likely follow-ups:** 1) *How do late entries affect reports already shared?* Past figures can change; decide a freeze or restatement rule. 2) *Which date for a promotion count?* Effective date.
**Common mistakes:** Joining on the latest row only; using entry date as the event date; forgetting that back-dated changes alter closed periods.

### Q8 ⭐⭐⭐ 🟢 What is the difference between grade, band, level, designation and job family in an HR data table?
**Asked at:** commonly asked (no company-specific report found); the terms vary by company (unverified).
**What the interviewer is checking:** That you can read an HR table without confusing seniority, pay and job content.
**Say this in the interview:** "These overlap and every company uses them slightly differently, so I check the company's job architecture document. Broadly: job family is the type of work, level and grade show seniority and pay structure, band groups grades, and designation is the title."
**Explain simply:**
- **Job family:** the type of work, e.g. Finance, Engineering, HR.
- **Grade:** a rank in the pay structure (e.g. G5), each with a salary range.
- **Band:** a group of grades (e.g. "junior band" is G1 to G4), often used for policy such as leave or travel.
- **Level:** seniority in the career ladder; some firms use level and grade as the same thing.
- **Designation:** the job title on the business card, e.g. "Senior Analyst"; titles are not always consistent across teams.
- For pay comparisons use grade; for career analysis use level; for org-wide cuts use job family.
**Likely follow-ups:** 1) *Can two designations share a grade?* Yes. 2) *Which for pay equity?* Compare within the same grade and job family.
**Common mistakes:** Comparing pay by designation text (spelling variants); assuming grade and level are always the same; ignoring that mappings change after restructures.

### Q9 ⭐⭐⭐ 🟢 What is CTC, and how do gross salary, deductions and take-home pay relate to it in an Indian payroll (basic, HRA, special allowance, employer and employee PF, variable pay)?
**Asked at:** commonly asked (no company-specific report found); Indian payroll vocabulary is expected in India HR analytics roles (unverified).
**What the interviewer is checking:** That you can separate what the company spends from what the employee receives.
**Say this in the interview:** "CTC is cost to company: everything the employer spends on the employee in a year, including employer PF and variable pay. Take-home is lower, because employer PF and unpaid variable pay are not in monthly pay, and employee deductions are removed."
**Explain simply:**
- **Basic:** the core pay; PF and often other items are calculated on it.
- **HRA (house rent allowance):** an allowance for rent, often a percentage of basic.
- **Special allowance:** the balancing figure that makes the total equal the CTC.
- **Employer PF (provident fund):** retirement contribution paid by the company; part of CTC, never in the employee's hand monthly. **Employee PF** is deducted from the employee's salary.
- **Variable pay:** performance-linked amount, paid later and only if earned.
- Gross monthly salary = basic + HRA + special allowance (fixed monthly cash). Take-home = gross minus employee deductions (employee PF, professional tax, income tax deducted at source, called TDS).
- Component percentages and statutory details below are invented and, for rules, from memory, unverified; confirm with the payroll or compliance team.
**Worked example:** Assume CTC of 12,00,000 a year. Basic 40% of CTC = 4,80,000. HRA 50% of basic = 2,40,000. Employer PF 12% of basic = 57,600. Variable 10% of CTC = 1,20,000. Special allowance (balance) = 12,00,000 - 4,80,000 - 2,40,000 - 57,600 - 1,20,000 = 3,02,400. Fixed gross a year = 4,80,000 + 2,40,000 + 3,02,400 = 10,22,400, so gross per month = 85,200. Employee PF 12% of basic = 4,800 a month; assume professional tax of 200 a month. Monthly take-home before income tax = 85,200 - 4,800 - 200 = 80,200. Income tax (TDS) would reduce it further and depends on the employee's declarations. All amounts in rupees; no rounding needed.
**Likely follow-ups:** 1) *Why does take-home differ from CTC divided by 12?* CTC includes employer PF and variable. 2) *Which figure for cost analysis?* CTC; for employee experience, take-home.
**Common mistakes:** Calling CTC the salary the employee receives; treating variable pay as guaranteed; forgetting employer PF sits inside CTC (some companies add it on top, so confirm the definition).

### Q10 ⭐⭐⭐ 🟢 Which employment statuses do HR systems carry (active, on leave, on notice, absconding, terminated, retired), and which should count as headcount in a month-end report?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you handle status edge cases deliberately and consistently.
**Say this in the interview:** "Anyone still employed on the report date counts: active, on leave and on notice. Terminated and retired people have left. Absconding is the grey case, so I follow the company's written rule."
**Explain simply:**
- **Active:** working normally; counts.
- **On leave** (maternity, medical, sabbatical): still employed, so usually counts; some firms show them separately as "not working".
- **On notice:** resigned but still serving the notice period; still employed until the last working day, so counts. Attrition is recorded when they leave.
- **Absconding:** stopped coming without notice. Many firms keep them in headcount until a formal termination is processed; others exclude after a set number of days. The rule must be documented.
- **Terminated:** left; excluded from the date after the termination effective date.
- **Retired:** left; excluded.
- Use the status as of the report date (effective-dated), not today's status.
**Likely follow-ups:** 1) *Do notice-period people count in next month's forecast?* Show them as expected exits. 2) *Does long leave count?* Yes unless the policy says otherwise.
**Common mistakes:** Using current status for a past month; dropping people on notice early (understates headcount and attrition timing); no written rule for absconding cases.

### Q11 ⭐⭐⭐ 🟢 What are the stages of a hiring lifecycle (requisition approval, sourcing, screening, interviews, offer, background verification, joining), and what table or timestamp in an applicant tracking system marks each stage?
**Asked at:** commonly asked (no company-specific report found); the hiring funnel is a standard People Analyst theme (unverified).
**What the interviewer is checking:** That you can map a business process to data columns, so you can compute stage times.
**Say this in the interview:** "Each stage should leave a timestamp. Differences between consecutive timestamps give the time spent in a stage, and counts at each stage give conversion."
**Explain simply:** (table and column names below are illustrative; every ATS names them differently)
- **Requisition approval:** `requisitions.approved_date`, the clock for time to fill starts here (some firms start at opening).
- **Sourcing:** `applications.applied_date` and `source` (portal, referral, agency).
- **Screening:** `application_stages` row with stage "screen" and its date and result.
- **Interviews:** `interviews` table, one row per round, with date and outcome.
- **Offer:** `offers.offer_date`, `accepted_date`, offered salary.
- **Background verification (BGV):** `bgv.initiated_date`, `bgv.cleared_date`. Failure here loses a candidate after acceptance.
- **Joining:** `joining_date`, normally from the HRIS once the person becomes an employee.
**Data and tables involved:** `requisitions`, `candidates`, `applications`, `application_stages`, `interviews`, `offers`, `bgv`. First cuts: count per stage, median days between stages, drop-off by source.
**Likely follow-ups:** 1) *Where does the candidate become an employee?* At joining; link by candidate ID to employee ID. 2) *Why use median days?* A few very slow hires distort the average.
**Common mistakes:** Assuming every stage has a date (some are only status flags); mixing "offered" and "accepted" counts; ignoring candidates who skip stages.

### Q12 ⭐⭐⭐ 🟢 What is the difference between a replacement (backfill) hire and a growth (net new) hire, and why do finance and HR report them separately?
**Asked at:** commonly asked (no company-specific report found); headcount planning with finance is named in People Analyst guides (unverified).
**What the interviewer is checking:** That you understand why a hire can be neutral or additive for headcount and cost.
**Say this in the interview:** "A backfill replaces someone who left, so headcount stays flat; a growth hire adds a new seat and raises headcount and budget. Finance needs them separately because only growth hires change the approved headcount plan."
**Explain simply:**
- **Replacement (backfill):** the seat already exists and was budgeted; the old salary is freed, so cost impact is roughly the pay difference.
- **Growth (net new):** a new position needing new budget approval.
- Reason for separate reporting: attrition creates backfill demand, while growth is a business decision. Mixing them hides whether hiring is just running to stand still.
- Simple check: closing headcount = opening + growth hires - (exits - backfills). If every exit is backfilled, closing equals opening plus growth hires.
- Tag it in the requisition table (`hire_type`: replacement or growth) when it is raised, because it is hard to reconstruct afterwards.
**Likely follow-ups:** 1) *Is an internal transfer a backfill?* The vacated seat may be, but it is not an external hire; report it separately. 2) *Who approves growth?* Usually finance and business heads.
**Common mistakes:** Treating all hires as growth; no link between the leaver and the replacement requisition; counting a frozen backfill as still open.

### Q13 ⭐⭐⭐ 🟢 What types of employee surveys exist (annual engagement, pulse, onboarding, exit, stay interview), and how do their purposes and data differ?
**Asked at:** commonly asked (no company-specific report found); engagement dashboards are a recurring theme in HR analyst guides (unverified).
**What the interviewer is checking:** That you match each survey to its question and know the data limits.
**Say this in the interview:** "Each survey asks a different question at a different time: engagement asks how people feel overall, pulse checks quickly, onboarding checks the first weeks, exit asks why people leave, and stay interviews ask why people stay."
**Explain simply:**
- **Annual engagement:** long, whole company, once a year; scores by theme and team; good for trends.
- **Pulse:** a few questions, monthly or quarterly; early warning, small samples.
- **Onboarding:** new joiners at 30, 60 or 90 days; links to early attrition.
- **Exit:** at leaving; reasons and feedback, often free text; biased because leavers may be polite.
- **Stay interview:** a manager conversation with current employees about what keeps them; mostly notes, little numeric data.
- Anonymity: survey data is usually reported only for groups above a minimum size to protect identity.
**Likely follow-ups:** 1) *Can you link surveys to attrition?* Yes with care, respecting anonymity promises. 2) *Which is best?* None alone.
**Common mistakes:** Comparing scores from different survey scales; reporting tiny groups; ignoring response rate.

### Q14 ⭐⭐⭐ 🟢 Which DEI metrics do companies commonly track (representation, hiring, promotion, attrition, pay equity, leadership pipeline), and how is representation different from inclusion?
**Asked at:** commonly asked (no company-specific report found); fairness and bias themes appear in People Analyst guides (unverified).
**What the interviewer is checking:** That you can name measurable DEI indicators and know their limits.
**Say this in the interview:** "Representation counts who is in the workforce; inclusion is whether people feel they belong and are treated fairly. The first comes from HR records, the second mostly from surveys."
**Explain simply:** (DEI means diversity, equity and inclusion)
- **Representation:** share of a group (for example women) overall, by level and by team.
- **Hiring:** group share among applicants, interviewed, offered, joined.
- **Promotion:** promotion rate by group.
- **Attrition:** exit rate by group; a higher rate for one group is a signal to investigate.
- **Pay equity:** pay of comparable roles (same grade and job family) across groups.
- **Leadership pipeline:** group share at each step toward senior roles.
- **Inclusion:** survey questions such as "I feel I belong" scored by group.
- Collecting caste, religion or similar data raises privacy and legal issues; awareness only, from memory, unverified: confirm what is allowed with the compliance team.
**Likely follow-ups:** 1) *Why compare to applicants?* Representation in hiring depends on who applies. 2) *Small groups?* Suppress or combine them.
**Common mistakes:** Reporting only overall representation; treating a gap as proof of bias without controls; naming individuals in small cells.

### Q15 ⭐⭐⭐ 🟢 What are the fixed, variable and long-term components of an employee's total rewards (fixed pay, bonus, ESOP or RSU, benefits), and how does total rewards differ from CTC?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you can break pay into parts and know what each measures.
**Say this in the interview:** "Total rewards is everything of value the employee gets from the employer, including benefits and equity. CTC is a narrower cost-to-company number, usually fixed pay, variable pay and statutory costs."
**Explain simply:**
- **Fixed:** basic, allowances; paid regardless of performance.
- **Variable / short term:** annual bonus or incentive, linked to performance.
- **Long term:** ESOP (employee stock option plan: a right to buy company shares at a set price) or RSU (restricted stock unit: shares given after a vesting period). Vesting means the right is earned gradually over time.
- **Benefits:** health insurance, leave, meals, learning budget, retirement contributions.
- Total rewards may also include non-cash items (flexibility, development). CTC may or may not include ESOP value or some benefits, depending on the company, so state the definition.
- For analysis, keep each component in its own column so you can compare, say, fixed versus variable mix by grade.
**Likely follow-ups:** 1) *How do you value ESOP?* At grant or vest value, per company policy. 2) *Which for a pay-gap study?* Compare components separately and in total.
**Common mistakes:** Assuming CTC equals total rewards; counting unvested equity as paid; ignoring benefits cost.

### Q16 ⭐⭐⭐ 🟢 What is workforce planning, and how do demand forecasting (how many people we need) and supply forecasting (how many we will have) fit together?
**Asked at:** commonly asked (no company-specific report found); headcount planning with finance appears in People Analyst guides (unverified).
**What the interviewer is checking:** That you see planning as demand versus supply with a gap to close.
**Say this in the interview:** "Workforce planning is making sure the company has the right number of people with the right skills at the right time. Demand is what the business will need, supply is what current staff will still be there after exits and moves, and the gap is the hiring or reskilling plan."
**Explain simply:**
- **Demand forecast:** from business plans, such as sales growth, new offices or projects, converted to roles and headcount.
- **Supply forecast:** opening headcount minus expected attrition and retirements, plus internal moves and committed joiners, using past rates.
- **Gap:** demand minus supply. A positive gap means hiring, training or contractors; a negative gap means a surplus (slow hiring, redeployment).
- Do it by skill and location, not just a total.
- Revisit regularly, since business plans and attrition change.
**Likely follow-ups:** 1) *What data for supply?* Headcount by team, past attrition rates, notice-period list, retirement ages. 2) *Who owns demand?* Business leaders with finance.
**Common mistakes:** Planning only total numbers; using last year's attrition blindly; ignoring hiring lead time.

### Q17 ⭐⭐⭐ 🟢 What are the main steps of a monthly payroll run (attendance and leave cut-off, new joiners and exits, increments, deductions, payslips, bank file), and which of these steps produce data an analyst may use?
**Asked at:** commonly asked (no company-specific report found); payroll is called a core people-analytics dataset in vendor commentary (unverified).
**What the interviewer is checking:** That you know the payroll cycle and can say which outputs are reliable for analysis.
**Say this in the interview:** "Payroll closes the month's inputs, calculates pay, checks it and pays it. Several steps leave tables I can use, especially the final payroll register."
**Explain simply:**
- **Attendance and leave cut-off:** a deadline after which days worked and leave are frozen; produces days-paid and loss-of-pay (unpaid leave) data.
- **New joiners and exits:** adds new people and processes final settlement for leavers; produces joiner and leaver lists with dates.
- **Increments and other changes:** salary revisions, effective-dated, with arrears for back-dated ones.
- **Deductions:** PF, tax, loans; produces a deductions table.
- **Calculation and review:** the payroll register (one row per employee per month) with every component; the best source for cost.
- **Payslips:** the employee-facing output of the register.
- **Bank file:** the payment instruction sent to the bank; contains sensitive account details, so analysts rarely get it.
**Data and tables involved:** `payroll_register` (employee, month, components, net pay), `loss_of_pay_days`, `arrears`, `final_settlement`. First cut: payroll headcount versus HRIS headcount for the same month.
**Likely follow-ups:** 1) *What if payroll and HRIS differ?* Investigate timing, late entries and status mismatches. 2) *Which figure for cost?* Payroll register, not the HRIS salary field.
**Common mistakes:** Using the HRIS salary instead of what was paid; ignoring arrears when comparing months; handling bank details casually.

### Q18 ⭐⭐⭐ 🟢 Which employee data is especially sensitive (salary, health and medical leave, disciplinary records, caste or religion, bank and government ID numbers), and why should access be role-based?
**Asked at:** commonly asked (no company-specific report found); data privacy and ethics are a recurring theme in people-analytics prep guides (unverified).
**What the interviewer is checking:** Whether you understand that HR data is personal and that an analyst must handle it with care, not just analyse it.
**Say this in the interview:** "All of these are sensitive because misuse can hurt a person: embarrassment, discrimination or fraud. So each person should see only what their job needs, which is role-based access."
**Explain simply:**
- **Salary:** causes conflict and poaching if leaked; managers see their team's pay, not everyone's.
- **Health and medical leave:** reveals illness; usually only a small HR/benefits team should see even the reason.
- **Disciplinary records:** can damage reputation and be used unfairly; limit to HR case owners and the line chain.
- **Caste, religion, gender, disability:** protected characteristics; wrongly used, they enable discrimination. Analysts may need them only in aggregate (for example, diversity counts).
- **Bank account and government ID numbers (such as PAN or Aadhaar):** direct fraud and identity-theft risk; an analyst rarely needs the raw number, a masked version is enough.
- **Role-based access** means permissions follow the job (payroll officer, HRBP, analyst, manager), not the person. It limits the damage of mistakes and leaks, and gives an audit trail of who saw what.
**Regulation / privacy note (awareness only):** Indian data-protection law (the DPDP Act 2023) and company policy expect employers to protect personal data; from memory, unverified, confirm with the compliance/legal team.
**Likely follow-ups:** 1) *What would you do as an analyst?* Ask for the minimum columns, use employee IDs instead of names, mask IDs and bank numbers, and share only aggregates. 2) *Can you email a salary file?* No; use the approved shared location with restricted access.
**Common mistakes:** Pulling every column "just in case"; sharing raw extracts on email or chat; showing small-group salary averages that point to one person.

### Q19 ⭐⭐⭐ 🟢 What does an HR analyst actually do in a typical week at a mid-sized company (recurring MIS reports, ad hoc requests, data clean-up, dashboard maintenance), and which of these would a newcomer handle first?
**Asked at:** commonly asked (no company-specific report found); "describe your day or what you would do in the first 90 days" appears in prep guides (unverified).
**What the interviewer is checking:** Whether you have realistic expectations of the job and know that much of it is routine, not modelling.
**Say this in the interview:** "A typical week is mostly recurring reports and data clean-up, plus a few ad hoc questions from HR leaders. A newcomer usually starts with the recurring MIS reports, because they have a fixed recipe and teach you the data."
**Explain simply:**
- **MIS (management information system) reports:** the regular headcount, joiner, leaver, attendance and attrition reports sent weekly or monthly.
- **Ad hoc requests:** one-off questions such as "why did the sales team's attrition rise?"; they need judgment and clear scoping.
- **Data clean-up:** fixing duplicates, missing managers and wrong dates, usually by flagging them to the HRIS (HR information system) owner.
- **Dashboard maintenance:** refreshing data, checking numbers still match the source, and answering "why does this differ from my number?".
- **Newcomer order:** recurring reports and data checks first, then dashboard upkeep, then ad hoc analysis once you know the definitions.
**Likely follow-ups:** 1) *How do you handle a rush request?* Confirm the question, the deadline and the definition, deliver a simple answer first, and refine later. 2) *What do you do when two reports disagree?* Compare definitions and cut-off dates before blaming the data.
**Common mistakes:** Expecting machine learning on day one; skipping the definition check; not documenting how a report was built.

### Q20 ⭐⭐⭐ 🟡 Opening headcount on 1 April was 1,200. During April there were 90 external joiners, 15 rehires, 12 transfers into the entity, 8 transfers out, 55 resignations and 6 terminations. Build the headcount roll-forward and give the closing headcount.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can reconcile movements to a closing number, and keep additions and reductions separate.
**Say this in the interview:** "Closing headcount is 1,248. I add all inflows, subtract all outflows, and check that opening plus movement equals closing."
**Explain simply:**
- A **roll-forward** is opening + additions - reductions = closing, so every change in headcount is explained.
- Additions: joiners, rehires (people who left earlier and came back) and transfers in from another legal entity.
- Reductions: resignations (employee's choice), terminations (company's decision) and transfers out.
**Worked example:**

| Line | Heads |
|---|---|
| Opening (1 April) | 1,200 |
| + External joiners | 90 |
| + Rehires | 15 |
| + Transfers in | 12 |
| = Total additions | 117 |
| - Resignations | 55 |
| - Terminations | 6 |
| - Transfers out | 8 |
| = Total reductions | 69 |
| **Closing (30 April)** | **1,248** |

Net change is +48 heads (1,200 + 117 - 69 = 1,248). For attrition, only the 61 resignations and terminations normally count as exits; the 8 transfers out leave the entity but not the company (see Q23).
**Likely follow-ups:** 1) *Why not count transfers as hires?* They are not new to the company, and mixing them inflates hiring. 2) *The closing figure does not match HRIS, what then?* Look for late-entered joiners or leavers and date cut-off differences.
**Common mistakes:** Forgetting transfers; counting a resignation in the month it was submitted rather than the last working day (Q21); not reconciling to the system's closing count.

### Q21 ⭐⭐⭐ 🟡 An employee resigns on 5 October, serves a 60-day notice period and has a last working day of 4 December. In which month should the exit be counted in an attrition report, and what rule would you write for the data dictionary?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know that exits are dated by a defined event, and that this must be written down.
**Say this in the interview:** "I would count it in December, because December is when the person actually leaves the headcount. I would record the resignation date separately so we can also report resignations received in October."
**Explain simply:**
- The employee stays on payroll and in headcount until the last working day (4 December; 5 October + 60 days is exactly 4 December, so the dates are consistent).
- Counting the exit in October would drop the person from headcount while they are still paid, and the numerator and denominator would disagree.
- **Data dictionary rule (example wording):** "An exit is counted in the calendar month of the employee's last working day (LWD). Resignation date is stored separately and used for notice-period and pipeline reports only. If the LWD is later changed (early release, buy-out or extension), the exit moves to the month of the final LWD."
- Say it is the definition I use; some companies count by resignation date for a "resignations received" view, which is fine if it is labelled.
**Likely follow-ups:** 1) *What about notice served at 31 December and LWD on 1 January?* The exit belongs to January and the year-end headcount still includes the person. 2) *How do you track people on notice?* A "notice pipeline" count, useful as an early warning of upcoming exits.
**Common mistakes:** Using resignation date for attrition; changing the rule between reports; not storing both dates.

### Q22 ⭐⭐⭐ 🟡 Twelve month-end headcounts for a year are: 980, 985, 990, 1,000, 1,010, 1,030, 1,040, 1,020, 1,015, 1,005, 1,000, 1,010. Compute the average headcount and say why it is better than using only the opening and closing figures as the denominator for attrition.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know the denominator of attrition should represent the whole period.
**Say this in the interview:** "The average headcount is about 1,007. It uses all twelve months, so it is less affected by a spike or dip at the start or end."
**Explain simply:**
- Attrition rate = exits during the period / average headcount during the period.
- Sum of the 12 month-ends is 12,085; divided by 12 gives 1,007.08, so about 1,007 (rounded to a whole person).
- Using only first and last (980 and 1,010) gives 995, which ignores the peak of 1,040 in the middle and so understates the average size.
- If the company hired heavily in one month, or cut staff late in the year, opening and closing points can mislead.
**Worked example:** Suppose 120 people left during the year (an invented figure). With average headcount 1,007.08, attrition is 120 / 1,007.08 = 11.9%. With the 995 two-point average it is 120 / 995 = 12.1%. A small gap here, but it grows when headcount swings sharply. Rounded to one decimal.
**Likely follow-ups:** 1) *Why not use the closing headcount?* Exits happened from a larger or smaller group than the closing one. 2) *Are month-end figures perfect?* No; a daily average is more exact, but month-end is the practical standard.
**Common mistakes:** Using only the closing figure; averaging with the wrong number of points; mixing contractors into one headcount and not the other.

### Q23 ⭐⭐⭐ 🟡 How should rehires (boomerang employees) and internal transfers between legal entities be treated in hiring counts and attrition counts, and what happens to the numbers if two teams treat them differently?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know that definitions drive the numbers and that consistency matters more than any single choice.
**Say this in the interview:** "I would keep rehires as their own category, counted as hires but flagged, and treat inter-entity transfers as movements, not exits or hires, at the company level. Whatever the rule, it is written down and applied by every team."
**Explain simply:**
- **Rehire (boomerang):** someone who left and returned. Report them separately from first-time hires so "new talent" is not overstated.
- **Transfer between legal entities (for example, from the Indian company to its subsidiary):** the person is still an employee of the group. At group level it is neither exit nor hire; at entity level it is a transfer out of one and a transfer in to the other.
- Definitions differ across companies; this is the one I would propose and document.
**Worked example:** (invented figures) Entity A has 10 transfers out and Entity B has 10 transfers in. If both teams count transfers as exit and hire, group exits and hires are both overstated by 10, and attrition rises by 10 / average headcount (about 1 percentage point on 1,000 heads). If team A counts them as exits but team B does not count them as hires, the group totals will not reconcile at all, as roll-forwards stop adding up.
**Likely follow-ups:** 1) *Does a rehire reset tenure?* A policy question; store both original and latest joining dates. 2) *Do rehires count in early attrition?* Yes, by their latest joining date, unless the policy says otherwise.
**Common mistakes:** Giving a rehire a new employee ID so they appear as a stranger; double counting transfers; each team using its own rule.

### Q24 ⭐⭐⭐ 🟡 Which data checks would you run on an HRIS extract before building any report (for example, duplicate employee IDs, joining date after exit date, missing manager, impossible dates of birth)? List at least eight.
**Asked at:** commonly asked (no company-specific report found); data quality and integrity are named in HR data analyst job posts (unverified).
**What the interviewer is checking:** Whether you have a systematic habit of checking data before trusting it.
**Say this in the interview:** "I run a standard checklist covering keys, dates, categories and totals, log what fails, and take unresolved issues to the HRIS owner before building anything."
**Explain simply:** (HRIS is the HR information system, the master record of employees.)
1. **Duplicate employee IDs:** the ID should be unique per person.
2. **Joining date after exit date:** impossible sequence.
3. **Missing manager, or a manager who is not an employee:** breaks reporting lines.
4. **Impossible dates of birth:** future dates, or ages under 18 or over 75 (adjust to policy).
5. **Joining date in the future or before the company existed.**
6. **Active status with an exit date,** or exited status with no exit date.
7. **Missing mandatory fields:** department, location, grade, employment type.
8. **Inconsistent spellings of categories:** "Sales" vs "sales " vs "Sale".
9. **A person as their own manager,** or circular reporting loops.
10. **Salary outside the band, zero or negative.**
11. **Row count and headcount versus the last report,** and versus payroll.
**Likely follow-ups:** 1) *Do you fix errors yourself?* Fix in my copy with a log; ask the owner to correct the source. 2) *How do you do it quickly?* A saved script or Excel check sheet that I rerun on each extract.
**Common mistakes:** Deleting bad rows silently; checking only for blanks; skipping the check against a known total.

### Q25 ⭐⭐⭐ 🟡 Employees who left within 90 days of joining are called early attrition. Why do HR teams track it separately from overall attrition, and what data would you pull to understand it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can link a metric to its likely business cause, here hiring and onboarding quality.
**Say this in the interview:** "Early leavers have different causes from long-serving leavers: a poor hire, a mismatch with what was promised, or a bad first experience. They are also the most wasteful exits, because the company has paid for hiring and training and got little back."
**Explain simply:**
- Overall attrition mixes retirements, career moves and layoffs. Early attrition points at hiring and onboarding.
- It is a signal for recruiters (wrong people, wrong promises) and managers (poor onboarding).
- Definition used here: exit date minus joining date is 90 days or fewer; companies differ on 90 or 180 days.
**Data and tables involved:** Employee master (joining date, exit date, department, grade, location, manager), requisition/ATS (applicant tracking system) data (source, recruiter, offer details), exit reasons, onboarding feedback. First cuts: early-leaver share of all joiners by month of joining (a cohort view, with joiners as the denominator), by source, recruiter, manager, department, location and offer gap versus band; and the stated exit reason.
**Likely follow-ups:** 1) *What is the denominator?* Joiners in a cohort, not average headcount, so people who joined recently are tracked for their first 90 days. 2) *Can you evaluate a recent cohort?* Only after 90 days have passed, so recent months look artificially low.
**Common mistakes:** Dividing by average headcount; judging a cohort before 90 days; ignoring voluntary versus involuntary early exits (probation terminations).

### Q26 ⭐⭐⭐ 🟡 Exit interviews give a "primary reason for leaving" for each leaver. What are the weaknesses of this data, and how would you code and cross-check reasons before reporting them?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you treat self-reported data critically and know how to make it usable.
**Say this in the interview:** "Exit reasons are useful but biased: people avoid burning bridges, so I code them into a fixed list and cross-check with other data before telling leaders what drives attrition."
**Explain simply:**
- **Weaknesses:** leavers give polite reasons ("better opportunity", "personal reasons"); not everyone attends the interview; free text is inconsistent; one "primary" reason hides several; the interviewer's own judgement affects the answer.
- **Coding:** map free text to a fixed list (compensation, manager, growth, relocation, health, personal, other), with a short guide so two coders choose the same code; allow a secondary reason.
- **Cross-checks:** compare with pay position in band (Q35), time since last promotion, manager's team attrition, engagement scores, and exit interview coverage (percentage of leavers interviewed).
- Report coverage (for example, "interviews for 70% of leavers") beside the reasons.
**Likely follow-ups:** 1) *Is there a better time to ask?* Some firms survey again 3 to 6 months after leaving, or use stay interviews. 2) *Should you report "personal reasons" as is?* Show it, but flag that it often hides other causes.
**Common mistakes:** Treating stated reasons as the truth; reporting without coverage; letting each recruiter invent new categories.

### Q27 ⭐⭐⭐ 🟡 What is regretted attrition, who decides which exits are "regretted", and what data (ratings, critical skills, tenure) would you use to flag it consistently?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know that not all exits cost the same, and that "regretted" needs a rule, not a feeling.
**Say this in the interview:** "Regretted attrition is the exit of people the company would have preferred to keep. Business and HR leaders decide the rule, and I apply it consistently using rating, critical skill and role data."
**Explain simply:**
- **Regretted:** a good performer, a critical-skill holder or a successor to a key role leaves. **Non-regretted:** a low performer or a role that is no longer needed.
- Who decides: the manager's view can be biased, so the usual approach is a rule set by HR and business leaders, with the manager confirming at the time of resignation.
- **Example rule (to be agreed with leaders):** regretted if the last performance rating was in the top two bands, or the person holds a role on the critical-skills list, or is on the succession plan.
- Report regretted attrition separately; a low overall rate can hide losing the best people.
- Definitions differ by company; I state the one used.
**Data and tables involved:** performance ratings (latest two cycles), critical-skills and succession lists, tenure, grade, exit record, manager flag.
**Likely follow-ups:** 1) *What about people never rated?* Show them as "not rated" rather than guess. 2) *Is a manager's flag enough?* Use it as an input, but audit it against the rule.
**Common mistakes:** Deciding after the fact based on opinion; using one old rating; no record of the flag at exit time.

### Q28 ⭐⭐⭐ 🟡 Monthly exits for the last 12 months were 8, 10, 9, 12, 15, 11, 10, 9, 14, 13, 12, 17 against an average headcount of 1,000. Compute the rolling 12-month attrition, and compare it with annualising the last quarter's exits.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can compute attrition on two bases and notice what the difference means.
**Say this in the interview:** "Rolling 12-month attrition is 14.0%. The last quarter, annualised, is 16.8%, which says exits are running faster recently."
**Explain simply:**
- **Rolling 12-month attrition** = exits in the last 12 months / average headcount = 140 / 1,000 = 14.0%.
- **Annualising the last quarter:** last three months' exits are 13 + 12 + 17 = 42; multiplied by 4 gives 168; 168 / 1,000 = 16.8%. This assumes the quarter's pace continues for a year and the headcount is also about 1,000.
- The first three months had 27 exits (10.8% annualised), so the pace has risen.
**Worked example:** 140 / 1,000 = 14.0%; (42 x 4) / 1,000 = 16.8%; the gap is 2.8 percentage points (a percentage-point difference, not a percentage change). Rounded to one decimal; headcount assumed constant at the given 1,000.
**Likely follow-ups:** 1) *Which would you report?* The rolling 12-month rate as the headline and the quarterly pace as a trend flag. 2) *Why not just use one month?* Too noisy and affected by seasonality.
**Common mistakes:** Annualising one quarter without caveats; adding percentages across months; mixing the headcount definitions.

### Q29 ⭐⭐⭐ 🟡 An open-requisitions table has 40 requisitions; 12 are older than 90 days. Define requisition ageing and fill rate, and say what first cuts you would make to understand why some are stuck.
**Asked at:** commonly asked (no company-specific report found); time-to-fill and requisition tracking are named in HR-metric guides (unverified).
**What the interviewer is checking:** Whether you know recruiting terms and can break a problem down into useful cuts.
**Say this in the interview:** "A requisition is an approved request to hire one role. Ageing is how long it has been open; fill rate is the share of requisitions that were filled. Here 12 of 40, or 30%, are older than 90 days, so I would cut them by role, team, recruiter and stage."
**Explain simply:**
- **Requisition ageing:** today's date minus the date the requisition was approved/opened, in days, grouped into buckets (0 to 30, 31 to 60, 61 to 90, over 90).
- **Fill rate:** requisitions filled / requisitions opened (or approved) in a period. Definitions vary; state yours.
- 12 / 40 = 30% of open requisitions are older than 90 days (the 90-day cut-off is the question's choice).
- **First cuts:** by department, role family and grade; by recruiter and hiring manager; by location; by funnel stage where each is stuck (no candidates, no interview, offer declined); by salary offered versus market or band; by whether the requisition is on hold.
**Data and tables involved:** requisition table (ID, open date, role, department, status), candidate pipeline (stage, date), offers.
**Likely follow-ups:** 1) *Should on-hold requisitions count in ageing?* Usually pause the clock or report them separately. 2) *Is a long age always bad?* No; niche or senior roles take longer, so compare like with like.
**Common mistakes:** Using one average age for all roles; counting cancelled requisitions as unfilled; ignoring hold periods.

### Q30 ⭐⭐⭐ 🟡 In a recruiting funnel by source, one candidate appears under both "job portal" and "referral". How would you assign credit, and what duplicates would you remove before computing source-wise conversion?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can set a clear attribution rule and clean data before computing conversion.
**Say this in the interview:** "I would count the candidate once, give credit by a written rule such as 'first source that brought the candidate to us', and deduplicate candidates before computing any conversion rate."
**Explain simply:**
- **Source** is how a candidate reached the company (portal, referral, agency, careers site).
- Common rules: first touch (the first source), last touch, or priority order (for example, referral beats portal because it carries a bonus). Choose one, document it, and apply it everywhere. Referral credit may need extra checks because of the payout.
- **Duplicates to remove:** the same person with two candidate IDs (match on email, phone, name plus date of birth); the same person applying to the same requisition twice; the same person across requisitions (keep the row per application but count unique candidates in candidate-level metrics); test or internal records.
- Conversion by source = hires from that source / candidates from that source, after deduplication.
**Likely follow-ups:** 1) *What if the sum of sources is more than total candidates?* This signals double counting; check the rule. 2) *Does the rule change the answer?* Yes, it can shift credit between sources, so state it beside the chart.
**Common mistakes:** Counting the person under both sources; matching only on name; changing the rule between quarters.

### Q31 ⭐⭐⭐ 🟡 An engagement survey had 640 responses from 800 invited employees. What is the response rate, why does it matter when reading the scores, and what would worry you at 35%?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you question who answered before trusting a score.
**Say this in the interview:** "The response rate is 80%. It matters because scores describe only the people who replied. At 35% I would worry that the answers are not representative."
**Explain simply:**
- Response rate = responses / invited = 640 / 800 = 80.0%.
- High response means the score is closer to the whole company's view. Low response may mean only the very happy or very unhappy replied (non-response bias).
- At 35%, you would have 280 responses from 800 (35% of 800 = 280); so 520 people are unheard, and their views may differ.
- Worrying signs: low response in specific teams or locations, which can mean fear or disengagement; a gap between respondents and the employee population (for example, junior staff missing).
- Check response rates by group before comparing scores between them.
**Likely follow-ups:** 1) *What would you do at 35%?* Show the caveat, check who is missing, and avoid strong conclusions. 2) *How do you raise the rate?* Easy access, clear anonymity, and visible follow-up on past surveys.
**Common mistakes:** Quoting a score without the response rate; comparing teams with very different response rates.

### Q32 ⭐⭐⭐ 🟡 In a 5-point agreement item, the answers were 5: 120, 4: 200, 3: 150, 2: 80, 1: 50. Compute the mean score and the favourable percentage (top-two-box), and say which one you would report to a manager and why.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can compute both and pick the one a non-technical manager can use.
**Say this in the interview:** "The mean is 3.43 out of 5 and the favourable percentage is 53.3%. For a manager I would lead with the favourable percentage, and show the full distribution."
**Explain simply:**
- **Mean:** (5x120 + 4x200 + 3x150 + 2x80 + 1x50) / 600 = 2,060 / 600 = 3.43.
- **Top-two-box (favourable):** answers of 4 or 5 = 120 + 200 = 320; 320 / 600 = 53.3%.
- For context, neutral (3) is 25.0% and unfavourable (1 or 2) is 21.7%; the three add to 100.0%.
- Why favourable: "about 53 out of 100 agree" is easier to grasp than "3.43", and it is less distorted by a few extreme answers. The mean hides split opinions (a mean of 3 may be everyone neutral or half 1s and half 5s).
- Rounding to one decimal for percentages and two for the mean; "agreement" scales are ordinal, so the mean is only a rough summary.
**Likely follow-ups:** 1) *Why still report the mean?* It is useful for ranking and tracking small changes. 2) *How do you compare to last year?* Use the percentage-point change in favourable, not percent change.
**Common mistakes:** Quoting a mean to two decimals as if it were precise; ignoring neutral; mixing up the base (600 answers on this item, not 800 invited).

### Q33 ⭐⭐⭐ 🟡 Why do survey teams set a minimum group size (for example, five or ten responses) before reporting a team's score, and what happens to your dashboard design because of it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand anonymity and can design a dashboard that respects it.
**Say this in the interview:** "A small group's score can reveal how one person answered, which breaks the anonymity employees were promised. So below the minimum, the dashboard hides the number, and I design around that."
**Explain simply:**
- If a team has three responses and a score of 1.0, everyone knows how all three answered. Even a score from six people may point to one person when filtered by gender and grade.
- The minimum (five, ten or whatever the policy says) is set by the survey owner or HR leadership.
- **Dashboard effects:** show "fewer than N responses" instead of a score; roll small teams into the next level of the hierarchy; limit how many filters can be stacked (department plus grade plus gender plus location can create tiny cells); hide counts for small cuts too; apply the rule to comments.
- Watch for "differencing": two reports that allow a hidden group to be calculated by subtraction.
**Regulation / privacy note (awareness only):** survey anonymity promises are also a trust and data-protection matter; from memory, unverified, confirm with the compliance/legal team.
**Likely follow-ups:** 1) *Does the rule apply to the denominator or responses?* Usually responses; state which. 2) *Do you hide the whole team?* You hide the score, not the team's existence.
**Common mistakes:** Suppressing the score but showing a count of 1; allowing unlimited filters; forgetting free-text comments.

### Q34 ⭐⭐⭐ 🟡 Women are 120 of 300 employees at junior level, 60 of 240 at middle level and 12 of 100 at senior level. Compute representation at each level and say where the pipeline narrows most.
**Asked at:** commonly asked (no company-specific report found); diversity dashboards are named in HR analyst job posts (unverified).
**What the interviewer is checking:** Whether you compute shares per level and read the drop-off carefully.
**Say this in the interview:** "Representation is 40% at junior, 25% at middle and 12% at senior. The share falls at every step, and the sharpest relative fall is from middle to senior."
**Explain simply:**
- Representation = women at level / all employees at that level.
- **Worked example:** Junior 120 / 300 = 40.0%. Middle 60 / 240 = 25.0%. Senior 12 / 100 = 12.0%. Overall, 192 / 640 = 30.0%.
- Junior to middle: down 15.0 percentage points (a 37.5% relative fall). Middle to senior: down 13.0 percentage points (a 52.0% relative fall).
- In percentage points the biggest step is junior to middle (15 vs 13), but relative to the starting share, middle to senior loses more than half. I would say "the pipeline narrows at both steps; the narrowest point in relative terms is the move to senior", and state both measures.
- Caveat: this is a snapshot, not a tracked group over time; the senior group is only 100 people, so 12 women is a small base. To locate the cause, look at promotion rates and hiring mix by gender at each level.
**Likely follow-ups:** 1) *Does this prove bias?* No; it shows where to look (hiring, promotion, exits). 2) *What next data would you want?* Promotion and attrition rates by gender and level.
**Common mistakes:** Mixing percent and percentage points; comparing counts instead of shares; reading cause into a single snapshot.

### Q35 ⭐⭐⭐ 🟡 A pay band runs from INR 8 lakh (minimum) to INR 14 lakh (maximum) with a midpoint of INR 11 lakh. An employee earns INR 12.5 lakh. Compute the range penetration and say how you would read it.
**Asked at:** commonly asked (no company-specific report found); pay-band metrics appear in compensation-analytics prep material (unverified).
**What the interviewer is checking:** Whether you know the basic compensation vocabulary and can read a pay position, not just compute it.
**Say this in the interview:** "Range penetration is how far through the band the salary sits: (salary minus minimum) divided by (maximum minus minimum). Here it is 75%, so the employee is in the upper quarter of the band."
**Explain simply:**
- A **pay band** (or salary range) is the minimum-to-maximum pay the company allows for a grade. The **midpoint** is the market-reference pay for a fully competent person in that grade.
- **Range penetration** = position inside the band, 0% at the minimum and 100% at the maximum.
- Do not confuse it with **compa-ratio** = salary / midpoint, a different view of the same pay.
**Worked example:** (12.5 - 8) / (14 - 8) = 4.5 / 6 = 75%. Compa-ratio = 12.5 / 11 = 1.136, so about 13.6% above midpoint. Both figures are exact to the rounding shown. The 11 lakh midpoint is consistent with (8 + 14) / 2.
**How to read it:** At 75% the employee has limited room left (1.5 lakh to the cap). Check tenure and rating: a long-serving strong performer here is normal; a recent joiner here may mean they were hired at a premium. Near the cap, future increments may have to come as one-time bonuses or a promotion instead of base pay.
**Likely follow-ups:** 1) *What if penetration is above 100%?* The employee is "red-circled" (paid above the band); flag it for review. 2) *Below 0%?* "Green-circled"; likely an under-payment to correct.
**Common mistakes:** Using the midpoint instead of the minimum in the formula; mixing up range penetration (position in band) with compa-ratio (versus midpoint); reading a high figure as bad without checking tenure and performance.

### Q36 ⭐⭐⭐ 🟡 Compute the weighted average increment for the company from the data below and explain why it differs from the simple average of the three percentages.
Rating group A: 100 employees, total salary INR 12 crore, increment 14%
Rating group B: 600 employees, total salary INR 60 crore, increment 8%
Rating group C: 100 employees, total salary INR 9 crore, increment 2%
**Asked at:** commonly asked (no company-specific report found); increment and merit-budget arithmetic is a standard compensation-analytics exercise (unverified).
**What the interviewer is checking:** That you weight percentages by the right base instead of averaging percentages blindly.
**Say this in the interview:** "The company-level increment is total rupees of increment divided by total salary, so I weight each percentage by the salary base. That gives 8.22% against a simple average of 8%."
**Explain simply:**
- An **increment** is the percentage raise given at appraisal time.
- A percentage applies to a base. A group with a bigger salary bill moves the company figure more.
- The cost view (what finance cares about) weights by salary. A headcount-weighted view (average raise per person) is a second figure; I would state which one I use.
**Worked example (INR crore, rounded to 2 decimals for the percentage):**

| Group | Salary | Increment % | Increment cost |
|---|---|---|---|
| A | 12 | 14% | 1.68 |
| B | 60 | 8% | 4.80 |
| C | 9 | 2% | 0.18 |
| Total | 81 | | 6.66 |

Weighted (salary) average = 6.66 / 81 = 8.22%. Simple average = (14 + 8 + 2) / 3 = 8.00%. Headcount-weighted = (100x14 + 600x8 + 100x2) / 800 = 8.00%.
**Why they differ:** The simple average treats the three groups as equal. Group A (highest raise) has a larger salary bill per head (INR 12 lakh average, versus 10 and 9 lakh) so it pulls the cost-weighted figure up. The 8.00% match between simple and headcount-weighted is a coincidence of these numbers.
**Likely follow-ups:** 1) *Which would you report to finance?* The salary-weighted 8.22%, because it ties to the INR 6.66 crore cost. 2) *Does it include on-cost like PF?* Only if stated; I would say "base salary only".
**Common mistakes:** Averaging percentages; weighting by headcount when the question is about cost; forgetting to state whether the base is fixed pay or CTC.

### Q37 ⭐⭐⭐ 🟡 Compute the variance and the vacancy rate for each department from the table below, and say what you would flag.
Dept A: approved positions 100, filled 92
Dept B: approved 60, filled 61
Dept C: approved 40, filled 28
**Asked at:** commonly asked (no company-specific report found); position-control and vacancy reporting appear in workforce-planning prep material (unverified).
**What the interviewer is checking:** Whether you understand approved versus filled, and notice over-filled and high-vacancy cases.
**Say this in the interview:** "Variance is approved minus filled; vacancy rate is variance divided by approved. A is 8% vacant, B is over-filled by one, and C has 30% vacancy which I would flag first."
**Explain simply:**
- **Approved positions** (sanctioned headcount): seats finance has budgeted. **Filled**: seats with a person in them.
- **Variance** = approved - filled; positive means open seats, negative means over-filled.
- **Vacancy rate** = variance / approved.
**Worked example (percentages rounded to 1 decimal):**

| Dept | Approved | Filled | Variance | Vacancy rate |
|---|---|---|---|---|
| A | 100 | 92 | 8 | 8.0% |
| B | 60 | 61 | -1 | -1.7% (over-filled) |
| C | 40 | 28 | 12 | 30.0% |
| Total | 200 | 181 | 19 | 9.5% |

**What I would flag:** C first (30% vacant; check requisition ageing and whether work is being absorbed by others). B next: is the extra person a temporary overlap, a transfer not yet moved, or a budget breach? A is moderate; compare with its attrition. Note that the total of 9.5% hides the spread between departments.
**Likely follow-ups:** 1) *Does open requisition equal vacancy?* Not always: a position may be approved but no requisition raised yet. 2) *Use headcount or FTE?* State which; part-timers change the answer.
**Common mistakes:** Showing a negative vacancy rate without explaining it; computing the total by averaging the three percentages (8, -1.7, 30 would give 12.1%, wrong) instead of 19 / 200.

### Q38 ⭐⭐⭐ 🟡 The HRIS shows 1,014 active employees at month-end, but payroll paid 1,021 people. List the reasons the two counts can legitimately differ and the checks you would run to reconcile them.
**Asked at:** commonly asked (no company-specific report found); HRIS versus payroll reconciliation is a common people-analytics data-quality theme (unverified).
**What the interviewer is checking:** That you know the two systems answer different questions and can reconcile them methodically.
**Say this in the interview:** "The gap is 7 people, 0.7%. HRIS counts people employed at month-end; payroll counts people paid in the month. Leavers paid for part of the month, arrears and full-and-final payments explain most gaps, so I would match by employee ID."
**Explain simply:**
- **HRIS** (the HR master system) says who is on the rolls at a date. **Payroll** says who received money during the month. The time windows differ.
- **Legitimate reasons payroll > HRIS:** employees who left during the month but were paid till their last working day; full-and-final settlement paid to ex-employees; arrears or notice-pay to people already exited; people on payroll who are not counted as headcount (for example interns, consultants paid through payroll, if policy excludes them).
- **Reasons the other way:** unpaid leave or a salary hold for someone active; joiners whose first pay comes next month.
- **Not legitimate:** late exit updates in HRIS, duplicate IDs, ghost employees, rehires with two IDs.
**Reconciliation checks:**
1. Full outer join on employee ID: list IDs only in payroll, only in HRIS.
2. For the 7+ payroll-only IDs, look at last working day, pay type (regular, F&F, arrears) and worker type.
3. For HRIS-only IDs, check unpaid leave, hold, joining date after the payroll cut-off.
4. Confirm both use the same cut-off date and the same worker-type rule.
5. Count duplicates by name, date of birth, bank account.
**Likely follow-ups:** 1) *Which is the "official" headcount?* HRIS, once reconciled; payroll is the cost source. 2) *Is a 7 gap alarming?* Not by itself; unexplained IDs are.
**Common mistakes:** Assuming one system is wrong; not defining the cut-off; reconciling by names instead of IDs; ignoring ghost-employee risk (mention it carefully, as a control check, not an accusation).

### Q39 ⭐⭐⭐ 🟡 Monthly payroll cost rose from INR 4.10 crore to INR 4.45 crore. Build a bridge from the data below and say how much is unexplained.
New joiners added INR 0.20 crore
Exits removed INR 0.12 crore
Increments effective this month added INR 0.15 crore
One-time arrears paid INR 0.05 crore
Variable pay changed by INR 0.02 crore
**Asked at:** commonly asked (no company-specific report found); payroll cost bridges (waterfalls) are a standard finance-partnering task (unverified).
**What the interviewer is checking:** That you can reconcile a change into drivers and be honest about a residual.
**Say this in the interview:** "Opening 4.10 plus the five drivers gives 4.40, but actual is 4.45, so INR 0.05 crore is unexplained. I would not hide it; I would investigate it."
**Explain simply:**
- A **bridge** (waterfall) starts from last month's cost, adds each driver with its sign, and ends at this month's cost.
- **Arrears** are pay owed for earlier months paid now; they are one-time, so they will drop out next month.
- The **unexplained** (residual) is actual change minus the sum of known drivers.
**Worked example (INR crore):**

| Step | Amount | Running total |
|---|---|---|
| Opening (last month) | | 4.10 |
| New joiners | +0.20 | 4.30 |
| Exits | -0.12 | 4.18 |
| Increments | +0.15 | 4.33 |
| One-time arrears | +0.05 | 4.38 |
| Variable pay change | +0.02 | 4.40 |
| Unexplained | +0.05 | 4.45 |

Total change = 0.35. Explained = 0.30 (86% of the change). Unexplained = 0.05 (14% of the change; about 1.1% of closing cost).
**Where to look for the 0.05:** employer contributions on the new items (PF, insurance), overtime, joiners' partial-month effect, a one-off bonus or an error, and cost-centre re-mapping.
**Likely follow-ups:** 1) *What is the recurring run rate?* Closing less one-time arrears: 4.45 - 0.05 = 4.40, before resolving the residual. 2) *Is 14% unexplained acceptable?* Not for a finance audience; target a small, documented residual.
**Common mistakes:** Forcing the bridge to balance by renaming the gap as "other"; treating one-time arrears as permanent; mixing monthly cost with annual CTC.

### Q40 ⭐⭐⭐ 🟡 In plain words, what does India's Digital Personal Data Protection Act 2023 expect of an employer handling employee and candidate data (data fiduciary, consent, legitimate use for employment, deletion)? Mention that you are answering from general awareness.
**Asked at:** commonly asked (no company-specific report found); data privacy appears as a core theme in people-analytics prep material (unverified).
**What the interviewer is checking:** Privacy awareness and honesty about the limits of your knowledge, not legal expertise.
**Say this in the interview:** "I am answering from general awareness, not as legal advice. As I understand it, the employer is the responsible party, must handle personal data only for lawful purposes, keep it secure and not keep it longer than needed. I would confirm details with the legal and compliance team."
**Explain simply:**
- **Data fiduciary:** the organisation that decides why and how personal data is used; for employee data, that is the employer. A payroll or HRIS vendor acting on its behalf is a **processor**.
- **Consent:** the Act is built around notice and consent, but I recall that it also lists "legitimate uses", which I believe include some employment-related purposes. How wide that is should be confirmed.
- **Candidate data** (CVs, interview notes) is also personal data; I would use it only for the hiring purpose.
- **Deletion:** data should not be kept longer than the purpose needs; people can ask for correction and erasure, subject to legal retention.
**Regulation / privacy note (awareness only):** From memory, unverified: the Act was passed in 2023; rules and the dates by which obligations apply have been reported differently across sources. Confirm everything with the compliance/legal team.
**What it means for an analyst:** Use only the columns needed, mask IDs in shared files, restrict access by role, and avoid personal data in emails and personal laptops.
**Likely follow-ups:** 1) *Can you share the file with a vendor?* Only with a contract and approval. 2) *What about old candidate data?* Follow the retention rule; do not keep indefinitely "just in case".
**Common mistakes:** Sounding like a lawyer and giving legal certainty; assuming consent alone covers everything; forgetting candidates, not only employees, are covered.

### Q41 ⭐⭐⭐ 🟡 What is the difference between master data (employee, position, organisation) and transactional data (leave, payroll, appraisal) in HR, and why does the difference matter when you build tables for reporting?
**Asked at:** commonly asked (no company-specific report found); HRIS data-model basics appear in HR data analyst job posts (unverified).
**What the interviewer is checking:** That you can design clean tables: slowly changing "who and where" versus event-by-event "what happened".
**Say this in the interview:** "Master data describes the entities and changes slowly: who the employee is, which position, which unit. Transactional data records events with dates: a leave taken, a payslip, an appraisal. I keep them in separate tables joined by keys."
**Explain simply:**
- **Master data:** one row per employee, position or org unit (name, grade, manager, location). It is the dimension (lookup) side.
- **Transactional data:** many rows per employee, each tied to a date (leave days, monthly pay, rating per cycle). It is the fact (measurement) side.
- **Why it matters:** if you copy master attributes (department) into every transaction, they go stale when the employee transfers. Joining facts to master data on the right date gives the right department for that period.
- Master data also needs **effective dating**, so you can say what the grade was in March, not just today.
**Example:** Attrition by department should use the department on the exit date, from a dated master table, not today's department.
**Likely follow-ups:** 1) *Which key joins them?* Employee ID, plus a date range for effective-dated master data. 2) *Where do you store a rating?* Transaction table: one row per employee per cycle.
**Common mistakes:** One giant flat table that duplicates master fields; joining on the current department and rewriting history; forgetting that master data is also dated.

### Q42 ⭐⭐⭐ 🔴 A CHRO asks you to design a monthly HR dashboard. Which pages, KPIs, filters and refresh rules would you propose, and which privacy controls would you build in?
**Asked at:** commonly asked (no company-specific report found); headcount and attrition dashboard design appears in prep-site People Analytics questions (unverified).
**What the interviewer is checking:** Structured thinking: audience, decisions, definitions, and privacy before charts.
**Say this in the interview:** "I would first ask which decisions the CHRO wants to make, then agree metric definitions, and then build a few pages: headcount, hiring, attrition, and talent. Monthly refresh after payroll close, with role-based access and small-group suppression."
**Clarify first:** Who views it (CHRO only, or HR business partners too)? What definitions apply (headcount, attrition)? What is the source of truth?
**Explain simply (the proposal):**
- **Page 1, Summary:** headcount, net change, attrition (rolling 12 months), open requisitions, engagement score.
- **Page 2, Headcount and cost:** by unit, location, grade; approved versus filled; payroll cost.
- **Page 3, Hiring:** requisitions ageing, time to fill, offer acceptance, joining rate.
- **Page 4, Attrition:** voluntary versus involuntary, by tenure, early attrition, regretted share.
- **Page 5, Talent and diversity:** representation by level, promotion rates.
- **Filters:** month, business unit, location, grade band, worker type.
- **Refresh:** monthly, after payroll and HRIS month-end close, with the "as of" date shown on every page.
- **Privacy controls:** role-based row-level access; no names on the summary; hide groups below a minimum size (for example fewer than 10); no salary at employee level; audit log of who views what.
**Likely follow-ups:** 1) *How do you keep trust?* A definitions page and a reconciliation to payroll. 2) *Why monthly, not daily?* HR decisions are monthly and the data is closed monthly.
**Common mistakes:** Starting with chart types; no metric definitions; too many KPIs; leaving employee names and salaries visible to everyone.

### Q43 ⭐⭐⭐ 🔴 A business head asks for the names of employees your attrition model flags as likely to resign so that he can "talk to them". How do you respond, and what do you offer instead?
**Asked at:** commonly asked (no company-specific report found); ethical attrition prediction is a named theme in prep-site People Analytics guides (unverified).
**What the interviewer is checking:** Judgement: you take the business need seriously but protect employees from harm from an imperfect model.
**Say this in the interview:** "I would not hand over names. A prediction is a probability, not a fact, and a name list can hurt people through being passed over, watched or treated differently. I would offer team-level risk themes and actions that help everyone."
**Explain simply:**
- The model can be wrong; some flagged people would never have left, and some real leavers would be missed.
- Employees did not agree to be profiled for this purpose; it may breach privacy principles and trust.
- If names leak or are used, the person may lose a promotion or opportunity: a harm built on a guess.
**Offer instead:**
- Team-level or segment-level risk (for example "teams with long gaps since last promotion"), with small groups suppressed.
- The main drivers: promotion gap, pay position in band, manager changes, workload.
- Support for the manager: skip-level conversations, stay interviews, career-path plans for all.
- If the company decides to use individual-level flags, route them to HR business partners with governance, human review, no use for adverse decisions, and legal and privacy sign-off.
**Regulation / privacy note (awareness only):** From memory, unverified: purpose limitation and fairness principles apply to employee data; confirm with the compliance/legal team.
**Likely follow-ups:** 1) *How do you say no to a senior?* Explain the risk, offer the alternative, and escalate to the CHRO if needed. 2) *How accurate is the model?* Share precision and recall, and the limits.
**Common mistakes:** Flatly refusing without an alternative; handing over names "just this once"; presenting a risk score as certainty.

### Q44 ⭐⭐ 🟢 What is a requisition and how does a headcount approval work (budget approved by finance, requisition raised by manager, approved by HR), and which data fields come from each step?
**Asked at:** commonly asked (no company-specific report found); requisition and approval flows come up in hiring-analytics prep (unverified).
**What the interviewer is checking:** You understand how a vacancy formally comes into existence, and where the data comes from.
**Say this in the interview:** "A requisition is the formal approved request to fill a position. Finance approves the budget, the manager raises the requisition, HR approves it, and only then recruiting starts."
**Explain simply:**
- **Budget (finance):** the approved headcount plan for the year. Fields: department, approved positions, cost, cost centre, fiscal year.
- **Requisition (hiring manager):** the request against an approved position. Fields: requisition ID, position ID, role, grade, location, reason (backfill or growth), date raised.
- **HR approval:** checks grade, job description and policy. Fields: approver, approval date, status.
- After approval the requisition is **open**; it is closed when the hire joins, or cancelled.
**Likely follow-ups:** 1) *Why does the approval date matter?* Time to fill is usually measured from approval. 2) *Can a requisition exist without budget?* Not normally; if it does, flag it.
**Common mistakes:** Treating requisition and position as the same; measuring from the manager's request date without saying so.

### Q45 ⭐⭐ 🟢 What is the difference between attrition, layoffs, retirement, termination for cause and absconding, and how should an exit-type field be coded so that voluntary and involuntary exits can be separated?
**Asked at:** commonly asked (no company-specific report found); exit-type coding is a common data-dictionary topic (unverified).
**What the interviewer is checking:** Clean definitions and a coding scheme that supports separate reporting.
**Say this in the interview:** "Attrition is the overall term for people leaving. I split it by who initiated the exit: voluntary, such as resignation, versus involuntary, such as layoff or termination for cause, with retirement as its own type."
**Explain simply:**
- **Attrition:** headcount leaving the company for any reason (definitions differ; some exclude retirement or layoffs).
- **Layoff:** the company ends jobs for business reasons, not performance.
- **Retirement:** exit at superannuation age.
- **Termination for cause:** the company ends employment for misconduct or poor performance.
- **Absconding:** employee stops coming without notice and does not resign formally.
**Coding:** use two fields, **exit category** (voluntary, involuntary, other) and **exit type** (resignation, layoff, termination for cause, absconding, retirement, death, end of contract). Absconding is usually coded involuntary in reports because the process is company-led, but state the rule in the data dictionary.
**Likely follow-ups:** 1) *Is an end of fixed-term contract attrition?* Depends on policy; code it separately. 2) *Why report voluntary alone?* It reflects retention problems.
**Common mistakes:** One free-text reason field; mixing retirement into voluntary; not documenting the rule for absconding.

### Q46 ⭐⭐ 🟢 What are resignation, notice period, last working day, notice buyout and full-and-final settlement, and which of them are dates you would store in the exit table?
**Asked at:** commonly asked (no company-specific report found); exit-process vocabulary appears in HR data model questions (unverified).
**What the interviewer is checking:** You know the exit timeline and which dates matter for reports.
**Say this in the interview:** "I store four dates: resignation date, last working day, the actual relieving date if different, and settlement date. Notice period is a number of days; buyout is an amount and a flag."
**Explain simply:**
- **Resignation:** the employee formally gives notice (date of resignation).
- **Notice period:** the agreed days between resignation and leaving (for example 60 days).
- **Last working day (LWD):** the final day the person is employed.
- **Notice buyout:** paying money instead of serving some or all of the notice; this shortens the period.
- **Full-and-final settlement (F&F):** the last payment of dues (salary, leave encashment, recoveries) after exit.
**Exit table fields:** employee ID, resignation date, notice days (policy), notice days served, buyout flag and amount, LWD, F&F paid date, exit type.
**Likely follow-ups:** 1) *Which date counts for attrition?* Usually LWD (see Q21). 2) *Why store resignation date?* For forecasting from the pending-exit pipeline.
**Common mistakes:** Storing only one date; counting exits at resignation date; forgetting buyout changes the LWD.

### Q47 ⭐⭐ 🟢 What is span of control, how is it computed from a reporting hierarchy table, and what might very high or very low values suggest?
**Asked at:** commonly asked (no company-specific report found); organisation-structure metrics appear in people-analytics prep (unverified).
**What the interviewer is checking:** Can you compute a manager metric from a simple employee-manager table?
**Say this in the interview:** "Span of control is the number of direct reports per manager. From an employee table with a manager ID, I count rows grouped by manager ID."
**Explain simply:**
- A **reporting hierarchy table** has one row per employee with their manager's ID.
- **Direct reports** are people who report straight to one manager (not the whole team below).
- Very high spans (for example 20+) can mean thin supervision, overload or a flat structure. Very low spans (1 to 3) can mean too many layers or managers with little to manage.
- What counts as "too high" depends on the type of work; I would compare similar teams.
**Worked example (small invented table of 11 employees: employee 1 is the top person with no manager; employees 2 and 3 report to 1; 4, 5 and 6 report to 2; 7, 8, 9 and 10 report to 3; employee 11 reports to 4):**
```python
direct_reports = (
    employees[employees["manager_id"].notna()]   # skip the top person
    .groupby("manager_id")
    .size()
)
direct_reports.mean()
```
Result: manager 3 has 4 direct reports, manager 2 has 3, manager 1 has 2, manager 4 has 1; the average is 2.5 (10 reports across 4 managers). The same count in SQL is `SELECT manager_id, COUNT(*) FROM emp WHERE manager_id IS NOT NULL GROUP BY manager_id`. In plain words: group people under each manager and count.
**Likely follow-ups:** 1) *Do you count contractors?* State the rule. 2) *Spans for people with no reports?* Exclude them from the average.
**Common mistakes:** Counting everyone below a manager (that is team size, not span); including people with no reports in the average; ignoring vacant manager positions.

### Q48 ⭐⭐ 🟢 What is campus hiring (offers, pre-placement offers, internship conversion, batch joining), and why do campus offers often have a long gap before joining?
**Asked at:** commonly asked (no company-specific report found); campus-hiring joining-rate analysis appears in India HR analytics prep (unverified).
**What the interviewer is checking:** You understand the campus calendar and why joining is uncertain.
**Say this in the interview:** "Campus hiring means recruiting students from colleges before they graduate. The offer is made months before the degree ends, so joining happens in batches after graduation, with a drop-out risk in between."
**Explain simply:**
- **Campus offer:** made at a college placement drive.
- **Pre-placement offer (PPO):** a job offer given to an intern, usually after a summer internship.
- **Internship conversion:** share of interns who get and accept a full-time offer.
- **Batch joining:** many graduates start on the same date, often after final exams and results.
- **Why the gap:** the students must finish their degree, and the company wants a planned, aligned start date, so offers in the winter lead to joining mid-year.
- The gap creates risk: students may get a better offer, or change plans, so the company often makes more offers than seats.
**Likely follow-ups:** 1) *What data is tracked?* Offer date, college, branch, joining date, status. 2) *How do you reduce drop-off?* Keep in touch, early onboarding, and joining incentives.
**Common mistakes:** Treating campus offers like lateral hires; no tracking between offer and joining.

### Q49 ⭐⭐ 🟢 What do KRA, KPI, OKR, PIP, calibration and the 9-box grid mean in performance management, and which of them produce data you could analyse?
**Asked at:** commonly asked (no company-specific report found); performance-system vocabulary appears in HR analyst prep (unverified).
**What the interviewer is checking:** Vocabulary and awareness of which items yield analysable data.
**Say this in the interview:** "These are the language of performance management. Ratings, calibration outcomes and 9-box placements give the most analysable data; KRAs and OKRs are mostly text unless scored."
**Explain simply:**
- **KRA (Key Result Area):** the main areas of responsibility for a role.
- **KPI (Key Performance Indicator):** a measure of how well a KRA is being met (for example, calls handled).
- **OKR (Objectives and Key Results):** a goal-setting method: an objective plus measurable key results.
- **PIP (Performance Improvement Plan):** a formal plan for an employee whose performance is below expectations.
- **Calibration:** a meeting where managers compare ratings across teams to make them consistent.
- **9-box grid:** a 3x3 grid placing employees by performance and potential.
**Analysable data:** rating per cycle (before and after calibration), KPI scores, OKR progress percent, PIP start and outcome, and 9-box cell. Handle PIP data with care.
**Likely follow-ups:** 1) *Why compare ratings before and after calibration?* To see how much it changed. 2) *Is a PIP count a good metric?* Only with context.
**Common mistakes:** Mixing KRA and KPI; reporting PIP names widely; treating the 9-box as a precise measure.

### Q50 ⭐⭐ 🟢 How is demographic data (gender, disability, age, region, caste or religion) collected for DEI reporting, why is much of it optional and incomplete, and how should "prefer not to say" be handled in analysis?
**Asked at:** commonly asked (no company-specific report found); DEI data handling appears in people-analytics prep (unverified).
**What the interviewer is checking:** Respect for privacy and an honest approach to missing data.
**Say this in the interview:** "Most of it is self-declared and voluntary, so it is incomplete. I report 'prefer not to say' as its own category, show the coverage, and avoid guessing."
**Explain simply:**
- **Collection:** gender and date of birth are usually collected at joining; disability, caste or religion are typically asked through voluntary self-identification forms, with a clear purpose.
- **Why optional and incomplete:** these are sensitive, people fear misuse, and in some places collecting certain items is restricted or discouraged.
- **Handling "prefer not to say":** keep it as a separate category; do not drop it silently or impute it; show completeness (for example, 82% declared); note that results are for declared employees only.
- Small groups should be suppressed to protect identity.
**Regulation / privacy note (awareness only):** From memory, unverified: sensitive personal data needs a clear purpose, consent and strict access; confirm with the compliance/legal team before collecting caste or religion.
**Likely follow-ups:** 1) *Can you infer gender from name?* I would avoid it. 2) *What if coverage is low?* Report it as limited and improve the data collection method.
**Common mistakes:** Deleting missing records; guessing a category; publishing small groups.

### Q51 ⭐⭐ 🟢 Which statutory items does a payroll deal with in plain words (provident fund, ESI, professional tax, income tax deducted at source, gratuity), and which would an analyst need for employee cost reporting? Answer from general awareness.
**Asked at:** commonly asked (no company-specific report found); Indian payroll statutory items appear in HR analyst prep (unverified).
**What the interviewer is checking:** Basic payroll literacy and the ability to separate employee deductions from employer costs.
**Say this in the interview:** "I am answering from general awareness. Statutory items are payments required by law; some are deducted from the employee's pay and some are costs paid by the employer. For cost reporting I need the employer-borne ones."
**Explain simply:**
- **Provident fund (PF):** a retirement savings scheme; both employee and employer contribute a percentage of basic pay. Employer share is a company cost.
- **ESI (Employees' State Insurance):** health insurance for lower-paid employees; both share a small percentage, applicable under a salary limit.
- **Professional tax:** a state-level tax deducted from salary, in states where it applies.
- **TDS on salary (income tax deducted at source):** the employer deducts the employee's income tax and pays it to the government; it is the employee's money, not company cost.
- **Gratuity:** a lump sum paid after a minimum years of service; the company usually builds a provision for it, so it is an employer cost.
**For employee cost reporting:** employer PF, employer ESI, gratuity provision (and bonus provision), not employee deductions or TDS.
**Regulation / privacy note (awareness only):** From memory, unverified: rates, ceilings and eligibility change; confirm with payroll or finance before using any figure.
**Likely follow-ups:** 1) *Is TDS a cost to the company?* No, it is withheld from the employee. 2) *Why add employer costs to salary?* To see the true cost of an employee.
**Common mistakes:** Adding employee deductions to company cost; quoting rates from memory as facts; forgetting the gratuity provision.

### Q52 ⭐⭐ 🟢 What leave and attendance data does a company hold (casual, sick, earned, maternity leave, swipe records, regularisation requests), and what analyses can it support?
**Asked at:** commonly asked (no company-specific report found); HR dashboards and data integrity appear in HR-analyst job posts (unverified).
**What the interviewer is checking:** Whether you know what the raw data looks like and can link it to useful questions, not just name leave types.
**Say this in the interview:** "There are two families: leave records (who applied for what, approved or not) and attendance records (swipes, shifts, corrections). Together they show absence patterns, workload and early warning signs of disengagement."
**Explain simply:**
- **Leave balances and transactions:** one row per leave application: employee ID, leave type, from and to date, days, status (applied, approved, rejected, cancelled). Casual leave is short, unplanned time off; sick leave is for illness; earned (privilege) leave is accrued over service and can often be carried forward or encashed; maternity leave is statutory, long and tracked separately. Rules and quotas differ by company and by law (from memory, unverified).
- **Swipe records:** door or biometric punches, first-in and last-out times per day. They are a proxy for presence, not for work done.
- **Regularisation requests:** an employee asks to correct a day (forgot to swipe, worked from client site). Each request has a reason and an approver.
- **Analyses supported:** absence rate by team; Monday and Friday leave patterns; sick-leave spikes; unused earned-leave liability (a cost the company owes); late-coming trends; hours worked versus overtime; high regularisation counts as a sign of poor process or poor data; leave-taking before resignation.
**Data and tables involved:** Employee master (ID, team, location, shift), leave_transactions, leave_balances (monthly snapshot), swipe_log (employee, timestamp, device), regularisation_requests, holiday calendar. First cuts: absence days per employee per month, split by leave type and team.
**Regulation / privacy note (awareness only):** Sick and maternity leave reveal health and family information. From memory, unverified: restrict access, report in groups, and confirm with the compliance or legal team.
**Likely follow-ups:** 1) *How do you count a half-day?* As 0.5 day, and say so in the metric definition. 2) *Is a missing swipe an absence?* Not until you check leave and regularisation data.
**Common mistakes:** Treating swipes as productivity; ignoring public holidays and weekends in denominators; showing individual sick-leave data to line managers.

### Q53 ⭐⭐ 🟡 Compute the average span of control and the number of organisation layers for the data below, and say what you would flag.
Manager A has 4 direct reports
Manager B has 14
Manager C has 9
Manager D has 2
Manager E has 11
Managers A and B report to a director; C, D and E report to a different director; both directors report to the CEO
**Asked at:** commonly asked (no company-specific report found); span of control is a standard organisation-design metric.
**What the interviewer is checking:** Whether you can do the arithmetic, define "layer" clearly, and spot outliers rather than quote an average.
**Say this in the interview:** "Span of control is the number of direct reports per manager. The five managers average 8.0. There are four layers from CEO down to staff. I would flag B at 14 and D at 2, and the directors, who each manage only two or three people."
**Explain simply:**
- **Span of control** = direct reports of one manager. (4 + 14 + 9 + 2 + 11) / 5 = 40 / 5 = **8.0** for the five managers.
- **Layers:** CEO, directors, managers, staff = **4 layers** (3 levels of management). I state this counting the CEO as layer 1; some companies count from the CEO's reports.
- By group: Director 1's managers average (4 + 14) / 2 = 9.0; Director 2's average (9 + 2 + 11) / 3 = 7.3.
- If I include directors (spans 2 and 3) and the CEO (span 2), all eight managers average 47 / 8 = 5.9, which shows the top is narrow.
- **Flags:** B at 14 may be overloaded (feedback, hiring and appraisals suffer); D at 2 may be a layer that adds little; two directors with 2 to 3 managers each suggests a possibly thin middle. Spans are normally judged by role type (routine work allows wider spans), so I would not apply one fixed ideal number.
- Headcount check: 40 staff + 5 managers + 2 directors + 1 CEO = 48 people, assuming managers' reports are all staff.
**Likely follow-ups:** 1) *Mean or median?* Show both, plus the min and max; here the median is 9. 2) *Do contractors count?* State the rule; I would show spans with and without them.
**Common mistakes:** Counting the manager in their own span; reporting only the average; counting layers inconsistently; mixing player-coaches with pure managers.

### Q54 ⭐⭐ 🟡 Which fields do you need in an organisation hierarchy table to roll attrition up to a vice president's total team, and what goes wrong when a manager leaves and the team is reassigned?
**Asked at:** commonly asked (no company-specific report found); reporting-line data quality is a recurring HRIS theme (unverified).
**What the interviewer is checking:** Whether you understand hierarchies as data (parent-child links over time) and the effective-dating problem.
**Say this in the interview:** "I need each employee's ID, manager's ID and an effective start and end date, so I can walk up the chain to any VP as it was on the exit date. The risk is that a reassigned team gets rolled up to the new boss, rewriting history."
**Explain simply:**
- **Core fields:** employee_id, manager_id, effective_start_date, effective_end_date, department, level, location, and an active flag. A **snapshot** (monthly copy of who reported to whom) or effective-dated history lets you look backward.
- **Roll-up** means following manager_id upward repeatedly (employee to manager to director to VP). In SQL this is a recursive query; many HR tools precompute "level 1, level 2, level 3 manager" columns.
- **What goes wrong:** if you only keep today's manager, a leaver from March is attributed to whoever manages their old team now. When a manager leaves, their team may briefly show a blank manager (orphans), be double-counted under two managers during handover, or vanish from the VP's total.
- **Fixes:** attribute exits using the hierarchy on the last working day; keep an interim manager; flag blank manager IDs as a data-quality alert; reconcile VP totals back to company headcount.
**Data and tables involved:** employee_master, reporting_line_history (the effective-dated table), exits, month-end headcount snapshot. First cut: does the sum of all VPs' headcount equal total headcount?
**Likely follow-ups:** 1) *Matrix reporting?* Choose one primary line for roll-up and state it. 2) *Circular links?* A data error; test that nobody is their own ancestor.
**Common mistakes:** Joining exits to today's hierarchy; ignoring vacancies; forgetting that the manager's own exit also needs a home.

### Q55 ⭐⭐ 🟡 A department was split into two in July. How would you report attrition for the whole year for the old and the new structure without breaking comparability?
**Asked at:** commonly asked (no company-specific report found); restructuring comparability is a practical people-analytics issue.
**What the interviewer is checking:** Whether you can keep a time series consistent across an organisation change.
**Say this in the interview:** "I would report on both bases: the old structure for the full year by mapping every employee back to the original department, and the new structure with each person assigned as of their date, clearly labelled. I would never mix them in one trend line."
**Explain simply:**
- **Attrition rate** here = leavers in the period / average headcount in the period. Both parts must use the same unit definition.
- **View 1, old structure (like for like):** map the two new departments back to the one old department for all 12 months. January to December is comparable to last year.
- **View 2, new structure:** January to June exits are re-cut to the unit the person belongs to under the new split (restated history), so both new departments get a full year. Say that this is a "pro forma" view, meaning it applies the new structure backwards.
- **Alternative:** report each new unit only from July (six months) and annualise carefully, stating that the figure is a part-year rate.
- Keep a mapping table: old_dept, new_dept, effective date. Put a footnote on every chart.
**Likely follow-ups:** 1) *People who moved in July?* They are transfers, not exits (see Q56). 2) *Which view for the board?* The one that matches last year's comparison, plus the new view for forward planning.
**Common mistakes:** Calculating a new unit's rate on a headcount that only exists from July; annualising six months without saying so; silently changing the denominator.

### Q56 ⭐⭐ 🟡 A mid-year reorganisation moved 120 people from sales operations to a new shared-services unit. How do you stop this movement from showing up as attrition in one unit and as hiring in another?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you separate external movement (joins, exits) from internal movement (transfers).
**Say this in the interview:** "I classify each movement by type. A transfer between units is an internal move, so it is excluded from attrition and from new hires at the company level, and shown as a transfer-out for one unit and transfer-in for the other."
**Explain simply:**
- **Attrition** counts people who leave the company. **Hiring** counts people who join it. A reorganisation moves people inside the company, so neither applies.
- The problem arises when the system closes one record (exit-like) and opens another (join-like). Use a movement type field: Hire, Exit, Transfer-in, Transfer-out, Promotion, Reorg.
- **Unit-level reporting:** show opening headcount, plus hires, plus transfers in, minus exits, minus transfers out, equals closing headcount. For sales operations, the 120 is a transfer-out, so headcount falls by 120 but attrition does not rise.
- **Rate comparison:** for trends, restate history so the 120 people are in the shared-services unit for the whole period (as in Q55), or adjust the denominator.
- Check: company total headcount must not change because of the move (120 out, 120 in, net 0). If it does, the movement was coded as an exit and a hire.
- Also check that service dates and employee IDs are retained, otherwise tenure resets to zero.
**Likely follow-ups:** 1) *Do you ever count internal moves as exits?* For a unit-level "loss of talent" view only, shown separately as "unit outflow". 2) *Hiring by the new unit?* Count them as transfers-in, not hires.
**Common mistakes:** Reporting 120 extra exits in sales ops; double-counting them as hires; resetting tenure; not reconciling company headcount before and after.

### Q57 ⭐⭐ 🟡 The table below lists leavers and stayers by pay position in band. Compute the share of each group below band midpoint and say what it suggests and what it does not.
Leavers: 60 total, 42 below midpoint
Stayers: 940 total, 376 below midpoint
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can compute a simple comparison and avoid concluding causation.
**Say this in the interview:** "70% of leavers were below the band midpoint versus 40% of stayers, a gap of 30 percentage points. Low pay position is associated with leaving, but this alone does not prove pay caused it."
**Explain simply:**
- A **pay band** is the minimum-to-maximum salary range for a job grade; the **midpoint** is its halfway point, roughly the market-typical pay for a fully competent person.
- Leavers below midpoint: 42 / 60 = **70.0%**. Stayers below midpoint: 376 / 940 = **40.0%**.
- Difference = 30 percentage points (not "30%"); leavers are 1.75 times as likely to be below midpoint.
- **Suggests:** people paid lower in their band are over-represented among leavers; worth a closer look, particularly if concentrated in a team or grade.
- **Does not suggest:** that raising pay would stop exits. Confounders: junior or newly hired people sit lower in band and leave more anyway; low performers may be paid lower and be pushed out; some leavers leave for reasons unrelated to pay.
- Also note, all 60 leavers are measured at exit but stayers at one date; use pay position at a fixed point (for example 6 months before) for both groups.
**Likely follow-ups:** 1) *How would you test it?* Compare within the same grade and tenure, or use a regression. 2) *Sample size?* 60 leavers is small; do not slice too thinly.
**Common mistakes:** Calling it "30% higher"; saying "pay causes attrition"; ignoring tenure and grade mix.

### Q58 ⭐⭐ 🟡 Attrition by time since last promotion is 8% for under 1 year, 11% for 1 to 2 years, 15% for 2 to 3 years and 24% for over 3 years. What does this suggest, and what other variables could be confounding it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Pattern reading, restraint on causation, and a sensible list of confounders.
**Say this in the interview:** "Attrition rises steadily with time since promotion, and it is three times higher (24% vs 8%) after three years. That points to stagnation as a risk, but tenure, grade, performance and manager could explain part of it."
**Explain simply:**
- Reading: 8%, 11%, 15%, 24%. The jump is largest after year 3, so the risk is not linear.
- **Confounder** = another factor that drives both things. Time since promotion rises with **tenure**, and tenure itself relates to attrition.
- Others: **grade or level** (senior levels promote less often); **performance** (high performers promoted faster, but low performers stuck may be leaving or being managed out); **age or career stage**; **function** (some job families have slow ladders); **pay position** (stuck people sit at the top of their band); **manager and team**; **location and market demand** for the skill.
- Survivor bias: those who left early never reach year 3, so the over-3 group is people who stayed this long.
- Next step: compare within the same tenure and grade bands; if the gap persists, the promotion link is stronger.
**Likely follow-ups:** 1) *Action?* Review the over-3-year group for promotion readiness, a targeted conversation, not automatic promotion. 2) *Rate type?* State the period (annual, trailing 12 months).
**Common mistakes:** Saying promotion would cure attrition; not controlling for tenure; ignoring the group sizes behind each percentage.

### Q59 ⭐⭐ 🟡 At a given date, 48 employees have resigned but are serving notice, and 30 of them will have their last working day next month. How would you use this pending-exit pipeline in a headcount forecast?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you treat known exits separately from predicted exits.
**Say this in the interview:** "Those 48 are known exits, so I subtract them on their last working dates: 30 next month and 18 later. On top of that I add an estimate for people who have not resigned yet."
**Explain simply:**
- **Notice period:** time between resignation and last working day (often somewhere between 30 and 90 days, from memory, unverified; it varies by company and level). The person still counts in headcount until the last day.
- Known exits: 30 next month, 48 - 30 = **18** in the months after (use each person's actual date).
- **Forecast closing headcount** = opening + planned hires (joined) - known exits - expected new resignations that also leave within the period. A resignation next week with a 60-day notice would not leave this month.
- **Risks to adjust for:** some resignations are withdrawn (counter-offers); notice buyouts bring dates forward; extensions push them back. Use history to apply a small withdrawal percentage.
- Use the pipeline also as an early signal to recruiters: 30 backfills needed within a month, and a lead time of weeks to fill them.
**Data and tables involved:** resignation table (resignation date, last working day, notice status), headcount snapshot, open requisitions, offer-accepted list.
**Likely follow-ups:** 1) *Why not use a flat 16% annual attrition?* Because it ignores the exits you already know about. 2) *Does the pipeline show attrition risk by team?* Yes, group by team.
**Common mistakes:** Subtracting all 48 at once; subtracting them from today's headcount; double-counting them in both the known and the predicted exits.

### Q60 ⭐⭐ 🟡 Why might top performers leave at a different rate from average performers, and how would you compare them using ratings data that are only available once a year?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Awareness of timing issues in ratings and of selection effects.
**Say this in the interview:** "Top performers often have more outside options and higher expectations, but may also be better retained with pay and attention. To compare fairly I fix each person's rating as of the last completed cycle and track exits for the next 12 months."
**Explain simply:**
- Why rates differ: top performers are noticed by recruiters; they expect faster promotion and pay; or they may be retained through bonuses and development. Low performers may leave voluntarily or be pushed out, so look at **voluntary** and **involuntary** exits separately.
- **Problem with annual ratings:** the rating is a snapshot. People who leave before the cycle have no rating, and a rating given in March tells you nothing about someone who resigned in January.
- **Method:** use the most recent rating before the observation date, then follow the group forward for 12 months (a cohort). Rate = leavers in the group / headcount at start.
- People with no rating (new joiners, early leavers) form their own group; do not drop them.
- Compare like with like: control for grade, tenure and team.
**Likely follow-ups:** 1) *Does the rating itself change?* Yes, calibration can move ratings, so use the final one. 2) *Small group?* Top performers may be a small slice of staff (say 10 to 15%, illustrative), so numbers are small; avoid conclusions from a handful of exits.
**Common mistakes:** Using the rating that comes after the person left; excluding unrated leavers; mixing voluntary and forced exits.

### Q61 ⭐⭐ 🟡 What is a boomerang (rehired) employee, how would you measure the rehire rate, and what decisions could the data inform?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Concept clarity and the data problem of tracking one person across two stints.
**Say this in the interview:** "A boomerang is someone who left and later came back. I measure rehire rate as rehires divided by total hires in the period, after making sure each person keeps one ID across stints."
**Explain simply:**
- **Rehire rate** (definition I use) = rehired former employees / all external hires in the period. For example, 12 rehires among 300 hires = 4.0%. Other definitions exist (share of past leavers who return); state yours.
- **Data issue:** if a rehire gets a new employee ID, they look like a fresh hire. Match on a permanent ID, email, or PAN-type national ID (restrict access), and keep prior-service dates.
- Decisions it can inform: alumni outreach, rehire eligibility rules, how long to keep leavers' records, whether leaving on good terms matters, onboarding that skips basics, salary decisions on return.
- Add context: time away, reason for leaving, whether rehires stay longer than new hires, and their performance.
**Data and tables involved:** employee master with a person ID, exits (with reason and rehire-eligible flag), hires with a previous-employee flag.
**Regulation / privacy note (awareness only):** Keeping ex-employee data for alumni outreach needs a clear purpose and retention limit. From memory, unverified; confirm with legal.
**Likely follow-ups:** 1) *Is a high rate good?* Maybe, but it may also mean people leave to find out the market is no better. 2) *Contractors who become employees?* Define whether they count.
**Common mistakes:** Counting new IDs as fresh hires; not stating the denominator; treating returning interns as the same as experienced rehires.

### Q62 ⭐⭐ 🟡 The company's attrition is 16% but it rose from 9% in the sales team to 25% while engineering stayed at 8%. What further cuts (tenure, manager, location, hire source, pay position) would you apply first, and in what order?
**Asked at:** commonly asked (no company-specific report found); drill-down on attrition is a staple of HR analytics question banks (unverified).
**What the interviewer is checking:** Structured, hypothesis-led drill-down instead of random slicing.
**Say this in the interview:** "I would focus on sales, split voluntary from forced exits, then cut by tenure, then manager, location, hire source and pay position, because each step narrows where the problem sits."
**Explain simply:**
- **Step 0:** confirm the numbers: same definition, enough people, exits by type (voluntary vs involuntary), and check for a reorg or a sales-target change.
- **1. Tenure:** are exits in the first year (hiring or onboarding problem) or after several years (career or pay problem)?
- **2. Manager:** are exits concentrated under a few managers? That is the strongest, most actionable cut.
- **3. Location:** is it one city or office (local competitor, site issue)?
- **4. Hire source:** campus, agency or referral; some sources bring people who leave early.
- **5. Pay position:** below band midpoint, or high-performers paid low (see Q57).
- Then combine the top two cuts (for example new joiners under three managers). Stop cutting when the groups get too small to trust.
- Remember the rate is a headcount mix issue too: sales has high turnover roles by nature, so compare with last year and with the industry (benchmarks from memory, unverified).
**Likely follow-ups:** 1) *Why tenure first?* It separates early-stage from long-term causes cheaply. 2) *Next step?* Exit interview themes and a stay survey for the affected team.
**Common mistakes:** Slicing five ways at once; using tiny groups; ignoring forced exits; jumping to a cause.

### Q63 ⭐⭐ 🟡 A company made 400 campus offers in December for July joining, and 340 joined. Compute the joining rate and say which data cuts (college tier, branch, offer date, interim offers elsewhere) you would use to find the leak.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Calculation plus a funnel-leak approach for a long gap between offer and joining.
**Say this in the interview:** "Joining rate is 340 / 400 = 85%, so 60 offers (15%) did not convert. I would cut the drop-outs by college tier, branch, offer date and by whether they accepted a rival offer."
**Explain simply:**
- **Joining rate (offer-to-join)** = joined / offers made = 340 / 400 = **85.0%**; the drop-out is 60 people, 15.0%. (Offer acceptance is a different earlier step.)
- **Campus** means hiring final-year students; the gap between December offer and July joining is about 7 months, long enough for rival offers or changes of plan.
- Cuts: **college tier** (top-tier students get multiple offers); **branch** (high-demand branches such as computer science may be poached); **offer date** (earlier offers wait longer, so more drop); **interim offers elsewhere** (survey or social signals); also **offer-to-joining engagement** (contacts made, onboarding emails opened), joining bonus, and location.
- Compare each cut's joining rate against 85%; flag cuts that are well below it and large enough in count.
**Data and tables involved:** offers (candidate, college, branch, offer date, location), joiners (join date), engagement log, reason for drop (if captured).
**Likely follow-ups:** 1) *Action?* Keep contact in the gap; consider a joining bonus (cost trade-off); over-offer by a buffer based on the history. 2) *Is 85% good?* Compare with your prior years, not an external number.
**Common mistakes:** Mixing acceptance and joining rates; not using last year's rate; no reason capture on drop-outs.

### Q64 ⭐⭐ 🟡 A hiring plan asked for 240 hires by September; actual hires were 168 and 36 more offers are accepted but not yet joined. Compute plan attainment and the likely year-end position, and say which assumptions you made.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Arithmetic plus a clear separation of actual, pipeline and assumption.
**Say this in the interview:** "Attainment so far is 168 / 240 = 70%. If all 36 pending offers join, we reach 204, or 85%, still 36 short of plan. With some drop-out, closer to 200."
**Explain simply:**
- **Plan attainment** = actual hires / planned hires = 168 / 240 = **70.0%**; shortfall is 72.
- Best case with the pipeline: 168 + 36 = 204 = **85.0%** of plan; gap to plan 240 - 204 = **36**.
- Realistic case: assume 10% of accepted offers do not join (an invented figure; use your own history): 36 x 0.9 = 32.4, rounded to 32, so 168 + 32 = **200**, about 83% of plan.
- **Assumptions:** the 36 join before year end; no extra offers beyond those 36; the 240 is for the whole plan period, so the remaining 36 (or 40) will need new offers made soon, given the time-to-hire and notice periods; interpretation: "by September" is the plan cut-off date, not a year-end target. If the plan runs to year end, say so and re-state.
- Note: hires made are not the same as headcount; exits during the period offset them.
**Likely follow-ups:** 1) *What would you tell the business?* We need roughly 36 more offers at once to hit plan, and the notice periods make that unlikely this year. 2) *Net headcount?* Subtract expected exits.
**Common mistakes:** Counting accepted offers as hires; forgetting offer drop-out; not stating the plan period.

### Q65 ⭐⭐ 🟡 One recruiter closed 18 positions from 30 assigned requisitions in a quarter and another closed 9 from 12. How would you compare them fairly?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you see that raw closure rates ignore difficulty, volume and sample size.
**Say this in the interview:** "Raw closure is 60% for the first recruiter and 75% for the second, but they are not comparable until I adjust for role difficulty, age of requisitions and workload, and note that 12 requisitions is a very small sample."
**Explain simply:**
- A **requisition** is an approved open job position that a recruiter works to fill.
- Closure rate: 18 / 30 = **60.0%**; 9 / 12 = **75.0%**. The first recruiter filled twice as many roles (18 vs 9) with a larger load.
- Small numbers: the difference of 15 percentage points is within what chance can produce (a standard test for comparing two proportions, Fisher's exact test, gives a p-value of about 0.48; in plain words, a gap this large would appear by chance roughly half the time even if both recruiters were equally good), so do not rank on it.
- **Fair comparison adds:** seniority and skill of roles (niche roles close slowly); how old each requisition is when assigned; hiring manager responsiveness; location; requisitions cancelled or put on hold (exclude them from the denominator); quality (90-day retention, hiring manager satisfaction); time to fill; offer acceptance.
- Use a like-for-like cohort (same job family and level) and the same time window.
**Likely follow-ups:** 1) *Single scorecard?* Use several measures; one rate encourages gaming. 2) *Who is better?* I cannot say yet.
**Common mistakes:** Ranking on rate alone; including cancelled requisitions; ignoring role mix; rewarding speed at the cost of quality.

### Q66 ⭐⭐ 🟡 What would you measure about the candidate experience in recruiting (survey scores, stage drop-off, communication delay), and from which systems would the data come?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Knowledge of the recruiting data landscape and a balanced set of measures.
**Say this in the interview:** "I would combine what candidates say (surveys), what they do (drop-off by stage) and how fast we respond (time between steps), pulled from the ATS and the survey tool."
**Explain simply:**
- **ATS** (applicant tracking system) is the software that holds each candidate's stage history, dates and recruiter notes.
- **Say:** post-interview or post-offer survey score (satisfaction, or a likelihood-to-recommend score), comments, rejected-candidate feedback.
- **Do:** stage-to-stage conversion; drop-off by stage and who withdrew (candidate vs company); no-shows to interviews; offer decline reasons.
- **Time:** days from application to first response; days between interview and feedback; time to offer; scheduling delays; number of reschedules.
- **Systems:** ATS (stages, dates), the careers site and scheduling tool, email logs, survey tool, interview feedback forms, HRIS (for later joiners).
- Segment by role, source, location and recruiter. Report response rates for the survey, since only some candidates reply.
**Data and tables involved:** candidate_stage_history (candidate, requisition, stage, entry date, exit date, outcome), survey_responses, interviews, offers.
**Regulation / privacy note (awareness only):** Candidate data is personal data; consent, retention limits and purpose need to be clear. From memory, unverified; confirm with legal.
**Likely follow-ups:** 1) *Which matters most?* Communication delay, usually, as it is controllable. 2) *Survey bias?* Rejected candidates reply less.
**Common mistakes:** Only surveying those who got offers; averaging scores without response counts; ignoring the delay between steps.

### Q67 ⭐⭐ 🟡 Of 60 joiners, 4 never turned up on the joining date and 3 left within the first week. What would you call these figures, and what pre-joining data would you review?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Correct names for early-stage loss and awareness of what predicts it.
**Say this in the interview:** "The 4 are no-shows, or offer drop-outs on joining day: 4 out of 60 expected joiners is 6.7%. The 3 are early attrition, or first-week exits. If I count against those who actually joined (56), that is 3 out of 56 = 5.4%."
**Explain simply:**
- **No-show (joining drop-out):** accepted the offer but did not arrive. 4 / 60 = **6.7%** of expected joiners.
- **First-week attrition:** joined, then left in the first 7 days: 3 / 56 = **5.4%** of actual joiners (3 / 60 = 5.0% of expected). State the denominator.
- Combined loss from the expected group: 7 / 60 = **11.7%**; only 53 remain.
- Definitions vary by company ("early attrition" may mean 30, 90 or 180 days); say yours.
- **Pre-joining data to review:** notice period length and notice-buyout status, number of days between offer and joining, competing offers, pay increase offered, source (agency, referral, campus), recruiter and hiring manager, BGV delays (see Q68), engagement during notice, interview experience and any change of role or location after the offer.
- Check for patterns: one recruiter, one role, long notice periods, small pay hikes.
**Likely follow-ups:** 1) *Reduce it?* Stay in touch during notice, early manager call, a clear first-day plan. 2) *Do exits count in attrition?* Yes, as early attrition; no-shows are normally not employees.
**Common mistakes:** Calling a no-show "attrition"; not stating the denominator; treating the 7 as one number.

### Q68 ⭐⭐ 🟡 Background verification (BGV) fails or is delayed for 9% of offered candidates. Which measures (turnaround time, discrepancy rate, fall-out stage) would you report, and what privacy concerns arise?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Process measurement ability and sensitivity to personal data.
**Say this in the interview:** "I would report how long BGV takes, how often checks find a mismatch, and at which check or stage candidates fall out, and I would only share results needed for the hiring decision."
**Explain simply:**
- **BGV** is checking that what a candidate stated (identity, past employers, education, address, sometimes criminal records) is true, usually by an outside vendor.
- **Turnaround time (TAT):** days from case initiation to final report, by check type, median and 90th percentile, against the agreed vendor service level.
- **Discrepancy rate:** cases with at least one mismatch / cases completed. Split minor (date off by a few days) from major (fake degree).
- **Fall-out stage:** where cases stop: documents not submitted, employer not responding, education check pending, adverse finding, candidate withdrew.
- Also: pending cases ageing beyond a set number of days, the share of candidates joined before BGV closed, vendor performance, and the 9% split into "failed" vs "delayed", which need different actions.
**Regulation / privacy note (awareness only):** BGV uses sensitive personal data (identity documents, criminal and employment history). Principles: tell the candidate and get consent, collect only what the role needs, restrict access, limit sharing with vendors under contract, delete after the retention period. From memory, unverified; confirm with the compliance or legal team. Report in aggregates, not with names.
**Likely follow-ups:** 1) *Can delay be reduced?* Early document collection and vendor follow-up. 2) *Should failed BGV be shared widely?* No, only with those who decide.
**Common mistakes:** Combining failed and delayed; no TAT by check; reporting candidate names in dashboards; ignoring minor versus major discrepancies.

### Q69 ⭐⭐ 🟡 What is the interview-to-offer ratio and interviews per hire, and how would you compute them from an interview-level table with candidate IDs and panel members?
**Asked at:** commonly asked (no company-specific report found); recruiting-funnel metrics appear in HR-metric guides (unverified).
**What the interviewer is checking:** Whether you know the grain of the table (one row per panel member, not per interview) and avoid double counting.
**Say this in the interview:** "Interview-to-offer is how many candidates we interview for each offer made; interviews per hire is how many interview sessions we run for each person who joins. I count distinct candidate-and-round pairs, not panel rows."
**Explain simply:**
- A panel is several interviewers meeting one candidate at once. If the table has one row per panel member, a 3-person panel creates 3 rows for 1 interview. Counting rows overstates effort.
- Interview-to-offer ratio = candidates interviewed : offers made (or offers divided by candidates interviewed, as a %).
- Interviews per hire = distinct interview sessions (candidate and round) divided by hires. A second view, panel-member hours per hire, counts every row because each interviewer spends time.
- Definitions vary by company; state yours.

**Worked example:** 4 candidates were interviewed (11 panel rows, 6 distinct candidate-round sessions). 2 got offers, 1 joined.
- Interview-to-offer: 4 candidates : 2 offers = 2 to 1, or 50% of interviewed candidates received an offer.
- Interviews per hire: 6 sessions / 1 hire = 6.0. Per offer: 6 / 2 = 3.0.
- Wrong way: 11 rows / 1 hire = 11, which counts every panelist as a separate interview.
```sql
-- one session = one candidate in one round, however many panelists
SELECT COUNT(DISTINCT candidate_id)                AS candidates_interviewed,
       COUNT(DISTINCT candidate_id || '-' || round_no) AS interview_sessions
FROM interviews;
```
Output: 4 candidates, 6 sessions. Join to an offers table for offers and hires.

**Likely follow-ups:** 1) *Is a high number bad?* It can mean unclear job criteria or a slow, repetitive process; compare by role. 2) *Why panel-member count?* It shows the real interviewer time spent.
**Common mistakes:** Counting panel rows as interviews; dividing by hires when a role had no hires yet; mixing roles with different round counts.

### Q70 ⭐⭐ 🟡 What share of hires should come from internal moves and from referrals, and how would you measure the quality of referral hires against other sources?
**Asked at:** commonly asked (no company-specific report found); source-of-hire is a standard recruiting metric in HR guides (unverified).
**What the interviewer is checking:** That you do not quote a "magic" share and that you know how to judge quality fairly.
**Say this in the interview:** "There is no universal right share; it depends on company size, growth and role mix. I would track the share over time and judge each source by what happens after the hire, not just by how many people it brings."
**Explain simply:**
- Internal moves (a current employee takes a new role) keep skills and cost less, but too many leave the pool of new ideas and create gaps behind.
- Referrals (an employee recommends someone) are usually quick, but can reduce diversity if everyone refers similar people.
- Quality means outcomes by source, compared on the same roles and hire period: first-year attrition, performance rating at 12 months, time to productivity, offer acceptance, and time to fill.
- Compare like with like: referrals for a role type against other sources for the same role type and level, with group sizes shown.
- Check referral bonus cost against agency fees.
- Small groups: show counts, not just percentages.

**Likely follow-ups:** 1) *Is "referrals stay longer" proof?* No; referrers may suggest people they know will fit, or roles differ. 2) *What about diversity?* Compare source mix across gender and background groups.
**Common mistakes:** Quoting an industry "ideal" as fact; judging quality by volume; ignoring that new hires from recent months have not had time to leave.

### Q71 ⭐⭐ 🟡 What is time-to-productivity (ramp-up) for new joiners, and what data would you use to estimate it for a sales team or a support team?
**Asked at:** commonly asked (no company-specific report found); ramp-up is a typical onboarding metric (unverified).
**What the interviewer is checking:** Whether you can turn "productive" into something measurable per role.
**Say this in the interview:** "Time-to-productivity is how long a new joiner takes to reach the normal output of an experienced colleague in the same role. I would define 'normal' as a target from tenured staff, then find the month a new joiner first reaches it."
**Explain simply:**
- Ramp-up is the learning period when someone is paid but not yet at full output.
- Sales: monthly revenue or quota attainment per rep by months since joining; compare with tenured reps' median. Ramp = first month the new rep reaches, say, 80% of the tenured median (the 80% line is your choice; state it).
- Support: tickets closed per day, average handling time (minutes per ticket), first-contact resolution (share solved at the first reply), quality score; compare against tenured agents.
- Data: joining date, role, manager, monthly performance data, plus territory or ticket difficulty so a hard start is not blamed on the person.
- Use cohorts (all joiners of one month) and the median, not one star hire.

**Likely follow-ups:** 1) *Why does it matter?* It sets realistic targets and hiring plans. 2) *What if people leave first?* Include leavers; ignoring them makes ramp look too good (survivor bias).
**Common mistakes:** Using calendar months instead of months since joining; comparing with the best performer instead of the median; ignoring that some quarters are seasonally easier.

### Q72 ⭐⭐ 🟡 The hiring manager rejects most profiles that recruiters shortlist. What data would you collect to find out whether the problem is the job description, the sourcing or the screening?
**Asked at:** commonly asked (no company-specific report found); a typical recruiting-funnel diagnosis case (unverified).
**What the interviewer is checking:** Whether you split a vague complaint into testable causes.
**Say this in the interview:** "I would not guess. I would look at where candidates drop in the funnel, why the manager rejected each profile, and how rejected profiles differ from accepted ones, then link each pattern to the job description, the source or the screen."
**Explain simply:**
- Funnel: applied, screened, shortlisted, manager-reviewed, interviewed, offered, joined, by requisition and by source.
- Rejection reasons: ask the manager to tag each rejection (skills, experience level, salary expectation, location, communication). Free text is hard to count, so use a short list.
- Job description (JD) problem: rejection reasons point to a mismatch between what the JD says and what the manager wants; compare JD requirements with the skills of accepted profiles.
- Sourcing problem: one source (portal, agency, referral) has far more rejections than others.
- Screening problem: profiles pass the recruiter's checklist but fail on the same point every time; the screen checks the wrong thing.
- Compare with other requisitions for the same role to see if this manager is an outlier.

**Data and tables involved:** requisitions (role, manager, JD version), candidates (source, date), stage history (stage, date, outcome), rejection reasons, offers and joins. First cut: rejection rate by source and by reason.
**Likely follow-ups:** 1) *Quick fix?* A calibration meeting: manager and recruiter review 5 profiles together. 2) *How measure success?* Higher manager acceptance rate on shortlists.
**Common mistakes:** Blaming recruiters without data; no rejection reason captured; judging on tiny counts.

### Q73 ⭐⭐ 🟡 The rating distribution is 12% outstanding, 55% exceeds, 30% meets and 3% below. The guideline was 10%, 25%, 55%, 10%. Compute how far each category is from guideline and say what you would check before telling leadership about rating inflation.
**Asked at:** commonly asked (no company-specific report found); performance-rating distribution is a common HR analytics exercise (unverified).
**What the interviewer is checking:** Percentage-point arithmetic, and caution before calling a pattern a problem.
**Say this in the interview:** "Outstanding is 2 points over guideline, exceeds is 30 points over, meets is 25 under and below is 7 under. The top two ratings total 67% against a guideline of 35%, so it looks inflated, but I would check a few things before saying so."
**Explain simply:**
- Rating inflation means ratings drift upward without a matching rise in real performance.
- Differences are in percentage points (pp), actual minus guideline.

**Worked example:**

| Category | Actual | Guideline | Gap |
|---|---|---|---|
| Outstanding | 12% | 10% | +2 pp |
| Exceeds | 55% | 25% | +30 pp |
| Meets | 30% | 55% | -25 pp |
| Below | 3% | 10% | -7 pp |

Gaps add to zero, as they should. Top two ratings: 12 + 55 = 67% vs 10 + 25 = 35%, a gap of +32 pp.
- Check: the data covers all employees and the same cycle (no missing ratings).
- Check: is the guideline a rule or a suggestion, and was it communicated?
- Check: spread by department, manager and grade; inflation may sit in a few teams.
- Check: did business results and goal achievement also rise? High ratings in a poor year point to leniency.
- Check: compare with last years, and with pay or promotion outcomes.

**Likely follow-ups:** 1) *Could high ratings be genuine?* Yes, after strong hiring or a good year. 2) *What next?* Calibration sessions across managers.
**Common mistakes:** Mixing "percent" and "percentage points"; calling it inflation from one cycle; naming individual managers without context.

### Q74 ⭐⭐ 🟡 From the 9-box table below, compute the share of employees in each talent group (high performance and high potential, core, low performance and low potential) and say how HR might use the result.
High performance and high potential: 45
High performance and medium potential: 90
Medium performance and medium potential: 210
Low performance and any potential: 55
**Asked at:** commonly asked (no company-specific report found); 9-box grids are common in talent-review discussions (unverified).
**What the interviewer is checking:** Grouping boxes sensibly, computing shares, and using the result with care.
**Say this in the interview:** "There are 400 employees. About 11% are high performance and high potential, 75% are core, and 14% are low performance. HR can use this to plan succession and development, but not as a final verdict on people."
**Explain simply:**
- A 9-box grid places each person by performance (what they deliver now) and potential (how far they could grow).
- Grouping: high-high is the talent pool; "core" is the steady middle; low performance is those needing support.
- I grouped "high performance, medium potential" (90) with core because the question lists only three groups; a company could also call these strong performers. State the grouping.

**Worked example:** Total = 45 + 90 + 210 + 55 = 400.
- High performance and high potential: 45 / 400 = 11.25%
- Core: (90 + 210) / 400 = 300 / 400 = 75.0%
- Low performance and low potential: 55 / 400 = 13.75% (the table says "any potential", so this box is wider than the label)
- Shares add to 100%.
- Uses: succession planning (do we have enough ready successors per leadership role?), targeted development, retention watch on the top group, support plans for the bottom group.

**Likely follow-ups:** 1) *Is 11% enough?* Compare with the number of senior roles to fill. 2) *Is the grid objective?* No, manager judgement drives it; check calibration.
**Common mistakes:** Treating the grid as a verdict; leaving the table with no counts; sharing individual placements widely (it is sensitive).

### Q75 ⭐⭐ 🟡 What are the four Kirkpatrick levels of training evaluation, and which levels can you measure from a learning management system versus other data?
**Asked at:** commonly asked (no company-specific report found); a standard L&D evaluation framework (from memory, unverified).
**What the interviewer is checking:** Do you know the framework and the limits of LMS data.
**Say this in the interview:** "The four levels are reaction, learning, behaviour and results. A learning management system (LMS, the software that hosts and tracks courses) covers levels 1 and 2 well; levels 3 and 4 need data from managers and business systems."
**Explain simply:**
- Level 1 Reaction: did people like it? LMS feedback forms.
- Level 2 Learning: did they learn? Quiz or test scores in the LMS (best with a pre-test and post-test).
- Level 3 Behaviour: do they work differently afterwards? Manager observation, 360 feedback, performance data; not in the LMS.
- Level 4 Results: did the business improve? Sales, error rates, ticket times, safety incidents, attrition, from business systems.
- Higher levels are more useful but harder, because other factors also change results; use a comparison group of untrained staff where possible.

**Likely follow-ups:** 1) *What about ROI?* Some add it as level 5: benefit minus cost, divided by cost. 2) *Most measured level?* Level 1, because it is easy.
**Common mistakes:** Treating completion rate as impact; claiming training caused a result without a comparison group.

### Q76 ⭐⭐ 🟡 Mandatory compliance training (for example, prevention of sexual harassment and code of conduct) had 1,640 completions from 1,820 assigned employees by the deadline. Compute the completion rate and say what you would report and to whom.
**Asked at:** commonly asked (no company-specific report found); compliance-training completion is a routine HR report (unverified).
**What the interviewer is checking:** Simple rate arithmetic plus knowing the audience and the sensitivity.
**Say this in the interview:** "The completion rate is 1,640 divided by 1,820, which is 90.1%. 180 people are pending. I would report the gap by department and manager to HR and compliance, with a plan to close it."
**Explain simply:**
- Completion rate = completions / assigned.
- Pending = 1,820 - 1,640 = 180 employees, 9.9%.
- Report: overall rate, by department, location and manager, new joiners vs old, days overdue, and trend against last cycle.
- Audience: HR head and the compliance or legal team (they may need evidence of coverage); department heads get their own team's list for follow-up.
- Check definitions: are leavers, people on long leave and new joiners (assigned late) excluded from the 1,820? Is a half-finished course counted?
- Keep individual names to those who need to chase them.

**Regulation / privacy note (awareness only):** Many countries, including India, expect employers to have a harassment-prevention policy and awareness measures (from memory, unverified; confirm with the compliance/legal team what evidence is needed).
**Likely follow-ups:** 1) *Is 90% good?* Compliance training usually targets close to 100%; depends on policy. 2) *What would you do?* Reminders, manager escalation, set a final date.
**Common mistakes:** Dividing by total employees instead of assigned; counting started as completed; not stating the cut-off date.

### Q77 ⭐⭐ 🟡 What would you measure about onboarding (30-60-90 day check-ins, early attrition, manager rating of the new joiner, time to first task), and how would you judge whether a new onboarding programme is helping?
**Asked at:** commonly asked (no company-specific report found); onboarding metrics appear in HR-metric guides (unverified).
**What the interviewer is checking:** Choosing measures and judging a programme with a fair comparison.
**Say this in the interview:** "I would measure early attrition, check-in completion, manager and new-joiner ratings, and time to first task. To judge the new programme I compare joiners on it with similar joiners before it or on the old programme."
**Explain simply:**
- Onboarding is everything that helps a new joiner start well: documents, laptop, introductions, training, check-ins.
- Early attrition: share who leave within 90 days (and within 6 or 12 months).
- Check-ins: share of 30-60-90 day conversations done on time, and scores from them.
- Manager rating of the new joiner at 90 days; new-joiner survey on how welcome and clear they felt.
- Time to first task: days from joining to first real work assignment or system access ready.
- Judging: compare cohorts on the same measures. Account for other changes (hiring mix, season). Small cohorts need caution: show counts.
- A pilot where some teams get the new programme and others do not gives the cleanest comparison.

**Likely follow-ups:** 1) *When to judge?* Early signs at 90 days; attrition needs 6 to 12 months. 2) *What if only happy people answer?* Note the response rate.
**Common mistakes:** Judging on one cohort; counting only survivors; ignoring role mix between cohorts.

### Q78 ⭐⭐ 🟡 What employee relations data (grievances, disciplinary cases, harassment complaints, closure time) might an analyst handle, and what extra care does this data need?
**Asked at:** commonly asked (no company-specific report found); employee data sensitivity is a recurring interview theme (unverified).
**What the interviewer is checking:** Awareness that this is among the most sensitive HR data.
**Say this in the interview:** "I might see counts of grievances, disciplinary cases and harassment complaints with closure times, but I would work on anonymised, grouped data, with strict access, and never expose names."
**Explain simply:**
- Typical measures: number of cases by type, by month, by location; average and median days to close; share closed within the policy time; repeat cases; outcome categories.
- Why extra care: cases involve named people, reputation and sometimes legal action; a leak can harm the complainant and the accused.
- Use the minimum data needed; remove names and IDs for trend work.
- Suppress small groups: if a department has 2 cases, reporting it by department may identify the person (a common rule is a minimum group size; set it with HR and legal).
- Restrict access to a named few, log who views it, and store it separately.
- Report patterns, not stories; do not guess at causes.

**Regulation / privacy note (awareness only):** India's data protection law and the workplace harassment law have confidentiality aspects (from memory, unverified; confirm with the compliance/legal team).
**Likely follow-ups:** 1) *Why median closure time?* A few long cases skew the average. 2) *Can you share with leadership?* Only aggregated and cleared.
**Common mistakes:** Emailing case lists; breaking totals down until one person is identifiable; treating a rise in complaints as automatically bad (it can show more trust in reporting).

### Q79 ⭐⭐ 🟡 Compute the Bradford factor for the two employees below (spells squared times total days absent) and say what it is meant to show and what its limits are.
Employee X: one absence of 10 days
Employee Y: ten absences of one day each
**Asked at:** commonly asked (no company-specific report found); the Bradford factor is a known absence-scoring formula (from memory, unverified).
**What the interviewer is checking:** Can you apply the formula and see why it weights frequency.
**Say this in the interview:** "X scores 1 squared times 10 = 10. Y scores 10 squared times 10 = 1,000. Both lost 10 days, but the formula treats frequent short absences as far more disruptive."
**Explain simply:**
- A spell is one continuous absence. Bradford factor = (number of spells)^2 x total days absent, usually over a rolling 52 weeks.
- It aims to flag patterns of frequent short absence, which disrupt teams more than one long one.

**Worked example:**
- X: 1 spell, 10 days: 1^2 x 10 = 10
- Y: 10 spells, 10 days: 10^2 x 10 = 1,000
- Same days, a 100-times higher score for Y.
- Limits: ignores the reason (a chronic illness, surgery, caring duties, pregnancy-related illness or disability may be legally protected in some places; from memory, unverified); penalises people who are genuinely ill; thresholds are arbitrary; it ignores part-time work patterns; and it can pressure sick people to come to work. Use it as one prompt for a conversation, never as an automatic penalty.

**Likely follow-ups:** 1) *Better alternative?* Look at absence rate plus reason categories, with manager conversation. 2) *Who should see scores?* HR and line manager only.
**Common mistakes:** Squaring days instead of spells; using it to discipline automatically; mixing different periods.

### Q80 ⭐⭐ 🟡 Employees have accumulated 12,000 unused earned-leave days and the average daily salary is INR 2,500. Estimate the leave encashment liability and say which team besides HR would want this number.
**Asked at:** commonly asked (no company-specific report found); leave liability is a finance-HR interface topic (unverified).
**What the interviewer is checking:** Simple arithmetic, and awareness that leave is a financial liability.
**Say this in the interview:** "12,000 days times INR 2,500 is INR 3 crore (30,000,000). Finance would want it because unused leave is money the company may have to pay later."
**Explain simply:**
- Earned leave (EL) is paid leave that builds up through the year. Some companies let unused days carry forward, and some pay cash for them on exit or at year end (encashment).
- Liability means an amount owed in future. Finance records it in the accounts (provision), so the accountants and auditors care.

**Worked example:** 12,000 days x INR 2,500 = INR 30,000,000 = INR 3.00 crore (1 crore = 10 million).
- This is a rough estimate. Real figures need: which salary base is used (often basic plus some allowances, not total pay), the number of days per month used to get a daily rate (for example 26 or 30; company-specific), caps on encashable days, and who is eligible.
- Also employees with high balances usually earn more than average, so an average daily salary may understate the amount; compute person by person.
- Accounting rules for how to value it (including expected future salary rises) are from memory, unverified; confirm with finance and actuaries.
- Also ask who is likely to leave, since the cash payout happens then.

**Likely follow-ups:** 1) *How reduce it?* Encourage taking leave or set carry-forward caps. 2) *Which teams?* Finance, payroll, and the auditors.
**Common mistakes:** Using total CTC as daily salary; ignoring caps; treating the estimate as the accounting number.

### Q81 ⭐⭐ 🟡 Why would an analyst look at who has not taken any leave for six months or who regularly works weekends, and what are the privacy and ethical limits of such monitoring?
**Asked at:** commonly asked (no company-specific report found); wellbeing analytics and ethics are common themes (unverified).
**What the interviewer is checking:** Can you use data to care for people without turning it into surveillance.
**Say this in the interview:** "These patterns can signal burnout risk, poor workload planning or even control or fraud risk. I would look at team-level patterns first and use them to prompt a caring conversation, not to judge individuals."
**Explain simply:**
- No leave for six months: possible burnout, leave balance building (a financial liability), or an employee who cannot be spared; in some roles, forced leave also helps detect fraud.
- Regular weekend work: overload, unclear deadlines or understaffing.
- Where to start: aggregate by team, then ask managers about workload.
- Limits: collect only what is needed for a stated purpose; tell employees what is measured and why; do not read message content or track behaviour outside work; do not use the data to punish or to guess health or family status.
- Data accuracy: logins or badge swipes do not equal work; remote or shift workers differ.
- Share individual-level lists only with the people responsible for wellbeing, with clear rules.

**Regulation / privacy note (awareness only):** Employee data is covered by data protection law, including purpose limitation and employer notice (from memory, unverified; confirm with the compliance/legal team).
**Likely follow-ups:** 1) *What action?* Manager check-in, workload review, a nudge to take leave. 2) *Opt-out?* Ask legal; at least be transparent.
**Common mistakes:** Treating long hours as high performance; building lists of individuals without purpose; hidden monitoring.

### Q82 ⭐⭐ 🟡 How would you compute the median and the mean tenure of current employees, and why can a rising average tenure mean different things?
Tenure in years of seven employees: 0.5, 1, 1.5, 2, 3, 4, 12
**Asked at:** commonly asked (no company-specific report found); tenure statistics are common HR descriptive measures (unverified).
**What the interviewer is checking:** Mean versus median, and critical reading of a trend.
**Say this in the interview:** "Sort the values; the middle one is the median, 2 years. The mean is the total divided by the count, 24 / 7 = 3.43 years. The one 12-year employee pulls the mean above the median."
**Explain simply:**
- Tenure = time from joining date to today (for current employees).
- Median is the middle value and is not moved by one extreme; the mean is.
- Rising average tenure can be good: people are staying. Or it can mean hiring has slowed, so few new joiners drag it down; or newer people are leaving fast, leaving only veterans; or a layoff targeted juniors.
- So look at the full distribution: share under 1 year, 1 to 3, over 5, plus hiring and exit counts.

**Worked example:** sum = 0.5 + 1 + 1.5 + 2 + 3 + 4 + 12 = 24.0. Median (4th of 7) = 2.0 years. Mean = 24 / 7 = 3.43 years (rounded to 2 decimals).
In Excel: `=MEDIAN(B2:B8)` and `=AVERAGE(B2:B8)`. Tenure from dates: `=(TODAY()-C2)/365.25`.
Also: average tenure of current staff differs from the average tenure of people who left; do not mix them.

**Likely follow-ups:** 1) *Which to report?* Both, with the distribution. 2) *Does a rise mean engagement improved?* Not by itself.
**Common mistakes:** Using the mean with outliers; using exited employees by mistake; not saying how rehires are counted.

### Q83 ⭐⭐ 🟡 The workforce has 1,000 employees. Compute revenue per employee and employee cost as a percentage of revenue from the data below, and say what each can mislead you about.
Revenue INR 300 crore
Total employee cost INR 120 crore
Average headcount 1,000
Contract workers (not in headcount) 200
**Asked at:** commonly asked (no company-specific report found); productivity ratios are common in workforce-planning discussions (unverified).
**What the interviewer is checking:** Unit handling (crore) and awareness of what a ratio hides.
**Say this in the interview:** "Revenue per employee is INR 30 lakh, and employee cost is 40% of revenue. But these ignore the 200 contract workers, so they flatter productivity unless contractor cost is handled consistently."
**Explain simply:**
- 1 crore = 100 lakh = 10 million rupees.
- Revenue per employee = revenue / average headcount.
- Employee cost % = total employee cost / revenue x 100.

**Worked example:**
- Revenue per employee: 300 crore / 1,000 = 0.30 crore = INR 30 lakh.
- Employee cost %: 120 / 300 = 40.0%.
- Including contract workers (1,200 people): 300 crore / 1,200 = INR 25 lakh per person, a 16.7% drop. The ratio changes, which shows the original is sensitive to who is counted.
- Whether the INR 120 crore includes contractor payments is not stated; I assume it does not. If contractor cost is outside it, the true labour cost share is higher than 40%.
- Cost per employee: 120 crore / 1,000 = INR 12 lakh.
- What each misleads: revenue per employee is affected by price, product mix and outsourcing, not just effort; a business with machines or trading margins looks very different. Employee cost % ignores margin, and falls if prices rise even when nothing improves. Compare with the same company over time or similar firms.

**Likely follow-ups:** 1) *Better measure?* Profit or gross margin per FTE (full-time equivalent). 2) *Why average headcount?* Year-end headcount can be unrepresentative.
**Common mistakes:** Mixing crore and lakh; using year-end instead of average headcount; omitting contractors silently.

### Q84 ⭐⭐ 🟡 What is the retention rate of women returning from maternity leave (for example, still employed 12 months after return), how would you compute it from leave and exit data, and what would you do about small numbers?
**Asked at:** commonly asked (no company-specific report found); this is a common inclusion and diversity metric (unverified).
**What the interviewer is checking:** Proper cohort definition (only people who could have reached 12 months) and care with small groups.
**Say this in the interview:** "Among women who returned from maternity leave and have had at least 12 months since return, what share were still employed 12 months after returning. I would pool several years if the numbers are small and show counts."
**Explain simply:**
- Define the group (cohort): women whose leave ended and who returned to work.
- Only include those whose 12-month mark has passed by the report date; otherwise recent returners look falsely loyal.
- Retained = no exit date, or exit after return date + 12 months.
- Compare with a similar group (women who did not take leave or all employees of similar age and grade).
- Small numbers: 3 of 4 is 75% but one person changes it by 25 points. Pool several years, give counts, avoid percentages for tiny groups, and do not report if a person could be identified.

**Worked example (invented sample, report date 31 Dec 2025):**
```sql
-- returners whose 12-month mark has passed, and how many were still employed then
SELECT COUNT(*) AS eligible_returners,
       SUM(CASE WHEN e.exit_date IS NULL
                  OR e.exit_date > DATE(r.return_date, '+12 months')
                THEN 1 ELSE 0 END) AS still_employed_12m
FROM maternity_returns r
LEFT JOIN exits e ON e.employee_id = r.employee_id
WHERE DATE(r.return_date, '+12 months') <= '2025-12-31';
```
Output: 5 eligible, 4 retained: 4 / 5 = 80%. One sixth returner (returned Aug 2025) is correctly left out.
A single missed person moves the rate by 20 points, so I would pool years and show "4 of 5".

**Regulation / privacy note (awareness only):** Maternity-related data is health-adjacent and sensitive; keep aggregated (from memory, unverified; confirm with the compliance/legal team).
**Likely follow-ups:** 1) *Why compare?* A rate means little without a baseline. 2) *Add reasons?* Exit interview themes, carefully.
**Common mistakes:** Including recent returners; counting those still on leave; reporting percentages of tiny groups.

### Q85 ⭐⭐ 🟡 A target is to reach 40% women in leadership by 2030. With 20 leadership positions filling per year, the current share of 25% and 100 current leaders, outline how you would test whether the target is feasible.
**Asked at:** commonly asked (no company-specific report found); representation targets are a common diversity analytics case (unverified).
**What the interviewer is checking:** Turning a goal into a simple projection with clear assumptions.
**Say this in the interview:** "I would model how many women leaders we have each year: women who leave plus women who are added. Under simple assumptions, about half of all new leadership fills would need to be women, which I would compare with the real pipeline."
**Explain simply:**
- Start: 100 leaders, 25 women. Target: 40 of 100, so 15 more women net.
- Assume leadership size stays 100, and 20 positions fill each year (replacing 20 leavers) for the 4 years 2027-2030.
- Assume women leave at the same rate as everyone (20%).
- Each year: women next year = women now x 0.8 + 20 x (share of fills that are women).

**Worked example:**
- If only 25% of fills are women, the count stays at 25.0, never improving.
- Solving for 4 years: the share of fills that are women must be about 50.4% (on average) to reach 40.
- Check: 50% gives 39.8 women (just short); 55% gives 42.7.
- Then test feasibility: how many women sit one level below leadership, how many are promotion-ready (from the talent review), and historical promotion and exit rates of women vs men. If the feeder level has only 30% women, a 50% fill share needs women to be promoted at well above their share.
- Run scenarios: best, base, worst; show which levers matter (more promotions, fewer exits of women, external hiring).

**Likely follow-ups:** 1) *Is it realistic?* Only if pipeline and retention support about half of fills; otherwise extend the date. 2) *What if leader count grows?* Rerun with growth.
**Common mistakes:** Ignoring exits; assuming leadership size is fixed without saying so; setting quotas without checking the feeder pool.

### Q86 ⭐⭐ 🟡 What is the "leaky pipeline" in DEI analysis, and which three tables would you join to see where representation drops between hiring and promotion?
**Asked at:** commonly asked (no company-specific report found); DEI dashboards are a named duty in HR data analyst job posts.
**What the interviewer is checking:** Do you understand a stage-by-stage funnel view of representation, and can you name the data needed.
**Say this in the interview:** A leaky pipeline means the share of a group, say women, shrinks at each step up, from applicants to hires to promotions to leadership. I would join the candidate table, the employee master table and the promotion history table to see which step loses the most.
**Explain simply:**
- Think of a pipe with holes: 45% of applicants may be women, but only 25% of managers. The question is where the drop happens, not just that it exists.
- Table 1: applicant tracking system (ATS) candidate table (applicants, shortlisted, offered, joined, with gender if collected). It shows the hiring steps.
- Table 2: employee master table (one row per person: employee ID, gender, grade, join date, department). It shows who is inside and at what level.
- Table 3: promotion or job-history table (employee ID, effective date, old grade, new grade). It shows who moved up. Join on employee ID, and on candidate ID to employee ID for new joiners.
- Compare the female share at each stage against the stage before it, and against the pool eligible to be promoted (people at least 1 year in grade).
**Data and tables involved:** ATS candidates, HRIS employee master, job-history. First cut: stage-wise share by gender and by grade; then by department.
**Regulation / privacy note (awareness only):** gender and similar fields are personal data, often optional. From memory, unverified; confirm with the compliance/legal team.
**Likely follow-ups:**
- How is it different from a glass ceiling? The ceiling is one blocked step; "leaky" describes drops across many steps.
- Which denominator for promotion? People eligible for promotion, not total headcount.
**Common mistakes:** Comparing shares of the whole company instead of eligible pools; ignoring that missing gender data in the ATS hides the first steps.

### Q87 ⭐⭐ 🟡 How would you compute and compare time-to-promotion by gender or by hiring source, and what bias risks exist in the comparison?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you measure a duration fairly, handle people who have not been promoted yet, and spot bias risks.
**Say this in the interview:** For each person I measure the time from joining (or the last promotion) to the next promotion, then compare the median by group. People not yet promoted must be handled as "still waiting", not dropped.
**Explain simply:**
- Time-to-promotion = promotion effective date minus the start date (join date or previous promotion date), in months.
- Use the median, since a few very slow cases distort the mean.
- Censoring: someone hired 18 months ago and not yet promoted is not "never promoted". Excluding them makes everything look faster; a survival-style view (share promoted by month 12, 24, 36) handles this.
- Compare like with like: same grade, same function, same joining year.
- Bias risks: groups differ in grade mix, tenure and function (mix effects); small groups; promotion cycles fixed once a year, so timing is bunched; career breaks such as maternity leave; performance ratings may themselves be biased, so controlling for them can hide a problem; hiring source may link with role level.
**Likely follow-ups:**
- Would you control for performance rating? Show both views; the gap is itself a finding.
- What if a group has 8 people? Do not report; combine groups or suppress.
**Common mistakes:** Dropping the not-yet-promoted; using the mean; comparing across grades; claiming discrimination from a raw gap, which only shows where to look.

### Q88 ⭐⭐ 🟡 What is intersectional analysis in DEI reporting, and why does it quickly lead to very small groups that cannot be reported safely?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand slicing by several attributes at once and the privacy cost of small cells.
**Say this in the interview:** Intersectional analysis looks at combinations, for example women in engineering at senior level, because a gap can hide inside single-attribute averages. Every extra attribute splits the data, so groups quickly drop to a handful of people who could be identified.
**Explain simply:**
- Single view: "women are 30%". Combined view: gender x grade x department x location. Gaps can appear in one cell only.
- Cell count multiplies: 2 genders x 5 grades x 8 departments x 4 locations = 320 cells. With 1,000 employees that is about 3 people per cell on average, and many cells have 0 or 1.
- Small cells are unstable (one exit swings the percentage) and risky (everyone knows who the only senior woman in a location is).
- Safe practice: set a minimum group size (a common rule is 5 or 10, set by policy), suppress or merge small cells, and avoid showing the same group in overlapping reports so values cannot be subtracted to reveal a person (differencing).
- Report fewer combinations at senior level, use multi-year pooling, or give the analysis to a restricted audience.
**Regulation / privacy note (awareness only):** from memory, unverified: sensitive attributes need extra care; confirm with the compliance/legal team.
**Likely follow-ups:**
- How to still use it? Pool years, or combine categories (grades into bands).
**Common mistakes:** Reporting 100% or 0% for a group of 2; hiding the cell but leaving the total, which lets people subtract.

### Q89 ⭐⭐ 🟡 Why is workforce age distribution a planning topic, and how would you estimate the retirement risk in a plant where 22 of 180 supervisors are within five years of retirement age?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you turn an age profile into a risk number with explicit assumptions.
**Say this in the interview:** Age shows when knowledge and skills will leave. Here 22 of 180 supervisors is 12.2%, about 4.4 per year over five years if retirements are spread evenly; I would refine with the actual retirement dates and the time needed to train a replacement.
**Explain simply:**
- Age distribution is a planning topic because retirement is predictable, unlike resignation, so you can start hiring and training early.
- Share at risk: 22 / 180 = 12.2% (rounded). Average per year: 22 / 5 = 4.4 supervisors, about 2.4% of the group a year.
- Refine: list each person with their expected retirement date (retirement age is a company policy, so use the policy); count by year; do not assume even spread.
- Adjust for people who may retire early or be extended (some firms re-employ past retirement age).
- Compare with lead time: if a new supervisor needs 18 months of training, you must start before the retirement year.
- Add other exits: normal resignations also reduce the pool, so retirement is one part of the supply forecast.
**Likely follow-ups:**
- What would you recommend? Succession list, trainee supervisors, knowledge handover.
**Common mistakes:** Treating "within five years" as "all gone next year"; ignoring that critical skills matter more than counts.

### Q90 ⭐⭐ 🟡 What is market benchmarking in compensation (salary surveys, percentiles such as P25, P50 and P75), and how would you compute an employee's position against the market median?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know what market benchmarking and percentiles are.
**Say this in the interview:** Benchmarking compares our pay for a role with what the market pays, using salary survey data; I compute each employee's pay divided by the market median (P50) to see where they sit.
**Explain simply:**
- A salary survey is a data set bought from consulting firms (or shared by peer companies) showing pay for matched roles. Matching roles properly (job family, level, location, company size) is the hard part.
- Percentile: P50 (median) means half of the market pays less; P25 means a quarter pays less; P75 means three quarters pay less. A company's policy might be "pay at P50" or "P75 for critical skills".
- Position vs median: market ratio = employee pay / market P50. A ratio of 1.00 is at median, below 1 is below.
- Use the same pay definition (fixed pay or total cash, annual) on both sides, and age the survey data to today if it is a year old (from memory, firms add a growth factor).
**Worked example:** Invented inputs: pay INR 12 lakh, P50 INR 10 lakh. 12 / 10 = 1.20, which is 20% above median.
**Likely follow-ups:**
- Compa-ratio vs market ratio? Compa-ratio uses the internal range midpoint; market ratio uses the external median.
**Common mistakes:** Matching on job title only; mixing fixed pay with total pay; ignoring location.

### Q91 ⭐⭐ 🟡 An employee is paid INR 9.6 lakh and the market median for the role is INR 11.2 lakh. Compute the market ratio and say what a compensation team would do with this for 150 employees.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you compute the ratio and think about what to do for a group.
**Say this in the interview:** Market ratio is 9.6 / 11.2 = 0.857, so this person is paid about 14.3% below the market median. For 150 employees I would calculate this for each person, then prioritise.
**Explain simply:**
- Ratio: 9.6 / 11.2 = 0.857 (85.7%, rounded to 1 decimal). Gap: INR 1.6 lakh, which is 14.3% below the median (1.6 / 11.2).
- Two ways to say it: the person is paid 85.7% of the market median, which is the same as 14.3% below it, because the gap is divided by the market figure (not by own pay).
- For 150 people: add market ratio, performance rating, tenure, critical skill flag, and compare with the pay range.
- Group them: ratio under 0.85, 0.85 to 0.95, 0.95 to 1.05, and above. Count and cost to bring each group to a target (for example to 0.90 or to the median).
- Cost to fix is the sum of (target minus current pay) for the chosen people; show finance a few scenarios.
- Sanity check the match: a low ratio may come from a wrong benchmark job.
**Likely follow-ups:**
- Would you raise everyone to median? Not automatically; prioritise high performers and critical roles.
**Common mistakes:** Dividing by own pay instead of market; treating the survey as exact.

### Q92 ⭐⭐ 🟡 How would you detect pay compression or pay inversion (a new joiner paid more than a longer-serving peer) in a salary table, and what would you recommend?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you define the two terms and write a query to find them.
**Say this in the interview:** Pay compression means pay differences between junior and senior people have shrunk; inversion means a newer person earns more than someone who joined earlier in the same role. I would compare pay against join date within the same grade and job.
**Explain simply:**
- Within each grade (and job family, location) look at pairs where the later joiner has higher pay than the earlier joiner.
- Compression: the correlation between tenure and pay is weak, or the gap between the new-joiner pay and the 5-year employee pay is small.
- Check performance: if the earlier employee is a stronger performer, the inversion is more serious.
- Recommend: review the affected people and fix the biggest gaps in the next increment cycle or off-cycle, and review hiring pay rules (offer above range needs approval).

```sql
-- pairs in the same grade where the later joiner earns more
select a.grade, a.emp_id as senior_id, a.salary_lakh as senior_pay,
       b.emp_id as newer_id, b.salary_lakh as newer_pay
from emp a join emp b
  on a.grade = b.grade
 and b.join_date > a.join_date
 and b.salary_lakh > a.salary_lakh;
```
On a small invented table of 6 employees (grade G5: employee 1 joined 2018 on 9.0 lakh, employee 2 joined 2021 on 9.8, employee 4 joined 2023 on 10.4, employee 3 joined 2025 on 11.2; grade G4: two employees, the later joiner paid more) this returned 7 pairs, for example grade G5 employee 1 (joined 2018, 9.0 lakh) against employee 3 (joined 2025, 11.2 lakh). It says: in G5 the 2025 joiner out-earns all three earlier joiners.
**Likely follow-ups:**
- Is every inversion wrong? No; a scarce skill may justify it, but it should be documented.
**Common mistakes:** Comparing across grades; ignoring part-year or part-time pay.

### Q93 ⭐⭐ 🟡 A salesperson has an annual variable target of INR 6 lakh with this payout curve: below 80% achievement pays zero, 80 to 100% pays pro rata, and above 100% pays 1.5 times for the excess. Compute the payout at 70%, 90% and 120% achievement.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you follow a piecewise payout rule and state the assumption on "pro rata".
**Say this in the interview:** At 70% the payout is zero; at 90% it is INR 5.4 lakh; at 120% it is INR 7.8 lakh. I assumed "pro rata" means payout equals achievement times target.
**Explain simply:**
- Target (the payout at 100% achievement): INR 6 lakh. Variable pay is the part of pay that depends on results.
- 70%: below the 80% threshold, so 0.
- 90%: 0.90 x 6 = 5.4 lakh.
- 120%: 6 + 1.5 x (0.20 x 6) = 6 + 1.8 = 7.8 lakh. The "excess" is the 20% above target (1.2 lakh), paid at 1.5 times.
- Jump at the threshold: 79.9% pays 0 but 80% pays 4.8 lakh (0.8 x 6). Interviewers like this; it is a cliff that may push behaviour.
- Rounded to the nearest 0.1 lakh; if the plan means a different pro-rata scale (for example, payout starts from 0 at 80%), the answer at 90% changes, so check the plan document.
**Likely follow-ups:**
- Is there a cap? Not stated; ask, as caps change cost forecasts.
**Common mistakes:** Paying 1.5 times on the whole target instead of only the excess above 100%; forgetting the zero below the threshold; not noticing the cliff at 80%.

### Q94 ⭐⭐ 🟡 Increments of 10% take effect on 1 July for a company with a financial year from April to March. What are the costs in the current financial year and in the next financial year per INR 100 of current salary?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you split a mid-year change across financial years.
**Say this in the interview:** Per INR 100 of current annual salary, this financial year costs 107.5 and the next costs 110. The increment's full effect shows up only in the next year.
**Explain simply:**
- Financial year April to March: April, May, June (3 months) at the old pay; July to March (9 months) at the new pay.
- Current FY: 100 x 3/12 + 110 x 9/12 = 25 + 82.5 = 107.5.
- Next FY (assuming no new increment in it): 110, a full year.
- The in-year cost of the 10% increment is 7.5 (the 10 x 9/12), not 10; the other 2.5 lands in next year as the "carry-over" or annualisation effect.
- Budgets must therefore show both: a 10% increment raises this year's cost by 7.5% and next year's by a further 2.3% (110 / 107.5, rounded).
- Assumes salary only; bonus and PF linked to pay rise with it.
**Likely follow-ups:**
- What if increments are delayed to October? In-year cost falls (6 months at new pay), and the carry-over grows.
**Common mistakes:** Budgeting a full 10% in year one; forgetting carry-over; using calendar year rather than the company's financial year.

### Q95 ⭐⭐ 🟡 ESOPs vest over four years with a one-year cliff (25% at the end of year one, then monthly). Compute the vested percentage for someone who has served 30 months and say what the cliff means for attrition analysis.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you compute vesting and link cliffs to attrition.
**Say this in the interview:** At 30 months the vested share is 62.5%. The cliff means nothing vests before 12 months, so exits just before and just after it carry different value for the employee.
**Explain simply:**
- ESOP (employee stock option plan) gives the right to buy shares later at a fixed price; vesting is the schedule by which you earn that right.
- Months 1 to 11: 0%. Month 12: 25% (the cliff). Then the other 75% vests monthly over the next 36 months: 75 / 36 = 2.083% per month.
- At 30 months, 18 months after the cliff: 25 + 18 x 2.083 = 62.5%. Check: 30 / 48 = 62.5%.
- Attrition read: leaving before month 12 forfeits everything, so resignations bunch just after month 12; an extra bump near the 48-month end is common once everything is vested. Do not assume these patterns are real; check your own data.
- Look at exits by tenure month, split by employees with and without ESOP grants.
- Plan terms differ (from memory, plans vary), so use the actual plan document.
**Likely follow-ups:**
- Vested versus exercised? Vested means earned; exercised means bought.
**Common mistakes:** Forgetting the cliff jump; assuming vesting is linear from month 1 (it gives the same 62.5% at 30 months but wrong values before month 12).

### Q96 ⭐⭐ 🟡 What would you check in a salary table to find outliers or data entry errors before a compensation analysis (zero or negative pay, ten-times jumps, monthly versus annual mix-ups)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you validate data before analysing.
**Say this in the interview:** I check ranges, jumps, units, duplicates and consistency with grade bands before any compensation analysis.
**Explain simply:**
- Zero, negative or blank pay (can be real for unpaid leave, but not for fixed pay).
- Minimum and maximum by grade; flag values outside the pay band by a large margin.
- Jumps: month-on-month change above a threshold (for example 2x or 10x) points to a typo or extra zero.
- Monthly versus annual mix-up: a monthly 80,000 stored next to annual 9,60,000. Look at the ratio to the grade median; values near 1/12 or 12 times are suspects.
- Currency and unit mix (INR versus lakh versus crore, or other countries).
- Duplicate employee-month rows; salary for people with exit dates before the pay month; pay for people not in the master.
- Part-month or part-time pay (not full-time equivalent).
- Fix at source with HR operations; document what was excluded.
**Likely follow-ups:**
- Remove outliers? Only after confirming they are errors; true high earners are not errors.
**Common mistakes:** Deleting outliers silently; trusting a currency column that is blank.

### Q97 ⭐⭐ 🟡 What is the difference between cost to company and cost to the employer (employer PF, gratuity, insurance, bonus), and which is right for budgeting?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the two cost views and which one to use.
**Say this in the interview:** Cost to company (CTC) is what the employee is promised; cost to the employer is the full amount the company spends, which adds items outside CTC. For budgeting I use the full employer cost.
**Explain simply:**
- CTC: the annual package, usually fixed pay, employer PF (provident fund contribution), and some benefits inside the offer letter.
- Cost to employer adds items that may sit outside CTC: statutory bonus, gratuity provision, insurance premium, recruitment and training, and other overheads such as laptop and seat; what is inside CTC differs by company.
- Budgeting needs all the spend, because finance records the full cost. Employee communication uses CTC.
- Be clear which one a report uses; the same person may show INR 12 lakh in HR and INR 13.4 lakh in finance with both being right.
**Likely follow-ups:**
- Which cost for a make-or-buy against contractors? Full employer cost.
**Common mistakes:** Comparing HR CTC with a finance employee-cost line without a bridge.

### Q98 ⭐⭐ 🟡 An employee joined on 11 November and the contractual monthly gross is INR 60,000. Compute the pro-rated salary for November (30 days) on a calendar-day basis and on a fixed 26-working-day basis, and say what could differ.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you do pro-rata pay under two day-count rules.
**Say this in the interview:** Calendar-day basis gives INR 40,000; the fixed 26-day basis gives about INR 39,231 if the employee has 17 paid working days.
**Explain simply:**
- Joined 11 November, so the days from 11 to 30 inclusive are 20 days.
- Calendar basis: 60,000 x 20 / 30 = 40,000.
- 26-day basis: daily rate = 60,000 / 26 = 2,307.69. Working days from 11 to 30 November (Monday to Saturday, Sunday off), counting the 2026 calendar, are 17. Pay: 17 x 2,307.69 = 39,230.77 (rounded to paise).
- Difference: INR 769.23 (calendar basis pays more here).
- What can differ: which weekly off applies (5-day week gives a different count), public holidays being paid or not, whether the 26 days exclude holidays, the year (the count depends on the weekday), rounding rules, and how the company handles loss of pay when the employee works part of a month. The policy document decides.
**Likely follow-ups:**
- Which is common? Both exist; calendar-day basis is simpler (from memory, varies by company).
**Common mistakes:** Counting 20 working days; forgetting to include the joining day; using 30 as a fixed divisor in a 31-day month without saying so.

### Q99 ⭐⭐ 🟡 What are loss-of-pay days, arrears and full-and-final settlement, and what data errors typically cause an arrears payment?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know three payroll terms and where errors originate.
**Say this in the interview:** Loss of pay (LOP) days are unpaid absence days deducted from salary; arrears are amounts owed from earlier months paid later; full-and-final settlement (FNF) is the last payment when someone leaves.
**Explain simply:**
- LOP: leave without pay or unapproved absence, deducted at the daily rate.
- Arrears: for example an increment effective 1 April but processed in June, so two months of difference is paid in June.
- FNF: pending salary, leave encashment, bonus, less notice shortfall and dues, typically processed after the last working day.
- Common data errors behind arrears: increment or promotion entered late (effective-dated change entered after payroll cut-off), wrong joining date, attendance or leave corrected after payroll closed, wrong grade or allowance, missing transfer, wrong tax or PF details.
- Analyst use: count arrears per month and by cause; high counts show a process delay.
**Likely follow-ups:**
- How to reduce them? Earlier data cut-offs and entry checks.
**Common mistakes:** Treating arrears as extra cost; they are cost already owed, reported in the wrong month.

### Q100 ⭐⭐ 🟡 How are contract or third-party workers' costs and hours usually tracked compared with employees, and why does this make "total workforce" reporting hard?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you see why contingent workforce data is fragmented.
**Say this in the interview:** Employees sit in the HRIS and payroll; contract and agency workers are usually tracked through vendor invoices and purchase orders, so cost and hours live in finance or procurement systems, not HR.
**Explain simply:**
- Employee: salary, attendance and leave in HRIS and payroll.
- Third-party staff are paid by the agency; the company sees an invoice, often a lump sum per month or per head, not a salary.
- Hours may come from vendor timesheets, gate or badge records, or a vendor management system (VMS), if one exists. Names and IDs differ from employee IDs.
- Costs are booked in finance as services, not salary, so they miss "employee cost".
- So "total workforce" needs a rule on who counts, a common ID or worker table, matching of vendor invoices to heads, and a definition of cost (invoice versus rate).
- Result: totals differ between HR, finance and operations unless one owner defines the rule.
**Likely follow-ups:**
- First step? A single worker-type field and a list of vendors with head counts.
**Common mistakes:** Adding employee cost and contractor invoices without checking overlaps; counting agency staff in headcount without writing the rule.

### Q101 ⭐⭐ 🟡 How is data typically handed over from the applicant tracking system to the HRIS when a candidate joins, and what mismatches (names, dates, grades, cost centres) can appear?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you understand the ATS-to-HRIS handoff and its failure points.
**Say this in the interview:** When a candidate joins, a record is created in the HRIS either by an integration (the ATS pushes accepted-offer data) or manually by HR operations from the offer letter; mismatches arise because the two systems hold the same facts separately.
**Explain simply:**
- Typical data passed: name, date of birth, contact, offered grade and designation, joining date, department, cost centre, manager, salary.
- Name mismatch: resume says "Rahul K.", ID proof says "Rahul Kumar"; spelling and order differ.
- Date mismatch: offered joining date versus actual joining date; the date of birth different from the ID proof.
- Grade or designation mismatch: offer letter changed late, ATS has the old value.
- Cost centre mismatch: requisition cost centre differs from the department that actually hires; or has been closed.
- Candidate ID versus employee ID: keep a cross-reference column so analysts can trace hire source to later performance.
- Checks: compare the ATS accepted-offer list with HRIS new joiners by month; list unmatched.
**Likely follow-ups:**
- Who owns the correction? Usually HR operations with the recruiter.
**Common mistakes:** Joining by name; no stored candidate-to-employee key.

### Q102 ⭐⭐ 🟡 How would you build a monthly headcount snapshot table from effective-dated employee records, and what are the benefits of keeping snapshots rather than recomputing from transactions?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you use effective-dated records to rebuild a past date and justify snapshots.
**Say this in the interview:** I keep a table of month-end dates and join it to the effective-dated employee history, so each person appears in a month if the month-end falls within their effective period and status is active.
**Explain simply:**
- Effective-dated records have effective-from and effective-to dates per version (see Q7); the open row ends at 9999-12-31.
- Build: month-end calendar table, join on date between from and to, filter to active, group by the attributes (department, grade).
- Save the result as a snapshot table, with one row per employee per month, instead of recomputing.

```sql
-- headcount at each month end, by department
select m.snapshot_date, h.dept, count(*) as headcount
from month_ends m
join emp_history h
  on m.snapshot_date between h.effective_from and h.effective_to
where h.status = 'Active'
group by m.snapshot_date, h.dept
order by m.snapshot_date, h.dept;
```
On invented data (3 people), the output was: 31 Jan Sales 2, Ops 1; 29 Feb Sales 1, Ops 2; 31 Mar Sales 1, Ops 1. It says: employee 2 moved from Sales to Ops on 15 February, and employee 3 was terminated on 10 March, so was missing in March.
- Why keep snapshots: the reports never change when later corrections arrive (or, if they change, you know why), faster dashboards, audit evidence of what was reported (see Q150), history of department names and managers as they were, and simple trend charts.
- Cost: storage and a rule for restating when late corrections are made.
**Likely follow-ups:**
- Late-entered change? Re-run the affected month, log the restatement.
**Common mistakes:** Using today's department for past months; using a join on exact date equality; losing leavers in the table.

### Q103 ⭐⭐ 🟡 The HR dashboard shows 1,014 headcount and the finance report shows 1,036. How would you trace the difference and who should own the final definition?
**Asked at:** commonly asked (no company-specific report found); HR-versus-finance headcount reconciliation is a theme in prep-site people-analytics guides (unverified).
**What the interviewer is checking:** Whether you reconcile methodically (same date, same population, same definition) instead of declaring one number "wrong".
**Say this in the interview:** "A gap of 22 is usually a definition or timing difference, not an error. I would line both reports up on the same date and the same population, list the people in one but not the other, and group them by reason. The final definition should be owned jointly: HR owns who is an employee, finance owns what is paid, and a named business owner signs off."
**Explain simply:**
- **Headcount** means the number of people on the books on a given date. Each report may count a slightly different group.
- Check in this order: (1) **cut-off date**: month-end 31st versus the 30th, or data refreshed on different days; (2) **population**: are contractors, interns, trainees, consultants, part-timers or people on long leave in or out; (3) **status timing**: someone who resigned but is serving notice, or who left on the 31st but is still in payroll for that month; (4) **duplicates and rehires**: one person with two records; (5) **entity or cost-centre mapping**: a unit that sits in one company code in finance and another in HR.
- Method: export the employee ID lists from both, do a full outer join on ID, and tag each mismatch with a reason.
**Worked example:** Illustrative gap of 1,036 - 1,014 = 22 people. A possible breakdown (invented): finance includes 12 contract staff paid through payroll (+12); 8 people exited on the last day but finance still paid them that month (+8); 4 joiners are in finance but the HR joining date falls next month (+4); 2 duplicate rehire records inflate the HR figure (-2). Total: 12 + 8 + 4 - 2 = 22, so the gap is fully explained.
**Likely follow-ups:** 1) *Which number is right?* Both can be right for their purpose; publish both with definitions, then agree one "official headcount". 2) *How do you stop it recurring?* A written metric definition, one shared snapshot table and a month-end freeze date.
**Common mistakes:** Picking the number you like; reconciling totals without comparing ID lists; ignoring the cut-off date.

### Q104 ⭐⭐ 🟡 What is the difference between a dimension and a measure in an HR data model (for example, department, grade, location versus headcount, tenure, salary), and which dimensions are always needed for a headcount report?
**Asked at:** commonly asked (no company-specific report found); data-modelling basics appear in HRIS and BI analyst question lists (unverified).
**What the interviewer is checking:** That you understand how a report is built: labels you slice by versus numbers you add up.
**Say this in the interview:** "Dimensions are the descriptive columns I group or filter by, such as department, grade and location. Measures are the numbers I calculate, such as headcount, average tenure or total salary. A headcount report always needs a date, a department or org unit, a location and an employment type or status."
**Explain simply:**
- **Dimension:** a category that describes a person or a row. Think of the row and column headings of a pivot table.
- **Measure:** a number you aggregate (count, sum, average) in the body of the pivot. Headcount is a count of employee IDs; tenure is usually averaged; salary is summed or averaged.
- Not every number is a measure: grade 7 is a label (a dimension) even though it looks like a number. Ask: "does it make sense to add it up?"
- Always needed for headcount: **snapshot date** (headcount is meaningless without "as on"), **organisation unit** (department or cost centre), **location**, **employment type** (permanent, contract, intern), **worker status** (active, on leave, notice period). Grade or band, gender and manager are common additions.
**Likely follow-ups:** 1) *Can tenure be a dimension?* Yes, if banded (0-1, 1-3, 3+ years); the band is the dimension, average tenure is the measure. 2) *Why add up headcount carefully?* A count of rows can double-count people with several records; count distinct employee IDs.
**Common mistakes:** Averaging an average across groups; treating a coded label as a number; reporting headcount without a date.

### Q105 ⭐⭐ 🟡 What does it mean that a person has multiple records (concurrent employment, contract then permanent, rehire), and how do you pick one row per person without losing history?
**Asked at:** commonly asked (no company-specific report found); data-quality and duplicate handling is a standard HRIS analyst theme (unverified).
**What the interviewer is checking:** Whether you know that one person is not always one row, and can choose the right grain for the question.
**Say this in the interview:** "In HR systems a person can have several employment records. For a current headcount I take one row per person using the latest or primary record, but I keep the full history table for tenure, movement and attrition questions."
**Explain simply:**
- **Concurrent employment:** a person holds two jobs inside the same company at once (for example a full-time role plus a part-time teaching role). Two active rows, one human.
- **Contract then permanent:** the contractor's record ends and a permanent one starts. Tenure may need both records joined.
- **Rehire:** someone leaves and returns later. Depending on the system they get a new record or a new ID, which can inflate counts and break tenure.
- **Rule:** keep a history table (all records) and derive a "current" view with one row per person, defined by a clear rule (latest start date, or the record flagged primary).
**Worked example:** The sample table below (invented) has 3 people and 6 records. The query keeps the most recent record per person.
```sql
-- Rank each person's records from newest to oldest
SELECT employee_id, employment_type, start_date
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY employee_id
                              ORDER BY start_date DESC) AS recency_rank
    FROM employment_records
)
WHERE recency_rank = 1;   -- keep only the newest record
```
Output: E101 Permanent 2022-04-01; E102 Permanent 2024-02-01; E103 Part-time 2023-05-01. Three rows for three people, and `employment_records` still holds all six rows for history. Note E103 shows only the part-time record, which is why "primary record" rules must be agreed (here E103 has two open records, so the rule matters).
**Likely follow-ups:** 1) *How do you calculate tenure for a rehire?* Agree a policy: continuous service from the latest start, or total of all stints; state it. 2) *What if the rehire has a new ID?* Match on a stable attribute under HR guidance, such as a national ID held securely, and flag for HR to confirm.
**Common mistakes:** Deleting older rows; counting rows instead of distinct people; no written rule for "primary".

### Q106 ⭐⭐ 🟡 What is a position-based versus a person-based HR model, and why does vacancy reporting need positions?
**Asked at:** commonly asked (no company-specific report found); position management appears in HRIS tool discussions such as Workday and SAP (unverified).
**What the interviewer is checking:** Whether you understand that a seat and the person sitting in it are two different things.
**Say this in the interview:** "In a person-based model the system tracks employees and their jobs. In a position-based model the company first creates positions, the approved seats, and then fills them with people. Vacancies are positions with nobody in them, so you cannot report vacancies without a position list."
**Explain simply:**
- **Person-based:** a row exists only when someone is hired. Simple, but an empty seat leaves no trace in the data.
- **Position-based:** each approved role has a position ID, a department, a grade and a budget. A person is assigned to it, or it stays open. Vacancy = approved positions - filled positions.
- Position models also support budgeted headcount, hiring approvals and "who replaced whom". The cost is more admin: someone must keep positions current.
- Example: a department has 20 approved positions and 17 employees. Only a position list shows that 3 are vacant and which ones.
**Likely follow-ups:** 1) *What if the company has no position data?* Start from the approved headcount budget in finance and compare to actuals by department. 2) *Is a vacancy the same as an open requisition?* No, a requisition is a hiring request; a position can be vacant with no requisition raised yet.
**Common mistakes:** Treating "budgeted headcount" and "positions" as the same without checking; computing vacancies by subtracting two unreconciled totals.

### Q107 ⭐⭐ 🟡 A plant has 5% budgeted absenteeism but actual is 7.5% in the night shift and 4% in the day shift. How would you slice the data to find what is happening, and why would you be careful about naming individuals?
**Asked at:** commonly asked (no company-specific report found); absenteeism analysis is a common scenario in HR analytics guides (unverified).
**What the interviewer is checking:** Structured slicing, awareness of the weighted overall number, and sensitivity about individuals.
**Say this in the interview:** "I would first check the overall rate against budget, then slice by shift, line, supervisor, day of week, leave type and tenure to see where the extra absence sits. I would report groups, not names, because absence often links to health or family reasons and small groups make people identifiable."
**Explain simply:**
- **Absenteeism rate** (definition I use): absent days divided by scheduled working days, as a percentage. Companies differ on whether planned leave counts.
- Slices: shift, line or section, supervisor, day of week (Mondays, days after payday or festivals), month, leave type (sick, unplanned, casual), tenure band, commute distance if available.
- Look for the pattern, not the person: is night shift high on specific lines or only with one supervisor? Is it concentrated on Fridays and Mondays? Is it a few long sick spells or many one-day absences?
- Caution: a handful of people with long illness can drive the rate; sickness data is sensitive health-related information. Names invite blame and can breach confidentiality.
**Worked example:** Suppose (invented) 60% of scheduled days are day shift and 40% night. Blended rate = 0.6 x 4% + 0.4 x 7.5% = 5.4%, against budget 5%, so the plant is 0.4 percentage points over. Night shift is 2.5 percentage points over budget; day shift is 1 point under. If 40 night workers are scheduled 26 days each (1,040 days), 7.5% means 78 absent days against 52 at budget.
**Regulation / privacy note (awareness only):** Health-related leave data is usually treated as sensitive. From memory, unverified: confirm handling rules with the compliance or legal team.
**Likely follow-ups:** 1) *What if the sample is tiny?* Combine lines or months before reporting. 2) *What action follows?* Share findings with HR and plant management for root causes (transport, fatigue, rosters), not discipline of named people.
**Common mistakes:** Comparing percentages without the shift's size; quoting 5.4% minus 5% as "0.4%" instead of percentage points; naming individuals in a dashboard.

### Q108 ⭐⭐ 🟡 What is workforce supply forecasting using an internal movement (transition) matrix of promotions, lateral moves and exits, and how would you build a simple one from two years of data?
**Asked at:** commonly asked (no company-specific report found); workforce planning appears in people-analytics guides (unverified).
**What the interviewer is checking:** Whether you can turn history into probabilities and project the current workforce forward.
**Say this in the interview:** "A movement matrix shows, for each level, what share of people stayed, were promoted, moved sideways or left in a year. I count the movements over the past two years, divide by the starting headcount of each level, and apply those rates to today's headcount to forecast next year's supply."
**Explain simply:**
- **Transition matrix:** rows are where people start, columns where they end (including "Exit"). Each row adds to 100%.
- Build: take snapshots at the start and end of each year; link people by ID; count each from-to pair; pool the two years for stable rates; divide each count by its row total.
- Forecast = current headcount per level x the matrix, plus planned hires. It tells you the **internal supply**; the gap to demand is what must be hired.
- Limits: assumes the past repeats; small levels give shaky rates; ignores a changing market.
**Worked example:** Pooled movements (invented counts) from a table of from-state, to-state, count:
```python
# Pooled two-year counts: people who started a year at each level, and where they ended
rows = [("L1","L1",60), ("L1","L2",9), ("L1","L3",1), ("L1","Exit",10),
        ("L2","L1",1),  ("L2","L2",30), ("L2","L3",3), ("L2","Exit",4),
        ("L3","L2",1),  ("L3","L3",16), ("L3","Exit",3)]
movements = pd.DataFrame(rows, columns=["from", "to", "n"])
counts = movements.pivot_table(index="from", columns="to",
                               values="n", aggfunc="sum", fill_value=0)
# Divide each row by its total to get the share of people
rates = counts.div(counts.sum(axis=1), axis=0).round(3)
```
Output (rates, each row sums to 1): L1 stays 0.750, to L2 0.112, to L3 0.012, exits 0.125; L2 stays 0.789, to L3 0.079, down to L1 0.026, exits 0.105; L3 stays 0.800, to L2 0.050, exits 0.150. With today's headcount of 800, 380 and 100 (1,280 total), about 1,125 remain after a year (155 exits, exact before rounding), landing at roughly 610 in L1, 395 in L2 and 120 in L3 (using the unrounded rates). Planned hires must cover the rest.
**Likely follow-ups:** 1) *Why pool two years?* More data per cell, less noise. 2) *What about a big restructure in year one?* Weight recent data more or exclude the unusual year.
**Common mistakes:** Dividing by end headcount instead of start; ignoring exits in the matrix; treating rates as promises.

### Q109 ⭐⭐ 🟡 How would you compute bench strength for succession planning (ready-now and ready-in-one-to-two-years successors per critical role), and which data would you need?
**Asked at:** commonly asked (no company-specific report found); succession and talent-pipeline reporting is a talent-analytics theme (unverified).
**What the interviewer is checking:** That you can define the measure, join the right tables and highlight risky roles.
**Say this in the interview:** "Bench strength per critical role is the number of named successors who are ready now and who will be ready in one to two years. I need the list of critical roles, a successor table with readiness ratings from talent reviews, and performance and potential data to support them. Roles with no ready-now successor are the risk."
**Explain simply:**
- **Critical role:** a position where a vacancy would seriously hurt the business, chosen by leadership.
- **Successor:** an employee nominated as a possible replacement; **readiness** is a rating from talent review meetings (ready now, 1-2 years, 3+ years).
- Data needed: critical roles list, successor nominations with readiness and date reviewed, current roles, performance ratings, potential ratings, retention-risk indicators, incumbent retirement or exit dates.
- Start from the critical roles list so roles with zero successors still appear (use a left join).
**Worked example:** Five critical roles, six nominations rated ready now or in 1 to 2 years (invented):
```sql
-- Count successors by readiness; LEFT JOIN keeps roles with no successors
SELECT r.critical_role,
       SUM(CASE WHEN s.readiness = 'Ready now' THEN 1 ELSE 0 END)  AS ready_now,
       SUM(CASE WHEN s.readiness = '1-2 years' THEN 1 ELSE 0 END)  AS ready_in_1_to_2_years
FROM critical_roles r
LEFT JOIN successors s ON s.critical_role = r.critical_role
GROUP BY r.critical_role
ORDER BY ready_now;
```
Output: HR Head 0 and 1; IT Head 0 and 0; Sales Head 0 and 0; Plant Head 1 and 2; Finance Controller 2 and 0. Three of five roles (60%) have no ready-now successor, and two have no successor at all.
**Regulation / privacy note (awareness only):** Readiness ratings are sensitive and often confidential. From memory, unverified: restrict access and confirm with the HR and legal teams.
**Likely follow-ups:** 1) *Is 2 ready successors better than 1?* Usually, but check they are not the same person on several lists. 2) *How fresh must ratings be?* Typically refreshed at each annual talent review.
**Common mistakes:** Inner join that hides roles with no successor; counting one person across many roles as separate strength.

### Q110 ⭐⭐ 🟡 What are skills inventories and skills gap analysis, and which data (certifications, learning records, project history) would you use for a first version?
**Asked at:** commonly asked (no company-specific report found); skills analytics is a growing people-analytics topic (unverified).
**What the interviewer is checking:** Whether you can start practical and honest about data quality, not promise a perfect skills map.
**Say this in the interview:** "A skills inventory is a list of who has which skills and at what level. A gap analysis compares it with the skills the business needs. For a first version I would use data that already exists: certifications, completed training and project history, accepting that it is incomplete."
**Explain simply:**
- **Skills inventory:** one row per person per skill, with a level and a source (for example "SQL, intermediate, from certification").
- **Demand side:** skills required by roles or planned projects, from job descriptions or business plans.
- **Gap** = required level or count minus available. Example: 10 people needed with cloud skills, 6 available, gap of 4.
- Sources and their weakness: certifications (clear but expire), learning records (shows exposure, not mastery), project history (shows use, but tagging is inconsistent), manager ratings (subjective), self-declared skills (often outdated).
- First version: pick 10 to 15 critical skills, map them from the three sources, and validate with managers.
**Likely follow-ups:** 1) *How do you handle different names for one skill?* Build a standard skills list and a mapping table. 2) *Self-ratings?* Use with caution and cross-check.
**Common mistakes:** Starting with hundreds of skills; treating course completion as proof of skill; letting the inventory go stale.

### Q111 ⭐⭐ 🟡 What is the difference between descriptive, diagnostic, predictive and prescriptive people analytics, and which stage would most HR teams in India be at today?
**Asked at:** commonly asked (no company-specific report found); the four-stage framing is a common prep-site question (unverified).
**What the interviewer is checking:** Vocabulary and a realistic view of maturity, not hype.
**Say this in the interview:** "Descriptive says what happened, diagnostic says why, predictive says what is likely next, and prescriptive says what to do about it. My impression, unverified, is that many HR teams are still mostly descriptive with some diagnostic work, but I would not claim a precise figure."
**Explain simply:**
- **Descriptive:** attrition was 14% last year, headcount by department.
- **Diagnostic:** attrition was highest in first-year employees under one manager group; here are the drivers.
- **Predictive:** a model estimates which groups are likely to leave next quarter.
- **Prescriptive:** recommends actions, for example which retention levers to try and the expected impact.
- Each stage needs cleaner data and more trust. A team with weak data definitions should fix descriptive reporting first.
- The India maturity view is a judgement, not a measured fact: no statistic here is verified. Say you would assess a team by asking what decisions its reports currently support.
**Likely follow-ups:** 1) *Is predictive always better?* No, a clear descriptive dashboard often adds more value. 2) *First step up?* Add diagnostic cuts to existing reports.
**Common mistakes:** Jumping to machine learning on messy data; quoting a made-up maturity percentage.

### Q112 ⭐⭐ 🟡 How would you compare the quality of hires from campus, referral, agency and job portal sources using first-year performance, retention and ramp-up time?
**Asked at:** commonly asked (no company-specific report found); source-of-hire quality is a recruitment-analytics theme (unverified).
**What the interviewer is checking:** Whether you compare fairly with several measures and notice small samples and role mix.
**Say this in the interview:** "I would build one table per hire with source, hire date, first-year rating, still-employed flag at 12 months and days to full productivity, then compare sources on each measure, keeping role and level comparable. I would also look at volume and cost, not only quality."
**Explain simply:**
- **First-year performance:** rating after the first review cycle (ratings are subjective; use consistent scales).
- **12-month retention:** hires still employed 12 months after joining, divided by hires, only for hires who have had 12 months.
- **Ramp-up time:** days until a new hire meets a defined productivity standard; the definition varies by role.
- Compare like with like: campus hires are entry level, referrals may be experienced, so compare within level or role family.
**Worked example:** Invented hires data:
Campus: 80 hires, 60 retained, 75.0% retention, avg rating 3.1, ramp 110 days. Referral: 50 hires, 44 retained, 88.0%, rating 3.6, ramp 60 days. Agency: 40 hires, 28 retained, 70.0%, rating 3.4, ramp 70 days. Job portal: 130 hires, 91 retained, 70.0%, rating 3.2, ramp 85 days. Retention = retained / hires x 100, rounded to 1 decimal. Referral looks best on all three, yet only 50 hires; campus is slower to ramp, which is expected for entry-level staff.
**Likely follow-ups:** 1) *Is the difference real?* With small groups, show counts and avoid strong claims. 2) *What else?* Cost per hire and time to hire by source.
**Common mistakes:** Mixing levels; including hires with under 12 months of tenure in retention; ranking on one measure.

### Q113 ⭐⭐ 🟡 What anonymisation methods (removing names, pseudonymising employee IDs, banding salaries, grouping small cells) would you apply before sharing an HR dataset with an external survey or benchmarking vendor?
**Asked at:** commonly asked (no company-specific report found); data-sharing and anonymisation is a privacy theme in people-analytics guides (unverified).
**What the interviewer is checking:** Layered thinking and awareness that removing names is not enough.
**Say this in the interview:** "I would share only the columns the vendor needs, remove direct identifiers, replace IDs with random codes, band numbers like salary and age, and suppress small groups. Then I would check whether anyone could still be recognised by combining columns, and get legal and HR sign-off."
**Explain simply:**
- **Data minimisation:** drop every column not needed for the purpose.
- **Remove direct identifiers:** name, phone, email, national ID.
- **Pseudonymise:** replace the employee ID with a random code; keep the lookup key with the company only. This is reversible by the key holder, so the data is still personal data.
- **Banding:** salary 11.3 lakh becomes "10-15 lakh"; age becomes 30-34.
- **Group small cells:** if a department-grade-gender group has fewer than a minimum count (for example 5, a threshold your policy sets), merge or hide it.
- **Check re-identification:** a unique combination such as rare job title plus location plus joining month can identify someone.
- **Contract:** vendor agreement covering purpose, security and deletion.
**Likely follow-ups:** 1) *Anonymised or pseudonymised?* Pseudonymised can be linked back; truly anonymised cannot. 2) *Who approves?* Data owner, privacy or legal, and HR leadership.
**Common mistakes:** Only deleting the name column; keeping exact dates of birth; forgetting small cells.

### Q114 ⭐⭐ 🟡 How would you set up row-level security so that each HR business partner sees only their own business unit's employee data in the dashboard, and what could still leak?
**Asked at:** commonly asked (no company-specific report found); row-level security is a standard BI topic (unverified).
**What the interviewer is checking:** Practical BI setup plus awareness of side channels.
**Say this in the interview:** "I would keep a mapping table of user to business unit and create a security rule that filters the data to the logged-in user's unit. Then I would test with a few users and check for leaks such as totals, exports and cross-unit comparisons."
**Explain simply:**
- **Row-level security (RLS):** the same report shows different rows to different users based on who they are.
- Setup: a table with columns user email and business unit; a rule that filters the employee table where business unit matches the user's entry (in Power BI this is a role with a filter; the exact steps depend on your tool). Assign users to the role in the service.
- Test using the "view as role" option and a second person.
- Keep the mapping maintained: when a partner changes unit, access must change too.
- **Possible leaks:** company-wide totals or averages that reveal other units; exports and screenshots; users with edit rights who bypass the role; data refreshed to an unsecured file; small-unit numbers that identify people; names in tooltips; an admin dataset shared separately.
**Likely follow-ups:** 1) *Who manages the mapping?* HR systems team, with periodic access reviews. 2) *Can partners see company totals?* Only if policy allows, via a separate aggregated page.
**Common mistakes:** Testing only as the admin; forgetting leavers and movers; securing the report but not the dataset.

### Q115 ⭐⭐ 🟡 An employee asks the company to show all the personal data it holds about them. What awareness of employee data rights should an analyst have, and what would your role be?
**Asked at:** commonly asked (no company-specific report found); data-subject requests appear in privacy-awareness questions (unverified).
**What the interviewer is checking:** That you know to route the request properly and cooperate, not freelance.
**Say this in the interview:** "I would not answer it myself. I would tell the employee the request goes through the HR or privacy team, then help by identifying where their data sits and producing the extract once the request is approved and the identity is verified."
**Explain simply:**
- People generally have a right to know what personal data an organisation holds about them and to ask for correction. This is the idea behind many privacy laws, including India's DPDP Act (from memory, unverified: details, timelines and exemptions need to be confirmed with the compliance or legal team).
- The company usually has a named process and owner, such as a data protection officer or privacy lead.
- Analyst role: map the systems (HRIS, payroll, attendance, learning, recruitment, email), pull only that person's records, exclude other people's data (for example comments by a manager that name colleagues) as the privacy team decides, and log what was shared.
- Never send the data informally by email or chat.
**Regulation / privacy note (awareness only):** From memory, unverified: employee rights, response deadlines and exceptions vary by law and country. Confirm with the compliance or legal team; this is not legal advice.
**Likely follow-ups:** 1) *Do you decide what is shared?* No, the privacy or legal team does. 2) *What if data sits in many systems?* A data inventory helps.
**Common mistakes:** Sending the file directly to the employee; including colleagues' data; not recording the request.

### Q116 ⭐⭐ 🟡 What does purpose limitation mean for employee data (for example, using badge-swipe data collected for security to judge productivity), and why does it matter?
**Asked at:** commonly asked (no company-specific report found); purpose limitation is a core privacy principle often asked in awareness questions (unverified).
**What the interviewer is checking:** Whether you pause before reusing data for a new purpose.
**Say this in the interview:** "Purpose limitation means data collected for one stated reason should not be reused for a very different one without a proper basis and, usually, telling people. Using badge swipes meant for building security to rate productivity would be a new purpose, so I would raise it with HR and privacy before doing it."
**Explain simply:**
- When employees give data, they are told why. Purpose limitation keeps the company to that promise.
- Badge swipes were collected for physical security and fire safety. Using them to judge work effort changes the purpose, and also misleads (people sit in meetings, work from client sites or take calls).
- Why it matters: trust, legal exposure (from memory, unverified: privacy laws such as the DPDP Act build on this idea; confirm with legal), and bad decisions from poor proxy data.
- Practical test: "Were employees told this use? Is it needed? Is there a less intrusive way?"
**Likely follow-ups:** 1) *Can the new purpose ever be allowed?* Possibly, with a documented basis, notice to employees and approval. 2) *What about anonymous footfall for office space planning?* Aggregated counts are lower risk, but still check the policy.
**Common mistakes:** "The data is already there so we can use it"; assuming the employee contract covers everything.

### Q117 ⭐⭐ 🟡 What are the ethical risks of scoring employees on "flight risk" or monitoring productivity from emails and logins, and what transparency would you recommend?
**Asked at:** commonly asked (no company-specific report found); ethical attrition prediction is a theme in people-analytics prep guides (unverified).
**What the interviewer is checking:** Judgement: you can see benefits and harms and propose safeguards.
**Say this in the interview:** "The risks are unfairness, self-fulfilling labels, loss of trust and misuse of the scores. I would use group-level insights rather than individual labels, tell employees what is measured and why, and keep humans in the decision."
**Explain simply:**
- **Flight risk score:** a model's estimate of how likely a person is to leave. Risks: a label that follows someone (they miss promotions or stretch work); errors and bias against groups; managers who treat the score as fact; employees who feel watched and leave.
- **Monitoring emails and logins:** counts of emails or hours online do not measure good work and penalise people in roles with different rhythms. It also feels intrusive.
- Safeguards: a clear purpose, minimum data, group-level reporting, bias checks across groups, no automated decisions, review by HR and legal, and limited access.
- Transparency: a plain notice on what data is used, why, who sees it, how long it is kept, and a way to ask questions.
**Likely follow-ups:** 1) *Better alternative?* Exit and stay interviews and team-level attrition drivers. 2) *Should employees see their own score?* Many would argue yes if used; decide with HR and legal.
**Common mistakes:** Treating a probability as a verdict; skipping bias checks; hiding the monitoring.

### Q118 ⭐⭐ 🟡 Why is it risky to email an Excel file with salaries or performance ratings, and what working habits would you follow instead?
**Asked at:** commonly asked (no company-specific report found); data-handling habits are often probed in behavioural questions (unverified).
**What the interviewer is checking:** Everyday security discipline with sensitive data.
**Say this in the interview:** "Email copies are uncontrolled: they can be forwarded, sit in many inboxes and be sent to the wrong person. I would share through an approved access-controlled location, send only the minimum, and protect files with permissions."
**Explain simply:**
- Risks: wrong recipient, forwarding, copies on personal devices, no way to take it back or see who opened it, hidden sheets or columns still containing data, and file names or previews that expose content.
- Better habits: share a link to a company-approved folder with named viewers; share aggregated data where possible; remove columns not needed; use IDs rather than names; password-protect and send the password separately if a file must travel (as the company policy allows); delete downloaded copies; use the dashboard with row-level security instead of files.
- Check before sending: right people, right purpose, right columns.
- If it goes wrong, report it at once to the security or privacy team.
**Likely follow-ups:** 1) *What if the manager insists?* Offer a secure link or summary and mention the policy. 2) *Is a password enough?* It is a minimum, not a replacement for access control.
**Common mistakes:** Hiding rather than deleting columns; using personal email; keeping old extracts on the desktop.

### Q119 ⭐⭐ 🟡 How long should an employer keep resumes of candidates who were not hired, and what practical steps would you take as an analyst to avoid keeping unnecessary candidate data?
**Asked at:** commonly asked (no company-specific report found); candidate-data retention is a recruitment-privacy awareness topic (unverified).
**What the interviewer is checking:** That you know retention should be limited and defined, and that you will follow policy rather than invent a number.
**Say this in the interview:** "There is no single answer I would quote; the period should come from the company's retention policy and local law. The principle is to keep it only as long as needed, for example for the hiring decision, possible disputes, or a talent pool the candidate agreed to. As an analyst I would help enforce deletion."
**Explain simply:**
- **Retention period:** how long data is kept before deletion. Some companies keep unsuccessful applications for months to a couple of years; this varies and the figure needs confirming with legal (from memory, unverified).
- A talent pool (keeping resumes for future roles) usually needs the candidate's agreement.
- Analyst steps: ask for the written retention rule; add a "date received" and "retention due date" to the candidate table; create a monthly list of records due for deletion for the owner to approve; keep only anonymised or aggregated records for funnel reporting; avoid copies of resumes in spreadsheets, emails and personal folders; remove sensitive fields not needed, such as photos, caste or marital status.
**Regulation / privacy note (awareness only):** From memory, unverified: privacy laws, including India's DPDP Act, generally expect data to be erased when its purpose ends. Confirm exact periods with the compliance or legal team.
**Likely follow-ups:** 1) *Can we keep funnel statistics?* Yes if anonymised. 2) *What if a candidate asks for deletion?* Route it to the privacy team.
**Common mistakes:** Keeping everything forever "just in case"; deleting from the ATS but not from exports; quoting a legal period as certain.

### Q120 ⭐⭐ 🟡 A global company's Indian centre sends employee data to a parent company abroad for global reporting. What privacy awareness points (cross-border transfer, access, purpose) would you raise?
**Asked at:** commonly asked (no company-specific report found); privacy and ethics themes appear in prep-site people-analytics guides (unverified).
**What the interviewer is checking:** Whether you treat employee data as something to protect, and whether you ask "does the parent really need this?" before you build the feed.
**Say this in the interview:** "I would ask three things: what exactly is being sent and why (purpose), who can see it abroad (access), and under what legal and contract cover it travels (transfer). Then I would send the least detail that still answers the reporting need, usually aggregated numbers instead of named records."
**Explain simply:**
- **Cross-border transfer** means personal data (name, salary, performance rating) moving out of India to a server or team in another country. Check that a transfer agreement or group policy exists and that Legal has approved it.
- **Purpose:** global headcount and attrition reporting needs counts by team, not salary of named people. Data collected for payroll should not quietly be reused for something unrelated.
- **Access:** use role-based access, so only the few people who need it can open it, and keep a log of who looked.
- **Minimise:** drop names, national ID numbers, bank details and health data from the feed. Replace employee IDs with codes where possible.
- **Retention and vendors:** agree how long the parent keeps the data, and check that any payroll or HRIS vendor in the chain is covered by contract.
**Regulation / privacy note (awareness only):** from memory, unverified, confirm with the compliance/legal team: India's data protection law (the DPDP Act, 2023) is understood to treat the employer as the party responsible for the data, to allow transfers abroad unless the government restricts particular countries, and to include notice and security duties. Exact dates and rules are still being phased in; this is not legal advice.
**Likely follow-ups:** 1) *Would you send salary by name?* Only if there is a stated need and approval; otherwise bands or averages. 2) *Who decides?* Legal, the data protection owner and HR leadership, not the analyst alone.
**Common mistakes:** Sending the whole HRIS extract "just in case"; assuming a global policy overrides local law; emailing spreadsheets with named data.

### Q121 ⭐⭐ 🟡 What is the difference between anonymity and confidentiality in employee surveys, and what happens when survey answers are linked to HRIS attributes such as team, grade and gender?
**Asked at:** commonly asked (no company-specific report found); survey privacy is a common people-analytics theme (unverified).
**What the interviewer is checking:** That you understand a promise of "anonymous" can be broken by the way you slice the data.
**Say this in the interview:** "Anonymous means nobody, including the survey team, can tell who answered. Confidential means the survey team knows who answered but promises not to share individual answers. Once I join answers to team, grade and gender, small groups can become identifiable, so I set a minimum group size before showing any result."
**Explain simply:**
- **Anonymity:** no name, ID or login is stored with the answers.
- **Confidentiality:** the vendor or HR can see who said what, but reports only show group results. Employees must be told clearly which one applies.
- **Linking to HRIS** (the core employee record system) lets you cut results by team, grade and gender. It is useful but each extra cut makes groups smaller.
**Worked example:** 40 respondents split by 4 teams x 3 grades x 2 genders = 24 cells, so 40 / 24 = 1.7 people per cell on average (rounded to 1 decimal). A cell holding 1 or 2 people effectively points to a person.
**Regulation / privacy note (awareness only):** from memory, unverified, confirm with the compliance/legal team: using answers for a purpose employees were not told about is a privacy concern; say plainly in the survey invitation how data is linked and used.
**Likely follow-ups:** 1) *What minimum group size?* Companies often pick a number around 5 to 10 (from memory, unverified); it is a policy choice, so state yours. 2) *What about overlapping cuts?* Hide results where two reports subtracted from each other reveal a small group.
**Common mistakes:** Calling a survey anonymous while the link carries a personal ID; reporting a team of 3; forgetting that "female, grade L7, Pune" may be one person.

### Q122 ⭐⭐ 🟡 How would you analyse free-text survey comments (themes, keyword counts, sentiment) and how would you protect the identity of commenters?
**Asked at:** commonly asked (no company-specific report found); text analysis of survey comments appears in prep-site lists (unverified).
**What the interviewer is checking:** That you can turn messy text into numbers, and that you know comments can identify people.
**Say this in the interview:** "I first remove names and identifying details, then group comments into themes such as workload, manager and pay, count how often each appears by group, and use sentiment as a rough tag. I read a sample by hand to check the grouping, and I publish only themes with enough comments."
**Explain simply:**
- **Theme coding:** read 100 to 200 comments, write a short list of themes, tag every comment (one comment can have two themes). This is slow but accurate.
- **Keyword counts:** quick and transparent ("shift", "manager", "salary"), but miss meaning ("no complaints about salary" counts as a pain point).
- **Sentiment:** a tool scores each comment positive, neutral or negative. It is rough and often confused by sarcasm or by local phrases or mixed languages, so spot-check it.
- **Protecting identity:** strip names, team names, places and unusual details ("the only night-shift trainer"); show comments only for groups above the minimum size; quote only a few, lightly edited; limit who can see the raw file.
**Likely follow-ups:** 1) *Can you show verbatim quotes?* Only after removing identifying detail and with the survey's privacy promise in mind. 2) *How do you check the tags?* Have a second person tag a sample and compare agreement.
**Common mistakes:** Trusting sentiment scores blindly; reporting keyword counts without volume of respondents; publishing a revealing quote because it is "powerful".

### Q123 ⭐⭐ 🟡 How would you identify the main drivers of overall engagement from the survey items, and why does high correlation between an item and engagement not prove causation?
**Asked at:** commonly asked (no company-specific report found); key-driver analysis is a standard survey topic (unverified).
**What the interviewer is checking:** That you know the basic method and its limits.
**Say this in the interview:** "I would correlate each survey item (manager support, growth, workload, pay) with the overall engagement score, then use a regression to see which items still matter when considered together. But a strong link only tells us two things move together, not that one causes the other."
**Explain simply:**
- **Correlation** (a number from -1 to +1) shows how strongly two scores move together; **regression** estimates each item's effect while holding the others steady.
- Items such as "I get recognition" and "I recommend this company" are often so alike that they overlap; check for that before ranking drivers.
- Plot importance (the link strength) against score (how well we do): an item that is important and scored low is the priority.
- **Why not causation:** (1) *reverse direction*: engaged people may rate their manager kindly, not the other way round; (2) a *third factor* such as a recent bonus lifts every answer; (3) the same mood colours every item answered in one sitting.
- To get nearer to cause, compare over time, run a small pilot where one team gets a change and a similar team does not, and add outside data such as actual attrition.
**Likely follow-ups:** 1) *How many responses do you need?* Enough per group that results are stable; small teams give noisy drivers. 2) *Which correlation level counts as high?* There is no fixed cut-off; say what you use and give context.
**Common mistakes:** Saying "manager support drives engagement" from one correlation; ignoring overlap between items; running it on very small groups.

### Q124 ⭐⭐ 🟡 Engagement scores in a team rose from 62 to 71, but the response rate fell from 85% to 48%. How would you interpret the change?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you notice that a score from fewer people may not mean the same thing.
**Say this in the interview:** "I would not report this as an improvement yet. When response falls that much, the missing people may be the unhappy ones, so the rise could be a change in who answered, not in how people feel. I would check who stopped responding and compare the same people across both rounds."
**Explain simply:**
- **Response rate** is respondents divided by people invited. Low response means the score describes only the people who chose to answer (**non-response bias**).
- Disengaged people often skip surveys, so scores can rise as response falls.
- Fewer answers also make the score less stable.
**Worked example (assume a team of 100, so 85 then 48 respondents; scores 0 to 100; all invented):** The first round total is 85 x 62 = 5,270 points. The second is 48 x 71 = 3,408. If the 48 were among the original 85, the 37 who stopped answering would have averaged (5,270 - 3,408) / 37 = 50.3 on the first survey. So if the people who left the survey were that unhappy, the "9 point rise" can appear with no one changing their mind. With an assumed spread of 20 points between individual answers, the 95% margin of error on the difference (the size of gap that chance alone could plausibly produce) is about +/-7.1 points (rounded). A 9-point rise is only slightly larger than that, which is another reason for caution.
**Data and tables involved:** survey invite list joined to HRIS (team, tenure, grade), respondents by round; first cuts: who responded in both rounds, response by tenure and grade, exits between rounds.
**Likely follow-ups:** 1) *How do you test it?* Compare only repeat respondents, and compare responders with the invited population on tenure, grade and gender. 2) *Why did response fall?* Survey fatigue, a broken link, or fear; ask the survey team.
**Common mistakes:** Celebrating the score; comparing scores without comparing response; forgetting people who left the team during the period.

### Q125 ⭐⭐ 🟡 What would you look at in the early days of a new joiner cohort (attendance, system access, check-in survey, manager one-to-ones) to predict who will leave in 90 days?
**Asked at:** commonly asked (no company-specific report found); first-90-day metrics are a theme in prep-site people-analytics guides (unverified).
**What the interviewer is checking:** That you think of early warning signals, not just counting exits afterwards.
**Say this in the interview:** "I would build a simple early-warning view per new joiner from the first two weeks: attendance and lateness, whether laptop and system access were ready on day one, the answers to a day-30 check-in, and whether the manager held the planned one-to-ones. Then I would compare it with who actually left within 90 days, to learn which signals count."
**Explain simply:**
- **Attendance:** unplanned absence or late logins in week 1 to 2 (use the attendance system, not memory).
- **System access:** late access means the person sat idle and felt unwelcome; measure days from joining to full access.
- **Check-in survey:** a short pulse at day 15 or 30 (clear role? supported? would you recommend us?).
- **Manager one-to-ones:** held or skipped, from the manager's calendar or HR tool.
- 90-day attrition = joiners who left within 90 days / joiners in the cohort. Example: 30 of 200 joiners left, so 30 / 200 = 15%.
- Compare past cohorts first (signal present vs absent, and exit rate in each), before building any model.
**Regulation / privacy note (awareness only):** from memory, unverified, confirm with the compliance/legal team: use such flags to help managers support people, not to punish, and tell employees what is tracked.
**Likely follow-ups:** 1) *How do you avoid unfair flags?* Check results by group and keep a human in the loop. 2) *Small cohort?* Report patterns across several cohorts.
**Common mistakes:** Using exit data only after the fact; treating every flag as a certain leaver; ignoring joiners' source and role differences.

### Q126 ⭐⭐ 🟡 What does it mean that some HR metrics are leading indicators (pending resignations, engagement, internal mobility) and others are lagging (attrition, time to fill)? Give examples of each.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can separate "early warning" from "final result".
**Say this in the interview:** "A leading indicator moves before the outcome and lets you act; a lagging indicator reports what already happened. Engagement and pending resignations warn of attrition; the attrition rate confirms it afterwards."
**Explain simply:**
- **Leading (early signal):** engagement or pulse score; notice-period (pending resignation) count; internal mobility (people moving into new roles instead of leaving); offer-acceptance rate; training completion.
- **Lagging (result):** attrition rate; time to fill (days from requisition approval to offer acceptance); cost per hire; revenue per employee.
- Think of a car: the fuel light is leading, the empty tank is lagging.
- Leading signals are noisier and not guaranteed to predict, so validate them against what happened later.
- Use both: leading ones for action, lagging ones for judging the result.
**Likely follow-ups:** 1) *Is time to fill always lagging?* Yes for a filled job; open-requisition age is closer to leading. 2) *How prove a signal leads?* Show it changes before attrition in past data.
**Common mistakes:** Calling attrition a warning sign; assuming a leading metric always predicts; reporting only lagging ones.

### Q127 ⭐⭐ 🟡 How would you explain the difference between a metric and a KPI to an HR head, using one example from attrition and one from hiring?
**Asked at:** commonly asked (no company-specific report found); the metric vs KPI distinction appears in HR-metrics guides (unverified).
**What the interviewer is checking:** Plain-spoken clarity with senior people.
**Say this in the interview:** "A metric is any number we can measure. A KPI is a metric we chose because it ties to a business goal, with a target and an owner. We track many metrics but only a few KPIs."
**Explain simply:**
- **Attrition example:** overall attrition rate (say 14%) is a metric. The KPI might be "regretted attrition (exits we wanted to keep) in critical roles below 8% this year", with the HR business partner as owner.
- **Hiring example:** the number of applications received is a metric. The KPI might be "critical roles filled within 45 days for 90% of requisitions", owned by the talent acquisition head.
- Rule of thumb: if no one acts when it moves, it is a metric, not a KPI.
- Definitions differ by company; state yours (for example, how "regretted" is decided).
**Likely follow-ups:** 1) *How many KPIs?* A handful; too many hide what matters. 2) *Can a metric become a KPI?* Yes, once a goal and owner are agreed. (The 14%, 8%, 45 days and 90% are invented examples.)
**Common mistakes:** Calling every dashboard number a KPI; KPIs with no target; picking a KPI people can game.

### Q128 ⭐⭐ 🟡 HR operations says they closed 92% of employee queries within the agreed time. What additional data (volume, category, reopen rate, satisfaction) would you ask for before judging service quality?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That one headline percentage does not satisfy you.
**Say this in the interview:** "92% on time is a good start, but I would ask for volume, a split by category, how many tickets were reopened, and employee satisfaction, because a team can close fast without solving the problem."
**Explain simply:**
- **Volume** and trend: 92% of 50 queries is very different from 92% of 5,000.
- **Category split:** easy ones (leave balance) can hide slow, painful ones (payroll errors).
- **Reopen rate:** share of closed tickets the employee reopened; high means closing without fixing.
- **Satisfaction (CSAT):** a one-question rating after closing; check response rate too.
- **The agreed time itself:** is the SLA (service-level agreement, the promised time) generous or tight, and does the clock stop when HR "awaits employee reply"?
**Worked example (invented):** 1,000 queries: payroll 300 at 85% on time, leave 500 at 99%, other 200 at 85%. On-time total = 255 + 495 + 170 = 920, so 920 / 1,000 = 92%. Yet 45 payroll queries (300 x 15%) missed the target. If payroll's reopen rate is 12%, that is 36 reopened tickets.
**Likely follow-ups:** 1) *What else?* Average resolution time and the long tail (slowest 5%), and tickets per 100 employees. 2) *Who owns it?* HR operations; the analyst only measures.
**Common mistakes:** Accepting the headline; ignoring that urgency differs; counting auto-closed tickets as solved.

### Q129 ⭐⭐ 🟡 What is the employee-to-HR ratio and the HR cost per employee, and why are benchmarks of these two ratios hard to compare across companies?
**Asked at:** commonly asked (no company-specific report found); HR-to-employee ratio is named in HR-metrics guides (unverified).
**What the interviewer is checking:** That you can calculate simple ratios and also doubt comparisons.
**Say this in the interview:** "Employee-to-HR ratio is employees served per HR staff member; HR cost per employee is total HR spend divided by employees. The formulas are easy; comparing across companies is hard because the definitions of HR and the scope of work differ."
**Explain simply:**
- Employee-to-HR ratio = employees / HR staff (full-time equivalents, FTE).
- HR cost per employee = total HR cost / employees.
- Hard to compare because: whether payroll, recruiting, learning or HR tech sit inside HR; outsourcing (the cost moves to a vendor line); contractors in or out of headcount; company size and industry; shift or factory workforce versus office; and average versus year-end headcount.
- Published benchmarks (from memory, unverified) vary widely, so use them as a rough guide.
**Worked example (invented):** 1,200 employees, 12 HR staff, HR cost of Rs 3.6 crore (36,000,000). Ratio: 1,200 / 12 = 100 employees per HR person (or 1.0 HR per 100). Cost per employee: 36,000,000 / 1,200 = Rs 30,000 a year.
**Likely follow-ups:** 1) *Is lower always better?* No; too lean may mean slow service. 2) *How compare fairly?* Agree definitions and scope first.
**Common mistakes:** Comparing to a benchmark blindly; leaving outsourced cost out; mixing headcount types.

### Q130 ⭐⭐ 🔴 Regretted attrition among high performers rose while overall attrition stayed flat. How would you structure an analysis for the CHRO and which three actions might the data support?
**Asked at:** commonly asked (no company-specific report found); attrition analysis is a standard case theme (unverified).
**What the interviewer is checking:** Structured thinking: define, segment, find causes, recommend.
**Say this in the interview:** "Flat overall attrition can hide a bad mix: fewer weak performers leaving and more strong ones. I would confirm the definition of high performer and regretted, split attrition by segment, find where and why they leave, then propose targeted actions."
**Explain simply:**
- **Define:** who is a "high performer" (latest rating, same cycle) and "regretted" (a manager flag when they leave). Define once, document it.
- **Segment:** by team, location, manager, tenure, grade, pay position versus market, time since promotion, and rating.
- **Reasons:** exit-interview themes and where they went (competitor, other function).
- **Caution:** small numbers make rates swing; show counts as well.
**Worked example (invented):** High performers are 20% of staff. Year 1: high performers 10%, others 16.25%, overall 0.2 x 10 + 0.8 x 16.25 = 15%. Year 2: high performers 14%, others 15.25%, overall 0.2 x 14 + 0.8 x 15.25 = 15%. Overall is flat, yet high-performer attrition is 1.4 times higher (4 percentage points more).
**Three actions the data might support (pick only what it shows):** (1) fix pay where high performers sit below market; (2) review managers or teams with clusters of exits; (3) clear promotion and career paths for those waiting too long.
**Likely follow-ups:** 1) *Is the rise random?* Compare with last years and a confidence range. 2) *Cost?* Replacement cost times people lost.
**Common mistakes:** Reporting only the overall rate; changing the high-performer definition mid-analysis; recommending actions without data.

### Q131 ⭐⭐ 🔴 Sixty requisitions have been open for more than 90 days and the business says recruiting is slow. How would you analyse whether the delay is due to recruiters, hiring managers, pay competitiveness or unrealistic requirements?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you test the claim by splitting the time, not by blaming a group.
**Say this in the interview:** "I would measure how many days each requisition spent at each stage and who owned the wait: recruiter, hiring manager or candidate. Then I would test pay and requirements using offer-decline reasons and market comparisons."
**Explain simply:**
- **Requisition:** the approved request to fill a job.
- **Stage timing:** days from approval to first shortlist (recruiter), to interview feedback and scheduling (hiring manager), to offer and acceptance (candidate, pay).
- **Recruiters:** slate quality and speed, workload per recruiter.
- **Hiring managers:** days to give feedback, number of interview rounds, reschedules.
- **Pay:** offer-decline reasons and offered pay against market or against existing peers.
- **Requirements:** very rare skill combinations; compare how many candidates meet all stated requirements versus the pool.
**Worked example (invented averages across the 60):** recruiter stage 28 days, hiring manager stage 41 days, offer stage 21 days, total 90 days. Hiring-manager wait is 41 / 90 = 46% of the time, recruiter 31%, offer 23% (rounded). Here the bottleneck is feedback, not sourcing.
**Data and tables involved:** applicant tracking system (ATS) stage history (requisition ID, candidate, stage, date), requisition table (role, level, location, approver), offer table (outcome, decline reason), pay benchmark table.
**Likely follow-ups:** 1) *Median or mean?* Show both; a few very old requisitions skew the mean. 2) *Are the 60 comparable?* Group by role family first.
**Common mistakes:** Blaming recruiters without stage data; ignoring requisitions on hold; judging by aggregate time only.

### Q132 ⭐⭐ 🔴 Compensation says 120 employees are paid more than 15% below market and asks for an off-cycle correction. How would you design the analysis to prioritise who gets a correction, and what would you tell finance about cost?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Fair prioritisation and a clear, honest cost range.
**Say this in the interview:** "I would first verify that the market comparison is right for each person, then rank by how far below market, performance, criticality, flight risk and fairness against peers. For finance I would show a cost range by target level and by start date, including on-costs."
**Explain simply:**
- **Check the data first:** job match to market survey, location, pay components, tenure (new joiners often sit lower).
- **Market ratio** (often loosely called compa-ratio here) is pay divided by the market reference pay for the job; 0.85 means 15% below. In the strict sense, compa-ratio divides by the internal pay-range midpoint (Q35); I use the market figure here, so state which.
- **Priority score:** gap size, performance, critical skill, exit risk, internal equity, with a documented rule so it is defensible.
- **Fairness:** check by gender and group so the fix does not create a new gap.
- **Options:** correct to market in one step, to 90% of market now, or phase over two cycles.
**Worked example (invented):** 120 employees: 20 at compa 0.75, 40 at 0.80, 60 at 0.83, each with market pay Rs 10 lakh. To lift to 0.90: 20 x 0.15 x 10 lakh = 30 lakh; 40 x 0.10 x 10 = 40 lakh; 60 x 0.07 x 10 = 42 lakh; total Rs 1.12 crore a year. To 1.00 (full market): Rs 2.32 crore. With a 20% allowance for linked costs (an assumption), 1.34 crore and 2.78 crore. If effective mid-year, in-year cost is about half. Average current compa is 0.81.
**Likely follow-ups:** 1) *Is market data reliable?* Say the source and its date. 2) *What if budget is short?* Prioritise by score; phase the rest.
**Common mistakes:** Giving everyone the same raise; skipping the equity check; quoting only a total with no range.

### Q133 ⭐⭐ 🔴 The business plans 25% revenue growth next year. Build the headcount plan: list the assumptions you need (productivity, attrition, hiring lead time, mix of roles) and the checks you would show leadership.
**Asked at:** commonly asked (no company-specific report found); headcount planning with finance is named in prep-site guides (unverified).
**What the interviewer is checking:** That you can turn a revenue goal into a hiring number with stated assumptions.
**Say this in the interview:** "Required headcount equals planned revenue divided by revenue per employee. Then I add replacement hiring for people who will leave, split by role, and work back from lead times to when recruiting must start."
**Explain simply:**
- **Assumptions to collect:** current headcount and revenue; productivity change (revenue per employee); attrition rate by role; time to fill plus notice and ramp-up; role mix (delivery, sales, support); budget; contractors versus employees.
- **Checks to show:** revenue per head, hires per month versus recruiter capacity, cost of the plan against budget, and a sensitivity case (lower productivity gain, higher attrition).
**Worked example (invented, rounded):** 1,000 people now; revenue +25%; productivity +5%. End headcount = 1,000 x 1.25 / 1.05 = 1,190.5 (about 1,190), so net adds = about 190. Average headcount = about 1,095; at 15% attrition, replacements = about 164. Gross hires = 190.5 + 164.3 = about 355 (rounded from unrounded figures). Mix of 60%, 25%, 15% gives 213, 89 and 53 hires. With no productivity gain, net adds would be 250.
**Lead time:** if a hire takes 60 days to fill plus 30 days notice, recruiting for a role needed on 1 April must start around the start of January at the latest (90 days earlier), so December is safer.
**Likely follow-ups:** 1) *Does revenue move headcount one for one?* Not always; some roles scale less. 2) *How update?* Review quarterly.
**Common mistakes:** Forgetting replacement hiring; hiring all at the year start; one blended attrition rate for all roles.

### Q134 ⭐⭐ 🔴 Engagement fell by 10 points in one location year on year. Which data would you combine (attrition, pulse comments, manager changes, workload, leave) and how would you separate real change from noise?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you test the drop for significance and look for cause across datasets.
**Say this in the interview:** "First I check the drop is real: response, number of respondents and a confidence range. Then I join survey results with attrition, manager changes, overtime and leave to see what changed in that location compared with others."
**Explain simply:**
- **Real or noise:** with few respondents, scores swing. Use the margin of error and compare other locations over the same year.
- **Data to combine:** attrition and exits by team; manager changes (new manager, vacancies); workload (overtime, headcount per team); leave taken and unplanned absence; pulse comments themes; business events (restructure, move, pay cycle).
- **Compare** with unaffected locations (a difference-in-differences view): did the others also fall?
- Look for the sub-group driving it (one team, one shift).
**Worked example (invented):** about 60 and 55 respondents, spread of 18 points: standard error of the difference (how much the gap would wobble by chance) = sqrt(18^2/60 + 18^2/55) = 3.4; 95% margin = 1.96 x 3.4 = about 6.6 points. A 10-point drop is larger than that, so probably real, though not by much. With around 300 and 280 respondents, the margin would be about 2.9.
**Likely follow-ups:** 1) *Did response change?* Check first (see Q124). 2) *Next step?* Listening sessions to test the explanation.
**Common mistakes:** Reacting to small-group swings; claiming a cause from one data link; ignoring company-wide trends.

### Q135 ⭐ 🟢 What is a BPO or contact-centre "nesting period" and why do those workforces track first-90-day attrition so closely?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand the operations behind the numbers.
**Say this in the interview:** "A BPO (business process outsourcing) runs processes such as customer calls for other companies. After classroom training, new agents spend a 'nesting' period taking live calls with extra support before working alone. Many leave in training or nesting, and each dropout wastes a lot of hiring and training cost, so first-90-day attrition is watched closely."
**Explain simply:**
- Typical path: hire, classroom (product and process) training, nesting with a coach or a reduced target, then production. Lengths differ by company (from memory, unverified).
- Joiners are paid and trained before they bring in full revenue, so early exits lose that investment.
- Track by batch: share of a hiring batch lost during training, during nesting, and by day 90.
**Worked example (invented):** batch of 40: 6 leave in training, 5 in nesting. Loss = 11 / 40 = 27.5% (6 / 40 = 15% in training, 5 / 40 = 12.5% in nesting).
**Likely follow-ups:** 1) *Causes?* Mismatched expectations, shift timings, commute, trainer quality. 2) *Action?* Realistic job previews and better coaching.
**Common mistakes:** Mixing batches of different sizes; counting only post-production exits.

### Q136 ⭐ 🟢 What is the difference between an HR analyst, an HR generalist, an HR operations executive and an HRIS analyst, and which one suits an HR career switcher moving into analytics?
**Asked at:** commonly asked (no company-specific report found); role titles are from job posts, whose scope varies by company (unverified).
**What the interviewer is checking:** That you understand the HR function and can place yourself honestly.
**Say this in the interview:** "An HR generalist handles day-to-day people matters for a business unit; HR operations runs processes such as onboarding, payroll inputs and queries; an HRIS analyst looks after the HR system and its data and reports; an HR analyst studies the data to answer business questions. For a switcher, HR analyst is the most direct fit, with HRIS analyst as a technical route."
**Explain simply:**
- **HR generalist:** employee relations, hiring support, policy; broad, people-facing.
- **HR operations executive:** process work (joining, exits, letters, attendance, payroll inputs); accuracy and deadlines.
- **HRIS analyst:** HRIS means human resource information system (for example Workday, from memory); configures it, fixes data and builds reports.
- **HR analyst / people analyst:** dashboards on headcount, attrition, hiring and engagement, and insights to leaders; needs Excel, SQL, a BI tool such as Power BI.
- Job-post evidence suggests many HRIS and analytics roles ask for several years of experience, so entry through HR operations or an analyst role is realistic.
**Likely follow-ups:** 1) *Why you?* HR knowledge plus data skills is the pairing employers seek. 2) *First skill?* Excel and SQL on HR data.
**Common mistakes:** Assuming titles mean the same everywhere; ignoring HR domain knowledge as your strength.

### Q137 ⭐ 🟡 What is the difference between full-time, part-time and shift-based rostering data, and which metrics matter for a shift workforce (shrinkage, adherence, overtime)?
**Asked at:** commonly asked (no company-specific report found); more likely in BPO, retail, hospital and factory-linked HR analytics roles.
**What the interviewer is checking:** Whether you know that shift workers are measured on hours and coverage, not just headcount.
**Say this in the interview:** "Full-time and part-time describe the contract (hours per week). Shift-based describes when and how the hours are scheduled. For shift teams I track shrinkage, adherence and overtime because they show whether the right people are present at the right time."
**Explain simply:**
- **Full-time / part-time:** contract type. A part-timer might be contracted for 20 hours a week, so counts as 0.5 FTE (full-time equivalent: one full-time person's worth of hours).
- **Shift-based rostering:** a roster is the schedule saying who works which shift (morning, evening, night). The data has one row per person per shift, with planned and actual start and end times.
- **Shrinkage:** the share of paid scheduled time when people are NOT available to work (leave, absence, training, meetings). Definitions vary by company.
- **Adherence:** the share of scheduled time a person actually did what the roster said, at the time it said.
- **Overtime:** hours beyond contracted hours, usually shown as a % of base hours; high overtime signals understaffing or burnout risk.
**Worked example:** A 40-hour week: 3 hours absent + 2 leave + 1.5 training + 0.5 team meeting = 7 hours not available. Shrinkage = 7 / 40 = 17.5%. Adherence: 378 of 420 scheduled minutes on plan = 90.0%. Overtime: 120 overtime hours across 40 people on 40 base hours each = 120 / 1,600 = 7.5%.
**Regulation / privacy note (awareness only):** Overtime and working-hour limits are set by labour laws and state rules (from memory, unverified, confirm with the compliance/legal team).
**Likely follow-ups:** 1) *Is shrinkage always bad?* No, training and leave are planned; unplanned absence is the part to manage. 2) *Why FTE?* It lets part-timers and full-timers be compared on one scale.
**Common mistakes:** Counting a part-timer as one full head in workload metrics; mixing planned and unplanned shrinkage; not stating which definition you use.

### Q138 ⭐ 🟡 What is Human Capital Value Added or Human Capital ROI, and why do analysts treat such ratios with caution?
**Asked at:** commonly asked (no company-specific report found); appears in HR-analytics prep lists (unverified).
**What the interviewer is checking:** Whether you can define a classic ratio and also question what it really tells you.
**Say this in the interview:** "Both ratios ask how much value the business earns per unit of people cost or per person. They are useful for trends, but I would not use one number to judge HR or people."
**Explain simply:**
- **Human Capital Value Added (HCVA)** = (revenue minus all costs other than pay and benefits) divided by the number of FTE. In plain words: money left after buying everything except people, per person.
- **Human Capital ROI** = the same top line divided by total pay and benefits. It says how many rupees come back per rupee spent on people.
- Formulas vary between authors (from memory, unverified); always state yours.
- **Caution:** revenue depends on price, market, machines and luck, not only people; the ratio hides who is productive; different industries are not comparable; and a rise can come from cutting headcount rather than from better work.
**Worked example (invented numbers, in crore):** Revenue 500, total operating cost 420, pay and benefits 150, 100 FTE. Value added = 500 - (420 - 150) = 230. HCVA = 230 / 100 = 2.3 crore per FTE. HC ROI = 230 / 150 = 1.53 (rounded to 2 decimals).
**Likely follow-ups:** 1) *Better alternatives?* Track simple, explainable trends such as revenue per FTE alongside quality and attrition. 2) *Can it drive decisions?* Only as one input.
**Common mistakes:** Quoting it as proof that people "earn" a return; comparing across industries; using headcount instead of FTE.

### Q139 ⭐ 🟡 What contingent workforce share is "normal" in an IT or manufacturing company, and how would you track the cost difference between contractors and employees?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you avoid inventing a "normal" figure and can compare costs fairly.
**Say this in the interview:** "There is no single normal share. It depends on the business model, season and policy, so I compare against the company's own history and its stated target. For cost I compare fully loaded cost per productive hour."
**Explain simply:**
- **Contingent workforce:** people who are not on the company payroll as permanent staff: contractors, agency temps, consultants, freelancers.
- I would not quote an industry percentage; any figure I recalled would be from memory, unverified.
- Employee cost is more than salary: add benefits, provident fund, bonus, equipment, training and leave. Contractor cost is the invoice rate plus any agency management fee.
- Compare per hour actually worked, not per month.
**Worked example (invented):** Employee: annual pay 12,00,000 plus 25% loading = 15,00,000 for 1,800 worked hours = 833 per hour. Contractor: 1,000 per hour plus 10% agency fee = 1,100 per hour (1,800 hours = 19,80,000). Contractor costs about 32% more per hour here (1,100 / 833.33 = 1.32), but no recruitment, benefits or notice-period cost beyond the contract. Share: 120 contractors with 480 employees = 120 / 600 = 20% of workforce (or 25% of employee headcount; say which).
**Data and tables involved:** Headcount by worker type, vendor invoices or purchase orders, timesheets, cost centre, start and end dates.
**Likely follow-ups:** 1) *Why use contractors?* Flexibility for peaks and skills. 2) *Risk?* Knowledge loss and, from memory, unverified, legal worker-classification issues; check with legal.
**Common mistakes:** Comparing salary with invoice; forgetting contractors are often missing from the HRIS; stating a benchmark as fact.

### Q140 ⭐ 🟡 How would you measure the effectiveness of an employee referral programme, including the bonus cost per hire and the 12-month retention of referred hires?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you compare referred hires with non-referred hires on cost, quality and retention.
**Say this in the interview:** "I compare referrals with other sources on share of hires, cost per hire, speed, and 12-month retention. A referral programme works if referred hires cost less and stay at least as long."
**Explain simply:**
- **Referral:** an existing employee recommends a candidate; the employee gets a bonus if the hire succeeds (often after a waiting period).
- **Bonus cost per hire** = total bonus paid divided by referred hires (add programme running costs if known).
- **12-month retention** = of those hired, the share still employed 12 months later. Only count hires who have had 12 months to pass.
- Compare against agency fees, which are often a percentage of annual pay (from memory, unverified).
**Worked example (invented):** 40 hires in the year, 10 referred: referral share = 25%. Bonus 30,000 each: total 3,00,000, so 30,000 per referred hire. Agency fee at 8.33% of a 12,00,000 pay = about 99,960 per hire. After 12 months, 9 of 10 referred hires remain = 90%; 24 of 30 others remain = 80%. The 10 percentage point gap is based on tiny numbers, so call it a signal, not proof.
**Data and tables involved:** Hires table with source, referrer ID, join date, exit date, bonus paid date and amount.
**Likely follow-ups:** 1) *Any risk?* Referrals can reduce diversity if the network is similar; check mix. 2) *Is higher retention caused by the programme?* Not necessarily; referred candidates may be better matched anyway.
**Common mistakes:** Including recent hires in the retention denominator; ignoring bonus timing; small-sample over-claiming.

### Q141 ⭐ 🟡 What is a stay interview, and how could you use stay interview data and attrition data together?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can link qualitative conversations to a measurable outcome.
**Say this in the interview:** "A stay interview is a conversation with a current employee about why they stay and what might make them leave. I would code the answers into themes and risk flags, then check later whether flagged people actually left."
**Explain simply:**
- It is the opposite of an exit interview: done while the person is still here, so there is time to act.
- Turn notes into consistent fields: main reason to stay, main risk, risk rating (high/medium/low), date, manager.
- Join to the exit list by employee ID and look at who left within 6 or 12 months.
- Use the findings to improve the questions, find the themes behind leaving (pay, manager, growth), and target retention actions.
**Worked example (invented):** 60 people flagged high risk, 15 left within 6 months = 25%. 140 flagged low risk, 7 left = 5%. The high flag is 5 times as likely to be followed by an exit (25 / 5), so it is a useful signal.
**Regulation / privacy note (awareness only):** Interview notes are personal and sensitive; keep access limited, tell employees how notes are used, and report themes rather than names (from memory, unverified, confirm with the compliance/legal team).
**Likely follow-ups:** 1) *Does the flag cause attrition?* No; actions after the flag also change results. 2) *Sample bias?* Managers may pick comfortable employees.
**Common mistakes:** Leaving notes as free text; naming individuals on dashboards; judging success only on attrition rate.

### Q142 ⭐ 🟡 What are alumni (ex-employee) networks used for in HR analytics, and what data would you need to track rehire potential?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you see ex-employees as a talent source and know what data to keep.
**Say this in the interview:** "Alumni networks keep contact with former employees for rehiring, referrals and business links. To track rehire potential I need exit reason, performance at exit, eligibility for rehire, skills and consent to be contacted."
**Explain simply:**
- Uses: boomerang hires (people who return), referrals, learning why people left, brand reputation.
- Data: employee ID, exit date and type (resigned, terminated, retired), exit reason, last rating, last role and skills, manager's rehire-eligibility flag, notice-period behaviour, consent to contact, latest contact details.
- Metrics: share of hires who are rehires, time before return, rehire retention compared with new hires, cost saved on hiring.
- Keep one employee ID across stints so a returning person is not counted as brand new.
**Regulation / privacy note (awareness only):** Keeping and using ex-employee data needs a clear purpose, consent and a retention limit (from memory, unverified, confirm with the compliance/legal team).
**Likely follow-ups:** 1) *Rehire rate?* Rehires divided by total hires, over a stated period. 2) *Who should not be contacted?* Those flagged ineligible or without consent.
**Common mistakes:** Treating all leavers as rehire candidates; keeping data forever; ignoring consent.

### Q143 ⭐ 🟡 How would you describe the role of an employer brand in the hiring funnel, and which metrics (career page visits, application rate, offer acceptance) would you link to it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can tie a soft idea (reputation) to funnel numbers.
**Say this in the interview:** "Employer brand is how attractive the company looks as a place to work. It mostly shows up at the top and the bottom of the funnel: how many people visit and apply, and how many accept offers."
**Explain simply:**
- **Funnel:** the stages candidates pass through: visit, apply, interview, offer, join.
- Linked metrics: career page visits by source, visit-to-application rate, quality of applicants (share shortlisted), offer acceptance rate, cost per hire, and employer review ratings.
- Brand also shows in how many applicants per vacancy and how far you must raise pay to close offers.
- You cannot isolate brand cleanly; many things move at once (job market, pay, role).
**Worked example (invented):** 20,000 page visits, 800 applications = 4.0% application rate. 40 offers, 28 accepted = 70% acceptance. Compare both across quarters or against a campaign start date.
**Likely follow-ups:** 1) *Prove a campaign worked?* Compare before and after and against roles not targeted. 2) *Why do offers fail?* Pay, notice period, competing offers.
**Common mistakes:** Claiming causation from one rise; using visits alone; mixing roles of very different demand.

### Q144 ⭐ 🟡 How is an HR analytics maturity journey sequenced in a company with data in spreadsheets, HRIS and payroll in separate systems, and what would you build in the first 90 days?
**Asked at:** commonly asked (no company-specific report found); "first 90 days" questions appear in people-analytics prep guides (unverified).
**What the interviewer is checking:** Whether you start with trust in the data, not fancy models.
**Say this in the interview:** "I sequence it as: agree definitions, fix and join the data, report the basics reliably, then explain, and only then predict. In the first 90 days I would build a trusted headcount and attrition view."
**Explain simply:**
- **Stage 1, descriptive:** what happened (headcount, joiners, leavers). **Stage 2, diagnostic:** why. **Stage 3, predictive:** what may happen. **Stage 4, prescriptive:** what to do.
- Days 1-30: list data sources and owners, agree metric definitions with HR and finance, find the common key (employee ID).
- Days 31-60: match HRIS to payroll, clean duplicates and missing values, log every fix.
- Days 61-90: publish one dashboard (headcount, joiners, leavers, attrition by department) that ties to payroll and finance totals, with a refresh schedule.
- Quick win first; it builds trust.
**Regulation / privacy note (awareness only):** Set access rules early, since the data is personal (from memory, unverified, confirm with the compliance/legal team).
**Likely follow-ups:** 1) *Why not predict attrition first?* No clean base, no trust. 2) *First stakeholder?* The HR head and finance partner.
**Common mistakes:** Buying a tool before agreeing definitions; skipping reconciliation; building many dashboards instead of one trusted one.

### Q145 ⭐ 🟡 What is the difference between a legal entity, business unit, cost centre and location in HR reporting, and why do the same employees look different depending on the view?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know one employee has several organisational tags and can explain mismatched totals.
**Say this in the interview:** "Each is a different way of grouping the same person: who legally employs them, which part of the business they serve, whose budget pays them and where they sit. Totals differ because the groupings do not line up."
**Explain simply:**
- **Legal entity:** the registered company that employs and pays the person (used for statutory filings and tax).
- **Business unit:** a part of the business, like Retail or Consulting, used for management reporting.
- **Cost centre:** the budget bucket their cost is charged to; can be shared or split.
- **Location:** the office or site; can differ from the legal entity's registered address.
- Example: Asha is employed by Company A Pvt Ltd (entity), works in Retail (business unit), is paid from cost centre 4102, and sits in Pune (location). She can be counted in four different tables.
- Differences also come from people on loan between entities, split cost centres, and mid-year transfers.
**Likely follow-ups:** 1) *Which view for the board?* Usually legal entity or business unit, stated clearly. 2) *How to prevent confusion?* A reference table mapping all four tags per employee with effective dates.
**Common mistakes:** Mixing views in one chart; assuming cost centre equals department; ignoring effective dates.

### Q146 ⭐ 🟡 How does an employee's work location (office, hybrid, remote) get stored in HR data, and what difficulties arise in analysing hybrid work?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know a single field rarely captures real behaviour.
**Say this in the interview:** "Usually it is a work-arrangement field (office, hybrid, remote) plus a base location. The trouble is that the field shows the policy, not the days people actually come in."
**Explain simply:**
- Typical fields: base location, work arrangement type, home city for remote staff, effective date.
- **Hybrid:** the policy might be 3 office days a week, but the HRIS records only the label "hybrid".
- Actual attendance comes from other sources: badge swipes, desk booking, Wi-Fi logs.
- Difficulties: the label is rarely updated; arrangements change by team or by week; remote staff in another state or country affect payroll and tax; comparing hybrid against office staff mixes in role and seniority differences.
- Start with a check: does the label match badge data?
**Regulation / privacy note (awareness only):** Tracking attendance or location is monitoring; explain purpose and keep it aggregate (from memory, unverified, confirm with the compliance/legal team).
**Likely follow-ups:** 1) *Measure hybrid effect on attrition?* Compare similar roles, controlling for grade and tenure. 2) *Which data is more reliable?* Badge data for presence, with its gaps.
**Common mistakes:** Treating the label as truth; ignoring effective dates; drawing causal conclusions from raw comparisons.

### Q147 ⭐ 🟡 What is a probation period, how does confirmation work, and which confirmation data would you analyse (confirmed on time, extended, terminated during probation)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand the new-hire lifecycle and can define cohort-based metrics.
**Say this in the interview:** "Probation is an initial trial period, often a few months, after which the company decides to confirm the employee, extend probation or end employment. I track outcomes by joining cohort."
**Explain simply:**
- **Probation:** a fixed period at the start (length depends on company policy and contract).
- **Confirmation:** a formal decision, usually based on the manager's review, that the employee passes and becomes permanent.
- Data: join date, probation end date, review date, outcome (confirmed, extended, terminated, resigned), extension length, manager and department.
- Analyse by cohort: only include people whose probation end date has passed.
- Look for delay in confirmation (paperwork gaps), departments with many extensions, and early exits that suggest weak hiring or onboarding.
**Worked example (invented):** Cohort of 100 joiners, probation ended for all. Confirmed on time 72 = 72%; extended 18 = 18%; terminated or left in probation 10 = 10%. Total 100%.
**Likely follow-ups:** 1) *What is "on time"?* Confirmed by the probation end date; define it. 2) *High extensions?* Possibly unclear goals or slow managers.
**Common mistakes:** Including people still on probation; mixing resignations and terminations; ignoring who owns the delay.

### Q148 ⭐ 🟡 What are internal job postings and internal movement, and how would you compute the share of vacancies filled internally by grade?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can compute a rate by group and define the denominator.
**Say this in the interview:** "Internal postings let current employees apply first. Internal movement is promotion or transfer. The share filled internally is vacancies filled by employees divided by all vacancies filled, by grade."
**Explain simply:**
- **Internal job posting:** a vacancy advertised to employees before or with outside hiring.
- **Internal movement:** an employee changes role (transfer), grade (promotion) or both.
- Denominator is vacancies filled (not opened, not including cancelled ones); say so.
- Why it matters: career growth, lower hiring cost, and retention.
**Worked example (invented data, SQLite):**
```sql
-- For each grade, count filled vacancies and how many went to employees
SELECT
    grade,
    COUNT(*) AS vacancies_filled,
    SUM(CASE WHEN filled_by = 'Internal' THEN 1 ELSE 0 END) AS filled_internally,
    ROUND(100.0 * SUM(CASE WHEN filled_by = 'Internal' THEN 1 ELSE 0 END) / COUNT(*), 1) AS internal_fill_pct
FROM filled_vacancies
GROUP BY grade
ORDER BY grade;
```
Output: G3: 4 filled, 1 internal, 25.0%; G4: 3 filled, 2 internal, 66.7%; G5: 3 filled, 2 internal, 66.7%. Overall 5 of 10 = 50%. In plain words: junior roles are mostly filled from outside; senior roles mostly from inside.
**Likely follow-ups:** 1) *Higher is better?* Not always; fresh talent matters too. 2) *Which date?* Fill date, in a stated period.
**Common mistakes:** Dividing by openings rather than fills; mixing grade before and after promotion; counting transfers that change no grade as promotions.

### Q149 ⭐ 🔴 Leadership asks for a one-page "state of the workforce" for the board. Which ten numbers would you include, and what notes would you add on definitions and privacy?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can choose few, decision-useful metrics and state their definitions.
**Say this in the interview:** "I would pick ten numbers that cover size, movement, cost, hiring, retention and fairness, each with its definition in a footnote and a trend against last period."
**Explain simply:** A sensible ten (my judgement; adapt to the company):
1. Total headcount and FTE at period end.
2. Joiners and leavers in the period.
3. Attrition rate (rolling 12 months), split voluntary and involuntary.
4. Open positions and time to fill.
5. Offer acceptance rate.
6. Total people cost and as % of revenue.
7. Contractor share of workforce.
8. Engagement score (and response rate).
9. Share of women overall and in senior roles.
10. Internal fill rate or promotions, plus new-hire 12-month retention.
- Notes: define each metric once (period, who counts as an employee, FTE rule); source and "as of" date; comparison to prior period; known data gaps.
- Privacy: show aggregates only; hide groups below a minimum size; no names.
**Regulation / privacy note (awareness only):** Board packs spread widely; follow the company's data-protection policy (from memory, unverified, confirm with the compliance/legal team).
**Likely follow-ups:** 1) *Why not 30 metrics?* The board needs decisions, not a data dump. 2) *Gender data?* Present as aggregates, and say how it is recorded.
**Common mistakes:** Undefined terms; headcount and FTE mixed; trends missing; small-group figures exposing individuals.

### Q150 ⭐ 🔴 An external audit asks you to prove the headcount reported to the board on 31 March. What evidence (HRIS snapshot, payroll register, attendance, reconciliations) would you assemble?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can build a traceable, reproducible evidence trail.
**Say this in the interview:** "I would freeze a dated HRIS snapshot, reconcile it to the March payroll register, explain every difference, and keep the definition and query used so the number can be rebuilt."
**Explain simply:**
- **HRIS snapshot:** the employee list as of 31 March with status, join and exit dates (a stored copy, not today's live data).
- **Payroll register:** the list of people paid for March; the independent second source.
- **Attendance or access records:** show that sampled people were actually working.
- **Reconciliation:** a bridge between the two counts with each difference explained by joiner, leaver or leave.
- Also keep: the headcount definition used, the query or report, a list of joiners and leavers with approvals, offer and exit letters for a sample, and a list of manual corrections.
**Worked example (invented):** HRIS active on 31 March: 1,240. Payroll paid in March: 1,252. Remove 15 who left during March but were paid for part of the month: 1,237. Add 3 who joined on 31 March but are first paid in April: 1,240. Bridge ties to HRIS (1,252 - 15 + 3 = 1,240).
**Regulation / privacy note (awareness only):** Share only what the auditor needs, via a secure channel (from memory, unverified, confirm with the compliance/legal team).
**Likely follow-ups:** 1) *If it does not tie?* Investigate and document; do not force it. 2) *Backdated entries?* Compare the snapshot against the later data to find them.
**Common mistakes:** Using today's HRIS data for a past date; ignoring contractors in the definition; unexplained differences.
