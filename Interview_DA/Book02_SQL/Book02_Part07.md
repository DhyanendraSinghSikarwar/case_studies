# Book 2 — SQL · Part 7: CASE WHEN, NULL handling, string & date functions 🟢🟡

**Target:** 50 questions  |  **Actual:** 60

**Scope:** conditional logic (CASE WHEN, IIF), NULL behaviour (IS NULL, COALESCE, NULLIF, NULL in aggregates/joins/NOT IN), string functions and date functions, with MySQL / PostgreSQL / SQL Server differences noted where they matter.

### Q1 ⭐⭐⭐ 🟢 How do you check for NULL values? Why does `WHERE col = NULL` return nothing?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know NULL means 'unknown', so ordinary comparisons with it never come out true.
**Say this in the interview:** NULL is not a value, it is 'unknown', so `= NULL` is never true. I use `IS NULL` or `IS NOT NULL` instead.
**Explain simply:**
- **NULL** means the data is missing or unknown (not zero, not an empty string).
- Any comparison with an unknown gives *unknown* (SQL's third truth value), and `WHERE` keeps only rows that are true. So `salary = NULL` keeps nothing.
- Even `NULL = NULL` is unknown, because two unknowns are not necessarily equal.
- Use `IS NULL` / `IS NOT NULL`. This is the same in every dialect.
**Example:** HR asks 'who has no salary recorded yet?' In our 8-employee table, 2 people (Meera, Karan) have a blank salary. `WHERE salary = NULL` returns 0 rows; `WHERE salary IS NULL` returns those 2.
**Sample data:**

`employees`

| emp_id | first_name | last_name | gender | dept | salary | joining_date |
|---|---|---|---|---|---|---|
| 1 | Asha | Rao | F | HR | 52000 | 2019-03-15 |
| 2 | Ravi | Kumar | M | IT | 78000 | 2021-07-01 |
| 3 | Meera | Nair | F | HR | NULL | 2023-01-10 |
| 4 | Arjun | Singh | M | Sales | 45000 | 2018-11-20 |
| 5 | Neha | Gupta | F | IT | 91000 | 2020-02-05 |
| 6 | Karan | Shah | M | Sales | NULL | 2022-09-12 |
| 7 | Anil | Verma | M | Finance | 30000 | 2024-05-30 |
| 8 | Sana | Khan | F | Finance | 65000 | 2017-08-08 |
**SQL:**
```sql
-- SQLite (run here); standard SQL unless noted
SELECT emp_id, first_name, salary FROM employees WHERE salary = NULL;

SELECT emp_id, first_name, salary FROM employees WHERE salary IS NULL;

SELECT NULL = NULL AS null_eq_null, NULL IS NULL AS null_is_null;

-- Same in MySQL / PostgreSQL / SQL Server. (MySQL also has the NULL-safe operator <=>, see Q43.)
```
**Output:**

Query 1:

| emp_id | first_name | salary |
|---|---|---|

Query 2:

| emp_id | first_name | salary |
|---|---|---|
| 3 | Meera | NULL |
| 6 | Karan | NULL |

Query 3:

| null_eq_null | null_is_null |
|---|---|
| NULL | 1 |
**pandas equivalent:**
```python
# employees = pd.read_sql('SELECT * FROM employees', conn)
res = employees.loc[employees['salary'].isna(), ['emp_id', 'first_name', 'salary']]
```
Result matches the SQL output.
**Edge cases:** `NULL = NULL` is also not true. Empty string `''` is NOT NULL (Oracle is the exception: it treats `''` as NULL). In pandas, missing is `NaN`, so use `.isna()` (`== np.nan` is always False, the same trap).
**Likely follow-ups:**
1. *How do I treat NULL as a value in a comparison?* Use `IS NOT DISTINCT FROM` (PostgreSQL) or `<=>` (MySQL), see Q43.
2. *Does `NOT IN` work with NULLs?* No, if the list contains a NULL it returns nothing. Use `NOT EXISTS`.
**Common mistakes:** Writing `= NULL` or `!= NULL`; assuming NULL means 0; forgetting that `<> 'X'` also drops NULL rows (Q13).

### Q2 ⭐⭐⭐ 🟢 What does COALESCE do? Replace missing salaries with 0 in a report.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can handle missing values in reports without changing the stored data.
**Say this in the interview:** COALESCE returns the first non-NULL value in its list. For missing salaries I write `COALESCE(salary, 0)` so the report shows 0 instead of blank.
**Explain simply:**
- **COALESCE(a, b, c, ...)** checks the arguments left to right and returns the first one that is not NULL (NULL if all are).
- It works only in the query result; the table itself is not changed.
- It is standard SQL: MySQL, PostgreSQL, SQL Server, Oracle and SQLite all support it.
- Caution: 0 is not the same as 'unknown'. For averages, replacing NULL with 0 pulls the average down.
**Example:** Total payroll for HR = 52,000 + (Meera's missing salary shown as 0) = 52,000. A report that prints blanks looks broken to a manager; printing 0 or 'Not set' reads cleanly.
**Sample data:**

`employees`

| emp_id | first_name | last_name | gender | dept | salary | joining_date |
|---|---|---|---|---|---|---|
| 1 | Asha | Rao | F | HR | 52000 | 2019-03-15 |
| 2 | Ravi | Kumar | M | IT | 78000 | 2021-07-01 |
| 3 | Meera | Nair | F | HR | NULL | 2023-01-10 |
| 4 | Arjun | Singh | M | Sales | 45000 | 2018-11-20 |
| 5 | Neha | Gupta | F | IT | 91000 | 2020-02-05 |
| 6 | Karan | Shah | M | Sales | NULL | 2022-09-12 |
| 7 | Anil | Verma | M | Finance | 30000 | 2024-05-30 |
| 8 | Sana | Khan | F | Finance | 65000 | 2017-08-08 |
**SQL:**
```sql
-- SQLite (run here); standard SQL unless noted
SELECT emp_id, first_name,
       salary,
       COALESCE(salary, 0) AS salary_report
FROM employees;

SELECT AVG(salary) AS avg_ignoring_null, AVG(COALESCE(salary, 0)) AS avg_null_as_zero FROM employees;

-- Same syntax in MySQL / PostgreSQL / SQL Server.
```
**Output:**

Query 1:

| emp_id | first_name | salary | salary_report |
|---|---|---|---|
| 1 | Asha | 52000 | 52000 |
| 2 | Ravi | 78000 | 78000 |
| 3 | Meera | NULL | 0 |
| 4 | Arjun | 45000 | 45000 |
| 5 | Neha | 91000 | 91000 |
| 6 | Karan | NULL | 0 |
| 7 | Anil | 30000 | 30000 |
| 8 | Sana | 65000 | 65000 |

Query 2:

| avg_ignoring_null | avg_null_as_zero |
|---|---|
| 60166.67 | 45125 |
**pandas equivalent:**
```python
res = employees[['emp_id', 'first_name', 'salary']].copy()
res['salary_report'] = res['salary'].fillna(0)
```
Result matches the SQL output.
**Edge cases:** Averages change when NULL becomes 0 (second query: about 60,167 vs 45,125), so decide deliberately. COALESCE can take several arguments, e.g. `COALESCE(bonus, allowance, 0)`.
**Likely follow-ups:**
1. *COALESCE vs ISNULL/IFNULL?* See Q17: COALESCE is standard and takes many arguments.
2. *Can I show text for a missing number?* Cast first: `COALESCE(CAST(salary AS VARCHAR(20)), 'Not set')` because all arguments should be compatible types.
**Common mistakes:** Mixing types (number and text) in one COALESCE; replacing NULL with 0 inside AVG without thinking.

### Q3 ⭐⭐⭐ 🟢 Write a CASE WHEN statement to label employees as Low / Medium / High based on salary.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Basic CASE WHEN logic and range thinking; also whether you remember NULL salaries.
**Say this in the interview:** I use a searched CASE: `CASE WHEN salary < 40000 THEN 'Low' WHEN salary < 70000 THEN 'Medium' ELSE 'High' END`. The first matching condition wins.
**Explain simply:**
- **CASE WHEN** is SQL's if / else-if / else, used inside SELECT.
- Conditions are checked top to bottom and the first true one returns its value, so order matters.
- Without `ELSE`, anything unmatched becomes NULL.
- A NULL salary fails every comparison, so it falls to ELSE ('High' here, which is wrong). Handle it with an explicit `WHEN salary IS NULL` branch placed first.
**Example:** Bands: below 40,000 = Low, 40,000 to 69,999 = Medium, 70,000 and above = High. Anil (30,000) is Low; Ravi (78,000) is High; Meera (blank) should be 'Unknown'.
**Sample data:**

`employees`

| emp_id | first_name | last_name | gender | dept | salary | joining_date |
|---|---|---|---|---|---|---|
| 1 | Asha | Rao | F | HR | 52000 | 2019-03-15 |
| 2 | Ravi | Kumar | M | IT | 78000 | 2021-07-01 |
| 3 | Meera | Nair | F | HR | NULL | 2023-01-10 |
| 4 | Arjun | Singh | M | Sales | 45000 | 2018-11-20 |
| 5 | Neha | Gupta | F | IT | 91000 | 2020-02-05 |
| 6 | Karan | Shah | M | Sales | NULL | 2022-09-12 |
| 7 | Anil | Verma | M | Finance | 30000 | 2024-05-30 |
| 8 | Sana | Khan | F | Finance | 65000 | 2017-08-08 |
**SQL:**
```sql
-- SQLite (run here); standard SQL unless noted
SELECT emp_id, first_name, salary,
       CASE
         WHEN salary IS NULL  THEN 'Unknown'
         WHEN salary < 40000  THEN 'Low'
         WHEN salary < 70000  THEN 'Medium'
         ELSE 'High'
       END AS salary_band
FROM employees
ORDER BY emp_id;

-- Works unchanged in MySQL / PostgreSQL / SQL Server.
```
**Output:**

| emp_id | first_name | salary | salary_band |
|---|---|---|---|
| 1 | Asha | 52000 | Medium |
| 2 | Ravi | 78000 | High |
| 3 | Meera | NULL | Unknown |
| 4 | Arjun | 45000 | Medium |
| 5 | Neha | 91000 | High |
| 6 | Karan | NULL | Unknown |
| 7 | Anil | 30000 | Low |
| 8 | Sana | 65000 | Medium |
**pandas equivalent:**
```python
res = employees[['emp_id', 'first_name', 'salary']].copy()
res['salary_band'] = np.select(
    [res['salary'].isna(), res['salary'] < 40000, res['salary'] < 70000],
    ['Unknown', 'Low', 'Medium'], default='High')
```
Result matches the SQL output.
**Edge cases:** NULL salary (see above). Boundaries: use `<` consistently so 40,000 lands in exactly one band. All THEN results should be the same data type.
**Likely follow-ups:**
1. *Can I use BETWEEN?* Yes, but for decimals `<` and `>=` are safer than BETWEEN's inclusive ends.
2. *Can I count people per band?* Wrap the CASE in a subquery and GROUP BY, see Q37.
**Common mistakes:** Forgetting the NULL case; overlapping ranges; putting a broad condition first so later ones never run.

### Q4 ⭐⭐⭐ 🟢 Explain the syntax of CASE WHEN. What are the simple and searched forms?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** That you know both CASE forms and can pick the right one.
**Say this in the interview:** CASE has two forms. Simple CASE compares one column to fixed values; searched CASE evaluates any true/false condition. Searched is more flexible.
**Explain simply:**
- **Simple CASE:** `CASE col WHEN value THEN result ... END`. It only tests equality (`col = value`).
- **Searched CASE:** `CASE WHEN condition THEN result ... END`. Conditions can be ranges, AND/OR, IS NULL, anything.
- Both stop at the first match; both allow an optional `ELSE`; both end with `END`.
- Simple CASE cannot match NULL (`WHEN NULL` never fires) because it uses equality.
**Example:** Expand department codes with simple CASE ('HR' to 'Human Resources'). Band salaries with searched CASE.
**Sample data:**

`employees`

| emp_id | first_name | last_name | gender | dept | salary | joining_date |
|---|---|---|---|---|---|---|
| 1 | Asha | Rao | F | HR | 52000 | 2019-03-15 |
| 2 | Ravi | Kumar | M | IT | 78000 | 2021-07-01 |
| 3 | Meera | Nair | F | HR | NULL | 2023-01-10 |
| 4 | Arjun | Singh | M | Sales | 45000 | 2018-11-20 |
| 5 | Neha | Gupta | F | IT | 91000 | 2020-02-05 |
| 6 | Karan | Shah | M | Sales | NULL | 2022-09-12 |
| 7 | Anil | Verma | M | Finance | 30000 | 2024-05-30 |
| 8 | Sana | Khan | F | Finance | 65000 | 2017-08-08 |
**SQL:**
```sql
-- SQLite (run here); standard SQL unless noted
SELECT first_name, dept,
       -- simple form
       CASE dept
         WHEN 'HR' THEN 'Human Resources'
         WHEN 'IT' THEN 'Information Technology'
         ELSE dept
       END AS dept_name,
       -- searched form
       CASE WHEN salary >= 70000 THEN 'Senior pay'
            WHEN salary IS NULL  THEN 'Not set'
            ELSE 'Standard' END AS pay_group
FROM employees
ORDER BY emp_id;

-- Identical in all major dialects. SQL Server/MySQL/PostgreSQL additionally allow CASE inside ORDER BY, GROUP BY, UPDATE (Q35, Q36).
```
**Output:**

| first_name | dept | dept_name | pay_group |
|---|---|---|---|
| Asha | HR | Human Resources | Standard |
| Ravi | IT | Information Technology | Senior pay |
| Meera | HR | Human Resources | Not set |
| Arjun | Sales | Sales | Standard |
| Neha | IT | Information Technology | Senior pay |
| Karan | Sales | Sales | Not set |
| Anil | Finance | Finance | Standard |
| Sana | Finance | Finance | Standard |
**pandas equivalent:**
```python
res = employees[['first_name', 'dept']].copy()
res['dept_name'] = res['dept'].map({'HR': 'Human Resources', 'IT': 'Information Technology'}).fillna(res['dept'])
res['pay_group'] = np.select([employees['salary'] >= 70000, employees['salary'].isna()],
                             ['Senior pay', 'Not set'], default='Standard')
```
Result matches the SQL output.
**Edge cases:** `CASE x WHEN NULL` never matches; use searched `WHEN x IS NULL`. Missing ELSE gives NULL. Result types must be compatible.
**Likely follow-ups:**
1. *Is CASE an expression or a statement?* An expression: it returns a value, so it can sit anywhere a value can.
2. *Does CASE short-circuit?* Yes, it returns at the first true branch.
**Common mistakes:** Using `WHEN NULL`; leaving out END; mixing text and numbers in the THEN branches.

### Q5 ⭐⭐⭐ 🟢 How do NULLs behave in aggregate functions (COUNT(*), COUNT(col), SUM, AVG)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know aggregates ignore NULLs and how COUNT(*) differs from COUNT(col).
**Say this in the interview:** COUNT(*) counts all rows. COUNT(col), SUM and AVG skip NULLs, so AVG divides by the number of non-NULL values, not by all rows.
**Explain simply:**
- `COUNT(*)` counts rows, whatever is inside them.
- `COUNT(col)` counts only rows where col is NOT NULL.
- `SUM`, `AVG`, `MIN`, `MAX` ignore NULLs. So AVG = SUM / count of non-NULL, not / total rows.
- If every value is NULL (or there are no rows), SUM and AVG return NULL, while COUNT returns 0.
**Example:** 8 employees, 2 with blank salary. COUNT(*) = 8, COUNT(salary) = 6. The average is over those 6 people only.
**Sample data:**

`employees`

| emp_id | first_name | last_name | gender | dept | salary | joining_date |
|---|---|---|---|---|---|---|
| 1 | Asha | Rao | F | HR | 52000 | 2019-03-15 |
| 2 | Ravi | Kumar | M | IT | 78000 | 2021-07-01 |
| 3 | Meera | Nair | F | HR | NULL | 2023-01-10 |
| 4 | Arjun | Singh | M | Sales | 45000 | 2018-11-20 |
| 5 | Neha | Gupta | F | IT | 91000 | 2020-02-05 |
| 6 | Karan | Shah | M | Sales | NULL | 2022-09-12 |
| 7 | Anil | Verma | M | Finance | 30000 | 2024-05-30 |
| 8 | Sana | Khan | F | Finance | 65000 | 2017-08-08 |
**SQL:**
```sql
-- SQLite (run here); standard SQL unless noted
SELECT COUNT(*)      AS all_rows,
       COUNT(salary) AS salary_not_null,
       SUM(salary)   AS total_salary,
       AVG(salary)   AS avg_salary,
       SUM(salary) * 1.0 / COUNT(*) AS if_nulls_were_zero
FROM employees;

-- Same in MySQL / PostgreSQL / SQL Server.
```
**Output:**

| all_rows | salary_not_null | total_salary | avg_salary | if_nulls_were_zero |
|---|---|---|---|---|
| 8 | 6 | 361000 | 60166.67 | 45125 |
**pandas equivalent:**
```python
res = pd.DataFrame({
    'all_rows': [len(employees)],
    'salary_not_null': [employees['salary'].count()],
    'total_salary': [employees['salary'].sum()],
    'avg_salary': [employees['salary'].mean()],
    'if_nulls_were_zero': [employees['salary'].sum() / len(employees)]})
```
Result matches the SQL output.
**Edge cases:** Pandas `.count()` also skips NaN, like SQL COUNT(col); `len()` is like COUNT(*). `SUM` over all-NULL gives NULL, so wrap with `COALESCE(SUM(x),0)` if you need 0. `COUNT(DISTINCT col)` also ignores NULL.
**Likely follow-ups:**
1. *Why does AVG look higher than expected?* NULLs are not counted as 0.
2. *How do I treat NULL as 0 in AVG?* `AVG(COALESCE(salary,0))`.
**Common mistakes:** Using COUNT(col) when you mean rows; assuming AVG divides by all rows.

### Q6 ⭐⭐⭐ 🟢 How do you find the difference in days between two dates (e.g., joining date and today) in MySQL, PostgreSQL and SQL Server?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know date-difference syntax differs by dialect.
**Say this in the interview:** MySQL: `DATEDIFF(CURDATE(), joining_date)`. PostgreSQL: subtract the dates, `CURRENT_DATE - joining_date`. SQL Server: `DATEDIFF(day, joining_date, GETDATE())`. Watch argument order.
**Explain simply:**
- MySQL `DATEDIFF(end, start)` returns days, with the **later date first**.
- SQL Server `DATEDIFF(day, start, end)` has the **earlier date first** and needs the unit.
- PostgreSQL has no DATEDIFF; date minus date gives an integer number of days.
- SQLite (used here to run the code) uses `julianday(end) - julianday(start)`. I fix 'today' at 2025-06-30 so results are repeatable.
**Example:** Asha joined 2019-03-15; on 2025-06-30 she has 2,299 days of service.
**Sample data:**

`employees`

| emp_id | first_name | last_name | gender | dept | salary | joining_date |
|---|---|---|---|---|---|---|
| 1 | Asha | Rao | F | HR | 52000 | 2019-03-15 |
| 2 | Ravi | Kumar | M | IT | 78000 | 2021-07-01 |
| 3 | Meera | Nair | F | HR | NULL | 2023-01-10 |
| 4 | Arjun | Singh | M | Sales | 45000 | 2018-11-20 |
| 5 | Neha | Gupta | F | IT | 91000 | 2020-02-05 |
| 6 | Karan | Shah | M | Sales | NULL | 2022-09-12 |
| 7 | Anil | Verma | M | Finance | 30000 | 2024-05-30 |
| 8 | Sana | Khan | F | Finance | 65000 | 2017-08-08 |
**SQL:**
```sql
-- SQLite (run here); standard SQL unless noted
SELECT first_name, joining_date,
       CAST(julianday('2025-06-30') - julianday(joining_date) AS INTEGER) AS days_in_company
FROM employees
ORDER BY emp_id;

-- Not run here (other dialects):
-- MySQL:      SELECT DATEDIFF(CURDATE(), joining_date) FROM employees;
-- PostgreSQL: SELECT CURRENT_DATE - joining_date FROM employees;   -- joining_date must be DATE
-- SQL Server: SELECT DATEDIFF(day, joining_date, GETDATE()) FROM employees;
```
**Output:**

| first_name | joining_date | days_in_company |
|---|---|---|
| Asha | 2019-03-15 | 2299 |
| Ravi | 2021-07-01 | 1460 |
| Meera | 2023-01-10 | 902 |
| Arjun | 2018-11-20 | 2414 |
| Neha | 2020-02-05 | 1972 |
| Karan | 2022-09-12 | 1022 |
| Anil | 2024-05-30 | 396 |
| Sana | 2017-08-08 | 2883 |
**pandas equivalent:**
```python
today = pd.Timestamp('2025-06-30')
res = employees[['first_name', 'joining_date']].copy()
res['days_in_company'] = (today - pd.to_datetime(res['joining_date'])).dt.days
```
Result matches the SQL output.
**Edge cases:** NULL joining date gives NULL. Time parts make DATEDIFF fractional/rounded differently by dialect. SQL Server counts boundaries crossed (midnights), not elapsed 24-hour periods.
**Likely follow-ups:**
1. *How to get months or years?* Change the unit: `DATEDIFF(month, ...)` (SQL Server), `TIMESTAMPDIFF(MONTH, a, b)` (MySQL), `AGE()` (PostgreSQL). See Q12.
2. *Order of arguments?* Most common bug: MySQL end-first, SQL Server start-first.
**Common mistakes:** Swapping argument order and getting negative days; using `GETDATE()` in MySQL; storing dates as text.

### Q7 ⭐⭐⭐ 🟢 How do you get the current date and current timestamp in each dialect (NOW, CURRENT_DATE, GETDATE)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Dialect awareness for the most basic date functions.
**Say this in the interview:** MySQL: `CURDATE()`, `NOW()`. PostgreSQL: `CURRENT_DATE`, `NOW()`. SQL Server: `GETDATE()` or `SYSDATETIME()`, plus `CAST(GETDATE() AS DATE)` for date only. `CURRENT_TIMESTAMP` is standard and works in all.
**Explain simply:**
- `CURRENT_DATE` and `CURRENT_TIMESTAMP` are ANSI standard (MySQL, PostgreSQL, SQLite; SQL Server only has CURRENT_TIMESTAMP).
- `NOW()` works in MySQL and PostgreSQL, not in SQL Server.
- `GETDATE()` is SQL Server only; `SYSDATE` is Oracle.
- 'Current' time is the database server's clock and time zone, not your laptop's.
**Example:** A daily HR report that says 'employees joined in the last 7 days' needs today's date computed at run time, never typed in.
**SQL:**
```sql
-- SQLite (run here); standard SQL unless noted
SELECT CURRENT_DATE AS today, CURRENT_TIMESTAMP AS now_utc, date('now') AS sqlite_date, datetime('now') AS sqlite_datetime;

-- Not run here:
-- MySQL:      SELECT CURDATE(), NOW(), CURRENT_TIMESTAMP;
-- PostgreSQL: SELECT CURRENT_DATE, NOW(), CURRENT_TIMESTAMP;
-- SQL Server: SELECT CAST(GETDATE() AS DATE), GETDATE(), SYSDATETIME(), CURRENT_TIMESTAMP;
```
**Output:**

| today | now_utc | sqlite_date | sqlite_datetime |
|---|---|---|---|
| 2026-10-21 | 2026-10-21 05:55:32 | 2026-10-21 | 2026-10-21 05:55:32 |
**pandas equivalent:**
```python
res = pd.DataFrame({'today': [pd.Timestamp.now().normalize()], 'now': [pd.Timestamp.now()]})
# values differ every run, like the SQL output
```
**Edge cases:** Output above is the value on the day this was run, so yours will differ. SQLite and some servers report UTC, not local time (Q59). In PostgreSQL `NOW()` is fixed for the whole transaction.
**Likely follow-ups:**
1. *Date vs timestamp?* Date has no time part; timestamp has both (Q53).
2. *Why is `NOW()` the same for all rows in a statement?* It is evaluated once per statement (per transaction in PostgreSQL).
**Common mistakes:** Hard-coding today's date; mixing up GETDATE (SQL Server) with NOW (MySQL/PostgreSQL).

### Q8 ⭐⭐⭐ 🟢 How do you filter rows for the last 30 days / this month / this year?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Relative date filtering without functions on the column, and correct month/year boundaries.
**Say this in the interview:** Compare the date column to a computed start date, with `>=` start and `<` next start. I avoid wrapping the column in a function so an index can be used.
**Explain simply:**
- **Last 30 days:** `order_date >= today - 30 days`.
- **This month:** `>= first day of this month` and `< first day of next month`.
- **This year:** `>= Jan 1 this year` and `< Jan 1 next year`.
- Half-open ranges (`>=` and `<`) are safe even if the column has a time part (BETWEEN would miss the last day's later times).
**Example:** Taking 'today' as 2025-06-30: last 30 days starts 2025-05-31; this month starts 2025-06-01; this year starts 2025-01-01.
**Sample data:**

`sales`

| order_id | order_date | region | amount |
|---|---|---|---|
| 1 | 2025-06-02 | North | 1200 |
| 2 | 2025-05-31 | South | 800 |
| 3 | 2025-05-28 | North | 500 |
| 4 | 2025-06-29 | South | 1500 |
| 5 | 2025-01-10 | North | 700 |
| 6 | 2024-12-20 | South | 900 |
| 7 | 2025-06-30 | North | 400 |
**SQL:**
```sql
-- SQLite (run here); standard SQL unless noted
-- last 30 days
SELECT order_id, order_date, amount FROM sales
WHERE order_date >= date('2025-06-30', '-30 days') AND order_date <= '2025-06-30';

-- this month
SELECT order_id, order_date, amount FROM sales
WHERE order_date >= date('2025-06-30', 'start of month')
  AND order_date <  date('2025-06-30', 'start of month', '+1 month');

-- this year
SELECT order_id, order_date, amount FROM sales
WHERE order_date >= date('2025-06-30', 'start of year')
  AND order_date <  date('2025-06-30', 'start of year', '+1 year');

-- Not run here (replace the fixed date with the live one):
-- MySQL:      WHERE order_date >= CURDATE() - INTERVAL 30 DAY
--             month: >= DATE_FORMAT(CURDATE(), '%Y-%m-01') AND < DATE_FORMAT(CURDATE(), '%Y-%m-01') + INTERVAL 1 MONTH
-- PostgreSQL: WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
--             month: >= date_trunc('month', CURRENT_DATE) AND < date_trunc('month', CURRENT_DATE) + INTERVAL '1 month'
-- SQL Server: WHERE order_date >= DATEADD(day, -30, CAST(GETDATE() AS DATE))
--             month: >= DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1)  (SQL Server 2022: DATETRUNC)
```
**Output:**

Query 1:

| order_id | order_date | amount |
|---|---|---|
| 1 | 2025-06-02 | 1200 |
| 2 | 2025-05-31 | 800 |
| 4 | 2025-06-29 | 1500 |
| 7 | 2025-06-30 | 400 |

Query 2:

| order_id | order_date | amount |
|---|---|---|
| 1 | 2025-06-02 | 1200 |
| 4 | 2025-06-29 | 1500 |
| 7 | 2025-06-30 | 400 |

Query 3:

| order_id | order_date | amount |
|---|---|---|
| 1 | 2025-06-02 | 1200 |
| 2 | 2025-05-31 | 800 |
| 3 | 2025-05-28 | 500 |
| 4 | 2025-06-29 | 1500 |
| 5 | 2025-01-10 | 700 |
| 7 | 2025-06-30 | 400 |
**pandas equivalent:**
```python
sales['order_date'] = pd.to_datetime(sales['order_date'])
today = pd.Timestamp('2025-06-30')
res = sales[(sales['order_date'] >= today - pd.Timedelta(days=30)) & (sales['order_date'] <= today)][['order_id', 'order_date', 'amount']]
res = res.assign(order_date=res['order_date'].dt.strftime('%Y-%m-%d'))
```
Result matches the SQL output.
**Edge cases:** 'Last 30 days' is ambiguous (30 days back, or 30 days including today?). State your choice. Future-dated rows are excluded by the upper bound. Order 3 (2025-05-28) falls outside all but the year filter.
**Likely follow-ups:**
1. *Why not `MONTH(order_date)=6`?* It breaks index use and ignores year, see Q56.
2. *Last full month?* From first day of last month up to (but not including) first day of this month.
**Common mistakes:** Using BETWEEN with timestamps; filtering MONTH() without YEAR(); off-by-one in the 30 days.

### Q9 ⭐⭐⭐ 🟢 How do you concatenate first name and last name into a full name? Does it differ across dialects?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** String concatenation and dialect differences.
**Say this in the interview:** Standard SQL and PostgreSQL use `||`; MySQL uses `CONCAT()`; SQL Server uses `+` or `CONCAT()`. CONCAT_WS is handy for adding a separator.
**Explain simply:**
- **Concatenation** = joining text pieces into one.
- `first || ' ' || last` works in PostgreSQL, SQLite, Oracle. In MySQL `||` means OR by default.
- `CONCAT(first, ' ', last)` works in MySQL, PostgreSQL, SQL Server 2012+.
- SQL Server also supports `first + ' ' + last`.
**Example:** Asha + Rao becomes 'Asha Rao' for a name badge or a report column.
**Sample data:**

`employees`

| emp_id | first_name | last_name | gender | dept | salary | joining_date |
|---|---|---|---|---|---|---|
| 1 | Asha | Rao | F | HR | 52000 | 2019-03-15 |
| 2 | Ravi | Kumar | M | IT | 78000 | 2021-07-01 |
| 3 | Meera | Nair | F | HR | NULL | 2023-01-10 |
| 4 | Arjun | Singh | M | Sales | 45000 | 2018-11-20 |
| 5 | Neha | Gupta | F | IT | 91000 | 2020-02-05 |
| 6 | Karan | Shah | M | Sales | NULL | 2022-09-12 |
| 7 | Anil | Verma | M | Finance | 30000 | 2024-05-30 |
| 8 | Sana | Khan | F | Finance | 65000 | 2017-08-08 |
**SQL:**
```sql
-- SQLite (run here); standard SQL unless noted
SELECT emp_id, first_name || ' ' || last_name AS full_name
FROM employees
ORDER BY emp_id;

-- Not run here:
-- MySQL / PostgreSQL / SQL Server 2012+: SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM employees;
-- SQL Server:  SELECT first_name + ' ' + last_name FROM employees;
-- With separator: CONCAT_WS(' ', first_name, last_name)  -- MySQL, PostgreSQL, SQL Server 2017+
```
**Output:**

| emp_id | full_name |
|---|---|
| 1 | Asha Rao |
| 2 | Ravi Kumar |
| 3 | Meera Nair |
| 4 | Arjun Singh |
| 5 | Neha Gupta |
| 6 | Karan Shah |
| 7 | Anil Verma |
| 8 | Sana Khan |
**pandas equivalent:**
```python
res = employees[['emp_id']].copy()
res['full_name'] = employees['first_name'] + ' ' + employees['last_name']
```
Result matches the SQL output.
**Edge cases:** NULL handling differs: `||`, `+` and MySQL's CONCAT return NULL if any part is NULL, while PostgreSQL's and SQL Server's CONCAT treat NULL as empty (from memory; see Q29).
**Likely follow-ups:**
1. *How to avoid a double space when last name is blank?* `TRIM(CONCAT(...))` or CONCAT_WS.
2. *Can I concat numbers?* Cast to text first in strict dialects.
**Common mistakes:** Using `+` in MySQL (it adds numbers); using `||` in MySQL; forgetting the space between names.

### Q10 ⭐⭐⭐ 🟡 How do you use CASE WHEN inside an aggregate (conditional aggregation) to count male and female employees in one query?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Conditional aggregation, the core 'pivot-lite' trick for HR dashboards.
**Say this in the interview:** I put CASE WHEN inside SUM or COUNT: `SUM(CASE WHEN gender='M' THEN 1 ELSE 0 END)` for males and a second one for females, all in a single pass.
**Explain simply:**
- **Aggregate** = a function over many rows (SUM, COUNT, AVG).
- CASE gives 1 when the row matches and 0 when it does not; SUM then counts the matches.
- `COUNT(CASE WHEN gender='M' THEN 1 END)` is the same, because COUNT skips the NULL from the missing ELSE.
- PostgreSQL/SQLite also allow `COUNT(*) FILTER (WHERE gender='M')`.
**Example:** Headcount by gender for each department (HR, IT, Sales, Finance) in one query, ready for a diversity dashboard.
**Sample data:**

`employees`

| emp_id | first_name | last_name | gender | dept | salary | joining_date |
|---|---|---|---|---|---|---|
| 1 | Asha | Rao | F | HR | 52000 | 2019-03-15 |
| 2 | Ravi | Kumar | M | IT | 78000 | 2021-07-01 |
| 3 | Meera | Nair | F | HR | NULL | 2023-01-10 |
| 4 | Arjun | Singh | M | Sales | 45000 | 2018-11-20 |
| 5 | Neha | Gupta | F | IT | 91000 | 2020-02-05 |
| 6 | Karan | Shah | M | Sales | NULL | 2022-09-12 |
| 7 | Anil | Verma | M | Finance | 30000 | 2024-05-30 |
| 8 | Sana | Khan | F | Finance | 65000 | 2017-08-08 |
**SQL:**
```sql
-- SQLite (run here); standard SQL unless noted
SELECT dept,
       SUM(CASE WHEN gender = 'M' THEN 1 ELSE 0 END) AS male,
       SUM(CASE WHEN gender = 'F' THEN 1 ELSE 0 END) AS female,
       COUNT(*) AS total
FROM employees
GROUP BY dept
ORDER BY dept;

-- PostgreSQL / SQLite alternative: COUNT(*) FILTER (WHERE gender = 'M') AS male
-- Same CASE version works in MySQL / SQL Server.
```
**Output:**

| dept | male | female | total |
|---|---|---|---|
| Finance | 1 | 1 | 2 |
| HR | 0 | 2 | 2 |
| IT | 1 | 1 | 2 |
| Sales | 2 | 0 | 2 |
**pandas equivalent:**
```python
res = (employees.groupby('dept')
       .agg(male=('gender', lambda s: (s == 'M').sum()),
            female=('gender', lambda s: (s == 'F').sum()),
            total=('gender', 'size'))
       .reset_index())
```
Result matches the SQL output.
**Edge cases:** Genders other than M/F or NULL are in total but in neither column. ELSE 0 vs no ELSE with SUM: an empty group would give NULL without ELSE 0.
**Likely follow-ups:**
1. *Why not two queries with WHERE?* One pass over the table, and you get both side by side.
2. *Percent female?* `100.0 * SUM(CASE WHEN gender='F' THEN 1 ELSE 0 END) / COUNT(*)`, see Q41.
**Common mistakes:** Using `COUNT(CASE ... ELSE 0 END)`, which counts the zeros too and gives the total.

### Q11 ⭐⭐⭐ 🟡 How do you get the month and year from a date column and group sales by month?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Date part extraction and grouping by month (always include the year).
**Say this in the interview:** I turn the date into a year-month key, for example `strftime('%Y-%m', d)` in SQLite or `DATE_TRUNC('month', d)` in PostgreSQL, then GROUP BY that key with SUM.
**Explain simply:**
- Group by **year and month together**; grouping by month number alone mixes January 2024 with January 2025.
- MySQL: `DATE_FORMAT(d,'%Y-%m')`, or `YEAR(d), MONTH(d)`.
- PostgreSQL: `DATE_TRUNC('month', d)` or `TO_CHAR(d,'YYYY-MM')`; SQL Server: `FORMAT(d,'yyyy-MM')` or `YEAR(d), MONTH(d)`.
- Text keys 'YYYY-MM' sort correctly alphabetically.
**Example:** Sales of 1,200 and 400 in June 2025 roll up into one June row of 1,600 (plus other June orders).
**Sample data:**

`sales`

| order_id | order_date | region | amount |
|---|---|---|---|
| 1 | 2025-06-02 | North | 1200 |
| 2 | 2025-05-31 | South | 800 |
| 3 | 2025-05-28 | North | 500 |
| 4 | 2025-06-29 | South | 1500 |
| 5 | 2025-01-10 | North | 700 |
| 6 | 2024-12-20 | South | 900 |
| 7 | 2025-06-30 | North | 400 |
**SQL:**
```sql
-- SQLite (run here); standard SQL unless noted
SELECT strftime('%Y', order_date) AS yr,
       strftime('%m', order_date) AS mth,
       SUM(amount) AS total_sales
FROM sales
GROUP BY strftime('%Y', order_date), strftime('%m', order_date)
ORDER BY yr, mth;

-- Not run here:
-- MySQL:      SELECT YEAR(order_date) yr, MONTH(order_date) mth, SUM(amount) FROM sales GROUP BY YEAR(order_date), MONTH(order_date);
-- PostgreSQL: SELECT EXTRACT(YEAR FROM order_date) yr, EXTRACT(MONTH FROM order_date) mth, SUM(amount) FROM sales GROUP BY 1, 2 ORDER BY 1, 2;
-- SQL Server: SELECT YEAR(order_date), MONTH(order_date), SUM(amount) FROM sales GROUP BY YEAR(order_date), MONTH(order_date);
```
**Output:**

| yr | mth | total_sales |
|---|---|---|
| 2024 | 12 | 900 |
| 2025 | 01 | 700 |
| 2025 | 05 | 1300 |
| 2025 | 06 | 3100 |
**pandas equivalent:**
```python
sales['order_date'] = pd.to_datetime(sales['order_date'])
res = (sales.assign(yr=sales['order_date'].dt.strftime('%Y'), mth=sales['order_date'].dt.strftime('%m'))
       .groupby(['yr', 'mth'], as_index=False)['amount'].sum()
       .rename(columns={'amount': 'total_sales'}))
```
Result matches the SQL output.
**Edge cases:** Months with no sales do not appear (see Q42/Q60 for a calendar table). NULL dates form their own group. Do not forget the year.
**Likely follow-ups:**
1. *How to show month names?* `TO_CHAR(d,'Mon')`, `DATE_FORMAT(d,'%b')`, `FORMAT(d,'MMM')`.
2. *Why is SQLite's strftime returning text?* SQLite has no real date type; dates are text.
**Common mistakes:** Grouping by month name or number only; selecting a column that is not in GROUP BY.

### Q12 ⭐⭐⭐ 🟡 How do you calculate each employee's tenure in years from their joining date?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you handle 'completed years' correctly rather than just dividing days by 365.
**Say this in the interview:** For completed years I take year difference and subtract one if the anniversary has not arrived yet; for a quick decimal I divide days by 365.25.
**Explain simply:**
- **Tenure** = how long someone has worked, from joining date to today (or to leaving date).
- Subtracting only the years (2025 - 2019) overstates tenure if the work anniversary is later in the year.
- Dialect shortcuts: MySQL `TIMESTAMPDIFF(YEAR, joining_date, CURDATE())`; PostgreSQL `DATE_PART('year', AGE(joining_date))`; SQL Server needs the anniversary check because `DATEDIFF(year, ...)` just counts year boundaries.
- I fix 'today' at 2025-06-30 for repeatable output.
**Example:** Asha joined 15 Mar 2019: on 30 Jun 2025 she has completed 6 years (6.3 in decimals). Sana joined 8 Aug 2017: her 8th anniversary (Aug 2025) has not arrived, so she has 7 completed years, not 8.
**Sample data:**

`employees`

| emp_id | first_name | last_name | gender | dept | salary | joining_date |
|---|---|---|---|---|---|---|
| 1 | Asha | Rao | F | HR | 52000 | 2019-03-15 |
| 2 | Ravi | Kumar | M | IT | 78000 | 2021-07-01 |
| 3 | Meera | Nair | F | HR | NULL | 2023-01-10 |
| 4 | Arjun | Singh | M | Sales | 45000 | 2018-11-20 |
| 5 | Neha | Gupta | F | IT | 91000 | 2020-02-05 |
| 6 | Karan | Shah | M | Sales | NULL | 2022-09-12 |
| 7 | Anil | Verma | M | Finance | 30000 | 2024-05-30 |
| 8 | Sana | Khan | F | Finance | 65000 | 2017-08-08 |
**SQL:**
```sql
-- SQLite (run here); standard SQL unless noted
SELECT first_name, joining_date,
       (CAST(strftime('%Y', '2025-06-30') AS INT) - CAST(strftime('%Y', joining_date) AS INT))
         - (strftime('%m-%d', '2025-06-30') < strftime('%m-%d', joining_date)) AS tenure_years,
       ROUND((julianday('2025-06-30') - julianday(joining_date)) / 365.25, 1) AS tenure_decimal
FROM employees
ORDER BY emp_id;

-- Not run here:
-- MySQL:      TIMESTAMPDIFF(YEAR, joining_date, CURDATE())
-- PostgreSQL: DATE_PART('year', AGE(CURRENT_DATE, joining_date))
-- SQL Server: DATEDIFF(year, joining_date, GETDATE())
--             - CASE WHEN DATEADD(year, DATEDIFF(year, joining_date, GETDATE()), joining_date) > GETDATE() THEN 1 ELSE 0 END
```
**Output:**

| first_name | joining_date | tenure_years | tenure_decimal |
|---|---|---|---|
| Asha | 2019-03-15 | 6 | 6.3 |
| Ravi | 2021-07-01 | 3 | 4 |
| Meera | 2023-01-10 | 2 | 2.5 |
| Arjun | 2018-11-20 | 6 | 6.6 |
| Neha | 2020-02-05 | 5 | 5.4 |
| Karan | 2022-09-12 | 2 | 2.8 |
| Anil | 2024-05-30 | 1 | 1.1 |
| Sana | 2017-08-08 | 7 | 7.9 |
**pandas equivalent:**
```python
today = pd.Timestamp('2025-06-30')
jd = pd.to_datetime(employees['joining_date'])
res = employees[['first_name', 'joining_date']].copy()
res['tenure_years'] = today.year - jd.dt.year - (((today.month, today.day) < pd.Series(list(zip(jd.dt.month, jd.dt.day)))).astype(int))
res['tenure_decimal'] = ((today - jd).dt.days / 365.25).round(1)
```
Result matches the SQL output.
**Edge cases:** Leavers should use leaving date instead of today: `COALESCE(leaving_date, today)`. 29 Feb joiners need care. Ravi shows 3 completed years but 4 decimal years because 3.99 rounds up to 4.0. Rounding: `ROUND(x, 1)` of .x5 differs slightly between engines.
**Likely follow-ups:**
1. *Why not days/365?* Leap years make it drift.
2. *Why does SQL Server's DATEDIFF(year) mislead?* It counts calendar-year boundaries: 31 Dec 2024 to 1 Jan 2025 = 1 year.
**Common mistakes:** Using YEAR(today) - YEAR(joining_date); ignoring leavers.

### Q13 ⭐⭐⭐ 🟡 How does NULL affect joins and comparisons, such as WHERE col <> 'X' skipping NULL rows?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Three-valued logic: whether you realise NULL rows silently vanish from <> and from join matches.
**Say this in the interview:** Any comparison with NULL is unknown, and WHERE only keeps true rows. So `status <> 'Active'` drops NULL-status rows; I add `OR status IS NULL`. In joins, NULL keys never match each other either.
**Explain simply:**
- SQL logic has three outcomes: true, false, unknown. NULL comparisons give unknown.
- `WHERE status <> 'Active'` keeps only rows where it is true; NULL status gives unknown, so it is skipped.
- Fix: `OR status IS NULL`, or `COALESCE(status,'Unknown') <> 'Active'`.
- In a JOIN, `a.key = b.key` with both NULL is unknown, so those rows do not match (they show up only in outer joins as unmatched).
**Example:** Of 6 employees: 2 Active, 2 Resigned, 2 with blank status. 'Not active' should arguably be 4 people, but `<> 'Active'` returns only 2.
**Sample data:**

`emp_status`

| emp_id | name | status |
|---|---|---|
| 1 | Asha | Active |
| 2 | Ravi | Resigned |
| 3 | Meera | NULL |
| 4 | Arjun | Active |
| 5 | Neha | NULL |
| 6 | Karan | Resigned |
**SQL:**
```sql
-- SQLite (run here); standard SQL unless noted
SELECT emp_id, name, status FROM emp_status WHERE status <> 'Active';

SELECT emp_id, name, status FROM emp_status WHERE status <> 'Active' OR status IS NULL;

WITH a(k) AS (VALUES (1), (NULL)), b(k) AS (VALUES (1), (NULL))
SELECT a.k AS a_key, b.k AS b_key FROM a JOIN b ON a.k = b.k;

-- Same behaviour in MySQL / PostgreSQL / SQL Server (Oracle also treats '' as NULL).
```
**Output:**

Query 1:

| emp_id | name | status |
|---|---|---|
| 2 | Ravi | Resigned |
| 6 | Karan | Resigned |

Query 2:

| emp_id | name | status |
|---|---|---|
| 2 | Ravi | Resigned |
| 3 | Meera | NULL |
| 5 | Neha | NULL |
| 6 | Karan | Resigned |

Query 3:

| a_key | b_key |
|---|---|
| 1 | 1 |
**pandas equivalent:**
```python
# SQL-style: NULL rows excluded
res = emp_status.loc[emp_status['status'].notna() & (emp_status['status'] != 'Active'), ['emp_id', 'name', 'status']]
# Note: pandas (status != 'Active') alone would also return the NaN rows, unlike SQL
```
Result matches the SQL output.
**Edge cases:** Pandas differs from SQL here: NaN != 'Active' is True. `NOT IN (subquery)` with a NULL in the list returns no rows at all (use NOT EXISTS). Aggregates and DISTINCT/GROUP BY do treat NULLs as one group.
**Likely follow-ups:**
1. *How do I make NULLs match in a join?* `ON a.k = b.k OR (a.k IS NULL AND b.k IS NULL)`, or NULL-safe operators (Q43).
2. *NULL in NOT IN?* Returns nothing; use NOT EXISTS.
**Common mistakes:** Assuming `<>` includes NULLs; assuming NULL = NULL in joins.

### Q14 ⭐⭐⭐ 🟡 How do you pivot rows to columns using CASE WHEN (e.g., monthly sales in separate columns)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Pivoting rows to columns manually with conditional aggregation.
**Say this in the interview:** For each column I write `SUM(CASE WHEN month = X THEN amount ELSE 0 END)` and GROUP BY the row label. It works in every dialect without PIVOT.
**Explain simply:**
- **Pivot** = turning values of one column (months) into separate columns.
- One CASE per output column, wrapped in SUM; GROUP BY the thing that stays as rows (region).
- SQL Server has a `PIVOT` operator and PostgreSQL has `crosstab()`, but CASE is portable.
- The column list is fixed in the query; new months need a new column (or dynamic SQL).
**Example:** Rows: region (North, South). Columns: Jan, May, Jun 2025 sales.
**Sample data:**

`sales`

| order_id | order_date | region | amount |
|---|---|---|---|
| 1 | 2025-06-02 | North | 1200 |
| 2 | 2025-05-31 | South | 800 |
| 3 | 2025-05-28 | North | 500 |
| 4 | 2025-06-29 | South | 1500 |
| 5 | 2025-01-10 | North | 700 |
| 6 | 2024-12-20 | South | 900 |
| 7 | 2025-06-30 | North | 400 |
**SQL:**
```sql
-- SQLite (run here); standard SQL unless noted
SELECT region,
       SUM(CASE WHEN strftime('%Y-%m', order_date) = '2025-01' THEN amount ELSE 0 END) AS jan_2025,
       SUM(CASE WHEN strftime('%Y-%m', order_date) = '2025-05' THEN amount ELSE 0 END) AS may_2025,
       SUM(CASE WHEN strftime('%Y-%m', order_date) = '2025-06' THEN amount ELSE 0 END) AS jun_2025
FROM sales
GROUP BY region
ORDER BY region;

-- Month test in other dialects: MySQL DATE_FORMAT(order_date,'%Y-%m'); PostgreSQL TO_CHAR(order_date,'YYYY-MM'); SQL Server FORMAT(order_date,'yyyy-MM').
```
**Output:**

| region | jan_2025 | may_2025 | jun_2025 |
|---|---|---|---|
| North | 700 | 500 | 1600 |
| South | 0 | 800 | 1500 |
**pandas equivalent:**
```python
sales['order_date'] = pd.to_datetime(sales['order_date'])
s = sales.assign(ym=sales['order_date'].dt.strftime('%Y-%m'))
res = (s.pivot_table(index='region', columns='ym', values='amount', aggfunc='sum', fill_value=0)
       .reindex(columns=['2025-01', '2025-05', '2025-06'], fill_value=0)
       .rename(columns={'2025-01': 'jan_2025', '2025-05': 'may_2025', '2025-06': 'jun_2025'})
       .reset_index())
res.columns.name = None
```
Result matches the SQL output.
**Edge cases:** Use ELSE 0 (or COALESCE) to avoid NULL cells. Months outside the listed ones (Dec 2024) are silently dropped.
**Likely follow-ups:**
1. *Dynamic month columns?* Needs dynamic SQL (build the query string), or do it in the BI tool.
2. *Unpivot?* `UNION ALL` of one SELECT per column, or UNPIVOT in SQL Server.
**Common mistakes:** Forgetting GROUP BY; using COUNT instead of SUM; comparing month number without year.

### Q15 ⭐⭐ 🟢 What is NULLIF and when do you use it (e.g., avoiding divide-by-zero)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know the NULLIF trick for safe division.
**Say this in the interview:** NULLIF(a, b) returns NULL when a equals b, otherwise a. Putting `NULLIF(denominator, 0)` makes a divide-by-zero return NULL instead of an error.
**Explain simply:**
- `NULLIF(x, y)` = 'give NULL if x = y, else give x'. It is the opposite of COALESCE.
- Division by NULL gives NULL, so the query keeps running.
- PostgreSQL and SQL Server raise an error on /0 (SQLite and MySQL by default return NULL), so the guard is needed for portability.
- Also useful to turn blank strings into NULL: `NULLIF(TRIM(col), '')`.
**Example:** IT has a budget of 900,000 but 0 headcount; budget per head would be a divide-by-zero. With NULLIF it shows NULL.
**Sample data:**

`dept_stats`

| dept | budget | headcount | leavers |
|---|---|---|---|
| HR | 500000 | 5 | 1 |
| IT | 900000 | 0 | 0 |
| Sales | 300000 | 3 | 1 |
| Finance | 400000 | 4 | 2 |
**SQL:**
```sql
-- SQLite (run here); standard SQL unless noted
SELECT dept, budget, headcount,
       budget * 1.0 / NULLIF(headcount, 0) AS budget_per_head
FROM dept_stats
ORDER BY dept;

-- Same in MySQL / PostgreSQL / SQL Server. Integer division: multiply by 1.0 (or cast) to avoid truncation in SQL Server / PostgreSQL.
```
**Output:**

| dept | budget | headcount | budget_per_head |
|---|---|---|---|
| Finance | 400000 | 4 | 100000 |
| HR | 500000 | 5 | 100000 |
| IT | 900000 | 0 | NULL |
| Sales | 300000 | 3 | 100000 |
**pandas equivalent:**
```python
res = dept_stats[['dept', 'budget', 'headcount']].sort_values('dept').reset_index(drop=True)
res['budget_per_head'] = res['budget'] / res['headcount'].replace(0, np.nan)
```
Result matches the SQL output.
**Edge cases:** Integer / integer truncates in PostgreSQL and SQL Server (5/2 = 2). Pandas gives inf for /0 unless you replace 0 with NaN. Show NULL as 'n/a' with COALESCE if needed.
**Likely follow-ups:**
1. *COALESCE on top?* `COALESCE(x / NULLIF(y,0), 0)` if 0 is acceptable.
2. *Different from CASE?* Same result as `CASE WHEN y = 0 THEN NULL ELSE x / y END`, just shorter.
**Common mistakes:** Writing `NULLIF(headcount = 0)`; getting integer division; replacing with 0 and hiding bad data.

### Q16 ⭐⭐ 🟢 How do you avoid a division-by-zero error when calculating a percentage?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Practical safe-division and percentage calculation.
**Say this in the interview:** I guard the denominator with NULLIF and multiply by 100.0 (a decimal) so I get a real percentage: `100.0 * leavers / NULLIF(headcount, 0)`.
**Explain simply:**
- Percentage = part / whole x 100.
- Guard the whole with `NULLIF(whole, 0)` so a zero gives NULL instead of an error.
- Use `100.0` (decimal) so SQL does not do integer division and round everything to 0.
- Optionally `COALESCE(..., 0)` if a missing percentage should show as 0.
**Example:** Attrition rate per department: HR 1 leaver out of 5 = 20%. IT has 0 headcount, so rate is undefined (NULL).
**Sample data:**

`dept_stats`

| dept | budget | headcount | leavers |
|---|---|---|---|
| HR | 500000 | 5 | 1 |
| IT | 900000 | 0 | 0 |
| Sales | 300000 | 3 | 1 |
| Finance | 400000 | 4 | 2 |
**SQL:**
```sql
-- SQLite (run here); standard SQL unless noted
SELECT dept, leavers, headcount,
       ROUND(100.0 * leavers / NULLIF(headcount, 0), 1) AS attrition_pct,
       COALESCE(ROUND(100.0 * leavers / NULLIF(headcount, 0), 1), 0) AS attrition_pct_or_zero
FROM dept_stats
ORDER BY dept;

-- Same in all dialects. SQL Server/PostgreSQL: 100.0 keeps decimals; 100 * leavers / headcount would truncate integers.
```
**Output:**

| dept | leavers | headcount | attrition_pct | attrition_pct_or_zero |
|---|---|---|---|---|
| Finance | 2 | 4 | 50 | 50 |
| HR | 1 | 5 | 20 | 20 |
| IT | 0 | 0 | NULL | 0 |
| Sales | 1 | 3 | 33.3 | 33.3 |
**pandas equivalent:**
```python
res = dept_stats[['dept', 'leavers', 'headcount']].sort_values('dept').reset_index(drop=True)
res['attrition_pct'] = (100.0 * res['leavers'] / res['headcount'].replace(0, np.nan)).round(1)
res['attrition_pct_or_zero'] = res['attrition_pct'].fillna(0)
```
Result matches the SQL output.
**Edge cases:** Zero denominator (shown), NULL denominator (gives NULL), integer division. Do not average percentages across groups; recompute from totals.
**Likely follow-ups:**
1. *Why not just use a CASE?* You can; NULLIF is shorter.
2. *Overall percentage?* `100.0 * SUM(leavers) / NULLIF(SUM(headcount),0)`.
**Common mistakes:** Integer division; hiding 0-headcount with 0 so it looks like 'no attrition'.

### Q17 ⭐⭐ 🟢 Difference between COALESCE, IFNULL, ISNULL and NVL?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Dialect knowledge of NULL-replacement functions.
**Say this in the interview:** COALESCE is the standard one and takes any number of arguments. IFNULL is MySQL/SQLite, ISNULL is SQL Server, NVL is Oracle; all of those take exactly two.
**Explain simply:**
- **COALESCE(a,b,c,...)**: ANSI standard, many arguments, works everywhere.
- **IFNULL(a,b)**: MySQL and SQLite, two arguments.
- **ISNULL(a,b)**: SQL Server, two arguments, result takes the data type of the first argument (can truncate text). In MySQL `ISNULL(x)` is a different thing: it returns 1 or 0.
- **NVL(a,b)**: Oracle, two arguments.
**Example:** Use `COALESCE(bonus, allowance, 0)` to pay the bonus if present, else allowance, else 0.
**Sample data:**

`employees`

| emp_id | first_name | last_name | gender | dept | salary | joining_date |
|---|---|---|---|---|---|---|
| 1 | Asha | Rao | F | HR | 52000 | 2019-03-15 |
| 2 | Ravi | Kumar | M | IT | 78000 | 2021-07-01 |
| 3 | Meera | Nair | F | HR | NULL | 2023-01-10 |
| 4 | Arjun | Singh | M | Sales | 45000 | 2018-11-20 |
| 5 | Neha | Gupta | F | IT | 91000 | 2020-02-05 |
| 6 | Karan | Shah | M | Sales | NULL | 2022-09-12 |
| 7 | Anil | Verma | M | Finance | 30000 | 2024-05-30 |
| 8 | Sana | Khan | F | Finance | 65000 | 2017-08-08 |
**SQL:**
```sql
-- SQLite (run here); standard SQL unless noted
SELECT emp_id, salary,
       COALESCE(salary, 0)      AS coalesce_v,
       IFNULL(salary, 0)        AS ifnull_v,
       COALESCE(NULL, NULL, 5)  AS first_non_null
FROM employees
WHERE emp_id IN (1, 3, 6);

-- Not run here (from memory):
-- SQL Server: ISNULL(salary, 0)        -- 2 args; type of first argument wins
-- Oracle:     NVL(salary, 0)
-- PostgreSQL: only COALESCE (no IFNULL/ISNULL/NVL)
```
**Output:**

| emp_id | salary | coalesce_v | ifnull_v | first_non_null |
|---|---|---|---|---|
| 1 | 52000 | 52000 | 52000 | 5 |
| 3 | NULL | 0 | 0 | 5 |
| 6 | NULL | 0 | 0 | 5 |
**pandas equivalent:**
```python
res = employees.loc[employees['emp_id'].isin([1, 3, 6]), ['emp_id', 'salary']].copy()
res['coalesce_v'] = res['salary'].fillna(0)
res['ifnull_v'] = res['salary'].fillna(0)
res['first_non_null'] = 5
```
Result matches the SQL output.
**Edge cases:** With ISNULL, `ISNULL(varchar5_col, 'a long text')` is cut to 5 characters; COALESCE picks the higher-precedence type. Prefer COALESCE for portable code.
**Likely follow-ups:**
1. *Which is faster?* Differences are negligible; choose for portability.
2. *Does MySQL have ISNULL?* Yes, but it tests for NULL and returns 0/1.
**Common mistakes:** Using ISNULL in MySQL as a replacement function; using NVL outside Oracle.

### Q18 ⭐⭐ 🟢 How do you use IIF or IF in place of CASE WHEN?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Know the shorthand and its limits.
**Say this in the interview:** IIF(cond, a, b) in SQL Server (and SQLite 3.32+) and IF(cond, a, b) in MySQL are shortcuts for a two-way CASE. PostgreSQL has neither; I use CASE, which works everywhere.
**Explain simply:**
- IIF / IF handle a single condition: true result, false result.
- For more than two outcomes, nest them or just use CASE.
- IIF is a shortcut in SQL Server 2012+; internally it is converted to CASE.
- A NULL condition counts as false, so it falls to the else value.
**Example:** Label employees 'High' if salary is 60,000 or more, else 'Other'. Meera (NULL) lands in 'Other', which may hide missing data.
**Sample data:**

`employees`

| emp_id | first_name | last_name | gender | dept | salary | joining_date |
|---|---|---|---|---|---|---|
| 1 | Asha | Rao | F | HR | 52000 | 2019-03-15 |
| 2 | Ravi | Kumar | M | IT | 78000 | 2021-07-01 |
| 3 | Meera | Nair | F | HR | NULL | 2023-01-10 |
| 4 | Arjun | Singh | M | Sales | 45000 | 2018-11-20 |
| 5 | Neha | Gupta | F | IT | 91000 | 2020-02-05 |
| 6 | Karan | Shah | M | Sales | NULL | 2022-09-12 |
| 7 | Anil | Verma | M | Finance | 30000 | 2024-05-30 |
| 8 | Sana | Khan | F | Finance | 65000 | 2017-08-08 |
**SQL:**
```sql
-- SQLite (run here); standard SQL unless noted
SELECT first_name, salary,
       IIF(salary >= 60000, 'High', 'Other') AS grade,
       CASE WHEN salary >= 60000 THEN 'High' ELSE 'Other' END AS grade_case
FROM employees
ORDER BY emp_id;

-- Not run here:
-- MySQL:      IF(salary >= 60000, 'High', 'Other')
-- SQL Server: IIF(salary >= 60000, 'High', 'Other')
-- PostgreSQL: use CASE (no IF/IIF in SELECT)
```
**Output:**

| first_name | salary | grade | grade_case |
|---|---|---|---|
| Asha | 52000 | Other | Other |
| Ravi | 78000 | High | High |
| Meera | NULL | Other | Other |
| Arjun | 45000 | Other | Other |
| Neha | 91000 | High | High |
| Karan | NULL | Other | Other |
| Anil | 30000 | Other | Other |
| Sana | 65000 | High | High |
**pandas equivalent:**
```python
res = employees[['first_name', 'salary']].copy()
res['grade'] = np.where(res['salary'] >= 60000, 'High', 'Other')
res['grade_case'] = res['grade']
```
Result matches the SQL output.
**Edge cases:** NULL condition = else branch. MySQL `IF()` function is not the same as the `IF` statement in stored procedures.
**Likely follow-ups:**
1. *Why prefer CASE in interviews?* Portable and extensible beyond two branches.
2. *Can IIF nest?* Yes, up to 10 levels in SQL Server, but it gets unreadable.
**Common mistakes:** Using IF/IIF in PostgreSQL; forgetting the NULL case.

### Q19 ⭐⭐ 🟢 How do you use UPPER, LOWER and TRIM to clean text before comparing it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Basic text cleaning before matching or joining.
**Say this in the interview:** I normalise with `LOWER(TRIM(col))` on both sides, so 'Hyderabad ' and 'hyderabad' match. Cleaning first avoids missed matches and duplicate groups.
**Explain simply:**
- `UPPER` / `LOWER` change letter case; `TRIM` removes leading and trailing spaces.
- Many databases (MySQL, SQL Server default) are already case-insensitive, but PostgreSQL and SQLite compare case-sensitively, so you cannot rely on it.
- Apply the same cleaning to both sides of a comparison.
- Functions on a column stop an index from being used, so clean the data once or store a cleaned column for big tables.
**Example:** A city column has ' Hyderabad', 'HYDERABAD ', 'hyderabad', 'Pune', ' pune'. Cleaned, it has just two cities: hyderabad (3) and pune (2).
**Sample data:**

`candidates`

| id | city |
|---|---|
| 1 |  Hyderabad |
| 2 | HYDERABAD  |
| 3 | hyderabad |
| 4 | Pune |
| 5 |  pune |
**SQL:**
```sql
-- SQLite (run here); standard SQL unless noted
SELECT id, city, '[' || LOWER(TRIM(city)) || ']' AS cleaned
FROM candidates
ORDER BY id;

SELECT LOWER(TRIM(city)) AS city_clean, COUNT(*) AS n
FROM candidates
GROUP BY LOWER(TRIM(city))
ORDER BY city_clean;

-- Works in MySQL / PostgreSQL / SQL Server (TRIM exists in SQL Server 2017+; before that use LTRIM(RTRIM(col))).
-- PostgreSQL/SQL Server: output of group query is the same.
```
**Output:**

Query 1:

| id | city | cleaned |
|---|---|---|
| 1 |  Hyderabad | [hyderabad] |
| 2 | HYDERABAD  | [hyderabad] |
| 3 | hyderabad | [hyderabad] |
| 4 | Pune | [pune] |
| 5 |  pune | [pune] |

Query 2:

| city_clean | n |
|---|---|
| hyderabad | 3 |
| pune | 2 |
**pandas equivalent:**
```python
res = candidates[['id', 'city']].copy()
res['cleaned'] = '[' + candidates['city'].str.strip().str.lower() + ']'
```
Result matches the SQL output.
**Edge cases:** TRIM removes only normal spaces by default; tabs, non-breaking spaces (char 160) and line breaks need REPLACE or a character list. NULL stays NULL.
**Likely follow-ups:**
1. *Case-insensitive search?* Q32.
2. *Why not fix at insert time?* Yes, validate and clean on load; queries should not carry this burden.
**Common mistakes:** Cleaning only one side of the comparison; forgetting hidden characters.

### Q20 ⭐⭐ 🟢 How do you find the length of a string and filter names longer than 10 characters?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** String length functions and the dialect/trailing-space traps.
**Say this in the interview:** `LENGTH(name)` (or `LEN` in SQL Server, `CHAR_LENGTH` in MySQL for characters) gives the character count; filter with `WHERE LENGTH(name) > 10`.
**Explain simply:**
- PostgreSQL: `LENGTH` or `CHAR_LENGTH`. MySQL: `CHAR_LENGTH` counts characters, `LENGTH` counts **bytes** (matters for non-English names).
- SQL Server: `LEN` ignores trailing spaces; `DATALENGTH` returns bytes.
- NULL names give NULL length, so they never pass the filter.
- Test data below includes 'Ravi Kumar' followed by two trailing spaces.
**Example:** Name length 10 ('Neha Gupta') is not > 10. 'Priyadarshini Menon' has 19 characters, so it passes.
**Sample data:**

`staff_names`

| id | name |
|---|---|
| 1 | Priyadarshini Menon |
| 2 | Ravi Kumar   |
| 3 | Asha Rao |
| 4 | Venkatasubramanian |
| 5 | Neha Gupta |
| 6 | NULL |
**SQL:**
```sql
-- SQLite (run here); standard SQL unless noted
SELECT id, name, LENGTH(name) AS name_len
FROM staff_names
WHERE LENGTH(name) > 10
ORDER BY id;

-- Not run here:
-- MySQL:      CHAR_LENGTH(name) > 10
-- SQL Server: LEN(name) > 10      -- 'Ravi Kumar  ' would be 10 here, so it would NOT pass
-- PostgreSQL: LENGTH(name) > 10
```
**Output:**

| id | name | name_len |
|---|---|---|
| 1 | Priyadarshini Menon | 19 |
| 2 | Ravi Kumar   | 12 |
| 4 | Venkatasubramanian | 18 |
**pandas equivalent:**
```python
res = staff_names.assign(name_len=staff_names['name'].str.len())
res = res.loc[res['name_len'] > 10, ['id', 'name', 'name_len']]
```
Result matches the SQL output.
**Edge cases:** Trailing spaces counted in SQLite/PostgreSQL/MySQL but not by SQL Server LEN (so results differ). Use `LENGTH(TRIM(name))` if you want clean lengths. NULL excluded.
**Likely follow-ups:**
1. *Longest name?* `ORDER BY LENGTH(name) DESC LIMIT 1` (TOP 1 in SQL Server).
2. *Bytes vs characters?* Use CHAR_LENGTH in MySQL.
**Common mistakes:** Using LENGTH in MySQL for multi-byte text; ignoring trailing spaces.

### Q21 ⭐⭐ 🟢 How do you extract the first 3 characters of a string with SUBSTRING / LEFT?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the basic string functions and the dialect differences (LEFT is not in SQLite or Oracle).
**Say this in the interview:** To take the first 3 characters I use SUBSTRING(text, 1, 3), which means start at position 1 and take 3 characters. MySQL, PostgreSQL and SQL Server also have LEFT(text, 3) as a shortcut.
**Explain simply:**
- A *string* is just text. SQL counts character positions starting at 1, not 0 (unlike Python).
- `SUBSTRING(text, start, length)`: start at `start`, take `length` characters. SQLite and Oracle spell it `SUBSTR`.
- `LEFT(text, n)` gives the first n characters; `RIGHT(text, n)` gives the last n.
- In SQLite the last 3 characters are `SUBSTR(text, -3)` (a negative start counts from the end).
**Example:** Employee names 'Aarav Sharma' -> 'Aar'. A real use: employee codes like 'HR-0012', where `LEFT(code, 2)` gives the department prefix 'HR'.
**Sample data:**

| emp_id | name |
|---|---|
| 1 | Aarav Sharma |
| 2 | Neha Iyer |
| 3 | Karan Menon |
| 4 | Anita Desai |
| 5 | Imran Khan |
| 6 | Priya Nair |
| 7 | Arun Pillai |
| 8 | Meera Joshi |

**SQL:**
```sql
-- table: emp(emp_id, name, email, phone, dept, salary, dob, hire_date, status)
SELECT name,
       SUBSTR(name, 1, 3) AS first3,
       SUBSTR(name, -3)   AS last3
FROM emp;
```
Other dialects (not run here / from memory):
```sql
-- MySQL / PostgreSQL / SQL Server
SELECT LEFT(name, 3), RIGHT(name, 3), SUBSTRING(name, 1, 3) FROM emp;
-- Oracle: SUBSTR(name, 1, 3)
```

**Output:**

| name | first3 | last3 |
|---|---|---|
| Aarav Sharma | Aar | rma |
| Neha Iyer | Neh | yer |
| Karan Menon | Kar | non |
| Anita Desai | Ani | sai |
| Imran Khan | Imr | han |
| Priya Nair | Pri | air |
| Arun Pillai | Aru | lai |
| Meera Joshi | Mee | shi |

**pandas equivalent:**
```python
emp = pd.DataFrame([['Aarav Sharma'], ['Neha Iyer'], ['Karan Menon'], ['Anita Desai'], ['Imran Khan'], ['Priya Nair'], ['Arun Pillai'], ['Meera Joshi']],
    columns=['name'])

res = pd.DataFrame({'name': emp['name'],
                    'first3': emp['name'].str[:3],
                    'last3': emp['name'].str[-3:]})
print(res)
```
**Edge cases:** NULL input gives NULL output. If the text is shorter than 3 characters you just get what exists (no error). Spaces count as characters.
**Likely follow-ups:**
- How do I get the part before a space? Combine SUBSTRING with INSTR/CHARINDEX/POSITION (see Q31).
- Is SUBSTRING 0-based? No, 1-based; starting at 0 behaves differently across databases, so avoid it (from memory).
**Common mistakes:** Starting at position 0 (Python habit), or using LEFT in SQLite/Oracle where it does not exist.

### Q22 ⭐⭐ 🟢 How do you use REPLACE to remove or change characters, such as hyphens in phone numbers?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you clean messy text (phone numbers, codes) and do you know REPLACE is case-sensitive and NULL-safe.
**Say this in the interview:** REPLACE(column, 'old', 'new') swaps every occurrence of the old text with the new text. To remove hyphens I replace them with an empty string.
**Explain simply:**
- `REPLACE(text, find, replacement)` swaps *every* match, not just the first one.
- Replacing with `''` (empty text) deletes the character.
- You can nest them: `REPLACE(REPLACE(phone,'-',''),' ','')` removes hyphens and spaces.
- It is a SELECT-time change; the stored data stays the same unless you run an UPDATE.
**Example:** HR gets phone numbers typed as '98765-43210'. Before checking duplicates across two systems we strip the hyphen to '9876543210'.
**Sample data:**

| emp_id | name | phone |
|---|---|---|
| 1 | Aarav Sharma | 98765-43210 |
| 2 | Neha Iyer | 91234-56789 |
| 3 | Karan Menon | 99887-76655 |
| 4 | Anita Desai | 90000-12345 |
| 5 | Imran Khan | NULL |
| 6 | Priya Nair | 98700-11122 |
| 7 | Arun Pillai | 97000-22233 |
| 8 | Meera Joshi | 96000-33344 |

**SQL:**
```sql
-- table: emp(emp_id, name, email, phone, dept, salary, dob, hire_date, status)
SELECT emp_id, phone,
       REPLACE(phone, '-', '')       AS phone_clean,
       REPLACE(phone, '-', ' ')      AS phone_spaced
FROM emp;
```

**Output:**

| emp_id | phone | phone_clean | phone_spaced |
|---|---|---|---|
| 1 | 98765-43210 | 9876543210 | 98765 43210 |
| 2 | 91234-56789 | 9123456789 | 91234 56789 |
| 3 | 99887-76655 | 9988776655 | 99887 76655 |
| 4 | 90000-12345 | 9000012345 | 90000 12345 |
| 5 | NULL | NULL | NULL |
| 6 | 98700-11122 | 9870011122 | 98700 11122 |
| 7 | 97000-22233 | 9700022233 | 97000 22233 |
| 8 | 96000-33344 | 9600033344 | 96000 33344 |

**pandas equivalent:**
```python
emp = pd.DataFrame([[1, '98765-43210'], [2, '91234-56789'], [3, '99887-76655'], [4, '90000-12345'], [5, None], [6, '98700-11122'], [7, '97000-22233'], [8, '96000-33344']],
    columns=['emp_id', 'phone'])

res = pd.DataFrame({'emp_id': emp['emp_id'], 'phone': emp['phone'],
                    'phone_clean': emp['phone'].str.replace('-', '', regex=False),
                    'phone_spaced': emp['phone'].str.replace('-', ' ', regex=False)})
print(res)
```
**Edge cases:** NULL phone stays NULL (emp 5). REPLACE is case-sensitive in most dialects (SQL Server follows the column collation, so it may be case-insensitive). If the find text is empty, most databases return the text unchanged.
**Likely follow-ups:**
- REPLACE vs TRANSLATE? TRANSLATE (PostgreSQL, Oracle, SQL Server 2017+) swaps single characters one-for-one in a single call; REPLACE swaps whole substrings.
- How do I remove all non-digits? PostgreSQL: `REGEXP_REPLACE(phone,'[^0-9]','','g')`; MySQL 8: `REGEXP_REPLACE(phone,'[^0-9]','')` (from memory, not run here).
**Common mistakes:** Expecting REPLACE to change the table. It only changes the query output; you need UPDATE to change stored data. Also forgetting that NULL stays NULL.

### Q23 ⭐⭐ 🟢 How do you use LIKE with % and _ wildcards to search text patterns?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you search text patterns; do you know % means any number of characters and _ exactly one.
**Say this in the interview:** LIKE does pattern matching. The percent sign % stands for any number of characters, including none, and the underscore _ stands for exactly one character.
**Explain simply:**
- `'A%'` starts with A. `'%n'` ends with n. `'%an%'` contains 'an' anywhere.
- `'_r%'` means any one character, then 'r', then anything: so names whose second letter is r.
- `NOT LIKE` finds the opposite. To search for a real % or _ use `ESCAPE` (`LIKE '50\%' ESCAPE '\'`).
- A pattern starting with % cannot use a normal index, so it can be slow on big tables.
**Example:** Finding every employee with a Gmail address: `email LIKE '%@gmail.com'`. Finding codes like 'HR-001' to 'HR-099': `code LIKE 'HR-0__'`.
**Sample data:**

| name | email |
|---|---|
| Aarav Sharma | aarav.sharma@acme.com |
| Neha Iyer | neha.iyer@gmail.com |
| Karan Menon | karan.menon@acme.com |
| Anita Desai | anita.desai@outlook.com |
| Imran Khan | imran.khan@acme.com |
| Priya Nair | priya.nair@gmail.com |
| Arun Pillai | arun.pillai@gmail.com |
| Meera Joshi | NULL |

**SQL:**
```sql
-- table: emp(emp_id, name, email, phone, dept, salary, dob, hire_date, status)
SELECT name,
       name LIKE 'A%'   AS starts_with_A,
       name LIKE '%an%' AS contains_an,
       name LIKE '_r%'  AS second_letter_r,
       email LIKE '%@gmail.com' AS gmail
FROM emp;
```

**Output:**

| name | starts_with_A | contains_an | second_letter_r | gmail |
|---|---|---|---|---|
| Aarav Sharma | 1 | 0 | 0 | 0 |
| Neha Iyer | 0 | 0 | 0 | 1 |
| Karan Menon | 0 | 1 | 0 | 0 |
| Anita Desai | 1 | 1 | 0 | 0 |
| Imran Khan | 0 | 1 | 0 | 0 |
| Priya Nair | 0 | 0 | 1 | 1 |
| Arun Pillai | 1 | 0 | 1 | 1 |
| Meera Joshi | 0 | 0 | 0 | NULL |

**pandas equivalent:**
```python
emp = pd.DataFrame([['Aarav Sharma', 'aarav.sharma@acme.com'], ['Neha Iyer', 'neha.iyer@gmail.com'], ['Karan Menon', 'karan.menon@acme.com'], ['Anita Desai', 'anita.desai@outlook.com'], ['Imran Khan', 'imran.khan@acme.com'], ['Priya Nair', 'priya.nair@gmail.com'], ['Arun Pillai', 'arun.pillai@gmail.com'], ['Meera Joshi', None]],
    columns=['name', 'email'])

res = pd.DataFrame({'name': emp['name'],
  'starts_with_A': emp['name'].str.startswith('A').astype(int),
  'contains_an': emp['name'].str.contains('an', case=False, regex=False).astype(int),
  'second_letter_r': emp['name'].str.match('^.r', case=False).astype(int),
  'gmail': emp['email'].str.endswith('@gmail.com').map({True: 1, False: 0})})
print(res)
```
**Edge cases:** In SQLite and MySQL LIKE ignores case by default (for ASCII); in PostgreSQL it is case-sensitive (use ILIKE). A NULL email gives NULL (not 0), so a WHERE filter drops the row (emp 8 above shows NULL). Trailing spaces can break exact patterns.
**Likely follow-ups:**
- LIKE vs equals? `=` needs the full exact value; LIKE allows wildcards.
- LIKE vs regex? Regex (REGEXP, ~ in PostgreSQL, RLIKE in MySQL) is more powerful but dialect-specific.
**Common mistakes:** Writing `LIKE 'A'` and expecting a prefix match (without %). Forgetting `_` is a wildcard when searching for a literal underscore. Putting % at the start on huge tables and wondering why it is slow.

### Q24 ⭐⭐ 🟢 Which employees have names starting with 'A' or ending with 'n'? Show LIKE patterns.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you combine two LIKE patterns with OR and read the pattern direction right (start vs end).
**Say this in the interview:** I use WHERE name LIKE 'A%' OR name LIKE '%n'. The first catches names that start with A, the second names that end with n.
**Explain simply:**
- Each LIKE is a separate condition, so they are joined with OR (either is enough). AND would need both.
- Here `name` is the full name, so 'ends with n' looks at the surname (Khan, Menon).
- To check the first name only, split the name first (Q31).
- SQL Server and MySQL ignore case by default; PostgreSQL needs ILIKE for case-insensitive matching.
**Example:** Hiring wants a quick list of employees whose names begin with A or end with n for a name-badge printing batch.
**Sample data:**

| emp_id | name |
|---|---|
| 1 | Aarav Sharma |
| 2 | Neha Iyer |
| 3 | Karan Menon |
| 4 | Anita Desai |
| 5 | Imran Khan |
| 6 | Priya Nair |
| 7 | Arun Pillai |
| 8 | Meera Joshi |

**SQL:**
```sql
-- table: emp(emp_id, name, email, phone, dept, salary, dob, hire_date, status)
SELECT emp_id, name
FROM emp
WHERE name LIKE 'A%' OR name LIKE '%n'
ORDER BY emp_id;
```

**Output:**

| emp_id | name |
|---|---|
| 1 | Aarav Sharma |
| 3 | Karan Menon |
| 4 | Anita Desai |
| 5 | Imran Khan |
| 7 | Arun Pillai |

**pandas equivalent:**
```python
emp = pd.DataFrame([[1, 'Aarav Sharma'], [2, 'Neha Iyer'], [3, 'Karan Menon'], [4, 'Anita Desai'], [5, 'Imran Khan'], [6, 'Priya Nair'], [7, 'Arun Pillai'], [8, 'Meera Joshi']],
    columns=['emp_id', 'name'])

res = emp[emp['name'].str.startswith('A') | emp['name'].str.endswith('n')][['emp_id','name']].sort_values('emp_id')
print(res)
```
**Edge cases:** Names with a trailing space would fail the `%n` test (TRIM first). Lowercase 'a%' matches in SQLite/MySQL/SQL Server but not in PostgreSQL. A NULL name matches neither pattern and is excluded. Someone matching both rules appears once, not twice.
**Likely follow-ups:**
- Starting with A AND ending with n? Change OR to AND.
- Case-insensitive in PostgreSQL? `name ILIKE 'a%' OR name ILIKE '%n'` (not run here).
**Common mistakes:** Using AND instead of OR, mixing up 'A%' and '%A', and forgetting parentheses when adding another condition such as `AND dept = 'IT'` (AND binds tighter than OR).

### Q25 ⭐⭐ 🟢 How do you add or subtract days, months or years from a date (DATE_ADD, DATEADD, INTERVAL)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know date arithmetic differs a lot between databases, and that month-ends are a trap.
**Say this in the interview:** In MySQL I use DATE_ADD(date, INTERVAL 90 DAY), in PostgreSQL date + INTERVAL '90 days', in SQL Server DATEADD(day, 90, date). To subtract I use a negative number or DATE_SUB.
**Explain simply:**
- An *interval* is a length of time like 90 days or 6 months that you add to a date.
- Adding days is simple. Adding months/years is trickier because months have different lengths.
- I ran SQLite below: `date(d, '+90 days')`, `'+6 months'`, `'-1 year'` modifiers.
- To get the *difference* between two dates use DATEDIFF (MySQL/SQL Server), subtraction (PostgreSQL), or julianday (SQLite).
**Example:** Probation ends 6 months after hire date: hire 2021-03-15 gives 2021-09-15. A 90-day notice from 2021-03-15 ends 2021-06-13.
**Sample data:**

| emp_id | name | hire_date |
|---|---|---|
| 1 | Aarav Sharma | 2021-03-15 |
| 2 | Neha Iyer | 2018-07-01 |
| 3 | Karan Menon | 2022-11-10 |
| 4 | Anita Desai | 2019-05-20 |
| 5 | Imran Khan | 2023-01-09 |

**SQL:**
```sql
-- table: emp(emp_id, name, email, phone, dept, salary, dob, hire_date, status)
SELECT emp_id, hire_date,
       date(hire_date, '+90 days')  AS notice_end,
       date(hire_date, '+6 months') AS probation_end,
       date(hire_date, '-1 year')   AS one_year_before
FROM emp
WHERE emp_id <= 5;
```
Other dialects (not run here / from memory):
```sql
-- MySQL
SELECT DATE_ADD(hire_date, INTERVAL 90 DAY), DATE_ADD(hire_date, INTERVAL 6 MONTH), DATE_SUB(hire_date, INTERVAL 1 YEAR) FROM emp;
-- PostgreSQL
SELECT hire_date + INTERVAL '90 days', hire_date + INTERVAL '6 months', hire_date - INTERVAL '1 year' FROM emp;
-- SQL Server
SELECT DATEADD(day, 90, hire_date), DATEADD(month, 6, hire_date), DATEADD(year, -1, hire_date) FROM emp;
```

**Output:**

| emp_id | hire_date | notice_end | probation_end | one_year_before |
|---|---|---|---|---|
| 1 | 2021-03-15 | 2021-06-13 | 2021-09-15 | 2020-03-15 |
| 2 | 2018-07-01 | 2018-09-29 | 2019-01-01 | 2017-07-01 |
| 3 | 2022-11-10 | 2023-02-08 | 2023-05-10 | 2021-11-10 |
| 4 | 2019-05-20 | 2019-08-18 | 2019-11-20 | 2018-05-20 |
| 5 | 2023-01-09 | 2023-04-09 | 2023-07-09 | 2022-01-09 |

**pandas equivalent:**
```python
emp = pd.DataFrame([[1, '2021-03-15'], [2, '2018-07-01'], [3, '2022-11-10'], [4, '2019-05-20'], [5, '2023-01-09'], [6, '2016-09-12'], [7, '2024-02-01'], [8, '2020-10-05']],
    columns=['emp_id', 'hire_date'])

emp['hire_date'] = pd.to_datetime(emp['hire_date'])
res = pd.DataFrame({'emp_id': emp['emp_id'],
    'hire_date': emp['hire_date'].dt.strftime('%Y-%m-%d'),
    'notice_end': (emp['hire_date'] + pd.Timedelta(days=90)).dt.strftime('%Y-%m-%d'),
    'probation_end': (emp['hire_date'] + pd.DateOffset(months=6)).dt.strftime('%Y-%m-%d'),
    'one_year_before': (emp['hire_date'] - pd.DateOffset(years=1)).dt.strftime('%Y-%m-%d')})
res = res[res['emp_id'] <= 5]
print(res)
```
**Edge cases:** Month-end: in SQLite `date('2025-01-31','+1 month')` returned 2025-03-03 (it overflows into March, verified here). MySQL and PostgreSQL clamp to the last valid day, 2025-02-28 (from memory, not run here). SQLite gave 2025-03-01 for Feb 29 2024 plus 1 year. NULL date gives NULL.
**Likely follow-ups:**
- How many days between two dates? MySQL `DATEDIFF(end, start)`; SQL Server `DATEDIFF(day, start, end)` (argument order differs!); PostgreSQL `end - start`.
- Add business days only? No built-in; use a calendar table.
**Common mistakes:** Mixing up argument order of DATEDIFF between MySQL and SQL Server, and assuming month arithmetic behaves the same everywhere.

### Q26 ⭐⭐ 🟢 How do you extract day, month, year, weekday using EXTRACT, DATEPART or DAY/MONTH/YEAR?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you pull parts out of a date and do you know weekday numbering differs by dialect.
**Say this in the interview:** EXTRACT(YEAR FROM date) is the standard way, in PostgreSQL and MySQL. SQL Server uses DATEPART or the YEAR(), MONTH(), DAY() functions. SQLite uses strftime.
**Explain simply:**
- Pulling out the year, month or day lets you group hires by year or find a particular month.
- Standard / PostgreSQL / MySQL: `EXTRACT(MONTH FROM d)`. SQL Server: `DATEPART(month, d)` or `MONTH(d)`.
- Weekday numbers vary: SQLite `%w` has Sunday = 0; MySQL `DAYOFWEEK` has Sunday = 1; PostgreSQL `EXTRACT(DOW ...)` has Sunday = 0; SQL Server depends on `SET DATEFIRST` (last three from memory).
- In SQLite strftime returns text, so wrap in CAST(... AS INTEGER).
**Example:** Hire date 2021-03-15: year 2021, month 3, day 15, it was a Monday.
**Sample data:**

| emp_id | name | hire_date |
|---|---|---|
| 1 | Aarav Sharma | 2021-03-15 |
| 2 | Neha Iyer | 2018-07-01 |
| 3 | Karan Menon | 2022-11-10 |
| 4 | Anita Desai | 2019-05-20 |
| 5 | Imran Khan | 2023-01-09 |

**SQL:**
```sql
-- table: emp(emp_id, name, email, phone, dept, salary, dob, hire_date, status)
SELECT emp_id, hire_date,
       CAST(strftime('%Y', hire_date) AS INTEGER) AS yr,
       CAST(strftime('%m', hire_date) AS INTEGER) AS mth,
       CAST(strftime('%d', hire_date) AS INTEGER) AS dy,
       CAST(strftime('%w', hire_date) AS INTEGER) AS weekday_sun0
FROM emp
WHERE emp_id <= 5;
```
Other dialects (not run here / from memory):
```sql
-- PostgreSQL / MySQL
SELECT EXTRACT(YEAR FROM hire_date), EXTRACT(MONTH FROM hire_date), EXTRACT(DAY FROM hire_date) FROM emp;
-- SQL Server
SELECT YEAR(hire_date), MONTH(hire_date), DAY(hire_date), DATEPART(weekday, hire_date) FROM emp;
```

**Output:**

| emp_id | hire_date | yr | mth | dy | weekday_sun0 |
|---|---|---|---|---|---|
| 1 | 2021-03-15 | 2021 | 3 | 15 | 1 |
| 2 | 2018-07-01 | 2018 | 7 | 1 | 0 |
| 3 | 2022-11-10 | 2022 | 11 | 10 | 4 |
| 4 | 2019-05-20 | 2019 | 5 | 20 | 1 |
| 5 | 2023-01-09 | 2023 | 1 | 9 | 1 |

**pandas equivalent:**
```python
emp = pd.DataFrame([[1, '2021-03-15'], [2, '2018-07-01'], [3, '2022-11-10'], [4, '2019-05-20'], [5, '2023-01-09'], [6, '2016-09-12'], [7, '2024-02-01'], [8, '2020-10-05']],
    columns=['emp_id', 'hire_date'])

emp['hd'] = pd.to_datetime(emp['hire_date'])
res = pd.DataFrame({'emp_id': emp['emp_id'], 'hire_date': emp['hire_date'],
    'yr': emp['hd'].dt.year, 'mth': emp['hd'].dt.month, 'dy': emp['hd'].dt.day,
    'weekday_sun0': (emp['hd'].dt.dayofweek + 1) % 7})
res = res[res['emp_id'] <= 5]
print(res)
```
**Edge cases:** NULL date gives NULL. In pandas `dayofweek` has Monday = 0, so I shifted it to match SQLite. Always check the weekday convention before reporting 'weekend' numbers.
**Likely follow-ups:**
- Weekday name? MySQL `DAYNAME(d)`, SQL Server `DATENAME(weekday, d)`, PostgreSQL `TO_CHAR(d,'Day')` (not run here).
- Quarter? `EXTRACT(QUARTER FROM d)` or `DATEPART(quarter, d)`.
**Common mistakes:** Assuming Sunday or Monday is day 1 everywhere, and comparing strftime text ('03') to a number without CAST.

### Q27 ⭐⭐ 🟢 How do you change a date's display format (DATE_FORMAT, TO_CHAR, FORMAT)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know display formatting happens at output time and the format codes differ per dialect.
**Say this in the interview:** MySQL uses DATE_FORMAT(date, '%d-%m-%Y'), PostgreSQL uses TO_CHAR(date, 'DD-MM-YYYY'), and SQL Server uses FORMAT(date, 'dd-MM-yyyy') or CONVERT with a style number.
**Explain simply:**
- Formatting turns a date into *text* for display. Do it last, because text dates in dd-mm-yyyy form sort by day first ('15-03-2021' lands before '20-01-2019'), which is not real date order.
- MySQL and SQLite: `%d` day, `%m` month, `%Y` four-digit year.
- PostgreSQL / Oracle: `DD`, `MM`, `YYYY`. SQL Server FORMAT: `dd`, `MM` (capital M for month; small mm is minutes).
- Ran here with SQLite strftime.
**Example:** A payroll report that must show 15/03/2021 instead of 2021-03-15.
**Sample data:**

| emp_id | name | hire_date |
|---|---|---|
| 1 | Aarav Sharma | 2021-03-15 |
| 2 | Neha Iyer | 2018-07-01 |
| 3 | Karan Menon | 2022-11-10 |
| 4 | Anita Desai | 2019-05-20 |
| 5 | Imran Khan | 2023-01-09 |

**SQL:**
```sql
-- table: emp(emp_id, name, email, phone, dept, salary, dob, hire_date, status)
SELECT emp_id, hire_date,
       strftime('%d/%m/%Y', hire_date) AS uk_style,
       strftime('%Y-%m', hire_date)    AS year_month
FROM emp
WHERE emp_id <= 5;
```
Other dialects (not run here / from memory):
```sql
-- MySQL
SELECT DATE_FORMAT(hire_date, '%d/%m/%Y') FROM emp;
-- PostgreSQL / Oracle
SELECT TO_CHAR(hire_date, 'DD/MM/YYYY') FROM emp;
-- SQL Server
SELECT FORMAT(hire_date, 'dd/MM/yyyy'), CONVERT(varchar(10), hire_date, 103) FROM emp;
```

**Output:**

| emp_id | hire_date | uk_style | year_month |
|---|---|---|---|
| 1 | 2021-03-15 | 15/03/2021 | 2021-03 |
| 2 | 2018-07-01 | 01/07/2018 | 2018-07 |
| 3 | 2022-11-10 | 10/11/2022 | 2022-11 |
| 4 | 2019-05-20 | 20/05/2019 | 2019-05 |
| 5 | 2023-01-09 | 09/01/2023 | 2023-01 |

**pandas equivalent:**
```python
emp = pd.DataFrame([[1, '2021-03-15'], [2, '2018-07-01'], [3, '2022-11-10'], [4, '2019-05-20'], [5, '2023-01-09'], [6, '2016-09-12'], [7, '2024-02-01'], [8, '2020-10-05']],
    columns=['emp_id', 'hire_date'])

emp['hd'] = pd.to_datetime(emp['hire_date'])
res = pd.DataFrame({'emp_id': emp['emp_id'], 'hire_date': emp['hire_date'],
    'uk_style': emp['hd'].dt.strftime('%d/%m/%Y'),
    'year_month': emp['hd'].dt.strftime('%Y-%m')})
res = res[res['emp_id'] <= 5]
print(res)
```
**Edge cases:** NULL date gives NULL. The result is text, not a date. SQL Server FORMAT can be slow on big tables (CONVERT with style 103 gives dd/mm/yyyy - from memory). `YYYY-MM` text sorts correctly, which is handy for monthly grouping.
**Likely follow-ups:**
- Format vs convert? CAST/CONVERT change the data type; formatting changes the look.
- Month name? MySQL `%M`/`%b`, PostgreSQL `TO_CHAR(d,'Mon')` (not run here).
**Common mistakes:** Formatting a date early then sorting or comparing the text. Using `mm` for month in SQL Server FORMAT, or confusing MySQL `%i` (minutes) with month.

### Q28 ⭐⭐ 🟢 What is CAST and CONVERT? Convert text to number and number to text.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know how to change data types and that failed conversions behave differently per database.
**Say this in the interview:** CAST(value AS type) is the standard way to change a data type, for example CAST('52000' AS INTEGER). CONVERT does the same in MySQL and SQL Server, with SQL Server adding style codes for dates.
**Explain simply:**
- *Data type* means what kind of value a column holds: number, text, date.
- Text to number: `CAST(salary_text AS REAL)`. Number to text: `CAST(salary AS TEXT)` (use VARCHAR in MySQL/SQL Server/PostgreSQL).
- SQL Server: `CONVERT(INT, x)` (type first). MySQL: `CONVERT(x, SIGNED)`. PostgreSQL also has `x::int`.
- Bad text such as 'abc': SQLite quietly returns 0 (verified); PostgreSQL and SQL Server raise an error; SQL Server has TRY_CAST; MySQL gives 0 with a warning (from memory).
**Example:** A salary column imported from Excel as text '61000.50' cannot be summed until you CAST it to a number.
**Sample data:**

| emp_id | salary_text |
|---|---|
| 1 | 52000 |
| 2 | 61000.50 |
| 3 |  87000  |
| 4 | NULL |

**SQL:**
```sql
-- table: raw_pay(emp_id INT, salary_text TEXT)
SELECT emp_id, salary_text,
       CAST(salary_text AS REAL)                      AS salary_num,
       ROUND(CAST(salary_text AS REAL) * 1.10, 2)     AS with_10pct_raise,
       CAST(CAST(salary_text AS INTEGER) AS TEXT) || ' INR' AS back_to_text
FROM raw_pay;
```

**Output:**

| emp_id | salary_text | salary_num | with_10pct_raise | back_to_text |
|---|---|---|---|---|
| 1 | 52000 | 52000.0 | 57200.0 | 52000 INR |
| 2 | 61000.50 | 61000.5 | 67100.55 | 61000 INR |
| 3 |  87000  | 87000.0 | 95700.0 | 87000 INR |
| 4 | NULL | NULL | NULL | NULL |

**pandas equivalent:**
```python
raw_pay = pd.DataFrame([[1, '52000'], [2, '61000.50'], [3, ' 87000 '], [4, None]],
    columns=['emp_id', 'salary_text'])

raw_pay['salary_num'] = pd.to_numeric(raw_pay['salary_text'])
res = pd.DataFrame({'emp_id': raw_pay['emp_id'], 'salary_text': raw_pay['salary_text'],
    'salary_num': raw_pay['salary_num'],
    'with_10pct_raise': (raw_pay['salary_num'] * 1.10).round(2),
    'back_to_text': raw_pay['salary_num'].apply(lambda v: None if pd.isna(v) else f'{int(v)} INR')})
print(res)
```
**Edge cases:** NULL stays NULL. SQLite accepted ' 87000 ' with spaces (other databases differ - not run here). Decimal text cast to INTEGER truncates (61000.50 became 61000). 'abc' casts to 0 in SQLite, which can silently corrupt totals.
**Likely follow-ups:**
- CAST vs CONVERT? CAST is standard SQL and works everywhere; CONVERT is vendor-specific.
- Safe conversion? SQL Server `TRY_CAST`/`TRY_CONVERT` return NULL on failure; PostgreSQL has no direct TRY_CAST (from memory).
**Common mistakes:** Not cleaning the text before casting, relying on silent 0s, and doing salary math on text.

### Q29 ⭐⭐ 🟢 How do you handle NULLs in CONCAT? How does it differ in MySQL vs PostgreSQL vs SQL Server?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know that one NULL can wipe out a whole concatenated string in some dialects and not in others.
**Say this in the interview:** With the || operator (PostgreSQL, SQLite, Oracle) one NULL makes the whole result NULL. CONCAT() in PostgreSQL and SQL Server 2012+ treats NULL as empty text. CONCAT_WS skips NULLs and avoids double spaces. MySQL's CONCAT is the odd one: it returns NULL.
**Explain simply:**
- *Concatenate* means joining pieces of text together.
- `first || ' ' || middle || ' ' || last` gives NULL if middle is NULL (verified in SQLite).
- `CONCAT(first,' ',middle,' ',last)` ignores NULL in SQLite (verified) but leaves a double space.
- `CONCAT_WS(' ', first, middle, last)` joins with a separator and skips NULLs: the cleanest.
- MySQL: CONCAT returns NULL if any argument is NULL (from memory, not run here). SQL Server: `+` gives NULL unless CONCAT_NULL_YIELDS_NULL is off; its CONCAT() ignores NULL.
**Example:** Full name column: 'Aarav Sharma' has no middle name, so an unprotected join returns NULL instead of the name.
**Sample data:**

| emp_id | first_name | middle_name | last_name |
|---|---|---|---|
| 1 | Aarav | NULL | Sharma |
| 2 | Neha | Rani | Iyer |
| 3 | Karan | NULL | Menon |

**SQL:**
```sql
-- table: person(emp_id INT, first_name TEXT, middle_name TEXT, last_name TEXT)
SELECT emp_id,
       first_name || ' ' || middle_name || ' ' || last_name AS with_pipes,
       CONCAT(first_name, ' ', middle_name, ' ', last_name)  AS with_concat,
       CONCAT_WS(' ', first_name, middle_name, last_name)    AS with_concat_ws,
       first_name || ' ' || COALESCE(middle_name || ' ', '') || last_name AS with_coalesce
FROM person;
```

**Output:**

| emp_id | with_pipes | with_concat | with_concat_ws | with_coalesce |
|---|---|---|---|---|
| 1 | NULL | Aarav  Sharma | Aarav Sharma | Aarav Sharma |
| 2 | Neha Rani Iyer | Neha Rani Iyer | Neha Rani Iyer | Neha Rani Iyer |
| 3 | NULL | Karan  Menon | Karan Menon | Karan Menon |

**pandas equivalent:**
```python
person = pd.DataFrame([[1, 'Aarav', None, 'Sharma'], [2, 'Neha', 'Rani', 'Iyer'], [3, 'Karan', None, 'Menon']],
    columns=['emp_id', 'first_name', 'middle_name', 'last_name'])

def join_ws(r):
    return ' '.join(x for x in [r.first_name, r.middle_name, r.last_name] if pd.notna(x))
res = pd.DataFrame({'emp_id': person['emp_id'],
    'with_pipes': [None if pd.isna(m) else f'{f} {m} {l}' for f, m, l in zip(person.first_name, person.middle_name, person.last_name)],
    'with_concat': [f'{f} {"" if pd.isna(m) else m} {l}' for f, m, l in zip(person.first_name, person.middle_name, person.last_name)],
    'with_concat_ws': person.apply(join_ws, axis=1),
    'with_coalesce': person.apply(join_ws, axis=1)})
print(res)
```
**Edge cases:** CONCAT_WS exists in SQLite 3.44+, MySQL, PostgreSQL, SQL Server 2017+. Numbers/dates inside || may need CAST. An empty string '' is not NULL (Oracle treats them the same, others do not).
**Likely follow-ups:**
- Why does + fail in MySQL? In MySQL `+` is arithmetic only; use CONCAT (from memory).
- How to avoid double spaces? Use CONCAT_WS or TRIM/REPLACE the result.
**Common mistakes:** Using || or + with nullable columns and getting NULL names in reports; or double spaces when CONCAT skips a middle name.

### Q30 ⭐⭐ 🟡 How do you extract the domain from an email address (the part after @)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you combine INSTR/POSITION with SUBSTRING and then group by the result.
**Say this in the interview:** I find the position of the @ sign, then take everything after it: SUBSTRING(email, position + 1). Then I can group by that domain to count employees per email provider.
**Explain simply:**
- The *domain* is the part after @, like gmail.com.
- Find the @: `INSTR(email,'@')` (SQLite, MySQL, Oracle), `POSITION('@' IN email)` (PostgreSQL/MySQL), `CHARINDEX('@', email)` (SQL Server).
- Then `SUBSTR(email, pos + 1)` takes the rest of the text.
- Group by the new column to count per domain.
**Example:** neha.iyer@gmail.com gives gmail.com. HR can then see how many staff use personal email accounts instead of company ones.
**Sample data:**

| emp_id | name | email |
|---|---|---|
| 1 | Aarav Sharma | aarav.sharma@acme.com |
| 2 | Neha Iyer | neha.iyer@gmail.com |
| 3 | Karan Menon | karan.menon@acme.com |
| 4 | Anita Desai | anita.desai@outlook.com |
| 5 | Imran Khan | imran.khan@acme.com |
| 6 | Priya Nair | priya.nair@gmail.com |
| 7 | Arun Pillai | arun.pillai@gmail.com |
| 8 | Meera Joshi | NULL |

**SQL:**
```sql
-- table: emp(emp_id, name, email, phone, dept, salary, dob, hire_date, status)
SELECT SUBSTR(email, INSTR(email, '@') + 1) AS domain,
       COUNT(*) AS headcount
FROM emp
GROUP BY SUBSTR(email, INSTR(email, '@') + 1)
ORDER BY headcount DESC, domain;
```
Other dialects (not run here / from memory):
```sql
-- SQL Server
SELECT SUBSTRING(email, CHARINDEX('@', email) + 1, LEN(email)) FROM emp;
-- PostgreSQL
SELECT SPLIT_PART(email, '@', 2) FROM emp;
-- MySQL
SELECT SUBSTRING_INDEX(email, '@', -1) FROM emp;
```

**Output:**

| domain | headcount |
|---|---|
| acme.com | 3 |
| gmail.com | 3 |
| NULL | 1 |
| outlook.com | 1 |

**pandas equivalent:**
```python
emp = pd.DataFrame([[1, 'aarav.sharma@acme.com'], [2, 'neha.iyer@gmail.com'], [3, 'karan.menon@acme.com'], [4, 'anita.desai@outlook.com'], [5, 'imran.khan@acme.com'], [6, 'priya.nair@gmail.com'], [7, 'arun.pillai@gmail.com'], [8, None]],
    columns=['emp_id', 'email'])

emp['domain'] = emp['email'].str.split('@').str[1]
res = (emp.groupby('domain', dropna=False).size().reset_index(name='headcount')
          .sort_values(['headcount', 'domain'], ascending=[False, True], na_position='first')
          .reset_index(drop=True))
print(res)
```
**Edge cases:** A NULL email gives a NULL domain, and GROUP BY shows it as its own row (headcount 1 above, emp 8). If there is no @ in the text, INSTR returns 0 so SUBSTR starts at 1 and returns the whole string (bad data looks like a domain!). Domain case: LOWER it before grouping.
**Likely follow-ups:**
- Get the username before @? `SUBSTR(email, 1, INSTR(email,'@') - 1)`.
- MySQL shortcut? `SUBSTRING_INDEX(email,'@',-1)`; PostgreSQL `SPLIT_PART(email,'@',2)` (not run here).
**Common mistakes:** Forgetting the +1 (the @ sign stays in the result) and not handling NULL or malformed emails.

### Q31 ⭐⭐ 🟡 How do you split a full name into first name and last name in SQL?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you split text at a delimiter, and do you think about names with one word or three words.
**Say this in the interview:** I find the first space with INSTR, take everything before it as the first name and everything after as the last name. I always guard against names with no space.
**Explain simply:**
- A *delimiter* is the separator character, here a space.
- First name = text before the first space: `SUBSTR(n, 1, INSTR(n,' ') - 1)`.
- Last name = text after it: `SUBSTR(n, INSTR(n,' ') + 1)`.
- A CASE expression handles one-word names like 'Madonna' (INSTR returns 0, which would break SUBSTR).
- Honest caveat: for 'Raj Kumar Singh' this gives 'Kumar Singh' as the rest, not just 'Singh'.
**Example:** 'Aarav Sharma' -> first 'Aarav', last 'Sharma'. Best practice: store first and last names in separate columns from the start.
**Sample data:**

| full_name |
|---|
| Aarav Sharma |
| Raj Kumar Singh |
| Madonna |
| Anita Desai |

**SQL:**
```sql
-- table: staff_names(full_name TEXT)
SELECT full_name,
       CASE WHEN INSTR(full_name, ' ') = 0 THEN full_name
            ELSE SUBSTR(full_name, 1, INSTR(full_name, ' ') - 1) END AS first_name,
       CASE WHEN INSTR(full_name, ' ') = 0 THEN NULL
            ELSE TRIM(SUBSTR(full_name, INSTR(full_name, ' ') + 1)) END AS rest_of_name
FROM staff_names;
```

**Output:**

| full_name | first_name | rest_of_name |
|---|---|---|
| Aarav Sharma | Aarav | Sharma |
| Raj Kumar Singh | Raj | Kumar Singh |
| Madonna | Madonna | NULL |
| Anita Desai | Anita | Desai |

**pandas equivalent:**
```python
staff_names = pd.DataFrame([['Aarav Sharma'], ['Raj Kumar Singh'], ['Madonna'], ['Anita Desai']],
    columns=['full_name'])

parts = staff_names['full_name'].str.split(' ', n=1, expand=True)
res = pd.DataFrame({'full_name': staff_names['full_name'],
                    'first_name': parts[0],
                    'rest_of_name': parts[1].str.strip()})
print(res)
```
**Edge cases:** One-word names (no space) and NULL names need handling. Leading spaces break the logic: TRIM first. Names with a middle name or surname prefixes ('Van der Berg') cannot be split reliably by a space; the real last word needs different tools.
**Likely follow-ups:**
- How to get the true last word? MySQL `SUBSTRING_INDEX(n,' ',-1)`; PostgreSQL `(string_to_array(n,' '))[array_length(string_to_array(n,' '),1)]`; SQL Server 2022 `STRING_SPLIT` with ordinal (all not run here).
- Is there a shortcut? PostgreSQL `SPLIT_PART(n,' ',1)` and `SPLIT_PART(n,' ',2)`.
**Common mistakes:** Not handling one-word names (SUBSTR with length -1 returns odd results) and assuming everyone has exactly two names.

### Q32 ⭐⭐ 🟡 How do you do case-insensitive search across MySQL, PostgreSQL (ILIKE) and SQL Server?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know that case sensitivity depends on the database and column collation, and how to write portable code.
**Say this in the interview:** The portable way is to LOWER both sides: WHERE LOWER(name) LIKE '%khan%'. PostgreSQL also has ILIKE for case-insensitive LIKE. MySQL and SQL Server are usually case-insensitive already.
**Explain simply:**
- *Collation* is the rule a database uses to compare text (does 'A' equal 'a'?).
- MySQL and SQL Server default collations are case-insensitive, so `LIKE '%khan%'` already matches 'Khan'.
- PostgreSQL is case-sensitive for `=` and LIKE; use `ILIKE` or `LOWER()`.
- SQLite: `=` is case-sensitive but LIKE is case-insensitive for plain English letters (verified below). Inconsistent, so LOWER both sides when in doubt.
- Downside of LOWER(): it can stop an index being used on that column.
**Example:** A recruiter types 'KHAN' in a search box; the candidate record is stored as 'Imran Khan'.
**Sample data:**

| emp_id | name |
|---|---|
| 1 | Aarav Sharma |
| 2 | Neha Iyer |
| 3 | Karan Menon |
| 4 | Anita Desai |
| 5 | Imran Khan |
| 6 | Priya Nair |
| 7 | Arun Pillai |
| 8 | Meera Joshi |

**SQL:**
```sql
-- table: emp(emp_id, name, email, phone, dept, salary, dob, hire_date, status)
SELECT name,
       name = 'imran khan'                 AS plain_equals,
       LOWER(name) = 'imran khan'          AS lower_equals,
       LOWER(name) LIKE '%khan%'           AS lower_like
FROM emp
WHERE LOWER(name) LIKE '%khan%';
```
Other dialects (not run here / from memory):
```sql
-- PostgreSQL
SELECT name FROM emp WHERE name ILIKE '%khan%';
-- MySQL / SQL Server (usually already case-insensitive)
SELECT name FROM emp WHERE name LIKE '%khan%';
```

**Output:**

| name | plain_equals | lower_equals | lower_like |
|---|---|---|---|
| Imran Khan | 0 | 1 | 1 |

**pandas equivalent:**
```python
emp = pd.DataFrame([['Aarav Sharma'], ['Neha Iyer'], ['Karan Menon'], ['Anita Desai'], ['Imran Khan'], ['Priya Nair'], ['Arun Pillai'], ['Meera Joshi']],
    columns=['name'])

mask = emp['name'].str.contains('khan', case=False, regex=False)
res = pd.DataFrame({'name': emp['name'][mask],
    'plain_equals': (emp['name'][mask] == 'imran khan').astype(int),
    'lower_equals': (emp['name'][mask].str.lower() == 'imran khan').astype(int),
    'lower_like': 1}).reset_index(drop=True)
print(res)
```
**Edge cases:** NULL names never match. Non-English characters (accents, Turkish i) may not lowercase the way you expect. SQL Server can force case-sensitive with `COLLATE Latin1_General_CS_AS`; MySQL with `LIKE BINARY` (from memory).
**Likely follow-ups:**
- ILIKE syntax? `WHERE name ILIKE '%khan%'` in PostgreSQL (not run here).
- Case-insensitive but index-friendly? PostgreSQL expression index on `LOWER(name)`, or the citext type (from memory).
**Common mistakes:** Assuming all databases behave like the one you practised on, and applying LOWER only to one side of the comparison.

### Q33 ⭐⭐ 🟡 What is DATE_TRUNC / how do you truncate dates to month or week in each dialect?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know how to group dates into month or week buckets and that week start day differs.
**Say this in the interview:** DATE_TRUNC('month', date) chops a date down to the first day of its month. PostgreSQL, DuckDB, Snowflake and BigQuery have it; MySQL and SQLite do not, so I use DATE_FORMAT or date modifiers instead.
**Explain simply:**
- *Truncate* here means rounding a date down: 2021-03-15 becomes 2021-03-01 for month.
- It is the standard trick to count hires per month: GROUP BY the truncated date.
- `DATE_TRUNC('week', d)` returns the Monday of that week in PostgreSQL/DuckDB (from memory for PostgreSQL). SQL Server's DATETRUNC week depends on DATEFIRST.
- The main query below ran in DuckDB (PostgreSQL-style syntax); the SQLite version is also run and matches.
**Example:** Hire 2021-03-15 (a Monday) -> month_start 2021-03-01, week_start 2021-03-15. Hire 2022-11-10 (Thursday) -> week starts Monday 2022-11-07.
**Sample data:**

| emp_id | name | hire_date |
|---|---|---|
| 1 | Aarav Sharma | 2021-03-15 |
| 2 | Neha Iyer | 2018-07-01 |
| 3 | Karan Menon | 2022-11-10 |
| 4 | Anita Desai | 2019-05-20 |
| 5 | Imran Khan | 2023-01-09 |

**SQL:**
```sql
-- table: emp(emp_id, name, hire_date)  -- DuckDB, hire_date is DATE
SELECT emp_id, hire_date,
       CAST(date_trunc('month', hire_date) AS DATE) AS month_start,
       CAST(date_trunc('week',  hire_date) AS DATE) AS week_start_monday
FROM emp
WHERE emp_id <= 5;
```
SQLite alternative (also run here, same result; SQLite has no DATE_TRUNC):
```sql
SELECT emp_id, hire_date,
       date(hire_date, 'start of month')            AS month_start,
       date(hire_date, 'weekday 0', '-6 days')      AS week_start_monday
FROM emp WHERE emp_id <= 5;
```
Other dialects (not run here / from memory):
```sql
-- PostgreSQL: DATE_TRUNC('month', hire_date), DATE_TRUNC('week', hire_date)  (week starts Monday)
-- MySQL:      DATE_FORMAT(hire_date, '%Y-%m-01')   or  DATE_SUB(hire_date, INTERVAL DAYOFMONTH(hire_date)-1 DAY)
-- SQL Server: DATETRUNC(month, hire_date) (2022+);  older: DATEADD(month, DATEDIFF(month, 0, hire_date), 0)
-- Oracle:     TRUNC(hire_date, 'MM')
```

**Output:**

| emp_id | hire_date | month_start | week_start_monday |
|---|---|---|---|
| 1 | 2021-03-15 | 2021-03-01 | 2021-03-15 |
| 2 | 2018-07-01 | 2018-07-01 | 2018-06-25 |
| 3 | 2022-11-10 | 2022-11-01 | 2022-11-07 |
| 4 | 2019-05-20 | 2019-05-01 | 2019-05-20 |
| 5 | 2023-01-09 | 2023-01-01 | 2023-01-09 |

**pandas equivalent:**
```python
emp = pd.DataFrame([[1, '2021-03-15'], [2, '2018-07-01'], [3, '2022-11-10'], [4, '2019-05-20'], [5, '2023-01-09'], [6, '2016-09-12'], [7, '2024-02-01'], [8, '2020-10-05']],
    columns=['emp_id', 'hire_date'])

emp['hd'] = pd.to_datetime(emp['hire_date'])
res = pd.DataFrame({'emp_id': emp['emp_id'], 'hire_date': emp['hire_date'],
    'month_start': emp['hd'].dt.to_period('M').dt.start_time.dt.strftime('%Y-%m-%d'),
    'week_start_monday': (emp['hd'] - pd.to_timedelta(emp['hd'].dt.dayofweek, unit='D')).dt.strftime('%Y-%m-%d')})
res = res[res['emp_id'] <= 5].reset_index(drop=True)
print(res)
```
**Edge cases:** NULL date gives NULL. date_trunc on a DATE returns a timestamp (2021-03-01 00:00:00) in DuckDB (verified here, hence the CAST to DATE) and in PostgreSQL (from memory). A week crossing a year end can belong to the earlier year. Decide Monday vs Sunday start before reporting weekly numbers.
**Likely follow-ups:**
- Count hires per month? `SELECT date_trunc('month', hire_date) m, COUNT(*) FROM emp GROUP BY 1 ORDER BY 1`.
- Truncate to year or quarter? Replace 'month' with 'year' or 'quarter'.
**Common mistakes:** Grouping by the raw date (one group per day), or expecting DATE_TRUNC to exist in MySQL/SQLite.

### Q34 ⭐⭐ 🟡 How do you convert a text date such as '15-08-2025' to a proper date (STR_TO_DATE, TO_DATE, CONVERT)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know text dates must be converted to real dates, and the format string differs by dialect.
**Say this in the interview:** MySQL: STR_TO_DATE('15-08-2025', '%d-%m-%Y'). PostgreSQL and Oracle: TO_DATE('15-08-2025', 'DD-MM-YYYY'). SQL Server: CONVERT(date, '15-08-2025', 105). You tell the database how the text is laid out.
**Explain simply:**
- A text like '15-08-2025' is ambiguous: is it 15 August or (in US style) month 15? The database needs the *format*.
- Once it is a real DATE you can add days, sort correctly, and extract the month.
- SQLite has no such function; I rebuilt the ISO form 'YYYY-MM-DD' with SUBSTR, which SQLite treats as a date.
- DuckDB's `strptime(text, '%d-%m-%Y')` gave identical dates (also run here).
**Example:** A legacy HR file has joining dates as '15-08-2025'; you convert them to 2025-08-15 so tenure and month reports work.
**Sample data:**

| emp_id | joined_text |
|---|---|
| 1 | 15-08-2025 |
| 2 | 01-01-2024 |
| 3 | 29-02-2024 |
| 4 | 31-12-2023 |

**SQL:**
```sql
-- table: raw_dates(emp_id INT, joined_text TEXT)
SELECT emp_id, joined_text,
       SUBSTR(joined_text, 7, 4) || '-' || SUBSTR(joined_text, 4, 2) || '-' || SUBSTR(joined_text, 1, 2) AS joined_date
FROM raw_dates;
```
Other dialects (not run here / from memory):
```sql
-- MySQL
SELECT STR_TO_DATE(joined_text, '%d-%m-%Y') FROM raw_dates;
-- PostgreSQL / Oracle
SELECT TO_DATE(joined_text, 'DD-MM-YYYY') FROM raw_dates;
-- SQL Server (style 105 = dd-mm-yyyy)
SELECT CONVERT(date, joined_text, 105) FROM raw_dates;
-- DuckDB (run here): SELECT strptime(joined_text, '%d-%m-%Y')::DATE FROM raw_dates;
```

**Output:**

| emp_id | joined_text | joined_date |
|---|---|---|
| 1 | 15-08-2025 | 2025-08-15 |
| 2 | 01-01-2024 | 2024-01-01 |
| 3 | 29-02-2024 | 2024-02-29 |
| 4 | 31-12-2023 | 2023-12-31 |

**pandas equivalent:**
```python
raw_dates = pd.DataFrame([[1, '15-08-2025'], [2, '01-01-2024'], [3, '29-02-2024'], [4, '31-12-2023']],
    columns=['emp_id', 'joined_text'])

parts = raw_dates['joined_text']
res = pd.DataFrame({'emp_id': raw_dates['emp_id'], 'joined_text': parts,
    'joined_date': pd.to_datetime(parts, format='%d-%m-%Y').dt.strftime('%Y-%m-%d')})
print(res)
```
**Edge cases:** Invalid dates: the SUBSTR trick does not validate, and SQLite's `date('2025-02-31')` returned 2025-03-03 (it rolls over silently, verified). MySQL STR_TO_DATE returns NULL for invalid dates; PostgreSQL TO_DATE can raise an error or roll over depending on the version (from memory). Mixed formats in one column need cleaning first. NULL stays NULL.
**Likely follow-ups:**
- Two-digit years? Use `%y` (MySQL) / `YY` (PostgreSQL), but be careful with century guesses.
- Safe conversion on SQL Server? `TRY_CONVERT(date, x, 105)` returns NULL on failure.
**Common mistakes:** Letting the database guess the format (month and day swapped silently), and storing dates as text forever.

### Q35 ⭐⭐ 🟡 How do you use CASE WHEN in ORDER BY for custom sort order (e.g., High, Medium, Low)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you use CASE as a sort key when alphabetical or numeric order is not the order the business wants.
**Say this in the interview:** I put a CASE expression in ORDER BY that turns each label into a rank number: High = 1, Medium = 2, Low = 3. The database sorts by that number.
**Explain simply:**
- Alphabetical order would give High, Low, Medium, which is wrong for priority.
- `ORDER BY CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 WHEN 'Low' THEN 3 ELSE 4 END`.
- ELSE catches NULL or unexpected values and decides where they land (here, last).
- Add a second sort column (req_id) to make ties predictable.
- MySQL also has `FIELD(priority,'High','Medium','Low')` as a shortcut (from memory).
**Example:** A hiring-requisition list where 'High' priority openings must appear at the top.
**Sample data:**

| req_id | role | priority |
|---|---|---|
| 1 | Data Analyst | Low |
| 2 | HR Manager | High |
| 3 | Developer | Medium |
| 4 | Recruiter | High |
| 5 | Intern | Low |
| 6 | Designer | NULL |

**SQL:**
```sql
-- table: reqs(req_id INT, role TEXT, priority TEXT)
SELECT req_id, role, priority
FROM reqs
ORDER BY CASE priority
           WHEN 'High'   THEN 1
           WHEN 'Medium' THEN 2
           WHEN 'Low'    THEN 3
           ELSE 4 END,
         req_id;
```

**Output:**

| req_id | role | priority |
|---|---|---|
| 2 | HR Manager | High |
| 4 | Recruiter | High |
| 3 | Developer | Medium |
| 1 | Data Analyst | Low |
| 5 | Intern | Low |
| 6 | Designer | NULL |

**pandas equivalent:**
```python
reqs = pd.DataFrame([[1, 'Data Analyst', 'Low'], [2, 'HR Manager', 'High'], [3, 'Developer', 'Medium'], [4, 'Recruiter', 'High'], [5, 'Intern', 'Low'], [6, 'Designer', None]],
    columns=['req_id', 'role', 'priority'])

rank = reqs['priority'].map({'High': 1, 'Medium': 2, 'Low': 3}).fillna(4)
res = reqs.assign(rank=rank).sort_values(['rank', 'req_id'])[['req_id', 'role', 'priority']]
print(res)
```
**Edge cases:** NULL priority: without ELSE, CASE returns NULL, and where NULL sorts depends on the dialect (Q39). Spelling variants ('high ', 'HIGH') fall to ELSE; clean with LOWER/TRIM. You can also sort a CASE result in the SELECT list by its alias in most dialects.
**Likely follow-ups:**
- Descending custom order? Just reverse the numbers.
- Why not store a priority number? Better design: a lookup table with a sort_order column.
**Common mistakes:** Typing the labels differently from the data (case and spaces) so everything falls into ELSE, and forgetting tie-breakers.

### Q36 ⭐⭐ 🟡 How do you use CASE WHEN inside UPDATE to change values conditionally?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you update different rows by different rules in one pass, and do you know the NULL and ELSE traps.
**Say this in the interview:** I use UPDATE with SET column = CASE WHEN condition THEN new value ... ELSE column END. It applies a different rule to each row in a single statement.
**Explain simply:**
- One UPDATE with CASE is better than several UPDATEs: one scan, and rows cannot be changed twice by accident.
- The ELSE should return the *current* value (`ELSE salary`), otherwise unmatched rows become NULL.
- Add a WHERE clause when you only intend to touch some rows, and test with a SELECT first (or run inside a transaction).
- Here: IT gets 10 percent, HR gets 5 percent, everyone else unchanged.
**Example:** Annual appraisal: IT salary 87000 -> 95700; HR 52000 -> 54600; Finance and Sales unchanged.
**Sample data:**

| emp_id | name | dept | salary |
|---|---|---|---|
| 1 | Aarav Sharma | HR | 52000 |
| 2 | Neha Iyer | Finance | 61000 |
| 3 | Karan Menon | IT | 87000 |
| 4 | Anita Desai | IT | 73000 |
| 5 | Imran Khan | Sales | 45000 |
| 6 | Priya Nair | HR | NULL |
| 7 | Arun Pillai | Sales | 38000 |
| 8 | Meera Joshi | Finance | NULL |

**SQL:**
```sql
-- table: emp(emp_id, name, email, phone, dept, salary, dob, hire_date, status)
UPDATE emp
SET salary = CASE WHEN dept = 'IT' THEN ROUND(salary * 1.10)
                  WHEN dept = 'HR' THEN ROUND(salary * 1.05)
                  ELSE salary END;

SELECT emp_id, name, dept, salary FROM emp;
```

**Output:**

| emp_id | name | dept | salary |
|---|---|---|---|
| 1 | Aarav Sharma | HR | 54600 |
| 2 | Neha Iyer | Finance | 61000 |
| 3 | Karan Menon | IT | 95700 |
| 4 | Anita Desai | IT | 80300 |
| 5 | Imran Khan | Sales | 45000 |
| 6 | Priya Nair | HR | NULL |
| 7 | Arun Pillai | Sales | 38000 |
| 8 | Meera Joshi | Finance | NULL |

(The Output shows the table after the UPDATE; the sample above is before.)

**pandas equivalent:**
```python
emp = pd.DataFrame([[1, 'Aarav Sharma', 'HR', 52000], [2, 'Neha Iyer', 'Finance', 61000], [3, 'Karan Menon', 'IT', 87000], [4, 'Anita Desai', 'IT', 73000], [5, 'Imran Khan', 'Sales', 45000], [6, 'Priya Nair', 'HR', None], [7, 'Arun Pillai', 'Sales', 38000], [8, 'Meera Joshi', 'Finance', None]],
    columns=['emp_id', 'name', 'dept', 'salary'])

mult = emp['dept'].map({'IT': 1.10, 'HR': 1.05}).fillna(1.0)
emp['salary'] = (emp['salary'] * mult).round()
res = emp[['emp_id', 'name', 'dept', 'salary']]
print(res)
```
**Edge cases:** NULL salary stays NULL (NULL times 1.05 is NULL), as seen for Priya (HR). A forgotten ELSE sets all other rows to NULL. UPDATE without WHERE touches every row. Use a transaction: BEGIN; UPDATE...; check; COMMIT or ROLLBACK. Rounding: stored integers get rounded; decimals may be better for money.
**Likely follow-ups:**
- UPDATE with a JOIN? Syntax differs: MySQL `UPDATE a JOIN b ...`, PostgreSQL `UPDATE a SET ... FROM b`, SQL Server `UPDATE a SET ... FROM a JOIN b` (not run here).
- How to undo? ROLLBACK if still inside the transaction; otherwise restore from backup.
**Common mistakes:** Missing ELSE (silently NULLing data), no WHERE, and running UPDATE in production without testing the SELECT first.

### Q37 ⭐⭐ 🟡 How do you create age bands or salary buckets using CASE WHEN and count per bucket?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you bucket a number with CASE WHEN and then count per bucket, and do you remember the CASE order and NULL rules.
**Say this in the interview:** I write a CASE expression that labels each row with a band, then GROUP BY that label and COUNT(*). CASE checks conditions top to bottom and stops at the first match, so I order them from lowest to highest.
**Explain simply:**
- A *bucket* or *band* is a range such as salary below 50k.
- Because CASE stops at the first true condition, `salary < 75000` after `salary < 50000` really means 50k to 74,999.
- Number the labels ('1. Below 50k') so the ORDER BY puts bands in logical order, not alphabetical.
- Give NULLs their own bucket; otherwise they fall into ELSE and are mislabelled as the top band.
- SQL Server cannot GROUP BY an alias; wrap the CASE in a subquery or repeat it.
**Example:** Compensation review: 2 people below 50k, 3 between 50k and 75k, 1 above, and 2 with no salary recorded.
**Sample data:**

| emp_id | name | salary | dob |
|---|---|---|---|
| 1 | Aarav Sharma | 52000 | 1990-08-14 |
| 2 | Neha Iyer | 61000 | 1985-01-22 |
| 3 | Karan Menon | 87000 | 1992-08-30 |
| 4 | Anita Desai | 73000 | 1988-12-05 |
| 5 | Imran Khan | 45000 | 1995-08-02 |
| 6 | Priya Nair | NULL | 1983-04-17 |
| 7 | Arun Pillai | 38000 | 1998-02-11 |
| 8 | Meera Joshi | NULL | 1991-11-25 |

**SQL:**
```sql
-- table: emp(emp_id, name, email, phone, dept, salary, dob, hire_date, status)
SELECT CASE WHEN salary IS NULL   THEN '4. Unknown'
            WHEN salary < 50000    THEN '1. Below 50k'
            WHEN salary < 75000    THEN '2. 50k to 74,999'
            ELSE                        '3. 75k and above' END AS salary_band,
       COUNT(*) AS headcount
FROM emp
GROUP BY salary_band
ORDER BY salary_band;
```
Age bands the same way (reference date fixed at 2025-08-20 for a repeatable result; also run here):
```sql
SELECT CASE WHEN age < 30 THEN '1. Under 30'
            WHEN age < 40 THEN '2. 30-39'
            ELSE '3. 40 and over' END AS age_band,
       COUNT(*) AS headcount
FROM (SELECT CAST((julianday('2025-08-20') - julianday(dob)) / 365.25 AS INTEGER) AS age
      FROM emp) t
GROUP BY age_band
ORDER BY age_band;
```
Result:

| age_band | headcount |
|---|---|
| 1. Under 30 | 1 |
| 2. 30-39 | 5 |
| 3. 40 and over | 2 |

Other dialects (not run here / from memory): age via `DATEDIFF(year, dob, GETDATE())` in SQL Server (counts calendar-year boundaries, can be off by one) or `TIMESTAMPDIFF(YEAR, dob, CURDATE())` in MySQL.

**Output:**

| salary_band | headcount |
|---|---|
| 1. Below 50k | 2 |
| 2. 50k to 74,999 | 3 |
| 3. 75k and above | 1 |
| 4. Unknown | 2 |

**pandas equivalent:**
```python
emp = pd.DataFrame([[1, 52000], [2, 61000], [3, 87000], [4, 73000], [5, 45000], [6, None], [7, 38000], [8, None]],
    columns=['emp_id', 'salary'])

import numpy as np
band = np.select([emp['salary'].isna(), emp['salary'] < 50000, emp['salary'] < 75000],
                 ['4. Unknown', '1. Below 50k', '2. 50k to 74,999'], default='3. 75k and above')
res = (pd.DataFrame({'salary_band': band}).groupby('salary_band').size()
         .reset_index(name='headcount'))
print(res)
```
**Edge cases:** NULL salary: `salary < 50000` is unknown (not true), so without an IS NULL branch it falls to ELSE and wrongly lands in the top band. Boundaries: decide whether 50000 belongs to the lower or upper band (here it goes up). Empty bands do not appear unless you join to a list of bands.
**Likely follow-ups:**
- Show empty bands too? LEFT JOIN from a small bands table.
- Use BETWEEN? Fine for integers, risky for decimals (gaps like 49999.50).
**Common mistakes:** Overlapping or out-of-order conditions, forgetting NULLs, and sorting band labels alphabetically ('10-20' before '5-10').

### Q38 ⭐⭐ 🟡 How do you find employees whose birthday falls this month?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you compare only the month part of a date and avoid the year trap; do you know the 'current date' function per dialect.
**Say this in the interview:** I compare the month of the birth date with the month of today's date, ignoring the year: MONTH(dob) = MONTH(CURRENT_DATE). Birthdays repeat every year, so only the month matters.
**Explain simply:**
- The mistake is comparing full dates; the birth year never equals this year.
- MySQL: `MONTH(dob) = MONTH(CURDATE())`. PostgreSQL: `EXTRACT(MONTH FROM dob) = EXTRACT(MONTH FROM CURRENT_DATE)`. SQL Server: `MONTH(dob) = MONTH(GETDATE())`.
- SQLite (run here): `strftime('%m', dob) = strftime('%m', 'now')`. I replaced 'now' with 2025-08-20 so the output is repeatable.
- Order by day to give HR a calendar-style list.
**Example:** HR wants to send birthday emails: for August the list is Imran (2 Aug), Aarav (14 Aug), Karan (30 Aug).
**Sample data:**

| emp_id | name | dob |
|---|---|---|
| 1 | Aarav Sharma | 1990-08-14 |
| 2 | Neha Iyer | 1985-01-22 |
| 3 | Karan Menon | 1992-08-30 |
| 4 | Anita Desai | 1988-12-05 |
| 5 | Imran Khan | 1995-08-02 |
| 6 | Priya Nair | 1983-04-17 |
| 7 | Arun Pillai | 1998-02-11 |
| 8 | Meera Joshi | 1991-11-25 |

**SQL:**
```sql
-- table: emp(emp_id, name, email, phone, dept, salary, dob, hire_date, status)
SELECT emp_id, name, dob
FROM emp
WHERE strftime('%m', dob) = strftime('%m', '2025-08-20')   -- in real use: strftime('%m', 'now')
ORDER BY strftime('%d', dob);
```
Other dialects (not run here / from memory):
```sql
-- MySQL
SELECT emp_id, name, dob FROM emp WHERE MONTH(dob) = MONTH(CURDATE()) ORDER BY DAY(dob);
-- PostgreSQL
SELECT emp_id, name, dob FROM emp WHERE EXTRACT(MONTH FROM dob) = EXTRACT(MONTH FROM CURRENT_DATE) ORDER BY EXTRACT(DAY FROM dob);
-- SQL Server
SELECT emp_id, name, dob FROM emp WHERE MONTH(dob) = MONTH(GETDATE()) ORDER BY DAY(dob);
```

**Output:**

| emp_id | name | dob |
|---|---|---|
| 5 | Imran Khan | 1995-08-02 |
| 1 | Aarav Sharma | 1990-08-14 |
| 3 | Karan Menon | 1992-08-30 |

**pandas equivalent:**
```python
emp = pd.DataFrame([[1, 'Aarav Sharma', '1990-08-14'], [2, 'Neha Iyer', '1985-01-22'], [3, 'Karan Menon', '1992-08-30'], [4, 'Anita Desai', '1988-12-05'], [5, 'Imran Khan', '1995-08-02'], [6, 'Priya Nair', '1983-04-17'], [7, 'Arun Pillai', '1998-02-11'], [8, 'Meera Joshi', '1991-11-25']],
    columns=['emp_id', 'name', 'dob'])

emp['d'] = pd.to_datetime(emp['dob'])
res = emp[emp['d'].dt.month == 8].assign(day=emp['d'].dt.day).sort_values('day')[['emp_id', 'name', 'dob']]
print(res)
```
**Edge cases:** NULL dob is excluded. Feb 29 birthdays: they match in February every year, but you may need a rule for non-leap years. Year-end lists (December to January) need a next-30-days style test instead. Never compare the full `dob` to today's date.
**Likely follow-ups:**
- Birthdays in the next 7 days? Compare day-of-year or build this year's birthday date and test BETWEEN today and today+7 (tricky around year end).
- Employees' age today? Use DATEDIFF/age functions and adjust if the birthday has not happened yet this year.
**Common mistakes:** Comparing the whole date, mixing text '08' with number 8 in SQLite, and forgetting the dialect-specific current-date function.

### Q39 ⭐⭐ 🟡 How do you handle NULLs when sorting (NULLS FIRST / NULLS LAST) across dialects?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know where NULLs sort by default and how to control it portably.
**Say this in the interview:** PostgreSQL, Oracle and SQLite support ORDER BY col DESC NULLS LAST. MySQL and SQL Server do not, so I add a helper sort key: CASE WHEN col IS NULL THEN 1 ELSE 0 END first, then the real column.
**Explain simply:**
- Databases disagree on whether NULL is the smallest or the largest value when sorting.
- Default (from memory): MySQL, SQL Server and SQLite treat NULL as smallest (first in ASC, last in DESC); PostgreSQL and Oracle treat NULL as largest (last in ASC, first in DESC).
- SQLite run here: ascending order put the two NULL salaries first (verified).
- `NULLS FIRST` / `NULLS LAST` makes it explicit; the CASE helper gives the same result everywhere.
**Example:** A salary report sorted high to low should not show people with missing salary at the very top.
**Sample data:**

| emp_id | name | salary |
|---|---|---|
| 1 | Aarav Sharma | 52000 |
| 2 | Neha Iyer | 61000 |
| 3 | Karan Menon | 87000 |
| 4 | Anita Desai | 73000 |
| 5 | Imran Khan | 45000 |
| 6 | Priya Nair | NULL |
| 7 | Arun Pillai | 38000 |
| 8 | Meera Joshi | NULL |

**SQL:**
```sql
-- table: emp(emp_id, name, email, phone, dept, salary, dob, hire_date, status)
SELECT emp_id, name, salary
FROM emp
ORDER BY salary DESC NULLS LAST, emp_id;
```
Portable version for MySQL and SQL Server, which lack NULLS FIRST/LAST (also run here, same result):
```sql
SELECT emp_id, name, salary
FROM emp
ORDER BY CASE WHEN salary IS NULL THEN 1 ELSE 0 END, salary DESC, emp_id;
```
MySQL shortcut (not run here): `ORDER BY salary IS NULL, salary DESC`.

**Output:**

| emp_id | name | salary |
|---|---|---|
| 3 | Karan Menon | 87000 |
| 4 | Anita Desai | 73000 |
| 2 | Neha Iyer | 61000 |
| 1 | Aarav Sharma | 52000 |
| 5 | Imran Khan | 45000 |
| 7 | Arun Pillai | 38000 |
| 6 | Priya Nair | NULL |
| 8 | Meera Joshi | NULL |

**pandas equivalent:**
```python
emp = pd.DataFrame([[1, 'Aarav Sharma', 52000], [2, 'Neha Iyer', 61000], [3, 'Karan Menon', 87000], [4, 'Anita Desai', 73000], [5, 'Imran Khan', 45000], [6, 'Priya Nair', None], [7, 'Arun Pillai', 38000], [8, 'Meera Joshi', None]],
    columns=['emp_id', 'name', 'salary'])

res = emp.sort_values(['salary', 'emp_id'], ascending=[False, True], na_position='last')[['emp_id', 'name', 'salary']]
print(res)
```
**Edge cases:** Several NULLs tie with each other, so add a tie-breaker (emp_id) for a stable order. In SQLite the default ASC order starts with emp 6, emp 8 (the NULLs). A NULL is not zero: sorting never treats it as 0.
**Likely follow-ups:**
- Put NULLs first on a column? `ORDER BY salary IS NOT NULL, salary` in MySQL.
- Does the CASE trick slow things down? It can prevent an index from being used for the sort (from memory).
**Common mistakes:** Assuming NULLs sort the same everywhere, and using COALESCE(salary, 0) for sorting, which wrongly mixes missing values with real zeros.

### Q40 ⭐⭐ 🟡 How do you count NULLs and non-NULLs of a column in one query?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know COUNT(*) counts rows but COUNT(column) skips NULLs; a classic data-quality check.
**Say this in the interview:** COUNT(*) counts all rows, COUNT(column) counts only rows where that column is not NULL. The difference is the number of NULLs. I can also use SUM(CASE WHEN col IS NULL THEN 1 ELSE 0 END).
**Explain simply:**
- NULL means the value is missing or unknown, not zero and not empty text.
- `COUNT(*)` = all rows. `COUNT(phone)` = rows with a phone. `COUNT(*) - COUNT(phone)` = rows without.
- The CASE form is more flexible: you can add other conditions, and it generalises to counting empty strings too.
- PostgreSQL also has `COUNT(*) FILTER (WHERE phone IS NULL)` (SQLite supports it too; not run here).
**Example:** Data-quality check before an attrition model: 8 employees, 7 phone numbers filled, 1 missing; 6 salaries filled, 2 missing.
**Sample data:**

| emp_id | name | phone | salary |
|---|---|---|---|
| 1 | Aarav Sharma | 98765-43210 | 52000 |
| 2 | Neha Iyer | 91234-56789 | 61000 |
| 3 | Karan Menon | 99887-76655 | 87000 |
| 4 | Anita Desai | 90000-12345 | 73000 |
| 5 | Imran Khan | NULL | 45000 |
| 6 | Priya Nair | 98700-11122 | NULL |
| 7 | Arun Pillai | 97000-22233 | 38000 |
| 8 | Meera Joshi | 96000-33344 | NULL |

**SQL:**
```sql
-- table: emp(emp_id, name, email, phone, dept, salary, dob, hire_date, status)
SELECT COUNT(*)                                  AS total_rows,
       COUNT(phone)                              AS phone_filled,
       COUNT(*) - COUNT(phone)                   AS phone_missing,
       SUM(CASE WHEN phone IS NULL THEN 1 ELSE 0 END) AS phone_missing_v2,
       COUNT(salary)                             AS salary_filled,
       COUNT(*) - COUNT(salary)                  AS salary_missing
FROM emp;
```

**Output:**

| total_rows | phone_filled | phone_missing | phone_missing_v2 | salary_filled | salary_missing |
|---|---|---|---|---|---|
| 8 | 7 | 1 | 1 | 6 | 2 |

**pandas equivalent:**
```python
emp = pd.DataFrame([[1, '98765-43210', 52000], [2, '91234-56789', 61000], [3, '99887-76655', 87000], [4, '90000-12345', 73000], [5, None, 45000], [6, '98700-11122', None], [7, '97000-22233', 38000], [8, '96000-33344', None]],
    columns=['emp_id', 'phone', 'salary'])

res = pd.DataFrame({'total_rows': [len(emp)],
    'phone_filled': [emp['phone'].notna().sum()],
    'phone_missing': [emp['phone'].isna().sum()],
    'phone_missing_v2': [emp['phone'].isna().sum()],
    'salary_filled': [emp['salary'].notna().sum()],
    'salary_missing': [emp['salary'].isna().sum()]})
print(res)
```
**Edge cases:** Empty strings '' are NOT NULL, so COUNT counts them as filled; check with `phone = ''` too. COUNT(DISTINCT col) also ignores NULLs. On an empty table COUNT returns 0, while SUM returns NULL (wrap with COALESCE).
**Likely follow-ups:**
- Percentage missing? `100.0 * (COUNT(*) - COUNT(col)) / COUNT(*)` (use 100.0 to avoid integer division).
- Per department? Add `GROUP BY dept`.
**Common mistakes:** Using `= NULL` instead of IS NULL, using COUNT(*) when you meant COUNT(column), and integer division when computing percentages.

### Q41 ⭐⭐ 🟡 How do you calculate the percentage of rows meeting a condition (e.g., attrition rate) using CASE WHEN?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you turn a condition into 1/0 and divide to get a rate, without integer-division or NULL traps?
**Say this in the interview:** I flag each row with CASE WHEN, add up the flags, and divide by the row count, multiplying by 100.0 so the division is not whole-number only.
**Explain simply:**
- CASE WHEN tests a condition per row. Giving 1 for leavers and 0 for others lets SUM count the leavers (this is called conditional aggregation: an aggregate with a CASE inside).
- Multiply by 100.0, not 100: in many databases (SQL Server, PostgreSQL) integer / integer drops decimals, so 1/3 becomes 0.
- Shortcut: `AVG(CASE WHEN status='Left' THEN 1.0 ELSE 0 END)` is the leaver share directly.
- Strictly, attrition rate = leavers / average headcount in the period; this simple version uses current rows.
**Example:** HR has 3 IT staff and 1 has left, so IT attrition is 1/3 = 33.3%.
**Sample data:**
| emp_id | name | dept | status |
|---|---|---|---|
| 1 | Asha | Sales | Active |
| 2 | Bala | Sales | Left |
| 3 | Chitra | HR | Active |
| 4 | Deepak | HR | Left |
| 5 | Esha | IT | Active |
| 6 | Farhan | IT | Active |
| 7 | Gita | IT | Left |
**SQL:**
```sql
SELECT dept,
       COUNT(*) AS headcount,
       SUM(CASE WHEN status = 'Left' THEN 1 ELSE 0 END) AS leavers,
       ROUND(100.0 * SUM(CASE WHEN status = 'Left' THEN 1 ELSE 0 END) / COUNT(*), 1) AS attrition_pct
FROM emp
GROUP BY dept
ORDER BY dept
```
**Output:**
| dept | headcount | leavers | attrition_pct |
|---|---|---|---|
| HR | 2 | 1 | 50.0 |
| IT | 3 | 1 | 33.3 |
| Sales | 2 | 1 | 50.0 |
**pandas equivalent:**
```python
res = emp.assign(l=(emp.status == 'Left').astype(int)).groupby('dept').agg(headcount=('emp_id','count'), leavers=('l','sum')).reset_index()
res['attrition_pct'] = (100 * res.leavers / res.headcount).round(1)
# result matches the SQL output (checked)
```
**Edge cases:** A NULL status makes the CASE fall to ELSE 0, so it counts as 'not left' - decide if that is right. An empty department never appears with GROUP BY (no rows). Divide-by-zero can occur only if the denominator can be 0 (see NULLIF, Q15).
**Likely follow-ups:**
- How do I show it as a % string? `CONCAT(ROUND(...,1),'%')` in MySQL/Postgres; SQL Server uses `CAST(... AS varchar)+'%'`.
- How to get the company total next to each department? Add a second query with no GROUP BY, or use a window function `SUM(...) OVER ()`.
**Common mistakes:** Using 100 instead of 100.0 (result 0 or 33 instead of 33.3), and putting the condition in WHERE, which removes the denominator rows.

### Q42 ⭐⭐ 🟡 How do you find missing dates or the first and last day of a month?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know a missing date is found by building a full calendar and anti-joining, and how to get month boundaries?
**Say this in the interview:** SQL only returns rows that exist, so to find gaps I generate every date in the range and LEFT JOIN my data; the rows with no match are the missing dates.
**Explain simply:**
- A recursive CTE (a query that calls itself, adding one day each round) makes the calendar. PostgreSQL has `generate_series`; see Q60.
- LEFT JOIN + `WHERE right.col IS NULL` is called an anti-join: it keeps only unmatched calendar days.
- First day of month: `DATE_TRUNC('month', d)` (Postgres), `DATE_FORMAT(d,'%Y-%m-01')` (MySQL), `DATEFROMPARTS(YEAR(d),MONTH(d),1)` (SQL Server). Last day: `EOMONTH(d)` (SQL Server), `LAST_DAY(d)` (MySQL), `DATE_TRUNC('month',d)+INTERVAL '1 month - 1 day'` (Postgres). Not run here / from memory; SQLite version below was run.
**Example:** Asha has attendance rows on 3, 4, 6 and 7 March 2025, so 5 March is the missing day.
**Sample data:**
| emp_id | work_date |
|---|---|
| 1 | 2025-03-03 |
| 1 | 2025-03-04 |
| 1 | 2025-03-06 |
| 1 | 2025-03-07 |
**SQL:**
```sql
WITH RECURSIVE cal(d) AS (
    SELECT MIN(work_date) FROM attendance
    UNION ALL
    SELECT date(d, '+1 day') FROM cal WHERE d < (SELECT MAX(work_date) FROM attendance)
)
SELECT cal.d AS missing_date
FROM cal
LEFT JOIN attendance a ON a.work_date = cal.d
WHERE a.work_date IS NULL;

-- first and last day of the month containing 14 Feb 2025 (SQLite)
SELECT date('2025-02-14', 'start of month') AS first_day,
       date('2025-02-14', 'start of month', '+1 month', '-1 day') AS last_day;
```
**Output:**
| missing_date |
|---|
| 2025-03-05 |

| first_day | last_day |
|---|---|
| 2025-02-01 | 2025-02-28 |
**pandas equivalent:**
```python
full = pd.date_range(att.work_date.min(), att.work_date.max())
res = pd.DataFrame({'missing_date': full.difference(att.work_date)})
# month boundaries
d = pd.Timestamp('2025-02-14'); first = d.replace(day=1); last = d + pd.offsets.MonthEnd(0)
# result matches the SQL output (checked)
```
**Edge cases:** Weekends and holidays show as missing unless you filter them (Q44). Duplicate attendance rows do not matter for the anti-join. If the table is empty, MIN is NULL and the calendar is empty. Leap-year February is handled automatically by the date functions.
**Likely follow-ups:**
- How to find missing IDs rather than dates? Same pattern with a number series.
- Why not just compare consecutive rows? LAG can find gaps too, but only reports the gap start/end, not every date.
**Common mistakes:** Trying to find missing dates from the same table alone, and forgetting that the end of the calendar must come from MAX or a fixed end date.

### Q43 ⭐⭐ 🟡 What are NULL-safe comparisons (IS DISTINCT FROM, <=> in MySQL)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know that = with NULL gives unknown, and which operator treats two NULLs as equal?
**Say this in the interview:** A normal comparison with NULL returns unknown, so those rows drop out. A NULL-safe comparison treats NULL as a value: IS NOT DISTINCT FROM in standard SQL and PostgreSQL, <=> in MySQL.
**Explain simply:**
- NULL means 'unknown'. Is unknown equal to unknown? Unknown - so `NULL = NULL` is not true, and a WHERE filter only keeps rows that are true.
- `a IS NOT DISTINCT FROM b` is true when both are equal or both are NULL; `IS DISTINCT FROM` is the opposite (different, or exactly one is NULL).
- MySQL: `a <=> b`. SQL Server: `a IS NOT DISTINCT FROM b` since SQL Server 2022 (from memory); older versions use `(a = b OR (a IS NULL AND b IS NULL))`. SQLite: `a IS b` also works.
- Handy for comparing old and new data to find changed rows, including changes to or from NULL.
**Example:** Comparing last year's manager_id to this year's: if both are NULL (no manager) a normal `=` says 'not equal' - wrong for a change report.
**Sample data:**
| id | a | b |
|---|---|---|
| 1 | x | x |
| 2 | x | NULL |
| 3 | NULL | NULL |
| 4 | x | y |
**SQL:**
```sql
SELECT id, a, b,
       CASE WHEN a = b THEN 'true' WHEN NOT (a = b) THEN 'false' ELSE 'unknown(NULL)' END AS plain_equals,
       CASE WHEN a IS NOT DISTINCT FROM b THEN 'true' ELSE 'false' END AS null_safe_equals
FROM t
```
**Output:**
| id | a | b | plain_equals | null_safe_equals |
|---|---|---|---|---|
| 1 | x | x | true | true |
| 2 | x | NULL | unknown(NULL) | false |
| 3 | NULL | NULL | unknown(NULL) | true |
| 4 | x | y | false | false |
**pandas equivalent:**
```python
same = (tdf.a == tdf.b) | (tdf.a.isna() & tdf.b.isna())
print(tdf[same].id.tolist())   # [1, 3]
# note: pandas NaN != NaN, so you must add the both-null test yourself
```
**Edge cases:** `WHERE a <> b` misses row 2 (x vs NULL) - a real difference. Indexes may not be used with the OR-expanded version in some engines.
**Likely follow-ups:**
- Is `NULL IS NULL` true? Yes, IS NULL is the right test for one column.
- Does GROUP BY treat NULLs as equal? Yes, NULLs form one group, as do DISTINCT and UNION.
**Common mistakes:** Writing `a = NULL`, or using `<>` and expecting NULL changes to be found.

### Q44 ⭐⭐ 🟡 How do you calculate working days / exclude weekends between two dates?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you count only Monday-Friday days between two dates, including both ends, and handle ranges with zero working days?
**Say this in the interview:** I build a calendar of dates, join each task to the dates inside its range, drop Saturdays and Sundays in the join condition, and count what is left. Holidays would need a holiday table to exclude.
**Explain simply:**
- No dialect has one built-in function; you either use a calendar table or arithmetic on the weekday.
- I put the weekday test in the LEFT JOIN's ON clause (not WHERE) so a weekend-only task still appears with 0.
- SQL Server idea (not run here): `DATEDIFF(day,s,e)+1 - DATEDIFF(week,s,e)*2` with corrections for start/end on Sunday/Saturday. PostgreSQL: `COUNT(*) FILTER (WHERE EXTRACT(isodow FROM d) < 6)` over `generate_series`. MySQL: same recursive calendar with `WEEKDAY(d) < 5`.
- Counted inclusive: 3 to 14 March has 12 calendar days, 10 of them weekdays.
**Example:** Leave from Fri 7 Mar to Mon 10 Mar is 2 working days; Sat 8 to Sun 9 is 0.
**Sample data:**
| id | start_date | end_date |
|---|---|---|
| 1 | 2025-03-03 | 2025-03-14 |
| 2 | 2025-03-07 | 2025-03-10 |
| 3 | 2025-03-08 | 2025-03-09 |
**SQL:**
```sql
WITH RECURSIVE cal(d) AS (
    SELECT MIN(start_date) FROM tasks
    UNION ALL
    SELECT date(d, '+1 day') FROM cal WHERE d < (SELECT MAX(end_date) FROM tasks)
)
SELECT t.id, t.start_date, t.end_date,
       COUNT(cal.d) AS working_days
FROM tasks t
LEFT JOIN cal
       ON cal.d BETWEEN t.start_date AND t.end_date
      AND strftime('%w', cal.d) NOT IN ('0', '6')      -- 0 = Sunday, 6 = Saturday
GROUP BY t.id, t.start_date, t.end_date
ORDER BY t.id
```
**Output:**
| id | start_date | end_date | working_days |
|---|---|---|---|
| 1 | 2025-03-03 | 2025-03-14 | 10 |
| 2 | 2025-03-07 | 2025-03-10 | 2 |
| 3 | 2025-03-08 | 2025-03-09 | 0 |
**pandas equivalent:**
```python
res = tk.copy()
res['working_days'] = np.busday_count(pd.to_datetime(tk.start_date).values.astype('datetime64[D]'),
                                      (pd.to_datetime(tk.end_date) + pd.Timedelta(days=1)).values.astype('datetime64[D]'))
# busday_count excludes the end date, so add 1 day for an inclusive count
# result matches the SQL output (checked)
```
**Edge cases:** Weekday numbering differs: SQLite %w and MySQL DAYOFWEEK start at Sunday (0 or 1), MySQL WEEKDAY starts Monday=0, SQL Server depends on DATEFIRST. Public holidays and half days are not handled. Start after end gives 0 here.
**Likely follow-ups:**
- How to remove holidays? Add `AND cal.d NOT IN (SELECT hol_date FROM holidays)`.
- Does this scale? For a big HR system, keep a permanent calendar table with an is_workday flag.
**Common mistakes:** Counting calendar days minus a guess, forgetting inclusive vs exclusive end dates, and using an INNER JOIN so zero-day ranges vanish.

### Q45 ⭐ 🟢 How do you use TRIM, LTRIM and RTRIM to remove spaces?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Basic text-cleaning knowledge, and that TRIM only removes certain characters.
**Say this in the interview:** TRIM removes spaces from both ends, LTRIM from the left, RTRIM from the right. It never touches spaces inside the text.
**Explain simply:**
- Stray spaces make 'Asha' and 'Asha ' look different, so joins and filters silently miss rows.
- MySQL, PostgreSQL, SQLite have TRIM/LTRIM/RTRIM. SQL Server has LTRIM/RTRIM always, and TRIM from 2017 (from memory); older code writes `LTRIM(RTRIM(x))`.
- Standard form `TRIM(BOTH 'x' FROM col)` removes other characters in MySQL/Postgres (not run here); SQLite `TRIM(col, 'x')`.
- Plain TRIM removes spaces only, not tabs, line breaks or the non-breaking space copied from web pages; use REPLACE for those.
**Example:** A name typed as '  Asha ' with 6 characters becomes 'Asha' with 4.
**Sample data:**
| id | name |
|---|---|
| 1 |   Asha  |
| 2 |  Bala |
| 3 | Chitra    |
| 4 | Deepak |
**SQL:**
```sql
SELECT '[' || name || ']'          AS raw,
       '[' || TRIM(name) || ']'    AS trimmed,
       '[' || LTRIM(name) || ']'   AS left_trimmed,
       '[' || RTRIM(name) || ']'   AS right_trimmed,
       LENGTH(TRIM(name))          AS clean_length
FROM names
```
**Output:**
| raw | trimmed | left_trimmed | right_trimmed | clean_length |
|---|---|---|---|---|
| [  Asha ] | [Asha] | [Asha ] | [  Asha] | 4 |
| [ Bala] | [Bala] | [Bala] | [ Bala] | 4 |
| [Chitra   ] | [Chitra] | [Chitra   ] | [Chitra] | 6 |
| [Deepak] | [Deepak] | [Deepak] | [Deepak] | 6 |
**pandas equivalent:**
```python
res = pd.DataFrame({'raw': '[' + nm.name + ']', 'trimmed': '[' + nm.name.str.strip() + ']',
                    'left_trimmed': '[' + nm.name.str.lstrip() + ']', 'right_trimmed': '[' + nm.name.str.rstrip() + ']',
                    'clean_length': nm.name.str.strip().str.len()})
# result matches the SQL output (checked)
```
**Edge cases:** TRIM(NULL) is NULL. A value of only spaces becomes an empty string '', not NULL (Oracle treats '' as NULL). Trailing spaces in CHAR columns can be padded by the database.
**Likely follow-ups:**
- Why does LENGTH differ from what I see? Hidden spaces.
- Should I trim in the table? Best to clean once on load and also compare with TRIM.
**Common mistakes:** Expecting TRIM to remove inner spaces or tabs, and trimming only on one side of a join.

### Q46 ⭐ 🟢 How do you pad numbers with leading zeros (LPAD, RIGHT, FORMAT)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you format codes with fixed width in each dialect?
**Say this in the interview:** In MySQL and PostgreSQL I use LPAD(id, 5, '0'); SQL Server has no LPAD so I use RIGHT('00000'+CAST(id AS varchar),5) or FORMAT(id,'00000').
**Explain simply:**
- Padding turns 7 into 00007 so codes sort and look uniform. The result is text, not a number.
- MySQL: `LPAD(emp_id,5,'0')`. PostgreSQL: `LPAD(emp_id::text,5,'0')`. SQL Server: `RIGHT('00000'+CAST(emp_id AS varchar(5)),5)` or `FORMAT(emp_id,'00000')`. Not run here / from memory.
- Run here in SQLite: `printf('%05d', id)`, and the portable `substr('00000'||id, -5)` trick.
- Caution: LPAD truncates if the value is longer than the target width (MySQL/Postgres), so 1234567 becomes 12345.
**Example:** Employee 42 becomes EMP00042 and 105 becomes EMP00105.
**Sample data:**
| emp_id |
|---|
| 7 |
| 42 |
| 105 |
**SQL:**
```sql
SELECT emp_id,
       printf('%05d', emp_id)                      AS padded,
       'EMP' || printf('%05d', emp_id)            AS emp_code,
       substr('00000' || emp_id, -5)               AS padded_alt
FROM ids
```
**Output:**
| emp_id | padded | emp_code | padded_alt |
|---|---|---|---|
| 7 | 00007 | EMP00007 | 00007 |
| 42 | 00042 | EMP00042 | 00042 |
| 105 | 00105 | EMP00105 | 00105 |
**pandas equivalent:**
```python
res = pd.DataFrame({'emp_id': ii.emp_id, 'padded': ii.emp_id.astype(str).str.zfill(5)})
res['emp_code'] = 'EMP' + res.padded
res['padded_alt'] = res.padded
# result matches the SQL output (checked)
```
**Edge cases:** NULL id gives NULL (SQLite printf gives 00000 for NULL; check your engine). Numbers wider than the pad length may be cut. Padded text sorts correctly as text.
**Likely follow-ups:**
- Why not store the code as a number? Leading zeros would be lost.
- How do I remove leading zeros? CAST to integer.
**Common mistakes:** Forgetting that the padded value is text, and that LPAD cuts long values.

### Q47 ⭐ 🟡 How do you find the day of the week with the highest sales?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you derive the weekday from a date, group by it and pick the top one?
**Say this in the interview:** I extract the weekday from the sale date, SUM the amount per weekday, sort descending and take the first row.
**Explain simply:**
- Weekday functions: MySQL `DAYNAME(d)`, PostgreSQL `TO_CHAR(d,'Day')` or `EXTRACT(dow FROM d)`, SQL Server `DATENAME(weekday,d)`. SQLite: `strftime('%w', d)` (number), as run here.
- Top-1 syntax: `LIMIT 1` (MySQL/Postgres/SQLite), `SELECT TOP 1` (SQL Server), `FETCH FIRST 1 ROW ONLY` (standard).
- For ties use `RANK()` or `FETCH FIRST 1 ROW WITH TIES`.
- Better question: is it total sales or average per day? A weekday that appears in more weeks naturally has more total.
**Example:** Fridays 7 and 14 March gave 300 + 320 = 620, the highest total.
**Sample data:**
| sale_date | amount |
|---|---|
| 2025-03-03 | 200 |
| 2025-03-04 | 150 |
| 2025-03-05 | 180 |
| 2025-03-07 | 300 |
| 2025-03-08 | 90 |
| 2025-03-10 | 250 |
| 2025-03-14 | 320 |
| 2025-03-15 | 60 |
**SQL:**
```sql
SELECT strftime('%w', sale_date) AS dow_no,           -- 0 = Sunday in SQLite
       substr('SunMonTueWedThuFriSat', strftime('%w', sale_date) * 3 + 1, 3) AS day_name,
       SUM(amount) AS total_sales
FROM sales
GROUP BY dow_no, day_name
ORDER BY total_sales DESC
LIMIT 1
```
**Output:**
| dow_no | day_name | total_sales |
|---|---|---|
| 5 | Fri | 620 |
**pandas equivalent:**
```python
sd['day'] = sd.d.dt.day_name().str[:3]
res = sd.groupby('day', as_index=False).amount.sum().sort_values('amount', ascending=False).head(1)
print(res)   # Fri, 620
```
**Edge cases:** Ties give an arbitrary single row with LIMIT 1. Weekday numbering and first-day-of-week settings differ by dialect. NULL amounts are ignored by SUM. Days with no sales do not appear.
**Likely follow-ups:**
- How do I average per weekday rather than total? Count distinct dates and divide.
- How to show all 7 days? Remove LIMIT.
**Common mistakes:** Grouping by the date instead of the weekday, and forgetting to repeat the weekday expression in GROUP BY on strict engines.

### Q48 ⭐ 🟡 How do you group sales by fiscal year or quarter (e.g., April-March)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you shift the calendar so the year starts in April and derive quarters from it?
**Say this in the interview:** A date belongs to the financial year that started in April: if the month is April or later the year is the calendar year, otherwise it is last year. Quarter is the months-since-April divided by three.
**Explain simply:**
- A fiscal year is the company's accounting year; in India it runs April to March, written FY2025-26.
- Fiscal year start year = `CASE WHEN month >= 4 THEN year ELSE year - 1 END`.
- Fiscal quarter = `((month + 8) % 12) / 3 + 1` with integer division. April-June = Q1, Jan-Mar = Q4.
- Shortcut in MySQL/SQL Server: shift the date back 3 months, then use the normal YEAR/QUARTER: `YEAR(DATE_SUB(d, INTERVAL 3 MONTH))` (not run here).
**Example:** Sale on 20 March 2025 is FY2024-25 Q4; sale on 5 April 2025 is FY2025-26 Q1.
**Sample data:**
| sale_date | amount |
|---|---|
| 2025-03-20 | 100 |
| 2025-04-05 | 200 |
| 2025-06-18 | 150 |
| 2025-07-02 | 120 |
| 2025-12-25 | 300 |
| 2026-01-10 | 80 |
| 2026-03-31 | 60 |
**SQL:**
```sql
WITH x AS (
    SELECT amount,
           CAST(strftime('%Y', sale_date) AS INT) AS yr,
           CAST(strftime('%m', sale_date) AS INT) AS mon
    FROM sales2
)
SELECT 'FY' || fy_start || '-' || substr(fy_start + 1, 3, 2) AS fiscal_year,
       'Q' || (((mon + 8) % 12) / 3 + 1)                  AS fiscal_quarter,
       SUM(amount) AS total_sales
FROM (SELECT *, CASE WHEN mon >= 4 THEN yr ELSE yr - 1 END AS fy_start FROM x)
GROUP BY fy_start, fiscal_quarter
ORDER BY fy_start, fiscal_quarter
```
**Output:**
| fiscal_year | fiscal_quarter | total_sales |
|---|---|---|
| FY2024-25 | Q4 | 100 |
| FY2025-26 | Q1 | 350 |
| FY2025-26 | Q2 | 120 |
| FY2025-26 | Q3 | 300 |
| FY2025-26 | Q4 | 140 |
**pandas equivalent:**
```python
d = pd.to_datetime(s2.sale_date)
fy = np.where(d.dt.month >= 4, d.dt.year, d.dt.year - 1)
s2['fiscal_year'] = ['FY%d-%02d' % (y, (y + 1) % 100) for y in fy]
s2['fiscal_quarter'] = ['Q%d' % (((m + 8) % 12) // 3 + 1) for m in d.dt.month]
res = s2.groupby(['fiscal_year', 'fiscal_quarter'], as_index=False).amount.sum().rename(columns={'amount': 'total_sales'})
# pandas shortcut: d.dt.to_period('Q-MAR')
# result matches the SQL output (checked)
```
**Edge cases:** The `/` must be integer division (true in SQLite, MySQL needs DIV, PostgreSQL integers truncate, SQL Server integers truncate). Dates with NULL give NULL group. Quarters with no sales are missing.
**Likely follow-ups:**
- What if the fiscal year ends in September? Change the 4 and the shift.
- How to sort the labels correctly? Sort by fy_start, not the text.
**Common mistakes:** Using YEAR(date) directly, and getting the quarter by calendar month.

### Q49 ⭐ 🟡 How do you find a character's position inside a string (CHARINDEX, POSITION, INSTR)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the position-finding function name in each dialect and that positions start at 1 (0 means not found)?
**Say this in the interview:** INSTR in MySQL/SQLite/Oracle, POSITION or STRPOS in PostgreSQL, CHARINDEX in SQL Server. They return the 1-based position, and 0 when the text is not found.
**Explain simply:**
- MySQL: `INSTR(str, sub)` or `LOCATE(sub, str)`. PostgreSQL: `POSITION(sub IN str)` / `STRPOS(str, sub)`. SQL Server: `CHARINDEX(sub, str)` (note sub comes first). SQLite: `INSTR(str, sub)`. Only the SQLite form was run.
- Position 1 means the first character, so e.g. 'asha@acme.com' has '@' at position 5.
- Combine with SUBSTRING to cut text before/after the character (Q30, Q31).
- pandas `find` is 0-based and returns -1 for not found, so add 1.
**Example:** In asha@acme.com the @ is the 5th character.
**Sample data:**
| emp_id | email |
|---|---|
| 1 | asha@acme.com |
| 2 | bala@gmail.com |
| 3 | chitra@acme.com |
| 4 | deepak@acme.com |
**SQL:**
```sql
SELECT email, INSTR(email, '@') AS at_position, SUBSTR(email, INSTR(email, '@') + 1) AS domain FROM emp WHERE emp_id <= 4
```
**Output:**
| email | at_position | domain |
|---|---|---|
| asha@acme.com | 5 | acme.com |
| bala@gmail.com | 5 | gmail.com |
| chitra@acme.com | 7 | acme.com |
| deepak@acme.com | 7 | acme.com |
**pandas equivalent:**
```python
res = pd.DataFrame({'email': e4.email, 'at_position': e4.email.str.find('@') + 1, 'domain': e4.email.str.split('@').str[1]})
# result matches the SQL output (checked)
```
**Edge cases:** Not found returns 0 in SQL; pandas find gives -1, so +1 also maps it to 0. NULL input gives NULL. Case sensitivity of the search depends on collation (MySQL/SQL Server default case-insensitive; PostgreSQL case-sensitive). Only the first occurrence is returned.
**Likely follow-ups:**
- How to find the second occurrence? Pass a start position (`CHARINDEX(sub, str, start)`) or use regex.
- Does it work with multi-byte text? Most count characters, but SQL Server `CHARINDEX` follows column collation.
**Common mistakes:** Mixing up argument order (CHARINDEX sub first, INSTR string first) and treating 0 as a valid position.

### Q50 ⭐ 🟡 How do you count occurrences of a character in a string?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the length-minus-replaced-length trick for counting a character?
**Say this in the interview:** I measure the string, remove every occurrence of the character with REPLACE, measure again, and the difference is the count. For a longer substring I divide by its length.
**Explain simply:**
- Length 13 before, 12 after removing one dot means 1 dot.
- For a substring such as 'ab': `(LENGTH(s) - LENGTH(REPLACE(s,'ab',''))) / LENGTH('ab')`.
- SQL Server uses `LEN`, which ignores trailing spaces; use `DATALENGTH` for bytes (from memory). PostgreSQL also has `LENGTH`; MySQL `CHAR_LENGTH` counts characters while `LENGTH` counts bytes.
- Regex counting exists in some engines (Oracle `REGEXP_COUNT`, not run here).
**Example:** 'esha@outlook.in' has 1 dot; 'asha@acme.com' has 1 dot; a value like 'a.b.c@x.com' has 3.
**Sample data:**
| emp_id | email |
|---|---|
| 1 | asha@acme.com |
| 3 | chitra@acme.com |
| 4 | deepak@acme.com |
| 5 | esha@outlook.in |
**SQL:**
```sql
SELECT email, LENGTH(email) - LENGTH(REPLACE(email, '.', '')) AS dot_count FROM emp WHERE emp_id IN (1,3,4,5)
```
**Output:**
| email | dot_count |
|---|---|
| asha@acme.com | 1 |
| chitra@acme.com | 1 |
| deepak@acme.com | 1 |
| esha@outlook.in | 1 |
**pandas equivalent:**
```python
res = pd.DataFrame({'email': e.email, 'dot_count': e.email.str.count(r'\.')})
# result matches the SQL output (checked)
```
**Edge cases:** NULL gives NULL. Case matters in REPLACE (counting 'a' will not count 'A') in most engines. Overlapping patterns are not counted twice.
**Likely follow-ups:**
- How to count words? Count spaces + 1 after trimming.
- Does the trick work for emojis? Byte vs character length functions can differ.
**Common mistakes:** Forgetting to divide by the substring length, and using byte length on multi-byte text.

### Q51 ⭐ 🟡 How do you use REGEXP / regular expressions to validate emails or phone numbers?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know regex support differs sharply by dialect, and can you write a simple pattern?
**Say this in the interview:** A regular expression is a pattern language for text. MySQL uses REGEXP, PostgreSQL uses the ~ operator, SQL Server has no regex (use LIKE or PATINDEX), and I would keep the pattern simple and document its limits.
**Explain simply:**
- Pattern parts: `^` start, `$` end, `[0-9]{5}` exactly five digits, `+` one or more, `\.` a real dot.
- MySQL: `email REGEXP 'pattern'`. PostgreSQL: `email ~ 'pattern'` (`~*` ignores case). Oracle: `REGEXP_LIKE`. DuckDB (run here): `regexp_matches`. SQL Server: no native regex until recent previews (from memory), so use LIKE/PATINDEX. Only DuckDB was run; SQLite has no built-in REGEXP.
- Regex validates shape only: it cannot tell if the mailbox exists.
- Use it to flag dirty data in a staging table before loading it.
**Example:** Flag HR records where the phone is not 5 digits, a dash, then 5 digits.
**Sample data:**
| name | email | phone |
|---|---|---|
| Asha | asha@acme.com | 98765-43210 |
| Bala | bala@gmail | 91234-56789 |
| Chitra | chitra@acme.com | 99999 00000 |
| Deepak | deepak@@acme.com | 9876543210 |
| Esha | esha@outlook.in | 77777-22222 |
**SQL:**
```sql
SELECT name, email, phone,
       regexp_matches(email, '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$') AS email_ok,
       regexp_matches(phone, '^[0-9]{5}-[0-9]{5}$')                              AS phone_ok
FROM contacts
```
**Output:**
| name | email | phone | email_ok | phone_ok |
|---|---|---|---|---|
| Asha | asha@acme.com | 98765-43210 | 1 | 1 |
| Bala | bala@gmail | 91234-56789 | 0 | 1 |
| Chitra | chitra@acme.com | 99999 00000 | 1 | 0 |
| Deepak | deepak@@acme.com | 9876543210 | 0 | 0 |
| Esha | esha@outlook.in | 77777-22222 | 1 | 1 |
**pandas equivalent:**
```python
res = ct.copy()
res['email_ok'] = ct.email.str.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
res['phone_ok'] = ct.phone.str.match(r'^[0-9]{5}-[0-9]{5}$')
# result matches the SQL output (checked)
```
**Edge cases:** NULL input gives NULL (not true or false). Backslash escaping differs (MySQL needs doubled backslashes in strings; PostgreSQL standard strings do not). Case sensitivity and Unicode behaviour vary. Complex patterns are slow and cannot use indexes.
**Likely follow-ups:**
- Is regex index friendly? No, it usually scans.
- Simpler alternative? LIKE '%@%.%' as a rough check.
**Common mistakes:** Expecting one regex syntax everywhere, and over-engineering the email pattern.

### Q52 ⭐ 🟡 How do you aggregate strings (GROUP_CONCAT, STRING_AGG, LISTAGG)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the name of the string aggregate in each dialect and how to order it?
**Say this in the interview:** It joins the values of a group into one text value: GROUP_CONCAT in MySQL and SQLite, STRING_AGG in PostgreSQL and SQL Server, LISTAGG in Oracle.
**Explain simply:**
- This is an aggregate function (like SUM), but it glues text instead of adding.
- MySQL: `GROUP_CONCAT(name ORDER BY name SEPARATOR ', ')`. PostgreSQL: `STRING_AGG(name, ', ' ORDER BY name)`. SQL Server 2017+: `STRING_AGG(name, ', ') WITHIN GROUP (ORDER BY name)`. Oracle: `LISTAGG(name, ', ') WITHIN GROUP (ORDER BY name)`. Only SQLite (shown) was run.
- MySQL truncates at `group_concat_max_len` (default 1024 bytes, from memory) - a silent trap.
- SQLite: `GROUP_CONCAT(x, sep ORDER BY ...)` needs 3.44+.
**Example:** List all HR people in one cell for a report: 'Chitra, Deepak'.
**Sample data:**
| dept | name |
|---|---|
| Sales | Asha |
| Sales | Bala |
| HR | Chitra |
| HR | Deepak |
| IT | Esha |
| IT | Farhan |
| IT | Gita |
**SQL:**
```sql
SELECT dept, GROUP_CONCAT(name, ', ' ORDER BY name) AS employees FROM emp GROUP BY dept ORDER BY dept
```
**Output:**
| dept | employees |
|---|---|
| HR | Chitra, Deepak |
| IT | Esha, Farhan, Gita |
| Sales | Asha, Bala |
**pandas equivalent:**
```python
res = emp.sort_values('name').groupby('dept', as_index=False).name.agg(', '.join).rename(columns={'name': 'employees'})
# result matches the SQL output (checked)
```
**Edge cases:** NULL values are skipped; if all are NULL the result is NULL. Duplicates are kept (use DISTINCT). Without ORDER BY the order is not guaranteed. Very long results can be cut off (MySQL).
**Likely follow-ups:**
- How to remove duplicates? `STRING_AGG(DISTINCT ...)` in PostgreSQL.
- Reverse operation? Split text into rows (STRING_SPLIT, `unnest(string_to_array())`).
**Common mistakes:** Assuming the concatenated order is sorted, and hitting the MySQL length limit.

### Q53 ⭐ 🟡 What is the difference between DATE, DATETIME and TIMESTAMP data types?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know what each type stores, its range and its time-zone behaviour, which differ by dialect?
**Say this in the interview:** DATE holds only a day, DATETIME holds day plus time with no time zone, and TIMESTAMP is time-zone aware or UTC-based depending on the database.
**Explain simply:**
- DATE: calendar day only, e.g. 2025-03-10. Use for joining date or birthday.
- DATETIME / `timestamp without time zone`: day and time as written, no zone info. MySQL DATETIME range is 1000-9999 (from memory).
- MySQL TIMESTAMP: stored in UTC and shown in the session time zone; range only 1970 to 2038 (from memory). PostgreSQL has `timestamp` and `timestamptz` (the latter converts to UTC); it has no DATETIME. SQL Server has `date`, `datetime`, `datetime2` (more precise, preferred) and `datetimeoffset`; its `timestamp` is an unrelated row-version counter.
- Rule of thumb: store event times in UTC with a zone-aware type; store pure calendar facts as DATE.
**Example:** Joining date 2021-03-15 is a DATE; a login at 2025-03-10 09:15:00 IST is a timestamp.
**SQL:**
```sql
-- PostgreSQL syntax, not run here
CREATE TABLE login_log (
    emp_id   INT,
    work_day DATE,          -- 2025-03-10
    login_at TIMESTAMPTZ    -- 2025-03-10 09:15:00+05:30
);
-- MySQL: login_at DATETIME or TIMESTAMP;  SQL Server: login_at DATETIME2 or DATETIMEOFFSET
```
**Edge cases:** Comparing a DATETIME to a DATE treats the date as midnight, so rows later that day are missed (Q54). SQLite has no true date types; it stores text/numbers. Inserting an out-of-range date errors or gives zero-date in lenient MySQL modes.
**Likely follow-ups:**
- Which should I use for audit logs? A zone-aware type in UTC.
- Does DATETIME2 differ from DATETIME in SQL Server? More range and precision.
**Common mistakes:** Believing TIMESTAMP is the same everywhere, and using DATETIME for events across time zones.

### Q54 ⭐ 🟡 How do you compare timestamps while ignoring the time part (e.g., filter a full day)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the half-open range pattern and why BETWEEN fails with timestamps?
**Say this in the interview:** I filter with start <= ts and ts < next day, so the whole day is covered and the next midnight is excluded. That also lets an index on the column be used.
**Explain simply:**
- '2025-03-10' is read as 2025-03-10 00:00:00, so `BETWEEN '2025-03-10' AND '2025-03-10'` matches only midnight.
- `BETWEEN ... AND '2025-03-10 23:59:59'` misses 23:59:59.5 on fractional-second columns and is fragile.
- Casting the column (`CAST(ts AS DATE) = '2025-03-10'`, or `DATE(ts)`) works but wraps the column in a function, which hurts index use (Q56).
- Same shape in MySQL, PostgreSQL, SQL Server; only the next-day arithmetic differs (`+ INTERVAL 1 DAY`, `+ INTERVAL '1 day'`, `DATEADD(day,1,...)`).
**Example:** Count how many people logged in on 10 March 2025: 3 rows (00:00, 09:15, 23:59:59).
**Sample data:**
| user_id | login_ts |
|---|---|
| 1 | 2025-03-09 18:30:00 |
| 2 | 2025-03-10 00:00:00 |
| 3 | 2025-03-10 09:15:00 |
| 4 | 2025-03-10 23:59:59 |
| 5 | 2025-03-11 00:00:00 |
**SQL:**
```sql
-- wrong: BETWEEN '2025-03-10' AND '2025-03-10' only matches exactly midnight
SELECT COUNT(*) AS wrong_count
FROM logins WHERE login_ts BETWEEN '2025-03-10' AND '2025-03-10';

-- right: half-open range, start inclusive, next day exclusive
SELECT user_id, login_ts
FROM logins
WHERE login_ts >= '2025-03-10'
  AND login_ts <  '2025-03-11'
```
**Output:**
| wrong_count |
|---|
| 0 |

| user_id | login_ts |
|---|---|
| 2 | 2025-03-10 00:00:00 |
| 3 | 2025-03-10 09:15:00 |
| 4 | 2025-03-10 23:59:59 |
**pandas equivalent:**
```python
res = lg[(lg.t >= '2025-03-10') & (lg.t < '2025-03-11')][['user_id', 'login_ts']]
# result matches the SQL output (checked)
```
**Edge cases:** NULL timestamps never match. Time zones can shift which day a row belongs to (Q59). A pure DATE column can use plain equality.
**Likely follow-ups:**
- Why is exclusive end better? No rounding gaps, works for any precision.
- How for a whole month? `>= '2025-03-01' AND < '2025-04-01'`.
**Common mistakes:** Using BETWEEN with a date-only end value, and using 23:59:59 as the end.

### Q55 ⭐ 🟡 How do you use nested CASE WHEN? When should you avoid it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you nest CASE correctly and do you know when to flatten it or use a lookup table?
**Say this in the interview:** A CASE can sit inside a branch of another CASE. I use it for two-level rules, but if it goes beyond two levels I flatten it with AND conditions or move the rules to a mapping table.
**Explain simply:**
- Nested CASE = an inner CASE returned as the result of an outer branch. Each CASE needs its own END.
- Flattening: put both conditions in one WHEN with AND. Same answer, easier to read; the demo shows both columns are identical.
- CASE is evaluated top to bottom and the first true WHEN wins, so order matters. No ELSE gives NULL.
- Avoid deep nesting when rules change often or exceed ~5 branches: store thresholds in a table and JOIN.
**Example:** IT earning 80,000+ is 'IT-Senior', HR earning 50,000+ is 'HR-Senior'.
**Sample data:**
| name | dept | salary |
|---|---|---|
| Asha | Sales | 52000 |
| Bala | Sales | 48000 |
| Chitra | HR | 61000 |
| Deepak | HR | 45000 |
| Esha | IT | 90000 |
| Farhan | IT | 75000 |
| Gita | IT | 82000 |
**SQL:**
```sql
SELECT name, dept, salary,
       CASE WHEN dept = 'IT' THEN
                CASE WHEN salary >= 80000 THEN 'IT-Senior' ELSE 'IT-Regular' END
            WHEN dept = 'HR' THEN
                CASE WHEN salary >= 50000 THEN 'HR-Senior' ELSE 'HR-Regular' END
            ELSE 'Other'
       END AS band_nested,
       CASE WHEN dept = 'IT' AND salary >= 80000 THEN 'IT-Senior'
            WHEN dept = 'IT'                      THEN 'IT-Regular'
            WHEN dept = 'HR' AND salary >= 50000 THEN 'HR-Senior'
            WHEN dept = 'HR'                      THEN 'HR-Regular'
            ELSE 'Other'
       END AS band_flat
FROM emp
```
**Output:**
| name | dept | salary | band_nested | band_flat |
|---|---|---|---|---|
| Asha | Sales | 52000 | Other | Other |
| Bala | Sales | 48000 | Other | Other |
| Chitra | HR | 61000 | HR-Senior | HR-Senior |
| Deepak | HR | 45000 | HR-Regular | HR-Regular |
| Esha | IT | 90000 | IT-Senior | IT-Senior |
| Farhan | IT | 75000 | IT-Regular | IT-Regular |
| Gita | IT | 82000 | IT-Senior | IT-Senior |
**pandas equivalent:**
```python
def band(r):
    if r.dept == 'IT': return 'IT-Senior' if r.salary >= 80000 else 'IT-Regular'
    if r.dept == 'HR': return 'HR-Senior' if r.salary >= 50000 else 'HR-Regular'
    return 'Other'
emp['band'] = emp.apply(band, axis=1)
# columns band_nested and band_flat in the SQL output are identical (checked)
```
**Edge cases:** NULL salary makes `salary >= 80000` unknown, so it falls to ELSE (IT-Regular here). Mixed result types across branches may error in strict engines. Overlapping WHENs hide later ones.
**Likely follow-ups:**
- Is CASE short-circuit? Evaluated in order, but do not rely on it to prevent errors in all engines.
- Alternative? Lookup table with JOIN.
**Common mistakes:** Forgetting an END, putting broader conditions first, and mixing data types in branches.

### Q56 ⭐ 🟡 Why is wrapping a date column in a function (YEAR(col)=2025) bad for speed, and what is the better filter?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand sargability: a condition the index can use?
**Say this in the interview:** If I wrap the column in a function, the database must compute it for every row and cannot use the index on the column. I compare the raw column to a date range instead.
**Explain simply:**
- An index is like a sorted phone book of one column. Searching 'Smith' is quick; searching 'names whose 3rd letter is m' needs reading every entry.
- `WHERE YEAR(order_date) = 2025` hides the column inside a function, so the engine scans the whole table (a full scan).
- Sargable (search-argument-able) version: `order_date >= '2025-01-01' AND order_date < '2026-01-01'`.
- Same principle: avoid `col + 1 = 5`, `LEFT(col,3)='abc'` (use `LIKE 'abc%'`), and leading-% LIKE. SQL Server and PostgreSQL can use function-based indexes if needed (from memory).
**Example:** On a 10-million-row order table, the YEAR() filter reads all rows; the range filter jumps straight to 2025.
**SQL:**
```sql
CREATE TABLE orders(order_id INT, order_date TEXT, amount INT);
CREATE INDEX idx_orders_date ON orders(order_date);

-- slow shape
EXPLAIN QUERY PLAN
SELECT amount FROM orders WHERE strftime('%Y', order_date) = '2025';

-- fast shape
EXPLAIN QUERY PLAN
SELECT amount FROM orders WHERE order_date >= '2025-01-01' AND order_date < '2026-01-01';
```
**Output:**
Query plans from SQLite (499 rows):

| Filter style | Plan |
|---|---|
| function on column | SCAN orders |
| date range | SEARCH orders USING INDEX idx_orders_date (order_date>? AND order_date<?) |
**Edge cases:** Small tables may be scanned anyway. A function-based/computed index can make the first form fast. Statistics and data distribution affect the plan. Implicit conversions also break index use (Q58).
**Likely follow-ups:**
- How to check? Look at the execution plan (EXPLAIN / SHOW PLAN).
- Is `BETWEEN` fine? Yes for dates, but beware time parts (Q54).
**Common mistakes:** Wrapping the indexed column in YEAR/MONTH/DATE/CAST, and testing only on a tiny table.

### Q57 ⭐ 🟡 How do you detect and clean inconsistent text values (e.g., 'Hyd', 'hyderabad ') in a city column?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you spot dirty categories by grouping, then standardise them with TRIM, LOWER and a mapping?
**Say this in the interview:** First I group by the raw value to see every variant, then I standardise with TRIM and LOWER and map known short forms to one name; for a long list I use a mapping table.
**Explain simply:**
- Detect: GROUP BY the column and eyeball the distinct values; also compare `COUNT(DISTINCT city)` to `COUNT(DISTINCT LOWER(TRIM(city)))`.
- Clean: `LOWER(TRIM(city))` fixes case and stray spaces; abbreviations like 'hyd' need CASE or a lookup table.
- A mapping table (raw_value, clean_value) joined to the data is auditable and reusable.
- Fix at source with validation (drop-downs) where possible.
**Example:** The 7 employees show as 5 different city strings, but after cleaning only 2 cities remain (see output).
**Sample data:**
| emp_id | name | city |
|---|---|---|
| 1 | Asha | Hyderabad |
| 2 | Bala | hyd  |
| 3 | Chitra | Hyderabad |
| 4 | Deepak | Bengaluru |
| 5 | Esha | Hyderabad |
| 6 | Farhan | HYDERABAD |
| 7 | Gita | Hyd |
**SQL:**
```sql
-- detect
SELECT city, COUNT(*) AS employees FROM emp GROUP BY city ORDER BY city;

-- clean
SELECT CASE WHEN LOWER(TRIM(city)) IN ('hyd', 'hyderabad') THEN 'Hyderabad'
            ELSE city
       END AS clean_city,
       COUNT(*) AS employees
FROM emp
GROUP BY clean_city
ORDER BY employees DESC
```
**Output:**
| city | employees |
|---|---|
| Bengaluru | 1 |
| HYDERABAD | 1 |
| Hyd | 1 |
| Hyderabad | 3 |
| hyd  | 1 |

After cleaning:

| clean_city | employees |
|---|---|
| Hyderabad | 6 |
| Bengaluru | 1 |
**pandas equivalent:**
```python
cm = emp.city.str.strip().str.lower().replace({'hyd': 'hyderabad'}).str.title()
res = cm.value_counts().rename_axis('clean_city').reset_index(name='employees')
# result matches the SQL output (checked)
```
**Edge cases:** NULL city stays NULL as its own group. Non-breaking spaces survive TRIM. Case sensitivity of GROUP BY depends on collation (MySQL/SQL Server default case-insensitive, PostgreSQL sensitive). Genuine different places with similar spelling must not be merged blindly.
**Likely follow-ups:**
- Should I UPDATE the table? Only after backing up and reviewing; often better to clean in a view.
- Misspellings? Use fuzzy matching outside SQL, or a mapping table.
**Common mistakes:** Assuming GROUP BY merges case variants everywhere, and hard-coding dozens of CASE branches.

### Q58 ⭐ 🟡 What is implicit type conversion and how can it cause wrong results in comparisons?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know that databases silently convert types and that rules differ, producing wrong rows or slow scans?
**Say this in the interview:** Implicit conversion is when the database changes a type on its own to compare two values. It can compare numbers as text or convert every row of a column, giving wrong results or killing index use, so I CAST explicitly.
**Explain simply:**
- Text sorts character by character: '10' comes before '9'. A text column compared to a number may be compared as text or as numbers depending on the engine.
- In SQLite, comparing a TEXT column to the number 5 converts 5 to '5', so `'10' > '5'` is false. Shown below.
- MySQL converts strings to numbers loosely: `'abc' = 0` and `'1abc' = 1` are true (from memory, not run here). PostgreSQL is stricter and errors on text vs integer. SQL Server converts by data-type precedence, which can convert the whole column and prevent an index seek (from memory).
- Fix the schema (store numbers as numbers) and CAST explicitly.
**Example:** A zip or employee code stored as text: finding codes above 5 returns only 9 instead of 9, 10, 25, 100.
**Sample data:**
| code |
|---|
| 9 |
| 10 |
| 100 |
| 25 |
**SQL:**
```sql
-- code is stored as TEXT
SELECT code FROM codes ORDER BY code;                         -- text order

SELECT code FROM codes ORDER BY CAST(code AS INTEGER);        -- number order

SELECT code FROM codes WHERE code > 5;                        -- number 5 silently turned into text '5'

SELECT code FROM codes WHERE CAST(code AS INTEGER) > 5;       -- explicit, correct
```
**Output:**
- ORDER BY code (text order): 10, 100, 25, 9
- ORDER BY CAST(code AS INTEGER): 9, 10, 25, 100
- WHERE code > 5: 9
- WHERE CAST(code AS INTEGER) > 5: 9, 10, 100, 25
**Edge cases:** NULLs stay NULL. Dates stored as text compare correctly only in ISO yyyy-mm-dd format. CAST of bad text errors in PostgreSQL and SQL Server and gives 0 in SQLite (MySQL: 0 with a warning, from memory).
**Likely follow-ups:**
- How to find bad conversions safely? `TRY_CAST` (SQL Server) / `TRY_CONVERT`, `CAST ... DEFAULT ON CONVERSION ERROR` (Oracle), regex checks first.
- Why can it be slow? Conversion applied to each row blocks the index.
**Common mistakes:** Storing numbers or dates as text, comparing different types, and trusting the engine to guess.

### Q59 ⭐ 🔴 How do you handle time zones in timestamps (AT TIME ZONE, CONVERT_TZ)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand storing UTC and converting for display, and the syntax per dialect?
**Say this in the interview:** I store timestamps in UTC and convert to the viewer's zone only when reporting. PostgreSQL uses AT TIME ZONE, MySQL uses CONVERT_TZ, SQL Server uses AT TIME ZONE on datetimeoffset.
**Explain simply:**
- A time zone is an offset from UTC: India is +05:30 all year; New York changes with daylight saving. Always use named zones like 'Asia/Kolkata', not fixed offsets.
- PostgreSQL / DuckDB: `ts AT TIME ZONE 'Asia/Kolkata'` converts a timestamptz to local clock time (run here in DuckDB).
- MySQL: `CONVERT_TZ(ts,'UTC','Asia/Kolkata')` - needs the time-zone tables loaded, else returns NULL. SQL Server 2016+: `ts AT TIME ZONE 'UTC' AT TIME ZONE 'India Standard Time'`. Not run here / from memory.
- Day boundaries change with zone: 9 pm UTC on 10 March is already 11 March in India, so convert before grouping by day.
**Example:** A login at 09:00 UTC shows as 14:30 for a Hyderabad employee and 05:00 for New York in March 2025.
**SQL:**
```sql
SELECT TIMESTAMPTZ '2025-03-10 09:00:00+00' AT TIME ZONE 'Asia/Kolkata'     AS ist_local,
       TIMESTAMPTZ '2025-03-10 09:00:00+00' AT TIME ZONE 'America/New_York' AS new_york_local
```
**Output:**
| ist_local | new_york_local |
|---|---|
| 2025-03-10 14:30:00 | 2025-03-10 05:00:00 |
**pandas equivalent:**
```python
ts = pd.Timestamp('2025-03-10 09:00:00', tz='UTC')
print(ts.tz_convert('Asia/Kolkata'))      # 2025-03-10 14:30:00+05:30
print(ts.tz_convert('America/New_York'))  # 2025-03-10 05:00:00-04:00
```
**Edge cases:** Daylight-saving gaps and repeated hours make some local times missing or ambiguous. Naive timestamps (no zone) are guesses. Output printing depends on the session time zone setting.
**Likely follow-ups:**
- What to store? UTC plus, if needed, the user's zone name.
- Why NULL from CONVERT_TZ? Zone tables not loaded.
**Common mistakes:** Using fixed offsets (+5:30) for zones with daylight saving, and grouping by day before converting.

### Q60 ⭐ 🔴 How do you generate a continuous series of dates (calendar table) in each dialect?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you create a calendar on the fly in each dialect and use it to fill gaps?
**Say this in the interview:** I generate the dates with GENERATE_SERIES in PostgreSQL, or a recursive CTE in MySQL 8, SQL Server and SQLite, then LEFT JOIN my data so days with no rows show zero.
**Explain simply:**
- A calendar (date) table lists every day once, so gaps in the data become visible.
- PostgreSQL: `SELECT d::date FROM generate_series('2025-03-01'::date,'2025-03-07','1 day') d`. DuckDB: `generate_series(DATE '2025-03-01', DATE '2025-03-07', INTERVAL 1 DAY)`.
- MySQL 8 / SQL Server / SQLite: recursive CTE as run here. SQL Server needs `WITH` (no RECURSIVE keyword) and `DATEADD(day,1,d)`, plus `OPTION (MAXRECURSION 0)` for >100 days; MySQL 8 uses `DATE_ADD(d, INTERVAL 1 DAY)` (from memory, not run).
- For production reporting, keep a permanent calendar table with columns such as weekday, month, fiscal year, holiday flag.
**Example:** Sales exist for 4 of 7 days; the report must still show the 3 empty days as 0.
**Sample data:**
| sale_date | amount |
|---|---|
| 2025-03-01 | 100 |
| 2025-03-02 | 50 |
| 2025-03-02 | 70 |
| 2025-03-05 | 200 |
| 2025-03-07 | 90 |
**SQL:**
```sql
WITH RECURSIVE cal(d) AS (
    SELECT '2025-03-01'
    UNION ALL
    SELECT date(d, '+1 day') FROM cal WHERE d < '2025-03-07'
)
SELECT cal.d AS day, COALESCE(SUM(s.amount), 0) AS sales
FROM cal
LEFT JOIN daily_sales s ON s.sale_date = cal.d
GROUP BY cal.d
ORDER BY cal.d
```
**Output:**
| day | sales |
|---|---|
| 2025-03-01 | 100 |
| 2025-03-02 | 120 |
| 2025-03-03 | 0 |
| 2025-03-04 | 0 |
| 2025-03-05 | 200 |
| 2025-03-06 | 0 |
| 2025-03-07 | 90 |
**pandas equivalent:**
```python
res = ds.groupby('sale_date').amount.sum()
res.index = pd.to_datetime(res.index)
res = res.reindex(pd.date_range('2025-03-01', '2025-03-07'), fill_value=0).rename_axis('day').reset_index(name='sales')
# result matches the SQL output (checked)
```
**Edge cases:** Put filters on the right-hand table in the ON clause, not WHERE, or you lose zero days. Recursion limits: SQL Server 100 by default, MySQL `cte_max_recursion_depth` 1000 (from memory). Time parts in timestamps stop the equality join; cast to date first.
**Likely follow-ups:**
- Month-level series? Step by '+1 month'.
- Faster for decades of dates? Permanent calendar table with an index.
**Common mistakes:** Using an INNER JOIN or a WHERE on the data table, which removes the empty days.

