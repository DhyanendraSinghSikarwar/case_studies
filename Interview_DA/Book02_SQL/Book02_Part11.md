# Book 2 — SQL | Part 11: DB Concepts (keys, normalization, indexes, views, stored procedures, DDL/DML, transactions/ACID, OLTP vs OLAP, data warehouse basics)

- **Target:** 35 questions (minimum)
- **Actual:** 44 questions
- **Scope:** Database-concept questions asked in DA/BA technical rounds (🟢🟡, a few ⭐ 🔴 design questions). Heavy query writing lives in Parts 1-10. Questions on UNION/UNION ALL, WHERE vs HAVING and DELETE/TRUNCATE/DROP appear here with a database-concept framing; Parts 1-2 cover their query-writing use.
- **Ordering:** ⭐⭐⭐ → ⭐, then 🟢 → 🔴.

### Q1 ⭐⭐⭐ 🟢 What is a primary key, and how is it different from a foreign key?
**Asked at:** service MNCs (a 2026 DBMS guide names TCS/Infosys/Wipro/Accenture; one 2025 Infosys candidate report mentions keys, normalization and basic SQL; secondary/anonymous sources, not DA-specific)
**What the interviewer is checking:** Whether you understand that a primary key identifies a row and a foreign key links two tables.
**Say this in the interview:** A primary key uniquely identifies each row in its own table: no duplicates, no NULLs. A foreign key is a column in another table that points to that primary key, so the database can refuse rows that point to something that does not exist.
**Explain simply:**
- **Primary key (PK):** like an employee ID. Every employee has exactly one, and no two share it.
- **Foreign key (FK):** like the department ID written on the employee's record. It must match a real department.
- A table has only **one** primary key (it may span several columns) but can have **many** foreign keys.
- FK values may repeat (many employees in one department) and may be NULL (not yet assigned), unless blocked by NOT NULL.
- This is what keeps data "referentially intact": no employee in a department that does not exist.
**Example:** `departments` has dept_id 10 (HR) and 20 (Sales). An employee with dept_id 99 is rejected. A department that still has employees cannot be deleted by default.
**SQL:** (run in SQLite 3.45.1; SQLite only enforces foreign keys after `PRAGMA foreign_keys=ON`, which must be set on every connection)
```sql
PRAGMA foreign_keys = ON;
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT,
                       dept_id INTEGER REFERENCES departments(dept_id));
INSERT INTO departments VALUES (10,'HR'),(20,'Sales');
INSERT INTO employees VALUES (1,'Asha',10),(2,'Ravi',20);
INSERT INTO employees VALUES (3,'Meena',99);   -- bad department
INSERT INTO employees VALUES (1,'Karan',10);   -- duplicate emp_id
DELETE FROM departments WHERE dept_id = 10;    -- Asha still belongs to it
```
**Output (actual run):**
```text
INSERT dept 99          -> FOREIGN KEY constraint failed
INSERT duplicate emp_id -> UNIQUE constraint failed: employees.emp_id
DELETE dept 10          -> FOREIGN KEY constraint failed
```
**Edge cases:** In PostgreSQL/MySQL/SQL Server the same `REFERENCES` syntax is enforced by default (MySQL InnoDB only; from memory, not run here). You can choose what happens on delete: `ON DELETE CASCADE` (delete children too), `SET NULL`, or the default block. CASCADE is dangerous on HR data (not run here).
**Likely follow-ups:**
- Can a foreign key be NULL? Yes, unless the column is also NOT NULL.
- Can a foreign key point to a non-primary column? It must point to a PK or UNIQUE column.
**Common mistakes:** Saying a table can have several primary keys, forgetting that SQLite ignores foreign keys unless the PRAGMA is on, and thinking the FK must be unique.

### Q2 ⭐⭐⭐ 🟢 What are DDL, DML, DCL and TCL commands? Give one example of each.
**Asked at:** commonly asked (no company-specific report found); SQL command categories appear in generic DBMS question guides
**What the interviewer is checking:** Basic SQL vocabulary: which commands change structure, data, permissions or transactions.
**Say this in the interview:** DDL defines structure (CREATE), DML changes the data (INSERT, UPDATE, DELETE), DCL controls permissions (GRANT), and TCL controls transactions (COMMIT, ROLLBACK). SELECT is often grouped under DML, or called DQL (query) on its own.
**Explain simply:**
| Group | Full name | Plain meaning | Examples |
|---|---|---|---|
| DDL | Data Definition Language | Builds or changes the **containers** | CREATE, ALTER, DROP, TRUNCATE |
| DML | Data Manipulation Language | Changes the **rows** | INSERT, UPDATE, DELETE (SELECT reads) |
| DCL | Data Control Language | Decides **who may do what** | GRANT, REVOKE |
| TCL | Transaction Control Language | Saves or undoes a batch of DML | COMMIT, ROLLBACK, SAVEPOINT |
- Think of a filing cabinet: DDL builds drawers, DML moves papers in and out, DCL hands out keys, TCL says "keep" or "undo" for the last batch of changes.
- Some textbooks list TRUNCATE under DDL and some under DML; say it is usually DDL.
**Example:** HR admin creates `employees` (DDL), inserts a new joiner (DML), gives the payroll analyst read-only access (DCL), then commits (TCL).
**SQL:** (run in SQLite 3.45.1)
```sql
CREATE TABLE emp(emp_id INTEGER PRIMARY KEY, salary INT);   -- DDL
INSERT INTO emp VALUES (1, 50000);                          -- DML
BEGIN; UPDATE emp SET salary = 55000 WHERE emp_id = 1;      -- DML in a transaction
ROLLBACK;                                                   -- TCL
SELECT * FROM emp;
GRANT SELECT ON emp TO analyst;                             -- DCL
```
**Output (actual run):**
```text
emp after ROLLBACK -> (1, 50000)     # the raise was undone
GRANT              -> near "GRANT": syntax error   (SQLite has no users or permissions)
```
DCL is **not run here**. Standard form, from memory: PostgreSQL / MySQL / SQL Server all accept `GRANT SELECT ON emp TO analyst;` (MySQL needs a user like `'analyst'@'%'`; SQL Server also has `DENY`).
**Edge cases:** In MySQL, DDL commits automatically (you cannot roll back a DROP); in PostgreSQL and SQL Server DDL can be rolled back inside a transaction (from memory, not run here).
**Likely follow-ups:**
- Is SELECT DML? Often yes; some say DQL.
- Is TRUNCATE DDL or DML? Usually DDL.
**Common mistakes:** Calling DELETE a DDL command, forgetting DCL and TCL, and not knowing that DDL can auto-commit in MySQL.

### Q3 ⭐⭐⭐ 🟢 What is the difference between DELETE, TRUNCATE and DROP?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Whether you know what each removes (rows vs all rows vs the table itself) and which can be undone.
**Say this in the interview:** DELETE removes chosen rows and can use WHERE; TRUNCATE empties the whole table quickly but keeps its structure; DROP removes the table itself, structure and data. (The query-writing use of DELETE is in Parts 1-2; here the focus is the concept.)
**Explain simply:**
| | DELETE | TRUNCATE | DROP |
|---|---|---|---|
| Type | DML | DDL (usually) | DDL |
| Removes | Rows you pick (WHERE) | All rows | Table, rows, indexes |
| WHERE allowed | Yes | No | No |
| Table still exists | Yes | Yes | No |
| Rollback | Yes, inside a transaction | Engine-dependent* | Engine-dependent* |
| Speed on big tables | Slower (row by row, logged) | Fast | Fast |
*PostgreSQL and SQL Server can roll them back inside a transaction; MySQL and Oracle cannot (from memory, not run here).
- Typical extra: TRUNCATE usually resets auto-number counters; DELETE does not.
**Example:** Remove only employees who left in 2020: DELETE with WHERE. Clear a staging table before tonight's load: TRUNCATE. Retire the table `temp_payroll_test`: DROP.
**SQL:** (run in SQLite 3.45.1)
```sql
DELETE FROM emp WHERE emp_id = 3;   -- 3 rows -> 2 rows
TRUNCATE TABLE emp;                 -- SQLite: not supported
DROP TABLE emp;                     -- table gone
SELECT * FROM emp;
```
**Output (actual run):**
```text
rows after DELETE -> 2
TRUNCATE          -> near "TRUNCATE": syntax error
SELECT after DROP -> no such table: emp
```
SQLite has no TRUNCATE; people use `DELETE FROM emp;`. Standard syntax `TRUNCATE TABLE emp;` works in PostgreSQL (also `TRUNCATE emp`), MySQL and SQL Server (from memory, not run here).
**Edge cases:** TRUNCATE is blocked on tables referenced by foreign keys in several engines; DROP of a table used by a view leaves the view broken.
**Likely follow-ups:**
- Which is fastest to empty a table? TRUNCATE.
- Can you recover after DROP? Only from a backup, or by rollback in engines that allow transactional DDL.
**Common mistakes:** Running DELETE without WHERE, believing TRUNCATE always can be rolled back, and saying DROP "deletes rows" (it deletes the table).

### Q4 ⭐⭐⭐ 🟢 What is a view in SQL, and why would an analyst use one?
**Asked at:** commonly asked (no company-specific report found); views appear in SQL question banks (low-reliability source)
**What the interviewer is checking:** Whether you know a view is a saved query, not a copy of data.
**Say this in the interview:** A view is a saved SELECT that behaves like a table. It stores the query, not the data, so it always shows current numbers. I use views to reuse tricky logic, hide sensitive columns and give dashboards a clean table.
**Explain simply:**
- A normal view stores **no rows**; each time you query it the saved SELECT runs again.
- Benefits: write the logic once; simpler queries for colleagues; hide columns like salary from some users; keep reports consistent.
- Limits: it does not speed up a slow query by itself; some views cannot be updated through (e.g. ones with GROUP BY).
- A **materialized view** (PostgreSQL, Oracle) stores the result physically and must be refreshed.
**Example:** HR wants "active headcount and payroll per department" in every report. One view `active_headcount` does it.
**SQL:** (run in SQLite 3.45.1)
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept TEXT, salary INT, left_date TEXT);
INSERT INTO employees VALUES (1,'Asha','HR',50000,NULL),(2,'Ravi','Sales',62000,'2025-05-15'),
                             (3,'Meena','Sales',58000,NULL),(4,'Karan','HR',45000,NULL);
CREATE VIEW active_headcount AS
SELECT dept, COUNT(*) AS active_emps, SUM(salary) AS payroll
FROM employees WHERE left_date IS NULL GROUP BY dept;
SELECT * FROM active_headcount ORDER BY dept;
INSERT INTO employees VALUES (5,'Divya','HR',70000,NULL);   -- new hire
SELECT * FROM active_headcount ORDER BY dept;               -- view updates by itself
```
**Output (actual run):**

Before the hire:

| dept | active_emps | payroll |
|---|---|---|
| HR | 2 | 95000 |
| Sales | 1 | 58000 |

After the hire:

| dept | active_emps | payroll |
|---|---|---|
| HR | 3 | 165000 |
| Sales | 1 | 58000 |

**Edge cases:** `CREATE MATERIALIZED VIEW` gave `syntax error` in SQLite (not supported). Not run here, from memory: PostgreSQL `CREATE MATERIALIZED VIEW mv AS SELECT ...; REFRESH MATERIALIZED VIEW mv;`. SQL Server uses an "indexed view" and MySQL has none built in. A view stays fresh, but if the base table's columns change the view can break.
**Likely follow-ups:**
- Does a view store data? No (unless materialized).
- Can you INSERT into a view? Only simple single-table views in most engines.
**Common mistakes:** Saying a view is a copy of the table, expecting a view to be faster, and using `SELECT *` inside a view (it breaks when columns change).

### Q5 ⭐⭐⭐ 🟢 What is an index, and how does it make a query faster?
**Asked at:** service MNCs (the 2026 DBMS guide and the 2025 Infosys and 2024 Accenture candidate reports in the Part 11 sources mention indexing/normalization; secondary or single anonymous reports)
**What the interviewer is checking:** Do you understand indexes as a sorted lookup structure with a write-cost trade-off.
**Say this in the interview:** An index is like the index at the back of a book: a sorted list of values with pointers to the rows. Instead of reading the whole table (full scan), the database jumps straight to matching rows. The price is extra storage and slower INSERT/UPDATE/DELETE.
**Explain simply:**
- Without an index the database reads **every row** (a "full table scan" or SCAN).
- With an index (usually a **B-tree**, a sorted tree structure) it **searches** and reads only the matching rows.
- Good columns: ones used in WHERE, JOIN and ORDER BY with many distinct values.
- Costs: each index must be updated on every write, and takes disk space. Tiny tables or queries that read most rows do not benefit (MySQL docs say a full scan can win in those cases).
- Wrapping the column in a function (`salary+0 = 30500`) usually stops the index from being used.
**Example:** Finding one employee among 2,000 rows: scan reads 2,000, an index reads about 1.
**SQL:** (run in SQLite 3.45.1; 2,000-row `emp` table)
```sql
EXPLAIN QUERY PLAN SELECT * FROM emp WHERE salary = 30500;   -- before
CREATE INDEX idx_emp_salary ON emp(salary);
EXPLAIN QUERY PLAN SELECT * FROM emp WHERE salary = 30500;   -- after
EXPLAIN QUERY PLAN SELECT * FROM emp WHERE salary + 0 = 30500;  -- function on column
```
**Output (actual run, `detail` column):**
```text
before:  SCAN emp
after:   SEARCH emp USING INDEX idx_emp_salary (salary=?)
salary+0 = 30500: SCAN emp      # index ignored
```
PostgreSQL and MySQL use `EXPLAIN` (PostgreSQL `EXPLAIN ANALYZE` actually runs the query); SQL Server uses a graphical or `SET SHOWPLAN` plan (from memory, not run here).
**Edge cases:** Many duplicate values (e.g. gender) make an index weak. NULLs are indexed in most engines.
**Likely follow-ups:**
- Downside of indexes? Slower writes and more storage.
- What is a composite index? One index on several columns; order matters (leftmost column first).
**Common mistakes:** Indexing every column, thinking indexes always help, and writing `WHERE UPPER(name)='ASHA'` on an indexed column.

### Q6 ⭐⭐⭐ 🟢 What is normalization, and why do databases use it?
**Asked at:** service MNCs (the Part 11 sources list normalization in the 2026 DBMS guide and in the 2025 Infosys and 2024 Accenture candidate reports; secondary or single anonymous reports)
**What the interviewer is checking:** Do you know it means splitting repeated data into related tables and can name the anomalies it prevents.
**Say this in the interview:** Normalization organises data so each fact is stored once. We split big tables into smaller linked ones to avoid duplicates and update mistakes (anomalies).
**Explain simply:**
- Problem: a flat table repeating department name and head on every employee row.
- **Update anomaly:** change the HR head on one row and the others keep the old name.
- **Insert anomaly:** you cannot record a new department until an employee joins it.
- **Delete anomaly:** deleting the last employee of a department also deletes the department facts.
- Fix: one `departments` table, one `employees` table, linked by `dept_id`. Normal forms (1NF, 2NF, 3NF; see Q9) are the rules.
- Trade-off: more joins when reading (see Q21 on denormalization).
**Example:** Four employees, two departments. The department head "Nisha" is typed on 2 rows; change it on 1 and the data disagrees.
**SQL:** (run in SQLite 3.45.1)
```sql
CREATE TABLE emp_flat(emp_id INT, name TEXT, dept_id INT, dept_name TEXT, dept_head TEXT);
INSERT INTO emp_flat VALUES (1,'Asha',10,'HR','Nisha'),(2,'Karan',10,'HR','Nisha'),
                            (3,'Ravi',20,'Sales','Vikram'),(4,'Meena',20,'Sales','Vikram');
UPDATE emp_flat SET dept_head='Neha' WHERE emp_id = 1;      -- forgot Karan's row
SELECT dept_name, dept_head, COUNT(*) FROM emp_flat GROUP BY 1,2;
```
**Output (actual run):**

| dept_name | dept_head | n |
|---|---|---|
| HR | Neha | 1 |
| HR | Nisha | 1 |
| Sales | Vikram | 2 |

HR now has two heads. After splitting into `departments(dept_id, dept_name, dept_head)` (2 rows: 10 HR Nisha, 20 Sales Vikram) and `employees(emp_id, name, dept_id)` (4 rows), a join gives back the original view: Asha-HR, Karan-HR, Ravi-Sales, Meena-Sales (actual run).
**Edge cases:** Over-normalizing makes reporting queries need many joins.
**Likely follow-ups:**
- What are the normal forms? See Q9.
- Do data warehouses normalize? Usually not (Q8, Q21).
**Common mistakes:** Saying normalization "speeds up queries" (it mainly protects data accuracy), and mixing it up with data cleaning.

### Q7 ⭐⭐⭐ 🟢 What are the ACID properties of a database transaction?
**Asked at:** service MNCs (the 2026 DBMS guide and the 2024 Accenture candidate report in the Part 11 sources mention ACID; secondary or single anonymous reports)
**What the interviewer is checking:** Can you name four letters AND explain each with an example.
**Say this in the interview:** ACID is four guarantees for a transaction: Atomicity (all or nothing), Consistency (rules stay satisfied), Isolation (parallel transactions do not disturb each other), Durability (committed data survives a crash).
**Explain simply:**
- **Atomicity:** a salary transfer of 300 debits one account and credits another; either both happen or neither.
- **Consistency:** the database moves from one valid state to another; constraints (e.g. balance >= 0) are never violated by a committed transaction.
- **Isolation:** two people updating at once should not see each other's half-finished work. Strength is set by isolation levels (Read Committed, Repeatable Read, Serializable). PostgreSQL's default is Read Committed.
- **Durability:** once COMMIT returns, the change survives a power cut (via a write-ahead log).
**Example:** Transfer Rs 300 from Asha (1,000) to Ravi (500).
**SQL:** (run in SQLite 3.45.1)
```sql
CREATE TABLE acct(acct_id INTEGER PRIMARY KEY, holder TEXT, balance INT CHECK(balance >= 0));
INSERT INTO acct VALUES (1,'Asha',1000),(2,'Ravi',500);
BEGIN; UPDATE acct SET balance = balance - 300 WHERE acct_id = 1; ROLLBACK;  -- atomicity: undo
BEGIN; UPDATE acct SET balance = balance - 300 WHERE acct_id = 1;
       UPDATE acct SET balance = balance + 300 WHERE acct_id = 2; COMMIT;
BEGIN; UPDATE acct SET balance = balance - 5000 WHERE acct_id = 1;           -- consistency
```
**Output (actual run):**
```text
inside txn      : Asha 700, Ravi 500
after ROLLBACK  : Asha 1000, Ravi 500
after COMMIT    : Asha 700, Ravi 800
overdraw 5000   : CHECK constraint failed: balance>=0   (then ROLLBACK; balances unchanged)
reopen file DB after commit: 1 row still there          (durability, basic check)
```
Isolation was **not** demonstrated here (needs two concurrent sessions). Isolation level facts from the PostgreSQL documentation: Read Committed blocks dirty reads; Serializable blocks all anomalies; PostgreSQL treats Read Uncommitted as Read Committed.
**Edge cases:** Higher isolation costs concurrency; serialization failures must be retried by the app.
**Likely follow-ups:**
- What is a dirty read? Reading another transaction's uncommitted change.
- Which letter does a CHECK constraint support? Consistency.
**Common mistakes:** Listing the words without examples, confusing consistency with "same data on all servers", and saying ROLLBACK works after COMMIT.

### Q8 ⭐⭐⭐ 🟡 What is the difference between OLTP and OLAP systems?
**Asked at:** general DW guides (Coursera, DataCamp) list it; data modelling basics are reported for Flipkart and Amazon BIE interviews (research/interview_processes.md; via search summary, lower confidence)
**What the interviewer is checking:** Whether you connect system design to workload: many small writes vs few big reads.
**Say this in the interview:** OLTP runs the day-to-day business: many small, fast inserts and updates, like placing an order. OLAP is for analysis: fewer, big read-heavy queries over history, like yearly sales by region. Analysts mostly work on OLAP systems.
**Explain simply:**
| | OLTP (Online Transaction Processing) | OLAP (Online Analytical Processing) |
|---|---|---|
| Purpose | Run operations | Analyse and report |
| Typical query | "Insert this order", "update leave balance" | "Revenue by month by region, 3 years" |
| Data | Current, detailed | Historical, often summarised |
| Design | Normalized, many tables | Denormalized, star schema |
| Users | Clerks, apps, customers | Analysts, managers |
| Speed goal | Milliseconds per transaction | Fast big scans and aggregates |
| Examples | HRMS, banking, e-commerce checkout | Data warehouse, BI reports |
**Example:** Swiping attendance at the gate writes one row (OLTP). The monthly attrition dashboard scans 3 years of rows (OLAP).
**Code / Steps:** No query needed. The same table can be queried both ways; the difference is the workload and design. Running heavy analytics directly on the OLTP database can slow the live system, so companies copy data into a warehouse.
**Likely follow-ups:**
- Which is normalized? OLTP.
- Where do star schemas live? OLAP (Q10).
**Common mistakes:** Saying OLAP is "bigger SQL", forgetting that the data is copied (ETL) from OLTP, and mixing up the acronyms.

### Q9 ⭐⭐⭐ 🟡 What are 1NF, 2NF and 3NF? Explain each with a simple table example.
**Asked at:** service MNCs (the Part 11 sources mention normalization in the 2026 DBMS guide and in Infosys 2025 and Accenture 2024 candidate reports; secondary or single anonymous reports)
**What the interviewer is checking:** Can you state the rule for each form and spot a violation in a small table.
**Say this in the interview:** 1NF: one value per cell, no repeating groups. 2NF: it is in 1NF and every non-key column depends on the **whole** key, not part of it. 3NF: it is in 2NF and non-key columns depend only on the key, not on other non-key columns.
**Explain simply:**
- **1NF:** a cell must not hold a list like "Python, SQL". Make one row per skill.
- **2NF** matters only for composite keys (key of 2+ columns). In `training(emp_id, course_id, emp_name, score)` the key is (emp_id, course_id), but `emp_name` depends on `emp_id` alone: partial dependency. Move it to an `emp` table.
- **3NF:** in `employees(emp_id, dept_id, dept_name)`, `dept_name` depends on `dept_id`, not on `emp_id`: transitive dependency (A determines B, B determines C). Move it to `departments`.
- Memory trick: every non-key column depends on "the key, the whole key, and nothing but the key".
**Example:** 1NF violation: row `emp 1 | skills: "SQL, Excel"` becomes `emp 1 | SQL` and `emp 1 | Excel`.
**SQL:** (2NF fix, run in SQLite 3.45.1)
```sql
CREATE TABLE training(emp_id INT, course_id INT, emp_name TEXT, score INT, PRIMARY KEY(emp_id, course_id));
INSERT INTO training VALUES (1,101,'Asha',80),(1,102,'Asha',90),(2,101,'Ravi',70);
CREATE TABLE emp2(emp_id INT PRIMARY KEY, emp_name TEXT);
INSERT INTO emp2 SELECT DISTINCT emp_id, emp_name FROM training;
CREATE TABLE scores(emp_id INT, course_id INT, score INT, PRIMARY KEY(emp_id, course_id));
INSERT INTO scores SELECT emp_id, course_id, score FROM training;
```
**Output (actual run):** before, `Asha` is stored twice; after:

`emp2`

| emp_id | emp_name |
|---|---|
| 1 | Asha |
| 2 | Ravi |

`scores`

| emp_id | course_id | score |
|---|---|---|
| 1 | 101 | 80 |
| 1 | 102 | 90 |
| 2 | 101 | 70 |

3NF split is the same idea (department columns moved to `departments`), shown in Q6.
**Edge cases:** A table with a single-column key is automatically free of partial dependencies, so it is in 2NF if it is in 1NF. BCNF is a stricter 3NF (follow-up).
**Likely follow-ups:**
- What is BCNF? Every determinant must be a candidate key.
- Is 3NF always best? Not for reporting (Q21).
**Common mistakes:** Memorising names without being able to point at the violating column, and applying 2NF to single-column keys.

### Q10 ⭐⭐⭐ 🟡 What is a star schema? What are fact tables and dimension tables?
**Asked at:** product and GCC: data modelling basics (star schema, normalization) are reported for Flipkart and Amazon BIE interviews in research/interview_processes.md (via search summaries, lower confidence); also in generic DW guides
**What the interviewer is checking:** Can you describe a central fact table surrounded by dimensions and why analysts like it.
**Say this in the interview:** A star schema has one central **fact table** holding measurable events (sales amount, quantity) with foreign keys to surrounding **dimension tables** holding descriptions (product, region, date). Drawn out, it looks like a star. It makes reporting queries simple and fast.
**Explain simply:** (definitions are standard textbook meanings, from memory)
- **Fact table:** one row per event at a chosen **grain** (level of detail), e.g. one row per sale line. Holds numbers to add up plus keys.
- **Dimension table:** descriptive context used to filter and group: who, what, where, when.
- Queries are the same shape: join the fact to dimensions, GROUP BY a dimension attribute, SUM a fact measure.
- Dimensions are kept denormalized (flat), so few joins.
**Example:** Sales fact with 5 rows; dimensions `dim_product` (3) and `dim_region` (2).
**SQL:** (run in SQLite 3.45.1)
```sql
CREATE TABLE dim_product(product_id INTEGER PRIMARY KEY, product_name TEXT, category TEXT);
CREATE TABLE dim_region(region_id INTEGER PRIMARY KEY, region TEXT);
CREATE TABLE fact_sales(sale_id INTEGER PRIMARY KEY, product_id INT REFERENCES dim_product,
                        region_id INT REFERENCES dim_region, sale_date TEXT, qty INT, amount INT);
-- 3 products (Laptop, Mouse: Electronics; Desk: Furniture), 2 regions (South, North), 5 sales
SELECT p.category, r.region, SUM(f.amount) AS revenue
FROM fact_sales f
JOIN dim_product p ON p.product_id = f.product_id
JOIN dim_region  r ON r.region_id  = f.region_id
GROUP BY p.category, r.region ORDER BY 1, 2;
```
**Output (actual run):**

| category | region | revenue |
|---|---|---|
| Electronics | North | 60500 |
| Electronics | South | 61500 |
| Furniture | North | 12000 |

**Edge cases:** A real date dimension usually exists (year, month, weekday). A fact row with an unknown dimension needs a "Unknown" dimension row.
**Likely follow-ups:**
- Star vs snowflake? See Q22.
- What is grain? The level of detail of one fact row.
**Common mistakes:** Putting descriptive text in the fact table, mixing different grains in one fact table, and forgetting to say why it suits reporting.

### Q11 ⭐⭐ 🟢 What is the difference between a primary key and a unique key?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** The NULL rule and the one-vs-many rule.
**Say this in the interview:** Both enforce uniqueness. A table has only one primary key and it can never be NULL. A table can have many unique keys, and most databases allow NULL in them.
**Explain simply:**
| | Primary key | Unique key |
|---|---|---|
| How many per table | 1 | Many |
| NULL allowed | No | Usually yes (see engines) |
| Purpose | Identify the row | Stop duplicates in another attribute |
| Typical column | emp_id | email, PAN number |
- Engines differ on NULLs in a unique column: SQLite and PostgreSQL allow many NULLs; SQL Server allows only one NULL (from memory, not run here).
**Example:** `emp_id` is the primary key; `email` is unique, so two staff cannot share an email, but a new joiner can have no email yet.
**SQL:** (run in SQLite 3.45.1)
```sql
CREATE TABLE emp(emp_id INTEGER PRIMARY KEY, email TEXT UNIQUE, name TEXT NOT NULL);
INSERT INTO emp(emp_id,email,name) VALUES (1,'a@x.com','Asha'),(2,NULL,'Ravi'),(3,NULL,'Meena');
INSERT INTO emp(emp_id,email,name) VALUES (4,'a@x.com','Karan');
```
**Output (actual run):** the first insert works (two rows with NULL email are accepted); the second fails with `UNIQUE constraint failed: emp.email`.
**Edge cases:** SQLite quirk: a non-integer PRIMARY KEY column can hold NULL unless declared NOT NULL (known SQLite behaviour, from memory); `INTEGER PRIMARY KEY` becomes an auto-assigned row id (inserting NULL gave id 4 in a test).
**Likely follow-ups:**
- Can a unique key be a foreign key target? Yes.
- Does a primary key create an index? Yes in most engines.
**Common mistakes:** Saying unique keys cannot be NULL, and saying a table can have two primary keys.

### Q12 ⭐⭐ 🟢 What is a candidate key, a composite key and a surrogate key?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Key vocabulary with clear examples.
**Say this in the interview:** A candidate key is any column set that could uniquely identify a row; one of them becomes the primary key. A composite key uses two or more columns together. A surrogate key is an artificial ID with no business meaning, like an auto-number.
**Explain simply:**
- **Candidate key:** in `employees`, both `emp_id` and `pan_number` could identify a person. Both are candidates; you choose `emp_id` as the primary key; the other becomes an alternate key.
- **Composite key:** in `attendance`, one employee appears every day, so (emp_id, att_date) together identify a row.
- **Surrogate key:** a system-generated number (cust_sk = 1, 2, 3...). Useful because natural keys like phone numbers change. Opposite: a **natural key** (real-world value).
**Example:** `attendance(emp_id, att_date, status)` with a composite primary key; `cust` with a surrogate `cust_sk` and natural code `C-101`.
**SQL:** (run in SQLite 3.45.1)
```sql
CREATE TABLE attendance(emp_id INT, att_date TEXT, status TEXT, PRIMARY KEY(emp_id, att_date));
INSERT INTO attendance VALUES (1,'2025-06-01','P'),(1,'2025-06-02','P'),(2,'2025-06-01','A');
INSERT INTO attendance VALUES (1,'2025-06-01','A');      -- same pair again
CREATE TABLE cust(cust_sk INTEGER PRIMARY KEY AUTOINCREMENT, cust_code TEXT UNIQUE, city TEXT);
INSERT INTO cust(cust_code, city) VALUES ('C-101','Pune'),('C-102','Delhi');
```
**Output (actual run):** the duplicate pair fails with `UNIQUE constraint failed: attendance.emp_id, attendance.att_date`. `cust` rows: (1, C-101, Pune), (2, C-102, Delhi). Auto-number syntax differs: PostgreSQL `GENERATED ALWAYS AS IDENTITY` or `SERIAL`, MySQL `AUTO_INCREMENT`, SQL Server `IDENTITY(1,1)` (from memory, not run here).
**Edge cases:** Employee 1 can appear on many dates, and many employees on one date: only the pair is unique.
**Likely follow-ups:**
- Why use a surrogate key? Stable, short, and does not change when business data changes (important for warehouse dimensions).
- Is every candidate key a primary key? No, only the chosen one.
**Common mistakes:** Calling a composite key "two primary keys", and thinking a surrogate key must be hidden from users.

### Q13 ⭐⭐ 🟢 What is a database, a DBMS and an RDBMS?
**Asked at:** commonly asked (no company-specific report found); basic theory in service MNC DBMS guides
**What the interviewer is checking:** That you separate the data, the software and the relational model.
**Say this in the interview:** A database is an organised collection of data. A DBMS is the software that stores, protects and retrieves it. An RDBMS is a DBMS that stores data in related tables using keys and SQL, like MySQL, PostgreSQL, SQL Server or Oracle.
**Explain simply:**
- Database = the filing cabinet and files. DBMS = the office clerk system managing access, security and backups.
- RDBMS = a clerk who files everything in tables (rows and columns) and links them with keys.
- Not all DBMSs are relational: MongoDB (documents) and Redis (key-value) are NoSQL DBMSs (from memory).
- A DBMS handles: storage, queries, security, concurrency (many users at once), backup and recovery.
**Example:** The HR team's employee data = database. PostgreSQL running on the server = DBMS/RDBMS. The `employees` and `departments` tables linked by `dept_id` make it relational (Q1).
**Code / Steps:** Concept only. SQLite (used for demos in this book) is a small RDBMS stored in a single file; the others run as server programs.
**Likely follow-ups:**
- Excel vs RDBMS? Excel has no enforced keys, no multi-user safety, and limited rows.
- What is SQL? The language to talk to an RDBMS.
**Common mistakes:** Saying "database" and "DBMS" mean the same thing, and treating MySQL as a "database" instead of a DBMS.

### Q14 ⭐⭐ 🟢 What are constraints in SQL (NOT NULL, UNIQUE, CHECK, DEFAULT)? Why are they useful?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** That you use rules in the database to protect data quality.
**Say this in the interview:** Constraints are rules the database enforces on every insert and update: NOT NULL forces a value, UNIQUE blocks duplicates, CHECK tests a condition, DEFAULT fills a value when none is given. They stop bad data at the door.
**Explain simply:**
- Together with PRIMARY KEY and FOREIGN KEY they make up the constraints.
- DEFAULT is not a rule that rejects; it supplies a value.
- Benefit: bad data (negative salary, missing name) is rejected rather than cleaned later by analysts.
**Example:** Employee table: name required, email unique, salary above 0, status 'active' by default.
**SQL:** (run in SQLite 3.45.1)
```sql
CREATE TABLE emp(emp_id INTEGER PRIMARY KEY, email TEXT UNIQUE, name TEXT NOT NULL,
                 salary INT CHECK(salary > 0), status TEXT DEFAULT 'active');
INSERT INTO emp(emp_id,email,name,salary) VALUES (1,'a@x.com','Asha',50000);
INSERT INTO emp(emp_id,email,name,salary) VALUES (4,'a@x.com','Karan',40000);   -- dup email
INSERT INTO emp(emp_id,email,name,salary) VALUES (5,'k@x.com',NULL,40000);      -- no name
INSERT INTO emp(emp_id,email,name,salary) VALUES (6,'z@x.com','Divya',-5);      -- bad salary
```
**Output (actual run):**
```text
row 1 saved with status = 'active' (DEFAULT filled it)
dup email       -> UNIQUE constraint failed: emp.email
NULL name       -> NOT NULL constraint failed: emp.name
negative salary -> CHECK constraint failed: salary>0
```
**Edge cases:** MySQL enforced CHECK only from 8.0.16 onward (from memory, not run here). A CHECK that evaluates to NULL passes (NULL salary is not rejected by `salary > 0`; add NOT NULL).
**Likely follow-ups:**
- Can you add a constraint later? Yes: `ALTER TABLE ... ADD CONSTRAINT` (PostgreSQL/SQL Server/MySQL, not run here; SQLite has limited ALTER).
- Constraints vs app validation? Do both; the database is the last line of defence.
**Common mistakes:** Thinking CHECK catches NULLs, and relying only on the application to validate.

### Q15 ⭐⭐ 🟢 What is a transaction? What do COMMIT and ROLLBACK do?
**Asked at:** commonly asked (no company-specific report found); transactions/ACID appear in service MNC reports (Q7)
**What the interviewer is checking:** Whether you know a transaction groups steps and that COMMIT makes them permanent while ROLLBACK undoes them.
**Say this in the interview:** A transaction is a group of SQL steps treated as one unit. COMMIT saves all of them permanently; ROLLBACK cancels all of them since the transaction started.
**Explain simply:**
- Start with `BEGIN` (or `START TRANSACTION` in MySQL/PostgreSQL; SQL Server `BEGIN TRANSACTION`).
- Inside, changes are visible to you but not final.
- `COMMIT` = save; `ROLLBACK` = undo; `SAVEPOINT` marks a halfway point you can roll back to.
- Many tools run in **autocommit** mode: every statement commits at once unless you start a transaction.
**Example:** Giving a department a 10% raise: 40 UPDATEs. If step 25 fails you roll back and nobody is left half-paid.
**SQL:** (run in SQLite 3.45.1)
```sql
BEGIN;
UPDATE acct SET balance = balance - 300 WHERE acct_id = 1;
SELECT * FROM acct;       -- Asha 700 inside the transaction
ROLLBACK;                 -- Asha back to 1000
BEGIN; UPDATE acct SET balance = balance - 300 WHERE acct_id = 1;
       UPDATE acct SET balance = balance + 300 WHERE acct_id = 2;
COMMIT;                   -- now permanent: Asha 700, Ravi 800
```
**Output (actual run):** inside: Asha 700 / Ravi 500; after ROLLBACK: Asha 1000 / Ravi 500; after COMMIT: Asha 700 / Ravi 800.
**Edge cases:** After COMMIT you cannot ROLLBACK. If the connection drops before COMMIT, the changes are rolled back automatically. In MySQL, DDL auto-commits (from memory, not run here).
**Likely follow-ups:**
- What is autocommit? Each statement is its own transaction.
- What is a SAVEPOINT? A partial rollback point.
**Common mistakes:** Forgetting to COMMIT (changes vanish when the session ends), running UPDATE without WHERE and relying on a rollback that autocommit already prevented.

### Q16 ⭐⭐ 🟢 What is a data warehouse, and how is it different from an operational database?
**Asked at:** generic DW guides list it (Coursera, DataCamp; undated); data modelling basics reported at Flipkart and Amazon BIE (research/interview_processes.md, via search summary, lower confidence)
**What the interviewer is checking:** Whether you know why companies copy data into a separate analytical store.
**Say this in the interview:** A data warehouse is a central store of cleaned, historical data from many systems, built for reporting and analysis. An operational database runs live transactions. The warehouse is read-heavy, historical and integrated; the operational one is write-heavy and current.
**Explain simply:**
- Data flows in through **ETL/ELT** (extract from sources, transform/clean, load).
- Subject-oriented (sales, HR), integrated (one definition of "employee" across systems), time-variant (keeps history), non-volatile (rarely changed after loading).
- Typically modelled as star schemas (Q10).
- Keeps heavy analytics from slowing the live application.
**Example:** The HRMS, payroll tool and recruiting portal each hold part of the story. The warehouse combines them so you can compute attrition by tenure by department.
**Code / Steps:** Concept question. A sketch: nightly job copies yesterday's `payroll` rows into `fact_payroll` and refreshes `dim_employee`. Not run here.
**Likely follow-ups:**
- Data warehouse vs data lake? A lake stores raw files of any shape; a warehouse stores structured, modelled data.
- What is a data mart? A smaller warehouse for one team (e.g. HR).
**Common mistakes:** Calling the warehouse "a bigger database", and ignoring ETL and data cleaning.

### Q17 ⭐⭐ 🟢 What is the difference between UNION and UNION ALL?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** Duplicate handling and the performance trade-off. (Parts 1-2 cover its query use; here the concept.)
**Say this in the interview:** Both stack the results of two SELECTs. UNION removes duplicate rows; UNION ALL keeps everything and is faster because it skips the de-duplication step.
**Explain simply:**
- Both queries need the same number of columns, with compatible types, in the same order.
- Column names come from the first query.
- UNION must sort or hash to find duplicates; UNION ALL just appends.
- Use UNION ALL when you know there are no duplicates or you want to keep them (e.g. summing monthly tables).
**Example:** Two HR offices send employee lists; Ravi is in both.
**SQL:** (run in SQLite 3.45.1)
```sql
CREATE TABLE hr_a(name TEXT, city TEXT); CREATE TABLE hr_b(name TEXT, city TEXT);
INSERT INTO hr_a VALUES ('Asha','Pune'),('Ravi','Delhi');
INSERT INTO hr_b VALUES ('Ravi','Delhi'),('Meena','Pune');
SELECT * FROM hr_a UNION     SELECT * FROM hr_b ORDER BY 1;
SELECT * FROM hr_a UNION ALL SELECT * FROM hr_b ORDER BY 1;
```
**Output (actual run):**

UNION (3 rows)

| name | city |
|---|---|
| Asha | Pune |
| Meena | Pune |
| Ravi | Delhi |

UNION ALL (4 rows, Ravi twice)

| name | city |
|---|---|
| Asha | Pune |
| Meena | Pune |
| Ravi | Delhi |
| Ravi | Delhi |

**Edge cases:** UNION compares whole rows, and treats NULLs as equal for de-duplication. Within one query both rows must match on all columns to be a duplicate. Use `EXCEPT`/`INTERSECT` for other set operations (PostgreSQL/SQLite; Oracle uses `MINUS`, from memory).
**Likely follow-ups:**
- Which is faster? UNION ALL.
- How is UNION different from JOIN? UNION stacks rows; JOIN adds columns side by side.
**Common mistakes:** Using UNION out of habit and silently dropping legitimate duplicates (e.g. two identical sales), and mismatched column order.

### Q18 ⭐⭐ 🟢 What is a schema, and what is the difference between a table and a view?
**Asked at:** commonly asked (no company-specific report found)
**What the interviewer is checking:** That you know a schema is a container/blueprint and a view is a saved query.
**Say this in the interview:** A schema is a named group of database objects (tables, views, and so on); it can also mean the overall design. A table stores data physically; a view stores only a query and shows data from tables when you read it.
**Explain simply:**
- Premise note: "schema" means different things. In PostgreSQL/SQL Server it is a namespace inside a database (`hr.employees`). In MySQL, schema is a synonym for database. In general talk it means the design blueprint.
- **Table:** holds rows on disk. **View:** saved SELECT, no rows of its own (Q4).
- Schemas help organise (hr, sales, finance) and control permissions.
**Example:** `hr.employees` (table), `hr.active_headcount` (view), `sales.orders` (table).
**SQL:** (run in SQLite 3.45.1; SQLite has no `CREATE SCHEMA`, but an attached database plays a similar role)
```sql
CREATE TABLE emp(a); CREATE VIEW v_emp AS SELECT a FROM emp;
ATTACH DATABASE ':memory:' AS hr;  CREATE TABLE hr.leave(b);
SELECT type, name FROM sqlite_master;       -- main
SELECT type, name FROM hr.sqlite_master;    -- attached "hr"
```
**Output (actual run):** main has `table emp` and `view v_emp`; `hr` has `table leave`. Standard syntax, from memory (not run here): `CREATE SCHEMA hr;` then `CREATE TABLE hr.employees (...);` in PostgreSQL and SQL Server.
**Edge cases:** Two schemas can each have a table with the same name.
**Likely follow-ups:**
- Schema vs database? Depends on the engine (see premise note).
- Can a view join tables from different schemas? Yes, with permission.
**Common mistakes:** Saying a view holds its own copy of data, and not mentioning that "schema" is engine-specific.

### Q19 ⭐⭐ 🟡 What is the difference between a clustered and a non-clustered index?
**Asked at:** commonly asked (no company-specific report found); gap-fill question from the standard DBMS syllabus
**What the interviewer is checking:** That a clustered index defines the physical order of the rows and there can be only one.
**Say this in the interview:** A clustered index sorts and stores the table's rows in the index order, so the table is the index. There is one per table. A non-clustered index is a separate structure holding the key values and pointers to the rows; a table can have many.
**Explain simply:** (from memory, standard behaviour)
- **Clustered:** like a phone book sorted by name; you find the entry and the data is right there. In SQL Server the primary key is clustered by default; in MySQL InnoDB the primary key is the clustered index and secondary indexes store the primary key value.
- **Non-clustered:** like the book index at the back pointing to page numbers; an extra lookup is needed unless the index **covers** the query (contains all needed columns).
- Trade-off: range searches on the clustered key are fast; every extra index adds write cost.
- PostgreSQL has no automatically maintained clustered index (table is a heap; `CLUSTER` reorders once).
**Example:** Employees clustered by emp_id; a non-clustered index on dept speeds "all HR staff".
**SQL:** Clustered syntax is **not run here** (SQLite has no clustered index command; its normal tables are stored in rowid order, which behaves like a clustered key). Standard syntax from memory:
```sql
-- SQL Server
CREATE CLUSTERED INDEX ix_emp_id ON employees(emp_id);
CREATE NONCLUSTERED INDEX ix_emp_dept ON employees(dept);
```
What I ran in SQLite on a 1,000-row table:
```text
WHERE emp_id = 500           -> SEARCH emp USING INTEGER PRIMARY KEY (rowid=?)      (direct row access)
WHERE dept = 'HR' (idx_dept) -> SEARCH emp USING INDEX idx_dept (dept=?)            (index, then row lookup)
SELECT dept ... WHERE dept='HR' -> SEARCH emp USING COVERING INDEX idx_dept (dept=?) (index alone is enough)
SELECT dept,salary ... with index (dept,salary) -> COVERING INDEX idx_dept_sal
```
**Edge cases:** Clustering on a random key (e.g. a random GUID) causes page splits (from memory).
**Likely follow-ups:**
- Can a table have two clustered indexes? No, rows can be sorted one way only.
- What is a covering index? One containing every column the query needs.
**Common mistakes:** Saying a clustered index is "faster in all cases", and claiming PostgreSQL/SQLite behave like SQL Server.

### Q20 ⭐⭐ 🟡 What is a stored procedure? How is it different from a user-defined function?
**Asked at:** service MNC: one 2023 Wipro candidate report (via search summary, lower confidence) mentions stored procedures; also GCC (Wells Fargo) per research/interview_processes.md
**What the interviewer is checking:** That you know procedures run actions and functions return values used inside queries.
**Say this in the interview:** A stored procedure is a named, saved block of SQL that I can call repeatedly, and it can change data. A user-defined function also has a name and logic, but it must return a value and is meant to be used inside a query, usually without changing data.
**Explain simply:** (typical behaviour, from memory; details vary by engine)
| | Stored procedure | User-defined function |
|---|---|---|
| Called with | `CALL` / `EXEC` | Inside `SELECT`, `WHERE` |
| Returns | Optional output, result sets | Must return a value (scalar or table) |
| Can change data (INSERT/UPDATE) | Yes | Usually not (restricted in SQL Server) |
| Transactions inside | Yes | Generally no |
| Parameters | IN / OUT | IN only |
- Benefits of procedures: reuse, fewer network calls, permission control, consistent logic.
- Downsides: logic hidden in the database, harder to version control, engine-specific syntax.
**Example:** `usp_close_month(month)` locks payroll and writes summary rows; `fn_tenure_years(join_date)` is used in a SELECT to show tenure.
**SQL:** **Not run here.** SQLite has no stored procedures (Python can register functions, but that is not SQL). Standard forms from memory:
```sql
-- SQL Server
CREATE PROCEDURE usp_raise_salary @dept NVARCHAR(20), @pct DECIMAL(5,2) AS
  UPDATE employees SET salary = salary * (1 + @pct/100) WHERE dept = @dept;
EXEC usp_raise_salary 'HR', 10;
-- PostgreSQL 11+
CREATE PROCEDURE raise_salary(d text, pct numeric) LANGUAGE sql AS
$$ UPDATE employees SET salary = salary*(1+pct/100) WHERE dept = d; $$;
CALL raise_salary('HR', 10);
-- MySQL
DELIMITER //  CREATE PROCEDURE raise_salary(IN d VARCHAR(20), IN pct DECIMAL(5,2))
BEGIN UPDATE employees SET salary = salary*(1+pct/100) WHERE dept = d; END //  DELIMITER ;
CALL raise_salary('HR', 10);
```
**Edge cases:** PostgreSQL only got true procedures (`CREATE PROCEDURE`) in version 11; before that people used functions (from memory).
**Likely follow-ups:**
- Can a function be used in SELECT? Yes.
- What is a trigger? Code that runs automatically on INSERT/UPDATE/DELETE.
**Common mistakes:** Claiming functions can do everything procedures can, and presenting one engine's syntax as universal.

### Q21 ⭐⭐ 🟡 What is denormalization, and when would you choose it over normalization?
**Asked at:** commonly asked (no company-specific report found); related data modelling basics reported for Flipkart and Amazon BIE (research/interview_processes.md, lower confidence)
**What the interviewer is checking:** Whether you understand it as a deliberate trade-off of duplication for read speed.
**Say this in the interview:** Denormalization means deliberately storing redundant or pre-joined data to avoid joins and speed up reads. I choose it for reporting and analytics (warehouses), where reads dominate and data rarely changes; I keep it normalized for transactional systems where accuracy of updates matters.
**Explain simply:**
- Benefit: fewer joins, simpler and faster read queries.
- Cost: duplicate data, bigger storage, risk of inconsistency, harder updates (Q6 anomalies come back).
- Common forms: a wide reporting table, copied columns, precomputed totals.
- Fix the risk with a controlled load process: rebuild the table nightly from the normalized source.
**Example:** A dashboard shows employee name, department name and head thousands of times a day; build `emp_report` once nightly.
**SQL:** (run in SQLite 3.45.1)
```sql
CREATE TABLE emp_report AS
SELECT e.emp_id, e.name, d.dept_name, d.dept_head
FROM employees e JOIN departments d USING (dept_id);
SELECT * FROM emp_report;       -- no join needed to read it
```
**Output (actual run of the normalized join from Q6):** emp_id 1 Asha HR Nisha; 2 Karan HR Nisha; 3 Ravi Sales Vikram; 4 Meena Sales Vikram. `Nisha` and `Vikram` are now repeated: that is the redundancy being accepted.
**Edge cases:** If `dept_head` changes, `emp_report` is stale until rebuilt.
**Likely follow-ups:**
- Where would you not denormalize? Payroll or banking transactions.
- Alternative to denormalizing? Indexes, materialized views.
**Common mistakes:** Denormalizing before measuring a real performance problem, and saying denormalization is "bad design".

### Q22 ⭐⭐ 🟡 What is a snowflake schema, and how does it differ from a star schema?
**Asked at:** generic DW guides (Coursera, DataCamp); product/GCC data modelling basics (research/interview_processes.md, lower confidence)
**What the interviewer is checking:** Star = flat dimensions; snowflake = dimensions split into sub-tables (normalized).
**Say this in the interview:** A snowflake schema is a star schema whose dimension tables are further normalized into sub-dimensions, for example product linked to a separate category table. It saves some storage and avoids duplication, but needs more joins, so queries are a bit more complex and often slower.
**Explain simply:**
| | Star | Snowflake |
|---|---|---|
| Dimensions | Flat (denormalized) | Split into sub-tables (normalized) |
| Joins per query | Fewer | More |
| Redundancy | Some repeated text | Less |
| Ease for analysts | Easier | More complex |
| Maintenance of a changing attribute | Update many rows | Update one row |
- Most BI tools and analysts prefer star for simplicity (editorial view; trade-offs are standard textbook).
**Example:** `dim_product` holds category text on every product (star). In the snowflake, `dim_product_sf` holds a `category_id` and `dim_category` holds the name once.
**SQL:** (run in SQLite 3.45.1, same fact table as Q10)
```sql
CREATE TABLE dim_category(category_id INTEGER PRIMARY KEY, category TEXT);
CREATE TABLE dim_product_sf(product_id INTEGER PRIMARY KEY, product_name TEXT,
                            category_id INT REFERENCES dim_category);
SELECT cat.category, r.region, SUM(f.amount) AS revenue
FROM fact_sales f
JOIN dim_product_sf p ON p.product_id = f.product_id
JOIN dim_category cat ON cat.category_id = p.category_id     -- extra join
JOIN dim_region r ON r.region_id = f.region_id
GROUP BY cat.category, r.region ORDER BY 1, 2;
```
**Output (actual run):**

| category | region | revenue |
|---|---|---|
| Electronics | North | 60500 |
| Electronics | South | 61500 |
| Furniture | North | 12000 |

Identical answer to the star version, but with 3 joins instead of 2.
**Edge cases:** A "galaxy" (fact constellation) schema has several fact tables sharing dimensions (follow-up, from memory).
**Likely follow-ups:**
- Which performs better? Star usually, because of fewer joins.
- Which saves storage? Snowflake, slightly.
**Common mistakes:** Believing snowflake is always better because it is "normalized", and describing it as a different kind of fact table.

### Q23 ⭐⭐ 🟡 What is the difference between a view and a materialized view?
**Asked at:** commonly asked (no company-specific report found); views appear in SQL question banks (low-reliability source, Part 11 sources).
**What the interviewer is checking:** Whether you know a view stores a query and a materialized view stores the result, and the freshness-versus-speed trade-off.
**Say this in the interview:** A view is a saved query: every time you read it, the database runs it again, so it is always fresh. A materialized view saves the result on disk, so reads are fast, but the data is only as fresh as the last refresh.
**Explain simply:**
- **View** = a named SELECT. No data is copied; it is like a shortcut to a question.
- **Materialized view** = the answer of that SELECT stored as a physical table that must be **refreshed** (manually or on a schedule).
- Use a view for security (hide salary columns) and for reusing logic. Use a materialized view for heavy dashboards that scan millions of rows.
- Cost of a materialized view: extra storage and stale data between refreshes.
**Example:** A "department payroll" view over 5 lakh payroll rows is slow if the dashboard opens 200 times a day; materialize it and refresh nightly.
**SQL:**
```sql
-- SQLite (run here): views yes, materialized views NOT supported.
CREATE TABLE emp(emp_id INT, name TEXT, dept TEXT, salary INT);
INSERT INTO emp VALUES (1,'Asha','HR',50000),(2,'Ravi','Sales',62000),(3,'Meena','HR',58000);
CREATE VIEW v_dept AS SELECT dept, SUM(salary) AS payroll FROM emp GROUP BY dept;
-- manual stand-in for a materialized view: a snapshot table
CREATE TABLE mv_dept AS SELECT * FROM v_dept;
INSERT INTO emp VALUES (4,'Karan','HR',45000);   -- new data arrives
SELECT * FROM v_dept ORDER BY dept;               -- view re-runs
SELECT * FROM mv_dept ORDER BY dept;              -- snapshot is stale
-- PostgreSQL (not run here): CREATE MATERIALIZED VIEW mv AS SELECT ...; REFRESH MATERIALIZED VIEW mv;
```
**Output:** `v_dept` after the insert (fresh):

| dept | payroll |
|---|---|
| HR | 153000 |
| Sales | 62000 |

`mv_dept` snapshot (stale, HR still 108000):

| dept | payroll |
|---|---|
| HR | 108000 |
| Sales | 62000 |

**Edge cases:** Real materialized views (PostgreSQL, Oracle, Snowflake, BigQuery) differ in refresh rules (not run here / from memory). MySQL has no native materialized view.
**Likely follow-ups:**
- Can you update through a view? Only simple single-table views usually; aggregated views cannot be updated.
- Does a view make a query faster? No, it only reuses logic.
**Common mistakes:** Saying a view stores data; forgetting to schedule the refresh.

### Q24 ⭐⭐ 🟡 What is ETL? How is it different from ELT?
**Asked at:** commonly asked (no company-specific report found); listed in generic data-warehouse interview guides (Coursera, DataCamp per Part 11 sources).
**What the interviewer is checking:** Whether you know where the cleaning happens: before loading (ETL) or after loading, inside the warehouse (ELT).
**Say this in the interview:** ETL is Extract, Transform, Load: clean the data on a separate server and then load it. ELT loads the raw data first and transforms it inside the warehouse with SQL, which suits cloud warehouses that have cheap, powerful compute.
**Explain simply:**
- **Extract** = pull data from sources (HRMS, payroll, Excel). **Transform** = clean, join, standardise. **Load** = write into the target.
- **ETL**: transform before load. Good when you must mask or drop sensitive data before it lands.
- **ELT**: raw copy is kept, so you can re-transform later without re-extracting. Analysts write the transform step in SQL.
- Trade-off: ELT stores messy raw data too (more storage, more governance).
**Example:** Attendance exports arrive with names as ' asha ' and blank hours. ELT: land them in a `stg_att` staging table as-is, then a SQL step cleans them.
**SQL:**
```sql
-- The "T" of ELT as plain SQL (SQLite, run here)
CREATE TABLE stg_att(emp TEXT, day TEXT, hrs TEXT);
INSERT INTO stg_att VALUES (' asha ','2025-06-01','8'),('RAVI','2025-06-01',''),('Asha','2025-06-02','7.5');
CREATE TABLE att AS
SELECT UPPER(SUBSTR(TRIM(emp),1,1)) || LOWER(SUBSTR(TRIM(emp),2)) AS emp,
       day, CAST(NULLIF(hrs,'') AS REAL) AS hrs
FROM stg_att;
SELECT * FROM att;
```
**Output:**

| emp | day | hrs |
|---|---|---|
| Asha | 2025-06-01 | 8.0 |
| Ravi | 2025-06-01 | NULL |
| Asha | 2025-06-02 | 7.5 |

**Edge cases:** Blank string is not NULL; `NULLIF(hrs,'')` fixes it. Re-running the load can create duplicates unless the job is idempotent (safe to re-run).
**Likely follow-ups:**
- Which tools? Examples only: SSIS, Informatica (ETL), dbt (the T in ELT); named from memory.
- What is a staging table? A raw landing area before cleaning.
**Common mistakes:** Treating ETL and ELT as the same; thinking ELT means "no transformation".

### Q25 ⭐⭐ 🟡 What is referential integrity? What happens if you delete a parent row that has child rows (CASCADE, RESTRICT, SET NULL)?
**Asked at:** commonly asked; primary/foreign keys are reported in one Infosys candidate account (Glassdoor, Oct 2025, via search snippet, Part 11 sources).
**What the interviewer is checking:** Whether you understand foreign keys and the three delete rules.
**Say this in the interview:** Referential integrity means a child row can only point to a parent that exists. If I delete a parent, CASCADE deletes the children, RESTRICT blocks the delete, and SET NULL keeps the children but blanks the link.
**Explain simply:**
- **Parent** = `dept`; **child** = `employee` holding `dept_id` (the **foreign key**, a column that must match a parent's key).
- **CASCADE**: delete a department, its employees vanish too. Dangerous for payroll data.
- **RESTRICT / NO ACTION**: refuse to delete while children exist (the safe default).
- **SET NULL**: employees stay, but dept becomes unknown.
**Example:** Delete 'Sales' with 40 staff: CASCADE removes 40 employee rows; RESTRICT gives an error; SET NULL leaves 40 people with no department.
**SQL:**
```sql
-- SQLite (run here). Foreign keys are OFF by default in SQLite: turn them on per connection.
PRAGMA foreign_keys = ON;
CREATE TABLE dept(dept_id INT PRIMARY KEY, name TEXT);
CREATE TABLE emp_cascade (emp_id INT PRIMARY KEY, dept_id INT REFERENCES dept(dept_id) ON DELETE CASCADE);
CREATE TABLE emp_restrict(emp_id INT PRIMARY KEY, dept_id INT REFERENCES dept(dept_id) ON DELETE RESTRICT);
CREATE TABLE emp_setnull (emp_id INT PRIMARY KEY, dept_id INT REFERENCES dept(dept_id) ON DELETE SET NULL);
INSERT INTO dept VALUES (10,'HR'),(20,'Sales'),(30,'Ops');
INSERT INTO emp_cascade VALUES (1,10),(2,20);
INSERT INTO emp_restrict VALUES (1,20);
INSERT INTO emp_setnull VALUES (1,30);
INSERT INTO emp_cascade VALUES (9,99);      -- orphan insert
DELETE FROM dept WHERE dept_id = 20;        -- restricted child exists
DELETE FROM dept WHERE dept_id = 10;        -- cascade
DELETE FROM dept WHERE dept_id = 30;        -- set null
```
**Output:** Orphan insert and the delete of dept 20 both fail with `FOREIGN KEY constraint failed`. After the other deletes, `emp_cascade` has lost the dept-10 employee and `emp_setnull` has a NULL link:

| emp_id | dept_id |
|---|---|
| 2 | 20 |

(`emp_cascade`)

| emp_id | dept_id |
|---|---|
| 1 | NULL |

(`emp_setnull`)
**Edge cases:** NULL in a foreign key is allowed (no parent needed) unless the column is NOT NULL. Syntax is the same in PostgreSQL/MySQL/SQL Server (SQL Server: `ON DELETE NO ACTION`, from memory).
**Likely follow-ups:**
- Which rule for payroll? RESTRICT, so history is never lost silently.
- What is an orphan row? A child whose parent no longer exists.
**Common mistakes:** Assuming SQLite enforces foreign keys by default; using CASCADE casually.

### Q26 ⭐⭐ 🟡 What are the types of relationships between tables (one-to-one, one-to-many, many-to-many)? How is many-to-many stored?
**Asked at:** commonly asked (keys/relationships are standard DBMS theory in service-MNC question guides, Part 11 sources).
**What the interviewer is checking:** Whether you can name the three types and know the junction (bridge) table.
**Say this in the interview:** One-to-one: one employee, one passport record. One-to-many: one department, many employees. Many-to-many: employees and training courses, stored in a third table that holds one row per pair.
**Explain simply:**
- **One-to-one**: rare; usually splits sensitive or optional columns into a second table.
- **One-to-many**: the foreign key sits on the "many" side (`employee.dept_id`).
- **Many-to-many**: cannot be stored with a single column; create a **junction table** with both keys, often as a combined primary key.
- The junction table can carry its own facts (completion date).
**Example:** 2 employees and 2 courses can give 3 enrolments, not a messy comma list like `'POSH,Excel'`.
**SQL:**
```sql
-- SQLite (run here)
CREATE TABLE employee(emp_id INT PRIMARY KEY, name TEXT);
CREATE TABLE training(course_id INT PRIMARY KEY, title TEXT);
CREATE TABLE enrolment(
  emp_id INT REFERENCES employee, course_id INT REFERENCES training,
  completed_on TEXT, PRIMARY KEY (emp_id, course_id));
INSERT INTO employee VALUES (1,'Asha'),(2,'Ravi');
INSERT INTO training VALUES (101,'POSH'),(102,'Excel');
INSERT INTO enrolment VALUES (1,101,'2025-03-01'),(1,102,NULL),(2,101,'2025-03-02');
SELECT e.name, t.title, n.completed_on
FROM enrolment n JOIN employee e USING(emp_id) JOIN training t USING(course_id)
ORDER BY e.name, t.title;
```
**Output:**

| name | title | completed_on |
|---|---|---|
| Asha | Excel | NULL |
| Asha | POSH | 2025-03-01 |
| Ravi | POSH | 2025-03-02 |

**Edge cases:** The composite primary key blocks the same pair twice. Asha's NULL means enrolled but not completed.
**Likely follow-ups:**
- How do you query it? Two joins through the junction table, as above.
- Where is the foreign key in one-to-many? On the many side.
**Common mistakes:** Storing lists in one cell; putting the foreign key on the wrong side.

### Q27 ⭐⭐ 🟡 When should you NOT create an index? What are the costs of indexes?
**Asked at:** commonly asked; indexing appears in service-MNC DBMS guides and one Infosys report (Part 11 sources).
**What the interviewer is checking:** Balanced judgement: indexes speed reads but cost storage and write speed.
**Say this in the interview:** An index is like a book's index: great for finding a few rows, but it must be updated on every insert, update and delete and takes space. I skip it on small tables, columns with few distinct values, columns that are rarely filtered and heavy write tables.
**Explain simply:**
- **Index** = a sorted lookup structure (usually a B-tree) pointing to rows.
- Costs: extra disk, slower INSERT/UPDATE/DELETE, more for the optimiser to consider.
- Low-selectivity columns (gender: about half the rows match) rarely help; the engine may still read most of the table.
- Small tables and queries reading most rows are often faster with a full scan (MySQL manual, https://dev.mysql.com/doc/refman/8.4/en/mysql-indexes.html).
**Example:** 20,000 employees: `city` has about 23 rows per value (great index); `gender` splits 10,000 / 10,000 (poor index).
**SQL:**
```sql
-- SQLite (run here)
CREATE TABLE emp(emp_id INTEGER PRIMARY KEY, gender TEXT, dept TEXT, city TEXT);
-- 20,000 rows loaded: gender alternates M/F, city has 900 values
CREATE INDEX ix_g ON emp(gender);
CREATE INDEX ix_city ON emp(city);
ANALYZE;
EXPLAIN QUERY PLAN SELECT * FROM emp WHERE gender='F';
EXPLAIN QUERY PLAN SELECT * FROM emp WHERE city='C7';
SELECT COUNT(*) FROM emp WHERE gender='F';  -- 10000 rows
SELECT COUNT(*) FROM emp WHERE city='C7';   -- 23 rows
```
**Output:** Both plans say `SEARCH emp USING INDEX ix_g (gender=?)` and `SEARCH emp USING INDEX ix_city (city=?)`. The counts show the difference: `gender='F'` returns 10000 rows, `city='C7'` returns 23. SQLite still chose the gender index, which is little help when half the table matches; do not read the plan alone, look at how many rows come back.
**Edge cases:** Bulk loads are faster if you drop and rebuild indexes (general practice, from memory). Unused indexes can be found in engine-specific views (not run here).
**Likely follow-ups:**
- Does an index help `LIKE '%abc'`? No, a leading wildcard cannot use it.
- Does a function on the column help? `WHERE UPPER(name)=...` bypasses a plain index.
**Common mistakes:** Indexing every column; indexing tiny tables; forgetting write cost.

### Q28 ⭐ 🟢 What is the difference between SQL and NoSQL databases? When would you use each?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Practical awareness, not hype.
**Say this in the interview:** SQL databases store data in tables with a fixed schema and strong consistency, ideal for payroll and reporting. NoSQL covers document, key-value, column and graph stores with flexible structure and easy horizontal scaling, suited to varied or very high-volume data like logs or clickstreams.
**Explain simply:**
- **Schema** = the agreed column layout. SQL enforces it; document stores let each record differ.
- SQL gives joins and transactions; most NoSQL trades some of that for scale and flexibility (varies by product).
- Analysts mostly meet SQL; NoSQL data usually gets flattened into tables for reporting.
- They are not rivals: many companies use both.
**Example:** Payroll (fixed columns, must be exact) in SQL. Resumes with different fields per candidate as JSON documents in a document store.
**SQL:**
```sql
-- SQLite (run here): a JSON "document" column, read with json_extract
CREATE TABLE candidate_doc(id INT, doc TEXT);
INSERT INTO candidate_doc VALUES
 (1,'{"name":"Asha","skills":["SQL","Excel"]}'),
 (2,'{"name":"Ravi","skills":["Python"],"notice_days":30}');
SELECT id, json_extract(doc,'$.name') AS name,
       json_extract(doc,'$.notice_days') AS notice_days,
       json_array_length(doc,'$.skills') AS n_skills
FROM candidate_doc;
```
**Output:**

| id | name | notice_days | n_skills |
|---|---|---|---|
| 1 | Asha | NULL | 2 |
| 2 | Ravi | 30 | 1 |

**Edge cases:** Missing fields come back as NULL. This shows flexible records, not a real NoSQL engine (MongoDB etc. not run here).
**Likely follow-ups:**
- Is NoSQL always faster? No; it depends on the access pattern.
- Can SQL databases store JSON? Yes, most modern ones do.
**Common mistakes:** Saying "NoSQL has no schema at all" or "SQL cannot scale".

### Q29 ⭐ 🟢 What is an ER diagram, and what do entities, attributes and relationships mean?
**Asked at:** commonly asked; data modelling basics are reported for Flipkart and Amazon BIE rounds (research/interview_processes.md, search-summary level).
**What the interviewer is checking:** Basic modelling vocabulary.
**Say this in the interview:** An ER (Entity-Relationship) diagram is a picture of the database plan. Entities are the things we store (Employee, Department), attributes are their facts (name, salary), and relationships are how they connect (an employee works in one department).
**Explain simply:**
- **Entity** becomes a table; **attribute** becomes a column; a **relationship** becomes a foreign key or a junction table.
- **Cardinality** = how many on each side (1:1, 1:N, M:N). Crow's-foot lines show this.
- Drawing it first catches mistakes before any table is built.
**Example:**
```text
DEPARTMENT (dept_id PK, dept_name) 1 ---- N EMPLOYEE (emp_id PK, name, dept_id FK)
EMPLOYEE 1 ---- N ATTENDANCE (emp_id, work_date, status)
```
**Likely follow-ups:**
- Primary key? A column uniquely identifying a row. See Q42 for a full runnable design.
- Weak entity? An entity that needs its parent to be identified (an attendance row needs an employee).
**Common mistakes:** Turning attributes into entities needlessly; forgetting cardinality.

### Q30 ⭐ 🟢 What are the common SQL data types (INT, VARCHAR, DATE, DECIMAL)? Why does choosing the right type matter?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Whether you know wrong types give wrong answers, not just slow ones.
**Say this in the interview:** INT for whole numbers, DECIMAL for exact money, VARCHAR for text, DATE for dates. The right type saves space, enforces valid values and gives correct sorting and maths; money in a float type can produce tiny errors.
**Explain simply:**
- **INT** whole numbers; **DECIMAL(p,s)** exact fixed-point (salary); **FLOAT** approximate; **VARCHAR(n)** text; **DATE/TIMESTAMP** dates; **BOOLEAN** yes/no.
- Dates stored as text sort correctly only if written `YYYY-MM-DD`.
- Numbers stored as text sort alphabetically ('9' after '10').
- Dialect: SQLite uses flexible "type affinity" and has no real DATE type (from memory/doc knowledge); other engines enforce types strictly.
**Example:** Sum of 10,000 salaries as float can drift by paise; DECIMAL(12,2) does not.
**SQL:**
```sql
-- SQLite (run here)
SELECT 0.1+0.2 AS float_sum, 0.1+0.2=0.3 AS equals_point3,
       10/4 AS int_div, 10/4.0 AS dec_div, round(0.1+0.2,2)=0.3 AS rounded_eq;
SELECT '2025-12-01' < '2025-2-01' AS unpadded_text_says_dec_before_feb,
       '9' < '10' AS text_numbers_9_before_10, 9 < 10 AS real_numbers;
```
**Output:**

| float_sum | equals_point3 | int_div | dec_div | rounded_eq |
|---|---|---|---|---|
| 0.30000000000000004 | 0 | 2 | 2.5 | 1 |

| unpadded_text_says_dec_before_feb | text_numbers_9_before_10 | real_numbers |
|---|---|---|
| 1 | 0 | 1 |

**Edge cases:** Integer division truncates in SQLite, SQL Server and PostgreSQL (`10/4=2`); MySQL `/` gives 2.5 (from memory, not run here). Storing `'9'<'10'` returned 0 here because SQLite compared text; the text date `'2025-12-01'` was wrongly called earlier than `'2025-2-01'`.
**Likely follow-ups:**
- CHAR vs VARCHAR? CHAR is fixed length, VARCHAR variable.
- Why not store phone numbers as INT? Leading zeros and `+` are lost.
**Common mistakes:** Money in FLOAT; dates as text in mixed formats; VARCHAR(255) everywhere.

### Q31 ⭐ 🟡 What is a trigger? Give a business use case and a drawback.
**Asked at:** commonly asked; triggers appear in SQL question banks (low-reliability scribd source, Part 11 sources).
**What the interviewer is checking:** Whether you know triggers run automatically on data changes, and their hidden cost.
**Say this in the interview:** A trigger is code the database runs automatically when a row is inserted, updated or deleted. A classic use is an audit log of salary changes. The drawback is hidden logic: it slows writes and is hard to debug.
**Explain simply:**
- Fires **BEFORE** or **AFTER** an INSERT/UPDATE/DELETE; can see `OLD` and `NEW` row values.
- Good for audit trails and enforcing rules the application might skip.
- Drawbacks: invisible side effects, slower writes, cascading triggers, harder testing and migration.
- Many teams prefer explicit application or pipeline logic.
**Example:** HR changes Asha's salary from 50,000 to 55,000; the trigger writes one audit row, no one has to remember.
**SQL:**
```sql
-- SQLite syntax (run here); PostgreSQL uses a trigger function (not run here)
CREATE TABLE emp(emp_id INT PRIMARY KEY, name TEXT, salary INT);
CREATE TABLE salary_audit(emp_id INT, old_salary INT, new_salary INT, changed_at TEXT);
CREATE TRIGGER trg_sal AFTER UPDATE OF salary ON emp
WHEN OLD.salary <> NEW.salary
BEGIN
  INSERT INTO salary_audit VALUES (OLD.emp_id, OLD.salary, NEW.salary, '2025-07-01');
END;
INSERT INTO emp VALUES (1,'Asha',50000),(2,'Ravi',62000);
UPDATE emp SET salary = 55000 WHERE emp_id = 1;
UPDATE emp SET salary = 62000 WHERE emp_id = 2;   -- same value: no audit row
SELECT * FROM salary_audit;
```
**Output:**

| emp_id | old_salary | new_salary | changed_at |
|---|---|---|---|
| 1 | 50000 | 55000 | 2025-07-01 |

**Edge cases:** The `WHEN` clause avoids logging no-change updates. A bulk update of 1 lakh rows fires the trigger per row (row-level in SQLite).
**Likely follow-ups:**
- Trigger vs stored procedure? A trigger fires automatically; a procedure is called on purpose.
- Can triggers be recursive? Yes in some engines; usually limited.
**Common mistakes:** Putting heavy logic in triggers; forgetting they fire on bulk loads.

### Q32 ⭐ 🟡 What is BCNF, and how does it differ from 3NF?
**Asked at:** normalization is commonly reported (Infosys, Accenture accounts; Part 11 sources) but BCNF itself has no specific report; treat as differentiator.
**What the interviewer is checking:** Whether you understand normal forms beyond 3NF.
**Say this in the interview:** BCNF (Boyce-Codd Normal Form) is a stricter 3NF: whenever one column set determines another, the determining set must be a candidate key, a column set that could uniquely identify the row. 3NF allows an exception when the dependent column is part of a key; BCNF does not.
**Explain simply:**
- A **functional dependency** `A -> B` means: knowing A tells you B.
- 3NF: non-key columns depend on "the key, the whole key, nothing but the key". BCNF removes the leftover exception.
- Problem pattern: overlapping candidate keys.
- Fix: split the table; the cost is that some rules may need a join to enforce.
**Example:** A trainer teaches only one subject. Table `(student, subject, trainer)` has key `(student, subject)`, but `trainer -> subject`, and trainer is not a key. This is in 3NF but violates BCNF; if Mehta switches subject, you must update many rows.
**SQL:**
```sql
-- SQLite (run here)
CREATE TABLE course_slot(student TEXT, subject TEXT, trainer TEXT, PRIMARY KEY(student,subject));
INSERT INTO course_slot VALUES ('Asha','SQL','Mehta'),('Ravi','SQL','Mehta'),
                               ('Asha','Excel','Rao'),('Meena','Excel','Rao');
CREATE TABLE trainer_subject AS SELECT DISTINCT trainer, subject FROM course_slot;
CREATE TABLE student_trainer AS SELECT student, trainer FROM course_slot;
SELECT * FROM trainer_subject;
-- rebuild the original with a join: lossless
SELECT s.student, t.subject, s.trainer
FROM student_trainer s JOIN trainer_subject t USING(trainer) ORDER BY 1,2;
```
**Output:** `trainer_subject`:

| trainer | subject |
|---|---|
| Mehta | SQL |
| Rao | Excel |

The rebuild returns the same 4 rows (Asha/Excel/Rao, Asha/SQL/Mehta, Meena/Excel/Rao, Ravi/SQL/Mehta).
**Edge cases:** Every BCNF table is in 3NF, not the other way. Some designs cannot be decomposed to BCNF without losing a dependency (theory, from memory).
**Likely follow-ups:**
- Is BCNF always needed? Analytics models often denormalize anyway (Q21).
- 3NF in one line? No non-key column depends on another non-key column.
**Common mistakes:** Confusing it with 4NF; saying it is "3NF with more tables" without the key rule.

### Q33 ⭐ 🟡 What are transaction isolation levels and the problems they prevent (dirty read, non-repeatable read, phantom read)?
**Asked at:** ACID and transactions are commonly reported in service-MNC theory rounds (Part 11 sources); isolation levels specifically have no company report.
**What the interviewer is checking:** Whether you know the four levels and the three anomalies.
**Say this in the interview:** Isolation decides how much one running transaction can see of another's work. Stricter levels prevent more anomalies but allow less concurrency. A dirty read sees uncommitted data, a non-repeatable read sees a row change between two reads, and a phantom read sees new rows appear.
**Explain simply:**
- **Transaction** = a group of statements that succeed or fail together.
- **Dirty read**: reading another transaction's uncommitted change (it may be rolled back).
- **Non-repeatable read**: same row, different value on the second read.
- **Phantom read**: same query, extra rows on the second run.
**Example:** HR report reads headcount = 100, a hire is committed, the report re-reads and gets 101 mid-report: a phantom.

| Level | Dirty read | Non-repeatable | Phantom (SQL standard) |
|---|---|---|---|
| Read Uncommitted | allowed | allowed | allowed |
| Read Committed | blocked | allowed | allowed |
| Repeatable Read | blocked | blocked | allowed |
| Serializable | blocked | blocked | blocked |

Source: PostgreSQL docs, https://www.postgresql.org/docs/current/transaction-iso.html. PostgreSQL treats Read Uncommitted as Read Committed, defaults to Read Committed, and its Repeatable Read also prevents phantoms; Serializable failures raise error 40001 and the app must retry.
**SQL:**
```sql
-- Not run here (SQLite has no per-transaction isolation levels; it is effectively serializable). PostgreSQL:
BEGIN ISOLATION LEVEL REPEATABLE READ;
SELECT COUNT(*) FROM employees;
-- another session inserts and commits here
SELECT COUNT(*) FROM employees;  -- same count under Repeatable Read in PostgreSQL
COMMIT;
```
**Edge cases:** MySQL InnoDB defaults to Repeatable Read (from memory, not run here); SQL Server defaults to Read Committed (from memory).
**Likely follow-ups:**
- Which level for a monthly payroll report? Repeatable Read or snapshot-style, so numbers stay consistent.
- Cost of Serializable? More blocking or retries.
**Common mistakes:** Mixing up non-repeatable and phantom; assuming every engine implements levels identically.

### Q34 ⭐ 🟡 What is a slowly changing dimension (Type 1, Type 2, Type 3)? Give an HR example such as an employee changing department.
**Asked at:** SCD types 1/2/3 are listed in generic data-warehouse guides (Coursera, DataCamp; Part 11 sources); no company-specific report found.
**What the interviewer is checking:** Whether you know how to keep or overwrite history in a dimension table.
**Say this in the interview:** A slowly changing dimension handles attributes that change rarely, like an employee's department. Type 1 overwrites and loses history, Type 2 adds a new row with validity dates, Type 3 keeps the old value in an extra column.
**Explain simply:**
- **Dimension** = descriptive table (employee, department) used to slice numbers.
- **Type 1**: overwrite. Simple, but old reports change retroactively.
- **Type 2**: new row per change with `valid_from`, `valid_to`, `is_current`, plus a new surrogate key. Full history. Most common in practice.
- **Type 3**: add a `prev_dept` column; only one step of history. (Names per Kimball: https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/ ; definitions here are from memory.)
**Example:** Asha moves from HR to Analytics on 1 Jul 2025. Her May 2024 salary should still count under HR.
**SQL:**
```sql
-- SQLite (run here): Type 2
CREATE TABLE dim_emp2(sk INTEGER PRIMARY KEY AUTOINCREMENT, emp_id INT, name TEXT, dept TEXT,
                      valid_from TEXT, valid_to TEXT, is_current INT);
INSERT INTO dim_emp2(emp_id,name,dept,valid_from,valid_to,is_current) VALUES
 (1,'Asha','HR','2023-04-01','9999-12-31',1),(2,'Ravi','Sales','2022-01-01','9999-12-31',1);
-- change: close the old row, insert the new one
UPDATE dim_emp2 SET valid_to='2025-06-30', is_current=0 WHERE emp_id=1 AND is_current=1;
INSERT INTO dim_emp2(emp_id,name,dept,valid_from,valid_to,is_current)
VALUES (1,'Asha','Analytics','2025-07-01','9999-12-31',1);
SELECT * FROM dim_emp2;
-- as-was reporting
CREATE TABLE fact_pay(emp_id INT, pay_date TEXT, amount INT);
INSERT INTO fact_pay VALUES (1,'2024-05-31',50000),(1,'2025-08-31',60000);
SELECT d.dept, SUM(f.amount) AS paid
FROM fact_pay f JOIN dim_emp2 d ON d.emp_id=f.emp_id AND f.pay_date BETWEEN d.valid_from AND d.valid_to
GROUP BY d.dept ORDER BY d.dept;
-- Type 1:  UPDATE dim SET dept='Analytics' WHERE emp_id=1;
-- Type 3:  UPDATE dim SET prev_dept=dept, dept='Analytics' WHERE emp_id=1;
```
**Output:** Type 2 table after the change:

| sk | emp_id | name | dept | valid_from | valid_to | is_current |
|---|---|---|---|---|---|---|
| 1 | 1 | Asha | HR | 2023-04-01 | 2025-06-30 | 0 |
| 2 | 2 | Ravi | Sales | 2022-01-01 | 9999-12-31 | 1 |
| 3 | 1 | Asha | Analytics | 2025-07-01 | 9999-12-31 | 1 |

As-was payroll by department:

| dept | paid |
|---|---|
| Analytics | 60000 |
| HR | 50000 |

Type 1 result: `(1, Analytics)`, history lost. Type 3 result: `(1, Analytics, prev_dept=HR)`, both run here.
**Edge cases:** Real pipelines fact-join on the surrogate key assigned at load; the date join above is for demonstration. Two changes in one day need a rule. Types 0, 4 and 6 exist (Kimball names).
**Likely follow-ups:**
- Which type for attrition by department? Type 2.
- What is a surrogate key? A system-made ID unique per row version.
**Common mistakes:** Updating a Type 2 table in place; forgetting to close the old row.

### Q35 ⭐ 🟡 What is a data mart, and how is it different from a data warehouse and a data lake?
**Asked at:** commonly asked in generic DW guides (Coursera, DataCamp; Part 11 sources); no company-specific report found.
**What the interviewer is checking:** Scope and structure differences.
**Say this in the interview:** A data warehouse is the company-wide, cleaned, structured store for reporting. A data mart is a smaller slice for one team, like HR. A data lake holds raw data of any format, structured or not, to be shaped later.
**Explain simply:**

| | Data lake | Data warehouse | Data mart |
|---|---|---|---|
| Data | raw, any format | cleaned, structured | subset for one function |
| Schema | applied when reading | designed up front | designed up front |
| Users | data engineers, scientists | analysts, BI | one department |
| Example | resume PDFs, logs | all HR, finance, sales tables | HR attrition mart |

- A mart can be carved out of a warehouse, or built directly from sources (definitions from memory/textbook).
**Example:** The HR mart holds headcount, attrition and hiring tables so HR analysts do not touch finance tables.
**Likely follow-ups:**
- What is a lakehouse? A newer design merging lake storage with warehouse-style tables (from memory).
- Where do you work as an analyst? Mostly warehouse and marts.
**Common mistakes:** Saying a lake is "just a bigger warehouse"; ignoring governance (a lake without rules becomes a swamp).

### Q36 ⭐ 🟡 What is a temporary table, and how does it differ from a CTE or a table variable?
**Asked at:** commonly asked (no company-specific report found).
**What the interviewer is checking:** Scope, lifetime and reuse differences.
**Say this in the interview:** A temp table is a real table that lives for my session, so I can index it and reuse it many times. A CTE is a named subquery that exists only for one statement. A table variable is a SQL Server/T-SQL object scoped to a batch.
**Explain simply:**
- **Temp table** (`CREATE TEMP TABLE` / `#t` in SQL Server): stored, reusable across statements, dropped at session end.
- **CTE** (`WITH ... AS`): readable, one statement only, not stored (some engines may reuse its result, engine-specific).
- **Table variable** (`DECLARE @t TABLE`, SQL Server, not run here): smaller scope; often used for small row counts (from memory).
- Use a temp table for large intermediate results reused several times; use a CTE for readability.
**Example:** Employees paid at least 50,000 are needed in three later queries: store once.
**SQL:**
```sql
-- SQLite (run here)
CREATE TABLE emp(emp_id INT, dept TEXT, salary INT);
INSERT INTO emp VALUES (1,'HR',50000),(2,'HR',58000),(3,'Sales',62000),(4,'Sales',40000);
WITH hi AS (SELECT * FROM emp WHERE salary >= 50000)       -- gone after this statement
SELECT dept, COUNT(*) AS n FROM hi GROUP BY dept ORDER BY dept;
CREATE TEMP TABLE tmp_high AS SELECT * FROM emp WHERE salary >= 50000;
SELECT dept, COUNT(*) AS n FROM tmp_high GROUP BY dept ORDER BY dept;   -- reusable
```
**Output:** Both queries return the same result:

| dept | n |
|---|---|
| HR | 2 |
| Sales | 1 |

`sqlite_temp_master` lists `tmp_high` (type table) while the connection is open; the CTE leaves no object.
**Edge cases:** Temp tables disappear when the session ends. Table variables are not available in SQLite, PostgreSQL or MySQL.
**Likely follow-ups:**
- Can a CTE be recursive? Yes (Part on recursive CTEs).
- Temp table vs view? A view is a saved query; a temp table is saved data.
**Common mistakes:** Expecting a CTE to persist; forgetting to drop temp tables in long sessions.

### Q37 ⭐ 🟡 What is a deadlock, and how can it be avoided?
**Asked at:** commonly asked in DBMS theory lists; no company-specific report found.
**What the interviewer is checking:** Whether you understand circular waiting and practical prevention.
**Say this in the interview:** A deadlock is when two transactions each hold a lock the other needs, so both wait forever. The database detects it and kills one as the victim. To avoid it, access tables in the same order, keep transactions short and lock only what you need.
**Explain simply:**
- **Lock** = a claim on a row/table so others cannot change it meanwhile.
- Circular wait: T1 holds A wants B; T2 holds B wants A.
- Prevent: consistent update order, short transactions, no user prompts inside a transaction, proper indexes (fewer rows locked), retry the victim.
**Example:**
```text
T1: UPDATE payroll row 1   ... then wants row 2
T2: UPDATE payroll row 2   ... then wants row 1   -> deadlock
Fix: both update rows in ascending emp_id order.
```
**SQL:**
```sql
-- Not run here: needs two concurrent sessions, which a single script cannot show.
-- Session 1: BEGIN; UPDATE payroll SET amount = amount+1 WHERE emp_id = 1;
-- Session 2: BEGIN; UPDATE payroll SET amount = amount+1 WHERE emp_id = 2;
-- Session 1: UPDATE payroll SET amount = amount+1 WHERE emp_id = 2;   -- waits
-- Session 2: UPDATE payroll SET amount = amount+1 WHERE emp_id = 1;   -- deadlock detected, one aborted
```
**Edge cases:** SQLite uses a database-level write lock, so classic row deadlocks do not occur the same way (from memory). An aborted transaction must be retried by the application.
**Likely follow-ups:**
- Deadlock vs a plain lock wait? A lock wait ends when the holder commits; a deadlock never would.
- How does the DB resolve it? Picks a victim and rolls it back.
**Common mistakes:** Calling any slow query a deadlock; not retrying the failed transaction.

### Q38 ⭐ 🟡 What is table partitioning, and how does it help with large tables?
**Asked at:** commonly asked in DBMS curricula; no company-specific report found (gap-fill topic).
**What the interviewer is checking:** Whether you know partitioning splits one big table into pieces and speeds queries by skipping pieces.
**Say this in the interview:** Partitioning splits a very large table into smaller physical parts, usually by date. A query filtered on date only reads the matching parts, and old data can be dropped instantly by removing a partition.
**Explain simply:**
- Methods: **range** (by month), **list** (by region), **hash** (spread evenly).
- **Partition pruning** = the engine skips partitions that cannot match the WHERE clause.
- Dropping or detaching an old partition is far faster than a bulk DELETE.
- Worth it only for very large tables; PostgreSQL docs say roughly bigger than server memory (https://www.postgresql.org/docs/current/ddl-partitioning.html).
**Example:** 10 crore attendance rows partitioned by month: "June 2025" touches 1 partition; archiving 2022 is a single drop.
**SQL:**
```sql
-- Not run here: SQLite has no table partitioning. PostgreSQL syntax:
CREATE TABLE attendance (emp_id INT, work_date DATE, status TEXT) PARTITION BY RANGE (work_date);
CREATE TABLE attendance_2025_06 PARTITION OF attendance
  FOR VALUES FROM ('2025-06-01') TO ('2025-07-01');
SELECT COUNT(*) FROM attendance WHERE work_date >= '2025-06-01' AND work_date < '2025-07-01';  -- prunes
```
**Edge cases:** Filtering on a non-partition column gives no pruning. A function on the date column can defeat pruning. Too many tiny partitions add overhead.
**Likely follow-ups:**
- Partitioning vs indexing? Indexes find rows; partitions skip chunks. Often used together.
- Partitioning vs sharding? Sharding spreads data across servers.
**Common mistakes:** Partitioning small tables; choosing a key queries never filter on.

### Q39 ⭐ 🟡 How do you read a query execution plan (EXPLAIN) at a basic level to spot a missing index?
**Asked at:** commonly asked in performance rounds; no company-specific report found.
**What the interviewer is checking:** Whether you can tell a full scan from an index lookup.
**Say this in the interview:** I run EXPLAIN and look for a full table scan on a big table where I filter or join. I add an index on the filtered column, run EXPLAIN again and check it now says index search, then compare real run time.
**Explain simply:**
- **Execution plan** = the engine's step-by-step method for your query.
- SQLite: `SCAN` = whole table, `SEARCH ... USING INDEX` = index lookup, `COVERING INDEX` = answered from the index alone.
- PostgreSQL: Seq Scan vs Index Scan vs Bitmap Scan; `cost` is in arbitrary units, not milliseconds; a big gap between estimated and actual rows usually means stale statistics (run ANALYZE). `EXPLAIN ANALYZE` actually executes the statement, so wrap INSERT/UPDATE/DELETE in BEGIN...ROLLBACK (https://www.postgresql.org/docs/current/using-explain.html).
- Small tables may legitimately scan.
**Example:** Find Hyderabad-style employees by dept and city in a 20,000-row table.
**SQL:**
```sql
-- SQLite (run here)
CREATE TABLE emp(emp_id INTEGER PRIMARY KEY, dept_id INT, city TEXT, salary INT, name TEXT);
-- 20,000 rows loaded
EXPLAIN QUERY PLAN SELECT name FROM emp WHERE dept_id=7 AND city='C27';   -- before
CREATE INDEX ix_dept ON emp(dept_id);  ANALYZE;
EXPLAIN QUERY PLAN SELECT name FROM emp WHERE dept_id=7 AND city='C27';   -- after
CREATE INDEX ix_dept_city_sal ON emp(dept_id, city, salary);
EXPLAIN QUERY PLAN SELECT salary FROM emp WHERE dept_id=7 AND city='C27'; -- covering
```
**Output:** The `detail` column of each plan:

| step | detail |
|---|---|
| before | SCAN emp |
| after single index | SEARCH emp USING INDEX ix_dept (dept_id=?) |
| composite, only index columns needed | SEARCH emp USING COVERING INDEX ix_dept_city_sal (dept_id=? AND city=?) |

**Edge cases:** Plan wording differs by engine and version (SQL Server: Index Scan vs Index Seek, from memory, not run here). The plan shows intent; confirm with real timings.
**Likely follow-ups:**
- EXPLAIN vs EXPLAIN ANALYZE? The first estimates, the second runs it and reports actuals.
- Index exists but unused? Function on the column, type mismatch, low selectivity or stale statistics.
**Common mistakes:** Adding indexes without re-checking the plan; reading cost as seconds.

### Q40 ⭐ 🟡 What is a composite index, and does the order of its columns matter?
**Asked at:** commonly asked as a follow-up to indexing; no company-specific report found.
**What the interviewer is checking:** The leftmost-prefix idea.
**Say this in the interview:** A composite index covers several columns together, like sorting a phone book by last name then first name. Order matters: it works best when the query filters on the leftmost columns, so (dept_id, city) helps dept alone or dept plus city, but is usually poor for city alone.
**Explain simply:**
- Sorted by the first column, ties sorted by the second, and so on.
- Equality on leading columns plus one range on the next narrows the search; later columns are checked inside the index (PostgreSQL docs, https://www.postgresql.org/docs/current/indexes-multicolumn.html; MySQL calls it leftmost prefix).
- Put the most commonly filtered, equality-tested column first; avoid more than about 3 columns.
- Newer engines can skip the leading column when it has few distinct values (PostgreSQL 18 skip scan; SQLite does it after ANALYZE, seen below).
**Example:** Index on `(dept_id, city)`.
**SQL:**
```sql
-- SQLite (run here)
CREATE TABLE emp(emp_id INTEGER PRIMARY KEY, dept_id INT, city TEXT, salary INT);
-- 20,000 rows: 20 depts, 100 cities
CREATE INDEX ix_dc ON emp(dept_id, city);  ANALYZE;
EXPLAIN QUERY PLAN SELECT * FROM emp WHERE dept_id=7 AND city='C27';
EXPLAIN QUERY PLAN SELECT * FROM emp WHERE dept_id=7;
EXPLAIN QUERY PLAN SELECT * FROM emp WHERE city='C27';
EXPLAIN QUERY PLAN SELECT * FROM emp WHERE dept_id=7 AND city>'C5';
```
**Output:**

| query filters on | plan detail |
|---|---|
| dept_id and city | SEARCH emp USING INDEX ix_dc (dept_id=? AND city=?) |
| dept_id only | SEARCH emp USING INDEX ix_dc (dept_id=?) |
| city only | SEARCH emp USING INDEX ix_dc (ANY(dept_id) AND city=?) |
| dept_id and city range | SEARCH emp USING INDEX ix_dc (dept_id=? AND city>?) |

The city-only line is SQLite's skip-scan: it works because dept_id has only 20 values after ANALYZE. With many distinct leading values it would not be efficient.
**Edge cases:** `ORDER BY dept_id, city` can also use the index. Wrong order can leave a frequent query with a full scan.
**Likely follow-ups:**
- (a,b) vs (b,a)? Different indexes; choose by the filters you use most.
- Two single-column indexes instead? Engines may combine them but a composite is usually better for AND filters.
**Common mistakes:** Assuming order does not matter; putting a range column before equality columns.

### Q41 ⭐ 🟡 What is the grain of a fact table, and why must you define it before building reports?
**Asked at:** data modelling and star schema appear in Flipkart and Amazon BIE reports (research/interview_processes.md, search-summary level); definitions here are textbook, from memory.
**What the interviewer is checking:** That you decide what one row means before choosing columns, to avoid double counting.
**Say this in the interview:** The grain is exactly what one row of the fact table represents, such as one employee per day. I fix it first, because every measure and dimension must fit that grain; mixing grains double counts numbers.
**Explain simply:**
- **Fact table** = measurable events (hours worked, revenue). **Grain** = the level of one row.
- Write it as a sentence: "one row per employee per day".
- Finer grain (daily) can be rolled up to month; a monthly table can never be split back to days.
- Joining two facts of different grain multiplies rows (fan-out).
**Example:** Payroll is monthly (1 row per employee-month); attendance is daily. Joining them directly repeats salary per attendance day.
**SQL:**
```sql
-- SQLite (run here)
CREATE TABLE fact_att(emp_id INT, day TEXT, hours REAL);
INSERT INTO fact_att VALUES (1,'2025-06-01',8),(1,'2025-06-02',8),(2,'2025-06-01',9);
CREATE TABLE fact_pay(emp_id INT, month TEXT, amount INT);
INSERT INTO fact_pay VALUES (1,'2025-06',50000),(2,'2025-06',62000);
SELECT SUM(p.amount) AS wrong_payroll
FROM fact_pay p JOIN fact_att a ON a.emp_id = p.emp_id;     -- mixed grain
SELECT SUM(amount) AS right_payroll FROM fact_pay;
```
**Output:**

| wrong_payroll |
|---|
| 162000 |

| right_payroll |
|---|
| 112000 |

Employee 1's 50,000 was counted twice because that employee has two attendance rows.
**Edge cases:** Duplicate rows at the stated grain mean a data problem; test with `GROUP BY` on the grain columns `HAVING COUNT(*)>1`.
**Likely follow-ups:**
- Grain of a hiring funnel? One row per candidate per stage change, or per candidate per day.
- Fix mixed grain? Aggregate to the common grain before joining.
**Common mistakes:** Adding columns first and discovering the grain later; summing a monthly measure across daily rows.

### Q42 ⭐ 🔴 Design a simple database for an HR system (employees, departments, salaries, attendance): tables, keys and relationships.
**Asked at:** data modelling is reported for Amazon BIE (GfG, early 2023) and Flipkart (2022 senior review, via search summary) in research/interview_processes.md; HR schema itself is an editorial example.
**What the interviewer is checking:** Whether you separate entities, choose keys and constraints, and keep salary history.
**Say this in the interview:** Four tables: department, employee, salary_history and attendance. Employee points to department and to its manager (self-reference); salary history keeps one row per change so past pay is never overwritten; attendance has one row per employee per day, enforced by a composite primary key.
**Explain simply:**
- One department has many employees (1:N); one employee has many salary rows and many attendance rows (1:N).
- **Manager** is a foreign key from employee to employee (a self join).
- Salary lives in its own table so history is kept, not overwritten (SCD idea, Q34).
- Constraints (NOT NULL, UNIQUE, CHECK) block bad data at the door.
```text
department 1---N employee 1---N salary_history
                   | 1---N attendance      (employee.manager_id -> employee.emp_id)
```
**SQL:**
```sql
-- SQLite (run here); foreign keys need PRAGMA foreign_keys=ON in SQLite
PRAGMA foreign_keys=ON;
CREATE TABLE department(dept_id INTEGER PRIMARY KEY, dept_name TEXT NOT NULL UNIQUE);
CREATE TABLE employee(
  emp_id INTEGER PRIMARY KEY, emp_name TEXT NOT NULL, email TEXT UNIQUE,
  dept_id INTEGER NOT NULL REFERENCES department(dept_id),
  manager_id INTEGER REFERENCES employee(emp_id),
  hire_date TEXT NOT NULL, left_date TEXT);
CREATE TABLE salary_history(
  emp_id INTEGER NOT NULL REFERENCES employee(emp_id),
  effective_from TEXT NOT NULL, monthly_salary NUMERIC NOT NULL CHECK(monthly_salary>0),
  PRIMARY KEY(emp_id,effective_from));
CREATE TABLE attendance(
  emp_id INTEGER NOT NULL REFERENCES employee(emp_id),
  work_date TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN('P','A','L','WFH')),
  PRIMARY KEY(emp_id,work_date));
-- sample rows: 2 departments, 3 employees, 3 salary rows, 3 attendance rows
SELECT e.emp_name, d.dept_name, m.emp_name AS manager,
  (SELECT monthly_salary FROM salary_history s WHERE s.emp_id=e.emp_id ORDER BY effective_from DESC LIMIT 1) AS current_salary,
  (SELECT COUNT(*) FROM attendance a WHERE a.emp_id=e.emp_id AND a.status='L') AS leave_days
FROM employee e JOIN department d USING(dept_id) LEFT JOIN employee m ON m.emp_id=e.manager_id
ORDER BY e.emp_id;
```
**Output:**

| emp_name | dept_name | manager | current_salary | leave_days |
|---|---|---|---|---|
| Meena | HR | NULL | NULL | 0 |
| Asha | Analytics | Meena | 56000 | 1 |
| Ravi | Analytics | Asha | 62000 | 0 |

Constraint tests (run): a second attendance row for the same employee and date fails with `UNIQUE constraint failed: attendance.emp_id, attendance.work_date`; attendance for non-existent employee 99 fails with `FOREIGN KEY constraint failed`.
**Edge cases:** Meena (the top manager) has NULL manager and no salary rows, so LEFT JOINs and NULL handling matter. Leaving staff keep their rows (`left_date`) rather than being deleted. Store salary as DECIMAL in other engines (Q30). Sensitive columns need access control (not run here).
**Likely follow-ups:**
- Employee changes department? Add a department-history table (Type 2, Q34).
- Reporting design? Build a star schema on top (Q43).
**Common mistakes:** Salary as a column on employee (history lost); no composite key on attendance; text dates in mixed formats.

### Q43 ⭐ 🔴 How would you design a star schema for a sales or hiring-funnel report? Name the fact table, dimensions and measures.
**Asked at:** star schema is reported in Flipkart's 2022 senior review and Amazon BIE data-modelling rounds (research/interview_processes.md, search-summary level) and in generic DW guides (Part 11 sources).
**What the interviewer is checking:** That you set the grain, then name fact, dimensions and measures, and can query it.
**Say this in the interview:** I state the grain first, say one row per order line. The fact table holds the measures, quantity and revenue, plus foreign keys to dimension tables for date, product and customer. Reports are then simple joins and GROUP BYs.
**Explain simply:**
- **Fact table** = numbers to add up; **dimensions** = the who/what/when used to slice; **measure** = a numeric column to aggregate.
- **Star** = one fact in the centre, dimensions around it, one join each (snowflake normalises dimensions further, Q22).
- Hiring funnel version: grain = one row per candidate per stage; dimensions = date, job, recruiter, source, stage; measures = candidate count, days in stage.
- Use surrogate integer keys in dimensions (Q34).
**Example (sales):** June: laptop 55,000 to Pune; July: laptops 1,10,000 and stationery to Hyderabad.
**SQL:**
```sql
-- SQLite (run here)
CREATE TABLE dim_date(date_key INTEGER PRIMARY KEY, full_date TEXT, month TEXT, year INT);
CREATE TABLE dim_product(product_key INTEGER PRIMARY KEY, product_name TEXT, category TEXT);
CREATE TABLE dim_customer(customer_key INTEGER PRIMARY KEY, customer_name TEXT, city TEXT);
CREATE TABLE fact_sales(date_key INT REFERENCES dim_date, product_key INT REFERENCES dim_product,
  customer_key INT REFERENCES dim_customer, order_id INT, qty INT, revenue REAL);
INSERT INTO dim_date VALUES (20250601,'2025-06-01','2025-06',2025),(20250702,'2025-07-02','2025-07',2025);
INSERT INTO dim_product VALUES (1,'Pen','Stationery'),(2,'Laptop','Electronics'),(3,'Notebook','Stationery');
INSERT INTO dim_customer VALUES (1,'Asha','Hyderabad'),(2,'Ravi','Pune');
INSERT INTO fact_sales VALUES (20250601,1,1,501,10,100),(20250601,2,2,502,1,55000),
                              (20250702,3,1,503,5,250),(20250702,2,1,504,2,110000);
SELECT d.month, p.category, c.city, SUM(f.revenue) AS revenue, SUM(f.qty) AS units
FROM fact_sales f JOIN dim_date d USING(date_key) JOIN dim_product p USING(product_key)
JOIN dim_customer c USING(customer_key)
GROUP BY d.month, p.category, c.city ORDER BY d.month, p.category, c.city;
```
**Output:**

| month | category | city | revenue | units |
|---|---|---|---|---|
| 2025-06 | Electronics | Pune | 55000.0 | 1 |
| 2025-06 | Stationery | Hyderabad | 100.0 | 10 |
| 2025-07 | Electronics | Hyderabad | 110000.0 | 2 |
| 2025-07 | Stationery | Hyderabad | 250.0 | 5 |

**Edge cases:** Non-additive measures (prices, ratios) should not be summed; store the components. Unknown dimension values need a default "Unknown" row. Order-level amounts repeated on each line cause double counting (Q41).
**Likely follow-ups:**
- Why a date dimension? Month, quarter, weekday and holiday flags without date functions.
- Why not one big table? It repeats text, is harder to maintain and slower to scan in row stores (denormalisation trade-off, Q21).
**Common mistakes:** Skipping the grain; putting measures in dimensions; joining dimension to dimension.

### Q44 ⭐ 🔴 What is the CAP theorem, and why do analytics databases often relax consistency?
**Asked at:** advanced and rare for DA roles; commonly asked only for data-engineering style rounds (no company-specific report found). Keep the answer short.
**What the interviewer is checking:** Awareness, not depth.
**Say this in the interview:** CAP says a distributed database facing a network partition must choose between Consistency (everyone sees the same latest data) and Availability (every request gets an answer). Many analytics and NoSQL systems accept slightly stale reads to stay fast and available, because a report can tolerate being a few minutes behind.
**Explain simply:**
- **Consistency**: all copies agree. **Availability**: the system always responds. **Partition tolerance**: it keeps working when servers cannot talk to each other.
- Partitions happen in real networks, so the real choice is C or A during a failure.
- Payroll writes favour consistency; dashboards and logs can accept **eventual consistency** (copies agree after a short delay).
**Example:** Two data centres lose contact: a payroll system rejects writes (consistent, not available); a clicks dashboard keeps serving slightly old counts (available, not consistent).
**Edge cases:** CAP applies to distributed systems only; a single-server database is not a CAP case. Not run here: needs a cluster.
**Likely follow-ups:**
- Is a SQL database always CP? No, it depends on the product and setup.
**Common mistakes:** Saying you can pick any 2 of 3 freely; applying CAP to a single laptop database.

