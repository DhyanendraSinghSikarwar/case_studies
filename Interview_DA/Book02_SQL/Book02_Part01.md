# Book 2 — SQL · Part 1: SELECT, WHERE, ORDER BY, DISTINCT, LIMIT 🟢

**Target:** 50 questions  |  **Actual:** 61 questions

**Scope:** Reading data from a single table: SELECT, column aliases, WHERE filters (AND/OR/NOT, IN, BETWEEN, LIKE, NULL), ORDER BY, DISTINCT, LIMIT/OFFSET, clause execution order, second/Nth highest salary via LIMIT-OFFSET. Aggregates, joins, windows and DENSE_RANK solutions are in later parts.

### Q1 ⭐⭐⭐ 🟢 What does the SELECT statement do? Why is naming the columns you need usually better than `SELECT *`?
**Asked at:** Commonly asked at service MNCs, GCCs, analytics firms and startups as a warm-up (no company-specific report found).
**What the interviewer is checking:** Do you know SELECT picks columns and does not change data, and that you avoid `SELECT *` on purpose.
**Say this in the interview:** SELECT is how you ask the database to show me data. It only reads, never changes anything. I name the columns I need because it is faster, clearer and does not break when someone adds a column later.
**Explain simply:**
- **SELECT** = the command that reads data. It lists which **columns** (fields like name or salary) you want; **FROM** says which **table** (a sheet of rows and columns).
- `SELECT *` means every column. Fine for a quick peek, risky in real work.
- Naming columns: less data travels over the network, the database may skip reading unused columns, and the query still returns the same shape if a new column is added.
- It is also self-documenting: the reader sees exactly what the report contains (and you do not accidentally expose sensitive columns like salary).
**Example:** An HR dashboard needs name and department of 50,000 employees. `SELECT *` also drags salary, address and phone to the screen; two columns is lighter and safer.
**SQL:**
```sql
SELECT emp_name, department FROM Employees ORDER BY emp_id LIMIT 3;
```
**Output:**

| emp_name | department |
|---|---|
| Anita Sharma | HR |
| Arjun Mehta | Sales |
| Sneha Iyer | HR |
**Edge cases:** `SELECT *` over a view or joined tables can return duplicate column names. Order of columns follows your list, not the table.
**Likely follow-ups:**
- Does SELECT change data? No, only INSERT/UPDATE/DELETE do.
- Is `SELECT *` ever fine? Yes, for exploring a small table or `SELECT COUNT(*)`.
**Common mistakes:** Using `SELECT *` in production reports or inside subqueries, and thinking SELECT can modify rows.

### Q2 ⭐⭐⭐ 🟢 Write a query to show only the employee name and department for everyone in the `Employees` table (columns: emp_id, emp_name, department, city, salary, manager_id, hire_date).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Basic SELECT syntax.
**Say this in the interview:** I list only the two columns after SELECT and name the table after FROM.
**Explain simply:**
- Columns are separated by commas; no comma after the last one.
- Rows come back in no guaranteed order (see Q33).
**Example:** For a headcount-by-name list, the HR team just needs name and department: 8 employees, 2 columns.
**Sample data:** `Employees` (8 rows; manager_id blank = NULL, i.e. no manager):

| emp_id | emp_name | department | city | salary | manager_id | hire_date |
|---|---|---|---|---|---|---|
| 1 | Anita Sharma | HR | Hyderabad | 90000 | NULL | 2020-03-10 |
| 2 | Arjun Mehta | Sales | Bengaluru | 72000 | 1 | 2021-07-01 |
| 3 | Sneha Iyer | HR | Pune | 48000 | 1 | 2022-11-20 |
| 4 | Rahul Verma | Sales | Hyderabad | 55000 | 2 | 2023-02-14 |
| 5 | Priya Nair | IT | Bengaluru | 90000 | 1 | 2023-08-01 |
| 6 | Amit Kumar | IT | Pune | 65000 | 5 | 2023-12-31 |
| 7 | Kavya Reddy | Finance | Hyderabad | 50000 | 1 | 2024-01-15 |
| 8 | Vikram Singh | Sales | Chennai | 38000 | 2 | 2024-04-01 |
**SQL:**
```sql
SELECT emp_name, department
FROM Employees;
```
**Output:**

| emp_name | department |
|---|---|
| Anita Sharma | HR |
| Arjun Mehta | Sales |
| Sneha Iyer | HR |
| Rahul Verma | Sales |
| Priya Nair | IT |
| Amit Kumar | IT |
| Kavya Reddy | Finance |
| Vikram Singh | Sales |
**pandas equivalent:**
```python
emp = pd.read_sql('SELECT * FROM Employees', conn)  # or pd.read_csv(...)
res = emp[['emp_name', 'department']]
```
Same result as the SQL (checked by running both).
**Edge cases:** Duplicate rows are kept (use DISTINCT to remove). NULL departments would show as NULL.
**Likely follow-ups:**
- How do I rename a column? Use an alias (Q21).
- How to remove repeats? DISTINCT.
**Common mistakes:** Trailing comma before FROM, or misspelling the column name.

### Q3 ⭐⭐⭐ 🟢 Write a query to list all employees earning more than 50,000 from the `Employees` table (columns: emp_id, emp_name, department, city, salary, manager_id, hire_date). What does the WHERE clause do?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you filter rows with WHERE and use comparison operators correctly.
**Say this in the interview:** WHERE keeps only the rows that pass the condition. Here it keeps salary strictly greater than 50,000, so exactly 50,000 is left out.
**Explain simply:**
- **WHERE** is a filter on **rows** (SELECT picks columns, WHERE picks rows).
- `>` is strictly greater; use `>=` to include 50,000.
- Numbers are written without quotes.
**Example:** Find who earns above 50,000 for a pay-band review: Kavya earns exactly 50,000, so she is not in the list.
**Sample data:** `Employees` (8 rows; manager_id blank = NULL, i.e. no manager):

| emp_id | emp_name | department | city | salary | manager_id | hire_date |
|---|---|---|---|---|---|---|
| 1 | Anita Sharma | HR | Hyderabad | 90000 | NULL | 2020-03-10 |
| 2 | Arjun Mehta | Sales | Bengaluru | 72000 | 1 | 2021-07-01 |
| 3 | Sneha Iyer | HR | Pune | 48000 | 1 | 2022-11-20 |
| 4 | Rahul Verma | Sales | Hyderabad | 55000 | 2 | 2023-02-14 |
| 5 | Priya Nair | IT | Bengaluru | 90000 | 1 | 2023-08-01 |
| 6 | Amit Kumar | IT | Pune | 65000 | 5 | 2023-12-31 |
| 7 | Kavya Reddy | Finance | Hyderabad | 50000 | 1 | 2024-01-15 |
| 8 | Vikram Singh | Sales | Chennai | 38000 | 2 | 2024-04-01 |
**SQL:**
```sql
SELECT emp_name, salary
FROM Employees
WHERE salary > 50000;
```
**Output:**

| emp_name | salary |
|---|---|
| Anita Sharma | 90000 |
| Arjun Mehta | 72000 |
| Rahul Verma | 55000 |
| Priya Nair | 90000 |
| Amit Kumar | 65000 |
**pandas equivalent:**
```python
emp = pd.read_sql('SELECT * FROM Employees', conn)  # or pd.read_csv(...)
res = emp.loc[emp['salary'] > 50000, ['emp_name', 'salary']]
```
Same result as the SQL (checked by running both).
**Edge cases:** NULL salary rows never pass `> 50000` (unknown is not true). Empty result is valid, not an error.
**Likely follow-ups:**
- How to include 50,000? Use `>=`.
- Can WHERE use aggregates like AVG? No, use HAVING (Q26).
**Common mistakes:** Writing `salary > '50,000'` with a comma or quotes, or using `=>` instead of `>=`.

### Q4 ⭐⭐⭐ 🟢 Write a query to find employees who work in 'Sales' or 'HR' and earn more than 50,000. Why do you need brackets when mixing AND with OR?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** AND/OR precedence: AND is evaluated before OR.
**Say this in the interview:** I put the OR part in brackets, because AND binds tighter than OR. Without brackets the salary rule would apply only to HR.
**Explain simply:**
- **AND** needs both sides true; **OR** needs at least one. AND is calculated first, like multiplication before addition.
- Without brackets, `A OR B AND C` is read as `A OR (B AND C)`.
- Brackets make the intention explicit and cost nothing.
**Example:** Shortlist Sales or HR staff above 50,000. Wrong version also returns Vikram (Sales, 38,000).
**Sample data:** `Employees` (8 rows; manager_id blank = NULL, i.e. no manager):

| emp_id | emp_name | department | city | salary | manager_id | hire_date |
|---|---|---|---|---|---|---|
| 1 | Anita Sharma | HR | Hyderabad | 90000 | NULL | 2020-03-10 |
| 2 | Arjun Mehta | Sales | Bengaluru | 72000 | 1 | 2021-07-01 |
| 3 | Sneha Iyer | HR | Pune | 48000 | 1 | 2022-11-20 |
| 4 | Rahul Verma | Sales | Hyderabad | 55000 | 2 | 2023-02-14 |
| 5 | Priya Nair | IT | Bengaluru | 90000 | 1 | 2023-08-01 |
| 6 | Amit Kumar | IT | Pune | 65000 | 5 | 2023-12-31 |
| 7 | Kavya Reddy | Finance | Hyderabad | 50000 | 1 | 2024-01-15 |
| 8 | Vikram Singh | Sales | Chennai | 38000 | 2 | 2024-04-01 |
**SQL:**
```sql
SELECT emp_name, department, salary
FROM Employees
WHERE (department = 'Sales' OR department = 'HR')
  AND salary > 50000;
```
**Output:**

| emp_name | department | salary |
|---|---|---|
| Anita Sharma | HR | 90000 |
| Arjun Mehta | Sales | 72000 |
| Rahul Verma | Sales | 55000 |
**Wrong version (no brackets) - note Vikram 38,000 sneaks in:**
```sql
SELECT emp_name, department, salary
FROM Employees
WHERE department = 'Sales' OR department = 'HR' AND salary > 50000;
```

| emp_name | department | salary |
|---|---|---|
| Anita Sharma | HR | 90000 |
| Arjun Mehta | Sales | 72000 |
| Rahul Verma | Sales | 55000 |
| Vikram Singh | Sales | 38000 |
**pandas equivalent:**
```python
emp = pd.read_sql('SELECT * FROM Employees', conn)  # or pd.read_csv(...)
res = emp.loc[emp['department'].isin(['Sales', 'HR']) & (emp['salary'] > 50000), ['emp_name', 'department', 'salary']]
```
Same result as the SQL (checked by running both).
**Edge cases:** pandas also needs brackets around each condition because `&` binds tighter than `>`. `department IN ('Sales','HR')` is a tidy alternative.
**Likely follow-ups:**
- Shorter way? `department IN ('Sales','HR') AND salary > 50000`.
- Does order of OR terms matter? No.
**Common mistakes:** Dropping the brackets and not noticing the extra rows; always test with a row that should be excluded.

### Q5 ⭐⭐⭐ 🟢 Write a query to list employees from the highest salary to the lowest. What is the default sort direction of ORDER BY, and how do you reverse it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** ORDER BY, default direction, DESC.
**Say this in the interview:** ORDER BY sorts ascending by default, smallest first. I add DESC to flip it for highest first.
**Explain simply:**
- Default is **ASC** (ascending: A to Z, small to large, oldest to newest).
- **DESC** reverses it.
- Without ORDER BY the row order is not guaranteed.
- Add a second column to break ties (Q34): here two people earn 90,000.
**Example:** Payroll wants the salary list top to bottom: 90,000 first, 38,000 last.
**Sample data:** `Employees` (8 rows; manager_id blank = NULL, i.e. no manager):

| emp_id | emp_name | department | city | salary | manager_id | hire_date |
|---|---|---|---|---|---|---|
| 1 | Anita Sharma | HR | Hyderabad | 90000 | NULL | 2020-03-10 |
| 2 | Arjun Mehta | Sales | Bengaluru | 72000 | 1 | 2021-07-01 |
| 3 | Sneha Iyer | HR | Pune | 48000 | 1 | 2022-11-20 |
| 4 | Rahul Verma | Sales | Hyderabad | 55000 | 2 | 2023-02-14 |
| 5 | Priya Nair | IT | Bengaluru | 90000 | 1 | 2023-08-01 |
| 6 | Amit Kumar | IT | Pune | 65000 | 5 | 2023-12-31 |
| 7 | Kavya Reddy | Finance | Hyderabad | 50000 | 1 | 2024-01-15 |
| 8 | Vikram Singh | Sales | Chennai | 38000 | 2 | 2024-04-01 |
**SQL:**
```sql
SELECT emp_name, salary
FROM Employees
ORDER BY salary DESC, emp_id;
```
**Output:**

| emp_name | salary |
|---|---|
| Anita Sharma | 90000 |
| Priya Nair | 90000 |
| Arjun Mehta | 72000 |
| Amit Kumar | 65000 |
| Rahul Verma | 55000 |
| Kavya Reddy | 50000 |
| Sneha Iyer | 48000 |
| Vikram Singh | 38000 |
**pandas equivalent:**
```python
emp = pd.read_sql('SELECT * FROM Employees', conn)  # or pd.read_csv(...)
res = emp.sort_values(['salary', 'emp_id'], ascending=[False, True])[['emp_name', 'salary']]
```
Same result as the SQL (checked by running both).
**Edge cases:** Tied salaries (Anita and Priya) appear in unpredictable order unless you add emp_id. NULL salaries sort first in SQLite/MySQL/SQL Server ascending, last in PostgreSQL/Oracle (Q35).
**Likely follow-ups:**
- Is ASC needed? No, optional.
- Sort by two columns? Comma-separate them (Q18).
**Common mistakes:** Writing `DESC` before the column name, or assuming the table is already stored in sorted order.

### Q6 ⭐⭐⭐ 🟢 What does DISTINCT do? Write a query to list each department name only once from the Employees table.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Knowing DISTINCT removes duplicate rows.
**Say this in the interview:** DISTINCT returns each unique value once. For department it gives HR, Sales, IT and Finance one time each.
**Explain simply:**
- Eight rows but only four departments, so repeats get collapsed.
- DISTINCT looks at the whole selected row, not just one column (Q19).
- It sorts or hashes internally, so it costs time on big tables.
**Example:** A manager asks which departments exist: 8 employees, 4 departments.
**Sample data:** `Employees` (8 rows; manager_id blank = NULL, i.e. no manager):

| emp_id | emp_name | department | city | salary | manager_id | hire_date |
|---|---|---|---|---|---|---|
| 1 | Anita Sharma | HR | Hyderabad | 90000 | NULL | 2020-03-10 |
| 2 | Arjun Mehta | Sales | Bengaluru | 72000 | 1 | 2021-07-01 |
| 3 | Sneha Iyer | HR | Pune | 48000 | 1 | 2022-11-20 |
| 4 | Rahul Verma | Sales | Hyderabad | 55000 | 2 | 2023-02-14 |
| 5 | Priya Nair | IT | Bengaluru | 90000 | 1 | 2023-08-01 |
| 6 | Amit Kumar | IT | Pune | 65000 | 5 | 2023-12-31 |
| 7 | Kavya Reddy | Finance | Hyderabad | 50000 | 1 | 2024-01-15 |
| 8 | Vikram Singh | Sales | Chennai | 38000 | 2 | 2024-04-01 |
**SQL:**
```sql
SELECT DISTINCT department
FROM Employees;
```
**Output:**

| department |
|---|
| HR |
| Sales |
| IT |
| Finance |
**pandas equivalent:**
```python
emp = pd.read_sql('SELECT * FROM Employees', conn)  # or pd.read_csv(...)
res = emp[['department']].drop_duplicates()
```
Same result as the SQL (checked by running both).
**Edge cases:** NULL counts as one distinct value (all NULLs are grouped). Output order is not guaranteed; add ORDER BY if you need it. Case differences ('hr' vs 'HR') count as different in most databases.
**Likely follow-ups:**
- Count the distinct ones? `COUNT(DISTINCT department)` (Q43).
- Alternative? GROUP BY department (Q44).
**Common mistakes:** Using DISTINCT to hide duplicates caused by a wrong join (Q56).

### Q7 ⭐⭐⭐ 🟢 Write a query to show the 5 highest-paid employees. How does this differ across databases (LIMIT, TOP, FETCH FIRST)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Top-N pattern and awareness of dialect differences.
**Say this in the interview:** I sort by salary descending and take the first 5. MySQL, PostgreSQL and SQLite use LIMIT 5, SQL Server uses TOP 5, and Oracle and standard SQL use FETCH FIRST 5 ROWS ONLY.
**Explain simply:**
- **Top-N** = sort first, then cut the list. Without ORDER BY, LIMIT returns arbitrary rows.
- I add `emp_id` as a tie-breaker so the answer is repeatable.
**Example:** Pick the 5 highest earners for a compensation review.
**Sample data:** `Employees` (8 rows; manager_id blank = NULL, i.e. no manager):

| emp_id | emp_name | department | city | salary | manager_id | hire_date |
|---|---|---|---|---|---|---|
| 1 | Anita Sharma | HR | Hyderabad | 90000 | NULL | 2020-03-10 |
| 2 | Arjun Mehta | Sales | Bengaluru | 72000 | 1 | 2021-07-01 |
| 3 | Sneha Iyer | HR | Pune | 48000 | 1 | 2022-11-20 |
| 4 | Rahul Verma | Sales | Hyderabad | 55000 | 2 | 2023-02-14 |
| 5 | Priya Nair | IT | Bengaluru | 90000 | 1 | 2023-08-01 |
| 6 | Amit Kumar | IT | Pune | 65000 | 5 | 2023-12-31 |
| 7 | Kavya Reddy | Finance | Hyderabad | 50000 | 1 | 2024-01-15 |
| 8 | Vikram Singh | Sales | Chennai | 38000 | 2 | 2024-04-01 |
**SQL:**
```sql
SELECT emp_name, salary
FROM Employees
ORDER BY salary DESC, emp_id
LIMIT 5;
```
Other dialects (not run here):
```sql
-- SQL Server / MS Access
SELECT TOP 5 emp_name, salary FROM Employees ORDER BY salary DESC, emp_id;
-- Oracle 12c+, PostgreSQL, standard SQL
SELECT emp_name, salary FROM Employees ORDER BY salary DESC, emp_id FETCH FIRST 5 ROWS ONLY;
```
**Output:**

| emp_name | salary |
|---|---|
| Anita Sharma | 90000 |
| Priya Nair | 90000 |
| Arjun Mehta | 72000 |
| Amit Kumar | 65000 |
| Rahul Verma | 55000 |
**pandas equivalent:**
```python
emp = pd.read_sql('SELECT * FROM Employees', conn)  # or pd.read_csv(...)
res = emp.sort_values(['salary', 'emp_id'], ascending=[False, True]).head(5)[['emp_name', 'salary']]
```
Same result as the SQL (checked by running both).
**Edge cases:** Fewer than 5 rows in the table just returns what exists. Ties at the cutoff are cut arbitrarily unless you use WITH TIES (Q59).
**Likely follow-ups:**
- Older Oracle? Use `WHERE ROWNUM <= 5` on a sorted subquery.
- Keep ties? `FETCH FIRST 5 ROWS WITH TIES` or RANK().
**Common mistakes:** Using LIMIT without ORDER BY, or writing LIMIT in SQL Server (it needs TOP).

### Q8 ⭐⭐⭐ 🟢 Write a query to find employees who have no manager (manager_id is blank/NULL). Why does `manager_id = NULL` not work?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** NULL handling: IS NULL vs = NULL.
**Say this in the interview:** I use `IS NULL`. `= NULL` never works because NULL means unknown, and nothing equals unknown, not even NULL.
**Explain simply:**
- **NULL** = missing/unknown value.
- Any comparison with NULL gives *unknown*, and WHERE only keeps rows that are true, so `= NULL` returns zero rows.
- `IS NULL` / `IS NOT NULL` are the special tests.
**Example:** Find the top of the reporting chain: Anita has no manager.
**Sample data:** `Employees` (8 rows; manager_id blank = NULL, i.e. no manager):

| emp_id | emp_name | department | city | salary | manager_id | hire_date |
|---|---|---|---|---|---|---|
| 1 | Anita Sharma | HR | Hyderabad | 90000 | NULL | 2020-03-10 |
| 2 | Arjun Mehta | Sales | Bengaluru | 72000 | 1 | 2021-07-01 |
| 3 | Sneha Iyer | HR | Pune | 48000 | 1 | 2022-11-20 |
| 4 | Rahul Verma | Sales | Hyderabad | 55000 | 2 | 2023-02-14 |
| 5 | Priya Nair | IT | Bengaluru | 90000 | 1 | 2023-08-01 |
| 6 | Amit Kumar | IT | Pune | 65000 | 5 | 2023-12-31 |
| 7 | Kavya Reddy | Finance | Hyderabad | 50000 | 1 | 2024-01-15 |
| 8 | Vikram Singh | Sales | Chennai | 38000 | 2 | 2024-04-01 |
**SQL:**
```sql
SELECT emp_id, emp_name
FROM Employees
WHERE manager_id IS NULL;
```
**Output:**

| emp_id | emp_name |
|---|---|
| 1 | Anita Sharma |
**Broken version: = NULL returns nothing:**
```sql
SELECT emp_id, emp_name FROM Employees WHERE manager_id = NULL;
```

| emp_id | emp_name |
|---|---|
| *(no rows)* | |
**pandas equivalent:**
```python
emp = pd.read_sql('SELECT * FROM Employees', conn)  # or pd.read_csv(...)
res = emp.loc[emp['manager_id'].isna(), ['emp_id', 'emp_name']]
```
Same result as the SQL (checked by running both).
**Edge cases:** If the 'blank' is an empty string rather than NULL (common in CSV imports), IS NULL misses it (Q48).
**Likely follow-ups:**
- Not null? `IS NOT NULL`.
- Replace NULL with a value? COALESCE(manager_id, 0).
**Common mistakes:** `= NULL`, or `!= NULL`, which also returns nothing.

### Q9 ⭐⭐⭐ 🟢 What is NULL in SQL, and how is it different from 0 or an empty text? What does `NULL = NULL` return?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you understand NULL as 'unknown', not zero or blank.
**Say this in the interview:** NULL means no value or unknown. It is not 0 and not an empty text. NULL = NULL returns NULL (unknown), not true.
**Explain simply:**
- **0** is a real number; **''** is a real but empty text; **NULL** is the absence of any value.
- Comparisons with NULL give unknown, so use IS NULL.
- Aggregates like AVG and COUNT(column) skip NULLs; COUNT(*) does not.
**Example:** Leave days: 0 means an employee took none; NULL means the data was never entered. Averaging treats them very differently.
**SQL:**
```sql
SELECT NULL = NULL AS null_eq_null,
       NULL IS NULL AS null_is_null,
       0 = NULL AS zero_eq_null,
       '' IS NULL AS empty_is_null;
```
**Output:**

| null_eq_null | null_is_null | zero_eq_null | empty_is_null |
|---|---|---|---|
| NULL | 1 | NULL | 0 |
**Edge cases:** SQLite shows true as 1 and false as 0; NULL stays NULL (unknown). Oracle treats '' as NULL, other databases do not. NULL + 5 is NULL.
**Likely follow-ups:**
- COUNT(*) vs COUNT(col)? The latter skips NULLs.
- NULL in ORDER BY / DISTINCT? Q35 and Q6.
**Common mistakes:** Treating NULL as zero in calculations, or filtering with `= NULL`.

### Q10 ⭐⭐⭐ 🟢 Write a query to find employees whose name starts with 'A'. What do the `%` and `_` wildcards in LIKE mean?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** LIKE wildcards.
**Say this in the interview:** I use LIKE 'A%'. The percent sign matches any number of characters, including none; the underscore matches exactly one character.
**Explain simply:**
- `%` = any text of any length (even empty).
- `_` = exactly one character.
- `'A%'` starts with A; `'%A'` ends with A; `'%A%'` contains A.
- Case sensitivity depends on the database (Q29).
**Example:** Find employees whose name starts with A: Anita, Arjun, Amit.
**Sample data:** `Employees` (8 rows; manager_id blank = NULL, i.e. no manager):

| emp_id | emp_name | department | city | salary | manager_id | hire_date |
|---|---|---|---|---|---|---|
| 1 | Anita Sharma | HR | Hyderabad | 90000 | NULL | 2020-03-10 |
| 2 | Arjun Mehta | Sales | Bengaluru | 72000 | 1 | 2021-07-01 |
| 3 | Sneha Iyer | HR | Pune | 48000 | 1 | 2022-11-20 |
| 4 | Rahul Verma | Sales | Hyderabad | 55000 | 2 | 2023-02-14 |
| 5 | Priya Nair | IT | Bengaluru | 90000 | 1 | 2023-08-01 |
| 6 | Amit Kumar | IT | Pune | 65000 | 5 | 2023-12-31 |
| 7 | Kavya Reddy | Finance | Hyderabad | 50000 | 1 | 2024-01-15 |
| 8 | Vikram Singh | Sales | Chennai | 38000 | 2 | 2024-04-01 |
**SQL:**
```sql
SELECT emp_name
FROM Employees
WHERE emp_name LIKE 'A%';
```
**Output:**

| emp_name |
|---|
| Anita Sharma |
| Arjun Mehta |
| Amit Kumar |
**Underscore demo - A, any one letter, then i:**
```sql
SELECT emp_name FROM Employees WHERE emp_name LIKE 'A_i%';
```

| emp_name |
|---|
| Anita Sharma |
| Amit Kumar |
**pandas equivalent:**
```python
emp = pd.read_sql('SELECT * FROM Employees', conn)  # or pd.read_csv(...)
res = emp.loc[emp['emp_name'].str.startswith('A'), ['emp_name']]
```
Same result as the SQL (checked by running both).
**Edge cases:** SQLite and MySQL LIKE ignore case by default; PostgreSQL LIKE is case-sensitive (use ILIKE). Leading `%` cannot use an ordinary index. NULL names are never matched.
**Likely follow-ups:**
- Ends with 'a'? `LIKE '%a'`.
- Search for a literal %? ESCAPE (Q58).
**Common mistakes:** Using `=` with a wildcard (`= 'A%'`) which matches the literal text only.

### Q11 ⭐⭐⭐ 🟢 Write a query to find employees hired between 1 Jan 2023 and 31 Dec 2023. Is BETWEEN inclusive of both ends?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Date filtering and inclusive BETWEEN.
**Say this in the interview:** Yes, BETWEEN includes both ends, so employees hired on 1 Jan or 31 Dec are included. Watch out if the column also stores time of day (Q42).
**Explain simply:**
- `BETWEEN a AND b` is the same as `>= a AND <= b`.
- Order matters: low value first, otherwise nothing is returned.
- Dates are written as text in `'YYYY-MM-DD'` format.
**Example:** 2023 joiners for an annual induction report: Amit joined on 31 Dec, and is included.
**Sample data:** `Employees` (8 rows; manager_id blank = NULL, i.e. no manager):

| emp_id | emp_name | department | city | salary | manager_id | hire_date |
|---|---|---|---|---|---|---|
| 1 | Anita Sharma | HR | Hyderabad | 90000 | NULL | 2020-03-10 |
| 2 | Arjun Mehta | Sales | Bengaluru | 72000 | 1 | 2021-07-01 |
| 3 | Sneha Iyer | HR | Pune | 48000 | 1 | 2022-11-20 |
| 4 | Rahul Verma | Sales | Hyderabad | 55000 | 2 | 2023-02-14 |
| 5 | Priya Nair | IT | Bengaluru | 90000 | 1 | 2023-08-01 |
| 6 | Amit Kumar | IT | Pune | 65000 | 5 | 2023-12-31 |
| 7 | Kavya Reddy | Finance | Hyderabad | 50000 | 1 | 2024-01-15 |
| 8 | Vikram Singh | Sales | Chennai | 38000 | 2 | 2024-04-01 |
**SQL:**
```sql
SELECT emp_name, hire_date
FROM Employees
WHERE hire_date BETWEEN '2023-01-01' AND '2023-12-31';
```
**Output:**

| emp_name | hire_date |
|---|---|
| Rahul Verma | 2023-02-14 |
| Priya Nair | 2023-08-01 |
| Amit Kumar | 2023-12-31 |
**pandas equivalent:**
```python
emp = pd.read_sql('SELECT * FROM Employees', conn)  # or pd.read_csv(...)
emp['hire_date'] = pd.to_datetime(emp['hire_date'])
res = emp.loc[emp['hire_date'].between('2023-01-01', '2023-12-31'), ['emp_name', 'hire_date']]
res = res.assign(hire_date=res['hire_date'].dt.strftime('%Y-%m-%d'))
```
Same result as the SQL (checked by running both).
**Edge cases:** With a DATETIME column, '2023-12-31' means midnight, so afternoon hires on 31 Dec are missed; use `>= '2023-01-01' AND < '2024-01-01'`. SQL Server date literals can be regional; ISO format is safest.
**Likely follow-ups:**
- Safer alternative? Half-open range (>= start, < next start).
- Year only? `EXTRACT(YEAR ...)` works but can stop index use.
**Common mistakes:** Writing the range in reverse order, or assuming BETWEEN excludes the end values.

### Q12 ⭐⭐⭐ 🟢 When would you use IN instead of several OR conditions? Write a query for employees in Hyderabad, Bengaluru or Pune.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** IN as shorthand for multiple ORs.
**Say this in the interview:** I use IN when I am matching one column against a list of values. It is shorter and easier to read than a chain of ORs.
**Explain simply:**
- `city IN ('A','B','C')` = `city = 'A' OR city = 'B' OR city = 'C'`.
- The list can also come from a subquery.
- NOT IN is the opposite (careful with NULLs, Q37).
**Example:** Hiring in three metro offices: Hyderabad, Bengaluru, Pune. Vikram in Chennai is out.
**Sample data:** `Employees` (8 rows; manager_id blank = NULL, i.e. no manager):

| emp_id | emp_name | department | city | salary | manager_id | hire_date |
|---|---|---|---|---|---|---|
| 1 | Anita Sharma | HR | Hyderabad | 90000 | NULL | 2020-03-10 |
| 2 | Arjun Mehta | Sales | Bengaluru | 72000 | 1 | 2021-07-01 |
| 3 | Sneha Iyer | HR | Pune | 48000 | 1 | 2022-11-20 |
| 4 | Rahul Verma | Sales | Hyderabad | 55000 | 2 | 2023-02-14 |
| 5 | Priya Nair | IT | Bengaluru | 90000 | 1 | 2023-08-01 |
| 6 | Amit Kumar | IT | Pune | 65000 | 5 | 2023-12-31 |
| 7 | Kavya Reddy | Finance | Hyderabad | 50000 | 1 | 2024-01-15 |
| 8 | Vikram Singh | Sales | Chennai | 38000 | 2 | 2024-04-01 |
**SQL:**
```sql
SELECT emp_name, city
FROM Employees
WHERE city IN ('Hyderabad', 'Bengaluru', 'Pune');
```
**Output:**

| emp_name | city |
|---|---|
| Anita Sharma | Hyderabad |
| Arjun Mehta | Bengaluru |
| Sneha Iyer | Pune |
| Rahul Verma | Hyderabad |
| Priya Nair | Bengaluru |
| Amit Kumar | Pune |
| Kavya Reddy | Hyderabad |
**pandas equivalent:**
```python
emp = pd.read_sql('SELECT * FROM Employees', conn)  # or pd.read_csv(...)
res = emp.loc[emp['city'].isin(['Hyderabad', 'Bengaluru', 'Pune']), ['emp_name', 'city']]
```
Same result as the SQL (checked by running both).
**Edge cases:** NULL city never matches IN. Text values are case-sensitive in some databases. Huge lists are better placed in a table and joined.
**Likely follow-ups:**
- Same result as OR? Yes.
- IN vs BETWEEN? IN is a list, BETWEEN is a range (Q25).
**Common mistakes:** Forgetting quotes around text or mixing AND with city names (`city = 'A' AND city = 'B'` returns nothing).

### Q13 ⭐⭐⭐ 🟡 In what order does SQL actually run the clauses FROM, WHERE, SELECT, ORDER BY and LIMIT? Why does the order matter?
**Asked at:** Service MNC (a Cognizant interview report mentions SQL order of execution); also common elsewhere.
**What the interviewer is checking:** Do you know SQL does not run in the order you type it.
**Say this in the interview:** I write SELECT first, but the database runs FROM, then WHERE, then SELECT, then ORDER BY, and LIMIT last.
**Explain simply:**
- Order of running: **FROM** (pick the table) -> **WHERE** (filter rows) -> **GROUP BY** -> **HAVING** -> **SELECT** (compute columns, aliases) -> **DISTINCT** -> **ORDER BY** (sort) -> **LIMIT/OFFSET** (cut).
- So WHERE cannot see SELECT aliases, but ORDER BY can.
- Filtering early (WHERE) shrinks data before expensive steps; LIMIT after ORDER BY means top-N is sorted first.
**Example:** From 8 employees: WHERE keeps 5 earning above 50,000, SELECT computes annual pay, ORDER BY sorts, LIMIT 2 keeps the top two.
**SQL:**
```sql
SELECT emp_name, salary * 12 AS annual_pay
FROM Employees           -- 1. FROM
WHERE salary > 50000      -- 2. WHERE
ORDER BY annual_pay DESC, emp_id  -- 4. ORDER BY (alias is known now)
LIMIT 2;                  -- 5. LIMIT (SELECT is step 3)
```
**Output:**

| emp_name | annual_pay |
|---|---|
| Anita Sharma | 1080000 |
| Priya Nair | 1080000 |
**Edge cases:** Real optimisers may reorder internally, but results behave as if this order holds. Window functions run after WHERE/GROUP BY/HAVING, before ORDER BY.
**Likely follow-ups:**
- Where do aggregates filter? HAVING runs after GROUP BY.
- Why alias fails in WHERE? Q14.
**Common mistakes:** Assuming SELECT runs first, or putting LIMIT before ORDER BY mentally.

### Q14 ⭐⭐⭐ 🟡 Why can you use a column alias in ORDER BY but not in WHERE?
**Asked at:** Service MNC and analytics-firm interviews (execution-order follow-up; no company-specific report found).
**What the interviewer is checking:** Applying the execution order to a real error.
**Say this in the interview:** WHERE runs before SELECT, so the alias does not exist yet. ORDER BY runs after SELECT, so it knows the alias.
**Explain simply:**
- The alias is born in the SELECT step.
- WHERE (step 2) is evaluated earlier, so strict databases (PostgreSQL, SQL Server, Oracle) say 'column does not exist'.
- Fix: repeat the expression in WHERE, or wrap the query in a subquery or CTE (a named temporary result) and filter outside.
- Caveat: SQLite, MySQL (partly) and DuckDB are lenient and allow some alias use in WHERE; do not rely on it.
**Example:** annual_pay = salary x 12. To keep annual_pay above 700,000 you cannot write that alias in WHERE on PostgreSQL.
**SQL:**
```sql
-- portable fix: filter in an outer query
SELECT emp_name, annual_pay
FROM (SELECT emp_name, salary * 12 AS annual_pay FROM Employees) t
WHERE annual_pay > 700000
ORDER BY annual_pay DESC;
```
**Output:**

| emp_name | annual_pay |
|---|---|
| Anita Sharma | 1080000 |
| Priya Nair | 1080000 |
| Arjun Mehta | 864000 |
| Amit Kumar | 780000 |
**Alias in ORDER BY works everywhere:**
```sql
SELECT emp_name, salary * 12 AS annual_pay FROM Employees ORDER BY annual_pay DESC, emp_id LIMIT 3;
```

| emp_name | annual_pay |
|---|---|
| Anita Sharma | 1080000 |
| Priya Nair | 1080000 |
| Arjun Mehta | 864000 |
**Edge cases:** `WHERE annual_pay > 700000` directly is an error on PostgreSQL/SQL Server/Oracle (not run here; this SQLite engine happens to accept it). In SQL Server ORDER BY alias works too.
**Likely follow-ups:**
- Can HAVING use alias? MySQL yes, PostgreSQL no.
- Other fix? CTE: `WITH t AS (...) SELECT ... WHERE`.
**Common mistakes:** Trusting that the query works because your local database is lenient.

### Q15 ⭐⭐⭐ 🟡 Write a query to find the second-highest salary in the Employees table using DISTINCT, ORDER BY and LIMIT/OFFSET. What should it return if there is only one salary?
**Asked at:** Service MNCs (second/Nth highest salary is a staple in the research notes) and general SQL guides.
**What the interviewer is checking:** Handling duplicates with DISTINCT, ORDER BY and OFFSET.
**Say this in the interview:** I take the distinct salaries, sort them descending, skip the first one and take the next. If there is only one salary, a plain query returns no row, so I wrap it in a subquery to return NULL.
**Explain simply:**
- **DISTINCT** so that two people at 90,000 count as one salary level.
- **OFFSET 1** skips the highest, **LIMIT 1** takes the next.
- No second salary: the query returns an empty result; wrapping it in `SELECT (subquery)` turns that into a single NULL, which is what many interviewers expect.
**Example:** Salaries: 90,000 (two people), 72,000, 65,000... The second-highest is 72,000, not 90,000.
**Sample data:** `Employees` (8 rows; manager_id blank = NULL, i.e. no manager):

| emp_id | emp_name | department | city | salary | manager_id | hire_date |
|---|---|---|---|---|---|---|
| 1 | Anita Sharma | HR | Hyderabad | 90000 | NULL | 2020-03-10 |
| 2 | Arjun Mehta | Sales | Bengaluru | 72000 | 1 | 2021-07-01 |
| 3 | Sneha Iyer | HR | Pune | 48000 | 1 | 2022-11-20 |
| 4 | Rahul Verma | Sales | Hyderabad | 55000 | 2 | 2023-02-14 |
| 5 | Priya Nair | IT | Bengaluru | 90000 | 1 | 2023-08-01 |
| 6 | Amit Kumar | IT | Pune | 65000 | 5 | 2023-12-31 |
| 7 | Kavya Reddy | Finance | Hyderabad | 50000 | 1 | 2024-01-15 |
| 8 | Vikram Singh | Sales | Chennai | 38000 | 2 | 2024-04-01 |
**SQL:**
```sql
SELECT DISTINCT salary
FROM Employees
ORDER BY salary DESC
LIMIT 1 OFFSET 1;
```
SQL Server: `ORDER BY salary DESC OFFSET 1 ROWS FETCH NEXT 1 ROWS ONLY`. MySQL also accepts `LIMIT 1, 1`. Not run here.
**Output:**

| salary |
|---|
| 72000 |
**Safe version when only one salary exists (table Pay1 has only 70,000 twice):**
```sql
SELECT (SELECT DISTINCT salary FROM Pay1 ORDER BY salary DESC LIMIT 1 OFFSET 1) AS second_highest;
```

| second_highest |
|---|
| NULL |
**pandas equivalent:**
```python
emp = pd.read_sql('SELECT * FROM Employees', conn)  # or pd.read_csv(...)
vals = sorted(emp['salary'].unique(), reverse=True)
res = pd.DataFrame({'salary': vals[1:2]})
```
Same result as the SQL (checked by running both).
**Edge cases:** Empty table or one distinct salary gives no row (or NULL when wrapped). NULL salaries sort last on DESC in some databases; filter them out with `WHERE salary IS NOT NULL`.
**Likely follow-ups:**
- Another way? DENSE_RANK() (Part 5) or `MAX(salary) WHERE salary < (SELECT MAX(salary))`.
- Per department? Needs window functions.
**Common mistakes:** Leaving out DISTINCT (Q20) or returning an empty set instead of NULL.

### Q16 ⭐⭐⭐ 🟡 Write a query to find the 3rd highest (Nth highest) salary using ORDER BY with LIMIT/OFFSET. What goes wrong when two people share the same salary?
**Asked at:** Service MNCs (Dataquest-style 3rd highest salary question); no company-specific report found.
**What the interviewer is checking:** Generalising to Nth and understanding ties.
**Say this in the interview:** For the Nth highest I use DISTINCT, ORDER BY DESC, and OFFSET N-1. Without DISTINCT, two people sharing a salary use up two positions, so the answer is wrong.
**Explain simply:**
- Nth highest = skip N-1 rows, then take one: for 3rd, `OFFSET 2`.
- With ties, the answer depends on whether you count rows or salary levels. DISTINCT counts levels.
**Example:** Salaries 90k, 90k, 72k, 65k: the 3rd highest salary is 65,000. Without DISTINCT the query says 72,000.
**Sample data:** `Employees` (8 rows; manager_id blank = NULL, i.e. no manager):

| emp_id | emp_name | department | city | salary | manager_id | hire_date |
|---|---|---|---|---|---|---|
| 1 | Anita Sharma | HR | Hyderabad | 90000 | NULL | 2020-03-10 |
| 2 | Arjun Mehta | Sales | Bengaluru | 72000 | 1 | 2021-07-01 |
| 3 | Sneha Iyer | HR | Pune | 48000 | 1 | 2022-11-20 |
| 4 | Rahul Verma | Sales | Hyderabad | 55000 | 2 | 2023-02-14 |
| 5 | Priya Nair | IT | Bengaluru | 90000 | 1 | 2023-08-01 |
| 6 | Amit Kumar | IT | Pune | 65000 | 5 | 2023-12-31 |
| 7 | Kavya Reddy | Finance | Hyderabad | 50000 | 1 | 2024-01-15 |
| 8 | Vikram Singh | Sales | Chennai | 38000 | 2 | 2024-04-01 |
**SQL:**
```sql
SELECT DISTINCT salary
FROM Employees
ORDER BY salary DESC
LIMIT 1 OFFSET 2;
```
Replace the 2 with N-1. MySQL cannot do `OFFSET N-1` inside LIMIT; compute it in the app or use a stored function. Not run here.
**Output:**

| salary |
|---|
| 65000 |
**Wrong: without DISTINCT the two 90,000 rows take up places 1 and 2:**
```sql
SELECT salary FROM Employees ORDER BY salary DESC LIMIT 1 OFFSET 2;
```

| salary |
|---|
| 72000 |
**pandas equivalent:**
```python
emp = pd.read_sql('SELECT * FROM Employees', conn)  # or pd.read_csv(...)
vals = sorted(emp['salary'].unique(), reverse=True)
res = pd.DataFrame({'salary': vals[2:3]})
```
Same result as the SQL (checked by running both).
**Edge cases:** If fewer than N distinct salaries exist, nothing comes back; wrap in a subquery for NULL. If the business wants the 3rd person (not salary level) then skip DISTINCT but add a tie-breaker.
**Likely follow-ups:**
- Handle N dynamically? Use a window function DENSE_RANK in Part 5.
- Why not MAX on a subquery? It does not scale to 3rd, 4th.
**Common mistakes:** Forgetting DISTINCT or using OFFSET N instead of N-1.

### Q17 ⭐⭐⭐ 🟡 Write a query to list employees hired after 1 Jan 2023, sorted by salary from highest to lowest.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Combining WHERE and ORDER BY and date comparison.
**Say this in the interview:** I filter first with WHERE hire_date > '2023-01-01', then sort by salary descending.
**Explain simply:**
- WHERE chooses rows; ORDER BY arranges the chosen rows.
- `>` means strictly after; someone hired on 1 Jan 2023 itself would be excluded. Use `>=` if they should count.
- Date text in `'YYYY-MM-DD'` format sorts and compares correctly.
**Example:** Recent joiners sorted by pay for onboarding budget: 5 people joined after 1 Jan 2023, highest earner is Priya (90,000).
**Sample data:** `Employees` (8 rows; manager_id blank = NULL, i.e. no manager):

| emp_id | emp_name | department | city | salary | manager_id | hire_date |
|---|---|---|---|---|---|---|
| 1 | Anita Sharma | HR | Hyderabad | 90000 | NULL | 2020-03-10 |
| 2 | Arjun Mehta | Sales | Bengaluru | 72000 | 1 | 2021-07-01 |
| 3 | Sneha Iyer | HR | Pune | 48000 | 1 | 2022-11-20 |
| 4 | Rahul Verma | Sales | Hyderabad | 55000 | 2 | 2023-02-14 |
| 5 | Priya Nair | IT | Bengaluru | 90000 | 1 | 2023-08-01 |
| 6 | Amit Kumar | IT | Pune | 65000 | 5 | 2023-12-31 |
| 7 | Kavya Reddy | Finance | Hyderabad | 50000 | 1 | 2024-01-15 |
| 8 | Vikram Singh | Sales | Chennai | 38000 | 2 | 2024-04-01 |
**SQL:**
```sql
SELECT emp_name, hire_date, salary
FROM Employees
WHERE hire_date > '2023-01-01'
ORDER BY salary DESC, emp_id;
```
**Output:**

| emp_name | hire_date | salary |
|---|---|---|
| Priya Nair | 2023-08-01 | 90000 |
| Amit Kumar | 2023-12-31 | 65000 |
| Rahul Verma | 2023-02-14 | 55000 |
| Kavya Reddy | 2024-01-15 | 50000 |
| Vikram Singh | 2024-04-01 | 38000 |
**pandas equivalent:**
```python
emp = pd.read_sql('SELECT * FROM Employees', conn)  # or pd.read_csv(...)
emp['hire_date'] = pd.to_datetime(emp['hire_date'])
res = emp.loc[emp['hire_date'] > '2023-01-01'].sort_values(['salary', 'emp_id'], ascending=[False, True])[['emp_name', 'hire_date', 'salary']]
res = res.assign(hire_date=res['hire_date'].dt.strftime('%Y-%m-%d'))
```
Same result as the SQL (checked by running both).
**Edge cases:** NULL hire_date is excluded. In SQL Server the literal may need `CAST('2023-01-01' AS date)` if the column type is odd. Add emp_id to settle salary ties.
**Likely follow-ups:**
- Include 1 Jan? Use `>=`.
- Latest first instead? ORDER BY hire_date DESC.
**Common mistakes:** Putting ORDER BY before WHERE.

### Q18 ⭐⭐⭐ 🟡 Write a query to sort employees by department A to Z and, inside each department, by salary highest first. How does ORDER BY with several columns work?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Multi-column ORDER BY.
**Say this in the interview:** ORDER BY department ASC, salary DESC sorts by department first. Salary only matters to break ties within the same department.
**Explain simply:**
- SQL sorts by the first column; only rows with equal values on it are then sorted by the second.
- Each column gets its own ASC/DESC.
- Think of a phone book: surname first, then first name.
**Example:** A department-wise pay list: Finance, HR, IT, Sales, each with the highest earner on top.
**Sample data:** `Employees` (8 rows; manager_id blank = NULL, i.e. no manager):

| emp_id | emp_name | department | city | salary | manager_id | hire_date |
|---|---|---|---|---|---|---|
| 1 | Anita Sharma | HR | Hyderabad | 90000 | NULL | 2020-03-10 |
| 2 | Arjun Mehta | Sales | Bengaluru | 72000 | 1 | 2021-07-01 |
| 3 | Sneha Iyer | HR | Pune | 48000 | 1 | 2022-11-20 |
| 4 | Rahul Verma | Sales | Hyderabad | 55000 | 2 | 2023-02-14 |
| 5 | Priya Nair | IT | Bengaluru | 90000 | 1 | 2023-08-01 |
| 6 | Amit Kumar | IT | Pune | 65000 | 5 | 2023-12-31 |
| 7 | Kavya Reddy | Finance | Hyderabad | 50000 | 1 | 2024-01-15 |
| 8 | Vikram Singh | Sales | Chennai | 38000 | 2 | 2024-04-01 |
**SQL:**
```sql
SELECT department, emp_name, salary
FROM Employees
ORDER BY department ASC, salary DESC;
```
**Output:**

| department | emp_name | salary |
|---|---|---|
| Finance | Kavya Reddy | 50000 |
| HR | Anita Sharma | 90000 |
| HR | Sneha Iyer | 48000 |
| IT | Priya Nair | 90000 |
| IT | Amit Kumar | 65000 |
| Sales | Arjun Mehta | 72000 |
| Sales | Rahul Verma | 55000 |
| Sales | Vikram Singh | 38000 |
**pandas equivalent:**
```python
emp = pd.read_sql('SELECT * FROM Employees', conn)  # or pd.read_csv(...)
res = emp.sort_values(['department', 'salary'], ascending=[True, False], kind='stable')[['department', 'emp_name', 'salary']]
```
Same result as the SQL (checked by running both).
**Edge cases:** Ties on both columns have no guaranteed order; add emp_id. NULL departments cluster at one end (Q35).
**Likely follow-ups:**
- Sort by column position? Possible but not recommended (Q40).
- Mixed sort in pandas? Pass a list to `ascending`.
**Common mistakes:** Thinking `ORDER BY department, salary DESC` applies DESC to both columns; DESC only affects the column it follows.

### Q19 ⭐⭐⭐ 🟡 What does `SELECT DISTINCT department, city` return? Does DISTINCT apply to one column or to the whole row?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** DISTINCT applies to the whole row.
**Say this in the interview:** DISTINCT works on the whole combination of selected columns, not on one column. It returns every unique department-city pair.
**Explain simply:**
- It compares the full row you selected.
- The department HR appears twice if it is in two cities, because the pairs differ.
- To get distinct values of one column, select only that column.
**Example:** Office footprint: where does each department operate?
**Sample data:** `Employees` (8 rows; manager_id blank = NULL, i.e. no manager):

| emp_id | emp_name | department | city | salary | manager_id | hire_date |
|---|---|---|---|---|---|---|
| 1 | Anita Sharma | HR | Hyderabad | 90000 | NULL | 2020-03-10 |
| 2 | Arjun Mehta | Sales | Bengaluru | 72000 | 1 | 2021-07-01 |
| 3 | Sneha Iyer | HR | Pune | 48000 | 1 | 2022-11-20 |
| 4 | Rahul Verma | Sales | Hyderabad | 55000 | 2 | 2023-02-14 |
| 5 | Priya Nair | IT | Bengaluru | 90000 | 1 | 2023-08-01 |
| 6 | Amit Kumar | IT | Pune | 65000 | 5 | 2023-12-31 |
| 7 | Kavya Reddy | Finance | Hyderabad | 50000 | 1 | 2024-01-15 |
| 8 | Vikram Singh | Sales | Chennai | 38000 | 2 | 2024-04-01 |
**SQL:**
```sql
SELECT DISTINCT department, city
FROM Employees
ORDER BY department, city;
```
**Output:**

| department | city |
|---|---|
| Finance | Hyderabad |
| HR | Hyderabad |
| HR | Pune |
| IT | Bengaluru |
| IT | Pune |
| Sales | Bengaluru |
| Sales | Chennai |
| Sales | Hyderabad |
**pandas equivalent:**
```python
emp = pd.read_sql('SELECT * FROM Employees', conn)  # or pd.read_csv(...)
res = emp[['department', 'city']].drop_duplicates().sort_values(['department', 'city'])
```
Same result as the SQL (checked by running both).
**Edge cases:** NULL pairs count as equal to each other for DISTINCT. `SELECT DISTINCT a, b` is not `DISTINCT(a), b`: the brackets do nothing.
**Likely follow-ups:**
- Unique cities per department count? GROUP BY department + COUNT(DISTINCT city).
- Distinct on a single column only? Select just it.
**Common mistakes:** Expecting department to appear once, and writing `DISTINCT(department), city`.

### Q20 ⭐⭐⭐ 🟡 Why can the second-highest salary query return the wrong answer without DISTINCT? Show it with salaries 90, 90, 80.
**Asked at:** Service MNC style Nth-highest follow-up (no company-specific report found).
**What the interviewer is checking:** Whether you notice that duplicates break position-based logic.
**Say this in the interview:** With salaries 90, 90, 80, skipping one row lands on the other 90, which is wrong. DISTINCT collapses duplicates first, so offset 1 correctly gives 80.
**Explain simply:**
- OFFSET counts rows, not salary levels.
- Two people earning the top salary occupy rows 1 and 2.
- DISTINCT makes each salary level one row.
**Example:** Two managers at 90,000 and one analyst at 80,000: the true second-highest salary is 80,000.
**Sample data:** table `Pay3` (salaries 90, 90, 80):

| emp_name | salary |
|---|---|
| A | 90 |
| B | 90 |
| C | 80 |
**SQL:**
```sql
SELECT DISTINCT salary
FROM Pay3
ORDER BY salary DESC
LIMIT 1 OFFSET 1;
```
**Output:**

| salary |
|---|
| 80 |
**Wrong - no DISTINCT returns 90:**
```sql
SELECT salary FROM Pay3 ORDER BY salary DESC LIMIT 1 OFFSET 1;
```

| salary |
|---|
| 90 |
**pandas equivalent:**
```python
res = pd.DataFrame({'salary': sorted(pay3['salary'].unique(), reverse=True)[1:2]})
```
Same result as the SQL (checked by running both).
**Edge cases:** If you really want the second-highest person (not level), the first query is right, but you must then say how ties are handled.
**Likely follow-ups:**
- Why not RANK? RANK leaves gaps; DENSE_RANK matches DISTINCT behaviour.
- All equal salaries? No second level, NULL/empty.
**Common mistakes:** Dropping DISTINCT because it passed on data with no duplicates.

### Q21 ⭐⭐ 🟢 What is a column alias? Write a query that shows `emp_name` as 'Employee Name' and annual salary (monthly salary x 12) as 'Annual Pay'.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Aliases and calculated columns.
**Say this in the interview:** An alias is a temporary nickname for a column or expression, written with AS. It only changes the output heading, not the table.
**Explain simply:**
- `AS` is optional in most databases but clearer.
- Use quotes when the alias has spaces: double quotes in standard SQL/PostgreSQL/SQLite, backticks in MySQL, square brackets (or quotes) in SQL Server.
- Calculated columns like `salary * 12` get an ugly default name, so alias them.
**Example:** Monthly salary 72,000 becomes annual pay 864,000 on the offer sheet.
**Sample data:** `Employees` (8 rows; manager_id blank = NULL, i.e. no manager):

| emp_id | emp_name | department | city | salary | manager_id | hire_date |
|---|---|---|---|---|---|---|
| 1 | Anita Sharma | HR | Hyderabad | 90000 | NULL | 2020-03-10 |
| 2 | Arjun Mehta | Sales | Bengaluru | 72000 | 1 | 2021-07-01 |
| 3 | Sneha Iyer | HR | Pune | 48000 | 1 | 2022-11-20 |
| 4 | Rahul Verma | Sales | Hyderabad | 55000 | 2 | 2023-02-14 |
| 5 | Priya Nair | IT | Bengaluru | 90000 | 1 | 2023-08-01 |
| 6 | Amit Kumar | IT | Pune | 65000 | 5 | 2023-12-31 |
| 7 | Kavya Reddy | Finance | Hyderabad | 50000 | 1 | 2024-01-15 |
| 8 | Vikram Singh | Sales | Chennai | 38000 | 2 | 2024-04-01 |
**SQL:**
```sql
SELECT emp_name AS "Employee Name",
       salary * 12 AS "Annual Pay"
FROM Employees
ORDER BY emp_id
LIMIT 4;
```
MySQL: use backticks (`Employee Name`). SQL Server: [Employee Name] or "Employee Name". Not run here.
**Output:**

| Employee Name | Annual Pay |
|---|---|
| Anita Sharma | 1080000 |
| Arjun Mehta | 864000 |
| Sneha Iyer | 576000 |
| Rahul Verma | 660000 |
**pandas equivalent:**
```python
emp = pd.read_sql('SELECT * FROM Employees', conn)  # or pd.read_csv(...)
res = emp.assign(**{'Annual Pay': emp['salary'] * 12}).rename(columns={'emp_name': 'Employee Name'})[['Employee Name', 'Annual Pay']].head(4)
```
Same result as the SQL (checked by running both).
**Edge cases:** Assumes salary is monthly, as the question says. A NULL salary gives NULL annual pay. Aliases cannot be used in WHERE (Q14).
**Likely follow-ups:**
- Alias for a table? `FROM Employees e`, used in joins.
- Same alias twice? Avoid, it confuses ORDER BY.
**Common mistakes:** Using single quotes for the alias (fails in some databases) or putting the alias in WHERE.

### Q22 ⭐⭐ 🟢 What do the comparison operators `=`, `<>`, `!=`, `>=` and `<=` mean? Write a query for employees not in the 'HR' department.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know the basic comparison symbols and that `<>` and `!=` mean the same thing.
**Say this in the interview:** "`=` means equal, `<>` and `!=` both mean not equal, and `>=` / `<=` mean greater-or-equal / less-or-equal. To exclude HR I write `WHERE department <> 'HR'`."
**Explain simply:**
- **Comparison operator** = a symbol that compares two values and answers true or false for each row.
- `=` equal, `<>` not equal (the official SQL standard), `!=` not equal (works in almost every database, including MySQL, PostgreSQL, SQL Server, SQLite), `>=` greater than or equal, `<=` less than or equal.
- Text goes in single quotes (`'HR'`); numbers do not.
- Catch: rows where department is **NULL** (unknown) are also dropped by `<>` - see Q36.
**Example:** In an 8-person company, "everyone outside HR" should be 6 people if 2 are in HR. Here Sam has no department recorded, so the query returns 5, not 6.
**Sample data:** `employees`

| emp_id | emp_name | department | city | salary | hire_date |
|---|---|---|---|---|---|
| 1 | Asha | HR | Pune | 45000 | 2021-06-15 |
| 2 | Ravi | IT | Hyderabad | 80000 | 2020-03-01 |
| 3 | Meena | Sales | Pune | 60000 | 2023-01-10 |
| 4 | Karan | IT | Bengaluru | 80000 | 2024-04-01 |
| 5 | Divya | Finance | Hyderabad | 70000 | 2022-09-20 |
| 6 | Sam | NULL | Pune | 50000 | 2024-02-12 |
| 7 | Neha | HR | Hyderabad | 52000 | 2024-04-01 |
| 8 | Omar | Sales | Bengaluru | 70000 | 2023-11-05 |
**SQL:**
```sql
SELECT emp_id, emp_name, department
FROM employees
WHERE department <> 'HR';
```
**Output:**
| emp_id | emp_name | department |
|---|---|---|
| 2 | Ravi | IT |
| 3 | Meena | Sales |
| 4 | Karan | IT |
| 5 | Divya | Finance |
| 8 | Omar | Sales |
**pandas equivalent:**
```python
# employees / candidates / orders = the tables above loaded as DataFrames
result = employees.loc[employees.department.notna() & (employees.department != 'HR'),
                      ['emp_id', 'emp_name', 'department']]
```
(Checked: the pandas result is identical to the SQL output.)
**Edge cases:** Sam (NULL department) is missing from the output. To keep Sam add `OR department IS NULL`. In pandas, `!= 'HR'` keeps NaN rows, unlike SQL, so I added `notna()` to match.
**Likely follow-ups:**
- Is `<>` the same as `!=`? Yes, same result; `<>` is the ISO standard, `!=` is a common extension.
- Can I compare text with `>`? Yes, it compares alphabetically (depends on collation).
**Common mistakes:** Writing `= NULL` or `<> NULL` (never works, use `IS NULL`); using double quotes for text (many databases read them as column names); forgetting NULL rows disappear.

### Q23 ⭐⭐ 🟢 How do you write NOT IN, NOT BETWEEN and NOT LIKE? Give one example of each on the Employees table.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** That you can negate the three pattern/list filters with the word NOT in front of the operator.
**Say this in the interview:** "You put NOT before the operator: `NOT IN (list)`, `NOT BETWEEN a AND b`, `NOT LIKE pattern`. Each one keeps the rows that fail the original test."
**Explain simply:**
- `IN (...)` = matches any value in a list; `NOT IN` = matches none of them.
- `BETWEEN a AND b` = from a to b **including both ends**; `NOT BETWEEN` = below a or above b.
- `LIKE` = pattern match; `%` means "any number of characters", `_` means "exactly one character". `NOT LIKE` flips it.
- All three drop NULL rows, because comparing NULL gives "unknown", not true.
**Example:** Salary NOT BETWEEN 50,000 and 70,000 finds people paid under 50k or over 70k - useful to spot pay outliers.
**Sample data:** `employees`

| emp_id | emp_name | department | city | salary | hire_date |
|---|---|---|---|---|---|
| 1 | Asha | HR | Pune | 45000 | 2021-06-15 |
| 2 | Ravi | IT | Hyderabad | 80000 | 2020-03-01 |
| 3 | Meena | Sales | Pune | 60000 | 2023-01-10 |
| 4 | Karan | IT | Bengaluru | 80000 | 2024-04-01 |
| 5 | Divya | Finance | Hyderabad | 70000 | 2022-09-20 |
| 6 | Sam | NULL | Pune | 50000 | 2024-02-12 |
| 7 | Neha | HR | Hyderabad | 52000 | 2024-04-01 |
| 8 | Omar | Sales | Bengaluru | 70000 | 2023-11-05 |
**SQL:**
```sql
-- NOT IN
SELECT emp_name, department FROM employees
WHERE department NOT IN ('HR', 'IT');
-- NOT BETWEEN
SELECT emp_name, salary FROM employees
WHERE salary NOT BETWEEN 50000 AND 70000;
-- NOT LIKE
SELECT emp_name FROM employees
WHERE emp_name NOT LIKE 'A%';
```
**Output:**
NOT IN

| emp_name | department |
|---|---|
| Meena | Sales |
| Divya | Finance |
| Omar | Sales |

NOT BETWEEN

| emp_name | salary |
|---|---|
| Asha | 45000 |
| Ravi | 80000 |
| Karan | 80000 |

NOT LIKE

| emp_name |
|---|
| Ravi |
| Meena |
| Karan |
| Divya |
| Sam |
| Neha |
| Omar |
**pandas equivalent:**
```python
# employees / candidates / orders = the tables above loaded as DataFrames
result = employees.loc[employees.department.notna() & ~employees.department.isin(['HR', 'IT']),
                      ['emp_name', 'department']]
```
(Checked: the pandas result is identical to the SQL output.)
```python
# employees / candidates / orders = the tables above loaded as DataFrames
result = employees.loc[~employees.salary.between(50000, 70000), ['emp_name', 'salary']]
```
(Checked: the pandas result is identical to the SQL output.)
```python
# employees / candidates / orders = the tables above loaded as DataFrames
result = employees.loc[~employees.emp_name.str.startswith('A'), ['emp_name']]
```
(Checked: the pandas result is identical to the SQL output.)
**Edge cases:** Sam (NULL department) is excluded from the NOT IN result; 50,000 and 70,000 themselves are excluded from NOT BETWEEN because the range ends are inclusive. If the NOT IN list contains a NULL, you get zero rows (Q37).
**Likely follow-ups:**
- Is `NOT BETWEEN` inclusive? The inner range is inclusive, so the boundary values are NOT returned.
- Is `NOT x = 5` valid? Yes, same as `x <> 5`.
**Common mistakes:** Writing `department NOT = 'HR'`; putting NOT in the wrong place (`department IS NOT IN`); ignoring that NULL rows vanish.

### Q24 ⭐⭐ 🟢 What is the difference between `=` and `LIKE` when filtering text?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** That `=` is an exact match while `LIKE` is a pattern match with wildcards.
**Say this in the interview:** "`=` needs the whole value to match exactly. `LIKE` lets me search a pattern: `%` for any characters, `_` for exactly one. So `LIKE 'A%'` finds names starting with A."
**Explain simply:**
- **Wildcard** = a stand-in character: `%` = zero or more characters, `_` = exactly one character.
- `=` is faster and can use an index; `LIKE '%abc'` (leading `%`) usually forces a full scan of the table.
- Case rules differ by database: SQLite `LIKE` ignores case for English letters; MySQL and SQL Server depend on the column collation (default is case-insensitive); PostgreSQL `LIKE` is case-sensitive (use `ILIKE` for ignoring case).
- To search for a real `%` use `ESCAPE`, e.g. `LIKE '50\%' ESCAPE '\'`.
**Example:** `city = 'Pune'` finds exactly Pune. `emp_name LIKE '_a%'` finds names whose second letter is a: Karan, Ravi, Sam.
**Sample data:** `employees`

| emp_id | emp_name | department | city | salary | hire_date |
|---|---|---|---|---|---|
| 1 | Asha | HR | Pune | 45000 | 2021-06-15 |
| 2 | Ravi | IT | Hyderabad | 80000 | 2020-03-01 |
| 3 | Meena | Sales | Pune | 60000 | 2023-01-10 |
| 4 | Karan | IT | Bengaluru | 80000 | 2024-04-01 |
| 5 | Divya | Finance | Hyderabad | 70000 | 2022-09-20 |
| 6 | Sam | NULL | Pune | 50000 | 2024-02-12 |
| 7 | Neha | HR | Hyderabad | 52000 | 2024-04-01 |
| 8 | Omar | Sales | Bengaluru | 70000 | 2023-11-05 |
**SQL:**
```sql
SELECT emp_name, city FROM employees WHERE city = 'Pune';
SELECT emp_name FROM employees WHERE emp_name LIKE '_a%';
```
**Output:**
Exact match

| emp_name | city |
|---|---|
| Asha | Pune |
| Meena | Pune |
| Sam | Pune |

Pattern match

| emp_name |
|---|
| Ravi |
| Karan |
| Sam |
**pandas equivalent:**
```python
# employees / candidates / orders = the tables above loaded as DataFrames
result = employees.loc[employees.city == 'Pune', ['emp_name', 'city']]
```
(Checked: the pandas result is identical to the SQL output.)
```python
# employees / candidates / orders = the tables above loaded as DataFrames
result = employees.loc[employees.emp_name.str.match('.a'), ['emp_name']]
```
(Checked: the pandas result is identical to the SQL output.)
**Edge cases:** Trailing spaces: `'Pune '` is not equal to `'Pune'` in most databases (SQL Server and MySQL may ignore trailing spaces in `=`, a known quirk). NULL never matches either operator. `LIKE` with no wildcard behaves like `=` but with the case rules above.
**Likely follow-ups:**
- Can I use `=` with `%`? No, `%` is then just a literal character.
- How to search case-insensitively everywhere? `LOWER(col) LIKE LOWER('pattern')`.
**Common mistakes:** Using `= 'A%'` expecting a pattern; assuming `LIKE` is case-sensitive everywhere; leading `%` on a huge table.

### Q25 ⭐⭐ 🟢 What are the differences between LIKE, IN and BETWEEN, and when do you use each?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** That you can pick the right tool: a list (IN), a range (BETWEEN) or a text pattern (LIKE).
**Say this in the interview:** "IN checks against a list of exact values, BETWEEN checks a range with both ends included, and LIKE checks a text pattern. I use IN for a few known values, BETWEEN for numbers and dates in a range, LIKE when I only know part of the text."
**Explain simply:**
- | Operator | Use it for | Example |
|---|---|---|
| `IN` | a short list of exact values | `department IN ('IT','Sales')` |
| `BETWEEN` | a range, **inclusive** of both ends | `salary BETWEEN 60000 AND 80000` |
| `LIKE` | partial text match | `emp_name LIKE '%a'` |
- `IN` is just shorthand for several `OR` conditions; `BETWEEN a AND b` is shorthand for `>= a AND <= b`.
- Order matters in `BETWEEN`: `BETWEEN 80000 AND 60000` returns nothing.
**Example:** HR wants IT or Sales staff paid 60k-80k whose name ends in "a": the three operators combine with AND.
**Sample data:** `employees`

| emp_id | emp_name | department | city | salary | hire_date |
|---|---|---|---|---|---|
| 1 | Asha | HR | Pune | 45000 | 2021-06-15 |
| 2 | Ravi | IT | Hyderabad | 80000 | 2020-03-01 |
| 3 | Meena | Sales | Pune | 60000 | 2023-01-10 |
| 4 | Karan | IT | Bengaluru | 80000 | 2024-04-01 |
| 5 | Divya | Finance | Hyderabad | 70000 | 2022-09-20 |
| 6 | Sam | NULL | Pune | 50000 | 2024-02-12 |
| 7 | Neha | HR | Hyderabad | 52000 | 2024-04-01 |
| 8 | Omar | Sales | Bengaluru | 70000 | 2023-11-05 |
**SQL:**
```sql
SELECT emp_name, department, salary
FROM employees
WHERE department IN ('IT', 'Sales')
  AND salary BETWEEN 60000 AND 80000
  AND emp_name LIKE '%a';
```
**Output:**
| emp_name | department | salary |
|---|---|---|
| Meena | Sales | 60000 |
**pandas equivalent:**
```python
# employees / candidates / orders = the tables above loaded as DataFrames
result = employees.loc[employees.department.isin(['IT', 'Sales'])
                      & employees.salary.between(60000, 80000)
                      & employees.emp_name.str.endswith('a'),
                      ['emp_name', 'department', 'salary']]
```
(Checked: the pandas result is identical to the SQL output.)
**Edge cases:** `BETWEEN` with dates and timestamps can miss the last day (Q41). `IN` with a NULL in the list never matches NULL rows. Lists in `IN` can be a subquery.
**Likely follow-ups:**
- IN vs OR? Same result; IN is shorter and easier to read.
- Is BETWEEN inclusive in every database? Yes, in all the major ones.
**Common mistakes:** Thinking BETWEEN excludes the end values; reversing the range; using LIKE where IN or = would be faster.

### Q26 ⭐⭐ 🟢 What is the difference between WHERE and HAVING? (Only the basic idea here; deep dive is in Part 2.)
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** That you know WHERE filters rows before grouping and HAVING filters groups after grouping.
**Say this in the interview:** "WHERE filters individual rows before any grouping, so it cannot use aggregates like COUNT. HAVING filters the groups after GROUP BY, so it can."
**Explain simply:**
- **Aggregate** = a function that turns many rows into one number: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`.
- **GROUP BY** = bundle rows that share a value (e.g. same department) and calculate per bundle.
- Order of work: `FROM` -> `WHERE` (rows) -> `GROUP BY` -> `HAVING` (groups) -> `SELECT` -> `ORDER BY`.
- Rule of thumb: if the condition is about one row, use WHERE; if it is about a total or average, use HAVING.
**Example:** Step 1 WHERE drops anyone under 50,000. Step 2 groups the rest by department. Step 3 HAVING keeps only departments with at least 2 such people.
**Sample data:** `employees`

| emp_id | emp_name | department | city | salary | hire_date |
|---|---|---|---|---|---|
| 1 | Asha | HR | Pune | 45000 | 2021-06-15 |
| 2 | Ravi | IT | Hyderabad | 80000 | 2020-03-01 |
| 3 | Meena | Sales | Pune | 60000 | 2023-01-10 |
| 4 | Karan | IT | Bengaluru | 80000 | 2024-04-01 |
| 5 | Divya | Finance | Hyderabad | 70000 | 2022-09-20 |
| 6 | Sam | NULL | Pune | 50000 | 2024-02-12 |
| 7 | Neha | HR | Hyderabad | 52000 | 2024-04-01 |
| 8 | Omar | Sales | Bengaluru | 70000 | 2023-11-05 |
**SQL:**
```sql
SELECT department, COUNT(*) AS headcount, AVG(salary) AS avg_salary
FROM employees
WHERE salary >= 50000
GROUP BY department
HAVING COUNT(*) >= 2;
```
**Output:**
| department | headcount | avg_salary |
|---|---|---|
| IT | 2 | 80000.00 |
| Sales | 2 | 65000.00 |
**pandas equivalent:**
```python
# employees / candidates / orders = the tables above loaded as DataFrames
t = employees[employees.salary >= 50000]
g = t.groupby('department', dropna=True).agg(headcount=('emp_id', 'count'), avg_salary=('salary', 'mean')).reset_index()
result = g[g.headcount >= 2]
```
(Checked: the pandas result is identical to the SQL output.)
**Edge cases:** The NULL-department row (Sam) forms its own group in SQL (shown if it passes WHERE and HAVING); pandas drops it by default unless `dropna=False`. Here Sam's group has only 1 person, so it is removed by HAVING in both.
**Likely follow-ups:**
- Can HAVING be used without GROUP BY? Yes, the whole table is treated as one group.
- Can I put the filter on department in HAVING? Possible, but WHERE is faster because it removes rows earlier.
**Common mistakes:** Writing `WHERE COUNT(*) > 2` (error); filtering plain columns in HAVING; assuming HAVING runs before WHERE.

### Q27 ⭐⭐ 🟢 In a query, when do you put quotes around values? Compare filtering a number, a text and a date (e.g. salary = 50000, city = 'Pune', hire_date = '2024-04-01').
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** That you know numbers are bare, text and dates are quoted, and what goes wrong otherwise.
**Say this in the interview:** "Numbers have no quotes, text values go in single quotes, and dates also go in single quotes in the `YYYY-MM-DD` format. Without quotes the database thinks the text is a column name."
**Explain simply:**
- | Type | Quote? | Example |
|---|---|---|
| Number | No | `salary = 50000` |
| Text | Yes, single quotes | `city = 'Pune'` |
| Date | Yes, single quotes, `YYYY-MM-DD` | `hire_date = '2024-04-01'` |
- Single quotes are the SQL standard. Double quotes usually mean a column or table name (PostgreSQL, SQLite, SQL Server); MySQL also accepts them for text, which causes confusion.
- Dates: write `DATE '2024-04-01'` in PostgreSQL/Oracle/MySQL for safety; SQL Server and MySQL accept the plain string. Avoid regional formats like 01/04/2024 (is it 1 April or 4 January?).
- Quoting a number (`salary = '50000'`) often works by silent conversion, but it can disable an index and is poor style.
**Example:** Without quotes, `city = Pune` makes the database look for a column called Pune. I ran it in SQLite and got: `no such column: Pune`.
**Sample data:** `employees`

| emp_id | emp_name | department | city | salary | hire_date |
|---|---|---|---|---|---|
| 1 | Asha | HR | Pune | 45000 | 2021-06-15 |
| 2 | Ravi | IT | Hyderabad | 80000 | 2020-03-01 |
| 3 | Meena | Sales | Pune | 60000 | 2023-01-10 |
| 4 | Karan | IT | Bengaluru | 80000 | 2024-04-01 |
| 5 | Divya | Finance | Hyderabad | 70000 | 2022-09-20 |
| 6 | Sam | NULL | Pune | 50000 | 2024-02-12 |
| 7 | Neha | HR | Hyderabad | 52000 | 2024-04-01 |
| 8 | Omar | Sales | Bengaluru | 70000 | 2023-11-05 |
**SQL:**
```sql
SELECT emp_name FROM employees
WHERE salary = 80000
  AND city = 'Bengaluru'
  AND hire_date = '2024-04-01';
```
**Output:**
| emp_name |
|---|
| Karan |
**pandas equivalent:**
```python
# employees / candidates / orders = the tables above loaded as DataFrames
result = employees.loc[(employees.salary == 80000) & (employees.city == 'Bengaluru') & (employees.hire_date == '2024-04-01'), ['emp_name']]
```
(Checked: the pandas result is identical to the SQL output.)
**Edge cases:** A text value with an apostrophe needs doubling: `'O''Brien'`. Dates with a time part (`2024-04-01 09:30:00`) will not equal a plain date - compare with a range (Q41). Dates stored as text compare alphabetically; ISO format makes that correct.
**Likely follow-ups:**
- Why not use double quotes for text? In standard SQL they quote identifiers (names).
- How to filter between two dates? `>= '2024-01-01' AND < '2025-01-01'`.
**Common mistakes:** Forgetting quotes on text; adding quotes to numbers; using local date formats; using `=` on a date-time column.

### Q28 ⭐⭐ 🟢 What do the words table, row, column, primary key and query mean? Explain with a simple employee table.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** That you know the building blocks of a relational database in plain words.
**Say this in the interview:** "A table is a grid of data. Each row is one record, like one employee. Each column is one attribute, like salary. The primary key is a column whose value is unique for every row, like emp_id. A query is a question you ask the database in SQL."
**Explain simply:**
- **Table** = a named grid, like an Excel sheet: `employees`.
- **Row** (record) = one entry, e.g. Ravi with all his details. **Column** (field) = one property for all rows, e.g. `salary`.
- **Primary key** = a column (or combination) that uniquely identifies each row and is never NULL: `emp_id`. Two employees can share a name but never an `emp_id`.
- **Query** = a request, usually starting with `SELECT`, that reads data without changing it. Other statements change data: `INSERT`, `UPDATE`, `DELETE`.
**Example:** In the table below, 8 rows and 6 columns; `emp_id` is the primary key. Looking up emp_id = 2 returns exactly one row (Ravi).
**Sample data:** `employees`

| emp_id | emp_name | department | city | salary | hire_date |
|---|---|---|---|---|---|
| 1 | Asha | HR | Pune | 45000 | 2021-06-15 |
| 2 | Ravi | IT | Hyderabad | 80000 | 2020-03-01 |
| 3 | Meena | Sales | Pune | 60000 | 2023-01-10 |
| 4 | Karan | IT | Bengaluru | 80000 | 2024-04-01 |
| 5 | Divya | Finance | Hyderabad | 70000 | 2022-09-20 |
| 6 | Sam | NULL | Pune | 50000 | 2024-02-12 |
| 7 | Neha | HR | Hyderabad | 52000 | 2024-04-01 |
| 8 | Omar | Sales | Bengaluru | 70000 | 2023-11-05 |
**SQL:**
```sql
CREATE TABLE employees (
  emp_id     INTEGER PRIMARY KEY,   -- primary key: unique, not NULL
  emp_name   TEXT,
  department TEXT,
  city       TEXT,
  salary     INTEGER,
  hire_date  TEXT                   -- DATE type in PostgreSQL/MySQL/SQL Server
);
SELECT * FROM employees WHERE emp_id = 2;   -- a query
```
**Output:**
| emp_id | emp_name | department | city | salary | hire_date |
|---|---|---|---|---|---|
| 2 | Ravi | IT | Hyderabad | 80000 | 2020-03-01 |
**pandas equivalent:**
```python
# employees / candidates / orders = the tables above loaded as DataFrames
result = employees[employees.emp_id == 2]
```
(Checked: the pandas result is identical to the SQL output.)
**Edge cases:** A primary key cannot repeat or be NULL (inserting a duplicate `emp_id` raises an error). Tables can have a composite primary key (two columns together).
**Likely follow-ups:**
- Primary key vs foreign key? A foreign key in another table points to this table's primary key (e.g. `attendance.emp_id`).
- Can a table have two primary keys? No, only one, though it may span several columns.
**Common mistakes:** Calling a table a database; using a name or email as primary key (they can change or repeat); thinking a query always changes data.

### Q29 ⭐⭐ 🟢 Is SQL case-sensitive? Are keywords, table names and text values (e.g. 'sales' vs 'Sales') case-sensitive?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** That you separate "SQL language is forgiving" from "data comparisons depend on the database".
**Say this in the interview:** "SQL keywords like SELECT or select are not case-sensitive. Table and column names usually are not either, with some exceptions. Text values like 'sales' versus 'Sales' depend on the database collation: PostgreSQL and SQLite treat them as different with `=`, while MySQL and SQL Server treat them as equal by default."
**Explain simply:**
- **Keywords** (`SELECT`, `WHERE`) are never case-sensitive; convention is to write them in capitals for readability.
- **Table/column names**: case-insensitive in SQLite, SQL Server; PostgreSQL folds unquoted names to lower-case (but quoted `"Employees"` is exact); MySQL table names are case-sensitive on Linux, insensitive on Windows.
- **Text values**: depends on **collation** (the database rule for comparing and sorting text). Default `=` is case-insensitive in MySQL and SQL Server, case-sensitive in PostgreSQL, SQLite (for `=`) and Oracle.
- Safe habit: `LOWER(col) = LOWER('value')`, or clean the data on load.
**Example:** In SQLite I ran: `'sales' = 'Sales'` gives 0 (different), `'sales' LIKE 'Sales'` gives 1 (LIKE ignores case in SQLite), `LOWER('sales') = LOWER('Sales')` gives 1. Lower-case keywords also work: the query `select emp_name from employees where department = 'Sales';` ran fine.
**Sample data:** `employees`

| emp_id | emp_name | department | city | salary | hire_date |
|---|---|---|---|---|---|
| 1 | Asha | HR | Pune | 45000 | 2021-06-15 |
| 2 | Ravi | IT | Hyderabad | 80000 | 2020-03-01 |
| 3 | Meena | Sales | Pune | 60000 | 2023-01-10 |
| 4 | Karan | IT | Bengaluru | 80000 | 2024-04-01 |
| 5 | Divya | Finance | Hyderabad | 70000 | 2022-09-20 |
| 6 | Sam | NULL | Pune | 50000 | 2024-02-12 |
| 7 | Neha | HR | Hyderabad | 52000 | 2024-04-01 |
| 8 | Omar | Sales | Bengaluru | 70000 | 2023-11-05 |
**SQL:**
```sql
SELECT emp_name FROM employees WHERE LOWER(department) = 'sales';   -- safe everywhere
```
**Output:**
| emp_name |
|---|
| Meena |
| Omar |
**pandas equivalent:**
```python
# employees / candidates / orders = the tables above loaded as DataFrames
result = employees.loc[employees.department.str.lower() == 'sales', ['emp_name']]
```
(Checked: the pandas result is identical to the SQL output.)
**Edge cases:** pandas `==` is always case-sensitive. `LOWER(NULL)` is NULL, so NULL rows stay out. Wrapping a column in `LOWER()` can stop an index being used.
**Likely follow-ups:**
- How do I make PostgreSQL ignore case? `ILIKE`, or `LOWER()` both sides.
- What is a collation? The rule set for comparing text (case, accents).
**Common mistakes:** Believing all databases behave like MySQL; mixing 'HR' / 'hr' / 'Hr' in data and then missing rows; assuming quoted names are case-insensitive.

### Q30 ⭐⭐ 🟢 Write a query to find the most recently hired employee and the 5 most recently hired employees.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** ORDER BY ... DESC plus LIMIT, and whether you notice the tie on hire date.
**Say this in the interview:** "I sort by hire_date descending so the newest comes first, then use LIMIT 1 for the latest hire or LIMIT 5 for the latest five. I add emp_id as a tie-breaker because two people can join on the same day."
**Explain simply:**
- **ORDER BY** sorts the result; `DESC` = biggest/latest first, `ASC` (default) = smallest/oldest first.
- **LIMIT n** keeps only the first n rows of the sorted result.
- Dialects: MySQL/PostgreSQL/SQLite `LIMIT 5`; SQL Server `SELECT TOP 5 ...`; Oracle 12c+/PostgreSQL/standard `FETCH FIRST 5 ROWS ONLY` (not run here).
- Here Karan (id 4) and Neha (id 7) both joined on 2024-04-01, so "most recent" is a tie; the tie-breaker picks Neha.
**Example:** HR wants the 5 latest joiners for an onboarding batch. Two joined on the same day, so we need a stable rule to decide the order.
**Sample data:** `employees`

| emp_id | emp_name | department | city | salary | hire_date |
|---|---|---|---|---|---|
| 1 | Asha | HR | Pune | 45000 | 2021-06-15 |
| 2 | Ravi | IT | Hyderabad | 80000 | 2020-03-01 |
| 3 | Meena | Sales | Pune | 60000 | 2023-01-10 |
| 4 | Karan | IT | Bengaluru | 80000 | 2024-04-01 |
| 5 | Divya | Finance | Hyderabad | 70000 | 2022-09-20 |
| 6 | Sam | NULL | Pune | 50000 | 2024-02-12 |
| 7 | Neha | HR | Hyderabad | 52000 | 2024-04-01 |
| 8 | Omar | Sales | Bengaluru | 70000 | 2023-11-05 |
**SQL:**
```sql
-- most recent hire
SELECT emp_id, emp_name, hire_date
FROM employees
ORDER BY hire_date DESC, emp_id DESC
LIMIT 1;
-- 5 most recent
SELECT emp_id, emp_name, hire_date
FROM employees
ORDER BY hire_date DESC, emp_id DESC
LIMIT 5;
-- SQL Server (not run here): SELECT TOP 5 ... ORDER BY hire_date DESC, emp_id DESC;
```
**Output:**
Most recent hire

| emp_id | emp_name | hire_date |
|---|---|---|
| 7 | Neha | 2024-04-01 |

5 most recent

| emp_id | emp_name | hire_date |
|---|---|---|
| 7 | Neha | 2024-04-01 |
| 4 | Karan | 2024-04-01 |
| 6 | Sam | 2024-02-12 |
| 8 | Omar | 2023-11-05 |
| 3 | Meena | 2023-01-10 |
**pandas equivalent:**
```python
# employees / candidates / orders = the tables above loaded as DataFrames
result = employees.sort_values(['hire_date', 'emp_id'], ascending=False).head(1)[['emp_id', 'emp_name', 'hire_date']]
```
(Checked: the pandas result is identical to the SQL output.)
```python
# employees / candidates / orders = the tables above loaded as DataFrames
result = employees.sort_values(['hire_date', 'emp_id'], ascending=False).head(5)[['emp_id', 'emp_name', 'hire_date']]
```
(Checked: the pandas result is identical to the SQL output.)
**Edge cases:** Ties on the cut-off date (use `FETCH FIRST ... WITH TIES` in PostgreSQL 13+/Oracle to return all tied rows; or a window function `RANK()`). NULL hire dates: sort position depends on the database (Q35). Dates stored as text must be ISO `YYYY-MM-DD` to sort correctly.
**Likely follow-ups:**
- Latest hire per department? Use `ROW_NUMBER() OVER (PARTITION BY department ORDER BY hire_date DESC)`.
- Oldest hire? Use `ASC`.
**Common mistakes:** Forgetting `DESC` (returns the oldest); using `MAX(hire_date)` and losing the name; no tie-breaker.

### Q31 ⭐⭐ 🟢 Write a query to find the highest-paid employee using ORDER BY and LIMIT 1. What happens if two employees tie for the top salary?
**Asked at:** commonly asked at service MNC screening rounds (the sampled sources list top/Nth-salary as a staple; no company-specific report found)
**What the interviewer is checking:** Basic ORDER BY + LIMIT, and whether you think about ties.
**Say this in the interview:** "I sort by salary descending and take LIMIT 1. If two people tie for the top salary, LIMIT 1 returns only one of them, and which one is not guaranteed. To get everyone at the top, I compare salary to the MAX salary."
**Explain simply:**
- `ORDER BY salary DESC LIMIT 1` = sort high to low, keep the first row.
- Ravi and Karan both earn 80,000. `LIMIT 1` shows just one; without a tie-breaker the choice may change between runs.
- If the business question is "who is paid the most?" the right answer is both people; use `= (SELECT MAX(salary) ...)`.
- A **subquery** is a query inside another query; here it first finds the max salary, then the outer query finds who earns it.
**Example:** Two employees earn 80,000 - the correct answer to "who is the highest paid?" is two names, not one.
**Sample data:** `employees`

| emp_id | emp_name | department | city | salary | hire_date |
|---|---|---|---|---|---|
| 1 | Asha | HR | Pune | 45000 | 2021-06-15 |
| 2 | Ravi | IT | Hyderabad | 80000 | 2020-03-01 |
| 3 | Meena | Sales | Pune | 60000 | 2023-01-10 |
| 4 | Karan | IT | Bengaluru | 80000 | 2024-04-01 |
| 5 | Divya | Finance | Hyderabad | 70000 | 2022-09-20 |
| 6 | Sam | NULL | Pune | 50000 | 2024-02-12 |
| 7 | Neha | HR | Hyderabad | 52000 | 2024-04-01 |
| 8 | Omar | Sales | Bengaluru | 70000 | 2023-11-05 |
**SQL:**
```sql
-- one row only
SELECT emp_id, emp_name, salary
FROM employees
ORDER BY salary DESC
LIMIT 1;
-- all tied for top
SELECT emp_id, emp_name, salary
FROM employees
WHERE salary = (SELECT MAX(salary) FROM employees);
```
**Output:**
LIMIT 1 (tie ignored)

| emp_id | emp_name | salary |
|---|---|---|
| 2 | Ravi | 80000 |

All top earners

| emp_id | emp_name | salary |
|---|---|---|
| 2 | Ravi | 80000 |
| 4 | Karan | 80000 |
**pandas equivalent:**
```python
# employees / candidates / orders = the tables above loaded as DataFrames
result = employees.sort_values('salary', ascending=False).head(1)[['emp_id', 'emp_name', 'salary']]
```
(Checked: the pandas result is identical to the SQL output.)
```python
# employees / candidates / orders = the tables above loaded as DataFrames
result = employees.loc[employees.salary == employees.salary.max(), ['emp_id', 'emp_name', 'salary']]
```
(Checked: the pandas result is identical to the SQL output.)
**Edge cases:** Ties (above). NULL salaries: `MAX` ignores them; `ORDER BY salary DESC` may put NULLs first in PostgreSQL (Q35), so `LIMIT 1` could return a NULL row. Empty table returns no rows.
**Likely follow-ups:**
- Make LIMIT 1 deterministic? Add a tie-breaker: `ORDER BY salary DESC, emp_id` (Q34).
- Return all tied rows with LIMIT? `FETCH FIRST 1 ROW WITH TIES` (PostgreSQL 13+, Oracle; not run here), or `RANK()`.
**Common mistakes:** Assuming LIMIT 1 is always the full answer; forgetting DESC; not handling NULL salaries.

### Q32 ⭐⭐ 🟢 In an HR scenario: a `Candidates` table has candidate_name, city, interview_score and status. Write a query for the top 10 'Shortlisted' candidates in Hyderabad by interview score.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Combining WHERE conditions with ORDER BY DESC and LIMIT on an HR-style table, and handling NULL scores and ties.
**Say this in the interview:** "I filter city and status with WHERE joined by AND, sort by interview_score descending, and take LIMIT 10. I add NULLS LAST so candidates with a pending score do not jump to the top, and the name as a tie-breaker."
**Explain simply:**
- `WHERE city = 'Hyderabad' AND status = 'Shortlisted'` keeps only rows meeting **both** conditions.
- `ORDER BY interview_score DESC` = highest score first; `LIMIT 10` = first 10 rows only. If fewer than 10 match, you simply get fewer.
- Priya and Sneha tie at 88; ordering by name breaks the tie the same way every run.
- Lata has a NULL score (interview not done yet). PostgreSQL and Oracle put NULLs **first** in a DESC sort, so state `NULLS LAST`. MySQL / SQL Server have no `NULLS LAST`: use `ORDER BY (interview_score IS NULL), interview_score DESC` (not run here); SQL Server uses `TOP 10` instead of `LIMIT 10`.
**Example:** The Hyderabad recruiter wants the 10 best shortlisted candidates to call first. Only 5 of the 8 candidates qualify, so 5 rows come back, not 10.
**Sample data:** `candidates`

| cand_id | candidate_name | city | interview_score | status |
|---|---|---|---|---|
| 1 | Priya | Hyderabad | 88 | Shortlisted |
| 2 | Arjun | Hyderabad | 92 | Shortlisted |
| 3 | Sneha | Hyderabad | 88 | Shortlisted |
| 4 | Imran | Hyderabad | 75 | Rejected |
| 5 | Kavya | Pune | 95 | Shortlisted |
| 6 | Rohit | Hyderabad | 81 | Shortlisted |
| 7 | Lata | Hyderabad | NULL | Shortlisted |
| 8 | Vikram | Hyderabad | 70 | On hold |
**SQL:**
```sql
SELECT candidate_name, interview_score
FROM candidates
WHERE city = 'Hyderabad'
  AND status = 'Shortlisted'
ORDER BY interview_score DESC NULLS LAST, candidate_name
LIMIT 10;
```
**Output:**
| candidate_name | interview_score |
|---|---|
| Arjun | 92 |
| Priya | 88 |
| Sneha | 88 |
| Rohit | 81 |
| Lata | NULL |
**pandas equivalent:**
```python
# employees / candidates / orders = the tables above loaded as DataFrames
result = (candidates[(candidates.city == 'Hyderabad') & (candidates.status == 'Shortlisted')]
          .sort_values(['interview_score', 'candidate_name'], ascending=[False, True], na_position='last')
          .head(10)[['candidate_name', 'interview_score']])
```
(Checked: the pandas result is identical to the SQL output.)
**Edge cases:** NULL score is kept but placed last. Kavya (Pune) and Imran (Rejected) are filtered out. Text values must match exactly - `'shortlisted'` vs `'Shortlisted'` may behave differently by database (Q29).
**Likely follow-ups:**
- Top 10 per city? `ROW_NUMBER() OVER (PARTITION BY city ORDER BY interview_score DESC)`.
- Exclude unscored candidates? Add `AND interview_score IS NOT NULL`.
**Common mistakes:** `ORDER BY` before `WHERE`; forgetting `DESC` (returns lowest scores); not thinking about NULL scores.

### Q33 ⭐⭐ 🟡 If you run a query without ORDER BY, is the order of rows guaranteed? What is the risk of using LIMIT without ORDER BY?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** That you know a table is an unordered set and only ORDER BY guarantees order.
**Say this in the interview:** "No. Without ORDER BY the database may return rows in any order, and that order can change when data, indexes or the execution plan change. So LIMIT without ORDER BY gives me an arbitrary slice, not the top or first rows."
**Explain simply:**
- A table is like a bag of rows, not a sorted list. Today's order often looks like insertion order, but that is an accident of storage.
- The **execution plan** (how the database decides to read data) can switch to an **index** (a sorted lookup structure) and rows then come out in index order.
- `LIMIT 3` with no `ORDER BY` returns "any 3 rows". Two runs, two replicas or a later release can give different rows - a nasty bug in reports and paging.
- Rule: if the order or the "first N" matters, write `ORDER BY` with a unique tie-breaker.
**Example:** Below, the same table is read twice in SQLite. The first query (no filter) comes back in insertion order. After I add an index on salary, a query with a salary filter returns the rows in salary order instead, though I never asked for it.
**Sample data:** `employees`

| emp_id | emp_name | department | city | salary | hire_date |
|---|---|---|---|---|---|
| 1 | Asha | HR | Pune | 45000 | 2021-06-15 |
| 2 | Ravi | IT | Hyderabad | 80000 | 2020-03-01 |
| 3 | Meena | Sales | Pune | 60000 | 2023-01-10 |
| 4 | Karan | IT | Bengaluru | 80000 | 2024-04-01 |
| 5 | Divya | Finance | Hyderabad | 70000 | 2022-09-20 |
| 6 | Sam | NULL | Pune | 50000 | 2024-02-12 |
| 7 | Neha | HR | Hyderabad | 52000 | 2024-04-01 |
| 8 | Omar | Sales | Bengaluru | 70000 | 2023-11-05 |
**SQL:**
```sql
SELECT emp_name, salary FROM employees;
CREATE INDEX idx_sal ON employees(salary);
SELECT emp_name, salary FROM employees WHERE salary > 0;
SELECT emp_name, salary FROM employees WHERE salary > 0 LIMIT 3;
-- correct way: ORDER BY salary DESC, emp_id LIMIT 3;
```
**Output:**
No ORDER BY, before index

| emp_name | salary |
|---|---|
| Asha | 45000 |
| Ravi | 80000 |
| Meena | 60000 |
| Karan | 80000 |
| Divya | 70000 |
| Sam | 50000 |
| Neha | 52000 |
| Omar | 70000 |

No ORDER BY, after index on salary

| emp_name | salary |
|---|---|
| Asha | 45000 |
| Sam | 50000 |
| Neha | 52000 |
| Meena | 60000 |
| Divya | 70000 |
| Omar | 70000 |
| Ravi | 80000 |
| Karan | 80000 |

LIMIT 3, no ORDER BY, after index

| emp_name | salary |
|---|---|
| Asha | 45000 |
| Sam | 50000 |
| Neha | 52000 |
**pandas equivalent:**
```python
# a DataFrame keeps row order, so pandas hides this problem; always sort explicitly
result = employees.sort_values(['salary', 'emp_id'], ascending=[False, True]).head(3)
```
**Edge cases:** This output is one SQLite run; other engines (and parallel queries in PostgreSQL / SQL Server) may order differently. Even `GROUP BY` and `DISTINCT` do not promise sorted output in the standard (many engines happen to sort or hash).
**Likely follow-ups:**
- Does primary key order guarantee order? No, still not guaranteed.
- Is ORDER BY free? No, sorting costs time on big tables, so add it only where needed.
**Common mistakes:** Relying on the order seen in testing; using `LIMIT 1` to get "the latest" without `ORDER BY`; paging without a stable sort.

### Q34 ⭐⭐ 🟡 How do you break ties in an ORDER BY + LIMIT query so the result is the same every time? (e.g. salary ties, add emp_id)
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** That you understand ties make ORDER BY + LIMIT non-deterministic and know to add a unique column.
**Say this in the interview:** "I add a second sort column that is unique, usually the primary key, like ORDER BY salary DESC, emp_id. Then there is only one possible order, so the same rows come back every time."
**Explain simply:**
- A **tie** = two rows with the same sort value. The database may order tied rows either way.
- Ravi and Karan earn 80,000; Divya and Omar earn 70,000. For the top 3, the third place is a tie between Divya (id 5) and Omar (id 8), so plain `salary DESC LIMIT 3` could return either.
- Add a unique tie-breaker (`emp_id`) so the full sort order is fixed: here Divya wins because her id is lower.
- Also important for paging (Q39): without a stable order, rows can repeat or vanish between pages.
**Example:** Payroll wants the top 3 earners for a bonus. With ties at 70,000, an unstable query could pick Omar one day and Divya the next.
**Sample data:** `employees`

| emp_id | emp_name | department | city | salary | hire_date |
|---|---|---|---|---|---|
| 1 | Asha | HR | Pune | 45000 | 2021-06-15 |
| 2 | Ravi | IT | Hyderabad | 80000 | 2020-03-01 |
| 3 | Meena | Sales | Pune | 60000 | 2023-01-10 |
| 4 | Karan | IT | Bengaluru | 80000 | 2024-04-01 |
| 5 | Divya | Finance | Hyderabad | 70000 | 2022-09-20 |
| 6 | Sam | NULL | Pune | 50000 | 2024-02-12 |
| 7 | Neha | HR | Hyderabad | 52000 | 2024-04-01 |
| 8 | Omar | Sales | Bengaluru | 70000 | 2023-11-05 |
**SQL:**
```sql
SELECT emp_id, emp_name, salary
FROM employees
ORDER BY salary DESC, emp_id ASC
LIMIT 3;
```
**Output:**
| emp_id | emp_name | salary |
|---|---|---|
| 2 | Ravi | 80000 |
| 4 | Karan | 80000 |
| 5 | Divya | 70000 |
**pandas equivalent:**
```python
# employees / candidates / orders = the tables above loaded as DataFrames
result = employees.sort_values(['salary', 'emp_id'], ascending=[False, True]).head(3)[['emp_id', 'emp_name', 'salary']]
```
(Checked: the pandas result is identical to the SQL output.)
**Edge cases:** If business rules say all tied people should be included, a tie-breaker is the wrong tool; use `RANK()` or `FETCH FIRST 3 ROWS WITH TIES` (PostgreSQL 13+/Oracle, not run here). The tie-breaker must be unique, so `emp_name` alone is not enough if two people share a name.
**Likely follow-ups:**
- What if no unique column exists? Use `ROW_NUMBER()` or add a surrogate id.
- Does the tie-breaker direction matter? Only for who wins the tie; choose a business-sensible rule (e.g. earliest hire).
**Common mistakes:** Tie-breaking with a non-unique column; forgetting to tie-break at all; hiding the fact that other tied people were dropped.

### Q35 ⭐⭐ 🟡 Where do NULL values appear when you sort ascending or descending? How do you control it (NULLS FIRST / NULLS LAST)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** That NULL placement in sorting differs across databases and you know how to control it.
**Say this in the interview:** "It depends on the database. In MySQL, SQL Server and SQLite, NULLs count as the smallest value: first in ascending, last in descending. In PostgreSQL and Oracle, NULLs count as the largest: last in ascending, first in descending. I control it with NULLS FIRST or NULLS LAST."
**Explain simply:**
- **NULL** = a missing or unknown value (not zero, not blank text).
- | Database | ASC | DESC | Control |
|---|---|---|---|
| MySQL, SQL Server, SQLite | NULL first | NULL last | no `NULLS` keyword in MySQL/SQL Server; SQLite 3.30+ has it |
| PostgreSQL, Oracle | NULL last | NULL first | `NULLS FIRST / NULLS LAST` |
- Portable trick (works in MySQL and SQL Server too, not run in those): sort by a flag first, `ORDER BY (col IS NULL), col` in MySQL, or `ORDER BY CASE WHEN col IS NULL THEN 1 ELSE 0 END, col` in SQL Server.
- The SQLite output below was really run; PostgreSQL ordering is described from its documented behaviour.
**Example:** Sam has no department recorded. In a department-wise attendance list, you may want Sam at the bottom (`NULLS LAST`) so "unassigned" does not lead the report.
**Sample data:** `employees`

| emp_id | emp_name | department | city | salary | hire_date |
|---|---|---|---|---|---|
| 1 | Asha | HR | Pune | 45000 | 2021-06-15 |
| 2 | Ravi | IT | Hyderabad | 80000 | 2020-03-01 |
| 3 | Meena | Sales | Pune | 60000 | 2023-01-10 |
| 4 | Karan | IT | Bengaluru | 80000 | 2024-04-01 |
| 5 | Divya | Finance | Hyderabad | 70000 | 2022-09-20 |
| 6 | Sam | NULL | Pune | 50000 | 2024-02-12 |
| 7 | Neha | HR | Hyderabad | 52000 | 2024-04-01 |
| 8 | Omar | Sales | Bengaluru | 70000 | 2023-11-05 |
**SQL:**
```sql
SELECT emp_name, department FROM employees ORDER BY department ASC;
SELECT emp_name, department FROM employees ORDER BY department DESC;
SELECT emp_name, department FROM employees ORDER BY department ASC NULLS LAST, emp_id;   -- PostgreSQL, Oracle, SQLite, DuckDB
SELECT emp_name, department FROM employees ORDER BY (department IS NULL), department;   -- MySQL / SQLite style flag
```
**Output:**
ASC (SQLite: NULL first)

| emp_name | department |
|---|---|
| Sam | NULL |
| Divya | Finance |
| Asha | HR |
| Neha | HR |
| Ravi | IT |
| Karan | IT |
| Meena | Sales |
| Omar | Sales |

DESC (SQLite: NULL last)

| emp_name | department |
|---|---|
| Meena | Sales |
| Omar | Sales |
| Ravi | IT |
| Karan | IT |
| Asha | HR |
| Neha | HR |
| Divya | Finance |
| Sam | NULL |

NULLS LAST

| emp_name | department |
|---|---|
| Divya | Finance |
| Asha | HR |
| Neha | HR |
| Ravi | IT |
| Karan | IT |
| Meena | Sales |
| Omar | Sales |
| Sam | NULL |

Flag trick

| emp_name | department |
|---|---|
| Divya | Finance |
| Asha | HR |
| Neha | HR |
| Ravi | IT |
| Karan | IT |
| Meena | Sales |
| Omar | Sales |
| Sam | NULL |
**pandas equivalent:**
```python
# employees / candidates / orders = the tables above loaded as DataFrames
result = employees.sort_values(['department', 'emp_id'], na_position='last')[['emp_name', 'department']]
```
(Checked: the pandas result is identical to the SQL output.)
**Edge cases:** Tied non-NULL rows (the two HR people, the two IT people) can come out in either order unless you add a tie-breaker; I added `emp_id` in the checked version. pandas `na_position` plays the role of NULLS FIRST/LAST.
**Likely follow-ups:**
- Where do NULLs go in PostgreSQL DESC? First.
- How to treat NULL as a value? `COALESCE(department, 'Unknown')`.
**Common mistakes:** Assuming all databases sort NULLs the same; getting an unexpected NULL row from `ORDER BY col DESC LIMIT 1` in PostgreSQL.

### Q36 ⭐⭐ 🟡 What does `WHERE department <> 'HR'` do to rows where department is NULL? Explain SQL's three-valued logic (true / false / unknown) in plain words.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you understand that comparisons with NULL give "unknown", and that WHERE keeps only "true".
**Say this in the interview:** "The row with a NULL department is not returned. NULL means unknown, and unknown not-equal HR is not true, it is unknown. WHERE keeps only rows where the condition is true, so it drops that row. To keep it I add OR department IS NULL."
**Explain simply:**
- **Three-valued logic**: every test gives TRUE, FALSE or UNKNOWN (UNKNOWN appears whenever a NULL is involved).
- `NULL <> 'HR'` = UNKNOWN (we cannot tell). `NULL = 'HR'` = UNKNOWN too. Even `NULL = NULL` is UNKNOWN. Use `IS NULL` / `IS NOT NULL`.
- **WHERE** keeps rows only where the result is TRUE; FALSE and UNKNOWN are both thrown away.
- Logic rules: `UNKNOWN AND TRUE` = UNKNOWN; `UNKNOWN OR TRUE` = TRUE; `NOT UNKNOWN` = UNKNOWN.
- Null-safe options: `IS DISTINCT FROM` (PostgreSQL, SQL Server 2022+, DuckDB), `<=>` (MySQL), `IS NOT` (SQLite).
**Example:** Of 8 employees, 2 are in HR. People "not in HR" should be 6, but plain `<> 'HR'` returns 5 because Sam's department was never filled in.
**Sample data:** `employees`

| emp_id | emp_name | department | city | salary | hire_date |
|---|---|---|---|---|---|
| 1 | Asha | HR | Pune | 45000 | 2021-06-15 |
| 2 | Ravi | IT | Hyderabad | 80000 | 2020-03-01 |
| 3 | Meena | Sales | Pune | 60000 | 2023-01-10 |
| 4 | Karan | IT | Bengaluru | 80000 | 2024-04-01 |
| 5 | Divya | Finance | Hyderabad | 70000 | 2022-09-20 |
| 6 | Sam | NULL | Pune | 50000 | 2024-02-12 |
| 7 | Neha | HR | Hyderabad | 52000 | 2024-04-01 |
| 8 | Omar | Sales | Bengaluru | 70000 | 2023-11-05 |
**SQL:**
```sql
-- Sam is silently dropped
SELECT emp_name, department FROM employees WHERE department <> 'HR';
-- fix 1: keep NULLs explicitly
SELECT emp_name, department FROM employees WHERE department <> 'HR' OR department IS NULL;
-- fix 2 (SQLite null-safe compare; PostgreSQL: IS DISTINCT FROM)
SELECT emp_name, department FROM employees WHERE department IS NOT 'HR';
```
**Output:**
Plain `<>`

| emp_name | department |
|---|---|
| Ravi | IT |
| Meena | Sales |
| Karan | IT |
| Divya | Finance |
| Omar | Sales |

Fix 1

| emp_name | department |
|---|---|
| Ravi | IT |
| Meena | Sales |
| Karan | IT |
| Divya | Finance |
| Sam | NULL |
| Omar | Sales |

Fix 2

| emp_name | department |
|---|---|
| Ravi | IT |
| Meena | Sales |
| Karan | IT |
| Divya | Finance |
| Sam | NULL |
| Omar | Sales |
**pandas equivalent:**
```python
# employees / candidates / orders = the tables above loaded as DataFrames
result = employees.loc[(employees.department != 'HR') | employees.department.isna(), ['emp_name', 'department']]
```
(Checked: the pandas result is identical to the SQL output.)
**Edge cases:** The same trap hits `NOT IN`, `NOT LIKE`, `>`, `<` and `!=`. `COUNT(department)` skips NULLs while `COUNT(*)` counts them. `COALESCE(department, 'Unknown') <> 'HR'` is another fix.
**Likely follow-ups:**
- What does `WHERE NULL = NULL` return? No rows.
- Is NULL the same as empty string? No (except Oracle, which treats `''` as NULL).
**Common mistakes:** Writing `= NULL`; assuming `<> 'HR'` means "everything else"; forgetting NULLs after joins.

### Q37 ⭐⭐ 🟡 Why can `NOT IN` return no rows when the list contains a NULL? How would you fix it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** The classic NULL trap in NOT IN and whether you know the safe alternatives.
**Say this in the interview:** "`x NOT IN (1, 2, NULL)` expands to x<>1 AND x<>2 AND x<>NULL. The last part is UNKNOWN, so the whole condition can never be TRUE, and no rows come back. I fix it by filtering NULLs out of the list or by using NOT EXISTS."
**Explain simply:**
- `NOT IN ('HR', NULL)` is shorthand for `<> 'HR' AND <> NULL`. `<> NULL` is always UNKNOWN, and TRUE AND UNKNOWN = UNKNOWN, so WHERE rejects every row.
- It happens most often when the list comes from a **subquery** (a query inside a query) whose column contains a NULL.
- Fix 1: remove NULLs in the subquery (`WHERE dept_name IS NOT NULL`). Fix 2: `NOT EXISTS`, which ignores NULL comparisons correctly. Fix 3: `LEFT JOIN ... WHERE right.key IS NULL`.
- `IN` (positive) does not have this problem: it still finds matches.
**Example:** HR keeps a list of closed departments, but one entry was left blank (NULL). The query to find employees in departments that are not closed returns nobody, which looks like a data bug but is really this rule.
**Sample data:** `employees`

| emp_id | emp_name | department | city | salary | hire_date |
|---|---|---|---|---|---|
| 1 | Asha | HR | Pune | 45000 | 2021-06-15 |
| 2 | Ravi | IT | Hyderabad | 80000 | 2020-03-01 |
| 3 | Meena | Sales | Pune | 60000 | 2023-01-10 |
| 4 | Karan | IT | Bengaluru | 80000 | 2024-04-01 |
| 5 | Divya | Finance | Hyderabad | 70000 | 2022-09-20 |
| 6 | Sam | NULL | Pune | 50000 | 2024-02-12 |
| 7 | Neha | HR | Hyderabad | 52000 | 2024-04-01 |
| 8 | Omar | Sales | Bengaluru | 70000 | 2023-11-05 |

`closed_depts`

| dept_name |
|---|
| HR |
| NULL |
**SQL:**
```sql
-- breaks: list contains a NULL
SELECT emp_name, department FROM employees
WHERE department NOT IN (SELECT dept_name FROM closed_depts);
-- fix 1: drop NULLs from the list
SELECT emp_name, department FROM employees
WHERE department NOT IN (SELECT dept_name FROM closed_depts WHERE dept_name IS NOT NULL);
-- fix 2: NOT EXISTS
SELECT e.emp_name, e.department FROM employees e
WHERE NOT EXISTS (SELECT 1 FROM closed_depts c WHERE c.dept_name = e.department);
```
**Output:**
Broken NOT IN

| emp_name | department |
|---|---|
| (no rows) |  |

Fix 1

| emp_name | department |
|---|---|
| Ravi | IT |
| Meena | Sales |
| Karan | IT |
| Divya | Finance |
| Omar | Sales |

Fix 2

| emp_name | department |
|---|---|
| Ravi | IT |
| Meena | Sales |
| Karan | IT |
| Divya | Finance |
| Sam | NULL |
| Omar | Sales |
**pandas equivalent:**
```python
# employees / candidates / orders = the tables above loaded as DataFrames
result = employees.loc[employees.department.notna() & ~employees.department.isin(['HR']), ['emp_name', 'department']]
```
(Checked: the pandas result is identical to the SQL output.)
(pandas `isin` has no NULL trap, so the broken case is not reproducible there.)
**Edge cases:** Sam (NULL department) is missing from fix 1 because `NULL NOT IN (...)` is itself UNKNOWN (add `OR department IS NULL` to keep Sam), but NOT EXISTS keeps Sam because no closed department matches NULL. Empty list: `NOT IN (empty subquery)` returns every row, including NULL-department rows. `NOT EXISTS` and `NOT IN` agree only when no NULLs exist.
**Likely follow-ups:**
- Why does NOT EXISTS work? It tests whether any row matches, not whether values are not-equal.
- Does IN have the same problem? No.
**Common mistakes:** Debugging data instead of the NULL rule; using `<> NULL`; trusting NOT IN subqueries on nullable columns.

### Q38 ⭐⭐ 🟡 What is the difference between `a OR b AND c` and `(a OR b) AND c`? Show how a wrong result can sneak in.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** That you know AND binds tighter than OR and use brackets to say what you mean.
**Say this in the interview:** "AND is evaluated before OR, so `a OR b AND c` means `a OR (b AND c)`. If I wanted both a and b to face the c test, I must write `(a OR b) AND c`. I always use brackets when mixing them."
**Explain simply:**
- Order of precedence: brackets first, then `NOT`, then `AND`, then `OR` - like multiplication before addition.
- `department = 'HR' OR department = 'IT' AND salary > 60000` reads as: all HR people, plus IT people paid over 60k.
- With brackets: only HR or IT people who are paid over 60k. The HR people under 60k disappear.
- Same logic in every database; the safest habit is adding brackets even when not needed.
**Example:** The recruiter says "HR or IT staff earning over 60,000". Without brackets, Asha (45,000) and Neha (52,000) from HR slip into the result - a wrong answer that looks plausible.
**Sample data:** `employees`

| emp_id | emp_name | department | city | salary | hire_date |
|---|---|---|---|---|---|
| 1 | Asha | HR | Pune | 45000 | 2021-06-15 |
| 2 | Ravi | IT | Hyderabad | 80000 | 2020-03-01 |
| 3 | Meena | Sales | Pune | 60000 | 2023-01-10 |
| 4 | Karan | IT | Bengaluru | 80000 | 2024-04-01 |
| 5 | Divya | Finance | Hyderabad | 70000 | 2022-09-20 |
| 6 | Sam | NULL | Pune | 50000 | 2024-02-12 |
| 7 | Neha | HR | Hyderabad | 52000 | 2024-04-01 |
| 8 | Omar | Sales | Bengaluru | 70000 | 2023-11-05 |
**SQL:**
```sql
-- wrong for the request
SELECT emp_name, department, salary FROM employees
WHERE department = 'HR' OR department = 'IT' AND salary > 60000;
-- correct
SELECT emp_name, department, salary FROM employees
WHERE (department = 'HR' OR department = 'IT') AND salary > 60000;
```
**Output:**
Without brackets

| emp_name | department | salary |
|---|---|---|
| Asha | HR | 45000 |
| Ravi | IT | 80000 |
| Karan | IT | 80000 |
| Neha | HR | 52000 |

With brackets

| emp_name | department | salary |
|---|---|---|
| Ravi | IT | 80000 |
| Karan | IT | 80000 |
**pandas equivalent:**
```python
# employees / candidates / orders = the tables above loaded as DataFrames
result = employees.loc[(employees.department == 'HR') | ((employees.department == 'IT') & (employees.salary > 60000)), ['emp_name', 'department', 'salary']]
```
(Checked: the pandas result is identical to the SQL output.)
```python
# employees / candidates / orders = the tables above loaded as DataFrames
result = employees.loc[employees.department.isin(['HR', 'IT']) & (employees.salary > 60000), ['emp_name', 'department', 'salary']]
```
(Checked: the pandas result is identical to the SQL output.)
**Edge cases:** NULL conditions follow three-valued logic (Q36): `UNKNOWN OR TRUE` is TRUE. In pandas you must bracket every comparison yourself because `&` and `|` bind tighter than `==`, a different trap.
**Likely follow-ups:**
- Rewrite `OR` of the same column? Use `IN`.
- How would you debug it? Count rows with and without brackets and inspect the extras.
**Common mistakes:** Assuming left-to-right evaluation; relying on indentation instead of brackets; missing that the wrong result "looks right" on a small sample.

### Q39 ⭐⭐ 🟡 How do you show page 3 of results with 10 rows per page using LIMIT and OFFSET?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** That you know the OFFSET formula and that paging needs a stable ORDER BY.
**Say this in the interview:** "For page 3 with 10 rows per page I skip the first 20 rows and take the next 10: `ORDER BY ... LIMIT 10 OFFSET 20`. The formula is OFFSET = (page - 1) x page size."
**Explain simply:**
- **LIMIT** = how many rows to return; **OFFSET** = how many rows to skip first.
- Page 3 of size 10: skip (3 - 1) x 10 = 20 rows, return 10 (rows 21-30).
- Dialects: MySQL `LIMIT 20, 10` or `LIMIT 10 OFFSET 20`; PostgreSQL/SQLite `LIMIT 10 OFFSET 20`; SQL Server and Oracle 12c+ `OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY` (SQL Server requires `ORDER BY`); neither run here.
- Always include `ORDER BY` with a unique tie-breaker, otherwise pages can overlap or skip rows (Q33, Q34).
- Large offsets are slow because the database still reads the skipped rows; **keyset pagination** (`WHERE emp_id > last_seen_id ORDER BY emp_id LIMIT 10`) scales better.
**Example:** An HR portal lists 8 employees. Page 3 at 10 per page is empty (only 8 rows exist). Using page size 3 shows page 3 as rows 7 and 8.
**Sample data:** `employees`

| emp_id | emp_name | department | city | salary | hire_date |
|---|---|---|---|---|---|
| 1 | Asha | HR | Pune | 45000 | 2021-06-15 |
| 2 | Ravi | IT | Hyderabad | 80000 | 2020-03-01 |
| 3 | Meena | Sales | Pune | 60000 | 2023-01-10 |
| 4 | Karan | IT | Bengaluru | 80000 | 2024-04-01 |
| 5 | Divya | Finance | Hyderabad | 70000 | 2022-09-20 |
| 6 | Sam | NULL | Pune | 50000 | 2024-02-12 |
| 7 | Neha | HR | Hyderabad | 52000 | 2024-04-01 |
| 8 | Omar | Sales | Bengaluru | 70000 | 2023-11-05 |
**SQL:**
```sql
SELECT emp_id, emp_name FROM employees
ORDER BY emp_id
LIMIT 10 OFFSET 20;   -- page 3, 10 per page
SELECT emp_id, emp_name FROM employees
ORDER BY emp_id
LIMIT 3 OFFSET 6;    -- page 3, 3 per page
```
**Output:**
Page 3, size 10 (nothing that far)

| emp_id | emp_name |
|---|---|
| (no rows) |  |

Page 3, size 3

| emp_id | emp_name |
|---|---|
| 7 | Neha |
| 8 | Omar |
**pandas equivalent:**
```python
# employees / candidates / orders = the tables above loaded as DataFrames
page, size = 3, 10
result = employees.sort_values('emp_id').iloc[(page - 1) * size : page * size][['emp_id', 'emp_name']]
```
(Checked: the pandas result is identical to the SQL output.)
```python
# employees / candidates / orders = the tables above loaded as DataFrames
page, size = 3, 3
result = employees.sort_values('emp_id').iloc[(page - 1) * size : page * size][['emp_id', 'emp_name']]
```
(Checked: the pandas result is identical to the SQL output.)
**Edge cases:** Page beyond the data gives zero rows, not an error. If rows are inserted between page requests, OFFSET paging can repeat or skip rows. Total page count needs a separate `SELECT COUNT(*)`.
**Likely follow-ups:**
- Why is OFFSET slow at high pages? It reads and discards rows first.
- Better approach? Keyset pagination.
**Common mistakes:** Using the page number itself as OFFSET (OFFSET 3 instead of 20); paging without ORDER BY; forgetting pages are 1-based.

### Q40 ⭐⭐ 🟡 Can you sort by a column number (ORDER BY 2) or by a calculated expression? Is this good practice?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** That ORDER BY accepts positions, aliases and expressions, and that you know the trade-offs.
**Say this in the interview:** "Yes. ORDER BY 2 sorts by the second column in the SELECT list, and I can also sort by an expression like salary x 12 or by its alias. Positions are fine for quick checks but bad practice in saved code because reordering the SELECT list silently changes the sort."
**Explain simply:**
- `ORDER BY 2` = sort by the 2nd column of the SELECT list (counting starts at 1).
- `ORDER BY salary * 12` sorts by a calculation; you can also use the alias (`ORDER BY annual_pay`). ORDER BY runs after SELECT, so aliases are allowed here (but not in `WHERE`).
- Good practice: use column names or aliases; position numbers break when someone edits the SELECT list. Some teams ban them.
- Sorting by an expression can prevent index use on large tables.
**Example:** A quick check `ORDER BY 2 DESC` ranks people by salary; the readable version `ORDER BY annual_pay DESC` still works if someone adds a new column.
**Sample data:** `employees`

| emp_id | emp_name | department | city | salary | hire_date |
|---|---|---|---|---|---|
| 1 | Asha | HR | Pune | 45000 | 2021-06-15 |
| 2 | Ravi | IT | Hyderabad | 80000 | 2020-03-01 |
| 3 | Meena | Sales | Pune | 60000 | 2023-01-10 |
| 4 | Karan | IT | Bengaluru | 80000 | 2024-04-01 |
| 5 | Divya | Finance | Hyderabad | 70000 | 2022-09-20 |
| 6 | Sam | NULL | Pune | 50000 | 2024-02-12 |
| 7 | Neha | HR | Hyderabad | 52000 | 2024-04-01 |
| 8 | Omar | Sales | Bengaluru | 70000 | 2023-11-05 |
**SQL:**
```sql
-- by position (2nd column = salary)
SELECT emp_name, salary FROM employees ORDER BY 2 DESC, 1;
-- by expression (alias form gives the same result: annual_pay DESC, emp_name;)
SELECT emp_name, salary * 12 AS annual_pay FROM employees ORDER BY salary * 12 DESC, emp_name;
```
**Output:**
ORDER BY 2 DESC, 1

| emp_name | salary |
|---|---|
| Karan | 80000 |
| Ravi | 80000 |
| Divya | 70000 |
| Omar | 70000 |
| Meena | 60000 |
| Neha | 52000 |
| Sam | 50000 |
| Asha | 45000 |

ORDER BY salary * 12 DESC, emp_name

| emp_name | annual_pay |
|---|---|
| Karan | 960000 |
| Ravi | 960000 |
| Divya | 840000 |
| Omar | 840000 |
| Meena | 720000 |
| Neha | 624000 |
| Sam | 600000 |
| Asha | 540000 |
**pandas equivalent:**
```python
# employees / candidates / orders = the tables above loaded as DataFrames
result = employees.sort_values(['salary', 'emp_name'], ascending=[False, True])[['emp_name', 'salary']]
```
(Checked: the pandas result is identical to the SQL output.)
```python
# employees / candidates / orders = the tables above loaded as DataFrames
result = employees.assign(annual_pay=employees.salary * 12).sort_values(['annual_pay', 'emp_name'], ascending=[False, True])[['emp_name', 'annual_pay']]
```
(Checked: the pandas result is identical to the SQL output.)
**Edge cases:** Position number out of range raises an error (`ORDER BY 5` on a 2-column SELECT). `SELECT *` with a position is fragile. With `UNION`, positions or output column names are the only way to sort the combined result.
**Likely follow-ups:**
- Can I sort by a column not in the SELECT list? Yes (not with `DISTINCT` in some databases).
- Can GROUP BY use positions? Yes in MySQL/PostgreSQL/SQLite, with the same drawbacks.
**Common mistakes:** Counting from 0; leaving `ORDER BY 3` after changing the SELECT list; sorting numbers stored as text.

### Q41 ⭐⭐ 🟡 An `Orders` table has order_id, status, total_amount, order_date. Write a query for orders placed in 2023 with status 'Completed', sorted by total_amount highest first.
**Asked at:** appears in a public SQL practice set (CodingShuttle); no company-specific interview report found
**What the interviewer is checking:** Combining text and date filters, sorting highest first, and handling a date column that carries a time.
**Say this in the interview:** "I filter status = 'Completed' and use a half-open date range, order_date >= 2023-01-01 and < 2024-01-01, so nothing on 31 December is lost even if the column has a time. Then ORDER BY total_amount DESC."
**Explain simply:**
- Half-open range (`>= start` and `< next start`) works for DATE, DATETIME and timestamp columns.
- `BETWEEN '2023-01-01' AND '2023-12-31'` treats the end as midnight, so an order at 18:45 on 31 Dec is missed (shown below).
- Year shortcuts: `YEAR(order_date) = 2023` (MySQL/SQL Server), `EXTRACT(YEAR FROM order_date) = 2023` (PostgreSQL), `strftime('%Y', order_date)` (SQLite). They work, but wrapping the column in a function blocks index use, so the range form is better.
- Here dates are stored as ISO text, so comparison is alphabetical, which equals date order. Add `order_id` to break the tie between the two 2,500 orders.
**Example:** Finance asks for completed 2023 orders, biggest first. Order 3 (2,500) was placed at 18:45 on 31 Dec 2023 and must be included.
**Sample data:** `orders`

| order_id | status | total_amount | order_date |
|---|---|---|---|
| 1 | Completed | 1200.50 | 2023-02-14 |
| 2 | Cancelled | 800.00 | 2023-03-02 |
| 3 | Completed | 2500.00 | 2023-12-31 18:45:00 |
| 4 | Completed | 950.00 | 2022-12-30 |
| 5 | Pending | 400.00 | 2023-07-19 |
| 6 | Completed | 2500.00 | 2023-06-01 |
| 7 | Completed | 300.00 | 2024-01-01 |
| 8 | Completed | 1800.00 | 2023-09-09 |
**SQL:**
```sql
SELECT order_id, total_amount, order_date
FROM orders
WHERE status = 'Completed'
  AND order_date >= '2023-01-01'
  AND order_date <  '2024-01-01'
ORDER BY total_amount DESC, order_id;
-- risky version with BETWEEN
SELECT order_id, total_amount, order_date
FROM orders
WHERE status = 'Completed'
  AND order_date BETWEEN '2023-01-01' AND '2023-12-31'
ORDER BY total_amount DESC, order_id;
```
**Output:**
Half-open range (correct)

| order_id | total_amount | order_date |
|---|---|---|
| 3 | 2500.00 | 2023-12-31 18:45:00 |
| 6 | 2500.00 | 2023-06-01 |
| 8 | 1800.00 | 2023-09-09 |
| 1 | 1200.50 | 2023-02-14 |

BETWEEN version (misses order 3)

| order_id | total_amount | order_date |
|---|---|---|
| 6 | 2500.00 | 2023-06-01 |
| 8 | 1800.00 | 2023-09-09 |
| 1 | 1200.50 | 2023-02-14 |
**pandas equivalent:**
```python
# employees / candidates / orders = the tables above loaded as DataFrames
od = pd.to_datetime(orders.order_date, format='mixed')
result = (orders[(orders.status == 'Completed') & (od >= '2023-01-01') & (od < '2024-01-01')]
          .sort_values(['total_amount', 'order_id'], ascending=[False, True])[['order_id', 'total_amount', 'order_date']])
```
(Checked: the pandas result is identical to the SQL output.)
**Edge cases:** Status spelling or case (`'completed'` vs `'Completed'`, Q29); NULL `order_date` rows never match; no matching rows returns an empty table, not an error; the 2022 and 2024 orders are correctly excluded.
**Likely follow-ups:**
- Total revenue for those orders? Replace the SELECT with `SUM(total_amount)`.
- Top 3 only? Add `LIMIT 3` (`TOP 3` in SQL Server).
**Common mistakes:** Using BETWEEN with timestamps; sorting ascending by default; applying a function to the date column on a huge table; forgetting the status filter.

### Q42 ⭐⭐ 🟡 An order_date column stores date and time. Why does `BETWEEN '2024-01-01' AND '2024-01-31'` miss orders on 31 Jan afternoon, and how do you fix it?
**Asked at:** service MNC / analytics firm (general SQL-basics screens; no company-specific report found for this exact question)
**What the interviewer is checking:** Do you know that a date with a time part is not the same as a plain date.
**Say this in the interview:** A date written as '2024-01-31' really means 31 Jan at 00:00:00 (midnight). So BETWEEN stops at midnight and drops the rest of that day. The safe pattern is: on or after the first day, and before the day after the last day.
**Explain simply:**
- BETWEEN is inclusive on both ends, but '2024-01-31' is read as 2024-01-31 00:00:00.
- An order at 14:45 on 31 Jan is later than that midnight, so it falls outside.
- Fix: use a half-open range, `>= start AND < next day`. Half-open means the start is included and the end is excluded.
- It works for any column type and any dialect.
**Example:** A payroll swipe log has timestamps. A January report that uses BETWEEN ... '2024-01-31' loses every swipe on 31 Jan after midnight, so the last day looks almost empty.
**Sample data:**
`orders`

| order_id | order_date | amount |
|---|---|---|
| 1 | 2024-01-15 10:30:00 | 500 |
| 2 | 2024-01-31 00:00:00 | 700 |
| 3 | 2024-01-31 14:45:00 | 1200 |
| 4 | 2024-01-31 23:59:00 | 300 |
| 5 | 2024-02-01 09:00:00 | 900 |

Buggy version: `WHERE order_date BETWEEN '2024-01-01' AND '2024-01-31'` on a real TIMESTAMP column (checked in DuckDB) returns only orders 1 and 2. Orders 3 and 4 (31 Jan afternoon and night) are lost. The sample table below stores the time as text, where order 2 would drop too, so the fixed query is what we run.

**SQL:**
```sql
SELECT order_id, order_date, amount
FROM orders
WHERE order_date >= '2024-01-01'
  AND order_date <  '2024-02-01'   -- half-open: includes all of 31 Jan
ORDER BY order_id;
```
**Output:** (orders 1-4; the 1 Feb order is correctly excluded)

| order_id | order_date | amount |
|---|---|---|
| 1 | 2024-01-15 10:30:00 | 500 |
| 2 | 2024-01-31 00:00:00 | 700 |
| 3 | 2024-01-31 14:45:00 | 1200 |
| 4 | 2024-01-31 23:59:00 | 300 |

**pandas equivalent:**
```python
# each table above is a DataFrame of the same name
result = orders[(orders.order_date >= '2024-01-01') & (orders.order_date < '2024-02-01')][['order_id','order_date','amount']]
```
Result (real output): same rows as the SQL output above.
**Edge cases:** Dates stored as text compare alphabetically; this works only for ISO format (YYYY-MM-DD). Wrapping the column in a function (`DATE(order_date) BETWEEN ...`) also works but stops an index being used. SQL Server `datetime` precision makes `<= '23:59:59.997'` hacks fragile; use the half-open range.
**Likely follow-ups:** 
- *Is BETWEEN inclusive?* Yes, both ends.
- *Can I use `CAST(order_date AS DATE)`?* Yes, but it is slower on big tables because the index on order_date cannot be used.
**Common mistakes:** Using `<= '2024-01-31 23:59:59'` (misses fractions of a second) or forgetting the time part exists at all.

### Q43 ⭐⭐ 🟡 How do you count how many different cities appear in the Employees table? How is COUNT(DISTINCT city) different from COUNT(city) and COUNT(*)?
**Asked at:** service MNC / analytics firm (general SQL-basics screens; no company-specific report found for this exact question)
**What the interviewer is checking:** Whether you know how COUNT treats NULLs and duplicates.
**Say this in the interview:** COUNT(*) counts rows, COUNT(city) counts rows where city is filled in, and COUNT(DISTINCT city) counts the different filled-in cities. NULLs are ignored by the last two.
**Explain simply:**
- COUNT(*): every row, NULL or not.
- COUNT(city): non-NULL values only, repeats included.
- COUNT(DISTINCT city): unique non-NULL values. NULL is not counted as a city.
- NULL means 'unknown or missing', not a value you can count.
**Example:** Of 6 employees, one has no city recorded, and Pune and Bengaluru each appear twice. The answers are 6, 5 and 3.
**Sample data:**
`employees`

| emp_id | name | city |
|---|---|---|
| 1 | Anita | Pune |
| 2 | Rahul | Pune |
| 3 | Sana | Bengaluru |
| 4 | Ankur | NULL |
| 5 | Priya | Hyderabad |
| 6 | Kavya | Bengaluru |

**SQL:**
```sql
SELECT COUNT(*)             AS all_rows,
       COUNT(city)          AS cities_filled,
       COUNT(DISTINCT city) AS distinct_cities
FROM employees;
```
**Output:**

| all_rows | cities_filled | distinct_cities |
|---|---|---|
| 6 | 5 | 3 |

**pandas equivalent:**
```python
# each table above is a DataFrame of the same name
result = pd.DataFrame({'all_rows':[len(employees)],
                       'cities_filled':[employees.city.count()],
                       'distinct_cities':[employees.city.nunique()]})
```
Result (real output): same rows as the SQL output above.
**Edge cases:** All-NULL column: COUNT(city) = 0. Case variants ('pune' vs 'Pune') count as separate cities in case-sensitive databases; clean with LOWER(TRIM(city)). SQL Server does not allow several columns inside COUNT(DISTINCT); use a subquery.
**Likely follow-ups:** 
- *How do you count NULL cities?* `COUNT(*) - COUNT(city)` or `SUM(CASE WHEN city IS NULL THEN 1 ELSE 0 END)`.
- *Does COUNT(1) differ from COUNT(*)?* No, same result.
**Common mistakes:** Saying COUNT(DISTINCT city) includes NULL as one more city. It does not.

### Q44 ⭐⭐ 🟡 Can DISTINCT and GROUP BY give the same result? When would you use which to list unique values?
**Asked at:** service MNC / analytics firm (general SQL-basics screens; no company-specific report found for this exact question)
**What the interviewer is checking:** Whether you see that two different tools can solve the same problem, and know when GROUP BY is the right one.
**Say this in the interview:** Yes. For just listing unique values, DISTINCT and GROUP BY give identical results. I use DISTINCT when I only want unique values, and GROUP BY the moment I also need a count, sum or average per group.
**Explain simply:**
- `SELECT DISTINCT city` removes repeated rows from the result.
- `GROUP BY city` makes one row per city and lets you add aggregates (COUNT, SUM).
- DISTINCT is shorter and states the intent; GROUP BY is needed for headcount per city.
- Databases usually plan both the same way.
**Example:** HR wants the list of cities we hire in (DISTINCT) versus how many people sit in each city (GROUP BY).
**Sample data:**
`employees`

| emp_id | name | city |
|---|---|---|
| 1 | Anita | Pune |
| 2 | Rahul | Pune |
| 3 | Sana | Bengaluru |
| 4 | Ankur | NULL |
| 5 | Priya | Hyderabad |
| 6 | Kavya | Bengaluru |

**SQL:**
```sql
SELECT DISTINCT city FROM employees ORDER BY city;
-- same unique list:
--   SELECT city FROM employees GROUP BY city ORDER BY city;
-- with a count, only GROUP BY works:
--   SELECT city, COUNT(*) AS headcount FROM employees GROUP BY city;
```
**Output:**

| city |
|---|
| NULL |
| Bengaluru |
| Hyderabad |
| Pune |

**pandas equivalent:**
```python
# each table above is a DataFrame of the same name
result = employees[['city']].drop_duplicates().sort_values('city', na_position='first')
```
Result (real output): same rows as the SQL output above.
**Edge cases:** NULL: both DISTINCT and GROUP BY keep one NULL row (the NULL group). It is listed first in SQLite and MySQL; PostgreSQL puts NULLs last in ascending order. DISTINCT applies to the whole row of selected columns, not just the first column.
**Likely follow-ups:** 
- *Which is faster?* Usually the same; check the query plan.
- *DISTINCT on two columns?* It de-duplicates the pair.
**Common mistakes:** Writing `SELECT DISTINCT(city), name` and thinking DISTINCT applies to city only; it applies to the whole row.

### Q45 ⭐⭐ 🟡 An `Attendance` table has emp_id, work_date and status ('Present', 'Absent', 'Leave'). Write a query listing each employee who was absent at least once in March 2025, with no repeated IDs.
**Asked at:** service MNC / analytics firm (general SQL-basics screens; no company-specific report found for this exact question)
**What the interviewer is checking:** Date-range filtering plus de-duplication in a realistic HR scenario.
**Say this in the interview:** I filter to status Absent and to March with a half-open date range, then use DISTINCT on emp_id so someone absent three times is listed once.
**Explain simply:**
- Filter rows first (WHERE), then remove repeats (DISTINCT).
- March = on or after 1 March and before 1 April; safe even if work_date has a time.
- Without DISTINCT, an employee absent twice appears twice.
**Example:** Employee 101 was absent on 3 and 10 March, so without DISTINCT 101 shows up twice. 103's absence was on 28 Feb and 101's on 1 April; both are out of range.
**Sample data:**
`attendance`

| emp_id | work_date | status |
|---|---|---|
| 101 | 2025-03-03 | Absent |
| 101 | 2025-03-10 | Absent |
| 102 | 2025-03-04 | Present |
| 102 | 2025-03-05 | Leave |
| 103 | 2025-02-28 | Absent |
| 103 | 2025-03-12 | Present |
| 101 | 2025-04-01 | Absent |
| 104 | 2025-03-20 | Absent |

**SQL:**
```sql
SELECT DISTINCT emp_id
FROM attendance
WHERE status = 'Absent'
  AND work_date >= '2025-03-01'
  AND work_date <  '2025-04-01'
ORDER BY emp_id;
```
**Output:**

| emp_id |
|---|
| 101 |
| 104 |

**pandas equivalent:**
```python
# each table above is a DataFrame of the same name
m = (attendance.status=='Absent') & (attendance.work_date>='2025-03-01') & (attendance.work_date<'2025-04-01')
result = attendance[m][['emp_id']].drop_duplicates().sort_values('emp_id')
```
Result (real output): same rows as the SQL output above.
**Edge cases:** Empty result is valid (nobody absent). Status spelling ('absent', 'ABSENT') may differ; check with LOWER(status). Use GROUP BY emp_id with COUNT(*) if you later need how many days.
**Likely follow-ups:** 
- *How many days each?* `GROUP BY emp_id` with `COUNT(*)`.
- *Only those absent 2+ times?* Add `HAVING COUNT(*) >= 2`.
**Common mistakes:** Using `BETWEEN '2025-03-01' AND '2025-03-31'` on a timestamp column, or forgetting DISTINCT.

### Q46 ⭐⭐ 🟡 Write a query to find employees whose salary is between 40,000 and 60,000 and who joined after 2022 and live in Bengaluru or Hyderabad, sorted by hire date.
**Asked at:** service MNC / analytics firm (general SQL-basics screens; no company-specific report found for this exact question)
**What the interviewer is checking:** Combining several conditions correctly with AND, BETWEEN, IN and ORDER BY.
**Say this in the interview:** I combine the filters with AND, use BETWEEN for the salary range, IN for the two cities, a date comparison for 'after 2022', and ORDER BY hire_date.
**Explain simply:**
- BETWEEN 40000 AND 60000 includes both ends.
- 'Joined after 2022' is ambiguous. I read it as hired from 1 Jan 2023 onwards (`hire_date >= '2023-01-01'`) and say so out loud.
- `city IN ('Bengaluru','Hyderabad')` is shorthand for two ORs.
**Example:** Of 7 employees, Anita, Ankur and Manoj pass every test. Manoj earns exactly 40,000, which BETWEEN includes.
**Sample data:**
`employees`

| emp_id | name | salary | hire_date | city |
|---|---|---|---|---|
| 1 | Anita | 45000 | 2023-03-15 | Bengaluru |
| 2 | Rahul | 52000 | 2022-11-20 | Hyderabad |
| 3 | Sana | 38000 | 2024-01-10 | Pune |
| 4 | Ankur | 60000 | 2023-06-05 | Hyderabad |
| 5 | Priya | 58000 | 2021-07-01 | Bengaluru |
| 6 | Kavya | 41000 | 2022-09-12 | Mumbai |
| 7 | Manoj | 40000 | 2024-05-02 | Hyderabad |

**SQL:**
```sql
SELECT emp_id, name, salary, hire_date, city
FROM employees
WHERE salary BETWEEN 40000 AND 60000
  AND hire_date >= '2023-01-01'
  AND city IN ('Bengaluru', 'Hyderabad')
ORDER BY hire_date;
```
**Output:**

| emp_id | name | salary | hire_date | city |
|---|---|---|---|---|
| 1 | Anita | 45000 | 2023-03-15 | Bengaluru |
| 4 | Ankur | 60000 | 2023-06-05 | Hyderabad |
| 7 | Manoj | 40000 | 2024-05-02 | Hyderabad |

**pandas equivalent:**
```python
# each table above is a DataFrame of the same name
m = employees.salary.between(40000,60000) & (employees.hire_date>='2023-01-01') & employees.city.isin(['Bengaluru','Hyderabad'])
result = employees[m].sort_values('hire_date')
```
Result (real output): same rows as the SQL output above.
**Edge cases:** Premise note: 'after 2022' could mean year > 2022 or after a specific date; state your reading. NULL salary or city rows are dropped automatically. Mixing AND with OR needs brackets.
**Likely follow-ups:** 
- *Newest first?* `ORDER BY hire_date DESC`.
- *Exclude the edges of BETWEEN?* Use `> 40000 AND < 60000`.
**Common mistakes:** Writing `city = 'Bengaluru' OR 'Hyderabad'` (not valid logic), or forgetting that BETWEEN includes both ends.

### Q47 ⭐⭐ 🟡 Write a query to find names with exactly five letters, and names whose second letter is 'a'.
**Asked at:** service MNC / analytics firm (general SQL-basics screens; no company-specific report found for this exact question)
**What the interviewer is checking:** Knowing the LIKE wildcards % and _ .
**Say this in the interview:** In LIKE, underscore means exactly one character and percent means any number of characters. Five letters is five underscores; second letter 'a' is underscore, then a, then percent.
**Explain simply:**
- `_` = exactly one character. `%` = zero or more characters.
- Five-letter names: `name LIKE '_____'` (5 underscores).
- Second letter 'a': `name LIKE '_a%'`.
- A 'wildcard' is a placeholder symbol that stands in for unknown characters.
**Example:** Rahul and Kavya are both: five letters and 'a' second. Sana has 'a' second but only four letters.
**Sample data:**
`employees`

| emp_id | name |
|---|---|
| 1 | Anita |
| 2 | Rahul |
| 3 | Sana |
| 4 | Ankur |
| 5 | Priya |
| 6 | Kavya |
| 7 | Manoj |

**SQL:**
```sql
SELECT name,
       CASE WHEN name LIKE '_____' THEN 'Y' ELSE 'N' END AS five_letters,
       CASE WHEN name LIKE '_a%'   THEN 'Y' ELSE 'N' END AS second_is_a
FROM employees
ORDER BY emp_id;
```
**Output:**

| name | five_letters | second_is_a |
|---|---|---|
| Anita | Y | N |
| Rahul | Y | Y |
| Sana | N | Y |
| Ankur | Y | N |
| Priya | Y | N |
| Kavya | Y | Y |
| Manoj | Y | Y |

**pandas equivalent:**
```python
# each table above is a DataFrame of the same name
result = employees[['name']].assign(
    five_letters=employees.name.str.len().eq(5).map({True:'Y',False:'N'}),
    second_is_a=employees.name.str[1].eq('a').map({True:'Y',False:'N'}))
```
Result (real output): same rows as the SQL output above.
**Edge cases:** Exactly-five alternative: `LENGTH(name) = 5` (SQL Server: `LEN`). Case: LIKE is case-insensitive in SQLite and MySQL (default collation), case-sensitive in PostgreSQL and Oracle. Trailing spaces in CHAR columns can break the length test. To filter instead of flag, move each pattern into WHERE.
**Likely follow-ups:** 
- *Names ending with 'a'?* `LIKE '%a'`.
- *Case-insensitive in PostgreSQL?* Use `ILIKE`.
**Common mistakes:** Using `*` as the wildcard, or miscounting the underscores.

### Q48 ⭐⭐ 🟡 What is the difference between NULL and an empty string '' in WHERE conditions? How do you find rows where email is missing in either form?
**Asked at:** service MNC / analytics firm (general SQL-basics screens; no company-specific report found for this exact question)
**What the interviewer is checking:** Whether you understand NULL as unknown, not as empty text, and that `= NULL` never works.
**Say this in the interview:** NULL means no value at all; '' is a real value that happens to be empty text. They behave differently in WHERE, so to find 'missing' emails I check for both with IS NULL OR empty.
**Explain simply:**
- `email = NULL` is never true. NULL needs `IS NULL`.
- `email = ''` finds only empty text, not NULL.
- A value with only spaces is a third case; TRIM catches it.
- Oracle is the exception: it treats '' as NULL.
**Example:** A candidate form saved Bilal's email as NULL (never asked) and Chitra's as '' (typed then deleted). Both are 'missing' for the recruiter.
**Sample data:**
`candidates`

| cand_id | name | email |
|---|---|---|
| 1 | Asha | asha@mail.com |
| 2 | Bilal | NULL |
| 3 | Chitra |  |
| 4 | Dev |     |
| 5 | Esha | esha@mail.com |

**SQL:**
```sql
SELECT cand_id, name, email
FROM candidates
WHERE email IS NULL OR TRIM(email) = ''
ORDER BY cand_id;
```
**Output:**

| cand_id | name | email |
|---|---|---|
| 2 | Bilal | NULL |
| 3 | Chitra |  |
| 4 | Dev |     |

**pandas equivalent:**
```python
# each table above is a DataFrame of the same name
result = candidates[candidates.email.isna() | (candidates.email.fillna('').str.strip()=='')]
```
Result (real output): same rows as the SQL output above.
**Edge cases:** `WHERE email <> ''` also drops NULL rows, because NULL <> '' is unknown. Shortcut: `COALESCE(TRIM(email),'') = ''`. Count NULLs with `COUNT(*) - COUNT(email)`. The output shows NULL for Bilal and blanks for Chitra and Dev.
**Likely follow-ups:** 
- *Why does `= NULL` return nothing?* Comparing with unknown gives unknown, and WHERE keeps only true rows.
- *NULL in Oracle?* '' and NULL are the same.
**Common mistakes:** Writing `WHERE email = NULL`, or checking only one of the two forms.

### Q49 ⭐ 🟢 Can you write a SELECT without a FROM clause? Show `SELECT 1 + 1` and `SELECT 'hello'`.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Basic SQL fluency and awareness of dialect differences.
**Say this in the interview:** Yes. SELECT can evaluate an expression or a literal without any table. PostgreSQL, MySQL, SQLite and SQL Server allow it; Oracle needs `FROM DUAL`.
**Explain simply:**
- Handy as a quick calculator or to test a function.
- A literal is a fixed value such as 'hello'.
- Oracle: `SELECT 1 + 1 FROM DUAL;`.
**Example:** Before writing a long date query, I run a tiny SELECT with no table to check that the function does what I think.
**SQL:**
```sql
SELECT 1 + 1 AS two, 'hello' AS greeting;
```
**Output:**

| two | greeting |
|---|---|
| 2 | hello |

**Edge cases:** Result is always one row. Oracle requires `FROM DUAL`; DB2 uses `FROM SYSIBM.SYSDUMMY1`.
**Likely follow-ups:** 
- *How do I list numbers 1 to 5?* A recursive CTE or a numbers table.
**Common mistakes:** Thinking FROM is always mandatory.

### Q50 ⭐ 🟢 How do you add comments in SQL, and does the semicolon matter at the end of a query?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Basic SQL hygiene.
**Say this in the interview:** Two dashes start a one-line comment, and slash-star ... star-slash wraps a multi-line one. The semicolon ends a statement; it is optional for a single query in most tools but needed to separate several.
**Explain simply:**
- `-- comment` runs to the end of the line (MySQL needs a space after the dashes).
- `/* comment */` can span lines.
- Semicolon: separates statements. SQL Server tolerates it missing, but a CTE after a previous statement requires one.
- MySQL also allows `#` comments.
**Example:** I leave a comment like `-- active employees only` above filters so my teammate understands the rule.
**SQL:**
```sql
-- one-line comment
SELECT 1 + 1 AS two  /* inline comment */;
```
**Output:**

| two |
|---|
| 2 |

**Edge cases:** A semicolon inside a string is fine. Missing semicolons between two statements cause errors in scripts. Comments are ignored by the engine, so they cost nothing.
**Likely follow-ups:** 
- *Do comments slow the query?* No, they are stripped before execution.
**Common mistakes:** Writing `--` with no space after it in MySQL, or leaving a `/*` comment unclosed.

### Q51 ⭐ 🟡 How do you do a case-insensitive search for names containing 'kumar' (LOWER, ILIKE, UPPER)? Does it matter for performance?
**Asked at:** service MNC / analytics firm (general SQL-basics screens; no company-specific report found for this exact question)
**What the interviewer is checking:** Case handling in text search and awareness of how it affects indexes.
**Say this in the interview:** I lower-case the column and compare with a lower-case pattern: `LOWER(name) LIKE '%kumar%'`. PostgreSQL also has ILIKE, which does the same thing in one word.
**Explain simply:**
- Whether LIKE ignores case depends on the database. MySQL and SQL Server (default settings) and SQLite (ASCII only) ignore it; PostgreSQL and Oracle do not.
- To be safe everywhere, wrap both sides: `LOWER(name) LIKE '%kumar%'` (UPPER works the same way).
- PostgreSQL only: `name ILIKE '%kumar%'` (not run here).
- Performance: a leading `%` means the database cannot use an ordinary index and must scan the whole table; wrapping the column in LOWER also blocks a normal index. Fixes: an expression index on LOWER(name) for prefix searches, or full-text search / trigram index for 'contains'.
**Example:** HR searching 'kumar' should also find 'KUMAR' and 'Kumar' but not mis-spelt rows. Note 'Kumari' also contains kumar, so say whether you want a whole-word match.
**Sample data:**
`employees`

| emp_id | name |
|---|---|
| 1 | Sanjay KUMAR |
| 2 | Anil Kumar |
| 3 | kumar Verma |
| 4 | Priya Nair |
| 5 | Rahul Kumari |

**SQL:**
```sql
SELECT emp_id, name
FROM employees
WHERE LOWER(name) LIKE '%kumar%'
ORDER BY emp_id;
```
**Output:**

| emp_id | name |
|---|---|
| 1 | Sanjay KUMAR |
| 2 | Anil Kumar |
| 3 | kumar Verma |
| 5 | Rahul Kumari |

**pandas equivalent:**
```python
# each table above is a DataFrame of the same name
result = employees[employees.name.str.lower().str.contains('kumar')]
```
Result (real output): same rows as the SQL output above.
**Edge cases:** NULL names never match. Accents and non-English characters need a proper collation. 'Kumari' matches the pattern; use a word-boundary regex if you need only 'Kumar'.
**Likely follow-ups:** 
- *Does it matter for performance?* Yes, on millions of rows: leading wildcard plus LOWER() forces a full scan.
- *Starts-with search?* `LIKE 'kumar%'` can use an index.
**Common mistakes:** Lower-casing the column but typing 'Kumar' in the pattern.

### Q52 ⭐ 🟡 Why does SELECT DISTINCT with ORDER BY sometimes give an error (the ORDER BY column must be in the SELECT list)? Explain with an example.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Understanding of how DISTINCT and ORDER BY interact logically.
**Say this in the interview:** DISTINCT first collapses rows to unique values, then ORDER BY sorts what is left. If I sort by a column that is not in the SELECT list, the database cannot tell which of the many hire dates to use for a city, so PostgreSQL and SQL Server refuse.
**Explain simply:**
- Pune appears twice with two different hire dates; after DISTINCT city there is one Pune row.
- ORDER BY hire_date is then ambiguous: 2022 or 2024?
- PostgreSQL error (not run here): `for SELECT DISTINCT, ORDER BY expressions must appear in select list`. SQL Server says the same in other words. SQLite is lenient (DuckDB accepted it too when I tried) and picks some value, which can silently give a wrong order.
- Fix: decide what you mean, such as latest hire date per city, using GROUP BY with an aggregate.
**Example:** HR wants cities listed by who joined most recently. 'Most recent hire in that city' is a clear question; 'DISTINCT city ORDER BY hire_date' is not.
**Sample data:**
`employees`

| emp_id | city | hire_date |
|---|---|---|
| 1 | Pune | 2022-01-10 |
| 2 | Pune | 2024-03-01 |
| 3 | Bengaluru | 2021-06-15 |
| 4 | Hyderabad | 2023-09-09 |
| 5 | Bengaluru | 2023-02-20 |

**SQL:**
```sql
SELECT city, MAX(hire_date) AS latest_hire
FROM employees
GROUP BY city
ORDER BY latest_hire DESC;
-- or sort by the select-list column:  SELECT DISTINCT city ... ORDER BY city;
```
**Output:**

| city | latest_hire |
|---|---|
| Pune | 2024-03-01 |
| Hyderabad | 2023-09-09 |
| Bengaluru | 2023-02-20 |

**pandas equivalent:**
```python
# each table above is a DataFrame of the same name
result = (employees.groupby('city', as_index=False).agg(latest_hire=('hire_date','max'))
          .sort_values('latest_hire', ascending=False))
```
Result (real output): same rows as the SQL output above.
**Edge cases:** With ORDER BY on a selected column, DISTINCT works in every dialect. Expressions like `ORDER BY UPPER(city)` must also appear in the select list. Same rule applies to window-function results.
**Likely follow-ups:** 
- *Why does GROUP BY allow ORDER BY MAX(...)?* The aggregate is a defined value per group.
- *Is this an Oracle issue too?* Yes, Oracle raises ORA-01791.
**Common mistakes:** Adding the ORDER BY column to the SELECT list just to silence the error; that changes the DISTINCT result back to many rows.

### Q53 ⭐ 🟡 Write a query to return only employees with an even emp_id (or odd). Which operator or function do you use?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Knowing the modulo (remainder) operator.
**Say this in the interview:** I use the remainder after dividing by 2. If emp_id % 2 is 0 the number is even; if it is 1 the number is odd.
**Explain simply:**
- `%` is the modulo operator: it returns the remainder. 7 % 2 = 1.
- MySQL, PostgreSQL, SQLite, SQL Server: `emp_id % 2 = 0`. Oracle has no `%`; use `MOD(emp_id, 2) = 0` (MOD also works in MySQL and PostgreSQL).
- Use `= 1` for odd.
**Example:** Splitting employees into two groups for an A/B survey: even IDs get form A and odd IDs get form B.
**Sample data:**
`employees`

| emp_id | name |
|---|---|
| 101 | Anita |
| 102 | Rahul |
| 103 | Sana |
| 104 | Ankur |
| 105 | Priya |
| 106 | Kavya |

**SQL:**
```sql
SELECT emp_id, name
FROM employees
WHERE emp_id % 2 = 0      -- use = 1 for odd; Oracle: MOD(emp_id, 2) = 0
ORDER BY emp_id;
```
**Output:**

| emp_id | name |
|---|---|
| 102 | Rahul |
| 104 | Ankur |
| 106 | Kavya |

**pandas equivalent:**
```python
# each table above is a DataFrame of the same name
result = employees[employees.emp_id % 2 == 0]
```
Result (real output): same rows as the SQL output above.
**Edge cases:** Negative numbers: in SQL Server and PostgreSQL -3 % 2 = -1, so test `<> 0` for odd instead of `= 1`. NULL ids never match. Works only on integers.
**Likely follow-ups:** 
- *Every 3rd employee?* `emp_id % 3 = 0`.
- *Alternate rows by order rather than ID?* Number rows with ROW_NUMBER() and apply the modulo to that.
**Common mistakes:** Using `/` (division) or forgetting that Oracle uses MOD().

### Q54 ⭐ 🟡 Why might `WHERE city = 'Pune'` miss rows that look like Pune? Think hidden spaces and upper/lower case, and how TRIM helps.
**Asked at:** service MNC / analytics firm (general SQL-basics screens; no company-specific report found for this exact question)
**What the interviewer is checking:** Data-cleaning instinct: the data that looks right but is not.
**Say this in the interview:** The equals sign compares every character. 'Pune ' with a trailing space, ' PUNE' with a leading space, or 'pune' in lower case are different strings, so they are missed. I clean the value with TRIM and LOWER before comparing.
**Explain simply:**
- TRIM removes spaces at the start and end (SQL Server older versions: `LTRIM(RTRIM(x))`).
- LOWER makes the case uniform. Databases differ: MySQL and SQL Server compare case-insensitively by default, PostgreSQL and Oracle do not.
- MySQL ignores trailing spaces in `=`; PostgreSQL does not for text.
- Better long-term: clean the data when it is loaded.
**Example:** A hiring form let people type their city. 'Pune', 'Pune ', 'pune' and ' PUNE' are all one city in reality, so headcount reports under-count Pune.
**Sample data:**
`employees`

| emp_id | name | city |
|---|---|---|
| 1 | Anita | Pune |
| 2 | Rahul | Pune  |
| 3 | Sana | pune |
| 4 | Ankur |  PUNE |
| 5 | Priya | Pune |

Plain `WHERE city = 'Pune'` returns only the rows below (in SQLite, which is case-sensitive for `=`):

| emp_id | city |
|---|---|
| 1 | Pune |
| 5 | Pune |

**SQL:**
```sql
SELECT emp_id, name, city
FROM employees
WHERE LOWER(TRIM(city)) = 'pune'
ORDER BY emp_id;
```
**Output:**

| emp_id | name | city |
|---|---|---|
| 1 | Anita | Pune |
| 2 | Rahul | Pune  |
| 3 | Sana | pune |
| 4 | Ankur |  PUNE |
| 5 | Priya | Pune |

**pandas equivalent:**
```python
# each table above is a DataFrame of the same name
result = employees[employees.city.str.strip().str.lower()=='pune']
```
Result (real output): same rows as the SQL output above.
**Edge cases:** A non-breaking space (copied from web or Excel) is not removed by TRIM; replace it with `REPLACE(city, CHAR(160), ' ')`. NULL city is never equal to anything. Wrapping the column in functions stops index use, so also fix the data at the source.
**Likely follow-ups:** 
- *How do I find the dirty rows?* `WHERE city <> TRIM(city)` or compare LENGTH(city) with LENGTH(TRIM(city)).
- *Why not LIKE '%pune%'?* It also matches 'Pune City' or 'Punekar'.
**Common mistakes:** Trimming the column but forgetting the case, or trusting that the data is clean.

### Q55 ⭐ 🟡 How do you pick 10 random rows from a table? Why is ORDER BY RANDOM() slow on very large tables?
**Asked at:** service MNC / analytics firm (general SQL-basics screens; no company-specific report found for this exact question)
**What the interviewer is checking:** Sampling and an awareness of performance on big tables.
**Say this in the interview:** I sort by a random number and take the first 10: `ORDER BY RANDOM() LIMIT 10` in PostgreSQL and SQLite. On huge tables I avoid it because it has to give every row a random number and sort them all.
**Explain simply:**
- PostgreSQL/SQLite: `ORDER BY RANDOM() LIMIT 10`. MySQL: `ORDER BY RAND() LIMIT 10`. SQL Server: `SELECT TOP 10 ... ORDER BY NEWID()`. Oracle: `ORDER BY DBMS_RANDOM.VALUE FETCH FIRST 10 ROWS ONLY`. (Only the SQLite form was run here.)
- Why slow: with 50 million rows it computes 50 million random values and sorts them (O(n log n)), just to keep 10.
- Faster for 'about 1%': `TABLESAMPLE SYSTEM (1)` in PostgreSQL/SQL Server (not run here), which reads random pages instead of every row. It is approximate and block-based, so rows may be clustered.
- The result changes on every run; for a repeatable sample set a seed in pandas or sample in the application.
**Example:** HR wants 10 random exit-interview candidates from 12 leavers; a quick random pick is fine at this size.
**Sample data:**
`employees`

| emp_id | name |
|---|---|
| 1 | Anita |
| 2 | Rahul |
| 3 | Sana |
| 4 | Ankur |
| 5 | Priya |
| 6 | Kavya |
| 7 | Manoj |
| 8 | Meena |
| 9 | Kiran |
| 10 | Divya |
| 11 | Rohan |
| 12 | Isha |

**SQL:**
```sql
SELECT emp_id, name
FROM employees
ORDER BY RANDOM()
LIMIT 10;
```
**Output:** (one sample run; your run will differ, which is the point)

| emp_id | name |
|---|---|
| 11 | Rohan |
| 9 | Kiran |
| 6 | Kavya |
| 1 | Anita |
| 10 | Divya |
| 2 | Rahul |
| 8 | Meena |
| 12 | Isha |
| 5 | Priya |
| 7 | Manoj |

**pandas equivalent:**
```python
# each table above is a DataFrame of the same name
result = employees.sample(n=10, random_state=42)
```
Result (real output): ten randomly chosen rows; they differ from the SQL run, because both are random (random_state=42 makes the pandas pick repeatable, SQL has no easy seed).
**Edge cases:** Table smaller than N returns all rows. Needs a unique-key column if you want to re-fetch the same sample. Do not use `WHERE id = RANDOM()*max(id)`; gaps in ids bias the result.
**Likely follow-ups:** 
- *Repeatable random sample?* Hash the id (e.g. `WHERE MOD(emp_id, 100) = 7`) or store the chosen ids.
- *Is TABLESAMPLE exact?* No, approximate.
**Common mistakes:** Using RANDOM() in WHERE and expecting 10 rows, or running ORDER BY RANDOM() on a billion-row table.

### Q56 ⭐ 🟡 Can DISTINCT hide a mistake in your query? Describe a case where it removes duplicates that you should have investigated instead.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you use DISTINCT as a quick fix or look for the root cause.
**Say this in the interview:** Yes, DISTINCT can paper over a join that duplicates rows. I treat unexpected duplicates as a signal to investigate the join or data first, because the same bug often corrupts totals even if the list looks clean.
**Explain simply:**
- 'Fan-out' means a join returns several rows for one employee, for example when each employee has several department-history rows.
- `SELECT DISTINCT name` makes the list look right, but `SUM(salary)` over the same join counts Anita twice.
- Real fix: join to the right grain (one row per employee, e.g. current department only), or aggregate before joining.
- Quick check: `GROUP BY emp_id HAVING COUNT(*) > 1` finds which keys are duplicated.
**Example:** Anita has two department records (HR, Finance). Total payroll should be 150,000; the joined sum gives 200,000, a 50,000 over-statement that DISTINCT on the name list never reveals.
**Sample data:**
`employees`

| emp_id | name | salary |
|---|---|---|
| 1 | Anita | 50000 |
| 2 | Rahul | 60000 |
| 3 | Sana | 40000 |

`dept_history`

| emp_id | dept |
|---|---|
| 1 | HR |
| 1 | Finance |
| 2 | HR |
| 3 | Ops |

With DISTINCT the list looks fine:

| name | salary |
|---|---|
| Anita | 50000 |
| Rahul | 60000 |
| Sana | 40000 |

but the same join overstates payroll:

| total_salary |
|---|
| 200000 |

The diagnostic that exposes the duplication:

**SQL:**
```sql
SELECT e.emp_id, e.name, COUNT(*) AS rows_after_join
FROM employees e
JOIN dept_history d ON d.emp_id = e.emp_id
GROUP BY e.emp_id, e.name
HAVING COUNT(*) > 1;
```
**Output:**

| emp_id | name | rows_after_join |
|---|---|---|
| 1 | Anita | 2 |

**pandas equivalent:**
```python
# each table above is a DataFrame of the same name
j = employees.merge(dept_history, on='emp_id')
result = (j.groupby(['emp_id','name']).size().reset_index(name='rows_after_join')
          .query('rows_after_join > 1'))
```
Result (real output): same rows as the SQL output above.
**Edge cases:** Legitimate DISTINCT: de-duplicating a genuinely repeated attribute (list of cities). Suspicious DISTINCT: appears with many columns or after several joins. Exact-duplicate rows in the source table are a data-quality issue to report, not hide.
**Likely follow-ups:** 
- *When is DISTINCT fine?* When duplicates are expected and harmless, such as a list of unique cities.
- *Does DISTINCT slow queries?* It adds a sort or hash step.
**Common mistakes:** Adding DISTINCT whenever the row count looks too high, without asking why.

### Q57 ⭐ 🟡 Write a query to find all employees whose names contain 'an' but do not start with 'S'.
**Asked at:** service MNC / analytics firm (general SQL-basics screens; no company-specific report found for this exact question)
**What the interviewer is checking:** Combining LIKE and NOT LIKE patterns and noticing case and NULL.
**Say this in the interview:** I use LIKE '%an%' for 'contains an' and NOT LIKE 'S%' for 'does not start with S', joined by AND. To ignore case I lower-case both parts.
**Explain simply:**
- `%an%` means 'an' anywhere in the name.
- `NOT LIKE 's%'` removes names beginning with S.
- LOWER makes it case-insensitive, so 'Anita' and 'Ankur' (capital A) are found even in PostgreSQL where LIKE is case-sensitive.
- NULL names are dropped because NULL LIKE anything is unknown.
**Example:** From ten names, Sanjay, Sana and Shanti contain 'an' but start with S, so they are excluded.
**Sample data:**
`employees`

| emp_id | name |
|---|---|
| 1 | Sanjay |
| 2 | Aman |
| 3 | Rohan |
| 4 | Anita |
| 5 | Sana |
| 6 | Ankur |
| 7 | Meena |
| 8 | Shanti |
| 9 | Kiran |
| 10 | NULL |

**SQL:**
```sql
SELECT emp_id, name
FROM employees
WHERE LOWER(name) LIKE '%an%'
  AND LOWER(name) NOT LIKE 's%'
ORDER BY emp_id;
```
**Output:**

| emp_id | name |
|---|---|
| 2 | Aman |
| 3 | Rohan |
| 4 | Anita |
| 6 | Ankur |
| 9 | Kiran |

**pandas equivalent:**
```python
# each table above is a DataFrame of the same name
low = employees.name.str.lower()
result = employees[low.str.contains('an', na=False) & ~low.str.startswith('s', na=True)]
```
Result (real output): same rows as the SQL output above.
**Edge cases:** NULL: excluded by both conditions. 'Not starting with S' is case-dependent; decide whether 'sanjay' in lower case counts. PostgreSQL shortcut: `name ILIKE '%an%' AND name NOT ILIKE 's%'`.
**Likely follow-ups:** 
- *Contains 'an' but not at the end?* Add `AND LOWER(name) NOT LIKE '%an'`.
- *Name has exactly one 'an'?* Compare LENGTH before and after REPLACE.
**Common mistakes:** Writing `NOT LIKE '%S'` (ends with S) or forgetting that case matters in PostgreSQL and Oracle.

### Q58 ⭐ 🔴 How do you search for a value that contains the characters % or _ themselves (e.g. a discount code '20%OFF')? What does ESCAPE do?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Awareness that % and _ are special in LIKE, and how to switch that off.
**Say this in the interview:** In LIKE, % and _ are wildcards. To match them as plain characters I put an escape character in front and declare it with ESCAPE: `LIKE '20!%OFF' ESCAPE '!'`.
**Explain simply:**
- `ESCAPE '!'` tells the database that a character after `!` is literal, not a wildcard.
- Pick any rarely used character; backslash is the default in MySQL and PostgreSQL, but declaring ESCAPE is clearer and portable.
- Same for underscore: `'SAVE!_10' ESCAPE '!'` matches only SAVE_10, not SAVEX10.
- SQL Server also allows brackets: `LIKE '20[%]OFF'`.
**Example:** A discount-code table has '20%OFF'. If I search with a plain pattern '20%OFF' I also get '20PCTOFF' and '200OFF', and an HR-benefits voucher check would accept wrong codes.
**Sample data:**
`codes`

| code_id | code |
|---|---|
| 1 | 20%OFF |
| 2 | 20PCTOFF |
| 3 | 200OFF |
| 4 | SAVE_10 |
| 5 | SAVEX10 |

Without ESCAPE, `LIKE '20%OFF'` over-matches:

| code |
|---|
| 20%OFF |
| 20PCTOFF |
| 200OFF |

**SQL:**
```sql
SELECT code
FROM codes
WHERE code LIKE '20!%OFF' ESCAPE '!'
ORDER BY code_id;
```
**Output:**

| code |
|---|
| 20%OFF |

**pandas equivalent:**
```python
# each table above is a DataFrame of the same name
result = codes[codes.code == '20%OFF'][['code']]
```
Result (real output): same rows as the SQL output above.
**Edge cases:** If the code contains the escape character itself, double it ('!!'). ESCAPE must be a single character. Exact-match alternative: `code = '20%OFF'` (no wildcard needed at all). Bind parameters: escape user input before putting it in LIKE.
**Likely follow-ups:** 
- *Why not just use =?* Use = when you want the whole value; ESCAPE is for partial matches such as `'%20!%OFF%'`.
- *Underscore?* Same approach.
**Common mistakes:** Forgetting the ESCAPE clause, or escaping with a backslash on a database where that is not the default.

### Q59 ⭐ 🔴 What does FETCH FIRST n ROWS WITH TIES do, and how is it different from LIMIT n?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Understanding of ties at the cut-off of a Top-N list.
**Say this in the interview:** FETCH FIRST n ROWS WITH TIES returns n rows and then also every further row that has the same sort value as the nth row. LIMIT n returns exactly n rows and cuts through a tie arbitrarily.
**Explain simply:**
- 'Tie' means two or more rows with the same value in the ORDER BY column.
- PostgreSQL 13+, Oracle 12c+ and SQL Server (`TOP (n) WITH TIES`) support it; MySQL and SQLite do not. It needs an ORDER BY. (Not run here: neither SQLite nor DuckDB supports it.)
- Standard syntax: `ORDER BY salary DESC FETCH FIRST 3 ROWS WITH TIES`.
- Equivalent that does run everywhere with window functions: keep rows where `RANK() <= n`.
**Example:** Top 3 salaries: Anita 90,000, then three people on 85,000. LIMIT 3 shows only two of the three 85,000 earners and which one is dropped is arbitrary, which is unfair in a pay-review list.
**Sample data:**
`employees`

| emp_id | name | salary |
|---|---|---|
| 1 | Anita | 90000 |
| 2 | Rahul | 85000 |
| 3 | Sana | 85000 |
| 4 | Ankur | 85000 |
| 5 | Priya | 70000 |
| 6 | Kavya | 60000 |

`ORDER BY salary DESC, emp_id LIMIT 3` returns exactly 3 rows and drops one of the 85,000 earners:

| name | salary |
|---|---|
| Anita | 90000 |
| Rahul | 85000 |
| Sana | 85000 |

**SQL:**
```sql
-- PostgreSQL 13+ / Oracle 12c+ (not run here):
--   SELECT name, salary FROM employees ORDER BY salary DESC FETCH FIRST 3 ROWS WITH TIES;
-- SQL Server (not run here): SELECT TOP (3) WITH TIES name, salary FROM employees ORDER BY salary DESC;
-- Runnable equivalent (SQLite / any engine with window functions):
SELECT name, salary
FROM (SELECT name, salary, RANK() OVER (ORDER BY salary DESC) AS rnk FROM employees)
WHERE rnk <= 3
ORDER BY salary DESC, name;
```
**Output:**

| name | salary |
|---|---|
| Anita | 90000 |
| Ankur | 85000 |
| Rahul | 85000 |
| Sana | 85000 |

**pandas equivalent:**
```python
# each table above is a DataFrame of the same name
r = employees.salary.rank(method='min', ascending=False)
result = employees[r <= 3].sort_values(['salary','name'], ascending=[False,True])[['name','salary']]
```
Result (real output): same rows as the SQL output above.
**Edge cases:** Without a tie-break column LIMIT is not repeatable between runs. WITH TIES can return more than n rows (here 4). It cannot be used with OFFSET in some databases (SQL Server needs TOP, not OFFSET).
**Likely follow-ups:** 
- *Top 3 distinct salary values instead?* Use DENSE_RANK.
- *Is PERCENT possible?* `FETCH FIRST 10 PERCENT ROWS ONLY` in Oracle/PostgreSQL 13+.
**Common mistakes:** Using LIMIT for 'top 3 earners' and being surprised that tied people are silently dropped.

### Q60 ⭐ 🔴 Why does a big OFFSET get slow for deep pages, and what is keyset (seek) pagination?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Practical thinking about performance on large paginated lists.
**Say this in the interview:** OFFSET makes the database read and throw away all the skipped rows every time, so page 5,000 is much slower than page 1. Keyset (seek) pagination instead remembers the last row of the previous page and says 'give me rows after this one', which can jump straight there using an index.
**Explain simply:**
- Pagination = showing results page by page (a page size of 3 here, 50 on a real screen).
- `LIMIT 3 OFFSET 3` scans 6 rows to return 3. At OFFSET 1,000,000 it scans a million rows each time, and rows can shift between pages if data changes.
- Keyset: `WHERE (salary, emp_id) < (last_salary, last_emp_id) ORDER BY salary DESC, emp_id DESC LIMIT 3`.
- The sort must include a unique column (emp_id) so the 'last seen' position is exact.
- Trade-off: you cannot jump to 'page 47'; only next or previous. Row-value comparison `(a,b) < (x,y)` works in PostgreSQL, MySQL and SQLite; SQL Server needs `a < x OR (a = x AND b < y)`.
**Example:** An HR portal listing 2 million attendance records: next-page should stay fast, so the app sends the last emp_id seen back with each click.
**Sample data:**
`employees`

| emp_id | name | salary |
|---|---|---|
| 1 | Anita | 90000 |
| 2 | Rahul | 85000 |
| 3 | Sana | 85000 |
| 4 | Ankur | 85000 |
| 5 | Priya | 70000 |
| 6 | Kavya | 70000 |
| 7 | Manoj | 65000 |
| 8 | Meena | 60000 |
| 9 | Kiran | 60000 |
| 10 | Divya | 55000 |
| 11 | Rohan | 50000 |
| 12 | Isha | 45000 |

For comparison, the OFFSET version of a page (`ORDER BY salary DESC, emp_id DESC`, skipping 3 rows):

| emp_id | name | salary |
|---|---|---|
| 2 | Rahul | 85000 |
| 6 | Kavya | 70000 |
| 5 | Priya | 70000 |

**SQL:**
```sql
-- Page 2 of 3 rows, sorted by salary DESC then emp_id DESC.
-- Last row of page 1 was (salary 85000, emp_id 3).
SELECT emp_id, name, salary
FROM employees
WHERE (salary, emp_id) < (85000, 3)
ORDER BY salary DESC, emp_id DESC
LIMIT 3;
```
**Output:**

| emp_id | name | salary |
|---|---|---|
| 2 | Rahul | 85000 |
| 6 | Kavya | 70000 |
| 5 | Priya | 70000 |

**pandas equivalent:**
```python
# each table above is a DataFrame of the same name
s = employees.sort_values(['salary','emp_id'], ascending=[False,False])
after = s[(s.salary < 85000) | ((s.salary == 85000) & (s.emp_id < 3))]
result = after.head(3)
```
Result (real output): same rows as the SQL output above.
**Edge cases:** If the sort column has NULLs, row-value comparisons behave unpredictably; filter or COALESCE them. Descending sort needs the comparison direction flipped. Index on (salary DESC, emp_id DESC) makes the seek fast.
**Likely follow-ups:** 
- *How do I go to the previous page?* Reverse both comparison and order, then re-reverse the page.
- *Does OFFSET cause duplicates between pages?* Yes, if rows are inserted meanwhile.
**Common mistakes:** Keyset on a non-unique column alone (ties get skipped), or mixing the sort and the filter columns.

### Q61 ⭐ 🔴 Write a query to find employees whose name starts and ends with a vowel using LIKE or a regular expression.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Text pattern matching and handling of first and last characters.
**Say this in the interview:** The portable way is to check the first and last letters with SUBSTR and IN. LIKE alone cannot say 'any vowel', so it needs regex (PostgreSQL `~*`, MySQL `REGEXP`) or one condition per vowel.
**Explain simply:**
- 'Vowel' means a, e, i, o, u.
- Portable: `LOWER(SUBSTR(name,1,1)) IN ('a','e','i','o','u')` and the same for the last letter (`SUBSTR(name,-1,1)`; SQL Server uses `RIGHT(name,1)`).
- Regex (PostgreSQL, not run here): `name ~* '^[aeiou].*[aeiou]$'`. MySQL: `name REGEXP '^[aeiou].*[aeiou]$'`. SQL Server: `name LIKE '[aeiou]%[aeiou]'` (it supports character classes in LIKE).
- `^` and `$` mean start and end of the text.
**Example:** Out of Anita, Esha, Uma and Ira, all start and end with a vowel; Omkar ends with 'r' and Ravi starts with 'R'.
**Sample data:**
`employees`

| emp_id | name |
|---|---|
| 1 | Anita |
| 2 | Esha |
| 3 | Uma |
| 4 | Omkar |
| 5 | Ishaan |
| 6 | Aarav |
| 7 | Ira |
| 8 | Indu |
| 9 | Ravi |
| 10 | A |

**SQL:**
```sql
SELECT emp_id, name
FROM employees
WHERE LOWER(SUBSTR(name, 1, 1))  IN ('a','e','i','o','u')
  AND LOWER(SUBSTR(name, -1, 1)) IN ('a','e','i','o','u')
ORDER BY emp_id;
```
**Output:**

| emp_id | name |
|---|---|
| 1 | Anita |
| 2 | Esha |
| 3 | Uma |
| 7 | Ira |
| 8 | Indu |
| 10 | A |

**pandas equivalent:**
```python
# each table above is a DataFrame of the same name
result = employees[employees.name.str.match(r'(?i)^[aeiou](.*[aeiou])?$')]
```
Result (real output): same rows as the SQL output above.
**Edge cases:** Single-letter name 'A' counts here (first and last letter are the same); the regex `^[aeiou].*[aeiou]$` would need two letters, so I made the second part optional in pandas. 'Y' is sometimes a vowel; decide. Accented letters and trailing spaces need cleaning first.
**Likely follow-ups:** 
- *Ends with a consonant?* Use NOT IN on the last letter.
- *Why SUBSTR over LIKE?* LIKE has no 'one of these characters' syntax except in SQL Server.
**Common mistakes:** Writing `LIKE 'aeiou%'` (that means the literal text 'aeiou'), or forgetting upper-case names.

