# Book 7 — Guesstimates, Case Studies & Business Metrics | Part 5: Root-Cause Cases (Sales Dropped, Orders Fell) 🟡🔴

**Target:** 90 questions | **Actual:** 91 questions
**Scope:** diagnosing falling sales, orders and revenue with hypothesis trees, data cuts, decision rules and numeric decompositions (price/volume/mix, funnel, region, cohort).

### Q1 ⭐⭐⭐ 🟢 Sales dropped 20% compared with last month. What clarifying questions do you ask before starting any analysis?
**Asked at:** commonly asked; question banks (Dataford, PracHub) list "sales dropped 20%" prompts, with company tags unverified.
**What the interviewer is checking:** Whether you pin down the problem before jumping to causes.
**Say this in the interview:** "Before any analysis I want to confirm the drop is real, define exactly what 'sales' means, and know the time, place and product where it shows up. Five quick questions, then I build a tree."
**Clarify first (the questions themselves):**
1. **Definition:** is "sales" gross or net of returns and discounts, in rupees or units, booked or delivered?
2. **Time:** is 20% month vs last month, or vs the same month last year? Did it fall suddenly on one day (a step) or slide slowly? Do both months have the same number of days and weekdays?
3. **Scope:** all products, cities, channels and customer types, or one pocket? Is it our company only or the whole market?
4. **Data trust:** was the number checked against finance or payment records? Any recent dashboard, tracking or pipeline change?
5. **Context:** what changed recently (price, promo, app release, stock, team, competitor, festival)? What is the target, and how urgent is this?
**What I would check, in order:** data validity, then the calendar, then segment cuts, then internal vs external causes. I only start cutting once the definition is agreed.
**If the answers show...:** a definition change or a calendar quirk means no real drop; a drop in one segment means chase that segment; a drop everywhere points to something global (price, tracking, market).
**Recommendation:** write the agreed problem statement in one line ("net sales in rupees, all channels, fell 20% month-on-month, from the 12th onward") and confirm it with the interviewer.
**Likely follow-ups:** 1) *What if the interviewer says "assume nothing is known"?* Say you will assume the data is correct but state the assumption aloud. 2) *Which question matters most?* Definition and baseline, since they can erase the problem.
**Common mistakes / traps:** Diving into causes immediately; asking ten unfocused questions; not confirming the baseline period.

### Q2 ⭐⭐⭐ 🟢 Orders on Tuesdays fell 20% compared with earlier weeks. How do you find out why?
**Data available:** order-level table (order time, city, platform, restaurant or seller id, customer id, promo code, order status, delivery time), app release log, marketing calendar, customer-support tickets.
**Asked at:** commonly asked; PracHub lists a Swiggy "20% week-over-week orders fall" prompt (unverified); the Tuesday wording is this book's own example.
**What the interviewer is checking:** A structured, data-driven path from a symptom to a cause, using the tables given.
**Say this in the interview:** "First I confirm the Tuesday drop is real, then I cut it by city, platform, restaurant and customer type to find where it sits, and I match that against the release log and promo calendar."
**Clarify first:** Is it every Tuesday since a certain date or one Tuesday? Other weekdays normal? Orders placed or delivered? Which cities?
**Structure:**
- Data check: late events, a logging change, a timezone shift.
- Demand: fewer customers ordering (new, repeat, a specific city or platform).
- Supply: fewer restaurants open on Tuesday, more items out of stock.
- Operations: slow delivery, few riders, more cancellations.
- Marketing: a promo that used to run on Tuesdays and stopped.
**What I would check, in order:**
1. Count orders per weekday for 8 weeks; mark the week the change began (SQL: GROUP BY week, weekday).
2. Compare Tuesday by platform and city; one segment carrying the whole drop is the lead.
3. Active restaurants and orders per restaurant on Tuesday.
4. Order status mix (cancelled, failed) and delivery time.
5. Promo-code orders by weekday.
6. Overlay the app release log, marketing calendar and support tickets.
**If the data shows...:** only Android fell, and the dip began after a release, so suspect a release bug; fewer active restaurants means a supply or weekly-off change; promo orders vanished means the promo schedule changed; every segment fell evenly means look at data or demand.
**Recommendation:** name the one or two causes that together explain at least 80% of the lost orders, propose the fix, and track Tuesday orders for two weeks.
**Likely follow-ups:** 1) *Where do you start if you can only run one query?* Tuesday orders by platform and city. 2) *How do you size it?* Lost orders per segment divided by total lost.
**Common mistakes / traps:** Comparing Tuesday to Monday instead of to earlier Tuesdays; listing hypotheses without saying which data tests each one.

### Q3 ⭐⭐⭐ 🟢 How do you check that a reported drop in sales is real and not a data or dashboard problem?
**Asked at:** commonly asked; the validate-first step appears in question-bank answer outlines (PracHub, Dataford) and is unverified for any single company.
**What the interviewer is checking:** Whether you doubt the number before explaining it.
**Say this in the interview:** "I reconcile the dashboard to a second source, check for late or duplicated data, and confirm the definition and filters did not change. Only then do I treat it as a real drop."
**Explain simply:**
- **Reconcile with another source:** compare the dashboard with finance ledger, payment gateway settlements or the raw order table. A 20% gap between sources means a pipeline problem, not a business problem.
- **Freshness:** the latest days are often incomplete because events arrive late; compare with the same day's earlier snapshot.
- **Definition and filter changes:** a new status filter, a currency or tax change, a changed metric logic, a dropped city or product from the report.
- **Duplicates and nulls:** the row count and the count of distinct order ids, missing join keys after a table change.
- **Tracking changes:** a new app version that stopped sending events makes sessions fall while payments do not.
- **Calendar:** days in the period, weekdays, holidays.
**Mini example:** the dashboard shows 8,000 orders; the payment report shows 9,800 paid orders. The 18% gap shows the dashboard misses events, so the "20% drop" is likely mostly a data issue.
**Practice step:** list three independent counts of orders in your own work (dashboard, database, finance) and note which differs.
**Likely follow-ups:** 1) *What if sources disagree by 2%?* That is normal timing noise; the drop is still real. 2) *Who do you ask?* The data engineering owner and finance.
**Common mistakes / traps:** Starting root-cause work on a dashboard number never cross-checked; trusting the latest two days of data.

### Q4 ⭐⭐⭐ 🟢 How do you split a revenue drop into volume, price and mix effects?
**Given:** Revenue = number of orders x average order value (AOV).
**Asked at:** commonly asked; revenue = price x volume trees appear in consulting prep (for example Hacking the Case Interview) and Sequoia's mix-shift article (both snippet-level, unverified).
**What the interviewer is checking:** Whether you can turn one number into additive pieces that sum back to the total change.
**Say this in the interview:** "I split the change in revenue into the part from fewer orders, valued at the old AOV, and the part from a different AOV, valued at the new order count. They add up exactly. If AOV moved, I then split that into price and mix."
**Explain simply:**
- **Volume effect** = (new orders - old orders) x old AOV. How much we lost purely from fewer orders.
- **AOV effect** = (new AOV - old AOV) x new orders. How much we lost from smaller baskets.
- Volume effect + AOV effect = total revenue change exactly, with no leftover term, because the AOV effect uses the new order count.
- **Price vs mix inside AOV:** price effect is a change in price for the same item; mix effect is customers moving to cheaper items or smaller baskets (compare the price of the same item across weeks, then the item share).
**Worked mini-example (numbers from Q12):** orders 20,000 to 18,000 at old AOV ₹250: volume = -2,000 x 250 = -₹5,00,000. New AOV = 40,00,000 / 18,000 = ₹222.22; AOV effect = (222.22 - 250) x 18,000 = -₹5,00,000. Total -₹10,00,000, matching 50,00,000 to 40,00,000.
**Practice step:** take any two weeks of revenue and orders and compute both effects in Excel; check they sum to the change.
**Likely follow-ups:** 1) *Why not use the old AOV in both?* You then get a leftover interaction term that needs explaining. 2) *Does the order matter?* Yes; reversing gives different but still additive splits, so state your convention.
**Common mistakes / traps:** Leaving a residual; calling a fall in AOV a "price effect" when it is a mix shift; mixing gross and net revenue.

### Q5 ⭐⭐⭐ 🟢 What is a hypothesis tree (issue tree) for a sales drop, and how do you build one in the first two minutes of the interview?
**Asked at:** commonly asked; structured issue trees are the standard expected answer in the question banks seen (unverified for any one company).
**What the interviewer is checking:** MECE thinking (branches do not overlap and together cover everything) under time pressure.
**Say this in the interview:** "A hypothesis tree breaks 'why did sales drop' into branches that do not overlap and cover every possible cause, each with a data test. I start with the sales equation, then split internal from external."
**Explain simply:**
- **Level 0:** Sales fell 20%.
- **Level 1 (from the equation Sales = customers x orders per customer x basket value):** fewer customers, fewer orders per customer, smaller basket.
- **Level 2 (why):** each of the three splits into internal (price, promo, stock, app, delivery, team) and external (competitor, season, weather, regulation, economy).
- **Level 3:** one data test per leaf.
**Building it in two minutes:** (1) say the equation aloud, 20 seconds; (2) draw three branches, 20 seconds; (3) split each into internal and external, 40 seconds; (4) mark which two leaves you test first and why, 40 seconds.
**Mini example (HR):** "Attendance fell" splits into more leave, more absenteeism, more attrition; each splits into policy changes and external causes such as a strike.
**Practice step:** write a tree for "headcount fell 10%" in two minutes by timer.
**Likely follow-ups:** 1) *How many branches?* 3 to 5 at the top. 2) *How do you stay MECE?* Start from an identity (revenue = orders x AOV).
**Common mistakes / traps:** Giving a flat list of ten random causes; overlapping branches; no test attached to each leaf.

### Q6 ⭐⭐⭐ 🟢 How do you separate internal causes from external causes when a metric falls?
**Asked at:** commonly asked; "internal vs external" is a standard first split in the question banks seen (PracHub), unverified for any single company.
**What the interviewer is checking:** Whether you test what we control before blaming the market.
**Say this in the interview:** "Internal causes leave a fingerprint in our own logs: a release, a price, a stock-out. External causes hit competitors and the whole market at the same time. I test internal first because we can fix those."
**Explain simply:**
- **Internal (we control):** price, promos, product and app releases, stock, delivery speed, marketing spend, team changes.
- **External (we do not):** competitor moves, season or festival, weather, regulation, economy, payment-network outages.
- **How to separate:**
  1. Timing: internal causes start on a known date in our change log; external ones are gradual or tied to dates (festival, rain).
  2. Segment: an internal bug hits one platform or product; an external shock hits all comparable segments.
  3. Benchmark: do peers, category data, search trends or a control region show the same drop?
  4. Dose-response: does the effect grow with exposure (more rain, more competitor stores nearby)?
**Likely follow-ups:** 1) *What if both are present?* Size each and split the drop. 2) *What if you have no external data?* Use a region or segment not exposed as a control.
**Common mistakes / traps:** Blaming the market first; counting a coincidence as external proof; ignoring that both can apply.

### Q7 ⭐⭐⭐ 🟢 Which comparison baselines do you use when a metric drops (day-over-day, same weekday last week, year-over-year), and when does each one mislead?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you pick a baseline that removes seasonality and weekday patterns.
**Say this in the interview:** "My default is the same weekday over recent weeks, then year-over-year for season. Day-over-day misleads because weekdays differ."
**Explain simply:**
- **Day-over-day:** fine for very smooth series; misleads because Monday is not Sunday (a weekend dip looks like a crash).
- **Same weekday last week (WoW):** best for spotting recent shocks; misleads if last week itself was odd (a holiday, a promo) so compare with the average of the last 4 to 8 same weekdays.
- **Month-over-month:** misleads when months have different days or weekdays (4 vs 5 Tuesdays) or festival timing; use per-day averages.
- **Year-over-year:** removes seasonality; misleads when festival dates move (Diwali in October vs November), or the business grew or changed a lot.
- **Rolling average or forecast band:** best for deciding if a drop exceeds normal noise.
**Mini example:** 800 orders on a Tuesday against 1,000 average Tuesdays is -20%; against Monday's 1,300 it is -38%, which exaggerates.
**Practice step:** for one metric, put WoW, 8-week average and YoY side by side and see which tells a different story.
**Likely follow-ups:** 1) *Which one do you pick for a festival period?* Same festival window last year, aligned on festival date. 2) *What if the business is new?* Use trend-adjusted baselines.
**Common mistakes / traps:** Using one baseline only; ignoring that last year's base had its own anomaly.

### Q8 ⭐⭐⭐ 🟢 Which segment cuts do you try first when a total metric falls, and in what order?
**Asked at:** commonly asked; PracHub-style root-cause answers start with funnel and segment breakdowns (unverified for any one company).
**What the interviewer is checking:** Whether you localise the drop efficiently instead of cutting randomly.
**Say this in the interview:** "I go from cheap, high-information cuts to specific ones: time, then platform, geography, customer type, product, and finally channel and promo. I stop when one cut explains most of the drop."
**Explain simply (order and why):**
1. **Time:** one-day dip, step or gradual? Tells you where to look in the change log.
2. **Funnel stage:** sessions, product views, cart, order, payment, delivery; finds the broken step.
3. **Platform and app version:** Android, iOS, web; catches release bugs.
4. **Geography:** city or region; catches local events or supply problems.
5. **Customer type:** new vs repeat, high vs low value; separates acquisition from retention.
6. **Product or category:** catches stock-outs and price effects.
7. **Channel and promo:** paid, organic, promo code; catches marketing changes.
**Rule of thumb:** run each cut as a "contribution to the drop" table (segment drop divided by total drop). A segment with 15% of volume but 60% of the drop is the lead.
**Likely follow-ups:** 1) *When do you stop?* When 80% of the drop is explained. 2) *What if no cut shows a pattern?* The drop is spread out: suspect a global cause (data, price, season).
**Common mistakes / traps:** Cutting by many dimensions at once; reading percent change without the volume share; ignoring Simpson's paradox.

### Q9 ⭐⭐⭐ 🟢 A food-delivery app's revenue last month was ₹5,00,000 (2,000 orders at ₹250 AOV) and this month it is ₹4,00,000 (1,600 orders at ₹250 AOV). By what percent did revenue fall and which driver explains it?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Basic percentage change and spotting the driver.
**Say this in the interview:** "Revenue fell 20%, and it is all volume: AOV is unchanged at ₹250, so the whole drop is fewer orders."
**Definition in plain words:** Percent change = (new - old) / old x 100. Revenue = orders x AOV.
**Worked answer:**
1. Fall in revenue = 5,00,000 - 4,00,000 = ₹1,00,000.
2. Percent = 1,00,000 / 5,00,000 = 20% fall.
3. Orders: (1,600 - 2,000) / 2,000 = -20%.
4. AOV: 250 to 250, so 0%.
5. Volume effect = -400 x 250 = -₹1,00,000; AOV effect = 0 x 1,600 = 0.
**Result:** Revenue down 20% (₹1,00,000), 100% explained by order volume; AOV effect is zero.
**Check:** 1,600 x 250 = 4,00,000. Also 0.8 x 1.0 = 0.8, a 20% fall.
**Caveats:** This only says volume fell, not why; next split orders into customers x orders per customer, and by funnel and segment.
**Likely follow-ups:** 1) *What do you do next?* Split the order fall by segment and funnel. 2) *If AOV also fell?* Use the volume/AOV split (Q4).
**Common mistakes / traps:** Dividing by this month's revenue (25%); looking for a price cause when AOV is flat.

### Q10 ⭐⭐⭐ 🟢 How do you decide which hypothesis to test first when you have ten possible causes and little time?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Prioritisation: you do not test everything.
**Say this in the interview:** "I rank hypotheses by how likely they are, how big the impact could be and how cheap they are to test, then start with the cheap, likely ones, and I always check data validity first."
**Explain simply:**
- Score each hypothesis on three things: **likelihood** (does the timing and the segment fit?), **impact** (could it explain a large share of the drop?) and **effort** (one query or a two-week study?).
- Test first the ones that are cheap and plausible; order roughly: data issue, a known recent change (release, price, promo), supply, then external.
- Use "kill tests": a quick check that can rule a hypothesis out (if the drop appears on all platforms, an Android-only bug is dead).
**Mini example:** ten ideas; the drop began on 12 March; the release log shows a release on 12 March; Android is the only segment that fell. Test "release bug" first, 5 minutes, high impact.
**Practice step:** write your ten hypotheses in a table with scores 1 to 3 on likelihood, impact, ease and sort by the product.
**Likely follow-ups:** 1) *What if two are tied?* Pick the cheaper one. 2) *What if the first test is negative?* Say so aloud and move down the list.
**Common mistakes / traps:** Starting with the most interesting rather than the most likely; skipping the data-validity check.

### Q11 ⭐⭐⭐ 🟢 How do you present a root-cause finding to a non-technical business stakeholder in two minutes?
**Asked at:** commonly asked; a recruiter guide (Taggd) says candidates must frame a business question and defend a recommendation (snippet, unverified).
**What the interviewer is checking:** Communication: answer first, evidence short, action clear.
**Say this in the interview:** "Answer first: what fell, why, how big and what we do. Then two supporting facts, one chart, and the next step with an owner and a date."
**Explain simply (a 2-minute script):**
1. **Headline (15 s):** "Orders fell 20% because the Android checkout broke after release 7.3."
2. **Size (15 s):** "That explains about 17 of the 20 points; the rest is normal Tuesday variation."
3. **Evidence (45 s):** one chart: Android vs iOS orders by day with the release date marked, plus the error rate rising at the payment step.
4. **What it is not (15 s):** "We ruled out pricing, stock and the market because they did not fit the timing."
5. **Action (30 s):** "Roll back or hotfix by Thursday; I will track Android orders daily and confirm recovery in a week."
**Practice step:** record yourself giving one past finding in 120 seconds, without technical terms.
**Likely follow-ups:** 1) *What if you are only 70% sure?* Say it, and state the check that would confirm it. 2) *How do you handle pushback?* Show the data cut they disagree with.
**Common mistakes / traps:** Starting with methodology; presenting ten charts; hiding uncertainty; no clear owner or deadline.

### Q12 ⭐⭐⭐ 🟡 Revenue fell from ₹50,00,000 to ₹40,00,000 while orders fell from 20,000 to 18,000. How much of the ₹10,00,000 drop is due to fewer orders and how much to a lower AOV?
**Method to use:** volume effect = (new orders - old orders) x old AOV; AOV effect = (new AOV - old AOV) x new orders.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Price-volume split arithmetic.
**Say this in the interview:** "Old AOV is ₹250, new is about ₹222. Fewer orders cost ₹5,00,000 and the lower AOV cost another ₹5,00,000, so the drop is half and half."
**Definition in plain words:** Volume effect = what we lose from fewer orders at the old basket value; AOV effect = what we lose from a smaller basket on the orders we still get. AOV = revenue / orders.
**Worked answer:**
1. Old AOV = 50,00,000 / 20,000 = ₹250.
2. New AOV = 40,00,000 / 18,000 = ₹222.22 (rounded).
3. Volume effect = (18,000 - 20,000) x 250 = -₹5,00,000.
4. AOV effect = (222.22 - 250) x 18,000 = -₹5,00,000 (rounded; exactly -₹5,00,000).
5. Sum = -₹10,00,000.
**Result:** ₹5,00,000 (50%) from fewer orders (-10% orders), ₹5,00,000 (50%) from a lower AOV (-11.1%).
**Check:** 18,000 x 222.22 = 40,00,000; and 50,00,000 - 5,00,000 - 5,00,000 = 40,00,000.
**Caveats:** Order of the method matters; the interaction term sits in the AOV effect. Next, split AOV into price, discount and mix.
**Likely follow-ups:** 1) *Where do you look next for AOV?* Discount depth, item mix, smaller baskets. 2) *And for orders?* Funnel and segment cuts.
**Common mistakes / traps:** Using old AOV in both lines and being unable to explain the leftover; calling the whole drop "volume" because orders fell.

### Q13 ⭐⭐⭐ 🟡 A shopping app's weekly funnel is below. Orders fell from 8,000 to 6,000. Which stage caused the fall and by what percent did it change?
| Stage | Last week | This week |
|---|---|---|
| Sessions | 2,00,000 | 2,00,000 |
| Sessions that reach a product page | 50% | 50% |
| Product-page views that add to cart | 20% | 20% |
| Carts that become orders | 40% | 30% |
**Asked at:** commonly asked; funnel breakdown is a standard step in the question-bank answers (PracHub, unverified for one company).
**What the interviewer is checking:** Locate the stage by comparing stage conversion rates.
**Say this in the interview:** "Only the last step changed: carts to orders went from 40% to 30%, a 25% relative fall, which is the entire drop. Traffic, browsing and add-to-cart are unchanged."
**Definition in plain words:** Funnel conversion at each stage = users who move on / users who reached that stage. Orders = sessions x each stage rate multiplied together.
**Worked answer:**
1. Last week: 2,00,000 x 0.5 = 1,00,000 product views; x 0.2 = 20,000 carts; x 0.4 = 8,000 orders.
2. This week: same 20,000 carts; x 0.3 = 6,000 orders.
3. Stage change: 40% to 30% = -10 percentage points, which is -25% relative (10/40).
4. Orders: 8,000 to 6,000 = -25%, equal to the stage drop because other stages are flat.
**Result:** The cart-to-order (checkout) stage caused all of it; down 25% in relative terms (10 points).
**Check:** 20,000 x 0.3 = 6,000 matches the given orders.
**Caveats:** Next ask why checkout fails: payment errors, delivery fee or address problems, price shown at checkout, app bug or a coupon change. Cut by payment method, platform and app version.
**Likely follow-ups:** 1) *Does 25% equal 10 points?* No; one is relative, one absolute. 2) *First check?* Checkout error rate and payment success by method.
**Common mistakes / traps:** Saying "10%" fall without saying points vs relative; looking at sessions when they did not change.

### Q14 ⭐⭐⭐ 🟡 Orders fell from 1,00,000 to 86,000 across four regions (table below). Which regions explain most of the drop, and which region fell fastest in percentage terms?
| Region | Last week | This week |
|---|---|---|
| North | 40,000 | 34,000 |
| South | 30,000 | 29,000 |
| East | 20,000 | 14,000 |
| West | 10,000 | 9,000 |
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Contribution to the drop versus rate of drop.
**Say this in the interview:** "North and East explain about 86% of the 14,000 drop; East fell fastest at 30%."
**Definition in plain words:** Contribution = region's drop / total drop. Percent change = region's drop / its own last-week base.
**Worked answer:**
1. Total drop = 1,00,000 - 86,000 = 14,000 (-14%).
2. North: -6,000 (-15%), share of drop 6,000/14,000 = 42.9%.
3. South: -1,000 (-3.3%), 7.1%.
4. East: -6,000 (-30%), 42.9%.
5. West: -1,000 (-10%), 7.1%.
**Result:** North and East together = 12,000 of 14,000 = 85.7% of the drop; East is fastest in percent (-30%), North second (-15%).
**Check:** 34,000 + 29,000 + 14,000 + 9,000 = 86,000.
**Caveats:** Both views matter: North is big with a moderate rate; East is small with a severe rate. Investigate East first for a single cause (supply, local event) and North for scale. Only North (-15%) and East (-30%) fell faster than the total (-14%); West (-10%) and South (-3.3%) fell more slowly.
**Likely follow-ups:** 1) *Which do you fix first?* The one with the biggest recoverable orders, usually North, unless East has an obvious single cause. 2) *Next cut?* City inside East, platform.
**Common mistakes / traps:** Ranking only by percent; forgetting weights.

### Q15 ⭐⭐⭐ 🟡 Orders fell from 10,000 to 8,500 per week. New customers fell from 3,000 to 1,800 and repeat customers from 7,000 to 6,700 orders. What share of the drop comes from new customers, and what does that suggest you check next?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Splitting a drop by customer type and linking it to acquisition.
**Say this in the interview:** "New customers explain 80% of the 1,500 drop. I read the question as new-customer orders (3,000 to 1,800), so the next check is acquisition: ad spend, channels, install and signup funnels."
**Definition in plain words:** Share of drop = segment's fall / total fall.
**Worked answer:**
1. Total drop = 10,000 - 8,500 = 1,500 (-15%).
2. New: 3,000 - 1,800 = 1,200 (-40%).
3. Repeat: 7,000 - 6,700 = 300 (-4.3%).
4. New share = 1,200 / 1,500 = 80%; repeat share = 20%.
**Result:** 80% of the drop is new customers; repeat orders are almost stable.
**Check:** 1,800 + 6,700 = 8,500 (matches); 3,000 + 7,000 = 10,000.
**Caveats:** The question mixes "customers" and "orders"; I assume each figure is orders from that group. What to check next: acquisition spend and channel mix, cost per install, landing pages, signup to first-order conversion, first-order offers and competitor promos. A modest repeat fall can follow later because fewer new customers today means fewer repeats next month.
**Likely follow-ups:** 1) *Is the new-customer fall leading?* Yes, repeat falls lag. 2) *What data?* Orders by acquisition channel and first-order cohort.
**Common mistakes / traps:** Blaming loyalty when repeat is nearly flat; mixing customer counts with order counts.

### Q16 ⭐⭐⭐ 🟡 Tuesday orders normally are 1,000 out of 7,000 per week. This Tuesday they were 800 and every other day was normal. What was the weekly drop in percent, and does it justify an urgent investigation?
**Asked at:** commonly asked; the Tuesday example is this book's own (no source found with this wording).
**What the interviewer is checking:** Putting a single-day drop in proportion to the week, and judging urgency.
**Say this in the interview:** "The week fell by 200 of 7,000 orders, about 2.9%. A 20% Tuesday drop is notable, but the weekly impact is small; I would do a quick check, not a fire drill, unless it repeats."
**Definition in plain words:** Weekly drop = lost orders / normal weekly orders.
**Worked answer:**
1. Normal week = 7,000; this week = 7,000 - 200 = 6,800.
2. Weekly drop = 200 / 7,000 = 2.86% (about 2.9%).
3. Tuesday alone: 200 / 1,000 = 20%.
**Result:** About 2.9% weekly; 20% for that day.
**Check:** Tuesday 800 + other six days 6,000 = 6,800.
**Caveats:** Urgency depends on three things: does it repeat next Tuesday? Is it outside normal noise (see Q45, where 800 is far outside the usual range of about 980 to 1,020)? Is a cause plausible and growing (a bug, an outage)? My plan: 30-minute check of platform and release logs now, escalate if it repeats or spreads. Also compare Tuesday with Tuesday, not with other days.
**Likely follow-ups:** 1) *What if it were Friday, the biggest day?* The weekly impact would be larger, so more urgent. 2) *What if it is the start of a trend?* Watch a second Tuesday.
**Common mistakes / traps:** Calling it a 20% weekly drop; ignoring it completely because the week looks fine.

### Q17 ⭐⭐⭐ 🟡 A food-delivery app received 10,000 orders in each of two weeks. Cancelled orders were 500 in week 1 and 2,500 in week 2. How much did completed orders fall in percent, and what do you investigate?
**Asked at:** commonly asked; AmbitionBox cases on rising cancellations are mentioned for Meesho in a search summary (unverified).
**What the interviewer is checking:** Whether you separate placed from completed orders.
**Say this in the interview:** "Placed orders are flat, but completed orders fell about 21%, from 9,500 to 7,500, because cancellations rose from 5% to 25%. I look at who cancels and why."
**Definition in plain words:** Completed = placed - cancelled. Cancellation rate = cancelled / placed.
**Worked answer:**
1. Week 1 completed = 10,000 - 500 = 9,500; cancel rate 5%.
2. Week 2 completed = 10,000 - 2,500 = 7,500; cancel rate 25%.
3. Fall = 2,000 / 9,500 = 21.05%.
**Result:** Completed orders down about 21.1%; cancellation rate up 20 percentage points.
**Check:** The extra 2,000 cancellations equal the 2,000 lost completions.
**Caveats:** Investigate by who cancels (customer, restaurant, rider-unavailable), cancel reason codes, stage of cancellation (before or after acceptance), restaurant, city, time of day, delivery time and payment failures. Check for a stock-out, a rider shortage or an app bug that cancels automatically.
**Likely follow-ups:** 1) *Which side first?* Cancel reason codes. 2) *Impact on revenue?* Lost revenue plus refunds and goodwill cost.
**Common mistakes / traps:** Saying "no drop" because placed orders are flat; computing the drop on 10,000 as base.

### Q18 ⭐⭐⭐ 🟡 Revenue = active users x orders per user x AOV. Active users fell 5%, orders per user fell 8% and AOV rose 2%. By what percent did revenue change overall?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** That you multiply growth factors, not add percentages.
**Say this in the interview:** "Multiply the factors: 0.95 x 0.92 x 1.02 = 0.8915, so revenue fell about 10.9%, not 11%."
**Definition in plain words:** If revenue is a product, its percent change is the product of the factors (1 + each change) minus 1.
**Worked answer:**
1. Users factor 0.95; orders per user 0.92; AOV 1.02.
2. 0.95 x 0.92 = 0.874.
3. 0.874 x 1.02 = 0.89148.
4. Change = 0.89148 - 1 = -10.85%.
**Result:** Revenue fell about 10.85% (roughly 10.9%).
**Check:** The quick sum -5 - 8 + 2 = -11% is close; the gap is the small cross-terms. Test with revenue of 100: 100 x 0.89148 = 89.1.
**Caveats:** Users and orders per user together explain the fall; AOV rose, which softened it. A log split gives each driver's share of the fall: users about 45%, orders per user about 73%, AOV offsets about -17% (rounded).
**Likely follow-ups:** 1) *Which driver is biggest?* Orders per user. 2) *Is AOV up good?* It may be mix (only big spenders stayed).
**Common mistakes / traps:** Adding percentages; assuming all drivers are independent.

### Q19 ⭐⭐⭐ 🟡 Orders dropped 20% on a single day (a Tuesday) and recovered fully the next day. How do you investigate a one-day dip?
**Asked at:** commonly asked; wording is this book's own variant of the "Tuesday orders fell" example.
**What the interviewer is checking:** Treating a spike as an incident: check data first, then outage, then external events, then decide whether to chase it.
**Say this in the interview:** "A one-day dip that fully recovers is usually an outage, a data glitch or an event. I check pipeline and incident logs first, then the segment pattern, and I decide how much effort it is worth."
**Clarify first:** Which hours were affected? All cities? Orders placed or completed? Any alert or incident that day?
**Structure:**
- Data: late or lost events, a pipeline failure, a timezone cut-off.
- Technical: app, server or payment gateway downtime.
- External: festival, strike, heavy rain, a cricket match, a network outage.
- Business: a promo that ended, a restaurant partner outage.
**What I would check, in order:**
1. Orders by hour for that day vs normal Tuesdays: a clean block of missing hours points to an outage or data gap.
2. Incident and release logs, payment success rate by hour.
3. Cities and platforms: one city suggests local events, all suggests technical.
4. Backfilled data: did the numbers rise later (late events)?
5. Next-day orders: was there a catch-up (delayed demand) or are they truly lost?
**If the data shows...:** a block of missing hours plus an outage ticket, estimate lost orders (hours x normal rate x drop) and move on; a data gap that fills in later means no business loss; no technical cause and a pattern recurring on Tuesdays means start the weekday investigation (Q20).
**Recommendation:** document the cause, add an alert, and watch the next two Tuesdays.
**Likely follow-ups:** 1) *Is it worth a full analysis?* Only if it repeats or the loss is material. 2) *How do you separate lost from delayed?* See Q74.
**Common mistakes / traps:** Over-investigating one blip; assuming a business cause before ruling out data issues.

### Q20 ⭐⭐⭐ 🟡 Orders are down 20% only on Tuesdays and normal on other days. List the weekday-specific hypotheses you would test, grouped by demand, supply, operations, marketing and data.
**Asked at:** commonly asked; the Tuesday wording is this book's own example (no source found with this wording).
**What the interviewer is checking:** Creative but organised hypotheses that are specific to a weekday.
**Say this in the interview:** "Because only one weekday moved, I look for things that run on a weekly schedule: promos, partner weekly-offs, rider shifts, jobs and reports. I group them under five heads and attach a test to each."
**Clarify first:** Since when? Which cities? Orders placed or completed? Any change last week?
**Structure (hypotheses and the quick test):**
- **Demand:** a competitor's Tuesday deal (check customer overlap and search trends); a habit shift such as a religious or fasting day in some regions (look at order mix by cuisine); office-attendance change, e.g. work-from-home on Tuesdays (office-area orders).
- **Supply:** many partner restaurants closed on Tuesday (active restaurants on Tuesday); a stock-out pattern on weekly supply days (out-of-stock rate).
- **Operations:** fewer riders on a Tuesday roster (rider logins, delivery time, cancellation reasons); a Tuesday maintenance window or release (release log).
- **Marketing:** a weekly "Tuesday offer" ended or push notification schedule changed (promo orders, notification sends).
- **Data:** a Tuesday ETL job failing or a timezone cut-off (compare events with payments).
**What I would check, in order:** data check, then promos and notifications, then restaurants and riders, then external demand.
**If the data shows...:** promo orders gone, so restore the promo; restaurants down, so work on weekly-off incentives; payments fine but events down, so a data problem.
**Recommendation:** fix the top cause and watch the next four Tuesdays.
**Likely follow-ups:** 1) *What is the quickest test?* Active restaurants and promo orders on Tuesday. 2) *Which is most likely?* A schedule-based supply or promo change.
**Common mistakes / traps:** Listing generic causes with no weekday link; not grouping.

### Q21 ⭐⭐⭐ 🟡 You open the executive dashboard and see completed orders falling month-on-month. You are the analytics lead. What do you do, step by step?
**Asked at:** Meesho: a search summary of a candidate report mentions a case on completed orders falling month-on-month on the executive dashboard (unverified; no page opened in full).
**What the interviewer is checking:** Calm, ordered action: validate, quantify, localise, explain, recommend.
**Say this in the interview:** "I validate the number, size the drop, localise it by segment and funnel, test the top two hypotheses against the change log, then bring a finding and an action to the business owner."
**Clarify first:** Is it month vs previous month or vs same month last year? Same number of days? Is the metric definition unchanged? Who is asking and by when?
**Structure and steps:**
1. **Validate:** reconcile with finance or the order table; check late data and filters.
2. **Normalise:** per-day orders, weekday-adjusted, vs seasonal baseline.
3. **Size:** percent and absolute drop; completed vs placed vs cancelled.
4. **Localise:** funnel stage, platform, city, customer type, category, channel.
5. **Hypothesise:** release, price, promo, stock, delivery, competitor, season; map to change-log dates.
6. **Test and size:** how many orders each cause explains; stop at about 80%.
7. **Communicate:** headline, size, evidence, action, owner.
**What I would check, in order:** the steps above, each as one query or chart.
**If the data shows...:** a rise in cancellations means operations (Q17); a fall in new customers means acquisition (Q15); a data gap means fix the pipeline and republish.
**Recommendation:** share a one-page finding with the action and a metric and date to confirm recovery, and add an alert for next time.
**Likely follow-ups:** 1) *What if you have only 30 minutes?* Validate, then the biggest-contribution cut. 2) *Who do you tell first?* The owner of the affected area.
**Common mistakes / traps:** Skipping validation; presenting causes without sizes; no recommendation.

### Q22 ⭐⭐⭐ 🟡 A food-delivery platform's orders fell 20% week-over-week. How do you structure a diagnosis across customers, restaurants and delivery partners?
**Asked at:** PracHub lists a Swiggy "20% week-over-week orders fall" prompt (snippet-level, unverified).
**What the interviewer is checking:** A three-sided marketplace view: demand, supply, delivery.
**Say this in the interview:** "I treat it as a three-sided marketplace: customers who want food, restaurants who supply it, delivery partners who move it. Orders need all three, so I check which side broke first."
**Clarify first:** Placed or completed orders? All cities? Sudden or gradual? Any outage, release or festival?
**Structure:**
- **Customers (demand):** fewer active customers, fewer orders per customer, weaker new-customer acquisition, a smaller basket.
- **Restaurants (supply):** fewer active restaurants, shorter hours, more items out of stock, lower acceptance, rating drops.
- **Delivery partners (fulfilment):** fewer riders online, longer delivery time, higher cancellations, surge or weather shortages.
- **Cross-cutting:** app/payment issues, pricing and promos, competitors, season, data.
**What I would check, in order:**
1. Validate the drop and the funnel (open, browse, cart, order, deliver).
2. Active customers and orders per customer, new vs repeat.
3. Active restaurants and orders per restaurant by city; acceptance rate.
4. Riders online, delivery time, rider-unavailable cancellations.
5. Promo, fee and price changes; release log; competitor and weather signals.
**If the data shows...:** active customers flat but restaurants down means supply; high delivery time and "no rider" cancellations means delivery; fewer sessions means demand or marketing.
**Recommendation:** fix the side that moved first and verify via the leading indicator (for example riders online) and orders.
**Likely follow-ups:** 1) *How do you know which side fell first?* Compare timing in daily series. 2) *Which is most common?* There is no single answer; test all three.
**Common mistakes / traps:** Analysing only customers; ignoring that a supply shortage looks like a demand fall.

### Q23 ⭐⭐⭐ 🟡 An e-commerce company's gross sales were ₹100 crore in both months, but returns rose from 10% to 25% of gross sales. By what percent did net sales fall and which causes of rising returns do you check?
**Asked at:** commonly asked; a Flipkart return-window deep-dive question is mentioned in internal research (unverified).
**What the interviewer is checking:** Gross vs net sales and diagnosis of returns.
**Say this in the interview:** "Net sales fell from ₹90 crore to ₹75 crore, a 16.7% fall, with gross sales flat. The problem is returns, so I look at which products, sellers and reasons drive them."
**Definition in plain words:** Net sales = gross sales - returns. Return rate = returns / gross sales.
**Worked answer:**
1. Month 1 net = 100 - 10 = ₹90 crore.
2. Month 2 net = 100 - 25 = ₹75 crore.
3. Fall = 15 / 90 = 16.67%.
**Result:** Net sales down about 16.7% (₹15 crore); return rate up 15 percentage points.
**Check:** 75 / 90 = 0.833.
**Caveats:** Gross sales hid the problem. Causes to check: return reasons (wrong size, damaged, not as described, late delivery), category and seller mix (more fashion, more cash-on-delivery), a policy change (a longer return window), a quality or logistics issue, a fraud or abuse pattern, a promo that attracted low-intent buyers, or a timing effect (returns lag sales by days, so check by order cohort). Also check refunds booked vs returns received.
**Likely follow-ups:** 1) *Does the return rate lag?* Yes; use the order-month cohort. 2) *First cut?* Return rate by category, seller and reason.
**Common mistakes / traps:** Reporting gross sales as flat and stopping; using 25 points as the percent fall of net sales.

### Q24 ⭐⭐⭐ 🟡 An edtech company's course sales fell 20%. Data is below. Which part of the funnel explains the fall and what do you recommend checking?
| Item | Last month | This month |
|---|---|---|
| Ad spend | ₹10,00,000 | ₹10,00,000 |
| Cost per lead | ₹200 | ₹250 |
| Lead-to-sale conversion | 4% | 4% |
**Asked at:** commonly asked (no company-specific report found); "sales dropped 20%" wording appears in question banks (unverified).
**What the interviewer is checking:** Whether you break sales into stages (spend, leads, conversion) and find the one stage that moved.
**Say this in the interview:** Sales = leads x conversion, and leads = spend / cost per lead. Spend and conversion are flat, so the fall is entirely the cost per lead rising 25%, which cut leads by 20% (5,000 to 4,000) and sales from 200 to 160.

**Definition in plain words:** A lead is an interested person who left their details. Cost per lead (CPL) = ad spend / leads. Sales = leads x lead-to-sale conversion.
**Worked answer:**
1. Last month leads = 10,00,000 / 200 = 5,000. Sales = 5,000 x 4% = 200.
2. This month leads = 10,00,000 / 250 = 4,000. Sales = 4,000 x 4% = 160.
3. Change = (160 - 200) / 200 = -20%. CPL rose (250 - 200) / 200 = +25%.
**Result:** Top of the funnel (lead generation) explains 100% of the fall; the lead-to-sale step did not move. Sales fell 40 courses.
**Check:** 1 / 1.25 = 0.8, so a 25% dearer lead means 20% fewer leads at the same budget.
**Caveats:** Equal conversion does not prove lead quality is equal; check whether cheaper-to-buy leads had been replaced by a different source mix. Also ask why CPL rose: auction competition, creative fatigue, a narrower audience, tracking change.
**What I would recommend checking:** CPL by channel and campaign (Google, Meta, others), ad frequency and creative age, audience overlap, a competitor's exam-season bidding, and whether the conversion split by lead source stayed flat. Then reallocate budget to channels with the lowest cost per sale, not just per lead.

**Likely follow-ups:** (1) What if the conversion were also lower? Multiply both effects: 0.8 x conversion ratio. (2) Would raising spend fix it? Only if the extra leads cost no more than the current marginal CPL; test it.
**Common mistakes / traps:** Blaming the sales team because "sales" fell; using absolute sales without the funnel; ignoring that flat conversion hides a channel mix change.

### Q25 ⭐⭐⭐ 🟡 UPI payment success fell from 96% to 92%. Data is below. How much of the extra failures come from Bank X, and what do you do next?
| Segment | Attempts | Failures last week | Failures this week |
|---|---|---|---|
| Bank X | 3,00,000 | 12,000 | 48,000 |
| All other banks | 7,00,000 | 28,000 | 32,000 |
**Asked at:** commonly asked (no company-specific report found); PhonePe is reported (unverified) to use case rounds, but no UPI-failure report was seen.
**What the interviewer is checking:** Whether you attribute the change to a segment with arithmetic and then move to causes.
**Say this in the interview:** Total failures went from 40,000 to 80,000 on 10,00,000 attempts. Bank X added 36,000 of the 40,000 extra failures, 90%, so I would treat this as a Bank X incident first.

**Definition in plain words:** Failure rate = failed attempts / total attempts. A segment's share of the rise = its extra failures / total extra failures.
**Worked answer:**
1. Total attempts = 3,00,000 + 7,00,000 = 10,00,000. Last week failures = 12,000 + 28,000 = 40,000 (4%, so 96% success).
2. This week failures = 48,000 + 32,000 = 80,000 (8%, so 92% success).
3. Extra failures = 40,000. Bank X extra = 48,000 - 12,000 = 36,000. Others extra = 32,000 - 28,000 = 4,000.
4. Bank X share = 36,000 / 40,000 = 90%; others 10%.
5. Bank X failure rate: 4% to 16%. Others: 4% to about 4.6%.
**Result:** Bank X causes 90% of the extra failures. If Bank X had stayed at 4%, overall success would be about 95.6%.
**Check:** 36,000 + 4,000 = 40,000. 
**Caveats:** Bank X is 30% of traffic, so one bank moves the headline a lot. Assumes attempts were the same both weeks (the table gives one attempts column). Others' small rise may be a spillover or retries.
**Next steps:** Split Bank X failures by error code (technical decline, timeout, insufficient funds), by hour (a sudden jump means an outage or release), by app version and by transaction type. Contact the bank or switch routing to a backup; track the failure rate hourly after the fix.

**Likely follow-ups:** (1) How do you tell a bank outage from user error? Outages show one error code spiking at a specific time across all users. (2) Customer impact? Count retried-and-succeeded users separately.
**Common mistakes / traps:** Quoting only the overall 4 point fall; computing each segment's own percent change but not its share of the total change; forgetting retries.

### Q26 ⭐⭐⭐ 🟡 Diwali fell in November last year and in October this year. Sales (in ₹ lakh) are below. November is down 16.7% year-over-year. Is there a real problem?
| Month | Last year | This year |
|---|---|---|
| October | 100 | 130 |
| November | 120 | 100 |
**Asked at:** commonly asked (no company-specific report found); calendar-shift variants are a gap-fill, not seen in sources.
**What the interviewer is checking:** Whether you notice a festival moving between months and compare a combined window.
**Say this in the interview:** November alone is down 16.7% but the festival moved into October. October plus November is 230 against 220, up 4.5%, so there is no real problem on this evidence.

**Definition in plain words:** Year-over-year (YoY) change = (this year - last year) / last year, compared for the same period. When an event moves, compare a window that holds the event in both years.
**Worked answer:**
1. November YoY = (100 - 120) / 120 = -16.7% (matches the question).
2. October YoY = (130 - 100) / 100 = +30%.
3. Two-month total: last year 100 + 120 = 220; this year 130 + 100 = 230.
4. Combined change = (230 - 220) / 220 = +4.5%.
**Result:** About +4.5% over the festival window; the November dip is mostly timing.
**Check:** The October gain (+30) is larger than the November loss (-20), so the net is +10.
**Caveats:** Only two months are shown; a full festive window (for example the weeks around Diwali, or September to December) is safer. Pull-forward can also borrow from the post-festival weeks, and this-year growth of only 4.5% may still be below the company's plan, so compare against its target.
**Next steps:** Align by days-to-Diwali (for example 15 days before to 15 days after), then check the rest of the year.

**Likely follow-ups:** (1) Why not just compare to the plan? Plan may have used last year's calendar too. (2) Other moving events? Eid, Ramadan, financial year-end, salary days.
**Common mistakes / traps:** Calling the November number a crisis; or the opposite, saying all is well without checking the aligned window and trend.

### Q27 ⭐⭐⭐ 🟡 Sales dropped 20% in Hyderabad while all other cities are flat. What hypotheses and data cuts do you use?
**Asked at:** commonly asked (no company-specific report found); city-level drop variants are common in question banks (unverified).
**What the interviewer is checking:** Whether a localised drop leads you to local causes and clean data cuts, not a company-wide story.
**Say this in the interview:** Because only one city fell, I would rule out company-wide causes and focus on local supply, local competition, local events and local data. I would first confirm it is real, then split Hyderabad by area, category, channel and customer type.

**Clarify first:** Since when and how sudden? Which metric (orders, revenue, both)? Is Hyderabad a big share of sales (say 10%, which would be 2 percentage points of the total)? Any local launches or tech changes?
**Structure:**
- Data check: Hyderabad tagging, new city or pincode mapping, pipeline failure for one region.
- Demand: local festival or event, weather or floods, competitor launch or discount, local economic shock, a local strike.
- Supply: stock-outs in the Hyderabad warehouse, fewer delivery partners or sellers, delivery times up, hub closure.
- Internal: city-specific pricing or offer change, local marketing cut, local team or partner churn, app or payment problem on one carrier.
**What I would check, in order:** (1) Is the drop in raw order logs, not just the dashboard? (2) Daily trend: sudden step or slow slide. (3) Split by area or pincode: one cluster or all. (4) Split by category, new versus repeat, app versus web. (5) Supply: stock availability and delivery time versus other cities. (6) Offers and spend by city. (7) Compare with similar cities (Bengaluru, Chennai) as a control.
**If the data shows...:** Drop only in a few pincodes means a hub or delivery partner issue. Drop in every area and category from one date means a pricing, tech or competitor trigger. Gradual slide with falling repeat orders means experience or service quality.
**Recommendation:** Name the one or two largest explained segments, fix the fastest lever (restock, relaunch offer, escalate the partner), and track Hyderabad daily against the control cities.

**Likely follow-ups:** (1) How do you size it? Hyderabad share x 20% = effect on total. (2) What if the other cities are flat only because of a national campaign? Compare with last year's same weeks.
**Common mistakes / traps:** Jumping to competitor causes before data and supply checks; ignoring that other cities flat rules out national causes.

### Q28 ⭐⭐⭐ 🔴 Cart additions on an e-commerce app fell 15% over the last three days, mostly on the mobile app. How do you diagnose it?
**Asked at:** Flipkart-tagged "15% cart-addition drop" write-ups exist on prep sites and blogs (unverified; not opened in full).
**What the interviewer is checking:** A structured funnel and platform diagnosis, including release and tracking suspects.
**Say this in the interview:** Mobile-only and sudden points to something I shipped: an app release, a tracking change or a bug. I would check data integrity first, then release timing by platform, OS and version, then the browse-to-cart funnel.

**Clarify first:** Android, iOS or both? What fraction of cart adds is mobile app? Did traffic fall, or only the share that adds to cart? Any release, A/B test or campaign in the last week?
**Structure:**
- Measurement: event tracking broken or renamed, SDK change, consent banner blocking events.
- Product and tech: release or experiment, bug on the add-to-cart button, crashes, slower load, new OS version.
- Traffic: fewer visits, different traffic mix (paid versus organic, new versus returning).
- Supply and price: stock-outs, price increases, delivery fee display, new offers.
- External: competitor sale, payday timing, a festival.
**What I would check, in order:** (1) Do orders (a different pipeline) fall too? If not, suspect tracking. (2) Daily cart adds by platform, OS and app version; find the exact day the line bent. (3) Funnel: sessions, product views, cart adds; which ratio dropped. (4) Crash and error rates and page load time from monitoring. (5) Experiments running on that date. (6) Cart adds per product view by category.
**If the data shows...:** One app version down and others flat means a release bug, so roll back or hotfix. Views fell but view-to-cart steady means a traffic problem. View-to-cart fell in all versions on the same day means price, stock or tracking.
**Recommendation:** Share the finding and sized impact, fix or roll back, and set an alert on view-to-cart by app version so the next break shows in hours.

**Likely follow-ups:** (1) How do you size it? Cart adds x cart-to-order conversion x AOV. (2) What if only 15% overall but 30% on one version? That version is the culprit.
**Common mistakes / traps:** Looking only at overall funnel; not checking tracking; blaming marketing before checking the release calendar.

### Q29 ⭐⭐⭐ 🔴 Leadership says a 20% drop in revenue is 'just seasonal'. How do you prove or disprove that with data?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can test a claim with history, not accept or reject it by instinct.
**Say this in the interview:** I would build the expected number from past years for the same weeks. If the usual seasonal dip is, say, 15% and we fell 20%, then seasonality explains most but not all, and 5 points need another cause.

**Clarify first:** How many years of history exist? Which weeks does the "drop" compare? Is the product's seasonality stable, and has the business changed (new cities, new products)?
**Structure:** Actual change = seasonal change + trend + one-off events + unexplained.
**What I would check, in order:** (1) Seasonal index per month or week: that period's average over the yearly average, using 2-3 prior years. (2) Expected value = a normal level x index. (3) Compare YoY for the same weeks, and check the same weeks in several years. (4) Compare with other regions, categories or a peer's public trend. (5) Check events (price, release, stock) timed with the dip.
**If the data shows...:** Past years fall by about the same percent in the same weeks and actual is within the normal range, so leadership is right. If the past dip was much smaller, or this year's fall started earlier or is deeper, it is not just seasonal.
**Numeric work (illustrative, not real data):** Normal monthly sales 100, seasonal index 0.85, so expected 85. Actual 80. Total drop vs normal = 20; seasonal part = 15 (75%); unexplained = 5, which is 5.9% below the seasonal expectation (80 / 85 - 1 = -5.9%).
**Recommendation:** Report both numbers ("15 points seasonal, 5 points to explain"), investigate the 5, and keep a seasonal baseline in the dashboard.

**Likely follow-ups:** (1) What if only one year of data exists? Say so and use the cross-section: segments that should be seasonal versus those that are not. (2) Is YoY enough? Not if holidays moved; align by event.
**Common mistakes / traps:** Accepting "seasonal" without a number; comparing to last month only; using a seasonal index from years with abnormal events.

### Q30 ⭐⭐⭐ 🔴 A price change, a competitor promotion and an app release all happened in the week orders fell 20%. How do you apportion the drop between them?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you use exposure differences (who saw which change) to separate overlapping causes, and are honest about overlap.
**Say this in the interview:** I would find groups that saw only some of the changes and use the unaffected group as control. What the control fell is the common baseline; extra falls in exposed groups are attributed to the change they alone saw.

**Clarify first:** Did each change hit everyone, or only some cities or platforms? Exact dates and times? Do I have order logs by city, platform and app version?
**Structure:** Total drop = common or external part + price part + release part + competitor part + overlap.
**What I would check, in order:** (1) Drop by day to see which change lines up with the start. (2) Split by platform and app version (release exposure). (3) Split by city, SKU or customer group that did or did not get the price change. (4) Compare cities where the competitor ran the promotion versus where it did not. (5) Try a simple regression of orders on the three exposure flags, with city and day effects.
**If the data shows...:** Where the groups are cleanly separated, differences give rough shares. If all three hit everyone at once, say it cannot be separated by data alone and propose a reversal test (restore the old price in a small test group) or an experiment.
**Numeric work (illustrative):** 10,000 orders fell to 8,000 (drop 2,000). The group with no price change, no release and no promo exposure fell 5% (500 orders on a 10,000 base). Extra fall 1,500: 1,000 sits where only the release applied, 500 where only the price applied. So release 50%, price 25%, common or competitor 25% of the drop. Overlap groups are given as a range.
**Recommendation:** Present shares as ranges with the method, act on the biggest and most reversible (rollback or price test), and run a small holdout for the rest.

**Likely follow-ups:** (1) Why not simply split evenly? Evenly has no evidence. (2) What if the effects interact? Report the overlap as its own bucket.
**Common mistakes / traps:** Claiming exact shares from one time series; ignoring the common baseline; attributing to the last event on the calendar.

### Q31 ⭐⭐⭐ 🔴 The CEO wants the cause of a 20% orders drop within one hour and only partial data is available. What do you deliver?
**Asked at:** commonly asked (no company-specific report found); a recruiter source (Taggd, unverified) says candidates must frame a business question and defend a recommendation.
**What the interviewer is checking:** Prioritisation, honesty about uncertainty and communication under time pressure.
**Say this in the interview:** I deliver a one-page status, not a final root cause: what is confirmed, what is ruled out, my top two hypotheses with a rough size, what is still unknown, and the next step with an ETA. I do not claim certainty I do not have.

**Clarify first:** Which orders and which dates? What data is available now (orders table, release log, ops alerts)? Who can I call (tech, supply, marketing) in 10 minutes?
**Structure:** Hour plan: 0-10 min, validate the drop is real and fix scope; 10-35 min, three fast cuts (platform and version, city, funnel stage); 35-50 min, ask owners about launches, outages, promotions; 50-60 min, write the one-pager.
**What I would check, in order:** (1) Raw count, not just dashboard. (2) Daily and hourly shape to date the start. (3) Cuts by platform, city, new versus repeat, funnel stage. (4) Release, price, outage and campaign calendars. (5) Complete-data check: is recent data still loading?
**If the data shows...:** One segment explains most of the drop, so state the likely cause with a confidence label. Nothing stands out, so say "no single segment found; data gap on X" and list the data to pull.
**Recommendation:** Hand over: (a) current finding with confidence (high, medium, low); (b) immediate safe actions (rollback, restock, pause a promo); (c) what I will confirm by when; (d) who is needed. Update at fixed times.

**Likely follow-ups:** (1) What if the CEO insists on one cause? Give the most likely one, clearly marked as a hypothesis. (2) How do you mark confidence? By how many independent checks support it.
**Common mistakes / traps:** Staying silent until certain; presenting a guess as fact; skipping the data-validity check.

### Q32 ⭐⭐ 🟢 How do you use the 5 Whys in a sales-drop analysis, and what are its limits?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can chain causes to a root and know that the method is not proof.
**Say this in the interview:** I keep asking "why" until I reach a cause I can act on and check with data. It is useful for one linear chain, but it can mislead when there are many causes, so I back each step with a number.

**Explain simply:**
- The 5 Whys means asking "why" repeatedly (about five times) so you move from symptom to cause.
- Example chain: Sales fell 20%. Why? Fewer orders. Why? Fewer repeat customers. Why? Late deliveries. Why? Fewer delivery partners in the evening. Why? A payout cut last month. Action: review payouts.
- Each "why" must be tested with data (for example repeat orders by delivery time), not assumed.
- Limits: it follows one path and misses parallel causes; it depends on who answers; it can stop at a convenient answer; it does not quantify impact.
**Example:** If late deliveries explain 600 of a 2,000-order drop, the chain covers 30%, so the other branches need their own chains.
**Practice step:** Take any drop you know and write a five-step chain; next to each step note the data that would prove it.

**Likely follow-ups:** (1) Why exactly five? It is a rule of thumb; stop at an actionable cause. (2) What do you pair it with? An issue tree for breadth.
**Common mistakes / traps:** Treating the chain as proof; blaming people (the "who") instead of processes; using it without data.

### Q33 ⭐⭐ 🟢 You find that discounts and orders both fell in the same week. How do you tell correlation from a root cause?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Causal thinking: direction, confounders and tests.
**Say this in the interview:** Discounts and orders moving together does not show discounts drove orders. I check timing, whether orders fell for people who never received a discount, and whether a hidden factor moved both.

**Explain simply:**
- Correlation means two numbers move together; a root cause means changing one changes the other.
- Check direction: did discounts end first, or did low demand make the team stop discounting?
- Check a third factor: stock-outs or a festival could cut discounts and orders together.
- Compare groups: orders among customers who still got a discount versus those who did not, in the same week.
- Check dose-response: were bigger discount cuts followed by bigger order falls?
- Best proof: a small test or holdout where discounts are restored for a random group.
**Example (illustrative):** Discount users' orders fell 10% and non-discount users' orders fell 10% too. Then discounts cannot be the cause; something common affected both.
**Practice step:** For any two series, write the three alternative stories (reverse cause, third factor, coincidence) and one data check for each.

**Likely follow-ups:** (1) What if you cannot experiment? Use matched groups or before-after with a control. (2) What if timing matches exactly? Still check confounders.
**Common mistakes / traps:** Saying "correlation is not causation" and stopping; not naming a test; ignoring reverse causation.

### Q34 ⭐⭐ 🟢 On a 'sales dropped' ticket, which tables and fields do you ask for first?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know what data a diagnosis needs and ask precisely.
**Say this in the interview:** Orders first, then the tables that explain them: customers, products, sessions, price and promotions, supply, and a change log. I ask for dates, status and keys so I can cut by every dimension.

**Explain simply:**
- Orders or sales table: order id, order timestamp, customer id, product id, city, platform, amount, discount, status (placed, cancelled, returned). Without status you cannot separate completed from cancelled.
- Customers: signup date, city, channel (to separate new from repeat).
- Products: category, price, stock status or inventory snapshot.
- Sessions or events: visits, product views, cart adds, checkout (funnel).
- Promotions and pricing: start and end dates, discount percent, codes.
- Operations and supply: delivery times, delivery partners, outages, stock-outs.
- Change log: releases, experiments, campaigns, policy changes.
- Plus: a calendar of holidays and a data-load log.
**Example:** Joining orders, customers and sessions lets me say "new-customer orders on Android fell 40%" instead of "orders fell".
**Practice step:** Write a one-line request message with these tables, the date range (four weeks before to now plus the same period last year) and the grain you need.

**Likely follow-ups:** (1) What do you ask for first if time is short? Orders with status, platform and city. (2) How far back? At least the same weeks last year for seasonality.
**Common mistakes / traps:** Asking only for the sales total; forgetting order status and timestamps; no change log.

### Q35 ⭐⭐ 🟢 How does your investigation change for a one-time dip, a step change and a gradual decline?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Matching the shape of the drop to the likely cause and method.
**Say this in the interview:** The shape tells me where to look: a one-day dip means an event or outage, a step means something changed on a date, a slope means slow erosion in users, quality or competition.

**Explain simply:**
- One-time dip (recovers fast): look for outages, data load gaps, a holiday or weather, a payment gateway problem. Often needs a post-mortem and monitoring, not a strategy change.
- Step change (new lower level that stays): find the exact date and list every change near it (release, price, policy, competitor entry, tracking change). Cut by who was exposed; consider a rollback.
- Gradual decline: look at cohorts, repeat rate, ratings, acquisition mix, competition and product fit; trends over months, not days.
**Example:** Orders 1,000 per day, then 800 for one day: dip. 1,000 then 800 every day from the 15th: step. 1,000 falling about 2% a week: slope; after 10 weeks about 817.
**Practice step:** Plot any metric by day and label each pattern, then list two causes for each.

**Likely follow-ups:** (1) Which is hardest? Gradual, because there is no date to anchor. (2) How do you tell a step from noise? Compare to normal variation (see Q45).
**Common mistakes / traps:** Treating a dip with long-run strategy work; searching for a "date" in a gradual decline.

### Q36 ⭐⭐ 🟢 How do you size the impact of a hypothesis so you know whether it explains the whole drop?
**Asked at:** commonly asked (no company-specific report found); "quantify each hypothesis" appears in RCA prep material (unverified).
**What the interviewer is checking:** Turning a story into a number and comparing it with the total.
**Say this in the interview:** For each hypothesis I estimate affected volume x change in rate, then divide by the total drop. I add the shares up; if they do not reach about 80%, I keep looking.

**Explain simply:**
- Impact = size of the affected group x how much that group changed.
- Share explained = impact / total drop.
- Do it for each hypothesis, then sum, watching for overlap so the same orders are not counted twice.
**Example (illustrative):** Orders fell 10,000 to 8,000 (drop 2,000). Hypothesis A: Tuesday partner restaurants closed; affected Tuesday orders 1,000, down 20%, impact 200, which is 200 / 2,000 = 10% of the drop. Hypothesis B: Android bug; Android baseline 6,000, down 15%, impact 900, which is 45%. Together 55%, so 45% remains unexplained and needs more hypotheses.
**Practice step:** For your last three hypotheses, write "who is affected x how much" and the share explained.

**Likely follow-ups:** (1) What if hypotheses overlap? Use mutually exclusive segments. (2) When to stop? See Q41.
**Common mistakes / traps:** Testing a hypothesis without ever sizing it; summing above 100% from overlap; sizing percent changes instead of volumes.

### Q37 ⭐⭐ 🟢 What are leading and lagging indicators, and how do they help diagnose a decline in orders?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know which metrics move first and use them to find where the decline began.
**Say this in the interview:** Leading indicators move before orders do (app opens, searches, cart adds); lagging ones confirm after (orders, revenue). If orders fell, I walk back the leading chain to find where the break first appears.

**Explain simply:**
- Lagging: results already happened (orders, revenue, retention at day 30).
- Leading: early signals that predict them (visits, searches, cart adds, signups, ratings, delivery time).
- For diagnosis, line up the series by date. The earliest one to bend points at the origin.
- HR analogy: attendance dips and late logins lead; attrition lags.
**Example (illustrative):** Delivery time rose in week 1, ratings fell in week 2, repeat orders fell in week 3, orders in week 4. The chain suggests delivery time is the root, though it still needs testing (Q47, Q56).
**Practice step:** Pick one lagging metric and write three leading indicators and the data source for each.

**Likely follow-ups:** (1) Can an indicator be both? Yes, depending on the question; revenue leads profit. (2) Danger? Leading metrics may not truly predict; check the lag historically.
**Common mistakes / traps:** Using only lagging metrics; assuming leading means causal.

### Q38 ⭐⭐ 🟢 Conversion fell from 5% to 4%. What is the drop in percentage points and in percent, and why does the difference matter in a root-cause discussion?
**Asked at:** commonly asked (no company-specific report found); percent versus percentage point is a gap-fill item.
**What the interviewer is checking:** Precision with rates.
**Say this in the interview:** It fell 1 percentage point, which is a 20% relative drop. For the same traffic, orders fall 20%, not 1%, so the number I quote must match the one the business feels.

**Definition in plain words:** Percentage points (pp) are the plain subtraction of two rates. Percent change is that gap divided by the starting rate: (4% - 5%) / 5%.
**Worked answer:**
1. Drop in points = 5% - 4% = 1 pp.
2. Relative drop = 1 / 5 = 20%.
3. With 1,00,000 visitors: orders go from 5,000 to 4,000, a 20% fall.
**Result:** 1 percentage point; 20% relative.
**Check:** 5% x 0.8 = 4%.
**Caveats:** Say which one you mean every time. In sizing, use relative change times volume; for comparing two segments' rates, the gap in pp is often clearer. Also note that a fall from 50% to 49% is the same 1 pp but only a 2% relative change.

**Likely follow-ups:** (1) If conversion rises 4% to 5%? +1 pp, +25%. (2) Which to report to executives? Relative change plus the absolute order impact.
**Common mistakes / traps:** Saying "conversion fell 1%" (ambiguous); dividing by the new rate (1/4 = 25%).

### Q39 ⭐⭐ 🟢 AOV fell 10% but order count is flat. What hypotheses do you check?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Splitting AOV (average order value) into items per order and price per item, and into mix.
**Say this in the interview:** With orders flat, revenue is down 10%. AOV = items per order x average price per item, so I check basket size, price or discount, product mix and customer mix.

**Explain simply:**
- Basket size: fewer items per order (free-delivery threshold changed, cross-sell widget removed).
- Price: lower list prices, bigger discounts or coupons, or a mix to cheaper items.
- Mix: a category shift, a new low-priced range, more new customers (usually smaller first baskets).
- Segments: one city or platform with lower-value orders; small-value cancelled-order pattern.
- Data: currency, tax or shipping fee treatment changed; refunds netted.
**Example (illustrative):** 10,000 orders at ₹500 AOV is ₹50,00,000; at ₹450 it is ₹45,00,000. A ₹50 drop could be 0.5 fewer items at ₹100 each.
**Practice step:** Split AOV into items per order and price per item for two weeks, and see which moved.

**Likely follow-ups:** (1) Is this bad? Check margin; low AOV with high volume may be fine. (2) Median versus mean? Check both; outliers can drive the mean.
**Common mistakes / traps:** Looking at order count only; not separating price from basket size.

### Q40 ⭐⭐ 🟢 This month has 4 Tuesdays and last month had 5. Tuesday orders were 5,000 per Tuesday in both months. Tuesday orders fell from 25,000 to 20,000 in total. Is that a real 20% drop?
**Asked at:** commonly asked (no company-specific report found); calendar-effect variants are a gap-fill, not seen in sources.
**What the interviewer is checking:** Normalising for number of days.
**Say this in the interview:** No. Each Tuesday still had 5,000 orders. The total fell 20% only because there was one fewer Tuesday, so the real change per Tuesday is 0%.

**Definition in plain words:** Compare per-day averages, not totals, when the number of days differs. Per-Tuesday orders = total / count of Tuesdays.
**Worked answer:**
1. Last month: 25,000 / 5 = 5,000 per Tuesday.
2. This month: 20,000 / 4 = 5,000 per Tuesday.
3. Per-Tuesday change = 0%. Total change = (20,000 - 25,000) / 25,000 = -20%, fully a calendar effect.
**Result:** No real drop; 0% per Tuesday.
**Check:** 5,000 x 4 = 20,000 and 5,000 x 5 = 25,000.
**Caveats:** Note the premise says the per-Tuesday figures are equal, so the stated drop is arithmetic only. Also compare with same-weekday-versus-weekday patterns; month totals differ for other days too.

**Likely follow-ups:** (1) How to avoid it in dashboards? Show orders per day or per same-weekday. (2) What about a 28-day versus 31-day month? Use per-day (see Q72).
**Common mistakes / traps:** Calling 25,000 to 20,000 a drop; running a long investigation on a calendar artefact.

### Q41 ⭐⭐ 🟢 How do you decide that a root-cause analysis is finished and you can recommend an action?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Judgement on "enough evidence" and the link to action.
**Say this in the interview:** I stop when the identified causes explain most of the drop in numbers (about 80% or more), the main cause is supported by more than one check, and I have an action to try that is measurable. I state remaining uncertainty openly.

**Explain simply:**
- Coverage: the sized causes add up to most of the drop; the unexplained part is small and stated.
- Consistency: timing, segment and mechanism agree (not just one chart).
- Alternatives ruled out: data errors, seasonality, calendar effects checked.
- Actionability: the cause is something the company can change, and the action has an owner and a metric.
- Cost of waiting: when the fix is cheap and reversible, act earlier; when it is costly, test more.
**Example (illustrative):** Drop 2,000 orders. Android bug explains 1,200 and a partner outage 400: 80% explained. Recommend a hotfix and monitor Android orders daily for a week.
**Practice step:** Before presenting, write the sentence "This explains X% of the drop; I am sure because A and B; the rest is unknown because C."

**Likely follow-ups:** (1) Is 100% needed? No, rarely reachable. (2) What if you cannot get to 80%? Present what you know and propose an experiment.
**Common mistakes / traps:** Stopping at the first plausible story; never stopping; presenting causes with no sizes.

### Q42 ⭐⭐ 🟡 A website's overall conversion fell although no segment's conversion changed. Data is below. Compute the overall conversion in both weeks and explain the cause.
| Platform | Traffic share week 1 | Conversion week 1 | Traffic share week 2 | Conversion week 2 |
|---|---|---|---|---|
| Android | 80% | 4% | 90% | 4% |
| iOS | 20% | 8% | 10% | 8% |
**Asked at:** mix-shift and Simpson's paradox style questions appear in company blogs (Sequoia, Spotify); no interview report found.
**What the interviewer is checking:** Whether you see a mix shift as the cause, not a performance problem.
**Say this in the interview:** Overall conversion went from 4.8% to 4.4%. No platform got worse; traffic moved toward the lower-converting Android, so it is a mix effect.

**Definition in plain words:** Overall conversion = sum of (traffic share x segment conversion). A mix shift is a change in the shares.
**Worked answer:**
1. Week 1: 0.80 x 4% + 0.20 x 8% = 3.2% + 1.6% = 4.8%.
2. Week 2: 0.90 x 4% + 0.10 x 8% = 3.6% + 0.8% = 4.4%.
3. Change = -0.4 pp, which is -8.3% relative.
4. Rate effect = 0 (segment rates unchanged), so the entire -0.4 pp is mix.
**Result:** 4.8% to 4.4%; 100% mix effect.
**Check:** If week 2 kept the week 1 mix, overall would be 4.8%.
**Caveats:** The mix shift itself may need a story: iOS traffic halved (10% vs 20% share), perhaps from a campaign change or a tracking issue on iOS. Do not call the site worse; do ask why iOS traffic fell.

**Likely follow-ups:** (1) Is the business worse? Orders per visitor fell, so yes, in total orders unless traffic rose. (2) How to avoid confusion? Report segment rates and shares side by side.
**Common mistakes / traps:** Looking for a conversion bug; failing to compute the weighted average.

### Q43 ⭐⭐ 🟡 A SaaS company's MRR (in ₹ lakh) moved as below. Compute closing MRR and say which component is the main culprit in the 5% fall.
| Opening MRR | New | Expansion | Contraction | Churn |
|---|---|---|---|---|
| 100 | +8 | +4 | -3 | -14 |
**Asked at:** commonly asked (no company-specific report found); the MRR bridge is a gap-fill item.
**What the interviewer is checking:** Reading an MRR (monthly recurring revenue) bridge and spotting the dominant leak.
**Say this in the interview:** Closing MRR is 95, down 5%. New and expansion add 12; contraction and churn remove 17. Churn at 14 is the main culprit.

**Definition in plain words:** Closing MRR = opening + new + expansion - contraction - churn. Churn is revenue lost from customers who left; contraction is downgrades; expansion is upsell.
**Worked answer:**
1. 100 + 8 + 4 - 3 - 14 = 95.
2. Change = -5, which is -5%.
3. Gains = 8 + 4 = 12; losses = 3 + 14 = 17; net = -5.
4. Churn is 14 / 100 = 14% of opening MRR and 82% of the 17 lost.
**Result:** Closing MRR ₹95 lakh; churn is the main culprit.
**Check:** Net new MRR (new + expansion - contraction) = +9; churn -14; total -5.
**Caveats:** Churn of 14% in one month is very high (check whether this is monthly or a quarter, or one big customer). New MRR of 8 is smaller than churn, so acquisition cannot offset it. Split churn by plan, tenure, size and reason.

**Likely follow-ups:** (1) Which metric next? Gross and net revenue retention: gross = (100 - 3 - 14) / 100 = 83%; net = (100 + 4 - 3 - 14) / 100 = 87%. (2) What to check? Churned accounts by segment and any pricing or product change.
**Common mistakes / traps:** Saying contraction is churn; blaming acquisition; not checking whether one large customer drove the 14.

### Q44 ⭐⭐ 🟡 Weekly active users fell from 50,000 to 45,000. Data is below. Which component drives the fall and what do you check next?
| Component | Last week | This week |
|---|---|---|
| Retained users | 40,000 | 38,000 |
| New users | 8,000 | 5,000 |
| Resurrected users | 2,000 | 2,000 |
**Asked at:** commonly asked (no company-specific report found); a DAU/WAU decline framework search failed, so no source is cited.
**What the interviewer is checking:** Splitting active users into retained, new and resurrected, and sizing each.
**Say this in the interview:** The fall is 5,000: new users account for 3,000 (60%) and retained users for 2,000 (40%); resurrected users did not change. I check acquisition first, then retention.

**Definition in plain words:** Weekly active users (WAU) = retained + new + resurrected. Retained were active in the previous period too; new signed up this period; resurrected came back after a gap.
**Worked answer:**
1. Last week: 40,000 + 8,000 + 2,000 = 50,000. This week: 38,000 + 5,000 + 2,000 = 45,000. Fall = 5,000 (-10%).
2. Retained: -2,000 (-5%). New: -3,000 (-37.5%). Resurrected: 0.
3. Shares of the fall: new 3,000 / 5,000 = 60%; retained 2,000 / 5,000 = 40%.
**Result:** New users drive the biggest part, but retained users also fell 5%.
**Check:** -2,000 - 3,000 + 0 = -5,000.
**Caveats:** The table uses the same row names in both weeks without defining which base "retained" is measured on; I assume each is that week's headcount. Retention rate needs the previous week's base, which is not given here. The new-user fall also shrinks next week's retained pool.
**Next checks:** New users by channel, campaign, install source and country (did a campaign end or tracking break?); retained users by cohort and app version; whether onboarding or notifications changed.

**Likely follow-ups:** (1) Which matters more long-term? Retention, but new-user falls feed it. (2) Why do resurrected matter? They respond to reactivation campaigns.
**Common mistakes / traps:** Looking at percent only (new -37.5% looks worst but retained is bigger in base); mixing weekly retention definitions.

### Q45 ⭐⭐ 🟡 The last eight Tuesdays had 1,000, 1,020, 980, 1,010, 990, 1,005, 995 and 1,000 orders. This Tuesday had 800. Is 800 within normal noise? Show a quick calculation using mean and standard deviation.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Using a mean and standard deviation (SD) to separate a real drop from ordinary variation.
**Say this in the interview:** The eight Tuesdays average 1,000 with a standard deviation of about 12. 800 is 200 below the mean, about 16 SDs, so it is far outside normal noise and deserves investigation.

**Definition in plain words:** The mean is the average. The standard deviation is the typical distance of a value from the mean. A common rule: values more than 3 SDs away are unusual.
**Worked answer:**
1. Mean = (1,000 + 1,020 + 980 + 1,010 + 990 + 1,005 + 995 + 1,000) / 8 = 8,000 / 8 = 1,000.
2. Differences from mean: 0, 20, -20, 10, -10, 5, -5, 0; squares: 0, 400, 400, 100, 100, 25, 25, 0 = 1,050.
3. Sample SD = square root of 1,050 / 7 = square root of 150 = about 12.2.
4. Normal range (mean plus or minus 3 SDs) = about 963 to 1,037.
5. 800 is (800 - 1,000) / 12.2 = about -16.3 SDs.
**Result:** 800 is far outside the normal range: a real drop, down 20%.
**Check:** Even with the population SD (11.5) the answer is about -17 SDs. Even if SD were 50, 800 would still be -4 SDs.
**Caveats:** Eight points is a small sample; check it was not a holiday or a data delay; if usual levels trend or have seasonality, compare with the trend-adjusted expectation.

**Likely follow-ups:** (1) What would be within noise? About 965 to 1,035. (2) Next step? Confirm data completeness, then cut by segment (Q19, Q20).
**Common mistakes / traps:** Quoting only "20% lower" without a noise scale; using a very short history; not checking holiday or data issues.

### Q46 ⭐⭐ 🟡 Ride requests were 1,00,000 in both weeks. Driver acceptance fell from 85% to 70% and 95% of accepted rides are completed in both weeks. By what percent did completed rides fall and where do you look?
**Asked at:** commonly asked (no company-specific report found); ride-hailing variant is a gap-fill, not seen in sources.
**What the interviewer is checking:** Multiplying the funnel stages and finding the stage that moved.
**Say this in the interview:** Completed rides = requests x acceptance x completion. Requests and completion are flat, so completed rides fell by the same percent as acceptance: from 80,750 to 66,500, down 17.6%. I look at the driver side.

**Definition in plain words:** Acceptance rate = accepted rides / requests. Completion rate = completed / accepted.
**Worked answer:**
1. Week 1: 1,00,000 x 85% = 85,000 accepted; x 95% = 80,750 completed.
2. Week 2: 1,00,000 x 70% = 70,000 accepted; x 95% = 66,500 completed.
3. Change = (66,500 - 80,750) / 80,750 = -17.6% (a loss of 14,250 rides).
4. Acceptance fell 15 pp, which is 15 / 85 = 17.6% relative.
**Result:** Completed rides fell about 17.6%.
**Check:** 70 / 85 = 0.8235, so a fall of 17.6%.
**Caveats:** Acceptance depends on both supply (enough drivers online) and driver choice (trip not worth it). Demand is flat, so the issue is on the supply side.
**Where I look:** Online driver count and hours; acceptance by time of day, zone and trip length; fares, surge and incentives (did driver incentives or commission change?); pickup distance and cancellation reasons; city events (rain, strike); app problems in the driver app.

**Likely follow-ups:** (1) What if requests also fell? Multiply the effects. (2) Which metric to watch daily? Acceptance by zone and hour.
**Common mistakes / traps:** Saying the fall is 15% (percentage points) instead of 17.6%; blaming demand when requests are flat.

### Q47 ⭐⭐ 🟡 A quick-commerce app's average delivery time rose from 10 to 16 minutes and orders fell. How do you test whether slower delivery caused the fall and not the other way round?
**Asked at:** commonly asked (no company-specific report found); quick-commerce root-cause prompts of this type appear on prep sites (unverified).
**What the interviewer is checking:** Whether you separate correlation from cause and can name a test for the direction of cause (reverse causality).
**Say this in the interview:** "Both numbers moved together, so I need timing and a mechanism. I would check which moved first, whether the same orders were hit, and whether slow areas lost more orders than fast areas."
**Clarify first:** Is 16 minutes an average (a few very slow orders can drag it up)? Over what dates? Did anything else change (app release, price, stock)?
**Structure:** Two stories. (1) Slow delivery causes fewer orders: customers see long ETAs, cancel or do not return. (2) Fewer orders cause slow delivery: for example, fewer orders mean riders leave the area, or dark stores run lean. Also (3) a third factor drives both, such as rain or a rider strike.
**What I would check, in order:**
- Timeline by day: did delivery time rise before orders fell? Slower first supports story 1.
- Cut by area or dark store (a local fulfilment centre): do stores with the biggest delay rise show the biggest order drop? A dose-response pattern (bigger delay, bigger drop) supports cause.
- Look at the funnel: do more people open the app and see a long ETA, then leave without ordering? That shows the customer reaction directly.
- Look at rider supply and cancellations: if riders left first, story 2 is weaker.
- Compare weather, strike or holiday days for story 3.
**If the data shows...:** Delay rises first and the drop is bigger where the delay is bigger: delivery is the likely cause. Orders fall first, then riders log off: reverse. Both move on rainy days only: common cause.
**Recommendation:** Fix delivery in the worst stores first (add riders, adjust ETA display) and measure whether orders recover there before the rest.
**Likely follow-ups:** (1) Can you run a test? Yes, add riders in half the stores and compare. (2) Why not just correlate? Correlation cannot give direction.
**Common mistakes / traps:** Calling the match causation; using only the city average and missing store-level variation; ignoring that fewer orders can themselves change delivery time.

### Q48 ⭐⭐ 🟡 A lending app's loan disbursals fell. Data is below. Compute disbursals in both months and the percent change, and name the likely driver.
| Item | Last month | This month |
|---|---|---|
| Applications | 50,000 | 48,000 |
| Approval rate | 40% | 32% |
| Approved loans actually disbursed | 90% | 90% |
**Asked at:** commonly asked (no company-specific report found); funnel-style numeric cases are common in product rounds (unverified).
**What the interviewer is checking:** Whether you multiply the funnel stages and find which stage caused the fall.
**Say this in the interview:** "Disbursals are applications times approval rate times disbursal rate. They fell from 18,000 to 13,824, down 23.2%, and the approval rate is the main driver."
**Definition in plain words:** Disbursals = loans actually paid out. Disbursals = applications x approval rate x share of approved loans disbursed.
**Worked answer:**
1. Last month: 50,000 x 0.40 = 20,000 approved; x 0.90 = 18,000 disbursed.
2. This month: 48,000 x 0.32 = 15,360 approved; x 0.90 = 13,824 disbursed.
3. Change: 13,824 / 18,000 - 1 = -23.2% (4,176 fewer loans).
4. Split by stage: applications 48,000/50,000 = -4%; approval 32/40 = -20%; disbursal rate 0%.
**Result:** 18,000 to 13,824, -23.2%. Driver: approval rate (-20%), with applications adding a small -4%.
**Check:** 0.96 x 0.80 x 1.00 = 0.768, which is -23.2%. Matches.
**Caveats:** The approval rate fell 8 percentage points (40% to 32%), which is a 20% relative fall; do not mix the two. Next, ask why: stricter credit rules, a riskier applicant mix (for example a new marketing channel), or a model or data-feed problem.
**Likely follow-ups:** (1) Is the fall bad? Not necessarily; the lender may have tightened risk on purpose. Check defaults. (2) What would you check next? Approval rate by channel and by credit-score band.
**Common mistakes / traps:** Adding percentage changes (-4% and -20% is not -24%); blaming applications because it is the first stage; ignoring that a policy change may be intended.

### Q49 ⭐⭐ 🟡 Payroll cost rose from ₹10 crore to ₹11.2 crore while headcount rose from 1,000 to 1,020. Compute the change in cost per head and list where you would look for the rise.
**Asked at:** commonly asked (no company-specific report found); a payroll flavour of cost-per-unit questions, which suits HR-analytics roles.
**What the interviewer is checking:** Whether you split a cost rise into "more people" and "more cost per person".
**Say this in the interview:** "Cost per head rose from about ₹1.00 lakh to ₹1.098 lakh, up 9.8%. Cost rose 12% but headcount only 2%, so most of the rise is a higher cost per person."
**Definition in plain words:** Cost per head = total payroll cost / headcount. (1 crore = 100 lakh. The question does not say if the figures are monthly or yearly; I treat them as one period.)
**Worked answer:**
1. Before: ₹10 crore / 1,000 = ₹1,00,000 per head.
2. After: ₹11.2 crore / 1,020 = ₹1,09,804 per head.
3. Change: +₹9,804, which is +9.8%.
4. Split the ₹1.2 crore rise: headcount effect = 20 x ₹1,00,000 = ₹20 lakh; per-head effect = 1,020 x ₹9,804 = ₹1 crore. Total ₹1.2 crore.
**Result:** Cost per head +9.8%; about ₹1 crore of the ₹1.2 crore rise (83%) comes from a higher cost per head.
**Check:** 1.12 / 1.02 = 1.098. Matches.
**Caveats:** Use average headcount over the period if people joined mid-way. Where to look for the per-head rise: annual increments and promotions; a change in the mix (more senior hires, fewer freshers); bonus, incentive or arrear payouts; overtime; benefits and statutory costs (PF, insurance); one-time items like notice-period buyouts or joining bonuses; attrition replacements hired at higher salaries.
**Likely follow-ups:** (1) Is 9.8% normal? Compare with the planned increment budget and market pay rise (benchmark unverified). (2) How would you find the cause? Break payroll by pay component and by grade.
**Common mistakes / traps:** Comparing 12% with 2% and stopping there; counting one-off items as a run-rate rise; mixing monthly and annual figures.

### Q50 ⭐⭐ 🟡 Monday attendance at a 500-agent call centre fell from 94% to 86%. How many more agents are absent on Mondays, and how do you find the cause?
**Asked at:** commonly asked (no company-specific report found); an HR flavour of the "drop on one weekday" case.
**What the interviewer is checking:** Whether you turn percentages into people and then diagnose by cuts.
**Say this in the interview:** "Absence went from 6% to 14%, so from 30 to 70 agents: 40 more absent. Then I would cut by who, when and why before guessing."
**Clarify first:** Is attendance measured the same way (scheduled agents only)? Planned leave counted? Since when did it fall?
**Structure:** Planned (approved leave, long weekend, shift swap) versus unplanned (sick, no-show); data issue (biometric or roster change); real change (new shift pattern, a payday on Friday, low morale).
**What I would check, in order:**
- Numbers: 500 x 6% = 30 absent before; 500 x 14% = 70 now; +40 agents (absence is 2.3 times higher; attendance fell 8 percentage points).
- Trend: is it every Monday or only the last few weeks? Compare with other weekdays.
- Cuts: team, supervisor, shift, tenure, new joiners, process or client, leave type.
- Pattern: Monday after a Friday payday; Monday after a festival; shift roster changed to give fewer weekends off.
- Check the attendance system for roster or sync errors.
**If the data shows...:** Concentrated in one team: look at the supervisor and workload. Mostly leave applied for in advance: policy or roster. Mostly no-shows among new joiners: onboarding and early attrition risk. Across everyone, starting on one date: process or data change.
**Recommendation:** Act on the biggest cut first, for example the roster, then track Monday absence weekly against the 6% baseline.
**Likely follow-ups:** (1) What is the cost? 40 absent agents is 8% of capacity, so check service level that day. (2) Is it attrition? Check whether absent agents later resign.
**Common mistakes / traps:** Writing "8% more absent" (it is 8 percentage points, 40 people); one-day conclusion; ignoring planned leave.

### Q51 ⭐⭐ 🟡 The dashboard shows orders down 20% but the payment settlement report shows only 2% fewer paid orders. How do you reconcile the two?
**Asked at:** commonly asked (no company-specific report found); Meesho-type reports mention completed orders falling on an executive dashboard (unverified, search summary).
**What the interviewer is checking:** Whether you trust neither number blindly and find the definition or pipeline gap.
**Say this in the interview:** "A 20% versus 2% gap is too big to be noise. I would first align the definition, the date field and the time zone, then compare order IDs between the two sources."
**Clarify first:** What does the dashboard call an order (placed, confirmed, delivered)? Which date does each report use (order date or settlement date)? Same period and time zone?
**Structure:** Definition difference; timing difference; pipeline loss; real change.
**What I would check, in order:**
- Definitions: dashboard may count "placed"; settlement counts "paid". If failed or cancelled orders rose, the two diverge.
- Dates: settlement lags by one to three days, so it reports earlier orders.
- Pipeline: missing events (for example a tracking bug in a new app version) would shrink the dashboard but not payments, which come from the bank side.
- Match order IDs: a join of the two lists gives orders in both, only in dashboard, only in settlement.
**If the data shows...:** Many settled orders with no dashboard event: tracking or pipeline bug, and the real drop is near 2%. Dashboard orders exist but payments do not: payment failures; real revenue is fine only if retries succeed. IDs match and both drop: then the real drop is real and the 2% is a timing lag.
**Numeric illustration (assumed):** Dashboard 10,000 to 8,000 (-20%); settled 9,000 to 8,820 (-2%). The 1,800-order gap in the second period would be the lost events.
**Recommendation:** Do not act on the 20% until the ID-level reconciliation is done; fix the source and set an automated daily check between the two.
**Likely follow-ups:** (1) Which is the "truth"? Money from the bank is usually the stronger record. (2) How often to reconcile? Daily.
**Common mistakes / traps:** Picking the number you like; ignoring settlement lag; comparing different date fields.

### Q52 ⭐⭐ 🟡 Mobile-phone page views were flat at 1,00,000 per day and the in-stock conversion rate is 3%. Stock availability fell from 95% to 70%. By what percent do you expect orders to change?
**Asked at:** commonly asked (no company-specific report found); stock-availability effects on conversion are a standard e-commerce case.
**What the interviewer is checking:** Whether you apply availability to the funnel and state your assumption on out-of-stock views.
**Say this in the interview:** "Orders should fall about 26%, from roughly 2,850 to 2,100 a day, because only in-stock page views can convert."
**Definition in plain words:** Expected orders = page views x share in stock x conversion rate when in stock. I assume out-of-stock views convert at zero.
**Worked answer:**
1. Before: 1,00,000 x 0.95 x 0.03 = 2,850 orders.
2. After: 1,00,000 x 0.70 x 0.03 = 2,100 orders.
3. Change: 2,100 / 2,850 - 1 = -26.3% (750 fewer orders a day).
**Result:** About -26%, with a sensible range of -15% to -26%: shoppers who find a sold-out phone may switch to another model, so the real fall is usually smaller than the full 26%.
**Check:** 70 / 95 = 0.737, so -26.3%. Same.
**Caveats:** The 3% is assumed to apply to in-stock views only; if 3% were already blended with availability, the numbers change. Stock-outs also bias traffic (people stop visiting), so views may not stay flat.
**Likely follow-ups:** (1) How do you reduce the loss? Show alternatives and "notify me". (2) Is availability by product or overall? Weight by page views, since popular phones matter most.
**Common mistakes / traps:** Applying -25 percentage points as -25% (it is 95 to 70, a 26.3% relative change); forgetting the substitution effect.

### Q53 ⭐⭐ 🟡 Average monthly sales are 100 (units in lakh) and November's seasonal index is 0.85. November actual sales were 90. Is this a drop or not?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you compare with a seasonal expectation, not with the plain average.
**Say this in the interview:** "November normally runs at 85% of the average month, so 85 lakh units was expected. At 90 lakh we are about 5.9% above expectation: not a drop."
**Definition in plain words:** A seasonal index says how a month usually compares with an average month (0.85 = 15% below average). Expected = average x index.
**Worked answer:**
1. Expected November sales: 100 x 0.85 = 85 lakh units.
2. Actual 90 lakh minus expected 85 = +5 lakh units.
3. 90 / 85 - 1 = +5.9% versus expectation. Versus the raw average, 90 / 100 - 1 = -10%, which would mislead.
**Result:** Not a drop; about 5.9% above the seasonal expectation. The seasonally adjusted figure is 90 / 0.85 = 105.9.
**Check:** 105.9 is above the average of 100, so adjusted demand is healthy.
**Caveats:** The index is assumed to come from several past years; check it is stable, and whether trend growth is already in the 100. Also compare with last November.
**Likely follow-ups:** (1) What if the index is based on one year? Weak; use more. (2) What about a trend? Add it (see Q67).
**Common mistakes / traps:** Comparing a festive or slow month with the yearly average; using the index the wrong way round (dividing when you should multiply to get expected).

### Q54 ⭐⭐ 🟡 A company raised its price by 10% and volume fell by 8%. Did revenue fall? Compute the change and say what else you would check before blaming the price rise.
**Asked at:** commonly asked (no company-specific report found); price x volume decomposition is the standard revenue-decline structure on case prep sites.
**What the interviewer is checking:** Whether you compute revenue = price x volume correctly and avoid a one-cause conclusion.
**Say this in the interview:** "Revenue = price x volume, so 1.10 x 0.92 = 1.012. Revenue rose 1.2%; it did not fall."
**Definition in plain words:** Revenue = price per unit x units sold. Price elasticity (how much volume reacts to price) here is -8% / +10% = -0.8, so demand is fairly inelastic.
**Worked answer:**
1. Example: price 100, volume 1,000 units: revenue 1,00,000.
2. New: price 110, volume 920: revenue 1,01,200.
3. Change: +1.2%.
4. Profit check (assumed unit cost 60): before 40 x 1,000 = 40,000; after 50 x 920 = 46,000, so profit +15%.
**Result:** Revenue +1.2%; profit likely up more, because costs fall with volume.
**Check:** The percentage result does not depend on the starting price or volume.
**Caveats:** Before blaming the price, check: did volume fall because of price or because of season, a competitor, stock-outs or lower marketing? Which customers left (high or low value)? Did the mix shift to cheaper variants? Is the fall continuing (a one-time shock or a trend)? Compare with an area where price did not change.
**Likely follow-ups:** (1) At what volume fall does revenue stay flat? 1/1.10 = 0.909, so a 9.1% fall. (2) Does it hurt long term? Possibly, through lost loyalty.
**Common mistakes / traps:** Subtracting 10 - 8 and getting +2% (close here, but wrong in general); ignoring margin; blaming price without a comparison group.

### Q55 ⭐⭐ 🟡 A promo code accounted for 40% of orders and the promo ended. Total orders fell 20% and non-promo orders were unchanged. What share of promo orders disappeared?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you set a base of 100 and split cleanly.
**Say this in the interview:** "With 100 orders as the base: 40 promo, 60 other. Total fell to 80 and the other 60 are unchanged, so 20 of the 40 promo orders disappeared: half."
**Definition in plain words:** Share lost = promo orders lost / promo orders before.
**Worked answer:**
1. Base 100: promo 40, non-promo 60.
2. After: total 80; non-promo still 60; so the remaining 20 came from the former promo group.
3. Lost = 40 - 20 = 20 orders. Share = 20 / 40 = 50%.
**Result:** 50% of promo-driven orders disappeared; half stayed and now pay full price.
**Check:** 60 + 20 = 80 = a 20% fall. Matches.
**Caveats:** A premise problem: if the promo truly ended, any remaining order would be a non-promo order, so "non-promo unchanged" cannot hold literally. I read it as "orders from customers who did not use promos are unchanged", and the 20 retained orders are former promo users now paying full price. Then check what the lost promo orders were worth: they may have been unprofitable, so lower orders can still mean higher profit.
**Likely follow-ups:** (1) Is it a failure? Compare margin per order with and without the discount. (2) Will they return? Test a smaller discount.
**Common mistakes / traps:** Answering 20% (mixing total with promo base); ignoring margin; treating all promo orders as incremental.

### Q56 ⭐⭐ 🟡 A restaurant app's average rating fell from 4.4 to 4.1 two weeks before orders fell. How would you test whether the rating drop led the order drop?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know that "came first" is only a clue, and you can test it with data.
**Say this in the interview:** "A 0.3 drop is about 6.8%. I would check whether the order drop is larger where ratings fell more, and whether the timing holds at restaurant level, not just in the average."
**Clarify first:** Is the rating app-wide or by restaurant? Is it the average of new ratings or of all history? What caused ratings to fall (food quality, delivery, an app change)?
**Structure:** Rating drop leads to fewer orders; versus a common cause (late delivery lowers both ratings and orders); versus orders fall first (reverse).
**What I would check, in order:**
- Plot weekly rating and orders on one timeline; compare the lag (rating first by two weeks).
- Restaurant-level: restaurants whose rating fell most vs those whose rating was stable; compare their order trend (difference between the two groups).
- Search to order conversion on restaurants after their rating crossed a visible bar (for example 4.0 or 4.2); customers often filter on a threshold.
- Check the reasons in low-star reviews: delivery vs food.
**If the data shows...:** Big drops only in restaurants that fell below a filter threshold: rating is a likely cause. Ratings and orders fall because of delivery delays: delivery is the root cause. Orders fell first: reverse direction.
**Recommendation:** Fix the cause in the review text, then track whether rating and orders recover together.
**Likely follow-ups:** (1) Can you prove it? Only with an experiment or a natural quasi-experiment, such as the threshold cut-off. (2) Is 2 weeks enough? Depends on the order cycle.
**Common mistakes / traps:** Using only the app-wide average; ignoring the common cause; treating timing as proof.

### Q57 ⭐⭐ 🟡 How do you test whether a competitor's launch caused your decline using only your own data?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can find indirect evidence of an external cause and are honest about its limits.
**Say this in the interview:** "I cannot see the competitor's data, but I can look for a footprint: a drop that starts at the launch date, is larger where they launched, and is mostly lost-customer behaviour, not a change in our own metrics."
**Clarify first:** Where and when did the competitor launch? Did we change anything at that time?
**Structure:** Internal causes first (release, price, stock); then external-footprint checks.
**What I would check, in order:**
- Timing: does the decline begin at the launch date, as a step, not a slow slide?
- Geography: compare launch cities with others (difference-in-differences, see Q63).
- Who left: customers who used us weekly and stopped, rather than new customers failing to arrive; the lost customers' last orders.
- Our own funnel: if conversion and delivery time are stable but new-user installs and returning users fall, the cause is outside.
- Competitor's offers: any discount or ad spike on the same dates (outside data, optional).
**If the data shows...:** Drop only in launch cities, from launch week, with stable internal metrics: strong support. Drop everywhere, with a release the same day: internal.
**Recommendation:** Respond only in the cities affected (offer, loyalty); keep an unaffected city as a comparison.
**Likely follow-ups:** (1) How certain are you? Not certain without a comparison group. (2) What outside data helps? App downloads, search trends (unverified sources).
**Common mistakes / traps:** Blaming the competitor before ruling out internal changes; no comparison region; ignoring seasonality.

### Q58 ⭐⭐ 🟡 Orders fell 20% on Android after app release 7.3 while iOS was flat. Android is 60% of 10,000 orders. What is the overall drop and what is your decision rule on rollback?
**Asked at:** commonly asked (no company-specific report found); app-release cases appear in product-analytics rounds (unverified).
**What the interviewer is checking:** Whether you size the drop and give a clear, evidence-based rollback rule.
**Say this in the interview:** "Android is 6,000 orders; a 20% fall is 1,200 orders, so the overall drop is 12%. I would roll back if the drop is clearly beyond normal variation, starts at the release, and is specific to the new version."
**Clarify first:** Is the release fully rolled out or staged (a share of users)? Are the drops in users on 7.3 only? Any crash spike?
**Structure:** Release effect versus coincidence (a sale, a holiday, an outage).
**What I would check, in order:**
- Numbers: Android 10,000 x 60% = 6,000; -20% = -1,200; Android becomes 4,800; total 8,800; overall -12%.
- Within Android, compare users on 7.3 with users still on the older version on the same days; if only 7.3 users fell, the release is the cause.
- Funnel steps for 7.3: crashes, checkout errors, payment button taps.
- Timing: did the drop start at the release time?
**Decision rule (my proposal):** Roll back, or pause the rollout, when (1) the 7.3 group is down well beyond its normal daily swing (for example beyond the usual range of past weeks), (2) the old-version Android group is not, and (3) the funnel shows a specific broken step. If only (1) holds, hold the rollout and investigate; fix forward if a quick patch exists.
**Recommendation:** Pause staged rollout today; each day of delay costs about 1,200 orders.
**Likely follow-ups:** (1) iOS flat helps? Yes, as a control. (2) What if a sale ran only on iOS? Then check promotions by platform.
**Common mistakes / traps:** Reporting 20% as the overall drop; comparing platforms without checking user mix; rolling back without comparing old and new version users.

### Q59 ⭐⭐ 🟡 The last two days show orders 20% lower than usual, but the data pipeline has late-arriving events. How do you detect and handle this?
**Asked at:** commonly asked (no company-specific report found); "validate the drop is real" is the first step in every drop-case guide seen (unverified).
**What the interviewer is checking:** Whether you know recent data can be incomplete and can test for it.
**Say this in the interview:** "The most recent days are often undercounted because events arrive late. I would compare how complete the same recent days looked in past weeks before calling it a drop."
**Clarify first:** Which source feeds the dashboard, and what is its normal delay? Is the order status from the app events or the order database?
**Structure:** Data lag (artefact) versus a real drop.
**What I would check, in order:**
- Completeness curve: for past days, how much of the final count was visible after 1 day, 2 days, 3 days? If day-1 data usually shows 80%, then 80 orders versus a normal 100 is not a drop (illustrative).
- Compare with the source system (the order database or payments), which has no lag.
- Check event timestamp versus load timestamp; a growing gap signals delay.
- Wait and re-run: do the two days refill to normal after 48 hours?
**If the data shows...:** Counts rise to normal on re-run: artefact. Counts stay low and the source database agrees: real drop.
**Recommendation:** On dashboards, mark the last N days as provisional, show an expected-completeness line, and alert only on complete days or after adjusting for the lag.
**Likely follow-ups:** (1) How to handle it? Use event time not load time, and re-state numbers later. (2) Could the lag itself be a symptom? Yes, an outage.
**Common mistakes / traps:** Escalating a "20% drop" from incomplete data; comparing partial days with full days; never revisiting the number.

### Q60 ⭐⭐ 🟡 The January cohort (10,000 users) has 30% active in month 1 and the March cohort (12,000 users) has 22%. How many fewer users are active than if March matched January, and what does this suggest about the sales drop?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you convert retention rates into users and link them to sales.
**Say this in the interview:** "If March matched January's 30%, it would have 3,600 active users; it has 2,640. That is 960 fewer. The newer cohort is bigger but weaker, so the sales drop looks like a retention and user-quality issue."
**Definition in plain words:** A cohort is a group of users who joined in the same month. Month-1 retention is the share still active one month later.
**Worked answer:**
1. January: 10,000 x 30% = 3,000 active.
2. March actual: 12,000 x 22% = 2,640 active.
3. March at January's rate: 12,000 x 30% = 3,600.
4. Gap: 3,600 - 2,640 = 960 fewer (26.7% below what it would be).
**Result:** 960 fewer active users. March has 20% more signups but 12% fewer active users than January (2,640 vs 3,000).
**Check:** 12,000 x 8 percentage points = 960. Same.
**Caveats:** Check the cohorts are compared at the same age and that "active" is defined the same way. Look at why quality fell: a new marketing channel with low intent, discount-driven signups, poorer onboarding, or an app issue. This explains part of the drop only; it does not prove the sales drop is all retention.
**Likely follow-ups:** (1) What next? Retention by acquisition channel. (2) Can you value it? Multiply 960 users by average monthly orders and order value.
**Common mistakes / traps:** Comparing a young cohort with an old one; celebrating bigger signups; assuming the drop is all from new users, since older cohorts also matter.

### Q61 ⭐⭐ 🟡 Many partner restaurants take their weekly off on Tuesday. Active restaurants on Tuesday fell from 1,000 to 800 and orders per active restaurant stayed at 10. By what percent did Tuesday orders change and how do you verify this hypothesis?
**Asked at:** commonly asked (no company-specific report found); the Tuesday-orders-fell wording is the brief's own example, and no source found it verbatim.
**What the interviewer is checking:** Whether you tie the drop to supply and can verify it, not just compute it.
**Say this in the interview:** "Orders = active restaurants x orders per restaurant. 1,000 x 10 = 10,000 falls to 800 x 10 = 8,000, so Tuesday orders fell 20%, entirely from fewer restaurants."
**Clarify first:** What counts as an active restaurant (accepted at least one order, or open on the app)? Did the number of Tuesday offs change over time?
**Structure:** Orders = active restaurants x orders per active restaurant. Here only the first factor moved.
**What I would check, in order:**
- Numbers: 10,000 to 8,000 = -20% (2,000 orders lost).
- List the 200 restaurants that were active before but not now: are they the same ones every Tuesday, and do they carry a weekly-off flag?
- Compare other weekdays: if only Tuesday shows fewer active restaurants, the weekly off is a good explanation.
- Check customers: since orders per restaurant stayed at 10, demand did not move to remaining restaurants; look at search results showing fewer options or those customers' orders disappearing.
- Check whether the offs are new (policy change, a festival, a restaurant association day).
**If the data shows...:** The same 200 restaurants closed every Tuesday for weeks: a standing pattern, so compare with last year and plan supply for Tuesday (incentives to stay open). Restaurants closed only this week: a one-off event.
**Recommendation:** Incentivise top restaurants to open on Tuesdays; track active restaurants per weekday daily.
**Likely follow-ups:** (1) Why did demand not move to others? Possibly the closed restaurants were popular or in dense areas. (2) Effect on revenue? Orders x average order value.
**Common mistakes / traps:** Treating a 20% order drop as a demand problem; counting restaurants listed instead of those actually active.

### Q62 ⭐⭐ 🔴 Segment A and B conversion are below. Both segments improved but overall conversion fell. Compute the rate effect and the mix effect.
| Segment | Users wk 1 | Conv wk 1 | Users wk 2 | Conv wk 2 |
|---|---|---|---|---|
| A | 6,000 | 5.0% | 8,000 | 5.5% |
| B | 4,000 | 10.0% | 2,000 | 11.0% |
**Asked at:** commonly asked (no company-specific report found); mix-shift and Simpson's paradox topics appear on analytics blogs (unverified).
**What the interviewer is checking:** Whether you can split a change into "rates changed" and "who we have changed".
**Say this in the interview:** "Overall conversion fell from 7.0% to 6.6%. Each segment improved, but traffic shifted toward the low-converting segment A. The rate effect is about +0.7 points and the mix effect about -1.1 points."
**Definition in plain words:** Conversion = buyers / users. Rate effect: the change if the segment mix stayed as in week 1 but the segment rates moved. Mix effect: the rest, caused by the share of users shifting between segments. (Simpson's paradox: every group improves yet the total worsens.)
**Worked answer:**
1. Week 1: A 6,000 x 5% = 300; B 4,000 x 10% = 400; total 700 / 10,000 = 7.0%.
2. Week 2: A 8,000 x 5.5% = 440; B 2,000 x 11% = 220; total 660 / 10,000 = 6.6%.
3. Mix: A share 60% to 80%; B share 40% to 20%.
4. Rate effect at week 1 mix: 0.6 x 5.5% + 0.4 x 11% = 7.7%; 7.7 - 7.0 = +0.7 points.
5. Mix effect (the remainder): 6.6 - 7.7 = -1.1 points.
**Result:** Total -0.4 points (7.0% to 6.6%) = rate +0.7, mix -1.1.
**Check:** Other order of calculation: mix first at week 1 rates gives 0.8 x 5% + 0.2 x 10% = 6.0%, so mix -1.0, rate +0.6. The split depends on order; averaging gives rate +0.65 and mix -1.05. The conclusion (mix dominates) is the same. Total is -0.4 either way.
**Caveats:** Users are 10,000 in both weeks, so volume is not the issue. Ask why more traffic is A: a new campaign that attracts low-intent users. Fix with segment-wise reporting.
**Likely follow-ups:** (1) Is this a problem? Not if A users are cheap and profitable. (2) What if the segments were uneven in size? Use user-share weights as above.
**Common mistakes / traps:** Concluding the product got worse; reporting only the total; forgetting that rate and mix split is order dependent.

### Q63 ⭐⭐ 🔴 Region T had a price test and Region C did not. Orders are below. Estimate the effect of the test using a difference-in-differences and say what assumption you rely on.
| Region | Before | After |
|---|---|---|
| T (test) | 10,000 | 8,500 |
| C (control) | 10,000 | 9,500 |
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you use a control region to remove the background trend and know the key assumption.
**Say this in the interview:** "T fell 15%, C fell 5% for other reasons, so the price test's effect is about -10 percentage points, roughly 1,000 orders."
**Definition in plain words:** Difference-in-differences (DiD) = change in the test group minus change in the control group. The control shows what would have happened to the test group without the test.
**Worked answer:**
1. T change: 8,500 - 10,000 = -1,500 (-15%).
2. C change: 9,500 - 10,000 = -500 (-5%).
3. DiD: -1,500 - (-500) = -1,000 orders; as a percent, -15% - (-5%) = -10 points.
4. Compared with the expected T of 9,500, the effect is 8,500 / 9,500 - 1 = -10.5%.
**Result:** Price test effect is about -1,000 orders, -10% to -10.5%.
**Check:** Expected T without the test = 10,000 - 500 = 9,500; actual 8,500; gap 1,000.
**Caveats:** Key assumption: parallel trends, meaning T would have moved like C had there been no test. Weak if regions differ in season, income, competitors, or if the regions started with different trends. Check several pre-test weeks. Also check spillover (customers crossing regions) and the revenue and margin effect, not just orders.
**Likely follow-ups:** (1) How would you check the assumption? Plot weeks before the test for both regions. (2) Is the effect significant? Need more data points and a confidence interval.
**Common mistakes / traps:** Using only T before and after; picking a control that differs; mixing percentage points and percent.

### Q64 ⭐⭐ 🔴 How would you design monitoring so that a Tuesday-type drop is caught within a day next time?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can turn a one-off diagnosis into a repeatable alert with sensible thresholds.
**Say this in the interview:** "I would compare each day with the same weekday in past weeks, set an expected band, alert when it is breached and break the alert down automatically by city, platform and restaurant status."
**Explain simply:**
- Compare like with like: Tuesday against previous Tuesdays, not Tuesday against Monday.
- Expected band: mean and spread of the last 8 same-weekdays. Example (assumed): past Tuesdays average 10,000 with a standard deviation (typical swing) of about 200; the alert line at the mean minus 3 swings is about 9,400, so 8,000 would trigger immediately (nearly 10 swings below).
- Use hourly checks as well, so a drop is seen within hours; adjust for data lag (see Q59).
- Alert on drivers too: active restaurants, delivery time, app errors, payment success, not just orders.
- Automatic split: every alert shows which city, platform, app version and category is responsible.
- Reduce noise: minimum size, holidays calendar, and a weekly review of false alarms.
**Short worked example:** A Tuesday alert says: orders -20%; active restaurants -20% (800 vs 1,000); everything else is normal. The cause is visible on day one.
**Practice step:** In Excel, take 8 past same-weekday values, compute average and STDEV, and flag a new value below average minus 3 x STDEV.
**Likely follow-ups:** (1) How to avoid too many alerts? Wider bands for noisy segments and a minimum volume. (2) Who owns the alert? A named owner and a runbook.
**Common mistakes / traps:** Comparing with the overall average; a fixed threshold ignoring weekday patterns; no owner; no drill-down.

### Q65 ⭐⭐ 🔴 Sales fell 20% after a loyalty programme change. How do you isolate its causal effect without a randomised experiment?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know observational methods and their assumptions.
**Say this in the interview:** "Without a randomised test I need a credible comparison group: customers or regions that were not affected, or the same customers before and after against a forecast. Each method relies on an assumption I would state."
**Explain simply:**
- Difference-in-differences: compare affected and unaffected groups before and after (see Q63); needs parallel trends.
- Staggered rollout: if the change reached regions at different dates, compare treated and not-yet-treated regions.
- Interrupted time series: model the trend and seasonality before the change, project it forward, and read the gap after the change as the effect; needs no other change at that date.
- Matched groups: compare customers who lost benefits with similar customers who did not (similar order history, city, tenure).
- Synthetic control: build a "control" as a weighted mix of unaffected regions that tracked us before the change.
- Check placebo tests: pretend the change happened earlier or in an unaffected group; no effect should appear.
**Short worked example:** Affected group 10,000 to 8,000 (-20%); similar unaffected group 10,000 to 9,500 (-5%). Effect is about -15 points; the other 5 points is background.
**Practice step:** Write which single assumption each method needs.
**Likely follow-ups:** (1) Which is best? Staggered rollout or a hold-out group. (2) Can you be sure? No, only more or less credible.
**Common mistakes / traps:** Attributing the whole 20% to the programme; before and after only; ignoring that customers chose whether to be affected.

### Q66 ⭐⭐ 🔴 Both orders per user and active restaurants fell on a two-sided marketplace. How do you tell which side fell first?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand a two-sided marketplace (buyers and sellers each need the other) and use timing and leading indicators.
**Say this in the interview:** "I would line up demand-side and supply-side indicators day by day and see which turned first, then check whether the drop reached the other side through a clear mechanism."
**Clarify first:** Which restaurants count as active? Are orders per user falling everywhere or only in some areas?
**Structure:** Orders = active users x orders per user = active restaurants x orders per restaurant. Supply fall: restaurants leave, close early, or get paused. Demand fall: fewer users or less frequent orders. Each can cause the other.
**What I would check, in order:**
- Timeline: first date each metric breaks its normal band; leader is the candidate.
- Early demand signals: app opens, search and menu views per user, before order.
- Early supply signals: restaurants online hours, offline rate, menu items available, acceptance and cancellation rates.
- Mechanism: if restaurants went offline first, users see fewer options and search results empty, then orders fall. If users fell first, restaurants see fewer orders and reduce hours.
- By area: where supply fell first, does demand follow?
**If the data shows...:** Supply indicators move first, demand follows by days, only in the affected areas: supply-led. Demand falls first with restaurants stable at first: demand-led, and restaurant activity falls after orders fall.
**Recommendation:** Tackle the first-moving side, then watch the other side for recovery.
**Likely follow-ups:** (1) Both together? Use a cross-correlation of daily series at lags. (2) What if simultaneous? Look for a common cause (outage, weather).
**Common mistakes / traps:** Using monthly averages (too coarse); not distinguishing listed from active; assuming the larger fall is the first.

### Q67 ⭐⭐ 🔴 How do you build an expected-value baseline with trend and seasonality so you can quantify the true shortfall in sales?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can say what "normal" would have been, then size the gap in numbers.
**Say this in the interview:** "Expected sales = underlying trend x seasonal index x known events. The shortfall is expected minus actual, with a range for normal noise."
**Explain simply:**
- Trend: the underlying level and growth, for example from a rolling 12-month average or a fitted line.
- Seasonality: the month or weekday pattern as an index (0.85 means 15% below average), from at least 2 to 3 years of history.
- Known events: festivals, sales, promos, holidays, stock-outs, adjusted or flagged.
- Uncertainty: past forecast errors give a band; only a gap outside the band is a real shortfall.
- Method steps: clean the history, remove past anomalies, build the baseline, test it on past months you already know, then apply.
- Excel: FORECAST.ETS, which handles trend and seasonality, or a simple trend line times the seasonal index.
**Short worked example (assumed):** Underlying monthly level 100 growing 4% a year gives about 104. November index 0.85, so expected is 104 x 0.85 = 88.4. Actual is 80. Shortfall 8.4, which is 9.5% of expected. If normal forecast error is plus or minus 3, the shortfall is real.
**Practice step:** Take 24 months of your own sales, compute each month's index as month / yearly average, and forecast the next month.
**Likely follow-ups:** (1) What about a new product? Short history; use similar products. (2) How do you test the baseline? Back-test on past months.
**Common mistakes / traps:** Comparing with last month only; ignoring the trend; including past anomalies in the history; giving a single number with no range.

### Q68 ⭐ 🟢 What is a fishbone (Ishikawa) diagram and how would you use it for falling orders?
**Asked at:** commonly asked (no company-specific report found); a classic root-cause tool named in many problem-solving guides.
**What the interviewer is checking:** Whether you know a structured brainstorming tool and turn it into testable hypotheses.
**Say this in the interview:** "A fishbone puts the problem at the head and groups possible causes into categories on the bones. I would use it to list ideas before testing each one with data."
**Explain simply:**
- The head of the fish is the problem: "orders fell 20%".
- Each bone is a category of causes. For an app: Product (app release, bugs, search), Price and promo, Supply (restaurants, stock, riders), Operations (delivery time, cancellations), Marketing and demand (traffic, channels), External (competitor, weather, holidays) and Data (tracking, pipeline).
- Under each bone, list specific causes, for example Supply: restaurants closed on Tuesday.
- Then turn each cause into a test and mark it confirmed or rejected.
**Short worked example:** Orders fell from 100 to 80. Under Supply: 200 of 1,000 restaurants closed (matches 20 orders lost). Under Product: release crash rate unchanged (rejected). A tick or cross on each bone makes the analysis visible.
**Practice step:** Draw one fishbone for "HR: attrition rose from 12% to 18%" with bones: pay, manager, workload, market, career growth, data.
**Likely follow-ups:** (1) Is it analysis? No, it is a brainstorming aid; data does the proving. (2) Alternative? A hypothesis (issue) tree.
**Common mistakes / traps:** Stopping at a nice picture; overlapping categories; listing causes without tests; ignoring data errors.

### Q69 ⭐ 🟢 Five causes explain a sales drop with contributions of 50, 25, 10, 8 and 7 units out of a 100-unit drop. Which causes would a Pareto approach fix first and what share do they cover?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you prioritise by impact using cumulative shares.
**Say this in the interview:** "The top two causes (50 and 25) cover 75% of the drop; adding the third (10) reaches 85%. I would fix those first."
**Definition in plain words:** The Pareto principle says a few causes usually explain most of the effect (often quoted as 80/20, a rule of thumb, not a law). Rank causes by size and add them up.
**Worked answer:**
1. Sort largest first: 50, 25, 10, 8, 7 (already sorted).
2. Cumulative: 50, 75, 85, 93, 100 units, which is 50%, 75%, 85%, 93%, 100% of the 100-unit drop.
3. The first two causes reach 75%, just short of 80%; the third crosses it at 85%.
**Result:** Fix the 50 and 25 causes first (75% of the drop); including the 10-unit cause covers 85%. The last two (8 and 7) add only 15% together.
**Check:** 50 + 25 + 10 + 8 + 7 = 100. Matches.
**Caveats:** Also weigh cost and ease: a small cause that is cheap to fix may go first, and a big cause that is unfixable (for example a regulation) may not. Causes should not overlap, or the shares double count.
**Likely follow-ups:** (1) What chart? A Pareto chart: bars sorted descending with a cumulative line. (2) Is 80/20 exact? No, only a guide.
**Common mistakes / traps:** Not sorting; ignoring effort and cost; double counting overlapping causes.

### Q70 ⭐ 🟢 What is a waterfall (bridge) chart, and what is the closing value of one starting at 100 with price +3, volume -18 and mix -5?
**Asked at:** commonly asked (no company-specific report found); price, volume and mix bridges are a standard way to present a revenue change (unverified for any company).
**What the interviewer is checking:** Whether you can explain the chart in plain words and do the add-and-subtract correctly.
**Say this in the interview:** "A waterfall starts at the opening value, shows each driver as a floating up or down bar, and ends at the closing value. Here 100 + 3 - 18 - 5 = 80."
**Explain simply:**
- A waterfall (bridge) chart is a bar chart where each bar hangs from the end of the previous one, so you see how a starting number turns into an ending number step by step. Rises are usually green, falls red.
- Here: start 100, price +3 gives 103, volume -18 gives 85, mix -5 gives 80. Closing value = 80, a 20% fall overall.
- Volume is the biggest driver (18 of the net 20 points); price partly cushioned the fall.
- The drivers must add up to the total change (+3 - 18 - 5 = -20). If they do not, a bar is missing.
**Short worked example:** In Excel, list start, each driver and the end in a column, then insert a Waterfall chart. In Power BI use the built-in Waterfall visual.
**Practice step:** Take any metric you know (monthly headcount) and bridge last month to this month using hires, exits and transfers.
**Likely follow-ups:** (1) What is mix? The shift between cheap and expensive items, or between segments. (2) Is order of bars important? Slightly, when drivers interact; state your convention.
**Common mistakes / traps:** Bars that do not reconcile to the end value; mixing percent and absolute units; too many tiny bars.

### Q71 ⭐ 🟢 Why is looking only at the average dangerous when you investigate a drop, and what do you look at instead?
**Asked at:** commonly asked (no company-specific report found); segment-first diagnosis is a recurring theme in metric-drop question banks (unverified).
**What the interviewer is checking:** Whether you know an average can hide a concentrated problem or a mix shift.
**Say this in the interview:** "An average blends everyone together, so one broken segment or a change in mix can vanish inside it. I look at the distribution and the segments: median, percentiles, and the split by city, channel, device and customer type."
**Explain simply:**
- Average (mean) = total divided by count. It is pulled by extreme values and hides who is behind it.
- Example: average order value stays at Rs 250, but premium orders fell and small orders rose in equal measure. The average looks calm while the business changed.
- Look instead at: the median and 25th/75th percentiles, a histogram of order values, and the same metric by segment, compared with the same weekday last week.
- Also check the count behind each average; a segment with 20 orders is noise.
**Short worked example:** Average AOV Rs 250 in both weeks. Week 1: 50% orders at Rs 100, 50% at Rs 400. Week 2: 70% at Rs 100, 30% at Rs 600 gives Rs 250 too, yet the mix is different.
**Practice step:** Take salary data for a team and compare the mean and median; note which one an outlier moves.
**Likely follow-ups:** (1) Which is better, mean or median? Neither alone; show both. (2) What visual? Histogram or box plot.
**Common mistakes / traps:** Reporting only the mean; comparing averages with very different group sizes; ignoring outliers without checking if they are real.

### Q72 ⭐ 🟢 A 28-day month had total sales of 280 and a 31-day month had 310. Is there a drop on a per-day basis?
**Asked at:** commonly asked (no company-specific report found); calendar-length effects are a gap-fill question, not seen in a company report (unverified).
**What the interviewer is checking:** Whether you normalise for unequal period lengths before calling something a drop.
**Say this in the interview:** "Divide each by its number of days: 280 / 28 = 10 a day and 310 / 31 = 10 a day. There is no per-day drop; the headline gap is purely calendar."
**Definition in plain words:** Per-day sales = total sales divided by days in the period.
**Worked answer:** Month A: 280 / 28 = 10.0 per day. Month B: 310 / 31 = 10.0 per day.
**Result:** Both are 10 per day, so the change per day is 0%. The total rose 10.7% only because the month has 3 more days.
**Check:** 10 x 31 = 310 and 10 x 28 = 280, so both totals are fully explained by length.
**Caveats:** Weekday mix also matters (a month with 5 weekends differs from one with 4); for sharper comparison use sales per trading day or same-weekday averages, and use "per working day" for B2B data.
**Likely follow-ups:** (1) What if the month has a holiday? Normalise per open day. (2) Which is better, per day or per week? Per week removes weekday mix.
**Common mistakes / traps:** Comparing raw monthly totals; forgetting leap-year February; dividing by calendar days when the store was shut some days.

### Q73 ⭐ 🟢 What is anomaly detection and when does a static threshold fail for orders data?
**Asked at:** commonly asked (no company-specific report found); monitoring and alerting appears in stronger analytics rounds (unverified).
**What the interviewer is checking:** Whether you understand that orders have rhythms (hour, weekday, season) a single fixed line ignores.
**Say this in the interview:** "Anomaly detection flags points that are unusual compared with what we expect. A static threshold fails because orders have daily, weekly and seasonal patterns, so a fixed line either fires every Sunday or misses a real dip on a busy day."
**Explain simply:**
- Anomaly = a value far from what normal behaviour predicts. Method: build an expected value (same hour, same weekday, recent weeks), measure normal spread (standard deviation), alert when the gap is large (say more than 3 standard deviations).
- Static rule "alert if orders below 700": weekday orders are 1,000, Sunday normal is 600, so you get a false alarm every Sunday. A real fall from 1,000 to 750 on Wednesday (25% drop) is missed.
- Failures also come from growth trends, festivals, promotions and new cities that shift the baseline.
**Short worked example:** Expected Wednesday 1,000 with standard deviation 25. A value of 750 is 10 standard deviations away, a clear anomaly, though the static line did not fire.
**Practice step:** Plot four weeks of hourly orders and mark the same hour on each weekday; notice the pattern a fixed line ignores.
**Likely follow-ups:** (1) What would you use instead? Seasonal baseline or rolling percent-of-expected. (2) Too many alerts? Raise the band and add a minimum size.
**Common mistakes / traps:** One threshold for all days; ignoring trend; alerting on tiny volumes.

### Q74 ⭐ 🟡 A payment-gateway outage lasted two hours in a period when normal orders are 500 per hour. During the outage only 40% of normal orders went through. Estimate lost orders and say how you would separate lost from delayed orders.
**Asked at:** commonly asked (no company-specific report found); outage-impact sizing is a plausible case variant (unverified).
**What the interviewer is checking:** Whether you size the gap simply and know that missing orders are not all permanently lost.
**Say this in the interview:** "Expected 2 x 500 = 1,000 orders; only 40% went through, so 400 completed and 600 are missing. Some of those 600 come back later, so I measure the catch-up before calling them lost."
**Definition in plain words:** Missing orders = expected orders - actual orders during the outage. Lost orders = missing orders that never come back.
**Worked answer:**
1. Expected: 500 x 2 hours = 1,000.
2. Actual: 40% x 1,000 = 400.
3. Missing = 1,000 - 400 = 600 (that is 300 per hour, 60% of normal).
4. Separate lost from delayed: look at the next 24 to 48 hours. If orders rise above normal, the excess is delayed demand. Example: if 200 extra orders appear afterwards, delayed = 200 and lost = 600 - 200 = 400. (The 200 is illustrative, not a given.)
**Result:** 600 orders missing; lost orders lie between 0 and 600 until catch-up is measured; at the illustrative 200 catch-up, 400 are lost.
**Check:** Also compare users who tried and failed with whether they ordered later (same user, within 24 hours); that is the cleanest test.
**Caveats:** Assumes flat 500 an hour (lunch and dinner peaks change this); some users switch to a competitor.
**Likely follow-ups:** (1) Revenue lost? Lost orders x AOV. (2) How to prevent? Fallback payment gateway and alerts.
**Common mistakes / traps:** Counting all missing orders as lost; applying 40% to the wrong base; ignoring failed-payment logs.

### Q75 ⭐ 🟡 How can timezone or daylight-saving handling create a fake 'Tuesday drop' in an events table?
**Asked at:** commonly asked (no company-specific report found); a data-artefact gap-fill, not seen in a company report (unverified).
**What the interviewer is checking:** Whether you check how timestamps are stored and cut into days before trusting a weekday pattern.
**Say this in the interview:** "If events are stored in UTC but the business day is IST, the daily cut is shifted by 5 hours 30 minutes, so some Tuesday orders land on Monday or Wednesday. A rule change in that handling looks like a drop."
**Explain simply:**
- UTC is the world reference time; IST is 5 hours 30 minutes ahead. A Tuesday in IST starts at 6:30 pm UTC Monday.
- Grouping by the UTC date puts IST Tuesday morning orders (the first 5.5 hours) into Monday. If the dashboard moved from UTC to IST, or a query truncates dates differently, Tuesday totals shift without any real change.
- Daylight saving (clocks moving by an hour) does not exist in India but does for UK/US data; on the change day a day has 23 or 25 hours, so counts look off by about 4%.
- Check: compare hourly counts for the day, and run the same query with an explicit conversion to IST.
**Short worked example:** If 8% of Tuesday orders come before 5:30 am IST and the pipeline begins to bucket those in UTC, Tuesday appears about 8% lower and Monday higher.
**Practice step:** Write the query with the timezone made explicit before grouping.
**Likely follow-ups:** (1) What would give it away? Another day rising by the same amount. (2) Fix? Store UTC, report in IST.
**Common mistakes / traps:** Not knowing the stored timezone; mixing local and UTC columns; ignoring DST in global data.

### Q76 ⭐ 🟡 How do bots or fraud filtering changes make orders or sessions look like they dropped?
**Asked at:** commonly asked (no company-specific report found); bot and fraud artefacts are a gap-fill, not seen in a company report (unverified).
**What the interviewer is checking:** Whether you separate a change in measurement from a change in behaviour.
**Say this in the interview:** "If a stricter bot or fraud filter starts removing traffic or orders, the reported number falls although real customers behaved the same. I would check what changed in the filter and compare the filtered and unfiltered series."
**Explain simply:**
- Reported metrics often exclude bots, test accounts and suspected fraud. Tighten the rules and past-versus-present are no longer comparable.
- Example (illustrative): 10,000 sessions, of which 1,500 were bots now filtered. Reported sessions drop 15% to 8,500 with no loss of real users.
- The reverse also happens: bots inflated earlier numbers, so a clean-up looks like a drop.
- Checks: ask the data/fraud team for the release date of the filter; plot the raw (unfiltered) count; see if the drop starts exactly that day and affects one traffic source or user agent; check whether paying customers and revenue moved (real demand shows there).
**Practice step:** Ask: did revenue drop as much as sessions? If not, suspect measurement.
**Likely follow-ups:** (1) What to report? Restated history using the new rule. (2) How to prevent confusion? Keep a change log.
**Common mistakes / traps:** Treating the filtered number as raw truth; not restating history; blaming marketing first.

### Q77 ⭐ 🟡 What is Simpson's paradox and how can it show up when you slice a falling metric by segment?
**Asked at:** commonly asked (no company-specific report found); mix-shift and Simpson's paradox appear in metric-change guides (Sequoia, Spotify glossary, unverified depth).
**What the interviewer is checking:** Whether you can show how a total moves opposite to its parts because the mix changed.
**Say this in the interview:** "Simpson's paradox is when every segment improves but the overall figure falls, because the weight of segments changed. So I always check mix before blaming performance."
**Explain simply:**
- Overall rate = weighted average of segment rates; the weights are each segment's share. If the share shifts towards a low-rate segment, the overall falls.
- Example: Week 1: mobile 800 visits at 4% converts 32; desktop 200 at 10% converts 20; overall 52 / 1,000 = 5.2%. Week 2: mobile 900 visits at 4.4% converts 39.6; desktop 100 at 10.5% converts 10.5; overall 50.1 / 1,000 = 5.0%.
- Both segments improved (4% to 4.4%, 10% to 10.5%), yet overall fell 0.2 points because the mix moved to mobile (80% to 90%).
- So the question becomes why the mix changed (a campaign driving mobile, desktop traffic lost), not "why conversion fell".
**Practice step:** Always split a falling rate into rate change inside segments and mix change between them.
**Likely follow-ups:** (1) Is the total wrong? No, just misleading. (2) Which view to trust? The segment view, with the mix explained.
**Common mistakes / traps:** Reading the total as a performance problem; slicing so finely that groups are tiny.

### Q78 ⭐ 🟡 Sales fell 20% but profit rose. Is that a problem, and how do you investigate?
**Asked at:** commonly asked (no company-specific report found); profit-versus-sales questions are standard in profitability cases (unverified).
**What the interviewer is checking:** Whether you look beyond revenue to margin and know the difference between good and bad profit growth.
**Say this in the interview:** "Not necessarily. Profit rising on lower sales means margin per rupee rose, perhaps from fewer discounts or cheaper costs. It is a problem if it is a short-term trade, like cutting marketing, that hurts future growth."
**Clarify first:** Is profit gross or net? Which period? Is the rise in absolute rupees or in margin?
**Structure:**
- Profit = sales x margin. Illustrative numbers: sales 100 at 10% margin = 10; sales 80 at 15% = 12, so profit rose 20% while sales fell 20%.
- Margin up from: lower discounts, mix towards higher-margin items, cheaper supply, lower delivery cost, one-off gains.
- Sales down from: dropped promotions, lost low-margin customers, stock-outs, weak demand.
**What I would check, in order:** Margin bridge (price, discount, cost, mix); customer count and repeat rate; marketing and one-off items; cohort of customers lost (were they unprofitable?).
**If the data shows...:** Discounts cut and lost customers were unprofitable: healthy, keep it. Margin from deferred spend (marketing, maintenance) or one-offs: unsustainable. Loyal high-value customers leaving: serious.
**Recommendation:** Track both profit and a growth indicator (active customers, repeat rate) for the next 2 to 3 months before declaring success.
**Likely follow-ups:** (1) Could it be good? Yes, shedding loss-making volume. (2) Which metric next? Contribution margin per order.
**Common mistakes / traps:** Celebrating profit without checking why; ignoring that costs were postponed.

### Q79 ⭐ 🟡 A tax or regulatory change is announced. How do you check whether it caused a drop in orders?
**Asked at:** commonly asked (no company-specific report found); external-cause checks are part of internal versus external drop analysis (unverified).
**What the interviewer is checking:** Whether you test timing and affected-versus-unaffected groups rather than assume.
**Say this in the interview:** "I check whether the drop starts at the effective date, hits exactly the affected products or regions, and spares unaffected ones. I compare these against a control group."
**Clarify first:** What exactly changed (rate, product, state), and from when? Was it announced early (people may buy ahead, then dip)?
**Structure:**
- Timing: did orders move at the announcement, the effective date, or neither?
- Exposure: affected versus unaffected categories or states.
- Mechanism: price change passed to customers? Compliance steps added at checkout?
**What I would check, in order:** Daily orders around the date; split affected versus unaffected; price and conversion at checkout; competitors under the same rule.
**If the data shows...:** Affected group drops, control flat, starts at the date: likely the rule. Everything drops everywhere: look elsewhere. Pre-announcement spike then dip: pull-forward, temporary.
**Recommendation:** Quantify as the difference between affected and unaffected groups' change (difference-in-differences) and recommend a price or process response.
**Likely follow-ups:** (1) Why a control group? To remove seasonality. (2) Pull-forward? Compare total over the combined weeks.
**Common mistakes / traps:** Assuming causation from timing; using no control group.

### Q80 ⭐ 🟡 A rainy week coincides with a drop in order count. How do you separate the weather effect from other causes?
**Asked at:** commonly asked (no company-specific report found); external-factor adjustments are in drop-diagnosis guides (unverified).
**What the interviewer is checking:** Whether you estimate weather's normal effect from history instead of guessing.
**Say this in the interview:** "I use past rainy weeks to estimate the usual effect, apply it to this week, and treat what remains as unexplained and worth investigating."
**Clarify first:** Is rain city-wide or local? Does the business expect weather to raise or lower orders (food delivery often rises in rain; delivery capacity may fall)?
**Structure:** Expected orders = normal orders x typical rain effect; unexplained = actual - expected.
**What I would check, in order:** Past rainy weeks versus dry weeks in the same city; rain only in some cities (compare rainy and dry cities the same week); rider supply and delivery times; other changes that week.
**Numeric work (illustrative):** Normal 10,000. Actual 8,500 (-15%). If past rain weeks average -8% (assumed), expected is 9,200, so weather explains about 8 points (800 orders) and 7 points (700 orders) are unexplained.
**If the data shows...:** Dry cities flat and rainy cities down by the usual: weather explains it. Dry cities down too: something else.
**Recommendation:** Report the split; chase the unexplained 7 points; add rainfall to the forecast.
**Likely follow-ups:** (1) Data source? Public rainfall data, unverified here. (2) Is rain good or bad? Depends on the business.
**Common mistakes / traps:** Blaming weather by default; one rainy week as the only evidence.

### Q81 ⭐ 🟡 You pause paid advertising for a week and orders fall 20%. How do you tell the share driven by ads from organic?
**Asked at:** commonly asked (no company-specific report found); incrementality is a common marketing-analytics topic (unverified).
**What the interviewer is checking:** Whether you know paused-ad drops overstate or understate ad impact unless a baseline exists.
**Say this in the interview:** "The 20% drop is the ad-driven share only if nothing else changed. Better is a holdout: pause in some regions and keep others running, then compare."
**Clarify first:** Was pausing the only change? Normal seasonality? Were all channels paused?
**Structure:** Orders = organic (would happen anyway) + ad-driven (incremental). Ad-driven share = fall / normal.
**What I would check, in order:** Orders by source (paid, organic, direct) before and during; regional holdout (paused versus running); brand search; whether organic fell too (ads also lift awareness).
**Numeric work (illustrative):** Normal 1,000 a week; during pause 800. Ad-attributed orders 200 = 20% of orders; organic 80%. If the control region (ads on) stayed at 1,000, the 200 is fully incremental. If the control also fell 5%, true incrementality is 15% (150 orders).
**If the data shows...:** Attributed paid orders far above the drop: many would have ordered anyway. Drop larger than attributed: ads boost organic too.
**Recommendation:** Run geo holdouts regularly; compare cost per incremental order, not per attributed order.
**Likely follow-ups:** (1) Short-term only? Effects can lag. (2) Why holdout? It controls timing.
**Common mistakes / traps:** Trusting last-click attribution; no control.

### Q82 ⭐ 🟡 How do survivorship effects mislead a retention or sales drop analysis that only uses currently active customers?
**Asked at:** commonly asked (no company-specific report found); survivorship bias is a standard analytics caution (unverified).
**What the interviewer is checking:** Whether you remember to include customers who left.
**Say this in the interview:** "If I only study customers still active, I see only the survivors, who naturally look loyal and high-spending, and I miss exactly the people who caused the drop."
**Explain simply:**
- Survivorship bias: analysing only those who "survived" a filter. Here the filter is "still active today".
- Example (illustrative): 1,000 customers joined; 600 left; 400 remain. Retention computed on the 400 is 100%, but true retention is 400 / 1,000 = 40%.
- Their average spend also looks higher because low spenders left first. A drop in total sales then looks unexplained.
- Fix: use the full starting cohort (all who joined in a period), track them forward, and include churned customers in profiling; compare leavers and stayers on early behaviour.
**Practice step:** Start every retention table from "everyone who joined in month X", not "everyone active now".
**Likely follow-ups:** (1) Which table? A cohort table. (2) Same for employees? Yes, exit-interview-only data misses those who stayed silent.
**Common mistakes / traps:** Averaging over survivors only; dropping inactive users from the denominator.

### Q83 ⭐ 🟡 Demand cannot be seen when an item is out of stock. How does this censor your sales data and how do you correct for it?
**Asked at:** commonly asked (no company-specific report found); stock-out censoring is a gap-fill, not seen in a company report (unverified).
**What the interviewer is checking:** Whether you distinguish sales (what you sold) from demand (what customers wanted).
**Say this in the interview:** "Sales are capped by stock, so out-of-stock days hide demand. I would estimate demand from in-stock days and treat the gap as lost sales."
**Explain simply:**
- Censored data: you only see up to a limit. Zero sales on a stock-out day does not mean zero demand.
- Example (illustrative): an item sells 100 a day when available. It is out of stock 6 of 30 days. Observed sales = 24 x 100 = 2,400, which looks like a 20% drop against 3,000.
- Correction: demand per in-stock day = 2,400 / 24 = 100; estimated demand for 30 days = 3,000; lost sales = 600 units. Customers did not leave; supply did.
- Check inventory logs and availability (the share of hours in stock) by item and store; also look for substitution (sales of a similar item rising).
**Practice step:** Always add "availability %" next to sales.
**Likely follow-ups:** (1) What if stock-out is partial-day? Use hourly availability. (2) Substitutes? Subtract substituted units from lost sales.
**Common mistakes / traps:** Reading a stock-out as demand collapse; averaging in zero-stock days.

### Q84 ⭐ 🟡 Why does a B2B SaaS company's Tuesday order drop need a different hypothesis list than a consumer app's?
**Asked at:** commonly asked (no company-specific report found); contrast question built from the Tuesday case (unverified).
**What the interviewer is checking:** Whether you adapt hypotheses to who buys and how, rather than reuse a consumer checklist.
**Say this in the interview:** "B2B orders come from few accounts, long contracts and business calendars, so I would check key-account timing, procurement cycles and sales-team activity, not weather or delivery times."
**Explain simply:**
- Consumer app: many small buyers, so causes are broad (app bug, promotion, delivery, weather).
- B2B: a handful of large accounts, so one delayed renewal or invoice can be the whole drop. Orders follow contract dates, month-end budgets, and billing runs.
- Hypotheses: a big customer's order moved to another day; sales team out (offsite, holiday in a customer's country); billing system or invoice batch schedule changed; quote-to-order lag; sales meetings pattern moved.
- Data: orders by account (top 10 share), deal stage dates, sales-rep activity, quote status.
**Short worked example:** If 3 accounts make 40% of Tuesday orders and one of them shifted its order to Wednesday, Tuesday drops without any demand change.
**Practice step:** For any case, first ask: many small buyers or few big ones?
**Likely follow-ups:** (1) Noise? Small samples make weekly swings bigger. (2) First check? Largest accounts.
**Common mistakes / traps:** Using consumer hypotheses; ignoring concentration.

### Q85 ⭐ 🟡 A telecom operator's prepaid recharge value fell 20% in a month. Which segment cuts and external factors do you check first?
**Asked at:** commonly asked (no company-specific report found); telecom variant of a revenue-drop case (unverified).
**What the interviewer is checking:** Whether you break recharge value into subscribers, frequency and recharge size, and think of price-plan and competition effects.
**Say this in the interview:** "Recharge value = subscribers x recharges per month x average recharge. I would find which factor fell, then cut by plan, circle and customer type, and check tariff changes and competitor offers."
**Clarify first:** Is it total or average per user (ARPU)? Same days in month? Gross or after validity changes?
**Structure:** Value = active subscribers x frequency x average recharge. External: competitor tariffs, regulatory changes, festivals, network issues, mobile number portability. Internal: plan change, app or channel issues.
**What I would check, in order:** Active subscribers by circle and acquisition month; recharge count per user; recharge size mix (small packs replacing large ones); plan validity (longer validity means fewer recharges, not less value per day); dual-SIM and churn to competitors.
**If the data shows...:** Subscribers flat, recharges fewer: validity or plan change. Subscribers down in some circles: network or competitor. Average recharge down: downgrade to cheaper plans.
**Recommendation:** Report value per user per day to remove validity effects, and size each factor in rupees.
**Likely follow-ups:** (1) Why per day? Validity differences. (2) External first? Competitor price moves.
**Common mistakes / traps:** Ignoring plan validity; confusing churn with lower usage.

### Q86 ⭐ 🔴 How do you use synthetic control or Causal Impact to estimate the effect of an event on sales?
**Asked at:** commonly asked (no company-specific report found); advanced differentiator, unlikely in entry rounds (unverified).
**What the interviewer is checking:** Whether you understand building a "what would have happened" line from unaffected comparison series.
**Say this in the interview:** "I build a counterfactual, the expected sales without the event, from similar unaffected series (other cities) that tracked our series before the event; the gap after the event is the estimated effect."
**Explain simply:**
- Problem: you cannot see what sales would have been without the event. Solution: a weighted mix of comparison regions (the synthetic control) that matched our region before the event.
- Causal Impact (a Google-developed method) does a similar thing using a statistical model on control series and gives a range of uncertainty.
- Steps: pick the event date; choose control series not affected; check the fit over the pre-period; predict the post-period; effect = actual - predicted; check with a placebo (pretend the event happened elsewhere).
- Example (illustrative): after the event, our city sells 80 units; the synthetic control predicts 95. Effect = -15 units, or -15.8%. A naive before-after comparison (100 to 80) says -20%, overstating because the baseline was rising.
**Practice step:** Try it in Excel as a ratio of our city to the average of other cities, before and after.
**Likely follow-ups:** (1) Needs? Good controls and a long pre-period. (2) Weakness? Poor fit means unreliable.
**Common mistakes / traps:** Controls affected by the event; short pre-period; reporting a single number without uncertainty.

### Q87 ⭐ 🔴 How do you use interrupted time series to test whether an app release caused a drop?
**Asked at:** commonly asked (no company-specific report found); advanced differentiator (unverified).
**What the interviewer is checking:** Whether you separate a level or slope change at the release from the existing trend.
**Say this in the interview:** "I fit the trend before the release, then test whether the level or slope changes right at the release date, after allowing for weekday effects. A sudden step at the date points to the release."
**Explain simply:**
- Interrupted time series: a long series with a known break (the release). Fit a trend line before the break; check for a jump (level change) or change in direction (slope change) after.
- Use daily data, at least several weeks before and after, with weekday adjustment (since orders have weekly cycles).
- Evidence for the release: break exactly at the date, bigger on the new app version than the old, similar drop across regions, and recovery after a fix.
- Weakness: other changes the same day (price, promotion) are indistinguishable; it shows timing, not proof. A staged rollout (some users on the new version) makes it much stronger.
**Short worked example (illustrative):** Orders trending flat at 1,000 a day before; after release 800 a day. That is a level shift of -200 (-20%) with no change in trend.
**Practice step:** Compare orders on the new versus the old app version on the same days.
**Likely follow-ups:** (1) Better method? A staged rollout test. (2) Gradual effect? Test the slope change.
**Common mistakes / traps:** Ignoring weekday pattern; too few points; assuming no concurrent changes.

### Q88 ⭐ 🔴 A new private-label product launched; branded sales fell 20% while category sales were flat. How do you assess cannibalisation?
**Asked at:** commonly asked (no company-specific report found); a retail-analytics case variant (unverified).
**What the interviewer is checking:** Whether you compare lost branded sales with private-label gains at category level, then at profit level.
**Say this in the interview:** "Flat category with branded down and private label up means customers switched rather than bought more. I would size the transfer, then check profit, because shifting to private label can be good if its margin is higher."
**Clarify first:** Whose business? A retailer selling both, or the brand owner? Same stores and period? Any promotions?
**Structure:** Category = branded + private label (PL). Cannibalisation = share of PL sales that came from branded sales lost.
**What I would check, in order:** Units and value by product before and after; customer-level switching (same customers who bought branded now buying PL); price gap; margin per unit; stores with and without the PL launch.
**Numeric work (illustrative, assumed):** Category 1,000 units. Branded 1,000 to 800 (-200); PL 0 to 200. Category flat at 1,000, so 100% of PL sales are cannibalised (200 of 200). If branded earns Rs 20 a unit and PL Rs 30, profit = 20,000 before; 800 x 20 + 200 x 30 = 22,000 after, a 10% gain for the retailer, but a brand owner loses.
**If the data shows...:** Category grows: some PL sales are incremental. Control stores without PL stay stable: confirms cause.
**Recommendation:** Judge by category profit, not branded sales; track switching by customer.
**Likely follow-ups:** (1) Branded owner? Loses share, consider response. (2) Control? Non-launch stores.
**Common mistakes / traps:** Treating the drop as a demand problem; ignoring margin.

### Q89 ⭐ 🔴 A stakeholder insists a competitor caused the drop but your data points elsewhere. How do you handle it?
**Asked at:** commonly asked (no company-specific report found); a stakeholder-handling question (unverified).
**What the interviewer is checking:** Whether you treat the stakeholder's idea as a hypothesis to test, stay respectful and let evidence lead.
**Say this in the interview:** "I would take the competitor idea seriously as a hypothesis, test it with the data I can get, show side by side what supports and what contradicts it, and agree on what further evidence would change my view."
**Clarify first:** What makes them confident (a competitor launch, a lost deal, news)? What evidence would convince them?
**Structure:** Hear the hypothesis; test it fairly (timing, affected segments, price comparisons, lost-customer surveys, share of search or traffic); present the evidence; agree on next steps.
**What I would check, in order:** Does the drop start when the competitor acted? Does it hit overlapping cities and products? Where did lost customers go (survey, switching data)? Does my alternative cause explain more of the size?
**If the data shows...:** Both explain part: size each in rupees and say so. Competitor hypothesis fails on timing: show the dates plainly, keep an open door for new data.
**Recommendation:** Present as "what we know, what we do not, and what test would settle it"; avoid saying the stakeholder is wrong.
**Likely follow-ups:** (1) What if data is thin? Say so, give a range. (2) Escalate? Only with evidence.
**Common mistakes / traps:** Arguing, defending ego, dismissing; hiding uncertainty.

### Q90 ⭐ 🔴 How would you design an automated root-cause tool for metric drops, and what are its failure modes?
**Asked at:** commonly asked (no company-specific report found); a product-thinking differentiator (unverified).
**What the interviewer is checking:** Whether you can turn a manual drill-down into steps and know where automation misleads.
**Say this in the interview:** "The tool detects a drop, validates the data, drills into dimensions to find the segments contributing most, adds context like releases and holidays, and gives a ranked, plain-language summary with confidence."
**Explain simply:**
- Step 1: detect against an expected value (seasonal), not a fixed threshold. Step 2: data-quality checks (pipeline delays, null counts). Step 3: break the change down by dimension (city, device, channel, product) and rank by contribution in absolute units. Step 4: tie to event logs (releases, price changes, campaigns). Step 5: output a short summary and a link to the dashboard.
- Failure modes: many false alarms; spurious segments when you test hundreds of cuts; mix-shift (Simpson) confusion; correlation presented as cause; missing event logs; tiny segments; stale data; people trust it blindly.
- Safeguards: minimum sizes, show contribution not only percent, human review, feedback on suggestions.
**Short worked example:** Drop of 2,000 orders: Hyderabad contributes 1,500 (75%), Android 1,400; the tool flags a release in Hyderabad Android yesterday. A human then verifies.
**Practice step:** Sketch the tool as five boxes on paper.
**Likely follow-ups:** (1) How to measure it? Share of drops correctly diagnosed. (2) Build or buy? Start simple.
**Common mistakes / traps:** Promising causes instead of leads; ignoring data-quality checks.

### Q91 ⭐ 🔴 Price and supply both fell together and orders fell 20%. How do you attribute the drop between two interacting causes?
**Asked at:** commonly asked (no company-specific report found); advanced attribution question (unverified).
**What the interviewer is checking:** Whether you admit the two effects overlap and use a fair method (solo effects plus a shared split) instead of forcing neat shares.
**Say this in the interview:** "When two causes act together, their solo effects do not add up. I estimate each alone, measure the overlap, and split the overlap fairly, for example with Shapley values (averaging the effect over both orders of adding the cause)."
**Clarify first:** "Price fell" means our price cut or a competitor's? "Supply fell" means fewer riders or stock? Can I find periods or places where only one changed?
**Structure:** Orders = f(price, supply). Estimate with four scenarios: neither changed, only price, only supply, both.
**What I would check, in order:** Find cities or days where only one moved; fit a model with an interaction term (price x supply); otherwise use the sizing from segment comparisons.
**Numeric work (illustrative, assumed):** Baseline 10,000. Price change alone: 9,000 (-1,000). Supply change alone: 8,800 (-1,200). Both: 8,000 (-2,000, the 20% drop). Solo effects sum to 2,200, but the real total is 2,000, so the overlap is +200 (the same customers lost). Shapley split: price = (-1,000 + (8,000 - 8,800)) / 2 = -900; supply = (-1,200 + (8,000 - 9,000)) / 2 = -1,100. Total -2,000, so price 45% and supply 55%.
**If the data shows...:** Effects add up: simple split. Strong overlap: say the split is a convention, not a fact.
**Recommendation:** Present a range, fix the larger lever first, and test with a controlled change.
**Likely follow-ups:** (1) Why not just split 50-50? It ignores size. (2) Is Shapley exact? It is a fair convention, not proof of cause.
**Common mistakes / traps:** Adding solo effects and expecting 100%; claiming precise shares without a control.

