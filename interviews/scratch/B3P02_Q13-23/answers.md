### Q13 ⭐⭐⭐ 🟡 Two child tables, one parent (the chasm trap): customers(customer_id, name), orders(order_id, customer_id, amount) and support_tickets(ticket_id, customer_id). Report per customer the total order amount and the ticket count in one query. Show why joining both child tables directly multiplies rows (3 orders x 2 tickets = 6 rows) and gives wrong totals, and fix it by aggregating each child to one row per customer before joining. Say when COUNT(DISTINCT) rescues a count but not a SUM. Give pandas.
**Asked at:** data-modelling write-ups on fan and chasm traps (Coginiti, Sisense, Holistics; snippets), not candidate reports; analyst and data scientist rounds and BI debugging
**Say this first (1 line):** Joining two child tables straight onto one parent makes every order meet every ticket for that customer (3 orders x 2 tickets = 6 rows), so any SUM or COUNT is multiplied; aggregate each child to one row per customer first, then LEFT JOIN those two small tables to the customer.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
CREATE TABLE support_tickets(ticket_id INTEGER PRIMARY KEY, customer_id INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1,20),(102,1,20),(103,1,30),(104,2,50);
INSERT INTO support_tickets VALUES (201,1),(202,1),(203,3);
```

**SQL answer:** the fix is `SQL_MAIN` in the Code block (the broken version is `SQL_NAIVE`, run next to it).
```sql
SELECT c.customer_id, c.name,
       COALESCE(o.total_amount, 0) AS total_amount,
       COALESCE(t.ticket_count, 0) AS ticket_count
FROM customers c
LEFT JOIN (SELECT customer_id, SUM(amount) AS total_amount
           FROM orders GROUP BY customer_id) o ON o.customer_id = c.customer_id
LEFT JOIN (SELECT customer_id, COUNT(*) AS ticket_count
           FROM support_tickets GROUP BY customer_id) t ON t.customer_id = c.customer_id
ORDER BY c.customer_id
```
The naive version, for contrast (also executed):
```sql
SELECT c.customer_id, c.name,
       COALESCE(SUM(o.amount), 0)           AS total_amount,
       COUNT(t.ticket_id)                   AS ticket_count,
       COUNT(DISTINCT t.ticket_id)          AS ticket_count_distinct,
       COALESCE(SUM(DISTINCT o.amount), 0)  AS sum_distinct_amount,
       COUNT(*)                             AS joined_rows
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
LEFT JOIN support_tickets t ON t.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY c.customer_id
```

**pandas answer:** aggregate each child with `groupby`, then merge the two small frames onto customers. `validate="one_to_one"` makes pandas raise if either aggregate is not one row per customer.
```python
order_tot = orders.groupby("customer_id", as_index=False).agg(total_amount=("amount", "sum"))
ticket_cnt = tickets.groupby("customer_id", as_index=False).agg(ticket_count=("ticket_id", "size"))
pd_df = (customers[["customer_id", "name"]]
         .merge(order_tot, on="customer_id", how="left", validate="one_to_one")
         .merge(ticket_cnt, on="customer_id", how="left", validate="one_to_one")
         .fillna({"total_amount": 0, "ticket_count": 0})
         .astype({"total_amount": "int64", "ticket_count": "int64"})
         .sort_values("customer_id").reset_index(drop=True))
```

**Example:** Asha has 3 orders (20, 20, 30; real total 70) and 2 tickets (201, 202).
- Joined directly, Asha becomes 3 x 2 = 6 rows. Each order row appears twice, so `SUM(amount)` = 2 x 70 = 140. Each ticket row appears three times, so `COUNT(t.ticket_id)` = 6.
- `COUNT(DISTINCT t.ticket_id)` = 2 is right, because ticket ids are unique. `SUM(DISTINCT o.amount)` = 20 + 30 = 50 is wrong (real 70, naive 140): it threw away the second order of 20.
- Ben: 1 order (50) and no tickets gives 1 joined row, so the naive result is correct for him. Chitra: no orders and 1 ticket gives 1 row with a NULL amount. Dev: 1 row, all NULL. The bug only bites customers that have 2 or more rows in both children, which is why it can pass a quick check on a few customers.
- Fixed: orders aggregate to (1, 70), (2, 50); tickets aggregate to (1, 2), (3, 1). Each side has one row per customer, so the LEFT JOINs add no rows. `COALESCE` turns the missing sides (Chitra's total, Ben's and Dev's ticket count) into 0.

**Code:** run with `python3 -I`.
```python
# Q13: chasm trap, two child tables under one parent: naive double join vs aggregate-each-child-first
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
CREATE TABLE support_tickets(ticket_id INTEGER PRIMARY KEY, customer_id INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1,20),(102,1,20),(103,1,30),(104,2,50);
INSERT INTO support_tickets VALUES (201,1),(202,1),(203,3);
"""
SQL_NAIVE = """
SELECT c.customer_id, c.name,
       COALESCE(SUM(o.amount), 0)           AS total_amount,
       COUNT(t.ticket_id)                   AS ticket_count,
       COUNT(DISTINCT t.ticket_id)          AS ticket_count_distinct,
       COALESCE(SUM(DISTINCT o.amount), 0)  AS sum_distinct_amount,
       COUNT(*)                             AS joined_rows
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
LEFT JOIN support_tickets t ON t.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY c.customer_id
"""
SQL_MAIN = """
SELECT c.customer_id, c.name,
       COALESCE(o.total_amount, 0) AS total_amount,
       COALESCE(t.ticket_count, 0) AS ticket_count
FROM customers c
LEFT JOIN (SELECT customer_id, SUM(amount) AS total_amount
           FROM orders GROUP BY customer_id) o ON o.customer_id = c.customer_id
LEFT JOIN (SELECT customer_id, COUNT(*) AS ticket_count
           FROM support_tickets GROUP BY customer_id) t ON t.customer_id = c.customer_id
ORDER BY c.customer_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
naive = pd.read_sql_query(SQL_NAIVE, con)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL naive (both children joined directly):")
print(naive.to_string(index=False))
print("\nSQL fixed (each child aggregated to one row per customer first):")
print(sql_df.to_string(index=False))

customers = pd.read_sql_query("SELECT * FROM customers", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
tickets = pd.read_sql_query("SELECT * FROM support_tickets", con)

# pandas naive: the same fan-out
fan = customers.merge(orders, on="customer_id", how="left").merge(tickets, on="customer_id", how="left")
print("\npandas naive merge, rows for Asha:", int((fan["customer_id"] == 1).sum()), "| total rows:", len(fan))
print("pandas naive sum of amount for Asha:", fan.loc[fan["customer_id"] == 1, "amount"].sum())

# pd:main
order_tot = orders.groupby("customer_id", as_index=False).agg(total_amount=("amount", "sum"))
ticket_cnt = tickets.groupby("customer_id", as_index=False).agg(ticket_count=("ticket_id", "size"))
pd_df = (customers[["customer_id", "name"]]
         .merge(order_tot, on="customer_id", how="left", validate="one_to_one")
         .merge(ticket_cnt, on="customer_id", how="left", validate="one_to_one")
         .fillna({"total_amount": 0, "ticket_count": 0})
         .astype({"total_amount": "int64", "ticket_count": "int64"})
         .sort_values("customer_id").reset_index(drop=True))
# pd:end
print("\npandas fixed:")
print(pd_df.to_string(index=False))

# compared after sorting both by customer_id
pd.testing.assert_frame_equal(sql_df.sort_values("customer_id").reset_index(drop=True), pd_df, check_dtype=False)
assert naive.loc[0, "total_amount"] == 140 and sql_df.loc[0, "total_amount"] == 70
assert orders["amount"].sum() == sql_df["total_amount"].sum() == 120   # totals tie to the child table
assert tickets.shape[0] == sql_df["ticket_count"].sum() == 3
print("\nasserts passed: SQL == pandas; totals tie to the child tables (120 and 3 tickets)")
```

**Output (my run):**
```text
SQL naive (both children joined directly):
 customer_id   name  total_amount  ticket_count  ticket_count_distinct  sum_distinct_amount  joined_rows
           1   Asha           140             6                      2                   50            6
           2    Ben            50             0                      0                   50            1
           3 Chitra             0             1                      1                    0            1
           4    Dev             0             0                      0                    0            1

SQL fixed (each child aggregated to one row per customer first):
 customer_id   name  total_amount  ticket_count
           1   Asha            70             2
           2    Ben            50             0
           3 Chitra             0             1
           4    Dev             0             0

pandas naive merge, rows for Asha: 6 | total rows: 9
pandas naive sum of amount for Asha: 140.0

pandas fixed:
 customer_id   name  total_amount  ticket_count
           1   Asha            70             2
           2    Ben            50             0
           3 Chitra             0             1
           4    Dev             0             0

asserts passed: SQL == pandas; totals tie to the child tables (120 and 3 tickets)
```

**Edge cases:**
- Customers with no orders or no tickets: the LEFT JOIN gives NULL, so `COALESCE(..., 0)` is needed in SQL and `fillna(0)` in pandas. In pandas the merged column turns `float64` (NaN), so I cast back to `int64`.
- If I used INNER JOINs to the aggregates, Ben, Chitra and Dev would vanish, because each is missing from one of the two children.
- Orphan children (an order whose customer_id is not in customers) are dropped by joining from `customers`; check totals against the child table to catch that. My assert compares 120 (sum of all orders) and 3 (all tickets) with the fixed result.
- Three child tables multiply the same way, and the fix is the same: one aggregate per child, then join.

**Then explain:**
- **Why it multiplies:** a join returns, for each customer, every combination of one matching order row and one matching ticket row. The two children are not related to each other, so every order pairs with every ticket. Rows per customer = orders x tickets.
- **Rule:** before joining, get every child to the same grain as the parent (one row per customer). Join aggregates, not raw rows.
- **COUNT(DISTINCT):** rescues a count only when you count a unique id of the child that was repeated (`COUNT(DISTINCT t.ticket_id)`, `COUNT(DISTINCT o.order_id)`). It cannot rescue a SUM: `SUM(DISTINCT amount)` collapses equal values that belong to different orders. It also costs a sort or hash on the multiplied rows, so it is a patch, not a design.
- **Order of joins does not help:** joining orders first and tickets second, or the reverse, gives the same 6 rows for Asha.
- **Check:** compare per-customer totals to `SUM(amount)` on the orders table alone. In my run the naive total for Asha is 140, orders alone give 70.
- Scalar subqueries in the SELECT list also work, but I have not run that form here.

**Follow-ups:**
- *Why is this called a chasm trap?* It is the data-modelling name for two one-to-many branches hanging off one parent (the BI-tool write-ups also call the single-branch version a fan trap).
- *Can I fix it with SUM(DISTINCT order_id)-style tricks?* Not safely: you can only distinct a value, and amounts repeat. Aggregate first.
- *What if I need the order and ticket detail rows?* Then they do not belong in one result; return two result sets, or accept the multiplication knowingly and never sum across it.

**Common mistakes:**
- Spotting the inflated SUM and adding `DISTINCT` to it.
- Fixing the count with `COUNT(DISTINCT)` and forgetting the SUM next to it is still wrong.
- Using INNER JOINs to the aggregates and silently dropping customers with no tickets.
- Not checking the result against each child table's own total.
- In pandas, two merges in a row with no `validate=` and no row-count check.

### Q14 ⭐⭐⭐ 🟡 Students and Examinations style grid: students(student_id, name), subjects(subject_name) and exams(student_id, subject_name), one row per exam attended. Report, for every student and every subject, how many times the student attended the exam, including 0. Explain why a CROSS JOIN of students and subjects comes first and a LEFT JOIN to exams second, and give the pandas version (how='cross', then merge and fillna).
**Asked at:** public LeetCode-style problem bank (SQL 50 join problems, known only from repo snippets), not a candidate report; analyst and data scientist screens
**Say this first (1 line):** Build the full grid first with a CROSS JOIN of students and subjects (every student-subject pair, even if never examined), then LEFT JOIN the exams onto the grid and COUNT a column from the exams side, so pairs with no exams show 0.

**Schema and sample data:**
```sql
CREATE TABLE students(student_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE subjects(subject_name TEXT PRIMARY KEY);
CREATE TABLE exams(student_id INTEGER, subject_name TEXT);
INSERT INTO students VALUES (1,'Alice'),(2,'Bob'),(6,'Alex'),(13,'John');
INSERT INTO subjects VALUES ('Math'),('Physics'),('Programming');
INSERT INTO exams VALUES (1,'Math'),(1,'Physics'),(1,'Programming'),(2,'Programming'),(1,'Physics'),
 (1,'Math'),(13,'Math'),(13,'Programming'),(13,'Physics'),(2,'Math'),(1,'Math');
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
SELECT st.student_id, st.name, su.subject_name,
       COUNT(e.subject_name) AS attended_exams
FROM students st
CROSS JOIN subjects su
LEFT JOIN exams e ON e.student_id = st.student_id AND e.subject_name = su.subject_name
GROUP BY st.student_id, st.name, su.subject_name
ORDER BY st.student_id, su.subject_name
```

**pandas answer:** `how="cross"` for the grid, `groupby(...).size()` for the counts, then a left merge and `fillna`.
```python
grid = students.merge(subjects, how="cross")
counts = exams.groupby(["student_id", "subject_name"], as_index=False).agg(attended_exams=("subject_name", "size"))
pd_df = (grid.merge(counts, on=["student_id", "subject_name"], how="left", validate="one_to_one")
         .fillna({"attended_exams": 0}).astype({"attended_exams": "int64"})
         .sort_values(["student_id", "subject_name"]).reset_index(drop=True))
```

**Example:** 4 students x 3 subjects = 12 grid rows.
- Alice's exam rows: Math x3, Physics x2, Programming x1, so (3, 2, 1).
- Bob: Math 1, Programming 1, Physics 0 (no exam row, so the LEFT JOIN gives NULL and `COUNT(e.subject_name)` counts 0).
- Alex (id 6): no exam rows at all, so (0, 0, 0). John (13): (1, 1, 1).
- The counts add up to 3+2+1+1+0+1+0+0+0+1+1+1 = 11, the number of rows in `exams`. My assert checks this.

**Code:** run with `python3 -I`.
```python
# Q14: students x subjects grid with exam counts (CROSS JOIN first, LEFT JOIN second)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE students(student_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE subjects(subject_name TEXT PRIMARY KEY);
CREATE TABLE exams(student_id INTEGER, subject_name TEXT);
INSERT INTO students VALUES (1,'Alice'),(2,'Bob'),(6,'Alex'),(13,'John');
INSERT INTO subjects VALUES ('Math'),('Physics'),('Programming');
INSERT INTO exams VALUES (1,'Math'),(1,'Physics'),(1,'Programming'),(2,'Programming'),(1,'Physics'),
 (1,'Math'),(13,'Math'),(13,'Programming'),(13,'Physics'),(2,'Math'),(1,'Math');
"""
SQL_MAIN = """
SELECT st.student_id, st.name, su.subject_name,
       COUNT(e.subject_name) AS attended_exams
FROM students st
CROSS JOIN subjects su
LEFT JOIN exams e ON e.student_id = st.student_id AND e.subject_name = su.subject_name
GROUP BY st.student_id, st.name, su.subject_name
ORDER BY st.student_id, su.subject_name
"""
SQL_WRONG_COUNT = """
SELECT st.student_id, su.subject_name, COUNT(*) AS attended_exams
FROM students st CROSS JOIN subjects su
LEFT JOIN exams e ON e.student_id = st.student_id AND e.subject_name = su.subject_name
WHERE st.student_id = 6
GROUP BY st.student_id, su.subject_name ORDER BY su.subject_name
"""
SQL_NO_GRID = """
SELECT st.student_id, e.subject_name, COUNT(*) AS attended_exams
FROM students st LEFT JOIN exams e ON e.student_id = st.student_id
WHERE st.student_id = 6 GROUP BY st.student_id, e.subject_name
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("\nrows:", len(sql_df), "= 4 students x 3 subjects")
print("\nCOUNT(*) instead of COUNT(e.subject_name), Alex (no exams):")
print(pd.read_sql_query(SQL_WRONG_COUNT, con).to_string(index=False))
print("\nLEFT JOIN students to exams only, no grid, Alex:")
print(pd.read_sql_query(SQL_NO_GRID, con).to_string(index=False))

students = pd.read_sql_query("SELECT * FROM students", con)
subjects = pd.read_sql_query("SELECT * FROM subjects", con)
exams = pd.read_sql_query("SELECT * FROM exams", con)

# pd:main
grid = students.merge(subjects, how="cross")
counts = exams.groupby(["student_id", "subject_name"], as_index=False).agg(attended_exams=("subject_name", "size"))
pd_df = (grid.merge(counts, on=["student_id", "subject_name"], how="left", validate="one_to_one")
         .fillna({"attended_exams": 0}).astype({"attended_exams": "int64"})
         .sort_values(["student_id", "subject_name"]).reset_index(drop=True))
# pd:end
print("\npandas dtype of attended_exams after fillna and astype:", pd_df["attended_exams"].dtype)
raw = grid.merge(counts, on=["student_id", "subject_name"], how="left")
print("dtype before fillna:", raw["attended_exams"].dtype)

# compared after sorting by student_id, subject_name
pd.testing.assert_frame_equal(sql_df.sort_values(["student_id", "subject_name"]).reset_index(drop=True),
                              pd_df[sql_df.columns], check_dtype=False)
assert pd_df["attended_exams"].sum() == len(exams) == 11
print("asserts passed: SQL == pandas; counts sum to", len(exams), "exam rows")
```

**Output (my run):**
```text
 student_id  name subject_name  attended_exams
          1 Alice         Math               3
          1 Alice      Physics               2
          1 Alice  Programming               1
          2   Bob         Math               1
          2   Bob      Physics               0
          2   Bob  Programming               1
          6  Alex         Math               0
          6  Alex      Physics               0
          6  Alex  Programming               0
         13  John         Math               1
         13  John      Physics               1
         13  John  Programming               1

rows: 12 = 4 students x 3 subjects

COUNT(*) instead of COUNT(e.subject_name), Alex (no exams):
 student_id subject_name  attended_exams
          6         Math               1
          6      Physics               1
          6  Programming               1

LEFT JOIN students to exams only, no grid, Alex:
 student_id subject_name  attended_exams
          6         None               1

pandas dtype of attended_exams after fillna and astype: int64
dtype before fillna: float64
asserts passed: SQL == pandas; counts sum to 11 exam rows
```

**Edge cases:**
- A student who sat nothing (Alex) still gets three rows of 0, because the grid is built before the exams are looked at.
- A student-subject pair can have many exam rows (Alice took Math three times), so the count can exceed 1. A pair is not unique in `exams`, which is why pandas counts with `groupby().size()` before merging, and why the merge can use `validate="one_to_one"`.
- Duplicate rows in `subjects` or `students` would multiply the grid; the primary key on `subject_name` in the sample guards that in SQL.
- A subject listed in `exams` but missing from `subjects` never appears in the output, because the grid is the source of truth.

**Then explain:**
- **Why CROSS JOIN first:** a LEFT JOIN keeps every row of its left side and nothing else. The left side must already contain every (student, subject) combination, and only a cross product of the two lists can create the combinations that never happened.
- **Why the LEFT JOIN second:** it attaches the exam rows, leaving NULLs where none exist. The ON condition has both keys (student and subject).
- **COUNT(e.subject_name), not COUNT(*):** for Alex, `COUNT(*)` counts the one NULL-extended row and returns 1 for every subject (shown in my output). Counting a column from the right table ignores NULLs and gives 0.
- **Without the grid:** a LEFT JOIN of students to exams alone gives Alex one row with a NULL subject, and Bob has no Physics row at all (shown in my output).
- **pandas dtype:** after the left merge the count column is `float64` (NaN for missing), `fillna(0)` alone keeps float, so cast to `int64` (both dtypes printed in my run).

**Follow-ups:**
- *What if the subject list should come from the data, not a table?* `SELECT DISTINCT subject_name FROM exams` as a derived table works, but it misses subjects nobody took, so keep a subjects table.
- *Can this be done with GROUP BY on exams alone?* No, there are no rows for the zero cases.
- *Cost?* The grid has students x subjects rows, which is fine here and large only for big dimension tables.

**Common mistakes:**
- Using `COUNT(*)` and getting 1 instead of 0.
- A LEFT JOIN from students to exams only, with no grid.
- Putting the subject condition in WHERE (which would turn the LEFT JOIN into an inner join, Q3).
- Forgetting to cast back to integer after `fillna` in pandas.
- Counting rows from `exams` per student without grouping by subject.

### Q15 ⭐⭐⭐ 🟡 Self join for pairs: employees(emp_id, name, dept_id). List all pairs of colleagues in the same department, each pair once and never an employee with themselves. Explain why a.emp_id < b.emp_id (not <>) removes mirror pairs, how many pairs n employees produce, and how to do the same in pandas (merge on dept_id then filter, and itertools.combinations as an alternative).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Self-join employees to itself on the same dept_id with `a.emp_id < b.emp_id`: it drops the self pairs and keeps exactly one of the two mirror pairs; n employees in a department make n(n-1)/2 pairs.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER);
INSERT INTO employees VALUES (1,'Asha',10),(2,'Ben',10),(3,'Chitra',10),(4,'Dev',20),(5,'Esha',20),
                             (6,'Farah',30),(7,'Gopal',NULL),(8,'Hari',NULL);
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
SELECT a.dept_id, a.name AS name_a, b.name AS name_b
FROM employees a
JOIN employees b ON a.dept_id = b.dept_id AND a.emp_id < b.emp_id
ORDER BY a.dept_id, a.emp_id, b.emp_id
```

**pandas answer:** merge the frame with itself on `dept_id`, filter on the id order. I drop NaN departments first (reason below). The alternative is `itertools.combinations` per group; both are in the Code block.
```python
m = emp.dropna(subset=["dept_id"]).merge(emp.dropna(subset=["dept_id"]), on="dept_id", suffixes=("_a", "_b"))
pd_df = (m[m["emp_id_a"] < m["emp_id_b"]][["dept_id", "name_a", "name_b", "emp_id_a", "emp_id_b"]]
         .sort_values(["dept_id", "emp_id_a", "emp_id_b"]).reset_index(drop=True))
```

**Example:** departments 10 = Asha(1), Ben(2), Chitra(3); 20 = Dev(4), Esha(5); 30 = Farah(6); Gopal(7) and Hari(8) have no department.
- Dept 10: pairs (1,2), (1,3), (2,3) = 3 = 3x2/2. Dept 20: (4,5) = 1. Dept 30: no pair (1 person gives 0). Gopal and Hari: NULL = NULL is not true, so no join, no pair.
- Total 4 pairs. With `<>` instead of `<`, each pair appears twice (8 rows). With no id filter at all the join returns 14 rows: 8 ordered pairs plus 6 rows pairing someone with themselves (3 + 2 + 1).

**Code:** run with `python3 -I`.
```python
# Q15: pairs of colleagues in the same department, each pair once (self join, a.emp_id < b.emp_id)
import sqlite3
from itertools import combinations
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER);
INSERT INTO employees VALUES (1,'Asha',10),(2,'Ben',10),(3,'Chitra',10),(4,'Dev',20),(5,'Esha',20),
                             (6,'Farah',30),(7,'Gopal',NULL),(8,'Hari',NULL);
"""
SQL_MAIN = """
SELECT a.dept_id, a.name AS name_a, b.name AS name_b
FROM employees a
JOIN employees b ON a.dept_id = b.dept_id AND a.emp_id < b.emp_id
ORDER BY a.dept_id, a.emp_id, b.emp_id
"""
SQL_NE = "SELECT COUNT(*) FROM employees a JOIN employees b ON a.dept_id = b.dept_id AND a.emp_id <> b.emp_id"
SQL_NO_FILTER = "SELECT COUNT(*) FROM employees a JOIN employees b ON a.dept_id = b.dept_id"
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("\npairs (a.emp_id < b.emp_id):", len(sql_df))
print("rows with <> instead of <:", con.execute(SQL_NE).fetchone()[0], "(every pair twice)")
print("rows with no id filter:", con.execute(SQL_NO_FILTER).fetchone()[0], "(8 ordered pairs + 6 self rows)")

emp = pd.read_sql_query("SELECT * FROM employees", con)
print("\ndept_id dtype in pandas:", emp["dept_id"].dtype)

# pd:main
m = emp.dropna(subset=["dept_id"]).merge(emp.dropna(subset=["dept_id"]), on="dept_id", suffixes=("_a", "_b"))
pd_df = (m[m["emp_id_a"] < m["emp_id_b"]][["dept_id", "name_a", "name_b", "emp_id_a", "emp_id_b"]]
         .sort_values(["dept_id", "emp_id_a", "emp_id_b"]).reset_index(drop=True))
# pd:end
print("\npandas merge + filter (NaN dept dropped first):", len(pd_df), "pairs")

# without dropna: NaN keys match each other in pandas merge
m_nan = emp.merge(emp, on="dept_id", suffixes=("_a", "_b"))
nan_pairs = m_nan[m_nan["emp_id_a"] < m_nan["emp_id_b"]]
print("pandas merge WITHOUT dropna, pairs:", len(nan_pairs))
print(nan_pairs[nan_pairs["dept_id"].isna()][["name_a", "name_b"]].to_string(index=False))

# itertools alternative (groupby drops NaN keys by default)
combo = [(g_dept, a, b) for g_dept, g in emp.groupby("dept_id")
         for (a, b) in combinations(g.sort_values("emp_id")["name"], 2)]
combo_df = pd.DataFrame(combo, columns=["dept_id", "name_a", "name_b"])
print("\nitertools.combinations pairs:", len(combo_df))

# n employees -> n(n-1)/2 pairs per department
sizes = emp.groupby("dept_id").size()
assert int((sizes * (sizes - 1) // 2).sum()) == len(sql_df) == 4
cmp_sql = sql_df.copy(); cmp_sql["dept_id"] = cmp_sql["dept_id"].astype(float)
# all compared after sorting by dept_id, then emp_id order (names listed in id order)
pd.testing.assert_frame_equal(cmp_sql, pd_df[["dept_id", "name_a", "name_b"]], check_dtype=False)
pd.testing.assert_frame_equal(cmp_sql.reset_index(drop=True),
                              combo_df.astype({"dept_id": "float64"}), check_dtype=False)
print("asserts passed: SQL == pandas merge+filter == itertools.combinations")
```

**Output (my run):**
```text
 dept_id name_a name_b
      10   Asha    Ben
      10   Asha Chitra
      10    Ben Chitra
      20    Dev   Esha

pairs (a.emp_id < b.emp_id): 4
rows with <> instead of <: 8 (every pair twice)
rows with no id filter: 14 (8 ordered pairs + 6 self rows)

dept_id dtype in pandas: float64

pandas merge + filter (NaN dept dropped first): 4 pairs
pandas merge WITHOUT dropna, pairs: 5
name_a name_b
 Gopal   Hari

itertools.combinations pairs: 4
asserts passed: SQL == pandas merge+filter == itertools.combinations
```

**Edge cases:**
- NULL dept_id: no pairs in SQL. Surprise in pandas: `merge` matches NaN keys to NaN keys, so merging without the `dropna` produced 5 pairs, with the extra pair Gopal-Hari (shown in the output). The `groupby` route drops NaN keys by default, so `combinations` gave 4. Decide on purpose whether "no department" people count as colleagues.
- A department with one person gives no pair; an empty department gives no row.
- Duplicate employee rows (same person loaded twice with different emp_id) show up as a pair with themselves; clean the data first.
- Ordering of the pair: `a.emp_id < b.emp_id` always puts the smaller id in column a, so (Asha, Ben) appears and (Ben, Asha) does not.

**Then explain:**
- **Why `<` and not `<>`:** `<>` removes self pairs but keeps both (a,b) and (b,a). `<` removes both the self pairs (a.emp_id = b.emp_id is not less) and the mirror pairs, because for any two people exactly one is smaller.
- **How many pairs:** n(n-1)/2 per department, so the self join grows with the square of the department size. A 1,000-person department gives 499,500 pairs, so check sizes first.
- **pandas:** the merge builds all n x n ordered pairs in memory then filters, which wastes memory for large groups; `combinations` generates only the n(n-1)/2 pairs but is a Python loop.
- The key to pass to pandas is the same `dept_id`; the suffixes `_a` and `_b` stand for the two aliases.

**Follow-ups:**
- *How would you include the pair count per department?* `GROUP BY a.dept_id` on the same join with `COUNT(*)`.
- *Three-person groups (triples)?* Add a second self join with `b.emp_id < c.emp_id`.
- *What if the table has no unique id?* Create one first, otherwise there is no ordering to break the tie.

**Common mistakes:**
- Using `<>` and reporting every pair twice.
- Using `a.name < b.name` when names can repeat (identical names would be dropped as "equal").
- Forgetting the dept condition, which makes a cross join of the whole table.
- Assuming pandas treats NaN keys like SQL treats NULLs.

### Q16 ⭐⭐⭐ 🟡 Find unmatched rows on both sides: payments(payment_id, order_id, amount) and orders(order_id, amount). List payments with no order, orders with no payment, and matched rows, in one result with a status column. Use FULL OUTER JOIN (SQLite 3.39+ runs it; hedge MySQL), and pandas merge how='outer' with indicator=True. Explain why the coalesced key is needed in the output.
**Asked at:** StrataScratch join problem list (bank items labelled with company names by the guide, not candidate reports); product-company data scientist screens
**Say this first (1 line):** FULL OUTER JOIN payments to orders on order_id, take the key with `COALESCE(o.order_id, p.order_id)`, and label each row from which side is NULL (matched, payment without order, order without payment); in pandas it is `merge(how="outer", indicator=True)`.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, amount INTEGER);
CREATE TABLE payments(payment_id INTEGER PRIMARY KEY, order_id INTEGER, amount INTEGER);
INSERT INTO orders VALUES (1,100),(2,200),(3,300);
INSERT INTO payments VALUES (11,1,100),(12,2,150),(13,9,50),(14,NULL,70);
```

**SQL answer:** `SQL_MAIN` in the Code block (executed on SQLite 3.45.1).
```sql
SELECT COALESCE(o.order_id, p.order_id) AS order_id,
       p.payment_id, o.amount AS order_amount, p.amount AS paid_amount,
       CASE WHEN o.order_id IS NULL THEN 'payment_without_order'
            WHEN p.payment_id IS NULL THEN 'order_without_payment'
            ELSE 'matched' END AS status
FROM payments p
FULL OUTER JOIN orders o ON o.order_id = p.order_id
ORDER BY status, order_id, payment_id
```
Dialect notes, **not executed here**: PostgreSQL, SQL Server, Oracle, Snowflake and BigQuery support `FULL OUTER JOIN`; MySQL has no `FULL OUTER JOIN` (the MySQL 8.4 JOIN page I read lists only LEFT and RIGHT), so there you emulate it with a LEFT JOIN plus the unmatched right rows (Q32). That SQLite added RIGHT and FULL JOIN in version 3.39 is from memory; I could only run on 3.45.1, where both work (my run printed a RIGHT JOIN result too).

**pandas answer:** the indicator column says which side each row came from.
```python
m = payments.merge(orders, on="order_id", how="outer", indicator=True,
                   suffixes=("_pay", "_ord"), validate="many_to_one")
m["status"] = m["_merge"].map({"both": "matched", "left_only": "payment_without_order",
                               "right_only": "order_without_payment"}).astype(str)
pd_df = (m.rename(columns={"amount_ord": "order_amount", "amount_pay": "paid_amount"})
         [["order_id", "payment_id", "order_amount", "paid_amount", "status"]]
         .sort_values(["status", "order_id", "payment_id"], na_position="last").reset_index(drop=True))
```

**Example:** orders 1 (100), 2 (200), 3 (300); payments 11 -> order 1 (100), 12 -> order 2 (150), 13 -> order 9 (50), 14 -> order NULL (70).
- Orders 1 and 2 have a matching payment: status `matched` (note order 2 is matched by key even though 150 is not 200; amount checks are a separate step, Q44).
- Order 3 has no payment: `order_without_payment`.
- Payment 13 points to order 9, which does not exist: `payment_without_order`. Payment 14 has a NULL order_id, which cannot equal anything: also `payment_without_order`.
- 5 rows in total: 2 matched, 1 order without payment, 2 payments without order.

**Code:** run with `python3 -I`.
```python
# Q16: reconcile payments and orders with FULL OUTER JOIN and a status column
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, amount INTEGER);
CREATE TABLE payments(payment_id INTEGER PRIMARY KEY, order_id INTEGER, amount INTEGER);
INSERT INTO orders VALUES (1,100),(2,200),(3,300);
INSERT INTO payments VALUES (11,1,100),(12,2,150),(13,9,50),(14,NULL,70);
"""
SQL_MAIN = """
SELECT COALESCE(o.order_id, p.order_id) AS order_id,
       p.payment_id, o.amount AS order_amount, p.amount AS paid_amount,
       CASE WHEN o.order_id IS NULL THEN 'payment_without_order'
            WHEN p.payment_id IS NULL THEN 'order_without_payment'
            ELSE 'matched' END AS status
FROM payments p
FULL OUTER JOIN orders o ON o.order_id = p.order_id
ORDER BY status, order_id, payment_id
"""
SQL_NO_COALESCE = """
SELECT o.order_id, p.payment_id FROM payments p FULL OUTER JOIN orders o ON o.order_id = p.order_id
ORDER BY o.order_id, p.payment_id
"""
SQL_RIGHT = "SELECT o.order_id, p.payment_id FROM orders o RIGHT JOIN payments p ON o.order_id = p.order_id ORDER BY p.payment_id"
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("SQLite version:", sqlite3.sqlite_version)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("\nwithout COALESCE (o.order_id only):")
print(pd.read_sql_query(SQL_NO_COALESCE, con).to_string(index=False))
print("\nRIGHT JOIN runs on this SQLite:", con.execute(SQL_RIGHT).fetchall())

payments = pd.read_sql_query("SELECT * FROM payments", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
m = payments.merge(orders, on="order_id", how="outer", indicator=True,
                   suffixes=("_pay", "_ord"), validate="many_to_one")
m["status"] = m["_merge"].map({"both": "matched", "left_only": "payment_without_order",
                               "right_only": "order_without_payment"}).astype(str)
pd_df = (m.rename(columns={"amount_ord": "order_amount", "amount_pay": "paid_amount"})
         [["order_id", "payment_id", "order_amount", "paid_amount", "status"]]
         .sort_values(["status", "order_id", "payment_id"], na_position="last").reset_index(drop=True))
# pd:end
print("\npandas outer merge with indicator:")
print(m[["order_id", "payment_id", "_merge"]].to_string(index=False))
print("\nstatus counts:", pd_df["status"].value_counts().to_dict())

def norm(d):
    d = d.copy()
    d["order_id"] = d["order_id"].astype("float64")
    for c in ["payment_id", "order_amount", "paid_amount"]:
        d[c] = d[c].astype("float64")
    return d.reset_index(drop=True)
# compared after sorting by status, then order_id, then payment_id (NULL order_id last)
s = sql_df.sort_values(["status", "order_id", "payment_id"], na_position="last")
pd.testing.assert_frame_equal(norm(s), norm(pd_df), check_dtype=False)
assert len(sql_df) == 5 and (sql_df["status"] == "matched").sum() == 2
print("asserts passed: SQL FULL JOIN == pandas outer merge")
```

**Output (my run):**
```text
SQLite version: 3.45.1
 order_id  payment_id  order_amount  paid_amount                status
      1.0        11.0         100.0        100.0               matched
      2.0        12.0         200.0        150.0               matched
      3.0         NaN         300.0          NaN order_without_payment
      NaN        14.0           NaN         70.0 payment_without_order
      9.0        13.0           NaN         50.0 payment_without_order

without COALESCE (o.order_id only):
 order_id  payment_id
      NaN        13.0
      NaN        14.0
      1.0        11.0
      2.0        12.0
      3.0         NaN

RIGHT JOIN runs on this SQLite: [(1, 11), (2, 12), (None, 13), (None, 14)]

pandas outer merge with indicator:
 order_id  payment_id     _merge
      1.0        11.0       both
      2.0        12.0       both
      3.0         NaN right_only
      9.0        13.0  left_only
      NaN        14.0  left_only

status counts: {'matched': 2, 'payment_without_order': 2, 'order_without_payment': 1}
asserts passed: SQL FULL JOIN == pandas outer merge
```

**Edge cases:**
- NULL order_id in payments: never matches, so it lands in the unmatched-payment group. After `COALESCE` its order_id is still NULL, so identify such rows by `payment_id`.
- Several payments for one order give several matched rows (a one-to-many join); aggregate first if you need one row per order (Q44).
- Duplicate order_id in orders would duplicate rows; in pandas `validate="many_to_one"` (payments on the left, orders on the right) raises an error instead.
- In pandas the key and the amount columns become `float64` because the outer merge introduces NaN; the compare step casts both sides.
- `indicator=True` values are `both`, `left_only` (payments only) and `right_only` (orders only); I map them to the same status words. The meaning of left and right flips if you swap the frames.

**Then explain:**
- **Why the coalesced key:** in a FULL JOIN a row from only one side has NULLs for the other side's columns. `o.order_id` alone is NULL for both orphan payments, so order 9 is invisible (the "without COALESCE" block in my output); `p.order_id` alone is NULL for the unpaid order 3. `COALESCE(o.order_id, p.order_id)` gives one key column that is filled for every row.
- **pandas does the coalescing for you** when you merge `on="order_id"`: one key column holding the keys of both sides, with `indicator` as the status. With `left_on` and `right_on` you get two columns and must coalesce yourself.
- **Status logic:** test the primary key of each side for NULL (`o.order_id IS NULL`, `p.payment_id IS NULL`), not an amount, which can be legitimately NULL.
- **RIGHT JOIN** is a LEFT JOIN with the tables swapped; FULL is the union of both.

**Follow-ups:**
- *No FULL JOIN in the engine?* LEFT JOIN plus UNION ALL of the right-only rows (Q32, hedged for MySQL).
- *How do I check the amounts too?* Add `CASE WHEN p.amount <> o.amount` only inside the matched branch, and aggregate payments per order first.
- *Why not UNION of two anti-joins?* That loses the matched rows; you would add a third query.

**Common mistakes:**
- Selecting only `o.order_id` and losing the keys of orphan payments.
- Using `p.amount IS NULL` as the "no payment" test.
- Putting a filter on one side in WHERE, which turns the FULL JOIN into a narrower join (Q3).
- Reading `left_only` as "orders only" in pandas without checking which frame is on the left.

### Q17 ⭐⭐⭐ 🟡 Multiple joins and join order: orders(order_id, customer_id, product_id), customers(customer_id, name, city), products(product_id, name, category_id) and categories(category_id, category_name). Write the four-table join for order, customer name and category. Does join order change the result for INNER joins? For LEFT joins? Show how an INNER JOIN placed after a LEFT JOIN on a nullable path drops rows, and what the optimiser does about join order (concept only).
**Asked at:** DataCamp and InterviewBit SQL joins interview guides, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** Start from orders and LEFT JOIN customers, products and categories in a chain; INNER joins can be listed in any order and give the same rows, but an INNER JOIN placed after a LEFT JOIN on a nullable path silently deletes the rows the LEFT JOIN kept.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE categories(category_id INTEGER PRIMARY KEY, category_name TEXT);
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT, category_id INTEGER);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER);
INSERT INTO customers VALUES (1,'Asha','Pune'),(2,'Ben','Delhi'),(3,'Chitra','Mumbai');
INSERT INTO categories VALUES (1,'Stationery'),(2,'Books');
INSERT INTO products VALUES (10,'Pen',1),(20,'Novel',2),(30,'Lamp',NULL),(40,'Desk',3);
INSERT INTO orders VALUES (1,1,10),(2,1,20),(3,2,30),(4,2,40),(5,NULL,10);
```

**SQL answer:** the four-table join keeping every order is `SQL_MAIN` (all LEFT); the all-INNER version is `SQL_INNER`.
```sql
SELECT o.order_id, c.name AS customer, p.name AS product, cat.category_name
FROM orders o
LEFT JOIN customers c  ON c.customer_id = o.customer_id
LEFT JOIN products p   ON p.product_id = o.product_id
LEFT JOIN categories cat ON cat.category_id = p.category_id
ORDER BY o.order_id
```
```sql
SELECT o.order_id, c.name AS customer, p.name AS product, cat.category_name
FROM orders o
JOIN customers c  ON c.customer_id = o.customer_id
JOIN products p   ON p.product_id = o.product_id
JOIN categories cat ON cat.category_id = p.category_id
ORDER BY o.order_id
```
The traps, also executed in the Code block:
```sql
SELECT o.order_id, p.name AS product, cat.category_name
FROM orders o
LEFT JOIN products p ON p.product_id = o.product_id
JOIN categories cat ON cat.category_id = p.category_id
ORDER BY o.order_id
```
```sql
SELECT o.order_id, p.name AS product, cat.category_name
FROM orders o
LEFT JOIN (products p JOIN categories cat ON cat.category_id = p.category_id)
       ON p.product_id = o.product_id
ORDER BY o.order_id
```

**pandas answer:** chain the merges, left from the fact table, each with `validate="many_to_one"` (each dimension key is unique).
```python
pd_df = (orders
         .merge(customers.rename(columns={"name": "customer"})[["customer_id", "customer"]],
                on="customer_id", how="left", validate="many_to_one")
         .merge(products.rename(columns={"name": "product"})[["product_id", "product", "category_id"]],
                on="product_id", how="left", validate="many_to_one")
         .merge(categories, on="category_id", how="left", validate="many_to_one")
         [["order_id", "customer", "product", "category_name"]]
         .sort_values("order_id").reset_index(drop=True))
pd_inner = (orders.merge(customers, on="customer_id", validate="many_to_one")
            .merge(products, on="product_id", suffixes=("_cust", "_prod"), validate="many_to_one")
            .merge(categories, on="category_id", validate="many_to_one"))
```

**Example:** orders 1 (Asha, Pen), 2 (Asha, Novel), 3 (Ben, Lamp), 4 (Ben, Desk), 5 (no customer, Pen). Pen is in category 1 and Novel in 2; Lamp has a NULL category_id; Desk points at category 3, which does not exist.
- All LEFT: 5 rows; category_name is NULL for orders 3 and 4, and customer is NULL for order 5.
- All INNER: only orders 1 and 2 survive (order 3: NULL category key, order 4: dangling key, order 5: no customer) = 2 rows.
- `orders LEFT JOIN products` then plain `JOIN categories`: 3 rows (orders 1, 2 and 5). Orders 3 and 4 are dropped, even though the first join kept them, because the NULL-extended category key can never equal a category_id. Order 5 survives because it has a product and a category; its missing customer is not in this query.
- Parenthesised form `orders LEFT JOIN (products JOIN categories ...)`: all 5 orders, but Lamp and Desk appear as NULL products, since the inner pair excluded them before the LEFT JOIN attached.

**Code:** run with `python3 -I`.
```python
# Q17: four-table join, join order, and an INNER JOIN after a LEFT JOIN on a nullable path
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE categories(category_id INTEGER PRIMARY KEY, category_name TEXT);
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT, category_id INTEGER);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER);
INSERT INTO customers VALUES (1,'Asha','Pune'),(2,'Ben','Delhi'),(3,'Chitra','Mumbai');
INSERT INTO categories VALUES (1,'Stationery'),(2,'Books');
INSERT INTO products VALUES (10,'Pen',1),(20,'Novel',2),(30,'Lamp',NULL),(40,'Desk',3);
INSERT INTO orders VALUES (1,1,10),(2,1,20),(3,2,30),(4,2,40),(5,NULL,10);
"""
SQL_MAIN = """
SELECT o.order_id, c.name AS customer, p.name AS product, cat.category_name
FROM orders o
LEFT JOIN customers c  ON c.customer_id = o.customer_id
LEFT JOIN products p   ON p.product_id = o.product_id
LEFT JOIN categories cat ON cat.category_id = p.category_id
ORDER BY o.order_id
"""
SQL_INNER = """
SELECT o.order_id, c.name AS customer, p.name AS product, cat.category_name
FROM orders o
JOIN customers c  ON c.customer_id = o.customer_id
JOIN products p   ON p.product_id = o.product_id
JOIN categories cat ON cat.category_id = p.category_id
ORDER BY o.order_id
"""
# same INNER joins written in a different textual order
SQL_INNER_REORDERED = """
SELECT o.order_id, c.name AS customer, p.name AS product, cat.category_name
FROM categories cat
JOIN products p ON p.category_id = cat.category_id
JOIN orders o ON o.product_id = p.product_id
JOIN customers c ON c.customer_id = o.customer_id
ORDER BY o.order_id
"""
SQL_LEFT_THEN_INNER = """
SELECT o.order_id, p.name AS product, cat.category_name
FROM orders o
LEFT JOIN products p ON p.product_id = o.product_id
JOIN categories cat ON cat.category_id = p.category_id
ORDER BY o.order_id
"""
SQL_NESTED = """
SELECT o.order_id, p.name AS product, cat.category_name
FROM orders o
LEFT JOIN (products p JOIN categories cat ON cat.category_id = p.category_id)
       ON p.product_id = o.product_id
ORDER BY o.order_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
def show(title, q):
    d = pd.read_sql_query(q, con); print(title, f"({len(d)} rows)"); print(d.to_string(index=False)); print(); return d
left_df = show("All LEFT joins", SQL_MAIN)
inner_df = show("All INNER joins", SQL_INNER)
inner2 = show("Same INNER joins, tables listed in another order", SQL_INNER_REORDERED)
lti = show("LEFT products, then INNER categories", SQL_LEFT_THEN_INNER)
nested = show("LEFT JOIN (products JOIN categories), nested", SQL_NESTED)

customers = pd.read_sql_query("SELECT * FROM customers", con)
products = pd.read_sql_query("SELECT * FROM products", con)
categories = pd.read_sql_query("SELECT * FROM categories", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
print("pandas dtypes: orders.customer_id", orders["customer_id"].dtype, "| products.category_id", products["category_id"].dtype)

# pd:main
pd_df = (orders
         .merge(customers.rename(columns={"name": "customer"})[["customer_id", "customer"]],
                on="customer_id", how="left", validate="many_to_one")
         .merge(products.rename(columns={"name": "product"})[["product_id", "product", "category_id"]],
                on="product_id", how="left", validate="many_to_one")
         .merge(categories, on="category_id", how="left", validate="many_to_one")
         [["order_id", "customer", "product", "category_name"]]
         .sort_values("order_id").reset_index(drop=True))
pd_inner = (orders.merge(customers, on="customer_id", validate="many_to_one")
            .merge(products, on="product_id", suffixes=("_cust", "_prod"), validate="many_to_one")
            .merge(categories, on="category_id", validate="many_to_one"))
# pd:end
print("pandas all-left rows:", len(pd_df), "| pandas all-inner rows:", len(pd_inner))

def norm(d): return d.astype(object).where(d.notna(), "<NULL>").reset_index(drop=True)
# compared after sorting by order_id
pd.testing.assert_frame_equal(norm(left_df), norm(pd_df))
assert list(inner_df["order_id"]) == list(pd_inner.sort_values("order_id")["order_id"]) == [1, 2]
pd.testing.assert_frame_equal(inner_df.reset_index(drop=True), inner2.reset_index(drop=True))
assert len(lti) == 3 and len(nested) == 5
# pandas: LEFT then INNER drops rows; inner first (the nested form) keeps all orders
lp = orders.merge(products, on="product_id", how="left").merge(categories, on="category_id")
pc = products.merge(categories, on="category_id")[["product_id", "name", "category_name"]]
np_ = orders.merge(pc, on="product_id", how="left").sort_values("order_id")
print("pandas LEFT then INNER rows:", len(lp), "| nested (inner first, then LEFT) rows:", len(np_))
assert len(lp) == 3 and len(np_) == 5
print("asserts passed: SQL == pandas; INNER join order does not change the result")
```

**Output (my run):**
```text
All LEFT joins (5 rows)
 order_id customer product category_name
        1     Asha     Pen    Stationery
        2     Asha   Novel         Books
        3      Ben    Lamp           NaN
        4      Ben    Desk           NaN
        5      NaN     Pen    Stationery

All INNER joins (2 rows)
 order_id customer product category_name
        1     Asha     Pen    Stationery
        2     Asha   Novel         Books

Same INNER joins, tables listed in another order (2 rows)
 order_id customer product category_name
        1     Asha     Pen    Stationery
        2     Asha   Novel         Books

LEFT products, then INNER categories (3 rows)
 order_id product category_name
        1     Pen    Stationery
        2   Novel         Books
        5     Pen    Stationery

LEFT JOIN (products JOIN categories), nested (5 rows)
 order_id product category_name
        1     Pen    Stationery
        2   Novel         Books
        3     NaN           NaN
        4     NaN           NaN
        5     Pen    Stationery

pandas dtypes: orders.customer_id float64 | products.category_id float64
pandas all-left rows: 5 | pandas all-inner rows: 2
pandas LEFT then INNER rows: 3 | nested (inner first, then LEFT) rows: 5
asserts passed: SQL == pandas; INNER join order does not change the result
```

**Edge cases:**
- A NULL foreign key (Lamp's category, order 5's customer) and a dangling foreign key (Desk's category 3) both give a NULL on the LEFT JOIN side; only a foreign key constraint would stop the dangling one.
- Duplicate keys in a dimension would multiply orders; each pandas merge uses `validate="many_to_one"` for that reason.
- Name clashes (customers.name, products.name): alias the columns, or in pandas rename or pass `suffixes`.
- In pandas the NULL foreign keys make `customer_id` and `category_id` `float64` after `read_sql`, and merging them with `int64` keys worked in my run.

**Then explain:**
- **INNER joins:** associative and commutative, so the order you write them in does not change the result. I proved it by listing the tables in another order (same 2 rows), and the optimiser is free to pick its own order for cost reasons.
- **LEFT joins:** not freely reorderable. `A LEFT JOIN B` is not the same as `B LEFT JOIN A`, and moving an inner join across an outer join can change the rows (the 3-row versus 5-row result above is the same tables joined in a different nesting).
- **Rule:** once a LEFT JOIN has been used on a path, keep every later join on that path LEFT, or you lose the rows it was there to keep. A WHERE condition on the right-hand table has the same effect (Q3).
- **Optimiser (concept only, not executed here):** for INNER joins it can reorder tables by estimated cost; for outer joins it reorders only when the result is provably identical. Plans are Part 11.

**Follow-ups:**
- *When do you want INNER after LEFT?* When you really want to filter to orders with a category; then say so in a WHERE or use INNER for that reason.
- *Does the written order matter for speed?* Usually not for INNER joins; engines differ (hedged), and SQLite documents some cases where CROSS JOIN fixes the order (from memory).
- *Several dimensions off one fact table?* A star join: LEFT JOIN each dimension to the fact table.

**Common mistakes:**
- Mixing LEFT and INNER joins at random and losing rows without noticing.
- Joining categories through `orders` instead of through `products`.
- Using `SELECT *` over four tables with repeated column names.
- Not comparing the row count with `COUNT(*)` from `orders`.

### Q18 ⭐⭐⭐ 🟡 Join to an aggregated derived table: orders(order_id, customer_id, amount) and customers(customer_id, name, city). Return customers whose total spend is above the average total spend of customers in their own city. Build the per-customer totals as a derived table in FROM, join it to a per-city average derived table, and explain the grain of each side. Give pandas groupby, transform or merge. (No window functions or CTEs.)
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Build a per-customer totals derived table, build a per-city average of those totals from it as a second derived table, join the two on city, and keep customers whose total is strictly above their city's average; the averages must be over customers, not over order rows.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha','Pune'),(2,'Ben','Pune'),(3,'Chitra','Pune'),(4,'Dev','Delhi'),
                             (5,'Esha','Delhi'),(6,'Farah','Mumbai'),(7,'Gopal','Pune');
INSERT INTO orders VALUES (1,1,60),(2,1,40),(3,2,300),(4,3,200),(5,4,50),(6,5,150),(7,6,70);
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
SELECT t.customer_id, t.name, t.city, t.total_spend, a.city_avg
FROM (SELECT c.customer_id, c.name, c.city, SUM(o.amount) AS total_spend
      FROM customers c JOIN orders o ON o.customer_id = c.customer_id
      GROUP BY c.customer_id, c.name, c.city) t
JOIN (SELECT city, AVG(total_spend) AS city_avg
      FROM (SELECT c.customer_id, c.city, SUM(o.amount) AS total_spend
            FROM customers c JOIN orders o ON o.customer_id = c.customer_id
            GROUP BY c.customer_id, c.city) x
      GROUP BY city) a ON a.city = t.city
WHERE t.total_spend > a.city_avg
ORDER BY t.customer_id
```
Grain: `t` has one row per customer (customer total), `a` has one row per city (average of those totals), so the join `a.city = t.city` is many-to-one and adds no rows. The two variants (`SQL_ZERO`, `SQL_WRONG`) are also in the Code block.

**pandas answer:** (also in the Code block; the `transform` alternative is checked there too)
```python
totals = (customers.merge(orders, on="customer_id")
          .groupby(["customer_id", "name", "city"], as_index=False).agg(total_spend=("amount", "sum")))
city_avg = totals.groupby("city", as_index=False).agg(city_avg=("total_spend", "mean"))
joined = totals.merge(city_avg, on="city", validate="many_to_one")
pd_df = (joined[joined["total_spend"] > joined["city_avg"]]
         .sort_values("customer_id").reset_index(drop=True))
```

**Example:** Pune: Asha 60+40 = 100, Ben 300, Chitra 200 (Gopal has no orders). Delhi: Dev 50, Esha 150. Mumbai: Farah 70.
- Pune average of totals = (100 + 300 + 200) / 3 = 200. Ben 300 > 200 yes; Chitra 200 is not strictly above 200; Asha no.
- Delhi average = (50 + 150) / 2 = 100: Esha 150 yes. Mumbai average = 70: Farah is equal, not above.
- Result: Ben and Esha.

**Code:** run with `python3 -I`.
```python
# Q18: customers whose total spend beats the average customer total in their own city (derived tables, no windows/CTEs)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha','Pune'),(2,'Ben','Pune'),(3,'Chitra','Pune'),(4,'Dev','Delhi'),
                             (5,'Esha','Delhi'),(6,'Farah','Mumbai'),(7,'Gopal','Pune');
INSERT INTO orders VALUES (1,1,60),(2,1,40),(3,2,300),(4,3,200),(5,4,50),(6,5,150),(7,6,70);
"""
SQL_MAIN = """
SELECT t.customer_id, t.name, t.city, t.total_spend, a.city_avg
FROM (SELECT c.customer_id, c.name, c.city, SUM(o.amount) AS total_spend
      FROM customers c JOIN orders o ON o.customer_id = c.customer_id
      GROUP BY c.customer_id, c.name, c.city) t
JOIN (SELECT city, AVG(total_spend) AS city_avg
      FROM (SELECT c.customer_id, c.city, SUM(o.amount) AS total_spend
            FROM customers c JOIN orders o ON o.customer_id = c.customer_id
            GROUP BY c.customer_id, c.city) x
      GROUP BY city) a ON a.city = t.city
WHERE t.total_spend > a.city_avg
ORDER BY t.customer_id
"""
# variant: customers with no orders count as 0 in their city's average
SQL_ZERO = """
SELECT t.customer_id, t.name, t.total_spend, a.city_avg
FROM (SELECT c.customer_id, c.name, c.city, COALESCE(SUM(o.amount), 0) AS total_spend
      FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
      GROUP BY c.customer_id, c.name, c.city) t
JOIN (SELECT city, AVG(total_spend) AS city_avg
      FROM (SELECT c.customer_id, c.city, COALESCE(SUM(o.amount), 0) AS total_spend
            FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
            GROUP BY c.customer_id, c.city) x
      GROUP BY city) a ON a.city = t.city
WHERE t.total_spend > a.city_avg
ORDER BY t.customer_id
"""
# wrong: average over ORDER rows per city, not over customer totals
SQL_WRONG = """
SELECT t.customer_id, t.name, t.total_spend, a.avg_order
FROM (SELECT c.customer_id, c.name, c.city, SUM(o.amount) AS total_spend
      FROM customers c JOIN orders o ON o.customer_id = c.customer_id
      GROUP BY c.customer_id, c.name, c.city) t
JOIN (SELECT c.city, AVG(o.amount) AS avg_order
      FROM customers c JOIN orders o ON o.customer_id = c.customer_id GROUP BY c.city) a ON a.city = t.city
WHERE t.total_spend > a.avg_order ORDER BY t.customer_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL main (customers with orders only):"); print(sql_df.to_string(index=False))
print("\nSQL variant, zero-order customers counted as 0:"); print(pd.read_sql_query(SQL_ZERO, con).to_string(index=False))
print("\nWRONG (average over order rows):"); print(pd.read_sql_query(SQL_WRONG, con).to_string(index=False))

customers = pd.read_sql_query("SELECT * FROM customers", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
totals = (customers.merge(orders, on="customer_id")
          .groupby(["customer_id", "name", "city"], as_index=False).agg(total_spend=("amount", "sum")))
city_avg = totals.groupby("city", as_index=False).agg(city_avg=("total_spend", "mean"))
joined = totals.merge(city_avg, on="city", validate="many_to_one")
pd_df = (joined[joined["total_spend"] > joined["city_avg"]]
         .sort_values("customer_id").reset_index(drop=True))
# pd:end
print("\npandas merge version:"); print(pd_df.to_string(index=False))

# transform alternative: no second frame
totals["city_avg"] = totals.groupby("city")["total_spend"].transform("mean")
alt = totals[totals["total_spend"] > totals["city_avg"]].sort_values("customer_id").reset_index(drop=True)
# compared after sorting by customer_id
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
pd.testing.assert_frame_equal(pd_df, alt, check_dtype=False)
assert list(sql_df["name"]) == ["Ben", "Esha"]
print("\nasserts passed: SQL == pandas merge == pandas transform")
```

**Output (my run):**
```text
SQL main (customers with orders only):
 customer_id name  city  total_spend  city_avg
           2  Ben  Pune          300     200.0
           5 Esha Delhi          150     100.0

SQL variant, zero-order customers counted as 0:
 customer_id   name  total_spend  city_avg
           2    Ben          300     150.0
           3 Chitra          200     150.0
           5   Esha          150     100.0

WRONG (average over order rows):
 customer_id   name  total_spend  avg_order
           2    Ben          300      150.0
           3 Chitra          200      150.0
           5   Esha          150      100.0

pandas merge version:
 customer_id name  city  total_spend  city_avg
           2  Ben  Pune          300     200.0
           5 Esha Delhi          150     100.0

asserts passed: SQL == pandas merge == pandas transform
```

**Edge cases:**
- Customers without orders: my main query counts only customers who ordered, because the totals come from an inner join. If they should count as 0 spend, use LEFT JOIN with `COALESCE`. That changes the answer: with Gopal (Pune, no orders) as 0 the Pune average drops to (100+300+200+0)/4 = 150, so Chitra now qualifies (`SQL_ZERO`, in my output). The question text does not say which one is wanted, so say your choice.
- A city with a single customer: the total equals the average, so nobody qualifies.
- Ties with the average are excluded because of `>`; all totals equal means no rows.
- NULL city: `a.city = t.city` never matches NULL, so these customers drop out; handle explicitly if it matters.
- NULL order amounts are ignored by SUM and AVG.

**Then explain:**
- **Grain of each side:** the first derived table is one row per customer; the second is one row per city. Joining a per-customer table to a per-city table on city fans out per customer (many-to-one), not per order.
- **The classic mistake:** averaging order amounts per city, `AVG(o.amount)`, is the average order, not the average customer spend. In my data that wrongly gives Pune 150 and lets Chitra in (`SQL_WRONG`, in my output). Average the customer totals.
- **Why no window function:** the question rules out windows and CTEs; `AVG(SUM(...)) OVER (PARTITION BY city)` is the later-part solution.
- **pandas:** `groupby` gives the per-customer totals, a second `groupby` the per-city mean, and `merge` (or `groupby(...).transform("mean")`) puts the average on each customer row.

**Follow-ups:**
- *What if the comparison should exclude the customer's own spend?* The average of the other customers needs a different computation (sum minus own, divided by count minus one).
- *Median instead of average?* Not a plain aggregate in SQLite; Part 3 onward.
- *Why not a correlated subquery?* It works but recomputes the city average per row (not run here).

**Common mistakes:**
- Averaging raw order rows per city.
- Joining orders directly to customers and comparing without grouping first, so a customer is compared once per order.
- Using `>=` and counting customers exactly at the average.
- Silently dropping customers without orders without saying so.

### Q19 ⭐⭐ 🟢 Joining on multiple columns: sales(store_id, product_id, qty) and prices(store_id, product_id, price), where price varies by store. Write the join on the composite key and show what goes wrong if you join on product_id alone (fan-out across stores, wrong revenue). Give the pandas merge on=['store_id','product_id'] and validate='many_to_one'.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Join on every column that makes up the key, `ON p.store_id = s.store_id AND p.product_id = s.product_id`; joining on product_id alone matches each sale to the price of every store, so rows and revenue are multiplied.

**Schema and sample data:**
```sql
CREATE TABLE sales(store_id INTEGER, product_id INTEGER, qty INTEGER);
CREATE TABLE prices(store_id INTEGER, product_id INTEGER, price INTEGER, PRIMARY KEY(store_id, product_id));
INSERT INTO sales VALUES (1,10,3),(1,20,2),(2,10,5),(2,20,1),(3,10,2);
INSERT INTO prices VALUES (1,10,100),(1,20,50),(2,10,110),(2,20,55);
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
SELECT s.store_id, s.product_id, s.qty, p.price, s.qty * p.price AS revenue
FROM sales s
JOIN prices p ON p.store_id = s.store_id AND p.product_id = s.product_id
ORDER BY s.store_id, s.product_id
```
The broken version (`SQL_WRONG`) joins on `product_id` only and is run in the Code block.

**pandas answer:**
```python
pd_df = sales.merge(prices, on=["store_id", "product_id"], how="inner", validate="many_to_one")
pd_df["revenue"] = pd_df["qty"] * pd_df["price"]
pd_df = pd_df.sort_values(["store_id", "product_id"]).reset_index(drop=True)
```

**Example:** prices: store 1 sells product 10 at 100 and product 20 at 50; store 2 sells 10 at 110 and 20 at 55. Sales: (1,10,3), (1,20,2), (2,10,5), (2,20,1), and (3,10,2) at a store with no price list.
- Correct: 3x100 + 2x50 + 5x110 + 1x55 = 300 + 100 + 550 + 55 = 1005. The store 3 sale has no price row, so an INNER JOIN drops it (a LEFT JOIN would show a NULL price).
- Product-only join: product 10 has 3 sales rows, each matched to 2 prices = 6 rows; product 20 has 2 sales rows x 2 prices = 4 rows. 10 rows, and revenue = 10 units x (100+110) + 3 units x (50+55) = 2100 + 315 = 2415, more than double the right answer.

**Code:** run with `python3 -I`.
```python
# Q19: joining on a composite key (store_id, product_id); what a product_id-only join does
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE sales(store_id INTEGER, product_id INTEGER, qty INTEGER);
CREATE TABLE prices(store_id INTEGER, product_id INTEGER, price INTEGER, PRIMARY KEY(store_id, product_id));
INSERT INTO sales VALUES (1,10,3),(1,20,2),(2,10,5),(2,20,1),(3,10,2);
INSERT INTO prices VALUES (1,10,100),(1,20,50),(2,10,110),(2,20,55);
"""
SQL_MAIN = """
SELECT s.store_id, s.product_id, s.qty, p.price, s.qty * p.price AS revenue
FROM sales s
JOIN prices p ON p.store_id = s.store_id AND p.product_id = s.product_id
ORDER BY s.store_id, s.product_id
"""
SQL_WRONG = """
SELECT COUNT(*) AS joined_rows, SUM(s.qty * p.price) AS revenue
FROM sales s JOIN prices p ON p.product_id = s.product_id
"""
SQL_RIGHT_TOTAL = "SELECT SUM(s.qty * p.price) FROM sales s JOIN prices p ON p.store_id = s.store_id AND p.product_id = s.product_id"
SQL_LEFT = """
SELECT s.store_id, s.product_id, s.qty, p.price FROM sales s
LEFT JOIN prices p ON p.store_id = s.store_id AND p.product_id = s.product_id
WHERE p.price IS NULL
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print(sql_df.to_string(index=False))
print("\ncorrect revenue:", con.execute(SQL_RIGHT_TOTAL).fetchone()[0])
print("product_id-only join (joined_rows, revenue):", con.execute(SQL_WRONG).fetchone())
print("sales rows with no price for their store:", con.execute(SQL_LEFT).fetchall())

sales = pd.read_sql_query("SELECT * FROM sales", con)
prices = pd.read_sql_query("SELECT * FROM prices", con)
# pd:main
pd_df = sales.merge(prices, on=["store_id", "product_id"], how="inner", validate="many_to_one")
pd_df["revenue"] = pd_df["qty"] * pd_df["price"]
pd_df = pd_df.sort_values(["store_id", "product_id"]).reset_index(drop=True)
# pd:end
print("\npandas revenue:", pd_df["revenue"].sum())
bad = sales.merge(prices, on="product_id", suffixes=("_sale", "_price"))
print("pandas product_id-only merge rows:", len(bad), "revenue:", (bad["qty"] * bad["price"]).sum())
try:
    sales.merge(prices, on="product_id", validate="many_to_one")
except Exception as e:
    print("validate on product_id alone ->", type(e).__name__ + ":", e)
left = sales.merge(prices, on=["store_id", "product_id"], how="left", indicator=True)
print("unmatched sales (indicator left_only):", left.loc[left["_merge"] == "left_only", ["store_id", "product_id"]].values.tolist())

# compared after sorting by store_id, product_id
pd.testing.assert_frame_equal(sql_df, pd_df[sql_df.columns], check_dtype=False)
assert pd_df["revenue"].sum() == 1005
print("asserts passed: SQL == pandas")
```

**Output (my run):**
```text
 store_id  product_id  qty  price  revenue
        1          10    3    100      300
        1          20    2     50      100
        2          10    5    110      550
        2          20    1     55       55

correct revenue: 1005
product_id-only join (joined_rows, revenue): (10, 2415)
sales rows with no price for their store: [(3, 10, 2, None)]

pandas revenue: 1005
pandas product_id-only merge rows: 10 revenue: 2415
validate on product_id alone -> MergeError: Merge keys are not unique in right dataset; not a many-to-one merge

Duplicates in right:
  product_id
         10
         20 ...
unmatched sales (indicator left_only): [[3, 10]]
asserts passed: SQL == pandas
```

**Edge cases:**
- A sale for a store with no price (store 3): INNER drops it, LEFT keeps it with a NULL price, and `qty * price` becomes NULL and is ignored by SUM. Find these with `WHERE p.price IS NULL` (SQL) or `indicator=True` (pandas) rather than letting revenue quietly shrink.
- A NULL in either key column never matches (NULL is not equal to anything).
- If `prices` had two rows for the same store and product, even the composite join would fan out; a PRIMARY KEY on (store_id, product_id) prevents it, and `validate="many_to_one"` checks it in pandas.
- Column order in a composite key does not matter, but the pair must be complete.

**Then explain:**
- **Composite key:** the unit of uniqueness in `prices` is the pair (store, product), so the join must use the pair. product_id alone is not unique in `prices`.
- **What goes wrong:** the join silently returns the cartesian product of sales and prices per product (10 rows instead of 5, matches 2 prices per sale); nothing errors.
- **pandas:** `on=["store_id", "product_id"]` with `validate="many_to_one"`. When I merged on `product_id` alone with `validate="many_to_one"`, pandas raised `MergeError: Merge keys are not unique in right dataset; not a many-to-one merge` (exact text in the output). Without `validate` it silently returned 10 rows and revenue 2415, the same wrong numbers as SQL.
- **Habit:** compare the row count after the join with the row count of the left table.

**Follow-ups:**
- *Why many_to_one and not one_to_one?* Many sales rows can share one store-product price; the price side must be unique.
- *Composite key with a date range?* That is a range join, covered later in this part (Q26).
- *Would an index help?* A composite index on both key columns, concept only (Part 11).

**Common mistakes:**
- Joining on the "obvious" single column because the other column name seems redundant.
- Never comparing the joined row count with the left table.
- Counting revenue after a fan-out join without checking the total.
- Dropping store 3 sales silently through an INNER JOIN.

### Q20 ⭐⭐ 🟢 USING versus ON: employees(emp_id, name, dept_id) and departments(dept_id, dept_name). Show both forms, what SELECT * returns for each (one dept_id column versus two), how USING behaves in outer joins and with qualified column names (hedge by engine: PostgreSQL, MySQL and SQLite differ in details), when ON is required (different column names, extra conditions), and the pandas parallels (on versus left_on/right_on).
**Asked at:** DataCamp and InterviewBit SQL joins interview guides, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** `USING (dept_id)` is shorthand for an equality join on a column that has the same name in both tables and returns that column once; `ON` is the general form that works with any condition, different names and extra predicates, and `SELECT *` returns the key twice.

**Schema and sample data:**
```sql
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER);
INSERT INTO departments VALUES (10,'Sales'),(20,'Tech'),(30,'HR');
INSERT INTO employees VALUES (1,'Asha',10),(2,'Ben',20),(3,'Chitra',99),(4,'Dev',NULL);
```

**SQL answer:** both forms, executed in the Code block (the queries are in its `Q` dictionary):
```sql
SELECT * FROM employees e JOIN departments d ON e.dept_id = d.dept_id ORDER BY emp_id;
SELECT * FROM employees e JOIN departments d USING (dept_id) ORDER BY emp_id;
```
The other `Q` entries cover LEFT, RIGHT and FULL joins with USING, FULL with ON, and qualified or unqualified names.

**pandas answer:**
```python
p_on = employees.merge(departments, on="dept_id", how="left")                                   # like USING: one key column
p_lr = employees.merge(departments, left_on="dept_id", right_on="dept_id", how="left")           # same, spelled with left_on/right_on
d2 = departments.rename(columns={"dept_id": "id"})
p_names = employees.merge(d2, left_on="dept_id", right_on="id", how="left")                      # like ON with different names: two key columns
```

**Example:** employees Asha (10), Ben (20), Chitra (99, no such department), Dev (NULL); departments 10 Sales, 20 Tech, 30 HR.
- Inner join with ON, `SELECT *`: Asha and Ben, 5 columns: emp_id, name, dept_id, dept_id, dept_name (the key appears twice). With USING: the same two rows and 4 columns, one dept_id.
- LEFT JOIN USING: also Chitra and Dev with a NULL dept_name. RIGHT JOIN USING: Asha, Ben and the HR department (no employees).
- FULL JOIN: with USING, the HR row has dept_id 30 filled in (SQLite coalesces the key); with ON the same row has two columns, `e.dept_id` NULL and `d.dept_id` 30. Chitra (99) and Dev (NULL) are in both.

**Code:** run with `python3 -I`.
```python
# Q20: USING versus ON
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER);
INSERT INTO departments VALUES (10,'Sales'),(20,'Tech'),(30,'HR');
INSERT INTO employees VALUES (1,'Asha',10),(2,'Ben',20),(3,'Chitra',99),(4,'Dev',NULL);
"""
Q = {
 "on_star":    "SELECT * FROM employees e JOIN departments d ON e.dept_id = d.dept_id ORDER BY emp_id",
 "using_star": "SELECT * FROM employees e JOIN departments d USING (dept_id) ORDER BY emp_id",
 "left_using": "SELECT * FROM employees e LEFT JOIN departments d USING (dept_id) ORDER BY emp_id",
 "right_using": "SELECT * FROM employees e RIGHT JOIN departments d USING (dept_id) ORDER BY dept_id, emp_id",
 "full_using": "SELECT * FROM employees e FULL JOIN departments d USING (dept_id) ORDER BY dept_id, emp_id",
 "full_on":    "SELECT * FROM employees e FULL JOIN departments d ON e.dept_id = d.dept_id ORDER BY d.dept_id, emp_id",
 "using_qualified": "SELECT e.dept_id, d.dept_id AS d_dept, emp_id FROM employees e JOIN departments d USING (dept_id) ORDER BY emp_id",
 "using_unqualified": "SELECT dept_id, name, dept_name FROM employees e JOIN departments d USING (dept_id) ORDER BY emp_id",
}
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
res = {}
for k, q in Q.items():
    cur = con.execute(q)
    cols = [c[0] for c in cur.description]
    res[k] = (cols, cur.fetchall())
    print(f"{k}: columns {cols}")
    for r in res[k][1]: print("   ", r)
# the ON form returns two dept_id columns, the USING form one
assert res["on_star"][0].count("dept_id") == 2 and res["using_star"][0].count("dept_id") == 1

employees = pd.read_sql_query("SELECT * FROM employees", con)
departments = pd.read_sql_query("SELECT * FROM departments", con)
# pd:main
p_on = employees.merge(departments, on="dept_id", how="left")                                   # like USING: one key column
p_lr = employees.merge(departments, left_on="dept_id", right_on="dept_id", how="left")           # same, spelled with left_on/right_on
d2 = departments.rename(columns={"dept_id": "id"})
p_names = employees.merge(d2, left_on="dept_id", right_on="id", how="left")                      # like ON with different names: two key columns
# pd:end
print("\npandas on='dept_id' columns:", list(p_on.columns))
print("pandas left_on/right_on, different names:", list(p_names.columns))
print("pandas on= with how='outer':")
print(employees.merge(departments, on="dept_id", how="outer").sort_values(["dept_id", "emp_id"]).to_string(index=False))

# USING result (LEFT) equals pandas on= result, compared after sorting by emp_id and reordering columns by name
sql_left = pd.DataFrame(res["left_using"][1], columns=res["left_using"][0])
cols = ["emp_id", "name", "dept_id", "dept_name"]
a = sql_left[cols].sort_values("emp_id").reset_index(drop=True)
b = p_on[cols].sort_values("emp_id").reset_index(drop=True)
pd.testing.assert_frame_equal(a.astype(object).where(a.notna(), None), b.astype(object).where(b.notna(), None), check_dtype=False)
pd.testing.assert_frame_equal(p_on, p_lr)
print("\nasserts passed: SQL LEFT JOIN USING == pandas merge on=; on= == left_on/right_on with the same name")
```

**Output (my run):**
```text
on_star: columns ['emp_id', 'name', 'dept_id', 'dept_id', 'dept_name']
    (1, 'Asha', 10, 10, 'Sales')
    (2, 'Ben', 20, 20, 'Tech')
using_star: columns ['emp_id', 'name', 'dept_id', 'dept_name']
    (1, 'Asha', 10, 'Sales')
    (2, 'Ben', 20, 'Tech')
left_using: columns ['emp_id', 'name', 'dept_id', 'dept_name']
    (1, 'Asha', 10, 'Sales')
    (2, 'Ben', 20, 'Tech')
    (3, 'Chitra', 99, None)
    (4, 'Dev', None, None)
right_using: columns ['emp_id', 'name', 'dept_id', 'dept_name']
    (1, 'Asha', 10, 'Sales')
    (2, 'Ben', 20, 'Tech')
    (None, None, 30, 'HR')
full_using: columns ['emp_id', 'name', 'dept_id', 'dept_name']
    (4, 'Dev', None, None)
    (1, 'Asha', 10, 'Sales')
    (2, 'Ben', 20, 'Tech')
    (None, None, 30, 'HR')
    (3, 'Chitra', 99, None)
full_on: columns ['emp_id', 'name', 'dept_id', 'dept_id', 'dept_name']
    (3, 'Chitra', 99, None, None)
    (4, 'Dev', None, None, None)
    (1, 'Asha', 10, 10, 'Sales')
    (2, 'Ben', 20, 20, 'Tech')
    (None, None, None, 30, 'HR')
using_qualified: columns ['dept_id', 'd_dept', 'emp_id']
    (10, 10, 1)
    (20, 20, 2)
using_unqualified: columns ['dept_id', 'name', 'dept_name']
    (10, 'Asha', 'Sales')
    (20, 'Ben', 'Tech')

pandas on='dept_id' columns: ['emp_id', 'name', 'dept_id', 'dept_name']
pandas left_on/right_on, different names: ['emp_id', 'name', 'dept_id', 'id', 'dept_name']
pandas on= with how='outer':
 emp_id   name  dept_id dept_name
    1.0   Asha     10.0     Sales
    2.0    Ben     20.0      Tech
    NaN    NaN     30.0        HR
    3.0 Chitra     99.0       NaN
    4.0    Dev      NaN       NaN

asserts passed: SQL LEFT JOIN USING == pandas merge on=; on= == left_on/right_on with the same name
```

**Edge cases:**
- Qualified names: in my SQLite run `e.dept_id` and `d.dept_id` were both accepted after `USING`, and the unqualified `dept_id` worked too. This is engine specific: from memory PostgreSQL and MySQL accept the unqualified name, and some engines (older Oracle) reject a qualified name for a USING column; not executed here, check the manual.
- Column order of `SELECT *`: SQLite kept `dept_id` in the left table's position (emp_id, name, dept_id, dept_name). The SQL standard and, I recall, the MySQL and PostgreSQL documentation put the join columns first; not executed here, so do not rely on the order, name your columns.
- Different column names (`departments.id`), extra conditions (`AND d.active = 1`), non-equality joins and expressions need `ON`.
- NULL keys do not match in either form (Dev stays unmatched).
- USING with more than one column is allowed: `USING (store_id, product_id)`.

**Then explain:**
- **One column versus two:** `SELECT *` with USING returns the join column once; with ON it returns both copies. After an outer join the single USING column holds the key from whichever side has it, which is the coalesced key from Q16 for free (seen in my FULL JOIN USING output).
- **When ON is required:** different names, more than an equality, or a condition that is not just equality of same-named columns.
- **Risk of USING:** it depends on names, so renaming a column or adding a second same-named column changes behaviour less than NATURAL JOIN (Q21) but still ties the query to naming conventions.
- **pandas parallels:** `on="dept_id"` is USING (one key column in the result); `left_on`/`right_on` with different names is ON and keeps both key columns (`dept_id` and `id` in my run). With the same name in `left_on` and `right_on` the result equals `on=` (my assert).
- **Outer merge in pandas:** `on=` with `how="outer"` gives one key column holding the keys of both sides, like USING.

**Follow-ups:**
- *Is USING faster?* No; it is syntax (not executed on other engines, concept only).
- *Which one do you write at work?* ON for clarity and safety, USING only for conventional shared key names.
- *What does NATURAL JOIN do?* USING over every common column (Q21).

**Common mistakes:**
- Assuming `SELECT *` shows one key column in an ON join.
- Qualifying the USING column in an engine that rejects it.
- Using USING when the key names differ or when extra conditions are needed.
- Expecting `merge(on=...)` to keep two key columns.

### Q21 ⭐⭐ 🟢 NATURAL JOIN and why many teams ban it: employees(emp_id, name, dept_id, updated_at) and departments(dept_id, dept_name, updated_at). Explain what NATURAL JOIN joins on, how an extra common column (updated_at) silently changes the result to zero rows, and what happens after a schema change adds a column. Contrast with explicit ON.
**Asked at:** DataCamp and InterviewBit SQL joins interview guides, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** NATURAL JOIN joins on every column name the two tables share, with no say from you, so an extra shared column like `updated_at` becomes part of the key and the result quietly shrinks (often to zero rows), and a later schema change can change it again; write an explicit ON.

**Schema and sample data:**
```sql
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT, updated_at TEXT);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, updated_at TEXT);
INSERT INTO departments VALUES (10,'Sales','2026-01-05'),(20,'Tech','2026-01-06');
INSERT INTO employees VALUES (1,'Asha',10,'2026-03-01'),(2,'Ben',20,'2026-03-02'),(3,'Chitra',20,'2026-01-06');
```

**SQL answer:** both queries run in the Code block.
```sql
SELECT * FROM employees NATURAL JOIN departments ORDER BY emp_id
```
```sql
SELECT e.emp_id, e.name, e.dept_id, d.dept_name
FROM employees e JOIN departments d ON d.dept_id = e.dept_id ORDER BY e.emp_id
```

**pandas answer:** `merge` with no `on=` is a natural join too; the explicit version names the key.
```python
p_default = employees.merge(departments)                                           # no on=: joins on ALL common columns
p_explicit = employees.merge(departments[["dept_id", "dept_name"]], on="dept_id", validate="many_to_one")
```

**Example:** employees Asha (dept 10, updated 2026-03-01), Ben (20, 2026-03-02), Chitra (20, 2026-01-06); departments 10 Sales (2026-01-05), 20 Tech (2026-01-06).
- Common columns: `dept_id` and `updated_at`. NATURAL JOIN therefore means `dept_id` equal AND `updated_at` equal.
- Asha: dept 10 matches, but 2026-03-01 differs from 2026-01-05, so no row. Ben: 2026-03-02 differs from 2026-01-06, no row. Chitra: dept 20 and 2026-01-06 equal, so she matches.
- Result: 1 row (Chitra), while the explicit ON on dept_id alone gives 3. In practice timestamps rarely match at all, which gives zero rows; my sample has one coincidence on purpose, to show the wrong answer can look plausible.
- Schema change: after adding a `name` column to departments (it also exists in employees), the NATURAL JOIN returned 0 rows, while the ON query still returned 3.

**Code:** run with `python3 -I`.
```python
# Q21: NATURAL JOIN joins on every same-named column; updated_at silently breaks it
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT, updated_at TEXT);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, updated_at TEXT);
INSERT INTO departments VALUES (10,'Sales','2026-01-05'),(20,'Tech','2026-01-06');
INSERT INTO employees VALUES (1,'Asha',10,'2026-03-01'),(2,'Ben',20,'2026-03-02'),(3,'Chitra',20,'2026-01-06');
"""
SQL_NATURAL = "SELECT * FROM employees NATURAL JOIN departments ORDER BY emp_id"
SQL_ON = """
SELECT e.emp_id, e.name, e.dept_id, d.dept_name
FROM employees e JOIN departments d ON d.dept_id = e.dept_id ORDER BY e.emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
def run(q):
    cur = con.execute(q); return [c[0] for c in cur.description], cur.fetchall()
cols, rows = run(SQL_NATURAL)
print("NATURAL JOIN columns:", cols); print("rows:", rows)
cols, rows = run(SQL_ON)
print("\nexplicit ON rows:", len(rows)); [print("   ", r) for r in rows]

# a schema change adds a second common column (name) to departments
con.execute("ALTER TABLE departments ADD COLUMN name TEXT")
con.execute("UPDATE departments SET name = 'HQ'")
print("\nafter ALTER TABLE departments ADD COLUMN name -> NATURAL JOIN rows:", len(run(SQL_NATURAL)[1]))
print("explicit ON rows after the same change:", len(run(SQL_ON)[1]))
con.execute("ALTER TABLE departments DROP COLUMN name")

# no common column at all: NATURAL JOIN turns into a cross join
con.executescript("CREATE TABLE tags(tag TEXT); INSERT INTO tags VALUES ('x'),('y');")
print("\nemployees NATURAL JOIN tags (no common column) rows:", len(run("SELECT * FROM employees NATURAL JOIN tags")[1]), "= 3 x 2")

employees = pd.read_sql_query("SELECT * FROM employees", con)
departments = pd.read_sql_query("SELECT * FROM departments", con)
# pd:main
p_default = employees.merge(departments)                                           # no on=: joins on ALL common columns
p_explicit = employees.merge(departments[["dept_id", "dept_name"]], on="dept_id", validate="many_to_one")
# pd:end
print("\npandas merge() with no on= uses common columns:", sorted(set(employees.columns) & set(departments.columns)))
print("pandas default merge rows:", len(p_default), "| explicit on='dept_id' rows:", len(p_explicit))
try:
    employees[["emp_id", "name"]].merge(pd.DataFrame({"tag": ["x", "y"]}))
except Exception as e:
    print("no common columns ->", type(e).__name__ + ":", e)

# SQL: natural -> 1 row (only Chitra, whose updated_at matches); explicit ON -> 3 rows
nat_rows = run(SQL_NATURAL)[1]
assert len(nat_rows) == 1 and nat_rows[0][1] == "Chitra"
assert len(run(SQL_ON)[1]) == 3
# the pandas default merge behaves like NATURAL JOIN (same single row); compared after sorting by emp_id
assert p_default["name"].tolist() == [r[1] for r in nat_rows]
sql_on = pd.DataFrame(run(SQL_ON)[1], columns=run(SQL_ON)[0])
pd.testing.assert_frame_equal(sql_on, p_explicit.sort_values("emp_id").reset_index(drop=True)[sql_on.columns], check_dtype=False)
print("asserts passed: NATURAL JOIN == pandas default merge (1 row); explicit ON == pandas on='dept_id' (3 rows)")
```

**Output (my run):**
```text
NATURAL JOIN columns: ['emp_id', 'name', 'dept_id', 'updated_at', 'dept_name']
rows: [(3, 'Chitra', 20, '2026-01-06', 'Tech')]

explicit ON rows: 3
    (1, 'Asha', 10, 'Sales')
    (2, 'Ben', 20, 'Tech')
    (3, 'Chitra', 20, 'Tech')

after ALTER TABLE departments ADD COLUMN name -> NATURAL JOIN rows: 0
explicit ON rows after the same change: 3

employees NATURAL JOIN tags (no common column) rows: 6 = 3 x 2

pandas merge() with no on= uses common columns: ['dept_id', 'updated_at']
pandas default merge rows: 1 | explicit on='dept_id' rows: 3
no common columns -> MergeError: No common columns to perform merge on. Merge options: left_on=None, right_on=None, left_index=False, right_index=False
asserts passed: NATURAL JOIN == pandas default merge (1 row); explicit ON == pandas on='dept_id' (3 rows)
```

**Edge cases:**
- Two tables with no common column: NATURAL JOIN becomes a cross join (3 x 2 = 6 rows in my run).
- Columns that are common by accident (`updated_at`, `created_at`, `id`, `name`, `status`) are the usual cause.
- Dropping a column can also widen the result or turn a join into a cross join.
- `SELECT *` with NATURAL JOIN shows each common column once (`dept_id` and `updated_at` once in my output).
- NULL values in the common columns never match, as with any equality.

**Then explain:**
- **What it does:** joins on all same-named columns, as if you wrote USING on all of them.
- **Why teams ban it:** the join key is implicit and can change when someone adds a column to either table, with no error and no warning; code review cannot see the join condition.
- **pandas has the same trap:** `employees.merge(departments)` with no `on=` joins on the intersection of column names (`dept_id`, `updated_at`) and returned the same single row (my run). With no common column at all, pandas raises `MergeError: No common columns to perform merge on` rather than making a cross join.
- **Support (not executed here):** from memory PostgreSQL, MySQL and Oracle support NATURAL JOIN and SQL Server does not; check the manual.
- **Fix:** an explicit ON on the key you mean, and rename audit columns (`emp_updated_at`) to avoid clashes.

**Follow-ups:**
- *Is NATURAL JOIN ever fine?* In a one-off exploration of tables whose columns you know, but not in saved code.
- *What about USING?* Safer than NATURAL, because you name the columns (Q20).
- *Natural outer joins?* `NATURAL LEFT JOIN` exists with the same implicit key.

**Common mistakes:**
- Not noticing that `updated_at` or `id` is a shared column.
- Reading a plausible-looking one-row result as correct.
- Calling `merge` in pandas without `on=` and trusting the guess.
- Renaming or adding a column without searching for NATURAL JOIN users.

### Q22 ⭐⭐ 🟢 One-level hierarchy: employees(emp_id, name, manager_id). List each employee with the manager's name (the top person shows NULL, so use LEFT JOIN), and then managers with at least 5 direct reports (self join plus GROUP BY ... HAVING, the LeetCode Managers with at Least 5 Direct Reports idea). Explain why an INNER JOIN drops the top person and why multi-level chains need recursion (Part 9). Give pandas.
**Asked at:** public LeetCode-style problem bank (SQL 50 join problems, known only from repo snippets), not a candidate report; analyst and data scientist screens
**Say this first (1 line):** Self join employees to itself with `e.manager_id = m.emp_id`, using a LEFT JOIN so the top person (NULL manager) still shows up; for managers with at least 5 reports, join, group by the manager and use HAVING COUNT(*) >= 5.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER);
INSERT INTO employees VALUES
 (1,'Zara',NULL),(2,'Ben',1),(3,'Chitra',1),(4,'Dev',1),(5,'Esha',1),(6,'Farah',1),
 (7,'Gopal',2),(8,'Hari',2),(9,'Ira',3),(10,'Jay',2);
```

**SQL answer:** manager names (`SQL_NAMES`) and managers with at least 5 direct reports (`SQL_MAIN`), both in the Code block.
```sql
SELECT e.emp_id, e.name, m.name AS manager_name
FROM employees e LEFT JOIN employees m ON m.emp_id = e.manager_id
ORDER BY e.emp_id
```
```sql
SELECT m.emp_id, m.name, COUNT(*) AS direct_reports
FROM employees e
JOIN employees m ON m.emp_id = e.manager_id
GROUP BY m.emp_id, m.name
HAVING COUNT(*) >= 5
ORDER BY m.emp_id
```

**pandas answer:**
```python
names_pd = (emp.merge(emp[["emp_id", "name"]], left_on="manager_id", right_on="emp_id",
                      how="left", suffixes=("", "_mgr"), validate="many_to_one")
            .rename(columns={"name_mgr": "manager_name"})[["emp_id", "name", "manager_name"]]
            .sort_values("emp_id").reset_index(drop=True))
pairs = emp.merge(emp[["emp_id", "name"]], left_on="manager_id", right_on="emp_id", suffixes=("", "_mgr"))
counts = (pairs.groupby(["emp_id_mgr", "name_mgr"], as_index=False).size()
          .rename(columns={"emp_id_mgr": "emp_id", "name_mgr": "name", "size": "direct_reports"}))
pd_df = counts[counts["direct_reports"] >= 5].sort_values("emp_id").reset_index(drop=True)
```

**Example:** 10 employees. Zara (1) has no manager. Reports: Zara has 5 (Ben, Chitra, Dev, Esha, Farah), Ben has 3 (Gopal, Hari, Jay), Chitra has 1 (Ira).
- With LEFT JOIN: 10 rows; Zara's manager_name is NULL.
- With INNER JOIN: 9 rows, Zara disappears because her manager_id NULL matches no emp_id.
- Group by manager: Zara 5, Ben 3, Chitra 1. HAVING COUNT(*) >= 5 keeps only Zara.

**Code:** run with `python3 -I`.
```python
# Q22: one-level hierarchy: manager names, and managers with at least 5 direct reports
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER);
INSERT INTO employees VALUES
 (1,'Zara',NULL),(2,'Ben',1),(3,'Chitra',1),(4,'Dev',1),(5,'Esha',1),(6,'Farah',1),
 (7,'Gopal',2),(8,'Hari',2),(9,'Ira',3),(10,'Jay',2);
"""
SQL_NAMES = """
SELECT e.emp_id, e.name, m.name AS manager_name
FROM employees e LEFT JOIN employees m ON m.emp_id = e.manager_id
ORDER BY e.emp_id
"""
SQL_INNER = "SELECT COUNT(*) FROM employees e JOIN employees m ON m.emp_id = e.manager_id"
SQL_MAIN = """
SELECT m.emp_id, m.name, COUNT(*) AS direct_reports
FROM employees e
JOIN employees m ON m.emp_id = e.manager_id
GROUP BY m.emp_id, m.name
HAVING COUNT(*) >= 5
ORDER BY m.emp_id
"""
SQL_COUNTS = """
SELECT m.emp_id, m.name, COUNT(*) AS direct_reports
FROM employees e JOIN employees m ON m.emp_id = e.manager_id
GROUP BY m.emp_id, m.name ORDER BY m.emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
names_df = pd.read_sql_query(SQL_NAMES, con)
print(names_df.to_string(index=False))
print("\nINNER JOIN rows:", con.execute(SQL_INNER).fetchone()[0], "of 10 employees (Zara dropped)")
print("\nreports per manager:"); print(pd.read_sql_query(SQL_COUNTS, con).to_string(index=False))
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("\nmanagers with >= 5 direct reports:"); print(sql_df.to_string(index=False))

emp = pd.read_sql_query("SELECT * FROM employees", con)
print("\nmanager_id dtype in pandas:", emp["manager_id"].dtype)
# pd:main
names_pd = (emp.merge(emp[["emp_id", "name"]], left_on="manager_id", right_on="emp_id",
                      how="left", suffixes=("", "_mgr"), validate="many_to_one")
            .rename(columns={"name_mgr": "manager_name"})[["emp_id", "name", "manager_name"]]
            .sort_values("emp_id").reset_index(drop=True))
pairs = emp.merge(emp[["emp_id", "name"]], left_on="manager_id", right_on="emp_id", suffixes=("", "_mgr"))
counts = (pairs.groupby(["emp_id_mgr", "name_mgr"], as_index=False).size()
          .rename(columns={"emp_id_mgr": "emp_id", "name_mgr": "name", "size": "direct_reports"}))
pd_df = counts[counts["direct_reports"] >= 5].sort_values("emp_id").reset_index(drop=True)
# pd:end
print("pandas result:"); print(pd_df.to_string(index=False))
print("pandas inner merge rows:", len(pairs))

def norm(d): return d.astype(object).where(d.notna(), None).reset_index(drop=True)
# compared after sorting by emp_id
pd.testing.assert_frame_equal(norm(names_df), norm(names_pd), check_dtype=False)
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
assert list(sql_df["name"]) == ["Zara"] and pd.isna(names_df.loc[0, "manager_name"])
print("asserts passed: SQL == pandas for both parts")
```

**Output (my run):**
```text
 emp_id   name manager_name
      1   Zara          NaN
      2    Ben         Zara
      3 Chitra         Zara
      4    Dev         Zara
      5   Esha         Zara
      6  Farah         Zara
      7  Gopal          Ben
      8   Hari          Ben
      9    Ira       Chitra
     10    Jay          Ben

INNER JOIN rows: 9 of 10 employees (Zara dropped)

reports per manager:
 emp_id   name  direct_reports
      1   Zara               5
      2    Ben               3
      3 Chitra               1

managers with >= 5 direct reports:
 emp_id name  direct_reports
      1 Zara               5

manager_id dtype in pandas: float64
pandas result:
 emp_id name  direct_reports
      1 Zara               5
pandas inner merge rows: 9
asserts passed: SQL == pandas for both parts
```

**Edge cases:**
- Employee with a NULL manager: appears with a NULL manager name under LEFT JOIN, never under INNER JOIN.
- Managers with no reports (leaf employees) never show up in the count, which is right: `HAVING COUNT(*) >= 5` cannot be satisfied by 0 rows.
- Group by id and name, not just name, since two managers can share a name.
- A manager_id that points to a deleted employee is dropped by the INNER JOIN (and has a NULL name under a LEFT JOIN); a foreign key would prevent it.
- In pandas `manager_id` is `float64` because of the NaN; merging it with the integer `emp_id` worked, and the NaN key matched nothing.
- The threshold is inclusive ("at least 5"): `>= 5`, not `> 5`.

**Then explain:**
- **The two aliases:** `e` is the employee, `m` is the same table read as the manager; the join condition links the employee's `manager_id` to the manager's `emp_id`.
- **Why INNER drops the top person:** a NULL `manager_id` equals nothing, so Zara has no partner row. LEFT JOIN keeps every employee and fills the manager columns with NULL.
- **Counting:** in the group query the join already restricts to employees who have a manager; each such row is one direct report of the grouped manager.
- **Multi-level chains:** one self join gives one level only (employee to manager). Manager's manager needs another join, and an unknown depth needs a recursive CTE (Part 9).
- **pandas:** `merge(left_on="manager_id", right_on="emp_id", suffixes=...)` for the names, then `groupby().size()` and a filter.

**Follow-ups:**
- *Can you do the count without a self join?* Yes: `GROUP BY manager_id HAVING COUNT(*) >= 5` on the employees table, then join once for the name (not run here).
- *Employees with no manager listed explicitly?* `WHERE manager_id IS NULL` on employees.
- *Number of reports for everyone, including zero?* LEFT JOIN from managers to employees and `COUNT(e.emp_id)`.

**Common mistakes:**
- INNER JOIN for the names, losing the top person.
- `HAVING COUNT(*) > 5` for "at least 5".
- Selecting the name without it being in the GROUP BY (SQLite accepts bare columns; strict engines reject it, not run here).
- Joining on `e.emp_id = m.manager_id`, which reverses who is the manager.

### Q23 ⭐⭐ 🟢 pandas join versus merge versus concat: left has index customer_id and columns name, city; right has index customer_id and column segment. Show left.join(right), pd.merge with left_index/right_index, and pd.concat(axis=1) side by side, explain which aligns on the index, the default how of each (join left, merge inner, concat outer), what concat does with duplicate index labels, and when to reset_index first.
**Asked at:** pandas user guide (merge, join, concatenate) and Comparison with SQL, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** All three align on the index, but with different defaults: `left.join(right)` is a left join, `pd.merge(..., left_index=True, right_index=True)` is an inner join, and `pd.concat([left, right], axis=1)` is an outer join; `concat(axis=1)` raises on duplicate labels when it has to reindex, so reset_index and merge when the key repeats.

**Schema and sample data:** (the pandas frames are built from these tables, with `customer_id` as the index; the SQL equivalents are LEFT, INNER and FULL JOIN)
```sql
CREATE TABLE left_t(customer_id INTEGER, name TEXT, city TEXT);
CREATE TABLE right_t(customer_id INTEGER, segment TEXT);
INSERT INTO left_t VALUES (1,'Asha','Pune'),(2,'Ben','Delhi'),(3,'Chitra','Mumbai');
INSERT INTO right_t VALUES (2,'gold'),(3,'silver'),(4,'bronze');
```

**SQL answer:** the three queries below are in the Code block, executed on SQLite 3.45.1: `join` is `SQL_LEFT`, `merge` is `SQL_INNER`, `concat(axis=1)` is `SQL_FULL`.
```sql
SELECT l.customer_id, l.name, l.city, r.segment FROM left_t l LEFT JOIN right_t r ON r.customer_id = l.customer_id ORDER BY 1
```
```sql
SELECT l.customer_id, l.name, l.city, r.segment FROM left_t l JOIN right_t r ON r.customer_id = l.customer_id ORDER BY 1
```
```sql
SELECT COALESCE(l.customer_id, r.customer_id) AS customer_id, l.name, l.city, r.segment
FROM left_t l FULL JOIN right_t r ON r.customer_id = l.customer_id ORDER BY 1
```

**pandas answer:**
```python
joined = left.join(right)                                                   # default how='left', aligns on index
merged = pd.merge(left, right, left_index=True, right_index=True)           # default how='inner'
stacked = pd.concat([left, right], axis=1)                                  # default join='outer', aligns on index
```

**Example:** left has customers 1, 2, 3; right has 2, 3, 4.
- `left.join(right)`: all left rows, so 1, 2, 3; customer 1 has NaN segment.
- `merge` with both indexes: only keys on both sides, 2 and 3.
- `concat(axis=1)`: the union of the indexes, 1, 2, 3, 4; customer 4 has NaN name and city.
- Counts: 3, 2 and 4 rows; each matches the SQL query (LEFT, INNER, FULL).

**Code:** run with `python3 -I`.
```python
# Q23: pandas join vs merge vs concat on indexed frames
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE left_t(customer_id INTEGER, name TEXT, city TEXT);
CREATE TABLE right_t(customer_id INTEGER, segment TEXT);
INSERT INTO left_t VALUES (1,'Asha','Pune'),(2,'Ben','Delhi'),(3,'Chitra','Mumbai');
INSERT INTO right_t VALUES (2,'gold'),(3,'silver'),(4,'bronze');
"""
SQL_LEFT = "SELECT l.customer_id, l.name, l.city, r.segment FROM left_t l LEFT JOIN right_t r ON r.customer_id = l.customer_id ORDER BY 1"
SQL_INNER = "SELECT l.customer_id, l.name, l.city, r.segment FROM left_t l JOIN right_t r ON r.customer_id = l.customer_id ORDER BY 1"
SQL_FULL = """
SELECT COALESCE(l.customer_id, r.customer_id) AS customer_id, l.name, l.city, r.segment
FROM left_t l FULL JOIN right_t r ON r.customer_id = l.customer_id ORDER BY 1
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda s: pd.read_sql_query(s, con).set_index("customer_id")
s_left, s_inner, s_full = q(SQL_LEFT), q(SQL_INNER), q(SQL_FULL)

left = pd.read_sql_query("SELECT * FROM left_t", con).set_index("customer_id")
right = pd.read_sql_query("SELECT * FROM right_t", con).set_index("customer_id")
# pd:main
joined = left.join(right)                                                   # default how='left', aligns on index
merged = pd.merge(left, right, left_index=True, right_index=True)           # default how='inner'
stacked = pd.concat([left, right], axis=1)                                  # default join='outer', aligns on index
# pd:end
for title, d in [("left.join(right)", joined), ("pd.merge(left_index, right_index)", merged), ("pd.concat(axis=1)", stacked)]:
    print(title); print(d.to_string()); print()

# duplicate index labels on the right: customer 2 has two segment rows
right_dup = pd.concat([right, pd.DataFrame({"segment": ["promo"]}, index=pd.Index([2], name="customer_id"))])
print("right with duplicate label 2:"); print(right_dup.to_string(), "\n")
print("left.join(right_dup):"); print(left.join(right_dup).to_string(), "\n")
try:
    pd.concat([left, right_dup], axis=1)
except Exception as e:
    print("concat(axis=1) with duplicate labels ->", type(e).__name__ + ":", e)
dup_chk = pd.concat([right_dup, right_dup], axis=1)
print("concat of two frames that share the SAME duplicated index works (identical indexes):", len(dup_chk), "rows")

# reset_index: the key becomes a normal column, so merge/join can use on=
l2, r2 = left.reset_index(), right.reset_index()
by_col = l2.merge(r2, on="customer_id", how="left")
print("\nreset_index + merge on column:"); print(by_col.to_string(index=False))

# all compared after sorting by customer_id (index)
for a, b in [(s_left, joined), (s_inner, merged), (s_full, stacked)]:
    pd.testing.assert_frame_equal(a.sort_index(), b.sort_index(), check_dtype=False)
pd.testing.assert_frame_equal(s_left.reset_index(), by_col.sort_values("customer_id").reset_index(drop=True), check_dtype=False)
assert (len(joined), len(merged), len(stacked)) == (3, 2, 4)
print("\nasserts passed: join == LEFT JOIN, merge == INNER JOIN, concat(axis=1) == FULL JOIN")
```

**Output (my run):**
```text
left.join(right)
               name    city segment
customer_id                        
1              Asha    Pune     NaN
2               Ben   Delhi    gold
3            Chitra  Mumbai  silver

pd.merge(left_index, right_index)
               name    city segment
customer_id                        
2               Ben   Delhi    gold
3            Chitra  Mumbai  silver

pd.concat(axis=1)
               name    city segment
customer_id                        
1              Asha    Pune     NaN
2               Ben   Delhi    gold
3            Chitra  Mumbai  silver
4               NaN     NaN  bronze

right with duplicate label 2:
            segment
customer_id        
2              gold
3            silver
4            bronze
2             promo 

left.join(right_dup):
               name    city segment
customer_id                        
1              Asha    Pune     NaN
2               Ben   Delhi    gold
2               Ben   Delhi   promo
3            Chitra  Mumbai  silver 

concat(axis=1) with duplicate labels -> InvalidIndexError: Reindexing only valid with uniquely valued Index objects
concat of two frames that share the SAME duplicated index works (identical indexes): 4 rows

reset_index + merge on column:
 customer_id   name   city segment
           1   Asha   Pune     NaN
           2    Ben  Delhi    gold
           3 Chitra Mumbai  silver

asserts passed: join == LEFT JOIN, merge == INNER JOIN, concat(axis=1) == FULL JOIN
```

**Edge cases:**
- Duplicate labels on the right (customer 2 twice): `join` repeats the left row, one output row per match (3 -> 4 rows, like a SQL one-to-many join). `concat(axis=1)` with a different duplicated index raised `InvalidIndexError: Reindexing only valid with uniquely valued Index objects`. Concat of two frames that share exactly the same index does not need reindexing, and ran without error (4 rows in my run).
- Overlapping column names: `join` and `merge` need a suffix rule, and concat keeps both columns with the same name; I did not run this case.
- A RangeIndex 0..n on both frames: `concat(axis=1)` and `join` align by position label, which looks fine until a filter changes one of them.
- After `reset_index()`, the key is an ordinary column and `merge(on="customer_id", how="left")` gives the same result as the join (my assert).

**Then explain:**
- **Alignment:** `join`, `merge` with `left_index`/`right_index`, and `concat(axis=1)` all line rows up by index label. Plain `merge(on=column)` ignores the index entirely.
- **Defaults:** `DataFrame.join` is `how="left"`; `pd.merge` is `how="inner"`; `concat` is `join="outer"`. All three accept an explicit setting (concat takes `join="inner"` or `"outer"`, and has no left or right).
- **Duplicates:** join and merge do the SQL thing (all matching combinations); concat refuses when it must reindex a duplicated index.
- **When to reset_index first:** when the key is an index on one frame but a column on the other, when the index has duplicates or is just a meaningless row number, when you need a key column in the output, or when you want `indicator=True` and `validate=` on a merge with named keys.
- **Which to use:** `merge` when you want SQL join semantics and named keys, `join` for quick index lookups, `concat(axis=1)` to place frames with the same index side by side.

**Follow-ups:**
- *Row-wise stacking?* `pd.concat(axis=0)` is UNION ALL (Q10).
- *Join on a column of left and the index of right?* `join(on=...)` supports that; not run here.
- *Which is fastest?* Not measured here; index alignment on a unique sorted index is the cheap case (concept only).

**Common mistakes:**
- Expecting `join` to be an inner join, or `merge` to be a left join.
- Using `concat(axis=1)` with a duplicated index and being surprised by the error.
- Concatenating side by side two frames whose indexes are unrelated row numbers.
- Forgetting that the key is in the index and writing `merge(on="customer_id")`, which fails with a KeyError (not run here).
