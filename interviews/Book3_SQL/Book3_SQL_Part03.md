# Book 3 — Part 3: Subqueries and CTEs with pandas equivalents

**Topic:** scalar subqueries in SELECT and WHERE (zero and many rows per engine), IN and NOT IN subqueries and the NULL trap, EXISTS and NOT EXISTS, correlated subqueries and per-row execution, derived tables and aliasing, ANY/SOME/ALL and their MAX/MIN/EXISTS equivalents, subquery versus JOIN equivalence, subqueries in HAVING, percent of total and above-average comparisons with scalar subqueries, nth-highest, median and top-N per group without window functions, max-per-group ties, relational division (GROUP BY HAVING COUNT DISTINCT and double NOT EXISTS), CTE syntax, naming, chained CTEs and CTE reuse, CTE versus subquery versus view versus temp table, CTE scaffolding for cohort and funnel questions, refactoring nested queries, debugging a join fan-out hidden in a CTE, UPDATE, DELETE and INSERT ... SELECT with subqueries, LIMIT inside subqueries, and the pandas side (boolean masks, groupby transform, isin and map from aggregated frames, merge of aggregated frames, query, pipe and assign, NaN pitfalls)
**Target:** 40  |  **Actual:** 40 (⭐⭐⭐ 16, ⭐⭐ 14, ⭐ 10)  |  **Date:** 2026-10-24  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part covers subqueries and non-recursive CTEs. Window functions (Parts 4 and 5) are deliberately absent: nth-highest, top-N per group, max-per-group and running comparisons are answered here without them and each points to the window version in Part 4 or 5. Recursive CTEs (Part 9), retention and funnel logic (Parts 6 and 8) and EXPLAIN-level tuning (Part 11) are out of scope; the CTE scaffolding questions only build the step-by-step structure. Every query question states its tables and columns so Wave B can build small sample data; answers must run on SQLite 3.45 and compare with pandas 3.0.x, and anything engine-specific is shown as hedged text labelled 'not executed'.

Verification notes for Wave B (from pages opened in Wave A, as summarised by the fetch tool): the SQLite expression page says a scalar subquery's value is the first row of its result and NULL when there are no rows, EXISTS gives 1 or 0 regardless of NULLs, an empty right side gives IN false and NOT IN true even for a NULL left operand, a NULL on either side with no match gives NULL for IN and NOT IN, and a correlated subquery is re-evaluated when needed while an uncorrelated one is evaluated once. The SQLite WITH page says CTEs can prefix SELECT, INSERT, DELETE and UPDATE, MATERIALIZED and NOT MATERIALIZED need 3.35.0, the default lets SQLite choose, and WITH cannot be used inside CREATE TRIGGER. The PostgreSQL pages say a non-recursive side-effect-free CTE referenced once is folded into the parent by default and a multiply referenced CTE is materialised by default, that a scalar subquery returning more than one row is an error, that IN is = ANY and NOT IN is <> ALL, and that ALL over an empty subquery is true. The MySQL 8.4 pages say modifying a table and selecting from it in a subquery is restricted (error number 1093 was not on the page and comes from general knowledge), a materialized derived table is the workaround, LIMIT in IN, ALL, ANY or SOME subqueries gives error 1235, WITH is allowed before SELECT, UPDATE and DELETE, and a CTE can be referenced several times unlike a derived table. The pandas groupby page says transform returns a result indexed like the input with the aggregate broadcast, and that NA group keys are dropped unless dropna=False; the Comparison with SQL page says null merge keys match each other. Items NOT verified from pages (run or hedge): whether SQLite requires an alias on a FROM-subquery (the SELECT page excerpt was truncated), SQLite behaviour for LIMIT -1 and expression LIMIT/OFFSET, UPDATE ... FROM support in SQLite 3.33+, row-value comparison support, the exact MySQL error for a many-row scalar subquery (1242 from general knowledge), PostgreSQL 12 as the version of the inlining change (from a guide and general knowledge), and any SQL Server, Oracle, BigQuery or Snowflake behaviour.

Evidence limits: no candidate-reported SQL questions were found; the search returned prep guides, practice-site lesson pages and documentation. The 'Asked at' tags are source types, and 'expert gap-check' marks questions chosen from practice. Star ratings blend how often a topic appears across guides with judgement. See research_notes/Book3_Part03_sources.md for which pages were opened.

---

### Q1 ⭐⭐⭐ 🟢 Scalar subquery in WHERE and in SELECT: employees(emp_id, name, dept_id, salary) has some NULL salaries. List employees earning more than the company average salary, and in a second query show each employee's salary next to the company average and the difference. Explain that an uncorrelated scalar subquery is evaluated once, that AVG ignores NULL salaries, what happens to a NULL salary row in the comparison, and give the pandas boolean-mask version (mean computed once, NaN rows dropped by the comparison).
**Asked at:** StrataScratch 'Understanding Subqueries' lesson (problem names such as Find Above-Average Earners; labels from the platform, not candidate reports); product-company data scientist screens
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 What happens when a scalar subquery returns more than one row, or none? products(product_id, name, category, price): write WHERE price = (SELECT price FROM products WHERE category = 'Books') where Books has several rows, and a variant where the category has no rows. State the behaviour per engine (SQLite uses the first row silently, PostgreSQL and MySQL raise an error, hedged as not executed), what zero rows gives (NULL, so no rows match), and the safe rewrites (MAX or MIN, IN, LIMIT 1 with ORDER BY, or a join).
**Asked at:** vendor documentation (SQLite, PostgreSQL, MySQL) on subquery expressions, WITH and subquery restrictions, not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 The NOT IN NULL trap: customers(customer_id, name) and orders(order_id, customer_id, amount), where one order row has customer_id NULL. List customers who have never ordered using NOT IN (SELECT customer_id FROM orders). Show that it returns no rows, explain three-valued logic (x NOT IN (1, NULL) is never true), give the three fixes (filter IS NOT NULL inside the subquery, NOT EXISTS, LEFT JOIN ... IS NULL), and the pandas ~isin version, noting isin does not have this trap.
**Asked at:** datadriven.io subquery interview patterns and a LetsDataScience CTE-vs-subquery guide, not candidate reports; analyst and data scientist screens
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟢 EXISTS versus IN: customers(customer_id, name) and orders(order_id, customer_id, amount). List customers who have at least one order over 100 with EXISTS and with IN, explain why EXISTS ignores the select list (SELECT 1 versus SELECT *), why EXISTS never returns NULL, why duplicates in the subquery do not duplicate outer rows, how the two forms differ when the subquery column contains NULL, and give the pandas isin or merge version.
**Asked at:** GeeksforGeeks SQL interview questions (subquery, correlated subquery, EXISTS vs IN, CTE entries), not candidate reports; analyst screens at IT services, GCCs and startups
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟢 Correlated subquery, the classic: employees(emp_id, name, dept_id, salary). List employees who earn more than the average salary of their own department. Write it as a correlated subquery, explain in words what 'executed once per outer row' means and what the correlation predicate is, then write the equivalent join to a derived table of department averages, and the pandas transform('mean') mask. Note that the window-function version belongs to Part 4.
**Asked at:** StrataScratch 'Understanding Subqueries' lesson (problem names such as Find Above-Average Earners; labels from the platform, not candidate reports); product-company data scientist screens
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟢 Derived tables (subquery in FROM) and the aliasing rule: orders(order_id, customer_id, amount). Find the average of per-customer total spend, which needs an aggregate of an aggregate. Write it as a derived table, say why you cannot nest AVG(SUM(amount)) in plain SQL, state the alias rule (PostgreSQL and MySQL require an alias on a derived table; test whether SQLite does), and give pandas groupby then mean.
**Asked at:** datadriven.io subquery interview patterns and a LetsDataScience CTE-vs-subquery guide, not candidate reports; analyst and data scientist screens
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟢 CTE basics: write WITH syntax with a name, an optional column list and a body, and convert this derived-table query into a CTE: SELECT city, AVG(t.total) FROM (SELECT c.city, o.customer_id, SUM(o.amount) AS total FROM orders o JOIN customers c ON c.customer_id = o.customer_id GROUP BY c.city, o.customer_id) t GROUP BY city, using customers(customer_id, name, city) and orders(order_id, customer_id, amount). Explain scope (the CTE exists only for that statement), naming advice, and that a CTE is not a persisted table or view. Give the pandas equivalent.
**Asked at:** GeeksforGeeks SQL interview questions (subquery, correlated subquery, EXISTS vs IN, CTE entries), not candidate reports; analyst screens at IT services, GCCs and startups
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 Customers whose total spend is above the average customer total: orders(order_id, customer_id, amount) and customers(customer_id, name). Write it as a CTE of per-customer totals plus a scalar subquery on that CTE, and as a derived table. Explain the difference between the average of order amounts and the average of customer totals (a common wrong answer), what happens to customers with no orders, and give pandas groupby plus a boolean mask.
**Asked at:** StrataScratch 'Understanding Subqueries' lesson (problem names such as Find Above-Average Earners; labels from the platform, not candidate reports); product-company data scientist screens
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 Percent of total with a scalar subquery (no window functions): sales(sale_id, region, amount). Report each region's total, its share of the grand total as a percentage rounded to 1 decimal, ordered by share. Show the scalar subquery in the SELECT list, the integer-division trap (use 100.0 or CAST), the cross-join-to-a-one-row-CTE alternative, what happens if the grand total is NULL or zero (NULLIF), and the pandas version (sum then divide).
**Asked at:** datadriven.io subquery interview patterns and a LetsDataScience CTE-vs-subquery guide, not candidate reports; analyst and data scientist screens
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 Latest order per customer with a correlated subquery: orders(order_id, customer_id, order_date, amount). Return each customer's most recent order row (all columns) using WHERE order_date = (SELECT MAX(order_date) FROM orders WHERE customer_id = o.customer_id). Explain what happens when a customer has two orders on the latest date (both returned), how to break ties by order_id, and give the pandas versions (sort and drop_duplicates, or idxmax) with the tie behaviour stated.
**Asked at:** datadriven.io subquery interview patterns and a LetsDataScience CTE-vs-subquery guide, not candidate reports; analyst and data scientist screens
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 Refactor a messy nested query into CTEs. Given customers(customer_id, name, city), orders(order_id, customer_id, order_date, amount) and this three-level query: SELECT name FROM customers WHERE customer_id IN (SELECT customer_id FROM (SELECT customer_id, SUM(amount) AS total FROM orders WHERE order_date >= '2025-01-01' GROUP BY customer_id) WHERE total > (SELECT AVG(total) FROM (SELECT SUM(amount) AS total FROM orders WHERE order_date >= '2025-01-01' GROUP BY customer_id))). Rewrite it with two chained, well-named CTEs, show the results are identical, and explain what the CTE version buys (named steps, the filtered per-customer totals computed once in the text, easier debugging by selecting from each CTE).
**Asked at:** datadriven.io subquery interview patterns and a LetsDataScience CTE-vs-subquery guide, not candidate reports; analyst and data scientist screens
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 Subquery in HAVING: employees(emp_id, name, dept_id, salary) and departments(dept_id, dept_name). List departments whose average salary is higher than the company-wide average salary. Write it with a scalar subquery in HAVING, explain why the subquery is evaluated once, why WHERE cannot hold an aggregate, and the equivalent with a CTE. Give the pandas groupby mean then mask version and state how a department with all-NULL salaries behaves.
**Asked at:** GeeksforGeeks SQL interview questions (subquery, correlated subquery, EXISTS vs IN, CTE entries), not candidate reports; analyst screens at IT services, GCCs and startups
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 Both an EXISTS and a NOT EXISTS in one query: users(user_id, name) and orders(order_id, user_id, status), where status is 'paid' or 'returned'. List users who have at least one paid order and no returned order. Write it with EXISTS plus NOT EXISTS, and a GROUP BY ... HAVING version using conditional SUM, state which is more readable, and give the pandas version (isin on two key sets).
**Asked at:** StrataScratch 'Understanding Subqueries' lesson (problem names such as Find Above-Average Earners; labels from the platform, not candidate reports); product-company data scientist screens
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🔴 Customers who bought every product (the Customers Who Bought All Products idea): products(product_id, name) and orders(order_id, customer_id, product_id), where a customer may buy the same product several times and product_id is never NULL. List customers who bought every product. Use GROUP BY customer_id HAVING COUNT(DISTINCT product_id) = (SELECT COUNT(*) FROM products), explain why DISTINCT is essential, what breaks if orders contains a product_id not in products, and give pandas (groupby nunique compared with the product count).
**Asked at:** public LeetCode-style problem bank (Customers Who Bought All Products, Nth Highest Salary, Department Highest Salary; known only from list snippets), not a candidate report; analyst and data scientist screens
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🔴 Nth highest salary without window functions (the window version is Part 4): employees(emp_id, name, salary) with duplicate salaries and possibly fewer than N distinct values. Write the 2nd and generic Nth highest distinct salary with SELECT DISTINCT salary ... ORDER BY salary DESC LIMIT 1 OFFSET n-1 wrapped so it returns NULL when absent, and with a correlated COUNT(DISTINCT) version. Explain why DISTINCT matters with ties, how to return NULL (scalar subquery around the LIMIT), and the pandas drop_duplicates, nlargest or unique approach. Note that the ranking-function version is covered in Part 4.
**Asked at:** public LeetCode-style problem bank (Customers Who Bought All Products, Nth Highest Salary, Department Highest Salary; known only from list snippets), not a candidate report; analyst and data scientist screens
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐⭐ 🔴 Debug a wrong total caused by a join fan-out inside a CTE: orders(order_id, customer_id, order_total) and order_items(item_id, order_id, product_id, qty). A report has WITH j AS (SELECT o.order_id, o.customer_id, o.order_total, i.item_id FROM orders o JOIN order_items i ON i.order_id = o.order_id) SELECT customer_id, SUM(order_total) FROM j GROUP BY customer_id and shows inflated revenue. Diagnose it by selecting from the CTE and comparing COUNT(*) with COUNT(DISTINCT order_id), then fix it two ways (aggregate items to one row per order in the CTE first, or sum from orders alone). Explain why the CTE hid the problem and how to test each CTE separately, and show the same bug and fix in pandas.
**Asked at:** datadriven.io subquery interview patterns and a LetsDataScience CTE-vs-subquery guide, not candidate reports; analyst and data scientist screens
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟢 Subquery versus CTE versus view versus temporary table: for the same per-customer totals over orders(order_id, customer_id, amount), show each form in SQLite (subquery, CTE, CREATE VIEW, CREATE TEMP TABLE). Compare lifetime, reuse across statements, whether data is stored, indexability, and who sees the result. Explain that whether a CTE is materialised or inlined is engine specific (SQLite and PostgreSQL have MATERIALIZED and NOT MATERIALIZED hints; hedge MySQL and others, not executed) and that readability is the main reason to choose a CTE.
**Asked at:** vendor documentation (SQLite, PostgreSQL, MySQL) on subquery expressions, WITH and subquery restrictions, not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟢 pandas boolean masks, transform and assign for subquery logic: employees(emp_id, name, dept_id, salary). Reproduce 'earn above the department average' and 'earn above the company average' with a boolean mask, groupby transform('mean') and assign, and with query() using a @variable. Explain why transform returns a result aligned to the original rows (unlike agg), the cost of a lambda versus the built-in 'mean', and that rows with a NaN dept_id get NaN from transform (dropna=True default).
**Asked at:** pandas user guide (groupby transform, dropna) and Comparison with SQL, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟢 CTE chains versus pandas pipelines: translate a three-CTE SQL query (filtered orders, per-customer totals, customers above the overall average of those totals) over orders(order_id, customer_id, order_date, amount) into pandas using named intermediate DataFrames, then into one .pipe() / assign() chain. Explain the mapping of each CTE to a variable or pipe step, the benefit of debugging a single intermediate, and the copy-on-write behaviour of pandas 3 that makes intermediate frames safe to modify.
**Asked at:** pandas user guide (groupby transform, dropna) and Comparison with SQL, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟢 INSERT ... SELECT: tables orders(order_id, customer_id, order_date, amount) and orders_archive with the same columns. Archive orders older than 2024-01-01 with INSERT INTO orders_archive (column list) SELECT ..., then delete them in a way that cannot lose rows. Explain why you name the columns, what happens if the archive already holds some ids (primary-key conflict) and how to skip them with NOT EXISTS, and the pandas parallel (concat of a filtered frame). Note the transaction and the dialect points (hedged, not executed).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 Translating IN and NOT IN subqueries to pandas: customers(customer_id, name, city) and orders(order_id, customer_id, amount) with some NaN customer_id in orders. Write 'customers with total spend over 500' using an aggregated frame, then isin on its index, then map of the aggregated Series onto customers, then a merge. Show what isin does with NaN (NaN matches NaN) versus SQL IN, and why ~isin has no NOT IN trap. State which form keeps customers without orders.
**Asked at:** pandas user guide (groupby transform, dropna) and Comparison with SQL, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 ANY, SOME and ALL when the engine lacks them (SQLite has none; PostgreSQL and MySQL do): products(product_id, name, category, price). Write 'price greater than ALL prices in Books' and 'price greater than ANY price in Books' as the native syntax (hedged text, not executed) and as the runnable equivalents (> MAX(...), > MIN(...), or NOT EXISTS / EXISTS). Explain what each does when the Books subquery is empty and when it contains NULL prices, and that = ANY is IN and <> ALL is NOT IN.
**Asked at:** vendor documentation (SQLite, PostgreSQL, MySQL) on subquery expressions, WITH and subquery restrictions, not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 Subquery versus JOIN: do they always return the same rows? customers(customer_id, name) and orders(order_id, customer_id, amount) with several orders per customer and a NULL customer_id order. Compare SELECT name FROM customers WHERE customer_id IN (SELECT customer_id FROM orders) with the same via JOIN, and NOT IN versus LEFT JOIN ... IS NULL. Show where counts differ (duplicates from the JOIN, the NULL in NOT IN), say when you need DISTINCT, and when a subquery is clearer than a join because you only need a yes or no.
**Asked at:** datadriven.io subquery interview patterns and a LetsDataScience CTE-vs-subquery guide, not candidate reports; analyst and data scientist screens
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 UPDATE with a subquery: customers(customer_id, name, total_spent) and orders(order_id, customer_id, amount). Set total_spent to each customer's order total, with 0 for customers with no orders, using a correlated scalar subquery with COALESCE. Explain what happens without COALESCE (NULL), that SQLite supports this, and the dialect points as hedged text: UPDATE ... FROM in PostgreSQL and SQLite 3.33+, join-update syntax in MySQL, and MySQL error 1093 when the subquery reads the table being updated. Show a before and after check and the pandas map or merge equivalent.
**Asked at:** vendor documentation (SQLite, PostgreSQL, MySQL) on subquery expressions, WITH and subquery restrictions, not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 DELETE with a subquery: employees(emp_id, name, email) has duplicate rows for the same email. Delete the duplicates keeping the row with the smallest emp_id using DELETE FROM employees WHERE emp_id NOT IN (SELECT MIN(emp_id) FROM employees GROUP BY email), and a NOT EXISTS / correlated version. Explain the NULL-email risk, the NOT IN with NULL id risk, that SQLite allows a subquery on the same table while MySQL raises error 1093 (hedged; workaround is a derived table), and the pandas drop_duplicates(keep='first').
**Asked at:** vendor documentation (SQLite, PostgreSQL, MySQL) on subquery expressions, WITH and subquery restrictions, not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 The max-per-group tie problem: employees(emp_id, name, dept_id, salary). Return the highest-paid employee in each department, and all of them when there is a tie. Solve it by joining to a derived table of MAX(salary) per department, and with a correlated subquery, and show that a LIMIT 1 per group or a GROUP BY with a bare column gives one arbitrary row. Explain the tie behaviour, the pandas transform('max') mask versus idxmax, and the pointer to the window version in Part 4.
**Asked at:** public LeetCode-style problem bank (Customers Who Bought All Products, Nth Highest Salary, Department Highest Salary; known only from list snippets), not a candidate report; analyst and data scientist screens
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 Top-N per group via a correlated subquery, no window functions: employees(emp_id, name, dept_id, salary). Return the top 2 earners in each department using WHERE (SELECT COUNT(*) FROM employees e2 WHERE e2.dept_id = e.dept_id AND e2.salary > e.salary) < 2. Explain why strict > makes ties share a rank (so more than 2 rows can return), how to break ties with emp_id, the cost (one count per outer row, quadratic per group), why LIMIT inside a per-group subquery is not portable (hedged: MySQL error 1235 for LIMIT in IN), and the pandas groupby head or nlargest. Point to Part 4 for ROW_NUMBER.
**Asked at:** datadriven.io subquery interview patterns and a LetsDataScience CTE-vs-subquery guide, not candidate reports; analyst and data scientist screens
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 Subqueries with LIMIT: customers(customer_id, name) and orders(order_id, customer_id, amount). Show the orders of the top 3 customers by total spend. Write WHERE customer_id IN (SELECT customer_id FROM orders GROUP BY customer_id ORDER BY SUM(amount) DESC LIMIT 3), explain that SQLite accepts it, that MySQL rejects LIMIT inside IN, ALL, ANY or SOME subqueries with error 1235 (hedged, not executed) and that a derived-table join is the portable workaround. Cover the tie at rank 3 and ORDER BY determinism, and give pandas nlargest then isin.
**Asked at:** vendor documentation (SQLite, PostgreSQL, MySQL) on subquery expressions, WITH and subquery restrictions, not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 CTE scaffolding for a cohort-style question (scaffolding only; retention logic is Part 6): orders(order_id, customer_id, order_date, amount) with ISO date strings. Using chained CTEs, compute each customer's first order date, label every order as 'first' or 'repeat', and count new versus repeat customers per month (strftime). Explain why each CTE has one purpose and one grain, how to check grain with COUNT(*) versus COUNT(DISTINCT customer_id), and give the pandas groupby/transform('min') version.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 CTE scaffolding for a funnel-style question (scaffolding only; funnel metrics are Part 8): events(user_id, event_name, event_time) with names 'view', 'cart', 'purchase'. With one CTE per step (users who viewed, users who carted, users who purchased) and joins, count users at each step and the step-to-step conversion. Explain why a CTE of DISTINCT users per step avoids double counting, that step order is ignored by this simple version, and give pandas sets or isin. Note that ordering within a session is a later part.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
<!-- ANSWER_PENDING -->

### Q31 ⭐ 🟡 Correlated subqueries in the SELECT list: orders(order_id, customer_id, order_date, amount). For every order, show the customer's number of orders, the customer's average order amount and how far this order is from that average, each as a correlated scalar subquery. Explain the per-row evaluation, rewrite it as one join to a derived table of per-customer count and average, confirm the results match, and give pandas groupby transform('count') and transform('mean').
**Asked at:** datadriven.io subquery interview patterns and a LetsDataScience CTE-vs-subquery guide, not candidate reports; analyst and data scientist screens
<!-- ANSWER_PENDING -->

### Q32 ⭐ 🟡 Reusing one CTE twice in a query: sales(sale_id, region, amount). Define regional totals once in a CTE, then return regions whose total is above the average of regional totals and also show the best region's total, referencing the CTE several times. Explain that a derived table cannot be named and reused (MySQL's CTE page says a derived table is derived again for each reference), how engines may inline or materialise a multiply-referenced CTE (hedged: PostgreSQL materialises by default when referenced more than once, SQLite chooses itself), and the pandas intermediate variable.
**Asked at:** vendor documentation (SQLite, PostgreSQL, MySQL) on subquery expressions, WITH and subquery restrictions, not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
<!-- ANSWER_PENDING -->

### Q33 ⭐ 🟡 NaN and NULL pitfalls on the pandas side of subquery logic: a frame with NaN salaries and NaN department keys. Show that df[df.salary > df.salary.mean()] drops NaN rows, that == np.nan is never true, that isin treats NaN as a value, that groupby(...).transform('mean') gives NaN for NaN group keys unless dropna=False, that sum of an all-NaN group is 0 unless min_count=1, and the SQL counterparts (NULL comparisons, IN, GROUP BY puts NULLs in one group). Ask what a candidate should state about NULL handling before answering any subquery question.
**Asked at:** pandas user guide (groupby transform, dropna) and Comparison with SQL, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
<!-- ANSWER_PENDING -->

### Q34 ⭐ 🟡 Empty results inside subqueries: products(product_id, name, category, price). Show what happens with price > (SELECT MAX(price) FROM products WHERE category = 'Toys') when there are no Toys (MAX of nothing is NULL, so no rows), IN and NOT IN over an empty subquery, EXISTS over an empty set, and COUNT versus MAX on an empty set (0 versus NULL). Explain how COALESCE changes the intent and when you would want a row to come back even though the subquery is empty. Give the pandas parallel (empty Series max is NaN).
**Asked at:** vendor documentation (SQLite, PostgreSQL, MySQL) on subquery expressions, WITH and subquery restrictions, not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
<!-- ANSWER_PENDING -->

### Q35 ⭐ 🔴 Relational division with double NOT EXISTS: products(product_id, name, category) and orders(order_id, customer_id, product_id). List customers who bought every product in category 'Books'. Write the double NOT EXISTS form ('there is no Books product for which there is no order by this customer'), compare it with GROUP BY HAVING COUNT(DISTINCT), and explain the vacuous-truth problem when the category has no products (every customer qualifies), duplicate order rows, and which form handles customers with no orders. Give pandas (set comparison via groupby and issubset).
**Asked at:** public LeetCode-style problem bank (Customers Who Bought All Products, Nth Highest Salary, Department Highest Salary; known only from list snippets), not a candidate report; analyst and data scientist screens
<!-- ANSWER_PENDING -->

### Q36 ⭐ 🔴 Second-highest salary per department without window functions: employees(emp_id, name, dept_id, salary). For each department return the second-highest distinct salary (or NULL if the department has only one distinct salary) using a correlated subquery or a derived table of MAX excluding the top. Explain how ties at the top are handled, why a department with one employee yields NULL and how to keep it in the output, the cost, and the pandas groupby with nlargest or unique. Note that DENSE_RANK in Part 4 is the normal answer.
**Asked at:** datadriven.io subquery interview patterns and a LetsDataScience CTE-vs-subquery guide, not candidate reports; analyst and data scientist screens
<!-- ANSWER_PENDING -->

### Q37 ⭐ 🔴 Median without window functions: employees(emp_id, name, salary) with an even or odd row count and NULL salaries. Compute the median salary using a scalar subquery for COUNT and ORDER BY salary LIMIT 2 - (n % 2) OFFSET (n - 1) / 2 wrapped in AVG. Explain why NULLs must be filtered in both the count and the sorted set, how even and odd counts are handled, that engines with PERCENTILE_CONT make this simpler (hedged, not executed), and show pandas median with its NaN skipping.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
<!-- ANSWER_PENDING -->

### Q38 ⭐ 🔴 Orders larger than the customer's earlier average: orders(order_id, customer_id, order_date, amount) with ISO dates. List orders whose amount is greater than the average of the same customer's earlier orders, using a correlated subquery with a date comparison. Explain what happens for a customer's first order (average over an empty set is NULL, so excluded), same-date orders (use order_id as a tie-break), the per-row cost, and a pandas version with groupby and expanding mean shifted by one (note the cumulative-window version is Part 5).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
<!-- ANSWER_PENDING -->

### Q39 ⭐ 🔴 Correlated subquery performance, concept and equivalence: a correlated COUNT subquery runs once per outer row, so n outer rows and m inner rows may cost about n times m without an index. Using orders(order_id, customer_id, amount) and customers(customer_id, name), write the customers with more than 3 orders as a correlated subquery in WHERE, as IN with GROUP BY HAVING, and as a join to a derived table, confirm the three give identical results on small data, and state how an index on orders(customer_id) and the optimiser's decorrelation change things (hedged by engine, not executed). Say EXPLAIN-level work belongs to Part 11.
**Asked at:** datadriven.io subquery interview patterns and a LetsDataScience CTE-vs-subquery guide, not candidate reports; analyst and data scientist screens
<!-- ANSWER_PENDING -->

### Q40 ⭐ 🔴 Dialect map for subqueries and CTEs (hedge everything not run on SQLite 3.45): scalar subquery returning many rows (first row in SQLite, error in PostgreSQL and MySQL), alias required on a derived table, ANY/SOME/ALL support, LIMIT inside IN subqueries (MySQL error 1235), UPDATE/DELETE reading the same table (MySQL error 1093), WITH before UPDATE, DELETE and INSERT, MATERIALIZED and NOT MATERIALIZED hints (SQLite 3.35+, PostgreSQL 12+), a derived table referenced once versus a CTE referenced many times, and LATERAL (not covered here). Present a table with a 'verified by running on SQLite' column and a 'hedged, not executed' column.
**Asked at:** vendor documentation (SQLite, PostgreSQL, MySQL) on subquery expressions, WITH and subquery restrictions, not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
<!-- ANSWER_PENDING -->
