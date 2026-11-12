# Book 7 — Guesstimates, Case Studies & Business Metrics | Part 5: Root-Cause Cases (Sales Dropped, Orders Fell) 🟡🔴

**Target:** 90 questions | **Actual:** 91 questions
**Scope:** diagnosing falling sales, orders and revenue with hypothesis trees, data cuts, decision rules and numeric decompositions (price/volume/mix, funnel, region, cohort).

### Q1 ⭐⭐⭐ 🟢 Sales dropped 20% compared with last month. What clarifying questions do you ask before starting any analysis?
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 Orders on Tuesdays fell 20% compared with earlier weeks. How do you find out why?
**Data available:** order-level table (order time, city, platform, restaurant or seller id, customer id, promo code, order status, delivery time), app release log, marketing calendar, customer-support tickets.
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 How do you check that a reported drop in sales is real and not a data or dashboard problem?
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 How do you split a revenue drop into volume, price and mix effects?
**Given:** Revenue = number of orders x average order value (AOV).
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 What is a hypothesis tree (issue tree) for a sales drop, and how do you build one in the first two minutes of the interview?
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 How do you separate internal causes from external causes when a metric falls?
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟢 Which comparison baselines do you use when a metric drops (day-over-day, same weekday last week, year-over-year), and when does each one mislead?
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟢 Which segment cuts do you try first when a total metric falls, and in what order?
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟢 A food-delivery app's revenue last month was ₹5,00,000 (2,000 orders at ₹250 AOV) and this month it is ₹4,00,000 (1,600 orders at ₹250 AOV). By what percent did revenue fall and which driver explains it?
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟢 How do you decide which hypothesis to test first when you have ten possible causes and little time?
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟢 How do you present a root-cause finding to a non-technical business stakeholder in two minutes?
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 Revenue fell from ₹50,00,000 to ₹40,00,000 while orders fell from 20,000 to 18,000. How much of the ₹10,00,000 drop is due to fewer orders and how much to a lower AOV?
**Method to use:** volume effect = (new orders - old orders) x old AOV; AOV effect = (new AOV - old AOV) x new orders.
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 A shopping app's weekly funnel is below. Orders fell from 8,000 to 6,000. Which stage caused the fall and by what percent did it change?
| Stage | Last week | This week |
|---|---|---|
| Sessions | 2,00,000 | 2,00,000 |
| Sessions that reach a product page | 50% | 50% |
| Product-page views that add to cart | 20% | 20% |
| Carts that become orders | 40% | 30% |
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 Orders fell from 1,00,000 to 86,000 across four regions (table below). Which regions explain most of the drop, and which region fell fastest in percentage terms?
| Region | Last week | This week |
|---|---|---|
| North | 40,000 | 34,000 |
| South | 30,000 | 29,000 |
| East | 20,000 | 14,000 |
| West | 10,000 | 9,000 |
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 Orders fell from 10,000 to 8,500 per week. New customers fell from 3,000 to 1,800 and repeat customers from 7,000 to 6,700 orders. What share of the drop comes from new customers, and what does that suggest you check next?
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🟡 Tuesday orders normally are 1,000 out of 7,000 per week. This Tuesday they were 800 and every other day was normal. What was the weekly drop in percent, and does it justify an urgent investigation?
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐⭐ 🟡 A food-delivery app received 10,000 orders in each of two weeks. Cancelled orders were 500 in week 1 and 2,500 in week 2. How much did completed orders fall in percent, and what do you investigate?
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐⭐ 🟡 Revenue = active users x orders per user x AOV. Active users fell 5%, orders per user fell 8% and AOV rose 2%. By what percent did revenue change overall?
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐⭐ 🟡 Orders dropped 20% on a single day (a Tuesday) and recovered fully the next day. How do you investigate a one-day dip?
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐⭐ 🟡 Orders are down 20% only on Tuesdays and normal on other days. List the weekday-specific hypotheses you would test, grouped by demand, supply, operations, marketing and data.
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐⭐ 🟡 You open the executive dashboard and see completed orders falling month-on-month. You are the analytics lead. What do you do, step by step?
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐⭐ 🟡 A food-delivery platform's orders fell 20% week-over-week. How do you structure a diagnosis across customers, restaurants and delivery partners?
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐⭐ 🟡 An e-commerce company's gross sales were ₹100 crore in both months, but returns rose from 10% to 25% of gross sales. By what percent did net sales fall and which causes of rising returns do you check?
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐⭐ 🟡 An edtech company's course sales fell 20%. Data is below. Which part of the funnel explains the fall and what do you recommend checking?
| Item | Last month | This month |
|---|---|---|
| Ad spend | ₹10,00,000 | ₹10,00,000 |
| Cost per lead | ₹200 | ₹250 |
| Lead-to-sale conversion | 4% | 4% |
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐⭐ 🟡 UPI payment success fell from 96% to 92%. Data is below. How much of the extra failures come from Bank X, and what do you do next?
| Segment | Attempts | Failures last week | Failures this week |
|---|---|---|---|
| Bank X | 3,00,000 | 12,000 | 48,000 |
| All other banks | 7,00,000 | 28,000 | 32,000 |
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐⭐ 🟡 Diwali fell in November last year and in October this year. Sales (in ₹ lakh) are below. November is down 16.7% year-over-year. Is there a real problem?
| Month | Last year | This year |
|---|---|---|
| October | 100 | 130 |
| November | 120 | 100 |
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐⭐ 🟡 Sales dropped 20% in Hyderabad while all other cities are flat. What hypotheses and data cuts do you use?
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐⭐ 🔴 Cart additions on an e-commerce app fell 15% over the last three days, mostly on the mobile app. How do you diagnose it?
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐⭐ 🔴 Leadership says a 20% drop in revenue is 'just seasonal'. How do you prove or disprove that with data?
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐⭐ 🔴 A price change, a competitor promotion and an app release all happened in the week orders fell 20%. How do you apportion the drop between them?
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐⭐ 🔴 The CEO wants the cause of a 20% orders drop within one hour and only partial data is available. What do you deliver?
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟢 How do you use the 5 Whys in a sales-drop analysis, and what are its limits?
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟢 You find that discounts and orders both fell in the same week. How do you tell correlation from a root cause?
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟢 On a 'sales dropped' ticket, which tables and fields do you ask for first?
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟢 How does your investigation change for a one-time dip, a step change and a gradual decline?
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟢 How do you size the impact of a hypothesis so you know whether it explains the whole drop?
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟢 What are leading and lagging indicators, and how do they help diagnose a decline in orders?
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟢 Conversion fell from 5% to 4%. What is the drop in percentage points and in percent, and why does the difference matter in a root-cause discussion?
<!-- ANSWER_PENDING -->

### Q39 ⭐⭐ 🟢 AOV fell 10% but order count is flat. What hypotheses do you check?
<!-- ANSWER_PENDING -->

### Q40 ⭐⭐ 🟢 This month has 4 Tuesdays and last month had 5. Tuesday orders were 5,000 per Tuesday in both months. Tuesday orders fell from 25,000 to 20,000 in total. Is that a real 20% drop?
<!-- ANSWER_PENDING -->

### Q41 ⭐⭐ 🟢 How do you decide that a root-cause analysis is finished and you can recommend an action?
<!-- ANSWER_PENDING -->

### Q42 ⭐⭐ 🟡 A website's overall conversion fell although no segment's conversion changed. Data is below. Compute the overall conversion in both weeks and explain the cause.
| Platform | Traffic share week 1 | Conversion week 1 | Traffic share week 2 | Conversion week 2 |
|---|---|---|---|---|
| Android | 80% | 4% | 90% | 4% |
| iOS | 20% | 8% | 10% | 8% |
<!-- ANSWER_PENDING -->

### Q43 ⭐⭐ 🟡 A SaaS company's MRR (in ₹ lakh) moved as below. Compute closing MRR and say which component is the main culprit in the 5% fall.
| Opening MRR | New | Expansion | Contraction | Churn |
|---|---|---|---|---|
| 100 | +8 | +4 | -3 | -14 |
<!-- ANSWER_PENDING -->

### Q44 ⭐⭐ 🟡 Weekly active users fell from 50,000 to 45,000. Data is below. Which component drives the fall and what do you check next?
| Component | Last week | This week |
|---|---|---|
| Retained users | 40,000 | 38,000 |
| New users | 8,000 | 5,000 |
| Resurrected users | 2,000 | 2,000 |
<!-- ANSWER_PENDING -->

### Q45 ⭐⭐ 🟡 The last eight Tuesdays had 1,000, 1,020, 980, 1,010, 990, 1,005, 995 and 1,000 orders. This Tuesday had 800. Is 800 within normal noise? Show a quick calculation using mean and standard deviation.
<!-- ANSWER_PENDING -->

### Q46 ⭐⭐ 🟡 Ride requests were 1,00,000 in both weeks. Driver acceptance fell from 85% to 70% and 95% of accepted rides are completed in both weeks. By what percent did completed rides fall and where do you look?
<!-- ANSWER_PENDING -->

### Q47 ⭐⭐ 🟡 A quick-commerce app's average delivery time rose from 10 to 16 minutes and orders fell. How do you test whether slower delivery caused the fall and not the other way round?
<!-- ANSWER_PENDING -->

### Q48 ⭐⭐ 🟡 A lending app's loan disbursals fell. Data is below. Compute disbursals in both months and the percent change, and name the likely driver.
| Item | Last month | This month |
|---|---|---|
| Applications | 50,000 | 48,000 |
| Approval rate | 40% | 32% |
| Approved loans actually disbursed | 90% | 90% |
<!-- ANSWER_PENDING -->

### Q49 ⭐⭐ 🟡 Payroll cost rose from ₹10 crore to ₹11.2 crore while headcount rose from 1,000 to 1,020. Compute the change in cost per head and list where you would look for the rise.
<!-- ANSWER_PENDING -->

### Q50 ⭐⭐ 🟡 Monday attendance at a 500-agent call centre fell from 94% to 86%. How many more agents are absent on Mondays, and how do you find the cause?
<!-- ANSWER_PENDING -->

### Q51 ⭐⭐ 🟡 The dashboard shows orders down 20% but the payment settlement report shows only 2% fewer paid orders. How do you reconcile the two?
<!-- ANSWER_PENDING -->

### Q52 ⭐⭐ 🟡 Mobile-phone page views were flat at 1,00,000 per day and the in-stock conversion rate is 3%. Stock availability fell from 95% to 70%. By what percent do you expect orders to change?
<!-- ANSWER_PENDING -->

### Q53 ⭐⭐ 🟡 Average monthly sales are 100 (units in lakh) and November's seasonal index is 0.85. November actual sales were 90. Is this a drop or not?
<!-- ANSWER_PENDING -->

### Q54 ⭐⭐ 🟡 A company raised its price by 10% and volume fell by 8%. Did revenue fall? Compute the change and say what else you would check before blaming the price rise.
<!-- ANSWER_PENDING -->

### Q55 ⭐⭐ 🟡 A promo code accounted for 40% of orders and the promo ended. Total orders fell 20% and non-promo orders were unchanged. What share of promo orders disappeared?
<!-- ANSWER_PENDING -->

### Q56 ⭐⭐ 🟡 A restaurant app's average rating fell from 4.4 to 4.1 two weeks before orders fell. How would you test whether the rating drop led the order drop?
<!-- ANSWER_PENDING -->

### Q57 ⭐⭐ 🟡 How do you test whether a competitor's launch caused your decline using only your own data?
<!-- ANSWER_PENDING -->

### Q58 ⭐⭐ 🟡 Orders fell 20% on Android after app release 7.3 while iOS was flat. Android is 60% of 10,000 orders. What is the overall drop and what is your decision rule on rollback?
<!-- ANSWER_PENDING -->

### Q59 ⭐⭐ 🟡 The last two days show orders 20% lower than usual, but the data pipeline has late-arriving events. How do you detect and handle this?
<!-- ANSWER_PENDING -->

### Q60 ⭐⭐ 🟡 The January cohort (10,000 users) has 30% active in month 1 and the March cohort (12,000 users) has 22%. How many fewer users are active than if March matched January, and what does this suggest about the sales drop?
<!-- ANSWER_PENDING -->

### Q61 ⭐⭐ 🟡 Many partner restaurants take their weekly off on Tuesday. Active restaurants on Tuesday fell from 1,000 to 800 and orders per active restaurant stayed at 10. By what percent did Tuesday orders change and how do you verify this hypothesis?
<!-- ANSWER_PENDING -->

### Q62 ⭐⭐ 🔴 Segment A and B conversion are below. Both segments improved but overall conversion fell. Compute the rate effect and the mix effect.
| Segment | Users wk 1 | Conv wk 1 | Users wk 2 | Conv wk 2 |
|---|---|---|---|---|
| A | 6,000 | 5.0% | 8,000 | 5.5% |
| B | 4,000 | 10.0% | 2,000 | 11.0% |
<!-- ANSWER_PENDING -->

### Q63 ⭐⭐ 🔴 Region T had a price test and Region C did not. Orders are below. Estimate the effect of the test using a difference-in-differences and say what assumption you rely on.
| Region | Before | After |
|---|---|---|
| T (test) | 10,000 | 8,500 |
| C (control) | 10,000 | 9,500 |
<!-- ANSWER_PENDING -->

### Q64 ⭐⭐ 🔴 How would you design monitoring so that a Tuesday-type drop is caught within a day next time?
<!-- ANSWER_PENDING -->

### Q65 ⭐⭐ 🔴 Sales fell 20% after a loyalty programme change. How do you isolate its causal effect without a randomised experiment?
<!-- ANSWER_PENDING -->

### Q66 ⭐⭐ 🔴 Both orders per user and active restaurants fell on a two-sided marketplace. How do you tell which side fell first?
<!-- ANSWER_PENDING -->

### Q67 ⭐⭐ 🔴 How do you build an expected-value baseline with trend and seasonality so you can quantify the true shortfall in sales?
<!-- ANSWER_PENDING -->

### Q68 ⭐ 🟢 What is a fishbone (Ishikawa) diagram and how would you use it for falling orders?
<!-- ANSWER_PENDING -->

### Q69 ⭐ 🟢 Five causes explain a sales drop with contributions of 50, 25, 10, 8 and 7 units out of a 100-unit drop. Which causes would a Pareto approach fix first and what share do they cover?
<!-- ANSWER_PENDING -->

### Q70 ⭐ 🟢 What is a waterfall (bridge) chart, and what is the closing value of one starting at 100 with price +3, volume -18 and mix -5?
<!-- ANSWER_PENDING -->

### Q71 ⭐ 🟢 Why is looking only at the average dangerous when you investigate a drop, and what do you look at instead?
<!-- ANSWER_PENDING -->

### Q72 ⭐ 🟢 A 28-day month had total sales of 280 and a 31-day month had 310. Is there a drop on a per-day basis?
<!-- ANSWER_PENDING -->

### Q73 ⭐ 🟢 What is anomaly detection and when does a static threshold fail for orders data?
<!-- ANSWER_PENDING -->

### Q74 ⭐ 🟡 A payment-gateway outage lasted two hours in a period when normal orders are 500 per hour. During the outage only 40% of normal orders went through. Estimate lost orders and say how you would separate lost from delayed orders.
<!-- ANSWER_PENDING -->

### Q75 ⭐ 🟡 How can timezone or daylight-saving handling create a fake 'Tuesday drop' in an events table?
<!-- ANSWER_PENDING -->

### Q76 ⭐ 🟡 How do bots or fraud filtering changes make orders or sessions look like they dropped?
<!-- ANSWER_PENDING -->

### Q77 ⭐ 🟡 What is Simpson's paradox and how can it show up when you slice a falling metric by segment?
<!-- ANSWER_PENDING -->

### Q78 ⭐ 🟡 Sales fell 20% but profit rose. Is that a problem, and how do you investigate?
<!-- ANSWER_PENDING -->

### Q79 ⭐ 🟡 A tax or regulatory change is announced. How do you check whether it caused a drop in orders?
<!-- ANSWER_PENDING -->

### Q80 ⭐ 🟡 A rainy week coincides with a drop in order count. How do you separate the weather effect from other causes?
<!-- ANSWER_PENDING -->

### Q81 ⭐ 🟡 You pause paid advertising for a week and orders fall 20%. How do you tell the share driven by ads from organic?
<!-- ANSWER_PENDING -->

### Q82 ⭐ 🟡 How do survivorship effects mislead a retention or sales drop analysis that only uses currently active customers?
<!-- ANSWER_PENDING -->

### Q83 ⭐ 🟡 Demand cannot be seen when an item is out of stock. How does this censor your sales data and how do you correct for it?
<!-- ANSWER_PENDING -->

### Q84 ⭐ 🟡 Why does a B2B SaaS company's Tuesday order drop need a different hypothesis list than a consumer app's?
<!-- ANSWER_PENDING -->

### Q85 ⭐ 🟡 A telecom operator's prepaid recharge value fell 20% in a month. Which segment cuts and external factors do you check first?
<!-- ANSWER_PENDING -->

### Q86 ⭐ 🔴 How do you use synthetic control or Causal Impact to estimate the effect of an event on sales?
<!-- ANSWER_PENDING -->

### Q87 ⭐ 🔴 How do you use interrupted time series to test whether an app release caused a drop?
<!-- ANSWER_PENDING -->

### Q88 ⭐ 🔴 A new private-label product launched; branded sales fell 20% while category sales were flat. How do you assess cannibalisation?
<!-- ANSWER_PENDING -->

### Q89 ⭐ 🔴 A stakeholder insists a competitor caused the drop but your data points elsewhere. How do you handle it?
<!-- ANSWER_PENDING -->

### Q90 ⭐ 🔴 How would you design an automated root-cause tool for metric drops, and what are its failure modes?
<!-- ANSWER_PENDING -->

### Q91 ⭐ 🔴 Price and supply both fell together and orders fell 20%. How do you attribute the drop between two interacting causes?
<!-- ANSWER_PENDING -->
