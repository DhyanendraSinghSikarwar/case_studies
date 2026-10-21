# Book 2 — SQL | Part 3: Joins (inner, left, right, full, self, cross)

- **Target:** 70 questions (plan.md Section 6)
- **Actual:** 77 questions
- **Scope:** Join concepts, INNER/LEFT/RIGHT/FULL/SELF/CROSS joins, anti-joins, join pitfalls (NULLs, duplicates, fan-out), join-based business queries. Difficulty 🟢🟡 with a few 🔴.

### Q1 ⭐⭐⭐ 🟢 What is a JOIN in SQL, and why do we need joins?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand that data lives in several tables and a join stitches them together.
**Say this in the interview:** A join combines rows from two tables side by side using a matching column. We keep data in separate tables to avoid repeating it, so we need joins to get the full picture back.
**Explain simply:**
- A **table** is a grid of rows and columns, like one Excel sheet. Real databases split data across many sheets: one for employees, one for departments.
- A **join** is like VLOOKUP done for every row at once: it looks at a shared column (the **join key**) and pulls matching rows together.
- Why split data at all? Storing 'Analytics' once in a departments table, instead of typing it on 200 employee rows, avoids typos and makes updates easy (this is called normalisation).
- Without joins you could not answer 'which department is each employee in' in one result.
**Example:** HR system: the employees sheet holds only dept_id (20); the departments sheet says 20 = Analytics. A join shows 'Ravi - Analytics' in one row.
**Sample data:**

`employees`

| emp_id | name | dept_id | manager_id | salary |
|---|---|---|---|---|
| 1 | Asha | 10 | NULL | 90000 |
| 2 | Ravi | 20 | 1 | 70000 |
| 3 | Meera | 20 | 2 | 75000 |
| 4 | Kiran | 30 | 1 | 60000 |
| 5 | Sana | NULL | 2 | 50000 |
| 6 | Tom | 10 | 1 | 55000 |

`departments`

| dept_id | dept_name |
|---|---|
| 10 | HR |
| 20 | Analytics |
| 30 | Finance |
| 40 | Legal |

**SQL:**
```sql
SELECT e.name, d.dept_name
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
ORDER BY e.emp_id;
```
**Output:**

| name | dept_name |
|---|---|
| Asha | HR |
| Ravi | Analytics |
| Meera | Analytics |
| Kiran | Finance |
| Tom | HR |

**pandas equivalent:**
```python
result = emp.merge(dept, on='dept_id', how='inner')[['name','dept_name']]  # emp, dept = the two tables as DataFrames
```
**Edge cases:** Employees with a NULL dept_id (Sana) or departments with no staff (Legal) vanish from an INNER JOIN. Duplicate keys in the lookup table multiply rows.
**Likely follow-ups:** 1) Which join is the default? INNER. 2) What if the key is missing on one side? Use an outer join (LEFT/RIGHT/FULL).
**Common mistakes:** Forgetting the ON condition (every row pairs with every row), or joining on the wrong column such as name instead of id.

### Q2 ⭐⭐⭐ 🟢 What are the different types of joins in SQL? Name them with a one-line meaning each.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you name the join types and say what each keeps.
**Say this in the interview:** There are five to know: INNER keeps only matches, LEFT keeps everything from the left table, RIGHT keeps everything from the right, FULL keeps everything from both, and CROSS pairs every row with every row. A SELF join is not a separate type; it is any join of a table to itself.
**Explain simply:**
- **INNER JOIN**: only rows with a match in both tables.
- **LEFT (OUTER) JOIN**: all left rows; right columns are NULL (empty) when there is no match.
- **RIGHT (OUTER) JOIN**: the mirror image of LEFT.
- **FULL (OUTER) JOIN**: all rows from both; NULL where either side has no match.
- **CROSS JOIN**: every left row with every right row (no key needed). **SELF JOIN**: a table joined to itself under two aliases (nicknames).
**Example:** 6 employees and 4 departments: INNER gives 5 rows (Sana has no department), LEFT 6, RIGHT 6 (Legal has no staff), FULL 7, CROSS 24 (6 x 4).
**Sample data:**

`employees`

| emp_id | name | dept_id | manager_id | salary |
|---|---|---|---|---|
| 1 | Asha | 10 | NULL | 90000 |
| 2 | Ravi | 20 | 1 | 70000 |
| 3 | Meera | 20 | 2 | 75000 |
| 4 | Kiran | 30 | 1 | 60000 |
| 5 | Sana | NULL | 2 | 50000 |
| 6 | Tom | 10 | 1 | 55000 |

`departments`

| dept_id | dept_name |
|---|---|
| 10 | HR |
| 20 | Analytics |
| 30 | Finance |
| 40 | Legal |

**SQL:**
```sql
SELECT 'INNER' AS join_type, COUNT(*) AS rows_returned FROM employees e INNER JOIN departments d ON e.dept_id = d.dept_id
UNION ALL SELECT 'LEFT',  COUNT(*) FROM employees e LEFT JOIN departments d ON e.dept_id = d.dept_id
UNION ALL SELECT 'RIGHT', COUNT(*) FROM employees e RIGHT JOIN departments d ON e.dept_id = d.dept_id
UNION ALL SELECT 'FULL',  COUNT(*) FROM employees e FULL OUTER JOIN departments d ON e.dept_id = d.dept_id
UNION ALL SELECT 'CROSS', COUNT(*) FROM employees e CROSS JOIN departments d;
```
**Output:**

| join_type | rows_returned |
|---|---|
| INNER | 5 |
| LEFT | 6 |
| RIGHT | 6 |
| FULL | 7 |
| CROSS | 24 |

**Edge cases:** Dialects: MySQL has no FULL OUTER JOIN (use LEFT UNION RIGHT, see Q41). SQLite supports RIGHT/FULL from 3.39. PostgreSQL and SQL Server support all.
**Likely follow-ups:** 1) Is the OUTER keyword required? No, LEFT JOIN = LEFT OUTER JOIN. 2) Is SELF JOIN a keyword? No.
**Common mistakes:** Calling SELF JOIN a separate syntax, or thinking a CROSS JOIN needs ON.

### Q3 ⭐⭐⭐ 🟢 What is the difference between an INNER JOIN and an OUTER JOIN?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know that outer joins keep unmatched rows and inner joins drop them.
**Say this in the interview:** An inner join returns only rows that match in both tables. An outer join also keeps the unmatched rows from one side (LEFT, RIGHT) or both (FULL) and fills the gaps with NULL.
**Explain simply:**
- **Matched** means the join key exists in both tables.
- INNER: matched only. OUTER: matched rows plus the unmatched rows of the 'kept' side.
- **NULL** means 'unknown/no value', not zero and not blank text.
- Use INNER when a missing match is irrelevant; use OUTER when you must not lose rows (e.g., all employees, even those not yet assigned a department).
**Example:** Headcount report: INNER JOIN would show 5 of 6 employees; the LEFT JOIN below shows all 6, with Sana's department as NULL, so HR can fix the data.
**Sample data:**

`employees`

| emp_id | name | dept_id | manager_id | salary |
|---|---|---|---|---|
| 1 | Asha | 10 | NULL | 90000 |
| 2 | Ravi | 20 | 1 | 70000 |
| 3 | Meera | 20 | 2 | 75000 |
| 4 | Kiran | 30 | 1 | 60000 |
| 5 | Sana | NULL | 2 | 50000 |
| 6 | Tom | 10 | 1 | 55000 |

`departments`

| dept_id | dept_name |
|---|---|
| 10 | HR |
| 20 | Analytics |
| 30 | Finance |
| 40 | Legal |

**SQL:**
```sql
SELECT e.name, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id
ORDER BY e.emp_id;
```
**Output:**

| name | dept_name |
|---|---|
| Asha | HR |
| Ravi | Analytics |
| Meera | Analytics |
| Kiran | Finance |
| Sana | NULL |
| Tom | HR |

**pandas equivalent:**
```python
result = emp.merge(dept, on='dept_id', how='left')[['name','dept_name']]
```
**Edge cases:** NULL keys never match, so Sana stays unmatched. Output has NULLs you may need to handle with COALESCE.
**Likely follow-ups:** 1) Which is faster? INNER can be cheaper because it discards rows early. 2) Is LEFT JOIN the same as LEFT OUTER JOIN? Yes.
**Common mistakes:** Saying OUTER JOIN returns 'only non-matching rows'. It returns matching plus non-matching.

### Q4 ⭐⭐⭐ 🟢 What does an INNER JOIN return? Explain with two small tables (employees and departments).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you apply INNER JOIN and predict the result.
**Say this in the interview:** INNER JOIN returns only the rows whose join key appears in both tables. Here it drops Sana (no department) and the Legal department (no employees).
**Explain simply:**
- The **ON** clause says how to match: e.dept_id = d.dept_id.
- **Aliases** (e, d) are short nicknames for tables so the query is easier to type and read.
- Each employee row finds its department row; unmatched rows on either side disappear.
**Example:** 6 employees, 4 departments: the result has 5 rows. Sana (dept_id NULL) and Legal (dept 40) are missing.
**Sample data:**

`employees`

| emp_id | name | dept_id | manager_id | salary |
|---|---|---|---|---|
| 1 | Asha | 10 | NULL | 90000 |
| 2 | Ravi | 20 | 1 | 70000 |
| 3 | Meera | 20 | 2 | 75000 |
| 4 | Kiran | 30 | 1 | 60000 |
| 5 | Sana | NULL | 2 | 50000 |
| 6 | Tom | 10 | 1 | 55000 |

`departments`

| dept_id | dept_name |
|---|---|
| 10 | HR |
| 20 | Analytics |
| 30 | Finance |
| 40 | Legal |

**SQL:**
```sql
SELECT e.emp_id, e.name, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id
ORDER BY e.emp_id;
```
**Output:**

| emp_id | name | dept_name |
|---|---|---|
| 1 | Asha | HR |
| 2 | Ravi | Analytics |
| 3 | Meera | Analytics |
| 4 | Kiran | Finance |
| 6 | Tom | HR |

**pandas equivalent:**
```python
result = emp.merge(dept, on='dept_id', how='inner')[['emp_id','name','dept_name']].sort_values('emp_id')
```
**Edge cases:** NULL dept_id never matches. If departments had a duplicate dept_id, employees would repeat.
**Likely follow-ups:** 1) How many rows at most? Employees x matching departments per key. 2) Is JOIN alone the same as INNER JOIN? Yes.
**Common mistakes:** Expecting unmatched employees to show up; forgetting ORDER BY and assuming a fixed row order.

### Q5 ⭐⭐⭐ 🟢 What does a LEFT JOIN return? Explain with two small tables (customers and orders).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know LEFT JOIN keeps every left row.
**Say this in the interview:** LEFT JOIN returns every row from the left table (customers) and the matching rows from the right (orders). Customers with no order still appear, with NULL in the order columns.
**Explain simply:**
- Left table = the one written before the word JOIN.
- A customer with 2 orders appears twice (once per order).
- NULL order_id is the tell-tale sign of 'no order'.
- Great for 'show all customers and their orders, including those who never bought'.
**Example:** 5 customers: Anil has 2 orders, Bela 1, Chitra 1, Dev and Esha none. Result has 6 rows, Dev and Esha with NULL orders.
**Sample data:**

`customers`

| customer_id | name | city |
|---|---|---|
| 1 | Anil | Hyderabad |
| 2 | Bela | Pune |
| 3 | Chitra | Hyderabad |
| 4 | Dev | Delhi |
| 5 | Esha | Pune |

`orders`

| order_id | customer_id | order_date | amount |
|---|---|---|---|
| 101 | 1 | 2026-01-05 | 5000 |
| 102 | 1 | 2026-02-10 | 7000 |
| 103 | 2 | 2026-01-20 | 3000 |
| 104 | 3 | 2026-03-01 | 6000 |
| 105 | NULL | 2026-03-05 | 2000 |

**SQL:**
```sql
SELECT c.customer_id, c.name, o.order_id, o.amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
ORDER BY c.customer_id, o.order_id;
```
**Output:**

| customer_id | name | order_id | amount |
|---|---|---|---|
| 1 | Anil | 101 | 5000 |
| 1 | Anil | 102 | 7000 |
| 2 | Bela | 103 | 3000 |
| 3 | Chitra | 104 | 6000 |
| 4 | Dev | NULL | NULL |
| 5 | Esha | NULL | NULL |

**pandas equivalent:**
```python
result = cust.merge(orders, on='customer_id', how='left')[['customer_id','name','order_id','amount']].sort_values(['customer_id','order_id'])
```
**Edge cases:** Order 105 has customer_id NULL, so it matches nobody and does not appear (it sits on the right side). Filtering on right-table columns in WHERE can cancel the outer behaviour (Q15, Q48).
**Likely follow-ups:** 1) How to list only customers with no orders? WHERE o.order_id IS NULL (Q12). 2) How to count orders per customer? COUNT(o.order_id), not COUNT(*).
**Common mistakes:** Using COUNT(*), which counts the NULL-padded row as 1.

### Q6 ⭐⭐⭐ 🟢 What is the difference between INNER JOIN and LEFT JOIN?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you contrast 'matches only' with 'keep all left rows'.
**Say this in the interview:** INNER JOIN returns only customers who have orders. LEFT JOIN returns all customers and gives NULLs for those with no orders. A LEFT JOIN returns at least as many rows as the left table has.
**Explain simply:**
- INNER = only keys present in both; LEFT = everything on the left plus matches.
- Choose by the business question: 'orders with customer details' (INNER) vs 'all customers, ordered or not' (LEFT).
- A LEFT JOIN followed by a WHERE on a right-table column quietly becomes an INNER JOIN (Q48).
**Example:** Below: INNER sees 3 customers (4 rows); LEFT sees all 5 customers (6 rows).
**Sample data:**

`customers`

| customer_id | name | city |
|---|---|---|
| 1 | Anil | Hyderabad |
| 2 | Bela | Pune |
| 3 | Chitra | Hyderabad |
| 4 | Dev | Delhi |
| 5 | Esha | Pune |

`orders`

| order_id | customer_id | order_date | amount |
|---|---|---|---|
| 101 | 1 | 2026-01-05 | 5000 |
| 102 | 1 | 2026-02-10 | 7000 |
| 103 | 2 | 2026-01-20 | 3000 |
| 104 | 3 | 2026-03-01 | 6000 |
| 105 | NULL | 2026-03-05 | 2000 |

**SQL:**
```sql
SELECT 'INNER' AS join_type, COUNT(*) AS rows_returned, COUNT(DISTINCT c.customer_id) AS customers_seen
FROM customers c INNER JOIN orders o ON c.customer_id = o.customer_id
UNION ALL
SELECT 'LEFT', COUNT(*), COUNT(DISTINCT c.customer_id)
FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id;
```
**Output:**

| join_type | rows_returned | customers_seen |
|---|---|---|
| INNER | 4 | 3 |
| LEFT | 6 | 5 |

**Edge cases:** Duplicate keys on the right inflate both results. Orders with NULL customer_id appear in neither.
**Likely follow-ups:** 1) Can LEFT return fewer rows than INNER? Never. 2) How to turn LEFT into INNER by accident? Add a WHERE that needs a right-side value.
**Common mistakes:** Using INNER JOIN for 'customer activity' reports and silently losing inactive customers.

### Q7 ⭐⭐⭐ 🟢 What is the difference between LEFT JOIN and RIGHT JOIN? Are they interchangeable?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you see RIGHT JOIN as LEFT JOIN with the tables swapped.
**Say this in the interview:** LEFT JOIN keeps all rows of the left table; RIGHT JOIN keeps all rows of the right table. They are interchangeable: A LEFT JOIN B gives the same rows as B RIGHT JOIN A. Most people use only LEFT JOIN for readability.
**Explain simply:**
- Swap the table order and flip the keyword: same rows.
- Teams prefer LEFT JOIN so queries read 'main table first'.
- Mixing RIGHT joins into a long query makes it hard to see which table is the 'main' one.
**Example:** To list all departments including empty ones (Legal), keep departments on the kept side: either `employees RIGHT JOIN departments` or `departments LEFT JOIN employees`.
**Sample data:**

`employees`

| emp_id | name | dept_id | manager_id | salary |
|---|---|---|---|---|
| 1 | Asha | 10 | NULL | 90000 |
| 2 | Ravi | 20 | 1 | 70000 |
| 3 | Meera | 20 | 2 | 75000 |
| 4 | Kiran | 30 | 1 | 60000 |
| 5 | Sana | NULL | 2 | 50000 |
| 6 | Tom | 10 | 1 | 55000 |

`departments`

| dept_id | dept_name |
|---|---|
| 10 | HR |
| 20 | Analytics |
| 30 | Finance |
| 40 | Legal |

**SQL:**
```sql
SELECT d.dept_name, e.name
FROM employees e
RIGHT JOIN departments d ON e.dept_id = d.dept_id
ORDER BY d.dept_id, e.emp_id;
```
**Output:**

| dept_name | name |
|---|---|
| HR | Asha |
| HR | Tom |
| Analytics | Ravi |
| Analytics | Meera |
| Finance | Kiran |
| Legal | NULL |

**Edge cases:** Verified here: the RIGHT JOIN and the swapped LEFT JOIN return identical rows. MySQL, PostgreSQL, SQL Server support RIGHT JOIN; SQLite only from 3.39. Equivalent LEFT form (also run):
```sql
SELECT d.dept_name, e.name
FROM departments d
LEFT JOIN employees e ON e.dept_id = d.dept_id
ORDER BY d.dept_id, e.emp_id;
```
**Likely follow-ups:** 1) Which do you prefer? LEFT, for consistency. 2) Is the result different? No, at most the column order.
**Common mistakes:** Thinking RIGHT JOIN returns only the unmatched rows.

### Q8 ⭐⭐⭐ 🟢 What is a join key (common column)? How do primary key and foreign key relate to joins?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know what a key is and why joins normally follow PK-FK links.
**Say this in the interview:** The join key is the column (or columns) that appears in both tables and is used to match rows, like dept_id. Usually it is a primary key in one table and a foreign key in the other.
**Explain simply:**
- **Primary key (PK)**: a column whose values are unique and never NULL; it identifies one row (emp_id, dept_id).
- **Foreign key (FK)**: a column in another table that points to a PK (employees.dept_id points to departments.dept_id).
- Joining PK to FK gives a clean one-to-many link: one department, many employees.
- Joining on a column that is not unique on the 'one' side creates duplicate rows.
**Example:** departments.dept_id = 20 is unique (PK). Two employees carry dept_id = 20 (FK). Joining on dept_id attaches the same department row to each.
**SQL:**
```sql
CREATE TABLE dept_demo(dept_id INT PRIMARY KEY, dept_name TEXT);
CREATE TABLE emp_demo(emp_id INT PRIMARY KEY, name TEXT,
                      dept_id INT REFERENCES dept_demo(dept_id));  -- foreign key
SELECT e.name, d.dept_name
FROM emp_demo e JOIN dept_demo d ON e.dept_id = d.dept_id
ORDER BY e.emp_id;
```
**Output:**

| name | dept_name |
|---|---|
| Asha | HR |
| Ravi | Analytics |
| Meera | Analytics |

**Edge cases:** A join works without a declared FK. In SQLite, FK enforcement needs PRAGMA foreign_keys=ON. An FK column may be NULL (an employee with no department).
**Likely follow-ups:** 1) Can a join key be composite? Yes, several columns (Q45). 2) Does a join need a FK constraint? No.
**Common mistakes:** Joining on a column that is not unique on the 'one' side, which multiplies rows.

### Q9 ⭐⭐⭐ 🟢 Write a query to show each employee's name along with their department name from two tables.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you write a basic join with aliases and a sensible column list.
**Say this in the interview:** I join employees to departments on dept_id and select the employee name and department name. I use aliases e and d, and switch to LEFT JOIN if I must keep employees with no department.
**Explain simply:**
- Pick the tables, then the key (dept_id), then the columns.
- Use aliases and prefix columns (e.name) to avoid 'ambiguous column' errors.
- Choose INNER vs LEFT based on whether unassigned employees must appear.
**Example:** 5 of the 6 employees appear: Sana has no department, so INNER JOIN drops her.
**Sample data:**

`employees`

| emp_id | name | dept_id | manager_id | salary |
|---|---|---|---|---|
| 1 | Asha | 10 | NULL | 90000 |
| 2 | Ravi | 20 | 1 | 70000 |
| 3 | Meera | 20 | 2 | 75000 |
| 4 | Kiran | 30 | 1 | 60000 |
| 5 | Sana | NULL | 2 | 50000 |
| 6 | Tom | 10 | 1 | 55000 |

`departments`

| dept_id | dept_name |
|---|---|
| 10 | HR |
| 20 | Analytics |
| 30 | Finance |
| 40 | Legal |

**SQL:**
```sql
SELECT e.name AS employee, d.dept_name AS department
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
ORDER BY e.emp_id;
```
**Output:**

| employee | department |
|---|---|
| Asha | HR |
| Ravi | Analytics |
| Meera | Analytics |
| Kiran | Finance |
| Tom | HR |

**pandas equivalent:**
```python
result = emp.merge(dept, on='dept_id')[['name','dept_name']].rename(columns={'name':'employee','dept_name':'department'})
```
**Edge cases:** Use LEFT JOIN to keep Sana (department shows NULL). To show 'Unassigned' use COALESCE(d.dept_name,'Unassigned'). Oracle does not allow AS before a table alias.
**Likely follow-ups:** 1) How to show Sana too? LEFT JOIN. 2) How to label her? COALESCE.
**Common mistakes:** Writing SELECT * (duplicate dept_id columns) or omitting ON.

### Q10 ⭐⭐⭐ 🟢 What is a SELF JOIN and when would you use it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you recognise hierarchy data and the two-alias trick.
**Say this in the interview:** A self join joins a table to itself, treating it as two copies with different aliases. I use it when a row points to another row of the same table, like an employee pointing to their manager through manager_id.
**Explain simply:**
- There is no special keyword: it is a normal JOIN where both sides are the same table.
- Aliases are mandatory so SQL can tell the two copies apart (e = employee copy, m = manager copy).
- Typical uses: employee-manager, comparing rows within a table (same salary, previous day), finding duplicates.
**Example:** Ravi's manager_id = 1 matches Asha's emp_id = 1, so Ravi's manager is Asha. Asha, the top boss, has a NULL manager and drops out of an INNER JOIN.
**Sample data:**

`employees`

| emp_id | name | dept_id | manager_id | salary |
|---|---|---|---|---|
| 1 | Asha | 10 | NULL | 90000 |
| 2 | Ravi | 20 | 1 | 70000 |
| 3 | Meera | 20 | 2 | 75000 |
| 4 | Kiran | 30 | 1 | 60000 |
| 5 | Sana | NULL | 2 | 50000 |
| 6 | Tom | 10 | 1 | 55000 |

**SQL:**
```sql
SELECT e.name AS employee, m.name AS manager
FROM employees e
JOIN employees m ON e.manager_id = m.emp_id
ORDER BY e.emp_id;
```
**Output:**

| employee | manager |
|---|---|
| Ravi | Asha |
| Meera | Ravi |
| Kiran | Asha |
| Sana | Ravi |
| Tom | Asha |

**pandas equivalent:**
```python
result = emp.merge(emp, left_on='manager_id', right_on='emp_id', suffixes=('','_m'))[['name','name_m']].rename(columns={'name':'employee','name_m':'manager'})
```
**Edge cases:** The top manager (NULL manager_id) is lost under INNER JOIN; use LEFT JOIN to keep them (Q13). NULL never matches.
**Likely follow-ups:** 1) Self join vs recursive CTE? A self join goes one level; a recursive CTE walks all levels. 2) Can you self join more than twice? Yes (Q71).
**Common mistakes:** Forgetting aliases, or joining on e.emp_id = m.emp_id, which just matches each row to itself.

### Q11 ⭐⭐⭐ 🟡 Table A has 10 rows and table B has 5 rows. What are the minimum and maximum rows a LEFT JOIN can return? What about an INNER JOIN?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you reason about row counts without running anything (and spot the duplicate-key explosion).
**Say this in the interview:** A LEFT JOIN returns at least 10 rows (every row of A) and at most 50 (10 x 5, if every key matches every key). An INNER JOIN returns at least 0 (nothing matches) and at most 50.
**Explain simply:**
- LEFT JOIN minimum = rows in the left table (10): unmatched rows still appear once.
- Maximum happens when keys repeat: if all 10 A rows and all 5 B rows share one key, each A row pairs with 5 B rows = 50.
- INNER JOIN minimum is 0 because rows without a match are dropped.
- If B's key is unique, the maximum drops to 10 for LEFT and 10 for INNER (each A row matches at most one B row).
**Example:** 10 employees and 5 department rows that all say dept_id = 1 would give 50 rows: a classic duplicate-key bug.
**SQL:**
```sql
-- a has 10 rows, b has 5 rows
SELECT COUNT(*) FROM a LEFT  JOIN b ON a.id = b.id;
SELECT COUNT(*) FROM a INNER JOIN b ON a.id = b.id;
```
**Output:**

| scenario | left_join_rows | inner_join_rows |
|---|---|---|
| No key matches | 10 | 0 |
| Each B key matches one A row | 10 | 5 |
| Every row has the same key (1) | 50 | 50 |

I built three tiny test cases and ran them; the middle row (unique B keys) shows INNER can also land in between.

**Edge cases:** NULL keys never match, so they count as unmatched. If A is empty, both joins return 0.
**Likely follow-ups:** 1) And FULL JOIN? Minimum 10 (A rows) and with no match at all it is 10 + 5 = 15; maximum is 50 when everything matches. 2) CROSS JOIN? Always exactly 50.
**Common mistakes:** Answering '5' for INNER (assuming one-to-one) or forgetting the join can multiply rows.

### Q12 ⭐⭐⭐ 🟡 Write a query to find all customers who have never placed an order.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you write an anti join (find missing matches).
**Say this in the interview:** I LEFT JOIN customers to orders and keep the rows where the order side is NULL. Those are customers with no matching order.
**Explain simply:**
- **Anti join** = rows from one table that have no match in another.
- After a LEFT JOIN, unmatched rows have NULL in every right-table column; testing a column that can never be NULL in real data (the order id) isolates them.
- Alternatives: NOT EXISTS (safest) or NOT IN (dangerous with NULLs, Q39).
**Example:** HR version: employees who never took leave. Here: customers Dev and Esha never ordered.
**Sample data:**

`customers`

| customer_id | name | city |
|---|---|---|
| 1 | Anil | Hyderabad |
| 2 | Bela | Pune |
| 3 | Chitra | Hyderabad |
| 4 | Dev | Delhi |
| 5 | Esha | Pune |

`orders`

| order_id | customer_id | order_date | amount |
|---|---|---|---|
| 101 | 1 | 2026-01-05 | 5000 |
| 102 | 1 | 2026-02-10 | 7000 |
| 103 | 2 | 2026-01-20 | 3000 |
| 104 | 3 | 2026-03-01 | 6000 |
| 105 | NULL | 2026-03-05 | 2000 |

**SQL:**
```sql
SELECT c.customer_id, c.name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL
ORDER BY c.customer_id;
```
**Output:**

| customer_id | name |
|---|---|
| 4 | Dev |
| 5 | Esha |

**pandas equivalent:**
```python
m = cust.merge(orders[['customer_id','order_id']], on='customer_id', how='left')
result = m[m['order_id'].isna()][['customer_id','name']]
```
**Edge cases:** Check IS NULL on a column that is NOT NULL in the right table (primary key). Order 105 has a NULL customer_id; it does not affect this query but would wreck NOT IN.
**Likely follow-ups:** 1) Same with NOT EXISTS? SELECT ... WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id=c.customer_id). 2) Why not WHERE o.customer_id = NULL? Equals NULL is never true.
**Common mistakes:** Writing = NULL instead of IS NULL, or testing a right-table column that may legitimately be NULL.

### Q13 ⭐⭐⭐ 🟡 Write a query to show each employee together with their manager's name (employee table has manager_id).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you do a self join and keep the top boss using LEFT JOIN.
**Say this in the interview:** I join employees to itself: e is the employee, m is the manager, matching e.manager_id to m.emp_id. I use a LEFT JOIN so the CEO, who has no manager, still appears.
**Explain simply:**
- manager_id stores the emp_id of the boss. It is a **foreign key that points to its own table**.
- Two aliases make one table behave like two.
- LEFT JOIN keeps employees whose manager_id is NULL.
**Example:** Ravi reports to Asha; Meera and Sana report to Ravi; Asha reports to nobody (NULL).
**Sample data:**

`employees`

| emp_id | name | dept_id | manager_id | salary |
|---|---|---|---|---|
| 1 | Asha | 10 | NULL | 90000 |
| 2 | Ravi | 20 | 1 | 70000 |
| 3 | Meera | 20 | 2 | 75000 |
| 4 | Kiran | 30 | 1 | 60000 |
| 5 | Sana | NULL | 2 | 50000 |
| 6 | Tom | 10 | 1 | 55000 |

**SQL:**
```sql
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.emp_id
ORDER BY e.emp_id;
```
**Output:**

| employee | manager |
|---|---|
| Asha | NULL |
| Ravi | Asha |
| Meera | Ravi |
| Kiran | Asha |
| Sana | Ravi |
| Tom | Asha |

**pandas equivalent:**
```python
result = emp.merge(emp, left_on='manager_id', right_on='emp_id', how='left', suffixes=('','_m'))[['name','name_m']]
```
**Edge cases:** Top boss shows a NULL manager. Orphans (manager_id pointing to a missing emp_id) also show NULL; check data quality.
**Likely follow-ups:** 1) Show 'No manager' text? COALESCE(m.name,'No manager'). 2) Manager's manager? Join a third copy (Q71).
**Common mistakes:** Using INNER JOIN, which silently drops the CEO.

### Q14 ⭐⭐⭐ 🟡 Write a query to find total sales per customer, including customers with zero sales.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know to start from the customers table with a LEFT JOIN and handle NULL sums.
**Say this in the interview:** I start from the customers table, LEFT JOIN orders, GROUP BY customer and use COALESCE(SUM(amount), 0) so customers with no orders show 0 instead of NULL.
**Explain simply:**
- **GROUP BY** collapses rows into one per customer; **SUM** adds the amounts.
- SUM of nothing is NULL, not 0. **COALESCE(x, 0)** swaps a NULL for 0.
- Customers must be on the LEFT (the 'keep all' side).
**Example:** Anil 5000 + 7000 = 12000; Bela 3000; Chitra 6000; Dev and Esha 0.
**Sample data:**

`customers`

| customer_id | name | city |
|---|---|---|
| 1 | Anil | Hyderabad |
| 2 | Bela | Pune |
| 3 | Chitra | Hyderabad |
| 4 | Dev | Delhi |
| 5 | Esha | Pune |

`orders`

| order_id | customer_id | order_date | amount |
|---|---|---|---|
| 101 | 1 | 2026-01-05 | 5000 |
| 102 | 1 | 2026-02-10 | 7000 |
| 103 | 2 | 2026-01-20 | 3000 |
| 104 | 3 | 2026-03-01 | 6000 |
| 105 | NULL | 2026-03-05 | 2000 |

**SQL:**
```sql
SELECT c.customer_id, c.name, COALESCE(SUM(o.amount), 0) AS total_sales
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY c.customer_id;
```
**Output:**

| customer_id | name | total_sales |
|---|---|---|
| 1 | Anil | 12000 |
| 2 | Bela | 3000 |
| 3 | Chitra | 6000 |
| 4 | Dev | 0 |
| 5 | Esha | 0 |

**pandas equivalent:**
```python
s = orders.groupby('customer_id', as_index=False)['amount'].sum().rename(columns={'amount':'total_sales'})
result = cust.merge(s, on='customer_id', how='left').fillna({'total_sales': 0}).astype({'total_sales': int})[['customer_id','name','total_sales']]
```
**Edge cases:** Order 105 (NULL customer) is not counted for anyone. If amount can be NULL, SUM ignores it. Duplicate customer rows would double-count.
**Likely follow-ups:** 1) Why not INNER JOIN? Dev and Esha would vanish. 2) Customers with the same name? Group by customer_id, not name.
**Common mistakes:** Starting from orders (no zero customers), or leaving NULL instead of 0.

### Q15 ⭐⭐⭐ 🟡 In a LEFT JOIN, what is the difference between putting a filter in the WHERE clause and in the ON clause?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand that ON filters before the join and WHERE filters after it.
**Say this in the interview:** In a LEFT JOIN, a filter in ON only decides which right-side rows may match, so left rows are kept. A filter in WHERE runs after the join and removes the NULL-padded rows too, which turns the LEFT JOIN into an INNER JOIN.
**Explain simply:**
- **ON** = rules for matching. **WHERE** = rules for what survives in the final result.
- Filtering the right table's columns in WHERE throws away unmatched left rows (their value is NULL, and NULL >= date is not true).
- To keep all customers but only count recent orders, put the date condition in ON.
- Filters on the left table's columns can go in WHERE safely.
**Example:** Question: 'all customers with their orders since 1 Feb'. Version B keeps everyone (Anil shows only the Feb order); version A drops Bela, Dev and Esha.
**Sample data:**

`customers`

| customer_id | name | city |
|---|---|---|
| 1 | Anil | Hyderabad |
| 2 | Bela | Pune |
| 3 | Chitra | Hyderabad |
| 4 | Dev | Delhi |
| 5 | Esha | Pune |

`orders`

| order_id | customer_id | order_date | amount |
|---|---|---|---|
| 101 | 1 | 2026-01-05 | 5000 |
| 102 | 1 | 2026-02-10 | 7000 |
| 103 | 2 | 2026-01-20 | 3000 |
| 104 | 3 | 2026-03-01 | 6000 |
| 105 | NULL | 2026-03-05 | 2000 |

**SQL:**
```sql
-- A: filter in WHERE
SELECT c.name, o.order_id, o.order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2026-02-01'
ORDER BY c.customer_id, o.order_id;

-- B: filter in ON
SELECT c.name, o.order_id, o.order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
                  AND o.order_date >= '2026-02-01'
ORDER BY c.customer_id, o.order_id;
```
**Output:**

Output of A (WHERE):

| name | order_id | order_date |
|---|---|---|
| Anil | 102 | 2026-02-10 |
| Chitra | 104 | 2026-03-01 |

Output of B (ON):

| name | order_id | order_date |
|---|---|---|
| Anil | 102 | 2026-02-10 |
| Bela | NULL | NULL |
| Chitra | 104 | 2026-03-01 |
| Dev | NULL | NULL |
| Esha | NULL | NULL |

**pandas equivalent:**
```python
# A: filter after the join
m = cust.merge(orders, on='customer_id', how='left')
result = m[m['order_date'] >= '2026-02-01'][['name','order_id','order_date']]

# B: filter before the join
o2 = orders[orders['order_date'] >= '2026-02-01']
result = cust.merge(o2, on='customer_id', how='left')[['name','order_id','order_date']]
```
**Edge cases:** For INNER JOIN the two placements give the same result, so the difference only matters for outer joins. NULL dates are removed by the WHERE version.
**Likely follow-ups:** 1) Which is right for 'customers with no recent orders'? ON filter plus WHERE o.order_id IS NULL. 2) Can WHERE keep the NULL rows? Add OR o.order_id IS NULL, but ON is cleaner.
**Common mistakes:** Putting the right-table filter in WHERE and wondering why customers disappeared.

### Q16 ⭐⭐⭐ 🟡 Why does the number of rows increase after a join? (one-to-many relationship and duplicate rows)
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand one-to-many and fan-out.
**Say this in the interview:** Rows increase when the key is not unique on the other side. If one order has 2 items, joining orders to items repeats that order's row twice, once per item. This is called fan-out.
**Explain simply:**
- **One-to-many**: one order, many order items (or one department, many employees).
- Each left row is repeated for every matching right row.
- Row counts rise and any SUM of a left-table column gets double-counted.
- Fix: aggregate the many side first, join on a unique key, or count DISTINCT ids.
**Example:** Order 104 (6000) has two items (Headset and Webcam), so its 6000 is added twice. Joined sum is 29000 but real total is 23000.
**Sample data:**

`orders`

| order_id | customer_id | order_date | amount |
|---|---|---|---|
| 101 | 1 | 2026-01-05 | 5000 |
| 102 | 1 | 2026-02-10 | 7000 |
| 103 | 2 | 2026-01-20 | 3000 |
| 104 | 3 | 2026-03-01 | 6000 |
| 105 | NULL | 2026-03-05 | 2000 |

`order_items`

| order_id | product_id | qty |
|---|---|---|
| 101 | 1 | 5 |
| 102 | 2 | 2 |
| 103 | 3 | 6 |
| 104 | 2 | 1 |
| 104 | 4 | 1 |
| 105 | 3 | 4 |

**SQL:**
```sql
SELECT COUNT(*) AS joined_rows,
       (SELECT COUNT(*) FROM orders) AS orders_rows,
       SUM(o.amount) AS joined_sum,
       (SELECT SUM(amount) FROM orders) AS true_sum
FROM orders o
JOIN order_items i ON i.order_id = o.order_id;
```
**Output:**

| joined_rows | orders_rows | joined_sum | true_sum |
|---|---|---|---|
| 6 | 5 | 29000 | 23000 |

**pandas equivalent:**
```python
j = orders.merge(items, on='order_id')
result = pd.DataFrame({'joined_rows':[len(j)], 'orders_rows':[len(orders)], 'joined_sum':[j['amount'].sum()], 'true_sum':[orders['amount'].sum()]})
```
**Edge cases:** Orders with no items vanish in an INNER JOIN (use LEFT JOIN to keep them). Exact duplicate rows in either table multiply rows further.
**Likely follow-ups:** 1) How to detect? Compare COUNT(*) before and after, check key uniqueness with GROUP BY HAVING COUNT(*)>1. 2) Fix? Pre-aggregate (Q49).
**Common mistakes:** Summing a header-level amount (order amount) after joining to line items.

### Q17 ⭐⭐⭐ 🟡 How do you join three or more tables? Write an example (customers, orders, products).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you chain joins and keep the keys straight.
**Say this in the interview:** Join them one after another: customers to orders, then orders to order_items, then order_items to products. Each JOIN has its own ON condition linking the new table to one already in the query.
**Explain simply:**
- Think of a chain: customer -> order -> item -> product.
- Each new JOIN adds one table and one ON; the result of the previous join is the 'left' side.
- Use meaningful aliases (c, o, i, p) and prefix all columns.
- Check for fan-out: order 104 has 2 items, so it appears twice.
**Example:** Chitra's order 104 became two lines: Headset 3500 + Webcam 2500 = 6000, matching the order total.
**Sample data:**

`customers`

| customer_id | name | city |
|---|---|---|
| 1 | Anil | Hyderabad |
| 2 | Bela | Pune |
| 3 | Chitra | Hyderabad |
| 4 | Dev | Delhi |
| 5 | Esha | Pune |

`orders`

| order_id | customer_id | order_date | amount |
|---|---|---|---|
| 101 | 1 | 2026-01-05 | 5000 |
| 102 | 1 | 2026-02-10 | 7000 |
| 103 | 2 | 2026-01-20 | 3000 |
| 104 | 3 | 2026-03-01 | 6000 |
| 105 | NULL | 2026-03-05 | 2000 |

`order_items`

| order_id | product_id | qty |
|---|---|---|
| 101 | 1 | 5 |
| 102 | 2 | 2 |
| 103 | 3 | 6 |
| 104 | 2 | 1 |
| 104 | 4 | 1 |
| 105 | 3 | 4 |

`products`

| product_id | product_name | price |
|---|---|---|
| 1 | Keyboard | 1000 |
| 2 | Headset | 3500 |
| 3 | Mouse | 500 |
| 4 | Webcam | 2500 |

**SQL:**
```sql
SELECT c.name AS customer, o.order_id, p.product_name, i.qty, i.qty * p.price AS line_total
FROM customers c
JOIN orders o       ON o.customer_id = c.customer_id
JOIN order_items i  ON i.order_id    = o.order_id
JOIN products p     ON p.product_id  = i.product_id
ORDER BY o.order_id, p.product_id;
```
**Output:**

| customer | order_id | product_name | qty | line_total |
|---|---|---|---|---|
| Anil | 101 | Keyboard | 5 | 5000 |
| Anil | 102 | Headset | 2 | 7000 |
| Bela | 103 | Mouse | 6 | 3000 |
| Chitra | 104 | Headset | 1 | 3500 |
| Chitra | 104 | Webcam | 1 | 2500 |

**pandas equivalent:**
```python
result = (cust.merge(orders, on='customer_id', suffixes=('_c',''))
            .merge(items, on='order_id')
            .merge(prod, on='product_id')
            .assign(line_total=lambda d: d['qty'] * d['price'])
            .sort_values(['order_id','product_id'])
            [['name','order_id','product_name','qty','line_total']])
```
**Edge cases:** Order 105 has no customer (NULL), so INNER JOIN drops it; use LEFT JOIN from orders to keep it. Mixing INNER and LEFT in a chain needs care (Q75).
**Likely follow-ups:** 1) Is there a limit on joins? Practical, not syntactic; performance drops as it grows. 2) Does the order of joins matter? For INNER no; for OUTER yes (Q75).
**Common mistakes:** Missing one ON condition (creating a Cartesian product), or joining to the wrong key.

### Q18 ⭐⭐⭐ 🟡 What does a FULL OUTER JOIN return? When is it useful?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know FULL OUTER JOIN keeps both sides and when that helps.
**Say this in the interview:** FULL OUTER JOIN returns all rows from both tables: matched pairs together, plus unmatched left rows and unmatched right rows, each padded with NULL on the missing side. I use it for reconciliation, to see what is missing on either side.
**Explain simply:**
- Think LEFT JOIN plus RIGHT JOIN combined, with matched rows shown once.
- Useful for comparing two lists: HR roster vs payroll list, source vs warehouse (Q73).
- NULL on the left columns means 'only in the right table', and vice versa.
**Example:** Employees vs departments: Sana has no department, Legal has no employees. Both show up.
**Sample data:**

`employees`

| emp_id | name | dept_id | manager_id | salary |
|---|---|---|---|---|
| 1 | Asha | 10 | NULL | 90000 |
| 2 | Ravi | 20 | 1 | 70000 |
| 3 | Meera | 20 | 2 | 75000 |
| 4 | Kiran | 30 | 1 | 60000 |
| 5 | Sana | NULL | 2 | 50000 |
| 6 | Tom | 10 | 1 | 55000 |

`departments`

| dept_id | dept_name |
|---|---|
| 10 | HR |
| 20 | Analytics |
| 30 | Finance |
| 40 | Legal |

**SQL:**
```sql
SELECT e.name AS employee, d.dept_name AS department
FROM employees e
FULL OUTER JOIN departments d ON e.dept_id = d.dept_id
ORDER BY d.dept_id, e.emp_id;
```
**Output:**

| employee | department |
|---|---|
| Sana | NULL |
| Asha | HR |
| Tom | HR |
| Ravi | Analytics |
| Meera | Analytics |
| Kiran | Finance |
| NULL | Legal |

**pandas equivalent:**
```python
m = emp.merge(dept, on='dept_id', how='outer').sort_values(['dept_id','emp_id'], na_position='first')
result = m[['name','dept_name']]
```
**Edge cases:** MySQL does not support FULL OUTER JOIN: emulate with LEFT JOIN UNION RIGHT JOIN (Q41). NULL keys do not match each other, so they stay separate rows. Result rows = matched + left-only + right-only.
**Likely follow-ups:** 1) How to find only the mismatches? WHERE e.emp_id IS NULL OR d.dept_id IS NULL. 2) Is it common in practice? Less than LEFT JOIN but valuable for audits.
**Common mistakes:** Expecting it to work in MySQL, or assuming it returns the Cartesian product.

### Q19 ⭐⭐⭐ 🟡 How do NULL values in the join column behave in a join? Do NULL = NULL rows match?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know NULL means 'unknown' and NULL = NULL is not true.
**Say this in the interview:** No. In SQL, NULL = NULL is not true (the result is unknown), so rows with NULL in the join column never match each other, in any join type. They only survive in outer joins as unmatched rows.
**Explain simply:**
- **NULL** = missing/unknown value. Comparing unknown to unknown gives unknown, which a join treats as 'no match'.
- To match NULLs on purpose, use a null-safe comparison: IS NOT DISTINCT FROM (PostgreSQL, SQL Server 2022), <=> (MySQL), IS (SQLite), or COALESCE the key to a sentinel value.
- Warning: pandas merge DOES match NaN with NaN, unlike SQL.
**Example:** Employee Sana has dept_id NULL: she never matches any department, not even a NULL department row. She appears only in a LEFT/FULL join, with NULL department.
**Sample data:**

`a`

| id | a_val |
|---|---|
| 1 | a1 |
| NULL | a_null |
| 3 | a3 |

`b`

| id | b_val |
|---|---|
| 1 | b1 |
| NULL | b_null |
| 4 | b4 |

**SQL:**
```sql
SELECT a.a_val, b.b_val FROM a JOIN b ON a.id = b.id ORDER BY a.a_val;
SELECT a.a_val, b.b_val FROM a JOIN b ON a.id IS b.id ORDER BY a.a_val;  -- SQLite null-safe equality
SELECT NULL = NULL AS null_equals_null, NULL IS NULL AS null_is_null;
```
**Output:**

Standard join (ON a.id = b.id):

| a_val | b_val |
|---|---|
| a1 | b1 |

NULL-safe join (IS):

| a_val | b_val |
|---|---|
| a1 | b1 |
| a_null | b_null |

Why:

| null_equals_null | null_is_null |
|---|---|
| NULL | 1 |

pandas (matches NaN keys, differs from SQL):

| a_val | b_val |
|---|---|
| a1 | b1 |
| a_null | b_null |

**pandas equivalent:**
```python
a = pd.DataFrame({'id':[1,None,3],'a_val':['a1','a_null','a3']})
b = pd.DataFrame({'id':[1,None,4],'b_val':['b1','b_null','b4']})
result = a.merge(b, on='id')[['a_val','b_val']]  # NOTE: pandas DOES match NaN with NaN
```
**Edge cases:** SQL Server: add ON (a.id = b.id OR (a.id IS NULL AND b.id IS NULL)) on versions before 2022. Not run here: PostgreSQL `ON a.id IS NOT DISTINCT FROM b.id`, MySQL `ON a.id <=> b.id`.
**Likely follow-ups:** 1) What does WHERE id = NULL return? Nothing. Use IS NULL. 2) How do you find NULL keys? WHERE col IS NULL.
**Common mistakes:** Assuming NULLs match each other, or using = NULL.

### Q20 ⭐⭐⭐ 🟡 Write a query to find employees who earn more than their manager.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you compare a row against another row of the same table.
**Say this in the interview:** Self join employees to employees to attach each person's manager, then keep rows where the employee's salary is greater than the manager's salary.
**Explain simply:**
- Two aliases: e for the employee, m for the manager.
- ON e.manager_id = m.emp_id links the employee to the boss row.
- WHERE e.salary > m.salary compares the two salaries on the same row.
**Example:** Meera earns 75000 and her manager Ravi earns 70000, so she is the only one who earns more than her manager.
**Sample data:**

`employees`

| emp_id | name | dept_id | manager_id | salary |
|---|---|---|---|---|
| 1 | Asha | 10 | NULL | 90000 |
| 2 | Ravi | 20 | 1 | 70000 |
| 3 | Meera | 20 | 2 | 75000 |
| 4 | Kiran | 30 | 1 | 60000 |
| 5 | Sana | NULL | 2 | 50000 |
| 6 | Tom | 10 | 1 | 55000 |

**SQL:**
```sql
SELECT e.name AS employee, e.salary AS emp_salary, m.name AS manager, m.salary AS mgr_salary
FROM employees e
JOIN employees m ON e.manager_id = m.emp_id
WHERE e.salary > m.salary
ORDER BY e.emp_id;
```
**Output:**

| employee | emp_salary | manager | mgr_salary |
|---|---|---|---|
| Meera | 75000 | Ravi | 70000 |

**pandas equivalent:**
```python
j = emp.merge(emp, left_on='manager_id', right_on='emp_id', suffixes=('','_m'))
result = j[j['salary'] > j['salary_m']][['name','salary','name_m','salary_m']]
```
**Edge cases:** Employees without a manager (Asha) are excluded by the INNER JOIN, which is right here. Ties (equal salary) are not 'more than'. NULL salary makes the comparison unknown, so the row is dropped.
**Likely follow-ups:** 1) Employees earning more than the department average? That needs an aggregate (subquery/CTE). 2) Earn at least as much? Use >=.
**Common mistakes:** Comparing e.salary with e.salary, or using a LEFT JOIN, where the NULL manager salary row gets filtered out anyway.

### Q21 ⭐⭐⭐ 🟡 Write a query to count orders per customer using JOIN plus GROUP BY.
**Asked at:** commonly asked (no company-specific report found) (join + GROUP BY is a staple of the SQL round at service MNCs, GCCs and analytics firms)
**What the interviewer is checking:** Can you combine two tables and then summarise, and do you know LEFT JOIN keeps customers with zero orders?
**Say this in the interview:** "I join customers to orders on customer_id, group by customer, and count order_id. I use a LEFT JOIN so customers with no orders still show up with a zero."
**Explain simply:**
- **JOIN** = put two tables side by side by matching a shared column (here customer_id).
- **GROUP BY** = squash the matched rows into one row per customer so we can count them.
- **COUNT(o.order_id)** counts only real orders. **COUNT(*)** counts rows, and a customer with no orders still has one (empty) joined row, so it wrongly shows 1.
- INNER JOIN would silently drop customers with no orders; LEFT JOIN keeps them.
**Example:** HR version: count training sessions per employee. Meena attended none, and she must still appear with 0, otherwise your report hides the people who most need nudging.
**Sample data:**

*customers*

| customer_id | name |
|---|---|
| 1 | Asha |
| 2 | Ravi |
| 3 | Meena |
| 4 | Kiran |

*orders*

| order_id | customer_id | amount |
|---|---|---|
| 101 | 1 | 500 |
| 102 | 1 | 300 |
| 103 | 2 | 700 |
| 104 | 1 | 200 |
| 105 | 2 | 150 |

**SQL:**
```sql
-- correct
SELECT c.customer_id, c.name, COUNT(o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY c.customer_id;

-- wrong_count_star
SELECT c.name, COUNT(*) AS order_count
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY c.customer_id;
```
**Output:**

*correct*

| customer_id | name | order_count |
|---|---|---|
| 1 | Asha | 3 |
| 2 | Ravi | 2 |
| 3 | Meena | 0 |
| 4 | Kiran | 0 |

*wrong_count_star*

| name | order_count |
|---|---|
| Asha | 3 |
| Ravi | 2 |
| Meena | 1 |
| Kiran | 1 |

**pandas equivalent:**
```python
# DataFrames named as in the sample data above
m = customers.merge(orders, on="customer_id", how="left")
result = (m.groupby(["customer_id", "name"], as_index=False)
            .agg(order_count=("order_id", "count"))   # count() skips NaN, like COUNT(col)
            .sort_values("customer_id"))
results = {"correct": result}
```
**Edge cases:** Customers with no orders -> 0 (only with LEFT JOIN + COUNT of the right-side column). NULL customer_id in orders never matches. Duplicate customer rows would double the counts.
**Likely follow-ups:**
- How to list only customers with 3+ orders? Add `HAVING COUNT(o.order_id) >= 3` (HAVING filters after grouping; WHERE filters before).
- Why group by name too? Strict engines (PostgreSQL, SQL Server) need every selected non-aggregate column in GROUP BY; MySQL/SQLite are lenient.
**Common mistakes:** Using COUNT(*) after a LEFT JOIN (zero-order customers show 1); using INNER JOIN and losing zero-order customers; grouping only by name when two customers share a name.

### Q22 ⭐⭐⭐ 🟡 Table A has 3 rows with id=1 and table B has 2 rows with id=1. How many rows does an INNER JOIN return for id=1?
**Asked at:** a related row-count question (min/max rows of a LEFT JOIN on 10-row and 5-row tables) was candidate-reported at Deloitte (consulting/GCC), Bengaluru, Mar 2025; this exact duplicate-key version is commonly asked
**What the interviewer is checking:** Do you understand that a join multiplies matching rows (many-to-many), not just matches them one to one?
**Say this in the interview:** "3 times 2, so 6 rows. Every id=1 row in A pairs with every id=1 row in B."
**Explain simply:**
- An INNER JOIN returns one output row for **every matching pair**. With 3 matching rows on one side and 2 on the other, pairs = 3 x 2 = 6.
- This blow-up is called a **fan-out** or many-to-many join. It silently inflates counts and sums.
- Rows with no partner (id=2 in A, id=3 in B) are dropped by INNER JOIN.
**Example:** Employee 7 has 3 rows in an attendance table and 2 rows in a bonus table. Joining both on emp_id gives 6 rows for her, and SUM(bonus) is now counted 3 times.
**Sample data:**

*a*

| id | val |
|---|---|
| 1 | a1 |
| 1 | a2 |
| 1 | a3 |
| 2 | a4 |

*b*

| id | val |
|---|---|
| 1 | b1 |
| 1 | b2 |
| 3 | b3 |

**SQL:**
```sql
SELECT a.id, a.val AS a_val, b.val AS b_val
FROM a
INNER JOIN b ON a.id = b.id
ORDER BY a.val, b.val;
```
**Output:**

| id | a_val | b_val |
|---|---|---|
| 1 | a1 | b1 |
| 1 | a1 | b2 |
| 1 | a2 | b1 |
| 1 | a2 | b2 |
| 1 | a3 | b1 |
| 1 | a3 | b2 |

**pandas equivalent:**
```python
# DataFrames named as in the sample data above
result = (a.merge(b, on="id", suffixes=("_a", "_b"))
          .rename(columns={"val_a": "a_val", "val_b": "b_val"})
          .sort_values(["a_val", "b_val"]))
print(len(result))   # 6
```
**Edge cases:** NULL ids never match, so they add no pairs. Row count for LEFT JOIN here would be 6 + 1 (a4 unmatched) = 7. General rule: matched pairs = sum over each key of (count in A x count in B).
**Likely follow-ups:**
- How do you prevent the blow-up? De-duplicate or aggregate one side first (e.g. SUM bonus per emp_id in a subquery) and then join.
- A=10 rows, B=5 rows, LEFT JOIN: min and max rows? Min 10 (every A row kept); max 50 (every row matches every B row).
**Common mistakes:** Answering 2 or 3 (thinking of one-to-one matching); forgetting unmatched rows are dropped; summing a column after a many-to-many join.

### Q23 ⭐⭐⭐ 🟡 Given two small tables with sample data, write out the output of INNER, LEFT, RIGHT and FULL joins by hand.
**Asked at:** Indium Software (analytics firm), Bengaluru, Nov 2025: candidate reported being asked to write the manual output of joins on given tables (single candidate report)
**What the interviewer is checking:** Can you work out join results on paper, including where NULLs appear?
**Say this in the interview:** "INNER keeps only ids in both. LEFT keeps all of A, RIGHT keeps all of B, FULL keeps everything, and missing sides show NULL."
**Explain simply:**
- **INNER**: only rows whose id exists in both tables.
- **LEFT**: every row of A, plus B's data where it matches, else NULL.
- **RIGHT**: mirror image, every row of B.
- **FULL OUTER**: every row from both; NULL wherever a side is missing.
- Quick check: A and B each have 3 rows, only ids 2 and 3 overlap, so INNER=2, LEFT=3, RIGHT=3, FULL=2+1+1=4.
**Example:** A = employees in the HR system (ids 1-3), B = employees in payroll (ids 2-4). FULL join reveals employee 1 missing from payroll and employee 4 missing from HR.
**Sample data:**

*a*

| id | a_val |
|---|---|
| 1 | A1 |
| 2 | A2 |
| 3 | A3 |

*b*

| id | b_val |
|---|---|
| 2 | B2 |
| 3 | B3 |
| 4 | B4 |

**SQL:**
```sql
-- inner
SELECT a.id, a.a_val, b.b_val FROM a INNER JOIN b ON a.id = b.id ORDER BY 1;

-- left
SELECT a.id, a.a_val, b.b_val FROM a LEFT JOIN b ON a.id = b.id ORDER BY 1;

-- right
-- RIGHT/FULL need SQLite 3.39+, PostgreSQL, SQL Server; MySQL has RIGHT but no FULL
SELECT b.id, a.a_val, b.b_val FROM a RIGHT JOIN b ON a.id = b.id ORDER BY 1;

-- full
SELECT COALESCE(a.id, b.id) AS id, a.a_val, b.b_val
FROM a FULL OUTER JOIN b ON a.id = b.id ORDER BY 1;
```
**Output:**

*inner*

| id | a_val | b_val |
|---|---|---|
| 2 | A2 | B2 |
| 3 | A3 | B3 |

*left*

| id | a_val | b_val |
|---|---|---|
| 1 | A1 | NULL |
| 2 | A2 | B2 |
| 3 | A3 | B3 |

*right*

| id | a_val | b_val |
|---|---|---|
| 2 | A2 | B2 |
| 3 | A3 | B3 |
| 4 | NULL | B4 |

*full*

| id | a_val | b_val |
|---|---|---|
| 1 | A1 | NULL |
| 2 | A2 | B2 |
| 3 | A3 | B3 |
| 4 | NULL | B4 |

**pandas equivalent:**
```python
# DataFrames named as in the sample data above
results = {}
for label, how in [("inner", "inner"), ("left", "left"), ("right", "right"), ("full", "outer")]:
    results[label] = a.merge(b, on="id", how=how).sort_values("id")[["id", "a_val", "b_val"]]
```
**Edge cases:** In the RIGHT result id comes from B (A's id would be NULL for id 4), so select b.id or COALESCE. NULL join keys never match, so they appear only in LEFT/RIGHT/FULL outputs as unmatched rows.
**Likely follow-ups:**
- Which is the same as swapping tables? A RIGHT JOIN B equals B LEFT JOIN A.
- What if A had two rows with id=2? Both would pair with B2, giving an extra row in every join type.
**Common mistakes:** Forgetting the NULL padding; thinking FULL = LEFT + RIGHT (that double counts the matched rows); losing the id of B-only rows by selecting a.id.

### Q24 ⭐⭐⭐ 🟡 What is the difference between JOIN and UNION?
**Asked at:** inner vs outer joins and set operations came up in a Deloitte (consulting) Gurgaon report, 2025 (single candidate report); JOIN vs UNION itself is commonly asked
**What the interviewer is checking:** Do you know JOIN adds columns side by side and UNION stacks rows on top of each other?
**Say this in the interview:** "JOIN widens a table by matching rows on a key. UNION lengthens it by stacking two result sets with the same columns, and removes duplicates; UNION ALL keeps them."
**Explain simply:**
- **JOIN** combines **columns** from two tables, row matched by a condition.
- **UNION** combines **rows** from two queries. Both queries need the same number of columns with compatible types.
- **UNION** removes duplicate rows (slower, it must sort/compare). **UNION ALL** keeps everything (faster).
**Example:** Bengaluru and Hyderabad each keep a list of trainees. UNION gives one combined list of people; a JOIN of employees to departments adds a department column to each employee.
**Sample data:**

*blr_staff*

| name |
|---|
| Asha |
| Ravi |
| Meena |

*hyd_staff*

| name |
|---|
| Ravi |
| Kiran |
| Sonal |

*employees*

| emp_id | name | dept_id |
|---|---|---|
| 1 | Asha | 1 |
| 2 | Ravi | 2 |
| 3 | Meena | 1 |

*departments*

| dept_id | dept_name |
|---|---|
| 1 | Sales |
| 2 | HR |
| 3 | IT |

**SQL:**
```sql
-- union
SELECT name FROM blr_staff UNION SELECT name FROM hyd_staff ORDER BY name;

-- union_all
SELECT name FROM blr_staff UNION ALL SELECT name FROM hyd_staff ORDER BY name;

-- join
SELECT e.name, d.dept_name FROM employees e
JOIN departments d ON d.dept_id = e.dept_id ORDER BY e.emp_id;
```
**Output:**

*union*

| name |
|---|
| Asha |
| Kiran |
| Meena |
| Ravi |
| Sonal |

*union_all*

| name |
|---|
| Asha |
| Kiran |
| Meena |
| Ravi |
| Ravi |
| Sonal |

*join*

| name | dept_name |
|---|---|
| Asha | Sales |
| Ravi | HR |
| Meena | Sales |

**pandas equivalent:**
```python
# DataFrames named as in the sample data above
results = {
 "union": pd.concat([blr_staff, hyd_staff]).drop_duplicates().sort_values("name"),
 "union_all": pd.concat([blr_staff, hyd_staff]).sort_values("name"),
 "join": employees.merge(departments, on="dept_id")[["name", "dept_name"]],
}
```
**Edge cases:** UNION treats NULLs as equal when removing duplicates (JOIN does not match NULLs). Column names come from the first query. Column order and types must line up.
**Likely follow-ups:**
- When use UNION ALL? When duplicates are impossible or wanted, e.g. stacking monthly tables; it is faster.
- Can you combine them? Yes: UNION ALL monthly tables, then JOIN the result to a dimension table.
**Common mistakes:** Using UNION when UNION ALL was meant (quietly deletes legitimate duplicate rows); mismatched column order in the two SELECTs; calling UNION a kind of join.

### Q25 ⭐⭐⭐ 🔴 How do you find the second/third highest salary or top earner per department using a join (without window functions)?
**Asked at:** commonly asked (no company-specific report found) (Nth-highest salary is a classic; the no-window-function version is common in older-style and screening rounds)
**What the interviewer is checking:** Can you solve ranking problems with self-joins, aggregates and subqueries, and handle ties?
**Say this in the interview:** "For the top earner I join employees to each department's MAX salary. For the Nth highest I self-join and count how many distinct salaries are higher; N-1 means it is the Nth."
**Explain simply:**
- **Self join** = joining a table to itself under two aliases (e1, e2) so each row can be compared with the others.
- Top earner per department: compute MAX(salary) per department in a subquery, then join back to find who earns it. Ties return all tied people.
- Nth highest: for each employee count the DISTINCT salaries above theirs; the 2nd highest has exactly 1 above. LEFT JOIN is used so N=1 (zero above) also works.
- Overall second highest: the max of everything below the max.
**Example:** Payroll wants the second-highest salary in each department to set a pay band. Sales has two people on 90,000, so the 'second highest salary' is 70,000, not 90,000 (distinct values).
**Sample data:**

*employees*

| emp_id | name | dept | salary |
|---|---|---|---|
| 1 | Asha | Sales | 90 |
| 2 | Ravi | Sales | 90 |
| 3 | Meena | Sales | 70 |
| 4 | Kiran | Sales | 60 |
| 5 | Sonal | HR | 50 |
| 6 | Dev | HR | 45 |
| 7 | Nina | HR | 40 |
| 8 | Omar | IT | 120 |
| 9 | Priya | IT | 100 |
| 10 | Zoya | IT | 100 |
| 11 | Leo | IT | 80 |

**SQL:**
```sql
-- top_per_dept
SELECT e.dept, e.name, e.salary
FROM employees e
JOIN (SELECT dept, MAX(salary) AS max_sal FROM employees GROUP BY dept) m
  ON e.dept = m.dept AND e.salary = m.max_sal
ORDER BY e.dept, e.name;

-- second_per_dept
SELECT e1.dept, e1.name, e1.salary
FROM employees e1
LEFT JOIN employees e2 ON e2.dept = e1.dept AND e2.salary > e1.salary
GROUP BY e1.emp_id, e1.dept, e1.name, e1.salary
HAVING COUNT(DISTINCT e2.salary) = 1          -- use = 2 for third highest
ORDER BY e1.dept, e1.name;

-- second_overall
SELECT MAX(salary) AS second_highest
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
```
**Output:**

*top_per_dept*

| dept | name | salary |
|---|---|---|
| HR | Sonal | 50 |
| IT | Omar | 120 |
| Sales | Asha | 90 |
| Sales | Ravi | 90 |

*second_per_dept*

| dept | name | salary |
|---|---|---|
| HR | Dev | 45 |
| IT | Priya | 100 |
| IT | Zoya | 100 |
| Sales | Meena | 70 |

*second_overall*

| second_highest |
|---|
| 100 |

**pandas equivalent:**
```python
# DataFrames named as in the sample data above
top = employees[employees.salary == employees.groupby("dept").salary.transform("max")]
rank = employees.groupby("dept").salary.rank(method="dense", ascending=False)
results = {
 "top_per_dept": top[["dept", "name", "salary"]].sort_values(["dept", "name"]),
 "second_per_dept": employees[rank == 2][["dept", "name", "salary"]].sort_values(["dept", "name"]),
 "second_overall": pd.DataFrame({"second_highest": [sorted(employees.salary.unique())[-2]]}),
}
```
**Edge cases:** Ties: top_per_dept returns both 90k earners; Priya and Zoya tie as IT's second highest (distinct salaries). A department with fewer than N distinct salaries returns no row. Salaries in thousands here to keep the table short. NULL salary: comparisons with NULL are false, so such rows never count as 'higher'.
**Likely follow-ups:**
- Why DISTINCT in the count? Without it, tied salaries are counted twice and rank skips (that is ROW-style ranking, not DENSE).
- Window-function answer? DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) = 2; cleaner and faster, so mention it after the join answer.
**Common mistakes:** Using MAX(salary) - 1 or LIMIT 1 OFFSET 1 per department (OFFSET gives the second row, not the second salary, and ignores departments); forgetting ties; using INNER JOIN in the self-join so the top earner can never be selected.

### Q26 ⭐⭐ 🟢 What is a CROSS JOIN (Cartesian product)? How many rows does it return?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know CROSS JOIN pairs every row with every row, and that rows = m x n?
**Say this in the interview:** "A CROSS JOIN pairs every row of one table with every row of the other, so 3 rows and 2 rows give 6. It has no ON condition. I use it deliberately to build combinations."
**Explain simply:**
- **Cartesian product** = all possible pairs, like matching every shirt with every trouser.
- Rows returned = rows in A x rows in B. Two 1,000-row tables give 1,000,000 rows, so be careful.
- Legit uses: shift rosters, date x employee grids, scenario tables.
**Example:** 3 employees x 2 shifts (Morning, Night) = 6 possible roster slots to then fill in.
**Sample data:**

*employees*

| name |
|---|
| Asha |
| Ravi |
| Meena |

*shifts*

| shift |
|---|
| Morning |
| Night |

**SQL:**
```sql
-- roster
SELECT e.name, s.shift
FROM employees e CROSS JOIN shifts s
ORDER BY e.name, s.shift;

-- row_count
SELECT COUNT(*) AS rows_returned FROM employees CROSS JOIN shifts;
```
**Output:**

*roster*

| name | shift |
|---|---|
| Asha | Morning |
| Asha | Night |
| Meena | Morning |
| Meena | Night |
| Ravi | Morning |
| Ravi | Night |

*row_count*

| rows_returned |
|---|
| 6 |

**pandas equivalent:**
```python
# DataFrames named as in the sample data above
roster = employees.merge(shifts, how="cross").sort_values(["name", "shift"])
results = {"roster": roster, "row_count": pd.DataFrame({"rows_returned": [len(roster)]})}
```
**Edge cases:** If either table is empty the result is empty (n x 0 = 0). NULLs are irrelevant since no matching happens. Old syntax `FROM a, b` does the same thing.
**Likely follow-ups:**
- Is it ever useful? Yes: build a calendar x employee grid, then LEFT JOIN actual attendance to see who is absent on which day.
- How is it different from INNER JOIN? INNER JOIN filters the pairs by a condition; CROSS keeps all pairs.
**Common mistakes:** Accidentally getting one by forgetting the ON condition; not warning about row explosion; assuming it needs a common column.

### Q27 ⭐⭐ 🟢 What are table aliases and why do we use them in joins?
**Asked at:** commonly asked (no company-specific report found) (self-joins, where aliases are mandatory, are reported at Flipkart, product company, Bengaluru, 2024-25)
**What the interviewer is checking:** Do you know aliases give tables short names, avoid ambiguity, and are required for self joins?
**Say this in the interview:** "An alias is a temporary nickname like `e` for employees. It makes the query shorter, avoids column-name clashes, and is essential when joining a table to itself."
**Explain simply:**
- Write `FROM employees e` (or `AS e`); then refer to `e.name`.
- Needed when the same column name is in both tables (dept_id) so the database knows which one you mean.
- Mandatory in a **self join**, where the same table appears twice. Alias is also used on columns: `m.name AS manager`.
- An alias lives only for that query.
**Example:** To show each employee with their manager's name, both come from the same employees table: `e` plays the employee, `m` plays the manager.
**Sample data:**

*employees*

| emp_id | name | manager_id |
|---|---|---|
| 1 | Meera | NULL |
| 2 | Ravi | 1 |
| 3 | Asha | 1 |
| 4 | Kiran | 2 |

**SQL:**
```sql
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.emp_id
ORDER BY e.emp_id;
```
**Output:**

| employee | manager |
|---|---|
| Meera | NULL |
| Ravi | Meera |
| Asha | Meera |
| Kiran | Ravi |

**pandas equivalent:**
```python
# DataFrames named as in the sample data above
result = (employees.merge(employees, how="left", left_on="manager_id", right_on="emp_id", suffixes=("", "_m"))
          .rename(columns={"name": "employee", "name_m": "manager"})
          .sort_values("emp_id")[["employee", "manager"]])
```
**Edge cases:** Meera has no manager (NULL), so LEFT JOIN keeps her with manager NULL; INNER JOIN would drop her. In WHERE/GROUP BY you can use table aliases; column aliases defined in SELECT can be used in ORDER BY but (in most engines) not in WHERE.
**Likely follow-ups:**
- Is AS required? Optional for table aliases in most databases; Oracle does not allow AS before a table alias.
- Can you use a column alias in WHERE? Not in standard SQL, because WHERE runs before SELECT.
**Common mistakes:** Reusing the same alias for both copies in a self join; forgetting to qualify columns and getting 'ambiguous column' errors; giving cryptic aliases (a, b, c) in long queries.

### Q28 ⭐⭐ 🟢 What is an equi join versus a non-equi join?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know joins are not only `=`; ranges and inequalities also work (non-equi), which is how bands are assigned.
**Say this in the interview:** "An equi join matches on equality, like emp.dept_id = dept.dept_id. A non-equi join uses another operator, such as BETWEEN, <, >, to match rows to ranges, for example salary to a pay band."
**Explain simply:**
- **Equi join**: the ON condition uses `=`. Most joins you write.
- **Non-equi join**: uses `<`, `>`, `<=`, `BETWEEN`, `<>`. One row can match several rows.
- Typical uses: salary bands, tenure buckets, effective-date lookups, comparing employees to each other.
**Example:** A salary of 72,000 falls in band B (50,000-79,999). The bands table has no employee id, so you can only join on the range.
**Sample data:**

*employees*

| name | dept_id | salary |
|---|---|---|
| Asha | 1 | 90000 |
| Ravi | 1 | 55000 |
| Meena | 2 | 40000 |
| Kiran | 2 | 72000 |

*departments*

| dept_id | dept_name |
|---|---|
| 1 | Sales |
| 2 | HR |

*bands*

| band | low | high |
|---|---|---|
| A | 0 | 49999 |
| B | 50000 | 79999 |
| C | 80000 | 999999 |

**SQL:**
```sql
-- equi
SELECT e.name, d.dept_name FROM employees e
JOIN departments d ON d.dept_id = e.dept_id ORDER BY e.name;

-- non_equi
SELECT e.name, e.salary, b.band FROM employees e
JOIN bands b ON e.salary BETWEEN b.low AND b.high ORDER BY e.name;
```
**Output:**

*equi*

| name | dept_name |
|---|---|
| Asha | Sales |
| Kiran | HR |
| Meena | HR |
| Ravi | Sales |

*non_equi*

| name | salary | band |
|---|---|---|
| Asha | 90000 | C |
| Kiran | 72000 | B |
| Meena | 40000 | A |
| Ravi | 55000 | B |

**pandas equivalent:**
```python
# DataFrames named as in the sample data above
results = {"equi": employees.merge(departments, on="dept_id")[["name", "dept_name"]].sort_values("name")}
x = employees.merge(bands, how="cross")           # pandas has no direct non-equi merge
x = x[(x.salary >= x.low) & (x.salary <= x.high)]
results["non_equi"] = x[["name", "salary", "band"]].sort_values("name")
```
**Edge cases:** Overlapping bands make one employee match two bands (duplicate rows); gaps (e.g. 49999.5) match none and the row disappears under INNER JOIN. NULL salary matches nothing. Non-equi joins can be slow as indexes help less.
**Likely follow-ups:**
- Give another non-equi use. Self join with `e1.salary > e2.salary` to find who earns more than whom.
- How does pandas do it? Cross merge then filter, or `pd.merge_asof` for nearest/range matching.
**Common mistakes:** Thinking every join must use `=`; leaving gaps/overlaps in band tables; using BETWEEN with decimals and boundary errors.

### Q29 ⭐⭐ 🟢 What happens if you join two tables without an ON condition (or forget the join condition)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know a missing join condition produces a Cartesian product and wrong, inflated numbers?
**Say this in the interview:** "Every row pairs with every row, so 4 employees and 3 departments return 12 rows instead of 4. Totals and counts become wrong, and on big tables it can hang the database."
**Explain simply:**
- Without a condition the database has nothing to match on, so it returns **all combinations** (Cartesian product).
- Dialects differ: PostgreSQL and SQL Server raise an error for `INNER JOIN` without `ON`; MySQL and SQLite accept it and treat it as a cross join. Comma-style joins with a forgotten WHERE also silently do this.
- Warning sign: row count suspiciously equals rows A x rows B.
**Example:** Joining 4 employees to 3 departments without ON, Asha appears next to Sales, HR and IT; her 'department' is now meaningless.
**Sample data:**

*employees*

| name | dept_id |
|---|---|
| Asha | 1 |
| Ravi | 2 |
| Meena | 1 |
| Kiran | 3 |

*departments*

| dept_id | dept_name |
|---|---|
| 1 | Sales |
| 2 | HR |
| 3 | IT |

**SQL:**
```sql
-- forgot_on_count
SELECT COUNT(*) AS rows_returned FROM employees e JOIN departments d;   -- SQLite/MySQL accept this; PostgreSQL/SQL Server error

-- correct_count
SELECT COUNT(*) AS rows_returned FROM employees e JOIN departments d ON d.dept_id = e.dept_id;

-- forgot_on_preview
SELECT e.name, d.dept_name FROM employees e JOIN departments d ORDER BY e.name, d.dept_name LIMIT 4;
```
**Output:**

*forgot_on_count*

| rows_returned |
|---|
| 12 |

*correct_count*

| rows_returned |
|---|
| 4 |

*forgot_on_preview*

| name | dept_name |
|---|---|
| Asha | HR |
| Asha | IT |
| Asha | Sales |
| Kiran | HR |

**pandas equivalent:**
```python
# DataFrames named as in the sample data above
wrong = employees.merge(departments, how="cross")
right = employees.merge(departments, on="dept_id")
results = {"forgot_on_count": pd.DataFrame({"rows_returned": [len(wrong)]}),
           "correct_count": pd.DataFrame({"rows_returned": [len(right)]}),
           "forgot_on_preview": wrong.sort_values(["name", "dept_name"])[["name", "dept_name"]].head(4)}
```
**Edge cases:** If one table is empty the product is empty. In pandas, `merge` with no common column raises an error unless you ask for `how='cross'`.
**Likely follow-ups:**
- How do you catch it? Compare row counts before and after the join; expect output <= larger table for a one-to-one/many-to-one join.
- LIMIT here is SQLite/MySQL/PostgreSQL; SQL Server uses TOP 4, Oracle FETCH FIRST 4 ROWS ONLY (not run here).
**Common mistakes:** Writing `FROM a, b` and forgetting WHERE; putting the condition in the wrong place in multi-table joins; not sanity-checking row counts.

### Q30 ⭐⭐ 🟢 What is a NATURAL JOIN and why is it considered risky?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know NATURAL JOIN joins on ALL same-named columns automatically, which breaks silently when schemas change?
**Say this in the interview:** "NATURAL JOIN automatically joins on every column with the same name in both tables. It is risky because an unrelated shared column, or a column added later, silently changes the result. I write explicit ON instead."
**Explain simply:**
- You do not write a condition; the database finds columns with identical names and matches them all.
- Here both tables have `dept_id` (good) and also `name` (employee name vs department name): it demands both match, so no rows come back.
- Risks: new columns (e.g. `created_at`) change results without any code change; unreadable intent. Not supported in SQL Server.
**Example:** Employee 'Asha' (Sales) and department named 'Sales': names differ, so a NATURAL JOIN returns nothing, even though dept_id matches.
**Sample data:**

*employees*

| emp_id | name | dept_id |
|---|---|---|
| 1 | Asha | 1 |
| 2 | Ravi | 2 |
| 3 | Meena | 1 |

*departments*

| dept_id | name |
|---|---|
| 1 | Sales |
| 2 | HR |

**SQL:**
```sql
-- natural
SELECT * FROM employees NATURAL JOIN departments;

-- explicit_on
SELECT e.emp_id, e.name AS employee, d.name AS department
FROM employees e JOIN departments d ON d.dept_id = e.dept_id ORDER BY e.emp_id;
```
**Output:**

*natural*

| emp_id | name | dept_id |
|---|---|---|
| *(no rows)* | | |

*explicit_on*

| emp_id | employee | department |
|---|---|---|
| 1 | Asha | Sales |
| 2 | Ravi | HR |
| 3 | Meena | Sales |

**pandas equivalent:**
```python
# DataFrames named as in the sample data above
results = {
 "natural": pd.merge(employees, departments),   # no 'on' -> pandas also joins on ALL common columns
 "explicit_on": (employees.merge(departments, on="dept_id", suffixes=("_e", "_d"))
                 .rename(columns={"name_e": "employee", "name_d": "department"})
                 [["emp_id", "employee", "department"]].sort_values("emp_id")),
}
```
**Edge cases:** Zero common columns -> NATURAL JOIN degrades to a cross join. NULLs in the shared columns never match. Supported in PostgreSQL, MySQL, Oracle, SQLite; not SQL Server.
**Likely follow-ups:**
- Safer alternatives? Explicit ON, or USING(col) to name the join column(s) yourself.
- Does pandas do the same? Yes, merge without `on` uses all shared column names.
**Common mistakes:** Using it for 'convenience' in production; not noticing a new shared column was added; expecting it to behave like USING with one column.

### Q31 ⭐⭐ 🟢 What is the difference between ON and USING in a join?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know USING is shorthand for same-named join columns and merges them into one output column?
**Say this in the interview:** "ON works with any condition and keeps both columns. USING(dept_id) only works when both tables have the same column name, and it returns that column once."
**Explain simply:**
- `ON a.dept_id = b.dept_id` is fully flexible: different names, extra conditions, non-equi.
- `USING (dept_id)` is shorter but only for equality on a same-named column.
- With `SELECT *`, USING gives one `dept_id` column; ON gives two.
- SQL Server has no USING. In PostgreSQL after USING, write plain `dept_id` (qualifying it is not allowed in some versions).
**Example:** Employee and department tables both have dept_id; USING gives a cleaner report with a single dept_id column.
**Sample data:**

*employees*

| emp_id | name | dept_id |
|---|---|---|
| 1 | Asha | 1 |
| 2 | Ravi | 2 |
| 3 | Meena | 1 |

*departments*

| dept_id | dept_name |
|---|---|
| 1 | Sales |
| 2 | HR |
| 3 | IT |

**SQL:**
```sql
-- on
SELECT * FROM employees e JOIN departments d ON d.dept_id = e.dept_id ORDER BY e.emp_id;

-- using
SELECT * FROM employees JOIN departments USING (dept_id) ORDER BY emp_id;
```
**Output:**

*on*

| emp_id | name | dept_id | dept_id | dept_name |
|---|---|---|---|---|
| 1 | Asha | 1 | 1 | Sales |
| 2 | Ravi | 2 | 2 | HR |
| 3 | Meena | 1 | 1 | Sales |

*using*

| emp_id | name | dept_id | dept_name |
|---|---|---|---|
| 1 | Asha | 1 | Sales |
| 2 | Ravi | 2 | HR |
| 3 | Meena | 1 | Sales |

**pandas equivalent:**
```python
# DataFrames named as in the sample data above
results = {"using": employees.merge(departments, on="dept_id")[["emp_id", "name", "dept_id", "dept_name"]].sort_values("emp_id")}
# ON with different column names -> left_on="dept_id", right_on="dept_code" (keeps both columns)
```
**Edge cases:** Column order of SELECT * can differ by dialect (PostgreSQL puts the USING column first; SQLite, run here, keeps table order). For LEFT/FULL joins USING shows a coalesced value; ON shows NULL on the missing side. Multi-column: USING (a, b).
**Likely follow-ups:**
- When must you use ON? Different column names, extra filter conditions, or non-equality joins.
- Does pandas have an equivalent? `on=` for same name, `left_on`/`right_on` for different names.
**Common mistakes:** Using USING when names differ; qualifying the USING column in dialects that forbid it; forgetting SQL Server lacks it.

### Q32 ⭐⭐ 🟢 What is the difference between JOIN and the old comma-style join (FROM a, b WHERE ...)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know both give the same inner-join result, but explicit JOIN is clearer, safer and the only way to do outer joins portably?
**Say this in the interview:** "The comma style lists tables and puts the join condition in WHERE. The modern JOIN ... ON separates the join logic from filters, makes forgetting the condition obvious, and supports LEFT/RIGHT/FULL joins. I always use JOIN."
**Explain simply:**
- `FROM a, b WHERE a.id = b.id` is an old (ANSI-89) inner join.
- `FROM a JOIN b ON a.id = b.id` (ANSI-92) does the same but keeps join conditions apart from filters.
- Forget the WHERE in comma style and you get a silent cross join; forgetting ON is more visible.
- Outer joins need the JOIN keyword (old vendor tricks like `(+)` are non-standard).
**Example:** Kiran has no department. Comma/inner style drops him; LEFT JOIN keeps him, which is what attrition-by-department reports often need.
**Sample data:**

*employees*

| emp_id | name | dept_id |
|---|---|---|
| 1 | Asha | 1 |
| 2 | Ravi | 2 |
| 3 | Meena | 1 |
| 4 | Kiran | NULL |

*departments*

| dept_id | dept_name |
|---|---|
| 1 | Sales |
| 2 | HR |
| 3 | IT |

**SQL:**
```sql
-- join
SELECT e.name, d.dept_name FROM employees e
JOIN departments d ON d.dept_id = e.dept_id ORDER BY e.name;

-- comma
SELECT e.name, d.dept_name FROM employees e, departments d
WHERE d.dept_id = e.dept_id ORDER BY e.name;

-- left_join
SELECT e.name, d.dept_name FROM employees e
LEFT JOIN departments d ON d.dept_id = e.dept_id ORDER BY e.name;
```
**Output:**

*join*

| name | dept_name |
|---|---|
| Asha | Sales |
| Meena | Sales |
| Ravi | HR |

*comma*

| name | dept_name |
|---|---|
| Asha | Sales |
| Meena | Sales |
| Ravi | HR |

*left_join*

| name | dept_name |
|---|---|
| Asha | Sales |
| Kiran | NULL |
| Meena | Sales |
| Ravi | HR |

**pandas equivalent:**
```python
# DataFrames named as in the sample data above
inner = employees.merge(departments, on="dept_id")[["name", "dept_name"]].sort_values("name")
results = {"join": inner, "comma": inner,
           "left_join": employees.merge(departments, on="dept_id", how="left")[["name", "dept_name"]].sort_values("name")}
```
**Edge cases:** Optimisers treat inner JOIN and comma+WHERE the same, so no speed difference. With outer joins, WHERE vs ON placement changes results: a WHERE on the right table's column can turn a LEFT JOIN back into an inner join.
**Likely follow-ups:**
- Any performance difference? Normally none; readability and safety differ.
- Where do filters go in LEFT JOIN? Conditions on the right table belong in ON to keep unmatched rows.
**Common mistakes:** Forgetting the WHERE in comma style; mixing comma and JOIN in one query (precedence surprises); filtering the right table in WHERE after a LEFT JOIN.

### Q33 ⭐⭐ 🟢 What does the error 'ambiguous column name' mean in a join and how do you fix it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you read an error message and fix it with table aliases/qualification?
**Say this in the interview:** "It means the column name exists in more than one joined table, so the database cannot choose. I fix it by prefixing the column with the table alias, like e.dept_id."
**Explain simply:**
- Both employees and departments contain `dept_id`; `SELECT dept_id` is ambiguous (unclear).
- Fix: qualify with table name or alias (`e.dept_id`).
- Message differs by dialect: SQLite 'ambiguous column name: dept_id'; PostgreSQL 'column reference "dept_id" is ambiguous'; SQL Server 'Ambiguous column name'; MySQL 'Column in field list is ambiguous' (PostgreSQL/SQL Server/MySQL texts not run here).
- Columns that exist in only one table (like `name`) need no prefix, but prefixing everything is good practice.
**Example:** Employee and department tables both carry dept_id. The report asks for dept_id; you must say whose.
**Sample data:**

*employees*

| emp_id | name | dept_id |
|---|---|---|
| 1 | Asha | 1 |
| 2 | Ravi | 2 |
| 3 | Meena | 1 |

*departments*

| dept_id | dept_name |
|---|---|
| 1 | Sales |
| 2 | HR |

**SQL:**
```sql
-- ambiguous
SELECT name, dept_id, dept_name
FROM employees e JOIN departments d ON e.dept_id = d.dept_id;

-- fixed
SELECT e.name, e.dept_id, d.dept_name
FROM employees e JOIN departments d ON e.dept_id = d.dept_id ORDER BY e.emp_id;
```
**Output:**

*ambiguous*

Error: `ambiguous column name: dept_id`

*fixed*

| name | dept_id | dept_name |
|---|---|---|
| Asha | 1 | Sales |
| Ravi | 2 | HR |
| Meena | 1 | Sales |

**pandas equivalent:**
```python
# DataFrames named as in the sample data above
# pandas merge on a shared key keeps ONE column; clashing non-key columns get _x/_y (or your suffixes)
result = employees.merge(departments, on="dept_id")[["name", "dept_id", "dept_name"]]
results = {"fixed": result}
```
**Edge cases:** Also happens in ORDER BY / GROUP BY and with SELECT * when exporting (two columns named dept_id). With USING (dept_id) the shared column is no longer ambiguous in most dialects.
**Likely follow-ups:**
- How do you keep SELECT * readable? Avoid it; list columns with aliases, e.g. `d.dept_id AS dept_id_dim`.
- Does a subquery alias matter too? Yes: derived tables need an alias in many dialects.
**Common mistakes:** Fixing the error by removing the column rather than qualifying it; qualifying with a table name after you aliased it (use the alias); relying on column order instead of names.

### Q34 ⭐⭐ 🟢 Is JOIN the same as INNER JOIN? What is the default join type?
**Asked at:** inner vs outer join was asked at Deloitte (consulting), Gurgaon, 2025 (single candidate report); this exact wording is commonly asked
**What the interviewer is checking:** Do you know bare JOIN means INNER JOIN, and the OUTER keyword is optional?
**Say this in the interview:** "Yes. JOIN on its own is an INNER JOIN, the default. Likewise LEFT JOIN is the same as LEFT OUTER JOIN."
**Explain simply:**
- **INNER JOIN** keeps only rows that match in both tables; the word INNER is optional.
- `LEFT JOIN` = `LEFT OUTER JOIN`, `RIGHT JOIN` = `RIGHT OUTER JOIN`, `FULL JOIN` = `FULL OUTER JOIN`.
- Comma-separated tables with WHERE is also an inner join; `CROSS JOIN` is the exception that needs no condition.
**Example:** Joining employees to departments: Kiran (no department) is dropped by JOIN/INNER JOIN but kept by LEFT JOIN.
**Sample data:**

*employees*

| emp_id | name | dept_id |
|---|---|---|
| 1 | Asha | 1 |
| 2 | Ravi | 2 |
| 3 | Meena | 1 |
| 4 | Kiran | NULL |

*departments*

| dept_id | dept_name |
|---|---|
| 1 | Sales |
| 2 | HR |
| 3 | IT |

**SQL:**
```sql
-- join
SELECT e.name, d.dept_name FROM employees e JOIN departments d ON d.dept_id = e.dept_id ORDER BY e.name;

-- inner_join
SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON d.dept_id = e.dept_id ORDER BY e.name;
```
**Output:**

*join*

| name | dept_name |
|---|---|
| Asha | Sales |
| Meena | Sales |
| Ravi | HR |

*inner_join*

| name | dept_name |
|---|---|
| Asha | Sales |
| Meena | Sales |
| Ravi | HR |

**pandas equivalent:**
```python
# DataFrames named as in the sample data above
r = employees.merge(departments, on="dept_id")[["name", "dept_name"]].sort_values("name")   # how="inner" is pandas' default too
results = {"join": r, "inner_join": r}
```
**Edge cases:** Kiran (NULL dept) and the unused IT department disappear in both. Explicit INNER makes the intent obvious to readers, which is why many teams write it.
**Likely follow-ups:**
- Which dialects differ? All major databases treat bare JOIN as INNER; MySQL also allows JOIN without ON (acts like cross).
- Default in pandas merge? how='inner'.
**Common mistakes:** Thinking JOIN means LEFT or FULL; being surprised that unmatched rows vanish; assuming OUTER is required.

### Q35 ⭐⭐ 🟢 What is the difference between a join and a subquery? When would you use each?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you pick the right tool: join when you need columns from another table, subquery for filtering or a computed value?
**Say this in the interview:** "I use a join when I need columns from both tables in the output. I use a subquery when I only need to filter by another table or compare to a computed value, such as the average salary."
**Explain simply:**
- **Subquery** = a query inside another query, in brackets.
- Join: returns columns from both; one-to-many matches repeat rows.
- `IN (subquery)`: only filters; returns left-table columns and never repeats rows.
- Subquery returning a single value (average) is neat and often needed with a comparison. Modern optimisers often run joins and IN/EXISTS the same way, so readability and correctness decide.
**Example:** 'Employees in Pune departments with the department name' needs a join. 'Employees earning above the company average' needs a subquery.
**Sample data:**

*employees*

| emp_id | name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 1 | 90000 |
| 2 | Ravi | 2 | 55000 |
| 3 | Meena | 1 | 70000 |
| 4 | Kiran | 3 | 60000 |
| 5 | Sonal | 2 | 48000 |

*departments*

| dept_id | dept_name | city |
|---|---|---|
| 1 | Sales | Pune |
| 2 | HR | Hyderabad |
| 3 | IT | Pune |

**SQL:**
```sql
-- join
SELECT e.name, d.dept_name FROM employees e
JOIN departments d ON d.dept_id = e.dept_id
WHERE d.city = 'Pune' ORDER BY e.name;

-- in_subquery
SELECT name FROM employees
WHERE dept_id IN (SELECT dept_id FROM departments WHERE city = 'Pune') ORDER BY name;

-- above_avg
SELECT name, salary FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees) ORDER BY name;
```
**Output:**

*join*

| name | dept_name |
|---|---|
| Asha | Sales |
| Kiran | IT |
| Meena | Sales |

*in_subquery*

| name |
|---|
| Asha |
| Kiran |
| Meena |

*above_avg*

| name | salary |
|---|---|
| Asha | 90000 |
| Meena | 70000 |

**pandas equivalent:**
```python
# DataFrames named as in the sample data above
pune = departments[departments.city == "Pune"]
results = {
 "join": employees.merge(pune, on="dept_id")[["name", "dept_name"]].sort_values("name"),
 "in_subquery": employees[employees.dept_id.isin(pune.dept_id)][["name"]].sort_values("name"),
 "above_avg": employees[employees.salary > employees.salary.mean()][["name", "salary"]].sort_values("name"),
}
```
**Edge cases:** Join duplicates the left row if the right side has several matches; IN does not. NOT IN with NULLs in the subquery returns nothing (see Q39). Scalar subquery must return one row or it errors.
**Likely follow-ups:**
- Which is faster? Usually the same after optimisation; test with EXPLAIN. Correlated subqueries can be slow on large data.
- What is a CTE? A named subquery (WITH ...) for readability.
**Common mistakes:** Using a join and getting duplicate rows when only a filter was needed; using `=` instead of IN when the subquery returns many rows; trying to select right-table columns from an IN subquery.

### Q36 ⭐⭐ 🟢 How is a SQL join different from VLOOKUP in Excel?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand joins are set-based and return ALL matches, while VLOOKUP returns only the first match and #N/A for misses?
**Say this in the interview:** "VLOOKUP fetches one value for each row and stops at the first match. A SQL join works on whole tables, returns every match, supports all join types, and handles millions of rows."
**Explain simply:**
- **VLOOKUP**: looks up one value to the right of a key; first match only; `#N/A` when missing; exact vs approximate setting (TRUE by default can give wrong answers).
- **LEFT JOIN** = the closest to VLOOKUP, but keeps *all* matches (duplicates produce extra rows) and shows NULL for no match.
- SQL can join on many columns, any direction, and different join types; XLOOKUP (Excel 365/2021) fixes some VLOOKUP limits but still returns one match.
- Excel has a row limit (about 1 million rows); databases do not.
**Example:** Ravi moved from HR to IT, so he has two rows in the department history. VLOOKUP returns only HR; the join returns both rows so you can spot the move. Meena has no history: VLOOKUP shows #N/A, the join shows NULL.
**Sample data:**

*employees*

| emp_id | name |
|---|---|
| 1 | Asha |
| 2 | Ravi |
| 3 | Meena |

*dept_history*

| emp_id | dept | from_year |
|---|---|---|
| 1 | Sales | 2022 |
| 2 | HR | 2021 |
| 2 | IT | 2024 |

**SQL:**
```sql
SELECT e.emp_id, e.name, h.dept, h.from_year
FROM employees e
LEFT JOIN dept_history h ON h.emp_id = e.emp_id
ORDER BY e.emp_id, h.from_year;
```
**Output:**

| emp_id | name | dept | from_year |
|---|---|---|---|
| 1 | Asha | Sales | 2022 |
| 2 | Ravi | HR | 2021 |
| 2 | Ravi | IT | 2024 |
| 3 | Meena | NULL | NULL |

**pandas equivalent:**
```python
# DataFrames named as in the sample data above
result = (employees.merge(dept_history, on="emp_id", how="left")
          .sort_values(["emp_id", "from_year"])[["emp_id", "name", "dept", "from_year"]])
```
**Edge cases:** To mimic VLOOKUP's first match in SQL, pick one row per key (e.g. earliest from_year using MIN/ROW_NUMBER) before joining. Duplicate keys in the lookup table are the main cause of unexpected extra rows.
**Likely follow-ups:**
- Excel equivalent of LEFT JOIN? XLOOKUP/VLOOKUP with IFNA, or Power Query merge (left outer).
- Why do analysts move from VLOOKUP to SQL? Scale, repeatability and many-to-many handling.
**Common mistakes:** Expecting a join to return one row per employee; leaving approximate-match on in VLOOKUP; ignoring duplicates in the lookup table.

### Q37 ⭐⭐ 🟢 How do you do the equivalent of a join in pandas (merge)? Map inner/left/right/outer to the how= options.
**Asked at:** commonly asked (no company-specific report found) (pandas merge is a standard follow-up where SQL and Python are both tested)
**What the interviewer is checking:** Can you translate SQL join types to pandas `merge(how=...)` and know `on`, `left_on`, `right_on`, `suffixes`, `indicator`?
**Say this in the interview:** "pandas.merge is the join: how='inner', 'left', 'right' or 'outer' map to INNER, LEFT, RIGHT and FULL OUTER JOIN. I use on= for same-named keys and left_on/right_on for different names."
**Explain simply:**
- `how='inner'` (default) = INNER JOIN; `'left'` = LEFT JOIN; `'right'` = RIGHT JOIN; `'outer'` = FULL OUTER JOIN; `'cross'` = CROSS JOIN.
- `indicator=True` adds a `_merge` column (left_only / right_only / both), handy for anti joins.
- `suffixes=('_x','_y')` renames clashing non-key columns; `validate='one_to_many'` guards against duplicate keys.
- Gotcha: pandas matches NaN keys to NaN keys; SQL never matches NULL = NULL.
**Example:** Employees (Kiran has an invalid dept 9) joined to departments (IT has no staff): left shows Kiran with NaN department; outer also shows the empty IT department.
**Sample data:**

*employees*

| emp_id | name | dept_id |
|---|---|---|
| 1 | Asha | 1 |
| 2 | Ravi | 2 |
| 3 | Meena | 1 |
| 4 | Kiran | 9 |

*departments*

| dept_id | dept_name |
|---|---|
| 1 | Sales |
| 2 | HR |
| 3 | IT |

**SQL:**
```sql
-- inner
SELECT COALESCE(e.dept_id, d.dept_id) AS dept_id, e.name, d.dept_name
FROM employees e INNER JOIN departments d ON d.dept_id = e.dept_id ORDER BY 1, 2;

-- left
SELECT COALESCE(e.dept_id, d.dept_id) AS dept_id, e.name, d.dept_name
FROM employees e LEFT JOIN departments d ON d.dept_id = e.dept_id ORDER BY 1, 2;

-- right
SELECT COALESCE(e.dept_id, d.dept_id) AS dept_id, e.name, d.dept_name
FROM employees e RIGHT JOIN departments d ON d.dept_id = e.dept_id ORDER BY 1, 2;

-- full
SELECT COALESCE(e.dept_id, d.dept_id) AS dept_id, e.name, d.dept_name
FROM employees e FULL OUTER JOIN departments d ON d.dept_id = e.dept_id ORDER BY 1, 2;
```
**Output:**

*inner*

| dept_id | name | dept_name |
|---|---|---|
| 1 | Asha | Sales |
| 1 | Meena | Sales |
| 2 | Ravi | HR |

*left*

| dept_id | name | dept_name |
|---|---|---|
| 1 | Asha | Sales |
| 1 | Meena | Sales |
| 2 | Ravi | HR |
| 9 | Kiran | NULL |

*right*

| dept_id | name | dept_name |
|---|---|---|
| 1 | Asha | Sales |
| 1 | Meena | Sales |
| 2 | Ravi | HR |
| 3 | NULL | IT |

*full*

| dept_id | name | dept_name |
|---|---|---|
| 1 | Asha | Sales |
| 1 | Meena | Sales |
| 2 | Ravi | HR |
| 3 | NULL | IT |
| 9 | Kiran | NULL |

**pandas equivalent:**
```python
# DataFrames named as in the sample data above
results = {}
for label, how in [("inner", "inner"), ("left", "left"), ("right", "right"), ("full", "outer")]:
    m = employees.merge(departments, on="dept_id", how=how)
    results[label] = m[["dept_id", "name", "dept_name"]].sort_values(["dept_id", "name"])
```
**Edge cases:** Duplicate keys multiply rows exactly as in SQL. Different key names: `left_on='dept_id', right_on='id'` keeps both columns. Ints become floats when NaN appears. `df.join()` joins on the index.
**Likely follow-ups:**
- Anti join in pandas? `merge(..., how='left', indicator=True)` then keep `_merge == 'left_only'`.
- Non-equi join? Cross merge then filter, or merge_asof for nearest keys.
**Common mistakes:** Forgetting `on` and getting an unintended merge on all shared columns; not noticing NaN keys match; expecting row order to be preserved after a join.

### Q38 ⭐⭐ 🟡 Write a query to find records in table A that have no match in table B (anti join) using LEFT JOIN ... IS NULL.
**Asked at:** commonly asked (no company-specific report found) (anti joins such as customers/employees with no activity are a frequent SQL-screen pattern)
**What the interviewer is checking:** Do you know to LEFT JOIN and keep rows where the right side's key is NULL?
**Say this in the interview:** "I LEFT JOIN A to B, then filter WHERE b.key IS NULL. Those are the A rows that found no partner in B."
**Explain simply:**
- **Anti join** = rows in A that have NO match in B.
- LEFT JOIN keeps every A row; unmatched ones get NULLs on B's columns. Filtering on that NULL keeps just the unmatched.
- Test a column that can never be NULL in a real match (B's key or primary key), otherwise genuine NULL data is confused with 'no match'.
**Example:** HR wants employees who never applied for leave this year: Ravi, Kiran and Sonal.
**Sample data:**

*employees*

| emp_id | name |
|---|---|
| 1 | Asha |
| 2 | Ravi |
| 3 | Meena |
| 4 | Kiran |
| 5 | Sonal |

*leave_requests*

| leave_id | emp_id | days |
|---|---|---|
| 1 | 1 | 2 |
| 2 | 1 | 1 |
| 3 | 3 | 5 |

**SQL:**
```sql
SELECT e.emp_id, e.name
FROM employees e
LEFT JOIN leave_requests l ON l.emp_id = e.emp_id
WHERE l.leave_id IS NULL
ORDER BY e.emp_id;
```
**Output:**

| emp_id | name |
|---|---|
| 2 | Ravi |
| 4 | Kiran |
| 5 | Sonal |

**pandas equivalent:**
```python
# DataFrames named as in the sample data above
m = employees.merge(leave_requests, on="emp_id", how="left", indicator=True)
result = m[m["_merge"] == "left_only"][["emp_id", "name"]].sort_values("emp_id")
```
**Edge cases:** Asha has two leave rows but is excluded anyway, so duplicates do not matter here. Do not put the IS NULL test on a column that can be legitimately NULL. A NULL emp_id on the employees side is unmatched, so it is returned.
**Likely follow-ups:**
- Other ways? NOT EXISTS or NOT IN (see Q39).
- Which rows would an INNER JOIN return? The opposite: only employees with leave.
**Common mistakes:** Checking `l.emp_id IS NULL` is fine, but checking a nullable data column is not; putting the right-table condition in WHERE when it belongs in ON; using INNER JOIN.

### Q39 ⭐⭐ 🟡 Compare three ways to find non-matching rows: LEFT JOIN IS NULL, NOT IN, NOT EXISTS. Which is safest with NULLs?
**Asked at:** commonly asked (no company-specific report found) (the NOT IN with NULL trap is a classic trick question)
**What the interviewer is checking:** Do you know NOT IN returns nothing when the subquery contains a NULL, while NOT EXISTS and LEFT JOIN are NULL-safe?
**Say this in the interview:** "All three find rows with no match, but NOT IN breaks if the subquery returns even one NULL, because `x NOT IN (1, NULL)` is never true. NOT EXISTS and LEFT JOIN IS NULL are safe, and NOT EXISTS is my default."
**Explain simply:**
- SQL uses three-valued logic: a comparison with NULL is *unknown*, not true.
- `x NOT IN (1, 3, NULL)` becomes `x<>1 AND x<>3 AND x<>NULL`; the last part is unknown, so the whole filter never passes: **zero rows**.
- NOT EXISTS only asks 'is there a matching row?', so NULLs just don't match.
- LEFT JOIN ... IS NULL is also safe, but it can look confusing and needs a non-null column to test.
**Example:** One leave record was entered with a blank employee id. With NOT IN, the report 'employees with no leave' comes back empty, which is wrong and silent.
**Sample data:**

*employees*

| emp_id | name |
|---|---|
| 1 | Asha |
| 2 | Ravi |
| 3 | Meena |
| 4 | Kiran |
| 5 | Sonal |

*leave_requests*

| leave_id | emp_id | days |
|---|---|---|
| 1 | 1 | 2 |
| 2 | 1 | 1 |
| 3 | 3 | 5 |
| 4 | NULL | 1 |

**SQL:**
```sql
-- left_join_is_null
SELECT e.emp_id, e.name FROM employees e
LEFT JOIN leave_requests l ON l.emp_id = e.emp_id
WHERE l.leave_id IS NULL ORDER BY e.emp_id;

-- not_in
SELECT emp_id, name FROM employees
WHERE emp_id NOT IN (SELECT emp_id FROM leave_requests) ORDER BY emp_id;

-- not_exists
SELECT e.emp_id, e.name FROM employees e
WHERE NOT EXISTS (SELECT 1 FROM leave_requests l WHERE l.emp_id = e.emp_id) ORDER BY e.emp_id;

-- not_in_fixed
SELECT emp_id, name FROM employees
WHERE emp_id NOT IN (SELECT emp_id FROM leave_requests WHERE emp_id IS NOT NULL) ORDER BY emp_id;
```
**Output:**

*left_join_is_null*

| emp_id | name |
|---|---|
| 2 | Ravi |
| 4 | Kiran |
| 5 | Sonal |

*not_in*

| emp_id | name |
|---|---|
| *(no rows)* | |

*not_exists*

| emp_id | name |
|---|---|
| 2 | Ravi |
| 4 | Kiran |
| 5 | Sonal |

*not_in_fixed*

| emp_id | name |
|---|---|
| 2 | Ravi |
| 4 | Kiran |
| 5 | Sonal |

**pandas equivalent:**
```python
# DataFrames named as in the sample data above
m = employees.merge(leave_requests, on="emp_id", how="left", indicator=True)
anti = m[m["_merge"] == "left_only"][["emp_id", "name"]].sort_values("emp_id")
fixed = employees[~employees.emp_id.isin(leave_requests.emp_id.dropna())][["emp_id", "name"]]
results = {"left_join_is_null": anti, "not_exists": anti, "not_in_fixed": fixed}
# note: pandas isin() ignores the NaN, so it behaves like NOT EXISTS, not like SQL NOT IN
```
**Edge cases:** NOT IN is only safe when the subquery column is declared NOT NULL or filtered with IS NOT NULL. The same issue exists for NULLs on the outer side. Performance: modern engines plan NOT EXISTS and LEFT JOIN well; NOT IN can be slower in some.
**Likely follow-ups:**
- Which is best? NOT EXISTS: clear intent, NULL-safe, and fast with an index.
- Does `IN` have the same problem? No, IN just ignores NULLs; the trap is specific to NOT IN.
**Common mistakes:** Using NOT IN on a nullable column; assuming 'empty result' means 'everyone matched'; adding `OR emp_id IS NULL` as a hack.

### Q40 ⭐⭐ 🟡 Write a query to find records present in both tables (using INNER JOIN, INTERSECT, or EXISTS).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you find the overlap of two tables in several ways and explain how duplicates behave?
**Say this in the interview:** "I can use INNER JOIN, INTERSECT or EXISTS. INNER JOIN can repeat rows if one side has duplicates, so I add DISTINCT; INTERSECT removes duplicates automatically; EXISTS is a pure yes/no check."
**Explain simply:**
- **INNER JOIN**: returns matched rows; repeats a row once per match.
- **INTERSECT**: set operation; returns distinct rows present in both result sets, comparing every selected column (treats NULLs as equal). Not in MySQL before 8.0.31.
- **EXISTS**: for each row in A, checks whether a match exists in B; never duplicates A's rows.
**Example:** Employees present in both the HR master list and the payroll file: Asha (2 payslip rows) and Ravi.
**Sample data:**

*hr_employees*

| emp_id | name |
|---|---|
| 1 | Asha |
| 2 | Ravi |
| 3 | Meena |
| 4 | Kiran |

*payroll*

| emp_id | month |
|---|---|
| 1 | Jan |
| 1 | Feb |
| 2 | Jan |
| 5 | Jan |

**SQL:**
```sql
-- inner_join_raw
SELECT h.emp_id, h.name FROM hr_employees h
JOIN payroll p ON p.emp_id = h.emp_id ORDER BY h.emp_id;

-- inner_join_distinct
SELECT DISTINCT h.emp_id, h.name FROM hr_employees h
JOIN payroll p ON p.emp_id = h.emp_id ORDER BY h.emp_id;

-- intersect
SELECT emp_id FROM hr_employees
INTERSECT
SELECT emp_id FROM payroll ORDER BY emp_id;

-- exists
SELECT h.emp_id, h.name FROM hr_employees h
WHERE EXISTS (SELECT 1 FROM payroll p WHERE p.emp_id = h.emp_id) ORDER BY h.emp_id;
```
**Output:**

*inner_join_raw*

| emp_id | name |
|---|---|
| 1 | Asha |
| 1 | Asha |
| 2 | Ravi |

*inner_join_distinct*

| emp_id | name |
|---|---|
| 1 | Asha |
| 2 | Ravi |

*intersect*

| emp_id |
|---|
| 1 |
| 2 |

*exists*

| emp_id | name |
|---|---|
| 1 | Asha |
| 2 | Ravi |

**pandas equivalent:**
```python
# DataFrames named as in the sample data above
j = hr_employees.merge(payroll, on="emp_id")[["emp_id", "name"]]
dist = j.drop_duplicates().sort_values("emp_id")
results = {
 "inner_join_raw": j.sort_values("emp_id"),
 "inner_join_distinct": dist,
 "intersect": dist[["emp_id"]],
 "exists": hr_employees[hr_employees.emp_id.isin(payroll.emp_id)].sort_values("emp_id"),
}
```
**Edge cases:** Asha appears twice with a raw join because payroll has two rows for her. INTERSECT compares whole rows, so both queries must select the same columns. NULL keys: join/EXISTS never match them, INTERSECT does.
**Likely follow-ups:**
- Which is best? EXISTS for 'just filter A'; join when you need B's columns; INTERSECT for quick set logic across similar queries.
- Opposite? Rows in A not in B: EXCEPT (MINUS in Oracle) or NOT EXISTS.
**Common mistakes:** Forgetting DISTINCT after a join with duplicates; selecting different columns in INTERSECT; assuming INTERSECT exists in every MySQL version.

### Q41 ⭐⭐ 🟡 How do you simulate a FULL OUTER JOIN in a database (e.g., MySQL) that does not support it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you understand that FULL OUTER JOIN = LEFT JOIN rows + the extra RIGHT-only rows, and the UNION vs UNION ALL trap.
**Say this in the interview:** "A full outer join keeps everything from both tables. In MySQL, which has no FULL JOIN, I do a LEFT JOIN, then UNION ALL a second query that keeps only the right-table rows with no match."
**Explain simply:**
- FULL OUTER JOIN = all matched rows + left rows with no match + right rows with no match (NULLs fill the missing side).
- Recipe: (1) LEFT JOIN gives matched + left-only. (2) A second query gives right-only: LEFT JOIN with the tables swapped, then WHERE the other side's key IS NULL. (3) Stack them with `UNION ALL`.
- `UNION ALL` just stacks rows; `UNION` also removes duplicates, which can wrongly delete genuine duplicate rows, so prefer UNION ALL with the IS NULL filter.
- PostgreSQL, SQL Server, Oracle, DuckDB and modern SQLite (3.39+) support FULL JOIN directly; MySQL and MariaDB do not.
**Example:** HR wants every employee and every department in one list: Zoya sits in dept 99 that does not exist, and Legal (40) has nobody. A full join shows both oddities.
**Sample data:**

`staff`

| name | dept_id |
|---|---|
| Asha | 10 |
| Ravi | 10 |
| Meena | 20 |
| Zoya | 99 |

`depts`

| dept_id | dept_name |
|---|---|
| 10 | HR |
| 20 | Sales |
| 40 | Legal |

**SQL:** native FULL JOIN (SQLite, PostgreSQL, SQL Server)

```sql
SELECT s.name, d.dept_name
FROM staff s FULL OUTER JOIN depts d ON s.dept_id = d.dept_id
ORDER BY s.name, d.dept_name;
```

**Output:**

| name | dept_name |
|---|---|
| NULL | Legal |
| Asha | HR |
| Meena | Sales |
| Ravi | HR |
| Zoya | NULL |

**pandas equivalent:** (result identical to the SQL output above)

```python
res = (staff.merge(depts, on='dept_id', how='outer')[['name','dept_name']]
       .sort_values(['name','dept_name'], na_position='first').reset_index(drop=True))
```

**SQL (MySQL-style simulation (also runs in SQLite)):**

```sql
SELECT s.name, d.dept_name
FROM staff s LEFT JOIN depts d ON s.dept_id = d.dept_id
UNION ALL
SELECT s.name, d.dept_name
FROM depts d LEFT JOIN staff s ON s.dept_id = d.dept_id
WHERE s.dept_id IS NULL
ORDER BY 1, 2;
```

**Output:**

| name | dept_name |
|---|---|
| NULL | Legal |
| Asha | HR |
| Meena | Sales |
| Ravi | HR |
| Zoya | NULL |

**Edge cases:** NULL keys never match, so a staff row with NULL dept_id lands in the left-only part (correct). Without the `WHERE ... IS NULL` filter in part two, matched rows appear twice. SQLite sorts NULLs first in ORDER BY (so `na_position='first'` in pandas); PostgreSQL puts them last by default.
**Likely follow-ups:**
- Why not UNION instead of UNION ALL? It de-duplicates, so two identical genuine rows collapse into one.
- Can I use RIGHT JOIN for part two? Yes, if the database has RIGHT JOIN (MySQL does).
**Common mistakes:** Using plain `UNION` of LEFT and RIGHT joins (hides real duplicates and is slower), or forgetting the IS NULL filter so matched rows are doubled.

### Q42 ⭐⭐ 🟡 Write a query to find pairs of employees working in the same department (self join).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Self join with a < condition to avoid mirror and self pairs.
**Say this in the interview:** "I join the employee table to itself on the same department, and add e1.emp_id < e2.emp_id so I get each pair once and nobody is paired with themselves."
**Explain simply:**
- A self join means using the same table twice under two aliases (e1, e2), like having two photocopies of the list.
- `e1.dept_id = e2.dept_id` finds colleagues. Without more, Asha-Ravi and Ravi-Asha both show up, and Asha-Asha too.
- `e1.emp_id < e2.emp_id` removes self pairs and keeps one direction only.
- A department with n people gives n*(n-1)/2 pairs: HR has 3 people, so 3 pairs.
**Example:** Buddy-programme planning: pair every two people in the same department.
**Sample data:**

`employees`

| emp_id | name | dept_id | manager_id | salary | join_date |
|---|---|---|---|---|---|
| 1 | Asha | 10 | NULL | 90000 | 2018-03-01 |
| 2 | Ravi | 10 | 1 | 60000 | 2019-07-15 |
| 3 | Meena | 20 | 1 | 60000 | 2017-01-10 |
| 4 | Karan | 20 | 3 | 45000 | 2020-02-01 |
| 5 | Sneha | 20 | 3 | 45000 | 2021-05-20 |
| 6 | Imran | 30 | 2 | 52000 | 2022-09-12 |
| 7 | Divya | 10 | 2 | 38000 | 2023-01-09 |

**SQL:**

```sql
SELECT e1.name AS emp1, e2.name AS emp2, e1.dept_id
FROM employees e1
JOIN employees e2
  ON e1.dept_id = e2.dept_id AND e1.emp_id < e2.emp_id
ORDER BY e1.dept_id, e1.emp_id, e2.emp_id;
```

**Output:**

| emp1 | emp2 | dept_id |
|---|---|---|
| Asha | Ravi | 10 |
| Asha | Divya | 10 |
| Ravi | Divya | 10 |
| Meena | Karan | 20 |
| Meena | Sneha | 20 |
| Karan | Sneha | 20 |

**pandas equivalent:** (result identical to the SQL output above)

```python
m = employees.merge(employees, on='dept_id', suffixes=('_1','_2'))
res = (m[m.emp_id_1 < m.emp_id_2].sort_values(['dept_id','emp_id_1','emp_id_2'])
       [['name_1','name_2','dept_id']])
```

**Edge cases:** Finance has a single employee, so it gives no pair. NULL dept_id never matches, so those employees are skipped. Use `<>` instead of `<` only if you really want both directions.
**Likely follow-ups:**
- How many rows for a department of 10 people? 45 with `<`, 90 with `<>`.
- Can I use a window function instead? Not for pairs; a self join is the natural tool.
**Common mistakes:** Using `e1.emp_id <> e2.emp_id`, which returns every pair twice, or forgetting the condition and getting self pairs.

### Q43 ⭐⭐ 🟡 Write a query to find duplicate records in a table using a self join.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you spot repeated records and show which rows repeat, not just count them.
**Say this in the interview:** "I self join the table on the field that should be unique, like email, and keep only pairs where the id of the first is smaller. Those are the duplicates. GROUP BY with HAVING COUNT > 1 is the shorter way to count them."
**Explain simply:**
- Duplicate here means the same email appears on more than one row (a candidate entered twice in the hiring system).
- Join the table to itself: same email, but different primary key. `a.cand_id < b.cand_id` lists each duplicate pair once.
- To see which rows to delete, keep the smallest id: any row that appears as `b` in a pair is an extra copy.
- Three copies give three pairs (1-3, 1-5, 3-5), which is normal for a self join, hence the DISTINCT.
**Example:** The ATS (applicant tracking system) holds 6 rows but only 3 real people: Priya appears 3 times and Arun 2 times.
**Sample data:**

`candidates`

| cand_id | name | email |
|---|---|---|
| 1 | Priya S | priya@mail.com |
| 2 | Arun K | arun@mail.com |
| 3 | Priya Sharma | priya@mail.com |
| 4 | Neha R | neha@mail.com |
| 5 | P. Sharma | priya@mail.com |
| 6 | Arun Kumar | arun@mail.com |

**SQL:** rows to delete (extra copies)

```sql
SELECT DISTINCT b.cand_id AS extra_copy, b.name, b.email
FROM candidates a
JOIN candidates b ON a.email = b.email AND a.cand_id < b.cand_id
ORDER BY b.cand_id;
```

**Output:**

| extra_copy | name | email |
|---|---|---|
| 3 | Priya Sharma | priya@mail.com |
| 5 | P. Sharma | priya@mail.com |
| 6 | Arun Kumar | arun@mail.com |

**pandas equivalent:** (result identical to the SQL output above)

```python
m = candidates.merge(candidates, on='email', suffixes=('_a','_b'))
res = (m[m.cand_id_a < m.cand_id_b][['cand_id_b','name_b','email']]
       .drop_duplicates().sort_values('cand_id_b')
       .rename(columns={'cand_id_b':'extra_copy','name_b':'name'}))
```

**SQL (shorter alternative):**

```sql
SELECT email, COUNT(*) AS copies, MIN(cand_id) AS keep_id
FROM candidates GROUP BY email HAVING COUNT(*) > 1
ORDER BY email;
```

**Output:**

| email | copies | keep_id |
|---|---|---|
| arun@mail.com | 2 | 2 |
| priya@mail.com | 3 | 1 |

**Edge cases:** NULL emails never match each other in a join, so NULL-duplicates are missed (GROUP BY would group them together). Use a trimmed, lower-case key (`LOWER(TRIM(email))`) if data is messy. Name differences do not matter because we match on email.
**Likely follow-ups:**
- How do I delete the duplicates? `DELETE FROM candidates WHERE cand_id NOT IN (SELECT MIN(cand_id) FROM candidates GROUP BY email)` (take a backup first; MySQL needs a derived-table wrapper).
- Why prefer GROUP BY? It is faster and clearer; a self join is slower on large tables.
**Common mistakes:** Using `a.email = b.email` alone, which matches every row with itself, so every row looks like a duplicate.

### Q44 ⭐⭐ 🟡 Write a query to find employees who have the same salary as another employee, or who joined before their manager, using a self join.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Self joins with non-key conditions (same salary, date comparison against the manager).
**Say this in the interview:** "These are two separate self joins. Same salary: join employees to employees on salary with e1.emp_id < e2.emp_id. Joined before manager: join each employee to their manager's row and compare join dates."
**Explain simply:**
- The question says 'or', but it is really two questions; I answer both, and you can combine them with UNION if one list is wanted.
- Same salary: pair rows with equal salary but different people (the `<` on emp_id avoids self and mirror pairs).
- Before manager: `e.manager_id = m.emp_id` links an employee to the manager's row; then `e.join_date < m.join_date`.
- Dates stored as text in ISO format (YYYY-MM-DD) compare correctly; real DATE columns are better.
**Example:** Pay-equity check: Ravi and Meena both earn 60,000, and Karan and Sneha both 45,000. Also Meena joined in 2017, before her manager Asha (2018), an oddity HR may want to review.
**Sample data:**

`employees`

| emp_id | name | dept_id | manager_id | salary | join_date |
|---|---|---|---|---|---|
| 1 | Asha | 10 | NULL | 90000 | 2018-03-01 |
| 2 | Ravi | 10 | 1 | 60000 | 2019-07-15 |
| 3 | Meena | 20 | 1 | 60000 | 2017-01-10 |
| 4 | Karan | 20 | 3 | 45000 | 2020-02-01 |
| 5 | Sneha | 20 | 3 | 45000 | 2021-05-20 |
| 6 | Imran | 30 | 2 | 52000 | 2022-09-12 |
| 7 | Divya | 10 | 2 | 38000 | 2023-01-09 |

**SQL:** same salary

```sql
SELECT e1.name AS emp1, e2.name AS emp2, e1.salary
FROM employees e1
JOIN employees e2 ON e1.salary = e2.salary AND e1.emp_id < e2.emp_id
ORDER BY e1.salary DESC, e1.emp_id;
```

**Output:**

| emp1 | emp2 | salary |
|---|---|---|
| Ravi | Meena | 60000 |
| Karan | Sneha | 45000 |

**pandas equivalent:** (result identical to the SQL output above)

```python
m = employees.merge(employees, on='salary', suffixes=('_1','_2'))
res = (m[m.emp_id_1 < m.emp_id_2].sort_values(['salary','emp_id_1'], ascending=[False,True])
       [['name_1','name_2','salary']])
```

**SQL (joined before their manager):**

```sql
SELECT e.name AS employee, e.join_date, m.name AS manager, m.join_date AS manager_join_date
FROM employees e
JOIN employees m ON e.manager_id = m.emp_id
WHERE e.join_date < m.join_date;
```

**Output:**

| employee | join_date | manager | manager_join_date |
|---|---|---|---|
| Meena | 2017-01-10 | Asha | 2018-03-01 |

**pandas equivalent:** (result identical to the SQL output above)

```python
m = employees.merge(employees, left_on='manager_id', right_on='emp_id', suffixes=('','_m'))
res = m[m.join_date < m.join_date_m][['name','join_date','name_m','join_date_m']]
```

**Edge cases:** The top manager (manager_id NULL) drops out of the manager join with an inner join, which is fine here. Three people with one salary create three pairs. NULL salaries never equal each other.
**Likely follow-ups:**
- How to list everyone sharing a salary, not pairs? `GROUP BY salary HAVING COUNT(*) > 1` or `COUNT(*) OVER (PARTITION BY salary)`.
- Why not use <> for the pair? You would get both Ravi-Meena and Meena-Ravi.
**Common mistakes:** Comparing `e.join_date < m.join_date` without joining to the manager row (so comparing a row with itself), or using `=` on NULL manager_id and expecting a match.

### Q45 ⭐⭐ 🟡 How do you join tables on multiple columns (composite key)? Give an example.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know a single column is sometimes not unique, and you must join on the full key.
**Say this in the interview:** "When one column alone does not identify a row, I join on all columns of the composite key with AND in the ON clause, here emp_id and year."
**Explain simply:**
- A composite key is a key made of two or more columns together (employee + year identifies one policy row).
- Write `ON a.emp_id = b.emp_id AND a.year = b.year`.
- If you join on emp_id alone, each employee-year row matches every year of the other table, and the result multiplies (fan-out).
- PostgreSQL/MySQL also allow `USING (emp_id, year)`; SQL Server does not.
**Example:** Leave balance = allowed minus taken per employee per year. Employee 1 has two years in each table, so joining on emp_id alone gives 4 rows instead of 2.
**Sample data:**

`leave_policy`

| emp_id | year | days_allowed |
|---|---|---|
| 1 | 2025 | 24 |
| 1 | 2026 | 24 |
| 2 | 2025 | 18 |
| 2 | 2026 | 20 |
| 3 | 2026 | 22 |

`leave_taken`

| emp_id | year | days_taken |
|---|---|---|
| 1 | 2025 | 10 |
| 1 | 2026 | 4 |
| 2 | 2025 | 18 |
| 2 | 2026 | 6 |
| 3 | 2026 | 9 |

**SQL:** correct, composite join

```sql
SELECT p.emp_id, p.year, p.days_allowed, t.days_taken, p.days_allowed - t.days_taken AS balance
FROM leave_policy p
JOIN leave_taken t ON p.emp_id = t.emp_id AND p.year = t.year
ORDER BY p.emp_id, p.year;
```

**Output:**

| emp_id | year | days_allowed | days_taken | balance |
|---|---|---|---|---|
| 1 | 2025 | 24 | 10 | 14 |
| 1 | 2026 | 24 | 4 | 20 |
| 2 | 2025 | 18 | 18 | 0 |
| 2 | 2026 | 20 | 6 | 14 |
| 3 | 2026 | 22 | 9 | 13 |

**pandas equivalent:** (result identical to the SQL output above)

```python
m = leave_policy.merge(leave_taken, on=['emp_id','year'])
m['balance'] = m.days_allowed - m.days_taken
res = m.sort_values(['emp_id','year'])
```

**SQL (wrong, emp_id only (row count blows up)):**

```sql
SELECT COUNT(*) AS rows_returned
FROM leave_policy p JOIN leave_taken t ON p.emp_id = t.emp_id;
```

**Output:**

| rows_returned |
|---|
| 9 |

**Edge cases:** If either column has NULLs, those rows do not match. Make sure types match in both columns. If the pair is not truly unique in one table, you still get duplicates.
**Likely follow-ups:**
- How do I check the key is unique? `SELECT emp_id, year, COUNT(*) ... GROUP BY emp_id, year HAVING COUNT(*) > 1` should return nothing.
- Can the columns have different names? Yes: `ON a.emp = b.employee_id AND a.yr = b.year`.
**Common mistakes:** Joining on only part of the key and then wondering why totals are too high.

### Q46 ⭐⭐ 🟡 Write a query to join orders with customers and filter to customers from Hyderabad with orders above 5,000.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Basic join plus filters; can you apply two conditions on different tables.
**Say this in the interview:** "I inner join orders to customers on cust_id, then filter in WHERE: city = 'Hyderabad' AND amount > 5000."
**Explain simply:**
- JOIN glues each order to its customer row using the shared column cust_id.
- WHERE then keeps only rows meeting both conditions; the filters can reference columns from either table.
- For an INNER JOIN, putting the filters in ON or in WHERE gives the same result; they only differ for LEFT JOINs (Q15).
- 'Above 5,000' means `> 5000`; Sana's order of exactly 5,000 is excluded.
**Example:** Regional sales review: Hyderabad customers placing big orders.
**Sample data:**

`customers`

| cust_id | name | city |
|---|---|---|
| 1 | Anita | Hyderabad |
| 2 | Rahul | Pune |
| 3 | Sana | Hyderabad |
| 4 | Vikram | Mumbai |
| 5 | Lata | Hyderabad |

`orders`

| order_id | cust_id | order_date | amount |
|---|---|---|---|
| 101 | 1 | 2026-09-02 | 7500 |
| 102 | 1 | 2026-09-10 | 3200 |
| 103 | 2 | 2026-09-11 | 9000 |
| 104 | 3 | 2026-09-15 | 5000 |
| 105 | 3 | 2026-09-20 | 5200 |
| 106 | 5 | 2026-09-21 | 800 |

**SQL:**

```sql
SELECT c.name, c.city, o.order_id, o.amount
FROM orders o
JOIN customers c ON o.cust_id = c.cust_id
WHERE c.city = 'Hyderabad' AND o.amount > 5000
ORDER BY o.order_id;
```

**Output:**

| name | city | order_id | amount |
|---|---|---|---|
| Anita | Hyderabad | 101 | 7500 |
| Sana | Hyderabad | 105 | 5200 |

**pandas equivalent:** (result identical to the SQL output above)

```python
m = orders.merge(customers, on='cust_id')
res = (m[(m.city == 'Hyderabad') & (m.amount > 5000)]
       .sort_values('order_id')[['name','city','order_id','amount']])
```

**Edge cases:** Customers without orders vanish (inner join). Text comparison of city is case-sensitive in PostgreSQL, usually case-insensitive in MySQL/SQL Server; trim and standardise city names. NULL amounts never pass `> 5000`.
**Likely follow-ups:**
- Total per customer instead? Add `SUM(o.amount)` and `GROUP BY c.name`.
- Which is faster, filter in ON or WHERE? Same plan for an inner join; the optimiser filters early.
**Common mistakes:** Mixing AND and OR without brackets (`city='A' OR city='B' AND amount>5000`), where AND binds first and gives wrong rows.

### Q47 ⭐⭐ 🟡 Write a query to list all departments with the number of employees, including departments with no employees.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** LEFT JOIN from the 'all rows' table, and COUNT(column) vs COUNT(*).
**Say this in the interview:** "I start from departments and LEFT JOIN employees so every department stays. Then I COUNT(e.emp_id), not COUNT(*), so an empty department shows 0 instead of 1."
**Explain simply:**
- LEFT JOIN keeps every row of the left table (departments) even with no match; the employee columns become NULL.
- `COUNT(column)` skips NULLs, so Legal gets 0. `COUNT(*)` counts the row itself and would give 1.
- Group by the department so you get one row each.
**Example:** HR headcount report must list Legal even though it has no staff yet.
**Sample data:**

`departments`

| dept_id | dept_name |
|---|---|
| 10 | HR |
| 20 | Sales |
| 30 | Finance |
| 40 | Legal |

`employees`

| emp_id | name | dept_id | manager_id | salary | join_date |
|---|---|---|---|---|---|
| 1 | Asha | 10 | NULL | 90000 | 2018-03-01 |
| 2 | Ravi | 10 | 1 | 60000 | 2019-07-15 |
| 3 | Meena | 20 | 1 | 60000 | 2017-01-10 |
| 4 | Karan | 20 | 3 | 45000 | 2020-02-01 |
| 5 | Sneha | 20 | 3 | 45000 | 2021-05-20 |
| 6 | Imran | 30 | 2 | 52000 | 2022-09-12 |
| 7 | Divya | 10 | 2 | 38000 | 2023-01-09 |

**SQL:**

```sql
SELECT d.dept_name, COUNT(e.emp_id) AS headcount
FROM departments d
LEFT JOIN employees e ON e.dept_id = d.dept_id
GROUP BY d.dept_id, d.dept_name
ORDER BY d.dept_id;
```

**Output:**

| dept_name | headcount |
|---|---|
| HR | 3 |
| Sales | 3 |
| Finance | 1 |
| Legal | 0 |

**pandas equivalent:** (result identical to the SQL output above)

```python
m = departments.merge(employees, on='dept_id', how='left')
res = (m.groupby(['dept_id','dept_name'], as_index=False)['emp_id'].count()
       .rename(columns={'emp_id':'headcount'})[['dept_name','headcount']])
```

**Edge cases:** Employees with a NULL or unknown dept_id are not shown at all, because they have no department row to attach to. Use a FULL JOIN to expose them (Q41). Never put an employee filter in WHERE (Q48).
**Likely follow-ups:**
- How to show only empty departments? Add `HAVING COUNT(e.emp_id) = 0`.
- Why GROUP BY both id and name? Standard SQL needs every non-aggregated column listed.
**Common mistakes:** `COUNT(*)` after a LEFT JOIN: empty departments show 1 instead of 0.

### Q48 ⭐⭐ 🟡 How can a LEFT JOIN accidentally behave like an INNER JOIN? How do you spot and fix it?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know that a WHERE filter on the right table's column removes the NULL rows a LEFT JOIN created.
**Say this in the interview:** "If I filter on a right-table column in WHERE, the unmatched rows have NULL there, the condition fails, and they disappear, so the LEFT JOIN acts like an INNER JOIN. I move the condition into the ON clause."
**Explain simply:**
- LEFT JOIN creates NULL-filled rows for unmatched left rows.
- `WHERE e.salary > 50000` is not true for NULL, so Legal (and any department with no one above 50,000) is removed.
- Fix: put the filter in the ON clause (`ON e.dept_id = d.dept_id AND e.salary > 50000`), or write `WHERE e.salary > 50000 OR e.emp_id IS NULL`.
- Spot it: a LEFT JOIN whose result has no NULLs on the right side, or fewer rows than the left table.
**Example:** Question: how many employees earn above 50,000 in each department, with departments that have none still listed? Legal should appear with 0.
**Sample data:**

`departments`

| dept_id | dept_name |
|---|---|
| 10 | HR |
| 20 | Sales |
| 30 | Finance |
| 40 | Legal |

`employees`

| emp_id | name | dept_id | manager_id | salary | join_date |
|---|---|---|---|---|---|
| 1 | Asha | 10 | NULL | 90000 | 2018-03-01 |
| 2 | Ravi | 10 | 1 | 60000 | 2019-07-15 |
| 3 | Meena | 20 | 1 | 60000 | 2017-01-10 |
| 4 | Karan | 20 | 3 | 45000 | 2020-02-01 |
| 5 | Sneha | 20 | 3 | 45000 | 2021-05-20 |
| 6 | Imran | 30 | 2 | 52000 | 2022-09-12 |
| 7 | Divya | 10 | 2 | 38000 | 2023-01-09 |

**SQL:** buggy: filter in WHERE

```sql
SELECT d.dept_name, COUNT(e.emp_id) AS high_earners
FROM departments d LEFT JOIN employees e ON e.dept_id = d.dept_id
WHERE e.salary > 50000
GROUP BY d.dept_name ORDER BY d.dept_name;
```

**Output:**

| dept_name | high_earners |
|---|---|
| Finance | 1 |
| HR | 2 |
| Sales | 1 |

**SQL (fixed: filter in ON):**

```sql
SELECT d.dept_name, COUNT(e.emp_id) AS high_earners
FROM departments d LEFT JOIN employees e ON e.dept_id = d.dept_id AND e.salary > 50000
GROUP BY d.dept_name ORDER BY d.dept_name;
```

**Output:**

| dept_name | high_earners |
|---|---|
| Finance | 1 |
| HR | 2 |
| Legal | 0 |
| Sales | 1 |

**pandas equivalent:** (result identical to the SQL output above)

```python
e = employees[employees.salary > 50000]
m = departments.merge(e, on='dept_id', how='left')
res = (m.groupby('dept_name', as_index=False)['emp_id'].count()
       .rename(columns={'emp_id':'high_earners'}).sort_values('dept_name'))
```

**Edge cases:** Filters on the LEFT table's columns are safe in WHERE. A deliberate `WHERE e.emp_id IS NULL` is the anti-join pattern (Q38), not a bug.
**Likely follow-ups:**
- Is it a bug when I want only matches? No, then use INNER JOIN and say so for clarity.
- Does the same happen with RIGHT JOIN? Yes, mirrored: filter on the left table's column.
**Common mistakes:** Writing LEFT JOIN, then filtering the right table in WHERE, and being surprised that zero-match rows vanish.

### Q49 ⭐⭐ 🟡 What is the difference between joining then aggregating and aggregating then joining? Why can joins inflate totals (fan-out)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Understanding grain (one row per what?) and fan-out when joining one-to-many.
**Say this in the interview:** "Joining first repeats the one-side values once per matching many-side row, so SUM on them gets inflated. I aggregate the many side first and then join."
**Explain simply:**
- Grain means what one row represents: one row per employee in employees, one per leave in leave_records.
- Join then aggregate: employee 2 has 3 leave rows, so their 60,000 salary is repeated 3 times and SUM(salary) counts it 3 times (fan-out = rows multiplied by the join).
- Aggregate then join: first reduce leave_records to one row per employee (total days), then join, so each salary is counted once.
- Rule: before summing a column after a join, ask 'is this column now repeated?'
**Example:** Total salary bill per department, together with leave days taken. HR's true salary total is 90,000 + 60,000 + 38,000 = 188,000; the wrong query will report 308,000.
**Sample data:**

`employees`

| emp_id | name | dept_id | manager_id | salary | join_date |
|---|---|---|---|---|---|
| 1 | Asha | 10 | NULL | 90000 | 2018-03-01 |
| 2 | Ravi | 10 | 1 | 60000 | 2019-07-15 |
| 3 | Meena | 20 | 1 | 60000 | 2017-01-10 |
| 4 | Karan | 20 | 3 | 45000 | 2020-02-01 |
| 5 | Sneha | 20 | 3 | 45000 | 2021-05-20 |
| 6 | Imran | 30 | 2 | 52000 | 2022-09-12 |
| 7 | Divya | 10 | 2 | 38000 | 2023-01-09 |

`leave_records`

| leave_id | emp_id | days |
|---|---|---|
| 1 | 1 | 2 |
| 2 | 2 | 3 |
| 3 | 2 | 1 |
| 4 | 2 | 5 |
| 5 | 3 | 2 |
| 6 | 4 | 1 |
| 7 | 4 | 2 |
| 8 | 7 | 4 |

**SQL:** wrong: join first, then SUM

```sql
SELECT e.dept_id, SUM(e.salary) AS total_salary, SUM(l.days) AS leave_days
FROM employees e JOIN leave_records l ON l.emp_id = e.emp_id
GROUP BY e.dept_id ORDER BY e.dept_id;
```

**Output:**

| dept_id | total_salary | leave_days |
|---|---|---|
| 10 | 308000 | 15 |
| 20 | 150000 | 5 |

**SQL (right: aggregate leave first, then join):**

```sql
SELECT e.dept_id, SUM(e.salary) AS total_salary, SUM(l.days) AS leave_days
FROM employees e
LEFT JOIN (SELECT emp_id, SUM(days) AS days FROM leave_records GROUP BY emp_id) l
  ON l.emp_id = e.emp_id
GROUP BY e.dept_id ORDER BY e.dept_id;
```

**Output:**

| dept_id | total_salary | leave_days |
|---|---|---|
| 10 | 188000 | 15 |
| 20 | 150000 | 5 |
| 30 | 52000 | NULL |

**pandas equivalent:** (result identical to the SQL output above)

```python
ls = leave_records.groupby('emp_id', as_index=False)['days'].sum()
m = employees.merge(ls, on='emp_id', how='left')
res = (m.groupby('dept_id', as_index=False)
       .agg(total_salary=('salary','sum'), leave_days=('days', lambda x: x.sum(min_count=1))))
```

**Edge cases:** In the wrong query the inner join also dropped employees with no leave (Imran, Finance's only person, vanishes entirely). Sales looks right only by coincidence: Karan's double count cancels Sneha's missing salary. Employees without leave give NULL days after the LEFT JOIN; SUM ignores NULLs. SUM(DISTINCT salary) is not a fix: two people with the same salary collapse into one.
**Likely follow-ups:**
- How can I detect fan-out? Compare row counts before and after the join, or check uniqueness of the join key on the one side.
- Does COUNT(DISTINCT emp_id) help? For counting people yes; for sums use pre-aggregation.
**Common mistakes:** Using SUM(DISTINCT) as a quick fix, or not noticing that the sum is larger than the table's own total.

### Q50 ⭐⭐ 🟡 Write a query to find the latest order of each customer using a join with a subquery on MAX(order_date).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Using an aggregate subquery as a derived table and joining back to get the full row.
**Say this in the interview:** "A subquery gets each customer's maximum order date; I join it back to orders on customer and date to pull the whole latest order. I also mention ties: two orders on the same day both come back."
**Explain simply:**
- The subquery `SELECT cust_id, MAX(order_date) ... GROUP BY cust_id` returns one row per customer: the last date only.
- Joining it back on both cust_id and order_date fetches the other columns (order_id, amount) of that row.
- Ties: Sana has two orders on 15 Sep, so both are returned. To get exactly one, tie-break (e.g. highest order_id) or use ROW_NUMBER().
- LEFT JOIN from customers if you also want customers with no orders.
**Example:** Latest interaction per candidate, latest appraisal per employee, last order per customer.
**Sample data:**

`customers`

| cust_id | name |
|---|---|
| 1 | Anita |
| 2 | Rahul |
| 3 | Sana |
| 4 | Vikram |

`orders`

| order_id | cust_id | order_date | amount |
|---|---|---|---|
| 101 | 1 | 2026-08-02 | 7500 |
| 102 | 1 | 2026-09-10 | 3200 |
| 103 | 2 | 2026-09-11 | 9000 |
| 104 | 3 | 2026-09-15 | 5000 |
| 105 | 3 | 2026-09-15 | 5200 |
| 106 | 3 | 2026-07-01 | 800 |

**SQL:**

```sql
SELECT c.name, o.order_id, o.order_date, o.amount
FROM customers c
JOIN orders o ON o.cust_id = c.cust_id
JOIN (SELECT cust_id, MAX(order_date) AS last_date
      FROM orders GROUP BY cust_id) m
  ON m.cust_id = o.cust_id AND m.last_date = o.order_date
ORDER BY c.name, o.order_id;
```

**Output:**

| name | order_id | order_date | amount |
|---|---|---|---|
| Anita | 102 | 2026-09-10 | 3200 |
| Rahul | 103 | 2026-09-11 | 9000 |
| Sana | 104 | 2026-09-15 | 5000 |
| Sana | 105 | 2026-09-15 | 5200 |

**pandas equivalent:** (result identical to the SQL output above)

```python
last = orders.groupby('cust_id', as_index=False)['order_date'].max().rename(columns={'order_date':'last_date'})
m = orders.merge(last, left_on=['cust_id','order_date'], right_on=['cust_id','last_date'])
res = (m.merge(customers, on='cust_id').sort_values(['name','order_id'])
       [['name','order_id','order_date','amount']])
```

**SQL (window-function alternative (one row per customer)):**

```sql
SELECT name, order_id, order_date, amount FROM (
  SELECT c.name, o.order_id, o.order_date, o.amount,
         ROW_NUMBER() OVER (PARTITION BY c.cust_id ORDER BY o.order_date DESC, o.order_id DESC) AS rn
  FROM customers c JOIN orders o ON o.cust_id = c.cust_id) t
WHERE rn = 1 ORDER BY name;
```

**Output:**

| name | order_id | order_date | amount |
|---|---|---|---|
| Anita | 102 | 2026-09-10 | 3200 |
| Rahul | 103 | 2026-09-11 | 9000 |
| Sana | 105 | 2026-09-15 | 5200 |

**Edge cases:** Vikram has no orders so he is absent (inner join). Date ties return multiple rows. NULL dates are ignored by MAX. Do not write `WHERE order_date = (SELECT MAX(order_date) FROM orders)` without correlation: that gives only the one global latest date.
**Likely follow-ups:**
- Why not just GROUP BY and select amount? The amount is not in the group, so the answer is invalid or arbitrary (old MySQL modes allowed it).
- Which is better, join or ROW_NUMBER? ROW_NUMBER is cleaner and handles ties your way.
**Common mistakes:** Joining on only cust_id (returns all orders again) or selecting non-grouped columns next to MAX().

### Q51 ⭐⭐ 🟡 Write a query using a self join to get the previous row's value (e.g., day-over-day sales).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you compare a row with the row before it without window functions (self join + subquery).
**Say this in the interview:** "I join the table to itself, matching each row to the row with the largest earlier date. That gives the previous value side by side, so I can subtract. Today I would just use LAG, but the self join shows I understand it."
**Explain simply:**
- Alias the table twice: `t` is today's row, `p` is the previous row.
- Join condition `p.sale_date = (SELECT MAX(sale_date) FROM daily_sales WHERE sale_date < t.sale_date)` picks the latest earlier date, so gaps (no 4 Oct here) are handled.
- Use LEFT JOIN so the first day, which has no previous row, still appears with NULLs.
- A 'calendar yesterday' join (`date + 1 day`) is simpler but returns NULL after a gap.
**Example:** Day-over-day change in daily hires or sales. 5 Oct follows 3 Oct (4 Oct has no record): 18,000 - 11,000 = +7,000.
**Sample data:**

`daily_sales`

| sale_date | sales |
|---|---|
| 2026-10-01 | 12000 |
| 2026-10-02 | 15000 |
| 2026-10-03 | 11000 |
| 2026-10-05 | 18000 |
| 2026-10-06 | 17000 |

**SQL:** previous available row

```sql
SELECT t.sale_date, t.sales, p.sale_date AS prev_date, p.sales AS prev_sales,
       t.sales - p.sales AS change
FROM daily_sales t
LEFT JOIN daily_sales p
  ON p.sale_date = (SELECT MAX(sale_date) FROM daily_sales WHERE sale_date < t.sale_date)
ORDER BY t.sale_date;
```

**Output:**

| sale_date | sales | prev_date | prev_sales | change |
|---|---|---|---|---|
| 2026-10-01 | 12000 | NULL | NULL | NULL |
| 2026-10-02 | 15000 | 2026-10-01 | 12000 | 3000 |
| 2026-10-03 | 11000 | 2026-10-02 | 15000 | -4000 |
| 2026-10-05 | 18000 | 2026-10-03 | 11000 | 7000 |
| 2026-10-06 | 17000 | 2026-10-05 | 18000 | -1000 |

**pandas equivalent:** (result identical to the SQL output above)

```python
d = daily_sales.sort_values('sale_date').reset_index(drop=True)
d['prev_date'] = d.sale_date.shift()
d['prev_sales'] = d.sales.shift()
d['change'] = d.sales - d.prev_sales
res = d
```

**SQL (window-function version (PostgreSQL, MySQL 8+, SQL Server, SQLite 3.25+)):**

```sql
SELECT sale_date, sales, LAG(sales) OVER (ORDER BY sale_date) AS prev_sales,
       sales - LAG(sales) OVER (ORDER BY sale_date) AS change
FROM daily_sales ORDER BY sale_date;
```

**Output:**

| sale_date | sales | prev_sales | change |
|---|---|---|---|
| 2026-10-01 | 12000 | NULL | NULL |
| 2026-10-02 | 15000 | 12000 | 3000 |
| 2026-10-03 | 11000 | 15000 | -4000 |
| 2026-10-05 | 18000 | 11000 | 7000 |
| 2026-10-06 | 17000 | 18000 | -1000 |

**SQL (strict calendar-yesterday join (SQLite date syntax; shows the gap problem)):**

```sql
SELECT t.sale_date, t.sales, p.sales AS yesterday
FROM daily_sales t
LEFT JOIN daily_sales p ON p.sale_date = date(t.sale_date, '-1 day')
ORDER BY t.sale_date;
```

**Output:**

| sale_date | sales | yesterday |
|---|---|---|
| 2026-10-01 | 12000 | NULL |
| 2026-10-02 | 15000 | 12000 |
| 2026-10-03 | 11000 | 15000 |
| 2026-10-05 | 18000 | NULL |
| 2026-10-06 | 17000 | 18000 |

**Edge cases:** First row has no previous value (NULL). Duplicate dates make the subquery join ambiguous: aggregate per day first. Ties and gaps depend on your definition of 'previous'. Date arithmetic differs: `DATEADD(day,-1,d)` in SQL Server, `d - INTERVAL '1 day'` in PostgreSQL, `DATE_SUB(d, INTERVAL 1 DAY)` in MySQL (not run here).
**Likely follow-ups:**
- Why is LAG better? One pass, no repeated subquery, easier to read.
- How to get percentage change? `(sales - prev)*100.0/prev`, guarding against prev = 0.
**Common mistakes:** Joining on `t.id = p.id + 1`, which breaks when ids have gaps, or using an INNER JOIN and silently losing the first row.

### Q52 ⭐⭐ 🟡 How do you join two tables when the key columns have different data types or formats (text vs number, trailing spaces, case)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Data-cleaning awareness: joins fail silently when the keys look the same but are not.
**Say this in the interview:** "First I profile the keys. Then I clean both sides inside the ON clause: TRIM to remove spaces, UPPER/LOWER for case, CAST to a common type. Long term I fix the data, because functions on join columns slow the query."
**Explain simply:**
- Keys that look equal can differ: text vs number, leading/trailing spaces, upper vs lower case, leading zeros, hidden characters.
- Make both sides the same type and shape: `CAST(TRIM(p.emp_no) AS INTEGER)`; for text codes use `UPPER(TRIM(x))`.
- Behaviour differs by database: PostgreSQL raises an error for integer = text; MySQL and SQL Server convert silently (sometimes wrongly, and the index may stop being used); SQLite compares loosely (not run here for the others).
- Anything that cannot convert (like 'E104') must be handled: strip the letter or use TRY_CAST (SQL Server), `CASE WHEN ... GLOB` or a mapping table.
**Example:** HRMS holds employee numbers as integers; payroll exported them as text with stray spaces and a zero-padded or prefixed form. In SQLite the loose type comparison happens to forgive the spaces and zero padding, but 'E104' (Karan) is still missed; stricter databases miss or reject more.
**Sample data:**

`employees`

| emp_no | name |
|---|---|
| 101 | Asha |
| 102 | Ravi |
| 103 | Meena |
| 104 | Karan |

`payroll`

| emp_no | net_pay |
|---|---|
| 101  | 50000 |
|  102 | 42000 |
| 0103 | 38000 |
| E104 | 30000 |

**SQL:** naive join (what the data does as-is)

```sql
SELECT e.name, p.net_pay FROM employees e JOIN payroll p ON e.emp_no = p.emp_no ORDER BY e.emp_no;
```

**Output:**

| name | net_pay |
|---|---|
| Asha | 50000 |
| Ravi | 42000 |
| Meena | 38000 |

**SQL (cleaned join):**

```sql
SELECT e.name, p.net_pay
FROM employees e
JOIN payroll p ON e.emp_no = CAST(REPLACE(TRIM(p.emp_no), 'E', '') AS INTEGER)
ORDER BY e.emp_no;
```

**Output:**

| name | net_pay |
|---|---|
| Asha | 50000 |
| Ravi | 42000 |
| Meena | 38000 |
| Karan | 30000 |

**pandas equivalent:** (result identical to the SQL output above)

```python
p = payroll.copy()
p['emp_no'] = p.emp_no.str.strip().str.replace('E', '', regex=False).astype(int)
res = employees.merge(p, on='emp_no').sort_values('emp_no')[['name','net_pay']]
```

**Edge cases:** NULL keys never match. CAST of a non-numeric string gives 0 or an error depending on the database. Compare row counts before and after cleaning, and test uniqueness of the cleaned key (leading zeros can make two different codes collide).
**Likely follow-ups:**
- Where should I really fix this? At load time: clean once, store the right type, add a constraint.
- Does a function on the join column hurt speed? Yes, it usually blocks index use; clean a copy of the column instead.
**Common mistakes:** Trusting a join that returns fewer rows without checking why; or blindly using LIKE or LOWER on only one side.

### Q53 ⭐⭐ 🟡 What is a range (non-equi) join? Give an example such as mapping a salary or score to a band/grade table.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Know that joins need not use equals; also boundary care.
**Say this in the interview:** "A range join, also called a non-equi join, matches a value to the band it falls in using >= and < instead of =. I use a half-open range so a value on the boundary lands in exactly one band."
**Explain simply:**
- Equi join uses `=`. A non-equi/range join uses `>`, `<`, `BETWEEN` and similar.
- Each employee matches the one band whose min <= salary < max.
- Use `>= min AND < max`: `BETWEEN` includes both ends, so 45,000 would match two bands if one ends at 45,000 and the next starts there.
- Bands must not overlap, otherwise one employee gets several rows.
**Example:** Grading salaries: 45,000 falls into G2 (45,000 up to 59,999), not G1.
**Sample data:**

`employees`

| emp_id | name | dept_id | manager_id | salary | join_date |
|---|---|---|---|---|---|
| 1 | Asha | 10 | NULL | 90000 | 2018-03-01 |
| 2 | Ravi | 10 | 1 | 60000 | 2019-07-15 |
| 3 | Meena | 20 | 1 | 60000 | 2017-01-10 |
| 4 | Karan | 20 | 3 | 45000 | 2020-02-01 |
| 5 | Sneha | 20 | 3 | 45000 | 2021-05-20 |
| 6 | Imran | 30 | 2 | 52000 | 2022-09-12 |
| 7 | Divya | 10 | 2 | 38000 | 2023-01-09 |

`salary_bands`

| grade | min_sal | max_sal |
|---|---|---|
| G1 | 30000 | 45000 |
| G2 | 45000 | 60000 |
| G3 | 60000 | 80000 |
| G4 | 80000 | 120000 |

**SQL:**

```sql
SELECT e.name, e.salary, b.grade
FROM employees e
JOIN salary_bands b ON e.salary >= b.min_sal AND e.salary < b.max_sal
ORDER BY e.salary DESC, e.name;
```

**Output:**

| name | salary | grade |
|---|---|---|
| Asha | 90000 | G4 |
| Meena | 60000 | G3 |
| Ravi | 60000 | G3 |
| Imran | 52000 | G2 |
| Karan | 45000 | G2 |
| Sneha | 45000 | G2 |
| Divya | 38000 | G1 |

**pandas equivalent:** (result identical to the SQL output above)

```python
m = employees.merge(salary_bands, how='cross')
m = m[(m.salary >= m.min_sal) & (m.salary < m.max_sal)]
res = m.sort_values(['salary','name'], ascending=[False,True])[['name','salary','grade']]
```

**Edge cases:** A salary outside all bands (say 25,000 or 150,000) disappears in an inner join; use LEFT JOIN to keep and flag them as 'unbanded'. Overlapping bands create duplicates. NULL salaries match nothing. Non-equi joins can be slow on big tables, since indexes help less.
**Likely follow-ups:**
- Pandas alternative? `pd.cut` with bin edges, or `pd.merge_asof` for 'nearest lower bound'.
- Another typical use? Matching a sale date to the price valid on that date (effective-dated pricing).
**Common mistakes:** Using BETWEEN with touching boundaries, which double-counts boundary values.

### Q54 ⭐⭐ 🟡 How do you join a fact table (orders) to dimension tables (customers, products, dates)? What is a star schema in join terms?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you can read a data warehouse layout and chain joins from one central table.
**Say this in the interview:** "The fact table holds the measurable events, here orders with amounts, plus keys. The dimension tables describe who, what and when. A star schema means the fact table sits in the middle and I join each dimension to it on one key, giving a star shape."
**Explain simply:**
- Fact table: one row per event (an order line), with numbers to add up (amount) and foreign keys (a foreign key is a column that points to another table's id).
- Dimension tables: descriptive lookups (customers, products, dates). Each is joined only to the fact table.
- Join pattern: `FROM fact JOIN dim1 ON ... JOIN dim2 ON ...`, then GROUP BY descriptive columns and SUM the fact measures.
- Many dimension joins are many-to-one, so they do not multiply fact rows (as long as dimension keys are unique).
**Example:** Revenue for September 2026 by city and product category.
**Sample data:**

`customers`

| cust_id | name | city |
|---|---|---|
| 1 | Anita | Hyderabad |
| 2 | Rahul | Pune |
| 3 | Sana | Hyderabad |

`products`

| prod_id | prod_name | category |
|---|---|---|
| 10 | Laptop | Electronics |
| 11 | Mouse | Electronics |
| 12 | Desk | Furniture |

`dim_date`

| date_key | month | quarter |
|---|---|---|
| 2026-08-20 | 2026-08 | Q3 |
| 2026-09-02 | 2026-09 | Q3 |
| 2026-09-15 | 2026-09 | Q3 |
| 2026-10-01 | 2026-10 | Q4 |

`orders`

| order_id | cust_id | prod_id | order_date | amount |
|---|---|---|---|---|
| 1 | 1 | 10 | 2026-09-02 | 60000 |
| 2 | 1 | 11 | 2026-09-02 | 800 |
| 3 | 2 | 12 | 2026-09-15 | 7000 |
| 4 | 3 | 10 | 2026-09-15 | 55000 |
| 5 | 3 | 11 | 2026-08-20 | 900 |
| 6 | 2 | 10 | 2026-10-01 | 58000 |

**SQL:**

```sql
SELECT c.city, p.category, SUM(o.amount) AS revenue
FROM orders o
JOIN customers c ON o.cust_id = c.cust_id
JOIN products p ON o.prod_id = p.prod_id
JOIN dim_date d ON o.order_date = d.date_key
WHERE d.month = '2026-09'
GROUP BY c.city, p.category
ORDER BY c.city, p.category;
```

**Output:**

| city | category | revenue |
|---|---|---|
| Hyderabad | Electronics | 115800 |
| Pune | Furniture | 7000 |

**pandas equivalent:** (result identical to the SQL output above)

```python
m = (orders.merge(customers, on='cust_id').merge(products, on='prod_id')
           .merge(dim_date, left_on='order_date', right_on='date_key'))
m = m[m.month == '2026-09']
res = (m.groupby(['city','category'], as_index=False)['amount'].sum()
       .rename(columns={'amount':'revenue'}))
```

**Edge cases:** If a fact row has a missing or unknown dimension key, an INNER JOIN silently drops its revenue; start from the fact table with LEFT JOIN to the dimensions when totals must reconcile. Dimension keys must be unique, otherwise rows duplicate. Date dimensions let you group by month or quarter without date functions.
**Likely follow-ups:**
- Star vs snowflake? In a snowflake, dimensions are split further (product to category table), so more joins.
- Why not store everything in one wide table? Redundancy, update errors, and larger storage.
**Common mistakes:** Joining two fact tables directly (fan-out); aggregate each to the same grain first (see Q49).

### Q55 ⭐⭐ 🟡 Which table should go on the left in a LEFT JOIN? What changes if you swap them?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you think about 'what do I want to keep all of' before writing a LEFT JOIN.
**Say this in the interview:** "The table whose every row I must keep goes on the left. If I need every customer, including those without orders, customers goes left. If I swap, I keep every order instead, including orders with no known customer."
**Explain simply:**
- LEFT JOIN keeps all rows of the left table and only matching rows of the right.
- Left = the 'population' you report on (all employees, all customers). Right = the optional extra data (leave, orders).
- Swapping changes both the row count and which side shows NULLs, so it answers a different question.
- Equivalent: `A LEFT JOIN B` equals `B RIGHT JOIN A`; most teams stick to LEFT for readability.
**Example:** Customers: 4 (Vikram and Sana have no orders). Orders: 4, one of which (104) belongs to customer 9 who is not in the customer table.
**Sample data:**

`customers`

| cust_id | name |
|---|---|
| 1 | Anita |
| 2 | Rahul |
| 3 | Sana |
| 4 | Vikram |

`orders`

| order_id | cust_id | amount |
|---|---|---|
| 101 | 1 | 7500 |
| 102 | 1 | 3200 |
| 103 | 2 | 9000 |
| 104 | 9 | 500 |

**SQL:** customers LEFT JOIN orders (every customer)

```sql
SELECT c.name, o.order_id
FROM customers c LEFT JOIN orders o ON o.cust_id = c.cust_id
ORDER BY c.cust_id, o.order_id;
```

**Output:**

| name | order_id |
|---|---|
| Anita | 101 |
| Anita | 102 |
| Rahul | 103 |
| Sana | NULL |
| Vikram | NULL |

**pandas equivalent:** (result identical to the SQL output above)

```python
res = (customers.merge(orders, on='cust_id', how='left')
       .sort_values(['cust_id','order_id'])[['name','order_id']])
```

**SQL (orders LEFT JOIN customers (every order)):**

```sql
SELECT c.name, o.order_id
FROM orders o LEFT JOIN customers c ON o.cust_id = c.cust_id
ORDER BY o.order_id;
```

**Output:**

| name | order_id |
|---|---|
| Anita | 101 |
| Anita | 102 |
| Rahul | 103 |
| NULL | 104 |

**pandas equivalent:** (result identical to the SQL output above)

```python
res = (orders.merge(customers, on='cust_id', how='left')
       .sort_values('order_id')[['name','order_id']]).reset_index(drop=True)
```

**Edge cases:** Two-to-one: Anita's two orders make the first query longer than the customer table (5 rows for 4 customers). The second query exposes the orphan order 104 (name NULL), a data-quality flag. If both tables have unmatched rows, you need a FULL JOIN (Q41).
**Likely follow-ups:**
- Which is better for finding customers with no orders? Customers on the left, then `WHERE o.order_id IS NULL`.
- Does order of tables matter for INNER JOIN? No for results; only the optimiser's strategy may differ.
**Common mistakes:** Putting the 'detail' table on the left and then expecting to see all customers.

### Q56 ⭐⭐ 🟡 What is the order of SQL execution (FROM/JOIN, WHERE, GROUP BY, HAVING, SELECT, ORDER BY) and how does it affect join filters?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** That you know SQL runs in a different order than you write it, which explains many errors and WHERE vs ON behaviour.
**Say this in the interview:** "Written order is SELECT first, but the database runs FROM and JOIN first, then WHERE, GROUP BY, HAVING, SELECT, DISTINCT, ORDER BY, and finally LIMIT. So WHERE cannot see aliases or aggregates, and a WHERE on the right table of a LEFT JOIN runs after the join."
**Explain simply:**
- 1 FROM + JOIN: build the combined rows (ON is applied here). 2 WHERE: filter rows. 3 GROUP BY: make groups. 4 HAVING: filter groups. 5 SELECT: compute columns and aliases. 6 DISTINCT. 7 ORDER BY. 8 LIMIT/TOP.
- Because WHERE runs before SELECT, an alias defined in SELECT is unknown in WHERE (PostgreSQL, MySQL, SQL Server raise an error; SQLite and DuckDB are lenient).
- Because WHERE runs before GROUP BY, you cannot use SUM() in WHERE; use HAVING.
- Because ON runs during the join and WHERE after it, a right-table filter in WHERE wipes out the NULL rows of a LEFT JOIN (Q48).
- ORDER BY runs after SELECT, so it can use aliases.
**Example:** Departments (except Legal, id 40) with at least one employee, ranked by average salary, top two.
**Sample data:**

`departments`

| dept_id | dept_name |
|---|---|
| 10 | HR |
| 20 | Sales |
| 30 | Finance |
| 40 | Legal |

`employees`

| emp_id | name | dept_id | manager_id | salary | join_date |
|---|---|---|---|---|---|
| 1 | Asha | 10 | NULL | 90000 | 2018-03-01 |
| 2 | Ravi | 10 | 1 | 60000 | 2019-07-15 |
| 3 | Meena | 20 | 1 | 60000 | 2017-01-10 |
| 4 | Karan | 20 | 3 | 45000 | 2020-02-01 |
| 5 | Sneha | 20 | 3 | 45000 | 2021-05-20 |
| 6 | Imran | 30 | 2 | 52000 | 2022-09-12 |
| 7 | Divya | 10 | 2 | 38000 | 2023-01-09 |

**SQL:**

```sql
SELECT d.dept_name, COUNT(e.emp_id) AS headcount, ROUND(AVG(e.salary), 0) AS avg_salary
FROM departments d                              -- 1. FROM / JOIN
LEFT JOIN employees e ON e.dept_id = d.dept_id
WHERE d.dept_id < 40                            -- 2. WHERE (row filter)
GROUP BY d.dept_name                            -- 3. GROUP BY
HAVING COUNT(e.emp_id) >= 1                     -- 4. HAVING (group filter)
ORDER BY avg_salary DESC                        -- 7. ORDER BY (can use alias)
LIMIT 2;                                        -- 8. LIMIT (TOP 2 in SQL Server)
```

**Output:**

| dept_name | headcount | avg_salary |
|---|---|---|
| HR | 3 | 62667 |
| Finance | 1 | 52000 |

**pandas equivalent:** (result identical to the SQL output above)

```python
m = departments[departments.dept_id < 40].merge(employees, on='dept_id', how='left')
g = (m.groupby('dept_name', as_index=False)
      .agg(headcount=('emp_id','count'), avg_salary=('salary','mean')))
g['avg_salary'] = g.avg_salary.round(0)
res = g[g.headcount >= 1].sort_values('avg_salary', ascending=False).head(2)
```

**Edge cases:** NULLs: AVG ignores NULL salaries; COUNT(column) ignores NULLs. Ties in ORDER BY make LIMIT arbitrary; add a second sort column. A window function is evaluated after WHERE/GROUP BY/HAVING but before ORDER BY, which is why you cannot filter on it directly in WHERE.
**Likely follow-ups:**
- Why can ORDER BY use an alias but WHERE not? ORDER BY runs after SELECT.
- Where is DISTINCT? After SELECT, before ORDER BY.
**Common mistakes:** Writing `WHERE COUNT(*) > 1` instead of HAVING, or filtering the right table in WHERE after a LEFT JOIN.

### Q57 ⭐⭐ 🟡 Write a query to find customers who bought product A but not product B (join or self join approach).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Combining 'has A' and 'does not have B' with joins, and handling repeat purchases.
**Say this in the interview:** "I join customers to their A purchases with an inner join, then LEFT JOIN their B purchases and keep rows where the B side is NULL. DISTINCT handles customers who bought A several times."
**Explain simply:**
- Inner join to orders filtered to product A: only customers with at least one A.
- LEFT JOIN to orders filtered to product B (filter in ON!), then `WHERE b.order_id IS NULL`: no B found.
- Vikram bought A twice, giving two rows, so use DISTINCT (or GROUP BY).
- Alternative with one pass: `GROUP BY cust_id HAVING SUM(product='A')>0 AND SUM(product='B')=0` (written with CASE for portability).
**Example:** Cross-sell targeting: employees who joined the health plan (A) but not the insurance top-up (B).
**Sample data:**

`customers`

| cust_id | name |
|---|---|
| 1 | Anita |
| 2 | Rahul |
| 3 | Sana |
| 4 | Vikram |
| 5 | Lata |

`orders`

| order_id | cust_id | product |
|---|---|---|
| 1 | 1 | A |
| 2 | 1 | B |
| 3 | 2 | A |
| 4 | 3 | B |
| 5 | 4 | A |
| 6 | 4 | A |

**SQL:** self-join (anti join) approach

```sql
SELECT DISTINCT c.name
FROM customers c
JOIN orders a ON a.cust_id = c.cust_id AND a.product = 'A'
LEFT JOIN orders b ON b.cust_id = c.cust_id AND b.product = 'B'
WHERE b.order_id IS NULL
ORDER BY c.name;
```

**Output:**

| name |
|---|
| Rahul |
| Vikram |

**pandas equivalent:** (result identical to the SQL output above)

```python
a = set(orders[orders['product'] == 'A'].cust_id)
b = set(orders[orders['product'] == 'B'].cust_id)
res = customers[customers.cust_id.isin(a - b)][['name']].sort_values('name')
```

**SQL (GROUP BY / HAVING alternative):**

```sql
SELECT c.name
FROM customers c JOIN orders o ON o.cust_id = c.cust_id
GROUP BY c.cust_id, c.name
HAVING SUM(CASE WHEN o.product = 'A' THEN 1 ELSE 0 END) > 0
   AND SUM(CASE WHEN o.product = 'B' THEN 1 ELSE 0 END) = 0
ORDER BY c.name;
```

**Output:**

| name |
|---|
| Rahul |
| Vikram |

**Edge cases:** Lata (no orders) is excluded because she has no A. Duplicates need DISTINCT. NULL product values count as neither A nor B. If B-filter is placed in WHERE instead of ON, the query returns nothing.
**Likely follow-ups:**
- Customers who bought both A and B? Inner join both sides, or HAVING with both sums > 0.
- Can I use NOT EXISTS? Yes: `WHERE NOT EXISTS (SELECT 1 FROM orders b WHERE b.cust_id = c.cust_id AND b.product = 'B')`.
**Common mistakes:** Writing `WHERE product = 'A' AND product <> 'B'` on a single row; one row can never be both, the logic must span a customer's rows.

### Q58 ⭐⭐ 🟡 How do you reconcile two tables and count how many keys are unmatched on each side (data reconciliation)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** A real analyst task: proving two systems agree, and watching for duplicates.
**Say this in the interview:** "I get the distinct keys from each table, FULL JOIN them, and classify each key as matched, only in system A, or only in system B, then count. Duplicates are removed first so the counts mean keys, not rows."
**Explain simply:**
- Reconciliation means checking that two sources hold the same set of records.
- FULL JOIN keeps matched keys and the unmatched keys from both sides; the NULL side tells you where a key is missing.
- De-duplicate first with DISTINCT: employee 3 appears twice in payroll and would otherwise inflate counts.
- Then list the unmatched keys so someone can investigate them.
**Example:** HRMS has 6 employees; October payroll has 5 distinct ids. Who is paid but not in HRMS (possible ghost employees), and who is in HRMS but unpaid (leavers, or a payroll miss)?
**Sample data:**

`hrms`

| emp_id |
|---|
| 1 |
| 2 |
| 3 |
| 4 |
| 5 |
| 6 |

`payroll`

| emp_id | month |
|---|---|
| 2 | Oct |
| 3 | Oct |
| 3 | Oct |
| 4 | Oct |
| 7 | Oct |
| 8 | Oct |

**SQL:** counts by status (FULL JOIN: PostgreSQL, SQL Server, SQLite 3.39+; MySQL see Q41)

```sql
WITH a AS (SELECT DISTINCT emp_id FROM hrms),
     b AS (SELECT DISTINCT emp_id FROM payroll)
SELECT CASE WHEN a.emp_id IS NULL THEN 'only in payroll'
            WHEN b.emp_id IS NULL THEN 'only in HRMS'
            ELSE 'matched' END AS status,
       COUNT(*) AS keys
FROM a FULL JOIN b ON a.emp_id = b.emp_id
GROUP BY 1
ORDER BY 1;
```

**Output:**

| status | keys |
|---|---|
| matched | 3 |
| only in HRMS | 3 |
| only in payroll | 2 |

**pandas equivalent:** (result identical to the SQL output above)

```python
a = hrms[['emp_id']].drop_duplicates()
b = payroll[['emp_id']].drop_duplicates()
m = a.merge(b, how='outer', indicator=True)
m['status'] = m['_merge'].astype(str).map({'both':'matched','left_only':'only in HRMS','right_only':'only in payroll'})
res = m.groupby('status', as_index=False).size().rename(columns={'size':'keys'}).sort_values('status')
```

**SQL (which keys are unmatched (works in every dialect)):**

```sql
SELECT 'only in HRMS' AS status, emp_id FROM hrms
WHERE emp_id NOT IN (SELECT emp_id FROM payroll WHERE emp_id IS NOT NULL)
UNION
SELECT 'only in payroll', emp_id FROM payroll
WHERE emp_id NOT IN (SELECT emp_id FROM hrms WHERE emp_id IS NOT NULL)
ORDER BY 1, 2;
```

**Output:**

| status | emp_id |
|---|---|
| only in HRMS | 1 |
| only in HRMS | 5 |
| only in HRMS | 6 |
| only in payroll | 7 |
| only in payroll | 8 |

**Edge cases:** NULL keys cannot match; count them separately. Compare key formats first (Q52). Matching keys does not mean matching values: also compare amounts for matched keys. `UNION` here removes the duplicate 3-style repeats; use UNION ALL if you want raw rows.
**Likely follow-ups:**
- How do I also compare values? Join on the key and filter `WHERE a.salary <> b.salary`.
- Why check row counts and key counts separately? Duplicates make rows exceed keys.
**Common mistakes:** Counting rows instead of distinct keys, or using NOT IN without guarding against NULL (one NULL makes it return nothing).

### Q59 ⭐⭐ 🟡 Write a query that joins employees with leave records and returns employees with no leave this month (HR scenario).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Anti join with a date filter in ON, and handling leave that starts or ends outside the month.
**Say this in the interview:** "I LEFT JOIN each employee to leave that overlaps the month, with the date test in the ON clause, then keep rows where the leave side is NULL. Overlap means leave starts on or before month end and ends on or after month start."
**Explain simply:**
- Anti join: LEFT JOIN then `WHERE right_key IS NULL` keeps left rows with no match.
- A leave overlaps October 2026 when `start_date <= '2026-10-31' AND end_date >= '2026-10-01'`; that also catches Asha, whose leave began in September.
- Keep the date test in ON, not WHERE, or the NULL rows are removed (Q48).
- Hard-coded dates keep the example reproducible; in practice use the current month (see edge cases).
**Example:** HR wants to remind employees who took no leave in October to plan some rest (burnout prevention).
**Sample data:**

`employees`

| emp_id | name | dept_id | manager_id | salary | join_date |
|---|---|---|---|---|---|
| 1 | Asha | 10 | NULL | 90000 | 2018-03-01 |
| 2 | Ravi | 10 | 1 | 60000 | 2019-07-15 |
| 3 | Meena | 20 | 1 | 60000 | 2017-01-10 |
| 4 | Karan | 20 | 3 | 45000 | 2020-02-01 |
| 5 | Sneha | 20 | 3 | 45000 | 2021-05-20 |
| 6 | Imran | 30 | 2 | 52000 | 2022-09-12 |
| 7 | Divya | 10 | 2 | 38000 | 2023-01-09 |

`leave_records`

| leave_id | emp_id | start_date | end_date |
|---|---|---|---|
| 1 | 1 | 2026-09-28 | 2026-10-02 |
| 2 | 2 | 2026-10-14 | 2026-10-16 |
| 3 | 3 | 2026-09-10 | 2026-09-12 |
| 4 | 4 | 2026-11-02 | 2026-11-04 |
| 5 | 7 | 2026-10-20 | 2026-10-20 |

**SQL:**

```sql
SELECT e.emp_id, e.name
FROM employees e
LEFT JOIN leave_records l
  ON l.emp_id = e.emp_id
 AND l.start_date <= '2026-10-31'
 AND l.end_date   >= '2026-10-01'
WHERE l.leave_id IS NULL
ORDER BY e.emp_id;
```

**Output:**

| emp_id | name |
|---|---|
| 3 | Meena |
| 4 | Karan |
| 5 | Sneha |
| 6 | Imran |

**pandas equivalent:** (result identical to the SQL output above)

```python
l = leave_records[(leave_records.start_date <= '2026-10-31') & (leave_records.end_date >= '2026-10-01')]
res = employees[~employees.emp_id.isin(l.emp_id)][['emp_id','name']].sort_values('emp_id')
```

**Edge cases:** Meena (leave in September) and Karan (leave in November) correctly show as no leave in October. An employee with several leave rows is simply excluded. Current month dialects (not run here): PostgreSQL `date_trunc('month', CURRENT_DATE)`; MySQL `DATE_FORMAT(CURDATE(),'%Y-%m-01')` and `LAST_DAY(CURDATE())`; SQL Server `EOMONTH(GETDATE())`. Use half-open `< next month start` if times are stored. Half-day or NULL end dates need rules.
**Likely follow-ups:**
- Same with NOT EXISTS? Yes, and it is just as safe with NULLs.
- Employees with leave this month and total days? Inner join, clip the dates to the month, then SUM.
**Common mistakes:** Checking only `start_date` inside the month, which misses leave that began last month and runs into this one.

### Q60 ⭐⭐ 🔴 Write a query to find employees who report directly or indirectly to a given manager (hierarchy using self joins or a recursive CTE).
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know recursive CTEs for hierarchies, and the limit of fixed self joins.
**Say this in the interview:** "For a known number of levels I chain self joins. For any depth I use a recursive CTE: start with the manager's direct reports, then repeatedly add the people who report to the people already found, until nobody new appears."
**Explain simply:**
- A CTE (common table expression) is a named temporary result written with `WITH`. A recursive CTE refers to itself.
- Part 1 (anchor): direct reports of manager 1 (level 1). Part 2 (recursive): join employees to the rows found so far to get the next level, `UNION ALL` them together.
- It stops by itself when a round returns no new rows.
- PostgreSQL, MySQL 8+, SQLite and DuckDB write `WITH RECURSIVE`; SQL Server and Oracle write just `WITH` (not run here).
**Example:** Asha (id 1) is the head. Ravi and Meena report to her directly; Imran and Divya report to Ravi; Karan and Sneha report to Meena. So 6 people report directly or indirectly to Asha.
**Sample data:**

`employees`

| emp_id | name | dept_id | manager_id | salary | join_date |
|---|---|---|---|---|---|
| 1 | Asha | 10 | NULL | 90000 | 2018-03-01 |
| 2 | Ravi | 10 | 1 | 60000 | 2019-07-15 |
| 3 | Meena | 20 | 1 | 60000 | 2017-01-10 |
| 4 | Karan | 20 | 3 | 45000 | 2020-02-01 |
| 5 | Sneha | 20 | 3 | 45000 | 2021-05-20 |
| 6 | Imran | 30 | 2 | 52000 | 2022-09-12 |
| 7 | Divya | 10 | 2 | 38000 | 2023-01-09 |

**SQL:** recursive CTE, any depth

```sql
WITH RECURSIVE reports(emp_id, name, manager_id, level) AS (
  SELECT emp_id, name, manager_id, 1 FROM employees WHERE manager_id = 1
  UNION ALL
  SELECT e.emp_id, e.name, e.manager_id, r.level + 1
  FROM employees e JOIN reports r ON e.manager_id = r.emp_id
)
SELECT r.level, r.name, m.name AS manager
FROM reports r JOIN employees m ON m.emp_id = r.manager_id
ORDER BY r.level, r.emp_id;
```

**Output:**

| level | name | manager |
|---|---|---|
| 1 | Ravi | Asha |
| 1 | Meena | Asha |
| 2 | Karan | Meena |
| 2 | Sneha | Meena |
| 2 | Imran | Ravi |
| 2 | Divya | Ravi |

**pandas equivalent:** (result identical to the SQL output above)

```python
lvl = 1
front = employees[employees.manager_id == 1].assign(level=lvl)
parts = [front]
while not front.empty:
    lvl += 1
    front = employees[employees.manager_id.isin(front.emp_id)].assign(level=lvl)
    parts.append(front)
r = pd.concat(parts).merge(employees[['emp_id','name']].rename(columns={'emp_id':'manager_id','name':'manager'}), on='manager_id')
res = r.sort_values(['level','emp_id'])[['level','name','manager']]
```

**SQL (fixed two levels with self joins):**

```sql
SELECT name, 'direct' AS relation FROM employees WHERE manager_id = 1
UNION ALL
SELECT e2.name, 'indirect (2 levels)'
FROM employees e1 JOIN employees e2 ON e2.manager_id = e1.emp_id
WHERE e1.manager_id = 1
ORDER BY 2, 1;
```

**Output:**

| name | relation |
|---|---|
| Meena | direct |
| Ravi | direct |
| Divya | indirect (2 levels) |
| Imran | indirect (2 levels) |
| Karan | indirect (2 levels) |
| Sneha | indirect (2 levels) |

**Edge cases:** A manager with no reports returns an empty result. Bad data with a cycle (A manages B, B manages A) loops forever: add a depth limit (`WHERE r.level < 10`) or, in PostgreSQL, the CYCLE clause. The top boss has manager_id NULL and is the root. Self joins need one extra join per level, so they only work when the depth is known.
**Likely follow-ups:**
- How to show the full chain (path)? Carry a string column `path || ' > ' || name` in the CTE.
- How to count total reports for every manager? Run the CTE from each manager, or build a closure table.
**Common mistakes:** Forgetting the anchor filter (so every employee becomes a start), forgetting `UNION ALL` between parts, or having no stop for cyclic data.

### Q61 ⭐⭐ 🔴 Given orders and returns tables, compute net sales per customer without double counting from join fan-out.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know that a one-to-many join repeats rows, and that you must collapse the many side to one row per key before joining.
**Say this in the interview:** "Join fan-out means an order with two returns becomes two rows, so its amount gets summed twice. I aggregate returns to one row per order first, then join, so the order amount is counted exactly once."
**Explain simply:**
- Fan-out: when one row on the left matches several rows on the right, the left row is copied once per match (like one employee with 2 leave records showing up twice).
- SUM over those copies adds the left-side amount again and again, so sales look bigger than real.
- Fix: pre-aggregate the many-side table (returns) to the same grain (one row per order) in a CTE or subquery, then join.
- Use LEFT JOIN so orders with no returns stay, and COALESCE (replace NULL with a value) to treat 'no return' as 0.
**Example:** Order 2 is 200 with refunds 50 and 30. Naive join counts 200 twice (400). C1's true net is 100 + 200 - 80 = 220.
**Sample data:**
`orders`

| order_id | customer_id | amount |
|---|---|---|
| 1 | C1 | 100 |
| 2 | C1 | 200 |
| 3 | C2 | 150 |
| 4 | C3 | 80 |
| 5 | C2 | 50 |

`returns` (order 2 was returned in two parts)

| return_id | order_id | refund_amount |
|---|---|---|
| 1 | 2 | 50 |
| 2 | 2 | 30 |
| 3 | 3 | 150 |

**SQL:**
```sql
WITH r AS (                      -- one row per order: collapse the returns FIRST
  SELECT order_id, SUM(refund_amount) AS refund
  FROM returns GROUP BY order_id
)
SELECT o.customer_id,
       SUM(o.amount)                      AS gross_sales,
       SUM(COALESCE(r.refund, 0))         AS refunds,
       SUM(o.amount - COALESCE(r.refund, 0)) AS net_sales
FROM orders o
LEFT JOIN r ON r.order_id = o.order_id
GROUP BY o.customer_id
ORDER BY o.customer_id;
```

Wrong version (join first, then SUM) gives this, which overstates C1's gross sales because order 2 appears twice after the join:

| customer_id | gross_sales | refunds | net_sales |
|---|---|---|---|
| C1 | 500 | 80 | 420 |
| C2 | 200 | 150 | 50 |
| C3 | 80 | 0 | 80 |

**Output:**

| customer_id | gross_sales | refunds | net_sales |
|---|---|---|---|
| C1 | 300 | 80 | 220 |
| C2 | 200 | 150 | 50 |
| C3 | 80 | 0 | 80 |

**pandas equivalent:**
```python
ret = returns.groupby('order_id', as_index=False)['refund_amount'].sum()
m = orders.merge(ret, on='order_id', how='left')
m['refund_amount'] = m['refund_amount'].fillna(0)
m['net'] = m['amount'] - m['refund_amount']
result = (m.groupby('customer_id', as_index=False)
            .agg(gross_sales=('amount','sum'), refunds=('refund_amount','sum'), net_sales=('net','sum'))
            .sort_values('customer_id'))
```

**Edge cases:** Orders with no returns give NULL refund, so use COALESCE. Refunds can exceed the amount in bad data; check for negative net. If there are no returns at all, the CTE is empty and the LEFT JOIN still works.
**Likely follow-ups:**
- How do you check it? Compare `SUM(amount)` from `orders` alone with the post-join sum; they must match.
- What if you also join order_items? Same fix: aggregate each many-side table separately, then join the summaries on order_id.
**Common mistakes:** Joining returns directly and summing `o.amount`; using INNER JOIN, which drops customers with no returns; forgetting COALESCE so the arithmetic with NULL makes net NULL.

### Q62 ⭐ 🟢 What are SEMI JOIN and ANTI JOIN? Does SQL have such keywords?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know how to filter by existence without duplicating rows, and the NOT IN with NULL trap.
**Say this in the interview:** "A semi join keeps rows from the left table that have a match on the right, but never returns right-side columns or duplicates. An anti join keeps the rows with no match. Most SQL databases have no SEMI JOIN keyword, so I write them with EXISTS and NOT EXISTS."
**Explain simply:**
- Semi join = 'employees who have at least one leave'. Anti join = 'employees who have no leave'.
- PostgreSQL, MySQL, SQL Server and SQLite have no `SEMI JOIN` / `ANTI JOIN` keyword: use EXISTS / NOT EXISTS (or IN / NOT IN, or LEFT JOIN ... IS NULL). Spark SQL and Databricks do have `LEFT SEMI JOIN` and `LEFT ANTI JOIN`; DuckDB has `SEMI JOIN` and `ANTI JOIN` (not run here for Spark).
- Unlike INNER JOIN, a semi join returns each left row at most once, even if there are many matches.
- Prefer NOT EXISTS over NOT IN: if the subquery has even one NULL, NOT IN returns nothing.
**Example:** Of 5 employees, 2 took leave (Asha twice, Chitra once). Semi gives 2 names, anti gives 3.
**Sample data:**
`employees`

| emp_id | name |
|---|---|
| 1 | Asha |
| 2 | Ben |
| 3 | Chitra |
| 4 | Dev |
| 5 | Esha |

`leaves` (Asha has two)

| leave_id | emp_id | leave_date |
|---|---|---|
| 1 | 1 | 2025-01-05 |
| 2 | 1 | 2025-02-10 |
| 3 | 3 | 2025-01-20 |

**SQL:**
```sql
SELECT 'semi: has leave' AS kind, e.name
FROM employees e
WHERE EXISTS (SELECT 1 FROM leaves l WHERE l.emp_id = e.emp_id)
UNION ALL
SELECT 'anti: no leave', e.name
FROM employees e
WHERE NOT EXISTS (SELECT 1 FROM leaves l WHERE l.emp_id = e.emp_id)
ORDER BY 1 DESC, 2;
```

**Output:**

| kind | name |
|---|---|
| semi: has leave | Asha |
| semi: has leave | Chitra |
| anti: no leave | Ben |
| anti: no leave | Dev |
| anti: no leave | Esha |

**pandas equivalent:**
```python
has = employees['emp_id'].isin(leaves['emp_id'])
semi = employees[has].assign(kind='semi: has leave')
anti = employees[~has].assign(kind='anti: no leave')
result = (pd.concat([semi, anti])[['kind','name']]
            .sort_values(['kind','name'], ascending=[False, True]))
```

Why not a plain INNER JOIN for the semi case? Asha would show twice:

| name |
|---|
| Asha |
| Asha |
| Chitra |

NULL trap: after inserting one leave row with `emp_id = NULL`, `WHERE emp_id NOT IN (SELECT emp_id FROM leaves)` returned 0 rows (real run), while NOT EXISTS still returned 3 rows (Ben, Dev, Esha).
**Edge cases:** NULL emp_id in the right table breaks NOT IN but not NOT EXISTS. Duplicate matches never duplicate semi-join output.
**Likely follow-ups:**
- Is LEFT JOIN ... IS NULL the same as NOT EXISTS? Same result; modern optimizers usually plan them alike.
- Which is faster, IN or EXISTS? Mostly equal today; check the plan.
**Common mistakes:** Using INNER JOIN and getting duplicate employees; using NOT IN against a nullable column; checking a nullable column for NULL in the LEFT JOIN version.

### Q63 ⭐ 🟢 Cheat sheet: which join would you use for (a) customers with their orders, (b) customers without orders, (c) all combinations?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you map a business need to the right join quickly.
**Say this in the interview:** "For customers with their orders I use INNER JOIN, or LEFT JOIN if I want every customer; for customers without orders, LEFT JOIN and filter where the order id is NULL (or NOT EXISTS); for all combinations, CROSS JOIN."
**Explain simply:**
- Cheat sheet: only matching rows -> INNER JOIN. Keep everything from the left -> LEFT JOIN. Keep everything from both -> FULL OUTER JOIN. Left rows with no match -> LEFT JOIN ... WHERE right.key IS NULL (or NOT EXISTS). Every pairing -> CROSS JOIN. Just 'does a match exist' -> EXISTS.
- Here 3 customers x 3 orders = 9 combinations; only 3 are real matches; Chitra has none.
- In (b), test the right table's key column for NULL, not a column that could legitimately be NULL.
**Example:** HR version: employees x leave records. Who took leave = (a); who never took leave = (b); every employee x every month grid = (c).
**Sample data:**
`customers`

| cust_id | name |
|---|---|
| 1 | Asha |
| 2 | Ben |
| 3 | Chitra |

`orders`

| order_id | cust_id | amount |
|---|---|---|
| 10 | 1 | 500 |
| 11 | 1 | 300 |
| 12 | 2 | 200 |

**SQL:**
```sql
SELECT '(a) customers with their orders - INNER JOIN' AS need, COUNT(*) AS rows_returned
FROM customers c JOIN orders o ON o.cust_id = c.cust_id
UNION ALL
SELECT '(b) customers without orders - LEFT JOIN + IS NULL', COUNT(*)
FROM customers c LEFT JOIN orders o ON o.cust_id = c.cust_id
WHERE o.order_id IS NULL
UNION ALL
SELECT '(c) all combinations - CROSS JOIN', COUNT(*)
FROM customers c CROSS JOIN orders o;
```

**Output:**

| need | rows_returned |
|---|---|
| (a) customers with their orders - INNER JOIN | 3 |
| (b) customers without orders - LEFT JOIN + IS NULL | 1 |
| (c) all combinations - CROSS JOIN | 9 |

**pandas equivalent:**
```python
a = customers.merge(orders, on='cust_id', how='inner')
b = customers.merge(orders, on='cust_id', how='left', indicator=True).query("_merge == 'left_only'")
c = customers.merge(orders, how='cross')
result = pd.DataFrame({'need': ['(a) customers with their orders - INNER JOIN',
                                 '(b) customers without orders - LEFT JOIN + IS NULL',
                                 '(c) all combinations - CROSS JOIN'],
                       'rows_returned': [len(a), len(b), len(c)]})
```

**Edge cases:** A LEFT JOIN with a WHERE filter on a right-table column silently turns into an INNER JOIN. Duplicates in orders repeat the customer. MySQL has no FULL OUTER JOIN.
**Likely follow-ups:**
- Which join for 'orders with no customer'? LEFT JOIN from orders, IS NULL on the customer key.
- How do you emulate FULL JOIN in MySQL? LEFT JOIN UNION RIGHT JOIN.
**Common mistakes:** Testing `o.amount IS NULL` when amount can be NULL anyway; creating a CROSS JOIN by accident (comma join with no condition).

### Q64 ⭐ 🟢 What happens to the output if both tables have columns with the same name? How do you rename them?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know SELECT * hides name clashes, and that you fix it with table aliases and column aliases.
**Say this in the interview:** "Both columns come back with the same name, which is confusing and breaks views and downstream tools. I qualify each column with its table alias and rename with AS, for example e.name AS emp_name and d.name AS dept_name."
**Explain simply:**
- The engine usually returns both columns with the same name. Creating a view or CREATE TABLE AS from such a result gives an error in most databases.
- Table alias (`e`, `d`): a short nickname that tells SQL which table's column you mean. Without it, `name` alone gives an 'ambiguous column' error.
- Column alias (`AS emp_name`) renames the output column.
- With `USING (id)` the join key appears once. In pandas, `merge` adds `_x` / `_y` suffixes, which you control with `suffixes=`.
**Example:** Employees and departments both have `id` and `name`; after aliasing you read emp_name = Asha, dept_name = HR, not two columns called name.
**Sample data:**
`employees`

| id | name | dept_id |
|---|---|---|
| 1 | Asha | 10 |
| 2 | Ben | 20 |
| 3 | Chitra | 10 |

`departments`

| id | name |
|---|---|
| 10 | HR |
| 20 | Finance |

**SQL:**
```sql
SELECT e.id   AS emp_id,
       e.name AS emp_name,
       d.id   AS dept_id,
       d.name AS dept_name
FROM employees e
JOIN departments d ON d.id = e.dept_id
ORDER BY e.id;
```

Column names returned by `SELECT *` on the same join: `['id', 'name', 'dept_id', 'id', 'name']` (id and name repeat).
**Output:**

| emp_id | emp_name | dept_id | dept_name |
|---|---|---|---|
| 1 | Asha | 10 | HR |
| 2 | Ben | 20 | Finance |
| 3 | Chitra | 10 | HR |

**pandas equivalent:**
```python
emp = employees.rename(columns={'id':'emp_id','name':'emp_name'})
dept = departments.rename(columns={'id':'dept_id','name':'dept_name'})   # rename BEFORE merging
result = emp.merge(dept, on='dept_id')[['emp_id','emp_name','dept_id','dept_name']].sort_values('emp_id')
```

**Edge cases:** Python or BI tools may keep only one of two same-named columns (for example a dictionary fetch silently loses one). NULL keys are unaffected.
**Likely follow-ups:**
- Can you SELECT d.* only? Yes, but still alias if names clash.
- What does the ambiguity error look like? 'ambiguous column name: name' in SQLite; 'column reference "name" is ambiguous' in PostgreSQL.
**Common mistakes:** Using SELECT * in production queries and views; forgetting aliases and hitting the ambiguity error; assuming the second column overwrites the first.

### Q65 ⭐ 🟡 What are join algorithms (nested loop, hash join, merge join)? Explain simply and how indexes help joins.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you explain, in simple words, how the database physically matches rows, and why an index helps.
**Say this in the interview:** "There are three main ways. Nested loop: for each row on one side, look for matches on the other. Hash join: build a lookup table in memory from the smaller table and probe it. Merge join: sort both sides and walk them together. An index turns the 'look for matches' step into a quick lookup instead of a full scan."
**Explain simply:**
- Nested loop: like checking each employee's department by flipping through the whole department list. Fine for tiny tables, and very fast when the inner side has an index.
- Hash join: like writing the department list on a board keyed by id, then looking each employee up on it. Good for big, unsorted tables joined on equality. Needs memory.
- Merge join: both lists already sorted by dept id, so you walk them side by side once. Good when data is already sorted or indexed.
- You do not choose the algorithm; the optimizer (the part of the database that plans the query) does, using table sizes and statistics. SQLite only does nested loops; PostgreSQL, SQL Server, MySQL 8 and DuckDB also use hash joins; PostgreSQL and SQL Server use merge joins (not run here).
- An index on the join column lets the inner side of a nested loop do a SEARCH (seek) instead of a SCAN (read everything).
**Example:** 40 employees x 3 departments: without an index, for each department the engine reads all 40 employees (up to 120 comparisons). With an index on employees.dept_id it jumps straight to that department's employees. For 1 million x 10,000 rows the gap is huge.
**SQL (small runnable demo, SQLite 3.49, `PRAGMA automatic_index=OFF`):**
```sql
EXPLAIN QUERY PLAN
SELECT e.name, d.dept_name FROM employees e JOIN departments d ON d.dept_id = e.dept_id;
-- then: CREATE INDEX ix_emp_dept ON employees(dept_id);  and EXPLAIN again
```

**Output (real plan lines):**
Before the index:
```
SCAN e
SCAN d
```
After `CREATE INDEX ix_emp_dept ON employees(dept_id)`:
```
SCAN d
SEARCH e USING INDEX ix_emp_dept (dept_id=?)
```
**Edge cases:** NULL join keys never match, so every algorithm skips them. Heavily skewed keys (one department with most employees) can hurt hash joins. Not run here: PostgreSQL EXPLAIN that shows `Hash Join` / `Merge Join` nodes.
**Likely follow-ups:**
- How do you see which algorithm is used? EXPLAIN (PostgreSQL, MySQL) or the execution plan (SQL Server).
- Does an index always help? Not when you read most of the table; a hash join or full scan can win.
**Common mistakes:** Thinking you write the algorithm yourself; believing an index is always used; indexing every column, which slows inserts.

### Q66 ⭐ 🟡 Why is a join slow on large tables? How would you speed it up (indexes, filter early, select only needed columns)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you diagnose slow joins systematically instead of guessing.
**Say this in the interview:** "A join is slow when the engine has to compare too many rows. I first look at the execution plan, then make sure join columns are indexed with matching data types, filter early, select only the columns I need, and join pre-aggregated data instead of raw rows."
**Explain simply:**
- Why slow: with no index the engine may scan all rows of one table for every row of the other.
- Index the join keys (and foreign keys). Make the types match (int to int, not int to text), otherwise the index cannot be used.
- Filter early: push WHERE conditions down, or pre-filter in a CTE (a named temporary result), so fewer rows enter the join.
- Select only needed columns, not SELECT *: less data to move and sort.
- Avoid row explosion: aggregate the many-side before joining, and avoid functions on join columns (see Q70).
**Example:** Joining 5 million attendance rows to 50,000 employees to report one department: index `dept_id`, filter that department first, and return only name and days present.
**SQL (tuned version, plus the plan before and after indexing; SQLite):**
```sql
SELECT e.name, d.dept_name FROM employees e JOIN departments d ON d.dept_id = e.dept_id WHERE e.dept_id = 10;
-- Fixes used:
-- 1) CREATE INDEX ix_emp_dept ON employees(dept_id);  CREATE INDEX ix_dept_id ON departments(dept_id);
-- 2) filter (WHERE) as early as possible
-- 3) SELECT only e.name, d.dept_name, not SELECT *
```

**Output (real plan lines):**
Before indexes:
```
SCAN e
SCAN d
```
After indexes:
```
SEARCH d USING INDEX ix_dept_id (dept_id=?)
SEARCH e USING INDEX ix_emp_dept (dept_id=?)
```
**Edge cases:** NULL keys drop out of equality joins. Duplicate keys make the join result larger than either table. Not run here: PostgreSQL `EXPLAIN ANALYZE` and SQL Server actual-plan output, which show real timings.
**Likely follow-ups:**
- How do you know what to fix? Read the plan for scans on big tables, wrong row-count estimates and sorts.
- Is more indexing always better? No; each index slows inserts and updates and uses space.
**Common mistakes:** Adding indexes without reading the plan; leaving type mismatches; selecting every column; joining before filtering on a huge table.

### Q67 ⭐ 🟡 What is a LATERAL / CROSS APPLY join? When is it useful?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the 'for each row, run a small query' pattern and its dialect names.
**Say this in the interview:** "A LATERAL join lets the subquery on the right refer to columns from the table on its left, so it runs once per left row. It is great for 'top N per group'. SQL Server calls it CROSS APPLY or OUTER APPLY."
**Explain simply:**
- Normally a subquery in FROM cannot see the other tables in the same FROM. LATERAL removes that rule (PostgreSQL, MySQL 8.0.14+, DuckDB, Oracle 12c+). SQLite has no LATERAL.
- Think of it as a loop: for each department, run 'top 2 salaries in this department'.
- CROSS APPLY is like INNER JOIN LATERAL (drops left rows with no result); OUTER APPLY is like LEFT JOIN LATERAL ... ON TRUE (keeps them with NULLs).
- Useful for top-N per group, latest record per employee, and calling a set-returning function per row. A window function with ROW_NUMBER often does the same job.
**Example:** HR: show the two highest-paid employees in each department; Legal has nobody, so LEFT keeps it with NULLs.
**Sample data:**
`departments`

| dept_id | dept_name |
|---|---|
| 10 | HR |
| 20 | Finance |
| 30 | Legal |

`employees`

| emp_id | emp_name | dept_id | salary |
|---|---|---|---|
| 1 | Asha | 10 | 60000 |
| 2 | Ben | 10 | 75000 |
| 3 | Chitra | 10 | 52000 |
| 4 | Dev | 20 | 90000 |
| 5 | Esha | 20 | 81000 |

**SQL (PostgreSQL / DuckDB / MySQL 8.0.14+ syntax; run here in DuckDB 1.5):**
```sql
SELECT d.dept_name, t.emp_name, t.salary
FROM departments d
LEFT JOIN LATERAL (
    SELECT e.emp_name, e.salary
    FROM employees e
    WHERE e.dept_id = d.dept_id        -- can refer to d, the table on its left
    ORDER BY e.salary DESC
    LIMIT 2                            -- top 2 PER department
) t ON TRUE
ORDER BY d.dept_name, t.salary DESC;
```

SQL Server / Oracle equivalent (not run here): `FROM departments d OUTER APPLY (SELECT TOP 2 e.emp_name, e.salary FROM employees e WHERE e.dept_id = d.dept_id ORDER BY e.salary DESC) t` (use `CROSS APPLY` to drop departments with no rows).
**Output:**

| dept_name | emp_name | salary |
|---|---|---|
| Finance | Dev | 90000 |
| Finance | Esha | 81000 |
| HR | Ben | 75000 |
| HR | Asha | 60000 |
| Legal | NULL | NULL |

**pandas equivalent:**
```python
top2 = employees.sort_values(['dept_id','salary'], ascending=[True, False]).groupby('dept_id').head(2)
result = (departments.merge(top2, on='dept_id', how='left')[['dept_name','emp_name','salary']]
            .sort_values(['dept_name','salary'], ascending=[True, False]))
```

**Edge cases:** Ties at the cut-off: LIMIT 2 picks arbitrarily; add a tiebreaker in ORDER BY. NULL salaries sort first or last depending on the database. Empty groups need LEFT ... ON TRUE (or OUTER APPLY).
**Likely follow-ups:**
- LATERAL vs window function? Window is usually simpler for top-N; LATERAL shines when the inner query needs LIMIT, an index seek or a function call per row.
- Does SQLite have it? No; use ROW_NUMBER() OVER (PARTITION BY ...).
**Common mistakes:** Forgetting `ON TRUE` after LEFT JOIN LATERAL; expecting it to work in SQLite; using CROSS APPLY and losing empty groups.

### Q68 ⭐ 🟡 Use a CROSS JOIN to generate all combinations (e.g., every employee x every month), then LEFT JOIN actuals to fill zeros.
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you build a complete grid so missing combinations show as 0 instead of disappearing.
**Say this in the interview:** "I first CROSS JOIN employees with a list of months to create every combination, then LEFT JOIN the actual leave data onto that grid, and use COALESCE to turn missing values into 0."
**Explain simply:**
- CROSS JOIN = every row of table A paired with every row of table B (3 employees x 3 months = 9 rows). No ON condition.
- The leave table only stores months where something happened, so a plain GROUP BY would silently skip zero-leave months.
- LEFT JOIN keeps all 9 grid rows; COALESCE(x, 0) replaces NULL with 0.
- Put BOTH matching conditions (employee and month) in the ON clause of the LEFT JOIN. A WHERE filter on `l` would delete the zero rows.
**Example:** Attendance dashboard: Ben took no leave at all, yet the report must still show Ben with 0 days in Jan, Feb and Mar.
**Sample data:**
`employees`

| emp_id | name |
|---|---|
| 1 | Asha |
| 2 | Ben |
| 3 | Chitra |

`leave_taken` (only months with leave are stored)

| emp_id | month | days |
|---|---|---|
| 1 | 2025-01 | 2 |
| 1 | 2025-03 | 1 |
| 3 | 2025-02 | 4 |

**SQL:**
```sql
WITH months(month) AS (VALUES ('2025-01'), ('2025-02'), ('2025-03'))
SELECT e.name, m.month, COALESCE(l.days, 0) AS leave_days
FROM employees e
CROSS JOIN months m                          -- every employee x every month (9 rows)
LEFT JOIN leave_taken l
       ON l.emp_id = e.emp_id AND l.month = m.month
ORDER BY e.name, m.month;
```

**Output:**

| name | month | leave_days |
|---|---|---|
| Asha | 2025-01 | 2 |
| Asha | 2025-02 | 0 |
| Asha | 2025-03 | 1 |
| Ben | 2025-01 | 0 |
| Ben | 2025-02 | 0 |
| Ben | 2025-03 | 0 |
| Chitra | 2025-01 | 0 |
| Chitra | 2025-02 | 4 |
| Chitra | 2025-03 | 0 |

**pandas equivalent:**
```python
months = pd.DataFrame({'month': ['2025-01','2025-02','2025-03']})
grid = employees.merge(months, how='cross')
m = grid.merge(leave_taken, on=['emp_id','month'], how='left')
m['leave_days'] = m['days'].fillna(0)
result = m[['name','month','leave_days']].sort_values(['name','month'])
```

**Edge cases:** If leave_taken has several rows per employee-month, the join repeats the grid row and SUMs would double count; aggregate to one row per employee-month first. Output size = employees x months, which can get big.
**Likely follow-ups:**
- How do you get the month list? From a VALUES list, a calendar table, or a recursive CTE (Q69).
- What if you have thousands of employees and 12 months? 12,000 grid rows is fine; watch out for a day-level grid.
**Common mistakes:** Putting the month condition in WHERE (turns the LEFT JOIN into an INNER JOIN); forgetting COALESCE; building the grid from the fact table itself, which can only contain existing combinations.

### Q69 ⭐ 🟡 How do you build a date spine (all dates, even with no sales) and show 0 for missing days?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you fill gaps in time series so charts and averages are not misleading.
**Say this in the interview:** "I generate every date in the range with a recursive CTE, a calendar table or generate_series, then LEFT JOIN the sales onto it and use COALESCE to show 0 for days with no sales."
**Explain simply:**
- A date spine is a list with one row for every date in a range, even dates with no data.
- Sales tables only contain days that had a sale. If you group by order_date you never see the empty days.
- Recursive CTE (a query that calls itself): start from the first date, keep adding 1 day until the last date.
- LEFT JOIN the spine to the sales, then COALESCE(SUM(amount), 0). Put any filter on the sales table in the ON clause, not WHERE.
**Example:** Daily headcount of employees present: a holiday with no rows should show 0, not vanish from the chart. Here 3, 4 and 6 March show 0 revenue.
**Sample data:**
`orders` (no sales on 3, 4 and 6 March)

| order_id | order_date | amount |
|---|---|---|
| 1 | 2025-03-01 | 500 |
| 2 | 2025-03-01 | 300 |
| 3 | 2025-03-02 | 200 |
| 4 | 2025-03-05 | 700 |
| 5 | 2025-03-07 | 150 |

**SQL (SQLite; recursive CTE builds the dates):**
```sql
WITH RECURSIVE spine(d) AS (
    SELECT '2025-03-01'                              -- first day
    UNION ALL
    SELECT date(d, '+1 day') FROM spine
    WHERE d < '2025-03-07'                           -- last day
)
SELECT s.d AS sale_date, COALESCE(SUM(o.amount), 0) AS revenue
FROM spine s
LEFT JOIN orders o ON o.order_date = s.d
GROUP BY s.d
ORDER BY s.d;
```

Other dialects (not run here): PostgreSQL `generate_series('2025-03-01'::date, '2025-03-07', interval '1 day')`; DuckDB `range(DATE '2025-03-01', DATE '2025-03-08', INTERVAL 1 DAY)`; SQL Server and MySQL 8 use the same recursive CTE with `DATEADD(day,1,d)` / `DATE_ADD(d, INTERVAL 1 DAY)`. Many warehouses keep a permanent `calendar` table instead.
**Output:**

| sale_date | revenue |
|---|---|
| 2025-03-01 | 800 |
| 2025-03-02 | 200 |
| 2025-03-03 | 0 |
| 2025-03-04 | 0 |
| 2025-03-05 | 700 |
| 2025-03-06 | 0 |
| 2025-03-07 | 150 |

**pandas equivalent:**
```python
spine = pd.DataFrame({'sale_date': pd.date_range('2025-03-01', '2025-03-07').strftime('%Y-%m-%d')})
daily = orders.groupby('order_date', as_index=False)['amount'].sum().rename(columns={'order_date':'sale_date'})
result = spine.merge(daily, on='sale_date', how='left').fillna({'amount': 0}).rename(columns={'amount':'revenue'})
```

**Edge cases:** If order_date has a time part, convert to date first (`DATE(order_ts)`) or nothing will match. Duplicate dates in the spine would double count. Average per day changes a lot once zero days are included (7 days, not 4).
**Likely follow-ups:**
- How do you handle a very long range? Use a permanent calendar table with an index.
- What if the range comes from the data? Use `SELECT MIN(order_date), MAX(order_date)` as the CTE bounds.
**Common mistakes:** Grouping only the sales table; joining on a timestamp instead of a date; using INNER JOIN; forgetting the recursion stop condition (infinite loop).

### Q70 ⭐ 🟡 Why can joining on a function-wrapped column (e.g., ON LOWER(a.email)=LOWER(b.email)) be slow?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand that indexes are built on raw column values, so wrapping the column in a function stops them being used (non-sargable).
**Say this in the interview:** "An index is sorted on the stored value, for example 'User1@Corp.com'. If I join on LOWER(email), the database cannot use that sorted order, so it has to compute LOWER for every row and scan. I fix it by cleaning the data once, using a computed or functional index, or standardising case at load time."
**Explain simply:**
- Index = a sorted lookup list on a column's real values. 'user1@corp.com' sits in a different place from 'User1@Corp.com'.
- With LOWER(col) the database must apply the function to every row before comparing, so the index on col is skipped: a full scan, often with a hash join or temporary index on top.
- Sargable means 'can use an index seek'; function-wrapped columns are non-sargable.
- Fixes: clean data on load (store lowercase), add a computed/generated column and index it, or create an expression index on LOWER(email). Some databases use case-insensitive collations (SQL Server default, MySQL), so LOWER is not even needed.
**Example:** Matching 500,000 HR emails to 500,000 payroll emails with LOWER() on both sides means 1,000,000 function calls and no index seek; storing a lowercase column makes it a fast lookup.
**SQL (SQLite; plans from EXPLAIN QUERY PLAN):**
```sql
-- slow pattern: function on both join columns
SELECT h.emp_id FROM hr_emp h JOIN payroll p ON LOWER(h.email) = LOWER(p.email);
-- fix 1: store a cleaned column (email_lower) once, index it, join on it
-- fix 2: expression index (SQLite, PostgreSQL, Oracle; SQL Server uses a computed column):
CREATE INDEX ix_pay_lower ON payroll(LOWER(email));
```

**Output (real plan lines; 200 rows each side, automatic temporary indexes turned off):**
Plain `ON h.email = p.email` (indexes usable):
```
SCAN h
SEARCH p USING COVERING INDEX ix_pay_email (email=?)
```
`ON LOWER(h.email) = LOWER(p.email)` (index on raw email can only be scanned, not searched):
```
SCAN h
SCAN p USING COVERING INDEX ix_pay_email
```
Same query after `CREATE INDEX ix_pay_lower ON payroll(LOWER(email))`:
```
SCAN h
SEARCH p USING COVERING INDEX ix_pay_lower (<expr>=?)
```
The function-wrapped join matches 200 of 200 rows here (the emails differ only in case).
**Edge cases:** NULL emails never match either way. Trailing spaces also break matches, so TRIM at load time too. Duplicate emails after lower-casing (User1@ and user1@) will create duplicate matches.
**Likely follow-ups:**
- Same problem in WHERE? Yes: `WHERE YEAR(order_date) = 2025` is non-sargable; use `order_date >= '2025-01-01' AND order_date < '2026-01-01'`.
- Not run here: SQL Server computed column and PostgreSQL EXPLAIN.
**Common mistakes:** Wrapping join or filter columns in functions out of habit; assuming the index will still be used; cleaning data in every query instead of once at load.

### Q71 ⭐ 🟡 How do you join a table to itself multiple times (employee, manager, manager's manager)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you use the same table twice under different aliases, and do you pick LEFT JOIN so the top of the chain is kept.
**Say this in the interview:** "I join the employees table to itself, giving it a different alias each time: e for the employee, m for the manager, g for the manager's manager. I use LEFT JOIN so people with no manager, like the CEO, are not dropped."
**Explain simply:**
- A self join is just a normal join where both sides are the same table. Aliases (`e`, `m`, `g`) are mandatory so SQL knows which copy you mean.
- Each extra level of the chain needs one more self join: manager = 1, manager's manager = 2.
- LEFT JOIN, because the CEO has NULL manager and level-2 people have no grand-manager.
- For an unknown depth of levels, use a recursive CTE instead (see Q60).
**Example:** Org chart with 6 people: Chitra reports to Asha, Asha to Ravi, so Chitra's manager's manager is Ravi.
**Sample data:**
`employees` (manager_id points to another row's emp_id)

| emp_id | name | manager_id |
|---|---|---|
| 1 | Meera (CEO) | NULL |
| 2 | Ravi | 1 |
| 3 | Asha | 2 |
| 4 | Ben | 2 |
| 5 | Chitra | 3 |
| 6 | Dev | 3 |

**SQL:**
```sql
SELECT e.name        AS employee,
       m.name        AS manager,
       g.name        AS managers_manager
FROM employees e
LEFT JOIN employees m ON m.emp_id = e.manager_id    -- 1st self join: manager
LEFT JOIN employees g ON g.emp_id = m.manager_id    -- 2nd self join: manager's manager
ORDER BY e.emp_id;
```

**Output:**

| employee | manager | managers_manager |
|---|---|---|
| Meera (CEO) | NULL | NULL |
| Ravi | Meera (CEO) | NULL |
| Asha | Ravi | Meera (CEO) |
| Ben | Ravi | Meera (CEO) |
| Chitra | Asha | Ravi |
| Dev | Asha | Ravi |

**pandas equivalent:**
```python
m = employees.rename(columns={'emp_id':'m_id','name':'manager','manager_id':'m_mgr'})
g = employees.rename(columns={'emp_id':'g_id','name':'managers_manager'})[['g_id','managers_manager']]
r = employees.merge(m[['m_id','manager','m_mgr']], left_on='manager_id', right_on='m_id', how='left')
r = r.merge(g, left_on='m_mgr', right_on='g_id', how='left')
result = r.rename(columns={'name':'employee'})[['employee','manager','managers_manager']]
```

**Edge cases:** NULL manager_id (CEO): no match, LEFT JOIN returns NULL. A cycle (A manages B, B manages A) can loop forever in a recursive version. Duplicate emp_id would duplicate rows.
**Likely follow-ups:**
- How many levels? One join per level; recursive CTE if unlimited.
- How do you find employees earning more than their manager? Join e to m and compare `e.salary > m.salary`.
**Common mistakes:** Forgetting aliases (ambiguous column); using INNER JOIN and losing the CEO; joining on the wrong direction (`m.manager_id = e.emp_id` gives the reports, not the manager).

### Q72 ⭐ 🔴 How do you find the top 3 products per category using joins only (no window functions)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you think in 'count how many are better than me' terms, a classic pre-window-function trick.
**Say this in the interview:** "I self-join the table to itself on the same category and count how many products have higher revenue. If fewer than 3 products beat a product, it is in the top 3. Window functions with ROW_NUMBER are simpler, but this works in any database."
**Explain simply:**
- For each product, `better` = other products in the same category with higher revenue. COUNT of those is the product's rank minus 1.
- LEFT JOIN keeps the best product, which has zero better products. With INNER JOIN it would vanish.
- HAVING (a filter applied after grouping) keeps those with fewer than 3 better products.
- Ties: this behaves like RANK, so tied products at the boundary are all kept. Here Phones returns 4 rows because P2, P3 and P4 tie at 700, and each is beaten by only one product.
- To force exactly 3 rows, add a tiebreaker to the join: `better.revenue > p.revenue OR (better.revenue = p.revenue AND better.product_id < p.product_id)`.
**Example:** Top 3 selling products per category for the catalog page; Laptops has only 3 products so all appear; Phones shows 4 because of the three-way tie.
**Sample data:**
`products` (P2, P3 and P4 tie at 700)

| product_id | category | product_name | revenue |
|---|---|---|---|
| 1 | Phones | P1 | 900 |
| 2 | Phones | P2 | 700 |
| 3 | Phones | P3 | 700 |
| 4 | Phones | P4 | 700 |
| 5 | Phones | P5 | 300 |
| 6 | Laptops | L1 | 1200 |
| 7 | Laptops | L2 | 800 |
| 8 | Laptops | L3 | 100 |

**SQL (self join, no window functions):**
```sql
SELECT p.category, p.product_name, p.revenue
FROM products p
LEFT JOIN products better                      -- products in the same category that earn MORE
       ON better.category = p.category
      AND better.revenue  > p.revenue
GROUP BY p.product_id, p.category, p.product_name, p.revenue
HAVING COUNT(better.product_id) < 3           -- fewer than 3 products beat me => I'm in the top 3
ORDER BY p.category, p.revenue DESC, p.product_name;
```

**Output:**

| category | product_name | revenue |
|---|---|---|
| Laptops | L1 | 1200 |
| Laptops | L2 | 800 |
| Laptops | L3 | 100 |
| Phones | P1 | 900 |
| Phones | P2 | 700 |
| Phones | P3 | 700 |
| Phones | P4 | 700 |

**pandas equivalent:**
```python
r = products.copy()
r['beaten_by'] = r.groupby('category')['revenue'].rank(method='min', ascending=False) - 1
result = (r[r['beaten_by'] < 3][['category','product_name','revenue']]
            .sort_values(['category','revenue','product_name'], ascending=[True, False, True]))
```

**Edge cases:** Ties (see above) can return more than 3 rows per category. Categories with fewer than 3 products return all. NULL revenue: the comparison is unknown, so NULL-revenue products never count as 'better' and may sneak in; filter them out first. Slow on huge tables (quadratic per category).
**Likely follow-ups:**
- Window version? `ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC)` then `WHERE rn <= 3`; use RANK or DENSE_RANK to treat ties.
- Correlated subquery version? `WHERE (SELECT COUNT(*) FROM products b WHERE b.category=p.category AND b.revenue>p.revenue) < 3`.
**Common mistakes:** Using INNER JOIN so the top product disappears; using `>=` and counting yourself; forgetting GROUP BY on all non-aggregated columns; not noticing tie behaviour.

### Q73 ⭐ 🔴 How would you reconcile source vs warehouse tables to find missing, extra and mismatched rows using FULL OUTER JOIN?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you do a data-quality reconciliation and compare values safely when NULLs are present.
**Say this in the interview:** "I FULL OUTER JOIN source and warehouse on the business key, so rows from either side survive. Then I classify: warehouse key NULL means missing, source key NULL means extra, both present but any column different means mismatch. For the comparison I use a NULL-safe operator, because a plain <> returns unknown when either value is NULL."
**Explain simply:**
- FULL OUTER JOIN keeps every row from both tables; unmatched columns come back NULL.
- Missing = in source but not in warehouse (warehouse key IS NULL). Extra = in warehouse but not in source (source key IS NULL).
- Mismatch = key in both but a column differs. `s.salary <> w.salary` is unknown (not true) when one side is NULL, so Dev's NULL vs 40000 would be missed. Use `IS NOT` / `IS DISTINCT FROM` / `<=>`.
- Use COALESCE(s.key, w.key) to show one key column.
- Also compare row counts and totals first; they tell you quickly whether to dig.
**Example:** Payroll source has 5 employees, the warehouse 5: Chitra is missing, Farah is extra, Ben's salary differs (60,000 vs 62,000), Dev's NULL vs 40,000 differs, and Esha is spelled Isha.
**Sample data:**
`src_emp` (source system)

| emp_id | name | salary |
|---|---|---|
| 1 | Asha | 50000 |
| 2 | Ben | 60000 |
| 3 | Chitra | 55000 |
| 4 | Dev | NULL |
| 5 | Esha | 70000 |

`dw_emp` (warehouse copy)

| emp_id | name | salary |
|---|---|---|
| 1 | Asha | 50000 |
| 2 | Ben | 62000 |
| 4 | Dev | 40000 |
| 5 | Isha | 70000 |
| 6 | Farah | 45000 |

**SQL (SQLite 3.39+, PostgreSQL, DuckDB, SQL Server; MySQL has no FULL JOIN):**
```sql
SELECT COALESCE(s.emp_id, w.emp_id) AS emp_id,
       CASE WHEN w.emp_id IS NULL THEN 'missing in warehouse'
            WHEN s.emp_id IS NULL THEN 'extra in warehouse'
            ELSE 'mismatch' END        AS status,
       s.name AS src_name, w.name AS dw_name,
       s.salary AS src_salary, w.salary AS dw_salary
FROM src_emp s
FULL OUTER JOIN dw_emp w ON w.emp_id = s.emp_id
WHERE w.emp_id IS NULL                      -- only in source
   OR s.emp_id IS NULL                      -- only in warehouse
   OR s.name   IS NOT w.name                -- NULL-safe "different" (SQLite / standard: IS DISTINCT FROM)
   OR s.salary IS NOT w.salary
ORDER BY 1;
```

Other dialects (not run here): PostgreSQL `s.salary IS DISTINCT FROM w.salary`; MySQL `NOT (s.salary <=> w.salary)` and FULL JOIN emulated with LEFT JOIN UNION RIGHT JOIN; SQL Server `IS DISTINCT FROM` from 2022, older versions need `(a <> b OR (a IS NULL AND b IS NOT NULL) OR (a IS NOT NULL AND b IS NULL))`.
**Output:**

| emp_id | status | src_name | dw_name | src_salary | dw_salary |
|---|---|---|---|---|---|
| 2 | mismatch | Ben | Ben | 60000 | 62000 |
| 3 | missing in warehouse | Chitra | NULL | 55000 | NULL |
| 4 | mismatch | Dev | Dev | NULL | 40000 |
| 5 | mismatch | Esha | Isha | 70000 | 70000 |
| 6 | extra in warehouse | NULL | Farah | NULL | 45000 |

**pandas equivalent:**
```python
m = src_emp.merge(dw_emp, on='emp_id', how='outer', suffixes=('_src','_dw'), indicator=True)
def differs(a, b):
    return ~((a == b) | (a.isna() & b.isna()))          # NULL-safe comparison
bad = (m['_merge'] != 'both') | differs(m['name_src'], m['name_dw']) | differs(m['salary_src'], m['salary_dw'])
m['status'] = m['_merge'].map({'left_only': 'missing in warehouse', 'right_only': 'extra in warehouse', 'both': 'mismatch'})
result = (m[bad].rename(columns={'name_src':'src_name','name_dw':'dw_name','salary_src':'src_salary','salary_dw':'dw_salary'})
            [['emp_id','status','src_name','dw_name','src_salary','dw_salary']].sort_values('emp_id'))
```

**Edge cases:** Duplicate keys on either side produce duplicate comparison rows; check for key uniqueness first. Trailing spaces and case differences can create false mismatches. Float columns need a tolerance, not equality.
**Likely follow-ups:**
- How would you do it without FULL JOIN? LEFT JOIN and RIGHT JOIN with UNION, or two NOT EXISTS queries plus a join for mismatches.
- Large tables? Compare a hash/checksum per row first, then drill into the differing keys.
**Common mistakes:** Using `<>` and missing NULL differences; INNER JOIN, which hides missing and extra rows; filtering with WHERE on one side's column that hides the other side's rows.

### Q74 ⭐ 🔴 How would you detect and fix join fan-out when report revenue is higher than the finance team's figure?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Can you debug a numbers-do-not-match problem methodically, finding the grain mismatch and fixing it.
**Say this in the interview:** "First I reconcile: compare the row count after the join with the count of distinct keys, and the report total with the source total. If rows go up, it is fan-out: the left table's amount repeats for each matching row on the right. I fix it by aggregating the many-side to one row per key before joining, or by summing at the right grain."
**Explain simply:**
- Grain = what one row represents (one order, one item). A join between different grains repeats the coarser one.
- Symptoms: row count after join > rows in the main table; totals higher than finance; `COUNT(*)` far above `COUNT(DISTINCT key)`.
- Find the culprit join: check each join's key for duplicates with `GROUP BY key HAVING COUNT(*) > 1`.
- Fixes: pre-aggregate the many-side in a CTE; or move the sum to a separate query per table and join the results; or use EXISTS if you only need a yes/no; or `SUM(DISTINCT ...)` only as a last resort (it wrongly collapses equal amounts).
**Example:** Finance says 1,000; the dashboard says 1,500 after joining order items. Order 2 (200) has 3 items, so it was counted 600.
**Sample data:**
`orders`

| order_id | customer_id | amount |
|---|---|---|
| 1 | C1 | 100 |
| 2 | C1 | 200 |
| 3 | C2 | 300 |
| 4 | C3 | 400 |

`order_items` (many rows per order)

| item_id | order_id | sku |
|---|---|---|
| 1 | 1 | A |
| 2 | 1 | B |
| 3 | 2 | A |
| 4 | 2 | C |
| 5 | 2 | D |
| 6 | 3 | B |
| 7 | 4 | A |

**SQL (step 1: detect the fan-out):**
```sql
SELECT COUNT(*)                          AS rows_after_join,
       COUNT(DISTINCT o.order_id)        AS distinct_orders,
       SUM(o.amount)                     AS report_revenue,
       (SELECT SUM(amount) FROM orders)  AS finance_revenue
FROM orders o
JOIN order_items i ON i.order_id = o.order_id;
```

**Output (step 1):**

| rows_after_join | distinct_orders | report_revenue | finance_revenue |
|---|---|---|---|
| 7 | 4 | 1500 | 1000 |

Reading it: 7 rows after the join but only 4 distinct orders, and report revenue (1,500) beats finance (1,000). Orders 1, 2 are repeated 2 and 3 times.
**SQL (step 2: fix by aggregating the many-side first):**
```sql
WITH items AS (                        -- bring the many-side to one row per order
  SELECT order_id, COUNT(*) AS item_count
  FROM order_items GROUP BY order_id
)
SELECT o.customer_id,
       SUM(o.amount)     AS revenue,
       SUM(i.item_count) AS items_sold
FROM orders o
LEFT JOIN items i ON i.order_id = o.order_id
GROUP BY o.customer_id
ORDER BY o.customer_id;
```

**Output (step 2):**

| customer_id | revenue | items_sold |
|---|---|---|
| C1 | 300 | 5 |
| C2 | 300 | 1 |
| C3 | 400 | 1 |

**pandas equivalent (step 2):**
```python
items = order_items.groupby('order_id', as_index=False).agg(item_count=('item_id','count'))
m = orders.merge(items, on='order_id', how='left')
result = (m.groupby('customer_id', as_index=False)
            .agg(revenue=('amount','sum'), items_sold=('item_count','sum'))
            .sort_values('customer_id'))
```

**Edge cases:** Left-side NULL amounts are ignored by SUM; orders without items vanish under INNER JOIN (use LEFT). `SUM(DISTINCT amount)` would wrongly merge two different orders with the same amount. Also check for duplicate rows in the source (a re-loaded file) which look just like fan-out.
**Likely follow-ups:**
- Why not DISTINCT on the final result? It can hide the symptom on rows but does not fix SUM, and can drop legitimate identical rows.
- How do you prevent it? Know the grain of every table, test with row-count assertions after each join.
**Common mistakes:** Using SELECT DISTINCT or SUM(DISTINCT) to hide the problem; not checking the join keys for duplicates; joining two many-side tables to the same parent (the two fan-outs multiply).

### Q75 ⭐ 🔴 In a query mixing LEFT and INNER joins, how does the order of joins change the result?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you understand that a later INNER JOIN can silently undo an earlier LEFT JOIN.
**Say this in the interview:** "With only INNER joins the order does not change the result. But once LEFT and INNER are mixed, order matters: a LEFT JOIN creates NULLs for unmatched rows, and a later INNER JOIN that compares those NULLs throws those rows away, so the LEFT JOIN is cancelled. I either chain LEFT joins, or put the inner join inside a bracket or CTE first."
**Explain simply:**
- INNER JOIN keeps rows only if the condition is true. NULL = anything is unknown, so rows with NULLs from an earlier LEFT JOIN fail it.
- Result: `employees LEFT JOIN leaves INNER JOIN leave_types` returns only people with a leave (2 rows), as if the first join were INNER.
- Fixes: use LEFT for every join after a LEFT join; or join leaves to leave_types first, then LEFT JOIN employees to that result; or use a derived table or CTE.
- Order matters for LEFT/RIGHT/FULL joins; all INNER joins can be reordered freely (optimizers do so for speed). Joins are evaluated left to right unless you add brackets.
- The same cancellation happens when you filter the right table in WHERE (e.g. `WHERE l.type_id = 2`); put such filters in ON to keep the LEFT JOIN.
**Example:** HR report 'all employees with leave type': Ben and Dev never took leave, but version A drops them from the headcount.
**Sample data:**
`employees`

| emp_id | name |
|---|---|
| 1 | Asha |
| 2 | Ben |
| 3 | Chitra |
| 4 | Dev |

`leaves`

| leave_id | emp_id | type_id |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 3 | 2 |

`leave_types`

| type_id | type_name |
|---|---|
| 1 | Casual |
| 2 | Sick |

**SQL (A: LEFT then INNER; B: all LEFT joins; C: inner part grouped first):**
```sql
SELECT e.name, t.type_name
FROM employees e
LEFT JOIN leaves l       ON l.emp_id  = e.emp_id
INNER JOIN leave_types t ON t.type_id = l.type_id     -- NULL type_id from the LEFT JOIN fails here
ORDER BY e.emp_id;
```

```sql
SELECT e.name, t.type_name
FROM employees e
LEFT JOIN (leaves l INNER JOIN leave_types t ON t.type_id = l.type_id)   -- inner join first, as a unit
       ON l.emp_id = e.emp_id
ORDER BY e.emp_id;
```

Alternative to C without nested join syntax: `FROM employees e LEFT JOIN leaves l ON ... LEFT JOIN leave_types t ON ...` (all LEFT), or move the leave_types condition into a subquery or CTE.
**Output (A): employees without leaves are lost**

| name | type_name |
|---|---|
| Asha | Casual |
| Chitra | Sick |

**Output (C, same as all-LEFT): all 4 employees kept**

| name | type_name |
|---|---|
| Asha | Casual |
| Ben | NULL |
| Chitra | Sick |
| Dev | NULL |

**pandas equivalent:**
```python
# (C) correct version: inner-join leaves with leave_types first, then LEFT JOIN employees onto it
lt = leaves.merge(leave_types, on='type_id', how='inner')
result = employees.merge(lt, on='emp_id', how='left')[['name','type_name']].sort_values('name', key=lambda s: s.map({'Asha':1,'Ben':2,'Chitra':3,'Dev':4}))
# (A) the dropped-rows version in pandas:
a = employees.merge(leaves, on='emp_id', how='left').merge(leave_types, on='type_id', how='inner')[['name','type_name']]
```

**Edge cases:** A LEFT JOIN whose right table has duplicates still repeats left rows. If the later join legitimately needs only matched rows (e.g. employees who took leave), the INNER JOIN is what you want. Brackets around joins are not supported in all MySQL versions of older syntax; use a subquery there.
**Likely follow-ups:**
- INNER JOIN then LEFT JOIN, any trouble? No: `employees JOIN departments ... LEFT JOIN leaves` keeps the inner result and adds optional leaves.
- How do you spot the bug? Compare the row count with the left table's row count.
**Common mistakes:** Chaining INNER after LEFT and then wondering why employees vanished; putting right-table filters in WHERE; assuming join order never matters.

### Q76 ⭐ 🔴 How would you write an interval-overlap join (e.g., employees assigned to projects with overlapping dates)?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know the two-condition overlap rule and how to avoid self-matches and mirrored pairs.
**Say this in the interview:** "Two periods overlap when each one starts on or before the other ends: A.start <= B.end and B.start <= A.end. I self-join assignments on the same employee, use a.id < b.id so a row is not paired with itself and each pair appears once, and treat a NULL end date as open-ended using COALESCE."
**Explain simply:**
- Overlap test: A.start <= B.end AND B.start <= A.end. This one rule covers partial overlap, containment and identical ranges.
- Joining on `<` or `>` (not equals) is called a non-equi join; it is fine but slower because indexes help less.
- `a.assign_id < b.assign_id` removes pairing a row with itself and the mirror pair (A,B) vs (B,A).
- Open-ended assignment (end date NULL) -> replace with a far-future date.
- Overlap period = latest start to earliest end. Decide whether end dates are inclusive: here they are, so 28 Feb to 28 Feb counts as one overlapping day. For exclusive ends use `<` instead of `<=`.
**Example:** E1 is on Alpha until 31 Mar and Beta from 15 Mar: they overlap for 17 days, so E1 is double-booked. E3's Gamma sits fully inside Beta; that also counts.
**Sample data:**
`assignments` (E1's Gamma has no end date yet; E2's two projects touch on 28 Feb)

| assign_id | emp_id | project | start_date | end_date |
|---|---|---|---|---|
| 1 | E1 | Alpha | 2025-01-01 | 2025-03-31 |
| 2 | E1 | Beta | 2025-03-15 | 2025-06-30 |
| 3 | E1 | Gamma | 2025-07-01 | NULL |
| 4 | E2 | Alpha | 2025-01-01 | 2025-02-28 |
| 5 | E2 | Delta | 2025-02-28 | 2025-04-30 |
| 6 | E3 | Beta | 2025-01-01 | 2025-12-31 |
| 7 | E3 | Gamma | 2025-03-01 | 2025-03-31 |

**SQL (self join with the overlap rule):**
```sql
SELECT a.emp_id,
       a.project AS project_1, b.project AS project_2,
       MAX(a.start_date, b.start_date) AS overlap_start,                                   -- SQLite scalar MAX; use GREATEST elsewhere
       MIN(COALESCE(a.end_date,'9999-12-31'), COALESCE(b.end_date,'9999-12-31')) AS overlap_end  -- use LEAST elsewhere
FROM assignments a
JOIN assignments b
  ON  a.emp_id = b.emp_id
  AND a.assign_id < b.assign_id                                  -- each pair once, never with itself
  AND a.start_date <= COALESCE(b.end_date,   '9999-12-31')       -- A starts before B ends
  AND b.start_date <= COALESCE(a.end_date,   '9999-12-31')       -- B starts before A ends
ORDER BY a.emp_id, a.assign_id, b.assign_id;
```

Other dialects (not run here): PostgreSQL / MySQL use `GREATEST(a.start_date, b.start_date)` and `LEAST(...)`; SQL Server 2022+ has the same; PostgreSQL also has a built-in `daterange(a.start,a.end,'[]') && daterange(...)` overlap operator.
**Output:**

| emp_id | project_1 | project_2 | overlap_start | overlap_end |
|---|---|---|---|---|
| E1 | Alpha | Beta | 2025-03-15 | 2025-03-31 |
| E2 | Alpha | Delta | 2025-02-28 | 2025-02-28 |
| E3 | Beta | Gamma | 2025-03-01 | 2025-03-31 |

**pandas equivalent:**
```python
OPEN = '9999-12-31'
a = assignments.assign(end_date=assignments['end_date'].fillna(OPEN))
m = a.merge(a, on='emp_id', suffixes=('_1','_2'))
m = m[(m['assign_id_1'] < m['assign_id_2']) &
      (m['start_date_1'] <= m['end_date_2']) & (m['start_date_2'] <= m['end_date_1'])].copy()
m['overlap_start'] = m[['start_date_1','start_date_2']].max(axis=1)
m['overlap_end']   = m[['end_date_1','end_date_2']].min(axis=1)
result = (m.rename(columns={'project_1':'project_1','project_2':'project_2'})
            [['emp_id','project_1','project_2','overlap_start','overlap_end','assign_id_1','assign_id_2']]
            .sort_values(['emp_id','assign_id_1','assign_id_2'])
            .drop(columns=['assign_id_1','assign_id_2']))
```

**Edge cases:** NULL end date: without COALESCE the comparison is unknown and the row is dropped. Same-day touching is an overlap if ends are inclusive. Duplicate assignment rows create duplicate pairs. Interpretation: the question wording is ambiguous; I treated it as 'same employee on two projects at the same time'. For 'two employees on the same project at the same time' join on project instead of emp_id.
**Likely follow-ups:**
- How to count the overlap days? `julianday(overlap_end) - julianday(overlap_start) + 1` in SQLite; DATEDIFF in other databases.
- How to find one date's active assignments? `WHERE '2025-03-20' BETWEEN start_date AND COALESCE(end_date,'9999-12-31')`.
**Common mistakes:** Using `BETWEEN` for only one of the two ends; forgetting a.id < b.id (every row matches itself); forgetting NULL end dates; mixing text dates in non-ISO formats so comparisons fail.

### Q77 ⭐ 🔴 With a FULL OUTER JOIN and USING, which column is shown for the key and how do you handle NULLs on either side?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Do you know USING returns one merged key column, and that NULL keys never match, even to each other.
**Say this in the interview:** "With FULL OUTER JOIN ... USING (emp_id), the database returns a single emp_id column that already takes the value from whichever side has the row, so it behaves like COALESCE(a.emp_id, b.emp_id). With ON, I get two separate key columns, one NULL for unmatched rows, so I wrap them in COALESCE. NULL keys never match each other, so such rows stay separate on both sides."
**Explain simply:**
- USING (emp_id) = join on equal emp_id and show the column once. PostgreSQL, SQLite 3.39+ and DuckDB give the merged (non-NULL) value for unmatched rows. In ON, `h.emp_id` and `p.emp_id` are separate columns and one is NULL.
- Handle NULLs in other columns with COALESCE (e.g. salary 0, name 'not in HR'). Do not use `col = NULL`; use IS NULL.
- A NULL key in either table matches nothing (NULL = NULL is unknown), so Ghost and the 40,000 pay row appear as two separate rows rather than one matched row.
- To know which side a row came from, test a column that is never NULL in its own table (like a primary key or name) with IS NULL.
- In SQL Server there is no USING, so use ON + COALESCE; MySQL has no FULL JOIN (LEFT UNION RIGHT).
**Example:** HR has Asha, Ben; payroll has Ben, 3. Output rows: Asha with no salary, Ben with both, employee 3 with a salary but no name.
**Sample data:**
`hr`

| emp_id | name |
|---|---|
| 1 | Asha |
| 2 | Ben |
| NULL | Ghost |

`pay`

| emp_id | salary |
|---|---|
| 2 | 60000 |
| 3 | 55000 |
| NULL | 40000 |

**SQL (USING):**
```sql
SELECT emp_id, name, salary
FROM hr
FULL OUTER JOIN pay USING (emp_id)
ORDER BY emp_id, name;
```

**Output:**

| emp_id | name | salary |
|---|---|---|
| NULL | NULL | 40000 |
| NULL | Ghost | NULL |
| 1 | Asha | NULL |
| 2 | Ben | 60000 |
| 3 | NULL | 55000 |

**pandas equivalent:**
```python
hk, pk = hr[hr['emp_id'].notna()], pay[pay['emp_id'].notna()]
m = hk.merge(pk, on='emp_id', how='outer')                 # pandas would match NaN keys with each other,
nulls = pd.concat([hr[hr['emp_id'].isna()], pay[pay['emp_id'].isna()]])   # so keep NULL-key rows apart (like SQL)
result = (pd.concat([m, nulls])[['emp_id','name','salary']]
            .sort_values(['emp_id','name'], na_position='first'))
```

**SQL (ON version, with NULL handling; here `emp_id` has to be built by COALESCE):**
```sql
SELECT COALESCE(h.emp_id, p.emp_id) AS emp_id,
       COALESCE(h.name, 'not in HR')  AS name,
       COALESCE(p.salary, 0)          AS salary,
       h.emp_id IS NULL AND h.name IS NULL AS missing_in_hr
FROM hr h
FULL OUTER JOIN pay p ON p.emp_id = h.emp_id
ORDER BY 1, 2;
```

| emp_id | name | salary | missing_in_hr |
|---|---|---|---|
| NULL | Ghost | 0 | 0 |
| NULL | not in HR | 40000 | 1 |
| 1 | Asha | 0 | 0 |
| 2 | Ben | 60000 | 0 |
| 3 | not in HR | 55000 | 1 |

(Dialect note: USING works in PostgreSQL, MySQL, SQLite and DuckDB, but not in SQL Server; MySQL has no FULL JOIN; Oracle supports both. Only the SQLite and DuckDB behaviour was checked here.)
**Edge cases:** NULL keys on both sides do not pair up (pandas `merge` does pair NaN keys, a classic difference; code above avoids it). Duplicate keys multiply rows. In some databases ORDER BY on the USING column or qualified `h.emp_id` after USING behaves differently; select the unqualified column.
**Likely follow-ups:**
- Which table's value does USING show? The coalesced value: the left one when both exist, else the one that exists (PostgreSQL docs: the key is merged).
- How to make NULL keys match? `ON a.id = b.id OR (a.id IS NULL AND b.id IS NULL)`, or `IS NOT DISTINCT FROM` in PostgreSQL.
**Common mistakes:** Selecting `h.emp_id` and getting NULL for rows only in payroll; comparing to NULL with `=`; assuming NULL keys will match each other.

