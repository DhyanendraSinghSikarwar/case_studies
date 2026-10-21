# Book 2 — SQL | Part 4: Subqueries & CTEs 🟡

**Target:** 55 | **Actual:** 55

**Scope:** subqueries (scalar, correlated, derived tables, IN/EXISTS/NOT IN/ANY/ALL), CTEs (WITH, multiple CTEs, scope), subquery vs CTE vs temp table vs view. Window-function ranking, nth-highest, de-duplication and recursive CTEs are covered in Parts 5 and 10.

---

### Q1 ⭐⭐⭐ 🟢 What is a subquery in SQL? Give a simple example (e.g., employees earning more than the company average salary).
**Asked at:** commonly asked in data-analyst interviews; a generic interview guide (LearnSQL) lists it. No company-specific report found.
**What the interviewer is checking:** Do you know a query can sit inside another query, and can you write the classic 'above average' example?
**Say this in the interview:** A subquery is a query inside another query. The inner one runs first and hands its answer to the outer one. For example, I find the company average salary in the inner query, then the outer query lists everyone paid above it.
**Explain simply:**
- A subquery (also called an inner or nested query) is a SELECT written inside brackets within another SELECT, UPDATE or DELETE.
- The database works out the inner result first, then uses it like a plain value or list in the outer query.
- Think of it as two HR steps: step 1 'what is the average pay?', step 2 'who earns more than that?'. One query does both.
- It can return one value (scalar), one column of many values (used with IN), or a whole table (used in FROM).
**Example:** Average salary across 8 employees is 75,000. Four people earn more: Chitra 80k, Esha 90k, Farhan 120k, Gita 90k.
**Sample data:**

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 80000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farhan | 3 | 120000 |
| 7 | Gita | 3 | 90000 |
| 8 | Hari | 4 | 40000 |

**SQL:**
```sql
SELECT emp_id, name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)   -- inner query: runs first, returns 75000
ORDER BY emp_id;
```
**Output:**

| emp_id | name | salary |
|---|---|---|
| 3 | Chitra | 80000 |
| 5 | Esha | 90000 |
| 6 | Farhan | 120000 |
| 7 | Gita | 90000 |

**pandas equivalent:**
```python
result = employees[employees.salary > employees.salary.mean()][['emp_id','name','salary']]
```
**Edge cases:** If `salary` is NULL for someone, AVG ignores that row and the comparison `NULL > 75000` is unknown, so that person is not returned. An empty table makes AVG return NULL and the result is empty.
**Likely follow-ups:**
- Why not `WHERE salary > AVG(salary)`? Aggregate functions are not allowed in WHERE; the subquery gets around that.
- Can you do it with a join instead? Yes, a cross join to a one-row average table, but the subquery is more readable.
**Common mistakes:** Writing `WHERE salary > AVG(salary)` directly (error). Forgetting the brackets around the inner query. Returning two columns from a subquery that is compared with `>`.

### Q2 ⭐⭐⭐ 🟢 What is a CTE (Common Table Expression)? Write a simple one using the WITH keyword and explain when you would use it.
**Asked at:** service MNC, GCC and startup reviews mention CTEs (Wipro, Microsoft Hyderabad, Infosys, Meesho candidate reports); candidate-reported, thin evidence.
**What the interviewer is checking:** Can you write WITH ... AS correctly and say why it helps readability?
**Say this in the interview:** A CTE, or Common Table Expression, is a named temporary result I define with WITH at the top of a query, then use like a table underneath. I use it to break a long query into small named steps that read top to bottom.
**Explain simply:**
- CTE = a named mini-result that lives only while the one query runs. Nothing is saved in the database.
- Syntax: `WITH name AS ( SELECT ... ) SELECT ... FROM name`.
- Use it when the same logic is needed twice, when nesting makes the query hard to read, or when you want to build a result in steps (count headcount first, then filter it).
- SQL Server needs the statement before WITH to end with a semicolon. MySQL supports it from version 8.0; PostgreSQL, SQLite, Oracle and SQL Server support it for years.
**Example:** HR asks 'which departments have at least 2 people?'. Step 1 is the CTE that counts people per department. Step 2 joins to names and filters.
**Sample data:**

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 80000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farhan | 3 | 120000 |
| 7 | Gita | 3 | 90000 |
| 8 | Hari | 4 | 40000 |

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Finance |
| 3 | IT |
| 4 | Sales |
| 5 | Legal |

**SQL:**
```sql
WITH dept_headcount AS (            -- CTE: a named, temporary result for this query only
    SELECT dept_id, COUNT(*) AS headcount
    FROM employees
    GROUP BY dept_id
)
SELECT d.dept_name, h.headcount
FROM dept_headcount h
JOIN departments d ON d.dept_id = h.dept_id
WHERE h.headcount >= 2
ORDER BY d.dept_name;
```
**Output:**

| dept_name | headcount |
|---|---|
| Finance | 2 |
| HR | 2 |
| IT | 3 |

**pandas equivalent:**
```python
hc = employees.groupby('dept_id', as_index=False).agg(headcount=('emp_id','count'))
hc = hc[hc.headcount >= 2]
result = hc.merge(departments, on='dept_id')[['dept_name','headcount']].sort_values('dept_name').reset_index(drop=True)
```
**Edge cases:** Departments with no employees (Legal) never appear in the CTE because GROUP BY only sees existing rows. A CTE name can hide a real table name if you reuse it, so choose distinct names.
**Likely follow-ups:**
- Does a CTE save data? No, it is gone when the query ends.
- Can I reference a CTE twice? Yes, in the same statement.
**Common mistakes:** Trying to use the CTE in a second query (it is out of scope). Forgetting the comma between two CTEs. Naming the CTE the same as a real table.

### Q3 ⭐⭐⭐ 🟡 What is the difference between a subquery and a CTE? When would you choose one over the other?
**Asked at:** candidate-reported at Meesho (startup), Infosys (service MNC) and a small firm via AmbitionBox; also in Indeed-style guides. One Hyderabad analytics-firm panel reportedly preferred plain nested SQL, so be ready to defend either.
**What the interviewer is checking:** Do you understand they usually give the same answer and the choice is about readability and reuse?
**Say this in the interview:** A subquery is a query nested inside another one; a CTE is the same logic given a name at the top with WITH. For one small use I am happy with a subquery. If the logic is long, reused, or needs explaining to a teammate, I choose a CTE.
**Explain simply:**
- Both return the same result here. The database often treats them the same internally.
- Subquery: sits inside WHERE / FROM / SELECT. Good for one-off, short logic.
- CTE: named, defined first, can be referenced many times, can be chained (CTE 2 uses CTE 1), and supports recursion (org charts).
- A CTE is not automatically faster, it is mostly about clarity (see Q28).
**Example:** HR wants staff in departments with 3 or more people (only IT, with Esha, Farhan, Gita). Same answer from both versions below.
**Sample data:**

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 80000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farhan | 3 | 120000 |
| 7 | Gita | 3 | 90000 |
| 8 | Hari | 4 | 40000 |

**SQL:**
```sql
-- 1) Subquery version
SELECT name, salary
FROM employees
WHERE dept_id IN (SELECT dept_id FROM employees GROUP BY dept_id HAVING COUNT(*) >= 3)
ORDER BY emp_id;

-- 2) CTE version
WITH big_depts AS (
    SELECT dept_id FROM employees GROUP BY dept_id HAVING COUNT(*) >= 3
)
SELECT name, salary
FROM employees
WHERE dept_id IN (SELECT dept_id FROM big_depts)
ORDER BY emp_id;
```
**Output:**

| name | salary |
|---|---|
| Esha | 90000 |
| Farhan | 120000 |
| Gita | 90000 |

(The CTE version returned exactly the same rows.)

**pandas equivalent:**
```python
big = employees.groupby('dept_id').emp_id.count().loc[lambda s: s >= 3].index
result = employees[employees.dept_id.isin(big)][['name','salary']]
```
**Edge cases:** Same results, including NULL handling, because the logic is identical. Only recursive logic cannot be done with a plain subquery.
**Likely follow-ups:**
- Which is faster? Usually the same; check EXPLAIN (Q53).
- When is a subquery better? Tiny one-liners, or when a team prefers traditional style.
**Common mistakes:** Saying a CTE is always faster or always stores its result. Using a CTE only once for a trivial condition and making the query longer for no gain.

### Q4 ⭐⭐⭐ 🟡 Find all employees whose salary is above the company average (subquery in WHERE).
**Asked at:** commonly asked (no company-specific report found) (the classic first subquery question).
**What the interviewer is checking:** Can you put a scalar subquery (one value) in WHERE?
**Say this in the interview:** I calculate the company average in a bracketed subquery and compare each salary to it in WHERE. The subquery returns one number, so I can use a plain greater-than.
**Explain simply:**
- Inner query: `SELECT AVG(salary) FROM employees` returns one value, 75000. This is called a scalar subquery.
- Outer query: keep rows whose salary is greater than that one value.
- You cannot write AVG directly in WHERE because aggregates are computed after WHERE filters rows; the subquery is the way around it.
- Total payroll is 600,000 over 8 people, so the average is 75,000.
**Example:** Farhan (120k) is the highest earner; Hari (40k) is lowest. Four people are above average.
**Sample data:**

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 80000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farhan | 3 | 120000 |
| 7 | Gita | 3 | 90000 |
| 8 | Hari | 4 | 40000 |

**SQL:**
```sql
SELECT emp_id, name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)
ORDER BY salary DESC, emp_id;
```
**Output:**

| emp_id | name | salary |
|---|---|---|
| 6 | Farhan | 120000 |
| 5 | Esha | 90000 |
| 7 | Gita | 90000 |
| 3 | Chitra | 80000 |

**pandas equivalent:**
```python
avg = employees.salary.mean()
result = employees[employees.salary > avg].sort_values(['salary','emp_id'], ascending=[False, True])[['emp_id','name','salary']].reset_index(drop=True)
```
**Edge cases:** Equal-to-average rows are excluded by `>` (use `>=` if the policy says so). NULL salaries are ignored by AVG and never returned. Ties: Esha and Gita both earn 90k, so ORDER BY adds emp_id as a tiebreaker.
**Likely follow-ups:**
- How would you include the average as a column? Subquery in SELECT (Q19).
- Above average per department? Correlated subquery (Q5).
**Common mistakes:** Using WHERE salary > AVG(salary). Comparing to the average of the wrong group. Forgetting that AVG skips NULLs.

### Q5 ⭐⭐⭐ 🟡 Find employees who earn more than the average salary of their own department (correlated subquery).
**Asked at:** commonly asked; correlated subqueries appear in a Deloitte-type consulting/analytics report (candidate-reported on AmbitionBox, not verified in full). Department-level salary queries also reported at Wipro and Amazon.
**What the interviewer is checking:** Do you understand the inner query re-runs per outer row using that row's department?
**Say this in the interview:** Here the inner query depends on the outer row. For each employee it looks at that person's department, calculates the department average, and the outer query keeps the person only if they beat it. That dependence is what makes it correlated.
**Explain simply:**
- Correlated = the inner query refers to a column from the outer query (`e.dept_id`). It cannot run alone.
- Think of HR checking each employee's pay against only their own team's average, not the whole company.
- Department averages: HR 55,000; Finance 75,000; IT 100,000; Sales 40,000.
- Result: Bala (60k>55k), Chitra (80k>75k), Farhan (120k>100k). Hari is alone in Sales, so he equals his average and is excluded.
**Example:** Bala earns 60k in HR where the average is 55k, so he is above his team average, even though 60k is below the company average of 75k.
**Sample data:**

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 80000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farhan | 3 | 120000 |
| 7 | Gita | 3 | 90000 |
| 8 | Hari | 4 | 40000 |

**SQL:**
```sql
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE e.salary > (SELECT AVG(x.salary)
                  FROM employees x
                  WHERE x.dept_id = e.dept_id)   -- inner query uses the outer row's dept_id
ORDER BY e.emp_id;
```
**Output:**

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 80000 |
| 6 | Farhan | 3 | 120000 |

**pandas equivalent:**
```python
employees['dept_avg'] = employees.groupby('dept_id').salary.transform('mean')
result = employees[employees.salary > employees.dept_avg][['emp_id','name','dept_id','salary']].reset_index(drop=True)
```
**Edge cases:** A one-person department never beats its own average. NULL dept_id: `x.dept_id = e.dept_id` is never true, the subquery returns NULL and the employee is dropped. Ties at the average are excluded.
**Likely follow-ups:**
- Is there a faster way? Join to a pre-grouped table or use AVG() OVER (PARTITION BY dept_id) (Q36).
- Why alias the same table twice? So the inner and outer copies can be told apart.
**Common mistakes:** Forgetting the aliases so both sides refer to the inner table (comparison always false for the whole department). Using the company average instead.

### Q6 ⭐⭐⭐ 🟡 What is the difference between a correlated and a non-correlated subquery?
**Asked at:** candidate-reported in a Deloitte data-analyst interview list (AmbitionBox, consulting) and in Indeed's SQL guide; commonly asked.
**What the interviewer is checking:** Can you say clearly which one runs once and which one runs per row?
**Say this in the interview:** A non-correlated subquery stands on its own: it runs once and passes its result to the outer query. A correlated one refers to the outer query's current row, so it is logically re-evaluated for each outer row.
**Explain simply:**
- Non-correlated: you can copy the inner query, run it alone and it works. Example: company average.
- Correlated: the inner query uses an outer column such as `e.dept_id`; running it alone fails.
- Correlated queries are more flexible (row-by-row comparisons) but can be slower; modern optimisers often turn them into joins.
- EXISTS and NOT EXISTS are almost always correlated.
**Example:** Company average (75,000) is one fixed number. A department average changes with each employee's department (55k, 75k, 100k, 40k).
**Sample data:**

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 80000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farhan | 3 | 120000 |
| 7 | Gita | 3 | 90000 |
| 8 | Hari | 4 | 40000 |

**SQL:**
```sql
-- Non-correlated: inner query is independent
SELECT name FROM employees WHERE salary > (SELECT AVG(salary) FROM employees) ORDER BY emp_id;

-- Correlated: inner query uses e.dept_id from the outer row
SELECT name FROM employees e WHERE salary > (SELECT AVG(salary) FROM employees WHERE dept_id = e.dept_id) ORDER BY emp_id;
```
**Output:**

Non-correlated (above company average):

| name |
|---|
| Chitra |
| Esha |
| Farhan |
| Gita |

Correlated (above own-department average):

| name |
|---|
| Bala |
| Chitra |
| Farhan |

**Edge cases:** NULL join column in a correlated subquery makes the comparison unknown, so those rows drop out.
**Likely follow-ups:**
- Which is faster? Non-correlated usually, since it runs once.
- Can a non-correlated one become correlated? Yes, as soon as it mentions an outer column.
**Common mistakes:** Thinking correlated means joined. Forgetting that a correlated subquery cannot be run on its own to test it.

### Q7 ⭐⭐⭐ 🟡 Rewrite a long nested query using a CTE to make it easier to read.
**Asked at:** commonly asked as a readability task; one Hyderabad analytics-firm panel reportedly preferred traditional nested SQL, so explain the trade-off (candidate report in research notes).
**What the interviewer is checking:** Can you untangle nesting into named steps without changing the answer?
**Say this in the interview:** I read the nested query from the inside out, give each inner layer a meaningful name in a CTE, then write the final SELECT on top. Same result, but each step can be read and tested on its own.
**Explain simply:**
- Find the innermost query, turn it into the first CTE (`dept_totals`).
- Each next layer becomes the next CTE, using the previous one by name.
- The inner total-per-department query appeared twice in the nested version; the CTE writes it once.
- Finish with a short final SELECT. Check both versions give identical rows.
**Example:** Task: staff in departments whose total salary is above the average department total. Department totals are HR 110k, Finance 150k, IT 300k, Sales 40k; average 150k, so only IT qualifies.
**Sample data:**

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 80000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farhan | 3 | 120000 |
| 7 | Gita | 3 | 90000 |
| 8 | Hari | 4 | 40000 |

**SQL:**
```sql
-- Before: nested
SELECT name, salary
FROM employees
WHERE dept_id IN (
    SELECT dept_id FROM (
        SELECT dept_id, SUM(salary) AS total FROM employees GROUP BY dept_id) t
    WHERE total > (SELECT AVG(total) FROM (
        SELECT dept_id, SUM(salary) AS total FROM employees GROUP BY dept_id) t2))
ORDER BY emp_id;

-- After: CTEs
WITH dept_totals AS (                         -- step 1: total salary per department
    SELECT dept_id, SUM(salary) AS total
    FROM employees
    GROUP BY dept_id
),
rich_depts AS (                               -- step 2: keep departments above the average total
    SELECT dept_id
    FROM dept_totals
    WHERE total > (SELECT AVG(total) FROM dept_totals)
)
SELECT name, salary
FROM employees
WHERE dept_id IN (SELECT dept_id FROM rich_depts)
ORDER BY emp_id;
```
**Output:**

| name | salary |
|---|---|
| Esha | 90000 |
| Farhan | 120000 |
| Gita | 90000 |

(The nested version returned exactly the same rows.)

**pandas equivalent:**
```python
tot = employees.groupby('dept_id', as_index=False).salary.sum().rename(columns={'salary':'total'})
rich = tot[tot.total > tot.total.mean()].dept_id
result = employees[employees.dept_id.isin(rich)][['name','salary']].reset_index(drop=True)
```
**Edge cases:** Finance total equals the average exactly (150k), so `>` excludes it. Departments with no staff are not in either version.
**Likely follow-ups:**
- Does the CTE change the result? No, same rows.
- How would you check? Run both and compare with EXCEPT, or compare row counts.
**Common mistakes:** Renaming columns inconsistently between steps. Giving CTEs vague names like `a`, `b`. Changing logic during the rewrite.

### Q8 ⭐⭐⭐ 🟡 Use a CTE to calculate each department's total salary, then list only departments above the average of those totals.
**Asked at:** commonly asked (no company-specific report found) (nested-aggregation pattern; standard curriculum).
**What the interviewer is checking:** Can you aggregate, then aggregate the aggregates?
**Say this in the interview:** First I build a CTE with total salary per department. Then I take the average of those totals and keep only departments above it. The CTE lets me use the same totals both in the average and in the final filter.
**Explain simply:**
- Step 1 (CTE): total per department: HR 110k, Finance 150k, IT 300k, Sales 40k.
- Step 2: average of those four totals = 150,000.
- Step 3: keep totals strictly above 150k, so only IT.
- Plain SQL does not let you write `AVG(SUM(salary))` in a normal query, which is why the extra layer (the CTE) is needed.
**Example:** Payroll cost per department: IT costs 300k, double the typical department.
**Sample data:**

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 80000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farhan | 3 | 120000 |
| 7 | Gita | 3 | 90000 |
| 8 | Hari | 4 | 40000 |

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Finance |
| 3 | IT |
| 4 | Sales |
| 5 | Legal |

Department totals (what the CTE will produce):

| dept_id | total_salary |
|---|---|
| 1 | 110000 |
| 2 | 150000 |
| 3 | 300000 |
| 4 | 40000 |

**SQL:**
```sql
WITH dept_totals AS (
    SELECT dept_id, SUM(salary) AS total_salary
    FROM employees
    GROUP BY dept_id
)
SELECT d.dept_name, t.total_salary
FROM dept_totals t
JOIN departments d ON d.dept_id = t.dept_id
WHERE t.total_salary > (SELECT AVG(total_salary) FROM dept_totals)
ORDER BY t.total_salary DESC;
```
**Output:**

| dept_name | total_salary |
|---|---|
| IT | 300000 |

**pandas equivalent:**
```python
tot = employees.groupby('dept_id', as_index=False).agg(total_salary=('salary','sum'))
tot = tot[tot.total_salary > tot.total_salary.mean()]
result = tot.merge(departments, on='dept_id')[['dept_name','total_salary']].sort_values('total_salary', ascending=False).reset_index(drop=True)
```
**Edge cases:** Finance equals the average and is excluded by `>`. Departments with no employees (Legal) are not in the CTE, so they are not counted in the average; with a LEFT JOIN they would count as 0 and pull the average down (see Q55).
**Likely follow-ups:**
- Include equal-to-average? Change `>` to `>=`, which adds Finance.
- Without a CTE? Repeat the grouped subquery inside the WHERE.
**Common mistakes:** Averaging salaries instead of totals. Using AVG over employees rather than over department totals. Forgetting ORDER BY for a stable result.

### Q9 ⭐⭐ 🟢 Where can a subquery be used? (WHERE, FROM, SELECT, HAVING clauses)
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know subqueries can sit in several clauses, not just WHERE?
**Say this in the interview:** A subquery can go in WHERE to filter, in FROM as a derived table, in SELECT as a one-value column, and in HAVING to filter groups. Also inside UPDATE, DELETE and INSERT.
**Explain simply:**
- WHERE / HAVING: usually a single value (with =, >) or a list (with IN, ANY, EXISTS).
- FROM: a full table in brackets; it needs an alias in most databases (Q12).
- SELECT: must return exactly one value per row (scalar, Q10).
- Also allowed in JOIN ... ON conditions and in INSERT/UPDATE/DELETE (Q29).
**Example:** HR examples: staff in HR or IT (WHERE); departments with average pay above 70k (FROM); show each person next to the company maximum (SELECT); departments bigger than average (IT has 3 people; the average is 8 people / 4 departments = 2, so HR and Finance with 2 do not qualify).
**Sample data:**

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 80000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farhan | 3 | 120000 |
| 7 | Gita | 3 | 90000 |
| 8 | Hari | 4 | 40000 |

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Finance |
| 3 | IT |
| 4 | Sales |
| 5 | Legal |

**SQL:**
```sql
-- WHERE: filter using another query's result
SELECT name FROM employees
WHERE dept_id IN (SELECT dept_id FROM departments WHERE dept_name IN ('HR','IT'))
ORDER BY emp_id;

-- FROM: derived table
SELECT dept_id, avg_sal
FROM (SELECT dept_id, AVG(salary) AS avg_sal FROM employees GROUP BY dept_id) t
WHERE avg_sal > 70000
ORDER BY dept_id;

-- SELECT: scalar subquery as a column
SELECT name, salary, (SELECT MAX(salary) FROM employees) AS company_max
FROM employees ORDER BY emp_id LIMIT 3;   -- LIMIT: PostgreSQL/MySQL/SQLite; SQL Server uses TOP 3

-- HAVING: filter groups using another query's result
SELECT dept_id, COUNT(*) AS headcount
FROM employees
GROUP BY dept_id
HAVING COUNT(*) > (SELECT COUNT(*) * 1.0 / COUNT(DISTINCT dept_id) FROM employees)
ORDER BY dept_id;
```
**Output:**

WHERE:

| name |
|---|
| Asha |
| Bala |
| Esha |
| Farhan |
| Gita |

FROM:

| dept_id | avg_sal |
|---|---|
| 2 | 75000 |
| 3 | 100000 |

SELECT:

| name | salary | company_max |
|---|---|---|
| Asha | 50000 | 120000 |
| Bala | 60000 | 120000 |
| Chitra | 80000 | 120000 |

HAVING:

| dept_id | headcount |
|---|---|
| 3 | 3 |

**Edge cases:** Subquery in SELECT returning more than one row errors in most databases. In HAVING the subquery sees the whole table, not the group (see Q54). NULLs inside IN lists cause surprises (Q18).
**Likely follow-ups:**
- Which clause is most common? WHERE, then FROM.
- Can a subquery be in ORDER BY? Yes, but rare.
**Common mistakes:** Putting a multi-row subquery where only one value is allowed. Forgetting the alias on a derived table in FROM.

### Q10 ⭐⭐ 🟢 What is a scalar subquery? What happens if it returns more than one row?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know a scalar subquery must give exactly one value, and that databases differ on what happens otherwise?
**Say this in the interview:** A scalar subquery returns one row and one column, so it can be used like a single value. If it returns more than one row, PostgreSQL, MySQL and SQL Server throw an error; SQLite quietly takes the first row, which is dangerous.
**Explain simply:**
- Scalar = one value, e.g. `(SELECT MAX(salary) FROM employees)`.
- Zero rows is allowed: the scalar subquery then gives NULL.
- More than one row: error in PostgreSQL ('more than one row returned by a subquery used as an expression'), MySQL (error 1242), SQL Server (error 512) and Oracle (ORA-01427). SQLite does not complain and uses the first row. Only the SQLite behaviour was run here; the error messages are from memory / not run here.
- Fix: guarantee one row with an aggregate (MAX/MIN/AVG), a primary-key filter, or use IN / ANY for lists.
**Example:** IT has three people (90k, 120k, 90k). `salary = (SELECT salary ... WHERE dept_id = 3)` asks to compare with three values at once, which is ambiguous.
**Sample data:**

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 80000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farhan | 3 | 120000 |
| 7 | Gita | 3 | 90000 |
| 8 | Hari | 4 | 40000 |

**SQL:**
```sql
-- Problem query (error in most databases)
SELECT name FROM employees WHERE salary = (SELECT salary FROM employees WHERE dept_id = 3);

-- Fix: one value guaranteed
SELECT name FROM employees WHERE salary = (SELECT MAX(salary) FROM employees WHERE dept_id = 3) ORDER BY emp_id;
```
**Output:**

Problem query run in SQLite (silently uses only the first IT salary found, so it returns the people earning 90k):

| name |
|---|
| Esha |
| Gita |

Same query in PostgreSQL (from memory, not run here): `ERROR: more than one row returned by a subquery used as an expression`.

Fixed query:

| name |
|---|
| Farhan |

**Edge cases:** Zero rows gives NULL, so `salary = NULL` matches nothing. Ties for MAX still return all tied employees.
**Likely follow-ups:**
- How do you handle several values? Use IN, ANY or an aggregate.
- What about no rows? The scalar subquery evaluates to NULL; wrap with COALESCE if needed.
**Common mistakes:** Assuming SQLite's silent behaviour is correct, then moving to PostgreSQL where the query crashes. Using = with a list.

### Q11 ⭐⭐ 🟢 What is the difference between IN and EXISTS? When is each better?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know both do a membership check but EXISTS stops at the first match and handles NULLs safely?
**Say this in the interview:** IN compares a value against a list the subquery builds. EXISTS just asks whether the subquery finds at least one row and stops at the first. For positive checks they give the same answer; for NOT IN versus NOT EXISTS, NULLs make NOT IN risky, so I use NOT EXISTS.
**Explain simply:**
- IN: 'is this dept_id in this list?'. The list is built first (conceptually).
- EXISTS: 'is there at least one matching row?' returns true/false and ignores the selected columns.
- Modern optimisers (PostgreSQL, SQL Server, MySQL 8) often plan them identically; EXISTS can be better for large correlated checks, IN is shorter for small lists.
- Big difference with negation: `NOT IN` returns nothing if the list contains a NULL; `NOT EXISTS` does not (Q18).
**Example:** Which departments have at least one employee? HR, Finance, IT, Sales; Legal has none.
**Sample data:**

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Finance |
| 3 | IT |
| 4 | Sales |
| 5 | Legal |

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 80000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farhan | 3 | 120000 |
| 7 | Gita | 3 | 90000 |
| 8 | Hari | 4 | 40000 |

**SQL:**
```sql
-- IN
SELECT dept_name FROM departments
WHERE dept_id IN (SELECT dept_id FROM employees)
ORDER BY dept_id;

-- EXISTS
SELECT dept_name FROM departments d
WHERE EXISTS (SELECT 1 FROM employees e WHERE e.dept_id = d.dept_id)
ORDER BY dept_id;
```
**Output:**

| dept_name |
|---|
| HR |
| Finance |
| IT |
| Sales |

(The IN version returned exactly the same rows.)

**pandas equivalent:**
```python
result = departments[departments.dept_id.isin(employees.dept_id)][['dept_name']]
```
**Edge cases:** NULLs: a NULL dept_id in the employee list is harmless for IN and EXISTS but breaks NOT IN. Duplicates in the subquery do not duplicate output rows (unlike a plain JOIN).
**Likely follow-ups:**
- Which is faster? Often same; test with EXPLAIN.
- Why SELECT 1? EXISTS ignores columns (Q43).
**Common mistakes:** Using NOT IN on a nullable column. Writing EXISTS without a correlation, which returns all or no rows.

### Q12 ⭐⭐ 🟢 What is a derived table (subquery in the FROM clause)? Why must it have an alias?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know a derived table is a subquery used as a temporary table, and why it needs a name?
**Say this in the interview:** A derived table is a subquery in the FROM clause that the outer query treats like a table. It needs an alias because the outer query has to refer to its columns by a name, like `s.avg_sal`; MySQL, SQL Server and older PostgreSQL refuse it without one.
**Explain simply:**
- The inner query builds a temporary table (headcount and average per department).
- The alias is the table's name for the rest of the query. Without it, there is nothing to write before the column names.
- Rules: PostgreSQL (before v16), MySQL, SQL Server: alias required. SQLite, Oracle: alias optional. Always add it.
- Columns computed inside (like AVG) must have names, so give them aliases too.
**Example:** Average pay per department first, then join to the department names and keep only departments averaging above 70,000: Finance (75k) and IT (100k).
**Sample data:**

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 80000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farhan | 3 | 120000 |
| 7 | Gita | 3 | 90000 |
| 8 | Hari | 4 | 40000 |

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Finance |
| 3 | IT |
| 4 | Sales |
| 5 | Legal |

**SQL:**
```sql
SELECT dp.dept_name, s.headcount, s.avg_sal
FROM departments dp
JOIN (SELECT dept_id, COUNT(*) AS headcount, AVG(salary) AS avg_sal
      FROM employees
      GROUP BY dept_id) s            -- derived table: the alias 's' is mandatory in most databases
  ON s.dept_id = dp.dept_id
WHERE s.avg_sal > 70000
ORDER BY dp.dept_id;
```
**Output:**

| dept_name | headcount | avg_sal |
|---|---|---|
| Finance | 2 | 75000 |
| IT | 3 | 100000 |

**pandas equivalent:**
```python
s = employees.groupby('dept_id', as_index=False).agg(headcount=('emp_id','count'), avg_sal=('salary','mean'))
s = s[s.avg_sal > 70000]
result = departments.merge(s, on='dept_id')[['dept_name','headcount','avg_sal']].sort_values('dept_name').reset_index(drop=True)
```
**Edge cases:** Departments with no employees are missing from the derived table, so the inner join drops Legal. Use LEFT JOIN to keep it (with NULL stats).
**Likely follow-ups:**
- Derived table vs CTE? Same idea, the CTE has a name up front and is reusable (Q3).
- Can I reference another FROM table inside it? Not without LATERAL (Q46).
**Common mistakes:** Leaving off the alias (error: 'Every derived table must have its own alias' in MySQL). Not aliasing computed columns.

### Q13 ⭐⭐ 🟢 What is the scope of a CTE? Can you use it in a second, separate query?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know a CTE lives for one statement only?
**Say this in the interview:** A CTE exists only for the single statement that immediately follows it. I cannot use it in a second query; I would need to repeat it, or use a view or temp table.
**Explain simply:**
- Scope = the one SELECT/INSERT/UPDATE/DELETE right after the WITH block.
- Inside that statement, later CTEs can use earlier ones, and the main query can use any of them.
- A CTE cannot see a CTE defined after it (except in recursive CTEs, where it can see itself).
- If you need reuse across several statements, use a temp table or a view (Q15, Q45).
**Example:** Counting headcount per department in a CTE works for one query. A separate query on the next line cannot see the name `dept_hc`.
**Sample data:**

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 80000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farhan | 3 | 120000 |
| 7 | Gita | 3 | 90000 |
| 8 | Hari | 4 | 40000 |

**SQL:**
```sql
-- Query 1: works
WITH dept_hc AS (SELECT dept_id, COUNT(*) AS hc FROM employees GROUP BY dept_id)
SELECT * FROM dept_hc ORDER BY dept_id;

-- Query 2: separate statement, CTE is gone
SELECT * FROM dept_hc;
```
**Output:**

| dept_id | hc |
|---|---|
| 1 | 2 |
| 2 | 2 |
| 3 | 3 |
| 4 | 1 |

Running Query 2 gives an error (SQLite wording): `no such table: dept_hc`

**Edge cases:** In SQL Server, a statement before WITH needs a semicolon. In some tools, running two statements in one batch still counts as two separate scopes.
**Likely follow-ups:**
- How do I reuse it? Create a view or a temp table.
- Can one CTE use another? Yes, if defined earlier in the same WITH (Q16).
**Common mistakes:** Defining a CTE, running a second query and expecting the name to still exist. Referencing a later CTE from an earlier one.

### Q14 ⭐⭐ 🟢 Can a subquery return multiple columns? Where is that allowed?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know where multi-column subqueries are allowed?
**Say this in the interview:** Yes. A subquery can return several columns when it is used as a derived table in FROM, as a CTE, or in a row-value comparison like `(a, b) IN (SELECT a, b ...)`. It cannot be used as a single-value scalar in SELECT or with a plain `=`.
**Explain simply:**
- Allowed: FROM (derived table), WITH (CTE), `(col1, col2) IN (...)` and EXISTS (columns ignored).
- Not allowed: scalar position such as `SELECT (SELECT a, b ...)` or `salary > (SELECT a, b ...)`.
- Row-value IN works in PostgreSQL, MySQL, SQLite, Oracle and DuckDB. SQL Server does not support it: use the join form or EXISTS.
- Here it finds the top earner of each department.
**Example:** Pair (dept, max salary) then find who matches the pair: Bala in HR (60k), Chitra in Finance (80k), Farhan in IT (120k), Hari in Sales (40k).
**Sample data:**

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 80000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farhan | 3 | 120000 |
| 7 | Gita | 3 | 90000 |
| 8 | Hari | 4 | 40000 |

**SQL:**
```sql
SELECT name, dept_id, salary
FROM employees
WHERE (dept_id, salary) IN (SELECT dept_id, MAX(salary) FROM employees GROUP BY dept_id)
ORDER BY dept_id;

-- SQL Server friendly alternative (join to derived table); also run here with the same result:
SELECT e.name, e.dept_id, e.salary
FROM employees e
JOIN (SELECT dept_id, MAX(salary) AS max_sal FROM employees GROUP BY dept_id) m
  ON m.dept_id = e.dept_id AND m.max_sal = e.salary
ORDER BY e.dept_id;
```
**Output:**

| name | dept_id | salary |
|---|---|---|
| Bala | 1 | 60000 |
| Chitra | 2 | 80000 |
| Farhan | 3 | 120000 |
| Hari | 4 | 40000 |

**pandas equivalent:**
```python
top = employees.groupby('dept_id', as_index=False).salary.max()
result = employees.merge(top, on=['dept_id','salary'])[['name','dept_id','salary']].sort_values('dept_id').reset_index(drop=True)
```
**Edge cases:** A NULL in either column makes the pair comparison unknown, so those rows never match. Ties for the maximum return all tied people.
**Likely follow-ups:**
- What if the subquery returns two columns but I compare one? Error: operand should contain 1 column.
- Is the row-value form faster? No, it is mostly convenience.
**Common mistakes:** Mixing up column order between the outer tuple and the subquery. Using it in SQL Server where it is unsupported.

### Q15 ⭐⭐ 🟡 What is the difference between a CTE, a temporary table and a view?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you pick the right tool for a use case?
**Say this in the interview:** A CTE is a named step inside one query; a temp table actually stores rows for my session so I can reuse and index them; a view is a saved query anyone can call by name, but it stores no data of its own.
**Explain simply:**
- CTE: readability inside one query, nothing is saved.
- Temp table: use when the same intermediate result is needed in several statements or is big and benefits from an index.
- View: use when a team needs one agreed definition, for example 'active employees', and you want to hide complexity or restrict columns.
- All three below return the same headcount table.
**Example:** HR analytics team keeps a view `v_active_employees` for everyone, uses a temp table while building a heavy monthly attrition run, and a CTE for a quick one-off query.
**Sample data:**

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 80000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farhan | 3 | 120000 |
| 7 | Gita | 3 | 90000 |
| 8 | Hari | 4 | 40000 |

| | CTE | Temp table | View |
|---|---|---|---|
| Stores data? | No | Yes (rows copied) | No (stores the query) |
| Lives for | One statement | Your session | Until dropped |
| Index possible? | No | Yes | Only on materialized views (PostgreSQL/Oracle) or indexed views (SQL Server); from memory, not run here |
| Reusable across queries? | No | Yes (same session) | Yes, by everyone with access |
| Typical use | Break a query into steps | Heavy intermediate result used many times | Shared, standard definition (e.g., 'active employees') |

**SQL:**
```sql
-- CTE: exists for one statement
WITH hc AS (SELECT dept_id, COUNT(*) AS n FROM employees GROUP BY dept_id)
SELECT * FROM hc ORDER BY dept_id;

-- Temp table: a real (but temporary) table with stored rows, lives for the session
CREATE TEMP TABLE hc_temp AS SELECT dept_id, COUNT(*) AS n FROM employees GROUP BY dept_id;
SELECT * FROM hc_temp ORDER BY dept_id;

-- View: a saved query (stores no data, re-runs each time)
CREATE VIEW v_hc AS SELECT dept_id, COUNT(*) AS n FROM employees GROUP BY dept_id;
SELECT * FROM v_hc ORDER BY dept_id;
-- PostgreSQL/MySQL: CREATE TEMPORARY TABLE ... ; SQL Server: SELECT ... INTO #hc_temp FROM ... (not run here)
```
**Output:**

| dept_id | n |
|---|---|
| 1 | 2 |
| 2 | 2 |
| 3 | 3 |
| 4 | 1 |

(All three SELECTs returned this same table.)

**Edge cases:** A view on a view on a view can become slow and hard to debug. Temp tables disappear when the session ends; SQL Server prefixes them with #.
**Likely follow-ups:**
- Which is fastest? Depends; temp tables win when the result is reused many times.
- Does a view store data? No, except a materialized view (PostgreSQL, Oracle).
**Common mistakes:** Thinking a CTE or view stores data. Forgetting to drop temp tables in long sessions.

### Q16 ⭐⭐ 🟡 Can you define multiple CTEs in one query? Show how one CTE can use another.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Do you know the comma-separated chain with one WITH?
**Say this in the interview:** Yes. I write WITH once, then list CTEs separated by commas. A later CTE can read from any earlier one, and the final SELECT can use all of them.
**Explain simply:**
- Only one WITH keyword; commas between CTEs; no comma before the final SELECT.
- Order matters: CTE 2 can use CTE 1, but CTE 1 cannot use CTE 2 (apart from recursive CTEs).
- Here CTE 1 computes department averages, CTE 2 picks people above their department average, the final SELECT adds names and the gap.
- Standard in PostgreSQL, SQL Server, MySQL 8+, SQLite and Oracle.
**Example:** Bala is 5,000 above HR's average, Chitra 5,000 above Finance's, Farhan 20,000 above IT's.
**Sample data:**

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 80000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farhan | 3 | 120000 |
| 7 | Gita | 3 | 90000 |
| 8 | Hari | 4 | 40000 |

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Finance |
| 3 | IT |
| 4 | Sales |
| 5 | Legal |

**SQL:**
```sql
WITH dept_avg AS (                       -- CTE 1
    SELECT dept_id, AVG(salary) AS avg_sal
    FROM employees
    GROUP BY dept_id
),
above_avg AS (                            -- CTE 2 uses CTE 1
    SELECT e.emp_id, e.name, e.dept_id, e.salary, d.avg_sal
    FROM employees e
    JOIN dept_avg d ON d.dept_id = e.dept_id
    WHERE e.salary > d.avg_sal
)
SELECT a.name, dp.dept_name, a.salary, a.avg_sal, a.salary - a.avg_sal AS gap
FROM above_avg a
JOIN departments dp ON dp.dept_id = a.dept_id
ORDER BY a.emp_id;
```
**Output:**

| name | dept_name | salary | avg_sal | gap |
|---|---|---|---|---|
| Bala | HR | 60000 | 55000 | 5000 |
| Chitra | Finance | 80000 | 75000 | 5000 |
| Farhan | IT | 120000 | 100000 | 20000 |

**pandas equivalent:**
```python
avg = employees.groupby('dept_id', as_index=False).agg(avg_sal=('salary','mean'))
a = employees.merge(avg, on='dept_id')
a = a[a.salary > a.avg_sal]
result = a.merge(departments, on='dept_id').assign(gap=lambda d: d.salary - d.avg_sal)[['name','dept_name','salary','avg_sal','gap']].sort_values('name').reset_index(drop=True)
```
**Edge cases:** A single-person department never has anyone above average. A department with NULL salaries still gets an average from the non-NULL rows.
**Likely follow-ups:**
- Can I use the same CTE twice? Yes, within the same statement.
- What if CTE 1 uses CTE 2? Error: relation does not exist, unless recursive.
**Common mistakes:** Writing WITH again before the second CTE. Adding a trailing comma before the final SELECT.

### Q17 ⭐⭐ 🟡 Find products that have never been sold (subquery vs join approach).
**Asked at:** commonly asked (no company-specific report found) (the classic 'never ordered' anti-join).
**What the interviewer is checking:** Can you find 'rows with no match' and know NOT EXISTS, LEFT JOIN ... IS NULL and NOT IN?
**Say this in the interview:** I look for products with no row in the order items table. My default is NOT EXISTS because it is safe with NULLs; LEFT JOIN with IS NULL gives the same result; NOT IN works if the column cannot be NULL.
**Explain simply:**
- This pattern is called an anti-join: keep rows from table A with no match in table B.
- NOT EXISTS: 'there is no order line for this product'.
- LEFT JOIN + IS NULL: join everything, then keep the rows where the right side is empty.
- Sold products: 1 Laptop, 2 Mouse, 4 Monitor. Never sold: Keyboard and Webcam.
**Example:** Think of it as employees who never took leave, or candidates who never got an interview call.
**Sample data:**

| product_id | product_name |
|---|---|
| 1 | Laptop |
| 2 | Mouse |
| 3 | Keyboard |
| 4 | Monitor |
| 5 | Webcam |

| order_id | product_id | qty |
|---|---|---|
| 101 | 1 | 1 |
| 101 | 2 | 2 |
| 102 | 2 | 1 |
| 103 | 4 | 1 |
| 104 | 1 | 1 |

**SQL:**
```sql
-- 1) NOT EXISTS (preferred)
SELECT p.product_id, p.product_name
FROM products p
WHERE NOT EXISTS (SELECT 1 FROM order_items oi WHERE oi.product_id = p.product_id)
ORDER BY p.product_id;

-- 2) LEFT JOIN
SELECT p.product_id, p.product_name
FROM products p
LEFT JOIN order_items oi ON oi.product_id = p.product_id
WHERE oi.product_id IS NULL
ORDER BY p.product_id;

-- 3) NOT IN (only if product_id is never NULL)
SELECT product_id, product_name FROM products
WHERE product_id NOT IN (SELECT product_id FROM order_items)
ORDER BY product_id;
```
**Output:**

| product_id | product_name |
|---|---|
| 3 | Keyboard |
| 5 | Webcam |

(All three versions returned the same rows.)

**pandas equivalent:**
```python
result = products[~products.product_id.isin(order_items.product_id)][['product_id','product_name']].reset_index(drop=True)
```
**Edge cases:** NULL in order_items.product_id makes NOT IN return no rows at all (Q18). Duplicate sales rows do not matter for the anti-join. If every product sold, the result is empty.
**Likely follow-ups:**
- Which is fastest? Often similar; NOT EXISTS and LEFT JOIN are usually safe choices.
- How to count them? Wrap in COUNT(*).
**Common mistakes:** Using an INNER JOIN, which can only return sold products. Using NOT IN with a NULL-containing column. Putting the filter on the right table in WHERE instead of IS NULL.

### Q18 ⭐⭐ 🟡 Find departments that have no employees (NOT EXISTS / NOT IN).
**Asked at:** commonly asked (no company-specific report found) (NOT IN versus NOT EXISTS trap is a favourite interview follow-up).
**What the interviewer is checking:** Do you know the NULL trap in NOT IN?
**Say this in the interview:** I find departments with no employees using NOT EXISTS. NOT IN gives the same answer only if the employee department column has no NULLs; one NULL makes NOT IN return nothing.
**Explain simply:**
- Normal data: both return Legal, the only department with no staff.
- Why NOT IN breaks: `x NOT IN (1,2,NULL)` is unknown for every x, never true, so zero rows.
- NOT EXISTS checks for matching rows and is not affected by NULL in the other table.
- Real HR case: a new joiner is saved with no department yet (NULL). That single row silently breaks a NOT IN report.
**Example:** Departments: HR, Finance, IT, Sales all have staff. Legal has none. If we add Ishaan with NULL department, NOT IN returns an empty table while NOT EXISTS still returns Legal.
**Sample data:**

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Finance |
| 3 | IT |
| 4 | Sales |
| 5 | Legal |

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 80000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farhan | 3 | 120000 |
| 7 | Gita | 3 | 90000 |
| 8 | Hari | 4 | 40000 |

**SQL:**
```sql
-- NOT EXISTS (safe)
SELECT dept_id, dept_name
FROM departments d
WHERE NOT EXISTS (SELECT 1 FROM employees e WHERE e.dept_id = d.dept_id)
ORDER BY dept_id;

-- NOT IN (risky with NULLs)
SELECT dept_id, dept_name
FROM departments
WHERE dept_id NOT IN (SELECT dept_id FROM employees)
ORDER BY dept_id;
```
**Output:**

Normal data (both queries):

| dept_id | dept_name |
|---|---|
| 5 | Legal |

After inserting an employee with NULL dept_id:

NOT IN:

| dept_id | dept_name |
|---|---|
| (no rows) | |

NOT EXISTS:

| dept_id | dept_name |
|---|---|
| 5 | Legal |

**pandas equivalent:**
```python
result = departments[~departments.dept_id.isin(employees.dept_id)][['dept_id','dept_name']].reset_index(drop=True)
# Note: pandas isin() treats NaN like a normal value, so it does not copy SQL's NOT IN trap.
```
**Edge cases:** NULLs are the main edge case, as shown. If every department has staff, the result is empty. Duplicated employee dept_ids do not matter.
**Likely follow-ups:**
- Fix for NOT IN? Add `WHERE dept_id IS NOT NULL` inside the subquery.
- LEFT JOIN alternative? Yes, `LEFT JOIN employees ... WHERE e.emp_id IS NULL`.
**Common mistakes:** Using NOT IN without checking for NULLs. Expecting NOT IN to behave like Python's `not in`.

### Q19 ⭐⭐ 🟡 Use a subquery in the SELECT clause to show each employee's salary next to the company average and the difference.
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Can you use a scalar subquery as a column?
**Say this in the interview:** I put a scalar subquery in the SELECT list. It returns the same single number, the company average, which the database attaches to every row. Then salary minus that column gives the difference.
**Explain simply:**
- The subquery must return exactly one value (Q10). It is evaluated once because it does not depend on the row.
- I repeat the subquery to compute the difference. Alternatively compute it once in a CTE or derived table and reuse it.
- Window function alternative: `AVG(salary) OVER ()`, which gives the same column (Part 5).
- Result: positive diff means above average (Farhan +45,000), negative means below (Hari -35,000).
**Example:** An HR pay-equity sheet: each person's salary beside the company average and how far above or below they are.
**Sample data:**

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 80000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farhan | 3 | 120000 |
| 7 | Gita | 3 | 90000 |
| 8 | Hari | 4 | 40000 |

**SQL:**
```sql
SELECT name, salary,
       (SELECT AVG(salary) FROM employees)            AS company_avg,
       salary - (SELECT AVG(salary) FROM employees)   AS diff
FROM employees
ORDER BY emp_id;
```
**Output:**

| name | salary | company_avg | diff |
|---|---|---|---|
| Asha | 50000 | 75000 | -25000 |
| Bala | 60000 | 75000 | -15000 |
| Chitra | 80000 | 75000 | 5000 |
| Dev | 70000 | 75000 | -5000 |
| Esha | 90000 | 75000 | 15000 |
| Farhan | 120000 | 75000 | 45000 |
| Gita | 90000 | 75000 | 15000 |
| Hari | 40000 | 75000 | -35000 |

**pandas equivalent:**
```python
avg = employees.salary.mean()
result = employees.assign(company_avg=avg, diff=employees.salary - avg)[['name','salary','company_avg','diff']]
```
**Edge cases:** NULL salary gives a NULL diff and is excluded from the average. If the table is empty, the average is NULL.
**Likely follow-ups:**
- Can I reuse the alias `company_avg` in the same SELECT? No, aliases cannot be reused in the same SELECT in most databases.
- Better way? `AVG(salary) OVER ()` or a CROSS JOIN to a one-row CTE.
**Common mistakes:** Repeating a correlated subquery for each row (slow). Trying to use the alias in the same SELECT. Returning more than one row from the subquery.

### Q20 ⭐⭐ 🟡 Show each department's highest-paid employee using a subquery (and compare with the window-function way).
**Asked at:** service MNC and GCC (candidate reports of a department-highest-salary query at Wipro, Noida 2025, and a per-department salary-rank question at Amazon, Bengaluru 2025; anonymous, not fully verified)
**What the interviewer is checking:** Can you pair a row with a group-level number (the department maximum) without losing the employee's name?
**Say this in the interview:** "A plain GROUP BY would give me the maximum but lose the name. So I use a correlated subquery: for each employee, find the highest salary in their own department and keep the rows that match. The window-function way uses RANK and keeps rank 1."
**Explain simply:**
- A **subquery** is a query inside another query. A **correlated** one refers to the outer row (`e.dept_id`), so it is re-evaluated for each outer row.
- The subquery returns one number (the department's top salary); `WHERE salary = that number` keeps only the top earners.
- Ties are kept: if two people share the top salary, both show up. `RANK() = 1` behaves the same; `ROW_NUMBER() = 1` would pick just one.
**Example:** In IT, Gita and Hari both earn 120,000. The max for IT is 120,000, so both rows are returned.
**Sample data:**

*employees*

| emp_id | name | dept_id | salary | left_date |
|---|---|---|---|---|
| 1 | Asha | 1 | 50000 | NULL |
| 2 | Bala | 1 | 60000 | 2026-03-31 |
| 3 | Chitra | 2 | 70000 | NULL |
| 4 | Dev | 2 | 90000 | 2026-06-30 |
| 5 | Esha | 2 | 90000 | NULL |
| 6 | Farid | 3 | 80000 | NULL |
| 7 | Gita | 3 | 120000 | NULL |
| 8 | Hari | 3 | 120000 | NULL |

*departments*

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Sales |
| 3 | IT |
| 4 | Finance |
**SQL:**
```sql
SELECT d.dept_name, e.name, e.salary
FROM employees e
JOIN departments d ON d.dept_id = e.dept_id
WHERE e.salary = (SELECT MAX(e2.salary)          -- correlated: re-runs per employee row
                  FROM employees e2
                  WHERE e2.dept_id = e.dept_id)
ORDER BY d.dept_name, e.name;

-- Window-function way (Part 5 covers ranking in depth) (also run here, same result)
SELECT dept_name, name, salary
FROM (SELECT d.dept_name, e.name, e.salary,
             RANK() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS rnk
      FROM employees e JOIN departments d ON d.dept_id = e.dept_id) t
WHERE rnk = 1
ORDER BY dept_name, name;
```
**Output:**

| dept_name | name | salary |
|---|---|---|
| HR | Bala | 60000 |
| IT | Gita | 120000 |
| IT | Hari | 120000 |
| Sales | Dev | 90000 |
| Sales | Esha | 90000 |
**pandas equivalent:**
```python
# each table above is a pandas DataFrame with the same name (employees, departments, orders, ...)
m = employees.merge(departments, on='dept_id')
res = (m[m.salary == m.groupby('dept_id').salary.transform('max')]
       [['dept_name','name','salary']].sort_values(['dept_name','name']).reset_index(drop=True))
# Output (matches the SQL):
# dept_name name  salary
#        HR Bala   60000
#        IT Gita  120000
#        IT Hari  120000
#     Sales  Dev   90000
#     Sales Esha   90000
```
**Edge cases:** Ties return several rows per department (shown for Sales and IT). A department with no employees (Finance) does not appear. A NULL salary is ignored by MAX and never equals anything.
**Likely follow-ups:**
- How do you return only one person per department? Use `ROW_NUMBER()` with a tie-breaker such as `emp_id`.
- Which is faster? On large tables the window version scans once; the correlated version may run the inner query many times (see Q36).
**Common mistakes:** Using `SELECT dept_id, MAX(salary), name ... GROUP BY dept_id` (name is not grouped, so the result is wrong or an error), or forgetting the `e2.dept_id = e.dept_id` link, which gives the company-wide top earner only.

### Q21 ⭐⭐ 🟡 Find customers whose total order value is above the average customer's total order value (nested aggregation).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand **nested aggregation**: an average of totals, which needs two levels of grouping?
**Say this in the interview:** "First I total orders per customer. Then I average those totals. Then I keep customers above that average. SQL cannot write AVG(SUM(...)) directly, so I use a CTE or a derived table for the first step."
**Explain simply:**
- Level 1: `SUM(amount)` per customer. Level 2: `AVG` of those totals. You cannot nest aggregates in one SELECT, so level 1 goes in a CTE (a named temporary result, written with `WITH`).
- The average is a single number, so it can sit in `WHERE total > (subquery)`.
- Do not confuse this with `AVG(amount)`, which averages single orders, not customers.
**Example:** Customer totals: Ravi 500, Sita 750, Tara 400, Uma 750, Vik 100. Average of totals = 500. Above 500: Sita and Uma.
**Sample data:**

*customers*

| customer_id | name | city |
|---|---|---|
| 1 | Ravi | Hyderabad |
| 2 | Sita | Hyderabad |
| 3 | Tara | Hyderabad |
| 4 | Uma | Bengaluru |
| 5 | Vik | Bengaluru |
| 6 | Wen | Pune |
| 7 | Xan | Chennai |

*orders*

| order_id | customer_id | product_id | order_date | amount |
|---|---|---|---|---|
| 101 | 1 | 1 | 2026-01-05 | 200 |
| 102 | 1 | 2 | 2026-01-20 | 300 |
| 103 | 2 | 1 | 2026-02-03 | 150 |
| 104 | 3 | 3 | 2026-02-14 | 400 |
| 105 | 4 | 2 | 2026-02-25 | 250 |
| 106 | 4 | 1 | 2026-03-02 | 500 |
| 107 | 5 | 3 | 2026-03-15 | 100 |
| 108 | 2 | 2 | 2026-03-28 | 600 |
**SQL:**
```sql
WITH cust_total AS (
    SELECT customer_id, SUM(amount) AS total
    FROM orders
    GROUP BY customer_id
)
SELECT c.name, t.total
FROM cust_total t
JOIN customers c ON c.customer_id = t.customer_id
WHERE t.total > (SELECT AVG(total) FROM cust_total)
ORDER BY t.total DESC, c.name;

-- Subquery-only version (derived table needs an alias) (also run here, same result)
SELECT c.name, SUM(o.amount) AS total
FROM orders o JOIN customers c ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING SUM(o.amount) > (SELECT AVG(t) FROM (SELECT SUM(amount) AS t FROM orders GROUP BY customer_id) x)
ORDER BY total DESC, c.name;
```
**Output:**

| name | total |
|---|---|
| Sita | 750 |
| Uma | 750 |
**pandas equivalent:**
```python
# each table above is a pandas DataFrame with the same name (employees, departments, orders, ...)
t = orders.groupby('customer_id', as_index=False).amount.sum().rename(columns={'amount':'total'})
res = (t[t.total > t.total.mean()].merge(customers, on='customer_id')[['name','total']]
       .sort_values(['total','name'], ascending=[False,True]).reset_index(drop=True))
# Output (matches the SQL):
# name  total
# Sita    750
#  Uma    750
```
**Edge cases:** Customers with no orders (Wen, Xan) are absent from the CTE, so they are not in the average. If you want them counted as 0, the average is 2500/7 = 357.1 and Ravi, Sita, Tara, Uma qualify; start from `customers` with a LEFT JOIN. Ties with the average are excluded by `>`.
**Likely follow-ups:**
- Why not `HAVING SUM(amount) > AVG(SUM(amount))`? Aggregates cannot be nested in standard SQL.
- How would you include zero-order customers? LEFT JOIN customers to orders and use `COALESCE(SUM(amount),0)`.
**Common mistakes:** Writing `WHERE amount > (SELECT AVG(amount) FROM orders)` (compares single orders, not customer totals), or forgetting to alias the derived table (an error in MySQL and PostgreSQL).

### Q22 ⭐⭐ 🟡 Use a CTE to find monthly sales and then the month with the highest sales.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you build an intermediate result (monthly totals) and then query it, and handle the 'highest' correctly?
**Say this in the interview:** "I put monthly totals in a CTE, then filter it where the total equals the maximum of the same CTE. That also returns ties, unlike ORDER BY with LIMIT 1."
**Explain simply:**
- Step 1 (CTE): turn each date into a 'year-month' label and sum amounts per month.
- Step 2: compare each month's total with `MAX(total)` of the same CTE; a CTE can be read twice in one query.
- The month-extraction function differs by database (see comments in the SQL).
**Example:** Monthly sales: Jan 500, Feb 800, Mar 1,200. March is the best month.
**Sample data:**

*orders*

| order_id | customer_id | product_id | order_date | amount |
|---|---|---|---|---|
| 101 | 1 | 1 | 2026-01-05 | 200 |
| 102 | 1 | 2 | 2026-01-20 | 300 |
| 103 | 2 | 1 | 2026-02-03 | 150 |
| 104 | 3 | 3 | 2026-02-14 | 400 |
| 105 | 4 | 2 | 2026-02-25 | 250 |
| 106 | 4 | 1 | 2026-03-02 | 500 |
| 107 | 5 | 3 | 2026-03-15 | 100 |
| 108 | 2 | 2 | 2026-03-28 | 600 |
**SQL:**
```sql
-- SQLite month = strftime('%Y-%m', date). PostgreSQL: TO_CHAR(order_date,'YYYY-MM') or DATE_TRUNC('month', order_date).
-- MySQL: DATE_FORMAT(order_date,'%Y-%m'). SQL Server: FORMAT(order_date,'yyyy-MM') or EOMONTH (not run here).
WITH monthly AS (
    SELECT strftime('%Y-%m', order_date) AS month, SUM(amount) AS total
    FROM orders
    GROUP BY strftime('%Y-%m', order_date)
)
SELECT month, total
FROM monthly
WHERE total = (SELECT MAX(total) FROM monthly);
```
**Output:**

| month | total |
|---|---|
| 2026-03 | 1200 |
**pandas equivalent:**
```python
# each table above is a pandas DataFrame with the same name (employees, departments, orders, ...)
monthly = (orders.assign(month=orders.order_date.str[:7]).groupby('month', as_index=False).amount.sum()
           .rename(columns={'amount':'total'}))
res = monthly[monthly.total == monthly.total.max()].reset_index(drop=True)
# Output (matches the SQL):
#   month  total
# 2026-03   1200
```
**Edge cases:** Two months with the same top total are both returned (that is the advantage over LIMIT 1). Months with no orders do not exist in the data, so they cannot win. NULL amounts are skipped by SUM. Group by year too, or the same month in two years gets merged (the `%Y-%m` label already includes the year).
**Likely follow-ups:**
- How to get only one month? Add `ORDER BY total DESC LIMIT 1` (TOP 1 in SQL Server).
- How to see growth between months? That is Q34 (LAG).
**Common mistakes:** Grouping by month name or month number only, which merges January 2025 and January 2026.

### Q23 ⭐⭐ 🟡 Use a subquery with HAVING: find departments whose headcount is above the average headcount per department.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know **HAVING** filters groups, and can it be compared with a subquery result?
**Say this in the interview:** "WHERE filters rows before grouping; HAVING filters groups after. Here the group is a department with its headcount, and I compare it with the average headcount, which comes from a subquery that counts per department first."
**Explain simply:**
- `HAVING` is the filter for aggregated numbers like `COUNT(*)`. `WHERE` cannot use them.
- The inner query counts people per department; the middle query averages those counts (2.67 here); HAVING keeps departments above it.
- In a derived table (subquery in FROM) you must give an alias (`x`) in MySQL and PostgreSQL.
**Example:** HR has 2 people, Sales 3, IT 3. Average = 8/3 = 2.67, so Sales and IT qualify.
**Sample data:**

*employees*

| emp_id | name | dept_id | salary | left_date |
|---|---|---|---|---|
| 1 | Asha | 1 | 50000 | NULL |
| 2 | Bala | 1 | 60000 | 2026-03-31 |
| 3 | Chitra | 2 | 70000 | NULL |
| 4 | Dev | 2 | 90000 | 2026-06-30 |
| 5 | Esha | 2 | 90000 | NULL |
| 6 | Farid | 3 | 80000 | NULL |
| 7 | Gita | 3 | 120000 | NULL |
| 8 | Hari | 3 | 120000 | NULL |

*departments*

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Sales |
| 3 | IT |
| 4 | Finance |
**SQL:**
```sql
SELECT d.dept_name, COUNT(*) AS headcount
FROM employees e
JOIN departments d ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name
HAVING COUNT(*) > (SELECT AVG(cnt)
                   FROM (SELECT COUNT(*) AS cnt FROM employees GROUP BY dept_id) x)
ORDER BY d.dept_name;
```
**Output:**

| dept_name | headcount |
|---|---|
| IT | 3 |
| Sales | 3 |
**pandas equivalent:**
```python
# each table above is a pandas DataFrame with the same name (employees, departments, orders, ...)
cnt = employees.groupby('dept_id').size().rename('headcount').reset_index()
res = (cnt[cnt.headcount > cnt.headcount.mean()].merge(departments, on='dept_id')
       [['dept_name','headcount']].sort_values('dept_name').reset_index(drop=True))
# Output (matches the SQL):
# dept_name  headcount
#        IT          3
#     Sales          3
```
**Edge cases:** Finance has zero employees and appears in no group, so it is not in the average (average would be 2.0 if Finance counted as 0: then Sales and IT still qualify but the logic changes; see Q55). NULL dept_id forms its own group.
**Likely follow-ups:**
- Why not WHERE? Because the count does not exist until after GROUP BY.
- What if zero-employee departments must count? Start from `departments` with a LEFT JOIN and `COUNT(e.emp_id)`.
**Common mistakes:** Using `AVG(COUNT(*))` directly (not allowed), or using WHERE instead of HAVING.

### Q24 ⭐⭐ 🟡 What is a nested subquery? How deep should you nest, and why avoid too many levels?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know when nesting stops being readable, and what to do instead?
**Say this in the interview:** "A nested subquery is a subquery inside another subquery. SQL allows many levels, but I stop at about two. Beyond that I move each step into a CTE with a clear name, because the next person has to read it."
**Explain simply:**
- Reading order of a nested query is inside-out, which is hard for humans; each extra level adds a bracket to match.
- Bugs hide easily: a misplaced bracket or a wrong alias changes the answer silently.
- Databases usually optimise nested and CTE versions the same way, so readability, not speed, is the reason to flatten.
- Rule of thumb: 1 level is fine, 2 is acceptable, 3+ becomes a CTE.
**Example:** Task: employees of departments whose total salary is above the average department total. Totals are HR 110k, Sales 250k, IT 320k; average 226.7k; so Sales and IT staff qualify.
**Sample data:**

*employees*

| emp_id | name | dept_id | salary | left_date |
|---|---|---|---|---|
| 1 | Asha | 1 | 50000 | NULL |
| 2 | Bala | 1 | 60000 | 2026-03-31 |
| 3 | Chitra | 2 | 70000 | NULL |
| 4 | Dev | 2 | 90000 | 2026-06-30 |
| 5 | Esha | 2 | 90000 | NULL |
| 6 | Farid | 3 | 80000 | NULL |
| 7 | Gita | 3 | 120000 | NULL |
| 8 | Hari | 3 | 120000 | NULL |
**SQL:**
```sql
SELECT name
FROM employees
WHERE dept_id IN (                                   -- level 1
        SELECT dept_id FROM employees
        GROUP BY dept_id
        HAVING SUM(salary) > (                       -- level 2
                SELECT AVG(s) FROM (                 -- level 3
                        SELECT SUM(salary) AS s FROM employees GROUP BY dept_id) t))
ORDER BY name;

-- Same logic as CTEs: each step has a name (also run here, same result)
WITH dept_cost AS (SELECT dept_id, SUM(salary) AS cost FROM employees GROUP BY dept_id),
     avg_cost  AS (SELECT AVG(cost) AS avg_cost FROM dept_cost),
     big_depts AS (SELECT dept_id FROM dept_cost, avg_cost WHERE cost > avg_cost)
SELECT name FROM employees WHERE dept_id IN (SELECT dept_id FROM big_depts) ORDER BY name;
```
**Output:**

| name |
|---|
| Chitra |
| Dev |
| Esha |
| Farid |
| Gita |
| Hari |
**Edge cases:** NOT IN at any level breaks if the inner list has a NULL (see Q18). Every derived table needs an alias in MySQL/PostgreSQL. SQL Server does not allow an ORDER BY inside a subquery without TOP.
**Likely follow-ups:**
- Do CTEs make it faster? Usually no, same plan (see Q28).
- Is there a hard limit on depth? Databases have large limits; the practical limit is human.
**Common mistakes:** Nesting because it 'works', then being unable to explain or debug it in the interview. Name CTEs after the business meaning (`dept_cost`), not `cte1`.

### Q25 ⭐⭐ 🟡 Find employees whose salary equals the maximum salary in the company (single-value subquery).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know a **scalar subquery** (one row, one column) can be used like a plain number, and how ties behave?
**Say this in the interview:** "I find the maximum salary in a subquery, which returns one number, and keep every employee whose salary equals it. This returns all tied top earners, where LIMIT 1 would drop one."
**Explain simply:**
- A single-value subquery behaves like a constant: `salary = (SELECT MAX(...))`.
- You cannot write `WHERE salary = MAX(salary)` directly, because aggregates are not allowed in WHERE.
- The subquery runs once (it is not correlated).
**Example:** Highest pay in the company is 120,000 and two people earn it (Gita and Hari), so two rows come back.
**Sample data:**

*employees*

| emp_id | name | dept_id | salary | left_date |
|---|---|---|---|---|
| 1 | Asha | 1 | 50000 | NULL |
| 2 | Bala | 1 | 60000 | 2026-03-31 |
| 3 | Chitra | 2 | 70000 | NULL |
| 4 | Dev | 2 | 90000 | 2026-06-30 |
| 5 | Esha | 2 | 90000 | NULL |
| 6 | Farid | 3 | 80000 | NULL |
| 7 | Gita | 3 | 120000 | NULL |
| 8 | Hari | 3 | 120000 | NULL |
**SQL:**
```sql
SELECT name, salary
FROM employees
WHERE salary = (SELECT MAX(salary) FROM employees)
ORDER BY name;
```
**Output:**

| name | salary |
|---|---|
| Gita | 120000 |
| Hari | 120000 |
**pandas equivalent:**
```python
# each table above is a pandas DataFrame with the same name (employees, departments, orders, ...)
res = employees[employees.salary == employees.salary.max()][['name','salary']].sort_values('name').reset_index(drop=True)
# Output (matches the SQL):
# name  salary
# Gita  120000
# Hari  120000
```
**Edge cases:** Ties give several rows. Empty table: MAX is NULL, `salary = NULL` is never true, so you get no rows. NULL salaries are ignored by MAX.
**Likely follow-ups:**
- Alternative? `ORDER BY salary DESC LIMIT 1` (TOP 1 / FETCH FIRST) gives one row only; `FETCH FIRST 1 ROWS WITH TIES` (PostgreSQL 13+, Oracle, SQL Server TOP 1 WITH TIES) keeps ties.
- Second highest? Part 10 covers nth-highest.
**Common mistakes:** Writing `WHERE salary = MAX(salary)` (error), or using `salary > ...` and getting an empty answer.

### Q26 ⭐⭐ 🟡 What do ANY, ALL and SOME do with a subquery? Give an example.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know how to compare one value against a whole list from a subquery?
**Say this in the interview:** "ANY means 'true if the comparison holds for at least one value in the list'; ALL means 'for every value'. SOME is just another name for ANY. `> ANY` is the same as `> MIN`, and `> ALL` is the same as `> MAX`."
**Explain simply:**
- `= ANY (subquery)` is the same as `IN`. `<> ALL (subquery)` is the same as `NOT IN`.
- `salary > ALL (HR salaries)` means higher than the best-paid HR person.
- `salary > ANY (Sales salaries)` means higher than the lowest-paid Sales person.
- Supported in PostgreSQL, MySQL, SQL Server, Oracle. **SQLite does not support ANY/ALL**, so the queries below with ANY/ALL were not run here; I ran the MAX/MIN equivalents.
**Example:** HR salaries are 50,000 and 60,000. Earning more than ALL of them means above 60,000.
**Sample data:**

*employees*

| emp_id | name | dept_id | salary | left_date |
|---|---|---|---|---|
| 1 | Asha | 1 | 50000 | NULL |
| 2 | Bala | 1 | 60000 | 2026-03-31 |
| 3 | Chitra | 2 | 70000 | NULL |
| 4 | Dev | 2 | 90000 | 2026-06-30 |
| 5 | Esha | 2 | 90000 | NULL |
| 6 | Farid | 3 | 80000 | NULL |
| 7 | Gita | 3 | 120000 | NULL |
| 8 | Hari | 3 | 120000 | NULL |
**SQL:**
```sql
-- PostgreSQL / MySQL / SQL Server / Oracle (not run here: SQLite lacks ANY/ALL)
SELECT name, salary FROM employees
WHERE salary > ALL (SELECT salary FROM employees WHERE dept_id = 1);   -- HR

SELECT name, salary FROM employees
WHERE salary > ANY (SELECT salary FROM employees WHERE dept_id = 2);   -- Sales

-- Equivalent forms that I ran in SQLite
SELECT name, salary FROM employees
WHERE salary > (SELECT MAX(salary) FROM employees WHERE dept_id = 1) ORDER BY salary, name;

SELECT name, salary FROM employees
WHERE salary > (SELECT MIN(salary) FROM employees WHERE dept_id = 2) ORDER BY salary, name;
```
**Output:**

ALL / MAX form (above 60,000):

| name | salary |
|---|---|
| Chitra | 70000 |
| Farid | 80000 |
| Dev | 90000 |
| Esha | 90000 |
| Gita | 120000 |
| Hari | 120000 |

ANY / MIN form (above 70,000, the lowest Sales salary):

| name | salary |
|---|---|
| Farid | 80000 |
| Dev | 90000 |
| Esha | 90000 |
| Gita | 120000 |
| Hari | 120000 |
**Edge cases:** `> ALL` over an empty subquery is true for every row; `> ANY` over an empty subquery is false. If the list contains a NULL, `> ALL` can become unknown (no rows) and `<> ALL` behaves like the NOT IN NULL trap.
**Likely follow-ups:**
- Is `= ANY` the same as IN? Yes.
- Which is more common in practice? MAX/MIN or IN/EXISTS, because they are clearer and portable.
**Common mistakes:** Thinking `> ANY` means 'greater than all' (it means greater than at least one, so greater than the minimum).

### Q27 ⭐⭐ 🟡 Find the cities that have more customers than the average city (subquery on grouped data).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you filter groups against an average of groups (same pattern as Q23)?
**Say this in the interview:** "Count customers per city, average those counts, and keep the cities above the average. The average is computed in a subquery over the grouped counts."
**Explain simply:**
- Inner query: customers per city (3, 2, 1, 1). Average = 7/4 = 1.75.
- Outer query groups again and uses HAVING to compare each city's count with 1.75.
- A subquery on grouped data is a derived table in FROM; it needs an alias.
**Example:** Hyderabad has 3 customers and Bengaluru 2; both are above 1.75. Pune and Chennai have 1 each.
**Sample data:**

*customers*

| customer_id | name | city |
|---|---|---|
| 1 | Ravi | Hyderabad |
| 2 | Sita | Hyderabad |
| 3 | Tara | Hyderabad |
| 4 | Uma | Bengaluru |
| 5 | Vik | Bengaluru |
| 6 | Wen | Pune |
| 7 | Xan | Chennai |
**SQL:**
```sql
SELECT city, COUNT(*) AS customers
FROM customers
GROUP BY city
HAVING COUNT(*) > (SELECT AVG(n) FROM (SELECT COUNT(*) AS n FROM customers GROUP BY city) t)
ORDER BY customers DESC, city;
```
**Output:**

| city | customers |
|---|---|
| Hyderabad | 3 |
| Bengaluru | 2 |
**pandas equivalent:**
```python
# each table above is a pandas DataFrame with the same name (employees, departments, orders, ...)
c = customers.groupby('city').size().rename('customers').reset_index()
res = c[c.customers > c.customers.mean()].sort_values(['customers','city'], ascending=[False,True]).reset_index(drop=True)
# Output (matches the SQL):
#      city  customers
# Hyderabad          3
# Bengaluru          2
```
**Edge cases:** Cities with NULL city form one group (shown as a city with NULL). Cities with zero customers cannot appear because they have no rows. Ties with the average are excluded.
**Likely follow-ups:**
- Why 1.75 and not 2? AVG gives a decimal; do not round it before comparing.
- Does it matter if you use a CTE? No, same result.
**Common mistakes:** Comparing `COUNT(*) > AVG(COUNT(*))` directly, or forgetting the derived-table alias.

### Q28 ⭐⭐ 🟡 Is a CTE faster than a subquery? Does a CTE store its result?
**Asked at:** analytics firm (one Hyderabad interview report: a panel preferred 'traditional' SQL over CTEs) and generic guides; otherwise commonly asked
**What the interviewer is checking:** Do you avoid the myth that CTE = faster, and know a CTE is not a stored table?
**Say this in the interview:** "Not by itself. A CTE mainly makes the query readable. It is not stored on disk. Depending on the database it is either merged into the main query or computed once for that query only. I check the execution plan before claiming any speed difference."
**Explain simply:**
- A CTE exists only for the one statement that follows it; nothing is saved afterwards.
- PostgreSQL 12+ inlines a non-recursive CTE used once (like a subquery) and computes a CTE used two or more times once and reuses it (you can force either way with MATERIALIZED / NOT MATERIALIZED); before version 12 it always computed it separately (from memory / not run here). SQL Server and MySQL 8 generally treat it like a subquery or derived table (SQL Server may re-evaluate a CTE referenced twice). Oracle may materialise it, or inline it.
- So: same result always; speed differs only by engine and version. Check with `EXPLAIN`.
- A temp table, by contrast, really stores data (Q15).
**Example:** Averaging salaries and listing people above average: both forms below give the same answer. In SQLite the plans for both are listed under Output.
**Sample data:**

*employees* (average salary = 680,000 / 8 = 85,000)

| emp_id | name | dept_id | salary | left_date |
|---|---|---|---|---|
| 1 | Asha | 1 | 50000 | NULL |
| 2 | Bala | 1 | 60000 | 2026-03-31 |
| 3 | Chitra | 2 | 70000 | NULL |
| 4 | Dev | 2 | 90000 | 2026-06-30 |
| 5 | Esha | 2 | 90000 | NULL |
| 6 | Farid | 3 | 80000 | NULL |
| 7 | Gita | 3 | 120000 | NULL |
| 8 | Hari | 3 | 120000 | NULL |

**SQL:**
```sql
SELECT name FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees) ORDER BY name;

WITH avg_sal AS (SELECT AVG(salary) AS a FROM employees)
SELECT name FROM employees, avg_sal WHERE salary > a ORDER BY name;

-- then: EXPLAIN QUERY PLAN <query>;   (PostgreSQL: EXPLAIN ANALYZE <query>)
```
**Output:**

Both queries return:

| name |
|---|
| Dev |
| Esha |
| Gita |
| Hari |

SQLite plan, subquery version: `SCAN employees | SCALAR SUBQUERY 1 | SCAN employees | USE TEMP B-TREE FOR ORDER BY`

SQLite plan, CTE version: `CO-ROUTINE avg_sal | SCAN employees | SCAN avg_sal | SCAN employees | USE TEMP B-TREE FOR ORDER BY`

**pandas equivalent:** (pandas has no CTE-vs-subquery split; both versions are the same one-liner)
```python
result = employees[employees.salary > employees.salary.mean()][['name']].sort_values('name').reset_index(drop=True)
```
**Edge cases:** A CTE referenced twice may be computed twice in some engines. A non-deterministic function inside a CTE (random, now) may give different values per reference when inlined.
**Likely follow-ups:**
- When is a CTE slower? When the engine re-runs it for each reference, or when it blocks index use by materialising (older PostgreSQL).
- Is a CTE the same as a view? No: a view is saved in the database, a CTE lives for one query.
**Common mistakes:** Saying 'CTEs are faster' or 'CTEs save the result for later'. Say 'readability first, check the plan'.

### Q29 ⭐⭐ 🟡 Update or delete rows using a subquery (e.g., remove employees whose department no longer exists).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you change data safely using a subquery, and do you know the NULL and safety traps?
**Say this in the interview:** "In DELETE or UPDATE the WHERE clause can contain a subquery. To remove orphans I use NOT EXISTS against the departments table. I run it first as a SELECT, and in a transaction, so I can check before committing."
**Explain simply:**
- **DELETE** removes rows; **UPDATE** changes values. Both can filter with `WHERE ... (subquery)`.
- Orphan = an employee whose department id is missing from departments (e.g. a department was closed).
- Prefer `NOT EXISTS` over `NOT IN`: NOT IN deletes nothing if the subquery returns a NULL.
- MySQL does not allow a subquery on the same table you are updating or deleting (error 1093); wrap it in a derived table or use a JOIN. SQL Server / PostgreSQL allow it.
**Example:** Ira (id 9) is in department 9, which does not exist, so Ira's row is deleted. HR salaries go up 10% (Asha 50,000 to 55,000).
**Sample data:**

*employees (before)*

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 70000 |
| 9 | Ira | 9 | 45000 |

*departments* (there is no department 9)

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Finance |

**SQL:**
```sql
DELETE FROM employees
WHERE NOT EXISTS (SELECT 1 FROM departments d WHERE d.dept_id = employees.dept_id);

UPDATE employees SET salary = salary * 11 / 10      -- +10% (integer math)
WHERE dept_id = (SELECT dept_id FROM departments WHERE dept_name = 'HR');

-- Safe habit: run the WHERE as a SELECT first, and wrap in BEGIN ... COMMIT / ROLLBACK.
```
**Output:**

After both statements (3 rows left; Ira was deleted):

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 55000 |
| 2 | Bala | 1 | 66000 |
| 3 | Chitra | 2 | 70000 |
**pandas equivalent:**
```python
# employees, departments are DataFrames; here we edit them in memory (a database UPDATE/DELETE changes the table itself)
employees = employees[employees.dept_id.isin(departments.dept_id)].copy()      # DELETE orphans
hr = departments.loc[departments.dept_name == 'HR', 'dept_id'].iloc[0]
employees.loc[employees.dept_id == hr, 'salary'] = employees.salary * 11 // 10   # UPDATE HR +10%
# Output (matches the SQL):
#  emp_id   name  dept_id  salary
#       1   Asha        1   55000
#       2   Bala        1   66000
#       3 Chitra        2   70000
```
**Edge cases:** A subquery returning more than one row in `= (subquery)` raises an error in most databases (SQLite silently takes the first row); use IN. NULL dept_id: `NOT EXISTS` treats an employee with NULL department as an orphan and deletes it; decide if that is wanted.
**Likely follow-ups:**
- How to undo a wrong delete? Use a transaction (ROLLBACK) or restore from a backup.
- What if the foreign key forbids it? The database stops the delete, which is the safer design.
**Common mistakes:** Running DELETE without WHERE, not testing as SELECT first, and using NOT IN with a column that may contain NULL.

### Q30 ⭐⭐ 🟡 Find students who took Maths but not Physics (subquery / EXISTS / EXCEPT).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you write an **anti-join** (rows with no match) and spot that one student can have many rows?
**Say this in the interview:** "I keep students who have a Maths row and do not have a Physics row, using EXISTS and NOT EXISTS. EXCEPT also works. I avoid a plain WHERE subject='Maths' AND subject<>'Physics' because that compares one row at a time and would still return Anil."
**Explain simply:**
- **EXISTS** asks 'is there at least one matching row?'. **NOT EXISTS** asks 'is there none?'.
- Each student has several enrolment rows, so the 'not Physics' test must look across all their rows, hence a subquery.
- **EXCEPT** (called MINUS in Oracle) returns rows in the first list that are not in the second; it also removes duplicates.
**Example:** Anil and Esha take both subjects, so they are excluded. Deep takes only Physics. Bina (Maths) and Charu (Maths, Chemistry) qualify.
**Sample data:**

*students*

| student_id | name |
|---|---|
| 1 | Anil |
| 2 | Bina |
| 3 | Charu |
| 4 | Deep |
| 5 | Esha |

*enrolments*

| student_id | subject |
|---|---|
| 1 | Maths |
| 1 | Physics |
| 2 | Maths |
| 3 | Maths |
| 3 | Chemistry |
| 4 | Physics |
| 5 | Maths |
| 5 | Physics |
**SQL:**
```sql
SELECT s.name
FROM students s
WHERE EXISTS (SELECT 1 FROM enrolments e WHERE e.student_id = s.student_id AND e.subject = 'Maths')
  AND NOT EXISTS (SELECT 1 FROM enrolments e WHERE e.student_id = s.student_id AND e.subject = 'Physics')
ORDER BY s.name;

-- EXCEPT (set difference; MINUS in Oracle) (also run here, same result)
SELECT s.name FROM students s JOIN enrolments e ON e.student_id = s.student_id WHERE e.subject = 'Maths'
EXCEPT
SELECT s.name FROM students s JOIN enrolments e ON e.student_id = s.student_id WHERE e.subject = 'Physics'
ORDER BY name;

-- NOT IN (safe here only because student_id is never NULL) (also run here, same result)
SELECT s.name FROM students s
WHERE s.student_id IN (SELECT student_id FROM enrolments WHERE subject = 'Maths')
  AND s.student_id NOT IN (SELECT student_id FROM enrolments WHERE subject = 'Physics')
ORDER BY s.name;
```
**Output:**

| name |
|---|
| Bina |
| Charu |
**pandas equivalent:**
```python
# each table above is a pandas DataFrame with the same name (employees, departments, orders, ...)
maths = set(enrolments.loc[enrolments.subject == 'Maths', 'student_id'])
phys = set(enrolments.loc[enrolments.subject == 'Physics', 'student_id'])
res = students[students.student_id.isin(maths - phys)][['name']].sort_values('name').reset_index(drop=True)
# Output (matches the SQL):
#  name
#  Bina
# Charu
```
**Edge cases:** Duplicate enrolment rows do not matter for EXISTS. A student with no enrolments never appears. NOT IN returns nothing if `student_id` in the subquery can be NULL. EXCEPT removes duplicates and compares all selected columns.
**Likely follow-ups:**
- Maths AND Physics? Use two EXISTS, or INTERSECT.
- Why not `WHERE subject = 'Maths' AND subject <> 'Physics'`? It is evaluated per row, so it returns every Maths row, including Anil's.
**Common mistakes:** Filtering the enrolment table row by row, or using NOT IN on a nullable column.

### Q31 ⭐⭐ 🟡 Count employees per department, including departments with zero employees, using a subquery in SELECT.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know a plain GROUP BY on employees would silently drop empty departments?
**Say this in the interview:** "I start from the departments table, and for each department a scalar subquery counts its employees. A scalar subquery returns one value, so an empty department gives 0 rather than disappearing."
**Explain simply:**
- Starting the query from `departments` guarantees every department appears, even Finance with nobody in it.
- The subquery in SELECT is **correlated**: it uses `d.dept_id` from the outer row and returns exactly one number.
- The LEFT JOIN version gives the same result; with it, count `e.emp_id`, not `*`, otherwise empty departments show 1.
**Example:** HR 2, Finance 0, IT 3, Sales 3. An HR manager asking 'which departments have no one?' needs Finance to be shown.
**Sample data:**

*employees*

| emp_id | name | dept_id | salary | left_date |
|---|---|---|---|---|
| 1 | Asha | 1 | 50000 | NULL |
| 2 | Bala | 1 | 60000 | 2026-03-31 |
| 3 | Chitra | 2 | 70000 | NULL |
| 4 | Dev | 2 | 90000 | 2026-06-30 |
| 5 | Esha | 2 | 90000 | NULL |
| 6 | Farid | 3 | 80000 | NULL |
| 7 | Gita | 3 | 120000 | NULL |
| 8 | Hari | 3 | 120000 | NULL |

*departments*

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Sales |
| 3 | IT |
| 4 | Finance |
**SQL:**
```sql
SELECT d.dept_name,
       (SELECT COUNT(*) FROM employees e WHERE e.dept_id = d.dept_id) AS headcount
FROM departments d
ORDER BY d.dept_name;

-- JOIN version: COUNT a column of the right table, not COUNT(*) (also run here, same result)
SELECT d.dept_name, COUNT(e.emp_id) AS headcount
FROM departments d LEFT JOIN employees e ON e.dept_id = d.dept_id
GROUP BY d.dept_id, d.dept_name
ORDER BY d.dept_name;
```
**Output:**

| dept_name | headcount |
|---|---|
| Finance | 0 |
| HR | 2 |
| IT | 3 |
| Sales | 3 |
**pandas equivalent:**
```python
# each table above is a pandas DataFrame with the same name (employees, departments, orders, ...)
cnt = employees.groupby('dept_id').size().rename('headcount').reset_index()
res = (departments.merge(cnt, on='dept_id', how='left').fillna({'headcount': 0})
       .astype({'headcount': int})[['dept_name','headcount']].sort_values('dept_name').reset_index(drop=True))
# Output (matches the SQL):
# dept_name  headcount
#   Finance          0
#        HR          2
#        IT          3
#     Sales          3
```
**Edge cases:** A scalar subquery that returns more than one row is an error. COUNT returns 0 (not NULL) when there are no rows, but SUM would return NULL (wrap in COALESCE). Employees with NULL dept_id are not counted anywhere.
**Likely follow-ups:**
- Which is faster, subquery or join? Usually the same on modern engines; check the plan.
- Why COUNT(e.emp_id)? COUNT of a column skips NULLs; the LEFT JOIN makes a NULL row for empty departments.
**Common mistakes:** Using `FROM employees GROUP BY dept_id`, which never shows departments with zero employees, or `COUNT(*)` after a LEFT JOIN (gives 1 for empty departments).

### Q32 ⭐⭐ 🟡 Write a query using a subquery and a join together: list orders from customers in the city that has the most customers.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you combine a subquery and a JOIN in one query, and do you think about ties?
**Say this in the interview:** "I use a subquery to find the city with the most customers, then join orders to customers and keep customers in that city. The LIMIT 1 version picks one city on a tie, so I would mention the HAVING = MAX version too."
**Explain simply:**
- Subquery job: return one value, the busiest city (Hyderabad: 3 customers).
- JOIN job: attach each order to its customer's city so we can filter.
- Dialect: `LIMIT 1` is MySQL/PostgreSQL/SQLite; `TOP 1` is SQL Server; `FETCH FIRST 1 ROW ONLY` is the standard (Oracle 12c+, PostgreSQL).
**Example:** Hyderabad has 3 customers (Ravi, Sita, Tara), so only their 5 orders are listed. Orders from Bengaluru and others are left out.
**Sample data:**

*customers*

| customer_id | name | city |
|---|---|---|
| 1 | Ravi | Hyderabad |
| 2 | Sita | Hyderabad |
| 3 | Tara | Hyderabad |
| 4 | Uma | Bengaluru |
| 5 | Vik | Bengaluru |
| 6 | Wen | Pune |
| 7 | Xan | Chennai |

*orders*

| order_id | customer_id | product_id | order_date | amount |
|---|---|---|---|---|
| 101 | 1 | 1 | 2026-01-05 | 200 |
| 102 | 1 | 2 | 2026-01-20 | 300 |
| 103 | 2 | 1 | 2026-02-03 | 150 |
| 104 | 3 | 3 | 2026-02-14 | 400 |
| 105 | 4 | 2 | 2026-02-25 | 250 |
| 106 | 4 | 1 | 2026-03-02 | 500 |
| 107 | 5 | 3 | 2026-03-15 | 100 |
| 108 | 2 | 2 | 2026-03-28 | 600 |
**SQL:**
```sql
SELECT o.order_id, c.name, c.city, o.amount
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
WHERE c.city = (SELECT city
                FROM customers
                GROUP BY city
                ORDER BY COUNT(*) DESC
                LIMIT 1)   -- SQL Server: SELECT TOP 1 city ...; Oracle 12c+: FETCH FIRST 1 ROW ONLY
ORDER BY o.order_id;

-- Tie-safe version (returns all cities tied for the most customers) (also run here, same result)
SELECT o.order_id, c.name, c.city, o.amount
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
WHERE c.city IN (SELECT city FROM customers GROUP BY city
                 HAVING COUNT(*) = (SELECT MAX(n) FROM (SELECT COUNT(*) AS n FROM customers GROUP BY city) t))
ORDER BY o.order_id;
```
**Output:**

| order_id | name | city | amount |
|---|---|---|---|
| 101 | Ravi | Hyderabad | 200 |
| 102 | Ravi | Hyderabad | 300 |
| 103 | Sita | Hyderabad | 150 |
| 104 | Tara | Hyderabad | 400 |
| 108 | Sita | Hyderabad | 600 |
**pandas equivalent:**
```python
# each table above is a pandas DataFrame with the same name (employees, departments, orders, ...)
top = customers.city.value_counts()
cities = top[top == top.max()].index
m = orders.merge(customers, on='customer_id')
res = m[m.city.isin(cities)][['order_id','name','city','amount']].sort_values('order_id').reset_index(drop=True)
# Output (matches the SQL):
#  order_id name      city  amount
#       101 Ravi Hyderabad     200
#       102 Ravi Hyderabad     300
#       103 Sita Hyderabad     150
#       104 Tara Hyderabad     400
#       108 Sita Hyderabad     600
```
**Edge cases:** Tie on customer count: LIMIT 1 returns an arbitrary one of them (add a tie-breaker to ORDER BY). Customers with no orders produce no rows because of the inner join. NULL cities form their own group and could win.
**Likely follow-ups:**
- What if two cities tie? Use the HAVING = MAX version.
- Could you do it without a subquery? Yes, with a window function COUNT(*) OVER (PARTITION BY city) and RANK.
**Common mistakes:** Joining first and then using `LIMIT 1` for the whole query (returns one order, not the city's orders).

### Q33 ⭐⭐ 🔴 Write a query that uses a CTE and then joins it to another table for a final report (e.g., HR attrition by department).
**Asked at:** GCC and service MNC (candidate reports mention basic CTE questions, e.g. Microsoft Hyderabad DA and Wipro 2023; HR attrition is my example, not a reported question)
**What the interviewer is checking:** Can you prepare numbers per group in a CTE and then join them to a master table to build a report?
**Say this in the interview:** "First a CTE computes headcount and leavers per department. Then I LEFT JOIN it to the departments table, so departments with nobody still show, and compute attrition as leavers divided by headcount."
**Explain simply:**
- **Attrition** = people who left / people in the department (simple version; many HR teams divide by average headcount over the period).
- `CASE WHEN left_date IS NOT NULL THEN 1 ELSE 0 END` turns each row into a 0/1 flag, and `SUM` counts leavers.
- `NULLIF(x, 0)` turns 0 into NULL so division by zero does not crash; the result is NULL, meaning 'not applicable'.
- LEFT JOIN keeps Finance (no employees).
**Example:** HR: 2 people, 1 left in March = 50%. Sales: 3 people, 1 left = 33.3%. IT: 0 leavers = 0%. Finance: no staff, so attrition is undefined.
**Sample data:**

*employees*

| emp_id | name | dept_id | salary | left_date |
|---|---|---|---|---|
| 1 | Asha | 1 | 50000 | NULL |
| 2 | Bala | 1 | 60000 | 2026-03-31 |
| 3 | Chitra | 2 | 70000 | NULL |
| 4 | Dev | 2 | 90000 | 2026-06-30 |
| 5 | Esha | 2 | 90000 | NULL |
| 6 | Farid | 3 | 80000 | NULL |
| 7 | Gita | 3 | 120000 | NULL |
| 8 | Hari | 3 | 120000 | NULL |

*departments*

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Sales |
| 3 | IT |
| 4 | Finance |
**SQL:**
```sql
WITH dept_stats AS (
    SELECT dept_id,
           COUNT(*) AS headcount,
           SUM(CASE WHEN left_date IS NOT NULL THEN 1 ELSE 0 END) AS leavers
    FROM employees
    GROUP BY dept_id
)
SELECT d.dept_name,
       COALESCE(s.headcount, 0) AS headcount,
       COALESCE(s.leavers, 0)   AS leavers,
       ROUND(100.0 * s.leavers / NULLIF(s.headcount, 0), 1) AS attrition_pct
FROM departments d
LEFT JOIN dept_stats s ON s.dept_id = d.dept_id
ORDER BY d.dept_name;
```
**Output:**

| dept_name | headcount | leavers | attrition_pct |
|---|---|---|---|
| Finance | 0 | 0 | NULL |
| HR | 2 | 1 | 50.0 |
| IT | 3 | 0 | 0.0 |
| Sales | 3 | 1 | 33.3 |
**pandas equivalent:**
```python
# each table above is a pandas DataFrame with the same name (employees, departments, orders, ...)
st = (employees.assign(left=employees.left_date.notna().astype(int)).groupby('dept_id')
      .agg(headcount=('emp_id','size'), leavers=('left','sum')).reset_index())
m = departments.merge(st, on='dept_id', how='left')
m['attrition_pct'] = (100.0 * m.leavers / m.headcount.where(m.headcount != 0)).round(1)
m[['headcount','leavers']] = m[['headcount','leavers']].fillna(0).astype(int)
res = m[['dept_name','headcount','leavers','attrition_pct']].sort_values('dept_name').reset_index(drop=True)
# Output (matches the SQL):
# dept_name  headcount  leavers  attrition_pct
#   Finance          0        0            NaN
#        HR          2        1           50.0
#        IT          3        0            0.0
#     Sales          3        1           33.3
```
**Edge cases:** Division by zero (empty department) handled by NULLIF; show NULL or 'n/a', not 0%. Integer division: use `100.0 *` to avoid 0 (SQL Server, PostgreSQL truncate integer division). Rehires or duplicate employee rows would inflate counts.
**Likely follow-ups:**
- How to get monthly attrition? Group leavers by month of left_date and divide by that month's average headcount.
- Why a CTE here? The aggregation is separate from the join, so each step is easy to test.
**Common mistakes:** Dividing integers (result 0), using an INNER JOIN (drops empty departments), or not handling division by zero.

### Q34 ⭐⭐ 🔴 Use a CTE to calculate month-over-month sales growth (join a monthly-sales CTE to itself, or use LAG).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you compare a row with the previous row, and guard against the first month having no previous?
**Say this in the interview:** "I make a monthly totals CTE, then use LAG to bring the previous month's total onto the same row, and compute (this - previous) / previous. The first month has no previous, so growth is NULL."
**Explain simply:**
- **Month-over-month (MoM) growth** = (this month - last month) / last month, shown as a percentage.
- **LAG(total)** is a window function: it reads the value from the previous row in the order you give.
- The self-join alternative joins the CTE to itself on 'month = previous month'; it also survives missing months correctly, whereas LAG just takes the previous existing row.
**Example:** Sales: Jan 500, Feb 800, Mar 1,200. Feb growth = (800-500)/500 = 60%. Mar = (1200-800)/800 = 50%.
**Sample data:**

*orders*

| order_id | customer_id | product_id | order_date | amount |
|---|---|---|---|---|
| 101 | 1 | 1 | 2026-01-05 | 200 |
| 102 | 1 | 2 | 2026-01-20 | 300 |
| 103 | 2 | 1 | 2026-02-03 | 150 |
| 104 | 3 | 3 | 2026-02-14 | 400 |
| 105 | 4 | 2 | 2026-02-25 | 250 |
| 106 | 4 | 1 | 2026-03-02 | 500 |
| 107 | 5 | 3 | 2026-03-15 | 100 |
| 108 | 2 | 2 | 2026-03-28 | 600 |
**SQL:**
```sql
WITH monthly AS (
    SELECT strftime('%Y-%m', order_date) AS month, SUM(amount) AS total
    FROM orders GROUP BY strftime('%Y-%m', order_date)
)
SELECT month, total,
       LAG(total) OVER (ORDER BY month) AS prev_total,
       ROUND(100.0 * (total - LAG(total) OVER (ORDER BY month))
             / LAG(total) OVER (ORDER BY month), 1) AS mom_growth_pct
FROM monthly
ORDER BY month;

-- Self-join version (works without window functions) (also run here, same result)
WITH monthly AS (
    SELECT strftime('%Y-%m', order_date) AS month, SUM(amount) AS total
    FROM orders GROUP BY strftime('%Y-%m', order_date)
)
SELECT cur.month, cur.total, prev.total AS prev_total,
       ROUND(100.0 * (cur.total - prev.total) / prev.total, 1) AS mom_growth_pct
FROM monthly cur
LEFT JOIN monthly prev ON prev.month = strftime('%Y-%m', date(cur.month || '-01', '-1 month'))
ORDER BY cur.month;
```
**Output:**

| month | total | prev_total | mom_growth_pct |
|---|---|---|---|
| 2026-01 | 500 | NULL | NULL |
| 2026-02 | 800 | 500 | 60.0 |
| 2026-03 | 1200 | 800 | 50.0 |
**pandas equivalent:**
```python
# each table above is a pandas DataFrame with the same name (employees, departments, orders, ...)
m = (orders.assign(month=orders.order_date.str[:7]).groupby('month', as_index=False).amount.sum()
     .rename(columns={'amount':'total'}).sort_values('month'))
m['prev_total'] = m.total.shift(1)
m['mom_growth_pct'] = (100 * (m.total - m.prev_total) / m.prev_total).round(1)
res = m[['month','total','prev_total','mom_growth_pct']].reset_index(drop=True)
# Output (matches the SQL):
#   month  total  prev_total  mom_growth_pct
# 2026-01    500         NaN             NaN
# 2026-02    800       500.0            60.0
# 2026-03   1200       800.0            50.0
```
**Edge cases:** First month: NULL growth. If a month is missing (no orders), LAG compares with the earlier month, not the calendar-previous one; fill gaps with a calendar table. Previous total of 0 gives division by zero: use NULLIF. Use `100.0 *` so integer math does not truncate.
**Likely follow-ups:**
- Year-over-year? `LAG(total, 12)` on monthly data, or join to the same month last year.
- LAG not available (old MySQL 5.7)? Use the self-join.
**Common mistakes:** Using integer division (all growth 0%), sorting the LAG by a text month name like 'Feb' (alphabetical, wrong), or forgetting that the first row is NULL.

### Q35 ⭐⭐ 🔴 Find each product's percentage of total sales using a CTE or scalar subquery.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you compute a 'share of total' by bringing a grand total next to each group?
**Say this in the interview:** "I sum sales per product and divide by the grand total from a scalar subquery. Multiply by 100.0 so it is a decimal percentage. The window version SUM(SUM(x)) OVER () does the same in one pass."
**Explain simply:**
- The grand total (2,500) is one number, so a scalar subquery in SELECT works.
- `100.0 *` forces decimal math; `100 * 850 / 2500` in integers would give 34 only by luck and would truncate otherwise.
- Percentages should add to about 100; rounding can make 99.9 or 100.1.
**Example:** Mouse 1,150 of 2,500 = 46.0%; Laptop 850 = 34.0%; Monitor 500 = 20.0%.
**Sample data:**

*orders*

| order_id | customer_id | product_id | order_date | amount |
|---|---|---|---|---|
| 101 | 1 | 1 | 2026-01-05 | 200 |
| 102 | 1 | 2 | 2026-01-20 | 300 |
| 103 | 2 | 1 | 2026-02-03 | 150 |
| 104 | 3 | 3 | 2026-02-14 | 400 |
| 105 | 4 | 2 | 2026-02-25 | 250 |
| 106 | 4 | 1 | 2026-03-02 | 500 |
| 107 | 5 | 3 | 2026-03-15 | 100 |
| 108 | 2 | 2 | 2026-03-28 | 600 |

*products*

| product_id | product_name |
|---|---|
| 1 | Laptop |
| 2 | Mouse |
| 3 | Monitor |
**SQL:**
```sql
SELECT p.product_name,
       SUM(o.amount) AS sales,
       ROUND(100.0 * SUM(o.amount) / (SELECT SUM(amount) FROM orders), 1) AS pct_of_total
FROM orders o
JOIN products p ON p.product_id = o.product_id
GROUP BY p.product_id, p.product_name
ORDER BY sales DESC;

-- CTE version (also run here, same result)
WITH by_product AS (SELECT product_id, SUM(amount) AS sales FROM orders GROUP BY product_id),
     total AS (SELECT SUM(sales) AS grand FROM by_product)
SELECT p.product_name, b.sales, ROUND(100.0 * b.sales / t.grand, 1) AS pct_of_total
FROM by_product b JOIN products p ON p.product_id = b.product_id CROSS JOIN total t
ORDER BY b.sales DESC;

-- Window version (also run here, same result)
SELECT p.product_name, SUM(o.amount) AS sales,
       ROUND(100.0 * SUM(o.amount) / SUM(SUM(o.amount)) OVER (), 1) AS pct_of_total
FROM orders o JOIN products p ON p.product_id = o.product_id
GROUP BY p.product_id, p.product_name
ORDER BY sales DESC;
```
**Output:**

| product_name | sales | pct_of_total |
|---|---|---|
| Mouse | 1150 | 46.0 |
| Laptop | 850 | 34.0 |
| Monitor | 500 | 20.0 |
**pandas equivalent:**
```python
# each table above is a pandas DataFrame with the same name (employees, departments, orders, ...)
t = orders.merge(products, on='product_id').groupby('product_name', as_index=False).amount.sum().rename(columns={'amount':'sales'})
t['pct_of_total'] = (100.0 * t.sales / t.sales.sum()).round(1)
res = t.sort_values('sales', ascending=False).reset_index(drop=True)
# Output (matches the SQL):
# product_name  sales  pct_of_total
#        Mouse   1150          46.0
#       Laptop    850          34.0
#      Monitor    500          20.0
```
**Edge cases:** Total of 0 gives division by zero (use NULLIF). NULL amounts are skipped by SUM. If the filter (e.g. one category) is applied, decide whether the denominator should be filtered too; the scalar subquery above is not filtered, so it stays the whole-company total.
**Likely follow-ups:**
- Percent within category? Use a window `SUM(...) OVER (PARTITION BY category)`.
- Why not AVG? Share of total needs the sum, not the mean.
**Common mistakes:** Integer division (everything shows 0), or computing the total inside the same GROUP BY so each row divides by itself (100%).

### Q36 ⭐⭐ 🔴 Why can a correlated subquery be slow? How would you rewrite it for speed?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand that a correlated subquery can run once per outer row, and can you rewrite it as a join or window?
**Say this in the interview:** "A correlated subquery depends on the outer row, so conceptually it runs once for every row: 1 million employees means up to 1 million small queries. I rewrite it so the department average is calculated once per department and joined back, or use a window function."
**Explain simply:**
- Slow part: repeated work. With N outer rows and an inner scan of M rows it can approach N x M.
- Fix 1: pre-aggregate in a derived table or CTE (one pass), then JOIN.
- Fix 2: a window function (`AVG() OVER (PARTITION BY dept_id)`).
- Fix 3: an index on the correlated column (`dept_id`) so each inner lookup is fast.
- Optimisers often rewrite simple correlated subqueries themselves, so measure with EXPLAIN before assuming it is slow.
**Example:** Employees above their own department average (HR avg 55k, Sales 83.3k, IT 106.7k): Bala, Dev, Esha, Gita, Hari. All three forms give this same answer.
**Sample data:**

*employees*

| emp_id | name | dept_id | salary | left_date |
|---|---|---|---|---|
| 1 | Asha | 1 | 50000 | NULL |
| 2 | Bala | 1 | 60000 | 2026-03-31 |
| 3 | Chitra | 2 | 70000 | NULL |
| 4 | Dev | 2 | 90000 | 2026-06-30 |
| 5 | Esha | 2 | 90000 | NULL |
| 6 | Farid | 3 | 80000 | NULL |
| 7 | Gita | 3 | 120000 | NULL |
| 8 | Hari | 3 | 120000 | NULL |

**SQL:**
```sql
-- slow-prone: correlated
SELECT name, dept_id, salary
FROM employees e
WHERE salary > (SELECT AVG(salary) FROM employees x WHERE x.dept_id = e.dept_id)
ORDER BY dept_id, name;

-- rewrite 1: join to pre-aggregated averages
SELECT e.name, e.dept_id, e.salary
FROM employees e
JOIN (SELECT dept_id, AVG(salary) AS avg_sal FROM employees GROUP BY dept_id) a
  ON a.dept_id = e.dept_id
WHERE e.salary > a.avg_sal
ORDER BY e.dept_id, e.name;

-- rewrite 2: window function
SELECT name, dept_id, salary
FROM (SELECT *, AVG(salary) OVER (PARTITION BY dept_id) AS avg_sal FROM employees) t
WHERE salary > avg_sal
ORDER BY dept_id, name;
```
**Output:**

All three return:

| name | dept_id | salary |
|---|---|---|
| Bala | 1 | 60000 |
| Dev | 2 | 90000 |
| Esha | 2 | 90000 |
| Gita | 3 | 120000 |
| Hari | 3 | 120000 |

SQLite plan for the correlated version:
```
  SCAN e
  CORRELATED SCALAR SUBQUERY 1
  SCAN x
  USE TEMP B-TREE FOR ORDER BY
```
SQLite plan for the join version:
```
  CO-ROUTINE a
  SCAN employees
  USE TEMP B-TREE FOR GROUP BY
  SCAN e
  BLOOM FILTER ON a (dept_id=?)
  SEARCH a USING AUTOMATIC COVERING INDEX (dept_id=?)
  USE TEMP B-TREE FOR ORDER BY
```
**pandas equivalent:** (the `transform` is the "join back" or window rewrite: one pass, no per-row re-run)
```python
employees['avg_sal'] = employees.groupby('dept_id').salary.transform('mean')
result = employees[employees.salary > employees.avg_sal].sort_values(['dept_id','name'])[['name','dept_id','salary']].reset_index(drop=True)
```
**Edge cases:** NULL salaries are ignored by AVG; all three forms agree. A department with a single employee never has salary > its own average. The speed gap only shows on large tables; at 8 rows nothing is slow.
**Likely follow-ups:**
- How do you prove it is slow? Run EXPLAIN (ANALYZE in PostgreSQL) and compare time and rows scanned.
- Is EXISTS correlated too? Yes, but it stops at the first match, so it is usually fine.
**Common mistakes:** Assuming correlated is always slow (engines can optimise it), or 'fixing' it without checking the plan or adding an index.

### Q37 ⭐ 🟢 Can a CTE be used with INSERT, UPDATE or DELETE? Give an example.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know a CTE is not limited to SELECT, and the dialect rules?
**Say this in the interview:** "Yes. Most databases let you put WITH in front of INSERT, UPDATE or DELETE, or use a CTE inside INSERT ... SELECT. PostgreSQL even lets the CTE itself contain the DELETE or UPDATE with RETURNING."
**Explain simply:**
- The CTE just prepares the list of rows; the INSERT/UPDATE/DELETE then uses it like any table.
- **SQLite / PostgreSQL / SQL Server / MySQL 8**: `WITH ... UPDATE` and `WITH ... DELETE` work (SQL Server needs the previous statement to end with `;`). `INSERT ... WITH ... SELECT` works everywhere that supports CTEs; the position of WITH differs (PostgreSQL and SQLite also allow it before INSERT).
- **SQL Server** can also update or delete through the CTE directly: `WITH c AS (...) DELETE FROM c;` changes the underlying table (not run here).
- **PostgreSQL** allows data-modifying CTEs: `WITH d AS (DELETE FROM t WHERE ... RETURNING *) INSERT INTO archive SELECT * FROM d;` (not run here). Oracle: do not put WITH in front of UPDATE/DELETE; put it inside a subquery (not run here).
**Example:** HR housekeeping: give HR staff +5,000, copy leavers to an archive table, then remove them from the live table.
**Sample data:**

*employees*

| emp_id | name | dept_id | salary | left_date |
|---|---|---|---|---|
| 1 | Asha | 1 | 50000 | NULL |
| 2 | Bala | 1 | 60000 | 2026-03-31 |
| 3 | Chitra | 2 | 70000 | NULL |
| 4 | Dev | 2 | 90000 | 2026-06-30 |
| 5 | Esha | 2 | 90000 | NULL |
| 6 | Farid | 3 | 80000 | NULL |
| 7 | Gita | 3 | 120000 | NULL |
| 8 | Hari | 3 | 120000 | NULL |

*departments*

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Sales |
| 3 | IT |
| 4 | Finance |

*leavers* starts as an empty archive table: `CREATE TABLE leavers (emp_id, name, left_date);`

**SQL:**
```sql
-- UPDATE (run in SQLite)
WITH hr AS (SELECT dept_id FROM departments WHERE dept_name = 'HR')
UPDATE employees SET salary = salary + 5000 WHERE dept_id IN (SELECT dept_id FROM hr);

-- INSERT
WITH gone AS (SELECT emp_id, name, left_date FROM employees WHERE left_date IS NOT NULL)
INSERT INTO leavers SELECT emp_id, name, left_date FROM gone;

-- DELETE
WITH gone AS (SELECT emp_id FROM leavers)
DELETE FROM employees WHERE emp_id IN (SELECT emp_id FROM gone);
```
**Output:**

Table `employees` afterwards (Bala and Dev removed; Asha +5,000, Bala's rise was applied before deletion):

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 55000 |
| 3 | Chitra | 2 | 70000 |
| 5 | Esha | 2 | 90000 |
| 6 | Farid | 3 | 80000 |
| 7 | Gita | 3 | 120000 |
| 8 | Hari | 3 | 120000 |

Table `leavers`:

| emp_id | name | left_date |
|---|---|---|
| 2 | Bala | 2026-03-31 |
| 4 | Dev | 2026-06-30 |

**pandas equivalent:** (in-memory edits, same three steps)
```python
leavers = employees.loc[employees.left_date.notna(), ['emp_id','name','left_date']]          # INSERT into archive
hr = departments.loc[departments.dept_name == 'HR', 'dept_id']
employees.loc[employees.dept_id.isin(hr), 'salary'] += 5000                                  # UPDATE
employees = employees[~employees.emp_id.isin(leavers.emp_id)]                                 # DELETE
```
**Edge cases:** Run the CTE as a SELECT first to see which rows will change. In a transaction you can ROLLBACK. A CTE cannot be reused by the next statement; it lives for one statement only.
**Likely follow-ups:**
- Why not just a subquery? Same effect; a CTE helps when the list is complex or used twice.
- Is it atomic? One statement is atomic; wrap several in a transaction.
**Common mistakes:** Forgetting the `;` before WITH in SQL Server, or assuming the CTE survives into the next statement.

### Q38 ⭐ 🟢 Do all databases support CTEs? (SQL Server, PostgreSQL, MySQL 8+ vs older MySQL, Oracle) Any syntax differences?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Practical awareness: will your query run on the company's database?
**Say this in the interview:** "Almost all modern databases support CTEs: PostgreSQL, SQL Server, Oracle, MySQL 8 and later, SQLite. The exception is MySQL 5.7 and older, where I would use a derived table or temp table instead. Basic syntax is the same; recursive CTEs differ slightly."
**Explain simply:**
- A CTE is standard SQL (SQL:1999), so the basic `WITH name AS (...) SELECT ...` is identical everywhere it is supported.
- Differences are around `RECURSIVE`, the `;` rule in SQL Server, and extras like MATERIALIZED (PostgreSQL).
- Version dates in the table are from my knowledge of the vendors' release notes (I did not re-check them here); verify for your exact version.
- Ask which database and version the team uses; interviews often do not care, but job tasks do.
**Example:** A company still on MySQL 5.7 cannot run `WITH`; the same logic goes into a subquery in FROM.
**Sample data:** the 8-row `employees` table from Q1 (department totals: 1 = 110,000; 2 = 150,000; 3 = 300,000; 4 = 40,000).
**SQL:**
```sql
-- Portable basic CTE (same text in PostgreSQL, SQL Server, MySQL 8+, Oracle, SQLite)
WITH dept_cost AS (SELECT dept_id, SUM(salary) AS cost FROM employees GROUP BY dept_id)
SELECT dept_id, cost FROM dept_cost WHERE cost > 100000;

-- Recursive: PostgreSQL / MySQL / SQLite need the word RECURSIVE (run here in SQLite)
WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 3)
SELECT i FROM n;
-- SQL Server and Oracle: same but write 'WITH n(i) AS ...' without RECURSIVE (not run here)

-- MySQL 5.7 workaround: put the CTE in FROM as a derived table
SELECT dept_id, cost
FROM (SELECT dept_id, SUM(salary) AS cost FROM employees GROUP BY dept_id) dept_cost
WHERE cost > 100000;
```
**Output:**

Portable CTE and the MySQL 5.7 derived-table version (both give the same rows; checked in SQLite):

| dept_id | cost |
|---|---|
| 1 | 110000 |
| 2 | 150000 |
| 3 | 300000 |

Recursive demo result (SQLite):

| i |
|---|
| 1 |
| 2 |
| 3 |

| Database | CTE support | Notes |
|---|---|---|
| PostgreSQL | Yes, since 8.4 (2009) | Needs `RECURSIVE` keyword for recursive CTEs; supports data-modifying CTEs; `MATERIALIZED` hints from 12 |
| SQL Server | Yes, since 2005 | No `RECURSIVE` keyword; previous statement must end with `;`; `OPTION (MAXRECURSION n)` limits depth (default 100) |
| MySQL | Yes, only from 8.0 | 5.7 and older: **no CTEs**, use derived tables, temp tables or views; `RECURSIVE` keyword needed |
| MariaDB | Yes, since 10.2 | Similar to MySQL |
| Oracle | Yes, 'subquery factoring', since 9i R2; recursive since 11gR2 | No `RECURSIVE` keyword; recursive CTE needs a column alias list; scalar SELECT needs `FROM dual` |
| SQLite | Yes, since 3.8.3 | Needs `RECURSIVE` |
**pandas equivalent:** (pandas has no CTE syntax; a named variable plays the same role)
```python
dept_cost = employees.groupby('dept_id', as_index=False).agg(cost=('salary','sum'))
result = dept_cost[dept_cost.cost > 100000]
```
**Edge cases:** On old versions the failure is a syntax error at `WITH`. Recursive CTEs have depth limits (SQL Server 100 by default).
**Likely follow-ups:**
- What replaces a CTE on MySQL 5.7? Derived tables, temporary tables or views.
- Is a recursive CTE supported everywhere? On the databases above yes, with the syntax differences noted (Part 10 covers it).
**Common mistakes:** Putting `WITH` after another statement in SQL Server without a semicolon, or writing RECURSIVE for SQL Server/Oracle where it is not allowed.

### Q39 ⭐ 🟡 What is a materialized vs inlined CTE? (PostgreSQL MATERIALIZED / NOT MATERIALIZED)
**Asked at:** commonly asked (no company-specific report found) (PostgreSQL-specific; mostly a differentiator at product / senior analytics rounds)
**What the interviewer is checking:** Whether you know a CTE is not always 'calculated once and saved', and that the database can choose.
**Say this in the interview:** A materialized CTE is computed once and stored as a temporary result. An inlined CTE is pasted into the main query like a subquery, so the optimizer can push filters into it. In PostgreSQL 12 and later I can force either with MATERIALIZED or NOT MATERIALIZED.
**Explain simply:**
- **CTE** = a named, temporary result written with `WITH`. **Materialized** = the database runs it once and keeps the rows in memory or temp storage. **Inlined** = the database treats it like a plain subquery and merges it into the outer query.
- PostgreSQL 11 and older always materialized a CTE (it acted as a wall the optimizer could not see through). From PostgreSQL 12, a CTE is inlined by default if it is not recursive, has no side effects and is used only once. If you use it two or more times, it is materialized by default.
- Use `MATERIALIZED` when the CTE is expensive and used many times, or when you want a guaranteed single computation. Use `NOT MATERIALIZED` when you want a filter in the outer query to be pushed inside the CTE.
- Other databases: SQL Server has no such keyword (CTEs are inlined, so a CTE used twice is calculated twice). Oracle uses hints `/*+ MATERIALIZE */` and `/*+ INLINE */`. MySQL 8 decides on its own. Check your version's docs (not run here).
**Example:** HR report: 'average salary per department' is needed twice in one query (once to filter employees, once to show on the report). Materializing it means the 8 employee rows are grouped once instead of twice. On 8 rows nobody notices; on 80 million payroll rows it matters.
**Sample data:**
`employees`

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 70000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farid | 3 | 80000 |
| 7 | Gita | 3 | 80000 |
| 8 | Hari | 4 | 65000 |
**SQL:**
*SQLite 3.35+ also accepts the same keywords, so this ran here*
```sql
WITH dept_avg AS MATERIALIZED (
  SELECT dept_id, AVG(salary) AS avg_sal FROM employees GROUP BY dept_id)
SELECT e.name, e.salary, d.avg_sal
FROM employees e JOIN dept_avg d ON d.dept_id = e.dept_id
WHERE e.salary > d.avg_sal
ORDER BY e.name
```
**Output:**

| name | salary | avg_sal |
|---|---|---|
| Bala | 60000 | 55000 |
| Esha | 90000 | 83333.33 |
**pandas equivalent:**
```python
g = employees.groupby('dept_id', as_index=False).agg(avg_sal=('salary','mean'))
m = employees.merge(g, on='dept_id')
result = m[m.salary > m.avg_sal][['name','salary','avg_sal']].sort_values('name')
```
(result checked identical to the SQL output)
**Inlined version (same result, checked):** swap `AS MATERIALIZED` for `AS NOT MATERIALIZED`.

Query plan SQLite printed for MATERIALIZED:
```text
  MATERIALIZE dept_avg
  SCAN employees
  USE TEMP B-TREE FOR GROUP BY
  SCAN e
  BLOOM FILTER ON d (dept_id=?)
  SEARCH d USING AUTOMATIC COVERING INDEX (dept_id=?)
  USE TEMP B-TREE FOR ORDER BY
```
Query plan for NOT MATERIALIZED:
```text
  CO-ROUTINE dept_avg
  SCAN employees
  USE TEMP B-TREE FOR GROUP BY
  SCAN e
  BLOOM FILTER ON d (dept_id=?)
  SEARCH d USING AUTOMATIC COVERING INDEX (dept_id=?)
  USE TEMP B-TREE FOR ORDER BY
```
**Edge cases:** Results are identical either way; only speed changes. A recursive CTE is always materialized. A CTE with side effects (e.g. a data-modifying CTE in PostgreSQL) is never inlined.
**Likely follow-ups:**
- Does the default ever hurt? Yes: if a materialized CTE returns a million rows and the outer query needs only 5, forcing NOT MATERIALIZED can be much faster.
- How do I check? Run EXPLAIN (ANALYZE) and look for a 'CTE Scan' node (materialized) versus the CTE body merged into the main plan (inlined).
**Common mistakes:** Saying 'a CTE is always stored'. That was true in old PostgreSQL only. Also using the keywords in MySQL or SQL Server, where they do not exist.

### Q40 ⭐ 🟡 Find employees who work in the same department as a named employee (subquery returning one value).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can use a subquery that returns exactly one value (a scalar) as a filter, and exclude the person themselves.
**Say this in the interview:** First I look up the named employee's department with a small inner query. The outer query then returns everyone in that department except that person. I filter by employee ID, not name, because names can repeat.
**Explain simply:**
- A **scalar subquery** is a query in brackets that returns one row and one column, so it can be used like a single value.
- The inner query runs first (it does not depend on the outer one) and the outer query compares `dept_id` to that value.
- Filtering on `emp_id` keeps the answer correct if two employees share a name. If the inner query could return two rows, most databases raise an error (SQLite quietly takes the first row, which is a trap).
**Example:** HR wants to invite colleagues of Esha (IT, 3 people) to a team lunch: the answer is Farid and Gita.
**Sample data:**
`employees`

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 70000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farid | 3 | 80000 |
| 7 | Gita | 3 | 80000 |
| 8 | Hari | 4 | 65000 |
**SQL:**
```sql
SELECT name, salary
FROM employees
WHERE dept_id = (SELECT dept_id FROM employees WHERE emp_id = 5)   -- 5 = Esha
  AND emp_id <> 5
ORDER BY name
```
**Output:**

| name | salary |
|---|---|
| Farid | 80000 |
| Gita | 80000 |
**pandas equivalent:**
```python
d = employees.loc[employees.emp_id == 5, 'dept_id'].iloc[0]
result = employees[(employees.dept_id == d) & (employees.emp_id != 5)][['name','salary']].sort_values('name')
```
(result checked identical to the SQL output)
**Edge cases:** Named employee not found: inner query returns NULL, `dept_id = NULL` is never true, so you get an empty result. Two employees with the same name: scalar subquery fails in PostgreSQL/MySQL/SQL Server ('more than one row'). Employee with NULL department: nobody matches. If you want to keep the person in the list, drop the `<>` line.
**Likely follow-ups:**
- How to write it with a self join? `FROM employees a JOIN employees b ON a.dept_id = b.dept_id WHERE a.emp_id = 5 AND b.emp_id <> 5`.
- What if the inner query can return many rows? Use `IN` instead of `=`.
**Common mistakes:** Using `=` with a subquery that can return many rows; matching on name rather than ID; forgetting to exclude the named person.

### Q41 ⭐ 🟡 Use a row-value subquery to match two columns at once: WHERE (dept_id, salary) IN (SELECT ...).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** That you know a row value (two or more columns in brackets) can be compared with `IN`, and what it replaces.
**Say this in the interview:** Instead of checking one column, I check a pair. The pair (dept_id, salary) of each employee must appear in the list of (dept, max salary) pairs from the inner query. It gives the top earner of every department, and keeps ties.
**Explain simply:**
- A **row value** (tuple) is a bracketed list like `(dept_id, salary)`. Matching it against a subquery that returns two columns means both values must match together, in the same row.
- Matching columns one at a time would be wrong: `dept_id IN (...) AND salary IN (...)` would accept an HR employee whose salary equals the top salary of some other department.
- Supported in PostgreSQL, MySQL, Oracle and SQLite. SQL Server does **not** support it; use `EXISTS` or a join to the grouped query instead (not run here).
**Example:** 'Who is the highest paid in each department?' Chitra and Dev both earn 70,000 in department 2, so both show up (a tie).
**Sample data:**
`employees`

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 70000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farid | 3 | 80000 |
| 7 | Gita | 3 | 80000 |
| 8 | Hari | 4 | 65000 |
**SQL:**
```sql
SELECT name, dept_id, salary
FROM employees
WHERE (dept_id, salary) IN (SELECT dept_id, MAX(salary) FROM employees GROUP BY dept_id)
ORDER BY dept_id, name
```
**Output:**

| name | dept_id | salary |
|---|---|---|
| Bala | 1 | 60000 |
| Chitra | 2 | 70000 |
| Dev | 2 | 70000 |
| Esha | 3 | 90000 |
| Hari | 4 | 65000 |
**pandas equivalent:**
```python
top = employees.groupby('dept_id', as_index=False).agg(salary=('salary','max'))
result = employees.merge(top, on=['dept_id','salary'])[['name','dept_id','salary']].sort_values(['dept_id','name'])
```
(result checked identical to the SQL output)
**SQL Server alternative (not run here):**
```sql
SELECT e.name, e.dept_id, e.salary
FROM employees e
JOIN (SELECT dept_id, MAX(salary) AS mx FROM employees GROUP BY dept_id) t
  ON t.dept_id = e.dept_id AND t.mx = e.salary;
```
**Edge cases:** Ties all appear (department 2). NULL in any column of the pair makes the comparison unknown, so that row never matches. Column order inside the brackets must be the same on both sides.
**Likely follow-ups:**
- Window-function way? `RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) = 1` (Part 5).
- Why not two separate IN conditions? They check columns independently and give wrong rows.
**Common mistakes:** Using two separate `IN` conditions; swapping the column order on one side; using the syntax on SQL Server.

### Q42 ⭐ 🟡 Find the top 3 products by sales per category without window functions (correlated subquery).
**Asked at:** commonly asked (no company-specific report found) (a classic 'top N per group' task; the window-function version is the one most interviewers expect today)
**What the interviewer is checking:** Whether you can solve top-N-per-group by counting how many rows beat the current row.
**Say this in the interview:** For each product I count how many products in the same category have higher sales. If fewer than 3 do, it is in the top 3. It is a correlated subquery, meaning the inner query uses a value from the current outer row.
**Explain simply:**
- **Correlated subquery** = an inner query that refers to the outer row (`p.category`, `p.sales`), so it re-runs for every outer row.
- 'Fewer than 3 products have more sales' is the same as 'this product is rank 1, 2 or 3'.
- Ties: Tablet and Watch both have 300, each has only 2 products above it, so both qualify and Electronics returns 4 rows. That is the same behaviour as `RANK()`, not `ROW_NUMBER()`.
- Window version: `RANK() OVER (PARTITION BY category ORDER BY sales DESC) <= 3` inside a CTE (Part 5). It is faster and clearer on big tables.
**Example:** Top 3 products in each category on a catalogue. For Grocery (only 3 products) all 3 appear.
**Sample data:**
`product_sales`

| product | category | sales |
|---|---|---|
| Phone | Electronics | 500 |
| Laptop | Electronics | 400 |
| Tablet | Electronics | 300 |
| Watch | Electronics | 300 |
| Cable | Electronics | 50 |
| Rice | Grocery | 200 |
| Oil | Grocery | 150 |
| Tea | Grocery | 100 |
**SQL:**
```sql
SELECT p.category, p.product, p.sales
FROM product_sales p
WHERE (SELECT COUNT(*) FROM product_sales x
       WHERE x.category = p.category AND x.sales > p.sales) < 3
ORDER BY p.category, p.sales DESC, p.product
```
**Output:**

| category | product | sales |
|---|---|---|
| Electronics | Phone | 500 |
| Electronics | Laptop | 400 |
| Electronics | Tablet | 300 |
| Electronics | Watch | 300 |
| Grocery | Rice | 200 |
| Grocery | Oil | 150 |
| Grocery | Tea | 100 |
**pandas equivalent:**
```python
ps = product_sales.copy()
ps['rnk'] = ps.groupby('category').sales.rank(method='min', ascending=False)
result = ps[ps.rnk <= 3][['category','product','sales']].sort_values(['category','sales','product'], ascending=[True,False,True])
```
(result checked identical to the SQL output)
**Edge cases:** Ties can return more than 3 rows. For exactly 3 rows add a tie-breaker, e.g. count rows with `x.sales > p.sales OR (x.sales = p.sales AND x.product < p.product)`. Categories with fewer than 3 products return all of them. NULL sales are never counted as higher.
**Likely follow-ups:**
- Why is it slow on large data? The inner query runs once per outer row (roughly n squared work); an index on (category, sales) helps.
- How to get strictly 3 rows? Use `ROW_NUMBER()`.
**Common mistakes:** Using `<= 3` instead of `< 3` (gives top 4); forgetting the category condition inside the subquery (gives overall top 3, not per category).

### Q43 ⭐ 🟡 Use EXISTS to check whether at least one matching record exists; why is SELECT 1 inside EXISTS fine?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you understand EXISTS only asks 'is there at least one row?' and does not care what columns come back.
**Say this in the interview:** EXISTS returns true as soon as the inner query finds one row. It never uses the selected columns, so SELECT 1, SELECT * or SELECT NULL all behave the same. I write SELECT 1 by habit to show I only care about existence.
**Explain simply:**
- **EXISTS** = a yes/no test on a subquery: true if it returns at least one row, false if it returns none.
- The database stops at the first match, so it does not need to read all matching rows.
- Unlike a join, it never duplicates the outer row: Asha has two leave records but appears once.
- I checked here that `SELECT *` gives exactly the same output as `SELECT 1`.
**Example:** Which employees have taken at least one leave? Asha (2 records), Chitra (1) and Esha (2) qualify; others do not.
**Sample data:**
`employees`

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 70000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farid | 3 | 80000 |
| 7 | Gita | 3 | 80000 |
| 8 | Hari | 4 | 65000 |

`leaves`

| leave_id | emp_id | days |
|---|---|---|
| 1 | 1 | 2 |
| 2 | 1 | 3 |
| 3 | 3 | 1 |
| 4 | 5 | 4 |
| 5 | 5 | 1 |
**SQL:**
```sql
SELECT e.emp_id, e.name
FROM employees e
WHERE EXISTS (SELECT 1 FROM leaves l WHERE l.emp_id = e.emp_id)
ORDER BY e.emp_id
```
**Output:**

| emp_id | name |
|---|---|
| 1 | Asha |
| 3 | Chitra |
| 5 | Esha |
**pandas equivalent:**
```python
result = employees[employees.emp_id.isin(leaves.emp_id)][['emp_id','name']].sort_values('emp_id')
```
(result checked identical to the SQL output)
**Edge cases:** NULLs inside the inner query do not matter (EXISTS counts rows, not values). If the inner query returns no rows, EXISTS is false; `NOT EXISTS` is the safe anti-join (unlike `NOT IN`, which breaks on NULLs).
**Likely follow-ups:**
- EXISTS vs JOIN? A join repeats outer rows per match; EXISTS does not.
- EXISTS vs IN? Same answer on clean data; NOT EXISTS is safer than NOT IN when NULLs are possible.
**Common mistakes:** Believing `SELECT *` inside EXISTS is slow (modern optimizers ignore the column list); forgetting the correlation condition (`l.emp_id = e.emp_id`), which makes EXISTS true for everyone whenever the leaves table is not empty.

### Q44 ⭐ 🟡 Find the median salary using subqueries or a CTE.
**Asked at:** commonly asked (one candidate-reported Meesho BA intern review mentions a median question, seen as a snippet only); otherwise no company-specific report found
**What the interviewer is checking:** Whether you know the median is the middle value, and how to handle an even number of rows.
**Say this in the interview:** I sort the salaries, number them, and pick the middle row. If the count is odd there is one middle row, if even there are two and I average them. The trick `rn IN ((cnt+1)/2, (cnt+2)/2)` picks one or two rows automatically.
**Explain simply:**
- **Median** = the middle value when sorted. It ignores extreme values, so HR prefers it to the average for pay reports.
- Here 8 salaries sorted: 50k, 60k, 65k, 70k, 70k, 80k, 80k, 90k. Middle rows are 4 and 5, both 70,000, so the median is 70,000 (the average is 70,625).
- Integer division: for cnt = 8, (8+1)/2 = 4 and (8+2)/2 = 5. For cnt = 7, both give 4 (one row).
- PostgreSQL / Oracle have it built in: `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary)`. SQL Server: `PERCENTILE_CONT(0.5) WITHIN GROUP (...) OVER ()`. MySQL has no built-in (not run here).
**Example:** Median pay of the company vs mean: one CEO at 10 lakh/month pulls the average up but not the median.
**Sample data:**
`employees`

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 70000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farid | 3 | 80000 |
| 7 | Gita | 3 | 80000 |
| 8 | Hari | 4 | 65000 |
**SQL:**
*CTE + window function*
```sql
WITH ordered AS (
  SELECT salary,
         ROW_NUMBER() OVER (ORDER BY salary) AS rn,
         COUNT(*) OVER ()                    AS cnt
  FROM employees)
SELECT AVG(salary) AS median_salary
FROM ordered
WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
```
**Output:**

| median_salary |
|---|
| 70000 |
**pandas equivalent:**
```python
result = pd.DataFrame({'median_salary': [employees.salary.median()]})
```
(result checked identical to the SQL output)
**Without window functions (subqueries only, `LIMIT ... OFFSET` style; checked identical in SQLite. PostgreSQL accepts subqueries in LIMIT/OFFSET (from memory, not run here); MySQL does not, so use the window version or a user variable there):**
```sql
SELECT AVG(salary) AS median_salary
FROM (SELECT salary FROM employees ORDER BY salary
      LIMIT 2 - (SELECT COUNT(*) FROM employees) % 2
      OFFSET (SELECT (COUNT(*) - 1) / 2 FROM employees))
```
**Edge cases:** NULL salaries: `COUNT(*)` counts them but `ORDER BY` puts them first in SQLite/MySQL, which breaks the middle position; filter `WHERE salary IS NOT NULL` first. Empty table returns NULL. Duplicate values are fine (they take separate row numbers).
**Likely follow-ups:**
- Median per department? Add `PARTITION BY dept_id` to both window functions and group by dept.
- Mean vs median? Use the median when a few very high salaries distort the average.
**Common mistakes:** Using `AVG` and calling it median; ignoring even counts; picking `cnt/2` only (wrong for even and odd); forgetting to remove NULLs.

### Q45 ⭐ 🟡 When should you prefer a temp table over a CTE (reusing a result many times, adding an index)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know when a CTE is not enough: reuse, size, and indexing.
**Say this in the interview:** A CTE lives for one query. If I need the same intermediate result across several queries, or it is big and I want to index it, I save it in a temp table. A temp table is a real table that disappears when my session ends.
**Explain simply:**
- **Temp table** = a table stored in the database's temporary space, visible only to your session, dropped automatically at the end. You can index it and collect statistics on it.
- Prefer it when: (1) the result is used by many later statements (a CTE would be recomputed or is gone after one query); (2) the intermediate result is large and later joins need an index; (3) the CTE's plan is poor and you want to force a stable result; (4) you want to inspect the middle step while debugging.
- Stay with a CTE when the logic is used once and the data is small: it is shorter and leaves nothing to clean up.
- Syntax differs: `CREATE TEMP TABLE` (PostgreSQL, SQLite), `CREATE TEMPORARY TABLE` (MySQL), `SELECT ... INTO #name` (SQL Server, the `#` makes it temporary). Not run here except SQLite.
**Example:** Monthly attrition pack: calculate 'average salary per department' once into a temp table, then reuse it for five different reports in the same session.
**Sample data:**
`employees`

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 70000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farid | 3 | 80000 |
| 7 | Gita | 3 | 80000 |
| 8 | Hari | 4 | 65000 |
**SQL:**
*after `CREATE TEMP TABLE tmp_dept_avg AS SELECT dept_id, AVG(salary) AS avg_sal FROM employees GROUP BY dept_id;` and `CREATE INDEX idx_tmp_dept ON tmp_dept_avg(dept_id);`*
```sql
SELECT e.name, e.salary, ROUND(t.avg_sal) AS dept_avg
FROM employees e JOIN tmp_dept_avg t ON t.dept_id = e.dept_id
WHERE e.salary >= t.avg_sal
ORDER BY e.name
```
**Output:**

| name | salary | dept_avg |
|---|---|---|
| Bala | 60000 | 55000 |
| Chitra | 70000 | 70000 |
| Dev | 70000 | 70000 |
| Esha | 90000 | 83333 |
| Hari | 65000 | 65000 |
**pandas equivalent:**
```python
g = employees.groupby('dept_id', as_index=False).agg(avg_sal=('salary','mean'))
m = employees.merge(g, on='dept_id')
m = m[m.salary >= m.avg_sal].assign(dept_avg=lambda x: x.avg_sal.round())
result = m[['name','salary','dept_avg']].sort_values('name')
```
(result checked identical to the SQL output)
**Edge cases:** Temp tables vanish when the session closes (and with connection pooling, 'your session' may change between calls). Name clashes: two users can both have `#orders` in SQL Server. Remember to drop in long sessions. Writes cost disk/log I/O, so for tiny data a CTE is faster.
**Likely follow-ups:**
- Is a temp table faster than a CTE? Not automatically. It wins on reuse and indexing, loses on small one-off queries.
- Temp table vs view? A view stores no data, only the query; a temp table stores the rows.
**Common mistakes:** Creating temp tables for everything; forgetting to clean up; assuming it persists to the next login or across pooled connections.

### Q46 ⭐ 🟡 Why can a derived table in FROM not reference other tables in the same FROM clause, and how does LATERAL change that?
**Asked at:** commonly asked (no company-specific report found) (PostgreSQL/product-company flavour)
**What the interviewer is checking:** Understanding of how a FROM clause is evaluated and what LATERAL / APPLY add.
**Say this in the interview:** Normally the items in FROM are built independently, so a derived table cannot see the other tables next to it. LATERAL lets the subquery look left and use the current row of an earlier table, like a correlated subquery but in FROM, and it can return many rows and columns.
**Explain simply:**
- **Derived table** = a subquery in FROM. By default it is evaluated on its own, as if each FROM item were a separate box. So `e.dept_id = d.dept_id` inside it fails: SQLite replied `no such column: d.dept_id`.
- **LATERAL** (PostgreSQL 9.3+, MySQL 8.0.14+, Oracle 12c+, DuckDB; version numbers from memory) removes that limit: the subquery runs once per row of the table to its left. SQL Server spells it `CROSS APPLY` / `OUTER APPLY`.
- Typical use: 'top N rows per group' (here the top 2 earners per department) without window functions.
- `LEFT JOIN LATERAL ... ON true` keeps departments with no match (Legal shows NULL), like `OUTER APPLY`.
**Example:** For every department, list its two best-paid employees. Legal has no employees and still shows up.
**Sample data:**
`departments`

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Sales |
| 3 | IT |
| 4 | Finance |
| 5 | Legal |

`employees`

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 70000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farid | 3 | 80000 |
| 7 | Gita | 3 | 80000 |
| 8 | Hari | 4 | 65000 |
**SQL:**
(PostgreSQL / DuckDB-style syntax; not run here, because SQLite has no LATERAL and DuckDB is not installed. The output below is worked out by hand and matches the pandas version, which was run.)
```sql
SELECT d.dept_name, t.name, t.salary
FROM departments d
LEFT JOIN LATERAL (
    SELECT e.name, e.salary
    FROM employees e
    WHERE e.dept_id = d.dept_id
    ORDER BY e.salary DESC, e.name
    LIMIT 2) t ON true
ORDER BY d.dept_id, t.salary DESC, t.name
```
**Output:**

| dept_name | name | salary |
|---|---|---|
| HR | Bala | 60000 |
| HR | Asha | 50000 |
| Sales | Chitra | 70000 |
| Sales | Dev | 70000 |
| IT | Esha | 90000 |
| IT | Farid | 80000 |
| Finance | Hari | 65000 |
| Legal | NULL | NULL |
**pandas equivalent:**
```python
top2 = (employees.sort_values(['salary','name'], ascending=[False,True])
        .groupby('dept_id').head(2))
m = departments.merge(top2, on='dept_id', how='left')
result = m.sort_values(['dept_id','salary','name'], ascending=[True,False,True], na_position='last')[['dept_name','name','salary']]
```
(result checked identical to the SQL output)
**SQL Server version (not run here):** `FROM departments d OUTER APPLY (SELECT TOP 2 e.name, e.salary FROM employees e WHERE e.dept_id = d.dept_id ORDER BY e.salary DESC, e.name) t`.
**Edge cases:** `INNER JOIN LATERAL` / `CROSS APPLY` drops departments with no match. Without ORDER BY inside, 'top 2' is arbitrary. SQLite and old MySQL (before 8.0.14) have no LATERAL.
**Likely follow-ups:**
- LATERAL vs window functions? Windows scan the table once; LATERAL runs per row but can use an index and stop early with LIMIT.
- Is it a correlated subquery? Yes, but placed in FROM, so it can return several columns and rows.
**Common mistakes:** Expecting a normal derived table to see sibling tables; forgetting `ON true` on `LEFT JOIN LATERAL`; using LATERAL on MySQL 5.7.

### Q47 ⭐ 🟡 Use a CTE to flag duplicate customer records before removing them (short version; full de-duplication is Part 10).
**Asked at:** commonly asked (no company-specific report found) (data-cleaning is common in HR/MIS analyst rounds)
**What the interviewer is checking:** Whether you can mark duplicates safely before deleting anything.
**Say this in the interview:** I clean the key (lower case, trimmed), number rows inside each group of the same email with ROW_NUMBER, and flag everything after number 1 as a duplicate. I look at the flags first, and only then delete.
**Explain simply:**
- **Duplicate** here = the same person entered twice, e.g. 'asha@x.com' and 'ASHA@x.com ' (capital letters and a trailing space).
- **ROW_NUMBER() OVER (PARTITION BY key ORDER BY id)** = numbers rows 1, 2, 3 inside each group; row 1 is the one we keep (the oldest ID).
- The CTE gives the numbering a name so the final SELECT can use `rn` (you cannot use a window function directly in WHERE).
- Flag first, delete later: this lets HR review what will go.
**Example:** Customer 1, 2 and 5 are all asha@x.com, customers 4 and 6 are c@x.com. 3 rows get 'duplicate', 3 rows 'keep'.
**Sample data:**
`customers_raw`

| customer_id | name | email |
|---|---|---|
| 1 | Asha | asha@x.com |
| 2 | Asha K | ASHA@x.com  |
| 3 | Bala | bala@x.com |
| 4 | Chitra | c@x.com |
| 5 | Asha Kumar | asha@x.com |
| 6 | Chitra S | c@x.com |
**SQL:**
```sql
WITH flagged AS (
  SELECT customer_id, name, LOWER(TRIM(email)) AS email_clean,
         ROW_NUMBER() OVER (PARTITION BY LOWER(TRIM(email)) ORDER BY customer_id) AS rn
  FROM customers_raw)
SELECT customer_id, name, email_clean,
       CASE WHEN rn = 1 THEN 'keep' ELSE 'duplicate' END AS status
FROM flagged
ORDER BY customer_id
```
**Output:**

| customer_id | name | email_clean | status |
|---|---|---|---|
| 1 | Asha | asha@x.com | keep |
| 2 | Asha K | asha@x.com | duplicate |
| 3 | Bala | bala@x.com | keep |
| 4 | Chitra | c@x.com | keep |
| 5 | Asha Kumar | asha@x.com | duplicate |
| 6 | Chitra S | c@x.com | duplicate |
**pandas equivalent:**
```python
c = customers_raw.copy()
c['email_clean'] = c.email.str.strip().str.lower()
c['rn'] = c.sort_values('customer_id').groupby('email_clean').cumcount() + 1
c['status'] = c.rn.map(lambda r: 'keep' if r == 1 else 'duplicate')
result = c[['customer_id','name','email_clean','status']].sort_values('customer_id')
```
(result checked identical to the SQL output)
**Edge cases:** NULL emails form one group in PARTITION BY, so every NULL-email row after the first is flagged: usually wrong, so exclude or handle NULLs. Fully identical rows need a tie-breaker in ORDER BY. Choosing 'keep newest' means `ORDER BY customer_id DESC`.
**Likely follow-ups:**
- How to delete them? Delete rows where `rn > 1` (Part 10). In SQL Server you can delete straight through the CTE.
- Why not DISTINCT? DISTINCT hides duplicates in the result; it does not tell you which row to keep.
**Common mistakes:** Not cleaning case and spaces before comparing; deleting without reviewing; ordering inconsistently so a different row is kept each run.

### Q48 ⭐ 🟡 Find users who ordered in January but not in February using CTEs.
**Asked at:** commonly asked (no company-specific report found) (a retention / churn pattern; HR version: 'employees present in January but absent in February')
**What the interviewer is checking:** Anti-join thinking with CTEs: build two clean sets, then subtract.
**Say this in the interview:** I make one CTE for the January buyers and one for February buyers, each with distinct users. Then I keep January users who have no match in February using NOT EXISTS.
**Explain simply:**
- **CTE** = a named temporary result written with `WITH`. Two CTEs are separated by a comma.
- **Anti-join** = 'rows in A with no match in B'. Written with NOT EXISTS, LEFT JOIN ... IS NULL, or NOT IN.
- Date range uses `>= first day` and `< first day of next month`, which is safe for dates with times and can use an index.
- Standard SQL also has `EXCEPT` (`SELECT user_id FROM jan EXCEPT SELECT user_id FROM feb`); Oracle calls it `MINUS`.
**Example:** u2 bought twice in January and never in February, u4 bought only in January: both are the answer. u1 and u5 bought in both months, u3 only in February.
**Sample data:**
`orders`

| order_id | user_id | order_date |
|---|---|---|
| 1 | u1 | 2025-01-05 |
| 2 | u1 | 2025-02-10 |
| 3 | u2 | 2025-01-12 |
| 4 | u2 | 2025-01-28 |
| 5 | u3 | 2025-02-03 |
| 6 | u4 | 2025-01-20 |
| 7 | u5 | 2025-01-30 |
| 8 | u5 | 2025-02-27 |
**SQL:**
```sql
WITH jan AS (
  SELECT DISTINCT user_id FROM orders
  WHERE order_date >= '2025-01-01' AND order_date < '2025-02-01'),
feb AS (
  SELECT DISTINCT user_id FROM orders
  WHERE order_date >= '2025-02-01' AND order_date < '2025-03-01')
SELECT j.user_id
FROM jan j
WHERE NOT EXISTS (SELECT 1 FROM feb f WHERE f.user_id = j.user_id)
ORDER BY j.user_id
```
**Output:**

| user_id |
|---|
| u2 |
| u4 |
**pandas equivalent:**
```python
o = orders
jan = set(o[(o.order_date >= '2025-01-01') & (o.order_date < '2025-02-01')].user_id)
feb = set(o[(o.order_date >= '2025-02-01') & (o.order_date < '2025-03-01')].user_id)
result = pd.DataFrame({'user_id': sorted(jan - feb)})
```
(result checked identical to the SQL output)
**Edge cases:** If `feb` contains a NULL user_id, `NOT IN` returns nothing at all; NOT EXISTS is immune. Use DISTINCT to avoid repeating a user who ordered twice. A user with orders in Dec and Feb but none in Jan is not included.
**Likely follow-ups:**
- Which users are new in February? Swap the two CTEs.
- Same with LEFT JOIN? `FROM jan LEFT JOIN feb ON feb.user_id = jan.user_id WHERE feb.user_id IS NULL` (the `USING` shortcut does not exist in SQL Server).
**Common mistakes:** Using `NOT IN` on a column that can be NULL; filtering months with `LIKE '2025-01%'` or functions on the column (slow, breaks on date types); forgetting that a 'user' may appear many times.

### Q49 ⭐ 🔴 Find customers who bought every product in a given category (relational division with NOT EXISTS).
**Asked at:** commonly asked (no company-specific report found) (relational division is a differentiator question)
**What the interviewer is checking:** Can you turn 'for all' into 'there is no X for which ... not'? A double negative.
**Say this in the interview:** 'Bought every Electronics product' means there is no Electronics product that the customer did not buy. So I write NOT EXISTS around a NOT EXISTS: for each customer, look for an Electronics product with no purchase row; if none is found, the customer qualifies.
**Explain simply:**
- **Relational division** = finding rows that are related to **all** items in another set (all products, all courses, all training modules).
- Read the query from the inside: innermost = 'this customer bought this product'; middle = 'a category product that customer did not buy'; outer = 'customers with no such missing product'.
- Counting alternative (also run, identical result): count the customer's distinct Electronics products and compare with the total Electronics products. Easier to read; needs DISTINCT.
**Example:** Electronics has 3 products (Phone, Laptop, Tablet). Asha bought all 3, Chitra bought all 3 plus Rice, Bala only 2, Dev bought Tablet twice. Result: Asha and Chitra.
**Sample data:**
`products`

| product_id | product_name | category |
|---|---|---|
| 1 | Phone | Electronics |
| 2 | Laptop | Electronics |
| 3 | Tablet | Electronics |
| 4 | Rice | Grocery |

`customers`

| customer_id | name |
|---|---|
| 1 | Asha |
| 2 | Bala |
| 3 | Chitra |
| 4 | Dev |
| 5 | Esha |

`purchases`

| customer_id | product_id |
|---|---|
| 1 | 1 |
| 1 | 2 |
| 1 | 3 |
| 2 | 1 |
| 2 | 2 |
| 3 | 1 |
| 3 | 2 |
| 3 | 3 |
| 3 | 4 |
| 4 | 3 |
| 4 | 3 |
**SQL:**
*double NOT EXISTS*
```sql
SELECT c.customer_id, c.name
FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM products p
    WHERE p.category = 'Electronics'
      AND NOT EXISTS (
          SELECT 1 FROM purchases b
          WHERE b.customer_id = c.customer_id AND b.product_id = p.product_id))
ORDER BY c.customer_id
```
**Output:**

| customer_id | name |
|---|---|
| 1 | Asha |
| 3 | Chitra |
**pandas equivalent:**
```python
need = set(products.loc[products.category == 'Electronics', 'product_id'])
bought = purchases.groupby('customer_id').product_id.apply(set)
ok = [cid for cid in customers.customer_id if need <= bought.get(cid, set())]
result = customers[customers.customer_id.isin(ok)][['customer_id','name']].sort_values('customer_id')
```
(result checked identical to the SQL output)
**Counting version (checked: same output):**
```sql
SELECT c.customer_id, c.name
FROM customers c
JOIN purchases b ON b.customer_id = c.customer_id
JOIN products p  ON p.product_id = b.product_id AND p.category = 'Electronics'
GROUP BY c.customer_id, c.name
HAVING COUNT(DISTINCT p.product_id) = (SELECT COUNT(*) FROM products WHERE category = 'Electronics')
ORDER BY c.customer_id
```
**Edge cases:** Dev's duplicate purchase would give a count of 2 without DISTINCT. A customer with no purchases (Esha) is excluded by the counting version, but if the category had zero products NOT EXISTS would return **every** customer (vacuously true). A category with a NULL product_id behaves oddly: clean it first.
**Likely follow-ups:**
- Which is faster? Usually similar; counting is easier to read, NOT EXISTS stops early and needs no DISTINCT.
- Employees who completed all mandatory trainings? Same pattern with employees, trainings, completions.
**Common mistakes:** Forgetting DISTINCT in the count version; filtering the category in the wrong place (it must be in the middle query); using `IN` and getting 'bought any', not 'bought all'.

### Q50 ⭐ 🔴 Refactor a query with three levels of nested subqueries into readable CTEs and explain your naming.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Readability and structure: can you break a nested query into named steps a colleague can follow?
**Say this in the interview:** I read the nested query from the inside out, turn each layer into a CTE with a name that says what it contains, and then the final SELECT reads top to bottom like a story. The result does not change, I checked both versions return the same rows.
**Explain simply:**
- **Nested subquery** = a query inside a query inside a query. Three levels is already hard to debug.
- Naming rule: name each CTE for the **business meaning of its rows**, not the technique: `dept_avg`, `benchmark`, `high_paying_depts` rather than `t1`, `t2`, `x`. Use the same style (snake_case) throughout.
- Each CTE does one job, so you can run it alone (`SELECT * FROM dept_avg`) to debug.
- Question: employees in departments whose average salary is above the average of all department averages (68,333): Sales and IT.
**Example:** Before: three layers of brackets with aliases t and u. After: three short named steps and a final join.
**Sample data:**
`employees`

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 70000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farid | 3 | 80000 |
| 7 | Gita | 3 | 80000 |
| 8 | Hari | 4 | 65000 |
**SQL:**
*refactored CTE version*
```sql
WITH dept_avg AS (                   -- 1. average salary of each department
  SELECT dept_id, AVG(salary) AS avg_sal
  FROM employees GROUP BY dept_id),
benchmark AS (                      -- 2. the average of those averages
  SELECT AVG(avg_sal) AS bench FROM dept_avg),
high_paying_depts AS (              -- 3. departments above the benchmark
  SELECT d.dept_id FROM dept_avg d CROSS JOIN benchmark b
  WHERE d.avg_sal > b.bench)
SELECT e.name, e.salary
FROM employees e
JOIN high_paying_depts h ON h.dept_id = e.dept_id
ORDER BY e.name
```
**Output:**

| name | salary |
|---|---|
| Chitra | 70000 |
| Dev | 70000 |
| Esha | 90000 |
| Farid | 80000 |
| Gita | 80000 |
**pandas equivalent:**
```python
da = employees.groupby('dept_id', as_index=False).agg(avg_sal=('salary','mean'))
bench = da.avg_sal.mean()
hi = da[da.avg_sal > bench].dept_id
result = employees[employees.dept_id.isin(hi)][['name','salary']].sort_values('name')
```
(result checked identical to the SQL output)
**Original nested version (checked: same rows):**
```sql
SELECT name, salary FROM employees
WHERE dept_id IN (
  SELECT dept_id FROM (
    SELECT dept_id, AVG(salary) AS avg_sal FROM employees GROUP BY dept_id) t
  WHERE avg_sal > (
    SELECT AVG(avg_sal) FROM (
      SELECT AVG(salary) AS avg_sal FROM employees GROUP BY dept_id) u))
ORDER BY name
```
**Edge cases:** Average of averages is not the company average when departments differ in size (here 68,333 vs 70,625): say which one the business wants. Departments with no employees do not appear in `dept_avg`.
**Likely follow-ups:**
- Will the CTE version be faster? Usually same plan; the gain is readability.
- When keep it nested? A short one-level subquery in WHERE is often clearer than a CTE.
**Common mistakes:** Meaningless names (cte1, cte2); stacking one CTE per tiny step; changing logic while refactoring without comparing results; mixing aggregate levels by accident.

### Q51 ⭐ 🔴 Using CTEs, find employees who earned more than their department average in two consecutive years.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Chaining CTEs: first compute a benchmark, then flag rows, then find consecutive years with a self-join.
**Say this in the interview:** CTE 1 is the department average per year. CTE 2 keeps the employee-years where pay is strictly above that average. Then I join CTE 2 to itself on the same employee and year + 1: any match means two years in a row.
**Explain simply:**
- **Self-join** = joining a table (here a CTE) to itself with two aliases, a1 for year Y and a2 for year Y+1.
- Joining on `year + 1` is safer than the LAG function when some years are missing, because LAG would pair the 2022 row with the 2024 row if 2023 is absent.
- Strictly above: Chitra earns exactly the department average in 2022 and 2023, so those years do not count.
- DISTINCT stops an employee who is above average three years in a row from showing twice.
**Example:** Asha is above her department's average in 2023 and 2024; Esha in 2022 and 2023. Bala is above only in 2022 (HR average 55,000; he earns 60,000), then below in 2023 and 2024, so no chain.
**Sample data:**
`pay`

| emp_id | name | dept_id | year | salary |
|---|---|---|---|---|
| 1 | Asha | 1 | 2022 | 50000 |
| 1 | Asha | 1 | 2023 | 55000 |
| 1 | Asha | 1 | 2024 | 70000 |
| 2 | Bala | 1 | 2022 | 60000 |
| 2 | Bala | 1 | 2023 | 52000 |
| 2 | Bala | 1 | 2024 | 61000 |
| 3 | Chitra | 2 | 2022 | 70000 |
| 3 | Chitra | 2 | 2023 | 72000 |
| 3 | Chitra | 2 | 2024 | 74000 |
| 4 | Dev | 2 | 2022 | 60000 |
| 4 | Dev | 2 | 2023 | 62000 |
| 4 | Dev | 2 | 2024 | 64000 |
| 5 | Esha | 2 | 2022 | 80000 |
| 5 | Esha | 2 | 2023 | 82000 |
| 5 | Esha | 2 | 2024 | 60000 |
**SQL:**
```sql
WITH dept_year_avg AS (
  SELECT dept_id, year, AVG(salary) AS avg_sal FROM pay GROUP BY dept_id, year),
above AS (
  SELECT p.emp_id, p.name, p.year
  FROM pay p JOIN dept_year_avg a ON a.dept_id = p.dept_id AND a.year = p.year
  WHERE p.salary > a.avg_sal)
SELECT DISTINCT a1.emp_id, a1.name
FROM above a1
JOIN above a2 ON a2.emp_id = a1.emp_id AND a2.year = a1.year + 1
ORDER BY a1.emp_id
```
**Output:**

| emp_id | name |
|---|---|
| 1 | Asha |
| 5 | Esha |
**pandas equivalent:**
```python
a = pay.groupby(['dept_id','year']).salary.transform('mean')
above = pay[pay.salary > a][['emp_id','name','year']]
nxt = above.assign(year=above.year - 1)
m = above.merge(nxt, on=['emp_id','name','year'])
result = m[['emp_id','name']].drop_duplicates().sort_values('emp_id')
```
(result checked identical to the SQL output)
**Edge cases:** Ties with the average are not above. Missing years break the chain (as they should). Departments with a single employee are never above their own average. NULL salaries are ignored by AVG and fail the comparison.
**Likely follow-ups:**
- Three consecutive years? Join a third copy (year + 2) or use the 'islands' trick with `year - ROW_NUMBER()`.
- LAG alternative? Flag per row, then `LAG(flag) OVER (PARTITION BY emp_id ORDER BY year)`; needs complete years.
**Common mistakes:** Comparing with the company average instead of the department average; using >= when the question says 'more than'; forgetting `year` in the join to the department-average CTE.

### Q52 ⭐ 🔴 What is a recursive CTE in one line, and when might an analyst need one? (basics only; details in Part 10)
**Asked at:** commonly asked (no company-specific report found) (full detail in Part 10)
**What the interviewer is checking:** That you know what recursion is for in SQL, without being asked for a deep build.
**Say this in the interview:** A recursive CTE is a CTE that refers to itself: it starts with a first set of rows and keeps adding rows that connect to the previous ones until nothing new appears. I would use it for an org chart: everyone reporting, directly or indirectly, to a manager.
**Explain simply:**
- **Recursive CTE** = `WITH RECURSIVE name AS (starting rows UNION ALL rows built from name itself)`.
- **Anchor** (first SELECT) gives the start, the **recursive part** (second SELECT) joins the CTE to the table to take one more step. It stops when the second part returns no rows.
- Analyst uses: reporting lines and team size under a manager, product category trees, date or number series, bill of materials.
- Dialects: PostgreSQL, MySQL 8, SQLite need `RECURSIVE`; SQL Server and Oracle write plain `WITH` (not run here).
**Example:** Meera (CEO) has Raj and Sita; Raj has Tom; Tom has Uma. Output shows each person's level in the hierarchy.
**Sample data:**
`org`

| emp_id | name | manager_id |
|---|---|---|
| 1 | Meera | NULL |
| 2 | Raj | 1 |
| 3 | Sita | 1 |
| 4 | Tom | 2 |
| 5 | Uma | 4 |
**SQL:**
```sql
WITH RECURSIVE chain(emp_id, name, level) AS (
  SELECT emp_id, name, 0 FROM org WHERE manager_id IS NULL      -- start: the top boss
  UNION ALL
  SELECT o.emp_id, o.name, c.level + 1                            -- repeat: people reporting to the last level
  FROM org o JOIN chain c ON o.manager_id = c.emp_id)
SELECT emp_id, name, level FROM chain ORDER BY level, emp_id
```
**Output:**

| emp_id | name | level |
|---|---|---|
| 1 | Meera | 0 |
| 2 | Raj | 1 |
| 3 | Sita | 1 |
| 4 | Tom | 2 |
| 5 | Uma | 3 |
**pandas equivalent:**
```python
rows = [(1, 'Meera', 0)]
frontier, lvl = [1], 0
while frontier:
    lvl += 1
    nxt = org[org.manager_id.isin(frontier)]
    rows += [(r.emp_id, r.name, lvl) for r in nxt.itertuples()]
    frontier = list(nxt.emp_id)
result = pd.DataFrame(rows, columns=['emp_id','name','level']).sort_values(['level','emp_id'])
```
(result checked identical to the SQL output)
**Edge cases:** A loop in the data (A reports to B, B reports to A) runs forever; add a level limit (`WHERE level < 10`) or, in PostgreSQL, the `CYCLE` clause. Employees whose manager is missing from the table never appear. `UNION` (not ALL) removes repeated rows but is slower.
**Likely follow-ups:**
- How to count team size under Raj? Start the anchor at Raj and `COUNT(*) - 1`.
- Is there a row limit? Yes, SQL Server's default is `MAXRECURSION 100`.
**Common mistakes:** Forgetting the termination condition; forgetting `RECURSIVE` in PostgreSQL/MySQL; putting the anchor and recursive parts in the wrong order.

### Q53 ⭐ 🔴 How would you compare the performance of a subquery version and a CTE version of the same query using EXPLAIN?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you measure instead of guess? Do you know the optimizer often treats both forms the same?
**Say this in the interview:** I run EXPLAIN on both versions and compare the plans, then EXPLAIN ANALYZE for the real time and row counts, running each several times on the same data. Often the plans are identical, because the database merges the CTE into the query, so I choose on readability.
**Explain simply:**
- **EXPLAIN** = asks the database to show its plan (how it will read tables, join, sort) without running it. **EXPLAIN ANALYZE** actually runs it and shows real time and rows.
- What to compare: scans of the same table (once or twice?), the join type, row estimates vs actual rows, any temp/materialize step, total time.
- Commands: PostgreSQL `EXPLAIN (ANALYZE, BUFFERS)`; MySQL 8 `EXPLAIN ANALYZE` (8.0.18+); SQL Server 'Include Actual Execution Plan' or `SET STATISTICS IO, TIME ON`; Oracle `EXPLAIN PLAN FOR` then `DBMS_XPLAN.DISPLAY`; SQLite `EXPLAIN QUERY PLAN` (the only one run here).
- Fair test: same data, warm cache, repeat 3 to 5 runs, ignore the first.
**Example:** 'Employees above the company average' as a subquery vs as a CTE. SQLite produced the plans below; both scan `employees` and compute the average once.
**Sample data:** same `employees` table as in Q40.
**SQL:**
*subquery version*
```sql
SELECT name, salary FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)
```
**Output:**

| name | salary |
|---|---|
| Esha | 90000 |
| Farid | 80000 |
| Gita | 80000 |
**pandas equivalent:**
```python
result = employees[employees.salary > employees.salary.mean()][['name','salary']]
```
(result checked identical to the SQL output)
**CTE version (checked: same rows):**
```sql
WITH avg_sal AS (SELECT AVG(salary) AS a FROM employees)
SELECT name, salary FROM employees, avg_sal WHERE salary > a
```

**SQLite plan, subquery version:**
```text
  SCAN employees
  SCALAR SUBQUERY 1
  SCAN employees
```
**SQLite plan, CTE version:**
```text
  CO-ROUTINE avg_sal
  SCAN employees
  SCAN avg_sal
  SCAN employees
```
**Edge cases:** Tiny tables prove nothing: the plan may change with volume and statistics. A correlated version will show a repeated subquery step. Plans differ between databases, so test on the production engine (PostgreSQL, SQL Server etc. not run here).
**Likely follow-ups:**
- The plans match; what then? Prefer the more readable one.
- Why not just time it? Cache and load add noise; plans show *why*, timing shows *how long*.
**Common mistakes:** Timing a single cold run; judging by query length; testing on 8 rows; confusing estimated and actual rows.

### Q54 ⭐ 🔴 Why can the same subquery give different results in a WHERE clause vs a HAVING clause?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand SQL's order: WHERE filters rows before grouping, HAVING filters groups after?
**Say this in the interview:** The subquery itself returns the same number in both places. What differs is what the outer clause compares it to: WHERE compares single rows before they are grouped, so rows are removed and the group numbers change; HAVING compares whole groups after the numbers are calculated.
**Explain simply:**
- **Premise check:** the subquery's own result does not change, the *clause around it* changes what is being filtered.
- Order of execution: FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY.
- WHERE: 'keep employees above the company average (80,000), then summarize'. Department A then has just 1 person (the 200,000 earner) with average 200,000.
- HAVING: 'summarize every department, keep those whose average is above 80,000'. Department A has all 3 people, average 90,000.
- A correlated subquery in HAVING can use group-level values; in WHERE it sees only the single row.
**Example:** Department A has salaries 30k, 40k, 200k; B has 60k, 70k, 80k; company average is 80k. One outlier makes A look 'high' at group level, but only one A person is above 80k at row level.
**Sample data:**
`staff`

| dept | salary |
|---|---|
| A | 30000 |
| A | 40000 |
| A | 200000 |
| B | 60000 |
| B | 70000 |
| B | 80000 |
**SQL:**
*WHERE version (row filter)*
```sql
SELECT dept, AVG(salary) AS avg_sal, COUNT(*) AS n
FROM staff
WHERE salary > (SELECT AVG(salary) FROM staff)
GROUP BY dept
ORDER BY dept
```
**Output:**

| dept | avg_sal | n |
|---|---|---|
| A | 200000 | 1 |
**pandas equivalent:**
```python
cut = staff.salary.mean()
result = (staff[staff.salary > cut].groupby('dept', as_index=False)
          .agg(avg_sal=('salary','mean'), n=('salary','size')))
```
(result checked identical to the SQL output)
**SQL (HAVING version (group filter)):**
```sql
SELECT dept, AVG(salary) AS avg_sal, COUNT(*) AS n
FROM staff
GROUP BY dept
HAVING AVG(salary) > (SELECT AVG(salary) FROM staff)
ORDER BY dept
```
**Output:**

| dept | avg_sal | n |
|---|---|---|
| A | 90000 | 3 |
**pandas equivalent:**
```python
cut = staff.salary.mean()
g = staff.groupby('dept', as_index=False).agg(avg_sal=('salary','mean'), n=('salary','size'))
result = g[g.avg_sal > cut]
```
(result checked identical to the SQL output)
**Edge cases:** NULL salaries are skipped by AVG and fail the comparison. An aggregate cannot be used in WHERE (`WHERE AVG(salary) > ...` is an error); a non-aggregated column in HAVING must be in GROUP BY.
**Likely follow-ups:**
- Can I put the same filter in both? Yes, WHERE first to cut rows cheaply, HAVING for group conditions.
- Which is faster? WHERE, because it shrinks the data before grouping.
**Common mistakes:** Using HAVING for a row-level condition or WHERE for an aggregate; expecting both to give the same numbers; mixing company average with department average.

### Q55 ⭐ 🔴 Use a CTE to find departments whose headcount is above the average department headcount, and explain what changes if some departments have zero employees.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you notice that your answer depends on whether empty departments are in the average?
**Say this in the interview:** I count employees per department in a CTE and compare each count with the average of that CTE. But I ask whether departments with zero employees should count. If they should, I start from the departments table with a LEFT JOIN and COUNT(e.emp_id) so zero rows are kept, which lowers the average.
**Explain simply:**
- **Headcount** = number of employees in a department.
- Version A groups the employees table only, so a department with no employees never appears: 4 departments, headcounts 2, 2, 3, 1, average 2.0. Only IT (3) is above.
- Version B starts from departments with a LEFT JOIN (keeps unmatched rows), so Legal appears with 0: 5 departments, average 8 / 5 = 1.6. Now HR (2), Sales (2) and IT (3) are above.
- `COUNT(e.emp_id)` counts non-NULL IDs, so Legal gets 0; `COUNT(*)` would wrongly give 1 for the joined NULL row.
**Example:** HR planning: 'which departments are bigger than the typical one?' If the empty Legal department is part of the company structure, the typical size is 1.6, not 2.
**Sample data:**
`departments`

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | Sales |
| 3 | IT |
| 4 | Finance |
| 5 | Legal |

`employees`

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 50000 |
| 2 | Bala | 1 | 60000 |
| 3 | Chitra | 2 | 70000 |
| 4 | Dev | 2 | 70000 |
| 5 | Esha | 3 | 90000 |
| 6 | Farid | 3 | 80000 |
| 7 | Gita | 3 | 80000 |
| 8 | Hari | 4 | 65000 |
**SQL:**
*A: only departments that have employees*
```sql
WITH headcount AS (
  SELECT dept_id, COUNT(*) AS n FROM employees GROUP BY dept_id)
SELECT d.dept_name, h.n
FROM headcount h JOIN departments d ON d.dept_id = h.dept_id
WHERE h.n > (SELECT AVG(n) FROM headcount)
ORDER BY d.dept_name
```
**Output:**

| dept_name | n |
|---|---|
| IT | 3 |
**pandas equivalent:**
```python
h = employees.groupby('dept_id', as_index=False).agg(n=('emp_id','size'))
m = h.merge(departments, on='dept_id')
result = m[m.n > h.n.mean()][['dept_name','n']].sort_values('dept_name')
```
(result checked identical to the SQL output)
**SQL (B: all departments, zero-employee ones included):**
```sql
WITH headcount AS (
  SELECT d.dept_id, d.dept_name, COUNT(e.emp_id) AS n
  FROM departments d LEFT JOIN employees e ON e.dept_id = d.dept_id
  GROUP BY d.dept_id, d.dept_name)
SELECT dept_name, n
FROM headcount
WHERE n > (SELECT AVG(n) FROM headcount)
ORDER BY dept_name
```
**Output:**

| dept_name | n |
|---|---|
| HR | 2 |
| IT | 3 |
| Sales | 2 |
**pandas equivalent:**
```python
h = departments.merge(employees, on='dept_id', how='left').groupby(['dept_id','dept_name'], as_index=False).agg(n=('emp_id','count'))
result = h[h.n > h.n.mean()][['dept_name','n']].sort_values('dept_name')
```
(result checked identical to the SQL output)
**Edge cases:** Same data, different answers: the business must say which average it wants. Strictly above: a department equal to the average is excluded. NULL `dept_id` employees belong to no department and are excluded from both. Zero departments gives an empty result.
**Likely follow-ups:**
- Which is right? Ask the stakeholder; for staffing benchmarks across all teams use B.
- How to show the average beside each row? `AVG(n) OVER ()` in the CTE.
**Common mistakes:** Using `COUNT(*)` with a LEFT JOIN (zero departments show 1); not noticing empty departments change the average; using INNER JOIN and silently dropping them.

