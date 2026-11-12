# Book 7 — Guesstimates, Case Studies & Business Metrics | Part 4: Business Metrics (KPIs, DAU/MAU, CAC, LTV, Churn, Retention, Conversion) 🟢🟡

**Target:** 80 questions | **Actual:** 87 questions
**Scope:** definitions, calculations with inline data and structured metric-design questions on KPIs, DAU/MAU, CAC, LTV, churn, retention, conversion, AOV, funnels and HR metrics for Indian consumer, fintech, SaaS and edtech contexts; no statistics or A/B-test theory (Book 5) and no root-cause cases (Part 5).

### Q1 ⭐⭐⭐ 🟢 What is the DAU/MAU ratio (stickiness), and what does it tell you about a product?
**Asked at:** commonly asked (no company-specific report found); prep sites list DAU/MAU among the most tested product metrics (unverified for any company).
**What the interviewer is checking:** Whether you can define the ratio and read it as "how often the monthly crowd comes back", not as a vague score.
**Say this in the interview:** "DAU is the average number of distinct users active on a day; MAU is distinct users active in the month. DAU divided by MAU is stickiness: the share of monthly users who show up on an average day."
**Explain simply:**
- DAU = Daily Active Users (people counted once per day). MAU = Monthly Active Users (people counted once per month, over the last 30 days).
- Stickiness = average DAU / MAU. Example: DAU 40,000 and MAU 160,000 gives 25%.
- Rough reading: 25% means the average monthly user is active about 7.5 days out of 30 (0.25 x 30). A 100% ratio would mean everyone uses it every day.
- What "good" is depends on the product: a chat or UPI app is expected to be daily; a travel booking app is not. Compare against similar products and against your own trend, not against one magic number (any benchmark such as "above 20%" is a rule of thumb, unverified).
**Short worked example:** If MAU rises from 160,000 to 200,000 but DAU stays at 40,000, stickiness falls from 25% to 20%: you added people, but they are not coming back more often.
**Practice step:** Pick an app you use. Guess how many days a month you open it, divide by 30, and that is your personal "stickiness".
**Likely follow-ups:** (1) Is higher always better? No; for a rarely needed product a low ratio is normal. (2) Does it show quality? Not alone; see the limitations in Q24.
**Common mistakes / traps:** Mixing a single-day DAU with a 30-day MAU instead of using the monthly average of DAU; using different "active" definitions for the top and bottom (see Q2); forgetting MAU includes people who were active only once.

### Q2 ⭐⭐⭐ 🟢 How do you define an "active user" for DAU, and why does the definition matter?
**Asked at:** commonly asked (no company-specific report found); metric-definition questions (numerator, denominator, window, exclusions) are described as typical on prep guides (unverified).
**What the interviewer is checking:** Whether you tie "active" to real value delivered, not just an app open.
**Say this in the interview:** "I would define active as a user who completes a core action, such as placing an order or sending a payment, not just opening the app, because the definition decides every ratio built on top of it."
**Explain simply:**
- A weak definition: "opened the app" or "any session". It counts accidental opens, push-notification taps and bots.
- A stronger definition: a meaningful action tied to the product's value. Examples: UPI app = at least one successful payment or balance check; food delivery = browsed a menu or placed an order; HR portal = logged in and viewed or submitted something.
- Decide also: the time window (calendar day or rolling 24 hours, and which time zone, IST for India), whether to count logged-in users only, and which users to exclude (employees, test accounts, bots).
**Short worked example:** 50,000 people open an app in a day, but only 30,000 do anything beyond the home screen. Under "open" DAU = 50,000; under "core action" DAU = 30,000. With MAU of 160,000 the stickiness is 31% versus 19%. Same product, very different story.
**Practice step:** Write your definition in one line: who, which action, which window, which exclusions.
**Likely follow-ups:** (1) Can a company have two actives? Yes, e.g. "active" and "transacting"; label them clearly. (2) What if the definition changes? Restate the old history on the new definition, otherwise trends break.
**Common mistakes / traps:** Counting opens and calling it engagement; changing the definition mid-year and reporting growth that is only a definition effect; not excluding internal and test accounts.

### Q3 ⭐⭐⭐ 🟢 What is customer churn rate, and how is it different from revenue churn?
**Asked at:** commonly asked (no company-specific report found); churn and LTV are listed among SaaS (software sold as a subscription) data analyst topics on prep blogs (unverified).
**What the interviewer is checking:** Whether you know churn can be counted in customers or in money, and that the two can disagree.
**Say this in the interview:** "Customer churn is the share of customers at the start of a period who left during it. Revenue churn is the share of starting revenue lost. They differ when the leavers are bigger or smaller spenders than average."
**Explain simply:**
- Customer churn rate = customers lost in the period / customers at the start of the period.
- Revenue churn rate = recurring revenue (money that repeats every month, such as subscription fees) lost through cancellations and downgrades / recurring revenue at the start. If upgrades from remaining customers are added back, the result is net revenue churn, which can even go negative.
- Worked example: 1,000 customers at the start, average payment Rs 500 a month, so Rs 5,00,000 revenue. 50 customers leave, each paying Rs 200. Customer churn = 50/1,000 = 5%. Revenue lost = 50 x 200 = Rs 10,000, so revenue churn = 10,000/5,00,000 = 2%.
- Reverse case: if the leavers are big customers, revenue churn is higher than customer churn. For an HR analogy, headcount attrition and payroll attrition behave the same way.
**Practice step:** For any subscription you know, ask: did we lose a lot of small customers or a few big ones?
**Likely follow-ups:** (1) Which is more important? Revenue churn for cash health, customer churn for product health; track both. (2) Do new joiners count in the denominator? No, only start-of-period customers.
**Common mistakes / traps:** Dividing by the end count or including customers acquired during the month in the denominator; mixing monthly and annual churn; ignoring downgrades in revenue churn.

### Q4 ⭐⭐⭐ 🟢 What is customer acquisition cost (CAC), and which costs should be included in it?
**Asked at:** CAC is named in prep guides for Swiggy business analyst rounds (Interview Query / Hacking the Case snippets, unverified).
**What the interviewer is checking:** Whether you count the full cost of winning a customer, not just ad spend.
**Say this in the interview:** "CAC is total sales and marketing cost in a period divided by the new customers won in that period. I would include everything spent to win customers, not only media spend."
**Explain simply:**
- Formula: CAC = total acquisition cost / number of new customers acquired.
- Include: ad and performance marketing spend, agency fees, referral and signup incentives or discounts given to win customers, salaries and commissions of sales and marketing staff, marketing tools, and a fair share of overheads.
- Do not include: costs of serving existing customers (support, delivery), or product development that benefits everyone (usually kept out; state the choice).
- Blended CAC counts all new customers, organic and paid. Paid CAC counts only paid spend divided by paid-acquired customers. Paid CAC is higher than blended CAC.
- Worked example: Rs 10,00,000 total cost, 400 new customers: CAC = Rs 2,500. If 150 of them came organically at no cost, paid CAC = 10,00,000 / 250 = Rs 4,000.
**Likely follow-ups:** (1) How do you compare it? Against LTV and payback (Q20). (2) HR parallel? Cost per hire: recruiter pay, job-board fees and agency fees divided by hires.
**Common mistakes / traps:** Using only ad spend; matching one month's spend to the same month's customers when conversion takes weeks; dividing by signups instead of paying or activated customers.

### Q5 ⭐⭐⭐ 🟢 What is customer lifetime value (LTV), and what is the simple formula when monthly churn is constant?
**Asked at:** LTV questions appear in Swiggy business analyst prep guides (PracHub / Interview Query snippets, unverified).
**What the interviewer is checking:** Whether you know the simple formula and its assumptions.
**Say this in the interview:** "LTV is the total profit a customer brings before leaving. With constant monthly churn, LTV = monthly ARPU x gross margin / monthly churn."
**Explain simply:**
- Customer lifetime in months = 1 / monthly churn. Example: 5% churn means 1/0.05 = 20 months on average.
- LTV = ARPU x gross margin % x lifetime = ARPU x gross margin / churn.
- Worked example: ARPU Rs 300, gross margin 50%, churn 5%. Monthly profit per customer = 300 x 0.5 = Rs 150. LTV = 150 / 0.05 = Rs 3,000. The revenue-only version (300 / 0.05 = Rs 6,000) overstates the value; use the margin version when comparing with CAC.
- It rests on assumptions: churn is the same every month (in reality new users churn faster), ARPU is flat, and no discounting. Treat the answer as a rough estimate.
**Likely follow-ups:** (1) Why does the formula work? Average lifetime of a customer under steady churn is 1/churn. (2) What if churn is very small? LTV explodes, so cap the lifetime (for example 3 to 5 years).
**Common mistakes / traps:** Using revenue instead of margin; mixing monthly ARPU with annual churn; applying a blended churn to a new cohort that behaves differently.

### Q6 ⭐⭐⭐ 🟢 What is retention rate, and what do Day-1, Day-7 and Day-30 retention mean for an app?
**Asked at:** retention is a named topic across prep banks (TechPrep, DataDriven snippets) and in the Mu Sigma guide lens (unverified).
**What the interviewer is checking:** Whether you know retention is measured per cohort, from a fixed start day.
**Say this in the interview:** "Retention is the share of a starting group of users who are still active later. Day-N retention is the share of users who installed on Day 0 and came back on Day N."
**Explain simply:**
- Retention rate = users from the starting group active at the later time / users in the starting group.
- Day-1: came back the day after install; this shows whether the first experience was worth a second visit. Day-7: whether a weekly habit is forming. Day-30: whether the product stuck for a month.
- Example: 1,000 installs, 400 open on Day 1, so Day-1 retention is 40% (see Q17 for the full calculation).
- Two ways to define: "classic" (active on exactly Day N) and "rolling or unbounded" (active on Day N or any day after). Always state which one.
- Typical shape: a big drop between Day 0 and Day 1, then a flattening curve. A curve that flattens at a positive level shows a loyal core.
**Likely follow-ups:** (1) Retention vs churn? Retention = 1 minus churn over the same group and window. (2) Which day matters? Depends on the natural usage cycle (daily app vs monthly bill-pay app).
**Common mistakes / traps:** Dividing by today's total users instead of the starting cohort; mixing cohorts of different dates; ignoring the definition of "active".

### Q7 ⭐⭐⭐ 🟢 What is a conversion rate, and why must its denominator be stated clearly?
**Asked at:** funnel and conversion topics appear in the Guvi Flipkart interview write-up (blog snippet, unverified) and prep banks.
**What the interviewer is checking:** Whether you treat a rate as "numerator over a stated base", not a loose percentage.
**Say this in the interview:** "Conversion rate is the share of people at one stage who complete the next action. I always say which group is the base, because the same orders give very different rates on different bases."
**Explain simply:**
- Conversion rate = people who did the target action / people who had the chance to do it.
- Same data, different denominators: 3,000 orders from 100,000 visits = 3% visit-to-order; the same 3,000 orders from 20,000 add-to-cart sessions = 15% cart-to-order. Both are true; they answer different questions.
- Also state the unit (visits, sessions, unique users) and the time window. A user who visits five times is five visits but one user.
- HR example: offer-acceptance rate = offers accepted / offers made (not / applicants).
**Likely follow-ups:** (1) Which denominator is best? The one that matches the decision; usually the people actually exposed to the step. (2) Can the rate exceed 100%? Only if the numerator and denominator are in different units or time windows, which is a warning sign.
**Common mistakes / traps:** Comparing rates with different bases; counting repeat visits as separate people; ignoring time lag between the visit and the order.

### Q8 ⭐⭐⭐ 🟢 What is the difference between a KPI and a metric?
**Asked at:** KPI understanding is listed in the Guvi Flipkart interview write-up and the Glassdoor Flipkart report mentions a KPI round (candidate claims, mapping unverified).
**What the interviewer is checking:** Whether you can separate "something we measure" from "something we manage the business by".
**Say this in the interview:** "Every KPI is a metric, but not every metric is a KPI. A KPI is a metric tied to a business goal, with a target and an owner."
**Explain simply:**
- Metric = any measurable number (page views, app opens, calls answered).
- KPI = Key Performance Indicator: a metric chosen because it shows progress on a goal, usually with a target, time frame and owner.
- Example: "Number of job-portal visits" is a metric. "Offer-acceptance rate of at least 80% this quarter, owned by the talent acquisition lead" is a KPI.
- The same metric can be a KPI for one team and just background for another.
- Fewer is better: a handful of KPIs per team, supported by many diagnostic metrics.
**Likely follow-ups:** (1) What is a vanity metric? One that looks good but does not drive decisions, such as total downloads. (2) How do KPIs link? Through a KPI tree (Q21).
**Common mistakes / traps:** Calling everything a KPI; choosing a KPI without a target or owner; picking numbers that are easy to measure rather than important.

### Q9 ⭐⭐⭐ 🟢 What is the difference between average order value (AOV) and average revenue per user (ARPU)?
**Asked at:** AOV is named in Swiggy business analyst prep guides and in a PracHub Swiggy AOV question (snippets, unverified).
**What the interviewer is checking:** Whether you know one is per order and the other is per user, linked by order frequency.
**Say this in the interview:** "AOV is revenue (or GMV) per order. ARPU is revenue per user over a period. ARPU = AOV x orders per user."
**Explain simply:**
- AOV = total order value / number of orders.
- ARPU = total revenue / number of users in the period (say which users: all active or paying only).
- Example: Rs 10,00,000 GMV from 5,000 orders placed by 1,000 users in a month. AOV = Rs 200. Orders per user = 5. ARPU = 10,00,000 / 1,000 = Rs 1,000, which equals 200 x 5.
- A rise in ARPU can come from a higher basket (AOV), more frequent ordering, or both. Diagnose which one before acting.
- Use GMV or net revenue consistently; for a marketplace the app's own revenue is a fraction of GMV (see Q30).
**Likely follow-ups:** (1) How do you raise AOV? Bundles, minimum-value free delivery, upsell. (2) Can AOV fall while ARPU rises? Yes, if frequency grows faster.
**Common mistakes / traps:** Using the wrong denominator (users versus orders); mixing GMV and revenue; reading ARPU for all registered users when only active ones matter.

### Q10 ⭐⭐⭐ 🟢 What is a North Star metric, and what would be a good one for a UPI payments app?
**Asked at:** North Star and primary metric definition is covered in the Towards Data Science case guide and prep sites; PhonePe is in the internal interview research for metric rounds (unverified for this question).
**What the interviewer is checking:** Whether you can pick one metric that reflects customer value and drives long-term growth.
**Say this in the interview:** "A North Star metric is the single number that best captures the value customers get and predicts long-term growth. For a UPI app I would choose monthly active transacting users, or successful transactions per active user per month."
**Explain simply:**
- A good North Star: reflects value delivered, is measurable, leads revenue, is influenceable by teams, and is not easy to game.
- For UPI: "number of successful payments per monthly active user" captures both reach (users) and depth (habit). Total payment value is weaker because a few large transfers can distort it.
- Back it with supporting metrics: new users activated, first-payment rate, payment success rate, repeat rate.
- Mention a guardrail such as payment failure rate and fraud rate (see Q11).
- Note: these are my choices for an exercise, not any company's official metric.
**Likely follow-ups:** (1) Why not revenue? It lags and can rise through price changes without more value. (2) Why not downloads? Vanity metric.
**Common mistakes / traps:** Choosing a metric the team cannot influence; picking total volume (hides who is using it); naming five "North Stars".

### Q11 ⭐⭐⭐ 🟢 What is a guardrail metric, and why do you need one next to a primary metric?
**Asked at:** guardrails with LTV appear in a PracHub Swiggy question snippet and primary-versus-supporting metrics in an Interview Query Flipkart guide (unverified).
**What the interviewer is checking:** Whether you think about unintended harm when you push one number.
**Say this in the interview:** "A guardrail is a metric that must not get worse while we chase the primary metric. It stops us winning the goal by damaging something else."
**Explain simply:**
- Primary metric = what we want to improve. Guardrail = what we refuse to damage.
- Example: a campaign to raise orders per user with big discounts. Primary: orders per user. Guardrails: profit per order, cancellation rate, customer complaints.
- HR example: primary metric = time to hire; guardrail = quality of hire or 90-day attrition, otherwise people rush bad hires.
- Set a clear limit in advance (for example, "complaint rate must not rise by more than 0.2 percentage points").
- Use two or three guardrails, not twenty.
**Likely follow-ups:** (1) What if the guardrail breaks? Pause or roll back and investigate. (2) Where do you see it? Same dashboard, same time window as the primary.
**Common mistakes / traps:** No guardrail at all; guardrails with no threshold; choosing guardrails that cannot move in the test period.

### Q12 ⭐⭐⭐ 🟢 An app had these average numbers in a month: DAU = 40,000 and MAU = 160,000. What is the stickiness ratio?
**Asked at:** commonly asked (no company-specific report found); a standard warm-up calculation on prep sites (unverified).
**What the interviewer is checking:** Whether you divide in the right order and read the result.
**Say this in the interview:** "DAU over MAU: 40,000 / 160,000 = 25%, so the average monthly user is active about 7 to 8 days a month."
**Definition in plain words:** Stickiness = average daily active users / monthly active users, the share of the monthly base that shows up on a typical day.
**Worked answer:**
1. Stickiness = DAU / MAU = 40,000 / 160,000 = 0.25.
2. As a percentage: 25%.
3. Reading: 0.25 x 30 days = 7.5 active days per monthly user on average.
**Result:** 25% stickiness (about 7.5 days a month per user).
**Check:** 25% of 160,000 = 40,000. Verified by script.
**Caveats:** Use the monthly average of daily DAU, not one day. "25%" is neither good nor bad without a benchmark of similar apps and a trend. The 7.5-day figure is a simplification: it assumes each user's active days are counted evenly, and it hides a mix of heavy daily users and one-time visitors.
**Likely follow-ups:** (1) If MAU rises to 200,000 and DAU stays 40,000? Stickiness drops to 20%. (2) Is 25% good for a payments app? Depends on peers; judge by trend.
**Common mistakes / traps:** Dividing MAU by DAU (gives 4); calling the ratio "users per day".

### Q13 ⭐⭐⭐ 🟢 A subscription app started the month with 5,000 paying customers and lost 150 of them during the month (no one else left). What is the monthly customer churn rate, and what average customer lifetime does it imply?
**Asked at:** commonly asked (no company-specific report found); churn and lifetime are standard SaaS-analyst topics on prep blogs (unverified).
**What the interviewer is checking:** Correct denominator (start-of-month customers) and the 1/churn lifetime link.
**Say this in the interview:** "150 lost out of 5,000 at the start is 3% monthly churn, so average lifetime is 1/0.03, about 33 months."
**Definition in plain words:** Monthly churn = customers lost in the month / customers at the start of the month. Average lifetime = 1 / churn.
**Worked answer:**
1. Churn = 150 / 5,000 = 0.03 = 3%.
2. Lifetime = 1 / 0.03 = 33.3 months, about 2.8 years.
**Result:** 3% monthly churn; implied average lifetime about 33 months.
**Check:** After 33 months at 3% a month, about 37% of a cohort (0.97^33) would still remain, so the 33-month average is a mean over a long tail, not a cut-off. Verified by script for the arithmetic.
**Caveats:** The lifetime holds only if churn stays constant at 3%. The denominator excludes new joiners during the month (the question says no one else left, and does not mention any joiners). Annualised, 3% a month is about 31% lost a year (1 - 0.97^12), not 36%.
**Likely follow-ups:** (1) If churn falls to 2%? Lifetime 50 months. (2) Is the 33-month figure reliable? Only roughly; new customers usually churn faster.
**Common mistakes / traps:** Using the end-of-month base; reporting lifetime as 3 months or 30; multiplying by 12 without compounding.

### Q14 ⭐⭐⭐ 🟢 A quick-commerce startup spent Rs 12,00,000 on marketing and Rs 3,00,000 on its sales team in a month and acquired 500 new customers. What is the blended CAC?
**Asked at:** CAC is named in Swiggy business analyst prep guides (snippets, unverified).
**What the interviewer is checking:** Whether you add all acquisition costs before dividing.
**Say this in the interview:** "Total acquisition cost is Rs 15,00,000; divided by 500 customers gives a blended CAC of Rs 3,000."
**Definition in plain words:** Blended CAC = (marketing cost + sales cost) / all new customers, organic and paid together.
**Worked answer:**
1. Total cost = 12,00,000 + 3,00,000 = Rs 15,00,000.
2. CAC = 15,00,000 / 500 = Rs 3,000.
**Result:** Blended CAC = Rs 3,000 per new customer.
**Check:** 500 x 3,000 = 15,00,000. Verified by script.
**Caveats:** Blended means organic customers are included, which lowers it compared with paid CAC. Whether other costs (discounts, tools, overhead) are included changes the number, so state the scope. Compare with LTV before judging if Rs 3,000 is acceptable: for example, it needs a margin-based LTV well above Rs 3,000 to make sense.
**Likely follow-ups:** (1) If 200 of the 500 were organic? Paid CAC = 15,00,000 / 300 = Rs 5,000 (all spend assigned to paid customers). (2) Is it good? Depends on LTV and payback.
**Common mistakes / traps:** Using only the marketing spend (Rs 2,400); counting signups instead of customers.

### Q15 ⭐⭐⭐ 🟢 A food delivery app had a GMV of Rs 45,00,000 from 18,000 orders in a week. What is the AOV?
**Asked at:** AOV questions appear in Swiggy prep guides (snippets, unverified).
**What the interviewer is checking:** The simple division and awareness of what GMV includes.
**Say this in the interview:** "AOV is GMV divided by orders: 45,00,000 / 18,000 = Rs 250."
**Definition in plain words:** Average order value = total order value (GMV) / number of orders.
**Worked answer:**
1. AOV = 45,00,000 / 18,000 = Rs 250 per order.
**Result:** AOV = Rs 250.
**Check:** 18,000 x 250 = 45,00,000. Verified by script.
**Caveats:** GMV (gross merchandise value) is the total value of orders placed, before discounts, cancellations or the app's share; check if cancelled orders are in GMV and whether delivery fees and taxes are included. AOV is not the app's revenue. A few large party orders can lift the average, so also look at the median.
**Likely follow-ups:** (1) If orders rise 10% at the same GMV? AOV falls to about Rs 227. (2) How do you raise AOV? Combos, add-ons, free-delivery thresholds.
**Common mistakes / traps:** Treating GMV as revenue; dividing by users rather than orders.

### Q16 ⭐⭐⭐ 🟢 An e-commerce site had 100,000 visits, 20,000 add-to-cart sessions, 6,000 checkout starts and 3,000 orders in a week. Find the step-wise conversion rates and the overall visit-to-order conversion rate.
**Asked at:** funnel and conversion analysis is described in the Guvi Flipkart write-up and prep banks (unverified).
**What the interviewer is checking:** Whether you use each step's own base and also the overall figure.
**Say this in the interview:** "Visit to cart 20%, cart to checkout 30%, checkout to order 50%, and overall 3% of visits end in an order."
**Definition in plain words:** Step conversion = people who reached the next step / people who reached this step. Overall conversion = final orders / first-step visits.
**Worked answer:**
1. Visit to add-to-cart = 20,000 / 100,000 = 20%.
2. Add-to-cart to checkout start = 6,000 / 20,000 = 30%.
3. Checkout start to order = 3,000 / 6,000 = 50%.
4. Overall = 3,000 / 100,000 = 3%. Also 0.20 x 0.30 x 0.50 = 0.03.
**Result:** 20%, 30%, 50% step-wise; 3% overall.
**Check:** The product of the step rates equals the overall rate. Verified by script.
**Caveats:** The data mixes units: visits, sessions and orders are not necessarily the same unit (one person can visit several times); state that. The biggest drop in share terms is visit to cart (80% lost), but the biggest fixable leak may be checkout (half of those who started do not finish); decide by effort and value, see Q29.
**Likely follow-ups:** (1) Which step first? Compare against benchmarks and consider the ease of a fix. (2) If checkout rises to 60%? Overall becomes 3.6%.
**Common mistakes / traps:** Dividing every step by the visits; reading 3% as poor without a comparison.

### Q17 ⭐⭐⭐ 🟢 A cohort of 1,000 users installed an app on Day 0. 400 opened it on Day 1, 220 on Day 7 and 120 on Day 30. What are the Day-1, Day-7 and Day-30 retention rates?
**Asked at:** retention calculations are a standard topic in the TechPrep and DataDriven prep banks (snippets, unverified).
**What the interviewer is checking:** Dividing by the original cohort every time.
**Say this in the interview:** "All three divide by the 1,000 who installed: 40%, 22% and 12%."
**Definition in plain words:** Day-N retention = users from the cohort active on Day N / users in the cohort.
**Worked answer:**
1. Day-1 = 400 / 1,000 = 40%.
2. Day-7 = 220 / 1,000 = 22%.
3. Day-30 = 120 / 1,000 = 12%.
**Result:** Day-1 40%, Day-7 22%, Day-30 12%.
**Check:** The curve is non-increasing, as expected in a classic definition; the fall from Day 7 to Day 30 (22% to 12%) is gentler per day than from Day 0 to Day 1. Verified by script.
**Caveats:** Always divide by the cohort, not the previous step (120/220 = 55% is "Day-7 to Day-30 survival", a different number). State whether the "classic" or "rolling" definition is used; the data suggests classic (active on exactly that day).
**Likely follow-ups:** (1) What would you do next? Compare cohorts by acquisition channel. (2) Is the 12% good? Depends on the app category.
**Common mistakes / traps:** Dividing by the Day-1 users; mixing classic and rolling retention.

### Q18 ⭐⭐⭐ 🟢 A company had 400 employees on 1 April and 360 on 31 March the next year, with 60 exits during the year. What is the annual attrition rate using average headcount?
**Asked at:** attrition formula (leavers / average headcount) appears in HR-analytics blogs such as Tutorialspoint and Deel; definitions vary (unverified for any company).
**What the interviewer is checking:** Average headcount in the denominator, plus noticing what the data implies about joiners.
**Say this in the interview:** "Average headcount is (400 + 360) / 2 = 380. Attrition is 60 / 380, about 15.8% for the year."
**Definition in plain words:** Attrition rate = employees who left in the period / average headcount in the period x 100.
**Worked answer:**
1. Average headcount = (400 + 360) / 2 = 380.
2. Attrition = 60 / 380 = 0.158 = 15.8%.
3. Implied hires: 400 - 60 + hires = 360, so hires = 20 (a derived figure; the question does not state it).
**Result:** Annual attrition about 15.8% (rounded).
**Check:** Using opening headcount instead: 60 / 400 = 15%; using closing: 60 / 360 = 16.7%. The average method sits between the two. Verified by script.
**Caveats:** Definitions vary: some firms use opening headcount or the average of twelve month-ends. Mention that the two-point average is a simplification. Separate voluntary (resignations) and involuntary exits, and consider excluding contract or retirement exits if the firm does. Note that the dates (1 April to 31 March) form one full year; the exit count of 60 should include only that year's leavers.
**Likely follow-ups:** (1) Monthly average? 15.8% / 12 is about 1.3%; for precision compute month by month. (2) What if no hires? Then closing would be 340, not 360, so some hiring happened.
**Common mistakes / traps:** Using closing headcount alone; forgetting that hires do not reduce attrition.

### Q19 ⭐⭐⭐ 🟡 An edtech app earns an ARPU of Rs 400 per month at a 60% gross margin, and monthly churn is 4%. What is the LTV per customer?
**Asked at:** LTV with margin and churn appears in Swiggy and SaaS prep guides (snippets, unverified).
**What the interviewer is checking:** Using margin, not revenue, and lifetime as 1/churn.
**Say this in the interview:** "Monthly gross profit per customer is 400 x 0.6 = Rs 240. Lifetime is 1/0.04 = 25 months. LTV = Rs 6,000."
**Definition in plain words:** LTV = ARPU x gross margin / monthly churn.
**Worked answer:**
1. Monthly gross profit = 400 x 60% = Rs 240.
2. Lifetime = 1 / 0.04 = 25 months.
3. LTV = 240 x 25 = Rs 6,000.
**Result:** LTV = Rs 6,000 per customer (margin basis). Revenue-basis LTV would be 400 x 25 = Rs 10,000.
**Check:** 240 / 0.04 = 6,000. Verified by script.
**Caveats:** Assumes constant churn and flat ARPU, with no discounting; it also treats the churn as the same for new and old customers. Say which version (revenue or margin) you quote; margin is the one that should be compared with CAC.
**Likely follow-ups:** (1) If churn drops to 3%? LTV = 240 / 0.03 = Rs 8,000. (2) Should you discount? A rough annual discount rate would lower it; mention but keep the simple formula first.
**Common mistakes / traps:** Quoting Rs 10,000 as LTV; using churn as 4 instead of 0.04.

### Q20 ⭐⭐⭐ 🟡 An edtech app has ARPU of Rs 400 per month, a 60% gross margin, 4% monthly churn and a CAC of Rs 1,800. What are the LTV:CAC ratio and the CAC payback period in months?
**Asked at:** CAC payback and LTV:CAC are SaaS analyst topics on Finalround AI and similar prep blogs (snippet, unverified); "3:1" is a rule of thumb, unverified.
**What the interviewer is checking:** Whether you can chain LTV, ratio and payback and interpret them.
**Say this in the interview:** "LTV is Rs 6,000, so LTV:CAC is 6,000 / 1,800 = 3.3. Payback is CAC divided by monthly gross profit: 1,800 / 240 = 7.5 months."
**Definition in plain words:** LTV:CAC = lifetime gross profit per customer / cost to acquire. CAC payback = months of gross profit needed to earn back the CAC.
**Worked answer:**
1. Monthly gross profit = 400 x 0.6 = Rs 240.
2. LTV = 240 / 0.04 = Rs 6,000.
3. LTV:CAC = 6,000 / 1,800 = 3.33.
4. Payback = 1,800 / 240 = 7.5 months.
**Result:** LTV:CAC about 3.3 to 1; payback 7.5 months.
**Check:** Over 7.5 months the cumulative gross profit is 7.5 x 240 = Rs 1,800. Verified by script.
**Caveats:** Simple payback ignores churn: with 4% monthly churn only about 74% of customers survive to month 7.5 (0.96^7.5), so the true payback of the average acquired customer is longer, which is why it is a first-pass figure. A common rule of thumb says LTV:CAC of 3 or more and payback under 12 months is healthy; these are rules of thumb, unverified, and vary by business and cash position.
**Likely follow-ups:** (1) What if CAC is Rs 3,000? Ratio 2.0, payback 12.5 months: weak. (2) Cash view? A long payback needs funding.
**Common mistakes / traps:** Using revenue in the payback; judging the ratio without checking payback; assuming LTV is certain.

### Q21 ⭐⭐⭐ 🟡 Which metrics would you track to judge the health of a food delivery app, and how would you organise them into a KPI tree?
**Asked at:** Swiggy business analyst guides mention CAC, retention, AOV and delivery time; KPI definition rounds are reported for Flipkart (prep-site and candidate claims, unverified).
**What the interviewer is checking:** Whether you build a structured, MECE tree (MECE = branches do not overlap and nothing is missing) and not a random list.
**Say this in the interview:** "I would start from one top outcome, profitable orders, and split it into demand, supply and unit economics, with quality as a guardrail."
**Clarify first:** Is the goal growth, profit or both? Which city or segment? Who owns each metric?
**Structure (KPI tree):**
- Top: Weekly gross profit (or contribution margin) from orders.
  - Demand: monthly active users x orders per user x AOV.
    - Acquisition: new users, CAC, install-to-first-order rate.
    - Engagement: DAU/MAU, orders per user, repeat rate, retention (Day-30, 90-day).
    - Basket: AOV, items per order.
  - Supply: active restaurants, delivery partners online, restaurant availability, partner utilisation.
  - Operations quality: delivery time, on-time rate, cancellation rate, order accuracy, refund rate, rating.
  - Unit economics: take rate (share of order value the app keeps), delivery cost per order, discount per order, contribution margin per order (money left per order after all costs that change with each order, see Q37).
**What I would check, in order:** (1) Top-line trend versus last week and last year. (2) Which branch of the tree moved, in a table by city. (3) A weekly Power BI or Excel dashboard with the tree as filters.
**If the data shows...:** Orders up but profit down: look at discounts and delivery cost. Users up, orders per user flat: acquisition without habit. Delivery time up and cancellations up: a supply problem.
**Recommendation:** Pick 5 to 7 headline KPIs (orders, AOV, retention, delivery time, contribution margin, cancellation) with owners and targets; keep the rest as diagnostic metrics.
**Likely follow-ups:** (1) North Star? Orders per active user per month, with a margin guardrail. (2) How would you measure quality of supply? Restaurant availability and rating.
**Common mistakes / traps:** A long unstructured list; mixing inputs and outcomes; no owners or guardrails.

### Q22 ⭐⭐⭐ 🟡 How would you choose a primary metric, supporting metrics and guardrail metrics for a newly launched feature, for example a "reorder in one tap" button on a food delivery app?
**Asked at:** primary versus supporting metrics and trade-offs is an Interview Query Flipkart guide topic, and the Tiger Analytics dashboard design question is similar (snippets, unverified).
**What the interviewer is checking:** Whether you link the metric to the feature's purpose and think of harm.
**Say this in the interview:** "The goal is making repeat ordering easier, so my primary metric is the share of eligible users who reorder within 14 days. Supporting metrics explain how; guardrails protect order quality and profit."
**Clarify first:** What problem does the feature solve (friction in repeat orders)? Who sees it? Is it an A/B test (the test design is in Book 5)? How long is the measurement window?
**Structure:**
- Primary: reorder rate = users who placed a repeat order / eligible users in the window. Alternative: orders per active user per week.
- Supporting (to understand the mechanism): button click rate, click-to-order conversion, time from open to order, share of orders via the button, new versus existing users.
- Guardrails: cancellation and refund rate (accidental taps), complaints, delivery time and profit per order (discounts), AOV (reorders may be smaller), and app crash rate.
**What I would check, in order:** (1) Eligible users and exposure definition. (2) Primary metric by cohort (exposed versus not). (3) Supporting funnel from click to order. (4) Guardrails against agreed limits.
**If the data shows...:** Primary up and guardrails flat: ship. Primary up but cancellations up: the one-tap design causes mistakes (add a confirmation step). Clicks high but orders flat: the button is noticed but trust or price is the barrier.
**Recommendation:** Ship if reorder rate improves by an agreed minimum with no guardrail breach; review again after four weeks to check the effect lasts and is not just a novelty.
**Likely follow-ups:** (1) Why not clicks? Clicks do not equal value. (2) Why a time window? It makes the rate comparable between groups.
**Common mistakes / traps:** Picking a metric the feature cannot move; skipping guardrails; measuring only short-term novelty.

### Q23 ⭐⭐⭐ 🟡 DAU on a ride-hailing app has been flat for three months while MAU has grown 20%. What does this tell you, and what would you check next?
**Asked at:** commonly asked (no company-specific report found); a DAU-versus-signups case type appears on prep sites (unverified).
**What the interviewer is checking:** Whether you read the DAU/MAU ratio (stickiness) and then split the problem into who is joining and how often they come back.
**Say this in the interview:** "DAU is daily active users, MAU is monthly active users. If MAU is up 20% and DAU is flat, the ratio DAU/MAU falls by about one sixth, so new users are arriving but not forming a habit. I would split by new versus existing users and by city."

**Clarify first:** How is "active" defined (app open, or a booked ride)? Is the 20% organic or from a campaign? Any seasonality, pricing or supply change in these three months?
**Structure:**
- Arithmetic: illustrative DAU 1,00,000 and MAU 4,00,000 gives 25%; MAU of 4,80,000 with the same DAU gives 20.8%.
- H1: growth came from low-intent users (promo-led, one-time riders).
- H2: existing riders ride less often (price rise, fewer drivers, long waits).
- H3: tracking or definition change inflated MAU.
**What I would check, in order:** (1) DAU/MAU trend by week; (2) MAU split into new, retained and reactivated users; (3) rides per active user per month; (4) cohort retention of the last three months' signups versus older ones; (5) cut by city, channel and device; (6) supply side (driver count, wait time, cancellations).
**If the data shows...:** New cohorts retain far worse, so the 20% is low-quality growth: fix acquisition and onboarding. Old users' frequency is falling, so it is a product or supply issue. One city or channel drives it, so the problem is local.
**Numeric work (if data given):** Ratio moves from 25.0% to 20.8%, a drop of about 4.2 points (about 17% relative). Verified by script (illustrative numbers).
**Recommendation:** Do not celebrate MAU. Report DAU/MAU and rides per user as guardrails, and review retention of new cohorts.
**Likely follow-ups:** Is a lower ratio always bad? No; if most riders use a ride-hailing app only a few times a month (an assumption, unverified), a ratio of 20-25% can be normal; the trend matters more than the level.
**Common mistakes / traps:** Calling flat DAU "no problem"; ignoring that DAU and MAU come from different user sets; not checking the definition of active.

### Q24 ⭐⭐⭐ 🟡 What are the limitations of using DAU/MAU as the single measure of engagement?
**Asked at:** commonly asked (no company-specific report found); DAU/MAU is described as heavily tested on prep sites (unverified).
**What the interviewer is checking:** Whether you know a ratio hides quality, product type and definition choices.
**Say this in the interview:** "DAU/MAU, called stickiness, is a quick health signal but a poor single number. It ignores depth of use, the natural frequency of the product, and how active is defined, so I pair it with retention and a value-action metric."

**Explain simply:**
- Stickiness = average daily active users divided by monthly active users. 20% means a typical monthly user shows up about 6 days a month.
- Product type matters: a payroll or leave app is used monthly by design; a messaging app daily. Comparing them is unfair.
- "Active" can be a mere app open or a real action (booking, payment). Loose definitions inflate it.
- It hides depth: a user who opens and leaves counts the same as a power user.
- It hides mix: new-user surges or heavy-user losses can leave the ratio unchanged.
- Monthly windows are slow and blur weekday or festival swings.
**Worked mini-example:** App A: DAU 20,000, MAU 1,00,000 = 20%. App B: same ratio, but A's users average 10 minutes per visit and B's 1 minute. Same ratio, very different engagement.
**Practice step:** Take any app you use; write what "active" would mean, and one second metric that proves value.
**Likely follow-ups:** What would you add? Retention curves, sessions or core actions per active user, and time to first value.
**Common mistakes / traps:** Quoting a benchmark such as "above 50% is good" as a law; comparing across product types; ignoring the definition.

### Q25 ⭐⭐⭐ 🟡 A product manager says "our conversion rate went up from 3% to 4%." What questions do you ask before accepting this as good news?
**Asked at:** commonly asked (no company-specific report found); conversion and funnel interpretation appears in Flipkart-related prep guides (unverified).
**What the interviewer is checking:** Whether you test the definition, the denominator, the sample size and the guardrails before applauding.
**Say this in the interview:** "A move from 3% to 4% is one point, or 33% relative. I would first confirm what is being counted and out of whom, whether it is statistically real, and whether anything else got worse, such as returns, refunds or order value."

**Clarify first:** Conversion of what (visit to order, signup to first purchase)? Same definition and period in both readings? Over how many sessions?
**Structure:**
- Definition: numerator and denominator unchanged? Bots, internal traffic, repeat sessions?
- Mix: did traffic shift to high-intent channels (for example more returning users)? Check each segment.
- Statistical: with 1,000 visits, 30 versus 40 orders is noisy; with 1,00,000 it is solid.
- Quality: average order value, returns, cancellations, discount depth, margin per order.
- Cause: promo, price cut, seasonality, a test result?
**What I would check, in order:** (1) the definition and query; (2) conversion by channel, device and new versus returning; (3) volume and a confidence interval (a range showing how much the rate could move by chance); (4) revenue and margin per visitor; (5) timing against launches.
**If the data shows...:** Every segment up, with order value stable: real gain. Only the traffic mix changed (a Simpson's paradox style effect: a total moves because the mix of groups changed, not because any group improved): no true improvement. Conversion up from heavy discounts and margin down: a trade, not a win.
**Numeric work (if data given):** 3% to 4% is +1 percentage point, +33.3% relative. Verified by script.
**Recommendation:** Accept only after segment, significance and margin checks; track revenue per visitor as the primary metric.
**Likely follow-ups:** Could fewer visitors raise the rate? Yes, if low-intent traffic was cut; total orders may have fallen.
**Common mistakes / traps:** Mixing percentage points with percent; ignoring sample size; judging a rate without volume.

### Q26 ⭐⭐⭐ 🟡 How do you define and track churn for a product where users do not formally cancel (for example a food delivery or a shopping app)?
**Asked at:** commonly asked (no company-specific report found); churn and retention are named in Swiggy business analyst guides (prep sites, unverified).
**What the interviewer is checking:** Whether you can build an inactivity-based definition from the product's natural buying cycle.
**Say this in the interview:** "With no cancel button, churn is silent. I define a user as churned when they pass a gap longer than their normal buying rhythm, say 60 days without an order for a food app, picked from the data, then track it by cohort."

**Explain simply:**
- This is "non-contractual" churn (no subscription), so we infer it from behaviour.
- Pick the window from data: look at the gap between consecutive orders; choose a point such as the 90th percentile of gaps (the gap that 90% of gaps stay under), so most active customers are not wrongly flagged.
- Window differs by product: food delivery weeks, groceries a few weeks, fashion months.
- Label users as active, at risk (gap past usual) and churned; allow reactivation, so churn is a status, not forever.
- Track: monthly churn = users active last period but not this period, over last period's actives; and cohort retention.
**Worked mini-example:** Median gap between orders is 9 days and 90% of gaps are under 45 days, so choose 45 days. A customer last ordering on 1 Sept is counted churned from 16 Oct. (Illustrative numbers.)
**Practice step:** In a sample orders table, compute gaps per customer with LAG() (a SQL function that looks at the previous row, here the previous order date) and read the percentiles.
**Likely follow-ups:** Why not 30 days for everything? Seasonal or occasional buyers would be mislabelled as churned.
**Common mistakes / traps:** One window for all products; treating churned as permanent; forgetting reactivation.

### Q27 ⭐⭐⭐ 🟡 What is a cohort retention table, and how do you read one?
**Asked at:** commonly asked (no company-specific report found); cohort and retention questions are listed on TechPrep and DataDriven (prep sites, unverified).
**What the interviewer is checking:** Whether you can build and interpret the triangle of cohorts against time.
**Say this in the interview:** "A cohort is a group of users who started in the same period. The table has one row per cohort, one column per month since start, and each cell shows the share still active. I read down columns to compare cohorts and across rows to see the curve flatten."

**Explain simply:**
- Row = signup month; column = months since signup (Month 0 is 100%).
- Reading across: the fall-off shape. A curve that flattens means a loyal core; one that keeps dropping means a leaky product.
- Reading down a column: are newer cohorts better than older ones at the same age? That shows whether changes helped.
- Reading the diagonal: shows calendar events such as a festival or an outage affecting all cohorts together.
- It is a triangle because recent cohorts have not aged yet.
**Worked mini-example:** Jan cohort 1,000 users: M0 100%, M1 40% (400), M2 30%, M3 28%. Feb cohort: M0 100%, M1 46%. Feb is better at the same age, so something improved. (Illustrative.)
**Practice step:** Build it in Excel with a pivot of cohort month by months since signup, divided by the cohort size.
**Likely follow-ups:** Classic versus rolling retention? Classic counts only exactly on day N; rolling counts on or after day N.
**Common mistakes / traps:** Comparing cohorts of different ages; averaging across cohorts of unequal size; judging recent cells that are incomplete.

### Q28 ⭐⭐⭐ 🟡 A company reports that its overall retention improved this quarter. How could this be a mix-shift illusion rather than a real improvement (Simpson's paradox style)?
**Asked at:** commonly asked (no company-specific report found); a gap-fill question (see the sources file).
**What the interviewer is checking:** Whether you know that an overall average can rise when every segment falls, purely because of changed mix.
**Say this in the interview:** "Overall retention is a weighted average of segment retentions. If the share of users shifts toward a high-retention segment, the total goes up even if each segment got slightly worse. I would check retention by segment with fixed weights."

**Clarify first:** Which segments exist (city tier, channel, plan, tenure)? Did the user mix change?
**Structure:** Overall = sum of (segment share x segment retention). Change in overall = effect of mix + effect of true within-segment change.
**What I would check, in order:** (1) retention per segment, both quarters; (2) segment shares both quarters; (3) overall retention recomputed with last quarter's shares; (4) tenure mix (older users retain better).
**If the data shows...:** Segments flat or down, but overall up: mix illusion. Segments up: real improvement.
**Numeric work (if data given):** Illustrative: Quarter 1, metro 200 users at 60%, small town 800 at 30%: overall 36%. Quarter 2, metro 600 at 58%, small town 400 at 28%: overall 46%. Overall is up 10 points while both segments fell 2 points. With Q1 weights, Q2 retention is 0.2 x 58% + 0.8 x 28% = 34%, so a real decline of 2 points. Verified by script.
**Recommendation:** Report segment-level and mix-adjusted retention beside the headline.
**Likely follow-ups:** Which number is true? Both are arithmetically right; the segment view answers "did our product improve."
**Common mistakes / traps:** Trusting a blended rate; forgetting tenure mix; not fixing weights.

### Q29 ⭐⭐⭐ 🟡 What is the funnel view of conversion, and how do you find which step to fix first?
**Asked at:** commonly asked; funnel breakdown and conversion questions are reported in Flipkart-related prep guides (unverified).
**What the interviewer is checking:** Whether you can turn a journey into step conversion and prioritise by impact, not just by lowest rate.
**Say this in the interview:** "A funnel lists the steps from visit to purchase and the share who pass each one. I compute step-to-step conversion, find the largest absolute loss, then judge how fixable it is and what lifting it adds to final orders."

**Explain simply:**
- Step conversion = users at this step divided by users at the previous step. Overall conversion = last step over first.
- Big drop does not always mean fix first: a step may be naturally leaky (browsing) or hard to change.
- Prioritise by: size of loss (users), effort and evidence of a cause (error rates, page speed, drop by device).
**Worked mini-example:** 10,000 visits, 5,000 view product (50%), 2,000 add to cart (40%), 1,000 start checkout (50%), 600 pay (60%). Overall 6%. Lifting add-to-cart from 40% to 44% gives 2,200 carts and 660 orders (+60, +10%); lifting payment from 60% to 66% also gives 660. Equal effect, so pick the one cheaper to fix. Verified by script (illustrative).
**Practice step:** Segment the funnel by device and channel; a mobile-only drop points to a UX bug.
**Likely follow-ups:** Order matters? Multiplying rates means a relative lift anywhere equals the same overall lift.
**Common mistakes / traps:** Fixing the lowest rate without checking feasibility; ignoring that steps are sequential; mixing sessions and users.

### Q30 ⭐⭐ 🟢 What is gross merchandise value (GMV), and how is it different from revenue for a marketplace?
**Asked at:** commonly asked (no company-specific report found); GMV and revenue appear in marketplace prep material (unverified).
**What the interviewer is checking:** Whether you separate the value of goods sold from what the platform earns.
**Say this in the interview:** "GMV is the total value of goods sold through the platform. The marketplace only keeps its commission and fees, so revenue is a fraction of GMV, called the take rate."

**Explain simply:**
- GMV = number of orders x average order value (before returns and cancellations in most definitions).
- Revenue = commission + fees + ads, what the platform actually earns.
- Take rate = revenue / GMV.
**Worked mini-example:** 1,00,000 orders at Rs 500 = GMV Rs 5 crore. At a 10% take rate, revenue is Rs 50 lakh. Verified by script (illustrative).
**Practice step:** Ask which of the two a company reports and whether GMV is net of returns.
**Likely follow-ups:** Why can GMV mislead? Heavy discounts can raise GMV while profit falls.
**Common mistakes / traps:** Calling GMV revenue; ignoring cancellations and returns; ignoring that a first-party retailer books full sales as revenue.

### Q31 ⭐⭐ 🟢 What is the difference between a leading and a lagging indicator? Give one example of each for an e-commerce business.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand early warning versus final outcome.
**Say this in the interview:** "A lagging indicator reports an outcome that already happened, like monthly revenue. A leading indicator moves first and predicts it, like add-to-cart rate or repeat visits this week."

**Explain simply:**
- Lagging: confirms results, hard to change now (revenue, churn, profit).
- Leading: early signal you can act on (new-user first-week activity, search-to-cart rate, delivery delays).
- HR parallel: attrition is lagging; falling engagement scores and rising absenteeism are leading.
- Good practice: pair each lagging goal with 1-2 leading metrics, and confirm the link with data.
**Worked mini-example:** Add-to-cart rate drops from 8% to 6% this week; month-end revenue will likely fall, but you learn it weeks earlier.
**Likely follow-ups:** How check the link? Plot the leading metric against later revenue, with a lag.
**Common mistakes / traps:** Assuming any early metric predicts the outcome; vanity metrics.

### Q32 ⭐⭐ 🟢 What are monthly recurring revenue (MRR) and annual recurring revenue (ARR), and what is ARR for a SaaS company with 200 customers each paying Rs 50,000 per month?
**Asked at:** commonly asked; MRR/ARR is a listed SaaS analyst topic on a prep blog (unverified).
**What the interviewer is checking:** Whether you can compute recurring revenue and exclude one-time items.
**Say this in the interview:** "MRR is predictable subscription revenue for a month; ARR is MRR times 12. Here MRR is 200 x Rs 50,000 = Rs 1 crore, so ARR is Rs 12 crore."

**Definition in plain words:** MRR = sum of monthly subscription fees from active customers. ARR = MRR x 12.
**Worked answer:** 1) MRR = 200 x 50,000 = Rs 1,00,00,000 (Rs 1 crore). 2) ARR = 1 crore x 12 = Rs 12 crore.
**Result:** MRR Rs 1 crore; ARR Rs 12 crore. Verified by script.
**Check:** 200 x 6,00,000 per year = Rs 12,00,00,000, same.
**Caveats:** Exclude one-time setup or consulting fees; annual contracts are divided by 12 for MRR; ARR is a run-rate, not booked cash.
**Likely follow-ups:** If 10 customers leave? MRR falls by Rs 5 lakh; ARR by Rs 60 lakh.
**Common mistakes / traps:** Adding one-time fees; multiplying a single bumper month by 12.

### Q33 ⭐⭐ 🟢 What is net promoter score (NPS), and how is it calculated from survey responses?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know the three groups and the subtraction.
**Say this in the interview:** "NPS comes from one question: how likely are you to recommend us, 0 to 10? Scores 9-10 are promoters, 7-8 passives, 0-6 detractors. NPS = % promoters minus % detractors, a number from -100 to +100."

**Definition in plain words:** NPS = (promoters / total) x 100 minus (detractors / total) x 100. Passives count in the total only.
**Worked answer:** Of 100 responses with 60 promoters, 25 passives and 15 detractors: 60 - 15 = NPS 45.
**Result:** Reported as a whole number, not a percent sign.
**Check:** All promoters give +100; all detractors -100.
**Caveats:** Response bias, small samples, cultural scoring differences, and NPS does not say why people feel as they do; add a comment question.
**Likely follow-ups:** Is 45 good? It depends on industry and trend; I would compare to own history.
**Common mistakes / traps:** Subtracting counts instead of percentages; leaving passives out of the denominator.

### Q34 ⭐⭐ 🟢 A survey of 200 customers gave 110 promoters (score 9-10), 50 passives (7-8) and 40 detractors (0-6). What is the NPS?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Correct arithmetic with the right denominator.
**Say this in the interview:** "Promoters are 55% and detractors 20% of 200, so NPS is 55 minus 20, which is 35."

**Definition in plain words:** NPS = % promoters minus % detractors.
**Worked answer:** 1) Total = 110 + 50 + 40 = 200 (matches). 2) Promoters = 110/200 = 55%. 3) Detractors = 40/200 = 20%. 4) NPS = 55 - 20 = 35.
**Result:** NPS = +35.
**Check:** (110 - 40)/200 = 70/200 = 0.35. Verified by script.
**Caveats:** Passives (25%) do not appear in the formula, but sit in the denominator. A margin of error exists with 200 respondents.
**Likely follow-ups:** What if 10 passives become promoters? Promoters become 120/200 = 60%, detractors stay 20%, so NPS = 40 (up 5 points).
**Common mistakes / traps:** Reporting 35%; dividing by 150 (leaving out passives) instead of 200.

### Q35 ⭐⭐ 🟢 What is cart abandonment rate? A site had 8,000 carts created and 2,000 orders completed; what is the abandonment rate?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Formula and a sensible reading.
**Say this in the interview:** "Abandonment rate is the share of carts that never turn into an order. Here 6,000 of 8,000 carts were abandoned, so 75%."

**Definition in plain words:** Abandonment rate = (carts created minus orders completed) / carts created, or 1 minus the checkout completion rate.
**Worked answer:** 1) Abandoned = 8,000 - 2,000 = 6,000. 2) Rate = 6,000 / 8,000 = 75%. 3) Completion rate = 2,000/8,000 = 25%.
**Result:** 75% abandonment.
**Check:** 75% + 25% = 100%. Verified by script.
**Caveats:** Carts are often used as a wish-list, so some "abandonment" is normal; count unique carts or sessions consistently; separate by step (shipping cost shown, payment failure).
**Likely follow-ups:** How cut it? Find the step with the biggest drop, then test fixes like showing delivery cost earlier.
**Common mistakes / traps:** Dividing by orders; counting multiple carts by one user as separate events.

### Q36 ⭐⭐ 🟢 What is the difference between customer churn and user inactivity (dormancy)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you see churn as a decision and dormancy as a behaviour state.
**Say this in the interview:** "Churn means the customer has left, formally or by our rule. Dormancy means they are quiet for now but could return. I track dormant users as at risk and win-back targets before calling them churned."

**Explain simply:**
- Churn: an end of relationship (cancelled, uninstalled, or past the long inactivity cut-off).
- Dormant: no activity in a short window, still reachable (app installed, push on).
- A dormant user may be a loyal occasional buyer; a churned one needs reacquiring, which costs more.
- Action: dormancy triggers reminders; churn triggers win-back offers and analysis.
**Worked mini-example:** Rule: no order in 30 days = dormant, 90 days = churned. A customer last ordering 45 days ago is dormant.
**Likely follow-ups:** Can a churned user return? Yes, that is reactivation, counted separately.
**Common mistakes / traps:** Using one threshold for both; counting dormant users as lost in revenue forecasts.

### Q37 ⭐⭐ 🟢 What is gross margin and contribution margin per order for a food delivery company, and why do analysts prefer contribution margin?
**Asked at:** commonly asked; unit economics (AOV, LTV) appear in Swiggy guides (prep sites, unverified).
**What the interviewer is checking:** Whether you can build per-order economics and know which costs vary with each order.
**Say this in the interview:** "Gross margin is revenue minus direct cost of serving the order, mainly delivery. Contribution margin goes further and subtracts all other costs that change with each order, like discounts and payment fees, so it shows whether one more order makes or loses money."

**Explain simply (illustrative numbers, assumed):**
- Order value Rs 400. Platform revenue per order: commission Rs 80 + delivery fee Rs 30 + ads Rs 10 = Rs 120.
- Delivery partner cost Rs 60, so gross margin = 120 - 60 = Rs 60 (50% of revenue).
- Less discounts Rs 25, payment fees Rs 5, support Rs 5 = Rs 35, so contribution margin = 60 - 35 = Rs 25 per order (about 21% of revenue, 6% of order value).
- Analysts prefer contribution margin because it leaves out fixed costs (tech team, office) yet keeps everything that scales with orders, so it guides discounts and pricing.
**Practice step:** Build the waterfall of revenue to contribution per order in a sheet, then see what happens at a bigger discount.
**Likely follow-ups:** Why not net profit? Fixed costs are spread over volume, so it hides the per-order story.
**Common mistakes / traps:** Counting full order value as revenue; leaving discounts out; mixing fixed and variable costs. Verified by script.

### Q38 ⭐⭐ 🟢 What is an acquisition-to-activation funnel for a fintech app, and what could be a sensible activation event?
**Asked at:** commonly asked; PhonePe and fintech KPI rounds are mentioned in internal notes (unverified mapping).
**What the interviewer is checking:** Whether you can pick an activation event tied to real value, not a vanity step.
**Say this in the interview:** "The funnel runs from install to registration, KYC (identity check), linking a bank account, and then a first real transaction. Activation should be the moment a user gets value, so I would pick first successful payment within 7 days of install."

**Explain simply:**
- Acquisition: install or signup, from ads, referrals, organic.
- Steps: install, signup (OTP), KYC complete, bank linked, first transaction.
- Activation event = the action that best predicts long-term retention; test candidates with cohort data (users who did X in week 1 retain at Y).
- Better than "registered," since many registered users never transact.
**Worked mini-example:** 10,000 installs, 6,000 registered, 3,000 KYC done, 2,000 first payment. Activation = 2,000/10,000 = 20%. Step rates: 60%, 50%, 67%, so the weakest step is registration to KYC (50%), while the largest loss in users is install to registration (4,000). (Illustrative.)
**Likely follow-ups:** How check the event is right? Compare 30-day retention of users who did it versus those who did not.
**Common mistakes / traps:** Choosing signup as activation; no time window; ignoring fraud and KYC rejections.

### Q39 ⭐⭐ 🟢 What is the repeat purchase rate? Of 10,000 customers who ordered in January, 3,200 ordered again in February. What is the repeat rate?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Formula, a fixed window and the correct base.
**Say this in the interview:** "Repeat rate is the share of customers who buy again within a defined period. Here 3,200 out of 10,000 January customers ordered in February, so 32%."

**Definition in plain words:** Repeat rate = customers who bought again in the window / customers in the starting group.
**Worked answer:** 3,200 / 10,000 = 0.32 = 32%.
**Result:** 32% one-month repeat rate.
**Check:** 32% repeat means 68% (6,800) did not return in February. Verified by script.
**Caveats:** The window matters (30 days versus calendar February); some define repeat over all customers who ordered more than once; new February customers are not part of the base.
**Likely follow-ups:** Is 32% good? Compare to history and category; grocery is higher than fashion.
**Common mistakes / traps:** Dividing by February's total customers; mixing windows.

### Q40 ⭐⭐ 🟢 What is employee attrition rate, and what is the difference between voluntary and involuntary attrition?
**Asked at:** commonly asked; formulas from HR-analytics prep sites (unverified, definitions vary).
**What the interviewer is checking:** Formula with average headcount, and the HR meaning of the two types.
**Say this in the interview:** "Attrition rate is leavers in a period divided by average headcount. Voluntary is the employee's choice, such as resignation; involuntary is the company's choice, such as termination or layoff."

**Definition in plain words:** Attrition rate = employees who left / average headcount x 100, where average headcount = (opening + closing) / 2.
**Worked answer (illustrative):** Opening 100, closing 108, 12 left. Average = 104. Rate = 12/104 = 11.5% for the period. Of the 12, 8 resigned (voluntary, 7.7%) and 4 were terminated (involuntary, 3.8%).
**Result:** 11.5% total; 7.7% voluntary; 3.8% involuntary. Verified by script.
**Check:** 7.7 + 3.8 = 11.5. To annualise a monthly rate, multiply by 12 as an approximation.
**Caveats:** Retirements, transfers and contract ends are classified differently; some firms use opening headcount; regretted attrition (loss of top performers) matters more than the total.
**Likely follow-ups:** Which one worries you more? Voluntary, since it is preventable; I would slice by tenure, manager and team.
**Common mistakes / traps:** Using closing headcount only; mixing monthly and annual rates; counting transfers as leavers.

### Q41 ⭐⭐ 🟢 What is a hiring funnel conversion rate? Out of 1,200 applications, 300 were screened in, 90 interviewed, 30 offered and 21 joined. Find the stage-wise and overall conversion.
**Asked at:** commonly asked; hiring funnel metrics appear on HR-analytics prep sites (unverified).
**What the interviewer is checking:** Step-wise division and the overall product.
**Say this in the interview:** "Each stage's conversion is that stage divided by the one before. Screening is 25%, interview 30%, offer 33%, joining 70%, and overall 21 out of 1,200 is 1.75%."

**Definition in plain words:** Stage conversion = people at this stage / people at the previous stage. Overall = joined / applications.
**Worked answer:** 1) Screened: 300/1,200 = 25%. 2) Interviewed: 90/300 = 30%. 3) Offered: 30/90 = 33.3%. 4) Joined (offer acceptance): 21/30 = 70%. 5) Overall: 21/1,200 = 1.75%.
**Result:** 25%, 30%, 33.3%, 70%; overall 1.75% (about 57 applications per hire).
**Check:** 0.25 x 0.30 x 0.333 x 0.70 = 0.0175. Verified by script.
**Caveats:** Time lags (people still in the pipeline); source quality; offer acceptance is 70%, so 30% of offers are declined, which suggests checking pay and the process.
**Likely follow-ups:** Which stage to fix? The 30% offer decline is costly late; also look at source-wise quality.
**Common mistakes / traps:** Dividing every stage by applications; ignoring time to hire.

### Q42 ⭐⭐ 🟡 A quick-commerce app has 2,50,000 customers at the start of a month. 40,000 new customers join and 30,000 leave during the month. What are the closing customers, the monthly net growth rate and the churn rate on the opening base?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Roll-forward arithmetic and the correct opening-base denominator.
**Say this in the interview:** "Closing = opening plus new minus lost = 2,60,000. Net growth is 10,000 on 2,50,000, which is 4%. Churn on the opening base is 30,000/2,50,000 = 12%."

**Definition in plain words:** Closing = opening + new - churned. Net growth = (closing - opening) / opening. Churn rate = churned / opening.
**Worked answer:** 1) 2,50,000 + 40,000 - 30,000 = 2,60,000. 2) Net growth = 10,000/2,50,000 = 4%. 3) Churn = 30,000/2,50,000 = 12%.
**Result:** Closing 2,60,000; net growth 4%; churn 12%. Verified by script.
**Check:** Gross adds are 16%; 16% - 12% = 4%.
**Caveats:** Some new customers may leave in the same month (they are not in the opening base); 12% a month is very high, so I would check the definition of "leave."
**Likely follow-ups:** Annualised? Not simply 12 x 4%; it compounds to about 60% if sustained (1.04^12 = 1.60).
**Common mistakes / traps:** Using closing or average base without saying so; confusing net growth with churn.

### Q43 ⭐⭐ 🟡 A SaaS company has MRR of Rs 50,00,000 at the start of the month. During the month: new MRR Rs 6,00,000, expansion MRR Rs 2,00,000, churned MRR Rs 3,00,000, contraction Rs 1,00,000. Find the closing MRR, gross revenue retention and net revenue retention for the month.
**Asked at:** commonly asked; MRR, NRR and churn are listed SaaS analyst topics on a prep blog (unverified).
**What the interviewer is checking:** Whether you exclude new revenue from retention and keep expansion only in NRR.
**Say this in the interview:** "Closing MRR is 54 lakh. Gross revenue retention counts only losses, so 46/50 = 92%. Net revenue retention adds expansion, 48/50 = 96%. Neither includes new customers."

**Definition in plain words:** MRR is monthly recurring revenue (subscription fees that repeat every month). Churned MRR is revenue lost from customers who cancelled; contraction is revenue lost from customers who downgraded; expansion is extra revenue from existing customers who upgraded. GRR (gross revenue retention) = (opening - churned - contraction) / opening. NRR (net revenue retention) = (opening + expansion - churned - contraction) / opening.
**Worked answer:** 1) Closing = 50 + 6 + 2 - 3 - 1 = Rs 54,00,000. 2) GRR = (50 - 3 - 1)/50 = 46/50 = 92%. 3) NRR = (50 + 2 - 3 - 1)/50 = 48/50 = 96%.
**Result:** Closing MRR Rs 54,00,000 (8% growth); GRR 92%; NRR 96%.
**Check:** GRR cannot exceed 100%; NRR below 100% means the existing base shrank even though total MRR grew from new sales. Verified by script.
**Caveats:** Monthly versus annual windows (monthly 96% compounds to about 61% yearly); definitions vary on reactivations.
**Likely follow-ups:** What does NRR 96% tell you? Growth relies on new sales; fix churn or upsell.
**Common mistakes / traps:** Including new MRR in NRR; allowing GRR to include expansion.

### Q44 ⭐⭐ 🟡 A subscription app has 10,000 subscribers at Rs 200 per month. Monthly churn is 5% and it adds 600 new subscribers each month. What level does the subscriber base stabilise at, and what is the base at the end of the first month?
Use the steady-state idea: base is stable when monthly churned users equal monthly new users.
**Asked at:** commonly asked (gap-fill pattern per the sources file; no company-specific report found).
**What the interviewer is checking:** Whether you can set churned = new and solve, and roll forward one step.
**Say this in the interview:** "The base is stable when 5% of it equals 600, so base = 600/0.05 = 12,000. After month one: 10,000 minus 500 churned plus 600 new gives 10,100."

**Definition in plain words:** Next base = current base x (1 - churn) + new adds. Steady state: churn x base = new adds.
**Worked answer:** 1) Month 1: churned = 5% x 10,000 = 500; closing = 10,000 - 500 + 600 = 10,100. 2) Steady state: 0.05 x S = 600, so S = 12,000. 3) Monthly revenue at steady state = 12,000 x Rs 200 = Rs 24,00,000 (now: Rs 20,00,000).
**Result:** First-month base 10,100 (revenue Rs 20,20,000); stable base 12,000.
**Check:** At 12,000, churn = 600 = adds, so no change. The gap to 12,000 shrinks by 5% each month (2,000 to 1,900); after 12 months the base is about 10,919. Verified by script.
**Caveats:** Assumes constant churn and adds; real churn is higher among new subscribers; the approach takes years to near steady state.
**Likely follow-ups:** How to raise the ceiling? Cut churn (at 4%, the base stabilises at 15,000) or add more subscribers.
**Common mistakes / traps:** Applying churn after adding new users; forgetting the gradual approach.

### Q45 ⭐⭐ 🟡 A ride-hailing app has an average fare of Rs 180, a take rate (commission) of 20%, and a driver incentive plus rider promo cost of Rs 14 per ride. What is the contribution per ride, and what happens at 10% promo growth?
Treat Rs 14 as the only variable cost and ignore taxes and payment fees. For the second part, raise the Rs 14 by 10%.
**Asked at:** commonly asked (no company-specific report found); unit-economics questions are a standard product/business analyst topic (prep sites, unverified).
**What the interviewer is checking:** Whether you start from the app's own revenue (the commission), not the full fare.
**Say this in the interview:** "The app keeps only its commission, Rs 36, so contribution is Rs 36 minus Rs 14 = Rs 22 per ride. If promo cost rises 10% to Rs 15.40, contribution falls to Rs 20.60, about 6.4% lower."
**Definition in plain words:** Take rate is the share of the fare the platform keeps. Contribution per ride is the money left from one ride after the variable costs of that ride: commission minus incentive and promo cost.
**Worked answer:**
1. Platform revenue per ride = 20% x Rs 180 = Rs 36 (the other Rs 144 goes to the driver).
2. Contribution = Rs 36 - Rs 14 = Rs 22 per ride.
3. Promo up 10%: Rs 14 x 1.10 = Rs 15.40.
4. New contribution = Rs 36 - Rs 15.40 = Rs 20.60.
**Result:** Rs 22 per ride now; Rs 20.60 after the promo rise. That is a drop of Rs 1.40, or 6.4% (1.40 / 22). As a share of the fare: 12.2% before, 11.4% after (rounded).
**Check:** A 10% rise in a Rs 14 cost is Rs 1.40, and it comes straight off contribution. Because the cost is large relative to the contribution (14 / 22), a 10% cost rise causes a smaller-than-expected 6.4% fall, not 10%.
**Caveats:** Using the full Rs 180 as "revenue" is wrong; it is gross booking value (GMV), not revenue. Real apps also have fixed costs, taxes and payment fees, ignored here as told.
**Likely follow-ups:** 1) *How many rides to cover Rs 11 lakh of fixed monthly cost?* 11,00,000 / 22 = 50,000 rides. 2) *What promo level gives zero contribution?* Rs 36 per ride.
**Common mistakes / traps:** Subtracting the Rs 14 from the Rs 180 fare; applying 10% to the contribution instead of to the cost.

### Q46 ⭐⭐ 🟡 A UPI payments app has 20 million monthly active users who made 300 million successful transactions out of 320 million attempts in a month. What are the success rate and the transactions per active user?
**Asked at:** commonly asked (no company-specific report found); a PhonePe prep guide mentions funnel metrics (see research/interview_processes.md, unverified); this exact question is unverified.
**What the interviewer is checking:** Whether you pick the right denominator for each ratio.
**Say this in the interview:** "Success rate is successful divided by attempted: 300/320 = 93.75%. Transactions per active user is 300 million / 20 million = 15 a month."
**Definition in plain words:** Success rate = successful transactions / attempted transactions. Transactions per active user = successful transactions / monthly active users (MAU, people who did at least one action in the month).
**Worked answer:**
1. Success rate = 300 / 320 = 0.9375 = 93.75%.
2. Failed attempts = 320 - 300 = 20 million (6.25%).
3. Transactions per user = 300 million / 20 million = 15.
4. For comparison, attempts per user = 320 / 20 = 16.
**Result:** 93.75% success rate; 15 successful transactions per active user per month.
**Check:** 15 x 20 million = 300 million, which matches. Success rate must be at most 100%, and it is.
**Caveats:** Some failed attempts are retries by the same person, so 20 million failures is not 20 million unhappy users. Also split failures by reason (bank down, wrong PIN, user cancelled), because only technical failures count against the platform. The average of 15 hides a skew: a few heavy users and many light ones, so also show the median.
**Likely follow-ups:** 1) *Which is better, a 94% success rate with retries or a 90% rate without?* Compare success per user journey, not per attempt. 2) *Would you count only users who paid?* Define "active" first.
**Common mistakes / traps:** Dividing successes by MAU for the success rate; mixing attempts and successes in one ratio.

### Q47 ⭐⭐ 🟡 An online store has 5,000 first-time buyers in January. Their retention is 30% in month 1 and 20% in month 2 (of the original 5,000). Each active buyer places 1 order of Rs 600 per month with a 25% margin. What is the margin earned from this cohort in months 0, 1 and 2, assuming month 0 orders are 1 per buyer?
**Asked at:** commonly asked (no company-specific report found); cohort and retention questions are heavily named in prep sites (unverified).
**What the interviewer is checking:** Whether you apply retention to the original cohort size and then margin to revenue.
**Say this in the interview:** "Active buyers are 5,000, 1,500 and 1,000. Margin per buyer is Rs 150, so the cohort earns Rs 7,50,000, Rs 2,25,000 and Rs 1,50,000, Rs 11,25,000 in total."
**Definition in plain words:** A cohort is a group of customers who started in the same period. Retention % is the share of the original group still buying. Margin = order value x margin %.
**Worked answer:**
1. Margin per order = 25% x Rs 600 = Rs 150.
2. Month 0: 5,000 buyers x Rs 150 = Rs 7,50,000.
3. Month 1: 30% x 5,000 = 1,500 buyers x Rs 150 = Rs 2,25,000.
4. Month 2: 20% x 5,000 = 1,000 buyers x Rs 150 = Rs 1,50,000.
**Result:** Rs 7,50,000, Rs 2,25,000, Rs 1,50,000; cumulative Rs 11,25,000 over three months (Rs 225 per original buyer).
**Check:** Revenue = (5,000 + 1,500 + 1,000) x 600 = Rs 45,00,000; 25% of that = Rs 11,25,000. Matches.
**Caveats:** Retention here is "share of the original 5,000", not of the previous month (month 2 is 20/30 = 67% of month-1 buyers). Margin ignores acquisition cost; if CAC were Rs 300 per buyer, the cohort has not yet paid back (Rs 225 per buyer earned so far).
**Likely follow-ups:** 1) *Does the cohort pay back a Rs 200 CAC per buyer?* Cumulative margin per buyer is Rs 150, Rs 195, Rs 225, so payback happens in month 2. 2) *What if retention keeps at 20%?* Add Rs 1,50,000 a month.
**Common mistakes / traps:** Applying 20% to the month-1 buyers (giving 300); forgetting month 0 revenue.

### Q48 ⭐⭐ 🟡 An app's blended CAC is Rs 400. Paid channels have a CAC of Rs 700 and organic installs cost Rs 0. If 1,000 customers were acquired in total, how many came from paid channels, and what is the marketing spend?
Assume the blended CAC includes only paid marketing spend divided by all new customers.
**Asked at:** commonly asked (no company-specific report found); Swiggy business analyst guides mention CAC (prep sites, unverified).
**What the interviewer is checking:** Whether you work backwards from total spend, not from the CAC figures directly.
**Say this in the interview:** "Spend = blended CAC x all customers = Rs 4,00,000. Paid customers = 4,00,000 / 700, about 571, so roughly 57% were paid and 429 were organic."
**Definition in plain words:** Blended CAC = total acquisition spend / all new customers (paid plus organic). Paid CAC = paid spend / paid customers only.
**Worked answer:**
1. Total spend = Rs 400 x 1,000 = Rs 4,00,000 (all spend is paid, by the stated assumption).
2. Paid customers = Rs 4,00,000 / Rs 700 = 571.4, so about 571.
3. Organic customers = 1,000 - 571 = about 429.
**Result:** About 571 paid customers (57%), about 429 organic; marketing spend Rs 4,00,000.
**Check:** Blended is a weighted average: 0.571 x 700 + 0.429 x 0 = Rs 400. Matches. The answer is not a whole number (571.4), so it is an approximation; 571 customers would give a blended CAC of Rs 399.7.
**Caveats:** Organic installs are not truly free: brand spend, SEO and referral rewards may sit elsewhere. Blended CAC falls whenever the organic share rises, even if paid efficiency worsens.
**Likely follow-ups:** 1) *What if paid CAC rises to Rs 800 with the same Rs 4,00,000 spend?* Paid customers fall to 500; if organic stays at 429, blended CAC becomes 4,00,000 / 929 = about Rs 430. 2) *Which CAC do you plan budgets with?* Paid CAC for the marginal decision.
**Common mistakes / traps:** Doing 1,000 x 700; averaging 700 and 0 to get 350.

### Q49 ⭐⭐ 🟡 A company has two customer segments. Segment A: ARPU Rs 600 per month, churn 3% per month. Segment B: ARPU Rs 900 per month, churn 6% per month. Ignoring margin, which has the higher LTV, and by how much?
**Asked at:** commonly asked (no company-specific report found); LTV is a core metric topic in prep sites and Swiggy-style guides (unverified).
**What the interviewer is checking:** Whether you use LTV = ARPU / churn and notice that low churn can beat high price.
**Say this in the interview:** "Segment A: 600 / 0.03 = Rs 20,000. Segment B: 900 / 0.06 = Rs 15,000. A is higher by Rs 5,000, about 33% more than B, even though its monthly price is lower."
**Definition in plain words:** ARPU is average revenue per user per month. With constant monthly churn, the average customer stays 1 / churn months, so LTV (revenue over a customer's life) = ARPU / churn.
**Worked answer:**
1. A: lifetime = 1 / 0.03 = 33.3 months; LTV = 600 x 33.3 = Rs 20,000.
2. B: lifetime = 1 / 0.06 = 16.7 months; LTV = 900 x 16.7 = Rs 15,000.
3. Difference = Rs 5,000.
**Result:** Segment A has the higher LTV by Rs 5,000 (A is 33% above B; B is 25% below A).
**Check:** B's price is 50% higher but its lifetime is half as long, so 1.5 x 0.5 = 0.75 of A's LTV. Matches 15,000 / 20,000.
**Caveats:** Ignores margin, discounting and CAC. If B costs far less to acquire, the LTV:CAC ratio could still favour B. Constant churn is an assumption.
**Likely follow-ups:** 1) *At what B churn do they tie?* 900 / 20,000 = 4.5%. 2) *Which segment do you invest in?* Compare LTV minus CAC and payback time.
**Common mistakes / traps:** Picking the higher ARPU; using annual churn with monthly ARPU.

### Q50 ⭐⭐ 🟡 Why can LTV calculated as ARPU divided by churn be misleading for a young startup? Name at least three problems.
**Asked at:** commonly asked (no company-specific report found); LTV and its limits appear in prep-site SaaS analyst lists (unverified).
**What the interviewer is checking:** Whether you know the formula's assumptions and can name its failure modes.
**Say this in the interview:** "It assumes churn is steady, revenue is flat and the data is long enough to trust. A young startup breaks all three, and the formula also ignores margin and cash timing."
**Explain simply:**
- **Short history:** churn is measured over a few months of early adopters; 3% observed does not mean 3% for ever. Dividing by a tiny, noisy churn number gives huge, unreliable LTVs (1% churn gives 100 months, 0.5% gives 200).
- **Churn is not constant:** new customers usually leave faster than old ones (see Q64), so the average lifetime is not 1 / churn.
- **Revenue is not flat:** ARPU can grow (upsells) or shrink (discounts); the formula uses one number.
- **No margin:** revenue is not profit; use gross-margin-adjusted ARPU.
- **No discounting:** a rupee in 5 years is worth less than a rupee now; startups also face cash limits.
- **Mix and survivorship:** early users are enthusiasts and not typical of later cohorts.
- Mini-example: ARPU Rs 500, churn 2% gives Rs 25,000. At 60% margin it is Rs 15,000; if real lifetime is capped at 24 months, it is under Rs 10,000.
**Practice step:** Take any one cohort you have and compare its actual cumulative revenue to the formula's prediction.
**Likely follow-ups:** 1) *What would you use instead?* Cohort-based cumulative margin over a fixed horizon (12 or 24 months). 2) *Why cap the horizon?* To avoid trusting a lifetime you have never observed.
**Common mistakes / traps:** Quoting a big LTV as proof of success; forgetting margin; not naming the constant-churn assumption.

### Q51 ⭐⭐ 🟡 What is the difference between blended CAC and paid CAC, and why can blended CAC hide a problem?
**Asked at:** commonly asked (no company-specific report found); CAC is named in Swiggy business analyst guides (prep sites, unverified).
**What the interviewer is checking:** Whether you see that organic customers dilute the average.
**Say this in the interview:** "Blended CAC divides spend by all new customers; paid CAC divides paid spend by paid customers only. Blended can look flat or better while paid CAC is climbing, because organic growth masks it."
**Explain simply:**
- **Blended CAC** = total acquisition spend / all new customers (organic included).
- **Paid CAC** = paid-channel spend / customers from paid channels. This is the cost of buying one more customer.
- Worked example: last quarter spend Rs 4,00,000 for 1,000 customers (571 paid): blended Rs 400, paid Rs 700. This quarter spend Rs 6,00,000 for 1,200 customers, of which 600 paid: blended Rs 500 and paid Rs 1,000 (a 43% rise). Blended rose 25% so the alarm is dulled by the 600 organic customers.
- Blended also falls if a viral event or festival pushes organic installs up, even when ads got worse.
**Practice step:** Split any CAC number by channel and look at the trend of each, not the total.
**Likely follow-ups:** 1) *Which do you use for budget decisions?* Paid (marginal) CAC by channel. 2) *Is organic free?* No: content, brand and referral costs sit somewhere.
**Common mistakes / traps:** Using blended CAC to justify more spend; counting organic customers in the paid denominator.

### Q52 ⭐⭐ 🟡 What is cohort analysis, and how is it different from looking at a single overall retention number?
**Asked at:** commonly asked (no company-specific report found); cohort and retention is a named question type in prep sites such as TechPrep and DataDriven (unverified).
**What the interviewer is checking:** Whether you understand that overall averages mix old and new users.
**Say this in the interview:** "A cohort groups users by when they started, then tracks each group over time. One overall number blends loyal old users with new ones and can hide whether newer cohorts are better or worse."
**Explain simply:**
- **Cohort** = a group sharing a start month (or channel or plan). Rows are cohorts, columns are months since joining; each cell is the % still active.
- An overall retention number is one average across all users. It moves with the mix of old and new customers, not only with product quality.
- Mini-example: January cohort keeps 40% at month 3; June cohort keeps 30%. A single overall figure of about 35% blends the two and hides that the newer cohort is 10 points worse.
- Cohorts also show the shape (steep early drop then flat is healthy; a steady slide is not) and the effect of changes (a new onboarding in June shows up only in the June row).
- HR parallel: attrition of employees by joining batch shows that new joiners leave faster, which an overall attrition rate hides.
**Practice step:** Build a 6 x 6 triangle in Excel from a table of customer id, start month and active months, then colour it.
**Likely follow-ups:** 1) *Calendar versus age view?* Age view (months since joining) compares cohorts fairly. 2) *What is a small-cohort risk?* Noise; show cohort sizes.
**Common mistakes / traps:** Comparing a young cohort's month 1 with an old cohort's month 6; ignoring cohort size.

### Q53 ⭐⭐ 🟡 How would you measure and report the retention of an edtech course (completion-based) versus a consumer subscription app?
**Asked at:** commonly asked (no company-specific report found); retention-by-product-type is a common metric-design topic (prep sites, unverified).
**What the interviewer is checking:** Whether you match the retention definition to how the product is used.
**Say this in the interview:** "A course has a natural end, so I measure progress and completion through it. A subscription app has no end, so I measure the share of subscribers still active or still paying month by month."
**Explain simply:**
- **Edtech course:** retention is about learners staying through lessons. Measures: share active in week 1, 2, 3...; lesson-to-lesson drop-off; completion rate = learners who finished / learners who enrolled (state the enrolment date window); with outcome metrics such as test scores or re-enrolment in the next course. Completion is the end, so "churn" is mostly a drop-off curve.
- **Consumer subscription:** classic cohort retention. Month-N retention = subscribers from a start month still active (or still paying) in month N. Report both logo retention (people) and revenue retention. Split free-trial users from paid.
- Report cohorts for both, with the same cohort layout; for edtech add "completion by week" lines.
- Mini-example: 1,000 learners enrol, 600 reach week 4, 400 finish: completion 40%. For an app: 1,000 subscribers, 700 left at month 3: 70% retention.
- Cautions: a completed course is a success, not churn; a paused subscription needs a rule.
**Practice step:** Write the definition of "retained" for each product in one sentence, with window and denominator.
**Likely follow-ups:** 1) *Why are course completion rates low?* Self-paced, no deadline; report by batch with live classes separately. 2) *What is the lead indicator?* First-week activity.
**Common mistakes / traps:** Treating completion as churn; using one retention definition for both products.

### Q54 ⭐⭐ 🟡 A bank's mobile app shows a rising MAU but falling revenue per user. What could explain this and what data would you pull?
**Asked at:** commonly asked (no company-specific report found); a KPI-diagnosis type seen in Flipkart-style KPI rounds per candidate reports (mapping unverified).
**What the interviewer is checking:** Structured thinking: revenue per user is total revenue divided by users, so check both parts.
**Say this in the interview:** "Revenue per user falls when the new users are low-value, when existing users use paid features less, or when pricing and fees changed. I would split by new versus old users, product and fee type."
**Clarify first:** How is "revenue" defined (fees, interest, interchange)? Over what period? Is MAU defined as a login or a transaction?
**Structure:**
- Mix: new users are low-value (students, small-ticket, free-account users); acquisition of a less affluent segment.
- Behaviour: existing users do fewer revenue transactions (moved to free UPI, fewer card swipes) or log in only to check balance.
- Pricing: fee waivers, lower interchange, reduced loan rates.
- Definition: MAU counts logins, so "active" inflates if a notification now pulls users in.
- Seasonality and external: a holiday month, regulation.
**What I would check, in order:**
1. Revenue per user split by new (joined this quarter) versus existing users.
2. Revenue by product (cards, loans, fees, deposits) and the user count for each.
3. Users per segment (age, city, salaried or not), revenue per segment over time.
4. MAU definition changes and the share of users with zero revenue.
5. Pricing and fee changes, and the transaction mix.
**If the data shows...:** Existing users stable and new users low: mix problem, build a cross-sell journey. Existing users down: product or pricing issue. Zero-revenue user share up: MAU definition inflated by logins.
**Numeric work (if data given):** Example (assumed): 1,00,000 users earning Rs 500 each = Rs 5 crore; later 1,30,000 users with Rs 5.2 crore = Rs 400 each. The 30,000 new users added only Rs 20 lakh (Rs 67 each).
**Recommendation:** Keep MAU but add revenue-active users and revenue per active user to the dashboard; target the low-value new users with a first-product offer.
**Likely follow-ups:** 1) *Is it bad?* Not necessarily; a funnel can be building. 2) *How to confirm?* Cohort revenue per user over time.
**Common mistakes / traps:** Treating MAU growth as success; not splitting new from existing.

### Q55 ⭐⭐ 🟡 How would you define the KPIs for a customer support team at a fintech company? Name 4-5 metrics with one risk of gaming for each.
**Asked at:** commonly asked (no company-specific report found); KPI and dashboard design is a named question type for analytics roles (prep sites such as Dataford, unverified).
**What the interviewer is checking:** Whether you pair every metric with a guardrail, since any single metric can be gamed.
**Say this in the interview:** "I would track speed, resolution, quality and cost together. First response time, resolution rate, CSAT, first-contact resolution and cost per ticket, each paired with a guardrail because each can be gamed."
**Explain simply:**
- **First response time (FRT):** time from ticket to first reply. Gaming: send an instant auto-reply that says nothing. Guardrail: measure time to meaningful reply.
- **Average resolution time:** time to close. Gaming: close tickets early and let them reopen. Guardrail: reopen rate.
- **First-contact resolution (FCR):** share of issues solved in the first interaction. Gaming: mark ticket "resolved" without confirmation. Guardrail: repeat contact within 7 days.
- **CSAT (customer satisfaction, 1-5 rating after ticket):** Gaming: ask only happy customers or coach customers to rate 5. Guardrail: survey response rate and random sampling.
- **Cost per ticket or tickets per agent:** Gaming: rush and push customers off. Guardrail: quality score and CSAT together.
- Fintech add-ons: share of fraud and failed-payment tickets resolved within the regulatory timeline, backlog ageing.
- Mini-example: 2,000 tickets, 1,700 resolved first contact: FCR 85%.
**Practice step:** For each metric write the formula, owner and one guardrail in one table.
**Likely follow-ups:** 1) *Which is the single best metric?* None; use CSAT or FCR as the headline with others as inputs. 2) *Escalations?* Track them as a quality guardrail.
**Common mistakes / traps:** Choosing only speed metrics; ignoring reopen rate; no segment cuts (payments versus KYC tickets).

### Q56 ⭐⭐ 🟡 What KPIs would you track for a quick-commerce dark store, and which would you put on a daily dashboard?
**Asked at:** commonly asked (no company-specific report found); quick-commerce operations metrics are a plausible analyst topic (unverified).
**What the interviewer is checking:** Whether you cover supply, demand, speed and money, and can pick what needs watching every day.
**Say this in the interview:** "I would group KPIs into availability, speed, quality and economics. The daily dashboard needs the few that need quick action: orders, fill rate, delivery time, stock-outs and cancellations."
**Explain simply:**
- **Demand and money:** orders per day, average order value (AOV), gross merchandise value (GMV), contribution per order.
- **Availability:** fill rate (share of ordered items delivered), stock-outs on top-selling items, inventory days.
- **Speed:** order-to-delivery time, picking time, share delivered within the promised time (for example 10-15 minutes; an assumed promise, it differs by company).
- **Quality:** wastage and expiry (perishables), damage, cancellation rate, refund rate, ratings.
- **Efficiency:** orders per picker per hour, rider utilisation, store capacity utilisation.
- **Daily dashboard:** orders against forecast, fill rate, delivery time (average and 90th percentile), stock-outs on top items, cancellations, rider availability. **Weekly or monthly:** wastage, contribution per order, inventory days, ratings.
- Mini-example: 4,000 orders, 3,880 delivered in time: 97% on-time.
**Practice step:** Choose five daily KPIs and write which action each one triggers.
**Likely follow-ups:** 1) *Average versus percentile delivery time?* Percentile shows the late tail. 2) *Fill rate versus stock-out?* Fill rate by order, stock-out by item.
**Common mistakes / traps:** Putting everything on the daily view; using only averages; no balance between speed and rider load.

### Q57 ⭐⭐ 🟡 How would you define the KPIs for an HR team: recruitment, attrition and engagement? Name the formulas.
**Asked at:** HR metric formulas appear on HR-analytics prep and blog sites (Tutorialspoint, Deel, HelloIntern; unverified); no company-specific report found.
**What the interviewer is checking:** Whether you can state clear formulas with correct denominators in your own field.
**Say this in the interview:** "Recruitment: time to fill, cost per hire, offer-accept rate. Attrition: leavers divided by average headcount, plus 90-day and 12-month new-hire attrition. Engagement: survey score, participation and eNPS."
**Explain simply:**
- **Recruitment:** time to fill = days from job opening to offer accepted (see Q58); cost per hire = total recruitment spend / hires; offer-accept rate = offers accepted / offers made; quality of hire = 12-month retention or performance of new hires.
- **Attrition:** attrition % = employees who left in a period / average headcount x 100, where average headcount = (opening + closing) / 2. Also voluntary versus involuntary and regretted versus non-regretted, and early attrition (leave within 90 days).
- **Engagement:** survey engagement score (average of favourable answers), survey participation rate, employee net promoter score (eNPS) = % promoters (9-10) minus % detractors (0-6), absenteeism rate.
- Mini-example: opening 480, closing 520, 60 left: average 500, attrition 12%.
**Practice step:** For each KPI write the numerator, denominator, period and exclusions.
**Likely follow-ups:** 1) *Annualise a quarterly figure?* Multiply by 4 as an approximation, say so. 2) *Which attrition to watch?* Regretted attrition in critical roles.
**Common mistakes / traps:** Dividing by closing headcount; mixing voluntary and involuntary exits; skipping the denominator in engagement.

### Q58 ⭐⭐ 🟡 What is the difference between time-to-fill and time-to-hire in recruitment analytics?
**Asked at:** HR prep sources define both (unverified); no company-specific report found.
**What the interviewer is checking:** Whether you know the two clocks start at different points.
**Say this in the interview:** "Time to fill starts when the job requisition is opened and ends when an offer is accepted. Time to hire starts when a specific candidate enters the pipeline and ends when they accept. The first measures the process, the second the candidate experience."
**Explain simply:**
- **Time to fill** = date offer accepted minus date job requisition approved (or posted).
- **Time to hire** = date offer accepted minus date the chosen candidate applied (or was first contacted).
- Definitions vary by company; always state both start dates.
- Mini-example: requisition opened 1 March, candidate applied 20 March, offer accepted 15 April. Time to fill = 45 days; time to hire = 26 days.
- Time to fill includes the time before candidates even arrive (sourcing, approvals); time to hire shows how quickly the team moves once someone is in the funnel.
- Use the median as well as the average, since a few long searches skew the average.
**Practice step:** Compute both for last quarter's hires and see which gap is larger.
**Likely follow-ups:** 1) *Which would you cut?* If the difference is large, fix sourcing; if time to hire is long, fix interviews. 2) *Why report both?* They diagnose different stages.
**Common mistakes / traps:** Using them as synonyms; mixing start dates between roles.

### Q59 ⭐⭐ 🟡 A company reports cost per hire as total recruitment spend divided by hires. Spend this quarter was Rs 24,00,000 (agency fees Rs 14,00,000, job portals Rs 4,00,000, referral bonuses Rs 2,00,000, recruiter salaries Rs 4,00,000) and there were 48 hires. Find the cost per hire and the cost per hire if recruiter salaries are excluded.
**Asked at:** HR-metric formulas appear on HR-analytics prep sites (unverified); no company-specific report found.
**What the interviewer is checking:** Whether you can calculate and explain that the definition changes the figure.
**Say this in the interview:** "Rs 24,00,000 divided by 48 is Rs 50,000 per hire. Without recruiter salaries it is Rs 20,00,000 / 48, about Rs 41,667."
**Definition in plain words:** Cost per hire = total recruitment cost / number of hires. External costs are fees paid outside; internal costs include salaries.
**Worked answer:**
1. Check the total: 14 + 4 + 2 + 4 = Rs 24 lakh. It matches.
2. All-in: 24,00,000 / 48 = Rs 50,000.
3. Excluding salaries: 24,00,000 - 4,00,000 = Rs 20,00,000; / 48 = Rs 41,666.7, about Rs 41,667.
**Result:** Rs 50,000 all-in; about Rs 41,667 excluding recruiter salaries (a Rs 8,333 gap, 16.7% lower).
**Check:** 48 x 50,000 = 24,00,000. And salaries per hire = 4,00,000 / 48 = Rs 8,333, which is the gap.
**Caveats:** Decide whether internal costs count and keep it consistent when comparing periods or companies. Agency fees: Rs 14,00,000 is 58% of spend; look at cost per hire by channel (see Q60). Cost per hire ignores hire quality.
**Likely follow-ups:** 1) *Which figure do you report?* All-in for the true cost, external-only for channel decisions. 2) *Add onboarding cost?* Some firms do; state it.
**Common mistakes / traps:** Dividing by applicants rather than hires; leaving out salaries without saying so.

### Q60 ⭐⭐ 🟡 A company's 12-month retention of new hires is 70% for those from agencies and 85% for referrals. Cost per hire is Rs 90,000 for agency hires and Rs 30,000 for referrals. How do you compare the two channels on cost per retained hire?
Use cost per retained hire = cost per hire divided by 12-month retention rate.
**Asked at:** HR-metric formulas appear on HR-analytics prep sites (unverified); no company-specific report found.
**What the interviewer is checking:** Whether you adjust cost for quality, not just compare headline cost.
**Say this in the interview:** "Agency: 90,000 / 0.70 = Rs 1,28,571 per retained hire. Referral: 30,000 / 0.85 = Rs 35,294. Referrals are about 3.6 times cheaper once we count who stays."
**Definition in plain words:** Cost per retained hire = what you spend to end up with one person still there after 12 months. If 30% of agency hires leave, their cost is spread over fewer survivors.
**Worked answer:**
1. Agency: 90,000 / 0.70 = Rs 1,28,571.
2. Referral: 30,000 / 0.85 = Rs 35,294.
3. Gap: 1,28,571 - 35,294 = Rs 93,277.
4. Ratio: 1,28,571 / 35,294 = 3.64.
**Result:** Referral hires cost about Rs 35,294 per retained hire versus Rs 1,28,571 for agency hires, a gap of about Rs 93,000.
**Check:** Headline gap is 3.0x (90,000 / 30,000), retention makes it 3.64x. Agency cost per hire rises 43% (1 / 0.7 = 1.43) and referral rises 18% (1 / 0.85 = 1.18).
**Caveats:** Referrals cannot fill every role and volume is limited; agencies may reach senior or niche roles. The 12-month window ignores replacement cost if only some stay, and sample sizes may be small. Roles in each channel may differ, so compare like for like.
**Likely follow-ups:** 1) *Does this prove agencies are bad?* No, only that they cost more per retained hire; check role mix. 2) *Other costs?* Replacement and lost productivity.
**Common mistakes / traps:** Multiplying by retention instead of dividing; comparing only cost per hire.

### Q61 ⭐⭐ 🟡 How would you build a single customer health score for a SaaS account, and how would you check that it predicts churn?
**Asked at:** commonly asked (no company-specific report found); SaaS analyst prep (for example Finalround) lists churn topics (unverified).
**What the interviewer is checking:** Whether you combine signals sensibly and then validate against real outcomes.
**Say this in the interview:** "I would pick a handful of usage, engagement, support and commercial signals, weight them into a 0 to 100 score, then test on past data whether low-score accounts actually churned more."
**Explain simply:**
- **Choose inputs:** product usage (logins, active seats / purchased seats), depth (key features used), trend (usage vs last 3 months), support (open or escalated tickets), commercial (days to renewal, payment delays), sentiment (NPS).
- **Score each input** 0 to 100 against fixed thresholds or percentiles, then take a weighted average. Start with simple weights agreed with customer success; refine with logistic regression (a model giving churn probability).
- **Bands:** green above 70, amber 40 to 70, red below 40.
- **Validate:** take scores as at 90 days before each past renewal; compare churn rate by band; measure how well it ranks accounts (AUC, a score where 0.5 is a coin flip and 1.0 is perfect ranking; aim well above 0.5), and calibration (do 20% predicted churners churn about 20% of the time?). Use a held-out time period, not the same data.
- Mini-example (assumed): red band churned 35%, amber 12%, green 3%: the score separates well.
**Practice step:** Compute churn rate by health band for last year in a pivot table.
**Likely follow-ups:** 1) *How often to refresh?* Weekly or monthly. 2) *What if usage is high but they still churn?* Add commercial signals such as budget or champion change.
**Common mistakes / traps:** Too many inputs; testing on the same data used to set weights; using today's score for past churn (leakage).

### Q62 ⭐⭐ 🟡 An e-commerce company wants to know whether free delivery on orders above Rs 499 increased AOV. What metrics and comparisons would you use besides the before/after AOV?
**Asked at:** commonly asked (no company-specific report found); Swiggy AOV question types and Flipkart funnel/KPI topics appear in prep sites (unverified).
**What the interviewer is checking:** Whether you avoid a naive before/after and look for a fair comparison and side effects.
**Say this in the interview:** "Before/after is confounded by seasonality and other changes. I would add a control group or difference-in-differences, check the order-value distribution near Rs 499, and look at conversion, orders per user and profit."
**Clarify first:** Was it a test with a control? Same period for other changes (sale, price cuts)? Which categories?
**Structure:**
- Fair comparison: A/B test or a control (similar cities or users without the offer); otherwise difference-in-differences (change in treated minus change in control).
- Mechanism: share of orders just above Rs 499 (say Rs 499 to 550) and drop below it; items per order; add-on behaviour.
- Side effects: conversion, orders per user, new-customer share, basket abandonment.
- Money: delivery cost absorbed, contribution per order, not only AOV.
**What I would check, in order:**
1. Histogram of order value by week, before and after (a spike at Rs 499-550 means the threshold works).
2. AOV for control versus treatment for the same weeks.
3. Items per order and basket mix.
4. Orders per user and conversion (AOV can rise while total orders fall).
5. Contribution per order after delivery cost.
**If the data shows...:** Spike at the threshold and control flat: real effect. AOV up but orders down and contribution down: it is shifting small orders away, not creating value. Treatment and control both up: seasonality.
**Recommendation:** Judge by contribution per user and orders, not AOV alone; tune the threshold.
**Likely follow-ups:** 1) *How long to run the test?* At least one or two full weekly cycles. 2) *What about mix?* Check categories with Simpson's paradox in mind.
**Common mistakes / traps:** Calling a before/after a causal result; ignoring order count and cost.

### Q63 ⭐⭐ 🔴 A food delivery company's monthly order frequency per active user rose from 3.0 to 3.3, but the number of active users fell from 1,00,000 to 92,000. Total orders went from 3,00,000 to 3,03,600. Break the order change into the effect of users and the effect of frequency.
**Asked at:** commonly asked (no company-specific report found); Swiggy-style order and frequency questions appear in prep sites (unverified); this decomposition is a gap-fill type.
**What the interviewer is checking:** Whether you can split a product (users x frequency) into two effects that add up to the total.
**Say this in the interview:** "Orders = users x frequency. Total change is +3,600. Fewer users cost 24,000 orders, higher frequency added 27,600, net +3,600."
**Definition in plain words:** Orders = active users x orders per user. A change in orders comes from a change in users (volume effect) and a change in frequency (behaviour effect).
**Worked answer:**
1. Check: 1,00,000 x 3.0 = 3,00,000; 92,000 x 3.3 = 3,03,600. Both match the question.
2. Total change = 3,03,600 - 3,00,000 = +3,600 (+1.2%).
3. User effect at old frequency = (92,000 - 1,00,000) x 3.0 = -24,000.
4. Frequency effect at new users = (3.3 - 3.0) x 92,000 = +27,600.
5. Sum = -24,000 + 27,600 = +3,600.
**Result:** Users effect -24,000 orders; frequency effect +27,600 orders; net +3,600.
**Check:** The other order of calculation: frequency at old users = 0.3 x 1,00,000 = +30,000; users at new frequency = -8,000 x 3.3 = -26,400; sum +3,600. The split changes slightly with the order, because of the interaction term (-8,000 x 0.3 = -2,400), so say which one you used.
**Caveats:** Frequency may rise because the lighter users left, so the average of those who remain is higher (a mix effect). Check by cohort. An 8% user loss with a 10% frequency gain is a risky replacement: acquisition costs are lost.
**Likely follow-ups:** 1) *Is this good news?* Orders are flat, but the base is shrinking; investigate why users left. 2) *Which order of decomposition?* Either; state it.
**Common mistakes / traps:** Adding percentages (-8% and +10% do not give +2%); forgetting the interaction term.

### Q64 ⭐⭐ 🔴 Monthly churn of a SaaS product is 2% for customers in their first year and 0.5% after the first year. About 60% of the base is in year one. What is the blended monthly churn and what should the company target?
**Asked at:** commonly asked (no company-specific report found); the mix-shift retention question is a gap-fill type, not source-evidenced.
**What the interviewer is checking:** Whether you weight by base share and see that blended churn depends on the mix of young and old customers.
**Say this in the interview:** "Blended churn = 0.6 x 2% + 0.4 x 0.5% = 1.4% a month. The real target is first-year churn, because it is four times higher and it drives the blend."
**Definition in plain words:** Blended churn is the base-weighted average of the segment churn rates (with the base weights as shares of customers at the start of the month).
**Worked answer:**
1. Year-one part: 0.60 x 2.0% = 1.2%.
2. Older part: 0.40 x 0.5% = 0.2%.
3. Blended = 1.2% + 0.2% = 1.4% a month.
4. Expected lifetime at 1.4% = 1 / 0.014 = about 71 months (a rough figure; see caveats).
5. Annual view: a first-year customer survives 12 months with 0.98^12 = 78.5%; an older one 0.995^12 = 94.2%.
**Result:** Blended monthly churn is 1.4%. Target: first-year churn. Cutting it from 2% to 1.5% lowers the blend to 1.1% (0.6 x 1.5 + 0.4 x 0.5); 1.0% takes it to 0.8%.
**Check:** The blend must lie between 0.5% and 2%. It does, and it sits nearer 2% because 60% of the base is young.
**Caveats:** The blend is not stable: as the base ages (say 50% in year one), the same segment rates give 1.25% with no real improvement. So track each segment, not only the blend. Lifetime of 71 months is a mix, not any one customer's life.
**Likely follow-ups:** 1) *What actions?* Onboarding, activation in the first 30 days, annual plans. 2) *What if year-one share rises to 70%?* Blend 1.55%.
**Common mistakes / traps:** Simple average (1.25%); targeting blended churn without the mix; trusting lower blended churn as improvement when the base just aged.

### Q65 ⭐⭐ 🔴 Your LTV:CAC looks healthy at 4:1 but the CFO says cash is running out. Explain how this is possible and which metrics you would add.
**Asked at:** commonly asked (no company-specific report found); LTV:CAC versus cash is a gap-fill type, not source-evidenced. SaaS prep sources mention CAC payback (unverified).
**What the interviewer is checking:** Whether you separate lifetime value (earned slowly, over years) from cash timing.
**Say this in the interview:** "LTV:CAC ignores timing. If it takes 20 months to earn back the CAC, or most LTV is far in the future, the company spends cash today and gets it back late, so it can run out before the profits arrive."
**Explain simply:**
- **Timing:** LTV is lifetime revenue earned over years; CAC is paid on day one. Example (assumed): CAC Rs 12,000, ARPU Rs 1,000 a month at 60% margin = Rs 600 monthly margin: payback is 12,000 / 600 = 20 months. LTV = 4 x 12,000 = Rs 48,000 needs 80 months (churn near 1.25% a month), a lifetime nobody has observed.
- **Wrong inputs:** LTV on revenue, not margin; optimistic churn from early data; undiscounted; CAC that excludes sales salaries.
- **Growth burns cash:** the faster you acquire, the more cash goes out before it comes back; fixed costs and unpaid-for working capital add to it.
- **Other cash drains:** fixed costs, refunds, annual versus monthly billing, delayed collections.
- **Metrics to add:** CAC payback period (months), cash burn (cash going out minus cash coming in each month) and runway (months of cash left = cash / monthly net burn), gross margin, contribution margin, cohort cumulative cash margin curve, net revenue retention, billing mix (annual upfront helps cash), accounts receivable days.
- Remedies: push annual prepay, cut payback below 12 months, slow paid acquisition, improve margin.
**Practice step:** Compute payback and runway for a made-up business and plot cumulative cash per cohort.
**Likely follow-ups:** 1) *Good payback?* Often cited under 12 months for SMB (a rule of thumb, unverified). 2) *Is 4:1 wrong?* Not wrong; it is incomplete.
**Common mistakes / traps:** Defending the ratio alone; not mentioning payback and runway.

### Q66 ⭐⭐ 🔴 Design a metric framework (North Star, inputs, guardrails) for a ride-hailing app that wants to grow rides without losing driver supply.
**Asked at:** commonly asked (no company-specific report found); North Star/primary-versus-guardrail framing appears in prep guides for Flipkart-style and Swiggy-style product cases (unverified).
**What the interviewer is checking:** Whether you balance two sides of a marketplace and set guardrails against growth that hurts supply.
**Say this in the interview:** "North Star: completed rides per week. Inputs on demand and supply sides, and guardrails on driver earnings, rider wait time and cancellations, so growth does not come by burning drivers."
**Clarify first:** City or national? Growth wanted in rides or profitable rides? Which vehicles? Is supply constrained at peak hours?
**Structure:**
- **North Star:** weekly completed rides (or completed rides per active driver hour, which also reflects supply health). Pick one and state why.
- **Demand inputs:** new and repeat riders, app opens to booking conversion, rides per rider.
- **Supply inputs:** active drivers, driver online hours, driver acceptance rate, drivers per ride request (supply/demand ratio).
- **Marketplace health:** rider wait time (ETA to pickup), request fulfilment rate (rides completed / requested), cancellation rates by side.
- **Guardrails:** driver earnings per hour and driver retention (the supply protection), rider cancellation and safety incidents, contribution per ride (not below a floor), ratings.
**What I would check, in order:**
1. Fulfilment rate and wait time by zone and hour (where supply is short).
2. Driver earnings per hour and 4-week retention of new drivers.
3. Rider repeat rate by cohort.
4. Contribution per ride versus incentives (see Q45).
**If the data shows...:** Rides up but driver earnings per hour down: growth is subsidised or oversupplied; slow rider promos. Wait time up and fulfilment down: supply is the bottleneck, spend on driver incentives. Driver churn up in new cohorts: onboarding or earnings problem.
**Recommendation:** Run the North Star with a driver earnings floor as a hard guardrail, review weekly by zone, and test rider promos only where fulfilment is above target.
**Likely follow-ups:** 1) *Why not rides alone?* It can be inflated by discounts that drain driver earnings. 2) *Why a guardrail?* A metric that must not worsen while you chase the North Star.
**Common mistakes / traps:** Only rider-side metrics; no guardrails; choosing a vanity North Star such as app downloads.

### Q67 ⭐⭐ 🔴 A cohort table shows Month-1 retention of 40% for all cohorts, but Month-3 retention has dropped from 25% in January cohort to 15% in April cohort. What are your hypotheses and how would you test them?
**Asked at:** commonly asked (no company-specific report found); cohort and retention reading questions are listed on prep sites (TechPrep, DataDriven), unverified for any company.
**What the interviewer is checking:** Whether you localise the problem in time and segment before guessing causes, and whether you suspect the data itself.
**Say this in the interview:** "Month-1 is identical, so onboarding looks fine; the damage happens between month 1 and month 3. Of the 40% who stay, 62.5% stayed to month 3 in January but only 37.5% in April. I would first check the data, then split by channel, version and plan."
**Clarify first:** What does "retained" mean (any activity, or a core action)? Is the month-3 figure for April complete, or is it still being filled? Did pricing, app version, trial length or acquisition channels change between January and April?
**Structure:**
- Data issues: April month-3 not fully matured (right-censoring), definition or tracking change, bots.
- Who changed (mix): channel mix, city or device mix, a campaign that brought lower-intent users who behave the same in month 1 (trial period) but leave after.
- What changed for the same people (product): feature removed or buggy, notification changes, paywall or price change after the trial, content quality.
- Outside factors: seasonality (January resolution-driven users versus April exams or summer), competitor launch.
**What I would check, in order:**
1. Confirm the April cohort has a full month 3 of data and that the metric definition did not change.
2. Add Month-2 retention to see exactly where the fall starts (conditional retention M1 to M3: January 25/40 = 62.5%, April 15/40 = 37.5%).
3. Cut each cohort by channel, platform, app version, city, plan; look for one segment that explains most of the drop (a mix shift) versus a drop in every segment (a product or external cause).
4. Compare usage in weeks 5 to 12 (sessions, core actions) for the two cohorts, and check release and pricing calendars.
**If the data shows...:** drop only in one channel means an acquisition-quality problem, fix targeting. Drop in all segments from one app version means a product regression. Drop right when a trial or discount ends means a pricing or value issue. Drop only because April is incomplete means no problem, wait.
**Numeric work (if data given):** M3 fell 10 points (25% to 15%), a 40% relative fall; of every 100 users, 40 are active in month 1 in both cohorts, but 25 versus 15 in month 3.
**Recommendation:** Share the segment finding, run a fix or experiment on the worst segment, and track month-2 and month-3 retention weekly for new cohorts.
**Likely follow-ups:** (1) How can month 1 be equal but month 3 differ? Different things drive early and late retention: onboarding versus lasting value. (2) How would you prove cause? A/B test the suspected change or a holdout.
**Common mistakes / traps:** Jumping to "product got worse" without checking cohort maturity; comparing blended numbers where mix hides the cause (Simpson's paradox); proposing five fixes without a test.

### Q68 ⭐⭐ 🔴 A product shows rising DAU, rising time spent and falling revenue per user. Is the product healthy? Structure your answer.
**Asked at:** commonly asked (no company-specific report found); metric-interpretation cases like this appear in prep guides for product and business analyst roles (unverified).
**What the interviewer is checking:** Whether you avoid a yes/no and decompose total revenue into users times revenue per user.
**Say this in the interview:** "It depends on total revenue and on who the new users are. Revenue is users times revenue per user, so I would check whether the growth in users outweighs the fall per user, and whether the fall is a mix shift or a real monetisation problem."
**Clarify first:** Which revenue per user (ARPU) and over what window? Is DAU growth from new users or old ones? Did monetisation (ads, pricing, free tier) change?
**Structure:**
- Arithmetic: revenue = DAU x revenue per DAU. Example: DAU 10 lakh to 13 lakh (+30%), revenue per user Rs 10 to Rs 8.5 (-15%); total revenue index 1.30 x 0.85 = 1.105, so +10.5%. Growing, but slower than usage.
- Cause tree for falling revenue per user: (a) mix shift, new users are in low-spend segments or cities; (b) less ad load or discounts or more free features; (c) time is going to unmonetised features; (d) tracking or bot issues.
- Quality of engagement: is time spent real value (task completed) or friction (slow app, confusing flow)?
**What I would check, in order:** revenue per user by segment (new versus old, city, plan); same-segment trend (if flat inside every segment it is pure mix); time spent split by monetised and unmonetised features; retention of the new users; cost to serve.
**If the data shows...:** per-segment revenue stable and mix shifted means healthy growth with a lower average, plan monetisation for the new segment. Per-segment revenue falling means a monetisation or pricing problem. Time spent up from frustration (more taps to do the same task) means unhealthy.
**Recommendation:** Call it "growing, health unproven": report total revenue, per-segment revenue per user and retention together, and set a guardrail so monetisation tests do not hurt engagement.
**Likely follow-ups:** (1) What single number would you trust? Cohort contribution or revenue per cohort over time. (2) When is it fine? When new users are an investment that monetises later.
**Common mistakes / traps:** Judging only by users and time; ignoring mix (averages hide segments); treating more time as always good.

### Q69 ⭐⭐ 🔴 How would you compute LTV for a new fintech lending product when borrowers have not yet completed their loan tenures?
**Asked at:** commonly asked (no company-specific report found); this is a gap-fill topic not directly evidenced in the source searches.
**What the interviewer is checking:** Whether you can estimate lifetime value from incomplete data using early indicators, and include credit losses.
**Say this in the interview:** "I would estimate the full-tenure value from the loans' early behaviour: model expected income, expected credit loss and repeat borrowing per borrower, using early repayment signals and older comparable loans, and update as real data matures."
**Clarify first:** Loan size and tenure? Interest plus fees structure? Who bears default risk? Is there repeat borrowing? What data exists so far (months on book, delinquency)?
**Structure:** LTV per borrower = expected interest and fee income - cost of funds - expected credit loss - servicing cost, then add repeat loans, then compare to CAC.
**What I would check, in order:**
1. Vintage curves: for each monthly disbursal group, the share late by 30 or 60 days at month 1, 2, 3.
2. Use older or similar products (or a pilot) to map early delinquency to final default, then project the new vintages' final default.
3. Expected income by month from the repayment schedule (adjusted for prepayment).
4. Repeat borrowing rate from early repeaters.
5. Test the estimate by back-testing on a matured vintage.
**Numeric work (illustrative, all assumed):** Loan Rs 20,000, 12 months. Income (interest plus fees) Rs 2,600; cost of funds Rs 800; servicing Rs 200. Expected loss = 4% default x 70% loss given default x Rs 20,000 = Rs 560. Margin per loan = 2,600 - 800 - 200 - 560 = Rs 1,040. If 30% take a repeat loan with the same margin, value = 1,040 / (1 - 0.30) = Rs 1,486. If CAC is Rs 400, net LTV is about Rs 1,086.
**If the data shows...:** early delinquency worse than the pilot means raise the loss estimate and tighten approval; repeat rate low means value rests on one loan, lower CAC limits.
**Recommendation:** Report LTV as a range (base, stressed loss), refresh monthly, and judge channels on loss-adjusted LTV not on disbursal volume.
**Likely follow-ups:** (1) Why not wait? Decisions on CAC and approvals cannot wait a year. (2) Why discount? Money is paid back over months, see Q84.
**Common mistakes / traps:** Counting interest and ignoring defaults; treating a short-term repayment rate as final; ignoring cost of funds.

### Q70 ⭐ 🟢 What is the difference between gross churn and net churn?
**Asked at:** commonly asked (no company-specific report found); churn, NRR and LTV are named SaaS analyst topics on prep blogs (Finalround AI), unverified.
**What the interviewer is checking:** Whether you know net churn subtracts expansion from the same customers.
**Say this in the interview:** "Gross churn counts only what is lost (cancellations and downgrades). Net churn subtracts the revenue added by existing customers (upgrades, add-ons), so it can even be negative."
**Explain simply:**
- Gross churn = (revenue lost to cancellations and downgrades) / (revenue at start).
- Net churn = (revenue lost - expansion revenue from existing customers) / (revenue at start).
- Example: start Rs 1,000 per month. Lost to cancellations Rs 80 and downgrades Rs 20 = Rs 100, so gross churn is 10%. Existing customers added Rs 60, so net churn = (100 - 60) / 1,000 = 4%. If they added Rs 130, net churn = -3% (negative churn).
- New customers are never included in either.
- The same split works for customer counts: gross is the share who left; net would need a rule for returning or upgraded users, so it is mostly used for revenue.
**Practice step:** Take any subscription list and compute both for one month.
**Likely follow-ups:** (1) Which to report? Both; gross shows leakage, net shows growth in the base. (2) Link to NRR? NRR = 1 - net churn (Q79).
**Common mistakes / traps:** Adding new-customer revenue to "net"; letting a good net figure hide high gross churn.

### Q71 ⭐ 🟢 What is a vanity metric? Give two examples from a consumer app.
**Asked at:** commonly asked (no company-specific report found); KPI-design questions appear in prep sources (InterviewStack), unverified for any company.
**What the interviewer is checking:** Whether you prefer actionable metrics to impressive-looking totals.
**Say this in the interview:** "A vanity metric looks good but does not guide decisions or show real value, such as total downloads or total registered users. I would replace them with active users, retention and revenue per user."
**Explain simply:**
- Vanity metrics only go up (cumulative) or ignore quality; you cannot act on them.
- Example 1: total downloads. Say (assumed example) 10 lakh downloads but only 50,000 monthly active users, so 5% of downloads are active.
- Example 2: total registered users or page views, which include dead accounts and accidental visits.
- Better: activation rate, week-4 retention, orders per active user, revenue per user.
- Test: "If this number changed, would I do something different?" If not, it is vanity.
**Practice step:** For an app you know, list three numbers a founder brags about and one better replacement for each.
**Likely follow-ups:** (1) Is a download count useless? Fine for brand reach, not for health. (2) Another HR example? Total CVs received versus offers accepted.
**Common mistakes / traps:** Calling every top-line number vanity; reporting cumulative totals without a rate.

### Q72 ⭐ 🟢 What is the K-factor (viral coefficient)? If each user invites 5 people and 10% of invitees join, what is the K-factor?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic on growth-metric lists, unverified.
**What the interviewer is checking:** Formula and what K above or below 1 means.
**Say this in the interview:** "K = invites per user x conversion of invites = 5 x 10% = 0.5. Each user brings in half a new user, so referrals alone cannot sustain growth."
**Explain simply:**
- K-factor = number of invites sent per user x share of invitees who join.
- K = 5 x 0.10 = 0.5.
- If K is above 1, each wave is bigger than the last, so growth feeds itself. Below 1, it fades.
- Example: 1,000 starting users bring 500 in wave 1, 250 in wave 2, and so on. Total users = 1,000 / (1 - 0.5) = 2,000, so referrals double the starting base but no more.
- Add the cycle time (days from joining to inviting) because a fast K of 0.5 is worth more than a slow one.
**Practice step:** What would you need to reach K = 1? For example 10 invites at 10%, or 5 invites at 20%.
**Likely follow-ups:** (1) Is K above 1 realistic? Rarely sustained; usually decays. (2) Does it count paid users? No, only organic referrals.
**Common mistakes / traps:** Adding the invitees who did not join; forgetting that K applies to each new wave.

### Q73 ⭐ 🟢 What is the Rule of 40 for SaaS companies, and how is it calculated?
**Asked at:** commonly asked (no company-specific report found); a rule-of-thumb topic on SaaS prep lists (unverified).
**What the interviewer is checking:** The formula and the growth-versus-profit idea.
**Say this in the interview:** "Rule of 40: revenue growth rate plus profit margin should be at least 40%. It says a company can trade growth for profit."
**Explain simply:**
- Score = annual revenue growth % + profit margin %, where margin is usually EBITDA margin (profit before interest, tax, depreciation and amortisation, as a share of revenue) or free cash flow margin (cash left after spending; the definition varies, so state which you use).
- Company A: growth 30% + margin 15% = 45, passes.
- Company B: growth 50% + margin -20% = 30, fails despite fast growth.
- It is a rule of thumb, not a law; early-stage firms often fail it by design and investors weigh it differently by size.
**Practice step:** Compute it for a company with growth 25% and margin 10%: 35, just short.
**Likely follow-ups:** (1) Why mix growth and profit? A way to compare firms with different strategies. (2) Weakness? Ignores size and the quality of growth.
**Common mistakes / traps:** Using revenue growth with gross margin; mixing quarterly growth with annual margin.

### Q74 ⭐ 🟢 What are the AARRR (pirate) metrics, and how can they be mapped to a UPI app?
**Asked at:** commonly asked (no company-specific report found); funnel and KPI questions are reported for fintech and product firms such as PhonePe (via prep guide, unverified).
**What the interviewer is checking:** Whether you can map a framework to a real product with concrete metrics.
**Say this in the interview:** "AARRR is Acquisition, Activation, Retention, Referral, Revenue. For a UPI app: installs, first successful payment, repeat monthly payers, invites accepted, and revenue per user."
**Explain simply:**
- Acquisition: how users arrive. Metrics: installs, cost per install, sign-ups by channel.
- Activation: first moment of value. Metrics: bank account linked, first successful payment within 7 days.
- Retention: coming back. Metrics: week-4 and month-3 retention of payers, transactions per active user per month.
- Referral: users bring users. Metrics: invites sent, invite conversion, K-factor (Q72).
- Revenue: money made, often indirect (assumed): bill-pay and recharge fees, merchant services, loan or insurance cross-sell, ads.
- Example funnel (assumed): 100 installs, 60 link a bank (60%), 40 pay once (40% activation).
**Practice step:** Draw the five stages for any app you use and name one metric each.
**Likely follow-ups:** (1) Which stage matters most? Retention usually, since it makes the others pay off. (2) Why revenue is hard in UPI? Direct fees on basic payments are limited, so value comes from cross-sell (assumed, unverified).
**Common mistakes / traps:** Treating the stages as a strict order; counting installs as activation.

### Q75 ⭐ 🟡 What is the difference between MAU, WAU and DAU, and when would you choose WAU as the main engagement metric?
**Asked at:** commonly asked (no company-specific report found); DAU/MAU questions are described as heavily tested (DataDriven, unverified).
**What the interviewer is checking:** Matching the activity window to the natural use cycle.
**Say this in the interview:** "They count distinct active users in a day, a week, a month. I choose WAU when the natural use pattern is weekly, such as grocery, fantasy sports on match days, or an HR self-service portal."
**Explain simply:**
- DAU: distinct users active on a day. WAU: distinct users in a 7-day window. MAU: in a 28 or 30-day window. Each person is counted once per window.
- Rule: pick the window that matches how often a healthy user should need the product. Daily need (messaging, UPI) means DAU; weekly need means WAU; occasional (travel) means MAU.
- Example (illustrative numbers): a grocery app has DAU 20,000, WAU 60,000, MAU 120,000. DAU/MAU = 17%, which looks poor, but WAU/MAU = 50% means half of monthly users shop weekly, which is the healthy pattern.
- WAU also smooths out weekday and weekend swings.
**Practice step:** For your own use of three apps, name the right window.
**Likely follow-ups:** (1) Is WAU the sum of 7 DAUs? No, distinct people. (2) Link to stickiness? DAU/MAU and WAU/MAU are the usual ratios.
**Common mistakes / traps:** Adding daily numbers to get WAU; using DAU for a product people use weekly and calling it unhealthy.

### Q76 ⭐ 🟡 What is a power-user curve (L-ness, L28), and what does it tell you that the DAU/MAU ratio does not?
**Asked at:** commonly asked (no company-specific report found); a differentiator topic, unverified.
**What the interviewer is checking:** Seeing the distribution behind an average.
**Say this in the interview:** "L28 is a histogram: of active users in the last 28 days, how many were active on 1 day, 2 days, up to 28. DAU/MAU is only its average, so it cannot show whether you have a loyal core or many one-time visitors."
**Explain simply:**
- Power-user (L28) curve: x-axis days active out of 28, y-axis number of users. "L-ness" is how much the curve leans toward the right end.
- DAU/MAU = average days active / 28.
- Example, 100 users: Product A: all 100 active 7 days, DAU/MAU = 700 / 2,800 = 25%. Product B: 20 users active 28 days, 60 users 2 days, 20 users 1 day = 700 days, also 25%. Same ratio, very different products: A is evenly engaged; B has a loyal core of 20 and a leaky mass.
- Use it to find the power users, spot whether a feature shifts the middle of the curve, and plan actions (nurture the core or activate the middle).
**Practice step:** Tabulate days active per user for one month and chart it.
**Likely follow-ups:** (1) Why 28? Four full weeks, so weekdays are balanced. (2) What shape is good? Depends on the product; a daily tool wants a bump near 28.
**Common mistakes / traps:** Reading the average as the whole story.

### Q77 ⭐ 🟡 What is the difference between cohort-based retention and rolling (unbounded) retention?
**Asked at:** commonly asked (no company-specific report found); retention question types listed on TechPrep (unverified).
**What the interviewer is checking:** Knowing the two definitions give different numbers.
**Say this in the interview:** "Cohort (classic, bounded) retention counts users active exactly on day N. Rolling or unbounded retention counts users active on day N or any later day, so it is always higher and never goes up with N."
**Explain simply:**
- Same signup group of 100. Day-7 classic: 30 users were active exactly on day 7. Day-7 rolling: 45 users were active on day 7 or later.
- Classic suits products used regularly (daily or weekly use). Rolling suits products with irregular use, such as travel or loan apps, where a user who returns after day 7 still counts.
- Rolling is a generous measure: it only says "have not gone completely".
- State which one you use when comparing.
**Practice step:** From a log with first-active date and activity dates, compute both for day 7.
**Likely follow-ups:** (1) Which is bigger? Rolling. (2) Which in a dashboard? Classic for habit products, with a label.
**Common mistakes / traps:** Comparing one team's classic with another's rolling.

### Q78 ⭐ 🟡 What is revenue per employee, and what are two ways it can mislead?
**Asked at:** commonly asked (no company-specific report found); HR-metric prep content only (unverified).
**What the interviewer is checking:** Formula and awareness of its limits.
**Say this in the interview:** "Revenue divided by average headcount. It is an efficiency signal, but it misleads when companies differ in how much work is outsourced or capital-intensive, and when headcount changes mid-year."
**Explain simply:**
- Revenue per employee = annual revenue / average headcount (average of start and end, or monthly average).
- Example: revenue Rs 120 crore; headcount 300 at start, 500 at end, average 400. Revenue per employee = 120 crore / 400 = Rs 30 lakh. Using the end headcount gives Rs 24 lakh, using the start headcount Rs 40 lakh, so the denominator choice moves the answer.
- Misleading way 1: comparing across business types or models. A firm that outsources or uses contractors shows a high figure; a people-intensive service firm looks low.
- Misleading way 2: timing and one-offs. A hiring burst late in the year or a one-time big deal changes the number without a real change in productivity. It also ignores margin: high revenue per employee with low profit is not efficient.
**Practice step:** Compute it using three headcount definitions and note the spread.
**Likely follow-ups:** (1) Better measure? Profit or gross margin per employee, or per full-time equivalent. (2) Contractors? Include as FTE or state excluded.
**Common mistakes / traps:** Using year-end headcount; comparing different industries.

### Q79 ⭐ 🟡 What is the difference between logo retention and net revenue retention in SaaS, and how can NRR exceed 100%?
**Asked at:** commonly asked (no company-specific report found); NRR is a named topic on SaaS analyst prep (Finalround AI), unverified.
**What the interviewer is checking:** Counts versus money, and expansion.
**Say this in the interview:** "Logo retention counts how many customers stayed. NRR measures revenue kept from the starting customers after cancellations, downgrades and upgrades, so upgrades can push it above 100%."
**Explain simply:**
- Logo retention = customers still there / customers at start.
- NRR = (starting revenue - churn - downgrades + expansion) / starting revenue, using only customers present at the start.
- Example: 10 customers, Rs 100 monthly revenue. One cancels (Rs 10), downgrades Rs 5, others upgrade by Rs 25. Logo retention = 9/10 = 90%. NRR = (100 - 10 - 5 + 25) / 100 = 110%. Gross revenue retention (without expansion) = 85%.
- NRR above 100% means the existing base grows even with zero new customers, which happens when seat or usage growth outweighs losses.
**Practice step:** Recompute with expansion Rs 5: NRR is 90%.
**Likely follow-ups:** (1) Can logos fall while NRR rises? Yes, if a few big customers expand. (2) Risk? Dependence on a few accounts.
**Common mistakes / traps:** Including new customers in NRR; ignoring that great NRR can hide high logo churn.

### Q80 ⭐ 🟡 A company has 20,000 customers at the start of a year and 22,500 at the end. 5,000 were new during the year. How many were lost, what is the annual churn, and what monthly churn does that approximate?
**Asked at:** commonly asked (no company-specific report found); churn arithmetic is typical on SaaS analyst lists (unverified).
**What the interviewer is checking:** Rebuilding the flow and using the right denominator.
**Say this in the interview:** "End = start + new - lost, so lost = 20,000 + 5,000 - 22,500 = 2,500. Annual churn = 2,500 / 20,000 = 12.5%, about 1.1% a month."
**Definition in plain words:** Churn rate = customers lost during a period / customers at the start of the period.
**Worked answer:**
1. Lost = 20,000 + 5,000 - 22,500 = 2,500.
2. Annual churn = 2,500 / 20,000 = 12.5%.
3. Monthly churn: compound form, 1 - (1 - 0.125)^(1/12) = 1.11%. Quick form, 12.5% / 12 = 1.04%.
**Result:** 2,500 lost; 12.5% annual; about 1.0 to 1.1% monthly.
**Check:** Retained = 20,000 - 2,500 = 17,500; plus 5,000 new = 22,500. Using the average base of 21,250 gives 11.8%, a variation.
**Caveats:** The 2,500 lost includes anyone who joined during the year and also left it, so the churn of the opening base alone cannot be separated without customer records. Denominator choice (start, average) changes the figure; state it. Dividing by 12 slightly understates the compound monthly rate.
**Likely follow-ups:** (1) Growth? 22,500 / 20,000 = 12.5% net growth. (2) Annual from monthly 1.1%? 1 - 0.989^12 is about 12.5%.
**Common mistakes / traps:** Using end customers as the base; treating net adds (2,500) as the lost count.

### Q81 ⭐ 🟡 A subscription app gives a first-month discount. Month-1 retention of discounted users is 25% and of full-price users 40%. Explain how this affects the LTV comparison and what you would do to evaluate the discount.
**Asked at:** commonly asked (no company-specific report found); a typical pricing-promotion metric case, unverified for any company.
**What the interviewer is checking:** Whether you compare value per signup, not retention alone, and think about selection bias.
**Say this in the interview:** "Lower retention does not automatically kill the discount: compare LTV per signup, including more signups from the offer, against CAC. And I would test it with randomisation because discount-seekers are a different crowd."
**Clarify first:** "Month-1 retention" here means share still subscribed after month 1. Discount depth? Margin? Were users randomly assigned?
**Structure:** LTV per signup = first-month revenue + P(retain) x expected later revenue. Compare with the extra signups the discount brings.
**What I would check, in order:** A/B test (random split of new users) on 90-day and 6-month retention and revenue; later-month retention among the retained (does the gap shrink?); signup volume uplift; refunds and support load.
**If the data shows...:** retained discount users later behave like full-price users means the gap is only less-committed users; discount may be worth it if extra volume is high. Persistently worse behaviour means the offer attracts deal-seekers.
**Numeric work (assumed: full price Rs 100 a month; discounted first month Rs 50; later churn 10% a month so a retained user pays about 10 more months; margin ignored):** Per 100 signups, discounted: 100 x 50 + 25 x 100 x 10 = Rs 30,000, i.e. Rs 300 per signup. Full price: 100 x 100 + 40 x 100 x 10 = Rs 50,000, i.e. Rs 500 per signup. The discount group earns 60% as much per signup, so it needs about 500 / 300 = 1.67 times as many signups (at equal CAC) to break even.
**Recommendation:** Run a randomised test, judge on 90-day revenue per original visitor, and keep the discount only if extra signups beat the 1.67x hurdle, otherwise test a smaller discount.
**Likely follow-ups:** (1) Why not compare the two existing groups? Self-selection; different users. (2) Other effects? Brand price anchoring.
**Common mistakes / traps:** Comparing retention and ignoring volume; comparing non-random groups.

### Q82 ⭐ 🟡 How would you set up the metrics for an internal HR dashboard so that attrition is shown fairly across teams of different sizes?
**Asked at:** commonly asked (no company-specific report found); HR metric formulas appear on HR-analytics prep sites only (unverified).
**What the interviewer is checking:** Rates not counts, a fair denominator, and awareness of small-number noise.
**Say this in the interview:** "I would show attrition as a rate, leavers over average headcount, on a rolling 12 months, always next to the counts, and flag small teams as low reliability instead of ranking them next to large teams."
**Definition in plain words:** Attrition rate = leavers in the period / average headcount in the period (average of start and end, or monthly average), annualised.
**Worked answer:**
1. Use rates: Team A has 10 people and 2 leavers = 20%; Team B has 200 people and 30 leavers = 15%.
2. Reliability: if the true rate were 15% for both, the typical random swing in leavers is about 1.1 people for Team A (plus or minus about 11 percentage points) and about 5 people for Team B (plus or minus about 2.5 points). So 20% in Team A is within normal noise.
3. Design: rolling 12 months; show leavers, average headcount, rate; compare with the company rate; show a "small team" tag below, say, 30 people; split into voluntary and involuntary, and regretted (good performers); add tenure bands (first-year attrition).
4. Slice with the same definitions everywhere; exclude interns or contractors consistently.
**Result:** Rates with counts and a reliability flag; no raw leaver ranking.
**Check:** Roll up: team leavers must add to the company total.
**Caveats:** Definitions vary (some use start headcount); small teams need longer windows; protect privacy by suppressing groups of very few people.
**Likely follow-ups:** (1) Why not sort teams by rate? Small teams would dominate the top and bottom by chance. (2) Alternative view? A funnel-plot style chart: a band around the company rate that is wider for small teams, so only teams outside the band stand out.
**Common mistakes / traps:** Showing counts; using end headcount; annualising one month.

### Q83 ⭐ 🟡 How would you measure the success of a loyalty programme (for example a subscription like Swiggy One) using metrics?
**Asked at:** commonly asked (no company-specific report found); Swiggy analyst guides mention retention, AOV and LTV topics (prep guides, unverified); no claim about any real programme's details is made here.
**What the interviewer is checking:** Incrementality, not just member-versus-non-member comparison, and programme economics.
**Say this in the interview:** "Success is the extra profit the programme causes: incremental orders and retention from members, minus fees given up and benefits paid, measured against a comparable group, not just members versus non-members."
**Clarify first:** What does the membership give (free delivery, discounts) and cost? What is the goal: frequency, retention, or share of wallet?
**Structure:** Adoption (penetration, sign-ups, renewal rate) then behaviour (orders per month, order value, retention) then economics (fee revenue, benefit cost, contribution per member) with guardrails (non-member experience, margin leakage).
**What I would check, in order:** member count and renewal rate; member orders versus a matched or randomly held-out control; retention curve difference; contribution per member including benefits.
**If the data shows...:** members order more only because heavy users self-select means no real lift; a lift in the controlled group and positive contribution means scale it; high sign-ups but low use means benefits unattractive.
**Numeric work (assumed):** Members order 7 times a month versus 4 for non-members, but a matched control suggests the programme causes only 2 extra orders. Contribution Rs 40 per order, fee income Rs 50 per member per month, benefit cost Rs 20 per order on all 7 orders (Rs 140). Raw view: 3 x 40 + 50 - 140 = +Rs 30. Incremental view: 2 x 40 + 50 - 140 = -Rs 10. The naive comparison says profit; the fair one says a small loss.
**Recommendation:** Run a holdout test, report contribution per member, and redesign benefits (for example thresholds) if negative.
**Likely follow-ups:** (1) Why a holdout? To remove self-selection. (2) Long-term value? Include retention and lifetime.
**Common mistakes / traps:** Crediting all member orders to the programme; ignoring benefit cost.

### Q84 ⭐ 🔴 Explain why LTV should use gross margin and a discount rate, and recompute the simple LTV for ARPU Rs 500 per month, 50% gross margin, 5% monthly churn, with a 1% monthly discount rate.
Use LTV = monthly margin / (churn + discount rate) as the discounted perpetuity approximation.
**Asked at:** commonly asked (no company-specific report found); LTV and CAC payback are named on SaaS prep blogs (unverified).
**What the interviewer is checking:** Why profit, not revenue, and why future money is worth less.
**Say this in the interview:** "Margin per month is Rs 250; churn plus discount is 6%; LTV = 250 / 0.06, about Rs 4,167, against Rs 10,000 if you wrongly use revenue and ignore discounting."
**Definition in plain words:** LTV = the present value of profit a customer is expected to bring. Margin, not revenue, because costs of serving use up part of each rupee. Discount, because Rs 100 received in a year is worth less today (cost of capital and risk).
**Worked answer:**
1. Monthly margin = 500 x 50% = Rs 250.
2. Churn + discount rate = 5% + 1% = 6% = 0.06.
3. LTV = 250 / 0.06 = Rs 4,166.67.
**Result:** About Rs 4,167 (rounded).
**Check:** Without discounting: 250 / 0.05 = Rs 5,000 (lifetime 1/0.05 = 20 months). Revenue-based and undiscounted: 500 / 0.05 = Rs 10,000. So the naive number is 2.4 times too high.
**Caveats:** The formula assumes constant churn and constant margin; real churn is high early and lower later. The 1% monthly rate is assumed (about 12.7% a year); choose a rate your finance team uses. Cash-in-hand view: include CAC separately (Q85).
**Likely follow-ups:** (1) Does a higher discount rate lower LTV? Yes. (2) Why ignore the discount rate in quick calculations? It is a small change for short lifetimes.
**Common mistakes / traps:** Using ARPU not margin; using 1/churn lifetime times revenue; adding discount rate as a multiplier.

### Q85 ⭐ 🔴 Two growth teams disagree: one wants to cut CAC by 20% using cheaper channels, the other wants to raise ARPU by 10%. Using LTV:CAC and payback, how do you decide?
**Asked at:** commonly asked (no company-specific report found); CAC, LTV and payback are listed topics for Swiggy-style business analyst prep (unverified).
**What the interviewer is checking:** Whether you compute both options and consider side effects on churn.
**Say this in the interview:** "I would put both on the same baseline and compute LTV:CAC and payback, then check what each does to churn: cheaper channels often bring lower quality users, and a price rise can raise churn."
**Clarify first:** Baseline CAC, ARPU, margin, churn; how the price rise would be done; which channels are cheaper and how those users behave.
**Structure:** LTV = monthly margin / churn; LTV:CAC; payback months = CAC / monthly margin; then stress each lever's side effect.
**What I would check, in order:** test the cheaper channels on a small budget and read 60-day retention; test price on a subset and read churn and conversion; compare cohort LTV:CAC.
**Numeric work (assumed baseline: ARPU Rs 500, margin 50% = Rs 250, churn 5%, CAC Rs 3,000):**
- Baseline: LTV = 250 / 0.05 = Rs 5,000; LTV:CAC = 1.67; payback = 3,000 / 250 = 12 months.
- Option 1, CAC down 20% to Rs 2,400, same quality: LTV:CAC = 2.08; payback = 9.6 months.
- Option 2, ARPU up 10% to Rs 550 (costs unchanged, margin Rs 300): LTV = Rs 6,000; LTV:CAC = 2.0; payback = 10 months. (If costs also rise by 10%, margin Rs 275: 1.83 and 10.9 months.)
- Break-even for option 1: if cheaper users churn above 6.25% a month (25% worse), LTV falls to 4,000 and LTV:CAC returns to 1.67, no better than baseline.
- Break-even for option 2: if the price rise lifts churn to 6% or more, LTV:CAC returns to 1.67 or below.
**If the data shows...:** cheaper-channel users keep similar retention means option 1 wins slightly (2.08 versus 2.0) and is faster for cash; after a price rise, churn below 6% (up by less than 20%) still beats the baseline, but option 2 only catches option 1 if churn does not rise at all (it would need to fall to about 4.8%). Both together are possible and independent.
**Recommendation:** The two are close on paper, so run small tests, pick by the measured churn effect, and favour the one with shorter payback if cash is tight.
**Likely follow-ups:** (1) Which suits a cash-poor startup? Shorter payback. (2) Can both be done? Yes, check interaction.
**Common mistakes / traps:** Assuming unchanged churn; using revenue instead of margin; ignoring payback.

### Q86 ⭐ 🔴 A marketplace's take rate rose from 18% to 22% and GMV grew 5%. Seller churn doubled. How do you judge whether the take-rate change was worthwhile?
**Asked at:** commonly asked (no company-specific report found); primary-metric trade-off cases are described for Flipkart in an Interview Query guide (unverified); no report of this exact take-rate question was found.
**What the interviewer is checking:** Short-term revenue gain versus long-term seller supply and lifetime value.
**Say this in the interview:** "Revenue looks up about 28% now, but sellers are the supply; doubled churn halves their expected lifetime, so I would compare seller lifetime profit before and after, and check whether GMV growth will hold."
**Clarify first:** Take rate = commission as a share of GMV (gross merchandise value, the total value of goods sold). What was the churn level, which sellers left (big or small), and did prices or conversion change?
**Structure:** Immediate revenue effect; supply and quality effect (churn, who leaves); long-term effect (lifetime value, GMV trend, buyer experience); alternatives.
**What I would check, in order:** revenue by seller size; churned sellers' share of GMV; category and search coverage; GMV per remaining seller; buyer repeat and prices.
**Numeric work (index GMV 100; assumed seller churn from 2% to 4% a month):**
- Revenue: before 100 x 18% = 18; after 105 x 22% = 23.1, up 28.3%.
- Seller lifetime: 1 / 0.02 = 50 months versus 1 / 0.04 = 25 months.
- Seller lifetime value per unit of GMV per month: 0.18 / 0.02 = 9.0 before; 0.22 / 0.04 = 5.5 after, down 39%.
- Break-even: churn can only rise to 0.22 / 9 = 2.44% (about 22% higher) before lifetime value is lower. Doubling is far past that.
**If the data shows...:** churned sellers are small, low-GMV ones and category coverage holds means worth it; churn is among top sellers or in key categories means damaging; GMV growth fades after a few months means the supply loss is now showing.
**Recommendation:** Do not judge on this quarter's revenue. Try a tiered take rate (lower for top or new sellers), run a test by category, and track seller retention, GMV per seller and supply coverage.
**Likely follow-ups:** (1) How to test? Randomise by region or category. (2) Why was GMV still up? Lag effect, sellers leave gradually.
**Common mistakes / traps:** Celebrating revenue alone; treating all churned sellers as equal; ignoring that part of the GMV growth would have come anyway.

### Q87 ⭐ 🔴 You are asked to design the 5 most important weekly KPIs for the CEO of a new Indian edtech startup. Which would you choose and why?
**Asked at:** commonly asked (no company-specific report found); KPI and dashboard-design questions are reported for firms such as Tiger Analytics and Flipkart (prep sources, unverified).
**What the interviewer is checking:** Choosing a few connected metrics across the funnel with clear definitions, not a long list.
**Say this in the interview:** "I would pick five that cover the full journey: new paying students, lead-to-paid conversion, learning activity, retention or renewal, and CAC payback, each with a precise definition and a guardrail."
**Clarify first:** What does the business sell (courses, subscription, live classes)? Stage (finding fit or scaling)? Who sees it, and what decisions follow weekly?
**Structure:** Growth, conversion, engagement (the product working), retention, economics.
**What I would check, in order (the five KPIs):**
1. Weekly new paid enrolments and revenue: the headline outcome.
2. Lead-to-paid conversion (and trial-to-paid): shows funnel quality. Example (assumed): 10,000 leads, 400 paid = 4%.
3. Weekly active learners: share of enrolled students completing at least a set number of lessons or classes; the true usage signal, and it predicts renewals and learning outcomes.
4. Cohort retention or renewal and refund rate: do students stay or ask for money back.
5. CAC and payback: marketing spend / new paid students. Example: Rs 20 lakh spend / 400 = Rs 5,000. If price Rs 12,000 at 70% margin gives Rs 8,400, LTV:CAC = 1.68 on one purchase.
**If the data shows...:** conversion falling with leads rising means low-quality traffic; high enrolment but low activity means refunds and churn are coming; payback lengthening means slow spending.
**Recommendation:** One page, five numbers with week-on-week change and a four-week trend, plus guardrails (refund rate, student satisfaction, learning outcome) in a drill-down, not on the CEO page.
**Likely follow-ups:** (1) Why not total downloads? Vanity (Q71). (2) A North Star? Weekly active learners completing a learning goal, if one must be chosen.
**Common mistakes / traps:** Too many KPIs; revenue without engagement; no definitions; counting enrolments instead of paid ones.

