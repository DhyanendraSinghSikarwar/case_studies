T = {}
T[4] = """**Say this first (1 line):** GMV is the gross value of orders placed in the month, net revenue is what stays after cancellations and returns, AOV is value per order, ARPU divides revenue by all users in scope and ARPPU by paying users only; I state each definition and denominator first and guard every division with `NULLIF`.

**Definitions and assumptions (stated before the query):** month is 2024-03, UTC dates, test users excluded everywhere. GMV = completed plus returned orders placed in the month (cancelled orders never became a sale, so they are out; some teams include returned orders in GMV and take them out in net revenue, which is exactly what this definition does). Net revenue = completed orders only. AOV = GMV over the number of orders in GMV. ARPU = net revenue over registered non-test users at month end (signup before the next month). I also show the "active" denominator (users who placed any order in the month, cancelled ones included, because this schema has no events table). ARPPU = net revenue over users with at least one completed order in the month. These are my assumptions; the interviewer may have others, and the point is to say them.

**Schema and sample data:** seven users (user 6 is a test user, user 5 signs up in April, user 7 never orders). Nine orders: a test order of 999, a February order of 300 and an April order of 70 must stay out of March; order 6 is at 2024-03-31 23:30, inside the month.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO users VALUES
 (1,'2024-01-05','IN',0),(2,'2024-02-10','IN',0),(3,'2024-03-05','IN',0),(4,'2024-03-20','US',0),
 (5,'2024-04-02','IN',0),(6,'2024-01-15','IN',1),(7,'2024-02-01','IN',0);
INSERT INTO orders VALUES
 (1,1,'2024-03-03 10:00:00',100,'completed'),
 (2,1,'2024-03-10 10:00:00',50,'completed'),
 (3,2,'2024-03-12 10:00:00',200,'returned'),
 (4,3,'2024-03-15 10:00:00',80,'completed'),
 (5,3,'2024-03-16 10:00:00',60,'cancelled'),
 (6,4,'2024-03-31 23:30:00',40,'completed'),
 (7,6,'2024-03-05 10:00:00',999,'completed'),
 (8,2,'2024-02-28 10:00:00',300,'completed'),
 (9,5,'2024-04-03 10:00:00',70,'completed');
```

**SQL answer:** `SQL_MAIN` in the Code block, parameterised by the month start. Each measure comes from its own aggregate at order grain, and the registered count comes from a separate CTE so the user count is not multiplied by orders.
```sql
{SQL:SQL_MAIN}
```

**pandas answer:** shown once, identical to the Code block (a function of the month start; `ratio` returns NaN for an empty denominator):
```py
{PD}
```

**Example:** March, non-test.
- Orders in March: 1 (100 completed), 2 (50 completed), 3 (200 returned), 4 (80 completed), 5 (60 cancelled), 6 (40 completed).
- GMV = 100 + 50 + 200 + 80 + 40 = 470 over 5 orders, so AOV = 94.0.
- Net revenue = 100 + 50 + 80 + 40 = 270.
- Registered at month end: users 1, 2, 3, 4, 7 = 5 (user 5 signs up in April, user 6 is test). ARPU = 270/5 = 54.0.
- Active users (any order in March): 1, 2, 3, 4 = 4, so revenue per active user = 67.5. Paying users: 1, 3, 4 = 3, so ARPPU = 90.0.
- Status choice moves GMV: all statuses 530, excluding cancelled 470, completed only 270 in my run.
- May has no orders: sums print 0, AOV, ARPU over active and ARPPU are NULL (not a division error), and ARPU over registered users is 0.0 because there are 6 registered users.

**Code:** run with `python3 -I`. Rows are in month order (2024-03, 2024-05); the SQL integer columns are cast to float before the compare because a NULL in a column makes it float.
```python
{CODE}
```

**Output (my run):**
```text
{OUT}
```

**Edge cases:**
- Honest surprise found while testing: my first SQL used `net_revenue / registered`, which gave NULL for the empty month, while pandas gave 0.0. With 6 registered users and no revenue ARPU is 0, not unknown; I wrapped the numerator in `COALESCE(net_revenue, 0)`. ARPU over active users or payers really is undefined (0 divided by 0), so NULL is right there.
- Month boundary: order 6 at 23:30 on 03-31 is inside because the range is half-open `< date(:m_start, '+1 month')`; `BETWEEN '2024-03-01' AND '2024-03-31'` would lose it.
- Returned orders: a return that happens in a later month is a refund in that month (Q10 and Q11 handle the order-month versus cash views).
- The test order of 999 would have multiplied GMV by more than three if it leaked.
- Currency, taxes and shipping: GMV may or may not include them; say which.
- ARPU over registered users shrinks when signups surge (Q39).

**Then explain:**
- GMV measures activity (what was bought), net revenue measures what the business keeps; mixing them in one ratio is the main trap.
- AOV is an order-grain mean, ARPU and ARPPU are user-grain: the denominators differ by grain.
- ARPU over registered users answers "what does an average user bring", over active users "how engaged buyers spend", over payers "how much a payer pays". The same 270 gives 54.0, 67.5 or 90.0 in my run.
- `NULLIF(den, 0)` returns NULL instead of an error in engines that raise one; SQLite returns NULL for division by zero anyway, but PostgreSQL raises an error (hedged: not executed here).
- Dialects (not executed here): PostgreSQL `date_trunc('month', order_ts)`; BigQuery `SAFE_DIVIDE`; MySQL `DATE_FORMAT`.

**Follow-ups:**
- GMV per country? Add `country` to the group (orders joined to users once; users has one row per user, so no fan-out).
- ARPU for a rolling 30 days? Same query, different window; say whether the denominator is as of the window end.
- Net of refunds? See Q10.

**Common mistakes:**
- Averaging order amounts per user and then averaging again (an average of averages).
- Joining orders to users twice or to a many-row table before summing.
- Counting cancelled orders in GMV without saying so.
- Using all users ever (including future signups) as the ARPU denominator.
- Dividing without a zero guard.
"""
T[5] = """**Say this first (1 line):** Take each customer's first order (earliest `order_date`), mark it immediate when the preferred date equals the order date, and take the average of that flag times 100, rounded to 2 decimals; I show the join-to-MIN version and the `ROW_NUMBER` version, and they agree unless a customer has a tie on the earliest date.

**Schema and sample data:** six customers. The problem guarantees one earliest order per customer; I test the same code on clean data, on data with a preferred date earlier than the order date (a data error) and on a customer with two orders on the earliest date (breaking the guarantee). The statement follows the LeetCode 1174 text as I remember it from a mirror I opened; I did not open leetcode.com.
```sql
CREATE TABLE delivery(delivery_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, customer_pref_delivery_date TEXT);
INSERT INTO delivery VALUES
 (1,1,'2024-03-01','2024-03-01'),(2,1,'2024-03-05','2024-03-05'),
 (3,2,'2024-03-02','2024-03-04'),(4,2,'2024-03-10','2024-03-10'),
 (5,3,'2024-03-03','2024-03-03'),
 (6,4,'2024-03-04','2024-03-09'),(7,4,'2024-03-06','2024-03-06'),
 (8,5,'2024-03-07','2024-03-07'),
 (9,6,'2024-03-08','2024-03-12');
```
The extra rows for the other two scenarios are `(10,7,'2024-03-02','2024-03-04'),(11,7,'2024-03-09','2024-03-02')` (dirty) and `(12,8,'2024-03-11','2024-03-11'),(13,8,'2024-03-11','2024-03-15')` (tie); they are added in the Code block.

**SQL answer:** `SQL_JOIN` in the Code block (join each order to its customer's MIN date):
```sql
{SQL:SQL_JOIN}
```
and `SQL_RN` (rank each customer's orders, keep row 1; the tie-breaker is `delivery_id`):
```sql
{SQL:SQL_RN}
```

**pandas answer:** both versions, shown once and identical to the Code block:
```py
{PD}
```

**Example:** clean data, first order per customer.
- Customer 1: first 03-01, preferred 03-01, immediate. Customer 2: first 03-02, preferred 03-04, scheduled. Customer 3: 03-03 and 03-03, immediate. Customer 4: first 03-04, preferred 03-09, scheduled (the later immediate order does not count). Customer 5: immediate. Customer 6: 03-08 and 03-12, scheduled.
- 3 immediate firsts out of 6 customers = 50.0%.
- Over all orders it would be 6 of 9 = 66.67%, which answers a different question.

**Code:** run with `python3 -I`. Each assert compares two scalars per scenario, so there is no row order.
```python
{CODE}
```

**Output (my run):**
```text
{OUT}
```

**Edge cases:**
- Correction to the premise: comparing `MIN(order_date)` with `MIN(customer_pref_delivery_date)` per customer is not wrong on clean data. If every preferred date is on or after its order date, the two minimums are equal exactly when the first order is immediate, and my run gave 50.0 for it, the same as the correct answer. It is wrong when the data breaks that rule: with a preferred date earlier than an order date (customer 7) it gave 57.14 against the correct 42.86. It also asks the wrong question (is any preferred date equal to the first order date), so I avoid it.
- Tie on the earliest date: the join-to-MIN version keeps both rows, so the tied customer counts twice (rows, not customers) and gave 50.0; `ROW_NUMBER` with a tie-breaker keeps one row and gave 57.14. State the rule (first by `delivery_id`, or immediate if any earliest order is immediate) and make the denominator customers.
- `AVG(a = b)` works in SQLite because a comparison is 0 or 1; in PostgreSQL cast the boolean (`(a = b)::int`) (not executed here).
- A customer with no orders does not exist in this table, so no denominator issue; if a customers table exists, decide whether to include them.
- Empty table: `SUM(...) / COUNT(*)` gives NULL in SQLite; `AVG` also gives NULL.

**Then explain:**
- The unit is the customer's first order, so the denominator is customers.
- Join-to-MIN is two scans plus a join; `ROW_NUMBER` is one sort per partition and makes the tie rule explicit.
- `ROUND(..., 2)` in SQLite rounds half away from zero; pandas `round` rounds half to even. No value here is an exact tie.
- Dialects (not executed here): MySQL (the LeetCode default as far as I remember) `ROUND(AVG(order_date = customer_pref_delivery_date) * 100, 2)`; PostgreSQL needs the boolean cast; Snowflake and BigQuery have `QUALIFY` for the row-number filter.

**Follow-ups:**
- Per cohort month? Group the first-order table by the month of `first_date`.
- Why not `DISTINCT ON`? PostgreSQL only (not executed here).
- Ties in a real table? Add a deterministic tie-breaker and report how many ties exist.

**Common mistakes:**
- Averaging over all orders.
- `MIN(order_date) = MIN(pref)` as a general rule (works only under clean data).
- No tie-breaker in `ROW_NUMBER`, so the pick changes between runs.
- Integer division when writing `SUM(...) / COUNT(*)` without `100.0`.
"""
T[6] = """**Say this first (1 line):** For each contest, count the distinct registered users and divide by the number of users in the Users table (not by rows in register), multiply by `100.0` to avoid integer division, round to 2 decimals, and order by percentage descending then contest id ascending.

**Schema and sample data:** eight users. Contest 100 has a duplicate register row for user 1. Contest 400 ties contest 100 at 50%. A `contests` table includes contest 500, which nobody joined. The statement follows LeetCode 1633 as I remember it from search snippets and a mirror; I did not open leetcode.com.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, user_name TEXT);
CREATE TABLE register(contest_id INTEGER, user_id INTEGER);
CREATE TABLE contests(contest_id INTEGER PRIMARY KEY);
INSERT INTO users VALUES (1,'A'),(2,'B'),(3,'C'),(4,'D'),(5,'E'),(6,'F'),(7,'G'),(8,'H');
INSERT INTO register VALUES
 (100,1),(100,2),(100,3),(100,4),(100,1),
 (200,2),(200,3),
 (300,5),(300,6),(300,7),
 (400,1),(400,2),(400,3),(400,4);
INSERT INTO contests VALUES (100),(200),(300),(400),(500);
```

**SQL answer:** `SQL_MAIN` in the Code block:
```sql
{SQL:SQL_MAIN}
```
Variants in the Code block: `SQL_COUNT_ROWS` (counts rows), `SQL_WRONG_DENOM` (divides by register rows), `SQL_INT_DIV` (integer arithmetic) and `SQL_WITH_CONTESTS` (starts from a contests table).

**pandas answer:** shown once, identical to the Code block:
```py
{PD}
```

**Example:** 8 users.
- Contest 100: distinct users 1, 2, 3, 4 = 4, so 50.0% (5 rows because of the duplicate, which would give 62.5%).
- Contest 400: 4 users, 50.0%. Tie with 100, so contest id decides: 100 first.
- Contest 300: 3 users = 37.5%. Contest 200: 2 users = 25.0%.
- Order: 100, 400, 300, 200.

**Code:** run with `python3 -I`. The assert compares frames after both are ordered by `percentage` descending, `contest_id` ascending.
```python
{CODE}
```

**Output (my run):**
```text
{OUT}
```

**Edge cases:**
- Duplicate register row: `COUNT(*)` gave 62.5 for contest 100 in my run; `COUNT(DISTINCT user_id)` gave 50.0.
- Wrong denominator: dividing by the 14 register rows gave 28.57, 28.57, 21.43, 14.29. The question is "of all users", so the denominator is `users`.
- Integer division: `COUNT(DISTINCT user_id) * 100 / (SELECT COUNT(*) FROM users)` returned 50, 50, 37, 25 in my run; the 37.5 was truncated to 37. In SQLite `3/2` is 1 and `3/2.0` is 1.5. `100.0 *` fixes it.
- A contest nobody joined is absent from `register`, so it is absent from the result. With a contests table, `LEFT JOIN` and `COUNT(DISTINCT r.user_id)` give 0.0 for contest 500 in my run.
- A register row for a user not in `users` (the problem guarantees this does not happen) would count toward the numerator and could push the percentage above 100; I did not run that case.
- Rounding: SQLite `ROUND` rounds half away from zero and pandas `round` half to even. In my run `ROUND(6.25, 1)` gave 6.3 while `Series.round(1)` gave 6.2. No value in this table is a tie at 2 decimals, so the assert holds, but a tie would differ.
- Empty `users`: the divisor is 0 and SQLite returns NULL.

**Then explain:**
- The question is a share of the whole user base, so the base is a scalar subquery; Part 3 covers scalar subqueries.
- Distinct protects against duplicate registrations; if the table has a primary key `(contest_id, user_id)` it is a no-op but harmless.
- Order is part of the contract: percentage descending, ties by contest id ascending.
- Dialects (not executed here): in PostgreSQL integer division also truncates, so keep `100.0`; MySQL divides to a decimal with `/`.

**Follow-ups:**
- Include contests with zero registrations? Start from a contests table (shown).
- Round to a string with two decimals? Format at the edge; `ROUND` returns a float.
- Percent of users who registered for at least one contest? A single `COUNT(DISTINCT user_id)` over register divided by users.

**Common mistakes:**
- Dividing by register rows.
- `COUNT(*)` with duplicate rows.
- Integer division (50, 37, 25 instead of 50.0, 37.5, 25.0).
- Ordering only by percentage and leaving ties in undefined order.
"""
T[7] = """**Say this first (1 line):** Build one row per user with `MIN(CASE WHEN event_name = ... THEN event_ts END)` for each step, count a user in a step only when its first timestamp is strictly after the previous step's, and note that "first of each" can reject a user whose first cart came before a later valid view, cart, purchase sequence, so a chained version looks for the first cart after the first view and the first purchase after that cart.

**Schema and sample data:** eight users. User 2 purchased before viewing. User 3 carted twice. User 4 carted at 08:00 before their first view at 09:00, then viewed, carted again and purchased (a valid sequence hidden behind an early cart). User 5 skipped the cart. User 8 viewed and carted at the same second.
```sql
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view'),(1,'2024-03-01 10:05:00','cart'),(1,'2024-03-01 10:10:00','purchase'),
 (2,'2024-03-01 09:00:00','purchase'),(2,'2024-03-01 09:30:00','view'),(2,'2024-03-01 09:40:00','cart'),
 (3,'2024-03-01 10:00:00','view'),(3,'2024-03-01 10:05:00','cart'),(3,'2024-03-01 10:07:00','cart'),(3,'2024-03-01 10:20:00','purchase'),
 (4,'2024-03-01 08:00:00','cart'),(4,'2024-03-01 09:00:00','view'),(4,'2024-03-01 09:10:00','cart'),(4,'2024-03-01 09:30:00','purchase'),
 (5,'2024-03-01 11:00:00','view'),(5,'2024-03-01 11:05:00','purchase'),
 (6,'2024-03-01 12:00:00','view'),(6,'2024-03-01 12:05:00','cart'),
 (7,'2024-03-01 13:00:00','view'),(7,'2024-03-01 13:01:00','view'),
 (8,'2024-03-01 12:00:00','view'),(8,'2024-03-01 12:00:00','cart'),(8,'2024-03-01 12:10:00','purchase');
```

**SQL answer:** `SQL_FIRST` in the Code block (the per-user first-timestamp table, then strict comparisons; a NULL timestamp makes the comparison NULL, so a missing step is not counted):
```sql
{SQL:SQL_FIRST}
```
The any-order counts are `SQL_ANY` and the chained version is `SQL_CHAIN` in the Code block:
```sql
{SQL:SQL_CHAIN}
```
`SQL_PER_USER` prints the first timestamps per user.

**pandas answer:** shown once, identical to the Code block (groupby/unstack for the first-timestamp table, then a merge-per-step chain):
```py
{PD}
```

**Example:** first timestamps per user (time of day):
- User 1: 10:00, 10:05, 10:10, in order. User 2: view 09:30, cart 09:40, purchase 09:00, so purchase before view: rejected at step 3. User 3: in order despite the second cart. User 4: view 09:00, first cart 08:00, purchase 09:30: first-of-each rejects (cart not after view). User 5: no cart. User 6: view and cart only. User 7: view only. User 8: view and cart at 12:00:00, equal, so `<` rejects.
- Any order: 8 viewed, 6 carted (1, 2, 3, 4, 6, 8), 6 purchased (1, 2, 3, 4, 5, 8).
- Strict first-of-each: 8, 4 (users 1, 2, 3, 6; user 4 and 8 fail), 2 (users 1 and 3).
- Chained after the first view: 8, 5 (user 4 now qualifies through the 09:10 cart; user 8 still fails on the tie), 3 (users 1, 3 and 4). User 2 still fails because the purchase at 09:00 is before the cart at 09:40.
- So the same table gives 6, 2 or 3 purchasers depending on the definition.

**Code:** run with `python3 -I`. The assert compares the three rows (any-order, strict, chained) in that order.
```python
{CODE}
```

**Output (my run):**
```text
{OUT}
```

**Edge cases:**
- Strict `<` versus `<=`: user 8's equal timestamps fail under `<`. With one-second timestamps ties are common in batched events; state the rule, and add an event id tie-breaker if the ordering of simultaneous events is known.
- Why "first of each" can be wrong: user 4's first cart (08:00) came before the first view, so the strict test fails, yet view 09:00, cart 09:10, purchase 09:30 is a valid sequence. It matters when carts can happen without a view in the same visit (saved carts, deep links, an app re-open); it does not matter if the product enforces the order.
- Greedy chaining is exact for "does a valid sequence exist": starting from the earliest view, then the earliest later cart, then the earliest later purchase can only help.
- A purchase before the first view (user 2) is excluded from the strict funnel but still counts in the any-order table; the gap between those two numbers is a data-quality signal.
- Repeated events (user 3's second cart) do not matter because only the first qualifying one is used.
- No time window yet: Q17 adds one.

**Then explain:**
- Conditional `MIN` is a pivot without PIVOT: one row per user, one column per step.
- `COUNT(col)` skips NULL, so users who never did the step fall out automatically.
- Comparisons with NULL are NULL, not false; `COUNT(CASE WHEN ... THEN 1 END)` handles that correctly.
- The three definitions answer different product questions; the interviewer expects you to name which one you computed.
- Dialects (not executed here): PostgreSQL and BigQuery can do the same with `MIN(...) FILTER (WHERE ...)` and `MIN(IF(...))`; some warehouses have a built-in funnel function (for example ClickHouse `windowFunnel`); not executed.

**Follow-ups:**
- Add a 7-day limit between steps? Add `AND e.event_ts <= datetime(v.t1, '+7 days')` (Q17).
- Do I need the first view as the anchor? The latest view before the purchase answers a different, attempt-level question (Q40).
- What about a step that is optional? Skip it from the chain and report it separately (Q35).

**Common mistakes:**
- Comparing first timestamps and thinking it handles every valid sequence.
- `<=` without thinking about same-second events.
- Counting any-order and strict on different populations.
- Using `MIN` of the wrong column (for example `MIN(event_name)`).
"""
