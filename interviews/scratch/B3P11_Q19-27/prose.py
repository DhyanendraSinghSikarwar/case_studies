Q = {}

Q[19] = dict(
say="A three-table join multiplies each order row by its item rows, so any order-level column (SUM(order_total)) is counted once per item; aggregate each child to the grain of the key you join on (one row per customer) before joining, and the totals are right and the join input is smaller.",
schema="""CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_total INTEGER);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, qty INTEGER, price INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chen');
INSERT INTO orders VALUES (10,1,100),(11,1,50),(12,2,70);
INSERT INTO order_items VALUES (1,10,1,60),(2,10,2,20),(3,10,1,0),(4,11,3,10),(5,11,1,20),(6,12,2,35);""",
sql_intro="`NAIVE` (the wrong one), `FIX_DERIVED` (one derived table per child) and `FIX_CTE` (items rolled up to order grain in a CTE, then orders to customer grain) are in the Code block, copied here.",
sql=["NAIVE", "FIX_DERIVED", "FIX_CTE"],
pd_intro="Aggregate each side with `groupby`, then merge at customer grain (the same idea as the SQL fix).",
pd=("pandas_answer",),
example="Asha has orders 10 (total 100, three items) and 11 (total 50, two items); Ben has order 12 (total 70, one item); Chen has no orders. The naive join returns one row per item: order 10 appears 3 times and order 11 twice, so SUM(order_total) for Asha is 100*3 + 50*2 = 400, but the true revenue is 100 + 50 = 150. Her item quantity is right in both forms (1+2+1 + 3+1 = 8) because `qty` lives at the item grain, and COUNT(DISTINCT order_id) = 2 is right only because of DISTINCT. Ben: 70 and 2 are right (one item, no fan-out). Chen: the naive form gives NULL revenue and quantity (the LEFT JOIN found nothing), the fixed forms give 0 through COALESCE. At scale (seed 19) the true SUM(order_total) is 25,505,616 and the naive query returns 103,626,730, a factor of 4.06 (about the 4 items per order).",
edge=["Customers with no orders (1,106 of the 20,000 here, including ids 19,001 to 20,000 which get none by construction) come out as NULL in the naive query and 0 in the fixed ones; the pandas answer fills them with 0 too. The assertion compares all 20,000 rows.",
      "Orders with no items still survive the LEFT JOINs (once, with NULL qty). The naive join returned 407,514 rows: 400,000 item rows plus 1,106 customers without orders plus 6,408 orders without items (400,000 + 1,106 + 6,408).",
      "Which columns are wrong depends on their grain: order-level measures (order_total) inflate, item-level measures (qty) do not, and COUNT(*) on the joined rows counts items, not orders. Only the first is silent; always check the grain of each column."],
explain=["Fan-out is a correctness problem and a cost problem at once: the join output has one row per item (here 407,514 rows against 100,000 orders), so everything after the join (GROUP BY, DISTINCT, sort) works on the multiplied row count.",
         "Aggregating before joining makes each join input one row per key: `oa` is one row per customer from orders, `ia` one row per customer from items. The grain check is a query: `SELECT MAX(c) FROM (SELECT COUNT(*) c FROM t GROUP BY key)` must be 1 on the side you treat as 'one row per key' (printed in the run: orders per order_id 1, items per order_id up to 3).",
         "Cost, honestly measured: VM steps were 7,782,137 for the naive join, 6,848,055 for the derived-table fix (about 12% fewer) and 9,116,103 for the CTE form, which is MORE than the naive query. The two fixed forms still have to read all 400,000 item rows, and each materialised child gets an automatic covering index (see the plans: `MATERIALIZE`, `BLOOM FILTER`, `AUTOMATIC COVERING INDEX`). In SQLite with indexed foreign keys the saving on this shape is modest; the decisive win is correctness. Without the two foreign-key indexes all three were slower (11,125,387, 9,448,060 and 11,716,107 steps).",
         "The chasm trap (Part 2 Q13) is the same fault with two sibling children (orders and, say, payments) joined to one customer: each child multiplies the other. Pre-aggregating each child to the customer grain is the standard fix. See Part 2 Q12 for fan-out inflating SUM and Part 2 Q18 for joining to an aggregated derived table.",
         "COUNT(DISTINCT) or SUM(DISTINCT) are not repairs: SUM(DISTINCT order_total) drops legitimately equal totals."],
follow=["Why did the CTE version take more steps than the naive join? (Two materialisations plus two automatic indexes; steps count work, not elapsed time, and the effect depends on the data.)",
        "How would you do this in a warehouse? (Same pre-aggregation; planner behaviour and costs on PostgreSQL, MySQL, BigQuery or Snowflake were not executed here.)",
        "What if items must stay at item grain (revenue = SUM(qty*price))? Then sum at item grain first, then roll up: the grain stays explicit."],
mist=["Adding DISTINCT to a SUM to 'fix' double counting.",
      "Trusting COUNT(*) after a one-to-many join to mean orders.",
      "Using an INNER JOIN to the aggregated child and silently dropping customers without orders (use LEFT JOIN and COALESCE).",
      "Joining two sibling child tables to one parent and aggregating after the join."],
)

Q[20] = dict(
say="The correlated scalar subquery re-runs the department average once per outer row (about n*n work with no index, n times an index range with one), while a derived table or a window computes each department once; SQLite does not decorrelate for you and builds no automatic index for that inner scan, so rewrite it.",
schema="""CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, dept_id INTEGER, salary INTEGER, hire_date TEXT);
INSERT INTO employees VALUES (1,10,100,'2020-01-01'),(2,10,200,'2021-01-01'),(3,10,300,'2022-01-01'),
 (4,20,50,'2020-05-01'),(5,20,50,'2021-05-01'),(6,30,70,'2023-01-01');""",
sql_intro="`A` is the correlated scalar subquery, `B` the join to a pre-aggregated derived table, `C` the window; all three are in the Code block, copied here.",
sql=["A", "B", "C"],
pd_intro="`groupby().transform('mean')` is the window version; the comparison is a boolean mask.",
pd=("pandas_answer",),
example="Dept 10 has salaries 100, 200, 300 (average 200): only employee 3 (300) earns more. Dept 20 has 50 and 50 (average 50): nobody earns MORE than the average, so both are excluded (the strict > matters). Dept 30 has one employee, equal to its own average: excluded. Result: emp_id 3 for all three forms (printed as `tiny A/B/C [3]`).",
edge=["Ties and a single-person department return nothing, because salary > average is false when equal. Use >= only if the question says so.",
      "NULL salaries are ignored by AVG and never satisfy salary > avg; an employee with NULL dept_id gets a NULL average in the correlated form and in B (the equality never matches), so those rows are dropped, but the window form puts all NULL-dept rows in one partition and compares them with that partition's average, so the forms can differ. Reasoned from the rules, not run; there are no NULL departments in this data.",
      "AVG returns a float: the comparison is exact here because integer salaries make sums exact, but with REAL columns compare with a tolerance in tests."],
explain=["Cost (VM steps, deterministic proxy). Correlated form, NO index: 1,010,385 steps at 500 rows, 4,025,775 at 1,000 and 16,071,237 at 2,000, i.e. 4.0 steps times n squared every time (doubling the table quadruples the work). Extrapolating by that ratio to 50,000 rows gives about 1.0e10 steps; that number is an estimate and was NOT run.",
         "At 50,000 rows without an index only B (1,404,036 steps) and C (2,426,239) were run. With an index on (dept_id, salary): A 51,076,033, B 628,860, C 2,026,237 steps. The index turns each inner scan into a covering range search (`SEARCH x USING COVERING INDEX ix_dept_sal (dept_id=?)`) but the subquery still runs once per outer row, so A is still about 81 times B.",
         "What SQLite prints for the unindexed correlated form: `SCAN e`, `CORRELATED SCALAR SUBQUERY 1`, `SCAN x`. No automatic index appears for the inner scan (automatic indexes were on by default), whereas the derived-table form B shows `BLOOM FILTER ON d` and `SEARCH d USING AUTOMATIC COVERING INDEX (dept_id=?)`, so SQLite builds an automatic index on the materialised derived table but not on the inner scan of a correlated subquery.",
         "The window form needs the rows ordered by the partition key: without the index the plan shows `USE TEMP B-TREE FOR ORDER BY` twice (the window sort, then the final ORDER BY); with the index the window sort is replaced by an index scan but the final ORDER BY emp_id still sorts.",
         "Decorrelation by the optimiser: PostgreSQL, SQL Server and MySQL optimisers can sometimes turn some correlated subqueries into joins (SQL Server and recent MySQL for some patterns; PostgreSQL generally not for a correlated scalar aggregate). I did not run any of them, so treat this as a hedge. Do not rely on it: it differs by engine and version and by query shape, and when it does not happen the cost is quadratic. A rewrite that states the grouping explicitly (B or C) is portable and predictable.",
         "Cross-reference Part 3 Q39 (correlated subquery performance)."],
follow=["When is the correlated form fine? (Small outer set, or a selective outer filter plus an index on the inner key, e.g. one department.)",
        "Why does C use more steps than B with the index? (Window evaluation buffers partitions and adds coroutines; steps are not time.)",
        "How would you test the three forms at the same size honestly? (Same data, same asserted result, fresh connection per plan print; steps first, timing only as a machine-specific second opinion.)"],
mist=["Assuming the optimiser will decorrelate the subquery.",
      "Reading a plan from a stale statement cache: this run varies the EXPLAIN text so SQLite cannot return an old plan (see the sources note).",
      "Comparing with >= and then wondering why ties appear.",
      "Running the quadratic form at full size 'just to see'; measure it on small sizes and extrapolate, labelled as an estimate."],
)

Q[21] = dict(
say="OR is fast only when every branch has an index (SQLite turns same-column ORs into IN and different indexed columns into a MULTI-INDEX OR), one unindexed term forces a scan, UNION ALL needs mutually exclusive branches to stay correct, UNION pays a temp B-tree to deduplicate, and != / NOT IN on a column that matches 98% of rows is a scan whichever way you write it.",
schema="""CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,5,'delivered','2024-05-05',100),(2,5,'cancelled','2024-01-01',20),
 (3,7,'delivered','2024-05-05',30),(4,8,'delivered','2024-05-05',900),(5,9,'returned','2024-02-02',10);""",
sql_intro="The tiny forms are `OR2`, `U_ALL_BAD`, `U_ALL_OK` and `U_PLAIN`; the scaled forms are in the `CASES` list of the Code block (same text):",
sql="""SELECT order_id FROM orders WHERE customer_id = 5 OR order_date = '2024-05-05' ORDER BY order_id

SELECT order_id FROM orders WHERE customer_id = 5 UNION ALL
SELECT order_id FROM orders WHERE order_date = '2024-05-05' AND customer_id IS NOT 5 ORDER BY order_id

SELECT order_id FROM orders WHERE customer_id = 5 UNION
SELECT order_id FROM orders WHERE order_date = '2024-05-05' ORDER BY order_id

SELECT order_id FROM orders WHERE customer_id = 5 OR customer_id = 7
SELECT order_id FROM orders WHERE customer_id = 5 OR amount > 400
SELECT order_id FROM orders WHERE status != 'delivered'
SELECT order_id FROM orders WHERE status NOT IN ('cancelled','returned')
SELECT order_id FROM orders WHERE status IN ('cancelled','returned')""",
pd_intro="Boolean masks, one per query (these are the `lambda d: ...` bodies in the `CASES` list, which the code asserts against each SQL result after sorting by order_id).",
pd='lambda d: d[(d.customer_id == 5) | (d.order_date == "2024-05-05")]',
example="Tiny table: customer 5 owns orders 1 and 2; date 2024-05-05 covers orders 1, 3 and 4. The OR returns {1,2,3,4} once each. UNION ALL without a guard returns order 1 twice ([1, 1, 2, 3, 4]) because it matches both branches. The guard `customer_id IS NOT 5` on the second branch removes it: [1, 2, 3, 4]. Plain UNION also returns [1, 2, 3, 4] by deduplicating, at the price of a sort or hash. If a row with customer_id NULL and that date exists (order 6), the guard `IS NOT 5` keeps it ([1,2,3,4,6], correct) but `!= 5` drops it (NULL != 5 is unknown). At 200,000 rows I forced row 1 to customer 5 on 2024-05-05 so the double count shows: the unguarded UNION ALL returned 614 rows against 613 correct.",
edge=["The double-count demonstration needed one forced row: with random data the two branches rarely overlap, so an unguarded UNION ALL can look right in a test and be wrong in production.",
      "NOT IN with a NULL in the list returns no rows (three-valued logic, see Part 3 Q3); the list here has none. `!=` and NOT IN exclude rows where status is NULL; there are none in this data.",
      "The status mix is seeded 98/1/1 percent (195,960 delivered, 1,976 cancelled, 2,064 returned in the run), so 'rare values' are 2% in total, not 0.5%."],
explain=["Plans and VM steps (200,000 rows, indexes on customer_id, order_date, status): `customer_id = 5 OR customer_id = 7` became one `SEARCH ... USING COVERING INDEX ix_cust (customer_id=?)`, 25 rows, 133 steps (SQLite rewrote the OR into IN). Two different indexed columns gave `MULTI-INDEX OR / INDEX 1 / INDEX 2`, 613 rows, 5,541 steps. With the unindexed `amount > 400` as one OR term the plan was `SCAN orders`, 40,185 rows, 1,080,349 steps: one unindexed branch ruins the whole OR.",
         "UNION ALL (guarded) took 4,265 steps and UNION 4,926; the UNION plan says `UNION USING TEMP B-TREE`, the cost of removing duplicates. Both branches used an index. UNION ALL is only correct when the branches cannot return the same row, or when you add the NOT condition shown.",
         "Inequality: `status != 'delivered'` matched 4,040 rows (2%) but the plan was `SCAN orders USING COVERING INDEX ix_status`, 608,089 steps, essentially identical to `NOT INDEXED` (608,088). SQLite did not seek an index for !=. `status IN ('cancelled','returned')` used `SEARCH ... (status=?)` and took 16,188 steps, about 38 times fewer, but it needs the complete list of other values and silently misses new statuses. `NOT IN ('cancelled','returned')` returns 98% of the table (195,960 rows, 1,785,914 steps), where no index can help: reading most of the table is what it costs.",
         "Why OR across columns is only fast when every branch is indexable: each branch needs its own index lookup, merged by rowid; one unindexed term needs a scan to evaluate, which makes the index lookups pointless. SQLite documents the MULTI-INDEX OR strategy; it does not intersect indexes for AND (see the sources note).",
         "Other engines, not executed: MySQL has an index_merge optimisation (union, intersection) and PostgreSQL combines indexes with bitmap OR / bitmap AND scans; both are hedged here because I only ran SQLite. Whether either is chosen depends on statistics.",
         "Rewriting with UNION ALL is a manual way to get what MULTI-INDEX OR does automatically: use it only when you have shown that the original OR is slow and the branches are exclusive."],
follow=["How would you make `status != 'delivered'` fast? (Often you cannot; a partial index on the rare statuses, or IN with the known list, or ask whether the report needs those rows at all; see Q22.)",
        "Why do the UNION plans say COVERING INDEX while the MULTI-INDEX OR plan printed a plain INDEX? (The index holds order_id as the rowid, so no table lookup is needed; I did not investigate why the OR plan does not say covering.)",
        "What does UNION do with NULLs? (Treats them as equal for deduplication.)"],
mist=["UNION ALL over overlapping branches without a guard.",
      "Writing the guard as `!= 5` and losing NULL rows.",
      "Expecting an index to help `!=` or `NOT IN` on a column where most rows match.",
      "Wrapping an indexed column in a function inside the OR and then blaming OR."],
)

Q[22] = dict(
say="A partial index is used only when the query's WHERE clearly implies the index's WHERE (in SQLite 3.45.1 `status = 'placed'` and a bound `status = ?` qualify, `IN ('placed')` and `!=` did not), an expression index is used only when the query contains the exact same expression, and a UNIQUE index treats NULLs as distinct so it allows several.",
schema="""CREATE TABLE orders(order_id INTEGER PRIMARY KEY, status TEXT, order_date TEXT, email TEXT);
INSERT INTO orders VALUES (1,'placed','2024-06-01','Asha@Mail.com'),(2,'delivered','2024-06-02','ben@mail.com'),
 (3,'placed','2024-06-03',NULL),(4,'delivered','2024-06-04',NULL);
CREATE UNIQUE INDEX ux_email ON orders(email);""",
sql_intro="The three indexes and the probe queries are in the Code block, copied here (the full probe list is the `Q` and `E` lists):",
sql="""CREATE INDEX ix_placed ON orders(order_date) WHERE status = 'placed'
CREATE INDEX ix_lower_email ON orders(lower(email))
CREATE UNIQUE INDEX ux_email ON orders(email)
CREATE INDEX ix_full ON orders(order_date)
SELECT order_id FROM orders WHERE status = 'placed' AND order_date > '2024-11-01'
SELECT order_id FROM orders WHERE status IN ('placed') AND order_date > '2024-11-01'
SELECT order_id FROM orders WHERE status != 'delivered' AND order_date > '2024-11-01'
SELECT order_id FROM orders WHERE status = ? AND order_date > '2024-11-01'
SELECT order_id FROM orders WHERE lower(email) = ?""",
pd_intro="Row-for-row filters that the code asserts against the SQL results.",
pd='exp = df[(df.status == "placed") & (df.order_date > "2024-11-01")]',
example="Tiny table: orders 1 and 3 are 'placed'. The partial index ix_placed would hold only those two rows (entries for dates 2024-06-01 and 2024-06-03); orders 2 and 4 are not in it at all. `status = 'placed' AND order_date > '2024-06-02'` is answered from it (order 3). The UNIQUE index on email holds 'Asha@Mail.com', 'ben@mail.com' and two NULL entries: the two NULLs do not conflict (count printed: 2), a second 'ben@mail.com' fails with `UNIQUE constraint failed: orders.email`, and 'BEN@mail.com' is accepted because the default comparison is case-sensitive. At 200,000 rows (6,064 placed, 3.03%) the query `status = 'placed' AND order_date > '2024-11-01'` returned 982 rows, which equals the pandas filter.",
edge=["Implication is syntactic and conservative: `status IN ('placed')` means the same as `= 'placed'` but SQLite 3.45.1 scanned the table (614,102 steps against 2,958). `status != 'delivered'` is not implied by `status = 'placed'` anyway (it also matches other statuses) and scanned. A bound parameter `status = ?` did use the index (5,907 steps): the planner accepts a parameter for the equality here; I did not test what happens in other engines.",
      "A query with no status condition cannot use the partial index (it would miss rows): SCAN.",
      "UNIQUE on a mixed-case email does not make emails unique ignoring case: add a unique expression index on lower(email) for that (not run here; the lower(email) expression index in the code is non-unique).",
      "NULL emails: 9,938 of 200,000 rows are NULL and all coexist under the UNIQUE index."],
explain=["Which query used which index (plans printed in the output): `status = 'placed' AND order_date > ...` used `COVERING INDEX ix_placed (order_date>?)`; `IN ('placed')`, `!=` and the no-status query scanned. `lower(email) = ?` used `ix_lower_email (<expr>=?)` (17 steps), as did `lower(email) = lower(?)`. `upper(email) = ?`, `lower(trim(email)) = ?`, `email = ? COLLATE NOCASE` and `email LIKE ?` all scanned (the plan shows a scan of the narrowest covering index ux_email, 600,011 to 1,000,011 steps). `email = ?` used the UNIQUE index (11 steps). The expression must match exactly.",
         "Size (dbstat, 4,096-byte pages): partial ix_placed 29 pages (118,784 bytes) against full ix_full 926 pages (3,792,896 bytes), about 3% of the size; ix_lower_email and ux_email 1,438 pages each; the table 2,740 pages.",
         "Write cost: a partial index is only maintained for rows that satisfy its WHERE, so inserts and updates of the other 97% do not touch it. In a 100,000-row insert of non-'placed' rows the partial index ended with 1 page against 516 for the full index, and wall time was 363 ms against 432 ms (no index: 245 ms; machine-specific single runs). The VM-step proxy did NOT show a difference (2,000,003 callbacks for both), because the progress handler counts jump-style opcodes and the cheap skip is not visible there; do not use steps for this comparison.",
         "Benefits: smaller index, cheaper writes for rows outside the predicate, and a UNIQUE rule that can be limited to a subset (e.g. one active row per customer, not run here).",
         "Other engines, not executed: PostgreSQL partial and expression indexes have the same idea (the planner must be able to prove the query predicate implies the index predicate, and parameterised queries and generic plans can change that; check with EXPLAIN there). SQL Server filtered indexes are similar but are reported to be restricted for parameterised queries unless the plan is recompiled, and SQL Server and PostgreSQL treat NULLs in unique indexes differently (SQL Server allows one NULL in a unique index; PostgreSQL allows many, and newer versions have NULLS NOT DISTINCT). All of this is from memory and was not run."],
follow=["What is the risk of an expression index? (Every query and every ORM must write the same expression; a different function or collation silently scans.)",
        "Would ANALYZE change any of these plans? (Not tested in this answer.)",
        "How would you enforce case-insensitive uniqueness? (UNIQUE index on lower(email), or a NOCASE collation on the column; the lower(email) unique variant is not run here.)"],
mist=["Assuming `IN ('placed')` or `!=` will use a partial index.",
      "Testing the expression index with `lower(trim(email))` or `upper(email)` and concluding indexes are broken.",
      "Believing UNIQUE rejects multiple NULLs (SQLite and PostgreSQL allow them; engines differ).",
      "Counting a partial index as free: the table still pays for all other indexes."],
)

Q[23] = dict(
say="Each commit forces a sync to disk, so one commit per row costs milliseconds per row, while one transaction (with executemany and bound parameters) costs microseconds per row; load first, create indexes afterwards, and never build SQL with string formatting.",
schema="""CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_type TEXT, event_time TEXT);
INSERT INTO events VALUES (1,17,'view','2024-01-01'),(2,17,'click','2024-01-01'),(3,42,'buy','2024-01-02');""",
sql_intro="The statements are the constants `DDL`, `INS` and the three `CREATE INDEX` strings in `IDX`; the load shapes are the Python functions in the Code block:",
sql_text="""CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_type TEXT, event_time TEXT)
INSERT INTO events VALUES (?,?,?,?)
CREATE INDEX ix_user ON events(user_id)
CREATE INDEX ix_type ON events(event_type)
CREATE INDEX ix_time ON events(event_time)""",
pd_intro="pandas holds the same seeded rows and is the checksum for every load.",
pd='pdf = pd.DataFrame(data, columns=["event_id", "user_id", "event_type", "event_time"])',
example="Three rows go in. With a commit per row there are three transactions: three journal writes and three syncs. In one transaction there is one commit and one sync for all three rows. For 100,000 rows the same logic applies at scale: 100,000 syncs against one. The checksum in the code (row count and SUM(user_id) against the pandas frame) proves every method stored the same rows.",
edge=["Per-row commit was run on 2,000 rows only (as asked); 100,000 syncs would take minutes on this storage. The per-row figures are not extrapolated into a total in the text.",
      "VM steps are the same per row for commit-per-row (21 steps per row) and for one transaction (15 per row): commit-and-sync cost is I/O wait, not VM work, so the deterministic step count cannot show it. Only wall-clock shows it, so the timings below are the evidence and they are machine- and disk-specific single runs.",
      "File-backed database in a temporary directory; storage type, filesystem and fsync behaviour change the numbers a lot (WAL with synchronous=NORMAL is far faster for per-row commits but gives up some durability on power loss)."],
explain=["Results in my run (machine-specific): commit per row 2,000 rows took about 2.2 seconds, around 1.1 ms per row; the same loop in one transaction inserted 100,000 rows in about 0.34 s (a few microseconds per row); executemany took about the same (0.31 s), because the loop overhead of Python is small next to the commit. A multi-row INSERT with 500 rows per statement was a little faster (0.26 s) and used the fewest VM steps (1,401,606 against 1,500,006). String formatting took longer (0.59 s) and cannot bind a value that contains a quote (the run shows `near \"s\": syntax error`) and is an injection hole: bound parameters are also faster because the statement is prepared once and reused.",
         "Settings printed: `PRAGMA journal_mode` = delete and `PRAGMA synchronous` = 2 (FULL) by default. For 2,000 per-row commits: WAL with synchronous=FULL about 0.58 s, WAL with synchronous=NORMAL about 0.05 s, journal_mode delete with synchronous=OFF about 0.1 s. Fewer syncs, faster commits; the price is durability, which is a business decision.",
         "Indexes: with three secondary indexes created BEFORE the load the insert took 3,100,168 steps and about 1.0 s; creating them AFTER the load took 4,200,168 steps but about 0.7 s. The step count went UP while the time went DOWN: a bulk index build sorts the keys and appends them in order instead of doing a random B-tree insert per row, and that is I/O and cache behaviour that VM steps do not capture. Use steps only for what they measure.",
         "Not executed here: PostgreSQL COPY, MySQL LOAD DATA, and bulk-load paths in warehouses (stage files then COPY or LOAD) are the same idea at a larger scale: few large operations rather than many small ones. Multi-row INSERT VALUES is standard SQL and was run on SQLite; its row limits differ by engine (SQLite's compile option here is MAX_VARIABLE_NUMBER=250000 bound variables, printed in the run)."],
follow=["What does executemany do beyond the loop? (Reuses one prepared statement; the speed-up over a per-row execute in one transaction was small here.)",
        "What is the durability trade-off of synchronous=NORMAL or OFF? (A crash or power loss can lose recent commits or corrupt data in OFF mode.)",
        "Would you load into an indexed table if it is live? (Yes if readers need it; for a one-off bulk load, drop or defer indexes.)"],
mist=["Calling commit inside the loop 'to be safe'.",
      "Leaving autocommit on with the Python default and wondering why it is slow (each INSERT outside a transaction commits).",
      "Building SQL with f-strings.",
      "Quoting wall-clock timings as if they were deterministic."],
)

Q[24] = dict(
say="N+1 is one query for the list plus one query per row, 101 statements here against 1 (JOIN + GROUP BY) or 2 (a batched IN); in-process SQLite hides the cost, but against a networked database every extra statement is a round trip, so latency multiplies by N.",
schema="""CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'cust001'),(2,'cust002'),(3,'cust003');
INSERT INTO orders VALUES (1,1,100),(2,1,50),(3,3,70);""",
sql_intro="The three shapes are in the Code block (the loop statement, the JOIN/GROUP BY and the batched IN), copied here:",
sql_text="""SELECT customer_id, name FROM customers ORDER BY customer_id
SELECT COALESCE(SUM(amount),0), COUNT(*) FROM orders WHERE customer_id = ?
SELECT c.customer_id, c.name, COUNT(o.order_id), COALESCE(SUM(o.amount),0)
FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name ORDER BY c.customer_id
SELECT customer_id, amount FROM orders WHERE customer_id IN (%s)""",
pd_intro="Per-row `read_sql` in a loop versus one `read_sql`, groupby and merge (both are in the Code block, copied here):",
pd='agg = ord_df.groupby("customer_id")["amount"].agg(cnt="size", total="sum").reset_index()',
example="Tiny table: customer 1 has orders of 100 and 50 (count 2, total 150), customer 2 has none (count 0, total 0), customer 3 has 70. The N+1 loop issues the list query and then three lookups: 4 statements, in general 1 + N. The JOIN with GROUP BY returns the same three rows in one statement; the LEFT JOIN keeps customer 2 with count 0. At scale (100 customers, 1,000 orders) the trace callback counted exactly 101, 1 and 2 statements, and the three results are asserted equal.",
edge=["Customers without orders: the loop form gives (0, 0) through COALESCE and the JOIN needs a LEFT JOIN (with an INNER JOIN they would vanish, and the assert would fail).",
      "The batched IN query returns raw order rows, so the grouping happens in Python; customers with no orders are filled with (0, 0) in the code.",
      "An empty id list makes `IN ()`: build the placeholders from a non-empty list or skip the query."],
explain=["Why N+1 hurts: each statement costs a round trip (network latency plus parse and plan). In-process SQLite has no network, so the timing is misleading: the loop took about 4.5 ms and the JOIN about 1 ms in my run (machine-specific), a small absolute difference. Illustrative arithmetic only, not a measurement: at an assumed 0.5 ms per round trip, 101 statements add about 50 ms while 1 statement adds 0.5 ms, and for 10,000 rows N+1 would add 5 seconds.",
         "Even in process the plan of the per-customer lookup matters: `SCAN orders` without an index (so the loop reads the whole orders table 100 times) and `SEARCH orders USING INDEX ix_orders_cust (customer_id=?)` with one. With the index, 100 lookups took 7,700 VM steps and the single JOIN/GROUP BY 15,219 steps (it reads all 1,000 orders): in VM steps N+1 was not worse. The cost of N+1 is latency, not engine work, which is why in-process counts hide it.",
         "ORM origin (described, no ORM executed): lazy loading fetches related rows when an attribute is first touched, so iterating over 100 parents and reading `parent.children` triggers 100 child queries. Eager-loading options (a JOIN fetch, or a second query with IN over the parent ids, usually called select-in or batch loading) turn it into 1 or 2 statements. Check the ORM's SQL log, as this answer does with `set_trace_callback`.",
         "Batching limits: an IN list is limited by the engine's bound-variable limit. SQLite here reports `MAX_VARIABLE_NUMBER=250000`; an IN list of 300,000 placeholders failed with `OperationalError too many SQL variables`. Other engines have their own limits (hedged, not executed); chunk the ids (the code runs 4 chunks of up to 30 ids).",
         "pandas: loading customers and then calling `read_sql` once per customer produced 101 statements (1 + 100); one `read_sql` for orders followed by `groupby` and `merge` produced 1 statement (the customers frame was reused from the first part; reading it again would make 2)."],
follow=["When is IN batching better than a JOIN? (When the child query needs different columns, filters or a different database or service from the parent.)",
        "How do you detect N+1 in production? (Statement counts per request in the application log or APM, repeated identical query shapes with different parameters.)",
        "What is the fix when the parent list is huge? (Chunk the ids, or push the work into one set-based query.)"],
mist=["Judging N+1 by in-process timing.",
      "Using an INNER JOIN and dropping parents without children.",
      "Putting 100,000 ids into one IN list without checking the engine's limit.",
      "Looping over DataFrame rows and calling the database inside the loop."],
)

Q[25] = dict(
say="In SQLite 3.45.1 a CTE (or subquery) used once is run as a co-routine and a filter on its grouping column is pushed down into it, a CTE used twice is materialised once by default (AS NOT MATERIALIZED re-runs it for each reference, which here doubled the steps), and a LIMIT or an aggregate condition inside blocks the push-down.",
schema="""CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,5,'2024-01-01',10),(2,5,'2024-01-02',30),(3,6,'2024-01-03',5),(4,7,'2024-01-04',100);""",
sql_intro="The CTE-twice query is `TWICE` with `%s` replaced by nothing, `MATERIALIZED` or `NOT MATERIALIZED`; the others are below (same text as the Code block):",
sql="""WITH t AS %s (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) SELECT customer_id, s FROM t WHERE s > (SELECT AVG(s) FROM t) ORDER BY customer_id
SELECT customer_id, s FROM (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) WHERE customer_id = 5
SELECT customer_id, SUM(amount) AS s FROM orders WHERE customer_id = 5 GROUP BY customer_id""",
pd_intro="Group, then compare with the mean of the group totals (the CTE-twice question), and a plain filter for customer 5.",
pd='exp5 = int(df.loc[df.customer_id == 5, "amount"].sum())',
example="Tiny table: customer totals are 5 -> 40, 6 -> 5, 7 -> 100; the average of the totals is 48.33, so only customer 7 (100) is above it: the CTE `t` is read twice, once for the rows and once inside the scalar subquery for the average. With `WHERE customer_id = 5` on top of the aggregate the answer is the single row (5, 40). The question is whether SQLite computes all customers' totals first and then throws four away, or computes only customer 5's.",
edge=["Both materialisation hints return identical rows; they change work, not results (asserted equal to the pandas totals).",
      "For a CTE referenced twice, NOT MATERIALIZED duplicates the work: it is only a good idea when the CTE is cheap or each use is selective.",
      "The plan wording CO-ROUTINE versus MATERIALIZE may change between SQLite versions (the EXPLAIN QUERY PLAN format is not a stable interface); these lines are 3.45.1."],
explain=["CTE referenced twice (200,000 rows, index on customer_id): the default plan was `MATERIALIZE t / SCAN orders USING INDEX ix_cust / SCAN t / SCALAR SUBQUERY 2 / SCAN t`, 2,385,659 steps, identical to AS MATERIALIZED. AS NOT MATERIALIZED showed `CO-ROUTINE t` twice and took 4,465,655 steps, because the whole GROUP BY ran twice. So for several uses SQLite materialises by default.",
         "A filter outside a GROUP BY subquery on the grouping column (`WHERE customer_id = 5`) was pushed into the subquery: plan `CO-ROUTINE (subquery-1) / SEARCH orders USING INDEX ix_cust (customer_id=?)`, 138 steps, against 125 for the hand-inlined form. The CTE used once with the same filter gave the identical plan and 138 steps: used once, a CTE behaves like a subquery. Adding AS MATERIALIZED to that single-use CTE disabled the push-down: `MATERIALIZE t / SCAN orders`, 2,180,011 steps (computing all 19,999 groups to keep one), close to the unfiltered aggregate (2,080,004 steps).",
         "Push-down limits observed (outer filter `customer_id = 5`): a LIMIT inside the subquery blocked it (`SCAN orders`, 1,800,040 steps, against 63 without the LIMIT, because the filter after a LIMIT is a different question). A filter on an aggregate result (`s > 2000`) cannot be pushed below the GROUP BY (2,178,912 steps, 13,890 rows). In this version a DISTINCT inside did NOT block a filter on one of the distinct columns (161 steps), and a window with the filter on its PARTITION BY column was pushed down too (349 steps); I did not test a filter on the rank value alone. The premise 'DISTINCT blocks push-down' is therefore only partly true: I tested the case where the filtered column is part of the DISTINCT list, and it did push.",
         "PostgreSQL, not executed here: from version 12 a single-use CTE that has no side effects is inlined and treated like a subquery, and MATERIALIZED and NOT MATERIALIZED exist there too; before 12, a CTE was an optimisation fence (always materialised). MySQL and SQL Server behaviour is not discussed here because it was not checked.",
         "Cross-reference Part 3 Q32 (reusing one CTE twice)."],
follow=["Why can't `s > 2000` be pushed in? (It depends on the aggregate result, so it is a HAVING.)",
        "How do you force a one-time computation? (AS MATERIALIZED, or a temporary table.)",
        "How do you force re-evaluation? (AS NOT MATERIALIZED, useful when the filter makes the CTE tiny.)"],
mist=["Treating a CTE as a stored temporary result in every engine.",
      "Adding AS MATERIALIZED 'for speed' and losing the push-down.",
      "Reading a plan once and generalising: the plan changes with the SQLite version and the data."],
)

Q[26] = dict(
say="A window function needs rows ordered by partition then order key, so unless an index supplies that order the plan sorts the whole table; an outer filter on the rank cannot run before the window, so the window still reads all 300,000 rows, and the correlated COUNT form grows quadratically.",
schema="""CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, region TEXT, product_id INTEGER, sale_date TEXT, amount INTEGER);
INSERT INTO sales VALUES (1,'N',1,'2024-01-01',50),(2,'N',2,'2024-01-02',90),(3,'N',3,'2024-01-03',90),(4,'N',4,'2024-01-04',70),(5,'N',5,'2024-01-05',10),
 (6,'S',1,'2024-01-06',20),(7,'S',2,'2024-01-07',30);""",
sql_intro="`WIN` (window), `CNT` (correlated COUNT) and `INL` (correlated IN with ORDER BY ... LIMIT 3) are in the Code block, copied here; the tie-break (amount DESC, sale_id) makes the result deterministic:",
sql=["WIN", "CNT", "INL"],
pd_intro="Sort, then `groupby().head(3)`.",
pd=("pandas_top3",),
example="Tiny table, region N: amounts 50 (id 1), 90 (id 2), 90 (id 3), 70 (id 4), 10 (id 5). Sorted by amount DESC then sale_id: 2 (90), 3 (90), 4 (70), 1 (50), 5 (10); the top 3 are ids 2, 3, 4. Region S: 30 (id 7) and 20 (id 6). All three SQL forms return [('N',2,90),('N',3,90),('N',4,70),('S',7,30),('S',6,20)]. The two 90s are a tie: ROW_NUMBER with the sale_id tie-break picks both; the COUNT form needs the same tie-break in its comparison or it would count ties as equal and could return more than 3 rows.",
edge=["Ties at the cut-off: ROW_NUMBER gives exactly 3 rows per region; RANK or the plain `b.amount > a.amount` COUNT can return more. The tie-break columns in every form make the comparison with pandas exact.",
      "A region with fewer than 3 rows returns what it has (region S).",
      "The correlated forms were compared at 6,000 rows (all three forms, with and without the index) and at 300,000 rows only where they finish in reasonable time (window, correlated IN with index); the correlated COUNT was not run at 300,000 rows."],
explain=["6,000 rows (50 regions x about 120 rows) VM steps, no index: window 290,187; correlated COUNT 147,731,516; correlated IN + LIMIT 148,685,000. With an index on (region, amount DESC, sale_id): window 230,185; COUNT 5,195,467; IN + LIMIT 162,611. Without an index each correlated outer row rescans or re-sorts its region (two temp B-trees for the IN form).",
         "Growth of the correlated COUNT with the index: 3,000 rows 1,332,755 steps (444 per row), 6,000 rows 5,195,467 (866 per row), 12,000 rows 20,470,934 (1,706 per row): steps per row double when n doubles, so cost is quadratic, because each row counts the rows above it in its region. That is why it was not run at 300,000.",
         "300,000 rows: window with no index 14,402,187 steps; with the index 11,402,185 steps; correlated IN with ORDER BY ... LIMIT 3 and the index 8,100,611 steps (each outer row reads about three index entries), lower than the window here. All three were asserted equal to pandas. SQLite accepted LIMIT inside an IN subquery; MySQL is known to reject LIMIT in such a subquery (hedged, not run).",
         "Sorts, counted from the plans: with no index the window plan has `USE TEMP B-TREE FOR ORDER BY` twice (the window's partition/order sort plus the final ORDER BY: 2); with the index the window sort disappears (`SCAN sales USING COVERING INDEX ix_reg_amt`) and only the final ORDER BY sort remains (1); dropping that final ORDER BY leaves 0. A different outer ORDER BY key (sale_date) needs its own sort on top of whatever order the window had (1 sort, plus a non-covering index scan, 12,602,486 steps). So an extra ORDER BY on another key is an extra sort.",
         "Why the rank filter is not pushed before the window: `rn <= 3` depends on the window's output, and the window needs all rows of each partition to number them, so the plan reads all 300,000 rows (about 11.4 million steps even with the index) to return 150. The index saves the sort, not the scan.",
         "Cross-references: Part 4 Q40 (window function performance concept) and Part 4 Q39 (top N and pagination)."],
follow=["How would you make top 3 per region cheap at 300,000 rows? (The correlated IN with an index above, or a LATERAL join in engines that have it, not executed; or keep a pre-aggregated table.)",
        "RANK versus ROW_NUMBER at a tie? (RANK keeps both tied rows, so more than 3 can come back.)",
        "Does the same plan appear in PostgreSQL? (Not executed; there, a WindowAgg node over a Sort or an Index Scan is the usual shape.)"],
mist=["Running the correlated COUNT on the full table without checking its growth.",
      "Forgetting a tie-break and getting nondeterministic or inflated results.",
      "Believing `WHERE rn <= 3` makes the window stop early.",
      "Comparing plans for a statement text the connection has already planned (this run varies the text)."],
)

Q[27] = dict(
say="Filter, aggregate and join in the database before the rows reach pandas: pulling 500,000 rows to compute 12 monthly totals moved 500,000 rows and 70 MB while the GROUP BY query moved 12 rows, and chunked reading saves memory, not time; chunked aggregation only works for decomposable aggregates such as sum and count.",
schema="""CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,1,'2024-01-05','delivered',100),(2,2,'2024-01-20','delivered',50),(3,3,'2024-01-21','cancelled',999),
 (4,1,'2024-02-02','delivered',70),(5,2,'2023-12-31','delivered',500),(6,3,'2025-01-01','delivered',5);""",
sql_intro="The pushed-down query `SQL` is in the Code block, copied here:",
sql=["SQL"],
pd_intro="The same aggregation in pandas, used for (a), (c) and (d) (a function in the Code block):",
pd=("pandas_agg",),
example="Tiny table: delivered orders in 2024 are 1 (Jan, 100), 2 (Jan, 50) and 4 (Feb, 70). Order 3 is cancelled (excluded), order 5 is 2023-12-31 and order 6 is 2025-01-01 (outside 2024). Result: 2024-01 revenue 150 (2 orders) and 2024-02 revenue 70 (1 order); the run prints `[('2024-01', 150, 2), ('2024-02', 70, 1)]`. At 500,000 rows (seed 27) the same 12 monthly totals come out of all methods.",
edge=["The date range is a half-open interval (`>= '2024-01-01' AND < '2025-01-01'`), which is safe for dates stored as ISO text; the month is `substr(order_date,1,7)` in SQL and `str[:7]` in pandas.",
      "Chunked results are partial sums per month; the per-chunk frames are concatenated and summed again. A month absent from a chunk simply contributes nothing.",
      "All five paths are asserted equal after casting revenue and n_orders to int64 and comparing sorted by month."],
explain=["Measured (500,000-row file database of 17.6 MB; timings are machine-specific single runs): (a) read the whole table: 500,000 rows transferred, `memory_usage(deep=True)` 70.3 MB, load about 1.2 s plus about 0.25 s to filter and group. (b) WHERE + GROUP BY in SQL: 12 rows, 996 bytes, about 0.16 s. (c) `chunksize=50,000`: still 500,000 rows transferred, peak chunk memory 7.0 MB, about 1.5 s: memory bounded, time not better. (d) only the three needed columns, filter in pandas: 500,000 rows, 62.3 MB, about 0.8 s load plus 0.28 s. (e) WHERE pushed down but aggregation in pandas, two columns: 174,908 rows, 11.7 MB, about 0.3 s.",
         "Honest observations: selecting columns alone (d) saved only 8 MB because the two dropped columns are integers, while the string columns order_date and status dominate the memory (pandas 3 uses the `str` dtype). The biggest saving is moving the filter (e) and the aggregation (b) to the database. No index was created here, so (b) still scanned the table in SQLite; an index on (status, order_date) would help but was not measured.",
         "Push down: filters, aggregations, joins on indexed keys, sampling and `LIMIT`; it reduces transferred rows and memory and uses the engine's indexes. Pandas is better for iterative exploration (re-slicing the same data many times after one load), logic that is awkward in SQL (complex reshaping, custom Python functions) and when the data is already small.",
         "Chunked aggregation works for decomposable aggregates (sum, count, min, max, and mean via sum and count): partial results combine exactly. The run shows mean from decomposed (sum, count) equal to the direct mean (2507.8495). A median does not decompose: the mean of 50,000-row chunk medians equalled the true median here only by chance (every chunk is a random sample of the same distribution); the counterexample with chunks [1,2,9] and [3,4,5,6,7] gives a true median of 4.5 and a mean of chunk medians of 3.5.",
         "Source note: the pandas guides named in the Asked-at line were opened for ideas only; no numbers from them are used."],
follow=["Would you use chunksize with a GROUP BY already in SQL? (Not needed: the result is small.)",
        "How would you do an exact median in chunks? (Two passes with a histogram or a sorted external merge, or use the database's percentile function where it exists; not run.)",
        "What if the table has no index? (Pushdown still reduces transfer, but the database scans; add an index for repeated queries.)"],
mist=["Reading the whole table 'because pandas is easier' and then filtering.",
      "Using chunksize to speed things up (it reduces peak memory).",
      "Averaging chunk means or medians of unequal chunks.",
      "Forgetting that SELECT * of text columns costs far more memory than the integer columns."],
)
