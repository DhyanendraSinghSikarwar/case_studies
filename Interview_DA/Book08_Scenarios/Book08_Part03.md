# Book 8 — Scenario-Based & Data Interpretation | Part 3: Dashboard and Report Scenarios 🟡

**Target:** 70 questions | **Actual:** 70 questions
**Scope:** On-the-job dashboard and report scenarios: numbers that do not match, slow dashboards and refreshes, stale or provisional data, and how to communicate and fix them, with inline exercise numbers where a figure can be derived.

### Q1 ⭐⭐⭐ 🟢 Your dashboard shows 10,200 orders for last month and a colleague's SQL report shows 9,800 for the same month. What is the first thing you check, and in what order do you work through the rest?
**Asked at:** commonly asked (no company-specific report found); "dashboard says X, SQL says Y" is the lead theme in the prep question banks and blogs found (unverified).
**What the interviewer is checking:** Whether you compare definitions before touching data, and work from the cheapest check to the costliest.
**Say this in the interview:** "First I confirm we are both counting the same thing: same definition of an order, same dates, same filters. The gap is 400 orders, about 4%, so I will look for a rule that explains it before I blame the data."
**First, clarify / contain:** Ask for the colleague's query or filters, and write down my own. Do not change the dashboard or the SQL yet. Note the gap: 10,200 minus 9,800 is 400 orders (4.1% of the SQL figure, 3.9% of the dashboard figure; rounded to one decimal).
**What I would check, in order:**
1. Definition: is an "order" an order ID or a row? Are cancelled, returned or test orders in or out?
2. Date field and range: order date or ship date; last day of the month included or cut at midnight?
3. Time zone: UTC on one side, IST on the other can move orders across the month boundary.
4. Filters and security: region, channel or row-level security (rules that show each user only their rows) hiding rows from one side.
5. Freshness: was the dashboard refreshed after late orders landed, or the SQL run earlier?
6. Duplicates and joins: a join that repeats orders (a fan-out).
7. Only then, row-level comparison: list order IDs on each side and find the 400 that appear in one only (`EXCEPT` in SQL, or a lookup in Excel).
**If I find...:** a rule difference means agree one definition and document it. A join duplicate means fix the model. Missing orders on one side means a load or filter bug, so I fix and re-test.
**What I would tell the stakeholder:** "The two numbers differ by 400 orders. I am checking definitions and dates first; I will confirm the cause by end of day and show you the list of the 400."
**Prevent it next time:** One shared metric definition, written next to the number on the dashboard.
**Likely follow-ups:** 1) *Why not start with the order-ID comparison?* It is the slowest check and often unnecessary. 2) *Which is right?* Neither until definitions match.
**Common mistakes / traps:** Assuming SQL is automatically right; "fixing" the dashboard before knowing the cause; comparing numbers from different refresh times.

### Q2 ⭐⭐⭐ 🟢 What are the most common reasons two reports built on the same business data show different totals for the same KPI?
**Asked at:** commonly asked (no company-specific report found); reconciliation causes (definitions, time zones, filters, refresh timing) recur in the vendor blogs and question banks found (unverified).
**What the interviewer is checking:** That you have a mental checklist, ordered by how often each cause happens.
**Say this in the interview:** "Most of the time it is not bad data, it is different definitions: different date field, different filters, different time zone, or a different refresh time."
**Clarify first:** Which two reports, which KPI, what is the size of the gap? The decision supported is "which number do we trust and publish".
**Plan:**
1. Definition of the KPI: what is counted, and the denominator for a ratio.
2. Date logic: order date vs invoice date; fiscal vs calendar month.
3. Time zone: UTC vs IST moves late-evening orders to the next day.
4. Filters and status: cancelled, returned, test records, internal accounts.
5. Data source or layer: one report reads raw tables, the other a cleaned summary.
6. Refresh timing and late-arriving data: one report is a day older.
7. Model problems: join duplicates, rows lost by an inner join, row-level security.
8. Aggregation: average of averages vs total divided by total; distinct counts that do not add.
**Method choice and why:** Start with definition and dates because they are free to check; go to row-level comparison last.
**Pitfalls:** Several small causes can add up; explain each one in rupees or counts until the gap is zero.
**Deliverable:** A short reconciliation table: starting figure, each adjustment, ending figure, unexplained remainder.
**Likely follow-ups:** 1) *Which cause is most common?* In my experience definitions, but that is judgement, not a measured statistic. 2) *How do you stop it?* One governed metric definition.
**Common mistakes / traps:** Jumping to "data is wrong"; stopping after finding one cause without checking the gap closes fully.

### Q3 ⭐⭐⭐ 🟢 A stakeholder messages you, "Your dashboard is wrong." How do you respond in the first hour?
**Asked at:** commonly asked (no company-specific report found); stakeholder-disputes-a-number prompts appear in the question banks found, and the research notes a stakeholder-management round at Cognizant (unverified, from internal compilation).
**What the interviewer is checking:** Calm, curiosity, and a structured reply that neither defends nor panics.
**Say this in the interview:** "I thank them, ask what they expected to see and where, and promise a first update within the hour. I do not argue, and I do not change anything yet."
**First, clarify / contain:** Reply within minutes: "Thanks for flagging; can you send a screenshot, the filters you used, and the number you expected and where it comes from?" If the report is going to leadership soon, ask them not to forward it until I confirm.
**What I would check, in order:**
1. Reproduce their view with the same filters and date range.
2. Compare to their expected number: whose definition, which source, which date.
3. Check refresh status and last-updated time.
4. Check filters, row-level security and time zone for that user.
5. Spot-check a few records back to the source.
**If I find...:** Their expectation uses another definition: explain and document. A real bug: say so, fix, and tell everyone who saw the number. Cannot reproduce: ask for a screen share.
**What I would tell the stakeholder:** "I could reproduce it. The dashboard counts X while your sheet counts Y, which explains 80% of the gap; I am checking the rest and will update you by 3 pm."
**Prevent it next time:** Show definitions and refresh time on the page; keep a log of reported issues.
**Likely follow-ups:** 1) *What if they are simply wrong?* Show the reconciliation politely, not "you are wrong". 2) *What if you are wrong?* Own it quickly.
**Common mistakes / traps:** Getting defensive; silent fixes; no time-bound update.

### Q4 ⭐⭐⭐ 🟢 A dashboard that took 5 seconds to open now takes 40 seconds. What is the first step you take before changing anything?
**Asked at:** commonly asked (no company-specific report found); a Prepfully snippet says a Tableau slow-dashboard question was asked at Deloitte and Apple (anonymous, unverified).
**What the interviewer is checking:** That you measure before you tune, and ask what changed.
**Say this in the interview:** "Before changing anything I find out what changed and where the 40 seconds go: query, data load, or drawing visuals. I use the tool's performance recorder for that."
**First, clarify / contain:** Ask: since when, for everyone or some users, which page or filter. Do not delete visuals or rebuild the model yet. Take a baseline: 40 seconds now versus 5 seconds earlier, about 8 times slower.
**What I would check, in order:**
1. What changed: new visuals, a new data source, a bigger table, a changed filter, new users.
2. Record performance (Power BI Performance Analyzer, Tableau performance recording) and note the slowest visual.
3. Split the time: data query, calculation, rendering.
4. Check data volume growth and whether the source database is itself slow.
5. Check connection mode: extract (data copied into the tool) vs live query.
**If I find...:** One slow visual means simplify or aggregate it. A slow query means fix the source or add summary tables. Growing data means incremental load or aggregations.
**What I would tell the stakeholder:** "I can see it is slower; I am measuring where the time goes and will give you the cause and a fix plan by tomorrow."
**Prevent it next time:** Track open time as a monitored number; review performance when adding visuals.
**Likely follow-ups:** 1) *Quick win?* Fewer visuals on the first page. 2) *Is it the server?* Test the same query outside the dashboard.
**Common mistakes / traps:** Guessing and changing five things at once so you cannot tell what worked.

### Q5 ⭐⭐⭐ 🟢 What is a single source of truth for metrics, and why does it matter when several dashboards report the same KPI?
**Asked at:** commonly asked (no company-specific report found); the vendor blogs found recommend a shared semantic layer as the fix for mismatched reports (unverified).
**What the interviewer is checking:** That you understand governance, not just tools.
**Say this in the interview:** "It means each KPI is defined and calculated once, in one place, and every dashboard reads that one definition. Then two dashboards cannot disagree."
**Explain simply:**
- A "source of truth" is the one agreed place where a number is calculated, such as a shared data model or a governed table.
- Without it, each analyst writes their own "active employees" formula and the numbers drift.
- With it, a definition change is made once and flows to all dashboards.
- It also needs an owner, a written definition, and a version history.
**Mini-example:** HR headcount: one team counts contractors, another does not. Result: 1,248 vs 1,196 on two dashboards. A single governed "Active employees" measure, defined as payroll employees as of month end, removes the argument.
**Practice step:** List your top 5 KPIs and write one sentence each defining them: what is counted, what is excluded, the date used, the owner.
**Likely follow-ups:** 1) *Does it mean one dashboard?* No, one definition. 2) *Who owns it?* A named business owner plus a data team that implements it.
**Common mistakes / traps:** Thinking it is a tool purchase; defining it but not publishing it; no owner.

### Q6 ⭐⭐⭐ 🟢 What do you validate before you publish a new dashboard to senior leadership?
**Asked at:** commonly asked (no company-specific report found); a Dataford prompt on validating a dashboard before leadership appears in the sources (unverified).
**What the interviewer is checking:** A repeatable quality checklist, not "I look at it".
**Say this in the interview:** "I check numbers against a trusted source, definitions with the business owner, filters and totals, and I test it as the leader would use it."
**Clarify first:** Who the audience is, which decisions the dashboard supports, and who owns each metric.
**Plan:**
1. Totals tie to the source or Finance report for a closed period; keep the reconciliation note.
2. Metric definitions agreed and written, including the denominator of each ratio.
3. Spot-check 5 to 10 individual records end to end.
4. Test filters, slicers and drill-downs; confirm totals do not jump when filtered.
5. Check edge cases: nulls, duplicates, cancelled records, time zones, latest refresh.
6. Row-level security tested with a real user account.
7. Performance: opens in a few seconds on a normal laptop.
8. Labels, units, "data as of" date, and no misleading axes.
9. Peer review by a second analyst, then a preview with one friendly business user.
**Method choice and why:** Reconcile first; polish last.
**Pitfalls:** Validating only the latest month, only happy paths, or only as the developer.
**Deliverable:** A one-page validation sheet and a sign-off from the metric owner.
**Likely follow-ups:** 1) *What if it does not tie?* Do not publish; explain the gap. 2) *How long?* Proportional to risk.
**Common mistakes / traps:** Publishing with an unexplained gap; no owner sign-off.

### Q7 ⭐⭐⭐ 🟢 A dashboard card labelled "Orders" shows 12,500, while Finance says there were 9,000 orders. The orders table has one row per order line item.
Inline data: 12,500 rows in the table; 9,000 distinct order IDs; the card uses a plain row count.
Question: how many orders are over-counted, by what percentage, and what is the fix?
**Asked at:** commonly asked (no company-specific report found); a DEV Community post on row count vs distinct count on line-item tables matches this (unverified).
**What the interviewer is checking:** Whether you spot the grain (what one row represents) and use a distinct count.
**Say this in the interview:** "The table has one row per line item, so counting rows counts items, not orders. The fix is a distinct count of order ID."
**What the data shows:** Each order can have several line items, so the row count is higher than the order count.
**Working:**
1. Over-count = 12,500 minus 9,000 = 3,500.
2. As a percentage of true orders: 3,500 / 9,000 = 38.9%.
3. Extra rows as a share of all rows: 3,500 / 12,500 = 28.0%.
4. Average line items per order: 12,500 / 9,000 = 1.39.
**Result:** 3,500 orders over-counted, which is 38.9% above the true 9,000 (rounded to one decimal).
**Caveats / what else I would check:** Confirm the order ID is truly unique per order; check for duplicate rows (same line loaded twice); check whether Finance excludes cancelled orders.
**Next step / recommendation:** Change the card to a distinct count of order ID (`COUNT(DISTINCT order_id)` in SQL, `DISTINCTCOUNT` in Power BI), label the card "Orders (distinct)" and add a separate "Order lines" card.
**Likely follow-ups:** 1) *Revenue also wrong?* No, revenue sums line values correctly unless header-level amounts are repeated on each line. 2) *How prevent?* Name the grain in the table description.
**Common mistakes / traps:** Using row count as order count; removing rows to "fix" it.

### Q8 ⭐⭐⭐ 🟢 The sales head says the dashboard "has not updated since yesterday" at 10 am, but the scheduled refresh shows as successful. How do you find out what is going on and what do you tell them?
**Asked at:** commonly asked (no company-specific report found); freshness appears in the debugging order of the LinkedIn post and vendor blogs found (unverified).
**What the interviewer is checking:** That you know "refresh succeeded" does not mean "new data arrived".
**Say this in the interview:** "A successful refresh only means the dashboard pulled whatever was in the source. I check whether the source itself has new data."
**First, clarify / contain:** Ask which number or date they are looking at and what they expected. Do not trigger repeated manual refreshes yet.
**What I would check, in order:**
1. Last data date in the dashboard (max order date) vs last refresh time.
2. The source table: does it contain today's rows? If not, the upstream load failed or is late.
3. Refresh time vs source load time: the refresh may run before the nightly load finishes.
4. Filters on the report, such as a "last 1 day" filter or a cached page or browser view.
5. Time zone: "yesterday" in UTC may differ from IST.
6. Refresh history for partial or empty loads (success with zero rows).
**If I find...:** Source is late: tell the data engineering owner and re-run the refresh after the load. Schedule too early: move it after the load. Filter or cache: fix the view.
**What I would tell the stakeholder:** "The refresh ran, but the source system had not delivered today's data when it ran. I have asked the data team to reload; I will confirm by 11 am. Numbers on the page are as of yesterday evening."
**Prevent it next time:** Show "data as of" on the page; chain refresh after the load; alert on zero-row loads.
**Likely follow-ups:** 1) *Manual refresh now?* Only after the source has data. 2) *Who owns the fix?* The pipeline owner, with me raising it.
**Common mistakes / traps:** Re-refreshing blindly; saying "it is working" because the status is green.

### Q9 ⭐⭐⭐ 🟡 The HR dashboard shows 1,248 active employees on 30 September while the payroll report shows 1,196. How do you reconcile the two, and what do you do with any gap you cannot explain?
Inline data: HRIS includes 38 contractors who are not on payroll; 9 new joiners have a joining date of 1 October but were entered early with 30 September; payroll excludes all of these.
Question: how many employees remain unexplained?
**Asked at:** commonly asked (no company-specific report found); this HRIS vs payroll reconciliation is a gap-fill scenario (judgement, no source).
**What the interviewer is checking:** Structured reconciliation and honesty about the unexplained remainder.
**Say this in the interview:** "Gap is 52. Contractors explain 38 and early-entered joiners 9, so 5 remain unexplained, and I would list those 5 by employee ID and chase them."
**What the data shows:** HRIS counts more people than payroll, and two known rules explain most of it.
**Working:**
1. Gap: 1,248 minus 1,196 = 52.
2. Contractors: 38 (not on payroll).
3. Early joiners with wrong joining date: 9 (should start 1 October).
4. Explained: 38 + 9 = 47.
5. HRIS adjusted: 1,248 minus 47 = 1,201.
6. Unexplained: 1,201 minus 1,196 = 5.
**Result:** 5 employees remain unexplained (0.4% of 1,196, rounded).
**Caveats / what else I would check:** Compare employee IDs on both sides (a lookup or join) to list exactly who is in one only. Likely causes for 5: employees on unpaid leave or notice period, leavers not yet closed in HRIS, payroll holds, timing of status changes. Also decide the "active" definition (as of the date, and which statuses).
**Next step / recommendation:** Report 1,201 vs 1,196 with a reconciliation table, name the 5 as "under investigation" with an owner and a date, and ask HR operations to fix the 9 wrong joining dates. Do not force the gap closed by adjusting numbers.
**Likely follow-ups:** 1) *Which number do you publish?* State headcount definition: with or without contractors. 2) *Is 5 material?* Small, but unexplained gaps need a name.
**Common mistakes / traps:** Plugging the 5 into "other"; not saying contractors should be a separate category.

### Q10 ⭐⭐⭐ 🟡 The sales dashboard shows revenue of INR 482 lakh for October, while Finance reports INR 465 lakh. How do you narrow down the INR 17 lakh gap?
Inline data: the dashboard counts revenue on order date and includes cancelled orders worth INR 11 lakh; Finance counts revenue on invoice date.
Question: how much of the gap is still unexplained after cancelled orders, and what do you check next?
**Asked at:** commonly asked (no company-specific report found); a revenue-differs-from-Finance reconciliation is a standard theme in the sources (unverified).
**What the interviewer is checking:** Stepwise reconciliation, and knowing that order date vs invoice date creates timing differences.
**Say this in the interview:** "Cancelled orders explain INR 11 lakh, leaving INR 6 lakh. My next check is the date basis: orders placed in October but invoiced in November, and the reverse."
**What the data shows:** The dashboard is higher; cancellations explain about two thirds of the gap.
**Working:**
1. Gap: 482 minus 465 = 17 lakh.
2. Cancelled orders: 11 lakh.
3. Remaining: 17 minus 11 = 6 lakh.
4. Dashboard excluding cancelled: 482 minus 11 = 471 lakh versus Finance 465 lakh.
5. Unexplained is 6 / 465 = 1.3% of Finance revenue.
**Result:** INR 6 lakh unexplained after cancellations.
**Caveats / what else I would check:** (a) Order-date vs invoice-date timing: October orders invoiced in November, and September orders invoiced in October; this can go either way, so net effect unknown. (b) Returns and credit notes. (c) Taxes: GST included or excluded. (d) Discounts or currency. (e) Duplicates in the order table.
**Next step / recommendation:** Rebuild the dashboard figure on invoice date excluding cancellations and see if it ties; list orders by status and invoice month to put rupee figures on each bucket. Agree with Finance which basis is "revenue".
**Likely follow-ups:** 1) *If it still does not tie?* Order-level comparison by invoice number. 2) *Which do you publish?* Finance's definition for "revenue", with "bookings" shown separately.
**Common mistakes / traps:** Stopping at the cancelled orders; mixing taxes into one side.

### Q11 ⭐⭐⭐ 🟡 Daily order counts on your UTC-based dashboard differ from the operations team's IST report, but the monthly totals nearly match. Can you show the two daily figures are consistent?
Inline data: dashboard (UTC) shows 820 orders for 1 November. IST is UTC+5:30, so the IST day 1 November runs from 31 October 18:30 UTC to 1 November 18:30 UTC. Orders placed 31 October 18:30 to 23:59 UTC: 160. Orders placed 1 November 18:30 to 23:59 UTC: 75.
Question: what should the IST report show for 1 November?
**Asked at:** commonly asked (no company-specific report found); time zone is named in the debugging order of the LinkedIn post found (unverified).
**What the interviewer is checking:** Whether you can convert between day boundaries and explain why months nearly match.
**Say this in the interview:** "The IST report should show 905 for 1 November: take the UTC day, drop the last 5.5 hours, and add the late-evening orders from the day before."
**What the data shows:** Each IST day straddles two UTC days, so daily numbers shift but the month total barely moves.
**Working:**
1. UTC 1 November = 820 orders.
2. Remove UTC 1 Nov 18:30 to 23:59, which belongs to IST 2 November: 75.
3. 820 minus 75 = 745 orders (UTC 1 Nov 00:00 to 18:30).
4. Add UTC 31 Oct 18:30 to 23:59, which belongs to IST 1 November: 160.
5. 745 + 160 = 905.
**Result:** IST report should show 905 orders for 1 November, 85 more than the UTC dashboard (10.4% higher; rounded).
**Caveats / what else I would check:** Month totals differ only by the orders in the 5.5 hours at the month's edges (the 31 October evening piece moves into November in IST, and the 30 November evening piece moves into December). Check the exact time stamp field and that both sides use the same one. Daylight saving does not apply to IST.
**Next step / recommendation:** Store a local-time date column (IST) in the model, label the dashboard "IST" and agree one time zone for all reports.
**Likely follow-ups:** 1) *Why monthly nearly equal?* Only edge-of-month hours move. 2) *Which time zone to use?* The business operating zone.
**Common mistakes / traps:** Adding 5.5 hours the wrong way; mixing up which side's evening orders move.

### Q12 ⭐⭐⭐ 🟡 The dashboard's average order value is INR 1,250, but an analyst's Excel calculation gives INR 1,400 for the same two days. Which is right and why do they differ?
Inline data: Day A had 100 orders with an average of INR 1,000; Day B had 400 orders with an average of INR 1,500. The dashboard takes the average of the two daily averages.
**Asked at:** commonly asked (no company-specific report found); "average of averages" is a standard aggregation trap (unverified as a company question).
**What the interviewer is checking:** Weighted vs unweighted averages.
**Say this in the interview:** "INR 1,400 is right for the two-day average order value. The dashboard averaged two daily averages and ignored that Day B had four times the orders."
**What the data shows:** Day B has far more orders, so it should count for more.
**Working:**
1. Dashboard: (1,000 + 1,500) / 2 = INR 1,250.
2. Day A revenue: 100 x 1,000 = INR 1,00,000.
3. Day B revenue: 400 x 1,500 = INR 6,00,000.
4. Total revenue INR 7,00,000 over 500 orders.
5. True average: 7,00,000 / 500 = INR 1,400.
**Result:** INR 1,400 is right; the dashboard understates it by INR 150 (10.7% below; rounded).
**Caveats / what else I would check:** The same error appears with any ratio (conversion rate, attrition, margin) averaged across groups. Check the dashboard measure is total revenue divided by total orders, not an average of an average.
**Next step / recommendation:** Rewrite the measure as sum of revenue divided by count of orders, and test on a two-day case with known answers.
**Likely follow-ups:** 1) *When is a simple average fine?* When groups have equal size. 2) *In Excel?* `SUMPRODUCT` of orders and average, divided by total orders.
**Common mistakes / traps:** Averaging the average row in a pivot.

### Q13 ⭐⭐⭐ 🟡 A Power BI dataset refresh took 15 minutes last month and now takes 70 minutes. What do you check, in what order?
**Asked at:** commonly asked (no company-specific report found); "refresh slowing after a new step" appears in the Power BI question banks found, and the internal notes mention Power BI optimisation in Deloitte USI rounds (unverified).
**What the interviewer is checking:** Methodical diagnosis from "what changed" to the slow step.
**Say this in the interview:** "I ask what changed: more data, a new step, a slower source, or a clash with other jobs. Then I find which table's load time grew."
**First, clarify / contain:** Ask since when, whether it is gradual or sudden, and whether failures occur. Do not turn off steps yet. The refresh is about 4.7 times slower (70/15).
**What I would check, in order:**
1. Refresh history: sudden jump (a change) or gradual growth (data volume).
2. Which table or query takes the time (refresh log or tracing).
3. Recent changes to the model: new steps, merges, custom columns, new tables.
4. Row counts now vs last month.
5. Source side: slow database, locks, network, or a busy gateway (the connection to on-premises data).
6. Query folding: does the step still run in the database, or is the tool pulling all rows and doing it locally?
7. Overlapping schedules competing for the same source or capacity.
8. Full reload where incremental refresh (loading only recent data) could be used.
**If I find...:** A new heavy step: simplify or move it upstream. Data growth: incremental refresh. Source slowness: involve the database owner. Schedule clash: stagger.
**What I would tell the stakeholder:** "Refresh now takes 70 minutes because X; dashboards are still correct but later. Target fix: this week."
**Prevent it next time:** Track refresh duration; alert on a sharp rise.
**Likely follow-ups:** 1) *What is query folding?* Pushing transformations to the database. 2) *Quick win?* Remove unused columns.
**Common mistakes / traps:** Blaming Power BI without checking the source.

### Q14 ⭐⭐⭐ 🟡 A report is fast for most users but very slow for some users and on Monday mornings. How do you diagnose it?
**Asked at:** commonly asked (no company-specific report found); Deloitte USI rounds reportedly include Power BI optimisation and row-level security (internal compilation, unverified).
**What the interviewer is checking:** Splitting the problem into user-specific and time-specific causes.
**Say this in the interview:** "Two patterns, two questions. Slow for certain users points to what is different about them: security rules, location, device. Slow on Monday mornings points to load: many users at once or a refresh running."
**First, clarify / contain:** Ask which users, from where, which pages, what time exactly. Do not change the report yet.
**What I would check, in order:**
1. Common thread among slow users: row-level security role (rules limiting rows per user), region, network or VPN, device, browser.
2. Their role: complex security filters evaluated for every query.
3. The size of data each user sees: a user with all-region access loads the most.
4. Monday timing: scheduled refreshes of the dataset or source overlapping; weekly report peak at start of week; month-end loads.
5. Capacity or server utilisation at those times (shared capacity, source database load).
6. Record performance for a slow user and a fast user on the same page and compare.
**If I find...:** Heavy security rule: simplify. Peak load: stagger the refresh or add capacity. Network: involve IT. Source contention: move the refresh time.
**What I would tell the stakeholder:** "The slowness is linked to X; I will test a fix and confirm next week's Monday."
**Prevent it next time:** Load-test with the heaviest role; schedule refreshes away from peak usage.
**Likely follow-ups:** 1) *Can you reproduce it?* Use "view as role". 2) *Cache?* Pre-warm on Monday if supported (confirm with the tool's documentation).
**Common mistakes / traps:** Optimising visuals when the problem is capacity or security.

### Q15 ⭐⭐⭐ 🟡 A manager says, "This number was different when I looked last week for the same period." How do you find out why and explain it?
**Asked at:** commonly asked (no company-specific report found); snapshot vs event definitions appear in the DEV Community post found (unverified).
**What the interviewer is checking:** Whether you know why history changes: late data, restatements, logic changes.
**Say this in the interview:** "I ask what the number was and when they saw it. Then I check three things: late or corrected data, a change to the calculation, and a change in filters."
**First, clarify / contain:** Get the old number, screenshot and date. Do not say "it did not change".
**What I would check, in order:**
1. Late-arriving data: orders or hires recorded after the period closed.
2. Corrections: cancelled, returned or re-dated records, HRIS backdated entries.
3. Logic or definition change: a measure edited since last week (check version history).
4. Source changes: new load, reloaded history.
5. Filters or date range differences, including a "to date" window that moves.
6. Snapshot vs live: if only live data is stored, history cannot be recreated.
**If I find...:** Late data means it is normal; show the movement. A logic change means document and tell users. An unexpected change means treat as a bug.
**What I would tell the stakeholder:** "Last week's figure was 4,100 and today it is 4,180. 80 of that is late-entered orders for that period; the rest is a definition fix on 8 November."
**Prevent it next time:** Keep period-end snapshots for key numbers; show "as of" dates and a change log.
**Likely follow-ups:** 1) *Should closed periods change?* Ideally freeze them and show restatements separately. 2) *How do you prove it?* Compare snapshots.
**Common mistakes / traps:** No history to compare against; denying the change.

### Q16 ⭐⭐⭐ 🟡 The dashboard shows Sales department attrition of 18.0%, but the HR lead calculated 14.4% for the same quarter. Explain the gap and say which you would publish.
Inline data: 54 leavers; closing headcount 300; opening headcount 450. Dashboard divides leavers by closing headcount; HR divides by average of opening and closing headcount.
**Asked at:** commonly asked (no company-specific report found); the attrition denominator is a gap-fill HR scenario (judgement, no source).
**What the interviewer is checking:** That you know attrition needs the average headcount over the period.
**Say this in the interview:** "Same 54 leavers, different denominators. Closing headcount gives 18.0%, average headcount gives 14.4%. I would publish the average-headcount version and label it."
**What the data shows:** The department shrank from 450 to 300, so the denominator choice matters a lot.
**Working:**
1. Dashboard: 54 / 300 = 18.0%.
2. Average headcount: (450 + 300) / 2 = 375.
3. HR: 54 / 375 = 14.4%.
4. For reference, opening headcount: 54 / 450 = 12.0%.
**Result:** 18.0% vs 14.4%; the gap is 3.6 percentage points (a difference between two percentages, not 3.6%).
**Caveats / what else I would check:** A closing denominator overstates attrition when headcount fell; check that 54 leavers includes only the department and quarter and that transfers out are not counted as leavers. The 14.4% is a quarterly rate; to compare with an annual rate, state the period. The headcount fall from 450 to 300 is itself notable: a reorganisation or transfers?
**Next step / recommendation:** Publish 14.4% as "Quarterly attrition (leavers / average headcount)", show the formula, and align the dashboard measure with HR's.
**Likely follow-ups:** 1) *Why not opening?* Also used; the key is consistency. 2) *Annualise?* Only with a clear note.
**Common mistakes / traps:** Calling the difference 3.6%; using closing headcount.

### Q17 ⭐⭐⭐ 🟡 A region table shows distinct customers of 120, 95 and 110, but the grand total says 290, not 325. Is this a bug, and how would you explain it to a business user?
**Asked at:** commonly asked (no company-specific report found); non-additive distinct counts are a standard BI trap (unverified as a company question).
**What the interviewer is checking:** Understanding that distinct counts do not add.
**Say this in the interview:** "Not a bug. The three rows add to 325, but the total counts each customer once, and 35 customers bought in more than one region."
**What the data shows:** The grand total is lower than the sum of the rows because some customers appear in several regions.
**Working:**
1. Sum of rows: 120 + 95 + 110 = 325.
2. Grand total of distinct customers: 290.
3. Difference: 325 minus 290 = 35.
**Result:** At least 35 repeat appearances, so about 35 customers (or more, if some appear in three regions) are counted in more than one region.
**Caveats / what else I would check:** Verify by listing customers in two regions (a count of regions per customer greater than 1). Confirm no duplicate customer IDs for one person (that would push the other direction).
**Next step / recommendation:** Add a note under the table: "Totals are unique customers; customers who shop in several regions appear in each region." Plain-language example for the user: "Priya bought in Pune and Mumbai: she is one customer in the total, but one in each region row."
**Likely follow-ups:** 1) *Where else?* Distinct users, active employees by department when people transfer. 2) *Hide the total?* Better to explain.
**Common mistakes / traps:** "Fixing" the total to 325; not explaining.

### Q18 ⭐⭐⭐ 🟡 After you add a payments table to the model, the revenue total jumps. How do you confirm a join fan-out and what do you do?
Inline data: before the change, total revenue INR 5,00,000 across 500 orders. 200 of the orders (revenue INR 2,40,000) have two payment rows each (split payments).
Question: what total does the report now show and why?
**Asked at:** commonly asked (no company-specific report found); join duplication is a standard model-bug theme (unverified).
**What the interviewer is checking:** Understanding of one-to-many joins and how to prove duplication.
**Say this in the interview:** "Each split-payment order now appears twice, so its revenue is counted twice. The total becomes INR 7,40,000, not 5,00,000."
**What the data shows:** Orders are one row each; payments are one or two rows each, so joining repeats the order.
**Working:**
1. Orders with one payment: 500 minus 200 = 300, revenue 5,00,000 minus 2,40,000 = INR 2,60,000.
2. Split-payment orders: 200, revenue INR 2,40,000, now counted twice = INR 4,80,000.
3. New total: 2,60,000 + 4,80,000 = INR 7,40,000.
4. Rows after join: 300 + 400 = 700.
**Result:** INR 7,40,000, which is INR 2,40,000 (48%) too high.
**Caveats / what else I would check:** Confirm with a row count: orders table 500 vs joined 700. Check order ID appearing more than once in the joined result. Revenue to sum must come from the orders table; payments should be summed on their own.
**Next step / recommendation:** Do not join payments onto orders at row level. Keep it as a separate fact table related by order ID, aggregate payments to one row per order first, or sum revenue from orders only. Re-test: total must return to INR 5,00,000.
**Likely follow-ups:** 1) *Why not remove duplicates?* You would lose payment detail. 2) *What if you need payment type by revenue?* Allocate carefully; payment amounts sum to the order value.
**Common mistakes / traps:** Using distinct on revenue values; hiding the problem with a filter.

### Q19 ⭐⭐⭐ 🟡 A dashboard total is INR 46 lakh while the source system says INR 50 lakh for the same period, and you suspect rows are being dropped in the model. How do you confirm and fix it?
Inline data: 5,000 orders in the source; 4,600 find a matching customer in the customer master; the model uses an inner join to the master.
Question: what share of orders and what rupee amount is missing from the dashboard?
**Asked at:** commonly asked (no company-specific report found); lost rows from an inner join is a standard model-bug theme (unverified).
**What the interviewer is checking:** Understanding of inner vs left join and how to quantify lost rows.
**Say this in the interview:** "An inner join keeps only orders with a matching customer. 400 orders, 8%, are dropped, which is INR 4 lakh. I would switch to a left join and flag unmatched orders."
**What the data shows:** The gap in orders and in rupees is the same share, so the dropped orders look average in size.
**Working:**
1. Orders dropped: 5,000 minus 4,600 = 400.
2. Share of orders: 400 / 5,000 = 8.0%.
3. Rupee gap: 50 minus 46 = INR 4 lakh, which is 8.0% of 50 lakh.
4. Average order value: source 50 lakh / 5,000 = INR 1,000; dashboard 46 lakh / 4,600 = INR 1,000.
**Result:** 8% of orders (400) and INR 4 lakh missing.
**Caveats / what else I would check:** List the 400 order IDs with no customer match (`LEFT JOIN ... WHERE customer_id IS NULL`). Causes: customers not yet in the master, guest checkouts, key format mismatch (spaces, case, leading zeros), or deleted customers. Other filters could also lose rows; the equal averages are consistent with one cause but do not prove it.
**Next step / recommendation:** Use a left join (keep all orders), show unmatched orders as "Unknown customer", fix key cleaning, and add a reconciliation check: dashboard total vs source total, with an alert if they differ.
**Likely follow-ups:** 1) *Why not simply delete the join?* You need customer attributes. 2) *Right vs left?* Keep the table whose rows must all stay.
**Common mistakes / traps:** Ignoring unmatched keys; trusting "no errors" in refresh.

### Q20 ⭐⭐⭐ 🟡 A VP sends you an Excel sheet and says the dashboard must be changed to match it. How do you decide whose number is right?
**Asked at:** commonly asked (no company-specific report found); a stakeholder-disagrees-with-the-dashboard prompt appears on Dataford (unverified).
**What the interviewer is checking:** Evidence-based judgement and tact with seniors.
**Say this in the interview:** "I do not change the dashboard to match a sheet, and I do not dismiss the sheet either. I find out how each number is built and reconcile them with evidence."
**First, clarify / contain:** Thank the VP; ask where the sheet's numbers come from, who made it, and when. Do not edit the dashboard yet.
**What I would check, in order:**
1. Source of the Excel data: export from which system, on what date, with what filters.
2. Definition: what is counted, which dates, which statuses.
3. Trace both back to the source system for a sample of records.
4. Look for manual edits, hardcoded values, broken formulas or old exports in the sheet.
5. Check the dashboard against the source for the same period.
6. Build a reconciliation: start at one number, bridge step by step to the other.
**If I find...:** The sheet has an error or a different definition: explain and offer to show both. The dashboard has a bug: fix, communicate and credit the VP for the catch. Both are right under different definitions: agree one.
**What I would tell the stakeholder:** "Thanks for the sheet. I have traced both to the source. The difference of X comes from Y. I suggest we use Z definition; I will confirm by tomorrow."
**Prevent it next time:** Published definitions; one governed data source for everyone.
**Likely follow-ups:** 1) *What if the VP insists?* Escalate with the reconciliation to the metric owner. 2) *Can the dashboard show both?* Yes, if labelled.
**Common mistakes / traps:** Giving in to authority; or proving the VP wrong publicly.

### Q21 ⭐⭐⭐ 🟡 The dashboard shows a conversion rate of 4.2% while the funnel report shows 3.5% for the same week. What explains it and which would you present?
Inline data: 700 orders; 20,000 sessions; about 16,700 unique visitors. One report divides orders by sessions and the other by unique visitors.
Question: which report uses which denominator?
**Asked at:** commonly asked (no company-specific report found); a rate-denominator mismatch is a standard conversion-rate scenario (unverified).
**What the interviewer is checking:** That you test both denominators and pick one with reasons.
**Say this in the interview:** "The dashboard's 4.2% is orders divided by unique visitors; the funnel's 3.5% is orders divided by sessions. I would present sessions-based conversion as the standard and show the other labelled."
**What the data shows:** A smaller denominator gives a bigger rate; unique visitors are fewer than sessions because one visitor can have several sessions.
**Working:**
1. Orders / sessions: 700 / 20,000 = 3.5%.
2. Orders / unique visitors: 700 / 16,700 = 4.19%, about 4.2%.
3. Match: dashboard 4.2% uses visitors; funnel 3.5% uses sessions.
**Result:** Dashboard = unique visitors (4.2%); funnel = sessions (3.5%); the difference is 0.7 percentage points (rounded; 4.19% minus 3.50%).
**Caveats / what else I would check:** Visitors are approximate (cookies, devices), so the 16,700 is "about". Both figures may include repeat purchases by one visitor. Define whether an order counts as a converted session or visitor.
**Next step / recommendation:** Pick one headline conversion definition with the product owner (sessions is common for site performance; visitors for user-level questions; both are judgement calls), label the denominator on the card, and show the second as secondary.
**Likely follow-ups:** 1) *Which is better?* Depends on the question; consistency matters most. 2) *Trend?* Both should move together.
**Common mistakes / traps:** Saying 3.5% is wrong; unlabelled denominators.

### Q22 ⭐⭐⭐ 🟡 A number matches the source for most filter selections but is wrong for a few combinations, such as one region in one month. How do you isolate the problem quickly?
**Asked at:** commonly asked (no company-specific report found); inconsistent results under filters are a standard debugging prompt (unverified).
**What the interviewer is checking:** Systematic narrowing down, like a binary search.
**Say this in the interview:** "I reproduce one bad combination, then strip filters one at a time until it becomes correct. Whatever I removed last points to the cause."
**First, clarify / contain:** Get the exact filter set, the wrong value and the right value. Do not change the measure yet.
**What I would check, in order:**
1. Reproduce: same region, same month, same visual.
2. Remove other filters and slicers one by one; note when the number becomes right.
3. Test the same combination in a plain table, one dimension at a time (region only, month only).
4. Compare the underlying rows for that combination with the source (a SQL query with the same filters).
5. Look at the data for that slice: nulls, duplicates, a region name spelt differently, late-arriving data, a new category missing from the lookup.
6. Check row-level security and relationships: a many-to-many link or missing dimension row.
7. Check the measure: logic that behaves differently in certain contexts, such as divisions with zero or blank.
**If I find...:** Bad data in one slice: fix at source or cleaning. Measure bug: correct and re-test across combinations. Relationship issue: fix the model.
**What I would tell the stakeholder:** "The error affects only region X in month Y because of Z. Other views are correct. Fix by tomorrow."
**Prevent it next time:** Automated tests on sampled filter combinations; reconcile at the lowest level of detail.
**Likely follow-ups:** 1) *Could totals be right but slices wrong?* Yes, errors can cancel. 2) *Best tool?* A temporary detail table.
**Common mistakes / traps:** Checking only the grand total; changing the measure blindly.

### Q23 ⭐⭐⭐ 🔴 Finance and Sales each quote a different revenue figure for the same quarter, and each wants the executive dashboard to show theirs. How do you resolve it?
**Asked at:** commonly asked (no company-specific report found); governance and single-source-of-truth fixes are recommended in the vendor blogs found (unverified).
**What the interviewer is checking:** Neutral facilitation, definitions, and governance rather than picking a winner.
**Say this in the interview:** "Both can be right under different definitions. I would not pick a side; I would document both, name them differently, and get an executive owner to decide which one is called 'Revenue'."
**First, clarify / contain:** Ask each team for their definition, source and date basis, and the two figures. Do not change the dashboard for either side yet.
**What I would check, in order:**
1. Write down both definitions: sales usually counts bookings or orders by order date; Finance counts recognised revenue by invoice or accounting rules (typical, from memory, confirm locally).
2. Build a bridge from one figure to the other: cancellations, returns, timing, taxes, discounts, currency.
3. Quantify each bridge item in rupees until the unexplained remainder is small.
4. Check both against the source system.
5. Decide which uses an audited basis: Finance's recognised revenue is usually the reported figure.
**If I find...:** Differences are definitions: show both with distinct names (for example "Bookings" and "Recognised revenue") and one bridge. A real error: fix and inform both teams. A dispute that persists: escalate to the CFO or data governance owner for a decision.
**What I would tell the stakeholder:** "Sales' INR X and Finance's INR Y are both correct for their definitions; the gap of Z is explained by A, B and C. I propose the dashboard headline 'Revenue' follows Finance and 'Bookings' follows Sales; I need a decision from [owner] by Friday."
**Prevent it next time:** A metric dictionary with owners and a change process; both numbers read from one governed model.
**Likely follow-ups:** 1) *Who decides?* A named executive owner, not the analyst. 2) *Show both on one page?* Yes, with a bridge.
**Common mistakes / traps:** Taking sides; using one word for two measures; deciding alone without sign-off.

### Q24 ⭐⭐⭐ 🔴 At 8 am you find one of three source systems failed overnight, so the executive dashboard is missing about 20% of the data, and the CEO reviews it at 9 am. What do you do?
**Asked at:** commonly asked (no company-specific report found); the "stale or incomplete data before a leadership review" theme appears across dashboard question banks (unverified).
**What the interviewer is checking:** Whether you protect the CEO from a silently wrong number, stay calm, and communicate before fixing.
**Say this in the interview:** "I would not let an incomplete number go out unlabelled. In the first 10 minutes I tell the owner of the meeting what is missing, then I either get the data in or put a clear warning on the page."

**First, clarify / contain:** Within minutes, confirm which of the three systems failed and which numbers it feeds (for example, one region or one product line). Do not quietly edit the dashboard or re-run everything blindly. Tell my manager and the CEO's office now, not at 8:55.
**What I would check, in order:**
1. Which system failed, and why (job error, expired login, source outage); is it fixable within the hour?
2. Which tiles and filters are affected; is the missing 20% spread evenly or concentrated (one region), because that decides how misleading the total is?
3. Can I load the missing data manually (a backup extract or a re-run of just that source)?
4. After any fix, reconcile totals against last known good numbers and the source system's own count.
**If I find...:**
- Fix is possible before 9: run it, reconcile, and tell the CEO's office it was delayed and is now complete.
- Fix is not possible: add a visible banner ("Source X missing; totals understate by about 20%, data as of yesterday 11 pm") or show the last complete day's snapshot, clearly dated.
- The missing share is concentrated in one region: say which region so nobody draws conclusions about it.
**What I would tell the stakeholder:** "One of our three source systems failed overnight. Today's dashboard is missing roughly 20% of the data. I am working on loading it; my next update is at 8:40. If it is not ready by 9, I will mark the page as incomplete and give you the last complete figures, dated."
**Prevent it next time:** Add a data completeness check (row counts per source versus yesterday) that blocks or flags the dashboard automatically, plus failure alerts to my phone and a standby owner.
**Likely follow-ups:** 1) *Would you ever pause the dashboard?* If a wrong number could drive a decision and I cannot label it, yes, a "data not ready" page beats a confident wrong one. 2) *Who owns the source fix?* The source system or IT team; I own the communication and the dashboard.
**Common mistakes / traps:** Scaling up the 80% to "estimate" 100% without saying so; staying silent hoping it fixes itself; telling the CEO only after the meeting.

### Q25 ⭐⭐⭐ 🔴 You discover that a number you sent to leadership last week was wrong and decisions may already have been taken on it. What do you do, step by step?
**Asked at:** commonly asked (no company-specific report found); an integrity and ownership question.
**What the interviewer is checking:** Honesty, speed, and whether you quantify impact instead of panicking or hiding the error.
**Say this in the interview:** "I own it and tell my manager immediately, before I have the full fix. Then I size the error, find which decisions used it, and send one clear correction."

**First, clarify / contain:** Stop sending or reusing the wrong number. Re-check that it really is wrong (not my new calculation being wrong). Tell my manager the same day, before finishing the analysis.
**What I would check, in order:**
1. Reproduce the error and find the root cause (wrong filter, double counting, wrong date range, stale data).
2. Compute the correct number and the size of the gap (absolute and percentage).
3. List who received it and which decisions or documents used it (budget, hiring plan, a board slide).
4. Judge materiality: would the decision change if the number were right?
**If I find...:**
- The decision would not change: send a short correction note and update the source.
- The decision would change or is already acted on: raise it with my manager and the decision owner right away, so they can pause or reverse.
- Others were affected by the same bug: check every other report that uses the same logic.
**What I would tell the stakeholder:** "I found an error in the figure I sent on [date]. It said X; the correct figure is Y (difference Z). It came from [plain cause]. The decision on [topic] may be affected, and here is how. I have fixed the source and added a check. I am available today to walk through it."
**Prevent it next time:** A peer review or reconciliation before sending numbers to leadership, a written definition of each metric, and a log of what was sent and when.
**Likely follow-ups:** 1) *Do you tell them before you know the cause?* Yes, tell them there is a possible error now and give the cause later. 2) *What if no one noticed?* I still correct it; hidden errors cost more later.
**Common mistakes / traps:** Quietly fixing the dashboard without telling people who already used the old number; blaming the data or a colleague; sending a long apology without the corrected figure and impact.

### Q26 ⭐⭐⭐ 🔴 A Power BI report on a table with about 200 million rows takes 3 minutes to open and the business wants it under 10 seconds. What is your plan?
**Asked at:** commonly asked (no company-specific report found); Power BI scenario question banks list large-table and aggregation themes, and Deloitte USI reports mention Power BI optimisation (anonymous, unverified).
**What the interviewer is checking:** Whether you diagnose before tuning and know the main levers: less data, a lighter model, smarter visuals.
**Say this in the interview:** "I would measure first to see whether the time goes to the data query or to the visuals, then cut the data volume, then fix the model and the page."

**Clarify first:** Which page is slow, how many users, how fresh must the data be, and what questions do people actually ask (daily totals, or individual transactions)? That tells me how much detail we can drop.
**Plan:**
1. Measure: use Performance Analyzer (a built-in Power BI tool that times every visual) to separate query time from render time.
2. Reduce rows and columns: remove unused columns, filter old history if the business does not use it, and pre-summarise in the source (for example one row per day per product instead of per transaction).
3. Use aggregation tables (small summary tables that answer most questions) with the 200 million row detail table kept for drill-through only.
4. Fix the model: a star schema (one fact table linked to small lookup tables), integer keys, no unneeded high-cardinality columns such as timestamps to the second (split date and time).
5. Page design: fewer visuals per page, avoid heavy slicers, review slow DAX measures.
6. Re-measure against the 10-second target and agree what is acceptable.
**Method choice and why:** Import mode with aggregations first; DirectQuery only if freshness demands it (from memory, unverified: Power BI import mode is generally faster, but confirm size limits with your admin).
**Pitfalls:** Tuning visuals when the model is the problem; promising 10 seconds before measuring; removing detail that someone needs.
**Deliverable:** A before/after timing table, the list of changes, and a note on what detail moved to drill-through.
**Likely follow-ups:** 1) *Where is the biggest win usually?* Reducing the data the report has to scan. 2) *Is 10 seconds realistic?* Often, with aggregations, but I would test.
**Common mistakes / traps:** Buying more capacity first; adding more visuals; ignoring the data model.

### Q27 ⭐⭐ 🟢 What is the difference between import (extract) and live/DirectQuery connections for a business dashboard, and when would you choose each?
**Asked at:** commonly asked (no company-specific report found); Power BI and Tableau question banks list import versus live (unverified).
**What the interviewer is checking:** That you understand the speed versus freshness trade-off, not just the names.
**Say this in the interview:** "Import copies the data into the dashboard tool, so it is fast but only as fresh as the last refresh. Live or DirectQuery asks the source each time, so it is fresher but slower and loads the source."

**Explain simply:**
- **Import / extract:** data is copied and compressed into the tool on a schedule. Quick to open, works offline from the source, but shows data as of the last refresh. Size limits apply (confirm with your admin).
- **Live / DirectQuery:** nothing is copied; every click sends a query to the source database. Always current, but each visual waits on the database and many users add load to it.
**Worked mini-example:** A daily sales report viewed by 200 managers at 9 am. Import: one refresh at 6 am, then everyone reads the stored copy. DirectQuery: 200 people times ten visuals sends thousands of queries to the sales database at 9 am.
**When I choose which:** Import for most management dashboards (daily or hourly is fine). DirectQuery or live for near-real-time needs, data too large to copy, or data that must stay in a governed source, with a fast, indexed source and a limit on visuals.
**Practice step:** Open any report, check its connection mode, note its last refresh time, and ask what happens if the source is slow.
**Likely follow-ups:** 1) *Is there a middle option?* Yes, mixed modes: aggregated summaries imported, detail queried live. 2) *Which is better for security?* Neither automatically; row-level rules work in both.
**Common mistakes / traps:** Saying "live is always better because it is real-time"; forgetting that source database load matters.

### Q28 ⭐⭐ 🟢 What is incremental refresh and when would you use it for a daily sales report?
**Asked at:** commonly asked (no company-specific report found); a Power BI scenario-bank theme (unverified).
**What the interviewer is checking:** That you know it refreshes only new or changed data and can say when it is worth it.
**Say this in the interview:** "Instead of reloading all history every day, it reloads only a recent window, say the last 7 days, and keeps the older data as is."

**Explain simply:**
- Normal refresh: reload every row each time.
- Incremental refresh: split the data into time slices; keep old slices untouched and refresh only the recent ones, which can still change (late orders, returns, corrections).
**Worked mini-example:** Three years of daily sales is 1,095 days. Refreshing a 7-day window touches 7 of 1,095 days, about 0.6% of the rows, instead of all of them.
**When I would use it:** When history is large, old rows do not change, the source has a reliable date column to filter on, and the full refresh is slow or hits timeouts. For a small table that refreshes in two minutes, the added setup is not worth it.
**Practice step:** In a sample dataset, define two parameters (start and end date), filter the date column on them, and set "store last 3 years, refresh last 7 days" (settings names from memory, unverified; check the tool version you use).
**Likely follow-ups:** 1) *What if an old order is corrected months later?* Widen the refresh window or run an occasional full refresh. 2) *Does the first refresh still take long?* Yes, the first load builds all history.
**Common mistakes / traps:** Using it when the source date column is unreliable; setting the window too short so late changes are missed.

### Q29 ⭐⭐ 🟢 How do you decide how often a dashboard should refresh?
**Asked at:** commonly asked (no company-specific report found); a design and refresh-architecture theme in question banks (unverified).
**What the interviewer is checking:** That you tie refresh frequency to the decision it supports, not to "as often as possible".
**Say this in the interview:** "I ask how fast the decision changes and how fast the source updates, then pick the slowest refresh that still supports the decision."

**Explain simply:** Three things set the answer:
- **Decision speed:** a monthly attrition review needs a daily refresh at most; a call-centre floor manager needs minutes.
- **Source update speed:** refreshing hourly from a source that updates nightly adds cost, no new information.
- **Cost and load:** each refresh uses capacity and can slow the source system.
**Worked mini-example:** Payroll dashboard: payroll runs monthly, so refresh daily after the HRIS (human resources information system) export. Hiring funnel: recruiters act daily, so a refresh each morning. Live attendance at a plant gate: every 15 minutes, if the source allows.
**How I decide:** Ask the users, check the source schedule, test the load, and show the "data as of" time on the page so nobody assumes it is live.
**Practice step:** For three dashboards you know, write the decision, the source refresh time and the refresh you would choose.
**Likely follow-ups:** 1) *Why not refresh every minute?* Cost, source load and no extra value if decisions are daily. 2) *Who agrees the schedule?* The business owner with IT.
**Common mistakes / traps:** Choosing real-time by default; refreshing before the upstream data is ready (see Q38).

### Q30 ⭐⭐ 🟢 A dashboard card shows "Attrition +20%", and an executive reads it as attrition being 20%. How would you fix the presentation?
Inline data: last quarter attrition was 10% and this quarter it is 12%.
Question: what are the two correct ways to state the change?
**Asked at:** commonly asked (no company-specific report found); a percentage versus percentage-point trap (gap-fill, judgement).
**What the interviewer is checking:** Whether you separate a rate from a change in that rate.
**Say this in the interview:** "I would show the level first, 12%, then the change as either +2 percentage points or +20% relative, labelled clearly."

**What the data shows:** Attrition went from 10% to 12%. The card showed the relative change, which looks like a level.
**Working:**
1. Percentage-point change = 12% - 10% = 2 percentage points (pp).
2. Relative change = (12 - 10) / 10 = 0.20 = 20%.
**Result:** "Attrition rose by 2 percentage points (10% to 12%)" or "Attrition rose 20% relative to last quarter (from 10% to 12%)". The attrition rate itself is 12%.
**Caveats / what else I would check:** Small headcounts make rates jumpy (2 points on 100 people is 2 leavers); also check the rate definition is the same both quarters (quarterly versus annualised).
**Next step / recommendation:** Redesign the card: big number "12%", small line "up 2 pp vs last quarter (10%)", tooltip with the definition. Ask three executives what they read before and after.
**Likely follow-ups:** 1) *Which do you prefer?* Percentage points for rates, since it avoids confusion. 2) *If it went 10% to 5%?* Down 5 pp, or down 50% relative.
**Common mistakes / traps:** Writing "+20%" with no base; mixing "percent" and "points".

### Q31 ⭐⭐ 🟢 A stakeholder objects that the percentages in a pie chart add up to 99%. How do you handle it?
Inline data: 121 employees split across three locations as 55, 33 and 33, shown rounded to whole percentages.
**Asked at:** commonly asked (no company-specific report found); a rounding trap (gap-fill, judgement).
**What the interviewer is checking:** That you can explain rounding calmly and offer a fix without altering the data.
**Say this in the interview:** "The data is right; each slice is rounded separately. I would explain it in one line and show one decimal place or a footnote."

**What the data shows:** Three locations, 121 employees.
**Working:**
1. 55 / 121 = 45.45%, which rounds to 45%.
2. 33 / 121 = 27.27%, which rounds to 27%; same for the second 33.
3. Sum of rounded values = 45 + 27 + 27 = 99%. Sum of unrounded = 100%.
**Result:** The extra 1% was lost to rounding down three times (0.45 + 0.27 + 0.27 = about 1 point dropped in total).
**Caveats / what else I would check:** Do not force one slice to 46% without saying so; hand-editing numbers breaks trust. Another option is to show headcounts (55, 33, 33) next to the percentages, and perhaps use a bar chart instead of a pie, which is easier to compare.
**Next step / recommendation:** Add a footnote "percentages may not sum to 100% due to rounding", or show one decimal (45.5%, 27.3%, 27.3% = 100.1%, which still differs slightly). Showing the counts removes the argument.
**Likely follow-ups:** 1) *Would you adjust the largest slice?* Only with a disclosed footnote. 2) *Is a pie suitable here?* It is fine for three parts, but a bar chart reads better.
**Common mistakes / traps:** Telling the stakeholder the data is wrong; silently plugging 1% into one slice.

### Q32 ⭐⭐ 🟢 The dashboard shows year-to-date revenue on a calendar-year basis, but the company's financial year runs April to March. How do you show the right figure?
Inline data: January to March revenue INR 24 lakh in total; April to October revenue INR 10 lakh per month.
Question: what are calendar YTD and financial-year YTD at the end of October?
**Asked at:** commonly asked (no company-specific report found); a fiscal-year definitional trap (gap-fill, judgement).
**What the interviewer is checking:** That you know YTD depends on the year definition and can fix it at the source.
**Say this in the interview:** "I would build the date table with a financial year column starting in April and make YTD follow it, then label the card 'FY YTD'."

**What the data shows:** Two different start dates give two figures for the same data.
**Working:**
1. April to October is 7 months (Apr, May, Jun, Jul, Aug, Sep, Oct), so April to October revenue = 7 x 10 = INR 70 lakh.
2. Calendar YTD = Jan to Mar (24 lakh) + Apr to Oct (70 lakh) = INR 94 lakh.
3. Financial-year YTD = INR 70 lakh (April to October only).
**Result:** Calendar YTD INR 94 lakh; FY YTD INR 70 lakh. The dashboard overstates the FY figure by INR 24 lakh (the Jan to Mar revenue belongs to last financial year).
**Caveats / what else I would check:** Compare with the same period last FY (April to October); confirm the company's year start with Finance; the Q1 to Q4 labels also shift (April to June is FY Q1).
**Next step / recommendation:** Add FY start month to the date table (in Power BI, the year-end date can be set to 31 March in the YTD function, from memory, unverified); rename the card "FY YTD (Apr-Oct)"; get Finance to sign off the number.
**Likely follow-ups:** 1) *How do you name FY?* Agree a rule such as FY26 = April 2025 to March 2026 (or the other way), and document it. 2) *What about weeks?* Needs its own agreed rule.
**Common mistakes / traps:** Counting from 1 January; mislabelling the card as just "YTD".

### Q33 ⭐⭐ 🟢 How do you communicate a change in a KPI definition on a live dashboard so users are not confused?
**Asked at:** commonly asked (no company-specific report found); a trust and governance theme in question banks (unverified).
**What the interviewer is checking:** Change management: notice, labelling, history and a single place for definitions.
**Say this in the interview:** "I announce it before it goes live, show the old and new values side by side for a while, and keep a visible change log on the dashboard."

**Explain simply:**
- **Before:** get the owner to approve the change; tell users what changes, why, and from which date.
- **On go-live:** show the new definition in a tooltip or info page, and mark the date on trend charts so people see why a line moves.
- **Parallel run:** for a few weeks show old and new values together so the gap is understood.
- **After:** restate history under the new definition (or clearly mark it as not comparable), and update the definition document.
**Worked mini-example:** Attrition changes from "all leavers" to "voluntary leavers only." The rate drops from 12% to 9%. Without notice, it looks as if retention improved; with a note it is clear the definition changed.
**Practice step:** Write a three-line change notice: what changed, why, effect on the number.
**Likely follow-ups:** 1) *Do you rewrite history?* Preferably yes, so trends compare like with like; if not, mark the break. 2) *Who approves?* The metric owner.
**Common mistakes / traps:** Changing quietly; changing the logic without version notes; breaking trends.

### Q34 ⭐⭐ 🟡 The attendance dashboard shows an employee at 61.3% attendance, but the employee expects a much higher figure. Find the cause and give the right figure.
Inline data: October has 31 calendar days and 22 working days. The employee was present 19 days, on approved leave 2 days and absent 1 day. The dashboard divides present days by calendar days.
**Asked at:** commonly asked (no company-specific report found); an attendance denominator trap (gap-fill, judgement).
**What the interviewer is checking:** That you check the denominator and the definition, not just the arithmetic.
**Say this in the interview:** "The dashboard divides by calendar days, which includes weekends and holidays. The right base is working days."

**What the data shows:** The cause is the denominator.
**Working:**
1. Dashboard: 19 / 31 = 61.3%.
2. Present over working days: 19 / 22 = 86.4%.
3. Counting approved leave as attended: (19 + 2) / 22 = 21 / 22 = 95.5%.
**Result:** Correct figure is 86.4% (presence rate), or 95.5% if the company counts approved leave as attended. Check: 19 + 2 + 1 = 22, so the days reconcile.
**Caveats / what else I would check:** Which definition HR uses (presence versus attendance with leave), holidays and weekly offs for this employee's shift pattern, half-days, and whether the employee joined mid-month.
**Next step / recommendation:** Change the formula to use the employee's working-day calendar, publish both measures with names ("Presence %" and "Attendance incl. approved leave %"), and tell the employee and manager.
**Likely follow-ups:** 1) *Which figure goes in a performance review?* The one the policy defines. 2) *Do you tell other users?* Yes, other employees are also understated.
**Common mistakes / traps:** Fixing one employee manually; changing the formula without saying which definition applies.

### Q35 ⭐⭐ 🟡 Your dashboard shows a gross margin of 31.5% while Finance reports 29.8%. How do you find what explains the difference?
Inline data: revenue INR 200 lakh. Dashboard COGS is INR 137 lakh. Finance also includes INR 3.4 lakh of freight in COGS.
Question: show that the freight explains the gap.
**Asked at:** commonly asked (no company-specific report found); the "two numbers, same KPI" family is the most common dashboard theme across question banks (unverified).
**What the interviewer is checking:** That you reconcile with a bridge instead of picking a winner.
**Say this in the interview:** "I would compare definitions line by line. Here Finance includes freight in cost of goods sold, and that alone accounts for the 1.7 point gap."

**What the data shows:** Same revenue, different cost definitions.
**Working:**
1. Dashboard gross profit = 200 - 137 = INR 63 lakh; margin = 63 / 200 = 31.5%.
2. Finance COGS = 137 + 3.4 = INR 140.4 lakh; gross profit = 59.6 lakh; margin = 59.6 / 200 = 29.8%.
3. Gap = 31.5% - 29.8% = 1.7 percentage points; freight alone is 3.4 / 200 = 1.7 points.
**Result:** Freight explains the full gap (1.7 percentage points, INR 3.4 lakh).
**Caveats / what else I would check:** Timing (month cut-off), returns, discounts, currency, and whether the dashboard and Finance use the same revenue (net or gross of tax).
**Next step / recommendation:** Agree with Finance which margin the dashboard should show; label the other one, or show both ("Gross margin" and "Margin before freight"). Document the definition.
**Likely follow-ups:** 1) *Who is right?* Neither; they use different definitions, and the business must choose one. 2) *What if the bridge leaves a gap?* Keep drilling: dates, filters, returns.
**Common mistakes / traps:** Assuming one team made an error; changing the dashboard without Finance agreement.

### Q36 ⭐⭐ 🟡 On 20 November, the dashboard shows month-to-date revenue 28% below last November and leadership is worried. Is the comparison fair?
Inline data: MTD revenue to 20 November is INR 3.6 crore. Last November in full was INR 5.0 crore, of which INR 3.4 crore fell between 1 and 20 November.
Question: what is the like-for-like change?
**Asked at:** commonly asked (no company-specific report found); a partial-period comparison trap (gap-fill, judgement).
**What the interviewer is checking:** That you compare the same days, not a part month against a full month.
**Say this in the interview:** "No, it is not fair: it compares 20 days with 30. Like for like, revenue is up about 6%."

**What the data shows:** This year's 20 days were set against last year's 30.
**Working:**
1. Dashboard comparison: 3.6 vs 5.0 gives (3.6 - 5.0) / 5.0 = -28%.
2. Like-for-like: this year 1 to 20 November INR 3.6 crore versus last year 1 to 20 November INR 3.4 crore.
3. Change = (3.6 - 3.4) / 3.4 = 0.0588, or +5.9%.
**Result:** Like-for-like growth is +5.9% (rounded to one decimal), not -28%.
**Caveats / what else I would check:** Number of weekdays and weekends in each 20-day window, a festival shift between years (Diwali moves), late-posting data in recent days, and returns.
**Next step / recommendation:** Change the YoY (year on year) comparison to "same days last year", and add the label "MTD to 20 Nov vs 1 to 20 Nov last year". Tell leadership today.
**Likely follow-ups:** 1) *How do you forecast the full month?* A run-rate or last year's remaining share, labelled as an estimate. 2) *Does 5.9% mean we are fine?* Check the calendar effects first.
**Common mistakes / traps:** Comparing MTD with the full prior month; reacting to a 28% fall before checking.

### Q37 ⭐⭐ 🟡 The revenue by region chart shows an "Unknown" bucket. What do you do about it and what do you tell the stakeholder?
Inline data: North INR 40 lakh, South INR 35 lakh, East INR 13 lakh, Unknown INR 12 lakh.
Question: what is North's share with and without the Unknown bucket?
**Asked at:** commonly asked (no company-specific report found); a data-quality theme (gap-fill, judgement).
**What the interviewer is checking:** That you find the cause of the missing region, and show shares with the gap stated.
**Say this in the interview:** "Unknown is 12% of revenue, too large to hide. I would find why those rows have no region, fix the mapping, and meanwhile show it as its own bar."

**What the data shows:** Total revenue is INR 100 lakh, and 12 lakh has no region.
**Working:**
1. Total with Unknown = 40 + 35 + 13 + 12 = INR 100 lakh.
2. North's share with Unknown = 40 / 100 = 40.0%.
3. Total without Unknown = 88 lakh; North's share = 40 / 88 = 45.5%.
4. Unknown share = 12 / 100 = 12%.
**Result:** North is 40.0% of all revenue, or 45.5% of revenue with a known region. The truth lies between, depending on where Unknown belongs.
**Caveats / what else I would check:** Why region is missing (new store or pin code not in the mapping, blank state, test accounts, a join that fails), whether it is one source or one customer type, and whether it is growing.
**Next step / recommendation:** Trace the Unknown rows; fix the mapping table; backfill history; add a data-quality check that alerts when Unknown exceeds, say, 2%. Until then keep the bar visible with a note.
**What I would tell the stakeholder:** "12% of revenue (INR 12 lakh) has no region tag. Rankings of regions are not yet reliable. I will fix the mapping by [date]; meanwhile North is between 40% and 45.5%."
**Likely follow-ups:** 1) *Would you spread Unknown proportionally?* Not without saying so. 2) *Delete the bucket?* Never; the revenue is real.
**Common mistakes / traps:** Hiding the bucket so the chart looks clean; using shares without stating the denominator.

### Q38 ⭐⭐ 🟡 Users see yesterday's numbers every morning even though refreshes succeed. How do you find the problem?
Inline data: source extract finishes 02:40; ETL runs 03:00 to 04:10; dataset refresh is scheduled for 04:00; report is viewed from 08:00.
Question: how long is the overlap, and what would you change?
**Asked at:** commonly asked (no company-specific report found); a refresh-chain timing theme (gap-fill, judgement).
**What the interviewer is checking:** That you trace the full chain (source, ETL, dataset, report) and compare timestamps.
**Say this in the interview:** "The dataset refresh starts at 04:00, 10 minutes before the ETL finishes at 04:10, so it reads the old tables. Refresh succeeds, but with yesterday's data."

**What the data shows:** The ETL (extract, transform, load: the job that cleans and loads data into the reporting tables) runs 70 minutes and ends after the refresh starts.
**Working:**
1. ETL duration = 03:00 to 04:10 = 70 minutes.
2. Refresh starts 04:00, ETL ends 04:10, so overlap = 10 minutes.
3. The refresh therefore reads tables not yet fully updated, so it picks up yesterday's data (or partial data).
4. The source extract finished at 02:40, so the source is not the issue (20 minutes before ETL starts).
**Result:** 10-minute overlap; the refresh is early.
**Caveats / what else I would check:** Confirm with the last-refresh timestamps and the maximum date in the dataset; ETL duration may vary (a long day could push past 04:30), time zone settings, and a cached report or a stale browser view.
**Next step / recommendation:** Trigger the refresh when the ETL finishes (a dependency or pipeline trigger) rather than at a fixed time; if only a schedule is possible, move it to about 04:30 to leave buffer. Add a "data as of" date on the report and an alert if the max date is not yesterday.
**Likely follow-ups:** 1) *Why not 04:11?* ETL time varies; a buffer or a completion trigger is safer. 2) *How do you prove it?* Compare the dataset's latest date with the ETL log time.
**Common mistakes / traps:** Re-running refresh repeatedly; blaming users' browser cache first; assuming "success" means "complete".

### Q39 ⭐⭐ 🟡 Your dataset has about 18 million rows covering three years (1,095 days), and a full daily refresh takes 60 minutes, though only the last 7 days of data ever change. How would incremental refresh help, and roughly how much data would each refresh process?
Inline data: assume rows are spread evenly across days.
**Asked at:** commonly asked (no company-specific report found); incremental refresh appears in Power BI question banks (unverified).
**What the interviewer is checking:** That you can estimate the saving and state its limits.
**Say this in the interview:** "Each refresh would process about 115,000 rows instead of 18 million, around 0.6%, so a 60-minute load could drop to a few minutes, subject to fixed overheads."

**What the data shows:** 99% of the data never changes but is reloaded every day.
**Working:**
1. Rows per day = 18,000,000 / 1,095 = about 16,438.
2. Rows in a 7-day window = 7 x 16,438 = about 115,068.
3. Share of the data = 115,068 / 18,000,000 = 0.64%.
4. If time scaled with rows: 60 minutes x 0.64% = about 0.4 minutes (roughly 23 seconds).
**Result:** About 115,000 rows (0.6% of the data) per refresh; in theory under a minute, in practice a few minutes after fixed overheads (connection, partition handling).
**Caveats / what else I would check:** Rows are not truly even (weekends, sales days); the first refresh still loads everything; late corrections older than 7 days would be missed, so choose the window by looking at how late changes arrive; the source needs a reliable date column.
**Next step / recommendation:** Set up "keep 3 years, refresh the last 7 days" with the date filter pushed to the source (from memory, unverified: check the folding requirement in your tool), and monitor the refresh time and row count for two weeks. Optionally run a full refresh monthly.
**Likely follow-ups:** 1) *What if changes can go back 30 days?* Use a 30-day window; still about 2.7% of rows. 2) *What if the source cannot filter by date?* The saving shrinks, so fix the source query first.
**Common mistakes / traps:** Promising a linear saving; choosing a window shorter than the true change period.

### Q40 ⭐⭐ 🟡 A dashboard page has 24 visuals and loads in 28 seconds; the target is 5 seconds. What do you do?
Inline data: in this exercise load time is the sum of visual times. Three visuals take 20 seconds in total; the other 21 take 8 seconds in total. After tuning, the three slow visuals take 2 seconds in total.
Question: what is the load time now, and what else must you do?
**Asked at:** commonly asked (no company-specific report found); Tableau and Power BI slow-dashboard pages list performance recording, fewer visuals and heavy filters; one prep-site snippet attributes a Tableau loading question to candidates at Deloitte and Apple (anonymous, unverified).
**What the interviewer is checking:** Measure first, fix the big offenders, and recognise that tuning alone may not reach the target.
**Say this in the interview:** "Tuning the three slow visuals gets me from 28 to 10 seconds. To reach 5, I also need to cut about 5 more seconds from the other 21, mainly by removing or merging visuals."

**What the data shows:** Three visuals cause 20 of 28 seconds (71%).
**Working:**
1. Now: 2 + 8 = 10 seconds (down from 20 + 8 = 28).
2. Gap to the 5-second target = 10 - 5 = 5 seconds.
3. The other 21 visuals average 8 / 21 = about 0.38 seconds each. To save 5 seconds I would need to remove about 5 / 0.38 = 13 of them, or make them faster.
4. In this simplified exercise, keeping the three tuned visuals at 2 seconds, the other visuals must total 3 seconds or less.
**Result:** Load time now is 10 seconds; still 5 seconds over target.
**Caveats / what else I would check:** In real tools visuals load partly in parallel, so the sum is a simplification; the cause of the slow three (heavy DAX, too many rows, high-cardinality fields); whether the target applies on first load or on filter clicks.
**Next step / recommendation:** (1) Use performance analysis to confirm which visuals are slow. (2) Cut the page to what the audience needs: move detail to a drill-through page, merge small tiles into one table. (3) Replace heavy filters with a few simple ones. (4) Re-measure and agree a realistic target with the business if 5 seconds costs too much content.
**Likely follow-ups:** 1) *What if the business insists on all 24?* Split into two pages or tabs. 2) *Which first?* The slowest visuals; they give the most saving.
**Common mistakes / traps:** Fixing the 0.4-second visuals first; assuming tuning alone reaches the goal.

### Q41 ⭐⭐ 🟡 An executive slicer lists all 40,000 employee IDs and makes the page slow. What do you change?
**Asked at:** commonly asked (no company-specific report found); high-cardinality filters are a listed theme on Tableau performance pages (unverified).
**What the interviewer is checking:** That you see the slicer as a poor tool for 40,000 values and offer a better design.
**Say this in the interview:** "A list of 40,000 IDs is unusable for an executive and expensive to load. I would replace it with a search box or higher-level filters like department and location."

**First, clarify / contain:** Ask what the executive is trying to do: find one person, or look at a team? Do not just delete the slicer.
**What I would check, in order:**
1. What the slicer is used for (usage logs or a quick chat).
2. Whether department, location or manager already answers most needs.
3. Whether the slicer loads all values at start-up (the slow part).
**If I find...:**
- Users look up individuals: use a search slicer (type to find) or a drill-through page to a single employee, with the access rules checked.
- Users filter groups: replace with hierarchy filters (department, grade, location).
- The ID is needed only for detail: move it to a detail table or tooltip.
**What I would tell the stakeholder:** "The employee list was making the page slow and hard to use. I have replaced it with department and manager filters and a search for individuals. The page now loads in about X seconds; tell me if you still need to find individual IDs."
**Prevent it next time:** Design rule: no filter with more than a few hundred values on a main page; include sensitive-data review for individual-level lists.
**Likely follow-ups:** 1) *Is an individual list a privacy issue?* It can be; confirm access rules with HR data owners. 2) *Could you just make it a dropdown?* A dropdown still loads all 40,000.
**Common mistakes / traps:** Keeping the slicer and adding more hardware; removing it without a substitute.

### Q42 ⭐⭐ 🟡 A user says, "I selected Hyderabad and the dashboard shows nothing, but it worked last week." How do you troubleshoot?
**Asked at:** commonly asked (no company-specific report found); the stakeholder-reported discrepancy theme appears on Dataford-style practice prompts (unverified).
**What the interviewer is checking:** A calm, ordered diagnosis: reproduce, then data, then access, then filters.
**Say this in the interview:** "First I try to reproduce it as that user. Then I check whether Hyderabad still exists in the data under that name, and whether the user's access changed."

**First, clarify / contain:** Ask for a screenshot, the page, the other filters selected and the time. Do not change the model yet.
**What I would check, in order:**
1. Reproduce it with the same filters; if I see data, compare my access and filters with theirs.
2. Look for other filters or date ranges that now exclude all rows (a saved view or bookmark).
3. Check the data for Hyderabad: spelling or code change (Hyderabad versus Hyd or a new city code), a trailing space, a re-mapped region.
4. Check row-level security (rules limiting who sees which rows) and whether the user's role or region changed.
5. Check the last refresh: did a failed load or a new source drop Hyderabad's rows?
6. Check recent changes to the report or the model.
**If I find...:**
- Name or code changed: fix the mapping, and tell users.
- Access changed: raise with the access owner, do not bypass the rules.
- Data missing: treat as a data incident and fix the load.
**What I would tell the stakeholder:** "Thanks for flagging it. I found [cause]. It is fixed / will be fixed by [time]. Other users in Hyderabad may have been affected; I have checked."
**Prevent it next time:** Alerts for dimension values that disappear or appear, a change log, and tests with role-based views.
**Likely follow-ups:** 1) *If it works for you but not for them?* Suspect permissions or their filter state. 2) *Is it worth a post-mortem?* Yes, if others were affected.
**Common mistakes / traps:** Assuming user error; testing only as the admin.

### Q43 ⭐⭐ 🟡 A senior leader asks you to add 15 more KPIs and 10 filters to an executive dashboard that is already slow and cluttered. How do you respond?
**Asked at:** commonly asked (no company-specific report found); a stakeholder-management scenario, in line with the stakeholder rounds described in internal interview-process notes (Cognizant theme, unverified).
**What the interviewer is checking:** That you push back with options, not with a flat "no", and tie the request to the decisions the leader makes.
**Say this in the interview:** "I would ask which decisions those KPIs support, then offer a prioritised short list on the main page and the rest on drill-down pages."

**First, clarify / contain:** Thank them, and ask, "What decisions do you want these to help with?" Do not agree or refuse on the spot.
**What I would check, in order:**
1. Which of the 15 KPIs are already available somewhere and who owns each definition.
2. Which KPIs the leader looks at weekly versus occasionally.
3. The current slowness and clutter (load time, visual count) as the baseline.
4. Data availability and refresh for each new KPI.
**If I find...:**
- Only a few matter for decisions: add those, remove or merge old ones.
- Many are needed: build a second layer, a summary page plus detail pages, or a separate analyst view.
- Some data does not exist: say so and give an estimated timeline.
**What I would tell the stakeholder:** "I can add these. To keep the page quick, I suggest 6 headline KPIs on the front page and the other 9 on a drill-down page, with filters limited to the 3 you use most. This would take about X days. Would you like to see a mock-up first?"
**Prevent it next time:** A simple intake rule (every new KPI needs an owner, definition and the decision it supports) and a regular clean-up of unused visuals.
**Likely follow-ups:** 1) *What if the leader insists?* Build it as a separate page and show the speed difference. 2) *How do you decide the headline KPIs?* The ones tied to the leader's goals.
**Common mistakes / traps:** Saying yes and delivering a slow, unreadable page; saying no without an alternative.

### Q44 ⭐⭐ 🟡 You find that test and dummy accounts have been included in a revenue dashboard for two months. How do you fix it and communicate it?
**Asked at:** commonly asked (no company-specific report found); a data-quality and trust scenario.
**What the interviewer is checking:** Whether you size the impact, correct history, and tell people proactively.
**Say this in the interview:** "I would size the effect first, fix the filter and the history, and tell the report users with the before and after numbers."

**First, clarify / contain:** Confirm how test accounts are identified (flag, naming pattern, email domain); do not delete rows. Note when the problem began.
**What I would check, in order:**
1. List all test and dummy accounts and their revenue by month for the two months.
2. Compute revenue with and without them, in rupees and as a share of the total.
3. Find how they entered (a new feature, missing flag, a changed source).
4. Find who has used the affected numbers (reports, forecasts, targets).
**If I find...:**
- The share is tiny: fix, restate, send a short note.
- The share is material: tell leadership at once, with a restated trend, and inform anyone who made decisions on it.
- The flag is unreliable: agree a rule with the source team (a customer type field).
**What I would tell the stakeholder:** "Test accounts were included in revenue for [dates]. They added INR X (Y% of revenue). The corrected figures are [..]. The dashboard now excludes them and I have restated the two months. Nothing else is affected."
**Prevent it next time:** An explicit "is test account" field in the source, an automatic exclusion rule, and a check that flags unusual accounts (round amounts, test-like names).
**Likely follow-ups:** 1) *Do you restate history?* Yes, with a note. 2) *Is it your fault?* Own the fix and the prevention; say what failed.
**Common mistakes / traps:** Fixing silently; excluding accounts by guessing names; forgetting downstream reports.

### Q45 ⭐⭐ 🟡 How would you design a dashboard so users can tell when its numbers are provisional or incomplete?
**Asked at:** commonly asked (no company-specific report found); a design and trust theme (gap-fill, judgement).
**What the interviewer is checking:** That you design trust signals into the page, not into a side email.
**Say this in the interview:** "I would show a 'data as of' time on every page and mark incomplete periods visually, with a short note on what is missing."

**Explain simply:**
- **Freshness stamp:** "Data as of 06:10, 12 Nov" at the top of each page.
- **Incomplete period marking:** show the current month in a lighter colour or with a dashed line, labelled "month to date".
- **Status banner:** appears automatically when a source failed or a completeness check fails ("Source X missing; totals understate").
- **Provisional labels:** a tag such as "Provisional" for numbers not yet closed by Finance, and "Final" after.
- **Definitions page:** how the number is built and when it is finalised.
**Worked mini-example:** Monthly payroll cost: days 1 to 20 are provisional until payroll closes on the 25th; the bar for the current month is hatched and the tooltip says "provisional, final on 26 Nov".
**Practice step:** Take any dashboard and list three numbers that can change after viewing; add a label for each.
**Likely follow-ups:** 1) *How does a banner appear automatically?* A check on row counts or latest date drives a flag field that the page reads. 2) *Is there a risk of too many labels?* Yes, so use a few consistent ones.
**Common mistakes / traps:** Showing a partial month as a drop; putting the timestamp in small print where nobody sees it.

### Q46 ⭐⭐ 🟡 A scheduled refresh failed at 3 am because of an expired credential and you only learnt about it at 9 am from users. How do you handle it and stop it recurring?
**Asked at:** commonly asked (no company-specific report found); a refresh-failure and monitoring theme (gap-fill, judgement).
**What the interviewer is checking:** Fix now, communicate, then remove the single point of failure.
**Say this in the interview:** "First I renew the credential and refresh, and tell users the state. Then I make sure failures alert me, and that the credential does not depend on one person's password."

**First, clarify / contain:** Check the failure message, renew the credential, run the refresh, and confirm the data and the last-updated time. Post a short update to users straight away.
**What I would check, in order:**
1. Which datasets and reports were stale and for how long.
2. Whether anyone used stale numbers for decisions since 3 am.
3. Why the credential expired (a personal account, a password policy, a token with an expiry).
4. Whether other refreshes use the same credential and will fail next.
**If I find...:**
- A personal login: move to a service account (an account that belongs to the system, not a person), with the owner's approval.
- A token with an expiry: calendar reminders and a rotation process (confirm with IT policy).
- Other datasets share it: renew those now.
**What I would tell the stakeholder:** "The 3 am refresh failed because a login expired, so the dashboard showed yesterday's data until 9:40. It is now refreshed. I have checked that no other reports are affected, and I have set up alerts so I find out within minutes."
**Prevent it next time:** Failure email or message alerts to a team inbox (not one person), a "data as of" stamp, an expiry calendar for credentials, and a documented runbook.
**Likely follow-ups:** 1) *Should you apologise?* Briefly; the focus is what changed. 2) *Who should own credentials?* A team or service account with IT oversight.
**Common mistakes / traps:** Fixing and not telling anyone; alerting only one person who is on leave.

### Q47 ⭐⭐ 🟡 An executive asks for a real-time dashboard, but the source can only deliver hourly batches and live queries would slow the operational system. How do you respond?
**Asked at:** commonly asked (no company-specific report found); a refresh-architecture and stakeholder theme (gap-fill, judgement).
**What the interviewer is checking:** That you ask what "real time" really means and offer options with costs.
**Say this in the interview:** "I would ask what decision needs it and how fresh it must be. Often hourly is enough; if not, there are options with a cost, and I would not slow the operational system."

**First, clarify / contain:** Ask, "What action would you take with a minute-old number that you cannot take with an hour-old one?" Do not promise real time yet.
**What I would check, in order:**
1. The real need: minutes, hourly, or daily; which metrics (not all of them).
2. What the source can offer: hourly batches only, a replica database, an event feed or a change log (ask the IT team).
3. Load impact of queries on the live system.
4. Cost and time of any near-real-time pipeline.
**If I find...:**
- Hourly is acceptable: refresh hourly and show "last updated" time.
- A few metrics need freshness: build a small feed only for those, from a read replica (a copy of the database for reporting) or event stream, agreed with IT.
- Real time is truly needed: scope it as a project with IT and a cost estimate.
**What I would tell the stakeholder:** "I can give you hourly updates by [date], with a visible timestamp. True real time would need a separate feed from IT and I would not run it on the live system. Let us decide which numbers truly need it."
**Prevent it next time:** Document the freshness level of each dashboard (daily, hourly, live) so expectations are set at the start.
**Likely follow-ups:** 1) *Why not DirectQuery?* It adds queries to a system that serves customers; it risks slowing it. 2) *Is hourly "real time"?* Not strictly, but often enough; always label it.
**Common mistakes / traps:** Agreeing to "real time" before checking the source; connecting directly to the production database.

### Q48 ⭐⭐ 🟡 The new Power BI report differs from the legacy Excel report by 0.8%, and the business refuses to switch. How do you handle the migration?
**Asked at:** commonly asked (no company-specific report found); report migration and reconciliation themes appear in prep-site question banks (unverified).
**What the interviewer is checking:** Whether you treat the gap as something to explain line by line, not argue away, and whether you manage the people side of a switch.
**Say this in the interview:** "I would not defend the new report. I would explain the 0.8% gap line by line, agree which number is right in writing, and run both reports side by side until the business signs off."
**First, clarify / contain:** Ask who owns the legacy report and what 0.8% is in rupees (for example, 0.8% of Rs 10 crore is Rs 8 lakh). Do not switch anyone over yet, and do not say "Excel is wrong" before checking.
**What I would check, in order:**
1. Definitions: same filters, same date range, same status codes (for example, are cancelled orders in both?).
2. Hidden manual steps in Excel: pasted values, hidden rows, hand-edited cells, old lookups.
3. Rounding and currency conversion done at different stages.
4. Data timing: refresh time against the Excel file's extract time.
5. Row-level compare: export both to one sheet and match by ID to list the exact rows that differ.
**If I find...:** Excel has a manual override or an old rule: document it, and ask the owner whether it is intended. Power BI has a bug: fix it and re-test. Both are right under different definitions: pick one definition, publish it, and show a bridge (a table from the old number to the new one).
**What I would tell the stakeholder:** "The gap is 0.8%. I have traced it to X rows and Y rule. Here is the bridge from the old number to the new one. I propose two months of parallel running, and we switch only when you are satisfied. I will update you every week."
**Prevent it next time:** Keep a sign-off checklist and a written metric definition for every migrated report. Retire the old file only after the agreed parallel period.
**Likely follow-ups:** 1) *What if the business still refuses?* Keep both for a fixed period and set an exit date with the sponsor. 2) *Is 0.8% acceptable?* It depends on the use; unexplained is the real problem, not the size.
**Common mistakes / traps:** Calling the old report wrong; forcing a cut-over by date; leaving the gap "unexplained but small".

### Q49 ⭐⭐ 🟡 Three regional managers each see only their region, and the national head sees a different total from the sum of their numbers. What do you check?
Inline data: the national head sees 1,000 records; managers see 400, 350 and 300 records.
Question: what does the 50-record excess suggest?
**Asked at:** commonly asked (no company-specific report found); the "RLS total mismatch" theme is a gap-fill question (judgement).
**What the interviewer is checking:** Whether you understand that row-level security (RLS, a rule that shows each user only their rows) can double count or hide rows.
**Say this in the interview:** "The managers add up to 1,050 but the national head sees 1,000, so 50 records appear in more than one region. I would find those records and the rule that places them twice."
**What the data shows:** 400 + 350 + 300 = 1,050. The national head sees 1,000. The managers' views exceed the total by 50 records, which is 5.0% of the national figure. Note the excess is on the managers' side, not the head's.
**Working:**
1. Sum of regions: 1,050.
2. Difference from national: 1,050 minus 1,000 = 50.
3. Most likely cause: 50 records are visible to two managers (counted in two regions), for example people on a shared or matrix assignment, or a many-to-many link between region and record.
**Result:** 50 records (5.0% of 1,000) are probably double counted across regions. If instead the national head were short, it would point to unmapped records.
**Caveats / what else I would check:** Do the roles use one region per record? Is a record linked to two regions, or a duplicate row in the security table? Is the national head's role filtering anything out? Check by listing record IDs per manager and finding IDs that appear in two lists.
**Next step / recommendation:** Fix the mapping so each record has one owning region (or state clearly that totals of regions are not additive), then add a check that regional counts sum to the national count.
**Likely follow-ups:** 1) *Is it a security risk?* If a manager sees another region's rows, yes, treat it like Q57. 2) *Could it be a filter?* Yes, test with the same filters on both views.
**Common mistakes / traps:** Assuming the national total is wrong; forgetting that shared records are legitimate sometimes; not saying which side is larger.

### Q50 ⭐⭐ 🟡 The headcount for March showed 520 when you published the report, but today the same dashboard shows 500 for March. What happened and how do you prevent it?
**Asked at:** commonly asked (no company-specific report found); as-of headcount is a gap-fill definitional trap (judgement).
**What the interviewer is checking:** Whether you know that data can be changed after the fact, and the difference between a snapshot and a live record.
**Say this in the interview:** "Something in the source changed after I published: 20 fewer people now count for March. I would find out whether it is a late correction or a definition change, then lock the published month."
**First, clarify / contain:** Ask who noticed and what they used the 520 for. Do not overwrite or delete the old number; keep a copy of both.
**What I would check, in order:**
1. Compare the March employee list now against a saved copy of the published list (the 20 IDs that dropped out; 20 is 3.8% of 520).
2. Are they backdated exits, duplicate removals, or transfers (changed dates in the HRIS)?
3. Did the headcount definition change (contractors, interns, as-of date versus month average)?
4. Did the refresh logic or a filter change in the model?
**If I find...:** Late corrections of real data: the new number is more accurate, so publish a restatement note. A definition change: restate both on one basis. A bug: fix and re-publish.
**What I would tell the stakeholder:** "March was 520 when published and is 500 today. 20 records were corrected in the HRIS after publishing (if confirmed). The 500 is the better figure; I will mark the change on the report and send a note to anyone who used 520."
**Prevent it next time:** Store a monthly snapshot (frozen copy) of headcount at month end, and show "as of" dates. Log changes to history.
**Likely follow-ups:** 1) *Which is right?* The one that matches the agreed definition and as-of date. 2) *Do you tell leadership?* Yes, quickly, with the reason.
**Common mistakes / traps:** Quietly changing the number; blaming the user; no snapshot.

### Q51 ⭐⭐ 🟡 When is a difference of 0.3% between a dashboard and a source report worth chasing, and when would you leave it?
**Asked at:** commonly asked (no company-specific report found); the materiality idea is a judgement-based question.
**What the interviewer is checking:** Judgement: size against impact, and whether the gap is explained.
**Say this in the interview:** "The percentage alone does not decide it. I chase it if it is unexplained, growing, in money or compliance, or on a count that should be exact; I leave it if I can explain it as rounding or timing."
**First, clarify / contain:** Ask what the number is used for. 0.3% of 1,000 employees is 3 people; of Rs 50 crore it is Rs 15 lakh; of Rs 1 crore it is Rs 30,000.
**What I would check, in order:**
1. The absolute size in rupees or people, not only the percentage.
2. Is it the same gap every day (rounding or a fixed rule) or does it change (a real leak)?
3. Could it be timing: different refresh times?
4. Is it in a regulated or audited figure (payroll, statutory reports, financial close)?
**If I find...:** Explained rounding or timing, small, stable: leave it and document it. Unexplained, growing, or in payroll or finance: chase now. A count that should match exactly (headcount, invoices): chase even at 0.3%.
**What I would tell the stakeholder:** "The gap is 0.3%, about 3 people (for example). It is explained by rounding and has been stable, so we are leaving it and have written the reason down."
**Prevent it next time:** Set a tolerance per metric in advance (for example, "money must match to the rupee; ratios within 0.1 point").
**Likely follow-ups:** 1) *Who sets the tolerance?* The metric owner with you. 2) *What if it is random each day?* That signals a real defect.
**Common mistakes / traps:** Using one threshold for everything; ignoring a small but growing gap; chasing noise for hours.

### Q52 ⭐⭐ 🟡 What automated checks would you add so a mismatch is caught before users see it?
**Asked at:** commonly asked (no company-specific report found); validation before leadership is a common prep-site theme (Dataford, unverified).
**What the interviewer is checking:** Whether you know the practical checks, and that they run on every refresh.
**Say this in the interview:** "I would add a small set of checks that run after every refresh: row counts, totals against source, duplicates, nulls, and freshness, with an alert and the publish blocked if they fail."
**Clarify first:** Which numbers matter most (headcount, revenue)? Who gets the alert, and what should happen on failure: block, or publish with a warning?
**Plan:**
1. Row count check: rows loaded against rows in the source.
2. Total check: dashboard total against the source total, within an agreed tolerance.
3. Key checks: no duplicate IDs; no blank IDs; every code maps to a lookup row (unmapped department, region).
4. Freshness check: latest date in the data is as expected.
5. Range checks: no negative headcount, no future dates, no percentages above 100%.
6. Change check: today's total against yesterday's, flag jumps over a set size.
**Method choice and why:** Start with simple scheduled SQL or a small script writing results to a "checks" table, then alert by email. Move to a testing tool only if the checks multiply.
**Pitfalls:** Too many alerts so people ignore them; tolerances nobody agreed; checks that pass because they use the same wrong logic as the report.
**Deliverable:** A one-page check list with owner, tolerance and action for each check, plus a small status table showing the last run result.
**Likely follow-ups:** 1) *What happens when a check fails?* Hold the last good version and alert the owner. 2) *How do you test the checks?* Feed in a known bad file.
**Common mistakes / traps:** Only checking after users complain; no owner for alerts; testing only totals, not mapping.

### Q53 ⭐⭐ 🟡 A VP says, "Your dashboard has too much on it and I cannot find the answer." How do you rework it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you start from the VP's decision, not from the chart count.
**Say this in the interview:** "I would ask the VP what decision they make with it, then rebuild a one-page view with three or four headline numbers and put the detail one click away."
**First, clarify / contain:** Ask: What question do you open this to answer? What do you look at first? What do you never use? Do not start deleting visuals before that.
**What I would check, in order:**
1. Usage data: which visuals are actually clicked.
2. The VP's top three questions, written down.
3. What each existing visual answers, and who else depends on it.
4. Whether the answer needs a number, a trend, or a comparison.
**If I find...:** Most visuals unused: move them to a detail page. A key answer exists but buried: bring it to the top left. Two groups of users want different things: make two views (executive summary and analyst detail).
**What I would tell the stakeholder:** "I will put your three numbers at the top with a one-line status for each, and move the rest to a second page. Here is a sketch for your approval by Friday."
**Prevent it next time:** Agree the purpose and audience for each dashboard before building. Review it quarterly.
**Likely follow-ups:** 1) *How many visuals?* No fixed rule; a handful per page for a summary page, as a guideline. 2) *What about the other users?* Keep the detail page.
**Common mistakes / traps:** Adding more filters; deleting what others use; redesigning without asking the VP.

### Q54 ⭐⭐ 🟡 Users have stopped trusting a dashboard after two incorrect numbers in a month. How do you rebuild trust?
**Asked at:** commonly asked (no company-specific report found); trust and disputed numbers are a stakeholder theme in prep material (unverified).
**What the interviewer is checking:** Ownership, root-cause thinking, and consistent communication, not just a fix.
**Say this in the interview:** "I would own the errors openly, show exactly what went wrong and what is now fixed, add checks, and prove it over several weeks."
**First, clarify / contain:** Find out which two numbers and who saw them. Put a short notice on the dashboard now ("under review") for the affected pages. Do not promise it will never happen again.
**What I would check, in order:**
1. Root cause of each error (logic, data, refresh, definition).
2. Whether the same cause could affect other numbers.
3. A full review of the key measures against source.
4. How users found the errors (they found it, not us, is the signal for missing checks).
**If I find...:** Same root cause: fix once, test everywhere. Separate causes: fix each, and add a pre-release test. Definitions unclear: write them down on the report.
**What I would tell the stakeholder:** "Two numbers were wrong: A because of X, B because of Y. Both are fixed and re-checked. We added daily checks and a definitions page. I will send a short status note each week for a month."
**Prevent it next time:** Automated checks (see Q52), a change log, a named owner, and a feedback link on the dashboard.
**Likely follow-ups:** 1) *How do you know trust is back?* Usage and fewer queries. 2) *Who do you tell?* Everyone who saw the wrong numbers.
**Common mistakes / traps:** Quiet fixes; blaming the data team or source; over-promising.

### Q55 ⭐⭐ 🔴 You discover 14 different "Sales Dashboard" files across teams, each with slightly different numbers. How do you rationalise them?
**Asked at:** commonly asked (no company-specific report found); the "single source of truth" theme appears in vendor blogs (unverified).
**What the interviewer is checking:** Whether you fix the cause (definitions and one data model), not only the files.
**Say this in the interview:** "I would inventory all 14, find why the numbers differ, agree one set of definitions with the owners, and consolidate onto one governed dataset."
**First, clarify / contain:** Do not delete anything. Ask who owns each file, who uses it, and for what decision. Pick a sponsor (for example, the sales head or Finance).
**What I would check, in order:**
1. Build an inventory: owner, source, refresh method, last used, number of users.
2. Compare the main figures for one month across all 14 and note the cause of each gap (filters, date logic, returns, tax, currency).
3. Group them: duplicates, true variants, obsolete.
4. List the definitions in dispute (what counts as a sale? when is it booked?).
**If I find...:** Same logic, different copy: retire after migration. Real differences by need: keep as views from one model. Unowned and unused: archive with a notice.
**What I would tell the stakeholder:** "We have 14 files, and the differences come from five definitions. I propose one agreed definition set and one official dashboard, with team views built on it. Plan and dates attached."
**Prevent it next time:** A shared dataset, certified dashboards, a naming standard, and an approval step to publish.
**Likely follow-ups:** 1) *Who decides a definition?* A named business owner, written down. 2) *How do you stop new copies?* Access control and a visible "official" label.
**Common mistakes / traps:** Deleting first; building a 15th dashboard; skipping the politics.

### Q56 ⭐⭐ 🔴 Customer counts differ across CRM, billing and finance systems, and none is accepted as authoritative. How do you build a reconciliation approach?
**Asked at:** commonly asked (no company-specific report found); reconciling conflicting systems is a theme in Dataford-style prompts (unverified).
**What the interviewer is checking:** Whether you can define "customer", match records across systems, and build a repeatable bridge.
**Say this in the interview:** "First I would agree what a customer is, then match records by a common key, and publish a bridge that explains every difference between the three counts."
**Clarify first:** What does each system count: leads, accounts, paying customers, active ones? Which decision needs the number? Is there any shared ID?
**Plan:**
1. Write a one-line definition of customer (for example, "paid at least once in the last 12 months").
2. Extract the customer lists with IDs, names and status from each system.
3. Build or request a mapping key (customer ID, tax ID, email); clean names and duplicates.
4. Match, then classify: in all three, in two, in one only.
5. Explain each gap type: timing, test accounts, merged accounts, closed accounts, wrong status.
6. Publish a bridge table: CRM count to billing count to finance count.
**Method choice and why:** Start with exact matching on a shared ID; use fuzzy name matching only for the leftover and have a person confirm it.
**Pitfalls:** Counting a customer once per contract; ignoring time; forcing one system to win without agreement; fuzzy matches that join different customers.
**Deliverable:** A bridge report with counts per category, the agreed definition, a proposed system of record per field, and an owner for fixing source data.
**Likely follow-ups:** 1) *Which system wins?* The one that is the owner of that fact, for example billing for paid status. 2) *How often?* Monthly, with an automatic check.
**Common mistakes / traps:** Matching before defining; ignoring duplicates; presenting one number with no bridge.

### Q57 ⭐⭐ 🔴 You notice a manager-level dashboard exposes peers' salary figures because of a row-level security mistake. What do you do?
**Asked at:** commonly asked (no company-specific report found); RLS appears in Deloitte USI round reports per internal research (unverified, anonymous).
**What the interviewer is checking:** Ethics, speed, containment and honest escalation.
**Say this in the interview:** "I would stop the exposure first by restricting access, then report it to the data owner and HR and security, find out who saw what, and fix and test the rule."
**First, clarify / contain:** Immediately restrict the report (unpublish or remove manager access), and do it quietly: do not discuss the salaries with anyone. Do not delete logs; they show who opened it.
**What I would check, in order:**
1. Exactly which fields and which roles were exposed.
2. Since when (check the change history of the RLS rule or model release).
3. Who opened the report in that period (usage and audit logs).
4. Whether the data was exported or shared on.
5. The cause: wrong filter, role mapping, or a missing role.
**If I find...:** Few viewers, short window: tell the owner and let them decide on notice. Wide exposure or export: escalate to security and legal under your incident process. Rule error: fix, and test with a test user from each role.
**What I would tell the stakeholder:** "At [time] I found managers could see peers' salary figures. I removed access at [time]. I am pulling the access logs now and will report who saw what by end of day. The fix will be tested before restoring access."
**Prevent it next time:** Test RLS with each role before release, keep sensitive fields out of the model where not needed, and review access regularly. Check privacy obligations (for example, India's DPDP Act, from memory, unverified) with the legal team.
**Likely follow-ups:** 1) *Do you hide it to avoid trouble?* No, report it promptly. 2) *Who decides on notifying staff?* HR, legal and the data owner.
**Common mistakes / traps:** Fixing quietly with no report; discussing salaries with colleagues; restoring access untested.

### Q58 ⭐ 🟢 A weekly dashboard refreshes four times a day for 20 minutes each, but usage logs show two viewers open it once a week. What do you do and how many refresh minutes per week do you save?
**Asked at:** commonly asked (no company-specific report found); refresh scheduling is a typical Power BI scenario theme (unverified).
**What the interviewer is checking:** Matching refresh frequency to real use, and doing the arithmetic.
**Say this in the interview:** "Four refreshes a day is wasted for a weekly report. I would refresh once a week, just before the viewers open it, and save about 540 minutes a week, subject to confirming how they use it."
**What the data shows:** 4 refreshes a day x 20 minutes = 80 minutes a day. Two viewers open it once a week.
**Working:**
1. Current load, assuming refresh runs 7 days a week: 80 x 7 = 560 minutes a week.
2. New load: one 20-minute refresh a week = 20 minutes.
3. Saving: 560 minus 20 = 540 minutes a week (9 hours).
4. If it runs only on 5 working days: 400 now, 380 saved.
**Result:** about 540 minutes a week saved on a 7-day schedule (380 on a 5-day schedule). That is 96% of refresh time on the 7-day basis.
**Caveats / what else I would check:** Confirm with the two viewers when and why they open it; check the log is complete (the log might miss mobile or email views); consider whether other reports share the dataset; keep a manual refresh option.
**Next step / recommendation:** Set the refresh for the morning before the usual viewing day, tell the viewers, and check after a month that they have no complaints.
**Likely follow-ups:** 1) *What if they want fresher data once?* Add a manual refresh button or a short exception. 2) *Does it matter if shared capacity is free?* Still tidy, and it reduces load for others.
**Common mistakes / traps:** Cutting without asking viewers; ignoring weekends; forgetting that two viewers may be the senior ones.

### Q59 ⭐ 🟢 A scheduled email PDF of the dashboard goes out at 7 am, while the data refreshes at 8 am, so recipients see old numbers. How do you fix it?
**Asked at:** commonly asked (no company-specific report found); the refresh-chain timing overlap is a gap-fill question (judgement).
**What the interviewer is checking:** Whether you see this as an ordering and dependency problem.
**Say this in the interview:** "The email runs one hour before the data. I would move the email after the refresh, ideally triggered by the refresh finishing, not by a clock time."
**First, clarify / contain:** Confirm the times and time zones (7 am in which zone?). Tell recipients for now that the 7 am email is yesterday's data, so they do not act on it.
**What I would check, in order:**
1. Refresh duration and its history (does it ever run late?).
2. The upstream data load time (the source may finish even later).
3. Time zones of the scheduler, the service and the readers.
4. Who needs the email and by when.
**If I find...:** Refresh takes 30 minutes and finishes about 8:30: schedule the email for 9 am or later. Refresh time varies: trigger the email when the refresh completes. Readers need numbers at 7: move the whole data chain earlier.
**What I would tell the stakeholder:** "The email was going out before the data was updated. From tomorrow it goes at 9 am after the refresh. If you need it earlier, we can move the data load; that needs a change from the data team."
**Prevent it next time:** Chain the jobs by dependency, show "data as of" on the PDF, and alert when a refresh fails.
**Likely follow-ups:** 1) *What if the refresh fails?* Do not send, or send with a warning. 2) *Why not just move the refresh to 6 am?* Possible if the source data is ready by then.
**Common mistakes / traps:** Moving only the clock time without a buffer; ignoring time zones; no "as of" stamp.

### Q60 ⭐ 🟢 The department headcount chart sums to 1,150, but the HRIS export totals 1,170. How do you find the difference?
Inline data: Engineering 410, Sales 280, Operations 330, Corporate 150 in the export; the dashboard excludes 20 employees whose department field is blank.
Question: confirm the 20-person gap and decide how to show them.
**Asked at:** commonly asked (no company-specific report found); HRIS versus report headcount is a gap-fill question (judgement).
**What the interviewer is checking:** Whether you reconcile systematically and treat missing values as a category, not silently drop them.
**Say this in the interview:** "The export adds to 1,170, the chart to 1,150, and the 20 blank-department employees explain the gap exactly. I would show them as 'Unassigned', not hide them."
**What the data shows:** The export's four departments sum to 1,170. The dashboard counts only employees with a department, so it shows 1,150.
**Working:**
1. Export total: 410 + 280 + 330 + 150 = 1,170.
2. Dashboard total: 1,150.
3. Gap: 1,170 minus 1,150 = 20, equal to the 20 employees with a blank department (1.7% of 1,170).
4. Check: 1,170 minus 20 blank = 1,150, so nothing else is unexplained.
**Result:** The 20-person gap is fully explained, by the blank department field. Caveat: the question lists four department totals that already sum to 1,170, so the blank 20 must be counted inside those departments in the export or in a separate row; I would check which, so as not to count them twice.
**Caveats / what else I would check:** Are the 20 new joiners awaiting assignment, or data entry errors? Are they in other fields (cost centre)? Do the blank rows differ by location?
**Next step / recommendation:** Add an "Unassigned" bar with a count of 20, send the list to HR operations to fill the department, and add a check that unassigned stays near zero.
**Likely follow-ups:** 1) *Why not just exclude them?* Totals would not match the HRIS and people would lose trust. 2) *What if the blank count grows?* Raise it as a data quality issue.
**Common mistakes / traps:** Dropping nulls silently; assuming the dashboard is wrong; not checking if the 20 are double counted.

### Q61 ⭐ 🟡 Dashboard sales in INR differ from Finance's INR figure for USD sales. Find the likely cause and decide which to use.
Inline data: USD 10,000 of sales in the month. Finance converts at one month-average rate of INR 83.00; the dashboard converts each transaction at its daily rate, giving INR 8,36,500.
Question: how big is the difference in rupees and per cent?
**Asked at:** commonly asked (no company-specific report found); currency conversion is a gap-fill question (judgement).
**What the interviewer is checking:** Whether you can find the method difference and choose a rule by purpose.
**Say this in the interview:** "The gap is Rs 6,500, about 0.78%, and it comes from daily rates against one average rate. I would use Finance's rule for official reporting and keep the daily view as a labelled analysis."
**What the data shows:** Finance: 10,000 x 83.00. Dashboard: Rs 8,36,500, which is an effective rate of 83.65.
**Working:**
1. Finance figure: 10,000 x 83.00 = Rs 8,30,000.
2. Dashboard figure: Rs 8,36,500.
3. Difference: 8,36,500 minus 8,30,000 = Rs 6,500.
4. Percent of Finance's figure: 6,500 / 8,30,000 = 0.78% (0.77% of the dashboard figure).
**Result:** Rs 6,500, about 0.78%; the dashboard is higher because the daily rates, weighted by when the sales happened, averaged 83.65 against 83.00.
**Caveats / what else I would check:** Which rate source and day? Are sales concentrated late in the month when the dollar was higher? Which rule does Finance use for closing, and which is stated in policy?
**Next step / recommendation:** Use Finance's rate for any number that must tie to the books. Keep daily-rate analysis if the business wants it, but label it, and show a bridge between the two on the report.
**Likely follow-ups:** 1) *Is the daily rate more accurate?* For transaction-level value, arguably, but official numbers follow finance policy. 2) *Constant currency?* Use a fixed rate to remove currency effect when comparing periods.
**Common mistakes / traps:** Calling one wrong; not showing the rate used; mixing both methods on one dashboard.

### Q62 ⭐ 🟡 After a data-model change, how would you regression-test a dashboard before releasing it?
**Asked at:** commonly asked (no company-specific report found); an AmbitionBox snippet mentions column changes breaking a view (unverified, mapping unclear).
**What the interviewer is checking:** A disciplined before-and-after comparison, not a quick glance.
**Say this in the interview:** "I would freeze the old version's numbers, run the new model on the same data, and compare key measures, filters and visuals one by one before anyone sees it."
**Clarify first:** What changed (columns, joins, measures, filters)? Which measures matter most? Is there a test copy of the report and data?
**Plan:**
1. Take a baseline: record key totals and a few detailed slices from the current (live) version.
2. Apply the change in a test copy and compare the same values.
3. Check row counts, duplicates and unmapped keys after joins.
4. Test filters, slicers and drill-downs; test each security role.
5. Check performance (load time) and refresh.
6. Have one business user try their usual questions.
7. Release with a rollback copy and a short change note.
**Method choice and why:** Side-by-side comparison of old and new on the same period, as a simple table of old value, new value and difference, flagged if beyond tolerance.
**Pitfalls:** Testing only totals; testing with different data; forgetting row-level security and mobile views; no rollback.
**Deliverable:** A test log (what was compared, results, issues) and a go or no-go note to the owner.
**Likely follow-ups:** 1) *What if numbers differ?* Explain each difference before release. 2) *Automate?* Yes, save the comparison as a repeatable script or query.
**Common mistakes / traps:** Eyeballing; no baseline; releasing on Friday evening.

### Q63 ⭐ 🟡 An old dashboard that people still rely on is broken and no one owns it. How do you handle it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Pragmatism: serving users now while fixing ownership.
**Say this in the interview:** "I would find who uses it and for what, get a quick fix or workaround going, then get an owner named or retire it properly."
**First, clarify / contain:** Check usage logs and ask users what they need from it and by when. Do not rebuild it blind, and do not delete it.
**What I would check, in order:**
1. What is broken (data source, refresh, credentials, a changed column).
2. Who uses it and how often.
3. Whether another dashboard now answers the same question.
4. Who created it and who owns the source data.
5. Effort to fix against the value.
**If I find...:** Simple break and heavy use: fix it, then document it. Duplicate exists: move users to it and retire this one. Complex, little use: tell users the end date, and archive.
**What I would tell the stakeholder:** "The dashboard broke because [cause]. I can restore a basic version by [date]. It has no owner, so I propose [team] takes it, or we retire it on [date]. Tell me if you need it."
**Prevent it next time:** Every dashboard has a named owner, a purpose and a review date in a central register.
**Likely follow-ups:** 1) *Who owns it if nobody does?* The sponsoring team of the main users, agreed in writing. 2) *Do you fix it yourself?* Only after agreeing ownership and time with your manager.
**Common mistakes / traps:** Silent heroics creating a permanent unofficial duty; deleting it; no documentation.

### Q64 ⭐ 🟡 A "Top 10 products" visual gives different results when another filter is applied, and the user thinks the numbers are wrong. How do you explain it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand that a ranking is recalculated within the current filters.
**Say this in the interview:** "The numbers are not wrong. The Top 10 is recalculated inside whatever filter is on, so the list changes: the top 10 in one region is not the top 10 overall."
**First, clarify / contain:** Ask the user for the two views (screenshots and the filters on each). Do not change anything yet.
**What I would check, in order:**
1. Which filters are applied in each view (region, date, channel).
2. Whether the Top 10 filter is applied after the other filters (normally yes).
3. Whether the ranking metric is the same (sales, quantity, profit).
4. Ties at rank 10 or items with blank categories.
5. Whether any filter should be exempt (a "Top 10 overall" fixed list).
**If I find...:** Normal behaviour: explain with an example (a product that is 12th nationally can be 3rd in one region). The user wants a fixed list: build it based on the full data, or add a pinned label. A wrong filter setup: fix it.
**What I would tell the stakeholder:** "Top 10 always means the top 10 of what you have selected. When you filter to the South, you see the South's top 10. I will add a subtitle showing the filters in force."
**Prevent it next time:** Title the visual with its filter context ("Top 10 products in the selected region"), and offer a separate overall version if needed.
**Likely follow-ups:** 1) *Why do totals differ?* The top 10 total is not the grand total. 2) *Can we fix the list?* Yes, rank first on all data and then filter.
**Common mistakes / traps:** Telling the user they are wrong; changing the visual without explaining; not showing the filter context.

### Q65 ⭐ 🟡 A % of total measure shows 100% for every row once a user selects a category in a slicer. What is happening and how would you change the measure?
**Asked at:** commonly asked (no company-specific report found); DAX filter-context behaviour, in line with the SUM versus SUMX style questions mentioned in internal research (unverified).
**What the interviewer is checking:** Understanding of filter context and ALL, ALLSELECTED.
**Say this in the interview:** "The total in the denominator is also being cut by the slicer or the row, so each row is divided by itself. I would define the denominator with ALLSELECTED or ALL, depending on what 'total' should mean."
**First, clarify / contain:** Ask what the percentage should be of: the selected categories, or the whole company? Check what is on the rows and in the slicer.
**What I would check, in order:**
1. The measure: a plain total of sales in the denominator takes the same row and slicer filters as the numerator.
2. What the rows show (for example, categories) and what the slicer selects (the same field).
3. Whether a visual filter hides other rows.
**If I find...:** Denominator with no override: it equals the numerator, so 100%. If the user wants a share of the selected items: use ALLSELECTED. If they want a share of the whole: use ALL (a grand total ignoring slicers).
**What I would tell the stakeholder:** "The measure was dividing each row by itself once the slicer limited the data. I have changed the total to ignore the row filter, so you see each category's share of what you have selected (or of the full total, whichever you prefer)."
**Prevent it next time:** Name measures clearly ("% of selected total" and "% of grand total") and test them with a slicer selected.
One readable form (DAX, comments for a beginner):
```
-- share of what the user has selected on the page
Share of Selected =
DIVIDE (
    [Total Sales],                                  -- this row's sales
    CALCULATE ( [Total Sales], ALLSELECTED ( Products[Category] ) )  -- sales of all selected categories
)
```
It returns each category's share within the selection; use ALL in place of ALLSELECTED for a share of the full company.
**Likely follow-ups:** 1) *ALL versus ALLSELECTED?* ALL ignores every filter on that field; ALLSELECTED keeps the filters coming from slicers and outer filters. 2) *Why is 100% there for a single category?* One selected category is correct as 100% of the selection.
**Common mistakes / traps:** Using ALL when users expect a share of the selection; testing only without a slicer; forgetting DIVIDE for a zero total.

### Q66 ⭐ 🟡 How do you measure whether a dashboard is actually being used and decide whether to retire it?
**Asked at:** commonly asked (no company-specific report found); dashboard retirement is a gap-fill differentiator (judgement).
**What the interviewer is checking:** Evidence-based housekeeping, and consulting users before removal.
**Say this in the interview:** "I would look at usage logs for views, unique viewers and recency, ask the owners and users, and retire it in stages if the evidence is clear."
**Clarify first:** Which dashboards, and over what period (at least one full business cycle, such as a quarter, since some reports are used only at quarter end)? What is the cost of keeping them (refresh load, maintenance, risk)?
**Plan:**
1. Pull usage metrics: views, unique viewers, last opened, by month (from the BI tool's usage or audit logs).
2. Compare with the number of intended users.
3. Check seasonal use (month-end, annual review).
4. Contact the owner and the heaviest users to ask what they use it for.
5. Check what depends on it (email subscriptions, other reports, downloads).
6. Decide: keep, merge, fix, or retire.
**Method choice and why:** Simple counts and recency are enough; add a short user survey if the evidence is mixed.
**Pitfalls:** Counting views (a bot or an auto-refresh) as real use; judging on one quiet month; removing without notice; ignoring a small but critical group such as the board.
**Deliverable:** A retirement list with usage figures, owner, decision and date. Steps: notice, move to archive, delete after a set period.
**Likely follow-ups:** 1) *What threshold?* Set it with the business, for example no unique viewers in 90 days; it is a judgement call. 2) *Can it be restored?* Keep an archive copy for a period.
**Common mistakes / traps:** Retiring on views alone; no user notice; no archive.

### Q67 ⭐ 🟡 A user says the mobile app shows different totals from the desktop view of the same report. How do you investigate?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** A structured comparison before guessing.
**Say this in the interview:** "I would ask for screenshots of both with the filters and time, then check whether they are the same report, the same filters, the same refresh and the same login."
**First, clarify / contain:** Ask: which report and page, what time, and what filters. Ask for both screenshots showing the "last refreshed" time. Do not edit anything yet.
**What I would check, in order:**
1. Is it the same report and the same version (a copy, an old bookmark)?
2. Filters and slicers: a mobile layout can keep a different default or saved filter state.
3. Refresh time: one view may be cached or older.
4. Security: is the user seeing the same rows (row-level security, different account)?
5. Time zone and date settings on the device.
6. A mobile layout that hides a visual or a total, so the totals are not like for like.
**If I find...:** Different filters: show them how to reset. Stale cache: refresh and check the schedule. Different login: check the role. A real defect in the mobile layout: fix and test on both.
**What I would tell the stakeholder:** "I compared the two views. The difference is because [cause]. After [fix] both show X. If you see it again, send me the time and screenshot."
**Prevent it next time:** Test on both layouts before release, show "data as of" and active filters on every page.
**Likely follow-ups:** 1) *Could it be a bug?* Yes, but rule out the common causes first. 2) *How do you reproduce?* Use the same account and filters on both.
**Common mistakes / traps:** Assuming a bug; not asking for the filters; ignoring that the user may be seeing a different role.

### Q68 ⭐ 🔴 A BI tool's approximate distinct count differs by 1.2% from an exact SQL count. When do you accept this and when not?
**Asked at:** commonly asked (no company-specific report found); approximate distinct counts are a gap-fill differentiator (judgement).
**What the interviewer is checking:** Understanding the trade-off between speed and exactness, and the purpose of the number.
**Say this in the interview:** "I accept a small, known error for exploring large data where speed matters; I do not accept it for numbers that must tie to a record, such as headcount, billing or audit figures."
**First, clarify / contain:** Confirm the function is approximate (many large-data tools offer one that is faster, with a small error; check the tool's documentation, from memory, unverified). Ask what the number will be used for.
**What I would check, in order:**
1. The tool's documented error range against the 1.2% gap.
2. The size of the gap in the real unit (1.2% of 2,00,000 customers is 2,400).
3. Whether it is stable day to day or varies.
4. What the number is compared to (a trend, a total that must match, a payout).
5. Whether the exact count is affordable (run time, cost).
**If I find...:** Used for trend, exploration or a rough audience size: accept, and label it "approximate". Used for reconciliation, money, compliance, or small groups: use the exact count. Results inconsistent across views: switch to exact.
**What I would tell the stakeholder:** "This figure is an estimate, within about 1.2% of the exact count. It is fine for the trend. For the finance report I will use the exact count so it ties."
**Prevent it next time:** Mark approximate measures in their name, document the tolerance, and use exact counts for anything that must reconcile.
**Likely follow-ups:** 1) *Why not always exact?* Slower and costlier on big data. 2) *Does the error matter more for small groups?* Yes, relative errors are harder to judge there.
**Common mistakes / traps:** Mixing approximate and exact counts in one table; hiding that it is an estimate; assuming the exact SQL is always right (check the join duplicates).

### Q69 ⭐ 🔴 After a department restructure, last year's department-wise numbers on the dashboard changed. How do you handle history in the model and what do you tell users?
**Asked at:** commonly asked (no company-specific report found); history of changing dimensions is a gap-fill differentiator (judgement).
**What the interviewer is checking:** Whether you know the choice between restating history and keeping it as it was, and can communicate it.
**Say this in the interview:** "Last year changed because the department names or mappings were overwritten. I would decide with the business whether they want history as it was or restated to the new structure, and keep both views clearly labelled."
**First, clarify / contain:** Tell users now that history changed because of the restructure. Do not revert or overwrite anything yet; take a copy of the current model.
**What I would check, in order:**
1. How the department link works: is each employee linked to the current department only?
2. What the old versus new numbers are (for example, Sales moved from 280 to 310).
3. Which view the business needs: as it was then (what really happened) or on the new structure (like for like).
4. Whether the HRIS stores the effective dates of each department change.
**If I find...:** Dates are available: keep a history table of department with start and end dates (a "slowly changing dimension", a standard technique for keeping changes over time) so both views work. No dates: build a mapping table from old to new departments and restate with a clear note.
**What I would tell the stakeholder:** "Last year's figures moved because employees were re-mapped to the new departments. Both views are valuable, so I will show 'as reported then' and 'on the new structure', and mark which is which. Totals are unchanged; only the split moved."
**Prevent it next time:** Store effective dates for org changes, version the department mapping, and publish a change note for every restructure.
**Likely follow-ups:** 1) *Which is the default?* Ask the owner; for trends, the new structure is common, for audit, as reported. 2) *Do totals change?* They should not; check that.
**Common mistakes / traps:** Overwriting history silently; showing only the new view with no note; breaking totals by mapping errors.

### Q70 ⭐ 🔴 A director asks you to remove a red KPI from the dashboard before a board meeting. How do you respond?
**Asked at:** commonly asked (no company-specific report found); an ethics scenario theme (judgement).
**What the interviewer is checking:** Integrity under pressure, while staying constructive and respectful.
**Say this in the interview:** "I would not quietly remove it. I would understand the director's concern, offer context and a plan next to the KPI, and escalate if they still insist on hiding true data."
**First, clarify / contain:** Ask why they want it removed. Is the number wrong, misleading, or just bad news? Do not change the dashboard yet, and do not agree or refuse in the first minute.
**What I would check, in order:**
1. Is the KPI correct (definition, data, threshold)? If it is wrong, fix it and tell everyone.
2. Is the red status fair, or is the target or colour rule poorly set?
3. Is there missing context (a cause, a recovery plan) that would make it fairer?
4. What the company's reporting policy says about changes before the board.
**If I find...:** The KPI is wrong: correct it, with a note. It is right but needs context: add an explanation, trend and action plan beside it. It is right and the director still wants it hidden: raise it with my manager or the data owner, and do not remove it on my own.
**What I would tell the stakeholder:** "I understand the concern. The number is accurate, and the board will probably ask about it. I suggest we keep it and add the cause and the plan to fix it, so we show we are in control. Can we do that by Thursday?"
**Prevent it next time:** Agree KPI definitions, targets and who can change them in a written governance process, so changes are never ad hoc.
**Likely follow-ups:** 1) *What if you are told to remove it anyway?* Escalate to my manager and the data owner, and record the request. 2) *Can you ever remove a KPI?* Yes, through the agreed change process, with a record and a reason, if it is retired or redefined.
**Common mistakes / traps:** Quietly complying; refusing rudely; changing thresholds to turn it green.

