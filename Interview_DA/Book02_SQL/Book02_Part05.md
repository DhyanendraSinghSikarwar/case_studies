# Book 2 — Part 5: Window functions: ROW_NUMBER, RANK, DENSE_RANK, top-N per group 🟡

- Target: 65 questions
- Actual: 71 questions
- Scope: ranking window functions (OVER, PARTITION BY, ROW_NUMBER/RANK/DENSE_RANK/NTILE, ties, top-N per group). Running totals/LAG/LEAD/moving averages are Part 6; nth-highest/dedup/gaps-islands are Part 10.

### Q1 ⭐⭐⭐ 🟢 What is a window function in SQL, in plain words, and how is it different from GROUP BY?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know that a window function keeps every row, while GROUP BY collapses rows into one per group?
**Say this in the interview:** "A window function does a calculation across a set of related rows but still returns every original row. GROUP BY squashes each group into a single row. So with a window function I can show each employee next to their department average."
**Explain simply:**
- A *window* is just the group of rows the calculation looks at (for example, all employees in the same department).
- GROUP BY: 4 HR rows in, 1 HR row out. You lose the individual employees.
- Window function: 4 HR rows in, 4 rows out, each with the department average added as a new column.
- Ranking functions (ROW_NUMBER, RANK, DENSE_RANK) are window-only; they have no GROUP BY form.
**Example:** HR wants every employee's salary beside the department average, to see who is above or below it. GROUP BY alone cannot show both on one row.
**Sample data:** `employees` (used in most answers here)

| emp_id | name | dept | salary | hire_date |
|---|---|---|---|---|
| 1 | Asha | HR | 50000 | 2019-03-01 |
| 2 | Ben | HR | 50000 | 2020-07-15 |
| 3 | Chitra | HR | 45000 | 2021-01-10 |
| 4 | Dev | HR | 40000 | 2022-05-20 |
| 5 | Esha | Sales | 70000 | 2018-02-11 |
| 6 | Farid | Sales | 65000 | 2019-09-01 |
| 7 | Gita | Sales | 65000 | 2020-03-12 |
| 8 | Hari | Sales | 60000 | 2021-11-30 |
| 9 | Isha | Sales | 55000 | 2023-01-09 |
| 10 | Jay | IT | 90000 | 2017-06-01 |
| 11 | Kiran | IT | 80000 | 2019-04-04 |
| 12 | Lata | IT | 80000 | 2022-08-08 |
| 13 | Manoj | IT | 75000 | 2023-02-02 |

**SQL:** GROUP BY version (one row per department)
```sql
SELECT dept, AVG(salary) AS avg_salary
FROM employees
GROUP BY dept
ORDER BY dept;
```
**Output:**

| dept | avg_salary |
|---|---|
| HR | 46250 |
| IT | 81250 |
| Sales | 63000 |

**pandas equivalent:**
```python
res = employees.groupby("dept", as_index=False).agg(avg_salary=("salary", "mean")).sort_values("dept")
print(res)
```
Output of the pandas code (same rows as the SQL):
```
 dept  avg_salary
   HR     46250.0
   IT     81250.0
Sales     63000.0
```

**SQL:** window version (every row kept; shown for HR only)
```sql
SELECT name, dept, salary,
       AVG(salary) OVER (PARTITION BY dept) AS dept_avg
FROM employees
WHERE dept = 'HR'
ORDER BY emp_id;
```
**Output:**

| name | dept | salary | dept_avg |
|---|---|---|---|
| Asha | HR | 50000 | 46250 |
| Ben | HR | 50000 | 46250 |
| Chitra | HR | 45000 | 46250 |
| Dev | HR | 40000 | 46250 |

**pandas equivalent:**
```python
hr = employees[employees.dept == "HR"].sort_values("emp_id")
res = hr.assign(dept_avg=hr.groupby("dept")["salary"].transform("mean"))[["name", "dept", "salary", "dept_avg"]]
print(res)
```
Output of the pandas code (same rows as the SQL):
```
  name dept  salary  dept_avg
  Asha   HR   50000   46250.0
   Ben   HR   50000   46250.0
Chitra   HR   45000   46250.0
   Dev   HR   40000   46250.0
```

**Edge cases:** Window functions run after WHERE, so filtering to HR first means the average only uses HR rows (same here, since the partition is already by dept). NULLs are ignored by AVG in both forms.
**Likely follow-ups:**
- *Can a window function be used with GROUP BY?* Yes, it runs after grouping and can rank the grouped results (see Q16).
- *Which is faster?* Depends; windows avoid a self-join but need a sort.
**Common mistakes:** Expecting a window function to reduce the row count; selecting a plain column next to an aggregate without GROUP BY (an error in most databases).

### Q2 ⭐⭐⭐ 🟢 What does the OVER() clause do?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know OVER() is what turns a function into a window function and defines which rows it sees?
**Say this in the interview:** "OVER() tells SQL to run the function as a window function. Inside it I say how to split the rows (PARTITION BY), how to order them (ORDER BY), and optionally which rows around the current row to include (the frame). An empty OVER() means the window is the whole result set."
**Explain simply:**
- No OVER, no window: `SUM(salary)` alone is a normal aggregate.
- `OVER ()` = one big window containing all rows.
- `OVER (PARTITION BY dept)` = one window per department.
- `OVER (ORDER BY salary DESC)` = rows lined up in order, needed by ranking functions.
**Example:** Show each employee's salary as a percentage of the company payroll: the payroll total sits in `SUM(salary) OVER ()`.
**Sample data:** `employees` (see Q1), first 4 rows used.

**SQL:**
```sql
SELECT name, salary,
       SUM(salary) OVER () AS company_total,
       ROUND(100.0 * salary / SUM(salary) OVER (), 1) AS pct_of_payroll
FROM employees
ORDER BY emp_id
LIMIT 4;
```
**Output:**

| name | salary | company_total | pct_of_payroll |
|---|---|---|---|
| Asha | 50000 | 825000 | 6.1 |
| Ben | 50000 | 825000 | 6.1 |
| Chitra | 45000 | 825000 | 5.5 |
| Dev | 40000 | 825000 | 4.8 |

**pandas equivalent:**
```python
e = employees.copy()
e["company_total"] = e["salary"].sum()
e["pct_of_payroll"] = (100.0 * e["salary"] / e["company_total"]).round(1)
res = e.sort_values("emp_id").head(4)[["name", "salary", "company_total", "pct_of_payroll"]]
print(res)
```
Output of the pandas code (same rows as the SQL):
```
  name  salary  company_total  pct_of_payroll
  Asha   50000         825000             6.1
   Ben   50000         825000             6.1
Chitra   45000         825000             5.5
   Dev   40000         825000             4.8
```

LIMIT is SQLite/MySQL/PostgreSQL; SQL Server uses `TOP 4` (not run here).
**Edge cases:** LIMIT is applied after the window is computed, so the total is the whole company, not just the 4 rows shown.
**Likely follow-ups:**
- *Can I name a window once and reuse it?* Yes: `WINDOW w AS (PARTITION BY dept)` then `OVER w` (PostgreSQL, MySQL 8, SQLite; not in SQL Server, from memory).
**Common mistakes:** Forgetting that OVER() with nothing inside still has meaning (whole table); putting ORDER BY inside OVER and expecting the final output to be sorted (it is not guaranteed).

### Q3 ⭐⭐⭐ 🟢 What does PARTITION BY do inside OVER()? Explain with an HR example (employees by department).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you explain PARTITION BY as "restart the calculation for each group" without collapsing rows?
**Say this in the interview:** "PARTITION BY splits the rows into groups, like departments, and the window function is calculated separately inside each group. Unlike GROUP BY, every employee row stays in the result."
**Explain simply:**
- Think of each department as its own mini table; the calculation restarts for each.
- A *partition* is just that group of rows.
- Rows in different partitions never see each other.
**Example:** For HR and IT employees, show headcount and how far each salary is from the department average.
**Sample data:** HR and IT rows of `employees`.

| emp_id | name | dept | salary | hire_date |
|---|---|---|---|---|
| 1 | Asha | HR | 50000 | 2019-03-01 |
| 2 | Ben | HR | 50000 | 2020-07-15 |
| 3 | Chitra | HR | 45000 | 2021-01-10 |
| 4 | Dev | HR | 40000 | 2022-05-20 |
| 10 | Jay | IT | 90000 | 2017-06-01 |
| 11 | Kiran | IT | 80000 | 2019-04-04 |
| 12 | Lata | IT | 80000 | 2022-08-08 |
| 13 | Manoj | IT | 75000 | 2023-02-02 |

**SQL:**
```sql
SELECT name, dept, salary,
       COUNT(*) OVER (PARTITION BY dept) AS dept_headcount,
       ROUND(AVG(salary) OVER (PARTITION BY dept), 0) AS dept_avg,
       salary - ROUND(AVG(salary) OVER (PARTITION BY dept), 0) AS diff_from_avg
FROM employees
WHERE dept IN ('HR', 'IT')
ORDER BY emp_id;
```
**Output:**

| name | dept | salary | dept_headcount | dept_avg | diff_from_avg |
|---|---|---|---|---|---|
| Asha | HR | 50000 | 4 | 46250 | 3750 |
| Ben | HR | 50000 | 4 | 46250 | 3750 |
| Chitra | HR | 45000 | 4 | 46250 | -1250 |
| Dev | HR | 40000 | 4 | 46250 | -6250 |
| Jay | IT | 90000 | 4 | 81250 | 8750 |
| Kiran | IT | 80000 | 4 | 81250 | -1250 |
| Lata | IT | 80000 | 4 | 81250 | -1250 |
| Manoj | IT | 75000 | 4 | 81250 | -6250 |

**pandas equivalent:**
```python
e = employees[employees.dept.isin(["HR", "IT"])].sort_values("emp_id").copy()
g = e.groupby("dept")["salary"]
e["dept_headcount"] = g.transform("count")
e["dept_avg"] = g.transform("mean").round(0)
e["diff_from_avg"] = e["salary"] - e["dept_avg"]
res = e[["name", "dept", "salary", "dept_headcount", "dept_avg", "diff_from_avg"]]
print(res)
```
Output of the pandas code (same rows as the SQL):
```
  name dept  salary  dept_headcount  dept_avg  diff_from_avg
  Asha   HR   50000               4   46250.0         3750.0
   Ben   HR   50000               4   46250.0         3750.0
Chitra   HR   45000               4   46250.0        -1250.0
   Dev   HR   40000               4   46250.0        -6250.0
   Jay   IT   90000               4   81250.0         8750.0
 Kiran   IT   80000               4   81250.0        -1250.0
  Lata   IT   80000               4   81250.0        -1250.0
 Manoj   IT   75000               4   81250.0        -6250.0
```

**Edge cases:** NULL in the PARTITION BY column forms its own partition. An empty partition does not appear.
**Likely follow-ups:**
- *Can I partition by two columns?* Yes, `PARTITION BY dept, job_level`.
**Common mistakes:** Mixing it up with GROUP BY and expecting fewer rows; forgetting that WHERE removes rows before partitions are formed.

### Q4 ⭐⭐⭐ 🟢 What does ORDER BY inside OVER() do for ranking functions?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand that for ranking functions ORDER BY is the rule that decides rank 1, 2, 3.
**Say this in the interview:** "Inside OVER, ORDER BY sets the order the rows are lined up in, and the ranking function numbers them in that order. Without DESC it is ascending, so the lowest salary would be rank 1."
**Explain simply:**
- Ranking needs an order, otherwise "first" has no meaning.
- Default direction is ASC (small to large); add DESC for highest first.
- It orders rows *inside each partition*; it does not sort the final result. Add a normal ORDER BY at the end for that.
**Example:** In Sales, rank 1 should be the top earner, so use `ORDER BY salary DESC`.
**Sample data:** Sales rows of `employees` (Esha 70000, Farid 65000, Gita 65000, Hari 60000, Isha 55000).

**SQL:**
```sql
SELECT name, salary,
       RANK() OVER (ORDER BY salary)      AS rank_asc,
       RANK() OVER (ORDER BY salary DESC) AS rank_desc
FROM employees
WHERE dept = 'Sales'
ORDER BY salary DESC, name;
```
**Output:**

| name | salary | rank_asc | rank_desc |
|---|---|---|---|
| Esha | 70000 | 5 | 1 |
| Farid | 65000 | 3 | 2 |
| Gita | 65000 | 3 | 2 |
| Hari | 60000 | 2 | 4 |
| Isha | 55000 | 1 | 5 |

**pandas equivalent:**
```python
e = employees[employees.dept == "Sales"].copy()
e["rank_asc"] = e["salary"].rank(method="min", ascending=True).astype(int)
e["rank_desc"] = e["salary"].rank(method="min", ascending=False).astype(int)
res = e.sort_values(["salary", "name"], ascending=[False, True])[["name", "salary", "rank_asc", "rank_desc"]]
print(res)
```
Output of the pandas code (same rows as the SQL):
```
 name  salary  rank_asc  rank_desc
 Esha   70000         5          1
Farid   65000         3          2
 Gita   65000         3          2
 Hari   60000         2          4
 Isha   55000         1          5
```

**Edge cases:** Tied values get the same rank; NULLs sort first in ASC and last in DESC in SQLite/MySQL/SQL Server, the opposite in PostgreSQL/Oracle (see Q32).
**Likely follow-ups:**
- *Is the output sorted by this ORDER BY?* Not guaranteed; add an outer ORDER BY.
**Common mistakes:** Forgetting DESC and getting the lowest-paid person as rank 1.

### Q5 ⭐⭐⭐ 🟢 What does ROW_NUMBER() do, and when would you use it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know ROW_NUMBER gives a unique 1, 2, 3... even for ties, and where that is useful.
**Say this in the interview:** "ROW_NUMBER numbers the rows 1, 2, 3 within each partition in the order I specify. It never repeats a number, even for ties, so I use it when I need exactly one row per group, like the latest record or de-duplicating."
**Explain simply:**
- Unique numbering per partition, restarting at 1.
- Ties still get different numbers; which tie gets the lower number is arbitrary unless you add a tie-breaker (Q30).
- Typical uses: top 1 per group, latest record per customer, removing duplicates, serial numbers.
**Example:** Number employees in each department by joining date, so join_order 1 is the longest-serving person.
**Sample data:** HR and IT rows of `employees` (see Q3).

**SQL:**
```sql
SELECT name, dept, hire_date,
       ROW_NUMBER() OVER (PARTITION BY dept ORDER BY hire_date) AS join_order
FROM employees
WHERE dept IN ('HR', 'IT')
ORDER BY dept, join_order;
```
**Output:**

| name | dept | hire_date | join_order |
|---|---|---|---|
| Asha | HR | 2019-03-01 | 1 |
| Ben | HR | 2020-07-15 | 2 |
| Chitra | HR | 2021-01-10 | 3 |
| Dev | HR | 2022-05-20 | 4 |
| Jay | IT | 2017-06-01 | 1 |
| Kiran | IT | 2019-04-04 | 2 |
| Lata | IT | 2022-08-08 | 3 |
| Manoj | IT | 2023-02-02 | 4 |

**pandas equivalent:**
```python
e = employees[employees.dept.isin(["HR", "IT"])].sort_values(["dept", "hire_date"]).copy()
e["join_order"] = e.groupby("dept").cumcount() + 1
res = e[["name", "dept", "hire_date", "join_order"]]
print(res)
```
Output of the pandas code (same rows as the SQL):
```
  name dept  hire_date  join_order
  Asha   HR 2019-03-01           1
   Ben   HR 2020-07-15           2
Chitra   HR 2021-01-10           3
   Dev   HR 2022-05-20           4
   Jay   IT 2017-06-01           1
 Kiran   IT 2019-04-04           2
  Lata   IT 2022-08-08           3
 Manoj   IT 2023-02-02           4
```

**Edge cases:** Ties on the ORDER BY column give non-deterministic numbering. Empty partitions produce nothing.
**Likely follow-ups:**
- *ROW_NUMBER vs RANK?* RANK repeats numbers for ties; ROW_NUMBER never does (Q8).
**Common mistakes:** Using it for "top 3 with ties" (it cuts ties arbitrarily); no tie-breaker.

### Q6 ⭐⭐⭐ 🟢 What does RANK() do, and how does it treat tied values?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know RANK gives tied rows the same rank and then skips numbers.
**Say this in the interview:** "RANK gives equal values the same rank, and the next rank skips ahead by the number of ties. Like an Olympic race: two golds, no silver, next is bronze."
**Explain simply:**
- Salaries 50000, 50000, 45000, 40000 get ranks 1, 1, 3, 4.
- Rank 2 does not exist because two people share rank 1; the *gap* equals the number of ties minus one.
- Use it when position-in-the-field matters ("3rd best", not "3rd best value").
**Example:** HR department: Asha and Ben both earn 50000, so both are rank 1; Chitra is rank 3.
**Sample data:** HR rows of `employees` (50000, 50000, 45000, 40000).

**SQL:**
```sql
SELECT name, salary,
       RANK() OVER (ORDER BY salary DESC) AS salary_rank
FROM employees
WHERE dept = 'HR'
ORDER BY salary_rank, name;
```
**Output:**

| name | salary | salary_rank |
|---|---|---|
| Asha | 50000 | 1 |
| Ben | 50000 | 1 |
| Chitra | 45000 | 3 |
| Dev | 40000 | 4 |

**pandas equivalent:**
```python
e = employees[employees.dept == "HR"].copy()
e["salary_rank"] = e["salary"].rank(method="min", ascending=False).astype(int)
res = e.sort_values(["salary_rank", "name"])[["name", "salary", "salary_rank"]]
print(res)
```
Output of the pandas code (same rows as the SQL):
```
  name  salary  salary_rank
  Asha   50000            1
   Ben   50000            1
Chitra   45000            3
   Dev   40000            4
```

**Edge cases:** All-equal values give everyone rank 1. NULLs rank together as a tie.
**Likely follow-ups:**
- *How to avoid the gap?* Use DENSE_RANK (Q7).
**Common mistakes:** Expecting rank 2 to exist; using `RANK() = 2` to find the second-highest salary (returns nothing if the top is tied).

### Q7 ⭐⭐⭐ 🟢 What does DENSE_RANK() do, and how does it treat tied values?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know DENSE_RANK ties share a rank but numbering continues with no gaps.
**Say this in the interview:** "DENSE_RANK also gives ties the same rank, but the next rank is just the next number, with no gap. It ranks distinct values, so rank 2 means the second-highest salary value."
**Explain simply:**
- Salaries 70000, 65000, 65000, 60000, 55000 get 1, 2, 2, 3, 4.
- "Dense" = no holes in the sequence.
- Ideal for "Nth highest salary", because N counts distinct values.
**Example:** In Sales, Farid and Gita both earn 65000 (rank 2); Hari at 60000 is rank 3, not 4.
**Sample data:** Sales rows of `employees`.

**SQL:**
```sql
SELECT name, salary,
       DENSE_RANK() OVER (ORDER BY salary DESC) AS salary_rank
FROM employees
WHERE dept = 'Sales'
ORDER BY salary_rank, name;
```
**Output:**

| name | salary | salary_rank |
|---|---|---|
| Esha | 70000 | 1 |
| Farid | 65000 | 2 |
| Gita | 65000 | 2 |
| Hari | 60000 | 3 |
| Isha | 55000 | 4 |

**pandas equivalent:**
```python
e = employees[employees.dept == "Sales"].copy()
e["salary_rank"] = e["salary"].rank(method="dense", ascending=False).astype(int)
res = e.sort_values(["salary_rank", "name"])[["name", "salary", "salary_rank"]]
print(res)
```
Output of the pandas code (same rows as the SQL):
```
 name  salary  salary_rank
 Esha   70000            1
Farid   65000            2
 Gita   65000            2
 Hari   60000            3
 Isha   55000            4
```

**Edge cases:** NULLs form one rank value. Empty input gives no rows.
**Likely follow-ups:**
- *Nth highest salary?* `DENSE_RANK() ... = N` in a subquery or CTE (Q12).
**Common mistakes:** Using RANK when the question means "distinct salary levels".

### Q8 ⭐⭐⭐ 🟢 What is the difference between ROW_NUMBER, RANK and DENSE_RANK? Show it with salaries 100, 100, 90, 80.
**Asked at:** commonly asked (no company-specific report found); generic prep sources list this as a very frequent question.
**What the interviewer is checking:** Can you show the three functions' different tie behaviour on a tiny example.
**Say this in the interview:** "With 100, 100, 90, 80: ROW_NUMBER gives 1, 2, 3, 4 (always unique), RANK gives 1, 1, 3, 4 (ties share, then it skips), DENSE_RANK gives 1, 1, 2, 3 (ties share, no skip)."
**Explain simply:**
- ROW_NUMBER: a unique line number; ties are split arbitrarily.
- RANK: competition ranking, has gaps.
- DENSE_RANK: no gaps.
- All three give the same result when there are no ties.
**Example:** Three employees at 100, 100, 90 in a salary table: who is "third highest"? RANK says the 90 person is 3rd person; DENSE_RANK says 2nd distinct salary.
**Sample data:** `s`

| label | salary |
|---|---|
| A | 100 |
| B | 100 |
| C | 90 |
| D | 80 |

**SQL:**
```sql
SELECT label, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num,
       RANK()       OVER (ORDER BY salary DESC) AS rnk,
       DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rnk
FROM s
ORDER BY row_num;
```
**Output:**

| label | salary | row_num | rnk | dense_rnk |
|---|---|---|---|---|
| A | 100 | 1 | 1 | 1 |
| B | 100 | 2 | 1 | 1 |
| C | 90 | 3 | 3 | 2 |
| D | 80 | 4 | 4 | 3 |

**pandas equivalent:**
```python
t = s.copy().sort_values("salary", ascending=False, kind="stable")
t["row_num"] = range(1, len(t) + 1)
t["rnk"] = t["salary"].rank(method="min", ascending=False).astype(int)
t["dense_rnk"] = t["salary"].rank(method="dense", ascending=False).astype(int)
res = t
print(res)
```
Output of the pandas code (same rows as the SQL):
```
label  salary  row_num  rnk  dense_rnk
    A     100        1    1          1
    B     100        2    1          1
    C      90        3    3          2
    D      80        4    4          3
```

**Edge cases:** Which of the two 100s is row_num 1 is arbitrary unless you add a tie-breaker.
**Likely follow-ups:**
- *Which for top-N with ties?* RANK or DENSE_RANK (Q15).
**Common mistakes:** Memorising the names but not the gap behaviour.

### Q9 ⭐⭐⭐ 🟢 Can you use RANK() without ORDER BY in OVER()? What happens?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know ranking needs an order, and that dialects differ on whether they enforce it.
**Say this in the interview:** "Logically, RANK needs ORDER BY, because rank means position in some order. In SQLite and PostgreSQL it runs without one and treats every row as a tie, so everyone is rank 1. SQL Server and Oracle reject it, from memory."
**Explain simply:**
- No ORDER BY means all rows are "peers" (equal), so RANK = 1 for all, DENSE_RANK = 1 for all.
- ROW_NUMBER without ORDER BY still numbers rows, but in no guaranteed order.
- The result is meaningless, so always supply ORDER BY.
**Example:** Ranking HR employees with no ORDER BY gives rank 1 to everyone.
**Sample data:** HR rows of `employees`.

**SQL:**
```sql
SELECT name, salary,
       RANK() OVER () AS rank_no_order,
       RANK() OVER (ORDER BY salary DESC) AS rank_with_order
FROM employees
WHERE dept = 'HR'
ORDER BY emp_id;
```
**Output:**

| name | salary | rank_no_order | rank_with_order |
|---|---|---|---|
| Asha | 50000 | 1 | 1 |
| Ben | 50000 | 1 | 1 |
| Chitra | 45000 | 1 | 3 |
| Dev | 40000 | 1 | 4 |

**pandas equivalent:**
```python
e = employees[employees.dept == "HR"].sort_values("emp_id").copy()
e["rank_no_order"] = 1
e["rank_with_order"] = e["salary"].rank(method="min", ascending=False).astype(int)
res = e[["name", "salary", "rank_no_order", "rank_with_order"]]
print(res)
```
Output of the pandas code (same rows as the SQL):
```
  name  salary  rank_no_order  rank_with_order
  Asha   50000              1                1
   Ben   50000              1                1
Chitra   45000              1                3
   Dev   40000              1                4
```

**Edge cases:** Behaviour verified here on SQLite only; SQL Server/Oracle error (not run here / from memory).
**Likely follow-ups:**
- *And aggregates like SUM OVER?* They do not need ORDER BY.
**Common mistakes:** Leaving out ORDER BY by accident and getting a silent "everyone is #1".

### Q10 ⭐⭐⭐ 🟡 Write a query to find the top 3 highest-paid employees in each department.
**Asked at:** commonly asked (no company-specific report found); generic prep sources list "top N per department" among the most-asked SQL queries.
**What the interviewer is checking:** Rank inside a partition, then filter in an outer query.
**Say this in the interview:** "I rank salaries within each department using a window function in a CTE (a named temporary result), then filter to rank 3 or less in the outer query. I would clarify how to treat ties first."
**Explain simply:**
- PARTITION BY dept restarts the ranking per department; ORDER BY salary DESC puts the highest first.
- A window function cannot sit in WHERE, so wrap it in a CTE (a named sub-query defined with WITH).
- ROW_NUMBER gives exactly 3 rows per department; use RANK/DENSE_RANK to keep ties (Q15).
**Example:** Show HR the three best-paid people in each department for a pay-equity review.
**Sample data:** `employees` (see Q1).

**SQL:**
```sql
WITH ranked AS (
    SELECT name, dept, salary,
           ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC, emp_id) AS rn
    FROM employees
)
SELECT dept, name, salary, rn
FROM ranked
WHERE rn <= 3
ORDER BY dept, rn;
```
**Output:**

| dept | name | salary | rn |
|---|---|---|---|
| HR | Asha | 50000 | 1 |
| HR | Ben | 50000 | 2 |
| HR | Chitra | 45000 | 3 |
| IT | Jay | 90000 | 1 |
| IT | Kiran | 80000 | 2 |
| IT | Lata | 80000 | 3 |
| Sales | Esha | 70000 | 1 |
| Sales | Farid | 65000 | 2 |
| Sales | Gita | 65000 | 3 |

**pandas equivalent:**
```python
e = employees.sort_values(["dept", "salary", "emp_id"], ascending=[True, False, True]).copy()
e["rn"] = e.groupby("dept").cumcount() + 1
res = e[e.rn <= 3][["dept", "name", "salary", "rn"]]
print(res)
```
Output of the pandas code (same rows as the SQL):
```
 dept   name  salary  rn
   HR   Asha   50000   1
   HR    Ben   50000   2
   HR Chitra   45000   3
   IT    Jay   90000   1
   IT  Kiran   80000   2
   IT   Lata   80000   3
Sales   Esha   70000   1
Sales  Farid   65000   2
Sales   Gita   65000   3
```

**Edge cases:** Ties: Farid and Gita tie at 65000 in Sales and both fit in the top 3 here, but in HR Asha/Ben tie and the tie-breaker emp_id decides order. A department with fewer than 3 people returns fewer rows.
**Likely follow-ups:**
- *Snowflake/BigQuery shortcut?* `QUALIFY ROW_NUMBER() OVER (...) <= 3` (not run here).
**Common mistakes:** `WHERE ROW_NUMBER() OVER (...) <= 3` (error); no tie-breaker so results change between runs.

### Q11 ⭐⭐⭐ 🟡 Write a query to find the highest-paid employee in each department (include everyone tied at the top).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Choosing RANK (not ROW_NUMBER) so everyone tied at the top stays.
**Say this in the interview:** "I use RANK partitioned by department, ordered by salary descending, and keep rank 1. Because RANK gives ties the same number, everyone tied at the top is included."
**Explain simply:**
- Same pattern as top-N, but N = 1.
- ROW_NUMBER = 1 would drop one of the tied people.
**Example:** HR: Asha and Ben both earn 50000, so both are returned.
**Sample data:** `employees` (see Q1).

**SQL:**
```sql
WITH ranked AS (
    SELECT name, dept, salary,
           RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk
    FROM employees
)
SELECT dept, name, salary
FROM ranked
WHERE rnk = 1
ORDER BY dept, name;
```
**Output:**

| dept | name | salary |
|---|---|---|
| HR | Asha | 50000 |
| HR | Ben | 50000 |
| IT | Jay | 90000 |
| Sales | Esha | 70000 |

**pandas equivalent:**
```python
e = employees.copy()
e["rnk"] = e.groupby("dept")["salary"].rank(method="min", ascending=False).astype(int)
res = e[e.rnk == 1].sort_values(["dept", "name"])[["dept", "name", "salary"]]
print(res)
```
Output of the pandas code (same rows as the SQL):
```
 dept name  salary
   HR Asha   50000
   HR  Ben   50000
   IT  Jay   90000
Sales Esha   70000
```

**Edge cases:** NULL salaries are ordered last in DESC order in SQLite, but in PostgreSQL NULLs come first in DESC and could steal rank 1: add `NULLS LAST` there (from memory).
**Likely follow-ups:**
- *Without window functions?* `salary = (SELECT MAX(salary) FROM employees e2 WHERE e2.dept = e.dept)` (Q52).
**Common mistakes:** Using ROW_NUMBER and silently losing tied top earners; using MAX with GROUP BY and then not being able to show the name.

### Q12 ⭐⭐⭐ 🟡 Write a query to find the second-highest salary in each department.
**Asked at:** commonly asked (no company-specific report found); generic prep sources list "second highest per department" as frequent.
**What the interviewer is checking:** DENSE_RANK so "second-highest" means second distinct salary value.
**Say this in the interview:** "I'd use DENSE_RANK by department ordered by salary descending and filter to 2. That way, if two people tie for the top salary, the second-highest is still the next distinct salary, not missing."
**Explain simply:**
- DENSE_RANK has no gaps, so rank 2 always exists if there are at least two distinct salaries.
- With RANK, a top tie would jump to rank 3 and you would get no rank 2.
**Example:** HR: top is 50000 (two people); second-highest is 45000 (Chitra).
**Sample data:** `employees` (see Q1).

**SQL:**
```sql
WITH ranked AS (
    SELECT name, dept, salary,
           DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS dr
    FROM employees
)
SELECT dept, name, salary
FROM ranked
WHERE dr = 2
ORDER BY dept, name;
```
**Output:**

| dept | name | salary |
|---|---|---|
| HR | Chitra | 45000 |
| IT | Kiran | 80000 |
| IT | Lata | 80000 |
| Sales | Farid | 65000 |
| Sales | Gita | 65000 |

**pandas equivalent:**
```python
e = employees.copy()
e["dr"] = e.groupby("dept")["salary"].rank(method="dense", ascending=False).astype(int)
res = e[e.dr == 2].sort_values(["dept", "name"])[["dept", "name", "salary"]]
print(res)
```
Output of the pandas code (same rows as the SQL):
```
 dept   name  salary
   HR Chitra   45000
   IT  Kiran   80000
   IT   Lata   80000
Sales  Farid   65000
Sales   Gita   65000
```

**Edge cases:** A department with one distinct salary returns nothing (no second-highest). If you want one row per department, use `ROW_NUMBER` after dedup, or `SELECT DISTINCT dept, salary`.
**Likely follow-ups:**
- *Interpreting "second highest" as second person?* Then ROW_NUMBER; state your assumption.
**Common mistakes:** Using RANK = 2 (empty when top is tied); `LIMIT 1 OFFSET 1` which is not per group.

### Q13 ⭐⭐⭐ 🟡 Why can't you use a window function directly in the WHERE clause, and how do you filter on a rank instead?
**Asked at:** commonly asked (no company-specific report found); generic prep sources list "window function in WHERE" as a classic mistake.
**What the interviewer is checking:** Do you know the order SQL evaluates clauses in and the CTE/subquery workaround.
**Say this in the interview:** "WHERE is processed before window functions exist, so the rank is not calculated yet. I compute the rank in a CTE or subquery, then filter on that column in the outer query."
**Explain simply:**
- Window functions are computed after WHERE, GROUP BY and HAVING, just before SELECT output.
- So WHERE cannot see their results.
- Fix: compute in an inner query, filter in the outer one. (Snowflake, BigQuery, DuckDB also offer QUALIFY, not run here for Snowflake/BigQuery.)
**Example:** Show only employees ranked in the top 2 salaries in their department.
**Sample data:** `employees` (see Q1).

The wrong query fails in SQLite with: `misuse of window function RANK()`

**SQL:**
```sql
-- WRONG: SELECT name FROM employees WHERE RANK() OVER (ORDER BY salary DESC) <= 2;
SELECT *
FROM (
    SELECT name, dept, salary,
           RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk
    FROM employees
) t
WHERE rnk <= 2
ORDER BY dept, rnk, name;
```
**Output:**

| name | dept | salary | rnk |
|---|---|---|---|
| Asha | HR | 50000 | 1 |
| Ben | HR | 50000 | 1 |
| Jay | IT | 90000 | 1 |
| Kiran | IT | 80000 | 2 |
| Lata | IT | 80000 | 2 |
| Esha | Sales | 70000 | 1 |
| Farid | Sales | 65000 | 2 |
| Gita | Sales | 65000 | 2 |

**pandas equivalent:**
```python
e = employees.copy()
e["rnk"] = e.groupby("dept")["salary"].rank(method="min", ascending=False).astype(int)
res = e[e.rnk <= 2].sort_values(["dept", "rnk", "name"])[["name", "dept", "salary", "rnk"]]
print(res)
```
Output of the pandas code (same rows as the SQL):
```
 name  dept  salary  rnk
 Asha    HR   50000    1
  Ben    HR   50000    1
  Jay    IT   90000    1
Kiran    IT   80000    2
 Lata    IT   80000    2
 Esha Sales   70000    1
Farid Sales   65000    2
 Gita Sales   65000    2
```

**Edge cases:** Ties at rank 2 can return more than 2 rows per department (Q69).
**Likely follow-ups:**
- *Can I do it in HAVING?* No; HAVING also runs before windows (Q67).
**Common mistakes:** Putting the window function in WHERE; trying to reference the SELECT alias `rnk` in the same query's WHERE.

### Q14 ⭐⭐⭐ 🟡 How do you do top-N per group using a CTE or subquery with ROW_NUMBER?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the standard two-step pattern: rank inside, filter outside.
**Say this in the interview:** "Step one: in a CTE or subquery I add ROW_NUMBER partitioned by the group and ordered by the measure. Step two: in the outer query I keep rows where the number is at most N."
**Explain simply:**
- CTE = a named temporary result defined with WITH; subquery = same idea written inline in FROM. They behave the same here.
- Change `<= 2` to any N.
- Add a tie-breaker (emp_id) so the result is stable.
**Example:** The two highest-paid employees per department.
**Sample data:** `employees` (see Q1).

**SQL:** CTE version
```sql
WITH ranked AS (
    SELECT name, dept, salary,
           ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC, emp_id) AS rn
    FROM employees
)
SELECT dept, name, salary, rn
FROM ranked
WHERE rn <= 2
ORDER BY dept, rn;
```
**Output:**

| dept | name | salary | rn |
|---|---|---|---|
| HR | Asha | 50000 | 1 |
| HR | Ben | 50000 | 2 |
| IT | Jay | 90000 | 1 |
| IT | Kiran | 80000 | 2 |
| Sales | Esha | 70000 | 1 |
| Sales | Farid | 65000 | 2 |

**pandas equivalent:**
```python
e = employees.sort_values(["dept", "salary", "emp_id"], ascending=[True, False, True]).copy()
e["rn"] = e.groupby("dept").cumcount() + 1
res = e[e.rn <= 2][["dept", "name", "salary", "rn"]]
print(res)
```
Output of the pandas code (same rows as the SQL):
```
 dept  name  salary  rn
   HR  Asha   50000   1
   HR   Ben   50000   2
   IT   Jay   90000   1
   IT Kiran   80000   2
Sales  Esha   70000   1
Sales Farid   65000   2
```

Subquery version (I ran it; it returns exactly the same rows):
```sql
SELECT dept, name, salary, rn
FROM (
    SELECT name, dept, salary,
           ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC, emp_id) AS rn
    FROM employees
) t
WHERE rn <= 2
ORDER BY dept, rn;
```
**Edge cases:** Groups smaller than N return fewer rows. Ties are cut arbitrarily without the tie-breaker.
**Likely follow-ups:**
- *CTE or subquery?* Same performance in most databases; CTEs read better when reused.
**Common mistakes:** Filtering in the same SELECT; forgetting the ORDER BY inside OVER.

### Q15 ⭐⭐⭐ 🟡 Which function would you choose for top-N per group when ties exist, and why?
**Asked at:** commonly asked (no company-specific report found); generic prep sources discuss the tie trade-off as a frequent follow-up.
**What the interviewer is checking:** Can you pick the function from the business requirement, and ask about ties.
**Say this in the interview:** "It depends what N means. Exactly N rows: ROW_NUMBER. Everyone who ties into the top N positions: RANK. N distinct values: DENSE_RANK. I would ask the interviewer which they want."
**Explain simply:**
- ROW_NUMBER: always N rows per group, ties cut arbitrarily.
- RANK: keeps ties, may return more than N rows; skips numbers.
- DENSE_RANK: keeps ties, N distinct salary levels, could return many rows.
- For a bonus to the "top 2 earners", RANK is typically fair.
**Example:** Sales has 70000, 65000, 65000, 60000, 55000. Top 2:
**Sample data:** Sales and IT rows of `employees`.

**SQL:**
```sql
SELECT dept, name, salary,
       ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC, emp_id) AS rn,
       RANK()       OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk,
       DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS dr
FROM employees
WHERE dept IN ('Sales', 'IT')
ORDER BY dept, rn;
```
**Output:**

| dept | name | salary | rn | rnk | dr |
|---|---|---|---|---|---|
| IT | Jay | 90000 | 1 | 1 | 1 |
| IT | Kiran | 80000 | 2 | 2 | 2 |
| IT | Lata | 80000 | 3 | 2 | 2 |
| IT | Manoj | 75000 | 4 | 4 | 3 |
| Sales | Esha | 70000 | 1 | 1 | 1 |
| Sales | Farid | 65000 | 2 | 2 | 2 |
| Sales | Gita | 65000 | 3 | 2 | 2 |
| Sales | Hari | 60000 | 4 | 4 | 3 |
| Sales | Isha | 55000 | 5 | 5 | 4 |

**pandas equivalent:**
```python
e = employees[employees.dept.isin(["Sales", "IT"])].sort_values(["dept", "salary", "emp_id"], ascending=[True, False, True]).copy()
g = e.groupby("dept")["salary"]
e["rn"] = e.groupby("dept").cumcount() + 1
e["rnk"] = g.rank(method="min", ascending=False).astype(int)
e["dr"] = g.rank(method="dense", ascending=False).astype(int)
res = e[["dept", "name", "salary", "rn", "rnk", "dr"]]
print(res)
```
Output of the pandas code (same rows as the SQL):
```
 dept  name  salary  rn  rnk  dr
   IT   Jay   90000   1    1   1
   IT Kiran   80000   2    2   2
   IT  Lata   80000   3    2   2
   IT Manoj   75000   4    4   3
Sales  Esha   70000   1    1   1
Sales Farid   65000   2    2   2
Sales  Gita   65000   3    2   2
Sales  Hari   60000   4    4   3
Sales  Isha   55000   5    5   4
```

Reading it for "top 2" in Sales: rn <= 2 gives Esha and Farid (Gita lost to the tie-break); rnk <= 2 gives Esha, Farid, Gita; dr <= 2 gives the same three. For "top 3" in Sales, dr <= 3 adds Hari while rnk <= 3 does not.
**Edge cases:** IT has Kiran and Lata tied at 80000: RANK top 2 returns 3 people (Jay, Kiran, Lata).
**Likely follow-ups:**
- *Can I get both exactly N rows and fair ties?* Not at once; choose and document.
**Common mistakes:** Defaulting to ROW_NUMBER and silently dropping tied employees.

### Q16 ⭐⭐⭐ 🟡 Write a query to rank sales representatives by total sales within each region.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Aggregate first (GROUP BY), then rank the totals with a window function.
**Say this in the interview:** "First I total sales per rep with SUM and GROUP BY, then I rank those totals within each region. A window function can use the grouped result because it is calculated after GROUP BY."
**Explain simply:**
- Window functions run after GROUP BY, so `RANK() OVER (... ORDER BY SUM(amount) DESC)` is legal.
- I wrap it in a CTE for clarity.
- RANK shows ties honestly (Anil and Bina both 800 in North).
**Example:** Each rep may have several sales; the leaderboard is by total per region.
**Sample data:** `sales`

| sale_id | rep | region | amount |
|---|---|---|---|
| 1 | Anil | North | 500 |
| 2 | Anil | North | 300 |
| 3 | Bina | North | 800 |
| 4 | Chetan | North | 200 |
| 5 | Deepa | South | 900 |
| 6 | Deepa | South | 100 |
| 7 | Esh | South | 600 |
| 8 | Farah | South | 400 |

**SQL:**
```sql
WITH totals AS (
    SELECT region, rep, SUM(amount) AS total_sales
    FROM sales
    GROUP BY region, rep
)
SELECT region, rep, total_sales,
       RANK() OVER (PARTITION BY region ORDER BY total_sales DESC) AS region_rank
FROM totals
ORDER BY region, region_rank, rep;
```
**Output:**

| region | rep | total_sales | region_rank |
|---|---|---|---|
| North | Anil | 800 | 1 |
| North | Bina | 800 | 1 |
| North | Chetan | 200 | 3 |
| South | Deepa | 1000 | 1 |
| South | Esh | 600 | 2 |
| South | Farah | 400 | 3 |

**pandas equivalent:**
```python
t = sales.groupby(["region", "rep"], as_index=False).agg(total_sales=("amount", "sum"))
t["region_rank"] = t.groupby("region")["total_sales"].rank(method="min", ascending=False).astype(int)
res = t.sort_values(["region", "region_rank", "rep"])
print(res)
```
Output of the pandas code (same rows as the SQL):
```
region    rep  total_sales  region_rank
 North   Anil          800            1
 North   Bina          800            1
 North Chetan          200            3
 South  Deepa         1000            1
 South    Esh          600            2
 South  Farah          400            3
```

**Edge cases:** Ties share a rank; NULL amounts are ignored by SUM, and a rep with only NULL sales gets a NULL total.
**Likely follow-ups:**
- *Top rep only?* Filter `region_rank = 1` in an outer query.
**Common mistakes:** Ranking raw rows instead of totals, so one rep appears several times.

### Q17 ⭐⭐⭐ 🟡 Write a query to find the top 5 products by revenue in each category.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Top-N per group with a measure (revenue) and a decision on ties.
**Say this in the interview:** "I aggregate revenue per product if needed, rank within each category with DENSE_RANK or RANK, and keep rank 5 or less in an outer query. I would use RANK to keep ties at the cut-off."
**Explain simply:**
- PARTITION BY category restarts the ranking for each category.
- A category with fewer than 5 products just returns what it has (Books has 4).
- If the table has one row per sale, first SUM per product.
**Example:** Show the five best-selling products in each category for a merchandising review.
**Sample data:** `product_revenue` (already one row per product).

| product | category | revenue |
|---|---|---|
| Phone | Electronics | 900 |
| Laptop | Electronics | 850 |
| Tablet | Electronics | 600 |
| Camera | Electronics | 400 |
| Speaker | Electronics | 300 |
| Cable | Electronics | 50 |
| Novel | Books | 200 |
| Atlas | Books | 150 |
| Guide | Books | 120 |
| Comic | Books | 80 |

**SQL:**
```sql
WITH ranked AS (
    SELECT category, product, revenue,
           RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS rnk
    FROM product_revenue
)
SELECT category, product, revenue, rnk
FROM ranked
WHERE rnk <= 5
ORDER BY category, rnk;
```
**Output:**

| category | product | revenue | rnk |
|---|---|---|---|
| Books | Novel | 200 | 1 |
| Books | Atlas | 150 | 2 |
| Books | Guide | 120 | 3 |
| Books | Comic | 80 | 4 |
| Electronics | Phone | 900 | 1 |
| Electronics | Laptop | 850 | 2 |
| Electronics | Tablet | 600 | 3 |
| Electronics | Camera | 400 | 4 |
| Electronics | Speaker | 300 | 5 |

**pandas equivalent:**
```python
p = product_revenue.copy()
p["rnk"] = p.groupby("category")["revenue"].rank(method="min", ascending=False).astype(int)
res = p[p.rnk <= 5].sort_values(["category", "rnk"])[["category", "product", "revenue", "rnk"]]
print(res)
```
Output of the pandas code (same rows as the SQL):
```
   category product  revenue  rnk
      Books   Novel      200    1
      Books   Atlas      150    2
      Books   Guide      120    3
      Books   Comic       80    4
Electronics   Phone      900    1
Electronics  Laptop      850    2
Electronics  Tablet      600    3
Electronics  Camera      400    4
Electronics Speaker      300    5
```

Cable (Electronics, revenue 50) is dropped as rank 6.
**Edge cases:** A tie at 5th place would return 6 rows with RANK; use ROW_NUMBER for exactly 5. NULL revenue ranks last in DESC in SQLite.
**Likely follow-ups:**
- *Per-product revenue from order lines?* `SUM(qty * price) ... GROUP BY product` in a CTE first.
**Common mistakes:** Forgetting to aggregate first; `LIMIT 5` which gives 5 rows overall, not per category.

### Q18 ⭐⭐ 🟢 What is the difference between a window function and an aggregate function?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Row count behaviour: aggregates collapse, window functions keep rows.
**Say this in the interview:** "An aggregate function like SUM used with GROUP BY returns one row per group. A window function calculates over a group of rows but returns a value on every row. Some functions, like SUM, can be either; ranking functions are window-only."
**Explain simply:**
- Aggregate (GROUP BY): fewer rows out, detail lost.
- Window (OVER): same number of rows out, detail kept.
- Aggregates can be used as windows by adding OVER; ROW_NUMBER, RANK, LAG have no aggregate form.
- Window functions cannot be filtered in WHERE; aggregates can be filtered with HAVING.
**Example:** Total sales per region (aggregate) versus each sale shown beside its region's total (window).
**Sample data:** `sales` (see Q16).

**SQL:** aggregate (2 rows)
```sql
SELECT region, SUM(amount) AS region_total
FROM sales
GROUP BY region
ORDER BY region;
```
**Output:**

| region | region_total |
|---|---|
| North | 1800 |
| South | 2000 |

**pandas equivalent:**
```python
res = sales.groupby("region", as_index=False).agg(region_total=("amount", "sum")).sort_values("region")
print(res)
```
Output of the pandas code (same rows as the SQL):
```
region  region_total
 North          1800
 South          2000
```

**SQL:** window (all 8 rows kept)
```sql
SELECT sale_id, rep, region, amount,
       SUM(amount) OVER (PARTITION BY region) AS region_total
FROM sales
ORDER BY sale_id;
```
**Output:**

| sale_id | rep | region | amount | region_total |
|---|---|---|---|---|
| 1 | Anil | North | 500 | 1800 |
| 2 | Anil | North | 300 | 1800 |
| 3 | Bina | North | 800 | 1800 |
| 4 | Chetan | North | 200 | 1800 |
| 5 | Deepa | South | 900 | 2000 |
| 6 | Deepa | South | 100 | 2000 |
| 7 | Esh | South | 600 | 2000 |
| 8 | Farah | South | 400 | 2000 |

**pandas equivalent:**
```python
t = sales.sort_values("sale_id").copy()
t["region_total"] = t.groupby("region")["amount"].transform("sum")
res = t
print(res)
```
Output of the pandas code (same rows as the SQL):
```
 sale_id    rep region  amount  region_total
       1   Anil  North     500          1800
       2   Anil  North     300          1800
       3   Bina  North     800          1800
       4 Chetan  North     200          1800
       5  Deepa  South     900          2000
       6  Deepa  South     100          2000
       7    Esh  South     600          2000
       8  Farah  South     400          2000
```

**Edge cases:** NULLs are skipped by SUM in both forms.
**Likely follow-ups:**
- *Percent of region total?* `amount * 100.0 / SUM(amount) OVER (PARTITION BY region)`.
**Common mistakes:** Selecting non-grouped columns with GROUP BY; thinking OVER makes a query slower in every case.

### Q19 ⭐⭐ 🟢 Can you use PARTITION BY without ORDER BY, and what does the result look like?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know that PARTITION BY alone (no ORDER BY) is legal, and that it gives one fixed value per group repeated on every row?
**Say this in the interview:** "Yes. PARTITION BY splits rows into groups, and without ORDER BY an aggregate like SUM just covers the whole group, so every row in the group shows the same total. Adding ORDER BY turns it into a running total."
**Explain simply:**
- A *window function* does a calculation across a set of related rows but keeps every row (unlike GROUP BY, which collapses rows).
- `PARTITION BY dept` = "treat each department as its own mini-table".
- No ORDER BY: the window is the whole partition, so `SUM(salary)` is the department total on every row.
- With ORDER BY: the default window becomes "from the first row up to the current row", so the same SUM turns into a running total.
- Ranking functions (ROW_NUMBER, RANK) need ORDER BY to be meaningful; SQL Server rejects them without it (from memory, not run here).
**Example:** HR wants each employee next to their department payroll without losing the employee rows. Dept IT total = 90+80+80+70 = 320k.
**Sample data:**
Table `emp`:
| emp_id | name | dept | salary | hire_date |
|---|---|---|---|---|
| 1 | Asha | HR | 50000 | 2019-03-01 |
| 2 | Bala | HR | 60000 | 2021-07-15 |
| 3 | Dev | IT | 90000 | 2020-05-20 |
| 4 | Esha | IT | 80000 | 2017-11-02 |
| 5 | Farid | IT | 80000 | 2022-02-14 |
| 6 | Gita | IT | 70000 | 2023-01-09 |
| 7 | Isha | Sales | 55000 | 2019-06-30 |
| 8 | Jay | Sales | 65000 | 2024-03-18 |
**SQL:**
```sql
SELECT name, dept, salary,
       SUM(salary) OVER (PARTITION BY dept)                  AS dept_total,
       COUNT(*)    OVER (PARTITION BY dept)                  AS dept_headcount,
       SUM(salary) OVER (PARTITION BY dept ORDER BY emp_id)  AS running_total   -- contrast: with ORDER BY
FROM emp
ORDER BY emp_id;
```
**Output:**
| name | dept | salary | dept_total | dept_headcount | running_total |
|---|---|---|---|---|---|
| Asha | HR | 50000 | 110000 | 2 | 50000 |
| Bala | HR | 60000 | 110000 | 2 | 110000 |
| Dev | IT | 90000 | 320000 | 4 | 90000 |
| Esha | IT | 80000 | 320000 | 4 | 170000 |
| Farid | IT | 80000 | 320000 | 4 | 250000 |
| Gita | IT | 70000 | 320000 | 4 | 320000 |
| Isha | Sales | 55000 | 120000 | 2 | 55000 |
| Jay | Sales | 65000 | 120000 | 2 | 120000 |
**pandas equivalent:** (result checked equal to the SQL output)
```python
res = emp.copy()
res["dept_total"] = res.groupby("dept")["salary"].transform("sum")
res["dept_headcount"] = res.groupby("dept")["salary"].transform("count")
res["running_total"] = res.sort_values("emp_id").groupby("dept")["salary"].cumsum()
res = res[["name", "dept", "salary", "dept_total", "dept_headcount", "running_total"]]
```
**Edge cases:** NULL salaries are ignored by SUM, but `COUNT(*)` still counts the row (`COUNT(salary)` would not). With ORDER BY, rows that tie on the ORDER BY value are treated as one step (RANGE frame), so the running total jumps for both at once. An empty table gives no rows.
**Likely follow-ups:**
- What if I omit PARTITION BY too? One partition = the entire result set (see Q20).
- Can I get the running total without ties jumping together? Yes: add `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`.
**Common mistakes:** Thinking PARTITION BY needs ORDER BY, or that adding ORDER BY to a SUM changes nothing (it silently makes it cumulative).

### Q20 ⭐⭐ 🟢 What happens if you omit PARTITION BY? What is the 'partition' then?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know OVER () is legal and treats the whole result as one group?
**Say this in the interview:** "If I leave out PARTITION BY, the partition is the entire result set after WHERE, JOIN and GROUP BY. So OVER () gives a company-wide number repeated on every row."
**Explain simply:**
- `OVER ()` with empty brackets = one big partition containing every row that survives WHERE/JOIN/GROUP BY.
- It is how you show 'row value vs overall value' side by side, for example salary vs company average.
- Rows removed by WHERE are not in the partition, so filtering changes the answer.
**Example:** Company average salary = 550,000 / 8 = 68,750. Gita earns 70,000 so she is 1,250 above average.
**Sample data:**
Table `emp`:
| emp_id | name | dept | salary | hire_date |
|---|---|---|---|---|
| 1 | Asha | HR | 50000 | 2019-03-01 |
| 2 | Bala | HR | 60000 | 2021-07-15 |
| 3 | Dev | IT | 90000 | 2020-05-20 |
| 4 | Esha | IT | 80000 | 2017-11-02 |
| 5 | Farid | IT | 80000 | 2022-02-14 |
| 6 | Gita | IT | 70000 | 2023-01-09 |
| 7 | Isha | Sales | 55000 | 2019-06-30 |
| 8 | Jay | Sales | 65000 | 2024-03-18 |
**SQL:**
```sql
SELECT name, salary,
       COUNT(*)    OVER () AS headcount,
       AVG(salary) OVER () AS company_avg,
       salary - AVG(salary) OVER () AS diff_from_avg
FROM emp
ORDER BY emp_id;
```
**Output:**
| name | salary | headcount | company_avg | diff_from_avg |
|---|---|---|---|---|
| Asha | 50000 | 8 | 68750 | -18750 |
| Bala | 60000 | 8 | 68750 | -8750 |
| Dev | 90000 | 8 | 68750 | 21250 |
| Esha | 80000 | 8 | 68750 | 11250 |
| Farid | 80000 | 8 | 68750 | 11250 |
| Gita | 70000 | 8 | 68750 | 1250 |
| Isha | 55000 | 8 | 68750 | -13750 |
| Jay | 65000 | 8 | 68750 | -3750 |
**pandas equivalent:** (result checked equal to the SQL output)
```python
res = emp[["name", "salary"]].copy()
res["headcount"] = len(emp)
res["company_avg"] = emp["salary"].mean()
res["diff_from_avg"] = res["salary"] - res["company_avg"]
```
**Edge cases:** AVG ignores NULL salaries (so the average is over non-NULL rows only). A WHERE filter shrinks the partition. Empty input returns no rows, so no average appears.
**Likely follow-ups:**
- How is this different from a subquery `(SELECT AVG(salary) FROM emp)`? Same value, but OVER () respects the current WHERE/GROUP BY and reads more cleanly.
- Percent of total? `salary * 100.0 / SUM(salary) OVER ()`.
**Common mistakes:** Using GROUP BY to get the average and then losing the individual rows, or forgetting that WHERE is applied before the window.

### Q21 ⭐⭐ 🟢 How do you rank in descending order (highest value gets rank 1)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the sort direction in the window's ORDER BY decides who gets rank 1?
**Say this in the interview:** "Put DESC in the ORDER BY inside OVER. RANK() OVER (ORDER BY salary DESC) gives the highest salary rank 1. The default is ASC, which gives the lowest value rank 1."
**Explain simply:**
- The ORDER BY inside `OVER (...)` controls ranking, not the final ORDER BY of the query.
- Default is ASC, so smallest = rank 1. Write `DESC` for biggest = rank 1.
- `RANK` leaves gaps after ties, `DENSE_RANK` does not, `ROW_NUMBER` never repeats (more in Q29).
**Example:** Top salary 90,000 should be rank 1 in a pay review.
**Sample data:**
Table `emp`:
| emp_id | name | dept | salary | hire_date |
|---|---|---|---|---|
| 1 | Asha | HR | 50000 | 2019-03-01 |
| 2 | Bala | HR | 60000 | 2021-07-15 |
| 3 | Dev | IT | 90000 | 2020-05-20 |
| 4 | Esha | IT | 80000 | 2017-11-02 |
| 5 | Farid | IT | 80000 | 2022-02-14 |
| 6 | Gita | IT | 70000 | 2023-01-09 |
| 7 | Isha | Sales | 55000 | 2019-06-30 |
| 8 | Jay | Sales | 65000 | 2024-03-18 |
**SQL:**
```sql
SELECT name, salary,
       RANK()       OVER (ORDER BY salary DESC) AS rnk,
       DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rnk,
       RANK()       OVER (ORDER BY salary ASC)  AS rnk_ascending   -- default direction, for contrast
FROM emp
ORDER BY rnk, name;
```
**Output:**
| name | salary | rnk | dense_rnk | rnk_ascending |
|---|---|---|---|---|
| Dev | 90000 | 1 | 1 | 8 |
| Esha | 80000 | 2 | 2 | 6 |
| Farid | 80000 | 2 | 2 | 6 |
| Gita | 70000 | 4 | 3 | 5 |
| Jay | 65000 | 5 | 4 | 4 |
| Bala | 60000 | 6 | 5 | 3 |
| Isha | 55000 | 7 | 6 | 2 |
| Asha | 50000 | 8 | 7 | 1 |
**pandas equivalent:** (result checked equal to the SQL output)
```python
res = emp[["name", "salary"]].copy()
res["rnk"] = res["salary"].rank(method="min", ascending=False).astype(int)
res["dense_rnk"] = res["salary"].rank(method="dense", ascending=False).astype(int)
res["rnk_ascending"] = res["salary"].rank(method="min", ascending=True).astype(int)
res = res.sort_values(["rnk", "name"]).reset_index(drop=True)
```
**Edge cases:** Ties share a rank (Esha and Farid are both 2). NULLs sort as smallest in SQLite/MySQL/SQL Server but largest in PostgreSQL/Oracle, so a NULL salary may take rank 1 in PostgreSQL with DESC (see Q32).
**Likely follow-ups:**
- Rank only the top 3? Wrap in a CTE and filter `rnk <= 3` (you cannot filter a window function in WHERE; see Q23).
- Can the outer ORDER BY differ? Yes, it only sorts the output.
**Common mistakes:** Putting ORDER BY salary DESC at the end of the query and expecting the rank column to change; or forgetting DESC inside OVER.

### Q22 ⭐⭐ 🟢 What does NTILE() do? Give an example such as splitting employees into 4 salary quartiles.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know NTILE cuts ordered rows into N roughly equal buckets, and how it handles leftovers?
**Say this in the interview:** "NTILE(4) sorts the rows and splits them into four buckets of as-equal-as-possible size, numbered 1 to 4. Order by salary DESC and bucket 1 is the top quartile."
**Explain simply:**
- `NTILE(n)` = 'cut the sorted list into n groups'. A *quartile* is one quarter of the data (n = 4).
- If rows don't divide evenly, the first buckets get one extra row (8 rows into 3 buckets = 3, 3, 2).
- It splits by row position, not by value, so equal salaries can land in different buckets unless you accept that or tie-break.
- Add `PARTITION BY dept` to bucket within each department.
**Example:** 8 employees into 4 salary quartiles = 2 people per quartile; into 3 groups = 3, 3, 2.
**Sample data:**
Table `emp`:
| emp_id | name | dept | salary | hire_date |
|---|---|---|---|---|
| 1 | Asha | HR | 50000 | 2019-03-01 |
| 2 | Bala | HR | 60000 | 2021-07-15 |
| 3 | Dev | IT | 90000 | 2020-05-20 |
| 4 | Esha | IT | 80000 | 2017-11-02 |
| 5 | Farid | IT | 80000 | 2022-02-14 |
| 6 | Gita | IT | 70000 | 2023-01-09 |
| 7 | Isha | Sales | 55000 | 2019-06-30 |
| 8 | Jay | Sales | 65000 | 2024-03-18 |
**SQL:**
```sql
SELECT name, salary,
       NTILE(4) OVER (ORDER BY salary DESC, emp_id) AS quartile,
       NTILE(3) OVER (ORDER BY salary DESC, emp_id) AS tercile
FROM emp
ORDER BY salary DESC, emp_id;
```
**Output:**
| name | salary | quartile | tercile |
|---|---|---|---|
| Dev | 90000 | 1 | 1 |
| Esha | 80000 | 1 | 1 |
| Farid | 80000 | 2 | 1 |
| Gita | 70000 | 2 | 2 |
| Jay | 65000 | 3 | 2 |
| Bala | 60000 | 3 | 2 |
| Isha | 55000 | 4 | 3 |
| Asha | 50000 | 4 | 3 |
**pandas equivalent:** (result checked equal to the SQL output)
```python
def ntile(n_rows, n):
    q, r = divmod(n_rows, n)
    out = []
    for i in range(n_rows):
        out.append(i // (q + 1) + 1 if i < r * (q + 1) else r + (i - r * (q + 1)) // q + 1)
    return out

res = emp.sort_values(["salary", "emp_id"], ascending=[False, True])[["name", "salary"]].reset_index(drop=True)
res["quartile"] = ntile(len(res), 4)
res["tercile"] = ntile(len(res), 3)
```
**Edge cases:** Fewer rows than buckets: some buckets stay empty. Ties at a bucket boundary are split arbitrarily, so add a tie-break column (emp_id). NULLs sort first/last per dialect and land in an end bucket. In pandas, `pd.qcut` cuts by value quantiles and differs slightly.
**Likely follow-ups:**
- NTILE vs PERCENT_RANK? PERCENT_RANK gives a 0-1 position, NTILE gives a bucket number.
- Quartile per department? `NTILE(4) OVER (PARTITION BY dept ORDER BY salary DESC)`.
**Common mistakes:** Assuming NTILE buckets by salary value ranges, or not realising uneven counts push extra rows into the earlier buckets.

### Q23 ⭐⭐ 🟡 What is the SQL order of execution, and why does it matter for window functions?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the logical order SQL evaluates clauses, and why you cannot filter on a window result in WHERE?
**Say this in the interview:** "SQL runs FROM, then WHERE, GROUP BY, HAVING, then window functions, then SELECT's remaining work, DISTINCT, ORDER BY and LIMIT. Window functions come after WHERE, so WHERE can't see them and they only see rows that survived the filter. To filter on a rank, I wrap the query in a CTE or subquery."
**Explain simply:**
- Logical order (not the order you type): 1 FROM/JOIN, 2 WHERE, 3 GROUP BY, 4 HAVING, 5 window functions, 6 SELECT list, 7 DISTINCT, 8 ORDER BY, 9 LIMIT/TOP.
- WHERE runs before windows, so `WHERE rnk = 1` fails: the rank does not exist yet. Same reason you can't use a SELECT alias in WHERE.
- Rows removed by WHERE never enter the window: filter first and the ranks change.
- Fix: compute the rank in a subquery/CTE, then filter in the outer query. (Some engines like Snowflake/BigQuery/DuckDB offer QUALIFY, a clause that filters after windows; not standard, not in SQLite/PostgreSQL/MySQL/SQL Server, from memory.)
**Example:** Top earner per department. Filtering `salary <= 80000` inside the inner query first would drop Dev (90k) before ranking, so Esha would wrongly look like the IT top earner; filtering after ranking keeps everyone in the ranking.
**Sample data:** same `emp` table as above (8 employees, 3 departments).
**SQL:**
```sql
-- wrong: window alias used in WHERE
SELECT name, RANK() OVER (ORDER BY salary DESC) AS r FROM emp WHERE r = 1;
-- SQLite error: misuse of aliased window function r

-- right: filter in the outer query (rank over ALL employees)
SELECT dept, name, salary FROM (
  SELECT dept, name, salary,
         RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk
  FROM emp
) t WHERE rnk = 1 ORDER BY dept;
```
**Output:** (right query, run)
| dept | name | salary |
|---|---|---|
| HR | Bala | 60000 |
| IT | Dev | 90000 |
| Sales | Jay | 65000 |
With `WHERE salary <= 80000` placed inside the inner query (filter first), the IT winner changes because Dev is removed before ranking:
| dept | name | salary |
|---|---|---|
| HR | Bala | 60000 |
| IT | Esha | 80000 |
| IT | Farid | 80000 |
| Sales | Jay | 65000 |
**Edge cases:** HAVING also runs before windows, so you can window over aggregated results (`RANK() OVER (ORDER BY SUM(x) DESC)`) but not filter on the rank in HAVING. ORDER BY runs after windows, so it can use the rank alias.
**Likely follow-ups:**
- Why can ORDER BY use an alias but WHERE can't? ORDER BY runs later, after SELECT.
- Can I use a window function in GROUP BY or HAVING? No.
**Common mistakes:** Writing `WHERE ROW_NUMBER() OVER (...) = 1` (error in every major engine), or thinking the typed order of clauses is the run order.

### Q24 ⭐⭐ 🟡 How do you get the latest record per customer (for example, most recent order) using ROW_NUMBER?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you do the classic 'latest row per group' with ROW_NUMBER, including a tie-break?
**Say this in the interview:** "Number each customer's orders newest first with ROW_NUMBER partitioned by customer, then keep row number 1. I add order_id as a tie-breaker so two orders on the same day don't make it random."
**Explain simply:**
- `ROW_NUMBER()` hands out 1, 2, 3... inside each group, no repeats.
- `PARTITION BY customer ORDER BY order_date DESC` = newest order gets 1.
- Filter `rn = 1` in an outer query (windows can't be used in WHERE; Q23).
- Tie-break on a unique column so the answer is repeatable.
**Example:** Rahul has two orders on 12 Mar (102 and 106). With order_id DESC as tie-break, 106 is picked every time.
**Sample data:**
Table `orders`:
| order_id | customer | order_date | amount |
|---|---|---|---|
| 101 | Rahul | 2025-01-05 | 500 |
| 102 | Rahul | 2025-03-12 | 700 |
| 103 | Meena | 2025-02-01 | 300 |
| 104 | Meena | 2025-02-01 | 450 |
| 105 | Karan | 2025-01-20 | 900 |
| 106 | Rahul | 2025-03-12 | 200 |
| 107 | Karan | 2025-04-02 | 100 |
**SQL:**
```sql
SELECT customer, order_id, order_date, amount
FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY customer
                               ORDER BY order_date DESC, order_id DESC) AS rn
  FROM orders
) t
WHERE rn = 1
ORDER BY customer;
```
**Output:**
| customer | order_id | order_date | amount |
|---|---|---|---|
| Karan | 107 | 2025-04-02 | 100 |
| Meena | 104 | 2025-02-01 | 450 |
| Rahul | 106 | 2025-03-12 | 200 |
**pandas equivalent:** (result checked equal to the SQL output)
```python
res = (orders.sort_values(["customer", "order_date", "order_id"], ascending=[True, False, False])
             .drop_duplicates("customer")[["customer", "order_id", "order_date", "amount"]]
             .reset_index(drop=True))
```
**Edge cases:** Same-day ties need a tie-break (else arbitrary). NULL dates sort last/first depending on dialect and could be picked as 'latest' in PostgreSQL with DESC. Use RANK instead if you want to keep all tied latest orders. A customer with no orders does not appear.
**Likely follow-ups:**
- Why not MAX(order_date)? It gives the date, not the whole row, and joining back duplicates on ties.
- Keep all tied orders? Use RANK() = 1.
**Common mistakes:** Forgetting the tie-break, or filtering `rn = 1` in the same SELECT where it is created.

### Q25 ⭐⭐ 🟡 How do you get the first order of each customer using a window function?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Same pattern as 'latest per group' but ascending; do you handle ties?
**Say this in the interview:** "ROW_NUMBER partitioned by customer ordered by order_date ascending, keep rn = 1. Same trick as latest, only the sort direction flips, and I add order_id to break ties."
**Explain simply:**
- First order = earliest date, so the ORDER BY inside OVER is ASC.
- `PARTITION BY customer` restarts numbering for each customer.
- The outer query keeps `rn = 1`.
- Useful in HR too: each employee's first appraisal, first role, first leave.
**Example:** Meena placed 103 and 104 on 1 Feb. Order by order_id ASC makes 103 the first.
**Sample data:**
Table `orders` (as in Q24).
**SQL:**
```sql
SELECT customer, order_id, order_date, amount
FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY customer
                               ORDER BY order_date ASC, order_id ASC) AS rn
  FROM orders
) t
WHERE rn = 1
ORDER BY customer;
```
**Output:**
| customer | order_id | order_date | amount |
|---|---|---|---|
| Karan | 105 | 2025-01-20 | 900 |
| Meena | 103 | 2025-02-01 | 300 |
| Rahul | 101 | 2025-01-05 | 500 |
**pandas equivalent:** (result checked equal to the SQL output)
```python
res = (orders.sort_values(["customer", "order_date", "order_id"])
             .drop_duplicates("customer")[["customer", "order_id", "order_date", "amount"]]
             .reset_index(drop=True))
```
**Edge cases:** Tied earliest dates, NULL dates (sorted first in SQLite/MySQL/SQL Server for ASC, so a NULL date could win; PostgreSQL puts NULLs last on ASC), customers with one order (their only order is the first).
**Likely follow-ups:**
- Alternative without windows? `WHERE order_date = (SELECT MIN(order_date) ...)` correlated subquery, but it returns both tied rows.
- First AND latest in one query? Two ROW_NUMBERs (ASC and DESC) and keep either = 1.
**Common mistakes:** Using MIN(order_date) with GROUP BY and then trying to select other columns (invalid or wrong in strict engines).

### Q26 ⭐⭐ 🟡 Write a query to find the top 3 students by marks in each class, keeping ties.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Top-N per group with ties: do you pick RANK/DENSE_RANK instead of ROW_NUMBER and explain the difference?
**Say this in the interview:** "I rank marks descending within each class and keep rank <= 3. I use RANK so tied students all stay in. If they mean three distinct mark levels I'd use DENSE_RANK."
**Explain simply:**
- `RANK` gives tied students the same rank and skips the next number (1, 2, 2, 4).
- `rnk <= 3` therefore keeps ties but may return more than 3 rows per class.
- The question is a little ambiguous: 'top 3 places' (RANK) vs 'top 3 distinct scores' (DENSE_RANK). I state my choice out loud.
- ROW_NUMBER would drop tied students arbitrarily, so it is wrong here.
**Example:** Class A: Ann 95, Ben 90, Cara 90, Dan 85. Ben and Cara tie for 2nd, so Dan is 4th with RANK and is excluded.
**Sample data:**
Table `students`:
| name | class | marks |
|---|---|---|
| Ann | A | 95 |
| Ben | A | 90 |
| Cara | A | 90 |
| Dan | A | 85 |
| Eli | A | 80 |
| Fay | B | 88 |
| Gus | B | 88 |
| Hal | B | 88 |
| Ivy | B | 70 |
| Jo | B | 60 |
**SQL:**
```sql
SELECT class, name, marks, rnk
FROM (
  SELECT class, name, marks,
         RANK() OVER (PARTITION BY class ORDER BY marks DESC) AS rnk
  FROM students
) t
WHERE rnk <= 3
ORDER BY class, rnk, name;
```
**Output:**
| class | name | marks | rnk |
|---|---|---|---|
| A | Ann | 95 | 1 |
| A | Ben | 90 | 2 |
| A | Cara | 90 | 2 |
| B | Fay | 88 | 1 |
| B | Gus | 88 | 1 |
| B | Hal | 88 | 1 |
**pandas equivalent:** (result checked equal to the SQL output)
```python
res = students.copy()
res["rnk"] = res.groupby("class")["marks"].rank(method="min", ascending=False).astype(int)
res = res[res["rnk"] <= 3].sort_values(["class", "rnk", "name"]).reset_index(drop=True)[["class", "name", "marks", "rnk"]]
```
**Edge cases:** A big tie at the top (class B has three students on 88) means 3 rows already fill the quota, so Ivy and Jo are out. NULL marks sort per dialect and could get rank 1 in PostgreSQL. Fewer than 3 students returns them all.
**Likely follow-ups:**
- Exactly 3 rows per class, ties broken by name? Use ROW_NUMBER with `ORDER BY marks DESC, name`.
- With DENSE_RANK <= 3 the result has 9 rows instead of 6: Dan (class A) and Ivy, Jo (class B) come in.
**Common mistakes:** Using ROW_NUMBER and silently dropping tied students, or using LIMIT 3 which cannot work per group.

### Q27 ⭐⭐ 🟡 Write a query to rank employees by tenure within each department.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you turn 'tenure' into a date calculation and rank the right way round (earliest hire = longest tenure)?
**Say this in the interview:** "Longest tenure means earliest hire date, so I rank by hire_date ascending inside each department. I also show years of service computed against a fixed date."
**Explain simply:**
- *Tenure* = how long someone has been with the company = today minus hire date.
- Rank 1 should be the most senior person, so sort hire_date ASC (earliest first).
- Ranking by hire_date ASC is the same as ranking tenure DESC, and it avoids rounding issues.
- Date functions differ by dialect (see below).
**Example:** In IT, Esha joined Nov 2017 (rank 1, about 7.2 years by 1 Jan 2025) and Gita joined Jan 2023 (rank 4).
**Sample data:**
Table `emp`:
| emp_id | name | dept | salary | hire_date |
|---|---|---|---|---|
| 1 | Asha | HR | 50000 | 2019-03-01 |
| 2 | Bala | HR | 60000 | 2021-07-15 |
| 3 | Dev | IT | 90000 | 2020-05-20 |
| 4 | Esha | IT | 80000 | 2017-11-02 |
| 5 | Farid | IT | 80000 | 2022-02-14 |
| 6 | Gita | IT | 70000 | 2023-01-09 |
| 7 | Isha | Sales | 55000 | 2019-06-30 |
| 8 | Jay | Sales | 65000 | 2024-03-18 |
**SQL:**
```sql
-- tenure measured up to a fixed date so the result is repeatable
SELECT dept, name, hire_date,
       ROUND((julianday('2025-01-01') - julianday(hire_date)) / 365.25, 1) AS tenure_years,
       RANK() OVER (PARTITION BY dept ORDER BY hire_date ASC) AS tenure_rank
FROM emp
ORDER BY dept, tenure_rank;
```
Dialect notes (not run here, from memory): PostgreSQL `CURRENT_DATE - hire_date` gives days, or `AGE(...)`; MySQL `TIMESTAMPDIFF(YEAR, hire_date, CURDATE())`; SQL Server `DATEDIFF(YEAR, hire_date, GETDATE())` (counts year boundaries, not full years).
**Output:**
| dept | name | hire_date | tenure_years | tenure_rank |
|---|---|---|---|---|
| HR | Asha | 2019-03-01 | 5.8 | 1 |
| HR | Bala | 2021-07-15 | 3.5 | 2 |
| IT | Esha | 2017-11-02 | 7.2 | 1 |
| IT | Dev | 2020-05-20 | 4.6 | 2 |
| IT | Farid | 2022-02-14 | 2.9 | 3 |
| IT | Gita | 2023-01-09 | 2 | 4 |
| Sales | Isha | 2019-06-30 | 5.5 | 1 |
| Sales | Jay | 2024-03-18 | 0.8 | 2 |
**pandas equivalent:** (result checked equal to the SQL output)
```python
res = emp[["dept", "name", "hire_date"]].copy()
hd = pd.to_datetime(res["hire_date"])
res["tenure_years"] = ((pd.Timestamp("2025-01-01") - hd).dt.days / 365.25).round(1)
res["tenure_rank"] = res.groupby("dept")["hire_date"].rank(method="min").astype(int)
res = res.sort_values(["dept", "tenure_rank"]).reset_index(drop=True)
```
**Edge cases:** Same hire date = same rank (RANK). NULL hire dates sort first in SQLite/MySQL/SQL Server and last in PostgreSQL on ASC, so decide whether to exclude them. Employees who left need an exit date instead of 'today'.
**Likely follow-ups:**
- Tenure per employee as of today? Replace the fixed date with `CURRENT_DATE` (PostgreSQL/MySQL) or `GETDATE()` (SQL Server).
- Rank across the company? Drop PARTITION BY.
**Common mistakes:** Ranking by tenure DESC when tenure is stored as a date (that inverts it), or using today's date so results change every day in a demo.

### Q28 ⭐⭐ 🟡 Write a query that shows each employee's salary rank within their department and across the whole company in the same output.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you mix two windows (partitioned and unpartitioned) in one SELECT?
**Say this in the interview:** "I use two RANK calls with different OVER clauses: one with PARTITION BY dept for the department rank and one without for the company rank. Both come back in the same row."
**Explain simply:**
- Each window function has its own `OVER (...)`, so each can partition differently.
- `PARTITION BY dept ORDER BY salary DESC` = rank inside the department.
- `OVER (ORDER BY salary DESC)` = rank across everyone.
- No extra join or subquery needed.
**Example:** Dev (IT) is rank 1 in IT and rank 1 in the company; Bala (HR) is rank 1 in HR but only rank 6 in the company.
**Sample data:**
Table `emp`:
| emp_id | name | dept | salary | hire_date |
|---|---|---|---|---|
| 1 | Asha | HR | 50000 | 2019-03-01 |
| 2 | Bala | HR | 60000 | 2021-07-15 |
| 3 | Dev | IT | 90000 | 2020-05-20 |
| 4 | Esha | IT | 80000 | 2017-11-02 |
| 5 | Farid | IT | 80000 | 2022-02-14 |
| 6 | Gita | IT | 70000 | 2023-01-09 |
| 7 | Isha | Sales | 55000 | 2019-06-30 |
| 8 | Jay | Sales | 65000 | 2024-03-18 |
**SQL:**
```sql
SELECT name, dept, salary,
       RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS dept_rank,
       RANK() OVER (ORDER BY salary DESC)                   AS company_rank
FROM emp
ORDER BY company_rank, name;
```
**Output:**
| name | dept | salary | dept_rank | company_rank |
|---|---|---|---|---|
| Dev | IT | 90000 | 1 | 1 |
| Esha | IT | 80000 | 2 | 2 |
| Farid | IT | 80000 | 2 | 2 |
| Gita | IT | 70000 | 4 | 4 |
| Jay | Sales | 65000 | 1 | 5 |
| Bala | HR | 60000 | 1 | 6 |
| Isha | Sales | 55000 | 2 | 7 |
| Asha | HR | 50000 | 2 | 8 |
**pandas equivalent:** (result checked equal to the SQL output)
```python
res = emp[["name", "dept", "salary"]].copy()
res["dept_rank"] = res.groupby("dept")["salary"].rank(method="min", ascending=False).astype(int)
res["company_rank"] = res["salary"].rank(method="min", ascending=False).astype(int)
res = res.sort_values(["company_rank", "name"]).reset_index(drop=True)
```
**Edge cases:** Ties share both ranks (Esha and Farid). NULL salaries rank per dialect (Q32). A department with one person has dept_rank 1.
**Likely follow-ups:**
- Same thing via named windows? `WINDOW w AS (...)` in PostgreSQL/MySQL 8/SQLite, not SQL Server (from memory).
- Add percentile? `PERCENT_RANK() OVER (...)`.
**Common mistakes:** Computing the company rank in a separate query and joining, which is slower and unnecessary.

### Q29 ⭐⭐ 🟡 If two employees tie for 2nd place, what rank does RANK() give the next person? What about DENSE_RANK()?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the exact gap behaviour of RANK vs DENSE_RANK (and ROW_NUMBER)?
**Say this in the interview:** "RANK gives tied people the same rank and then skips: two people on 2 means the next is 4. DENSE_RANK doesn't skip, so the next is 3. ROW_NUMBER ignores ties and just counts 1, 2, 3, 4."
**Explain simply:**
- Two employees tied for 2nd: RANK = 1, 2, 2, 4 (a gap, like sports medals).
- DENSE_RANK = 1, 2, 2, 3 (no gap).
- ROW_NUMBER = 1, 2, 3, 4 (always unique; ties broken arbitrarily).
- Use DENSE_RANK for 'Nth highest salary' questions; use RANK for competition-style placing.
**Example:** Salaries 90k, 80k, 80k, 70k: the 70k person is 4th by RANK, 3rd by DENSE_RANK.
**Sample data:**
Table `emp`:
| emp_id | name | dept | salary | hire_date |
|---|---|---|---|---|
| 1 | Asha | HR | 50000 | 2019-03-01 |
| 2 | Bala | HR | 60000 | 2021-07-15 |
| 3 | Dev | IT | 90000 | 2020-05-20 |
| 4 | Esha | IT | 80000 | 2017-11-02 |
| 5 | Farid | IT | 80000 | 2022-02-14 |
| 6 | Gita | IT | 70000 | 2023-01-09 |
| 7 | Isha | Sales | 55000 | 2019-06-30 |
| 8 | Jay | Sales | 65000 | 2024-03-18 |
**SQL:**
```sql
SELECT name, salary,
       RANK()       OVER (ORDER BY salary DESC) AS rank_,
       DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rank_,
       ROW_NUMBER() OVER (ORDER BY salary DESC, emp_id) AS row_num
FROM emp
ORDER BY salary DESC, emp_id;
```
**Output:**
| name | salary | rank_ | dense_rank_ | row_num |
|---|---|---|---|---|
| Dev | 90000 | 1 | 1 | 1 |
| Esha | 80000 | 2 | 2 | 2 |
| Farid | 80000 | 2 | 2 | 3 |
| Gita | 70000 | 4 | 3 | 4 |
| Jay | 65000 | 5 | 4 | 5 |
| Bala | 60000 | 6 | 5 | 6 |
| Isha | 55000 | 7 | 6 | 7 |
| Asha | 50000 | 8 | 7 | 8 |
**pandas equivalent:** (result checked equal to the SQL output)
```python
res = emp.sort_values(["salary", "emp_id"], ascending=[False, True])[["name", "salary"]].copy()
res["rank_"] = res["salary"].rank(method="min", ascending=False).astype(int)
res["dense_rank_"] = res["salary"].rank(method="dense", ascending=False).astype(int)
res["row_num"] = range(1, len(res) + 1)
res = res.reset_index(drop=True)
```
**Edge cases:** Esha and Farid are tied at 80k; Gita (70k) is 4th with RANK but 3rd with DENSE_RANK. If every value is unique all three functions agree. NULLs tie with each other.
**Likely follow-ups:**
- Which one for 'second highest salary'? DENSE_RANK = 2 (RANK = 2 would skip if the top is tied).
- Why does ROW_NUMBER need a tie-break? See Q30/Q31.
**Common mistakes:** Using RANK for 'Nth highest' and getting no row because rank N was skipped.

### Q30 ⭐⭐ 🟡 How would you break ties in ROW_NUMBER deterministically (for example by employee ID)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know to add a unique column to ORDER BY so ROW_NUMBER is repeatable?
**Say this in the interview:** "I add a unique column such as emp_id as the last ORDER BY key inside OVER. Then even if two salaries tie, the order is always the same, so ROW_NUMBER gives the same answer on every run."
**Explain simply:**
- ROW_NUMBER must give every row a different number, so for tied rows the database has to choose who comes first.
- Without a tie-break, that choice is up to the engine and can change between runs or after an index/plan change.
- Append a unique key: `ORDER BY salary DESC, emp_id ASC`.
- The tie-break should be something meaningful if possible (earlier hire date, alphabetical name) and finally a unique ID.
**Example:** Esha and Farid both earn 80k. With emp_id ASC as the tie-break, Esha (id 4) is always row 3 and Farid (id 5) row 4.
**Sample data:**
Table `emp`:
| emp_id | name | dept | salary | hire_date |
|---|---|---|---|---|
| 1 | Asha | HR | 50000 | 2019-03-01 |
| 2 | Bala | HR | 60000 | 2021-07-15 |
| 3 | Dev | IT | 90000 | 2020-05-20 |
| 4 | Esha | IT | 80000 | 2017-11-02 |
| 5 | Farid | IT | 80000 | 2022-02-14 |
| 6 | Gita | IT | 70000 | 2023-01-09 |
| 7 | Isha | Sales | 55000 | 2019-06-30 |
| 8 | Jay | Sales | 65000 | 2024-03-18 |
**SQL:**
```sql
SELECT emp_id, name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC, emp_id ASC) AS rn
FROM emp
ORDER BY rn;
```
**Output:**
| emp_id | name | salary | rn |
|---|---|---|---|
| 3 | Dev | 90000 | 1 |
| 4 | Esha | 80000 | 2 |
| 5 | Farid | 80000 | 3 |
| 6 | Gita | 70000 | 4 |
| 8 | Jay | 65000 | 5 |
| 2 | Bala | 60000 | 6 |
| 7 | Isha | 55000 | 7 |
| 1 | Asha | 50000 | 8 |
**pandas equivalent:** (result checked equal to the SQL output)
```python
res = emp.sort_values(["salary", "emp_id"], ascending=[False, True])[["emp_id", "name", "salary"]].reset_index(drop=True)
res["rn"] = range(1, len(res) + 1)
```
**Edge cases:** If the tie-break column itself has NULLs or duplicates the problem returns, so use a primary key. In pandas, `sort_values` is not stable by default for all kinds, so pass `kind='stable'` when tie order matters.
**Likely follow-ups:**
- Why not just ORDER BY salary DESC? The tie order is undefined (Q31).
- Per group? Add PARTITION BY and keep the same tie-break.
**Common mistakes:** Assuming the engine will 'naturally' keep insertion order for ties, it may not.

### Q31 ⭐⭐ 🟡 Is ROW_NUMBER() deterministic when ORDER BY values tie? Explain the risk.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand that ties make ROW_NUMBER's order undefined, and the business risk of that?
**Say this in the interview:** "No. When ORDER BY values tie, the standard doesn't say which tied row gets the lower number, so results can change between runs, engines, or after someone adds an index. That makes 'top 1 per group' queries unstable, so I always add a unique tie-break column."
**Explain simply:**
- *Deterministic* = same input always gives the same output.
- ROW_NUMBER with tied ORDER BY values is not guaranteed deterministic: the tied rows get different numbers in an unspecified order.
- Risk: a 'top paid employee per department' report could show Esha today and Farid tomorrow, with no data change. Bonus or payroll decisions on that are unsafe.
- Fix: add a unique key to the ORDER BY (Q30), or use RANK if you want ties kept.
**Example:** Esha and Farid both earn 80k. Without a tie-break either could be row 2 or row 3 of the company list.
**Sample data:** `emp` as above; Esha and Farid tie at 80,000.
**SQL:**
```sql
SELECT name, salary,
       ROW_NUMBER() OVER (ORDER BY salary DESC)           AS rn_no_tiebreak,   -- tied order not guaranteed
       ROW_NUMBER() OVER (ORDER BY salary DESC, emp_id)   AS rn_with_tiebreak  -- always the same
FROM emp WHERE salary >= 70000 ORDER BY rn_with_tiebreak;
```
**Output:** (SQLite 3 run; the unsafe column happened to look sensible here, which is exactly why the bug hides)
| name | salary | rn_no_tiebreak | rn_with_tiebreak |
|---|---|---|---|
| Dev | 90000 | 1 | 1 |
| Esha | 80000 | 2 | 2 |
| Farid | 80000 | 3 | 3 |
| Gita | 70000 | 4 | 4 |
In a quick test on the two 80k rows, SQLite returned [('Esha', 1), ('Farid', 2)] without a tie-break and [('Esha', 1), ('Farid', 2)] with one, even after I added an index on (salary, name). I could not make it differ here, so I cannot show the failure live; the standard simply does not guarantee the order, and other engines or larger data may differ.
**Edge cases:** Ties are only a problem when you filter on the number (rn = 1) or the tied rows differ in other columns. If the ORDER BY is on a unique column there is no issue. The same risk applies to LIMIT with ties (Q37).
**Likely follow-ups:**
- How do you fix it? Add a unique column to ORDER BY.
- When is non-determinism acceptable? When you only need any one row and the choice does not matter.
**Common mistakes:** Testing once on a small table, seeing a sensible answer, and concluding the query is safe.

### Q32 ⭐⭐ 🟡 How do NULL values behave in the ORDER BY of a ranking function (NULLS FIRST or LAST)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know NULLs are not equal to anything, how each database sorts them, and how to control it?
**Say this in the interview:** "NULL means unknown. In a ranking ORDER BY, NULLs are all grouped together and tie with each other. Where they land depends on the database: SQLite, MySQL and SQL Server treat NULL as the smallest value, PostgreSQL and Oracle as the largest. I stop guessing by writing NULLS LAST or NULLS FIRST explicitly."
**Explain simply:**
- A NULL salary = 'not known'. It is not 0.
- In SQLite/MySQL/SQL Server (NULL = smallest): ASC puts NULLs first, DESC puts them last. In PostgreSQL/Oracle (NULL = largest): the reverse (from memory, only SQLite run here).
- `NULLS FIRST` / `NULLS LAST` is supported in PostgreSQL, Oracle, SQLite 3.30+; MySQL and SQL Server do not support it, so use `ORDER BY (col IS NULL), col` instead (from memory).
- All NULLs tie, so they share one rank.
**Example:** Two new joiners have no salary entered yet. A salary ranking should not put them at rank 1.
**Sample data:**
Table `emp_n`:
| emp_id | name | salary |
|---|---|---|
| 1 | Anil | 50000 |
| 2 | Bina | NULL |
| 3 | Chet | 60000 |
| 4 | Divya | NULL |
| 5 | Eshan | 40000 |
**SQL:**
```sql
SELECT name, salary,
       RANK() OVER (ORDER BY salary DESC)             AS rank_default,
       RANK() OVER (ORDER BY salary DESC NULLS LAST)  AS rank_nulls_last,
       RANK() OVER (ORDER BY salary DESC NULLS FIRST) AS rank_nulls_first
FROM emp_n ORDER BY emp_id;
```
**Output:**
| name | salary | rank_default | rank_nulls_last | rank_nulls_first |
|---|---|---|---|---|
| Anil | 50000 | 2 | 2 | 4 |
| Bina | NULL | 4 | 4 | 1 |
| Chet | 60000 | 1 | 1 | 3 |
| Divya | NULL | 4 | 4 | 1 |
| Eshan | 40000 | 3 | 3 | 5 |
**pandas equivalent:** (result checked equal to the SQL output)
```python
res = emp_n[["name", "salary"]].copy()
res["rank_default"] = res["salary"].rank(method="min", ascending=False, na_option="bottom").astype(int)
res["rank_nulls_last"] = res["salary"].rank(method="min", ascending=False, na_option="bottom").astype(int)
res["rank_nulls_first"] = res["salary"].rank(method="min", ascending=False, na_option="top").astype(int)
```
**Edge cases:** Bina and Divya (NULL) tie, so they share a rank and the next value jumps (RANK). Filter them out (`WHERE salary IS NOT NULL`) if they should not be ranked at all. In SQLite the default for DESC puts NULLs last, so default equals NULLS LAST here; PostgreSQL's default would equal NULLS FIRST.
**Likely follow-ups:**
- MySQL workaround for NULLS LAST? `ORDER BY salary IS NULL, salary DESC` (from memory).
- Do NULLs count in DENSE_RANK? They get their own rank value, all sharing it.
**Common mistakes:** Assuming NULLs are ignored by RANK, or that all databases sort NULLs the same way.

### Q33 ⭐⭐ 🟡 Write a query to find the top-selling product each month.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you aggregate first, then rank inside each month, in a CTE?
**Say this in the interview:** "First I total quantity per product per month. Then I rank products inside each month by that total, and keep rank 1. I use RANK so if two products tie for top, both show."
**Explain simply:**
- Step 1 (GROUP BY): one row per product-month with total quantity.
- Step 2 (window): `RANK() OVER (PARTITION BY month ORDER BY total_qty DESC)`.
- Step 3: outer query keeps `rnk = 1`.
- A *CTE* (WITH ... AS) is a named temporary result that makes the steps readable. 'Top-selling' = by quantity here; swap SUM(qty) for revenue if asked.
**Example:** January: Mouse 15, Keyboard 12, Laptop 4 so Mouse wins. February: Laptop 8 and Keyboard 8 tie for first.
**Sample data:**
Table `sales`:
| sale_id | product | sale_date | qty |
|---|---|---|---|
| 1 | Mouse | 2025-01-05 | 10 |
| 2 | Laptop | 2025-01-12 | 4 |
| 3 | Mouse | 2025-01-20 | 5 |
| 4 | Keyboard | 2025-01-25 | 12 |
| 5 | Laptop | 2025-02-03 | 8 |
| 6 | Keyboard | 2025-02-10 | 6 |
| 7 | Mouse | 2025-02-14 | 6 |
| 8 | Keyboard | 2025-02-21 | 2 |
**SQL:**
```sql
WITH monthly AS (
  SELECT strftime('%Y-%m', sale_date) AS month, product, SUM(qty) AS total_qty
  FROM sales
  GROUP BY strftime('%Y-%m', sale_date), product
), ranked AS (
  SELECT month, product, total_qty,
         RANK() OVER (PARTITION BY month ORDER BY total_qty DESC) AS rnk
  FROM monthly
)
SELECT month, product, total_qty
FROM ranked
WHERE rnk = 1
ORDER BY month, product;
```
Month extraction shown is SQLite (`strftime`); other dialects differ as listed in the follow-ups.
**Output:**
| month | product | total_qty |
|---|---|---|
| 2025-01 | Mouse | 15 |
| 2025-02 | Keyboard | 8 |
| 2025-02 | Laptop | 8 |
**pandas equivalent:** (result checked equal to the SQL output)
```python
s = sales.assign(month=sales["sale_date"].str[:7])
m = s.groupby(["month", "product"], as_index=False)["qty"].sum().rename(columns={"qty": "total_qty"})
m["rnk"] = m.groupby("month")["total_qty"].rank(method="min", ascending=False)
res = m[m["rnk"] == 1].sort_values(["month", "product"])[["month", "product", "total_qty"]].reset_index(drop=True)
```
**Edge cases:** Ties show both products (RANK); use ROW_NUMBER with a tie-break for exactly one. Months with no sales do not appear. NULL qty is ignored by SUM. Don't forget year: `%Y-%m` keeps January 2024 and 2025 apart.
**Likely follow-ups:**
- Month from date in other databases? PostgreSQL `DATE_TRUNC('month', d)` or `TO_CHAR(d,'YYYY-MM')`, MySQL `DATE_FORMAT(d,'%Y-%m')`, SQL Server `FORMAT(d,'yyyy-MM')` (not run here).
- Top 3 per month? Change to `rnk <= 3`.
**Common mistakes:** Ranking raw rows instead of monthly totals, or grouping by month number alone and mixing years.

### Q34 ⭐⭐ 🟡 Write a query to find the department with the highest total salary using a ranking function.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know you can use a window function over aggregated results, and can pick the max with RANK instead of LIMIT?
**Say this in the interview:** "I total salary per department, rank departments by that total descending in the same step, and keep rank 1. Using RANK means that if two departments tie for the highest payroll, both are returned, which LIMIT 1 would miss."
**Explain simply:**
- `GROUP BY dept` + `SUM(salary)` gives each department's payroll (salary bill).
- Window functions run after GROUP BY, so `RANK() OVER (ORDER BY SUM(salary) DESC)` is legal in the same SELECT.
- Wrap it in a subquery so you can filter on the rank.
- Simpler options exist (ORDER BY ... LIMIT 1) but the ranking version handles ties.
**Example:** Payroll: HR 110k, Sales 120k, IT 320k, so IT is the answer.
**Sample data:**
Table `emp`:
| emp_id | name | dept | salary | hire_date |
|---|---|---|---|---|
| 1 | Asha | HR | 50000 | 2019-03-01 |
| 2 | Bala | HR | 60000 | 2021-07-15 |
| 3 | Dev | IT | 90000 | 2020-05-20 |
| 4 | Esha | IT | 80000 | 2017-11-02 |
| 5 | Farid | IT | 80000 | 2022-02-14 |
| 6 | Gita | IT | 70000 | 2023-01-09 |
| 7 | Isha | Sales | 55000 | 2019-06-30 |
| 8 | Jay | Sales | 65000 | 2024-03-18 |
**SQL:**
```sql
SELECT dept, total_salary
FROM (
  SELECT dept, SUM(salary) AS total_salary,
         RANK() OVER (ORDER BY SUM(salary) DESC) AS rnk
  FROM emp
  GROUP BY dept
) t
WHERE rnk = 1;
```
**Output:**
| dept | total_salary |
|---|---|
| IT | 320000 |
**pandas equivalent:** (result checked equal to the SQL output)
```python
t = emp.groupby("dept", as_index=False)["salary"].sum().rename(columns={"salary": "total_salary"})
t["rnk"] = t["total_salary"].rank(method="min", ascending=False)
res = t[t["rnk"] == 1][["dept", "total_salary"]].reset_index(drop=True)
```
**Edge cases:** Ties return all tied departments. NULL salaries are skipped by SUM (a department of all NULLs sums to NULL and ranks per dialect). Empty table returns no rows.
**Likely follow-ups:**
- Without window functions? `ORDER BY total_salary DESC LIMIT 1` (MySQL/PostgreSQL/SQLite), `SELECT TOP 1 ... ORDER BY` (SQL Server), `FETCH FIRST 1 ROW ONLY` (standard/PostgreSQL/Oracle); ties are lost.
- `FETCH FIRST 1 ROW WITH TIES` keeps ties in PostgreSQL 13+/Oracle/SQL Server TOP WITH TIES (from memory, not run here).
**Common mistakes:** Using MAX(SUM(salary)) (not allowed) or selecting dept with a bare MAX in a non-strict engine and getting a random department.

### Q35 ⭐⭐ 🟡 Write a query to find the top 2 hiring sources by number of hires in each year.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you group by year and source, count, then take top N per year?
**Say this in the interview:** "I count hires by year and source, rank sources inside each year by that count, and keep the top 2. I use ROW_NUMBER with source name as a tie-break so exactly two come back per year; with RANK I would keep ties."
**Explain simply:**
- `hires` has one row per hire with the channel (LinkedIn, Referral, Agency) it came from.
- GROUP BY year and source gives hires per source per year.
- `ROW_NUMBER() OVER (PARTITION BY year ORDER BY hires DESC, source)` ranks sources within each year.
- Keep `rn <= 2`. Year comes from the date (`strftime('%Y', hire_date)` in SQLite).
**Example:** 2023: LinkedIn 2, then Agency 1 and Referral 1 tie; Agency is kept by the alphabetical tie-break. 2024: Referral 3, LinkedIn 1.
**Sample data:**
Table `hires`:
| hire_id | source | hire_date |
|---|---|---|
| 1 | LinkedIn | 2023-02-10 |
| 2 | LinkedIn | 2023-05-04 |
| 3 | Referral | 2023-08-21 |
| 4 | Agency | 2023-11-02 |
| 5 | Referral | 2024-01-15 |
| 6 | Referral | 2024-03-09 |
| 7 | Referral | 2024-07-30 |
| 8 | LinkedIn | 2024-09-12 |
**SQL:**
```sql
WITH yearly AS (
  SELECT strftime('%Y', hire_date) AS yr, source, COUNT(*) AS hires
  FROM hires
  GROUP BY strftime('%Y', hire_date), source
), ranked AS (
  SELECT yr, source, hires,
         ROW_NUMBER() OVER (PARTITION BY yr ORDER BY hires DESC, source) AS rn
  FROM yearly
)
SELECT yr, source, hires, rn
FROM ranked
WHERE rn <= 2
ORDER BY yr, rn;
```
**Output:**
| yr | source | hires | rn |
|---|---|---|---|
| 2023 | LinkedIn | 2 | 1 |
| 2023 | Agency | 1 | 2 |
| 2024 | Referral | 3 | 1 |
| 2024 | LinkedIn | 1 | 2 |
**pandas equivalent:** (result checked equal to the SQL output)
```python
h = hires.assign(yr=hires["hire_date"].str[:4])
y = h.groupby(["yr", "source"], as_index=False).size().rename(columns={"size": "hires"})
y = y.sort_values(["yr", "hires", "source"], ascending=[True, False, True])
y["rn"] = y.groupby("yr").cumcount() + 1
res = y[y["rn"] <= 2].reset_index(drop=True)
```
**Edge cases:** Ties at 2nd place: ROW_NUMBER picks one by the tie-break, RANK keeps all (2023 would then return 3 rows). A year with only one source returns one row. NULL source forms its own group; filter it out if meaningless.
**Likely follow-ups:**
- Keep ties? Use RANK() and `rnk <= 2`.
- Year in other dialects? PostgreSQL `EXTRACT(YEAR FROM hire_date)`, MySQL/SQL Server `YEAR(hire_date)` (not run here).
**Common mistakes:** Counting hires across all years (forgetting PARTITION BY year), or putting COUNT(*) and the window in one SELECT without grouping first.

### Q36 ⭐⭐ 🟡 Can you use two window functions with different PARTITION BY in one query? Give an example.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know each window function has its own OVER clause, so partitions can differ in one query?
**Say this in the interview:** "Yes. Every window function carries its own OVER clause, so I can have one partitioned by department and another over the whole company in the same SELECT, with no joins."
**Explain simply:**
- Window functions are independent of each other; each defines its own partition and order.
- The database computes each separately and lines the results up on the same row.
- Typical use: compare an employee to their department average AND to the company average.
- Under the hood the engine may sort the data more than once, so very many different windows can cost performance.
**Example:** Dev earns 90k: dept average (IT) 80k, company average 68,750, so +10k vs dept and +21,250 vs company.
**Sample data:**
Table `emp`:
| emp_id | name | dept | salary | hire_date |
|---|---|---|---|---|
| 1 | Asha | HR | 50000 | 2019-03-01 |
| 2 | Bala | HR | 60000 | 2021-07-15 |
| 3 | Dev | IT | 90000 | 2020-05-20 |
| 4 | Esha | IT | 80000 | 2017-11-02 |
| 5 | Farid | IT | 80000 | 2022-02-14 |
| 6 | Gita | IT | 70000 | 2023-01-09 |
| 7 | Isha | Sales | 55000 | 2019-06-30 |
| 8 | Jay | Sales | 65000 | 2024-03-18 |
**SQL:**
```sql
SELECT name, dept, salary,
       AVG(salary) OVER (PARTITION BY dept)                  AS dept_avg,
       AVG(salary) OVER ()                                   AS company_avg,
       RANK()      OVER (PARTITION BY dept ORDER BY salary DESC) AS dept_rank,
       salary - AVG(salary) OVER (PARTITION BY dept)         AS vs_dept_avg
FROM emp
ORDER BY dept, dept_rank, name;
```
**Output:**
| name | dept | salary | dept_avg | company_avg | dept_rank | vs_dept_avg |
|---|---|---|---|---|---|---|
| Bala | HR | 60000 | 55000 | 68750 | 1 | 5000 |
| Asha | HR | 50000 | 55000 | 68750 | 2 | -5000 |
| Dev | IT | 90000 | 80000 | 68750 | 1 | 10000 |
| Esha | IT | 80000 | 80000 | 68750 | 2 | 0 |
| Farid | IT | 80000 | 80000 | 68750 | 2 | 0 |
| Gita | IT | 70000 | 80000 | 68750 | 4 | -10000 |
| Jay | Sales | 65000 | 60000 | 68750 | 1 | 5000 |
| Isha | Sales | 55000 | 60000 | 68750 | 2 | -5000 |
**pandas equivalent:** (result checked equal to the SQL output)
```python
res = emp[["name", "dept", "salary"]].copy()
res["dept_avg"] = res.groupby("dept")["salary"].transform("mean")
res["company_avg"] = res["salary"].mean()
res["dept_rank"] = res.groupby("dept")["salary"].rank(method="min", ascending=False).astype(int)
res["vs_dept_avg"] = res["salary"] - res["dept_avg"]
res = res.sort_values(["dept", "dept_rank", "name"]).reset_index(drop=True)
```
**Edge cases:** Ties and NULLs behave as in each function (AVG ignores NULLs, ranks tie). If several windows share the same definition, name it once with `WINDOW w AS (PARTITION BY dept)` where supported (from memory: PostgreSQL, MySQL 8, SQLite, not SQL Server).
**Likely follow-ups:**
- Performance concern? Windows with the same PARTITION BY/ORDER BY can share one sort; different ones need extra sorts.
- Can I nest a window inside another? Not directly; use a CTE/subquery.
**Common mistakes:** Thinking all window functions in a SELECT must share one partition, and joining to a GROUP BY subquery unnecessarily.

### Q37 ⭐⭐ 🟡 What is the difference between using ROW_NUMBER() and LIMIT/TOP for 'top 1 per group'?
**Asked at:** commonly asked (no company-specific report found); prep sources list top-N per department among the most frequent window-function questions
**What the interviewer is checking:** Whether you know that LIMIT/TOP cuts the whole result, not each group, and that ROW_NUMBER numbers rows inside each group.
**Say this in the interview:** LIMIT 1 or TOP 1 gives me one row for the whole table. For top 1 per group I number the rows inside each group with ROW_NUMBER and keep number 1.
**Explain simply:**
- **LIMIT / TOP** (MySQL, PostgreSQL, SQLite use LIMIT; SQL Server uses TOP; the standard form is FETCH FIRST n ROWS ONLY) trims the final result to n rows in total. It has no idea about groups.
- **ROW_NUMBER()** is a *window function*: a calculation that looks at a set of related rows without collapsing them. With PARTITION BY dept it restarts the count 1, 2, 3... for every department.
- Filtering on that number (rn = 1) gives one row per department. You need a CTE or subquery for this, because WHERE cannot see a window result directly (see Q41).
- ROW_NUMBER picks exactly one row per group even when salaries tie, so add a tie-breaker column or the winner is arbitrary.
**Example:** Four departments, we want each department's best-paid person. LIMIT 1 returns only Kiran (120,000) for the whole company. ROW_NUMBER returns Meera (HR), Kiran (Eng), Isha (Sales), Om (Support).
**Sample data:**

`employees`

| emp_id | name | dept | manager_id | salary | rating |
|---|---|---|---|---|---|
| 1 | Meera | HR | NULL | 90000 | 4 |
| 2 | Ravi | HR | 1 | 60000 | 5 |
| 3 | Sana | HR | 1 | 60000 | 3 |
| 4 | Tom | HR | 1 | 45000 | 4 |
| 5 | Kiran | Eng | NULL | 120000 | 4 |
| 6 | Leena | Eng | 5 | 95000 | 5 |
| 7 | Arjun | Eng | 5 | 95000 | 4 |
| 8 | Divya | Eng | 5 | 70000 | 3 |
| 9 | Farah | Eng | 5 | 48000 | 5 |
| 10 | Gopal | Sales | NULL | 46000 | 4 |
| 11 | Isha | Sales | 10 | 52000 | 5 |
| 12 | Jay | Sales | 10 | 52000 | 3 |
| 13 | Neha | Sales | 10 | 40000 | 4 |
| 14 | Om | Support | NULL | 44000 | 3 |
| 15 | Pia | Support | 14 | 38000 | 4 |
| 16 | Quinn | Support | 14 | 38000 | 5 |
| 17 | Ujwal | Eng | 5 | 85000 | 4 |
| 18 | Vik | Eng | 5 | 60000 | 3 |
**SQL:**
```sql
-- LIMIT 1: one row for the whole table
SELECT dept, name, salary FROM employees ORDER BY salary DESC LIMIT 1;

-- ROW_NUMBER: one row per department
WITH ranked AS (
  SELECT dept, name, salary,
         ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC, emp_id) AS rn
  FROM employees
)
SELECT dept, name, salary FROM ranked WHERE rn = 1 ORDER BY dept;
```
**Output:**

LIMIT 1: one row for the whole table:

| dept | name | salary |
|---|---|---|
| Eng | Kiran | 120000 |

ROW_NUMBER: one row per department:

| dept | name | salary |
|---|---|---|
| Eng | Kiran | 120000 |
| HR | Meera | 90000 |
| Sales | Isha | 52000 |
| Support | Om | 44000 |
**pandas equivalent:**
```python
import pandas as pd
# emp = employees table as a DataFrame
res = (emp.sort_values(['dept', 'salary', 'emp_id'], ascending=[True, False, True])
          .groupby('dept').head(1)[['dept', 'name', 'salary']])
# result matches the SQL Output above (checked by running both)
```
**Edge cases:** Ties: if two people share the top salary, ROW_NUMBER keeps only one (decided by the tie-breaker emp_id here). Use RANK() = 1 if you want all tied people. NULL salaries sort first in DESC order in PostgreSQL/Oracle and last in MySQL/SQLite/SQL Server, so filter them out or use NULLS LAST (PostgreSQL, SQLite 3.30+; not run here for other engines).
**Likely follow-ups:**
1. Can you do it in SQL Server with TOP? Yes, `SELECT TOP 1 WITH TIES ... ORDER BY ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC)` is a known trick (not run here, from memory).
2. Which is faster? On a small table nobody notices; on a big one the window sort is usually fine, and a LATERAL / CROSS APPLY with an index can beat it (Q53).
**Common mistakes:** Writing `GROUP BY dept ... LIMIT 1` and expecting one row per group; selecting name next to MAX(salary) without a window (MySQL may allow it and return a wrong name); forgetting a tie-breaker so results change between runs.

### Q38 ⭐⭐ 🟡 How do you display ROW_NUMBER, RANK and DENSE_RANK side by side in one query?
**Asked at:** commonly asked (no company-specific report found); prep sources list top-N per department among the most frequent window-function questions
**What the interviewer is checking:** Whether you can state the tie behaviour of the three ranking functions and show it in one query.
**Say this in the interview:** I just put all three in the SELECT list with the same OVER clause. ROW_NUMBER never repeats, RANK repeats on ties and skips numbers, DENSE_RANK repeats on ties and skips nothing.
**Explain simply:**
- Each function gets its own column, all using `OVER (PARTITION BY dept ORDER BY salary DESC)`: rank inside each department, highest salary first.
- **ROW_NUMBER**: 1,2,3,4 always, even for equal salaries (the order among equals is arbitrary unless you add a tie-breaker).
- **RANK**: equal salaries share a number, then the next number jumps (1,1,3).
- **DENSE_RANK**: equal salaries share a number, the next number is just +1 (1,1,2).
**Example:** In Sales, Isha and Jay both earn 52,000. Both are rank 1. Gopal (46,000) is rank 3 with RANK but rank 2 with DENSE_RANK.
**Sample data:**

`employees`

| emp_id | name | dept | salary |
|---|---|---|---|
| 1 | Meera | HR | 90000 |
| 2 | Ravi | HR | 60000 |
| 3 | Sana | HR | 60000 |
| 4 | Tom | HR | 45000 |
| 10 | Gopal | Sales | 46000 |
| 11 | Isha | Sales | 52000 |
| 12 | Jay | Sales | 52000 |
| 13 | Neha | Sales | 40000 |
**SQL:**
```sql
SELECT dept, name, salary,
       ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC, emp_id) AS row_num,
       RANK()       OVER (PARTITION BY dept ORDER BY salary DESC)         AS rnk,
       DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC)         AS dense_rnk
FROM employees
WHERE dept IN ('Sales', 'HR')
ORDER BY dept, salary DESC, emp_id;
```
**Output:**

| dept | name | salary | row_num | rnk | dense_rnk |
|---|---|---|---|---|---|
| HR | Meera | 90000 | 1 | 1 | 1 |
| HR | Ravi | 60000 | 2 | 2 | 2 |
| HR | Sana | 60000 | 3 | 2 | 2 |
| HR | Tom | 45000 | 4 | 4 | 3 |
| Sales | Isha | 52000 | 1 | 1 | 1 |
| Sales | Jay | 52000 | 2 | 1 | 1 |
| Sales | Gopal | 46000 | 3 | 3 | 2 |
| Sales | Neha | 40000 | 4 | 4 | 3 |
**pandas equivalent:**
```python
import pandas as pd
d = emp[emp['dept'].isin(['Sales', 'HR'])].sort_values(['dept', 'emp_id']).copy()
g = d.groupby('dept')['salary']
d['row_num'] = g.rank(method='first', ascending=False).astype(int)
d['rnk'] = g.rank(method='min', ascending=False).astype(int)
d['dense_rnk'] = g.rank(method='dense', ascending=False).astype(int)
res = d.sort_values(['dept', 'row_num'])[['dept', 'name', 'salary', 'row_num', 'rnk', 'dense_rnk']]
# result matches the SQL Output above (checked by running both)
```
**Edge cases:** Without a tie-breaker, ROW_NUMBER among equal salaries can change between runs or engines. NULLs in the ORDER BY column are treated as equal to each other, so they tie. An empty table returns no rows.
**Likely follow-ups:**
1. When would you choose each? ROW_NUMBER for exactly N rows or de-duplication, RANK when ties should share a place and gaps are acceptable, DENSE_RANK for 'second highest salary' (Q47).
**Common mistakes:** Assuming ROW_NUMBER and RANK give the same answer when there are no visible ties (they do only if values are unique); forgetting PARTITION BY and ranking the whole company.

### Q39 ⭐⭐ 🟡 How do you number rows 1..n in a table without a ranking-specific column (a simple serial number)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know ROW_NUMBER can act as a plain serial number and that you must still define an order.
**Say this in the interview:** I use ROW_NUMBER() OVER (ORDER BY some_column). It does not need a partition, and I pick a stable order such as the primary key so the serial numbers are repeatable.
**Explain simply:**
- A *serial number* (S.No) is just 1, 2, 3 down the result. ROW_NUMBER with no PARTITION BY numbers the whole result in one go.
- The ORDER BY inside OVER decides who gets 1. Use a unique column such as emp_id so the numbering is the same every time.
- SQL Server requires ORDER BY inside OVER for ROW_NUMBER; if you truly do not care, `ORDER BY (SELECT NULL)` is the usual trick (not run here, from memory).
- A table has no natural row order in SQL. Do not rely on the order rows were inserted.
**Example:** An HR report listing employees as 1, 2, 3 ... so managers can refer to 'row 5'.
**Sample data:**

`employees`

| emp_id | name | dept |
|---|---|---|
| 1 | Meera | HR |
| 2 | Ravi | HR |
| 3 | Sana | HR |
| 4 | Tom | HR |
| 5 | Kiran | Eng |
| 6 | Leena | Eng |
**SQL:**
```sql
SELECT ROW_NUMBER() OVER (ORDER BY emp_id) AS s_no, name, dept
FROM employees
ORDER BY s_no
LIMIT 6;
```
**Output:**

| s_no | name | dept |
|---|---|---|
| 1 | Meera | HR |
| 2 | Ravi | HR |
| 3 | Sana | HR |
| 4 | Tom | HR |
| 5 | Kiran | Eng |
| 6 | Leena | Eng |
**pandas equivalent:**
```python
import pandas as pd
d = emp.sort_values('emp_id').reset_index(drop=True)
d['s_no'] = d.index + 1
res = d[['s_no', 'name', 'dept']].head(6)
# result matches the SQL Output above (checked by running both)
```
**Edge cases:** If you ORDER BY a column with duplicates, the numbering among duplicates is arbitrary. SQLite also has a hidden `rowid`, and MySQL 5.7 users used session variables (`@n := @n + 1`), but ROW_NUMBER (MySQL 8+) is the clean way (version facts from memory). The LIMIT clause is dialect-specific: TOP 6 in SQL Server, FETCH FIRST 6 ROWS ONLY in standard SQL/Oracle/PostgreSQL (not run here).
**Likely follow-ups:**
1. How is it different from an auto-increment id? An id is stored and fixed; ROW_NUMBER is computed per query and changes if the filter or order changes.
**Common mistakes:** Using the stored emp_id as the serial number (it has gaps after deletes); omitting ORDER BY inside OVER in SQL Server (error).

### Q40 ⭐⭐ 🟡 Write a query to find employees whose salary is the highest in their department and above 50,000.
**Asked at:** commonly asked (no company-specific report found); prep sources list top-N per department among the most frequent window-function questions
**What the interviewer is checking:** Combining 'top per group' with an extra filter, and noticing how ties should behave.
**Say this in the interview:** I rank salaries inside each department with RANK, keep rank 1 in a CTE, then apply the salary above 50,000 filter on the outside. RANK keeps people who tie for the top.
**Explain simply:**
- Step 1: `RANK() OVER (PARTITION BY dept ORDER BY salary DESC)` labels the best-paid people in each department as 1.
- Step 2: wrap it in a CTE (a named temporary result you can query again) and keep `rk = 1 AND salary > 50000`.
- Order of operations matters: the Support department's top earner (Om, 44,000) is the best in the department but fails the 50,000 test, so Support disappears.
- For a salary threshold, filtering before or after ranking gives the same top row. For other filters (for example only 'full-time'), filtering first would change who is rank 1, so think about what the question means.
**Example:** Eng top earner Kiran 120,000, HR Meera 90,000, Sales Isha and Jay both 52,000 (tie), Support Om 44,000 is dropped.
**Sample data:**

`employees`

| emp_id | name | dept | salary |
|---|---|---|---|
| 1 | Meera | HR | 90000 |
| 2 | Ravi | HR | 60000 |
| 3 | Sana | HR | 60000 |
| 4 | Tom | HR | 45000 |
| 5 | Kiran | Eng | 120000 |
| 6 | Leena | Eng | 95000 |
| 7 | Arjun | Eng | 95000 |
| 8 | Divya | Eng | 70000 |
| 9 | Farah | Eng | 48000 |
| 10 | Gopal | Sales | 46000 |
| 11 | Isha | Sales | 52000 |
| 12 | Jay | Sales | 52000 |
| 13 | Neha | Sales | 40000 |
| 14 | Om | Support | 44000 |
| 15 | Pia | Support | 38000 |
| 16 | Quinn | Support | 38000 |
| 17 | Ujwal | Eng | 85000 |
| 18 | Vik | Eng | 60000 |
**SQL:**
```sql
WITH ranked AS (
  SELECT name, dept, salary,
         RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rk
  FROM employees
)
SELECT name, dept, salary
FROM ranked
WHERE rk = 1 AND salary > 50000
ORDER BY dept, name;
```
**Output:**

| name | dept | salary |
|---|---|---|
| Kiran | Eng | 120000 |
| Meera | HR | 90000 |
| Isha | Sales | 52000 |
| Jay | Sales | 52000 |
**pandas equivalent:**
```python
import pandas as pd
d = emp.copy()
d['rk'] = d.groupby('dept')['salary'].rank(method='min', ascending=False)
res = d[(d['rk'] == 1) & (d['salary'] > 50000)][['name', 'dept', 'salary']]
# result matches the SQL Output above (checked by running both)
```
**Edge cases:** Ties: RANK keeps both Isha and Jay; use ROW_NUMBER with a tie-breaker if you need exactly one per department. NULL salary: NULL > 50000 is unknown, so those rows are dropped. If no one qualifies, the result is empty.
**Likely follow-ups:**
1. How do you get exactly one per department? Swap RANK for ROW_NUMBER and add a tie-breaker such as emp_id.
**Common mistakes:** Putting `rk = 1` in the same WHERE as the window function (not allowed); using `salary = MAX(salary)` with GROUP BY and losing the name column.

### Q41 ⭐⭐ 🟡 How do you use a window function inside a subquery, and why do you need to wrap it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the order in which SQL evaluates clauses, and why window results cannot be used in WHERE?
**Say this in the interview:** Window functions are calculated after WHERE, GROUP BY and HAVING, so WHERE has not got the value yet. I compute the window in an inner query or CTE, and filter on that column in the outer query.
**Explain simply:**
- SQL logically runs FROM, then WHERE, then GROUP BY, HAVING, then window functions, then SELECT's output, then ORDER BY. WHERE comes too early to see a window result.
- Trying it gives an error. Real message from SQLite: `misuse of window function RANK()`. Other engines word it differently but all refuse (QUALIFY, in Snowflake/BigQuery/DuckDB/Teradata, is a shortcut that filters on a window result directly; not run here, from memory).
- **Wrapping** = put the query with the window in a subquery (`FROM (...) t`) or a CTE (`WITH t AS (...)`), then the outer WHERE sees the window column like any normal column.
- A subquery in FROM needs an alias in most databases (`) AS t`).
**Example:** 'Show employees who are rank 1 or 2 by salary in their department.' Rank first inside, filter outside.
**Sample data:**

`employees`

| emp_id | name | dept | salary |
|---|---|---|---|
| 10 | Gopal | Sales | 46000 |
| 11 | Isha | Sales | 52000 |
| 12 | Jay | Sales | 52000 |
| 13 | Neha | Sales | 40000 |
| 14 | Om | Support | 44000 |
| 15 | Pia | Support | 38000 |
| 16 | Quinn | Support | 38000 |
**SQL:**
```sql
-- Wrong: window function in WHERE (errors, not shown as output)
-- SELECT name, dept FROM employees WHERE RANK() OVER (PARTITION BY dept ORDER BY salary DESC) = 1
-- ERROR

-- Right, with a subquery
SELECT name, dept, salary
FROM (
  SELECT name, dept, salary,
         DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rk
  FROM employees
) AS t
WHERE rk <= 2 AND dept IN ('Sales', 'Support')
ORDER BY dept, salary DESC, name;

-- Same thing with a CTE
WITH t AS (
  SELECT name, dept, salary,
         DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rk
  FROM employees
)
SELECT name, dept, salary FROM t
WHERE rk <= 2 AND dept IN ('Sales', 'Support')
ORDER BY dept, salary DESC, name;
```
**Output:**

Right, with a subquery:

| name | dept | salary |
|---|---|---|
| Isha | Sales | 52000 |
| Jay | Sales | 52000 |
| Gopal | Sales | 46000 |
| Om | Support | 44000 |
| Pia | Support | 38000 |
| Quinn | Support | 38000 |

Same thing with a CTE:

| name | dept | salary |
|---|---|---|
| Isha | Sales | 52000 |
| Jay | Sales | 52000 |
| Gopal | Sales | 46000 |
| Om | Support | 44000 |
| Pia | Support | 38000 |
| Quinn | Support | 38000 |
**pandas equivalent:**
```python
import pandas as pd
d = emp.copy()
d['rk'] = d.groupby('dept')['salary'].rank(method='dense', ascending=False)
res = d[(d['rk'] <= 2) & d['dept'].isin(['Sales', 'Support'])][['name', 'dept', 'salary']]
# result matches the SQL Output above (checked by running both)
```
**Edge cases:** Filtering `dept` in the outer query works but the inner query still ranks every department; filter inside as well when the table is big. Ties: DENSE_RANK <= 2 can return more than 2 people per department (Sales has 3 here).
**Likely follow-ups:**
1. Is there a shortcut? QUALIFY in Snowflake, BigQuery, Teradata and DuckDB (not in SQL Server, PostgreSQL, MySQL; from memory).
**Common mistakes:** Putting the window function in WHERE, GROUP BY or HAVING; forgetting the alias on the subquery; thinking a column alias defined in SELECT can be used in WHERE of the same query (it cannot in most engines).

### Q42 ⭐⭐ 🟡 What is PERCENT_RANK() and how is it different from RANK()?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Understanding that PERCENT_RANK scales rank onto 0 to 1 and uses the RANK formula, not a count of rows.
**Say this in the interview:** RANK gives a position like 1, 2, 3. PERCENT_RANK turns that position into a fraction between 0 and 1 using (rank - 1) divided by (rows - 1), so the top row is 0 and the bottom row is 1.
**Explain simply:**
- `PERCENT_RANK() = (RANK - 1) / (number of rows in the partition - 1)`. A partition is the group defined by PARTITION BY.
- It answers 'what fraction of the other rows sit above this one?' With ORDER BY salary DESC, 0 is the best-paid and 1 is the lowest.
- A group with one row gets 0 (avoiding division by zero).
- Ties share the same value, just like RANK, because it is built on RANK.
**Example:** Sales has 4 people. Isha and Jay (rank 1) get 0. Gopal (rank 3) gets (3-1)/(4-1) = 0.667. Neha (rank 4) gets 1.
**Sample data:**

`employees`

| emp_id | name | dept | salary |
|---|---|---|---|
| 10 | Gopal | Sales | 46000 |
| 11 | Isha | Sales | 52000 |
| 12 | Jay | Sales | 52000 |
| 13 | Neha | Sales | 40000 |
| 14 | Om | Support | 44000 |
| 15 | Pia | Support | 38000 |
| 16 | Quinn | Support | 38000 |
**SQL:**
```sql
SELECT dept, name, salary,
       RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk,
       ROUND(PERCENT_RANK() OVER (PARTITION BY dept ORDER BY salary DESC), 3) AS pct_rank
FROM employees
WHERE dept IN ('Sales', 'Support')
ORDER BY dept, salary DESC, name;
```
**Output:**

| dept | name | salary | rnk | pct_rank |
|---|---|---|---|---|
| Sales | Isha | 52000 | 1 | 0 |
| Sales | Jay | 52000 | 1 | 0 |
| Sales | Gopal | 46000 | 3 | 0.667 |
| Sales | Neha | 40000 | 4 | 1 |
| Support | Om | 44000 | 1 | 0 |
| Support | Pia | 38000 | 2 | 0.5 |
| Support | Quinn | 38000 | 2 | 0.5 |
**pandas equivalent:**
```python
import pandas as pd
d = emp[emp['dept'].isin(['Sales', 'Support'])].copy()
g = d.groupby('dept')['salary']
d['rnk'] = g.rank(method='min', ascending=False).astype(int)
n = g.transform('size')
d['pct_rank'] = ((d['rnk'] - 1) / (n - 1)).round(3)
res = d.sort_values(['dept', 'salary', 'name'], ascending=[True, False, True])[['dept', 'name', 'salary', 'rnk', 'pct_rank']]
# result matches the SQL Output above (checked by running both)
```
**Edge cases:** One-row partitions give 0, not NULL or error. NULLs in ORDER BY sort together and tie. If the last rows tie, they share a value below 1 (the value 1 needs a unique last row). For 'top 10 percent' CUME_DIST is often the better tool (Q43).
**Likely follow-ups:**
1. How is it different from CUME_DIST? CUME_DIST = rows up to and including the current value divided by total rows, so it ranges above 0 up to exactly 1.
**Common mistakes:** Thinking PERCENT_RANK is a percentage of salary or of total; believing the first row is 1 (it is 0 for ascending or descending); forgetting it is built on RANK so ties repeat.

### Q43 ⭐⭐ 🟡 Write a query to rank customers by total spend and show the top 10 percent.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Aggregate first (total per customer), then rank, then pick a percentage cut-off correctly including ties.
**Say this in the interview:** First I total the spend per customer with GROUP BY. Then on that result I use CUME_DIST ordered by spend descending, and keep customers where it is 0.10 or less. That gives the top 10 percent, ties included.
**Explain simply:**
- You cannot rank the raw order lines: one customer has several orders. So step 1 is `SUM(amount) ... GROUP BY customer`.
- **CUME_DIST()** = share of customers whose spend is at least as big as this one. Ordered DESC, a value of 0.10 or less means 'in the top 10 percent'.
- **NTILE(10)** splits customers into 10 equal buckets; bucket 1 is the top 10 percent. It is simple, but it cuts through ties arbitrarily.
- With 20 customers, 10 percent is 2 customers.
**Example:** HR wants the top 10 percent of employees by overtime pay: same shape, with customers replaced by employees.
**Sample data:**

`orders`

| order_id | customer | amount |
|---|---|---|
| 1 | C01 | 140 |
| 2 | C01 | 165 |
| 3 | C02 | 280 |
| 4 | C02 | 190 |
| 5 | C02 | 30 |
| 6 | C03 | 320 |
**SQL:**
```sql
WITH totals AS (
  SELECT customer, SUM(amount) AS total_spend
  FROM orders
  GROUP BY customer
),
ranked AS (
  SELECT customer, total_spend,
         RANK()      OVER (ORDER BY total_spend DESC) AS spend_rank,
         CUME_DIST() OVER (ORDER BY total_spend DESC) AS cume,
         NTILE(10)   OVER (ORDER BY total_spend DESC) AS decile
  FROM totals
)
SELECT customer, total_spend, spend_rank, cume, decile
FROM ranked
WHERE cume <= 0.10
ORDER BY spend_rank;
```
**Output:**

| customer | total_spend | spend_rank | cume | decile |
|---|---|---|---|---|
| C20 | 3500 | 1 | 0.05 | 1 |
| C18 | 3240 | 2 | 0.1 | 1 |
**pandas equivalent:**
```python
import pandas as pd
t = orders.groupby('customer', as_index=False)['amount'].sum().rename(columns={'amount': 'total_spend'})
t['spend_rank'] = t['total_spend'].rank(method='min', ascending=False).astype(int)
t['cume'] = t['total_spend'].rank(method='max', ascending=False) / len(t)
t = t.sort_values(['total_spend', 'customer'], ascending=[False, True]).reset_index(drop=True)
t['decile'] = t.index * 10 // len(t) + 1   # NTILE(10) when 20 rows divide evenly
res = t[t['cume'] <= 0.10][['customer', 'total_spend', 'spend_rank', 'cume', 'decile']]
# result matches the SQL Output above (checked by running both)
```
**Edge cases:** Ties at the cut-off: CUME_DIST keeps all tied customers, so you may return more than 10 percent; NTILE splits ties arbitrarily. If the row count is not divisible by 10, NTILE makes the first buckets one row larger. Floating-point: compare with `<= 0.10` carefully (2/20 is exactly 0.1 here). A customer with NULL spend sorts to the top in some engines, so filter NULLs.
**Likely follow-ups:**
1. How would you get the top 10 percent with a fixed row count, without window functions? `ORDER BY total DESC LIMIT (SELECT COUNT(*)*0.1 ...)` works in some engines only; in SQL Server use `TOP 10 PERCENT` (not run here).
**Common mistakes:** Ranking order lines instead of customers; using `LIMIT 10` thinking it means 10 percent; using PERCENT_RANK < 0.1, which gives a different (and off-by-one-looking) cut.

### Q44 ⭐⭐ 🟡 How would you rank employees by performance rating within each manager's team?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Partitioning by manager (a different grouping column) and handling ties and the top boss with no manager.
**Say this in the interview:** I partition by manager_id so each manager's team is ranked separately, order by rating descending, and use a second sort column like salary as a tie-breaker. People with no manager are left out.
**Explain simply:**
- `manager_id` points to the boss's emp_id. All employees with the same manager_id form one team, so `PARTITION BY manager_id` ranks inside each team.
- Rating is 1 to 5 (5 best), so `ORDER BY rating DESC`. Many people share a rating, so I show plain RANK (ties share a number) and a version with salary as a tie-breaker.
- Top bosses have manager_id NULL. NULLs would form one big group of their own, so I filter them out with `WHERE manager_id IS NOT NULL`.
**Example:** Manager 5 (Kiran) has six reports. Leena and Farah both have rating 5. By rating alone they tie for 1; with salary as tie-breaker Leena (95,000) is 1 and Farah (48,000) is 2.
**Sample data:**

`employees`

| emp_id | name | dept | manager_id | salary | rating |
|---|---|---|---|---|---|
| 1 | Meera | HR | NULL | 90000 | 4 |
| 2 | Ravi | HR | 1 | 60000 | 5 |
| 3 | Sana | HR | 1 | 60000 | 3 |
| 4 | Tom | HR | 1 | 45000 | 4 |
| 5 | Kiran | Eng | NULL | 120000 | 4 |
| 6 | Leena | Eng | 5 | 95000 | 5 |
| 7 | Arjun | Eng | 5 | 95000 | 4 |
| 8 | Divya | Eng | 5 | 70000 | 3 |
| 9 | Farah | Eng | 5 | 48000 | 5 |
| 10 | Gopal | Sales | NULL | 46000 | 4 |
| 11 | Isha | Sales | 10 | 52000 | 5 |
| 12 | Jay | Sales | 10 | 52000 | 3 |
| 13 | Neha | Sales | 10 | 40000 | 4 |
| 14 | Om | Support | NULL | 44000 | 3 |
| 15 | Pia | Support | 14 | 38000 | 4 |
| 16 | Quinn | Support | 14 | 38000 | 5 |
| 17 | Ujwal | Eng | 5 | 85000 | 4 |
| 18 | Vik | Eng | 5 | 60000 | 3 |
**SQL:**
```sql
SELECT manager_id, name, rating, salary,
       RANK() OVER (PARTITION BY manager_id ORDER BY rating DESC)                 AS rating_rank,
       RANK() OVER (PARTITION BY manager_id ORDER BY rating DESC, salary DESC)    AS rank_with_tiebreak
FROM employees
WHERE manager_id IS NOT NULL
ORDER BY manager_id, rating_rank, rank_with_tiebreak;
```
**Output:**

| manager_id | name | rating | salary | rating_rank | rank_with_tiebreak |
|---|---|---|---|---|---|
| 1 | Ravi | 5 | 60000 | 1 | 1 |
| 1 | Tom | 4 | 45000 | 2 | 2 |
| 1 | Sana | 3 | 60000 | 3 | 3 |
| 5 | Leena | 5 | 95000 | 1 | 1 |
| 5 | Farah | 5 | 48000 | 1 | 2 |
| 5 | Arjun | 4 | 95000 | 3 | 3 |
| 5 | Ujwal | 4 | 85000 | 3 | 4 |
| 5 | Divya | 3 | 70000 | 5 | 5 |
| 5 | Vik | 3 | 60000 | 5 | 6 |
| 10 | Isha | 5 | 52000 | 1 | 1 |
| 10 | Neha | 4 | 40000 | 2 | 2 |
| 10 | Jay | 3 | 52000 | 3 | 3 |
| 14 | Quinn | 5 | 38000 | 1 | 1 |
| 14 | Pia | 4 | 38000 | 2 | 2 |
**pandas equivalent:**
```python
import pandas as pd
d = emp[emp['manager_id'].notna()].copy()
d['rating_rank'] = d.groupby('manager_id')['rating'].rank(method='min', ascending=False).astype(int)
d = d.sort_values(['manager_id', 'rating', 'salary'], ascending=[True, False, False])
d['rank_with_tiebreak'] = d.groupby('manager_id').cumcount() + 1   # unique salaries within equal ratings here
res = d.sort_values(['manager_id', 'rating_rank', 'rank_with_tiebreak'])[['manager_id', 'name', 'rating', 'salary', 'rating_rank', 'rank_with_tiebreak']]
# result matches the SQL Output above (checked by running both)
```
**Edge cases:** The pandas tie-breaker uses cumcount and matches RANK only because no two people in the same team share both rating and salary; for true RANK behaviour on two keys use the sort-and-compare approach in Q55. NULL ratings: DESC puts NULL last in MySQL/SQLite/SQL Server and first in PostgreSQL/Oracle (use NULLS LAST where supported). Managers with one report get rank 1.
**Likely follow-ups:**
1. How do you show the manager's name? Self-join `employees m ON m.emp_id = e.manager_id`.
2. How do you compare to the team average? Add `AVG(rating) OVER (PARTITION BY manager_id)`.
**Common mistakes:** Ranking company-wide instead of per team; including NULL manager rows; forgetting that rating is a poor sort key by itself because of many ties.

### Q45 ⭐⭐ 🔴 Write a query to find the top 3 products by revenue per category, but return only categories with at least 3 products.
**Asked at:** commonly asked (no company-specific report found); prep sources list top-N per department among the most frequent window-function questions
**What the interviewer is checking:** Combining top-N per group with a group-size condition; knowing the size must be counted before the rank filter.
**Say this in the interview:** I rank products by revenue inside each category and also count the products in each category with a window COUNT. Then I keep rank 3 or better where that count is at least 3.
**Explain simply:**
- `RANK() OVER (PARTITION BY category ORDER BY revenue DESC)` gives each product its place in its category.
- `COUNT(*) OVER (PARTITION BY category)` attaches the category's product count to every row without collapsing rows. That lets me filter `n >= 3` in the same outer WHERE.
- Accessories has only 2 products, so it is excluded entirely.
- I used RANK, so Phones returns 4 rows (Edge and Spark tie for 3rd). Use ROW_NUMBER if you must return exactly 3.
**Example:** Laptops, Phones and Tablets have 3 or more products; Accessories has 2 and is dropped. If revenue came from an orders table, SUM it per product first, then do this.
**Sample data:**

`products`

| category | product | revenue |
|---|---|---|
| Laptops | AeroBook | 520000 |
| Laptops | ProBook | 480000 |
| Laptops | LiteBook | 310000 |
| Laptops | ChromeGo | 150000 |
| Laptops | EduBook | 90000 |
| Phones | Nova | 700000 |
| Phones | Pulse | 450000 |
| Phones | Edge | 300000 |
| Phones | Spark | 300000 |
| Tablets | Slate | 210000 |
| Tablets | Tab9 | 180000 |
| Tablets | Mini | 60000 |
| Accessories | Cable | 30000 |
| Accessories | Case | 45000 |
**SQL:**
```sql
WITH r AS (
  SELECT category, product, revenue,
         RANK()   OVER (PARTITION BY category ORDER BY revenue DESC) AS rk,
         COUNT(*) OVER (PARTITION BY category)                       AS n_products
  FROM products
)
SELECT category, product, revenue, rk
FROM r
WHERE rk <= 3 AND n_products >= 3
ORDER BY category, rk, product;
```
**Output:**

| category | product | revenue | rk |
|---|---|---|---|
| Laptops | AeroBook | 520000 | 1 |
| Laptops | ProBook | 480000 | 2 |
| Laptops | LiteBook | 310000 | 3 |
| Phones | Nova | 700000 | 1 |
| Phones | Pulse | 450000 | 2 |
| Phones | Edge | 300000 | 3 |
| Phones | Spark | 300000 | 3 |
| Tablets | Slate | 210000 | 1 |
| Tablets | Tab9 | 180000 | 2 |
| Tablets | Mini | 60000 | 3 |
**pandas equivalent:**
```python
import pandas as pd
d = products.copy()
d['rk'] = d.groupby('category')['revenue'].rank(method='min', ascending=False).astype(int)
d['n_products'] = d.groupby('category')['revenue'].transform('size')
res = d[(d['rk'] <= 3) & (d['n_products'] >= 3)].sort_values(['category', 'rk', 'product'])[['category', 'product', 'revenue', 'rk']]
# result matches the SQL Output above (checked by running both)
```
**Edge cases:** Ties at 3rd place give more than 3 rows with RANK. If a product appears on several rows (e.g. one row per order), COUNT(*) counts rows, not products: use the grouped revenue table first or COUNT(DISTINCT) via a subquery (COUNT(DISTINCT) is not allowed as a window function in some engines, e.g. SQL Server). NULL revenue sorts first in DESC in PostgreSQL.
**Likely follow-ups:**
1. Alternative without window COUNT? Join to `SELECT category FROM products GROUP BY category HAVING COUNT(*) >= 3`.
2. Does the size filter go before ranking? It can, in a subquery, and gives the same answer here.
**Common mistakes:** Using `HAVING COUNT(*) >= 3` in the same query as the window rank (it collapses rows); counting only the rows after the rank filter; forgetting ties.

### Q46 ⭐⭐ 🔴 Find the top-N per group when N differs by group (for example a lookup table gives N for each department).
**Asked at:** commonly asked (no company-specific report found); prep sources list top-N per department among the most frequent window-function questions
**What the interviewer is checking:** Whether you can make the cut-off a column (data-driven N) by joining a lookup table to ranked rows.
**Say this in the interview:** I rank employees inside each department with ROW_NUMBER, then join to the limits table on department and keep rows where the rank is less than or equal to that department's N. A LEFT JOIN with COALESCE gives a default N for departments missing from the lookup.
**Explain simply:**
- `LIMIT` and `TOP` take a fixed number, so they cannot vary by group. A window rank plus a join can.
- The condition `rn <= l.n` sits in the JOIN. Each department keeps its own number of rows.
- Support is not in the lookup. LEFT JOIN keeps it, and `COALESCE(l.n, 1)` (use the first non-NULL value) gives it a default of 1.
- Use an INNER JOIN instead if departments missing from the lookup should be dropped.
**Example:** HR wants 2 highest earners from Eng, 1 from HR, 3 from Sales, and 1 by default elsewhere.
**Sample data:**

`employees`

| emp_id | name | dept | salary |
|---|---|---|---|
| 1 | Meera | HR | 90000 |
| 2 | Ravi | HR | 60000 |
| 3 | Sana | HR | 60000 |
| 4 | Tom | HR | 45000 |
| 5 | Kiran | Eng | 120000 |
| 6 | Leena | Eng | 95000 |
| 7 | Arjun | Eng | 95000 |
| 8 | Divya | Eng | 70000 |
| 9 | Farah | Eng | 48000 |
| 10 | Gopal | Sales | 46000 |
| 11 | Isha | Sales | 52000 |
| 12 | Jay | Sales | 52000 |
| 13 | Neha | Sales | 40000 |
| 14 | Om | Support | 44000 |
| 15 | Pia | Support | 38000 |
| 16 | Quinn | Support | 38000 |
| 17 | Ujwal | Eng | 85000 |
| 18 | Vik | Eng | 60000 |

`dept_limits`

| dept | n |
|---|---|
| Eng | 2 |
| HR | 1 |
| Sales | 3 |
**SQL:**
```sql
CREATE TABLE dept_limits (dept TEXT, n INTEGER);
INSERT INTO dept_limits VALUES ('Eng', 2), ('HR', 1), ('Sales', 3);

WITH ranked AS (
  SELECT dept, name, salary,
         ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC, emp_id) AS rn
  FROM employees
)
SELECT r.dept, r.name, r.salary, r.rn
FROM ranked r
LEFT JOIN dept_limits l ON l.dept = r.dept
WHERE r.rn <= COALESCE(l.n, 1)
ORDER BY r.dept, r.rn;
```
**Output:**

| dept | name | salary | rn |
|---|---|---|---|
| Eng | Kiran | 120000 | 1 |
| Eng | Leena | 95000 | 2 |
| HR | Meera | 90000 | 1 |
| Sales | Isha | 52000 | 1 |
| Sales | Jay | 52000 | 2 |
| Sales | Gopal | 46000 | 3 |
| Support | Om | 44000 | 1 |
**pandas equivalent:**
```python
import pandas as pd
d = emp.sort_values(['dept', 'salary', 'emp_id'], ascending=[True, False, True]).copy()
d['rn'] = d.groupby('dept').cumcount() + 1
d['n'] = d['dept'].map(limits.set_index('dept')['n']).fillna(1)
res = d[d['rn'] <= d['n']].sort_values(['dept', 'rn'])[['dept', 'name', 'salary', 'rn']]
# result matches the SQL Output above (checked by running both)
```
**Edge cases:** If you want ties included, switch to RANK or DENSE_RANK. If a department has N = 0 in the lookup, it returns nothing (correct). Duplicate rows for one department in the lookup would multiply output rows, so make `dept` unique in dept_limits (a key). Departments with fewer people than N simply return all their people.
**Likely follow-ups:**
1. Can the lookup be avoided? Yes, with a CASE: `rn <= CASE dept WHEN 'Eng' THEN 2 WHEN 'HR' THEN 1 ELSE 3 END`, fine for a handful of departments.
**Common mistakes:** Trying `LIMIT l.n` (not allowed); filtering rn in WHERE before the join so it uses a fixed number; INNER JOIN silently dropping departments that are not in the lookup.

### Q47 ⭐ 🟢 What is the difference between RANK and DENSE_RANK in terms of 'gaps' in the sequence?
**Asked at:** commonly asked (no company-specific report found); prep sources list top-N per department among the most frequent window-function questions
**What the interviewer is checking:** The classic tie question: do you know RANK leaves gaps and DENSE_RANK does not, and which one to pick for 'Nth highest'?
**Say this in the interview:** Both give tied rows the same number. After a tie RANK skips numbers (1, 1, 3) because it counts the rows ahead of you, while DENSE_RANK carries on with the next number (1, 1, 2). For 'second highest salary' I use DENSE_RANK.
**Explain simply:**
- RANK = 1 + number of rows strictly better than you. Two people ahead of you means rank 3, even if the two ahead tie with each other. That creates a *gap*.
- DENSE_RANK = 1 + number of distinct values better than you. No gaps.
- If you ask for 'rank = 2' with RANK in a department where two people tie for first, you get nothing. DENSE_RANK gives the next salary level.
**Example:** Sales salaries: 52,000, 52,000, 46,000, 40,000. RANK = 1,1,3,4. DENSE_RANK = 1,1,2,3.
**Sample data:**

`employees`

| emp_id | name | dept | salary |
|---|---|---|---|
| 10 | Gopal | Sales | 46000 |
| 11 | Isha | Sales | 52000 |
| 12 | Jay | Sales | 52000 |
| 13 | Neha | Sales | 40000 |
**SQL:**
```sql
-- Gap vs no gap (Sales)
SELECT name, salary,
       RANK()       OVER (ORDER BY salary DESC) AS rnk,
       DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rnk
FROM employees
WHERE dept = 'Sales'
ORDER BY salary DESC, name;

-- Second-highest salary level: RANK finds nobody, DENSE_RANK finds Gopal
SELECT 'RANK = 2' AS method, name, salary FROM (
  SELECT name, salary, RANK() OVER (ORDER BY salary DESC) AS r FROM employees WHERE dept = 'Sales') WHERE r = 2
UNION ALL
SELECT 'DENSE_RANK = 2', name, salary FROM (
  SELECT name, salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS r FROM employees WHERE dept = 'Sales') WHERE r = 2;
```
**Output:**

Gap vs no gap (Sales):

| name | salary | rnk | dense_rnk |
|---|---|---|---|
| Isha | 52000 | 1 | 1 |
| Jay | 52000 | 1 | 1 |
| Gopal | 46000 | 3 | 2 |
| Neha | 40000 | 4 | 3 |

Second-highest salary level: RANK finds nobody, DENSE_RANK finds Gopal:

| method | name | salary |
|---|---|---|
| DENSE_RANK = 2 | Gopal | 46000 |
**pandas equivalent:**
```python
import pandas as pd
d = emp[emp['dept'] == 'Sales'].copy()
d['rnk'] = d['salary'].rank(method='min', ascending=False).astype(int)
d['dense_rnk'] = d['salary'].rank(method='dense', ascending=False).astype(int)
res = d.sort_values(['salary', 'name'], ascending=[False, True])[['name', 'salary', 'rnk', 'dense_rnk']]
# result matches the SQL Output above (checked by running both)
```
**Edge cases:** The gap size equals (number of tied rows - 1). With no ties the two functions are identical. NULLs tie with each other. Empty input returns no rows.
**Likely follow-ups:**
1. Which for 'Nth highest salary'? DENSE_RANK, because you want the Nth distinct salary.
2. Which for a leaderboard with Olympic-style medals? RANK.
**Common mistakes:** Using RANK for 'second highest' and getting an empty result; assuming DENSE_RANK has fewer rows (it has the same rows, just different numbers).

### Q48 ⭐ 🟢 Which SQL databases support window functions (MySQL 8, PostgreSQL, SQL Server, Oracle, SQLite) and which do not?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Practical awareness of which databases you can use window functions on, and the old-MySQL trap.
**Say this in the interview:** Today almost every mainstream database supports them: PostgreSQL, SQL Server, Oracle, SQLite and MySQL 8. The notable exception is MySQL 5.7 and older, where you must fall back on variables or self joins.
**Explain simply:**
- Window functions entered the SQL standard in 2003. Versions below are from memory (not run here), so double-check before quoting them.
- **PostgreSQL**: 8.4 and later (2009). **Oracle**: yes for a long time (analytic functions since 8i). **SQL Server**: ranking functions (ROW_NUMBER, RANK, DENSE_RANK, NTILE) since 2005; running totals, LAG, LEAD and FIRST_VALUE need 2012 or later.
- **MySQL**: yes from 8.0 (2018); **not** in 5.7 or earlier. **MariaDB** from 10.2. **SQLite**: from 3.25 (2018). Cloud warehouses (BigQuery, Snowflake, Redshift) support them.
- Verified here: SQLite 3.49.1 and DuckDB 1.5.6 run the demo below. Check yours with `SELECT VERSION();` (MySQL/PostgreSQL), `SELECT @@VERSION;` (SQL Server), `SELECT sqlite_version();` (SQLite).
- Syntax differences: QUALIFY exists only in some engines; named WINDOW clauses (`WINDOW w AS (...)`) are not in SQL Server (from memory).
**Example:** A team moves from an old MySQL 5.7 server to MySQL 8: queries that needed correlated subqueries for rank can be rewritten with ROW_NUMBER.
**SQL:**
```sql
SELECT sqlite_version() AS sqlite_version,
       (SELECT ROW_NUMBER() OVER (ORDER BY salary DESC) FROM employees WHERE name = 'Kiran') AS top_row_number;
```
**Output:**

| sqlite_version | top_row_number |
|---|---|
| 3.49.1 | 1 |
**Edge cases:** On an unsupported engine the query fails with a syntax error near OVER. SQLite older than 3.25 behaves the same.
**Likely follow-ups:**
1. What do you do on MySQL 5.7? Correlated subquery or self join (Q52), or session variables, which are fragile (from memory).
**Common mistakes:** Assuming all MySQL versions support them; mixing up the SQL Server 2005 ranking support with the richer frame support added in 2012.

### Q49 ⭐ 🟡 What is the difference between RANK() and PERCENT_RANK() on a 5-row example?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you work through a small example by hand and show RANK as a position and PERCENT_RANK as a 0 to 1 scale?
**Say this in the interview:** On five rows, RANK gives positions like 1, 2, 2, 4, 5. PERCENT_RANK converts them with (rank - 1) over (5 - 1), so 0, 0.25, 0.25, 0.75, 1.
**Explain simply:**
- Five candidates with scores 90, 85, 85, 70, 60, ordered highest first.
- RANK: 1, 2, 2, 4, 5. Two tied rows share rank 2, and rank 3 is skipped.
- PERCENT_RANK = (RANK - 1) / 4: 0, 0.25, 0.25, 0.75, 1.
- RANK tells you the position; PERCENT_RANK tells you how far down the list you are as a fraction, comparable across groups of different sizes.
**Example:** Anil is rank 1 / percent 0 (nobody above him). Esha is rank 5 / percent 1 (everybody above her).
**Sample data:**

`scores`

| candidate | score |
|---|---|
| Anil | 90 |
| Bela | 85 |
| Chirag | 85 |
| Dev | 70 |
| Esha | 60 |
**SQL:**
```sql
SELECT candidate, score,
       RANK() OVER (ORDER BY score DESC) AS rnk,
       PERCENT_RANK() OVER (ORDER BY score DESC) AS pct_rank
FROM scores
ORDER BY score DESC, candidate;
```
**Output:**

| candidate | score | rnk | pct_rank |
|---|---|---|---|
| Anil | 90 | 1 | 0 |
| Bela | 85 | 2 | 0.25 |
| Chirag | 85 | 2 | 0.25 |
| Dev | 70 | 4 | 0.75 |
| Esha | 60 | 5 | 1 |
**pandas equivalent:**
```python
import pandas as pd
d = scores.copy()
d['rnk'] = d['score'].rank(method='min', ascending=False).astype(int)
d['pct_rank'] = (d['rnk'] - 1) / (len(d) - 1)
res = d.sort_values(['score', 'candidate'], ascending=[False, True])[['candidate', 'score', 'rnk', 'pct_rank']]
# result matches the SQL Output above (checked by running both)
```
**Edge cases:** Tied rows get identical PERCENT_RANK. A one-row table gives 0. NULL scores sort together and share a rank.
**Likely follow-ups:**
1. Why is the denominator n-1, not n? So that the first row is exactly 0 and the last is exactly 1.
**Common mistakes:** Using rank / n (that is closer to CUME_DIST); expecting the percent to be 0.2, 0.4 ... evenly spaced when ties exist.

### Q50 ⭐ 🟡 Write a query to find the top 3 and the bottom 3 earners in each department in one result.
**Asked at:** commonly asked (no company-specific report found); prep sources list top-N per department among the most frequent window-function questions
**What the interviewer is checking:** Using two ROW_NUMBERs (ascending and descending) to pick both ends in a single pass.
**Say this in the interview:** I number each department's rows twice, once from the highest salary and once from the lowest, and keep a row if either number is 3 or less. A CASE column labels top or bottom.
**Explain simply:**
- `rn_top` counts from the highest salary; `rn_bottom` counts from the lowest. Same PARTITION BY, opposite ORDER BY.
- `WHERE rn_top <= 3 OR rn_bottom <= 3` keeps both ends in one result.
- Small departments overlap: someone can be in the top 3 and the bottom 3 at once (HR has 4 people, so they all qualify). The CASE labels them 'Top' first.
- Alternative: two queries joined with UNION ALL. The two-ROW_NUMBER version reads the table once.
**Example:** Eng has 7 people: Kiran, Leena, Arjun are the top 3; Farah, Vik, Divya are the bottom 3; Ujwal (85,000) is in the middle and is dropped.
**Sample data:**

`employees`

| emp_id | name | dept | salary |
|---|---|---|---|
| 5 | Kiran | Eng | 120000 |
| 6 | Leena | Eng | 95000 |
| 7 | Arjun | Eng | 95000 |
| 8 | Divya | Eng | 70000 |
| 9 | Farah | Eng | 48000 |
| 17 | Ujwal | Eng | 85000 |
| 18 | Vik | Eng | 60000 |
**SQL:**
```sql
WITH r AS (
  SELECT dept, name, salary,
         ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC, emp_id) AS rn_top,
         ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary ASC,  emp_id) AS rn_bottom
  FROM employees
)
SELECT dept, name, salary,
       CASE WHEN rn_top <= 3 THEN 'Top ' || rn_top ELSE 'Bottom ' || rn_bottom END AS bucket
FROM r
WHERE (rn_top <= 3 OR rn_bottom <= 3) AND dept = 'Eng'
ORDER BY dept, salary DESC, name;
```
**Output:**

| dept | name | salary | bucket |
|---|---|---|---|
| Eng | Kiran | 120000 | Top 1 |
| Eng | Arjun | 95000 | Top 3 |
| Eng | Leena | 95000 | Top 2 |
| Eng | Divya | 70000 | Bottom 3 |
| Eng | Vik | 60000 | Bottom 2 |
| Eng | Farah | 48000 | Bottom 1 |
**pandas equivalent:**
```python
import pandas as pd
d = emp.sort_values(['dept', 'salary', 'emp_id'], ascending=[True, False, True]).copy()
d['rn_top'] = d.groupby('dept').cumcount() + 1
d = d.sort_values(['dept', 'salary', 'emp_id'], ascending=[True, True, True])
d['rn_bottom'] = d.groupby('dept').cumcount() + 1
d['bucket'] = d.apply(lambda r: f"Top {r.rn_top}" if r.rn_top <= 3 else f"Bottom {r.rn_bottom}", axis=1)
res = d[((d['rn_top'] <= 3) | (d['rn_bottom'] <= 3)) & (d['dept'] == 'Eng')].sort_values(['dept', 'salary', 'name'], ascending=[True, False, True])[['dept', 'name', 'salary', 'bucket']]
# result matches the SQL Output above (checked by running both)
```
**Edge cases:** Ties at the boundary: Leena and Arjun both earn 95,000; ROW_NUMBER with emp_id tie-break splits them. Use RANK/DENSE_RANK to include all ties. Departments with 5 or fewer people return everyone. Remove the `dept = 'Eng'` filter to see all departments (filtered here only to keep the output short).
**Likely follow-ups:**
1. How with UNION ALL? Two ranked CTE selects, one DESC and one ASC, combined with UNION ALL (use UNION to remove overlap).
**Common mistakes:** Using ORDER BY salary in one ROW_NUMBER and expecting it to give both ends; double-counting overlap people when using UNION ALL.

### Q51 ⭐ 🟡 How do FIRST_VALUE() and LAST_VALUE() help in ranking-style questions (for example, highest salary in the department shown beside every row)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know FIRST_VALUE is easy but LAST_VALUE has a default-frame trap?
**Say this in the interview:** FIRST_VALUE over a department ordered by salary descending puts the department's top salary beside every row. LAST_VALUE needs the frame widened to UNBOUNDED FOLLOWING, otherwise it just returns the current row's value.
**Explain simply:**
- `FIRST_VALUE(salary) OVER (PARTITION BY dept ORDER BY salary DESC)` = the highest salary in the department, repeated on each row.
- A **frame** is the slice of the partition the function looks at. With an ORDER BY the default frame runs from the start of the partition up to the *current row*.
- So `LAST_VALUE` with the default frame returns the current row's own value (the last row it can see). Fix: `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`.
- Handy for 'gap to top salary' columns, or for 'the highest earner's name beside every row' (use FIRST_VALUE(name)).
- For just the max or min, `MAX(salary) OVER (PARTITION BY dept)` is simpler and needs no frame.
**Example:** HR: Meera earns 90,000. Show 90,000 next to Ravi, Sana and Tom, plus how far each is from the top.
**Sample data:**

`employees`

| emp_id | name | dept | salary |
|---|---|---|---|
| 1 | Meera | HR | 90000 |
| 2 | Ravi | HR | 60000 |
| 3 | Sana | HR | 60000 |
| 4 | Tom | HR | 45000 |
| 14 | Om | Support | 44000 |
| 15 | Pia | Support | 38000 |
| 16 | Quinn | Support | 38000 |
**SQL:**
```sql
SELECT dept, name, salary,
       FIRST_VALUE(salary) OVER w AS top_salary,
       LAST_VALUE(salary)  OVER w AS last_value_default,
       LAST_VALUE(salary)  OVER (PARTITION BY dept ORDER BY salary DESC, emp_id
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS lowest_salary,
       FIRST_VALUE(salary) OVER w - salary AS gap_to_top
FROM employees
WHERE dept IN ('HR', 'Support')
WINDOW w AS (PARTITION BY dept ORDER BY salary DESC, emp_id)
ORDER BY dept, salary DESC, emp_id;
```
**Output:**

| dept | name | salary | top_salary | last_value_default | lowest_salary | gap_to_top |
|---|---|---|---|---|---|---|
| HR | Meera | 90000 | 90000 | 90000 | 45000 | 0 |
| HR | Ravi | 60000 | 90000 | 60000 | 45000 | 30000 |
| HR | Sana | 60000 | 90000 | 60000 | 45000 | 30000 |
| HR | Tom | 45000 | 90000 | 45000 | 45000 | 45000 |
| Support | Om | 44000 | 44000 | 44000 | 38000 | 0 |
| Support | Pia | 38000 | 44000 | 38000 | 38000 | 6000 |
| Support | Quinn | 38000 | 44000 | 38000 | 38000 | 6000 |
**pandas equivalent:**
```python
import pandas as pd
d = emp[emp['dept'].isin(['HR', 'Support'])].copy()
g = d.groupby('dept')['salary']
d['top_salary'] = g.transform('max')
d['last_value_default'] = d['salary']          # default frame: last visible row is the current row
d['lowest_salary'] = g.transform('min')
d['gap_to_top'] = d['top_salary'] - d['salary']
res = d.sort_values(['dept', 'salary', 'emp_id'], ascending=[True, False, True])[['dept', 'name', 'salary', 'top_salary', 'last_value_default', 'lowest_salary', 'gap_to_top']]
# result matches the SQL Output above (checked by running both)
```
**Edge cases:** Ties in the ORDER BY: with RANGE frames (the default when no ROWS is given) tied rows are treated as peers, so I add emp_id as a tie-breaker. NULLs: FIRST_VALUE returns NULL if the first row's value is NULL (use IGNORE NULLS in Oracle/SQL Server 2022; not run here). The named WINDOW clause works in SQLite, PostgreSQL, MySQL 8, DuckDB; SQL Server needs the clause repeated (from memory).
**Likely follow-ups:**
1. Simpler way for max? `MAX(salary) OVER (PARTITION BY dept)`.
2. Name of the top earner? `FIRST_VALUE(name) OVER (PARTITION BY dept ORDER BY salary DESC, emp_id)`.
**Common mistakes:** Using LAST_VALUE without a frame and getting the current row back; forgetting ORDER BY inside OVER so 'first' is undefined.

### Q52 ⭐ 🟡 How do you get the top-N per group without window functions (correlated subquery or self join)? Compare the two approaches.
**Asked at:** commonly asked (no company-specific report found); prep sources list top-N per department among the most frequent window-function questions
**What the interviewer is checking:** Whether you can solve top-N per group on old engines and explain the cost difference.
**Say this in the interview:** With a correlated subquery I count how many people in the same department earn more than this person and keep those with fewer than N. With a self join I do the same count using GROUP BY and HAVING. Both are simpler to explain but slower than a window function on big tables.
**Explain simply:**
- **Correlated subquery**: a subquery that refers to the outer row. For each employee it counts higher-paid colleagues in the same department. `< 2` means at most 1 person is above, so that person is top 2.
- **Self join**: join the table to itself on the same department and salary greater than mine; `LEFT JOIN` keeps the top earner (who has nobody above). `GROUP BY` + `HAVING COUNT(...) < 2` does the filtering.
- Both behave like RANK: tied people share the position, so ties can return extra rows (Eng returns 3 here because Leena and Arjun tie for 2nd).
- Cost: roughly comparing every row with every other row in its department (quadratic). An index on (dept, salary) helps; a window function sorts each department once.
- Use these on MySQL 5.7-era systems or in interviews that ban window functions.
**Example:** Top 2 earners per department without ROW_NUMBER.
**Sample data:**

`employees`

| emp_id | name | dept | salary |
|---|---|---|---|
| 1 | Meera | HR | 90000 |
| 2 | Ravi | HR | 60000 |
| 3 | Sana | HR | 60000 |
| 4 | Tom | HR | 45000 |
| 5 | Kiran | Eng | 120000 |
| 6 | Leena | Eng | 95000 |
| 7 | Arjun | Eng | 95000 |
| 8 | Divya | Eng | 70000 |
| 9 | Farah | Eng | 48000 |
| 10 | Gopal | Sales | 46000 |
| 11 | Isha | Sales | 52000 |
| 12 | Jay | Sales | 52000 |
| 13 | Neha | Sales | 40000 |
| 14 | Om | Support | 44000 |
| 15 | Pia | Support | 38000 |
| 16 | Quinn | Support | 38000 |
| 17 | Ujwal | Eng | 85000 |
| 18 | Vik | Eng | 60000 |
**SQL:**
```sql
CREATE INDEX idx_emp_dept_salary ON employees (dept, salary DESC);

-- Correlated subquery (top 2 per department, ties included)
SELECT dept, name, salary
FROM employees e
WHERE (SELECT COUNT(*) FROM employees x
       WHERE x.dept = e.dept AND x.salary > e.salary) < 2
ORDER BY dept, salary DESC, name;

-- Self join with GROUP BY / HAVING (same answer)
SELECT e.dept, e.name, e.salary
FROM employees e
LEFT JOIN employees x ON x.dept = e.dept AND x.salary > e.salary
GROUP BY e.emp_id, e.dept, e.name, e.salary
HAVING COUNT(x.emp_id) < 2
ORDER BY e.dept, e.salary DESC, e.name;
```
**Output:**

Correlated subquery (top 2 per department, ties included):

| dept | name | salary |
|---|---|---|
| Eng | Kiran | 120000 |
| Eng | Arjun | 95000 |
| Eng | Leena | 95000 |
| HR | Meera | 90000 |
| HR | Ravi | 60000 |
| HR | Sana | 60000 |
| Sales | Isha | 52000 |
| Sales | Jay | 52000 |
| Support | Om | 44000 |
| Support | Pia | 38000 |
| Support | Quinn | 38000 |

Self join with GROUP BY / HAVING (same answer):

| dept | name | salary |
|---|---|---|
| Eng | Kiran | 120000 |
| Eng | Arjun | 95000 |
| Eng | Leena | 95000 |
| HR | Meera | 90000 |
| HR | Ravi | 60000 |
| HR | Sana | 60000 |
| Sales | Isha | 52000 |
| Sales | Jay | 52000 |
| Support | Om | 44000 |
| Support | Pia | 38000 |
| Support | Quinn | 38000 |
**pandas equivalent:**
```python
import pandas as pd
d = emp.copy()
d['higher_paid_in_dept'] = d.apply(lambda r: ((emp['dept'] == r['dept']) & (emp['salary'] > r['salary'])).sum(), axis=1)
res = d[d['higher_paid_in_dept'] < 2].sort_values(['dept', 'salary', 'name'], ascending=[True, False, True])[['dept', 'name', 'salary']]
# result matches the SQL Output above (checked by running both)
```
**Edge cases:** Ties return extra rows. NULL salary: `x.salary > NULL` is unknown so a NULL-salary person has zero people above and is wrongly kept; filter `salary IS NOT NULL`. Self-join duplicates: COUNT(x.emp_id) (not COUNT(*)) avoids counting the NULL row from the LEFT JOIN. Exactly-N needs a unique tie-breaker, e.g. `x.salary > e.salary OR (x.salary = e.salary AND x.emp_id < e.emp_id)`.
**Likely follow-ups:**
1. Which is faster? Neither beats a window function on large data; the correlated subquery is easier to read, the join sometimes plans better (check the query plan; behaviour varies by engine, from memory).
2. Why is it slow? Quadratic comparisons within each group.
**Common mistakes:** Using `<= N` instead of `< N` in the count (off by one); using COUNT(*) with LEFT JOIN; expecting exactly N rows when ties exist.

### Q53 ⭐ 🟡 Using CROSS APPLY or LATERAL join, how do you get top-N per group? When is it faster?
**Asked at:** commonly asked (no company-specific report found); prep sources list top-N per department among the most frequent window-function questions
**What the interviewer is checking:** Knowing the row-by-row 'for each group, run this small query' pattern and its engine syntax.
**Say this in the interview:** LATERAL in PostgreSQL, MySQL 8 and DuckDB, or CROSS APPLY in SQL Server, lets a subquery refer to the outer row. For each department I run a small ORDER BY ... LIMIT N query. It is fastest when there are few groups and an index on (group, sort column), because each group then costs a quick index lookup.
**Explain simply:**
- A normal subquery in FROM cannot see the other tables in the same FROM. **LATERAL** (standard SQL; PostgreSQL, MySQL 8.0.14+, DuckDB, Oracle 12c+) and **CROSS APPLY** (SQL Server, Oracle) allow it; the right side is evaluated once per left row, like a loop.
- Pattern: take the list of groups (departments), and for each one fetch `ORDER BY salary DESC LIMIT 2`. Per-group LIMIT is now possible because it is inside the loop.
- SQL Server form: `FROM departments d CROSS APPLY (SELECT TOP 2 name, salary FROM employees e WHERE e.dept = d.dept ORDER BY salary DESC) t` (not run here, from memory).
- **Faster when**: few groups, many rows per group, and an index on (dept, salary DESC): each group reads only N index entries without sorting everything.
- **Slower when**: many tiny groups (thousands of loops) or no index, where a single window-function pass is better.
- Version note: MySQL LATERAL support is from memory; verified here only in DuckDB.
**Example:** HR wants the 2 best-paid people for each department; the department list is short (4) and the employee table is huge.
**Sample data:**

`employees`

| emp_id | name | dept | salary |
|---|---|---|---|
| 1 | Meera | HR | 90000 |
| 2 | Ravi | HR | 60000 |
| 3 | Sana | HR | 60000 |
| 4 | Tom | HR | 45000 |
| 10 | Gopal | Sales | 46000 |
| 11 | Isha | Sales | 52000 |
| 12 | Jay | Sales | 52000 |
| 13 | Neha | Sales | 40000 |
**SQL:**
```sql
-- optional supporting index, matters on big tables
-- CREATE INDEX idx_emp_dept_salary ON employees (dept, salary DESC);

SELECT d.dept, t.name, t.salary
FROM (SELECT DISTINCT dept FROM employees) AS d,
LATERAL (SELECT name, salary
         FROM employees e
         WHERE e.dept = d.dept
         ORDER BY salary DESC, emp_id
         LIMIT 2) AS t
ORDER BY d.dept, t.salary DESC, t.name;
```
**Output:**

| dept | name | salary |
|---|---|---|
| Eng | Kiran | 120000 |
| Eng | Leena | 95000 |
| HR | Meera | 90000 |
| HR | Ravi | 60000 |
| Sales | Isha | 52000 |
| Sales | Jay | 52000 |
| Support | Om | 44000 |
| Support | Pia | 38000 |
**pandas equivalent:**
```python
import pandas as pd
res = (emp.sort_values(['dept', 'salary', 'emp_id'], ascending=[True, False, True])
          .groupby('dept').head(2)[['dept', 'name', 'salary']])
# result matches the SQL Output above (checked by running both)
```
**Edge cases:** A group with fewer than N rows returns what it has; a group with no rows disappears with CROSS APPLY / inner LATERAL (use OUTER APPLY / LEFT JOIN LATERAL ... ON TRUE to keep it). Ties: ORDER BY with a tie-breaker gives exactly N; SQL Server `TOP N WITH TIES` includes ties.
**Likely follow-ups:**
1. PostgreSQL syntax? Same as DuckDB: `JOIN LATERAL (...) t ON TRUE` (not run here).
2. Does it need a list of groups? Yes, a departments table or `SELECT DISTINCT dept`; a real departments table with an index is faster than DISTINCT.
**Common mistakes:** Forgetting the join condition inside the lateral subquery; expecting it to be faster without an index; using it with thousands of tiny groups.

### Q54 ⭐ 🟡 Write a query to find employees earning more than the average of their department using a window function instead of a join.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Using AVG as a window function to avoid a join/subquery, and knowing it must be filtered from an outer query.
**Say this in the interview:** AVG(salary) OVER (PARTITION BY dept) puts the department average on every row without collapsing the rows. Then an outer WHERE keeps people above it. No join or GROUP BY needed.
**Explain simply:**
- A normal `AVG ... GROUP BY dept` collapses to one row per department and you would have to join it back to employees. The window version keeps every employee row and adds the average next to it.
- Because WHERE cannot see window results, wrap it in a CTE (Q41), then compare `salary > dept_avg`.
- Averages ignore NULL salaries.
**Example:** Sales average = (52,000 + 52,000 + 46,000 + 40,000) / 4 = 47,500, so Isha and Jay are above average, Gopal and Neha are below.
**Sample data:**

`employees`

| emp_id | name | dept | salary |
|---|---|---|---|
| 1 | Meera | HR | 90000 |
| 2 | Ravi | HR | 60000 |
| 3 | Sana | HR | 60000 |
| 4 | Tom | HR | 45000 |
| 5 | Kiran | Eng | 120000 |
| 6 | Leena | Eng | 95000 |
| 7 | Arjun | Eng | 95000 |
| 8 | Divya | Eng | 70000 |
| 9 | Farah | Eng | 48000 |
| 10 | Gopal | Sales | 46000 |
| 11 | Isha | Sales | 52000 |
| 12 | Jay | Sales | 52000 |
| 13 | Neha | Sales | 40000 |
| 14 | Om | Support | 44000 |
| 15 | Pia | Support | 38000 |
| 16 | Quinn | Support | 38000 |
| 17 | Ujwal | Eng | 85000 |
| 18 | Vik | Eng | 60000 |
**SQL:**
```sql
WITH t AS (
  SELECT name, dept, salary,
         AVG(salary) OVER (PARTITION BY dept) AS dept_avg
  FROM employees
)
SELECT name, dept, salary, ROUND(dept_avg, 0) AS dept_avg
FROM t
WHERE salary > dept_avg
ORDER BY dept, salary DESC, name;
```
**Output:**

| name | dept | salary | dept_avg |
|---|---|---|---|
| Kiran | Eng | 120000 | 81857 |
| Arjun | Eng | 95000 | 81857 |
| Leena | Eng | 95000 | 81857 |
| Ujwal | Eng | 85000 | 81857 |
| Meera | HR | 90000 | 63750 |
| Isha | Sales | 52000 | 47500 |
| Jay | Sales | 52000 | 47500 |
| Om | Support | 44000 | 40000 |
**pandas equivalent:**
```python
import pandas as pd
d = emp.copy()
d['dept_avg'] = d.groupby('dept')['salary'].transform('mean')
res = d[d['salary'] > d['dept_avg']].assign(dept_avg=lambda x: x['dept_avg'].round(0)).sort_values(['dept', 'salary', 'name'], ascending=[True, False, True])[['name', 'dept', 'salary', 'dept_avg']]
# result matches the SQL Output above (checked by running both)
```
**Edge cases:** NULL salary: ignored by AVG, and NULL > average is unknown, so that person is excluded. A department with one person never qualifies (salary equals average). Integer division: in SQL Server, AVG of an INT column returns an INT (truncated), so cast to DECIMAL first (from memory, not run here).
**Likely follow-ups:**
1. Same with a join? `JOIN (SELECT dept, AVG(salary) a FROM employees GROUP BY dept) d ON ...`; same result, two passes.
2. Compare to company average? `AVG(salary) OVER ()`.
**Common mistakes:** Writing `WHERE salary > AVG(salary) OVER (...)` directly (error); using `GROUP BY dept` and then trying to show employee names; comparing to a rounded average.

### Q55 ⭐ 🟡 How do you rank rows by two columns (for example department rank, then salary within it)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can combine ranking at two levels (group level and row level) and know that one ORDER BY with two columns is a different thing.
**Say this in the interview:** "Two columns can mean two rankings or one ranking with a tie-breaker. For two levels I rank the departments with one window and rank the people inside each department with a second window that has PARTITION BY. If I just want one running order sorted by department then salary, I put both columns in a single ORDER BY."
**Explain simply:**
- A *window function* is a calculation that looks at a set of related rows but still keeps every row in the result. The set is defined in `OVER (...)`.
- `PARTITION BY dept` means "restart the ranking for each department" (like separate class lists per department). `ORDER BY` inside `OVER` decides who is first.
- Two-level ranking = two separate windows in the same SELECT: one without PARTITION BY (ranks whole departments) and one with it (ranks people within a department).
- Single window, two sort columns, e.g. `ORDER BY dept, salary DESC`, gives one overall numbering where `dept` is the main key and `salary` only breaks ties inside it.
**Example:** Payroll totals: Eng 230,000, Sales 110,000, HR 100,000. So Eng is department rank 1. Inside Eng, Asha (90,000) is 1 and Bala and Chitra (70,000 each) share rank 2.
**Sample data:**

`employees`

| emp_id | emp_name | dept | salary |
|---|---|---|---|
| 1 | Asha | Eng | 90000 |
| 2 | Bala | Eng | 70000 |
| 3 | Chitra | Eng | 70000 |
| 4 | Dev | Sales | 60000 |
| 5 | Esha | Sales | 50000 |
| 6 | Farah | HR | 55000 |
| 7 | Gita | HR | 45000 |
**SQL:**
```sql
-- Two-level ranking (dept payroll rank + salary rank inside dept)
WITH t AS (
    SELECT emp_name, dept, salary,
           SUM(salary) OVER (PARTITION BY dept) AS dept_payroll   -- total pay of the department on every row
    FROM employees
)
SELECT dept,
       DENSE_RANK() OVER (ORDER BY dept_payroll DESC)               AS dept_rank,    -- level 1: rank the departments
       emp_name, salary,
       RANK() OVER (PARTITION BY dept ORDER BY salary DESC)         AS salary_rank   -- level 2: rank people inside the department
FROM t
ORDER BY dept_rank, salary_rank, emp_name;

-- One window with two sort columns
SELECT dept, emp_name, salary,
       ROW_NUMBER() OVER (ORDER BY dept, salary DESC, emp_name) AS overall_position
FROM employees
ORDER BY overall_position;
```
Runs unchanged on PostgreSQL, MySQL 8, SQL Server and Oracle (comments use `--`). Main query was run in SQLite 3.49.
**Output:**

*Two-level ranking (dept payroll rank + salary rank inside dept)*

| dept | dept_rank | emp_name | salary | salary_rank |
|---|---|---|---|---|
| Eng | 1 | Asha | 90000 | 1 |
| Eng | 1 | Bala | 70000 | 2 |
| Eng | 1 | Chitra | 70000 | 2 |
| Sales | 2 | Dev | 60000 | 1 |
| Sales | 2 | Esha | 50000 | 2 |
| HR | 3 | Farah | 55000 | 1 |
| HR | 3 | Gita | 45000 | 2 |

*One window with two sort columns*

| dept | emp_name | salary | overall_position |
|---|---|---|---|
| Eng | Asha | 90000 | 1 |
| Eng | Bala | 70000 | 2 |
| Eng | Chitra | 70000 | 3 |
| HR | Farah | 55000 | 4 |
| HR | Gita | 45000 | 5 |
| Sales | Dev | 60000 | 6 |
| Sales | Esha | 50000 | 7 |
**pandas equivalent:**
```python
import pandas as pd
import numpy as np

employees = pd.DataFrame([
    (1, 'Asha', 'Eng', 90000),
    (2, 'Bala', 'Eng', 70000),
    (3, 'Chitra', 'Eng', 70000),
    (4, 'Dev', 'Sales', 60000),
    (5, 'Esha', 'Sales', 50000),
    (6, 'Farah', 'HR', 55000),
    (7, 'Gita', 'HR', 45000)],
    columns=['emp_id', 'emp_name', 'dept', 'salary'])

t = employees.copy()
t['dept_payroll'] = t.groupby('dept')['salary'].transform('sum')
t['dept_rank'] = t['dept_payroll'].rank(method='dense', ascending=False).astype(int)
t['salary_rank'] = t.groupby('dept')['salary'].rank(method='min', ascending=False).astype(int)
result = (t.sort_values(['dept_rank', 'salary_rank', 'emp_name'])
            [['dept', 'dept_rank', 'emp_name', 'salary', 'salary_rank']])

t2 = employees.sort_values(['dept', 'salary', 'emp_name'], ascending=[True, False, True]).reset_index(drop=True)
t2['overall_position'] = range(1, len(t2) + 1)
result2 = t2[['dept', 'emp_name', 'salary', 'overall_position']]
# result matches the SQL output row for row (checked by running both)
```
**Edge cases:** Tied department totals get the same `dept_rank` (DENSE_RANK keeps numbers continuous). Tied salaries get the same `salary_rank` (RANK leaves a gap after). NULL salary: SUM ignores it, but in `ORDER BY salary DESC` it sorts last in SQLite/MySQL and first in PostgreSQL/Oracle (from memory).
**Likely follow-ups:**
- How is this different from `GROUP BY`? GROUP BY collapses rows; window functions keep each employee row beside the department number.
- How do you rank only the top department's people? Wrap in a CTE (a named temporary result) and filter `dept_rank = 1`.
**Common mistakes:** Putting two ORDER BY columns in one window and expecting two separate rankings; forgetting to wrap in a CTE before filtering on a rank; ordering the final output only by `dept` so the ranks look shuffled.

### Q56 ⭐ 🟡 How do you rank by multiple criteria with tie-breakers (score descending, then name ascending)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know that ORDER BY inside OVER accepts several columns, each with its own direction, and that the extra columns act as tie-breakers.
**Say this in the interview:** "I list the criteria in priority order inside the window's ORDER BY: `score DESC, name ASC`. The second column is only looked at when the first one ties. I use ROW_NUMBER when I need one unique position, and RANK when tied players should share a place."
**Explain simply:**
- A *tie-breaker* is a second (third...) sort column used only when the first column is equal.
- Each column gets its own `ASC` (small to large, the default) or `DESC` (large to small).
- ROW_NUMBER with a full tie-breaker gives every row a different number. RANK ignores the tie-breaker for numbering and still shows the tie.
**Example:** Zoya and Meera both score 92. Sorted by name A to Z, Meera is position 1 and Zoya position 2, but both are rank 1 on score. Arjun, Kabir and Ravi all have 85, so their rank is 3 and the next rank jumps to 6.
**Sample data:**

`students`

| name | score |
|---|---|
| Meera | 92 |
| Arjun | 85 |
| Zoya | 92 |
| Kabir | 85 |
| Lata | 78 |
| Ravi | 85 |
**SQL:**
```sql
SELECT name, score,
       ROW_NUMBER() OVER (ORDER BY score DESC, name ASC) AS position,       -- unique: ties broken by name A->Z
       RANK()       OVER (ORDER BY score DESC)           AS rank_by_score   -- ties share a rank
FROM students
ORDER BY position;
```
**Output:**

| name | score | position | rank_by_score |
|---|---|---|---|
| Meera | 92 | 1 | 1 |
| Zoya | 92 | 2 | 1 |
| Arjun | 85 | 3 | 3 |
| Kabir | 85 | 4 | 3 |
| Ravi | 85 | 5 | 3 |
| Lata | 78 | 6 | 6 |
**pandas equivalent:**
```python
import pandas as pd
import numpy as np

students = pd.DataFrame([
    ('Meera', 92),
    ('Arjun', 85),
    ('Zoya', 92),
    ('Kabir', 85),
    ('Lata', 78),
    ('Ravi', 85)],
    columns=['name', 'score'])

result = students.sort_values(['score', 'name'], ascending=[False, True]).reset_index(drop=True)
result['position'] = range(1, len(result) + 1)
result['rank_by_score'] = result['score'].rank(method='min', ascending=False).astype(int)
# result matches the SQL output row for row (checked by running both)
```
**Edge cases:** If even the tie-breaker columns tie (two students with the same name and score), ROW_NUMBER picks between them arbitrarily, so add a unique column such as `student_id` as the last key. NULL score sorts last in SQLite/MySQL for ASC and first for DESC in PostgreSQL/Oracle.
**Likely follow-ups:**
- How do you sort names Z to A as the tie-breaker? `name DESC`.
- What if the tie-breaker should be a date? Same idea: `score DESC, submitted_at ASC` (earliest wins).
**Common mistakes:** Writing `ORDER BY score, name DESC` and forgetting that DESC applies only to the column right before it; writing `ORDER BY score DESC` only and getting a random order among ties.

### Q57 ⭐ 🟡 How do you create a leaderboard where tied players share a rank and the next rank is not skipped?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you pick DENSE_RANK (no gaps) over RANK (gaps) for the stated requirement.
**Say this in the interview:** "Tied players share a rank and the next rank is not skipped, that is exactly DENSE_RANK. RANK would jump from 1 to 3, DENSE_RANK goes 1, 1, 2."
**Explain simply:**
- *DENSE_RANK* gives equal values the same rank and then continues with the very next number. "Dense" means no holes in the sequence.
- *RANK* also shares a rank on ties but skips numbers after them (two firsts means nobody is second).
- Use `ORDER BY points DESC` so the highest score gets rank 1.
**Example:** Ana and Ben both have 950 points, so both are rank 1. Cy (900) is rank 2 under DENSE_RANK but rank 3 under RANK.
**Sample data:**

`leaderboard`

| player | points |
|---|---|
| Ana | 950 |
| Ben | 950 |
| Cy | 900 |
| Dee | 870 |
| Eli | 870 |
| Fay | 800 |
**SQL:**
```sql
SELECT player, points,
       DENSE_RANK() OVER (ORDER BY points DESC) AS leaderboard_rank,   -- 1,1,2,3,3,4 (no gaps)
       RANK()       OVER (ORDER BY points DESC) AS rank_with_gaps      -- 1,1,3,4,4,6 (for comparison)
FROM leaderboard
ORDER BY points DESC, player;
```
**Output:**

| player | points | leaderboard_rank | rank_with_gaps |
|---|---|---|---|
| Ana | 950 | 1 | 1 |
| Ben | 950 | 1 | 1 |
| Cy | 900 | 2 | 3 |
| Dee | 870 | 3 | 4 |
| Eli | 870 | 3 | 4 |
| Fay | 800 | 4 | 6 |
**pandas equivalent:**
```python
import pandas as pd
import numpy as np

leaderboard = pd.DataFrame([
    ('Ana', 950),
    ('Ben', 950),
    ('Cy', 900),
    ('Dee', 870),
    ('Eli', 870),
    ('Fay', 800)],
    columns=['player', 'points'])

result = leaderboard.sort_values(['points', 'player'], ascending=[False, True]).copy()
result['leaderboard_rank'] = result['points'].rank(method='dense', ascending=False).astype(int)
result['rank_with_gaps'] = result['points'].rank(method='min', ascending=False).astype(int)
# result matches the SQL output row for row (checked by running both)
```
**Edge cases:** NULL points: SQLite and MySQL treat NULL as the smallest value, so under DESC they come last; PostgreSQL and Oracle treat NULL as the largest, so they come first unless you add `NULLS LAST` (from memory; see Q32). Decide whether unscored players should appear at all (filter `WHERE points IS NOT NULL`).
**Likely follow-ups:**
- How many players share the top rank? `COUNT(*) ... WHERE leaderboard_rank = 1` in a wrapper query.
- Can I get the 2nd place group? Filter `leaderboard_rank = 2`.
**Common mistakes:** Using RANK and being surprised by the gap; forgetting `DESC` so the lowest score is rank 1; filtering the rank in the same SELECT instead of a wrapper query.

### Q58 ⭐ 🟡 Write a query to rank months by revenue within each year.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Two-step thinking: first collapse to one row per month with GROUP BY, then rank those monthly totals inside each year.
**Say this in the interview:** "I first total revenue per month in a CTE, then use RANK with PARTITION BY year ordered by revenue descending, so every year gets its own 1, 2, 3 ranking of months."
**Explain simply:**
- You cannot rank months directly on raw orders, because many orders fall in one month. Group first so there is one row per month.
- A *CTE* (`WITH name AS (...)`) is a named temporary result you can query right after, which keeps the steps readable.
- `PARTITION BY yr` restarts the ranking each year, so January 2025 competes only with other 2025 months.
**Example:** 2024 monthly revenue: Jan 5,000 (3,000 + 2,000), Feb 7,000, Mar 5,000. February is rank 1; January and March tie at rank 2.
**Sample data:**

`orders`

| order_id | order_date | amount |
|---|---|---|
| 1 | 2024-01-10 | 3000 |
| 2 | 2024-01-25 | 2000 |
| 3 | 2024-02-14 | 7000 |
| 4 | 2024-03-05 | 5000 |
| 5 | 2025-01-18 | 4000 |
| 6 | 2025-02-20 | 6500 |
| 7 | 2025-03-11 | 3000 |
**SQL:**
```sql
WITH monthly AS (
    SELECT strftime('%Y', order_date) AS yr,
           strftime('%m', order_date) AS mon,
           SUM(amount)                AS revenue
    FROM orders
    GROUP BY strftime('%Y', order_date), strftime('%m', order_date)
)
SELECT yr, mon, revenue,
       RANK() OVER (PARTITION BY yr ORDER BY revenue DESC) AS month_rank
FROM monthly
ORDER BY yr, month_rank, mon;
```
Other dialects (not run here / from memory): PostgreSQL `EXTRACT(YEAR FROM order_date)` and `EXTRACT(MONTH FROM order_date)`; MySQL `YEAR(order_date)`, `MONTH(order_date)`; SQL Server `YEAR()` / `MONTH()`. Only the date-part functions change; the RANK part is identical.
**Output:**

| yr | mon | revenue | month_rank |
|---|---|---|---|
| 2024 | 02 | 7000 | 1 |
| 2024 | 01 | 5000 | 2 |
| 2024 | 03 | 5000 | 2 |
| 2025 | 02 | 6500 | 1 |
| 2025 | 01 | 4000 | 2 |
| 2025 | 03 | 3000 | 3 |
**pandas equivalent:**
```python
import pandas as pd
import numpy as np

orders = pd.DataFrame([
    (1, '2024-01-10', 3000),
    (2, '2024-01-25', 2000),
    (3, '2024-02-14', 7000),
    (4, '2024-03-05', 5000),
    (5, '2025-01-18', 4000),
    (6, '2025-02-20', 6500),
    (7, '2025-03-11', 3000)],
    columns=['order_id', 'order_date', 'amount'])

o = orders.copy()
o['order_date'] = pd.to_datetime(o['order_date'])
o['yr'] = o['order_date'].dt.strftime('%Y')
o['mon'] = o['order_date'].dt.strftime('%m')
m = o.groupby(['yr', 'mon'], as_index=False)['amount'].sum().rename(columns={'amount': 'revenue'})
m['month_rank'] = m.groupby('yr')['revenue'].rank(method='min', ascending=False).astype(int)
result = m.sort_values(['yr', 'month_rank', 'mon'])
# result matches the SQL output row for row (checked by running both)
```
**Edge cases:** Months with no orders do not appear at all, so they cannot be ranked (add a calendar table if they must show as 0). Ties share a rank under RANK; switch to DENSE_RANK to avoid a gap. Make sure the year is part of the PARTITION, otherwise January 2024 and January 2025 would be mixed.
**Likely follow-ups:**
- How do I get only the best month per year? Wrap the query and filter `month_rank = 1` (ties return more than one month).
- What if the data spans several years but I group only by month? Different years merge into one 'January'; always group by year and month.
**Common mistakes:** Grouping by month name only (merging years); applying RANK to individual orders; using `ORDER BY month` inside OVER instead of revenue.

### Q59 ⭐ 🟡 What does the NTILE(n) function do when rows do not divide evenly into n buckets?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know NTILE does not make equal-value buckets; it makes (nearly) equal-count buckets and the extra rows go to the first buckets.
**Say this in the interview:** "NTILE(n) cuts the ordered rows into n groups of roughly equal size. If the rows do not divide evenly, the first few buckets get one extra row each. With 10 rows and 4 buckets the sizes are 3, 3, 2, 2."
**Explain simply:**
- *NTILE(n)* hands out bucket numbers 1 to n in the order you specify, like dealing a sorted list of employees into n piles.
- Rule: with `r` leftover rows (`rows mod n`), buckets 1 to r are one row bigger than the rest.
- If there are fewer rows than buckets, the later buckets are simply empty (3 rows into 4 buckets uses buckets 1, 2, 3).
**Example:** 10 employees into 4 salary quartiles: 10 / 4 = 2 remainder 2, so buckets 1 and 2 hold 3 people, buckets 3 and 4 hold 2.
**Sample data:**

`employees`

| emp_id | salary |
|---|---|
| 1 | 95000 |
| 2 | 90000 |
| 3 | 85000 |
| 4 | 80000 |
| 5 | 75000 |
| 6 | 70000 |
| 7 | 65000 |
| 8 | 60000 |
| 9 | 55000 |
| 10 | 50000 |
**SQL:**
```sql
-- 10 rows into 4 buckets
SELECT emp_id, salary,
       NTILE(4) OVER (ORDER BY salary DESC) AS bucket
FROM employees
ORDER BY salary DESC;

-- Only 3 rows into 4 buckets
WITH top3 AS (SELECT * FROM employees ORDER BY salary DESC LIMIT 3)
SELECT emp_id, salary, NTILE(4) OVER (ORDER BY salary DESC) AS bucket
FROM top3;
```
**Output:**

*10 rows into 4 buckets*

| emp_id | salary | bucket |
|---|---|---|
| 1 | 95000 | 1 |
| 2 | 90000 | 1 |
| 3 | 85000 | 1 |
| 4 | 80000 | 2 |
| 5 | 75000 | 2 |
| 6 | 70000 | 2 |
| 7 | 65000 | 3 |
| 8 | 60000 | 3 |
| 9 | 55000 | 4 |
| 10 | 50000 | 4 |

*Only 3 rows into 4 buckets*

| emp_id | salary | bucket |
|---|---|---|
| 1 | 95000 | 1 |
| 2 | 90000 | 2 |
| 3 | 85000 | 3 |
**pandas equivalent:**
```python
import pandas as pd
import numpy as np

employees = pd.DataFrame([
    (1, 95000),
    (2, 90000),
    (3, 85000),
    (4, 80000),
    (5, 75000),
    (6, 70000),
    (7, 65000),
    (8, 60000),
    (9, 55000),
    (10, 50000)],
    columns=['emp_id', 'salary'])

n, k = len(employees), 4
sizes = [n // k + (1 if i < n % k else 0) for i in range(k)]   # first (n % k) buckets get one extra row
result = employees.sort_values('salary', ascending=False).reset_index(drop=True)
result['bucket'] = np.repeat(range(1, k + 1), sizes)
# result matches the SQL output row for row (checked by running both)
```
**Edge cases:** Ties are not kept together: two equal salaries can land in different buckets because NTILE only counts rows (add a tie-breaker in ORDER BY for repeatable results). NULLs are ordered like any value, so decide where they go. In MySQL, PostgreSQL, SQL Server and Oracle NTILE behaves the same way (from memory).
**Likely follow-ups:**
- Are the buckets equal in salary range? No, equal in headcount.
- How do I get a true 'top 25 percent' with ties kept together? Use PERCENT_RANK or CUME_DIST (see Q61).
**Common mistakes:** Assuming buckets are equal-sized always; forgetting ORDER BY (then buckets are arbitrary); expecting two equal salaries to share a bucket.

### Q60 ⭐ 🟡 How would you use ROW_NUMBER to pick a random sample of 2 employees per department?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can combine a random shuffle with ROW_NUMBER and a filter, and handle departments with fewer than 2 people.
**Say this in the interview:** "I number the employees in each department in a random order using ORDER BY RANDOM(), then keep row numbers 1 and 2. Departments with fewer than two people just return what they have."
**Explain simply:**
- `RANDOM()` gives each row a random number, so ordering by it is a shuffle. Because the shuffle sits inside the window, every department is shuffled separately.
- `ROW_NUMBER` then labels the shuffled rows 1, 2, 3... and `WHERE rn <= 2` keeps two per department.
- The result changes on every run. That is the point of a random sample, so it cannot be compared row by row with pandas.
**Example:** A survey team wants 2 random employees per department to interview about engagement. Eng has 4 people and Sales 3, so each gives 2; HR has only Hari so Hari is returned alone.
**Sample data:**

`employees`

| emp_id | emp_name | dept |
|---|---|---|
| 1 | Asha | Eng |
| 2 | Bala | Eng |
| 3 | Chitra | Eng |
| 4 | Dev | Eng |
| 5 | Esha | Sales |
| 6 | Farah | Sales |
| 7 | Gita | Sales |
| 8 | Hari | HR |
**SQL:**
```sql
SELECT dept, emp_name
FROM (
    SELECT dept, emp_name,
           ROW_NUMBER() OVER (PARTITION BY dept ORDER BY RANDOM()) AS rn   -- shuffle inside each department
    FROM employees
) AS shuffled
WHERE rn <= 2
ORDER BY dept, emp_name;
```
Random function by dialect: SQLite and PostgreSQL `RANDOM()`, MySQL `RAND()`, SQL Server `NEWID()` (not run here / from memory). Output below is from one real run; yours will differ.
**Output:**

| dept | emp_name |
|---|---|
| Eng | Bala |
| Eng | Dev |
| HR | Hari |
| Sales | Farah |
| Sales | Gita |
**pandas equivalent:**
```python
import pandas as pd
import numpy as np

employees = pd.DataFrame([
    (1, 'Asha', 'Eng'),
    (2, 'Bala', 'Eng'),
    (3, 'Chitra', 'Eng'),
    (4, 'Dev', 'Eng'),
    (5, 'Esha', 'Sales'),
    (6, 'Farah', 'Sales'),
    (7, 'Gita', 'Sales'),
    (8, 'Hari', 'HR')],
    columns=['emp_id', 'emp_name', 'dept'])

result = (employees.sample(frac=1, random_state=7)      # shuffle all rows
                .groupby('dept').head(2)                # keep the first 2 of each department
                .sort_values(['dept', 'emp_name']).reset_index(drop=True))
```
**Edge cases:** Not reproducible unless you control a seed (SQLite and PostgreSQL `RANDOM()` have no simple per-query seed; pandas uses `random_state`). Departments smaller than 2 return fewer rows. On a huge table a full shuffle is expensive.
**Likely follow-ups:**
- How would I make it repeatable? Store the sample, or order by a hash such as `MD5(emp_id || 'seed')` instead of RANDOM().
- Why not `ORDER BY RANDOM() LIMIT 2`? That samples 2 rows overall, not per department.
**Common mistakes:** Using `ORDER BY RANDOM() LIMIT 2` (one sample for the whole table); leaving out PARTITION BY; forgetting the wrapper so `WHERE rn <= 2` fails.

### Q61 ⭐ 🟡 Write a query to assign a 'salary band' (top 25 percent, middle, bottom 25 percent) using NTILE or PERCENT_RANK.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Turning a rank into business labels with CASE, and knowing the two ways to define 'top 25 percent'.
**Say this in the interview:** "I can use NTILE(4) and label bucket 1 as top, 4 as bottom. Or I use PERCENT_RANK, which gives each person a position between 0 and 1, and label 0.75 and above as top and 0.25 and below as bottom. NTILE splits by headcount, PERCENT_RANK splits by position and keeps ties together."
**Explain simply:**
- *NTILE(4)* deals sorted rows into 4 piles of near-equal size (quartiles).
- *PERCENT_RANK()* = (rank - 1) / (rows - 1): the lowest value gets 0, the highest gets 1. Equal values get the same number.
- `CASE WHEN ... THEN ... END` is SQL's if/else: it turns a number into a label.
**Example:** 8 employees, salaries 50k to 120k. Top 25% = Asha and Bala, Bottom 25% = Gita and Hari, the other four are Middle (both methods agree here).
**Sample data:**

`employees`

| emp_id | emp_name | salary |
|---|---|---|
| 1 | Asha | 120000 |
| 2 | Bala | 110000 |
| 3 | Chitra | 100000 |
| 4 | Dev | 90000 |
| 5 | Esha | 80000 |
| 6 | Farah | 70000 |
| 7 | Gita | 60000 |
| 8 | Hari | 50000 |
**SQL:**
```sql
WITH s AS (
    SELECT emp_name, salary,
           NTILE(4)       OVER (ORDER BY salary DESC) AS q,    -- 1 = top quarter
           PERCENT_RANK() OVER (ORDER BY salary)      AS pr    -- 0 (lowest) to 1 (highest)
    FROM employees
)
SELECT emp_name, salary,
       CASE WHEN q = 1 THEN 'Top 25%' WHEN q = 4 THEN 'Bottom 25%' ELSE 'Middle' END AS band_ntile,
       ROUND(pr, 3) AS pct_rank,
       CASE WHEN pr >= 0.75 THEN 'Top 25%' WHEN pr <= 0.25 THEN 'Bottom 25%' ELSE 'Middle' END AS band_pct_rank
FROM s
ORDER BY salary DESC;
```
**Output:**

| emp_name | salary | band_ntile | pct_rank | band_pct_rank |
|---|---|---|---|---|
| Asha | 120000 | Top 25% | 1 | Top 25% |
| Bala | 110000 | Top 25% | 0.857 | Top 25% |
| Chitra | 100000 | Middle | 0.714 | Middle |
| Dev | 90000 | Middle | 0.571 | Middle |
| Esha | 80000 | Middle | 0.429 | Middle |
| Farah | 70000 | Middle | 0.286 | Middle |
| Gita | 60000 | Bottom 25% | 0.143 | Bottom 25% |
| Hari | 50000 | Bottom 25% | 0 | Bottom 25% |
**pandas equivalent:**
```python
import pandas as pd
import numpy as np

employees = pd.DataFrame([
    (1, 'Asha', 120000),
    (2, 'Bala', 110000),
    (3, 'Chitra', 100000),
    (4, 'Dev', 90000),
    (5, 'Esha', 80000),
    (6, 'Farah', 70000),
    (7, 'Gita', 60000),
    (8, 'Hari', 50000)],
    columns=['emp_id', 'emp_name', 'salary'])

n = len(employees)
r = employees.sort_values('salary', ascending=False).reset_index(drop=True).copy()
q = np.repeat(range(1, 5), [n // 4 + (1 if i < n % 4 else 0) for i in range(4)])
r['band_ntile'] = np.select([q == 1, q == 4], ['Top 25%', 'Bottom 25%'], 'Middle')
pr = (r['salary'].rank(method='min') - 1) / (n - 1)
r['pct_rank'] = pr.round(3)
r['band_pct_rank'] = np.select([pr >= 0.75, pr <= 0.25], ['Top 25%', 'Bottom 25%'], 'Middle')
result = r[['emp_name', 'salary', 'band_ntile', 'pct_rank', 'band_pct_rank']]
# result matches the SQL output row for row (checked by running both)
```
**Edge cases:** With ties, NTILE can put two equal salaries in different bands while PERCENT_RANK keeps them together. With a row count not divisible by 4, NTILE bands have unequal sizes. A single-row table makes PERCENT_RANK 0 (it avoids dividing by zero). PERCENT_RANK is available in PostgreSQL, MySQL 8, SQL Server, Oracle and SQLite 3.25+.
**Likely follow-ups:**
- Which is better for ties? PERCENT_RANK (or CUME_DIST).
- How do I get 4 equal salary-range bands instead? Compute `(salary - MIN) / (MAX - MIN)` and cut with CASE.
**Common mistakes:** Ordering NTILE ascending and then calling bucket 1 the 'top'; hard-coding salaries instead of using the rank; forgetting that the bands overlap by definition at the 0.25 and 0.75 edges.

### Q62 ⭐ 🔴 How do window functions perform on large tables, and how would an index on the PARTITION BY/ORDER BY columns help?
**Asked at:** commonly asked (no company-specific report found); more typical for experienced or product-company rounds
**What the interviewer is checking:** Whether you understand that a window function has to sort (or read pre-sorted) data per partition, and what an index can save.
**Say this in the interview:** "A window function needs the rows grouped by the PARTITION BY columns and sorted by the ORDER BY columns. Without help the database sorts the whole table, which is the expensive part on a large table. A composite index on (partition column, order column) lets it read rows already in order and skip that sort."
**Explain simply:**
- An *index* is a pre-sorted lookup structure on one or more columns, like the alphabetical index at the back of a book.
- Cost drivers: the sort, memory for each partition, and reading wide rows. Selecting only the columns you need helps.
- A matching index is (partition columns, then order columns in the same direction). It can let the engine stream rows in order; whether it actually does depends on the database and the query plan, so always check the plan.
- Filter early: put a `WHERE` on the base table (e.g. only active employees) so fewer rows enter the window.
- Top-N per group with a small N can also be faster with a LATERAL / CROSS APPLY join plus an index (see Q53), because it reads only N rows per group (from memory).
**Example:** Payroll table with 50,000 rows and 5 departments: top 3 salaries per department needs the rows sorted by department and salary. With the index the plan switches from a temp sort to an index scan.
**SQL:**
```sql
CREATE INDEX idx_dept_salary ON big (dept, salary DESC);   -- partition column first, then the ORDER BY column

SELECT * FROM (
    SELECT emp_id, dept, salary,
           ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn
    FROM big
) AS t
WHERE rn <= 3;

-- see how the database plans it (SQLite syntax; PostgreSQL uses EXPLAIN (ANALYZE))
EXPLAIN QUERY PLAN <the SELECT above>;
```
**Output:**

Table `big` was generated with 50,000 rows (5 departments, random salaries). Real SQLite 3.49 `EXPLAIN QUERY PLAN` output:

- Before the index: `CO-ROUTINE (subquery-1)`, `CO-ROUTINE (subquery-3)`, `SCAN big`, `USE TEMP B-TREE FOR ORDER BY`, `SCAN (subquery-3)`, `SCAN (subquery-1)`
- After the index: `CO-ROUTINE (subquery-1)`, `CO-ROUTINE (subquery-3)`, `SCAN big USING INDEX idx_dept_salary`, `SCAN (subquery-3)`, `SCAN (subquery-1)`
- Rows returned either way: 15 (5 departments x 3).
**Edge cases:** An index only helps if its column order and direction match PARTITION BY then ORDER BY. A function on the column (`UPPER(dept)`) or a different sort order may prevent use. Very wide partitions (one giant department) still need big memory. Index syntax such as `DESC` in the index definition and `INCLUDE` columns differs by database (SQL Server and PostgreSQL support covering indexes; from memory).
**Likely follow-ups:**
- Does the index make window functions free? No, it can only remove the sort; the numbering is still computed row by row.
- How would you check? Read the execution plan (EXPLAIN) and look for a sort step before and after.
**Common mistakes:** Indexing only the ORDER BY column; putting the partition column second; assuming an index is used without checking the plan; selecting `*` on a wide table inside the window query.

### Q63 ⭐ 🔴 Write a query to find the top 3 products per category along with each product's share of the category's revenue.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know the order: window functions are calculated before the rank filter, so the total still includes the products you later drop.
**Say this in the interview:** "In one CTE I compute each product's rank and the category total using two windows, both partitioned by category. Because the filter on rank happens in the outer query, the total still includes every product, so the share is true share of the whole category."
**Explain simply:**
- `SUM(revenue) OVER (PARTITION BY category)` is a *window total*: it puts the category's total next to every product row without collapsing rows.
- Share = product revenue / category total x 100.
- The `WHERE rnk <= 3` must sit in the outer query. If you filter before the window runs, the total shrinks to the top 3 only and every share is inflated.
**Example:** Electronics total is 1,300. Phone 500 / 1,300 = 38.5%, Laptop 30.8%, TV 23.1%. Those three cover 92.4% of the category; Cable's 7.7% is not shown but is still in the 1,300.
**Sample data:**

`products`

| category | product | revenue |
|---|---|---|
| Electronics | Phone | 500 |
| Electronics | Laptop | 400 |
| Electronics | TV | 300 |
| Electronics | Cable | 100 |
| Apparel | Jeans | 250 |
| Apparel | Shirt | 200 |
| Apparel | Jacket | 150 |
| Apparel | Socks | 100 |
**SQL:**
```sql
WITH r AS (
    SELECT category, product, revenue,
           SUM(revenue) OVER (PARTITION BY category)                      AS category_total,  -- over ALL products
           RANK()       OVER (PARTITION BY category ORDER BY revenue DESC) AS rnk
    FROM products
)
SELECT category, product, revenue, rnk,
       ROUND(100.0 * revenue / category_total, 1) AS share_pct
FROM r
WHERE rnk <= 3
ORDER BY category, rnk;
```
**Output:**

| category | product | revenue | rnk | share_pct |
|---|---|---|---|---|
| Apparel | Jeans | 250 | 1 | 35.7 |
| Apparel | Shirt | 200 | 2 | 28.6 |
| Apparel | Jacket | 150 | 3 | 21.4 |
| Electronics | Phone | 500 | 1 | 38.5 |
| Electronics | Laptop | 400 | 2 | 30.8 |
| Electronics | TV | 300 | 3 | 23.1 |
**pandas equivalent:**
```python
import pandas as pd
import numpy as np

products = pd.DataFrame([
    ('Electronics', 'Phone', 500),
    ('Electronics', 'Laptop', 400),
    ('Electronics', 'TV', 300),
    ('Electronics', 'Cable', 100),
    ('Apparel', 'Jeans', 250),
    ('Apparel', 'Shirt', 200),
    ('Apparel', 'Jacket', 150),
    ('Apparel', 'Socks', 100)],
    columns=['category', 'product', 'revenue'])

p = products.copy()
p['category_total'] = p.groupby('category')['revenue'].transform('sum')
p['rnk'] = p.groupby('category')['revenue'].rank(method='min', ascending=False).astype(int)
p['share_pct'] = (100.0 * p['revenue'] / p['category_total']).round(1)
result = p[p['rnk'] <= 3].sort_values(['category', 'rnk'])[['category', 'product', 'revenue', 'rnk', 'share_pct']]
# result matches the SQL output row for row (checked by running both)
```
**Edge cases:** Ties at rank 3 return more than 3 rows under RANK (use ROW_NUMBER with a tie-breaker for exactly 3). Category total of 0 gives a divide-by-zero error in SQL Server/PostgreSQL, so guard with `NULLIF(category_total, 0)`. NULL revenue is skipped by SUM but sorts oddly in ORDER BY.
**Likely follow-ups:**
- How do I show the cumulative share of the top 3? Add a running `SUM(revenue) OVER (PARTITION BY category ORDER BY revenue DESC)` (Part 6).
- Integer division? In SQL Server/PostgreSQL `revenue / total` with two integers is integer division, so multiply by 100.0 first.
**Common mistakes:** Filtering the top 3 in a subquery first and then computing the total (inflated shares); integer division returning 0; mixing GROUP BY and window functions without a CTE.

### Q64 ⭐ 🔴 How would you find departments where the top earner earns more than twice the second-highest earner?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Pivoting ranks into columns (top and second side by side) and handling the departments that have fewer than two people.
**Say this in the interview:** "I number employees per department by salary descending, then in the outer query I pull the rank-1 and rank-2 salaries into two columns with MAX(CASE WHEN ...) and keep departments where the first is more than double the second. One-person departments have no second salary, so they drop out automatically."
**Explain simply:**
- `MAX(CASE WHEN rn = 1 THEN salary END)` picks the salary of the person numbered 1. It is the usual trick to turn rows into columns (a *pivot*).
- Departments with only one employee give NULL for the second salary; `x > 2 * NULL` is unknown, so the row is filtered out.
- I used ROW_NUMBER, so 'second-highest earner' means the second person. If two people tie for the top, the ratio is 1, correctly not more than 2.
**Example:** Finance: 300,000 vs 100,000 is 3 times, so it qualifies. HR: 150,000 vs 80,000 is 1.9 times, no. Sales: 100,000 and 100,000 tie, ratio 1, no. Ops has one person, skipped.
**Sample data:**

`employees`

| emp_id | dept | salary |
|---|---|---|
| 1 | Eng | 200000 |
| 2 | Eng | 90000 |
| 3 | HR | 150000 |
| 4 | HR | 80000 |
| 5 | Sales | 100000 |
| 6 | Sales | 100000 |
| 7 | Ops | 80000 |
| 8 | Finance | 300000 |
| 9 | Finance | 100000 |
**SQL:**
```sql
WITH r AS (
    SELECT dept, salary,
           ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn
    FROM employees
)
SELECT dept,
       MAX(CASE WHEN rn = 1 THEN salary END) AS top_salary,
       MAX(CASE WHEN rn = 2 THEN salary END) AS second_salary
FROM r
GROUP BY dept
HAVING MAX(CASE WHEN rn = 1 THEN salary END) > 2 * MAX(CASE WHEN rn = 2 THEN salary END)
ORDER BY dept;
```
**Output:**

| dept | top_salary | second_salary |
|---|---|---|
| Eng | 200000 | 90000 |
| Finance | 300000 | 100000 |
**pandas equivalent:**
```python
import pandas as pd
import numpy as np

employees = pd.DataFrame([
    (1, 'Eng', 200000),
    (2, 'Eng', 90000),
    (3, 'HR', 150000),
    (4, 'HR', 80000),
    (5, 'Sales', 100000),
    (6, 'Sales', 100000),
    (7, 'Ops', 80000),
    (8, 'Finance', 300000),
    (9, 'Finance', 100000)],
    columns=['emp_id', 'dept', 'salary'])

s = employees.sort_values(['dept', 'salary'], ascending=[True, False])
g = s.groupby('dept')['salary'].agg(top_salary='first',
                                    second_salary=lambda x: x.iloc[1] if len(x) > 1 else np.nan)
result = g[g['top_salary'] > 2 * g['second_salary']].astype(int).reset_index()
# result matches the SQL output row for row (checked by running both)
```
**Edge cases:** Ambiguity: 'second-highest' can mean the second person (ROW_NUMBER) or the second distinct salary value (DENSE_RANK = 2). Ask which one is wanted. NULL salaries sort last or first by dialect, which can change who is second. Exactly 2x does not qualify with `>`; use `>=` if the manager means 'at least double'.
**Likely follow-ups:**
- Alternative without pivoting? Use `LEAD(salary) OVER (PARTITION BY dept ORDER BY salary DESC)` on the top row (LEAD is Part 6).
- What if I want the second distinct value? Use DENSE_RANK instead of ROW_NUMBER.
**Common mistakes:** Using RANK and then looking for rank 2 (it does not exist when two people tie for first); comparing with `/` using integers and getting integer division; forgetting that a single-person department has no second row.

### Q65 ⭐ 🔴 How would you rank hierarchical data (employees under each manager) combining a ranking function with a self join?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you join a table to itself to bring in the manager's name, then rank inside each manager's team, and do you know recursive CTEs exist for deeper levels.
**Say this in the interview:** "I self-join the employees table: one copy plays the employee, the other plays the manager. Then I rank with PARTITION BY manager ordered by the measure I care about. For full multi-level trees I add a recursive CTE to get the level first."
**Explain simply:**
- *Self join*: joining a table to itself using different aliases (`e` and `m`) so one row can point at another row (employee to manager).
- `PARTITION BY e.manager_id` means each manager's direct reports are ranked as their own list.
- A *recursive CTE* repeatedly joins to its own previous result to walk down levels (CEO, managers, staff); the second query ranks people within each level.
**Example:** Ravi's team: Uma 95,000 is rank 1, Tom and Vik both 90,000 share rank 2. Sunita's team: Xan 100,000 then Wen 85,000.
**Sample data:**

`employees`

| emp_id | emp_name | manager_id | salary |
|---|---|---|---|
| 1 | Priya | NULL | 300000 |
| 2 | Ravi | 1 | 150000 |
| 3 | Sunita | 1 | 140000 |
| 4 | Tom | 2 | 90000 |
| 5 | Uma | 2 | 95000 |
| 6 | Vik | 2 | 90000 |
| 7 | Wen | 3 | 85000 |
| 8 | Xan | 3 | 100000 |
**SQL:**
```sql
-- Rank direct reports inside each manager's team
SELECT m.emp_name AS manager, e.emp_name AS employee, e.salary,
       RANK() OVER (PARTITION BY e.manager_id ORDER BY e.salary DESC) AS rank_in_team,
       COUNT(*) OVER (PARTITION BY e.manager_id)                       AS team_size
FROM employees e
JOIN employees m ON e.manager_id = m.emp_id      -- self join: the same table used twice (e = employee, m = manager)
ORDER BY manager, rank_in_team, employee;

-- Rank by organisation level (recursive CTE)
WITH RECURSIVE tree AS (
    SELECT emp_id, emp_name, salary, 1 AS lvl FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.emp_id, e.emp_name, e.salary, t.lvl + 1
    FROM employees e JOIN tree t ON e.manager_id = t.emp_id
)
SELECT lvl, emp_name, salary,
       RANK() OVER (PARTITION BY lvl ORDER BY salary DESC) AS rank_in_level
FROM tree
ORDER BY lvl, rank_in_level, emp_name;
```
Recursive CTE syntax: PostgreSQL, MySQL 8 and SQLite use `WITH RECURSIVE`; SQL Server and Oracle write `WITH` without RECURSIVE (from memory, not run here).
**Output:**

*Rank direct reports inside each manager's team*

| manager | employee | salary | rank_in_team | team_size |
|---|---|---|---|---|
| Priya | Ravi | 150000 | 1 | 2 |
| Priya | Sunita | 140000 | 2 | 2 |
| Ravi | Uma | 95000 | 1 | 3 |
| Ravi | Tom | 90000 | 2 | 3 |
| Ravi | Vik | 90000 | 2 | 3 |
| Sunita | Xan | 100000 | 1 | 2 |
| Sunita | Wen | 85000 | 2 | 2 |

*Rank by organisation level (recursive CTE)*

| lvl | emp_name | salary | rank_in_level |
|---|---|---|---|
| 1 | Priya | 300000 | 1 |
| 2 | Ravi | 150000 | 1 |
| 2 | Sunita | 140000 | 2 |
| 3 | Xan | 100000 | 1 |
| 3 | Uma | 95000 | 2 |
| 3 | Tom | 90000 | 3 |
| 3 | Vik | 90000 | 3 |
| 3 | Wen | 85000 | 5 |
**pandas equivalent:**
```python
import pandas as pd
import numpy as np

employees = pd.DataFrame([
    (1, 'Priya', None, 300000),
    (2, 'Ravi', 1.0, 150000),
    (3, 'Sunita', 1.0, 140000),
    (4, 'Tom', 2.0, 90000),
    (5, 'Uma', 2.0, 95000),
    (6, 'Vik', 2.0, 90000),
    (7, 'Wen', 3.0, 85000),
    (8, 'Xan', 3.0, 100000)],
    columns=['emp_id', 'emp_name', 'manager_id', 'salary'])

m = employees[['emp_id', 'emp_name']].rename(columns={'emp_id': 'manager_id', 'emp_name': 'manager'})
j = employees.merge(m, on='manager_id')                      # inner join, like the SQL
j['rank_in_team'] = j.groupby('manager_id')['salary'].rank(method='min', ascending=False).astype(int)
j['team_size'] = j.groupby('manager_id')['emp_id'].transform('count')
result = (j.rename(columns={'emp_name': 'employee'})
           .sort_values(['manager', 'rank_in_team', 'employee'])
           [['manager', 'employee', 'salary', 'rank_in_team', 'team_size']])
# result matches the SQL output row for row (checked by running both)
```
**Edge cases:** The top boss has NULL manager_id, so an inner join drops them (use LEFT JOIN to keep, and their manager shows NULL). Cycles in bad data (A reports to B, B to A) make a recursive CTE loop forever; add a depth limit. Ties in salary share a rank under RANK.
**Likely follow-ups:**
- How do I show only each manager's top performer? Wrap and filter `rank_in_team = 1`.
- Why not just GROUP BY manager? That gives one row per manager (e.g. max salary), not each person's rank.
**Common mistakes:** Joining on the wrong columns (`e.emp_id = m.manager_id` reverses the direction); forgetting aliases so column names clash; partitioning by manager name when two managers share a name instead of by manager_id.

### Q66 ⭐ 🔴 Write a query to find the top 3 customers per city by order count, breaking ties by most recent order date.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Three-layer pattern: GROUP BY to count, window to rank with a multi-column tie-breaker, outer filter for top 3.
**Say this in the interview:** "First I count orders and find the latest order date per customer, grouped by city. Then I number customers in each city by order count descending, then latest order date descending. ROW_NUMBER makes sure I return exactly three per city even with ties, and the unique customer id is the final tie-breaker."
**Explain simply:**
- Count per customer needs `GROUP BY`. The ranking needs a *window function* and cannot be done in the same step as the filter, so I use two CTEs (named temporary results).
- `MAX(order_date)` gives each customer's most recent order, used only to break ties.
- Order of tie-breakers: more orders first, then more recent last order, then smaller customer_id so the result never changes between runs.
**Example:** Mumbai: Anil has 3 orders (position 1), Bina 2 (position 2). Charu and Dinesh both have 1; Dinesh ordered later (28 Mar vs 25 Feb) so he takes position 3 and Charu is dropped.
**Sample data:**

`customers`

| customer_id | name | city |
|---|---|---|
| 1 | Anil | Mumbai |
| 2 | Bina | Mumbai |
| 3 | Charu | Mumbai |
| 4 | Dinesh | Mumbai |
| 5 | Esha | Pune |
| 6 | Farid | Pune |
| 7 | Gauri | Pune |

`orders`

| order_id | customer_id | order_date |
|---|---|---|
| 1 | 1 | 2025-01-05 |
| 2 | 1 | 2025-02-10 |
| 3 | 1 | 2025-03-15 |
| 4 | 2 | 2025-01-20 |
| 5 | 2 | 2025-03-01 |
| 6 | 3 | 2025-02-25 |
| 7 | 4 | 2025-03-28 |
| 8 | 5 | 2025-01-12 |
| 9 | 5 | 2025-02-02 |
| 10 | 6 | 2025-03-05 |
| 11 | 7 | 2025-01-30 |
**SQL:**
```sql
WITH stats AS (
    SELECT c.city, c.name, c.customer_id,
           COUNT(o.order_id)  AS orders,
           MAX(o.order_date)  AS last_order
    FROM customers c
    JOIN orders o ON o.customer_id = c.customer_id
    GROUP BY c.city, c.name, c.customer_id
),
ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY city
                              ORDER BY orders DESC, last_order DESC, customer_id) AS rn
    FROM stats
)
SELECT city, name, orders, last_order, rn AS position
FROM ranked
WHERE rn <= 3
ORDER BY city, rn;
```
**Output:**

| city | name | orders | last_order | position |
|---|---|---|---|---|
| Mumbai | Anil | 3 | 2025-03-15 | 1 |
| Mumbai | Bina | 2 | 2025-03-01 | 2 |
| Mumbai | Dinesh | 1 | 2025-03-28 | 3 |
| Pune | Esha | 2 | 2025-02-02 | 1 |
| Pune | Farid | 1 | 2025-03-05 | 2 |
| Pune | Gauri | 1 | 2025-01-30 | 3 |
**pandas equivalent:**
```python
import pandas as pd
import numpy as np

customers = pd.DataFrame([
    (1, 'Anil', 'Mumbai'),
    (2, 'Bina', 'Mumbai'),
    (3, 'Charu', 'Mumbai'),
    (4, 'Dinesh', 'Mumbai'),
    (5, 'Esha', 'Pune'),
    (6, 'Farid', 'Pune'),
    (7, 'Gauri', 'Pune')],
    columns=['customer_id', 'name', 'city'])
orders = pd.DataFrame([
    (1, 1, '2025-01-05'),
    (2, 1, '2025-02-10'),
    (3, 1, '2025-03-15'),
    (4, 2, '2025-01-20'),
    (5, 2, '2025-03-01'),
    (6, 3, '2025-02-25'),
    (7, 4, '2025-03-28'),
    (8, 5, '2025-01-12'),
    (9, 5, '2025-02-02'),
    (10, 6, '2025-03-05'),
    (11, 7, '2025-01-30')],
    columns=['order_id', 'customer_id', 'order_date'])

m = customers.merge(orders, on='customer_id')
s = (m.groupby(['city', 'name', 'customer_id'], as_index=False)
       .agg(orders=('order_id', 'count'), last_order=('order_date', 'max')))
s = s.sort_values(['city', 'orders', 'last_order', 'customer_id'], ascending=[True, False, False, True])
s['position'] = s.groupby('city').cumcount() + 1
result = s[s['position'] <= 3][['city', 'name', 'orders', 'last_order', 'position']]
# result matches the SQL output row for row (checked by running both)
```
**Edge cases:** Customers with zero orders disappear because of the inner join (use LEFT JOIN and COUNT(o.order_id) to keep them with 0). A city with fewer than 3 customers just returns what it has. Date stored as text sorts correctly only in ISO format (YYYY-MM-DD).
**Likely follow-ups:**
- How to keep ties at 3rd place? Use RANK on `orders` only and drop the date tie-breaker.
- Where does the city come from if orders has no city? Join to customers, as above.
**Common mistakes:** Ranking inside the same query as the GROUP BY without a CTE; using DESC on the date but forgetting it on the count; no unique final tie-breaker so results change between runs.

### Q67 ⭐ 🔴 Can you use a window function in GROUP BY, HAVING or another window function? How do you work around it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the clause order (windows run late) and the standard workaround: compute the window in a CTE or subquery, then use it like a normal column.
**Say this in the interview:** "No. Window functions are calculated after WHERE, GROUP BY and HAVING, so those clauses cannot see them, and a window cannot sit inside another window. The fix is always the same: compute the window in a CTE or subquery, then filter, group or window again in the outer query."
**Explain simply:**
- SQL runs in this order: FROM, WHERE, GROUP BY, HAVING, then window functions, then SELECT/ORDER BY. A clause that runs earlier cannot use something computed later.
- The reverse is fine: a window function can take an aggregate as input (`RANK() OVER (ORDER BY SUM(salary))`) because GROUP BY has already run.
- A *CTE* is a named temporary result; the outer query treats the window's answer as a plain column.
- Window inside window (e.g. rank of a running total): compute the inner one in a CTE first.
**Example:** 'Count how many people hold each of the top 3 salary ranks' needs a rank (window) and then a count (GROUP BY): CTE first, group second.
**Sample data:**

`employees`

| emp_id | emp_name | dept | salary |
|---|---|---|---|
| 1 | Asha | Eng | 90000 |
| 2 | Bala | Eng | 70000 |
| 3 | Chitra | Sales | 60000 |
| 4 | Dev | Sales | 60000 |
| 5 | Esha | HR | 55000 |
**SQL:**
```sql
-- These FAIL in SQLite (other major databases also reject them):
-- Window function in WHERE
SELECT emp_name FROM employees WHERE RANK() OVER (ORDER BY salary DESC) = 1;
-- Window function in GROUP BY
SELECT dept, COUNT(*) FROM employees GROUP BY ROW_NUMBER() OVER (ORDER BY salary);
-- Window function in HAVING
SELECT dept FROM employees GROUP BY dept HAVING RANK() OVER (ORDER BY SUM(salary)) = 1;
-- Window inside a window
SELECT SUM(ROW_NUMBER() OVER (ORDER BY salary)) OVER () FROM employees;

-- Allowed: a window can use an aggregate result, because windows run AFTER GROUP BY
SELECT dept, SUM(salary) AS payroll,
       RANK() OVER (ORDER BY SUM(salary) DESC) AS payroll_rank
FROM employees
GROUP BY dept
ORDER BY payroll_rank, dept;

-- Workaround for filtering / grouping / nesting: compute the window in a CTE, then use it
WITH r AS (
    SELECT dept, emp_name, salary,
           RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM employees
)
SELECT rnk, COUNT(*) AS people          -- now rnk is an ordinary column, so GROUP BY and WHERE work
FROM r
WHERE rnk <= 3
GROUP BY rnk
ORDER BY rnk;
```
**Output:**

Real SQLite errors for the four failing statements:

- Window function in WHERE: `misuse of window function RANK()`
- Window function in GROUP BY: `misuse of window function ROW_NUMBER()`
- Window function in HAVING: `misuse of window function RANK()`
- Window inside a window: `misuse of window function ROW_NUMBER()`

*Allowed: window over an aggregate*

| dept | payroll | payroll_rank |
|---|---|---|
| Eng | 160000 | 1 |
| Sales | 120000 | 2 |
| HR | 55000 | 3 |

*Workaround via CTE*

| rnk | people |
|---|---|
| 1 | 1 |
| 2 | 1 |
| 3 | 2 |
**Edge cases:** Error wording differs: PostgreSQL says window functions are not allowed in WHERE/GROUP BY/HAVING, SQL Server says they can only appear in SELECT or ORDER BY (from memory). Snowflake, BigQuery and DuckDB have QUALIFY to filter on a window without a wrapper (see Q70).
**Likely follow-ups:**
- Why does `HAVING` work with SUM but not with RANK? HAVING runs after GROUP BY but before windows.
- Can a window function be in ORDER BY? Yes, SELECT and ORDER BY are the allowed places.
**Common mistakes:** Writing `WHERE rn = 1` in the same SELECT that defines `rn`; assuming an alias defined in SELECT can be used in WHERE; nesting `SUM(RANK() OVER ...) OVER ...` instead of using a CTE.

### Q68 ⭐ 🔴 You see duplicated rank values in your ROW_NUMBER output. What are the likely causes?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Debugging mindset: ROW_NUMBER itself never repeats inside one partition, so where do 'duplicates' come from?
**Say this in the interview:** "Premise check first: ROW_NUMBER cannot repeat within a single partition. If I see repeated numbers it is because of PARTITION BY restarting the count, a join or UNION that repeats rows after numbering, or I am really looking at RANK or DENSE_RANK. I check which of these happened."
**Explain simply:**
- *Partition restart*: with `PARTITION BY dept`, every department has its own 1, 2, 3, so the number 1 appears several times in the whole result. That is correct, not a bug.
- *Row fan-out*: if you number first and then join to a table with several matching rows (employee to projects), the same number is copied onto each match.
- *Wrong function*: RANK and DENSE_RANK give equal numbers on ties by design.
- *Combining result sets*: `UNION ALL` of two numbered queries gives two 1s.
- *Not a unique key*: the number is not an ID; compare it with a real key like `emp_id`.
**Example:** Asha works on two projects, so after the join she appears twice, both rows carrying rn = 1.
**Sample data:**

`employees`

| emp_id | emp_name | dept | salary |
|---|---|---|---|
| 1 | Asha | Eng | 90000 |
| 2 | Bala | Eng | 80000 |
| 3 | Chitra | Sales | 70000 |

`assignments`

| emp_id | project |
|---|---|
| 1 | Alpha |
| 1 | Beta |
| 2 | Alpha |
| 3 | Gamma |
| 3 | Delta |
**SQL:**
```sql
-- Looks like duplicate ranks: numbering happens BEFORE a join that repeats rows
WITH n AS (
    SELECT emp_id, emp_name, ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn
    FROM employees
)
SELECT n.rn, n.emp_name, a.project
FROM n JOIN assignments a ON a.emp_id = n.emp_id
ORDER BY n.rn, a.project;

-- Fix: decide the grain first (one row per employee-project), then number
SELECT ROW_NUMBER() OVER (ORDER BY e.salary DESC, e.emp_id, a.project) AS rn,
       e.emp_name, a.project
FROM employees e JOIN assignments a ON a.emp_id = e.emp_id
ORDER BY rn;

-- Another cause: PARTITION BY restarts the count, so rn = 1 appears once per department
SELECT dept, emp_name,
       ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn
FROM employees
ORDER BY dept, rn;
```
**Output:**

*Cause: number, then join (fan-out)*

| rn | emp_name | project |
|---|---|---|
| 1 | Asha | Alpha |
| 1 | Asha | Beta |
| 2 | Bala | Alpha |
| 3 | Chitra | Delta |
| 3 | Chitra | Gamma |

*Fix: number at the final grain*

| rn | emp_name | project |
|---|---|---|
| 1 | Asha | Alpha |
| 2 | Asha | Beta |
| 3 | Bala | Alpha |
| 4 | Chitra | Delta |
| 5 | Chitra | Gamma |

*Cause: PARTITION BY restarts the count*

| dept | emp_name | rn |
|---|---|---|
| Eng | Asha | 1 |
| Eng | Bala | 2 |
| Sales | Chitra | 1 |
**Edge cases:** If you truly see repeated values with no PARTITION BY and no join, check that you are not reading a RANK column, that the data was not appended twice, and that the number was not computed in two places. NULLs never cause repeated ROW_NUMBER values; they only affect the order.
**Likely follow-ups:**
- How do I deduplicate with it? Number per duplicate key and keep `rn = 1` (Part 10).
- How to prove the cause? Compare `COUNT(*)` with `COUNT(DISTINCT rn)` and inspect the join keys.
**Common mistakes:** Treating the number as a primary key; computing it in a subquery before a one-to-many join; mixing up ROW_NUMBER with RANK; forgetting that PARTITION BY intentionally restarts at 1.

### Q69 ⭐ 🔴 Explain a top-N per group result that returns more than N rows. Why does it happen and how do you fix it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you recognise that RANK/DENSE_RANK cannot promise N rows because ties share a number, and do you know the options to fix it.
**Say this in the interview:** "It happens when I filter `rank <= 3` using RANK or DENSE_RANK: everyone tied at the cutoff gets the same rank, so all of them pass. If the business wants exactly N rows I switch to ROW_NUMBER with a clear tie-breaker; if it wants everyone tied, the extra rows are actually correct."
**Explain simply:**
- A *tie* means two employees have the same value in the ORDER BY column, so the ranking function cannot tell them apart.
- RANK gives tied rows the same number, so 'rank <= 3' can include a 4th person who shares 3rd place.
- DENSE_RANK can return even more rows, because it counts distinct values, not people.
- ROW_NUMBER always gives different numbers, so it returns exactly N, but you must choose a fair tie-breaker (`emp_name`, hire date, id) or the pick is arbitrary.
**Example:** Eng salaries 90k, 80k, 70k, 70k, 60k: Chitra and Dev both are rank 3, so RANK returns 4 people. ROW_NUMBER with `emp_name` as tie-breaker returns Asha, Bala, Chitra only.
**Sample data:**

`employees`

| emp_id | emp_name | dept | salary |
|---|---|---|---|
| 1 | Asha | Eng | 90000 |
| 2 | Bala | Eng | 80000 |
| 3 | Chitra | Eng | 70000 |
| 4 | Dev | Eng | 70000 |
| 5 | Esha | Eng | 60000 |
| 6 | Farah | Sales | 75000 |
| 7 | Gita | Sales | 65000 |
| 8 | Hari | Sales | 55000 |
**SQL:**
```sql
-- RANK <= 3 (returns 4 in Eng)
-- Top 3 with RANK: ties at 3rd place all qualify
SELECT dept, emp_name, salary, rnk
FROM (SELECT dept, emp_name, salary,
             RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk
      FROM employees) t
WHERE rnk <= 3
ORDER BY dept, rnk, emp_name;

-- ROW_NUMBER <= 3 (exactly 3)
-- Exactly 3 per department: ROW_NUMBER with a tie-breaker
SELECT dept, emp_name, salary, rn
FROM (SELECT dept, emp_name, salary,
             ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC, emp_name) AS rn
      FROM employees) t
WHERE rn <= 3
ORDER BY dept, rn;
```
**Output:**

*RANK <= 3 (returns 4 in Eng)*

| dept | emp_name | salary | rnk |
|---|---|---|---|
| Eng | Asha | 90000 | 1 |
| Eng | Bala | 80000 | 2 |
| Eng | Chitra | 70000 | 3 |
| Eng | Dev | 70000 | 3 |
| Sales | Farah | 75000 | 1 |
| Sales | Gita | 65000 | 2 |
| Sales | Hari | 55000 | 3 |

*ROW_NUMBER <= 3 (exactly 3)*

| dept | emp_name | salary | rn |
|---|---|---|---|
| Eng | Asha | 90000 | 1 |
| Eng | Bala | 80000 | 2 |
| Eng | Chitra | 70000 | 3 |
| Sales | Farah | 75000 | 1 |
| Sales | Gita | 65000 | 2 |
| Sales | Hari | 55000 | 3 |
**pandas equivalent:**
```python
import pandas as pd
import numpy as np

employees = pd.DataFrame([
    (1, 'Asha', 'Eng', 90000),
    (2, 'Bala', 'Eng', 80000),
    (3, 'Chitra', 'Eng', 70000),
    (4, 'Dev', 'Eng', 70000),
    (5, 'Esha', 'Eng', 60000),
    (6, 'Farah', 'Sales', 75000),
    (7, 'Gita', 'Sales', 65000),
    (8, 'Hari', 'Sales', 55000)],
    columns=['emp_id', 'emp_name', 'dept', 'salary'])

a = employees.copy()
a['rnk'] = a.groupby('dept')['salary'].rank(method='min', ascending=False).astype(int)
result = a[a['rnk'] <= 3].sort_values(['dept', 'rnk', 'emp_name'])[['dept', 'emp_name', 'salary', 'rnk']]

b = employees.sort_values(['dept', 'salary', 'emp_name'], ascending=[True, False, True]).copy()
b['rn'] = b.groupby('dept').cumcount() + 1
result2 = b[b['rn'] <= 3][['dept', 'emp_name', 'salary', 'rn']]
# result matches the SQL output row for row (checked by running both)
```
**Edge cases:** Decide with the business whether ties should be shown (RANK), or exactly N (ROW_NUMBER with tie-breaker), or N distinct values (DENSE_RANK, Q71). Mention the choice in your answer. If the tie-breaker column can be NULL, its order differs by dialect.
**Likely follow-ups:**
- Is dropping Dev unfair? It can be; if so, report the tie or use RANK and explain the extra row.
- Can I add a tie-breaker to RANK? Yes, but then it stops sharing ranks on the original value and behaves like ROW_NUMBER.
**Common mistakes:** Assuming `rank <= 3` always returns 3 rows; using ROW_NUMBER without a tie-breaker (non-repeatable result); not telling the stakeholder which tie rule was used.

### Q70 ⭐ 🔴 Compare QUALIFY (Snowflake, BigQuery) with a subquery filter for window-function results.
**Asked at:** commonly asked (no company-specific report found); mostly for candidates using Snowflake or BigQuery
**What the interviewer is checking:** Do you know QUALIFY is just shorter syntax for the subquery filter, and which databases do not have it.
**Say this in the interview:** "QUALIFY filters rows after window functions are calculated, the way HAVING filters after GROUP BY. It saves writing a wrapper subquery. Where it is not supported, like PostgreSQL, MySQL or SQL Server, I use the subquery or CTE with the same logic, so the result is identical."
**Explain simply:**
- Normal clause order: WHERE, GROUP BY, HAVING, window functions, QUALIFY, ORDER BY.
- QUALIFY lets you write the window expression directly in the filter, or filter on an alias of a window defined in SELECT (support for aliases depends on the database).
- It is not part of the common SQL standard, so interviews that use PostgreSQL or SQL Server need the subquery version.
- Support (verified here only for DuckDB; others from memory): Snowflake, BigQuery, Teradata and DuckDB have it. PostgreSQL, MySQL, SQL Server and Oracle do not.
- Speed is normally the same, the optimiser treats both alike (from memory, check the plan).
**Example:** Top 2 earners per department: Eng gives Asha and Bala, Sales gives Dev and Esha, HR gives Farah. QUALIFY needs one clause, the subquery needs a wrapper.
**Sample data:**

`employees`

| emp_id | emp_name | dept | salary |
|---|---|---|---|
| 1 | Asha | Eng | 90000 |
| 2 | Bala | Eng | 80000 |
| 3 | Chitra | Eng | 70000 |
| 4 | Dev | Sales | 75000 |
| 5 | Esha | Sales | 65000 |
| 6 | Farah | HR | 55000 |
**SQL:**
```sql
-- QUALIFY: filter on a window function directly (DuckDB, Snowflake, BigQuery, Teradata)
SELECT dept, emp_name, salary
FROM employees
QUALIFY ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) <= 2
ORDER BY dept, salary DESC;

-- Portable subquery version (works everywhere with window functions)
SELECT dept, emp_name, salary
FROM (SELECT dept, emp_name, salary,
             ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn
      FROM employees) t
WHERE rn <= 2
ORDER BY dept, salary DESC;
```
**Output:**

*QUALIFY version, run in DuckDB 1.5 (SQLite has no QUALIFY)*

| dept | emp_name | salary |
|---|---|---|
| Eng | Asha | 90000 |
| Eng | Bala | 80000 |
| HR | Farah | 55000 |
| Sales | Dev | 75000 |
| Sales | Esha | 65000 |

*Subquery version, run in SQLite 3.49 (and DuckDB gives the identical rows)*

| dept | emp_name | salary |
|---|---|---|
| Eng | Asha | 90000 |
| Eng | Bala | 80000 |
| HR | Farah | 55000 |
| Sales | Dev | 75000 |
| Sales | Esha | 65000 |
**Edge cases:** With QUALIFY you cannot filter on a window and use a plain WHERE that depends on the window result; WHERE still runs before the window. Ties follow the same rules as any ranking (ROW_NUMBER exact N, RANK keeps ties). BigQuery historically wanted QUALIFY alongside a WHERE/GROUP BY/HAVING (from memory, may have changed).
**Likely follow-ups:**
- Can QUALIFY replace a CTE for everything? Only for filtering on window results; you still need a CTE to reuse results.
- Is QUALIFY in MySQL? No (from memory).
**Common mistakes:** Using QUALIFY on PostgreSQL or SQL Server and getting a syntax error; filtering the window in WHERE; putting QUALIFY before the FROM clause.

### Q71 ⭐ 🔴 A manager asks: 'show top 3 salaries per department, but I want 3 distinct salary values, not 3 people.' Which function and why?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Choosing DENSE_RANK because the manager counts salary values, not people, and explaining why the other two functions fail.
**Say this in the interview:** "DENSE_RANK. It ranks distinct salary values with no gaps, so `dense_rank <= 3` keeps every person earning one of the top three salary amounts, even if that is more than three people. ROW_NUMBER would count people and RANK would skip numbers after ties."
**Explain simply:**
- *Distinct values* means each different amount is counted once, no matter how many people earn it.
- DENSE_RANK increases by exactly 1 each time the salary changes. Equal salaries share a number.
- RANK skips numbers after a tie (1, 1, 3), so `rank <= 3` can cut off a third distinct value. ROW_NUMBER counts people, which is the opposite of what the manager wants.
- If only the distinct values are wanted, group by (dept, salary) first and rank those.
**Example:** Eng salaries 100k, 100k, 90k, 80k, 70k: the top 3 distinct values are 100k, 90k, 80k, which covers 4 people (70k is dropped). Under ROW_NUMBER the top 3 people would be only Asha, Bala and Chitra.
**Sample data:**

`employees`

| emp_id | emp_name | dept | salary |
|---|---|---|---|
| 1 | Asha | Eng | 100000 |
| 2 | Bala | Eng | 100000 |
| 3 | Chitra | Eng | 90000 |
| 4 | Dev | Eng | 80000 |
| 5 | Esha | Eng | 70000 |
| 6 | Farah | Sales | 80000 |
| 7 | Gita | Sales | 80000 |
| 8 | Hari | Sales | 75000 |
| 9 | Ila | Sales | 60000 |
**SQL:**
```sql
-- People holding the top 3 distinct salaries
-- everyone whose salary is one of the 3 highest DISTINCT salaries in the department
SELECT dept, emp_name, salary, dr
FROM (SELECT dept, emp_name, salary,
             DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS dr
      FROM employees) t
WHERE dr <= 3
ORDER BY dept, dr, emp_name;

-- The 3 distinct values with head-count
-- just the 3 distinct salary values per department, with head-count
SELECT dept, salary, people, dr
FROM (SELECT dept, salary, COUNT(*) AS people,
             DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS dr
      FROM employees
      GROUP BY dept, salary) t
WHERE dr <= 3
ORDER BY dept, dr;
```
**Output:**

*People holding the top 3 distinct salaries*

| dept | emp_name | salary | dr |
|---|---|---|---|
| Eng | Asha | 100000 | 1 |
| Eng | Bala | 100000 | 1 |
| Eng | Chitra | 90000 | 2 |
| Eng | Dev | 80000 | 3 |
| Sales | Farah | 80000 | 1 |
| Sales | Gita | 80000 | 1 |
| Sales | Hari | 75000 | 2 |
| Sales | Ila | 60000 | 3 |

*The 3 distinct values with head-count*

| dept | salary | people | dr |
|---|---|---|---|
| Eng | 100000 | 2 | 1 |
| Eng | 90000 | 1 | 2 |
| Eng | 80000 | 1 | 3 |
| Sales | 80000 | 2 | 1 |
| Sales | 75000 | 1 | 2 |
| Sales | 60000 | 1 | 3 |
**pandas equivalent:**
```python
import pandas as pd
import numpy as np

employees = pd.DataFrame([
    (1, 'Asha', 'Eng', 100000),
    (2, 'Bala', 'Eng', 100000),
    (3, 'Chitra', 'Eng', 90000),
    (4, 'Dev', 'Eng', 80000),
    (5, 'Esha', 'Eng', 70000),
    (6, 'Farah', 'Sales', 80000),
    (7, 'Gita', 'Sales', 80000),
    (8, 'Hari', 'Sales', 75000),
    (9, 'Ila', 'Sales', 60000)],
    columns=['emp_id', 'emp_name', 'dept', 'salary'])

a = employees.copy()
a['dr'] = a.groupby('dept')['salary'].rank(method='dense', ascending=False).astype(int)
result = a[a['dr'] <= 3].sort_values(['dept', 'dr', 'emp_name'])[['dept', 'emp_name', 'salary', 'dr']]

g = employees.groupby(['dept', 'salary'], as_index=False).agg(people=('emp_id', 'count'))
g['dr'] = g.groupby('dept')['salary'].rank(method='dense', ascending=False).astype(int)
result2 = g[g['dr'] <= 3].sort_values(['dept', 'dr'])[['dept', 'salary', 'people', 'dr']]
# result matches the SQL output row for row (checked by running both)
```
**Edge cases:** Ties are the whole point here, so the result can have more than 3 rows. A department with only 2 distinct salaries returns just those. NULL salary forms its own value; filter it with `WHERE salary IS NOT NULL` if it should not count.
**Likely follow-ups:**
- What if they want exactly three people? Use ROW_NUMBER with a tie-breaker (Q69).
- How is the 3rd highest distinct salary different? Filter `dr = 3` (nth-highest is covered in Part 10).
**Common mistakes:** Using RANK and missing the third distinct value after a tie; using `SELECT DISTINCT` on the whole row (names make rows distinct); ranking the raw rows and expecting 3 rows back.

