# Book 8 — Scenario-Based & Data Interpretation | Part 6: Data Interpretation from Given Tables and Charts 🟡

**Target:** 80 questions | **Actual:** 92 questions
**Scope:** Analyst-style interpretation of given tables and charts (read the exhibit, state the insight, name the caveats, propose the next step), with inline exercise data where a single figure can be checked; calculation-drill aptitude is in Book 6 Part 8.

### Q1 ⭐⭐⭐ 🟢 You are shown a table or chart you have never seen before, in an interview or on the job. What steps do you follow before you state an insight?
**Asked at:** commonly asked (no company-specific report found); prep sites list "read the title, units and axes first" as a standard routine (unverified).
**What the interviewer is checking:** That you read the exhibit carefully and tie it to a decision before speaking.
**Say this in the interview:** "I slow down. I read the title, units, period and definitions, check what is being compared, then look for the biggest movement, and only then say what it means for the decision."

**Clarify first:** What question is this exhibit meant to answer, and who will act on it? If I cannot ask, I state my assumption aloud.
**Plan:**
1. Read the labels: title, units (rupees, lakh, crore, percent), period, filters, source and date of the data.
2. Check the definitions: is it a count, a rate or an average, and what is the denominator?
3. Check the scale: where does the axis start, are the intervals even, is it a total or per head?
4. Do a sanity check: do parts add to totals, are the percentages plausible, are there blanks or outliers?
5. Find the headline: the largest, smallest or most changed item, and the trend.
6. Compare like with like: against last period, target or benchmark, and look at mix (a total can hide opposite moves).
7. Say the insight in one sentence: what moved, by how much, the likely reason, and what I would do next.
**Method choice and why:** Simple arithmetic first (differences, shares, rates). I only go further (tests, models) if the decision needs it.
**Pitfalls:** Jumping to a cause from one view; confusing percent with percentage points; reading blank or incomplete cells as zero; trusting a truncated axis.
**Deliverable:** A one-line headline, two supporting numbers, one caveat and one next step.
**Likely follow-ups:** 1) *What if there is no time?* Do steps 1, 2 and 5 aloud, and flag what you have not checked. 2) *What if the numbers do not add up?* Say so first; it is a finding.
**Common mistakes / traps:** Describing the chart instead of interpreting it; skipping units; giving an insight with no next step.

### Q2 ⭐⭐⭐ 🟢 A stakeholder says "cancellations went up 1%" when the cancellation rate moved from 2% to 3%. How do you restate this, and why does the wording matter?
**Asked at:** commonly asked (no company-specific report found); percent versus percentage point is a recurring prep-site theme (unverified).
**What the interviewer is checking:** That you separate a percentage-point change from a relative percent change.
**Say this in the interview:** "The rate rose by 1 percentage point, from 2% to 3%. That is a 50% relative increase, so cancellations are one and a half times what they were."

**Explain simply:**
- Percentage point (pp) is the plain gap between two percentages: 3% minus 2% = 1 pp.
- Relative change is the gap divided by the starting value: 1 / 2 = 50%.
- "Up 1%" could be heard as 2.00% to 2.02%, which is trivial. The real move is large.

**Worked example (computed):** Take 100,000 bookings. At 2%, there are 2,000 cancellations; at 3%, there are 3,000. That is 1,000 extra cancellations, +50%.
**Restated sentence:** "Cancellation rate rose from 2% to 3% (up 1 percentage point, or 50% in relative terms), which is about 1,000 more cancellations per 100,000 bookings."
**Why wording matters:** Executives size problems by the words. Under-stating hides a real issue; over-stating ("50% jump!") without the base causes panic. Give both the pp and the relative change, plus the count.
**Practice step:** Rewrite any three percent changes from your own dashboards in pp and relative terms.
**Likely follow-ups:** 1) *If it then fell from 3% to 2%?* Down 1 pp, but down 33.3% relative (1/3), not 50%. The relative change is not symmetric. 2) *Which do you report?* Both, with the count.
**Common mistakes / traps:** Saying "1% increase"; quoting the relative change with no base; forgetting the count of cancellations.

### Q3 ⭐⭐⭐ 🟢 A chart of monthly revenue and a chart of monthly profit are shown to you. Revenue rose from 500 to 550 (exercise figures, in lakh) while gross margin fell from 30% to 24%. What happened to gross profit, and what do you say to the sales head?
**Asked at:** commonly asked (no company-specific report found); "sales up, margin down" is a listed prompt type in data-interpretation guides (unverified).
**What the interviewer is checking:** That you convert margin percentages into rupees and do not celebrate revenue alone.
**Say this in the interview:** "Gross profit actually fell from 150 to 132 lakh, down 18 lakh or 12%, even though revenue grew 10%."

**What the data shows:** Revenue up, margin down, and the margin fall is bigger than the revenue gain.
**Working:**
1. Gross profit before: 500 x 30% = 150 lakh.
2. Gross profit after: 550 x 24% = 132 lakh.
3. Change: 132 - 150 = -18 lakh, which is -12.0% (revenue itself +10.0%).
4. Split: extra revenue at the old margin adds 50 x 30% = +15; the margin fall of 6 percentage points on 550 costs 550 x 6% = -33. Net: +15 - 33 = -18.
**Result:** Gross profit fell 18 lakh (12%); margin fell 6 percentage points (not 6%).
**Caveats / what else I would check:** Why margin fell: discounts, a shift towards low-margin products, higher input or delivery cost, or returns. Whether the period has one-offs.
**Next step / recommendation:** To the sales head: "The extra 50 lakh of sales did not pay for itself; we lost about 33 lakh of profit to lower margin. Let us look at discounts and product mix, and track gross profit, not only revenue, in the sales review."
**Likely follow-ups:** 1) *What revenue would restore 150?* 150 / 24% = 625 lakh, a 25% rise. 2) *Is a margin drop always bad?* No, if it buys valuable customers; check retention.
**Common mistakes / traps:** Calling profit "up because revenue is up"; saying margin fell "6%"; blaming sales without checking costs.

### Q4 ⭐⭐⭐ 🟢 What is the difference between an observation and an insight when you present a table, and can you give one example of each from a sales table?
**Asked at:** commonly asked (no company-specific report found); consulting prep sites stress "so what" over description (unverified).
**What the interviewer is checking:** That you move from describing numbers to explaining why they matter and what to do.
**Say this in the interview:** "An observation says what the numbers show. An insight says why it matters and what we should do about it."

**Explain simply:**
- Observation: a fact you can read off the table.
- Insight: a fact plus a reason or comparison, the business meaning, and an action.

**Example (a regional sales table, Q1 to Q2, in lakh: North 120 to 132, South 80 to 84, East 60 to 72, West 40 to 34; figures computed in Q6):**
- Observation: "North sales rose from 120 to 132 lakh."
- Insight: "Total sales grew 7.3%, and North and East each added 12 lakh. But East grew 20% on a smaller base, while West fell 15%. Growth is coming from East, and West needs a review, so I would check East's capacity to keep growing and what happened in West."

**Test:** if the listener can ask "so what?", you only gave an observation.
**Practice step:** Take any table and write one observation, then add a comparison, a reason to test, and an action.
**Likely follow-ups:** 1) *Can an insight be wrong?* Yes, which is why you state the evidence and what you would check. 2) *How many insights per slide?* One main message.
**Common mistakes / traps:** Reading out the table; giving an insight with no number behind it; claiming a cause the data cannot show.

### Q5 ⭐⭐⭐ 🟢 Two teams' average ticket-handling times are shown below. A manager says the overall average is 6.5 minutes. Is that right, and what is the correct figure?
| Team | Avg handle time (min) | Tickets closed |
|---|---|---|
| A | 5 | 100 |
| B | 8 | 400 |

**Asked at:** commonly asked (no company-specific report found); weighted-average questions are a standard theme (unverified).
**What the interviewer is checking:** That you weight averages by volume.
**Say this in the interview:** "6.5 is the simple average of 5 and 8, but Team B closed four times as many tickets, so the correct overall figure is 7.4 minutes."

**What the data shows:** Team B is slower but handles 80% of the tickets, so it pulls the overall average towards 8.
**Working:**
1. Total minutes: A = 5 x 100 = 500; B = 8 x 400 = 3,200; total 3,700.
2. Total tickets: 100 + 400 = 500.
3. Weighted average: 3,700 / 500 = 7.4 minutes.
4. The manager's 6.5 = (5 + 8) / 2 treats both teams as equal in size.
**Result:** 7.4 minutes (the manager's 6.5 is understated by 0.9 minutes).
**Caveats / what else I would check:** Whether ticket types differ in difficulty (B may get harder tickets); whether the average is hiding a long tail (check the median and the 90th percentile); whether the two teams count handle time the same way.
**Next step / recommendation:** Report 7.4, and show tickets alongside the average. If the goal is faster handling, check B's mix before judging the team.
**Likely follow-ups:** 1) *When would the simple average be right?* Only if both teams closed the same number of tickets. 2) *Which team is better?* Not answerable from averages alone; compare like-for-like ticket types.
**Common mistakes / traps:** Averaging averages; ignoring volumes; drawing conclusions about team quality from raw averages.

### Q6 ⭐⭐⭐ 🟢 The table below shows revenue by region for two quarters (exercise data, in lakh). Which region contributed most to the total growth, and what is the overall growth percentage?
| Region | Q1 | Q2 |
|---|---|---|
| North | 120 | 132 |
| South | 80 | 84 |
| East | 60 | 72 |
| West | 40 | 34 |

**Asked at:** commonly asked (no company-specific report found); contribution-to-growth questions are common in data-interpretation guides (unverified).
**What the interviewer is checking:** That you separate contribution (absolute change) from growth rate.
**Say this in the interview:** "Overall growth is 7.3%. North and East tie as the largest contributors at +12 lakh each, but East grew 20% against North's 10%, and West dropped."

**What the data shows:** Three regions grew and West shrank. The question has a tie on the biggest contributor.
**Working:**
1. Totals: Q1 = 120 + 80 + 60 + 40 = 300; Q2 = 132 + 84 + 72 + 34 = 322.
2. Overall growth: (322 - 300) / 300 = 7.33%.
3. Change by region: North +12, South +4, East +12, West -6 (these add to +22).
4. Share of net growth: North 54.5%, East 54.5%, South 18.2%, West -27.3% (they add to 100%).
5. Region growth rates: North +10%, South +5%, East +20%, West -15%.
**Result:** Overall growth 7.3% (+22 lakh). North and East tie at +12 lakh each, so there is no single winner on contribution. The tie is in the data, not a mistake.
**Caveats / what else I would check:** Two quarters only (seasonality); whether East's rise is one big deal; West's fall reason (lost customer, stock-out, region reorganisation); whether regions are defined the same in both quarters.
**Next step / recommendation:** Say "North and East drove the growth; East is the faster engine, West is the drag". Investigate West and confirm East's growth is repeatable.
**Likely follow-ups:** 1) *Why do shares exceed 100%?* Because West's -27% offsets; the positive shares add up to more than 100%. 2) *Which region would you invest in?* Needs margin and potential, not only growth.
**Common mistakes / traps:** Confusing biggest growth rate with biggest contribution; ignoring the negative region; averaging the four growth rates (which gives 5%, not 7.3%).

### Q7 ⭐⭐⭐ 🟢 The attrition table below is from an HRIS export (exercise data). Which department has the highest attrition rate, which has the highest number of leavers, and what would you tell the HR head?
| Department | Average headcount | Leavers (year) |
|---|---|---|
| Engineering | 400 | 36 |
| Sales | 150 | 24 |
| Support | 250 | 30 |
| HR | 40 | 2 |

**Asked at:** commonly asked (no company-specific report found); HR metrics such as attrition appear as gap-fill HR exhibits in this part (judgement).
**What the interviewer is checking:** That you use a rate with a denominator, not raw counts.
**Say this in the interview:** "Sales has the highest rate at 16%, while Engineering has the most leavers (36) but a rate of only 9%."

**What the data shows:** Counts and rates point to different departments.
**Working:**
1. Attrition rate = leavers / average headcount: Engineering 36 / 400 = 9.0%; Sales 24 / 150 = 16.0%; Support 30 / 250 = 12.0%; HR 2 / 40 = 5.0%.
2. Company: headcount 840, leavers 92, rate 92 / 840 = 10.95%, about 11.0%.
3. Highest count: Engineering (36). Highest rate: Sales (16.0%).
**Result:** Highest rate Sales 16.0%; highest leavers Engineering 36; company rate about 11.0% (annual, on average headcount).
**Caveats / what else I would check:** Voluntary versus involuntary exits (the table does not say); regretted losses (high performers); tenure of leavers (early exits point to hiring or onboarding); small numbers in HR (2 leavers); whether Sales has a normal seasonal churn; benchmarks (confirm with HR).
**Next step / recommendation:** Tell the HR head: "Sales and Support are above the company rate, so those are the priority. I would split leavers by tenure, manager and reason, and check regretted exits, before proposing an action. Engineering's count is large because the team is large."
**Likely follow-ups:** 1) *Why use average headcount?* Headcount changes through the year; the average reflects the exposure. 2) *Is 16% bad?* Depends on the industry and past years; compare with the department's own trend.
**Common mistakes / traps:** Ranking by leaver counts; ignoring voluntary versus involuntary; drawing conclusions from HR's 2 leavers.

### Q8 ⭐⭐⭐ 🟢 A checkout funnel for one week is shown below (exercise data). Compute the step-to-step conversion rates and the overall conversion, and say which step you would investigate first.
| Step | Sessions |
|---|---|
| Product page view | 50,000 |
| Add to cart | 6,000 |
| Checkout started | 2,400 |
| Payment success | 1,800 |

**Asked at:** commonly asked (no company-specific report found); funnel reading is a recurring prep-site theme (unverified).
**What the interviewer is checking:** That you compute step rates, find the leak and prioritise it sensibly.
**Say this in the interview:** "Overall conversion is 3.6%. The step with the biggest loss of buyers who already showed intent is cart to checkout at 40%, so I would look there first."

**What the data shows:** Each step loses people, and the biggest drop is at the top, which is normal for browsing.
**Working:**
1. Page view to cart: 6,000 / 50,000 = 12.0%.
2. Cart to checkout: 2,400 / 6,000 = 40.0% (3,600 lost).
3. Checkout to payment: 1,800 / 2,400 = 75.0% (600 lost).
4. Overall: 1,800 / 50,000 = 3.6%.
**Result:** 12.0%, 40.0%, 75.0%; overall 3.6%.
**Caveats / what else I would check:** One week gives no benchmark: compare with prior weeks and by device, source and new versus returning visitors. Check whether steps count sessions or users, and tracking gaps.
**Next step / recommendation:** Start with cart to checkout (3,600 high-intent sessions lost: shipping fee shown late, forced login, price surprises). Then payment failures (600 lost): gateway errors, UPI or card failures, which are often easy to fix. Measure the change in step rate after each fix.
**Likely follow-ups:** 1) *Why not page to cart, the biggest loss?* Many visitors only browse; the gain per fix is smaller. I would still check by source. 2) *What is a good rate?* Benchmarks vary; I would not quote one without data.
**Common mistakes / traps:** Quoting only the overall rate; assuming the biggest absolute drop is the problem; treating one week as a trend.

### Q9 ⭐⭐⭐ 🟢 A salary export for a nine-person team is shown below (in lakh per year, exercise data). Compute the mean and the median, and say which one you would report to leadership and why.
Salaries: 6, 6, 7, 7, 8, 8, 9, 10, 60
**Asked at:** commonly asked (no company-specific report found); mean versus median is a standard theme (unverified).
**What the interviewer is checking:** That you recognise skew and outliers and choose the fitting measure.
**Say this in the interview:** "The mean is 13.4 lakh but the median is 8 lakh; one salary of 60 drags the mean up, so I would report the median and mention the outlier."

**What the data shows:** Eight people earn 6 to 10 lakh; one earns 60.
**Working:**
1. Sum = 6 + 6 + 7 + 7 + 8 + 8 + 9 + 10 + 60 = 121; mean = 121 / 9 = 13.44 lakh.
2. Sorted, the middle (5th) value of 9 is 8; median = 8 lakh.
3. Mean without the 60: 61 / 8 = 7.63 lakh.
**Result:** Mean 13.4 lakh; median 8.0 lakh (a typical employee earns about 8).
**Caveats / what else I would check:** Is the 60 correct (a typo, a leader, a bonus included)? Are all salaries on the same basis (fixed versus total pay)? Nine people is a small group; are roles comparable?
**Next step / recommendation:** Report the median as "typical", show the range (6 to 60), and footnote the outlier. If a payroll budget is needed, the total (121) matters, not the median.
**Likely follow-ups:** 1) *When would you report the mean?* For totals and budgets, or when the data is not skewed. 2) *Should you delete the outlier?* No, explain it; remove only if it is an error.
**Common mistakes / traps:** Reporting the mean of skewed data; silently dropping the outlier; not noting the sample size.

### Q10 ⭐⭐⭐ 🟢 You see a bar chart whose y-axis starts at 90 and shows two bars at 92 and 95. The title says "Customer satisfaction jumped". What is wrong with how this is presented, and how would you redraw or reword it?
**Asked at:** commonly asked (no company-specific report found); misleading axes are a recurring theme in chart questions (unverified).
**What the interviewer is checking:** That you spot visual exaggeration and propose an honest alternative.
**Say this in the interview:** "A bar chart should start at zero. With the axis at 90, a 3-point gain looks like the second bar is 2.5 times taller. In truth it is a 3.3% rise."

**Explain simply:**
- Bar length encodes the value. Cutting the axis at 90 makes the bars show 2 and 5 units: 5 / 2 = 2.5 times taller, while 95 / 92 = only 1.03 times (up 3.3%).
- "Jumped" is a claim with no evidence; the title should state the fact.

**How I would fix it:**
1. Start the bars at 0, or use a dot or line chart where a non-zero axis is acceptable, with labels showing 92 and 95.
2. Reword: "Customer satisfaction rose 3 points, from 92 to 95."
3. Add the sample size and the margin of error: with a few hundred responses, 3 points may be within noise.
4. Say what the score is (CSAT percent, scale out of 100) and the period.
**Practice step:** Redraw a truncated chart of your own from zero and see whether the story still holds.
**Likely follow-ups:** 1) *Is a truncated axis ever fine?* For lines or dot plots where the change matters, yes, if labelled clearly. 2) *Is 3 points big?* Depends on the scale's usual movement and the sample size.
**Common mistakes / traps:** Accepting "jumped" without a base; only fixing the axis and leaving the claim; ignoring sampling noise.

### Q11 ⭐⭐⭐ 🟢 A dashboard card shows "Sales: 1.2 crore, green arrow up". What context do you need before you can say whether this is good news?
**Asked at:** commonly asked (no company-specific report found); KPI card context is a standard dashboard-review prompt (unverified).
**What the interviewer is checking:** That you ask what the arrow compares with and whether the number is relevant to the decision.
**Say this in the interview:** "I would ask: up compared with what, over what period, against what target, and what is inside the 1.2 crore?"

**First, clarify / contain:** I make no claim yet. A green arrow shows direction, not size or quality.
**What I would check, in order:**
1. Comparison base: last day, last month, the same period last year, or a target? Is the period complete or month-to-date?
2. Size of the move: up 0.5% or 20%? What threshold turns the arrow green?
3. Definition: revenue, bookings or invoiced; gross or net of tax, returns and discounts?
4. Target or plan: is 1.2 crore above or below it?
5. Mix: volume, price, one large order, or one region, versus broad growth?
6. Profit and quality: margin, returns, collections, repeat customers.
7. Data freshness: time of last refresh.
**If I find...:** the arrow is against a weak base or a part-month, it is not good news yet; if it is above target with healthy margin and broad growth, it is.
**What I would tell the stakeholder:** "Sales are 1.2 crore, up against [base]. Before calling it good news, I need the target, the period and the margin. I will confirm by [time]."
**Prevent it next time:** Add the comparison, target and refresh time on every card, and a metric dictionary link.
**Likely follow-ups:** 1) *What if no target exists?* Use the previous period and last year, and flag the gap. 2) *Is a red arrow always bad?* No, same logic applies.
**Common mistakes / traps:** Treating colour as the verdict; ignoring definitions; looking at revenue without margin.

### Q12 ⭐⭐⭐ 🟢 A scatter chart shows that employees with more training hours have higher performance ratings (correlation about 0.6 in the exercise data). A manager says training causes better performance. How do you respond?
**Asked at:** commonly asked (no company-specific report found); correlation versus causation is a standard theme (unverified).
**What the interviewer is checking:** That you respect the manager's view but explain why the data alone does not prove cause.
**Say this in the interview:** "There is a moderate link, but training and performance may both be driven by something else, or good performers may simply get more training. I would test it before claiming cause."

**Explain simply:**
- A correlation of 0.6 means the two move together; squared, it is 0.36, so about 36% of the variation in ratings lines up with training hours in a straight-line sense. 64% is something else.
- Possible explanations: (1) training helps; (2) reverse direction, since managers send high performers to training; (3) a third factor, such as motivation, role or tenure, drives both; (4) chance or a few outliers on a small sample.

**What I would do:**
1. Look at the chart for outliers and subgroups (roles, tenure).
2. Compare ratings before and after training for the same people.
3. Compare trained versus similar untrained people (a matched comparison).
4. If possible, run a pilot where who gets training is randomly chosen.
**What I would tell the manager:** "The data is encouraging and consistent with training helping. Before we expand the budget, let us check the before-and-after ratings of the same people."
**Likely follow-ups:** 1) *Does 0.6 mean strong?* Moderate; the meaning depends on the context. 2) *Can we ever prove cause?* Randomised trials come closest; otherwise careful comparisons.
**Common mistakes / traps:** Saying "correlation is not causation" and stopping; ignoring reverse cause; treating 0.6 as 60%.

### Q13 ⭐⭐⭐ 🟢 You are given a monthly attendance table with one column of absentee percentages for each weekday, and Monday and Friday are visibly higher. What caveats do you state before recommending a policy change?
**Asked at:** commonly asked (no company-specific report found); HR attendance exhibits are a gap-fill in this part (judgement).
**What the interviewer is checking:** That you slow down on an HR pattern that affects people, and state limits clearly.
**Say this in the interview:** "A Monday and Friday pattern is a lead, not a verdict. Before any policy, I would check definitions, how many weeks the data covers, planned leave and who is behind the pattern."

**First, clarify / contain:** Ask what counts as absent (unplanned, all leave, half-days?), the denominator (scheduled staff), and what decision the policy is for. No recommendation yet.
**What I would check, in order:**
1. One month gives only four or five of each weekday, so I would get 6 to 12 months to see if the pattern is stable.
2. Separate planned leave and holidays from unplanned absence; Monday and Friday sit next to weekends, so planned leave and long weekends naturally cluster there.
3. Check the calendar effect: public holidays, festivals, month-end and payday.
4. Is it everyone, or a few people, teams, shifts or locations? A few frequent absentees can create the whole pattern.
5. Look at the size: how many extra absences per Monday, in headcount, not just percent?
6. Check data quality: late leave entry, regularisation, system outages.
**If I find...:** a spread-out pattern, a general policy discussion (flexibility, workload) fits; a pattern in a few people or teams, then a targeted conversation or a manager review; mostly planned leave, no policy change.
**What I would tell the stakeholder:** "Mondays and Fridays are higher in this month's data. I cannot yet say it is misuse. I need more months and the leave-type split. I will confirm by [date]."
**Prevent it next time:** Standardise absence definitions and keep a monthly dashboard by leave type, with a weekday and holiday calendar.
**Likely follow-ups:** 1) *Would you tighten leave rules?* Not before knowing the cause. 2) *What privacy care?* Report in aggregate; avoid naming individuals, and confirm rules with HR or legal.
**Common mistakes / traps:** Reading a pattern as misuse; ignoring planned leave and holidays; recommending a policy from one month.

### Q14 ⭐⭐⭐ 🟢 The retention table below is by signup month (exercise data). Are newer cohorts retaining better, and which cells would you not read yet?
| Cohort | Size | M1 | M2 | M3 |
|---|---|---|---|---|
| Jan | 1,000 | 40% | 30% | 28% |
| Feb | 1,200 | 45% | 34% | - |
| Mar | 900 | 52% | - | - |

**Asked at:** commonly asked (no company-specific report found); cohort retention tables with immature cells are a listed theme (unverified).
**What the interviewer is checking:** That you compare cohorts at the same age and treat blanks as not yet observed.
**Say this in the interview:** "Yes, M1 retention rises 40%, 45%, 52%, and M2 is better for Feb than Jan. But the blank cells are not zero, they are not observed yet, and I would not compare cohorts at different ages."

**What the data shows:** Each newer cohort retains more at month 1; the later months are only available for older cohorts.
**Working:**
1. Compare at the same age. M1: Jan 40%, Feb 45%, Mar 52%. M2: Jan 30%, Feb 34% (Mar not available).
2. In users (size x rate): Jan M1 = 400, M2 = 300, M3 = 280; Feb M1 = 540, M2 = 408; Mar M1 = 468.
3. Decay after month 1, M2 as a share of M1: Jan 30 / 40 = 75.0%; Feb 34 / 45 = 75.6%. So the improvement is at M1; the pattern after M1 looks about the same.
4. Jan M2 to M3 drop: 2 points (30% to 28%), so the curve flattens.
**Result:** Yes for M1 (up 12 points from Jan to Mar) and M2 (up 4 points from Jan to Feb); the gain looks front-loaded.
**Caveats / what else I would check:** Cells I would not read: Feb M3, Mar M2 and M3 (not yet happened), and Mar M1 if the month window is not complete. Compare M3 only for Jan. Check cohort mix: a campaign or channel shift could lift M1; check if retention means "any activity" or "purchase"; sizes differ (900 to 1,200).
**Next step / recommendation:** Wait for the cells to fill. Meanwhile ask what changed (onboarding, pricing, channel) in Feb and Mar and test whether M2 and M3 follow M1.
**Likely follow-ups:** 1) *Can you predict Mar M3?* Roughly, using the earlier cohorts' decay, but flag it as an estimate. 2) *Why do sizes matter?* Smaller cohorts have noisier rates.
**Common mistakes / traps:** Reading blanks as zero; comparing M1 of one cohort with M3 of another; ignoring that the cohort mix changed.

### Q15 ⭐⭐⭐ 🟢 Training completion by department is shown below (exercise data). Compute the company-wide completion rate and say why it differs from the simple average of the three percentages.
| Department | Employees | Completed |
|---|---|---|
| Sales | 300 | 150 |
| Tech | 100 | 90 |
| Ops | 100 | 70 |

**Asked at:** commonly asked (no company-specific report found); weighted rates are a standard theme (unverified).
**What the interviewer is checking:** That you compute a pooled rate from totals, not by averaging rates.
**Say this in the interview:** "The company-wide rate is 62%, not 70%. Sales is 60% of the people and has the lowest completion, so it pulls the overall down."

**What the data shows:** Tech does well, Sales does poorly, and Sales is the biggest group.
**Working:**
1. Department rates: Sales 150 / 300 = 50%; Tech 90 / 100 = 90%; Ops 70 / 100 = 70%.
2. Company: completed 150 + 90 + 70 = 310; employees 500; rate = 310 / 500 = 62.0%.
3. Simple average of the three rates: (50 + 90 + 70) / 3 = 70.0%.
4. The gap: the simple average gives each department equal weight; Sales has 300 of 500 employees (60%) and a 50% rate.
**Result:** Company-wide completion 62.0%, 8 percentage points below the simple average of 70.0%.
**Caveats / what else I would check:** Whether the training is mandatory, and the deadline; why Sales is low (field travel, targets, access); whether "completed" is defined consistently; whether new joiners are in the denominator.
**Next step / recommendation:** Report 62% as the company figure, with the three department rates. Target Sales: 90 more completions would bring Sales to 80%; reaching 90% would need 120 more (270 completions).
**Likely follow-ups:** 1) *When would both numbers match?* When every department is the same size. 2) *Which figure goes to the board?* The pooled one.
**Common mistakes / traps:** Averaging percentages; forgetting the denominator; not showing the group sizes.

### Q16 ⭐⭐⭐ 🟡 The hiring-funnel table below is split by source (exercise data). Which source is best, and does your answer change if you look at offer acceptance or cost per join instead of volume?
| Source | Applicants | Interviewed | Offers | Joined | Cost (Rs thousand) |
|---|---|---|---|---|---|
| Job portal | 2,000 | 200 | 40 | 24 | 480 |
| Referral | 150 | 60 | 24 | 21 | 105 |
| Agency | 300 | 90 | 30 | 18 | 540 |

**Asked at:** commonly asked (no company-specific report found); hiring-funnel metrics are a gap-fill HR exhibit in this part (judgement).
**What the interviewer is checking:** That "best" depends on the metric, and you can name the trade-off.
**Say this in the interview:** "On volume the job portal wins with 24 joins, but the referral source is best on quality and cost: 87.5% offer acceptance and Rs 5 thousand per join, against Rs 20 thousand for the portal and Rs 30 thousand for the agency."

**What the data shows:** Different sources win on different metrics.
**Working:**
1. Joined: portal 24, referral 21, agency 18 (total 63).
2. Interview to offer: portal 40 / 200 = 20%; referral 24 / 60 = 40%; agency 30 / 90 = 33.3%.
3. Offer acceptance (joined / offers): portal 24 / 40 = 60%; referral 21 / 24 = 87.5%; agency 18 / 30 = 60%.
4. Applicant to join: portal 1.2%; referral 14.0%; agency 6.0%.
5. Cost per join (Rs thousand): portal 480 / 24 = 20; referral 105 / 21 = 5; agency 540 / 18 = 30. Overall: 1,125 / 63 = 17.9.
**Result:** Volume: portal. Acceptance, conversion and cost per join: referral. Agency is the costliest per join.
**Caveats / what else I would check:** Referral supply is limited (only 150 applicants), so it cannot replace the portal; quality after joining (90-day exits, performance), time to hire, role mix across sources, fairness (referrals can narrow diversity), and whether "cost" includes referral bonuses and recruiter time.
**Next step / recommendation:** Grow referrals (incentives, easy submission), keep the portal for volume, and review the agency for hard-to-fill roles only. Track 90-day retention by source.
**Likely follow-ups:** 1) *Why is offer acceptance lower for portal and agency hires (60% each, against 87.5%)?* Possibly weaker fit, slower process or competing offers; ask candidates. 2) *Would you stop the agency?* Not without checking which roles it fills.
**Common mistakes / traps:** Picking by volume only; comparing sources with different role mixes; ignoring post-joining quality.

### Q17 ⭐⭐⭐ 🟡 The A/B result below is for a new checkout button (exercise data). Compute the relative lift, and say whether you would recommend shipping on this evidence alone.
| Variant | Visitors | Conversions |
|---|---|---|
| Control | 10,000 | 500 |
| Test | 10,000 | 540 |

**Asked at:** commonly asked (no company-specific report found); A/B result reading is a recurring theme (unverified).
**What the interviewer is checking:** That you quote the lift correctly and test whether it could be chance.
**Say this in the interview:** "The test converts at 5.4% against 5.0%, a relative lift of 8%, but it is only 0.4 percentage points and is not statistically significant, so I would not ship on this alone."

**What the data shows:** The test is ahead, but by a small margin on these sample sizes.
**Working:**
1. Control rate: 500 / 10,000 = 5.0%. Test rate: 540 / 10,000 = 5.4%.
2. Absolute difference: 0.4 percentage points. Relative lift: 0.4 / 5.0 = 8.0%.
3. Two-proportion z-test (pooled rate 5.2%; the z score says how many standard errors apart the two rates are, and the p-value is the chance of a gap this big if the button truly did nothing): z is about 1.27, two-sided p-value about 0.20.
4. 95% interval for the difference: about -0.2 to +1.0 percentage points (it includes zero).
**Result:** +0.4 pp (8% relative lift); p about 0.20, not significant at the usual 5% level.
**Caveats / what else I would check:** Was the sample size planned in advance? Did the test run full weeks? Was assignment random (check both groups look alike)? Were guardrail metrics checked (revenue per visitor, refunds, page speed)? Novelty effects? Did I peek and stop early?
**Next step / recommendation:** Keep running to a pre-agreed sample size, or accept that a small lift needs more traffic: to detect 0.4 pp reliably (80% power, 5% level) needs about 48,000 visitors per arm, far more than 10,000. If the change is cheap and harmless, a business may still ship it on non-statistical grounds, saying so openly.
**Likely follow-ups:** 1) *Does p = 0.20 mean no effect?* No, it means the data cannot rule out chance. 2) *Percent or percentage points?* Say both.
**Common mistakes / traps:** Shipping because B is higher; quoting 8% without the 0.4 pp; stopping the test the first time it looks good.

### Q18 ⭐⭐⭐ 🟡 Variant B has a higher conversion rate than A in every device segment below, but a lower rate overall. Verify the overall rates, explain how this can happen, and say which variant you would recommend.
| Variant | Mobile | Desktop |
|---|---|---|
| A | 10 / 100 | 180 / 400 |
| B | 120 / 800 | 50 / 100 |

(each cell is conversions / visitors)
**Asked at:** commonly asked (no company-specific report found); Simpson's-type reversals are a recurring theme on practice sites (unverified).
**What the interviewer is checking:** That you can explain a reversal through mix, and pick the sensible comparison.
**Say this in the interview:** "B wins in both segments, 15% against 10% on mobile and 50% against 45% on desktop, but loses overall (18.9% against 38.0%) because B got mostly mobile traffic, which converts less. This is Simpson's paradox."

**What the data shows:** The segment view and the overall view disagree, and the difference is in the traffic mix.
**Working:**
1. Mobile: A = 10 / 100 = 10%; B = 120 / 800 = 15%. Desktop: A = 180 / 400 = 45%; B = 50 / 100 = 50%.
2. Overall: A = 190 / 500 = 38.0%; B = 170 / 900 = 18.9%.
3. Mix: A traffic is 20% mobile (100 of 500); B is 88.9% mobile (800 of 900).
4. Same-mix comparison, using the pooled traffic (900 mobile, 500 desktop): A = (10% x 900 + 45% x 500) / 1,400 = 22.5%; B = (15% x 900 + 50% x 500) / 1,400 = 27.5%.
**Result:** Overall A 38.0% vs B 18.9%; at equal mix B leads, 27.5% vs 22.5%.
**Caveats / what else I would check:** The mix itself is a red flag: random assignment would give similar device shares in both arms, so I would check for a split bug or a targeting rule. Small cells (A mobile has 100 visitors, B desktop 100) mean wide uncertainty; the differences (5 points on desktop) may be noise. Also check the effect is real after the mix issue is fixed.
**Next step / recommendation:** Prefer B on this evidence only if the device split is understood. Use the segment view, because device is fixed before the visitor sees the variant, but re-run with a properly randomised split before shipping.
**Likely follow-ups:** 1) *Which number goes to leadership?* The within-segment (or mix-adjusted) comparison, with the caveat. 2) *Could the reverse happen?* Yes, if a segment variable is influenced by the variant, the overall view is the right one.
**Common mistakes / traps:** Trusting the overall rate; not computing the mix; recommending without questioning why the mix differs.

### Q19 ⭐⭐⭐ 🟡 Orders, returns and return rate by city are shown below (exercise data). A colleague says the top three cities "cause most returns". Do you agree, and what would you check next?
| City | Orders | Returns | Return rate |
|---|---|---|---|
| City A | 20,000 | 1,600 | 8.0% |
| City B | 15,000 | 900 | 6.0% |
| City C | 12,000 | 840 | 7.0% |
| City D | 3,000 | 330 | 11.0% |
| City E | 800 | 120 | 15.0% |

**Asked at:** commonly asked (no company-specific report found); concentration versus rate questions are a recurring theme (unverified).
**What the interviewer is checking:** That you separate volume from rate and do not confuse "most returns" with "worst problem".
**Say this in the interview:** "They have most returns only because they have most orders. Their share of returns, 88.1%, is lower than their share of orders, 92.5%. The problem cities by rate are D and E."

**What the data shows:** Big cities have many returns, but small cities return a higher share of orders.
**Working:**
1. Totals: orders 50,800; returns 3,790; overall return rate 3,790 / 50,800 = 7.46%.
2. Top three (A, B, C): returns 1,600 + 900 + 840 = 3,340, which is 88.1% of returns; orders 47,000, which is 92.5% of orders.
3. Excess returns versus the 7.46% average: City A +108, City B -219, City C -55, City D +106, City E +60 (rounded).
4. Rates: D 11.0% and E 15.0% are well above average.
**Result:** I agree on counts, not on cause. City A is the one big city above average (+108 excess); D and E have the highest rates, but E has only 800 orders.
**Caveats / what else I would check:** Return reason and product category by city (size and fit in fashion, damage in transit); courier or warehouse by city; cash-on-delivery share; promotions; time lag (returns arrive after orders, so recent orders are under-counted); small base in E (120 returns, so one bad batch matters).
**Next step / recommendation:** Break returns by reason, category and courier for City A, D and E. Fix the biggest leaks first by excess returns, which are A and D. Track return rate monthly with a cut-off so lags do not distort it.
**Likely follow-ups:** 1) *Why not act on City E first (15%)?* Smaller excess (60 returns) than A or D; check if it is one product or courier. 2) *Is 7.5% bad?* Depends on category; benchmark internally.
**Common mistakes / traps:** Ranking by counts; ignoring return lag; assuming the city causes the returns.

### Q20 ⭐⭐⭐ 🟡 Average order value rose from Rs 800 to Rs 900 while orders fell from 10,000 to 8,500 (exercise data). Compute the change in total revenue and say what you would investigate.
**Asked at:** commonly asked (no company-specific report found); price-volume decomposition is a recurring theme (unverified).
**What the interviewer is checking:** That you compute total revenue and split it into value and volume effects.
**Say this in the interview:** "Revenue fell from Rs 80 lakh to Rs 76.5 lakh, down Rs 3.5 lakh or 4.4%: the 12.5% higher order value did not make up for 15% fewer orders."

**What the data shows:** Fewer orders, each bigger, with a net loss of revenue.
**Working:**
1. Before: 10,000 x Rs 800 = Rs 80,00,000 (80 lakh). After: 8,500 x Rs 900 = Rs 76,50,000 (76.5 lakh).
2. Change: -Rs 3,50,000 (-3.5 lakh), which is -4.375%, about -4.4%.
3. Orders: -15.0%. Average order value: +12.5%.
4. Split: value effect = (900 - 800) x 8,500 = +Rs 8.5 lakh; volume effect = (8,500 - 10,000) x 800 = -Rs 12 lakh; net = -3.5 lakh.
**Result:** Revenue down Rs 3.5 lakh (4.4%); lost volume cost Rs 12 lakh, higher order value recovered Rs 8.5 lakh.
**Caveats / what else I would check:** Why order value rose: a price increase (which could have cost orders), small orders disappearing (mix, such as dropped low-value customers or removed free-shipping threshold), more items per order, or a big bulk order. Customer counts and repeat rate; profit per order; returns; seasonality.
**Next step / recommendation:** Split orders by order-value band and by new versus repeat customers, and check whether a price or threshold change on a known date lines up with the fall. Judge success on profit and customers retained, not revenue alone.
**Likely follow-ups:** 1) *Is it bad that orders fell?* If the lost orders were unprofitable, profit might still rise; check margin. 2) *What is the break-even order drop?* At Rs 900, orders need to be at least 80,00,000 / 900, about 8,889, to hold revenue.
**Common mistakes / traps:** Looking at one metric; calling higher order value a win; not splitting the effects.

### Q21 ⭐⭐⭐ 🟡 A funnel for two weeks is shown below (exercise data). Overall conversion fell. Which step moved, and what are the two or three explanations you would test first?
| Step | Week 1 | Week 2 |
|---|---|---|
| Sessions | 100,000 | 120,000 |
| Add to cart | 12,000 | 13,200 |
| Payment success | 3,000 | 2,900 |

**Asked at:** commonly asked (no company-specific report found); funnel-drop diagnosis is a recurring theme (unverified).
**What the interviewer is checking:** That you compute step rates in both weeks and localise the fall.
**Say this in the interview:** "Overall conversion fell from 3.0% to 2.4%. The biggest move is cart to payment, from 25.0% to 22.0%; the cart rate also slipped a little, from 12.0% to 11.0%."

**What the data shows:** Traffic is up 20% but payments are down 3.3%.
**Working:**
1. Session to cart: Week 1 12,000 / 100,000 = 12.0%; Week 2 13,200 / 120,000 = 11.0% (-1.0 pp).
2. Cart to payment: Week 1 3,000 / 12,000 = 25.0%; Week 2 2,900 / 13,200 = 22.0% (-3.0 pp).
3. Overall: Week 1 3,000 / 100,000 = 3.0%; Week 2 2,900 / 120,000 = 2.42%, about 2.4% (-0.6 pp, or -19.4% relative).
4. If Week 2 cart-to-payment had stayed at 25%, payments would be 3,300, which is 400 more than the actual 2,900.
**Result:** Both steps weakened, with most of the damage at cart to payment (the funnel has no "checkout started" step, so it hides where in checkout).
**Caveats / what else I would check:** Week definitions and tracking; whether Week 2 had a sale; new or returning, source and device mix.
**Next step / recommendation:** Test first: (1) payment or checkout failures after a release (error rates, gateway success by method and bank); (2) traffic mix: a campaign bringing low-intent visitors (check by source), which would explain the lower cart rate and some of the payment rate; (3) pricing, shipping fees or a stock-out discovered at checkout. Then compare by device and source and agree a fix and a metric.
**Likely follow-ups:** 1) *Which fix is first?* Whatever the data localises; payment failures are usually quickest to check. 2) *Is week-on-week enough?* Also compare with the same weekday pattern and a longer trend.
**Common mistakes / traps:** Pointing to the traffic increase only; computing rates only on the overall level; ignoring that payment success (not attempts) is measured.

### Q22 ⭐⭐⭐ 🟡 The month-to-date figures on a dashboard show a 30% drop in orders versus last month on the 12th. What do you check before raising an alarm?
**Asked at:** commonly asked (no company-specific report found); "traffic or sales dropped" investigation prompts recur in guides (unverified).
**What the interviewer is checking:** That you rule out comparison and data-lag artefacts before looking for business causes.
**Say this in the interview:** "First I check whether the comparison is fair: the same 12 days, the same weekdays, and complete data. Only then do I treat a 30% drop as real."

**First, clarify / contain:** Note the time, source and what is being compared; tell the owner I am verifying and will update by a set time. I do not announce a cause.
**What I would check, in order:**
1. What is the comparison? If it is 12 days against the full last month, 12 / 30 = 40% of the month, so a normal month would show a 60% "drop". A 30% drop shown this way would actually mean a daily run-rate 75% above last month (0.70 / 0.40 = 1.75), which is implausible, so either the comparison is already like-for-like or something else is off.
2. Same period? Day 1 to 12 against day 1 to 12 of last month, with the same weekday mix (weekends, month-end spikes).
3. Data completeness: did today's and the last few days' loads finish (row counts, refresh time, late-arriving orders)?
4. Definitions: did the order definition, filters or time zone change?
5. Calendar: holiday, salary-day timing, a sale that last month had and this month lacks.
6. Segment: is the fall everywhere or in one channel, city or product (this separates demand from a technical issue)?
7. Traffic and conversion: are visits normal, and is the fall in the funnel?
**If I find...:** an unfair comparison or incomplete data, it is not a real drop, fix the report; a real drop in one segment, localise it and alert the owner; a real broad drop, escalate with sizes and next steps.
**What I would tell the stakeholder:** "The dashboard shows orders down 30% against last month. I am checking that the comparison is like for like and the data is complete. Update by [time]."
**Prevent it next time:** Show same-day-of-month and same-weekday comparisons, a data-freshness stamp and a "partial period" label on month-to-date tiles.
**Likely follow-ups:** 1) *If real?* Quantify the lost orders and revenue, and find the segment. 2) *Who do you tell first?* The metric owner, then the business lead.
**Common mistakes / traps:** Raising an alarm on a part-month comparison; ignoring data lag; guessing a business cause first.

### Q23 ⭐⭐⭐ 🟡 The company-level average salary by gender looks very different from the within-grade averages below (exercise data, in lakh). Compute the overall male and female averages, and explain what the grade split says and what is still unexplained.
| Grade | Male avg | Female avg | Male count | Female count |
|---|---|---|---|---|
| L1 | 6.0 | 5.9 | 20 | 60 |
| L2 | 10.0 | 9.9 | 50 | 40 |
| L3 | 18.0 | 17.8 | 40 | 10 |

**Asked at:** commonly asked (no company-specific report found); pay-gap-by-grade is a gap-fill HR exhibit in this part (judgement).
**What the interviewer is checking:** That you can show how grade mix creates most of the headline gap, without declaring the remaining gap fine.
**Say this in the interview:** "The overall averages are 12.18 lakh for men and 8.44 lakh for women, a 31% gap. Within each grade the gap is only 1 to 2%, so most of the headline gap is about who sits in which grade, which is itself the question to examine."

**What the data shows:** Women are concentrated in the lowest grade and men in the highest, while within each grade pay is almost equal.
**Working:**
1. Male average: (6.0 x 20 + 10.0 x 50 + 18.0 x 40) / 110 = 1,340 / 110 = 12.18 lakh.
2. Female average: (5.9 x 60 + 9.9 x 40 + 17.8 x 10) / 110 = 928 / 110 = 8.44 lakh.
3. Overall gap: 3.75 lakh, which is 30.7% of the male average.
4. Within-grade gaps: L1 0.1 (1.7%), L2 0.1 (1.0%), L3 0.2 (1.1%).
5. Grade mix: women are 54.5% L1, 36.4% L2, 9.1% L3; men are 18.2% L1, 45.5% L2, 36.4% L3.
6. If men had the female grade mix, their average would be 8.55, only 0.11 above women's 8.44 (about 1.3%).
**Result:** Overall averages: men 12.18 lakh, women 8.44 lakh (gap 3.75 lakh, about 31%); within-grade gaps are about 1 to 2%.
**Caveats / what else I would check:** The small within-grade gap is not proof of equal pay: check tenure, role, performance, location and starting pay inside each grade. Unexplained: why women are in lower grades (hiring level, promotion rates, attrition by gender, career breaks); whether grade assignment is itself fair. Group sizes are small (L3 has 10 women), so a 0.2 gap may be noise. Check in a regression only with enough data.
**Next step / recommendation:** Report both views: the headline gap and the within-grade gap. Then look at the promotion rate, hiring grade and exits by gender. Handle individual pay data with restricted access.
**Likely follow-ups:** 1) *Is this Simpson's paradox?* It is a mix effect: the group gap comes from composition, not within-group pay. 2) *Would you correct the within-grade gaps?* Review individual cases, with HR and legal.
**Common mistakes / traps:** Saying "no gap" because within-grade is close; ignoring the grade mix as a finding; using small groups to claim precision.

### Q24 ⭐⭐⭐ 🟡 Customer survey scores are shown for two quarters, based on different numbers of responses (exercise data). Is the NPS drop real, and what do you tell the product manager?
| Quarter | Responses | NPS |
|---|---|---|
| Q1 | 1,200 | 45 |
| Q2 | 40 | 38 |

**Asked at:** commonly asked (no company-specific report found); small-sample survey scores are a staple of data-interpretation guides (unverified).
**What the interviewer is checking:** Whether you ask "how many responses?" before calling a change real.
**Say this in the interview:** "I would not call it a drop yet. The Q2 score rests on only 40 responses, so it could easily be noise. I would say 'not enough evidence either way' and fix the sample."
**What the data shows:** NPS (Net Promoter Score: percent promoters minus percent detractors, range -100 to +100) is 45 on 1,200 responses in Q1 and 38 on 40 responses in Q2. The headline gap is 7 points, but the two scores are not equally trustworthy.
**Working:**
1. Change: 38 - 45 = -7 points (a difference of points, not percent).
2. Uncertainty of an NPS (the standard error, a measure of how much a score from a sample can wobble by chance) is roughly sqrt((P + D - (P - D)^2) / n), where P and D are the promoter and detractor shares and n is the number of responses. The table does not give P and D, so I use the worst case (P + D = 1), which gives a safe upper bound.
3. Q1 (n = 1,200): standard error about 2.6 points, so a 95% range of roughly 40 to 50.
4. Q2 (n = 40): standard error about 14.6 points, so a 95% range of roughly 9 to 67.
5. Standard error of the difference is about 14.9 points; -7 is only about 0.5 standard errors, far below the usual 2.
**Result:** The 7-point fall is well inside the noise. With an assumed realistic mix (60% promoters, 15% detractors in Q1; 55% and 17% in Q2) the answer is the same: roughly 0.6 standard errors. For scale: about 1,230 responses would shrink one quarter's 95% range to plus or minus 5 points, and reliably detecting a 7-point fall between two quarters would need roughly 2,500 responses in each (worst case, 80% power). Figures rounded to 1 decimal.
**Caveats / what else I would check:** Why did responses fall from 1,200 to 40 (a survey trigger broke, a different channel, only a quarter-to-date partial)? Who responded (non-response bias)? Same question wording and scale? Is Q2 an incomplete quarter?
**Next step / recommendation:** Tell the product manager: "No evidence of a real drop yet; the Q2 sample is too small. Let us first find out why volume collapsed, collect as many responses as we can (a few hundred gives a plus or minus 9 point range; over a thousand gives about plus or minus 5), and re-read the score with a range, not a single number."
**Likely follow-ups:** 1) *What if 40 was all you could get?* Report the score with its wide range and call it directional. 2) *Could the drop still be real?* Yes; small data cannot rule it in or out.
**Common mistakes / traps:** Reporting 45 to 38 as a trend; comparing scores without comparing sample sizes; quoting the 7 as "7%".

### Q25 ⭐⭐⭐ 🟡 The table below shows planned versus actual cost by department (exercise data, in lakh). Which department is the real concern, and why might the biggest percentage variance not be it?
| Department | Budget | Actual |
|---|---|---|
| Marketing | 20 | 26 |
| IT | 200 | 214 |
| Admin | 50 | 49 |
| Operations | 400 | 436 |

**Asked at:** commonly asked (no company-specific report found); budget-variance reading appears in finance-flavoured analyst case discussions (unverified).
**What the interviewer is checking:** Whether you look at rupee impact and share of the overrun, not just the percentage.
**Say this in the interview:** "Marketing has the biggest percentage overrun at 30%, but it is only 6 lakh. Operations at 9% is 36 lakh, about two thirds of the net overrun, so that is where I would look first."
**What the data shows:** Three of four departments are over budget; Admin is slightly under.
**Working:**
1. Marketing: 26 - 20 = +6 lakh, 6/20 = 30.0%.
2. IT: 214 - 200 = +14 lakh, 7.0%.
3. Admin: 49 - 50 = -1 lakh, -2.0%.
4. Operations: 436 - 400 = +36 lakh, 9.0%.
5. Total: budget 670, actual 725, net overrun 55 lakh, 8.2%.
6. Operations' share of the net overrun: 36/55 = 65.5%; IT 25.5%; Marketing 10.9%; Admin -1.8%.
**Result:** Real concern: Operations (36 lakh, 65% of the net overrun, at 9%). Biggest percentage: Marketing (30%), but only 6 lakh. Rounded to 1 decimal.
**Caveats / what else I would check:** Is the overrun timing (spend booked early) or permanent? Is it volume-driven (more orders, so more cost is healthy) or price-driven? Was the small Marketing budget unrealistic? Is the year only partly complete (compare to budget-to-date, not full year)? Are one-off items included?
**Next step / recommendation:** Ask Operations to split the 36 lakh into volume, rate and one-off items; keep Marketing on a watch list because 30% on a small base can double next quarter. Track variance in lakh and percent side by side.
**Likely follow-ups:** 1) *When does percentage matter?* When a small line is growing fast or sits on a risky budget. 2) *What would you chart?* A bar of variance in lakh, labelled with percent.
**Common mistakes / traps:** Ranking by percent only; ignoring the base; treating every overrun as bad without checking volume.

### Q26 ⭐⭐⭐ 🟡 What is a checklist of caveats you would mention for any chart or table before an insight is acted on?
**Asked at:** commonly asked (no company-specific report found); caveats and "what else would you check" are recurring themes in interpretation guides (unverified).
**What the interviewer is checking:** That you have a habit, not a one-off list of worries.
**Say this in the interview:** "Before anyone acts on a chart I run a short checklist: what is counted, over what period, against what, and how sure are we."
**Explain simply:**
- **Definition and units:** what does the metric mean, and is it rupees, lakh, percent or percentage points?
- **Denominator:** rate of what? 5 resignations means little without headcount.
- **Time window:** full period or partial? Is the last month incomplete? Seasonality (festive months, appraisal cycles)?
- **Comparison base:** versus last month, last year, target? Fair like-for-like?
- **Sample size and spread:** how many records? Averages hiding a wide spread or outliers (use median or percentiles)?
- **Mix and segments:** does the total hide a different story by region, grade or product (Simpson's paradox)?
- **Data quality:** duplicates, missing values, definition changes, late-arriving data, filters left on.
- **Cause versus pattern:** correlation is not cause; what else could explain it?
- **Chart honesty:** axis start, dual axes, truncated scales.
**Mini-example:** "Attrition 12%" becomes safe to act on once I know: annualised or monthly, which headcount, which period, and that the sales team is not 30%.
**Practice step:** Take any dashboard you have seen and write one line against each bullet.
**Likely follow-ups:** 1) *Which is most important?* Denominator and definition, because they change the number itself. 2) *What if you cannot check them?* State them as assumptions and label the insight provisional.
**Common mistakes / traps:** A long generic list with no example; skipping the denominator; saying "more data needed" without saying which data.

### Q27 ⭐⭐⭐ 🟡 How would you present the main finding from a table to a non-technical executive in two minutes, and what would you deliberately leave out?
**Asked at:** commonly asked (no company-specific report found); executive summarising is described in consulting and hiring guides as "insight, link to the decision, next step" (unverified).
**What the interviewer is checking:** Whether you lead with the answer and keep to what the executive needs for a decision.
**Say this in the interview:** "I lead with one sentence: what happened, why it matters, and what I recommend. The working goes in a backup slide."
**Clarify first:** What decision is this executive about to make, and how much time and trust do they have?
**Plan:**
1. Sentence one: the headline with one number ("Attrition in sales is 24%, double the company average").
2. Sentence two: why it matters in money or risk terms.
3. Sentence three: the cause I believe, with my confidence level.
4. Sentence four: the ask or recommendation, owner and date.
5. One simple visual that shows only the key comparison; keep the table as backup.
6. Pause for questions; I carry the detail in my head, not on the slide.
**Method choice and why:** Answer first, then evidence (pyramid style). Executives rarely need the method.
**Pitfalls:** Walking through the table row by row; ten caveats; jargon like "p-value"; hiding a weak spot. What I leave out: data-cleaning steps, minor categories, tests, and findings that do not change the decision (kept in the appendix, and I say they exist).
**Deliverable:** A one-slide or one-paragraph summary plus an appendix, delivered within the two minutes, followed by a written note.
**Likely follow-ups:** 1) *What if they ask for the detail?* Go to the backup. 2) *What if the finding is uncertain?* Say it in one line: "I am fairly sure about X, less sure about Y; here is how we will find out."
**Common mistakes / traps:** Describing the table instead of interpreting it; burying the recommendation; hiding the uncertainty that matters.

### Q28 ⭐⭐⭐ 🟡 Weekly sales spike in the week of a marketing campaign, as the chart shows. What else could explain the spike, and what would you need to claim the campaign caused it?
**Asked at:** commonly asked (no company-specific report found); causation-versus-correlation on a campaign chart is a common case prompt (unverified).
**What the interviewer is checking:** Whether you can list alternative explanations and name the evidence that would show causation.
**Say this in the interview:** "The spike fits the campaign, but it also fits other things. To claim the campaign caused it I would want a comparison group or a baseline, not just the timing."
**Clarify first:** Spike in what (orders, revenue, visitors), how big, and which products or regions? What was the decision: repeat the campaign or cut it?
**Plan:**
1. Rule out data issues: a double load, a changed definition, a bulk order.
2. List other explanations: seasonality or payday week, festival, a price cut or discount, a stock-out in the previous week pushing demand forward, competitor stock-out, a pricing change, a trend already rising.
3. Check the pre-period: was sales already rising before launch? Is the same week last year also high?
4. Check segments: did regions or products that were not targeted spike too? If yes, the campaign is not the only driver.
5. Look after the spike: a drop afterwards means demand was pulled forward, not created.
**Method choice and why:** Simplest first: compare with last year's same week and with untargeted regions. If possible, a holdout (some customers or regions with no campaign) or a difference-in-differences comparison (change in the targeted group minus change in the untargeted group).
**Pitfalls:** Attributing all of the spike to the campaign; ignoring cost (incremental margin versus campaign spend).
**Deliverable:** "Estimated uplift of X (range Y to Z) over baseline, cost per incremental order, confidence level", with caveats.
**Likely follow-ups:** 1) *No holdout exists?* Use a same-week-last-year or similar-region comparison and label it indicative. 2) *Next campaign?* Design a holdout.
**Common mistakes / traps:** "Sales spiked after the campaign, so it worked"; claiming ROI without a baseline.

### Q29 ⭐⭐⭐ 🟡 A delivery-time chart shows an average of 30 minutes, but customers complain about lateness. The percentile table below is given (exercise data). What does it tell you, and which metric would you put on the dashboard?
| Metric | Minutes |
|---|---|
| Mean | 30 |
| Median | 26 |
| 90th percentile | 48 |
| 99th percentile | 85 |

**Asked at:** commonly asked (no company-specific report found); mean-versus-tail delivery metrics appear in operations and e-commerce case prompts (unverified).
**What the interviewer is checking:** Whether you know that an average can hide the bad experiences that customers actually complain about.
**Say this in the interview:** "The average of 30 minutes hides a long tail. One in ten orders takes 48 minutes or more and one in a hundred takes 85 or more. I would put the 90th percentile on the dashboard."
**What the data shows:** Mean 30 is above the median 26, so a few very slow orders pull the mean up (right-skewed). Half of orders arrive within 26 minutes, yet the slow end is long.
**Working:**
1. Mean minus median: 30 - 26 = 4 minutes (tail pulls the average up).
2. 90th percentile (P90) is 48, which is 48/26 = 1.85 times the median (+22 minutes).
3. 99th percentile (P99) is 85, which is 85/30 = 2.83 times the mean.
4. So about 10% of orders take at least 48 minutes, which can explain the complaints.
**Result:** The mean is not the experience of the unhappy customers. Put P90 (and the share of orders later than the promised time) on the dashboard, with the median as the "typical" figure.
**Caveats / what else I would check:** Is the promise 30 minutes, 45 minutes? What share of orders is late against it? Which zones, hours or restaurants make up the tail? Are cancelled orders excluded (which would hide the worst cases)? Is P99 stable or noisy on a small base?
**Next step / recommendation:** Dashboard: median, P90, and "percent delivered within promise". Investigate the slow tail by zone and hour. Track the tail weekly.
**Likely follow-ups:** 1) *Why not P99?* It is noisy and sensitive to outliers; good for a quality alert, not the main KPI. 2) *Why keep the median?* It is robust and tells the typical case.
**Common mistakes / traps:** Reporting only the average; showing the mean and median with no tail; using a percentile without saying what share of orders it covers.

### Q30 ⭐⭐⭐ 🟡 A recruiter reports that offers made to women and men in one hiring round gave the numbers below (exercise data). Compute the selection rates and the ratio, and say what you would do with the result.
| Group | Applicants | Selected |
|---|---|---|
| Men | 200 | 40 |
| Women | 120 | 16 |

**Asked at:** commonly asked (no company-specific report found); adverse-impact checks are a standard HR-analytics prompt (unverified; the 80% rule is a US guideline recalled from memory, so confirm the applicable standard with HR/legal).
**What the interviewer is checking:** That you compute selection rates correctly, compare them as a ratio, and handle a sensitive finding carefully.
**Say this in the interview:** "Men were selected at 20% and women at 13.3%, a ratio of 0.67. That is below the common 0.8 screening threshold, so I would flag it for review, not call it discrimination yet."
**What the data shows:** Women were selected at a lower rate than men.
**Working:**
1. Men: 40/200 = 20.0%.
2. Women: 16/120 = 13.3%.
3. Impact ratio (women's rate divided by men's rate): 13.3/20.0 = 0.67.
4. If women had been selected at the men's rate: 120 x 20% = 24 offers expected versus 16 actual, a gap of 8.
5. Significance check (Fisher's exact test on the 2 by 2 counts: it asks how often a gap this big would appear by chance if both groups had the same true rate): p about 0.17, so with these numbers the gap could still be chance.
**Result:** Ratio 0.67 (below the 0.8 rule of thumb), but not statistically significant on 320 applicants (p about 0.17). Percent and ratios rounded to 1 to 2 decimals.
**Caveats / what else I would check:** Same job and stage? Qualifications and shortlisting criteria; interviewer effects; the stage where women drop (screening, interview or offer); a larger sample across rounds; whether data is complete.
**Next step / recommendation:** Report privately to the HR head and legal as "flagged for review", not as a conclusion; review the stage-by-stage funnel and accumulate more rounds; document it, and restrict access to the data.
**Likely follow-ups:** 1) *Is it bias?* The numbers cannot say; they show where to look. 2) *Would a bigger sample change it?* If the same rates held on three times the applicants it would be significant.
**Common mistakes / traps:** Comparing counts (40 vs 16) instead of rates; declaring discrimination or "no problem" from one round; sharing individual-level data widely.

### Q31 ⭐⭐⭐ 🟡 The table below shows offer acceptance by salary band (exercise data). Compute acceptance by band and overall, and say what you would investigate.
| Band | Offers | Accepted |
|---|---|---|
| B1 | 100 | 85 |
| B2 | 80 | 56 |
| B3 | 40 | 22 |

**Asked at:** commonly asked (no company-specific report found); offer-acceptance analysis by band is an HR-analytics gap-fill exercise (judgement; no source report).
**What the interviewer is checking:** That you compute each rate from its own base and overall acceptance from totals, and spot the pattern.
**Say this in the interview:** "Acceptance falls as the band goes up: 85%, 70%, 55%, and 74% overall. The senior offers are the leak, so I would look at pay competitiveness and time to offer there."
**What the data shows:** Acceptance drops steadily with band.
**Working:**
1. B1: 85/100 = 85.0%.
2. B2: 56/80 = 70.0%.
3. B3: 22/40 = 55.0%.
4. Overall: (85 + 56 + 22) / (100 + 80 + 40) = 163/220 = 74.1%.
5. Declined offers: B1 15, B2 24, B3 18, total 57; B3 has 18% of offers but 32% of declines (18/57).
**Result:** 85%, 70%, 55% by band; 74.1% overall (not the simple average of the three, which would be 70.0%). Rounded to 1 decimal.
**Caveats / what else I would check:** B3 has only 40 offers, so 55% is a wide range; check role family and city mix; reasons for decline; counter-offers; our offer versus the candidate's current pay (compa-ratio); time from interview to offer; any seasonal effect.
**Next step / recommendation:** Pull decline reasons for B2 and B3, benchmark pay for those bands, and measure acceptance monthly with the same definition (accepted divided by offers released).
**Likely follow-ups:** 1) *Why not average 85, 70, 55?* The bands have different numbers of offers; use the totals. 2) *Is B3 low because of pay?* Test it against decline reasons.
**Common mistakes / traps:** Averaging the percentages; ignoring the small B3 base; not defining whether withdrawn offers count.

### Q32 ⭐⭐⭐ 🟡 New joiner exits are shown below by joining month (exercise data). Compute the 90-day exit rate for each cohort and say what you would ask the business.
| Joining month | Joiners | Left within 90 days |
|---|---|---|
| Jan | 50 | 5 |
| Feb | 60 | 9 |
| Mar | 40 | 10 |

**Asked at:** commonly asked (no company-specific report found); 90-day exit cohorts are an HR-analytics gap-fill exercise (judgement; no source report).
**What the interviewer is checking:** Whether you compute exit rates per cohort and ask what changed in the business.
**Say this in the interview:** "Early exits rose from 10% in January to 15% in February and 25% in March. That is a clear worsening trend, so I would ask what changed in hiring or onboarding."
**What the data shows:** Each later cohort loses a bigger share in the first 90 days.
**Working:**
1. Jan: 5/50 = 10.0%.
2. Feb: 9/60 = 15.0%.
3. Mar: 10/40 = 25.0%.
4. All three: 24/150 = 16.0%.
**Result:** 10%, 15%, 25%; combined 16.0%. March is 15 percentage points above January (2.5 times the rate).
**Caveats / what else I would check:** Is the March cohort complete? The 90-day window must have fully closed; if the data was pulled before 90 days passed for March joiners, 25% is understated, not overstated. Counts are small (10 leavers), so the trend needs confirming. Check whether exits were resignations or terminations (probation fails).
**Next step / recommendation:** Ask the business: did the source of hire change, did the role mix or the managers change, did onboarding or the offer promise change, was there a bulk hiring drive? Split by source, role and manager, and track the rate monthly.
**Likely follow-ups:** 1) *How do you treat the March cohort if joiners are too recent?* Mark it "not mature" and use a shorter window for all cohorts. 2) *Is it statistically significant?* Probably not on its own at these counts; I would call it a signal to monitor.
**Common mistakes / traps:** Reading the March cohort before 90 days have passed; mixing resignations and terminations; no cohort split.

### Q33 ⭐⭐⭐ 🔴 Two dashboards show different totals for the same month: Finance shows revenue of 10.4 crore and Sales shows 10.9 crore. Given a table of both definitions (booking date versus invoice date, taxes included versus excluded), how do you reconcile them and what do you present?
**Asked at:** commonly asked (no company-specific report found); reconciling two dashboards is a standard data-trust scenario (unverified). Premise note: the question refers to a definitions table that is not in the part file, so the amounts below are an illustrative bridge I built to total the 0.5 crore gap.
**What the interviewer is checking:** Whether you reconcile with a bridge from one number to the other instead of picking a winner.
**Say this in the interview:** "Both can be right under different definitions. I would build a bridge from Sales 10.9 to Finance 10.4, explain each step, and present one agreed metric."
**First, clarify / contain:** The gap is 10.9 - 10.4 = 0.5 crore (about 4.8% of Finance's figure). I do not say either dashboard is wrong, and I do not send the numbers upward until reconciled.
**What I would check, in order:**
1. Definition: Sales counts on booking date (order placed); Finance counts on invoice date (billed).
2. Tax basis: are both ex-tax or are taxes in only one? A tax difference would show up as one steady percentage of every invoice, so I test whether the 0.5 crore is a flat share of revenue (here 0.5 / 10.4 = 4.8%).
3. Period cut-offs: the month-end date and the time zone.
4. Credits: returns, credit notes and cancellations posted in one system only.
5. Scope: same entities, currencies, intercompany sales excluded.
**If I find...:** Booked but not invoiced explains the gap: this is timing, not an error. Tax included in one side: restate to the same basis. Unexplained residual: raise it to both data owners and treat it as a data issue.
**Illustrative bridge (crore; all amounts are invented, and it assumes both sides already use the same tax basis, otherwise I would add a tax line):** Sales 10.9; less booked this month but invoiced later 0.70; plus invoiced this month from earlier bookings 0.35; less credit notes posted only in Finance 0.15; equals Finance 10.4 (10.9 - 0.70 + 0.35 - 0.15 = 10.4, checked).
**What I would tell the stakeholder:** "The two numbers differ by 0.5 crore because of timing and credit notes. Bookings are a leading indicator; invoiced revenue is what we report externally. I suggest we show both, clearly labelled, with this bridge, by Friday."
**Prevent it next time:** One metric dictionary with one owner per definition, both labelled "Bookings" and "Invoiced revenue", and an automatic monthly reconciliation.
**Likely follow-ups:** 1) *Which do you show the CEO?* Both, labelled, with the bridge; use the Finance number for reported revenue. 2) *What if a residual remains?* List it, set a tolerance (for example under 0.5%), and investigate above it.
**Common mistakes / traps:** Choosing a winner; renaming both "Revenue"; forgetting taxes and credit notes.

### Q34 ⭐⭐⭐ 🔴 Revenue by product is shown below (exercise data). Compute the overall growth, and say what the real story is when the existing products are flat or declining.
| Product | Q1 revenue | Q2 revenue |
|---|---|---|
| Legacy | 300 | 280 |
| Core | 400 | 395 |
| New launch | 0 | 120 |

**Asked at:** commonly asked (no company-specific report found); mix-versus-total growth stories appear in business-case prompts (unverified).
**What the interviewer is checking:** Whether you look under the total to see which products are growing.
**Say this in the interview:** "Total revenue is up 13.6%, but all of it comes from the new launch. Without it, revenue fell 3.6%, so the base business is slipping."
**What the data shows:** Legacy and Core both fell slightly; the new launch adds 120.
**Working:**
1. Q1 total: 300 + 400 + 0 = 700. Q2 total: 280 + 395 + 120 = 795.
2. Overall growth: (795 - 700) / 700 = 13.6%.
3. Legacy: -20, -6.7%. Core: -5, -1.3%.
4. Existing products together: 700 to 675, a fall of 25, -3.6%.
5. New launch is 120/795 = 15.1% of Q2 revenue; it contributes 120 of the +95 total (more than 100% of net growth).
**Result:** Total +13.6%; existing products -3.6%; the growth is entirely new-launch revenue. Rounded to 1 decimal.
**Caveats / what else I would check:** Is the new launch cannibalising Legacy (customers switching)? Is the launch revenue a one-time pipeline fill (distributor stocking) or recurring? Price versus volume in Legacy; one quarter is too short for a trend; margin of the new product versus the old.
**Next step / recommendation:** Report total and base growth side by side; analyse Legacy churn and cannibalisation, new-launch repeat purchases and margin; set a target for the base business, not just for the total.
**Likely follow-ups:** 1) *Is this bad news?* Mixed: a healthy launch, but a flat or shrinking core is a risk. 2) *How would you test cannibalisation?* Look at customers who bought Legacy and now buy the new product.
**Common mistakes / traps:** Celebrating 13.6% alone; calling Core's 1.3% fall noise without checking; ignoring the launch's quality.

### Q35 ⭐⭐ 🟢 A pie chart has twelve slices of similar size. What is wrong with it, and what chart would you use instead?
**Asked at:** commonly asked (no company-specific report found); chart-choice questions are common in dashboard rounds (unverified).
**What the interviewer is checking:** Whether you know that people cannot compare many similar slices by angle.
**Say this in the interview:** "Twelve similar slices cannot be compared by eye. I would use a sorted horizontal bar chart, which shows rank and size at once."
**Explain simply:**
- Humans compare lengths far better than angles or areas, so close slices look the same.
- Twelve labels and colours need a legend, which makes the reader look back and forth.
- Pies suit two to five parts that add to a whole, with clear differences.
**Mini-example:** Twelve departments at 7% to 10% each: a sorted bar chart shows the top three and the bottom three immediately; the pie shows twelve similar wedges.
**Practice step:** Re-draw any pie you have with a sorted bar and see what you notice that the pie hid. If a part-to-whole message matters, add the percent labels, or group the small slices into "Other" (watch that "Other" does not become the largest slice).
**Likely follow-ups:** 1) *When is a pie fine?* A few slices where one is clearly dominant. 2) *Stacked bar instead?* Good for a single total split into a few parts, poor for twelve.
**Common mistakes / traps:** 3D pies; unsorted slices; random colours with no legend order; an "Other" slice bigger than any single category.

### Q36 ⭐⭐ 🟢 A chart uses two y-axes, with revenue on the left and orders on the right, and the lines appear to cross. Why is this risky, and how do you present it more honestly?
**Asked at:** commonly asked (no company-specific report found); dual-axis charts are a standard misleading-chart discussion (unverified).
**What the interviewer is checking:** Whether you know that the crossing point on a dual-axis chart is created by the axis scale, not by the data.
**Say this in the interview:** "The two lines crossing means nothing, because I can move the crossing anywhere by changing either axis. I would show them separately or index both to 100."
**Explain simply:**
- Each axis can be stretched or shifted independently, so a "cross" is an artifact.
- Readers assume the lines are comparable and infer a story (orders overtaking revenue) that the data does not show.
- Different units (rupees, counts) are not comparable on one scale.
**Mini-example:** Revenue 100 to 120 and orders 1,000 to 1,100. Indexed to the start at 100, revenue is 120 and orders 110: revenue rose faster, which a dual axis could show either way.
**Practice step:** Two small charts stacked on the same time axis, or one chart with both series indexed to 100 at the start, with a note on the base. If you must use two axes, start both at zero, label units clearly and avoid commenting on crossings.
**Likely follow-ups:** 1) *Are dual axes ever fine?* Occasionally for a bar and a rate, with clear labels, but I avoid them for executives. 2) *What would you add?* The ratio itself (revenue per order) as its own line.
**Common mistakes / traps:** Reading the crossing as an event; truncated axes; unlabeled units.

### Q37 ⭐⭐ 🟢 You are shown a 100% stacked bar chart of channel mix by month. A stakeholder says the share of the web channel fell, so web sales fell. How do you respond?
**Asked at:** commonly asked (no company-specific report found); share-versus-level confusion in stacked charts is a common interpretation trap (unverified).
**What the interviewer is checking:** Whether you separate a share (percent of total) from an absolute value.
**Say this in the interview:** "A falling share does not mean falling sales. If the total grew faster, web sales can rise while its share falls. I need the absolute numbers."
**What the data shows:** A 100% stacked chart shows only shares. It hides the total.
**Working (illustrative numbers):**
1. Month 1: total 1,000, web 40%, so web = 400.
2. Month 2: total 1,300, web 35%, so web = 455.
3. Web share fell 5 percentage points (40% to 35%), yet web sales rose 55 units, +13.8% (455/400 - 1).
**Result:** A fall in share is consistent with rising web sales when the total is growing faster. The reverse is also possible.
**Caveats / what else I would check:** Need the totals by month; whether the total is growing because other channels got a promotion; seasonality; channel definition changes.
**Next step / recommendation:** Show the absolute values (a regular stacked bar or lines) beside the share chart, and state the totals on the slide.
**Likely follow-ups:** 1) *When does a fall in share mean a fall in sales?* When the total is flat or growing slowly. 2) *Percentage points or percent?* Share moves are in percentage points.
**Common mistakes / traps:** Reading share as volume; omitting the total; calling a 5-point fall "5%".

### Q38 ⭐⭐ 🟢 The median delivery time fell from 30 to 25 minutes while the mean stayed flat at 32. What can you say about the distribution, and what would you check?
**Asked at:** commonly asked (no company-specific report found); median versus mean is a staple interpretation topic (unverified). Note: I treat the two numbers as exercise inputs and draw only what they support.
**What the interviewer is checking:** Whether you reason about skew and tails from two summary numbers.
**Say this in the interview:** "The middle order got faster, but the average did not improve, so the slow orders have probably got slower. The tail likely grew, and I would confirm with percentiles."
**What the data shows:** Median 30 to 25 (-5 minutes) with the mean flat at 32 in both periods (as the question states). The mean is above the median in both periods, so the distribution has a long right tail.
**Working:**
1. Gap between mean and median before: 32 - 30 = 2 minutes; after: 32 - 25 = 7 minutes.
2. A bigger gap means a heavier right tail: the median fell, yet the mean did not.
3. The mean is the total time divided by the number of orders. The middle order got 5 minutes faster, yet total time per order did not fall, so the orders above the median must on average have got slower by enough to offset the faster ones.
**Result:** The distribution became more skewed: the middle order is faster, but the slow end got worse. Two summary numbers cannot show exactly how many orders improved, so this is a lead to check with percentiles, not a proof. A single "improvement" headline would mislead.
**Caveats / what else I would check:** Percentiles (P75, P90, P99); the share of orders over the promise; outliers or data errors (stuck timestamps); changes in mix (zones, order types); whether cancelled orders are excluded.
**Next step / recommendation:** Show a histogram or percentiles for both periods and find where the slow orders sit (zones, hours, restaurants).
**Likely follow-ups:** 1) *Is the median better than the mean?* Neither; use both plus percentiles. 2) *Which would customers feel?* The tail drives complaints.
**Common mistakes / traps:** Reporting only the median fall as success; assuming the mean tells the same story; ignoring the tail.

### Q39 ⭐⭐ 🟢 A table reports complaints by branch: Branch X has 120 and Branch Y has 45. What do you need before saying that Branch X is worse?
**Asked at:** commonly asked (no company-specific report found); denominator-first reading is emphasised in data-interpretation guides (unverified).
**What the interviewer is checking:** Whether you demand a base (volume) before comparing counts.
**Say this in the interview:** "120 versus 45 is a count, not a rate. I need how many orders or customers each branch handled, and the period, before I can say X is worse."
**Clarify first:** What does "complaint" mean (the same definition at both branches)? Same period? Same product mix?
**Plan:**
1. Get the base: orders, customers or transactions per branch.
2. Compute complaints per 1,000 transactions.
3. Check mix: complaint types, severity, channel; repeat complaints from one customer.
4. Check reporting: does Branch X have an easier way to complain?
5. Look at the trend and a range if volumes are small.
**Illustrative example:** If X handles 12,000 orders and Y 1,500, the rates are 10.0 and 30.0 per 1,000 (120/12 and 45/1.5), so Y is three times worse despite fewer complaints. If both handle 6,000, X is 20 per 1,000 and Y 7.5.
**Method choice and why:** A simple rate first; a funnel-plot or a significance check only if volumes are small.
**Pitfalls:** Comparing counts; large branches always look worse in counts; unequal reporting channels.
**Deliverable:** A table of complaints per 1,000 orders by branch, with volumes shown, sorted, with the types broken down.
**Likely follow-ups:** 1) *What if volumes are equal?* Then X has more complaints, so look at the types. 2) *Small branch?* The rate swings; use a wider period.
**Common mistakes / traps:** Ranking on counts; ignoring severity; comparing different definitions.

### Q40 ⭐⭐ 🟢 A rate in a dashboard tile is shown without a denominator. Give three examples of metrics where that is dangerous and what you would add.
**Asked at:** commonly asked (no company-specific report found); denominators come up in the dashboard-definition discussions of the guides (unverified).
**What the interviewer is checking:** That you know a rate needs both parts, and can name concrete cases.
**Say this in the interview:** "A rate tile with no denominator is a number with no meaning. I would add the base, the period and the definition in the tile's subtitle or hover."
**Explain simply:**
- **Attrition 12%:** of what headcount, over what period (monthly or annual), and which exits count? Add average headcount and the window.
- **Conversion 4%:** of visitors, sessions or leads? Add the funnel step it starts from, and the number of users.
- **Return rate 8%:** of orders, units or revenue, and returned within how many days? Add the unit and window.
- Others: defect rate, complaint rate, absentee rate, offer acceptance.
**Mini-example:** "2 resignations" out of a team of 10 is 20% attrition in a month; out of 1,000 it is 0.2%. The tile hides which.
**Practice step:** Put a tooltip on each rate tile showing numerator, denominator, period and an "as of" date, and show the count beside the percent.
**Likely follow-ups:** 1) *Why is a small denominator dangerous?* One event moves the rate by a large amount. 2) *How do you display it?* Show the counts with the rate, and grey out rates with tiny bases.
**Common mistakes / traps:** Percent without the base; mixing time windows in a tile; "rate" meaning different things on different dashboards.

### Q41 ⭐⭐ 🟢 A forecast is compared with actuals below (exercise data). Compute the MAPE and say what you would also look at beyond that single number.
| Month | Actual | Forecast |
|---|---|---|
| 1 | 100 | 110 |
| 2 | 120 | 100 |
| 3 | 80 | 90 |

**Asked at:** commonly asked (no company-specific report found); forecast accuracy (MAPE) appears in forecasting discussions (unverified).
**What the interviewer is checking:** Whether you can compute MAPE (Mean Absolute Percentage Error) and know what it misses.
**Say this in the interview:** "MAPE is 13.1%, so the forecast is off by about 13% on average. But it does not show whether we are biased high or low, and it treats a 10-unit miss on a small month as a big error."
**What the data shows:** The forecast is wrong in each month, by different amounts.
**Working:**
1. Month 1: |100 - 110| / 100 = 10.0%.
2. Month 2: |120 - 100| / 120 = 16.7%.
3. Month 3: |80 - 90| / 80 = 12.5%.
4. MAPE = (10.0 + 16.7 + 12.5) / 3 = 13.1%.
**Result:** MAPE about 13.1%. Rounded to 1 decimal.
**Caveats / what else I would check:** Bias: forecast minus actual is +10, -20, +10 = 0 in total, so the forecast is not consistently high or low, but errors cancel out, which hides the swing. Weighted error: total absolute error 40 on total actual 300 is 13.3% (WAPE). Also check MAPE breaks when actuals are near zero; three months is a small sample; the cost of over versus under forecasting; a naive benchmark (last month's actual or seasonal).
**Next step / recommendation:** Report MAPE with bias and WAPE, compare with a simple baseline, and track by month.
**Likely follow-ups:** 1) *Is 13% good?* Depends on the business, the horizon and the baseline. 2) *When use WAPE?* When volumes differ widely or contain zeros.
**Common mistakes / traps:** Netting errors (so +10 and -10 cancel); dividing by the forecast instead of the actual; ignoring bias.

### Q42 ⭐⭐ 🟢 The headcount bridge below is from a monthly HR report (exercise data). Compute the closing headcount and check it against the stated figure of 515.
| Item | Employees |
|---|---|
| Opening | 500 |
| New hires | 40 |
| Resignations | 20 |
| Terminations | 5 |
| Transfers in | 3 |
| Transfers out | 8 |

**Asked at:** commonly asked (no company-specific report found); bridge and reconciliation checks are common HR-data prompts (judgement; no source report). Premise note: the stated 515 does not match the bridge.
**What the interviewer is checking:** Whether you recompute a bridge instead of trusting the stated figure, and find the cause of the gap.
**Say this in the interview:** "The bridge gives 510, not 515. The 5 difference is exactly the net transfers (3 in, 8 out), so the report seems to have ignored transfers."
**What the data shows:** The reported closing headcount does not tie out to its own components.
**Working:**
1. Opening 500 + new hires 40 = 540.
2. Less resignations 20 and terminations 5: 540 - 25 = 515.
3. Plus transfers in 3 and less transfers out 8: 515 + 3 - 8 = 510.
4. Stated 515 minus computed 510 = 5 (that is, the net transfers of -5).
**Result:** Closing headcount is 510; the stated 515 is overstated by 5 (about 1.0%). The stated 515 is exactly the figure you get when transfers are left out, which is the likely cause but still a hypothesis to confirm, not proof.
**Caveats / what else I would check:** Transfers in a single-company headcount should usually net to zero (one person's transfer out is another's transfer in), so 3 in versus 8 out is itself suspicious: are 5 transfers out to another legal entity, or are transfers in missing from the data? Check the report's scope (one entity or a department), the same cut-off date, and the HRIS headcount on the closing date.
**Next step / recommendation:** Confirm the closing headcount from the HRIS on the closing date, find the 5 unmatched transfers, correct the report and add a bridge check to it.
**Likely follow-ups:** 1) *Which number do you trust?* The HRIS count on the date, after the transfers are explained. 2) *Does a gap of 5 matter?* At 1% it is small, but it signals a process error.
**Common mistakes / traps:** Accepting 515; forgetting the sign of the transfers; not asking why transfers do not match.

### Q43 ⭐⭐ 🟢 Quarterly sales are shown below (exercise data, in lakh). Compute the seasonal index of Q4 (Q4 divided by the quarterly average), and say how you would use it when comparing Q4 with Q1.
| Quarter | Sales |
|---|---|
| Q1 | 80 |
| Q2 | 90 |
| Q3 | 100 |
| Q4 | 130 |

**Asked at:** commonly asked (no company-specific report found); seasonal index (seasonality) is a standard part of trend discussions (unverified). Premise note: a seasonal index from one year of data is only a rough illustration.
**What the interviewer is checking:** Whether you adjust for seasonality before comparing quarters.
**Say this in the interview:** "Q4 is 1.3 times an average quarter. If that seasonal pattern is real, Q4 beating Q1 by 62.5% is mostly the season. But one year of data cannot prove the pattern."
**What the data shows:** Sales rise through the year, with Q4 the highest.
**Working:**
1. Quarterly average: (80 + 90 + 100 + 130) / 4 = 100 lakh.
2. Q4 index: 130 / 100 = 1.30.
3. Q1 index: 80 / 100 = 0.80 (and Q2 0.90, Q3 1.00; the four indices add to 4.0).
4. Raw Q4 versus Q1: 130 / 80 = 1.625, so +62.5%.
5. Seasonally adjusted: Q4 = 130/1.30 = 100; Q1 = 80/0.80 = 100.
**Result:** Q4 seasonal index is 1.30. After adjusting, Q4 and Q1 are equal at 100, so the apparent 62.5% growth would be only seasonality. Caution: with one year of data this is true by construction, because the indices are built from the same four numbers, so any real growth through the year is also counted as "season". Treat it as an illustration of the method, not a finding.
**Caveats / what else I would check:** One year is not enough to define a season, so I use at least two to three years; a trend inside the year (growth) mixes with seasonality here; promotions or festivals in Q4; year-on-year comparison (Q4 versus last Q4) avoids the problem.
**Next step / recommendation:** Compare Q4 with the previous Q4, or deseasonalise using indices from several years; build targets with the season in them.
**Likely follow-ups:** 1) *Simplest fix?* Compare the same quarter last year. 2) *What if there is a real trend?* Use a model to separate trend and season.
**Common mistakes / traps:** Comparing consecutive quarters raw; building an index from a single year without saying so.

### Q44 ⭐⭐ 🟢 A seven-day moving average of daily orders is built from the figures below (exercise data). Compute the 3-day moving average for days 3 to 5, and say what it hides.
| Day | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Orders | 90 | 120 | 60 | 150 | 90 |

**Asked at:** commonly asked (no company-specific report found); moving averages are a common smoothing topic (unverified). Premise note: the question says seven-day moving average but only five days are given, so I compute the 3-day version it asks for.
**What the interviewer is checking:** Whether you can compute a moving average and know that smoothing hides things.
**Say this in the interview:** "The 3-day averages are 90, 110 and 100. It smooths the jumpy daily numbers, but it also hides the real peaks and dips."
**What the data shows:** The daily orders jump between 60 and 150; the raw series is noisy.
**Working:**
1. Day 3: (90 + 120 + 60) / 3 = 90.
2. Day 4: (120 + 60 + 150) / 3 = 110.
3. Day 5: (60 + 150 + 90) / 3 = 100.
**Result:** 90, 110, 100 (centred on days 3, 4, 5; the first and last days have no value without the window). The raw range is 60 to 150; the smoothed range is 90 to 110.
**Caveats / what else I would check:** The average hides the single-day peaks (the 150 on day 4) and the dip on day 3, which may matter for staffing and stock. A moving average lags a real change. A seven-day window suits daily data because it covers one full weekly cycle; 3 days would blend weekday and weekend patterns. Check missing days.
**Next step / recommendation:** Show daily bars with the 7-day line over them; use the average for trend and the daily values for operations.
**Likely follow-ups:** 1) *Why 7 days?* It covers each weekday once. 2) *Trailing or centred?* Trailing for live dashboards; centred for looking back.
**Common mistakes / traps:** Reading the smoothed line as actual daily demand; picking a window that clashes with weekly patterns.

### Q45 ⭐⭐ 🟡 Revenue by region before and after a price change is shown below (exercise data, in lakh). Prices rose 10% on average. How much of the revenue change is price and how much is volume?
| Period | Revenue | Units |
|---|---|---|
| Before | 200 | 10,000 |
| After | 209 | 9,500 |

**Asked at:** commonly asked (no company-specific report found); price-volume decomposition appears in finance and e-commerce case discussions (unverified). Premise note: the table says "by region" but shows one total row per period; I treat it as a single total.
**What the interviewer is checking:** Whether you split a revenue change into price and volume effects and know the split depends on the method.
**Say this in the interview:** "Revenue rose 9 lakh. Price added about 19 lakh and lower volume took away about 10, so the price rise did the work while volume fell 5%."
**What the data shows:** Revenue up 4.5%, units down 5%, so the average price went up about 10%.
**Working:**
1. Revenue change: 209 - 200 = +9 lakh (+4.5%).
2. Price per unit before: 200 lakh / 10,000 = Rs 2,000. After: 209 lakh / 9,500 = Rs 2,200 (+10.0%).
3. Volume effect (at the old price): (9,500 - 10,000) x Rs 2,000 = -10 lakh.
4. Price effect (at the new volume): (2,200 - 2,000) x 9,500 = +19 lakh.
5. Check: -10 + 19 = +9 lakh.
**Result:** Price +19 lakh, volume -10 lakh, net +9 lakh. Another ordering (price at old volume +20, volume at new price -11) gives a slightly different split; the difference is the interaction (about 1 lakh).
**Caveats / what else I would check:** The change in average price may include mix (customers shifting between cheaper and pricier items), so it is not all list price; elasticity (volume loss of 5% for a 10% price rise); whether the loss of volume is permanent; the profit effect after cost.
**Next step / recommendation:** Say whether the price rise is worth it in margin terms; monitor volume for several weeks; do the split by product or region to see where customers left.
**Likely follow-ups:** 1) *Why does the split differ by method?* The interaction term goes to one side or the other. 2) *Is the price rise a success?* Revenue is up, but check margin, churn and customer loss.
**Common mistakes / traps:** Saying "price effect is 10% so 20 lakh" with no volume; ignoring mix; forgetting the method.

### Q46 ⭐⭐ 🟡 A mix-shift table is shown below (exercise data). Overall average order value fell even though each category's AOV is flat. Explain this and compute the overall AOV for each month.
| Category | AOV | Jan orders | Feb orders |
|---|---|---|---|
| Electronics | 2,000 | 1,000 | 600 |
| Accessories | 400 | 1,000 | 1,400 |

**Asked at:** commonly asked (no company-specific report found); mix shift (a Simpson-style effect) is a recurring interpretation theme (unverified).
**What the interviewer is checking:** That you know a blended average moves when the mix changes even if each part is flat.
**Say this in the interview:** "Nothing got cheaper. The share of low-value accessory orders grew, so the blended AOV fell from Rs 1,200 to Rs 880."
**What the data shows:** Each category's AOV (average order value) is flat; accessories orders rose, electronics orders fell.
**Working:**
1. Jan orders: 1,000 + 1,000 = 2,000; revenue 1,000 x 2,000 + 1,000 x 400 = 24,00,000 (Rs 24 lakh).
2. Jan AOV: 24,00,000 / 2,000 = Rs 1,200.
3. Feb orders: 600 + 1,400 = 2,000; revenue 600 x 2,000 + 1,400 x 400 = 17,60,000 (Rs 17.6 lakh).
4. Feb AOV: 17,60,000 / 2,000 = Rs 880.
5. Electronics' share of orders fell from 50% to 30%.
**Result:** AOV fell from Rs 1,200 to Rs 880 (-26.7%) because of mix, with total orders unchanged at 2,000. Revenue fell 26.7% too (Rs 24 lakh to Rs 17.6 lakh).
**Caveats / what else I would check:** Why did the mix shift (a promotion on accessories, a stock-out of electronics, new channel)? Is it a seasonal pattern? Is revenue the right outcome, rather than margin (accessories can have a higher margin)? Check the AOV by category stayed flat for real (not rounded).
**Next step / recommendation:** Report AOV by category alongside the blended AOV and the order mix; find the cause of the fall in electronics orders.
**Likely follow-ups:** 1) *Is this Simpson's paradox?* It is the same idea (mix drives the total); a strict reversal needs the trend to flip within segments. 2) *What would you chart?* A stacked bar of orders by category beside AOV.
**Common mistakes / traps:** Blaming price or customers; reading the blended AOV alone; ignoring volume mix.

### Q47 ⭐⭐ 🟡 A cohort chart shows that day-30 retention improved from 18% to 22% after an app release. What else could explain this, and how would you test it?
**Asked at:** commonly asked (no company-specific report found); cohort-retention reading appears on practice-question sites (unverified).
**What the interviewer is checking:** Whether you treat "after the release" as a correlation and know how to separate the release from other causes.
**Say this in the interview:** "Retention is up 4 percentage points, about 22% relative, but 'after' is not 'because of'. I would first check who was in each cohort, then use a holdout or staged rollout to test the release itself."

**What the data shows:** Day-30 retention (the share of a signup cohort still active on day 30) moved from 18% to 22%.
**Working:**
1. Absolute change = 22 - 18 = 4 percentage points.
2. Relative change = 4 / 18 = 22.2%.
3. Illustrative size check: if each cohort had 2,000 users, the 95% interval for the 4-point gap is about +1.5 to +6.5 points (standard error 1.26 points). With only 200 users each, the gap would be too noisy to trust.
**Result:** +4 percentage points (+22% relative). The size of the cohorts decides whether that is signal or noise.
**Caveats / what else I would check:**
1. Mix: did the acquisition channel, country, device or paid-versus-organic share change? A better user mix lifts retention with no product change.
2. Seasonality or events: a festival, exam season or a competitor's outage.
3. Definition: did "active" or the day-30 window change, or are the new cohorts still maturing (incomplete day-30 data)?
4. Other changes shipped at the same time (onboarding emails, pricing, a bug fix).
5. Novelty effect: a new feature can lift early retention and then fade.
**Next step / recommendation:** Best test is a randomised holdout: release to 90% of new users, hold back 10%, compare day-30 retention. If that is not possible, compare the same segments before and after (channel by channel, platform by platform), and look at the same weeks last year. Report the lift with a range.
**Likely follow-ups:** 1) Why not just compare before and after? Anything else that changed gets credited to the release. 2) What if the release was already 100% live? Use staggered rollout by platform or region as a natural experiment, or a before/after with controls.
**Common mistakes / traps:** Calling it "+4%" instead of 4 percentage points; reading the newest cohort before day 30 has passed; ignoring cohort size.

### Q48 ⭐⭐ 🟡 A salary table shows compa-ratios (salary divided by grade midpoint) by tenure band (exercise data). What does it say, and what would you check before recommending corrections?
| Tenure band | Employees | Avg compa-ratio |
|---|---|---|
| 0-1 yrs | 80 | 1.05 |
| 1-3 yrs | 120 | 0.98 |
| 3-5 yrs | 90 | 0.92 |
| 5+ yrs | 60 | 0.90 |

**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you spot pay compression (new hires paid more than long-serving staff) and look for explanations before proposing money.
**Say this in the interview:** "The longer someone has stayed, the lower they sit against their grade midpoint, from 1.05 for new joiners to 0.90 for five-plus years. That looks like pay compression, but I would check grade mix and performance before recommending any correction."

**What the data shows:** Compa-ratio of 1.00 means paid exactly at the grade midpoint. It falls steadily with tenure, so the newest people are paid above midpoint and the most experienced below it.
**Working:**
1. Headcount = 80 + 120 + 90 + 60 = 350.
2. Employee-weighted average compa-ratio = 0.967 (about 3% below midpoint overall).
3. Gap between newest and longest-serving bands = 1.05 - 0.90 = 0.15, which is 15 points of midpoint.
4. Cost lens: lifting a 0.90 person to 1.00 is a raise of 1.00 / 0.90 - 1 = 11.1%; for 0.92 it is 8.7%.
**Result:** Average compa-ratio 0.97 overall; tenure and pay position move in opposite directions (0.90 to 1.05).
**Caveats / what else I would check:**
1. Grade mix: are long-tenured people in higher grades where midpoints are set differently, or in different job families?
2. Performance and skills: low compa-ratio may be justified for some people.
3. Market: new joiners may be hired at the market rate, which has risen faster than internal pay.
4. Averages hide spread: look at the median and the share below 0.85 in each band.
5. Location, gender and data errors in the grade midpoint table.
**Next step / recommendation:** Build a list of employees below, say, 0.90 with rating, grade and time since last raise; prioritise high performers; cost the options for the next cycle with Finance. Do not apply a blanket correction from a band average.
**Likely follow-ups:** 1) Does low compa-ratio mean underpaid? Not by itself; it needs performance and market context. 2) Which people are the flight risk? Compare compa-ratio with attrition by band.
**Common mistakes / traps:** Treating the average as a rule for every individual; ignoring grade mix; forgetting the budget impact.

### Q49 ⭐⭐ 🟡 Attrition by tenure bucket is shown below (exercise data). Where is the problem concentrated, and what question would you ask the business next?
| Tenure | Employees at start | Leavers |
|---|---|---|
| < 1 year | 200 | 56 |
| 1-3 years | 400 | 48 |
| 3+ years | 400 | 16 |

**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you compare rates, not counts, and ask the next useful "why" question.
**Say this in the interview:** "The problem is in the first year: 28% leave, against 12% and 4% in the other groups. I would ask why new joiners leave, and whether it is hiring quality, onboarding or role mismatch."

**What the data shows:** Attrition falls sharply as tenure rises.
**Working:**
1. Rates: under 1 year = 56 / 200 = 28.0%; 1-3 years = 48 / 400 = 12.0%; 3+ years = 16 / 400 = 4.0%.
2. Total = 120 leavers out of 1,000 = 12.0% overall.
3. Concentration: the under-1-year group is 200 / 1,000 = 20% of staff but 56 / 120 = 46.7% of leavers.
4. Counts alone would show 1-3 years (48) and 3+ years (16) as milder; the rate view shows the gap is far bigger than the counts suggest.
**Result:** First-year attrition 28% versus 12% overall; the under-1-year group is 20% of staff but 47% of leavers (rounded).
**Caveats / what else I would check:**
1. Denominator: "employees at start" ignores people who joined during the year and left before year-end, so first-year attrition may be understated.
2. Tenure bucket is taken at start or at exit? State it, because people move buckets during the year.
3. Voluntary versus involuntary exits (probation terminations are a hiring problem, resignations an experience problem).
4. Split by hiring source, manager, department and joining month.
**Next step / recommendation:** Ask the business: "Are first-year exits resignations or terminations, and in which teams and sources are they concentrated?" Then review onboarding, the job preview and probation feedback; track 90-day and 180-day exit rates monthly.
**Likely follow-ups:** 1) What is a good attrition rate? It depends on industry and role, so compare with your own history and peers (confirm benchmarks). 2) Would you act on 3+ years at 4%? Not first; look at who the 16 are (key talent).
**Common mistakes / traps:** Quoting leaver counts without headcount; using average headcount for one bucket and starting headcount for another; jumping to "bad onboarding" before checking exit types.

### Q50 ⭐⭐ 🟡 An accounts-receivable ageing table is shown below (exercise data, in lakh). What is the share overdue by more than 60 days, and what would you flag?
| Bucket | Amount |
|---|---|
| 0-30 days | 120 |
| 31-60 days | 50 |
| 61-90 days | 20 |
| 90+ days | 10 |

**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can compute shares from an ageing table and think about collection risk, not just arithmetic.
**Say this in the interview:** "Receivables total 200 lakh and 30 lakh, 15%, is more than 60 days old. The older the bill, the less likely it is paid, so I would look at the 90-plus bucket by customer and at what is about to roll into it."

**What the data shows:** "Ageing" means how long each unpaid invoice has been outstanding. Most of the money is recent, with a tail of older amounts.
**Working:**
1. Total outstanding = 120 + 50 + 20 + 10 = 200 lakh.
2. More than 60 days = 20 + 10 = 30 lakh, so 30 / 200 = 15.0%.
3. Shares by bucket: 60%, 25%, 10%, 5% (90+ days is 5%).
4. The 31-60 bucket (50 lakh, 25%) is next month's 61-90 bucket if not collected.
**Result:** 15% of receivables (30 lakh) is more than 60 days old; 5% (10 lakh) is over 90 days.
**Caveats / what else I would check:**
1. Credit terms: if terms are 45 days, "overdue" begins earlier than 60 days; this table is by age, not by due date.
2. Concentration: is the 30 lakh one or two customers? Is any a disputed invoice?
3. Trend: compare with last month and the same month last year; one snapshot says little.
4. Billing timing: large invoices raised on the last day inflate the 0-30 bucket.
5. Provisioning: Finance decides on bad-debt allowances; I only flag.
**Next step / recommendation:** Flag the 61+ days list by customer and owner to Finance and Sales; chase the 31-60 bucket now; track days sales outstanding (receivables divided by sales times days) monthly.
**Likely follow-ups:** 1) What is DSO? Average days to collect payment. 2) Who acts? Collections and account managers, with Finance.
**Common mistakes / traps:** Using only the 90+ bucket and missing the rolling 31-60 bucket; treating all customers as equal; forgetting credit terms.

### Q51 ⭐⭐ 🟡 The table below shows customer revenue concentration (exercise data). What is the share of the top five customers, and what is the business implication?
| Customer | Revenue (lakh) |
|---|---|
| C1 | 40 |
| C2 | 30 |
| C3 | 25 |
| C4 | 20 |
| C5 | 15 |
| Other 45 customers | 70 |

**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you compute shares correctly and link concentration to risk.
**Say this in the interview:** "The top five customers bring 130 of 200 lakh, 65% of revenue. Losing C1 alone would take 20%, so the business is exposed to a few relationships."

**What the data shows:** A small group of customers generates most of the revenue; the remaining 45 customers are small.
**Working:**
1. Top five = 40 + 30 + 25 + 20 + 15 = 130 lakh.
2. Total = 130 + 70 = 200 lakh across 50 customers (5 + 45).
3. Top-five share = 130 / 200 = 65.0%; the 45 others = 35.0%.
4. C1 alone = 40 / 200 = 20%; top three = 95 / 200 = 47.5%.
5. Average revenue: top five = 26 lakh each; the other 45 = 70 / 45 = about 1.6 lakh each.
6. C1 (40 lakh) is worth about 26 average small customers (40 / 1.56); the average top-five customer is worth about 17.
**Result:** Top five = 65% of revenue (C1 = 20%). C1 alone equals roughly 26 of the small customers.
**Caveats / what else I would check:**
1. Time period and whether it is revenue or profit; a big customer may be low margin.
2. Contracts: length, renewal dates, pricing power, any exclusivity.
3. Is it one year only? Check last three years for stability and whether concentration is rising.
4. Parent groups: C2 and C3 may belong to the same group, which raises concentration.
**Next step / recommendation:** Present it as a risk: set a limit (for example no single customer above 15 to 20% target; the threshold is a management choice), build account plans for the top five, and grow the long tail. Track the top-five share quarterly.
**Likely follow-ups:** 1) Is concentration always bad? It can mean efficient large accounts, but the downside risk is high. 2) What chart? A Pareto chart (bars plus cumulative line).
**Common mistakes / traps:** Counting the "Other" line as one customer; calling 65% "too high" without context; ignoring profit.

### Q52 ⭐⭐ 🟡 Agent-level CSAT is shown below (exercise data). Agent D has the highest score. Would you reward them, and what else do you check?
| Agent | Surveys | CSAT |
|---|---|---|
| A | 120 | 4.2 |
| B | 150 | 4.3 |
| C | 90 | 4.1 |
| D | 4 | 5.0 |

**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you notice small sample size before ranking people.
**Say this in the interview:** "No, not on this evidence. Agent D's 5.0 rests on four surveys, so one more response could move it a lot. I would wait for more surveys and look at other measures too."

**What the data shows:** Three agents have 90 to 150 responses and scores between 4.1 and 4.3; D tops the table with only 4 responses.
**Working:**
1. Average of A, B, C (weighted by surveys) = (120 x 4.2 + 150 x 4.3 + 90 x 4.1) / 360 = 4.22. Including D: 4.23 (D adds almost nothing).
2. Uncertainty: assume (illustratively) a spread of 0.8 points between responses. The standard error is about 0.8 / sqrt(4) = 0.40 for D, against about 0.07 for B (0.8 / sqrt(150)). D's 5.0 could easily be a true 4.4.
3. Adjusting D toward the average (give the team average 30 "virtual surveys" of weight; illustrative method): (4 x 5.0 + 30 x 4.23) / 34 = about 4.32, not clearly above B's 4.3.
**Result:** D's lead is not reliable; with 4 responses the adjusted score is about 4.3, in line with B.
**Caveats / what else I would check:**
1. How surveys are sent: only after resolved tickets or only to happy customers (response bias)?
2. Ticket mix: D may handle easy tickets.
3. Other measures: resolution rate, handling time, quality audits, re-opened tickets.
4. Survey count per agent over three months, not one week.
**Next step / recommendation:** Rank only agents above a minimum survey count (for example 30; a rule of thumb), show confidence intervals, and base recognition on several metrics.
**Likely follow-ups:** 1) What minimum sample? It depends on spread; 30 or more is a common starting point. 2) Why is CSAT biased? Only some customers respond.
**Common mistakes / traps:** Ranking on the raw average; treating a small team's survey score as performance.

### Q53 ⭐⭐ 🟡 A histogram of order delivery times shows two peaks, one around 20 minutes and one around 55 minutes. What might cause this, and what would you do before reporting the average?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you recognise two populations hidden in one average.
**Say this in the interview:** "Two peaks mean two different kinds of orders mixed together. I would find what separates them and report each group, because one average, around the middle, describes almost nobody."

**First, clarify / contain:** Ask how delivery time is defined (order placed to delivered, or dispatch to delivered) and the period covered. Do not publish the overall average yet.
**What I would check, in order:**
1. Split the data by candidate causes: distance or zone, restaurant or warehouse, delivery partner type, hour of day, weekday versus weekend, weather days.
2. Check for two operating modes, such as express versus standard, or pre-ordered versus instant orders.
3. Check timestamp quality: two systems recording different events, or missing "delivered" times filled by default.
4. Draw one histogram per segment; see which split pulls the peaks apart.
5. Calculate the share of orders in each peak and the median per segment.
**If I find...:** A clean business split (for example far zones): report both segments with separate targets. A data problem (mixed definitions): fix the definition first. Peak hours only: staffing issue, show by hour.
**What I would tell the stakeholder:** "Delivery times are not one pattern. About 60% of orders arrive near 20 minutes and about 40% near 55 minutes (illustrative split); a single average of about 34 minutes describes neither. I am checking what separates the groups and will report each, in two days."
**Prevent it next time:** Report medians and percentiles by segment; keep a standard timestamp definition.
**Likely follow-ups:** 1) Which metric to report? Median and 90th percentile per segment. 2) Is the mean wrong? It is correct arithmetic but meaningless here.
**Common mistakes / traps:** Reporting a single average; assuming the second peak is "bad data" without checking; mixing segments of different size.

### Q54 ⭐⭐ 🟡 A heat map shows support tickets by weekday and hour. How would you turn it into a staffing recommendation, and what caveats apply?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you move from "busy times" to workload and agents needed, with realistic caveats.
**Say this in the interview:** "I would convert ticket counts into workload hours, add allowances for breaks and leave, and propose shifts that follow the pattern. A heat map is a starting point, so I would check it over several weeks."

**Clarify first:** What decision is it: shift rosters, hiring, or an outsourcing contract? What service level (for example, 80% answered within 2 minutes) does the team target?
**Plan:**
1. Use at least 8 to 12 weeks of data, averaged by weekday and hour, and mark holidays and campaign days.
2. Convert tickets to workload: tickets per hour x average handling time. Example (illustrative): 120 tickets x 6 minutes = 720 minutes = 12 agent-hours per hour.
3. Add occupancy: agents cannot be 100% busy; at 80% target occupancy, 12 / 0.8 = 15 agents on the desk.
4. Add shrinkage (leave, breaks, training, absence), say 30%: 15 / 0.7 = about 22 rostered agents.
5. Compare with the current roster hour by hour; propose staggered shifts to match peaks.
**Method choice and why:** Start with simple workload arithmetic. For tight service levels use a queueing model (Erlang C) or ask a workforce-planning tool; confirm assumptions with operations.
**Pitfalls:** Ticket arrival times are not the same as when work occurs (backlog); a few outlier days; different channels (chat, email, calls) with different handling times; tickets rising over time; averages hide spikes; arrival pattern changes after releases.
**Deliverable:** A one-page table of recommended agents by weekday and hour, the assumptions, the service-level result, and the cost of the change, with a plan to review after a month.
**Likely follow-ups:** 1) Staff for the peak? Not always; use flexible shifts or part-timers. 2) How do you validate? Compare the new roster's actual wait times.
**Common mistakes / traps:** Staffing by tickets without handling time; ignoring shrinkage; using one week of data.

### Q55 ⭐⭐ 🟡 Two dashboards show the same metric with different trends: one uses daily data and one uses a seven-day moving average. Which do you show to leadership, and why?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand smoothing, lag and what each view is for.
**Say this in the interview:** "Both are correct, they answer different questions. For leadership I show the seven-day average as the trend, with the daily line faintly behind it, and I label which is which."

**What the data shows:** Daily data is noisy: weekday and weekend patterns, one-off spikes. A seven-day moving average (the average of the latest 7 days) removes the weekly cycle and shows direction, but reacts late.
**Working:**
1. Seven days always include each weekday once, so weekday effects cancel out.
2. A trailing 7-day average lags a turning point by about 3 days (the middle of the window), so a sudden drop appears late and softened.
3. A daily chart shows the true size of spikes and the exact day of an event but can look like a trend when it is only noise.
**Result:** Show the smoothed line for trend, daily for events.
**Caveats / what else I would check:** Whether the two dashboards truly use the same data and definitions (not only different smoothing); holiday weeks that distort the window; a partly loaded last day. Smoothed numbers should never be added or averaged as if they were raw days.
**Next step / recommendation:** Put the moving average on the main chart, daily values in a drill-down, mark releases and campaigns, and write "7-day average" in the title. For fast-moving issues (outages, fraud) add a daily alert.
**Likely follow-ups:** 1) What window size? Seven for weekly cycles; match the business rhythm. 2) What do you tell people if the lines disagree? Daily shows the event, the average shows the direction.
**Common mistakes / traps:** Not labelling the smoothing; comparing a smoothed line with a raw one without saying so; using the average to find the date of an event.

### Q56 ⭐⭐ 🟡 Performance ratings by manager are shown below (exercise data). What does the table suggest about the rating process, and what should HR do?
| Manager | Team size | Rated 5 | Rated 4 | Rated 3 | Rated 2 |
|---|---|---|---|---|---|
| M1 | 10 | 6 | 3 | 1 | 0 |
| M2 | 12 | 1 | 4 | 6 | 1 |
| M3 | 8 | 2 | 3 | 3 | 0 |

**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you spot rating leniency and strictness between managers and propose a fair process step without accusing anyone.
**Say this in the interview:** "M1 gave 90% of the team a 4 or 5, M2 only 42%. Teams may differ, but this gap suggests managers rate on different scales, so I would run a calibration before ratings drive pay or promotion."

**What the data shows:** The rows add up to the team sizes (10, 12, 8; 30 employees). Nobody was rated 1.
**Working:**
1. Top-two share (rated 4 or 5): M1 = 9 / 10 = 90%; M2 = 5 / 12 = 41.7%; M3 = 5 / 8 = 62.5%. Company: 19 / 30 = 63.3%.
2. Average rating: M1 = 4.50; M2 = 3.42; M3 = 3.88.
3. Rated 5 only: M1 = 60%; M2 = 8.3%; M3 = 25%.
4. A quick significance check on M1 versus M2 (top-two share, Fisher exact test, which asks how often a gap this big would appear by chance between two equal teams) gives p of about 0.03, but with 10 and 12 people, and chosen after looking, treat it as a flag, not proof.
**Result:** M1's team averages 4.50 and M2's 3.42, a gap of 1.08 rating points.
**Caveats / what else I would check:**
1. Real team differences: seniority, role, and the work they do.
2. Objective measures (targets achieved, quality) to see if M1's team genuinely delivered more.
3. The same managers' ratings in earlier years (consistent leniency?).
4. Small teams: one person changes a percentage a lot.
5. Whether a forced distribution or guideline exists.
**Next step / recommendation:** Hold a calibration session where managers justify ratings with evidence, compare ratings to objective results, share the distribution guideline, and re-check after the cycle. Do not blindly force a curve.
**Likely follow-ups:** 1) Does M1 rate too high? Possibly; we need evidence, not assumption. 2) Fix? Calibration and clear rating criteria.
**Common mistakes / traps:** Calling a manager biased from one cycle; ignoring team differences; forgetting the pay impact on employees.

### Q57 ⭐⭐ 🟡 Returns and revenue by seller are shown below (exercise data). Which seller would you escalate first, and why is the return rate alone not enough?
| Seller | Orders | Returns | Revenue (lakh) |
|---|---|---|---|
| S1 | 50 | 10 | 0.5 |
| S2 | 5,000 | 400 | 60 |
| S3 | 1,200 | 180 | 18 |

**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you weigh rate, volume and money together instead of one ratio.
**Say this in the interview:** "S1 has the highest return rate at 20% but only 50 orders. S3 has 15% on 1,200 orders and about 2.7 lakh of returned revenue, so I would escalate S3 first, and keep an eye on S2 for its size."

**What the data shows:** Three different sizes of seller, so a rate alone misleads.
**Working:**
1. Return rates: S1 = 10 / 50 = 20.0%; S2 = 400 / 5,000 = 8.0%; S3 = 180 / 1,200 = 15.0%.
2. Share of all 590 returns: S1 1.7%; S2 67.8%; S3 30.5%.
3. Revenue per order: S1 = Rs 1,000; S2 = Rs 1,200; S3 = Rs 1,500.
4. Returned revenue (assuming returned orders are average value): S1 = 20% x 0.5 = 0.1 lakh; S2 = 8% x 60 = 4.8 lakh; S3 = 15% x 18 = 2.7 lakh.
5. Uncertainty (a 95% Wilson interval is the range in which the true return rate plausibly lies, given only this many orders): S1 11% to 33% (wide); S2 7.3% to 8.8%; S3 13.1% to 17.1% (S3 is clearly above S2).
**Result:** S3 is the sharpest problem (15% on a meaningful volume). S2 holds the most returned money (4.8 lakh) but its rate is the lowest. S1 is too small to judge.
**Caveats / what else I would check:**
1. Why they return: wrong size, damage, quality, fake listing (reasons by seller).
2. Product category: S3 may sell clothing, which has naturally high returns.
3. Time window and refund costs (shipping both ways).
4. Fraud signals on S1.
**Next step / recommendation:** Escalate S3 with return reasons by SKU; review S2's absolute loss; set a rule that sellers need a minimum order count before they are ranked.
**Likely follow-ups:** 1) Why not S1? Only 10 returns; the rate could be chance. 2) What other metric? Return cost per order.
**Common mistakes / traps:** Escalating the highest rate without volume; ignoring category mix.

### Q58 ⭐⭐ 🟡 A line chart shows a steady rise in monthly active users. You find that the definition of active changed in month 7. How do you handle the chart and how do you tell the stakeholder?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you protect comparability and communicate a definition break openly.
**Say this in the interview:** "I would stop showing it as one continuous line. Either I recompute months 1 to 6 under the new definition, or I show a clear break with both definitions side by side, and tell the stakeholder that part of the rise is definitional."

**First, clarify / contain:** Confirm exactly what changed (for example, 'any login' became 'one meaningful action') and the date. Do not publish the old chart or quote the growth rate until this is settled.
**What I would check, in order:**
1. Can the new definition be rebuilt for earlier months from raw event data?
2. For month 7 (or the overlap period), compute both definitions to measure the step change: ratio of new to old.
3. Check whether the trend within each definition still rises.
4. Check who else uses the old chart (dashboards, board decks).
**If I find...:** Restatement possible: redraw the whole series on the new definition and note it. Not possible: show two lines with a visible break and an annotation. The rise exists under both: say so. Only the change created the rise: say the trend is flat.
**What I would tell the stakeholder:** "The active-user definition changed in month 7, so months before and after are not comparable. On the same definition, users grew X% (to be confirmed); the rest of the apparent rise is the definition. I will send the restated chart by Thursday."
**Prevent it next time:** A metric dictionary with version dates, a change log on every KPI, and a rule to recompute history or mark a break when definitions change.
**Likely follow-ups:** 1) Why not keep the old line going? It is not the same metric. 2) Annotation? Add a vertical line and a note.
**Common mistakes / traps:** Silently splicing two definitions into one line; blaming the data team instead of explaining.

### Q59 ⭐⭐ 🟡 A table compares sales in November this year against October (exercise data show a 25% increase). What is wrong with this comparison, and what comparison would you make?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you recognise seasonality and unequal period lengths.
**Say this in the interview:** "October to November mixes real growth with season, festival timing and different day counts. I would compare November with last November, adjusted for events."

**What the data shows:** Sales are 25% higher in November than in October (exercise figure).
**Working:**
1. Month length: October has 31 days and November 30. Sales per day grow by 1.25 x 31 / 30 = 1.2917, which is 29.2%, a little more than the headline.
2. Festival timing: if a major festival or sale falls in November this year but fell in October last year, a month-on-month comparison credits the season.
3. Day mix: different numbers of weekends and paydays.
4. Better comparison: November this year versus November last year (year on year), adjusted for events such as the shifted festival date, plus the average daily sales for like-for-like periods.
**Result:** 25% is not a clean growth figure; per day it is about 29%, but season probably explains much of it.
**Caveats / what else I would check:** Last year's October-to-November change (the normal seasonal lift); stock-outs or campaigns in either month; whether the full month is closed; business growth overall.
**Next step / recommendation:** Present: (1) year-on-year growth for November, (2) the seasonal index (typical November divided by typical October) and growth over that, (3) daily averages.
**Likely follow-ups:** 1) Is month-on-month ever useful? Yes, for short-term momentum if seasonality is removed. 2) Which season index? The average ratio over several years.
**Common mistakes / traps:** Announcing 25% growth to leadership; ignoring the number of days and festival dates.

### Q60 ⭐⭐ 🟡 A regression output on salary versus tenure is shown below (exercise data). Interpret the coefficient and R-squared in plain words, and say what you would not conclude.
| Term | Estimate | Std error |
|---|---|---|
| Intercept | 4.5 | 0.4 |
| Tenure (years) | 0.6 | 0.1 |

R-squared = 0.30, n = 220
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can read a regression in plain words and avoid causal or over-precise claims.
**Say this in the interview:** "On average, each extra year of tenure goes with about 0.6 lakh higher salary, and tenure explains about 30% of the differences in pay. It is a pattern, not a rule, and I would not say tenure causes the pay."

**What the data shows:** A fitted line: salary = 4.5 + 0.6 x tenure (units not stated; I assume salary is in lakh per year).
**Working:**
1. Intercept 4.5: predicted salary at zero years of tenure.
2. Slope 0.6: each extra year goes with about 0.6 higher; predictions: 5 years = 4.5 + 3.0 = 7.5; 10 years = 4.5 + 6.0 = 10.5.
3. Reliability: the t value (estimate divided by its standard error, which says how many "wobbles" the slope is away from zero) is 0.6 / 0.1 = 6; the approximate 95% range for the slope is 0.60 +/- 0.20, so 0.40 to 0.80. Tenure is clearly related to salary.
4. R-squared 0.30: tenure accounts for 30% of the variation in salary; 70% is due to other things (grade, role, performance, location, market). The correlation is the square root, about 0.55.
**Result:** About 0.6 lakh extra per year of tenure on average; R-squared 0.30.
**Caveats / what else I would check:** Residual plot (are errors larger at high salaries?); outliers such as executives; non-straight relationship (pay may flatten after some years); grade and job family as extra variables; n = 220 only; the model describes this group, not every company.
**Next step / recommendation:** Add grade, role and performance and see how the tenure effect shrinks; use the model to flag employees far below predicted pay, then review them individually.
**Likely follow-ups:** 1) Is 0.30 low? It leaves 70% unexplained; I would expect grade to explain a lot more of pay, but I would test that rather than assume. 2) Does tenure cause pay? Possibly through raises, but this does not prove it.**Common mistakes / traps:** "Tenure explains 30% of salary" (it is of the variation, not of the amount); causal language; extrapolating to 30 years.

### Q61 ⭐⭐ 🟡 Support tickets per thousand orders are shown by quarter (exercise data). Raw tickets rose 40% but orders rose 60%. What is the change in the rate, and which framing would you present?
| Quarter | Orders | Tickets |
|---|---|---|
| Q1 | 50,000 | 2,500 |
| Q2 | 80,000 | 3,500 |

**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you normalise for volume and present the right framing.
**Say this in the interview:** "Tickets rose 40% but orders rose 60%, so tickets per thousand orders fell from 50 to 43.75, a 12.5% improvement. I would lead with the rate, and show the raw count too."

**What the data shows:** Both volumes grew, orders faster than tickets.
**Working:**
1. Q1 rate = 2,500 / 50,000 x 1,000 = 50.0 tickets per thousand orders.
2. Q2 rate = 3,500 / 80,000 x 1,000 = 43.75.
3. Change = 43.75 - 50 = -6.25 tickets per thousand, which is -12.5% (6.25 / 50).
4. Check: raw tickets +1,000 (+40%); orders +30,000 (+60%); 1.40 / 1.60 = 0.875, which is -12.5%.
**Result:** Rate fell from 50.0 to 43.75 per thousand orders (-12.5%, or -6.25 per thousand).
**Caveats / what else I would check:** Tickets lag orders (a ticket may arrive days after the order), so use cohorts by order date; ticket types (are new tickets about delivery or product?); order mix (new categories); the workload still grew by 1,000 tickets, so staffing needs rise.
**Next step / recommendation:** Show the rate as the quality measure and the count as the workload measure side by side: "quality improved, volume still grows, so plan capacity." Track by month and issue category.
**Likely follow-ups:** 1) Which is better to report? Both, with different purposes. 2) Why would the rate fall? Better product, fewer issues, or lag.
**Common mistakes / traps:** Reporting "tickets up 40%" with no context; subtracting percentages (40 - 60); forgetting the time lag.

### Q62 ⭐⭐ 🟡 A year-on-year comparison shows December sales up 40% over last December, but last December had a stock-out for two weeks. How do you describe the growth?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you recognise a distorted base and give a fair, honest growth story.
**Say this in the interview:** "The 40% is real arithmetic but flattered by a weak base. I would estimate what last December would have been without the stock-out and report both numbers."

**What the data shows:** The comparison base (last December) was depressed by two weeks of lost sales, so the growth looks larger than underlying demand growth.
**Working:**
1. Reported growth = 40% (this December = 1.40 x last December).
2. Illustrative normalisation: say last December was 100 with the stock-out and about 130 without it, estimated from the November run-rate and in-stock days (an assumption to be agreed with the business).
3. This December = 140, so growth on the normalised base = 140 / 130 - 1 = 7.7%.
4. Another check: sales per in-stock day, or growth versus two years ago.
**Result:** "40% reported, about 8% underlying (illustrative estimate; method and range to be shared)".
**Caveats / what else I would check:** How the lost sales were estimated (a range, not a point); whether customers bought later (recovered sales) or left; whether this December had its own campaigns or stock issues.
**Next step / recommendation:** Say: "December sales are 40% above last year, though last year's base was reduced by a two-week stock-out; adjusted for that, growth is roughly 8% (estimate)". Document the assumption, and also give two-year growth.
**Likely follow-ups:** 1) Why not just report 40%? It overstates demand growth. 2) How certain is the estimate? Give a range and the method.
**Common mistakes / traps:** Celebrating 40%; presenting an adjusted number as exact; not telling the stakeholder about the stock-out.

### Q63 ⭐⭐ 🟡 Revenue per head by team is shown below (exercise data). Compute each team's revenue per head, and say why this might be an unfair comparison.
| Team | Revenue (lakh) | Headcount | Type |
|---|---|---|---|
| Enterprise | 900 | 15 | Long cycle |
| SMB | 600 | 30 | Short cycle |
| Inside sales | 400 | 20 | Short cycle |

**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you compute simple ratios and challenge comparisons of unlike teams.
**Say this in the interview:** "Enterprise is 60 lakh per head against 20 for the other two, but the teams sell different things on different cycles, so I would compare each against its own target and history."

**What the data shows:** Enterprise has the highest revenue per head by a wide margin.
**Working:**
1. Enterprise = 900 / 15 = 60 lakh per head.
2. SMB = 600 / 30 = 20 lakh per head.
3. Inside sales = 400 / 20 = 20 lakh per head.
4. Overall = 1,900 / 65 = about 29.2 lakh per head.
**Result:** 60, 20 and 20 lakh per head (company 29.2).
**Caveats / what else I would check:**
1. Sales cycle: Enterprise revenue this year may come from deals started last year, so the revenue is not this year's effort.
2. Deal size and customer type are different; compare each team with its own quota.
3. Headcount: includes managers, support and new hires still ramping up?
4. Territory, lead quality and who gets the leads.
5. Revenue versus profit: Enterprise may need heavy discounting and cost.
**Next step / recommendation:** Compare attainment against target, win rate, cost of sales per rupee, and the trend over four quarters; use revenue per head only within similar teams.
**Likely follow-ups:** 1) Better metric? Quota attainment. 2) Is revenue per head useless? No, it helps for capacity planning within a team type.
**Common mistakes / traps:** Ranking teams on one ratio; using year-end headcount for a team that hired late.

### Q64 ⭐⭐ 🟡 A table shows the average time-to-fill for open requisitions of 38 days, but the median is 24 days. What do you conclude, and what would you chart?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you read the gap between mean and median as skew and choose the right summary and chart.
**Say this in the interview:** "The mean is well above the median, so a few very long requisitions pull it up. The typical requisition fills in about 24 days; I would show the distribution and report the median with a 90th percentile."

**What the data shows:** Mean 38 versus median 24 means the distribution is skewed right: most requisitions close quickly and a few take very long.
**Working:**
1. Illustration (not the real data): nine requisitions at 24 days and one at 164 days give a mean of (9 x 24 + 164) / 10 = 38 and a median of 24.
2. So one stale requisition can account for the 14-day gap between mean and median.
3. The mean is accurate for total effort but not for "typical".
**Result:** Typical time-to-fill is about 24 days (median); the 38-day average is inflated by a long tail.
**Caveats / what else I would check:** The data says "open requisitions", so these are still unfilled and their final times are unknown (the numbers will grow); check whether closed requisitions were used; on-hold or forgotten requisitions that were never cancelled; senior or niche roles that naturally take longer; Q-end spikes.
**Next step / recommendation:** Chart: a histogram or box plot of days open, by role level; a table of the oldest 10 open requisitions; report median and 90th percentile for closed requisitions separately from the age of open ones. Clean up stale requisitions with owners.
**Likely follow-ups:** 1) Which number goes to leadership? Median, plus the tail. 2) What if the median also rises? Look at the pipeline stage where delays happen.
**Common mistakes / traps:** Reporting only the mean; mixing open and closed requisitions; deleting the long ones as "outliers" without asking.

### Q65 ⭐⭐ 🟡 A pivot table shows subtotals and grand totals, and a stakeholder copies the totals column into a new chart that counts them twice. How do you spot and prevent this kind of mistake?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you have habits that catch double counting before a chart goes out.
**Say this in the interview:** "I reconcile the chart's total to the source before sharing, and I build charts from the detail rows or a PivotChart, never from a copied range that includes subtotals."

**First, clarify / contain:** Ask which chart and where it was shared; pause its circulation until checked. Do not just delete the chart, as someone may have used it.
**What I would check, in order:**
1. Compare the sum of the chart's data with the pivot grand total; if the chart's sum is about double, totals are inside.
2. Look for rows or labels called "Total", "Subtotal" or "Grand Total" in the chart's legend or axis.
3. Illustration: three regions 100 + 120 + 80 = 300, but if the Total row (300) is included, the chart sums to 600.
4. Check the number of bars against the number of categories expected.
5. Cross-check one category against the source with a simple count or SUMIF.
**If I find...:** Totals included: rebuild from a PivotChart or the detail rows. Correct chart but misleading labels: fix the labels. Already circulated: send a correction.
**What I would tell the stakeholder:** "The chart included the totals row as if it were another category, so every figure looked doubled. I rebuilt it from the detail; the corrected totals are X. Please use the new version."
**Prevent it next time:** Turn off subtotals and grand totals for chart sources (PivotTable Design), build charts from PivotCharts or Excel tables, and put a check cell next to the data: "chart total = source total".
**Likely follow-ups:** 1) How do you stop copy-paste? Link charts to the model; avoid pasted values. 2) Other double counts? Joins that duplicate rows (many-to-many).
**Common mistakes / traps:** Never reconciling to the source; trusting that the chart "looks right".

### Q66 ⭐⭐ 🟡 Sick-leave days by location are shown below (exercise data). Compute the days per employee for each, and say what the data can and cannot tell you.
| Location | Employees | Sick-leave days (year) |
|---|---|---|
| Pune | 400 | 2,800 |
| Chennai | 150 | 1,500 |
| Remote | 200 | 800 |

**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you normalise by headcount and stay cautious about causes.
**Say this in the interview:** "Chennai has the most days per person at 10, Pune 7 and Remote 4, against an overall 6.8. Totals favour Pune, but per person Chennai stands out. The data shows where, not why."

**What the data shows:** Pune has the most total days, but it is also the biggest location.
**Working:**
1. Pune = 2,800 / 400 = 7.0 days per employee.
2. Chennai = 1,500 / 150 = 10.0.
3. Remote = 800 / 200 = 4.0.
4. Company = 5,100 / 750 = 6.8 days per employee.
**Result:** Chennai 10.0, Pune 7.0, Remote 4.0 days per employee per year (overall 6.8).
**Caveats / what else I would check:**
1. Headcount basis: was employees the year-end figure? Use average headcount (or FTE) over the year.
2. A few long absences (surgery, long illness) can drive a location's total; check the median days and the number of people who took any leave.
3. Recording differences: remote staff may not log small absences, so low numbers may mean under-reporting.
4. Job types, age mix, season or a local outbreak.
5. Privacy: sick-leave is sensitive; report only in groups large enough and follow company policy (confirm with HR and legal).
**Next step / recommendation:** Split Chennai's 1,500 days by length of absence and by team; if most days come from a few long cases, it is a case-management matter, not a location-wide issue. Track monthly.
**Likely follow-ups:** 1) Can I say Chennai staff are less healthy? No. 2) What would explain Remote being low? Under-reporting or working while unwell.
**Common mistakes / traps:** Ranking by total days; reading health conclusions into leave data; using the wrong denominator.

### Q67 ⭐⭐ 🟡 A pivot can show payment mode by city as row percent or as column percent. Using the order counts below (exercise data), which statement is correct: "most UPI orders come from City A" or "most City A orders are UPI"?
Orders: City A UPI 600, card 200; City B UPI 300, card 700.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know which denominator each percentage uses.
**Say this in the interview:** "Both statements are true with these numbers. They answer different questions: the first uses UPI orders as the base, the second uses City A orders. I would pick the one that matches the decision."

**What the data shows:** City A has 800 orders, City B 1,000; UPI orders total 900 and card orders 900.
**Working:**
1. "Most UPI orders come from City A": City A UPI / all UPI = 600 / 900 = 66.7% (column percent). True.
2. "Most City A orders are UPI": City A UPI / all City A = 600 / 800 = 75% (row percent). True.
3. City B: UPI share = 300 / 1,000 = 30%; card = 70%. City B has 33.3% of UPI orders.
4. Context: overall UPI share is 900 / 1,800 = 50%; City A is 44.4% of all orders, but 66.7% of UPI orders.
**Result:** 66.7% of UPI orders come from City A; 75% of City A orders are UPI. The question as phrased expects one answer, but both statements are correct.
**Caveats / what else I would check:** Counts versus value (UPI orders may be smaller); the time period; whether the order counts are complete; small differences in cities of different size.
**Next step / recommendation:** To show where UPI volume sits, use column percent. To show how customers in a city prefer to pay, use row percent (City A 75% against City B 30%, so City A is far more UPI-inclined). Label the denominator on every table.
**Likely follow-ups:** 1) Which statement shows preference? The row percent. 2) Which shows market size? The column percent.
**Common mistakes / traps:** Swapping the two readings; presenting a percentage without saying "of what".

### Q68 ⭐⭐ 🟡 Overtime hours per employee and attrition by team are shown below (exercise data). What would you conclude, and what additional cut would you request?
| Team | Avg overtime hrs / month | Attrition % |
|---|---|---|
| Alpha | 10 | 8 |
| Beta | 25 | 18 |
| Gamma | 40 | 31 |
| Delta | 12 | 22 |

**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you see the pattern, the exception and the limits of four data points.
**Say this in the interview:** "Alpha, Beta and Gamma show attrition rising with overtime, but Delta breaks the pattern, with low overtime and 22% attrition. Overtime may be one factor, not the whole story. I would ask for person-level and exit-reason data."

**What the data shows:** Three teams move together; one team does not.
**Working:**
1. Correlation across all four teams = 0.80; without Delta = 0.997 (only three points).
2. For Alpha to Gamma, each extra 10 overtime hours goes with about 7.7 points more attrition (slope 0.77).
3. Delta is an outlier: only 12 hours of overtime but 22% attrition, near Beta's level.
**Result:** Overtime and attrition are positively related across four teams (r about 0.80), but four points prove little and Delta shows other drivers.
**Caveats / what else I would check:**
1. Reverse direction: high attrition leaves vacancies, and the remaining staff work more overtime.
2. Team-level data: it cannot say whether the people who work overtime are those who leave.
3. Team size, tenure mix, role type, pay, manager and location.
4. Whether attrition is voluntary; the time period.
**Next step / recommendation:** Request: (a) person-level overtime in the months before exit versus stayers, (b) exit reasons, (c) data by manager and tenure, (d) Delta's specific issues (manager, pay, career growth). Pilot overtime limits in Gamma and measure.
**Likely follow-ups:** 1) Does overtime cause attrition? Plausible, not proven. 2) What about Delta? Investigate separately.
**Common mistakes / traps:** Claiming causation from four teams; ignoring Delta; using team averages as if they described individuals.

### Q69 ⭐⭐ 🟡 Inventory turnover is shown below for two warehouses (exercise data). Compute turnover for each and say which is performing better and what could mislead you.
| Warehouse | Annual COGS (lakh) | Average inventory (lakh) |
|---|---|---|
| W1 | 600 | 100 |
| W2 | 450 | 50 |

**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can compute turnover (cost of goods sold divided by average inventory) and interpret it with care.
**Say this in the interview:** "W1 turns its stock 6 times a year, W2 9 times. W2 moves stock faster, using less money tied up, but I would check product mix and stock-outs before calling it better."

**What the data shows:** W1 sells more (COGS 600 versus 450), but also holds twice the inventory.
**Working:**
1. Turnover W1 = 600 / 100 = 6.0 times a year.
2. Turnover W2 = 450 / 50 = 9.0 times a year.
3. Days of inventory = 365 / turnover: W1 = 60.8 days; W2 = 40.6 days.
4. W2 ties up 50 lakh to support 450 lakh of cost; W1 needs 100 lakh for 600 lakh.
**Result:** W2 turns inventory 9.0 times versus 6.0, about 41 days of stock versus 61 (365-day year, rounded).
**Caveats / what else I would check:**
1. Product mix: fast-moving goods turn quickly, bulky or slow lines do not.
2. Stock-outs: very low inventory can mean lost sales; check fill rate and service level.
3. How average inventory is measured: two points (start and end) or monthly? Seasonal peaks matter.
4. One-off items such as clearance, large orders or a change in valuation method.
5. Customer service and delivery times, and handling cost.
**Next step / recommendation:** Add fill rate, stock-out days, gross margin and aged-stock share; compare like with like (same product categories); set targets per category rather than one number.
**Likely follow-ups:** 1) Is a higher turnover always better? No, too high may mean stock-outs. 2) Formula alternatives? Sales divided by inventory, but COGS is the preferred basis.
**Common mistakes / traps:** Choosing W2 only on the ratio; mixing sales and COGS in the numerator; using end-of-year inventory instead of the average.

### Q70 ⭐⭐ 🔴 A survey of current employees shows 82% satisfaction. How can that number mislead, and what extra data would you request?
**Asked at:** commonly asked (no company-specific report found); survey-headline-number prompts appear in vendor interview guides (unverified).
**What the interviewer is checking:** Whether you question who is in a survey before trusting its headline.
**Say this in the interview:** "82% of whom? A survey of current employees leaves out everyone who already quit, so I would ask for response rates, exit data and a breakdown before I believe it."
**What the data shows:** A single percentage with no denominator, no trend and no comparison.
**Working:**
1. Survivorship: unhappy people who left are not in the sample, so satisfaction among current staff is naturally higher.
2. Response bias: if only 40% replied, the silent 60% may differ; happy or very angry people reply most.
3. Fear of honesty: if the survey is not seen as anonymous, scores are inflated.
4. Averaging hides groups: 82% overall can hide 55% in one department or in new joiners.
5. Wording and scale: "satisfied" may include neutral answers; the cut-off (4 and 5 out of 5?) must be stated.
**Result:** No conclusion yet; 82% is a starting point, not a finding.
**Caveats / what else I would check:** Number of invited versus responded, by department and tenure; small groups (under about 10 responses) should be suppressed to protect anonymity.
**Next step / recommendation:** Request response rate by group, last three surveys for trend, attrition and exit-interview reasons for the same period, and an external benchmark (from memory, unverified: many firms compare with industry averages; confirm the source). Report "82% of the 70% who responded".
**Likely follow-ups:** 1) *Would you drop the survey?* No, I would pair it with exit data. 2) *Is 82% good?* Only against last year and peers.
**Common mistakes / traps:** Quoting 82% as "employees are happy"; ignoring leavers; comparing groups of 5 people.

### Q71 ⭐⭐ 🔴 A cumulative chart of signups always rises. How does that hide a slowdown, and what do you plot instead?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you know a running total can only go up and so hides trend changes.
**Say this in the interview:** "A cumulative line rises even when growth is shrinking. I would plot the per-period signups, with a moving average if it is noisy."
**What the data shows:** A line that never falls, so the eye reads "healthy growth" even if each month adds less than the last.
**Working:**
1. Take illustrative monthly signups: 100, 90, 80, 70, 60, 50 (exercise figures).
2. The running total is 100, 190, 270, 340, 400, 450: always up.
3. Signups per month have fallen 50% from 100 to 50, which the cumulative line never shows.
**Result:** Cumulative total 450, while monthly signups halved (100 to 50, a 50% fall).
**Caveats / what else I would check:** Seasonality (compare with the same month last year), a campaign that pulled signups forward, and whether the latest month is complete.
**Next step / recommendation:** Show monthly signups as bars with a 3-month moving average, and keep the cumulative total only as a small number ("450 so far").
**Likely follow-ups:** 1) *When is cumulative useful?* For progress toward a target. 2) *Slope reading?* The slope of the cumulative line is the per-period figure, but people cannot see it by eye.
**Common mistakes / traps:** Celebrating total growth; truncating the axis to make the slope look steep.

### Q72 ⭐⭐ 🔴 An index chart rebased to 100 shows two products grew from 100 to 140 and 100 to 120 over two years. Why can the one with the lower index still have contributed more absolute revenue, and what would you show?
**Asked at:** commonly asked (no company-specific report found); rebased-index charts are a differentiator topic, not a reported question (judgement).
**What the interviewer is checking:** That you know an index removes the size of the base.
**Say this in the interview:** "Rebasing to 100 shows growth rate, not rupees. A small product can grow faster in percent and still add fewer rupees than a big one."
**What the data shows:** Both lines start at 100 whatever their real revenue, so the chart cannot show contribution.
**Working:** (illustrative revenue bases, my assumption, in lakh)
1. Product A starts at 50 and grows 40%: it ends at 70, adding 20.
2. Product B starts at 200 and grows 20%: it ends at 240, adding 40.
3. Total added is 60; B gave 40 of 60, two-thirds, although its index (120) is lower than A's (140).
**Result:** Index 140 versus 120 says A grew faster in percent; absolute gain is 20 versus 40 lakh, so B contributed more.
**Caveats / what else I would check:** Which year is the base (a weak base year inflates the index); whether prices or volumes drove growth.
**Next step / recommendation:** Show the index chart next to a bar of absolute change (or a waterfall of the 60 lakh), and label the starting revenue.
**Likely follow-ups:** 1) *Why rebase at all?* To compare series of different size on one chart. 2) *What if the base year is unusual?* Rebase to a normal year.
**Common mistakes / traps:** Reading index points as rupees; forgetting to say what the base year is.

### Q73 ⭐⭐ 🔴 Customer churn and revenue churn are shown below (exercise data). Compute both and say which you report, and why they differ.
| Segment | Customers (start) | Churned | Avg revenue per customer |
|---|---|---|---|
| Small | 900 | 90 | 1 |
| Large | 100 | 30 | 25 |

**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you weight by value, not just by head count.
**Say this in the interview:** "Customer churn is 12%, but revenue churn is about 24.7%, because the customers we lost were disproportionately the big ones."
**What the data shows:** Small customers churned at 10%, large at 30%, and the large ones carry most of the money.
**Working:**
1. Customer churn: (90 + 30) / (900 + 100) = 120 / 1,000 = 12.0%.
2. Starting revenue: 900 x 1 + 100 x 25 = 900 + 2,500 = 3,400 (units as given).
3. Lost revenue: 90 x 1 + 30 x 25 = 90 + 750 = 840.
4. Revenue churn: 840 / 3,400 = 24.7%.
5. Segment churn: Small 90/900 = 10%; Large 30/100 = 30%. Large customers are 25% of the lost customers but 750/840 = 89.3% of lost revenue.
**Result:** Customer churn 12.0%; revenue churn 24.7% (about 2 times higher; difference of 12.7 percentage points).
**Caveats / what else I would check:** Downgrades (revenue loss without churning), expansion from retained customers (net revenue churn), the time window, and whether the 30 large exits are a few named accounts.
**Next step / recommendation:** Report both, lead with revenue churn for financial decisions and customer churn for product health; investigate why large accounts leave (interview them).
**Likely follow-ups:** 1) *Net revenue churn?* Subtract expansion from remaining customers. 2) *Which for a board?* Revenue churn, with the split.
**Common mistakes / traps:** Reporting only 12%; mixing percent and percentage points; using end-of-period customers as the denominator.

### Q74 ⭐⭐ 🔴 A profit bridge from last year to this year is shown below (exercise data, in lakh). Which factor was the biggest drag, and what question would you ask the business?
| Item | Change |
|---|---|
| Last year profit | 100 |
| Volume | +30 |
| Price | +15 |
| Product mix | -22 |
| Input cost | -35 |
| Overheads | -8 |
| This year profit | ? |

**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you can finish a bridge, and read it for causes rather than just signs.
**Say this in the interview:** "This year's profit is 80 lakh, down 20. Input cost is the biggest single drag at minus 35, and mix at minus 22 is the one I would question next."
**What the data shows:** Gains from volume and price (+45) are more than cancelled by cost, mix and overheads (-65).
**Working:**
1. Positives: 30 + 15 = +45.
2. Negatives: -22 - 35 - 8 = -65.
3. Net change: 45 - 65 = -20.
4. This year profit: 100 - 20 = 80.
5. Input cost is 35 of the 65 lakh of drag (53.8%); mix is 22 (33.8%).
**Result:** This year's profit = 80 lakh, a 20 lakh (20%) fall; biggest drag is input cost (-35).
**Caveats / what else I would check:** How price, volume and mix are defined (a bridge depends on method and order), whether input cost was a market price rise or waste, whether price increases partly offset it.
**Next step / recommendation:** Ask: "Did input costs rise by market prices or by usage, and could we have passed more to customers? Why did mix shift toward lower-margin products?" Then test a pricing action.
**Likely follow-ups:** 1) *Is volume +30 good?* Only if it came at normal margin. 2) *Would you reorder the bridge?* Totals are the same, but attribution can shift.
**Common mistakes / traps:** Not adding up the bridge; blaming the largest bar without asking why; reading mix as a cost.

### Q75 ⭐⭐ 🔴 A time series of daily orders shows a sudden drop to zero for two days, then a spike. How do you decide whether this is a real event or a data problem, and how do you treat it in the chart?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you test the pipeline before explaining the business.
**Say this in the interview:** "Zero then a spike is the classic signature of a data load failure and catch-up. I would confirm with the data team before I tell a business story."
**First, clarify / contain:** Do not publish a story or delete the points yet. Ask the data owner whether any job failed or any outage occurred on those two days.
**What I would check, in order:**
1. Pipeline logs and last-refresh timestamps for those dates.
2. Whether the spike roughly equals the two missing days plus a normal day (catch-up pattern).
3. Other sources: payment gateway, warehouse dispatches, finance totals for the same days.
4. Whether other metrics (visits, signups) also dropped to zero.
5. Whether the same pattern happens in other tables or regions.
**If I find...:** Pipeline failure with backfilled data: reload the correct dates and the chart becomes normal. A real outage (site down): keep the zero, annotate it, and treat the spike as recovered demand. No explanation yet: show the points but mark them "under review".
**What I would tell the stakeholder:** "Orders show zero on 14 and 15 and a spike on 16. This may be a data load issue rather than lost sales, but I have not confirmed it yet; I am checking with the data team and will update by 5 pm."
**Prevent it next time:** Add a freshness and row-count alert on the orders table, and annotate known incidents on the dashboard.
**Likely follow-ups:** 1) *Chart treatment?* Annotate, or show a gap rather than a fake zero. 2) *Interpolate?* Only for a clearly marked data fault.
**Common mistakes / traps:** Explaining a "buying frenzy"; smoothing it away silently; deleting the data.

### Q76 ⭐⭐ 🔴 Confidence intervals for conversion by variant overlap slightly in the chart. Does that mean there is no difference, and how do you communicate it?
**Asked at:** commonly asked (no company-specific report found); A/B interpretation questions appear on practice sites (unverified).
**What the interviewer is checking:** That you know overlapping intervals are not the same as "no significant difference".
**Say this in the interview:** "Slight overlap does not prove no difference. The right check is the confidence interval of the difference itself."
**What the data shows:** Illustrative case, 10,000 users per variant: A converts 5.00%, B 5.75% (my assumed numbers).
**Working:**
1. 95% interval for A: 4.57% to 5.43%.
2. 95% interval for B: 5.29% to 6.21%. The two overlap between 5.29% and 5.43%.
3. Difference: 5.75% - 5.00% = 0.75 percentage points.
4. Interval of the difference: 0.12 to 1.38 percentage points; z = 2.35 (the gap is about 2.35 standard errors, and anything above about 1.96 is significant at the usual 5% level). It excludes zero, so the difference is statistically significant.
**Result:** Overlap yet a significant difference of 0.75 percentage points (a 15% relative lift).
**Caveats / what else I would check:** The reverse also holds: non-overlap is a safe sign, but borderline overlap needs the difference test; check sample ratio, run time, multiple looks, and practical size of the lift.
**Next step / recommendation:** Say "B is likely better, by roughly 0.1 to 1.4 points; the plausible range is wide, so I would confirm if the cost of being wrong is high."
**Likely follow-ups:** 1) *Why does overlap mislead?* The difference has a smaller standard error than either alone suggests. 2) *Statistical vs practical significance?* A real but tiny lift may not justify the change.
**Common mistakes / traps:** Declaring "no difference"; reporting a p-value without the size; peeking and stopping early.

### Q77 ⭐⭐ 🔴 Payroll cost per head is shown below for two years (exercise data). Total payroll rose from 50 crore to 56 crore while headcount rose from 1,000 to 1,200. Compute the change in cost per head and explain what could produce it.
**Asked at:** commonly asked (no company-specific report found); an HR-metrics gap-fill chosen by judgement.
**What the interviewer is checking:** Per-unit thinking, and mix explanations for an average that moves.
**Say this in the interview:** "Total payroll rose 12%, but cost per head fell about 6.7%, from 5.0 to 4.67 lakh. That can mean we hired cheaper roles or people who joined part-way through the year, not that anyone took a pay cut; I would split by grade to confirm."
**What the data shows:** Headcount grew faster (20%) than payroll (12%).
**Working:**
1. Year 1: 50 crore / 1,000 = 5.00 lakh per head per year (1 crore = 100 lakh).
2. Year 2: 56 crore / 1,200 = 4.667 lakh per head.
3. Change: 4.667 / 5.00 - 1 = -6.7%, or -0.33 lakh per head.
4. If the original 1,000 people still cost 50 crore (no raises, no exits), the 200 extra heads added 6 crore, an average of 3.0 lakh each, well below the existing 5.0 lakh average. In reality raises and exits also move the total, so this is the upper limit of the "cheap hires" story, not a measured fact.
**Result:** Cost per head fell 6.7% (5.00 to 4.67 lakh).
**Caveats / what else I would check:** Joining dates (people joined mid-year only cost part of the year, so full-year cost per head will be higher), grade and location mix, attrition of expensive senior staff, bonus and one-off timing, whether contractors are in the headcount.
**Next step / recommendation:** Split by grade and compute like-for-like pay change; use average headcount (or full-time equivalents), not year-end.
**Likely follow-ups:** 1) *Did pay fall?* Not necessarily; mix explains it. 2) *Better metric?* Cost per grade-adjusted head.
**Common mistakes / traps:** Concluding salary cuts; ignoring part-year hires; dividing by year-end headcount only.

### Q78 ⭐⭐ 🔴 Pass rates by programme are shown below for two years (exercise data). Compute the overall pass rate for each year and explain why the overall fell although each programme improved.
| Programme | Year 1 (pass / sat) | Year 2 (pass / sat) |
|---|---|---|
| Easy | 90 / 100 | 48 / 50 |
| Hard | 100 / 400 | 130 / 450 |

**Asked at:** commonly asked (no company-specific report found); Simpson's-type reversals appear on practice sites (unverified).
**What the interviewer is checking:** That you can explain a mix-driven reversal with numbers.
**Say this in the interview:** "Both programmes improved but the overall rate fell from 38.0% to 35.6%, because more candidates sat the hard programme. That is a mix shift."
**What the data shows:** Easy 90.0% to 96.0%; Hard 25.0% to 28.9%; yet overall down.
**Working:**
1. Year 1 overall: (90 + 100) / (100 + 400) = 190 / 500 = 38.0%.
2. Year 2 overall: (48 + 130) / (50 + 450) = 178 / 500 = 35.6%.
3. Easy: 90/100 = 90.0%, then 48/50 = 96.0% (+6.0 points).
4. Hard: 100/400 = 25.0%, then 130/450 = 28.9% (+3.9 points).
5. Share of candidates in the hard programme: 400/500 = 80% in year 1, 450/500 = 90% in year 2.
**Result:** Overall pass rate fell 2.4 percentage points (38.0% to 35.6%) while both programmes rose; the weight of the low-pass hard programme grew.
**Caveats / what else I would check:** Why did the mix move (policy, marketing)? Is the Easy group of 50 too small? Did the paper difficulty change?
**Next step / recommendation:** Report the rate by programme, and a mix-adjusted overall (apply year 1 weights to year 2 rates: 0.2 x 96.0 + 0.8 x 28.9 = 42.3%) to show the underlying improvement.
**Likely follow-ups:** 1) *Which is the "true" figure?* Both are true; the question decides which to show. 2) *Name?* Simpson's paradox or mix effect.
**Common mistakes / traps:** Averaging 90% and 25%; saying "the data is wrong".

### Q79 ⭐ 🟢 What is the difference between a stacked bar, a 100% stacked bar and a grouped bar, and which would you choose to show a changing channel mix?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Chart choice linked to the message.
**Say this in the interview:** "For a changing mix I use a 100% stacked bar, and I add a small total line or table so volume is not lost."
**Explain simply:**
- **Stacked bar:** segments sit on top of each other; the bar height is the total. Good for total plus parts, but only the bottom segment is easy to compare.
- **100% stacked bar:** every bar is scaled to 100%, so it shows share, not size.
- **Grouped bar:** the segments sit side by side; best for comparing exact values across categories, but gets crowded.
**Mini-example:** Web orders go from 400 of 1,000 (40%) to 450 of 1,500 (30%). The 100% chart shows a fall in share; the stacked chart shows web actually grew by 50 orders.
**Practice step:** Draw the same three-channel table in all three forms and write the one-line message each supports.
**Likely follow-ups:** 1) *Many channels?* Group small ones into "Other". 2) *Line chart?* Good for share over many months.
**Common mistakes / traps:** Using 100% stacked and implying volume; too many colours; unsorted segments.

### Q80 ⭐ 🟢 What is a log-scale axis, when would you use one, and what is the risk in showing it to a non-technical audience?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic (judgement).
**What the interviewer is checking:** Awareness of scale choices and audience.
**Say this in the interview:** "On a log axis each step is a multiple (say 10 times), not an equal amount. It is useful for data that spans very large ranges, but I explain it carefully or avoid it for lay audiences."
**Explain simply:**
- Equal distances on the axis mean equal percentage change, not equal rupee change.
- Use it when values span orders of magnitude (1 to 1,00,000), or when you want to compare growth rates; a straight line then means constant percentage growth.
- Risk: people read it as a normal scale and underestimate big gaps; zero and negative values cannot be shown.
**Mini-example:** 10 to 100 and 1,000 to 10,000 look the same height on a log chart, though one is a 90 gain and the other a 9,000 gain.
**Practice step:** Plot values 10, 100, 1,000 on linear and log axes and describe the difference.
**Likely follow-ups:** 1) *Alternative?* Show percentage change or an index. 2) *Label?* Say "log scale" on the axis.
**Common mistakes / traps:** Using log without a label; applying it to data with zeros.

### Q81 ⭐ 🟡 A chart shows average rating by product, ranked, and the top products have 3 to 5 reviews. How would you adjust the ranking?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Small-sample awareness.
**Say this in the interview:** "A 5.0 from three reviews is weak evidence. I would shrink each rating toward the overall average according to how many reviews it has, or set a minimum review count."
**Explain simply:**
- Simple fix: show only products with at least a set number of reviews (say 20), and list the rest separately.
- Better fix, a weighted (shrinkage) rating: (n x product rating + m x overall mean) / (n + m), where m is a chosen weight like 20 reviews.
**Mini-example:** Overall mean 3.8, m = 20 (my assumed values). A 5.0 with 3 reviews becomes (3 x 5.0 + 20 x 3.8) / 23 = 3.96. A 4.5 with 400 reviews becomes 4.47. The big product now ranks higher.
**Practice step:** Add a review-count column and compute the adjusted rating in Excel.
**Likely follow-ups:** 1) *How to pick m?* Judgement; test how the ranking reacts. 2) *Fake reviews?* Check unusual bursts.
**Common mistakes / traps:** Ranking on raw average; hiding review count; treating ratings as exact.

### Q82 ⭐ 🟡 A map shows sales by state, with the large states darkest. Why can that be misleading, and what would you plot instead?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic (judgement).
**What the interviewer is checking:** Normalising before comparing.
**Say this in the interview:** "Big states are dark because they have more people. I would plot sales per customer or per 1,000 people, or share against potential."
**Explain simply:**
- Totals follow population and area, so the map mostly shows where people live.
- Large land area with few customers draws the eye in a filled map though it matters little.
- Plot a rate (sales per capita, penetration, growth), or use a sorted bar or tile map so each state has equal weight.
**Mini-example:** State A sells 50 lakh with 1 crore people (Rs 0.50 per person); State B sells 10 lakh with 10 lakh people (Rs 1.00 per person): A is darker on the map, but B is twice as strong per person (illustrative numbers).
**Practice step:** Add a population column and compute per capita before mapping.
**Likely follow-ups:** 1) *Denominator?* Population, addressable customers or stores. 2) *Colour scale?* Use a clear, even scale.
**Common mistakes / traps:** Mapping raw counts; unequal colour bins.

### Q83 ⭐ 🟡 A year-on-year growth table shows a 150% increase for one product. How do you check whether the base is too small before celebrating it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Percent change versus absolute change.
**Say this in the interview:** "I look at the absolute numbers behind 150%: 20 to 50 units is a 150% rise but only 30 extra units."
**Explain simply:**
- Show last year, this year and the absolute change next to the percentage.
- Compare the absolute change with total revenue (is the product 0.5% of sales?).
- Check whether it is a one-off, such as a single big order, and the monthly pattern.
**Mini-example:** (50 - 20) / 20 = 150%, yet 30 units on a base of, say, 10,000 total units is 0.3% of the company's volume (my assumed total).
**Practice step:** Add "contribution to total growth" as a column.
**Likely follow-ups:** 1) *What threshold?* A minimum base set by the business. 2) *Use anything else?* A multi-year CAGR.
**Common mistakes / traps:** Celebrating a rate; ranking by growth percent alone.

### Q84 ⭐ 🟡 A box plot shows salary by grade, with one grade having several dots above the whisker. How do you read it, and what do you do about those points?
**Asked at:** commonly asked (no company-specific report found); an HR gap-fill (judgement).
**What the interviewer is checking:** Reading a box plot and handling outliers sensibly.
**Say this in the interview:** "The dots are outliers: values far above the typical spread. I check them as people first, not delete them."
**Explain simply:**
- The box holds the middle 50% of salaries, the line inside is the median, the whiskers reach about 1.5 times the box width, and dots lie beyond.
- Several high dots in one grade may mean promoted-but-not-regraded staff, special-skill hires, a retention package, or a data error (an extra zero).
**Plan to handle:** Look up each dotted employee, verify the figure, tag the reason, then report with and without them if material. Do not delete real salaries; use the median rather than the mean.
**Likely follow-ups:** 1) *Why median?* It resists outliers. 2) *Pay equity?* Several high points may be policy exceptions.
**Common mistakes / traps:** Deleting outliers automatically; calling them errors without checking; confusing the box with a bar.

### Q85 ⭐ 🟡 Two charts of the same attrition data, one showing counts and one rates, are presented in the same deck. How do you reconcile them for the audience?
**Asked at:** commonly asked (no company-specific report found); an HR gap-fill (judgement).
**What the interviewer is checking:** Linking numerator, denominator and message.
**Say this in the interview:** "Counts tell us where most people leave; rates tell us where people are most likely to leave. I show both with the headcount, and say which one supports which decision."
**Explain simply:**
- A big department has many leavers even at a low rate; a small one can have a high rate with few leavers.
**Mini-example:** Department A: 30 leavers of 600 = 5.0%. Department B: 12 leavers of 100 = 12.0%. Counts point at A; rates point at B.
**Practice step:** Put both on one table with headcount, leavers, rate, and rank on each.
**Likely follow-ups:** 1) *Which for hiring cost?* Counts. 2) *For retention risk?* Rates, with small-number caution.
**Common mistakes / traps:** Letting the two charts disagree without comment; hiding headcount.

### Q86 ⭐ 🟡 The same revenue table gives different stories by absolute and percentage change. When do you lead with each in a business review?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Choosing the figure that fits the decision.
**Say this in the interview:** "Lead with absolute change when the question is money or contribution; lead with percentage when comparing things of different size or tracking momentum. Always show both."
**Explain simply:**
- Absolute: shows what moved the total; use for resource and impact discussions.
- Percentage: allows fair comparison across sizes; use for efficiency and trend.
**Mini-example:** A grows 5 on 50 (+10%); B grows 100 on 1,000 (+10%): same rate, but B is 20 times more money.
**Practice step:** Add both columns and a "share of total change" column.
**Likely follow-ups:** 1) *Negative bases?* Percentages mislead. 2) *Lead for a board?* Absolute, then rate.
**Common mistakes / traps:** Showing only the flattering one; mixing percent and percentage points.

### Q87 ⭐ 🟡 A sparkline panel shows twenty KPIs with no targets. How would you redesign it to help a decision-maker?
**Asked at:** commonly asked (no company-specific report found); BI candidates are reported being asked to justify chart choices (unverified).
**What the interviewer is checking:** Dashboard design tied to decisions.
**Say this in the interview:** "I would ask which decisions this supports, cut to the handful of KPIs that drive them, and add target, status and owner to each."
**Explain simply:**
- Clarify the audience and decisions first.
- Reduce to about 5 to 8 headline KPIs; move the rest to a detail page.
- For each KPI: current value, target, variance, trend versus last period, status colour with a rule, owner.
- Add a one-line definition and the data refresh time.
- Sort by exceptions (off target first).
**Mini-example:** "Attrition 14.2%, target 12%, +2.2 points, red, owner HR Ops."
**Practice step:** Redesign any dashboard you know on one page.
**Likely follow-ups:** 1) *Who sets targets?* The business owner. 2) *Colour only?* No, add words for accessibility.
**Common mistakes / traps:** Sparklines with no scale or target; decoration; no owner.

### Q88 ⭐ 🟡 Your market share rose (exercise data) from 20% to 22% while the market grew 5%. Compute your revenue growth and say what you would highlight.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Growth as share times market, and percent versus points.
**Say this in the interview:** "Revenue grew about 15.5%: the market added 5% and our share gain added the rest."
**What the data shows:** Share rose 2 percentage points (a 10% relative rise).
**Working:**
1. Take the market as 100 last year: our revenue = 20.
2. This year the market is 105; our revenue = 22% x 105 = 23.1.
3. Growth = 23.1 / 20 - 1 = 15.5%.
4. Check: share ratio 1.10 x market ratio 1.05 = 1.155.
**Result:** Revenue growth 15.5%; share gain 2 percentage points (10% relative); market growth 5%.
**Caveats / what else I would check:** The market definition, whether share is by value or volume, price effects, and competitor behaviour.
**Next step / recommendation:** Highlight that we outgrew the market by about 10 points of growth (15.5% versus 5%) and find which products or regions drove the share gain.
**Likely follow-ups:** 1) *Why not 7%?* Adding 5% and 2 points is wrong; growth multiplies. 2) *Share by value or volume?* State which.
**Common mistakes / traps:** Adding 2 and 5; calling 2 points "2%".

### Q89 ⭐ 🔴 A table of top performers by revenue and a table by growth rate show different names. Which do you use for a bonus decision, and how do you explain the difference?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Fairness thinking and metric design.
**Say this in the interview:** "They answer different questions: revenue shows scale, growth shows momentum. For a bonus I would use the metric agreed in the incentive policy, ideally against each person's target, and I would show both."
**First, clarify / contain:** Ask what the bonus is meant to reward (volume, growth, new business) and whether territories are comparable.
**What I would check, in order:**
1. Territory size and potential: a big territory gives big revenue with little effort.
2. Base effect: Asha 120 to 126 lakh is +5% (+6 lakh); Ravi 40 to 64 lakh is +60% (+24 lakh), illustrative numbers I assumed.
3. Target attainment (actual versus target) as a fairer common yardstick.
4. One-off deals or returns that flatter either number.
**If I find...:** Territories unequal means use attainment against target. A growth leader on a tiny base means cap or weight by absolute gain. One-offs means exclude with documented rules.
**What I would tell the stakeholder:** "Revenue favours large territories and growth favours small bases. I propose scoring on target attainment plus absolute growth; here are both tables."
**Prevent it next time:** Agree the metric and rules before the period starts, in writing.
**Likely follow-ups:** 1) *Combine?* Weighted scorecard. 2) *Bias check?* Review outcomes by territory type.
**Common mistakes / traps:** Picking the list that suits a favoured person; ignoring base size.

### Q90 ⭐ 🔴 Two correlated metrics in a chart seem to move together, with one leading the other by two periods. How do you test whether the lead is real and whether it is useful for forecasting?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Rigour with lead-lag claims.
**Say this in the interview:** "I would test the lead on data the model has not seen, compare against a simple baseline, and check it makes business sense. A lead is useful only if it improves forecasts."
**Clarify first:** What are the two metrics, how many periods of history do we have, and what decision does the forecast support?
**Plan:**
1. Remove trend and seasonality (use changes or growth rates) so shared trends do not create fake correlation.
2. Compute correlation at lags 0, 1, 2, 3 and see if 2 clearly stands out.
3. Check stability: does the lag hold in different sub-periods?
4. Out-of-sample test: forecast the later periods with and without the lagged metric; compare errors.
5. Check the mechanism (marketing spend leading sales makes sense).
**Method choice and why:** Lagged correlation and a simple regression with a baseline first; formal Granger-type tests only if you have long history (from memory, unverified: such tests assume stationary data).
**Pitfalls:** Spurious correlation from trends, many lags tried (some will look good by chance), short history, a reverse effect.
**Deliverable:** One chart of the lagged relationship, the forecast-error comparison, and a plain statement such as "improves error by X%, confidence moderate".
**Likely follow-ups:** 1) *Causal?* Not shown; leading is not causing. 2) *Too few points?* Say so.
**Common mistakes / traps:** Relying on one chart; skipping the baseline; in-sample fit only.

### Q91 ⭐ 🔴 You find that a chart you published last week had a wrong filter, and a decision was taken from it. What do you do, and what do you say to the stakeholder?
**Asked at:** commonly asked (no company-specific report found); gap-fill on correcting a published error (judgement).
**What the interviewer is checking:** Ownership, speed and honesty.
**Say this in the interview:** "I tell the stakeholder immediately, quantify the impact, give the corrected numbers and say what has changed. I do not wait to be asked."
**First, clarify / contain:** Confirm the error and its size first, then pause further use of the chart (take it down or mark it "under correction"). Do not quietly fix it.
**What I would check, in order:**
1. Exactly what filter was wrong and which charts or reports share it.
2. The corrected figures and the difference from what was published.
3. Who saw it and which decision used it.
4. Whether the decision would change with the correct numbers.
**If I find...:** Decision unchanged: tell them, correct the report. Decision affected: escalate to the decision owner right away with options. Others copied the chart: send a correction notice to all.
**What I would tell the stakeholder:** "I found an error in last week's chart: a filter excluded one region. Corrected, the figure is X instead of Y. The decision may be affected, so here is what changes; the corrected chart is attached, and I will confirm it by tomorrow."
**Prevent it next time:** Peer review and reconciliation to a known total before publishing; a change log and a filter summary shown on the chart.
**Likely follow-ups:** 1) *Do you apologise?* Briefly, factually, and focus on the fix. 2) *Who do you tell?* Your manager and the decision owner.
**Common mistakes / traps:** Silent fixing; hiding it; excuses; fixing the chart but not the decision.

### Q92 ⭐ 🔴 The last month in a trend chart is incomplete because data is still loading, so the line dips. How do you present it so nobody misreads the dip?
**Asked at:** commonly asked (no company-specific report found); gap-fill (judgement).
**What the interviewer is checking:** Handling incomplete periods honestly.
**Say this in the interview:** "I would never show a partial month as a full one. I show it as a dashed or grey point labelled 'month to date', or I leave it out and show the last complete month."
**First, clarify / contain:** Confirm the cause (partial month or delayed load) and when the data will be complete.
**What I would check, in order:**
1. Whether the dip is just days elapsed (for example 12 of 30 days = 40% of the month).
2. Whether the data is delayed (late-arriving records) even for older days.
3. Whether a like-for-like comparison is possible (same 12 days last month).
**If I find...:** A partial month: grey or dashed point and a "partial" label. A delay: mark the latest days "provisional". A full month with a real dip: investigate it as a real change.
**What I would tell the stakeholder:** "The last point covers 12 days only; do not read it as a fall. The like-for-like comparison to the same 12 days last month shows X; the full month will be available on the 5th."
**Prevent it next time:** Build the incomplete-period flag into the dashboard, or default to complete months; show month-to-date as a separate tile.
**Likely follow-ups:** 1) *Project the month?* Only with a stated method and a range. 2) *Weekly charts?* Same rule for the current week.
**Common mistakes / traps:** Letting the line fall off a cliff unexplained; comparing 12 days with a full month.

