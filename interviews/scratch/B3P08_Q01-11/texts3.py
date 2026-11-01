T = {}
T[8] = """**Say this first (1 line):** Group the events by the channel on the event itself (NULL shown as 'unknown'), count distinct users per step with conditional `COUNT(DISTINCT ...)`, join only to `users` (one row per user) to drop test users, and remember that a user who appears in two channels is counted in both, so the channel rows add up to more than the distinct user total and a channel can even show more than 100% conversion.

**Schema and sample data:** seven real users and one test user (8). User 2 views from `ads` but carts and purchases from `email`. User 3 views and carts from `organic` and purchases from `partner` (a channel with no view). User 4 has NULL channels. User 6 views from two channels. `user_channel` is a deliberately bad helper table in which user 2 appears twice.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT, channel TEXT);
CREATE TABLE user_channel(user_id INTEGER, channel TEXT);
INSERT INTO users VALUES (1,'2024-01-01','IN',0),(2,'2024-01-01','IN',0),(3,'2024-01-01','IN',0),(4,'2024-01-01','IN',0),
 (5,'2024-01-01','IN',0),(6,'2024-01-01','IN',0),(7,'2024-01-01','IN',0),(8,'2024-01-01','IN',1);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view','ads'),(1,'2024-03-01 10:05:00','cart','ads'),(1,'2024-03-01 10:10:00','purchase','ads'),
 (2,'2024-03-01 11:00:00','view','ads'),(2,'2024-03-02 09:00:00','cart','email'),(2,'2024-03-02 09:10:00','purchase','email'),
 (3,'2024-03-01 12:00:00','view','organic'),(3,'2024-03-01 12:05:00','cart','organic'),(3,'2024-03-01 12:30:00','purchase','partner'),
 (4,'2024-03-01 13:00:00','view',NULL),(4,'2024-03-01 13:10:00','purchase',NULL),
 (5,'2024-03-01 14:00:00','view','ads'),
 (6,'2024-03-01 15:00:00','view','organic'),(6,'2024-03-01 15:05:00','view','ads'),(6,'2024-03-01 15:10:00','purchase','organic'),
 (7,'2024-03-01 16:00:00','view','email'),(7,'2024-03-01 16:05:00','cart','email'),(7,'2024-03-01 16:10:00','purchase','email'),
 (8,'2024-03-01 17:00:00','view','ads'),(8,'2024-03-01 17:10:00','purchase','ads');
INSERT INTO user_channel VALUES (1,'ads'),(2,'ads'),(2,'email'),(3,'organic'),(4,'ads'),(5,'ads'),(6,'organic'),(7,'email');
```

**SQL answer:** `SQL_MAIN` in the Code block. `users` has one row per user, so the join cannot repeat events.
```sql
{SQL:SQL_MAIN}
```
`SQL_FIRST_TOUCH` in the Code block applies a defined attribution rule instead: each user gets the channel of their first event, so every user is in exactly one channel. `SQL_WRONG_JOIN` joins events to the repeating `user_channel` table.

**pandas answer:** shown once, identical to the Code block (`fillna('unknown')` before the groupby, because a default groupby drops NaN keys):
```py
{PD}
```

**Example:** non-test users 1 to 7.
- ads: view users 1, 2, 5, 6 = 4; cart user 1 = 1; purchase user 1 = 1; 25.0%.
- organic: view users 3, 6 = 2; cart 3; purchase user 6; 50.0%.
- email: view user 7 = 1; cart users 2 and 7 = 2; purchase users 2 and 7 = 2; 200.0% (two purchasers from one viewer, because user 2's view was in `ads`).
- unknown: view user 4 = 1, purchase user 4: 100.0%. partner: view 0, purchase user 3: NULL conversion (no views).
- Channel rows sum to 8 view users, but only 7 distinct users viewed (user 6 is in two channels); purchases sum to 6, which happens to equal the distinct purchasers here.
- Under the first-touch rule: ads 3 views, 2 purchasers, 66.7%; organic 2, 2, 100.0%; email 1, 1, 100.0%; unknown 1, 1, 100.0%. Views sum to 7, which is the distinct total. Conversion can no longer exceed 100%.

**Code:** run with `python3 -I`. The assert compares the SQL and pandas frames after ordering by `view_users` descending then `channel` ascending (ties email/unknown by name, partner last with 0 views).
```python
{CODE}
```

**Output (my run):**
```text
{OUT}
```

**Edge cases:**
- Channel from the event is a definition, not a truth: it says where each action came from. A conversion above 100% (email 200.0%) is the signal that the steps are attributed to different channels; then a per-user rule (first touch, last touch before the purchase) is the right frame (Q20).
- NULL channel: `GROUP BY channel` keeps a NULL group in SQL; `COALESCE(channel, 'unknown')` names it. In pandas a default `groupby` drops NaN keys: in my run the default groupby on this data listed only ads, email, organic, partner, and `dropna=False` added the NaN group. The `fillna` in the answer is what keeps the unknown row.
- A channel with zero view users gives NULL conversion via `NULLIF`, not an error (partner).
- Joining a table that repeats users: joining events to `user_channel` gave 7 purchase rows for 6 purchase events in my run, because user 2 matched twice. Even `COUNT(DISTINCT user_id)` would hide this while `COUNT(*)` or `SUM(amount)` would not.
- Test users: the test user's view and purchase (both `ads`) would add 1 to ads views and 1 to ads purchases; the join with `is_test = 0` removes both.
- Users with no row in `users` drop out of the inner join.

**Then explain:**
- Take the channel from the event itself, or from one declared rule; do not join a user-to-channel table that can have several rows per user.
- Distinct users per channel are not additive across channels. Report the distinct total separately.
- Show counts next to the percentage; a rate on 1 viewer is noise.
- Dialects (not executed here): BigQuery `COUNT(DISTINCT IF(...))`, PostgreSQL `FILTER`; `COALESCE` is standard everywhere.

**Follow-ups:**
- Channel rows must add up to the total? Use a one-channel-per-user rule (shown).
- Order within the funnel? Combine with Q7.
- Conversion of NULL channel as a data-quality metric? Report the share of events with NULL channel.

**Common mistakes:**
- Joining a many-row channel table and counting rows.
- Dropping the NULL channel (silently in pandas).
- Reporting channel conversion above 100% without explaining it.
- Summing channel rows and calling it the total.
"""
T[9] = """**Say this first (1 line):** A later step can only be larger than an earlier one if the steps are not nested: purchases without a cart event (express checkout or tracking gaps), purchase events counted instead of users, test users in one step only, duplicate purchase events, and different filters per step all do it; the fix is to count distinct non-test users and make each step require the previous one, saying clearly that this checks presence, not time order.

**Causes (at least five):**
1. Purchase without a cart event: express checkout, buy-now button, a tracking gap or an ad blocker that drops the cart event.
2. Counting events instead of users: a retried or double-clicked purchase counts twice.
3. Steps not restricted to users who passed the earlier step: the purchase count includes users who never carted.
4. Duplicate purchase events from client retries or server and client both logging.
5. A different date filter on each step (purchases counted over a longer period than views).
6. Test or internal users filtered from one step only, or present only in the purchase step.
7. Identity changes: the same person counted under an anonymous id at the view and a logged-in id at the purchase (not reproduced here).

**Schema and sample data:** I reproduce three causes: express checkout (users 3 and 10 purchase without a cart), purchase events counted instead of users (user 2 purchases twice, two seconds apart) and a test user (9) who only purchases.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES (1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,1),(10,0);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view'),(1,'2024-03-01 10:05:00','cart'),(1,'2024-03-01 10:10:00','purchase'),
 (2,'2024-03-01 11:00:00','view'),(2,'2024-03-01 11:05:00','cart'),(2,'2024-03-01 11:10:00','purchase'),(2,'2024-03-01 11:10:02','purchase'),
 (3,'2024-03-01 12:00:00','view'),(3,'2024-03-01 12:03:00','purchase'),
 (4,'2024-03-01 13:00:00','view'),(4,'2024-03-01 13:05:00','cart'),
 (5,'2024-03-01 14:00:00','view'),
 (6,'2024-03-01 15:00:00','view'),(6,'2024-03-01 15:05:00','cart'),(6,'2024-03-01 15:10:00','purchase'),
 (7,'2024-03-01 16:00:00','view'),(7,'2024-03-01 16:05:00','cart'),
 (8,'2024-03-01 17:00:00','view'),
 (9,'2024-03-01 18:00:00','purchase'),
 (10,'2024-03-01 19:00:00','view'),(10,'2024-03-01 19:02:00','purchase');
```

**SQL answer:** four queries in the Code block, one per row of the result: `SQL_NAIVE` (distinct users for view and cart but purchase events, test users in), `SQL_USERS` (distinct users everywhere), `SQL_NOTEST` (test users removed) and the corrected cumulative funnel `SQL_CUM`:
```sql
{SQL:SQL_CUM}
```
`SQL_SKIP` lists the purchasers with no cart event.

**pandas answer:** shown once, identical to the Code block (`counts` for the first three rows, a user by step flag table from `crosstab` for the cumulative row):
```py
{PD}
```

**Example:** nine users have a view (1 to 8 and 10), five have a cart (1, 2, 4, 6, 7).
- Naive dashboard: 9 view users, 5 cart users, 7 purchase events (users 1, 2 twice, 3, 6, 9, 10): step 3 is bigger than step 2.
- Distinct users instead of events: 6 purchasers (1, 2, 3, 6, 9, 10): still more than 5 cart users.
- Drop the test user 9: 5 purchasers, no longer greater, but it includes users 3 and 10 who never carted.
- Cumulative (each step needs the previous one): 9 viewed, 5 carted, 3 purchased (users 1, 2, 6). The funnel is now monotone.
- Express-checkout purchasers (3 and 10) are not lost; report them as their own number (2 in my run), because they are real revenue.

**Code:** run with `python3 -I`. The assert compares the four rows in the printed order.
```python
{CODE}
```

**Output (my run):**
```text
{OUT}
```

**Edge cases:**
- The cumulative funnel here needs the previous step's event to exist, but not to be earlier in time. Order is Q7, a cumulative funnel with a step index is Q35. If the product allows express checkout, forcing the cart step makes the funnel understate purchases; the honest answer is to show the main path and the bypass count.
- `MAX(event_name = 'view')` returns 0 or 1 per user, so the multiplication `v * c * p` is an AND.
- Duplicate purchase events are removed in the funnel by counting users; for purchase counts you need event-level dedup (Q38).
- Different date filter per step: not reproduced in the code, but the fix is one shared window applied once in a CTE before the step counts.
- An empty step makes every later cumulative count 0, not an error.

**Then explain:**
- A funnel step is a set of users, and a valid funnel has nested sets. If a later set is larger, the sets are not nested, and the debugging method is to list who is in step N but not in step N-1.
- Fix one cause at a time and print the table after each, so the 7, 6, 5 and 3 above explain the gap fully.
- Tell stakeholders that cumulative means "reached the step", not "did it in order".

**Follow-ups:**
- How do I find the users in step 3 but not step 2? A `NOT EXISTS` or a `HAVING MAX(purchase) = 1 AND MAX(cart) = 0` query (`SQL_SKIP`).
- Should express checkout count as a cart step? Product decision: either log a synthetic cart event or make the funnel start at checkout.
- How do I check tracking gaps? Compare against orders in the database.

**Common mistakes:**
- Counting events, not users.
- Test and internal users removed from only one step.
- Reporting a conversion above 100% without investigating.
- Different date ranges or filters per step.
- Forcing each step to include the previous one and hiding the users who bypass it.
"""
T[10] = """**Say this first (1 line):** An order can have several refund rows, so joining orders to refunds and then summing `orders.amount` counts the order once per refund; I pre-aggregate refunds to one row per order (or use a scalar subquery) before summing, and I state whether refunds are charged to the order month or to the month they were paid.

**Schema and sample data:** six orders and four refunds. Order 1 (completed, 100) has two refunds, one in January and one in February. Order 3 is fully refunded. Order 5 (February) is refunded in March. Order 4 is cancelled and ignored.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
CREATE TABLE refunds(refund_id INTEGER PRIMARY KEY, order_id INTEGER, refund_ts TEXT, amount REAL);
INSERT INTO orders VALUES
 (1,1,'2024-01-10 10:00:00',100,'completed'),
 (2,2,'2024-01-20 10:00:00',200,'completed'),
 (3,3,'2024-02-05 10:00:00',150,'completed'),
 (4,4,'2024-02-14 10:00:00',80,'cancelled'),
 (5,1,'2024-02-20 10:00:00',50,'completed'),
 (6,5,'2024-03-03 10:00:00',120,'completed');
INSERT INTO refunds VALUES
 (1,1,'2024-01-15 10:00:00',30),(2,1,'2024-02-02 10:00:00',20),
 (3,3,'2024-02-10 10:00:00',150),(4,5,'2024-03-01 10:00:00',10);
```

**SQL answer:** the wrong query `SQL_WRONG`, then fix 1 `SQL_PREAGG` and fix 2 `SQL_SCALAR`, and the cash view `SQL_CASH`, all in the Code block. Wrong:
```sql
{SQL:SQL_WRONG}
```
Fix 1, pre-aggregate refunds to the order grain:
```sql
{SQL:SQL_PREAGG}
```
Fix 2, scalar subquery per order (the same result, one correlated lookup per order):
```sql
{SQL:SQL_SCALAR}
```
Cash view, each refund charged to the month it is paid:
```sql
{SQL:SQL_CASH}
```

**pandas answer:** shown once, identical to the Code block (sum refunds per order first, then a left merge):
```py
{PD}
```

**Example:** order-month view.
- January: completed orders 1 (100) and 2 (200), gross 300. Refunds on January orders: 30 + 20 = 50 on order 1. Net = 250.
- February: orders 3 (150) and 5 (50), gross 200. Refunds: 150 (order 3) + 10 (order 5, paid in March) = 160. Net = 40.
- March: order 6 (120), no refunds. Net = 120.
- Wrong query: order 1 has two refund rows, so after the join it appears twice and January gross becomes 100 + 100 + 200 = 400, net 350 instead of 250. February and March are right only because their orders have at most one refund.
- Cash view: January 300 - 30 = 270, February 200 - 170 (20 for order 1 and 150 for order 3) = 30, March 120 - 10 = 110.

**Code:** run with `python3 -I`. Fix 1 and fix 2 are asserted equal, then pandas is asserted equal to fix 1, all ordered by month.
```python
{CODE}
```

**Output (my run):**
```text
{OUT}
```

**Edge cases:**
- `LEFT JOIN` is required, otherwise orders without refunds disappear from the gross (an inner join silently drops order 2 and order 6).
- The same fan-out happens in pandas: merging the raw refund rows into completed orders gave a January gross of 400.0 in my run, the same wrong number.
- Order-month view versus cash view: the order-month view assigns a refund back to the month of its order, so January net changes after February's refund arrives (restatement); the cash view books the refund when it is paid, so history does not move but a month's net can be low because of old orders. Finance often wants cash, product often wants order-month; say which one and label it.
- A refund larger than the order, or a refund on a cancelled order: I excluded cancelled orders from both views; I would flag over-refunds as data errors instead of letting them go negative.
- Orders with no refunds: `COALESCE(..., 0)` is needed because a NULL refund would make `gross - NULL` NULL.
- Currency or partial refund of shipping only: out of scope here.

**Then explain:**
- Fan-out: joining a parent to a many-row child repeats the parent's columns, so any parent-level SUM is multiplied. Aggregate the child to the parent's grain first.
- Pre-aggregation keeps one join and is easy to index; the scalar subquery is clearer but runs once per order (the engine may optimise it, not executed beyond SQLite).
- Check the result by recomputing gross from the orders table alone: it must not change after the join.
- Dialects (not executed here): the same two fixes work in PostgreSQL, MySQL, BigQuery and Snowflake; `strftime` becomes `date_trunc('month', ...)` or `DATE_FORMAT`.

**Follow-ups:**
- Refund rates? See Q11.
- Net revenue per user (LTV net of refunds)? Q22.
- Refunds with no matching order? A `LEFT JOIN` from refunds to orders finds them (data-quality check).

**Common mistakes:**
- Join first, then `SUM(orders.amount)`.
- Inner join that drops unrefunded orders.
- Mixing month bases: orders by order month, refunds by refund month, in one net figure.
- Forgetting `COALESCE`.
"""
T[11] = """**Say this first (1 line):** Group orders by order month; cancellation rate is cancelled over all orders, refund rate by count is completed orders with at least one refund over completed orders (pre-aggregate or `EXISTS` so two refunds count once), and refund rate by value is refunded amount over completed amount, with the refund assigned to its order's month so numerator and denominator describe the same orders.

**Schema and sample data:** eleven orders and four refunds. Order 1 has two refunds. April has only a cancelled order, so there are no completed orders at all in that month.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
CREATE TABLE refunds(refund_id INTEGER PRIMARY KEY, order_id INTEGER, refund_ts TEXT, amount REAL);
INSERT INTO orders VALUES
 (1,1,'2024-01-10 10:00:00',100,'completed'),
 (2,2,'2024-01-20 10:00:00',200,'completed'),
 (7,6,'2024-01-25 10:00:00',60,'cancelled'),
 (3,3,'2024-02-05 10:00:00',150,'completed'),
 (4,4,'2024-02-14 10:00:00',80,'cancelled'),
 (5,1,'2024-02-20 10:00:00',50,'completed'),
 (6,5,'2024-03-03 10:00:00',120,'completed'),
 (9,5,'2024-03-20 10:00:00',60,'completed'),
 (8,7,'2024-03-09 10:00:00',40,'cancelled'),
 (10,7,'2024-03-12 10:00:00',25,'cancelled'),
 (11,1,'2024-04-02 10:00:00',70,'cancelled');
INSERT INTO refunds VALUES
 (1,1,'2024-01-15 10:00:00',30),(2,1,'2024-02-02 10:00:00',20),
 (3,3,'2024-02-10 10:00:00',150),(4,5,'2024-03-01 10:00:00',10);
```

**SQL answer:** `SQL_MAIN` in the Code block (refunds pre-aggregated to one row per order, then one pass over orders):
```sql
{SQL:SQL_MAIN}
```
The `EXISTS` form for the count rate is `SQL_EXISTS` in the Code block; the wrong refund-month version is `SQL_WRONG`:
```sql
{SQL:SQL_EXISTS}
```

**pandas answer:** shown once, identical to the Code block:
```py
{PD}
```

**Example:** per order month.
- January: 3 orders, 1 cancelled = 33.3% cancellation. Completed 2 (orders 1, 2); order 1 has two refunds, so 1 refunded order of 2 = 50.0% by count. By value: refunded 30 + 20 = 50 over completed 300 = 16.7%.
- February: 3 orders, 1 cancelled = 33.3%. Completed 2 (orders 3, 5), both refunded = 100.0% by count; value (150 + 10) over 200 = 80.0%.
- March: 4 orders, 2 cancelled = 50.0%; 2 completed, none refunded = 0.0% and 0.0%.
- April: 1 order, cancelled = 100.0%; no completed orders, so both refund rates are NULL (undefined), not 0.
- If the refund is joined by refund month instead (wrong), January value is 10.0 (only the 30 paid in January, over 300), February 85.0 (170 over 200: order 1's 20 and order 3's 150) and March count 50.0 and value 5.6 (the 10 paid in March over 180), even though no March order was refunded.

**Code:** run with `python3 -I`. The assert compares pandas to the SQL main result ordered by month; the `EXISTS` rate column is also asserted equal for the three months that have completed orders.
```python
{CODE}
```

**Output (my run):**
```text
{OUT}
```

**Edge cases:**
- Two refunds on one order (order 1) count once in the count rate because of the pre-aggregation or `EXISTS`; a plain join would count the order twice in the numerator and could push the rate above 100%.
- A month with no completed orders: `NULLIF(..., 0)` returns NULL; in pandas I mask the zero denominator to get NaN. Show it as "n/a", not 0%.
- Refund on a cancelled order (should not happen): the status filter ignores it; I would also list such rows as data errors.
- Refunds lag orders: recent months are incomplete (a March order may still be refunded in May), so the latest months understate the refund rate; use a mature window or cohort by age (Part 6 Q13 covers the immature-cohort idea for retention).
- Cancellation rate is order-level over all orders in the month; a cancellation that happens in a later month is still charged to the order month here.
- Partial refunds: the count rate treats a 10 refund like a 150 refund; the value rate does not, so report both.

**Then explain:**
- Refund rate by count answers "how many orders have a problem"; by value answers "how much revenue is lost"; they differ (50.0 versus 16.7 in January).
- Numerator and denominator must be about the same set of orders. Counting refunds by `refund_ts` month over orders by `order_ts` month mixes two populations and makes the March rate nonzero when no March order was refunded.
- `SUM(boolean)` counts true values in SQLite; in PostgreSQL use `COUNT(*) FILTER (WHERE ...)` or `SUM(CASE ...)` (not executed here).
- Dialects (not executed here): BigQuery `COUNTIF`, `SAFE_DIVIDE`; MySQL `DATE_FORMAT(order_ts, '%Y-%m')`.

**Follow-ups:**
- Net revenue per month? Q10.
- Refund rate by cohort age rather than calendar month? Group by months since order and use only mature ages (Part 6).
- Cancellations by reason or by side? Add the dimension to the group; see Q23 for who cancelled.

**Common mistakes:**
- Joining refunds to orders and counting rows (order 1 twice).
- Bucketing refunds by refund month over orders by order month.
- Treating a month with no completed orders as a 0% refund rate.
- Dividing refunded amount by gross including cancelled orders.
- Integer division.
"""
