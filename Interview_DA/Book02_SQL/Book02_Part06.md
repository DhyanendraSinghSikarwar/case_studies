# Book 2 — SQL | Part 6: Window functions — running totals, LAG/LEAD, moving averages 🟡

- **Target:** 50 questions (minimum)
- **Actual:** 52 questions
- **Scope:** window mechanics — OVER(), PARTITION BY, ORDER BY in windows, frames (ROWS vs RANGE), running and moving calculations, LAG/LEAD, FIRST_VALUE/LAST_VALUE/NTH_VALUE, NTILE, percent-of-total. Excludes ROW_NUMBER/RANK/top-N (Part 5) and retention/cohorts/funnels/MoM growth business cases (Part 9).

### Q1 ⭐⭐⭐ 🟢 What does an empty OVER() clause do? For example, SUM(salary) OVER() next to every employee row.
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 What does PARTITION BY do inside OVER(), and how is it different from GROUP BY?
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 What does ORDER BY inside OVER() do, and how does it change the result of SUM()?
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 What do LAG() and LEAD() do? Explain the difference in plain words.
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 How do you calculate a running (cumulative) total of daily sales?
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 Why does LAG() return NULL on the first row, and how do you replace it with a default value?
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 Show each month's sales next to the previous month's sales and the difference between them (LAG mechanics).
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 How do you calculate a running total that restarts for each group, such as each department or each customer?
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 How do you calculate a 3-day or 7-day moving average using ROWS BETWEEN?
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 What is the difference between ROWS and RANGE in a window frame?
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 What is the default window frame when ORDER BY is present, and why can a running total show wrong numbers when two rows share the same date?
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 Where do window functions sit in the SQL order of execution (relative to WHERE, GROUP BY, HAVING, SELECT, ORDER BY)?
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 How do you show each row's share of the total (percentage of total) using SUM() OVER()?
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🔴 How do you write a 7-day moving average that shows NULL until a full 7 days of data exist?
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐ 🟢 What is a window frame? Explain UNBOUNDED PRECEDING, CURRENT ROW and UNBOUNDED FOLLOWING in plain words.
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟢 What do FIRST_VALUE() and LAST_VALUE() do?
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟢 What does NTILE(n) do? Give an example.
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟢 How do you add a count of employees per department to every employee row using COUNT(*) OVER()?
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟢 How do you use LAG() or LEAD() with an offset of 2 or more rows back or forward?
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟢 Name the main categories of window functions (ranking, value, aggregate) and one example of each.
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 Why does LAST_VALUE() often return the current row's value, and how do you fix it?
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 How do you compute the number of days between each customer's consecutive orders?
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 How do you flag each row as increased, decreased or unchanged compared with the previous row?
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 How do you show each employee's salary minus the average salary of their department?
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 How do you split customers into quartiles (4 equal groups) by total spend using NTILE?
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 How do you calculate a running count of orders per customer?
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 How do you calculate a cumulative percentage of total (running share)?
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 How do you find each customer's first order date and show it on every row without GROUP BY?
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 How do you use LEAD() to find the next login date or next event for each user?
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 How do you calculate a running maximum or running minimum?
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 How do you calculate a running average (average of all rows from the start to the current row)?
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 How do you compare each month with the same month last year using LAG(12) or a self-join, and what breaks if a month is missing?
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 How do you calculate percent change safely when the previous value is zero or NULL (NULLIF)?
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 How do you use PARTITION BY with more than one column?
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 What is the named WINDOW clause, and when does it make queries shorter?
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🟡 How do you compute a window function on top of GROUP BY results (for example, running total of monthly totals)?
<!-- ANSWER_PENDING -->

### Q37 ⭐⭐ 🟡 Show each employee's salary and the salary of the next higher-paid employee in the same department using LEAD().
<!-- ANSWER_PENDING -->

### Q38 ⭐⭐ 🟡 What is the pandas equivalent of cumsum, shift and rolling for SQL running totals, LAG and moving averages?
<!-- ANSWER_PENDING -->

### Q39 ⭐ 🟢 What are PERCENT_RANK() and CUME_DIST(), and how do they differ from NTILE?
<!-- ANSWER_PENDING -->

### Q40 ⭐ 🟡 How do you compute a 7-day moving sum when some dates are missing, using RANGE with an INTERVAL?
<!-- ANSWER_PENDING -->

### Q41 ⭐ 🟡 How do you calculate a running total of only some rows, such as only refunds, using a CASE inside the window function?
<!-- ANSWER_PENDING -->

### Q42 ⭐ 🟡 How do you calculate a moving average of the previous 3 days that excludes the current day?
<!-- ANSWER_PENDING -->

### Q43 ⭐ 🟡 What does NTH_VALUE() do, and how is it different from FIRST_VALUE()?
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🟡 What is the GROUPS frame type, and when would it differ from ROWS and RANGE?
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🟡 How do you fill NULLs with the last known value (forward fill) using window functions?
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🔴 How do you calculate a running bank balance from deposits and withdrawals, and find the first date it went negative?
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🔴 How do you detect three consecutive days of increasing stock price using LAG()?
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🔴 How do you calculate a running total that resets when a condition is met (for example, when a limit is crossed)?
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🔴 How do you calculate a median per group using window functions (PERCENTILE_CONT) and what is the alternative in MySQL?
<!-- ANSWER_PENDING -->

### Q50 ⭐ 🔴 How do you calculate an exponential moving average in SQL, and why is it hard?
<!-- ANSWER_PENDING -->

### Q51 ⭐ 🔴 How do you find rows where the value is greater than both the previous and the next row (local peaks) using LAG and LEAD?
<!-- ANSWER_PENDING -->

### Q52 ⭐ 🔴 How do you calculate a running distinct count (for example, new unique customers so far), given COUNT(DISTINCT) is not allowed in window frames?
<!-- ANSWER_PENDING -->

