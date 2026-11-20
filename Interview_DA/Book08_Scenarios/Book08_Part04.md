# Book 8 — Scenario-Based & Data Interpretation | Part 4: Metric-Change Investigations 🟡

**Target:** 80 questions | **Actual:** 80 questions
**Scope:** On-the-job metric-change investigations: confirm the change is real, localise it by segment and funnel step, separate rate from mix, rule out data and definition artefacts, size the impact and communicate the finding, in sales, e-commerce, operations and HR contexts, with inline exercise data where a figure can be derived.

### Q1 ⭐⭐⭐ 🟢 A stakeholder messages you, "Sales have dropped, please look into it." What clarifying questions do you ask before you touch any data?
**Asked at:** commonly asked (no company-specific report found); question banks list "sales dropped, how would you investigate" as a core prompt (unverified).
**What the interviewer is checking:** Whether you pin down the problem and the decision before pulling numbers.
**Say this in the interview:** "Before any data, I would ask what 'sales' means to them, compared with what, since when, and what decision this feeds. Then I would confirm the drop is real."

**Clarify first:** Ask these, in this order:
1. Which metric: revenue, orders, units, or bookings? Gross or net of returns and discounts?
2. Compared with what: yesterday, last week, same period last year, or a target? Over what window?
3. Where did they see it: which dashboard, report or person? Has anyone else seen it?
4. Is it everywhere or one product, region, channel or customer group?
5. Did anything change recently: a launch, price change, system release, campaign, holiday, a competitor?
6. What decision depends on this, and by when?

I do not open the data, form a theory or reply with a cause yet.
**What I would check, in order:**
1. Reproduce the number from the source system, not only the dashboard.
2. Check the data is complete (refresh time, missing days).
3. Compare like with like (same days, same definition).
4. Only then segment and look for the driver.
**If I find...:** the drop is not reproducible, it is a data or definition problem; if it is real and narrow, I localise it; if real and broad, I check traffic and external events first.
**What I would tell the stakeholder:** "Thanks, I have noted the drop. I am confirming the number is real and comparing like for like. I will send you a first update by 3 pm with what is known and unknown."
**Prevent it next time:** Keep a short intake template (metric, window, comparison, decision, deadline) and a metric dictionary so "sales" has one meaning.
**Likely follow-ups:** 1) *Why not just start querying?* Without a defined metric and comparison you may answer the wrong question. 2) *What if they cannot answer?* Say so, state your own assumptions in writing, and proceed.
**Common mistakes / traps:** Starting with a cause guess; accepting "sales" without a definition; not asking what decision it supports.

### Q2 ⭐⭐⭐ 🟢 A key dashboard metric moves sharply overnight. What is your first-hour checklist, in order, before you say anything to the business?
**Asked at:** commonly asked (no company-specific report found); the "verify data, segment, check releases and external events, quantify" frame recurs in question banks (unverified).
**What the interviewer is checking:** That you check data health before business causes.
**Say this in the interview:** "First I rule out the dull explanations: did the data load, did the definition change, is the comparison fair. Only then do I go looking for real business causes."

**First, clarify / contain:** Note the exact time, metric, size and where it was seen. Tell the owner "I am checking, update by a set time", and do not announce a cause.
**What I would check, in order:**
1. Data freshness: did all tables and today's partial data load (row counts vs usual)?
2. Pipeline or job failures, and duplicate or missing loads, in the last 24 hours.
3. Release or tracking changes: any app, website, ETL or dashboard deployment overnight?
4. Definition or filter changes (a new status code, currency, time zone).
5. Calendar: holiday, weekend, month-end, payday, known campaign.
6. Reproduce the figure in the source system independently.
7. Segment: by product, region, channel, device, new vs existing.
8. Check upstream drivers (traffic, funnel steps) and sister metrics.
**If I find...:** a pipeline or definition fault, fix or flag it and tell people the metric is unreliable; if the metric is real, localise by segment and size the impact; if I cannot tell, say that and give a time for the next update.
**What I would tell the stakeholder:** "Metric X moved by about Y. I have ruled out [what]. Still checking [what]. Next update at [time]. Please hold off on decisions based on it until then."
**Prevent it next time:** Automated data-freshness and volume alerts, a release calendar visible to analysts, a metric dictionary.
**Likely follow-ups:** 1) *Why data issues first?* They are the cheapest to check and the most common. 2) *What if the business is already panicking?* Share the "not yet confirmed" status and a time.
**Common mistakes / traps:** Explaining a drop to the business before checking data; checking only one source; skipping the calendar.

### Q3 ⭐⭐⭐ 🟢 Name five data-side (non-business) reasons a metric can appear to drop, and one quick check for each.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know that numbers can fall without any real change.
**Say this in the interview:** "Many drops are artefacts. Five I check first are late data, a broken pipeline, a tracking change, a definition change and duplicates being removed."

**Explain simply:** A "data-side" reason means the world did not change; the measurement did.
1. **Late-arriving or partial data:** today's or yesterday's numbers are not fully loaded. Check: compare row counts and last-loaded timestamp against a normal day.
2. **Pipeline failure or missing partition:** a source feed did not run. Check: count of records per source per day, look for a flat zero.
3. **Tracking or instrumentation change:** an app release stopped sending an event. Check: compare event volume by app version and platform.
4. **Definition or filter change:** a new status, currency, or time zone altered what counts. Check: diff the query or dashboard logic against its previous version.
5. **Duplicate cleanup or double counting fixed:** counts fall after a dedupe. Check: count distinct IDs vs rows before and after.
Others: a changed denominator, a join that drops rows, a time-zone shift.
**Mini-example:** HR headcount drops 8% overnight; the HRIS export now excludes contractors. No one left.
**Practice step:** For one dashboard you know, write down its source tables and who refreshes them.
**Likely follow-ups:** 1) *Which is most common?* From memory, late data and definition changes are very common (unverified). 2) *How to spot quickly?* A sudden clean step change on one day is a red flag.
**Common mistakes / traps:** Naming only business reasons; giving checks that are not specific; forgetting time zones.

### Q4 ⭐⭐⭐ 🟢 Orders were 12,500 last week and 11,000 this week. What is the percentage change, and what would you look at before deciding whether to escalate?
Data: last week 12,500 orders; this week 11,000 orders.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Correct percentage change, then judgement on whether the move is meaningful.
**Say this in the interview:** "It is down 12 percent, 1,500 orders. Before escalating I would check the data, whether the weeks are comparable, and whether this is beyond the normal week-to-week swing."

**What the data shows:** Orders fell by 1,500, a fairly large one-week drop.
**Working:**
1. Change = 11,000 - 12,500 = -1,500 orders.
2. Percentage change = -1,500 / 12,500 = -0.12 = -12.0%.
**Result:** Down 12.0% (1,500 orders), computed against last week, the starting point.
**Caveats / what else I would check:**
- Data complete for both weeks? Same number of days, same cut-off?
- Holiday, payday, sale or festival in either week?
- Usual weekly variation: is -12% outside the past 8 to 12 weeks' range (see Q15)?
- Where: by region, category, channel, device.
- Traffic vs conversion: did visits fall or did fewer visitors buy?
**Next step / recommendation:** If the data is clean and -12% is outside normal swings, escalate with the segment where it is concentrated; if it is within normal variation or data-related, report it as "monitoring" with a re-check date.
**Likely follow-ups:** 1) *What if it was 11,000 to 12,500?* That is +13.6%, because the base is smaller (1,500 / 11,000). 2) *Would you escalate immediately?* Not before a 30-minute data and calendar check.
**Common mistakes / traps:** Dividing by the new number; escalating without checking data; ignoring that one week is a small sample.

### Q5 ⭐⭐⭐ 🟢 Attrition rose from 12% to 15% over the year. What is the change in percentage points and in percent, and why does the distinction matter when you report it?
Data: attrition 12% last year, 15% this year.
**Asked at:** commonly asked (no company-specific report found); HR attrition investigation material stresses definitions and segments (unverified prep sources).
**What the interviewer is checking:** Percentage points vs relative percent, a classic reporting trap.
**Say this in the interview:** "Attrition rose 3 percentage points, which is a 25 percent relative increase. I would always say which one I mean."

**What the data shows:** Attrition went from 12% to 15%.
**Working:**
1. Change in percentage points (pp) = 15% - 12% = 3 pp. A percentage point is a simple subtraction of two percentages.
2. Relative change = 3 / 12 = 0.25 = 25%.
**Result:** +3 percentage points, which is +25% relative to last year's rate. Both are correct but mean different things.
**Caveats / what else I would check:**
- "Up 3%" is ambiguous: a reader could think 12% became 12.36% (3% of 12%).
- Same definition both years? (Voluntary only or all exits, average headcount or opening headcount as the denominator.)
- Is the rise in one department, tenure band or manager group?
- A company with 1,000 people: 3 pp is about 30 more leavers (illustrative figure).
**Next step / recommendation:** Report as "up 3 percentage points (from 12% to 15%, a 25% relative rise)", then break it down by department, tenure and exit reason.
**Likely follow-ups:** 1) *Which should I headline?* The pp change, with the relative figure in brackets. 2) *Can pp be used for any metric?* For any metric that is itself a percentage.
**Common mistakes / traps:** Saying "attrition rose 3%" or "25 pp"; mixing definitions between years.

### Q6 ⭐⭐⭐ 🟢 On the 18th of a 30-day month, the dashboard shows month-to-date revenue of INR 60 lakh against last month's full-month INR 90 lakh, a fall of 33%. What is wrong with this comparison, and what is the like-for-like change?
Data: month-to-date revenue (18 days) INR 60 lakh; last month (30 days) INR 90 lakh.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you spot an unfair comparison (partial period vs full period).
**Say this in the interview:** "It compares 18 days with 30 days. On a daily-run-rate basis revenue is up about 11 percent, not down 33."

**What the data shows:** The -33% is just 18 days versus 30 days.
**Working:**
1. The dashboard figure: (60 - 90) / 90 = -33.3%. Arithmetic is right; the comparison is not.
2. This month's daily run-rate = 60 / 18 = INR 3.33 lakh per day.
3. Last month's daily rate = 90 / 30 = INR 3.00 lakh per day.
4. Like-for-like change = 3.33 / 3.00 - 1 = +11.1%.
5. A simple projection: 3.33 x 30 = INR 100 lakh for the month.
**Result:** About +11.1% per day (projection about INR 100 lakh vs 90 lakh), not -33%. Figures rounded to one decimal.
**Caveats / what else I would check:**
- Better like-for-like: compare month-to-date days 1 to 18 of last month with days 1 to 18 this month.
- Weekday mix (how many weekends), paydays and month-end spikes can make a straight-line projection wrong.
- Revenue may be back-loaded (more at month-end), so the run-rate can overstate or understate.
**Next step / recommendation:** Change the dashboard to default to same-period comparison and label it "MTD vs same days last month".
**Likely follow-ups:** 1) *Is +11% certain?* No, it is a run-rate estimate; same-days data is better. 2) *How to prevent?* Build MTD vs prior-MTD as a standard view.
**Common mistakes / traps:** Quoting -33% to leadership; projecting by multiplying without noticing weekday or month-end patterns.

### Q7 ⭐⭐⭐ 🟢 Revenue fell from INR 50 lakh to INR 45 lakh while orders rose from 10,000 to 10,500. What happened to average order value, and what does it tell you about where to look?
Data: last month 10,000 orders, INR 50 lakh; this month 10,500 orders, INR 45 lakh.
**Asked at:** commonly asked (no company-specific report found); price and volume decomposition is a standard item in question banks (unverified).
**What the interviewer is checking:** That you split revenue into orders times average order value (AOV).
**Say this in the interview:** "Revenue is orders times AOV. Orders rose 5 percent but AOV fell about 14 percent, so the problem is basket value, not demand."

**What the data shows:** More orders, but smaller ones.
**Working:**
1. AOV last month = 50,00,000 / 10,000 = INR 500.
2. AOV this month = 45,00,000 / 10,500 = INR 428.57.
3. AOV change = 428.57 / 500 - 1 = -14.3%.
4. Orders change = +5.0%; revenue change = -10.0%.
**Result:** AOV fell from INR 500 to about INR 429 (-14.3%), while orders rose 5.0%, so revenue fell 10.0%.
**Caveats / what else I would check:**
- Discounts or coupons: was there a big promo that lifted orders but cut value?
- Mix: more low-priced items, a new cheaper category, or a change in customer type.
- Items per order vs price per item.
- Returns or cancellations netted off? Order definition (split shipments counted as two)?
**Next step / recommendation:** Break AOV down by category, discount level, new vs repeat customers and items per order; find which part explains most of the INR 71 drop.
**Likely follow-ups:** 1) *Is that bad?* Not necessarily if the promo bought customers who return; check margin, not just revenue. 2) *Which should I check first?* Discounting and category mix.
**Common mistakes / traps:** Looking only at orders because they rose; ignoring that it can be a definition change in what counts as an order.

### Q8 ⭐⭐⭐ 🟢 What is the difference between a metric moving because customer or employee behaviour changed and a metric moving because its definition or measurement changed? Give two examples of each.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you separate a real change from a measurement change.
**Say this in the interview:** "A behaviour change is something people actually did differently. A measurement change is something we did to how we count. The first needs a business response; the second needs a data fix."

**Explain simply:**
- **Behaviour change (real):** customers or employees acted differently.
  1. Customers buy less after a price rise.
  2. Attrition rises after a pay-revision delay as employees resign.
- **Definition or measurement change (artefact):** the number moved though behaviour did not.
  1. "Active user" changes from 30-day to 7-day activity, so the count drops.
  2. HR attrition now counts only voluntary exits, or headcount excludes contractors after an HRIS export change.
- Other measurement changes: a new tracking event, a time-zone change, a duplicate fix.
**Mini-example:** If "Active users" falls 20% the day the definition tightens and all segments fall evenly, suspect measurement. If one segment falls after a price change, suspect behaviour.
**Practice step:** For each metric on your dashboard, write one line on how it is defined and who last changed it.
**Likely follow-ups:** 1) *How do you tell them apart?* Look for a step change on a release date, and rebuild the old definition on new data to see if the gap disappears. 2) *Can both happen together?* Yes; separate them by recomputing with the old definition.
**Common mistakes / traps:** Assuming every drop is business-driven; not versioning definitions; comparing across a definition change without a note.

### Q9 ⭐⭐⭐ 🟡 Daily active users of your company's app are 10% below the 7-day average this morning. You are the on-call analyst. Walk me through your first two hours.
**Asked at:** DAU-drop prompts appear in question banks such as PracHub (company attribution unverified); otherwise commonly asked (no company-specific report found).
**What the interviewer is checking:** A calm, ordered investigation: data first, then segments, then causes, with communication.
**Say this in the interview:** "First 15 minutes, confirm the data is complete and not a tracking fault. Then segment, check releases and external events, and send a status note within the hour."

**First, clarify / contain:** Confirm what "DAU" means (which event counts as active), and whether "this morning" is a partial day. A partial day will always look low against full-day averages, so I compare the same hours of previous days. I do not announce a cause.
**What I would check, in order:**
1. 0 to 15 min: data freshness, pipeline status, same-time-of-day comparison, usual Monday or weekday pattern (is -10% unusual?).
2. 15 to 40 min: segment by platform, app version, country, new vs returning, acquisition channel.
3. 40 to 70 min: compare event volumes by version for tracking breaks; check releases, outages, push-notification sends, app store issues, campaigns and holidays.
4. 70 to 100 min: drill on the segment that explains the drop; check funnel (installs, opens, logins).
5. Throughout: size it (how many users, how much revenue at risk).
**If I find...:** one app version with falling events means a likely tracking or crash issue, so alert engineering; a pipeline gap means a data fix and a note; a broad real drop with no data fault means an escalation with segments.
**What I would tell the stakeholder:** "DAU is about 10% below its 7-day average. Data looks complete. The gap is concentrated in [segment]. Cause not confirmed; checking release and tracking. Next update in 30 minutes."
**Prevent it next time:** Anomaly alert with same-hour baselines, a release calendar, event-volume monitoring per version.
**Likely follow-ups:** 1) *What if nothing explains it?* Say it may be normal noise, show the usual range, and keep monitoring. 2) *When do you page engineering?* When one version or platform shows a sharp step.
**Common mistakes / traps:** Comparing a partial day with a full-day average; escalating before data checks; not communicating for two hours.

### Q10 ⭐⭐⭐ 🟡 Conversion fell this week. Use the funnel below to find the step that explains the fall, and state the change in paid orders.
Data (views to paid orders):
| Step | Last week | This week |
|---|---|---|
| Product views | 100,000 | 100,000 |
| Add to cart | 12,000 | 11,900 |
| Checkout started | 7,200 | 7,140 |
| Payment successful | 6,480 | 5,712 |

**Asked at:** Indian e-commerce conversion-RCA prompts (for example Meesho, MakeMyTrip) appear in Dataford question banks (unverified, company attribution not confirmed); funnel breakdown is commonly asked.
**What the interviewer is checking:** Step-to-step conversion, not just the top and bottom numbers.
**Say this in the interview:** "The fall is almost all at the payment step: success from checkout dropped from 90 percent to 80 percent. Paid orders are down 768, or about 11.9 percent."

**What the data shows:** Traffic is flat and the early steps barely moved; payment success broke.
**Working:**
1. View to cart: 12.0% to 11.9% (-0.1 pp).
2. Cart to checkout: 7,200 / 12,000 = 60.0%; 7,140 / 11,900 = 60.0% (no change).
3. Checkout to paid: 6,480 / 7,200 = 90.0%; 5,712 / 7,140 = 80.0% (-10 pp).
4. Overall conversion: 6.48% to 5.712%, a fall of 0.768 pp.
5. Paid orders: 5,712 - 6,480 = -768, which is -11.9%.
6. If payment success had stayed at 90%, this week's paid orders would be 7,140 x 0.9 = 6,426, so the payment step costs 714 orders; the remaining 54 are from the fewer checkouts.
**Result:** Paid orders down 768 (-11.9%); about 714 of the 768 (93%) trace to payment success falling 10 pp. Figures rounded.
**Caveats / what else I would check:**
- Payment gateway, bank, method (UPI, card, wallet), device and app version.
- Payment-failure error codes; any gateway change or outage this week.
- Whether "payment successful" tracking changed.
- Retries: did failed users try again later (delayed orders)?
**Next step / recommendation:** Break payment failures down by gateway and method (see Q17), involve the payments owner, and track hourly success rate until it recovers.
**Likely follow-ups:** 1) *Is the 0.1 pp at add-to-cart important?* No, it is small and within normal noise. 2) *How to prove it is payment?* Show the other step rates are unchanged.
**Common mistakes / traps:** Only comparing views and orders; ignoring step-level rates; blaming marketing.

### Q11 ⭐⭐⭐ 🟡 Overall conversion fell even though both mobile and desktop conversion improved. Calculate the overall rates and explain how this can happen.
Data:
| Segment | Period 1 sessions | Period 1 conv. | Period 2 sessions | Period 2 conv. |
|---|---|---|---|---|
| Mobile | 40,000 | 2.0% | 70,000 | 2.2% |
| Desktop | 60,000 | 5.0% | 30,000 | 5.5% |

**Asked at:** Simpson's paradox and mix-shift items appear in question banks and vendor blogs such as Mixpanel (unverified); commonly asked.
**What the interviewer is checking:** That you understand mix shift (Simpson's paradox).
**Say this in the interview:** "Both segments improved, but traffic shifted to the low-converting segment, mobile. The overall rate is a weighted average, so a change in weights can pull it down."

**What the data shows:** (This pattern, where every segment improves but the total falls, is called Simpson's paradox.) Mobile share of sessions went from 40% to 70%.
**Working:**
1. Period 1 orders: 40,000 x 2.0% = 800; 60,000 x 5.0% = 3,000; total 3,800 of 100,000 sessions = 3.80%.
2. Period 2 orders: 70,000 x 2.2% = 1,540; 30,000 x 5.5% = 1,650; total 3,190 of 100,000 = 3.19%.
3. Overall change = 3.19% - 3.80% = -0.61 pp.
4. Rate effect (new mix, change in each rate): 0.7 x 0.2 pp + 0.3 x 0.5 pp = +0.29 pp.
5. Mix effect (old rates, change in mix): (0.7 - 0.4) x 2.0% + (0.3 - 0.6) x 5.0% = 0.60 - 1.50 = -0.90 pp.
6. Check: +0.29 - 0.90 = -0.61 pp.
**Result:** Overall conversion fell from 3.80% to 3.19% (-0.61 pp) because the mix shift (-0.90 pp) outweighed the rate gains (+0.29 pp).
**Caveats / what else I would check:**
- Why did the mix move: a mobile ad campaign, an app promotion, desktop traffic loss?
- Is the extra mobile traffic useful (cheap, low intent) or a tracking change?
- Decomposition split depends on the order of calculation; state which you used.
**Next step / recommendation:** Report segment conversion and mix separately; check the channel behind the mobile surge; use segment rates, not the overall rate, to judge product changes.
**Likely follow-ups:** 1) *Did the product get worse?* No: both segments improved. 2) *Which number should management watch?* Segment conversion plus traffic mix.
**Common mistakes / traps:** Saying "the data is wrong"; reporting only the overall rate; forgetting to check mix.

### Q12 ⭐⭐⭐ 🟡 Monthly revenue fell from INR 20,00,000 to INR 18,90,000 for one product. Split the change into a volume effect and a price effect and say what you would do next.
Data: last month 10,000 units at INR 200; this month 9,000 units at INR 210. Use last month's price for the volume effect and this month's volume for the price effect.
**Asked at:** price and volume decomposition appears in PracHub and Codemia revenue-drop items (unverified); commonly asked.
**What the interviewer is checking:** Clean price-volume split that sums to the total.
**Say this in the interview:** "Volume fell 10 percent and cost INR 2 lakh; price rose 5 percent and added INR 90,000. Net fall INR 1.1 lakh, so the issue is volume."

**What the data shows:** Fewer units sold at a higher price.
**Working:**
1. Last month: 10,000 x 200 = INR 20,00,000. This month: 9,000 x 210 = INR 18,90,000.
2. Total change = 18,90,000 - 20,00,000 = -INR 1,10,000 (-5.5%).
3. Volume effect = (9,000 - 10,000) x 200 = -INR 2,00,000.
4. Price effect = (210 - 200) x 9,000 = +INR 90,000.
5. Check: -2,00,000 + 90,000 = -1,10,000.
**Result:** Volume effect -INR 2,00,000; price effect +INR 90,000; net -INR 1,10,000 (-5.5%).
**Caveats / what else I would check:**
- Did units fall because of the price rise (price elasticity, meaning how sensitive buyers are to price)? Or stock-outs, competitor action, seasonality?
- Is the price effect a list-price rise or less discounting?
- Margin: higher price may protect profit even if revenue fell.
- Other products: are customers switching to a substitute within the company?
**Next step / recommendation:** Compare weekly units against the date of the price change, check stock availability and competitor prices, and judge whether the price rise is worth the lost volume using margin, not revenue.
**Likely follow-ups:** 1) *Is the order of the calculation important?* Yes, using the other base gives a slightly different split; state your convention. 2) *What would you do if volume fell before the price rise?* The price is not the cause.
**Common mistakes / traps:** Calling the rise in price a "good" result; forgetting a cross term; not checking stock.

### Q13 ⭐⭐⭐ 🟡 Sales fell company-wide by 26 units of revenue. What share of the net decline comes from the South, and how would you proceed from here?
Data (INR lakh):
| Region | Q1 | Q2 |
|---|---|---|
| North | 120 | 116 |
| South | 90 | 66 |
| East | 100 | 98 |
| West | 80 | 84 |

**Asked at:** commonly asked (no company-specific report found); driver contribution by segment is standard in revenue-drop question banks (unverified).
**What the interviewer is checking:** Contribution to the decline, not just growth rates.
**Say this in the interview:** "South explains about 92 percent of the net fall, 24 of 26 lakh. I would go deeper into South next."

**What the data shows:** Three regions are nearly flat; one collapsed.
**Working:**
1. Totals: Q1 = 120 + 90 + 100 + 80 = 390; Q2 = 116 + 66 + 98 + 84 = 364; change = -26 lakh (-6.7%).
2. Regional change: North -4, South -24, East -2, West +4.
3. South share of net decline = 24 / 26 = 92.3%.
4. South's own change = -24 / 90 = -26.7%.
5. Share of gross declines (the sum of falls only, 4 + 24 + 2 = 30): South is 24 / 30 = 80%.
**Result:** South accounts for 92.3% of the net INR 26 lakh decline (80% of gross declines); it fell 26.7% itself. Rounded to one decimal.
**Caveats / what else I would check:**
- The net share exceeds the gross share because West offset 4 lakh; say which base you use.
- Is South's drop a data issue (missing feed), a large customer lost, a stock-out, or a pricing change?
- Q1 vs Q2 seasonality by region.
**Next step / recommendation:** Break South down by state, product, channel and top customers; compare with the same period last year; talk to the regional sales lead with the facts.
**Likely follow-ups:** 1) *Should you ignore the other regions?* Not entirely: check North and East for slow declines. 2) *Could the share be above 100%?* Yes, if other regions grew more.
**Common mistakes / traps:** Dividing by gross declines and calling it "share of net"; stopping at region.

### Q14 ⭐⭐⭐ 🟡 Monthly attrition rose from 2.0% to 3.1%. Which department explains most of the increase, what share is it, and what would you check there?
Data (headcount constant at 1,000 across both months):
| Dept | Avg headcount | Leavers last month | Leavers this month |
|---|---|---|---|
| Support | 250 | 7 | 17 |
| Engineering | 400 | 6 | 6 |
| Sales | 200 | 4 | 5 |
| Operations | 150 | 3 | 3 |

**Asked at:** HR attrition investigation is covered in educational and vendor material (unverified); commonly asked (no company-specific report found).
**What the interviewer is checking:** Segmenting attrition and giving a share of the change.
**Say this in the interview:** "Support explains about 91 percent of the rise: 10 of 11 extra leavers. Its monthly attrition went from 2.8 to 6.8 percent."

**What the data shows:** One department changed; the rest are flat.
**Working:**
1. Totals: last month 7 + 6 + 4 + 3 = 20 leavers = 2.0% of 1,000; this month 17 + 6 + 5 + 3 = 31 = 3.1%.
2. Change = +11 leavers = +1.1 percentage points.
3. Support: +10 leavers; Sales +1; Engineering and Operations 0.
4. Support's share = 10 / 11 = 90.9%, which is 1.0 pp of the 1.1 pp rise.
5. Support's own rate: 7/250 = 2.8% to 17/250 = 6.8%.
**Result:** Support explains 90.9% of the increase (about 1.0 of 1.1 pp); its monthly attrition rose from 2.8% to 6.8% (+4.0 pp).
**Caveats / what else I would check:**
- Small numbers: 11 extra leavers is a handful; one team or one manager may drive it.
- Voluntary vs involuntary (a layoff or contract-end batch?), tenure, performance rating, shift.
- Exit-interview reasons, manager, location, pay compared with peers, recent policy changes (shift roster, targets).
- Regretted exits (people you wanted to keep).
- Is the headcount really constant?
**Next step / recommendation:** Pull Support leavers by manager, tenure, shift and reason; share a draft with HR business partner before conclusions; track weekly.
**Likely follow-ups:** 1) *Is it a crisis?* Judge by the reasons and by how far 6.8% a month sits above Support's usual 2.8% and the company's own history; I would not call it a crisis from one month. 2) *Why not just look at Sales?* Its change is tiny.
**Common mistakes / traps:** Using percentages without leaver counts; naming a cause before exit data; confusing pp and percent.

### Q15 ⭐⭐⭐ 🟡 This week's orders look low. Is this a real drop or normal noise? Calculate how many standard deviations below the 8-week mean it is.
Data: weekly orders for the last 8 weeks: 10,200; 9,900; 10,400; 10,100; 9,800; 10,300; 10,000; 10,300. This week: 9,600. Use the sample standard deviation.
**Asked at:** commonly asked (no company-specific report found); signal vs noise appears in root-cause question banks (unverified).
**What the interviewer is checking:** Whether you compare a move with normal variation.
**Say this in the interview:** "This week is about 2.5 standard deviations below the 8-week mean, so it looks unusual but not conclusive with only eight points. I would check data and calendar before calling it real."

**What the data shows:** Past weeks stay between 9,800 and 10,400; 9,600 is below all of them.
**Working:**
1. Mean = 81,000 / 8 = 10,125 orders.
2. Sample standard deviation (a measure of typical weekly swing, dividing by n-1) = about 212.1.
3. Z-score = (9,600 - 10,125) / 212.1 = -2.47.
4. Drop vs mean = -525, or -5.2%.
5. A rough normal range (mean plus or minus 2 SD) is about 9,701 to 10,549; 9,600 is just outside.
**Result:** About 2.5 standard deviations below the mean (z = -2.47); 5.2% below average. Rounded. (With a population standard deviation of 198.4 it would be -2.65.)
**Caveats / what else I would check:**
- Eight points is a small sample, and the SD itself is uncertain; weeks may have trends or seasonality.
- Is this week complete (late data), or does it include a holiday?
- By chance, a z beyond 2 happens in a few percent of normal weeks; if you watch many metrics, some will cross it.
- Check segments and traffic to see whether a real cause exists.
**Next step / recommendation:** Treat it as a probable real dip worth a data and segment check; confirm with next week's number before a major escalation.
**Likely follow-ups:** 1) *Is 2 SD the rule?* It is a common rough alert threshold, not a law. 2) *Which SD?* Sample SD here, as instructed.
**Common mistakes / traps:** Declaring it "statistically significant" off one number; using only last week as the baseline; ignoring completeness.

### Q16 ⭐⭐⭐ 🟡 The average delivery time rose from 28 to about 33 minutes. Calculate the new mean and median and explain what you would report to operations.
Data: last week all 1,000 sampled orders took 28 minutes. This week 950 took 28 minutes and 50 took 130 minutes.
**Asked at:** commonly asked (no company-specific report found); Swiggy-style delivery problems appear in prep guides (unverified).
**What the interviewer is checking:** That you notice a few extreme values, and choose measures that tell the true story.
**Say this in the interview:** "The mean rose to 33.1 minutes, but the median is still 28. Only 5 percent of orders are very late, so I would report the tail, not just the average."

**What the data shows:** Most deliveries are unchanged; a small group is very slow.
**Working:**
1. New mean = (950 x 28 + 50 x 130) / 1,000 = (26,600 + 6,500) / 1,000 = 33.1 minutes.
2. Change in mean = +5.1 minutes, +18.2%.
3. Median (middle value of 1,000 sorted orders) = 28 minutes, since 950 are at 28.
4. The 50 slow orders (5%) contribute 6,500 of 33,100 total minutes, about 19.6%.
**Result:** Mean 33.1 minutes (up 5.1), median 28 minutes (unchanged). Rounded to one decimal.
**Caveats / what else I would check:**
- Which orders took 130 minutes: one area, one rider group, one restaurant, a bad weather event, an app bug that did not close the order timer?
- Is 130 a data error (timestamp not recorded)?
- Report the 90th and 95th percentile and the share of orders over a target (for example over 45 minutes).
- Sample of 1,000 may not represent all orders.
**Next step / recommendation:** Tell operations: "Typical delivery is unchanged at 28 minutes; 5% of sampled orders took about 130 minutes. Let us find what they have in common." Then trace those orders.
**Likely follow-ups:** 1) *Which metric is better for operations?* Median plus a tail percentile. 2) *Would you remove the 130s?* Not until you know whether they are real or errors.
**Common mistakes / traps:** Reporting only the mean; deleting outliers blindly; saying "everything got slower".

### Q17 ⭐⭐⭐ 🟡 The payment success rate fell. Find the cause from the table and quantify the extra failed payments.
Data:
| Gateway | Attempts (both weeks) | Success last week | Success this week |
|---|---|---|---|
| A | 50,000 | 96% | 96% |
| B | 30,000 | 94% | 94% |
| C | 20,000 | 90% | 70% |

**Asked at:** commonly asked (no company-specific report found); payment-step breakdown follows the funnel items in Dataford question banks (unverified).
**What the interviewer is checking:** Pinpointing the segment and quantifying its impact.
**Say this in the interview:** "Gateway C is the whole story: its success fell from 90 to 70 percent, causing 4,000 extra failed payments and taking overall success from 94.2 to 90.2 percent."

**What the data shows:** Gateways A and B are unchanged; C dropped 20 points.
**Working:**
1. Last week failures: A 2,000 + B 1,800 + C 2,000 = 5,800; overall success = 94.2%.
2. This week failures: A 2,000 + B 1,800 + C 6,000 = 9,800; overall success = 90.2%.
3. Extra failures = 9,800 - 5,800 = 4,000, all from C (20,000 x 20 pp = 4,000).
4. Overall change = -4.0 pp; C explains 100% of it.
**Result:** 4,000 extra failed payments, all from Gateway C; overall success down 4.0 pp (94.2% to 90.2%).
**Caveats / what else I would check:**
- Error codes at C: bank declines, timeouts, a certificate or API change, or a change in routing?
- Payment method mix (UPI, cards) on C; device or app version; time of day.
- Customers who retried on another gateway: net lost orders may be lower.
- The attempts are equal in both weeks per the table; in real data check that volume share did not shift.
**Next step / recommendation:** Alert the payments team, consider routing traffic away from C while they investigate, and monitor hourly success by gateway. Estimate revenue at risk as 4,000 x average order value.
**Likely follow-ups:** 1) *How do I size revenue loss?* Failures x AOV, less retries. 2) *Why use counts as well as rates?* Counts show business impact.
**Common mistakes / traps:** Looking only at the overall rate; forgetting to check retries; assuming all gateways changed.

### Q18 ⭐⭐⭐ 🟡 The average product rating fell from 4.4 to about 4.2. Calculate the new average and decide whether existing products got worse.
Data: last month 10,000 ratings averaging 4.4. This month the same 10,000 existing-product ratings still average 4.4, plus 2,000 ratings from a newly launched category averaging 3.2.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Mix effect on an average (new group dilutes it).
**Say this in the interview:** "Existing products did not get worse; their average is still 4.4. The overall fall is because a new category with lower ratings joined the pool."

**What the data shows:** No change in the old base; a new low-rated group added.
**Working:**
1. Last month total rating points = 10,000 x 4.4 = 44,000.
2. New-category points = 2,000 x 3.2 = 6,400.
3. This month total = 44,000 + 6,400 = 50,400 over 12,000 ratings = 4.20.
4. Change = -0.20 points; the new category is 2,000 / 12,000 = 16.7% of ratings.
**Result:** The new average is 4.20 (down 0.20), fully explained by the new category; existing products unchanged at 4.4.
**Caveats / what else I would check:**
- Is the new category really worse, or are early ratings from fewer, more critical buyers (small sample, early adopters)?
- Is the new category's 3.2 due to delivery or quality of a few sellers?
- Existing products' average could still hide offsetting moves at product level.
- Whether the rating scale and collection method are the same.
**Next step / recommendation:** Report ratings separately for existing and new categories; investigate the 3.2 (themes in reviews, returns, seller concentration); avoid mixing the two in one trend line.
**Likely follow-ups:** 1) *Is the overall 4.2 wrong?* No, it is right but misleading without the split. 2) *What would you tell the product team?* The old catalogue is stable; the new category needs attention.
**Common mistakes / traps:** Concluding quality fell everywhere; averaging 4.4 and 3.2 without weights (which would give 3.8).

### Q19 ⭐⭐⭐ 🟡 It is 10 am and the CEO asks why revenue fell yesterday. You have partial findings only. What exactly do you tell them, and what do you not say?
**Asked at:** commonly asked (no company-specific report found); stakeholder communication appears in scenario-round guides (unverified).
**What the interviewer is checking:** Honest, calm communication when findings are incomplete.
**Say this in the interview:** "I would give three things: what is confirmed, what is ruled out, and when I will come back. I would not offer an unconfirmed cause as fact."

**First, clarify / contain:** Ask what the CEO needs: a number, a cause, or a decision? Confirm the size of the drop and the comparison being used so we are talking about the same figure.
**What I would check, in order (already in progress):**
1. Data complete and definition unchanged.
2. Size: how much, versus what baseline.
3. Where: segment concentration.
4. What is ruled out and what remains.
**If I find...:** a data issue, say the number is unreliable; a segment concentration, name it as "where", not "why"; nothing yet, say so.
**What I would tell the stakeholder:** "Revenue yesterday was about X, which is Y% below the usual level for a [weekday]. I have confirmed the data loaded fully. The drop is concentrated in [segment]; it is not a company-wide pattern. I have not yet established why; I am checking [two items]. I will update you by [time] and sooner if it changes."
What I do not say: a guessed cause ("it is the competitor"), a final number I have not verified, blame on a team, or "nothing to worry about". I avoid jargon and I also do not hide partial findings.
**Prevent it next time:** A standard incident-style update template (confirmed, suspected, ruled out, next update time) and a daily revenue monitor.
**Likely follow-ups:** 1) *What if the CEO insists on a cause?* Offer the most likely hypotheses, labelled as hypotheses, with how and when you will confirm. 2) *What if you are wrong later?* Correct it quickly and plainly (see Q30).
**Common mistakes / traps:** Guessing a cause to fill silence; giving a number you have not checked; going quiet until you are certain.

### Q20 ⭐⭐⭐ 🟡 How would you build a metric tree for orders on an e-commerce marketplace so that you can localise a decline in minutes?
**Asked at:** metric-tree and DAU-drop angles appear in PracHub items (company attribution unverified); commonly asked.
**What the interviewer is checking:** Structured decomposition of a metric into drivers, ready to test.
**Say this in the interview:** "I split orders into traffic times conversion, then break conversion along the funnel, and cut each branch by segment. That lets me test every branch with one query and find where the fall sits."

**Clarify first:** Which orders (placed, paid, delivered), what time grain (hourly, daily), what are the standard cuts (category, region, device, channel, new vs repeat)?
**Plan:**
1. Top level: Orders = Visitors x Conversion rate (orders per visitor). Alternatively Orders = Active buyers x Orders per buyer.
2. Traffic branch: visitors by channel (organic, paid, app, email), device, region; new vs returning.
3. Conversion branch: search or browse to product view, view to cart, cart to checkout, checkout to payment success (each a ratio).
4. Supply side: sellers live, products in stock, price competitiveness, delivery promise (cannot buy what is unavailable).
5. Overlay cuts for every node: category, region, device, app version, customer type.
6. Pre-build a table or dashboard with each node as a column, today vs baseline, so that the node with the biggest change stands out.
**Method choice and why:** A simple multiplication tree plus segment cuts first; add price-volume and mix decomposition if rates move in opposite directions, as in Q11. Statistical models are not required to localise a drop.
**Pitfalls:**
- Nodes that overlap or do not multiply back to the top (the tree must reconcile).
- Different definitions of "visitor" across tools.
- Ignoring supply and data-quality branches.
- Treating correlation in the tree as proof of cause.
**Deliverable:** A one-page tree diagram with each node's definition, owner, data source and this-week vs baseline value; a standing dashboard view; and a short runbook: "check data, then branch with the largest contribution to the gap".
**Likely follow-ups:** 1) *Why a tree?* It forces a complete, non-overlapping list of reasons so nothing is missed. 2) *How deep do you go?* Until the branch is actionable by a team.
**Common mistakes / traps:** A list of ideas instead of a mathematical tree; no data-health branch; not checking that the parts multiply to the total.

### Q21 ⭐⭐⭐ 🟡 You have twelve possible causes for a metric drop and two hours. How do you prioritise which hypotheses to test first?
**Asked at:** commonly asked (no company-specific report found); prep sites list "verify data, segment, check releases and external events" as the standard root-cause frame (unverified for any company).
**What the interviewer is checking:** Whether you rank hypotheses by likelihood, cost to test and impact, instead of testing in random order.
**Say this in the interview:** "I would not test all twelve. I would score each on how likely it is, how big the impact would be, and how cheap it is to check, then start with the cheap, likely ones, and rule out data problems first."
**First, clarify / contain:** Confirm the drop is real and its size, which metric definition is used, and the exact start time. Do not start fixing anything yet; first agree on the two-hour plan with the requester.
**What I would check, in order:**
1. Data and pipeline health (late loads, duplicates, a changed definition): cheapest to test and, if true, makes every other test meaningless.
2. Anything that changed on the drop day: releases, config, price, campaign, tracking tags. A sharp start date points to a change, not a trend.
3. Segment the drop (platform, region, channel, product): if one slice carries most of the fall, only the causes that touch that slice stay on the list.
4. External causes (competitor, holiday, weather, outage at a payment partner) once internal ones are cleared.
5. Slow causes (seasonality, mix shift) last, because they rarely explain a sudden drop.
**If I find...:** One segment explains most of the drop: drop every hypothesis that does not touch it and go deep there. A data issue: stop and fix the numbers, then re-check whether a drop remains. Nothing explains it after the cheap tests: widen to the slower, costlier hypotheses and tell the stakeholder.
**What I would tell the stakeholder:** "At the one-hour mark: the drop is confirmed, data checks are clean, it sits mainly in X. Three causes are ruled out, two are still open. Next update in 45 minutes."
**Prevent it next time:** Keep a standing checklist and a metric tree, so the order is agreed before an incident; log every release and campaign in a shared change calendar.
**Likely follow-ups:** (1) Scoring? A simple 1-3 scale for likelihood, impact and effort is enough. (2) What if two causes overlap? Test the one that can be ruled out fastest first.
**Common mistakes / traps:** Falling for the most exciting story first; skipping the data check; testing each hypothesis without segmenting first; no time-boxing.

### Q22 ⭐⭐⭐ 🟡 A metric dropped the same day a release shipped and a competitor ran a sale. How do you tell whether the release, the competitor or something else caused it?
**Asked at:** commonly asked (no company-specific report found); a "product change vs traffic mix shift vs data issue" prompt appears on question-bank sites (unverified; Dataford listing, answer not seen).
**What the interviewer is checking:** Whether you separate causes using comparison groups and segments, and are honest that two events on one day cannot be fully separated by timing alone.
**Say this in the interview:** "Same-day timing proves nothing by itself. I would look for a group the release touched and a group it did not, and for a group the competitor sale reached and one it did not."
**First, clarify / contain:** Ask what the release changed, who got it (all users, staged rollout, one platform), and which products or cities the competitor sale covers. Do not blame either yet.
**What I would check, in order:**
1. Data check: is the drop real and not a tracking change in the same release?
2. Release exposure: compare users on the new version with users on the old one (staged rollouts and platforms that did not get it act as a control group).
3. Competitor exposure: compare categories, cities or price bands where the competitor sale applies against ones where it does not.
4. Funnel position: a release bug usually breaks a specific step (checkout errors, crashes); a competitor sale usually lowers top-of-funnel visits and conversion at the browsing stage, with no errors.
5. Rule out other causes: traffic mix, a holiday, a paused campaign.
**If I find...:** The drop appears only on the new version: release is the main cause; roll back or hotfix. The drop appears only where the competitor sale applies: external cause; plan a response. The drop appears in all groups alike: look for a third cause. Both: say honestly that the effect is shared and give a range.
**What I would tell the stakeholder:** "The drop is concentrated in X. This points to the release/competitor. Confidence is medium because both happened the same day; a rollback test on 10% of traffic would settle it by tomorrow."
**Prevent it next time:** Staged rollouts with a holdout group, a shared change calendar, and release flags that can be switched off for a slice.
**Likely follow-ups:** (1) No control group exists? Use a before/after on unaffected segments (difference-in-differences) and label it as an estimate. (2) Can I roll back to test? Yes, if cost is low.
**Common mistakes / traps:** Claiming causation from timing; ignoring a staged-rollout control; not checking tracking changes shipped in the same release.

### Q23 ⭐⭐⭐ 🟡 Orders by 9 am today look low. Is it a real shortfall or late-arriving data? Calculate the shortfall and list your checks.
Data: a typical day has 25,000 orders, with 32% usually placed before 9 am. Orders recorded by 9 am today: 6,400.
**Asked at:** commonly asked (no company-specific report found); data lag and incomplete-day comparisons are listed as common traps on prep sites (unverified).
**What the interviewer is checking:** Whether you compare like with like (same time of day) and test for data lag before sounding the alarm.
**Say this in the interview:** "Expected by 9 am is 8,000 orders, we have 6,400, a 20% shortfall. Before calling it real, I would check whether the data feed is simply late."
**What the data shows:** A typical day by 9 am has about 8,000 orders; today shows 6,400, so we are 1,600 orders (20%) behind the usual pace.
**Working:**
1. Expected by 9 am = 25,000 x 32% = 8,000.
2. Shortfall = 8,000 - 6,400 = 1,600 orders.
3. Shortfall % = 1,600 / 8,000 = 20%.
4. If the pace holds, the day would end near 6,400 / 0.32 = 20,000 orders (5,000 below typical, also 20%). This is only a projection, not a forecast.
**Result:** 1,600 orders short by 9 am, 20% below the usual pace (rounded, exercise numbers).
**Caveats / what else I would check:** (1) Pipeline: when did the orders table last load and is the latest timestamp near 9 am? (2) Compare the same weekday and time, not the daily average (a Monday morning is not a Sunday morning). (3) Count from the source system or payment gateway and compare with the report. (4) Check cumulative orders every 15 minutes: a late feed jumps up when caught up, a real shortfall stays flat in slope. (5) Check traffic and error logs for an outage.
**Next step / recommendation:** Wait for the next refresh and check again; if the gap persists after the load completes, treat it as real and move to segmenting. Tell the stakeholder it is "possibly late data, will confirm by 10 am".
**Likely follow-ups:** (1) How to tell lag from real? Source count versus warehouse count. (2) What if both agree? Real drop; segment by channel and region.
**Common mistakes / traps:** Comparing a partial day with a full day; using the wrong weekday; sounding the alarm before checking the load time; calling 8,000 the "target" when it is only the typical pace.

### Q24 ⭐⭐⭐ 🟡 Time-to-hire rose from 30 to 42 days. Which stage contributes most of the increase, and what would you ask the recruiting team?
Data (days):
| Stage | Before | Now |
|---|---|---|
| Sourcing | 7 | 8 |
| Screening | 5 | 5 |
| Interviews | 10 | 18 |
| Offer and joining | 8 | 11 |

**Asked at:** commonly asked (no company-specific report found); HR-funnel equivalents of the revenue-drop frame are common in people-analytics material (unverified).
**What the interviewer is checking:** Whether you decompose a total into stage contributions and then ask operational questions instead of guessing.
**Say this in the interview:** "Interviews account for 8 of the 12 extra days, about two thirds, so I would start there and ask what changed in the interview process."
**What the data shows:** The stages add up (7+5+10+8 = 30 before; 8+5+18+11 = 42 now). Interviews nearly doubled; offer and joining grew a little; screening did not change.
**Working:**
1. Total rise = 42 - 30 = 12 days.
2. Stage changes: sourcing +1, screening 0, interviews +8, offer and joining +3 (sum 12).
3. Shares of the rise: sourcing 8.3%, screening 0%, interviews 66.7%, offer and joining 25.0%.
**Result:** Interviews contribute 8 of 12 days (67%); offer and joining 3 days (25%).
**Caveats / what else I would check:** Averages hide mix: did the role mix change (more senior roles take longer)? Is "time-to-hire" measured the same way (from requisition open or from first application)? Are the stages sequential or do they overlap? Look at medians and spread, because a few stuck requisitions can lift an average.
**Next step / recommendation:** Ask the recruiting team: did the number of interview rounds rise? Are interviewers scarce or on leave? How long do panels take to give feedback? Did scheduling move to a new tool? Is there a backlog of candidates? For offer and joining: longer notice periods, approval delays, or negotiation? Then track days per stage weekly.
**Likely follow-ups:** (1) Mix check? Split by department and seniority. (2) Is a longer time to hire bad? Only if it costs candidates; check drop-out rates by stage.
**Common mistakes / traps:** Blaming the biggest stage without checking mix; mixing calendar days and working days; using averages with outliers; asking "why is recruiting slow?" as an accusation.

### Q25 ⭐⭐⭐ 🟡 Offer acceptance fell from 80% to 60%. Calculate the change and describe how you would investigate before telling HR why.
Data: last quarter 50 offers, 40 accepted; this quarter 50 offers, 30 accepted.
**Asked at:** commonly asked (no company-specific report found); offer acceptance is a standard HR-funnel metric (unverified for any company).
**What the interviewer is checking:** Percentage-point versus relative change, a small-numbers warning, and structured investigation before storytelling.
**Say this in the interview:** "It fell 20 percentage points, which is a 25% relative drop, ten fewer acceptances from the same 50 offers. Before giving a reason I would check small-sample noise, mix and the decline reasons."
**What the data shows:** Same number of offers, ten fewer acceptances.
**Working:**
1. Last quarter: 40 / 50 = 80%. This quarter: 30 / 50 = 60%.
2. Change in points = 60 - 80 = -20 percentage points.
3. Relative change = (60 - 80) / 80 = -25%.
**Result:** -20 percentage points (-25% relative); 10 fewer acceptances.
**Caveats / what else I would check:** With 50 offers per quarter, the sampling noise is large (the standard error of a 70% rate on 50 offers is about 6.5 points). A Fisher exact test (a standard test for whether two small-count proportions really differ) on these counts gives p of about 0.049, borderline (p is the chance of a gap this big if nothing had really changed). So the drop is probably real but not certain, and the size is uncertain. Check: (1) role, level and location mix of offers; (2) offered salary versus market and versus candidates' expectations; (3) decline reasons from recruiters or exit-from-process notes; (4) time between final interview and offer (slow offers lose people); (5) competitor offers; (6) the same candidates' counter-offers; (7) whether offers still pending are counted as declined (definition).
**Next step / recommendation:** Break acceptances by role family and recruiter, read the decline reasons, and bring HR a ranked list of likely causes with evidence, not one story. Track acceptance monthly with the offer count shown.
**Likely follow-ups:** (1) Is it significant? Borderline, so do not overclaim. (2) What would you tell HR today? "It fell 20 points; the cause is not yet known; I will report by Thursday."
**Common mistakes / traps:** Calling 20 points "20%"; ignoring that 50 is a small sample; counting offers still open as declined; giving HR a cause before checking.

### Q26 ⭐⭐⭐ 🟡 Payroll cost rose 8% month on month while headcount stayed flat. Calculate cost per head and list what you would check.
Data: last month payroll INR 4.00 crore, 800 employees; this month INR 4.32 crore, 800 employees.
**Asked at:** commonly asked (no company-specific report found); payroll variance questions are a common HR-analytics scenario (unverified).
**What the interviewer is checking:** Whether you split a cost change into per-head and headcount effects and then list the payroll components that can move.
**Say this in the interview:** "Cost per head went from INR 50,000 to INR 54,000, up 8%. With flat headcount, it is all a per-head effect, so I would look inside the pay components and at who left and joined."
**What the data shows:** Headcount is the same, so the whole INR 32 lakh rise sits in cost per head.
**Working:**
1. Last month cost per head = 4,00,00,000 / 800 = INR 50,000.
2. This month = 4,32,00,000 / 800 = INR 54,000.
3. Rise = INR 4,000 per head = 8%; total rise = INR 32,00,000.
**Result:** INR 50,000 to INR 54,000 per head (+8%, +INR 32 lakh in total).
**Caveats / what else I would check:** Flat headcount can hide churn: leavers replaced by higher-paid hires. Check: (1) one-offs (bonus, incentive, arrears, leave encashment, notice-period payouts); (2) increment cycle effective this month; (3) overtime and shift allowances; (4) employer contributions (PF, ESI, gratuity provision; rates are from memory, confirm with finance); (5) joiners and leavers during the month (full vs part-month pay); (6) working days or pay-cycle cut-off differences; (7) data errors such as duplicate employee lines.
**Next step / recommendation:** Build a bridge from INR 4.00 crore to 4.32 crore by component and by department, tag each bar as one-off or recurring, and tell finance which part will repeat next month.
**Likely follow-ups:** (1) Is 8% bad? Not by itself; depends on whether it is planned increments. (2) How to separate one-off? Compare components against the last 6 months.
**Common mistakes / traps:** Assuming flat headcount means flat people; not separating one-off from recurring; comparing months with different days or cut-off dates.

### Q27 ⭐⭐⭐ 🔴 Break the overall conversion fall into a rate effect and a mix effect, in percentage points, using the segments below, and explain which one management should act on.
Data:
| Segment | Share of sessions, P1 | Conv. P1 | Share of sessions, P2 | Conv. P2 |
|---|---|---|---|---|
| Mobile | 40% | 2.0% | 70% | 2.2% |
| Desktop | 60% | 5.0% | 30% | 5.5% |

Use period 1 rates for the mix effect and period 2 shares for the rate effect.
**Asked at:** commonly asked (no company-specific report found); rate versus mix decomposition appears on question-bank and vendor pages on Simpson's paradox (unverified).
**What the interviewer is checking:** Whether you can show that every segment improved yet the total fell, and name the right owner for the fix.
**Say this in the interview:** "Overall conversion fell 0.61 points, but both segments improved. The fall is a mix effect of -0.90 points, partly offset by a rate effect of +0.29."
**What the data shows:** Mobile (low-converting) grew from 40% to 70% of sessions, so the blend drops even though each segment got better.
**Working:**
1. Overall P1 = 0.4 x 2.0 + 0.6 x 5.0 = 3.80%.
2. Overall P2 = 0.7 x 2.2 + 0.3 x 5.5 = 1.54 + 1.65 = 3.19%.
3. Change = 3.19 - 3.80 = -0.61 points.
4. Mix effect = (P2 shares x P1 rates) - P1 overall = (0.7 x 2.0 + 0.3 x 5.0) - 3.80 = 2.90 - 3.80 = -0.90 points.
5. Rate effect = P2 shares x (P2 rate - P1 rate) = 0.7 x 0.2 + 0.3 x 0.5 = 0.29 points.
6. Check: -0.90 + 0.29 = -0.61.
**Result:** Total -0.61 points = mix -0.90 plus rate +0.29 (percentage points, exact for this method; splitting order changes the split slightly).
**Caveats / what else I would check:** Why did mobile share jump (a campaign, a new app, a tracking change)? Are new mobile sessions lower quality (paid traffic, bots)? Both effects depend on the chosen order of calculation; say which you used. Look at orders and revenue, not only conversion rate.
**Next step / recommendation:** Management should not panic about "conversion falling": experiences improved. Act on mix: decide if the extra mobile traffic is worth its cost, and lift mobile conversion, the big lever, since mobile now carries 70% of sessions. Report conversion by segment alongside the blend.
**Likely follow-ups:** (1) Which segment to fix? Mobile: lifting it by 1 point adds 0.7 points overall. (2) Is this Simpson's paradox? A close cousin: segments up, total down.
**Common mistakes / traps:** Reporting the blended number alone; calling points "percent"; using one set of weights for both effects without saying so.

### Q28 ⭐⭐⭐ 🔴 Weekly active users fell 15% on the exact day of a mobile app release, and the app team insists nothing broke. How do you prove or disprove a tracking regression?
**Asked at:** commonly asked (no company-specific report found); the DAU-drop "first two hours" prompt appears on PracHub (company attribution unverified).
**What the interviewer is checking:** Whether you can separate "users left" from "events stopped being recorded" using independent data sources.
**Say this in the interview:** "A drop that starts to the minute of a release smells like tracking. I would compare the analytics numbers against sources the release could not affect, such as server logs, orders and payments."
**First, clarify / contain:** Ask for the release notes, which SDK or event names changed, and the rollout percentage. Do not announce a user loss to leadership yet, and do not tell the app team they are wrong yet.
**What I would check, in order:**
1. Split by app version: if the drop is only on the new version, suspect the release; if it hits old versions too, suspect something else.
2. Split by platform (Android or iOS) and by event: did one event (for example app_open) vanish while others stayed?
3. Compare with independent signals: server-side login or API request counts, orders, payments, push-notification opens. If orders are flat, users did not leave.
4. Check event volume per active user and sessions per user: a tracking fault often changes events per user sharply or leaves the user ID blank.
5. Check for duplicate or changed user IDs and consent or privacy prompts (a new consent banner can reduce tracked users).
6. Check the data pipeline for dropped or rejected events and schema errors.
**If I find...:** Server counts normal, only the new version drops: tracking regression; ask engineering to fix and backfill if possible. Server counts also fall: real user loss; look for a bug, crash or a store-listing issue. Mixed: report both.
**What I would tell the stakeholder:** "Analytics shows -15%, but server requests are flat and the drop is only on the new version, which points to an event not firing. I will confirm with the app team by today 4 pm and mark the data as unreliable until then."
**Prevent it next time:** Release checklist with tracking tests (event counts compared before and after on a small rollout), alerts on event volume, and version-level dashboards.
**Likely follow-ups:** (1) Team says nothing broke? Show the version split; it is data, not blame. (2) Can the data be fixed? Possibly backfilled from server logs; confirm with engineering.
**Common mistakes / traps:** Reporting 15% user loss without cross-checks; arguing with the app team instead of showing evidence; ignoring that the metric definition changed.

### Q29 ⭐⭐⭐ 🔴 Revenue is down 10% year on year for the quarter and the board meets on Friday. Design the full investigation and the three-slide readout.
**Asked at:** commonly asked (no company-specific report found); the price/volume and segment frame is common on revenue-drop prep pages (unverified).
**What the interviewer is checking:** Structure, time management, decomposition and clear communication under a deadline.
**Say this in the interview:** "I would first confirm what 10% means, then split revenue into volume and price, then by customer, product and region, and give the board three slides: what happened, why, and what we do."
**Clarify first:** Is this gross or net revenue? Same quarter last year on the same definition? Any price, tax or product-scope changes, currency effects or a different number of days? The decision: what should the board do, and what should they not worry about?
**Plan:**
1. Day 1 (Tue): validate numbers against finance, restate on a like-for-like basis, and agree on definitions.
2. Day 1-2: decompose revenue = orders x average order value (or customers x revenue per customer); split by product, region, channel, new versus existing customers; use price/volume/mix.
3. Day 2-3: test causes: lost customers or lower volumes, discounts, one-off large deals in the base period, seasonality or calendar effects, competitor moves, supply issues.
4. Day 3: size each cause in rupees and rank them; check the quarter trend by month to see whether it is worsening or stabilising.
5. Day 4 (Thu): peer review with finance and sales, remove claims that cannot be defended, rehearse.
**Method choice and why:** Simple decomposition and segment tables first; no model is needed for a board. Go further (regression or cohort analysis) only if the simple view leaves a big unexplained share.
**Pitfalls:** Comparing against an unusual base quarter; mix shift; one-off deals; mixing gross and net; blaming the market without evidence; presenting causes without sizes.
**Deliverable:** Three slides. (1) The answer: "Revenue is down 10% (INR X crore); N% of it comes from A and B", with a bridge chart. (2) Why: the top 2-3 drivers with evidence and a confidence level, and what is not the cause. (3) Actions and next steps: owners, expected effect, how it will be measured, plus an appendix with definitions. Also state what is still unknown.
**Likely follow-ups:** (1) What if you cannot find the cause by Friday? Show what is ruled out, the leading hypotheses and the plan. (2) What is the headline? The one driver that explains the most.
**Common mistakes / traps:** A slide with every chart; no rupee sizing; presenting an unverified reason as fact; ignoring the base period.

### Q30 ⭐⭐⭐ 🔴 You find a real cause on Tuesday but the stakeholder had already told leadership a different explanation on Monday. How do you handle the correction?
**Asked at:** commonly asked (no company-specific report found); stakeholder-handling scenarios are common in analytics interviews (unverified).
**What the interviewer is checking:** Integrity, tact and judgement: you correct the record early, privately first, and help the stakeholder look good.
**Say this in the interview:** "I would go to the stakeholder first, privately, with the evidence, and agree on a correction to leadership together, quickly, without making it about who was wrong."
**First, clarify / contain:** Re-check my own finding with a second method and a peer, so I am certain. Do not email leadership directly, and do not leave the wrong explanation standing.
**What I would check, in order:**
1. Is my finding solid and does it truly contradict Monday's explanation, or can both be partly true?
2. What decisions have already been made on Monday's explanation (budget, a rollback, a message to a client)?
3. What evidence did Monday's explanation rest on (a partial dataset, an assumption)?
4. How big is the difference in action: does anything need to change today?
**If I find...:** Monday's explanation was partly right: present the finding as a refinement. It was wrong and decisions depend on it: correct it the same day. Low-impact difference: include it in the next scheduled update, but still correct it.
**What I would tell the stakeholder:** "Yesterday's view was based on partial data. With full data I found X, and here is the evidence. I suggest we tell leadership today: early data pointed to A; the full picture is B. I can draft the note and we send it together."
**Prevent it next time:** Share early findings labelled "preliminary", state confidence and what is still open, and agree the update rhythm up front.
**Likely follow-ups:** (1) What if the stakeholder refuses to correct? Escalate calmly to my manager, with facts; do not go around them silently. (2) Should I apologise? Neutral wording, no blame.
**Common mistakes / traps:** Waiting for the next meeting; surprising the stakeholder in public; saying "you were wrong"; softening the correction until it is unclear.

### Q31 ⭐⭐ 🟢 January revenue was INR 62 lakh and February's was INR 56 lakh. A manager says sales fell. Is that right?
Data: January has 31 days, February 28 days (non-leap year).
**Asked at:** commonly asked (no company-specific report found); unequal month length is a standard trap on prep sites (unverified).
**What the interviewer is checking:** Whether you normalise for the number of days before judging a change.
**Say this in the interview:** "Total revenue fell, but per day it is flat at INR 2 lakh a day in both months, so no real fall."
**What the data shows:** February has 3 fewer days, which explains the lower total.
**Working:**
1. Total change = (56 - 62) / 62 = -9.68%.
2. January per day = 62 / 31 = INR 2.00 lakh.
3. February per day = 56 / 28 = INR 2.00 lakh.
4. Per-day change = 0%.
**Result:** Total -9.7% (INR 6 lakh lower); revenue per day unchanged at INR 2 lakh.
**Caveats / what else I would check:** Number of weekdays and weekends (a month with fewer Saturdays may differ), month-end billing patterns, a salary-day or festival effect, and whether the business sells every day.
**Next step / recommendation:** Report revenue per day (or per working day) next to the total, and compare with the same month last year.
**Likely follow-ups:** (1) Is the manager wrong? Not about the total, only about the conclusion. (2) Weekday mix? Compare per trading day.
**Common mistakes / traps:** Comparing months of different length; saying "sales fell" without normalising; checking only one day of the week.

### Q32 ⭐⭐ 🟢 The absenteeism rate went up this month. Calculate both months' rates and the change, and say what you would check first.
Data: 500 employees, 22 working days in both months. Absence days: 440 last month, 605 this month.
**Asked at:** commonly asked (no company-specific report found); HR attendance metrics are a typical people-analytics example (unverified).
**What the interviewer is checking:** Correct rate definition (absence days over available days) and a sensible first check.
**Say this in the interview:** "Absenteeism went from 4.0% to 5.5%, up 1.5 percentage points. Before reacting I would check whether it is a few long leaves or many short ones, and whether the definition and data changed."
**What the data shows:** Absence days rose by 165, a 37.5% relative rise.
**Working:**
1. Available days = 500 x 22 = 11,000.
2. Last month = 440 / 11,000 = 4.0%.
3. This month = 605 / 11,000 = 5.5%.
4. Change = +1.5 percentage points (relative +37.5%).
**Result:** 4.0% to 5.5%, +1.5 points (+37.5% relative), on the stated assumptions.
**Caveats / what else I would check:** First: definition and data (did leave codes change, was a leave type such as sick versus planned added, or were regularisations posted late?). Then: a few people on long medical leave versus many short absences; a department, shift or location concentrating it; Monday/Friday pattern; festival or weather effects; and whether the headcount denominator is the same. Keep individual-level detail confidential.
**Next step / recommendation:** Split by department and by leave type, then tell the HR head whether it is broad or concentrated before suggesting any policy.
**Likely follow-ups:** (1) Exclude approved leave? Report both unplanned and total. (2) Is 1.5 points big? Compare with the last 12 months' range.
**Common mistakes / traps:** Calling points "percent"; counting calendar days instead of working days; reading one month as a trend.

### Q33 ⭐⭐ 🟢 Orders in the table appear to have grown 25% week on week. Calculate the true growth and explain what you would check.
Data: this week the orders table has 12,500 rows but 10,000 distinct order IDs; last week 10,000 rows and 10,000 distinct IDs.
**Asked at:** commonly asked (no company-specific report found); duplicate rows are a standard data-quality trap (unverified).
**What the interviewer is checking:** Whether you count distinct orders, not rows, and trace the source of duplicates.
**Say this in the interview:** "Rows grew 25%, but distinct orders are 10,000 in both weeks, so true growth is 0%. The extra 2,500 rows are duplicates."
**What the data shows:** 2,500 of 12,500 rows (20%) this week are repeats.
**Working:**
1. Row growth = 12,500 / 10,000 - 1 = 25%.
2. True growth = 10,000 / 10,000 - 1 = 0%.
3. Duplicates = 12,500 - 10,000 = 2,500 rows (20% of this week's rows).
**Result:** True growth is 0%; the 25% is a duplicate effect.
**Caveats / what else I would check:** Are the duplicates exact copies or different statuses of the same order (placed, shipped, returned; one order may legitimately have several rows)? Did a pipeline retry, a double load or a join cause them? Do revenue totals also double count? Compare with the source system's count. The same ID with different amounts needs a rule.
**Next step / recommendation:** Deduplicate with a clear rule (keep the latest status per order ID), fix the load, restate any reports built on this table, and add a daily uniqueness check.
**Likely follow-ups:** (1) How would you check in SQL? Compare count of rows with count of distinct order IDs. (2) Which row to keep? Latest by update time, per agreed rule.
**Common mistakes / traps:** Reporting rows as orders; deleting duplicates without understanding them; forgetting revenue is also overstated.

### Q34 ⭐⭐ 🟢 The orders table stores timestamps in UTC but the daily report is in IST. Which IST date does an order placed at 20:00 UTC on 31 March belong to, and how can this create a false dip?
**Asked at:** commonly asked (no company-specific report found); time-zone mismatches are listed as second-line traps on prep material (unverified).
**What the interviewer is checking:** Time zone arithmetic and awareness of how it shifts counts between days.
**Say this in the interview:** "IST is UTC plus 5 hours 30 minutes, so 20:00 UTC on 31 March is 01:30 IST on 1 April. It belongs to 1 April."
**What the data shows:** Any order placed between 18:30 and 24:00 UTC lands on the next IST date.
**Working:**
1. 20:00 UTC + 5:30 = 25:30, which is 01:30 the next day.
2. So the order date in IST is 1 April, not 31 March.
3. The IST day 31 March covers 18:30 UTC on 30 March to 18:30 UTC on 31 March.
**Result:** 1 April, 01:30 IST (IST has no daylight saving, from memory, unverified).
**Caveats / what else I would check:** A false dip appears when the report cuts days by UTC date but the business thinks in IST. The first 5.5 hours of each IST day (00:00 to 05:30 IST) fall on the previous UTC date, so those early-morning orders are counted in the wrong day; at month-end, orders placed just after midnight IST on 1 April are counted in March, making April look lower and March higher. A feed that is only loaded up to midnight UTC is also cut at 05:30 IST, so the IST "today" can look incomplete. Check where the conversion occurs (database, BI tool or report) and that it happens only once; also check whether source and report both say which zone they use.
**Next step / recommendation:** Convert to IST once in a single place, document it, and use the same cut for all reports; compare with the finance ledger at month-end.
**Likely follow-ups:** (1) Why does it matter at month-end? Revenue lands in the wrong month. (2) What if the timestamps are naive? Confirm the zone with the owner before converting.
**Common mistakes / traps:** Converting twice; forgetting the half hour; reporting UTC dates to an Indian business.

### Q35 ⭐⭐ 🟢 After finance started reporting revenue net of refunds, the weekly figure fell. Calculate the change and say how you would explain it.
Data: previously reported gross revenue INR 1,00,00,000; refunds INR 8,00,000; the new report shows gross minus refunds.
**Asked at:** commonly asked (no company-specific report found); definition changes are a standard metric-change cause (unverified).
**What the interviewer is checking:** Recognising a definition change, not a performance fall, and communicating it plainly.
**Say this in the interview:** "The figure fell from INR 1.00 crore to INR 92 lakh, an 8% drop, entirely because of the definition. No sales were lost."
**What the data shows:** The same business is measured on a stricter basis.
**Working:**
1. New revenue = 1,00,00,000 - 8,00,000 = INR 92,00,000.
2. Change = -8,00,000 / 1,00,00,000 = -8%.
**Result:** INR 92 lakh versus INR 100 lakh; -8%, a definition effect only.
**Caveats / what else I would check:** Were earlier weeks restated on the same basis (otherwise trends break)? Are refunds booked in the week of the refund or the week of the original sale (this changes weekly figures)? Cancellations, chargebacks and discounts: included or not? Which dashboards still show gross?
**Next step / recommendation:** Restate past periods on the net basis, label every chart "net of refunds", keep a gross-to-net bridge (gross 100, refunds 8, net 92), and record the change in the metric dictionary.
**Likely follow-ups:** (1) Which is better? Net shows real money kept; gross shows demand. Report both. (2) How would you tell leaders? "Same business, new definition: -8% is not a performance change."
**Common mistakes / traps:** Reporting the fall as a business decline; mixing old and new definitions in one trend; not annotating the chart.

### Q36 ⭐⭐ 🟢 Support tickets rose from 2,000 to 2,800 and a manager asks whether quality worsened. What is the ticket rate per 100 orders in each period, and what is your answer?
Data: last month 20,000 orders; this month 35,000 orders.
**Asked at:** commonly asked (no company-specific report found); using rates rather than counts is a standard denominator check (unverified).
**What the interviewer is checking:** Whether you normalise by volume before judging.
**Say this in the interview:** "Tickets rose 40%, but orders rose 75%. Tickets per 100 orders fell from 10 to 8, so on this evidence quality did not worsen."
**What the data shows:** Volume grew faster than complaints.
**Working:**
1. Last month = 2,000 / 20,000 x 100 = 10 tickets per 100 orders.
2. This month = 2,800 / 35,000 x 100 = 8 tickets per 100 orders.
3. Ticket count change = +40%; orders change = +75%.
4. Rate change = -2 per 100 orders, which is -20% relative.
**Result:** 10 down to 8 tickets per 100 orders (-20%).
**Caveats / what else I would check:** Ticket types (delivery, quality, payment); a tracked rate hides a bad product category; ticket lag (tickets arrive days after the order, so compare with orders from earlier days); new customers may raise first-order tickets; a new support channel may change what is counted; and the workload is still up 40%, so the team may need capacity.
**Next step / recommendation:** Report the rate next to the count, split by ticket type, and separately plan support staffing for the higher volume.
**Likely follow-ups:** (1) Does quality improve? Not proven, only that the rate did not worsen. (2) What about lag? Match tickets to the orders they came from.
**Common mistakes / traps:** Judging by counts alone; ignoring workload implications; mixing ticket creation date with order date.

### Q37 ⭐⭐ 🟡 When you investigate a dip, how do you choose between a week-over-week, same-week-last-year and trailing 4-week baseline? Calculate all three comparisons.
Data: this week 9,600 orders; last week 10,000; same week last year 9,000; average of the last 4 weeks 9,900.
**Asked at:** commonly asked (no company-specific report found); baseline choice is a common follow-up in metric-drop rounds (unverified).
**What the interviewer is checking:** That you know each baseline answers a different question and can read conflicting signals.
**Say this in the interview:** "The three baselines give -4.0%, +6.7% and -3.0%. They disagree, which tells me this is a small recent dip on top of year-long growth."
**What the data shows:** Down versus recent weeks, up versus last year.
**Working:**
1. Week over week = 9,600 / 10,000 - 1 = -4.0%.
2. Same week last year = 9,600 / 9,000 - 1 = +6.7%.
3. Trailing 4-week average = 9,600 / 9,900 - 1 = -3.0%.
**Result:** -4.0%, +6.7%, -3.0% respectively (rounded to 0.1 point).
**Caveats / what else I would check:** Week over week is sensitive to one odd week (last week might have been a spike); it ignores seasonality. Same week last year adjusts for season but not for changes in the business or holiday dates that moved (for example a festival). The trailing average is smoother and the best test of "is this unusual", but lags a trend. Also compare the dip with the normal week-to-week spread, because -3% to -4% could be noise.
**Next step / recommendation:** Use the trailing average as the main anomaly baseline, same week last year for seasonal context and week over week as a quick alert; say which one you used. Here: a mild dip, worth a segment check but not an alarm.
**Likely follow-ups:** (1) Which to report? Whichever matches the decision, with the others as context. (2) What if a holiday moved? Align by event, not date.
**Common mistakes / traps:** Cherry-picking the baseline that tells the preferred story; ignoring holidays; not checking normal variation.

### Q38 ⭐⭐ 🟡 A single B2B order of INR 10 lakh is in the data this month. Revenue appears up 15%. What is the growth excluding it, and how do you report it?
Data: last month INR 80 lakh; this month INR 92 lakh including the one INR 10 lakh order.
**Asked at:** commonly asked (no company-specific report found); outliers and one-off deals are a standard trap (unverified).
**What the interviewer is checking:** Whether you separate a one-off from the underlying trend and report both transparently.
**Say this in the interview:** "Reported growth is 15%, but without the one order it is 2.5%. I would report both and explain."
**What the data shows:** 10 of the 12 lakh rise comes from one order.
**Working:**
1. Reported growth = (92 - 80) / 80 = 15%.
2. Excluding the order: 92 - 10 = INR 82 lakh.
3. Underlying growth = (82 - 80) / 80 = 2.5%.
4. The order is 10 / 92 = 10.9% of this month's revenue.
**Result:** 15% reported, 2.5% excluding the one-off.
**Caveats / what else I would check:** Is it truly one-off or a first order from a new recurring customer? Did last month contain a similar one (then the comparison is fair)? Is the order confirmed and delivered, not cancelled or pre-billed? Check the customer mix and whether the INR 10 lakh was a data entry error. Do not delete real revenue; show it separately.
**Next step / recommendation:** Report "INR 92 lakh, up 15%; excluding one INR 10 lakh B2B order, INR 82 lakh, up 2.5%". Add a rule for flagging large orders in the report and watch whether the customer reorders.
**Likely follow-ups:** (1) Exclude it permanently? No, show it as a separate line. (2) When is it not an outlier? If large deals are normal for the business.
**Common mistakes / traps:** Quietly dropping the order; celebrating 15%; deciding the outlier rule after seeing the result.

### Q39 ⭐⭐ 🟡 Customer acquisition cost rose. Calculate the change and decompose it into the spend and customer-count effects, then list what you would check.
Data: last month spend INR 10 lakh, 5,000 new customers; this month spend INR 12 lakh, 4,800 new customers.
**Asked at:** commonly asked (no company-specific report found); CAC and its drivers are a common marketing-analytics question (unverified).
**What the interviewer is checking:** Ratio decomposition and stating the order of the decomposition.
**Say this in the interview:** "CAC rose from INR 200 to INR 250, up 25%. Most of the INR 50 rise is higher spend (INR 40) and the rest is fewer customers (INR 10)."
**What the data shows:** Spend rose 20% while customers fell 4%.
**Working:**
1. Last month CAC = 10,00,000 / 5,000 = INR 200.
2. This month CAC = 12,00,000 / 4,800 = INR 250.
3. Change = +INR 50 (+25%).
4. Spend effect (new spend, old customers) = (12,00,000 - 10,00,000) / 5,000 = +INR 40.
5. Customer-count effect (new spend, new customers versus old) = 12,00,000 / 4,800 - 12,00,000 / 5,000 = 250 - 240 = +INR 10.
6. Check: 40 + 10 = 50.
**Result:** CAC +INR 50 (+25%): spend effect +INR 40, customer-count effect +INR 10. Doing the count effect first would give roughly INR 8.3 and INR 41.7, so quote it as "about 80% spend, 20% fewer customers".
**Caveats / what else I would check:** Spend by channel and campaign; blended versus channel CAC and mix (see Q40); attribution window and lag (spend today brings customers later); what counts as a "new customer" (first order or sign-up); whether incentives or brand spend are included; seasonality; and customer quality (are cheaper customers also lower value?). Check also whether the extra spend was planned for growth.
**Next step / recommendation:** Break CAC by channel, compare against payback and lifetime value, and decide where spend has stopped being efficient.
**Likely follow-ups:** (1) Is a higher CAC bad? Not if the customers are worth more. (2) Which effect is more actionable? The spend one: test where the extra money went.
**Common mistakes / traps:** Reading CAC without lifetime value; ignoring attribution lag; not stating the decomposition order.

### Q40 ⭐⭐ 🟡 Blended customer acquisition cost rose from INR 120 to INR 150 although no channel got more expensive. Show how, using the table.
Data:
| Channel | CAC | Customers, month 1 | Customers, month 2 |
|---|---|---|---|
| Search | INR 100 | 800 | 500 |
| Social | INR 200 | 200 | 500 |

**Asked at:** commonly asked (no company-specific report found); blended-versus-channel mix shifts are a standard "Simpson-style" trap (unverified).
**What the interviewer is checking:** That you see a mix shift toward the more expensive channel.
**Say this in the interview:** "Each channel's CAC is unchanged. The customers moved from cheap search to costlier social, so the blended average rose from INR 120 to INR 150."
**What the data shows:** Total customers are 1,000 in both months, but social's share went from 20% to 50%.
**Working:**
1. Month 1 spend = 800 x 100 + 200 x 200 = 80,000 + 40,000 = INR 1,20,000; blended CAC = 1,20,000 / 1,000 = INR 120.
2. Month 2 spend = 500 x 100 + 500 x 200 = 50,000 + 1,00,000 = INR 1,50,000; blended CAC = 1,50,000 / 1,000 = INR 150.
3. Rate effect (channel CAC changes) = 0, since both are unchanged.
4. Mix effect = +INR 30, the whole rise.
**Result:** Blended CAC +INR 30 (+25%), all from mix shift; channel CACs unchanged.
**Caveats / what else I would check:** Why did social grow (a campaign, search budget cut, less search volume)? Is channel CAC really constant or does it rise at higher volume (marginal versus average CAC)? Customer quality by channel (a costlier channel may bring better customers). In a real table CAC rarely stays exactly flat.
**Next step / recommendation:** Do not conclude marketing got less efficient; report channel CAC beside the blended CAC with a mix bridge, and judge channels by payback or lifetime value.
**Likely follow-ups:** (1) Is this Simpson's paradox? A related mix effect. (2) What action? Check whether the search volume dropped because of budget or a demand limit.
**Common mistakes / traps:** Reading blended CAC as efficiency; ignoring mix; assuming channel CAC stays flat at any scale.

### Q41 ⭐⭐ 🟡 Average salary in the HRIS report fell from INR 7.5 lakh to INR 7.0 lakh although nobody's pay changed. Show why with the numbers and explain what you would tell the CHRO.
Data: before, 50 seniors at INR 12 lakh and 150 juniors at INR 6 lakh. After a hiring drive: the same 50 seniors and 250 juniors at the same pay.
**Asked at:** commonly asked (no company-specific report found); mix-shift (Simpson's paradox style) questions appear on prep sites (unverified for any company).
**What the interviewer is checking:** Whether you see that an average can fall purely because the mix of people changed.
**Say this in the interview:** "Nobody's pay changed. The hiring drive added only juniors, so the senior share fell and the average fell with it. I would show averages by level, not one blended number."
**What the data shows:** The pay for each level is unchanged. Only the headcount mix changed.
**Working:**
1. Before: (50 x 12 + 150 x 6) / 200 = 1,500 / 200 = INR 7.5 lakh. Seniors are 50/200 = 25% of staff.
2. After: (50 x 12 + 250 x 6) / 300 = 2,100 / 300 = INR 7.0 lakh. Seniors are 50/300 = 16.7% of staff.
3. Senior pay (12) and junior pay (6) are identical in both months, so the whole INR 0.5 lakh drop is mix.
**Result:** Average fell by INR 0.5 lakh (6.7%) with zero change in anyone's pay. Rounded to 1 decimal.
**Caveats / what else I would check:** Confirm no leavers or promotions hid in the HRIS export; check the median and the grade-wise average; check whether new juniors are in the same band.
**Next step / recommendation:** Tell the CHRO: "Pay is stable at each level; the fall is because 100 junior joiners enlarged the junior group. For pay-fairness or budget questions we should report average pay by grade and headcount mix side by side, and use a fixed-mix comparison (today's pay at last month's headcount mix) when we want a like-for-like trend."
**Likely follow-ups:** (1) Would the median help? Here the median is 6 in both months, so yes, it stays steady, but it hides the senior mix change too. (2) What is the budget view? Total payroll rose from 1,500 to 2,100 (INR lakh per year, 40%), which is the real cost story.
**Common mistakes / traps:** Reporting "average salary fell" as if pay was cut; comparing blended averages across periods with different headcount mix.

### Q42 ⭐⭐ 🟡 After a hiring drive the average tenure dropped. Calculate the new average and explain how you would present tenure so it is not misread.
Data: 100 employees averaging 4.0 years of tenure; 50 new hires averaging 0.5 years join; nobody leaves.
**Asked at:** commonly asked (no company-specific report found); tenure and attrition metrics are standard HR analytics topics (unverified for any company).
**What the interviewer is checking:** Whether you know averages move mechanically with new joiners and can present tenure fairly.
**Say this in the interview:** "The new average is 2.83 years. The drop is arithmetic from 50 new hires, not people leaving. I would show tenure bands and the tenure of the existing group separately."
**What the data shows:** Existing staff still average 4.0 years; new joiners average 0.5 years.
**Working:**
1. Total tenure before: 100 x 4.0 = 400 years. New hires add 50 x 0.5 = 25 years.
2. New average = (400 + 25) / 150 = 2.83 years (2.8333, rounded).
3. Drop = 4.0 - 2.83 = 1.17 years (29%), with nobody leaving.
**Result:** Average tenure 2.83 years, down 1.17 years.
**Caveats / what else I would check:** Mean tenure is skewed by a few very long-serving staff; the median would be a better centre; "tenure" for leavers (see exits) is a different measure from tenure of current staff.
**Next step / recommendation:** Present (a) tenure bands (under 1 year, 1 to 3, 3 to 5, 5+) as percentages of headcount; (b) the median; (c) the average for employees who were here before the drive; (d) retention of the new cohort at 3, 6 and 12 months. Add a one-line note: "average fell because 33% of staff are new."
**Likely follow-ups:** (1) Is a lower average bad? No, it is a mix change. (2) Which number tracks retention? Cohort retention, not average tenure.
**Common mistakes / traps:** Reading falling average tenure as an attrition problem; reporting only the mean.

### Q43 ⭐⭐ 🟡 A test planned as a 50/50 split shows the allocation below, and the treatment metric looks worse. Calculate how far the split is from expected in standard deviations and say what you do.
Data: 100,000 users, planned 50/50; observed 52,000 control and 48,000 treatment.
**Asked at:** commonly asked (no company-specific report found); sample ratio mismatch (SRM) is a standard A/B testing check on prep sites (unverified for any company).
**What the interviewer is checking:** Whether you check the split is healthy before trusting any result.
**Say this in the interview:** "52,000 vs 48,000 looks small, but it is about 12.6 standard deviations from a fair 50/50. That is a sample ratio mismatch, so I do not trust the metric until I find the cause."
**What the data shows:** A 52/48 split out of 100,000 users, where 50,000 each was planned.
**Working:**
1. Expected: 50,000 control and 50,000 treatment.
2. Standard deviation of a fair split: square root of (100,000 x 0.5 x 0.5) = 158.1 users.
3. Gap: 52,000 - 50,000 = 2,000 users. 2,000 / 158.1 = 12.65 standard deviations (z-score).
4. Chance of such a gap by luck is effectively zero (below 1 in 10^30).
**Result:** z about 12.6; the split is broken, not random. Rounded to 1 decimal.
**Caveats / what else I would check:** Which users are missing from treatment (crashes, slower page load, bot filtering, redirects, logging failures, users who dropped before the event fired)? Check assignment logs against exposure logs; check by device, browser, country and new vs returning.
**Next step / recommendation:** Do not report "treatment is worse". Find the cause, fix it, and rerun or reanalyse on a clean assignment table. If treatment is losing users who would have behaved badly (or well), the comparison is biased in an unknown direction.
**Likely follow-ups:** (1) Is 50.5/49.5 also a problem? At 100,000 users, a 500 gap is 3.2 SD, so yes, worth checking. (2) Can you just reweight? Rarely; the missing users are not random.
**Common mistakes / traps:** Calling 52/48 "close enough"; analysing the result before checking randomisation.

### Q44 ⭐⭐ 🟡 Add-to-cart events fell sharply while orders stayed flat. Calculate the percentage fall and say what it suggests.
Data: add-to-cart events 50,000 last week, 32,500 this week; orders 5,000 both weeks. A new app version rolled out to 40% of users midweek.
**Asked at:** commonly asked (no company-specific report found); tracking-vs-behaviour questions appear on e-commerce analytics prep (unverified for any company).
**What the interviewer is checking:** Whether you use a steady downstream metric to detect a likely tracking bug.
**Say this in the interview:** "Add-to-cart fell 35%, but orders did not move. People still buy, so the likely cause is that the new app version stopped logging the event. I would check the data before treating it as a business problem."
**What the data shows:** Add-to-cart events fell; orders stayed flat; a release hit 40% of users midweek.
**Working:**
1. Fall = (50,000 - 32,500) / 50,000 = 35%.
2. Add-to-cart events per order: 50,000 / 5,000 = 10.0 before; 32,500 / 5,000 = 6.5 after.
3. If the whole loss of 17,500 events sits in the 40% of users on the new version (40% of 50,000 = 20,000 events), those users' events fell by 17,500 / 20,000 = 87.5% (an illustrative assumption, to be verified).
**Result:** 35% fall in add-to-cart, 0% change in orders; suggests broken event logging in the new version. Rounded.
**Caveats / what else I would check:** Split add-to-cart by app version and platform; compare orders per version; check the release notes and event schema; check whether the button moved (a UI change could change behaviour, but orders would likely move too).
**Next step / recommendation:** Raise it with the app and tracking team; label the dashboard "add-to-cart undercounted since release X"; ask for a fix and backfill if possible; do not report a funnel conversion drop meanwhile.
**Likely follow-ups:** (1) What if orders also fell? Then it is real or a wider tracking failure. (2) Which source is the truth? Backend order data.
**Common mistakes / traps:** Reporting a demand problem; ignoring the release; mixing app and web.

### Q45 ⭐⭐ 🟡 Is Sunday's figure a problem or normal? Use the day-of-week index below.
Data: the average day has 10,000 orders; Sunday's index is 0.8; this Sunday had 8,500 orders.
**Asked at:** commonly asked (no company-specific report found); day-of-week seasonality checks are a basic expectation (unverified for any company).
**What the interviewer is checking:** Whether you compare with the expected value for that weekday, not the weekly average.
**Say this in the interview:** "Sunday's expected figure is 8,000 (10,000 x 0.8). We got 8,500, so it is 6% above expectation. It is normal, even good."
**What the data shows:** Raw Sunday looks 15% below an average day, but Sundays are always lower.
**Working:**
1. Expected Sunday = 10,000 x 0.8 = 8,000 orders.
2. Actual = 8,500. Difference = +500 orders, or 8,500 / 8,000 - 1 = +6.25%.
3. Against an average day: 8,500 / 10,000 = 0.85, which is 15% below, but that is the wrong benchmark.
**Result:** Sunday is 6.25% above its expected level. Not a problem.
**Caveats / what else I would check:** How noisy are Sundays normally (use the past 8 to 12 Sundays to get a usual range)? Any holiday or promotion? Is the index recent (re-estimate as behaviour changes)?
**Next step / recommendation:** Report "vs same weekday" or a seasonally adjusted figure on the dashboard; alert on deviation from expected, not on raw level.
**Likely follow-ups:** (1) How do you build the index? Average each weekday's orders over several weeks divided by the overall daily average. (2) What range counts as normal? Compare against past Sunday variation, for example the spread of the last 10 Sundays.
**Common mistakes / traps:** Comparing a Sunday with a Wednesday; using a single week to judge.

### Q46 ⭐⭐ 🟡 Two sales reps' attainment is averaged in two different ways and gives different answers. Calculate both and say which to report.
Data: Rep A quota 100, achieved 120; Rep B quota 400, achieved 360 (units of INR lakh).
**Asked at:** commonly asked (no company-specific report found); averaging ratios is a common trap on analytics prep (unverified for any company).
**What the interviewer is checking:** Whether you know that averaging ratios ignores their size.
**Say this in the interview:** "Averaging the two attainment percentages gives 105%; dividing total achieved by total quota gives 96%. I report 96%, because that is what the team actually delivered against its target."
**What the data shows:** Rep A beat a small quota; Rep B missed a big one.
**Working:**
1. Rep A attainment = 120 / 100 = 120%. Rep B = 360 / 400 = 90%.
2. Simple average of the ratios = (120% + 90%) / 2 = 105%.
3. Weighted (pooled) attainment = (120 + 360) / (100 + 400) = 480 / 500 = 96%.
**Result:** 105% (simple) vs 96% (weighted). Team is 4% short of target.
**Caveats / what else I would check:** Are quotas fair across reps? Are targets set by territory size? Is the unit identical (INR lakh)? State the definition on the report.
**Next step / recommendation:** Report team attainment as total achieved / total quota (96%) and show each rep's own ratio next to it.
**Likely follow-ups:** (1) When is the simple average ok? When all quotas are equal. (2) Name the effect? Weighted vs unweighted mean, similar to the mix problem in Q41.
**Common mistakes / traps:** Averaging percentages and telling management the team beat target.

### Q47 ⭐⭐ 🟡 Churn fell from 5% to 4.0% and a manager calls it an improvement. Check the figures and give your view.
Data: last month 500 churned of 10,000 customers; this month 520 churned of 13,000 customers.
**Asked at:** commonly asked (no company-specific report found); churn definition and denominator questions are common (unverified for any company).
**What the interviewer is checking:** Whether you see that a rate can fall while the count rises, and test the denominator.
**Say this in the interview:** "The percentages are right, 5.0% and 4.0%, but actual churners rose from 500 to 520. The rate fell because the base grew, so I would first check whether 13,000 is the right denominator."
**What the data shows:** More people left, but from a bigger base.
**Working:**
1. Last month: 500 / 10,000 = 5.0%.
2. This month: 520 / 13,000 = 4.0%.
3. Churners rose by 20 (4%); customer base rose by 3,000 (30%).
**Result:** Arithmetic is correct. Whether it is an improvement depends on the denominator.
**Caveats / what else I would check:** Churn should be leavers divided by customers at the start of the period. If 13,000 includes customers acquired during the month, the rate is diluted. Also check: were the new customers recently acquired (they churn differently)? Are churn definitions the same both months? Is churn by cohort age (tenure) improving?
**Next step / recommendation:** Recompute using the start-of-month base (the data gives no such figure, so I would ask for it); show churn by customer age; present as "churn is 4.0% on the current basis; before calling it better I want the same-definition comparison."
**Likely follow-ups:** (1) Is a flat count of churners a good sign? Not by itself. (2) Use cohort retention for a cleaner view.
**Common mistakes / traps:** Celebrating a lower rate caused by a bigger denominator; using end-of-period customers as the base.

### Q48 ⭐⭐ 🟡 A subscription price rose and churn rose with it. Is revenue better or worse next month?
Data: 10,000 subscribers at INR 199 before; price rises to INR 249; monthly churn rises from 3% to 4.5%. Compare revenue from retained subscribers next month with this month's revenue.
**Asked at:** commonly asked (no company-specific report found); price-elasticity and churn trade-offs appear on prep sites (unverified for any company).
**What the interviewer is checking:** Whether you do the revenue arithmetic and also think past one month.
**Say this in the interview:** "Next month's revenue from the retained subscribers is about INR 23.8 lakh against INR 19.9 lakh now, about 19% higher. But if churn stays at 4.5%, the long-run value of each subscriber is lower."
**What the data shows:** The price rose 25% while churn rose 1.5 points.
**Working:**
1. This month: 10,000 x 199 = INR 19,90,000.
2. Retained next month: 10,000 x (1 - 0.045) = 9,550 subscribers.
3. Revenue = 9,550 x 249 = INR 23,77,950; that is +19.5% vs this month.
4. If there had been no price change: 9,700 x 199 = INR 19,30,300, so the price rise adds about INR 4.48 lakh relative to that.
5. Break-even: 199 / 249 = 79.9%, so churn would have to reach about 20.1% for revenue to be flat.
**Result:** Revenue is better next month by about INR 3.88 lakh (+19.5%). Rounded.
**Caveats / what else I would check:** Longer view: if 4.5% churn persists, expected lifetime is 1/0.045 = 22.2 months, so revenue per subscriber over life is 249 x 22.2 = INR 5,533 vs 199 x 33.3 = INR 6,633 before. Churn can rise further after the first bill; new sign-ups may fall; price rise may not apply to everyone.
**Next step / recommendation:** Recommend keeping the price if churn is a one-time bump, and track churn weekly for three months; compare cohorts.
**Likely follow-ups:** (1) What would worry you? Churn that keeps rising. (2) What about margin? Revenue is not profit; check support and acquisition cost.
**Common mistakes / traps:** Stopping at one month; mixing up percentage-point (1.5 points) and percent change (50% relative).

### Q49 ⭐⭐ 🟡 NPS apparently fell from 40 to 35. Calculate this month's NPS and say whether you would act on the change.
Data: last month 400 responses (200 promoters, 40 detractors). This month 40 responses (18 promoters, 4 detractors).
**Asked at:** commonly asked (no company-specific report found); NPS and eNPS sample-size questions appear on prep sites (unverified for any company).
**What the interviewer is checking:** Whether you calculate the score and judge noise from a tiny sample.
**Say this in the interview:** "This month's NPS is 35 on 40 responses; it is a 5-point fall, but the uncertainty on 40 responses is about plus or minus 20 points, so I would not act on it yet."
**What the data shows:** Last month's survey had 400 responses and this month's only 40.
**Working:**
1. NPS (Net Promoter Score) = % promoters (customers scoring 9 to 10 on "would you recommend us?") minus % detractors (scoring 0 to 6), so it runs from -100 to +100.
2. Last month: 200/400 = 50% and 40/400 = 10%, so NPS = 40.
3. This month: 18/40 = 45% and 4/40 = 10%, so NPS = 35.
4. Approx 95% margin of error: last month about plus or minus 6.5 points; this month about plus or minus 20.3 points (normal approximation, 1.96 x standard error).
**Result:** NPS 35 (down 5 points), well inside the noise. Rounded to 1 decimal.
**Caveats / what else I would check:** Why did responses fall 90%? Who answered (response bias)? Was the survey sent to the same people? Is the drop in promoters or in detractors (promoters 50% to 45%, detractors flat at 10%)?
**Next step / recommendation:** Do not act or report a decline. Say "NPS 35, not statistically different from 40"; collect more responses and look at the trend over several periods.
**Likely follow-ups:** (1) How many responses are needed? Several hundred for a margin of a few points. (2) Is it still useful? Read the comments qualitatively.
**Common mistakes / traps:** Reacting to a 5-point move on 40 responses; comparing samples of different size without error bars.

### Q50 ⭐⭐ 🟡 Conversion looks like it dropped from 2.0% to 1.54% after a traffic spike. Calculate the conversion after removing suspected bot sessions and list your checks.
Data: last week 100,000 sessions and 2,000 orders. This week 130,000 sessions and 2,000 orders; 25,000 sessions are suspected bots.
**Asked at:** commonly asked (no company-specific report found); bot-traffic and conversion-denominator questions appear on e-commerce prep (unverified for any company).
**What the interviewer is checking:** Whether you adjust the denominator and still check whether a residual drop is real.
**Say this in the interview:** "Removing the 25,000 suspected bot sessions gives 2,000 / 105,000 = 1.90%, so most of the drop disappears. A small gap of 0.1 point remains, and I would test whether it is real."
**What the data shows:** Orders are flat at 2,000 while sessions rose.
**Working:**
1. Last week: 2,000 / 100,000 = 2.00%.
2. This week raw: 2,000 / 130,000 = 1.54%.
3. Remove suspected bots: 130,000 - 25,000 = 105,000 sessions; 2,000 / 105,000 = 1.90% (assuming bots placed no orders).
4. Remaining gap: 2.00% - 1.90% = 0.10 percentage points (about 4.8% relative). A two-proportion z-test gives about 1.6, which is not significant at the usual 5% level.
**Result:** Cleaned conversion 1.90%; most of the fall is bots. Rounded.
**Caveats / what else I would check:** How were bots flagged (user agent, IP, no engagement, one-page sessions)? Were last week's bots removed with the same rule? Traffic source of the spike (a paid campaign with low-intent visitors changes the mix); device and landing page split; any real site issue.
**Next step / recommendation:** Ask the data team to filter bots consistently in history and going forward; report conversion on human sessions with both numbers shown; segment by channel.
**Likely follow-ups:** (1) What if bots did place orders? Remove those too. (2) Should the spike be blocked? Ask the security team.
**Common mistakes / traps:** Removing bots only from this week; assuming the entire gap closes.

### Q51 ⭐⭐ 🟡 Cohort retention for April looks much worse. Calculate the gap and say what you would check first.
Data (month-1 retention by signup cohort): January 40%, February 41%, March 39%, April 31%.
**Asked at:** commonly asked (no company-specific report found); cohort retention is a core product-analytics topic (unverified for any company).
**What the interviewer is checking:** Whether you first check the cohort is complete and comparable before alarming anyone.
**Say this in the interview:** "April is 9 points below the January to March average of 40%. Before reacting I would check that April's month-1 window has fully elapsed and has been measured the same way."
**What the data shows:** January to March sit tightly at 39 to 41%; April is 31%.
**Working:**
1. Jan to March average = (40 + 41 + 39) / 3 = 40.0%.
2. Gap: 31% - 40% = -9 percentage points, a 22.5% relative drop.
3. The normal spread is only about 2 points (39 to 41%), so April is well outside it.
**Result:** April is 9 percentage points (22.5% relative) below the earlier cohorts. Rounded.
**Caveats / what else I would check, in order:** (1) Is the cohort mature? If the data was pulled before every April signup completed 30 days, retention is understated. (2) Is the definition identical (active means the same action)? (3) Tracking or release changes. (4) Acquisition mix: a new channel or discount campaign can bring low-intent users. (5) Product or pricing changes in April.
**Next step / recommendation:** Wait or re-pull once the cohort is complete; segment April by channel, device and plan; compare day-7 and day-14 retention for an early read.
**Likely follow-ups:** (1) What if still low? Treat it as real and segment. (2) How would you show it? A cohort table.
**Common mistakes / traps:** Comparing an incomplete cohort with complete ones; ignoring channel mix.

### Q52 ⭐⭐ 🟡 Marketing says yesterday's conversions are poor. How do you account for attribution lag? Estimate the eventual total.
Data: historically 50% of conversions arrive within 1 day of the click, 80% within 3 days, 100% within 7 days. Yesterday's clicks have 400 conversions so far.
**Asked at:** commonly asked (no company-specific report found); attribution and conversion lag appear in marketing analytics prep (unverified for any company).
**What the interviewer is checking:** Whether you know recent data is incomplete and you scale up using the historical curve.
**Say this in the interview:** "If half of conversions normally arrive within a day, yesterday's 400 conversions imply about 800 eventually. Comparing it with fully matured days would be unfair."
**What the data shows:** Conversions arrive over seven days after a click, so recent days look low.
**Working:**
1. Historical curve: 50% by day 1, 80% by day 3, 100% by day 7.
2. Assuming yesterday's clicks have been observed for 1 day: eventual = 400 / 0.50 = 800 conversions.
3. Still to come: 800 - 400 = 400 (expected 240 more by day 3, 160 more by day 7).
4. If the data had been 3 days old, eventual would be 400 / 0.80 = 500.
**Result:** Estimated eventual total about 800 conversions (state the assumption about the age of the data). Rounded.
**Caveats / what else I would check:** The curve may differ by channel and day (a sale weekend); small numbers give wide ranges; the estimate is a projection, not a fact.
**Next step / recommendation:** Compare each day's conversions after the same number of days (day 1 vs day 1), or use a projected figure with a range; tell marketing to wait 7 days before judging; show matured and projected figures separately.
**Likely follow-ups:** (1) How would you check the estimate? Compare past projections with the final values. (2) What if the curve changed? Refresh it.
**Common mistakes / traps:** Judging a campaign on yesterday's partial data; mixing click date and conversion date.

### Q53 ⭐⭐ 🟡 Biometric-recorded attendance dropped after a new device was installed at gate 2. Estimate how many employees are affected and what you would do.
Data: 500 employees; recorded attendance fell from 94% to 86% starting the day the device was installed; 40 employees use gate 2.
**Asked at:** commonly asked (no company-specific report found); HR attendance data-quality scenarios are a typical gap-fill for HR candidates (unverified for any company).
**What the interviewer is checking:** Whether you connect the drop to a system change and protect employees from wrong pay or discipline actions.
**Say this in the interview:** "The drop is 8 points, or 40 of 500 employees, which matches the 40 who use gate 2. It is probably the device not recording them, not 40 people suddenly absent."
**First, clarify / contain:** Ask IT and security when the device went live and who uses gate 2. Do not mark absences, apply loss of pay, or send attendance warnings for these people yet.
**What I would check, in order:**
1. Size: 94% to 86% = 8 points x 500 = 40 employee-days a day. Gate 2 users: 40, so nearly all of them look missing (if they normally attend at 94%, about 38 are lost).
2. Gate-2 users' attendance before and after versus users of other gates (should be unchanged).
3. Device logs: failed reads, wrong time zone or clock, enrolment of fingerprints or cards, duplicate IDs.
4. Whether people used another source (swipe records, laptop login, manager approval).
**If I find...:** Gate-2 users near 0% recorded and others unchanged: device or enrolment fault; fix it and regularise attendance. Gate-2 drop is partial: sync or connectivity problems. Other gates dropped too: wider issue, escalate.
**What I would tell the stakeholder:** "Attendance fell 8 points on the day gate 2 got its new device. All 40 gate-2 users appear affected, so I believe it is a recording fault. I am holding payroll deductions for them, asking IT to check the device, and will update by end of day tomorrow."
**Prevent it next time:** Pilot new devices in parallel with the old ones; add an attendance-per-gate monitor with alerts.
**Likely follow-ups:** (1) Is the exact number 40? About 38 to 40 if their normal attendance is 94%. (2) Who tells employees? HR with IT, in writing.
**Common mistakes / traps:** Treating it as a real attendance problem; applying pay deductions before verifying.

### Q54 ⭐⭐ 🟡 Refund rate jumped from 2% to 5%. Calculate the rate excluding the outlier product and say what you would do.
Data: this week 2,000 refunds on 40,000 orders. Product X alone has 1,100 refunds on 1,500 orders.
**Asked at:** commonly asked (no company-specific report found); outlier-product refund investigations are a standard e-commerce case (unverified for any company).
**What the interviewer is checking:** Whether you isolate a concentrated driver and still check what remains.
**Say this in the interview:** "Product X has 1,100 refunds on 1,500 orders, a 73% refund rate. Without it the refund rate is 2.3%, so nearly all the jump comes from one product."
**What the data shows:** One product produces over half of all refunds.
**Working:**
1. Overall: 2,000 / 40,000 = 5.0%.
2. Product X: 1,100 / 1,500 = 73.3% refund rate; it is 3.75% of orders but 55% of refunds.
3. Excluding X: (2,000 - 1,100) / (40,000 - 1,500) = 900 / 38,500 = 2.34%.
4. Taking X out lowers the overall rate from 5.00% to 2.34%, so X accounts for about 2.66 of the 3.0-point jump. The other products sit 0.34 points above the old 2.0% level.
**Result:** Rate without Product X is 2.34% (2.0% before). Rounded.
**Caveats / what else I would check:** Why is X refunded: defect, wrong listing, a supplier or batch problem, fraud, courier damage? Are refunds recorded in the week of the order or of the refund? Is the 0.34-point residual noise or another issue?
**Next step / recommendation:** Pause or flag the product with the category owner, review the listing and reviews, check the batch and the seller; report the refund rate with and without X until resolved; consider a refund-rate alert by product.
**Likely follow-ups:** (1) Would you just remove X from reports? No, disclose it. (2) How to track? Daily product-level refund rate.
**Common mistakes / traps:** Dropping the outlier silently; not asking why.

### Q55 ⭐⭐ 🟡 Delivery-partner attrition rose from 6% to 8%. Which tenure group explains the rise?
Data (leavers per month, base 1,500 partners): under 30 days' tenure 50 last month, 85 this month; 30 days or more 40 last month, 35 this month.
**Asked at:** commonly asked (no company-specific report found); attrition by tenure is a standard HR analytics breakdown (unverified for any company).
**What the interviewer is checking:** Whether you segment the leavers and compare each group's change.
**Say this in the interview:** "The rise is in partners under 30 days' tenure: 50 to 85 leavers. Longer-tenure leavers actually fell from 40 to 35."
**What the data shows:** Early-tenure exits explain the rise.
**Working:**
1. Last month total: 50 + 40 = 90 leavers; 90 / 1,500 = 6.0%.
2. This month total: 85 + 35 = 120 leavers; 120 / 1,500 = 8.0%.
3. Change: +30 leavers. Under 30 days: +35. 30 days or more: -5.
4. Early-tenure change is 35 / 30 = 117% of the net rise (1,500 base assumed unchanged).
**Result:** The under-30-days group explains the entire 2-point rise. Rounded.
**Caveats / what else I would check:** Headcount of each tenure group is not given; the early-tenure group's own attrition rate needs its denominator (a bigger onboarding intake raises exits even at a steady rate). Ask: city, hiring source, incentives, onboarding, training, payout timing.
**Next step / recommendation:** Check the onboarding experience, first-week earnings, joining incentives and the recruiting channel; track 30-day retention by hiring cohort.
**Likely follow-ups:** (1) Why not look at the overall rate only? It hides the cause. (2) What does "tenure group" help with? It points to hiring and onboarding, not the experienced workforce.
**Common mistakes / traps:** Treating attrition as one number; reading counts without bases.

### Q56 ⭐⭐ 🟡 Overall conversion fell from 3.75% to 2.85% with no change in any segment's conversion. Show how with the numbers.
Data: new users convert at 1.5% and returning users at 6.0% in both weeks; new users were 50% of sessions last week and 70% this week.
**Asked at:** commonly asked (no company-specific report found); Simpson's paradox and mix shift are classic analytics-interview topics (unverified for any company).
**What the interviewer is checking:** Whether you separate rate change from mix change.
**Say this in the interview:** "No segment got worse. The traffic simply shifted toward new users, who convert less, so the blended rate fell."
**What the data shows:** Segment conversions are constant; the session mix changed.
**Working:**
1. Last week: 0.5 x 1.5% + 0.5 x 6.0% = 0.75% + 3.00% = 3.75%.
2. This week: 0.7 x 1.5% + 0.3 x 6.0% = 1.05% + 1.80% = 2.85%.
3. Fall = 0.90 percentage points (24% relative).
4. Rate effect = 0 (segment rates unchanged), so the full 0.90 points is mix effect.
**Result:** Overall conversion fell 3.75% to 2.85% purely from mix. Rounded.
**Caveats / what else I would check:** Why did new-user share jump (a campaign, an SEO change, fewer returning users)? Are new users lower quality or only earlier in the journey? Is traffic growth worth it despite the lower rate?
**Next step / recommendation:** Report conversion by segment with the session mix next to it; use a fixed-mix benchmark (e.g. last week's 50/50 mix) for trend lines.
**Likely follow-ups:** (1) Is this Simpson's paradox? It is the mix effect behind it. (2) Is anything to fix? Maybe returning-user traffic fell; investigate.
**Common mistakes / traps:** Searching for a product bug; mixing percent with percentage points.

### Q57 ⭐⭐ 🟡 Sales rise every October and fall in November. How do you separate festival seasonality from the underlying trend?
**Asked at:** commonly asked (no company-specific report found); seasonality adjustment is a standard time-series topic (unverified for any company).
**What the interviewer is checking:** Whether you know how to compare like with like across seasons.
**Say this in the interview:** "I would compare each October with last year's October and use several years of data to estimate the seasonal pattern, so what is left is the trend."
**Clarify first:** What decision is it for (forecast, targets, reading a recent dip)? How many years of history do we have, and does Diwali (a moving date) shift between October and November?
**Plan:**
1. Plot monthly sales for at least 2 to 3 years; mark festival dates.
2. Year-over-year (YoY) growth: October vs last October. This removes seasonality without modelling.
3. Build seasonal indices: each month's sales divided by the yearly average; divide actuals by the index for a deseasonalised series.
4. Trend: a 12-month rolling total or average.
5. Check the festival timing shift by moving to weekly or festival-aligned windows.
**Method choice and why:** YoY and index division first (explainable). If more is needed, use a decomposition (trend plus seasonal plus remainder, such as STL) or a regression with festival flags.
**Pitfalls:** Only one year of data; a festival moving between months; promotions and price changes that are not seasonal; calling the November fall a decline.
**Deliverable:** A chart of actual, seasonally adjusted and trend lines, plus the plain sentence "underlying sales are up x% after adjusting for the festival season", with the method stated.
**Likely follow-ups:** (1) How many years? At least two full cycles. (2) Why not month on month? It mixes the season in.
**Common mistakes / traps:** Month-on-month comparison across the festival; assuming festival timing is fixed.

### Q58 ⭐⭐ 🟡 What is the difference between investigating a sudden step-change and a gradual drift in a metric, and how does your approach change?
**Asked at:** commonly asked (no company-specific report found); step-change vs drift is a common metric-diagnosis distinction (unverified for any company).
**What the interviewer is checking:** Whether you use the shape of the change as a clue.
**Say this in the interview:** "A step is a sudden jump on a date, so I look for what changed that day: a release, a tracking change, a pipeline job. A drift is slow, so I look for gradual causes such as mix shift, ageing cohorts, or competitors."
**Clarify first:** The metric definition, the date range, and whether the data source changed.
**Plan:**
1. Plot the daily series; find the exact date of any break.
2. Step: build a timeline of releases, campaigns, config, tracking and pipeline changes; split before/after by device, country and version; check data logging; confirm with the source system.
3. Drift: break down by segment over time (mix), cohort age, channel; test whether the average is moving or only a subgroup; compare with seasonality; check definitions and slow data decay (for example consent rates).
4. Quantify with decomposition and test with an experiment or a rollback where possible.
**Method choice and why:** Steps are best explained by a changelog and a before/after cut (fast, binary). Drifts need trend analysis and segment decomposition (slower, many small causes).
**Pitfalls:** Calling a drift a step because of one noisy day; ignoring that a step in only one segment can look like a drift in the total.
**Deliverable:** A timeline chart with annotations, ranked causes with evidence and an owner.
**Likely follow-ups:** (1) Alert type? Threshold for steps, trend or control-chart rules for drifts. (2) Fastest check for a step? Data pipeline and tracking, before business causes.
**Common mistakes / traps:** Starting with business theories before validating the data.

### Q59 ⭐⭐ 🟡 Tracked sessions dropped 20% after a cookie-consent banner went live while backend orders are unchanged. How do you restate the metric and what do you tell the business?
**Asked at:** commonly asked (no company-specific report found); consent-banner tracking loss is a common web-analytics issue (unverified for any company).
**What the interviewer is checking:** Whether you separate a measurement change from a behaviour change and restate the metric honestly.
**Say this in the interview:** "Orders did not change, so customers did not change; our tracking sees fewer of them. I would label the break, anchor reporting to backend numbers, and estimate the true sessions rather than present a 20% fall."
**Clarify first:** The banner go-live date, the countries affected, and what is blocked (analytics cookies only?). Do not announce a traffic problem yet.
**Plan:**
1. Confirm the break date aligns with the banner and that the drop appears across channels.
2. Anchor on untouched sources: backend orders, server logs, payment data.
3. Estimate the missing share: tracked sessions are 80% of before, so an indicative scale factor is 1 / 0.8 = 1.25 (assuming the lost sessions behave like the tracked ones, which is rarely exactly true).
4. Illustration: 5,000 orders on 100,000 sessions is 5.0% conversion; with 80,000 tracked sessions the apparent conversion is 6.25%. The true figure is still near 5.0%.
5. Restate history with a flag, or track "before consent" and "after consent" as separate series.
**Method choice and why:** Use backend orders as the anchor and scale or model sessions; consented users may not represent all users (differs by region and device).
**Pitfalls:** Reporting a 20% traffic drop, or inflating conversion by dividing orders by missing sessions, or using scale factors without checking by region.
**Deliverable:** A one-line note on the dashboard, "Tracked sessions are about 20% lower since [date] due to the consent banner; orders unchanged", plus an adjusted series.
**Likely follow-ups:** (1) What do you tell marketing? Channel metrics based on cookies are understated. (2) Legal view? Consent rules are for the legal team to confirm.
**Common mistakes / traps:** Treating the fall as real; ignoring that consent rates vary by user group.

### Q60 ⭐⭐ 🟡 The engagement survey's eNPS fell sharply and the response rate fell too. How do you decide whether the fall is real?
Data: 1,200 employees invited. Last survey 900 responded; this survey 300 responded.
**Asked at:** commonly asked (no company-specific report found); survey response bias is a standard HR analytics topic (unverified for any company).
**What the interviewer is checking:** Whether you see that a falling response rate can change both the score and its reliability.
**Say this in the interview:** "Response fell from 75% to 25%, so before I believe the fall I need to know who stopped answering. I would compare respondent mix and look at the margin of error."
**What the data shows:** The sample is one third of its former size, and non-response is large.
**Working:**
1. Response rate: 900 / 1,200 = 75% last time; 300 / 1,200 = 25% now.
2. Worst-case margin of error on eNPS (employee Net Promoter Score, the same promoter-minus-detractor score asked of staff, from -100 to +100): 900 responses give about plus or minus 6.5 points; 300 give about plus or minus 11.3 points (95%, normal approximation; the real value is smaller if many answers are neutral).
3. Seventy-five percent of staff did not answer now, so non-response bias is the bigger risk.
**Result:** Without the actual eNPS values, only a fall bigger than about 11 points on 300 responses can be called statistically real, and even then only for the people who answered.
**Caveats / what else I would check:** Mix of respondents versus employee population by department, tenure, location and grade; whether the invitation, reminders, survey length or timing changed; anonymity concerns; whether disengaged people are more or less likely to respond.
**Next step / recommendation:** Reweight to the employee mix (post-stratify) as a sensitivity check; compare like for like (same groups); follow up non-respondents with short pulse checks; report eNPS with response rate and range; read the comments.
**Likely follow-ups:** (1) Can you just compare? Only after matching the mix. (2) What would you tell leadership? "Directionally concerning, not yet confirmed."
**Common mistakes / traps:** Treating respondents as the whole company; reporting a score without a response rate.

### Q61 ⭐⭐ 🟡 How do you decide whether a statistically significant dip is big enough to matter to the business?
**Asked at:** commonly asked (no company-specific report found); "noise vs signal" is a recurring theme in the question banks found (unverified).
**What the interviewer is checking:** That you separate "statistically significant" (probably not chance) from "practically significant" (big enough to act on).
**Say this in the interview:** "Significant only means the dip is unlikely to be luck. I then convert it into rupees or people and compare it with what the business would do differently."
**Clarify first:** Which metric, what decision does it feed (stop a campaign, hire, escalate), and what size of change would the owner call material?
**Plan:**
1. Confirm the dip is real (p-value or confidence interval) and the data is clean.
2. Express the size two ways: relative and absolute. Example (exercise numbers): conversion falls from 5.0% to 4.6%, a drop of 0.4 percentage points, or 8% relative.
3. Convert to money: with 20,00,000 visitors a month and an order value of 1,500 rupees, that is 8,000 fewer orders, about 1.2 crore rupees a month (rounded).
4. Compare with a threshold agreed beforehand (cost of the fix, normal week-to-week swing, target tolerance).
5. Check persistence: one week or a trend?
**Method choice and why:** A confidence interval beats a bare p-value because it shows the plausible range of loss. With huge samples even a tiny dip is "significant", so size matters more than the p-value.
**Pitfalls:** Treating p < 0.05 as "important"; mixing percent and percentage points; ignoring that a small dip on a very large base can still be costly.
**Deliverable:** One line: "Dip of 0.4 points (8%), about 1.2 crore a month; above or below our action threshold; recommend X."
**Likely follow-ups:** 1) *What if it is not significant but large?* Possibly too little data; say "inconclusive", not "no effect", and collect more. 2) *Who sets the threshold?* The business owner, agreed before looking.
**Common mistakes / traps:** Equating significance with importance; reporting only relative change; no money translation.

### Q62 ⭐⭐ 🔴 A price rise and a marketing campaign launched the same week. Estimate the price effect with the regions below and state your assumptions.
Data (revenue index, before to after): Region A (price rise and campaign) 100 to 112; Region B (campaign only) 100 to 106; Region C (neither) 100 to 101.
**Asked at:** commonly asked (no company-specific report found); separating two overlapping changes appears in the price-volume and causal items of the question banks found (unverified).
**What the interviewer is checking:** That you can use comparison regions to peel overlapping effects apart and state what you had to assume.
**Say this in the interview:** "Region A minus Region B isolates the price rise, because both had the campaign. That gives about 6 index points, if the assumptions hold."
**What the data shows:** All three regions grew, even the untouched one (C, plus 1). So some growth is background (season, trend). B adds the campaign on top; A adds campaign and price.
**Working:**
1. Changes: A +12, B +6, C +1 index points.
2. Campaign effect = B minus C = 6 - 1 = 5 points.
3. Price effect = A minus B = 12 - 6 = 6 points (this is difference-in-differences: change in the treated region minus change in the comparison region).
4. Check: background 1 + campaign 5 + price 6 = 12, matches A.
5. In percentage terms (multiplicative version): 1.12 / 1.06 - 1 = 5.7% for price; 1.06 / 1.01 - 1 = 5.0% for campaign.
**Result:** Price effect on revenue is about +6 index points (about +5.7% in the multiplicative version), rounded. Campaign about +5 points.
**Caveats / what else I would check:** Assumptions: the regions would have moved in parallel without the changes; the campaign works equally in A and B; the price and campaign effects simply add up (no interaction); no spillover between regions. Revenue mixes price and volume: a price rise lifting revenue 6 points does not say volume held; check units sold. One week is short; check a longer window.
**Next step / recommendation:** Look at units and customer churn by region, and run the comparison over several weeks before concluding the rise paid off.
**Likely follow-ups:** 1) *What if the price rise cut volume?* Then revenue gain understates the unit-price effect; report units and revenue separately. 2) *What if A was a bigger region?* Parallel trends may fail; compare pre-period trends.
**Common mistakes / traps:** Using A minus C (11) and calling it all price; ignoring that C also grew; hiding the assumptions.

### Q63 ⭐⭐ 🔴 Revenue in INR rose 2.4% but USD revenue is flat. What happened, and how do you report it?
Data: USD revenue 10,00,000 in both months; exchange rate 82 to 84 INR per USD.
**Asked at:** commonly asked (no company-specific report found); the currency effect is a gap-fill item beyond common question-bank themes (judgement).
**What the interviewer is checking:** That you separate real business growth from exchange-rate translation.
**Say this in the interview:** "Nothing changed in the business. The same 10 lakh dollars is worth more rupees because the rupee weakened. I would report constant-currency revenue next to the reported figure."
**What the data shows:** Dollar sales are identical; only the conversion rate moved.
**Working:**
1. Month 1: 10,00,000 x 82 = 8,20,00,000 rupees (8.2 crore).
2. Month 2: 10,00,000 x 84 = 8,40,00,000 rupees (8.4 crore).
3. Growth = 84 / 82 - 1 = 2.44%, which matches the 2.4% (rounded).
4. Rise in rupees: 20,00,000 (20 lakh), all from exchange rate.
**Result:** INR revenue up 2.4% (2.44% before rounding); constant-currency growth is 0%. The rupee lost 2.38% of its dollar value (1 - 82/84), which is a slightly different figure from the 2.44% INR gain.
**Caveats / what else I would check:** Which rate: month-end, average or booked rate; the finance policy decides. Costs in dollars would rise too, so margin may fall. Check whether the customers' contracts are in USD or INR.
**Next step / recommendation:** Show two lines: reported INR and constant-currency (both months at one fixed rate), with the currency effect as its own bar. Agree the rate policy with finance.
**Likely follow-ups:** 1) *Is this real growth?* No, it is translation. 2) *Is the currency gain good?* Only for the rupee view; hedging and costs decide the net.
**Common mistakes / traps:** Celebrating 2.4% growth; mixing average and closing rates; not labelling the currency on the chart.

### Q64 ⭐⭐ 🔴 How would you set up automated monitoring so that metric drops are caught by alerts rather than by stakeholders? Cover thresholds, seasonality and alert fatigue.
**Asked at:** commonly asked (no company-specific report found); monitoring and anomaly-alert design appears as a differentiator topic in the sources (judgement).
**What the interviewer is checking:** That you design alerts people will trust: right metrics, sensible thresholds, few false alarms.
**Say this in the interview:** "I monitor a small set of key metrics against a seasonal baseline, alert on meaningful deviations, route each alert to an owner, and review noisy alerts every month."
**Clarify first:** Which metrics matter, who acts, how fast must they know (hourly, daily), and what does a drop cost?
**Plan:**
1. Pick few metrics (the top of the metric tree) plus data-health checks: row counts, freshness, nulls.
2. Baseline: compare with the same weekday in previous weeks, not yesterday, so weekly seasonality does not trigger alarms.
3. Thresholds: start with a simple rule (for example a drop beyond a few standard deviations of recent same-weekday values, or beyond a business-agreed percentage). Tune using past history: how many alerts would it have fired?
4. Known events (festivals, sales, holidays) go in a calendar that adjusts expectations.
5. Severity levels: warn vs page; each alert names an owner and a first check.
6. Alert fatigue control: group related alerts, suppress repeats, require persistence for two periods, review alert hit rate monthly and retire noisy ones.
**Method choice and why:** Rules on a seasonal baseline first; machine-learning detection only if rules fail. Simple rules are explainable.
**Pitfalls:** Too many alerts so people ignore them; fixed thresholds that ignore weekends; monitoring only the metric, not the pipeline behind it.
**Deliverable:** A monitoring sheet: metric, baseline method, threshold, owner, severity, runbook link, and a monthly alert review.
**Likely follow-ups:** 1) *How do you test thresholds?* Replay them on last year's data and count false and missed alerts. 2) *Who is paged?* The metric owner first.
**Common mistakes / traps:** One threshold for everything; no owner; never reviewing alerts.

### Q65 ⭐ 🟢 A stakeholder asks you to just fix the number because it looks wrong. When do you refuse, and how do you say it?
**Asked at:** commonly asked (no company-specific report found); stakeholder-pressure and ethics prompts are gap-fill items (judgement).
**What the interviewer is checking:** Integrity: you will correct errors, but never edit numbers to match expectations.
**Say this in the interview:** "I will always check a number that looks wrong, but I will not change it without evidence. If the data is right, I explain it; if it is wrong, I fix the cause and document it."
**First, clarify / contain:** Ask why it looks wrong and what they expected, with source. Do not overwrite anything yet.
**What I would check, in order:**
1. Reproduce the number and its definition.
2. Compare with their expectation: different definition, date or filter?
3. Trace sample records back to the source system.
4. Check pipeline logs and recent changes.
**If I find...:** A real error: fix at the source or in the logic, record what changed, tell everyone who saw the old number. A definition difference: explain and, if needed, show both. No error: I refuse to change it, because an edited number cannot be defended. I also refuse any hidden manual override with no record.
**What I would tell the stakeholder:** "I understand it looks off. I checked it back to the source and it matches our definition; here is why it differs from your expectation. If you believe the source is wrong, let us raise it with its owner. I cannot adjust a figure without a documented reason."
**Prevent it next time:** Write the definition on the report; keep an approval-and-change log for any adjustment.
**Likely follow-ups:** 1) *What if the boss insists?* Offer an annotated alternative (a labelled adjusted view) and escalate if asked to misstate. 2) *What about legitimate corrections?* Fine, with a log.
**Common mistakes / traps:** Quietly editing; refusing without checking; sounding accusatory.

### Q66 ⭐ 🟡 A weekly sales target was announced and a spike appeared in the last two days of every quarter. How do you investigate metric gaming?
**Asked at:** commonly asked (no company-specific report found); metric gaming is a gap-fill item (judgement).
**What the interviewer is checking:** That you look for patterns, test them with data, and stay fair rather than accusing.
**Say this in the interview:** "A spike at every quarter end can be normal buying, or people pulling sales forward. I would check whether the following weeks dip and whether those orders are later cancelled or returned."
**First, clarify / contain:** Ask how targets and incentives work and when the target was announced. Do not accuse anyone; keep the findings at pattern level first.
**What I would check, in order:**
1. Compare with pre-target quarters: did the spike exist before the target?
2. Check the first weeks of the next quarter: a dip suggests pull-forward.
3. Cancellations, returns and credit notes on the spike orders, later.
4. Order profile: unusual discounts, large one-off deals, same customers, round amounts, back-dated dates.
5. Distribution by salesperson or team: concentrated in a few?
6. Genuine causes: customer budget cycles, seasonality, a promotion.
**If I find...:** Pull-forward with no net gain: raise a design issue, since the target rewards timing. Cancellations or back-dating: pass to the control or audit team; I report evidence, not verdicts. Genuine seasonality: no action beyond documenting it.
**What I would tell the stakeholder:** "Quarter-end shows a spike followed by a dip, so some sales appear to move earlier. I have not found misconduct; I recommend reviewing the target design and checking the returns data."
**Prevent it next time:** Measure on rolling averages, add quality metrics (returns, margin), and rotate targets.
**Likely follow-ups:** 1) *Is it fraud?* Not from this data alone; refer to the right team. 2) *How to fix incentives?* Reward sustained and net sales.
**Common mistakes / traps:** Accusing individuals; ignoring genuine seasonality; checking only the spike, not the aftermath.

### Q67 ⭐ 🟡 How do you verify that a fix actually restored a metric, and when do you declare an incident closed?
**Asked at:** commonly asked (no company-specific report found); gap-fill item (judgement).
**What the interviewer is checking:** That you confirm recovery with evidence rather than assume the fix worked.
**Say this in the interview:** "I check the fixed data against the expected range and the source, backfill the affected days, then watch for a full cycle before closing."
**First, clarify / contain:** Agree what "restored" means: back within normal range, matching source totals, and all affected periods corrected.
**What I would check, in order:**
1. Row counts and totals now match the source system for the broken days.
2. The metric is back in its normal range for the same weekday and season.
3. Segments recover too (not only the total).
4. Backfilled history is corrected and downstream reports refreshed.
5. Root cause is addressed, not only the symptom.
6. A monitoring check is added for the same failure.
**If I find...:** Total fixed but one segment off: keep open. Recovered only after the fix date with history still wrong: backfill first. Recovery within noise but unclear: wait another cycle.
**What I would tell the stakeholder:** "The fix is in and numbers match the source from 3 November. I will watch for one full week and confirm closure on Friday."
**Prevent it next time:** Add automated checks and a closure checklist.
**Likely follow-ups:** 1) *How long to watch?* At least one full business cycle (often a week; a month-end if it is a monthly metric). 2) *Who signs off?* The metric owner.
**Common mistakes / traps:** Closing when the number "looks right"; forgetting to backfill; no monitor afterwards.

### Q68 ⭐ 🟡 Write the structure of a short post-mortem for a metric incident: what goes in each section and what stays out?
**Asked at:** commonly asked (no company-specific report found); gap-fill item (judgement).
**What the interviewer is checking:** Whether you learn from incidents in a blameless, useful way.
**Say this in the interview:** "A post-mortem is a short, blameless write-up: what happened, impact, cause, how we fixed it, and what we change. It names processes, not people."
**Clarify first:** Who reads it (the metric owners and leadership) and what decision it supports (prevent a repeat).
**Plan:** Sections:
1. Summary: two lines on what broke and the impact.
2. Impact: which metrics, dates, decisions and who saw wrong numbers.
3. Timeline: detection, response, fix, closure, with times.
4. Root cause: the actual cause plus contributing factors (for example no check on a source change).
5. How we fixed and verified it.
6. What went well and what did not.
7. Action items: each with an owner and date.
**Method choice and why:** Ask "why" repeatedly until you reach a process gap (the "five whys").
**Pitfalls:** Staying out: blame and names, long log dumps, speculation stated as fact, and vague actions like "be more careful".
**Deliverable:** A one-page document, shared with all affected users within a few days.
**Likely follow-ups:** 1) *Why blameless?* People hide errors if they fear blame. 2) *How many actions?* Few, owned and dated.
**Common mistakes / traps:** Blame; no owners on actions; never following up.

### Q69 ⭐ 🟡 When an investigation cannot find a definite cause, how do you present the findings without overclaiming?
**Asked at:** commonly asked (no company-specific report found); gap-fill item (judgement).
**What the interviewer is checking:** Honesty and calibration: you can say "not sure" and still be useful.
**Say this in the interview:** "I say what I ruled out, what is still possible, how confident I am, and what I will do to narrow it down."
**Clarify first:** What decision is waiting on this, and can it be made without certainty?
**Plan:**
1. List the causes tested and the evidence that ruled each out.
2. Rank what remains by likelihood, with plain labels (likely, possible, unlikely).
3. State the size of the movement that is explained and unexplained (for example "about 70% of the drop is traced to X; 30% unexplained").
4. Say what data would settle it and when.
5. Give a recommendation that works under uncertainty (a cheap safeguard or a monitor).
**Method choice and why:** Show ranges and confidence rather than one confident story; a clean "unknown" beats a wrong cause that drives a bad decision.
**Pitfalls:** Choosing the most convenient explanation; using words such as "caused" for correlations; hiding the unexplained part.
**Deliverable:** A one-page summary: facts, ruled out, leading hypotheses, confidence, next steps with date.
**Likely follow-ups:** 1) *What if leadership wants a single answer?* Give the best-supported one, labelled with its confidence. 2) *When do you stop?* When further effort costs more than the decision is worth.
**Common mistakes / traps:** Overclaiming; vague hedging with no next step.

### Q70 ⭐ 🟡 A data pipeline was fixed after you reported a drop. How do you communicate that the earlier numbers were wrong?
**Asked at:** commonly asked (no company-specific report found); gap-fill item (judgement).
**What the interviewer is checking:** Transparency and ownership when you reported a wrong number, even if the cause was upstream.
**Say this in the interview:** "I tell everyone who saw the earlier number, right away, in plain words: what was wrong, the corrected figure, and what it changes."
**First, clarify / contain:** Confirm the corrected numbers first; list who received the wrong report and which decisions used it.
**What I would check, in order:**
1. Exact period and metrics affected.
2. Old vs corrected values side by side.
3. Decisions or messages already made on the old figure.
4. Whether all copies (dashboards, decks, emails) can be updated.
**If I find...:** A small change: a short note. A big change or decision already made: a direct call to the decision-maker, then a written follow-up.
**What I would tell the stakeholder:** "Correction: the drop I reported on 3 November was caused by a pipeline fault, not customers. The corrected figure is attached and is within normal range. The earlier number should not be used. Nothing else is affected; I will confirm by tomorrow."
**Prevent it next time:** Add data checks before publishing; mark preliminary numbers as provisional; keep a visible change log.
**Likely follow-ups:** 1) *Do you apologise?* Briefly, factually, then focus on the fix. 2) *Whose fault?* Describe the cause, not a person.
**Common mistakes / traps:** Quietly replacing the number; long excuses; forgetting people who got the old file.

### Q71 ⭐ 🟡 Monsoon rains and a cricket match night both affect order volumes in the same week. How do you control for external events when explaining a movement?
**Asked at:** commonly asked (no company-specific report found); the "external events" step is in the common frame of the question banks found (unverified).
**What the interviewer is checking:** That you can separate outside events from internal causes without over-claiming precision.
**Say this in the interview:** "I build an events calendar, compare against similar weeks and unaffected areas, and say how much of the movement external events plausibly explain, with a range."
**Clarify first:** Which orders, which cities, and which direction? Rain and match nights may push in opposite ways (more food orders, fewer deliveries).
**Plan:**
1. Mark both events by date, time and city (rain by city, match night nationally).
2. Compare affected cities with unaffected ones on the same days (a comparison-group approach).
3. Compare with the same weekday in non-event weeks, and with last year's events if available.
4. Look at the hour of day: match nights concentrate in the evening.
5. Check supply: delivery delays or fewer drivers can cut orders when it rains.
6. Estimate each effect separately where cities differ; where both overlap, give a combined range.
**Method choice and why:** Simple comparisons first; a regression with event flags (rain, match, weekday) only if there is enough history.
**Pitfalls:** Assuming the events explain everything; double counting overlapping effects; very few event weeks, so the estimate is rough.
**Deliverable:** A chart: expected vs actual with events shaded, plus a short note of the explained and unexplained part.
**Likely follow-ups:** 1) *How to separate rain and match?* Use cities with only one of them. 2) *What if nothing is left?* Then report the residual as unexplained.
**Common mistakes / traps:** Blaming weather by default; ignoring supply-side effects.

### Q72 ⭐ 🟡 How do you handle a metric investigation when you only have access to aggregated weekly data and no raw tables?
**Asked at:** commonly asked (no company-specific report found); the weekly-series-only variant appears in the revenue-drop question banks found (unverified).
**What the interviewer is checking:** That you can still reason well with limited data, and say what you cannot conclude.
**Say this in the interview:** "I decompose whatever splits the weekly data has, state clearly what it cannot tell me, and request the specific extra cut that would settle the question."
**Clarify first:** Which columns does the weekly data have (region, product, channel)? Is there a definition note? Can I request more?
**Plan:**
1. Check the series itself: gaps, week definition, restated weeks.
2. Compare with the same weeks last year and the recent average.
3. Decompose the change using available splits (price x volume, region, product, channel).
4. Check mix: do segment rates move or only segment sizes (Simpson's paradox, a trend that reverses once data is combined)?
5. Cross-check against other sources (finance totals, external events).
6. List hypotheses I cannot test and the exact data needed (for example daily by region).
**Method choice and why:** Simple decomposition. With only weekly points, statistical tests are weak and daily patterns (launch date, a one-day outage) are invisible.
**Pitfalls:** Averages hiding mix changes; pretending to know the day it started; small number of data points.
**Deliverable:** A short note with the decomposition, confidence, and a specific data request with a date.
**Likely follow-ups:** 1) *Can you rule out a data fault?* Not fully; reconcile totals with finance. 2) *What would you ask for first?* Daily data for the broken segment.
**Common mistakes / traps:** Over-interpreting; not asking for the extra cut.

### Q73 ⭐ 🟡 How do you use leading and lagging indicators to explain a rise in attrition before the exit numbers show it?
**Asked at:** commonly asked (no company-specific report found); HR attrition investigation material (UW people analytics text, Umbrex, infeedo, SHRM India) is cited in the sources (snippet-level, unverified).
**What the interviewer is checking:** That you can warn early, using signals that move before resignations, and avoid overclaiming prediction.
**Say this in the interview:** "Exits are a lagging indicator: they confirm what already happened. I would watch leading signals such as engagement scores, absenteeism, leave patterns, overtime, manager changes, and lateral interviews, by team, and check which have preceded exits in the past."
**Clarify first:** The decision (target retention action where?), the attrition definition (voluntary or all, regretted or not), and the time window.
**Plan:**
1. Define attrition and fix the denominator (average headcount).
2. List candidate leading signals: engagement score drop, rising unplanned leave, overtime, no promotion in X years, low pay position, new manager, notice-period behaviour.
3. Back-test: for people who left last year, did those signals appear 2-6 months earlier? Compare with those who stayed.
4. Rank signals by how well they separate leavers from stayers.
5. Build a team-level watch list rather than individual labels.
**Method choice and why:** A simple comparison of leavers vs stayers first; a model only if there is enough data and governance.
**Pitfalls:** Correlation is not cause; small teams give noisy rates; using individual predictions harmfully (privacy and fairness: confirm with HR policy and the privacy or legal team).
**Deliverable:** A team-level early-warning view with the leading signals and a suggested action, not a list of "likely leavers".
**Likely follow-ups:** 1) *What lag?* Test it on your own history. 2) *Is exit interview data leading?* No, it is lagging.
**Common mistakes / traps:** Treating a signal as proof; naming individuals; not back-testing.

### Q74 ⭐ 🟡 How should a team define a metric dictionary entry so that a mid-year definition change does not silently break trend comparisons?
**Asked at:** commonly asked (no company-specific report found); metric dictionary is a gap-fill item (judgement).
**What the interviewer is checking:** That you treat metric definitions as versioned, governed assets.
**Say this in the interview:** "Each entry has an owner, a precise formula and a version history. A definition change gets a new version, a date, and a restated back-series, or a visible break in the chart."
**Clarify first:** Who owns the metric, who uses it and for which decisions?
**Plan (entry fields):**
1. Name and plain-language meaning (for example attrition rate: leavers in the period divided by average headcount).
2. Exact formula, including included and excluded groups, the date field and time zone.
3. Source table and refresh time.
4. Owner and approver.
5. Version, effective date and a change reason.
6. Change log: old and new definitions and the size of the impact on the last 12 months.
7. Known limits and related metrics.
**Method choice and why:** On a change, restate history on the new definition where possible. If not possible, show a chart break and an annotation, and never join old and new into one unlabelled line.
**Pitfalls:** Silent edits; same name for two definitions; unrestated history.
**Deliverable:** A single dictionary page linked from each dashboard, with version numbers on the reports.
**Likely follow-ups:** 1) *How do you show the change?* Overlap period with both definitions. 2) *Who approves?* The metric owner plus users.
**Common mistakes / traps:** Fixing the formula and forgetting the history.

### Q75 ⭐ 🔴 Explain Goodhart's law with an example of a metric that moved because people were optimising for it, and how you would detect it.
**Asked at:** commonly asked (no company-specific report found); Goodhart-style gaming is a differentiator item (judgement).
**What the interviewer is checking:** That you understand that targets change behaviour and that you pair metrics.
**Say this in the interview:** "When a measure becomes a target, it stops being a good measure, because people optimise the number rather than the goal. I would watch a paired quality metric to detect it."
**Clarify first:** What is the target, what is the real goal behind it, and what are the ways to hit the number without the goal?
**Plan:**
Explain simply: A recruiting team is judged on time-to-hire. Illustrative (exercise numbers): it falls from 45 to 30 days, which is 15 days or one third. At the same time, offer declines and 90-day exits rise. The team hurried or lowered the bar, so the number improved while hiring quality fell.
Detection:
1. Pair the target with a counter-metric (quality of hire, 90-day retention, offer acceptance).
2. Look for a sudden change at the time the target started.
3. Look for discontinuities near the threshold (many cases just under the limit).
4. Compare with teams or periods without the target.
5. Spot-check records.
**Method choice and why:** Counter-metrics are cheaper than policing; use several metrics, not one.
**Pitfalls:** Assuming bad intent; adding too many targets; ignoring that some improvement is real.
**Deliverable:** A balanced scorecard: target plus guardrail metrics and a review rule.
**Likely follow-ups:** 1) *Other examples?* Support tickets closed fast then reopened. 2) *How to design a good target?* Outcome-based, with guardrails.
**Common mistakes / traps:** Blaming people; one-metric dashboards.

### Q76 ⭐ 🔴 A data migration changed a metric by 3% overnight. How do you run a reconciliation so you can attribute the movement to the migration?
**Asked at:** commonly asked (no company-specific report found); migration reconciliation is a differentiator item (judgement).
**What the interviewer is checking:** That you can isolate a system change from a real business change.
**Say this in the interview:** "I run the old and new systems side by side on the same period, then explain the gap step by step until the unexplained remainder is near zero."
**First, clarify / contain:** Note the cut-over time and the metric. Tell users the number is under review; do not overwrite either figure. A 3% move on a base of 10,00,000 is 30,000 (exercise number).
**What I would check, in order:**
1. Was the movement exactly at cut-over, and did a similar business event also happen?
2. Reconcile record counts old vs new for the same period.
3. Reconcile totals, then by segment, then record by record for the differences.
4. Look for definition changes: time zone, rounding, null handling, status mapping, duplicates, deleted records.
5. Rerun the old logic on new data (and the new logic on old data) to separate logic changes from data changes.
6. Compare the overlap period if both systems ran in parallel.
**If I find...:** All explained by migration rules: restate history or annotate a break. Partly explained: report the explained and the unexplained shares. Not explained: a real change may be mixed in, so keep investigating.
**What I would tell the stakeholder:** "About 2.8 of the 3 points trace to a time-zone and duplicate-handling change in the new system; 0.2 is still being checked. The business has not changed. I will confirm by Thursday."
**Prevent it next time:** Run a parallel period and sign-off checklist before any cut-over.
**Likely follow-ups:** 1) *What if you cannot run both?* Use the historical data in the new system. 2) *Which number is right?* The one matching the agreed definition.
**Common mistakes / traps:** Assuming the migration explains everything; no explained-vs-unexplained split.

### Q77 ⭐ 🔴 When is difference-in-differences or a synthetic control a sensible way to explain a metric change, and what are the failure modes?
**Asked at:** commonly asked (no company-specific report found); a differentiator item in the sources (judgement).
**What the interviewer is checking:** That you know when a before-after comparison is not enough and how comparison groups can mislead.
**Say this in the interview:** "When something changed for one group and not another and I cannot run an experiment, I compare the change in the affected group with the change in a similar unaffected group. It works only if both would have moved together anyway."
**Clarify first:** What changed, where and when, and is there a comparable group that did not get it?
**Plan:**
1. Difference-in-differences: change in the treated group minus the change in the comparison group (for example Q62: 12 - 6 = 6 points).
2. Check the trends before the change look parallel.
3. Synthetic control: when no single region is a good match, build a weighted mix of several untouched regions that follows the treated region closely before the change; after the change, the gap is the estimated effect.
4. Test robustness: use different comparison groups and a fake change date (placebo).
**Method choice and why:** Use these for one-off changes (price rise, policy, launch) where a randomised test was impossible. Simple before-after is used only if no comparison exists, and with strong caveats.
**Pitfalls:** Failure modes: trends not parallel; the comparison group was also affected (spillover); another event hit only the treated group; few comparison units; the pre-period is too short.
**Deliverable:** A chart of treated vs comparison/synthetic lines with the change date, the estimate with a range, and the assumptions listed.
**Likely follow-ups:** 1) *How do you check parallel trends?* Plot several pre-change periods. 2) *Is it causal?* Only under the assumptions.
**Common mistakes / traps:** Claiming proof; picking the comparison group that gives the wanted answer.

### Q78 ⭐ 🔴 A stakeholder believes a metric fell because of a campaign they disliked. How do you test that explanation fairly without confirming their bias?
**Asked at:** commonly asked (no company-specific report found); causal separation is a second-line topic in the sources (judgement).
**What the interviewer is checking:** That you test a hypothesis, including the rival ones, instead of seeking a confirming story.
**Say this in the interview:** "I write down, before looking, what we would see if the campaign caused the fall and what we would see if it did not. Then I test it and the alternatives equally hard."
**Clarify first:** What exactly fell, when, and which campaign and audience? Agree the evidence standard with the stakeholder before the analysis.
**Plan:**
1. State the hypothesis and what it predicts: the drop appears only in the exposed audience, starts after the campaign, and is larger with heavier exposure.
2. Check timing: did the drop start before the campaign?
3. Compare exposed and unexposed groups (or regions), as in a difference-in-differences.
4. Check rivals: seasonality, pricing, stock, data or tracking changes, competitors, mix shifts.
5. Look for evidence that would disprove it, and report it.
6. Write down the result, including "consistent with" vs "proven".
**Method choice and why:** Pre-agreed prediction and comparison groups; a hold-out for future campaigns, which is the cleanest test.
**Pitfalls:** Confirmation bias (mine too), cherry-picking segments, treating correlation in time as cause.
**Deliverable:** A short note: hypotheses tested, evidence for and against, conclusion with confidence, and a hold-out recommendation.
**Likely follow-ups:** 1) *What if the evidence supports the stakeholder?* Say so plainly. 2) *What if it is mixed?* Say so and design a test.
**Common mistakes / traps:** Hunting for supporting data only; dismissing the stakeholder's idea without testing it.

### Q79 ⭐ 🔴 A decline appears only in a survivorship-biased view of cohorts (only users still active). How do you spot and correct the bias?
**Asked at:** commonly asked (no company-specific report found); survivorship in cohorts is a gap-fill item (judgement).
**What the interviewer is checking:** That you always keep the original cohort size as the denominator.
**Say this in the interview:** "A view of only the users who stayed hides everyone who left. I recompute the metric per original sign-up, including the ones who left, and the story often changes."
**What the data shows (illustrative):** The premise is unusual: survivorship bias more often flatters a metric, but it can also create a false decline when a cohort keeps more marginal users, who dilute the survivors' average. Exercise numbers: Cohort A has 1,000 sign-ups, 400 still active, average 10 sessions each. Cohort B has 1,000 sign-ups, 600 still active, average 8 each.
**Working:**
1. Survivor view: A is 10, B is 8, a 20% fall (8 / 10 - 1).
2. Total sessions: A 400 x 10 = 4,000; B 600 x 8 = 4,800.
3. Per original sign-up: A 4,000 / 1,000 = 4.0; B 4,800 / 1,000 = 4.8, a 20% rise (4.8 / 4.0 - 1).
**Result:** The decline in the survivor view reverses to a 20% gain once all sign-ups are counted. Retention rose from 40% to 60%, so more weaker-engaged users stayed.
**Caveats / what else I would check:** Spot the bias: the denominator shrinks over time, the base differs between cohorts, and retention differs between the compared groups. Correct by using the cohort's original size, reporting retention and engagement together, and comparing like with like at the same age (week 4 vs week 4).
**Next step / recommendation:** Show retention curve and per-sign-up engagement side by side, and decide with both.
**Likely follow-ups:** 1) *Is the survivor metric useless?* No, it answers "how engaged are active users", if labelled. 2) *Other examples?* Only counting current employees in a satisfaction study.
**Common mistakes / traps:** Dividing by active users only; comparing cohorts of different ages.

### Q80 ⭐ 🔴 Your anomaly detector flags a spike on every festival. How would you redesign it to learn from known events?
**Asked at:** commonly asked (no company-specific report found); anomaly-detection design is a differentiator item (judgement).
**What the interviewer is checking:** That you can improve a detector with context and feedback, not by just widening thresholds.
**Say this in the interview:** "Festivals are expected, not anomalous. I would give the detector an event calendar, compare each festival with past festivals, and use analyst feedback to retire false alarms."
**Clarify first:** Which metric, how often it runs, what a false alarm costs, and whether festival dates (some move yearly) are known ahead.
**Plan:**
1. Build an events calendar (festival, sales, holiday) with start and end dates and affected regions; update it yearly because lunar-calendar dates shift.
2. Add event flags and "days to festival" as inputs, so expected lift is part of the baseline.
3. Baseline against the same event last year or similar events, scaled for growth.
4. Alert on deviation from the event-adjusted forecast, so a festival that is much weaker or much stronger than usual still fires.
5. Feedback loop: label each alert (true or false) and review monthly; use labels to tune.
6. Keep the generic rule for the days outside events.
**Method choice and why:** Rules and event-adjusted baselines first (explainable); a forecasting model with holiday terms if history is long enough.
**Pitfalls:** Suppressing alerts during events (a real outage would be missed); few past festivals, so small samples; shifting dates.
**Deliverable:** A detector with an event calendar, a monthly false-alarm report and an owner for the calendar.
**Likely follow-ups:** 1) *How to evaluate?* Replay history and count false and missed alarms. 2) *New festival?* Use the nearest similar event with a wider band at first.
**Common mistakes / traps:** Muting the detector on festival days; hard-coding last year's dates.

