# Book 2 — SQL | Part 6: Window functions — running totals, LAG/LEAD, moving averages 🟡

- **Target:** 50 questions (minimum)
- **Actual:** 52 questions
- **Scope:** window mechanics — OVER(), PARTITION BY, ORDER BY in windows, frames (ROWS vs RANGE), running and moving calculations, LAG/LEAD, FIRST_VALUE/LAST_VALUE/NTH_VALUE, NTILE, percent-of-total. Excludes ROW_NUMBER/RANK/top-N (Part 5) and retention/cohorts/funnels/MoM growth business cases (Part 9).

### Q1 ⭐⭐⭐ 🟢 What does an empty OVER() clause do? For example, SUM(salary) OVER() next to every employee row.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know a window function can add a whole-table number to every row without collapsing rows?
**Say this in the interview:** An empty OVER() means the window is the whole result set, so SUM(salary) OVER() gives the company payroll and repeats it on every employee row, and no rows are lost.
**Explain simply:**
- A **window function** does a calculation across a set of rows (the "window") but keeps every original row. GROUP BY, in contrast, squashes rows into one per group.
- `OVER()` with nothing inside means: no partition, no ordering, so the window is all rows.
- So each row sees the same total, which is handy for "this salary vs the company total".
**Example:** Payroll is 520,000 across 8 employees; each row shows its own salary plus 520,000 beside it.
**Sample data:**

`employees`

| emp_id | name | dept | salary |
|---|---|---|---|
| 1 | Asha | HR | 50000 |
| 2 | Bala | HR | 60000 |
| 3 | Chitra | HR | 60000 |
| 4 | Dev | Sales | 45000 |
| 5 | Esha | Sales | 70000 |
| 6 | Farid | IT | 80000 |
| 7 | Gita | IT | 90000 |
| 8 | Hari | IT | 65000 |

**SQL:**
```sql
-- Runs on PostgreSQL, MySQL 8+, SQL Server, SQLite 3.25+ (window functions need these versions)
SELECT name, salary,
       SUM(salary) OVER () AS total_payroll
FROM employees
ORDER BY emp_id;
```
**Output:**

| name | salary | total_payroll |
|---|---|---|
| Asha | 50000 | 520000 |
| Bala | 60000 | 520000 |
| Chitra | 60000 | 520000 |
| Dev | 45000 | 520000 |
| Esha | 70000 | 520000 |
| Farid | 80000 | 520000 |
| Gita | 90000 | 520000 |
| Hari | 65000 | 520000 |

**pandas equivalent:**
```python
res = emp[['name','salary']].copy()
res['total_payroll'] = emp['salary'].sum()
```
**Edge cases:** NULL salaries are ignored by SUM (they do not break it). An empty table returns no rows. SUM over only NULLs gives NULL.
**Likely follow-ups:** 1) Can you also show the average? Yes, AVG(salary) OVER () in the same SELECT. 2) How is this different from a subquery `(SELECT SUM(salary) FROM employees)`? Same value, but the window version is shorter and extends easily to PARTITION BY.
**Common mistakes:** Adding a plain column next to SUM() without OVER and getting a GROUP BY error; thinking OVER() reduces the row count.

### Q2 ⭐⭐⭐ 🟢 What does PARTITION BY do inside OVER(), and how is it different from GROUP BY?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know PARTITION BY splits rows into groups for the calculation but, unlike GROUP BY, keeps every row?
**Say this in the interview:** PARTITION BY cuts the window into groups, for example one per department, and the calculation restarts in each group. GROUP BY gives one row per group; PARTITION BY keeps every employee row.
**Explain simply:**
- **PARTITION BY dept** = "treat each department as its own mini-table for this calculation".
- **GROUP BY** collapses rows, so you lose the employee names. PARTITION BY keeps them.
- Use GROUP BY for a summary report, PARTITION BY when you need detail and group numbers side by side.
**Example:** HR has 170,000 total salary across 3 people. With PARTITION BY every HR employee row shows 170,000; with GROUP BY you only get one HR row.
**Sample data:**

`employees` (same 8 rows as Q1)
**SQL:**
```sql
-- Runs on PostgreSQL, MySQL 8+, SQL Server, SQLite 3.25+ (window functions need these versions)
SELECT name, dept, salary,
       SUM(salary) OVER (PARTITION BY dept) AS dept_total
FROM employees
ORDER BY emp_id;
```

For comparison, the GROUP BY version of the same total (not run in the answer's main query):
```sql
SELECT dept, SUM(salary) AS dept_total FROM employees GROUP BY dept ORDER BY dept;
```
GROUP BY output (3 rows only, employee detail is lost):

| dept | dept_total |
|---|---|
| HR | 170000 |
| IT | 235000 |
| Sales | 115000 |

**Output:**

| name | dept | salary | dept_total |
|---|---|---|---|
| Asha | HR | 50000 | 170000 |
| Bala | HR | 60000 | 170000 |
| Chitra | HR | 60000 | 170000 |
| Dev | Sales | 45000 | 115000 |
| Esha | Sales | 70000 | 115000 |
| Farid | IT | 80000 | 235000 |
| Gita | IT | 90000 | 235000 |
| Hari | IT | 65000 | 235000 |

**pandas equivalent:**
```python
res = emp[['name','dept','salary']].copy()
res['dept_total'] = emp.groupby('dept')['salary'].transform('sum')
```
**Edge cases:** NULL in the partition column forms its own group. A group with one row simply shows its own value.
**Likely follow-ups:** 1) Can you use both together? Yes, GROUP BY runs first, then the window runs over the grouped result. 2) Can you partition by two columns? Yes, PARTITION BY dept, grade.
**Common mistakes:** Using GROUP BY and then wondering where the names went; forgetting that the window value repeats on every row so summing it again double-counts.

### Q3 ⭐⭐⭐ 🟢 What does ORDER BY inside OVER() do, and how does it change the result of SUM()?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know ORDER BY inside OVER makes SUM a running total (default frame), not a grand total?
**Say this in the interview:** Without ORDER BY, SUM() OVER() is the grand total on every row. Add ORDER BY and each row sums from the first row up to itself, which gives a running total.
**Explain simply:**
- ORDER BY inside OVER sorts rows only for the window; it does not sort your final output (add a normal ORDER BY for that).
- Once ordered, the default window becomes "from the start up to the current row" (more precisely RANGE, see Q11).
- So the same SUM changes meaning purely because of ORDER BY.
**Example:** Daily sales of 100, 120, 80: the running total reads 100, 220, 300.
**Sample data:**

`daily_sales`

| sale_date | amount |
|---|---|
| 2024-01-01 | 100 |
| 2024-01-02 | 120 |
| 2024-01-03 | 80 |
| 2024-01-04 | 150 |
| 2024-01-05 | 200 |
| 2024-01-06 | 90 |
| 2024-01-07 | 110 |
| 2024-01-08 | 130 |

**SQL:**
```sql
-- Runs on PostgreSQL, MySQL 8+, SQL Server, SQLite 3.25+ (window functions need these versions)
SELECT sale_date, amount,
       SUM(amount) OVER ()                    AS grand_total,
       SUM(amount) OVER (ORDER BY sale_date)  AS running_total
FROM daily_sales
ORDER BY sale_date;
```
**Output:**

| sale_date | amount | grand_total | running_total |
|---|---|---|---|
| 2024-01-01 | 100 | 980 | 100 |
| 2024-01-02 | 120 | 980 | 220 |
| 2024-01-03 | 80 | 980 | 300 |
| 2024-01-04 | 150 | 980 | 450 |
| 2024-01-05 | 200 | 980 | 650 |
| 2024-01-06 | 90 | 980 | 740 |
| 2024-01-07 | 110 | 980 | 850 |
| 2024-01-08 | 130 | 980 | 980 |

**pandas equivalent:**
```python
res = ds.sort_values('sale_date').copy()
res['grand_total'] = res['amount'].sum()
res['running_total'] = res['amount'].cumsum()
```
**Edge cases:** If two rows have the same sort value, the default frame treats them as peers and both show the same running total (Q11). NULL amounts are skipped.
**Likely follow-ups:** 1) Is it the final sort order? No. 2) How to be exact? Write the frame: ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW.
**Common mistakes:** Assuming the output is sorted by the OVER ORDER BY; expecting the grand total once ORDER BY is added.

### Q4 ⭐⭐⭐ 🟢 What do LAG() and LEAD() do? Explain the difference in plain words.
**Asked at:** reported at Indium Software (data analyst) per AmbitionBox, Feb 2024: window function question naming LEAD/LAG (research/Book02_Part06_sources.md); otherwise commonly asked
**What the interviewer is checking:** Can you explain looking backward vs forward across rows in plain words?
**Say this in the interview:** LAG looks at an earlier row and LEAD looks at a later row, in the order I specify. LAG(amount) is yesterday's amount and LEAD(amount) is tomorrow's, both shown on today's row.
**Explain simply:**
- **LAG(col, n)** = value from n rows before (default n = 1).
- **LEAD(col, n)** = value from n rows after.
- Rows that have no previous (first) or next (last) row get NULL.
- Needs ORDER BY inside OVER, otherwise "previous" has no meaning.
**Example:** On 3 Jan sales were 80; yesterday 120 (LAG), tomorrow 150 (LEAD).
**Sample data:**

`daily_sales` (8 rows, see Q3)
**SQL:**
```sql
-- Runs on PostgreSQL, MySQL 8+, SQL Server, SQLite 3.25+ (window functions need these versions)
SELECT sale_date, amount,
       LAG(amount)  OVER (ORDER BY sale_date) AS prev_day,
       LEAD(amount) OVER (ORDER BY sale_date) AS next_day
FROM daily_sales
ORDER BY sale_date;
```
**Output:**

| sale_date | amount | prev_day | next_day |
|---|---|---|---|
| 2024-01-01 | 100 | NULL | 120 |
| 2024-01-02 | 120 | 100 | 80 |
| 2024-01-03 | 80 | 120 | 150 |
| 2024-01-04 | 150 | 80 | 200 |
| 2024-01-05 | 200 | 150 | 90 |
| 2024-01-06 | 90 | 200 | 110 |
| 2024-01-07 | 110 | 90 | 130 |
| 2024-01-08 | 130 | 110 | NULL |

**pandas equivalent:**
```python
res = ds.sort_values('sale_date').copy()
res['prev_day'] = res['amount'].shift(1)
res['next_day'] = res['amount'].shift(-1)
```
**Edge cases:** First row LAG is NULL, last row LEAD is NULL. If a date is missing, LAG still takes the previous existing row, not the previous calendar day.
**Likely follow-ups:** 1) Can I jump 2 rows? LAG(amount, 2). 2) Can I set a default? LAG(amount, 1, 0). 3) Is there a way to partition? Yes, PARTITION BY customer.
**Common mistakes:** Forgetting ORDER BY inside OVER; mixing up the direction; assuming a missing calendar day is handled.

### Q5 ⭐⭐⭐ 🟢 How do you calculate a running (cumulative) total of daily sales?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you write the most common window pattern, a running total, with a clear frame?
**Say this in the interview:** I use SUM(amount) OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW). It adds every row from the first day up to the current day.
**Explain simply:**
- A **running (cumulative) total** is the sum so far; it only grows if amounts are positive.
- Writing the frame explicitly avoids the tie problem of the default RANGE frame (Q11).
- Last row of the running total equals the grand total, a good sanity check.
**Example:** Daily sales 100, 120, 80, 150: running total 100, 220, 300, 450.
**Sample data:**

`daily_sales` (see Q3)
**SQL:**
```sql
-- Runs on PostgreSQL, MySQL 8+, SQL Server, SQLite 3.25+ (window functions need these versions)
SELECT sale_date, amount,
       SUM(amount) OVER (
           ORDER BY sale_date
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_total
FROM daily_sales
ORDER BY sale_date;
```
**Output:**

| sale_date | amount | running_total |
|---|---|---|
| 2024-01-01 | 100 | 100 |
| 2024-01-02 | 120 | 220 |
| 2024-01-03 | 80 | 300 |
| 2024-01-04 | 150 | 450 |
| 2024-01-05 | 200 | 650 |
| 2024-01-06 | 90 | 740 |
| 2024-01-07 | 110 | 850 |
| 2024-01-08 | 130 | 980 |

**pandas equivalent:**
```python
res = ds.sort_values('sale_date').copy()
res['running_total'] = res['amount'].cumsum()
```
**Edge cases:** NULL amounts are skipped, so the total just carries on. Two rows on the same date: add a unique tie-breaker (e.g. id) to the ORDER BY. Missing dates simply do not appear.
**Likely follow-ups:** 1) Restart per group? Add PARTITION BY (Q8). 2) Running total in MySQL 5.7? Not available; windows need MySQL 8.0.
**Common mistakes:** Using GROUP BY with SUM and getting only one row; ordering by a non-unique column; forgetting the outer ORDER BY.

### Q6 ⭐⭐⭐ 🟢 Why does LAG() return NULL on the first row, and how do you replace it with a default value?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand why there is no row before the first one, and the 3-argument form of LAG?
**Say this in the interview:** The first row has no earlier row, so LAG has nothing to return and gives NULL. I can pass a third argument, LAG(amount, 1, 0), to supply a default, or wrap it in COALESCE.
**Explain simply:**
- NULL means "no value", and the first row truly has no previous row.
- `LAG(col, offset, default)`: the default fills in only when the row at that offset does not exist.
- `COALESCE(LAG(col) OVER(...), 0)` also replaces NULLs that were already stored in the column, so the two are not exactly the same.
- Be careful: a default of 0 may look like a real zero sale.
**Example:** Day 1 has no previous day, so prev shows NULL, or 0 if I choose that default.
**Sample data:**

`daily_sales` (see Q3)
**SQL:**
```sql
-- Runs on PostgreSQL, MySQL 8+, SQL Server, SQLite 3.25+ (window functions need these versions)
SELECT sale_date, amount,
       LAG(amount)       OVER (ORDER BY sale_date) AS prev_null,
       LAG(amount, 1, 0) OVER (ORDER BY sale_date) AS prev_default
FROM daily_sales
ORDER BY sale_date;
```
**Output:**

| sale_date | amount | prev_null | prev_default |
|---|---|---|---|
| 2024-01-01 | 100 | NULL | 0 |
| 2024-01-02 | 120 | 100 | 100 |
| 2024-01-03 | 80 | 120 | 120 |
| 2024-01-04 | 150 | 80 | 80 |
| 2024-01-05 | 200 | 150 | 150 |
| 2024-01-06 | 90 | 200 | 200 |
| 2024-01-07 | 110 | 90 | 90 |
| 2024-01-08 | 130 | 110 | 110 |

**pandas equivalent:**
```python
res = ds.sort_values('sale_date').copy()
res['prev_null'] = res['amount'].shift(1)
res['prev_default'] = res['amount'].shift(1, fill_value=0)
```
**Edge cases:** A stored NULL in the previous row stays NULL with the default form but becomes the default with COALESCE. In SQL Server 2012+, LAG also supports the default argument (not run here).
**Likely follow-ups:** 1) Does MySQL support the default argument? Yes, in 8.0. 2) Should I always use 0? No, think about whether 0 misleads a percent-change calculation.
**Common mistakes:** Treating the first-row NULL as a bug; using 0 as default and then dividing, which distorts growth numbers.

### Q7 ⭐⭐⭐ 🟡 Show each month's sales next to the previous month's sales and the difference between them (LAG mechanics).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you apply LAG to build a period-over-period difference?
**Say this in the interview:** I use LAG(sales) ordered by month to bring the previous month onto the current row, then subtract. The first month has no previous value so its change is NULL.
**Explain simply:**
- Plain subtraction between the row and its LAG gives the month-on-month change.
- You cannot reuse the alias `prev_sales` in the same SELECT, so repeat the LAG or use a CTE.
- Growth percentages are a separate topic (Q33).
**Example:** Jan 1000, Feb 1200: Feb change = 1200 - 1000 = +200; March 900 gives -300.
**Sample data:**

`monthly_sales`

| month | sales |
|---|---|
| 2024-01 | 1000 |
| 2024-02 | 1200 |
| 2024-03 | 900 |
| 2024-04 | 1500 |
| 2024-05 | 1400 |

**SQL:**
```sql
-- Runs on PostgreSQL, MySQL 8+, SQL Server, SQLite 3.25+ (window functions need these versions)
SELECT month, sales,
       LAG(sales) OVER (ORDER BY month)          AS prev_sales,
       sales - LAG(sales) OVER (ORDER BY month)  AS change
FROM monthly_sales
ORDER BY month;
```
**Output:**

| month | sales | prev_sales | change |
|---|---|---|---|
| 2024-01 | 1000 | NULL | NULL |
| 2024-02 | 1200 | 1000 | 200 |
| 2024-03 | 900 | 1200 | -300 |
| 2024-04 | 1500 | 900 | 600 |
| 2024-05 | 1400 | 1500 | -100 |

**pandas equivalent:**
```python
res = ms.sort_values('month').copy()
res['prev_sales'] = res['sales'].shift(1)
res['change'] = res['sales'] - res['prev_sales']
```
**Edge cases:** First month has NULL change. A missing month makes LAG pick the month before the gap, so the difference spans two months (Q32). Month stored as 'YYYY-MM' text sorts correctly.
**Likely follow-ups:** 1) How to show percent? 100.0 * change / NULLIF(prev,0). 2) Change per category? Add PARTITION BY.
**Common mistakes:** Using the alias in the same SELECT; sorting months as text like 'Jan','Feb' (alphabetical, not calendar).

### Q8 ⭐⭐⭐ 🟡 How do you calculate a running total that restarts for each group, such as each department or each customer?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know PARTITION BY + ORDER BY together makes a running total that restarts per group?
**Say this in the interview:** I add PARTITION BY customer and ORDER BY order_date inside OVER. The sum restarts at each new customer, so every customer has their own running total.
**Explain simply:**
- PARTITION BY defines the groups, ORDER BY defines the sequence inside each group.
- The running total resets because each partition is a separate window.
- Same idea works for department-wise running payroll or attendance counts.
**Example:** Ravi's orders 200, 300, 150 run to 200, 500, 650; Meena starts again from her own 500.
**Sample data:**

`orders`

| order_id | customer | order_date | amount |
|---|---|---|---|
| 101 | Ravi | 2024-01-05 | 200 |
| 102 | Ravi | 2024-01-20 | 300 |
| 103 | Ravi | 2024-02-10 | 150 |
| 104 | Meena | 2024-01-07 | 500 |
| 105 | Meena | 2024-02-14 | 250 |
| 106 | Meena | 2024-03-01 | 100 |

**SQL:**
```sql
-- Runs on PostgreSQL, MySQL 8+, SQL Server, SQLite 3.25+ (window functions need these versions)
SELECT customer, order_date, amount,
       SUM(amount) OVER (
           PARTITION BY customer
           ORDER BY order_date, order_id
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_total
FROM orders
ORDER BY customer DESC, order_date;
```
**Output:**

| customer | order_date | amount | running_total |
|---|---|---|---|
| Ravi | 2024-01-05 | 200 | 200 |
| Ravi | 2024-01-20 | 300 | 500 |
| Ravi | 2024-02-10 | 150 | 650 |
| Meena | 2024-01-07 | 500 | 500 |
| Meena | 2024-02-14 | 250 | 750 |
| Meena | 2024-03-01 | 100 | 850 |

**pandas equivalent:**
```python
o = orders.sort_values(['customer','order_date','order_id'])
res = o[['customer','order_date','amount']].copy()
res['running_total'] = o.groupby('customer')['amount'].cumsum()
res = res.sort_values(['customer','order_date'], ascending=[False, True])
```
**Edge cases:** Same-day orders need a tie-breaker (order_id here). A customer with one order shows just that amount. NULL customer forms its own group.
**Likely follow-ups:** 1) How to run it per department and month? PARTITION BY dept, month. 2) How to get the final total per customer? Take the last row per group or use plain SUM with GROUP BY.
**Common mistakes:** Forgetting PARTITION BY (one big running total); partitioning but not ordering (every row shows the group total).

### Q9 ⭐⭐⭐ 🟡 How do you calculate a 3-day or 7-day moving average using ROWS BETWEEN?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you define a sliding frame with ROWS BETWEEN n PRECEDING AND CURRENT ROW?
**Say this in the interview:** For a 3-day moving average I use AVG(amount) OVER (ORDER BY sale_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW): today plus the two days before. For 7 days I change 2 to 6.
**Explain simply:**
- A **moving average** smooths noise by averaging the last few rows as the window slides forward.
- The window is "n-1 PRECEDING to CURRENT ROW" because it includes today.
- In the first rows there are fewer than 3 rows, so the average uses what exists (partial). Q14 shows how to hide those.
**Example:** Sales of 100, 120, 80: 3-day average on day 3 is (100+120+80)/3 = 100.
**Sample data:**

`daily_sales` (see Q3)
**SQL:**
```sql
-- Runs on PostgreSQL, MySQL 8+, SQL Server, SQLite 3.25+ (window functions need these versions)
SELECT sale_date, amount,
       ROUND(AVG(amount) OVER (
           ORDER BY sale_date
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS ma_3day
FROM daily_sales
ORDER BY sale_date;
```
**Output:**

| sale_date | amount | ma_3day |
|---|---|---|
| 2024-01-01 | 100 | 100.0 |
| 2024-01-02 | 120 | 110.0 |
| 2024-01-03 | 80 | 100.0 |
| 2024-01-04 | 150 | 116.67 |
| 2024-01-05 | 200 | 143.33 |
| 2024-01-06 | 90 | 146.67 |
| 2024-01-07 | 110 | 133.33 |
| 2024-01-08 | 130 | 110.0 |

**pandas equivalent:**
```python
res = ds.sort_values('sale_date').copy()
res['ma_3day'] = res['amount'].rolling(3, min_periods=1).mean().round(2)
```
**Edge cases:** ROWS counts physical rows, so if dates are missing the window spans more than 3 calendar days (use RANGE with an interval, Q40). NULLs are ignored by AVG, shrinking the divisor.
**Likely follow-ups:** 1) 7-day? ROWS BETWEEN 6 PRECEDING AND CURRENT ROW. 2) Centered average? 1 PRECEDING AND 1 FOLLOWING.
**Common mistakes:** Writing 3 PRECEDING (gives 4 rows); no ORDER BY inside OVER; trusting partial early rows.

### Q10 ⭐⭐⭐ 🟡 What is the difference between ROWS and RANGE in a window frame?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know ROWS counts physical rows while RANGE groups rows with equal sort values (peers)?
**Say this in the interview:** ROWS looks at the exact number of rows before and after the current row. RANGE looks at the value in ORDER BY, so rows with the same date are treated together as peers and get the same result.
**Explain simply:**
- **ROWS**: position based. Row 3 is row 3, even if row 2 has the same date.
- **RANGE**: value based. All rows tied on the ORDER BY value are in the frame together.
- The difference shows up only when ORDER BY values repeat (or when you use value offsets like 7 days).
- RANGE with numeric or date offsets is not supported on every database (MySQL and PostgreSQL differ; check your dialect).
**Example:** Two sales on 2 Jan (50 and 70): ROWS gives 150 then 220; RANGE gives 220 on both rows.
**Sample data:**

`ties_sales`

| sale_id | sale_date | amount |
|---|---|---|
| 1 | 2024-01-01 | 100 |
| 2 | 2024-01-02 | 50 |
| 3 | 2024-01-02 | 70 |
| 4 | 2024-01-03 | 30 |

**SQL:**
```sql
-- Runs on PostgreSQL, MySQL 8+, SQL Server, SQLite 3.25+ (window functions need these versions)
SELECT sale_id, sale_date, amount,
       SUM(amount) OVER (ORDER BY sale_date
            ROWS  BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS rows_total,
       SUM(amount) OVER (ORDER BY sale_date
            RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS range_total
FROM ties_sales
ORDER BY sale_id;
```
**Output:**

| sale_id | sale_date | amount | rows_total | range_total |
|---|---|---|---|---|
| 1 | 2024-01-01 | 100 | 100 | 100 |
| 2 | 2024-01-02 | 50 | 150 | 220 |
| 3 | 2024-01-02 | 70 | 220 | 220 |
| 4 | 2024-01-03 | 30 | 250 | 250 |

**pandas equivalent:**
```python
t = ties.sort_values('sale_id')
res = t[['sale_id','sale_date','amount']].copy()
res['rows_total'] = t['amount'].cumsum()
# RANGE: every row takes the running total of the LAST row sharing its date
res['range_total'] = res['rows_total'].groupby(t['sale_date']).transform('max')
```
**Edge cases:** With unique ORDER BY values, ROWS and RANGE give the same answer. With ROWS and ties, the order among tied rows is arbitrary unless you add a tie-breaker, so results can change between runs.
**Likely follow-ups:** 1) Which is the default? RANGE (Q11). 2) Which is faster? ROWS is usually cheaper. 3) What is GROUPS? Counts peer groups (Q44).
**Common mistakes:** Believing they are always identical; leaving ties unordered with ROWS and getting unstable output.

### Q11 ⭐⭐⭐ 🟡 What is the default window frame when ORDER BY is present, and why can a running total show wrong numbers when two rows share the same date?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the hidden default frame and the tie trap it causes?
**Say this in the interview:** With ORDER BY and no frame, the default is RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW. Because RANGE groups tied dates together, both rows on the same date show the same running total, which looks wrong. I fix it with ROWS or an extra unique tie-breaker.
**Explain simply:**
- Default with ORDER BY present: **RANGE UNBOUNDED PRECEDING to CURRENT ROW**. Without ORDER BY: the entire partition.
- Rows with equal ORDER BY values are "peers"; RANGE includes all peers up to the end of the tie.
- Result: two rows on 2 Jan both show 220 instead of 150 then 220.
- Best practice: always write the frame, and add a unique column to ORDER BY.
**Example:** A manager posts two attendance corrections on the same day; the running total jumps for both rows at once.
**Sample data:**

`ties_sales` (see Q10)
**SQL:**
```sql
-- Runs on PostgreSQL, MySQL 8+, SQL Server, SQLite 3.25+ (window functions need these versions)
SELECT sale_id, sale_date, amount,
       SUM(amount) OVER (ORDER BY sale_date)                    AS default_total,
       SUM(amount) OVER (ORDER BY sale_date, sale_id)           AS tiebreak_total,
       SUM(amount) OVER (ORDER BY sale_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)   AS rows_total
FROM ties_sales
ORDER BY sale_id;
```
**Output:**

| sale_id | sale_date | amount | default_total | tiebreak_total | rows_total |
|---|---|---|---|---|---|
| 1 | 2024-01-01 | 100 | 100 | 100 | 100 |
| 2 | 2024-01-02 | 50 | 220 | 150 | 150 |
| 3 | 2024-01-02 | 70 | 220 | 220 | 220 |
| 4 | 2024-01-03 | 30 | 250 | 250 | 250 |

**pandas equivalent:**
```python
t = ties.sort_values('sale_id')
res = t[['sale_id','sale_date','amount']].copy()
res['rows_total'] = t['amount'].cumsum()
res['default_total'] = res['rows_total'].groupby(t['sale_date']).transform('max')
res['tiebreak_total'] = res['rows_total']
res = res[['sale_id','sale_date','amount','default_total','tiebreak_total','rows_total']]
```
**Edge cases:** Note rows_total with ties but no tie-breaker depends on arbitrary row order inside the tie; add sale_id to be deterministic. The default is the SQL standard; most engines follow it. In SQL Server with ORDER BY, the default is also RANGE (with a restriction on RANGE offsets) from memory, not run here.
**Likely follow-ups:** 1) So which should I use? ROWS plus a tie-breaker. 2) Does the last row matter? The last row's total is always the full total either way.
**Common mistakes:** Not noticing duplicates in the order column; assuming the default frame is ROWS.

### Q12 ⭐⭐⭐ 🟡 Where do window functions sit in the SQL order of execution (relative to WHERE, GROUP BY, HAVING, SELECT, ORDER BY)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know windows run after WHERE/GROUP BY/HAVING, so you cannot filter on them directly?
**Say this in the interview:** Windows are evaluated late: FROM, WHERE, GROUP BY, HAVING first, then window functions, then SELECT's final columns, DISTINCT, ORDER BY and LIMIT. So a window function is not allowed in WHERE; I compute it in a subquery or CTE and filter outside.
**Explain simply:**
- Logical order: FROM/JOIN, WHERE, GROUP BY, HAVING, **WINDOW**, SELECT output, DISTINCT, ORDER BY, LIMIT.
- Consequence 1: window functions only see rows that survived WHERE. Filtering first changes the window values.
- Consequence 2: you can use them in SELECT and ORDER BY, not in WHERE, GROUP BY or HAVING.
- Fix: wrap in a CTE/subquery, or use QUALIFY where available (Snowflake, BigQuery, Teradata; not in MySQL/PostgreSQL/SQL Server).
**Example:** Employees paid above the company average: compute the average in the inner query, then filter in the outer query.
**Sample data:**

`employees` (see Q1; average salary is 65000)
**SQL:**
```sql
SELECT name, salary, ROUND(avg_sal, 2) AS avg_sal
FROM (
    SELECT name, salary, AVG(salary) OVER () AS avg_sal
    FROM employees
) AS t
WHERE salary > avg_sal
ORDER BY name;
```

The wrong way (window function inside WHERE) fails. Real error from SQLite when run:
```sql
SELECT name, salary, AVG(salary) OVER () AS avg_sal
FROM employees
WHERE salary > AVG(salary) OVER ();
-- error: misuse of window function AVG()
```
The right way (wrap in a subquery or CTE, then filter):
**Output:**

| name | salary | avg_sal |
|---|---|---|
| Esha | 70000 | 65000.0 |
| Farid | 80000 | 65000.0 |
| Gita | 90000 | 65000.0 |

**pandas equivalent:**
```python
avg_sal = emp['salary'].mean()
res = emp.loc[emp['salary'] > avg_sal, ['name','salary']].copy()
res['avg_sal'] = round(avg_sal, 2)
res = res.sort_values('name')
```
**Edge cases:** A WHERE filter placed inside the inner query changes the average, because the window only sees remaining rows. Compare WHERE inside versus outside carefully.
**Likely follow-ups:** 1) What is QUALIFY? A filter on window results, in some engines. 2) Can I use a window in HAVING? No.
**Common mistakes:** Putting a window function in WHERE; not realising a WHERE in the same query shrinks the window.

### Q13 ⭐⭐⭐ 🟡 How do you show each row's share of the total (percentage of total) using SUM() OVER()?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you build percent-of-total without a self-join or subquery?
**Say this in the interview:** I divide each row by SUM(salary) OVER () and multiply by 100. The empty OVER gives the total on every row so the division is straightforward. Use 100.0 so integer division does not round to zero.
**Explain simply:**
- Percent of total = row value / grand total x 100.
- For share within a department, use SUM(salary) OVER (PARTITION BY dept).
- In some databases (SQL Server, PostgreSQL), integer / integer truncates to an integer, so multiply by 100.0 first.
**Example:** Gita earns 90,000 out of 520,000 payroll, so her share is 17.3 percent.
**Sample data:**

`employees` (see Q1)
**SQL:**
```sql
-- Runs on PostgreSQL, MySQL 8+, SQL Server, SQLite 3.25+ (window functions need these versions)
SELECT name, salary,
       ROUND(100.0 * salary / SUM(salary) OVER (), 1) AS pct_of_payroll
FROM employees
ORDER BY emp_id;
```
**Output:**

| name | salary | pct_of_payroll |
|---|---|---|
| Asha | 50000 | 9.6 |
| Bala | 60000 | 11.5 |
| Chitra | 60000 | 11.5 |
| Dev | 45000 | 8.7 |
| Esha | 70000 | 13.5 |
| Farid | 80000 | 15.4 |
| Gita | 90000 | 17.3 |
| Hari | 65000 | 12.5 |

**pandas equivalent:**
```python
res = emp[['name','salary']].copy()
res['pct_of_payroll'] = (100.0 * emp['salary'] / emp['salary'].sum()).round(1)
```
**Edge cases:** Total of 0 or NULL leads to divide-by-zero or NULL; guard with NULLIF(SUM(...) OVER (), 0). Percentages may sum to 99.9 or 100.1 because of rounding.
**Likely follow-ups:** 1) Share within department? Add PARTITION BY dept. 2) Running share? See Q27.
**Common mistakes:** Integer division giving 0; using GROUP BY and losing the row detail.

### Q14 ⭐⭐⭐ 🔴 How do you write a 7-day moving average that shows NULL until a full 7 days of data exist?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you control partial windows with COUNT(*) OVER the same frame?
**Say this in the interview:** I compute the average over 6 PRECEDING AND CURRENT ROW and wrap it in a CASE that checks COUNT(*) over the same frame equals 7. Until 7 rows exist, it returns NULL.
**Explain simply:**
- A rolling average on the first 6 rows uses fewer than 7 values, which can mislead.
- COUNT(*) OVER (same frame) tells how many rows the window really contains.
- CASE WHEN that count is 7 THEN AVG ELSE NULL END hides incomplete windows.
- Alternative: filter the first 6 rows with ROW_NUMBER() in an outer query.
**Example:** Day 1 to 6 show NULL; day 7 shows the first full-week average.
**Sample data:**

`daily_sales` (see Q3, 8 days)
**SQL:**
```sql
-- Runs on PostgreSQL, MySQL 8+, SQL Server, SQLite 3.25+ (window functions need these versions)
SELECT sale_date, amount,
       CASE WHEN COUNT(*) OVER w = 7
            THEN ROUND(AVG(amount) OVER w, 2) END AS ma_7day
FROM daily_sales
WINDOW w AS (ORDER BY sale_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
ORDER BY sale_date;
-- Named WINDOW clause: PostgreSQL, MySQL 8, SQLite. SQL Server does not support it (not run here / from memory); repeat the OVER(...) text instead.
```
**Output:**

| sale_date | amount | ma_7day |
|---|---|---|
| 2024-01-01 | 100 | NULL |
| 2024-01-02 | 120 | NULL |
| 2024-01-03 | 80 | NULL |
| 2024-01-04 | 150 | NULL |
| 2024-01-05 | 200 | NULL |
| 2024-01-06 | 90 | NULL |
| 2024-01-07 | 110 | 121.43 |
| 2024-01-08 | 130 | 125.71 |

**pandas equivalent:**
```python
res = ds.sort_values('sale_date').copy()
res['ma_7day'] = res['amount'].rolling(7).mean().round(2)   # min_periods defaults to 7 -> NaN until full
res = res[['sale_date','amount','ma_7day']]
```
**Edge cases:** COUNT(*) counts NULL-amount rows too; COUNT(amount) counts only non-NULL values, so choose based on whether a NULL day should count. Missing calendar dates make the 7 rows cover more than a week.
**Likely follow-ups:** 1) Why not just WHERE row_number > 6? That works in an outer query but removes the first rows from the output. 2) What does pandas do? rolling(7) gives NaN until 7 rows.
**Common mistakes:** Leaving the partial windows in the report; counting the wrong column; not repeating the same frame in COUNT.

### Q15 ⭐⭐ 🟢 What is a window frame? Explain UNBOUNDED PRECEDING, CURRENT ROW and UNBOUNDED FOLLOWING in plain words.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand frames as the set of rows around the current row?
**Say this in the interview:** A window frame is the slice of rows, within the partition and in the ORDER BY sequence, that the function actually uses for the current row. UNBOUNDED PRECEDING means the very first row, CURRENT ROW means this row, and UNBOUNDED FOLLOWING means the very last row.
**Explain simply:**
- Syntax: `ROWS BETWEEN <start> AND <end>`.
- **UNBOUNDED PRECEDING**: start of the partition. **CURRENT ROW**: the row being computed. **UNBOUNDED FOLLOWING**: end of the partition.
- You can also use numbers: `2 PRECEDING`, `1 FOLLOWING`.
- start-to-current = running total; current-to-end = "still to go"; start-to-end = full partition.
**Example:** Think of a payroll list read top to bottom: so far, from here to the end, and everything.
**Sample data:**

`daily_sales` (see Q3)
**SQL:**
```sql
-- Runs on PostgreSQL, MySQL 8+, SQL Server, SQLite 3.25+ (window functions need these versions)
SELECT sale_date, amount,
       SUM(amount) OVER (ORDER BY sale_date
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)   AS so_far,
       SUM(amount) OVER (ORDER BY sale_date
           ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING)   AS from_here_on,
       SUM(amount) OVER (ORDER BY sale_date
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS whole
FROM daily_sales
ORDER BY sale_date;
```
**Output:**

| sale_date | amount | so_far | from_here_on | whole |
|---|---|---|---|---|
| 2024-01-01 | 100 | 100 | 980 | 980 |
| 2024-01-02 | 120 | 220 | 880 | 980 |
| 2024-01-03 | 80 | 300 | 760 | 980 |
| 2024-01-04 | 150 | 450 | 680 | 980 |
| 2024-01-05 | 200 | 650 | 530 | 980 |
| 2024-01-06 | 90 | 740 | 330 | 980 |
| 2024-01-07 | 110 | 850 | 240 | 980 |
| 2024-01-08 | 130 | 980 | 130 | 980 |

**pandas equivalent:**
```python
res = ds.sort_values('sale_date').copy()
res['so_far'] = res['amount'].cumsum()
res['from_here_on'] = res['amount'][::-1].cumsum()[::-1]
res['whole'] = res['amount'].sum()
```
**Edge cases:** The frame must start before it ends (an invalid order errors). Frames never cross partition boundaries.
**Likely follow-ups:** 1) Default frame? RANGE UNBOUNDED PRECEDING to CURRENT ROW with ORDER BY (Q11). 2) Do ranking functions use frames? No.
**Common mistakes:** Mixing up PRECEDING and FOLLOWING; leaving the frame out and getting the default.

### Q16 ⭐⭐ 🟢 What do FIRST_VALUE() and LAST_VALUE() do?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know FIRST_VALUE/LAST_VALUE return one specific row's value and that LAST_VALUE needs a frame?
**Say this in the interview:** FIRST_VALUE returns the value from the first row of the window and LAST_VALUE returns it from the last row. With ORDER BY and no frame, LAST_VALUE stops at the current row, so I extend the frame to UNBOUNDED FOLLOWING.
**Explain simply:**
- **FIRST_VALUE(col)**: value at the start of the frame. **LAST_VALUE(col)**: value at the end.
- Example: lowest-paid person's name in each department.
- The default frame ends at the current row, so LAST_VALUE just returns the current row's value (see Q21).
**Example:** In IT (Hari 65000, Farid 80000, Gita 90000) the lowest-paid name is Hari and the highest is Gita.
**Sample data:**

`employees` (see Q1)
**SQL:**
```sql
-- Runs on PostgreSQL, MySQL 8+, SQL Server, SQLite 3.25+ (window functions need these versions)
SELECT dept, name, salary,
       FIRST_VALUE(name) OVER w AS lowest_paid,
       LAST_VALUE(name)  OVER (PARTITION BY dept ORDER BY salary, emp_id
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS highest_paid
FROM employees
WINDOW w AS (PARTITION BY dept ORDER BY salary, emp_id)
ORDER BY dept, salary, emp_id;
```
**Output:**

| dept | name | salary | lowest_paid | highest_paid |
|---|---|---|---|---|
| HR | Asha | 50000 | Asha | Chitra |
| HR | Bala | 60000 | Asha | Chitra |
| HR | Chitra | 60000 | Asha | Chitra |
| IT | Hari | 65000 | Hari | Gita |
| IT | Farid | 80000 | Hari | Gita |
| IT | Gita | 90000 | Hari | Gita |
| Sales | Dev | 45000 | Dev | Esha |
| Sales | Esha | 70000 | Dev | Esha |

**pandas equivalent:**
```python
e = emp.sort_values(['dept','salary','emp_id'])
res = e[['dept','name','salary']].copy()
res['lowest_paid'] = e.groupby('dept')['name'].transform('first')
res['highest_paid'] = e.groupby('dept')['name'].transform('last')
res = res.sort_values(['dept','salary'], kind='stable')
```
**Edge cases:** Ties in the ORDER BY make the pick arbitrary unless a tie-breaker (emp_id) is added. NULL values: some engines support IGNORE NULLS (not in SQLite or MySQL). PostgreSQL has no IGNORE NULLS either (from memory).
**Likely follow-ups:** 1) Why does LAST_VALUE misbehave? Q21. 2) Alternative for the max? MAX(salary) OVER (PARTITION BY dept).
**Common mistakes:** Forgetting the frame for LAST_VALUE; forgetting the tie-breaker.

### Q17 ⭐⭐ 🟢 What does NTILE(n) do? Give an example.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know NTILE splits ordered rows into n nearly equal buckets and how leftovers are spread?
**Say this in the interview:** NTILE(n) sorts rows and cuts them into n buckets of roughly equal size, numbered 1 to n. If the rows do not divide evenly, the first buckets get one extra row each.
**Explain simply:**
- NTILE(4) gives quartiles, NTILE(10) deciles, NTILE(100) percentiles.
- It splits by row count, not by value, so equal salaries can land in different buckets.
- 8 employees in 3 buckets: sizes 3, 3, 2.
**Example:** Rank 8 employees by salary into 3 pay bands: band 1 = top 3 earners.
**Sample data:**

`employees` (see Q1)
**SQL:**
```sql
-- Runs on PostgreSQL, MySQL 8+, SQL Server, SQLite 3.25+ (window functions need these versions)
SELECT name, salary,
       NTILE(3) OVER (ORDER BY salary DESC, emp_id) AS pay_band
FROM employees
ORDER BY salary DESC, emp_id;
```
**Output:**

| name | salary | pay_band |
|---|---|---|
| Gita | 90000 | 1 |
| Farid | 80000 | 1 |
| Esha | 70000 | 1 |
| Hari | 65000 | 2 |
| Bala | 60000 | 2 |
| Chitra | 60000 | 2 |
| Asha | 50000 | 3 |
| Dev | 45000 | 3 |

**pandas equivalent:**
```python
e = emp.sort_values(['salary','emp_id'], ascending=[False, True]).reset_index(drop=True)
res = e[['name','salary']].copy()
n, k = len(e), 3
sizes = [n // k + (1 if i < n % k else 0) for i in range(k)]
res['pay_band'] = [b + 1 for b, s in enumerate(sizes) for _ in range(s)]
```
**Edge cases:** Fewer rows than buckets: some buckets stay empty. Tied values can be split across buckets, so add a tie-breaker. NTILE(0) or negative is an error.
**Likely follow-ups:** 1) Quartiles by spend? NTILE(4) (Q25). 2) How is it different from PERCENT_RANK? Q39.
**Common mistakes:** Assuming equal-width value ranges; expecting ties to stay together.

### Q18 ⭐⭐ 🟢 How do you add a count of employees per department to every employee row using COUNT(*) OVER()?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you attach a group count to detail rows without GROUP BY?
**Say this in the interview:** COUNT(*) OVER (PARTITION BY dept) counts the rows in each employee's department and repeats that number on every row of the department.
**Explain simply:**
- Same idea as SUM OVER PARTITION BY (Q2) but counting rows.
- The number is the same for everyone in the group; use it for headcount ratios or filters in an outer query.
- COUNT(*) counts rows; COUNT(col) skips NULLs.
**Example:** IT has 3 employees, so each IT row shows 3.
**Sample data:**

`employees` (see Q1)
**SQL:**
```sql
-- Runs on PostgreSQL, MySQL 8+, SQL Server, SQLite 3.25+ (window functions need these versions)
SELECT name, dept, salary,
       COUNT(*) OVER (PARTITION BY dept) AS dept_headcount
FROM employees
ORDER BY emp_id;
```
**Output:**

| name | dept | salary | dept_headcount |
|---|---|---|---|
| Asha | HR | 50000 | 3 |
| Bala | HR | 60000 | 3 |
| Chitra | HR | 60000 | 3 |
| Dev | Sales | 45000 | 2 |
| Esha | Sales | 70000 | 2 |
| Farid | IT | 80000 | 3 |
| Gita | IT | 90000 | 3 |
| Hari | IT | 65000 | 3 |

**pandas equivalent:**
```python
res = emp[['name','dept','salary']].copy()
res['dept_headcount'] = emp.groupby('dept')['name'].transform('size')
```
**Edge cases:** NULL dept forms its own group. COUNT(salary) would skip NULL salaries, COUNT(*) would not.
**Likely follow-ups:** 1) Filter departments with more than 2 people? Wrap in a CTE and filter. 2) Why not GROUP BY? You would lose employee detail.
**Common mistakes:** Using COUNT(*) with a plain column and no OVER (GROUP BY error); using COUNT(DISTINCT ...) in a window (not allowed everywhere, Q52).

### Q19 ⭐⭐ 🟢 How do you use LAG() or LEAD() with an offset of 2 or more rows back or forward?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the second argument of LAG/LEAD is the offset, and that the third is a default?
**Say this in the interview:** LAG(col, 2) looks two rows back, LEAD(col, 2) looks two rows forward. The first rows with no row that far back give NULL unless I pass a third argument as the default.
**Explain simply:**
- **LAG(column, n, default)**: value from the row **n positions earlier** in the window order (a **window** is the set of rows the function can see, ordered by the ORDER BY inside OVER).
- **LEAD(column, n, default)**: the same, but **n rows later**. n defaults to 1.
- It counts rows, not days. If a day is missing, 'two rows back' is not 'two days back'.
- If no row exists that far away you get NULL, or the default (third argument) if given.
**Example:** Compare today's sales with sales two days ago to skip a weekend effect. Day 3 (90) has two_days_ago = 120 (day 1).
**Sample data:**

| day | amount |
|---|---|
| 2024-06-01 | 120 |
| 2024-06-02 | 150 |
| 2024-06-03 | 90 |
| 2024-06-04 | 200 |
| 2024-06-05 | 170 |
| 2024-06-06 | 130 |

**SQL:**
```sql
SELECT day, amount,
       LAG(amount, 2)    OVER (ORDER BY day) AS two_days_ago,
       LEAD(amount, 2, 0) OVER (ORDER BY day) AS two_days_ahead
FROM dsales
ORDER BY day;
```
**Output:**

| day | amount | two_days_ago | two_days_ahead |
|---|---|---|---|
| 2024-06-01 | 120 | NULL | 90 |
| 2024-06-02 | 150 | NULL | 200 |
| 2024-06-03 | 90 | 120 | 170 |
| 2024-06-04 | 200 | 150 | 130 |
| 2024-06-05 | 170 | 90 | 0 |
| 2024-06-06 | 130 | 200 | 0 |

**pandas equivalent:**
```python
d = dsales.sort_values('day').copy()
d['two_days_ago'] = d['amount'].shift(2)
d['two_days_ahead'] = d['amount'].shift(-2).fillna(0)
res = d
```
pandas output (same as the SQL result):
```text
       day  amount  two_days_ago  two_days_ahead
2024-06-01     120           NaN            90.0
2024-06-02     150           NaN           200.0
2024-06-03      90         120.0           170.0
2024-06-04     200         150.0           130.0
2024-06-05     170          90.0             0.0
2024-06-06     130         200.0             0.0
```
**Edge cases:** First 2 rows of LAG(…,2) and last 2 rows of LEAD(…,2) are NULL (or the default). Missing dates silently shift the offset. Offset must be a non-negative integer; negative or NULL offsets error in most engines (from memory).
**Likely follow-ups:**
- *Can I look 7 days back for the same weekday?* Yes, LAG(x, 7), but only when there is exactly one row per day.
- *LAG with a negative offset?* Not allowed; use LEAD instead.
**Common mistakes:** Thinking the offset means days, forgetting the default, and forgetting PARTITION BY when each customer needs its own look-back.

### Q20 ⭐⭐ 🟢 Name the main categories of window functions (ranking, value, aggregate) and one example of each.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you have a mental map of the window-function families?
**Say this in the interview:** There are three families: ranking functions like RANK, value functions like LAG, and aggregate functions like SUM used with OVER.
**Explain simply:**
- **Ranking** (position of a row): ROW_NUMBER, RANK, DENSE_RANK, NTILE, PERCENT_RANK, CUME_DIST.
- **Value** (pull a value from another row): LAG, LEAD, FIRST_VALUE, LAST_VALUE, NTH_VALUE.
- **Aggregate** (normal totals, but kept per row): SUM, AVG, COUNT, MIN, MAX followed by OVER(...).
- All of them need `OVER (...)`; that is what makes a function a window function.
**Example:** In an HR table: RANK = who is the top earner in each department; LAG = the next higher salary; SUM OVER = department payroll beside each person.
**Sample data:**

| name | dept | salary |
|---|---|---|
| Anita | HR | 50000 |
| Ravi | HR | 62000 |
| Sneha | HR | 58000 |
| Arjun | Sales | 45000 |
| Meera | Sales | 70000 |
| Karan | Sales | 52000 |
| Divya | IT | 90000 |
| Imran | IT | 75000 |

**SQL:**
```sql
SELECT name, dept, salary,
       RANK()     OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk,            -- ranking
       LAG(salary) OVER (PARTITION BY dept ORDER BY salary DESC) AS salary_above,  -- value
       SUM(salary) OVER (PARTITION BY dept)                      AS dept_total     -- aggregate
FROM emp
ORDER BY dept, rnk;
```
**Output:**

| name | dept | salary | rnk | salary_above | dept_total |
|---|---|---|---|---|---|
| Ravi | HR | 62000 | 1 | NULL | 170000 |
| Sneha | HR | 58000 | 2 | 62000 | 170000 |
| Anita | HR | 50000 | 3 | 58000 | 170000 |
| Divya | IT | 90000 | 1 | NULL | 165000 |
| Imran | IT | 75000 | 2 | 90000 | 165000 |
| Meera | Sales | 70000 | 1 | NULL | 167000 |
| Karan | Sales | 52000 | 2 | 70000 | 167000 |
| Arjun | Sales | 45000 | 3 | 52000 | 167000 |

**Edge cases:** Some engines (SQL Server 2019 and older) do not support every function, e.g. NTH_VALUE or the WINDOW clause (from memory). Ties: RANK repeats the number and skips; ROW_NUMBER never repeats.
**Likely follow-ups:**
- *Are NTILE/PERCENT_RANK ranking?* Yes, they sit in the ranking family.
- *Can a normal aggregate be a window function?* Yes, add OVER.
**Common mistakes:** Calling GROUP BY aggregates 'window functions', or forgetting that aggregates become window functions only with OVER.

### Q21 ⭐⭐ 🟡 Why does LAST_VALUE() often return the current row's value, and how do you fix it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand default window frames, the classic LAST_VALUE trap?
**Say this in the interview:** When I add ORDER BY, the default frame stops at the current row, so the last row it can see is the current one. I fix it by extending the frame to UNBOUNDED FOLLOWING.
**Explain simply:**
- A **frame** is the slice of the partition the function is allowed to look at for the current row.
- With ORDER BY and no frame, the default is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`: start of group up to here.
- LAST_VALUE takes the last row of that frame, which is the current row (plus ties).
- Fix: `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`, or flip the sort and use FIRST_VALUE.
**Example:** Highest salary in each department: LAST_VALUE with the default frame just echoes each person's own salary; with the full frame it returns 62000 for every HR person.
**Sample data:**

| name | dept | salary |
|---|---|---|
| Anita | HR | 50000 |
| Ravi | HR | 62000 |
| Sneha | HR | 58000 |
| Arjun | Sales | 45000 |
| Meera | Sales | 70000 |
| Karan | Sales | 52000 |
| Divya | IT | 90000 |
| Imran | IT | 75000 |

**SQL:**
```sql
SELECT name, dept, salary,
       LAST_VALUE(salary) OVER (PARTITION BY dept ORDER BY salary) AS last_default,
       LAST_VALUE(salary) OVER (PARTITION BY dept ORDER BY salary
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS dept_max
FROM emp
ORDER BY dept, salary;
```
**Output:**

| name | dept | salary | last_default | dept_max |
|---|---|---|---|---|
| Anita | HR | 50000 | 50000 | 62000 |
| Sneha | HR | 58000 | 58000 | 62000 |
| Ravi | HR | 62000 | 62000 | 62000 |
| Imran | IT | 75000 | 75000 | 90000 |
| Divya | IT | 90000 | 90000 | 90000 |
| Arjun | Sales | 45000 | 45000 | 70000 |
| Karan | Sales | 52000 | 52000 | 70000 |
| Meera | Sales | 70000 | 70000 | 70000 |

**pandas equivalent:**
```python
d = emp.sort_values(['dept','salary']).copy()
d['last_default'] = d['salary']   # default frame ends at the current row (no ties in this data)
d['dept_max'] = d.groupby('dept')['salary'].transform('max')
res = d
```
pandas output (same as the SQL result):
```text
 name  dept  salary  last_default  dept_max
Anita    HR   50000         50000     62000
Sneha    HR   58000         58000     62000
 Ravi    HR   62000         62000     62000
Imran    IT   75000         75000     90000
Divya    IT   90000         90000     90000
Arjun Sales   45000         45000     70000
Karan Sales   52000         52000     70000
Meera Sales   70000         70000     70000
```
**Edge cases:** With ties on the ORDER BY column the default RANGE frame includes all tied rows, so tied rows see the same last value. NULLs: LAST_VALUE returns NULL if the last row is NULL unless the engine supports IGNORE NULLS (PostgreSQL and SQLite do not; Oracle/SQL Server 2022 do, from memory).
**Likely follow-ups:**
- *Simpler way to get the max?* MAX(salary) OVER (PARTITION BY dept).
- *Why does FIRST_VALUE not have this problem?* The default frame starts at the partition start, so the first row is always visible.
**Common mistakes:** Assuming LAST_VALUE means last row of the partition, and not specifying the frame.

### Q22 ⭐⭐ 🟡 How do you compute the number of days between each customer's consecutive orders?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you combine LAG with a date subtraction inside each customer?
**Say this in the interview:** I use LAG on the order date partitioned by customer, then subtract it from the current date. The first order per customer has no previous order so it is NULL.
**Explain simply:**
- **PARTITION BY customer** restarts the look-back for every customer.
- **LAG(order_date)** fetches the previous order's date; subtract to get days.
- Date subtraction differs by dialect: SQLite `julianday(a) - julianday(b)` (run here); PostgreSQL `a - b` on dates; MySQL `DATEDIFF(a, b)`; SQL Server `DATEDIFF(day, b, a)` (the last three not run here).
- Add a tie-breaker (order_id) so two orders on the same day sort in a fixed order.
**Example:** Asha ordered 5 Jan, 20 Jan and 2 Mar: gaps are 15 and 42 days. HR parallel: days between an employee's consecutive leaves.
**Sample data:**

| order_id | customer | order_date | amount |
|---|---|---|---|
| 1 | Asha | 2024-01-05 | 200 |
| 2 | Asha | 2024-01-20 | 150 |
| 3 | Asha | 2024-03-02 | 300 |
| 4 | Bala | 2024-01-10 | 500 |
| 5 | Bala | 2024-02-14 | 100 |
| 6 | Bala | 2024-03-30 | 350 |
| 7 | Chitra | 2024-02-01 | 250 |
| 8 | Chitra | 2024-02-01 | 50 |
| 9 | Chitra | 2024-04-10 | 400 |

**SQL:**
```sql
SELECT customer, order_id, order_date,
       LAG(order_date) OVER (PARTITION BY customer ORDER BY order_date, order_id) AS prev_order_date,
       CAST(julianday(order_date) - julianday(
            LAG(order_date) OVER (PARTITION BY customer ORDER BY order_date, order_id)) AS INTEGER) AS days_since_prev
FROM orders
WHERE customer IN ('Asha','Bala','Chitra')
ORDER BY customer, order_date, order_id;
```
**Output:**

| customer | order_id | order_date | prev_order_date | days_since_prev |
|---|---|---|---|---|
| Asha | 1 | 2024-01-05 | NULL | NULL |
| Asha | 2 | 2024-01-20 | 2024-01-05 | 15 |
| Asha | 3 | 2024-03-02 | 2024-01-20 | 42 |
| Bala | 4 | 2024-01-10 | NULL | NULL |
| Bala | 5 | 2024-02-14 | 2024-01-10 | 35 |
| Bala | 6 | 2024-03-30 | 2024-02-14 | 45 |
| Chitra | 7 | 2024-02-01 | NULL | NULL |
| Chitra | 8 | 2024-02-01 | 2024-02-01 | 0 |
| Chitra | 9 | 2024-04-10 | 2024-02-01 | 69 |

**pandas equivalent:**
```python
d = orders[orders.customer.isin(['Asha','Bala','Chitra'])].sort_values(['customer','order_date','order_id']).copy()
d['prev_order_date'] = d.groupby('customer')['order_date'].shift(1)
d['days_since_prev'] = (pd.to_datetime(d['order_date']) - pd.to_datetime(d['prev_order_date'])).dt.days
res = d
```
pandas output (same as the SQL result):
```text
customer  order_id order_date prev_order_date  days_since_prev
    Asha         1 2024-01-05             NaN              NaN
    Asha         2 2024-01-20      2024-01-05             15.0
    Asha         3 2024-03-02      2024-01-20             42.0
    Bala         4 2024-01-10             NaN              NaN
    Bala         5 2024-02-14      2024-01-10             35.0
    Bala         6 2024-03-30      2024-02-14             45.0
  Chitra         7 2024-02-01             NaN              NaN
  Chitra         8 2024-02-01      2024-02-01              0.0
  Chitra         9 2024-04-10      2024-02-01             69.0
```
**Edge cases:** First order per customer = NULL gap. Two orders on the same date give a gap of 0. In SQL Server and MySQL, put the LAG in a CTE if you want to reuse it. Datetime columns: cast to date first or the gap includes fractions.
**Likely follow-ups:**
- *Average gap per customer?* Wrap this in a CTE and AVG(days_since_prev) GROUP BY customer.
- *Customers with a single order?* They only have the NULL row, which AVG ignores.
**Common mistakes:** Forgetting PARTITION BY (so the gap crosses customers), not breaking date ties, and mixing dialect date functions.

### Q23 ⭐⭐ 🟡 How do you flag each row as increased, decreased or unchanged compared with the previous row?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you use LAG with CASE, and handle the first row where there is no previous value?
**Say this in the interview:** I bring the previous value alongside with LAG, then a CASE compares the two. I handle the NULL first row explicitly so it is not mislabelled.
**Explain simply:**
- LAG gives the previous row's value in the order you choose.
- A **CASE** is SQL's if/else: it returns the first matching label.
- Window functions cannot be used inside WHERE, so I put LAG in a CTE (a named temporary result) or use it directly in the CASE.
- Without the IS NULL branch the first row would fall to 'unchanged', which is wrong.
**Example:** Monthly headcount 100, 104, 104, 99: the labels are first row, increased, unchanged, decreased. Same pattern flags rising or falling attrition.
**Sample data:**

| month | headcount |
|---|---|
| 2024-01 | 100 |
| 2024-02 | 104 |
| 2024-03 | 104 |
| 2024-04 | 99 |
| 2024-05 | 101 |
| 2024-06 | 101 |

**SQL:**
```sql
WITH x AS (
  SELECT month, headcount, LAG(headcount) OVER (ORDER BY month) AS prev_hc FROM hc)
SELECT month, headcount, prev_hc,
       CASE WHEN prev_hc IS NULL          THEN 'first row'
            WHEN headcount > prev_hc      THEN 'increased'
            WHEN headcount < prev_hc      THEN 'decreased'
            ELSE 'unchanged' END AS trend
FROM x ORDER BY month;
```
**Output:**

| month | headcount | prev_hc | trend |
|---|---|---|---|
| 2024-01 | 100 | NULL | first row |
| 2024-02 | 104 | 100 | increased |
| 2024-03 | 104 | 104 | unchanged |
| 2024-04 | 99 | 104 | decreased |
| 2024-05 | 101 | 99 | increased |
| 2024-06 | 101 | 101 | unchanged |

**pandas equivalent:**
```python
d = hc.sort_values('month').copy()
d['prev_hc'] = d['headcount'].shift(1)
d['trend'] = np.select([d.prev_hc.isna(), d.headcount > d.prev_hc, d.headcount < d.prev_hc],
                       ['first row', 'increased', 'decreased'], default='unchanged')
res = d
```
pandas output (same as the SQL result):
```text
  month  headcount  prev_hc     trend
2024-01        100      NaN first row
2024-02        104    100.0 increased
2024-03        104    104.0 unchanged
2024-04         99    104.0 decreased
2024-05        101     99.0 increased
2024-06        101    101.0 unchanged
```
**Edge cases:** NULL prev (first row, or a NULL value in the data): comparisons with NULL are never true, so they would fall to ELSE; handle explicitly. Missing months break 'previous' meaning.
**Likely follow-ups:**
- *Could I use SIGN()?* Yes, SIGN(headcount - prev_hc) gives 1/0/-1 (SIGN exists in MySQL/PostgreSQL/SQL Server, SQLite 3.35+ with math functions only).
- *Count the increases?* SUM(CASE WHEN trend='increased' THEN 1 END).
**Common mistakes:** Letting the first row become 'unchanged', and comparing with NULL using = instead of IS NULL.

### Q24 ⭐⭐ 🟡 How do you show each employee's salary minus the average salary of their department?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know a window average lets you compare a row with its group without a join?
**Say this in the interview:** AVG(salary) OVER (PARTITION BY dept) puts the department average on every row, then I subtract it from the person's salary.
**Explain simply:**
- **PARTITION BY dept** splits rows into department groups but, unlike GROUP BY, keeps every row.
- The average is the same for everyone in the department; subtract to get the gap (positive = paid above average).
- The older way is a GROUP BY subquery joined back; the window version is shorter.
**Example:** HR dept average is (50000 + 62000 + 58000)/3 = 56666.67, so Ravi at 62000 is +5333.33 above his department. Useful for pay-equity checks.
**Sample data:**

| name | dept | salary |
|---|---|---|
| Anita | HR | 50000 |
| Ravi | HR | 62000 |
| Sneha | HR | 58000 |
| Arjun | Sales | 45000 |
| Meera | Sales | 70000 |
| Karan | Sales | 52000 |
| Divya | IT | 90000 |
| Imran | IT | 75000 |

**SQL:**
```sql
SELECT name, dept, salary,
       ROUND(AVG(salary) OVER (PARTITION BY dept), 2)          AS dept_avg,
       ROUND(salary - AVG(salary) OVER (PARTITION BY dept), 2) AS diff_from_avg
FROM emp
ORDER BY dept, salary DESC;
```
**Output:**

| name | dept | salary | dept_avg | diff_from_avg |
|---|---|---|---|---|
| Ravi | HR | 62000 | 56666.67 | 5333.33 |
| Sneha | HR | 58000 | 56666.67 | 1333.33 |
| Anita | HR | 50000 | 56666.67 | -6666.67 |
| Divya | IT | 90000 | 82500 | 7500 |
| Imran | IT | 75000 | 82500 | -7500 |
| Meera | Sales | 70000 | 55666.67 | 14333.33 |
| Karan | Sales | 52000 | 55666.67 | -3666.67 |
| Arjun | Sales | 45000 | 55666.67 | -10666.67 |

**pandas equivalent:**
```python
d = emp.sort_values(['dept','salary'], ascending=[True, False]).copy()
d['dept_avg'] = d.groupby('dept')['salary'].transform('mean').round(2)
d['diff_from_avg'] = (d['salary'] - d.groupby('dept')['salary'].transform('mean')).round(2)
res = d
```
pandas output (same as the SQL result):
```text
 name  dept  salary  dept_avg  diff_from_avg
 Ravi    HR   62000  56666.67        5333.33
Sneha    HR   58000  56666.67        1333.33
Anita    HR   50000  56666.67       -6666.67
Divya    IT   90000  82500.00        7500.00
Imran    IT   75000  82500.00       -7500.00
Meera Sales   70000  55666.67       14333.33
Karan Sales   52000  55666.67       -3666.67
Arjun Sales   45000  55666.67      -10666.67
```
**Edge cases:** NULL salaries are ignored by AVG, but the NULL person's own diff is NULL. A one-person department gives diff 0. Integer division: in SQL Server/PostgreSQL AVG of integers returns decimal, fine; some engines truncate, so cast if unsure.
**Likely follow-ups:**
- *Percent above average?* salary * 100.0 / AVG(salary) OVER (PARTITION BY dept).
- *Only people above average?* Put it in a CTE and filter WHERE diff_from_avg > 0.
**Common mistakes:** Using GROUP BY and losing the employee rows, or filtering on the window result in WHERE directly.

### Q25 ⭐⭐ 🟡 How do you split customers into quartiles (4 equal groups) by total spend using NTILE?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you bucket customers into equal groups and know which is the top bucket?
**Say this in the interview:** I total spend per customer with GROUP BY in a CTE, then NTILE(4) over spend sorted high to low, so quartile 1 is the top 25 percent of spenders.
**Explain simply:**
- **NTILE(4)** deals the sorted rows into 4 buckets of (almost) equal row count, numbered 1 to 4.
- The sort direction decides what bucket 1 means: DESC puts the biggest spenders in 1.
- It splits by row count, not by value ranges, so equal spend can land in different buckets: add a tie-breaker like customer.
- If rows do not divide evenly, the first buckets get one extra row.
**Example:** 8 customers means 2 per quartile. Bala (950) and Chitra (700) are the top quartile. HR parallel: pay quartiles for compensation benchmarking.
**Sample data:**

| order_id | customer | order_date | amount |
|---|---|---|---|
| 1 | Asha | 2024-01-05 | 200 |
| 2 | Asha | 2024-01-20 | 150 |
| 3 | Asha | 2024-03-02 | 300 |
| 4 | Bala | 2024-01-10 | 500 |
| 5 | Bala | 2024-02-14 | 100 |
| 6 | Bala | 2024-03-30 | 350 |
| 7 | Chitra | 2024-02-01 | 250 |
| 8 | Chitra | 2024-02-01 | 50 |
| 9 | Chitra | 2024-04-10 | 400 |
| 10 | Dev | 2024-01-15 | 80 |
| 11 | Esha | 2024-02-20 | 120 |
| 12 | Farah | 2024-03-05 | 90 |
| 13 | Gita | 2024-03-18 | 600 |
| 14 | Hari | 2024-04-02 | 210 |

**SQL:**
```sql
WITH spend AS (
  SELECT customer, SUM(amount) AS total_spend FROM orders GROUP BY customer)
SELECT customer, total_spend,
       NTILE(4) OVER (ORDER BY total_spend DESC, customer) AS quartile
FROM spend
ORDER BY quartile, total_spend DESC, customer;
```
**Output:**

| customer | total_spend | quartile |
|---|---|---|
| Bala | 950 | 1 |
| Chitra | 700 | 1 |
| Asha | 650 | 2 |
| Gita | 600 | 2 |
| Hari | 210 | 3 |
| Esha | 120 | 3 |
| Farah | 90 | 4 |
| Dev | 80 | 4 |

**pandas equivalent:**
```python
s = orders.groupby('customer', as_index=False)['amount'].sum().rename(columns={'amount':'total_spend'})
s = s.sort_values(['total_spend','customer'], ascending=[False, True]).reset_index(drop=True)
n = len(s)
s['quartile'] = (np.arange(n) * 4) // n + 1     # exact NTILE only because 8 divides evenly by 4
res = s
```
pandas output (same as the SQL result):
```text
customer  total_spend  quartile
    Bala          950         1
  Chitra          700         1
    Asha          650         2
    Gita          600         2
    Hari          210         3
    Esha          120         3
   Farah           90         4
     Dev           80         4
```
**Edge cases:** Fewer rows than buckets leaves some buckets empty. 10 rows into 4 buckets gives sizes 3,3,2,2. Ties split arbitrarily without a tie-breaker. NULL spend sorts first or last depending on the engine.
**Likely follow-ups:**
- *Quartile labels like Top/Bottom?* Wrap in CASE on the NTILE number.
- *NTILE vs percentile cut-offs?* NTILE counts rows; percentile functions use values.
**Common mistakes:** Forgetting that NTILE(4) with ASC makes bucket 1 the lowest, and running NTILE before aggregating (so it ranks orders, not customers).

### Q26 ⭐⭐ 🟡 How do you calculate a running count of orders per customer?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you see a running count as a running total of 1s, restarted per customer?
**Say this in the interview:** COUNT(*) with OVER, partitioned by customer and ordered by date, counts each customer's orders so far. I add a ROWS frame so tied dates still count one by one.
**Explain simply:**
- **Running count** = how many rows up to and including this one.
- PARTITION BY customer restarts the count for each customer; ORDER BY date sets the sequence.
- Without a frame, the default RANGE frame counts tied dates together (Chitra's two orders on 1 Feb would both show 2). `ROWS` counts strictly row by row.
- If you only need numbering, ROW_NUMBER() does the same thing (covered in Part 5).
**Example:** Order number 3 for a customer tells you she is a repeat buyer. HR parallel: nth interview round for each candidate.
**Sample data:**

| order_id | customer | order_date | amount |
|---|---|---|---|
| 1 | Asha | 2024-01-05 | 200 |
| 2 | Asha | 2024-01-20 | 150 |
| 3 | Asha | 2024-03-02 | 300 |
| 4 | Bala | 2024-01-10 | 500 |
| 5 | Bala | 2024-02-14 | 100 |
| 6 | Bala | 2024-03-30 | 350 |
| 7 | Chitra | 2024-02-01 | 250 |
| 8 | Chitra | 2024-02-01 | 50 |
| 9 | Chitra | 2024-04-10 | 400 |

**SQL:**
```sql
SELECT customer, order_id, order_date, amount,
       COUNT(*) OVER (PARTITION BY customer ORDER BY order_date, order_id
                      ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS order_no
FROM orders
WHERE customer IN ('Asha','Bala','Chitra')
ORDER BY customer, order_date, order_id;
```
**Output:**

| customer | order_id | order_date | amount | order_no |
|---|---|---|---|---|
| Asha | 1 | 2024-01-05 | 200 | 1 |
| Asha | 2 | 2024-01-20 | 150 | 2 |
| Asha | 3 | 2024-03-02 | 300 | 3 |
| Bala | 4 | 2024-01-10 | 500 | 1 |
| Bala | 5 | 2024-02-14 | 100 | 2 |
| Bala | 6 | 2024-03-30 | 350 | 3 |
| Chitra | 7 | 2024-02-01 | 250 | 1 |
| Chitra | 8 | 2024-02-01 | 50 | 2 |
| Chitra | 9 | 2024-04-10 | 400 | 3 |

**pandas equivalent:**
```python
d = orders[orders.customer.isin(['Asha','Bala','Chitra'])].sort_values(['customer','order_date','order_id']).copy()
d['order_no'] = d.groupby('customer').cumcount() + 1
res = d
```
pandas output (same as the SQL result):
```text
customer  order_id order_date  amount  order_no
    Asha         1 2024-01-05     200         1
    Asha         2 2024-01-20     150         2
    Asha         3 2024-03-02     300         3
    Bala         4 2024-01-10     500         1
    Bala         5 2024-02-14     100         2
    Bala         6 2024-03-30     350         3
  Chitra         7 2024-02-01     250         1
  Chitra         8 2024-02-01      50         2
  Chitra         9 2024-04-10     400         3
```
**Edge cases:** Ties on date with the default frame inflate the count; use ROWS or a unique tie-breaker. COUNT(col) skips NULLs; COUNT(*) does not.
**Likely follow-ups:**
- *Only count orders above 100?* COUNT(CASE WHEN amount > 100 THEN 1 END) OVER (...).
- *Is ROW_NUMBER simpler?* Yes, when you only want the sequence.
**Common mistakes:** Forgetting PARTITION BY (counts across all customers) and relying on the default frame with duplicate dates.

### Q27 ⭐⭐ 🟡 How do you calculate a cumulative percentage of total (running share)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you combine a running total with a grand total in the same query?
**Say this in the interview:** I divide the running total by the grand total, SUM() OVER (), and multiply by 100. The last row always reaches 100 percent.
**Explain simply:**
- Running total = SUM(amount) with an ordered frame up to the current row.
- Grand total = SUM(amount) OVER () with empty parentheses (every row sees the whole table).
- Multiply by **100.0**, not 100, to avoid integer division (5/10 would become 0 in some engines).
- For a Pareto (80/20) view, sort by amount descending instead of by date.
**Example:** Sales total 860 over 6 days; by day 4 we have 560, which is 65.1 percent of the period. HR parallel: cumulative share of attrition by tenure band.
**Sample data:**

| day | amount |
|---|---|
| 2024-06-01 | 120 |
| 2024-06-02 | 150 |
| 2024-06-03 | 90 |
| 2024-06-04 | 200 |
| 2024-06-05 | 170 |
| 2024-06-06 | 130 |

**SQL:**
```sql
SELECT day, amount,
       SUM(amount) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,
       ROUND(100.0 * SUM(amount) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
             / SUM(amount) OVER (), 1) AS cum_pct
FROM dsales
ORDER BY day;
```
**Output:**

| day | amount | running_total | cum_pct |
|---|---|---|---|
| 2024-06-01 | 120 | 120 | 14 |
| 2024-06-02 | 150 | 270 | 31.4 |
| 2024-06-03 | 90 | 360 | 41.9 |
| 2024-06-04 | 200 | 560 | 65.1 |
| 2024-06-05 | 170 | 730 | 84.9 |
| 2024-06-06 | 130 | 860 | 100 |

**pandas equivalent:**
```python
d = dsales.sort_values('day').copy()
d['running_total'] = d['amount'].cumsum()
d['cum_pct'] = (100.0 * d['running_total'] / d['amount'].sum()).round(1)
res = d
```
pandas output (same as the SQL result):
```text
       day  amount  running_total  cum_pct
2024-06-01     120            120     14.0
2024-06-02     150            270     31.4
2024-06-03      90            360     41.9
2024-06-04     200            560     65.1
2024-06-05     170            730     84.9
2024-06-06     130            860    100.0
```
**Edge cases:** Total of zero would divide by zero: wrap the denominator in NULLIF(...,0). Negative amounts (refunds) can push the share above 100 mid-way. Ties on the ORDER BY need ROWS frame to avoid jumpy shares.
**Likely follow-ups:**
- *Pareto: which customers make 80 percent?* Order by spend DESC, compute cum_pct, filter cum_pct <= 80 in an outer query.
- *Per group?* Add PARTITION BY to both windows.
**Common mistakes:** Integer division, and putting ORDER BY in the grand-total window (which turns it into a running total).

### Q28 ⭐⭐ 🟡 How do you find each customer's first order date and show it on every row without GROUP BY?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know a group aggregate can be attached to each row with a window?
**Say this in the interview:** MIN(order_date) OVER (PARTITION BY customer) puts the customer's first order date on every one of their rows, no GROUP BY or join needed.
**Explain simply:**
- MIN/MAX/SUM etc. become **window aggregates** when followed by OVER; they do not collapse rows.
- No ORDER BY inside OVER here: we want the minimum of the whole customer group, not a running minimum.
- ISO dates (YYYY-MM-DD) compare correctly as text; real DATE columns are safer.
- Alternative: FIRST_VALUE(order_date) OVER (PARTITION BY customer ORDER BY order_date).
**Example:** Asha's first order was 5 Jan, so every Asha row shows 5 Jan. Then days since first order = order_date minus first_order_date (customer tenure). HR parallel: joining date beside each attendance row.
**Sample data:**

| order_id | customer | order_date | amount |
|---|---|---|---|
| 1 | Asha | 2024-01-05 | 200 |
| 2 | Asha | 2024-01-20 | 150 |
| 3 | Asha | 2024-03-02 | 300 |
| 4 | Bala | 2024-01-10 | 500 |
| 5 | Bala | 2024-02-14 | 100 |
| 6 | Bala | 2024-03-30 | 350 |
| 7 | Chitra | 2024-02-01 | 250 |
| 8 | Chitra | 2024-02-01 | 50 |
| 9 | Chitra | 2024-04-10 | 400 |

**SQL:**
```sql
SELECT customer, order_id, order_date, amount,
       MIN(order_date) OVER (PARTITION BY customer) AS first_order_date
FROM orders
WHERE customer IN ('Asha','Bala','Chitra')
ORDER BY customer, order_date, order_id;
```
**Output:**

| customer | order_id | order_date | amount | first_order_date |
|---|---|---|---|---|
| Asha | 1 | 2024-01-05 | 200 | 2024-01-05 |
| Asha | 2 | 2024-01-20 | 150 | 2024-01-05 |
| Asha | 3 | 2024-03-02 | 300 | 2024-01-05 |
| Bala | 4 | 2024-01-10 | 500 | 2024-01-10 |
| Bala | 5 | 2024-02-14 | 100 | 2024-01-10 |
| Bala | 6 | 2024-03-30 | 350 | 2024-01-10 |
| Chitra | 7 | 2024-02-01 | 250 | 2024-02-01 |
| Chitra | 8 | 2024-02-01 | 50 | 2024-02-01 |
| Chitra | 9 | 2024-04-10 | 400 | 2024-02-01 |

**pandas equivalent:**
```python
d = orders[orders.customer.isin(['Asha','Bala','Chitra'])].sort_values(['customer','order_date','order_id']).copy()
d['first_order_date'] = d.groupby('customer')['order_date'].transform('min')
res = d
```
pandas output (same as the SQL result):
```text
customer  order_id order_date  amount first_order_date
    Asha         1 2024-01-05     200       2024-01-05
    Asha         2 2024-01-20     150       2024-01-05
    Asha         3 2024-03-02     300       2024-01-05
    Bala         4 2024-01-10     500       2024-01-10
    Bala         5 2024-02-14     100       2024-01-10
    Bala         6 2024-03-30     350       2024-01-10
  Chitra         7 2024-02-01     250       2024-02-01
  Chitra         8 2024-02-01      50       2024-02-01
  Chitra         9 2024-04-10     400       2024-02-01
```
**Edge cases:** NULL dates are ignored by MIN. If a customer has no rows, they simply do not appear. Time zones or datetime stamps: cast to date for day-level work.
**Likely follow-ups:**
- *Why not GROUP BY?* It would return one row per customer, losing order details.
- *Flag the first order?* CASE WHEN order_date = first_order_date.
**Common mistakes:** Adding ORDER BY inside OVER (turns it into a running minimum, which happens to also work for MIN but is confusing).

### Q29 ⭐⭐ 🟡 How do you use LEAD() to find the next login date or next event for each user?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you look forward in time per user with LEAD?
**Say this in the interview:** LEAD(login_date) partitioned by user and ordered by date gives that user's next login on the current row. The last login has no next one, so it is NULL.
**Explain simply:**
- **LEAD** is the mirror of LAG: it reads the **next** row instead of the previous.
- PARTITION BY user_id keeps each user's logins separate.
- NULL next_login means 'no later login yet'; for churn analysis that is the signal you want.
- Gap in days is the next date minus the current date (dialect-specific functions as in Q22).
**Example:** User 1 logs in on 2 Jan, 5 Jan, 9 Jan: gaps 3 and 4 days, last row NULL. HR parallel: next absence date after each absence.
**Sample data:**

| user_id | login_date |
|---|---|
| 1 | 2024-01-02 |
| 1 | 2024-01-05 |
| 1 | 2024-01-09 |
| 2 | 2024-01-03 |
| 2 | 2024-01-04 |

**SQL:**
```sql
SELECT user_id, login_date,
       LEAD(login_date) OVER (PARTITION BY user_id ORDER BY login_date) AS next_login,
       CAST(julianday(LEAD(login_date) OVER (PARTITION BY user_id ORDER BY login_date))
            - julianday(login_date) AS INTEGER) AS days_to_next
FROM logins
ORDER BY user_id, login_date;
```
**Output:**

| user_id | login_date | next_login | days_to_next |
|---|---|---|---|
| 1 | 2024-01-02 | 2024-01-05 | 3 |
| 1 | 2024-01-05 | 2024-01-09 | 4 |
| 1 | 2024-01-09 | NULL | NULL |
| 2 | 2024-01-03 | 2024-01-04 | 1 |
| 2 | 2024-01-04 | NULL | NULL |

**pandas equivalent:**
```python
d = logins.sort_values(['user_id','login_date']).copy()
d['next_login'] = d.groupby('user_id')['login_date'].shift(-1)
d['days_to_next'] = (pd.to_datetime(d['next_login']) - pd.to_datetime(d['login_date'])).dt.days
res = d
```
pandas output (same as the SQL result):
```text
 user_id login_date next_login  days_to_next
       1 2024-01-02 2024-01-05           3.0
       1 2024-01-05 2024-01-09           4.0
       1 2024-01-09        NaN           NaN
       2 2024-01-03 2024-01-04           1.0
       2 2024-01-04        NaN           NaN
```
**Edge cases:** Duplicate login dates give a gap of 0: de-duplicate to dates first. Last row per user is always NULL. Users with a single login give a single NULL row.
**Likely follow-ups:**
- *Flag users who never returned?* Filter rows where next_login IS NULL (in an outer query).
- *Next event of a specific type?* Filter in a CTE first, then LEAD.
**Common mistakes:** Using LAG instead of LEAD, and forgetting that the last row is NULL.

### Q30 ⭐⭐ 🟡 How do you calculate a running maximum or running minimum?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know MAX/MIN also work as running calculations with a frame?
**Say this in the interview:** MAX(x) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) gives the highest value seen so far; swap in MIN for the lowest.
**Explain simply:**
- Same idea as a running total, but the function is MAX or MIN instead of SUM.
- **UNBOUNDED PRECEDING** = start of the partition; **CURRENT ROW** = this row. So the window grows as you go down.
- Useful to spot new records: price = running_high means a new all-time high that day.
- Add PARTITION BY to restart per group (per stock, per employee).
**Example:** A stock closes 102, 100, 105, 103, 99, 108; the running high goes 102, 102, 105, 105, 105, 108. HR parallel: best monthly performance score so far.
**Sample data:**

| day | price |
|---|---|
| 2024-06-01 | 102 |
| 2024-06-02 | 100 |
| 2024-06-03 | 105 |
| 2024-06-04 | 103 |
| 2024-06-05 | 99 |
| 2024-06-06 | 108 |

**SQL:**
```sql
SELECT day, price,
       MAX(price) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_high,
       MIN(price) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_low
FROM prices
ORDER BY day;
```
**Output:**

| day | price | running_high | running_low |
|---|---|---|---|
| 2024-06-01 | 102 | 102 | 102 |
| 2024-06-02 | 100 | 102 | 100 |
| 2024-06-03 | 105 | 105 | 100 |
| 2024-06-04 | 103 | 105 | 100 |
| 2024-06-05 | 99 | 105 | 99 |
| 2024-06-06 | 108 | 108 | 99 |

**pandas equivalent:**
```python
d = prices.sort_values('day').copy()
d['running_high'] = d['price'].cummax()
d['running_low'] = d['price'].cummin()
res = d
```
pandas output (same as the SQL result):
```text
       day  price  running_high  running_low
2024-06-01    102           102          102
2024-06-02    100           102          100
2024-06-03    105           105          100
2024-06-04    103           105          100
2024-06-05     99           105           99
2024-06-06    108           108           99
```
**Edge cases:** NULLs are skipped, so a NULL row inherits the previous high. The first row's running max is itself. Ties are harmless for MAX/MIN.
**Likely follow-ups:**
- *Drawdown from the peak?* price - running_high.
- *Running high within the last 30 days?* Use ROWS BETWEEN 29 PRECEDING AND CURRENT ROW.
**Common mistakes:** Leaving the ORDER BY out (giving the overall max on every row) or ordering by the wrong column.

### Q31 ⭐⭐ 🟡 How do you calculate a running average (average of all rows from the start to the current row)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you tell a running (cumulative) average apart from a moving average?
**Say this in the interview:** A running average uses every row from the start up to now: AVG with ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW. A moving average only uses the last few rows.
**Explain simply:**
- Window grows each row: row 3 averages rows 1-3, row 4 averages rows 1-4.
- It equals running total divided by running count.
- Moving average = fixed-size window, e.g. `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` (Q9).
- AVG ignores NULLs, so the denominator counts only non-NULL values.
**Example:** Daily sales 120, 150, 90: running average is 120, 135, 120. Handy to see where an average is settling. HR parallel: average time-to-hire of all hires so far.
**Sample data:**

| day | amount |
|---|---|
| 2024-06-01 | 120 |
| 2024-06-02 | 150 |
| 2024-06-03 | 90 |
| 2024-06-04 | 200 |
| 2024-06-05 | 170 |
| 2024-06-06 | 130 |

**SQL:**
```sql
SELECT day, amount,
       ROUND(AVG(amount) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS running_avg
FROM dsales
ORDER BY day;
```
**Output:**

| day | amount | running_avg |
|---|---|---|
| 2024-06-01 | 120 | 120 |
| 2024-06-02 | 150 | 135 |
| 2024-06-03 | 90 | 120 |
| 2024-06-04 | 200 | 140 |
| 2024-06-05 | 170 | 146 |
| 2024-06-06 | 130 | 143.33 |

**pandas equivalent:**
```python
d = dsales.sort_values('day').copy()
d['running_avg'] = d['amount'].expanding().mean().round(2)
res = d
```
pandas output (same as the SQL result):
```text
       day  amount  running_avg
2024-06-01     120       120.00
2024-06-02     150       135.00
2024-06-03      90       120.00
2024-06-04     200       140.00
2024-06-05     170       146.00
2024-06-06     130       143.33
```
**Edge cases:** NULL values are left out of both sum and count. With ORDER BY and no frame, the default RANGE frame would average tied dates together; ROWS avoids that. Round only for display.
**Likely follow-ups:**
- *Difference from AVG() OVER ()?* That one is the overall average on every row.
- *Weighted version?* Divide a running SUM(x*weight) by a running SUM(weight).
**Common mistakes:** Mixing up running and moving averages and not stating the frame.

### Q32 ⭐⭐ 🟡 How do you compare each month with the same month last year using LAG(12) or a self-join, and what breaks if a month is missing?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know LAG(12) counts rows, not months, and so breaks when a month is missing?
**Say this in the interview:** LAG(sales, 12) works only if every month has exactly one row. If a month is missing it picks the wrong month, so I self-join on the date minus one year, which is safe against gaps.
**Explain simply:**
- **LAG(sales, 12)** = the row 12 positions earlier (same month last year, if no gaps).
- **Self-join** = joining a table to itself (second copy aliased `p` for 'previous year') on `month = month - 1 year`.
- In the data below June 2023 is missing. LAG(12) for Feb 2024 returns Jan 2023's 100 (wrong) while the join correctly returns Feb 2023's 110.
- Filter to the year in an outer query: a WHERE in the same SELECT runs before the window and would delete the 2023 rows LAG needs.
- Date shift per dialect: SQLite `date(m,'-1 year')` (run); PostgreSQL `m - INTERVAL '1 year'`; MySQL `DATE_SUB(m, INTERVAL 1 YEAR)`; SQL Server `DATEADD(year,-1,m)` (not run).
**Example:** Sales this February vs last February. A missing month in the data silently shifts every later LAG(12) by one. HR parallel: headcount vs same month last year when a month's snapshot failed to load.
**Sample data:**

| month | sales |
|---|---|
| 2023-01-01 | 100 |
| 2023-02-01 | 110 |
| 2023-03-01 | 120 |
| 2023-04-01 | 115 |
| 2023-05-01 | 130 |
| 2023-07-01 | 140 |
| 2023-08-01 | 150 |
| 2023-09-01 | 145 |
| 2023-10-01 | 160 |
| 2023-11-01 | 170 |
| 2023-12-01 | 200 |
| 2024-01-01 | 120 |
| 2024-02-01 | 121 |
| 2024-03-01 | 150 |

**SQL:**
```sql
WITH s AS (SELECT month, sales FROM msales),
j AS (
  SELECT s.month, s.sales,
         LAG(s.sales, 12) OVER (ORDER BY s.month) AS lag12_value,
         p.sales                                  AS same_month_last_year,
         s.sales - p.sales                        AS yoy_change
  FROM s
  LEFT JOIN s AS p ON p.month = date(s.month, '-1 year'))
SELECT * FROM j
WHERE month >= '2023-12-01'
ORDER BY month;
```
**Output:**

| month | sales | lag12_value | same_month_last_year | yoy_change |
|---|---|---|---|---|
| 2023-12-01 | 200 | NULL | NULL | NULL |
| 2024-01-01 | 120 | NULL | 100 | 20 |
| 2024-02-01 | 121 | 100 | 110 | 11 |
| 2024-03-01 | 150 | 110 | 120 | 30 |

**pandas equivalent:**
```python
m = msales.sort_values('month').reset_index(drop=True)
lookup = dict(zip(m.month, m.sales))
m['lag12_value'] = m['sales'].shift(12)
m['same_month_last_year'] = [lookup.get(str(pd.Timestamp(x) - pd.DateOffset(years=1))[:10]) for x in m.month]
m['yoy_change'] = m['sales'] - m['same_month_last_year']
res = m[m.month >= '2023-12-01']
```
pandas output (same as the SQL result):
```text
     month  sales  lag12_value  same_month_last_year  yoy_change
2023-12-01    200          NaN                   NaN         NaN
2024-01-01    120          NaN                 100.0        20.0
2024-02-01    121        100.0                 110.0        11.0
2024-03-01    150        110.0                 120.0        30.0
```
**Edge cases:** Missing months: fix by joining to a calendar table (a table with every month) with LEFT JOIN, so gaps become NULL rows. First 12 months have NULL last year. Zero last-year values need NULLIF (Q33).
**Likely follow-ups:**
- *Fill the gap rows instead?* Generate a month calendar and LEFT JOIN sales; COALESCE to 0 if appropriate.
- *Why not LAG(1) for MoM?* LAG(1) has the same gap problem.
**Common mistakes:** Assuming one row per month always, and filtering to the year in the same SELECT's WHERE (it runs before the window, so LAG finds nothing).

### Q33 ⭐⭐ 🟡 How do you calculate percent change safely when the previous value is zero or NULL (NULLIF)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you avoid divide-by-zero errors and understand how NULL propagates?
**Say this in the interview:** I divide by NULLIF(prev, 0): that turns a zero denominator into NULL so the result is NULL instead of an error. A NULL previous or current value also gives NULL.
**Explain simply:**
- **NULLIF(a, b)** returns NULL if a equals b, otherwise a. So NULLIF(prev, 0) is NULL when prev is 0.
- Anything divided by NULL is NULL, so the percent change shows as NULL, not a crash.
- NULL arithmetic: if prev_rev or revenue is NULL, the whole expression is NULL.
- Some engines (SQL Server, PostgreSQL) raise 'division by zero'; SQLite and MySQL return NULL by default, but NULLIF keeps the code portable.
- Optionally COALESCE(..., 0) if you prefer 0 or a text label like 'n/a'.
**Example:** Revenue goes 0, 120, 90: month 2 has no meaningful percent change (growth from zero), month 3 is -25.0 percent. HR parallel: attrition rate change when last month's leavers were zero.
**Sample data:**

| month | revenue |
|---|---|
| m1 | 0 |
| m2 | 120 |
| m3 | 90 |
| m4 | NULL |
| m5 | 60 |
| m6 | 75 |

**SQL:**
```sql
WITH x AS (SELECT month, revenue, LAG(revenue) OVER (ORDER BY month) AS prev_rev FROM gr)
SELECT month, revenue, prev_rev,
       ROUND(100.0 * (revenue - prev_rev) / NULLIF(prev_rev, 0), 1) AS pct_change
FROM x ORDER BY month;
```
**Output:**

| month | revenue | prev_rev | pct_change |
|---|---|---|---|
| m1 | 0 | NULL | NULL |
| m2 | 120 | 0 | NULL |
| m3 | 90 | 120 | -25 |
| m4 | NULL | 90 | NULL |
| m5 | 60 | NULL | NULL |
| m6 | 75 | 60 | 25 |

**pandas equivalent:**
```python
d = gr.sort_values('month').copy()
d['prev_rev'] = d['revenue'].shift(1)
d['pct_change'] = (100.0 * (d['revenue'] - d['prev_rev']) / d['prev_rev'].replace(0, np.nan)).round(1)
res = d
```
pandas output (same as the SQL result):
```text
month  revenue  prev_rev  pct_change
   m1      0.0       NaN         NaN
   m2    120.0       0.0         NaN
   m3     90.0     120.0       -25.0
   m4      NaN      90.0         NaN
   m5     60.0       NaN         NaN
   m6     75.0      60.0        25.0
```
**Edge cases:** Previous value 0 -> NULL. Current value NULL -> NULL, and the month after it also NULL because its previous is NULL. Negative previous values give odd signs: divide by ABS(prev) if needed. Integer division: use 100.0.
**Likely follow-ups:**
- *Show 'new' instead of NULL?* CASE WHEN prev_rev = 0 THEN 'new' ...
- *Why not WHERE prev <> 0?* It drops the rows instead of showing them.
**Common mistakes:** Dividing by the current value instead of the previous one, and integer division (100 instead of 100.0).

### Q34 ⭐⭐ 🟡 How do you use PARTITION BY with more than one column?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know PARTITION BY accepts a comma-separated list, like GROUP BY?
**Say this in the interview:** I list the columns separated by commas, PARTITION BY dept, city. A new group is every unique combination of those columns.
**Explain simply:**
- Each distinct (dept, city) pair is its own partition.
- Rows stay visible, unlike GROUP BY: every employee shows their own group's count and average.
- The same list works in other windows or together with ORDER BY for running totals per combination.
- Different window functions in one SELECT can use different PARTITION BY lists.
**Example:** Pune HR has 2 people averaging 56000; Mumbai HR has 1 at 58000. HR parallel: average salary per department per location.
**Sample data:**

| emp_id | name | dept | city | salary |
|---|---|---|---|---|
| 1 | Anita | HR | Pune | 50000 |
| 2 | Ravi | HR | Pune | 62000 |
| 3 | Sneha | HR | Mumbai | 58000 |
| 4 | Arjun | Sales | Mumbai | 45000 |
| 5 | Meera | Sales | Mumbai | 70000 |
| 6 | Karan | Sales | Pune | 52000 |
| 7 | Divya | IT | Pune | 90000 |
| 8 | Imran | IT | Pune | 75000 |

**SQL:**
```sql
SELECT name, dept, city, salary,
       COUNT(*)              OVER (PARTITION BY dept, city) AS heads_in_group,
       ROUND(AVG(salary) OVER (PARTITION BY dept, city), 0) AS group_avg_salary
FROM emp
ORDER BY dept, city, salary;
```
**Output:**

| name | dept | city | salary | heads_in_group | group_avg_salary |
|---|---|---|---|---|---|
| Sneha | HR | Mumbai | 58000 | 1 | 58000 |
| Anita | HR | Pune | 50000 | 2 | 56000 |
| Ravi | HR | Pune | 62000 | 2 | 56000 |
| Imran | IT | Pune | 75000 | 2 | 82500 |
| Divya | IT | Pune | 90000 | 2 | 82500 |
| Arjun | Sales | Mumbai | 45000 | 2 | 57500 |
| Meera | Sales | Mumbai | 70000 | 2 | 57500 |
| Karan | Sales | Pune | 52000 | 1 | 52000 |

**pandas equivalent:**
```python
d = emp.sort_values(['dept','city','salary']).copy()
g = d.groupby(['dept','city'])['salary']
d['heads_in_group'] = g.transform('count')
d['group_avg_salary'] = g.transform('mean').round(0)
res = d
```
pandas output (same as the SQL result):
```text
 name  dept   city  salary  heads_in_group  group_avg_salary
Sneha    HR Mumbai   58000               1           58000.0
Anita    HR   Pune   50000               2           56000.0
 Ravi    HR   Pune   62000               2           56000.0
Imran    IT   Pune   75000               2           82500.0
Divya    IT   Pune   90000               2           82500.0
Arjun Sales Mumbai   45000               2           57500.0
Meera Sales Mumbai   70000               2           57500.0
Karan Sales   Pune   52000               1           52000.0
```
**Edge cases:** NULL in a partition column forms its own group (NULLs are grouped together). Single-row groups give average = own value. Order of columns in the list does not change the groups.
**Likely follow-ups:**
- *Can two windows have different partitions?* Yes, in one query.
- *Can I use an expression?* Yes, e.g. PARTITION BY dept, strftime('%Y', hire_date).
**Common mistakes:** Thinking only one column is allowed, or partitioning by too many columns so every group has one row.

### Q35 ⭐⭐ 🟡 What is the named WINDOW clause, and when does it make queries shorter?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the WINDOW clause avoids repeating the same OVER definition?
**Say this in the interview:** The WINDOW clause lets me define a window once, give it a name, and reuse it in several functions with OVER w. It shortens queries and keeps them consistent.
**Explain simply:**
- `WINDOW w AS (...)` goes after HAVING and before ORDER BY.
- `OVER w` reuses it. You can also extend a named window, e.g. `OVER (w ORDER BY x)` (rules vary by engine).
- Supported in PostgreSQL, MySQL 8+, SQLite 3.28+ (run here). SQL Server does not support it (from memory), where you repeat the definition.
- Best when 3 or more functions share the same partition and order.
**Example:** A salary report needing rank, running payroll and next-higher salary per department would repeat the same 40-character window three times; with the WINDOW clause it is written once.
**Sample data:**

| name | dept | salary |
|---|---|---|
| Anita | HR | 50000 |
| Ravi | HR | 62000 |
| Sneha | HR | 58000 |
| Arjun | Sales | 45000 |
| Meera | Sales | 70000 |
| Karan | Sales | 52000 |
| Divya | IT | 90000 |
| Imran | IT | 75000 |

**SQL:**
```sql
SELECT name, dept, salary,
       RANK()     OVER w AS rnk,
       SUM(salary) OVER w AS running_payroll,
       LAG(salary) OVER w AS next_higher_salary
FROM emp
WINDOW w AS (PARTITION BY dept ORDER BY salary DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
ORDER BY dept, salary DESC;
```
**Output:**

| name | dept | salary | rnk | running_payroll | next_higher_salary |
|---|---|---|---|---|---|
| Ravi | HR | 62000 | 1 | 62000 | NULL |
| Sneha | HR | 58000 | 2 | 120000 | 62000 |
| Anita | HR | 50000 | 3 | 170000 | 58000 |
| Divya | IT | 90000 | 1 | 90000 | NULL |
| Imran | IT | 75000 | 2 | 165000 | 90000 |
| Meera | Sales | 70000 | 1 | 70000 | NULL |
| Karan | Sales | 52000 | 2 | 122000 | 70000 |
| Arjun | Sales | 45000 | 3 | 167000 | 52000 |

**Edge cases:** Referencing an undefined window name is an error. The frame in the named window applies to every function using it, but ranking functions like RANK ignore frames, so mixing them is fine. LAG also ignores frames.
**Likely follow-ups:**
- *Does it change the result?* No, it is just shorthand.
- *Why is the running payroll in descending order?* Because the shared window sorts by salary DESC.
**Common mistakes:** Placing WINDOW before WHERE/GROUP BY, or using it on SQL Server.

### Q36 ⭐⭐ 🟡 How do you compute a window function on top of GROUP BY results (for example, running total of monthly totals)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand windows run after GROUP BY, so they can use grouped results?
**Say this in the interview:** GROUP BY runs first and produces one row per month; the window function then runs over those grouped rows. I can write SUM(SUM(amount)) OVER (...) or use a CTE for clarity.
**Explain simply:**
- Order of execution: FROM, WHERE, GROUP BY, HAVING, then window functions, then SELECT output and ORDER BY.
- So a window can wrap an aggregate: the inner SUM(amount) is per group, the outer SUM ... OVER is the running total across groups.
- The CTE version (`WITH m AS (... GROUP BY month) SELECT ... SUM(monthly_total) OVER (...)`) gives the same result (checked) and is easier to read.
- Month formatting: SQLite `strftime('%Y-%m', d)`; PostgreSQL `to_char(d,'YYYY-MM')`; MySQL `DATE_FORMAT(d,'%Y-%m')`; SQL Server `FORMAT(d,'yyyy-MM')` (not run).
**Example:** Monthly totals 930, 520, 1340, 610 give running totals 930, 1450, 2790, 3400. HR parallel: cumulative hires by month.
**Sample data:**

| order_id | customer | order_date | amount |
|---|---|---|---|
| 1 | Asha | 2024-01-05 | 200 |
| 2 | Asha | 2024-01-20 | 150 |
| 3 | Asha | 2024-03-02 | 300 |
| 4 | Bala | 2024-01-10 | 500 |
| 5 | Bala | 2024-02-14 | 100 |
| 6 | Bala | 2024-03-30 | 350 |
| 7 | Chitra | 2024-02-01 | 250 |
| 8 | Chitra | 2024-02-01 | 50 |
| 9 | Chitra | 2024-04-10 | 400 |
| 10 | Dev | 2024-01-15 | 80 |
| 11 | Esha | 2024-02-20 | 120 |
| 12 | Farah | 2024-03-05 | 90 |
| 13 | Gita | 2024-03-18 | 600 |
| 14 | Hari | 2024-04-02 | 210 |

**SQL:**
```sql
SELECT strftime('%Y-%m', order_date) AS month,
       SUM(amount)                   AS monthly_total,
       SUM(SUM(amount)) OVER (ORDER BY strftime('%Y-%m', order_date)
                              ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM orders
GROUP BY strftime('%Y-%m', order_date)
ORDER BY month;
```
**Output:**

| month | monthly_total | running_total |
|---|---|---|
| 2024-01 | 930 | 930 |
| 2024-02 | 520 | 1450 |
| 2024-03 | 1340 | 2790 |
| 2024-04 | 610 | 3400 |

**pandas equivalent:**
```python
o = orders.copy()
o['month'] = o['order_date'].str[:7]
m = o.groupby('month', as_index=False)['amount'].sum().rename(columns={'amount':'monthly_total'})
m['running_total'] = m['monthly_total'].cumsum()
res = m
```
pandas output (same as the SQL result):
```text
  month  monthly_total  running_total
2024-01            930            930
2024-02            520           1450
2024-03           1340           2790
2024-04            610           3400
```
**Edge cases:** Every non-aggregated column in SELECT or window ORDER BY must be in GROUP BY or be aggregated. Months with no orders do not appear: use a calendar table if you need them. Ordering by text 'YYYY-MM' sorts correctly.
**Likely follow-ups:**
- *Can I use the alias 'month' in the window's ORDER BY?* Not in all engines: repeat the expression or use a CTE.
- *Why not window then group?* You would get the running total per order row, not per month.
**Common mistakes:** Trying to run the window first, or selecting a raw column that is not grouped.

### Q37 ⭐⭐ 🟡 Show each employee's salary and the salary of the next higher-paid employee in the same department using LEAD().
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you use LEAD with PARTITION BY and ORDER BY, and do you notice what happens at the last row and with tied salaries?
**Say this in the interview:** LEAD looks one row ahead inside each department after sorting by salary, so for every employee it returns the next higher salary; the top earner gets NULL because nobody is above them.
**Explain simply:**
- LEAD(column) means: peek at the next row in the sorted order, without joining the table to itself.
- PARTITION BY dept is like a separate mini-table per department, so one department's salary never leaks into another's.
- ORDER BY salary inside OVER() decides what 'next' means. Without it, 'next' is random.
- Tied salaries are the catch: LEAD returns the very next row, which may have the same salary. If you want the next strictly higher salary, use the MIN-over-RANGE version shown below.
**Example:** In HR, Asha earns 50,000 and the next person up the ladder earns 60,000. A manager can use the gap (10,000) to see how steep the pay ladder is.
**Sample data:** `emp`

| emp_id | name | dept | salary |
|---|---|---|---|
| 1 | Asha | HR | 50000 |
| 2 | Bala | HR | 60000 |
| 3 | Chitra | HR | 60000 |
| 4 | Dev | IT | 70000 |
| 5 | Esha | IT | 90000 |
| 6 | Farhan | IT | 80000 |
| 7 | Gita | Sales | 45000 |
**SQL:**
```sql
CREATE TABLE emp (emp_id INT, name TEXT, dept TEXT, salary INT);

SELECT name, dept, salary,
       LEAD(salary) OVER (PARTITION BY dept ORDER BY salary, emp_id) AS next_in_order,
       MIN(salary)  OVER (PARTITION BY dept ORDER BY salary
                          RANGE BETWEEN 1 FOLLOWING AND UNBOUNDED FOLLOWING) AS next_strictly_higher
FROM emp
ORDER BY dept, salary, emp_id;

-- Dialects: LEAD works the same in MySQL 8+, PostgreSQL, SQL Server 2012+, SQLite 3.25+.
-- RANGE ... 1 FOLLOWING with a number works in PostgreSQL 11+, SQLite, DuckDB; not in SQL Server (not run here / from memory).
```
**Output:** (run in sqlite)

| name | dept | salary | next_in_order | next_strictly_higher |
|---|---|---|---|---|
| Asha | HR | 50000 | 60000 | 60000 |
| Bala | HR | 60000 | 60000 | NULL |
| Chitra | HR | 60000 | NULL | NULL |
| Dev | IT | 70000 | 80000 | 80000 |
| Farhan | IT | 80000 | 90000 | 90000 |
| Esha | IT | 90000 | NULL | NULL |
| Gita | Sales | 45000 | NULL | NULL |
**pandas equivalent:**
```python
import pandas as pd
emp = pd.DataFrame([
    (1, 'Asha', 'HR', 50000),
    (2, 'Bala', 'HR', 60000),
    (3, 'Chitra', 'HR', 60000),
    (4, 'Dev', 'IT', 70000),
    (5, 'Esha', 'IT', 90000),
    (6, 'Farhan', 'IT', 80000),
    (7, 'Gita', 'Sales', 45000),
], columns=['emp_id', 'name', 'dept', 'salary'])
out = emp.sort_values(['dept', 'salary', 'emp_id']).reset_index(drop=True)
out['next_in_order'] = out.groupby('dept')['salary'].shift(-1)
out['next_strictly_higher'] = out.groupby('dept')['salary'].transform(
    lambda s: s.apply(lambda v: s[s > v].min()))
out = out[['name', 'dept', 'salary', 'next_in_order', 'next_strictly_higher']]
print(out.to_string(index=False))
```
Output (real run, matches the SQL result):
```text
  name  dept  salary  next_in_order  next_strictly_higher
  Asha    HR   50000        60000.0               60000.0
  Bala    HR   60000        60000.0                   NaN
Chitra    HR   60000            NaN                   NaN
   Dev    IT   70000        80000.0               80000.0
Farhan    IT   80000        90000.0               90000.0
  Esha    IT   90000            NaN                   NaN
  Gita Sales   45000            NaN                   NaN
```
**Edge cases:** The highest earner in each department gets NULL. A department with one person (Sales) gives NULL for everyone. Ties: Asha's and Bala's next_in_order are both 60,000 and Chitra's is NULL, while the strict version skips equal salaries (Bala and Chitra both get NULL). Always add a tiebreaker (emp_id) so the result is repeatable.
**Likely follow-ups:**
- How do I get the previous lower salary instead? Use LAG, or LEAD on ORDER BY salary DESC.
- How do I show the gap? salary difference: LEAD(salary) OVER (...) - salary, wrapped in COALESCE if you want 0 instead of NULL.
**Common mistakes:** Forgetting PARTITION BY (so departments mix), forgetting ORDER BY (random 'next'), and assuming LEAD skips ties. Also trying to filter on LEAD in WHERE; wrap in a subquery first.

### Q38 ⭐⭐ 🟡 What is the pandas equivalent of cumsum, shift and rolling for SQL running totals, LAG and moving averages?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know that every SQL window idea has a pandas twin, and can you move between the two when a task is done in Python?
**Say this in the interview:** Running total is cumsum, LAG is shift, and a moving average is rolling().mean(). For per-group work I add groupby first, which is the pandas version of PARTITION BY.
**Explain simply:**
- SQL SUM() OVER (ORDER BY day) -> pandas `cumsum()`: add up everything so far.
- SQL LAG(x) -> pandas `shift(1)`; LEAD(x) -> `shift(-1)`. Both push values up or down one row and leave a gap (NaN, pandas' word for NULL).
- SQL AVG() OVER (ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) -> `rolling(3, min_periods=1).mean()`. min_periods=1 makes the first rows average what exists, exactly like SQL.
- PARTITION BY dept -> `df.groupby('dept')['col'].cumsum()` (or shift, rolling).
- pandas does not sort for you: sort_values first, just like ORDER BY inside OVER().
**Example:** Daily sales of a canteen: today's running total, yesterday's sales and the 3-day average appear as three new columns in either tool.
**Sample data:** `sales`

| day | amount |
|---|---|
| 2026-03-01 | 100 |
| 2026-03-02 | 150 |
| 2026-03-03 | 120 |
| 2026-03-04 | 200 |
| 2026-03-05 | 180 |
| 2026-03-06 | 90 |
**SQL:**
```sql
CREATE TABLE sales (day TEXT, amount INT);

SELECT day, amount,
       SUM(amount) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,
       LAG(amount, 1) OVER (ORDER BY day) AS prev_amount,
       ROUND(AVG(amount) OVER (ORDER BY day ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS avg_3day
FROM sales
ORDER BY day;
```
**Output:** (run in sqlite)

| day | amount | running_total | prev_amount | avg_3day |
|---|---|---|---|---|
| 2026-03-01 | 100 | 100 | NULL | 100 |
| 2026-03-02 | 150 | 250 | 100 | 125 |
| 2026-03-03 | 120 | 370 | 150 | 123.33 |
| 2026-03-04 | 200 | 570 | 120 | 156.67 |
| 2026-03-05 | 180 | 750 | 200 | 166.67 |
| 2026-03-06 | 90 | 840 | 180 | 156.67 |
**pandas equivalent:**
```python
import pandas as pd
sales = pd.DataFrame([
    ('2026-03-01', 100),
    ('2026-03-02', 150),
    ('2026-03-03', 120),
    ('2026-03-04', 200),
    ('2026-03-05', 180),
    ('2026-03-06', 90),
], columns=['day', 'amount'])
out = sales.sort_values('day').reset_index(drop=True)
out['running_total'] = out['amount'].cumsum()
out['prev_amount'] = out['amount'].shift(1)
out['avg_3day'] = out['amount'].rolling(3, min_periods=1).mean().round(2)
print(out.to_string(index=False))
```
Output (real run, matches the SQL result):
```text
       day  amount  running_total  prev_amount  avg_3day
2026-03-01     100            100          NaN    100.00
2026-03-02     150            250        100.0    125.00
2026-03-03     120            370        150.0    123.33
2026-03-04     200            570        120.0    156.67
2026-03-05     180            750        200.0    166.67
2026-03-06      90            840        180.0    156.67
```
**Edge cases:** First row: LAG gives NULL/NaN, and the 3-day average uses only the rows available. NaN in pandas turns integer columns into floats (100 becomes 100.0). Missing calendar days are ignored by ROWS and by rolling(3); use a time-based window (rolling('3D')) if dates have gaps.
**Likely follow-ups:**
- pandas version of PARTITION BY? groupby(...).transform or groupby(...)[col].cumsum()/shift().
- pandas version of ROW_NUMBER? groupby(...).cumcount() + 1; for RANK use rank(method='min').
**Common mistakes:** Not sorting before cumsum/shift, forgetting groupby so groups bleed into each other, and expecting rolling(3) to match SQL on the first two rows without min_periods=1.

### Q39 ⭐ 🟢 What are PERCENT_RANK() and CUME_DIST(), and how do they differ from NTILE?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you separate rank-as-a-fraction (PERCENT_RANK, CUME_DIST) from equal-sized buckets (NTILE)?
**Say this in the interview:** PERCENT_RANK tells me what fraction of rows are strictly below this one, CUME_DIST tells me what fraction are at or below it, and NTILE just chops the sorted rows into n equal-sized buckets.
**Explain simply:**
- PERCENT_RANK = (rank - 1) / (rows - 1). It runs from 0 to 1; the lowest value is always 0 and the highest is 1.
- CUME_DIST = rows with value less than or equal to this one / total rows. It never returns 0, and the top row is always 1. Ties get the same (higher) value.
- NTILE(4) gives bucket numbers 1 to 4 and does not care about the actual values. Tied values can land in different buckets.
- So the first two describe position as a number between 0 and 1; NTILE labels groups.
**Example:** Seven employees sorted by salary: the 50,000 earner has 1 person below out of 6 others, so PERCENT_RANK = 1/6 = 0.1667.
**Sample data:** `emp`

| emp_id | name | dept | salary |
|---|---|---|---|
| 1 | Asha | HR | 50000 |
| 2 | Bala | HR | 60000 |
| 3 | Chitra | HR | 60000 |
| 4 | Dev | IT | 70000 |
| 5 | Esha | IT | 90000 |
| 6 | Farhan | IT | 80000 |
| 7 | Gita | Sales | 45000 |
**SQL:**
```sql
CREATE TABLE emp (emp_id INT, name TEXT, dept TEXT, salary INT);

SELECT name, salary,
       ROUND(PERCENT_RANK() OVER (ORDER BY salary), 4) AS pct_rank,
       ROUND(CUME_DIST()    OVER (ORDER BY salary), 4) AS cume_dist,
       NTILE(4)             OVER (ORDER BY salary, emp_id) AS quartile
FROM emp
ORDER BY salary, emp_id;

-- Dialects: all three exist in PostgreSQL, MySQL 8+, SQL Server 2012+, SQLite 3.25+.
```
**Output:** (run in sqlite)

| name | salary | pct_rank | cume_dist | quartile |
|---|---|---|---|---|
| Gita | 45000 | 0 | 0.1429 | 1 |
| Asha | 50000 | 0.1667 | 0.2857 | 1 |
| Bala | 60000 | 0.3333 | 0.5714 | 2 |
| Chitra | 60000 | 0.3333 | 0.5714 | 2 |
| Dev | 70000 | 0.6667 | 0.7143 | 3 |
| Farhan | 80000 | 0.8333 | 0.8571 | 3 |
| Esha | 90000 | 1 | 1 | 4 |
**pandas equivalent:**
```python
import pandas as pd
emp = pd.DataFrame([
    (1, 'Asha', 'HR', 50000),
    (2, 'Bala', 'HR', 60000),
    (3, 'Chitra', 'HR', 60000),
    (4, 'Dev', 'IT', 70000),
    (5, 'Esha', 'IT', 90000),
    (6, 'Farhan', 'IT', 80000),
    (7, 'Gita', 'Sales', 45000),
], columns=['emp_id', 'name', 'dept', 'salary'])
out = emp.sort_values(['salary', 'emp_id']).reset_index(drop=True)
n = len(out)
out['pct_rank'] = ((out['salary'].rank(method='min') - 1) / (n - 1)).round(4)
out['cume_dist'] = (out['salary'].rank(method='max') / n).round(4)
q, r = divmod(n, 4)
def ntile(i):
    cut = r * (q + 1)
    return i // (q + 1) + 1 if i < cut else (i - cut) // q + r + 1
out['quartile'] = [ntile(i) for i in range(n)]
out = out[['name', 'salary', 'pct_rank', 'cume_dist', 'quartile']]
print(out.to_string(index=False))
```
Output (real run, matches the SQL result):
```text
  name  salary  pct_rank  cume_dist  quartile
  Gita   45000    0.0000     0.1429         1
  Asha   50000    0.1667     0.2857         1
  Bala   60000    0.3333     0.5714         2
Chitra   60000    0.3333     0.5714         2
   Dev   70000    0.6667     0.7143         3
Farhan   80000    0.8333     0.8571         3
  Esha   90000    1.0000     1.0000         4
```
**Edge cases:** The two 60,000 salaries share pct_rank 0.3333 and cume_dist 0.5714, but NTILE works on row positions, not values, so tied values could be split across two buckets (here both happen to land in quartile 2). With 7 rows and 4 buckets, the first 3 buckets get 2 rows and the last gets 1. One row only: PERCENT_RANK is 0 (no divide-by-zero in standard engines).
**Likely follow-ups:**
- When do I use NTILE over PERCENT_RANK? When I need labelled groups (quartiles, deciles); PERCENT_RANK when I need an exact percentile position.
- Top 10 percent of earners? WHERE pct_rank >= 0.9 in a subquery, or cume_dist > 0.9.
**Common mistakes:** Thinking PERCENT_RANK equals rank/count (that is closer to CUME_DIST), using NTILE when ties must stay together, and filtering a window result in the same SELECT's WHERE.

### Q40 ⭐ 🟡 How do you compute a 7-day moving sum when some dates are missing, using RANGE with an INTERVAL?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know ROWS counts rows while RANGE counts values (like dates), so gaps in dates do not break your window?
**Say this in the interview:** With ROWS 6 PRECEDING I get the last 7 rows, but if some days are missing that reaches too far back in time. RANGE with an INTERVAL of 6 days looks at the actual dates, so it always means the last 7 calendar days.
**Explain simply:**
- ROWS = count physical rows. RANGE = look at the ORDER BY value and include rows whose value is inside a distance.
- RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW = today and the 6 days before it (7 days in total).
- Missing dates simply contribute nothing, which is usually what you want for a calendar window.
- Dialect support differs: PostgreSQL 11+, DuckDB and MySQL 8 allow it; SQL Server and SQLite do not allow INTERVAL here. SQLite workaround: convert the date to a day number and use a plain number distance (shown second).
**Example:** Daily leave applications are recorded only on days someone applied. A rolling 7-day total must still mean 7 calendar days, not the last 7 entries.
**Sample data:** `sales2`

| sale_date | amount |
|---|---|
| 2026-03-01 | 100 |
| 2026-03-02 | 50 |
| 2026-03-05 | 70 |
| 2026-03-08 | 30 |
| 2026-03-09 | 20 |
| 2026-03-15 | 40 |
| 2026-03-16 | 10 |
**SQL:**
```sql
CREATE TABLE sales2 (sale_date DATE, amount INT);

SELECT sale_date, amount,
       SUM(amount) OVER (ORDER BY sale_date
                         RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW) AS sum_7_calendar_days,
       SUM(amount) OVER (ORDER BY sale_date
                         ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS sum_last_7_rows
FROM sales2
ORDER BY sale_date;

-- SQLite version: RANGE with a plain number (day number)
WITH d AS (SELECT sale_date, amount, CAST(julianday(sale_date) AS INT) AS day_no FROM sales2)
SELECT sale_date, amount,
       SUM(amount) OVER (ORDER BY day_no RANGE BETWEEN 6 PRECEDING AND CURRENT ROW) AS sum_7_calendar_days
FROM d
ORDER BY sale_date;

-- MySQL 8: RANGE BETWEEN INTERVAL 6 DAY PRECEDING AND CURRENT ROW (not run here / from memory).
-- SQL Server: no INTERVAL in RANGE; use a correlated subquery or a calendar table (not run here).
```
**Output:**

Query 1 (run in duckdb):

| sale_date | amount | sum_7_calendar_days | sum_last_7_rows |
|---|---|---|---|
| 2026-03-01 | 100 | 100 | 100 |
| 2026-03-02 | 50 | 150 | 150 |
| 2026-03-05 | 70 | 220 | 220 |
| 2026-03-08 | 30 | 150 | 250 |
| 2026-03-09 | 20 | 120 | 270 |
| 2026-03-15 | 40 | 60 | 310 |
| 2026-03-16 | 10 | 50 | 320 |

Query 2 (run in sqlite):

| sale_date | amount | sum_7_calendar_days |
|---|---|---|
| 2026-03-01 | 100 | 100 |
| 2026-03-02 | 50 | 150 |
| 2026-03-05 | 70 | 220 |
| 2026-03-08 | 30 | 150 |
| 2026-03-09 | 20 | 120 |
| 2026-03-15 | 40 | 60 |
| 2026-03-16 | 10 | 50 |
**pandas equivalent:**
```python
import pandas as pd
sales2 = pd.DataFrame([
    ('2026-03-01', 100),
    ('2026-03-02', 50),
    ('2026-03-05', 70),
    ('2026-03-08', 30),
    ('2026-03-09', 20),
    ('2026-03-15', 40),
    ('2026-03-16', 10),
], columns=['sale_date', 'amount'])
s = sales2.assign(sale_date=pd.to_datetime(sales2['sale_date'])).set_index('sale_date')['amount']
out = s.rolling('7D').sum().to_frame('sum_7_calendar_days')
out['sum_last_7_rows'] = s.rolling(7, min_periods=1).sum()
out = out.reset_index()
out.insert(1, 'amount', sales2['amount'].values)
print(out.to_string(index=False))
```
Output (real run, matches the SQL result):
```text
 sale_date  amount  sum_7_calendar_days  sum_last_7_rows
2026-03-01     100                100.0            100.0
2026-03-02      50                150.0            150.0
2026-03-05      70                220.0            220.0
2026-03-08      30                150.0            250.0
2026-03-09      20                120.0            270.0
2026-03-15      40                 60.0            310.0
2026-03-16      10                 50.0            320.0
```
**Edge cases:** On 16 March the ROWS version still adds entries from 5 March and earlier (the gap is ignored) giving 320, while the 7-calendar-day sum correctly gives 50. The window must be ordered by a single date/number column. Empty days still produce no row, so add a calendar table if you need a row for every day.
**Likely follow-ups:**
- What if I need a row for every day? LEFT JOIN a calendar table to the data first, then ROWS and RANGE agree.
- What is a 7-day window in pandas? rolling('7D') on a datetime index.
**Common mistakes:** Using ROWS 6 PRECEDING on data with missing days and calling it 7 days, writing INTERVAL 7 DAYS (that is 8 calendar days including today), or ordering by a text date.

### Q41 ⭐ 🟡 How do you calculate a running total of only some rows, such as only refunds, using a CASE inside the window function?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you apply a condition inside a window function, instead of splitting the table?
**Say this in the interview:** I put a CASE inside the SUM so only refund rows add their amount and other rows add zero, then keep the running window around it. FILTER does the same on engines that support it.
**Explain simply:**
- SUM(CASE WHEN kind = 'refund' THEN amount ELSE 0 END) adds the amount only for refunds.
- OVER (ORDER BY day ...) then makes that a running total, so non-refund rows just repeat the previous total.
- FILTER (WHERE kind = 'refund') is a cleaner shortcut (PostgreSQL, SQLite, DuckDB). MySQL and SQL Server do not have it, so use CASE there.
- Use ELSE 0 (not ELSE NULL) if you want the total shown on every row; SUM ignores NULL anyway, but the first row would show NULL if it is not a refund.
**Example:** Finance wants cumulative refunds to date next to each day's transaction, to watch the refund budget.
**Sample data:** `txns`

| id | day | kind | amount |
|---|---|---|---|
| 1 | 2026-03-01 | sale | 500 |
| 2 | 2026-03-02 | refund | 80 |
| 3 | 2026-03-03 | sale | 300 |
| 4 | 2026-03-04 | refund | 120 |
| 5 | 2026-03-05 | sale | 200 |
| 6 | 2026-03-06 | refund | 50 |
**SQL:**
```sql
CREATE TABLE txns (id INT, day TEXT, kind TEXT, amount INT);

SELECT id, day, kind, amount,
       SUM(CASE WHEN kind = 'refund' THEN amount ELSE 0 END)
           OVER (ORDER BY day, id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_refunds,
       SUM(amount) FILTER (WHERE kind = 'refund')
           OVER (ORDER BY day, id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_refunds_filter
FROM txns
ORDER BY day, id;
```
**Output:** (run in sqlite)

| id | day | kind | amount | running_refunds | running_refunds_filter |
|---|---|---|---|---|---|
| 1 | 2026-03-01 | sale | 500 | 0 | NULL |
| 2 | 2026-03-02 | refund | 80 | 80 | 80 |
| 3 | 2026-03-03 | sale | 300 | 80 | 80 |
| 4 | 2026-03-04 | refund | 120 | 200 | 200 |
| 5 | 2026-03-05 | sale | 200 | 200 | 200 |
| 6 | 2026-03-06 | refund | 50 | 250 | 250 |
**pandas equivalent:**
```python
import pandas as pd
txns = pd.DataFrame([
    (1, '2026-03-01', 'sale', 500),
    (2, '2026-03-02', 'refund', 80),
    (3, '2026-03-03', 'sale', 300),
    (4, '2026-03-04', 'refund', 120),
    (5, '2026-03-05', 'sale', 200),
    (6, '2026-03-06', 'refund', 50),
], columns=['id', 'day', 'kind', 'amount'])
out = txns.sort_values(['day', 'id']).reset_index(drop=True)
out['running_refunds'] = out['amount'].where(out['kind'] == 'refund', 0).cumsum()
out['running_refunds_filter'] = out['amount'].where(out['kind'] == 'refund').cumsum().ffill()
print(out.to_string(index=False))
```
Output (real run, matches the SQL result):
```text
 id        day   kind  amount  running_refunds  running_refunds_filter
  1 2026-03-01   sale     500                0                     NaN
  2 2026-03-02 refund      80               80                    80.0
  3 2026-03-03   sale     300               80                    80.0
  4 2026-03-04 refund     120              200                   200.0
  5 2026-03-05   sale     200              200                   200.0
  6 2026-03-06 refund      50              250                   250.0
```
**Edge cases:** FILTER gives NULL until the first refund occurs (the row's window has no matching rows), whereas CASE gives 0. pandas: cumsum skips NaN, so I mask the early rows to reproduce this. No refunds at all: CASE column is all 0, FILTER column all NULL.
**Likely follow-ups:**
- Running refund share of sales? Divide the two conditional running sums, using NULLIF on the denominator.
- Why not WHERE kind='refund'? WHERE removes the other rows from the output; the CASE keeps every row.
**Common mistakes:** Filtering with WHERE (losing rows), forgetting ELSE 0, leaving out the frame, and using the default RANGE frame so tied dates all show the same total.

### Q42 ⭐ 🟡 How do you calculate a moving average of the previous 3 days that excludes the current day?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you shift the window frame so the current row is excluded, a common leak-free trend feature?
**Say this in the interview:** I use ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING, which is the three rows before today and stops one short of today.
**Explain simply:**
- The frame is a sliding box of rows around the current row. '1 PRECEDING' as the end means 'stop one row before me'.
- So AVG over that box is the average of the previous three days only, which is useful for comparing today against its recent normal.
- The first row has no earlier rows, so the result is NULL. The second row averages one day, the third two days, and so on until three days exist.
- Alternative: keep the box ending at CURRENT ROW and add EXCLUDE CURRENT ROW (PostgreSQL 11+, SQLite, DuckDB; not MySQL/SQL Server).
**Example:** Is today's 200 orders unusual? Compare it with the average of the previous three days (the average without today, otherwise today drags its own benchmark up).
**Sample data:** `sales`

| day | amount |
|---|---|
| 2026-03-01 | 100 |
| 2026-03-02 | 150 |
| 2026-03-03 | 120 |
| 2026-03-04 | 200 |
| 2026-03-05 | 180 |
| 2026-03-06 | 90 |
**SQL:**
```sql
CREATE TABLE sales (day TEXT, amount INT);

SELECT day, amount,
       ROUND(AVG(amount) OVER (ORDER BY day ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING), 2) AS prev3_avg,
       ROUND(AVG(amount) OVER (ORDER BY day ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
                               EXCLUDE CURRENT ROW), 2) AS prev3_avg_exclude
FROM sales
ORDER BY day;
```
**Output:** (run in sqlite)

| day | amount | prev3_avg | prev3_avg_exclude |
|---|---|---|---|
| 2026-03-01 | 100 | NULL | NULL |
| 2026-03-02 | 150 | 100 | 100 |
| 2026-03-03 | 120 | 125 | 125 |
| 2026-03-04 | 200 | 123.33 | 123.33 |
| 2026-03-05 | 180 | 156.67 | 156.67 |
| 2026-03-06 | 90 | 166.67 | 166.67 |
**pandas equivalent:**
```python
import pandas as pd
sales = pd.DataFrame([
    ('2026-03-01', 100),
    ('2026-03-02', 150),
    ('2026-03-03', 120),
    ('2026-03-04', 200),
    ('2026-03-05', 180),
    ('2026-03-06', 90),
], columns=['day', 'amount'])
out = sales.sort_values('day').reset_index(drop=True)
prev = out['amount'].shift(1)
out['prev3_avg'] = prev.rolling(3, min_periods=1).mean().round(2)
out['prev3_avg_exclude'] = out['prev3_avg']
print(out.to_string(index=False))
```
Output (real run, matches the SQL result):
```text
       day  amount  prev3_avg  prev3_avg_exclude
2026-03-01     100        NaN                NaN
2026-03-02     150     100.00             100.00
2026-03-03     120     125.00             125.00
2026-03-04     200     123.33             123.33
2026-03-05     180     156.67             156.67
2026-03-06      90     166.67             166.67
```
**Edge cases:** Row 1 is NULL. Rows 2 and 3 average fewer than 3 days; if you need a full 3 days, wrap it as CASE WHEN COUNT(*) OVER (same frame) = 3 THEN avg END. Missing dates are not handled by ROWS.
**Likely follow-ups:**
- How do I then flag unusual days? Compare amount with prev3_avg, e.g. amount > 1.5 * prev3_avg, in an outer query.
- pandas? shift(1) then rolling(3), or rolling(3, closed='left') on a time index.
**Common mistakes:** Using 3 PRECEDING AND CURRENT ROW (that includes today and is 4 rows), or writing 1 PRECEDING AND 3 PRECEDING (the frame start must come first).

### Q43 ⭐ 🟡 What does NTH_VALUE() do, and how is it different from FIRST_VALUE()?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know NTH_VALUE picks the n-th row of the frame, and that the default frame hides later rows?
**Say this in the interview:** FIRST_VALUE is always the first row of the frame; NTH_VALUE(col, 2) is the second. Because the default frame ends at the current row, I set the frame to UNBOUNDED FOLLOWING or the first rows show NULL.
**Explain simply:**
- FIRST_VALUE(x) = same as NTH_VALUE(x, 1). NTH_VALUE(x, n) = the value in the n-th row of the frame.
- If the frame does not have n rows yet, the result is NULL.
- Default frame with ORDER BY = start of partition to current row, so the 2nd value is NULL on the first row.
- Fix: ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING.
- Classic use: second-highest salary per department (order by salary DESC).
**Example:** HR wants to show each person alongside the second-highest salary in their department.
**Sample data:** `emp`

| emp_id | name | dept | salary |
|---|---|---|---|
| 1 | Asha | HR | 50000 |
| 2 | Bala | HR | 60000 |
| 3 | Chitra | HR | 60000 |
| 4 | Dev | IT | 70000 |
| 5 | Esha | IT | 90000 |
| 6 | Farhan | IT | 80000 |
| 7 | Gita | Sales | 45000 |
**SQL:**
```sql
CREATE TABLE emp (emp_id INT, name TEXT, dept TEXT, salary INT);

SELECT name, dept, salary,
       FIRST_VALUE(salary) OVER w_full AS highest,
       NTH_VALUE(salary, 2) OVER w_default AS second_default_frame,
       NTH_VALUE(salary, 2) OVER w_full    AS second_full_frame
FROM emp
WINDOW w_default AS (PARTITION BY dept ORDER BY salary DESC, emp_id),
       w_full AS (PARTITION BY dept ORDER BY salary DESC, emp_id
                  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
ORDER BY dept, salary DESC, emp_id;

-- Dialects: NTH_VALUE exists in PostgreSQL, MySQL 8, SQL Server 2022, SQLite, DuckDB (not in older SQL Server; use ROW_NUMBER then). The named WINDOW clause is not in SQL Server (not run here / from memory).
```
**Output:** (run in sqlite)

| name | dept | salary | highest | second_default_frame | second_full_frame |
|---|---|---|---|---|---|
| Bala | HR | 60000 | 60000 | NULL | 60000 |
| Chitra | HR | 60000 | 60000 | 60000 | 60000 |
| Asha | HR | 50000 | 60000 | 60000 | 60000 |
| Esha | IT | 90000 | 90000 | NULL | 80000 |
| Farhan | IT | 80000 | 90000 | 80000 | 80000 |
| Dev | IT | 70000 | 90000 | 80000 | 80000 |
| Gita | Sales | 45000 | 45000 | NULL | NULL |
**pandas equivalent:**
```python
import pandas as pd
emp = pd.DataFrame([
    (1, 'Asha', 'HR', 50000),
    (2, 'Bala', 'HR', 60000),
    (3, 'Chitra', 'HR', 60000),
    (4, 'Dev', 'IT', 70000),
    (5, 'Esha', 'IT', 90000),
    (6, 'Farhan', 'IT', 80000),
    (7, 'Gita', 'Sales', 45000),
], columns=['emp_id', 'name', 'dept', 'salary'])
out = emp.sort_values(['dept', 'salary', 'emp_id'], ascending=[True, False, True]).reset_index(drop=True)
g = out.groupby('dept')['salary']
out['highest'] = g.transform('first')
out['second_full_frame'] = g.transform(lambda s: s.iloc[1] if len(s) > 1 else np.nan)
out['second_default_frame'] = out['second_full_frame'].where(g.cumcount() >= 1)
out = out[['name', 'dept', 'salary', 'highest', 'second_default_frame', 'second_full_frame']]
print(out.to_string(index=False))
```
Output (real run, matches the SQL result):
```text
  name  dept  salary  highest  second_default_frame  second_full_frame
  Bala    HR   60000    60000                   NaN            60000.0
Chitra    HR   60000    60000               60000.0            60000.0
  Asha    HR   50000    60000               60000.0            60000.0
  Esha    IT   90000    90000                   NaN            80000.0
Farhan    IT   80000    90000               80000.0            80000.0
   Dev    IT   70000    90000               80000.0            80000.0
  Gita Sales   45000    45000                   NaN                NaN
```
**Edge cases:** Departments with a single person (Sales) give NULL for the second value. Ties count as separate rows (two people on 60,000 in HR fill positions 2 and 3), so 'second-highest salary value' needs DENSE_RANK instead. NTH_VALUE counts NULLs unless IGNORE NULLS is supported (Oracle, SQL Server 2022; not PostgreSQL/MySQL).
**Likely follow-ups:**
- Second highest salary overall without NTH_VALUE? DENSE_RANK() = 2 in a subquery.
- Difference to LEAD? LEAD is relative to the current row; NTH_VALUE is absolute inside the frame.
**Common mistakes:** Not widening the frame (getting NULLs), mixing up row number and distinct value with ties, and forgetting the ORDER BY (the n-th row is meaningless).

### Q44 ⭐ 🟡 What is the GROUPS frame type, and when would it differ from ROWS and RANGE?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the three frame types and how they treat ties and gaps differently?
**Say this in the interview:** ROWS counts rows, RANGE counts values, and GROUPS counts groups of tied rows. GROUPS 1 PRECEDING means 'the previous group of equal values plus the current group'.
**Explain simply:**
- ROWS 1 PRECEDING: exactly the previous physical row.
- RANGE 1 PRECEDING: every row whose sort value is within 1 of the current value (a distance on the value itself).
- GROUPS 1 PRECEDING: the previous peer group, where peers are rows with the same ORDER BY value, no matter how large the gap between values is.
- It matters when the ORDER BY column has ties or gaps, e.g. several orders per date, with missing dates.
- Support: PostgreSQL 11+, SQLite 3.28+, DuckDB. Not MySQL or SQL Server (not run here / from memory).
**Example:** Orders per day where 2 orders happen on the same day and some days are missing: 'last 2 days with activity' is a GROUPS question.
**Sample data:** `t`

| id | day | amt |
|---|---|---|
| 1 | 1 | 10 |
| 2 | 2 | 20 |
| 3 | 2 | 30 |
| 4 | 5 | 40 |
| 5 | 6 | 50 |
**SQL:**
```sql
CREATE TABLE t (id INT, day INT, amt INT);

SELECT id, day, amt,
       SUM(amt) OVER (ORDER BY day, id ROWS   BETWEEN 1 PRECEDING AND CURRENT ROW) AS rows_sum,
       SUM(amt) OVER (ORDER BY day     RANGE  BETWEEN 1 PRECEDING AND CURRENT ROW) AS range_sum,
       SUM(amt) OVER (ORDER BY day     GROUPS BETWEEN 1 PRECEDING AND CURRENT ROW) AS groups_sum
FROM t
ORDER BY day, id;
```
**Output:** (run in sqlite)

| id | day | amt | rows_sum | range_sum | groups_sum |
|---|---|---|---|---|---|
| 1 | 1 | 10 | 10 | 10 | 10 |
| 2 | 2 | 20 | 30 | 60 | 60 |
| 3 | 2 | 30 | 50 | 60 | 60 |
| 4 | 5 | 40 | 70 | 40 | 90 |
| 5 | 6 | 50 | 90 | 90 | 90 |
**pandas equivalent:**
```python
import pandas as pd
t = pd.DataFrame([
    (1, 1, 10),
    (2, 2, 20),
    (3, 2, 30),
    (4, 5, 40),
    (5, 6, 50),
], columns=['id', 'day', 'amt'])
rows = t.sort_values(['day', 'id']).reset_index(drop=True)
out = rows.copy()
out['rows_sum'] = out['amt'].rolling(2, min_periods=1).sum()
out['range_sum'] = [rows.loc[(rows.day >= d - 1) & (rows.day <= d), 'amt'].sum() for d in rows.day]
by_day = rows.groupby('day')['amt'].sum()
days = list(by_day.index)
out['groups_sum'] = [by_day.iloc[max(days.index(d) - 1, 0): days.index(d) + 1].sum() for d in rows.day]
print(out.to_string(index=False))
```
Output (real run, matches the SQL result):
```text
 id  day  amt  rows_sum  range_sum  groups_sum
  1    1   10      10.0         10          10
  2    2   20      30.0         60          60
  3    2   30      50.0         60          60
  4    5   40      70.0         40          90
  5    6   50      90.0         90          90
```
**Edge cases:** Day 5 shows the difference: ROWS adds row 3 (30), RANGE adds nothing earlier (days 3 and 4 do not exist), GROUPS adds the previous group, day 2 (20 + 30). For ROWS the window order of tied rows must be made unique (add id). RANGE with numbers needs a single numeric/date ORDER BY.
**Likely follow-ups:**
- Which frame is the default? RANGE UNBOUNDED PRECEDING to CURRENT ROW when ORDER BY is present.
- Do I need GROUPS often? Rarely. Name it, give the tie example, and say ROWS or a calendar table is usually enough.
**Common mistakes:** Assuming ROWS and RANGE are the same, forgetting that RANGE/GROUPS include all tied peers of the current row, and using GROUPS on a database that lacks it.

### Q45 ⭐ 🟡 How do you fill NULLs with the last known value (forward fill) using window functions?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you fill gaps with the last known value, a common data-cleaning step, using only standard window tools?
**Say this in the interview:** I count the non-NULL values so far to create a group number that changes whenever a real value appears, then take the MAX of that group. Every NULL row inherits the value that started its group.
**Explain simply:**
- COUNT(col) ignores NULLs, so a running COUNT(col) only goes up on rows that have a value.
- That running count is a label: all rows after one real value (up to the next one) share a label.
- MAX(col) OVER (PARTITION BY label) then returns that one real value for the whole group.
- Some engines have LAST_VALUE(col IGNORE NULLS) (Oracle, SQL Server 2022, DuckDB). PostgreSQL, MySQL and SQLite do not, so this trick is the portable way.
**Example:** Salary is recorded only in months where it changed. HR wants the salary in force each month.
**Sample data:** `pay`

| emp_id | month | salary |
|---|---|---|
| 101 | 2026-01 | 50000 |
| 101 | 2026-02 | NULL |
| 101 | 2026-03 | NULL |
| 101 | 2026-04 | 55000 |
| 101 | 2026-05 | NULL |
| 102 | 2026-01 | NULL |
| 102 | 2026-02 | 40000 |
| 102 | 2026-03 | NULL |
**SQL:**
```sql
CREATE TABLE pay (emp_id INT, month TEXT, salary INT);

WITH g AS (
  SELECT emp_id, month, salary,
         COUNT(salary) OVER (PARTITION BY emp_id ORDER BY month
                             ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS grp
  FROM pay)
SELECT emp_id, month, salary,
       MAX(salary) OVER (PARTITION BY emp_id, grp) AS salary_filled
FROM g
ORDER BY emp_id, month;
```
**Output:** (run in sqlite)

| emp_id | month | salary | salary_filled |
|---|---|---|---|
| 101 | 2026-01 | 50000 | 50000 |
| 101 | 2026-02 | NULL | 50000 |
| 101 | 2026-03 | NULL | 50000 |
| 101 | 2026-04 | 55000 | 55000 |
| 101 | 2026-05 | NULL | 55000 |
| 102 | 2026-01 | NULL | NULL |
| 102 | 2026-02 | 40000 | 40000 |
| 102 | 2026-03 | NULL | 40000 |
**pandas equivalent:**
```python
import pandas as pd
pay = pd.DataFrame([
    (101, '2026-01', 50000),
    (101, '2026-02', None),
    (101, '2026-03', None),
    (101, '2026-04', 55000),
    (101, '2026-05', None),
    (102, '2026-01', None),
    (102, '2026-02', 40000),
    (102, '2026-03', None),
], columns=['emp_id', 'month', 'salary'])
out = pay.sort_values(['emp_id', 'month']).reset_index(drop=True)
out['salary_filled'] = out.groupby('emp_id')['salary'].ffill()
print(out.to_string(index=False))
```
Output (real run, matches the SQL result):
```text
 emp_id   month  salary  salary_filled
    101 2026-01 50000.0        50000.0
    101 2026-02     NaN        50000.0
    101 2026-03     NaN        50000.0
    101 2026-04 55000.0        55000.0
    101 2026-05     NaN        55000.0
    102 2026-01     NaN            NaN
    102 2026-02 40000.0        40000.0
    102 2026-03     NaN        40000.0
```
**Edge cases:** Leading NULLs (employee 102 in January) stay NULL: nothing earlier exists. A genuine NULL meaning 'no salary' cannot be told apart from a missing one. Without PARTITION BY emp_id, one employee's value would flow into the next.
**Likely follow-ups:**
- Back fill (use next value)? Run the same idea in reverse order, or use FIRST_VALUE over later rows.
- Why not LAG? LAG only looks one row back and fails when several NULLs are in a row.
**Common mistakes:** Using LAG once (fills only a one-row gap), forgetting PARTITION BY, using MAX without the group label (returns the overall maximum), and using the default RANGE frame.

### Q46 ⭐ 🔴 How do you calculate a running bank balance from deposits and withdrawals, and find the first date it went negative?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you turn two kinds of transaction into one signed amount, build a running balance, and then pick the first row that meets a condition?
**Say this in the interview:** I convert withdrawals into negative amounts, take a running SUM ordered by date and id to get the balance, then in an outer query keep the rows where the balance is below zero and take the earliest.
**Explain simply:**
- Signed amount: deposit = +amount, withdrawal = -amount, via CASE.
- Running balance = SUM(signed amount) OVER (ORDER BY date, id). The id breaks ties between same-day transactions.
- You cannot filter on a window result in WHERE, so put the balance in a CTE (a named temporary result) first.
- 'First' = smallest date and id among rows where balance < 0.
**Example:** Employee salary-advance account: start with 1,000 deposit, then withdrawals. On which date did it first overdraw?
**Sample data:** `bank`

| id | txn_date | kind | amount |
|---|---|---|---|
| 1 | 2026-03-01 | deposit | 1000 |
| 2 | 2026-03-03 | withdrawal | 400 |
| 3 | 2026-03-05 | withdrawal | 500 |
| 4 | 2026-03-08 | withdrawal | 300 |
| 5 | 2026-03-10 | deposit | 700 |
| 6 | 2026-03-12 | withdrawal | 200 |
**SQL:**
```sql
CREATE TABLE bank (id INT, txn_date TEXT, kind TEXT, amount INT);

WITH b AS (
  SELECT id, txn_date, kind, amount,
         SUM(CASE WHEN kind = 'deposit' THEN amount ELSE -amount END)
             OVER (ORDER BY txn_date, id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS balance
  FROM bank)
SELECT * FROM b ORDER BY txn_date, id;

WITH b AS (
  SELECT id, txn_date, kind, amount,
         SUM(CASE WHEN kind = 'deposit' THEN amount ELSE -amount END)
             OVER (ORDER BY txn_date, id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS balance
  FROM bank)
SELECT txn_date AS first_negative_date, balance
FROM b
WHERE balance < 0
ORDER BY txn_date, id
LIMIT 1;

-- Dialects: LIMIT 1 -> SELECT TOP 1 (SQL Server) or FETCH FIRST 1 ROW ONLY (standard/PostgreSQL/Oracle) (not run here).
```
**Output:**

Query 1 (run in sqlite):

| id | txn_date | kind | amount | balance |
|---|---|---|---|---|
| 1 | 2026-03-01 | deposit | 1000 | 1000 |
| 2 | 2026-03-03 | withdrawal | 400 | 600 |
| 3 | 2026-03-05 | withdrawal | 500 | 100 |
| 4 | 2026-03-08 | withdrawal | 300 | -200 |
| 5 | 2026-03-10 | deposit | 700 | 500 |
| 6 | 2026-03-12 | withdrawal | 200 | 300 |

Query 2 (run in sqlite):

| first_negative_date | balance |
|---|---|
| 2026-03-08 | -200 |
**pandas equivalent:**
```python
import pandas as pd
bank = pd.DataFrame([
    (1, '2026-03-01', 'deposit', 1000),
    (2, '2026-03-03', 'withdrawal', 400),
    (3, '2026-03-05', 'withdrawal', 500),
    (4, '2026-03-08', 'withdrawal', 300),
    (5, '2026-03-10', 'deposit', 700),
    (6, '2026-03-12', 'withdrawal', 200),
], columns=['id', 'txn_date', 'kind', 'amount'])
out = bank.sort_values(['txn_date', 'id']).reset_index(drop=True)
out['balance'] = out['amount'].where(out['kind'] == 'deposit', -out['amount']).cumsum()
print(out.to_string(index=False))
first_neg = out[out['balance'] < 0].head(1)[['txn_date', 'balance']]
print(first_neg.to_string(index=False))
```
Output (real run, matches the SQL result):
```text
 id   txn_date       kind  amount  balance
  1 2026-03-01    deposit    1000     1000
  2 2026-03-03 withdrawal     400      600
  3 2026-03-05 withdrawal     500      100
  4 2026-03-08 withdrawal     300     -200
  5 2026-03-10    deposit     700      500
  6 2026-03-12 withdrawal     200      300
  txn_date  balance
2026-03-08     -200
```
**Edge cases:** The account can go negative, recover and go negative again; the query returns only the first time. If it never goes negative the second query returns no rows. Same-day transactions need the id tiebreaker or the order is unpredictable. 'Balance below zero' vs 'zero or below' is a business decision to confirm.
**Likely follow-ups:**
- Show every overdraft episode? Use LAG(balance) to detect balance < 0 with previous balance >= 0.
- What if there is an opening balance? Add it as a first row, or add it to the running SUM.
**Common mistakes:** Forgetting the minus sign for withdrawals, filtering the window result in WHERE directly, no tiebreaker for same-day rows, and ordering by date only (so default RANGE frame groups same-day rows).

### Q47 ⭐ 🔴 How do you detect three consecutive days of increasing stock price using LAG()?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you use LAG twice to look two rows back and combine conditions, and spot the 'three days vs three rises' ambiguity?
**Say this in the interview:** I pull yesterday's and the day before's price with LAG, and keep days where price is above yesterday and yesterday is above the day before, giving three days of consecutive increases.
**Explain simply:**
- LAG(price, 1) is yesterday; LAG(price, 2) is two days ago.
- Three days increasing: price(day) > price(day-1) > price(day-2).
- The comparison must be done in an outer query or CTE, because window results cannot be used in WHERE.
- Ambiguity: three days increasing means two rises. If the interviewer means three rises in a row, add LAG(price, 3).
- For streaks of any length use the 'islands' method (group rows by day number minus running count).
**Example:** Attendance rate improving three days in a row, or a share price rising for three straight days.
**Sample data:** `prices`

| day | price |
|---|---|
| 1 | 100 |
| 2 | 101 |
| 3 | 103 |
| 4 | 102 |
| 5 | 104 |
| 6 | 105 |
| 7 | 107 |
| 8 | 106 |
**SQL:**
```sql
CREATE TABLE prices (day INT, price INT);

WITH p AS (
  SELECT day, price,
         LAG(price, 1) OVER (ORDER BY day) AS yesterday,
         LAG(price, 2) OVER (ORDER BY day) AS two_days_ago
  FROM prices)
SELECT day, two_days_ago, yesterday, price
FROM p
WHERE price > yesterday AND yesterday > two_days_ago
ORDER BY day;
```
**Output:** (run in sqlite)

| day | two_days_ago | yesterday | price |
|---|---|---|---|
| 3 | 100 | 101 | 103 |
| 6 | 102 | 104 | 105 |
| 7 | 104 | 105 | 107 |
**pandas equivalent:**
```python
import pandas as pd
prices = pd.DataFrame([
    (1, 100),
    (2, 101),
    (3, 103),
    (4, 102),
    (5, 104),
    (6, 105),
    (7, 107),
    (8, 106),
], columns=['day', 'price'])
out = prices.sort_values('day').reset_index(drop=True)
out['yesterday'] = out['price'].shift(1)
out['two_days_ago'] = out['price'].shift(2)
out = out[(out['price'] > out['yesterday']) & (out['yesterday'] > out['two_days_ago'])]
out = out[['day', 'two_days_ago', 'yesterday', 'price']].reset_index(drop=True)
print(out.to_string(index=False))
```
Output (real run, matches the SQL result):
```text
 day  two_days_ago  yesterday  price
   3         100.0      101.0    103
   6         102.0      104.0    105
   7         104.0      105.0    107
```
**Edge cases:** The first two days can never match (NULL comparisons are not true). Equal prices are not an increase. Days 6 and 7 both appear because windows overlap; a four-day rise is reported twice. Gaps in dates (weekends) mean the 'previous row' may not be the previous calendar day; decide whether that matters.
**Likely follow-ups:**
- Longest streak? Flag each up day, group consecutive flags with ROW_NUMBER differences, then COUNT per group.
- Use LEAD instead? Yes, it reports the first day of the run instead of the last.
**Common mistakes:** Writing the conditions in WHERE of the same SELECT as LAG, comparing with >= when strictly increasing is needed, and forgetting the NULL rows at the start.

### Q48 ⭐ 🔴 How do you calculate a running total that resets when a condition is met (for example, when a limit is crossed)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know plain window functions cannot reset based on a running result, and that you need a recursive CTE (or a loop)?
**Say this in the interview:** A running total that restarts depends on its own previous answer, which a window function cannot see. So I use a recursive CTE: each step either adds to the previous total or starts again from the current amount.
**Explain simply:**
- A recursive CTE is a query that calls itself: a starting row, then a rule to build the next row from the previous one.
- Rule here: if the previous total hit the limit (100), restart with today's amount, otherwise add to it.
- SUM() OVER can reset on a known label (a department) but not on a limit crossed by its own running result.
- In a real project, many analysts do this part in Python/pandas with a loop.
**Example:** Overtime hours: whenever the running hours reach 100, a bonus is paid and the counter restarts.
**Sample data:** `orders_amt`

| id | amt |
|---|---|
| 1 | 40 |
| 2 | 30 |
| 3 | 50 |
| 4 | 20 |
| 5 | 90 |
| 6 | 15 |
| 7 | 60 |
| 8 | 70 |
**SQL:**
```sql
CREATE TABLE orders_amt (id INT, amt INT);

WITH RECURSIVE r(id, amt, run_total, hit) AS (
  SELECT id, amt, amt, CASE WHEN amt >= 100 THEN 1 ELSE 0 END
  FROM orders_amt WHERE id = 1
  UNION ALL
  SELECT o.id, o.amt,
         CASE WHEN r.hit = 1 THEN o.amt ELSE r.run_total + o.amt END,
         CASE WHEN (CASE WHEN r.hit = 1 THEN o.amt ELSE r.run_total + o.amt END) >= 100 THEN 1 ELSE 0 END
  FROM r JOIN orders_amt o ON o.id = r.id + 1)
SELECT id, amt, run_total, hit AS limit_reached
FROM r
ORDER BY id;

-- Dialects: SQL Server and Oracle omit the word RECURSIVE (WITH r AS ...); PostgreSQL, MySQL 8 and SQLite need it. Not run here for SQL Server/Oracle.
```
**Output:** (run in sqlite)

| id | amt | run_total | limit_reached |
|---|---|---|---|
| 1 | 40 | 40 | 0 |
| 2 | 30 | 70 | 0 |
| 3 | 50 | 120 | 1 |
| 4 | 20 | 20 | 0 |
| 5 | 90 | 110 | 1 |
| 6 | 15 | 15 | 0 |
| 7 | 60 | 75 | 0 |
| 8 | 70 | 145 | 1 |
**pandas equivalent:**
```python
import pandas as pd
orders_amt = pd.DataFrame([
    (1, 40),
    (2, 30),
    (3, 50),
    (4, 20),
    (5, 90),
    (6, 15),
    (7, 60),
    (8, 70),
], columns=['id', 'amt'])
out = orders_amt.sort_values('id').reset_index(drop=True)
totals, hits, run = [], [], 0
for a in out['amt']:
    run = a if (hits and hits[-1] == 1) or not totals else run + a
    totals.append(run)
    hits.append(1 if run >= 100 else 0)
out['run_total'] = totals
out['limit_reached'] = hits
print(out.to_string(index=False))
```
Output (real run, matches the SQL result):
```text
 id  amt  run_total  limit_reached
  1   40         40              0
  2   30         70              0
  3   50        120              1
  4   20         20              0
  5   90        110              1
  6   15         15              0
  7   60         75              0
  8   70        145              1
```
**Edge cases:** Rows must be numbered consecutively (use ROW_NUMBER() in a first CTE if ids have gaps). 'Reset after crossing' vs 'reset when the crossing row is excluded' are different rules, so confirm. Very long tables make recursive CTEs slow and may hit a recursion limit (SQL Server default 100; MAXRECURSION).
**Likely follow-ups:**
- Is there a non-recursive way? Not for a true data-dependent reset; some tricks exist for fixed rules.
- Is it efficient? It walks row by row, so use it on small or filtered sets, or do it in Python.
**Common mistakes:** Trying SUM() OVER with a CASE reset (the window cannot see its own result), forgetting UNION ALL, and joining on id + 1 when ids have gaps.

### Q49 ⭐ 🔴 How do you calculate a median per group using window functions (PERCENTILE_CONT) and what is the alternative in MySQL?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the median is the 50th percentile, how engines differ, and a portable fallback?
**Say this in the interview:** Where PERCENTILE_CONT(0.5) is available I use it; in MySQL I number the rows per group and average the one or two middle rows.
**Explain simply:**
- The median is the middle value when sorted; with an even count it is the average of the two middle values.
- PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) computes it. In PostgreSQL, Oracle and DuckDB it is an aggregate (use GROUP BY); in SQL Server it is a window function (OVER (PARTITION BY ...)); MySQL has neither.
- AVG would be pulled up by one very high salary; the median is not.
- MySQL/SQLite alternative: ROW_NUMBER and COUNT per group; keep the rows at positions (n+1)/2 and (n+2)/2 and average them (integer division).
**Example:** Median salary per department: HR has an outlier (90,000), so the average would mislead.
**Sample data:** `staff`

| name | dept | salary |
|---|---|---|
| A | HR | 40000 |
| B | HR | 50000 |
| C | HR | 60000 |
| D | HR | 90000 |
| E | IT | 70000 |
| F | IT | 80000 |
| G | IT | 120000 |
| H | Sales | 45000 |
| I | Sales | 55000 |
**SQL:**
```sql
CREATE TABLE staff (name TEXT, dept TEXT, salary INT);

SELECT dept,
       PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median_salary
FROM staff
GROUP BY dept
ORDER BY dept;

-- Portable (MySQL 8 / SQLite / any engine with window functions)
WITH r AS (
  SELECT dept, salary,
         ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary) AS rn,
         COUNT(*)     OVER (PARTITION BY dept) AS n
  FROM staff)
SELECT dept, AVG(salary) AS median_salary
FROM r
WHERE rn IN ((n + 1) / 2, (n + 2) / 2)
GROUP BY dept
ORDER BY dept;

-- SQL Server (window form, not run here): SELECT DISTINCT dept, PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) OVER (PARTITION BY dept) FROM staff;
-- PostgreSQL: the aggregate form above also works (PostgreSQL has no window form; from memory).
```
**Output:**

Query 1 (run in duckdb):

| dept | median_salary |
|---|---|
| HR | 55000 |
| IT | 80000 |
| Sales | 50000 |

Query 2 (run in sqlite):

| dept | median_salary |
|---|---|
| HR | 55000 |
| IT | 80000 |
| Sales | 50000 |
**pandas equivalent:**
```python
import pandas as pd
staff = pd.DataFrame([
    ('A', 'HR', 40000),
    ('B', 'HR', 50000),
    ('C', 'HR', 60000),
    ('D', 'HR', 90000),
    ('E', 'IT', 70000),
    ('F', 'IT', 80000),
    ('G', 'IT', 120000),
    ('H', 'Sales', 45000),
    ('I', 'Sales', 55000),
], columns=['name', 'dept', 'salary'])
out = staff.groupby('dept', as_index=False)['salary'].median().rename(columns={'salary': 'median_salary'})
print(out.to_string(index=False))
```
Output (real run, matches the SQL result):
```text
 dept  median_salary
   HR        55000.0
   IT        80000.0
Sales        50000.0
```
**Edge cases:** Even counts average the two middle values (HR: 55,000). NULL salaries are ignored by PERCENTILE_CONT; in the portable method filter WHERE salary IS NOT NULL before numbering or the count is wrong. PERCENTILE_DISC returns an actual value from the data instead of interpolating.
**Likely follow-ups:**
- Median vs mean? Median resists outliers; report both when pay is skewed.
- Median of the whole company? Drop the PARTITION BY / GROUP BY.
**Common mistakes:** Using AVG and calling it median, forgetting ORDER BY inside WITHIN GROUP, and in the portable method using / on engines where it returns a decimal (use integer division, or FLOOR).

### Q50 ⭐ 🔴 How do you calculate an exponential moving average in SQL, and why is it hard?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand an EMA depends on its own previous value, so window functions alone cannot do it, and you need recursion?
**Say this in the interview:** An exponential moving average is today's value weighted by alpha plus yesterday's EMA weighted by one minus alpha. Because it uses its own previous result, I need a recursive CTE or I do it in Python.
**Explain simply:**
- Simple moving average: every day in the window counts equally. EMA: recent days count more, old days fade away but never fully disappear.
- Formula: EMA(today) = alpha x value + (1 - alpha) x EMA(yesterday). First EMA = first value.
- alpha = 2 / (N + 1) for an N-day EMA (0.5 here is a 3-day EMA).
- Hard in SQL because a window function can only see source columns, not its own output. Recursive CTE is needed.
**Example:** Daily order counts: EMA 'remembers' a spike for a few days instead of dropping it suddenly like a 5-day average.
**Sample data:** `daily`

| day | orders |
|---|---|
| 1 | 10 |
| 2 | 12 |
| 3 | 11 |
| 4 | 15 |
| 5 | 14 |
**SQL:**
```sql
CREATE TABLE daily (day INT, orders INT);

WITH RECURSIVE e(day, orders, ema) AS (
  SELECT day, orders, CAST(orders AS REAL) FROM daily WHERE day = 1
  UNION ALL
  SELECT d.day, d.orders, 0.5 * d.orders + 0.5 * e.ema
  FROM e JOIN daily d ON d.day = e.day + 1)
SELECT day, orders, ROUND(ema, 4) AS ema_alpha_0_5
FROM e
ORDER BY day;
```
**Output:** (run in sqlite)

| day | orders | ema_alpha_0_5 |
|---|---|---|
| 1 | 10 | 10 |
| 2 | 12 | 11 |
| 3 | 11 | 11 |
| 4 | 15 | 13 |
| 5 | 14 | 13.5 |
**pandas equivalent:**
```python
import pandas as pd
daily = pd.DataFrame([
    (1, 10),
    (2, 12),
    (3, 11),
    (4, 15),
    (5, 14),
], columns=['day', 'orders'])
out = daily.sort_values('day').reset_index(drop=True)
out['ema_alpha_0_5'] = out['orders'].ewm(alpha=0.5, adjust=False).mean().round(4)
print(out.to_string(index=False))
```
Output (real run, matches the SQL result):
```text
 day  orders  ema_alpha_0_5
   1      10           10.0
   2      12           11.0
   3      11           11.0
   4      15           13.0
   5      14           13.5
```
**Edge cases:** Days must be consecutive numbers (use ROW_NUMBER otherwise). Warm-up: the first values depend on the starting choice (pandas adjust=True gives a different start). Missing days change the meaning. NULL values break the chain, so fill them first.
**Likely follow-ups:**
- Is there a closed form? Yes, a weighted sum with POWER(1 - alpha, k) and a window SUM, but it is clumsy and overflows on long histories.
- What would you do in practice? Compute it in pandas or a BI tool; keep SQL for the heavy aggregation.
**Common mistakes:** Applying AVG with a window (that is a simple average), forgetting to seed the first row, and mixing up alpha with the number of days.

### Q51 ⭐ 🔴 How do you find rows where the value is greater than both the previous and the next row (local peaks) using LAG and LEAD?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you combine LAG and LEAD in one query and filter using a subquery?
**Say this in the interview:** I bring in the previous and next value on each row, then keep rows where the value is bigger than both, which are local peaks.
**Explain simply:**
- LAG gives the row before, LEAD the row after.
- A local peak is higher than its neighbours on both sides.
- Put both functions in a CTE/subquery, then filter in the outer query.
- The first and last rows have a missing neighbour (NULL), so they are never counted as peaks.
**Example:** Daily absenteeism counts: find the days that spiked above the days before and after.
**Sample data:** `series`

| day | val |
|---|---|
| 1 | 3 |
| 2 | 5 |
| 3 | 4 |
| 4 | 6 |
| 5 | 6 |
| 6 | 2 |
| 7 | 7 |
| 8 | 3 |
**SQL:**
```sql
CREATE TABLE series (day INT, val INT);

WITH n AS (
  SELECT day, val,
         LAG(val)  OVER (ORDER BY day) AS prev_val,
         LEAD(val) OVER (ORDER BY day) AS next_val
  FROM series)
SELECT day, prev_val, val, next_val
FROM n
WHERE val > prev_val AND val > next_val
ORDER BY day;
```
**Output:** (run in sqlite)

| day | prev_val | val | next_val |
|---|---|---|---|
| 2 | 3 | 5 | 4 |
| 7 | 2 | 7 | 3 |
**pandas equivalent:**
```python
import pandas as pd
series = pd.DataFrame([
    (1, 3),
    (2, 5),
    (3, 4),
    (4, 6),
    (5, 6),
    (6, 2),
    (7, 7),
    (8, 3),
], columns=['day', 'val'])
out = series.sort_values('day').reset_index(drop=True)
out['prev_val'] = out['val'].shift(1)
out['next_val'] = out['val'].shift(-1)
out = out[(out['val'] > out['prev_val']) & (out['val'] > out['next_val'])]
out = out[['day', 'prev_val', 'val', 'next_val']].reset_index(drop=True)
print(out.to_string(index=False))
```
Output (real run, matches the SQL result):
```text
 day  prev_val  val  next_val
   2       3.0    5       4.0
   7       2.0    7       3.0
```
**Edge cases:** Plateaus: day 4 and day 5 both have value 6, so neither is strictly higher than both neighbours and neither is reported; decide whether a flat top counts. The two end rows are excluded. Troughs are the same query with < instead.
**Likely follow-ups:**
- Treat edge rows as peaks too? COALESCE the missing neighbour to a very low number.
- Peaks per group? Add PARTITION BY to both functions.
**Common mistakes:** Applying the comparison in the same SELECT as the windows, using >= by accident, and forgetting ORDER BY inside OVER().

### Q52 ⭐ 🔴 How do you calculate a running distinct count (for example, new unique customers so far), given COUNT(DISTINCT) is not allowed in window frames?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know COUNT(DISTINCT) is not allowed in a window, and can you work around it by flagging first appearances?
**Say this in the interview:** I mark each customer's first order with ROW_NUMBER, 1 for first and 0 for repeats, and then take a running SUM of that flag.
**Explain simply:**
- Most databases refuse COUNT(DISTINCT x) OVER (...).
- Workaround: ROW_NUMBER() OVER (PARTITION BY customer ORDER BY date, order_id) = 1 marks exactly one row per customer (their first).
- A running SUM of that 1/0 flag counts distinct customers so far.
- Use an explicit ROWS frame so same-day rows get their own running value.
**Example:** How many unique employees have raised a ticket so far, by date?
**Sample data:** `orders`

| order_id | order_date | customer |
|---|---|---|
| 1 | 2026-03-01 | Ravi |
| 2 | 2026-03-01 | Meera |
| 3 | 2026-03-02 | Ravi |
| 4 | 2026-03-03 | Sana |
| 5 | 2026-03-03 | Meera |
| 6 | 2026-03-04 | Ravi |
| 7 | 2026-03-04 | Tej |
**SQL:**
```sql
CREATE TABLE orders (order_id INT, order_date TEXT, customer TEXT);

WITH f AS (
  SELECT order_id, order_date, customer,
         CASE WHEN ROW_NUMBER() OVER (PARTITION BY customer ORDER BY order_date, order_id) = 1
              THEN 1 ELSE 0 END AS is_new
  FROM orders)
SELECT order_id, order_date, customer, is_new,
       SUM(is_new) OVER (ORDER BY order_date, order_id
                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS unique_customers_so_far
FROM f
ORDER BY order_date, order_id;
```
**Output:** (run in sqlite)

| order_id | order_date | customer | is_new | unique_customers_so_far |
|---|---|---|---|---|
| 1 | 2026-03-01 | Ravi | 1 | 1 |
| 2 | 2026-03-01 | Meera | 1 | 2 |
| 3 | 2026-03-02 | Ravi | 0 | 2 |
| 4 | 2026-03-03 | Sana | 1 | 3 |
| 5 | 2026-03-03 | Meera | 0 | 3 |
| 6 | 2026-03-04 | Ravi | 0 | 3 |
| 7 | 2026-03-04 | Tej | 1 | 4 |
**pandas equivalent:**
```python
import pandas as pd
orders = pd.DataFrame([
    (1, '2026-03-01', 'Ravi'),
    (2, '2026-03-01', 'Meera'),
    (3, '2026-03-02', 'Ravi'),
    (4, '2026-03-03', 'Sana'),
    (5, '2026-03-03', 'Meera'),
    (6, '2026-03-04', 'Ravi'),
    (7, '2026-03-04', 'Tej'),
], columns=['order_id', 'order_date', 'customer'])
out = orders.sort_values(['order_date', 'order_id']).reset_index(drop=True)
out['is_new'] = (~out['customer'].duplicated()).astype(int)
out['unique_customers_so_far'] = out['is_new'].cumsum()
print(out.to_string(index=False))
```
Output (real run, matches the SQL result):
```text
 order_id order_date customer  is_new  unique_customers_so_far
        1 2026-03-01     Ravi       1                        1
        2 2026-03-01    Meera       1                        2
        3 2026-03-02     Ravi       0                        2
        4 2026-03-03     Sana       1                        3
        5 2026-03-03    Meera       0                        3
        6 2026-03-04     Ravi       0                        3
        7 2026-03-04      Tej       1                        4
```
**Edge cases:** Ties on the same date need the order_id tiebreaker so 'first' is stable. To report one row per day, take the MAX of the running value per day, or aggregate the flags per day first and then run the SUM. NULL customer ids would form their own partition; filter them out.
**Likely follow-ups:**
- Does the engine support it directly? Some (e.g. DuckDB) allow approximations; standard answer is the flag method.
- Running distinct per month (resets)? Partition the ROW_NUMBER by customer and month.
**Common mistakes:** Using COUNT(DISTINCT) OVER (error or unsupported), forgetting the tiebreaker, and taking a plain COUNT(DISTINCT customer) per row without the window.

