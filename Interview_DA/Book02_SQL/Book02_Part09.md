# Book 2 — SQL | Part 9: Retention, Cohorts, Funnels, MoM Growth 🔴

**Target:** 40 questions | **Actual:** 46 questions
**Scope:** MoM/YoY/QoQ growth, retention and churn, cohort tables, funnel conversion, DAU/WAU/MAU, new vs repeat customers, consecutive-day activity, sessions, repeat purchase. (Generic dedupe, nth-highest, recursive CTE and optimisation sit in Part 10; plain window-function basics in Parts 5-6.)

### Q1 ⭐⭐⭐ 🟢 Using an events table (user_id, event_time), calculate DAU, WAU and MAU (daily, weekly and monthly active users). Why must you use COUNT(DISTINCT user_id)?
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 Using an orders table (order_id, order_date, amount), calculate monthly revenue and the month-over-month (MoM) growth percentage using LAG.
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 Given a funnel_events table (user_id, step: view/cart/purchase), count the users at each step and the overall conversion percentage from view to purchase.
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 Count new signups per month from a users table (user_id, signup_date) and show the change versus the previous month.
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟡 Calculate MoM growth safely: how do you handle the first month (no previous value), a previous month of zero (divide by zero) and months with no data at all?
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 Calculate month-1 retention: of the users who signed up in each month, what percentage were active again in the following month? (users + activity tables)
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 For each month, split customers into new (first ever order that month) and repeat (ordered before), with their counts and revenue.
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 Find customers who bought in January but not in February (lost customers), and explain the LEFT JOIN / NOT EXISTS options.
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 Find users who were active on at least 3 consecutive days from a login table (user_id, login_date).
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 For a view -> cart -> checkout -> payment funnel, calculate the step-to-step conversion and the drop-off percentage at each stage.
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 Build a monthly cohort retention table: rows = signup month (cohort), columns = months since signup (0, 1, 2, ...), values = number of active users.
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 Calculate year-over-year (YoY) growth in monthly revenue by comparing each month with the same month last year.
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🔴 Calculate weekly retention by cohort using window functions: for each signup week, the percentage of users active in week 0, 1, 2, 3 ...
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐ 🟢 Calculate the repeat purchase rate: the percentage of customers who placed more than one order.
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐ 🟢 Calculate stickiness (DAU/MAU ratio) for a given month and explain what a good value means.
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟢 Calculate the signup-to-activation conversion rate: the percentage of signed-up users who completed a first key action (e.g. first order) within 7 days.
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟢 Calculate the average number of orders per active customer per month.
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟡 Find the average number of days between a customer's first and second order.
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟡 Calculate the monthly churn rate: customers active last month who were not active this month, as a percentage of last month's active customers.
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 Find users who were active in the past but have had no activity in the last 30 days (inactive/at-risk users) relative to a reference date.
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 Find reactivated (resurrected) users: customers who were inactive for 60+ days and then came back.
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 Calculate rolling 7-day active users for every date (a user is counted once in the window).
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 Find the product categories with the highest MoM revenue growth last month, ignoring tiny-base categories.
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 Calculate quarter-over-quarter (QoQ) revenue growth, including fiscal quarters (April-March) for Indian companies.
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 Compare funnel conversion across segments (device, city or acquisition channel) in one query and identify the weakest segment.
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 Calculate sessions per user and average session duration from a sessions table (session_id, user_id, start_time, end_time).
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 Calculate Day-1 and Day-7 retention: the percentage of new users who returned exactly 1 day and 7 days after signup.
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 Calculate cumulative new customers over time (running total by month) and the cumulative share of total.
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 Calculate cumulative revenue per signup cohort by month since signup (a simple customer lifetime value curve).
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 Find customers who ordered in 3 consecutive months.
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🔴 Build sessions from raw events: start a new session when a user is idle for more than 30 minutes (sessionization with LAG and a running SUM).
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🔴 Build a monthly active-user bridge: for each month, count new, retained, resurrected and churned users, and check that they reconcile to MAU.
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🔴 Calculate a strict-order funnel: count a user at 'purchase' only if the purchase happened after the 'cart' event, which happened after the 'view' event.
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🔴 Produce a cohort retention table as percentages in pivot form (one column per month since signup) using conditional aggregation.
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🔴 Calculate rolling N-day (bracket) retention: the percentage of users who were active on or after day N, versus classic day-N retention. Explain the difference.
<!-- ANSWER_PENDING -->

### Q36 ⭐ 🟡 Find the median time taken by users to go from signup to first purchase.
<!-- ANSWER_PENDING -->

### Q37 ⭐ 🟡 Calculate week-over-week (WoW) growth correctly across the year boundary (week 52/53 to week 1).
<!-- ANSWER_PENDING -->

### Q38 ⭐ 🟡 Compare retention across acquisition channels (e.g. organic, paid, referral) using the same cohort logic.
<!-- ANSWER_PENDING -->

### Q39 ⭐ 🟡 For a quick-commerce app, calculate the percentage of customers who reorder within 30 days of their first order.
<!-- ANSWER_PENDING -->

### Q40 ⭐ 🟡 Clean raw event logs before computing active users: remove duplicate events, null user_ids and test accounts. What checks do you run?
<!-- ANSWER_PENDING -->

### Q41 ⭐ 🔴 Handle incomplete cohorts: how do you avoid showing artificially low retention for recent cohorts that have not yet had time to return?
<!-- ANSWER_PENDING -->

### Q42 ⭐ 🔴 Calculate net revenue retention (NRR): revenue this month from customers who existed last month, divided by their revenue last month.
<!-- ANSWER_PENDING -->

### Q43 ⭐ 🔴 Given a subscriptions table (user_id, start_date, end_date), count active subscribers at the end of each month, including months with no events (generated calendar).
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🔴 Find peak concurrent users: given session start and end times, find the time with the most overlapping sessions.
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🔴 Find customers whose monthly spend increased every month for at least 3 months in a row.
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🔴 Find the largest gap (in days) between two consecutive visits for each user, and flag users with a gap above 30 days.
<!-- ANSWER_PENDING -->
