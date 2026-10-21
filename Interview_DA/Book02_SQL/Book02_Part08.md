# Book 2 — SQL | Part 8: Scenario business queries (sales, HR, e-commerce, banking)

**Target:** 70 | **Actual:** 74 | **Scope:** Business-style SQL asked as "here are the tables, write the query" in sales, HR/payroll, e-commerce and banking. Retention/cohort/funnel/MoM growth belong to Part 9; nth highest, de-duplication, gaps-and-islands, recursive CTEs belong to Part 10.

### Q1 ⭐⭐⭐ 🟢 HR: Using `employees` (emp_id, name, dept_id) and `departments` (dept_id, dept_name), show the headcount of every department, including departments that currently have no employees.
**Asked at:** commonly asked (no company-specific report found); a sources note lists headcount-by-department as a standard HR-analytics screen task (Yardstick HR data analyst work samples).
**What the interviewer is checking:** Do you know that INNER JOIN silently drops empty departments, and that you must LEFT JOIN from the department side and COUNT a column from the employee side?
**Say this in the interview:** I start from the departments table and LEFT JOIN employees onto it, so a department with nobody in it still shows up. Then I use COUNT(e.emp_id), not COUNT(*), so an empty department shows 0 instead of 1.
**Explain simply:**
- A **JOIN** glues two tables together on a matching column (here `dept_id`). A **LEFT JOIN** keeps every row of the left table even when there is no match on the right; the right-side columns come back as NULL (an unknown/empty value).
- `COUNT(column)` counts only non-NULL values, so the NULL row from an empty department adds 0. `COUNT(*)` counts rows, so it would wrongly give 1.
- Group by the department so you get one row per department.
**Example:** Four departments, six employees. Legal has nobody, so the correct answer for Legal is 0, not a missing row.
**Sample data:**

`employees`

| emp_id | name | dept_id |
|---|---|---|
| 1 | Asha | 1 |
| 2 | Bala | 1 |
| 3 | Chitra | 2 |
| 4 | Dev | 3 |
| 5 | Esha | 3 |
| 6 | Farhan | 3 |

`departments`

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Finance |
| 3 | IT |
| 4 | Legal |

**SQL:**
```sql
-- setup (SQLite types; dates stored as 'YYYY-MM-DD' text)
CREATE TABLE employees (emp_id INTEGER, name TEXT, dept_id INTEGER);
CREATE TABLE departments (dept_id INTEGER, dept_name TEXT);

SELECT d.dept_name,
       COUNT(e.emp_id) AS headcount
FROM departments d
LEFT JOIN employees e ON e.dept_id = d.dept_id
GROUP BY d.dept_id, d.dept_name
ORDER BY headcount DESC, d.dept_name;
```
**Output:**

| dept_name | headcount |
|---|---|
| IT | 3 |
| HR | 2 |
| Finance | 1 |
| Legal | 0 |

**pandas equivalent** (gives the same result as the SQL above):
```python
m = departments.merge(employees, on="dept_id", how="left")
result = (m.groupby("dept_name", as_index=False)
            .agg(headcount=("emp_id", "count"))      # count() skips NaN, like COUNT(col)
            .sort_values(["headcount", "dept_name"], ascending=[False, True])
            .reset_index(drop=True))
```
**Edge cases:** An employee whose dept_id is NULL or points to a missing department will not appear (they belong to no department row). Duplicate employee rows would inflate the count, so check emp_id is unique. Count only active staff by adding `AND e.left_date IS NULL` in the ON clause (not WHERE; WHERE would turn the LEFT JOIN back into an inner join).
**Likely follow-ups:** Why not INNER JOIN? It drops Legal. Why ON and not WHERE for the active filter? A WHERE on the employee table removes the NULL rows and loses empty departments. RIGHT JOIN? Same result if you swap table order; most people stick to LEFT JOIN for readability.
**Common mistakes:** Using COUNT(*) (gives 1 for empty departments); filtering the right table in WHERE; grouping only by dept_name when two departments share a name.

### Q2 ⭐⭐⭐ 🟢 Sales: Using `orders`, `order_items` (order_id, product_id, qty, unit_price) and `products` (product_id, category), find total revenue per product category, highest first.
**Asked at:** commonly asked (no company-specific report found); revenue per category/customer is a recurring pattern in published SQL guides (Analytics Vidhya, Interview Query).
**What the interviewer is checking:** Can you compute revenue as quantity times price per line, join to the product table, and group at the right level?
**Say this in the interview:** Revenue per line is qty times unit_price. I join order_items to products to get the category, add the lines up per category with SUM, and sort descending.
**Explain simply:**
- Order lines carry a quantity and a price, so revenue is `qty * unit_price` for each line; you cannot just add `unit_price`.
- `GROUP BY category` collapses many lines into one row per category, and `SUM()` adds revenue inside each group.
- The `orders` table is only needed if you must filter by order status or date; for a plain total, `order_items` and `products` are enough.
**Example:** Electronics: 1x500 + 1x200 + 2x500 = 1,700. Books: 2x300 + 3x300 + 5x100 = 2,000. Toys: 4x50 = 200.
**Sample data:**

`order_items`

| order_id | product_id | qty | unit_price |
|---|---|---|---|
| 1 | 10 | 1 | 500 |
| 1 | 12 | 2 | 300 |
| 2 | 11 | 1 | 200 |
| 3 | 12 | 3 | 300 |
| 3 | 14 | 4 | 50 |
| 4 | 10 | 2 | 500 |
| 5 | 13 | 5 | 100 |

`products`

| product_id | category |
|---|---|
| 10 | Electronics |
| 11 | Electronics |
| 12 | Books |
| 13 | Books |
| 14 | Toys |

**SQL:**
```sql
-- setup (SQLite types; dates stored as 'YYYY-MM-DD' text)
CREATE TABLE order_items (order_id INTEGER, product_id INTEGER, qty INTEGER, unit_price INTEGER);
CREATE TABLE products (product_id INTEGER, category TEXT);

SELECT p.category,
       SUM(oi.qty * oi.unit_price) AS revenue
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY revenue DESC;
```
**Output:**

| category | revenue |
|---|---|
| Books | 2000 |
| Electronics | 1700 |
| Toys | 200 |

**pandas equivalent** (gives the same result as the SQL above):
```python
m = order_items.merge(products, on="product_id")
m["revenue"] = m["qty"] * m["unit_price"]
result = (m.groupby("category", as_index=False)["revenue"].sum()
            .sort_values("revenue", ascending=False).reset_index(drop=True))
```
**Edge cases:** Products with no sales do not appear (inner join); use a LEFT JOIN from products if you want them with 0. NULL qty or price makes that line's revenue NULL and SUM ignores it. Ties in revenue: add a second ORDER BY column for stable output. Cancelled orders should be excluded via a join to orders (see Q5).
**Likely follow-ups:** How do you include categories with no sales? LEFT JOIN from products and wrap in COALESCE(SUM(...),0). How do you show share of total? Divide by SUM(SUM(...)) OVER () (see Q8).
**Common mistakes:** SUM(unit_price) instead of SUM(qty*unit_price); joining orders and double counting; forgetting the category lives in products, not order_items.

### Q3 ⭐⭐⭐ 🟢 Sales: Find the top 5 customers by total amount spent, showing customer name and total spend.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you aggregate per customer, order the totals and take the top N, and do you know what happens on ties?
**Say this in the interview:** I join customers to orders, SUM the order amount per customer, sort the totals high to low and keep the first 5. If ties at the 5th place matter, I would use RANK or DENSE_RANK instead of LIMIT.
**Explain simply:**
- `GROUP BY customer` gives one row per customer; `SUM(amount)` is their total spend.
- `ORDER BY total DESC` puts the biggest spender first and `LIMIT 5` keeps only 5 rows. This is MySQL/PostgreSQL/SQLite syntax; SQL Server uses `SELECT TOP 5`, and standard SQL uses `FETCH FIRST 5 ROWS ONLY` (not run here).
- Group by customer_id and also show the name; two customers can share a name.
**Example:** Asha spent 500+700+300 = 1,500; Dev 2,000; Bala 1,500; Chitra 1,600; Farhan 1,000; Esha 250. Gita placed no orders, so she is not in the top 5.
**Sample data:**

`customers`

| customer_id | name |
|---|---|
| 1 | Asha |
| 2 | Bala |
| 3 | Chitra |
| 4 | Dev |
| 5 | Esha |
| 6 | Farhan |
| 7 | Gita |

`orders`

| order_id | customer_id | amount |
|---|---|---|
| 1 | 1 | 500 |
| 2 | 1 | 700 |
| 3 | 2 | 1500 |
| 4 | 3 | 300 |
| 5 | 3 | 400 |
| 6 | 3 | 900 |
| 7 | 4 | 2000 |
| 8 | 5 | 250 |
| 9 | 1 | 300 |
| 10 | 6 | 1000 |

**SQL:**
```sql
-- setup (SQLite types; dates stored as 'YYYY-MM-DD' text)
CREATE TABLE customers (customer_id INTEGER, name TEXT);
CREATE TABLE orders (order_id INTEGER, customer_id INTEGER, amount INTEGER);

SELECT c.name,
       SUM(o.amount) AS total_spend
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spend DESC, c.name
LIMIT 5;
```
**Output:**

| name | total_spend |
|---|---|
| Dev | 2000 |
| Chitra | 1600 |
| Asha | 1500 |
| Bala | 1500 |
| Farhan | 1000 |

**pandas equivalent** (gives the same result as the SQL above):
```python
m = customers.merge(orders, on="customer_id")
result = (m.groupby(["customer_id", "name"], as_index=False)["amount"].sum()
            .rename(columns={"amount": "total_spend"})
            .sort_values(["total_spend", "name"], ascending=[False, True])
            .head(5)[["name", "total_spend"]].reset_index(drop=True))
```
**Edge cases:** Tie for 5th place: LIMIT 5 cuts one of the tied customers arbitrarily; use DENSE_RANK() <= 5 in a CTE (common table expression, a named temporary result) to keep all ties. Cancelled orders should be filtered first. Customers with no orders are excluded; that is right for a top list.
**Likely follow-ups:** How to keep ties? RANK() OVER (ORDER BY SUM(amount) DESC) in a CTE, then filter rank <= 5. How to do top 5 per city? Use ROW_NUMBER() PARTITION BY city (see Q20).
**Common mistakes:** Grouping by name only; forgetting a tie-breaker so results change between runs; using LIMIT inside SQL Server.

### Q4 ⭐⭐⭐ 🟢 HR: List employees earning more than ₹80,000 with their department name and salary, highest salary first.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** A basic JOIN plus WHERE plus ORDER BY, and attention to the strict 'more than' (Dev at exactly 80,000 is not included).
**Say this in the interview:** I join employees to departments to get the department name, keep rows where salary is strictly above 80,000, and sort by salary descending.
**Explain simply:**
- **WHERE** filters individual rows before anything is grouped. 'More than' means `>`, so someone paid exactly 80,000 is out.
- The join pulls the readable department name from `departments` using `dept_id`.
- `ORDER BY salary DESC` puts the highest earner first.
**Example:** Of 6 employees, 3 earn above 80,000: Chitra 120,000, Esha 95,000 and Bala 82,000. Dev at exactly 80,000 is excluded.
**Sample data:**

`employees`

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 75000 |
| 2 | Bala | 2 | 82000 |
| 3 | Chitra | 3 | 120000 |
| 4 | Dev | 3 | 80000 |
| 5 | Esha | 2 | 95000 |
| 6 | Farhan | 1 | 61000 |

`departments`

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Finance |
| 3 | IT |

**SQL:**
```sql
-- setup (SQLite types; dates stored as 'YYYY-MM-DD' text)
CREATE TABLE employees (emp_id INTEGER, name TEXT, dept_id INTEGER, salary INTEGER);
CREATE TABLE departments (dept_id INTEGER, dept_name TEXT);

SELECT e.name, d.dept_name, e.salary
FROM employees e
JOIN departments d ON d.dept_id = e.dept_id
WHERE e.salary > 80000
ORDER BY e.salary DESC;
```
**Output:**

| name | dept_name | salary |
|---|---|---|
| Chitra | IT | 120000 |
| Esha | Finance | 95000 |
| Bala | Finance | 82000 |

**pandas equivalent** (gives the same result as the SQL above):
```python
m = employees.merge(departments, on="dept_id")
result = (m[m["salary"] > 80000][["name", "dept_name", "salary"]]
            .sort_values("salary", ascending=False).reset_index(drop=True))
```
**Edge cases:** Employees with NULL dept_id disappear with an INNER JOIN; use LEFT JOIN if you want them listed with a blank department. NULL salary is never > 80000 so it is excluded. Ties in salary: add a second sort key such as name.
**Likely follow-ups:** How to include people without a department? LEFT JOIN. How to show only the top earner per department? Window function or correlated subquery (Part 10 topics).
**Common mistakes:** Using >= instead of >; putting the salary filter in HAVING (HAVING is for groups); forgetting the sort direction (the default is ascending).

### Q5 ⭐⭐⭐ 🟢 E-commerce: Orders have a status (delivered, cancelled, returned, in-transit). Calculate total revenue counting only delivered orders.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you filter on a status column so that only completed sales count as revenue?
**Say this in the interview:** Revenue should only count orders that were actually delivered, so I add WHERE status = 'delivered' and SUM the amount. Cancelled, returned and in-transit orders are not realised revenue.
**Explain simply:**
- **Revenue** here means money from orders that are completed. Cancelled orders never produced money, returned ones gave it back, and in-transit ones are not final yet.
- `WHERE status = 'delivered'` throws away the other rows before `SUM` runs.
- A business may define 'revenue' differently (e.g. count in-transit as booked). Say your definition out loud; interviewers like that.
**Example:** Delivered orders: 1,200 + 450 + 950 = 2,600. All orders would give 4,300, an over-statement of 1,700.
**Sample data:**

`orders`

| order_id | customer_id | status | amount |
|---|---|---|---|
| 1 | 1 | delivered | 1200 |
| 2 | 2 | cancelled | 800 |
| 3 | 3 | delivered | 450 |
| 4 | 1 | returned | 600 |
| 5 | 4 | in-transit | 300 |
| 6 | 2 | delivered | 950 |

**SQL:**
```sql
-- setup (SQLite types; dates stored as 'YYYY-MM-DD' text)
CREATE TABLE orders (order_id INTEGER, customer_id INTEGER, status TEXT, amount INTEGER);

SELECT SUM(amount) AS delivered_revenue
FROM orders
WHERE status = 'delivered';

-- Bonus: all statuses side by side using conditional aggregation (CASE inside SUM)
SELECT SUM(CASE WHEN status = 'delivered' THEN amount ELSE 0 END) AS delivered_revenue,
       SUM(amount) AS all_orders_value
FROM orders;
```
**Output:**

| delivered_revenue |
|---|
| 2600 |

Bonus: all statuses side by side using conditional aggregation (CASE inside SUM)

| delivered_revenue | all_orders_value |
|---|---|
| 2600 | 4300 |

**pandas equivalent** (gives the same result as the SQL above):
```python
result = pd.DataFrame({"delivered_revenue": [orders.loc[orders["status"] == "delivered", "amount"].sum()]})

# Bonus: all statuses side by side using conditional aggregation (CASE inside SUM)
result = pd.DataFrame({"delivered_revenue": [orders.loc[orders["status"] == "delivered", "amount"].sum()],
                       "all_orders_value": [orders["amount"].sum()]})
```
**Edge cases:** If no order is delivered, SUM returns NULL, not 0; wrap in COALESCE(SUM(amount), 0). Status spelling can vary ('Delivered ', 'DELIVERED'), so clean with LOWER(TRIM(status)). String comparison is case-sensitive in PostgreSQL but usually not in MySQL/SQL Server (from memory, not run here).
**Likely follow-ups:** What about returns after delivery? Subtract refunds from the returns table or treat 'returned' as negative. How to show revenue per status? GROUP BY status.
**Common mistakes:** Summing everything and filtering later; typing 'Delivered' vs 'delivered' wrongly; forgetting COALESCE for the empty case.

### Q6 ⭐⭐⭐ 🟢 Sales: Show the number of orders and total sales value per day for the last 7 days.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you do a date-range filter plus GROUP BY a date, and do you know that days with no orders will not appear unless you build a calendar?
**Say this in the interview:** I keep orders from the last 7 days including today, group them by date and show COUNT of orders and SUM of amount. A day with zero orders will not show up unless I join to a calendar.
**Explain simply:**
- 'Last 7 days' needs a clear rule: I take today and the 6 days before it, so 7 calendar days in total. For this answer 'today' is fixed at 2026-10-21 so the result repeats; in real use replace it with `date('now')` (SQLite), `CURRENT_DATE` (PostgreSQL/MySQL) or `CAST(GETDATE() AS date)` (SQL Server, not run here).
- If order_date also stores a time, wrap it with `date(order_date)` so all orders of a day group together.
- `COUNT(*)` counts orders; `SUM(amount)` totals the money.
**Example:** Orders on 14 Oct fall outside the window. 17 and 19 Oct have no orders, so they are missing from the result.
**Sample data:**

`orders`

| order_id | order_date | amount |
|---|---|---|
| 1 | 2026-10-14 | 400 |
| 2 | 2026-10-15 | 250 |
| 3 | 2026-10-15 | 350 |
| 4 | 2026-10-16 | 900 |
| 5 | 2026-10-18 | 150 |
| 6 | 2026-10-18 | 200 |
| 7 | 2026-10-18 | 300 |
| 8 | 2026-10-20 | 700 |
| 9 | 2026-10-21 | 250 |
| 10 | 2026-10-21 | 350 |

**SQL:**
```sql
-- setup (SQLite types; dates stored as 'YYYY-MM-DD' text)
CREATE TABLE orders (order_id INTEGER, order_date TEXT, amount INTEGER);

SELECT date(order_date) AS order_day,
       COUNT(*)           AS orders,
       SUM(amount)        AS total_sales
FROM orders
WHERE date(order_date) BETWEEN date('2026-10-21', '-6 days') AND '2026-10-21'
GROUP BY date(order_date)
ORDER BY order_day;
```
**Output:**

| order_day | orders | total_sales |
|---|---|---|
| 2026-10-15 | 2 | 600 |
| 2026-10-16 | 1 | 900 |
| 2026-10-18 | 3 | 650 |
| 2026-10-20 | 1 | 700 |
| 2026-10-21 | 2 | 600 |

**pandas equivalent** (gives the same result as the SQL above):
```python
today = pd.Timestamp("2026-10-21")   # same fixed date as the SQL
o = orders.copy()
o["order_date"] = pd.to_datetime(o["order_date"])
w = o[(o["order_date"] >= today - pd.Timedelta(days=6)) & (o["order_date"] <= today)]
result = (w.groupby("order_date").agg(orders=("order_id", "count"), total_sales=("amount", "sum"))
            .reset_index().rename(columns={"order_date": "order_day"}))
result["order_day"] = result["order_day"].dt.strftime("%Y-%m-%d")
```
**Edge cases:** Missing days: build a 7-row calendar with a recursive CTE and LEFT JOIN orders to show 0 (same idea as Q7). A timestamp like '2026-10-21 18:30' fails `<= '2026-10-21'` if you forget date(); that silently drops today's orders. Cancelled orders may need excluding.
**Likely follow-ups:** How to show zero days? Calendar table + LEFT JOIN + COALESCE. What if 'last 7 days' must exclude today? Use BETWEEN today-7 and today-1.
**Common mistakes:** Using order_date > today - 7 (gives 6 days); comparing timestamps to a bare date; hardcoding a date in production code.

### Q7 ⭐⭐⭐ 🟡 Sales: Show total revenue for each calendar month of 2025 (month name and amount), including months with zero sales.
**Asked at:** commonly asked (no company-specific report found); month-wise revenue appears in Analytics Vidhya's SQL query list (a guide, not an interview report).
**What the interviewer is checking:** Can you generate a list of all 12 months yourself and LEFT JOIN the data to it so empty months show 0, while keeping the year filter in the right place?
**Say this in the interview:** A plain GROUP BY month only returns months that have orders. So I write down all 12 months, LEFT JOIN the 2025 orders onto them, and use COALESCE to turn missing totals into 0.
**Explain simply:**
- Months with no sales have no rows, so GROUP BY cannot invent them. You need a **calendar** (a list of months) as the left table.
- `strftime('%m', order_date)` pulls the month number in SQLite; PostgreSQL uses `EXTRACT(MONTH FROM order_date)`, MySQL `MONTH(order_date)`, SQL Server `MONTH(order_date)` (not run here).
- Put the year filter inside the `ON` clause. If you put it in `WHERE`, the empty months are thrown out again and the LEFT JOIN is wasted.
- `COALESCE(x, 0)` replaces NULL by 0.
**Example:** Jan 2025 = 1,000 + 500 = 1,500; Feb 1,200; Mar 0; Apr 1,500; Sep 650. The 2024 and 2026 orders must not leak in.
**Sample data:**

`orders`

| order_id | order_date | amount |
|---|---|---|
| 1 | 2024-12-20 | 999 |
| 2 | 2025-01-10 | 1000 |
| 3 | 2025-01-25 | 500 |
| 4 | 2025-02-14 | 1200 |
| 5 | 2025-04-02 | 800 |
| 6 | 2025-04-30 | 700 |
| 7 | 2025-09-09 | 650 |
| 8 | 2026-01-03 | 5000 |

**SQL:**
```sql
-- setup (SQLite types; dates stored as 'YYYY-MM-DD' text)
CREATE TABLE orders (order_id INTEGER, order_date TEXT, amount INTEGER);

WITH months(m, month_name) AS (
  VALUES (1,'Jan'),(2,'Feb'),(3,'Mar'),(4,'Apr'),(5,'May'),(6,'Jun'),
         (7,'Jul'),(8,'Aug'),(9,'Sep'),(10,'Oct'),(11,'Nov'),(12,'Dec')
)
SELECT mo.month_name,
       COALESCE(SUM(o.amount), 0) AS revenue
FROM months mo
LEFT JOIN orders o
       ON CAST(strftime('%m', o.order_date) AS INTEGER) = mo.m
      AND strftime('%Y', o.order_date) = '2025'
GROUP BY mo.m, mo.month_name
ORDER BY mo.m;
```
**Output:**

| month_name | revenue |
|---|---|
| Jan | 1500 |
| Feb | 1200 |
| Mar | 0 |
| Apr | 1500 |
| May | 0 |
| Jun | 0 |
| Jul | 0 |
| Aug | 0 |
| Sep | 650 |
| Oct | 0 |
| Nov | 0 |
| Dec | 0 |

**pandas equivalent** (gives the same result as the SQL above):
```python
o = orders.copy()
o["order_date"] = pd.to_datetime(o["order_date"])
o = o[o["order_date"].dt.year == 2025]
by_m = o.groupby(o["order_date"].dt.month)["amount"].sum()
names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
result = pd.DataFrame({"month_name": names,
                       "revenue": [by_m.get(i, 0) for i in range(1, 13)]})
```
**Edge cases:** Year in the ON clause, not WHERE. Orders with NULL date are ignored. If the table has several years, forgetting the year filter merges Jan 2025 with Jan 2024. Sorting by month_name alphabetically gives Apr, Aug, Dec; sort by the month number instead.
**Likely follow-ups:** How to do this for the last 12 rolling months? Generate dates with a recursive CTE. Month-on-month growth? That is Part 9 (LAG).
**Common mistakes:** WHERE year = 2025 after the LEFT JOIN; ordering by month name; no COALESCE so empty months show NULL.

### Q8 ⭐⭐⭐ 🟡 HR/payroll: Show each department's total monthly payroll and its percentage share of the company payroll.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you combine GROUP BY with a window function to get a percent-of-total in one query?
**Say this in the interview:** I SUM salary per department, then divide it by the company total. The company total comes from SUM(SUM(salary)) OVER (), a window function that adds up all the group totals without collapsing rows.
**Explain simply:**
- **Payroll** is the total salary bill. Per department it is a plain `SUM(monthly_salary)`.
- A **window function** does a calculation across rows without collapsing them. `OVER ()` with empty brackets means 'across the whole result'.
- `SUM(SUM(x)) OVER ()` reads as: first sum per department (inner SUM), then add those department totals together (outer window SUM).
- Multiply by 100.0 (with a decimal point) so integer division does not round everything to 0.
**Example:** Total payroll = 450,000. HR 110,000 is 24.4%, Finance 90,000 is 20%, IT 250,000 is 55.6%. Shares add up to 100%.
**Sample data:**

`employees`

| emp_id | name | dept_id | monthly_salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 90000 |
| 4 | Dev | 3 | 70000 |
| 5 | Esha | 3 | 80000 |
| 6 | Farhan | 3 | 100000 |

`departments`

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Finance |
| 3 | IT |

**SQL:**
```sql
-- setup (SQLite types; dates stored as 'YYYY-MM-DD' text)
CREATE TABLE employees (emp_id INTEGER, name TEXT, dept_id INTEGER, monthly_salary INTEGER);
CREATE TABLE departments (dept_id INTEGER, dept_name TEXT);

SELECT d.dept_name,
       SUM(e.monthly_salary) AS payroll,
       ROUND(100.0 * SUM(e.monthly_salary) / SUM(SUM(e.monthly_salary)) OVER (), 1) AS pct_share
FROM employees e
JOIN departments d ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name
ORDER BY payroll DESC;
```
**Output:**

| dept_name | payroll | pct_share |
|---|---|---|
| IT | 250000 | 55.6 |
| HR | 110000 | 24.4 |
| Finance | 90000 | 20 |

**pandas equivalent** (gives the same result as the SQL above):
```python
m = employees.merge(departments, on="dept_id")
g = m.groupby("dept_name", as_index=False).agg(payroll=("monthly_salary", "sum"))
g["pct_share"] = (100.0 * g["payroll"] / g["payroll"].sum()).round(1)
result = g.sort_values("payroll", ascending=False).reset_index(drop=True)
```
**Edge cases:** Include only active employees (add `WHERE left_date IS NULL`) or the share is wrong. NULL salaries are skipped by SUM. Rounded shares may add to 99.9 or 100.1. An alternative to the window is a scalar subquery `/ (SELECT SUM(monthly_salary) FROM employees)`, which gives the same number.
**Likely follow-ups:** Why not divide by COUNT? Share means part of the total, so total payroll is the denominator. What if payroll is per month? Add the month to GROUP BY and PARTITION BY month in the window.
**Common mistakes:** Integer division (100 * a / b with whole numbers); dividing by the wrong total (a per-department total); including ex-employees.

### Q9 ⭐⭐⭐ 🟡 Banking: `transactions` has account_id, txn_type ('deposit' or 'withdrawal') and amount. Calculate the current balance of each account.
**Asked at:** commonly asked (no company-specific report found); final-balance-from-deposits-and-withdrawals appears in user-uploaded bank question lists (unverified).
**What the interviewer is checking:** Can you turn two transaction types into a signed total using CASE inside SUM?
**Say this in the interview:** Deposits add money and withdrawals take it away. So I give deposits a plus sign and withdrawals a minus sign with CASE WHEN, then SUM per account. That is the current balance.
**Explain simply:**
- **CASE WHEN** is SQL's if/else: it returns one value per row depending on a condition.
- Each row becomes +amount or -amount, and `SUM` per `account_id` nets them off.
- This is a ledger-style balance: balance = all deposits minus all withdrawals ever made (add an opening balance if one exists).
**Example:** Account 101: 5,000 + 2,000 - 1,500 = 5,500. Account 104 only withdrew 200, so its balance is -200 (an overdraft or a data problem worth flagging).
**Sample data:**

`transactions`

| txn_id | account_id | txn_type | amount |
|---|---|---|---|
| 1 | 101 | deposit | 5000 |
| 2 | 101 | deposit | 2000 |
| 3 | 101 | withdrawal | 1500 |
| 4 | 102 | deposit | 10000 |
| 5 | 102 | withdrawal | 4000 |
| 6 | 103 | deposit | 3000 |
| 7 | 103 | withdrawal | 3500 |
| 8 | 104 | withdrawal | 200 |

**SQL:**
```sql
-- setup (SQLite types; dates stored as 'YYYY-MM-DD' text)
CREATE TABLE transactions (txn_id INTEGER, account_id INTEGER, txn_type TEXT, amount INTEGER);

SELECT account_id,
       SUM(CASE WHEN txn_type = 'deposit' THEN amount ELSE -amount END) AS balance
FROM transactions
GROUP BY account_id
ORDER BY account_id;
```
**Output:**

| account_id | balance |
|---|---|
| 101 | 5500 |
| 102 | 6000 |
| 103 | -500 |
| 104 | -200 |

**pandas equivalent** (gives the same result as the SQL above):
```python
t = transactions.copy()
t["signed"] = t["amount"].where(t["txn_type"] == "deposit", -t["amount"])
result = t.groupby("account_id", as_index=False).agg(balance=("signed", "sum"))
```
**Edge cases:** ELSE -amount treats any unknown txn_type as a withdrawal; use two explicit WHEN branches and `ELSE 0` to be safe. Accounts with no transactions are missing; LEFT JOIN from the accounts table and COALESCE to 0. NULL amount is skipped by SUM. Negative balance may mean bad data.
**Likely follow-ups:** How to show a running balance? SUM(...) OVER (PARTITION BY account_id ORDER BY txn_date). How to include accounts with no activity? LEFT JOIN from accounts.
**Common mistakes:** Subtracting totals in the wrong direction; forgetting the minus sign; mixing the opening balance in twice.

### Q10 ⭐⭐⭐ 🟡 HR: Using `employees` (join_date, left_date, dept_id), calculate the attrition rate per department for 2025 (leavers divided by average headcount), and explain your denominator.
**Asked at:** commonly asked (no company-specific report found); attrition by department is listed as an HR-analytics SQL task in a Yardstick work-sample guide and a ClickHouse people-analytics tutorial (read as snippets only).
**What the interviewer is checking:** Do you understand that attrition is a rate (leavers divided by average headcount), and can you count opening and closing headcount from join and leave dates?
**Say this in the interview:** Attrition rate is leavers in the year divided by average headcount. I take average headcount as (opening headcount on 1 Jan + closing headcount on 31 Dec) divided by 2, count leavers by left_date in 2025, and guard the division with NULLIF.
**Explain simply:**
- **Attrition rate** = people who left / average number of people employed, as a percent. Using average headcount (not year-end) avoids overstating the rate in a shrinking team or understating it in a growing one.
- **Opening headcount**: joined before 1 Jan 2025 and had not left before 1 Jan 2025. **Closing headcount**: joined by 31 Dec 2025 and had not left by then. A person with a NULL left_date is still employed.
- Convention used: left_date is the last working day, so someone leaving on 31 Dec 2025 is counted as a leaver and not in closing headcount (they have left once the year ends).
- Two-point averaging is the simple method; a 12-month average of month-end headcounts is more accurate (see Q18). Say which one you used.
- `NULLIF(x, 0)` turns a zero denominator into NULL so the division returns NULL instead of an error.
**Example:** Sales (small team): opening 4, closing 2, leavers 3. Average headcount = (4+2)/2 = 3, attrition = 3/3 = 100%. IT: opening 5, closing 4, leavers 2, average 4.5, attrition 2/4.5 = 44.4%. A tiny team makes the rate swing wildly; say so.
**Sample data:**

`employees`

| emp_id | dept_id | join_date | left_date |
|---|---|---|---|
| 1 | 1 | 2020-03-01 | NULL |
| 2 | 1 | 2021-06-15 | 2025-05-31 |
| 3 | 1 | 2022-01-10 | 2025-11-30 |
| 4 | 1 | 2023-02-01 | NULL |
| 5 | 1 | 2025-03-01 | 2025-09-30 |
| 6 | 1 | 2019-07-01 | 2024-10-31 |
| 7 | 2 | 2020-01-05 | NULL |
| 8 | 2 | 2021-09-01 | NULL |
| 9 | 2 | 2018-05-01 | 2025-02-28 |
| 10 | 2 | 2019-08-12 | 2025-08-31 |
| 11 | 2 | 2022-04-01 | NULL |
| 12 | 2 | 2025-02-01 | NULL |

`departments`

| dept_id | dept_name |
|---|---|
| 1 | Sales |
| 2 | IT |

**SQL:**
```sql
-- setup (SQLite types; dates stored as 'YYYY-MM-DD' text)
CREATE TABLE employees (emp_id INTEGER, dept_id INTEGER, join_date TEXT, left_date TEXT);
CREATE TABLE departments (dept_id INTEGER, dept_name TEXT);

WITH hc AS (
  SELECT dept_id,
    SUM(CASE WHEN join_date < '2025-01-01'
              AND (left_date IS NULL OR left_date >= '2025-01-01') THEN 1 ELSE 0 END) AS opening,
    SUM(CASE WHEN join_date <= '2025-12-31'
              AND (left_date IS NULL OR left_date >  '2025-12-31') THEN 1 ELSE 0 END) AS closing,
    SUM(CASE WHEN left_date BETWEEN '2025-01-01' AND '2025-12-31' THEN 1 ELSE 0 END) AS leavers
  FROM employees
  GROUP BY dept_id
)
SELECT d.dept_name, hc.opening, hc.closing, hc.leavers,
       (hc.opening + hc.closing) / 2.0 AS avg_headcount,
       ROUND(100.0 * hc.leavers / NULLIF((hc.opening + hc.closing) / 2.0, 0), 1) AS attrition_pct
FROM hc
JOIN departments d ON d.dept_id = hc.dept_id
ORDER BY d.dept_name;
```
**Output:**

| dept_name | opening | closing | leavers | avg_headcount | attrition_pct |
|---|---|---|---|---|---|
| IT | 5 | 4 | 2 | 4.5 | 44.4 |
| Sales | 4 | 2 | 3 | 3 | 100 |

**pandas equivalent** (gives the same result as the SQL above):
```python
e = employees.copy()
e["join_date"] = pd.to_datetime(e["join_date"]); e["left_date"] = pd.to_datetime(e["left_date"])
y0, y1 = pd.Timestamp("2025-01-01"), pd.Timestamp("2025-12-31")
e["opening"] = (e["join_date"] < y0) & (e["left_date"].isna() | (e["left_date"] >= y0))
e["closing"] = (e["join_date"] <= y1) & (e["left_date"].isna() | (e["left_date"] > y1))
e["leaver"] = e["left_date"].between(y0, y1)
g = e.groupby("dept_id", as_index=False).agg(opening=("opening", "sum"), closing=("closing", "sum"), leavers=("leaver", "sum"))
g = g.merge(departments, on="dept_id")
g["avg_headcount"] = (g["opening"] + g["closing"]) / 2
g["attrition_pct"] = (100.0 * g["leavers"] / g["avg_headcount"]).round(1)
result = g.sort_values("dept_name")[["dept_name", "opening", "closing", "leavers", "avg_headcount", "attrition_pct"]].reset_index(drop=True)
```
**Edge cases:** A person who joins and leaves inside 2025 is a leaver but is in neither opening nor closing, so the rate can look high for small teams; mention this. People who left in 2024 must not be in opening (handled by `left_date >= 2025-01-01`). Zero average headcount gives NULL, not an error. Voluntary vs involuntary split is Q37.
**Likely follow-ups:** Why average headcount? Leavers over year-end headcount ignores how big the team was during the year. Why not the opening headcount only? It ignores growth during the year. Monthly attrition? Do the same per month (Q18).
**Common mistakes:** Dividing by closing headcount only; counting people with NULL left_date as leavers; dividing integers so the rate becomes 0; forgetting people who left on exactly the boundary date.

### Q11 ⭐⭐⭐ 🟡 HR: Calculate each current employee's tenure in years from join_date, the average tenure per department, and list employees with more than 5 years of service.
**Asked at:** commonly asked (no company-specific report found); average tenure by department is a listed HR-analytics task (Yardstick work-sample guide).
**What the interviewer is checking:** Can you do date arithmetic, a per-group average next to row-level detail (window AVG), and filter on a computed column?
**Say this in the interview:** Tenure is today minus join date, divided by 365.25 to get years. For current employees only, I show each person's tenure along with their department's average using AVG OVER PARTITION BY, then a second query keeps those above 5 years.
**Explain simply:**
- **Tenure** = how long someone has been employed. Date subtraction gives days; divide by 365.25 (the extra .25 covers leap years) to get years.
- **Current employee** = `left_date IS NULL`. Gita left in 2020, so she is excluded.
- `AVG(...) OVER (PARTITION BY dept_id)` puts the department average beside every employee row without collapsing the rows.
- You cannot use a column alias in WHERE in the same SELECT, so the >5 filter repeats the expression or uses a CTE/subquery.
- 'Today' is fixed at 2026-10-21 here so the numbers are repeatable. In production use `date('now')` (SQLite), `CURRENT_DATE` (PostgreSQL/MySQL), `GETDATE()` (SQL Server). Other dialects (from memory, not run here): PostgreSQL `AGE(CURRENT_DATE, join_date)`, MySQL `TIMESTAMPDIFF(YEAR, join_date, CURDATE())`, SQL Server `DATEDIFF(day, join_date, GETDATE())/365.25` (plain `DATEDIFF(year,...)` counts calendar boundaries, so it over-counts).
**Example:** Asha joined 1 Apr 2015, about 11.6 years of service. Farhan joined in Jan 2026, so about 0.8 years. Gita left in 2020 and is excluded.
**Sample data:**

`employees`

| emp_id | name | dept_id | join_date | left_date |
|---|---|---|---|---|
| 1 | Asha | 1 | 2015-04-01 | NULL |
| 2 | Bala | 1 | 2020-10-01 | NULL |
| 3 | Chitra | 1 | 2025-06-01 | NULL |
| 4 | Dev | 2 | 2018-01-15 | NULL |
| 5 | Esha | 2 | 2021-03-01 | NULL |
| 6 | Farhan | 2 | 2026-01-10 | NULL |
| 7 | Gita | 2 | 2012-08-20 | 2020-12-31 |

`departments`

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | IT |

**SQL:**
```sql
-- setup (SQLite types; dates stored as 'YYYY-MM-DD' text)
CREATE TABLE employees (emp_id INTEGER, name TEXT, dept_id INTEGER, join_date TEXT, left_date TEXT);
CREATE TABLE departments (dept_id INTEGER, dept_name TEXT);

-- Each current employee with tenure and department average
SELECT e.name, d.dept_name,
       ROUND((julianday('2026-10-21') - julianday(e.join_date)) / 365.25, 1) AS tenure_years,
       ROUND(AVG((julianday('2026-10-21') - julianday(e.join_date)) / 365.25)
             OVER (PARTITION BY e.dept_id), 1) AS dept_avg_tenure
FROM employees e
JOIN departments d ON d.dept_id = e.dept_id
WHERE e.left_date IS NULL
ORDER BY d.dept_name, tenure_years DESC;

-- Employees with more than 5 years of service
SELECT e.name, d.dept_name,
       ROUND((julianday('2026-10-21') - julianday(e.join_date)) / 365.25, 1) AS tenure_years
FROM employees e
JOIN departments d ON d.dept_id = e.dept_id
WHERE e.left_date IS NULL
  AND (julianday('2026-10-21') - julianday(e.join_date)) / 365.25 > 5
ORDER BY tenure_years DESC;
```
**Output:**

Each current employee with tenure and department average

| name | dept_name | tenure_years | dept_avg_tenure |
|---|---|---|---|
| Asha | HR | 11.6 | 6.3 |
| Bala | HR | 6.1 | 6.3 |
| Chitra | HR | 1.4 | 6.3 |
| Dev | IT | 8.8 | 5.1 |
| Esha | IT | 5.6 | 5.1 |
| Farhan | IT | 0.8 | 5.1 |

Employees with more than 5 years of service

| name | dept_name | tenure_years |
|---|---|---|
| Asha | HR | 11.6 |
| Dev | IT | 8.8 |
| Bala | HR | 6.1 |
| Esha | IT | 5.6 |

**pandas equivalent** (gives the same result as the SQL above):
```python
today = pd.Timestamp("2026-10-21")   # same fixed date as the SQL
# Each current employee with tenure and department average
e = employees[employees["left_date"].isna()].merge(departments, on="dept_id").copy()
e["tenure_years"] = (today - pd.to_datetime(e["join_date"])).dt.days / 365.25
e["dept_avg_tenure"] = e.groupby("dept_id")["tenure_years"].transform("mean").round(1)
e["tenure_years"] = e["tenure_years"].round(1)
result = e.sort_values(["dept_name", "tenure_years"], ascending=[True, False])[["name", "dept_name", "tenure_years", "dept_avg_tenure"]].reset_index(drop=True)

# Employees with more than 5 years of service
e = employees[employees["left_date"].isna()].merge(departments, on="dept_id").copy()
e["tenure_years"] = ((today - pd.to_datetime(e["join_date"])).dt.days / 365.25)
e = e[e["tenure_years"] > 5].copy()
e["tenure_years"] = e["tenure_years"].round(1)
result = e.sort_values("tenure_years", ascending=False)[["name", "dept_name", "tenure_years"]].reset_index(drop=True)
```
**Edge cases:** Include ex-employees in the average? Usually no for 'current'; for leavers use left_date instead of today. NULL join_date gives NULL tenure and is skipped by AVG. Future-dated join_date gives negative tenure, a data-quality flag. Rounded tenure of exactly 5.0 can look like 'not above 5'; filter on the unrounded value (done above).
**Likely follow-ups:** How to get average tenure of leavers? Use left_date minus join_date for people who left. How to bucket tenure (0-1, 1-3, 3-5, 5+)? CASE WHEN on the years value.
**Common mistakes:** Using DATEDIFF(year) boundaries; dividing by 365 vs 365.25 (small, but be consistent); including leavers; filtering on the alias in WHERE.

### Q12 ⭐⭐⭐ 🟡 E-commerce: Find customers who placed more than 3 orders in the last 90 days.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you filter to a time window first, then GROUP BY customer and use HAVING for the 'more than 3' condition?
**Say this in the interview:** I filter the orders to the last 90 days, group by customer, count the orders per customer and use HAVING COUNT(*) > 3, because the condition is on a group result.
**Explain simply:**
- **WHERE** filters rows before grouping; **HAVING** filters the groups after counting. 'More than 3 orders' is about a count, so it goes in HAVING.
- 'Last 90 days' means from today minus 90 days up to today. 'Today' is fixed at 2026-10-21 here (SQLite `date('2026-10-21','-90 days')`); real code would use `date('now','-90 days')`, `CURRENT_DATE - INTERVAL '90 days'` (PostgreSQL), `DATE_SUB(CURDATE(), INTERVAL 90 DAY)` (MySQL) or `DATEADD(day,-90,GETDATE())` (SQL Server) (not run here).
- 'More than 3' is strictly greater, so exactly 3 orders does not qualify.
**Example:** Customer 101 has 4 orders in the window (qualifies). 102 has exactly 3 (does not). 103 has 5 orders, but only 3 are within 90 days (does not). So only 101 is returned.
**Sample data:**

`orders`

| order_id | customer_id | order_date |
|---|---|---|
| 1 | 101 | 2026-10-01 |
| 2 | 101 | 2026-09-15 |
| 3 | 101 | 2026-08-20 |
| 4 | 101 | 2026-07-30 |
| 5 | 102 | 2026-10-05 |
| 6 | 102 | 2026-09-01 |
| 7 | 102 | 2026-08-01 |
| 8 | 103 | 2026-10-10 |
| 9 | 103 | 2026-09-20 |
| 10 | 103 | 2026-08-15 |
| 11 | 103 | 2026-06-30 |
| 12 | 103 | 2026-05-15 |
| 13 | 104 | 2026-10-18 |

**SQL:**
```sql
-- setup (SQLite types; dates stored as 'YYYY-MM-DD' text)
CREATE TABLE orders (order_id INTEGER, customer_id INTEGER, order_date TEXT);

SELECT customer_id,
       COUNT(*) AS orders_last_90d
FROM orders
WHERE order_date >= date('2026-10-21', '-90 days')
  AND order_date <= '2026-10-21'
GROUP BY customer_id
HAVING COUNT(*) > 3
ORDER BY orders_last_90d DESC, customer_id;
```
**Output:**

| customer_id | orders_last_90d |
|---|---|
| 101 | 4 |

**pandas equivalent** (gives the same result as the SQL above):
```python
today = pd.Timestamp("2026-10-21")   # same fixed date as the SQL
o = orders.copy()
o["order_date"] = pd.to_datetime(o["order_date"])
w = o[(o["order_date"] >= today - pd.Timedelta(days=90)) & (o["order_date"] <= today)]
g = w.groupby("customer_id", as_index=False).agg(orders_last_90d=("order_id", "count"))
result = g[g["orders_last_90d"] > 3].sort_values(["orders_last_90d", "customer_id"], ascending=[False, True]).reset_index(drop=True)
```
**Edge cases:** Cancelled orders: decide whether they count and filter by status if not. Duplicate order rows (e.g. one row per item) inflate the count; use COUNT(DISTINCT order_id) if you join to order_items. Customers with zero recent orders simply do not appear. Whether day 90 is included depends on the rule; state it.
**Likely follow-ups:** How to include customer names? JOIN customers. How to count distinct orders if there are item lines? COUNT(DISTINCT order_id).
**Common mistakes:** Putting COUNT(*) > 3 in WHERE (error); using >= 3; counting order lines instead of orders; not filtering by date first.

### Q13 ⭐⭐⭐ 🟡 HR: `attendance` has emp_id, work_date and status (present/absent/leave). Find employees whose attendance in March 2026 was below 75% of working days.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you define the denominator (working days) clearly and compute a percentage with conditional counting and HAVING?
**Say this in the interview:** Attendance percent is present days divided by working days. I count working days as the distinct dates in March 2026 in the table, count present days per employee with CASE WHEN, and keep employees whose percent is below 75 using HAVING.
**Explain simply:**
- Denominator first: **working days** = days the office was open. If your table only has working days, count distinct `work_date` values in the month (a Saturday-Sunday would not appear). Here I use 8 working days to keep it small; real March would have about 22.
- Numerator: days with `status = 'present'`. I treat `leave` as not present. If your HR policy counts approved leave as attended, add it to the numerator; say that assumption aloud.
- `SUM(CASE WHEN status='present' THEN 1 ELSE 0 END)` counts present days per employee.
- Use `< 0.75` (strictly below). An employee at exactly 75% is not below it.
**Example:** Employee 2: 5 present of 8 = 62.5% (flagged). Employee 3: 6 of 8 = 75% exactly (not flagged). Employee 4: 4 of 8 = 50% (flagged). Employee 1: 100%.
**Sample data:**

`attendance`

| emp_id | work_date | status |
|---|---|---|
| 1 | 2026-03-02 | present |
| 1 | 2026-03-03 | present |
| 1 | 2026-03-04 | present |
| 1 | 2026-03-05 | present |
| 1 | 2026-03-06 | present |
| 1 | 2026-03-09 | present |
| 1 | 2026-03-10 | present |
| 1 | 2026-03-11 | present |
| 2 | 2026-03-02 | present |
| 2 | 2026-03-03 | present |
| 2 | 2026-03-04 | present |
| 2 | 2026-03-05 | present |
| 2 | 2026-03-06 | present |
| 2 | 2026-03-09 | absent |
| 2 | 2026-03-10 | leave |
| 2 | 2026-03-11 | absent |
| 3 | 2026-03-02 | present |
| 3 | 2026-03-03 | present |
| 3 | 2026-03-04 | present |
| 3 | 2026-03-05 | present |
| 3 | 2026-03-06 | present |
| 3 | 2026-03-09 | present |
| 3 | 2026-03-10 | absent |
| 3 | 2026-03-11 | leave |
| 4 | 2026-03-02 | present |
| 4 | 2026-03-03 | present |
| 4 | 2026-03-04 | present |
| 4 | 2026-03-05 | present |
| 4 | 2026-03-06 | absent |
| 4 | 2026-03-09 | absent |
| 4 | 2026-03-10 | leave |
| 4 | 2026-03-11 | absent |

**SQL:**
```sql
-- setup (SQLite types; dates stored as 'YYYY-MM-DD' text)
CREATE TABLE attendance (emp_id INTEGER, work_date TEXT, status TEXT);

WITH march AS (
  SELECT * FROM attendance
  WHERE work_date >= '2026-03-01' AND work_date < '2026-04-01'
),
wd AS (SELECT COUNT(DISTINCT work_date) AS working_days FROM march)
SELECT m.emp_id,
       SUM(CASE WHEN m.status = 'present' THEN 1 ELSE 0 END) AS present_days,
       wd.working_days,
       ROUND(100.0 * SUM(CASE WHEN m.status = 'present' THEN 1 ELSE 0 END) / wd.working_days, 1) AS attendance_pct
FROM march m
CROSS JOIN wd
GROUP BY m.emp_id, wd.working_days
HAVING 1.0 * SUM(CASE WHEN m.status = 'present' THEN 1 ELSE 0 END) / wd.working_days < 0.75
ORDER BY m.emp_id;
```
**Output:**

| emp_id | present_days | working_days | attendance_pct |
|---|---|---|---|
| 2 | 5 | 8 | 62.5 |
| 4 | 4 | 8 | 50 |

**pandas equivalent** (gives the same result as the SQL above):
```python
a = attendance[(attendance["work_date"] >= "2026-03-01") & (attendance["work_date"] < "2026-04-01")]
wd = a["work_date"].nunique()
g = a.groupby("emp_id", as_index=False).agg(present_days=("status", lambda s: (s == "present").sum()))
g["working_days"] = wd
g["attendance_pct"] = (100.0 * g["present_days"] / wd).round(1)
result = g[g["present_days"] / wd < 0.75].sort_values("emp_id").reset_index(drop=True)
```
**Edge cases:** An employee with no rows at all in March (never marked) will not appear; start from the employees table with a LEFT JOIN to catch them. Duplicate attendance rows on one date inflate present_days; dedupe. Using each employee's own row count as the denominator hides missing days; the company calendar is safer. Public holidays and weekends must not be in the denominator.
**Likely follow-ups:** How to count approved leave as attended? Use `status IN ('present','leave')`. How to do this for every month? Add a month column to GROUP BY.
**Common mistakes:** Dividing by the number of calendar days (31); using the employee's own row count as denominator; integer division so every percent becomes 0; using <= 0.75.

### Q14 ⭐⭐⭐ 🟡 E-commerce: Find customers who bought both 'Laptop' and 'Mouse' (in any orders).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you find customers who match BOTH conditions across different rows, using GROUP BY, HAVING COUNT(DISTINCT) (or INTERSECT)?
**Say this in the interview:** I join customers to what they bought, keep only Laptop and Mouse rows, group by customer, and keep customers with 2 distinct products. That means they bought both, even in different orders.
**Explain simply:**
- A plain `WHERE product = 'Laptop' AND product = 'Mouse'` returns nothing, because one row has only one product.
- So I first keep rows for either product (`IN ('Laptop','Mouse')`), then count how many different products each customer has: `HAVING COUNT(DISTINCT product_name) = 2`.
- `DISTINCT` matters: a customer buying two Laptops would otherwise count 2 without ever buying a Mouse.
- Alternative: `SELECT ... WHERE product='Laptop' INTERSECT SELECT ... WHERE product='Mouse'`; INTERSECT keeps only customers present in both lists (works in SQLite, PostgreSQL, SQL Server; MySQL 8.0.31+; from memory, not run here).
**Example:** Asha bought a Laptop in order 1 and a Mouse in order 2 (qualifies). Bala bought both in the same order 3 (qualifies). Chitra bought only a Laptop, Dev only a Mouse and Esha only a Keyboard, so none of them qualify.
**Sample data:**

`customers`

| customer_id | name |
|---|---|
| 1 | Asha |
| 2 | Bala |
| 3 | Chitra |
| 4 | Dev |
| 5 | Esha |

`orders`

| order_id | customer_id |
|---|---|
| 1 | 1 |
| 2 | 1 |
| 3 | 2 |
| 4 | 3 |
| 5 | 4 |
| 6 | 5 |

`order_items`

| order_id | product_id |
|---|---|
| 1 | 10 |
| 2 | 11 |
| 3 | 10 |
| 3 | 11 |
| 4 | 10 |
| 5 | 11 |
| 6 | 12 |

`products`

| product_id | product_name |
|---|---|
| 10 | Laptop |
| 11 | Mouse |
| 12 | Keyboard |

**SQL:**
```sql
-- setup (SQLite types; dates stored as 'YYYY-MM-DD' text)
CREATE TABLE customers (customer_id INTEGER, name TEXT);
CREATE TABLE orders (order_id INTEGER, customer_id INTEGER);
CREATE TABLE order_items (order_id INTEGER, product_id INTEGER);
CREATE TABLE products (product_id INTEGER, product_name TEXT);

SELECT c.name
FROM customers c
JOIN orders o       ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id   = o.order_id
JOIN products p     ON p.product_id  = oi.product_id
WHERE p.product_name IN ('Laptop', 'Mouse')
GROUP BY c.customer_id, c.name
HAVING COUNT(DISTINCT p.product_name) = 2
ORDER BY c.name;
```
**Output:**

| name |
|---|
| Asha |
| Bala |

**pandas equivalent** (gives the same result as the SQL above):
```python
m = (customers.merge(orders, on="customer_id").merge(order_items, on="order_id").merge(products, on="product_id"))
m = m[m["product_name"].isin(["Laptop", "Mouse"])]
g = m.groupby(["customer_id", "name"], as_index=False).agg(n=("product_name", "nunique"))
result = g[g["n"] == 2][["name"]].sort_values("name").reset_index(drop=True)
```
**Edge cases:** Cancelled/returned orders may need filtering. Product names should be unique (use product_id if two products share a name). If the list grows to 3 products, change the 2 to 3 (or use the count of the list). Customers who bought neither never appear.
**Likely follow-ups:** How to require both in the SAME order? Group by order_id instead of customer_id. How to find Laptop but NOT Mouse? Use NOT EXISTS or LEFT JOIN ... IS NULL.
**Common mistakes:** Writing AND on the same column (empty result); forgetting DISTINCT in the count; hardcoding 2 without matching the IN list.

### Q15 ⭐⭐⭐ 🟡 HR: List departments that have more than 5 employees and an average salary above ₹60,000.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know WHERE vs HAVING, and can you combine two conditions on groups in one HAVING?
**Say this in the interview:** I group employees by department, and in HAVING I keep groups where COUNT(*) is more than 5 AND AVG(salary) is above 60,000. HAVING is the filter for group-level results.
**Explain simply:**
- **Aggregate functions** (COUNT, AVG, SUM) summarise many rows into one value per group.
- **WHERE** cannot see aggregate results because it runs before grouping; **HAVING** runs after, so it can.
- Both conditions are about groups, so both go in HAVING joined by AND.
**Example:** HR: 6 people, average 56,167 (fails salary test). Finance: 6, average 74,333 (passes). IT: 7, average 94,286 (passes). Legal: 3 people (fails count even though the average is high). Admin: 6, average 41,667 (fails).
**Sample data:**

`employees`

| emp_id | name | dept_name | salary |
|---|---|---|---|
| 1 | E1 | HR | 50000 |
| 2 | E2 | HR | 55000 |
| 3 | E3 | HR | 58000 |
| 4 | E4 | HR | 52000 |
| 5 | E5 | HR | 60000 |
| 6 | E6 | HR | 62000 |
| 7 | E7 | Finance | 70000 |
| 8 | E8 | Finance | 75000 |

(first 8 of 28 rows shown)

**SQL:**
```sql
-- setup (SQLite types; dates stored as 'YYYY-MM-DD' text)
CREATE TABLE employees (emp_id INTEGER, name TEXT, dept_name TEXT, salary INTEGER);

SELECT dept_name,
       COUNT(*)                AS headcount,
       ROUND(AVG(salary), 0)   AS avg_salary
FROM employees
GROUP BY dept_name
HAVING COUNT(*) > 5 AND AVG(salary) > 60000
ORDER BY avg_salary DESC;
```
**Output:**

| dept_name | headcount | avg_salary |
|---|---|---|
| IT | 7 | 94286 |
| Finance | 6 | 74333 |

**pandas equivalent** (gives the same result as the SQL above):
```python
g = employees.groupby("dept_name", as_index=False).agg(headcount=("emp_id", "count"), avg_salary=("salary", "mean"))
g["avg_salary"] = g["avg_salary"].round(0)
result = g[(g["headcount"] > 5) & (employees.groupby("dept_name")["salary"].mean().reindex(g["dept_name"]).values > 60000)].sort_values("avg_salary", ascending=False).reset_index(drop=True)
```
**Edge cases:** AVG ignores NULL salaries but COUNT(*) counts those rows too; use COUNT(salary) if only paid rows matter. Exactly 5 employees fails 'more than 5'. Departments with no employees never appear. Use active employees only if the question means current staff.
**Likely follow-ups:** How to also show department name from a departments table? JOIN first, then GROUP BY. Can I use the alias avg_salary in HAVING? Not in standard SQL; MySQL allows it, PostgreSQL and SQL Server do not.
**Common mistakes:** Using WHERE COUNT(*) > 5 (error); using >= 5; putting AVG on the unrounded vs rounded value; forgetting that HAVING needs GROUP BY logic.

### Q16 ⭐⭐⭐ 🟡 E-commerce: Find products that have never been sold (present in `products` but not in `order_items`).
**Asked at:** commonly asked (no company-specific report found); the 'customers with no orders' anti-join pattern is listed in Analytics Vidhya's SQL guide, and this is the same idea for products.
**What the interviewer is checking:** Do you know the anti-join: LEFT JOIN with IS NULL (or NOT EXISTS), and the NOT IN trap with NULLs?
**Say this in the interview:** I LEFT JOIN products to order_items and keep rows where the order_items side is NULL, meaning no match. NOT EXISTS gives the same answer and is safer than NOT IN when NULLs are around.
**Explain simply:**
- An **anti-join** finds rows in table A with no match in table B.
- LEFT JOIN keeps every product; for products never sold, the order_items columns come back NULL, so `WHERE oi.product_id IS NULL` isolates them.
- `NOT EXISTS (SELECT 1 FROM order_items WHERE ...)` says 'there is no matching sale row' and reads naturally.
- `NOT IN (SELECT product_id FROM order_items)` returns nothing at all if even one product_id in order_items is NULL, a classic trap.
**Example:** 5 products, 2 sold (Laptop, Mouse). Keyboard, Webcam and Dock have never been sold.
**Sample data:**

`products`

| product_id | product_name |
|---|---|
| 1 | Laptop |
| 2 | Mouse |
| 3 | Keyboard |
| 4 | Webcam |
| 5 | Dock |

`order_items`

| order_id | product_id |
|---|---|
| 1 | 1 |
| 1 | 2 |
| 2 | 1 |
| 3 | 2 |

**SQL:**
```sql
-- setup (SQLite types; dates stored as 'YYYY-MM-DD' text)
CREATE TABLE products (product_id INTEGER, product_name TEXT);
CREATE TABLE order_items (order_id INTEGER, product_id INTEGER);

-- LEFT JOIN version
SELECT p.product_id, p.product_name
FROM products p
LEFT JOIN order_items oi ON oi.product_id = p.product_id
WHERE oi.product_id IS NULL
ORDER BY p.product_id;

-- NOT EXISTS version (same result)
SELECT p.product_id, p.product_name
FROM products p
WHERE NOT EXISTS (SELECT 1 FROM order_items oi WHERE oi.product_id = p.product_id)
ORDER BY p.product_id;
```
**Output:**

LEFT JOIN version

| product_id | product_name |
|---|---|
| 3 | Keyboard |
| 4 | Webcam |
| 5 | Dock |

NOT EXISTS version (same result)

| product_id | product_name |
|---|---|
| 3 | Keyboard |
| 4 | Webcam |
| 5 | Dock |

**pandas equivalent** (gives the same result as the SQL above):
```python
# LEFT JOIN version
m = products.merge(order_items, on="product_id", how="left", indicator=True)
result = m[m["_merge"] == "left_only"][["product_id", "product_name"]].sort_values("product_id").reset_index(drop=True)

# NOT EXISTS version (same result)
sold = set(order_items["product_id"])
result = products[~products["product_id"].isin(sold)][["product_id", "product_name"]].sort_values("product_id").reset_index(drop=True)
```
**Edge cases:** A sale that was cancelled may still sit in order_items; decide if 'never sold' should ignore cancelled orders (join to orders and filter status). NULL product_id in order_items breaks NOT IN but not NOT EXISTS or LEFT JOIN. Duplicate product rows in products would be listed twice.
**Likely follow-ups:** Which is faster? Modern optimisers treat the three forms similarly; check the execution plan. How to find customers with no orders? Same pattern with customers and orders.
**Common mistakes:** Using INNER JOIN (returns the sold ones); `WHERE oi.product_id = NULL` (never true, use IS NULL); NOT IN with NULLs; putting the IS NULL test on a column from products.

### Q17 ⭐⭐⭐ 🟡 Sales: Calculate average order value per customer city.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you define 'average order value' correctly (average per order, not per customer) and join orders to the customer's city?
**Say this in the interview:** Average order value is total order amount divided by number of orders. I join orders to customers for the city, group by city and take AVG(amount), so each order counts once.
**Explain simply:**
- **Average order value (AOV)** = revenue / number of orders. It is not the average of customers' totals.
- `orders` has no city, so JOIN to `customers` on `customer_id`, then `GROUP BY city`.
- Cities with customers but no orders (Delhi) do not appear in an inner join; LEFT JOIN from customers shows them with NULL AOV.
**Example:** Mumbai: orders 1,000, 500, 1,500, 900 = 3,900 over 4 orders = 975. Pune: 800, 400, 1,200 = 2,400 over 3 = 800.
**Sample data:**

`customers`

| customer_id | name | city |
|---|---|---|
| 1 | Asha | Mumbai |
| 2 | Bala | Mumbai |
| 3 | Chitra | Pune |
| 4 | Dev | Pune |
| 5 | Esha | Delhi |

`orders`

| order_id | customer_id | amount |
|---|---|---|
| 1 | 1 | 1000 |
| 2 | 1 | 500 |
| 3 | 2 | 1500 |
| 4 | 3 | 800 |
| 5 | 3 | 400 |
| 6 | 4 | 1200 |
| 7 | 2 | 900 |

**SQL:**
```sql
-- setup (SQLite types; dates stored as 'YYYY-MM-DD' text)
CREATE TABLE customers (customer_id INTEGER, name TEXT, city TEXT);
CREATE TABLE orders (order_id INTEGER, customer_id INTEGER, amount INTEGER);

SELECT c.city,
       COUNT(o.order_id)      AS orders,
       ROUND(AVG(o.amount), 1) AS avg_order_value
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
GROUP BY c.city
ORDER BY avg_order_value DESC;
```
**Output:**

| city | orders | avg_order_value |
|---|---|---|
| Mumbai | 4 | 975 |
| Pune | 3 | 800 |

**pandas equivalent** (gives the same result as the SQL above):
```python
m = orders.merge(customers, on="customer_id")
g = m.groupby("city", as_index=False).agg(orders=("order_id", "count"), avg_order_value=("amount", "mean"))
g["avg_order_value"] = g["avg_order_value"].round(1)
result = g.sort_values("avg_order_value", ascending=False).reset_index(drop=True)
```
**Edge cases:** If the orders table holds one row per item line, you must first sum to order level (CTE grouped by order_id) before averaging, or AOV is really average line value. NULL city forms its own group; label it with COALESCE(city,'Unknown'). Cancelled orders may need excluding. Customers who moved cities: the city is as of today, not at order time.
**Likely follow-ups:** How is that different from average spend per customer? Spend per customer divides by customers, AOV by orders. How to show cities without orders? LEFT JOIN from customers.
**Common mistakes:** Averaging per-customer totals; averaging order lines instead of orders; AVG after joining to order_items (repeats each order amount once per item and skews the average).

### Q18 ⭐⭐⭐ 🔴 HR: Using join_date and left_date, produce for each month of 2025 the opening headcount, joiners, leavers and closing headcount.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you build a month-by-month roll-forward (opening + joiners - leavers = closing) from two date columns, using a generated calendar?
**Say this in the interview:** I generate the 12 month starts with a recursive CTE. For each month I count opening headcount as people who joined before the month and were still there on its first day, joiners as join dates inside the month, leavers as left dates inside the month, and closing as opening plus joiners minus leavers.
**Explain simply:**
- **Roll-forward**: opening headcount + joiners - leavers = closing headcount, and each month's closing equals next month's opening. It is the standard way HR reports headcount.
- A **recursive CTE** builds the list of months: start with '2025-01-01' and keep adding one month until December (SQLite/PostgreSQL syntax; SQL Server omits the word RECURSIVE; not run here). A plain VALUES list of 12 dates works too.
- Convention: left_date is the last day worked, so a person leaving on 28 Feb counts as a leaver in Feb and is not in March's opening. State your convention.
- Join each month to employees with a condition-based join, or use correlated sub-selects as below.
**Example:** Opening in Jan = people already employed on 1 Jan (employee 7 left on 31 Dec 2024, so excluded). Check at the end: Dec closing must match a direct count of people active on 31 Dec 2025.
**Sample data:**

`employees`

| emp_id | join_date | left_date |
|---|---|---|
| 1 | 2019-05-01 | NULL |
| 2 | 2020-02-10 | 2025-02-14 |
| 3 | 2021-08-01 | NULL |
| 4 | 2022-01-03 | 2025-03-31 |
| 5 | 2023-04-17 | NULL |
| 6 | 2024-11-01 | 2025-06-30 |
| 7 | 2018-07-01 | 2024-12-31 |
| 8 | 2025-01-20 | NULL |

(first 8 of 12 rows shown)

**SQL:**
```sql
-- setup (SQLite types; dates stored as 'YYYY-MM-DD' text)
CREATE TABLE employees (emp_id INTEGER, join_date TEXT, left_date TEXT);

WITH RECURSIVE months(m_start) AS (
  SELECT '2025-01-01'
  UNION ALL
  SELECT date(m_start, '+1 month') FROM months WHERE m_start < '2025-12-01'
),
x AS (
  SELECT m.m_start,
    (SELECT COUNT(*) FROM employees e
      WHERE e.join_date < m.m_start
        AND (e.left_date IS NULL OR e.left_date >= m.m_start)) AS opening,
    (SELECT COUNT(*) FROM employees e
      WHERE e.join_date >= m.m_start AND e.join_date < date(m.m_start, '+1 month')) AS joiners,
    (SELECT COUNT(*) FROM employees e
      WHERE e.left_date >= m.m_start AND e.left_date < date(m.m_start, '+1 month')) AS leavers
  FROM months m
)
SELECT substr(m_start, 1, 7) AS month,
       opening, joiners, leavers,
       opening + joiners - leavers AS closing
FROM x
ORDER BY m_start;

-- Cross-check: direct count of people active on 31 Dec 2025 (should equal the December closing)
SELECT COUNT(*) AS active_on_31_dec
FROM employees
WHERE join_date <= '2025-12-31' AND (left_date IS NULL OR left_date > '2025-12-31');
```
**Output:**

| month | opening | joiners | leavers | closing |
|---|---|---|---|---|
| 2025-01 | 6 | 1 | 0 | 7 |
| 2025-02 | 7 | 0 | 1 | 6 |
| 2025-03 | 6 | 1 | 1 | 6 |
| 2025-04 | 6 | 2 | 0 | 8 |
| 2025-05 | 8 | 0 | 0 | 8 |
| 2025-06 | 8 | 0 | 1 | 7 |
| 2025-07 | 7 | 0 | 0 | 7 |
| 2025-08 | 7 | 0 | 0 | 7 |
| 2025-09 | 7 | 0 | 1 | 6 |
| 2025-10 | 6 | 1 | 0 | 7 |
| 2025-11 | 7 | 0 | 0 | 7 |
| 2025-12 | 7 | 0 | 0 | 7 |

Cross-check: direct count of people active on 31 Dec 2025 (should equal the December closing)

| active_on_31_dec |
|---|
| 7 |

**pandas equivalent** (gives the same result as the SQL above):
```python
e = employees.copy()
e["join_date"] = pd.to_datetime(e["join_date"]); e["left_date"] = pd.to_datetime(e["left_date"])
rows = []
for s in pd.date_range("2025-01-01", periods=12, freq="MS"):
    nxt = s + pd.offsets.MonthBegin(1)
    opening = int(((e["join_date"] < s) & (e["left_date"].isna() | (e["left_date"] >= s))).sum())
    joiners = int(((e["join_date"] >= s) & (e["join_date"] < nxt)).sum())
    leavers = int(((e["left_date"] >= s) & (e["left_date"] < nxt)).sum())
    rows.append((s.strftime("%Y-%m"), opening, joiners, leavers, opening + joiners - leavers))
result = pd.DataFrame(rows, columns=["month", "opening", "joiners", "leavers", "closing"])

# Cross-check: direct count of people active on 31 Dec 2025 (should equal the December closing)
e = employees.copy()
j = pd.to_datetime(e["join_date"]); l = pd.to_datetime(e["left_date"])
result = pd.DataFrame({"active_on_31_dec": [int(((j <= "2025-12-31") & (l.isna() | (l > "2025-12-31"))).sum())]})
```
**Edge cases:** Someone who joins and leaves in the same month is counted as both joiner and leaver, and the roll-forward still balances. Left_date earlier than join_date is a data error. If left_date is the first day of absence instead of the last day worked, change `>=` to `>` in opening. Rehires (same person with two rows) need an ID clean-up first.
**Likely follow-ups:** How to compute monthly attrition from this? leavers / ((opening+closing)/2) per month. How to do it without a recursive CTE? A calendar table or generate_series in PostgreSQL.
**Common mistakes:** Opening computed with <= month start (counts joiners twice); forgetting people who left before the year; hardcoding 12 separate queries; not checking that closing = next opening.

### Q19 ⭐⭐⭐ 🔴 E-commerce: Find customers who placed at least one order in every month of 2025.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you count DISTINCT months per customer (not orders), filter to the year, and compare to 12 with HAVING?
**Say this in the interview:** I keep 2025 orders, group by customer, count the distinct months they ordered in, and keep customers where that count is 12. Counting orders would be wrong, because many orders can fall in one month.
**Explain simply:**
- A customer ordering in every month has 12 different month numbers within 2025. `COUNT(DISTINCT month)` counts each month once even if they ordered five times in it.
- Apply the year filter in WHERE first. Otherwise December 2024 plus Jan-Nov 2025 would look like 12 months.
- Month number in SQLite: `strftime('%m', order_date)`; PostgreSQL `EXTRACT(MONTH ...)`; MySQL/SQL Server `MONTH(order_date)` (not run here).
**Example:** Customers 101 and 104 order in all 12 months of 2025 (101 also has two extra orders). 102 misses December. 103 has a December order, but in 2024, so it does not count. 105 ordered only 3 months.
**Sample data:**

`orders`

| order_id | customer_id | order_date |
|---|---|---|
| 1 | 101 | 2025-01-11 |
| 2 | 101 | 2025-02-12 |
| 3 | 101 | 2025-03-13 |
| 4 | 101 | 2025-04-14 |
| 5 | 101 | 2025-05-15 |
| 6 | 101 | 2025-06-16 |
| 7 | 101 | 2025-07-17 |
| 8 | 101 | 2025-08-18 |

(first 8 of 52 rows shown)

**SQL:**
```sql
-- setup (SQLite types; dates stored as 'YYYY-MM-DD' text)
CREATE TABLE orders (order_id INTEGER, customer_id INTEGER, order_date TEXT);

SELECT customer_id,
       COUNT(DISTINCT strftime('%m', order_date)) AS active_months
FROM orders
WHERE order_date >= '2025-01-01' AND order_date < '2026-01-01'
GROUP BY customer_id
HAVING COUNT(DISTINCT strftime('%m', order_date)) = 12
ORDER BY customer_id;
```
**Output:**

| customer_id | active_months |
|---|---|
| 101 | 12 |
| 104 | 12 |

**pandas equivalent** (gives the same result as the SQL above):
```python
o = orders.copy()
o["order_date"] = pd.to_datetime(o["order_date"])
o = o[o["order_date"].dt.year == 2025]
g = o.groupby("customer_id", as_index=False).agg(active_months=("order_date", lambda s: s.dt.month.nunique()))
result = g[g["active_months"] == 12].sort_values("customer_id").reset_index(drop=True)
```
**Edge cases:** Counting rows (COUNT(*) = 12) is wrong both ways: a customer can have 12 orders in 8 months, or 11 months of orders plus extras. Cancelled orders may need excluding. For a part-year (e.g. 'every month so far this year'), compare to the number of elapsed months. Hard-coding 12 is fine for a full calendar year.
**Likely follow-ups:** How to list the missing months for customers who almost qualify? Cross join customers with a month list and LEFT JOIN orders. How to find longest consecutive streaks? That is gaps-and-islands (Part 10).
**Common mistakes:** COUNT(*) instead of COUNT(DISTINCT month); forgetting the year filter so months from different years combine; using strftime('%m') without a year filter on multi-year data.

### Q20 ⭐⭐⭐ 🔴 Sales: Find the top 3 products by revenue within each product category.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you rank rows inside each group (not across the whole table) and keep only the top N per group?
**Say this in the interview:** "First I total the revenue per product, because an order has many lines. Then I rank products inside each category with RANK and PARTITION BY category, and keep rank 3 or better. I wrap it in a CTE because I cannot filter on a window function directly."
**Explain simply:**
- **Revenue** here is quantity times unit price, added up per product (`SUM(qty * unit_price)`).
- A **window function** (`RANK() OVER (...)`) numbers rows without collapsing them. `PARTITION BY category` restarts the numbering for each category, like ranking staff separately inside each department.
- A **CTE** (the `WITH name AS (...)` part) is a named temporary result that keeps the query readable. It is needed because `WHERE rnk <= 3` cannot sit in the same SELECT that creates `rnk`.
- `RANK` gives tied products the same number, so a tie for 3rd place returns 4 rows. Use `ROW_NUMBER` for exactly 3 rows, or `DENSE_RANK` if you want no gaps in the numbers.
**Example:** Electronics: Laptop 100,000, Phone 60,000, Tablet 40,000 and Earbuds 40,000 (tie for 3rd). Apparel has only 4 products, so its 4th (Socks, 2,000) drops out.
**Sample data:**

*products*

| product_id | product_name | category |
|---|---|---|
| 1 | Laptop | Electronics |
| 2 | Phone | Electronics |
| 3 | Tablet | Electronics |
| 4 | Earbuds | Electronics |
| 5 | Cable | Electronics |
| 6 | Shirt | Apparel |
| 7 | Jeans | Apparel |
| 8 | Jacket | Apparel |
| 9 | Socks | Apparel |

*order_items*

| order_id | product_id | qty | unit_price |
|---|---|---|---|
| 101 | 1 | 1 | 50000 |
| 102 | 1 | 1 | 50000 |
| 101 | 2 | 3 | 20000 |
| 103 | 3 | 4 | 10000 |
| 104 | 4 | 8 | 5000 |
| 105 | 5 | 10 | 500 |
| 106 | 6 | 10 | 800 |
| 107 | 7 | 5 | 1500 |
| 108 | 8 | 2 | 3000 |
| 109 | 9 | 20 | 100 |

**SQL:**
```sql
WITH rev AS (
  SELECT p.category, p.product_name, SUM(oi.qty * oi.unit_price) AS revenue
  FROM order_items oi
  JOIN products p ON p.product_id = oi.product_id
  GROUP BY p.category, p.product_name
),
ranked AS (
  SELECT category, product_name, revenue,
         RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS rnk
  FROM rev
)
SELECT category, product_name, revenue, rnk
FROM ranked
WHERE rnk <= 3
ORDER BY category, rnk, product_name;

-- Same idea, exactly 3 rows per category (ties broken arbitrarily): swap RANK() for ROW_NUMBER() (not run here).
```
**Output:**

| category | product_name | revenue | rnk |
|---|---|---|---|
| Apparel | Shirt | 8000 | 1 |
| Apparel | Jeans | 7500 | 2 |
| Apparel | Jacket | 6000 | 3 |
| Electronics | Laptop | 100000 | 1 |
| Electronics | Phone | 60000 | 2 |
| Electronics | Earbuds | 40000 | 3 |
| Electronics | Tablet | 40000 | 3 |

**pandas equivalent:**
```python
# the tables above are DataFrames with the same names and columns
import pandas as pd
m = order_items.merge(products, on='product_id')
m['revenue'] = m.qty * m.unit_price
rev = m.groupby(['category', 'product_name'], as_index=False).revenue.sum()
rev['rnk'] = rev.groupby('category').revenue.rank(method='min', ascending=False).astype(int)
res = (rev[rev.rnk <= 3].sort_values(['category', 'rnk', 'product_name'])
       .reset_index(drop=True))
# Output (matches the SQL):
#    category product_name  revenue  rnk
#     Apparel        Shirt     8000    1
#     Apparel        Jeans     7500    2
#     Apparel       Jacket     6000    3
# Electronics       Laptop   100000    1
# Electronics        Phone    60000    2
# Electronics      Earbuds    40000    3
# Electronics       Tablet    40000    3
```
**Edge cases:** Ties at the cut-off (Tablet and Earbuds) return 4 rows with `RANK`. A category with fewer than 3 products simply returns what it has. Products never sold have no `order_items` rows, so they are absent (use a LEFT JOIN from `products` if you want them with 0 revenue). NULL qty or price gives a NULL line value that `SUM` skips.
**Likely follow-ups:**
- How do you get exactly 3 per category? `ROW_NUMBER()`, adding a tie-breaker such as `product_name`.
- Top 3 without window functions? A correlated subquery counting how many products in the same category earn more; keep those with fewer than 3. It is slower and harder to read.
- SQL Server/MySQL 8/PostgreSQL all support this form; MySQL 5.7 does not support window functions (from memory, not run here).
**Common mistakes:** Using `LIMIT 3` (gives 3 rows for the whole table, not per category); ranking before totalling per product, so the same product ranks several times; filtering `WHERE rnk <= 3` in the same SELECT where `rnk` is created.

### Q21 ⭐⭐ 🟢 HR: Show the number of male and female employees in each department.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Conditional counting (a CASE inside COUNT/SUM) and keeping departments that have nobody.
**Say this in the interview:** "I start from the departments table and LEFT JOIN employees, so an empty department still shows with zeros. Then I use COUNT with CASE WHEN gender = 'M' to get male and female side by side. I also keep a column for blank genders so the numbers add up to the headcount."
**Explain simply:**
- **Conditional aggregation** = putting a CASE inside an aggregate so each column counts only its own rows. `COUNT(CASE WHEN gender='M' THEN 1 END)` counts only males, because `COUNT` ignores NULLs and the CASE returns NULL for everyone else.
- **LEFT JOIN** keeps every row from the left table (departments) even when no employee matches.
- Real HR data has blanks or other values in gender; a third column keeps the totals honest instead of silently losing people.
- A simpler 'long' alternative is `GROUP BY dept_name, gender`, which gives one row per department-gender pair instead of columns.
**Example:** Sales has Dev, Farid, Gopal (M) and Esha (F): 3 male, 1 female. Finance has nobody: 0 and 0.
**Sample data:**

*departments*

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Sales |
| 3 | IT |
| 4 | Finance |

*employees*

| emp_id | name | dept_id | gender |
|---|---|---|---|
| 1 | Asha | 1 | F |
| 2 | Bala | 1 | M |
| 3 | Chitra | 1 | F |
| 4 | Dev | 2 | M |
| 5 | Esha | 2 | F |
| 6 | Farid | 2 | M |
| 7 | Gopal | 2 | M |
| 8 | Hari | 3 | M |
| 9 | Isha | 3 | NULL |

**SQL:**
```sql
SELECT d.dept_name,
       COUNT(CASE WHEN e.gender = 'M' THEN 1 END) AS male,
       COUNT(CASE WHEN e.gender = 'F' THEN 1 END) AS female,
       COUNT(CASE WHEN e.emp_id IS NOT NULL AND e.gender IS NULL THEN 1 END) AS not_stated
FROM departments d
LEFT JOIN employees e ON e.dept_id = d.dept_id
GROUP BY d.dept_name
ORDER BY d.dept_name;
```
**Output:**

| dept_name | male | female | not_stated |
|---|---|---|---|
| Finance | 0 | 0 | 0 |
| HR | 1 | 2 | 0 |
| IT | 1 | 0 | 1 |
| Sales | 3 | 1 | 0 |

**pandas equivalent:**
```python
# the tables above are DataFrames with the same names and columns
import pandas as pd
m = departments.merge(employees, on='dept_id', how='left')
m['male'] = (m.gender == 'M').astype(int)
m['female'] = (m.gender == 'F').astype(int)
m['not_stated'] = (m.emp_id.notna() & m.gender.isna()).astype(int)
res = (m.groupby('dept_name', as_index=False)[['male', 'female', 'not_stated']].sum()
       .sort_values('dept_name').reset_index(drop=True))
# Output (matches the SQL):
# dept_name  male  female  not_stated
#   Finance     0       0           0
#        HR     1       2           0
#        IT     1       0           1
#     Sales     3       1           0
```
**Edge cases:** Empty department (Finance) shows 0s only because of the LEFT JOIN; an inner JOIN would drop it. NULL gender (Isha) would vanish from both columns without the `not_stated` column. Inconsistent spellings ('Male', 'm', 'M ') need cleaning first (`UPPER(TRIM(gender))`). Counting `COUNT(*)` after a LEFT JOIN would give Finance a wrong count of 1.
**Likely follow-ups:**
- Same result with `SUM(CASE WHEN ... THEN 1 ELSE 0 END)`? Yes, identical; `COUNT(CASE ...)` is just shorter.
- How do you add a percentage of female staff? `ROUND(100.0 * female / NULLIF(male+female+not_stated, 0), 1)`, and say what the denominator is.
- PostgreSQL has `COUNT(*) FILTER (WHERE gender='M')`, SQLite 3.30+ too; MySQL and SQL Server need CASE.
**Common mistakes:** Using an inner JOIN and losing empty departments; `WHERE gender = 'M'` before grouping, which kills the female column; writing `COUNT(CASE WHEN ... THEN 1 ELSE 0 END)`, which counts every row because 0 is not NULL.

### Q22 ⭐⭐ 🟢 HR: List employees who joined in the last 90 days (new hires) with their department.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Date arithmetic with a clear window, and whether you notice joiners with a future date or no department.
**Say this in the interview:** "I compute the cutoff as today minus 90 days and keep people whose hire date is on or after it. I also cap at today so someone with a future joining date is not counted as a new hire, and I LEFT JOIN departments so a missing department doesn't hide the person."
**Explain simply:**
- The **window** is `hire_date >= today - 90 days` and `hire_date <= today`. Both ends matter.
- Date functions differ by database: that is the main thing to name in the interview (see the dialect list in the SQL block).
- **LEFT JOIN** keeps the employee even if `dept_id` is NULL; the department name then shows as NULL.
- Compare the raw `hire_date` column to the cutoff (do not wrap the column in a function), which lets the database use an index (a lookup shortcut) on that column.
**Example:** With today = 2026-10-21 the cutoff is 2026-07-23. Esha joined exactly on 2026-07-23 (90 days ago) and is in; Farid joined on 07-22 and is out. Today is fixed at 2026-10-21 in the sample so the result never changes; in real life replace it with `CURRENT_DATE`.
**Sample data:**

*departments*

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Sales |
| 3 | IT |

*employees*

| emp_id | name | dept_id | hire_date |
|---|---|---|---|
| 1 | Asha | 1 | 2025-04-01 |
| 2 | Bala | 2 | 2026-08-05 |
| 3 | Chitra | 2 | 2026-09-15 |
| 4 | Dev | NULL | 2026-10-01 |
| 5 | Esha | 3 | 2026-07-23 |
| 6 | Farid | 3 | 2026-07-22 |
| 7 | Gita | 1 | 2026-11-03 |

**SQL:**
```sql
-- SQLite (dialect used to run it). 'now' is replaced by a fixed date for a repeatable result.
SELECT e.emp_id, e.name, d.dept_name, e.hire_date,
       CAST(julianday('2026-10-21') - julianday(e.hire_date) AS INTEGER) AS days_since_joining
FROM employees e
LEFT JOIN departments d ON d.dept_id = e.dept_id
WHERE e.hire_date >= date('2026-10-21', '-90 day')
  AND e.hire_date <= '2026-10-21'
ORDER BY e.hire_date DESC;

-- Alternatives (not run here / from memory):
-- PostgreSQL : WHERE hire_date >= CURRENT_DATE - INTERVAL '90 days' AND hire_date <= CURRENT_DATE
-- MySQL      : WHERE hire_date >= CURDATE() - INTERVAL 90 DAY AND hire_date <= CURDATE()
-- SQL Server : WHERE hire_date >= DATEADD(day, -90, CAST(GETDATE() AS date)) AND hire_date <= CAST(GETDATE() AS date)
```
**Output:**

| emp_id | name | dept_name | hire_date | days_since_joining |
|---|---|---|---|---|
| 4 | Dev | NULL | 2026-10-01 | 20 |
| 3 | Chitra | Sales | 2026-09-15 | 36 |
| 2 | Bala | Sales | 2026-08-05 | 77 |
| 5 | Esha | IT | 2026-07-23 | 90 |

**pandas equivalent:**
```python
# the tables above are DataFrames with the same names and columns
import pandas as pd
today = pd.Timestamp('2026-10-21')
cutoff = (today - pd.Timedelta(days=90)).strftime('%Y-%m-%d')
m = employees.merge(departments, on='dept_id', how='left')
m['days_since_joining'] = (today - pd.to_datetime(m.hire_date)).dt.days
res = (m[(m.hire_date >= cutoff) & (m.hire_date <= '2026-10-21')]
       [['emp_id', 'name', 'dept_name', 'hire_date', 'days_since_joining']]
       .sort_values('hire_date', ascending=False).reset_index(drop=True))
# Output (matches the SQL):
#  emp_id   name dept_name  hire_date  days_since_joining
#       4    Dev       NaN 2026-10-01                  20
#       3 Chitra     Sales 2026-09-15                  36
#       2   Bala     Sales 2026-08-05                  77
#       5   Esha        IT 2026-07-23                  90
```
**Edge cases:** Future joiner (Gita, 2026-11-03) is excluded by the upper bound. Dev has no department (NULL) but is still listed. If `hire_date` is stored as text in a non-ISO format ('21/10/2026') comparisons break; convert first. If `hire_date` has a time part, compare against the start of the day. Rehires may have two rows; decide whether they count as new.
**Likely follow-ups:**
- 'Last 3 months' instead of 90 days? Use a month interval (`INTERVAL '3 months'` in PostgreSQL); state which one you chose because they differ by a few days.
- New hires per department? Add `GROUP BY d.dept_name` with `COUNT(*)`.
- Why not `WHERE DATEDIFF(day, hire_date, GETDATE()) <= 90`? It works but wraps the column in a function, so an index on hire_date can't be used.
**Common mistakes:** Forgetting the upper bound (future joiners slip in); using `BETWEEN` with a datetime column and missing the last day; hard-coding today's date and forgetting to update it; using an inner JOIN and dropping people with no department.

### Q23 ⭐⭐ 🟢 HR: Show the highest, lowest and spread (max minus min) of salary in each department.
**Asked at:** commonly asked; per-department salary aggregates appear in a 2025 SQL question guide (Analytics Vidhya, source 2 in research/Book02_Part08_sources.md); no company-specific report found
**What the interviewer is checking:** MIN/MAX/arithmetic on aggregates and how NULLs and one-person departments behave.
**Say this in the interview:** "I group by department and take MAX and MIN of salary; the spread is MAX minus MIN. I LEFT JOIN from departments so empty ones still show, and I know MIN and MAX skip NULL salaries."
**Explain simply:**
- An **aggregate** (MAX, MIN, SUM...) collapses many rows into one number per group. `GROUP BY dept_name` makes one group per department.
- **Spread** (also called range) = highest minus lowest. It tells HR how wide the pay band is: a spread of 40,000 on a 60,000 base means big internal differences.
- You can do arithmetic on two aggregates in the same SELECT: `MAX(salary) - MIN(salary)`.
- A department with one person has spread 0; a department with nobody has NULLs, because there is nothing to take a maximum of.
**Example:** Sales: highest 90,000, lowest 70,000, spread 20,000. Admin has one person at 45,000, so spread is 0.
**Sample data:**

*departments*

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Sales |
| 3 | IT |
| 4 | Finance |
| 5 | Admin |

*employees*

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 1 | NULL |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 2 | 90000 |
| 6 | Farid | 2 | 90000 |
| 7 | Gita | 3 | 80000 |
| 8 | Hari | 3 | 120000 |
| 9 | Isha | 5 | 45000 |

**SQL:**
```sql
SELECT d.dept_name,
       MAX(e.salary) AS highest,
       MIN(e.salary) AS lowest,
       MAX(e.salary) - MIN(e.salary) AS spread
FROM departments d
LEFT JOIN employees e ON e.dept_id = d.dept_id
GROUP BY d.dept_name
ORDER BY d.dept_name;
```
**Output:**

| dept_name | highest | lowest | spread |
|---|---|---|---|
| Admin | 45000 | 45000 | 0 |
| Finance | NULL | NULL | NULL |
| HR | 60000 | 50000 | 10000 |
| IT | 120000 | 80000 | 40000 |
| Sales | 90000 | 70000 | 20000 |

**pandas equivalent:**
```python
# the tables above are DataFrames with the same names and columns
import pandas as pd
m = departments.merge(employees, on='dept_id', how='left')
res = (m.groupby('dept_name', as_index=False)
       .agg(highest=('salary', 'max'), lowest=('salary', 'min')))
res['spread'] = res.highest - res.lowest
res = res.sort_values('dept_name').reset_index(drop=True)
# Output (matches the SQL):
# dept_name  highest  lowest  spread
#     Admin  45000.0 45000.0     0.0
#   Finance      NaN     NaN     NaN
#        HR  60000.0 50000.0 10000.0
#        IT 120000.0 80000.0 40000.0
#     Sales  90000.0 70000.0 20000.0
```
**Edge cases:** Finance (no employees) returns NULL for all three numbers. HR's NULL salary (Chitra) is ignored, so HR's min is 50,000 and not 0; decide whether a missing salary is a data error to fix. One-person department = spread 0. Grouping by `dept_id` instead of `dept_name` is safer if two departments share a name.
**Likely follow-ups:**
- Who earns the max in each department? Needs the subquery or `RANK()` approach (Part 8 Q20 style / Part 5).
- How would you show the average too? Add `AVG(e.salary)`; AVG also ignores NULLs, so state that the average excludes blanks.
- Spread vs standard deviation? Spread uses only two people; standard deviation uses everyone (`STDDEV` in PostgreSQL/MySQL, `STDEV` in SQL Server; not run here).
**Common mistakes:** Using an inner JOIN and losing empty departments; selecting `name` next to `MAX(salary)` without grouping (invalid or arbitrary in many databases); treating NULL as 0 and getting a wrong minimum.

### Q24 ⭐⭐ 🟢 E-commerce: Count orders by status (delivered, cancelled, returned, in-transit).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Plain GROUP BY / COUNT, plus whether you handle a missing status and give a percentage.
**Say this in the interview:** "I group by status and count the rows. I show NULL status as 'unknown' instead of hiding it, and I add each status's share of all orders so the numbers are easy to read."
**Explain simply:**
- `GROUP BY status` makes one bucket per status; `COUNT(*)` counts rows in each bucket.
- `COALESCE(status, 'unknown')` swaps a NULL for a label. Without it the NULL group shows up as a blank row that people misread.
- `SUM(COUNT(*)) OVER ()` is a **window total**: the grand total of all the group counts, used as the denominator for the percentage.
- Percentages should add to 100; checking that is a quick sanity test.
**Example:** Of 12 orders: 6 delivered (50%), 2 cancelled, 2 in-transit, 1 returned and 1 with no status (each shown with its share).
**Sample data:**

*orders*

| order_id | customer_id | status | amount |
|---|---|---|---|
| 1 | 101 | delivered | 800 |
| 2 | 102 | delivered | 1200 |
| 3 | 103 | cancelled | 500 |
| 4 | 104 | delivered | 300 |
| 5 | 101 | in-transit | 900 |
| 6 | 105 | delivered | 450 |
| 7 | 106 | returned | 700 |
| 8 | 107 | delivered | 1500 |
| 9 | 102 | in-transit | 650 |
| 10 | 108 | cancelled | 400 |
| 11 | 109 | delivered | 250 |
| 12 | 110 | NULL | 600 |

**SQL:**
```sql
SELECT COALESCE(status, 'unknown') AS status,
       COUNT(*) AS orders,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_of_orders
FROM orders
GROUP BY COALESCE(status, 'unknown')
ORDER BY orders DESC, status;
```
**Output:**

| status | orders | pct_of_orders |
|---|---|---|
| delivered | 6 | 50.0 |
| cancelled | 2 | 16.7 |
| in-transit | 2 | 16.7 |
| returned | 1 | 8.3 |
| unknown | 1 | 8.3 |

**pandas equivalent:**
```python
# the tables above are DataFrames with the same names and columns
import pandas as pd
o = orders.assign(status=orders.status.fillna('unknown'))
res = o.groupby('status', as_index=False).agg(orders=('order_id', 'count'))
res['pct_of_orders'] = (100 * res.orders / res.orders.sum()).round(1)
res = res.sort_values(['orders', 'status'], ascending=[False, True]).reset_index(drop=True)
# Output (matches the SQL):
#     status  orders  pct_of_orders
#  delivered       6           50.0
#  cancelled       2           16.7
# in-transit       2           16.7
#   returned       1            8.3
#    unknown       1            8.3
```
**Edge cases:** NULL status (order 12) is its own group. Spelling variants ('Cancelled', 'CANCELLED', 'canceled') make separate groups: clean with `LOWER(TRIM(status))`. Statuses with zero orders do not appear at all; to show them, LEFT JOIN from a list of statuses. Ties in the count are broken by name so the output is stable.
**Likely follow-ups:**
- Why not just `COUNT(status)`? It skips NULLs, so the unknown order would not be counted; `COUNT(*)` counts rows.
- How do you show statuses as columns? Conditional aggregation: `COUNT(CASE WHEN status='delivered' THEN 1 END)` per column (see Q21).
- Window functions need MySQL 8+ / SQL Server 2012+ / any recent PostgreSQL (from memory, not run here).
**Common mistakes:** Forgetting `GROUP BY`; counting a column that has NULLs; computing percentage with integer division (`100 * 2 / 12` gives 16 in many databases, so use `100.0`); not cleaning status text first.

### Q25 ⭐⭐ 🟢 E-commerce: Calculate the overall order cancellation rate as a percentage.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Rate = part / whole; avoiding integer division and a divide-by-zero; stating the denominator.
**Say this in the interview:** "Cancelled orders divided by all orders, times 100. I multiply by 100.0 so it is not integer division, and I say clearly that the denominator is every order. I would also check what the business wants to do with orders that have no status yet."
**Explain simply:**
- **Rate** = cancelled orders / total orders x 100. The 'total' you choose changes the answer, so state it.
- **Integer division** means 2 / 12 becomes 0 in some databases (SQL Server, PostgreSQL). Writing `100.0 *` first forces a decimal answer.
- `SUM(CASE WHEN status='cancelled' THEN 1 ELSE 0 END)` counts cancelled rows; `AVG` of the same 1/0 flag gives the rate directly.
- If the table can be empty, `NULLIF(COUNT(*), 0)` turns a zero denominator into NULL instead of an error.
**Example:** 2 cancelled out of 12 orders = 16.67%. If the 1 order with no status is left out of the denominator, it is 2 / 11 = 18.18%.
**Sample data:**

*orders*

| order_id | customer_id | status | amount |
|---|---|---|---|
| 1 | 101 | delivered | 800 |
| 2 | 102 | delivered | 1200 |
| 3 | 103 | cancelled | 500 |
| 4 | 104 | delivered | 300 |
| 5 | 101 | in-transit | 900 |
| 6 | 105 | delivered | 450 |
| 7 | 106 | returned | 700 |
| 8 | 107 | delivered | 1500 |
| 9 | 102 | in-transit | 650 |
| 10 | 108 | cancelled | 400 |
| 11 | 109 | delivered | 250 |
| 12 | 110 | NULL | 600 |

**SQL:**
```sql
SELECT COUNT(*) AS total_orders,
       SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled,
       ROUND(100.0 * SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END)
             / NULLIF(COUNT(*), 0), 2) AS cancellation_pct
FROM orders;

SELECT ROUND(100.0 * AVG(CASE WHEN status = 'cancelled' THEN 1.0 ELSE 0.0 END), 2) AS cancellation_pct
FROM orders
WHERE status IS NOT NULL;
```
**Output:**

*All orders in the denominator*

| total_orders | cancelled | cancellation_pct |
|---|---|---|
| 12 | 2 | 16.67 |

*Only orders that have a status*

| cancellation_pct |
|---|
| 18.18 |

**pandas equivalent:**
```python
# the tables above are DataFrames with the same names and columns
import pandas as pd
# All orders in the denominator
res = pd.DataFrame({'total_orders': [len(orders)],
                    'cancelled': [int((orders.status == 'cancelled').sum())]})
res['cancellation_pct'] = (100 * res.cancelled / res.total_orders).round(2)
# Output (matches the SQL):
#  total_orders  cancelled  cancellation_pct
#            12          2             16.67

# Only orders that have a status
known = orders[orders.status.notna()]
res = pd.DataFrame({'cancellation_pct': [round(100 * (known.status == 'cancelled').mean(), 2)]})
# Output (matches the SQL):
#  cancellation_pct
#             18.18
```
**Edge cases:** Empty table: `NULLIF` returns NULL instead of a divide-by-zero error. NULL status: decide whether it belongs in the denominator (shown both ways). Duplicated order rows (e.g. one row per item) inflate counts: count `DISTINCT order_id`. Cancellation can mean different things (before dispatch vs after): ask.
**Likely follow-ups:**
- Cancellation rate per city or per month? Add `GROUP BY`; see Q29.
- Is 16.67% good or bad? Compare with a benchmark or the previous period before judging; one number alone does not say.
- `AVG(CASE ...)` trick: why does it work? The CASE gives 1 for cancelled and 0 otherwise, so the average of 1s and 0s is the share of 1s.
**Common mistakes:** Integer division returning 0; dividing by only delivered orders by accident; counting cancelled order lines instead of orders; forgetting that `COUNT(column)` skips NULLs.

### Q26 ⭐⭐ 🟢 HR: Find employees who have no manager assigned and employees whose department is missing (NULLs).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** `IS NULL` (not `= NULL`) and the difference between a NULL department and a department id that points to nothing.
**Say this in the interview:** "I use IS NULL, because comparing with = NULL never matches. And 'department missing' has two meanings: dept_id is blank, or dept_id has a value that does not exist in the departments table. A LEFT JOIN catches both, and I flag each case separately."
**Explain simply:**
- **NULL** means 'unknown or not filled in'. NULL is not equal to anything, not even NULL, so `manager_id = NULL` returns no rows; you must write `manager_id IS NULL`.
- A top person such as the CEO legitimately has no manager, so NULL manager is not always an error: that is a business judgement.
- An **orphan** value is a `dept_id` (like 9) that does not exist in `departments`. It is not NULL, but the department is still effectively missing. The LEFT JOIN plus `d.dept_id IS NULL` finds it.
- The 0/1 flag columns explain why each person was listed.
**Example:** Meera (CEO) has no manager; Sana has no department; Uma has neither; Vikram has dept_id 9 which does not exist.
**Sample data:**

*departments*

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Sales |

*employees*

| emp_id | name | manager_id | dept_id |
|---|---|---|---|
| 1 | Meera | NULL | 1 |
| 2 | Rohan | 1 | 1 |
| 3 | Sana | 1 | NULL |
| 4 | Tarun | 2 | 2 |
| 5 | Uma | NULL | NULL |
| 6 | Vikram | 2 | 9 |
| 7 | Wasim | 2 | 2 |

**SQL:**
```sql
SELECT e.emp_id, e.name,
       CASE WHEN e.manager_id IS NULL THEN 1 ELSE 0 END AS no_manager,
       CASE WHEN e.dept_id IS NULL THEN 1 ELSE 0 END AS dept_is_null,
       CASE WHEN e.dept_id IS NOT NULL AND d.dept_id IS NULL THEN 1 ELSE 0 END AS dept_not_found
FROM employees e
LEFT JOIN departments d ON d.dept_id = e.dept_id
WHERE e.manager_id IS NULL
   OR d.dept_id IS NULL
ORDER BY e.emp_id;
```
**Output:**

| emp_id | name | no_manager | dept_is_null | dept_not_found |
|---|---|---|---|---|
| 1 | Meera | 1 | 0 | 0 |
| 3 | Sana | 0 | 1 | 0 |
| 5 | Uma | 1 | 1 | 0 |
| 6 | Vikram | 0 | 0 | 1 |

**pandas equivalent:**
```python
# the tables above are DataFrames with the same names and columns
import pandas as pd
m = employees.merge(departments, on='dept_id', how='left')
m['no_manager'] = m.manager_id.isna().astype(int)
m['dept_is_null'] = m.dept_id.isna().astype(int)
m['dept_not_found'] = (m.dept_id.notna() & m.dept_name.isna()).astype(int)
res = (m[(m.no_manager == 1) | m.dept_name.isna()]
       [['emp_id', 'name', 'no_manager', 'dept_is_null', 'dept_not_found']]
       .sort_values('emp_id').reset_index(drop=True))
# Output (matches the SQL):
#  emp_id   name  no_manager  dept_is_null  dept_not_found
#       1  Meera           1             0               0
#       3   Sana           0             1               0
#       5    Uma           1             1               0
#       6 Vikram           0             0               1
```
**Edge cases:** `= NULL` and `<> NULL` return nothing; `NOT IN` with a NULL in the list also returns nothing. Empty strings ('') and 'N/A' are not NULL: check for them in messy HR exports. Self-managed rows (manager_id = own emp_id) are another data problem. If nothing matches, the query returns an empty result, which is itself a good data-quality sign.
**Likely follow-ups:**
- How do you replace NULL for display? `COALESCE(manager_id, 0)` or `COALESCE(dept_name, 'Unassigned')`; `IFNULL` (MySQL/SQLite), `ISNULL` (SQL Server).
- How would you stop this happening? A NOT NULL constraint on `dept_id` and a foreign key to `departments`.
- Employees with no manager vs managers with no reports? Different queries; the second is a self-join (Part 8 Q35 style).
**Common mistakes:** Writing `manager_id = NULL`; checking only `dept_id IS NULL` and missing orphan ids; using an inner JOIN, which silently drops exactly the rows you are hunting.

### Q27 ⭐⭐ 🟢 Banking: Using `customers` (dob), count customers by age band: under 25, 25-40, 41-60, above 60.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Deriving age from date of birth correctly, then bucketing with CASE and counting.
**Say this in the interview:** "First I turn date of birth into completed years as of a fixed date, being careful about whose birthday hasn't happened yet this year. Then a CASE expression puts each age in a band and I count per band. Missing birth dates get their own 'Unknown' band."
**Explain simply:**
- **Age** in whole years = year difference, minus 1 if this year's birthday has not happened yet. Simply subtracting years is wrong for part of the year.
- A **CASE** expression is SQL's if/else. Conditions are checked top to bottom, so `age < 25` is tested before `age <= 40` and I do not need to repeat the lower bound.
- The bands in the question (under 25, 25-40, 41-60, above 60) cover whole-number ages with no gaps. I sort bands by the youngest age in each so they appear in natural order, not alphabetical.
- Different databases have their own age/date-difference functions (see the alternatives in the SQL block).
**Example:** Today is fixed at 2026-10-21 in the sample so the result never changes; in real life replace it with `CURRENT_DATE`. Bala was born 2001-10-22 so he is still 24 (birthday tomorrow); Chitra was born 2001-10-21 and just turned 25.
**Sample data:**

*customers*

| customer_id | name | dob |
|---|---|---|
| 1 | Asha | 2003-05-14 |
| 2 | Bala | 2001-10-22 |
| 3 | Chitra | 2001-10-21 |
| 4 | Dev | 1990-01-01 |
| 5 | Esha | 1985-10-21 |
| 6 | Farid | 1970-03-03 |
| 7 | Gita | 1965-10-22 |
| 8 | Hari | 1961-10-21 |
| 9 | Isha | NULL |

**SQL:**
```sql
WITH ages AS (
  SELECT customer_id,
         CAST(strftime('%Y', '2026-10-21') AS INTEGER) - CAST(strftime('%Y', dob) AS INTEGER)
         - (strftime('%m-%d', dob) > strftime('%m-%d', '2026-10-21')) AS age
  FROM customers
)
SELECT CASE WHEN age IS NULL THEN 'Unknown'
            WHEN age < 25  THEN 'Under 25'
            WHEN age <= 40 THEN '25-40'
            WHEN age <= 60 THEN '41-60'
            ELSE 'Above 60' END AS age_band,
       COUNT(*) AS customers
FROM ages
GROUP BY 1
ORDER BY MIN(COALESCE(age, 999));

-- Age alternatives (not run here / from memory):
-- PostgreSQL : DATE_PART('year', AGE(CURRENT_DATE, dob))
-- MySQL      : TIMESTAMPDIFF(YEAR, dob, CURDATE())
-- SQL Server : DATEDIFF(year, dob, GETDATE()) is WRONG near birthdays; adjust with a CASE as above, or use DATEDIFF(day, dob, GETDATE()) / 365.25
```
**Output:**

| age_band | customers |
|---|---|
| Under 25 | 2 |
| 25-40 | 2 |
| 41-60 | 3 |
| Above 60 | 1 |
| Unknown | 1 |

**pandas equivalent:**
```python
# the tables above are DataFrames with the same names and columns
import pandas as pd
asof = pd.Timestamp('2026-10-21')
dob = pd.to_datetime(customers.dob)
age = asof.year - dob.dt.year - ((dob.dt.month * 100 + dob.dt.day) > (asof.month * 100 + asof.day))
def band(a):
    if pd.isna(a): return 'Unknown'
    if a < 25: return 'Under 25'
    if a <= 40: return '25-40'
    if a <= 60: return '41-60'
    return 'Above 60'
c = pd.DataFrame({'age': age, 'age_band': age.map(band)})
c['sort_age'] = c.age.fillna(999)
res = (c.groupby('age_band').agg(customers=('age_band', 'size'), s=('sort_age', 'min'))
       .sort_values('s').reset_index()[['age_band', 'customers']])
# Output (matches the SQL):
# age_band  customers
# Under 25          2
#    25-40          2
#    41-60          3
# Above 60          1
#  Unknown          1
```
**Edge cases:** NULL dob goes to 'Unknown' (otherwise it falls into 'Above 60' via ELSE: a classic bug). Birthdays exactly today count as the new age (Chitra, Esha, Hari). Wrong or future dates of birth (e.g. 1900-01-01 as a default) produce absurd ages: check with MIN/MAX first. Bands with zero customers do not appear unless you build them in a small bands table.
**Likely follow-ups:**
- Why not `DATEDIFF(year, ...)`? In SQL Server it counts calendar-year boundaries crossed, so someone born 2001-12-31 is 'one year old' on 2002-01-01.
- How do you keep the bands in one place? A `age_bands(min_age, max_age, label)` table joined on `age BETWEEN min_age AND max_age`.
- Share of customers per band? Divide by `SUM(COUNT(*)) OVER ()` like Q24.
**Common mistakes:** Subtracting only the years; forgetting NULL dob; writing overlapping or gapped bands (`BETWEEN 25 AND 40` then `BETWEEN 41 AND 60` is fine for whole-number ages but breaks for decimals like 40.5); ordering bands alphabetically ('25-40' before 'Under 25').

### Q28 ⭐⭐ 🟢 Retail: `inventory` has product_id, stock_qty and reorder_level. List products that need re-ordering.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** A simple row-level comparison between two columns, and awareness that NULLs silently fall out of a comparison.
**Say this in the interview:** "A product needs re-ordering when stock is at or below its re-order level. I compare the two columns on the same row, join to products to show names, and sort by how short we are. I also run a second check for rows with a missing stock or level, because NULL comparisons drop them without warning."
**Explain simply:**
- **Re-order level** = the stock quantity that triggers a new purchase order. 'Needs re-ordering' normally means stock is **at or below** that level, so use `<=` not `<`.
- You compare two columns of the same row: `stock_qty <= reorder_level`. No GROUP BY is needed.
- **Shortfall** = `reorder_level - stock_qty` shows how urgent each item is.
- `NULL <= 20` is not true and not false, it is unknown, so such rows are skipped. The second query lists them so no product is ignored by accident.
**Example:** Marker: stock 0, level 25 -> shortfall 25 (urgent). Stapler: stock 30, level 30 -> exactly at the level, so it is listed with shortfall 0.
**Sample data:**

*products*

| product_id | product_name |
|---|---|
| 1 | Pen |
| 2 | Notebook |
| 3 | Stapler |
| 4 | Folder |
| 5 | Marker |
| 6 | Tape |

*inventory*

| product_id | stock_qty | reorder_level |
|---|---|---|
| 1 | 120 | 100 |
| 2 | 40 | 50 |
| 3 | 30 | 30 |
| 4 | NULL | 20 |
| 5 | 0 | 25 |
| 6 | 15 | NULL |

**SQL:**
```sql
SELECT p.product_id, p.product_name, i.stock_qty, i.reorder_level,
       i.reorder_level - i.stock_qty AS shortfall
FROM inventory i
JOIN products p ON p.product_id = i.product_id
WHERE i.stock_qty <= i.reorder_level
ORDER BY shortfall DESC, p.product_name;

SELECT p.product_id, p.product_name, i.stock_qty, i.reorder_level
FROM inventory i
JOIN products p ON p.product_id = i.product_id
WHERE i.stock_qty IS NULL OR i.reorder_level IS NULL
ORDER BY p.product_id;
```
**Output:**

*Products to re-order*

| product_id | product_name | stock_qty | reorder_level | shortfall |
|---|---|---|---|---|
| 5 | Marker | 0 | 25 | 25 |
| 2 | Notebook | 40 | 50 | 10 |
| 3 | Stapler | 30 | 30 | 0 |

*Data-quality check: rows the first query cannot judge*

| product_id | product_name | stock_qty | reorder_level |
|---|---|---|---|
| 4 | Folder | NULL | 20 |
| 6 | Tape | 15 | NULL |

**pandas equivalent:**
```python
# the tables above are DataFrames with the same names and columns
import pandas as pd
# Products to re-order
m = inventory.merge(products, on='product_id')
m['shortfall'] = m.reorder_level - m.stock_qty
res = (m[m.stock_qty <= m.reorder_level]
       [['product_id', 'product_name', 'stock_qty', 'reorder_level', 'shortfall']]
       .sort_values(['shortfall', 'product_name'], ascending=[False, True]).reset_index(drop=True))
# Output (matches the SQL):
#  product_id product_name  stock_qty  reorder_level  shortfall
#           5       Marker        0.0           25.0       25.0
#           2     Notebook       40.0           50.0       10.0
#           3      Stapler       30.0           30.0        0.0

# Data-quality check: rows the first query cannot judge
m = inventory.merge(products, on='product_id')
res = (m[m.stock_qty.isna() | m.reorder_level.isna()]
       [['product_id', 'product_name', 'stock_qty', 'reorder_level']]
       .sort_values('product_id').reset_index(drop=True))
# Output (matches the SQL):
#  product_id product_name  stock_qty  reorder_level
#           4       Folder        NaN           20.0
#           6         Tape       15.0            NaN
```
**Edge cases:** Stock exactly equal to the level counts (Stapler). NULL stock or level (Folder, Tape) is excluded by the first query and caught by the second. Negative stock (returns, system errors) would also be listed: usually correct, but flag it. A product with no row in `inventory` at all is invisible to both queries; use a LEFT JOIN from `products` to catch it. With several warehouses, sum stock per product first.
**Likely follow-ups:**
- How many units to order? Often target stock minus current stock, or a fixed order quantity; the shortfall is only a starting point.
- Products with several warehouse rows? `GROUP BY product_id` and compare `SUM(stock_qty)` with the level in a `HAVING` clause.
- Treat NULL stock as 0? `COALESCE(i.stock_qty, 0) <= i.reorder_level`, only if the business confirms that blank means none.
**Common mistakes:** Using `<` and missing items exactly at the level; assuming NULL rows are 'fine'; comparing a column to a typed number instead of the row's own reorder level; forgetting that stock stored as text compares alphabetically ('100' < '20').

### Q29 ⭐⭐ 🟡 E-commerce (food delivery): Calculate the cancellation rate per city and show cities above the company average.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Group-level rate compared with an overall figure: a subquery (or CTE) for the company average, and being clear about what 'average' means.
**Say this in the interview:** "I compute the cancellation rate per city with conditional counting, then compare each city to the company rate, which I calculate over all orders in a subquery. I filter on that comparison. I use the overall rate, not the average of the city rates, because small cities would otherwise count as much as big ones."
**Explain simply:**
- **Cancellation rate** per city = cancelled orders in that city / all orders in that city x 100.
- The **company average** is the overall rate across every order. It is a single number computed once, in a **scalar subquery** (a subquery that returns one value).
- The average of the four city rates (31.25) is not the same as the overall rate (33.33) because cities have different volumes. Name your choice.
- A **CTE** (`WITH city AS (...)`) holds the per-city table so the final SELECT can filter on it.
**Example:** Company: 4 cancelled of 12 = 33.33%. Bengaluru 2 of 4 = 50% and Pune 1 of 2 = 50% are above it; Hyderabad 25% and Mumbai 0% are not.
**Sample data:**

*orders*

| order_id | city | status |
|---|---|---|
| 1 | Hyderabad | cancelled |
| 2 | Hyderabad | delivered |
| 3 | Hyderabad | delivered |
| 4 | Hyderabad | delivered |
| 5 | Bengaluru | cancelled |
| 6 | Bengaluru | cancelled |
| 7 | Bengaluru | delivered |
| 8 | Bengaluru | delivered |
| 9 | Pune | cancelled |
| 10 | Pune | delivered |
| 11 | Mumbai | delivered |
| 12 | Mumbai | delivered |

**SQL:**
```sql
WITH city AS (
  SELECT city,
         COUNT(*) AS orders,
         SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled
  FROM orders
  GROUP BY city
)
SELECT city, orders, cancelled,
       ROUND(100.0 * cancelled / orders, 1) AS cancel_pct,
       (SELECT ROUND(100.0 * SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*), 1)
        FROM orders) AS company_pct
FROM city
WHERE 1.0 * cancelled / orders >
      (SELECT 1.0 * SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*) FROM orders)
ORDER BY cancel_pct DESC, city;
```
**Output:**

| city | orders | cancelled | cancel_pct | company_pct |
|---|---|---|---|---|
| Bengaluru | 4 | 2 | 50.0 | 33.3 |
| Pune | 2 | 1 | 50.0 | 33.3 |

**pandas equivalent:**
```python
# the tables above are DataFrames with the same names and columns
import pandas as pd
o = orders.assign(is_c=(orders.status == 'cancelled').astype(int))
city = o.groupby('city', as_index=False).agg(orders=('order_id', 'count'), cancelled=('is_c', 'sum'))
overall = o.is_c.mean()
city['cancel_pct'] = (100 * city.cancelled / city.orders).round(1)
city['company_pct'] = round(100 * overall, 1)
res = (city[city.cancelled / city.orders > overall]
       .sort_values(['cancel_pct', 'city'], ascending=[False, True])
       [['city', 'orders', 'cancelled', 'cancel_pct', 'company_pct']].reset_index(drop=True))
# Output (matches the SQL):
#      city  orders  cancelled  cancel_pct  company_pct
# Bengaluru       4          2        50.0         33.3
#      Pune       2          1        50.0         33.3
```
**Edge cases:** Compare the unrounded values (rounding first can push a city across the line). A city with 1 order and 1 cancellation shows 100%: small samples are noisy, so mention a minimum order count (`HAVING COUNT(*) >= 20`). NULL city rows form their own group. Cities exactly equal to the average are excluded (strictly above). If status is NULL, decide whether it belongs in the denominator.
**Likely follow-ups:**
- Average of city rates instead? `AVG(cancel_pct)` over the CTE gives 31.25 here; say why you prefer the overall rate.
- Can you do it without a subquery? Yes, with a window: `AVG(...) OVER ()` on the per-order flag inside a CTE, then filter in an outer query.
- Why a `1.0 *` in the WHERE? Without it some databases do integer division and the comparison is wrong.
**Common mistakes:** Comparing a city's rate with the average of rates; integer division making every rate 0; putting the aggregate comparison in `WHERE` (it belongs in `HAVING` when no CTE is used); no minimum volume, so tiny cities top the list.

### Q30 ⭐⭐ 🟡 HR/payroll: Monthly payroll cost = salary + bonus, where bonus can be NULL. Show total payroll cost per month for 2025.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** The NULL trap in arithmetic: `salary + NULL` is NULL, so bonus must be wrapped in COALESCE. Plus month grouping and a clean date filter.
**Say this in the interview:** "Any number plus NULL is NULL, so I use COALESCE(bonus, 0) before adding, otherwise people without a bonus vanish from the total. I filter 2025 with a date range on the raw column and group by year-month."
**Explain simply:**
- **NULL** = value not filled in. `50000 + NULL` gives NULL, and `SUM` skips NULLs, so employees with no bonus would silently drop out of payroll.
- `COALESCE(bonus, 0)` returns the bonus, or 0 if it is NULL: it fixes this at the row level, before the SUM.
- The year filter is written as `>= '2025-01-01' AND < '2026-01-01'`, which is correct even if the column holds timestamps and lets an index be used.
- Grouping by month means turning each date into a 'YYYY-MM' label. The function differs by database (see alternatives).
**Example:** January: Employee 1 earns 50,000 + 5,000 bonus, Employee 2 earns 60,000 with no bonus: correct cost 115,000. The naive `SUM(salary + bonus)` says 55,000 because Employee 2 disappears; in February (no bonuses at all) it returns NULL.
**Sample data:** (each row = one employee's pay for one month; 2024 and 2026 rows are there to prove the filter)

*payroll*

| emp_id | pay_date | salary | bonus |
|---|---|---|---|
| 1 | 2025-01-31 | 50000 | 5000 |
| 2 | 2025-01-31 | 60000 | NULL |
| 1 | 2025-02-28 | 50000 | NULL |
| 2 | 2025-02-28 | 60000 | NULL |
| 1 | 2025-03-31 | 52000 | 2000 |
| 2 | 2025-03-31 | 60000 | 3000 |
| 1 | 2024-12-31 | 48000 | 1000 |
| 3 | 2026-01-31 | 40000 | NULL |

**SQL:**
```sql
SELECT strftime('%Y-%m', pay_date) AS pay_month,
       SUM(salary + COALESCE(bonus, 0)) AS payroll_cost,
       SUM(salary + bonus) AS naive_wrong
FROM payroll
WHERE pay_date >= '2025-01-01' AND pay_date < '2026-01-01'
GROUP BY strftime('%Y-%m', pay_date)
ORDER BY pay_month;

-- Month label alternatives (not run here / from memory):
-- PostgreSQL : TO_CHAR(pay_date, 'YYYY-MM')   or DATE_TRUNC('month', pay_date)
-- MySQL      : DATE_FORMAT(pay_date, '%Y-%m')
-- SQL Server : FORMAT(pay_date, 'yyyy-MM')   or EOMONTH(pay_date)
-- NULL replacement: COALESCE works everywhere; ISNULL (SQL Server), IFNULL (MySQL/SQLite)
```
**Output:**

| pay_month | payroll_cost | naive_wrong |
|---|---|---|
| 2025-01 | 115000 | 55000 |
| 2025-02 | 110000 | NULL |
| 2025-03 | 117000 | 117000 |

**pandas equivalent:**
```python
# the tables above are DataFrames with the same names and columns
import pandas as pd
p = payroll[(payroll.pay_date >= '2025-01-01') & (payroll.pay_date < '2026-01-01')].copy()
p['pay_month'] = p.pay_date.str[:7]
p['cost'] = p.salary + p.bonus.fillna(0)
p['naive'] = p.salary + p.bonus            # NaN when bonus is missing
res = (p.groupby('pay_month', as_index=False)
       .agg(payroll_cost=('cost', 'sum'), naive_wrong=('naive', lambda s: s.sum(min_count=1)))
       .sort_values('pay_month').reset_index(drop=True))
# Output (matches the SQL):
# pay_month  payroll_cost  naive_wrong
#   2025-01      115000.0      55000.0
#   2025-02      110000.0          NaN
#   2025-03      117000.0     117000.0
```
**Edge cases:** A month where every bonus is NULL: the naive formula returns NULL, the COALESCE version is correct. Months with no payroll rows do not appear (build a calendar table to show them as 0). Salary itself NULL still makes that row's cost NULL: decide if that is a data error. Employer costs (PF, insurance) are not in 'salary + bonus' and the question's definition is used as given. If you store one row per employee-month, be careful not to double-count mid-month revisions.
**Likely follow-ups:**
- Cost per department per month? Join employees to payroll and group by `dept` and month.
- Month-on-month change? Use `LAG` on the monthly total (Part 9 covers it).
- Why `< '2026-01-01'` and not `BETWEEN ... AND '2025-12-31'`? Because a timestamp on 2025-12-31 at 10:00 would be missed by the BETWEEN.
**Common mistakes:** `SUM(salary + bonus)` without COALESCE; `COALESCE(SUM(...), 0)` instead of coalescing per row (wrong for mixed NULLs); `WHERE YEAR(pay_date) = 2025` on a big table (stops index use); grouping by month name only, which merges different years.

### Q31 ⭐⭐ 🟡 HR: Find employees who have taken no leave this year (`leaves`: emp_id, start_date, end_date).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Anti-join ('rows with no match') with NOT EXISTS, correct date-overlap logic for leave that crosses a year boundary, and the NOT IN / NULL trap.
**Say this in the interview:** "I use NOT EXISTS: keep employees for whom no leave row overlaps this year. Overlap means the leave starts on or before the end of the window and ends on or after the start, so leave that began on 28 December still counts. I avoid NOT IN because one NULL in the list makes it return nothing."
**Explain simply:**
- An **anti-join** finds rows in table A with no match in table B. In SQL: `NOT EXISTS`, or `LEFT JOIN ... WHERE b.key IS NULL`.
- **Overlap test** for a period [start, end] against a window [W1, W2]: `start <= W2 AND end >= W1`. This catches leave that starts in December and ends in January.
- 'Taken this year' is read as taken up to today (2026-10-21), so a future booking does not count. State this assumption. Today is fixed at 2026-10-21 in the sample so the result never changes; in real life replace it with `CURRENT_DATE`.
- `NOT IN (subquery)` returns no rows at all if the subquery contains a single NULL, which is shown as a second query below.
**Example:** Bala's leave ran 2025-12-28 to 2026-01-03, so he did take leave this year. Chitra's only leave was in 2025; Dev has none; Esha's leave starts in December (not yet taken): all three are listed.
**Sample data:** (the last leave row has a NULL emp_id, a typical data-entry slip)

*employees*

| emp_id | name |
|---|---|
| 1 | Asha |
| 2 | Bala |
| 3 | Chitra |
| 4 | Dev |
| 5 | Esha |

*leaves*

| emp_id | start_date | end_date |
|---|---|---|
| 1 | 2026-03-10 | 2026-03-12 |
| 2 | 2025-12-28 | 2026-01-03 |
| 3 | 2025-05-01 | 2025-05-05 |
| 5 | 2026-12-30 | 2027-01-02 |
| NULL | 2026-04-01 | 2026-04-02 |

**SQL:**
```sql
SELECT e.emp_id, e.name
FROM employees e
WHERE NOT EXISTS (
  SELECT 1 FROM leaves l
  WHERE l.emp_id = e.emp_id
    AND l.start_date <= '2026-10-21'   -- started on/before today
    AND l.end_date   >= '2026-01-01'   -- ended on/after 1 Jan
)
ORDER BY e.emp_id;

SELECT e.emp_id, e.name
FROM employees e
WHERE e.emp_id NOT IN (
  SELECT l.emp_id FROM leaves l
  WHERE l.start_date <= '2026-10-21' AND l.end_date >= '2026-01-01'
)
ORDER BY e.emp_id;
```
**Output:**

*Correct: NOT EXISTS*

| emp_id | name |
|---|---|
| 3 | Chitra |
| 4 | Dev |
| 5 | Esha |

*Trap: NOT IN with a NULL in the list returns nothing*

(no rows returned: empty result)

**pandas equivalent:**
```python
# the tables above are DataFrames with the same names and columns
import pandas as pd
# Correct: NOT EXISTS
l = leaves[(leaves.start_date <= '2026-10-21') & (leaves.end_date >= '2026-01-01')]
res = (employees[~employees.emp_id.isin(l.emp_id.dropna())]
       .sort_values('emp_id').reset_index(drop=True))
# Output (matches the SQL):
#  emp_id   name
#       3 Chitra
#       4    Dev
#       5   Esha
```
**Edge cases:** Leave crossing New Year (Bala) is caught by the overlap rule; a simple `start_date >= '2026-01-01'` would miss it. NULL `emp_id` in `leaves` breaks `NOT IN` (shown). Half-day leave, cancelled or rejected leave rows should be filtered by a status column if one exists. Employees who joined or left mid-year may need a different window. Dates stored as text must be ISO format (YYYY-MM-DD) for these comparisons.
**Likely follow-ups:**
- Same with a LEFT JOIN? `LEFT JOIN leaves l ON ... AND <overlap conditions> WHERE l.emp_id IS NULL`; keep the date conditions in the ON clause, not in WHERE.
- Which is faster, NOT EXISTS or LEFT JOIN? Usually the same plan; check with the database's execution-plan tool (EXPLAIN).
- How would you list people with the most leave days? See Q32.
**Common mistakes:** `NOT IN` on a column that can contain NULL; checking only `start_date` inside the year; putting the date filter in `WHERE` after a LEFT JOIN, which turns it into an inner join and loses the very rows you want.

### Q32 ⭐⭐ 🟡 HR: Calculate average leave days per employee per department and list employees who took more than 20 days.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Date difference with the inclusive +1, aggregating twice (per employee, then per department), and keeping zero-leave employees in the average.
**Say this in the interview:** "First I total leave days per employee: end minus start plus one, because both days count. I keep employees with no leave as zero so they are not left out of the average. Then I average those totals per department, and filter employees above 20 days."
**Explain simply:**
- **Inclusive days**: a leave from the 10th to the 12th is 3 days, not 2, so the formula is `end - start + 1`.
- Two levels of aggregation: first **per employee** (sum of their leaves), then **per department** (average of those totals). Doing the average directly on leave rows would give 'average per leave request', which is a different number.
- LEFT JOIN + `COALESCE(..., 0)` keeps people with no leave rows in the average. Dropping them inflates the average. State which one HR wants.
- I assume all rows in `leaves` belong to the year being analysed; add a year filter otherwise (see Q31).
**Example:** Asha took 10 + 12 = 22 days; Bala 5 days: HR average = 13.5. Sales: Chitra 26, Dev 3, Esha 0 -> 9.7.
**Sample data:**

*departments*

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Sales |
| 3 | IT |

*employees*

| emp_id | name | dept_id |
|---|---|---|
| 1 | Asha | 1 |
| 2 | Bala | 1 |
| 3 | Chitra | 2 |
| 4 | Dev | 2 |
| 5 | Esha | 2 |
| 6 | Farid | 3 |

*leaves*

| emp_id | start_date | end_date |
|---|---|---|
| 1 | 2026-02-01 | 2026-02-10 |
| 1 | 2026-06-01 | 2026-06-12 |
| 2 | 2026-03-01 | 2026-03-05 |
| 3 | 2026-01-05 | 2026-01-30 |
| 4 | 2026-04-01 | 2026-04-03 |
| 6 | 2026-05-10 | 2026-05-10 |

**SQL:**
```sql
WITH emp_days AS (
  SELECT e.emp_id, e.name, e.dept_id,
         COALESCE(SUM(CAST(julianday(l.end_date) - julianday(l.start_date) AS INTEGER) + 1), 0) AS leave_days
  FROM employees e
  LEFT JOIN leaves l ON l.emp_id = e.emp_id
  GROUP BY e.emp_id, e.name, e.dept_id
)
SELECT d.dept_name,
       COUNT(*) AS employees,
       SUM(x.leave_days) AS total_days,
       ROUND(AVG(x.leave_days), 1) AS avg_days_per_employee
FROM emp_days x
JOIN departments d ON d.dept_id = x.dept_id
GROUP BY d.dept_name
ORDER BY d.dept_name;

SELECT e.emp_id, e.name, d.dept_name,
       SUM(CAST(julianday(l.end_date) - julianday(l.start_date) AS INTEGER) + 1) AS leave_days
FROM employees e
JOIN leaves l ON l.emp_id = e.emp_id
JOIN departments d ON d.dept_id = e.dept_id
GROUP BY e.emp_id, e.name, d.dept_name
HAVING SUM(CAST(julianday(l.end_date) - julianday(l.start_date) AS INTEGER) + 1) > 20
ORDER BY leave_days DESC;

-- Day difference in other databases (not run here / from memory):
-- PostgreSQL : (end_date - start_date) + 1          (date minus date gives days)
-- MySQL      : DATEDIFF(end_date, start_date) + 1
-- SQL Server : DATEDIFF(day, start_date, end_date) + 1
```
**Output:**

*Average leave days per employee, by department*

| dept_name | employees | total_days | avg_days_per_employee |
|---|---|---|---|
| HR | 2 | 27 | 13.5 |
| IT | 1 | 1 | 1.0 |
| Sales | 3 | 29 | 9.7 |

*Employees with more than 20 leave days*

| emp_id | name | dept_name | leave_days |
|---|---|---|---|
| 3 | Chitra | Sales | 26 |
| 1 | Asha | HR | 22 |

**pandas equivalent:**
```python
# the tables above are DataFrames with the same names and columns
import pandas as pd
# Average leave days per employee, by department
l = leaves.copy()
l['days'] = (pd.to_datetime(l.end_date) - pd.to_datetime(l.start_date)).dt.days + 1
tot = l.groupby('emp_id').days.sum()
e = employees.copy()
e['leave_days'] = e.emp_id.map(tot).fillna(0).astype(int)
res = (e.merge(departments, on='dept_id').groupby('dept_name', as_index=False)
       .agg(employees=('emp_id', 'count'), total_days=('leave_days', 'sum'),
            avg_days_per_employee=('leave_days', 'mean')))
res['avg_days_per_employee'] = res.avg_days_per_employee.round(1)
res = res.sort_values('dept_name').reset_index(drop=True)
# Output (matches the SQL):
# dept_name  employees  total_days  avg_days_per_employee
#        HR          2          27                   13.5
#        IT          1           1                    1.0
#     Sales          3          29                    9.7

# Employees with more than 20 leave days
t = (l.groupby('emp_id', as_index=False).days.sum().rename(columns={'days': 'leave_days'})
     .merge(employees, on='emp_id').merge(departments, on='dept_id'))
res = (t[t.leave_days > 20][['emp_id', 'name', 'dept_name', 'leave_days']]
       .sort_values('leave_days', ascending=False).reset_index(drop=True))
# Output (matches the SQL):
#  emp_id   name dept_name  leave_days
#       3 Chitra     Sales          26
#       1   Asha        HR          22
```
**Edge cases:** Employees with no leave (Esha) count as 0 in the average; excluding them would make Sales (26+3)/2 = 14.5. Leave spanning two years needs splitting at the year end. Overlapping or duplicate leave rows double-count days. Public holidays/weekends inside a leave are counted unless you use a working-day calendar. NULL `end_date` (ongoing leave) gives NULL days: decide how to treat it. `HAVING` filters after grouping; `WHERE` cannot filter on a SUM.
**Likely follow-ups:**
- Why HAVING and not WHERE? `WHERE` runs before grouping so the sum does not exist yet; `HAVING` runs after.
- Why not average the leave rows directly? That gives average days per request (Asha's rows: 10 and 12), not per person.
- Leave days by type (sick, casual)? Add `leave_type` to the GROUP BY.
**Common mistakes:** Forgetting `+ 1`; averaging per leave request instead of per employee; inner-joining and dropping people with no leave; using `WHERE SUM(...) > 20`, which is invalid.

### Q33 ⭐⭐ 🟡 HR: From `attendance` (clock_in, clock_out), find employees whose overtime exceeded 40 hours in a month (standard day = 9 hours).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Time arithmetic on timestamps, per-day logic before the monthly total, and a clean threshold filter with HAVING.
**Say this in the interview:** "For each day I work out hours worked from clock-out minus clock-in, then overtime is hours above 9, never below zero. I add up overtime per employee per month and keep those above 40 with HAVING. The 'never below zero' step matters: a short day should not cancel out a long one."
**Explain simply:**
- **Hours worked** = clock-out minus clock-in. SQLite has no time-subtraction operator, so I convert both to seconds with `strftime('%s', ...)` and divide by 3600. Other databases have their own function (see alternatives).
- **Overtime** for a day = `MAX(0, hours - 9)`. In SQLite `MAX(a, b)` with two values returns the bigger one; PostgreSQL/MySQL use `GREATEST`, SQL Server uses a CASE.
- Do the daily step first, then `SUM` per employee-month. If you subtract 9 hours from the monthly total instead, short days cancel long days, which is not what overtime pay means.
- `HAVING SUM(...) > 40` keeps only groups above the threshold (`WHERE` cannot see sums).
**Example:** Employee 3 in October works 15 days of 12 hours (+3 each = 45 overtime hours) and 5 days of 6 hours. Per-day logic: 45 hours -> listed. Wrong monthly-net logic: 45 - 15 = 30 -> missed. Employee 1 in September has exactly 40 hours: not above 40, so not listed.
**Sample data:** (the real test set has 84 rows: Employee 1 works 11-hour days (20 days in September, 22 in October); Employee 2 works 10.5-hour days (22 days in October); Employee 3 as in the example. Only the first rows are shown to keep the page short. Clock times are text 'YYYY-MM-DD HH:MM'.)

*attendance* (first 6 of 84 rows)

| emp_id | work_date | clock_in | clock_out |
|---|---|---|---|
| 1 | 2026-09-01 | 2026-09-01 09:00 | 2026-09-01 20:00 |
| 1 | 2026-09-02 | 2026-09-02 09:00 | 2026-09-02 20:00 |
| 1 | 2026-09-03 | 2026-09-03 09:00 | 2026-09-03 20:00 |
| 1 | 2026-09-04 | 2026-09-04 09:00 | 2026-09-04 20:00 |
| 1 | 2026-09-07 | 2026-09-07 09:00 | 2026-09-07 20:00 |
| 1 | 2026-09-08 | 2026-09-08 09:00 | 2026-09-08 20:00 |

**SQL:**
```sql
WITH daily AS (
  SELECT emp_id, work_date,
         (strftime('%s', clock_out) - strftime('%s', clock_in)) / 3600.0 AS hours_worked
  FROM attendance
  WHERE clock_out IS NOT NULL
)
SELECT emp_id,
       strftime('%Y-%m', work_date) AS month,
       ROUND(SUM(MAX(hours_worked - 9, 0)), 2) AS overtime_hours
FROM daily
GROUP BY emp_id, strftime('%Y-%m', work_date)
HAVING SUM(MAX(hours_worked - 9, 0)) > 40
ORDER BY overtime_hours DESC, emp_id;

-- Other dialects (not run here / from memory):
-- PostgreSQL : EXTRACT(EPOCH FROM (clock_out - clock_in)) / 3600.0 ;  GREATEST(hours - 9, 0) ;  TO_CHAR(work_date,'YYYY-MM')
-- MySQL      : TIMESTAMPDIFF(MINUTE, clock_in, clock_out) / 60.0 ;  GREATEST(hours - 9, 0) ;  DATE_FORMAT(work_date,'%Y-%m')
-- SQL Server : DATEDIFF(MINUTE, clock_in, clock_out) / 60.0 ;  CASE WHEN h > 9 THEN h - 9 ELSE 0 END
```
**Output:**

| emp_id | month | overtime_hours |
|---|---|---|
| 3 | 2026-10 | 45.0 |
| 1 | 2026-10 | 44.0 |

**pandas equivalent:**
```python
# the tables above are DataFrames with the same names and columns
import pandas as pd
a = attendance.dropna(subset=['clock_out']).copy()
a['hours'] = (pd.to_datetime(a.clock_out) - pd.to_datetime(a.clock_in)).dt.total_seconds() / 3600
a['ot'] = (a.hours - 9).clip(lower=0)
a['month'] = a.work_date.str[:7]
g = a.groupby(['emp_id', 'month'], as_index=False).ot.sum().rename(columns={'ot': 'overtime_hours'})
res = (g[g.overtime_hours > 40].assign(overtime_hours=lambda x: x.overtime_hours.round(2))
       .sort_values(['overtime_hours', 'emp_id'], ascending=[False, True]).reset_index(drop=True))
# Output (matches the SQL):
#  emp_id   month  overtime_hours
#       3 2026-10            45.0
#       1 2026-10            44.0
```
**Edge cases:** Missing clock-out (forgot to swipe out) is excluded, which understates overtime: report these separately. Night shifts that end after midnight work because full timestamps are used; if only times are stored, add a day when out < in. A month boundary: group by the work date's month, not the clock-out month. Exactly 40 is not 'exceeded 40' (Employee 1, September). Lunch breaks, weekends and public holidays may need separate rules from HR.
**Likely follow-ups:**
- Why use 3600.0 and not 3600? Integer division would round hours down in many databases.
- Should weekend work count fully as overtime? A business rule: add a CASE on the weekday if so.
- How to see the monthly total for everyone, not just above 40? Remove the HAVING line.
**Common mistakes:** Taking (total hours - 9 x days) for the month so shorts cancel longs; using `WHERE` instead of `HAVING` for the sum; forgetting NULL clock-outs; integer division on minutes; grouping by employee only and mixing months.

### Q34 ⭐⭐ 🟡 HR: `salary_history` has emp_id, effective_date and salary. Calculate each employee's hike percentage between their last two revisions.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Using LAG (or ROW_NUMBER) to look at the previous row within each employee and computing a percentage change correctly.
**Say this in the interview:** "I order each employee's salary revisions by date, use LAG to bring in the previous salary on the same row, and mark the latest revision with ROW_NUMBER descending. Then I keep only the latest row that has a previous salary and compute (new - old) / old times 100. Employees with only one revision have no hike to report."
**Explain simply:**
- **LAG(salary)** looks one row back inside the group; `PARTITION BY emp_id ORDER BY effective_date` makes the group and the order.
- **ROW_NUMBER() ... DESC** = 1 for the newest revision of each employee, so I can keep just the latest hike.
- **Hike %** = (new salary - old salary) / old salary x 100. Dividing by the old salary matters: 40,000 to 44,000 is 10%, not 9.1%.
- An employee with a single row has `LAG` = NULL; the filter `prev_salary IS NOT NULL` drops them (they have no 'last two revisions').
**Example:** Employee 1: 44,000 -> 48,400 = 10.0%. Employee 5 had a pay cut: 66,000 -> 64,000 = -3.0%. Employee 4 got a revision with no change: 0.0%.
**Sample data:**

*salary_history*

| emp_id | effective_date | salary |
|---|---|---|
| 1 | 2023-04-01 | 40000 |
| 1 | 2024-04-01 | 44000 |
| 1 | 2025-04-01 | 48400 |
| 2 | 2024-07-01 | 50000 |
| 2 | 2025-07-01 | 56000 |
| 3 | 2025-01-01 | 30000 |
| 4 | 2024-01-01 | 70000 |
| 4 | 2025-01-01 | 70000 |
| 5 | 2023-01-01 | 60000 |
| 5 | 2024-01-01 | 66000 |
| 5 | 2025-01-01 | 64000 |

**SQL:**
```sql
WITH h AS (
  SELECT emp_id, effective_date, salary,
         LAG(salary) OVER (PARTITION BY emp_id ORDER BY effective_date) AS prev_salary,
         ROW_NUMBER() OVER (PARTITION BY emp_id ORDER BY effective_date DESC) AS rn
  FROM salary_history
)
SELECT emp_id, effective_date AS last_revision, prev_salary, salary AS new_salary,
       ROUND(100.0 * (salary - prev_salary) / prev_salary, 1) AS hike_pct
FROM h
WHERE rn = 1 AND prev_salary IS NOT NULL
ORDER BY emp_id;
```
**Output:**

| emp_id | last_revision | prev_salary | new_salary | hike_pct |
|---|---|---|---|---|
| 1 | 2025-04-01 | 44000 | 48400 | 10.0 |
| 2 | 2025-07-01 | 50000 | 56000 | 12.0 |
| 4 | 2025-01-01 | 70000 | 70000 | 0.0 |
| 5 | 2025-01-01 | 66000 | 64000 | -3.0 |

**pandas equivalent:**
```python
# the tables above are DataFrames with the same names and columns
import pandas as pd
h = salary_history.sort_values(['emp_id', 'effective_date']).copy()
h['prev_salary'] = h.groupby('emp_id').salary.shift(1)
h['rn'] = h.groupby('emp_id').cumcount(ascending=False) + 1
x = h[(h.rn == 1) & h.prev_salary.notna()].copy()
x['hike_pct'] = (100.0 * (x.salary - x.prev_salary) / x.prev_salary).round(1)
res = (x.rename(columns={'effective_date': 'last_revision', 'salary': 'new_salary'})
       [['emp_id', 'last_revision', 'prev_salary', 'new_salary', 'hike_pct']]
       .sort_values('emp_id').reset_index(drop=True))
# Output (matches the SQL):
#  emp_id last_revision  prev_salary  new_salary  hike_pct
#       1    2025-04-01      44000.0       48400      10.0
#       2    2025-07-01      50000.0       56000      12.0
#       4    2025-01-01      70000.0       70000       0.0
#       5    2025-01-01      66000.0       64000      -3.0
```
**Edge cases:** Single-revision employee (3) is excluded. Two revisions on the same date make 'previous' ambiguous: add a tie-breaker to the ORDER BY. Zero previous salary would divide by zero (use `NULLIF(prev_salary, 0)`). Pay cuts show as negative. Unsorted or back-dated entries are handled because ordering is by `effective_date`, not by insertion order. Revisions that are not hikes (e.g. role changes with equal pay) still appear.
**Likely follow-ups:**
- Hike for every revision, not just the last? Drop `rn = 1` and keep `prev_salary IS NOT NULL`.
- Without window functions? Self-join each row to the previous one (the max earlier date); longer and slower.
- Annualised growth between first and last? Use `FIRST_VALUE`/`LAST_VALUE` or the first and last rows, then a CAGR formula.
**Common mistakes:** Dividing by the new salary; using `MAX(effective_date)` and `MIN` instead of the last two rows; forgetting `PARTITION BY` so LAG crosses from one employee to the next; integer division (`(48400-44000)/44000` = 0).

### Q35 ⭐⭐ 🟡 HR: Show the number of direct reports per manager and list managers with more than 5.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Counting rows by a foreign key, joining a table to itself to get the manager's name, and HAVING.
**Say this in the interview:** "Each employee row stores their manager's id, so direct reports are just a count of employees grouped by manager_id. I join the table to itself once to show the manager's name, and use HAVING COUNT(*) > 5 to keep the large teams."
**Explain simply:**
- A **direct report** is someone whose `manager_id` equals the manager's `emp_id`. A manager and the people they manage live in the same table.
- A **self-join** joins the table to itself under two aliases (`e` for the employee, `m` for the manager): the same table playing two roles.
- `GROUP BY manager` then `COUNT(*)` gives team size. `HAVING` filters groups after counting (`WHERE` cannot filter on a count).
- Only direct reports are counted; 'everyone below' (indirect reports) needs a recursive query (Part 10).
**Example:** Rohan (emp 2) has 6 direct reports: Tarun, Uma, Vikram, Wasim, Xena, Yash. Sana has 3. Rohan is the only manager above 5.
**Sample data:**

*employees*

| emp_id | name | manager_id |
|---|---|---|
| 1 | Meera | NULL |
| 2 | Rohan | 1 |
| 3 | Sana | 1 |
| 4 | Tarun | 2 |
| 5 | Uma | 2 |
| 6 | Vikram | 2 |
| 7 | Wasim | 2 |
| 8 | Xena | 2 |
| 9 | Yash | 2 |
| 10 | Zoya | 3 |
| 11 | Aman | 3 |
| 12 | Bina | 3 |
| 13 | Chetan | 4 |

**SQL:**
```sql
SELECT m.emp_id AS manager_id, m.name AS manager, COUNT(*) AS direct_reports
FROM employees e
JOIN employees m ON m.emp_id = e.manager_id
GROUP BY m.emp_id, m.name
ORDER BY direct_reports DESC, m.name;

SELECT m.emp_id AS manager_id, m.name AS manager, COUNT(*) AS direct_reports
FROM employees e
JOIN employees m ON m.emp_id = e.manager_id
GROUP BY m.emp_id, m.name
HAVING COUNT(*) > 5
ORDER BY direct_reports DESC;
```
**Output:**

*Direct reports per manager (everyone)*

| manager_id | manager | direct_reports |
|---|---|---|
| 2 | Rohan | 6 |
| 3 | Sana | 3 |
| 1 | Meera | 2 |
| 4 | Tarun | 1 |

*Managers with more than 5 direct reports*

| manager_id | manager | direct_reports |
|---|---|---|
| 2 | Rohan | 6 |

**pandas equivalent:**
```python
# the tables above are DataFrames with the same names and columns
import pandas as pd
# Direct reports per manager (everyone)
m = employees.merge(employees, left_on='manager_id', right_on='emp_id', suffixes=('', '_mgr'))
res = (m.groupby(['emp_id_mgr', 'name_mgr'], as_index=False).size()
       .rename(columns={'emp_id_mgr': 'manager_id', 'name_mgr': 'manager', 'size': 'direct_reports'})
       .sort_values(['direct_reports', 'manager'], ascending=[False, True]).reset_index(drop=True))
# Output (matches the SQL):
#  manager_id manager  direct_reports
#           2   Rohan               6
#           3    Sana               3
#           1   Meera               2
#           4   Tarun               1

# Managers with more than 5 direct reports
res = res[res.direct_reports > 5].reset_index(drop=True)
# Output (matches the SQL):
#  manager_id manager  direct_reports
#           2   Rohan               6
```
**Edge cases:** Employees with NULL manager_id (the CEO) drop out of the inner JOIN, which is fine because they are nobody's report. People with zero reports never appear; use a LEFT JOIN from `employees m` to `employees e` with `COUNT(e.emp_id)` if you want 0s. 'More than 5' means 6 or more. Two managers with the same name are separated by grouping on `emp_id`. Inactive employees may need `WHERE e.left_date IS NULL`.
**Likely follow-ups:**
- Include managers with zero reports? Start from `employees m LEFT JOIN employees e ON e.manager_id = m.emp_id`, count `e.emp_id`, and filter to people who manage someone only if needed.
- Total team size including indirect reports? Recursive CTE (Part 10).
- Span of control analysis? Compare the team-size distribution across departments; a very large span (over about 8-10) is often a talk-point, but that is a rule of thumb, not a standard.
**Common mistakes:** Grouping by name only; using `WHERE COUNT(*) > 5`; counting the manager as their own report; forgetting that the join must connect `e.manager_id` to `m.emp_id` (not `e.emp_id`).

### Q36 ⭐⭐ 🟡 HR/recruitment: From `applications` (applied_date, offer_date, source), find the average time-to-offer by sourcing channel (referral, portal, agency).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Date difference per row, averaging only rows that have an offer (NULLs), and grouping by channel.
**Say this in the interview:** "For each application I take offer date minus applied date in days, and average it by source channel. Applications that never got an offer have a NULL offer date, so they drop out of the average automatically, but I count them separately so the reader sees how many offers each average is based on."
**Explain simply:**
- **Time-to-offer** = days between applying and receiving an offer. It is a core recruiting metric: shorter means you are less likely to lose the candidate to another company.
- `AVG` ignores NULLs. A NULL offer date makes the day-difference NULL, so no-offer candidates are not counted as zero days.
- Always show how many offers sit behind each average: an average from 2 offers is weak evidence.
- `COUNT(offer_date)` counts offers (non-NULL); `COUNT(*)` counts all applications.
**Example:** Referral offers took 7 and 10 days: average 8.5. Portal: 28 and 35 days: 31.5. Agency: 15 and 20 days: 17.5. Walk-in has no offers, so its average is NULL.
**Sample data:**

*applications*

| app_id | source | applied_date | offer_date |
|---|---|---|---|
| 1 | referral | 2026-01-05 | 2026-01-12 |
| 2 | referral | 2026-01-10 | 2026-01-20 |
| 3 | referral | 2026-01-15 | NULL |
| 4 | portal | 2026-01-02 | 2026-01-30 |
| 5 | portal | 2026-01-08 | 2026-02-12 |
| 6 | portal | 2026-01-09 | NULL |
| 7 | portal | 2026-01-11 | NULL |
| 8 | agency | 2026-01-03 | 2026-01-18 |
| 9 | agency | 2026-01-07 | 2026-01-27 |
| 10 | walk-in | 2026-01-14 | NULL |

**SQL:**
```sql
SELECT source,
       COUNT(*) AS applications,
       COUNT(offer_date) AS offers,
       ROUND(AVG(julianday(offer_date) - julianday(applied_date)), 1) AS avg_days_to_offer
FROM applications
GROUP BY source
ORDER BY source;

-- Day difference in other databases (not run here / from memory):
-- PostgreSQL : AVG(offer_date - applied_date)          MySQL : AVG(DATEDIFF(offer_date, applied_date))
-- SQL Server : AVG(DATEDIFF(day, applied_date, offer_date) * 1.0)   -- the 1.0 avoids integer averaging
```
**Output:**

| source | applications | offers | avg_days_to_offer |
|---|---|---|---|
| agency | 2 | 2 | 17.5 |
| portal | 4 | 2 | 31.5 |
| referral | 3 | 2 | 8.5 |
| walk-in | 1 | 0 | NULL |

**pandas equivalent:**
```python
# the tables above are DataFrames with the same names and columns
import pandas as pd
a = applications.copy()
a['days'] = (pd.to_datetime(a.offer_date) - pd.to_datetime(a.applied_date)).dt.days
res = (a.groupby('source', as_index=False)
       .agg(applications=('app_id', 'count'), offers=('offer_date', 'count'),
            avg_days_to_offer=('days', 'mean')))
res['avg_days_to_offer'] = res.avg_days_to_offer.round(1)
res = res.sort_values('source').reset_index(drop=True)
# Output (matches the SQL):
#   source  applications  offers  avg_days_to_offer
#   agency             2       2               17.5
#   portal             4       2               31.5
# referral             3       2                8.5
#  walk-in             1       0                NaN
```
**Edge cases:** No-offer rows are excluded from the average automatically; walk-in shows NULL because it has no offers. Offer date before applied date is a data error: check `WHERE offer_date < applied_date`. Duplicate applications by the same candidate skew counts. Averages hide outliers: one 120-day offer pulls the mean up; a median is often more honest. Mixed source spellings ('Referral', 'referral ') split groups.
**Likely follow-ups:**
- Median instead of average? PostgreSQL: `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY days)`; MySQL/SQLite have no built-in median, so use window functions (not run here).
- Offer rate by source? `100.0 * COUNT(offer_date) / COUNT(*)`: referral 66.7%, portal 50%, agency 100%, walk-in 0% in this data.
- Why not average days to hire instead? That depends on a later milestone (joined date); say which stage the business tracks.
**Common mistakes:** Treating missing offers as 0 days (e.g. `COALESCE(offer_date, applied_date)`), which drags the average down; averaging in SQL Server with integer day differences; forgetting to show the number of offers; subtracting date strings in a database that does not support it.

### Q37 ⭐⭐ 🟡 HR: Split leavers into voluntary and involuntary using exit_reason, per department, with percentages.
**Asked at:** commonly asked; attrition-by-department queries are listed in HR-analytics work-sample and tutorial material (sources 12-14 in research/Book02_Part08_sources.md); no company-specific report found
**What the interviewer is checking:** Mapping free-text reasons into categories with CASE, conditional counting per group, and percentages with a stated denominator.
**Say this in the interview:** "I only look at people who have a leaving date. I map each exit reason into voluntary, involuntary or other with a CASE, count each per department, and divide by that department's leavers for the percentage. I'd confirm the mapping with HR first, because for example retirement is often treated separately."
**Explain simply:**
- **Voluntary** exit = the employee chose to go (resignation, relocation). **Involuntary** = the company decided (termination, layoff). The reason list below is my assumption: confirm it with HR.
- A **CASE** expression turns many reason texts into three categories. Anything unmapped (retirement, blank) goes to 'other_unknown' so nobody is lost.
- Percentage = category count / that department's total leavers x 100. The denominator is leavers, not headcount: this is a **mix**, not an attrition rate.
- Active employees have no `left_date`, so `WHERE left_date IS NOT NULL` removes them.
**Example:** Sales had 5 leavers: 3 resigned (voluntary, 60%), 1 laid off (involuntary, 20%), 1 retired (other, 20%).
**Sample data:**

*departments*

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Sales |
| 3 | IT |
| 4 | Finance |

*employees*

| emp_id | name | dept_id | left_date | exit_reason |
|---|---|---|---|---|
| 1 | Asha | 1 | 2026-01-31 | Resignation |
| 2 | Bala | 1 | 2026-02-28 | Termination |
| 3 | Chitra | 1 | 2026-04-30 | Resignation |
| 4 | Dev | 1 | NULL | NULL |
| 5 | Esha | 2 | 2026-03-31 | Resignation |
| 6 | Farid | 2 | 2026-05-31 | Relocation |
| 7 | Gopal | 2 | 2026-06-30 | Resignation |
| 8 | Hari | 2 | 2026-07-31 | Layoff |
| 9 | Isha | 2 | 2026-08-31 | Retirement |
| 10 | Jai | 3 | 2026-09-30 | NULL |
| 11 | Kiran | 3 | NULL | NULL |

**SQL:**
```sql
SELECT d.dept_name,
       COUNT(*) AS leavers,
       SUM(CASE WHEN e.exit_reason IN ('Resignation', 'Relocation') THEN 1 ELSE 0 END) AS voluntary,
       SUM(CASE WHEN e.exit_reason IN ('Termination', 'Layoff') THEN 1 ELSE 0 END) AS involuntary,
       SUM(CASE WHEN e.exit_reason IS NULL
                  OR e.exit_reason NOT IN ('Resignation', 'Relocation', 'Termination', 'Layoff')
                THEN 1 ELSE 0 END) AS other_unknown,
       ROUND(100.0 * SUM(CASE WHEN e.exit_reason IN ('Resignation', 'Relocation') THEN 1 ELSE 0 END) / COUNT(*), 1) AS voluntary_pct,
       ROUND(100.0 * SUM(CASE WHEN e.exit_reason IN ('Termination', 'Layoff') THEN 1 ELSE 0 END) / COUNT(*), 1) AS involuntary_pct
FROM employees e
JOIN departments d ON d.dept_id = e.dept_id
WHERE e.left_date IS NOT NULL
GROUP BY d.dept_name
ORDER BY d.dept_name;
```
**Output:**

| dept_name | leavers | voluntary | involuntary | other_unknown | voluntary_pct | involuntary_pct |
|---|---|---|---|---|---|---|
| HR | 3 | 2 | 1 | 0 | 66.7 | 33.3 |
| IT | 1 | 0 | 0 | 1 | 0.0 | 0.0 |
| Sales | 5 | 3 | 1 | 1 | 60.0 | 20.0 |

**pandas equivalent:**
```python
# the tables above are DataFrames with the same names and columns
import pandas as pd
vol, inv = ['Resignation', 'Relocation'], ['Termination', 'Layoff']
x = employees[employees.left_date.notna()].merge(departments, on='dept_id').copy()
x['voluntary'] = x.exit_reason.isin(vol).astype(int)
x['involuntary'] = x.exit_reason.isin(inv).astype(int)
x['other_unknown'] = 1 - x.voluntary - x.involuntary
res = (x.groupby('dept_name', as_index=False)
       .agg(leavers=('emp_id', 'count'), voluntary=('voluntary', 'sum'),
            involuntary=('involuntary', 'sum'), other_unknown=('other_unknown', 'sum')))
res['voluntary_pct'] = (100 * res.voluntary / res.leavers).round(1)
res['involuntary_pct'] = (100 * res.involuntary / res.leavers).round(1)
res = res.sort_values('dept_name').reset_index(drop=True)
# Output (matches the SQL):
# dept_name  leavers  voluntary  involuntary  other_unknown  voluntary_pct  involuntary_pct
#        HR        3          2            1              0           66.7             33.3
#        IT        1          0            0              1            0.0              0.0
#     Sales        5          3            1              1           60.0             20.0
```
**Edge cases:** Departments with no leavers (Finance) are absent; use a LEFT JOIN from `departments` with the leaver filter in the ON clause to show them with 0 (and guard the division with `NULLIF`). NULL exit reason (Jai) lands in other_unknown, which is why the three counts always add up. Spelling variants ('resigned', 'Resign') need a cleaned reason column or a mapping table. Counting people who left over several years together mixes periods: add a date filter. Percentages do not say which department has the worst attrition: that needs headcount as the denominator.
**Likely follow-ups:**
- Better: a mapping table `exit_reason_map(reason, type)` joined in, so new reasons need no code change.
- Attrition rate instead of mix? Leavers / average headcount for the period, per department.
- Is retirement voluntary? Often reported separately; the definition is a policy choice, so say which one you used.
**Common mistakes:** Counting active employees (no `left_date` filter); dividing by department headcount and calling it a mix; letting NULL reasons vanish so the percentages do not sum to 100; hard-coding messy free-text reasons without checking the distinct values first (`SELECT DISTINCT exit_reason`).

### Q38 ⭐⭐ 🟡 HR: Find employees who left within 6 months of joining (early attrition) and the share of total leavers they represent.
**Asked at:** commonly asked; early-attrition / tenure-of-leavers analyses appear in HR-analytics tutorial and study material (sources 13-14 in research/Book02_Part08_sources.md); no company-specific report found
**What the interviewer is checking:** Adding a time interval to a date (join date + 6 months), a conditional share, and defining the denominator (all leavers).
**Say this in the interview:** "An early leaver is someone whose leaving date is on or before their joining date plus six months. I list them, then divide their count by all leavers, ignoring people still employed. The date-add syntax differs by database, so I'd name that."
**Explain simply:**
- **Early attrition** = leaving within a set time of joining (here 6 months). It flags problems in hiring quality or onboarding.
- The test is `left_date <= join_date + 6 months`. Date-add functions differ by database (see alternatives).
- The share's denominator is **all leavers** (people with a leaving date), not all employees.
- `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` counts the early leavers inside a normal summary query.
**Example:** 5 people have left; 3 of them (Asha, Chitra, Dev) left within 6 months of joining: 3 / 5 = 60.0%. Esha is still employed so she is in neither number.
**Sample data:**

*employees*

| emp_id | name | join_date | left_date |
|---|---|---|---|
| 1 | Asha | 2025-01-10 | 2025-05-20 |
| 2 | Bala | 2024-03-01 | 2026-02-28 |
| 3 | Chitra | 2025-08-31 | 2026-02-28 |
| 4 | Dev | 2026-03-01 | 2026-04-15 |
| 5 | Esha | 2023-06-01 | NULL |
| 6 | Farid | 2025-02-01 | 2025-09-15 |

**SQL:**
```sql
SELECT emp_id, name, join_date, left_date,
       CAST(julianday(left_date) - julianday(join_date) AS INTEGER) AS days_to_exit
FROM employees
WHERE left_date IS NOT NULL
  AND left_date <= date(join_date, '+6 months')
ORDER BY days_to_exit;

SELECT COUNT(*) AS leavers,
       SUM(CASE WHEN left_date <= date(join_date, '+6 months') THEN 1 ELSE 0 END) AS early_leavers,
       ROUND(100.0 * SUM(CASE WHEN left_date <= date(join_date, '+6 months') THEN 1 ELSE 0 END)
             / COUNT(*), 1) AS early_share_pct
FROM employees
WHERE left_date IS NOT NULL;

-- Add 6 months in other dialects (not run here / from memory):
-- PostgreSQL : left_date <= join_date + INTERVAL '6 months'
-- MySQL      : left_date <= DATE_ADD(join_date, INTERVAL 6 MONTH)
-- SQL Server : left_date <= DATEADD(month, 6, join_date)
```
**Output:**

*The early leavers*

| emp_id | name | join_date | left_date | days_to_exit |
|---|---|---|---|---|
| 4 | Dev | 2026-03-01 | 2026-04-15 | 45 |
| 1 | Asha | 2025-01-10 | 2025-05-20 | 130 |
| 3 | Chitra | 2025-08-31 | 2026-02-28 | 181 |

*Share of all leavers*

| leavers | early_leavers | early_share_pct |
|---|---|---|
| 5 | 3 | 60.0 |

**pandas equivalent:**
```python
# the tables above are DataFrames with the same names and columns
import pandas as pd
# The early leavers
e = employees[employees.left_date.notna()].copy()
j, l = pd.to_datetime(e.join_date), pd.to_datetime(e.left_date)
e['days_to_exit'] = (l - j).dt.days
early = e[l <= j + pd.DateOffset(months=6)]
res = (early[['emp_id', 'name', 'join_date', 'left_date', 'days_to_exit']]
       .sort_values('days_to_exit').reset_index(drop=True))
# Output (matches the SQL):
#  emp_id   name  join_date  left_date  days_to_exit
#       4    Dev 2026-03-01 2026-04-15            45
#       1   Asha 2025-01-10 2025-05-20           130
#       3 Chitra 2025-08-31 2026-02-28           181

# Share of all leavers
res = pd.DataFrame({'leavers': [len(e)], 'early_leavers': [len(early)]})
res['early_share_pct'] = (100 * res.early_leavers / res.leavers).round(1)
# Output (matches the SQL):
#  leavers  early_leavers  early_share_pct
#        5              3             60.0
```
**Edge cases:** Active employees (NULL left_date) are excluded from both numerator and denominator. 'Within 6 months' is taken as inclusive of the 6-month date. Month-end joiners differ by database: for 2025-08-31 + 6 months, SQLite rolls over to 2026-03-03, while PostgreSQL clamps to 2026-02-28 (from memory); the result here is the same either way. Rehired people with two rows should be treated carefully. Joiners from the last 6 months who have not left yet cannot be 'early leavers' yet, so recent cohorts look better than they are. A leaving date before the joining date is a data error.
**Likely follow-ups:**
- Early attrition rate per hiring cohort? Group by the joining year or quarter, and divide early leavers by the people hired in that period (not by leavers).
- By department or manager? Join departments and add `GROUP BY`; compare with the company share.
- Why a different denominator from the rate? The question asks what share of leavers are early; a rate asks what share of hires leave early.
**Common mistakes:** Dividing by all employees; including people who haven't left; using `DATEDIFF(month, ...) <= 6`, which counts calendar-month boundaries and mis-measures; leaving out the NULL `left_date` filter.

### Q39 ⭐⭐ 🟡 Banking: Flag customers who made transactions totalling more than ₹50,000 in a single day.

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Whether you know to group by customer AND day, and to filter the totals with HAVING (not WHERE).

**Say this in the interview:** "I add up each customer's transactions per day using GROUP BY on customer and date, then keep only the groups whose total is above 50,000 using HAVING, because WHERE cannot see totals."

**Explain simply:**
- GROUP BY puts rows into buckets; here one bucket per customer per day.
- SUM adds the amounts inside each bucket.
- HAVING filters buckets after adding up; WHERE filters single rows before adding up.
- If the column is a timestamp (date plus time), cut it to a date first, e.g. DATE(txn_ts), otherwise every second is its own day.

**Example:** Think of an HR expense claim: an employee submits two claims of 30,000 and 25,000 on the same day. Neither is big alone, but 55,000 for the day trips the review rule. This is how banks flag possible structuring (splitting a big amount into small ones).

**Sample data:**
`transactions`

| txn_id | customer_id | txn_date | amount |
|---|---|---|---|
| 1 | 101 | 2025-09-10 | 30000 |
| 2 | 101 | 2025-09-10 | 25000 |
| 3 | 102 | 2025-09-10 | 50000 |
| 4 | 103 | 2025-09-10 | 30000 |
| 5 | 103 | 2025-09-11 | 30000 |
| 6 | 104 | 2025-09-10 | 60000 |
| 7 | 101 | 2025-09-12 | 10000 |
| 8 | 102 | 2025-09-11 | 1 |

**SQL:**
```sql
SELECT customer_id, txn_date, SUM(amount) AS day_total
FROM transactions
GROUP BY customer_id, txn_date
HAVING SUM(amount) > 50000
ORDER BY customer_id, txn_date;
```

**Output:**
| customer_id | txn_date | day_total |
|---|---|---|
| 101 | 2025-09-10 | 55000 |
| 104 | 2025-09-10 | 60000 |

**pandas equivalent:**
```python
# DataFrames named like the tables above (e.g. transactions = pd.DataFrame(...))
t = transactions.groupby(['customer_id','txn_date'], as_index=False)['amount'].sum().rename(columns={'amount':'day_total'})
result = t[t.day_total > 50000].sort_values(['customer_id','txn_date'])
```
(Each pandas result was run and matches the SQL output above.)

**Edge cases:** Exactly 50,000 is NOT flagged (strictly greater than). Customer 103 has 30,000 on two different days, so no flag. NULL amounts are ignored by SUM. If txn_date holds a time, convert to a date first.

**Likely follow-ups:** 1) Show only the customers, not the days? SELECT DISTINCT customer_id from the same query. 2) Count how many flagged days per customer? Wrap it and GROUP BY customer_id with COUNT(*).

**Common mistakes:** Using WHERE SUM(amount) > 50000 (error). Grouping only by customer, which adds all days together. Using >= when the rule says more than.

### Q40 ⭐⭐ 🟡 Banking: Find dormant accounts: accounts with no transaction in the last 6 months.

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Whether you take each account's LAST transaction date and also remember accounts with no transactions at all (LEFT JOIN).

**Say this in the interview:** "I find each account's latest transaction date with MAX, using a LEFT JOIN so accounts with zero transactions stay in, and keep those whose last date is older than six months or missing."

**Explain simply:**
- Today is taken as 1 Oct 2025 so the answer is repeatable; in real use replace it with CURRENT_DATE.
- 'Dormant' means silent for a period. An account with no activity ever is also dormant, which an inner JOIN would silently drop.
- LEFT JOIN keeps every row from the left table (accounts) even if there is no match; unmatched columns come back as NULL.
- Dates written as YYYY-MM-DD compare correctly as plain text, so < works.

**Example:** Same idea as HR finding employees with no leave or training record in 6 months: take each person's last record date and check if it is too old, but do not forget people with no record at all.

**Sample data:**
`accounts`

| account_id | customer | opened |
|---|---|---|
| 1 | Asha | 2020-01-10 |
| 2 | Ravi | 2021-05-03 |
| 3 | Meera | 2022-08-19 |
| 4 | Kabir | 2024-11-01 |
| 5 | Neha | 2025-02-14 |

`transactions`

| txn_id | account_id | txn_date |
|---|---|---|
| 1 | 1 | 2025-09-20 |
| 2 | 1 | 2024-12-01 |
| 3 | 2 | 2025-03-15 |
| 4 | 2 | 2025-01-10 |
| 5 | 3 | 2025-06-30 |
| 6 | 5 | 2025-02-20 |

**SQL:**
```sql
-- SQLite syntax. Cut-off = DATE('2025-10-01','-6 months') = 2025-04-01
SELECT a.account_id, a.customer, MAX(t.txn_date) AS last_txn
FROM accounts a
LEFT JOIN transactions t ON t.account_id = a.account_id
GROUP BY a.account_id, a.customer
HAVING MAX(t.txn_date) IS NULL
    OR MAX(t.txn_date) < DATE('2025-10-01', '-6 months')
ORDER BY a.account_id;
```
Other dialects (not run here / from memory): MySQL `DATE_SUB(CURDATE(), INTERVAL 6 MONTH)`; PostgreSQL `CURRENT_DATE - INTERVAL '6 months'`; SQL Server `DATEADD(month, -6, GETDATE())`.

**Output:**
| account_id | customer | last_txn |
|---|---|---|
| 2 | Ravi | 2025-03-15 |
| 4 | Kabir | NULL |
| 5 | Neha | 2025-02-20 |

**pandas equivalent:**
```python
# DataFrames named like the tables above (e.g. transactions = pd.DataFrame(...))
last = transactions.groupby('account_id', as_index=False)['txn_date'].max().rename(columns={'txn_date':'last_txn'})
m = accounts.merge(last, on='account_id', how='left')[['account_id','customer','last_txn']]
cutoff = '2025-04-01'
result = m[m.last_txn.isna() | (m.last_txn < cutoff)].sort_values('account_id')
```
(Each pandas result was run and matches the SQL output above.)

**Edge cases:** Account 4 never transacted: appears with last_txn NULL. Account 5 last transacted on 20 Feb 2025 (older than cutoff) so it is dormant. Account 3 on 30 Jun is active. A transaction exactly on the cutoff date is treated as active here (< not <=).

**Likely follow-ups:** 1) Why not use NOT IN? NOT IN breaks if the subquery returns a NULL; NOT EXISTS is safer. 2) How many dormant accounts per branch? Add GROUP BY branch over this result.

**Common mistakes:** Using an INNER JOIN and losing never-used accounts. Filtering with WHERE txn_date < cutoff, which flags an account that has an old transaction AND a recent one.

### Q41 ⭐⭐ 🟡 Banking: Show average balance by account type and list branches whose average balance is above the bank-wide average.

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** GROUP BY with AVG, then comparing a group figure with an overall figure using a subquery in HAVING.

**Say this in the interview:** "First query is a plain GROUP BY on account type. For the second, I compute the bank-wide average in a scalar subquery and keep only branches whose own average is higher, using HAVING."

**Explain simply:**
- A subquery is a query inside another query; a scalar one returns a single number (here the overall average).
- HAVING compares each branch's average with that number.
- Bank-wide average here is the average over all accounts, not the average of branch averages. The two differ when branches have different account counts; say which one you used.

**Example:** Like HR listing departments whose average salary beats the company average.

**Sample data:**
`accounts`

| account_id | branch | account_type | balance |
|---|---|---|---|
| 1 | Mumbai | Savings | 50000 |
| 2 | Mumbai | Current | 200000 |
| 3 | Delhi | Savings | 30000 |
| 4 | Delhi | Savings | 40000 |
| 5 | Pune | Current | 120000 |
| 6 | Pune | Savings | 20000 |
| 7 | Chennai | Current | 90000 |
| 8 | Chennai | Savings | 60000 |

**SQL:**
```sql
-- Query 1
SELECT account_type, ROUND(AVG(balance), 0) AS avg_balance
FROM accounts
GROUP BY account_type
ORDER BY account_type;

-- Query 2
SELECT branch, ROUND(AVG(balance), 0) AS branch_avg,
       (SELECT ROUND(AVG(balance), 0) FROM accounts) AS bank_avg
FROM accounts
GROUP BY branch
HAVING AVG(balance) > (SELECT AVG(balance) FROM accounts)
ORDER BY branch;
```

**Output:**
Query 1:

| account_type | avg_balance |
|---|---|
| Current | 136667 |
| Savings | 40000 |

Query 2:

| branch | branch_avg | bank_avg |
|---|---|---|
| Mumbai | 125000 | 76250 |

**pandas equivalent:**
```python
# DataFrames named like the tables above (e.g. transactions = pd.DataFrame(...))
result = accounts.groupby('account_type', as_index=False)['balance'].mean().rename(columns={'balance':'avg_balance'}).round(0)

bank = accounts.balance.mean()
b = accounts.groupby('branch', as_index=False)['balance'].mean().rename(columns={'balance':'branch_avg'})
b = b[b.branch_avg > bank].copy()
b['branch_avg'] = b.branch_avg.round(0); b['bank_avg'] = round(bank)
result = b.sort_values('branch')
```
(Each pandas result was run and matches the SQL output above.)

**Edge cases:** Branch with NULL balances: AVG ignores NULLs. Empty table returns no rows. A branch exactly equal to the bank average is excluded (strictly above).

**Likely follow-ups:** 1) Same with a window function? AVG(balance) OVER () gives the overall average on every row. 2) Average of branch averages instead? Wrap the branch averages in a CTE and take AVG of that.

**Common mistakes:** Writing WHERE AVG(balance) > ... (not allowed). Forgetting the bracketed subquery. Comparing against the average of branch averages without saying so.

### Q42 ⭐⭐ 🟡 Banking: Using `loans` (customer_id, loan_amount) and `repayments` (loan_id, amount), show total outstanding balance per customer.

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Spotting the one-to-many trap (a loan has many repayments) and the need to total repayments first so loan amounts are not counted twice.

**Say this in the interview:** "I total the repayments per loan first in a CTE, then LEFT JOIN to loans so unpaid loans stay, and subtract paid from loan amount per customer."

**Explain simply:**
- Premise note: the question lists loans(customer_id, loan_amount) but repayments link by loan_id, so loans must also have a loan_id.
- If you join loans to repayments directly, a 100,000 loan with 2 repayments appears twice and is counted as 200,000 (fan-out).
- COALESCE(x, 0) turns a missing value into 0, needed for loans with no repayments yet.
- A CTE (WITH ... AS) is a named temporary result that makes the query readable.

**Example:** Like HR tracking a salary advance: advance given 100,000, recovered 20,000 + 30,000 over months, so 50,000 is still to recover.

**Sample data:**
`loans`

| loan_id | customer_id | loan_amount |
|---|---|---|
| 1 | 11 | 100000 |
| 2 | 11 | 50000 |
| 3 | 12 | 80000 |
| 4 | 13 | 60000 |

`repayments`

| repayment_id | loan_id | amount |
|---|---|---|
| 1 | 1 | 20000 |
| 2 | 1 | 30000 |
| 3 | 2 | 10000 |
| 4 | 3 | 50000 |
| 5 | 3 | 30000 |

**SQL:**
```sql
WITH paid AS (
    SELECT loan_id, SUM(amount) AS paid
    FROM repayments
    GROUP BY loan_id
)
SELECT l.customer_id,
       SUM(l.loan_amount)                         AS total_loan,
       SUM(COALESCE(p.paid, 0))                   AS total_paid,
       SUM(l.loan_amount - COALESCE(p.paid, 0))   AS outstanding
FROM loans l
LEFT JOIN paid p ON p.loan_id = l.loan_id
GROUP BY l.customer_id
ORDER BY l.customer_id;
```

**Output:**
| customer_id | total_loan | total_paid | outstanding |
|---|---|---|---|
| 11 | 150000 | 60000 | 90000 |
| 12 | 80000 | 80000 | 0 |
| 13 | 60000 | 0 | 60000 |

**pandas equivalent:**
```python
# DataFrames named like the tables above (e.g. transactions = pd.DataFrame(...))
paid = repayments.groupby('loan_id', as_index=False)['amount'].sum().rename(columns={'amount':'paid'})
m = loans.merge(paid, on='loan_id', how='left').fillna({'paid':0})
m['outstanding'] = m.loan_amount - m.paid
g = m.groupby('customer_id', as_index=False).agg(total_loan=('loan_amount','sum'), total_paid=('paid','sum'), outstanding=('outstanding','sum'))
result = g.sort_values('customer_id')
```
(Each pandas result was run and matches the SQL output above.)

**Edge cases:** Loan 4 has no repayments: outstanding = full 60,000. Customer 12 has fully repaid (outstanding 0). Overpayments would give negative balances; wrap with GREATEST(...,0)/MAX in real use.

**Likely follow-ups:** 1) Only customers who still owe? Add HAVING SUM(...) > 0. 2) Why not join first then SUM? It repeats loan_amount for every repayment row.

**Common mistakes:** Joining first and summing loan_amount (double counting). Using an inner join and dropping loans with no repayments. Forgetting COALESCE so NULL wipes the result.

### Q43 ⭐⭐ 🟡 E-commerce: Calculate the late-delivery rate (delivered_at later than promised_at) per delivery partner.

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Conditional counting with CASE WHEN and calculating a rate with the right denominator (and decimals).

**Say this in the interview:** "I count deliveries per partner, count the late ones with a CASE expression, and divide, multiplying by 100.0 so the division is not integer division. Undelivered orders are excluded since they have no delivery time yet."

**Explain simply:**
- Rate = late deliveries / delivered deliveries.
- CASE WHEN gives 1 for a late order and 0 otherwise; SUM of those is the late count. (AVG of the 0/1 flag gives the rate directly.)
- In many databases 3/4 gives 0 (integer division); 100.0 forces decimals.
- Order 8 is still on the way (NULL delivered_at), so it is not counted as on-time or late.

**Example:** Like HR measuring late arrivals: days an employee clocked in after 9:30, divided by days they came in.

**Sample data:**
`deliveries`

| order_id | partner | promised_at | delivered_at |
|---|---|---|---|
| 1 | FastGo | 2025-09-10 18:00 | 2025-09-10 17:00 |
| 2 | FastGo | 2025-09-11 18:00 | 2025-09-12 09:00 |
| 3 | FastGo | 2025-09-12 18:00 | 2025-09-12 18:00 |
| 4 | QuickShip | 2025-09-10 18:00 | 2025-09-10 19:30 |
| 5 | QuickShip | 2025-09-11 18:00 | 2025-09-11 20:00 |
| 6 | QuickShip | 2025-09-12 18:00 | 2025-09-12 17:00 |
| 7 | QuickShip | 2025-09-13 18:00 | 2025-09-13 17:30 |
| 8 | FastGo | 2025-09-14 18:00 | NULL |

**SQL:**
```sql
SELECT partner,
       COUNT(*) AS delivered,
       SUM(CASE WHEN delivered_at > promised_at THEN 1 ELSE 0 END) AS late,
       ROUND(100.0 * SUM(CASE WHEN delivered_at > promised_at THEN 1 ELSE 0 END) / COUNT(*), 1) AS late_pct
FROM deliveries
WHERE delivered_at IS NOT NULL
GROUP BY partner
ORDER BY partner;
```

**Output:**
| partner | delivered | late | late_pct |
|---|---|---|---|
| FastGo | 3 | 1 | 33.3 |
| QuickShip | 4 | 2 | 50 |

**pandas equivalent:**
```python
# DataFrames named like the tables above (e.g. transactions = pd.DataFrame(...))
d = deliveries[deliveries.delivered_at.notna()].copy()
d['late'] = (d.delivered_at > d.promised_at).astype(int)
g = d.groupby('partner', as_index=False).agg(delivered=('order_id','count'), late=('late','sum'))
g['late_pct'] = (100.0 * g.late / g.delivered).round(1)
result = g.sort_values('partner')
```
(Each pandas result was run and matches the SQL output above.)

**Edge cases:** NULL delivered_at must be excluded or reported separately. Comparing text timestamps works only in a consistent YYYY-MM-DD HH:MM format; use real timestamp types in production. A partner with no delivered orders would be missing (COUNT 0 would divide by zero).

**Likely follow-ups:** 1) Late by more than 1 hour? Use a time difference (e.g. julianday or DATEDIFF/INTERVAL by dialect). 2) Rate per month? Add the month to GROUP BY.

**Common mistakes:** Integer division giving 0 or 1. Counting undelivered orders as on-time. Dividing by all orders including undelivered ones without saying so.

### Q44 ⭐⭐ 🟡 E-commerce: Calculate the return rate (returned items divided by items sold) per product category.

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Joining a fact table to a lookup table and computing a ratio per group.

**Say this in the interview:** "I join order items to products to get the category, then per category divide the returned count by the items sold. A 0/1 returned flag lets me just SUM it."

**Explain simply:**
- Assumed design: one row per item sold with an is_returned flag (1 = returned). If returns sit in a separate table, LEFT JOIN it instead.
- Return rate = returned items / items sold.
- If you have a quantity column, sum quantities instead of counting rows.

**Example:** Same as HR attrition rate per department: leavers divided by headcount.

**Sample data:**
`products`

| product_id | category |
|---|---|
| 1 | Shoes |
| 2 | Shoes |
| 3 | Shirts |
| 4 | Phones |

`order_items`

| item_id | product_id | is_returned |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 1 | 0 |
| 3 | 2 | 0 |
| 4 | 2 | 0 |
| 5 | 3 | 1 |
| 6 | 3 | 1 |
| 7 | 3 | 0 |
| 8 | 4 | 0 |
| 9 | 4 | 0 |
| 10 | 4 | 1 |

**SQL:**
```sql
SELECT p.category,
       COUNT(*) AS items_sold,
       SUM(oi.is_returned) AS items_returned,
       ROUND(100.0 * SUM(oi.is_returned) / COUNT(*), 1) AS return_rate_pct
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY return_rate_pct DESC, p.category;
```

**Output:**
| category | items_sold | items_returned | return_rate_pct |
|---|---|---|---|
| Shirts | 3 | 2 | 66.7 |
| Phones | 3 | 1 | 33.3 |
| Shoes | 4 | 1 | 25 |

**pandas equivalent:**
```python
# DataFrames named like the tables above (e.g. transactions = pd.DataFrame(...))
m = order_items.merge(products, on='product_id')
g = m.groupby('category', as_index=False).agg(items_sold=('item_id','count'), items_returned=('is_returned','sum'))
g['return_rate_pct'] = (100.0 * g.items_returned / g.items_sold).round(1)
result = g.sort_values(['return_rate_pct','category'], ascending=[False, True])
```
(Each pandas result was run and matches the SQL output above.)

**Edge cases:** Items sold with NULL is_returned: treat as 0 with COALESCE. Categories with no sales do not appear. With a separate returns table, join carefully so one item is not counted twice.

**Likely follow-ups:** 1) Return rate by value instead of count? Use SUM(price*flag)/SUM(price). 2) Only categories above 30%? Add HAVING.

**Common mistakes:** Integer division. Counting returned rows in the denominator only. Joining a returns table with many rows per item and inflating the count.

### Q45 ⭐⭐ 🟡 E-commerce: What percentage of customers have placed two or more orders (overall repeat-purchase rate)?

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Two-step aggregation (orders per customer, then a summary of that) and awareness of which denominator you are using.

**Say this in the interview:** "I count orders per customer in a CTE, then count customers with two or more and divide by customers who bought at all. I mention that dividing by all registered customers gives a lower number."

**Explain simply:**
- Standard repeat-purchase rate = customers with 2+ orders / customers with at least 1 order.
- Customers who registered but never ordered (5 here) only appear in the 'all registered' version.
- The question is ambiguous on the denominator, so state your choice in the interview.

**Example:** Like HR asking what share of past interns got a second contract: among those hired once or more, how many were hired again.

**Sample data:**
`customers`

| customer_id |
|---|
| 1 |
| 2 |
| 3 |
| 4 |
| 5 |
| 6 |

`orders`

| order_id | customer_id |
|---|---|
| 1 | 1 |
| 2 | 1 |
| 3 | 2 |
| 4 | 3 |
| 5 | 3 |
| 6 | 3 |
| 7 | 4 |
| 8 | 6 |

**SQL:**
```sql
WITH per_cust AS (
    SELECT customer_id, COUNT(*) AS n_orders
    FROM orders
    GROUP BY customer_id
)
SELECT COUNT(*) AS buyers,
       SUM(CASE WHEN n_orders >= 2 THEN 1 ELSE 0 END) AS repeat_buyers,
       ROUND(100.0 * SUM(CASE WHEN n_orders >= 2 THEN 1 ELSE 0 END) / COUNT(*), 1) AS repeat_rate_pct,
       ROUND(100.0 * SUM(CASE WHEN n_orders >= 2 THEN 1 ELSE 0 END) / (SELECT COUNT(*) FROM customers), 1) AS repeat_of_all_registered_pct
FROM per_cust;
```

**Output:**
| buyers | repeat_buyers | repeat_rate_pct | repeat_of_all_registered_pct |
|---|---|---|---|
| 5 | 2 | 40 | 33.3 |

**pandas equivalent:**
```python
# DataFrames named like the tables above (e.g. transactions = pd.DataFrame(...))
pc = orders.groupby('customer_id').size().rename('n_orders').reset_index()
buyers = len(pc); rep = int((pc.n_orders >= 2).sum())
result = pd.DataFrame({'buyers':[buyers], 'repeat_buyers':[rep], 'repeat_rate_pct':[round(100.0*rep/buyers,1)], 'repeat_of_all_registered_pct':[round(100.0*rep/len(customers),1)]})
```
(Each pandas result was run and matches the SQL output above.)

**Edge cases:** Customers with zero orders; cancelled orders (filter them out first if they should not count); one customer with duplicate order rows. Empty orders table would divide by zero.

**Likely follow-ups:** 1) Repeat within 30 days? Compare each customer's first and second order dates. 2) Why a CTE? Because we aggregate an aggregate, which cannot be nested directly in one SELECT.

**Common mistakes:** Using COUNT(DISTINCT customer_id) with HAVING in one step (returns rows, not a rate). Integer division. Using the wrong denominator without saying so.

### Q46 ⭐⭐ 🟡 Sales: Compare total sales on weekdays versus weekends.

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Date-part functions and CASE for bucketing, and fairness of comparison (5 weekdays vs 2 weekend days).

**Say this in the interview:** "I label each sale Weekday or Weekend from its day of week, sum by label, and also show average per day, because a total alone favours weekdays which are five days a week."

**Explain simply:**
- strftime('%w') in SQLite returns 0 for Sunday to 6 for Saturday.
- Totals are not a fair comparison when there are different numbers of days, so give an average per day too.
- The group is labelled in the SELECT and reused in GROUP BY (SQLite/MySQL/PostgreSQL allow the alias; SQL Server needs the full expression).

**Example:** Like comparing weekday and weekend attendance in a call centre: totals are higher on weekdays just because there are more of them.

**Sample data:**
`sales`

| sale_id | sale_date | amount |
|---|---|---|
| 1 | 2025-09-01 | 1000 |
| 2 | 2025-09-02 | 1200 |
| 3 | 2025-09-05 | 1500 |
| 4 | 2025-09-06 | 3000 |
| 5 | 2025-09-07 | 2500 |
| 6 | 2025-09-08 | 900 |
| 7 | 2025-09-13 | 2000 |
| 8 | 2025-09-14 | 1800 |

**SQL:**
```sql
SELECT CASE WHEN STRFTIME('%w', sale_date) IN ('0', '6') THEN 'Weekend' ELSE 'Weekday' END AS day_type,
       SUM(amount) AS total_sales,
       COUNT(DISTINCT sale_date) AS days_with_sales,
       ROUND(1.0 * SUM(amount) / COUNT(DISTINCT sale_date), 0) AS avg_per_day
FROM sales
GROUP BY day_type
ORDER BY day_type DESC;
```
Other dialects (not run here / from memory): MySQL `DAYOFWEEK(sale_date) IN (1,7)` (1 = Sunday); PostgreSQL `EXTRACT(DOW FROM sale_date) IN (0,6)`; SQL Server `DATENAME(weekday, sale_date) IN ('Saturday','Sunday')` (avoids the DATEFIRST setting).

**Output:**
| day_type | total_sales | days_with_sales | avg_per_day |
|---|---|---|---|
| Weekend | 9300 | 4 | 2325 |
| Weekday | 4600 | 4 | 1150 |

**pandas equivalent:**
```python
# DataFrames named like the tables above (e.g. transactions = pd.DataFrame(...))
s = sales.copy()
s['day_type'] = pd.to_datetime(s.sale_date).dt.dayofweek.map(lambda d: 'Weekend' if d >= 5 else 'Weekday')
g = s.groupby('day_type', as_index=False).agg(total_sales=('amount','sum'), days_with_sales=('sale_date','nunique'))
g['avg_per_day'] = (g.total_sales / g.days_with_sales).round(0)
result = g.sort_values('day_type', ascending=False)
```
(Each pandas result was run and matches the SQL output above.)

**Edge cases:** Weekend definition differs by country (Fri-Sat in some). Days with no sales are not counted in the per-day average. NULL dates drop out of both groups' labels as 'Weekday', so filter them first.

**Likely follow-ups:** 1) Which weekday is best? Group by day name. 2) Is Pandas the same? Yes, dt.dayofweek gives 0=Monday so >=5 is weekend.

**Common mistakes:** Mixing up weekday numbering across databases. Comparing raw totals only. Putting the CASE alias in WHERE.

### Q47 ⭐⭐ 🟡 Sales: Show quarterly sales per region as columns Q1, Q2, Q3, Q4 (one row per region).

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Pivoting rows into columns with conditional aggregation (SUM + CASE), and computing the quarter from a month.

**Say this in the interview:** "Standard SQL has no simple pivot, so I work out the quarter as (month+2)/3 using integer division and then SUM a CASE per quarter, which turns the rows into four columns."

**Explain simply:**
- A pivot turns row values (quarters) into column headings.
- Quarter = (month + 2) / 3 with integer division: Jan-Mar = 1, Apr-Jun = 2, etc. (SQLite integer division; PostgreSQL/SQL Server also integer; MySQL use DIV.)
- ELSE 0 makes empty quarters show 0 rather than NULL.
- SQL Server and Oracle have a PIVOT keyword; the CASE method works everywhere.

**Example:** Like an HR report with one row per department and columns for hires in Q1 to Q4.

**Sample data:**
`sales`

| sale_id | region | sale_date | amount |
|---|---|---|---|
| 1 | North | 2025-01-15 | 100 |
| 2 | North | 2025-02-10 | 150 |
| 3 | North | 2025-05-20 | 200 |
| 4 | South | 2025-03-05 | 300 |
| 5 | South | 2025-08-12 | 250 |
| 6 | South | 2025-11-30 | 400 |
| 7 | East | 2025-04-01 | 50 |
| 8 | East | 2025-07-07 | 60 |
| 9 | East | 2025-10-10 | 70 |
| 10 | East | 2025-12-25 | 80 |

**SQL:**
```sql
SELECT region,
       SUM(CASE WHEN q = 1 THEN amount ELSE 0 END) AS Q1,
       SUM(CASE WHEN q = 2 THEN amount ELSE 0 END) AS Q2,
       SUM(CASE WHEN q = 3 THEN amount ELSE 0 END) AS Q3,
       SUM(CASE WHEN q = 4 THEN amount ELSE 0 END) AS Q4
FROM (SELECT region, amount,
             (CAST(STRFTIME('%m', sale_date) AS INTEGER) + 2) / 3 AS q
      FROM sales) s
GROUP BY region
ORDER BY region;
```

**Output:**
| region | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| East | 0 | 50 | 60 | 150 |
| North | 250 | 200 | 0 | 0 |
| South | 300 | 0 | 250 | 400 |

**pandas equivalent:**
```python
# DataFrames named like the tables above (e.g. transactions = pd.DataFrame(...))
s = sales.copy()
s['q'] = 'Q' + ((pd.to_datetime(s.sale_date).dt.month + 2) // 3).astype(str)
p = s.pivot_table(index='region', columns='q', values='amount', aggfunc='sum', fill_value=0).reindex(columns=['Q1','Q2','Q3','Q4'], fill_value=0)
result = p.reset_index()
```
(Each pandas result was run and matches the SQL output above.)

**Edge cases:** If data spans several years, add the year to GROUP BY or you merge Q1 2024 with Q1 2025. Calendar quarters assumed; a fiscal year starting in April needs a different formula. A region with no sales in a quarter gets 0.

**Likely follow-ups:** 1) Add a total column? Add Q1+Q2+Q3+Q4 or SUM(amount). 2) Dynamic columns? Needs dynamic SQL; not possible in plain SQL.

**Common mistakes:** Forgetting the year. Using ELSE NULL then wondering about blanks. Integer-division surprises in MySQL (use DIV or FLOOR).

### Q48 ⭐⭐ 🟡 Sales: List customers whose total spend is above the average spend of customers in their own city.

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Window functions (AVG OVER PARTITION BY) or correlated subqueries, and aggregating first before comparing.

**Say this in the interview:** "I total spend per customer, then use AVG as a window function partitioned by city to put the city average next to each customer, and filter where the customer is above it."

**Explain simply:**
- Step 1: total spend per customer (an aggregate).
- Step 2: AVG(...) OVER (PARTITION BY city) adds the city average to every row without collapsing rows.
- You cannot use a window function directly in WHERE, so wrap it in a CTE first.
- Customers with no orders count as 0 spend and pull the average down; say so, or drop them if the average should be only among buyers.

**Example:** Like finding employees paid above their own department's average, but here per customer spend.

**Sample data:**
`customers`

| customer_id | name | city |
|---|---|---|
| 1 | Asha | Mumbai |
| 2 | Ravi | Mumbai |
| 3 | Meera | Mumbai |
| 4 | Kabir | Delhi |
| 5 | Neha | Delhi |
| 6 | Omar | Delhi |

`orders`

| order_id | customer_id | amount |
|---|---|---|
| 1 | 1 | 500 |
| 2 | 1 | 700 |
| 3 | 2 | 300 |
| 4 | 3 | 200 |
| 5 | 3 | 100 |
| 6 | 4 | 900 |
| 7 | 5 | 400 |
| 8 | 5 | 300 |
| 9 | 5 | 200 |

**SQL:**
```sql
WITH spend AS (
    SELECT c.customer_id, c.name, c.city, COALESCE(SUM(o.amount), 0) AS total_spend
    FROM customers c
    LEFT JOIN orders o ON o.customer_id = c.customer_id
    GROUP BY c.customer_id, c.name, c.city
),
with_avg AS (
    SELECT *, AVG(total_spend) OVER (PARTITION BY city) AS city_avg
    FROM spend
)
SELECT name, city, total_spend, ROUND(city_avg, 1) AS city_avg
FROM with_avg
WHERE total_spend > city_avg
ORDER BY city, name;
```

**Output:**
| name | city | total_spend | city_avg |
|---|---|---|---|
| Kabir | Delhi | 900 | 600 |
| Neha | Delhi | 900 | 600 |
| Asha | Mumbai | 1200 | 600 |

**pandas equivalent:**
```python
# DataFrames named like the tables above (e.g. transactions = pd.DataFrame(...))
o = orders.groupby('customer_id', as_index=False)['amount'].sum().rename(columns={'amount':'total_spend'})
s = customers.merge(o, on='customer_id', how='left').fillna({'total_spend':0})
s['city_avg'] = s.groupby('city')['total_spend'].transform('mean')
r = s[s.total_spend > s.city_avg].copy()
r['city_avg'] = r.city_avg.round(1)
result = r[['name','city','total_spend','city_avg']].sort_values(['city','name'])
```
(Each pandas result was run and matches the SQL output above.)

**Edge cases:** Mumbai spends 1200, 300, 300 (avg 600), so only Asha is above. Delhi spends 900, 900, 0 (avg 600): Omar's zero from having no orders pulls the average down; excluding him would make the Delhi average 900 and nobody above it. Ties equal to the average are not above. NULL city forms its own group.

**Likely follow-ups:** 1) Without window functions? Join to a subquery that GROUPs BY city and averages. 2) Above the median instead? Needs PERCENTILE or a rank approach.

**Common mistakes:** Averaging order amounts instead of customer totals. Using window function in WHERE. Forgetting customers with no orders.

### Q49 ⭐⭐ 🔴 Banking: `transfers` has from_account, to_account and amount. Compute the net inflow (received minus sent) for every account.

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Handling a table where an account appears in two different columns; the UNION ALL trick with signed amounts.

**Say this in the interview:** "I stack the table on itself: received amounts as positive rows and sent amounts as negative rows with UNION ALL, then SUM per account. That also covers accounts that only sent or only received."

**Explain simply:**
- UNION ALL glues two result sets one under the other and keeps every row (UNION would remove duplicates and wrongly merge equal transfers).
- Money received is +amount, money sent is -amount, so the sum is the net inflow.
- Account A only sent money, D only received; the stacking approach handles both without outer joins.

**Example:** Like an HR leave balance: leave credited to you is +, leave taken is -, and the balance is the sum.

**Sample data:**
`transfers`

| transfer_id | from_account | to_account | amount |
|---|---|---|---|
| 1 | A | B | 1000 |
| 2 | A | C | 500 |
| 3 | B | C | 300 |
| 4 | C | A | 200 |
| 5 | B | D | 100 |

**SQL:**
```sql
SELECT account, SUM(amount) AS net_inflow
FROM (
    SELECT to_account   AS account,  amount FROM transfers
    UNION ALL
    SELECT from_account AS account, -amount FROM transfers
) x
GROUP BY account
ORDER BY account;
```

**Output:**
| account | net_inflow |
|---|---|
| A | -1300 |
| B | 600 |
| C | 600 |
| D | 100 |

**pandas equivalent:**
```python
# DataFrames named like the tables above (e.g. transactions = pd.DataFrame(...))
a = pd.concat([transfers[['to_account','amount']].rename(columns={'to_account':'account'}),
               transfers[['from_account','amount']].rename(columns={'from_account':'account'}).assign(amount=lambda d: -d.amount)])
result = a.groupby('account', as_index=False)['amount'].sum().rename(columns={'amount':'net_inflow'}).sort_values('account')
```
(Each pandas result was run and matches the SQL output above.)

**Edge cases:** Use UNION ALL, not UNION (two identical transfers would collapse). Accounts with no transfers at all will not appear; LEFT JOIN from an accounts table if they must show 0. NULL amounts are ignored. Transfers to self net to zero.

**Likely follow-ups:** 1) Show received and sent as separate columns? Use SUM(CASE ...) over the stacked rows with a direction column. 2) Why not two joins? Joining twice risks missing accounts that appear on only one side.

**Common mistakes:** Using UNION and losing duplicate transfers. Doing an inner join of received and sent totals, dropping accounts that only received or sent. Getting the sign backwards.

### Q50 ⭐⭐ 🔴 Sales: For each quarter, find the region with the highest sales, keeping all regions in case of a tie.

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Top-N per group with ties: knowing RANK vs ROW_NUMBER, and aggregating before ranking.

**Say this in the interview:** "I total sales per quarter and region, then use RANK partitioned by quarter ordered by total descending, and keep rank 1. RANK gives tied regions the same rank, so ties are all kept; ROW_NUMBER would drop one."

**Explain simply:**
- Step 1: total per quarter and region (GROUP BY).
- Step 2: RANK() OVER (PARTITION BY quarter ORDER BY total DESC) numbers regions within each quarter; ties share a rank.
- Step 3: filter rank = 1 in an outer query, since window functions cannot go in WHERE.
- Q2 2025 has a tie (South and East, 400 each), and both show.

**Example:** Like finding the top department by hires each quarter, and showing both if two are level.

**Sample data:**
`sales`

| sale_id | region | sale_date | amount |
|---|---|---|---|
| 1 | North | 2025-01-10 | 500 |
| 2 | South | 2025-02-10 | 300 |
| 3 | East | 2025-03-10 | 200 |
| 4 | North | 2025-04-10 | 100 |
| 5 | South | 2025-05-10 | 400 |
| 6 | East | 2025-06-10 | 400 |
| 7 | North | 2025-07-10 | 600 |
| 8 | South | 2025-08-10 | 100 |
| 9 | East | 2025-09-10 | 50 |
| 10 | North | 2025-10-10 | 700 |

**SQL:**
```sql
WITH q AS (
    SELECT STRFTIME('%Y', sale_date) || '-Q' || ((CAST(STRFTIME('%m', sale_date) AS INTEGER) + 2) / 3) AS quarter,
           region, SUM(amount) AS total_sales
    FROM sales
    GROUP BY 1, 2
),
ranked AS (
    SELECT *, RANK() OVER (PARTITION BY quarter ORDER BY total_sales DESC) AS rnk
    FROM q
)
SELECT quarter, region, total_sales
FROM ranked
WHERE rnk = 1
ORDER BY quarter, region;
```

**Output:**
| quarter | region | total_sales |
|---|---|---|
| 2025-Q1 | North | 500 |
| 2025-Q2 | East | 400 |
| 2025-Q2 | South | 400 |
| 2025-Q3 | North | 600 |
| 2025-Q4 | North | 700 |

**pandas equivalent:**
```python
# DataFrames named like the tables above (e.g. transactions = pd.DataFrame(...))
s = sales.copy()
d = pd.to_datetime(s.sale_date)
s['quarter'] = d.dt.year.astype(str) + '-Q' + ((d.dt.month + 2) // 3).astype(str)
q = s.groupby(['quarter','region'], as_index=False)['amount'].sum().rename(columns={'amount':'total_sales'})
q['top'] = q.groupby('quarter')['total_sales'].transform('max')
result = q[q.total_sales == q.top][['quarter','region','total_sales']].sort_values(['quarter','region'])
```
(Each pandas result was run and matches the SQL output above.)

**Edge cases:** Tie handled by RANK. If there are several years, the year is part of the quarter label. Regions with no sales in a quarter do not compete (add zero rows if needed). NULL amounts are ignored in SUM.

**Likely follow-ups:** 1) What if you want only one winner? Use ROW_NUMBER with a tie-break column. 2) DENSE_RANK difference? No gaps after ties; irrelevant for rank 1.

**Common mistakes:** Using ROW_NUMBER (silently drops tied regions). Using MAX(total) with GROUP BY and losing the region name. Forgetting the year.

### Q51 ⭐ 🟢 HR: Group employees into salary bands (below 30k, 30-60k, 60-100k, above 100k) and count each band.

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** CASE WHEN for bucketing, boundary handling, and group-by on the derived label.

**Say this in the interview:** "I use a CASE expression to label each salary with its band, checking from the lowest band upward so each row takes the first match, then GROUP BY that label and COUNT."

**Explain simply:**
- CASE checks conditions top to bottom and stops at the first true one, so '< 60000' automatically means 30000 to 59999.
- Pick and state the boundaries: here 30,000 belongs to 30-60k, 60,000 to 60-100k, 100,000 to Above 100k.
- A number prefix in the label keeps bands in the right order when sorted.

**Example:** Like HR grouping staff into pay grades to see how many sit in each.

**Sample data:**
`employees`

| emp_id | name | salary |
|---|---|---|
| 1 | Asha | 25000 |
| 2 | Ravi | 30000 |
| 3 | Meera | 45000 |
| 4 | Kabir | 60000 |
| 5 | Neha | 85000 |
| 6 | Omar | 100000 |
| 7 | Priya | 150000 |
| 8 | Sam | 29999 |
| 9 | Tara | NULL |

**SQL:**
```sql
SELECT CASE WHEN salary < 30000  THEN '1. Below 30k'
            WHEN salary < 60000  THEN '2. 30-60k'
            WHEN salary < 100000 THEN '3. 60-100k'
            WHEN salary >= 100000 THEN '4. Above 100k'
            ELSE '5. Unknown (NULL)' END AS salary_band,
       COUNT(*) AS employees
FROM employees
GROUP BY salary_band
ORDER BY salary_band;
```

**Output:**
| salary_band | employees |
|---|---|
| 1. Below 30k | 2 |
| 2. 30-60k | 2 |
| 3. 60-100k | 2 |
| 4. Above 100k | 2 |
| 5. Unknown (NULL) | 1 |

**pandas equivalent:**
```python
# DataFrames named like the tables above (e.g. transactions = pd.DataFrame(...))
def band(s):
    if pd.isna(s): return '5. Unknown (NULL)'
    if s < 30000: return '1. Below 30k'
    if s < 60000: return '2. 30-60k'
    if s < 100000: return '3. 60-100k'
    return '4. Above 100k'
e = employees.copy(); e['salary_band'] = e.salary.map(band)
result = e.groupby('salary_band', as_index=False).size().rename(columns={'size':'employees'}).sort_values('salary_band')
```
(Each pandas result was run and matches the SQL output above.)

**Edge cases:** NULL salary matches none of the numeric conditions, so it needs its own label (else it would silently fall in ELSE). 29,999 vs 30,000 is the boundary test. A band with zero employees will not appear unless you LEFT JOIN from a bands table.

**Likely follow-ups:** 1) Show empty bands too? Build a bands table and LEFT JOIN. 2) Percentage per band? Divide by SUM(COUNT(*)) OVER ().

**Common mistakes:** Overlapping ranges using BETWEEN 30000 AND 60000 and BETWEEN 60000 AND 100000 (60,000 would be in both). Putting the ELSE band as 'Above 100k' so NULLs land there.

### Q52 ⭐ 🟢 HR: List employees whose work anniversary falls in the current month.

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Extracting month from a date and comparing it with the current month, plus thinking about the same-year joiner.

**Say this in the interview:** "I compare the month of the joining date to the current month, and require the joining year to be earlier so new joiners this month are not shown as having an anniversary."

**Explain simply:**
- I fixed 'today' as 15 Oct 2025 so the result is repeatable. In real use replace '2025-10-15' with date('now') in SQLite, CURRENT_DATE in PostgreSQL/MySQL, GETDATE() in SQL Server.
- Month extraction: strftime('%m') in SQLite, MONTH() in MySQL/SQL Server, EXTRACT(MONTH FROM ...) in PostgreSQL (not run here / from memory).
- Years completed = current year minus joining year.

**Example:** HR sends work-anniversary greetings each month; this is the monthly list.

**Sample data:**
`employees`

| emp_id | name | join_date |
|---|---|---|
| 1 | Asha | 2018-10-05 |
| 2 | Ravi | 2021-10-28 |
| 3 | Meera | 2022-03-15 |
| 4 | Kabir | 2025-10-02 |
| 5 | Neha | 2020-09-30 |
| 6 | Omar | 2019-10-15 |

**SQL:**
```sql
SELECT name, join_date,
       CAST(STRFTIME('%Y', '2025-10-15') AS INTEGER) - CAST(STRFTIME('%Y', join_date) AS INTEGER) AS years_completed
FROM employees
WHERE STRFTIME('%m', join_date) = STRFTIME('%m', '2025-10-15')
  AND STRFTIME('%Y', join_date) < STRFTIME('%Y', '2025-10-15')
ORDER BY STRFTIME('%d', join_date);
```

**Output:**
| name | join_date | years_completed |
|---|---|---|
| Asha | 2018-10-05 | 7 |
| Omar | 2019-10-15 | 6 |
| Ravi | 2021-10-28 | 4 |

**pandas equivalent:**
```python
# DataFrames named like the tables above (e.g. transactions = pd.DataFrame(...))
e = employees.copy()
j = pd.to_datetime(e.join_date)
e['years_completed'] = 2025 - j.dt.year
r = e[(j.dt.month == 10) & (j.dt.year < 2025)].copy()
r['d'] = pd.to_datetime(r.join_date).dt.day
result = r.sort_values('d')[['name','join_date','years_completed']]
```
(Each pandas result was run and matches the SQL output above.)

**Edge cases:** Kabir joined this month this year (0 years), so he is excluded. Joiners on 29 Feb have anniversaries on 28 Feb or 1 Mar in non-leap years. NULL join_date drops out. Left employees should be filtered out with a status/left_date condition.

**Likely follow-ups:** 1) Anniversaries in the next 7 days? Compare month-day strings, handling year-end wrap. 2) Include only active staff? Add WHERE left_date IS NULL.

**Common mistakes:** Comparing full dates instead of month. Including this year's joiners. Hard-coding the month number.

### Q53 ⭐ 🟢 E-commerce: Compare average order value of orders that used a coupon with those that did not.

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Splitting rows into two groups on a NULL test and using AVG.

**Say this in the interview:** "A NULL coupon code means no coupon was used, so I label each order Coupon or No coupon with CASE and compute the average amount per label."

**Explain simply:**
- Average order value (AOV) = total sales / number of orders.
- Here coupon_code is NULL when no coupon was applied; if your data stores empty text or 'NONE', test for that instead.
- Show the count too so nobody over-reads an average from three orders.

**Example:** Like comparing average salary of employees who got a referral bonus and those who did not.

**Sample data:**
`orders`

| order_id | amount | coupon_code |
|---|---|---|
| 1 | 1000 | SAVE10 |
| 2 | 800 | NULL |
| 3 | 1200 | SAVE10 |
| 4 | 600 | NULL |
| 5 | 900 | NEW5 |
| 6 | 700 | NULL |
| 7 | 500 | NULL |
| 8 | 1100 | SAVE10 |

**SQL:**
```sql
SELECT CASE WHEN coupon_code IS NOT NULL THEN 'Coupon' ELSE 'No coupon' END AS order_type,
       COUNT(*) AS orders,
       ROUND(AVG(amount), 1) AS avg_order_value
FROM orders
GROUP BY order_type
ORDER BY order_type;
```

**Output:**
| order_type | orders | avg_order_value |
|---|---|---|
| Coupon | 4 | 1050 |
| No coupon | 4 | 650 |

**pandas equivalent:**
```python
# DataFrames named like the tables above (e.g. transactions = pd.DataFrame(...))
o = orders.copy()
o['order_type'] = o.coupon_code.map(lambda c: 'No coupon' if pd.isna(c) else 'Coupon')
g = o.groupby('order_type', as_index=False).agg(orders=('order_id','count'), avg_order_value=('amount','mean'))
g['avg_order_value'] = g.avg_order_value.round(1)
result = g.sort_values('order_type')
```
(Each pandas result was run and matches the SQL output above.)

**Edge cases:** Empty-string coupon codes look non-NULL but mean no coupon. Orders with NULL amount are ignored by AVG. Refunded or cancelled orders may need filtering first.

**Likely follow-ups:** 1) Is the difference significant? Needs a statistical test, SQL only gives the averages. 2) Discount-adjusted? Use amount after discount consistently.

**Common mistakes:** Writing coupon_code = NULL (never true; use IS NULL). Averaging averages across groups.

### Q54 ⭐ 🟢 Sales: Show the number of customers per city, largest first.

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Basic GROUP BY with COUNT and ORDER BY DESC, and a tie-breaker.

**Say this in the interview:** "GROUP BY city, COUNT the rows, and ORDER BY the count descending. I add city as a second sort key so ties come out in a stable order."

**Explain simply:**
- COUNT(*) counts rows in each city.
- ORDER BY can use the alias 'customers' from the SELECT.
- Use COUNT(DISTINCT customer_id) if the table could hold duplicate customer rows.

**Example:** Like headcount by office location in HR.

**Sample data:**
`customers`

| customer_id | name | city |
|---|---|---|
| 1 | Asha | Mumbai |
| 2 | Ravi | Mumbai |
| 3 | Meera | Mumbai |
| 4 | Kabir | Delhi |
| 5 | Neha | Delhi |
| 6 | Omar | Pune |
| 7 | Priya | Pune |
| 8 | Sam | Chennai |
| 9 | Tara | Mumbai |

**SQL:**
```sql
SELECT city, COUNT(*) AS customers
FROM customers
GROUP BY city
ORDER BY customers DESC, city;
```

**Output:**
| city | customers |
|---|---|
| Mumbai | 4 |
| Delhi | 2 |
| Pune | 2 |
| Chennai | 1 |

**pandas equivalent:**
```python
# DataFrames named like the tables above (e.g. transactions = pd.DataFrame(...))
result = customers.groupby('city', as_index=False).size().rename(columns={'size':'customers'}).sort_values(['customers','city'], ascending=[False, True])
```
(Each pandas result was run and matches the SQL output above.)

**Edge cases:** NULL city forms its own group (shown as NULL). Pune and Delhi tie at 2, so the second sort key decides. Spelling variants ('Mumbai', 'mumbai ') split groups; clean with TRIM/UPPER.

**Likely follow-ups:** 1) Top 3 cities only? Add LIMIT 3 (TOP 3 in SQL Server, FETCH FIRST 3 ROWS ONLY in Oracle/PostgreSQL). 2) Percentage share? Divide by SUM(COUNT(*)) OVER ().

**Common mistakes:** Using COUNT(city) and missing NULL-city customers. Forgetting DESC. Not cleaning city spellings.

### Q55 ⭐ 🟡 HR: Find the headcount of active employees on a given date (for example 30 Sep 2025), by department.

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Point-in-time (as-of date) logic: joined on or before the date and not yet left.

**Say this in the interview:** "Someone is active on a date if they joined on or before it and either have no left date or left on or after it. I count those by department."

**Explain simply:**
- Two conditions: join_date <= D, and left_date is NULL or >= D.
- I treat the left date as the last working day, so someone leaving on 30 Sep is still counted that day. Change to > if the left date is the first day away.
- The OR with IS NULL matters: comparing NULL with a date never gives true.

**Example:** HR month-end headcount report: how many people were on the rolls on 30 Sep.

**Sample data:**
`employees`

| emp_id | name | department | join_date | left_date |
|---|---|---|---|---|
| 1 | Asha | HR | 2020-01-01 | NULL |
| 2 | Ravi | HR | 2024-06-01 | 2025-09-30 |
| 3 | Meera | HR | 2025-10-15 | NULL |
| 4 | Kabir | IT | 2019-05-01 | NULL |
| 5 | Neha | IT | 2023-02-01 | 2025-06-30 |
| 6 | Omar | IT | 2025-09-30 | NULL |
| 7 | Priya | Sales | 2021-03-01 | 2025-09-29 |
| 8 | Sam | Sales | 2022-04-01 | NULL |

**SQL:**
```sql
SELECT department, COUNT(*) AS active_headcount
FROM employees
WHERE join_date <= '2025-09-30'
  AND (left_date IS NULL OR left_date >= '2025-09-30')
GROUP BY department
ORDER BY department;
```

**Output:**
| department | active_headcount |
|---|---|
| HR | 2 |
| IT | 2 |
| Sales | 1 |

**pandas equivalent:**
```python
# DataFrames named like the tables above (e.g. transactions = pd.DataFrame(...))
d = '2025-09-30'
e = employees[(employees.join_date <= d) & (employees.left_date.isna() | (employees.left_date >= d))]
result = e.groupby('department', as_index=False).size().rename(columns={'size':'active_headcount'}).sort_values('department')
```
(Each pandas result was run and matches the SQL output above.)

**Edge cases:** Meera joins after the date and is excluded. Priya left the day before and is excluded. Departments with zero active people vanish; LEFT JOIN from a departments table to show 0. Rejoiners need one row per stint.

**Likely follow-ups:** 1) Headcount for every month-end? Join to a calendar/dates table. 2) Why not just WHERE left_date IS NULL? That gives today's headcount, not as of a past date.

**Common mistakes:** Forgetting the join_date check, counting future joiners. Not handling NULL left_date. Mixing > and >= without stating the rule.

### Q56 ⭐ 🟡 HR: Calculate each department's average salary after excluding its highest and lowest paid employee.

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Window functions with ROW_NUMBER in both directions to drop the top and bottom row per group (a 'trimmed mean').

**Say this in the interview:** "I number employees in each department from lowest and from highest with ROW_NUMBER, drop rank 1 in either direction, and average the rest."

**Explain simply:**
- ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary) numbers rows inside each department.
- Doing it ascending and descending lets one filter remove both the lowest and highest.
- This is a trimmed average: it protects the average from outliers like one very high salary.
- ROW_NUMBER removes exactly one lowest and one highest even with ties (IT has two at 40,000: only one is removed).

**Example:** HR wants the typical department salary without the CEO-level outlier or the intern.

**Sample data:**
`employees`

| emp_id | name | department | salary |
|---|---|---|---|
| 1 | A | HR | 30000 |
| 2 | B | HR | 40000 |
| 3 | C | HR | 50000 |
| 4 | D | HR | 60000 |
| 5 | E | HR | 90000 |
| 6 | F | IT | 40000 |
| 7 | G | IT | 40000 |
| 8 | H | IT | 70000 |
| 9 | I | IT | 80000 |
| 10 | J | Sales | 35000 |
| 11 | K | Sales | 45000 |
| 12 | L | Sales | 55000 |

**SQL:**
```sql
WITH r AS (
    SELECT department, salary,
           ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary ASC)  AS rn_low,
           ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rn_high
    FROM employees
)
SELECT department, ROUND(AVG(salary), 1) AS avg_salary_trimmed, COUNT(*) AS employees_used
FROM r
WHERE rn_low > 1 AND rn_high > 1
GROUP BY department
ORDER BY department;
```

**Output:**
| department | avg_salary_trimmed | employees_used |
|---|---|---|
| HR | 50000 | 3 |
| IT | 55000 | 2 |
| Sales | 45000 | 1 |

**pandas equivalent:**
```python
# DataFrames named like the tables above (e.g. transactions = pd.DataFrame(...))
rows = []
for dept, g in employees.groupby('department'):
    s = g.salary.sort_values().iloc[1:-1]
    if len(s): rows.append((dept, round(s.mean(), 1), len(s)))
result = pd.DataFrame(rows, columns=['department','avg_salary_trimmed','employees_used'])
```
(Each pandas result was run and matches the SQL output above.)

**Edge cases:** A department with 2 or fewer employees leaves nothing, so it disappears (Sales has 3, so only 1 employee is used; a 2-person department would vanish). If ties should ALL be removed, compare salary to MIN/MAX per department instead. NULL salaries sort first in SQLite, filter them out.

**Likely follow-ups:** 1) Remove ties for min/max entirely? Use salary > MIN and < MAX via window MIN/MAX. 2) Median instead? PERCENTILE_CONT in PostgreSQL/SQL Server (not run here).

**Common mistakes:** Using RANK, which can remove several tied rows or none. Using LIMIT/OFFSET per group (not possible). Ignoring tiny departments.

### Q57 ⭐ 🟡 HR: Find pairs of employees in the same department with identical salary.

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Self-join with a condition that avoids duplicate and self pairs (a.emp_id < b.emp_id).

**Say this in the interview:** "I join the employees table to itself on same department and same salary, and add a.emp_id < b.emp_id so a person is not paired with themselves and each pair appears once."

**Explain simply:**
- A self-join treats one table as two copies (a and b) to compare rows with each other.
- Without a.emp_id < b.emp_id you get (Asha, Asha) and both (Asha, Ravi) and (Ravi, Asha).
- Three people with the same salary produce three pairs (n x (n-1) / 2); HR has Asha, Ravi, Priya at 50,000 so three pairs.
- Omar earns 50,000 too but is in IT, so he is not paired with HR.

**Example:** Like HR checking pay equity: who in the same team earns exactly the same?

**Sample data:**
`employees`

| emp_id | name | department | salary |
|---|---|---|---|
| 1 | Asha | HR | 50000 |
| 2 | Ravi | HR | 50000 |
| 3 | Meera | HR | 60000 |
| 4 | Kabir | IT | 70000 |
| 5 | Neha | IT | 70000 |
| 6 | Omar | IT | 50000 |
| 7 | Priya | HR | 50000 |

**SQL:**
```sql
SELECT a.department, a.name AS employee_1, b.name AS employee_2, a.salary
FROM employees a
JOIN employees b
  ON a.department = b.department
 AND a.salary = b.salary
 AND a.emp_id < b.emp_id
ORDER BY a.department, a.emp_id, b.emp_id;
```

**Output:**
| department | employee_1 | employee_2 | salary |
|---|---|---|---|
| HR | Asha | Ravi | 50000 |
| HR | Asha | Priya | 50000 |
| HR | Ravi | Priya | 50000 |
| IT | Kabir | Neha | 70000 |

**pandas equivalent:**
```python
# DataFrames named like the tables above (e.g. transactions = pd.DataFrame(...))
m = employees.merge(employees, on=['department','salary'], suffixes=('_1','_2'))
m = m[m.emp_id_1 < m.emp_id_2].sort_values(['department','emp_id_1','emp_id_2'])
result = m.rename(columns={'name_1':'employee_1','name_2':'employee_2'})[['department','employee_1','employee_2','salary']]
```
(Each pandas result was run and matches the SQL output above.)

**Edge cases:** Groups of three or more give several pairs. NULL salaries never match (NULL = NULL is not true). Duplicate employee rows would create false pairs, so check emp_id is unique.

**Likely follow-ups:** 1) Only list salaries that are shared, not pairs? GROUP BY department, salary HAVING COUNT(*) > 1. 2) Why < and not <>? <> gives each pair twice.

**Common mistakes:** Using <> and getting mirrored duplicates. Forgetting the department condition. Using a.name < b.name where names repeat.

### Q58 ⭐ 🟡 HR/payroll: Find salary payments in `payroll` made to employees after their left_date (payroll audit).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can compare two dates across tables with a join and know that NULL (no left date) means 'still working'.
**Say this in the interview:** I join payroll to employees and keep only rows where the pay date is later than the left date. Active staff have a NULL left date, so they drop out of the comparison automatically.
**Explain simply:**
- A **join** lines up each payroll row with its employee's row so both dates sit side by side.
- **NULL** means 'unknown/none'. Any comparison with NULL is neither true nor false, so the row is filtered out. That is exactly what we want for people who have not left.
- Dates stored as `YYYY-MM-DD` compare correctly as plain text or as real DATE columns.
- Every row returned is a payment worth investigating: it could be a fraud, a ghost employee, or a legitimate final settlement.
**Example:** Asha left on 31 March but was still paid on 30 April and 31 May: Rs 1,00,000 paid out after exit, so HR/finance recovers it.
**Sample data:**

`employees`

| emp_id | name | left_date |
|---|---|---|
| 1 | Asha | 2025-03-31 |
| 2 | Ravi | 2025-05-15 |
| 3 | Meena | NULL |
| 4 | Karan | 2025-02-28 |
| 5 | Divya | NULL |

`payroll`

| emp_id | pay_date | amount |
|---|---|---|
| 1 | 2025-03-31 | 50000 |
| 1 | 2025-04-30 | 50000 |
| 1 | 2025-05-31 | 50000 |
| 2 | 2025-04-30 | 62000 |
| 2 | 2025-05-31 | 62000 |
| 3 | 2025-05-31 | 58000 |
| 4 | 2025-02-28 | 45000 |
| 5 | 2025-05-31 | 70000 |

**SQL:**
```sql
SELECT e.emp_id, e.name, e.left_date, p.pay_date, p.amount
FROM payroll p
JOIN employees e ON e.emp_id = p.emp_id
WHERE p.pay_date > e.left_date          -- NULL left_date => row filtered out
ORDER BY e.emp_id, p.pay_date;
```

**Output:**

| emp_id | name | left_date | pay_date | amount |
|---|---|---|---|---|
| 1 | Asha | 2025-03-31 | 2025-04-30 | 50000 |
| 1 | Asha | 2025-03-31 | 2025-05-31 | 50000 |
| 2 | Ravi | 2025-05-15 | 2025-05-31 | 62000 |

**pandas equivalent:**
```python
# employees and payroll are DataFrames with the same columns as the tables
m = payroll.merge(employees, on="emp_id")
late = m["left_date"].notna() & (pd.to_datetime(m["pay_date"]) > pd.to_datetime(m["left_date"]))
result = (m[late][["emp_id","name","left_date","pay_date","amount"]]
          .sort_values(["emp_id","pay_date"]).reset_index(drop=True))
```
Result (actual run):
```text
 emp_id name  left_date   pay_date  amount
      1 Asha 2025-03-31 2025-04-30   50000
      1 Asha 2025-03-31 2025-05-31   50000
      2 Ravi 2025-05-15 2025-05-31   62000
```
**Edge cases:** NULL left_date (still employed) is excluded automatically. Payment on the exact left date is not flagged (`>` not `>=`). Ravi's 31 May payment is only 16 days after exit, so it may be a legitimate final settlement; the query finds candidates, a human confirms. If dates are stored as text in other formats (`DD-MM-YYYY`) the text comparison silently breaks, so convert first.
**Likely follow-ups:**
- How much was overpaid per employee? Wrap in `SELECT e.emp_id, SUM(p.amount) ... GROUP BY e.emp_id`.
- How do you also catch employees missing from the employee table? Use a LEFT JOIN from payroll and filter `e.emp_id IS NULL` (ghost payments).
**Common mistakes:** Using `>=` (flags the legitimate last pay), forgetting that NULL left dates are active staff, or comparing a text date in `DD/MM/YYYY` format.

### Q59 ⭐ 🟡 E-commerce: Reconcile data: find orders where the order total does not equal the sum of its item lines.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you aggregate the child table first and then join, and whether you remember orders with no item lines at all.
**Say this in the interview:** I total qty times unit price per order in a subquery, LEFT JOIN that to orders, and list the orders where the header total and the line total differ. The LEFT JOIN with COALESCE catches orders that have no lines.
**Explain simply:**
- **Reconciliation** means checking that two sources that should agree actually do.
- Summarise `order_items` to one row per order first (`GROUP BY order_id`). If you join first and sum later you can double count the header total.
- A **LEFT JOIN** keeps every order even if it has no lines; the missing sum comes back as NULL, and `COALESCE(x, 0)` turns it into 0.
**Example:** Order 1002 header says 1,800 but lines add up to 1,600: Rs 200 gap (maybe shipping not stored as a line). Order 1004 has a total of 600 and no lines at all.
**Sample data:**

`orders`

| order_id | order_total |
|---|---|
| 1001 | 2500 |
| 1002 | 1800 |
| 1003 | 900 |
| 1004 | 600 |
| 1005 | 1200 |

`order_items`

| order_id | line_no | qty | unit_price |
|---|---|---|---|
| 1001 | 1 | 2 | 500 |
| 1001 | 2 | 1 | 1500 |
| 1002 | 1 | 1 | 1000 |
| 1002 | 2 | 2 | 300 |
| 1003 | 1 | 3 | 300 |
| 1005 | 1 | 5 | 250 |

**SQL:**
```sql
SELECT o.order_id,
       o.order_total,
       COALESCE(i.items_sum, 0)                  AS items_sum,
       o.order_total - COALESCE(i.items_sum, 0)  AS diff
FROM orders o
LEFT JOIN (SELECT order_id, SUM(qty * unit_price) AS items_sum
           FROM order_items
           GROUP BY order_id) i ON i.order_id = o.order_id
WHERE o.order_total <> COALESCE(i.items_sum, 0)
ORDER BY o.order_id;
```

**Output:**

| order_id | order_total | items_sum | diff |
|---|---|---|---|
| 1002 | 1800 | 1600 | 200 |
| 1004 | 600 | 0 | 600 |
| 1005 | 1200 | 1250 | -50 |

**pandas equivalent:**
```python
items = order_items.assign(line_amt=order_items["qty"] * order_items["unit_price"]) \
                   .groupby("order_id", as_index=False)["line_amt"].sum() \
                   .rename(columns={"line_amt": "items_sum"})
m = orders.merge(items, on="order_id", how="left").fillna({"items_sum": 0})
m["diff"] = m["order_total"] - m["items_sum"]
result = m[m["diff"] != 0].sort_values("order_id").reset_index(drop=True)
```
Result (actual run):
```text
 order_id  order_total  items_sum  diff
     1002         1800     1600.0 200.0
     1004          600        0.0 600.0
     1005         1200     1250.0 -50.0
```
**Edge cases:** Orders with no lines (1004) only show up because of the LEFT JOIN. With decimal money, compare with a tolerance (`ABS(diff) > 0.01`) to avoid rounding noise. Lines whose order_id is missing from `orders` (orphans) need the reverse check: `order_items` LEFT JOIN `orders` where `o.order_id IS NULL`. Discounts, tax and shipping often explain legitimate gaps.
**Likely follow-ups:**
- How do you find orphan item lines? LEFT JOIN from order_items to orders and filter on NULL.
- Why not join first and then SUM? The header total repeats on every line and gets multiplied.
**Common mistakes:** Using an inner join (misses orders without lines), joining before aggregating (inflated totals), and comparing floats with `=`.

### Q60 ⭐ 🟡 Banking: Find customers holding accounts in more than one branch.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know DISTINCT inside COUNT and HAVING, and can tell 'many accounts' from 'many branches'.
**Say this in the interview:** I group accounts by customer and keep those with COUNT(DISTINCT branch) greater than 1. DISTINCT matters because Ravi has two accounts but both are in Pune.
**Explain simply:**
- **GROUP BY customer** gives one row per customer; `COUNT(DISTINCT branch)` counts different branches, not rows.
- **HAVING** filters after grouping (WHERE cannot see aggregates).
- `GROUP_CONCAT` (SQLite/MySQL) lists the branches in one cell; PostgreSQL uses `STRING_AGG`, SQL Server `STRING_AGG` too (not run here).
**Example:** Asha has Mumbai and Pune accounts, so she is flagged. Ravi has two Pune accounts, so he is not.
**Sample data:**

`customers`

| customer_id | name |
|---|---|
| 1 | Asha |
| 2 | Ravi |
| 3 | Meena |
| 4 | Karan |

`accounts`

| account_id | customer_id | branch |
|---|---|---|
| 1 | 1 | Mumbai |
| 2 | 1 | Pune |
| 3 | 2 | Pune |
| 4 | 2 | Pune |
| 5 | 3 | Chennai |
| 6 | 3 | Delhi |
| 7 | 3 | Pune |
| 8 | 4 | Delhi |

**SQL:**
```sql
SELECT c.customer_id, c.name,
       COUNT(DISTINCT a.branch)  AS branches,
       GROUP_CONCAT(DISTINCT a.branch) AS branch_list   -- SQLite/MySQL; PostgreSQL: STRING_AGG(DISTINCT ..., ',')
FROM accounts a
JOIN customers c ON c.customer_id = a.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(DISTINCT a.branch) > 1
ORDER BY c.customer_id;
```

**Output:**

| customer_id | name | branches | branch_list |
|---|---|---|---|
| 1 | Asha | 2 | Mumbai,Pune |
| 3 | Meena | 3 | Chennai,Delhi,Pune |

**pandas equivalent:**
```python
g = accounts.merge(customers, on="customer_id").groupby(["customer_id","name"])["branch"]
r = g.agg(branches="nunique", branch_list=lambda s: ",".join(sorted(set(s)))).reset_index()
result = r[r["branches"] > 1].sort_values("customer_id").reset_index(drop=True)
```
Result (actual run):
```text
 customer_id  name  branches        branch_list
           1  Asha         2        Mumbai,Pune
           3 Meena         3 Chennai,Delhi,Pune
```
**Edge cases:** Without DISTINCT, Ravi (2 accounts, 1 branch) would wrongly appear. NULL branch values are ignored by COUNT(DISTINCT). Order inside GROUP_CONCAT is not guaranteed in SQLite, so do not rely on it. Customers with no accounts do not appear (inner join).
**Likely follow-ups:**
- Customers with more than one account at all? Use COUNT(*) instead of COUNT(DISTINCT branch).
- Customers with accounts in exactly one branch? `HAVING COUNT(DISTINCT branch) = 1`.
**Common mistakes:** Writing `HAVING COUNT(branch) > 1` (counts accounts, not branches) or putting the aggregate in WHERE.

### Q61 ⭐ 🟡 HR/recruitment: Calculate the offer-acceptance rate per recruiter (offers accepted divided by offers made).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Conditional aggregation and avoiding integer division.
**Say this in the interview:** I count all offers per recruiter and count how many of them are accepted using a CASE inside SUM, then divide, multiplying by 100.0 so the answer is a decimal, not a rounded-down integer.
**Explain simply:**
- **Conditional aggregation**: `SUM(CASE WHEN status='accepted' THEN 1 ELSE 0 END)` counts only rows that meet a condition.
- **Integer division** trap: in SQLite, SQL Server and PostgreSQL, `3/4` between two whole numbers gives 0. Multiply by `100.0` first to force decimals.
- 'Offers made' includes pending ones here, as the question states; I show the pending count so nobody is misled.
**Example:** Priya made 4 offers and 3 were accepted: 75%. Nisha made 3 offers and none accepted yet: 0%, with 1 still pending.
**Sample data:**

`offers`

| offer_id | recruiter | status |
|---|---|---|
| 1 | Priya | accepted |
| 2 | Priya | accepted |
| 3 | Priya | declined |
| 4 | Priya | accepted |
| 5 | Sam | accepted |
| 6 | Sam | declined |
| 7 | Sam | declined |
| 8 | Sam | accepted |
| 9 | Sam | pending |
| 10 | Nisha | declined |
| 11 | Nisha | pending |
| 12 | Nisha | declined |

**SQL:**
```sql
SELECT recruiter,
       COUNT(*)                                          AS offers_made,
       SUM(CASE WHEN status = 'accepted' THEN 1 ELSE 0 END) AS accepted,
       SUM(CASE WHEN status = 'pending'  THEN 1 ELSE 0 END) AS pending,
       ROUND(100.0 * SUM(CASE WHEN status = 'accepted' THEN 1 ELSE 0 END) / COUNT(*), 1) AS acceptance_pct
FROM offers
GROUP BY recruiter
ORDER BY acceptance_pct DESC, recruiter;
```

**Output:**

| recruiter | offers_made | accepted | pending | acceptance_pct |
|---|---|---|---|---|
| Priya | 4 | 3 | 0 | 75.0 |
| Sam | 5 | 2 | 1 | 40.0 |
| Nisha | 3 | 0 | 1 | 0.0 |

**pandas equivalent:**
```python
g = offers.groupby("recruiter")["status"]
r = pd.DataFrame({"offers_made": g.size(),
                  "accepted": g.apply(lambda s: (s == "accepted").sum()),
                  "pending": g.apply(lambda s: (s == "pending").sum())}).reset_index()
r["acceptance_pct"] = (100.0 * r["accepted"] / r["offers_made"]).round(1)
result = r.sort_values(["acceptance_pct","recruiter"], ascending=[False,True]).reset_index(drop=True)
```
Result (actual run):
```text
recruiter  offers_made  accepted  pending  acceptance_pct
    Priya            4         3        0            75.0
      Sam            5         2        1            40.0
    Nisha            3         0        1             0.0
```
**Edge cases:** Pending offers drag the rate down unfairly; a fairer rate divides by decided offers (`COUNT(*) - pending`), so state which one you used. A recruiter with zero offers does not appear unless you start from a recruiters table with LEFT JOIN, and then use NULLIF(COUNT(*),0) to avoid divide-by-zero (error in PostgreSQL/SQL Server).
**Likely follow-ups:**
- How do you make it a fair rate? Exclude pending from the denominator.
- How do you avoid divide by zero? `/ NULLIF(denominator, 0)`.
**Common mistakes:** Integer division returning 0, counting with `COUNT(status)` and no condition, and not stating how pending offers are treated.

### Q62 ⭐ 🟡 HR: Using `training_assignments` (emp_id, course_id, completed_date), find training completion rate per department.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Counting NULLs correctly (completed_date NULL means not completed), multi-table LEFT JOINs and safe division.
**Say this in the interview:** I count assignments with COUNT of a non-null column and completions with COUNT(completed_date), because COUNT ignores NULLs. I LEFT JOIN from departments so a department with no assignments still shows, and guard the division with NULLIF.
**Explain simply:**
- `COUNT(column)` counts only non-NULL values; `COUNT(*)` counts rows. So `COUNT(completed_date)` = number of finished courses.
- Start from `departments` and LEFT JOIN down, so empty departments are not lost.
- **NULLIF(x, 0)** returns NULL when x is 0, so the division gives NULL instead of crashing.
**Example:** Sales has 3 assignments and 1 completed: 33.3%. Legal has employees but no assigned training: NULL, not 0%.
**Sample data:**

`departments`

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Sales |
| 3 | Tech |
| 4 | Legal |

`employees`

| emp_id | name | dept_id |
|---|---|---|
| 1 | Asha | 1 |
| 2 | Ravi | 2 |
| 3 | Meena | 2 |
| 4 | Karan | 3 |
| 5 | Divya | 3 |
| 6 | Neha | 4 |

`training_assignments`

| emp_id | course_id | completed_date |
|---|---|---|
| 1 | 101 | 2025-02-10 |
| 1 | 102 | NULL |
| 2 | 101 | 2025-03-01 |
| 3 | 101 | NULL |
| 3 | 103 | NULL |
| 4 | 102 | 2025-04-12 |
| 5 | 102 | 2025-04-15 |
| 5 | 103 | 2025-05-02 |

**SQL:**
```sql
SELECT d.dept_name,
       COUNT(t.course_id)       AS assigned,
       COUNT(t.completed_date)  AS completed,
       ROUND(100.0 * COUNT(t.completed_date) / NULLIF(COUNT(t.course_id), 0), 1) AS completion_pct
FROM departments d
LEFT JOIN employees e             ON e.dept_id = d.dept_id
LEFT JOIN training_assignments t  ON t.emp_id  = e.emp_id
GROUP BY d.dept_id, d.dept_name
ORDER BY d.dept_name;
```

**Output:**

| dept_name | assigned | completed | completion_pct |
|---|---|---|---|
| HR | 2 | 1 | 50.0 |
| Legal | 0 | 0 | NULL |
| Sales | 3 | 1 | 33.3 |
| Tech | 3 | 3 | 100.0 |

**pandas equivalent:**
```python
m = (departments.merge(employees, on="dept_id", how="left")
                .merge(training_assignments, on="emp_id", how="left"))
r = m.groupby("dept_name").agg(assigned=("course_id","count"), completed=("completed_date","count")).reset_index()
r["completion_pct"] = (100.0 * r["completed"] / r["assigned"].where(r["assigned"] != 0)).round(1)
result = r.sort_values("dept_name").reset_index(drop=True)
```
Result (actual run):
```text
dept_name  assigned  completed  completion_pct
       HR         2          1            50.0
    Legal         0          0             NaN
    Sales         3          1            33.3
     Tech         3          3           100.0
```
**Edge cases:** Departments with zero assignments give NULL (undefined), which is honest; show 0 only if the business agrees. Duplicate assignment rows for the same employee and course would inflate counts, so dedupe first if the table allows repeats. 'Completed' could also mean a completed_date after a due date, so confirm the definition.
**Likely follow-ups:**
- Completion rate per employee instead? Group by emp_id.
- Only count courses due before today? Add a due_date filter inside the join condition, not in WHERE, to keep LEFT JOIN behaviour.
**Common mistakes:** Using `COUNT(*)` after a LEFT JOIN (counts the empty row as 1), filtering in WHERE after a LEFT JOIN and thereby dropping departments, and dividing by zero.

### Q63 ⭐ 🟡 HR: Compare average salary of men and women within each job grade to spot a pay gap.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Grouping by two columns or pivoting with conditional aggregation, and framing a pay-gap metric properly.
**Say this in the interview:** I group by grade and use AVG with CASE for each gender so men and women sit side by side, then compute the gap as a percentage of the men's average. Comparing within the same grade keeps the comparison like for like.
**Explain simply:**
- Comparing overall averages is misleading because men may sit in higher grades. Comparing **within a grade** removes that effect.
- `AVG(CASE WHEN gender='M' THEN salary END)` averages only men (other rows give NULL and AVG ignores NULL). This turns rows into columns, called a **pivot**.
- **Gender pay gap %** = (avg men - avg women) / avg men x 100.
**Example:** In G3 men average 107,000 and women 98,000: a gap of about 8.4%. Any grade with only one gender gives NULL.
**Sample data:**

`employees`

| emp_id | gender | grade | salary |
|---|---|---|---|
| 1 | M | G1 | 40000 |
| 2 | F | G1 | 38000 |
| 3 | M | G1 | 42000 |
| 4 | F | G1 | 39000 |
| 5 | M | G2 | 65000 |
| 6 | F | G2 | 58000 |
| 7 | F | G2 | 60000 |
| 8 | M | G3 | 110000 |
| 9 | F | G3 | 98000 |
| 10 | M | G3 | 104000 |

**SQL:**
```sql
SELECT grade,
       COUNT(CASE WHEN gender = 'M' THEN 1 END) AS men,
       COUNT(CASE WHEN gender = 'F' THEN 1 END) AS women,
       ROUND(AVG(CASE WHEN gender = 'M' THEN salary END), 0) AS avg_men,
       ROUND(AVG(CASE WHEN gender = 'F' THEN salary END), 0) AS avg_women,
       ROUND(100.0 * (AVG(CASE WHEN gender = 'M' THEN salary END)
                    - AVG(CASE WHEN gender = 'F' THEN salary END))
             / AVG(CASE WHEN gender = 'M' THEN salary END), 1) AS gap_pct
FROM employees
GROUP BY grade
ORDER BY grade;
```

**Output:**

| grade | men | women | avg_men | avg_women | gap_pct |
|---|---|---|---|---|---|
| G1 | 2 | 2 | 41000.0 | 38500.0 | 6.1 |
| G2 | 1 | 2 | 65000.0 | 59000.0 | 9.2 |
| G3 | 2 | 1 | 107000.0 | 98000.0 | 8.4 |

**pandas equivalent:**
```python
g = employees.groupby(["grade","gender"])["salary"].agg(["count","mean"]).unstack("gender")
r = pd.DataFrame({"grade": g.index,
                  "men": g[("count","M")].values, "women": g[("count","F")].values,
                  "avg_men": g[("mean","M")].values.round(0), "avg_women": g[("mean","F")].values.round(0)})
r["gap_pct"] = (100.0 * (g[("mean","M")].values - g[("mean","F")].values) / g[("mean","M")].values).round(1)
result = r.reset_index(drop=True)
```
Result (actual run):
```text
grade  men  women  avg_men  avg_women  gap_pct
   G1    2      2  41000.0    38500.0      6.1
   G2    1      2  65000.0    59000.0      9.2
   G3    2      1 107000.0    98000.0      8.4
```
**Edge cases:** Grades with only one gender return NULL for the other column and the gap. Small groups (1-2 people) make averages unreliable; always show headcounts. Rounding inside the gap formula would distort it, so round only at the end. This is an unadjusted gap; a real audit would also control for tenure, role and location. Salaries stored as text must be cast to numbers.
**Likely follow-ups:**
- Show it as a long table instead? `GROUP BY grade, gender` gives one row per combination.
- Use the median instead of the average? Averages are pulled up by a few high earners; the median is more robust (see Q73).
**Common mistakes:** Comparing overall averages across grades, forgetting COUNT, and ignoring that AVG skips NULL salaries.

### Q64 ⭐ 🟡 Retail: List products priced above the average price of their category.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Window functions versus correlated subqueries for comparing each row to its group average.
**Say this in the interview:** I use AVG as a window function partitioned by category, so each product carries its category's average next to it, and then filter to the ones above it. The correlated-subquery version gives the same answer.
**Explain simply:**
- A **window function** computes a group-level number (here the category average) without collapsing rows.
- `PARTITION BY category` means 'restart the average for every category'.
- You cannot filter a window result in the same SELECT's WHERE, so wrap it in a CTE or subquery first (a **CTE** is a named temporary result using WITH).
**Example:** Electronics average = (30000+20000+4000)/3 = 18,000, so Phone X (30,000) and Phone Y (20,000) are above; Earbuds are not.
**Sample data:**

`products`

| product_id | name | category | price |
|---|---|---|---|
| 1 | Phone X | Electronics | 30000 |
| 2 | Phone Y | Electronics | 20000 |
| 3 | Earbuds | Electronics | 4000 |
| 4 | Novel | Books | 400 |
| 5 | Textbook | Books | 1200 |
| 6 | Comic | Books | 200 |
| 7 | Pen | Stationery | 50 |
| 8 | Diary | Stationery | 50 |

**SQL:**
```sql
WITH p AS (
  SELECT product_id, name, category, price,
         AVG(price) OVER (PARTITION BY category) AS category_avg
  FROM products
)
SELECT name, category, price, ROUND(category_avg, 1) AS category_avg
FROM p
WHERE price > category_avg
ORDER BY category, price DESC;
```
Same result with a correlated subquery (ran and matched here):
```sql
SELECT p.name, p.category, p.price, ROUND((SELECT AVG(price) FROM products WHERE category = p.category),1) AS category_avg
FROM products p
WHERE p.price > (SELECT AVG(price) FROM products WHERE category = p.category)
ORDER BY p.category, p.price DESC;
```

**Output:**

| name | category | price | category_avg |
|---|---|---|---|
| Textbook | Books | 1200 | 600.0 |
| Phone X | Electronics | 30000 | 18000.0 |
| Phone Y | Electronics | 20000 | 18000.0 |

**pandas equivalent:**
```python
p = products.copy()
p["category_avg"] = p.groupby("category")["price"].transform("mean")
result = (p[p["price"] > p["category_avg"]]
          .assign(category_avg=lambda d: d["category_avg"].round(1))
          [["name","category","price","category_avg"]]
          .sort_values(["category","price"], ascending=[True,False]).reset_index(drop=True))
```
Result (actual run):
```text
    name    category  price  category_avg
Textbook       Books   1200         600.0
 Phone X Electronics  30000       18000.0
 Phone Y Electronics  20000       18000.0
```
**Edge cases:** Products priced exactly at the average are excluded (strict `>`). Stationery (Pen 50, Diary 50) returns nothing, because nothing is above its own average. NULL prices are ignored by AVG and never compare as greater. Averaging is per product row, not weighted by sales.
**Likely follow-ups:**
- Products below average? Use `<`.
- Why not WHERE price > AVG(price)? Aggregates are not allowed in WHERE; you need a subquery or window.
**Common mistakes:** Putting the window function directly in WHERE, using a global average instead of per-category, and forgetting the CTE.

### Q65 ⭐ 🟡 Banking: Bucket overdue loan instalments into 1-30, 31-60, 61-90 and 90+ days past due, and count loans in each bucket per branch.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Date arithmetic, CASE bucketing, and the judgement call of counting loans (not instalments) by their worst delinquency.
**Say this in the interview:** I take unpaid instalments due before the reporting date, find each loan's oldest overdue instalment, bucket that days-past-due number with CASE, and count loans per branch per bucket. A loan is counted once, in its worst bucket.
**Explain simply:**
- **Days past due (DPD)** = reporting date minus due date for an instalment that is still unpaid.
- The question says 'count loans', but one loan can have several overdue instalments. Banks bucket the loan by its **oldest** overdue one, so I use MAX(DPD) per loan first.
- **CASE** turns a number into a label; ranges are tested top to bottom.
**Example:** Loan L1 has instalments 51 and 20 days late, so it counts once, in the 31-60 bucket. L7 is due exactly on the reporting date (0 days) so it is not overdue.
**Sample data:**

`instalments`

| loan_id | branch | due_date | paid_date |
|---|---|---|---|
| L1 | Pune | 2025-05-10 | NULL |
| L1 | Pune | 2025-06-10 | NULL |
| L2 | Pune | 2025-06-20 | NULL |
| L3 | Mumbai | 2025-03-15 | NULL |
| L4 | Mumbai | 2025-05-01 | NULL |
| L5 | Mumbai | 2025-04-01 | NULL |
| L6 | Pune | 2025-05-05 | 2025-05-04 |
| L7 | Delhi | 2025-06-30 | NULL |

**SQL:**
```sql
-- SQLite; reporting date fixed at 2025-06-30 (use date('now') in real life)
WITH overdue AS (
  SELECT loan_id, branch,
         MAX(CAST(julianday('2025-06-30') - julianday(due_date) AS INTEGER)) AS dpd
  FROM instalments
  WHERE paid_date IS NULL AND due_date < '2025-06-30'
  GROUP BY loan_id, branch
), bucketed AS (
  SELECT branch, loan_id,
         CASE WHEN dpd <= 30 THEN '1-30'
              WHEN dpd <= 60 THEN '31-60'
              WHEN dpd <= 90 THEN '61-90'
              ELSE '90+' END AS bucket
  FROM overdue
)
SELECT branch,
       COUNT(CASE WHEN bucket = '1-30'  THEN 1 END) AS d1_30,
       COUNT(CASE WHEN bucket = '31-60' THEN 1 END) AS d31_60,
       COUNT(CASE WHEN bucket = '61-90' THEN 1 END) AS d61_90,
       COUNT(CASE WHEN bucket = '90+'   THEN 1 END) AS d90_plus
FROM bucketed
GROUP BY branch
ORDER BY branch;
```
Date difference in other dialects (not run here / from memory): SQL Server `DATEDIFF(day, due_date, '2025-06-30')`; MySQL `DATEDIFF('2025-06-30', due_date)`; PostgreSQL `DATE '2025-06-30' - due_date`.

**Output:**

| branch | d1_30 | d31_60 | d61_90 | d90_plus |
|---|---|---|---|---|
| Mumbai | 0 | 1 | 1 | 1 |
| Pune | 1 | 1 | 0 | 0 |

**pandas equivalent:**
```python
i = instalments[instalments["paid_date"].isna() & (instalments["due_date"] < "2025-06-30")].copy()
i["dpd"] = (pd.Timestamp("2025-06-30") - pd.to_datetime(i["due_date"])).dt.days
l = i.groupby(["branch","loan_id"], as_index=False)["dpd"].max()
l["bucket"] = pd.cut(l["dpd"], [0,30,60,90,10**6], labels=["d1_30","d31_60","d61_90","d90_plus"])
r = l.pivot_table(index="branch", columns="bucket", values="loan_id", aggfunc="count", fill_value=0, observed=False)
result = r.reset_index()[["branch","d1_30","d31_60","d61_90","d90_plus"]]
result.columns.name = None
```
Result (actual run):
```text
branch  d1_30  d31_60  d61_90  d90_plus
Mumbai      0       1       1         1
  Pune      1       1       0         0
```
**Edge cases:** Boundaries: 30, 60 and 90 days belong to the lower bucket (1-30, 31-60, 61-90). Branches with no overdue loans (Delhi here) vanish unless you LEFT JOIN from a branches table. Partially paid instalments need a balance column rather than paid_date. Never hardcode the date; use the reporting date as a parameter so the report is reproducible.
**Likely follow-ups:**
- Share of the portfolio in 90+ (NPA-style)? Divide d90_plus by total loans of the branch.
- Count instalments instead of loans? Skip the MAX step and bucket each row.
**Common mistakes:** Counting the same loan in several buckets, using inclusive/exclusive boundaries inconsistently, and including instalments that are not yet due.

### Q66 ⭐ 🟡 Sales: Calculate revenue lost to discounts (list price minus sold price times quantity) per category.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Joining and aggregating a computed expression, and knowing the difference between line-level and row-level maths.
**Say this in the interview:** For each line I compute list price minus sold price, multiply by quantity, then sum per category. It must be done per line, because discounts differ line to line.
**Explain simply:**
- Revenue lost to discounts = what we would have earned at list price minus what we actually earned.
- Compute `(list_price - sold_price) * qty` on every line, then `SUM` per category. Averaging first gives wrong numbers because quantities differ.
- I also show the loss as a percentage of the list value, which helps compare categories.
**Example:** Electronics: product 1 sold at 27,000 for 2 units against list 30,000 loses 6,000; product 2 sold at 3,200 for 5 units loses 4,000. Total 10,000.
**Sample data:**

`products`

| product_id | category | list_price |
|---|---|---|
| 1 | Electronics | 30000 |
| 2 | Electronics | 4000 |
| 3 | Books | 500 |
| 4 | Books | 300 |

`order_items`

| order_id | product_id | qty | sold_price |
|---|---|---|---|
| 1 | 1 | 2 | 27000 |
| 2 | 1 | 1 | 30000 |
| 3 | 2 | 5 | 3200 |
| 4 | 3 | 10 | 450 |
| 5 | 3 | 4 | 500 |
| 6 | 4 | 6 | 300 |

**SQL:**
```sql
SELECT p.category,
       SUM(p.list_price * i.qty)                         AS list_value,
       SUM(i.sold_price * i.qty)                         AS sold_value,
       SUM((p.list_price - i.sold_price) * i.qty)        AS discount_lost,
       ROUND(100.0 * SUM((p.list_price - i.sold_price) * i.qty) / SUM(p.list_price * i.qty), 1) AS lost_pct
FROM order_items i
JOIN products p ON p.product_id = i.product_id
GROUP BY p.category
ORDER BY discount_lost DESC;
```

**Output:**

| category | list_value | sold_value | discount_lost | lost_pct |
|---|---|---|---|---|
| Electronics | 110000 | 100000 | 10000 | 9.1 |
| Books | 8800 | 8300 | 500 | 5.7 |

**pandas equivalent:**
```python
m = order_items.merge(products, on="product_id")
m["list_value"] = m["list_price"] * m["qty"]
m["sold_value"] = m["sold_price"] * m["qty"]
r = m.groupby("category", as_index=False)[["list_value","sold_value"]].sum()
r["discount_lost"] = r["list_value"] - r["sold_value"]
r["lost_pct"] = (100.0 * r["discount_lost"] / r["list_value"]).round(1)
result = r.sort_values("discount_lost", ascending=False).reset_index(drop=True)
```
Result (actual run):
```text
   category  list_value  sold_value  discount_lost  lost_pct
Electronics      110000      100000          10000       9.1
      Books        8800        8300            500       5.7
```
**Edge cases:** Lines sold above list price give negative loss and net against discounts; filter `WHERE sold_price < list_price` if you want gross discounts only. List price may change over time, so the historical price at order date is better than today's `products.list_price`. NULL sold_price rows drop out of the sum.
**Likely follow-ups:**
- Which products lose the most? Group by product_id instead.
- Discount rate per order? Group by order_id.
**Common mistakes:** Not multiplying by quantity, subtracting in the wrong direction, and using current list price for old orders.

### Q67 ⭐ 🟡 Banking: Find accounts where ATM withdrawals on a single day exceeded the ₹40,000 daily limit.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Grouping by account and calendar day (not just account), and filtering rows before vs groups after.
**Say this in the interview:** I filter to ATM withdrawals, group by account and the date part of the timestamp, sum the amount, and use HAVING to keep days where the total is over 40,000.
**Explain simply:**
- The limit is **per day**, so the group key is account plus the date. Grouping by account alone adds up different days.
- `date(txn_ts)` strips the time (SQLite/MySQL `DATE()`, PostgreSQL `txn_ts::date`, SQL Server `CAST(txn_ts AS date)`).
- **WHERE** filters rows before grouping (only ATM withdrawals); **HAVING** filters the totals after grouping.
**Example:** Account 201 took out 20,000 + 15,000 + 8,000 = 43,000 on 1 June: over the limit by 3,000.
**Sample data:**

`atm_txns`

| txn_id | account_id | txn_ts | channel | txn_type | amount |
|---|---|---|---|---|---|
| 1 | 201 | 2025-06-01 09:00:00 | ATM | withdrawal | 20000 |
| 2 | 201 | 2025-06-01 13:30:00 | ATM | withdrawal | 15000 |
| 3 | 201 | 2025-06-01 21:10:00 | ATM | withdrawal | 8000 |
| 4 | 202 | 2025-06-01 10:00:00 | ATM | withdrawal | 40000 |
| 5 | 203 | 2025-06-01 18:00:00 | ATM | withdrawal | 25000 |
| 6 | 203 | 2025-06-02 09:00:00 | ATM | withdrawal | 25000 |
| 7 | 204 | 2025-06-01 11:00:00 | ATM | withdrawal | 30000 |
| 8 | 204 | 2025-06-01 15:00:00 | BRANCH | withdrawal | 20000 |

**SQL:**
```sql
SELECT account_id,
       date(txn_ts)  AS txn_date,
       COUNT(*)      AS withdrawals,
       SUM(amount)   AS atm_total
FROM atm_txns
WHERE channel = 'ATM' AND txn_type = 'withdrawal'
GROUP BY account_id, date(txn_ts)
HAVING SUM(amount) > 40000
ORDER BY account_id, txn_date;
```

**Output:**

| account_id | txn_date | withdrawals | atm_total |
|---|---|---|---|
| 201 | 2025-06-01 | 3 | 43000 |

**pandas equivalent:**
```python
a = atm_txns[(atm_txns["channel"] == "ATM") & (atm_txns["txn_type"] == "withdrawal")].copy()
a["txn_date"] = a["txn_ts"].str[:10]
r = a.groupby(["account_id","txn_date"], as_index=False).agg(withdrawals=("txn_id","count"), atm_total=("amount","sum"))
result = r[r["atm_total"] > 40000].sort_values(["account_id","txn_date"]).reset_index(drop=True)
```
Result (actual run):
```text
 account_id   txn_date  withdrawals  atm_total
        201 2025-06-01            3      43000
```
**Edge cases:** Account 202 withdrew exactly 40,000, which is not 'exceeded' (strict `>`). Account 203 took 25,000 on two different days, so not flagged. Account 204's branch withdrawal is excluded because the limit applies to ATMs only. Time zones: if timestamps are stored in UTC, the 'day' boundary may differ from the customer's day. Reversed or failed transactions should be excluded if the table has a status column.
**Likely follow-ups:**
- Show the excess amount? Add `SUM(amount) - 40000 AS excess`.
- Rolling 24 hours instead of calendar day? Use a window or self-join over timestamps (see Q69).
**Common mistakes:** Grouping by account only, using `>=` when the rule says 'exceeded', and filtering the total in WHERE instead of HAVING.

### Q68 ⭐ 🟡 E-commerce: For each customer, find the category of their very first order.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Picking the first row per group with ROW_NUMBER, and spotting that an order can hold several categories and that two orders can share a date.
**Say this in the interview:** I rank each customer's orders by date with ROW_NUMBER, keep rank 1, then join to items and products to get the category. If the first order has more than one category I list them all, and I break date ties with the lower order id.
**Explain simply:**
- `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, order_id)` numbers each customer's orders 1, 2, 3 from the earliest.
- The **tie-breaker** `order_id` matters: Meena placed two orders on the same day, and without it the 'first' order would be random.
- The question assumes one category per order. An order can contain several items, so I combine categories with `GROUP_CONCAT` (PostgreSQL `STRING_AGG`).
**Example:** Ravi's first order (id 3) contained Electronics and Stationery, so his first-order category is both. Meena's first order is id 4 (Stationery), not id 5.
**Sample data:**

`orders`

| order_id | customer_id | order_date |
|---|---|---|
| 1 | 1 | 2025-01-05 |
| 2 | 1 | 2025-02-10 |
| 3 | 2 | 2025-01-20 |
| 4 | 3 | 2025-03-01 |
| 5 | 3 | 2025-03-01 |
| 6 | 4 | 2025-04-15 |

`order_items`

| order_id | product_id |
|---|---|
| 1 | 10 |
| 2 | 11 |
| 3 | 10 |
| 3 | 12 |
| 4 | 12 |
| 5 | 11 |
| 6 | 11 |

`products`

| product_id | category |
|---|---|
| 10 | Electronics |
| 11 | Books |
| 12 | Stationery |

**SQL:**
```sql
WITH first_order AS (
  SELECT order_id, customer_id, order_date,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS rn
  FROM orders
)
SELECT f.customer_id, f.order_id AS first_order_id, f.order_date,
       GROUP_CONCAT(DISTINCT p.category) AS first_order_category
FROM first_order f
JOIN order_items i ON i.order_id = f.order_id
JOIN products p    ON p.product_id = i.product_id
WHERE f.rn = 1
GROUP BY f.customer_id, f.order_id, f.order_date
ORDER BY f.customer_id;
```

**Output:**

| customer_id | first_order_id | order_date | first_order_category |
|---|---|---|---|
| 1 | 1 | 2025-01-05 | Electronics |
| 2 | 3 | 2025-01-20 | Electronics,Stationery |
| 3 | 4 | 2025-03-01 | Stationery |
| 4 | 6 | 2025-04-15 | Books |

**pandas equivalent:**
```python
o = orders.sort_values(["customer_id","order_date","order_id"]).groupby("customer_id", as_index=False).first()
m = o.merge(order_items, on="order_id").merge(products, on="product_id")
r = m.groupby(["customer_id","order_id","order_date"], as_index=False)["category"] \
     .agg(lambda s: ",".join(sorted(set(s))))
result = r.rename(columns={"order_id":"first_order_id","category":"first_order_category"}).sort_values("customer_id").reset_index(drop=True)
```
Result (actual run):
```text
 customer_id  first_order_id order_date   first_order_category
           1               1 2025-01-05            Electronics
           2               3 2025-01-20 Electronics,Stationery
           3               4 2025-03-01             Stationery
           4               6 2025-04-15                  Books
```
**Edge cases:** Same-day orders need a tie-breaker (order_id or a timestamp). Orders with no items vanish from the inner join; use LEFT JOIN if you need them. Order of categories inside GROUP_CONCAT is not guaranteed in SQLite. Customers with no orders are not in `orders`, so they do not appear.
**Likely follow-ups:**
- Same for the most recent order? Sort `order_date DESC, order_id DESC`.
- Why not MIN(order_date) with a join? Ties and multi-category orders make that version return extra rows.
**Common mistakes:** Using MIN(order_date) per customer and joining back (duplicates on ties), no tie-breaker in ORDER BY, and ignoring multi-category orders.

### Q69 ⭐ 🔴 Banking (fraud check): Find accounts with 3 or more transactions of the same amount within a 10-minute window.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Time-window logic with window functions: can you count rows within a time range around each row?
**Say this in the interview:** For each transaction I count how many transactions of the same account and amount happen in the next 10 minutes, including itself, using a RANGE window over the time in seconds. Any count of 3 or more is a suspect, and I keep the maximum per account and amount.
**Explain simply:**
- A **window function** looks at neighbouring rows without collapsing them. `PARTITION BY account_id, amount` restricts it to identical repeats.
- `RANGE BETWEEN CURRENT ROW AND 600 FOLLOWING` means 'rows whose time is at most 600 seconds (10 minutes) after this one'. It needs the time as a number, so I convert with `strftime('%s', ...)` (seconds since 1970).
- Each transaction acts as the start of a window; if any window holds 3 or more, the account is flagged.
**Example:** Account 101 sends 9,999 at 10:00, 10:03 and 10:07: three in 7 minutes, flagged. Account 102 sends 5,000 at 11:00, 11:06, 11:12: only two fit in any 10-minute span (12 minutes in total), not flagged.
**Sample data:**

`transactions`

| txn_id | account_id | txn_ts | amount |
|---|---|---|---|
| 1 | 101 | 2025-06-10 10:00:00 | 9999 |
| 2 | 101 | 2025-06-10 10:03:00 | 9999 |
| 3 | 101 | 2025-06-10 10:07:00 | 9999 |
| 4 | 101 | 2025-06-10 10:20:00 | 9999 |
| 5 | 102 | 2025-06-10 11:00:00 | 5000 |
| 6 | 102 | 2025-06-10 11:06:00 | 5000 |
| 7 | 102 | 2025-06-10 11:12:00 | 5000 |
| 8 | 103 | 2025-06-10 12:00:00 | 2000 |
| 9 | 103 | 2025-06-10 12:01:00 | 2000 |
| 10 | 103 | 2025-06-10 12:02:00 | 2000 |
| 11 | 103 | 2025-06-10 12:05:00 | 750 |

**SQL:**
```sql
-- SQLite: time converted to epoch seconds because RANGE needs a numeric ordering key
WITH w AS (
  SELECT account_id, amount, txn_ts,
         COUNT(*) OVER (PARTITION BY account_id, amount
                        ORDER BY CAST(strftime('%s', txn_ts) AS INTEGER)
                        RANGE BETWEEN CURRENT ROW AND 600 FOLLOWING) AS txns_in_10min
  FROM transactions
)
SELECT account_id, amount, MAX(txns_in_10min) AS max_txns_in_10min
FROM w
GROUP BY account_id, amount
HAVING MAX(txns_in_10min) >= 3
ORDER BY account_id;
```
PostgreSQL alternative (not run here / from memory): `COUNT(*) OVER (PARTITION BY account_id, amount ORDER BY txn_ts RANGE BETWEEN CURRENT ROW AND INTERVAL '10 minutes' FOLLOWING)`. MySQL and SQL Server lack interval RANGE frames, so use a self-join: join the table to itself on same account and amount where `b.txn_ts BETWEEN a.txn_ts AND a.txn_ts + 10 minutes`, group by `a.txn_id`, `HAVING COUNT(*) >= 3`.

**Output:**

| account_id | amount | max_txns_in_10min |
|---|---|---|
| 101 | 9999 | 3 |
| 103 | 2000 | 3 |

**pandas equivalent:**
```python
t = transactions.assign(ts=pd.to_datetime(transactions["txn_ts"])).sort_values("ts").set_index("ts")
# backward window [t-10min, t] counts the same clusters as the forward SQL window
c = t.groupby(["account_id","amount"])["txn_id"].rolling("10min", closed="both").count()
r = c.groupby(["account_id","amount"]).max().rename("max_txns_in_10min").reset_index()
result = r[r["max_txns_in_10min"] >= 3].sort_values("account_id").reset_index(drop=True)
```
Result (actual run):
```text
 account_id  amount  max_txns_in_10min
        101    9999                3.0
        103    2000                3.0
```
**Edge cases:** Boundary: exactly 10 minutes apart counts as inside (inclusive); change 600 to 599 if the rule is strictly under 10. Account 103 has a 750 transaction that is correctly ignored because the amount differs. Four repeats (account 101 also has one at 10:20) do not change the flag. This is a screening rule only: legitimate repeat payments (subscriptions, EMIs) will trigger it, so review by a human or add more signals.
**Likely follow-ups:**
- How do you list the actual transactions involved? Self-join on the same account and amount within the window, or join the flagged accounts back to the table.
- Same amount versus similar amounts? Replace the amount partition with a range test, e.g. amount within 1%.
**Common mistakes:** Partitioning by account only (counts different amounts), using ROWS instead of RANGE (counts rows, not time), and comparing text timestamps without converting them.

### Q70 ⭐ 🔴 Sales: Find the smallest set of products that together make up 80% of revenue (Pareto analysis).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Running totals with window functions, and the subtle boundary of 'smallest set that reaches 80%'.
**Say this in the interview:** I total revenue per product, rank products from best to worst, take a running total, and keep every product whose running total before it was still under 80% of the grand total. That includes the product that crosses the line.
**Explain simply:**
- **Pareto (80/20) analysis**: a few products usually create most of the revenue.
- A **running (cumulative) total** is a sum that grows row by row: `SUM(revenue) OVER (ORDER BY revenue DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`.
- 'Smallest set that reaches 80%' means we must include the product that pushes us over 80%. The rule `cum - revenue < 0.8 x total` keeps a product only if the products above it had not reached 80% yet.
**Example:** Revenue per product: P1 4,000, P2 2,500, P3 1,200, P4 900 ... Cumulative: 40%, 65%, 77%, 86%. So four products (P1 to P4) are the smallest set covering 80%.
**Sample data:**

`order_items`

| product_id | qty | unit_price |
|---|---|---|
| P1 | 2 | 1000 |
| P1 | 4 | 500 |
| P2 | 5 | 500 |
| P3 | 3 | 400 |
| P4 | 9 | 100 |
| P5 | 6 | 100 |
| P6 | 4 | 100 |
| P7 | 5 | 50 |
| P8 | 3 | 50 |

**SQL:**
```sql
WITH rev AS (
  SELECT product_id, SUM(qty * unit_price) AS revenue
  FROM order_items
  GROUP BY product_id
), ranked AS (
  SELECT product_id, revenue,
         SUM(revenue) OVER (ORDER BY revenue DESC, product_id
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cum_rev,
         SUM(revenue) OVER () AS total_rev
  FROM rev
)
SELECT product_id, revenue, ROUND(100.0 * cum_rev / total_rev, 1) AS cum_pct
FROM ranked
WHERE cum_rev - revenue < 0.8 * total_rev
ORDER BY revenue DESC, product_id;
```

**Output:**

| product_id | revenue | cum_pct |
|---|---|---|
| P1 | 4000 | 40.0 |
| P2 | 2500 | 65.0 |
| P3 | 1200 | 77.0 |
| P4 | 900 | 86.0 |

**pandas equivalent:**
```python
r = order_items.assign(rev=order_items["qty"] * order_items["unit_price"]).groupby("product_id", as_index=False)["rev"].sum()
r = r.rename(columns={"rev": "revenue"}).sort_values(["revenue","product_id"], ascending=[False,True]).reset_index(drop=True)
r["cum_rev"] = r["revenue"].cumsum()
total = r["revenue"].sum()
r["cum_pct"] = (100.0 * r["cum_rev"] / total).round(1)
result = r[r["cum_rev"] - r["revenue"] < 0.8 * total][["product_id","revenue","cum_pct"]].reset_index(drop=True)
```
Result (actual run):
```text
product_id  revenue  cum_pct
        P1     4000     40.0
        P2     2500     65.0
        P3     1200     77.0
        P4      900     86.0
```
**Edge cases:** Ties in revenue need a tie-breaker (product_id) in the ORDER BY of the window, otherwise the running total is ambiguous. If a running total hits exactly 80%, the next product is not needed, which the `<` rule handles. Returned/negative-revenue lines should be removed or netted first. Always write the frame `ROWS BETWEEN ...`: the default RANGE frame treats tied values as one step.
**Likely follow-ups:**
- How would you express it as 'X% of products make 80% of revenue'? Divide the count of products in the set by the total product count.
- How do you label A/B/C classes? Bucket `cum_pct` with CASE (e.g. <=80 A, <=95 B, else C).
**Common mistakes:** Filtering `cum_pct <= 80` (drops the crossing product, so the set falls short of 80%), no tie-breaker, and leaving the default window frame.

### Q71 ⭐ 🔴 E-commerce: Find the pairs of products most frequently bought together in the same order (basket analysis).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Self-joins to build pairs without duplicates (A,B vs B,A) and without pairing an item with itself.
**Say this in the interview:** I join the order-lines table to itself on the same order, keep only pairs where the first product id is smaller than the second so each pair appears once, then count orders per pair and sort descending.
**Explain simply:**
- A **self-join** joins a table to itself; here, every line is matched with the other lines in the same order.
- `a.product_id < b.product_id` removes pairing an item with itself and keeps (Phone, Case) but drops (Case, Phone).
- I use `SELECT DISTINCT order_id, product_id` first, because the same product can appear on two lines of one order (order 6 has Case twice) and would otherwise double count.
**Example:** Phone and Case appear together in orders 1, 2 and 4: 3 times. Charger and Case appear in 1, 4 and 5: 3 times.
**Sample data:**

`order_items`

| order_id | product_id |
|---|---|
| 1 | 1 |
| 1 | 2 |
| 1 | 3 |
| 2 | 1 |
| 2 | 2 |
| 3 | 4 |
| 3 | 5 |
| 4 | 1 |
| 4 | 2 |
| 4 | 3 |
| 5 | 2 |
| 5 | 3 |
| 6 | 4 |
| 6 | 5 |
| 6 | 2 |
| 6 | 2 |

`products`

| product_id | product_name |
|---|---|
| 1 | Phone |
| 2 | Case |
| 3 | Charger |
| 4 | Laptop |
| 5 | Mouse |

**SQL:**
```sql
WITH li AS (SELECT DISTINCT order_id, product_id FROM order_items)
SELECT p1.product_name AS product_a, p2.product_name AS product_b,
       COUNT(*) AS orders_together
FROM li a
JOIN li b       ON b.order_id = a.order_id AND a.product_id < b.product_id
JOIN products p1 ON p1.product_id = a.product_id
JOIN products p2 ON p2.product_id = b.product_id
GROUP BY p1.product_name, p2.product_name
ORDER BY orders_together DESC, product_a, product_b
LIMIT 5;
```

**Output:**

| product_a | product_b | orders_together |
|---|---|---|
| Case | Charger | 3 |
| Phone | Case | 3 |
| Laptop | Mouse | 2 |
| Phone | Charger | 2 |
| Case | Laptop | 1 |

**pandas equivalent:**
```python
li = order_items.drop_duplicates()
m = li.merge(li, on="order_id", suffixes=("_a","_b"))
m = m[m["product_id_a"] < m["product_id_b"]]
m = m.merge(products.rename(columns={"product_id":"product_id_a","product_name":"product_a"}), on="product_id_a") \
     .merge(products.rename(columns={"product_id":"product_id_b","product_name":"product_b"}), on="product_id_b")
r = m.groupby(["product_a","product_b"], as_index=False).size().rename(columns={"size":"orders_together"})
result = r.sort_values(["orders_together","product_a","product_b"], ascending=[False,True,True]).head(5).reset_index(drop=True)
```
Result (actual run):
```text
product_a product_b  orders_together
     Case   Charger                3
    Phone      Case                3
   Laptop     Mouse                2
    Phone   Charger                2
     Case    Laptop                1
```
**Edge cases:** Ties: several pairs share the same count, so LIMIT 5 may cut a tie arbitrarily. Use `DENSE_RANK()` over the count to keep all tied pairs. Orders with a single item produce no pairs. The join grows fast: n items in an order give n(n-1)/2 pairs, so on big data filter to popular products first. Raw counts favour popular products; 'lift' or 'support' compare against what you'd expect by chance.
**Likely follow-ups:**
- Triples? Add a third join with `b.product_id < c.product_id`.
- How do you get a percentage? Divide by the total number of distinct orders (support).
**Common mistakes:** Using `<>` instead of `<` (every pair twice), not de-duplicating lines, and LIMIT cutting off tied pairs.

### Q72 ⭐ 🔴 HR: From `leaves`, find pairs of employees of the same team who are on leave on overlapping dates.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** The standard interval-overlap test (A starts before B ends AND B starts before A ends) plus self-join discipline.
**Say this in the interview:** I join the leaves table to itself for people in the same team, keep each pair once with emp_id less than, and test overlap with start_a <= end_b AND start_b <= end_a. I also show the overlapping dates.
**Explain simply:**
- Two date ranges overlap unless one finishes before the other begins. Written positively: `a.start <= b.end AND b.start <= a.end`.
- `a.emp_id < b.emp_id` gives each pair once and stops an employee being paired with themselves.
- Overlap dates are the later of the two starts and the earlier of the two ends. SQLite uses `MAX(x, y)`/`MIN(x, y)` for two values; PostgreSQL/MySQL use `GREATEST`/`LEAST` (not run here).
**Example:** Asha (1-5 July) and Ravi (4-10 July) are both away on 4 and 5 July. In team B, Karan (2-3 July) and Divya (3-4 July) clash on 3 July.
**Sample data:**

`employees`

| emp_id | name | team |
|---|---|---|
| 1 | Asha | A |
| 2 | Ravi | A |
| 3 | Meena | A |
| 4 | Karan | B |
| 5 | Divya | B |

`leaves`

| leave_id | emp_id | start_date | end_date |
|---|---|---|---|
| 1 | 1 | 2025-07-01 | 2025-07-05 |
| 2 | 2 | 2025-07-04 | 2025-07-10 |
| 3 | 3 | 2025-07-06 | 2025-07-08 |
| 4 | 4 | 2025-07-02 | 2025-07-03 |
| 5 | 5 | 2025-07-03 | 2025-07-04 |
| 6 | 1 | 2025-07-08 | 2025-07-09 |

**SQL:**
```sql
SELECT e1.name AS emp_a, e2.name AS emp_b, e1.team,
       MAX(l1.start_date, l2.start_date) AS overlap_from,
       MIN(l1.end_date,   l2.end_date)   AS overlap_to
FROM leaves l1
JOIN leaves l2    ON l1.emp_id < l2.emp_id
                 AND l1.start_date <= l2.end_date
                 AND l2.start_date <= l1.end_date
JOIN employees e1 ON e1.emp_id = l1.emp_id
JOIN employees e2 ON e2.emp_id = l2.emp_id AND e2.team = e1.team
ORDER BY e1.team, emp_a, emp_b, overlap_from;
```

**Output:**

| emp_a | emp_b | team | overlap_from | overlap_to |
|---|---|---|---|---|
| Asha | Meena | A | 2025-07-08 | 2025-07-08 |
| Asha | Ravi | A | 2025-07-04 | 2025-07-05 |
| Asha | Ravi | A | 2025-07-08 | 2025-07-09 |
| Ravi | Meena | A | 2025-07-06 | 2025-07-08 |
| Karan | Divya | B | 2025-07-03 | 2025-07-03 |

**pandas equivalent:**
```python
m = leaves.merge(leaves, how="cross", suffixes=("_1","_2"))
m = m[(m["emp_id_1"] < m["emp_id_2"]) & (m["start_date_1"] <= m["end_date_2"]) & (m["start_date_2"] <= m["end_date_1"])]
m = m.merge(employees.add_suffix("_1"), on="emp_id_1").merge(employees.add_suffix("_2"), on="emp_id_2")
m = m[m["team_1"] == m["team_2"]]
m["overlap_from"] = m[["start_date_1","start_date_2"]].max(axis=1)
m["overlap_to"] = m[["end_date_1","end_date_2"]].min(axis=1)
result = (m.rename(columns={"name_1":"emp_a","name_2":"emp_b","team_1":"team"})
           [["emp_a","emp_b","team","overlap_from","overlap_to"]]
           .sort_values(["team","emp_a","emp_b","overlap_from"]).reset_index(drop=True))
```
Result (actual run):
```text
emp_a emp_b team overlap_from overlap_to
 Asha Meena    A   2025-07-08 2025-07-08
 Asha  Ravi    A   2025-07-04 2025-07-05
 Asha  Ravi    A   2025-07-08 2025-07-09
 Ravi Meena    A   2025-07-06 2025-07-08
Karan Divya    B   2025-07-03 2025-07-03
```
**Edge cases:** Touching ranges (one ends 5 July, other starts 5 July) count as overlap with `<=`; use `<` if the end date is exclusive. A pair with two separate overlapping leave periods appears twice (Asha and Ravi here); wrap with `SELECT DISTINCT emp_a, emp_b` if only the pair is wanted. Open-ended leaves (NULL end_date) need `COALESCE(end_date, '9999-12-31')`. Do not skip the same-team join condition or you compare strangers.
**Likely follow-ups:**
- How many people are away on a given day per team? Join to a calendar table or use a date generator.
- Why not compare every row with every row in pandas? A cross join is fine for small data but grows with n squared; merge on team first for scale.
**Common mistakes:** Testing 'start between start and end' only (misses the case where one range completely contains the other), no `<` on emp_id (duplicate mirrored pairs), and forgetting the team condition.

### Q73 ⭐ 🔴 HR: Find the employee(s) whose salary equals the median salary of their department.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Computing a median in SQL (no built-in in most engines) and handling even-sized groups, where the median may match nobody.
**Say this in the interview:** I number the salaries within each department and take the middle one, or the average of the two middle ones when the headcount is even. Then I join back and keep employees whose salary equals that median. In PostgreSQL I would use PERCENTILE_CONT(0.5) instead.
**Explain simply:**
- The **median** is the middle value once sorted; it ignores extreme values, so it describes 'typical pay' better than the average.
- With an odd count there is one middle row; with an even count the median is the average of the two middle rows, so it can fall between salaries.
- `ROW_NUMBER` numbers the sorted rows and `COUNT(*) OVER` gives the group size n; the middle rows are numbers (n+1)/2 and (n+2)/2 using whole-number division.
- If the median is a value nobody earns, the answer for that department is no employees. That is correct, not a bug.
**Example:** HR has 5 salaries (40k, 45k, 50k, 52k, 70k): median 50k, so Meena. Tech has 55k, 60k, 60k, 90k: median 60k, so Arjun and Sara. Sales has 40k, 50k, 60k, 80k: median 55k, nobody earns that.
**Sample data:**

`employees`

| emp_id | name | dept | salary |
|---|---|---|---|
| 1 | Asha | HR | 40000 |
| 2 | Ravi | HR | 45000 |
| 3 | Meena | HR | 50000 |
| 4 | Karan | HR | 52000 |
| 5 | Divya | HR | 70000 |
| 6 | Neha | Tech | 55000 |
| 7 | Arjun | Tech | 60000 |
| 8 | Sara | Tech | 60000 |
| 9 | Vik | Tech | 90000 |
| 10 | Tina | Sales | 40000 |
| 11 | Omar | Sales | 50000 |
| 12 | Lata | Sales | 60000 |
| 13 | Ben | Sales | 80000 |

**SQL:**
```sql
-- SQLite (integer division in (n+1)/2). MySQL: use DIV instead of /
WITH ranked AS (
  SELECT dept, salary,
         ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary) AS rn,
         COUNT(*)     OVER (PARTITION BY dept)                 AS n
  FROM employees
), med AS (
  SELECT dept, AVG(salary) AS median_salary
  FROM ranked
  WHERE rn IN ((n + 1) / 2, (n + 2) / 2)
  GROUP BY dept
)
SELECT e.dept, e.name, e.salary, m.median_salary
FROM employees e
JOIN med m ON m.dept = e.dept AND e.salary = m.median_salary
ORDER BY e.dept, e.name;
```
Shorter in engines with a median function (ran in DuckDB here and matched; PostgreSQL's `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary)` and Oracle `MEDIAN` are not run here):
```sql
SELECT e.dept, e.name, e.salary, m.med AS median_salary
FROM employees e
JOIN (SELECT dept, MEDIAN(salary) AS med FROM employees GROUP BY dept) m
  ON m.dept = e.dept AND e.salary = m.med;
```

**Output:**

| dept | name | salary | median_salary |
|---|---|---|---|
| HR | Meena | 50000 | 50000.0 |
| Tech | Arjun | 60000 | 60000.0 |
| Tech | Sara | 60000 | 60000.0 |

**pandas equivalent:**
```python
e = employees.copy()
e["median_salary"] = e.groupby("dept")["salary"].transform("median")
result = (e[e["salary"] == e["median_salary"]][["dept","name","salary","median_salary"]]
          .sort_values(["dept","name"]).reset_index(drop=True))
```
Result (actual run):
```text
dept  name  salary  median_salary
  HR Meena   50000        50000.0
Tech Arjun   60000        60000.0
Tech  Sara   60000        60000.0
```
**Edge cases:** Even-sized groups: median is an average, so it may match nobody (Sales). Ties: everyone with the median salary is returned (Arjun and Sara). NULL salaries are ignored by AVG, but ROW_NUMBER/COUNT would still count them as rows and shift the middle, so filter `WHERE salary IS NOT NULL` first. Average salary is a different thing from median; do not mix them up.
**Likely follow-ups:**
- If the question wants the closest to the median? Order by `ABS(salary - median)` and take the first per department.
- Median of the whole company? Drop the PARTITION BY.
**Common mistakes:** Using AVG and calling it median, using `n/2` which gives the wrong row for odd n, and expecting every department to return someone.

### Q74 ⭐ 🔴 E-commerce: Split customers into 10 equal spend groups (deciles) and show the share of total revenue from the top decile.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** NTILE for bucketing, aggregating customers first, and reading a concentration result (top decile share).
**Say this in the interview:** I total spend per customer, split customers into 10 equal-sized groups with NTILE(10) ordered by spend descending, then sum revenue per group and divide by the grand total. Decile 1 is the top 10 percent of customers.
**Explain simply:**
- A **decile** is one of 10 equal-sized slices; `NTILE(10)` hands out bucket numbers 1 to 10 so each has about the same number of customers.
- I must aggregate to customer level first. NTILE on order rows would split orders, not customers.
- When customers do not divide evenly (12 customers into 10 buckets), the first buckets get one extra customer each. Ties at a bucket border are split arbitrarily, so add a tie-breaker.
**Example:** Here 12 customers total 32,000 of revenue. The top decile (the two biggest customers, 9,000 + 6,000) brings 15,000 of 32,000, about 47% of revenue.
**Sample data:**

`orders`

| order_id | customer_id | amount |
|---|---|---|
| 1 | C01 | 9000 |
| 2 | C02 | 3500 |
| 3 | C02 | 2500 |
| 4 | C03 | 4000 |
| 5 | C04 | 3000 |
| 6 | C05 | 1500 |
| 7 | C05 | 1000 |
| 8 | C06 | 2000 |

(first 8 of 14 rows shown)

**SQL:**
```sql
WITH spend AS (
  SELECT customer_id, SUM(amount) AS total_spend
  FROM orders
  GROUP BY customer_id
), tiles AS (
  SELECT customer_id, total_spend,
         NTILE(10) OVER (ORDER BY total_spend DESC, customer_id) AS decile
  FROM spend
)
SELECT decile,
       COUNT(*)          AS customers,
       SUM(total_spend)  AS revenue,
       ROUND(100.0 * SUM(total_spend) / SUM(SUM(total_spend)) OVER (), 1) AS share_pct
FROM tiles
GROUP BY decile
ORDER BY decile;
```

**Output:**

| decile | customers | revenue | share_pct |
|---|---|---|---|
| 1 | 2 | 15000 | 46.9 |
| 2 | 2 | 7000 | 21.9 |
| 3 | 1 | 2500 | 7.8 |
| 4 | 1 | 2000 | 6.3 |
| 5 | 1 | 1500 | 4.7 |
| 6 | 1 | 1200 | 3.8 |
| 7 | 1 | 1000 | 3.1 |
| 8 | 1 | 800 | 2.5 |
| 9 | 1 | 600 | 1.9 |
| 10 | 1 | 400 | 1.3 |

**pandas equivalent:**
```python
import numpy as np
s = orders.groupby("customer_id", as_index=False)["amount"].sum().rename(columns={"amount": "total_spend"})
s = s.sort_values(["total_spend","customer_id"], ascending=[False,True]).reset_index(drop=True)
base, extra = divmod(len(s), 10)                       # NTILE rule: first `extra` buckets get one more row
s["decile"] = np.repeat(np.arange(1, 11), [base + 1 if i < extra else base for i in range(10)])
r = s.groupby("decile", as_index=False).agg(customers=("customer_id","count"), revenue=("total_spend","sum"))
r["share_pct"] = np.floor(1000.0 * r["revenue"] / r["revenue"].sum() + 0.5) / 10   # round half up, like SQL ROUND
result = r
```
Result (actual run):
```text
 decile  customers  revenue  share_pct
      1          2    15000       46.9
      2          2     7000       21.9
      3          1     2500        7.8
      4          1     2000        6.3
      5          1     1500        4.7
      6          1     1200        3.8
      7          1     1000        3.1
      8          1      800        2.5
      9          1      600        1.9
     10          1      400        1.3
```
**Edge cases:** With fewer than 10 customers, some deciles are empty. Rounding: SQL ROUND rounds halves up (6.25 becomes 6.3) while pandas `.round()` rounds halves to even, so the pandas code rounds half up by hand. Uneven counts: deciles 1 and 2 hold 2 customers each here. Customers with equal spend straddling a border land in different deciles, so deterministic tie-breaking is important. Zero-order customers are not in `orders`; decide whether they belong in the base. `pd.qcut` splits on value quantiles and can differ from NTILE, so use the rank-based version to match SQL. The top-decile share (decile 1 row) is the headline number; a 20/80 style claim comes from adding decile shares.
**Likely follow-ups:**
- How do you show just the top decile share? Wrap the final query and filter `decile = 1`.
- Why not PERCENT_RANK? It gives a 0-1 position per customer; NTILE gives equal-size buckets, which is easier to report.
**Common mistakes:** Applying NTILE to order rows instead of customers, sorting ascending (decile 1 becomes the lowest spenders), and not stating how ties and uneven bucket sizes were handled.

