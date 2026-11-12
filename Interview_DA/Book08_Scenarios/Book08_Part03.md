# Book 8 — Scenario-Based & Data Interpretation | Part 3: Dashboard and Report Scenarios 🟡

**Target:** 70 questions | **Actual:** 70 questions
**Scope:** On-the-job dashboard and report scenarios: numbers that do not match, slow dashboards and refreshes, stale or provisional data, and how to communicate and fix them, with inline exercise numbers where a figure can be derived.

### Q1 ⭐⭐⭐ 🟢 Your dashboard shows 10,200 orders for last month and a colleague's SQL report shows 9,800 for the same month. What is the first thing you check, and in what order do you work through the rest?
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 What are the most common reasons two reports built on the same business data show different totals for the same KPI?
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 A stakeholder messages you, "Your dashboard is wrong." How do you respond in the first hour?
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 A dashboard that took 5 seconds to open now takes 40 seconds. What is the first step you take before changing anything?
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 What is a single source of truth for metrics, and why does it matter when several dashboards report the same KPI?
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 What do you validate before you publish a new dashboard to senior leadership?
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟢 A dashboard card labelled "Orders" shows 12,500, while Finance says there were 9,000 orders. The orders table has one row per order line item.
Inline data: 12,500 rows in the table; 9,000 distinct order IDs; the card uses a plain row count.
Question: how many orders are over-counted, by what percentage, and what is the fix?
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟢 The sales head says the dashboard "has not updated since yesterday" at 10 am, but the scheduled refresh shows as successful. How do you find out what is going on and what do you tell them?
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 The HR dashboard shows 1,248 active employees on 30 September while the payroll report shows 1,196. How do you reconcile the two, and what do you do with any gap you cannot explain?
Inline data: HRIS includes 38 contractors who are not on payroll; 9 new joiners have a joining date of 1 October but were entered early with 30 September; payroll excludes all of these.
Question: how many employees remain unexplained?
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 The sales dashboard shows revenue of INR 482 lakh for October, while Finance reports INR 465 lakh. How do you narrow down the INR 17 lakh gap?
Inline data: the dashboard counts revenue on order date and includes cancelled orders worth INR 11 lakh; Finance counts revenue on invoice date.
Question: how much of the gap is still unexplained after cancelled orders, and what do you check next?
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 Daily order counts on your UTC-based dashboard differ from the operations team's IST report, but the monthly totals nearly match. Can you show the two daily figures are consistent?
Inline data: dashboard (UTC) shows 820 orders for 1 November. IST is UTC+5:30, so the IST day 1 November runs from 31 October 18:30 UTC to 1 November 18:30 UTC. Orders placed 31 October 18:30 to 23:59 UTC: 160. Orders placed 1 November 18:30 to 23:59 UTC: 75.
Question: what should the IST report show for 1 November?
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 The dashboard's average order value is INR 1,250, but an analyst's Excel calculation gives INR 1,400 for the same two days. Which is right and why do they differ?
Inline data: Day A had 100 orders with an average of INR 1,000; Day B had 400 orders with an average of INR 1,500. The dashboard takes the average of the two daily averages.
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 A Power BI dataset refresh took 15 minutes last month and now takes 70 minutes. What do you check, in what order?
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 A report is fast for most users but very slow for some users and on Monday mornings. How do you diagnose it?
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 A manager says, "This number was different when I looked last week for the same period." How do you find out why and explain it?
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🟡 The dashboard shows Sales department attrition of 18.0%, but the HR lead calculated 14.4% for the same quarter. Explain the gap and say which you would publish.
Inline data: 54 leavers; closing headcount 300; opening headcount 450. Dashboard divides leavers by closing headcount; HR divides by average of opening and closing headcount.
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐⭐ 🟡 A region table shows distinct customers of 120, 95 and 110, but the grand total says 290, not 325. Is this a bug, and how would you explain it to a business user?
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐⭐ 🟡 After you add a payments table to the model, the revenue total jumps. How do you confirm a join fan-out and what do you do?
Inline data: before the change, total revenue INR 5,00,000 across 500 orders. 200 of the orders (revenue INR 2,40,000) have two payment rows each (split payments).
Question: what total does the report now show and why?
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐⭐ 🟡 A dashboard total is INR 46 lakh while the source system says INR 50 lakh for the same period, and you suspect rows are being dropped in the model. How do you confirm and fix it?
Inline data: 5,000 orders in the source; 4,600 find a matching customer in the customer master; the model uses an inner join to the master.
Question: what share of orders and what rupee amount is missing from the dashboard?
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐⭐ 🟡 A VP sends you an Excel sheet and says the dashboard must be changed to match it. How do you decide whose number is right?
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐⭐ 🟡 The dashboard shows a conversion rate of 4.2% while the funnel report shows 3.5% for the same week. What explains it and which would you present?
Inline data: 700 orders; 20,000 sessions; about 16,700 unique visitors. One report divides orders by sessions and the other by unique visitors.
Question: which report uses which denominator?
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐⭐ 🟡 A number matches the source for most filter selections but is wrong for a few combinations, such as one region in one month. How do you isolate the problem quickly?
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐⭐ 🔴 Finance and Sales each quote a different revenue figure for the same quarter, and each wants the executive dashboard to show theirs. How do you resolve it?
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐⭐ 🔴 At 8 am you find one of three source systems failed overnight, so the executive dashboard is missing about 20% of the data, and the CEO reviews it at 9 am. What do you do?
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐⭐ 🔴 You discover that a number you sent to leadership last week was wrong and decisions may already have been taken on it. What do you do, step by step?
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐⭐ 🔴 A Power BI report on a table with about 200 million rows takes 3 minutes to open and the business wants it under 10 seconds. What is your plan?
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟢 What is the difference between import (extract) and live/DirectQuery connections for a business dashboard, and when would you choose each?
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟢 What is incremental refresh and when would you use it for a daily sales report?
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟢 How do you decide how often a dashboard should refresh?
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟢 A dashboard card shows "Attrition +20%", and an executive reads it as attrition being 20%. How would you fix the presentation?
Inline data: last quarter attrition was 10% and this quarter it is 12%.
Question: what are the two correct ways to state the change?
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟢 A stakeholder objects that the percentages in a pie chart add up to 99%. How do you handle it?
Inline data: 121 employees split across three locations as 55, 33 and 33, shown rounded to whole percentages.
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟢 The dashboard shows year-to-date revenue on a calendar-year basis, but the company's financial year runs April to March. How do you show the right figure?
Inline data: January to March revenue INR 24 lakh in total; April to October revenue INR 10 lakh per month.
Question: what are calendar YTD and financial-year YTD at the end of October?
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟢 How do you communicate a change in a KPI definition on a live dashboard so users are not confused?
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 The attendance dashboard shows an employee at 61.3% attendance, but the employee expects a much higher figure. Find the cause and give the right figure.
Inline data: October has 31 calendar days and 22 working days. The employee was present 19 days, on approved leave 2 days and absent 1 day. The dashboard divides present days by calendar days.
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 Your dashboard shows a gross margin of 31.5% while Finance reports 29.8%. How do you find what explains the difference?
Inline data: revenue INR 200 lakh. Dashboard COGS is INR 137 lakh. Finance also includes INR 3.4 lakh of freight in COGS.
Question: show that the freight explains the gap.
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 On 20 November, the dashboard shows month-to-date revenue 28% below last November and leadership is worried. Is the comparison fair?
Inline data: MTD revenue to 20 November is INR 3.6 crore. Last November in full was INR 5.0 crore, of which INR 3.4 crore fell between 1 and 20 November.
Question: what is the like-for-like change?
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 The revenue by region chart shows an "Unknown" bucket. What do you do about it and what do you tell the stakeholder?
Inline data: North INR 40 lakh, South INR 35 lakh, East INR 13 lakh, Unknown INR 12 lakh.
Question: what is North's share with and without the Unknown bucket?
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 Users see yesterday's numbers every morning even though refreshes succeed. How do you find the problem?
Inline data: source extract finishes 02:40; ETL runs 03:00 to 04:10; dataset refresh is scheduled for 04:00; report is viewed from 08:00.
Question: how long is the overlap, and what would you change?
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟡 Your dataset has about 18 million rows covering three years (1,095 days), and a full daily refresh takes 60 minutes, though only the last 7 days of data ever change. How would incremental refresh help, and roughly how much data would each refresh process?
Inline data: assume rows are spread evenly across days.
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🟡 A dashboard page has 24 visuals and loads in 28 seconds; the target is 5 seconds. What do you do?
Inline data: in this exercise load time is the sum of visual times. Three visuals take 20 seconds in total; the other 21 take 8 seconds in total. After tuning, the three slow visuals take 2 seconds in total.
Question: what is the load time now, and what else must you do?
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🟡 An executive slicer lists all 40,000 employee IDs and makes the page slow. What do you change?
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🟡 A user says, "I selected Hyderabad and the dashboard shows nothing, but it worked last week." How do you troubleshoot?
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🟡 A senior leader asks you to add 15 more KPIs and 10 filters to an executive dashboard that is already slow and cluttered. How do you respond?
<!-- ANSWER_PENDING -->

### Q44 ⭐⭐ 🟡 You find that test and dummy accounts have been included in a revenue dashboard for two months. How do you fix it and communicate it?
<!-- ANSWER_PENDING -->

### Q45 ⭐⭐ 🟡 How would you design a dashboard so users can tell when its numbers are provisional or incomplete?
<!-- ANSWER_PENDING -->

### Q46 ⭐⭐ 🟡 A scheduled refresh failed at 3 am because of an expired credential and you only learnt about it at 9 am from users. How do you handle it and stop it recurring?
<!-- ANSWER_PENDING -->

### Q47 ⭐⭐ 🟡 An executive asks for a real-time dashboard, but the source can only deliver hourly batches and live queries would slow the operational system. How do you respond?
<!-- ANSWER_PENDING -->

### Q48 ⭐⭐ 🟡 The new Power BI report differs from the legacy Excel report by 0.8%, and the business refuses to switch. How do you handle the migration?
<!-- ANSWER_PENDING -->

### Q49 ⭐⭐ 🟡 Three regional managers each see only their region, and the national head sees a different total from the sum of their numbers. What do you check?
Inline data: the national head sees 1,000 records; managers see 400, 350 and 300 records.
Question: what does the 50-record excess suggest?
<!-- ANSWER_PENDING -->

### Q50 ⭐⭐ 🟡 The headcount for March showed 520 when you published the report, but today the same dashboard shows 500 for March. What happened and how do you prevent it?
<!-- ANSWER_PENDING -->

### Q51 ⭐⭐ 🟡 When is a difference of 0.3% between a dashboard and a source report worth chasing, and when would you leave it?
<!-- ANSWER_PENDING -->

### Q52 ⭐⭐ 🟡 What automated checks would you add so a mismatch is caught before users see it?
<!-- ANSWER_PENDING -->

### Q53 ⭐⭐ 🟡 A VP says, "Your dashboard has too much on it and I cannot find the answer." How do you rework it?
<!-- ANSWER_PENDING -->

### Q54 ⭐⭐ 🟡 Users have stopped trusting a dashboard after two incorrect numbers in a month. How do you rebuild trust?
<!-- ANSWER_PENDING -->

### Q55 ⭐⭐ 🔴 You discover 14 different "Sales Dashboard" files across teams, each with slightly different numbers. How do you rationalise them?
<!-- ANSWER_PENDING -->

### Q56 ⭐⭐ 🔴 Customer counts differ across CRM, billing and finance systems, and none is accepted as authoritative. How do you build a reconciliation approach?
<!-- ANSWER_PENDING -->

### Q57 ⭐⭐ 🔴 You notice a manager-level dashboard exposes peers' salary figures because of a row-level security mistake. What do you do?
<!-- ANSWER_PENDING -->

### Q58 ⭐ 🟢 A weekly dashboard refreshes four times a day for 20 minutes each, but usage logs show two viewers open it once a week. What do you do and how many refresh minutes per week do you save?
<!-- ANSWER_PENDING -->

### Q59 ⭐ 🟢 A scheduled email PDF of the dashboard goes out at 7 am, while the data refreshes at 8 am, so recipients see old numbers. How do you fix it?
<!-- ANSWER_PENDING -->

### Q60 ⭐ 🟢 The department headcount chart sums to 1,150, but the HRIS export totals 1,170. How do you find the difference?
Inline data: Engineering 410, Sales 280, Operations 330, Corporate 150 in the export; the dashboard excludes 20 employees whose department field is blank.
Question: confirm the 20-person gap and decide how to show them.
<!-- ANSWER_PENDING -->

### Q61 ⭐ 🟡 Dashboard sales in INR differ from Finance's INR figure for USD sales. Find the likely cause and decide which to use.
Inline data: USD 10,000 of sales in the month. Finance converts at one month-average rate of INR 83.00; the dashboard converts each transaction at its daily rate, giving INR 8,36,500.
Question: how big is the difference in rupees and per cent?
<!-- ANSWER_PENDING -->

### Q62 ⭐ 🟡 After a data-model change, how would you regression-test a dashboard before releasing it?
<!-- ANSWER_PENDING -->

### Q63 ⭐ 🟡 An old dashboard that people still rely on is broken and no one owns it. How do you handle it?
<!-- ANSWER_PENDING -->

### Q64 ⭐ 🟡 A "Top 10 products" visual gives different results when another filter is applied, and the user thinks the numbers are wrong. How do you explain it?
<!-- ANSWER_PENDING -->

### Q65 ⭐ 🟡 A % of total measure shows 100% for every row once a user selects a category in a slicer. What is happening and how would you change the measure?
<!-- ANSWER_PENDING -->

### Q66 ⭐ 🟡 How do you measure whether a dashboard is actually being used and decide whether to retire it?
<!-- ANSWER_PENDING -->

### Q67 ⭐ 🟡 A user says the mobile app shows different totals from the desktop view of the same report. How do you investigate?
<!-- ANSWER_PENDING -->

### Q68 ⭐ 🔴 A BI tool's approximate distinct count differs by 1.2% from an exact SQL count. When do you accept this and when not?
<!-- ANSWER_PENDING -->

### Q69 ⭐ 🔴 After a department restructure, last year's department-wise numbers on the dashboard changed. How do you handle history in the model and what do you tell users?
<!-- ANSWER_PENDING -->

### Q70 ⭐ 🔴 A director asks you to remove a red KPI from the dashboard before a board meeting. How do you respond?
<!-- ANSWER_PENDING -->
