P = {}

P[1] = r'''
**Say this first (1 line):** INNER keeps only matching pairs, LEFT keeps every left row, RIGHT keeps every right row, FULL keeps every row from both sides, and CROSS pairs every row with every row; with 4 customers and 5 orders (one customer without orders, one order with a NULL customer) the counts are 4, 5, 5, 6 and 20.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha','Pune'),(2,'Ben','Delhi'),(3,'Chitra','Pune'),(4,'Dev','Delhi');
INSERT INTO orders VALUES (101,1,100),(102,1,50),(103,2,75),(104,NULL,30),(105,3,20);
```
Dev (4) has no orders. Order 104 has a NULL customer_id.

**SQL answer:** the five queries are in the Code block as `sql["inner"]`, `sql["left"]`, `sql["right"]`, `sql["outer"]` and `sql["cross"]`, all joined `ON o.customer_id = c.customer_id` (CROSS has no ON). `sql_swapped` is the RIGHT JOIN rewritten as a LEFT JOIN with the tables swapped.

**pandas answer:** `customers.merge(orders, how=..., left_on=..., right_on=...)` with `how` equal to `"inner"`, `"left"`, `"right"`, `"outer"` (that is FULL OUTER) or `"cross"` (no keys). The mapping is one to one: inner = INNER JOIN, left = LEFT JOIN, right = RIGHT JOIN, outer = FULL OUTER JOIN, cross = CROSS JOIN.

**Example:** walk the five orders by hand.
- INNER: 101 and 102 match Asha, 103 matches Ben, 105 matches Chitra. Order 104 has a NULL key, which equals nothing. Dev matches nothing. Result: 4 rows.
- LEFT (all customers kept): the 4 matched rows plus Dev with NULL order columns. 5 rows. Order 104 is not shown because it is on the right side.
- RIGHT (all orders kept): the 4 matched rows plus order 104 with NULL customer columns. 5 rows. Dev is not shown.
- FULL: the 4 matched rows plus Dev plus order 104. 6 rows. That is 4 + 1 + 1: matches, unmatched left, unmatched right.
- CROSS: 4 x 5 = 20 rows, no condition at all.

**Code:** run with `python3 -I`. Rows are compared after sorting every row (NaN turned into None, whole floats into ints).
{CODE}

**Output (my run):**
{OUT}

**Edge cases:**
- **NULL key on the right (order 104):** it never matches, even a customer whose id is NULL, because `NULL = NULL` is not true. It only appears in RIGHT and FULL (Part 2 Q6 goes deeper).
- **Duplicates:** if a customer id were duplicated, INNER would return one row per matching pair, so the counts above are only right because `customer_id` is the primary key.
- **pandas dtype surprise:** `read_sql` turned `orders.customer_id` into `float64` because of the NULL. Merging that float key against the `int64` customer key still matched correctly in my run (all five asserts passed), so the float is a display issue here, not a wrong join. Part 2 Q35 covers dtype mismatches that do break.
- **Empty side:** an empty orders table gives INNER 0, LEFT = all customers, RIGHT 0, FULL = all customers, CROSS 0.

**Then explain:**
- **RIGHT is rarely needed:** `A RIGHT JOIN B` returns the same rows as `B LEFT JOIN A` (the Code block asserts this; only the column order changes, so I listed columns by name). Teams standardise on LEFT because queries then read top to bottom with the "main" table first.
- **FULL OUTER JOIN is for reconciliation:** compare two lists and see what exists in one, the other or both (Part 2 Q16).
- **CROSS JOIN has no ON:** use it on purpose (grids, combinations), never by accident (Part 2 Q30 and Q31).
- **Dialect facts (hedged):** SQLite added RIGHT and FULL OUTER JOIN in 3.39 (the version boundary is from memory; the queries above did run on SQLite 3.45.1 here). MySQL has no FULL OUTER JOIN; the MySQL 8.4 reference page I opened lists only LEFT and RIGHT [OUTER] JOIN, and the usual workaround is a LEFT JOIN UNION a RIGHT JOIN (Part 2 Q32). PostgreSQL, SQL Server, Oracle, BigQuery and Snowflake support FULL OUTER JOIN as far as I know (not executed here).
- **pandas default:** `merge` defaults to `how="inner"`, like a bare `JOIN`.

**Follow-ups:**
- *Which join returns rows from both tables that match neither side?* None of them; FULL returns unmatched rows from each side, padded with NULLs on the other.
- *Does LEFT JOIN ever return fewer rows than the left table?* No, at least one row per left row. It can return more if the right side has several matches.
- *How do I find the unmatched rows only?* LEFT JOIN with `IS NULL` on a right-side key (Part 2 Q2).

**Common mistakes:**
- Saying "LEFT JOIN returns the same number of rows as the left table" (it can grow with duplicates on the right).
- Expecting the NULL-key order to match a NULL-key customer.
- Using RIGHT JOIN in a chain of LEFT JOINs, which is hard to read.
- Forgetting that `how="outer"` in pandas is the FULL OUTER JOIN.
'''

P[2] = r'''
**Say this first (1 line):** For "customers with no orders" use `LEFT JOIN ... WHERE o.order_id IS NULL` or `NOT EXISTS`; avoid `NOT IN` unless the subquery column can never be NULL, and test a right-table column that is never NULL for matched rows, such as its primary key.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Esha');
-- 104 is a guest order (NULL customer); 105 belongs to Esha but its amount is NULL
INSERT INTO orders VALUES (101,1,100),(102,1,50),(103,2,75),(104,NULL,30),(105,5,NULL);
```

**SQL answer:** in the Code block: `sql_left` (LEFT JOIN with `o.order_id IS NULL`), `sql_not_exists`, `sql_not_in` (the trap), `sql_not_in_safe` (NOT NULL filter in the subquery) and `sql_wrong_col` (tests `o.amount`, which is wrong).

**pandas answer:** two forms in the Code block. `customers.merge(orders, on="customer_id", how="left", indicator=True)` then keep `_merge == "left_only"`, and `customers[~customers["customer_id"].isin(orders["customer_id"])]`.

**Example:** Asha, Ben and Esha each have an order, Chitra and Dev have none, so the answer is Chitra and Dev.
- LEFT JOIN: Chitra and Dev find no order, so their `o.order_id` is NULL and the WHERE keeps them.
- Which column to test: any column that is NULL only when the join found no match. The right table's primary key (`order_id`) is the safe choice. If I test `o.amount`, Esha's matched order 105 also has a NULL amount, so Esha would be listed wrongly. My run shows exactly that.
- NOT IN: the subquery returns 1, 1, 2, NULL, 5. For Chitra the test is `NOT (3 = 1 OR 3 = 2 OR 3 = NULL OR 3 = 5)`, which is UNKNOWN, so the row is dropped. Every customer is dropped, so the result is empty (Part 1 Q13 covers the three-valued logic).

**Code:** run with `python3 -I`. Results are compared in `customer_id` order.
{CODE}

**Output (my run):**
{OUT}

**Edge cases:**
- **NULL keys on the right (guest order 104):** harmless for LEFT JOIN and NOT EXISTS, fatal for NOT IN.
- **Duplicate orders per customer:** LEFT JOIN returns one row per match, but the anti-join keeps only rows with no match, so duplicates cannot appear in the result.
- **Empty orders table:** all three safe forms return every customer.
- **pandas:** `isin` is a plain membership test. NaN in `orders["customer_id"]` does not hurt the `~isin` result here (it matched my SQL answer), but a NaN on the customer side would count as "found" if the list also had NaN (Part 1 Q13 showed that).

**Then explain:**
- **Three equivalent safe forms:** LEFT JOIN + IS NULL, NOT EXISTS, and NOT IN with an `IS NOT NULL` filter all returned Chitra and Dev in my SQLite run.
- **Performance:** I am not claiming a speed difference from this run. Optimisers in many engines turn LEFT JOIN anti-joins and NOT EXISTS into the same plan, but that is engine specific (not executed here; Part 11 covers plans).
- **pandas:** `indicator=True` adds a `_merge` column with `left_only`, `right_only`, `both`. The `isin` form needs no merge and creates no extra rows, so it is the cheaper one to read.
- **Why order_id and not customer_id?** `customer_id` would also work for matched rows (the match means it is not NULL), but using the primary key of the right table is a habit that cannot go wrong.

**Follow-ups:**
- *Why does NOT IN fail?* One NULL in the subquery makes every comparison UNKNOWN.
- *Is LEFT JOIN IS NULL faster than NOT EXISTS?* Depends on the engine; measure it (hedged, not executed here).
- *How do I get customers that have orders?* The semi-join (Part 2 Q8).

**Common mistakes:**
- `WHERE o.customer_id IS NULL` is fine, but `WHERE o.amount IS NULL` mislabels customers whose order has a NULL amount.
- Putting an extra filter on the orders table in the WHERE instead of the ON (Part 2 Q3).
- `NOT IN` against a nullable column.
- In pandas, forgetting `indicator=True` and testing a column such as `amount` for NaN, which has the same trap as the SQL.
'''

P[3] = r'''
**Say this first (1 line):** A filter on the right table written in WHERE removes the NULL-padded rows and turns the LEFT JOIN into an INNER JOIN; put it in ON to keep customers with zero matches, and for an INNER JOIN it makes no difference.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1,'completed',100),(102,1,'completed',50),(103,1,'cancelled',40),
                          (104,2,'cancelled',75),(105,4,'completed',20);
```

**SQL answer:** in the Code block: `sql_on` (status in ON, correct), `sql_where` (status in WHERE, the trap), and `sql_inner_on` and `sql_inner_where` for the INNER JOIN case. All count with `COUNT(o.order_id)`.

**pandas answer:** filter the right frame first, then merge: `done = orders[orders["status"] == "completed"]; customers.merge(done, on="customer_id", how="left")`, then `groupby(...)["order_id"].count()`. The trap version merges first and filters after.

**Example:** The LEFT JOIN first pairs every customer with their orders. Ben has only a cancelled order, Chitra has none.
- Filter in ON: the condition decides which orders count as a match. Ben's cancelled order is not a match, so Ben is kept once with NULL order columns, and `COUNT(o.order_id)` counts 0. Chitra is the same. Asha has 2 completed matches and Dev has 1. Result: Asha 2, Ben 0, Chitra 0, Dev 1.
- Filter in WHERE: after the join, Ben's row is (cancelled), Chitra's row has `status` NULL. `NULL = 'completed'` is not true, so both rows are removed, and so is Asha's cancelled order. Result: Asha 2, Dev 1. The zero rows are gone, which is what an INNER JOIN would have given.

**Code:** run with `python3 -I`. Compared in `customer_id` order.
{CODE}

**Output (my run):**
{OUT}

**Edge cases:**
- **INNER JOIN:** ON and WHERE give identical results (the run shows both are Asha 2, Dev 1) because an inner join never keeps unmatched rows anyway.
- **`WHERE o.status = 'completed' OR o.status IS NULL` is not a fix:** it rescues only customers with no orders at all (Chitra). Ben, whose only order is cancelled, is still dropped. Use ON.
- **Conditions on the left table** (for example `c.city = 'Pune'`) are safe in WHERE for a LEFT JOIN, since they filter the preserved side.
- **Other engines:** this rule is part of standard SQL semantics, so I expect the same behaviour on other engines (not executed here).

**Then explain:**
- **Why:** ON decides which rows match; WHERE filters the joined rows afterwards. Unmatched left rows have NULLs on the right, and a comparison with NULL is not true.
- **Count the right column:** `COUNT(o.order_id)` counts matches only; `COUNT(*)` would give Ben and Chitra a 1 (Part 2 Q5).
- **pandas:** there is no ON versus WHERE, just order of operations. Filtering the right frame before `merge` equals the ON version; filtering after equals the WHERE version (my run: Ben and Chitra disappear).
- **Alternative:** a conditional count, `SUM(CASE WHEN o.status = 'completed' THEN 1 ELSE 0 END)`, over an unfiltered LEFT JOIN also keeps zeros. I did not run that variant.

**Follow-ups:**
- *Where would you put a condition on the left table?* WHERE is fine.
- *Does this apply to RIGHT JOIN?* Mirror image: filter on the left table belongs in ON.
- *Why not WHERE with IS NULL?* It rescues only customers with no orders at all, not customers with only non-completed orders, which is a different query.

**Common mistakes:**
- Writing the filter in WHERE and wondering why the zero rows vanished.
- Counting with `COUNT(*)`.
- Assuming the result changes for an INNER JOIN.
- In pandas, merging first and filtering the merged frame.
'''

P[4] = r'''
**Say this first (1 line):** Join the employees table to itself as `e` (employee) and `m` (manager) on `e.manager_id = m.emp_id`, then keep rows where `e.salary > m.salary`; the top person has a NULL manager_id, matches nothing, and never appears.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER, manager_id INTEGER);
INSERT INTO employees VALUES (1,'Ann',90,NULL),(2,'Bob',60,1),(3,'Cy',100,1),(4,'Di',70,2),(5,'Eli',55,2);
```
Salaries are toy column data.

**SQL answer:** `sql` in the Code block (an INNER JOIN of `employees e` to `employees m`, with the salary comparison in WHERE). `sql_all` lists every employee-manager pair.

**pandas answer:** `emp.merge(emp, left_on="manager_id", right_on="emp_id", suffixes=("_emp", "_mgr"))` then filter `salary_emp > salary_mgr`.

**Example:** Pairs produced by the join: Bob-Ann, Cy-Ann, Di-Bob, Eli-Bob (Ann has no manager so she has no pair). Compare salaries: Bob 60 vs Ann 90, no. Cy 100 vs Ann 90, yes. Di 70 vs Bob 60, yes. Eli 55 vs Bob 60, no. Answer: Cy and Di.

**Code:** run with `python3 -I`. Compared in `emp_id` order.
{CODE}

**Output (my run):**
{OUT}

**Edge cases:**
- **Top person:** `manager_id` is NULL, so the INNER JOIN has no partner. That is correct for this question (the CEO earns more than nobody). If you need everyone listed with the manager shown, use a LEFT JOIN (Part 2 Q22).
- **Manager who left (dangling manager_id):** also dropped by the INNER JOIN.
- **Equal salaries:** `>` excludes ties.
- **pandas dtype:** `manager_id` became `float64` because of the NULL (my run printed it in the Code output above). The merge against the `int64` `emp_id` still matched correctly.
- **pandas NaN key:** the NaN manager_id has no NaN partner in `emp_id`, so no false match appears here.

**Then explain:**
- **Two aliases:** the same table plays two roles; `e` is the employee row, `m` is the manager row reached through `manager_id`. Without aliases the column names are ambiguous.
- **Why the top person never appears:** NULL never equals anything, so there is no manager row to compare with.
- **pandas suffixes:** merging a frame with itself duplicates every column name, so `suffixes` is what makes `salary_emp` and `salary_mgr` distinguishable (without it you would get `_x` and `_y`).
- **Alternative:** a correlated subquery, `WHERE salary > (SELECT salary FROM employees WHERE emp_id = e.manager_id)`, also works; I did not run it, and the join reads more naturally when you want manager columns in the output.

**Follow-ups:**
- *How do I also list employees without a manager?* LEFT JOIN, then the salary condition must handle NULL.
- *Employees earning more than the average of their team?* Aggregate by manager first (Part 3).
- *Two levels up?* Another self join, or a recursive CTE (Part 9).

**Common mistakes:**
- Joining on `e.emp_id = m.manager_id` (reversed: gives managers with their reports, and the comparison is flipped).
- Forgetting the second alias.
- Expecting the top person in the output.
- In pandas, omitting `suffixes` and reading `salary_x`/`salary_y` backwards.
'''

P[5] = r'''
**Say this first (1 line):** LEFT JOIN products to sales, group by product, and use `COALESCE(SUM(s.qty), 0)`; count with `COUNT(s.sale_id)` because `COUNT(*)` counts the NULL-padded row and reports 1 for products that never sold.

**Schema and sample data:**
```sql
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, product_id INTEGER, qty INTEGER);
INSERT INTO products VALUES (1,'Pen'),(2,'Book'),(3,'Bag'),(4,'Cap');
INSERT INTO sales VALUES (1,1,5),(2,1,3),(3,2,4);
```

**SQL answer:** `sql` in the Code block (LEFT JOIN, `COALESCE(SUM(s.qty), 0)` as `units`, `COUNT(s.sale_id)` as `n_sales`). `sql_bad` shows `COUNT(*)`, `COUNT(s.sale_id)` and the raw `SUM` side by side.

**pandas answer:** `products.merge(sales, on="product_id", how="left")`, then `groupby(["product_id","name"]).agg(units=("qty","sum"), n_sales=("sale_id","count"))`, then `fillna(0).astype("int64")` on `units`.

**Example:** Pen sold 5 + 3 = 8 in 2 sales, Book 4 in 1 sale. Bag and Cap have no sales rows, so the LEFT JOIN gives each one row with NULL `qty` and NULL `sale_id`.
- `SUM(s.qty)` over only NULLs is NULL, so `COALESCE` turns it into 0.
- `COUNT(*)` counts that single padded row, giving 1 (wrong). `COUNT(s.sale_id)` skips NULLs, giving 0 (right).

**Code:** run with `python3 -I`. Compared in `product_id` order.
{CODE}

**Output (my run):**
{OUT}

**Edge cases:**
- **Sale row with NULL qty:** `SUM` ignores it, `COUNT(s.sale_id)` still counts the sale. So units and sale count can disagree; decide which one you mean. I did not run this case.
- **Product with only NULL qty rows:** same as no sales for the sum, COALESCE gives 0.
- **Ties and ordering:** the output order is set by `ORDER BY p.product_id`, not by the join.
- **pandas dtype:** after the left merge `qty` is `float64` (NaN needs a float). Surprise from my run: `groupby(...).sum()` already returned 0 for the unsold products (an all-NaN group sums to 0 by default), so the sum was `float64` with no NaN. `fillna(0)` therefore changed nothing there, and the `astype("int64")` is what restores integers. To get SQL's NULL for an all-NULL group you need `sum(min_count=1)`, which gave NaN for Bag.
- **pandas size():** `groupby.size()` counts rows including the padded one, like `COUNT(*)`; `count()` on a column skips NaN, like `COUNT(col)`.

**Then explain:**
- **Why LEFT JOIN:** an inner join drops products that never sold, so they could not show 0.
- **COALESCE:** turns the NULL sum into 0 at the end, after aggregation.
- **COUNT variants:** `COUNT(*)` = rows, `COUNT(col)` = non-NULL values. After an outer join, count a right-table column.
- **pandas:** `fillna` before or after the groupby both work here; the dtype is the point to mention.

**Follow-ups:**
- *Why not `COALESCE(s.qty, 0)` inside the SUM?* Also fine; `SUM(COALESCE(s.qty,0))` returns 0 directly. The outer COALESCE is cheaper to read.
- *What if you also want a revenue column?* Same pattern, but aggregate sales to one row per product first if other one-to-many tables join in (Part 2 Q12).
- *What does SUM of no rows return?* NULL in SQL, which is why the COALESCE is needed.

**Common mistakes:**
- `COUNT(*)` giving 1 for unsold products.
- `INNER JOIN` dropping the zeros.
- Putting a sales filter in WHERE (Part 2 Q3).
- Leaving pandas units as `float64` and printing 8.0, or assuming `fillna` fixes the dtype.
'''

P[6] = r'''
**Say this first (1 line):** A NULL join key matches nothing in SQL (`NULL = NULL` is not true), so those employees vanish from an INNER JOIN and appear with a NULL dept_name in a LEFT JOIN; pandas does the opposite and matches NaN keys with each other.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER);
CREATE TABLE departments(dept_id INTEGER, dept_name TEXT);          -- dept_id nullable, no PK
INSERT INTO employees VALUES (1,'Asha',10),(2,'Ben',20),(3,'Chitra',NULL),(4,'Dev',NULL),(5,'Esha',30);
INSERT INTO departments VALUES (10,'Sales'),(20,'Eng'),(NULL,'Unassigned');
```
Esha has dept 30, which does not exist. The departments table has a NULL-key row on purpose, to show that it still does not match.

**SQL answer:** in the Code block: `sql_inner` (`ON e.dept_id = d.dept_id`, INNER), `sql_left` (same ON, LEFT), `sql_is` (LEFT with `ON e.dept_id IS d.dept_id`) and `sql_isndf` (LEFT with `IS NOT DISTINCT FROM`).

**pandas answer:** the plain `emp.merge(dep, on="dept_id", how=...)`, and the SQL-like version that first drops NaN keys: `emp.dropna(subset=["dept_id"])` and `dep.dropna(subset=["dept_id"])` (for the LEFT case drop only on the right so unmatched employees stay).

**Example:**
- INNER with `=`: Asha matches Sales, Ben matches Eng. Chitra and Dev have a NULL key, `NULL = NULL` is UNKNOWN, no match, dropped. Esha has no dept 30, dropped. 2 rows.
- LEFT with `=`: the same two matches plus Chitra, Dev and Esha with NULL `dept_name`. 5 rows. Note that Chitra and Dev do not pick up the 'Unassigned' row.
- Null-safe `IS`: Chitra and Dev now match the NULL-key department row and get 'Unassigned'. Esha stays NULL.
- pandas merge: the NaN keys match each other, so even an inner merge returns 4 rows including Chitra and Dev with 'Unassigned'.

**Code:** run with `python3 -I`. Compared in `emp_id` order.
{CODE}

**Output (my run):**
{OUT}

**Edge cases:**
- **Both sides NULL is the only case where pandas and `=` disagree**, but it changes row counts, so check it before merging real data.
- **One side NULL only:** no match in either world.
- **Many NaN keys on both sides:** pandas matches every NaN left row with every NaN right row (a Cartesian product within the NaN group). With 2 NaN-key employees and 3 NaN-key departments that is 6 rows (the Code block runs this and prints it).
- **dtype:** `dept_id` became `float64` in both frames because of the NULLs, and the merge still worked.

**Then explain:**
- **Why:** NULL means unknown, and an unknown can't be said to equal another unknown. The comparison is UNKNOWN and joins keep only TRUE.
- **Null-safe operators (hedged dialect notes):** `IS NOT DISTINCT FROM` is standard SQL and works in PostgreSQL (not executed here); MySQL's equivalent is `<=>` (not executed here); SQLite's `IS` works for any two values (run here). In my run SQLite 3.45.1 also accepted `IS NOT DISTINCT FROM`, so the standard form works in SQLite too (I believe it arrived in 3.39 along with RIGHT/FULL JOIN; that version number is from memory).
- **pandas:** `merge` matches NaN with NaN. To get SQL behaviour, drop NaN keys first, as the Code block does and asserts equal to the SQL result. The pandas user guide page I opened did not state this; I confirmed it by running.
- **Practical rule:** decide what a missing key should mean. If you want "unassigned" rows grouped, say so explicitly; do not let the join decide.

**Follow-ups:**
- *Is a NULL-safe join index-friendly?* Usually not as well as plain equality in many engines (hedged, not executed here).
- *How do I keep employees with no department?* LEFT JOIN.
- *Can I replace NULL with a sentinel like -1?* Yes in the join (`COALESCE(dept_id, -1)`), but it makes the unassigned group match deliberately and can mask data problems.

**Common mistakes:**
- Expecting NULL-keyed employees to join the 'Unassigned' row.
- Assuming pandas follows SQL on NaN keys.
- Using `WHERE d.dept_id IS NULL` to find unmatched rows when NULL keys on the left also qualify.
- Forgetting to check row counts after a merge.
'''

P[7] = r'''
**Say this first (1 line):** `merge` is a SQL join: `how=` is the join type (default `inner`), `on`/`left_on`/`right_on` is the ON clause, `suffixes` renames clashing columns (default `_x`/`_y`), `indicator=True` adds a `_merge` column showing which side matched, and `validate=` raises an error if the key relationship is not what you assumed.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, created_at TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, cust_id INTEGER, amount INTEGER, created_at TEXT);
INSERT INTO customers VALUES (1,'Asha','2024-01-01'),(2,'Ben','2024-02-01'),(3,'Chitra','2024-03-01');
INSERT INTO orders VALUES (101,1,50,'2024-05-01'),(102,1,20,'2024-05-02'),(103,2,30,'2024-05-03'),(104,9,10,'2024-05-04');
```
Order 104 points to customer 9, who does not exist. Chitra has no orders.

**SQL answer:** `sql` in the Code block: a FULL OUTER JOIN `ON c.customer_id = o.cust_id`, with the two `created_at` columns aliased `created_at_cust` and `created_at_order`.

**pandas answer:** `customers.merge(orders, how="outer", left_on="customer_id", right_on="cust_id", suffixes=("_cust","_order"), indicator=True, validate="one_to_many")`, in the Code block as `p`.

**Example:** Matches: Asha twice (101, 102) and Ben once (103). Chitra is `left_only`, order 104 is `right_only`. Total 5 rows, which is the SQL FULL JOIN row count.

| pandas argument | SQL clause | what it guards against |
|---|---|---|
| `how="inner"` (default) | `INNER JOIN`, or just `JOIN` | surprise loss of unmatched rows if you expected a left join |
| `how="left"`/`"right"`/`"outer"`/`"cross"` | `LEFT`/`RIGHT`/`FULL OUTER`/`CROSS JOIN` | choose which unmatched rows survive |
| `on="k"` | `USING (k)` or `ON a.k = b.k` | same-named key, one output key column |
| `left_on`, `right_on` | `ON a.customer_id = b.cust_id` | differently named keys; both key columns stay in the output |
| `suffixes=("_a","_b")` | column aliases `AS created_at_a` | silent `_x`/`_y` names you then misread |
| `indicator=True` | a hand-made `CASE WHEN a.k IS NULL ...` flag | not knowing which rows are unmatched |
| `validate="one_to_many"` | a uniqueness constraint on the `one` side | duplicate keys silently multiplying rows |

**Code:** run with `python3 -I`. Rows compared after sorting (NaN as None).
{CODE}

**Output (my run):**
{OUT}

**Edge cases:**
- **Default suffixes:** without `suffixes`, the two `created_at` columns came out as `created_at_x` (left) and `created_at_y` (right) in my run. `_x` is the left frame, `_y` the right.
- **`left_on`/`right_on` keeps both keys:** in an outer merge `customer_id` is NaN for the orphan order and `cust_id` is NaN for Chitra (see the printed frame). With `on="customer_id"` you would get a single combined key column (Part 2 Q39).
- **validate on duplicates:** a duplicated customer made `validate="one_to_many"` raise `MergeError: Merge keys are not unique in left dataset; not a one-to-many merge`. Without `validate`, the same merge silently returned 5 rows instead of 3.
- **NaN keys** match each other (Part 2 Q6).
- **Float display:** `customer_id` shows as 1.0, 2.0 because the outer merge introduces NaN.

**Then explain:**
- **Default how:** `inner`, so unmatched rows disappear without a warning.
- **`_merge` values:** `left_only`, `right_only`, `both`; the counts in my run were 3 both, 1 left_only, 1 right_only.
- **validate options:** `one_to_one`, `one_to_many`, `many_to_one`, `many_to_many`. It checks key uniqueness on the sides named "one". It does not check that every row matched; use `indicator` for that.
- **Write `validate` on every production merge:** it is the pandas analogue of a primary-key constraint on the lookup side.

**Follow-ups:**
- *What if the key columns have different dtypes?* A ValueError or silent mismatches (Part 2 Q35).
- *join versus merge?* `DataFrame.join` is index-based and defaults to a left join (Part 2 Q23).
- *How do I drop the extra key column?* `.drop(columns="cust_id")` after the merge.

**Common mistakes:**
- Assuming the default is a left join.
- Reading `_x` and `_y` as "first" and "second" without checking which frame is which.
- Not passing `validate=` and finding duplicate keys after the totals look wrong.
- Forgetting that `left_on`/`right_on` leaves two key columns.
'''

P[8] = r'''
**Say this first (1 line):** For "customers with at least one order" use `WHERE EXISTS (correlated subquery)`; `IN` and `JOIN ... DISTINCT` give the same customers, a plain JOIN returns a customer once per order, and EXISTS is the form that never depends on NULLs.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1,100),(102,1,50),(103,2,75),(104,NULL,30);   -- 104 = guest, NULL customer
```

**SQL answer:** in the Code block: `sql_exists`, `sql_in`, `sql_join_distinct` and, for the contrast, `sql_plain_join`.

**pandas answer:** `customers[customers["customer_id"].isin(orders["customer_id"])]`, or `customers.merge(orders[["customer_id"]].drop_duplicates(), on="customer_id")`.

**Example:** Orders belong to customers 1, 1, 2 and a guest (NULL). Asha and Ben have orders, Chitra and Dev do not. The semi-join returns Asha and Ben, once each. A plain JOIN produces a row per order: Asha, Asha, Ben (3 rows), because Asha has two orders.

**Code:** run with `python3 -I`. Compared in `customer_id` order.
{CODE}

**Output (my run):**
{OUT}

**Edge cases:**
- **NULL in the subquery:** harmless here for `IN` (a positive `IN` can still be TRUE for real matches) and for EXISTS. It breaks only the negated forms, `NOT IN` (Part 2 Q2).
- **Safest form:** EXISTS. It stays correct whether the subquery column holds NULLs or not, and the negated form (`NOT EXISTS`) is just as safe, so one habit covers both semi and anti joins.
- **Duplicates in the right table:** EXISTS and IN ignore them; JOIN multiplies them, so aggregates over the joined rows are inflated (Part 2 Q12).
- **pandas dtype:** the orders key was `float64` because of the NULL; `isin` still matched the integer customer ids correctly in my run.
- **Customers with duplicate ids in the left table** would be returned twice by every form, since the duplication is on the left.

**Then explain:**
- **Semi-join:** return left rows that have a match, without returning right columns and without multiplying rows.
- **JOIN + DISTINCT** works but does extra work to remove duplicates it should never have created, and it only works if the selected columns identify the customer (DISTINCT over `name` alone would merge two different customers with the same name).
- **pandas:** `isin` is a membership test and returns the original rows. The merge form needs `drop_duplicates()` on the key first, or you reproduce the plain-JOIN row multiplication (3 rows in my run).
- **Engines:** many optimisers turn EXISTS and IN into a semi-join plan, but I did not check any plan here (hedged; not executed).

**Follow-ups:**
- *Which is faster, IN or EXISTS?* Depends on the engine and version; modern optimisers often treat them the same (not executed here).
- *Need columns from the orders table?* Then a JOIN is the right tool, and you must decide how to handle several orders per customer.
- *The opposite?* Anti-join (Part 2 Q2).

**Common mistakes:**
- Using a plain JOIN and getting duplicates, then "fixing" with `SELECT DISTINCT *`.
- Using `DISTINCT` on a column that is not the customer key.
- Believing the NULL trap applies to `IN` the same way it does to `NOT IN`.
- Merging without deduplicating the keys in pandas.
'''

P[9] = r'''
**Say this first (1 line):** If the lookup table repeats a key, every joined row is repeated and counts and revenue inflate silently; find the duplicate keys with `GROUP BY key HAVING COUNT(*) > 1`, fix the load or add a key constraint, and in pandas use `validate="many_to_one"` so the merge raises `MergeError`.

**Schema and sample data:**
```sql
CREATE TABLE products(product_id INTEGER, name TEXT, price INTEGER);      -- no PK: loaded twice
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, qty INTEGER);
INSERT INTO products VALUES (1,'Pen',10),(1,'Pen',10),(2,'Book',20),(3,'Cap',5);
INSERT INTO order_items VALUES (1,1,1,2),(2,1,2,1),(3,2,3,4);
```
Product 1 (Pen) was loaded twice.

**SQL answer:** in the Code block: the "bad" join (`order_items` JOIN `products`), `sql_detect` (the GROUP BY HAVING query), and `sql_fix` (join to a derived table of `SELECT DISTINCT product_id, name, price FROM products`). The source fix is the `products_clean` table with `PRIMARY KEY`.

**pandas answer:** `products[products.duplicated("product_id", keep=False)]` to see them, `items.merge(products, on="product_id", validate="many_to_one")` to raise, and `products.drop_duplicates(subset=["product_id","name","price"])` to fix.

**Example:** True revenue: item 1 is 2 x 10 = 20, item 2 is 1 x 20 = 20, item 3 is 4 x 5 = 20, total 60. Pen appears twice in `products`, so item 1 joins to two rows and counts twice (40). Result: 4 rows and revenue 80 instead of 3 rows and 60. Nothing errored.

**Code:** run with `python3 -I`.
{CODE}

**Output (my run):**
{OUT}

**Edge cases:**
- **Exact duplicates vs conflicting duplicates:** `DISTINCT` fixes the first kind (same price twice). If product 2 had two different prices, `DISTINCT` keeps both rows, as my run shows (2 rows for product 2). Then you need a rule (latest load, MAX, a date column) or a data fix.
- **Duplicate keys with no matching items:** harmless to this join, but they will bite later.
- **NULL keys** in the lookup do not join but are not flagged by `HAVING COUNT(*) > 1` as a join problem; check `COUNT(*) - COUNT(product_id)` as well (I did not run that check).
- **Fix at the source:** a `PRIMARY KEY` or `UNIQUE` constraint rejects the second row (my run: `IntegrityError: UNIQUE constraint failed: products_clean.product_id`). Cloud warehouses often do not enforce primary keys (hedged, not executed here), so add a test or an assertion in the load job.

**Then explain:**
- **Why inflation:** a join returns one row per matching pair, so 2 matching lookup rows turn one item into 2.
- **Detect:** `GROUP BY key HAVING COUNT(*) > 1` finds repeated keys; also compare `COUNT(*)` of the join to `COUNT(*)` of the fact table.
- **Source vs query:** fix the load and add a constraint so every consumer is safe. De-duplicating inside each query is a workaround, and it hides a data quality problem.
- **pandas:** `validate="many_to_one"` raised `MergeError: Merge keys are not unique in right dataset; not a many-to-one merge`. The naive merge returned 4 rows and revenue 80, same as the SQL.

**Follow-ups:**
- *Which duplicate do you keep?* Define it (latest by timestamp, highest version) and write it down.
- *How do I alert on this?* A scheduled check that returns rows from the HAVING query and fails if non-empty.
- *Is it only a problem for SUM?* No; counts and averages are distorted too.

**Common mistakes:**
- Checking the total against a different join and trusting it.
- Using `DISTINCT *` on the final result.
- Fixing conflicting duplicates with `DISTINCT`.
- Skipping `validate=` in pandas.
'''

P[10] = r'''
**Say this first (1 line):** Stack rows with `UNION ALL` (keeps every row, cheapest) or `UNION` (removes duplicates, costs a sort or hash and can drop real rows) when two tables describe the same kind of row, and join side by side when you want extra columns about the same entity; in pandas that is `concat` versus `merge`.

**Schema and sample data:**
```sql
CREATE TABLE web_orders(order_id INTEGER, customer_id INTEGER, amount INTEGER);
CREATE TABLE store_orders(order_id INTEGER, customer_id INTEGER, amount INTEGER);
INSERT INTO web_orders   VALUES (1,10,100),(2,11,50),(3,12,75);
INSERT INTO store_orders VALUES (3,12,75),(4,10,100),(5,13,20);   -- order 3 is loaded in both channels
```

**SQL answer:** in the Code block: `sql_all` (UNION ALL), `sql_union` (UNION), `sql_chan` (UNION ALL with a literal `channel` column), `sql_proj_all` and `sql_proj_union` (only `customer_id, amount`), and `sql_join` (side by side).

**pandas answer:** `pd.concat([web, store], ignore_index=True)` for UNION ALL, `.drop_duplicates()` for UNION, `web.assign(channel="web")` before the concat to add the channel, and `web.merge(store, on="order_id", suffixes=("_web","_store"))` for a side-by-side join.

**Example:** 3 web + 3 store rows = 6 rows with UNION ALL. Order 3 is in both tables with identical values, so `UNION` removes one copy: 5 rows. With a `channel` column the two copies of order 3 differ ('web' versus 'store'), so even `UNION` keeps both (my run prints 6 for that case). Projected to `(customer_id, amount)` only, `UNION` returns 4 rows from 6: it merges the duplicated order 3, which is fine, but it also merges orders 1 and 4, two different orders by customer 10 for 100, which is a real loss. The join on `order_id` returns only order 3, the one order present in both tables.

**Code:** run with `python3 -I`. Rows compared after sorting.
{CODE}

**Output (my run):**
{OUT}

**Edge cases:**
- **Legitimate duplicates:** two real orders with the same customer and amount look identical once `order_id` is dropped. `UNION` removes one, so a total computed afterwards is short. Use `UNION ALL` unless you really want set semantics.
- **Column count:** must match; SQLite error in my run: "SELECTs to the left and right of UNION ALL do not have the same number of result columns".
- **Types:** matching types are required by the standard; how strictly each engine enforces or coerces them differs (not executed here; I only tested the column-count error). Cast explicitly.
- **Column names:** the result takes names from the first SELECT; matching is by position, not by name. In pandas `concat` matches by column name and fills missing columns with NaN.
- **NULLs:** `UNION` treats NULLs as equal when de-duplicating (stated in the SQL standard; not tested here).
- **Cost:** `UNION` has to compare rows, usually via a sort or hash (hedged; I did not measure it), so it is slower than `UNION ALL` on large inputs.

**Then explain:**
- **Stack vs join:** stack when the tables are the same entity split by source or time (web and store orders). Join when the tables describe different facts about the same key (orders and customers). The test is: do I want more rows or more columns?
- **Add a channel column** before stacking, or you cannot tell where a row came from; it also keeps cross-channel copies of one order distinguishable.
- **De-duplicate on a key, not on all columns:** if you need "one row per order_id" across channels, decide the rule explicitly rather than relying on `UNION`.
- **pandas:** `concat` is `UNION ALL` (it never de-duplicates), `drop_duplicates` makes it `UNION`, and `merge` is the join. All asserts in the Code block compare these to SQL.

**Follow-ups:**
- *Does UNION ALL guarantee order?* No; add ORDER BY.
- *What if the column order differs between the two tables?* Name the columns in each SELECT so position matches.
- *Join or union for comparing channels?* A FULL JOIN on order_id (Part 2 Q16).

**Common mistakes:**
- Using `UNION` "to be safe" and silently dropping rows.
- Different column order between the SELECTs.
- Forgetting a source label.
- Using `merge` where `concat` is needed (merge returned 1 row here).
'''

P[11] = r'''
**Say this first (1 line):** Rows in a join = for each key, (rows on the left with that key) x (rows on the right with that key), plus unmatched rows for outer joins; with 100 customers, 450 orders and 20 customers without orders, INNER is 450, LEFT 470, RIGHT 450, FULL 470 and CROSS 45,000.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER, name TEXT);
CREATE TABLE orders(order_id INTEGER, customer_id INTEGER, amount INTEGER);
-- 100 customers (ids 1..100); 450 orders (ids 1..450) spread over customers 1..80 (customers 81..100 never order)
```
The data is generated in the Code block (loops), not typed in by hand; the sizes are the point.

**SQL answer:** the `COUNT(*)` queries over each join type in the Code block (the dict `counts`), plus the grain checks `COUNT(*)` versus `COUNT(DISTINCT customer_id)` on each table.

**pandas answer:** `len(cust.merge(orders, on="customer_id", how=...))` for each `how`, `cust["customer_id"].is_unique`, `cust["customer_id"].nunique()`, and `validate="one_to_many"` as a guard.

**Example (by hand):**
- Every order has a valid customer and the key is unique in `customers`, so each order matches exactly one customer. INNER = 450.
- LEFT keeps all 100 customers: 450 matched rows, plus the 20 customers with no orders, once each. 450 + 20 = 470.
- RIGHT keeps all 450 orders. Every order already matched, so there are no extra rows: 450.
- FULL: 450 matched + 20 unmatched customers + 0 unmatched orders = 470.
- CROSS: 100 x 450 = 45,000, no keys involved.
- Duplicated key in `customers`: if customers 1 to 5 are each loaded twice, every order of those customers matches twice. In my data customers 1 to 5 have 6 orders each (30 orders), so INNER grows by 30 to 480. If customer 90 (no orders) is also duplicated, LEFT grows by 1 for that unmatched row on top: 480 + 20 + 1 = 501.

**Code:** run with `python3 -I`.
{CODE}

**Output (my run):**
{OUT}

**Edge cases:**
- **One-to-one:** at most min(left, right) rows for INNER.
- **Many-to-many:** the per-key product can exceed both table sizes (Part 2 Q34).
- **NULL keys:** never match, so they are missing from INNER and appear once in outer joins.
- **Empty table:** INNER and CROSS give 0, outer joins give the preserved side.
- **Filters in ON versus WHERE** change outer-join counts (Part 2 Q3).

**Then explain:**
- **Cardinality:** one-to-one (each key at most once on both sides), one-to-many (the key is unique on one side only; the many side drives the row count), many-to-many (neither side unique; rows multiply per key).
- **Estimate before running:** know the grain (what one row means) and key uniqueness of each table, then apply the formula `sum over keys of left_count x right_count`. The Code block applies that formula with a `Counter` and gets 480 and 501, matching the real joins.
- **Verify the grain:** `COUNT(*)` equals `COUNT(DISTINCT key)` only if the key is unique. Here both were 100 for customers and 450 for orders. After the duplicates were loaded, pandas showed 106 rows but 100 unique ids.
- **pandas check:** `is_unique`, `nunique()` versus `len`, `validate=`, and `len(result)` compared with the expected number.

**Follow-ups:**
- *Why is the CROSS JOIN count useful?* It is the upper bound of any join, a sanity limit.
- *What if the join is on a non-unique key on both sides?* Multiply per key, then sum.
- *How do I guard this in production?* Row-count assertions and constraints (Part 2 Q40).

**Common mistakes:**
- Assuming a LEFT JOIN returns exactly the left row count.
- Forgetting the unmatched rows in the outer-join count.
- Trusting a key is unique because it is named `id`.
- Counting rows after the join and not before.
'''

P[12] = r'''
**Say this first (1 line):** Joining orders to order_items repeats each order's `order_total` once per item, so `SUM(order_total)` over the join adds it several times; sum from `orders` alone, or aggregate the items to one row per order before joining, and do not use `SUM(DISTINCT)` because it drops legitimate equal totals.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_total INTEGER);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, qty INTEGER);
INSERT INTO orders VALUES (1,1,100),(2,1,50),(3,2,80),(4,2,80),(5,3,40);
INSERT INTO order_items VALUES (1,1,7,1),(2,1,8,2),(3,2,7,1),(4,3,7,1),(5,3,8,1),(6,3,9,3),(7,4,7,1);
-- order 1 has 2 items, 2 has 1, 3 has 3, 4 has 1, 5 has none
```

**SQL answer:** in the Code block: `sql_bug` (the analyst's query), `sql_orders_only`, `sql_distinct` (`SUM(DISTINCT ...)`, also wrong), `sql_fix` (LEFT JOIN to a derived table that sums `qty` per `order_id`) and `sql_fix_units` (the fix when you need item totals as well).

**pandas answer:** the bug is `orders.merge(items, on="order_id")["order_total"].sum()`; the fixes are `orders["order_total"].sum()` or `per_order = items.groupby("order_id", as_index=False).agg(units=("qty","sum"))` then `orders.merge(per_order, on="order_id", how="left", validate="one_to_one")`.

**Example:** True revenue: 100 + 50 + 80 + 80 + 40 = 350.
- Joined (INNER): order 1 appears 2 times (200), order 2 once (50), order 3 three times (240), order 4 once (80). Order 5 has no items so it disappears. Total 570, which is 1.63 times the true value and not "double". It is double only if every order has exactly two items.
- `SUM(DISTINCT order_total)` over the join: the distinct values are 100, 50, 80 (the 40 is gone with order 5). Total 230. Orders 3 and 4 have the same total of 80 and one of them is lost, so this is wrong in the other direction.
- Pre-aggregated: one row per order in the derived table, so the join cannot repeat order rows. Total 350.

**Code:** run with `python3 -I`.
{CODE}

**Output (my run):**
{OUT}

**Edge cases:**
- **Orders with no items:** an INNER JOIN drops them (order 5, 40 missing). Even a correct pre-aggregation needs a LEFT JOIN if you want them counted.
- **Premise check:** the question says "double"; the multiplier depends on the number of items per order (here 570 versus 350). The same query would also be too small if orders without items were large.
- **COUNT:** `COUNT(DISTINCT o.order_id)` rescues a count of orders, but not a sum.
- **pandas:** `validate="one_to_many"` passed on the buggy merge, because the merge is legitimately one-to-many. The bug is in the aggregation, not in the join. `validate="one_to_one"` on the fixed merge guards the grain.
- **Dropping duplicates on the value** (`order_total.drop_duplicates()`) gave the same wrong 230 as `SUM(DISTINCT)`; dropping duplicates on `order_id` would be right but is just a roundabout way of summing from `orders`.

**Then explain:**
- **Why:** the join returns one row per item (7 rows from 5 orders), and the order-level column is carried on each. SUM adds every copy.
- **Rule:** only aggregate a column at the grain where it lives. Order-level numbers belong to the orders grain; item-level numbers to the items grain.
- **Fixes in order of preference:** (1) sum from the table where the column lives; (2) if you need both levels, aggregate the many side to the parent's grain, then join; (3) avoid `SUM(DISTINCT)`.
- **Detect it:** compare `COUNT(*)` before and after the join, and compare the total to the same sum from the source table (570 versus 350 here).

**Follow-ups:**
- *What if I need revenue per product and per order?* Different grains, different queries (Part 2 Q13, two child tables).
- *Is there a safe DISTINCT form?* Only over a pair like `(order_id, order_total)` in a derived table, and aggregating that; it is clearer to sum from `orders`.
- *Does a window function fix it?* It can (Part 4); the grain rule is the same.

**Common mistakes:**
- Using `SUM(DISTINCT)`.
- Blaming the data when the total is 570 and the source says 350.
- Not noticing the INNER JOIN also removed orders without items.
- In pandas, trusting `validate=` to catch this bug.
'''
