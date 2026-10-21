# Book 2 (SQL) - Part 10: Duplicates, Nth Highest, Gaps & Islands, Recursive CTE, Query Optimisation [P0]

**Target:** 40 questions | **Actual:** 43
**Scope:** Classic SQL puzzle forms only: de-duplication, Nth highest (with and without windows), gaps and islands, recursive CTE hierarchies, query optimisation/indexes. Generic top-N per group is Part 5; window running totals are Part 6.

### Q1 ⭐⭐⭐ 🟢 Find all duplicate rows (e.g., duplicate employee emails) in a table and how many times each appears.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know GROUP BY plus HAVING COUNT(*) > 1, and whether you handle NULLs.
**Say this in the interview:** I group by the column that should be unique, count the rows in each group, and keep only groups with a count above 1 using HAVING. HAVING is the filter that works after grouping.
**Explain simply:**
- **GROUP BY** puts rows with the same email into one bucket; **COUNT(*)** counts rows in each bucket.
- **WHERE** filters single rows before grouping; **HAVING** filters buckets after grouping. You cannot use COUNT(*) in WHERE.
- If you want the full duplicate rows (not just the email), join this result back to the table on email.
**Example:** HR finds 'asha@corp.com' on two employee records and 'ravi@corp.com' on two: someone was entered twice during onboarding.
**Sample data:**

`employees`

| emp_id | name | email | dept | salary |
|---|---|---|---|---|
| 1 | Asha | asha@corp.com | HR | 90000 |
| 2 | Ravi | ravi@corp.com | Sales | 90000 |
| 3 | Meena | meena@corp.com | Sales | 80000 |
| 4 | Karan | karan@corp.com | IT | 70000 |
| 5 | Divya | divya@corp.com | IT | 70000 |
| 6 | Asha K | asha@corp.com | HR | 60000 |
| 7 | Imran | NULL | Sales | 50000 |
| 8 | Neha | NULL | IT | 50000 |
| 9 | Ravi S | ravi@corp.com | Sales | 55000 |

**SQL:**
```sql
SELECT email, COUNT(*) AS times_seen
FROM employees
WHERE email IS NOT NULL          -- unknown emails are not 'duplicates'
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY times_seen DESC, email;
```

**Output:**

| email | times_seen |
|---|---|
| asha@corp.com | 2 |
| ravi@corp.com | 2 |

**pandas equivalent:**
```python
d = df[df["email"].notna()]
result = (d.groupby("email").size().reset_index(name="times_seen")
           .query("times_seen > 1")
           .sort_values(["times_seen","email"], ascending=[False, True]).reset_index(drop=True))
```
Result (actual run):
```text
        email  times_seen
asha@corp.com           2
ravi@corp.com           2
```

**Edge cases:** Two employees with a NULL email: GROUP BY puts all NULLs in one bucket, so without `email IS NOT NULL` you would get a fake 'duplicate' with 2 rows. Case or spaces ('Asha@corp.com ') make duplicates invisible; clean with `LOWER(TRIM(email))` first. In pandas `groupby` drops NaN keys by default, so it behaves like the filtered SQL.
**Likely follow-ups:**
- Show the full duplicate rows? `SELECT e.* FROM employees e JOIN (above query) d ON d.email = e.email`.
- Duplicates on several columns? See Q13.
**Common mistakes:** Putting `COUNT(*) > 1` in WHERE, selecting non-grouped columns, and forgetting NULLs.

### Q2 ⭐⭐⭐ 🟢 Find the second highest salary without using window functions (MAX with a subquery).
**Asked at:** Product / e-commerce and service MNC: Glassdoor interview reports (Myntra, Bengaluru, first round; Infosys, Hyderabad, technical round, about Jul 2025) mention a second-highest-salary question; anonymous, self-reported, so treat as indicative only.
**What the interviewer is checking:** Whether you can build a result from a subquery and handle ties at the top salary.
**Say this in the interview:** First find the maximum salary in a subquery, then take the maximum of everything strictly below it. That is the second highest distinct salary, and ties at the top do not confuse it.
**Explain simply:**
- A **subquery** is a query inside brackets whose answer feeds the outer query.
- The inner query returns 90000; the outer query asks 'biggest salary less than 90000'.
- Using `<` (strictly less) is what makes two people at 90000 count as one 'highest'.
- Needs no window functions, no LIMIT, so it works in every database.
**Example:** Salaries 90000, 90000, 80000: highest = 90000, second highest = 80000 (not 90000 again).
**Sample data:**

`employees`

| emp_id | name | email | dept | salary |
|---|---|---|---|---|
| 1 | Asha | asha@corp.com | HR | 90000 |
| 2 | Ravi | ravi@corp.com | Sales | 90000 |
| 3 | Meena | meena@corp.com | Sales | 80000 |
| 4 | Karan | karan@corp.com | IT | 70000 |
| 5 | Divya | divya@corp.com | IT | 70000 |
| 6 | Asha K | asha@corp.com | HR | 60000 |
| 7 | Imran | NULL | Sales | 50000 |
| 8 | Neha | NULL | IT | 50000 |
| 9 | Ravi S | ravi@corp.com | Sales | 55000 |

**SQL:**
```sql
SELECT MAX(salary) AS second_highest
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
```

**Output:**

| second_highest |
|---|
| 80000 |

**pandas equivalent:**
```python
s = df["salary"]
result = s[s < s.max()].max()
```
Result (actual run):
```text
80000
```

**Edge cases:** Only one distinct salary: the inner filter leaves no rows and MAX returns NULL (pandas gives NaN), which is the right 'does not exist' answer. NULL salaries are ignored by MAX. This returns the salary only, not who earns it; to get names, use `WHERE salary = (...)`.
**Likely follow-ups:**
- Third highest? Nest again, but use Q3 or Q6 for general N.
- Who earns it? Wrap the query: `SELECT name FROM employees WHERE salary = (this query)`.
**Common mistakes:** Using `<=` (returns the top salary), or `ORDER BY salary DESC LIMIT 1 OFFSET 1` without DISTINCT, which returns 90000 here because of the tie.

### Q3 ⭐⭐⭐ 🟢 Find the Nth highest salary using DENSE_RANK().
**Asked at:** commonly asked (no company-specific report found); Nth-highest is a standard question in public prep lists.
**What the interviewer is checking:** Whether you know window functions and why DENSE_RANK suits 'Nth highest'.
**Say this in the interview:** I rank salaries from high to low with DENSE_RANK, so ties share a rank and no number is skipped, then I keep the row where the rank equals N.
**Explain simply:**
- A **window function** adds a calculated column (here a rank) without collapsing rows.
- `OVER (ORDER BY salary DESC)` means: rank from the biggest salary down.
- **DENSE_RANK** gives equal salaries the same rank and the next rank is +1: 90000, 90000, 80000 become 1, 1, 2.
- `DISTINCT` returns one value even if many employees share that salary.
**Example:** Distinct salaries 90000, 80000, 70000, 60000, 55000, 50000: the 3rd highest is 70000, earned by two people.
**Sample data:**

`employees`

| emp_id | name | email | dept | salary |
|---|---|---|---|---|
| 1 | Asha | asha@corp.com | HR | 90000 |
| 2 | Ravi | ravi@corp.com | Sales | 90000 |
| 3 | Meena | meena@corp.com | Sales | 80000 |
| 4 | Karan | karan@corp.com | IT | 70000 |
| 5 | Divya | divya@corp.com | IT | 70000 |
| 6 | Asha K | asha@corp.com | HR | 60000 |
| 7 | Imran | NULL | Sales | 50000 |
| 8 | Neha | NULL | IT | 50000 |
| 9 | Ravi S | ravi@corp.com | Sales | 55000 |

**SQL:**
```sql
WITH ranked AS (
    SELECT salary,
           DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM employees
)
SELECT DISTINCT salary AS nth_highest
FROM ranked
WHERE rnk = 3;          -- change 3 to any N
```

**Output:**

| nth_highest |
|---|
| 70000 |

**pandas equivalent:**
```python
result = (df["salary"].drop_duplicates().sort_values(ascending=False)
          .reset_index(drop=True).iloc[[2]].rename("nth_highest").reset_index(drop=True))
# same idea with a rank: df["salary"].rank(method="dense", ascending=False)
```
Result (actual run):
```text
70000
```

**Edge cases:** If N is larger than the number of distinct salaries you get an empty result (no row), not NULL; wrap it in a scalar subquery if the app needs NULL (see Q7). NULL salaries sort first in PostgreSQL descending order (last in SQLite/MySQL), so filter `WHERE salary IS NOT NULL` first. Per department: add `PARTITION BY dept`.
**Likely follow-ups:**
- Return the employees, not just the value? Drop DISTINCT and select `name, salary`.
- Nth highest per department? Add `PARTITION BY dept` (Part 5 covers top-N per group).
**Common mistakes:** Using ROW_NUMBER or RANK (see Q4), or forgetting that N is counted over distinct salaries.

### Q4 ⭐⭐⭐ 🟢 Why do we use DENSE_RANK (not ROW_NUMBER or RANK) for the Nth highest salary when two people have the same salary?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you understand how the three ranking functions treat ties.
**Say this in the interview:** DENSE_RANK gives tied salaries the same rank and does not skip numbers, so rank 2 always means the second distinct salary. ROW_NUMBER breaks ties arbitrarily and RANK leaves a gap after ties.
**Explain simply:**
- **ROW_NUMBER**: 1, 2, 3, 4... always unique, even for equal salaries, so the 'second row' may still be a 90000 earner.
- **RANK**: ties share a rank, then the next rank jumps (1, 1, 3). Rank 2 may not exist at all.
- **DENSE_RANK**: ties share a rank, no jump (1, 1, 2).
- 'Second highest salary' means second highest *value*, which is exactly what DENSE_RANK counts.
**Example:** Two people earn 90000 and one earns 80000. The correct second highest is 80000.
**Sample data:** the `employees` table from Q1 (top salaries: 90000, 90000, 80000, 70000, 70000...).
**SQL:**
```sql
SELECT name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num,
       RANK()       OVER (ORDER BY salary DESC) AS rnk,
       DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rnk
FROM employees
ORDER BY salary DESC, emp_id;
```

**Output:**

| name | salary | row_num | rnk | dense_rnk |
|---|---|---|---|---|
| Asha | 90000 | 1 | 1 | 1 |
| Ravi | 90000 | 2 | 1 | 1 |
| Meena | 80000 | 3 | 3 | 2 |
| Karan | 70000 | 4 | 4 | 3 |
| Divya | 70000 | 5 | 4 | 3 |
| Asha K | 60000 | 6 | 6 | 4 |
| Ravi S | 55000 | 7 | 7 | 5 |
| Imran | 50000 | 8 | 8 | 6 |
| Neha | 50000 | 9 | 8 | 6 |

**Which row each function picks for 'second highest' (actual run):**
```sql
-- What each function returns for 'second highest'
WITH r AS (SELECT salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC) rn,
       RANK()       OVER (ORDER BY salary DESC) rk,
       DENSE_RANK() OVER (ORDER BY salary DESC) dr
  FROM employees)
SELECT 'ROW_NUMBER = 2' AS method, GROUP_CONCAT(salary) AS result FROM r WHERE rn = 2
UNION ALL SELECT 'RANK = 2',        GROUP_CONCAT(salary) FROM r WHERE rk = 2
UNION ALL SELECT 'DENSE_RANK = 2',  GROUP_CONCAT(salary) FROM r WHERE dr = 2;
```

| method | result |
|---|---|
| ROW_NUMBER = 2 | 90000 |
| RANK = 2 | NULL |
| DENSE_RANK = 2 | 80000 |

**Edge cases:** ROW_NUMBER is only right if salaries are guaranteed unique, which is rarely true. RANK is right only when you want 'the person at position N counting ties as sharing a place'.
**Likely follow-ups:**
- When would you use RANK? For competition-style results ('two golds, no silver').
- When ROW_NUMBER? De-duplication and picking exactly one row per group (Q5).
**Common mistakes:** Using `ROW_NUMBER() = 2` and silently returning 90000, or using `RANK() = 2` and getting an empty result.

### Q5 ⭐⭐⭐ 🟡 Delete duplicate rows from a table but keep exactly one copy of each (ROW_NUMBER with a CTE).
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can number rows inside groups and delete only the extras, safely.
**Say this in the interview:** I number the rows within each duplicate group with ROW_NUMBER, ordered by id so the oldest is number 1, then delete every row numbered above 1. I run it as a SELECT first to check what would go.
**Explain simply:**
- `PARTITION BY email` restarts the numbering for each email; `ORDER BY emp_id` decides who is number 1 (the survivor).
- Rows with `rn > 1` are the extra copies.
- A **CTE** (`WITH ... AS`) is a named temporary result that the next statement reads.
- Always preview with SELECT, take a backup, and use a transaction.
**Example:** 'asha@corp.com' appears for ids 1 and 6; 'ravi@corp.com' for ids 2 and 9. Ids 6 and 9 are removed, 1 and 2 stay.
**Sample data:**

`employees` (email column only matters here)

| emp_id | name | email |
|---|---|---|
| 1 | Asha | asha@corp.com |
| 2 | Ravi | ravi@corp.com |
| 3 | Meena | meena@corp.com |
| 4 | Karan | karan@corp.com |
| 5 | Divya | divya@corp.com |
| 6 | Asha K | asha@corp.com |
| 7 | Imran | NULL |
| 8 | Neha | NULL |
| 9 | Ravi S | ravi@corp.com |

**SQL:**
```sql
WITH numbered AS (
    SELECT emp_id,
           ROW_NUMBER() OVER (PARTITION BY email ORDER BY emp_id) AS rn
    FROM employees
    WHERE email IS NOT NULL      -- never treat unknown emails as duplicates
)
DELETE FROM employees
WHERE emp_id IN (SELECT emp_id FROM numbered WHERE rn > 1);
```

Dialect note (not run here, from memory): SQL Server can delete straight from the CTE (`DELETE FROM numbered WHERE rn > 1`, with `*` columns inside); MySQL 8 does not allow deleting from a CTE the same way, so use `DELETE e FROM employees e JOIN (...) d ON d.emp_id = e.emp_id`. The `IN (SELECT ...)` form above ran on SQLite.
**Output:** 2 rows deleted (ids 6 and 9). Table afterwards:

| emp_id | name | email |
|---|---|---|
| 1 | Asha | asha@corp.com |
| 2 | Ravi | ravi@corp.com |
| 3 | Meena | meena@corp.com |
| 4 | Karan | karan@corp.com |
| 5 | Divya | divya@corp.com |
| 7 | Imran | NULL |
| 8 | Neha | NULL |

**pandas equivalent:**
```python
result = (df[df["email"].isna() | ~df.duplicated(subset="email", keep="first")]
          .reset_index(drop=True))[["emp_id","name","email"]]
```
Result (actual run, same rows as the SQL left):
```text
 emp_id  name          email
      1  Asha  asha@corp.com
      2  Ravi  ravi@corp.com
      3 Meena meena@corp.com
      4 Karan karan@corp.com
      5 Divya divya@corp.com
      7 Imran            NaN
      8  Neha            NaN
```

**Edge cases:** Without `WHERE email IS NOT NULL`, all NULL emails fall into one group and id 8 would be deleted too: I ran that unsafe version and it left 6 rows instead of 7. Ties in `ORDER BY` make the survivor arbitrary, so use a unique tie-breaker like the id. If whole rows are identical and there is no id, see Q19.
**Likely follow-ups:**
- Keep the latest instead of the oldest? `ORDER BY updated_at DESC` (Q17).
- How to stop it recurring? Add a UNIQUE constraint on email (Q35).
**Common mistakes:** Running the DELETE without previewing, not partitioning by the right columns, and deleting NULL groups.

### Q6 ⭐⭐⭐ 🟡 Find the Nth highest salary without window functions (correlated subquery / COUNT DISTINCT).
**Asked at:** commonly asked (no company-specific report found); the COUNT DISTINCT correlated form appears in public prep blogs.
**What the interviewer is checking:** Whether you understand a correlated subquery and can do Nth-highest without window functions.
**Say this in the interview:** For each salary I count how many distinct salaries are higher. The Nth highest is the one with exactly N-1 higher distinct salaries.
**Explain simply:**
- A **correlated subquery** re-runs for every row of the outer query, using that row's value (`e1.salary`).
- `COUNT(DISTINCT ...)` counts different salaries once each, so ties do not inflate the count.
- Top salary has 0 higher; second has 1 higher; third has 2 higher.
- It is simple but slow on big tables (it compares every row with every other row). Window functions (Q3) scale better.
**Example:** For 70000: salaries above it are 90000 and 80000, so 2 distinct higher = third highest.
**Sample data:** the `employees` table from Q1.
**SQL:**
```sql
SELECT DISTINCT e1.salary AS nth_highest
FROM employees e1
WHERE (SELECT COUNT(DISTINCT e2.salary)
       FROM employees e2
       WHERE e2.salary > e1.salary) = 3 - 1;   -- N = 3, so 2 distinct salaries must be higher
```

Alternative (not run here, from memory): `SELECT TOP 1 salary FROM (SELECT DISTINCT TOP 3 salary FROM employees ORDER BY salary DESC) t ORDER BY salary` in SQL Server; `ORDER BY ... LIMIT 1 OFFSET 2` in MySQL/PostgreSQL/SQLite (see Q7).
**Output:**

| nth_highest |
|---|
| 70000 |

**pandas equivalent:**
```python
def nth(s, n):
    # count how many distinct salaries are higher, like the SQL does
    u = s.dropna().unique()
    return sorted(v for v in u if (u > v).sum() == n - 1)
result = pd.Series(nth(df["salary"], 3), name="nth_highest")
```
Result (actual run):
```text
70000
```

**Edge cases:** N larger than the count of distinct salaries returns no rows. NULL salaries: `x > NULL` is unknown, so a NULL-salary row counts 0 higher salaries and would be returned as the 'highest' when N = 1. Filter `salary IS NOT NULL` in the outer query to be safe.
**Likely follow-ups:**
- Why `DISTINCT` inside COUNT? Without it, ties push the count up and you skip a salary.
- Faster way? DENSE_RANK (Q3) or LIMIT/OFFSET (Q7).
**Common mistakes:** `COUNT(*)` instead of `COUNT(DISTINCT ...)`, `>=` instead of `>`, and an off-by-one (N versus N-1).

### Q7 ⭐⭐⭐ 🟡 Find the second highest salary using LIMIT/OFFSET, and return NULL when it does not exist.
**Asked at:** Product / e-commerce and service MNC: Glassdoor interview reports (Myntra, Bengaluru, first round; Infosys, Hyderabad, technical round, about Jul 2025) mention a second-highest-salary question; anonymous, self-reported, so treat as indicative only.
**What the interviewer is checking:** Whether you know LIMIT/OFFSET, DISTINCT for ties, and how to return NULL instead of an empty result.
**Say this in the interview:** I take the distinct salaries in descending order, skip one with OFFSET 1 and take one with LIMIT 1. I wrap that in a SELECT so that, if there is no second salary, the answer comes back as NULL instead of no rows.
**Explain simply:**
- `ORDER BY salary DESC` lines salaries up from highest; `OFFSET 1` skips the top one; `LIMIT 1` keeps the next.
- `DISTINCT` makes the tied 90000s count once.
- A query with no matching row returns an empty table, which many apps treat as an error. A **scalar subquery** (a query in brackets used as one value) turns 'no row' into NULL.
**Example:** A new team with one employee has no second highest salary, so the report should show NULL.
**Sample data:** the `employees` table from Q1, plus a one-row table `solo(salary)` holding 75000.
**SQL:**
```sql
SELECT (SELECT DISTINCT salary
        FROM employees
        ORDER BY salary DESC
        LIMIT 1 OFFSET 1) AS second_highest;   -- scalar subquery: no row => NULL
```

Dialect alternatives (not run here, from memory): SQL Server `SELECT (SELECT DISTINCT salary FROM employees ORDER BY salary DESC OFFSET 1 ROWS FETCH NEXT 1 ROWS ONLY)`; standard SQL / PostgreSQL 13+ / Oracle 12c+ `... OFFSET 1 ROW FETCH FIRST 1 ROW ONLY`; `TOP` cannot skip rows. MySQL and PostgreSQL accept the LIMIT form shown.
**Output:** on `employees`:

| second_highest |
|---|
| 80000 |

On the one-row table (same query, actual run):

| second_highest |
|---|
| NULL |

**pandas equivalent:**
```python
def second_highest(s):
    u = s.dropna().drop_duplicates().sort_values(ascending=False)
    return u.iloc[1] if len(u) > 1 else None
result = pd.DataFrame({"table": ["employees", "one-row table"],
    "second_highest": [second_highest(df["salary"]), second_highest(pd.Series([75000]))]})
```
Result (actual run):
```text
        table  second_highest
    employees         80000.0
one-row table             NaN
```

**Edge cases:** Without `DISTINCT` the OFFSET form returns 90000 here (tie). NULL salaries sort first in PostgreSQL descending order, so add `WHERE salary IS NOT NULL`. (From memory, not run here: MySQL rejects LIMIT inside an IN subquery, but a scalar subquery like this one is fine.)
**Likely follow-ups:**
- Nth instead of 2nd? Replace `OFFSET 1` with `OFFSET N-1` (OFFSET must be a number, so build the query in code).
- Which employees? Filter `WHERE salary = (this scalar)`.
**Common mistakes:** Forgetting DISTINCT, forgetting that OFFSET starts at 0, and returning an empty set instead of NULL.

### Q8 ⭐⭐⭐ 🟡 A query is running slowly. Walk through how you would optimise it.
**Asked at:** commonly asked (no company-specific report found); no source found for a company-specific optimisation round.
**What the interviewer is checking:** Whether you have a method (measure, read the plan, fix the biggest cost) rather than random tricks.
**Say this in the interview:** I first get the query plan to see where the time goes, usually a full table scan. Then I check the filters can use an index, select only the columns I need, reduce rows early, and re-check the plan and timing after each change.
**Explain simply:**
- **Step 1, measure:** note the current run time and row counts; look at the plan (Q9).
- **Step 2, fewer rows early:** filter in WHERE as soon as possible; avoid functions on filtered columns (Q10).
- **Step 3, index the filter/join columns:** an **index** is a sorted lookup list, like a book's index, that lets the database jump to rows instead of reading every page.
- **Step 4, fewer columns:** avoid `SELECT *` (Q15); avoid DISTINCT or ORDER BY you do not need.
- **Step 5, re-measure.** Indexes slow down inserts and updates and take space, so add only what the query needs. Refresh statistics (`ANALYZE`) if the plan looks wrong.
**Example:** HR table with 20,000 employees (generated test data); report: Sales hires since 1 Jan 2025. 366 rows match.
**Sample data:** `employees(emp_id, name, dept, hire_date, salary, emp_code)`, 20,000 generated rows (5 departments, hire dates 2015-2025, seed 7).
**SQL:**
```sql
-- the slow query
SELECT emp_id, salary FROM employees WHERE dept = 'Sales' AND hire_date >= '2025-01-01';

-- the fix
CREATE INDEX idx_dept_hire ON employees(dept, hire_date);
```
**Output:** real `EXPLAIN QUERY PLAN` from SQLite 3.45.1.

Before the index:
```text
SCAN employees
```
After the index:
```text
SEARCH employees USING INDEX idx_dept_hire (dept=? AND hire_date>?)
```
Reading it: SCAN means every row is read; SEARCH ... USING INDEX (dept=? AND hire_date>?) means the database jumps to the Sales rows and then walks only the 2025 dates (equality on the first column, range on the second, per the multi-column rule in the PostgreSQL docs, https://www.postgresql.org/docs/current/indexes-multicolumn.html).
**Edge cases:** On a tiny table a scan can be faster than an index, and the planner may choose it (MySQL docs say the same: https://dev.mysql.com/doc/refman/8.4/en/mysql-indexes.html). If the query returns most of the table, an index does not help. Stale statistics give bad plans. In PostgreSQL, compare estimated and actual rows in `EXPLAIN ANALYZE`; a big mismatch usually means run `ANALYZE` (https://www.postgresql.org/docs/current/using-explain.html).
**Likely follow-ups:**
- Index did not help, why? The filter uses a function or leading wildcard (Q10, Q28), or returns too many rows.
- Other levers? Rewrite correlated subqueries as joins (Q43), partition huge tables (Q40), pre-aggregate in a summary table.
**Common mistakes:** Adding indexes on every column, tuning without reading the plan, and testing on tiny data.

### Q9 ⭐⭐⭐ 🟡 What does EXPLAIN show, and how do you read a query plan (scan vs index lookup, cost, rows)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you can read a plan to see if the database scans everything or jumps through an index.
**Say this in the interview:** EXPLAIN shows the plan the database intends to use without (normally) running the query. I look for full scans versus index lookups, the join order, and in PostgreSQL the cost and estimated row counts.
**Explain simply:**
- **Seq/Full scan** (`SCAN` in SQLite): reads every row. **Index lookup** (`SEARCH ... USING INDEX`): jumps to matching rows.
- PostgreSQL reads like `cost=startup..total` in arbitrary units (not milliseconds) and `rows` = estimated rows. `Index Cond` is applied through the index; `Filter` is checked row by row. (From the PostgreSQL docs: https://www.postgresql.org/docs/current/using-explain.html)
- PostgreSQL `EXPLAIN ANALYZE` actually **runs** the statement and adds real time in ms and real row counts; wrap INSERT/UPDATE/DELETE in `BEGIN ... ROLLBACK`. Moderate selectivity can show a Bitmap Index/Heap Scan.
- SQLite's `EXPLAIN QUERY PLAN` is simpler: no costs or row estimates, just the access method. Syntax differs: `EXPLAIN` (PostgreSQL/MySQL), `EXPLAIN QUERY PLAN` (SQLite), `SET SHOWPLAN_ALL ON` or the graphical plan (SQL Server, from memory).
**Example:** The HR report 'employees in IT' on 20,000 rows: after indexing dept, the plan changes from SCAN to SEARCH.
**Sample data:** the 20,000-row `employees` table from Q8 with `PRIMARY KEY(emp_id)` and `CREATE INDEX idx_dept ON employees(dept)`.
**SQL:**
```sql
EXPLAIN QUERY PLAN SELECT * FROM employees WHERE dept = 'IT';   -- SQLite
-- PostgreSQL / MySQL (not run here): EXPLAIN SELECT ...;  EXPLAIN ANALYZE SELECT ...;
```
**Output (real SQLite plans):**

| Situation | Query | SQLite plan (actual run) |
|---|---|---|
| Filter on an unindexed column | `SELECT * FROM employees WHERE salary > 140000` | `SCAN employees` |
| Lookup by primary key | `SELECT * FROM employees WHERE emp_id = 500` | `SEARCH employees USING INTEGER PRIMARY KEY (rowid=?)` |
| Filter on an indexed column | `SELECT * FROM employees WHERE dept = 'IT'` | `SEARCH employees USING INDEX idx_dept (dept=?)` |
| Count answered from the index alone | `SELECT dept, COUNT(*) FROM employees GROUP BY dept` | `SCAN employees USING COVERING INDEX idx_dept` |
| Sort on an unindexed column | `SELECT * FROM employees ORDER BY salary DESC` | `SCAN employees ; USE TEMP B-TREE FOR ORDER BY` |

**Edge cases:** PostgreSQL costs are only comparable inside the same server and statistics. A big gap between estimated and actual rows means stale statistics (run `ANALYZE`). The plan can change as data grows.
**Likely follow-ups:**
- Is EXPLAIN ANALYZE safe on a DELETE? No, it executes it; use a transaction and ROLLBACK.
- What is a covering index? Q39.
**Common mistakes:** Reading cost as seconds, trusting a plan from a tiny test table, and running EXPLAIN ANALYZE on writes.

### Q10 ⭐⭐⭐ 🟡 When will a database NOT use an index? (Functions on columns, type mismatch, non-sargable filters.)
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know 'sargable' rules: the database can use an index only when the bare column is compared directly.
**Say this in the interview:** An index is sorted by the raw column value. If I wrap the column in a function, do math on it, or start a LIKE with a wildcard, the database cannot use that sorted order, so it scans every row. I keep the column bare and move the work to the other side.
**Explain simply:**
- **Sargable** = 'search-argument-able': the filter can use an index.
- Non-sargable: `YEAR(hire_date) = 2025`, `salary * 12 > ...`, `name LIKE '%99'`, `COALESCE(col, 0) = 5`.
- **Type mismatch**: comparing a text column to a number can force a conversion of every row in some databases (MySQL and PostgreSQL can behave this way; from memory, not run here). I ran it on SQLite and the index was still used, because SQLite applies the column's type to the value: do not assume the same elsewhere.
- Other reasons: the table is tiny or the filter matches most rows (scan is cheaper), stale statistics, or the query uses a column that is not the leftmost of a composite index (Q27).
**Example:** 'Employees hired in 2025' written as `strftime('%Y', hire_date) = '2025'` scans 20,000 rows; as a date range it jumps straight in.
**Sample data:** the 20,000-row `employees` table from Q8 with indexes on `hire_date`, `name`, `salary`, `emp_code`.
**SQL:**
```sql
EXPLAIN QUERY PLAN SELECT * FROM employees WHERE strftime('%Y', hire_date) = '2025';   -- scan
EXPLAIN QUERY PLAN SELECT * FROM employees WHERE hire_date >= '2025-01-01' AND hire_date < '2026-01-01';  -- index
-- PostgreSQL/MySQL equivalent function version: WHERE EXTRACT(YEAR FROM hire_date) = 2025 (not run here)
```
**Output (real SQLite plans):**

| Case | Query | SQLite plan (actual run) |
|---|---|---|
| Function on the column | `SELECT * FROM employees WHERE strftime('%Y', hire_date) = '2025'` | `SCAN employees` |
| Range on the bare column | `SELECT * FROM employees WHERE hire_date >= '2025-01-01' AND hire_date < '2026-01-01'` | `SEARCH employees USING INDEX idx_hire (hire_date>? AND hire_date<?)` |
| Arithmetic on the column | `SELECT * FROM employees WHERE salary * 12 > 1800000` | `SCAN employees` |
| Move the math to the other side | `SELECT * FROM employees WHERE salary > 1800000 / 12` | `SEARCH employees USING INDEX idx_sal (salary>?)` |
| Leading wildcard | `SELECT * FROM employees WHERE name LIKE '%99'` | `SCAN employees` |
| No leading wildcard (see note) | `SELECT * FROM employees WHERE name >= 'emp99' AND name < 'emp9:'` | `SEARCH employees USING INDEX idx_name (name>? AND name<?)` |
| Number compared with a text column | `SELECT * FROM employees WHERE emp_code = 100500` | `SEARCH employees USING INDEX idx_code (emp_code=?)` |

Notes from the run: a plain `LIKE 'emp99%'` still showed a scan in SQLite 3.45.1 here, because its LIKE optimisation needs case-insensitive-compatible settings; the range rewrite shown above does use the index. PostgreSQL can use a B-tree for `LIKE 'abc%'` only with a suitable operator class or C collation (from memory, not run here); see Q28.
**Edge cases:** PostgreSQL can index an expression (`CREATE INDEX ON employees ((EXTRACT(YEAR FROM hire_date)))`) so a function filter becomes usable; SQLite also supports expression indexes (not run here).
**Likely follow-ups:**
- Can you fix a function filter without rewriting? Create an expression index (above).
- Does OR kill indexes? Sometimes; modern planners can union indexes, check the plan.
**Common mistakes:** `WHERE YEAR(date) = ...`, `WHERE col + 1 = ...`, `LIKE '%x'`, and assuming 'indexed' means 'always used'.

### Q11 ⭐⭐⭐ 🔴 Using a recursive CTE, list all direct and indirect reports of a given manager from an employee table (employee_id, manager_id).
**Asked at:** commonly asked (no company-specific report found); no source found for a company-specific recursive CTE round.
**What the interviewer is checking:** Whether you know the anchor + recursive-step structure and can walk a hierarchy of unknown depth.
**Say this in the interview:** A recursive CTE has two parts glued by UNION ALL. The anchor selects the manager's direct reports; the recursive part keeps joining the table to the rows found so far to pick up the next level, and it stops when a step finds nobody new.
**Explain simply:**
- A **recursive CTE** is a query that refers to itself. The database repeats the second part, feeding it the rows from the previous round, until no new rows appear (PostgreSQL docs: https://www.postgresql.org/docs/current/queries-with.html).
- **Anchor** = starting rows. **Recursive step** = 'find the people who report to anyone found so far'.
- The `level` column counts the distance from the manager: 1 = direct report, 2 = report of a report.
- A plain self-join only goes a fixed number of levels; recursion handles any depth.
**Example:** Rahul manages Vikram and Sunita; Vikram manages Neeta and Omar; Sunita manages Pooja. Rahul's full team is 5 people.
**Sample data:**

`emp_org`

| employee_id | name | manager_id |
|---|---|---|
| 1 | Anita | NULL |
| 2 | Rahul | 1 |
| 3 | Priya | 1 |
| 4 | Vikram | 2 |
| 5 | Sunita | 2 |
| 6 | Arjun | 3 |
| 7 | Neeta | 4 |
| 8 | Omar | 4 |
| 9 | Pooja | 5 |
| 10 | Dev | 6 |

**SQL:**
```sql
WITH RECURSIVE reports AS (
    -- anchor: the direct reports of manager 2 (Rahul)
    SELECT employee_id, name, manager_id, 1 AS level
    FROM emp_org
    WHERE manager_id = 2
    UNION ALL
    -- recursive step: people who report to someone already found
    SELECT e.employee_id, e.name, e.manager_id, r.level + 1
    FROM emp_org e
    JOIN reports r ON e.manager_id = r.employee_id
)
SELECT employee_id, name, manager_id, level
FROM reports
ORDER BY level, employee_id;
```

Dialect note: PostgreSQL, MySQL 8 and SQLite need the word `RECURSIVE`; SQL Server writes just `WITH` (from memory, not run here).
**Output:**

| employee_id | name | manager_id | level |
|---|---|---|---|
| 4 | Vikram | 2 | 1 |
| 5 | Sunita | 2 | 1 |
| 7 | Neeta | 4 | 2 |
| 8 | Omar | 4 | 2 |
| 9 | Pooja | 5 | 2 |

**pandas equivalent:**
```python
def reports_of(org, boss):
    found, frontier, level = [], org[org["manager_id"] == boss], 1
    while len(frontier):
        found.append(frontier.assign(level=level))
        frontier = org[org["manager_id"].isin(frontier["employee_id"])]
        level += 1
    return pd.concat(found).sort_values(["level","employee_id"]).reset_index(drop=True)
result = reports_of(org_df, 2)[["employee_id","name","manager_id","level"]]
```
Result (actual run):
```text
 employee_id   name  manager_id  level
           4 Vikram         2.0      1
           5 Sunita         2.0      1
           7  Neeta         4.0      2
           8   Omar         4.0      2
           9  Pooja         5.0      2
```

**Edge cases:** Rahul himself is not listed (the anchor starts at his reports). A manager with no reports returns an empty result. A manager in a loop (A reports to B, B to A) would run forever: see Q33. Use UNION ALL; plain UNION removes duplicates and is slower.
**Likely follow-ups:**
- Include the manager in the list? Anchor on `employee_id = 2` instead.
- Add the depth or the chain text? Q24 and Q32.
**Common mistakes:** Forgetting the join condition direction (`e.manager_id = r.employee_id`), forgetting `RECURSIVE`, and having no stop for cycles.

### Q12 ⭐⭐⭐ 🔴 Gaps and islands: find the longest streak of consecutive login days for each user.
**Asked at:** commonly asked (no company-specific report found); the row-number trick is documented in public technical articles such as Red Gate's Simple Talk gaps-and-islands piece (not opened in full here).
**What the interviewer is checking:** Whether you know the 'date minus row number' trick to label consecutive runs.
**Say this in the interview:** I keep one row per user per day, number the days, and subtract that number from the date. Consecutive days produce the same result, so that value labels each streak. I then group by it, count days, and pick the longest per user.
**Explain simply:**
- Each unbroken run of dates is an **island**; the missing days between them are **gaps**.
- Dates 1, 2, 3 Jan with row numbers 1, 2, 3 give 31 Dec every time. A jump (5 Jan with row number 4) gives a new label.
- `DISTINCT` first, otherwise a double login on one day shifts the numbering and breaks the streak.
- Group by user and label, count rows = streak length.
**Example:** User 1 logs in 1, 2, 3 Jan and 5, 6 Jan: streaks of 3 and 2 days; longest is 3.
**Sample data:**

`logins` (user 1 has 3 Jan twice)

| user_id | login_date |
|---|---|
| 1 | 2025-01-01 |
| 1 | 2025-01-02 |
| 1 | 2025-01-03 |
| 1 | 2025-01-03 |
| 1 | 2025-01-05 |
| 1 | 2025-01-06 |
| 2 | 2025-01-10 |
| 2 | 2025-01-11 |
| 2 | 2025-01-12 |
| 2 | 2025-01-13 |
| 2 | 2025-01-20 |
| 3 | 2025-01-15 |

**SQL:**
```sql
WITH d AS (SELECT DISTINCT user_id, login_date FROM logins),          -- one row per user per day
numbered AS (
    SELECT user_id, login_date,
           ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
    FROM d
),
islands AS (
    SELECT user_id, login_date,
           date(login_date, '-' || rn || ' days') AS grp     -- same grp = same streak
    FROM numbered
),
streaks AS (
    SELECT user_id, grp, COUNT(*) AS streak_days,
           MIN(login_date) AS start_date, MAX(login_date) AS end_date
    FROM islands
    GROUP BY user_id, grp
),
best AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY streak_days DESC, start_date) AS pick
    FROM streaks
)
SELECT user_id, streak_days, start_date, end_date
FROM best
WHERE pick = 1
ORDER BY user_id;
```

Dialect alternatives for the date subtraction (not run here, from memory): PostgreSQL `login_date - rn::int`; MySQL `DATE_SUB(login_date, INTERVAL rn DAY)`; SQL Server `DATEADD(day, -rn, login_date)`.
**Output:**

| user_id | streak_days | start_date | end_date |
|---|---|---|---|
| 1 | 3 | 2025-01-01 | 2025-01-03 |
| 2 | 4 | 2025-01-10 | 2025-01-13 |
| 3 | 1 | 2025-01-15 | 2025-01-15 |

**pandas equivalent:**
```python
d = ldf.drop_duplicates().copy()
d["login_date"] = pd.to_datetime(d["login_date"])
d = d.sort_values(["user_id","login_date"])
d["grp"] = d["login_date"] - pd.to_timedelta(d.groupby("user_id").cumcount() + 1, unit="D")
s = (d.groupby(["user_id","grp"])["login_date"].agg(streak_days="count", start_date="min", end_date="max")
       .reset_index().sort_values(["user_id","streak_days","start_date"], ascending=[True, False, True]))
result = s.groupby("user_id").head(1).drop(columns="grp").reset_index(drop=True)
result["start_date"] = result["start_date"].dt.strftime("%Y-%m-%d")
result["end_date"] = result["end_date"].dt.strftime("%Y-%m-%d")
```
Result (actual run):
```text
 user_id  streak_days start_date   end_date
       1            3 2025-01-01 2025-01-03
       2            4 2025-01-10 2025-01-13
       3            1 2025-01-15 2025-01-15
```

**Edge cases:** Duplicate days (handled by DISTINCT). Ties between equal longest streaks: this picks the earliest; use RANK instead of ROW_NUMBER to return all. A user with one login has a streak of 1. Timestamps must be cut to dates first. If 'streak' should end at today, add a filter on `end_date`.
**Likely follow-ups:**
- Current streak only? Filter streaks whose `end_date` equals the latest date.
- Streaks that are not daily (30-minute sessions)? The row-number trick does not apply; use LAG plus a running sum.
**Common mistakes:** Forgetting DISTINCT, skipping the PARTITION BY user, and subtracting from a timestamp instead of a date.

### Q13 ⭐⭐ 🟢 Find duplicates based on a combination of columns (e.g., same name + date of birth + department).
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you extend GROUP BY / HAVING to a combination of columns and think about NULLs.
**Say this in the interview:** I group by all the columns that together define 'the same person', count rows per group and keep groups above 1. A row is only a duplicate if every listed column matches.
**Explain simply:**
- The group key is the full combination: name + date of birth + department.
- Asha (1995-04-12) in HR twice is a duplicate; Asha in IT is a different group, so not a duplicate.
- GROUP BY treats two NULLs as equal, so two Karans with unknown dob group together. Decide whether that is what you want.
- `GROUP_CONCAT` lists the ids to make cleanup easy (PostgreSQL / SQL Server: `STRING_AGG(staff_id::text, ',')` / `STRING_AGG(staff_id, ',')`; MySQL: `GROUP_CONCAT`; not run here).
**Example:** Meena appears 3 times with the same name, dob, department: a data-entry problem in the HRIS.
**Sample data:**

`staff`

| staff_id | name | dob | dept |
|---|---|---|---|
| 1 | Asha | 1995-04-12 | HR |
| 2 | Ravi | 1990-07-01 | Sales |
| 3 | Asha | 1995-04-12 | HR |
| 4 | Asha | 1995-04-12 | IT |
| 5 | Meena | 1988-01-30 | IT |
| 6 | Meena | 1988-01-30 | IT |
| 7 | Meena | 1988-01-30 | IT |
| 8 | Karan | NULL | IT |
| 9 | Karan | NULL | IT |

**SQL:**
```sql
SELECT name, dob, dept,
       COUNT(*) AS copies,
       GROUP_CONCAT(staff_id) AS staff_ids
FROM staff
GROUP BY name, dob, dept
HAVING COUNT(*) > 1
ORDER BY name;
```

**Output:**

| name | dob | dept | copies | staff_ids |
|---|---|---|---|---|
| Asha | 1995-04-12 | HR | 2 | 1,3 |
| Karan | NULL | IT | 2 | 8,9 |
| Meena | 1988-01-30 | IT | 3 | 5,6,7 |

**pandas equivalent:**
```python
g = sdf.groupby(["name","dob","dept"], dropna=False)
result = (g.agg(copies=("staff_id","size"), staff_ids=("staff_id", lambda s: ",".join(map(str, s))))
           .reset_index().query("copies > 1").sort_values("name").reset_index(drop=True))
```
Result (actual run):
```text
 name        dob dept  copies staff_ids
 Asha 1995-04-12   HR       2       1,3
Karan        NaN   IT       2       8,9
Meena 1988-01-30   IT       3     5,6,7
```

**Edge cases:** NULL dob rows (Karan) are grouped as duplicates in both SQL and pandas (`dropna=False` is needed in pandas). Spelling and case differences ('asha' vs 'Asha') hide duplicates; use `LOWER(TRIM(name))`. Two real people can share name and dob, so confirm with another field.
**Likely follow-ups:**
- Show all the duplicate rows? Join the result back on the three columns (use `IS` or `COALESCE` for NULL-safe matching).
- Delete extras? Q5 with `PARTITION BY name, dob, dept`.
**Common mistakes:** Grouping by too few columns (false duplicates) or too many (misses real ones), and ignoring NULLs.

### Q14 ⭐⭐ 🟢 How do you quickly check whether a table has duplicates by comparing COUNT(*) with COUNT(DISTINCT column)?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know how COUNT treats NULLs, and have a fast way to test uniqueness.
**Say this in the interview:** If COUNT of the column is bigger than COUNT DISTINCT of it, some values repeat. COUNT(*) counts all rows, COUNT(column) skips NULLs, and COUNT(DISTINCT column) counts each different non-NULL value once.
**Explain simply:**
- `COUNT(*)` = number of rows. `COUNT(email)` = rows where email is not NULL. `COUNT(DISTINCT email)` = different emails.
- If `COUNT(email) = COUNT(DISTINCT email)`, no non-NULL email repeats.
- The difference is the number of *extra* copies, not the number of duplicated emails (3 copies of one email = 2 extra).
- It is a quick yes/no check; use GROUP BY / HAVING (Q1) to see which ones.
**Example:** 9 employee rows, 7 have emails, 5 are different: 2 extra duplicate rows.
**Sample data:** the `employees` table from Q1.
**SQL:**
```sql
SELECT COUNT(*)                 AS total_rows,
       COUNT(email)              AS non_null_emails,
       COUNT(DISTINCT email)     AS distinct_emails,
       COUNT(email) - COUNT(DISTINCT email) AS extra_duplicate_rows
FROM employees;
```

**Output:**

| total_rows | non_null_emails | distinct_emails | extra_duplicate_rows |
|---|---|---|---|
| 9 | 7 | 5 | 2 |

**pandas equivalent:**
```python
result = pd.DataFrame([{"total_rows": len(df), "non_null_emails": df["email"].notna().sum(),
    "distinct_emails": df["email"].nunique(),
    "extra_duplicate_rows": df["email"].notna().sum() - df["email"].nunique()}])
```
Result (actual run):
```text
 total_rows  non_null_emails  distinct_emails  extra_duplicate_rows
          9                7                5                     2
```

**Edge cases:** Comparing `COUNT(*)` with `COUNT(DISTINCT email)` would wrongly count the 2 NULL rows as extra (9 vs 5 = 4, not 2). On a column that should be unique, NULLs may be allowed by a UNIQUE constraint (most databases allow several NULLs), so decide separately whether NULLs are acceptable. COUNT(DISTINCT) on very big tables is expensive.
**Likely follow-ups:**
- Check two columns together? Count distinct pairs by subquery: `SELECT COUNT(*) FROM (SELECT DISTINCT a, b FROM t)`.
- How to see which? GROUP BY ... HAVING (Q1).
**Common mistakes:** Using `COUNT(*)` in the comparison, and reading the difference as 'number of duplicated values'.

### Q15 ⭐⭐ 🟢 Why is SELECT * discouraged in production queries?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you think about performance, network cost and code that breaks when the table changes.
**Say this in the interview:** SELECT * reads and ships every column, even ones I do not need, which blocks index-only reads, wastes network and memory, and can break downstream code when someone adds or reorders a column. In production I list the columns I need.
**Explain simply:**
- **More data moved:** wide columns (notes, documents) travel to the app even if unused.
- **Index-only reads blocked:** if the query asks only for columns inside an index, the database can answer from the index alone (a **covering index**, Q39). `SELECT *` rules that out.
- **Fragile code:** inserting with `SELECT *` or relying on column position breaks when the table changes.
- **Readability:** the reader sees exactly which fields matter. (Fine for quick exploration.)
**Example:** A payroll screen needs name and salary, but `SELECT *` also pulls bank details: wasteful and a privacy risk.
**Sample data:** the 20,000-row `employees` table from Q8 with `CREATE INDEX idx_dept_sal ON employees(dept, salary)`; and a small `hr_emp` / `hr_emp_archive` pair.
**SQL:**
```sql
-- 1. Plans with and without SELECT *
EXPLAIN QUERY PLAN SELECT * FROM employees WHERE dept = 'IT';
EXPLAIN QUERY PLAN SELECT dept, salary FROM employees WHERE dept = 'IT';

-- 2. Fragile code: copy to archive using SELECT *
INSERT INTO hr_emp_archive SELECT * FROM hr_emp;      -- fine today
ALTER TABLE hr_emp ADD COLUMN salary INTEGER;         -- schema changes later
INSERT INTO hr_emp_archive SELECT * FROM hr_emp;      -- now fails
```
**Output (real run):**
```text
SELECT *            -> SEARCH employees USING INDEX idx_dept_sal (dept=?)
SELECT dept, salary -> SEARCH employees USING COVERING INDEX idx_dept_sal (dept=?)
Second INSERT ... SELECT * error: table hr_emp_archive has 3 columns but 4 values were supplied
```
**Edge cases:** For a table with only the columns you need, `SELECT *` costs little; the real harm grows with wide tables, joins (duplicate column names such as `id`) and views. `SELECT COUNT(*)` is fine: the star there means 'rows', not columns. `EXISTS (SELECT * ...)` is also fine.
**Likely follow-ups:**
- Is `SELECT *` ever fine? Ad-hoc exploration and `COUNT(*)`.
- Does it hurt in columnar warehouses? Usually yes: they bill by columns read (from memory, product-specific).
**Common mistakes:** Using `SELECT *` in views and ETL jobs, and `INSERT INTO t SELECT *` without naming columns.

### Q16 ⭐⭐ 🟡 Remove duplicate rows without ROW_NUMBER (using MIN(id) / self join).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can de-duplicate with plain GROUP BY / self join when window functions are not allowed, and whether you protect rows with NULLs.
**Say this in the interview:** I group the rows by the duplicate key, take the smallest id in each group as the copy to keep, and delete every row whose id is not one of those. The self-join version deletes any row that has an earlier row with the same key.
**Explain simply:**
- A **duplicate** here means two rows with the same email but different `id`. The `id` is the only thing that tells the copies apart.
- `MIN(id)` per email picks exactly one survivor per group (the oldest row). `NOT IN` then removes all the others.
- A **self join** (a table joined to itself under two nicknames) lets a row ask 'is there an older row with my email?'. If yes, it is a copy and goes.
- This works on any database, including old ones with no `ROW_NUMBER` (that window function arrived in MySQL 8.0, from memory).
**Example:** HR keeps the same candidate three times because the recruiter pasted Asha's CV thrice: ids 1, 3, 6. We keep id 1 and delete 3 and 6.
**Sample data:**

`contacts`

| id | name | email |
|---|---|---|
| 1 | Asha | asha@x.com |
| 2 | Ravi | ravi@x.com |
| 3 | Asha | asha@x.com |
| 4 | Meena | meena@x.com |
| 5 | Ravi | ravi@x.com |
| 6 | Asha | asha@x.com |
| 7 | Karan | NULL |
| 8 | Divya | NULL |

**SQL:**
```sql
-- main query (run in SQLite 3.45.1): keep the smallest id per email
DELETE FROM contacts
WHERE email IS NOT NULL                       -- do not treat NULL emails as duplicates
  AND id NOT IN (SELECT MIN(id) FROM contacts
                 WHERE email IS NOT NULL
                 GROUP BY email);

-- self-join style (also run here, same final table). In MySQL the multi-table form is
-- DELETE c FROM contacts c JOIN contacts o ON o.email = c.email AND o.id < c.id;   -- not run here
DELETE FROM contacts
WHERE EXISTS (SELECT 1 FROM contacts older
              WHERE older.email = contacts.email   -- same email
                AND older.id    < contacts.id);    -- but an earlier row exists
```

**Output:** (rows deleted: 3; remaining table)

| id | name | email |
|---|---|---|
| 1 | Asha | asha@x.com |
| 2 | Ravi | ravi@x.com |
| 4 | Meena | meena@x.com |
| 7 | Karan | NULL |
| 8 | Divya | NULL |

Both versions leave exactly the same rows (3 deleted by the self-join version).

**pandas equivalent:**
```python
keep = contacts["email"].isna() | ~contacts.duplicated("email", keep="first")
result = contacts[keep].sort_values("id").reset_index(drop=True)
```
Result (actual run):
```text
 id  name       email
  1  Asha  asha@x.com
  2  Ravi  ravi@x.com
  4 Meena meena@x.com
  7 Karan         NaN
  8 Divya         NaN
```
**Edge cases:** NULL emails: `GROUP BY` puts all NULLs in one group, so without the `IS NOT NULL` guard Divya (id 8) would be deleted because Karan (id 7) also has a NULL email, although they are different people. Ties cannot happen on `id` if it is unique. Always run the matching `SELECT` first to preview what will go.
**Likely follow-ups:**
- Keep the newest instead? Use `MAX(id)` (or compare dates), see Q17.
- Why can `NOT IN` be dangerous? If the subquery returns a NULL, `NOT IN` returns nothing. `MIN(id)` is never NULL for the grouped rows, so it is safe here.
- MySQL error 'You can't specify target table for update in FROM clause' (error 1093, from memory) appears when the subquery reads the table being deleted; wrap the subquery in a derived table or use the join form.
**Common mistakes:** Deleting without a backup or a preview `SELECT`, grouping by too few columns (deleting real different people), and forgetting that NULLs group together.

### Q17 ⭐⭐ 🟡 Among duplicate records for each customer, keep only the latest one (by updated date).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can pick 'the latest row per key' and decide what happens on a tie.
**Say this in the interview:** For each customer I keep the row that has no newer row after it. If two rows share the same date I break the tie with the higher id, so exactly one row survives.
**Explain simply:**
- 'Latest' means largest `updated_at`. A row is the latest if **no other row** of the same customer is newer (that is the `NOT EXISTS`).
- **Ties** (same date twice) would keep both rows, so we add a second rule: the higher `rec_id` wins.
- To actually remove the old rows, flip the test: delete every row that **does** have a newer copy.
- The window function version (`ROW_NUMBER ... ORDER BY updated_at DESC`) gives the same answer and is shorter; use it where available.
**Example:** A customer changed email on 5 March. The old record (10 Jan) is stale and should go; the 5 March record stays.
**Sample data:**

`customer_records`

| rec_id | customer_id | email | updated_at |
|---|---|---|---|
| 1 | 101 | old@a.com | 2025-01-10 |
| 2 | 101 | new@a.com | 2025-03-05 |
| 3 | 102 | r@b.com | 2025-02-01 |
| 4 | 103 | m1@c.com | 2025-01-15 |
| 5 | 103 | m2@c.com | 2025-01-15 |
| 6 | 103 | m3@c.com | 2024-12-01 |
| 7 | 104 | k@d.com | 2025-04-01 |

**SQL:**
```sql
-- main query (SQLite 3.45.1): preview the rows to KEEP
SELECT c.*
FROM customer_records c
WHERE NOT EXISTS (SELECT 1 FROM customer_records n          -- is there a newer copy?
                  WHERE n.customer_id = c.customer_id
                    AND (n.updated_at > c.updated_at
                         OR (n.updated_at = c.updated_at AND n.rec_id > c.rec_id)))  -- tie-break
ORDER BY c.customer_id;

-- shorter version with a window function (also run, same result)
SELECT rec_id, customer_id, email, updated_at
FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY customer_id
                                   ORDER BY updated_at DESC, rec_id DESC) AS rn
      FROM customer_records)
WHERE rn = 1
ORDER BY customer_id;

-- to remove the older copies (run here; afterwards the table equals the output below)
DELETE FROM customer_records
WHERE EXISTS (SELECT 1 FROM customer_records n
              WHERE n.customer_id = customer_records.customer_id
                AND (n.updated_at > customer_records.updated_at
                     OR (n.updated_at = customer_records.updated_at
                         AND n.rec_id > customer_records.rec_id)));
```

**Output:**

| rec_id | customer_id | email | updated_at |
|---|---|---|---|
| 2 | 101 | new@a.com | 2025-03-05 |
| 3 | 102 | r@b.com | 2025-02-01 |
| 5 | 103 | m2@c.com | 2025-01-15 |
| 7 | 104 | k@d.com | 2025-04-01 |

(The DELETE removed 3 rows; the remaining table is identical to this output.)

**pandas equivalent:**
```python
result = (df.sort_values(["updated_at", "rec_id"])
            .drop_duplicates("customer_id", keep="last")
            .sort_values("customer_id").reset_index(drop=True))
```
Result (actual run):
```text
 rec_id  customer_id     email updated_at
      2          101 new@a.com 2025-03-05
      3          102   r@b.com 2025-02-01
      5          103  m2@c.com 2025-01-15
      7          104   k@d.com 2025-04-01
```
**Edge cases:** Customer 103 has two rows with the same date (rows 4 and 5): the tie-break keeps row 5. A NULL `updated_at` is never greater than anything, so such a row would lose to any dated row; decide whether that is what the business wants. Compare real dates, not text in `DD-MM-YYYY` format.
**Likely follow-ups:**
- Why not `GROUP BY customer_id` with `MAX(updated_at)`? You lose the other columns (the email) unless you join back, and ties then return two rows.
- Which is faster? Index on `(customer_id, updated_at)` helps all versions; test with `EXPLAIN` on your data.
**Common mistakes:** No tie-break rule, joining back on `MAX(updated_at)` alone (returns duplicates on ties), and deleting before previewing.

### Q18 ⭐⭐ 🟡 Find the top 3 distinct salaries in the company (including ties).
**Asked at:** commonly asked (no company-specific report found); the related 'second highest salary' form appears in anonymous Glassdoor reviews (Myntra, Infosys) listed in research/Book02_Part10_sources.md (self-reported)
**What the interviewer is checking:** Whether you know the difference between top 3 rows and top 3 distinct values, and how ties behave.
**Say this in the interview:** I take the distinct salaries, sort them high to low and keep three. If I also need the people, I use DENSE_RANK and keep rank 3 or less, so everyone tied on a salary is included.
**Explain simply:**
- `DISTINCT` removes repeated salaries so 90000 counts once. `LIMIT 3` then gives three **different** amounts.
- `DENSE_RANK()` numbers salaries 1,2,3 with no gaps and the same number for ties, so 'rank <= 3' returns every employee in the top 3 salary levels (may be more than 3 people).
- Plain `LIMIT 3` without `DISTINCT` would return 90000, 90000, 75000: wrong for 'top 3 salaries'.
**Example:** Salary bands for a bonus: the three highest pay levels are 90,000, 75,000 and 60,000; six employees sit in those levels.
**Sample data:**

`employees`

| emp_id | name | salary |
|---|---|---|
| 1 | Asha | 90000 |
| 2 | Ravi | 75000 |
| 3 | Meena | 90000 |
| 4 | Karan | 60000 |
| 5 | Divya | 75000 |
| 6 | Sunil | 50000 |
| 7 | Priya | 60000 |
| 8 | Neha | NULL |

**SQL:**
```sql
-- 1) the three distinct salaries (run in SQLite 3.45.1)
SELECT DISTINCT salary
FROM employees
WHERE salary IS NOT NULL
ORDER BY salary DESC
LIMIT 3;                        -- SQLite / MySQL / PostgreSQL
-- SQL Server: SELECT DISTINCT TOP 3 salary ... ORDER BY salary DESC;  -- not run here
-- Standard/PostgreSQL/Oracle 12c+: ... FETCH FIRST 3 ROWS ONLY;        -- not run here

-- 2) the employees on those salaries
SELECT name, salary, rnk
FROM (SELECT name, salary,
             DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
      FROM employees
      WHERE salary IS NOT NULL)
WHERE rnk <= 3
ORDER BY salary DESC, name;
```

**Output (1):**

| salary |
|---|
| 90000 |
| 75000 |
| 60000 |

**Output (2):**

| name | salary | rnk |
|---|---|---|
| Asha | 90000 | 1 |
| Meena | 90000 | 1 |
| Divya | 75000 | 2 |
| Ravi | 75000 | 2 |
| Karan | 60000 | 3 |
| Priya | 60000 | 3 |

**pandas equivalent:**
```python
top3_salaries = pd.DataFrame({"salary": df["salary"].dropna().drop_duplicates().nlargest(3).astype(int)}).reset_index(drop=True)
d = df.dropna(subset=["salary"]).copy()
d["rnk"] = d["salary"].rank(method="dense", ascending=False).astype(int)
top3_people = d[d["rnk"] <= 3].sort_values(["salary", "name"], ascending=[False, True])[["name", "salary", "rnk"]].reset_index(drop=True)
```
Result (actual run, query 1):
```text
 salary
  90000
  75000
  60000
```
Result (actual run, query 2):
```text
 name  salary  rnk
 Asha 90000.0    1
Meena 90000.0    1
Divya 75000.0    2
 Ravi 75000.0    2
Karan 60000.0    3
Priya 60000.0    3
```
**Edge cases:** NULL salary (Neha) is excluded explicitly: SQLite sorts NULL last on `DESC` but PostgreSQL sorts NULL **first** on `DESC` (from memory), so the guard keeps the answer portable. Fewer than 3 distinct salaries simply returns fewer rows.
**Likely follow-ups:**
- Top 3 *employees* even with ties? Use `RANK` or `ROW_NUMBER` depending on whether ties should be cut off (see Q4).
- Third highest only? Q3 / Q6.
**Common mistakes:** Forgetting `DISTINCT`, using `ROW_NUMBER` (cuts ties), and letting NULL salaries sneak into the ranking.

### Q19 ⭐⭐ 🟡 How do you delete duplicates from a table that has no primary key or unique ID?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know a table with no key still has a hidden way to tell rows apart, or that you can rebuild it with DISTINCT.
**Say this in the interview:** Two safe ways: use the database's hidden row identifier to keep one copy, or write the distinct rows into a new table, check it, then swap it in. The rebuild is the safest.
**Explain simply:**
- With no `id`, identical rows are truly indistinguishable by their values, so you need something else: SQLite's `rowid`, PostgreSQL's `ctid`, Oracle's `ROWID` (the last two from memory, not run here).
- SQL Server has no such column but allows deleting through a CTE: `WITH x AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY emp_id, log_date, status ORDER BY (SELECT NULL)) rn FROM t) DELETE FROM x WHERE rn > 1;` (not run here).
- The portable alternative: `CREATE TABLE new AS SELECT DISTINCT ...`, verify counts, drop the old table, rename. Indexes and constraints must be recreated.
- Afterwards add a primary key or `UNIQUE (emp_id, log_date)` so it cannot happen again.
**Example:** The biometric attendance machine uploaded Asha's 1 June punch twice and Meena's three times: 6 clean rows, 7 in the table.
**Sample data:**

`attendance_log` (no primary key; 7 rows)

| emp_id | log_date | status |
|---|---|---|
| 1 | 2025-06-01 | P |
| 1 | 2025-06-01 | P |
| 2 | 2025-06-01 | A |
| 3 | 2025-06-01 | P |
| 3 | 2025-06-01 | P |
| 3 | 2025-06-01 | P |
| 2 | 2025-06-02 | P |

**SQL:**
```sql
-- main query (SQLite 3.45.1): keep the first physical copy of each identical row
DELETE FROM attendance_log
WHERE rowid NOT IN (SELECT MIN(rowid)               -- rowid = SQLite's hidden row number
                    FROM attendance_log
                    GROUP BY emp_id, log_date, status);

-- rebuild approach (also run, same result)
CREATE TABLE attendance_clean AS
SELECT DISTINCT emp_id, log_date, status FROM attendance_log_original;
-- then DROP the old table and rename attendance_clean (after taking a backup)
```

**Output:** (rows deleted: 3; remaining rows)

| emp_id | log_date | status |
|---|---|---|
| 1 | 2025-06-01 | P |
| 2 | 2025-06-01 | A |
| 2 | 2025-06-02 | P |
| 3 | 2025-06-01 | P |

The rebuild approach returned the same 4 rows.

**pandas equivalent:**
```python
result = df.drop_duplicates().sort_values(["emp_id", "log_date", "status"]).reset_index(drop=True)
```
Result (actual run):
```text
 emp_id   log_date status
      1 2025-06-01      P
      2 2025-06-01      A
      2 2025-06-02      P
      3 2025-06-01      P
```
**Edge cases:** `GROUP BY` and `DISTINCT` treat NULLs as equal, so two rows that are NULL in the same columns count as duplicates. If rows differ in any column (even a timestamp) they are not duplicates; choose the columns deliberately. Run inside a transaction with a backup.
**Likely follow-ups:**
- Why not `DELETE ... WHERE (a,b,c) IN (SELECT a,b,c ... HAVING COUNT(*)>1)`? That deletes **all** copies, including the one you wanted to keep.
**Common mistakes:** Deleting every copy, assuming `rowid` exists everywhere, and not adding a constraint afterwards.

### Q20 ⭐⭐ 🟡 Find the missing numbers in a sequence (e.g., missing invoice or order IDs).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can build the full list of numbers that should exist and subtract what exists (anti-join).
**Say this in the interview:** I generate every number from the smallest to the largest invoice with a recursive CTE, left join the real invoices, and keep the numbers that found no match. For ranges of gaps I can use LEAD instead.
**Explain simply:**
- You cannot find a row that is not there, so first create the **complete list** 1001..1010 (a *number series*), then compare.
- A **recursive CTE** is a query that calls itself; here it starts at the minimum and adds 1 until the maximum (see Q22).
- A **LEFT JOIN ... WHERE right side IS NULL** is called an anti-join: it keeps only numbers with no real invoice.
- The `LEAD` version looks at the next invoice number; if it jumps by more than 1, there is a gap between them.
**Example:** Finance audit: invoice numbers must be continuous. 1003, 1004 and 1008 are missing: were they cancelled or lost?
**Sample data:**

`invoices`

| invoice_no | amount |
|---|---|
| 1001 | 500 |
| 1002 | 700 |
| 1005 | 300 |
| 1006 | 900 |
| 1007 | 150 |
| 1009 | 400 |
| 1010 | 250 |

**SQL:**
```sql
-- main query (SQLite 3.45.1): list each missing number
WITH RECURSIVE seq(n) AS (
    SELECT MIN(invoice_no) FROM invoices
    UNION ALL
    SELECT n + 1 FROM seq WHERE n < (SELECT MAX(invoice_no) FROM invoices)
)
SELECT n AS missing_invoice
FROM seq
LEFT JOIN invoices i ON i.invoice_no = seq.n
WHERE i.invoice_no IS NULL
ORDER BY n;
-- PostgreSQL could use generate_series(min, max) instead of the CTE;
-- SQL Server omits the word RECURSIVE and defaults to MAXRECURSION 100 (not run here, from memory)

-- gap ranges with LEAD (also run)
SELECT invoice_no + 1 AS gap_start, next_no - 1 AS gap_end
FROM (SELECT invoice_no, LEAD(invoice_no) OVER (ORDER BY invoice_no) AS next_no
      FROM invoices)
WHERE next_no - invoice_no > 1
ORDER BY gap_start;
```

**Output (missing numbers):**

| missing_invoice |
|---|
| 1003 |
| 1004 |
| 1008 |

**Output (gap ranges):**

| gap_start | gap_end |
|---|---|
| 1003 | 1004 |
| 1008 | 1008 |

**pandas equivalent:**
```python
full = pd.DataFrame({"missing_invoice": range(df["invoice_no"].min(), df["invoice_no"].max() + 1)})
result = full[~full["missing_invoice"].isin(df["invoice_no"])].reset_index(drop=True)
s = df["invoice_no"].sort_values().reset_index(drop=True)
nxt = s.shift(-1)
gaps = nxt - s > 1
result = pd.DataFrame({"gap_start": s[gaps] + 1, "gap_end": (nxt[gaps] - 1).astype(int)}).reset_index(drop=True)
```
Result (actual run, missing numbers):
```text
 missing_invoice
            1003
            1004
            1008
```
Result (actual run, gap ranges):
```text
 gap_start  gap_end
      1003     1004
      1008     1008
```
**Edge cases:** Numbers missing **before the minimum or after the maximum** cannot be detected from the table itself (1000 or 1011): you need the expected start and end from the business. Duplicates do not hurt (the join only checks existence). A very wide range (millions) makes the recursive series slow: use a numbers table or `generate_series`.
**Likely follow-ups:**
- Missing **dates**? Same idea, see Q23.
- Is `NOT IN (SELECT ...)` an option? Yes, but it breaks if the subquery contains a NULL.
**Common mistakes:** Comparing only neighbours without thinking about the ends, and forgetting the stop condition of the recursion.

### Q21 ⭐⭐ 🟡 Find employees who were absent on 3 or more consecutive days from an attendance table (gaps and islands).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know the gaps-and-islands trick: date minus row number is constant inside an unbroken streak.
**Say this in the interview:** I keep only absent rows, number them per employee, and subtract that number of days from each date. Consecutive days all give the same result, so I group by it and keep groups with 3 or more days.
**Explain simply:**
- An **island** is an unbroken run of consecutive days; a **gap** is the break between runs.
- Take absent days 2, 3, 4 June with row numbers 1, 2, 3. Date minus row number = 1 June each time. A later absence on 6 June has row number 4 → 2 June, a different key, so it is a new island.
- Group by employee and that key; `MIN`/`MAX` date give the streak start and end; `COUNT(*)` its length.
- The `date(x, '-n days')` syntax is SQLite. SQL Server: `DATEADD(day, -rn, att_date)`; MySQL: `DATE_SUB(att_date, INTERVAL rn DAY)`; PostgreSQL: `att_date - rn` for a DATE column (not run here, from memory).
**Example:** HR policy: 3 or more absent days in a row triggers a check-in call. Asha (Mon-Wed) and Meena (all week) qualify; Ravi's two days do not.
**Sample data:** `attendance(emp_id, att_date, status)`, P = present, A = absent, shown as a grid (20 rows in the table)

| emp_id | Mon 02 | Tue 03 | Wed 04 | Thu 05 | Fri 06 |
|---|---|---|---|---|---|
| 1 | A | A | A | P | A |
| 2 | A | A | P | A | P |
| 3 | A | A | A | A | A |
| 4 | P | P | P | P | P |

**SQL:**
```sql
-- SQLite 3.45.1 (run here)
WITH absent AS (
    SELECT emp_id, att_date,
           ROW_NUMBER() OVER (PARTITION BY emp_id ORDER BY att_date) AS rn
    FROM attendance
    WHERE status = 'A'
),
islands AS (
    SELECT emp_id, att_date,
           date(att_date, '-' || rn || ' days') AS island_key   -- same key = consecutive days
    FROM absent
)
SELECT emp_id,
       MIN(att_date) AS streak_start,
       MAX(att_date) AS streak_end,
       COUNT(*)      AS days_absent
FROM islands
GROUP BY emp_id, island_key
HAVING COUNT(*) >= 3
ORDER BY emp_id, streak_start;
```

**Output:**

| emp_id | streak_start | streak_end | days_absent |
|---|---|---|---|
| 1 | 2025-06-02 | 2025-06-04 | 3 |
| 3 | 2025-06-02 | 2025-06-06 | 5 |

**pandas equivalent:**
```python
a = df[df["status"] == "A"].copy()
a["att_date"] = pd.to_datetime(a["att_date"])
a = a.sort_values(["emp_id", "att_date"])
a["rn"] = a.groupby("emp_id").cumcount() + 1
a["island_key"] = a["att_date"] - pd.to_timedelta(a["rn"], unit="D")
g = a.groupby(["emp_id", "island_key"]).agg(streak_start=("att_date", "min"),
                                           streak_end=("att_date", "max"),
                                           days_absent=("att_date", "size")).reset_index()
result = g[g["days_absent"] >= 3].drop(columns="island_key").sort_values(["emp_id", "streak_start"]).reset_index(drop=True)
```
Result (actual run):
```text
 emp_id streak_start streak_end  days_absent
      1   2025-06-02 2025-06-04            3
      3   2025-06-02 2025-06-06            5
```
**Edge cases:** Duplicate rows for the same day break the numbering (the key drifts): de-duplicate first. Weekends and holidays: Friday and next Monday absences are not consecutive **calendar** days; to treat them as consecutive, number the working days (from a calendar table) instead of using dates. Employees with no absence simply return no row. Decide whether the streak must be inside one month or may cross it (dates handle crossing naturally).
**Likely follow-ups:**
- Longest streak per user? Same pattern, then take `MAX(days)` (see Q12).
- Can I do it with `LAG`? Yes: flag a row as a new streak when the previous date is not yesterday, then running-sum the flags (works for thresholds like '30 minutes' too).
**Common mistakes:** Not filtering to absent rows before numbering, numbering over all rows, and subtracting from the wrong data type.

### Q22 ⭐⭐ 🟡 Use a recursive CTE to generate numbers from 1 to 10.
**Asked at:** commonly asked (no company-specific report found) for recursive CTEs: no company-specific source found (standard SQL curriculum, per research/Book02_Part10_sources.md)
**What the interviewer is checking:** Whether you understand the two parts of a recursive CTE and the stop condition.
**Say this in the interview:** A recursive CTE has an anchor row (start at 1) and a recursive step that adds 1 to the previous row, with a WHERE that stops it at 10. The database repeats the step until it returns no new rows.
**Explain simply:**
- **CTE** = a named temporary result written with `WITH`. **Recursive** = the CTE refers to itself.
- Shape: anchor query, `UNION ALL`, recursive query. PostgreSQL's documentation describes it as evaluated step by step: each round feeds only the rows from the previous round into the recursive part, until a round returns zero rows (https://www.postgresql.org/docs/current/queries-with.html).
- No stop condition means an endless loop. Always include `WHERE n < 10` or similar.
- Why bother? Number lists and date calendars (Q20, Q23) and org charts (Q24).
**Example:** Need a 1..12 list to show every month even when no one was hired in some month.
**SQL:**
```sql
-- main query (SQLite 3.45.1, run here)
WITH RECURSIVE nums(n) AS (
    SELECT 1                           -- anchor: the starting row
    UNION ALL
    SELECT n + 1 FROM nums WHERE n < 10   -- recursive step with a stop condition
)
SELECT n FROM nums;
-- PostgreSQL shortcut: SELECT generate_series(1, 10);                     -- not run here
-- SQL Server: drop the word RECURSIVE; default limit 100 rows (OPTION (MAXRECURSION n))  -- not run here, from memory
-- MySQL 8.0+: needs WITH RECURSIVE; limit set by cte_max_recursion_depth (default 1000)  -- not run here, from memory
```

**Output:**

| n |
|---|
| 1 |
| 2 |
| 3 |
| 4 |
| 5 |
| 6 |
| 7 |
| 8 |
| 9 |
| 10 |

**pandas equivalent:**
```python
result = pd.DataFrame({"n": range(1, 11)})
```
Result (actual run):
```text
 n
 1
 2
 3
 4
 5
 6
 7
 8
 9
10
```
**Edge cases:** Use `UNION ALL` (cheaper, keeps all rows); `UNION` removes duplicates each round and is only needed for cycle-prone data. If the stop condition is wrong the query may run forever (or hit the engine's recursion limit).
**Likely follow-ups:**
- What if I forget the stop? Infinite loop or a recursion-limit error depending on the database.
- Dates instead of numbers? Replace `n + 1` by `date(d, '+1 day')` in SQLite (see Q23).
**Common mistakes:** Missing stop condition, using `UNION` unnecessarily, and writing `n < 10` but expecting the 11th row (the check happens before adding).

### Q23 ⭐⭐ 🟡 Use a recursive CTE to generate a calendar of dates and find the dates with no sales.
**Asked at:** commonly asked (no company-specific report found) for recursive CTEs: no company-specific source found
**What the interviewer is checking:** Whether you know that missing dates must come from a generated calendar, since a sales table cannot show days with no rows.
**Say this in the interview:** I generate every date in the period with a recursive CTE, left join the sales table, and keep the dates where no sale was found.
**Explain simply:**
- The `sales` table only has rows for days when something sold, so zero-sale days do not exist in it. Build the **calendar** first.
- `date(d, '+1 day')` adds a day in SQLite. PostgreSQL: `generate_series(date '2025-01-01', date '2025-01-10', interval '1 day')`; SQL Server: `DATEADD(day, 1, d)`; MySQL: `DATE_ADD(d, INTERVAL 1 DAY)` (not run here, from memory).
- `LEFT JOIN ... WHERE s.sale_id IS NULL` keeps calendar days with no match. Two sales on 2 January make two joined rows but that day is filtered out anyway.
- In real work the start/end dates come from parameters or a permanent date table.
**Example:** Store sales for 1-10 January: nothing sold on the 3rd, 6th, 7th and 10th: are these holidays, stock-outs or data load failures?
**Sample data:**

`sales`

| sale_id | sale_date | amount |
|---|---|---|
| 1 | 2025-01-01 | 1200 |
| 2 | 2025-01-02 | 800 |
| 3 | 2025-01-02 | 450 |
| 4 | 2025-01-04 | 950 |
| 5 | 2025-01-05 | 700 |
| 6 | 2025-01-08 | 1100 |
| 7 | 2025-01-09 | 300 |

**SQL:**
```sql
-- SQLite 3.45.1 (run here)
WITH RECURSIVE calendar(d) AS (
    SELECT '2025-01-01'
    UNION ALL
    SELECT date(d, '+1 day') FROM calendar WHERE d < '2025-01-10'
)
SELECT c.d AS date_without_sales
FROM calendar c
LEFT JOIN sales s ON s.sale_date = c.d
WHERE s.sale_id IS NULL
ORDER BY c.d;
```

**Output:**

| date_without_sales |
|---|
| 2025-01-03 |
| 2025-01-06 |
| 2025-01-07 |
| 2025-01-10 |

**pandas equivalent:**
```python
cal = pd.date_range("2025-01-01", "2025-01-10")
sold = pd.to_datetime(df["sale_date"])
result = pd.DataFrame({"date_without_sales": cal[~cal.isin(sold)]})
```
Result (actual run):
```text
date_without_sales
        2025-01-03
        2025-01-06
        2025-01-07
        2025-01-10
```
**Edge cases:** Dates stored with a time part (`2025-01-03 14:20`) will not match the calendar date: convert with `date(sale_date)`. Sales dates outside the calendar range are ignored. If the range is long, set a recursion limit appropriate for your database.
**Likely follow-ups:**
- Show 0 instead of missing? `LEFT JOIN` and `COALESCE(SUM(amount), 0) ... GROUP BY c.d`.
- List the gaps as ranges? See Q42.
**Common mistakes:** Trying to find missing dates directly from the sales table, and joining the wrong way round (INNER JOIN drops the empty days).

### Q24 ⭐⭐ 🟡 Use a recursive CTE to show the level (depth) of each employee in the org chart (CEO = level 1).
**Asked at:** commonly asked (no company-specific report found) for recursive CTEs: no company-specific source found
**What the interviewer is checking:** Whether you can walk a manager-employee hierarchy and carry a counter down each step.
**Say this in the interview:** I start with the top person (no manager) at level 1, then repeatedly join employees whose manager is someone already found, adding 1 to the level each time.
**Explain simply:**
- The table stores each person's **manager_id**, pointing at another row of the same table (a **self-referencing** hierarchy).
- Anchor: the CEO, `manager_id IS NULL`, level 1. Recursive part: find people whose boss is already in the result, level = boss's level + 1.
- It stops by itself when no one reports to the last group found (no new rows).
- Level 1 = CEO, level 2 = direct reports of the CEO, and so on.
**Example:** Anita is CEO (1). Rahul and Sneha report to her (2). Vikram, Pooja, Arjun are level 3, and Divya and Karan under Vikram are level 4.
**Sample data:**

`employees`

| emp_id | name | manager_id |
|---|---|---|
| 1 | Anita | NULL |
| 2 | Rahul | 1 |
| 3 | Sneha | 1 |
| 4 | Vikram | 2 |
| 5 | Pooja | 2 |
| 6 | Arjun | 3 |
| 7 | Divya | 4 |
| 8 | Karan | 4 |

**SQL:**
```sql
-- SQLite 3.45.1 (run here). SQL Server: omit the word RECURSIVE (not run here).
WITH RECURSIVE org(emp_id, name, manager_id, level) AS (
    SELECT emp_id, name, manager_id, 1          -- anchor: the CEO has no manager
    FROM employees
    WHERE manager_id IS NULL
    UNION ALL
    SELECT e.emp_id, e.name, e.manager_id, o.level + 1   -- each step goes one level down
    FROM employees e
    JOIN org o ON e.manager_id = o.emp_id
)
SELECT emp_id, name, manager_id, level
FROM org
ORDER BY level, emp_id;
```

**Output:**

| emp_id | name | manager_id | level |
|---|---|---|---|
| 1 | Anita | NULL | 1 |
| 2 | Rahul | 1 | 2 |
| 3 | Sneha | 1 | 2 |
| 4 | Vikram | 2 | 3 |
| 5 | Pooja | 2 | 3 |
| 6 | Arjun | 3 | 3 |
| 7 | Divya | 4 | 4 |
| 8 | Karan | 4 | 4 |

**pandas equivalent:**
```python
lvl = {}
cur = df[df["manager_id"].isna()]["emp_id"].tolist()
d = 1
while cur:
    for e in cur:
        lvl[e] = d
    cur = df[df["manager_id"].isin(cur)]["emp_id"].tolist()
    d += 1
result = df.assign(level=df["emp_id"].map(lvl)).sort_values(["level", "emp_id"]).reset_index(drop=True)
result["manager_id"] = result["manager_id"].astype("Int64")
```
Result (actual run):
```text
 emp_id   name  manager_id  level
      1  Anita        <NA>      1
      2  Rahul           1      2
      3  Sneha           1      2
      4 Vikram           2      3
      5  Pooja           2      3
      6  Arjun           3      3
      7  Divya           4      4
      8  Karan           4      4
```
**Edge cases:** More than one top person (several NULL managers) all get level 1. An employee whose `manager_id` points to a missing row never appears (orphan). A cycle (A manages B manages A) loops forever: see Q33. The `Int64` cast in pandas only keeps the manager id as a whole number with a missing value.
**Likely follow-ups:**
- Show the chain as text? Q32.
- Count people per level? `GROUP BY level` on the CTE.
**Common mistakes:** Anchoring on the wrong row, joining on the wrong direction (`e.emp_id = o.manager_id` goes UP the tree), and no stop for cycles.

### Q25 ⭐⭐ 🟡 Is it faster to filter with WHERE or HAVING? Explain when each is applied.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know the order in which SQL runs (WHERE, GROUP BY, HAVING) rather than just a speed rule.
**Say this in the interview:** They do different jobs: WHERE filters individual rows before grouping, HAVING filters groups after the aggregate is calculated. A condition on a plain column belongs in WHERE because it throws rows away early; a condition on SUM/AVG/COUNT needs HAVING.
**Explain simply:**
- Logical order: `FROM` → `WHERE` → `GROUP BY` → aggregates → `HAVING` → `SELECT` → `ORDER BY`.
- `WHERE` cannot use `AVG(salary)` because the average does not exist yet at that step.
- The premise 'which is faster' is partly misleading: with a non-aggregate condition, WHERE is the right and usually cheaper place (fewer rows to group). Many optimisers move such a condition earlier on their own, but do not rely on it (from memory; not tested here).
- Putting a plain condition in HAVING is allowed by some databases but reads confusingly.
**Example:** Average salary per department, only for departments other than Admin, and only those averaging above 55,000: HR and IT.
**Sample data:**

`employees`

| emp_id | name | dept | salary |
|---|---|---|---|
| 1 | Asha | HR | 52000 |
| 2 | Ravi | Sales | 48000 |
| 3 | Meena | IT | 90000 |
| 4 | Karan | IT | 80000 |
| 5 | Divya | HR | 61000 |
| 6 | Sunil | Admin | 30000 |
| 7 | Priya | Sales | 55000 |
| 8 | Neha | Admin | 32000 |

**SQL:**
```sql
-- same result with the plain-column filter in WHERE or in HAVING (both run here)
SELECT dept, COUNT(*) AS headcount FROM employees WHERE dept <> 'Admin' GROUP BY dept ORDER BY dept;
SELECT dept, COUNT(*) AS headcount FROM employees GROUP BY dept HAVING dept <> 'Admin' ORDER BY dept;

-- combined: WHERE for rows, HAVING for the aggregate
SELECT dept, COUNT(*) AS headcount, AVG(salary) AS avg_salary
FROM employees
WHERE dept <> 'Admin'            -- row filter: runs BEFORE grouping
GROUP BY dept
HAVING AVG(salary) > 55000       -- group filter: runs AFTER grouping
ORDER BY dept;
```

**Output (combined query):**

| dept | headcount | avg_salary |
|---|---|---|
| HR | 2 | 56500 |
| IT | 2 | 85000 |

The two filter-only queries returned the same rows (HR 2, IT 2, Sales 2). Real SQLite plans: WHERE version `['SCAN employees', 'USE TEMP B-TREE FOR GROUP BY']`; HAVING version `['SCAN employees', 'USE TEMP B-TREE FOR GROUP BY']`: SQLite's plan output does not show the early filtering, so it cannot prove which is faster.

**pandas equivalent:**
```python
d = df[df["dept"] != "Admin"]
g = d.groupby("dept").agg(headcount=("emp_id", "size"), avg_salary=("salary", "mean")).reset_index()
result = g[g["avg_salary"] > 55000].reset_index(drop=True)
```
Result (actual run):
```text
dept  headcount  avg_salary
  HR          2     56500.0
  IT          2     85000.0
```
**Edge cases:** `HAVING` without `GROUP BY` treats the whole table as one group. NULL salaries are ignored by `AVG`. Column aliases are not allowed in `HAVING` in standard SQL (MySQL and SQLite allow it; from memory).
**Likely follow-ups:**
- Can HAVING use a column that is not grouped? Not in standard SQL.
- Which do I use for 'departments with more than 5 people'? HAVING COUNT(*) > 5.
**Common mistakes:** Using an aggregate inside WHERE (error), and moving plain filters to HAVING out of habit.

### Q26 ⭐⭐ 🟡 Compare EXISTS, IN and JOIN: which is faster for checking presence and why?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you understand that these three can look alike but differ on duplicates and NULLs, and that speed depends on the optimiser and indexes.
**Say this in the interview:** For 'does a matching row exist', I use EXISTS or IN: they never multiply rows. A JOIN can repeat the left row once per match, so it needs DISTINCT. On modern databases the first two are usually planned the same way, so I choose by correctness and readability, and check EXPLAIN.
**Explain simply:**
- **EXISTS** stops at the first match for each employee. **IN** compares to a list built by the subquery. **JOIN** actually pairs rows, so an employee with 3 leaves appears 3 times.
- 'Which is faster' has no universal answer: it depends on the database, indexes and data size. Test with EXPLAIN on your data (below, SQLite 3.45.1 shows what it does here).
- `NOT IN` is dangerous if the subquery has a NULL: it returns nothing. `NOT EXISTS` is safe (shown below).
- Use JOIN when you need columns from both tables; use EXISTS/IN when you only check presence.
**Example:** Which employees have applied for leave at least once? Asha (2 requests), Meena (1) and Divya (3): three people, but a plain JOIN returns six rows.
**Sample data:**

`employees`

| emp_id | name |
|---|---|
| 1 | Asha |
| 2 | Ravi |
| 3 | Meena |
| 4 | Karan |
| 5 | Divya |
| 6 | Sunil |

`leave_requests`

| leave_id | emp_id | days |
|---|---|---|
| 1 | 1 | 2 |
| 2 | 1 | 1 |
| 3 | 3 | 5 |
| 4 | 5 | 1 |
| 5 | 5 | 2 |
| 6 | 5 | 3 |

**SQL:**
```sql
-- all run in SQLite 3.45.1
SELECT e.emp_id, e.name FROM employees e WHERE EXISTS (SELECT 1 FROM leave_requests l WHERE l.emp_id = e.emp_id) ORDER BY e.emp_id;
SELECT emp_id, name FROM employees WHERE emp_id IN (SELECT emp_id FROM leave_requests) ORDER BY emp_id;
SELECT e.emp_id, e.name FROM employees e JOIN leave_requests l ON l.emp_id = e.emp_id ORDER BY e.emp_id;                 -- 6 rows: duplicates!
SELECT DISTINCT e.emp_id, e.name FROM employees e JOIN leave_requests l ON l.emp_id = e.emp_id ORDER BY e.emp_id;                 -- fixed with DISTINCT
```

**Output (EXISTS, IN and JOIN+DISTINCT all return this):**

| emp_id | name |
|---|---|
| 1 | Asha |
| 3 | Meena |
| 5 | Divya |

Plain JOIN returned 6 rows (Asha 2, Meena 1, Divya 3).

Real plans here:
- EXISTS: `['SCAN e', 'CORRELATED SCALAR SUBQUERY 1', 'SCAN l']`
- IN: `['SEARCH employees USING INTEGER PRIMARY KEY (rowid=?)', 'LIST SUBQUERY 1', 'SCAN leave_requests']`
- JOIN: `['SCAN l', 'SEARCH e USING INTEGER PRIMARY KEY (rowid=?)', 'USE TEMP B-TREE FOR ORDER BY']`

NULL trap (after inserting a leave row with `emp_id` NULL): `NOT IN` returned **0 rows**, `NOT EXISTS` returned | emp_id | name |
|---|---|
| 2 | Ravi |
| 4 | Karan |
| 6 | Sunil |

**pandas equivalent:**
```python
result = dfe[dfe["emp_id"].isin(dfl["emp_id"])].reset_index(drop=True)   # EXISTS / IN
joined = dfe.merge(dfl, on="emp_id")                                     # JOIN: one row per leave
```
Result (actual run, EXISTS/IN):
```text
 emp_id  name
      1  Asha
      3 Meena
      5 Divya
```
(`joined` has 6 rows, one per leave, like the JOIN.)
**Edge cases:** NULLs (above), duplicates (JOIN), and an empty subquery (EXISTS false, IN false, JOIN no rows). Correlated `EXISTS` is generally fine with an index on `leave_requests(emp_id)`.
**Likely follow-ups:**
- Which handles 'does NOT have a leave'? `NOT EXISTS` or `LEFT JOIN ... IS NULL`.
- Does the optimiser rewrite one into the other? Often yes; that is why plans may look identical (from memory; here EXPLAIN is the evidence).
**Common mistakes:** Claiming one is always fastest, forgetting DISTINCT after a JOIN, and using `NOT IN` on a nullable column.

### Q27 ⭐⭐ 🟡 In a composite (multi-column) index, why does column order matter?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know the 'leftmost prefix' idea: a multi-column index is sorted by the first column, then the second inside it.
**Say this in the interview:** A composite index is like a phone book sorted by surname then first name. It helps when you filter on the first column (or first plus second), but not when you filter only on the second. So put the column you always filter by with equals first, and the range column after it.
**Explain simply:**
- The index `(dept_id, hire_date)` is sorted by department, and inside each department by hire date. A search for dept 7 and hire date after 2024 jumps straight to one small slice.
- Searching only by hire date cannot use that order: dates are scattered across all 50 departments. Same for a phone book searched by first name only.
- Rule of thumb: equality columns first, then the range column; and consider your most common queries. PostgreSQL's documentation says the same: a B-tree is most efficient with constraints on the leftmost columns, and `WHERE minor = 2` alone on an index `(major, minor)` is usually inefficient (https://www.postgresql.org/docs/current/indexes-multicolumn.html). MySQL's manual describes the leftmost-prefix rule (https://dev.mysql.com/doc/refman/8.4/en/mysql-indexes.html).
- Every extra index slows down inserts/updates and uses space, so do not index everything.
**Example:** HR portal: 'employees in department 7 hired after 1 Jan 2024' runs thousands of times a day, so `(dept_id, hire_date)` is the right index.
**Sample data:** a generated table `emp(emp_id, dept_id, hire_date, salary, name)` with 50,000 random rows (Python `random.seed(7)`, 50 departments, hire dates 2015 to 2025).

**SQL:**
```sql
-- SQLite 3.45.1 (run here); EXPLAIN QUERY PLAN output in the table below
CREATE INDEX idx_dept_hire ON emp(dept_id, hire_date);       -- test A
-- (dropped, then) CREATE INDEX idx_hire_dept ON emp(hire_date, dept_id);  -- test B
EXPLAIN QUERY PLAN SELECT * FROM emp WHERE dept_id = 7 AND hire_date >= '2024-01-01';
EXPLAIN QUERY PLAN SELECT * FROM emp WHERE dept_id = 7;
EXPLAIN QUERY PLAN SELECT * FROM emp WHERE hire_date >= '2024-01-01';
```

**Output (real plans, before and after):**

| query filter | rows returned | no index | index (dept_id, hire_date) | index (hire_date, dept_id) |
|---|---|---|---|---|
| dept_id = 7 AND hire_date >= '2024-01-01' | 136 | SCAN emp | SEARCH emp USING INDEX idx_dept_hire (dept_id=? AND hire_date>?) | SEARCH emp USING INDEX idx_hire_dept (hire_date>?) |
| dept_id = 7 only | 1018 | SCAN emp | SEARCH emp USING INDEX idx_dept_hire (dept_id=?) | SCAN emp |
| hire_date >= '2024-01-01' only | 7881 | SCAN emp | SCAN emp | SEARCH emp USING INDEX idx_hire_dept (hire_date>?) |

(SCAN = reads the whole table; SEARCH ... USING INDEX = jumps through the index.) Another database may choose differently from SQLite: this is real SQLite 3.45.1 output only.

**pandas equivalent:** pandas has no indexes of this kind (it filters in memory); this only confirms the row counts.
```python
m1 = (dfe["dept_id"] == 7) & (dfe["hire_date"] >= "2024-01-01")
result = pd.Series({"both": int(m1.sum()), "dept only": int((dfe["dept_id"] == 7).sum()),
                    "date only": int((dfe["hire_date"] >= "2024-01-01").sum())}).rename("rows").reset_index()
```
Result (actual run):
```text
    index  rows
     both   136
dept only  1018
date only  7881
```
**Edge cases:** If a filter matches most of the table, the optimiser may ignore the index anyway. Low-cardinality leading columns (e.g. only 2 genders) are poor first columns. Skip-scan optimisation (PostgreSQL 18, SQLite after `ANALYZE`) can reduce the penalty (from memory; not tested here).
**Likely follow-ups:**
- Does order matter for `ORDER BY`? Yes, an index can also supply sort order if columns match its order.
- How many columns? PostgreSQL docs advise sparing use; more than 3 rarely helps.
**Common mistakes:** Putting the range column first, creating one index per column and expecting them to combine, and never checking the plan.

### Q28 ⭐⭐ 🟡 Why is LIKE '%abc' slow while LIKE 'abc%' can use an index?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you understand that an index is a sorted list, so only a known starting point (a prefix) can be searched quickly.
**Say this in the interview:** An index is sorted from the first letter, like a dictionary. 'abc%' says where to start looking, so the database can jump there. '%abc' could begin with anything, so every entry must be checked.
**Explain simply:**
- A **B-tree index** keeps values sorted. Finding 'Abra...' is like opening a dictionary at A-b-r: all matches sit together.
- `LIKE '%bra%'` has a wildcard first, so matches are spread everywhere: no starting point, so the plan is a full scan (shown below).
- 'Can use an index' is conditional. In SQLite here, the plain index was **not** used for `LIKE 'Abra%'` because SQLite's `LIKE` ignores upper/lower case by default while a normal index is case-sensitive. It was used with a `COLLATE NOCASE` index, with `GLOB`, or with `PRAGMA case_sensitive_like=ON` (see table). That behaviour is shown by EXPLAIN here only; the optimiser rules are from memory (SQLite docs page was unreachable).
- PostgreSQL and MySQL also have conditions (PostgreSQL needs a `text_pattern_ops` index or the C collation for non-C locales; MySQL uses a B-tree index for a constant prefix): from memory, not run here. For 'contains' searches use full-text search or trigram indexes (PostgreSQL `pg_trgm`).
**Example:** HR search box: typing 'Abra' should find employees quickly, but searching for names *containing* 'bra' on 30,000 rows is a full scan.
**Sample data:** generated table `emp(emp_id, name)` with 30,000 names such as `Abrakamo123` (random syllables, `random.seed(11)`).

**SQL:**
```sql
-- SQLite 3.45.1 (run here)
CREATE INDEX idx_name ON emp(name);
EXPLAIN QUERY PLAN SELECT * FROM emp WHERE name LIKE 'Abra%';
EXPLAIN QUERY PLAN SELECT * FROM emp WHERE name LIKE '%bra%';
CREATE INDEX idx_name_nc ON emp(name COLLATE NOCASE);   -- the variant that makes LIKE indexable in SQLite
```

**Output (real plans):**

| setup | filter | real EXPLAIN QUERY PLAN |
|---|---|---|
| no index | LIKE 'Abra%' | SCAN emp |
| index on name (default BINARY) | LIKE 'Abra%' | SCAN emp |
| index on name (default BINARY) | GLOB 'Abra*' | SEARCH emp USING COVERING INDEX idx_name (name>? AND name<?) |
| index on name (default BINARY) | LIKE '%bra%' | SCAN emp |
| index on name COLLATE NOCASE | LIKE 'Abra%' | SEARCH emp USING COVERING INDEX idx_name_nc (name>? AND name<?) |
| index on name COLLATE NOCASE | LIKE '%bra%' | SCAN emp |
| default index, PRAGMA case_sensitive_like=ON | LIKE 'Abra%' | SEARCH emp USING COVERING INDEX idx_name (name>? AND name<?) |

Rows matching: `LIKE 'Abra%'` 275, `LIKE '%bra%'` 579.

**pandas equivalent:** no index concept; this only confirms the match counts.
```python
result = pd.Series({"starts with Abra": int(dfe["name"].str.startswith("Abra").sum()),
                    "contains bra": int(dfe["name"].str.contains("bra", regex=False).sum())}).rename("rows").reset_index()
```
Result (actual run):
```text
           index  rows
starts with Abra   275
    contains bra   579
```
**Edge cases:** Leading wildcard, wildcard in the middle (`'A%c'` uses the prefix `A` only), case-insensitive matching, and `LOWER(name) LIKE ...` (function on the column breaks the index, see Q10). Collation and character set matter in every database.
**Likely follow-ups:**
- How to make '%abc' fast? Store the reversed string and search prefix, full-text search, or trigram index.
- Does `LIKE 'abc%'` always use an index? No: depends on collation and optimiser (shown above).
**Common mistakes:** Saying 'prefix LIKE always uses the index', and applying functions to the column.

### Q29 ⭐⭐ 🟡 CTE vs temp table vs subquery: which is faster for reuse of an intermediate result?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know what each tool is for, and that 'faster' depends on the database and how often you reuse the result.
**Say this in the interview:** A CTE and a subquery are just ways of writing the query; the database may recompute them each time they are used. A temp table is stored once, so it can win when the same expensive result is reused many times or needs an index. I decide by testing the plan.
**Explain simply:**
- **Subquery**: a query inside a query. Fine for one use; you must copy it for a second use.
- **CTE** (`WITH name AS (...)`): a named, readable subquery. Whether it is computed once or each time it is referenced depends on the database (PostgreSQL 12+ and SQLite decide by rules; older versions differ: from memory).
- **Temp table**: really stored for the session. Computed once, can be indexed, and can be reused across several statements, but costs a write.
- The premise 'which is faster' has no fixed answer. Below, real SQLite plans for all three; run this on your own data volume.
**Example:** Departments whose payroll is above the average department payroll: the dept totals are needed twice (list and average). IT (170,000) and HR (113,000) qualify.
**Sample data:**

`employees`

| emp_id | name | dept | salary |
|---|---|---|---|
| 1 | Asha | HR | 52000 |
| 2 | Ravi | Sales | 48000 |
| 3 | Meena | IT | 90000 |
| 4 | Karan | IT | 80000 |
| 5 | Divya | HR | 61000 |
| 6 | Sunil | Admin | 30000 |
| 7 | Priya | Sales | 55000 |
| 8 | Neha | Admin | 32000 |

**SQL:**
```sql
-- CTE (run in SQLite 3.45.1)
WITH dept_total AS (
    SELECT dept, SUM(salary) AS total FROM employees GROUP BY dept
)
SELECT dept, total
FROM dept_total
WHERE total > (SELECT AVG(total) FROM dept_total)   -- the CTE is used twice
ORDER BY dept;

-- repeated subquery (run, same result)
SELECT dept, total
FROM (SELECT dept, SUM(salary) AS total FROM employees GROUP BY dept)
WHERE total > (SELECT AVG(total) FROM (SELECT dept, SUM(salary) AS total FROM employees GROUP BY dept))
ORDER BY dept;

-- temp table: computed once, then reused (run, same result)
CREATE TEMP TABLE dept_total_t AS SELECT dept, SUM(salary) AS total FROM employees GROUP BY dept;
SELECT dept, total FROM dept_total_t WHERE total > (SELECT AVG(total) FROM dept_total_t) ORDER BY dept;
```

**Output (all three identical):**

| dept | total |
|---|---|
| HR | 113000 |
| IT | 170000 |

Real plans here: CTE `['MATERIALIZE dept_total', 'SCAN employees', 'USE TEMP B-TREE FOR GROUP BY', 'SCAN dept_total', 'SCALAR SUBQUERY 2', 'SCAN dept_total', 'USE TEMP B-TREE FOR ORDER BY']`; subquery `['CO-ROUTINE (subquery-1)', 'SCAN employees', 'USE TEMP B-TREE FOR GROUP BY', 'SCAN (subquery-1)', 'SCALAR SUBQUERY 3', 'CO-ROUTINE (subquery-2)', 'SCAN employees', 'USE TEMP B-TREE FOR GROUP BY', 'SCAN (subquery-2)', 'USE TEMP B-TREE FOR ORDER BY']`; temp table `['SCAN dept_total_t', 'SCALAR SUBQUERY 1', 'SCAN dept_total_t', 'USE TEMP B-TREE FOR ORDER BY']`.

**pandas equivalent:**
```python
t = df.groupby("dept", as_index=False).agg(total=("salary", "sum"))
result = t[t["total"] > t["total"].mean()].sort_values("dept").reset_index(drop=True)
```
Result (actual run):
```text
dept  total
  HR 113000
  IT 170000
```
**Edge cases:** The temp table is not refreshed if base data changes mid-session. A CTE cannot be reused in a later, separate statement. Recursive logic needs a CTE. PostgreSQL 12+ lets you force `WITH x AS MATERIALIZED (...)` or `NOT MATERIALIZED` (from memory, not run here); SQL Server temp tables use `#name` / `SELECT ... INTO #t`; MySQL uses `CREATE TEMPORARY TABLE` (not run here).
**Likely follow-ups:**
- When is a temp table clearly better? Big intermediate result used many times, or needing an index, or multi-step ETL.
- When is a CTE better? Readability, recursion, single use.
**Common mistakes:** Believing CTEs always cache their result, and using temp tables for tiny one-off queries.

### Q30 ⭐⭐ 🟡 Compute a running total without window functions (self join or correlated subquery).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can build a running total from first principles: 'add up everything up to and including this row'.
**Say this in the interview:** For each row I add up all rows whose date is less than or equal to that row's date, either with a self join and GROUP BY or with a correlated subquery. The window function is shorter and faster, but this works on any database.
**Explain simply:**
- **Running (cumulative) total** = sales so far: day 1, day 1+2, day 1+2+3...
- Self join: every row `a` is paired with all rows `b` up to its date; `SUM(b.amount)` gives the total.
- Correlated subquery: for each row, a small query sums the earlier rows.
- Both re-read many rows: cost grows roughly with the square of the row count, so on millions of rows use `SUM() OVER (ORDER BY ...)`.
**Example:** Cumulative payroll cost through the year, or cumulative hires: 1,200 → 2,000 → 2,450...
**Sample data:**

`daily_sales`

| sale_date | amount |
|---|---|
| 2025-01-01 | 1200 |
| 2025-01-02 | 800 |
| 2025-01-03 | 450 |
| 2025-01-04 | 950 |
| 2025-01-05 | 700 |
| 2025-01-06 | 1100 |

**SQL:**
```sql
-- self join (SQLite 3.45.1, run here)
SELECT a.sale_date, a.amount, SUM(b.amount) AS running_total
FROM daily_sales a
JOIN daily_sales b ON b.sale_date <= a.sale_date     -- all rows up to this day
GROUP BY a.sale_date, a.amount
ORDER BY a.sale_date;

-- correlated subquery (run, same result)
SELECT a.sale_date, a.amount,
       (SELECT SUM(b.amount) FROM daily_sales b WHERE b.sale_date <= a.sale_date) AS running_total
FROM daily_sales a
ORDER BY a.sale_date;

-- window version for comparison (run, same result)
SELECT sale_date, amount, SUM(amount) OVER (ORDER BY sale_date) AS running_total FROM daily_sales ORDER BY sale_date;
```

**Output:**

| sale_date | amount | running_total |
|---|---|---|
| 2025-01-01 | 1200 | 1200 |
| 2025-01-02 | 800 | 2000 |
| 2025-01-03 | 450 | 2450 |
| 2025-01-04 | 950 | 3400 |
| 2025-01-05 | 700 | 4100 |
| 2025-01-06 | 1100 | 5200 |

All three returned identical rows.

**pandas equivalent:**
```python
result = df.sort_values("sale_date").assign(running_total=lambda d: d["amount"].cumsum()).reset_index(drop=True)
```
Result (actual run):
```text
 sale_date  amount  running_total
2025-01-01    1200           1200
2025-01-02     800           2000
2025-01-03     450           2450
2025-01-04     950           3400
2025-01-05     700           4100
2025-01-06    1100           5200
```
**Edge cases:** Ties: if two rows share the same date, `<=` makes both include each other, so they get the same total (the window default behaves the same way); to number rows use a unique key such as `(date, id)`. NULL amounts are skipped by `SUM`. Totals per group (per employee) need an extra `AND b.emp_id = a.emp_id`.
**Likely follow-ups:**
- Why is it slow? Quadratic work (each row scans earlier rows); an index on the date column helps but does not remove it.
- Running total per month? Add the group condition to the join.
**Common mistakes:** Using `<` instead of `<=` (misses the current row), joining without grouping, and forgetting ties.

### Q31 ⭐⭐ 🟡 Gaps and islands: group consecutive employee IDs into ranges with start and end (e.g., 1-3, 7-9).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know the classic "gaps and islands" trick: subtract a row number from the value so every consecutive run gets the same label.
**Say this in the interview:** I number the IDs 1, 2, 3... in order and subtract that number from each ID. Inside an unbroken run the answer stays constant, and it jumps whenever there is a gap. So I group by that constant and take MIN and MAX as the start and end.
**Explain simply:**
- An **island** is a block of consecutive values (1, 2, 3). A **gap** is the hole between two islands.
- `ROW_NUMBER()` is a **window function**: it hands out 1, 2, 3... down the sorted rows without collapsing them.
- IDs 1, 2, 3 minus row numbers 1, 2, 3 all give 0. ID 7 minus row number 4 gives 3, a new label, so 7 starts a new island.
- `GROUP BY` that label, then `MIN`/`MAX` give the range ends.
**Example:** Employee IDs issued to a department are 1, 2, 3, 7, 8, 9, 12. HR wants to know which ID blocks are in use: 1-3, 7-9 and 12-12.
**Sample data:**

`employees` (only emp_id matters; name omitted from the print)

| emp_id |
|---|
| 1 |
| 2 |
| 3 |
| 7 |
| 8 |
| 9 |
| 12 |

**SQL:**
```sql
WITH g AS (
  SELECT emp_id,
         emp_id - ROW_NUMBER() OVER (ORDER BY emp_id) AS grp   -- same grp = same island
  FROM employees
)
SELECT MIN(emp_id) AS start_id, MAX(emp_id) AS end_id, COUNT(*) AS ids_in_range,
       MIN(emp_id) || '-' || MAX(emp_id) AS range_text
FROM g
GROUP BY grp
ORDER BY start_id;
```

**Output:**

| start_id | end_id | ids_in_range | range_text |
|---|---|---|---|
| 1 | 3 | 3 | 1-3 |
| 7 | 9 | 3 | 7-9 |
| 12 | 12 | 1 | 12-12 |

**pandas equivalent:**
```python
e = employees.sort_values("emp_id").reset_index(drop=True)
e["grp"] = e["emp_id"] - (e.index + 1)          # same trick: id minus row number
result = (e.groupby("grp")["emp_id"].agg(start_id="min", end_id="max", ids_in_range="count")
            .reset_index(drop=True))
result["range_text"] = result["start_id"].astype(str) + "-" + result["end_id"].astype(str)
```
Result (actual run):
```text
 start_id  end_id  ids_in_range range_text
        1       3             3        1-3
        7       9             3        7-9
       12      12             1      12-12
```
**Edge cases:** The trick needs unique values: if an ID can repeat, use `SELECT DISTINCT` first or `DENSE_RANK()` instead of `ROW_NUMBER()`, or the labels drift. A single ID (12) becomes a range 12-12. NULL IDs should be filtered out. An empty table returns no rows. `||` joins text in SQLite/PostgreSQL; MySQL uses `CONCAT()`, SQL Server `CONCAT()` or `+` (not run here).
**Likely follow-ups:**
- *Same problem with dates?* Subtract the row number in days: `date - ROW_NUMBER()` (PostgreSQL `sale_date - rn * INTERVAL '1 day'`, not run here).
- *Do the gaps instead?* See Q42: use `LEAD` and compare to the next value.
**Common mistakes:** Using `RANK()` or forgetting `DISTINCT` (labels break with duplicates); ordering the window differently from the final `ORDER BY`; trying a self join when one window function does it.

### Q32 ⭐⭐ 🔴 Use a recursive CTE to build the full reporting chain as text (CEO > VP > Manager > Employee) for every employee.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can carry a growing text value through each step of a recursive CTE.
**Say this in the interview:** I start with the CEO, whose chain is just their name. Each recursive step joins employees whose manager is already in the result and appends their name to the manager's chain with a separator.
**Explain simply:**
- A **recursive CTE** is a query that refers to itself: an **anchor** part (the starting rows) plus a **recursive** part that repeats on the newest rows until nothing new appears.
- Here the anchor is the CEO (`manager_id IS NULL`). Step 2 finds the VPs, step 3 the managers, and so on.
- Each step builds the text as `parent chain || ' > ' || my name`, so the chain grows from the top down.
- `level` counts the layers, with CEO = 1.
**Example:** Karan reports to Rahul, who reports to Arjun, who reports to Meera, so Karan's chain is `Meera > Arjun > Rahul > Karan`.
**Sample data:**

`employees`

| emp_id | name | title | manager_id |
|---|---|---|---|
| 1 | Meera | CEO | NULL |
| 2 | Arjun | VP | 1 |
| 3 | Nisha | VP | 1 |
| 4 | Rahul | Manager | 2 |
| 5 | Priya | Manager | 3 |
| 6 | Karan | Employee | 4 |
| 7 | Divya | Employee | 4 |
| 8 | Sana | Employee | 5 |

**SQL:**
```sql
WITH RECURSIVE chain AS (
  SELECT emp_id, name, name AS reporting_chain, 1 AS level
  FROM employees
  WHERE manager_id IS NULL                       -- anchor: the CEO
  UNION ALL
  SELECT e.emp_id, e.name, c.reporting_chain || ' > ' || e.name, c.level + 1
  FROM employees e
  JOIN chain c ON e.manager_id = c.emp_id        -- recursive step: add the next layer down
)
SELECT emp_id, name, level, reporting_chain
FROM chain
ORDER BY emp_id;
```

**Output:**

| emp_id | name | level | reporting_chain |
|---|---|---|---|
| 1 | Meera | 1 | Meera |
| 2 | Arjun | 2 | Meera > Arjun |
| 3 | Nisha | 2 | Meera > Nisha |
| 4 | Rahul | 3 | Meera > Arjun > Rahul |
| 5 | Priya | 3 | Meera > Nisha > Priya |
| 6 | Karan | 4 | Meera > Arjun > Rahul > Karan |
| 7 | Divya | 4 | Meera > Arjun > Rahul > Divya |
| 8 | Sana | 4 | Meera > Nisha > Priya > Sana |

**pandas equivalent:**
```python
emp = employees.set_index("emp_id")
def chain(i):
    names = []
    while pd.notna(i):                       # walk upward until the CEO (manager NULL)
        names.append(emp.loc[i, "name"])
        i = emp.loc[i, "manager_id"]
    return names[::-1]
rows = [(i, emp.loc[i, "name"], len(chain(i)), " > ".join(chain(i))) for i in emp.index]
result = pd.DataFrame(rows, columns=["emp_id", "name", "level", "reporting_chain"])
```
Result (actual run):
```text
 emp_id  name  level               reporting_chain
      1 Meera      1                         Meera
      2 Arjun      2                 Meera > Arjun
      3 Nisha      2                 Meera > Nisha
      4 Rahul      3         Meera > Arjun > Rahul
      5 Priya      3         Meera > Nisha > Priya
      6 Karan      4 Meera > Arjun > Rahul > Karan
      7 Divya      4 Meera > Arjun > Rahul > Divya
      8  Sana      4  Meera > Nisha > Priya > Sana
```
**Edge cases:** Several roots (more than one NULL manager) give several chains, all fine. An employee whose manager_id points to a missing row never appears (the join finds no parent). A cycle makes the query loop: see Q33. `WITH RECURSIVE` is required in PostgreSQL, MySQL 8 and SQLite; SQL Server omits the word `RECURSIVE`; text join is `CONCAT()` in MySQL/SQL Server (not run here).
**Likely follow-ups:**
- *Show only Karan's chain?* Filter the final SELECT: `WHERE name = 'Karan'`.
- *Order the output as a tree?* PostgreSQL has `SEARCH DEPTH FIRST` (docs, not run here); otherwise sort by the chain text.
**Common mistakes:** Forgetting the anchor row; using the child's name in the wrong order (`e.name || c.chain` reverses the chain); joining on `e.emp_id = c.manager_id` (reversed direction, which walks upward instead of downward).

### Q33 ⭐⭐ 🔴 How do you stop a recursive CTE from looping forever when the hierarchy has a cycle?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know a recursive CTE can run forever on bad data and how to guard it.
**Say this in the interview:** I carry a path of IDs already visited, as text or an array, and in the recursive step I skip any row whose ID is already in that path. PostgreSQL 14+ also has a built-in `CYCLE` clause that does this for you.
**Explain simply:**
- A **cycle** means the data loops: Arjun reports to Rahul, Rahul to Nisha, Nisha to Arjun. Following the chain never reaches a top.
- A recursive CTE stops only when a step returns **zero new rows**. In a loop every step finds more rows, so it never stops.
- **Guard 1 (all dialects):** keep a `path` and refuse to revisit an ID. SQLite has no `CYCLE` clause, so I used a text path with `instr()`.
- **Guard 2 (blunt):** a depth cap such as `WHERE depth < 20`. It stops the loop but still returns repeated rows.
- Changing `UNION ALL` to `UNION` is not a reliable fix: per the PostgreSQL docs it does not help once a depth column makes every row look different.
**Example:** A bad HR import set Arjun's manager to Rahul, who is Arjun's own subordinate. A report on "everyone under Arjun" would loop without the guard.
**Sample data:** employees 2, 3, 4 form a loop (2 reports to 4, 4 to 3, 3 to 2). Employees 5 and 6 are a normal chain under the CEO.

`employees`

| emp_id | name | manager_id |
|---|---|---|
| 1 | Meera | NULL |
| 2 | Arjun | 4 |
| 3 | Nisha | 2 |
| 4 | Rahul | 3 |
| 5 | Priya | 1 |
| 6 | Karan | 5 |

**Without a guard (demo only, capped at depth 6):**
```sql
WITH RECURSIVE team AS (
  SELECT emp_id, name, 0 AS depth FROM employees WHERE emp_id = 2   -- start inside the loop
  UNION ALL
  SELECT e.emp_id, e.name, t.depth + 1
  FROM employees e JOIN team t ON e.manager_id = t.emp_id
  WHERE t.depth < 6                              -- demo-only safety cap; without it this never ends
)
SELECT depth, emp_id, name FROM team ORDER BY depth;
```
Output: the same three people repeat every step.

| depth | emp_id | name |
|---|---|---|
| 0 | 2 | Arjun |
| 1 | 3 | Nisha |
| 2 | 4 | Rahul |
| 3 | 2 | Arjun |
| 4 | 3 | Nisha |
| 5 | 4 | Rahul |
| 6 | 2 | Arjun |

**SQL:**
```sql
WITH RECURSIVE team AS (
  SELECT emp_id, name, 0 AS depth,
         ',' || emp_id || ',' AS path               -- visited IDs as text: ,2,
  FROM employees WHERE emp_id = 2
  UNION ALL
  SELECT e.emp_id, e.name, t.depth + 1,
         t.path || e.emp_id || ','
  FROM employees e JOIN team t ON e.manager_id = t.emp_id
  WHERE instr(t.path, ',' || e.emp_id || ',') = 0   -- skip anyone already on this path
)
SELECT depth, emp_id, name, path FROM team ORDER BY depth;
```

**Output (guarded, each person once):**

| depth | emp_id | name | path |
|---|---|---|---|
| 0 | 2 | Arjun | ,2, |
| 1 | 3 | Nisha | ,2,3, |
| 2 | 4 | Rahul | ,2,3,4, |

**pandas equivalent:**
```python
emp = employees.set_index("emp_id")
seen, frontier, depth, rows = {2}, [2], 0, [(0, 2, "Arjun", ",2,")]
paths = {2: ",2,"}
while frontier:                               # breadth-first walk with a visited set
    nxt = []
    for m in frontier:
        for e in emp.index[emp["manager_id"] == m]:
            if e not in seen:                 # the cycle guard
                seen.add(e); nxt.append(e)
                paths[e] = paths[m] + f"{e},"
                rows.append((depth + 1, e, emp.loc[e, "name"], paths[e]))
    frontier, depth = nxt, depth + 1
result = pd.DataFrame(rows, columns=["depth", "emp_id", "name", "path"])
```
Result (actual run):
```text
 depth  emp_id  name    path
     0       2 Arjun     ,2,
     1       3 Nisha   ,2,3,
     2       4 Rahul ,2,3,4,
```
**PostgreSQL built-in alternative (from the PostgreSQL docs, not run here):**
```sql
WITH RECURSIVE team AS (
  SELECT emp_id, manager_id FROM employees WHERE emp_id = 2
  UNION ALL
  SELECT e.emp_id, e.manager_id FROM employees e JOIN team t ON e.manager_id = t.emp_id
) CYCLE emp_id SET is_cycle USING path
SELECT * FROM team WHERE NOT is_cycle;
```
**Edge cases:** Starting from the CEO (employee 1) never reaches the loop, because each employee has only one manager, so nobody can be reached from two directions. The loop bites when you start inside it, when you walk upward (find all managers of X), or on a table with several roots. Path-as-text needs the surrounding commas, otherwise ID `1` matches inside `12`.
**Likely follow-ups:**
- *How do you find the bad rows?* Return rows where the next step would revisit an ID (the PostgreSQL `is_cycle` flag), then fix the source data.
- *Prevent it at the source?* A constraint cannot easily forbid cycles; use a validation query or a trigger (from memory, not run here).
**Common mistakes:** Believing `UNION` always prevents loops; relying only on a depth cap and shipping repeated rows; matching ID substrings without delimiters.

### Q34 ⭐⭐ 🔴 Merge overlapping date ranges (e.g., overlapping leave or booking periods) into single continuous periods.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** A harder gaps-and-islands: can you detect "this period starts after everything before it has ended" and number the blocks.
**Say this in the interview:** I sort each employee's periods by start date and look at the latest end date seen so far. If a period starts after that, there is a break and a new block begins; otherwise it overlaps and joins the current block. A running sum of those break flags numbers the blocks, then MIN start and MAX end give each merged period.
**Explain simply:**
- Sorting by start date means a period can only overlap what came before it.
- The **running maximum end** matters because of nested periods: Feb 3-5 sits inside Feb 1-10, so comparing to only the previous row's end would wrongly start a new block.
- `new_block = 1` marks the first row of each block. A **running SUM** of the 0/1 flags turns them into block numbers 1, 2, 3.
- `MAX(...) OVER (... ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING)` means "the biggest end date among all earlier rows".
**Example:** Jan 1-5 and Jan 3-8 overlap, so they merge into Jan 1-8. Jan 10-12 and Jan 11-15 merge into Jan 10-15. Employee 1 was on leave in two continuous stretches.
**Sample data:**

`leave_periods`

| emp_id | start_date | end_date |
|---|---|---|
| 1 | 2025-01-01 | 2025-01-05 |
| 1 | 2025-01-03 | 2025-01-08 |
| 1 | 2025-01-10 | 2025-01-12 |
| 1 | 2025-01-11 | 2025-01-15 |
| 2 | 2025-02-01 | 2025-02-10 |
| 2 | 2025-02-03 | 2025-02-05 |
| 2 | 2025-02-20 | 2025-02-22 |
| 3 | 2025-03-01 | 2025-03-05 |
| 3 | 2025-03-06 | 2025-03-08 |

**SQL:**
```sql
WITH o AS (
  SELECT emp_id, start_date, end_date,
         MAX(end_date) OVER (PARTITION BY emp_id ORDER BY start_date, end_date
                             ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS prev_end
  FROM leave_periods
),
f AS (
  SELECT *, CASE WHEN prev_end IS NULL OR start_date > prev_end THEN 1 ELSE 0 END AS new_block
  FROM o
),
g AS (
  SELECT *, SUM(new_block) OVER (PARTITION BY emp_id ORDER BY start_date, end_date) AS block
  FROM f
)
SELECT emp_id, MIN(start_date) AS block_start, MAX(end_date) AS block_end
FROM g
GROUP BY emp_id, block
ORDER BY emp_id, block_start;
```

**Output:**

| emp_id | block_start | block_end |
|---|---|---|
| 1 | 2025-01-01 | 2025-01-08 |
| 1 | 2025-01-10 | 2025-01-15 |
| 2 | 2025-02-01 | 2025-02-10 |
| 2 | 2025-02-20 | 2025-02-22 |
| 3 | 2025-03-01 | 2025-03-05 |
| 3 | 2025-03-06 | 2025-03-08 |

**pandas equivalent:**
```python
d = leave_periods.copy()
d["start_date"] = pd.to_datetime(d["start_date"]); d["end_date"] = pd.to_datetime(d["end_date"])
d = d.sort_values(["emp_id", "start_date", "end_date"])
d["prev_end"] = d.groupby("emp_id")["end_date"].transform(lambda s: s.cummax().shift())
d["block"] = (d["prev_end"].isna() | (d["start_date"] > d["prev_end"])).groupby(d["emp_id"]).cumsum()
result = (d.groupby(["emp_id", "block"]).agg(block_start=("start_date", "min"), block_end=("end_date", "max"))
            .reset_index().drop(columns="block"))
result["block_start"] = result["block_start"].dt.strftime("%Y-%m-%d")
result["block_end"] = result["block_end"].dt.strftime("%Y-%m-%d")
```
Result (actual run):
```text
 emp_id block_start  block_end
      1  2025-01-01 2025-01-08
      1  2025-01-10 2025-01-15
      2  2025-02-01 2025-02-10
      2  2025-02-20 2025-02-22
      3  2025-03-01 2025-03-05
      3  2025-03-06 2025-03-08
```
**Edge cases:** Employee 3 has Mar 1-5 then Mar 6-8: back-to-back days. With `start_date > prev_end` they stay separate (they do not overlap). To treat touching periods as one, compare `start_date > date(prev_end, '+1 day')` in SQLite (PostgreSQL: `prev_end + 1`; not run here). Nested periods (employee 2) are handled by the running max. NULL end dates (open-ended leave) need a decision, e.g. replace with a far-future date. Identical periods are fine. ISO `YYYY-MM-DD` text compares correctly; other formats do not.
**Likely follow-ups:**
- *Total distinct leave days per employee?* Sum `block_end - block_start + 1` over the merged blocks, so overlapping days are not double counted.
- *Can it be done without window functions?* Yes, with a self join anti-pattern, but it is longer and slower; I would use windows.
**Common mistakes:** Comparing to only the previous row's end (breaks on nested ranges); forgetting to sort by start date; using `>=` and `>` inconsistently with how the business counts touching days.

### Q35 ⭐ 🟢 Why do duplicates appear in HR or sales data in the first place, and how can constraints prevent them?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you understand duplicates as a data-pipeline and design problem, not just a query problem.
**Say this in the interview:** Duplicates come from re-run loads, manual re-entry, merging two systems, and tables with no unique key. I prevent them at the source with a PRIMARY KEY or UNIQUE constraint, and use UPSERT so a re-run updates instead of inserting twice.
**Explain simply:**
- **Common causes:** a file loaded twice, a form submitted twice, the same employee entered in two HR systems with slightly different spellings, or a join that multiplies rows.
- A **constraint** is a rule the database enforces. `PRIMARY KEY` means each row has a unique, non-NULL ID. `UNIQUE` means no two rows may share the value (for example email).
- An **UPSERT** ("update or insert") handles a repeat key gracefully: `INSERT ... ON CONFLICT DO UPDATE` (PostgreSQL, SQLite), `ON DUPLICATE KEY UPDATE` (MySQL), `MERGE` (SQL Server); the non-SQLite forms are not run here.
- Constraints only catch **exact** matches. `asha@corp.com` and `ASHA@corp.com` can slip through unless you normalise case, or use a case-insensitive column.
- Constraints on a table already full of duplicates cannot be added until you clean it first (see Q5, Q36).
**Example:** HR loads the January joiners file twice. With no constraint the payroll table has 2 rows per person and salaries are paid double; with `UNIQUE(emp_id, month)` the second load is rejected.
**Sample data / SQL (ran in SQLite):**
```sql
CREATE TABLE emp(emp_id INTEGER PRIMARY KEY, email TEXT UNIQUE, name TEXT);
INSERT INTO emp VALUES (1, 'asha@corp.com', 'Asha');
-- then each attempt below, one at a time:
INSERT INTO emp VALUES (2, 'asha@corp.com', 'Asha K');
INSERT INTO emp VALUES (3, 'ASHA@corp.com', 'Asha K');
INSERT INTO emp VALUES (4, NULL, 'Ravi');
INSERT INTO emp VALUES (5, NULL, 'Meena');
-- case-insensitive version
CREATE TABLE emp2(emp_id INTEGER PRIMARY KEY, email TEXT COLLATE NOCASE UNIQUE);
INSERT INTO emp2 VALUES (1, 'asha@corp.com');
INSERT INTO emp2 VALUES (2, 'ASHA@corp.com');
-- upsert so a re-run does not fail
INSERT INTO emp VALUES (1, 'asha@corp.com', 'Asha Nair')
ON CONFLICT(emp_id) DO UPDATE SET name = excluded.name;
```
**Output:**

| attempt | result |
|---|---|
| insert same email again | REJECTED: UNIQUE constraint failed: emp.email |
| insert same email, different case | accepted |
| insert NULL email | accepted |
| insert another NULL email | accepted |
| NOCASE column: same email, different case | REJECTED: UNIQUE constraint failed: emp2.email |

Plain-word reading: the exact repeat is blocked, the upper-case variant slips through in a normal column, NULLs are allowed more than once (SQLite, PostgreSQL and MySQL allow several NULLs under UNIQUE; SQL Server allows only one, from memory, not run here), and a NOCASE column blocks the case variant.
**Edge cases:** Composite keys (`UNIQUE(emp_id, month)`) catch duplicates that only exist as a pair. Near-duplicates (typos, extra spaces) need cleaning, not constraints. In a data warehouse, constraints are sometimes not enforced for speed, so dedupe in the load step.
**Likely follow-ups:**
- *PRIMARY KEY vs UNIQUE?* One primary key per table, never NULL; many UNIQUE constraints allowed.
- *What if the source keeps sending duplicates?* Dedupe in staging with ROW_NUMBER, then load the clean rows (Q5).
**Common mistakes:** Assuming a UNIQUE column also blocks case/space variants; adding a constraint without cleaning old duplicates first; relying on `SELECT DISTINCT` in every report instead of fixing the table.

### Q36 ⭐ 🟡 How would you safely delete duplicates from a table with hundreds of millions of rows (batches, staging table, transaction, backup)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Production thinking: safety, locking, rollback and cost on huge tables, not just the `DELETE` syntax.
**Say this in the interview:** I would not run one giant DELETE. I take a backup, build a de-duplicated copy in a staging table, verify the counts, then swap the tables inside a transaction and add a UNIQUE constraint. If an in-place delete is unavoidable, I delete in small batches so locks and the transaction log stay small.
**Explain simply:**
- A **transaction** is a group of steps that either all succeed or all undo (`ROLLBACK`). A huge single DELETE holds locks for a long time and can bloat the log.
- **Staging table:** write the clean rows to a new table instead of deleting from the old one. Copying 100M good rows is often cheaper and safer than deleting 20M bad ones, and the old table stays as your backup.
- **Batches:** delete e.g. 100,000 rows at a time in a loop so other users are not blocked for hours.
- **Verify** with counts (`rows_after = distinct keys`) before swapping, and keep the old table until the business signs off.
- Add a UNIQUE index afterwards so duplicates cannot come back (Q35).
**Example:** A 300-million-row attendance table has repeated swipes. Create `attendance_clean`, compare `COUNT(DISTINCT (emp_id, swipe_time))`, swap during a quiet window, and keep `attendance_old` for a week.
**Sample data:** `emp_raw` (7 rows, 4 distinct emails)

| id | email | updated |
|---|---|---|
| 1 | asha@corp.com | 2025-01-01 |
| 2 | ravi@corp.com | 2025-01-02 |
| 3 | asha@corp.com | 2025-03-01 |
| 4 | meena@corp.com | 2025-02-01 |
| 5 | ravi@corp.com | 2025-02-15 |
| 6 | asha@corp.com | 2025-04-01 |
| 7 | karan@corp.com | 2025-01-20 |

**SQL:** (ran in SQLite; the swap uses `ALTER TABLE ... RENAME`)
```sql
-- 1. Backup / snapshot first (here: a copy of the table)
CREATE TABLE emp_backup AS SELECT * FROM emp_raw;

-- 2. Build a clean copy in a staging table: keep the latest row per email
CREATE TABLE emp_clean AS
SELECT id, email, updated FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY email ORDER BY updated DESC, id DESC) AS rn
  FROM emp_raw
) WHERE rn = 1;

-- 3. Verify before swapping
SELECT (SELECT COUNT(*) FROM emp_raw)                   AS rows_before,
       (SELECT COUNT(DISTINCT email) FROM emp_raw)      AS distinct_emails,
       (SELECT COUNT(*) FROM emp_clean)                 AS rows_after,
       (SELECT COUNT(*) - COUNT(DISTINCT email) FROM emp_clean) AS dupes_left;

-- 4. Swap inside one transaction, then lock the door
BEGIN;
ALTER TABLE emp_raw RENAME TO emp_old;
ALTER TABLE emp_clean RENAME TO emp_raw;
COMMIT;
CREATE UNIQUE INDEX ux_emp_email ON emp_raw(email);
```
**Output** of the verification query (step 3), then the table after the swap:

| rows_before | distinct_emails | rows_after | dupes_left |
|---|---|---|---|
| 7 | 4 | 4 | 0 |

| id | email | updated |
|---|---|---|
| 4 | meena@corp.com | 2025-02-01 |
| 5 | ravi@corp.com | 2025-02-15 |
| 6 | asha@corp.com | 2025-04-01 |
| 7 | karan@corp.com | 2025-01-20 |

**Batch version** (the loop is driven from Python; in production use a stored procedure or a script). Each pass deletes at most 2 duplicates here (use 100,000 on the real table); the loop stops when a pass deletes 0:
```sql
DELETE FROM b WHERE id IN (
  SELECT id FROM (SELECT id, ROW_NUMBER() OVER (PARTITION BY email ORDER BY updated DESC, id DESC) AS rn FROM b)
  WHERE rn > 1 LIMIT 2);
```
| pass | rows_deleted | rows_left |
|---|---|---|
| 1 | 2 | 5 |
| 2 | 1 | 4 |
| 3 | 0 | 4 |

PostgreSQL has no `DELETE ... LIMIT`, so the `id IN (subquery LIMIT n)` form above is used; MySQL allows `DELETE ... LIMIT n` directly; SQL Server uses `DELETE TOP (n)` (not run here). On a billion-row table, the ROW_NUMBER subquery must be cheap: index the partition key.
**Edge cases:** Decide the survivor rule first (latest `updated`, lowest id, most complete row). Rows in other tables may reference the ids you delete (foreign keys): re-point them or keep the lowest id. NULL emails would all fall into one group: handle separately. Disk space: a staging copy needs room for the whole clean table. Tables being written to while you copy need a catch-up step or a maintenance window.
**Likely follow-ups:**
- *Why not just `DELETE`?* Long locks, huge log, slow rollback if it fails halfway.
- *How do you verify success?* Row counts, `COUNT(*) = COUNT(DISTINCT key)`, spot-check a few keys, compare totals (e.g. sum of salary) with the backup.
**Common mistakes:** No backup; deleting without a deterministic survivor rule (`ORDER BY` missing, so a different row is kept each run); one giant transaction; not adding the unique constraint afterwards.

### Q37 ⭐ 🟡 Find the median salary without a MEDIAN function.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can build a statistic from first principles with row numbers, and handle odd vs even counts.
**Say this in the interview:** I sort the salaries, number them, count how many there are, and pick the middle row. If the count is odd that is one row; if even, I average the two middle rows. The trick `rn IN ((n+1)/2, (n+2)/2)` picks one or two rows automatically.
**Explain simply:**
- The **median** is the middle value after sorting. Unlike the average it is not dragged up by one huge salary.
- With 5 salaries the middle is the 3rd. With 4 salaries it is the average of the 2nd and 3rd.
- With n = 4: (4+1)/2 = 2 and (4+2)/2 = 3 in integer division, so rows 2 and 3. With n = 3: 2 and 2, so only row 2 (the `IN` list collapses to one value).
- `COUNT(*) OVER (PARTITION BY dept)` is a window count: it puts the group size on every row without collapsing rows.
**Example:** Dept A salaries 30k, 40k, 50k, 90k: median = (40k+50k)/2 = 45,000, while the average is 52,500. The outlier 90k pulls the average up, not the median.
**Sample data:**

`employees`

| emp_id | dept | salary |
|---|---|---|
| 1 | A | 30000 |
| 2 | A | 40000 |
| 3 | A | 50000 |
| 4 | A | 90000 |
| 5 | B | 25000 |
| 6 | B | 35000 |
| 7 | B | 60000 |
| 8 | B | NULL |

**SQL:**
```sql
WITH r AS (
  SELECT dept, salary,
         ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary) AS rn,
         COUNT(*)     OVER (PARTITION BY dept)                 AS n
  FROM employees
  WHERE salary IS NOT NULL                         -- NULLs must not be counted or ranked
)
SELECT dept, AVG(salary) AS median_salary
FROM r
WHERE rn IN ((n + 1) / 2, (n + 2) / 2)             -- integer division: 1 middle row if n odd, 2 if even
GROUP BY dept
ORDER BY dept;
```

**Output:**

| dept | median_salary |
|---|---|
| A | 45000.0 |
| B | 35000.0 |

**pandas equivalent:**
```python
result = (employees.dropna(subset=["salary"]).groupby("dept")["salary"]
          .median().reset_index(name="median_salary"))
```
Result (actual run):
```text
dept  median_salary
   A        45000.0
   B        35000.0
```
**Edge cases:** NULL salaries are excluded before counting (dept B has 3 real salaries, so median 35,000, not a value from 4 rows). Ties are fine because `ROW_NUMBER` still gives distinct positions. An empty group returns no row. `/` is integer division on integers in SQLite and PostgreSQL; in MySQL `/` returns a decimal, so use `DIV` (not run here). Built-ins (not run here): `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary)` in PostgreSQL/Oracle/SQL Server (as a window function in SQL Server), `MEDIAN()` in Oracle.
**Likely follow-ups:**
- *Median across the whole company?* Remove `PARTITION BY dept` from both windows and the `GROUP BY`.
- *Any percentile?* Use `NTILE` or `PERCENTILE_CONT` where available.
**Common mistakes:** Averaging the wrong two rows for even counts; counting NULL salaries in `COUNT(*)`; using `AVG` and calling it a median; forgetting integer division behaves differently across databases.

### Q38 ⭐ 🟡 Why is OFFSET pagination slow on large tables, and what is keyset pagination?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you understand that `OFFSET n` still reads and throws away n rows, and know the keyset ("seek") alternative.
**Say this in the interview:** With OFFSET the database must walk past all the skipped rows every time, so page 10,000 is far slower than page 1, and rows can be skipped or repeated if data changes between pages. Keyset pagination remembers the last ID seen and asks for rows after it, so the database jumps straight there using the index.
**Explain simply:**
- **Pagination** means showing results a page at a time (20 employees per page).
- `LIMIT 20 OFFSET 400000` = "skip 400,000 rows, return the next 20". Skipping is not free: the engine still produces those rows first.
- **Keyset pagination** = `WHERE emp_id > :last_seen_id ORDER BY emp_id LIMIT 20`. With an index on `emp_id` the engine seeks directly to the start point.
- Downside: you can only go to next/previous, not "jump to page 500", and the sort column must be unique (or add a tie-breaker, below).
**Example:** An HR portal lists 5,00,000 attendance records. Page 25,000 with OFFSET is slow; with keyset it is as fast as page 1.
**Sample data:** `employees` with emp_id 1 to 10 (names `Emp1`...`Emp10`). Page size 3, page 3.
**SQL:**
```sql
-- OFFSET version
SELECT emp_id, name FROM employees ORDER BY emp_id LIMIT 3 OFFSET 6;
-- Keyset version (last id seen on page 2 was 6)
SELECT emp_id, name FROM employees WHERE emp_id > 6 ORDER BY emp_id LIMIT 3;
-- Keyset with a non-unique sort column (salary) needs a tie-breaker:
-- WHERE (salary, emp_id) > (:last_salary, :last_id) ORDER BY salary, emp_id LIMIT 3
-- (row-value comparison works in PostgreSQL, MySQL and SQLite 3.15+; not run here)
```
**Output** (identical pages):

OFFSET:

| emp_id | name |
|---|---|
| 7 | Emp7 |
| 8 | Emp8 |
| 9 | Emp9 |

Keyset:

| emp_id | name |
|---|---|
| 7 | Emp7 |
| 8 | Emp8 |
| 9 | Emp9 |

**What changes if a row is deleted while the user is browsing** (I deleted emp_id 2 after page 2 was shown; then re-ran both):

OFFSET now returns (7 got skipped):

| emp_id | name |
|---|---|
| 8 | Emp8 |
| 9 | Emp9 |
| 10 | Emp10 |

Keyset still returns:

| emp_id | name |
|---|---|
| 7 | Emp7 |
| 8 | Emp8 |
| 9 | Emp9 |

**Speed check** (my run, SQLite, 5,00,000-row table, best of 5, last page, milliseconds; machine-dependent, not a benchmark): OFFSET 499,980 took **3.91 ms**, keyset took **0.012 ms**, OFFSET 0 took 0.011 ms. The plans, from `EXPLAIN QUERY PLAN`: OFFSET: `SCAN employees`; keyset: `SEARCH employees USING INTEGER PRIMARY KEY (rowid>?)`.
**pandas equivalent:**
```python
e = employees.sort_values("emp_id")
offset_page = e.iloc[6:9]                         # skip 6 rows, take 3  (OFFSET 6 LIMIT 3)
keyset_page = e[e["emp_id"] > 6].head(3)          # "after the last id I saw", take 3
result = pd.concat([offset_page.assign(method="offset"), keyset_page.assign(method="keyset")])
```
Result (actual run):
```text
 emp_id name method
      7 Emp7 offset
      8 Emp8 offset
      9 Emp9 offset
      7 Emp7 keyset
      8 Emp8 keyset
      9 Emp9 keyset
```
**Edge cases:** Keyset needs a deterministic order: always include a unique tie-breaker (the primary key). NULLs in the sort column complicate the comparison. Going backwards needs the reverse comparison and reverse order. OFFSET is acceptable for small tables or admin screens with few pages.
**Likely follow-ups:**
- *Why does OFFSET skip or repeat rows?* Inserts/deletes before your position shift everything (shown above).
- *Can OFFSET be made fast?* Not fundamentally; the "deferred join" trick helps but still scans the skipped index entries (from memory, not run here).
**Common mistakes:** Paginating without `ORDER BY` (order is then not guaranteed); keyset on a non-unique column without a tie-breaker (rows silently dropped); using OFFSET for deep pages in a large table.

### Q39 ⭐ 🟡 What is a covering index and an index-only scan?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know an index can answer a query completely, so the database never visits the table.
**Say this in the interview:** A covering index contains every column the query needs, so the database answers from the index alone. That is called an index-only scan. It skips the extra trip to the table, which is the expensive part.
**Explain simply:**
- An **index** is a sorted shortcut list, like the index at the back of a book: it maps a value to the row location.
- Normally the database finds the row in the index, then **jumps to the table** to fetch other columns. That jump is the cost.
- A **covering index** includes the filter columns *and* the selected columns, e.g. `(dept, salary)` for `SELECT dept, salary ... WHERE dept = ...`. No jump needed.
- Ask for one extra column (`name`) that is not in the index and it is no longer covering.
- The cost: bigger indexes and slower inserts/updates, so cover only your hot queries.
**Example:** A dashboard repeatedly runs "salaries above 1 lakh by department". An index on `(dept, salary)` answers it from the index; the wide table (names, addresses) is never touched.
**Sample data:** `employees(emp_id, dept, salary, name, address)`, 5,000 generated rows (5 departments).
**SQL:** (ran in SQLite 3.45 using `EXPLAIN QUERY PLAN`)
```sql
-- query
SELECT dept, salary FROM employees WHERE dept = 'Sales' AND salary > 100000;
CREATE INDEX ix_dept ON employees(dept);               -- plain index
CREATE INDEX ix_dept_sal ON employees(dept, salary);   -- covering for this query
EXPLAIN QUERY PLAN SELECT dept, salary FROM employees WHERE dept = 'Sales' AND salary > 100000;
```
**Output** (the plan SQLite chose each time):

| setup | plan |
|---|---|
| no index | SCAN employees |
| index on (dept) | SEARCH employees USING INDEX ix_dept (dept=?) |
| index on (dept, salary) | SEARCH employees USING COVERING INDEX ix_dept_sal (dept=? AND salary>?) |
| same index, but query also asks for name | SEARCH employees USING INDEX ix_dept_sal (dept=? AND salary>?) |

SQLite says `COVERING INDEX` in its plan when it never reads the table. Other databases (PostgreSQL docs, https://www.postgresql.org/docs/current/indexes-index-only-scans.html; MySQL docs, https://dev.mysql.com/doc/refman/8.4/en/mysql-indexes.html):
```sql
-- PostgreSQL 11+ (not run here): extra columns carried in the index leaf only
CREATE INDEX ix_dept_cover ON employees (dept) INCLUDE (salary);
-- Plan then shows "Index Only Scan"
-- MySQL: covering index shows "Using index" in the Extra column of EXPLAIN (from the docs' covering-index description; not run here)
-- SQL Server: CREATE INDEX ... INCLUDE (salary)   (from memory, not run here)
```
**Edge cases:** PostgreSQL index-only scans still visit the table for pages not marked "all-visible" (the visibility map; `VACUUM` keeps it fresh), so the benefit shrinks on heavily updated tables. `INCLUDE` columns make the index bigger: the docs say to be conservative. Tiny tables or queries that read most rows can be faster with a plain scan.
**Likely follow-ups:**
- *Composite vs INCLUDE?* Key columns can be searched/sorted; INCLUDE columns are only stored for covering.
- *How do you check it worked?* Read the plan for "Index Only Scan" / "COVERING INDEX" / "Using index".
**Common mistakes:** Adding `SELECT *` to a covered query (it stops being covered, see Q15); indexing every column "just in case"; assuming an index-only scan never touches the table in PostgreSQL.

### Q40 ⭐ 🟡 When would you partition a large table, and how does partition pruning speed up queries?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know why and when to split a huge table, and what pruning means.
**Say this in the interview:** I partition a very large table, usually by date, so each month sits in its own physical chunk. A query for one month then reads only that chunk. The database skipping the other chunks is called partition pruning. It also makes dropping old data instant.
**Explain simply:**
- A **partitioned table** looks like one table but is stored as several smaller pieces, split by a **partition key** (e.g. `work_date`) using range, list or hash rules.
- **Partition pruning:** if the WHERE clause filters on the partition key, the optimiser ignores partitions that cannot contain matches.
- **When to use:** tables so large they will not fit comfortably in memory, with queries that mostly filter on the key (monthly reports), or where old data must be archived or purged (the PostgreSQL docs: dropping/detaching a partition is much faster than a bulk DELETE).
- **When not to:** small tables (overhead for no gain), or queries that do not filter on the partition key (all partitions are still read).
**Example:** A 2-billion-row swipe-log table partitioned by month. "February attendance" reads one partition; deleting 2022 data drops 12 partitions in seconds instead of deleting billions of rows.
**Demo:** SQLite has no declarative partitioning, so I imitated it with one table per month plus a UNION ALL view. Querying the right monthly table by hand is what pruning does automatically; querying the view shows what happens without pruning. 15 rows per month, 45 in total. Both queries count February rows:

`SELECT COUNT(*) FROM attendance_2025_02` returns:

| COUNT(*) |
|---|
| 15 |

`SELECT COUNT(*) FROM attendance WHERE work_date >= '2025-02-01' AND work_date < '2025-03-01'` returns:

| COUNT(*) |
|---|
| 15 |

**SQL (ran in SQLite 3.45; plans from `EXPLAIN QUERY PLAN`):**
```sql
CREATE TABLE attendance_2025_01 (emp_id INT, work_date TEXT, hours REAL);  -- same for _02, _03
CREATE VIEW attendance AS
  SELECT * FROM attendance_2025_01 UNION ALL SELECT * FROM attendance_2025_02 UNION ALL SELECT * FROM attendance_2025_03;
```
**Plan, one monthly table:** `SCAN attendance_2025_02`
**Plan, via the view (no pruning here):** `CO-ROUTINE attendance; COMPOUND QUERY; LEFT-MOST SUBQUERY; SCAN attendance_2025_01; UNION ALL; SCAN attendance_2025_02; UNION ALL; SCAN attendance_2025_03; SCAN attendance`

The view's plan touches all three months; a pruned plan would touch one.
**Real partitioning in PostgreSQL (from the docs https://www.postgresql.org/docs/current/ddl-partitioning.html; not run here):**
```sql
CREATE TABLE attendance (emp_id INT, work_date DATE, hours NUMERIC)
  PARTITION BY RANGE (work_date);
CREATE TABLE attendance_2025_02 PARTITION OF attendance
  FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');
-- Pruning shows up in EXPLAIN: only attendance_2025_02 is scanned
EXPLAIN SELECT * FROM attendance WHERE work_date = '2025-02-10';
-- Retire old data fast:
ALTER TABLE attendance DETACH PARTITION attendance_2025_01;
```
MySQL: `PARTITION BY RANGE (...)` in `CREATE TABLE`; SQL Server: partition function + scheme (from memory, not run here).
**Edge cases:** Pruning only works when the filter uses the partition key in a way the optimiser can evaluate; wrapping it in a function (`MONTH(work_date) = 2`) can defeat it (same non-sargable idea as Q10). Rows that match no partition are rejected unless a default partition exists. Too many tiny partitions slow planning. In PostgreSQL, a primary key or unique index on a partitioned table must include the partition key.
**Likely follow-ups:**
- *Partitioning vs indexing?* Indexes speed lookups of a few rows; partitioning helps scans of a slice and data lifecycle. They are used together.
- *Range vs list vs hash?* Range: dates; list: region codes; hash: spread evenly when there is no natural range.
**Common mistakes:** Partitioning a small table; choosing a key the queries never filter on; thinking partitioning replaces indexes.

### Q41 ⭐ 🔴 For every manager, compute total team headcount (direct plus indirect) using a recursive CTE.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can aggregate over a recursive result, not just list it.
**Say this in the interview:** I use a recursive CTE to build every (manager, person under them) pair, direct and indirect, then COUNT per manager. A LEFT JOIN from the employee table keeps people with no team at zero.
**Explain simply:**
- **Direct** reports are one level down; **indirect** are reports of reports, any depth.
- The anchor puts every direct pair in: (Meera, Arjun), (Arjun, Rahul)...
- The recursive step says: if X manages U and U manages E, then X also (indirectly) manages E, so add the pair (X, E). It repeats until no new pairs appear.
- Then it is an ordinary `GROUP BY manager COUNT(*)` over those pairs.
**Example:** Rahul manages Karan and Divya: headcount 2. Arjun manages Rahul plus Rahul's two: 3. Meera, the CEO, has everyone else: 7.
**Sample data:**

`employees`

| emp_id | name | title | manager_id |
|---|---|---|---|
| 1 | Meera | CEO | NULL |
| 2 | Arjun | VP | 1 |
| 3 | Nisha | VP | 1 |
| 4 | Rahul | Manager | 2 |
| 5 | Priya | Manager | 3 |
| 6 | Karan | Employee | 4 |
| 7 | Divya | Employee | 4 |
| 8 | Sana | Employee | 5 |

**SQL:**
```sql
WITH RECURSIVE under_mgr(manager_id, emp_id) AS (
  SELECT manager_id, emp_id                       -- anchor: every direct report as a pair (boss, person)
  FROM employees WHERE manager_id IS NOT NULL
  UNION ALL
  SELECT u.manager_id, e.emp_id                   -- boss of the boss' reports inherits their reports
  FROM under_mgr u
  JOIN employees e ON e.manager_id = u.emp_id
)
SELECT m.emp_id AS manager_id, m.name,
       COUNT(u.emp_id) AS team_headcount          -- 0 for people with no team
FROM employees m
LEFT JOIN under_mgr u ON u.manager_id = m.emp_id
GROUP BY m.emp_id, m.name
ORDER BY team_headcount DESC, m.emp_id;
```

**Output:**

| manager_id | name | team_headcount |
|---|---|---|
| 1 | Meera | 7 |
| 2 | Arjun | 3 |
| 3 | Nisha | 2 |
| 4 | Rahul | 2 |
| 5 | Priya | 1 |
| 6 | Karan | 0 |
| 7 | Divya | 0 |
| 8 | Sana | 0 |

**pandas equivalent:**
```python
emp = employees.set_index("emp_id")
def team(m):
    out, stack = [], [m]
    while stack:
        cur = stack.pop()
        kids = emp.index[emp["manager_id"] == cur].tolist()
        out += kids; stack += kids
    return out
rows = [(i, emp.loc[i, "name"], len(team(i))) for i in emp.index]
result = (pd.DataFrame(rows, columns=["manager_id", "name", "team_headcount"])
            .sort_values(["team_headcount", "manager_id"], ascending=[False, True]).reset_index(drop=True))
```
Result (actual run):
```text
 manager_id  name  team_headcount
          1 Meera               7
          2 Arjun               3
          3 Nisha               2
          4 Rahul               2
          5 Priya               1
          6 Karan               0
          7 Divya               0
          8  Sana               0
```
**Edge cases:** Employees with no reports get 0 thanks to the LEFT JOIN plus `COUNT(u.emp_id)` (not `COUNT(*)`, which would give 1). A cycle in the data would loop (use the path guard from Q33). On a deep, wide company the pairs table can be large: it grows with the sum of every person's depth. In SQL Server drop the word `RECURSIVE`.
**Likely follow-ups:**
- *Include the manager in the count?* Add 1.
- *Count only people who manage others?* Use an inner join instead of the LEFT JOIN.
**Common mistakes:** Counting only direct reports (a plain `GROUP BY manager_id`); using `COUNT(*)` after a LEFT JOIN, which returns 1 for leaf employees; joining the pairs the wrong way round and producing "number of bosses" instead.

### Q42 ⭐ 🔴 Gaps report: list missing date ranges (start and end of each gap) in a daily sales table.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Gaps (not islands): can you report the holes themselves, with start and end, using LEAD.
**Say this in the interview:** For each sales date I look at the next sales date with LEAD. If the next date is more than one day away, the days in between are missing: the gap starts the day after the current date and ends the day before the next one.
**Explain simply:**
- `LEAD(col)` is a **window function** that reads the value from the *next* row in the chosen order, on the same line.
- Normal consecutive days differ by 1. A difference of 4 means 3 days are missing.
- Gap start = current date + 1 day; gap end = next date - 1 day.
- Rows where there is no next date (the last day) give NULL and drop out of the `WHERE` automatically.
**Example:** Sales on Jun 1, 2, 3 then Jun 7: the store had no sales on Jun 4, 5, 6 (3 missing days): perhaps a holiday or a data-feed failure worth chasing.
**Sample data:**

`daily_sales`

| sale_date | amount |
|---|---|
| 2025-06-01 | 500 |
| 2025-06-02 | 650 |
| 2025-06-03 | 400 |
| 2025-06-07 | 900 |
| 2025-06-08 | 700 |
| 2025-06-12 | 300 |
| 2025-06-15 | 800 |

**SQL:**
```sql
WITH d AS (
  SELECT DISTINCT sale_date FROM daily_sales
),
n AS (
  SELECT sale_date, LEAD(sale_date) OVER (ORDER BY sale_date) AS next_date
  FROM d
)
SELECT date(sale_date, '+1 day')  AS gap_start,
       date(next_date, '-1 day')  AS gap_end,
       CAST(julianday(next_date) - julianday(sale_date) - 1 AS INTEGER) AS missing_days
FROM n
WHERE julianday(next_date) - julianday(sale_date) > 1     -- more than 1 day to the next sale = gap
ORDER BY gap_start;
```

**Output:**

| gap_start | gap_end | missing_days |
|---|---|---|
| 2025-06-04 | 2025-06-06 | 3 |
| 2025-06-09 | 2025-06-11 | 3 |
| 2025-06-13 | 2025-06-14 | 2 |

**pandas equivalent:**
```python
d = pd.DataFrame({"sale_date": pd.to_datetime(sorted(daily_sales["sale_date"].unique()))})
d["next_date"] = d["sale_date"].shift(-1)
g = d[(d["next_date"] - d["sale_date"]).dt.days > 1]
result = pd.DataFrame({
    "gap_start": (g["sale_date"] + pd.Timedelta(days=1)).dt.strftime("%Y-%m-%d"),
    "gap_end": (g["next_date"] - pd.Timedelta(days=1)).dt.strftime("%Y-%m-%d"),
    "missing_days": (g["next_date"] - g["sale_date"]).dt.days - 1}).reset_index(drop=True)
```
Result (actual run):
```text
 gap_start    gap_end  missing_days
2025-06-04 2025-06-06             3
2025-06-09 2025-06-11             3
2025-06-13 2025-06-14             2
```
**Edge cases:** Gaps before the first or after the last sale are invisible to this query; to include them, compare with a calendar table (Q23) or add the reporting period's start and end as extra anchor rows. Several rows per day are collapsed with `DISTINCT`. NULL dates must be filtered out first. Dialects (not run here): PostgreSQL `next_date - sale_date > 1` and `sale_date + 1`; MySQL `DATEDIFF(next_date, sale_date) > 1` and `DATE_ADD(sale_date, INTERVAL 1 DAY)`; SQL Server `DATEDIFF(day, sale_date, next_date)` and `DATEADD(day, 1, sale_date)`.
**Likely follow-ups:**
- *Which days were missing, one per row?* Join a generated calendar (Q23) and keep dates with no sales.
- *Weekends should not count as gaps?* Add a business-day calendar table and compare against that.
**Common mistakes:** Reporting the existing dates around the gap instead of the missing dates (off by one); forgetting `DISTINCT` when there are multiple sales per day; expecting to see gaps at the edges of the period.

### Q43 ⭐ 🔴 Rewrite a slow correlated subquery as a JOIN or window function and prove the improvement using EXPLAIN ANALYZE.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can rewrite a per-row subquery as a set-based query and prove it with a plan and timing instead of guessing.
**Say this in the interview:** A correlated subquery may re-run once per outer row. I rewrite it as a join to a pre-aggregated subquery, or as a window function, which computes the averages once. Then I compare plans and actual timings with EXPLAIN ANALYZE. Always check the results are identical.
**Explain simply:**
- A **correlated subquery** refers to a column of the outer query (`e.dept_id`), so conceptually it runs again for each outer row: 4,000 employees means 4,000 average calculations.
- The **join** version calculates each department's average once (`GROUP BY dept_id`), then matches rows to it.
- The **window** version (`AVG() OVER (PARTITION BY dept_id)`) does the same in a single pass without collapsing rows.
- Modern optimisers can sometimes rewrite a correlated subquery themselves, so never assume: measure.
**Example:** "Employees paid above their own department's average": the classic HR query.
**Sample data:**

`employees`

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 10 | 60000 |
| 2 | Ravi | 10 | 40000 |
| 3 | Meena | 10 | 80000 |
| 4 | Karan | 20 | 50000 |
| 5 | Divya | 20 | 70000 |
| 6 | Sana | 30 | 90000 |

**SQL:** (all three ran; the original, then two rewrites)
```sql
-- 1. Correlated subquery (original)
SELECT e.emp_id, e.dept_id, e.salary
FROM employees e
WHERE e.salary > (SELECT AVG(e2.salary) FROM employees e2 WHERE e2.dept_id = e.dept_id)
ORDER BY e.emp_id;
-- 2. JOIN to a pre-aggregated subquery
SELECT e.emp_id, e.dept_id, e.salary
FROM employees e
JOIN (SELECT dept_id, AVG(salary) AS avg_sal FROM employees GROUP BY dept_id) d
  ON d.dept_id = e.dept_id
WHERE e.salary > d.avg_sal
ORDER BY e.emp_id;
-- 3. Window function
SELECT emp_id, dept_id, salary
FROM (SELECT *, AVG(salary) OVER (PARTITION BY dept_id) AS avg_sal FROM employees)
WHERE salary > avg_sal
ORDER BY emp_id;
```
**Output** (identical for all three, checked by the script):

| emp_id | dept_id | salary |
|---|---|---|
| 3 | 10 | 80000 |
| 5 | 20 | 70000 |

**pandas equivalent:**
```python
avg_sal = employees.groupby("dept_id")["salary"].transform("mean")   # window-style average per row
result = employees[employees["salary"] > avg_sal][["emp_id", "dept_id", "salary"]].sort_values("emp_id")
```
Result (actual run):
```text
 emp_id  dept_id  salary
      3       10   80000
      5       20   70000
```
**Proof.** PostgreSQL's `EXPLAIN ANALYZE` (executes the query and reports `actual time`, real `rows` and `loops`; wrap INSERT/UPDATE/DELETE in `BEGIN ... ROLLBACK`; from the docs https://www.postgresql.org/docs/current/using-explain.html) is not available here, and SQLite has **no EXPLAIN ANALYZE**. So the premise changes slightly: I used SQLite's `EXPLAIN QUERY PLAN` plus wall-clock timing on a generated 4,000-employee, 40-department table (best of 3, milliseconds, machine-dependent):

| version | time_ms | rows_returned | plan (SQLite) |
|---|---|---|---|
| correlated subquery, no index | 604.0 | 1969 | SCAN e; CORRELATED SCALAR SUBQUERY 1; SEARCH e2 USING COVERING INDEX ix_d (dept_id=?) |
| correlated subquery, index on (dept_id, salary) | 23.1 | 1969 | SCAN e; CORRELATED SCALAR SUBQUERY 1; SEARCH e2 USING COVERING INDEX ix_d (dept_id=?) |
| join to pre-aggregated subquery | 2.9 | 1969 | CO-ROUTINE d; SCAN employees; USE TEMP B-TREE FOR GROUP BY; SCAN e; BLOOM FILTER ON d (dept_id=?); SEARCH d USING AUTOMATIC COVERING INDEX (dept_id=?) |
| window function | 4.2 | 1969 | CO-ROUTINE (subquery-1); CO-ROUTINE (subquery-3); SCAN employees; USE TEMP B-TREE FOR ORDER BY; SCAN (subquery-3); SCAN (subquery-1); USE TEMP B-TREE FOR ORDER BY |

In PostgreSQL I would look for: the subquery node with a large `loops=` number (re-executed per row), `actual time` totals, `Rows Removed by Filter`, and an estimate-vs-actual row mismatch (stale statistics; run `ANALYZE`). PostgreSQL syntax: `EXPLAIN (ANALYZE, BUFFERS) <query>;` (not run here).
**Edge cases:** Ties and NULLs: `AVG` ignores NULL salaries; an employee with NULL salary never passes `salary > avg`. A department with one employee never exceeds its own average. If the subquery can return several rows or use `COUNT`, a join rewrite can change results (e.g. missing groups need a LEFT JOIN with COALESCE): always diff the outputs. A good index can make the correlated form fast too (see the second row).
**Likely follow-ups:**
- *Join or window, which wins?* Often similar; the window avoids a second pass over the table in some engines; test on your data.
- *Why does an index help the original?* It lets each per-row lookup avoid scanning the whole table.
**Common mistakes:** Claiming a speed-up without comparing results; timing once on a cold cache; comparing plans from different data volumes; using `EXPLAIN ANALYZE` on a DELETE without a transaction (it really deletes).

