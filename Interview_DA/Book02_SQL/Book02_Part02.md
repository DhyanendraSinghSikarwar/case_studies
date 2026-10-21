# Book 2 — SQL | Part 2: Aggregates, GROUP BY, HAVING 🟢

**Target:** 55 questions | **Actual:** 57 questions

**Scope:** COUNT/SUM/AVG/MIN/MAX, NULL behaviour in aggregates, GROUP BY on one or more columns, WHERE vs HAVING, duplicate detection with HAVING, conditional aggregation, and ROLLUP/GROUPING SETS. Joins, subqueries/CTEs, window functions and CASE/date function drill-downs belong to other parts.

### Q1 ⭐⭐⭐ 🟢 What are aggregate functions in SQL? Name the five common ones (COUNT, SUM, AVG, MIN, MAX) and say what each does.
**Asked at:** commonly listed in SQL prep guides for data analyst roles (LearnSQL, Indeed India, CCBP); research notes list GROUP BY/HAVING as a standard service-MNC SQL question type
**What the interviewer is checking:** Do you know what an aggregate function is and how it treats NULLs?
**Say this in the interview:** An aggregate function takes many rows and gives back one value. COUNT counts rows, SUM adds, AVG averages, MIN and MAX give the smallest and largest. Except for COUNT(*), they ignore NULLs.
**Explain simply:**
- Aggregate = a function that squeezes a whole column of values into a single answer.
- COUNT(*) counts rows; COUNT(col) counts rows where col is not NULL (NULL means 'no value recorded').
- SUM and AVG work on numbers; MIN and MAX also work on dates and text.
- NULLs are skipped, so AVG divides by the number of non-NULL values, not by all rows.
**Example:** HR wants the payroll summary for 16 employees: headcount, total, average, lowest and highest salary. One row comes back, not 16.
**Sample data:**

`employees`

| emp_id | name | dept | salary | hire_date | status |
|---|---|---|---|---|---|
| 1 | Asha | HR | 40000 | 2020-03-01 | Active |
| 2 | Bala | HR | 45000 | 2021-07-15 | Active |
| 3 | Chitra | HR | 52000 | 2022-02-10 | Left |
| 4 | Deepak | HR | 38000 | 2023-01-05 | Active |
| 5 | Esha | HR | NULL | 2023-06-20 | Active |
| 6 | Farhan | HR | 60000 | 2019-11-11 | Left |
| 7 | Gita | IT | 80000 | 2018-05-01 | Active |
| 8 | Hari | IT | 65000 | 2022-03-14 | Active |
| 9 | Indu | IT | 72000 | 2023-04-01 | Left |
| 10 | Jai | IT | 55000 | 2021-09-09 | Active |
| 11 | Kiran | IT | 90000 | 2022-08-18 | Active |
| 12 | Lata | Sales | 35000 | 2022-01-02 | Active |
| 13 | Manoj | Sales | 42000 | 2023-02-02 | Left |
| 14 | Neha | Sales | 30000 | 2020-10-10 | Active |
| 15 | Omar | Finance | 70000 | 2021-12-01 | Active |
| 16 | Pooja | Finance | 66000 | 2023-05-05 | Active |

**SQL:**
```sql
SELECT COUNT(*)      AS headcount,
       COUNT(salary)  AS salary_recorded,
       SUM(salary)    AS total_salary,
       AVG(salary)    AS avg_salary,
       MIN(salary)    AS lowest,
       MAX(salary)    AS highest
FROM employees;
```
**Output:**

| headcount | salary_recorded | total_salary | avg_salary | lowest | highest |
|---|---|---|---|---|---|
| 16 | 15 | 840000 | 56000 | 30000 | 90000 |

**pandas equivalent:**
```python
import pandas as pd
res = pd.DataFrame([{
    'headcount': len(emp), 'salary_recorded': emp['salary'].count(),
    'total_salary': emp['salary'].sum(), 'avg_salary': emp['salary'].mean(),
    'lowest': emp['salary'].min(), 'highest': emp['salary'].max()}])
# Output:
#  headcount  salary_recorded  total_salary  avg_salary  lowest  highest
#         16               15      840000.0     56000.0 30000.0  90000.0
```
**Edge cases:** Esha has no salary (NULL), so headcount is 16 but salary_recorded is 15 and AVG is over 15 values. On an empty table SUM/AVG/MIN/MAX return NULL and COUNT returns 0.
**Likely follow-ups:**
- Which one does not ignore NULLs? COUNT(*), because it counts rows, not values.
- Can I mix an aggregate with a normal column? Only if that column is in GROUP BY (see Q10).
**Common mistakes:** Thinking AVG treats NULL as zero. It does not; it skips the row.

### Q2 ⭐⭐⭐ 🟢 What does GROUP BY do? Explain with a simple example of counting employees in each department.
**Asked at:** commonly listed in SQL prep guides for data analyst roles (LearnSQL, Indeed India, CCBP); research notes list GROUP BY/HAVING as a standard service-MNC SQL question type
**What the interviewer is checking:** Can you explain grouping in plain words and write the standard headcount query?
**Say this in the interview:** GROUP BY splits the rows into buckets, one per value of the column, and then the aggregate runs once inside each bucket. So counting employees per department gives one row per department.
**Explain simply:**
- Without GROUP BY, an aggregate collapses the whole table into one row.
- With GROUP BY dept, SQL first sorts the rows into piles (HR pile, IT pile ...), then counts each pile.
- Every column in SELECT must be either in GROUP BY or inside an aggregate.
- Result has exactly one row per distinct dept value.
**Example:** HR has 6 employees, IT 5, Sales 3, Finance 2: the report shows 4 rows, not 16.
**Sample data:**

`employees`

| emp_id | name | dept | salary | hire_date | status |
|---|---|---|---|---|---|
| 1 | Asha | HR | 40000 | 2020-03-01 | Active |
| 2 | Bala | HR | 45000 | 2021-07-15 | Active |
| 3 | Chitra | HR | 52000 | 2022-02-10 | Left |
| 4 | Deepak | HR | 38000 | 2023-01-05 | Active |
| 5 | Esha | HR | NULL | 2023-06-20 | Active |
| 6 | Farhan | HR | 60000 | 2019-11-11 | Left |
| 7 | Gita | IT | 80000 | 2018-05-01 | Active |
| 8 | Hari | IT | 65000 | 2022-03-14 | Active |
| 9 | Indu | IT | 72000 | 2023-04-01 | Left |
| 10 | Jai | IT | 55000 | 2021-09-09 | Active |
| 11 | Kiran | IT | 90000 | 2022-08-18 | Active |
| 12 | Lata | Sales | 35000 | 2022-01-02 | Active |
| 13 | Manoj | Sales | 42000 | 2023-02-02 | Left |
| 14 | Neha | Sales | 30000 | 2020-10-10 | Active |
| 15 | Omar | Finance | 70000 | 2021-12-01 | Active |
| 16 | Pooja | Finance | 66000 | 2023-05-05 | Active |

**SQL:**
```sql
SELECT dept, COUNT(*) AS headcount
FROM employees
GROUP BY dept
ORDER BY dept;
```
**Output:**

| dept | headcount |
|---|---|
| Finance | 2 |
| HR | 6 |
| IT | 5 |
| Sales | 3 |

**pandas equivalent:**
```python
res = emp.groupby('dept').size().reset_index(name='headcount').sort_values('dept')
# Output:
#    dept  headcount
# Finance          2
#      HR          6
#      IT          5
#   Sales          3
```
**Edge cases:** A NULL dept would form its own group (shown as NULL). Departments with no employees do not appear at all (see Q31 for the fix).
**Likely follow-ups:**
- Does GROUP BY sort? Not guaranteed; add ORDER BY (Q16).
- Can I group by two columns? Yes, you get one row per unique combination (Q12).
**Common mistakes:** Selecting name along with COUNT(*) and no GROUP BY name; the database does not know which name to show.

### Q3 ⭐⭐⭐ 🟢 What is the difference between WHERE and HAVING?
**Asked at:** commonly listed in SQL prep guides for data analyst roles (LearnSQL, Indeed India, CCBP); research notes list GROUP BY/HAVING as a standard service-MNC SQL question type; WHERE vs HAVING had the highest count in the source tally (4 sources)
**What the interviewer is checking:** Do you know the order SQL works in: filter rows, group, then filter groups?
**Say this in the interview:** WHERE filters individual rows before grouping. HAVING filters whole groups after the aggregate has been calculated. So aggregates like COUNT or AVG can only be used in HAVING.
**Explain simply:**
- Order of work: FROM, then WHERE (rows), then GROUP BY, then HAVING (groups), then SELECT, then ORDER BY.
- WHERE cannot see COUNT(*) or AVG() because they do not exist yet at that stage.
- Use WHERE whenever the condition is about a single row (status = 'Active'); it is also cheaper because fewer rows get grouped.
- Use HAVING only for conditions on aggregates.
**Example:** Out of active employees only, which departments still have at least 3 people, and what is their average pay? WHERE keeps active staff; HAVING keeps departments with 3 or more.
**Sample data:**

`employees`

| emp_id | name | dept | salary | hire_date | status |
|---|---|---|---|---|---|
| 1 | Asha | HR | 40000 | 2020-03-01 | Active |
| 2 | Bala | HR | 45000 | 2021-07-15 | Active |
| 3 | Chitra | HR | 52000 | 2022-02-10 | Left |
| 4 | Deepak | HR | 38000 | 2023-01-05 | Active |
| 5 | Esha | HR | NULL | 2023-06-20 | Active |
| 6 | Farhan | HR | 60000 | 2019-11-11 | Left |
| 7 | Gita | IT | 80000 | 2018-05-01 | Active |
| 8 | Hari | IT | 65000 | 2022-03-14 | Active |
| 9 | Indu | IT | 72000 | 2023-04-01 | Left |
| 10 | Jai | IT | 55000 | 2021-09-09 | Active |
| 11 | Kiran | IT | 90000 | 2022-08-18 | Active |
| 12 | Lata | Sales | 35000 | 2022-01-02 | Active |
| 13 | Manoj | Sales | 42000 | 2023-02-02 | Left |
| 14 | Neha | Sales | 30000 | 2020-10-10 | Active |
| 15 | Omar | Finance | 70000 | 2021-12-01 | Active |
| 16 | Pooja | Finance | 66000 | 2023-05-05 | Active |

**SQL:**
```sql
SELECT dept, COUNT(*) AS active_count, AVG(salary) AS avg_salary
FROM employees
WHERE status = 'Active'          -- row filter, runs first
GROUP BY dept
HAVING COUNT(*) >= 3;            -- group filter, runs after grouping
```
**Output:**

| dept | active_count | avg_salary |
|---|---|---|
| HR | 4 | 41000 |
| IT | 4 | 72500 |

**pandas equivalent:**
```python
a = emp[emp['status'] == 'Active']
g = a.groupby('dept').agg(active_count=('emp_id', 'size'), avg_salary=('salary', 'mean')).reset_index()
res = g[g['active_count'] >= 3]
# Output:
# dept  active_count  avg_salary
#   HR             4     41000.0
#   IT             4     72500.0
```
**Edge cases:** Sales has only 2 active people, so it disappears. Putting status in HAVING would also work in some databases but is slower and unclear; keep row filters in WHERE.
**Likely follow-ups:**
- Can HAVING reference a non-aggregate column? Only if it is a GROUP BY column; better to put it in WHERE.
- Which runs first? WHERE.
**Common mistakes:** Writing WHERE COUNT(*) >= 3, which raises an error.

### Q4 ⭐⭐⭐ 🟢 Given employees(emp_id, name, dept, salary, hire_date, status), write a query to count the number of employees in each department.
**Asked at:** commonly listed in SQL prep guides for data analyst roles (LearnSQL, Indeed India, CCBP); research notes list GROUP BY/HAVING as a standard service-MNC SQL question type
**What the interviewer is checking:** Basic GROUP BY with COUNT, and whether you sort the result sensibly.
**Say this in the interview:** I group by department and count the rows in each group, then sort so the biggest department comes first.
**Explain simply:**
- COUNT(*) counts every row in the group, which is the employee count because each employee is one row.
- If emp_id could repeat, COUNT(DISTINCT emp_id) is the safer count.
- ORDER BY can use the COUNT result by its alias.
**Example:** Headcount report for the CHRO: HR 6, IT 5, Sales 3, Finance 2.
**Sample data:**

`employees`

| emp_id | name | dept | salary | hire_date | status |
|---|---|---|---|---|---|
| 1 | Asha | HR | 40000 | 2020-03-01 | Active |
| 2 | Bala | HR | 45000 | 2021-07-15 | Active |
| 3 | Chitra | HR | 52000 | 2022-02-10 | Left |
| 4 | Deepak | HR | 38000 | 2023-01-05 | Active |
| 5 | Esha | HR | NULL | 2023-06-20 | Active |
| 6 | Farhan | HR | 60000 | 2019-11-11 | Left |
| 7 | Gita | IT | 80000 | 2018-05-01 | Active |
| 8 | Hari | IT | 65000 | 2022-03-14 | Active |
| 9 | Indu | IT | 72000 | 2023-04-01 | Left |
| 10 | Jai | IT | 55000 | 2021-09-09 | Active |
| 11 | Kiran | IT | 90000 | 2022-08-18 | Active |
| 12 | Lata | Sales | 35000 | 2022-01-02 | Active |
| 13 | Manoj | Sales | 42000 | 2023-02-02 | Left |
| 14 | Neha | Sales | 30000 | 2020-10-10 | Active |
| 15 | Omar | Finance | 70000 | 2021-12-01 | Active |
| 16 | Pooja | Finance | 66000 | 2023-05-05 | Active |

**SQL:**
```sql
SELECT dept, COUNT(*) AS employee_count
FROM employees
GROUP BY dept
ORDER BY employee_count DESC, dept;
```
**Output:**

| dept | employee_count |
|---|---|
| HR | 6 |
| IT | 5 |
| Sales | 3 |
| Finance | 2 |

**pandas equivalent:**
```python
res = (emp.groupby('dept').size().reset_index(name='employee_count')
          .sort_values(['employee_count', 'dept'], ascending=[False, True]))
# Output:
#    dept  employee_count
#      HR               6
#      IT               5
#   Sales               3
# Finance               2
```
**Edge cases:** To count only current staff add WHERE status = 'Active'. Employees with NULL dept form a separate NULL group. Ties are broken by the second ORDER BY column.
**Likely follow-ups:**
- How to include departments with zero staff? LEFT JOIN from a departments table (Q31).
- How to show percent of total? Divide by a total (Q36).
**Common mistakes:** Using COUNT(dept): it skips NULL departments and silently undercounts.

### Q5 ⭐⭐⭐ 🟢 What is the difference between COUNT(*), COUNT(column) and COUNT(DISTINCT column)?
**Asked at:** commonly listed in SQL prep guides for data analyst roles (LearnSQL, Indeed India, CCBP); research notes list GROUP BY/HAVING as a standard service-MNC SQL question type
**What the interviewer is checking:** Do you know that the three COUNT forms answer different questions?
**Say this in the interview:** COUNT(*) counts all rows. COUNT(column) counts rows where that column is not NULL. COUNT(DISTINCT column) counts the different non-NULL values.
**Explain simply:**
- COUNT(*): how many rows, regardless of content.
- COUNT(column): how many rows actually have a value in that column (NULL = missing, skipped).
- COUNT(DISTINCT column): how many unique values, again ignoring NULL.
- They match only when the column has no NULLs and no repeats.
**Example:** 16 employee rows, but only 15 have a salary filled in, and they sit in 4 different departments.
**Sample data:**

`employees`

| emp_id | name | dept | salary | hire_date | status |
|---|---|---|---|---|---|
| 1 | Asha | HR | 40000 | 2020-03-01 | Active |
| 2 | Bala | HR | 45000 | 2021-07-15 | Active |
| 3 | Chitra | HR | 52000 | 2022-02-10 | Left |
| 4 | Deepak | HR | 38000 | 2023-01-05 | Active |
| 5 | Esha | HR | NULL | 2023-06-20 | Active |
| 6 | Farhan | HR | 60000 | 2019-11-11 | Left |
| 7 | Gita | IT | 80000 | 2018-05-01 | Active |
| 8 | Hari | IT | 65000 | 2022-03-14 | Active |
| 9 | Indu | IT | 72000 | 2023-04-01 | Left |
| 10 | Jai | IT | 55000 | 2021-09-09 | Active |
| 11 | Kiran | IT | 90000 | 2022-08-18 | Active |
| 12 | Lata | Sales | 35000 | 2022-01-02 | Active |
| 13 | Manoj | Sales | 42000 | 2023-02-02 | Left |
| 14 | Neha | Sales | 30000 | 2020-10-10 | Active |
| 15 | Omar | Finance | 70000 | 2021-12-01 | Active |
| 16 | Pooja | Finance | 66000 | 2023-05-05 | Active |

**SQL:**
```sql
SELECT COUNT(*)             AS all_rows,
       COUNT(salary)        AS salary_filled,
       COUNT(DISTINCT dept) AS distinct_depts
FROM employees;
```
**Output:**

| all_rows | salary_filled | distinct_depts |
|---|---|---|
| 16 | 15 | 4 |

**pandas equivalent:**
```python
res = pd.DataFrame([{'all_rows': len(emp), 'salary_filled': emp['salary'].count(),
                      'distinct_depts': emp['dept'].nunique()}])
# Output:
#  all_rows  salary_filled  distinct_depts
#        16             15               4
```
**Edge cases:** NULLs: ignored by the last two. Duplicates: only DISTINCT removes them. Empty table: all three return 0.
**Likely follow-ups:**
- Is COUNT(1) different from COUNT(*)? No, same result (Q42).
- How to count distinct including NULL as a value? Rare; use CASE or add 1 if any NULL exists.
**Common mistakes:** Using COUNT(email) to count people and missing the ones with a blank email.

### Q6 ⭐⭐⭐ 🟢 Given employees(emp_id, name, dept, salary, hire_date, status), show the total, average, highest and lowest salary for each department in one query.
**Asked at:** commonly listed in SQL prep guides for data analyst roles (LearnSQL, Indeed India, CCBP); research notes list GROUP BY/HAVING as a standard service-MNC SQL question type
**What the interviewer is checking:** Can you put several aggregates in one SELECT per group?
**Say this in the interview:** I group by department and put SUM, AVG, MAX and MIN in the same SELECT, so one pass gives the four numbers per department.
**Explain simply:**
- Any number of aggregates can sit in the same SELECT; each is calculated inside every group.
- Round AVG so the report is readable.
- NULL salaries are skipped by all four.
**Example:** Payroll summary for each department for the monthly review.
**Sample data:**

`employees`

| emp_id | name | dept | salary | hire_date | status |
|---|---|---|---|---|---|
| 1 | Asha | HR | 40000 | 2020-03-01 | Active |
| 2 | Bala | HR | 45000 | 2021-07-15 | Active |
| 3 | Chitra | HR | 52000 | 2022-02-10 | Left |
| 4 | Deepak | HR | 38000 | 2023-01-05 | Active |
| 5 | Esha | HR | NULL | 2023-06-20 | Active |
| 6 | Farhan | HR | 60000 | 2019-11-11 | Left |
| 7 | Gita | IT | 80000 | 2018-05-01 | Active |
| 8 | Hari | IT | 65000 | 2022-03-14 | Active |
| 9 | Indu | IT | 72000 | 2023-04-01 | Left |
| 10 | Jai | IT | 55000 | 2021-09-09 | Active |
| 11 | Kiran | IT | 90000 | 2022-08-18 | Active |
| 12 | Lata | Sales | 35000 | 2022-01-02 | Active |
| 13 | Manoj | Sales | 42000 | 2023-02-02 | Left |
| 14 | Neha | Sales | 30000 | 2020-10-10 | Active |
| 15 | Omar | Finance | 70000 | 2021-12-01 | Active |
| 16 | Pooja | Finance | 66000 | 2023-05-05 | Active |

**SQL:**
```sql
SELECT dept,
       SUM(salary)           AS total_salary,
       ROUND(AVG(salary), 0) AS avg_salary,
       MAX(salary)           AS highest,
       MIN(salary)           AS lowest
FROM employees
GROUP BY dept
ORDER BY dept;
```
**Output:**

| dept | total_salary | avg_salary | highest | lowest |
|---|---|---|---|---|
| Finance | 136000 | 68000 | 70000 | 66000 |
| HR | 235000 | 47000 | 60000 | 38000 |
| IT | 362000 | 72400 | 90000 | 55000 |
| Sales | 107000 | 35667 | 42000 | 30000 |

**pandas equivalent:**
```python
g = emp.groupby('dept')['salary']
res = pd.DataFrame({'total_salary': g.sum(), 'avg_salary': g.mean().round(0),
                    'highest': g.max(), 'lowest': g.min()}).reset_index()
# Output:
#    dept  total_salary  avg_salary  highest  lowest
# Finance      136000.0     68000.0  70000.0 66000.0
#      HR      235000.0     47000.0  60000.0 38000.0
#      IT      362000.0     72400.0  90000.0 55000.0
#   Sales      107000.0     35667.0  42000.0 30000.0
```
**Edge cases:** HR average is over 5 salaried people (Esha's NULL is ignored): 235000 / 5 = 47000. A department where every salary is NULL gives NULL for AVG/SUM/MIN/MAX. ROUND syntax is the same in all major databases.
**Likely follow-ups:**
- How to also get the headcount? Add COUNT(*).
- How to get the name of the highest earner? That needs a window function or join (a later part).
**Common mistakes:** Writing AVG(salary) in WHERE or forgetting GROUP BY dept.

### Q7 ⭐⭐⭐ 🟢 How do you find duplicate records in a table, for example the same email appearing more than once, using GROUP BY and HAVING?
**Asked at:** commonly listed in SQL prep guides for data analyst roles (LearnSQL, Indeed India, CCBP); research notes list GROUP BY/HAVING as a standard service-MNC SQL question type; duplicate-finding also appeared in the guides sampled
**What the interviewer is checking:** Can you use GROUP BY with HAVING COUNT(*) > 1 to find repeats?
**Say this in the interview:** I group by the column that should be unique, here email, and keep only groups with more than one row using HAVING COUNT(*) > 1.
**Explain simply:**
- A duplicate means the same value appears in more than one row.
- Group by the column, count each group, and keep groups where the count is above 1.
- To see the full duplicate rows, join this result back to the table or use a window function later.
- NULL emails group together as one group, so exclude them with WHERE email IS NOT NULL if missing is not a duplicate.
**Example:** Two HR records for 'asha@co.com' mean the same person was onboarded twice and gets two payslips. Here asha@co.com appears 3 times and bala@co.com twice.
**Sample data:**

`staff`

| emp_id | name | email |
|---|---|---|
| 1 | Asha | asha@co.com |
| 2 | Bala | bala@co.com |
| 3 | Asha K | asha@co.com |
| 4 | Chitra | chitra@co.com |
| 5 | Dev | NULL |
| 6 | Esha | NULL |
| 7 | Bala R | bala@co.com |
| 8 | Asha M | asha@co.com |

**SQL:**
```sql
SELECT email, COUNT(*) AS times_seen
FROM staff
WHERE email IS NOT NULL
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY times_seen DESC;
```
**Output:**

| email | times_seen |
|---|---|
| asha@co.com | 3 |
| bala@co.com | 2 |

**pandas equivalent:**
```python
s = staff.dropna(subset=['email'])
c = s.groupby('email').size().reset_index(name='times_seen')
res = c[c['times_seen'] > 1].sort_values('times_seen', ascending=False)
# Output:
#       email  times_seen
# asha@co.com           3
# bala@co.com           2
```
**Edge cases:** Two NULL emails exist; without the IS NOT NULL filter they would show as a duplicate group of 2. Different case or trailing spaces ('Asha@Co.com') escape the check; use LOWER(TRIM(email)) first.
**Likely follow-ups:**
- How to delete the extra rows but keep one? Use ROW_NUMBER() or keep MIN(emp_id) per email (later parts).
- How to list the IDs together? STRING_AGG or GROUP_CONCAT (Q28).
**Common mistakes:** Using WHERE COUNT(*) > 1, or grouping by several columns and then wondering why no duplicates show.

### Q8 ⭐⭐⭐ 🟢 Given employees(emp_id, name, dept, salary, hire_date, status), list the departments that have more than 5 employees.
**Asked at:** commonly listed in SQL prep guides for data analyst roles (LearnSQL, Indeed India, CCBP); research notes list GROUP BY/HAVING as a standard service-MNC SQL question type
**What the interviewer is checking:** Simple HAVING on a COUNT.
**Say this in the interview:** I group by department and use HAVING COUNT(*) > 5, because the count only exists after grouping.
**Explain simply:**
- HAVING filters groups; COUNT(*) is the group size.
- More than 5 means 6 or more; exactly 5 is excluded.
- Only HR (6 people) qualifies in the sample.
**Example:** Which departments are big enough to need their own HRBP (HR business partner)? Rule: more than 5 staff.
**Sample data:**

`employees`

| emp_id | name | dept | salary | hire_date | status |
|---|---|---|---|---|---|
| 1 | Asha | HR | 40000 | 2020-03-01 | Active |
| 2 | Bala | HR | 45000 | 2021-07-15 | Active |
| 3 | Chitra | HR | 52000 | 2022-02-10 | Left |
| 4 | Deepak | HR | 38000 | 2023-01-05 | Active |
| 5 | Esha | HR | NULL | 2023-06-20 | Active |
| 6 | Farhan | HR | 60000 | 2019-11-11 | Left |
| 7 | Gita | IT | 80000 | 2018-05-01 | Active |
| 8 | Hari | IT | 65000 | 2022-03-14 | Active |
| 9 | Indu | IT | 72000 | 2023-04-01 | Left |
| 10 | Jai | IT | 55000 | 2021-09-09 | Active |
| 11 | Kiran | IT | 90000 | 2022-08-18 | Active |
| 12 | Lata | Sales | 35000 | 2022-01-02 | Active |
| 13 | Manoj | Sales | 42000 | 2023-02-02 | Left |
| 14 | Neha | Sales | 30000 | 2020-10-10 | Active |
| 15 | Omar | Finance | 70000 | 2021-12-01 | Active |
| 16 | Pooja | Finance | 66000 | 2023-05-05 | Active |

**SQL:**
```sql
SELECT dept, COUNT(*) AS employee_count
FROM employees
GROUP BY dept
HAVING COUNT(*) > 5;
```
**Output:**

| dept | employee_count |
|---|---|
| HR | 6 |

**pandas equivalent:**
```python
c = emp.groupby('dept').size().reset_index(name='employee_count')
res = c[c['employee_count'] > 5]
# Output:
# dept  employee_count
#   HR               6
```
**Edge cases:** IT has exactly 5, so it is excluded by > 5 but included by >= 5; read the wording carefully. If no department qualifies the result is an empty table, not an error.
**Likely follow-ups:**
- How to add a status filter? WHERE status = 'Active' before GROUP BY.
- Can I use the alias in HAVING? MySQL and SQLite yes, PostgreSQL and SQL Server no (Q15).
**Common mistakes:** Writing WHERE COUNT(*) > 5.

### Q9 ⭐⭐⭐ 🟢 How do aggregate functions and GROUP BY treat NULL values?
**Asked at:** commonly listed in SQL prep guides for data analyst roles (LearnSQL, Indeed India, CCBP); research notes list GROUP BY/HAVING as a standard service-MNC SQL question type
**What the interviewer is checking:** Do you know NULLs are skipped by aggregates but form their own group in GROUP BY?
**Say this in the interview:** Aggregates like SUM, AVG, MIN, MAX and COUNT(column) ignore NULLs. COUNT(*) counts the row anyway. GROUP BY puts all NULLs of the grouping column into one single group.
**Explain simply:**
- NULL means 'unknown or not recorded', not zero.
- SUM of only NULLs is NULL, not 0; COUNT(column) of only NULLs is 0.
- In GROUP BY, two NULLs are treated as the same group even though NULL = NULL is not true in WHERE.
- AVG ignores NULL rows, so it is the average of the known values only.
**Example:** Some contractors have no department assigned and some staff have no salary entered yet; the report must handle both.
**Sample data:**

`t`

| dept | salary |
|---|---|
| HR | 100 |
| HR | NULL |
| NULL | 50 |
| NULL | 70 |
| IT | NULL |

**SQL:**
```sql
SELECT dept,
       COUNT(*)      AS rows_in_group,
       COUNT(salary) AS salary_known,
       SUM(salary)   AS total,
       AVG(salary)   AS average
FROM t
GROUP BY dept
ORDER BY dept;
```
**Output:**

| dept | rows_in_group | salary_known | total | average |
|---|---|---|---|---|
| NULL | 2 | 2 | 120 | 60 |
| HR | 2 | 1 | 100 | 100 |
| IT | 1 | 0 | NULL | NULL |

**pandas equivalent:**
```python
g = t.groupby('dept', dropna=False)
res = g.agg(rows_in_group=('salary', 'size'), salary_known=('salary', 'count'),
            total=('salary', lambda s: s.sum(min_count=1)), average=('salary', 'mean')).reset_index()
res = res.sort_values('dept', na_position='first')
# Output:
# dept  rows_in_group  salary_known  total  average
#  NaN              2             2  120.0     60.0
#   HR              2             1  100.0    100.0
#   IT              1             0    NaN      NaN
```
**Edge cases:** In pandas groupby drops NULL keys by default; pass dropna=False to match SQL. IT has only a NULL salary so SUM and AVG are NULL. ORDER BY places NULL first in SQLite and MySQL but last in PostgreSQL (use NULLS LAST/FIRST there).
**Likely follow-ups:**
- How to show 0 instead of NULL for the sum? COALESCE(SUM(salary), 0) (Q21).
- How to treat missing dept as 'Unassigned'? COALESCE(dept, 'Unassigned') in SELECT and GROUP BY.
**Common mistakes:** Assuming NULL salary counts as 0 in the average, or that NULL-dept rows vanish from the report.

### Q10 ⭐⭐⭐ 🟡 Why does SQL give the error 'column must appear in the GROUP BY clause or be used in an aggregate function'? How do you fix it?
**Asked at:** commonly listed in SQL prep guides for data analyst roles (LearnSQL, Indeed India, CCBP); research notes list GROUP BY/HAVING as a standard service-MNC SQL question type
**What the interviewer is checking:** Do you understand that every selected column must be one value per group?
**Say this in the interview:** After grouping, each group becomes one output row. A plain column like name has many different values inside a group, so SQL does not know which to show. Either add it to GROUP BY or wrap it in an aggregate.
**Explain simply:**
- The rule: every column in SELECT is either in GROUP BY or inside an aggregate function.
- Fix 1: add the column to GROUP BY (the groups become finer).
- Fix 2: wrap it in MIN, MAX, COUNT or STRING_AGG so it returns one value.
- Fix 3: remove the column from SELECT if you do not really need it.
**Example:** 'Show department, employee name and headcount' is ambiguous: HR has 6 names but one headcount. You must choose: one row per person, or one row per department with the names joined together.
**Sample data:**

`employees`

| emp_id | name | dept | salary | hire_date | status |
|---|---|---|---|---|---|
| 1 | Asha | HR | 40000 | 2020-03-01 | Active |
| 2 | Bala | HR | 45000 | 2021-07-15 | Active |
| 3 | Chitra | HR | 52000 | 2022-02-10 | Left |
| 4 | Deepak | HR | 38000 | 2023-01-05 | Active |
| 5 | Esha | HR | NULL | 2023-06-20 | Active |
| 6 | Farhan | HR | 60000 | 2019-11-11 | Left |
| 7 | Gita | IT | 80000 | 2018-05-01 | Active |
| 8 | Hari | IT | 65000 | 2022-03-14 | Active |
| 9 | Indu | IT | 72000 | 2023-04-01 | Left |
| 10 | Jai | IT | 55000 | 2021-09-09 | Active |
| 11 | Kiran | IT | 90000 | 2022-08-18 | Active |
| 12 | Lata | Sales | 35000 | 2022-01-02 | Active |
| 13 | Manoj | Sales | 42000 | 2023-02-02 | Left |
| 14 | Neha | Sales | 30000 | 2020-10-10 | Active |
| 15 | Omar | Finance | 70000 | 2021-12-01 | Active |
| 16 | Pooja | Finance | 66000 | 2023-05-05 | Active |

**SQL:**
```sql
-- Fix 1: finer groups
SELECT dept, status, COUNT(*) AS employee_count
FROM employees
GROUP BY dept, status
ORDER BY dept, status;

-- Fix 2: wrap in an aggregate
SELECT dept, MIN(hire_date) AS earliest_hire, COUNT(*) AS employee_count
FROM employees
GROUP BY dept
ORDER BY dept;
```
**Output (Fix 1: finer groups):**

| dept | status | employee_count |
|---|---|---|
| Finance | Active | 2 |
| HR | Active | 4 |
| HR | Left | 2 |
| IT | Active | 4 |
| IT | Left | 1 |
| Sales | Active | 2 |
| Sales | Left | 1 |

**Output (Fix 2: wrap in an aggregate):**

| dept | earliest_hire | employee_count |
|---|---|---|
| Finance | 2021-12-01 | 2 |
| HR | 2019-11-11 | 6 |
| IT | 2018-05-01 | 5 |
| Sales | 2020-10-10 | 3 |

**Edge cases:** The faulty query is `SELECT dept, name, COUNT(*) FROM employees GROUP BY dept;`. PostgreSQL, SQL Server, Oracle, DuckDB reject it. DuckDB says (run here): `Binder Error: column "name" must appear in the GROUP BY clause or must be part of an aggregate function.`. MySQL with ONLY_FULL_GROUP_BY (default since 5.7) also rejects it; older MySQL and SQLite accept it and return an arbitrary name, which is dangerous (Q50).
**Likely follow-ups:**
- What if I want each dept's top earner's name? Use a window function or a join to a grouped subquery (later parts).
- Is SQLite's silence safe? No; the shown name is arbitrary.
**Common mistakes:** Adding every column to GROUP BY just to silence the error, which turns the report into row-level detail.

### Q11 ⭐⭐⭐ 🟡 Given employees(emp_id, name, dept, salary, hire_date, status), list departments whose average salary is above 50,000, considering only employees hired after 1 Jan 2022. Where do WHERE and HAVING each go?
**Asked at:** commonly listed in SQL prep guides for data analyst roles (LearnSQL, Indeed India, CCBP); research notes list GROUP BY/HAVING as a standard service-MNC SQL question type
**What the interviewer is checking:** Can you combine a row filter (WHERE) and a group filter (HAVING) correctly?
**Say this in the interview:** The hire-date condition is about a single employee, so it goes in WHERE before grouping. The average-salary condition is about the group, so it goes in HAVING.
**Explain simply:**
- WHERE hire_date > '2022-01-01' removes older employees before any averaging.
- HAVING AVG(salary) > 50000 then keeps departments whose average of the remaining people is high enough.
- Swapping them changes the answer, because HAVING cannot filter dates of individuals.
**Example:** Compensation review for recent joiners: do new hires in IT and Finance earn above 50,000 on average?
**Sample data:**

`employees`

| emp_id | name | dept | salary | hire_date | status |
|---|---|---|---|---|---|
| 1 | Asha | HR | 40000 | 2020-03-01 | Active |
| 2 | Bala | HR | 45000 | 2021-07-15 | Active |
| 3 | Chitra | HR | 52000 | 2022-02-10 | Left |
| 4 | Deepak | HR | 38000 | 2023-01-05 | Active |
| 5 | Esha | HR | NULL | 2023-06-20 | Active |
| 6 | Farhan | HR | 60000 | 2019-11-11 | Left |
| 7 | Gita | IT | 80000 | 2018-05-01 | Active |
| 8 | Hari | IT | 65000 | 2022-03-14 | Active |
| 9 | Indu | IT | 72000 | 2023-04-01 | Left |
| 10 | Jai | IT | 55000 | 2021-09-09 | Active |
| 11 | Kiran | IT | 90000 | 2022-08-18 | Active |
| 12 | Lata | Sales | 35000 | 2022-01-02 | Active |
| 13 | Manoj | Sales | 42000 | 2023-02-02 | Left |
| 14 | Neha | Sales | 30000 | 2020-10-10 | Active |
| 15 | Omar | Finance | 70000 | 2021-12-01 | Active |
| 16 | Pooja | Finance | 66000 | 2023-05-05 | Active |

**SQL:**
```sql
SELECT dept, ROUND(AVG(salary), 0) AS avg_salary, COUNT(*) AS recent_hires
FROM employees
WHERE hire_date > '2022-01-01'
GROUP BY dept
HAVING AVG(salary) > 50000
ORDER BY dept;
```
**Output:**

| dept | avg_salary | recent_hires |
|---|---|---|
| Finance | 66000 | 1 |
| IT | 75667 | 3 |

**pandas equivalent:**
```python
r = emp[emp['hire_date'] > '2022-01-01']
g = r.groupby('dept').agg(avg_salary=('salary', 'mean'), recent_hires=('emp_id', 'size')).reset_index()
g['avg_salary'] = g['avg_salary'].round(0)
res = g[g['avg_salary'] > 50000].sort_values('dept')
# Output:
#    dept  avg_salary  recent_hires
# Finance     66000.0             1
#      IT     75667.0             3
```
**Edge cases:** 'After 1 Jan 2022' means > not >=, so someone hired exactly on 2022-01-01 is excluded. HR: Chitra 52000, Deepak 38000, Esha NULL, average of 2 known values = 45000, so HR fails. Date literal format: use 'YYYY-MM-DD' everywhere; SQL Server also accepts it.
**Likely follow-ups:**
- What if I used WHERE for the average? Error: aggregate not allowed in WHERE.
- Does the HR group's NULL salary affect the average? It is skipped.
**Common mistakes:** Putting the date check in HAVING (error or wrong), or filtering on the group average in WHERE.

### Q12 ⭐⭐⭐ 🟡 Given orders(order_id, customer_id, category, amount, order_date), find the total sales for each category in each month (grouping by more than one column).
**Asked at:** commonly listed in SQL prep guides for data analyst roles (LearnSQL, Indeed India, CCBP); research notes list GROUP BY/HAVING as a standard service-MNC SQL question type (a multi-column GROUP BY also appears in a real product-company question set on StrataScratch)
**What the interviewer is checking:** Can you group by two things at once and extract the month from a date?
**Say this in the interview:** I list both the category and the month in GROUP BY, so SQL makes one group per category-month combination and sums the amount in each.
**Explain simply:**
- Each unique pair (category, month) is a group.
- I build the month with a date function. Using year-month (2025-01) keeps January 2025 apart from January 2026.
- Dialect: SQLite strftime('%Y-%m', d); PostgreSQL TO_CHAR(d,'YYYY-MM') or DATE_TRUNC; MySQL DATE_FORMAT(d,'%Y-%m'); SQL Server FORMAT(d,'yyyy-MM') (not run here).
**Example:** Retail sales by category by month for a quarterly review: Electronics 7500 in Jan 2025, 12000 in Feb, and so on.
**Sample data:**

`orders`

| order_id | customer_id | category | amount | order_date |
|---|---|---|---|---|
| 1 | C1 | Electronics | 4000 | 2025-01-05 |
| 2 | C1 | Electronics | 3500 | 2025-01-20 |
| 3 | C1 | Clothing | 2000 | 2025-02-03 |
| 4 | C1 | Grocery | 1500 | 2025-02-14 |
| 5 | C1 | Grocery | 800 | 2025-03-02 |
| 6 | C2 | Clothing | 1200 | 2025-01-15 |
| 7 | C2 | Clothing | 900 | 2025-01-28 |
| 8 | C2 | Electronics | 6000 | 2025-03-09 |
| 9 | C3 | Grocery | 450 | 2025-02-01 |
| 10 | C3 | Grocery | 300 | 2025-02-01 |
| 11 | C3 | Clothing | 700 | 2025-03-15 |
| 12 | C4 | Electronics | 12000 | 2025-02-20 |
| 13 | C4 | Electronics | 5000 | 2026-01-10 |

**SQL:**
```sql
SELECT category,
       strftime('%Y-%m', order_date) AS month,
       SUM(amount) AS total_sales
FROM orders
GROUP BY category, strftime('%Y-%m', order_date)
ORDER BY category, month;
```
**Output:**

| category | month | total_sales |
|---|---|---|
| Clothing | 2025-01 | 2100 |
| Clothing | 2025-02 | 2000 |
| Clothing | 2025-03 | 700 |
| Electronics | 2025-01 | 7500 |
| Electronics | 2025-02 | 12000 |
| Electronics | 2025-03 | 6000 |
| Electronics | 2026-01 | 5000 |
| Grocery | 2025-02 | 2250 |
| Grocery | 2025-03 | 800 |

**pandas equivalent:**
```python
o = orders.assign(month=pd.to_datetime(orders['order_date']).dt.strftime('%Y-%m'))
res = (o.groupby(['category', 'month'])['amount'].sum().reset_index(name='total_sales')
         .sort_values(['category', 'month']))
# Output:
#    category   month  total_sales
#    Clothing 2025-01         2100
#    Clothing 2025-02         2000
#    Clothing 2025-03          700
# Electronics 2025-01         7500
# Electronics 2025-02        12000
# Electronics 2025-03         6000
# Electronics 2026-01         5000
#     Grocery 2025-02         2250
#     Grocery 2025-03          800
```
**Edge cases:** Months with no orders for a category do not appear (no zero rows). A NULL amount is skipped by SUM; a NULL date forms a NULL month group.
**Likely follow-ups:**
- How to make the months columns? Conditional aggregation (Q27).
- Why not group by the month number only? Jan 2025 and Jan 2026 would merge.
**Common mistakes:** Grouping by MONTH(order_date) only and merging different years.

### Q13 ⭐⭐⭐ 🟡 Given orders(order_id, customer_id, category, amount, order_date), find customers who placed more than 3 orders and spent more than 10,000 in total.
**Asked at:** commonly listed in SQL prep guides for data analyst roles (LearnSQL, Indeed India, CCBP); research notes list GROUP BY/HAVING as a standard service-MNC SQL question type (HAVING on two aggregate conditions)
**What the interviewer is checking:** Can you put two aggregate conditions in one HAVING?
**Say this in the interview:** I group orders by customer, then HAVING COUNT(*) > 3 AND SUM(amount) > 10000 keeps customers who meet both conditions.
**Explain simply:**
- Each customer is a group; COUNT(*) is number of orders and SUM(amount) is total spend.
- Join conditions with AND for both, OR for either.
- Both are aggregates, so both belong in HAVING.
**Example:** Loyalty programme: customers with over 3 orders and above 10,000 spend. C1 has 5 orders worth 11800, so C1 qualifies; C4 spent 17000 but only in 2 orders.
**Sample data:**

`orders`

| order_id | customer_id | category | amount | order_date |
|---|---|---|---|---|
| 1 | C1 | Electronics | 4000 | 2025-01-05 |
| 2 | C1 | Electronics | 3500 | 2025-01-20 |
| 3 | C1 | Clothing | 2000 | 2025-02-03 |
| 4 | C1 | Grocery | 1500 | 2025-02-14 |
| 5 | C1 | Grocery | 800 | 2025-03-02 |
| 6 | C2 | Clothing | 1200 | 2025-01-15 |
| 7 | C2 | Clothing | 900 | 2025-01-28 |
| 8 | C2 | Electronics | 6000 | 2025-03-09 |
| 9 | C3 | Grocery | 450 | 2025-02-01 |
| 10 | C3 | Grocery | 300 | 2025-02-01 |
| 11 | C3 | Clothing | 700 | 2025-03-15 |
| 12 | C4 | Electronics | 12000 | 2025-02-20 |
| 13 | C4 | Electronics | 5000 | 2026-01-10 |

**SQL:**
```sql
SELECT customer_id, COUNT(*) AS orders_placed, SUM(amount) AS total_spent
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 3 AND SUM(amount) > 10000;
```
**Output:**

| customer_id | orders_placed | total_spent |
|---|---|---|
| C1 | 5 | 11800 |

**pandas equivalent:**
```python
g = orders.groupby('customer_id')['amount'].agg(orders_placed='size', total_spent='sum').reset_index()
res = g[(g['orders_placed'] > 3) & (g['total_spent'] > 10000)]
# Output:
# customer_id  orders_placed  total_spent
#          C1              5        11800
```
**Edge cases:** More than 3 means 4 or more orders. Duplicate order rows (same order_id twice) would inflate both numbers; use COUNT(DISTINCT order_id) if that is possible. No match gives an empty result.
**Likely follow-ups:**
- How to use OR? HAVING COUNT(*) > 3 OR SUM(amount) > 10000 returns C1 and C4.
- Where does a date filter go? WHERE.
**Common mistakes:** Using WHERE for COUNT or SUM, or writing the two conditions as a comma.

### Q14 ⭐⭐⭐ 🟡 Can you use an aggregate function such as AVG() inside a WHERE clause? Why not, and what do you do instead (e.g., find employees earning more than the company average)?
**Asked at:** commonly listed in SQL prep guides for data analyst roles (LearnSQL, Indeed India, CCBP); research notes list GROUP BY/HAVING as a standard service-MNC SQL question type
**What the interviewer is checking:** Do you know WHERE runs before aggregates exist and can you use a subquery instead?
**Say this in the interview:** No. WHERE filters rows before any aggregate is calculated, so AVG() cannot be used there. I calculate the average in a subquery and compare each salary to that single number.
**Explain simply:**
- Error in SQLite: 'misuse of aggregate'; PostgreSQL: 'aggregate functions are not allowed in WHERE'.
- A scalar subquery (a query that returns exactly one value) can sit inside WHERE.
- Subquery runs once for the whole table, and the outer query compares each employee to it.
- Window functions (AVG() OVER ()) also work; later part.
**Example:** Which employees earn more than the company average? Average of the 15 known salaries is 56,000, so Farhan, Gita, Hari, Indu, Kiran, Omar and Pooja are above it.
**Sample data:**

`employees`

| emp_id | name | dept | salary | hire_date | status |
|---|---|---|---|---|---|
| 1 | Asha | HR | 40000 | 2020-03-01 | Active |
| 2 | Bala | HR | 45000 | 2021-07-15 | Active |
| 3 | Chitra | HR | 52000 | 2022-02-10 | Left |
| 4 | Deepak | HR | 38000 | 2023-01-05 | Active |
| 5 | Esha | HR | NULL | 2023-06-20 | Active |
| 6 | Farhan | HR | 60000 | 2019-11-11 | Left |
| 7 | Gita | IT | 80000 | 2018-05-01 | Active |
| 8 | Hari | IT | 65000 | 2022-03-14 | Active |
| 9 | Indu | IT | 72000 | 2023-04-01 | Left |
| 10 | Jai | IT | 55000 | 2021-09-09 | Active |
| 11 | Kiran | IT | 90000 | 2022-08-18 | Active |
| 12 | Lata | Sales | 35000 | 2022-01-02 | Active |
| 13 | Manoj | Sales | 42000 | 2023-02-02 | Left |
| 14 | Neha | Sales | 30000 | 2020-10-10 | Active |
| 15 | Omar | Finance | 70000 | 2021-12-01 | Active |
| 16 | Pooja | Finance | 66000 | 2023-05-05 | Active |

**SQL:**
```sql
-- Wrong: aggregate in WHERE
SELECT name, salary FROM employees WHERE salary > AVG(salary);

-- Right: subquery
SELECT name, dept, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)
ORDER BY salary DESC;
```
**Output (Wrong: aggregate in WHERE):** SQLite error `ERROR: misuse of aggregate function AVG()`

**Output (Right: subquery):**

| name | dept | salary |
|---|---|---|
| Kiran | IT | 90000 |
| Gita | IT | 80000 |
| Indu | IT | 72000 |
| Omar | Finance | 70000 |
| Pooja | Finance | 66000 |
| Hari | IT | 65000 |
| Farhan | HR | 60000 |

**pandas equivalent:**
```python
avg = emp['salary'].mean()
res = emp[emp['salary'] > avg].sort_values('salary', ascending=False)[['name', 'dept', 'salary']]
# Output:
#   name    dept  salary
#  Kiran      IT 90000.0
#   Gita      IT 80000.0
#   Indu      IT 72000.0
#   Omar Finance 70000.0
#  Pooja Finance 66000.0
#   Hari      IT 65000.0
# Farhan      HR 60000.0
```
**Edge cases:** NULL salary: comparison with NULL is unknown, so Esha is not returned. The subquery AVG ignores NULL. If the subquery returned more than one row the comparison would fail.
**Likely follow-ups:**
- Can I use an aggregate in HAVING? Yes, that is what HAVING is for.
- How to compare with the department average? Correlated subquery or window function (later parts).
**Common mistakes:** Trying a workaround like HAVING without GROUP BY or computing the average by hand.

### Q15 ⭐⭐ 🟢 Can you use a column alias (e.g., total_sales) in GROUP BY, HAVING or ORDER BY? What differs between databases?
**Asked at:** commonly listed in SQL prep guides for data analyst roles (LearnSQL, Indeed India, CCBP); research notes list GROUP BY/HAVING as a standard service-MNC SQL question type
**What the interviewer is checking:** Do you know the logical order SQL runs in and that databases differ on alias use?
**Say this in the interview:** ORDER BY can use aliases everywhere because it runs last. GROUP BY and HAVING depend on the database: MySQL and SQLite allow aliases, PostgreSQL allows it in GROUP BY but not HAVING, SQL Server allows neither, so repeating the expression is the portable choice.
**Explain simply:**
- The alias is created in SELECT, which logically runs after WHERE, GROUP BY and HAVING.
- ORDER BY runs after SELECT, so aliases always work there.
- Vendor extras: MySQL allows alias in GROUP BY and HAVING; PostgreSQL only in GROUP BY and ORDER BY; SQL Server and Oracle (older versions) only in ORDER BY (not run here).
- Portable habit: repeat the expression in GROUP BY and HAVING; alias only in ORDER BY.
**Example:** SUM(amount) AS total_sales is handy to sort a report, but HAVING total_sales > 10000 may break when the script moves from MySQL to SQL Server.
**Sample data:**

`orders`

| order_id | customer_id | category | amount | order_date |
|---|---|---|---|---|
| 1 | C1 | Electronics | 4000 | 2025-01-05 |
| 2 | C1 | Electronics | 3500 | 2025-01-20 |
| 3 | C1 | Clothing | 2000 | 2025-02-03 |
| 4 | C1 | Grocery | 1500 | 2025-02-14 |
| 5 | C1 | Grocery | 800 | 2025-03-02 |
| 6 | C2 | Clothing | 1200 | 2025-01-15 |
| 7 | C2 | Clothing | 900 | 2025-01-28 |
| 8 | C2 | Electronics | 6000 | 2025-03-09 |
| 9 | C3 | Grocery | 450 | 2025-02-01 |
| 10 | C3 | Grocery | 300 | 2025-02-01 |
| 11 | C3 | Clothing | 700 | 2025-03-15 |
| 12 | C4 | Electronics | 12000 | 2025-02-20 |
| 13 | C4 | Electronics | 5000 | 2026-01-10 |

**SQL:**
```sql
-- Portable form
SELECT category, SUM(amount) AS total_sales
FROM orders
GROUP BY category
HAVING SUM(amount) > 10000
ORDER BY total_sales DESC;

-- Alias in HAVING (SQLite, MySQL only)
SELECT category, SUM(amount) AS total_sales
FROM orders
GROUP BY category
HAVING total_sales > 10000
ORDER BY total_sales DESC;
```
**Output (Portable form):**

| category | total_sales |
|---|---|
| Electronics | 30500 |

**Output (Alias in HAVING (SQLite, MySQL only)):**

| category | total_sales |
|---|---|
| Electronics | 30500 |

**Edge cases:** Both queries returned the same rows here because SQLite accepts the alias in HAVING. PostgreSQL would raise 'column total_sales does not exist' for the second; I did not run PostgreSQL or SQL Server here. An alias can clash with a real column of the same name; the column usually wins in WHERE/GROUP BY.
**Likely follow-ups:**
- Can I use alias in WHERE? No in any major database, since WHERE runs before SELECT.
- What about GROUP BY 1? Position numbers work (Q41).
**Common mistakes:** Assuming that if it works in MySQL it works everywhere.

### Q16 ⭐⭐ 🟢 Does GROUP BY sort the result? How do you list groups from highest to lowest total?
**Asked at:** commonly listed in SQL prep guides for data analyst roles (LearnSQL, Indeed India, CCBP); research notes list GROUP BY/HAVING as a standard service-MNC SQL question type
**What the interviewer is checking:** Do you know GROUP BY order is not guaranteed and ORDER BY is how you sort?
**Say this in the interview:** No. GROUP BY only groups; the order of output rows is not guaranteed. To list groups from highest to lowest total I add ORDER BY SUM(...) DESC, with a tie-breaker so the order is stable.
**Explain simply:**
- Some engines sort as a side effect of grouping (SQLite did here), others do not (PostgreSQL hash grouping, MySQL 8 no longer sorts); never rely on it.
- ORDER BY is the only way to guarantee order.
- ORDER BY can use the alias or the aggregate itself.
**Example:** A payroll bill report: Finance 136000, IT 362000, HR 235000, Sales 107000; sort to show IT first.
**Sample data:**

`employees`

| emp_id | name | dept | salary | hire_date | status |
|---|---|---|---|---|---|
| 1 | Asha | HR | 40000 | 2020-03-01 | Active |
| 2 | Bala | HR | 45000 | 2021-07-15 | Active |
| 3 | Chitra | HR | 52000 | 2022-02-10 | Left |
| 4 | Deepak | HR | 38000 | 2023-01-05 | Active |
| 5 | Esha | HR | NULL | 2023-06-20 | Active |
| 6 | Farhan | HR | 60000 | 2019-11-11 | Left |
| 7 | Gita | IT | 80000 | 2018-05-01 | Active |
| 8 | Hari | IT | 65000 | 2022-03-14 | Active |
| 9 | Indu | IT | 72000 | 2023-04-01 | Left |
| 10 | Jai | IT | 55000 | 2021-09-09 | Active |
| 11 | Kiran | IT | 90000 | 2022-08-18 | Active |
| 12 | Lata | Sales | 35000 | 2022-01-02 | Active |
| 13 | Manoj | Sales | 42000 | 2023-02-02 | Left |
| 14 | Neha | Sales | 30000 | 2020-10-10 | Active |
| 15 | Omar | Finance | 70000 | 2021-12-01 | Active |
| 16 | Pooja | Finance | 66000 | 2023-05-05 | Active |

**SQL:**
```sql
SELECT dept, SUM(salary) AS total_salary
FROM employees
GROUP BY dept
ORDER BY total_salary DESC, dept;
```
**Output:**

| dept | total_salary |
|---|---|
| IT | 362000 |
| HR | 235000 |
| Finance | 136000 |
| Sales | 107000 |

**pandas equivalent:**
```python
res = (emp.groupby('dept')['salary'].sum().reset_index(name='total_salary')
          .sort_values(['total_salary', 'dept'], ascending=[False, True]))
# Output:
#    dept  total_salary
#      IT      362000.0
#      HR      235000.0
# Finance      136000.0
#   Sales      107000.0
```
**Edge cases:** Ties: two departments with the same total are ordered by the second key. NULLs in the sort column come first or last depending on the database.
**Likely follow-ups:**
- How to list only the top 3? Add LIMIT 3 (Q17).
- How to sort ascending? Default; ASC.
**Common mistakes:** Trusting the order that came out in testing.

### Q17 ⭐⭐ 🟢 Given employees(emp_id, name, dept, salary, hire_date, status), find the top 3 departments by number of employees.
**Asked at:** commonly listed in SQL prep guides for data analyst roles (LearnSQL, Indeed India, CCBP); research notes list GROUP BY/HAVING as a standard service-MNC SQL question type
**What the interviewer is checking:** Can you combine GROUP BY, ORDER BY and LIMIT, and mention ties?
**Say this in the interview:** I count employees per department, sort by that count descending, and take the first three rows. For ties I would use RANK or FETCH FIRST WITH TIES.
**Explain simply:**
- Group, then count, then ORDER BY the count DESC, then LIMIT 3.
- LIMIT is MySQL/PostgreSQL/SQLite; SQL Server uses SELECT TOP 3; Oracle and standard SQL use FETCH FIRST 3 ROWS ONLY (alternatives not run here).
- A tie-break column makes the answer deterministic.
**Example:** Which three departments are the largest? HR 6, IT 5, Sales 3 (Finance with 2 drops off).
**Sample data:**

`employees`

| emp_id | name | dept | salary | hire_date | status |
|---|---|---|---|---|---|
| 1 | Asha | HR | 40000 | 2020-03-01 | Active |
| 2 | Bala | HR | 45000 | 2021-07-15 | Active |
| 3 | Chitra | HR | 52000 | 2022-02-10 | Left |
| 4 | Deepak | HR | 38000 | 2023-01-05 | Active |
| 5 | Esha | HR | NULL | 2023-06-20 | Active |
| 6 | Farhan | HR | 60000 | 2019-11-11 | Left |
| 7 | Gita | IT | 80000 | 2018-05-01 | Active |
| 8 | Hari | IT | 65000 | 2022-03-14 | Active |
| 9 | Indu | IT | 72000 | 2023-04-01 | Left |
| 10 | Jai | IT | 55000 | 2021-09-09 | Active |
| 11 | Kiran | IT | 90000 | 2022-08-18 | Active |
| 12 | Lata | Sales | 35000 | 2022-01-02 | Active |
| 13 | Manoj | Sales | 42000 | 2023-02-02 | Left |
| 14 | Neha | Sales | 30000 | 2020-10-10 | Active |
| 15 | Omar | Finance | 70000 | 2021-12-01 | Active |
| 16 | Pooja | Finance | 66000 | 2023-05-05 | Active |

**SQL:**
```sql
SELECT dept, COUNT(*) AS employee_count
FROM employees
GROUP BY dept
ORDER BY employee_count DESC, dept
LIMIT 3;
-- SQL Server:  SELECT TOP 3 dept, COUNT(*) ... ORDER BY COUNT(*) DESC;
-- Oracle/PostgreSQL:  ... ORDER BY employee_count DESC FETCH FIRST 3 ROWS ONLY;
```
**Output:**

| dept | employee_count |
|---|---|
| HR | 6 |
| IT | 5 |
| Sales | 3 |

**pandas equivalent:**
```python
res = (emp.groupby('dept').size().reset_index(name='employee_count')
          .sort_values(['employee_count', 'dept'], ascending=[False, True]).head(3))
# Output:
#  dept  employee_count
#    HR               6
#    IT               5
# Sales               3
```
**Edge cases:** If the 3rd and 4th departments both had 3 people, LIMIT 3 would silently drop one; use RANK() <= 3 or FETCH FIRST 3 ROWS WITH TIES (Oracle, PostgreSQL 13+, SQL Server TOP 3 WITH TIES) to keep both.
**Likely follow-ups:**
- Top 3 by total salary instead? Replace COUNT(*) with SUM(salary).
- Why ORDER BY before LIMIT? LIMIT just cuts the rows in their current order.
**Common mistakes:** Using LIMIT without ORDER BY, which returns three arbitrary rows.

### Q18 ⭐⭐ 🟢 Given orders(order_id, customer_id, category, amount, order_date), find how many distinct customers bought in each category.
**Asked at:** commonly listed in SQL prep guides for data analyst roles (LearnSQL, Indeed India, CCBP); research notes list GROUP BY/HAVING as a standard service-MNC SQL question type (COUNT DISTINCT is used in a real product-company question on StrataScratch)
**What the interviewer is checking:** Do you know COUNT(DISTINCT ...) and the difference from counting orders?
**Say this in the interview:** I group by category and use COUNT(DISTINCT customer_id), so a customer who bought three times in a category is counted once.
**Explain simply:**
- COUNT(*) would give number of orders; COUNT(DISTINCT customer_id) gives number of different customers.
- DISTINCT is applied inside each group, per category.
- Same customer in two categories is counted once in each.
**Example:** Marketing wants reach: how many different shoppers bought Grocery vs Electronics.
**Sample data:**

`orders`

| order_id | customer_id | category | amount | order_date |
|---|---|---|---|---|
| 1 | C1 | Electronics | 4000 | 2025-01-05 |
| 2 | C1 | Electronics | 3500 | 2025-01-20 |
| 3 | C1 | Clothing | 2000 | 2025-02-03 |
| 4 | C1 | Grocery | 1500 | 2025-02-14 |
| 5 | C1 | Grocery | 800 | 2025-03-02 |
| 6 | C2 | Clothing | 1200 | 2025-01-15 |
| 7 | C2 | Clothing | 900 | 2025-01-28 |
| 8 | C2 | Electronics | 6000 | 2025-03-09 |
| 9 | C3 | Grocery | 450 | 2025-02-01 |
| 10 | C3 | Grocery | 300 | 2025-02-01 |
| 11 | C3 | Clothing | 700 | 2025-03-15 |
| 12 | C4 | Electronics | 12000 | 2025-02-20 |
| 13 | C4 | Electronics | 5000 | 2026-01-10 |

**SQL:**
```sql
SELECT category,
       COUNT(*)                    AS orders,
       COUNT(DISTINCT customer_id) AS distinct_customers
FROM orders
GROUP BY category
ORDER BY category;
```
**Output:**

| category | orders | distinct_customers |
|---|---|---|
| Clothing | 4 | 3 |
| Electronics | 5 | 3 |
| Grocery | 4 | 2 |

**pandas equivalent:**
```python
res = (orders.groupby('category').agg(orders=('order_id', 'size'), distinct_customers=('customer_id', 'nunique'))
          .reset_index().sort_values('category'))
# Output:
#    category  orders  distinct_customers
#    Clothing       4                   3
# Electronics       5                   3
#     Grocery       4                   2
```
**Edge cases:** NULL customer_id is ignored by COUNT(DISTINCT). A total across categories is not the sum of these numbers because a customer in two categories is counted twice.
**Likely follow-ups:**
- How many customers bought at all? COUNT(DISTINCT customer_id) over the whole table (4 here).
- Is COUNT(DISTINCT) slow? It can be on huge tables; it needs de-duplication.
**Common mistakes:** Adding the per-category distinct counts to get the total unique customers.

### Q19 ⭐⭐ 🟢 A salary column has NULLs. Why can AVG(salary) differ from SUM(salary)/COUNT(*)? Which one is right?
**Asked at:** commonly listed in SQL prep guides for data analyst roles (LearnSQL, Indeed India, CCBP); research notes list GROUP BY/HAVING as a standard service-MNC SQL question type
**What the interviewer is checking:** Do you understand that AVG divides by non-NULL values?
**Say this in the interview:** AVG(salary) divides by the number of rows that have a salary. SUM(salary)/COUNT(*) divides by all rows including NULL ones, so it comes out lower. AVG is the right one unless the business says a missing salary means zero.
**Explain simply:**
- SUM skips NULL, AVG skips NULL, COUNT(*) does not skip.
- AVG(salary) = SUM(salary)/COUNT(salary), which is what the database does.
- Dividing by COUNT(*) treats missing as zero and understates the average.
- If NULL really means 0 (for example, no bonus paid), use AVG(COALESCE(salary, 0)).
**Example:** HR department: 5 salaries recorded (total 235000) and 1 pending. AVG = 235000 / 5 = 47000, but 235000 / 6 = 39166.67.
**Sample data:**

`employees`

| emp_id | name | dept | salary | hire_date | status |
|---|---|---|---|---|---|
| 1 | Asha | HR | 40000 | 2020-03-01 | Active |
| 2 | Bala | HR | 45000 | 2021-07-15 | Active |
| 3 | Chitra | HR | 52000 | 2022-02-10 | Left |
| 4 | Deepak | HR | 38000 | 2023-01-05 | Active |
| 5 | Esha | HR | NULL | 2023-06-20 | Active |
| 6 | Farhan | HR | 60000 | 2019-11-11 | Left |
| 7 | Gita | IT | 80000 | 2018-05-01 | Active |
| 8 | Hari | IT | 65000 | 2022-03-14 | Active |
| 9 | Indu | IT | 72000 | 2023-04-01 | Left |
| 10 | Jai | IT | 55000 | 2021-09-09 | Active |
| 11 | Kiran | IT | 90000 | 2022-08-18 | Active |
| 12 | Lata | Sales | 35000 | 2022-01-02 | Active |
| 13 | Manoj | Sales | 42000 | 2023-02-02 | Left |
| 14 | Neha | Sales | 30000 | 2020-10-10 | Active |
| 15 | Omar | Finance | 70000 | 2021-12-01 | Active |
| 16 | Pooja | Finance | 66000 | 2023-05-05 | Active |

**SQL:**
```sql
SELECT dept,
       AVG(salary)                         AS avg_salary,
       SUM(salary) * 1.0 / COUNT(*)        AS sum_div_count_star,
       SUM(salary) * 1.0 / COUNT(salary)   AS sum_div_count_col
FROM employees
GROUP BY dept
ORDER BY dept;
```
**Output:**

| dept | avg_salary | sum_div_count_star | sum_div_count_col |
|---|---|---|---|
| Finance | 68000 | 68000 | 68000 |
| HR | 47000 | 39166.67 | 47000 |
| IT | 72400 | 72400 | 72400 |
| Sales | 35666.67 | 35666.67 | 35666.67 |

**pandas equivalent:**
```python
g = emp.groupby('dept')['salary']
res = pd.DataFrame({'avg_salary': g.mean(), 'sum_div_count_star': g.sum() / emp.groupby('dept').size(),
                    'sum_div_count_col': g.sum() / g.count()}).reset_index()
# Output:
#    dept   avg_salary  sum_div_count_star  sum_div_count_col
# Finance 68000.000000        68000.000000       68000.000000
#      HR 47000.000000        39166.666667       47000.000000
#      IT 72400.000000        72400.000000       72400.000000
#   Sales 35666.666667        35666.666667       35666.666667
```
**Edge cases:** Only HR differs because only HR has a NULL. The * 1.0 avoids integer division in SQL Server and PostgreSQL (INT / INT drops decimals); SQLite did it above for the same reason. All-NULL group: AVG is NULL, SUM/COUNT(*) becomes NULL or 0 depending on the rest.
**Likely follow-ups:**
- When would AVG(COALESCE(salary, 0)) be right? When a missing value truly means zero.
- Does MIN/MAX ignore NULL too? Yes.
**Common mistakes:** Using SUM/COUNT(*) and wondering why it does not match AVG.

### Q20 ⭐⭐ 🟢 Can you use aggregate functions without GROUP BY? What does the query return, e.g., SELECT COUNT(*), AVG(salary) FROM employees?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know that aggregates without GROUP BY treat the whole table as one group?
**Say this in the interview:** Yes. With no GROUP BY, the aggregate functions run over all the rows and return exactly one row, here the headcount and the average salary of the whole company.
**Explain simply:**
- An aggregate function (COUNT, SUM, AVG, MIN, MAX) squeezes many rows into one number.
- Without GROUP BY the whole table is treated as a single group, so you get one row back.
- The catch: you cannot add a plain column such as `dept` next to an aggregate unless you group by it. Strict databases (PostgreSQL, SQL Server) raise an error; old MySQL silently picks a random value.
- COUNT(*) counts rows; COUNT(salary) counts only rows where salary is not NULL; AVG ignores NULLs.
**Example:** HR wants one headline number for the dashboard: total headcount and average salary. The 8 employees below give 8 and 58,750.
**Sample data:**
**employees** (8 rows)

| emp_id | name | dept | salary | hire_date | status |
|---|---|---|---|---|---|
| 1 | Asha | HR | 45000 | 2020-03-01 | Active |
| 2 | Ravi | HR | 52000 | 2019-07-15 | Left |
| 3 | Ravi K | HR | 50000 | 2021-01-10 | Active |
| 4 | Karan | IT | 75000 | 2020-09-01 | Left |
| 5 | Sunil | IT | 110000 | 2017-02-11 | Active |
| 6 | Priya | Sales | 40000 | 2022-04-04 | Active |
| 7 | Neha | Sales | 38000 | 2023-01-09 | Left |
| 8 | Omar | Finance | 60000 | 2019-11-30 | Active |
**SQL:**
```sql
SELECT COUNT(*) AS headcount, AVG(salary) AS avg_salary
FROM employees;
```
**Output:**

| headcount | avg_salary |
|---|---|
| 8 | 58750 |
**pandas equivalent:** (run; result identical to the Output above)
```python
# whole-table aggregate: build a one-row frame
res = pd.DataFrame({'headcount': [len(emp)], 'avg_salary': [emp['salary'].mean()]})
```
**Edge cases:** An empty table still returns one row (COUNT = 0, AVG = NULL). AVG ignores NULL salaries, but COUNT(*) still counts the row.
**Likely follow-ups:** Q: What if I add `dept`? A: Error in strict SQL, because dept has many values but the output is one row. Add GROUP BY dept.
**Common mistakes:** Mixing a plain column with an aggregate and no GROUP BY; assuming AVG counts NULL as zero (it skips them).

### Q21 ⭐⭐ 🟢 What do SUM and COUNT return when no rows match? Why is SUM NULL but COUNT 0, and how does COALESCE help?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand NULL versus zero, and can you tame NULL with COALESCE?
**Say this in the interview:** When no row matches, COUNT returns 0 because it counts rows and there are none, but SUM returns NULL because there is nothing to add up, so the answer is unknown, not zero. I wrap it in COALESCE(SUM(x), 0) when the report needs a zero.
**Explain simply:**
- COUNT answers 'how many rows?' and zero is a perfectly good answer.
- SUM, AVG, MIN, MAX answer 'what is the value?' and with no rows there is no value, so SQL returns NULL (NULL means unknown or missing).
- COALESCE(a, b) returns the first non-NULL argument, so COALESCE(SUM(x), 0) turns the NULL into 0.
- Do not use COALESCE on AVG blindly: an average of 0 can be misleading.
**Example:** Legal department has no employees yet. Its salary bill is NULL, its headcount is 0, and a payroll report should show 0.
**Sample data:**
**employees** (8 rows)

| emp_id | name | dept | salary | hire_date | status |
|---|---|---|---|---|---|
| 1 | Asha | HR | 45000 | 2020-03-01 | Active |
| 2 | Ravi | HR | 52000 | 2019-07-15 | Left |
| 3 | Ravi K | HR | 50000 | 2021-01-10 | Active |
| 4 | Karan | IT | 75000 | 2020-09-01 | Left |
| 5 | Sunil | IT | 110000 | 2017-02-11 | Active |
| 6 | Priya | Sales | 40000 | 2022-04-04 | Active |
| 7 | Neha | Sales | 38000 | 2023-01-09 | Left |
| 8 | Omar | Finance | 60000 | 2019-11-30 | Active |
**SQL:**
```sql
SELECT SUM(salary) AS total_salary,
       COUNT(*) AS rows_n,
       COUNT(salary) AS cnt_salary,
       COALESCE(SUM(salary), 0) AS total_or_zero
FROM employees
WHERE dept = 'Legal';
```
**Output:**

| total_salary | rows_n | cnt_salary | total_or_zero |
|---|---|---|---|
| NULL | 0 | 0 | 0 |
**pandas equivalent:** (run; result identical to the Output above)
```python
m = emp[emp['dept'] == 'Legal']['salary']
res = pd.DataFrame({'total_salary': [m.sum(min_count=1)], 'rows_n': [len(m)], 'cnt_salary': [m.count()], 'total_or_zero': [m.sum()]})
```
**Edge cases:** Rows exist but all salaries are NULL: SUM is NULL, COUNT(*) is the row count, COUNT(salary) is 0. In pandas, `.sum()` of an empty Series is 0 (it differs from SQL); use `min_count=1` to get NaN like SQL. SQL Server uses ISNULL and Oracle NVL as alternatives (not run here).
**Likely follow-ups:** Q: Does GROUP BY change this? A: With GROUP BY, a group with no rows simply does not appear, so you get no row, not a NULL row.
**Common mistakes:** Assuming SUM of nothing is 0; forgetting that COUNT(column) skips NULLs while COUNT(*) does not.

### Q22 ⭐⭐ 🟢 What is the difference between DISTINCT and GROUP BY? When would you use each?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you explain two ways to de-duplicate and pick the right one?
**Say this in the interview:** DISTINCT just removes duplicate rows from the result. GROUP BY collapses rows into groups so I can also calculate something per group. If I only need the unique list I use DISTINCT; if I need counts, sums or averages I use GROUP BY.
**Explain simply:**
- DISTINCT: 'show me each unique value once'. No calculation.
- GROUP BY: 'put rows with the same value together, then calculate per group'.
- Without an aggregate, `SELECT dept FROM employees GROUP BY dept` gives the same rows as `SELECT DISTINCT dept`, and most engines run them the same way.
- Use GROUP BY plus HAVING when you need to filter on the aggregate (e.g. departments with 2+ people).
**Example:** List of departments that have staff: DISTINCT. Headcount per department: GROUP BY.
**Sample data:**
**employees** (8 rows)

| emp_id | name | dept | salary | hire_date | status |
|---|---|---|---|---|---|
| 1 | Asha | HR | 45000 | 2020-03-01 | Active |
| 2 | Ravi | HR | 52000 | 2019-07-15 | Left |
| 3 | Ravi K | HR | 50000 | 2021-01-10 | Active |
| 4 | Karan | IT | 75000 | 2020-09-01 | Left |
| 5 | Sunil | IT | 110000 | 2017-02-11 | Active |
| 6 | Priya | Sales | 40000 | 2022-04-04 | Active |
| 7 | Neha | Sales | 38000 | 2023-01-09 | Left |
| 8 | Omar | Finance | 60000 | 2019-11-30 | Active |
**SQL:**
```sql
-- unique list
SELECT DISTINCT dept FROM employees ORDER BY dept;
```
**Output:**

| dept |
|---|
| Finance |
| HR |
| IT |
| Sales |
Same list with GROUP BY, plus a count (the GROUP BY-only ability):

```sql
SELECT dept, COUNT(*) AS headcount
FROM employees
GROUP BY dept
ORDER BY dept;
```

| dept | headcount |
|---|---|
| Finance | 1 |
| HR | 3 |
| IT | 2 |
| Sales | 2 |
**pandas equivalent:** (run; result identical to the Output above)
```python
res = emp[['dept']].drop_duplicates().sort_values('dept').reset_index(drop=True)
```
**Edge cases:** DISTINCT applies to the whole row, not one column: `SELECT DISTINCT dept, status` gives unique pairs. NULLs are treated as one value by both.
**Likely follow-ups:** Q: Same result, so is one faster? A: Usually identical; check the execution plan. Q: Can I count unique values? A: COUNT(DISTINCT col).
**Common mistakes:** Thinking `DISTINCT dept, status` dedupes only dept; writing GROUP BY when only DISTINCT is needed.

### Q23 ⭐⭐ 🟢 Given employees(emp_id, name, dept, salary, hire_date, status), which department has the highest total salary bill? What if two departments tie?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you aggregate, rank, and handle ties instead of blindly using LIMIT 1?
**Say this in the interview:** I total salary per department with GROUP BY, then keep the department whose total equals the maximum. That returns all tied departments, whereas ORDER BY ... LIMIT 1 would silently drop one.
**Explain simply:**
- Salary bill = SUM(salary) per department.
- Step 1 in a CTE (a named temporary result, `WITH ... AS`): total per department.
- Step 2: keep rows equal to the maximum total, so ties all survive.
- `RANK() OVER (ORDER BY total DESC) = 1` does the same job.
**Example:** IT has two people costing 185,000 a month, the biggest bill. If HR also had 185,000, both should be shown.
**Sample data:**
**employees** (8 rows)

| emp_id | name | dept | salary | hire_date | status |
|---|---|---|---|---|---|
| 1 | Asha | HR | 45000 | 2020-03-01 | Active |
| 2 | Ravi | HR | 52000 | 2019-07-15 | Left |
| 3 | Ravi K | HR | 50000 | 2021-01-10 | Active |
| 4 | Karan | IT | 75000 | 2020-09-01 | Left |
| 5 | Sunil | IT | 110000 | 2017-02-11 | Active |
| 6 | Priya | Sales | 40000 | 2022-04-04 | Active |
| 7 | Neha | Sales | 38000 | 2023-01-09 | Left |
| 8 | Omar | Finance | 60000 | 2019-11-30 | Active |
**SQL:**
```sql
WITH bill AS (
  SELECT dept, SUM(salary) AS total_salary
  FROM employees
  GROUP BY dept
)
SELECT dept, total_salary
FROM bill
WHERE total_salary = (SELECT MAX(total_salary) FROM bill);
```
**Output:**

| dept | total_salary |
|---|---|
| IT | 185000 |
**pandas equivalent:** (run; result identical to the Output above)
```python
bill = emp.groupby('dept', as_index=False).agg(total_salary=('salary', 'sum'))
res = bill[bill['total_salary'] == bill['total_salary'].max()].reset_index(drop=True)
```
**Edge cases:** Tie demo: I added a 9th employee (HR, 38,000) in a scratch copy so HR also hits 185,000. `ORDER BY total_salary DESC LIMIT 1` returns only one row:

| dept | total_salary |
|---|---|
| IT | 185000 |

The MAX-equality query returns both:

| dept | total_salary |
|---|---|
| HR | 185000 |
| IT | 185000 |

NULL salaries are skipped by SUM; a department with all-NULL salaries has a NULL total and never wins.
**Likely follow-ups:** Q: LIMIT syntax per database? A: MySQL/PostgreSQL/SQLite `LIMIT 1`; SQL Server `TOP 1` (`TOP 1 WITH TIES` keeps ties); standard `FETCH FIRST 1 ROWS WITH TIES` (not run here).
**Common mistakes:** Using LIMIT 1 and ignoring ties; using `WHERE salary = MAX(salary)` (aggregates are not allowed in WHERE).

### Q24 ⭐⭐ 🟢 Given orders(order_id, customer_id, category, amount, order_date), find each customer's first and last order date (MIN and MAX on dates).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know MIN/MAX work on dates and text, not just numbers?
**Say this in the interview:** I group by customer and take MIN of the order date for the first order and MAX for the last. MIN and MAX work on dates because dates sort in time order.
**Explain simply:**
- MIN(date) is the earliest date, MAX(date) the latest.
- This only works if the column is a real date type, or text in YYYY-MM-DD form which sorts correctly. A text like '05-01-2025' would sort wrongly.
- NULL dates are ignored.
**Example:** HR parallel: first and last attendance day per employee. Here customer C1 first ordered on 2025-01-05 and last on 2026-01-08.
**Sample data:**
**orders** (8 rows)

| order_id | customer_id | category | amount | order_date |
|---|---|---|---|---|
| 1 | C1 | Laptop | 1000 | 2025-01-05 |
| 2 | C1 | Phone | 500 | 2025-01-05 |
| 3 | C2 | Laptop | 1200 | 2025-02-10 |
| 4 | C2 | Phone | 300 | 2025-04-15 |
| 5 | C3 | Tablet | 400 | 2025-07-01 |
| 6 | C3 | Laptop | 800 | 2025-10-12 |
| 7 | C4 | Phone | 600 | 2026-01-08 |
| 8 | C1 | Tablet | 200 | 2026-01-08 |
**SQL:**
```sql
SELECT customer_id,
       MIN(order_date) AS first_order,
       MAX(order_date) AS last_order
FROM orders
GROUP BY customer_id
ORDER BY customer_id;
```
**Output:**

| customer_id | first_order | last_order |
|---|---|---|
| C1 | 2025-01-05 | 2026-01-08 |
| C2 | 2025-02-10 | 2025-04-15 |
| C3 | 2025-07-01 | 2025-10-12 |
| C4 | 2026-01-08 | 2026-01-08 |
**pandas equivalent:** (run; result identical to the Output above)
```python
res = (orders.groupby('customer_id', as_index=False)
       .agg(first_order=('order_date', 'min'), last_order=('order_date', 'max')))
res['first_order'] = res['first_order'].dt.strftime('%Y-%m-%d')
res['last_order'] = res['last_order'].dt.strftime('%Y-%m-%d')
```
**Edge cases:** A customer with one order gets the same first and last date. A customer with only NULL dates gets NULL. If you also want the amount of the first order, MIN/MAX is not enough; use ROW_NUMBER().
**Likely follow-ups:** Q: How many days between first and last? A: Dialect specific: SQLite `julianday(MAX(d)) - julianday(MIN(d))`, MySQL `DATEDIFF(MAX(d), MIN(d))`, SQL Server `DATEDIFF(day, MIN(d), MAX(d))` (not run here).
**Common mistakes:** Storing dates as text in DD-MM-YYYY, so MIN/MAX sort alphabetically; selecting a non-grouped column such as category next to MIN.

### Q25 ⭐⭐ 🟡 Given employees(emp_id, name, dept, salary, hire_date, status) where status is 'Active' or 'Left', count active and left employees per department in one row using conditional aggregation (CASE WHEN inside SUM or COUNT).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you do conditional aggregation, which is the core trick behind pivots and attrition reports?
**Say this in the interview:** Inside each department group I use SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END), which adds 1 for every matching row and 0 otherwise. That gives separate columns for active and left in one row per department.
**Explain simply:**
- CASE WHEN is SQL's IF/ELSE; it makes a 1 or a 0 for each row.
- SUM then adds those 1s, effectively counting rows that meet the condition.
- Alternative: `COUNT(CASE WHEN status='Active' THEN 1 END)`. COUNT skips NULLs, and CASE without ELSE gives NULL when the condition fails.
- PostgreSQL/SQLite also have `COUNT(*) FILTER (WHERE status='Active')`.
**Example:** The HR head wants one line per department: Active vs Left. HR has 2 active and 1 left.
**Sample data:**
**employees** (8 rows)

| emp_id | name | dept | salary | hire_date | status |
|---|---|---|---|---|---|
| 1 | Asha | HR | 45000 | 2020-03-01 | Active |
| 2 | Ravi | HR | 52000 | 2019-07-15 | Left |
| 3 | Ravi K | HR | 50000 | 2021-01-10 | Active |
| 4 | Karan | IT | 75000 | 2020-09-01 | Left |
| 5 | Sunil | IT | 110000 | 2017-02-11 | Active |
| 6 | Priya | Sales | 40000 | 2022-04-04 | Active |
| 7 | Neha | Sales | 38000 | 2023-01-09 | Left |
| 8 | Omar | Finance | 60000 | 2019-11-30 | Active |
**SQL:**
```sql
SELECT dept,
       SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) AS active_cnt,
       SUM(CASE WHEN status = 'Left'   THEN 1 ELSE 0 END) AS left_cnt
FROM employees
GROUP BY dept
ORDER BY dept;
```
**Output:**

| dept | active_cnt | left_cnt |
|---|---|---|
| Finance | 1 | 0 |
| HR | 2 | 1 |
| IT | 1 | 1 |
| Sales | 1 | 1 |
**pandas equivalent:** (run; result identical to the Output above)
```python
t = emp.assign(a=(emp['status'] == 'Active').astype(int), l=(emp['status'] == 'Left').astype(int))
res = t.groupby('dept', as_index=False).agg(active_cnt=('a', 'sum'), left_cnt=('l', 'sum')).sort_values('dept').reset_index(drop=True)
```
**Edge cases:** Status values with different spelling ('left', 'Left ') are missed; clean them first. NULL status counts in neither column. Use ELSE 0 with SUM, otherwise a group with no matches returns NULL.
**Likely follow-ups:** Q: Same with COUNT? A: COUNT(CASE WHEN status='Left' THEN 1 END), and no ELSE. Q: Turn rows into columns for many values? A: Repeat the CASE for each value.
**Common mistakes:** Writing `COUNT(CASE WHEN ... THEN 1 ELSE 0 END)`, which counts every row because 0 is not NULL; forgetting GROUP BY.

### Q26 ⭐⭐ 🟡 Given employees(emp_id, name, dept, salary, hire_date, status), calculate the attrition rate (percentage of employees who left) for each department.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you build a ratio from conditional counts and avoid integer division?
**Say this in the interview:** Attrition rate is leavers divided by total employees in the department. I count leavers with SUM(CASE WHEN ...) and divide by COUNT(*), multiplying by 100.0 so the division is not an integer division.
**Explain simply:**
- Attrition rate (%) = employees who left / total employees x 100.
- In many databases 1 / 3 with two integers gives 0, because integer division drops the decimals. Multiplying by 100.0 first forces a decimal answer.
- Strictly, textbook attrition uses the average headcount over the period; this simple version uses everyone in the table, which is what the question asks.
**Example:** HR has 3 people, 1 left: 33.33%. IT has 2, 1 left: 50%.
**Sample data:**
**employees** (8 rows)

| emp_id | name | dept | salary | hire_date | status |
|---|---|---|---|---|---|
| 1 | Asha | HR | 45000 | 2020-03-01 | Active |
| 2 | Ravi | HR | 52000 | 2019-07-15 | Left |
| 3 | Ravi K | HR | 50000 | 2021-01-10 | Active |
| 4 | Karan | IT | 75000 | 2020-09-01 | Left |
| 5 | Sunil | IT | 110000 | 2017-02-11 | Active |
| 6 | Priya | Sales | 40000 | 2022-04-04 | Active |
| 7 | Neha | Sales | 38000 | 2023-01-09 | Left |
| 8 | Omar | Finance | 60000 | 2019-11-30 | Active |
**SQL:**
```sql
SELECT dept,
       COUNT(*) AS headcount,
       SUM(CASE WHEN status = 'Left' THEN 1 ELSE 0 END) AS left_cnt,
       ROUND(100.0 * SUM(CASE WHEN status = 'Left' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_pct
FROM employees
GROUP BY dept
ORDER BY dept;
```
**Output:**

| dept | headcount | left_cnt | attrition_pct |
|---|---|---|---|
| Finance | 1 | 0 | 0 |
| HR | 3 | 1 | 33.33 |
| IT | 2 | 1 | 50 |
| Sales | 2 | 1 | 50 |
**pandas equivalent:** (run; result identical to the Output above)
```python
g = emp.groupby('dept').agg(headcount=('emp_id', 'count'), left_cnt=('status', lambda s: (s == 'Left').sum()))
g['attrition_pct'] = (100.0 * g['left_cnt'] / g['headcount']).round(2)
res = g.reset_index().sort_values('dept').reset_index(drop=True)
```
**Edge cases:** COUNT(*) is never 0 inside a group, so no divide-by-zero here; with a LEFT JOIN from a department list (Q31) use NULLIF(COUNT(e.emp_id), 0). Employees with NULL status count in the denominator but not as leavers.
**Likely follow-ups:** Q: Rank worst departments? A: ORDER BY attrition_pct DESC. Q: Only departments above 40%? A: Put the same expression in HAVING.
**Common mistakes:** Writing `SUM(...)/COUNT(*)*100` with integers and getting 0; dividing by the Active count instead of total headcount.

### Q27 ⭐⭐ 🟡 Given orders(order_id, customer_id, category, amount, order_date), produce one row per category with separate columns for Q1, Q2, Q3, Q4 sales (a manual pivot with conditional aggregation).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you pivot rows into columns by hand?
**Say this in the interview:** I group by category and use one SUM(CASE WHEN ...) per quarter, so each quarter becomes its own column. I also filter to one year, otherwise Q1 2025 and Q1 2026 would be added together.
**Explain simply:**
- A pivot turns row values (the quarter) into column headings.
- Each CASE puts the amount into the right quarter's column and 0 elsewhere; SUM adds them up.
- Quarter from the month number: 1-3 is Q1, 4-6 Q2, 7-9 Q3, 10-12 Q4.
- Dialect: MySQL `QUARTER(order_date)`, PostgreSQL `EXTRACT(QUARTER FROM order_date)`, SQL Server `DATEPART(quarter, order_date)` (not run here); SQLite has none, hence the month trick.
**Example:** Laptop sold 1,000 + 1,200 = 2,200 in Q1 2025 and 800 in Q4 2025. The 2026 order is excluded by the year filter.
**Sample data:**
**orders** (8 rows)

| order_id | customer_id | category | amount | order_date |
|---|---|---|---|---|
| 1 | C1 | Laptop | 1000 | 2025-01-05 |
| 2 | C1 | Phone | 500 | 2025-01-05 |
| 3 | C2 | Laptop | 1200 | 2025-02-10 |
| 4 | C2 | Phone | 300 | 2025-04-15 |
| 5 | C3 | Tablet | 400 | 2025-07-01 |
| 6 | C3 | Laptop | 800 | 2025-10-12 |
| 7 | C4 | Phone | 600 | 2026-01-08 |
| 8 | C1 | Tablet | 200 | 2026-01-08 |
**SQL:**
```sql
SELECT category,
       SUM(CASE WHEN CAST(strftime('%m', order_date) AS INT) BETWEEN 1 AND 3   THEN amount ELSE 0 END) AS q1,
       SUM(CASE WHEN CAST(strftime('%m', order_date) AS INT) BETWEEN 4 AND 6   THEN amount ELSE 0 END) AS q2,
       SUM(CASE WHEN CAST(strftime('%m', order_date) AS INT) BETWEEN 7 AND 9   THEN amount ELSE 0 END) AS q3,
       SUM(CASE WHEN CAST(strftime('%m', order_date) AS INT) BETWEEN 10 AND 12 THEN amount ELSE 0 END) AS q4
FROM orders
WHERE order_date >= '2025-01-01' AND order_date < '2026-01-01'
GROUP BY category
ORDER BY category;
```
**Output:**

| category | q1 | q2 | q3 | q4 |
|---|---|---|---|---|
| Laptop | 2200 | 0 | 0 | 800 |
| Phone | 500 | 300 | 0 | 0 |
| Tablet | 0 | 0 | 400 | 0 |
**pandas equivalent:** (run; result identical to the Output above)
```python
o = orders[orders['order_date'].dt.year == 2025].copy()
o['q'] = 'q' + o['order_date'].dt.quarter.astype(str)
res = (o.pivot_table(index='category', columns='q', values='amount', aggfunc='sum', fill_value=0)
         .reindex(columns=['q1', 'q2', 'q3', 'q4'], fill_value=0).reset_index())
res.columns.name = None
```
**Edge cases:** Forgetting the year filter mixes years. Quarters with no sales show 0 thanks to ELSE 0. If a category has no 2025 orders it disappears; join to a category list to keep it.
**Likely follow-ups:** Q: How to get the year too? A: Add the year to GROUP BY. Q: Native pivot? A: SQL Server and Oracle have PIVOT; MySQL/PostgreSQL use this CASE method.
**Common mistakes:** Forgetting the year filter; using `ELSE amount` (counts every row in every column).

### Q28 ⭐⭐ 🟡 For each duplicated email, list all the employee IDs that share it in a single cell (STRING_AGG / GROUP_CONCAT).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know how to find duplicates and list their members in one cell?
**Say this in the interview:** I group by email, keep groups with more than one row using HAVING COUNT(*) > 1, and join the employee IDs into one text value with GROUP_CONCAT in MySQL/SQLite or STRING_AGG in PostgreSQL and SQL Server.
**Explain simply:**
- Group by the column that should be unique (email).
- HAVING filters groups after counting; WHERE cannot, because WHERE runs before grouping.
- String aggregation glues the values of a group into one string, like a comma-separated list.
**Example:** Two employees (2 and 3) were entered with ravi@x.com, and 6 and 7 share a mailbox: data-quality issues HR must fix.
**Sample data:**
**employees** (8 rows)

| emp_id | name | dept | salary | hire_date | status |
|---|---|---|---|---|---|
| 1 | Asha | HR | 45000 | 2020-03-01 | Active |
| 2 | Ravi | HR | 52000 | 2019-07-15 | Left |
| 3 | Ravi K | HR | 50000 | 2021-01-10 | Active |
| 4 | Karan | IT | 75000 | 2020-09-01 | Left |
| 5 | Sunil | IT | 110000 | 2017-02-11 | Active |
| 6 | Priya | Sales | 40000 | 2022-04-04 | Active |
| 7 | Neha | Sales | 38000 | 2023-01-09 | Left |
| 8 | Omar | Finance | 60000 | 2019-11-30 | Active |

Emails: Ravi and Ravi K share `ravi@x.com`; Priya and Neha share `sales@x.com` (the email column is also in the table).
**SQL:**
```sql
SELECT email,
       COUNT(*) AS n,
       GROUP_CONCAT(emp_id, ', ') AS emp_ids
FROM employees
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY email;
```
**Output:**

| email | n | emp_ids |
|---|---|---|
| ravi@x.com | 2 | 2, 3 |
| sales@x.com | 2 | 6, 7 |
**pandas equivalent:** (run; result identical to the Output above)
```python
g = emp.groupby('email').agg(n=('emp_id', 'count'), emp_ids=('emp_id', lambda s: ', '.join(map(str, s))))
res = g[g['n'] > 1].reset_index().sort_values('email').reset_index(drop=True)
```
**Edge cases:** NULL emails group together in one NULL group; exclude them with `WHERE email IS NOT NULL` if missing is not a duplicate. Case differences (`Ravi@x.com` vs `ravi@x.com`) hide duplicates: group by LOWER(TRIM(email)). Order inside the list is not guaranteed unless you specify it.
**Likely follow-ups:** Q: Syntax elsewhere? A: MySQL `GROUP_CONCAT(emp_id ORDER BY emp_id SEPARATOR ', ')`; PostgreSQL `STRING_AGG(emp_id::text, ', ' ORDER BY emp_id)`; SQL Server `STRING_AGG(emp_id, ', ')` (not run here).
**Common mistakes:** Using WHERE COUNT(*) > 1; forgetting that STRING_AGG needs text in PostgreSQL (cast the ID).

### Q29 ⭐⭐ 🟡 Given orders(order_id, customer_id, category, amount, order_date), list the categories whose average order value is above the overall average order value (subquery inside HAVING).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you use a subquery to compare a group against the overall figure?
**Say this in the interview:** I compute each category's average in the grouped query, and in HAVING I compare it to a subquery that returns the overall average of all orders. Only the categories above that line survive.
**Explain simply:**
- A subquery is a query inside another query; here it returns a single number.
- HAVING filters groups after the average is calculated, which WHERE cannot do.
- The subquery runs over the whole table, not per group, so it gives the company-wide average (625 here).
**Example:** Overall average order is 5,000 / 8 = 625. Laptop averages 1,000, so it is above; Phone (466.67) and Tablet (300) are not.
**Sample data:**
**orders** (8 rows)

| order_id | customer_id | category | amount | order_date |
|---|---|---|---|---|
| 1 | C1 | Laptop | 1000 | 2025-01-05 |
| 2 | C1 | Phone | 500 | 2025-01-05 |
| 3 | C2 | Laptop | 1200 | 2025-02-10 |
| 4 | C2 | Phone | 300 | 2025-04-15 |
| 5 | C3 | Tablet | 400 | 2025-07-01 |
| 6 | C3 | Laptop | 800 | 2025-10-12 |
| 7 | C4 | Phone | 600 | 2026-01-08 |
| 8 | C1 | Tablet | 200 | 2026-01-08 |
**SQL:**
```sql
SELECT category, AVG(amount) AS avg_order_value
FROM orders
GROUP BY category
HAVING AVG(amount) > (SELECT AVG(amount) FROM orders)
ORDER BY category;
```
**Output:**

| category | avg_order_value |
|---|---|
| Laptop | 1000 |
**pandas equivalent:** (run; result identical to the Output above)
```python
overall = orders['amount'].mean()
g = orders.groupby('category', as_index=False).agg(avg_order_value=('amount', 'mean'))
res = g[g['avg_order_value'] > overall].sort_values('category').reset_index(drop=True)
```
**Edge cases:** If no category is above the average (all equal) the result is empty. NULL amounts are ignored by AVG. The overall average is the average of orders, not of category averages (see Q35).
**Likely follow-ups:** Q: Show the overall average beside each row? A: Put the subquery in SELECT or CROSS JOIN a one-row CTE. Q: Window version? A: AVG(amount) OVER () before grouping.
**Common mistakes:** Comparing to the average of the category averages; using WHERE instead of HAVING.

### Q30 ⭐⭐ 🟡 Given employees(emp_id, name, dept, salary, hire_date, status), find departments where the gap between highest and lowest salary is more than 20,000.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you filter groups on an expression built from aggregates?
**Say this in the interview:** I group by department and put MAX(salary) - MIN(salary) > 20000 in HAVING, because the gap only exists after the group is built.
**Explain simply:**
- Gap = highest salary minus lowest salary in the department, a simple pay-spread check.
- HAVING can use any aggregate expression. Some databases allow the alias `gap` in HAVING (MySQL), but PostgreSQL and SQL Server do not, so repeat the expression.
- Thresholds are strict: exactly 20,000 does not qualify.
**Example:** IT pays 75,000 and 110,000: a 35,000 gap, flagged for a pay-equity review. HR spans only 7,000.
**Sample data:**
**employees** (8 rows)

| emp_id | name | dept | salary | hire_date | status |
|---|---|---|---|---|---|
| 1 | Asha | HR | 45000 | 2020-03-01 | Active |
| 2 | Ravi | HR | 52000 | 2019-07-15 | Left |
| 3 | Ravi K | HR | 50000 | 2021-01-10 | Active |
| 4 | Karan | IT | 75000 | 2020-09-01 | Left |
| 5 | Sunil | IT | 110000 | 2017-02-11 | Active |
| 6 | Priya | Sales | 40000 | 2022-04-04 | Active |
| 7 | Neha | Sales | 38000 | 2023-01-09 | Left |
| 8 | Omar | Finance | 60000 | 2019-11-30 | Active |
**SQL:**
```sql
SELECT dept,
       MAX(salary) AS max_salary,
       MIN(salary) AS min_salary,
       MAX(salary) - MIN(salary) AS gap
FROM employees
GROUP BY dept
HAVING MAX(salary) - MIN(salary) > 20000
ORDER BY dept;
```
**Output:**

| dept | max_salary | min_salary | gap |
|---|---|---|---|
| IT | 110000 | 75000 | 35000 |
**pandas equivalent:** (run; result identical to the Output above)
```python
g = emp.groupby('dept', as_index=False).agg(max_salary=('salary', 'max'), min_salary=('salary', 'min'))
g['gap'] = g['max_salary'] - g['min_salary']
res = g[g['gap'] > 20000].sort_values('dept').reset_index(drop=True)
```
**Edge cases:** A one-person department has a gap of 0. NULL salaries are ignored by MAX/MIN. If all NULL, the gap is NULL and the row is dropped.
**Likely follow-ups:** Q: Show who the highest and lowest earners are? A: Join back or use window functions (FIRST_VALUE). Q: Percentage gap? A: (MAX-MIN)*1.0/MIN.
**Common mistakes:** Putting the condition in WHERE; using the alias in HAVING on PostgreSQL/SQL Server.

### Q31 ⭐⭐ 🟡 You have departments(dept_id, dept_name) and employees. Show headcount for every department, including departments with zero employees. Why does COUNT(*) give the wrong answer here?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know LEFT JOIN keeps unmatched rows and how COUNT(*) vs COUNT(column) behaves on them?
**Say this in the interview:** I start from the departments table and LEFT JOIN employees, so every department appears even with no staff. Then I use COUNT(e.emp_id), not COUNT(*), because COUNT(*) counts the NULL-filled row the join creates and reports 1 for an empty department.
**Explain simply:**
- A LEFT JOIN keeps every row from the left table; where nothing matches, the right-side columns are NULL.
- COUNT(*) counts rows, including that one dummy row, so Legal shows 1.
- COUNT(e.emp_id) counts only non-NULL IDs, so Legal shows 0.
- Put the department table on the left, otherwise the empty department vanishes.
**Example:** Legal exists in the org chart but has no hires yet: the report must show Legal = 0, not 1 and not missing.
**Sample data:**
**departments**

| dept_id | dept_name |
|---|---|
| 1 | HR |
| 2 | IT |
| 3 | Sales |
| 4 | Finance |
| 5 | Legal |

**employees** (8 rows)

| emp_id | name | dept | salary | hire_date | status |
|---|---|---|---|---|---|
| 1 | Asha | HR | 45000 | 2020-03-01 | Active |
| 2 | Ravi | HR | 52000 | 2019-07-15 | Left |
| 3 | Ravi K | HR | 50000 | 2021-01-10 | Active |
| 4 | Karan | IT | 75000 | 2020-09-01 | Left |
| 5 | Sunil | IT | 110000 | 2017-02-11 | Active |
| 6 | Priya | Sales | 40000 | 2022-04-04 | Active |
| 7 | Neha | Sales | 38000 | 2023-01-09 | Left |
| 8 | Omar | Finance | 60000 | 2019-11-30 | Active |

The sample employees table stores the department name in `dept`, so I join on `dept_name`. In a real schema you would join on a `dept_id` foreign key.
**SQL:**
```sql
SELECT d.dept_name,
       COUNT(e.emp_id) AS headcount
FROM departments d
LEFT JOIN employees e ON e.dept = d.dept_name
GROUP BY d.dept_name
ORDER BY d.dept_name;
```
**Output:**

| dept_name | headcount |
|---|---|
| Finance | 1 |
| HR | 3 |
| IT | 2 |
| Legal | 0 |
| Sales | 2 |
With the wrong `COUNT(*)`, Legal is shown as 1:

| dept_name | headcount |
|---|---|
| Finance | 1 |
| HR | 3 |
| IT | 2 |
| Legal | 1 |
| Sales | 2 |
**pandas equivalent:** (run; result identical to the Output above)
```python
m = dept.merge(emp, how='left', left_on='dept_name', right_on='dept')
res = (m.groupby('dept_name', as_index=False).agg(headcount=('emp_id', 'count'))
         .sort_values('dept_name').reset_index(drop=True))
```
**Edge cases:** Filtering the right table in WHERE (e.g. `WHERE e.status='Active'`) turns the LEFT JOIN back into an inner join and drops empty departments; put such filters in the ON clause. Department names must match exactly in spelling.
**Likely follow-ups:** Q: What does the wrong version give? A: See above. Q: Departments with zero staff only? A: `HAVING COUNT(e.emp_id) = 0`, or `WHERE e.emp_id IS NULL`.
**Common mistakes:** Using COUNT(*); starting FROM employees; filtering in WHERE after a LEFT JOIN.

### Q32 ⭐⭐ 🟡 Given orders(order_id, customer_id, category, amount, order_date), find monthly revenue by extracting the month from order_date. How do you also keep year separate (Jan 2025 vs Jan 2026)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you group by time period and avoid mixing the same month of different years?
**Say this in the interview:** I extract both the year and the month and group by the pair. If I group by month number alone, January 2025 and January 2026 are added into one row.
**Explain simply:**
- Dates have parts: year, month, day. Grouping by a part buckets rows by it.
- Group by (year, month) or by a single 'YYYY-MM' text such as `strftime('%Y-%m', order_date)`.
- Dialects: MySQL `YEAR(d), MONTH(d)` or `DATE_FORMAT(d, '%Y-%m')`; PostgreSQL `DATE_TRUNC('month', d)` or `EXTRACT(YEAR FROM d)`; SQL Server `YEAR(d), MONTH(d)` or `FORMAT(d, 'yyyy-MM')` (not run here).
**Example:** January revenue: 1,500 in 2025 and 800 in 2026. Group by month alone and you would wrongly see 2,300 for 'January'.
**Sample data:**
**orders** (8 rows)

| order_id | customer_id | category | amount | order_date |
|---|---|---|---|---|
| 1 | C1 | Laptop | 1000 | 2025-01-05 |
| 2 | C1 | Phone | 500 | 2025-01-05 |
| 3 | C2 | Laptop | 1200 | 2025-02-10 |
| 4 | C2 | Phone | 300 | 2025-04-15 |
| 5 | C3 | Tablet | 400 | 2025-07-01 |
| 6 | C3 | Laptop | 800 | 2025-10-12 |
| 7 | C4 | Phone | 600 | 2026-01-08 |
| 8 | C1 | Tablet | 200 | 2026-01-08 |
**SQL:**
```sql
SELECT strftime('%Y', order_date) AS yr,
       strftime('%m', order_date) AS mth,
       SUM(amount) AS revenue
FROM orders
GROUP BY yr, mth
ORDER BY yr, mth;
```
**Output:**

| yr | mth | revenue |
|---|---|---|
| 2025 | 01 | 1500 |
| 2025 | 02 | 1200 |
| 2025 | 04 | 300 |
| 2025 | 07 | 400 |
| 2025 | 10 | 800 |
| 2026 | 01 | 800 |
**pandas equivalent:** (run; result identical to the Output above)
```python
g = orders.assign(yr=orders['order_date'].dt.strftime('%Y'), mth=orders['order_date'].dt.strftime('%m'))
res = g.groupby(['yr', 'mth'], as_index=False).agg(revenue=('amount', 'sum')).sort_values(['yr', 'mth']).reset_index(drop=True)
```
**Edge cases:** Months with no orders do not appear; to show zeros join to a calendar table. SQLite and PostgreSQL let you use the alias in GROUP BY; SQL Server does not (repeat the expression). NULL dates form their own group.
**Likely follow-ups:** Q: Why zero-padded month? A: So '10' sorts after '09', not after '1'. Q: Month names? A: MONTHNAME()/TO_CHAR; sort by the number, not the name.
**Common mistakes:** Grouping by month number only; sorting month names alphabetically (April before January).

### Q33 ⭐⭐ 🟡 Given orders(order_id, customer_id, category, amount, order_date), find customers who ordered in at least 2 different months.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you use COUNT(DISTINCT) with HAVING and handle the year trap?
**Say this in the interview:** I group by customer, count the distinct year-month values, and keep customers with at least 2. I count 'YYYY-MM', not just the month number, because January 2025 and January 2026 are different months.
**Explain simply:**
- COUNT(DISTINCT x) counts unique values only, so two orders on the same day or in the same month count as one month.
- The question says 'different months'. I read that as different calendar months including the year, and say so out loud to the interviewer.
- HAVING filters after counting.
**Example:** Customer C1 ordered in Jan 2025 and Jan 2026 (two months); C4 has one order in Jan 2026 only (one month).
**Sample data:**
**orders** (8 rows)

| order_id | customer_id | category | amount | order_date |
|---|---|---|---|---|
| 1 | C1 | Laptop | 1000 | 2025-01-05 |
| 2 | C1 | Phone | 500 | 2025-01-05 |
| 3 | C2 | Laptop | 1200 | 2025-02-10 |
| 4 | C2 | Phone | 300 | 2025-04-15 |
| 5 | C3 | Tablet | 400 | 2025-07-01 |
| 6 | C3 | Laptop | 800 | 2025-10-12 |
| 7 | C4 | Phone | 600 | 2026-01-08 |
| 8 | C1 | Tablet | 200 | 2026-01-08 |
**SQL:**
```sql
SELECT customer_id,
       COUNT(DISTINCT strftime('%Y-%m', order_date)) AS active_months
FROM orders
GROUP BY customer_id
HAVING COUNT(DISTINCT strftime('%Y-%m', order_date)) >= 2
ORDER BY customer_id;
```
**Output:**

| customer_id | active_months |
|---|---|
| C1 | 2 |
| C2 | 2 |
| C3 | 2 |
**pandas equivalent:** (run; result identical to the Output above)
```python
o = orders.assign(ym=orders['order_date'].dt.strftime('%Y-%m'))
g = o.groupby('customer_id', as_index=False).agg(active_months=('ym', 'nunique'))
res = g[g['active_months'] >= 2].sort_values('customer_id').reset_index(drop=True)
```
**Edge cases:** Ambiguity: if the interviewer means month-of-year ignoring year, C1 would have only 1 distinct month number (01), as this wrong-version count shows:

| customer_id | month_numbers |
|---|---|
| C1 | 1 |
| C2 | 2 |
| C3 | 2 |
| C4 | 1 |

NULL dates are ignored by COUNT(DISTINCT).
**Likely follow-ups:** Q: Consecutive months? A: Needs window functions (LAG) or a date-difference trick. Q: At least 2 orders? A: COUNT(*) >= 2 instead.
**Common mistakes:** Counting months by number only; using COUNT(*) which counts orders, not months.

### Q34 ⭐⭐ 🟡 Given employees(emp_id, name, dept, salary, hire_date, status) plus a gender column, find the average salary by department and gender, showing only groups with at least 10 employees.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you group by two columns and drop small groups with HAVING?
**Say this in the interview:** I group by department and gender, calculate AVG(salary) and COUNT(*), and use HAVING COUNT(*) >= 10 to hide groups too small to be reliable or to protect privacy. My sample is tiny, so I demonstrate with >= 2.
**Explain simply:**
- GROUP BY dept, gender creates one group per combination.
- HAVING COUNT(*) >= 10 removes groups with fewer than 10 people: small groups give noisy averages and can identify individuals.
- The sample has only 8 employees, so the demo uses 2; the production threshold would be 10.
**Example:** IT men average 92,500 over 2 people; the HR women group (1 person) is hidden because it is below the threshold.
**Sample data:**
The question mentions a `gender` column, which I add to the sample.

| emp_id | name | dept | gender | salary |
|---|---|---|---|---|
| 1 | Asha | HR | F | 45000 |
| 2 | Ravi | HR | M | 52000 |
| 3 | Ravi K | HR | M | 50000 |
| 4 | Karan | IT | M | 75000 |
| 5 | Sunil | IT | M | 110000 |
| 6 | Priya | Sales | F | 40000 |
| 7 | Neha | Sales | F | 38000 |
| 8 | Omar | Finance | M | 60000 |
**SQL:**
```sql
SELECT dept, gender,
       COUNT(*) AS headcount,
       ROUND(AVG(salary), 2) AS avg_salary
FROM employees
GROUP BY dept, gender
HAVING COUNT(*) >= 2
ORDER BY dept, gender;
```
**Output:**

| dept | gender | headcount | avg_salary |
|---|---|---|---|
| HR | M | 2 | 51000 |
| IT | M | 2 | 92500 |
| Sales | F | 2 | 39000 |
SQL as run uses `>= 2`; for the real question change it to `HAVING COUNT(*) >= 10`.
**pandas equivalent:** (run; result identical to the Output above)
```python
g = emp.groupby(['dept', 'gender'], as_index=False).agg(headcount=('emp_id', 'count'), avg_salary=('salary', 'mean'))
g['avg_salary'] = g['avg_salary'].round(2)
res = g[g['headcount'] >= 2].sort_values(['dept', 'gender']).reset_index(drop=True)
```
**Edge cases:** NULL gender forms its own group. Groups below the threshold disappear, so totals will not add to the company. Small-group suppression is also a data privacy practice.
**Likely follow-ups:** Q: Pay gap % between genders? A: Pivot the two averages into columns with conditional aggregation and compute the difference. Q: Why not WHERE? A: Group size is only known after grouping.
**Common mistakes:** Using WHERE COUNT(*) >= 10; averaging averages; forgetting that a group missing from the output means it was too small, not missing data.

### Q35 ⭐⭐ 🟡 Why is taking the average of department averages not the same as the company average? Show with a small numeric example.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand weighted averages and why averaging unequal groups misleads?
**Say this in the interview:** The average of department averages gives every department equal weight, even if one has 2 people and another 200. The company average weights each person equally, so a big department pulls it harder. To get it from the department averages you must weight by headcount.
**Explain simply:**
- Company average = total salary / total people.
- Average of averages = sum of department averages / number of departments, ignoring headcount.
- They match only when all departments have the same headcount.
- Fix: weighted average = SUM(avg x headcount) / SUM(headcount).
**Example:** Tiny case: dept A has 2 people averaging 100, dept B has 8 averaging 50. Average of averages = 75. Company average = (2x100 + 8x50)/10 = 60.

| dept | headcount | avg_salary |
|---|---|---|
| A | 2 | 100 |
| B | 8 | 50 |
**Sample data:**
**employees** (8 rows)

| emp_id | name | dept | salary | hire_date | status |
|---|---|---|---|---|---|
| 1 | Asha | HR | 45000 | 2020-03-01 | Active |
| 2 | Ravi | HR | 52000 | 2019-07-15 | Left |
| 3 | Ravi K | HR | 50000 | 2021-01-10 | Active |
| 4 | Karan | IT | 75000 | 2020-09-01 | Left |
| 5 | Sunil | IT | 110000 | 2017-02-11 | Active |
| 6 | Priya | Sales | 40000 | 2022-04-04 | Active |
| 7 | Neha | Sales | 38000 | 2023-01-09 | Left |
| 8 | Omar | Finance | 60000 | 2019-11-30 | Active |
**SQL:**
```sql
WITH d AS (
  SELECT dept, COUNT(*) AS n, AVG(salary) AS dept_avg
  FROM employees
  GROUP BY dept
)
SELECT ROUND((SELECT AVG(dept_avg) FROM d), 2) AS avg_of_dept_avgs,
       ROUND((SELECT AVG(salary) FROM employees), 2) AS company_avg,
       ROUND((SELECT SUM(dept_avg * n) / SUM(n) FROM d), 2) AS weighted_avg;
```
**Output:**

| avg_of_dept_avgs | company_avg | weighted_avg |
|---|---|---|
| 60125 | 58750 | 58750 |
**pandas equivalent:** (run; result identical to the Output above)
```python
g = emp.groupby('dept').agg(n=('salary', 'size'), dept_avg=('salary', 'mean'))
res = pd.DataFrame({'avg_of_dept_avgs': [round(g['dept_avg'].mean(), 2)], 'company_avg': [round(emp['salary'].mean(), 2)],
                    'weighted_avg': [round((g['dept_avg'] * g['n']).sum() / g['n'].sum(), 2)]})
```
**Edge cases:** Equal headcounts make both equal. NULL salaries: AVG skips them, so the weight must be COUNT(salary), not COUNT(*). Same issue applies to rates, e.g. averaging attrition percentages.
**Likely follow-ups:** Q: Which is right for reporting? A: Depends on the question: 'typical department' vs 'typical employee'. Q: Same for percentages? A: Yes, aggregate the numerator and denominator, then divide.
**Common mistakes:** Averaging percentages or averages from groups of different sizes and reporting it as the company figure.

### Q36 ⭐⭐ 🟡 Given orders(order_id, customer_id, category, amount, order_date), show each category's percentage contribution to total sales.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you compute a share of total using a subquery or a window function?
**Say this in the interview:** I sum sales per category and divide by the grand total, which I get from a subquery over the whole table, then multiply by 100.0 for a percentage.
**Explain simply:**
- Percent of total = category sales / all sales x 100.
- The grand total needs a separate calculation: a scalar subquery `(SELECT SUM(amount) FROM orders)`, or a window function `SUM(SUM(amount)) OVER ()`.
- Using 100.0 avoids integer division.
**Example:** Laptop sold 3,000 of 5,000 total, which is 60%.
**Sample data:**
**orders** (8 rows)

| order_id | customer_id | category | amount | order_date |
|---|---|---|---|---|
| 1 | C1 | Laptop | 1000 | 2025-01-05 |
| 2 | C1 | Phone | 500 | 2025-01-05 |
| 3 | C2 | Laptop | 1200 | 2025-02-10 |
| 4 | C2 | Phone | 300 | 2025-04-15 |
| 5 | C3 | Tablet | 400 | 2025-07-01 |
| 6 | C3 | Laptop | 800 | 2025-10-12 |
| 7 | C4 | Phone | 600 | 2026-01-08 |
| 8 | C1 | Tablet | 200 | 2026-01-08 |
**SQL:**
```sql
SELECT category,
       SUM(amount) AS sales,
       ROUND(100.0 * SUM(amount) / (SELECT SUM(amount) FROM orders), 2) AS pct_of_total
FROM orders
GROUP BY category
ORDER BY sales DESC;
```
**Output:**

| category | sales | pct_of_total |
|---|---|---|
| Laptop | 3000 | 60 |
| Phone | 1400 | 28 |
| Tablet | 600 | 12 |
**pandas equivalent:** (run; result identical to the Output above)
```python
g = orders.groupby('category', as_index=False).agg(sales=('amount', 'sum'))
g['pct_of_total'] = (100.0 * g['sales'] / g['sales'].sum()).round(2)
res = g.sort_values('sales', ascending=False).reset_index(drop=True)
```
**Edge cases:** Percentages can sum to 99.99 or 100.01 because of rounding. If the grand total is 0 or NULL you get NULL or an error: use NULLIF. A WHERE filter in the outer query does not change the subquery total unless repeated inside.
**Likely follow-ups:** Q: Window version? A: Same result, run here:

| category | sales | pct_of_total |
|---|---|---|
| Laptop | 3000 | 60 |
| Phone | 1400 | 28 |
| Tablet | 600 | 12 |

Q: Percent within customer? A: PARTITION BY customer_id in the window.
**Common mistakes:** Integer division giving 0; dividing by COUNT instead of SUM.

### Q37 ⭐⭐ 🟡 You join orders to order_items and then SUM(order amount); the total looks inflated. What is row duplication (fan-out) after a join and how do you fix it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know that a one-to-many join multiplies rows, and can you fix it by aggregating first?
**Say this in the interview:** When I join orders to order_items, an order with 3 items becomes 3 rows, so its amount is repeated 3 times and SUM inflates. This is fan-out. The fix is to aggregate the many-side to one row per order before joining, or to sum from the orders table alone.
**Explain simply:**
- One-to-many join: one order matches many item rows.
- Every item row carries a copy of the order-level amount, so SUM(o.amount) counts it once per item.
- Fix 1: pre-aggregate items to one row per order (CTE), then join.
- Fix 2: sum order amounts from `orders` only, using EXISTS to filter, if you do not need item columns.
- Avoid `SUM(DISTINCT amount)`: two different orders with the same amount would collapse.
**Example:** Order 101 is 1,000 with 3 items. The true revenue is 1,000 + 500 + 300 = 1,800. A naive join gives 3x1000 + 2x500 + 300 = 4,300.
**Sample data:**
**orders**

| order_id | customer_id | amount |
|---|---|---|
| 101 | C1 | 1000 |
| 102 | C2 | 500 |
| 103 | C3 | 300 |

**order_items**

| item_id | order_id | product | line_qty |
|---|---|---|---|
| 1 | 101 | Laptop | 1 |
| 2 | 101 | Mouse | 2 |
| 3 | 101 | Bag | 1 |
| 4 | 102 | Phone | 1 |
| 5 | 102 | Case | 1 |
| 6 | 103 | Tablet | 1 |
**SQL:**
```sql
WITH items AS (
  SELECT order_id, COUNT(*) AS item_rows, SUM(line_qty) AS units
  FROM order_items
  GROUP BY order_id
)
SELECT SUM(o.amount) AS total_revenue,
       SUM(i.units)  AS total_units
FROM orders o
JOIN items i ON i.order_id = o.order_id;
```
**Output:**

| total_revenue | total_units |
|---|---|
| 1800 | 7 |
**pandas equivalent:** (run; result identical to the Output above)
```python
items = (pd.DataFrame({'order_id': [101,101,101,102,102,103], 'line_qty': [1,2,1,1,1,1]})
         .groupby('order_id', as_index=False).agg(units=('line_qty', 'sum')))
ords = pd.DataFrame({'order_id': [101,102,103], 'amount': [1000,500,300]})
m = ords.merge(items, on='order_id')
res = pd.DataFrame({'total_revenue': [m['amount'].sum()], 'total_units': [m['units'].sum()]})
```
**Edge cases:** Naive join total (wrong):

| total_revenue |
|---|
| 4300 |

An inner join drops orders with no items; use LEFT JOIN if those orders still count. Row-count check: after any join, compare COUNT(*) to the expected number of rows. In pandas, `validate='one_to_one'` in `merge` raises an error when the key is duplicated.
**Likely follow-ups:** Q: How do I detect fan-out? A: Compare row counts before and after the join and check whether the join key is unique on each side. Q: Many-to-many? A: Worse, rows multiply both ways; aggregate both sides first.
**Common mistakes:** Using SUM(DISTINCT); using GROUP BY to hide the problem; not checking row counts after a join.

### Q38 ⭐⭐ 🟡 Given orders(order_id, customer_id, category, amount, order_date), count orders per day and show only days with more than 100 orders, newest first.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you combine GROUP BY, HAVING and ORDER BY in the right order?
**Say this in the interview:** I group by the order date, count rows, keep groups above the threshold with HAVING, and sort newest first with ORDER BY order_date DESC. With only 8 sample rows I demo with more than 1; on real data it is more than 100.
**Explain simply:**
- Execution order: FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY.
- HAVING filters groups after counting; WHERE filters rows before.
- If order_date also has a time part (a timestamp), group by the date only: `DATE(order_date)` in MySQL, `order_date::date` in PostgreSQL, `CAST(order_date AS DATE)` in SQL Server (not run here).
**Example:** A busy-day report: which days did the warehouse handle 100+ orders? On 2025-01-05 there were 2 orders, as on 2026-01-08.
**Sample data:**
**orders** (8 rows)

| order_id | customer_id | category | amount | order_date |
|---|---|---|---|---|
| 1 | C1 | Laptop | 1000 | 2025-01-05 |
| 2 | C1 | Phone | 500 | 2025-01-05 |
| 3 | C2 | Laptop | 1200 | 2025-02-10 |
| 4 | C2 | Phone | 300 | 2025-04-15 |
| 5 | C3 | Tablet | 400 | 2025-07-01 |
| 6 | C3 | Laptop | 800 | 2025-10-12 |
| 7 | C4 | Phone | 600 | 2026-01-08 |
| 8 | C1 | Tablet | 200 | 2026-01-08 |
**SQL:**
```sql
SELECT order_date, COUNT(*) AS orders_cnt
FROM orders
GROUP BY order_date
HAVING COUNT(*) > 1   -- use > 100 on real data
ORDER BY order_date DESC;
```
**Output:**

| order_date | orders_cnt |
|---|---|
| 2026-01-08 | 2 |
| 2025-01-05 | 2 |
As run: threshold `> 1`. Real question: `HAVING COUNT(*) > 100`.
**pandas equivalent:** (run; result identical to the Output above)
```python
g = orders.groupby('order_date', as_index=False).agg(orders_cnt=('order_id', 'count'))
res = g[g['orders_cnt'] > 1].sort_values('order_date', ascending=False).reset_index(drop=True)
res['order_date'] = res['order_date'].dt.strftime('%Y-%m-%d')
```
**Edge cases:** Timestamps make every row its own group if you do not cut to date. NULL dates form a group; exclude them if needed. Ties in count do not matter because the sort is by date.
**Likely follow-ups:** Q: Top 5 busiest days? A: ORDER BY orders_cnt DESC LIMIT 5. Q: Why not WHERE COUNT(*) > 100? A: WHERE runs before grouping.
**Common mistakes:** Using WHERE for the count; sorting ascending by mistake; grouping by a timestamp.

### Q39 ⭐⭐ 🔴 Given orders(order_id, customer_id, category, amount, order_date), find customers whose total spend is above the average total spend of all customers (aggregate of an aggregate).

**Asked at:** Zillow-style 'above the national average' questions appear on StrataScratch (product); GROUP BY threshold questions are common in guides. No company-specific report for this exact wording found.

**What the interviewer is checking:** Can you aggregate twice: first total per customer, then compare each total with the average of those totals?

**Say this in the interview:** First I add up each customer's spend in a CTE. A CTE is just a named temporary result I can reuse. Then I keep customers whose total is greater than the average of those totals.

**Explain simply:**
- An aggregate of an aggregate means two levels: level 1 is SUM per customer, level 2 is AVG over those sums.
- SQL will not let you write AVG(SUM(amount)) in one plain SELECT, so you use a CTE or subquery for level 1.
- The average of customer totals is not the same as the average order amount. Pick the one the question asks for.

**Example:** HR version: total overtime hours per employee, then find employees above the average overtime total. Here the five customers spend 1100, 1500, 550, 900 and 450; the average total is 900, so C1 and C2 qualify (C4 equals 900 and is not strictly above).

**Sample data:** `orders`

| order_id | customer_id | category | amount | order_date |
|---|---|---|---|---|
| 1 | C1 | Books | 300 | 2025-01-01 |
| 2 | C1 | Books | 800 | 2025-01-02 |
| 3 | C2 | Toys | 600 | 2025-01-03 |
| 4 | C2 | Toys | 900 | 2025-01-08 |
| 5 | C3 | Books | 550 | 2025-01-09 |
| 6 | C4 | Games | 200 | 2025-01-10 |
| 7 | C4 | Games | 700 | 2025-01-15 |
| 8 | C5 | Garden | 450 | 2025-01-16 |

**SQL:**
```sql
WITH cust AS (
  SELECT customer_id, SUM(amount) AS total_spend
  FROM orders
  GROUP BY customer_id
)
SELECT customer_id, total_spend
FROM cust
WHERE total_spend > (SELECT AVG(total_spend) FROM cust)
ORDER BY total_spend DESC;
```

**Output:**

| customer_id | total_spend |
|---|---|
| C2 | 1500 |
| C1 | 1100 |

**pandas equivalent:**
```python
totals = orders.groupby('customer_id', as_index=False)['amount'].sum().rename(columns={'amount': 'total_spend'})
result = totals[totals.total_spend > totals.total_spend.mean()].sort_values('total_spend', ascending=False)
print(result.to_string(index=False))
```
Output:
```text
customer_id  total_spend
         C2         1500
         C1         1100
```

**Edge cases:** Customers with no orders are not in the average (they have no rows). If you want them counted as zero, start from a customers table with LEFT JOIN. Use strict > so ties at the average are excluded. NULL amounts are ignored by SUM.

**Likely follow-ups:** Q: Show how far above average? A: add total_spend - (SELECT AVG(total_spend) FROM cust) as a column. Q: Without a CTE? A: use a subquery in FROM, or HAVING SUM(amount) > (subquery) directly.

**Common mistakes:** Writing HAVING SUM(amount) > AVG(SUM(amount)) (not valid in most databases); averaging raw order rows instead of customer totals; using >= and keeping the average customer.

### Q40 ⭐⭐ 🔴 Given employees(emp_id, name, dept, salary, hire_date, status), find the average number of employees per department (average of the group counts).

**Asked at:** Gap-fill question (author judgment of standard analyst SQL); no company-specific report found.

**What the interviewer is checking:** Do you know you must count per group first and then average those counts, in two steps?

**Say this in the interview:** I count employees per department in a subquery, then take the average of those counts in the outer query.

**Explain simply:**
- Inner query: GROUP BY dept with COUNT(*) gives headcount per department.
- Outer query: AVG over those counts gives average headcount per department.
- Shortcut check: total employees divided by number of departments gives the same number, since both come from the same rows.

**Example:** 8 employees across 3 departments (HR 3, IT 3, Sales 2): 8 / 3 = 2.67 employees per department on average.

**Sample data:** `employees`

| emp_id | name | dept | salary | hire_date | status | gender |
|---|---|---|---|---|---|---|
| 1 | Asha | HR | 40000 | 2022-03-01 | Active | F |
| 2 | Bala | HR | 40000 | 2023-06-15 | Active | M |
| 3 | Chitra | HR | 60000 | 2021-01-10 | Left | F |
| 4 | Esha | IT | 70000 | 2022-08-01 | Active | F |
| 5 | Farid | IT | 90000 | 2020-02-20 | Active | M |
| 6 | Gita | IT | 90000 | 2021-09-05 | Left | F |
| 7 | Jai | Sales | 30000 | 2024-01-08 | Active | M |
| 8 | Kiran | Sales | 45000 | 2023-04-12 | Left | F |

**SQL:**
```sql
SELECT ROUND(AVG(headcount * 1.0), 2) AS avg_employees_per_dept
FROM (
  SELECT dept, COUNT(*) AS headcount
  FROM employees
  GROUP BY dept
) AS d;
```

**Output:**

| avg_employees_per_dept |
|---|
| 2.67 |

**pandas equivalent:**
```python
counts = employees.groupby('dept').size()
print(round(counts.mean(), 2))
```
Output:
```text
2.67
```

**Edge cases:** In SQL Server and some others, AVG of an integer column returns an integer (rounds down), hence the * 1.0. Departments with zero employees are missing unless you start from a departments table. Decide whether to count only status = 'Active' people.

**Likely follow-ups:** Q: Why not AVG(COUNT(*))? A: Nested aggregates are not allowed in a single level in standard SQL (PostgreSQL rejects it). Q: Count only active staff? A: add WHERE status = 'Active' inside the subquery.

**Common mistakes:** Averaging the salary or id column by mistake; forgetting integer division; leaving out empty departments without saying so.

### Q41 ⭐ 🟢 Is GROUP BY 1 (position number) allowed? What are the pros and cons compared with naming the column?

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Do you know the shortcut, and do you know why many teams avoid it in production code?

**Say this in the interview:** Yes, in most databases GROUP BY 1 means group by the first column in the SELECT list. It is quick for ad-hoc work, but I name the columns in shared code because adding a column can silently change the grouping.

**Explain simply:**
- GROUP BY 1 (and ORDER BY 1) refer to the position of a column in the SELECT list, not to a column called 1.
- Works in PostgreSQL, MySQL, SQLite, DuckDB, BigQuery and Snowflake. SQL Server does not accept it in GROUP BY (it allows positions in ORDER BY). Not run here for SQL Server.
- Pro: short, handy when the group expression is long, like GROUP BY 1 for a DATE_TRUNC(...) expression.
- Con: if someone reorders the SELECT list, the query still runs but groups by something else. Harder to read and review.

**Example:** SELECT dept, COUNT(*) ... GROUP BY 1 groups by dept. If someone later puts hire_year first, GROUP BY 1 now groups by year and nothing errors.

**Sample data:** `employees`

| emp_id | name | dept | salary | hire_date | status | gender |
|---|---|---|---|---|---|---|
| 1 | Asha | HR | 40000 | 2022-03-01 | Active | F |
| 2 | Bala | HR | 40000 | 2023-06-15 | Active | M |
| 3 | Chitra | HR | 60000 | 2021-01-10 | Left | F |
| 4 | Esha | IT | 70000 | 2022-08-01 | Active | F |
| 5 | Farid | IT | 90000 | 2020-02-20 | Active | M |
| 6 | Gita | IT | 90000 | 2021-09-05 | Left | F |
| 7 | Jai | Sales | 30000 | 2024-01-08 | Active | M |
| 8 | Kiran | Sales | 45000 | 2023-04-12 | Left | F |

**SQL:**
```sql
SELECT dept, COUNT(*) AS headcount
FROM employees
GROUP BY 1
ORDER BY 1;
```

**Output:**

| dept | headcount |
|---|---|
| HR | 3 |
| IT | 3 |
| Sales | 2 |

**Edge cases:** Position numbers start at 1 and must be within the SELECT list; GROUP BY 0 or 9 raises an error. A literal number in WHERE is different: WHERE 1 = 1 is just a constant.

**Likely follow-ups:** Q: Can you use column aliases in GROUP BY instead? A: Yes in MySQL, PostgreSQL, DuckDB and BigQuery; not in SQL Server or Oracle. Q: Is it standard SQL? A: Positional GROUP BY is not in the standard, it is a vendor convenience.

**Common mistakes:** Thinking GROUP BY 1 means the first column of the table (it is the first column of the SELECT list); mixing it into production queries that get edited often.

### Q42 ⭐ 🟢 What is the difference between COUNT(1) and COUNT(*)? Is one faster?

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Whether you understand what COUNT counts, and can bust the 'COUNT(1) is faster' myth.

**Say this in the interview:** They give the same answer: both count rows. The 1 is just a constant, not a column position. Modern databases treat them the same, so I use COUNT(*) because it reads as 'count rows'.

**Explain simply:**
- COUNT(*) counts every row in the group, whatever it contains.
- COUNT(1) counts rows where the expression 1 is not NULL, which is every row. Same result.
- COUNT(column) is different: it skips rows where that column is NULL.
- Speed: no meaningful difference in PostgreSQL, MySQL, SQL Server or Oracle. Optimisers treat them as equivalent. COUNT(*) is the standard form.

**Example:** A table of 4 employees where 1 has no manager recorded: COUNT(*) = 4, COUNT(1) = 4, COUNT(manager) = 3.

**SQL:**
```sql
WITH emp AS (
  SELECT * FROM (VALUES (1, 'Asha', NULL), (2, 'Bala', 'Asha'), (3, 'Chitra', 'Asha'), (4, 'Esha', 'Bala'))
  AS t(emp_id, name, manager)
)
SELECT COUNT(*) AS count_star,
       COUNT(1) AS count_one,
       COUNT(manager) AS count_manager,
       COUNT(DISTINCT manager) AS count_distinct_manager
FROM emp;
```

**Output:**

| count_star | count_one | count_manager | count_distinct_manager |
|---|---|---|---|
| 4 | 4 | 3 | 2 |

**Edge cases:** NULLs only matter for COUNT(column). An empty table: COUNT(*) and COUNT(1) return 0 (one row, value 0); with GROUP BY and no rows you get no rows at all.

**Likely follow-ups:** Q: Does COUNT(*) read all columns? A: No, the engine only needs to know a row exists, it may use the smallest index. Q: COUNT(DISTINCT col)? A: counts unique non-NULL values.

**Common mistakes:** Believing COUNT(1) is faster or that the 1 means the first column; assuming COUNT(col) counts NULL rows.

### Q43 ⭐ 🟢 Can MIN and MAX be used on text? What does MAX('Apple','Banana') style comparison return?

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Do you know aggregates work on any sortable type, and do you spot that MAX('Apple','Banana') is not an aggregate call?

**Say this in the interview:** Yes, MIN and MAX work on text using alphabetical order. Note MAX('Apple','Banana') with two arguments is not an aggregate: in MySQL and PostgreSQL the scalar function is GREATEST, in SQLite MAX(a, b) works as a scalar.

**Explain simply:**
- Aggregate MIN/MAX take a column and return one value for the group. Text is compared by the database collation (sort rules).
- 'Banana' > 'Apple', so MAX over those two rows is 'Banana' and MIN is 'Apple'.
- Case and accents depend on the collation: in binary order, 'apple' sorts after 'Banana' (lowercase letters come after uppercase). MySQL and SQL Server default collations ignore case.
- Numbers stored as text compare character by character, so '9' is greater than '10'.

**Example:** MAX(name) over employee names returns the alphabetically last name, e.g. 'Kiran'. A text column with employee codes 'E9' and 'E10' gives MAX = 'E9', which surprises people.

**Sample data:** `employees`

| emp_id | name | dept | salary | hire_date | status | gender |
|---|---|---|---|---|---|---|
| 1 | Asha | HR | 40000 | 2022-03-01 | Active | F |
| 2 | Bala | HR | 40000 | 2023-06-15 | Active | M |
| 3 | Chitra | HR | 60000 | 2021-01-10 | Left | F |
| 4 | Esha | IT | 70000 | 2022-08-01 | Active | F |
| 5 | Farid | IT | 90000 | 2020-02-20 | Active | M |
| 6 | Gita | IT | 90000 | 2021-09-05 | Left | F |
| 7 | Jai | Sales | 30000 | 2024-01-08 | Active | M |
| 8 | Kiran | Sales | 45000 | 2023-04-12 | Left | F |

**SQL:**
```sql
SELECT MIN(name) AS first_name, MAX(name) AS last_name FROM employees;

SELECT GREATEST('Apple', 'Banana') AS bigger,
       (SELECT MAX(x) FROM (VALUES ('9'), ('10')) AS t(x)) AS max_of_text_numbers,
       (SELECT MAX(x) FROM (VALUES ('apple'), ('Banana')) AS t(x)) AS binary_case_demo;
```

**Output:**

Aggregate over a column:

| first_name | last_name |
|---|---|
| Asha | Kiran |

Scalar GREATEST and text-number trap (DuckDB, binary collation):

| bigger | max_of_text_numbers | binary_case_demo |
|---|---|---|
| Banana | 9 | apple |

**Edge cases:** NULLs are ignored by MIN/MAX. GREATEST in PostgreSQL ignores NULL arguments but in MySQL returns NULL if any argument is NULL. SQL Server has no GREATEST before 2022.

**Likely follow-ups:** Q: Can I use MAX on dates? A: Yes, latest date. Q: Longest text? A: use MAX(LENGTH(col)) or ORDER BY LENGTH(col) DESC LIMIT 1.

**Common mistakes:** Expecting MAX on text to return the longest string; storing numbers as text and getting '9' > '10'; forgetting collation changes case ordering.

### Q44 ⭐ 🟡 What are GROUP BY extensions in SQL (ROLLUP, CUBE, GROUPING SETS)? Which databases support them?

**Asked at:** Commonly asked (no company-specific report found); a GROUP BY extensions question appears in one learnsql.com GROUP BY guide.

**What the interviewer is checking:** Do you know there are ways to get several levels of totals in one query instead of stacking UNION ALLs?

**Say this in the interview:** ROLLUP gives a hierarchy of subtotals ending in a grand total. CUBE gives subtotals for every combination. GROUPING SETS lets me list exactly which groupings I want.

**Explain simply:**
- ROLLUP(a, b): groups by (a,b), then (a), then () the grand total. Good for hierarchies like country then city.
- CUBE(a, b): every combination: (a,b), (a), (b), (). Good for cross-tab style totals.
- GROUPING SETS: you list the exact combinations, the other two are shortcuts for it.
- Support: PostgreSQL (9.5+), SQL Server, Oracle, DuckDB, Snowflake and BigQuery support ROLLUP, CUBE and GROUPING SETS. MySQL only has GROUP BY a, b WITH ROLLUP (no CUBE, no GROUPING SETS). SQLite supports none. Check your version's docs.
- The result shows NULL in the rolled-up columns, so use GROUPING() to tell a subtotal NULL from a real NULL.

**Example:** HR headcount by department and status (Active/Left): CUBE returns department x status rows, a total per department, a total per status, and the company total.

**Sample data:** `employees`

| emp_id | name | dept | salary | hire_date | status | gender |
|---|---|---|---|---|---|---|
| 1 | Asha | HR | 40000 | 2022-03-01 | Active | F |
| 2 | Bala | HR | 40000 | 2023-06-15 | Active | M |
| 3 | Chitra | HR | 60000 | 2021-01-10 | Left | F |
| 4 | Esha | IT | 70000 | 2022-08-01 | Active | F |
| 5 | Farid | IT | 90000 | 2020-02-20 | Active | M |
| 6 | Gita | IT | 90000 | 2021-09-05 | Left | F |
| 7 | Jai | Sales | 30000 | 2024-01-08 | Active | M |
| 8 | Kiran | Sales | 45000 | 2023-04-12 | Left | F |

**SQL:**
```sql
SELECT dept, status, COUNT(*) AS headcount,
       GROUPING(dept) AS g_dept, GROUPING(status) AS g_status
FROM employees
GROUP BY CUBE (dept, status)
ORDER BY g_dept, g_status, dept, status;
```

**Output:**

| dept | status | headcount | g_dept | g_status |
|---|---|---|---|---|
| HR | Active | 2 | 0 | 0 |
| HR | Left | 1 | 0 | 0 |
| IT | Active | 2 | 0 | 0 |
| IT | Left | 1 | 0 | 0 |
| Sales | Active | 1 | 0 | 0 |
| Sales | Left | 1 | 0 | 0 |
| HR | NULL | 3 | 0 | 1 |
| IT | NULL | 3 | 0 | 1 |
| Sales | NULL | 2 | 0 | 1 |
| NULL | Active | 5 | 1 | 0 |
| NULL | Left | 3 | 1 | 0 |
| NULL | NULL | 8 | 1 | 1 |

**Edge cases:** Real NULL values in the grouped columns look like subtotal rows; GROUPING() returns 1 only for subtotal rows. Row count grows fast with CUBE: 2^n combinations.

**Likely follow-ups:** Q: ROLLUP vs CUBE? A: ROLLUP follows the column order (hierarchy), CUBE does all combinations. Q: MySQL alternative? A: WITH ROLLUP or UNION ALL of separate GROUP BYs.

**Common mistakes:** Using CUBE when ROLLUP is enough (extra rows); treating NULL as meaning 'total' without GROUPING(); assuming MySQL supports CUBE.

### Q45 ⭐ 🟡 Given orders(order_id, customer_id, category, amount, order_date), produce sales by category with a subtotal for each category and a grand total using ROLLUP.

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Can you produce detail, subtotal and grand total in one query and label the total rows?

**Say this in the interview:** I use ROLLUP on category and customer. It gives each category-customer row, a subtotal row per category, and a grand total, and I label the total rows with GROUPING().

**Explain simply:**
- With ROLLUP(category) alone you only get one row per category plus a grand total, since the category row is already its own total. To see a real subtotal you need a second level, so I roll up (category, customer_id).
- GROUPING(col) returns 1 when that column was rolled up in this row, which lets me write labels instead of NULL.
- MySQL writes GROUP BY category, customer_id WITH ROLLUP and uses GROUPING() too (8.0+). SQL Server also supports ROLLUP(...).

**Example:** Category Books has two customers (C1 1100, C3 550); the subtotal row says Books 1650. The last row is the grand total, 4500.

**Sample data:** `orders`

| order_id | customer_id | category | amount | order_date |
|---|---|---|---|---|
| 1 | C1 | Books | 300 | 2025-01-01 |
| 2 | C1 | Books | 800 | 2025-01-02 |
| 3 | C2 | Toys | 600 | 2025-01-03 |
| 4 | C2 | Toys | 900 | 2025-01-08 |
| 5 | C3 | Books | 550 | 2025-01-09 |
| 6 | C4 | Games | 200 | 2025-01-10 |
| 7 | C4 | Games | 700 | 2025-01-15 |
| 8 | C5 | Garden | 450 | 2025-01-16 |

**SQL:**
```sql
SELECT
  CASE WHEN GROUPING(category) = 1 THEN 'GRAND TOTAL' ELSE category END AS category,
  CASE WHEN GROUPING(category) = 1 THEN ''
       WHEN GROUPING(customer_id) = 1 THEN 'Subtotal'
       ELSE customer_id END AS customer_id,
  SUM(amount) AS sales
FROM orders
GROUP BY ROLLUP (category, customer_id)
ORDER BY GROUPING(category), category, GROUPING(customer_id), customer_id;
```

**Output:**

| category | customer_id | sales |
|---|---|---|
| Books | C1 | 1100 |
| Books | C3 | 550 |
| Books | Subtotal | 1650 |
| Games | C4 | 900 |
| Games | Subtotal | 900 |
| Garden | C5 | 450 |
| Garden | Subtotal | 450 |
| Toys | C2 | 1500 |
| Toys | Subtotal | 1500 |
| GRAND TOTAL |  | 4500 |

**pandas equivalent:**
```python
d = orders.groupby(['category', 'customer_id'], as_index=False)['amount'].sum().assign(lvl=0)
s = orders.groupby('category', as_index=False)['amount'].sum().assign(customer_id='Subtotal', lvl=1)
g = pd.DataFrame({'category': ['GRAND TOTAL'], 'customer_id': [''], 'amount': [orders.amount.sum()], 'lvl': [2]})
r = pd.concat([d, s, g], ignore_index=True)
r['grand'] = r.category.eq('GRAND TOTAL')
r['sub'] = r.customer_id.eq('Subtotal')
r = r.sort_values(['grand', 'category', 'sub', 'customer_id'])
r = r[['category', 'customer_id', 'amount']].rename(columns={'amount': 'sales'})
print(r.to_string(index=False))
```
Output:
```text
   category customer_id  sales
      Books          C1   1100
      Books          C3    550
      Books    Subtotal   1650
      Games          C4    900
      Games    Subtotal    900
     Garden          C5    450
     Garden    Subtotal    450
       Toys          C2   1500
       Toys    Subtotal   1500
GRAND TOTAL               4500
```

**Edge cases:** A real NULL category would look like a subtotal if you use COALESCE; GROUPING() avoids that. The grand total is a row with all grouping columns rolled up. Empty table: ROLLUP still returns the grand total row (NULL sum) in most databases.

**Likely follow-ups:** Q: Only category subtotals, no customer detail? A: GROUP BY ROLLUP(category) is just per category plus total. Q: How to sort total rows last? A: ORDER BY GROUPING(col) as shown.

**Common mistakes:** Using COALESCE(category,'Total') which mislabels real NULLs; reversing the column order in ROLLUP (it changes which subtotals you get); forgetting ROLLUP is not in SQLite.

### Q46 ⭐ 🟡 Can you use HAVING without GROUP BY? What does it mean?

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Do you know HAVING is a filter on groups, and that without GROUP BY the whole table is one group?

**Say this in the interview:** Yes. Without GROUP BY, the whole result is treated as one big group, so HAVING keeps or drops that single summary row.

**Explain simply:**
- Normal: GROUP BY makes many groups, HAVING filters them.
- No GROUP BY: all rows form one group, and the SELECT can only have aggregates (or constants).
- HAVING with a true condition returns one row, with a false condition returns zero rows.
- Works in PostgreSQL, MySQL, SQL Server, Oracle and SQLite. A WHERE condition would not work here because WHERE cannot see SUM().

**Example:** Return the company-wide order total only if it exceeds 4000. Our total is 4500, so a row comes back. Change the threshold to 5000 and you get nothing.

**Sample data:** `orders`

| order_id | customer_id | category | amount | order_date |
|---|---|---|---|---|
| 1 | C1 | Books | 300 | 2025-01-01 |
| 2 | C1 | Books | 800 | 2025-01-02 |
| 3 | C2 | Toys | 600 | 2025-01-03 |
| 4 | C2 | Toys | 900 | 2025-01-08 |
| 5 | C3 | Books | 550 | 2025-01-09 |
| 6 | C4 | Games | 200 | 2025-01-10 |
| 7 | C4 | Games | 700 | 2025-01-15 |
| 8 | C5 | Garden | 450 | 2025-01-16 |

**SQL:**
```sql
SELECT SUM(amount) AS total_sales FROM orders HAVING SUM(amount) > 4000;

SELECT SUM(amount) AS total_sales FROM orders HAVING SUM(amount) > 5000;
```

**Output:**

Threshold 4000 (condition true):

| total_sales |
|---|
| 4500 |

Threshold 5000 (condition false, empty result):

| total_sales |
|---|

**pandas equivalent:**
```python
total = orders.amount.sum()
print(total if total > 4000 else 'no rows')
print(total if total > 5000 else 'no rows')
```
Output:
```text
4500
no rows
```

**Edge cases:** Empty result means the condition was false, not that the table is empty. A non-aggregated column in SELECT with HAVING and no GROUP BY is an error in most databases.

**Likely follow-ups:** Q: Why not WHERE SUM(amount) > 4000? A: WHERE runs before aggregation; aggregates are not allowed there. Q: Is it useful? A: Rarely, for 'alert only if total crosses a limit' checks.

**Common mistakes:** Thinking HAVING needs GROUP BY always; expecting a row with 0 when the condition fails (you get no row).

### Q47 ⭐ 🟡 What is the FILTER clause (PostgreSQL) for aggregates, and how does it compare with CASE WHEN inside the aggregate?

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Do you know conditional aggregation and which syntax works on which database?

**Say this in the interview:** FILTER (WHERE ...) after an aggregate counts or sums only the rows that match. CASE WHEN inside the aggregate does the same and works everywhere.

**Explain simply:**
- FILTER is standard SQL, supported by PostgreSQL 9.4+, SQLite 3.30+ and DuckDB. MySQL and SQL Server do not have it.
- CASE WHEN works in every database: SUM(CASE WHEN status = 'Left' THEN 1 ELSE 0 END), or COUNT(CASE WHEN ... THEN 1 END) because COUNT skips NULL.
- FILTER is shorter and clearer; CASE is more portable and lets you change the value (e.g. weights).
- Result is the same; performance is similar in practice.

**Example:** Attrition by department: headcount and number who left. HR 3 with 1 left, IT 3 with 1 left, Sales 2 with 1 left.

**Sample data:** `employees`

| emp_id | name | dept | salary | hire_date | status | gender |
|---|---|---|---|---|---|---|
| 1 | Asha | HR | 40000 | 2022-03-01 | Active | F |
| 2 | Bala | HR | 40000 | 2023-06-15 | Active | M |
| 3 | Chitra | HR | 60000 | 2021-01-10 | Left | F |
| 4 | Esha | IT | 70000 | 2022-08-01 | Active | F |
| 5 | Farid | IT | 90000 | 2020-02-20 | Active | M |
| 6 | Gita | IT | 90000 | 2021-09-05 | Left | F |
| 7 | Jai | Sales | 30000 | 2024-01-08 | Active | M |
| 8 | Kiran | Sales | 45000 | 2023-04-12 | Left | F |

**SQL:**
```sql
SELECT dept,
       COUNT(*) AS headcount,
       COUNT(*) FILTER (WHERE status = 'Left') AS left_cnt,
       ROUND(100.0 * COUNT(*) FILTER (WHERE status = 'Left') / COUNT(*), 1) AS attrition_pct
FROM employees
GROUP BY dept
ORDER BY dept;

SELECT dept,
       COUNT(*) AS headcount,
       SUM(CASE WHEN status = 'Left' THEN 1 ELSE 0 END) AS left_cnt,
       ROUND(100.0 * SUM(CASE WHEN status = 'Left' THEN 1 ELSE 0 END) / COUNT(*), 1) AS attrition_pct
FROM employees
GROUP BY dept
ORDER BY dept;
```

**Output:**

FILTER version:

| dept | headcount | left_cnt | attrition_pct |
|---|---|---|---|
| HR | 3 | 1 | 33.3 |
| IT | 3 | 1 | 33.3 |
| Sales | 2 | 1 | 50.0 |

CASE WHEN version (portable):

| dept | headcount | left_cnt | attrition_pct |
|---|---|---|---|
| HR | 3 | 1 | 33.3 |
| IT | 3 | 1 | 33.3 |
| Sales | 2 | 1 | 50.0 |

**pandas equivalent:**
```python
r = employees.groupby('dept').agg(headcount=('emp_id', 'count'), left_cnt=('status', lambda s: (s == 'Left').sum())).reset_index()
r['attrition_pct'] = (100.0 * r.left_cnt / r.headcount).round(1)
print(r.to_string(index=False))
```
Output:
```text
 dept  headcount  left_cnt  attrition_pct
   HR          3         1           33.3
   IT          3         1           33.3
Sales          2         1           50.0
```

**Edge cases:** A group with no matching rows: FILTER with COUNT gives 0, but SUM with FILTER gives NULL (use COALESCE). With CASE and no ELSE, SUM(...) is NULL when nothing matches.

**Likely follow-ups:** Q: Can I FILTER a window function? A: In PostgreSQL yes for aggregate window functions. Q: MySQL equivalent? A: SUM(status = 'Left') works because MySQL treats true as 1.

**Common mistakes:** Using WHERE instead (which drops other rows from every column); forgetting ELSE 0 in SUM(CASE) and getting NULL; using FILTER on MySQL.

### Q48 ⭐ 🟡 What do STDDEV and VARIANCE aggregates tell a business user? Write a query for the standard deviation of order amount by category.

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Can you explain spread in business words, and do you know sample vs population?

**Say this in the interview:** Standard deviation tells how far values typically sit from the average. A big number means orders vary a lot, a small number means they are consistent. Variance is the same thing squared.

**Explain simply:**
- Standard deviation uses the same unit as the data (rupees), so it is easy to explain. Variance is in squared units, mostly used inside formulas.
- STDDEV_SAMP divides by n-1 (use for a sample of a bigger population); STDDEV_POP divides by n (use when you have the whole population). Plain STDDEV is the sample version in PostgreSQL and MySQL treats STDDEV as population.
- SQL Server names: STDEV and STDEVP; VAR and VARP.
- Business use: stable demand has low spread, which makes stock planning easier; wide salary spread within a grade flags pay inequity.

**Example:** Games orders are 200 and 700, so spread is large; Toys are 600 and 900, a similar average but tighter. A category with only one order has no sample standard deviation.

**Sample data:** `orders`

| order_id | customer_id | category | amount | order_date |
|---|---|---|---|---|
| 1 | C1 | Books | 300 | 2025-01-01 |
| 2 | C1 | Books | 800 | 2025-01-02 |
| 3 | C2 | Toys | 600 | 2025-01-03 |
| 4 | C2 | Toys | 900 | 2025-01-08 |
| 5 | C3 | Books | 550 | 2025-01-09 |
| 6 | C4 | Games | 200 | 2025-01-10 |
| 7 | C4 | Games | 700 | 2025-01-15 |
| 8 | C5 | Garden | 450 | 2025-01-16 |

**SQL:**
```sql
SELECT category,
       COUNT(*) AS orders,
       ROUND(AVG(amount), 1) AS avg_amount,
       ROUND(STDDEV_SAMP(amount), 2) AS stddev_samp,
       ROUND(STDDEV_POP(amount), 2) AS stddev_pop
FROM orders
GROUP BY category
ORDER BY category;
```

**Output:**

| category | orders | avg_amount | stddev_samp | stddev_pop |
|---|---|---|---|---|
| Books | 3 | 550.0 | 250.0 | 204.12 |
| Games | 2 | 450.0 | 353.55 | 250.0 |
| Garden | 1 | 450.0 | NULL | 0.0 |
| Toys | 2 | 750.0 | 212.13 | 150.0 |

**pandas equivalent:**
```python
g = orders.groupby('category')['amount']
r = pd.DataFrame({'orders': g.count(), 'avg_amount': g.mean().round(1),
                  'stddev_samp': g.std().round(2), 'stddev_pop': g.std(ddof=0).round(2)}).reset_index()
print(r.to_string(index=False))
```
Output:
```text
category  orders  avg_amount  stddev_samp  stddev_pop
   Books       3       550.0       250.00      204.12
   Games       2       450.0       353.55      250.00
  Garden       1       450.0          NaN        0.00
    Toys       2       750.0       212.13      150.00
```

**Edge cases:** A single-row group gives NULL for sample standard deviation (division by zero) and 0 for population. NULL amounts are ignored. pandas std defaults to sample (ddof=1), NumPy std defaults to population.

**Likely follow-ups:** Q: Why is SD alone not enough? A: Compare with the mean: coefficient of variation = SD / mean. Q: Outliers? A: SD is sensitive to them; consider median and IQR.

**Common mistakes:** Mixing up sample and population versions; assuming STDDEV means the same in all databases; reading variance in rupees.

### Q49 ⭐ 🟡 Given orders(order_id, customer_id, category, amount, order_date), find weekly sales totals using date truncation (DATE_TRUNC / WEEK).

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Do you know how to bucket dates into weeks and that the week start day differs by database?

**Say this in the interview:** I truncate each order date to the start of its week, then group and sum. In PostgreSQL and DuckDB that is DATE_TRUNC('week', order_date), and weeks start on Monday.

**Explain simply:**
- Date truncation snaps a date back to the start of a period, so every date in the same week gets the same label.
- PostgreSQL and DuckDB: DATE_TRUNC('week', d) returns Monday. MySQL: DATE_SUB(d, INTERVAL WEEKDAY(d) DAY) for Monday, or YEARWEEK(d, 1). SQL Server 2022+: DATETRUNC(week, d), but the start day follows SET DATEFIRST. BigQuery: DATE_TRUNC(d, WEEK(MONDAY)).
- SQLite has no DATE_TRUNC; use date(d, 'weekday 0', '-6 days') which gives Monday.
- State your assumption: weeks start Monday (ISO) or Sunday (US).

**Example:** Orders on 1, 2, 3 Jan 2025 (Wed to Fri) fall in the week starting Monday 30 Dec 2024, totalling 300 + 800 + 600 = 1700.

**Sample data:** `orders`

| order_id | customer_id | category | amount | order_date |
|---|---|---|---|---|
| 1 | C1 | Books | 300 | 2025-01-01 |
| 2 | C1 | Books | 800 | 2025-01-02 |
| 3 | C2 | Toys | 600 | 2025-01-03 |
| 4 | C2 | Toys | 900 | 2025-01-08 |
| 5 | C3 | Books | 550 | 2025-01-09 |
| 6 | C4 | Games | 200 | 2025-01-10 |
| 7 | C4 | Games | 700 | 2025-01-15 |
| 8 | C5 | Garden | 450 | 2025-01-16 |

**SQL:**
```sql
SELECT DATE_TRUNC('week', CAST(order_date AS DATE)) AS week_start,
       SUM(amount) AS weekly_sales
FROM orders
GROUP BY 1
ORDER BY 1;

SELECT date(order_date, 'weekday 0', '-6 days') AS week_start,
       SUM(amount) AS weekly_sales
FROM orders
GROUP BY 1
ORDER BY 1;
```

**Output:**

DuckDB / PostgreSQL style (main query):

| week_start | weekly_sales |
|---|---|
| 2024-12-30 | 1700 |
| 2025-01-06 | 1650 |
| 2025-01-13 | 1150 |

SQLite version (run here too):

| week_start | weekly_sales |
|---|---|
| 2024-12-30 | 1700 |
| 2025-01-06 | 1650 |
| 2025-01-13 | 1150 |

**pandas equivalent:**
```python
o = orders.assign(order_date=pd.to_datetime(orders.order_date))
o['week_start'] = o.order_date.dt.to_period('W-SUN').dt.start_time.dt.date
r = o.groupby('week_start', as_index=False)['amount'].sum().rename(columns={'amount': 'weekly_sales'})
print(r.to_string(index=False))
```
Output:
```text
week_start  weekly_sales
2024-12-30          1700
2025-01-06          1650
2025-01-13          1150
```

**Edge cases:** A week that straddles month or year end (30 Dec to 5 Jan) stays one group, which is good for weekly trends but not for monthly totals. Weeks with no orders do not appear; use a calendar table to show zeros. Partial first/last weeks are understated.

**Likely follow-ups:** Q: Why not GROUP BY WEEK(date) number? A: Week numbers repeat each year and differ by definition; use the week-start date. Q: Fill missing weeks? A: LEFT JOIN from a generated calendar.

**Common mistakes:** Grouping by the raw date; assuming Sunday and Monday starts are the same; using week number without the year.

### Q50 ⭐ 🟡 Why do MySQL's ONLY_FULL_GROUP_BY setting and SELECT * with GROUP BY cause errors or unpredictable results?

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Do you understand that every selected column must be grouped or aggregated, and what databases do when it is not?

**Say this in the interview:** ONLY_FULL_GROUP_BY makes MySQL reject a query that selects a column that is neither in GROUP BY nor inside an aggregate, because the value would be ambiguous. SELECT * with GROUP BY breaks that rule for every extra column.

**Explain simply:**
- If I group employees by dept and also select name, there are several names per department. Which one should the database show?
- MySQL 5.7.5+ has ONLY_FULL_GROUP_BY on by default and raises an error. Older MySQL (or with the mode switched off) silently picks an arbitrary row's value.
- SQLite also allows it and picks a value from some row. PostgreSQL and SQL Server raise an error, except PostgreSQL allows extra columns when you group by the primary key, since they are then determined.
- Fixes: add the column to GROUP BY, wrap it in an aggregate (MAX, MIN, STRING_AGG), use ANY_VALUE in MySQL 5.7+ if you truly do not care, or use a window function to keep row detail.

**Example:** Department headcount plus an employee name: unclear which name. Use MAX(name), or list all names with STRING_AGG / GROUP_CONCAT.

**Sample data:** `employees`

| emp_id | name | dept | salary | hire_date | status | gender |
|---|---|---|---|---|---|---|
| 1 | Asha | HR | 40000 | 2022-03-01 | Active | F |
| 2 | Bala | HR | 40000 | 2023-06-15 | Active | M |
| 3 | Chitra | HR | 60000 | 2021-01-10 | Left | F |
| 4 | Esha | IT | 70000 | 2022-08-01 | Active | F |
| 5 | Farid | IT | 90000 | 2020-02-20 | Active | M |
| 6 | Gita | IT | 90000 | 2021-09-05 | Left | F |
| 7 | Jai | Sales | 30000 | 2024-01-08 | Active | M |
| 8 | Kiran | Sales | 45000 | 2023-04-12 | Left | F |

**SQL:**
```sql
SELECT dept, name, COUNT(*) AS headcount FROM employees GROUP BY dept;

SELECT dept, name, COUNT(*) AS headcount FROM employees GROUP BY dept ORDER BY dept;

SELECT dept, COUNT(*) AS headcount, STRING_AGG(name, ', ' ORDER BY name) AS names FROM employees GROUP BY dept ORDER BY dept;
```

**Output:**

Strict engine (DuckDB, like PostgreSQL / MySQL strict mode) rejects it:

Error: Binder Error: column "name" must appear in the GROUP BY clause or must be part of an aggregate function.

SQLite accepts it and quietly picks a name per group:

| dept | name | headcount |
|---|---|---|
| HR | Asha | 3 |
| IT | Esha | 3 |
| Sales | Jai | 2 |

Correct fix: aggregate the name:

| dept | headcount | names |
|---|---|---|
| HR | 3 | Asha, Bala, Chitra |
| IT | 3 | Esha, Farid, Gita |
| Sales | 2 | Jai, Kiran |

**Edge cases:** SQLite's bare-column choice is not guaranteed; do not depend on it. MySQL checks functional dependency, so grouping by a primary key then selecting its columns is allowed. Do not disable ONLY_FULL_GROUP_BY to make an error go away.

**Likely follow-ups:** Q: How to show the highest-paid employee per department? A: use ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC), not GROUP BY. Q: What is ANY_VALUE? A: MySQL 5.7+ (and others) function that says any value is fine.

**Common mistakes:** Turning off ONLY_FULL_GROUP_BY to silence the error; trusting the arbitrary value returned; SELECT * with GROUP BY.

### Q51 ⭐ 🟡 Does putting a filter in WHERE or HAVING change query speed? Explain filtering early and how an index helps aggregate queries.

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Do you know WHERE shrinks the data before grouping, HAVING after, and that indexes can serve both filter and grouping?

**Say this in the interview:** Filtering early in WHERE is usually cheaper because fewer rows reach the grouping step. HAVING is only for conditions on aggregates. Good optimisers can push some HAVING filters down, but I should not rely on that.

**Explain simply:**
- Order of logical steps: FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY.
- A condition on a plain column (category = 'Books') belongs in WHERE. A condition on SUM or COUNT must be in HAVING.
- Index: a B-tree index on the filter column lets the database jump to matching rows instead of reading the whole table. An index on (category, amount) can answer SUM(amount) per category from the index alone (a covering index), and the rows already come out sorted for grouping.
- Always check the query plan (EXPLAIN) rather than guessing; I am not claiming a timing here.

**Example:** Total sales for Books only: filter in WHERE category = 'Books'. Doing GROUP BY category HAVING category = 'Books' gives the same answer but may do more work.

**Sample data:** `orders`

| order_id | customer_id | category | amount | order_date |
|---|---|---|---|---|
| 1 | C1 | Books | 300 | 2025-01-01 |
| 2 | C1 | Books | 800 | 2025-01-02 |
| 3 | C2 | Toys | 600 | 2025-01-03 |
| 4 | C2 | Toys | 900 | 2025-01-08 |
| 5 | C3 | Books | 550 | 2025-01-09 |
| 6 | C4 | Games | 200 | 2025-01-10 |
| 7 | C4 | Games | 700 | 2025-01-15 |
| 8 | C5 | Garden | 450 | 2025-01-16 |

**SQL:**
```sql
SELECT category, SUM(amount) AS total FROM orders WHERE category = 'Books' GROUP BY category;

SELECT category, SUM(amount) AS total FROM orders GROUP BY category HAVING category = 'Books';
```

**Output:**

Filter in WHERE:

| category | total |
|---|---|
| Books | 1650 |

Same result with HAVING:

| category | total |
|---|---|
| Books | 1650 |

Query plan (SQLite, real EXPLAIN QUERY PLAN output) after `CREATE INDEX idx_cat_amt ON orders(category, amount);`:
```text
SEARCH orders USING COVERING INDEX idx_cat_amt (category=?)
```
Same query with no index:
```text
SCAN orders
```

**Edge cases:** Wrapping the indexed column in a function (WHERE YEAR(order_date) = 2025) usually stops the index being used. Low-selectivity columns (few distinct values) benefit less. Too many indexes slow down inserts.

**Likely follow-ups:** Q: Show the plan? A: shown above (SQLite). Q: Is HAVING on a non-aggregate wrong? A: allowed, but WHERE is clearer and typically cheaper.

**Common mistakes:** Putting row filters in HAVING; indexing without checking the plan; applying functions on indexed columns.

### Q52 ⭐ 🟡 What is the danger of SUM(DISTINCT amount)? Show an example where it gives a wrong total.

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Do you know DISTINCT works on values, not on rows, so equal salaries are collapsed?

**Say this in the interview:** SUM(DISTINCT salary) adds each different salary value only once, so two people on the same salary are counted as one. It almost never answers a business question correctly.

**Explain simply:**
- DISTINCT removes duplicate values inside the aggregate, not duplicate employees.
- So two employees each earning 40000 contribute 40000 once, and the payroll total is understated.
- Fine uses: COUNT(DISTINCT customer_id) (how many different customers). If you want to de-duplicate rows, dedupe by key first (for example by emp_id) and then SUM.
- Same trap with AVG(DISTINCT x).

**Example:** HR department: salaries 40000, 40000, 60000. True payroll is 140000, but SUM(DISTINCT salary) gives 100000 because the second 40000 vanishes.

**Sample data:** `employees`

| emp_id | name | dept | salary | hire_date | status | gender |
|---|---|---|---|---|---|---|
| 1 | Asha | HR | 40000 | 2022-03-01 | Active | F |
| 2 | Bala | HR | 40000 | 2023-06-15 | Active | M |
| 3 | Chitra | HR | 60000 | 2021-01-10 | Left | F |
| 4 | Esha | IT | 70000 | 2022-08-01 | Active | F |
| 5 | Farid | IT | 90000 | 2020-02-20 | Active | M |
| 6 | Gita | IT | 90000 | 2021-09-05 | Left | F |
| 7 | Jai | Sales | 30000 | 2024-01-08 | Active | M |
| 8 | Kiran | Sales | 45000 | 2023-04-12 | Left | F |

**SQL:**
```sql
SELECT dept,
       SUM(salary) AS true_total,
       SUM(DISTINCT salary) AS distinct_total,
       SUM(salary) - SUM(DISTINCT salary) AS lost
FROM employees
GROUP BY dept
ORDER BY dept;
```

**Output:**

| dept | true_total | distinct_total | lost |
|---|---|---|---|
| HR | 140000 | 100000 | 40000 |
| IT | 250000 | 160000 | 90000 |
| Sales | 75000 | 75000 | 0 |

**pandas equivalent:**
```python
g = employees.groupby('dept')['salary']
r = pd.DataFrame({'true_total': g.sum(), 'distinct_total': g.apply(lambda s: s.drop_duplicates().sum())})
r['lost'] = r.true_total - r.distinct_total
print(r.reset_index().to_string(index=False))
```
Output:
```text
 dept  true_total  distinct_total  lost
   HR      140000          100000 40000
   IT      250000          160000 90000
Sales       75000           75000     0
```

**Edge cases:** Departments where all salaries differ (Sales) look correct, which hides the bug. NULLs are ignored either way. After a join that duplicates rows, SUM(DISTINCT amount) looks like a cheap fix but is wrong; dedupe by key instead (see fan-out).

**Likely follow-ups:** Q: Fix for a join fan-out? A: aggregate before joining, or SUM over a deduplicated subquery keyed by order_id. Q: Is COUNT(DISTINCT) safe? A: Yes when you want unique values.

**Common mistakes:** Using SUM(DISTINCT amount) to fix double counting; not testing on data with repeated values; assuming DISTINCT means distinct rows.

### Q53 ⭐ 🔴 Find the median salary for each department (the question reported in a Meesho Bengaluru 2025 interview was median per subject per class).

**Asked at:** Reported by a candidate for Meesho Bengaluru (business analyst intern, 2025) as median per subject per class; seen only as a Glassdoor search snippet, anecdotal.

**What the interviewer is checking:** Can you compute a median, which most databases lack as a simple aggregate, and do it per group?

**Say this in the interview:** Median is the middle value. In PostgreSQL, Oracle or DuckDB I use PERCENTILE_CONT(0.5) with WITHIN GROUP. Where that is missing, I number rows per department and average the one or two middle rows.

**Explain simply:**
- Median is better than average for salaries because a few very high salaries do not pull it up.
- PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) interpolates between the two middle values for an even count. PostgreSQL and Oracle support it as an aggregate; SQL Server only as a window function (OVER (PARTITION BY ...)). MySQL has no median function. DuckDB also has MEDIAN().
- Portable method: rank rows, count rows, take the middle row if odd, average the two middle rows if even.
- For the Meesho wording (median per subject per class) group by both columns: PARTITION BY subject, class.

**Example:** IT salaries 70000, 90000, 90000: the middle value is 90000. Sales has 30000 and 45000, so the median is the average, 37500.

**Sample data:** `employees`

| emp_id | name | dept | salary | hire_date | status | gender |
|---|---|---|---|---|---|---|
| 1 | Asha | HR | 40000 | 2022-03-01 | Active | F |
| 2 | Bala | HR | 40000 | 2023-06-15 | Active | M |
| 3 | Chitra | HR | 60000 | 2021-01-10 | Left | F |
| 4 | Esha | IT | 70000 | 2022-08-01 | Active | F |
| 5 | Farid | IT | 90000 | 2020-02-20 | Active | M |
| 6 | Gita | IT | 90000 | 2021-09-05 | Left | F |
| 7 | Jai | Sales | 30000 | 2024-01-08 | Active | M |
| 8 | Kiran | Sales | 45000 | 2023-04-12 | Left | F |

**SQL:**
```sql
SELECT dept,
       PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median_salary
FROM employees
GROUP BY dept
ORDER BY dept;

WITH r AS (
  SELECT dept, salary,
         ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary) AS rn,
         COUNT(*) OVER (PARTITION BY dept) AS cnt
  FROM employees
)
SELECT dept, AVG(salary) AS median_salary
FROM r
WHERE rn IN (FLOOR((cnt + 1) / 2.0), FLOOR((cnt + 2) / 2.0))
GROUP BY dept
ORDER BY dept;
```

**Output:**

PERCENTILE_CONT (PostgreSQL, Oracle, DuckDB):

| dept | median_salary |
|---|---|
| HR | 40000.0 |
| IT | 90000.0 |
| Sales | 37500.0 |

Portable method (any database with window functions):

| dept | median_salary |
|---|---|
| HR | 40000.0 |
| IT | 90000.0 |
| Sales | 37500.0 |

**pandas equivalent:**
```python
r = employees.groupby('dept')['salary'].median().reset_index(name='median_salary')
print(r.to_string(index=False))
```
Output:
```text
 dept  median_salary
   HR        40000.0
   IT        90000.0
Sales        37500.0
```

**Edge cases:** NULL salaries are ignored by PERCENTILE_CONT but must be filtered out manually in the portable method (otherwise they distort counts). Even counts return a value that may not exist in the data (37500). Use PERCENTILE_DISC(0.5) if you want an actual value.

**Likely follow-ups:** Q: Mean vs median? A: Mean uses all values and is pulled by outliers; median is the middle. Q: Median in MySQL? A: use the ROW_NUMBER method above.

**Common mistakes:** Computing AVG and calling it median; taking only one middle row for an even count; forgetting PARTITION BY so the median is overall.

### Q54 ⭐ 🔴 Given employees(emp_id, name, dept, salary, hire_date, status), find the most frequent salary (mode) in each department.

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Can you count frequency per group and then pick the top, handling ties?

**Say this in the interview:** I count how often each salary appears in each department, rank those counts within the department, and keep rank 1. RANK keeps ties, so I show all modes.

**Explain simply:**
- Mode is the most frequent value.
- Step 1: GROUP BY dept, salary with COUNT(*) as frequency.
- Step 2: RANK() OVER (PARTITION BY dept ORDER BY frequency DESC) and keep rank 1. RANK gives tied values the same rank, ROW_NUMBER would silently drop one.
- A window function is a calculation across related rows that keeps every row.

**Example:** HR has 40000 twice and 60000 once, so the mode is 40000. In Sales, 30000 and 45000 each appear once, so both are modes.

**Sample data:** `employees`

| emp_id | name | dept | salary | hire_date | status | gender |
|---|---|---|---|---|---|---|
| 1 | Asha | HR | 40000 | 2022-03-01 | Active | F |
| 2 | Bala | HR | 40000 | 2023-06-15 | Active | M |
| 3 | Chitra | HR | 60000 | 2021-01-10 | Left | F |
| 4 | Esha | IT | 70000 | 2022-08-01 | Active | F |
| 5 | Farid | IT | 90000 | 2020-02-20 | Active | M |
| 6 | Gita | IT | 90000 | 2021-09-05 | Left | F |
| 7 | Jai | Sales | 30000 | 2024-01-08 | Active | M |
| 8 | Kiran | Sales | 45000 | 2023-04-12 | Left | F |

**SQL:**
```sql
WITH c AS (
  SELECT dept, salary, COUNT(*) AS freq,
         RANK() OVER (PARTITION BY dept ORDER BY COUNT(*) DESC) AS rk
  FROM employees
  GROUP BY dept, salary
)
SELECT dept, salary AS mode_salary, freq
FROM c
WHERE rk = 1
ORDER BY dept, salary;
```

**Output:**

| dept | mode_salary | freq |
|---|---|---|
| HR | 40000 | 2 |
| IT | 90000 | 2 |
| Sales | 30000 | 1 |
| Sales | 45000 | 1 |

**pandas equivalent:**
```python
c = employees.groupby(['dept', 'salary']).size().reset_index(name='freq')
r = c[c.freq == c.groupby('dept')['freq'].transform('max')].rename(columns={'salary': 'mode_salary'})
print(r.sort_values(['dept', 'mode_salary']).to_string(index=False))
```
Output:
```text
 dept  mode_salary  freq
   HR        40000     2
   IT        90000     2
Sales        30000     1
Sales        45000     1
```

**Edge cases:** Ties: all tied values are returned; use ROW_NUMBER with a tiebreaker (e.g. lowest salary) if exactly one is required. A mode with frequency 1 (all values unique) is not meaningful, say so. NULL salaries form their own group unless filtered.

**Likely follow-ups:** Q: PostgreSQL shortcut? A: MODE() WITHIN GROUP (ORDER BY salary) returns one mode per group. Q: One row per dept only? A: ROW_NUMBER with ORDER BY freq DESC, salary.

**Common mistakes:** Using MAX(COUNT(*)) directly; using ROW_NUMBER and losing ties; forgetting PARTITION BY dept so the ranking is company-wide.

### Q55 ⭐ 🔴 Given orders(order_id, customer_id, category, amount, order_date), find customers whose every order was above 500 (all rows in the group meet a condition) using HAVING.

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Can you express 'every row meets a condition' as an aggregate test in HAVING?

**Say this in the interview:** Every order above 500 is the same as the smallest order being above 500. So I group by customer and use HAVING MIN(amount) > 500.

**Explain simply:**
- If the smallest value passes the test, all values pass it.
- Alternative: count the failing rows and require zero: HAVING SUM(CASE WHEN amount <= 500 THEN 1 ELSE 0 END) = 0.
- HAVING is the filter that runs after grouping, so it can use MIN, SUM and COUNT. WHERE would drop the small orders and make a customer with a 300 order look fine.

**Example:** C2 ordered 600 and 900, so qualifies. C3 has one order of 550, also qualifies. C1 has a 300 order, so does not.

**Sample data:** `orders`

| order_id | customer_id | category | amount | order_date |
|---|---|---|---|---|
| 1 | C1 | Books | 300 | 2025-01-01 |
| 2 | C1 | Books | 800 | 2025-01-02 |
| 3 | C2 | Toys | 600 | 2025-01-03 |
| 4 | C2 | Toys | 900 | 2025-01-08 |
| 5 | C3 | Books | 550 | 2025-01-09 |
| 6 | C4 | Games | 200 | 2025-01-10 |
| 7 | C4 | Games | 700 | 2025-01-15 |
| 8 | C5 | Garden | 450 | 2025-01-16 |

**SQL:**
```sql
SELECT customer_id, COUNT(*) AS orders, MIN(amount) AS min_amount
FROM orders
GROUP BY customer_id
HAVING MIN(amount) > 500
ORDER BY customer_id;

SELECT customer_id
FROM orders
GROUP BY customer_id
HAVING SUM(CASE WHEN amount <= 500 THEN 1 ELSE 0 END) = 0
ORDER BY customer_id;
```

**Output:**

MIN method:

| customer_id | orders | min_amount |
|---|---|---|
| C2 | 2 | 600 |
| C3 | 1 | 550 |

Count-the-failures method:

| customer_id |
|---|
| C2 |
| C3 |

**pandas equivalent:**
```python
g = orders.groupby('customer_id')['amount'].agg(orders='count', min_amount='min').reset_index()
print(g[g.min_amount > 500].to_string(index=False))
```
Output:
```text
customer_id  orders  min_amount
         C2       2         600
         C3       1         550
```

**Edge cases:** NULL amounts are ignored by MIN, so a customer with a NULL amount and other large orders still passes. If NULL should fail, add AND COUNT(*) = COUNT(amount). A customer with no orders is not in the table at all.

**Likely follow-ups:** Q: Customers with at least one order above 500? A: HAVING MAX(amount) > 500 or WHERE amount > 500. Q: Same with NOT EXISTS? A: yes, select customers with no order <= 500.

**Common mistakes:** Using WHERE amount > 500 (returns customers who have at least one large order, not all); using HAVING amount > 500 (amount is not grouped, error or wrong).

### Q56 ⭐ 🔴 Given orders(order_id, customer_id, category, amount, order_date), show the distribution: how many customers placed 1 order, 2 orders, 3 orders and so on (group of a group).

**Asked at:** Gap-fill question (author judgment of standard analyst SQL); no company-specific report found.

**What the interviewer is checking:** Can you group the output of a group, which is a classic two-level aggregation?

**Say this in the interview:** I first count orders per customer in a subquery, then group those counts and count how many customers share each count.

**Explain simply:**
- Level 1: GROUP BY customer_id, COUNT(*) gives orders per customer.
- Level 2: GROUP BY that count, COUNT(*) gives number of customers with that many orders.
- This is a frequency distribution, useful for repeat-purchase analysis; the HR equivalent is how many employees took 0, 1, 2 leaves.

**Example:** Customers C3 and C5 placed 1 order each; C1, C2 and C4 placed 2 each. So the distribution is 1 order: 2 customers, 2 orders: 3 customers.

**Sample data:** `orders`

| order_id | customer_id | category | amount | order_date |
|---|---|---|---|---|
| 1 | C1 | Books | 300 | 2025-01-01 |
| 2 | C1 | Books | 800 | 2025-01-02 |
| 3 | C2 | Toys | 600 | 2025-01-03 |
| 4 | C2 | Toys | 900 | 2025-01-08 |
| 5 | C3 | Books | 550 | 2025-01-09 |
| 6 | C4 | Games | 200 | 2025-01-10 |
| 7 | C4 | Games | 700 | 2025-01-15 |
| 8 | C5 | Garden | 450 | 2025-01-16 |

**SQL:**
```sql
SELECT order_count, COUNT(*) AS customers
FROM (
  SELECT customer_id, COUNT(*) AS order_count
  FROM orders
  GROUP BY customer_id
) AS per_customer
GROUP BY order_count
ORDER BY order_count;
```

**Output:**

| order_count | customers |
|---|---|
| 1 | 2 |
| 2 | 3 |

**pandas equivalent:**
```python
counts = orders.groupby('customer_id').size()
r = counts.value_counts().sort_index().rename_axis('order_count').reset_index(name='customers')
print(r.to_string(index=False))
```
Output:
```text
 order_count  customers
           1          2
           2          3
```

**Edge cases:** Counts with no customers (for example nobody with 4 orders) are missing; join to a generated number series to show zeros. Customers with zero orders need a customers table and LEFT JOIN to appear as order_count 0.

**Likely follow-ups:** Q: Add percentage of customers? A: customers * 100.0 / SUM(customers) OVER (). Q: Bucket 3+ orders together? A: CASE WHEN order_count >= 3 THEN '3+' ELSE order_count END.

**Common mistakes:** Trying GROUP BY COUNT(*) directly (not allowed); forgetting the inner query alias (required in MySQL and PostgreSQL); counting orders instead of customers in the outer step.

### Q57 ⭐ 🔴 Explain GROUPING SETS with an example that gives totals by (dept), by (gender) and by both in one query, and how GROUPING() flags subtotal rows.

**Asked at:** commonly asked (no company-specific report found)

**What the interviewer is checking:** Do you know how to get several independent groupings and tell subtotal rows apart from real NULLs?

**Say this in the interview:** GROUPING SETS lets me list exactly the groupings I want in one query: by dept, by gender and by both. GROUPING(col) returns 1 on rows where that column was rolled up.

**Explain simply:**
- Without it you would write three GROUP BY queries and UNION ALL them.
- In the output, a column that is not part of that grouping shows NULL. GROUPING(dept) = 1 means 'this row is not split by dept'.
- The employees table in the question has no gender column; I added one to the sample data to answer it.
- Supported by PostgreSQL 9.5+, SQL Server, Oracle, DuckDB, Snowflake, BigQuery. MySQL and SQLite do not have it (use UNION ALL).

**Example:** Headcount by dept and gender, by dept alone, and by gender alone, all in one result.

**Sample data:** `employees`

| emp_id | name | dept | salary | hire_date | status | gender |
|---|---|---|---|---|---|---|
| 1 | Asha | HR | 40000 | 2022-03-01 | Active | F |
| 2 | Bala | HR | 40000 | 2023-06-15 | Active | M |
| 3 | Chitra | HR | 60000 | 2021-01-10 | Left | F |
| 4 | Esha | IT | 70000 | 2022-08-01 | Active | F |
| 5 | Farid | IT | 90000 | 2020-02-20 | Active | M |
| 6 | Gita | IT | 90000 | 2021-09-05 | Left | F |
| 7 | Jai | Sales | 30000 | 2024-01-08 | Active | M |
| 8 | Kiran | Sales | 45000 | 2023-04-12 | Left | F |

**SQL:**
```sql
SELECT dept, gender, COUNT(*) AS headcount,
       GROUPING(dept) AS g_dept, GROUPING(gender) AS g_gender
FROM employees
GROUP BY GROUPING SETS ((dept), (gender), (dept, gender))
ORDER BY GROUPING(dept), GROUPING(gender), dept, gender;
```

**Output:**

| dept | gender | headcount | g_dept | g_gender |
|---|---|---|---|---|
| HR | F | 2 | 0 | 0 |
| HR | M | 1 | 0 | 0 |
| IT | F | 2 | 0 | 0 |
| IT | M | 1 | 0 | 0 |
| Sales | F | 1 | 0 | 0 |
| Sales | M | 1 | 0 | 0 |
| HR | NULL | 3 | 0 | 1 |
| IT | NULL | 3 | 0 | 1 |
| Sales | NULL | 2 | 0 | 1 |
| NULL | F | 5 | 1 | 0 |
| NULL | M | 3 | 1 | 0 |

**pandas equivalent:**
```python
a = employees.groupby(['dept', 'gender']).size().reset_index(name='headcount').assign(g_dept=0, g_gender=0)
b = employees.groupby('dept').size().reset_index(name='headcount').assign(g_dept=0, g_gender=1)
c = employees.groupby('gender').size().reset_index(name='headcount').assign(g_dept=1, g_gender=0)
r = pd.concat([a, b, c], ignore_index=True)[['dept', 'gender', 'headcount', 'g_dept', 'g_gender']]
print(r.to_string(index=False))
```
Output:
```text
 dept gender  headcount  g_dept  g_gender
   HR      F          2       0         0
   HR      M          1       0         0
   IT      F          2       0         0
   IT      M          1       0         0
Sales      F          1       0         0
Sales      M          1       0         0
   HR    NaN          3       0         1
   IT    NaN          3       0         1
Sales    NaN          2       0         1
  NaN      F          5       1         0
  NaN      M          3       1         0
```

**Edge cases:** If gender has real NULLs, those rows also show NULL; only GROUPING() distinguishes them. GROUPING SETS with () adds a grand total. ROLLUP(a,b) equals GROUPING SETS ((a,b),(a),()); CUBE(a,b) equals ((a,b),(a),(b),()).

**Likely follow-ups:** Q: GROUPING vs GROUPING_ID? A: GROUPING_ID (SQL Server, Oracle) packs several flags into one number. Q: MySQL substitute? A: UNION ALL of the three GROUP BY queries.

**Common mistakes:** Treating NULL as 'total' without GROUPING(); expecting MySQL to support it; forgetting the grand total needs ().

