# Book 8 — Scenario-Based & Data Interpretation | Part 5: Analysis-Approach Scenarios 🟡

**Target:** 90 questions | **Actual:** 101 questions
**Scope:** "How would you analyse X" scenarios from the analyst's seat: framing the question, checking data, choosing cuts and comparisons, avoiding causal over-claims, and presenting findings, across HR, sales, e-commerce, finance and operations contexts.

### Q1 ⭐⭐⭐ 🟢 A manager says, 'Analyse our sales data and tell me what is going on.' What is your step-by-step approach before you open any data?
**Asked at:** commonly asked (no company-specific report found); prep guides stress clarifying before analysing.
**What the interviewer is checking:** Whether you turn a vague request into a clear question and decision before touching data.
**Say this in the interview:** "I would not open the data yet. First I ask what decision this supports, what 'going on' means (a drop, a rise, a surprise), and which period and metric. Then I write the question down and confirm it."
**Clarify first:** What prompted the request? Which decision will it feed (budget, hiring, targets)? What is "sales" (revenue, units, orders; gross or net of returns)? Which period, compared against what (last month, last year, target)? Who reads the result and by when?
**Plan:**
1. Restate the question in one line and get a yes from the manager.
2. List hypotheses (price, volume, mix, region, channel, calendar).
3. Name the data needed and who owns it; check I may use it.
4. Agree a first deliverable (one page, 3 findings) and a deadline.
5. Only then open the data, starting with checks (counts, dates, duplicates).
**Method choice and why:** Start with simple totals and trends over time, then cut by region, product and channel. Anything fancier waits until a simple cut shows where the story is.
**Pitfalls:** Starting to chart without a question; using a metric the manager defines differently; comparing unequal periods (days, festivals).
**Deliverable:** A short note: question, answer in one line, three supporting cuts, caveats, suggested action.
**Likely follow-ups:** 1) *What if the manager cannot say what they want?* Offer two or three concrete questions and ask which matters most. 2) *What if time is short?* Deliver the headline trend and say what is still unchecked.
**Common mistakes / traps:** Producing a pile of charts; skipping the definition of sales; never confirming the question back.

### Q2 ⭐⭐⭐ 🟢 You are handed a new dataset and asked to analyse it with no further brief. What is your general framework for approaching any analysis from question to recommendation?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you have a repeatable, disciplined process and not just tool skills.
**Say this in the interview:** "My framework is: question, data understanding, cleaning, exploration, analysis, check, then a recommendation with caveats. With no brief, I make the question explicit myself and get it confirmed."
**Clarify first:** Who owns the data, what does each column mean, what is one row (an order, an employee, a day)? What decision might this serve? If nobody can say, I propose my best guess and ask.
**Plan:**
1. Define the question and the decision.
2. Understand the data: row count, columns, date range, data dictionary.
3. Clean: duplicates, missing values, odd formats, impossible values; log every change.
4. Explore: totals, distributions, trends, simple cuts.
5. Analyse: compare groups or time periods; test the one or two leads.
6. Check: reconcile totals to a known source; sanity-test numbers.
7. Recommend: finding, size of impact, action, caveats.
**Method choice and why:** Simple counts, averages, trends and comparisons first; models only if a simple view cannot answer the question.
**Pitfalls:** Hunting for patterns with no question (you will find false ones); silent cleaning; reporting without a baseline.
**Deliverable:** A one-page summary plus a workbook or query that someone else can rerun.
**Likely follow-ups:** 1) *Which step do you spend most time on?* Understanding and cleaning the data. 2) *When do you stop exploring?* When I can answer the question with evidence I would defend.
**Common mistakes / traps:** Jumping to modelling; no documentation; ending with charts and no recommendation.

### Q3 ⭐⭐⭐ 🟢 How would you analyse why customers are leaving (churn) for a subscription business, and how would you define churn before you start?
**Asked at:** commonly asked; cohort, funnel and retention prompts appear in prep guides (e.g. PracHub, unverified).
**What the interviewer is checking:** Whether you define churn precisely and then look for where and why it happens, without claiming cause too early.
**Say this in the interview:** "First I define churn exactly: a paying customer with no active subscription for a set window, say 30 days after expiry. Then I measure the monthly rate by cohort and segment to see who leaves and when."
**Clarify first:** Voluntary (cancelled) or involuntary (card failed)? Do pauses count? Is the goal a rate (share lost per month) or the reasons? Which decision follows: pricing, onboarding, support?
**Plan:**
1. Fix the definition: churn rate = customers lost in the month / customers active at the start of the month.
2. Build the data: customer id, start date, end date, plan, price, channel, usage, support tickets, payment failures.
3. Compute the churn rate by month, then by signup cohort, plan, channel and city.
4. Look at the timing: early churn (first 30 to 60 days) points to onboarding or wrong fit; steady churn points to value or price.
5. Compare leavers with stayers on usage in the first weeks, tickets, failed payments.
6. Add exit-survey reasons if they exist.
**Method choice and why:** Cohort tables and segment comparisons first. A churn prediction model only after I know what to act on.
**Pitfalls:** Mixing a monthly rate with an annual one; counting involuntary failures as dissatisfaction; survivorship (only looking at current customers); confusing correlation with cause.
**Deliverable:** A churn definition note, a cohort chart, the top two or three segments driving loss, suggested tests (e.g. onboarding fix, payment retry).
**Likely follow-ups:** 1) *Why does the definition matter?* A 30-day versus a 90-day window changes the rate and the story. 2) *What is the cheapest quick win?* Often fixing failed-payment retries.
**Common mistakes / traps:** No definition; one blended rate that hides cohort differences; jumping to a model.

### Q4 ⭐⭐⭐ 🟢 How would you analyse employee attrition in a company of 2,000 people to tell HR where the problem is?
**Asked at:** commonly asked; HR and people-analytics question banks list attrition diagnosis (startup.jobs bank, unverified).
**What the interviewer is checking:** Whether you use rates (not counts), cut sensibly, and find the pocket where the problem sits.
**Say this in the interview:** "I would define attrition as leavers in a period divided by average headcount, then split it by tenure, department, manager, grade and leaver type to find where it is concentrated, comparing rates and not raw counts."
**Clarify first:** Voluntary or involuntary? Is the concern the overall rate or a specific team? Which period? Any recent change (pay cycle, policy, reorganisation)? What counts as a leaver (resignation, termination, contract end)?
**Plan:**
1. Pull the HRIS export: employee id, join date, exit date, exit reason, department, location, grade, manager, pay band, performance rating.
2. Clean: duplicate ids, missing exit dates, rehires, transfers.
3. Compute the overall rate = leavers / average headcount, for example the last 12 months and the trend by month.
4. Cut by tenure band (0 to 6 months, 6 to 12 and so on), department, location, grade, manager.
5. Separate regretted exits (high performers) from the rest.
6. Check pay position against the band and exit-interview themes.
**Method choice and why:** Rate tables and a simple heatmap. A model is not needed to tell HR where; to find why, add exit reasons and surveys.
**Pitfalls:** Comparing counts across teams of different size; tiny teams with large swings; ignoring seasonality (appraisal and bonus cycles); treating correlation as cause.
**Deliverable:** A one-page view: overall rate, the 2 or 3 hotspots with rates and headcount, likely reasons, a suggested action, and the follow-up measure.
**Likely follow-ups:** 1) *What if the overall rate is normal?* A hotspot can still exist in one team or tenure band. 2) *Are all exits bad?* No; separate regretted from non-regretted exits.
**Common mistakes / traps:** Counts without headcount; one blended number; confidentiality ignored when showing small teams.

### Q5 ⭐⭐⭐ 🟢 How would you analyse a sales funnel (lead, qualified, proposal, won) to find where the biggest loss is?
**Asked at:** commonly asked; funnel prompts are common in case guides (unverified, no company-specific report found).
**What the interviewer is checking:** Whether you compute stage conversion, tell relative loss from absolute loss, and segment before concluding.
**Say this in the interview:** "I would count leads at each stage, compute conversion stage to stage and overall, and then segment by source, region and rep to see whether the leak is everywhere or in one pocket."
**Clarify first:** One time window or cohort of leads? Are the stage definitions consistent? How long is a typical sales cycle? Is the aim more wins or higher quality?
**Plan:**
1. Count each stage for a lead cohort (leads created in the same month), so late wins are not missed.
2. Compute stage conversion (qualified / leads, proposal / qualified, won / proposal) and overall (won / leads).
3. Compare each drop in relative terms and in absolute volume lost.
4. Cut by source, region, rep, deal size.
5. Look at time spent in each stage.
6. Check loss reasons where recorded.
**Method choice and why:** Simple funnel table and a bar chart. The biggest relative loss is not always the most valuable one to fix: weigh by the revenue at stake and how fixable the stage is.
**Pitfalls:** Mixing leads from different months (the cycle lag makes recent months look weak); inconsistent stage definitions across reps; ignoring deal value.
**Deliverable:** The funnel table, the top leak, the segment where it is worst, a proposed fix and a metric to track.
**Likely follow-ups:** 1) *Biggest percentage drop or biggest count drop?* Show both, then judge by revenue at stake. 2) *How do you test a fix?* Compare the stage conversion before and after, with a comparison group if possible.
**Common mistakes / traps:** Using stage-to-stage and overall rates interchangeably; ignoring cohort timing.

### Q6 ⭐⭐⭐ 🟢 How would you analyse the performance of a marketing campaign that ran for two weeks?
**Asked at:** commonly asked; campaign-effectiveness questions recur in marketing-analytics banks (unverified).
**What the interviewer is checking:** That you define success first, use a baseline, and avoid crediting the campaign for what would have happened anyway.
**Say this in the interview:** "I would agree the goal metric first (sales, sign-ups, cost per customer), then compare the campaign period with a baseline, ideally a comparison group, and look at cost against incremental result."
**Clarify first:** What was the goal and target? Which channels, audience and spend? Were prices, stock or other campaigns changing at the same time? How long after exposure do purchases still count?
**Plan:**
1. Define metrics: reach, clicks, conversions, cost per conversion, revenue, and return (revenue / spend).
2. Choose a baseline: the two weeks before, the same weeks last year, and a holdout or unexposed group if available.
3. Compute the lift = campaign result minus expected baseline.
4. Break down by channel, audience, creative, city.
5. Check customer quality (repeat rate, returns), not just first purchase.
6. Compare cost per incremental customer with the target.
**Method choice and why:** Before and after plus a comparison group is simple and robust. Use a proper test or difference-in-differences only if the data allows.
**Pitfalls:** Counting all sales in the window as caused by the campaign; ignoring seasonality or festivals; vanity metrics (impressions); short windows hiding repeat behaviour.
**Deliverable:** A one-page summary: result against goal, estimated incremental effect, best and worst channels, a recommendation to scale, fix or stop.
**Likely follow-ups:** 1) *What if no control group exists?* Use past weeks and similar markets, and state the weaker claim. 2) *What is incremental?* Sales that would not have happened without the campaign.
**Common mistakes / traps:** No baseline; reporting clicks as success; ignoring cost.

### Q7 ⭐⭐⭐ 🟢 A stakeholder asks you to 'find insights' in an HRIS export of employees. How do you decide what to analyse and what to leave out?
**Asked at:** commonly asked in HR and people-analytics prep banks (unverified, no company-specific report found).
**What the interviewer is checking:** Judgement: tying analysis to decisions, and handling sensitive data responsibly.
**Say this in the interview:** "I would ask which decisions HR is facing, pick two or three questions tied to them, and leave out anything that is sensitive, not needed or too thin to be reliable."
**Clarify first:** What worries leadership (attrition, pay, hiring, diversity)? Who sees the output? What may be used legally and by policy (consent, purpose)? What is the deadline?
**Plan:**
1. List the HRIS fields and check completeness and definitions.
2. Choose priority questions, for example attrition by tenure, headcount trend, pay against band.
3. Run basic profiling: counts, missing rates, duplicates.
4. Run the chosen cuts; look for large, actionable differences.
5. Leave out: fields with heavy missing data, tiny groups that identify individuals, and sensitive attributes unless the purpose and approval are clear.
6. Share findings in aggregate.
**Method choice and why:** Descriptive summaries and rate comparisons are enough for most HR questions; I confirm data-privacy rules with the HR and legal teams (I do not assume the rule from memory).
**Pitfalls:** "Insights" with no action; chasing every column; small-group results that expose individuals; mixing personal data into broad reports.
**Deliverable:** A short brief of three insights, each with the number, why it matters and a suggested action, plus a list of what was excluded and why.
**Likely follow-ups:** 1) *How do you avoid privacy problems?* Aggregate, set a minimum group size (confirm the number with policy), and limit access. 2) *What if they insist on more?* Agree a second round of questions.
**Common mistakes / traps:** Analysing everything; showing individual-level data; no link to a decision.

### Q8 ⭐⭐⭐ 🟢 How would you analyse whether a new onboarding programme improved new-hire retention, and what are the limits of what you can claim?
**Asked at:** commonly asked in HR-analytics banks (program evaluation with a comparison group, unverified).
**What the interviewer is checking:** Whether you compare like with like and are honest about causal limits.
**Say this in the interview:** "I would compare 90-day retention for people who joined before and after the programme, or those who got it and those who did not, check the groups are similar, and say what I can and cannot prove."
**Clarify first:** When did it start? Was it for everyone or some teams? What is retention here (still employed at 90 days, 6 months)? What else changed (hiring source, pay, manager)?
**Plan:**
1. Define retention: share still employed at day 90 of those who joined.
2. Split new hires into programme and comparison groups (by date or by team).
3. Compare the retention rates and the absolute difference in percentage points.
4. Check the groups on role, location, source, grade, and the period of joining.
5. Look at the number of hires; with small counts, show the range and not a single number.
6. Check supporting measures (training completion, manager feedback, early performance).
**Method choice and why:** Simple rate comparison, then a comparison between matched teams. Only go to regression if there are enough hires.
**Pitfalls:** The time effect (market or season changes); selection (better managers opted in); too-recent joiners not yet at day 90; small samples.
**Deliverable:** Retention rates for both groups, the gap, a clear sentence such as "retention was higher after the programme; we cannot prove the programme caused it because..." and a pilot design for stronger evidence.
**Likely follow-ups:** 1) *How would you prove causality?* Randomise or stagger the rollout across teams. 2) *What if the difference is 3 points on 40 hires?* Too small to be conclusive; say so.
**Common mistakes / traps:** Claiming causation from before and after; including people who have not reached day 90.

### Q9 ⭐⭐⭐ 🟢 How would you analyse monthly sales performance across regions to decide which region needs attention?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Fair comparison: against target, last year and region size, not raw totals.
**Say this in the interview:** "I would compare each region with its own target and last year's same month, not with other regions' totals, then see whether the gap comes from volume, price or mix."
**Clarify first:** What does "attention" mean: below target, declining, or loss-making? What is the target, and was it set fairly? Is the region's market size comparable?
**Plan:**
1. Build a table: region by month with sales, target, last-year same month.
2. Compute % to target and year-on-year growth, plus the 3-month trend.
3. Separate size from performance (growth rate and share of target, not totals).
4. Decompose the gap: orders, average order value, product mix, customers.
5. Check one-off effects (festival timing, stock-outs, a big deal).
6. Rank by revenue at risk.
**Method choice and why:** A simple variance table and trend lines; add per-capita or per-rep measures when regions differ in size.
**Pitfalls:** Ranking by totals; one month of noise; unfair targets; unequal working days.
**Deliverable:** A region scorecard with a flag, the cause for each flagged region, and a suggested next step.
**Likely follow-ups:** 1) *What if the biggest region is flat?* A flat large region may matter more in rupees than a small shrinking one. 2) *How many months do you look at?* At least three, to avoid acting on noise.
**Common mistakes / traps:** Total-based ranking; ignoring seasonality; no root-cause split.

### Q10 ⭐⭐⭐ 🟢 What is the difference between a descriptive, a diagnostic, a predictive and a prescriptive analysis, and which one is the request 'why did attrition rise' asking for?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know the four types and match a request to the right one.
**Say this in the interview:** "Descriptive says what happened, diagnostic says why, predictive says what is likely next, prescriptive says what to do. 'Why did attrition rise' is diagnostic, though I would start with the descriptive facts."
**Clarify first (what each type answers):**
- **Descriptive:** what happened (attrition was 14% last quarter, up from 11%; this is an example, not real data).
- **Diagnostic:** why (the rise sits in the first six months of tenure in one location).
- **Predictive:** what is likely to happen (who is likely to leave next quarter).
- **Prescriptive:** what to do (which action, for whom, at what cost).
**Plan for the attrition request:** confirm the rise is real (descriptive: rate, period, definition); locate it (cuts by tenure, department, manager); find reasons (exit data, pay, survey); recommend a test, which borders on prescriptive.
**Method choice and why:** Diagnostic work uses comparisons and breakdowns; I do not need a model to answer why, and one would only predict.
**Pitfalls:** Calling a model prediction an explanation; skipping the descriptive step; treating a correlation as the diagnosis.
**Deliverable:** A short answer that names the type, shows the evidence, and states the limit ("this suggests, it does not prove").
**Likely follow-ups:** 1) *Which is hardest?* Prescriptive, since it needs costs and tests. 2) *Can one project use all four?* Yes, in order.
**Common mistakes / traps:** Mixing up diagnostic and predictive; going straight to a model.

### Q11 ⭐⭐⭐ 🟢 What do you check in the data before you start any analysis, and why does that come before charts or models?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Data-quality discipline; that you know bad data produces confident wrong answers.
**Say this in the interview:** "I check size, definitions, duplicates, missing values, ranges and totals against a trusted source, because a chart or model on bad data looks convincing and is wrong."
**Clarify first:** What is one row? What is the date range and the source? Who owns it and when was it refreshed?
**Plan (checks in order):**
1. Row and column count against what I expected.
2. Meaning of each column and its data type (dates stored as text, numbers as text).
3. Duplicates (same id repeated).
4. Missing values: how many, and whether they are random or concentrated.
5. Range and impossible values (negative age, exit date before join date).
6. Consistency (spelling variants such as "Mumbai" and "Bombay"; units; currency).
7. Reconcile totals to a known figure (finance, payroll).
**Method choice and why:** Simple counts, filters and a pivot are enough; the aim is to decide what can be trusted.
**Pitfalls:** Silent deletion of odd rows; assuming a pipeline is correct; filling missing values without telling anyone.
**Deliverable:** A short data-quality log: issue, count, action taken, impact on results.
**Likely follow-ups:** 1) *What if you cannot fix it?* Report it as a caveat and quantify the affected share. 2) *Why before models?* Models amplify errors without flagging them.
**Common mistakes / traps:** Skipping straight to charts; cleaning without a log; no reconciliation.

### Q12 ⭐⭐⭐ 🟢 How would you analyse a table of order data to find the top 10 customers, and what must you decide about 'top' before you run it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you define "top" (by what, over what period) and handle data traps like returns and duplicate ids.
**Say this in the interview:** "I would first agree what 'top' means, usually net revenue in a fixed period, after returns, then group orders by customer and sort, after checking duplicates and customer id quality."
**Clarify first:** Top by revenue, profit, order count or frequency? Which period? Net of returns and cancellations? Should a company with several accounts be counted as one?
**Plan:**
1. Clean the table: drop duplicate order rows, remove cancelled orders, handle returns.
2. Standardise customer ids (one person with two ids).
3. Aggregate per customer: total net revenue, number of orders, last order date.
4. Sort descending and take the top 10 (SQL: GROUP BY customer_id ORDER BY revenue DESC LIMIT 10).
5. Check ties at rank 10 and each customer's share of the total.
6. Sanity-check that the top 10 are sensible (not test accounts).
**Method choice and why:** A simple aggregation. If revenue is concentrated, show cumulative share (for example, top 10 account for X% of sales).
**Pitfalls:** Ranking by gross including returns; ignoring ties; test or internal accounts; one big one-off order mistaken for a loyal customer.
**Deliverable:** A table of the top 10 with revenue, orders, share of total and last purchase, and the rule used for "top".
**Likely follow-ups:** 1) *Revenue or profit?* Profit if the margins differ widely. 2) *How do you handle ties?* Show all tied customers and say so.
**Common mistakes / traps:** Not defining top; counting returns as revenue.

### Q13 ⭐⭐⭐ 🟢 A funnel for one month is below. Which stage has the biggest relative drop, and what is the overall conversion from visit to purchase?
Inline data: Visits 50,000; add to cart 6,000; checkout started 3,000; purchase 1,200 (exercise data).
**Asked at:** commonly asked (no company-specific report found); funnel drop-off questions are common in e-commerce guides.
**What the interviewer is checking:** Stage-to-stage conversion arithmetic and the relative versus absolute distinction.
**Say this in the interview:** "The biggest relative drop is visit to add-to-cart: only 12% continue, so 88% are lost. Overall conversion is 1,200 / 50,000 = 2.4%."
**What the data shows:** Each stage keeps a share of the one before. Most people never add anything to the cart; of those who do, half start checkout; of those who start checkout, 40% buy.
**Working:**
1. Visit to cart: 6,000 / 50,000 = 12.0%, so the drop is 88.0%.
2. Cart to checkout: 3,000 / 6,000 = 50.0%, so the drop is 50.0%.
3. Checkout to purchase: 1,200 / 3,000 = 40.0%, so the drop is 60.0%.
4. Overall: 1,200 / 50,000 = 2.4%. Check: 0.12 x 0.50 x 0.40 = 0.024.
**Result:** Biggest relative drop: visit to cart (88%). Overall conversion: 2.4% (visit to purchase). Among the later steps, checkout to purchase loses the most (60%).
**Caveats / what else I would check:** Visits to cart is naturally low because many visitors are browsing, so its 88% is not necessarily a problem; the later stages are closer to purchase intent. Check whether visits are counted as sessions or people, bots and device mix, and whether the month is typical. A benchmark for each stage would help judge what is "bad".
**Next step / recommendation:** Focus first on checkout to purchase (payment failures, shipping cost surprises), where intent is highest, and test product-page improvements for the cart step; track each stage rate by device.
**Likely follow-ups:** 1) *Relative or absolute?* Visit to cart loses 44,000; checkout to purchase loses 1,800; both views matter. 2) *Is 2.4% good?* Depends on the category; compare against the past, not an unverified benchmark.
**Common mistakes / traps:** Calling the stage with the biggest count loss the problem without context; adding stage rates instead of multiplying; percentage versus percentage-point confusion.

### Q14 ⭐⭐⭐ 🟢 Two regions are compared below. Which has the better conversion, and what would you check before saying one team is better?
Inline data: Region A: 400 leads, 60 won. Region B: 1,000 leads, 120 won (exercise data).
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Using rates not counts, and then questioning whether the comparison is fair and not just noise.
**Say this in the interview:** "Region A converts 15% and Region B 12%, so A looks better by 3 percentage points, even though B won more deals. Before calling A's team better I would check lead quality, mix, deal size and whether the gap could be chance."
**What the data shows:** B won more deals (120 against 60) because it had many more leads; the rate is what compares performance.
**Working:**
1. Region A: 60 / 400 = 15.0%.
2. Region B: 120 / 1,000 = 12.0%.
3. Gap: 15.0% minus 12.0% = 3.0 percentage points (a relative advantage of 25% for A).
4. Rough check of noise (done by script, for the idea only): the 95% range for the gap is about minus 1.0 to plus 7.0 points, and a two-group test gives a p-value of about 0.13, so the gap could be chance.
**Result:** A converts better (15% versus 12%), but the evidence that A's team is better is weak with these numbers.
**Caveats / what else I would check:** Lead source and quality (A might get warmer leads); product and deal-size mix; lead age and time to follow up; rep experience and number of reps; sales cycle length (are all leads old enough to have closed?); revenue per lead, not only count won.
**Next step / recommendation:** Compare rates by lead source within each region and revenue per lead; check again with a few more months before rewarding or changing anything.
**Likely follow-ups:** 1) *Percentage or percentage-point?* The gap is 3 points; relatively A is 25% higher. 2) *Would you reward A?* Not on this alone.
**Common mistakes / traps:** Comparing won counts; ignoring sample size; calling a 3-point gap significant without checking.

### Q15 ⭐⭐⭐ 🟡 A store chain offered a discount in 10 stores and not in 10 others. Sales rose in the discount stores. How would you analyse whether the discount caused the rise?
**Asked at:** commonly asked; experiment and causal-inference prompts appear in guides (unverified).
**What the interviewer is checking:** That you use a comparison group and check how the stores were chosen before claiming cause.
**Say this in the interview:** "I would compare the change in sales in the discount stores with the change in the other stores over the same period, and first check how the 10 stores were picked, because that decides how much I can claim."
**Clarify first:** Were the stores chosen at random or by management? When did the discount start? Were sales per store trending up before it? Any other changes (local events, stock, ads)? Did the discount affect margin?
**Plan:**
1. Collect weekly sales per store for several weeks before and after.
2. Check that both groups looked similar before (size, city type, trend).
3. Compute the change per store, then the average change for each group.
4. Difference-in-differences: (discount stores' change) minus (other stores' change).
5. Check consistency: do most discount stores rise, or is one big store driving the average?
6. Look at margin and basket, not only sales; check for pull-forward (a dip after the offer ends) and cannibalisation of neighbours.
**Method choice and why:** Before and after plus a comparison group is simple and strong. If stores were randomly assigned, the claim is much stronger; if hand-picked, state the weaker claim.
**Pitfalls:** Looking at the discount stores alone; picking the best stores; seasonality and festivals; only 10 stores means noise; measuring revenue without profit.
**Deliverable:** The estimated extra sales per store, its uncertainty, margin impact, and a recommendation to scale, retest or stop.
**Likely follow-ups:** 1) *What if the groups differ?* Match stores on size and past trend. 2) *Is a rise in sales a win?* Only if extra margin exceeds the discount cost.
**Common mistakes / traps:** No comparison group; ignoring selection; reporting sales without margin.

### Q16 ⭐⭐⭐ 🟡 How would you analyse the hiring funnel of a company that says it is 'taking too long to hire'?
**Asked at:** commonly asked in HR-analytics banks (funnel by stage, unverified).
**What the interviewer is checking:** That you measure time per stage, define the clock, and find where waiting happens.
**Say this in the interview:** "I would define time-to-hire clearly, measure days spent in each stage, and compare by role and recruiter to find where the waiting really is, before blaming anyone."
**Clarify first:** What does "too long" mean: compared with what target or past period? Time to fill (from requisition approval to offer acceptance) or time to hire (from applicant first contact)? Which roles?
**Plan:**
1. Pull the applicant tracking system (ATS) data: requisition date, applied, screened, interviewed, offered, accepted, joined.
2. Clean dates, duplicates, withdrawn candidates.
3. Compute median days per stage and in total (median, because a few very long cases skew the mean).
4. Cut by role family, location, hiring manager, recruiter, source.
5. Separate waiting time (feedback delays, scheduling) from process time.
6. Check conversion and drop-off by stage, offer declines, and the share of requisitions on hold.
7. Compare with the stated target.
**Method choice and why:** Medians and a stage-wise table; a bar chart of days per stage shows the bottleneck immediately.
**Pitfalls:** Mixing time-to-fill and time-to-hire; counting only completed hires (survivorship: stuck requisitions are missed); mean skewed by outliers; role mix.
**Deliverable:** A stage-by-stage time chart, the bottleneck (for example, interview feedback), who and what drives it, and two fixes with a measure.
**Likely follow-ups:** 1) *Why median?* Robust to a few very slow hires. 2) *Do offers declined matter?* Yes, they restart the clock.
**Common mistakes / traps:** One average for all roles; ignoring open requisitions.

### Q17 ⭐⭐⭐ 🟡 How would you analyse customer retention using a cohort table, and what would you look for in it?
**Asked at:** commonly asked; PracHub-style cohort and retention pages exist (unverified).
**What the interviewer is checking:** That you can read a cohort table: rows, columns and patterns.
**Say this in the interview:** "A cohort table groups customers by when they joined and shows the share still active in each later month, so I can see whether newer cohorts retain better or worse and where the curve flattens."
**Clarify first:** What counts as "active" (purchase, login, paid)? Monthly or weekly cohorts? How many customers per cohort?
**Plan:**
1. Assign each customer to a start-month cohort.
2. Count, for each cohort, how many are active in month 0, 1, 2, and so on.
3. Convert to a percentage of the cohort's month-0 size.
4. Read across rows (one cohort over time) and down columns (cohorts at the same age).
5. Compare the curves of cohorts by channel or plan.
**Method choice and why:** A heatmap-coloured table is enough. The patterns to look for: a steep drop in month 1 (onboarding problem); a curve that flattens (a loyal core); newer cohorts worse than older ones (quality of acquisition is falling); a diagonal dip (a calendar event hit every cohort).
**Pitfalls:** Reading the incomplete latest cells as drops; tiny cohorts; mixing cohort age with calendar time; blending channels.
**Deliverable:** A cohort heatmap, the retention at months 1, 3, 6, the key pattern, and a hypothesis to test.
**Likely follow-ups:** 1) *Why cohorts and not one average?* An overall average hides whether the product is getting better. 2) *What if a cohort drops at month 3 only?* Check what happens then (trial ends, price change).
**Common mistakes / traps:** Misreading recent incomplete months; not defining active.

### Q18 ⭐⭐⭐ 🟡 How would you analyse the drop-off in an e-commerce checkout flow when the overall conversion looks stable?
**Asked at:** commonly asked; cart abandonment is a theme in Swiggy, Meesho and Flipkart guides (unverified).
**What the interviewer is checking:** That a stable total can hide offsetting changes (mix effects) and that you break it down.
**Say this in the interview:** "A stable overall rate can hide one segment getting worse and another better, or a change in traffic mix, so I split the funnel by device, source and step before deciding there is no issue."
**Clarify first:** Stable against what? Is the aim to improve conversion anyway? Any recent change (payment gateway, app release, shipping fee)?
**Plan:**
1. Build the checkout funnel step by step (cart, address, payment, confirmation).
2. Compute step conversion by device, new versus returning, source, payment method, city.
3. Compare with earlier weeks; check the mix of traffic (share of mobile, new users).
4. Find steps where one segment is far below the others (for example payment on Android).
5. Check errors, load times, payment failure codes, coupon use.
6. Size each leak: users lost times average order value.
**Method choice and why:** Segmented funnel tables. Simpson's paradox is the key idea: the overall rate can stay flat because the mix shifts while each segment moves.
**Pitfalls:** Looking only at the headline; treating all drop-offs as customer choice when some are technical errors; ignoring order value.
**Deliverable:** A table of segment by step with the largest recoverable leak, its size in rupees, and a fix to test.
**Likely follow-ups:** 1) *What is a mix effect?* The blend of segments changes, so the total hides segment moves. 2) *How do you prioritise fixes?* By recoverable revenue and ease.
**Common mistakes / traps:** Stopping at the stable number; no segmentation.

### Q19 ⭐⭐⭐ 🟡 Your manager wants to know which products to stock more of. How would you analyse the sales data to answer that?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you consider demand, margin and stock availability, not just sales rank.
**Say this in the interview:** "I would look at sales trend, margin and how often each product was out of stock, because a product that sold out looks weaker than its real demand. Then I rank by profit potential."
**Clarify first:** Stock more for what period? Any storage or cash limits? Is the goal revenue, profit or availability? Are there lead times from suppliers?
**Plan:**
1. Aggregate sales by product and week: units, revenue, margin.
2. Classify products (for example ABC by revenue share) and check trend and seasonality.
3. Adjust for stock-outs: days out of stock mean demand was censored (hidden).
4. Calculate sell-through and days of stock cover.
5. Check returns, discount dependence and margin.
6. Shortlist products with rising or steady demand, good margin, and low cover.
**Method choice and why:** A simple ranked table with cover and margin. A forecast is a second step only for the shortlist.
**Pitfalls:** Ranking by units only; ignoring stock-outs; chasing a promo spike; ignoring the cost of holding stock.
**Deliverable:** A shortlist with suggested quantities (with assumptions), expected profit, and the risk.
**Likely follow-ups:** 1) *What if the data lacks stock-outs?* Ask for inventory records; otherwise note the limit. 2) *Revenue or margin?* Margin per unit of shelf space or cash.
**Common mistakes / traps:** Stocking the best seller blindly; ignoring seasonality.

### Q20 ⭐⭐⭐ 🟡 How would you analyse absenteeism across a 300-person plant to find out whether it is a problem and where?
**Asked at:** commonly asked in HR banks (absenteeism as a burnout signal, unverified).
**What the interviewer is checking:** Defining the rate properly, comparing against a baseline, handling small groups and avoiding blame.
**Say this in the interview:** "I would define the absence rate as days absent divided by scheduled working days, compare it with the past and across teams and shifts, and separate planned leave from unplanned absence."
**Clarify first:** Does "absent" include approved leave, sick leave, or unplanned only? Which period? Is there a policy threshold or past benchmark? Why is it a concern now (production, cost)?
**Plan:**
1. Pull attendance data: employee, date, status (present, leave type, absent), shift, department.
2. Clean: duplicates, missing days, holidays and weekly offs.
3. Compute absence rate = absent days / scheduled days, by month.
4. Cut by shift, department, supervisor, day of week, tenure.
5. Check patterns: Mondays and Fridays, after pay day, around festivals, repeat short absences.
6. Look at concentration: a few employees with many days versus broad spread.
**Method choice and why:** Rate tables and a day-of-week chart. With only 300 people, small teams have noisy rates, so look at several months and avoid reacting to one.
**Pitfalls:** Counting leave as absence; ignoring seasonal illness; comparing counts across teams of different size; naming individuals in a general report.
**Deliverable:** The plant absence rate and trend, the two or three hotspots, the likely drivers, and a proposed action with a measure.
**Likely follow-ups:** 1) *Is it a problem?* Compare against the plant's own history and any internal target. 2) *Individual or systemic?* If a few people drive it, handle individually; if broad, look at working conditions.
**Common mistakes / traps:** No definition; a single month of data; stigma-driven conclusions.

### Q21 ⭐⭐⭐ 🟡 A senior asks, 'Is our new feature working?' What clarifying questions do you ask, and how do you analyse it?
**Asked at:** commonly asked in product-analytics case guides (unverified).
**What the interviewer is checking:** That you define "working", pick a success metric and a comparison, and consider side effects.
**Say this in the interview:** "I would first ask what 'working' means for this feature: which metric should move, by how much, and over what time. Then I compare users who used it with a fair comparison group and check side effects."
**Clarify first:** What was the feature meant to do? Success metric and target? Launch date and who has access? Was it a staged rollout or an A/B test? Any other changes at launch?
**Plan:**
1. Define one primary metric (for example conversion, retention, time to complete) and a guardrail metric (for example complaints, speed).
2. Measure adoption: share of users who tried it, and repeat use.
3. Compare outcomes: A/B groups if available; otherwise before and after with a comparison group.
4. Check users who adopt are not just the most engaged (self-selection).
5. Segment by user type, device and new versus old.
6. Look for side effects and novelty wear-off over several weeks.
**Method choice and why:** A randomised test is the best evidence; without one, state clearly that the result is suggestive.
**Pitfalls:** Comparing users of the feature to non-users; the novelty effect; too short a window; ignoring guardrails.
**Deliverable:** A verdict (working, not working, unclear), the effect with its range, the segments, and a next step.
**Likely follow-ups:** 1) *What if no test?* Use a staged rollout and difference-in-differences. 2) *How long to wait?* Until behaviour stabilises, often at least a few weeks (judge by the product).
**Common mistakes / traps:** Adoption mistaken for impact; self-selection.

### Q22 ⭐⭐⭐ 🟡 You find a strong correlation between employees who attend training and employees who get promoted. How do you analyse whether the training causes promotion?
**Asked at:** commonly asked in people-analytics banks (correlation versus causation, unverified).
**What the interviewer is checking:** That you spot selection and confounding and know what evidence would support causation.
**Say this in the interview:** "A correlation does not show cause: ambitious, high-performing people may both choose training and get promoted. I would compare like with like and test whether training adds anything after accounting for performance and manager."
**Clarify first:** Who is selected for training (volunteers, nominated by managers)? Timing: did training come before promotion? What are the promotion criteria? How many people?
**Plan:**
1. Check the order of events: training date before promotion date.
2. List confounders: past performance rating, tenure, grade, manager, department, potential.
3. Compare promotion rates for trained and untrained employees within the same performance band and grade.
4. Use matching or a regression adjusted for those factors (if the numbers allow).
5. Look for a natural experiment: seats limited by lottery or a rollout staggered by chance.
6. Check the result is not driven by one department.
**Method choice and why:** Stratified comparison first (simple and explainable). A matched or regression analysis only to refine.
**Pitfalls:** Reverse causation (people about to be promoted get sent to training); hidden confounders such as motivation; small groups; confusing "no effect" with "no evidence".
**Deliverable:** A statement such as "trained employees are promoted more often, and the gap shrinks to X after matching, so training may help but we cannot prove it", plus a design for a cleaner test.
**Likely follow-ups:** 1) *How would you prove it?* Randomise access to training. 2) *If the gap disappears after matching?* Then the correlation was mostly selection.
**Common mistakes / traps:** Claiming training causes promotion; ignoring who gets nominated.

### Q23 ⭐⭐⭐ 🟡 How would you segment customers for a retailer to support marketing decisions, and how would you check the segments are useful?
**Asked at:** commonly asked; RFM segmentation appears in e-commerce guides (one source unverified).
**What the interviewer is checking:** That segments are tied to action, simple, stable and measurably different.
**Say this in the interview:** "I would start with a simple RFM view (recency, frequency, monetary value) and check each segment differs in behaviour and can be targeted with a different action, otherwise it is just labelling."
**Clarify first:** What marketing decision will use the segments (offers, channel, retention)? How many segments can the team handle? What data exists (purchases, channel, category)?
**Plan:**
1. Build per-customer features: days since last purchase, number of orders, total spend, categories bought.
2. Score each of R, F and M into bands (for example quintiles) and combine into a few named groups (champions, loyal, at risk, lost, new).
3. Profile each segment: size, share of revenue, average order value, return rate.
4. Test usefulness: do segments respond differently to offers (a past campaign), and are they stable month to month?
5. Check segments are big enough and distinct.
6. Attach an action to each segment.
**Method choice and why:** Rules-based RFM is explainable to a marketing team. Clustering (for example k-means) is an option when many variables exist, but the output must still be named and actionable.
**Pitfalls:** Too many segments; segments that look different but need the same action; unstable assignments; ignoring outliers.
**Deliverable:** A segment table (size, revenue share, behaviour), the proposed action per segment and a test plan with a measure.
**Likely follow-ups:** 1) *How do you know it works?* Test an offer by segment against a control. 2) *RFM or clustering?* RFM first for clarity.
**Common mistakes / traps:** Segmenting with no action; unexplainable clusters.

### Q24 ⭐⭐⭐ 🟡 When would you use a median instead of a mean in an analysis, and how do you decide when your data has outliers that need treatment?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Understanding of skew and outliers, and a cautious, documented approach to treating them.
**Say this in the interview:** "I use the median when the data is skewed or has extreme values, such as salaries or order values, because the mean gets pulled by a few big ones. I treat outliers only after finding out whether they are errors or real."
**Explain simply:**
- Mean: add up and divide; sensitive to extremes. Median: the middle value; robust.
- Mini-example (salary in thousands per month, 10 employees, exercise data): 28, 30, 32, 35, 36, 40, 45, 50, 52, 400. Mean = 74.8; median = 38. One executive pulls the mean far above what a typical person earns.
- Use the median for pay, order value, resolution time, time to hire; use the mean for totals and for roughly symmetric data. Often report both.
**Deciding on outliers:**
1. Spot them: sorted values, a box plot, or the 1.5 x IQR rule (a rule of thumb, not law).
2. Investigate: a typing error (extra zero), a test record, or a real extreme (a bulk buyer)?
3. Act: fix or remove errors with a log; keep real values but report them separately or use robust measures (median, trimmed mean); never delete just because they spoil the picture.
4. Show the result with and without them to check how much they matter.
**Practice step:** take any order-value column, compute mean and median, and see which one matches a "typical" order.
**Likely follow-ups:** 1) *Does removing outliers always help?* No; it can hide your best customers. 2) *Mean and median very different means?* The data is skewed.
**Common mistakes / traps:** Deleting outliers silently; using only the mean for skewed data; assuming every extreme is an error.

### Q25 ⭐⭐⭐ 🟡 How would you analyse a survey with a 22 percent response rate before presenting results to leadership?
**Asked at:** commonly asked in HR-analytics banks (survey bias, unverified).
**What the interviewer is checking:** Awareness of non-response bias and honest presentation of limits.
**Say this in the interview:** "A 22 percent response rate means 78 percent are silent, and they may think differently. I would compare respondents with the whole population, present results with that caveat, and avoid over-claiming."
**Clarify first:** Who was invited, and how? Was it anonymous? Which groups responded (by department, tenure, location)? Is the survey a repeat, so I can compare with earlier response rates? What decision depends on it?
**Plan:**
1. Compute the response rate overall and by group (department, tenure, grade).
2. Compare respondent mix with the workforce mix to see who is over- or under-represented.
3. Look for patterns: did unhappy or very happy people respond more? Compare with last year's response.
4. Report counts alongside percentages, and a margin of error. Example for scale: if 1,000 were invited, 22% is 220 responses; at best the margin is about plus or minus 6.6 percentage points (95%, simple random assumption, which does not hold if bias exists).
5. Optionally weight results so groups match the workforce, if the groups differ a lot.
6. Treat free-text themes as directional.
**Method choice and why:** Descriptive results with clear caveats. Weighting corrects for known group imbalance but not for unknown bias.
**Pitfalls:** Presenting percentages as if everyone answered; ignoring that responders differ; small groups; reading small changes as real.
**Deliverable:** Results with the response rate on the first line, the groups covered, the caveat in plain words, and a suggestion to boost participation and follow up with focus groups.
**Likely follow-ups:** 1) *Is 22 percent too low?* It depends on the population and past rates; I would not set a fixed cutoff from memory. 2) *What reduces bias?* Reminders, assurance of anonymity, short surveys, follow-up with non-responders.
**Common mistakes / traps:** Treating respondents as representative; no caveat; false precision.

### Q26 ⭐⭐⭐ 🟡 How would you analyse whether late deliveries are hurting repeat purchases?
**Asked at:** commonly asked (no company-specific report found); e-commerce and quick-commerce case rounds use this theme (prep guides, unverified).
**What the interviewer is checking:** Whether you define "late" and "repeat" first and avoid claiming cause from a simple comparison.
**Say this in the interview:** "I would compare repeat rates of customers whose first order was late against on-time customers, matched on city, product and order value, then say how much of the gap is really due to lateness."

**Clarify first:** What counts as late (past the promised date, or past a fixed number of days)? Repeat within how many days (say 90)? The decision: fund faster delivery, or fix a specific courier or warehouse?
**Plan:**
1. Data: order table (order date, promised date, delivered date, customer id, city, category, value), plus courier and warehouse.
2. Clean: one row per first order; drop cancelled or returned orders; check delivered date is never before order date.
3. Flag each first order as late or on time; flag whether the customer ordered again within 90 days (only customers whose first order is at least 90 days old, otherwise the window is incomplete).
4. Compare repeat rate late vs on time, then by lateness band (1 day, 2-3 days, 4+ days) to look for a dose-response pattern.
5. Repeat the comparison within city, category and value bands.
**Method choice and why:** Start with a plain two-group repeat rate and a banded table. Go further (logistic regression, or matching) only if the gap shrinks sharply once you control for city and product.
**Pitfalls:** Late deliveries cluster in remote cities and heavy items, where repeat rates are low anyway (confounding). Also customers who never receive the order vanish from "delivered" data (survivorship). Customers who complained may have got a coupon, which changes behaviour.
**Deliverable:** A one-page view: repeat rate by lateness band, the gap after adjustment, and an estimate of orders lost per 1,000 late deliveries, worded as "associated with", plus one recommended fix.

**Likely follow-ups:** 1) *How would you prove cause?* Look for a natural experiment, such as a courier outage that delayed random orders. 2) *What if late customers repeat as much?* Then lateness is not the retention problem; look at price or product.
**Common mistakes / traps:** Measuring repeat over unequal windows; ignoring city mix; saying "late deliveries cause churn".

### Q27 ⭐⭐⭐ 🟡 You have data from three systems (HRIS, payroll, attendance) to analyse overtime cost. How do you plan the analysis before joining anything?
**Asked at:** commonly asked (no company-specific report found); HR analytics question banks use similar multi-system prompts (unverified).
**What the interviewer is checking:** Planning discipline: definitions, keys and grain before any join.
**Say this in the interview:** "Before joining I agree what overtime cost means, find the common key in each system, and decide the grain (one row per employee per month), because wrong joins quietly duplicate or drop people."

**Clarify first:** Overtime cost for what decision (budget, policy change, one plant)? Which period? Is overtime hours beyond the shift, or hours paid at overtime rate?
**Plan:**
1. Definitions: overtime hours (attendance) x rate (payroll) = cost; confirm with payroll how the rate is built (base pay, multiplier).
2. Profile each source: row count, date range, employee id format, duplicates, blanks.
3. Pick the key (employee id) and check it matches across systems (leading zeros, contractor ids, rehires with new ids).
4. Set the grain: aggregate attendance to employee-month before joining so one row meets one row.
5. Join in steps (HRIS to payroll, then attendance), counting rows and unmatched ids after each join.
6. Reconcile the total to the payroll ledger.
**Method choice and why:** Simple totals and averages by department and month first; no modelling needed.
**Pitfalls:** Many-to-many joins inflating cost; employees who changed department mid-month; different cut-off dates between systems; manual overrides in attendance.
**Deliverable:** A short data-plan note (definitions, keys, grain, checks) shared with the owners of each system, then the cost table with a reconciliation line.

**Likely follow-ups:** 1) *What if ids do not match?* Build a mapping table with HR and report the unmatched share. 2) *What if totals differ from payroll?* List the gap by cause before presenting.
**Common mistakes / traps:** Joining first and discovering duplicates later; not reconciling to a trusted total.

### Q28 ⭐⭐⭐ 🟡 How do you decide which chart or table to use to present an analysis, and what do you put on the first slide?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you choose by the message and audience, not by habit.
**Say this in the interview:** "I ask what comparison the viewer must make. Trend over time gets a line, comparing categories gets bars, exact lookups get a table. The first slide holds the answer, the evidence in one number, and the decision needed."

**Clarify first:** Who is the audience (executive or analyst)? What decision follows? How much time will they give it?
**Plan:**
1. Write the single message in one sentence.
2. Match the chart: change over time, line; compare categories, sorted bars; parts of a whole with few parts, a bar or stacked bar; relationship of two measures, scatter; exact values or many measures, table.
3. Remove clutter: one colour for emphasis, labelled axes starting at zero for bars, direct labels, no 3D.
4. First slide: headline finding, the key number with its comparison, the recommendation, and one caveat.
5. Put detail and method in an appendix.
**Method choice and why:** Simplest form that shows the comparison; a table when people need to look up values.
**Pitfalls:** Pie charts with many slices, dual axes that suggest false links, truncated bars, burying the answer on slide 6.
**Deliverable:** A short deck or one-page summary where each slide title states the takeaway, not the topic.

**Likely follow-ups:** 1) *Table or chart?* Table for lookup, chart for pattern. 2) *How many numbers on the first slide?* One or two that matter.
**Common mistakes / traps:** Starting with methodology; using a chart because it looks impressive.

### Q29 ⭐⭐⭐ 🟡 Leadership wants a single KPI for 'employee engagement'. How would you analyse what to measure and how would you build it?
**Asked at:** commonly asked (no company-specific report found); HR analytics guides cover engagement and survey metrics (unverified).
**What the interviewer is checking:** Whether you can turn a fuzzy idea into defined, defensible components and warn about the limits of one number.
**Say this in the interview:** "I would not invent a number first. I would agree what engagement means, pick a few measurable signals, test which of them relate to outcomes like attrition, and then combine them in a transparent index."

**Clarify first:** What decision will the KPI drive? Which population and how often? Is there a survey already?
**Plan:**
1. Define engagement with HR and leaders (commitment, enthusiasm, intent to stay).
2. Candidate signals: survey items (e.g. "I would recommend this company"), eNPS (the share promoters minus detractors), voluntary attrition, absence, internal mobility, participation in learning.
3. Check data quality and response coverage.
4. Test signals against outcomes (does a low score precede resignation in the next 6 months?).
5. Combine: start with an average of 3 to 5 survey items on a 0 to 100 scale; weights equal unless the test supports otherwise.
6. Validate: pilot on two quarters, check stability and by-team spread.
**Method choice and why:** A simple transparent average beats a black-box score; explain every part so managers trust it.
**Pitfalls:** Low response rates, social desirability in surveys, small teams where anonymity breaks, mixing lagging (attrition) with leading signals.
**Deliverable:** A KPI definition sheet plus a dashboard showing the headline with its components and a confidence note.

**Likely follow-ups:** 1) *Why not one number only?* A single number hides where the problem is; show components. 2) *How do you keep it honest?* Fix the definition and publish changes.
**Common mistakes / traps:** Picking the KPI before defining the concept; using only attrition.

### Q30 ⭐⭐⭐ 🟡 Average order value rose 12 percent after a pricing change. How would you analyse whether the change made money?
**Asked at:** commonly asked (no company-specific report found); metric and pricing cases appear in Flipkart/Meesho-style rounds (guides, unverified).
**What the interviewer is checking:** That you look beyond AOV to orders, margin and a fair comparison.
**Say this in the interview:** "A higher average order value only helps if total profit rose. I would check orders, margin per order and a comparison period, since a 12% AOV rise breaks even on revenue if orders fall about 10.7% (1 divided by 1.12, minus 1)."

**Clarify first:** What changed (list prices, discounts, shipping fee)? When? For all customers or some? What is the goal: revenue or profit?
**Plan:**
1. Define: profit = orders x (AOV x margin %) minus costs; check each term.
2. Compare equal periods before and after, adjusting for seasonality (use last year's same weeks).
3. Check order count and conversion: fewer orders is the usual price of higher prices.
4. Check mix: did AOV rise because prices rose, or because cheap items sold less?
5. Check margin and returns, and repeat customers over the following weeks.
6. If part of the base saw the old price, use them as a control group.
**Method choice and why:** Before-and-after with a control group if available; otherwise before-and-after against last year's pattern. Only then a significance test.
**Pitfalls:** Concurrent promotions, festive season, one-off bulk orders pulling the average up (check the median), losing loyal customers later.
**Deliverable:** A short table: orders, AOV, margin, profit before and after, with a clear "made money / did not" verdict and its confidence.

**Likely follow-ups:** 1) *Revenue flat, profit up?* Possible if margin per order rose; show it. 2) *Is a 12% rise real?* Check outliers and mix first.
**Common mistakes / traps:** Celebrating AOV alone; ignoring order volume.

### Q31 ⭐⭐⭐ 🟡 The analysis you finished contradicts what your manager believes. How do you re-check it and present it?
**Asked at:** commonly asked (no company-specific report found); behavioural and scenario rounds (Deloitte reports mention scenario questions, unverified).
**What the interviewer is checking:** Intellectual honesty plus tact: you verify first, then communicate without ego.
**Say this in the interview:** "I assume I might be wrong and re-check it first. If it holds, I meet my manager privately, show the evidence step by step, and invite them to challenge it."

**Clarify first:** What exactly does my manager believe, and what is it based on (a different data source, past experience, another report)?
**Plan:**
1. Re-check my work: definitions, filters, date ranges, join row counts, duplicates, and reconcile to a trusted total.
2. Have a colleague review the logic, or recompute one figure a second way.
3. Test the manager's view directly: which data would show it true? Look for a reason both could be right (different definitions, time periods).
4. Run a sensitivity check: does the conclusion survive reasonable alternative choices?
5. Prepare a short story: belief, what the data shows, how sure I am.
**Method choice and why:** Show the simplest evidence (one chart or table) rather than the complex method, so the argument is about data, not my technique.
**Pitfalls:** Springing it on them in a meeting, hiding uncertainty, overstating, or quietly changing the result to please.
**Deliverable:** A private walk-through first, then a short written note with the finding, evidence, limits and the decision at stake. If they still disagree, record both views and agree a test.

**Likely follow-ups:** 1) *What if you were wrong?* Say so promptly and fix it. 2) *What if the manager insists?* Escalate neutrally with the evidence, not as a complaint.
**Common mistakes / traps:** Defensiveness; skipping the re-check; presenting before the manager has seen it.

### Q32 ⭐⭐⭐ 🟡 How would you analyse the effect of a salary revision on attrition across bands, given the revision was not applied randomly?
**Asked at:** commonly asked (no company-specific report found); HR program-evaluation questions use this theme (unverified).
**What the interviewer is checking:** Awareness of selection bias and a practical way to compare like with like.
**Say this in the interview:** "Because the revision was not random, a raw comparison is unreliable. I would compare employees with similar band, tenure, performance and pay position, inside each band, and describe the result as an estimate, not proof."

**Clarify first:** Who got the revision and why (performance, market gap, retention risk)? When? What attrition window (6 or 12 months)? Voluntary exits only?
**Plan:**
1. Data: employee snapshot before the revision (band, tenure, rating, pay vs band midpoint, manager, location), revision flag and size, exit date and type.
2. Count exits only after the effective date; exclude involuntary exits.
3. Compare attrition revised vs not, within each band, then across tenure and rating groups.
4. Match each revised employee to a similar non-revised one (same band, tenure, rating, pay position).
5. If revisions were decided by a rule (e.g. pay below a threshold), compare people just above and below the cutoff.
**Method choice and why:** Stratified comparison first; matching or regression if groups are large enough. Keep it explainable.
**Pitfalls:** People targeted because they were flight risks look worse (reverse bias); those who left early never got revised; small cells; other changes at the same time (promotions, a new manager).
**Deliverable:** A band-wise table of attrition rates with sample sizes, a plain-language conclusion with its limits, and a suggestion to randomise or stage the next round.

**Likely follow-ups:** 1) *Could you run an experiment?* Stage the next revision by team and compare. 2) *Why report sample sizes?* Cells with a handful of people are noise.
**Common mistakes / traps:** Comparing revised vs all others; saying the revision "reduced attrition".

### Q33 ⭐⭐⭐ 🟡 Sales by quarter are given below. How would you analyse them, and what is the year-on-year growth for Q4?
Inline data: Q4 last year 80 lakh; Q1 90; Q2 100; Q3 105; Q4 this year 96 (lakh, exercise data).
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Correct growth formula, and noticing that the headline hides a recent slowdown.
**Say this in the interview:** "Year-on-year Q4 growth is (96 minus 80) divided by 80, which is 20%. But sales fell 8.6% from Q3 to Q4, so I would not call the trend healthy without looking closer."

**Clarify first:** Is this one product line or all? Is Q4 seasonal? Were there price changes or one-off deals? Do I have earlier years to see the normal Q3-to-Q4 pattern?
**Plan:**
1. Year-on-year (same quarter, a year apart): Q4 = 96 / 80 minus 1 = 20.0%. This is the only true year-on-year figure possible, since only last year's Q4 is given.
2. Quarter-on-quarter: Q3 to Q4 = 96 / 105 minus 1 = minus 8.6% (rounded). Earlier quarters this year grew: Q1 to Q2 +11.1%, Q2 to Q3 +5.0%.
3. For context only (not year-on-year): measured against the fixed Q4 base of 80, Q1 is +12.5%, Q2 +25.0%, Q3 +31.3% and Q4 +20.0%.
4. This year's total across Q1-Q4 is 391 lakh.
5. Split by product, region and customer to find where Q4 dropped.
**Method choice and why:** Simple percentage changes, a line chart; seasonal comparison needs at least two prior years.
**Pitfalls:** Mixing year-on-year with quarter-on-quarter; calling 20% growth strong while the latest quarter fell; ignoring seasonality in Q4.
**Deliverable:** A line chart of the five quarters with the two growth figures and one sentence: strong against last year, softening against the previous quarter, cause to be checked.

**Likely follow-ups:** 1) *Is Q4 decline seasonal?* Compare Q3-to-Q4 in earlier years. 2) *Percentage or percentage-point?* Sales change is a percentage; a change in a rate is points.
**Common mistakes / traps:** Dividing by the wrong base (96 instead of 80); using Q3 as the YoY base.

### Q34 ⭐⭐⭐ 🟡 A cohort table for a monthly subscription is below. Which cohort retains worst by month 3, and what do you analyse next?
Inline data: Cohort Jan: 1,000 users, month-3 active 520. Cohort Feb: 800 users, month-3 active 360. Cohort Mar: 1,200 users, month-3 active 500 (exercise data).
**Asked at:** commonly asked (no company-specific report found); cohort and retention prompts are common in case guides (unverified).
**What the interviewer is checking:** Using rates, not counts, and a sensible next step.
**Say this in the interview:** "Month-3 retention is active users divided by starting users: Jan 52.0%, Feb 45.0%, Mar 41.7%. March retains worst, even though it is the biggest cohort."

**Clarify first:** What does "active" mean? Is month 3 measured the same way for each cohort (same days since signup)? Was March's month-3 data complete?
**Plan:**
1. Working: Jan 520/1,000 = 52.0%; Feb 360/800 = 45.0%; Mar 500/1,200 = 41.7% (rounded). Pooled retention is 1,380/3,000 = 46.0%.
2. Gaps: Mar is 10.3 points below Jan (rounded). Note Feb had the fewest users, so its figure is the least precise.
3. Next, view the full curve (months 1, 2, 3, 4...) to see where March drops.
4. Slice March by acquisition channel, plan type, discount, country and device.
5. Check what changed in March: price, onboarding, a promotion, product bug.
**Method choice and why:** A cohort retention table and curve; no model needed. Test the difference only if the decision is costly.
**Pitfalls:** Comparing counts; different cohort mix (more discount-led signups in March); a cohort not yet fully observed.
**Deliverable:** A cohort heatmap, a note on March, and a hypothesis list ranked by effort to check.

**Likely follow-ups:** 1) *Is 41.7 vs 45.0 a real gap?* With these sizes it could be noise for small cohorts; test it. 2) *What would you do?* Compare March channels first.
**Common mistakes / traps:** Saying Jan retained "most users" because 520 is large; ignoring cohort size.

### Q35 ⭐⭐⭐ 🟡 A training programme is evaluated with the figures below. How would you analyse whether it worked, and what is the difference in attrition rate?
Inline data: Trained: 200 employees, 18 left in 12 months. Not trained: 800 employees, 100 left (exercise data). Trained group was volunteered by managers.
**Asked at:** commonly asked (no company-specific report found); HR program evaluation with a control group appears in HR analytics question banks (unverified).
**What the interviewer is checking:** The correct difference, plus recognition that volunteered participants are not comparable.
**Say this in the interview:** "Attrition was 9.0% for trained and 12.5% for untrained, a 3.5 percentage-point gap, but managers chose who went, so I cannot say the training caused it."

**Clarify first:** How did managers pick people (best performers? flight-risk ones)? Was the attrition window the same? Voluntary exits only?
**Plan:**
1. Working: trained 18/200 = 9.0%; not trained 100/800 = 12.5%.
2. Difference: 3.5 percentage points (relative drop of 28%). Use "points" because both figures are percentages.
3. Chance check: a chi-square test gives p of about 0.17, so with these numbers the gap is not statistically convincing (illustrative check only).
4. Compare like with like: break by band, tenure, rating and manager, since volunteered staff are usually engaged high performers who leave less anyway.
5. Look at pre-training attrition risk or engagement scores; if the groups differed before, the result is biased.
**Method choice and why:** Stratified comparison, then matching; a staggered rollout would be the proper test next time.
**Pitfalls:** Selection bias, survivorship (people who left during training excluded), counting exits before the training date.
**Deliverable:** A table with rates, the point difference and caution: "associated with lower attrition; not proven".

**Likely follow-ups:** 1) *Why not conclude it worked?* Volunteers were probably less likely to leave regardless. 2) *How would you test properly?* Randomly choose who goes first among interested staff.
**Common mistakes / traps:** Saying 3.5% instead of 3.5 points; ignoring selection.

### Q36 ⭐⭐⭐ 🔴 Revenue is growing but profit is falling. How would you analyse where the problem sits across products, customers and costs?
**Asked at:** commonly asked (no company-specific report found); a classic business case prompt.
**What the interviewer is checking:** A structured breakdown of profit rather than guessing.
**Say this in the interview:** "I would split profit into revenue, cost of goods and operating costs, then find which product, customer group or cost line moved against revenue, comparing the same periods."

**Clarify first:** Gross profit or net? Over what period? Did anything change (pricing, mix, discounts, new channel, hiring)?
**Plan:**
1. Define: profit = revenue minus cost of goods minus operating costs; get margin % at each level over time.
2. Gross margin trend: if it falls, the problem is price, discounts, product mix or input cost.
3. Product view: revenue and margin by product; find fast-growing low-margin items.
4. Customer view: revenue and margin by segment and channel; look for heavy discounting, high return or high service cost accounts.
5. Cost lines: compare operating costs (marketing, logistics, staff, returns) to revenue growth.
6. Bridge: a waterfall from last period profit to this period, showing each driver.
**Method choice and why:** Margin decomposition and a profit bridge; no model needed.
**Pitfalls:** Looking at revenue only; allocating shared costs arbitrarily; one-off items; timing mismatches between revenue and cost.
**Deliverable:** A waterfall chart plus a table of the top three contributors and a recommended action for each.

**Likely follow-ups:** 1) *Mix vs rate?* Separate the effect of selling more low-margin items from falling margins on each item. 2) *What first?* Gross margin, because it is the quickest split.
**Common mistakes / traps:** Blaming one cost without evidence; ignoring product mix.

### Q37 ⭐⭐⭐ 🔴 A new product launched and the early numbers look great. How would you analyse whether the launch is truly successful rather than just novel?
**Asked at:** commonly asked (no company-specific report found); product metrics cases (unverified).
**What the interviewer is checking:** Awareness of novelty effect, cannibalisation and sustained value.
**Say this in the interview:** "Early spikes often come from curiosity and launch promotions. I would look at repeat use, cohorts over weeks, whether it cannibalises existing products, and profit after launch costs."

**Clarify first:** What was the goal (revenue, new users, retention)? What is "great" compared with (target, a past launch)? How long since launch?
**Plan:**
1. Define success metrics beforehand: repeat rate, retention, revenue per user, margin, incremental revenue.
2. Plot daily or weekly new vs repeat users; novelty shows a spike then decay.
3. Cohort retention by launch week; does week-4 use stabilise?
4. Cannibalisation: did sales of related products drop by about as much as the new one gained?
5. Check promotion effect: compare full-price buyers vs discounted buyers.
6. Quality signals: returns, ratings, complaints, support tickets.
7. Include launch costs for net contribution.
**Method choice and why:** Cohorts and incremental comparison (against a similar region without launch); keep it simple.
**Pitfalls:** Total sales that include substitution; early adopters are not typical; short window.
**Deliverable:** A launch scorecard with early and 4-to-8-week metrics and a verdict "scale / watch / stop" with trigger values.

**Likely follow-ups:** 1) *How long to wait?* One or more full repeat cycles. 2) *What proves incrementality?* A holdout area or matched comparison.
**Common mistakes / traps:** Reporting total launch revenue without cannibalisation.

### Q38 ⭐⭐⭐ 🔴 How do you design an analysis to answer 'which customers should we spend retention budget on' rather than simply 'which customers are likely to leave'?
**Asked at:** commonly asked (no company-specific report found); a differentiating question (unverified).
**What the interviewer is checking:** That you target customers whose behaviour the spend can change and who are worth keeping.
**Say this in the interview:** "A churn score only says who may leave. I would also estimate their value and how much an offer would change their decision, and spend where value times persuadability beats the cost."

**Clarify first:** Budget size, offer type, and time window? Does a past campaign exist to learn from?
**Plan:**
1. Define churn and value (expected future margin over say 12 months, not just revenue).
2. Estimate churn risk (simple rules or a model).
3. Estimate uplift: who responds to offers? Past campaigns with a control group show the gain in retention caused by the offer.
4. Expected benefit per customer = value x extra retention probability minus offer cost.
5. Rank by benefit; spend down the list until benefit falls below cost or the budget ends.
6. Group: high value and persuadable (spend), high value and sure to stay (do not waste), sure to leave regardless (skip), low value (automate cheaply).
**Method choice and why:** Value-times-risk tiers first; uplift modelling later if control-group data exists.
**Pitfalls:** Discounting customers who would have stayed; no control group, so response is confused with effect; ignoring offer cost.
**Deliverable:** Segment table with size, value, expected return and recommended action, plus a plan to test with a held-out group.

**Likely follow-ups:** 1) *No past campaign?* Run a small randomised pilot. 2) *Why exclude sure-stayers?* The money buys nothing extra.
**Common mistakes / traps:** Targeting the highest churn scores only.

### Q39 ⭐⭐⭐ 🔴 You have only 24 hours and messy data to give an analysis for a Monday leadership meeting. How do you decide scope, what to trust and what to say with caveats?
**Asked at:** commonly asked (no company-specific report found); time-pressure prompts appear in case guides (unverified).
**What the interviewer is checking:** Prioritisation, honest caveats and not overpromising.
**Say this in the interview:** "I would agree the one decision the meeting needs, answer only that, check the few numbers that matter against a trusted total, and present the finding with a clear confidence level and what I did not verify."

**Clarify first:** What decision is Monday's meeting making? What is the single question? Who owns the data, and which figure do they already trust?
**Plan:**
1. First hour: write the question and a one-line hypothesis; list the 3 to 5 numbers needed.
2. Next 3 hours: profile data (row counts, missing, duplicates, date ranges) and fix only what affects those numbers.
3. Reconcile one total to a trusted source (finance report) to decide how far to trust the data.
4. Next 10 hours: do the simple analysis; cut everything else; keep a log of assumptions.
5. Sleep, then re-check the headline number a second way.
6. Final hours: one-page summary and backup slide.
**Method choice and why:** Simple totals, rates and one chart; nothing needing a model I cannot validate.
**Pitfalls:** Scope creep, silent assumptions, polishing charts before the numbers are right.
**Deliverable:** One page: the answer, confidence level (high/medium/low), three caveats, what I would do with another week.

**Likely follow-ups:** 1) *What if data is too bad?* Say which part is unusable and give a direction, not a number. 2) *What do you drop?* Nice-to-have breakdowns.
**Common mistakes / traps:** Trying to clean everything; hiding limits.

### Q40 ⭐⭐ 🟢 How would you analyse customer feedback comments (free text) to give leadership a view of the main complaints?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** A pragmatic way to turn text into counts, with caution about representativeness.
**Say this in the interview:** "I would read a sample, build a short list of complaint themes, tag all comments to those themes, count them, and show the top themes with real quotes and their share of all comments."

**Clarify first:** What decision follows (product fix, service training)? How many comments, which channels, which period? Are there ratings alongside?
**Plan:**
1. Clean: remove duplicates, blanks, spam; keep the date, rating, product, channel.
2. Read 100 to 200 comments and draft 8 to 12 themes (delivery delay, price, quality, staff behaviour).
3. Tag every comment: keyword rules in Excel or Python first; check a sample of 50 by hand for accuracy.
4. Count themes, share of comments, and average rating per theme; trend by month.
5. Pick top themes by volume and by severity (low ratings).
**Method choice and why:** Manual themes plus keyword tagging is explainable. Automated topic or sentiment tools can help at large volume but need a hand check.
**Pitfalls:** Vocal customers are not all customers; one comment can hold several themes; translation or mixed-language text; sarcasm misread by tools.
**Deliverable:** A one-page chart of top themes with quotes, the trend, and recommended owner for each.

**Likely follow-ups:** 1) *Sentiment scores?* Useful as a rough guide, check against a sample. 2) *Thousands of comments?* Tag a sample by hand and train a simple classifier.
**Common mistakes / traps:** Showing a word cloud with no counts.

### Q41 ⭐⭐ 🟢 How would you analyse whether a promotion email campaign worked, given the people who got the email were chosen by the marketing team?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Recognising that a hand-picked group is not comparable to the rest.
**Say this in the interview:** "Marketing probably picked likely buyers, so comparing them with others overstates the effect. I would compare similar customers who did and did not get the email, and say what remains uncertain."

**Clarify first:** How were recipients chosen? What was the goal (open, click, purchase)? Over what window? Any other promotions at the same time?
**Plan:**
1. Define the outcome: purchase within 7 days.
2. Compare recipients with non-recipients overall (baseline only).
3. Match on past purchases, recency, spend and region, then compare conversion in matched groups.
4. Compare recipients' behaviour before and after the email against non-recipients' change over the same dates.
5. Compute incremental revenue minus campaign cost.
**Method choice and why:** Matched comparison first; for the next campaign, keep a random hold-out group.
**Pitfalls:** Selection bias; people who would have bought anyway; unsubscribed customers; other channels running at the same time.
**Deliverable:** A table with conversion, estimated extra orders, cost and return, flagged as an estimate, with the hold-out recommendation.

**Likely follow-ups:** 1) *No comparable group?* Report only the lower and upper bounds. 2) *Open rate?* A weak outcome; purchases matter.
**Common mistakes / traps:** Crediting all sales from recipients to the email.

### Q42 ⭐⭐ 🟢 What is the difference between correlation and causation, and how does it change the way you word findings in an analysis?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Conceptual clarity and careful wording.
**Say this in the interview:** "Correlation means two things move together; causation means one changes the other. In reports I write 'is associated with' unless I have an experiment or strong controls."

**Explain simply:**
- Correlation: when A is high, B tends to be high. It says nothing about why.
- Causation: changing A would change B.
- Three common reasons for a link without cause: a hidden third factor (confounder), reverse direction, or chance.
- Example: employees who attend training get promoted more. Motivated employees may both sign up and perform; so motivation could drive both.
- Wording: "associated with", "tends to" for observed links; "caused", "led to" only after a randomised test or a well-controlled comparison.
**Practice step:** Take any link you see in an HR export (overtime and attrition) and list two other explanations, then write the sentence two ways.

**Likely follow-ups:** 1) *How do you get closer to cause?* Randomise, or compare like with like on a control group. 2) *Is correlation useless?* No, it is good for prediction and for deciding what to test.
**Common mistakes / traps:** Writing "drives" or "impacts" for observed links.

### Q43 ⭐⭐ 🟢 How would you analyse the cost per hire of a recruitment team and compare channels?
**Asked at:** commonly asked (no company-specific report found); HR analytics banks cover cost per hire and funnel analysis (unverified).
**What the interviewer is checking:** A clear cost definition and fair channel comparison beyond cost.
**Say this in the interview:** "Cost per hire is total recruiting cost divided by hires. For channels I allocate each cost to its channel and also compare quality and speed, since the cheapest hire is not always the best."

**Clarify first:** Which costs count (agency fees, job boards, referral bonuses, recruiter salaries, interview time)? Which period and roles?
**Plan:**
1. Define: cost per hire = (internal plus external recruiting cost) / number of hires. Agree the cost list with finance.
2. Data: ATS for hires by source, finance for costs.
3. Direct costs go to channels; shared costs (recruiter pay) are split by effort or hires, stated clearly.
4. Per channel: hires, cost per hire, time to hire, offer acceptance, 6 or 12-month retention, and early performance.
5. Compare within role type and level, since senior roles cost more.
**Method choice and why:** Simple table by channel and role family.
**Pitfalls:** Mixing role levels; ignoring quality (a cheap channel with high early exits); small hire counts; unclear source tagging in the ATS.
**Deliverable:** A channel comparison table with a recommendation on where to spend more or less, with caveats.

**Likely follow-ups:** 1) *Cost per hire vs quality of hire?* Add retention and performance. 2) *Shared costs?* State the allocation rule.
**Common mistakes / traps:** Comparing channels without controlling for role mix.

### Q44 ⭐⭐ 🟢 How would you analyse the productivity of a customer support team?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Balanced measures, not speed alone.
**Say this in the interview:** "I would pair output (tickets resolved per agent hour) with quality (customer satisfaction, reopen rate) and speed (resolution time), then compare agents within the same ticket type."

**Clarify first:** What is the goal (cost, speed, satisfaction)? Which channels (chat, email, phone)? Are tickets of equal difficulty?
**Plan:**
1. Data: ticket log (created, resolved, agent, type, channel, reopen, satisfaction score) and agent hours.
2. Metrics: tickets resolved per productive hour, first response time, median resolution time, first-contact resolution, reopen rate, satisfaction.
3. Group by ticket type and channel to compare fairly.
4. Look for patterns by shift, week and team.
5. Check the workload: queue size and arrival peaks.
**Method choice and why:** Medians and percentiles for time (skewed), rates for quality.
**Pitfalls:** Rewarding speed that drives reopens; mixed ticket difficulty; averages hiding a few long cases; paying attention only to top performers.
**Deliverable:** A dashboard with a few paired metrics and a table of drivers, avoiding ranking individuals on one number.

**Likely follow-ups:** 1) *Why median?* A few very long tickets inflate the mean. 2) *Compare agents?* Only on similar ticket mix.
**Common mistakes / traps:** One metric only; ranking agents without adjusting for ticket type.

### Q45 ⭐⭐ 🟢 Explain the difference between an ad hoc analysis and a recurring report, and how your approach differs for each.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Understanding of one-off answers versus maintained, automated outputs.
**Say this in the interview:** "Ad hoc answers one question once, so speed and clarity matter. A recurring report is a product: fixed definitions, automated refresh, checks and an owner."

**Explain simply:**
- Ad hoc: a single question (why did attrition rise in March?). Clarify the question, use whatever data is quickest, document assumptions, deliver a short answer.
- Recurring: weekly attendance report. Fix definitions, build once with a repeatable query, automate refresh, add data checks and a stable layout.
- Differences: lifespan, audience, validation, documentation, ownership, handling of changes.
- Example: the first time you analyse overtime, it is ad hoc; if leaders want it every month, turn it into a report.
**Practice step:** Take an Excel analysis you did once and list what you would need so someone else could refresh it monthly.

**Likely follow-ups:** 1) *When convert ad hoc to recurring?* When the same question returns. 2) *Biggest risk of recurring?* Silent breakage when source data changes.
**Common mistakes / traps:** Building a one-off in a way no one can repeat; over-engineering something needed once.

### Q46 ⭐⭐ 🟢 How do you document an analysis so another analyst can reproduce it later?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Habits of clean, auditable work.
**Say this in the interview:** "I record the question, the data source and extract date, every cleaning step, definitions and the code or formulas, so a colleague can rerun it and get the same numbers."

**Explain simply:**
- Purpose: the question, the decision and the requester.
- Data: source, extract date, filters, and row counts at each stage.
- Definitions: for example, "active employee" or "late delivery".
- Steps: cleaning choices with reasons (removed 12 duplicate rows, treated blanks as zero).
- Code: saved SQL or script or well-labelled Excel with inputs separated from formulas; use version names.
- Results: final numbers, checks done and known limits.
- Keep a short README or a "Method" sheet and store the file in a shared place.
**Practice step:** Ask a colleague to rerun your last analysis from the notes alone and fix whatever they cannot follow.

**Likely follow-ups:** 1) *Where would you store it?* A shared drive or a repository with version history, per the team's practice. 2) *What if the source data changes?* The extract date and a saved copy of the input show the difference.
**Common mistakes / traps:** Hard-coded numbers without notes; overwriting the raw data.

### Q47 ⭐⭐ 🟢 Average order value for two customer groups is given below. Which has the higher revenue per visitor, and why might the averages alone mislead you?
Inline data: Group A: 2,000 visitors, 100 orders, AOV 1,500. Group B: 3,000 visitors, 90 orders, AOV 2,200 (exercise data).
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Chaining conversion x AOV rather than looking at one metric.
**Say this in the interview:** "Revenue per visitor is conversion times average order value. Group A earns 75 per visitor and Group B 66, so A is higher even though B has the bigger AOV."

**Clarify first:** Are the groups comparable (same time, traffic source)? Does AOV include returns? Is the currency rupees?
**Plan:**
1. Conversion: A = 100/2,000 = 5.0%; B = 90/3,000 = 3.0%.
2. Revenue: A = 100 x 1,500 = 150,000; B = 90 x 2,200 = 198,000.
3. Revenue per visitor: A = 150,000/2,000 = 75; B = 198,000/3,000 = 66.
4. Check: 5.0% x 1,500 = 75; 3.0% x 2,200 = 66.
5. B has higher total revenue and AOV but weaker conversion across more visitors; A is the more efficient group per visitor.
**Method choice and why:** Simple decomposition; a significance test on conversion if the decision is costly.
**Pitfalls:** Looking at AOV alone; ignoring that groups differ in traffic source or product mix; small order counts (90 and 100 orders mean noisy averages); outliers inflating B's AOV (check the median).
**Deliverable:** A small table with visitors, orders, conversion, AOV and revenue per visitor, plus one line on which group to invest in and what to test.

**Likely follow-ups:** 1) *Which is better for the business?* Depends on margin and cost of acquiring visitors. 2) *Can B fix it?* Raising its conversion from 3.0% to 3.4% would match A (66 x 75/66 needs 3.41%).
**Common mistakes / traps:** Picking B because of AOV; mixing total revenue with per-visitor revenue.

### Q48 ⭐⭐ 🟡 How would you analyse seasonality in sales data, and how would you use it for next quarter's plan?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Simple seasonal indices and sensible planning use.
**Say this in the interview:** "I would compare each month with its yearly average over several years to get a seasonal index, remove it to see the real trend, then apply it to next quarter's baseline."

**Clarify first:** How many years of data? Weekly or monthly? Any promotions, price changes or one-offs (festivals, shifting dates)?
**Plan:**
1. Get at least two to three years of monthly sales; mark special events.
2. Plot sales by month on one line per year; repeated peaks suggest seasonality.
3. Seasonal index = average of a month's sales / average of all months (100 = typical).
4. Deseasonalise: sales divided by the index, to see the underlying trend.
5. Forecast: take the trend baseline, grow it sensibly, then multiply by next quarter's indices.
6. Check against last year's actual, and give a range.
**Method choice and why:** Seasonal indices or a year-on-year comparison first; use a forecasting method only if needed and explain it.
**Pitfalls:** Moving festival dates (the same festival lands in different months); too little history; a pandemic or one-off year distorting indices.
**Deliverable:** A chart of seasonal indices, a baseline-and-seasonal forecast with a range, and stock or staffing implications.

**Likely follow-ups:** 1) *Weekly seasonality?* Add a day-of-week index for operational planning. 2) *Only one year of data?* Say seasonality cannot be separated from trend.
**Common mistakes / traps:** Reading a one-off spike as seasonal.

### Q49 ⭐⭐ 🟡 How would you analyse employee performance ratings to check whether managers rate consistently?
**Asked at:** commonly asked (no company-specific report found); HR analytics banks cover rating calibration (unverified).
**What the interviewer is checking:** Fair comparison of manager distributions without assuming teams are equal, and careful handling of sensitive data.
**Say this in the interview:** "I would compare each manager's rating distribution and average with the company's, adjusting for team size and role, to flag unusually lenient or harsh patterns for a calibration discussion, not to accuse anyone."

**Clarify first:** What rating scale and forced distribution (if any)? Are teams comparable? What will the result be used for (calibration, or pay)?
**Plan:**
1. Data: ratings, manager, role, grade, tenure, team size, cycle.
2. Check each manager's average, share of top and bottom ratings, and spread; mark managers with fewer than about 8 reports as too small to judge.
3. Compare to the company and department norms for the same role and grade.
4. Look for patterns: everyone rated the same, or the same rating each cycle.
5. Check performance evidence (targets met) alongside ratings where available.
6. Restrict access, anonymise where possible, and share results with HR leadership only.
**Method choice and why:** Simple comparison and a chart; a statistical test or a mixed model only if volume allows.
**Pitfalls:** A strong team may rightly have high ratings; small teams; bias by gender or location needs careful, confidential handling.
**Deliverable:** A confidential manager-level summary with flags and a suggestion to calibrate, with a caution on team size.

**Likely follow-ups:** 1) *Is a high-rating manager lenient?* Not necessarily; check outcomes. 2) *Privacy?* Restrict access and follow company policy.
**Common mistakes / traps:** Ranking managers by average alone.

### Q50 ⭐⭐ 🟡 How would you analyse a sudden spike in refund requests without being given a reason?
**Asked at:** commonly asked (no company-specific report found); metric-change investigation is a standard case type (unverified).
**What the interviewer is checking:** A structured, data-first search for the cause.
**Say this in the interview:** "First I confirm the spike is real and measure it against a normal baseline, then I slice by product, date, channel, region and reason code to find where it concentrates."

**Clarify first:** What is the spike (count or rate), since when, and by how much? Has the definition or data feed changed? Any releases, offers or supplier changes?
**Plan:**
1. Check the data: duplicates, a backlog loaded at once, a changed refund-status definition.
2. Use refund rate (refunds / orders), not just count, since sales volume may have risen.
3. Compare with the same weeks last year and normal weeks.
4. Slice by product, category, supplier, courier, city, payment method, channel and customer type; see which slice holds most of the excess.
5. Read reason codes and a sample of tickets and notes.
6. Line up the start date with events: price change, new batch, site release, courier change, a fraud pattern.
**If I find...:** One product or batch: quality issue, tell operations. One payment type or customer set: possible fraud or a bug. Everything equally: a policy or system change.
**Method choice and why:** Slicing and time alignment; no model needed.
**Pitfalls:** Reading volume as rate; acting on the first guess; ignoring a lag between order and refund.
**Deliverable:** A short note with the size, where it concentrates, the likely cause and confidence, and an owner for action.

**Likely follow-ups:** 1) *Who do you tell first?* Operations or finance owner, early, with the caveat. 2) *Cannot find a cause?* Report what is ruled out.
**Common mistakes / traps:** Waiting for the reason to be provided.

### Q51 ⭐⭐ 🟡 How would you analyse the effect of a price increase on demand using only historical sales data?
**Asked at:** commonly asked (no company-specific report found); price and demand cases are a standard prep-guide theme (unverified).
**What the interviewer is checking:** Whether you know that history is observational, so price and demand move together with other things (season, promos, competitors).
**Say this in the interview:** "I would compare units before and after the price change, then strip out season, promotions and stock-outs before I call the leftover drop the effect of price. I would report it as a range, not a single number."

**Clarify first:** What decision is this for (raise again, roll back, price a new item)? Which products, and was the increase the same everywhere? Was anything else changed at the same time (promo, packaging, competitor move)?
**Plan:**
1. Pull weekly units, price, promo flag, stock availability and channel for 6-12 months before and after the change.
2. Clean: remove weeks with stock-outs (demand was not allowed to show), mark festival weeks.
3. Compare the same weeks last year to remove season.
4. Compute price elasticity (percentage change in units divided by percentage change in price). Illustration: price 100 to 110 (+10%), units 1000 to 920 (-8%), elasticity about -0.8, meaning demand is fairly insensitive. Revenue goes from 100,000 to 101,200 (+1.2%).
5. If the price rose in some stores or cities and not others, use those as a comparison group (difference-in-differences: the change in the raised group minus the change in the unchanged group).
**Method choice and why:** Start with before/after against a comparison group; it is easy to explain. Only move to a regression with price, season and promo as inputs if there are many products and enough variation.
**Pitfalls:** Price is rarely changed at random; it often rises when demand is already strong or falling. Short-run reaction differs from long-run. Cheaper substitutes and customers switching channels hide in totals.
**Deliverable:** A one-page note: elasticity range, revenue and margin impact (not just units), and the assumptions I could not test.

**Likely follow-ups:** 1) *Can history prove causation?* Not fully; a controlled price test would. 2) *Why look at margin?* Fewer units at a higher price can still raise profit.
**Common mistakes / traps:** Comparing before and after without adjusting for season; ignoring stock-outs; reporting revenue only.

### Q52 ⭐⭐ 🟡 An A/B test shows 3 percent lift but the result is not statistically significant. How do you analyse and present this to the product team?
**Asked at:** commonly asked (no company-specific report found); experiment plan checks such as power and go/no-go appear in 2026 case guides (unverified).
**What the interviewer is checking:** Whether you avoid both "it won" and "it did nothing", and speak in ranges.
**Say this in the interview:** "Not significant means the test cannot tell 3 percent from zero. I would show the confidence range, check whether the test had enough users, and recommend a decision, not just a verdict."

**Clarify first:** Is 3 percent relative or percentage points? What was the planned sample size and the main metric? Was the test stopped early? What does a wrong call cost?
**Plan:**
1. Check the setup: equal split of users (sample ratio check), no tracking gaps, test ran full weeks.
2. Compute the lift with its confidence interval. Illustration: 10,000 users per arm, 5.00% vs 5.15% conversion (3% relative lift). Difference 0.15 percentage points, p-value about 0.63, 95% interval about -0.46 to +0.76 points (roughly -9% to +15% relative).
3. Do the power check: to detect a 3% relative lift at this baseline with 80% power you would need about 336,000 users per arm, far more than 10,000.
4. Look at secondary metrics and segments only as hints, never as the verdict.
**Method choice and why:** A confidence interval is easier to explain than a p-value alone. Go further (more traffic, longer run, or a bigger change) only if the decision is worth it.
**Pitfalls:** Declaring victory on 3 percent; slicing segments until one looks significant; stopping early when the number looks good.
**Deliverable:** A short readout: "Result inconclusive. Plausible effect between a small loss and a moderate gain. Options: ship if cheap and safe, or extend the test to N users (about X weeks)." Ask the team what size of lift would justify the change.

**Likely follow-ups:** 1) *Would you ship?* If the change is free and reversible, possibly; otherwise extend. 2) *Does non-significant mean no effect?* No, it means unproven.
**Common mistakes / traps:** Saying "it failed"; reading 3 percent as certain; confusing percent and percentage points. (Figures above are computed exercise numbers, rounded.)

### Q53 ⭐⭐ 🟡 How would you analyse inventory data to find slow-moving and fast-moving items and decide what to do with each?
**Asked at:** commonly asked (no company-specific report found); operations cases are common in e-commerce rounds (unverified).
**What the interviewer is checking:** Whether you use cover and turnover, not just sales, and tie each group to an action.
**Say this in the interview:** "I would rank items by how many days of stock we hold at the current sales rate, split them into fast, medium and slow, and give each group a different action."

**Clarify first:** What is the goal (free up cash, avoid stock-outs, cut storage)? Do items expire or go out of fashion? What is the supplier lead time?
**Plan:**
1. Data: item, stock on hand, daily or weekly sales for 3-6 months, cost, shelf life, lead time, stock-out days.
2. Clean: adjust sales for stock-out days (zero sales may mean no stock, not no demand); remove one-off bulk orders.
3. Compute turnover (units sold divided by average stock) and days of cover (stock divided by daily sales).
4. Group by value too: rank by revenue share (ABC) and by sales speed, so you see a 3x3 view.
5. Actions: fast movers, keep safety stock and reorder early; slow movers, run discounts, bundle, return to supplier or stop reordering; dead stock, write-off or liquidate; fast and high-value, protect first.
**Method choice and why:** A simple cover table in Excel or SQL first. Forecast models only for the top items.
**Pitfalls:** New products look slow; seasonal items look dead out of season; stock-outs make fast items look slow.
**Deliverable:** A sheet with item, group, cover days, cash tied up, recommended action and owner, plus a one-line summary ("20 percent of items hold half the stock and sell little").

**Likely follow-ups:** 1) *Threshold for slow?* Set it with the business, for example cover above 90 days. 2) *What about new items?* Judge after a launch window.
**Common mistakes / traps:** Using sales alone; ignoring stock-out days; treating all slow items the same.

### Q54 ⭐⭐ 🟡 How would you analyse the lifetime value of customers acquired through different channels, and what could mislead you?
**Asked at:** commonly asked (no company-specific report found); cohort and retention themes appear in case guides (unverified).
**What the interviewer is checking:** Whether you handle young cohorts, cost and selection effects.
**Say this in the interview:** "I would group customers by the channel and month they joined, track their gross profit over time, and compare equal ages, because newer customers have not had time to spend."

**Clarify first:** Revenue or profit? Time horizon (12 months)? How is channel assigned (first touch or last touch)? What is the acquisition cost per channel?
**Plan:**
1. Data: customer id, acquisition date and channel, orders, returns, margin, cost to acquire.
2. Build cohorts (channel by join month) and compute cumulative gross profit per customer at month 1, 3, 6, 12.
3. Compare at the same age only, not total to date.
4. Subtract acquisition cost to get payback time and a LTV-to-cost ratio.
5. For young cohorts, extend the curve with a simple retention pattern from older cohorts and label it as an estimate.
**Method choice and why:** Cohort tables, which a pivot table can do. Predictive LTV models only when volume and history are large.
**Pitfalls:** Comparing old and new cohorts; using revenue not margin; the channel may attract different people to begin with (a discount channel brings bargain hunters), so the channel is not necessarily the cause; attribution rules shift customers between channels; a few big spenders can distort averages (check median too).
**Deliverable:** A chart of cumulative profit per customer by channel with payback month, plus a table of cost, 12-month value and confidence.

**Likely follow-ups:** 1) *How long to wait?* Use early signals (month 3) with the older curve as a guide. 2) *Average or median?* Show both when spend is skewed.
**Common mistakes / traps:** Quoting one LTV number; ignoring cost; comparing unequal ages.

### Q55 ⭐⭐ 🟡 How would you analyse whether remote work affects performance, given employees chose whether to work remotely?
**Asked at:** commonly asked (no company-specific report found); HR program-evaluation with a comparison group is a listed people-analytics theme (unverified).
**What the interviewer is checking:** Whether you spot selection bias: people who choose remote may differ already.
**Say this in the interview:** "Because people chose, a simple comparison would be unfair. I would compare each person with themselves before and after, and compare similar employees, then say how sure I am."

**Clarify first:** What does performance mean (rating, output, targets met)? Are ratings given by the same managers? Which roles can work remotely? Was the choice free or approved?
**Plan:**
1. Data: work mode by month, role, grade, tenure, team, manager, performance measures, prior-year ratings.
2. Compare only like with like: same role and grade, similar tenure and prior performance.
3. Use a before/after view for those who switched, with those who never switched as the comparison (difference-in-differences).
4. Check outcome by role and by manager, since manager bias in ratings can differ for people they rarely see.
5. If possible, use an objective measure (tickets closed, sales) alongside ratings.
**Method choice and why:** Matched comparison and before/after first; plain language. Regression with controls if the sample is large. Be clear that this reduces but does not remove bias.
**Pitfalls:** Self-selection (high performers may seek flexibility, or the reverse); manager rating bias; survivors only (those who left are missing); small groups.
**Deliverable:** A short note: "After adjusting for role and past performance, the difference is about X, with a range of Y to Z; here is what we cannot rule out." Treat the data as sensitive and report group results only.

**Likely follow-ups:** 1) *Can you prove causation?* Only a trial or a policy that assigns people randomly or by rule would. 2) *Fairness?* Check rating differences by work mode.
**Common mistakes / traps:** Comparing averages and concluding; ignoring selection; reporting individuals.

### Q56 ⭐⭐ 🟡 A report shows total sales up but the customer count down. How would you analyse what is happening?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you split sales into customers times spend per customer and look for mix and definition effects.
**Say this in the interview:** "Sales equals customers times average spend per customer, so higher sales with fewer customers means spend per customer rose. I would find who is spending more and whether the customer count is defined the same way."

**Clarify first:** How is customer counted (unique buyers, active accounts, registered)? Same period and filters for both? Which direction is the change and by how much?
**Plan:**
1. Decompose: Illustration: 1,000 customers at 500 each is 500,000; 900 customers at 600 each is 540,000. Sales +8%, customers -10%, spend per customer +20%.
2. Split spend per customer into orders per customer and value per order; check price rises, bigger baskets or more frequent buying.
3. Split customers into new, repeat and lapsed: did we lose small customers while big ones grew?
4. Look at concentration: how much of the growth is a few large accounts?
5. Check data: duplicates merged, a tracking change, or a changed customer definition.
**Method choice and why:** A simple bridge table (customers, orders, value) first; segment cuts next.
**Pitfalls:** Growth built on price rises while volume erodes; losing low-value customers may be healthy or the early sign of a shrinking base; one-off bulk buyers.
**Deliverable:** A bridge chart from last period to this period (customer change effect, spend change effect) with a view on whether the pattern is sustainable.

**Likely follow-ups:** 1) *Good or bad?* Depends on why; revenue from fewer customers is riskier. 2) *What next?* Check retention of the lost customers.
**Common mistakes / traps:** Treating it as a contradiction; skipping the definition check.

### Q57 ⭐⭐ 🟡 How would you analyse delivery time performance and decide whether the average, median or a percentile is the right number to report?
**Asked at:** commonly asked (no company-specific report found); delivery and operations cases appear in Swiggy and Flipkart style guides (unverified).
**What the interviewer is checking:** Whether you look at the distribution and match the statistic to the customer promise.
**Say this in the interview:** "I would plot the delivery times first. Delivery times have a long tail of late orders, so the average hides them. I would report the median for typical and the 90th percentile for the late experience."

**Clarify first:** What is the promise (within 45 minutes)? Is time measured from order or from dispatch? Are cancelled orders included? Which region and slot?
**Plan:**
1. Data: order time, pickup, delivery time, city, slot, status.
2. Clean: remove impossible values (negative times), keep late orders (do not delete the tail), treat cancelled separately.
3. Plot a histogram and compute mean, median, 90th and 95th percentile. Illustration with 16 orders: mean 61.8 minutes, median 43.5, 90th percentile 110 (a few very late orders pull the mean up).
4. Compute the share delivered within the promise.
5. Cut by city, hour and rider, to find where the tail lives.
**Method choice and why:** Median for typical; percentile or share-on-time for the promise; mean only for capacity planning, because it adds up total effort.
**Pitfalls:** Averages hiding bad experiences; averages of averages across cities; small samples in a city making percentiles unstable.
**Deliverable:** A chart with median, 90th percentile and on-time share per city, with a one-line definition of each.

**Likely follow-ups:** 1) *Why not drop outliers?* They are real customers; investigate instead. 2) *Which for a service agreement?* The promise percentile.
**Common mistakes / traps:** Reporting only the mean; deleting outliers silently.

### Q58 ⭐⭐ 🟡 How would you analyse the diversity of a hiring pipeline stage by stage, and what would you be careful about in handling the data?
**Asked at:** commonly asked (no company-specific report found); HR funnel-by-stage analysis is a people-analytics theme (unverified).
**What the interviewer is checking:** Whether you find where groups drop off, and whether you treat sensitive data with care.
**Say this in the interview:** "I would compute the share of each group at every stage and the pass rate between stages, to see where the gap opens, and I would handle the data with consent, limited access and group-level reporting."

**Clarify first:** What is the purpose (fairness check, target tracking)? Which attributes are collected, with what consent, and are they self-declared? Who will see the output?
**Plan:**
1. Data: stage-level records (applied, screened, interviewed, offered, joined), role, source, and the attribute, collected voluntarily.
2. Compute each group's share at each stage and the pass rate stage to stage.
3. Compare pass rates between groups at the same stage, for the same role and source, so you do not compare different jobs.
4. Check numbers: small groups give unstable rates, so show counts and avoid percentages on tiny groups.
5. Look at the reasons (interviewer, source, criteria) only after you find the stage.
**Method choice and why:** Simple pass-rate tables first; a significance test or confidence range only where counts are large enough.
**Pitfalls:** Small samples; missing declarations (is "unknown" random?); mixing roles; treating a gap as proof of bias (it is a flag to investigate). Handling: collect only what is needed, restrict access, remove names and ids from the analysis file, suppress groups below a minimum count, report in aggregate. Legal rules on sensitive data (for example India's DPDP Act, from memory, unverified) must be confirmed with the legal and privacy team.
**Deliverable:** A funnel chart by group with pass rates and counts, a note on limits, and agreed next steps.

**Likely follow-ups:** 1) *Where do you look first?* The stage with the biggest gap in pass rate. 2) *Can you share individual data?* No.
**Common mistakes / traps:** Reporting tiny groups; ignoring consent; claiming discrimination from one table.

### Q59 ⭐⭐ 🟡 How would you analyse a recurring complaint that the 'dashboard shows lower sales than finance', if you had to start from the raw tables?
**Asked at:** commonly asked (no company-specific report found); reconciliation of dashboard to finance is a typical analyst scenario (unverified).
**What the interviewer is checking:** Whether you reconcile step by step and find the rule differences rather than argue about who is right.
**Say this in the interview:** "I would rebuild both numbers from the same raw table for one day, list every rule that differs, and bridge the gap line by line."

**Clarify first:** Which period, which dashboard number, which finance number (booked, invoiced, received)? By how much is the gap and has it been constant?
**Plan:**
1. Write each side's definition: sales date (order, invoice, payment), tax in or out, returns and cancellations, discounts, currency, time zone.
2. Pick one small period and rebuild the finance number from raw invoices and the dashboard number from its source table.
3. Check row counts and totals at each step: raw, after filters, after joins, after aggregation (joins that drop rows or duplicate them are common causes).
4. Bridge the gap: totals difference split into definition differences, missing data (late loads), duplicates, and real errors.
5. Test the fix on a second period.
**Method choice and why:** A reconciliation table (step, count, amount) in SQL or Excel; no modelling needed.
**Pitfalls:** Inner joins dropping orders with missing product or customer; late-arriving data; time zones moving sales across month ends; trusting either side blindly.
**Deliverable:** A bridge from dashboard to finance with each reason and amount, an agreed official definition, and a fix with an owner. Add a monthly check that compares the two totals.

**Likely follow-ups:** 1) *Who is right?* Whoever matches the agreed definition. 2) *Prevent it?* Metric dictionary and automated reconciliation.
**Common mistakes / traps:** Starting with the dashboard formulas; changing numbers before agreeing a definition.

### Q60 ⭐⭐ 🟡 How would you analyse whether employees are leaving soon after a manager change?
**Asked at:** commonly asked (no company-specific report found); attrition cohort cuts are a listed HR-analytics theme (unverified).
**What the interviewer is checking:** Whether you use a fair comparison window and a comparison group, and count people at risk, not only leavers.
**Say this in the interview:** "I would compare the exit rate in the 6 months after a manager change with the same period for teams without a change, for similar employees, because a spike alone proves little."

**Clarify first:** What counts as a change (new manager, reorganisation, promotion of the old one)? Voluntary or all exits? Which window (3 or 6 months)? How many changes occurred?
**Plan:**
1. Data: HRIS employee records with manager history, join and exit dates and reason, role, grade, tenure, team.
2. Define for each employee the date of a manager change and follow the next 6 months.
3. Compute the exit rate (leavers divided by people at risk) in that window.
4. Build a comparison group: similar teams and time windows with no change, same tenure bands.
5. Break down by tenure and by new-manager source (internal or external), since new joiners always leave more.
6. Use survival curves (the share still employed month by month) if enough data, showing the two groups side by side.
**Method choice and why:** Rate comparison first; survival view next; regression only with enough cases.
**Pitfalls:** Small numbers per manager; reorganisations that also change pay or location; people leaving before the change (the manager left because the team was already weak); privacy and not blaming a named manager from thin data.
**Deliverable:** A chart of exit rate after change vs comparison, with counts, and recommendations (for example a handover and a stay-conversation step).

**Likely follow-ups:** 1) *Causation?* Not proven; flag for follow-up and exit interviews. 2) *Which exits?* Regretted and voluntary first.
**Common mistakes / traps:** Counting leavers without the base; no comparison group.

### Q61 ⭐⭐ 🟡 You are asked to compare two branches' performance. How do you make the comparison fair?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you adjust for size, mix, and conditions instead of ranking raw totals.
**Say this in the interview:** "I would first ask what 'performance' means, then compare on rates and per-unit figures, and match for size, product mix, location and period so that the branches face similar conditions."

**Clarify first:** The goal (bonus, closing a branch, learning best practice)? Which metrics? Same period? Any known differences (city tier, opening date, staffing)?
**Plan:**
1. Choose a small set of metrics: revenue per square foot or per employee, conversion, margin, customer satisfaction, cost.
2. Normalise: use per-head, per-visitor or per-day figures; same number of days.
3. Adjust for mix: compare by product category or customer type so that a branch with more high-value items does not win by default.
4. Account for context: local market size, footfall, branch age, staffing levels, local holidays.
5. Check variation over time (a branch can win one month by luck); show several months.
**Method choice and why:** Side-by-side table with per-unit measures and a comparison against similar peer branches (more than two if available). Regression adjustment only if many branches.
**Pitfalls:** Ranking raw totals; one-month snapshots; a metric that can be gamed; ignoring things the branch cannot control.
**Deliverable:** A scorecard with 4-5 metrics, context notes, and a clear statement of what is controllable.

**Likely follow-ups:** 1) *Only two branches?* Say the comparison is weak and add history or other branches. 2) *Who wins?* Only on the agreed metric.
**Common mistakes / traps:** Comparing totals; mixing metrics into one score without weights agreed.

### Q62 ⭐⭐ 🟡 How would you analyse the data to recommend the best day and time for a weekly promotion?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you aim for incremental sales, not just the busiest slot.
**Say this in the interview:** "The busiest slot is not automatically the best: a promotion in an already busy slot gives away discount to people who would have bought anyway. I would look for slots with spare capacity and responsive customers, and ideally test them."

**Clarify first:** What is the goal (more orders, new customers, clearing stock)? Channel (email, app notification, in-store)? Capacity limits? Budget?
**Plan:**
1. Data: orders by day of week and hour for 3-6 months, past promotions with dates and results, channel open rates.
2. Build a heatmap of orders by day and hour; compute a baseline for each slot.
3. For past promotions, measure the lift against the same slot in non-promotion weeks (so that season and weekday are matched).
4. Check capacity and margin: delivery or staff limits, and discount cost.
5. Shortlist 2-3 slots and run an A/B test, rotating slots across similar customer groups.
**Method choice and why:** Heatmap plus lift against baseline; a short test confirms. Modelling only if many past campaigns.
**Pitfalls:** Choosing the peak slot; one or two past promotions as proof; confusing weekend effect with promotion effect; pull-forward (sales taken from the next days).
**Deliverable:** A recommendation with the top slot, expected incremental orders as a range, cost, and the test plan.

**Likely follow-ups:** 1) *No past promotions?* Use baseline traffic and run a test. 2) *Measure success?* Incremental orders and margin after the promotion week.
**Common mistakes / traps:** Recommending the peak; ignoring cannibalisation.

### Q63 ⭐⭐ 🟡 How would you analyse payroll data for anomalies such as duplicate payments or unusual overtime?
**Asked at:** commonly asked (no company-specific report found); payroll checks are a natural HR-analyst scenario (unverified).
**What the interviewer is checking:** Whether you use clear rules, handle sensitive data with care, and avoid accusing people from a flag.
**Say this in the interview:** "I would run rule-based checks for exact duplicates and then compare overtime to each person's own history and peers. Anything flagged goes to payroll for verification, not to a conclusion."

**Clarify first:** Which months and entities? What is "normal" per policy (overtime caps, approval rules)? Who owns follow-up? Who is authorised to see this data?
**Plan:**
1. Data: payroll register, attendance and overtime approvals, bank details, employee master. Work in a restricted, anonymised copy where possible.
2. Duplicates: same employee id and month paid twice; same bank account across different employees; same amount, date and payee.
3. Overtime: hours above policy cap; overtime with no approval; overtime hours that do not match attendance; a jump compared with the person's last 6 months; comparison against peers in the same role (using median and a spread measure such as the interquartile range).
4. Other flags: payments after the exit date, ghost-like records (no attendance but pay), round-number manual adjustments.
5. Review each flag with payroll against source documents.
**Method choice and why:** Rules and thresholds first; they are explainable. Statistical outlier or model-based detection only to prioritise.
**Pitfalls:** Many legitimate reasons (arrears, shift allowances, festival months); false positives; discussing names widely; wrong comparisons across roles.
**Deliverable:** A confidential exception list with reason code and amount at risk, summarised counts for management, and recommended controls.

**Likely follow-ups:** 1) *Who sees names?* Only payroll and audit owners. 2) *Recover money?* Process decided by finance and HR.
**Common mistakes / traps:** Treating a flag as fraud; sharing the list broadly.

### Q64 ⭐⭐ 🟡 How do you analyse a metric that is a ratio (such as conversion rate) across segments without being misled by different sample sizes?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you show counts and uncertainty, and avoid averaging percentages.
**Say this in the interview:** "I always show the numerator and denominator next to the rate. A 30 percent rate from 10 visitors is much less reliable than 20 percent from 600, so I add a confidence range or a minimum sample size."

**Clarify first:** What is the numerator and denominator exactly (visitors or sessions)? Which segments and period? How big a gap would matter to the business?
**Plan:**
1. Build a table: segment, conversions, visitors, rate.
2. Add a 95% confidence interval for each rate. Illustration: 3 of 10 is 30% with an interval of about 2% to 58% (very wide); 120 of 600 is 20% with an interval of about 17% to 23%. The 30% looks higher, but we cannot say it is.
3. Flag or group segments below a minimum count (for example under 100 visitors).
4. Never average segment rates; recompute the overall rate as total conversions divided by total visitors.
5. When comparing segments, use a test of two proportions, or ranges that do not overlap, and beware of testing many segments (some will look different by chance).
**Method choice and why:** Counts plus intervals is enough. For many segments of mixed size, shrink small groups toward the overall rate (a mention is enough at interview).
**Pitfalls:** Ranking segments by raw rate; mix effects (Simpson's paradox, see Q72); changing denominators.
**Deliverable:** A table or chart with error bars, small segments greyed out, and a plain note on what can and cannot be concluded.

**Likely follow-ups:** 1) *Minimum sample size?* Depends on the rate and the difference to detect; use a power calculation. 2) *Why not just a percentage?* It hides reliability.
**Common mistakes / traps:** Averaging percentages; trusting tiny segments. (Intervals are computed, rounded, normal approximation.)

### Q65 ⭐⭐ 🟡 How do you analyse data you do not have the domain knowledge for, for example a logistics dataset on your first week?
**Asked at:** commonly asked (no company-specific report found); learning speed in a new domain is a common behavioural-technical question (unverified).
**What the interviewer is checking:** Whether you learn fast, ask the right people, and avoid overconfident conclusions.
**Say this in the interview:** "I learn the process before I analyse: I draw the flow of a shipment, list the key terms with someone who knows the work, and then profile the data to see if it matches that story."

**Clarify first:** Who is the domain expert I can ask for 30 minutes? What decision will this dataset feed? Is there a data dictionary?
**Plan:**
1. Map the process end to end (order, pickup, hub, delivery) and the events that create each row.
2. Build a glossary of terms and units (for example the exact meaning of "delivered", of delay, of RTO or returned-to-origin, which I would confirm, not assume).
3. Profile the data: row counts, date ranges, missing values, duplicates, value ranges, category lists.
4. Reconcile a few known facts with the expert (daily volumes, typical transit time).
5. Take 10 shipments end to end and verify the story in the rows.
6. Only then run the first simple summaries, and share them early for corrections.
**Method choice and why:** Descriptive statistics and simple charts; no complex model until definitions are confirmed.
**Pitfalls:** Assuming a column means what its name suggests; unit mix-ups; reading normal practice as an anomaly; hiding that you are new.
**Deliverable:** A one-page data guide (definitions, caveats, open questions) plus first findings labelled "draft for expert review".

**Likely follow-ups:** 1) *Who do you ask?* Operations team members and previous analysts. 2) *How do you avoid wrong assumptions?* Write them down and check each.
**Common mistakes / traps:** Pretending to know; skipping the profile step.

### Q66 ⭐⭐ 🟡 How would you analyse a request to 'compare this year with last year' when the business changed definitions mid-year?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you restore comparability rather than comparing unlike numbers.
**Say this in the interview:** "I would first find exactly what changed and when, then restate both years on one definition. If I cannot, I would show the two series separately and mark the break."

**Clarify first:** What changed (for example the definition of an active customer, or of attrition, or the product hierarchy), on which date, and why? Which definition does leadership want going forward?
**Plan:**
1. Document the old and new rule in plain words, with the effective date.
2. Check whether raw data still exists to recalculate the old year under the new rule (best), or the new year under the old rule.
3. If yes, recompute and compare like with like, and reconcile the old and new totals for an overlap period.
4. If not, split the comparison into before and after the change, and show the size of the break using a month where both rules exist.
5. Adjust any trend line or target for the break, and flag it on every chart.
**Method choice and why:** Restatement on one definition is simplest to explain; a bridge (old rule number to new rule number) when full restatement is impossible.
**Pitfalls:** Silent comparison across the break; reading definition effects as business change; changing history without a record.
**Deliverable:** A comparison table on a single definition, a note on what changed and the impact in numbers, and a change log entry.

**Likely follow-ups:** 1) *What if they insist on the raw comparison?* Show it with the break clearly labelled. 2) *Prevent?* A metric change log.
**Common mistakes / traps:** Not asking when the change happened; mixing definitions in one trend line.

### Q67 ⭐⭐ 🟡 How would you analyse ticket resolution time when a few tickets stay open for months?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you handle open items (censored data) and skewed values.
**Say this in the interview:** "Tickets still open are not missing data, they are the slowest cases. If I only average resolved tickets I understate the problem, so I report the median, a high percentile and the number of aged open tickets separately."

**Clarify first:** What clock starts and stops the timer (does waiting for the customer count)? Priority levels? What is the service target?
**Plan:**
1. Data: ticket id, created, first response, resolved, status, priority, team, reopen flag.
2. Resolved tickets: compute median and 90th percentile time by priority; Illustration with 12 resolved tickets (days): mean 3.9, median 3.0, a few high values pull the mean.
3. Open tickets: compute their current age; report counts above thresholds (30, 60, 90 days) and the oldest list.
4. Show the share resolved within target by cohort of creation month (the most recent months look better only because slow tickets are not closed yet).
5. Investigate the old tickets one by one (blocked, waiting on others, forgotten).
**Method choice and why:** Percentiles and an ageing table. A survival-style curve (share resolved by day) if you want one chart that includes open tickets properly.
**Pitfalls:** Analysing only closed tickets; using the mean; judging recent months too early; automatic closure rules that hide the issue.
**Deliverable:** A dashboard tile set: median, 90th percentile, on-target share, count of tickets older than 30 days, plus a short action list for the oldest.

**Likely follow-ups:** 1) *Remove old tickets as outliers?* No, they are the finding. 2) *Which statistic for leaders?* On-target share and ageing.
**Common mistakes / traps:** Dropping open tickets; relying on the average.

### Q68 ⭐⭐ 🟡 How do you decide between building a quick pivot-table analysis and a fuller model when time is short?
**Asked at:** commonly asked (no company-specific report found); data-light and time-pressure scenarios are common (unverified).
**What the interviewer is checking:** Judgement: matching effort to the decision and being open about limits.
**Say this in the interview:** "I ask what decision this feeds and how costly a wrong answer is. If it is a quick directional call I do the pivot now and say what it cannot tell us; I build a model only if the decision is big and the question needs it."

**Clarify first:** The decision, the deadline, the size of the money or people at stake, and whether it is reversible. Is the answer a direction or a precise number?
**Plan:**
1. Spend the first hour on a pivot or SQL summary: totals, trend, key splits.
2. See whether the pattern is obvious and stable; if yes, stop and communicate.
3. If the answer is unclear or high-stakes (forecast, pricing, many interacting factors), propose a fuller model with a scope and date.
4. Deliver the quick answer on time, with stated limits, and agree whether to continue.
**Method choice and why:** Simple first, because it is fast, explainable and easy to check; a model adds value when the pivot cannot separate effects or must predict.
**Pitfalls:** Over-engineering when the answer was visible; a pivot hiding a mix problem; no record of assumptions; presenting a rough number as exact.
**Deliverable:** The pivot with a three-line "what this shows, what it does not, what I would do next" note.

**Likely follow-ups:** 1) *Quick answer then wrong?* Say upfront the confidence level and what would change it. 2) *When is the model worth it?* Repeated, high-value decisions.
**Common mistakes / traps:** Saying "model always"; no stated limits.

### Q69 ⭐⭐ 🟡 The table below shows attrition by tenure band. Where is the problem, and what would you analyse next?
Inline data: 0-6 months: 200 employees, 30 left. 6-24 months: 500 employees, 40 left. 24+ months: 800 employees, 24 left (exercise data, one year).
**Asked at:** commonly asked (no company-specific report found); attrition cuts by tenure are a listed HR-analytics theme (unverified).
**What the interviewer is checking:** Whether you compute rates (not counts) and then ask why.
**Say this in the interview:** "The problem is the first six months: 15 percent left, against 8 and 3 percent in the other bands. I would look at who they are, where they were hired and why they left."

**What the data shows:** Rates fall as tenure rises, and early attrition is five times the long-tenure rate. The 6-24 band has the most leavers by count (40), but the first band has by far the highest rate.
**Working:**
1. 0-6 months: 30 / 200 = 15.0%.
2. 6-24 months: 40 / 500 = 8.0%.
3. 24+ months: 24 / 800 = 3.0%.
4. Total: 94 leavers / 1,500 employees = 6.27% (about 6.3%).
5. Share of all leavers from the first band: 30 / 94 = 31.9%, although it holds 13.3% of headcount (200 / 1,500).
**Result:** Early-tenure attrition is 15.0%, about 2.4 times the company rate of 6.3% and 5 times the 24+ rate. (Denominators here are the group headcount; strictly, average headcount during the year is better.)
**Caveats / what else I would check:** A one-year snapshot; employees who join during the year are partial-year in the band; is this voluntary or including terminations at probation; small teams; does the pattern differ by hire source, location, manager or role.
**Next step / recommendation:** Break the first band by hiring source, role, location and manager; read exit reasons; compare pre-joining expectations to the job; consider onboarding and 30-60-90-day check-ins. Measure by tracking 6-month retention of each new cohort.

**Likely follow-ups:** 1) *Is it the largest count?* The 6-24 band has 40 leavers (largest count) but the first band has the highest rate; use rates. 2) *Is some attrition healthy?* Yes, probation exits of poor fits may be intended; separate voluntary and regretted exits.
**Common mistakes / traps:** Ranking by counts; ignoring the denominator; assuming all exits are bad.

### Q70 ⭐⭐ 🟡 The table below shows time-to-hire by stage in days. Which stage should be analysed first, and what is the total median time?
Inline data: Screening 5; first interview 9; second interview 6; offer approval 12; offer to join 30 (days, medians, exercise data).
**Asked at:** commonly asked (no company-specific report found); hiring-funnel stage analysis is a listed HR scenario (unverified).
**What the interviewer is checking:** Whether you size each stage, separate what you can control, and notice that medians do not add exactly.
**Say this in the interview:** "The stage medians add up to about 62 days. Offer to join is the longest at 30 days, but it is mostly notice period, so I would look first at offer approval at 12 days, which the company controls, and then at offer-to-join drop-offs."

**What the data shows:** Two stages dominate: offer to join (30 days) and offer approval (12 days); together they are 42 of 62 days.
**Working:**
1. Sum of stage medians: 5 + 9 + 6 + 12 + 30 = 62 days.
2. Shares of 62: screening 8.1%, first interview 14.5%, second interview 9.7%, offer approval 19.4%, offer to join 48.4%.
3. Time before the offer (screening to second interview): 5 + 9 + 6 = 20 days; offer approval plus join: 42 days.
**Result:** About 62 days, an approximation: the median of total time is not exactly the sum of stage medians; compute it from candidate-level data.
**Caveats / what else I would check:** Notice periods are set by the candidate's employer; offer-to-join may include candidates who never joined; stage definitions (does waiting for a candidate's availability count?); medians hide long tails, so check 75th and 90th percentiles; differences by role and level.
**Next step / recommendation:** Analyse offer approval first (the delays are internal: approvers, steps, waiting days), then the offer-to-join gap (earlier offers, joining bonus, stay-in-touch). Track median days and the offer-acceptance and dropout rates by stage.

**Likely follow-ups:** 1) *Why not 30 first?* It is the biggest but least controllable; I would still check dropouts. 2) *Can you add medians?* Only as an estimate.
**Common mistakes / traps:** Reporting 62 as exact; ignoring what is controllable.

### Q71 ⭐⭐ 🟡 A promotion ran in two cities. Using the figures below, what is the lift in each city and what would you check before comparing them?
Inline data: City X: before 200 orders/day, during 260. City Y: before 50, during 75 (exercise data).
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you separate percentage lift from absolute lift and check the baseline.
**Say this in the interview:** "City Y has the higher lift at 50 percent against 30 percent, but City X added more orders a day, 60 against 25. Y started from a small base, so I would check baseline and other factors before calling either a winner."

**What the data shows:** Both cities grew; the smaller city grew faster in percentage terms, the larger in absolute orders.
**Working:**
1. City X: (260 - 200) / 200 = 30%; extra orders 60 a day.
2. City Y: (75 - 50) / 50 = 50%; extra orders 25 a day.
3. Combined: before 250, during 335; (335 - 250) / 250 = 34% (a weighted result, closer to X's lift because X is larger).
**Result:** X +30% (+60 orders/day), Y +50% (+25 orders/day), combined +34% (+85 orders/day). The 20-point gap between cities is in percentage points.
**Caveats / what else I would check:** Was the baseline normal (season, holiday, a previous campaign)? Same promotion type, discount and marketing spend? A control city or the same weeks last year to separate the promotion from natural growth; promotion cost per extra order and margin; pull-forward (a dip after the promotion); the number of days before and during (a few days are noisy); small base in Y makes percentages jump easily.
**Next step / recommendation:** Compare against a control group, compute incremental orders and cost per incremental order, and track two weeks after the promotion ends before deciding on rollout.

**Likely follow-ups:** 1) *Which city did better?* Depends on the metric: percentage (Y), volume (X), and profit after cost (unknown). 2) *Is 50% reliable?* Less so, because the base is small.
**Common mistakes / traps:** Declaring Y the winner on percentage alone; ignoring the baseline and cost.

### Q72 ⭐⭐ 🔴 The conversion rate fell in every segment but rose overall. How would you analyse this and explain it simply?
**Asked at:** commonly asked (no company-specific report found); this is the classic Simpson's paradox case (the name for this reversal).
**What the interviewer is checking:** Whether you recognise a mix shift and know which number to trust.
**Say this in the interview:** "This is a mix effect: the share of visitors moved toward the segment that converts better, so the overall rate rose even though each segment got worse. I would show the segment rates and the shift in mix side by side."

**Clarify first:** What are the segments (device, source, region)? Same definition of conversion in both periods? Is the question about each segment's health or the overall rate?
**Plan:**
1. Build a table by segment: visitors, conversions, rate, for both periods, plus the share of visitors.
2. Illustration. Last period: mobile 8,000 visitors at 2.0% (160), desktop 2,000 at 6.0% (120); overall 280 / 10,000 = 2.80%. This period: mobile 4,000 at 1.9% (76), desktop 6,000 at 5.8% (348); overall 424 / 10,000 = 4.24%. Both segments fell (0.1 and 0.2 points) yet overall rose by 1.44 points.
3. Separate the two effects: apply this period's rates to last period's mix: (0.019 x 8,000 + 0.058 x 2,000) / 10,000 = 2.68%. So with the same mix, the rate would have dropped from 2.80% to 2.68%; the rest of the rise comes from the mix shifting toward desktop.
4. Find why the mix moved (campaign changes, an app issue pushing mobile traffic away).
**Method choice and why:** A mix-versus-rate split in a simple table; no model needed.
**Pitfalls:** Quoting the overall rise as success; also missing why each segment fell.
**Deliverable:** A two-line explanation, "More visitors came from the strong segment, so the average rose, but each segment is weaker", and a chart with both periods per segment. Recommendation: judge performance by segment rates at a fixed mix and investigate the declines.

**Likely follow-ups:** 1) *Which number is right?* Both are arithmetically right; the segment view shows underlying performance. 2) *Simple analogy?* Class average rises because more strong students joined while each student's marks dropped.
**Common mistakes / traps:** Saying the data is wrong; reporting only the overall. (All figures are computed exercise values.)

### Q73 ⭐⭐ 🔴 How would you analyse whether a loyalty programme increases spending, when the best customers are the ones who joined?
**Asked at:** commonly asked (no company-specific report found); selection bias in retention programmes is a gap-fill theme in this book (judgement).
**What the interviewer is checking:** Whether you avoid reading selection as effect: good customers join, so members spend more anyway.
**Say this in the interview:** "Members spending more does not prove the programme works, because the best customers chose to join. I would compare each member's spending before and after joining, against similar non-members over the same time."

**Clarify first:** How do customers join (open to all, invite, or after a purchase)? What benefits? When did it launch? What is the goal, more spend, more frequency, or retention?
**Plan:**
1. Data: customer id, join date, monthly spend and orders for 12 months before and after, plus customer traits.
2. Define the pre-period to remove those who joined only because they were about to spend a lot (the join often follows a big purchase, which makes "before" look low or "after" high).
3. Match each member to a non-member with similar pre-period spend, frequency, tenure and category mix.
4. Compare the change in spend for members versus matched non-members (difference-in-differences).
5. Check whether the effect fades after the first months and whether it is just pull-forward or points earned and burnt.
6. Subtract the programme cost (points, discounts) to see the net benefit.
**Method choice and why:** Matched before/after is understandable. A randomised holdout (some eligible customers not invited) is the cleanest if the business allows it.
**Pitfalls:** Comparing members with all non-members; survivorship (only remaining customers are counted); the join-timing trap; ignoring cost.
**Deliverable:** A short result: "Matched members spent X more, range Y to Z, net of cost W", with an honest note on what matching cannot remove, and a proposal for a holdout test.

**Likely follow-ups:** 1) *Can you prove it?* Only with a randomised test. 2) *What if no holdout is possible?* Use matching and state limits.
**Common mistakes / traps:** Members versus non-members; ignoring programme cost.

### Q74 ⭐⭐ 🔴 How would you analyse the data to forecast headcount needs for the next 12 months, and what assumptions would you expose?
**Asked at:** commonly asked (no company-specific report found); workforce planning is a standard people-analytics theme (unverified).
**What the interviewer is checking:** Whether you build the forecast from demand, attrition and hiring pipeline, and state the assumptions openly.
**Say this in the interview:** "Headcount needed equals the workload-driven target, plus expected attrition replacement, minus current headcount. I would build it by team, give a base and a range, and list every assumption."

**Clarify first:** What drives demand (sales volume, projects, customers)? Is there a budget or hiring freeze? Which roles and locations? Does the plan include internal moves and contractors?
**Plan:**
1. Start with current headcount by team and role from HRIS.
2. Required headcount: business volume forecast divided by productivity per person (for example orders handled per agent), by team.
3. Attrition: historic rate by team and tenure, applied to current headcount. Illustration: 1,000 people, 8% growth in workload gives a target of 1,080; 12% attrition means 120 leavers; so hires needed are 80 (growth) + 120 (replacement) = 200.
4. Hiring lead time: time to hire plus notice period, so that requests start months ahead; add ramp-up time before a new hire is fully productive.
5. Build scenarios: low, base, high for growth and attrition; show hires per month.
**Method choice and why:** A driver-based spreadsheet model first; time-series forecasting of attrition only if there is long clean history.
**Pitfalls:** Assuming attrition stays flat; ignoring seasonality and hiring lead time; ignoring productivity changes (automation); using headcount instead of full-time equivalents.
**Deliverable:** A monthly plan by team with scenarios, an assumptions list (growth, attrition, productivity, lead time, budget) and the triggers for revising it. Review quarterly.

**Likely follow-ups:** 1) *Biggest uncertainty?* Business volume and attrition. 2) *How present?* Base case plus range.
**Common mistakes / traps:** A single number with hidden assumptions; forgetting replacement hiring.

### Q75 ⭐⭐ 🔴 How would you analyse the impact of an outage that you cannot rerun, when only partial logs exist?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you estimate honestly with a counterfactual and give a range, rather than pretend precision.
**Say this in the interview:** "I would estimate what would normally have happened in that window from comparable periods, subtract what we actually saw, and give a range, clearly saying how much of the log coverage is missing."

**Clarify first:** Outage start and end (as best known), who and what was affected, and what the business wants (revenue lost, customers hit, an SLA claim)? What logs and other sources exist (payments, support tickets, server metrics)?
**Plan:**
1. Inventory sources: partial logs, payment gateway or finance records, call-centre tickets, social mentions, and monitoring data.
2. Establish coverage of the logs: what share of events are present, and whether the gaps are random or concentrated.
3. Build the baseline: the same weekday and hour in recent comparable weeks, adjusted for trend. Illustration: normal 1,000 orders per hour, outage of 2 hours, so about 2,000 expected orders.
4. Measure actuals from the most reliable source (payments are better than app logs). If the logs cover 60% of events, scale up with a stated assumption, or use the finance totals directly.
5. Estimate lost orders = baseline minus actual, and separate lost from delayed (some customers return later); check the recovery period after the outage.
6. Give a low and high estimate, with ranges for baseline and coverage.
**Method choice and why:** Baseline comparison with a transparent range; a time-series counterfactual only if there is plenty of history.
**Pitfalls:** Treating missing logs as zero activity; one comparison week only; ignoring delayed purchases and customers lost permanently; false precision.
**Deliverable:** A short report: duration, estimated impact as a range with method and assumptions, confidence level, and what logging to add so the next incident can be measured.

**Likely follow-ups:** 1) *Which source is most reliable?* Money records. 2) *Lost or delayed?* Check the weeks after.
**Common mistakes / traps:** Pretending exactness; counting missing logs as no orders.

### Q76 ⭐⭐ 🔴 How would you analyse a model's output (for example, a churn score) to decide whether the business can trust it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you test a model against what really happened and against the business decision, not just quote one accuracy number.
**Say this in the interview:** "I would not trust a score until I have checked it on cases the model never saw, compared it with a simple baseline, and shown it helps the decision it is meant to support."

**Clarify first:** What decision uses the score (who gets a retention call)? What does a wrong call cost, a missed leaver or a wasted call? Who built it, and on which period of data?
**Plan:**
1. Get scores plus the real outcome (did the person or customer actually leave in the following 90 days?). Scores must be as they were at the time, not recalculated later.
2. Check on a later period the model never saw (a "hold-out"), not on the data it learned from.
3. Rank test: among the top 10% scored, what share really left, compared with the overall rate (called "lift").
4. Calibration: of people scored 30% risk, do about 30% leave?
5. Compare with a simple baseline (for example "tenure under one year") to see if the model adds anything.
6. Check by group (region, gender, tenure band) for uneven errors, and watch whether performance decays month by month.
**Method choice and why:** Start with a decile table (ten equal groups from highest to lowest score, with actual leave rate in each). Anyone can read it. Move to precision and recall only once the cost of each type of error is known.
**Pitfalls:** "Leakage" (a column that only exists after the person has left); one overall accuracy figure when only 5% leave (predicting "nobody leaves" scores 95%); testing on training data; ignoring drift.
**Deliverable:** A one-page verdict: trust for ranking, yes or no, with the decile table, baseline comparison, known weak groups and a monitoring plan.

**Likely follow-ups:** 1) *Why is accuracy misleading?* Because rare outcomes make "predict nobody" look good. 2) *How often recheck?* Monthly at first, then quarterly, or when the data feeding it changes.
**Common mistakes / traps:** Trusting the builder's own score on training data; skipping the baseline; reporting without the cost of errors.

### Q77 ⭐⭐ 🔴 How would you analyse which of 40 possible factors drive employee attrition, and how would you avoid reporting spurious drivers?
**Asked at:** commonly asked (no company-specific report found); HR attrition diagnosis appears in HR-analytics question banks (unverified).
**What the interviewer is checking:** Awareness that testing many factors throws up false hits by chance, and that "associated with" is not "causes".
**Say this in the interview:** "I would test the factors, but control for the number of tests and confirm findings on a separate period, otherwise some of the 40 will look important purely by luck."

**Clarify first:** Voluntary or all exits? Which window? What decision follows (which lever to pull)? Which factors can HR actually change?
**Plan:**
1. Define leaver (left within 12 months) and the population at risk; build one row per employee.
2. Clean the 40 factors, group the overlapping ones (age, tenure and grade move together).
3. Screen each factor alone: compare leave rates across its values.
4. Fit one combined model (logistic regression, a method that gives the chance of leaving from many factors together) so overlapping factors share credit.
5. Confirm on a held-back period or group.
**Method choice and why:** The arithmetic of chance: at the usual 5% threshold, 40 independent tests give about 2 false hits expected, and an 87% chance of at least one. A stricter cut-off (for example 0.05 / 40 = 0.00125, called Bonferroni) or a shrinkage method (lasso) cuts that. Plain comparisons first, modelling second.
**Pitfalls:** Reverse causation (low engagement score recorded after the resignation was decided); small groups; ranking by p-value instead of effect size; reporting factors HR cannot act on.
**Deliverable:** A short list of 3 to 5 factors with effect sizes, confidence, whether they held on the confirmation data, and a recommended pilot to test cause.

**Likely follow-ups:** 1) *Why not just report everything significant?* Roughly 2 of 40 would be noise. 2) *Can we say it causes attrition?* No, only a pilot or experiment can.
**Common mistakes / traps:** Running 40 tests and quoting the winners; ignoring overlap between factors; no confirmation step.

### Q78 ⭐⭐ 🔴 Sales for a product are 100, 110, 125, 140 units over four months. How would you analyse whether growth is accelerating, and what is the month-on-month growth each month?
Inline data: Exercise data.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you separate the size of the increase from the percentage growth, and are careful about concluding "acceleration" from three data points.
**Say this in the interview:** "Month-on-month growth is 10.0%, 13.6% and 12.0%. Units added per month rose from 10 to 15 and stayed at 15, so growth rate has not clearly accelerated; I would not call it from four points."

**Clarify first:** Are these units sold in each month or cumulative? Are months equal in selling days? Any promotion in months 2 and 3? Acceleration means the growth rate rising, or the unit increase rising? I fix: units per month; rate first, then increase.
**Plan:**
1. Month-on-month % = (this month / last month) - 1. Working: 110/100 = +10.0%; 125/110 = +13.6% (13.64); 140/125 = +12.0%.
2. Units added: +10, +15, +15.
3. Overall: 100 to 140 is +40% in 3 steps, about 11.9% a month on average (1.4 to the power 1/3, minus 1).
4. Compare the rate and the increase: the increase went up then flat; the rate went up then down.
**Method choice and why:** With four points, plain differences and ratios are enough. Use a trend line only with 12 or more months, and compare against the same months last year.
**Pitfalls:** Calling 10 to 13.6 acceleration while ignoring the drop to 12; mixing "percent" and "percentage points" (13.6% to 12.0% is a fall of 1.6 percentage points); days in the month; a one-off promotion.
**Deliverable:** A small table (units, change, % change) with a line: "steady growth of about 12% a month, with no clear acceleration; more months needed."

**Likely follow-ups:** 1) *Is the growth linear or compounding?* Increases of 10, 15, 15 sit between the two; too few points to say. 2) *What would you add?* Same months last year, price and promo calendar.
**Common mistakes / traps:** Confusing units increase with rate; concluding a trend from one jump; not stating the rounding (one decimal).

### Q79 ⭐ 🟢 How would you analyse the data for a request from a senior leader who says they only need 'one number'?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can give one headline while protecting the leader from a misleading number.
**Say this in the interview:** "I would give them one number, but first agree exactly what it means, and put one line of context next to it so it cannot be misread."

**Clarify first:** What decision will this number drive? Which exact definition (attrition: voluntary or all? headcount: including contractors?)? Compared with what, last month, target, last year?
**Plan:**
1. Confirm the definition and the period in writing.
2. Compute it from the single trusted source and reconcile once with another report.
3. Choose the one comparator (target or last year) that makes the number meaningful.
4. Prepare a backup page (breakdown by region, trend) in case they ask "why".
**Method choice and why:** A leader wants speed. The headline is the answer; the drill-down stays in your pocket. A number alone ("attrition is 14%") invites a wrong decision, so add "up 2 points on last year".
**Pitfalls:** Giving a number without definition; an average hiding a big gap between teams; sending 10 numbers when asked for one; not saying how fresh the data is.
**Deliverable:** One line: number, comparator, date of data, one-sentence meaning; plus an appendix ready on request.

**Likely follow-ups:** 1) *What if the number is misleading?* Say so briefly and offer the second number that fixes it. 2) *What if they refuse context?* Give the number with a footnote on the definition.
**Common mistakes / traps:** Refusing to simplify; or simplifying so much that the number has no meaning.

### Q80 ⭐ 🟢 How do you analyse an HRIS export for data-privacy risks before sharing it with a manager?
**Asked at:** commonly asked (no company-specific report found); privacy items are a differentiator, not a documented company question.
**What the interviewer is checking:** That you treat personal data carefully and share only what the manager needs.
**Say this in the interview:** "Before anything leaves my hands I list each column, remove what the manager does not need, and check that small groups cannot identify a person. I would also confirm company policy and legal rules, such as India's DPDP Act (from memory, unverified), with the privacy owner."

**Clarify first:** Who is the manager, what decision, and are they allowed to see this data (their own team only)? Is there a company data-sharing policy?
**Plan:**
1. Classify every column: identifiers (name, employee ID, phone), sensitive (salary, health, disciplinary, caste or religion if held), harmless.
2. Remove or mask whatever is not needed for the purpose ("data minimisation").
3. Replace names with a code, or aggregate (team averages) instead of rows.
4. Check small cells: a group of 2 or 3 people lets the reader guess who is who; combine or hide those.
5. Check the file itself: hidden sheets, filters, comments, formulas linking to the full file.
6. Share via an approved, access-controlled place, not a personal email.
**Method choice and why:** Aggregating is safer than masking; masking is safer than sharing raw rows. Take the simplest option that still answers the question.
**Pitfalls:** Deleting names but leaving a unique combination (grade, joining date, location); forgetting hidden columns; forwarding the same file to others.
**Deliverable:** The reduced file plus a short note of what was removed and why, logged for audit.

**Likely follow-ups:** 1) *What if the manager insists on salary?* Ask for the business reason and escalate to the data owner. 2) *Minimum group size?* A company rule; commonly 5 or more (confirm the policy).
**Common mistakes / traps:** Sharing the full export "just in case"; thinking an employee ID is anonymous.

### Q81 ⭐ 🟢 How would you analyse feedback from an employee engagement survey when comments could identify people?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Protecting respondent confidentiality while still extracting themes.
**Say this in the interview:** "I would analyse comments in themes at group level, hide any group too small to stay anonymous, and edit out names and details before anyone outside the survey team reads them."

**Clarify first:** What was respondents promised about anonymity? Who will read the output? What minimum group size does policy set?
**Plan:**
1. Keep raw comments only with the survey team; remove names, IDs and the metadata that points to individuals.
2. Group comments into themes (pay, manager, workload, growth) by reading a sample and tagging; count each theme.
3. Cut by team or location only if the group has enough responses (for example, 10 or more, per policy); otherwise combine.
4. Redact identifying details in quotes (a unique project, a named manager, a date).
5. Report the share of comments per theme and the trend against the last survey.
**Method choice and why:** Manual tagging of a sample plus counts is enough for a few hundred comments; use text-analysis tools only for thousands, and still review by hand. Quotes illustrate, they do not prove.
**Pitfalls:** Showing a comment from a team of 4; sentiment scores treated as truth; cutting by too many filters (location and grade and gender) until one person remains; reporting low-response groups as typical.
**Deliverable:** A theme summary with counts, safe example quotes, response rates, and an action list; no raw comment file shared.

**Likely follow-ups:** 1) *Someone writes about harassment?* Follow the company escalation policy; do not ignore it because it was meant to be anonymous. 2) *Small team?* Merge with a similar team.
**Common mistakes / traps:** Promising anonymity then slicing too finely; sharing raw verbatims.

### Q82 ⭐ 🟢 What deliverables would you produce at the end of a typical analysis, and how do they differ for an executive and for an analyst peer?
**Asked at:** commonly asked (no company-specific report found); guides stress reasoning and recommendation (Interview Query, Dataford, unverified).
**What the interviewer is checking:** That you tailor the output to the audience and leave work others can reuse.
**Say this in the interview:** "Executives get the answer and the decision in one page; analyst peers get the method, the code and the assumptions so they can reproduce it."

**Clarify first:** Who reads it, what decision, how much time do they have, will it be repeated?
**Plan:**
- For an executive: one-page summary (answer first, 2 or 3 supporting figures, one chart, recommendation, risks, next step); plain words, no jargon.
- For an analyst peer: cleaned dataset or query, code or workbook with comments, definitions and assumptions, checks done (row counts, reconciliations), limits and a README on how to rerun.
- For both: the same numbers, with a version date and the data source.
**Method choice and why:** Build the analyst version first (it is the evidence), then compress to the executive version. If they disagree, the executive page is wrong.
**Pitfalls:** Sending executives a 30-slide deck; sending peers only screenshots; no record of definitions; unlabelled files ("final_v3").
**Deliverable:** Executive summary + backup appendix + reproducible workbook or script in a shared folder.

**Likely follow-ups:** 1) *Which comes first?* The answer, then the proof. 2) *If asked for a quick Excel?* Still add a notes sheet with definitions and sources.
**Common mistakes / traps:** One output for everybody; hiding the assumptions.

### Q83 ⭐ 🟢 How do you decide when an analysis is 'good enough' to share and when it needs more work?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Judgement about effort versus decision value, not perfectionism or sloppiness.
**Say this in the interview:** "It is good enough when more work would not change the decision, and the numbers have passed my basic checks. I share early with the limits clearly stated."

**Clarify first:** What decision, by when, and how costly is being wrong? A reversible choice needs less rigour than a pay decision for 5,000 people.
**Plan:**
1. Core checks done: totals reconcile with a trusted report, no duplicates, no unexplained gaps, results pass a sense check.
2. Would a different reasonable assumption flip the recommendation? If not, stop refining.
3. Is the key caveat written beside the result?
4. Has someone else glanced at it (peer review) when the stakes are high?
5. If time is short, share a directional answer with confidence level and a date for the final.
**Method choice and why:** Match rigour to risk. A directional view for a quick call; a full check for anything touching pay, compliance or a leadership slide.
**Pitfalls:** Polishing charts while the data is unchecked; sharing a number that cannot be explained; infinite refinement after the answer is stable.
**Deliverable:** The result plus a "confidence and limits" line.

**Likely follow-ups:** 1) *What if the manager pushes for speed?* Share the draft marked as provisional. 2) *Which check never gets skipped?* Reconciliation to a known total.
**Common mistakes / traps:** Treating "more analysis" as always better; no stated caveats.

### Q84 ⭐ 🟡 How would you analyse the impact of an AI screening tool on shortlisting, including possible bias?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic for HR analytics.
**What the interviewer is checking:** Comparing before and after fairly, and testing for unequal outcomes by group, with legal care.
**Say this in the interview:** "I would compare shortlisting rates and quality of hires before and after the tool, then compare selection rates across groups, and bring in legal if one group's rate is much lower."

**Clarify first:** What was the tool meant to improve, speed, cost or quality? Which roles? Which group data (gender, age, college tier) is lawfully held and usable?
**Plan:**
1. Funnel per role: applications, shortlisted, interviewed, hired, before versus after, or tool-scored versus human-only if both exist.
2. Selection rate by group = shortlisted / applied. Compare the lowest group's rate to the highest (the "four-fifths" rule of thumb from US practice, from memory, unverified, flags a ratio below 80%).
3. Quality: interview-to-offer rate, 6-month performance, early attrition of those the tool shortlisted.
4. Sample audit: have a person rescreen a random batch the tool rejected; how many would have passed?
5. Look at which inputs the tool uses and any proxies (college, pin code).
**Method choice and why:** Rates and ratios are explainable to legal and HR; model-explanation tools only if the vendor allows.
**Pitfalls:** Different job mix before and after; tiny group counts; judging fairness only on outcomes of those hired; no human check.
**Deliverable:** Funnel table, group rates, audit result and a recommendation: continue, adjust or pause.

**Likely follow-ups:** 1) *If bias appears?* Pause or add human review, document, escalate to legal. 2) *No group data?* Say so; use proxies only with approval.
**Common mistakes / traps:** Assuming an algorithm is neutral; claiming bias from two or three people.

### Q85 ⭐ 🟡 How would you analyse the return on investment of a learning and development programme?
**Asked at:** commonly asked (no company-specific report found); programme evaluation with a control group appears in HR question banks (unverified).
**What the interviewer is checking:** Linking training to a business outcome fairly, with a comparison group, and costing it honestly.
**Say this in the interview:** "I would pick one business outcome the programme claims to improve, compare participants with similar non-participants, and set the gain against the full cost."

**Clarify first:** What did the programme aim to change (sales per rep, time to proficiency, attrition)? Over what period? Who joined, and how were they chosen?
**Plan:**
1. Define the outcome metric and when to measure (for example 6 months after).
2. Total cost: fees, trainer, participant hours at their pay, travel.
3. Build a comparison group of non-participants of the same role, tenure and prior performance.
4. Compare the change in the outcome for both groups (before to after).
5. Convert the extra gain to money; ROI = (gain - cost) / cost.
**Method choice and why:** Difference between the two groups' before-and-after change is the simple fair method. Randomised or staggered rollout is better if possible.
**Pitfalls:** Participants were often the keen or high-potential employees (selection bias); crediting training for something else that changed; measuring only satisfaction scores; leaving out participant time.
**Deliverable:** A one-page result with ROI range (low, base, high), assumptions, and a recommendation to scale, fix or stop.

**Likely follow-ups:** 1) *Can't measure money?* Use the non-money metric, such as time to proficiency. 2) *Short timeline?* Report early indicators, label them provisional.
**Common mistakes / traps:** Comparing participants with everyone else; claiming ROI from happy-sheet scores.

### Q86 ⭐ 🟡 How would you analyse delivery-partner attrition for a quick-commerce company when the workforce is mostly contract?
**Asked at:** commonly asked (no company-specific report found); quick-commerce case rounds exist at some firms but no matching question was found.
**What the interviewer is checking:** Redefining attrition for a loose, gig-style workforce and finding where people drop out.
**Say this in the interview:** "First I would define 'churned' as no deliveries for a set number of days, then look at survival by joining cohort, city and earnings."

**Clarify first:** What counts as active (at least one delivery in 14 days?). Are partners leaving the company or just pausing? What is the cost of replacing one (onboarding, kit)?
**Plan:**
1. Define active and churned, by agreement, and document the rule.
2. Cohort table: partners by joining week, share still active after 1, 4, 12 weeks.
3. Cut by city, shift, joining channel, earnings in the first 2 weeks, and order density.
4. Compare leavers and stayers on earnings per hour, waiting time between orders, penalties, app problems.
5. Check seasonality (festivals, monsoon, exam time).
**Method choice and why:** A retention curve by cohort is simple and handles the fact that many partners are still new. Later, a survival model.
**Pitfalls:** Using headcount-based attrition formula that ignores people dipping in and out; treating seasonal pauses as exits; averaging across cities with very different demand.
**Deliverable:** Retention curves, the top 2 or 3 differences between stayers and leavers, and a pilot idea (e.g. early-weeks earnings guarantee) with a measure.

**Likely follow-ups:** 1) *Compute a cost?* Replacement cost x leavers. 2) *Causes?* Correlation first; test with a pilot.
**Common mistakes / traps:** Applying a permanent-employee formula; ignoring reactivation.

### Q87 ⭐ 🟡 How would you analyse whether a team's overtime is a staffing problem or a process problem?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Separating "too little capacity" from "wasteful work", using patterns in the data.
**Say this in the interview:** "If overtime is spread all week and across the team, it points to too few people. If it clusters at certain days, steps or individuals, it points to a process bottleneck."

**Clarify first:** Which team, what period, is overtime paid or unpaid, what is the workload measure (tickets, orders, cases)?
**Plan:**
1. Overtime hours by week, day and person; compare with workload volume.
2. If overtime rises and falls with volume across everyone: capacity shortage.
3. If it is concentrated in a few people, a late stage, or month-end rushes: a process or handoff issue.
4. Look at rework, errors, waiting time for approvals, and manual steps.
5. Check vacancies, absence and attrition in the team, and the volume per person against a similar team.
**Method choice and why:** Simple charts of hours versus workload; a short conversation with the team to test the data story.
**Pitfalls:** Assuming overtime equals low staffing; missing unrecorded overtime; ignoring one-off projects.
**Deliverable:** A recommendation, hire, fix the process, or both, with the expected hours saved and how you would measure it afterwards.

**Likely follow-ups:** 1) *Both?* Fix the process first if cheap, then size the headcount. 2) *Cost?* Overtime premium versus a new hire's cost.
**Common mistakes / traps:** Recommending hiring from overtime alone.

### Q88 ⭐ 🟡 How would you analyse performance review calibration to see whether a department is rating too generously?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Comparing rating distributions fairly and not assuming leniency when performance may really differ.
**Say this in the interview:** "I would compare the department's rating distribution with the company's and with objective results, and look at differences by manager."

**Clarify first:** What is the rating scale and expected distribution (if any)? Do we have objective measures, targets achieved, to compare?
**Plan:**
1. Share of each rating in the department versus other departments and earlier years.
2. Average rating by manager (a manager rating everyone top is a signal).
3. Compare rating with objective output: if ratings are high but targets were missed, that supports leniency.
4. Check team size (small teams vary by chance) and role mix.
5. Check whether ratings drive bonuses, which can push generosity.
**Method choice and why:** Distribution tables and manager-level comparison first. A statistical test only if the claim needs it.
**Pitfalls:** Forcing the same distribution on every team; blaming a strong team; ignoring small sample; one year only.
**Deliverable:** A table by manager, a view on whether the gap is explained by performance, and a suggestion for the calibration meeting.

**Likely follow-ups:** 1) *Strong team?* Then objective results will support the ratings. 2) *Bias beyond leniency?* Check ratings by gender or tenure as well.
**Common mistakes / traps:** Assuming every department should look alike.

### Q89 ⭐ 🟡 How would you analyse web or app traffic data when 30 percent of events are missing due to a tracking bug?
**Asked at:** commonly asked (no company-specific report found); metric-and-RCA cases appear in e-commerce case guides (unverified).
**What the interviewer is checking:** Whether you size the damage, work out if the loss is random, and avoid reporting wrong levels.
**Say this in the interview:** "I would first find which events and which dates are missing and whether the loss is even across users; if it is, I can scale; if not, I report only on unaffected data and flag it."

**Clarify first:** Which events, which dates, which platforms? Is there a second source (server logs, orders table, payments) to compare with?
**Plan:**
1. Compare tracked events with a trusted source (orders in the database) to confirm the gap is about 30%.
2. Check whether the missing share is the same across app version, device, country, and hour.
3. If even: levels can be scaled up (divide by 0.70); ratios such as conversion stay roughly valid.
4. If uneven: report only on unaffected segments; trends are not safe.
5. Mark the affected dates on every chart; stop comparisons across the break.
6. Ask engineering for the fix date and whether events can be backfilled.
**Method choice and why:** Use the unaffected source as the anchor; correct only when the loss is proven random.
**Pitfalls:** Reporting a drop in traffic that is only the bug; scaling when loss hits one platform; comparing a pre-bug to post-bug period.
**Deliverable:** A note with affected period, estimated true level with a range, and what can and cannot be concluded.

**Likely follow-ups:** 1) *Can you fix history?* Only by estimate, and label it. 2) *Which metric is safest?* One from the transaction database.
**Common mistakes / traps:** Silently multiplying by 1.43; not telling stakeholders.

### Q90 ⭐ 🟡 How would you analyse a merger of two employee databases to produce a combined headcount report?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Matching records, removing duplicates, aligning definitions, and reconciling to totals.
**Say this in the interview:** "I would map both systems to one set of definitions, find people appearing in both, and reconcile the combined count to each source before reporting."

**Clarify first:** As of which date? Who counts as headcount (contractors, interns, notice period)? Is there a common employee ID?
**Plan:**
1. Profile each file: row counts, status values, duplicates, missing IDs.
2. Map fields (grade names, department codes, location, employment type) into a common list; keep a mapping table.
3. Match people: by ID if shared; else by name plus date of birth plus joining date, and list uncertain matches for review.
4. Resolve duplicates (a person on both payrolls) and choose which record wins by a stated rule.
5. Reconcile: A + B - overlaps = combined; compare with finance or payroll totals.
6. Log the exceptions and who approved them.
**Method choice and why:** Rule-based matching with manual review of the doubtful cases; fuzzy matching only for name spelling issues.
**Pitfalls:** Counting the same person twice; different definitions of "active"; losing history; matching on name alone.
**Deliverable:** Combined headcount by entity, department and type, a reconciliation page, and the mapping and exceptions list.

**Likely follow-ups:** 1) *Totals do not tie?* List the differences by cause. 2) *Which source wins?* The one that owns the field (payroll for pay, HRIS for job).
**Common mistakes / traps:** Stacking both files and counting rows.

### Q91 ⭐ 🟡 How would you analyse time-series data that includes holidays and a one-off event such as a strike?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Separating regular patterns from one-off shocks so the trend is not distorted.
**Say this in the interview:** "I would flag the holiday and strike dates, compare like with like (same weekday or same holiday last year), and report the trend with and without the one-off."

**Clarify first:** What is being measured, how far back is the data, what is the decision (forecast, performance review)? Exact dates and scope of the strike?
**Plan:**
1. Plot the series; mark holidays and the strike.
2. Compare against the same period last year and against a normal weekday baseline.
3. Add flag columns (holiday yes or no, strike yes or no) so they can be filtered or modelled.
4. Estimate the strike effect = expected value (from the usual pattern) minus the actual value; note rebound afterwards.
5. For trends, calculate with the strike period excluded and with it included; show both.
6. For forecasting, do not teach the model that the strike is normal.
**Method choice and why:** Year-on-year and flagged comparisons are enough for most business questions; seasonal decomposition or regression with flags if a forecast is needed.
**Pitfalls:** Moving holidays (festival dates shift); catching up after a strike that hides the real loss; deleting data instead of flagging.
**Deliverable:** A chart with annotations, an adjusted trend, and the estimated one-off impact with a range.

**Likely follow-ups:** 1) *Remove the strike?* Flag it, do not erase it. 2) *Only one year of data?* Say seasonality cannot be confirmed.
**Common mistakes / traps:** Comparing a holiday week to a normal week.

### Q92 ⭐ 🟡 How would you analyse a large dataset in Excel if it has about 800,000 rows and keeps crashing, and when would you move to another tool?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know the limits of the tool and the practical next step.
**Say this in the interview:** "Excel's sheet limit is about 1 million rows (from memory, unverified), so 800,000 rows fits but is heavy; I would first slim the file, then move to Power Query, Power Pivot, SQL or Python."

**Clarify first:** What is the question, how often will it recur, who needs to open the result? Are all columns needed?
**Plan:**
1. Remove unneeded columns and rows; save as .xlsx or .xlsb, not .xls.
2. Switch calculation to manual; replace heavy formulas (array and volatile ones, many VLOOKUPs) with values or one lookup.
3. Load via Power Query into the Data Model, and build a PivotTable from it instead of formulas on the sheet.
4. If it still struggles, aggregate in a database with SQL, or in Python (pandas), and bring only the summary into Excel.
5. Keep a copy of the raw file untouched.
**Method choice and why:** Stay in Excel while one-off and the Data Model works; move to SQL or Python when data grows, refreshes are frequent, joins are many, or the process must be repeatable.
**Pitfalls:** Filtering and copying huge ranges; opening the same file on a weak laptop; losing the original; no documentation of steps.
**Deliverable:** A summary workbook (small), the reproducible query or script, and a note on when it was last refreshed.

**Likely follow-ups:** 1) *Why Power Query?* It records the steps and handles large files better. 2) *More than 1 million rows?* Excel cannot hold them in a sheet; use the Data Model, a database or Python.
**Common mistakes / traps:** Buying a bigger computer rather than changing the method.

### Q93 ⭐ 🟡 How would you analyse the data to decide whether to open a new store location, given limited internal data?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Using proxies and outside data sensibly, and giving a conditional decision.
**Say this in the interview:** "I would find what makes my existing stores succeed, then check whether the new site has the same features, using outside data for anything I lack."

**Clarify first:** What does success mean (break-even in 18 months)? Investment and rent? Which formats and cities have we operated in?
**Plan:**
1. Rank current stores by sales per square foot and profit; find common traits (footfall, nearby offices, parking, income level).
2. Collect the same traits for the candidate site from outside sources: population in a 3 km catchment, competitors, footfall counts, rent (sources to be confirmed).
3. Use online orders and delivery pincodes from the area as a demand signal.
4. Make a simple forecast: expected sales from look-alike stores, minus costs; run low, base and high cases.
5. Find break-even sales and ask if it is plausible.
**Method choice and why:** Look-alike comparison and break-even is explainable; regression on only 8 stores would overfit.
**Pitfalls:** Cannibalising nearby own stores; survivor bias (closed stores missing); relying on one visit; trusting a landlord's footfall figure.
**Deliverable:** A go, no-go or pilot recommendation with the three cases, key risks and the signals to monitor in the first 3 months.

**Likely follow-ups:** 1) *Little data?* Be explicit about ranges and test with a smaller pop-up. 2) *Biggest risk?* Rent against uncertain sales.
**Common mistakes / traps:** False precision; ignoring cannibalisation.

### Q94 ⭐ 🟡 How would you check whether the sample in a customer panel is representative of the full customer base?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Comparing the sample with known population figures and knowing the cure for mismatch.
**Say this in the interview:** "I would compare the panel with the full customer base on the traits we know for both, such as age, city, spend and tenure, and weight the panel if it is lopsided."

**Clarify first:** How was the panel recruited (opt-in, random)? What do we know for all customers? What question will the panel answer?
**Plan:**
1. Choose comparison variables available for everyone: city, age band, product, tenure, spend, channel.
2. For each, compare the share in the panel with the share in the full base; mark gaps (for example over 5 percentage points).
3. Compare behaviour: average order value and purchase frequency in the panel versus base.
4. Check non-response: who was invited but did not join?
5. If gaps exist, reweight (post-stratification: give under-represented groups more weight) or restrict conclusions.
**Method choice and why:** Side-by-side tables first; a chi-square test only to show whether differences exceed chance; with a large sample, even small gaps look significant, so judge by size.
**Pitfalls:** Panels are often skewed to keen, heavy buyers; matching on a few traits while hidden ones differ; weighting small groups too heavily.
**Deliverable:** A representativeness table, a verdict, and weights or a note on what the panel can and cannot say.

**Likely follow-ups:** 1) *If it is not representative?* Weight, or use it for ideas, not for sizes. 2) *Can weights fix everything?* No, not hidden differences.
**Common mistakes / traps:** Assuming a large sample is automatically representative.

### Q95 ⭐ 🟡 How would you analyse support-chat transcripts and sales together to find reasons for lost deals?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Joining text and structured data, and tying themes to outcomes.
**Say this in the interview:** "I would link each deal to its chats, tag the chat reasons, and compare how often each theme appears in lost deals versus won deals."

**Clarify first:** What counts as lost? Is there a common customer or deal ID? Period and product? Who will use the answer (sales, product)?
**Plan:**
1. Join chats to deals by deal or account ID; check how many deals have no chat.
2. Read a sample of 100 or so chats and build a list of themes (pricing, missing feature, slow reply, competitor).
3. Tag all chats by theme (by keyword rules, then check an accuracy sample by hand).
4. Compare theme frequency in lost versus won deals, and by deal size and segment.
5. Add structured data: response time, discount, sales rep, stage lost at.
**Method choice and why:** Manual themes plus counts is clear and checkable; automated topic tools help at scale but need human review.
**Pitfalls:** Only deals with chats appear (selection bias); loss reasons the rep typed are often guesses; a theme common in both won and lost deals is not a reason; privacy of chats.
**Deliverable:** A ranked list of loss themes with the difference in rate, quotes, and 2 or 3 recommended fixes.

**Likely follow-ups:** 1) *Won deals mention price too?* Then price is not distinctive; compare rates. 2) *No chat link?* Match by email, with care for privacy.
**Common mistakes / traps:** Counting mentions without a won-deal comparison.

### Q96 ⭐ 🔴 How would you analyse customer survival (time until churn) when many customers are still active, and why can't you just average the tenure of those who left?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Understanding of "censoring": people still active have unfinished stories, and ignoring them biases results.
**Say this in the interview:** "Averaging only leavers understates how long customers stay, because long-staying customers have not left yet. I would use a survival curve (Kaplan-Meier), which counts active customers as 'still here at least this long'."

**Clarify first:** What counts as churn, and from which start date? Observation end date? Do customers differ by plan or acquisition channel?
**Plan:**
1. Build one row per customer: start date, end date if churned, otherwise the data cut-off date, and a flag (churned yes or no).
2. Tenure = end (or cut-off) minus start.
3. Build the survival curve: at each tenure, the share still active, counting only those still observed.
4. Read off the median tenure (time when 50% have left) and retention at 3, 6, 12 months.
5. Compare curves by segment.
**Method choice and why:** Tiny example (computed): 10 customers; 4 churned at months 2, 3, 4, 5 (average 3.5 months); 6 are still active after 12 months. The leaver average of 3.5 months wildly understates; counting everyone's observed time gives 8.6, still not a true average. The curve gives survival of 90% at month 2, 80% at 3, 70% at 4 and 60% at 5, and keeps going. Go further, to Cox regression, only if you need to compare many factors at once.
**Pitfalls:** Dropping active customers; treating them as churned; mixing cohorts of different ages; comparing a new cohort with an old one without matching tenure.
**Deliverable:** Survival curves by segment, the key retention points, and the plain message.

**Likely follow-ups:** 1) *What is censored?* A customer still active; we know only a minimum. 2) *Average of everyone's observed time?* Also biased; use the curve.
**Common mistakes / traps:** Averaging leavers' tenure; calling it churn when it is just newness.

### Q97 ⭐ 🔴 How would you analyse the effect of a retention bonus on attrition when only high performers received it?
**Asked at:** commonly asked (no company-specific report found); selection-bias themes are a differentiator.
**What the interviewer is checking:** Recognising that the bonus group differs from the rest, so a simple comparison is unfair.
**Say this in the interview:** "I cannot compare bonus recipients with everyone else, because they were already different. I would compare them with similar high performers who did not get it, or use the selection cut-off."

**Clarify first:** How were recipients picked (rating above a line, manager choice)? What was the bonus, when paid, what lock-in? Time window?
**Plan:**
1. Describe the groups: ratings, tenure, grade, pay, manager before the bonus.
2. Find a comparison group: high performers not paid (other units, earlier year, just below the cut-off).
3. Match on rating, tenure, grade, pay ratio, and compare leave rates in the next 12 months.
4. If a rating cut-off decided it, compare people just above and just below the line (they are almost alike).
5. Check pre-trends: did both groups have similar attrition before the bonus?
6. Estimate savings: avoided exits x replacement cost minus bonus cost.
**Method choice and why:** Matching and before-and-after comparison are explainable; the cut-off comparison is strongest if the rule was sharp.
**Pitfalls:** High performers leave less anyway, so a raw comparison flatters the bonus; people who stay until a lock-in ends and then leave; small numbers.
**Deliverable:** An estimated effect range with the key assumption stated, and a recommendation for any future rollout to be randomised or staged.

**Likely follow-ups:** 1) *No comparison group?* Present a before-and-after with cautions. 2) *Future design?* Stagger by team so comparison exists.
**Common mistakes / traps:** Comparing recipients with the whole company and claiming success.

### Q98 ⭐ 🔴 How would you analyse whether a recommendation on the dashboard actually changed behaviour, using only observational data?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Honest causal reasoning when no experiment exists.
**Say this in the interview:** "I would compare people who saw the recommendation with similar people who did not, and look at behaviour before and after, while saying clearly that without an experiment I can show a link, not proof."

**Clarify first:** What behaviour (acting on the alert, changing a decision)? Who saw it, and how did they get to see it? When did it launch?
**Plan:**
1. Define the behaviour metric and the time window.
2. Compare users before and after seeing the recommendation (their own history).
3. Compare with similar users who did not see it over the same dates ("difference in differences": change in the seen group minus change in the unseen group).
4. Check the groups were alike before: past usage, role, team.
5. Look for a dose pattern: more exposure, more change.
6. Rule out other changes at the same time.
**Method choice and why:** Before and after with a comparison group beats a raw comparison; more advanced matching only if the groups differ a lot.
**Pitfalls:** Keen users are the ones who open recommendations (self-selection); a trend already under way; coincident releases; claiming proof.
**Deliverable:** Effect estimate with a range, assumptions, and a proposal for a small randomised test (show to half) to confirm.

**Likely follow-ups:** 1) *Why not just compare viewers and non-viewers?* They differ to begin with. 2) *Can you prove it?* Only an experiment can.
**Common mistakes / traps:** Saying "caused" from observational data.

### Q99 ⭐ 🔴 How would you analyse a decline in a metric where several things changed in the same week (a price change, a release and a holiday)?
**Asked at:** commonly asked (no company-specific report found); metric-and-RCA cases are a common e-commerce round type (unverified).
**What the interviewer is checking:** Breaking an overlapping cause problem into parts you can separate, and admitting what you cannot.
**Say this in the interview:** "I would first break the drop by segment to see where it sits, because each change touches different people, and then use comparison groups; if the changes cannot be separated, I would say so and propose a staged test."

**Clarify first:** Which metric, how big is the drop, which dates? Exact times and scope of each change (all users or some)?
**Plan:**
1. Confirm it is real: data pipeline fine, definition unchanged.
2. Compare with the same holiday week last year to estimate the holiday effect.
3. Cut by who was exposed: price change by product or city, release by app version or platform, holiday by region.
4. Look at timing: hour or day when the drop began against each change's go-live time.
5. Use unaffected segments (old app version, products with no price change) as the control.
6. Break the metric into steps (traffic, conversion, order value) to see which step moved.
**Method choice and why:** Segment cuts and controls first; a regression with all three flags only if enough data, and it fails when changes overlap perfectly.
**Pitfalls:** Blaming the last thing shipped; ignoring that effects may stack; averaging away a segment that fell hard.
**Deliverable:** A split of the drop (rough shares with ranges), what remains unknown, and a next step such as rolling back one change in a small segment.

**Likely follow-ups:** 1) *Cannot separate them?* Roll back or stage them. 2) *Which first?* The cheapest to reverse.
**Common mistakes / traps:** Naming one cause without segment evidence.

### Q100 ⭐ 🔴 How would you analyse pay differences between genders at a company so that the result is defensible to both HR and legal?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic.
**What the interviewer is checking:** Distinguishing raw gaps from like-for-like gaps, careful method, and handling sensitive findings properly.
**Say this in the interview:** "I would show the raw gap and then the gap among comparable people, same role, level, location and experience, document every choice, and run it under legal guidance."

**Clarify first:** What is the purpose (compliance review, internal audit)? Does legal want it done under privilege (confirm with them)? Which pay elements (base, bonus, stock)? Which date?
**Plan:**
1. Data: base, bonus, total pay, job family, grade, location, tenure, performance, hours (convert part-time to full-time equivalent).
2. Raw gap: (men's median - women's median) / men's median. State mean and median.
3. Like-for-like: compare within the same grade and role; or regress log pay on gender plus legitimate factors (grade, tenure, location, performance) and read the gender coefficient.
4. Check the factors are not themselves biased (are women assigned lower grades or rated lower?).
5. Test statistical and practical significance; list outliers and individual cases.
6. Document methods and decisions; limit the access to results.
**Method choice and why:** Simple grade-level comparison is explainable to everyone; regression adds control. Use both and show they agree.
**Pitfalls:** Controlling for factors that are part of the problem; small groups; using only the mean; leaking individual pay; stating a legal conclusion yourself.
**Deliverable:** Raw and adjusted gaps with ranges, drivers, individual cases for review, and a remediation cost estimate; legal reviews the conclusions.

**Likely follow-ups:** 1) *Raw versus adjusted gap?* Raw shows overall pattern; adjusted shows like-for-like. 2) *If you find a gap?* Report to the owners, do not fix quietly.
**Common mistakes / traps:** Quoting one gap number; adjusting away the gap with questionable controls.

### Q101 ⭐ 🔴 How would you analyse the relationship between employee engagement scores and team performance without over-claiming?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Correlation is not cause, with sensible checks on direction and confounding.
**Say this in the interview:** "I would measure how strongly they move together, test whether it holds after allowing for team size, role and manager, and describe it as an association, not proof that engagement raises performance."

**Clarify first:** How is team performance measured (targets, output, ratings)? One survey wave or several? Level of analysis: team (not individual, to protect anonymity)?
**Plan:**
1. Build one row per team: engagement score, response rate, performance, size, function, manager tenure.
2. Plot engagement against performance; compute the correlation and its range.
3. Compare within similar functions, not the whole company (sales and support differ).
4. Check the timing: does engagement this year predict performance next year, or the reverse?
5. Drop teams with few responses; show results with and without them.
6. If data allows, check change in engagement against change in performance.
**Method choice and why:** Scatter plot and correlation first, then a simple regression with controls. Panel data over time helps with direction.
**Pitfalls:** Good performance may raise engagement (reverse cause); a good manager drives both (confounder); a few teams drive the pattern; correlation across teams applied to an individual.
**Deliverable:** A chart and a sentence such as "teams with higher engagement tend to perform better, an association of moderate strength, direction unknown", plus a pilot idea.

**Likely follow-ups:** 1) *Does engagement cause performance?* Not shown; needs timing and a test. 2) *Small teams?* Scores are noisy, so be careful.
**Common mistakes / traps:** Saying "raising engagement will raise performance"; ignoring response rates.

