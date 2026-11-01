### Q11 ⭐⭐⭐ 🔴 [Set E1, Q5 of 5, 12 min, 25 pts] Checkout funnel with order (e-commerce). events(user_id, event_ts, event_name) with names view, add_to_cart, checkout, purchase. Return the number of users reaching each step in strict order (a later step counts only if it happens after the earlier step for the same user, Part 8 Q7 and Q9), plus step-to-step and overall conversion. Seed 10 users, including a user who purchases before adding to cart and a user with two views. Solve in SQL (MIN(CASE) per step) and pandas (groupby min per step), assert equal.
**Asked at:** E-commerce SQL prep pages (Let's Data Science e-commerce and marketplace list, a Dev Genius article, user-uploaded Scribd question sets; search snippets only, not opened); editorial guides and uploads of unknown provenance, not verified candidate reports; analyst and data scientist rounds at Indian and global e-commerce firms
**Say this first (1 line):** For each user take the earliest `view`, then the earliest `add_to_cart` that is strictly later than that view, then the earliest `checkout` later than that, then the earliest `purchase` later than that; count users who got through each step, and divide by the previous step and by step 1.

**Schema and sample data:** (assumption said out loud: a step only counts if its time is strictly later than the time of the step before it, so two events with the same timestamp do not count as "in order"; users who never viewed are not in the funnel.)
```sql
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2025-03-01 10:00:00','view'),(1,'2025-03-01 10:05:00','add_to_cart'),(1,'2025-03-01 10:10:00','checkout'),(1,'2025-03-01 10:15:00','purchase'),
 (2,'2025-03-01 10:00:00','view'),(2,'2025-03-01 10:05:00','add_to_cart'),(2,'2025-03-01 10:10:00','checkout'),
 (3,'2025-03-01 10:00:00','view'),(3,'2025-03-01 10:05:00','add_to_cart'),
 (4,'2025-03-01 10:00:00','view'),
 (5,'2025-03-01 09:00:00','view'),(5,'2025-03-01 09:10:00','checkout'),(5,'2025-03-01 09:20:00','purchase'),(5,'2025-03-01 09:30:00','add_to_cart'),
 (6,'2025-03-01 10:00:00','view'),(6,'2025-03-01 10:10:00','add_to_cart'),(6,'2025-03-01 10:20:00','view'),
 (7,'2025-03-01 09:00:00','add_to_cart'),(7,'2025-03-01 09:30:00','view'),(7,'2025-03-01 10:00:00','add_to_cart'),(7,'2025-03-01 10:10:00','checkout'),(7,'2025-03-01 10:20:00','purchase'),
 (8,'2025-03-01 10:00:00','add_to_cart'),(8,'2025-03-01 10:05:00','checkout'),(8,'2025-03-01 10:10:00','purchase'),
 (9,'2025-03-01 10:00:00','view'),(9,'2025-03-01 10:00:00','add_to_cart'),
 (10,'2025-03-02 11:00:00','view'),(10,'2025-03-02 11:05:00','add_to_cart'),(10,'2025-03-02 11:10:00','checkout'),(10,'2025-03-02 11:15:00','purchase'),(10,'2025-03-02 11:20:00','purchase');
```

**SQL answer:** the query `sql` in the Code block. It chains four CTEs: `s1` is the first view per user; `s2` joins `s1` back to `events` and keeps `add_to_cart` events with `event_ts > s1.t`, then takes the MIN; `s3` and `s4` repeat that for `checkout` and `purchase`. A `UNION ALL` of the four counts gives the funnel, and `LAG` and `FIRST_VALUE` give the step and overall conversion.

**pandas answer:** the loop in the Code block. It keeps a frame `cur` of (user_id, t) for the previous step, merges the next step's events on `user_id`, filters `event_ts > t`, and takes `groupby('user_id').min()`. The row count at each step is the funnel count.

**Example:** by hand, per user (V = view, C = cart, K = checkout, P = purchase):
- User 1 and user 10: V, C, K, P in order, so they reach step 4 (user 10 has two purchases, still one user).
- User 2: V, C, K, then stops: step 3. User 3: V, C: step 2. User 4: V only: step 1.
- User 5: V 09:00, checkout 09:10, purchase 09:20, cart 09:30. The cart is after the view, so step 2 is reached; no checkout is later than 09:30, so the funnel stops at step 2 even though a purchase exists (purchase before add_to_cart).
- User 6: two views (10:00 and 10:20) and a cart at 10:10; the first view is 10:00, so the cart counts: step 2.
- User 7: cart 09:00, view 09:30, cart 10:00, checkout, purchase. The first cart is before the view, but the cart at 10:00 is after it, so the strict funnel counts this user through step 4.
- User 8: never viewed: not in step 1. User 9: view and cart at the same second: the cart is not strictly later, so step 1 only.
- Totals: step 1 = 9 (users 1 to 7, 9, 10), step 2 = 7 (1, 2, 3, 5, 6, 7, 10), step 3 = 4 (1, 2, 7, 10), step 4 = 3 (1, 7, 10). Conversions: 7/9 = 0.7778, 4/7 = 0.5714, 3/4 = 0.75; overall 3/9 = 0.3333.

**Code:** run with `python3 -I`.
```python
# Q11: strict-order checkout funnel (SQL chained MIN per step, pandas groupby min per step)
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2025-03-01 10:00:00','view'),(1,'2025-03-01 10:05:00','add_to_cart'),(1,'2025-03-01 10:10:00','checkout'),(1,'2025-03-01 10:15:00','purchase'),
 (2,'2025-03-01 10:00:00','view'),(2,'2025-03-01 10:05:00','add_to_cart'),(2,'2025-03-01 10:10:00','checkout'),
 (3,'2025-03-01 10:00:00','view'),(3,'2025-03-01 10:05:00','add_to_cart'),
 (4,'2025-03-01 10:00:00','view'),
 (5,'2025-03-01 09:00:00','view'),(5,'2025-03-01 09:10:00','checkout'),(5,'2025-03-01 09:20:00','purchase'),(5,'2025-03-01 09:30:00','add_to_cart'),
 (6,'2025-03-01 10:00:00','view'),(6,'2025-03-01 10:10:00','add_to_cart'),(6,'2025-03-01 10:20:00','view'),
 (7,'2025-03-01 09:00:00','add_to_cart'),(7,'2025-03-01 09:30:00','view'),(7,'2025-03-01 10:00:00','add_to_cart'),(7,'2025-03-01 10:10:00','checkout'),(7,'2025-03-01 10:20:00','purchase'),
 (8,'2025-03-01 10:00:00','add_to_cart'),(8,'2025-03-01 10:05:00','checkout'),(8,'2025-03-01 10:10:00','purchase'),
 (9,'2025-03-01 10:00:00','view'),(9,'2025-03-01 10:00:00','add_to_cart'),
 (10,'2025-03-02 11:00:00','view'),(10,'2025-03-02 11:05:00','add_to_cart'),(10,'2025-03-02 11:10:00','checkout'),(10,'2025-03-02 11:15:00','purchase'),(10,'2025-03-02 11:20:00','purchase');
""")

# strict order: each step uses the EARLIEST event of that step that is later than the previous step's time
sql = """
WITH s1 AS (SELECT user_id, MIN(event_ts) AS t FROM events WHERE event_name = 'view' GROUP BY user_id),
s2 AS (SELECT s1.user_id, MIN(e.event_ts) AS t FROM s1 JOIN events e
         ON e.user_id = s1.user_id AND e.event_name = 'add_to_cart' AND e.event_ts > s1.t GROUP BY s1.user_id),
s3 AS (SELECT s2.user_id, MIN(e.event_ts) AS t FROM s2 JOIN events e
         ON e.user_id = s2.user_id AND e.event_name = 'checkout' AND e.event_ts > s2.t GROUP BY s2.user_id),
s4 AS (SELECT s3.user_id, MIN(e.event_ts) AS t FROM s3 JOIN events e
         ON e.user_id = s3.user_id AND e.event_name = 'purchase' AND e.event_ts > s3.t GROUP BY s3.user_id),
f AS (
  SELECT 1 AS step, 'view' AS step_name, COUNT(*) AS users FROM s1
  UNION ALL SELECT 2, 'add_to_cart', COUNT(*) FROM s2
  UNION ALL SELECT 3, 'checkout', COUNT(*) FROM s3
  UNION ALL SELECT 4, 'purchase', COUNT(*) FROM s4)
SELECT step, step_name, users,
       ROUND(1.0 * users / LAG(users) OVER (ORDER BY step), 4) AS step_conv,
       ROUND(1.0 * users / FIRST_VALUE(users) OVER (ORDER BY step), 4) AS overall_conv
FROM f ORDER BY step
"""
a = pd.read_sql(sql, con)
print("SQL strict funnel"); print(a.to_string(index=False))

# the 'simple' MIN(CASE) per step, with and without chaining, to show where each goes wrong
simple = """
WITH t AS (SELECT user_id,
  MIN(CASE WHEN event_name='view' THEN event_ts END) AS v,
  MIN(CASE WHEN event_name='add_to_cart' THEN event_ts END) AS c,
  MIN(CASE WHEN event_name='checkout' THEN event_ts END) AS k,
  MIN(CASE WHEN event_name='purchase' THEN event_ts END) AS p
  FROM events GROUP BY user_id)
SELECT COUNT(v) AS view_n, COUNT(c) AS cart_any, COUNT(k) AS checkout_any, COUNT(p) AS purchase_any,
  SUM(c > v) AS cart_chain, SUM(c > v AND k > c) AS checkout_chain, SUM(c > v AND k > c AND p > k) AS purchase_chain
FROM t
"""
print("\nsimple MIN(CASE) counts (no order / chained min):")
print(pd.read_sql(simple, con).to_string(index=False))

# pandas: same chain, one merge per step
ev = pd.read_sql("SELECT * FROM events", con)
cur = ev[ev.event_name == "view"].groupby("user_id")["event_ts"].min().rename("t").reset_index()
counts = [("view", len(cur))]
for name in ["add_to_cart", "checkout", "purchase"]:
    nxt = ev[ev.event_name == name][["user_id", "event_ts"]].merge(cur, on="user_id")
    nxt = nxt[nxt.event_ts > nxt.t].groupby("user_id")["event_ts"].min().rename("t").reset_index()
    counts.append((name, len(nxt)))
    cur = nxt
p = pd.DataFrame(counts, columns=["step_name", "users"])
p.insert(0, "step", range(1, 5))
p["step_conv"] = (p.users / p.users.shift(1)).round(4)
p["overall_conv"] = (p.users / p.users.iloc[0]).round(4)
print("\npandas strict funnel"); print(p.to_string(index=False))
# compare in step order (both already ordered by step)
pd.testing.assert_frame_equal(a, p, check_dtype=False)
print("\nassert passed: SQL == pandas, rows in step order")
```

**Output (my run):**
```text
SQL strict funnel
 step   step_name  users  step_conv  overall_conv
    1        view      9        NaN        1.0000
    2 add_to_cart      7     0.7778        0.7778
    3    checkout      4     0.5714        0.4444
    4    purchase      3     0.7500        0.3333

simple MIN(CASE) counts (no order / chained min):
 view_n  cart_any  checkout_any  purchase_any  cart_chain  checkout_chain  purchase_chain
      9         9             6             5           6               3               2

pandas strict funnel
 step   step_name  users  step_conv  overall_conv
    1        view      9        NaN        1.0000
    2 add_to_cart      7     0.7778        0.7778
    3    checkout      4     0.5714        0.4444
    4    purchase      3     0.7500        0.3333

assert passed: SQL == pandas, rows in step order
```

**Edge cases:**
- **Purchase before cart (user 5):** a plain count of users with a purchase event would include them; the strict chain does not. The "any event" counts in the second printed table (`cart_any` 9, `checkout_any` 6, `purchase_any` 5) show how far an unordered funnel overstates.
- **Earliest-after, not global MIN (user 7):** the "chained MIN(CASE)" version (`cart_chain`, `checkout_chain`, `purchase_chain`: 6, 3, 2) takes each step's overall first time and compares it with the previous one. User 7's first cart (09:00) is before the first view (09:30), so that version drops them, and undercounts steps 2 to 4 by one. The fix is to take the earliest event after the previous step, as the Code block does. The prompt's "MIN(CASE) per step" idea is fine for the first step and for a funnel where order is not enforced; for strict order it needs the "later than" join.
- **Ties in time (user 9):** a same-timestamp view and cart do not count here (`>`); say if your product would count them (`>=`).
- **Repeat events (users 6 and 10):** MIN per user collapses them, so counts are users, not events.
- **Empty step:** if no user reaches a step, the `JOIN` returns no rows and `COUNT(*)` returns 0, so the funnel row still appears.

**Then explain:**
- **Why strict order:** an unordered funnel counts a purchase that has no cart before it (data fix-ups, duplicated events, clock skew, or a re-order link), and conversion can then even look better than reality.
- **The conversion columns:** step conversion divides by the previous step (`LAG`), overall conversion divides by step 1 (`FIRST_VALUE`). The first step has no previous step, so its step conversion is NULL in SQL and NaN in pandas.
- **Dialects (not executed here):** the same SQL works on PostgreSQL, MySQL 8, BigQuery and Snowflake (they all have `LAG` and `FIRST_VALUE`); `ROUND` and the `1.0 *` cast to avoid integer division are the usual small changes.
- **Scoring note (Set E1, Q5 of 5, 25 pts):** about 10 points for the right counts on the seed (9, 7, 4, 3), 5 for handling the seeded trap (user 5 and user 7, or at least user 5), 5 for the pandas version asserted equal, 2.5 for saying the order and tie assumption before coding, 2.5 for a check such as "step 1 is never smaller than step 2". Full marks need the "later than the previous step" join; the global-MIN version with the right numbers on a lucky seed earns partial credit only.

**Follow-ups:**
- *Add a time limit (purchase within 24 hours of the view)?* Add `AND e.event_ts <= datetime(s1.t, '+1 day')` style conditions in the join, measured from step 1, and state whether the window starts at the first view.
- *Do it by session?* Replace `user_id` with `session_id` in every join; the logic does not change.
- *How do you break it down by channel?* Add the channel to the select and `GROUP BY`, keeping the user in the step CTEs, or compute per channel in pandas with a groupby around the loop.

**Common mistakes:**
- Counting users with any `purchase` event as step 4 and ignoring order.
- Comparing global minimums per step (loses users like user 7).
- Counting events rather than distinct users (user 10's two purchases).
- Dividing by the wrong denominator, or integer division in SQL (`3/9` gives 0 without `1.0 *`).
- Forgetting that the first step's step-conversion is undefined.

### Q12 ⭐⭐⭐ 🔴 [Set E1, Q4 of 5, 12 min, 25 pts] Net revenue after returns without fan-out. orders(order_id, customer_id, order_date, shipping_fee), order_items(item_id, order_id, product_id, qty, unit_price) and returns(return_id, item_id, qty_returned, refund_amount) where one item can have two partial returns. Return net revenue per order (items minus refunds, shipping excluded) and the share of orders with any return. Show the naive three-table join total, why it is wrong (Part 2 Q12, Part 8 Q10), then the pre-aggregated version in SQL and pandas. Seed 5 orders.
**Asked at:** E-commerce SQL prep pages (Let's Data Science e-commerce and marketplace list, a Dev Genius article, user-uploaded Scribd question sets; search snippets only, not opened); editorial guides and uploads of unknown provenance, not verified candidate reports; analyst and data scientist rounds at Indian and global e-commerce firms
**Say this first (1 line):** Aggregate each child table to the order grain first (item total per order, refund total per order), then join the two one-row-per-order results to `orders`; a direct three-table join repeats an item's line total once for every return row of that item and overstates revenue.

**Schema and sample data:** (assumption: net revenue = sum of `qty * unit_price` minus the sum of `refund_amount`, shipping excluded; "orders with any return" counts orders that have at least one return row.)
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, shipping_fee INTEGER);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id TEXT, qty INTEGER, unit_price INTEGER);
CREATE TABLE returns(return_id INTEGER PRIMARY KEY, item_id INTEGER, qty_returned INTEGER, refund_amount INTEGER);
INSERT INTO orders VALUES (1,10,'2025-01-05',50),(2,11,'2025-01-06',0),(3,12,'2025-01-07',40),(4,10,'2025-01-08',30),(5,13,'2025-01-09',0);
INSERT INTO order_items VALUES (1,1,'P1',2,100),(2,1,'P2',1,200),(3,2,'P1',1,100),(4,3,'P3',3,50),(5,3,'P2',1,200),(6,4,'P1',1,100),(7,5,'P4',4,25);
INSERT INTO returns VALUES (1,1,1,100),(2,1,1,100),(3,4,1,50),(4,6,1,100);
```

**SQL answer:** `naive` (the broken three-table join), `sql` (pre-aggregated: CTE `item_tot` per order, CTE `ret_tot` per order through `order_items`, then two `LEFT JOIN`s from `orders` with `COALESCE`) and `share` (an `EXISTS` per order) are in the Code block.

**pandas answer:** the Code block computes the line value per item, `groupby('order_id').sum()` for items, merges `returns` to `order_items` to find each return's order, `groupby('order_id').sum()` for refunds, and left-merges both onto the orders frame with `fillna(0)`.

**Example:** by hand.
- Order 1: item 1 is 2 x 100 = 200, item 2 is 1 x 200 = 200, so items = 400. Item 1 has two partial returns of 100 each, so refunds = 200 and net = 200.
- Order 2: 1 x 100 = 100, no return, net 100.
- Order 3: 3 x 50 + 1 x 200 = 350, one refund of 50, net 300.
- Order 4: 100 with a full refund of 100, net 0. Order 5: 4 x 25 = 100, net 100.
- Total net = 200 + 100 + 300 + 0 + 100 = 700. Orders with a return: 1, 3, 4, so 3 of 5 = 0.6.
- The naive join has two rows for item 1 (one per return), so item 1's 200 appears twice: order 1 shows items = 600 and net 400, and the total net is 900 instead of 700, an overstatement of exactly 200.

**Code:** run with `python3 -I`.
```python
# Q12: net revenue per order after partial returns, without join fan-out
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, shipping_fee INTEGER);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id TEXT, qty INTEGER, unit_price INTEGER);
CREATE TABLE returns(return_id INTEGER PRIMARY KEY, item_id INTEGER, qty_returned INTEGER, refund_amount INTEGER);
INSERT INTO orders VALUES (1,10,'2025-01-05',50),(2,11,'2025-01-06',0),(3,12,'2025-01-07',40),(4,10,'2025-01-08',30),(5,13,'2025-01-09',0);
INSERT INTO order_items VALUES (1,1,'P1',2,100),(2,1,'P2',1,200),(3,2,'P1',1,100),(4,3,'P3',3,50),(5,3,'P2',1,200),(6,4,'P1',1,100),(7,5,'P4',4,25);
INSERT INTO returns VALUES (1,1,1,100),(2,1,1,100),(3,4,1,50),(4,6,1,100);
""")

naive = """
SELECT o.order_id, SUM(i.qty * i.unit_price) AS items_total, SUM(COALESCE(r.refund_amount, 0)) AS refunds,
       SUM(i.qty * i.unit_price) - SUM(COALESCE(r.refund_amount, 0)) AS net
FROM orders o JOIN order_items i ON i.order_id = o.order_id
LEFT JOIN returns r ON r.item_id = i.item_id
GROUP BY o.order_id ORDER BY o.order_id
"""
sql = """
WITH item_tot AS (
  SELECT order_id, SUM(qty * unit_price) AS items_total FROM order_items GROUP BY order_id),
ret_tot AS (
  SELECT i.order_id, SUM(r.refund_amount) AS refunds, COUNT(*) AS return_rows
  FROM returns r JOIN order_items i ON i.item_id = r.item_id GROUP BY i.order_id)
SELECT o.order_id, COALESCE(t.items_total, 0) AS items_total, COALESCE(r.refunds, 0) AS refunds,
       COALESCE(t.items_total, 0) - COALESCE(r.refunds, 0) AS net
FROM orders o LEFT JOIN item_tot t ON t.order_id = o.order_id
LEFT JOIN ret_tot r ON r.order_id = o.order_id
ORDER BY o.order_id
"""
share = """
SELECT COUNT(*) AS orders,
       SUM(EXISTS (SELECT 1 FROM returns r JOIN order_items i ON i.item_id = r.item_id WHERE i.order_id = o.order_id)) AS orders_with_return,
       ROUND(1.0 * SUM(EXISTS (SELECT 1 FROM returns r JOIN order_items i ON i.item_id = r.item_id WHERE i.order_id = o.order_id)) / COUNT(*), 4) AS return_share
FROM orders o
"""
n = pd.read_sql(naive, con); a = pd.read_sql(sql, con); s = pd.read_sql(share, con)
print("naive three-table join"); print(n.to_string(index=False), "\nnaive total net:", n.net.sum())
print("\npre-aggregated SQL"); print(a.to_string(index=False), "\ntotal net:", a.net.sum())
print("\nshare of orders with any return (SQL)"); print(s.to_string(index=False))

orders = pd.read_sql("SELECT * FROM orders", con)
items = pd.read_sql("SELECT * FROM order_items", con)
rets = pd.read_sql("SELECT * FROM returns", con)
items["line"] = items.qty * items.unit_price
it = items.groupby("order_id")["line"].sum().rename("items_total")
rt = rets.merge(items[["item_id", "order_id"]], on="item_id").groupby("order_id").agg(refunds=("refund_amount", "sum"), return_rows=("return_id", "size"))
p = orders[["order_id"]].merge(it, on="order_id", how="left").merge(rt[["refunds"]], on="order_id", how="left")
p[["items_total", "refunds"]] = p[["items_total", "refunds"]].fillna(0).astype("int64")
p["net"] = p.items_total - p.refunds
pshare = pd.DataFrame({"orders": [len(orders)], "orders_with_return": [int(orders.order_id.isin(rt.index).sum())]})
pshare["return_share"] = (pshare.orders_with_return / pshare.orders).round(4)
print("\npandas"); print(p.to_string(index=False)); print(pshare.to_string(index=False))
pd.testing.assert_frame_equal(a, p, check_dtype=False)
pd.testing.assert_frame_equal(s, pshare, check_dtype=False)
print("\nasserts passed: per-order table (ordered by order_id) and share row equal")
```

**Output (my run):**
```text
naive three-table join
 order_id  items_total  refunds  net
        1          600      200  400
        2          100        0  100
        3          350       50  300
        4          100      100    0
        5          100        0  100 
naive total net: 900

pre-aggregated SQL
 order_id  items_total  refunds  net
        1          400      200  200
        2          100        0  100
        3          350       50  300
        4          100      100    0
        5          100        0  100 
total net: 700

share of orders with any return (SQL)
 orders  orders_with_return  return_share
      5                   3           0.6

pandas
 order_id  items_total  refunds  net
        1          400      200  200
        2          100        0  100
        3          350       50  300
        4          100      100    0
        5          100        0  100
 orders  orders_with_return  return_share
      5                   3           0.6

asserts passed: per-order table (ordered by order_id) and share row equal
```

**Edge cases:**
- **Two returns on one item:** the case that breaks the naive join. The refund sum is right in the naive join (each refund appears once); the item total is what multiplies. A bug that hides because one of the two sums is correct.
- **Orders without items or returns:** `LEFT JOIN` plus `COALESCE(...,0)` keeps them. Without the `LEFT JOIN`, order 2 would vanish from the refunds side.
- **Refund larger than the item value, or a refund row with 0 amount:** a return row with a 0 refund still counts as "an order with a return" here (existence of a row). If your definition is "refund greater than 0", filter first.
- **NULL refund_amount:** `SUM` skips NULLs; if every refund is NULL the sum is NULL, hence the `COALESCE`.
- **Shipping:** excluded on purpose; if it were included and refunded it is a business rule to confirm.

**Then explain:**
- **Why fan-out happens:** joining order to items gives one row per item, and joining returns then gives one row per (item, return). Anything that lives at the item or order level is repeated per return row.
- **Fix pattern:** aggregate child tables to the grain you report (order), then join; or sum in a subquery. A `DISTINCT` on line items would be wrong, because two different items can have equal values.
- **The check:** the one-line sanity test is that the sum of item totals (1050 here) does not change when you join the returns table in; the naive join reports 1250.
- **Dialects (not executed here):** the same query runs on PostgreSQL, MySQL, BigQuery and Snowflake; `EXISTS` returns a boolean in those engines, so `SUM(EXISTS(...))` is a SQLite and MySQL habit; use `SUM(CASE WHEN EXISTS (...) THEN 1 ELSE 0 END)` or a join to the pre-aggregated `ret_tot` to be portable.
- **Scoring note (Set E1, Q4 of 5, 25 pts):** about 10 points for the correct per-order net and the 0.6 share, 5 for the fan-out explanation shown on the seed (the 900 versus 700 contrast), 5 for pandas asserted equal, 2.5 for stating that shipping is excluded and how a return is defined, 2.5 for a reconciliation check (1050 items, 350 refunds). Quoting the naive total but not saying why it is wrong gets partial credit only.

**Follow-ups:**
- *What if refunds are recorded per order, not per item?* Then join `returns` to `orders` directly; the same rule holds: aggregate it to one row per order before joining.
- *How would you get net revenue per product?* Aggregate returns per item, join to items, then group by product. Orders are no longer the grain.
- *Why not `COUNT(DISTINCT order_id)` and be done?* That fixes counts but not sums; sums double-count the repeated line.

**Common mistakes:**
- Summing item values after joining returns.
- `INNER JOIN` to returns, which drops every order without a return.
- Dividing the number of return rows (4 here) by orders instead of orders with a return (3 of 5).
- Letting a NULL refund turn net revenue NULL.

### Q13 ⭐⭐⭐ 🔴 [Set E2, Q5 of 5, 12 min, 25 pts] Stock never below zero. inventory_moves(move_id, sku, move_date, qty_change) with receipts positive, sales negative, several moves per day per sku. For each sku return the first date the running stock fell below zero, or NULL if it never did, and the lowest running stock (Part 5 Q22). Resolve same-day ordering by move_id and state the assumption. Seed 3 skus. SQL (running SUM, then MIN over a filter) and pandas (cumsum per group), assert equal.
**Asked at:** E-commerce SQL prep pages (Let's Data Science e-commerce and marketplace list, a Dev Genius article, user-uploaded Scribd question sets; search snippets only, not opened); editorial guides and uploads of unknown provenance, not verified candidate reports; analyst and data scientist rounds at Indian and global e-commerce firms
**Say this first (1 line):** Take a running sum of `qty_change` per sku ordered by `(move_date, move_id)`, then per sku return the earliest date among rows where the running total is below zero (NULL if none) and the minimum running total.

**Schema and sample data:** (assumption: moves on the same day are applied in `move_id` order, so a sale logged before a receipt on the same day is a real dip; the end-of-day view is a different question, shown for contrast. "Below zero" means strictly less than 0, so a stock of exactly 0 is fine.)
```sql
CREATE TABLE inventory_moves(move_id INTEGER PRIMARY KEY, sku TEXT, move_date TEXT, qty_change INTEGER);
INSERT INTO inventory_moves VALUES
 (1,'A','2025-01-01',10),(2,'A','2025-01-02',-4),(3,'A','2025-01-02',-8),(4,'A','2025-01-03',20),
 (5,'B','2025-01-01',5),(6,'B','2025-01-02',-7),(7,'B','2025-01-02',10),
 (8,'C','2025-01-01',3),(9,'C','2025-01-02',-3);
```

**SQL answer:** `sql` in the Code block: a CTE `r` with `SUM(qty_change) OVER (PARTITION BY sku ORDER BY move_date, move_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`, then `MIN(CASE WHEN stock < 0 THEN move_date END)` and `MIN(stock)` grouped by sku. `eod` is the end-of-day variant.

**pandas answer:** sort by `sku, move_date, move_id`, `groupby('sku')['qty_change'].cumsum()`, then the minimum `move_date` among rows with `stock < 0` and the minimum `stock`, put side by side with `concat` (so skus that never went negative still get a row, with NaN).

**Example:** by hand.
- A: +10, -4, -8, +20 gives running 10, 6, -2, 18. The -8 on 2025-01-02 is the first move that takes it below zero, so the first negative date is 2025-01-02 and the lowest is -2.
- B: +5 on 01-01, then -7 (move 6) and +10 (move 7) both on 01-02. In move_id order the running totals are 5, -2, 8, so the stock dips below zero on 01-02 with lowest -2. By end of day the balance on 01-02 is 8, so the end-of-day variant says NULL and lowest 5.
- C: +3 then -3 gives 3, 0: it hits zero but never below, so NULL and lowest 0.

**Code:** run with `python3 -I`.
```python
# Q13: first date running stock fell below zero, and lowest running stock, per sku
import sqlite3
import pandas as pd

def norm(df):
    return df.astype(object).where(df.notna(), None)

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE inventory_moves(move_id INTEGER PRIMARY KEY, sku TEXT, move_date TEXT, qty_change INTEGER);
INSERT INTO inventory_moves VALUES
 (1,'A','2025-01-01',10),(2,'A','2025-01-02',-4),(3,'A','2025-01-02',-8),(4,'A','2025-01-03',20),
 (5,'B','2025-01-01',5),(6,'B','2025-01-02',-7),(7,'B','2025-01-02',10),
 (8,'C','2025-01-01',3),(9,'C','2025-01-02',-3);
""")
sql = """
WITH r AS (
  SELECT sku, move_date,
         SUM(qty_change) OVER (PARTITION BY sku ORDER BY move_date, move_id
                               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS stock
  FROM inventory_moves)
SELECT sku, MIN(CASE WHEN stock < 0 THEN move_date END) AS first_negative_date, MIN(stock) AS lowest_stock
FROM r GROUP BY sku ORDER BY sku
"""
eod = """
WITH d AS (SELECT sku, move_date, SUM(qty_change) AS day_qty FROM inventory_moves GROUP BY sku, move_date),
r AS (SELECT sku, move_date, SUM(day_qty) OVER (PARTITION BY sku ORDER BY move_date ROWS UNBOUNDED PRECEDING) AS stock FROM d)
SELECT sku, MIN(CASE WHEN stock < 0 THEN move_date END) AS first_negative_date, MIN(stock) AS lowest_stock
FROM r GROUP BY sku ORDER BY sku
"""
a = pd.read_sql(sql, con)
print("SQL (running stock per move, ties by move_id)"); print(a.to_string(index=False))
print("\nSQL end-of-day variant (not the answer)"); print(pd.read_sql(eod, con).to_string(index=False))

m = pd.read_sql("SELECT * FROM inventory_moves", con).sort_values(["sku", "move_date", "move_id"])
m["stock"] = m.groupby("sku")["qty_change"].cumsum()
first_neg = m[m.stock < 0].groupby("sku")["move_date"].min().rename("first_negative_date")
low = m.groupby("sku")["stock"].min().rename("lowest_stock")
p = pd.concat([first_neg, low], axis=1).reset_index().sort_values("sku").reset_index(drop=True)
print("\npandas"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(norm(a), norm(p), check_dtype=False)
print("\nassert passed: equal, rows ordered by sku (NULL and NaN normalised to None before comparing)")
```

**Output (my run):**
```text
SQL (running stock per move, ties by move_id)
sku first_negative_date  lowest_stock
  A          2025-01-02            -2
  B          2025-01-02            -2
  C                 NaN             0

SQL end-of-day variant (not the answer)
sku first_negative_date  lowest_stock
  A          2025-01-02            -2
  B                 NaN             5
  C                 NaN             0

pandas
sku first_negative_date  lowest_stock
  A          2025-01-02            -2
  B          2025-01-02            -2
  C                 NaN             0

assert passed: equal, rows ordered by sku (NULL and NaN normalised to None before comparing)
```

**Edge cases:**
- **Same-day ordering:** the result for B depends on it. If the receipt (move 7) were logged first, B would never go negative. This is a business assumption, so state it and, if the timestamps exist, use them rather than `move_id`.
- **Exactly zero (C):** not below zero; the lowest running stock is 0.
- **Never negative:** the `CASE` returns NULL for every row, `MIN` of all-NULL is NULL, and the sku is still returned. In pandas the filtered frame has no rows for C, so `concat` creates NaN (the Code block compares after turning NaN and NULL into None).
- **Frame choice:** the frame is explicit `ROWS`; the default frame with an `ORDER BY` is `RANGE` and treats equal sort keys as peers (here the key is two columns and unique, but the habit is the safer one; see Part 5 Q6).
- **Dates as text:** `MIN` on ISO `YYYY-MM-DD` text sorts correctly; other formats would not.
- **Opening stock:** if there is an opening balance not in the moves table, add it as a first move or start the running sum from it.

**Then explain:**
- **First negative date, not first negative move:** the filter plus `MIN(move_date)` gives the date; to also return the move, use `ROW_NUMBER` over the negative rows.
- **Why not `HAVING stock < 0`:** window results cannot be filtered in the same `SELECT`'s `WHERE`; that is why the running sum is a CTE and the filter sits in a `CASE`.
- **Dialects (not executed here):** the SQL is standard and runs unchanged on PostgreSQL, MySQL 8, BigQuery and Snowflake; SQL Server needs the window with `ROWS` as written.
- **Scoring note (Set E2, Q5 of 5, 25 pts):** about 10 points for the right first dates and lows on the seed (A: 01-02 and -2, B: 01-02 and -2, C: NULL and 0), 5 for a correct treatment of the seeded edge cases (the same-day tie and the exact zero), 5 for pandas asserted equal, 2.5 for stating the same-day assumption, 2.5 for a one-line check (the final running stock equals the plain `SUM`). Dropping sku C from the result, or returning 0 or an empty string instead of NULL, loses the edge-case points.

**Follow-ups:**
- *How long was it negative?* Find the first date back at or above zero with a second window; use islands (Part 7) on the negative flag.
- *What if you only want end-of-day balances?* Aggregate to one row per sku and day first (`eod` in the Code block) and then run the cumulative sum; the answer for B changes.
- *Which index helps?* `(sku, move_date, move_id)` lets the window read in order without a sort (Part 11); not tested here.

**Common mistakes:**
- Leaving out `move_id` in the order, so same-day rows run in an arbitrary order.
- Using `<= 0` for "below zero".
- Filtering the running total in `WHERE` and dropping skus that never went negative.
- Comparing a date-ordered running sum with a plain cumsum on unsorted data in pandas.

### Q14 ⭐⭐⭐ 🔴 [Set E2, Q4 of 5, 15 min, 25 pts] Seller scorecard in one query (Part 8 Q41 style). sellers(seller_id, name, tier), orders(order_id, seller_id, placed_at, delivered_at, promised_by, status), reviews(order_id, rating). For each seller return orders, cancel rate, late-delivery rate among delivered orders (delivered_at > promised_by), average rating (only rated orders), and rank by late rate within seller tier. Seed 4 sellers with a seller with zero delivered orders (rate NULL, not 0) and an order with two reviews rows. SQL with CTEs and pandas, asserts equal.
**Asked at:** E-commerce SQL prep pages (Let's Data Science e-commerce and marketplace list, a Dev Genius article, user-uploaded Scribd question sets; search snippets only, not opened); editorial guides and uploads of unknown provenance, not verified candidate reports; analyst and data scientist rounds at Indian and global e-commerce firms
**Say this first (1 line):** Build three small per-seller aggregates (order counts, per-order average rating, then rates with `NULLIF` on the denominators), left-join them from `sellers` so no seller disappears, and rank by late rate within tier with a `RANK()` that sorts NULLs last.

**Schema and sample data:** (assumptions said out loud: cancel rate = cancelled orders / all orders; late rate = orders with `delivered_at > promised_by` / delivered orders, so delivering exactly on the promised date is on time; an order with two review rows counts once, with the average of its ratings; rank 1 = highest late rate, i.e. worst, and a seller with no delivered orders gets no rank.)
```sql
CREATE TABLE sellers(seller_id INTEGER PRIMARY KEY, name TEXT, tier TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, seller_id INTEGER, placed_at TEXT, delivered_at TEXT, promised_by TEXT, status TEXT);
CREATE TABLE reviews(order_id INTEGER, rating INTEGER);
INSERT INTO sellers VALUES (1,'Alpha','GOLD'),(2,'Beta','GOLD'),(3,'Gamma','SILVER'),(4,'Delta','SILVER');
INSERT INTO orders VALUES
 (1,1,'2025-01-01','2025-01-04','2025-01-05','DELIVERED'),
 (2,1,'2025-01-02','2025-01-07','2025-01-05','DELIVERED'),
 (3,1,'2025-01-03',NULL,'2025-01-08','CANCELLED'),
 (4,1,'2025-01-04','2025-01-10','2025-01-10','DELIVERED'),
 (5,2,'2025-01-01','2025-01-09','2025-01-05','DELIVERED'),
 (6,2,'2025-01-02','2025-01-08','2025-01-06','DELIVERED'),
 (7,2,'2025-01-03','2025-01-05','2025-01-06','DELIVERED'),
 (8,3,'2025-01-01','2025-01-03','2025-01-04','DELIVERED'),
 (9,3,'2025-01-02',NULL,'2025-01-06','CANCELLED'),
 (10,4,'2025-01-01',NULL,'2025-01-05','CANCELLED'),
 (11,4,'2025-01-02',NULL,'2025-01-06','SHIPPED');
INSERT INTO reviews VALUES (1,5),(2,3),(4,4),(5,2),(6,4),(6,2),(8,5);
```

**SQL answer:** `sql` in the Code block. CTE `o` has the order counts per seller with conditional sums (`SUM(status = 'CANCELLED')` and so on), CTE `rv` averages ratings per order first and then per seller, CTE `card` left-joins both to `sellers` and computes the rates with `NULLIF`, and the final `SELECT` adds `RANK() OVER (PARTITION BY tier ORDER BY late_rate DESC NULLS LAST)`.

**pandas answer:** boolean columns `is_cancel`, `is_deliv`, `is_late` on `orders`, a `groupby('seller_id').agg(...)`, a per-order mean of `reviews` then a per-seller mean, left merges onto `sellers`, rates with `.where(denominator > 0)` so a zero denominator becomes NaN, and `groupby('tier')['late_rate'].rank(method='min', ascending=False, na_option='keep')`.

**Example:** by hand.
- Alpha (GOLD): 4 orders, 1 cancelled (0.25). Delivered: orders 1, 2, 4. Late: order 2 only (delivered 01-07, promised 01-05); order 4 delivered on the promised day is on time. Late rate 1/3 = 0.3333. Ratings 5, 3, 4 give 4.0.
- Beta (GOLD): 3 orders, none cancelled, all delivered; orders 5 and 6 are late: 2/3 = 0.6667. Order 6 has two reviews (4 and 2) so it counts as 3; order 5 has 2; order 7 has no review. Average (2 + 3) / 2 = 2.5. Averaging the three review rows instead gives (2 + 4 + 2) / 3 = 2.67.
- Gamma (SILVER): 2 orders, 1 cancelled (0.5); the one delivered order is on time, late rate 0.0 (a real zero); rating 5.0.
- Delta (SILVER): 2 orders (one cancelled, one shipped), cancel rate 0.5, zero delivered so late rate is NULL, no ratings so NULL average.
- Ranks within GOLD: Beta 1, Alpha 2. Within SILVER: Gamma 1, Delta none (NULL).

**Code:** run with `python3 -I`.
```python
# Q14: seller scorecard: cancel rate, late rate among delivered, average rating, rank by late rate within tier
import sqlite3
import pandas as pd

def norm(df):
    return df.astype(object).where(df.notna(), None)

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE sellers(seller_id INTEGER PRIMARY KEY, name TEXT, tier TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, seller_id INTEGER, placed_at TEXT, delivered_at TEXT, promised_by TEXT, status TEXT);
CREATE TABLE reviews(order_id INTEGER, rating INTEGER);
INSERT INTO sellers VALUES (1,'Alpha','GOLD'),(2,'Beta','GOLD'),(3,'Gamma','SILVER'),(4,'Delta','SILVER');
INSERT INTO orders VALUES
 (1,1,'2025-01-01','2025-01-04','2025-01-05','DELIVERED'),
 (2,1,'2025-01-02','2025-01-07','2025-01-05','DELIVERED'),
 (3,1,'2025-01-03',NULL,'2025-01-08','CANCELLED'),
 (4,1,'2025-01-04','2025-01-10','2025-01-10','DELIVERED'),
 (5,2,'2025-01-01','2025-01-09','2025-01-05','DELIVERED'),
 (6,2,'2025-01-02','2025-01-08','2025-01-06','DELIVERED'),
 (7,2,'2025-01-03','2025-01-05','2025-01-06','DELIVERED'),
 (8,3,'2025-01-01','2025-01-03','2025-01-04','DELIVERED'),
 (9,3,'2025-01-02',NULL,'2025-01-06','CANCELLED'),
 (10,4,'2025-01-01',NULL,'2025-01-05','CANCELLED'),
 (11,4,'2025-01-02',NULL,'2025-01-06','SHIPPED');
INSERT INTO reviews VALUES (1,5),(2,3),(4,4),(5,2),(6,4),(6,2),(8,5);
""")
sql = """
WITH o AS (
  SELECT seller_id,
         COUNT(*) AS orders,
         SUM(status = 'CANCELLED') AS cancelled,
         SUM(status = 'DELIVERED' AND delivered_at IS NOT NULL) AS delivered,
         SUM(status = 'DELIVERED' AND delivered_at > promised_by) AS late
  FROM orders GROUP BY seller_id),
rv AS (  -- one rating per order first (an order can have two review rows)
  SELECT o.seller_id, AVG(x.avg_rating) AS avg_rating
  FROM (SELECT order_id, AVG(rating) AS avg_rating FROM reviews GROUP BY order_id) x
  JOIN orders o ON o.order_id = x.order_id GROUP BY o.seller_id),
card AS (
  SELECT s.seller_id, s.name, s.tier, COALESCE(o.orders, 0) AS orders,
         ROUND(1.0 * o.cancelled / NULLIF(o.orders, 0), 4) AS cancel_rate,
         ROUND(1.0 * o.late / NULLIF(o.delivered, 0), 4) AS late_rate,
         ROUND(rv.avg_rating, 2) AS avg_rating
  FROM sellers s LEFT JOIN o ON o.seller_id = s.seller_id LEFT JOIN rv ON rv.seller_id = s.seller_id)
SELECT seller_id, name, tier, orders, cancel_rate, late_rate, avg_rating,
       CASE WHEN late_rate IS NULL THEN NULL
            ELSE RANK() OVER (PARTITION BY tier ORDER BY late_rate DESC NULLS LAST) END AS late_rank
FROM card ORDER BY tier, late_rank NULLS LAST, seller_id
"""
a = pd.read_sql(sql, con)
print("SQL"); print(a.to_string(index=False))

# what averaging over review ROWS (instead of per order) would give for Beta
print("\nBeta average over review rows:", con.execute(
    "SELECT ROUND(AVG(rating),2) FROM reviews r JOIN orders o ON o.order_id=r.order_id WHERE o.seller_id=2").fetchone()[0],
    "vs per order:", a.loc[a.name == "Beta", "avg_rating"].iloc[0])

sellers = pd.read_sql("SELECT * FROM sellers", con)
orders = pd.read_sql("SELECT * FROM orders", con)
rev = pd.read_sql("SELECT * FROM reviews", con)
orders["is_cancel"] = orders.status == "CANCELLED"
orders["is_deliv"] = (orders.status == "DELIVERED") & orders.delivered_at.notna()
orders["is_late"] = (orders.status == "DELIVERED") & (orders.delivered_at > orders.promised_by)
g = orders.groupby("seller_id").agg(orders=("order_id", "size"), cancelled=("is_cancel", "sum"),
                                    delivered=("is_deliv", "sum"), late=("is_late", "sum")).reset_index()
per_order = rev.groupby("order_id")["rating"].mean().rename("r").reset_index().merge(orders[["order_id", "seller_id"]], on="order_id")
rv = per_order.groupby("seller_id")["r"].mean().rename("avg_rating").reset_index()
p = sellers.merge(g, on="seller_id", how="left").merge(rv, on="seller_id", how="left")
p["orders"] = p.orders.fillna(0).astype("int64")
p["cancel_rate"] = (p.cancelled / p.orders.where(p.orders > 0)).round(4)
p["late_rate"] = (p.late / p.delivered.where(p.delivered > 0)).round(4)
p["avg_rating"] = p.avg_rating.round(2)
p["late_rank"] = p.groupby("tier")["late_rate"].rank(method="min", ascending=False, na_option="keep")
p = p[["seller_id", "name", "tier", "orders", "cancel_rate", "late_rate", "avg_rating", "late_rank"]]
p = p.sort_values(["tier", "late_rank", "seller_id"], na_position="last").reset_index(drop=True)
print("\npandas"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(norm(a), norm(p), check_dtype=False)
print("\nassert passed: equal, rows ordered by tier, late_rank (NULL last), seller_id")
```

**Output (my run):**
```text
SQL
 seller_id  name   tier  orders  cancel_rate  late_rate  avg_rating  late_rank
         2  Beta   GOLD       3         0.00     0.6667         2.5        1.0
         1 Alpha   GOLD       4         0.25     0.3333         4.0        2.0
         3 Gamma SILVER       2         0.50     0.0000         5.0        1.0
         4 Delta SILVER       2         0.50        NaN         NaN        NaN

Beta average over review rows: 2.67 vs per order: 2.5

pandas
 seller_id  name   tier  orders  cancel_rate  late_rate  avg_rating  late_rank
         2  Beta   GOLD       3         0.00     0.6667         2.5        1.0
         1 Alpha   GOLD       4         0.25     0.3333         4.0        2.0
         3 Gamma SILVER       2         0.50     0.0000         5.0        1.0
         4 Delta SILVER       2         0.50        NaN         NaN        NaN

assert passed: equal, rows ordered by tier, late_rank (NULL last), seller_id
```

**Edge cases:**
- **Zero delivered (Delta):** late rate is NULL, not 0. A zero would rank Delta as a perfect seller. `NULLIF(delivered, 0)` makes the division NULL; pandas gets NaN from `.where(denominator > 0)`.
- **Two reviews on one order (order 6):** averaging rows weights that order double (2.67 versus 2.5). Collapse to one value per order first.
- **Unrated orders:** `AVG` skips them; do not turn missing ratings into 0.
- **Delivery exactly on the promise date:** on time (`>` not `>=`).
- **Cancelled order with a `delivered_at`:** not in the data; the code also requires `status = 'DELIVERED'` so a stray timestamp on a cancelled row cannot count as late.
- **NULL ordering in rank:** SQLite sorts NULL first in ascending order and last in descending; PostgreSQL does the opposite for DESC, hence the explicit `NULLS LAST`, which SQLite 3.30 and later accepts. Delta's rank is forced to NULL by the `CASE`.
- **Ties in rate:** `RANK` gives equal rates the same rank (pandas `method='min'` matches).
- **Sorting:** the final `ORDER BY` also uses `NULLS LAST` so the NULL-rank seller comes last in its tier; the pandas sort uses `na_position='last'`.

**Then explain:**
- **One query, several denominators:** orders, delivered orders and rated orders are three different bases; naming each denominator is the point of this question.
- **Why CTEs:** each CTE keeps one grain (order counts per seller, ratings per order then seller) so the joins do not fan out.
- **Dialects (not executed here):** `NULLS LAST` is in PostgreSQL and Oracle (from memory); MySQL 8 does not accept the keyword (use `ORDER BY late_rate IS NULL, late_rate DESC`). Boolean sums such as `SUM(status = 'CANCELLED')` work in SQLite and MySQL; PostgreSQL needs `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` or `COUNT(*) FILTER (WHERE ...)`.
- **Scoring note (Set E2, Q4 of 5, 25 pts):** about 10 points for the right scorecard on the seed, 5 for handling the seeded edge cases (Delta NULL not 0, order 6 counted once), 5 for pandas asserted equal, 2.5 for stating the denominators and the rank direction, 2.5 for a check (orders sum to 11, delivered orders 7, rated orders 6). A zero instead of NULL for Delta, or a late rate over all orders, loses most of the edge-case points.

**Follow-ups:**
- *Only the best seller per tier?* Filter `late_rank = 1` in an outer query; remember it returns all sellers tied for 1.
- *Late rate over the last 90 days?* Add the date condition to the conditional sums, not to a `WHERE` that would also remove sellers.
- *How would you make a single score?* Normalise each metric first; a weighted sum of rates with different denominators can mislead, so say what weights you chose.

**Common mistakes:**
- Joining `reviews` straight to `orders` and counting order 6 twice.
- Using total orders as the late-rate denominator.
- Showing 0 for a seller with no delivered orders.
- Putting the status filter in `WHERE`, which drops sellers with no matching orders.
- Ranking without saying which end is rank 1.

### Q15 ⭐⭐⭐ 🔴 [Set F1, Q4 of 5, 10 min, 25 pts] Seven-day rolling active users (Meta-style growth metric). events(user_id, event_date) over 14 days with several rows per user per day. For every day from day 7 to day 14 return the number of distinct users active in the trailing 7 days including that day, using a date spine so days with no events still appear (Part 8 Q33, Part 5 Q45). Solve in SQL (range join to the spine) and pandas, and say why a plain 7-row window on the daily distinct count is wrong.
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Make a date spine for days 7 to 14, join each spine day to the events from the previous six days and itself (`BETWEEN d - 6 days AND d`), and count distinct users; summing daily distinct counts over a 7-row window is wrong because one user active on three days is counted three times.

**Schema and sample data:** (assumption: "trailing 7 days including that day" means the day itself and the six days before it; the data runs 2025-03-01 to 2025-03-14, with no events at all on 03-04, 03-07 and 03-11. The seed has 6 users and several rows per user per day.)
```sql
CREATE TABLE events(user_id INTEGER, event_date TEXT);
INSERT INTO events VALUES
 (1,'2025-03-01'),(1,'2025-03-01'),(1,'2025-03-02'),(1,'2025-03-08'),(1,'2025-03-09'),
 (2,'2025-03-01'),(2,'2025-03-03'),
 (3,'2025-03-02'),(3,'2025-03-02'),(3,'2025-03-12'),
 (4,'2025-03-05'),(4,'2025-03-06'),(4,'2025-03-06'),(4,'2025-03-13'),
 (5,'2025-03-09'),(5,'2025-03-14'),
 (6,'2025-03-10');
```

**SQL answer:** `sql` in the Code block: a recursive CTE `spine(d)` from 2025-03-07 to 2025-03-14, a `LEFT JOIN` to `events` on `event_date BETWEEN date(s.d, '-6 days') AND s.d`, `COUNT(DISTINCT e.user_id)` grouped by `s.d`. `wrong` is the 7-row-window version, shown for contrast.

**pandas answer:** the Code block builds the spine with `pd.date_range`, does a `cross` merge with the events, keeps rows with `day - 6 days <= event_date <= day`, then `groupby('day')['user_id'].nunique()`, reindexed to the spine with `fill_value=0` so a day with an empty window would still show 0.

**Example:** by hand, the window for 03-07 is 03-01 to 03-07. Users with an event in it: 1 (03-01, 03-02), 2 (03-01, 03-03), 3 (03-02), 4 (03-05, 03-06). Users 5 and 6 are later. That is 4. The window for 03-12 is 03-06 to 03-12: user 4 (03-06), user 1 (03-08, 03-09), user 5 (03-09), user 6 (03-10), user 3 (03-12) gives 5. User 2's last event is on 03-03, so they drop out from 03-10 onward.

**Code:** run with `python3 -I`.
```python
# Q15: trailing 7-day distinct active users with a date spine
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE events(user_id INTEGER, event_date TEXT);
INSERT INTO events VALUES
 (1,'2025-03-01'),(1,'2025-03-01'),(1,'2025-03-02'),(1,'2025-03-08'),(1,'2025-03-09'),
 (2,'2025-03-01'),(2,'2025-03-03'),
 (3,'2025-03-02'),(3,'2025-03-02'),(3,'2025-03-12'),
 (4,'2025-03-05'),(4,'2025-03-06'),(4,'2025-03-06'),(4,'2025-03-13'),
 (5,'2025-03-09'),(5,'2025-03-14'),
 (6,'2025-03-10');
""")
sql = """
WITH RECURSIVE spine(d) AS (
  SELECT '2025-03-07' UNION ALL SELECT date(d, '+1 day') FROM spine WHERE d < '2025-03-14')
SELECT s.d AS day, COUNT(DISTINCT e.user_id) AS active_7d
FROM spine s LEFT JOIN events e ON e.event_date BETWEEN date(s.d, '-6 days') AND s.d
GROUP BY s.d ORDER BY s.d
"""
a = pd.read_sql(sql, con)
print("SQL"); print(a.to_string(index=False))

# the plain 7-row window on daily distinct counts: sums users more than once
wrong = """
WITH RECURSIVE spine(d) AS (
  SELECT '2025-03-01' UNION ALL SELECT date(d, '+1 day') FROM spine WHERE d < '2025-03-14'),
daily AS (SELECT s.d, COUNT(DISTINCT e.user_id) AS dau FROM spine s LEFT JOIN events e ON e.event_date = s.d GROUP BY s.d),
daily_nospine AS (SELECT event_date AS d, COUNT(DISTINCT user_id) AS dau FROM events GROUP BY event_date)
SELECT x.d AS day, x.w_spine, y.w_nospine FROM
 (SELECT d, SUM(dau) OVER (ORDER BY d ROWS 6 PRECEDING) AS w_spine FROM daily) x
 LEFT JOIN (SELECT d, SUM(dau) OVER (ORDER BY d ROWS 6 PRECEDING) AS w_nospine FROM daily_nospine) y ON y.d = x.d
WHERE x.d >= '2025-03-07' ORDER BY x.d
"""
w = pd.read_sql(wrong, con)
print("\nwrong windows (sum of daily distinct counts; w_nospine is NULL on days that have no events, 03-07 and 03-11, because that table has no row for them)")
print(w.to_string(index=False))

ev = pd.read_sql("SELECT * FROM events", con)
ev["event_date"] = pd.to_datetime(ev.event_date)
spine = pd.DataFrame({"day": pd.date_range("2025-03-07", "2025-03-14")})
m = spine.merge(ev, how="cross")
m = m[(m.event_date >= m.day - pd.Timedelta(days=6)) & (m.event_date <= m.day)]
cnt = m.groupby("day")["user_id"].nunique().reindex(spine.day, fill_value=0)
p = cnt.rename("active_7d").reset_index()
p["day"] = p.day.dt.strftime("%Y-%m-%d")
print("\npandas"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(a, p, check_dtype=False)
print("\nassert passed: equal, rows in day order")
```

**Output (my run):**
```text
SQL
       day  active_7d
2025-03-07          4
2025-03-08          4
2025-03-09          4
2025-03-10          4
2025-03-11          4
2025-03-12          5
2025-03-13          5
2025-03-14          5

wrong windows (sum of daily distinct counts; w_nospine is NULL on days that have no events, 03-07 and 03-11, because that table has no row for them)
       day  w_spine  w_nospine
2025-03-07        7        NaN
2025-03-08        6        8.0
2025-03-09        6       10.0
2025-03-10        6        9.0
2025-03-11        6        NaN
2025-03-12        6        8.0
2025-03-13        6        8.0
2025-03-14        7        8.0

pandas
       day  active_7d
2025-03-07          4
2025-03-08          4
2025-03-09          4
2025-03-10          4
2025-03-11          4
2025-03-12          5
2025-03-13          5
2025-03-14          5

assert passed: equal, rows in day order
```

**Edge cases:**
- **Days with no events (03-07 and 03-11 are the ones in the answer range):** the spine keeps them. A query that groups the events by day has no row for them, so it silently skips the day. Here the window of 03-11 (03-05 to 03-11) still has 4 active users.
- **Several rows per user per day:** `COUNT(DISTINCT user_id)` handles them; `COUNT(*)` would count events.
- **Empty window:** with a `LEFT JOIN` a spine day with no events in its window shows 0, because `COUNT(DISTINCT NULL)` is 0. In pandas the `reindex(fill_value=0)` does the same job.
- **First six days:** days 1 to 6 have partial windows, so the question asks only for day 7 onward; the events from 03-01 still feed day 7.
- **Dates as text:** `date(s.d, '-6 days')` returns an ISO string that compares correctly with the stored dates.

**Then explain:**
- **Why a 7-row window is wrong:** it adds up daily distinct counts. In the output the `w_spine` column (7-row sum with a full spine) shows 6 or 7 on days where the true 7-day distinct count is 4 or 5, because user 1 is counted on each day they were active. Distinct counts cannot be added across days; you need the distinct count of the union.
- **A 7-row window without a spine is wrong in a second way:** the frame is 7 *rows*, not 7 *days*; with missing days it reaches back further (`w_nospine`, 8 to 10 here), and the days without events have no row at all (NULL in the `LEFT JOIN`).
- **Cost:** the range join compares each spine day with up to 7 days of events; fine for a metric table, but at scale people keep a daily "user activity" table (user, day) first, then join that.
- **Dialects (not executed here):** PostgreSQL would build the spine with `generate_series`, BigQuery with `GENERATE_DATE_ARRAY`, and most engines do not allow `COUNT(DISTINCT ...)` as a window function (PostgreSQL rejects it, from memory), which is why the range join is the portable answer. SQLite does not allow it either.
- **Scoring note (Set F1, Q4 of 5, 25 pts):** about 10 points for the eight right counts (4, 4, 4, 4, 4, 5, 5, 5), 5 for the spine and the days-with-no-events handling, 5 for pandas asserted equal, 2.5 for stating that the window is the day plus six earlier days, 2.5 for the "why not a 7-row window" sentence (or a check that the metric never exceeds total distinct users, 6). Giving the 7-row-window numbers earns partial credit only.

**Follow-ups:**
- *Weekly and monthly actives together (WAU, MAU)?* Same pattern with `-6 days` and `-29 days`; stickiness is DAU divided by MAU (Part 8).
- *How do you make it incremental?* Keep a table of (user, last_active_date) and count users whose last active date falls in the window; this only works for the "active in window" count, not for retention-style questions.
- *What does it cost?* A (user_id, event_date) index (Part 11) lets each window read a range.

**Common mistakes:**
- Summing daily distinct counts.
- `ROWS 6 PRECEDING` on a table with missing days.
- Counting rows instead of distinct users.
- Off-by-one: using `-7 days` (an 8-day window).
- Starting the spine at day 1 and then reporting the partial windows of days 1 to 6.

### Q16 ⭐⭐⭐ 🔴 [Set F2, Q4 of 5, 12 min, 25 pts] Longest daily streak (Google-style engagement). searches(user_id, search_ts TEXT) with several searches per day. Return per user the longest run of consecutive calendar days with at least one search, with the run start and end, ties broken by the earlier run (Part 7 Q6 and Q7, and the duplicate-days trap of Part 7 Q8). Seed 5 users including one with a one-day gap and one with 3 searches on the same day. SQL (date minus ROW_NUMBER) and pandas, asserting equal.
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Reduce searches to distinct (user, day), number each user's days with `ROW_NUMBER`, subtract that number of days from the date so every consecutive run shares one constant, group by that constant to get run start, end and length, and keep the longest run per user, earliest first on ties.

**Schema and sample data:** (assumption: a day counts if it has at least one search; the calendar day is the first 10 characters of the timestamp; a tie in length keeps the earlier run.)
```sql
CREATE TABLE searches(user_id INTEGER, search_ts TEXT);
INSERT INTO searches VALUES
 (1,'2025-03-01 09:00:00'),(1,'2025-03-02 09:00:00'),(1,'2025-03-02 12:30:00'),(1,'2025-03-02 23:59:59'),(1,'2025-03-03 08:00:00'),(1,'2025-03-05 10:00:00'),(1,'2025-03-06 10:00:00'),
 (2,'2025-03-01 09:00:00'),(2,'2025-03-02 09:00:00'),(2,'2025-03-04 09:00:00'),(2,'2025-03-05 09:00:00'),(2,'2025-03-06 09:00:00'),
 (3,'2025-03-07 10:00:00'),
 (4,'2025-03-01 09:00:00'),(4,'2025-03-02 09:00:00'),(4,'2025-03-10 09:00:00'),(4,'2025-03-11 09:00:00'),
 (5,'2025-01-30 20:00:00'),(5,'2025-01-31 20:00:00'),(5,'2025-02-01 20:00:00');
```

**SQL answer:** `sql` in the Code block: `days` (distinct user and day), `g` (the group key `date(d, '-' || (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY d) - 1) || ' days')`), `runs` (MIN, MAX and COUNT per group), and `best` (`ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY days DESC, run_start ASC)`, keep `rn = 1`). SQLite cannot subtract an integer from a date, so the shift is written as a `date(..., '-n days')` modifier; the idea "date minus row number" is the same. The `raw` query is the version without the distinct-days step.

**pandas answer:** the Code block drops duplicate (user, day) pairs, sorts, marks a new run where the gap to the previous day is not exactly one day (`diff().ne(pd.Timedelta(days=1))`, which is also true for the first day of each user), runs a `cumsum` per user to make the run id, aggregates start, end and size, then sorts by `days` descending and `run_start` ascending and keeps the first row per user.

**Example:** by hand.
- User 1: searches on 03-01, 03-02 (three searches that day), 03-03, then 03-05 and 03-06. Distinct days: 1, 2, 3, 5, 6. Runs: 03-01 to 03-03 (3 days) and 03-05 to 03-06 (2 days). Best: 03-01 to 03-03.
- User 2: 03-01, 03-02, then a gap on 03-03, then 03-04, 03-05, 03-06. Runs of 2 and 3; best is 03-04 to 03-06.
- User 3: one day, 03-07: run of 1.
- User 4: 03-01 and 03-02, then 03-10 and 03-11. Two runs of length 2: the earlier one wins, 03-01 to 03-02.
- User 5: 01-30, 01-31, 02-01: one run of 3 across the month end.

**Code:** run with `python3 -I`.
```python
# Q16: longest daily streak per user with start and end, tie -> earlier run
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE searches(user_id INTEGER, search_ts TEXT);
INSERT INTO searches VALUES
 (1,'2025-03-01 09:00:00'),(1,'2025-03-02 09:00:00'),(1,'2025-03-02 12:30:00'),(1,'2025-03-02 23:59:59'),(1,'2025-03-03 08:00:00'),(1,'2025-03-05 10:00:00'),(1,'2025-03-06 10:00:00'),
 (2,'2025-03-01 09:00:00'),(2,'2025-03-02 09:00:00'),(2,'2025-03-04 09:00:00'),(2,'2025-03-05 09:00:00'),(2,'2025-03-06 09:00:00'),
 (3,'2025-03-07 10:00:00'),
 (4,'2025-03-01 09:00:00'),(4,'2025-03-02 09:00:00'),(4,'2025-03-10 09:00:00'),(4,'2025-03-11 09:00:00'),
 (5,'2025-01-30 20:00:00'),(5,'2025-01-31 20:00:00'),(5,'2025-02-01 20:00:00');
""")
sql = """
WITH days AS (SELECT DISTINCT user_id, date(search_ts) AS d FROM searches),
g AS (SELECT user_id, d, date(d, '-' || (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY d) - 1) || ' days') AS grp FROM days),
runs AS (SELECT user_id, MIN(d) AS run_start, MAX(d) AS run_end, COUNT(*) AS days FROM g GROUP BY user_id, grp),
best AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY days DESC, run_start ASC) AS rn FROM runs)
SELECT user_id, run_start, run_end, days FROM best WHERE rn = 1 ORDER BY user_id
"""
a = pd.read_sql(sql, con)
print("SQL"); print(a.to_string(index=False))
raw = """
WITH g AS (SELECT date(search_ts) AS d,
  date(date(search_ts), '-' || (ROW_NUMBER() OVER (ORDER BY search_ts) - 1) || ' days') AS grp
  FROM searches WHERE user_id = 1)
SELECT MIN(d) AS run_start, MAX(d) AS run_end, COUNT(*) AS n FROM g GROUP BY grp ORDER BY run_start
"""
print("\nuser 1 without the DISTINCT-days step (row numbers over raw rows): the 3 searches on 03-02 split the run")
print(pd.read_sql(raw, con).to_string(index=False))

s = pd.read_sql("SELECT * FROM searches", con)
s["d"] = pd.to_datetime(s.search_ts.str[:10])
dd = s[["user_id", "d"]].drop_duplicates().sort_values(["user_id", "d"])
dd["new_run"] = dd.groupby("user_id")["d"].diff().ne(pd.Timedelta(days=1))
dd["grp"] = dd.groupby("user_id")["new_run"].cumsum()
runs = dd.groupby(["user_id", "grp"]).agg(run_start=("d", "min"), run_end=("d", "max"), days=("d", "size")).reset_index()
best = runs.sort_values(["user_id", "days", "run_start"], ascending=[True, False, True]).drop_duplicates("user_id")
p = best[["user_id", "run_start", "run_end", "days"]].sort_values("user_id").reset_index(drop=True)
p["run_start"] = p.run_start.dt.strftime("%Y-%m-%d"); p["run_end"] = p.run_end.dt.strftime("%Y-%m-%d")
print("\npandas"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(a, p, check_dtype=False)
print("\nassert passed: equal, rows ordered by user_id")
```

**Output (my run):**
```text
SQL
 user_id  run_start    run_end  days
       1 2025-03-01 2025-03-03     3
       2 2025-03-04 2025-03-06     3
       3 2025-03-07 2025-03-07     1
       4 2025-03-01 2025-03-02     2
       5 2025-01-30 2025-02-01     3

user 1 without the DISTINCT-days step (row numbers over raw rows): the 3 searches on 03-02 split the run
 run_start    run_end  n
2025-03-01 2025-03-02  2
2025-03-02 2025-03-03  2
2025-03-02 2025-03-06  3

pandas
 user_id  run_start    run_end  days
       1 2025-03-01 2025-03-03     3
       2 2025-03-04 2025-03-06     3
       3 2025-03-07 2025-03-07     1
       4 2025-03-01 2025-03-02     2
       5 2025-01-30 2025-02-01     3

assert passed: equal, rows ordered by user_id
```

**Edge cases:**
- **Several searches on one day (user 1, 03-02):** without the `DISTINCT` day step the row numbers advance faster than the dates. The second printed table shows what happens to user 1: the runs come out as 03-01 to 03-02 (2 rows), 03-02 to 03-03 (2 rows) and an absurd 03-02 to 03-06 (3 rows) that bridges the real gap on 03-04. This is the duplicate-days trap of Part 7 Q8.
- **A one-day gap (user 2):** splits the run; the answer comes from the second run.
- **Tie (user 4):** broken by the earlier start through `run_start ASC`.
- **Single day (user 3):** a run of length 1 is still a run.
- **Month and year boundaries (user 5):** date arithmetic handles them; do not compare day-of-month numbers.
- **Time zones:** `search_ts` is taken as one zone. A "calendar day" in the user's zone needs the conversion before `date()`. Not run here.
- **Users with no searches:** no row; add a `LEFT JOIN` from `users` if they must appear.

**Then explain:**
- **Why the trick works:** within a run of consecutive days, the day number and the row number rise together, so their difference is constant; a gap makes the day jump while the row number goes up by one, changing the constant.
- **pandas vs SQL:** both use the same idea; pandas `cumsum` of "starts a new run" is the common alternative to subtracting a row number.
- **Dialects (not executed here):** from memory, PostgreSQL can subtract an integer from a date directly (`d - (ROW_NUMBER() OVER (...))::int`); MySQL uses `DATE_SUB(d, INTERVAL n DAY)`; the `ROW_NUMBER` tie rule is standard.
- **Scoring note (Set F2, Q4 of 5, 25 pts):** about 10 points for the five right run rows, 5 for the seeded edge cases (the same-day duplicates handled by distinct days, the tie rule, the month crossing), 5 for pandas asserted equal, 2.5 for stating "day counts if at least one search" and the tie rule, 2.5 for a check such as "the run length never exceeds the user's number of distinct days". Counting search rows instead of days is the usual way to lose most points here.

**Follow-ups:**
- *Current streak as of today?* Keep only the run whose end is the as-of date (or the day before); everything else is a broken streak.
- *All users' longest streak overall?* Take the maximum of `days` from `runs`, with ties listed.
- *Streak that allows one missed day?* Use a gap threshold of 2 days (`diff <= 2`) in pandas, or a `LAG` flag in SQL; that is an islands variation (Part 7).

**Common mistakes:**
- Using `ROW_NUMBER` over raw searches instead of distinct days.
- Comparing `search_ts` strings instead of days, so two searches on one day look like different days.
- Breaking ties arbitrarily (no second order key) so the answer changes between runs.
- Forgetting that the `DENSE_RANK` or `ROW_NUMBER` order must be by day, not by user.

### Q17 ⭐⭐ 🟡 [Set F1, Q3 of 5, 8 min, 20 pts] Top 2 posters per country with ties (Meta-style). users(user_id, country), posts(post_id, user_id, created_at). Return the users whose post count in March 2025 is within the top 2 distinct counts of their country (dense rank, ties all kept, Part 4 Q4 and Q45). Seed 8 users in 3 countries with a three-way tie and a user with zero posts (excluded). SQL and pandas, order by country, count descending, user_id.
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Count each user's March posts, then `DENSE_RANK()` those counts per country in descending order and keep rank 1 and 2: dense rank means ties share a rank and no rank number is skipped, so a three-way tie for second place keeps all three.

**Schema and sample data:** (assumptions: March means `created_at >= '2025-03-01'` and `< '2025-04-01'`, a half-open range that also catches a post at 23:59:59 on 03-31 and excludes one at 00:00:00 on 04-01; users with no March post are not ranked.) The 24 post rows are generated in the Code block from per-user counts, shown here as a table; the `users` rows are literal.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, country TEXT);
CREATE TABLE posts(post_id INTEGER PRIMARY KEY, user_id INTEGER, created_at TEXT);
INSERT INTO users VALUES (1,'IN'),(2,'IN'),(3,'IN'),(4,'IN'),(5,'IN'),(6,'US'),(7,'US'),(8,'UK');
```
| user_id | country | posts in March | other posts |
|---|---|---|---|
| 1 | IN | 5 | none |
| 2 | IN | 3 | none |
| 3 | IN | 3 | none |
| 4 | IN | 3 (the last one at 2025-03-31 23:59:59) | none |
| 5 | IN | 1 | 2 in February |
| 6 | US | 4 | none |
| 7 | US | 2 | 1 at 2025-04-01 00:00:00 |
| 8 | UK | 0 | none |

**SQL answer:** `sql` in the Code block: CTE `c` counts March posts per (country, user), CTE `r` adds `DENSE_RANK() OVER (PARTITION BY country ORDER BY posts DESC)`, and the final `SELECT` keeps `rk <= 2` ordered by country, posts descending, user_id.

**pandas answer:** filter the posts to March with two string comparisons, merge with `users`, `groupby(['country', 'user_id']).size()`, then `groupby('country')['posts'].rank(method='dense', ascending=False)` and keep `rk <= 2`.

**Example:** by hand, India has March counts 5 (user 1), 3, 3, 3 (users 2, 3, 4) and 1 (user 5). Distinct counts in descending order: 5, 3, 1. Dense ranks: 1, 2, 2, 2, 3. Rank 3 is dropped, so IN keeps users 1, 2, 3, 4. US has 4 and 2: ranks 1 and 2, both kept. UK has no March posts, so no row. Total 6 rows.

**Code:** run with `python3 -I`.
```python
# Q17: users within the top 2 DISTINCT post counts of their country, March 2025
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE users(user_id INTEGER PRIMARY KEY, country TEXT);
CREATE TABLE posts(post_id INTEGER PRIMARY KEY, user_id INTEGER, created_at TEXT);
INSERT INTO users VALUES (1,'IN'),(2,'IN'),(3,'IN'),(4,'IN'),(5,'IN'),(6,'US'),(7,'US'),(8,'UK');
""")
rows = []
pid = 0
def add(u, n, ts):
    global pid
    for _ in range(n):
        pid += 1
        rows.append((pid, u, ts))
add(1, 5, "2025-03-10 10:00:00"); add(2, 3, "2025-03-11 10:00:00"); add(3, 3, "2025-03-12 10:00:00"); add(4, 3, "2025-03-31 23:59:59")
add(5, 1, "2025-03-05 10:00:00"); add(5, 2, "2025-02-27 10:00:00")
add(6, 4, "2025-03-02 10:00:00"); add(7, 2, "2025-03-03 10:00:00"); add(7, 1, "2025-04-01 00:00:00")
con.executemany("INSERT INTO posts VALUES (?,?,?)", rows)

sql = """
WITH c AS (
  SELECT u.country, u.user_id, COUNT(*) AS posts
  FROM users u JOIN posts p ON p.user_id = u.user_id
  WHERE p.created_at >= '2025-03-01' AND p.created_at < '2025-04-01'
  GROUP BY u.country, u.user_id),
r AS (SELECT *, DENSE_RANK() OVER (PARTITION BY country ORDER BY posts DESC) AS rk FROM c)
SELECT country, user_id, posts, rk FROM r WHERE rk <= 2 ORDER BY country, posts DESC, user_id
"""
a = pd.read_sql(sql, con)
print("SQL"); print(a.to_string(index=False))
print("\nwith ROW_NUMBER instead of DENSE_RANK the kept (country, user_id) would be:",
      [(r[0], r[1]) for r in con.execute(sql.replace("DENSE_RANK()", "ROW_NUMBER()"))])

u = pd.read_sql("SELECT * FROM users", con); po = pd.read_sql("SELECT * FROM posts", con)
po = po[(po.created_at >= "2025-03-01") & (po.created_at < "2025-04-01")]
c = u.merge(po, on="user_id").groupby(["country", "user_id"]).size().rename("posts").reset_index()
c["rk"] = c.groupby("country")["posts"].rank(method="dense", ascending=False).astype("int64")
p = c[c.rk <= 2].sort_values(["country", "posts", "user_id"], ascending=[True, False, True]).reset_index(drop=True)
print("\npandas"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(a, p, check_dtype=False)
print("\nassert passed: equal, rows ordered by country, posts desc, user_id")
```

**Output (my run):**
```text
SQL
country  user_id  posts  rk
     IN        1      5   1
     IN        2      3   2
     IN        3      3   2
     IN        4      3   2
     US        6      4   1
     US        7      2   2

with ROW_NUMBER instead of DENSE_RANK the kept (country, user_id) would be: [('IN', 1), ('IN', 2), ('US', 6), ('US', 7)]

pandas
country  user_id  posts  rk
     IN        1      5   1
     IN        2      3   2
     IN        3      3   2
     IN        4      3   2
     US        6      4   1
     US        7      2   2

assert passed: equal, rows ordered by country, posts desc, user_id
```

**Edge cases:**
- **Three-way tie for second (users 2, 3, 4):** all kept by `DENSE_RANK`. `ROW_NUMBER` would keep exactly one of them arbitrarily: the printed line starting `with ROW_NUMBER` shows `ROW_NUMBER` keeping only users 1 and 2 for IN, and silently dropping 3 and 4.
- **`RANK` instead of `DENSE_RANK`:** the ranks would be 1, 2, 2, 2 and then 5. For "top 2" the kept rows are the same here, but `RANK` and "top 2 distinct counts" differ when the tie is at rank 1: `RANK` would skip rank 2 and return only the tied leaders. That is why the prompt says dense.
- **Zero-post user (user 8):** never in the count CTE because of the inner join; UK is absent from the result. To show UK as empty, left-join from `users` and handle NULL.
- **Date boundaries:** user 5's February posts and user 7's 04-01 midnight post must not count; the half-open range handles the timestamp boundary, whereas `<= '2025-03-31'` would drop the 23:59:59 post of user 4.
- **Posts per user as the only measure:** the count is a row count; if a post could be duplicated (retries), count distinct `post_id` (not needed here, `post_id` is the key).

**Then explain:**
- **Dense rank on counts, not on users:** ranking distinct counts means "the two highest levels of activity" rather than "two people".
- **pandas:** `rank(method='dense', ascending=False)` returns floats; the Code block casts to int to compare with SQL's integer rank.
- **Dialects (not executed here):** `DENSE_RANK` is standard (PostgreSQL, MySQL 8, SQL Server, BigQuery, Snowflake); `QUALIFY DENSE_RANK() ... <= 2` on BigQuery or Snowflake saves the extra CTE (not executed).
- **Scoring note (Set F1, Q3 of 5, 20 pts):** about 8 points for the six right rows, 4 for the seeded edge cases (three-way tie kept, zero-post user excluded), 4 for pandas asserted equal, 2 for stating dense versus row rank and the March boundary, 2 for a check (every kept user has posts, counts descend within a country). Using `ROW_NUMBER` or `LIMIT 2` per country is a wrong answer here, not a style choice.

**Follow-ups:**
- *Include countries with no posters as an empty row?* Left join from distinct countries and accept NULL user.
- *Top 2 per country per month?* Add the month to the grouping and partition; the code shape is the same.
- *What if you also need the rank of ties to be broken by earliest post?* Add `MIN(created_at)` as a secondary order key and use `ROW_NUMBER`, but that changes the question to "exactly two people".

**Common mistakes:**
- `ROW_NUMBER` or `LIMIT` and losing tied users.
- Filtering the rank in the same `SELECT` (window results are not available in `WHERE`).
- `<= '2025-03-31'` on a timestamp column.
- Ranking before filtering to March.

### Q18 ⭐⭐ 🟡 [Set F1, Q2 of 5, 8 min, 20 pts] Day-1 retention by signup date (Part 6 Q12, Q13). users(user_id, signup_date) and logins(user_id, login_date). For each signup date return signups, users who logged in exactly the next calendar day, and the rate rounded to 2 decimals; a signup date with zero retained users must still show 0.00. Seed 9 users over 3 days including a user who logs in two days after only and a user with duplicate login rows. SQL and pandas.
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** For each signup date count distinct signups and count distinct users who have a login dated exactly signup date plus one day, with a `LEFT JOIN` to the logins and `COUNT(DISTINCT CASE ...)` so duplicate login rows are harmless and a date with nobody retained still appears with 0.00.
 
**Schema and sample data:** (assumption: day 1 means the next calendar day only; logging in on the signup day or two days later does not count; the rate is retained users divided by all users who signed up that day, and it is rounded to 2 decimals.)
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT);
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO users VALUES (1,'2025-03-01'),(2,'2025-03-01'),(3,'2025-03-01'),
                         (4,'2025-03-02'),(5,'2025-03-02'),(6,'2025-03-02'),
                         (7,'2025-03-03'),(8,'2025-03-03'),(9,'2025-03-03');
INSERT INTO logins VALUES (1,'2025-03-02'),(1,'2025-03-02'),(2,'2025-03-03'),(3,'2025-03-02'),
                          (4,'2025-03-03'),(6,'2025-03-09'),
                          (7,'2025-03-05'),(9,'2025-03-03');
```

**SQL answer:** `sql` in the Code block: `FROM users u LEFT JOIN logins l ON l.user_id = u.user_id`, grouped by `signup_date`, with `COUNT(DISTINCT u.user_id)` for signups, `COUNT(DISTINCT CASE WHEN l.login_date = date(u.signup_date, '+1 day') THEN u.user_id END)` for retained, and `ROUND(1.0 * retained / signups, 2)` for the rate (the printout formats it with two decimals).

**pandas answer:** compute `next_day` for each user, merge with the de-duplicated logins on `(user_id, next_day = login_date)`, mark users found, then `groupby('signup_date').agg(signups=('user_id', 'nunique'), retained=('retained', 'sum'))` and `(retained / signups).round(2)`.

**Example:** by hand.
- Signup 03-01 (users 1, 2, 3): user 1 logs in on 03-02, twice (one retained user, not two); user 2 logs in only on 03-03 (two days later, not retained); user 3 logs in on 03-02. Retained 2 of 3: 0.67.
- Signup 03-02 (users 4, 5, 6): user 4 logs in on 03-03 (retained); user 5 never logs in; user 6 logs in only on 03-09. Retained 1 of 3: 0.33.
- Signup 03-03 (users 7, 8, 9): user 7 logs in on 03-05 (two days later), user 8 never, user 9 logs in on 03-03 itself (same day). None on 03-04, so 0 of 3: 0.00.

**Code:** run with `python3 -I`.
```python
# Q18: day-1 retention by signup date, 0.00 kept
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT);
CREATE TABLE logins(user_id INTEGER, login_date TEXT);
INSERT INTO users VALUES (1,'2025-03-01'),(2,'2025-03-01'),(3,'2025-03-01'),
                         (4,'2025-03-02'),(5,'2025-03-02'),(6,'2025-03-02'),
                         (7,'2025-03-03'),(8,'2025-03-03'),(9,'2025-03-03');
INSERT INTO logins VALUES (1,'2025-03-02'),(1,'2025-03-02'),(2,'2025-03-03'),(3,'2025-03-02'),
                          (4,'2025-03-03'),(6,'2025-03-09'),
                          (7,'2025-03-05'),(9,'2025-03-03');
""")
sql = """
SELECT u.signup_date,
       COUNT(DISTINCT u.user_id) AS signups,
       COUNT(DISTINCT CASE WHEN l.login_date = date(u.signup_date, '+1 day') THEN u.user_id END) AS retained,
       ROUND(1.0 * COUNT(DISTINCT CASE WHEN l.login_date = date(u.signup_date, '+1 day') THEN u.user_id END)
             / COUNT(DISTINCT u.user_id), 2) AS rate
FROM users u LEFT JOIN logins l ON l.user_id = u.user_id
GROUP BY u.signup_date ORDER BY u.signup_date
"""
a = pd.read_sql(sql, con)
print("SQL"); print(a.assign(rate=a.rate.map("{:.2f}".format)).to_string(index=False))
print("\nwithout DISTINCT, COUNT(*) of the joined rows for 2025-03-01 gives:",
      con.execute("SELECT COUNT(*) FROM users u JOIN logins l ON l.user_id=u.user_id AND l.login_date=date(u.signup_date,'+1 day') WHERE u.signup_date='2025-03-01'").fetchone()[0],
      "retained (user 1 has two login rows)")

u = pd.read_sql("SELECT * FROM users", con); lg = pd.read_sql("SELECT * FROM logins", con)
u["next_day"] = (pd.to_datetime(u.signup_date) + pd.Timedelta(days=1)).dt.strftime("%Y-%m-%d")
hit = u.merge(lg.drop_duplicates(), left_on=["user_id", "next_day"], right_on=["user_id", "login_date"])
u["retained"] = u.user_id.isin(hit.user_id)
p = u.groupby("signup_date").agg(signups=("user_id", "nunique"), retained=("retained", "sum")).reset_index()
p["rate"] = (p.retained / p.signups).round(2)
print("\npandas"); print(p.assign(rate=p.rate.map("{:.2f}".format)).to_string(index=False))
pd.testing.assert_frame_equal(a, p, check_dtype=False)
print("\nassert passed: equal, rows ordered by signup_date")
```

**Output (my run):**
```text
SQL
signup_date  signups  retained rate
 2025-03-01        3         2 0.67
 2025-03-02        3         1 0.33
 2025-03-03        3         0 0.00

without DISTINCT, COUNT(*) of the joined rows for 2025-03-01 gives: 3 retained (user 1 has two login rows)

pandas
signup_date  signups  retained rate
 2025-03-01        3         2 0.67
 2025-03-02        3         1 0.33
 2025-03-03        3         0 0.00

assert passed: equal, rows ordered by signup_date
```

**Edge cases:**
- **Duplicate login rows (user 1):** `COUNT(DISTINCT ...)` and `drop_duplicates()` collapse them. A plain count of joined rows gives 3 "retained" for 03-01 in the second printed line, instead of the true 2, and a rate above the truth.
- **Zero retained (03-03):** the date still appears because the denominator side comes from `users` and the `LEFT JOIN` keeps users with no logins; `COUNT(DISTINCT CASE ...)` returns 0, not NULL.
- **Users who never log in (users 5 and 8):** kept by the `LEFT JOIN`; their `login_date` is NULL, the comparison is not true, the `CASE` gives NULL, and `COUNT` ignores it.
- **Same-day logins (user 9) and day 2 logins (users 2, 7):** not day 1 by definition.
- **Matching the rule exactly:** a `login_date` compared with `date(signup_date, '+1 day')` works because both are `YYYY-MM-DD` text; with timestamps, take `date()` of the login first.
- **Immature cohorts:** if the latest signup date has not yet had its next day in the data, its rate is understated; mark or drop it in a real report (here the data covers up to 03-09).
- **Printing 0.00:** SQLite's `ROUND` returns the number 0.0; the two-decimal text is a formatting step (done in the printout).

**Then explain:**
- **Why a LEFT JOIN from users:** an inner join to logins would drop users who never came back and inflate the rate (and drop the 0.00 row).
- **Rounding:** `ROUND(2/3, 2)` is 0.67 in both engines. Rounding of exact halves can differ (SQLite and pandas disagree on, for example, 703.125, see Part 10), so keep the raw ratio if you need to compare cohorts.
- **Dialects (not executed here):** PostgreSQL would write `u.signup_date + 1` (date plus integer) and MySQL `DATE_ADD(u.signup_date, INTERVAL 1 DAY)`; `COUNT(DISTINCT CASE ...)` works in both.
- **Scoring note (Set F1, Q2 of 5, 20 pts):** about 8 points for the three right rows (0.67, 0.33, 0.00), 4 for the seeded edge cases (duplicate logins, the zero-retention date), 4 for pandas asserted equal, 2 for stating the day-1 definition and denominator, 2 for a check (retained never exceeds signups; signups add up to 9).

**Follow-ups:**
- *Day 7 retention?* Replace `+1 day` with `+7 days` (exactly day 7), or use a range if the product defines "within 7 days"; say which.
- *Retention by cohort week?* Group by week of signup; keep the same denominators.
- *Why did the number differ from the dashboard?* Check the definition (next day versus within a day), time zones, duplicate rows and whether test users are filtered.

**Common mistakes:**
- Counting login rows rather than distinct users.
- Using `INNER JOIN` and losing the cohort with no retention.
- Using `BETWEEN signup_date AND signup_date + 1` (includes day 0).
- Dividing by users who logged in at all, not by all signups.

### Q19 ⭐⭐ 🟡 [Set F2, Q3 of 5, 8 min, 20 pts] Sessions per user (Google-style). events(user_id, event_ts) and a 30-minute inactivity timeout; a gap of exactly 30 minutes starts a new session (Part 7 Q11, Q12). Return per user the session count and average events per session. Seed 3 users with a boundary gap exactly 30:00 and one with a single event. SQL (LAG then cumulative flag) and pandas (diff, gt, cumsum). Assert equal; state the rounding of the average.
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Order each user's events by time, take the gap to the previous event in whole seconds, flag a new session when there is no previous event or the gap is at least 1800 seconds, take a running sum of the flags as the session id, then count sessions and events per user.

**Schema and sample data:** (assumption: timeout rule = a gap of 30:00 or more starts a new session, so exactly 30:00 is a new session and 29:59 is not; the average is events (rows) per session, rounded to 2 decimals; duplicate timestamps count as separate events.)
```sql
CREATE TABLE events(user_id INTEGER, event_ts TEXT);
INSERT INTO events VALUES
 (1,'2025-03-01 09:00:00'),(1,'2025-03-01 09:10:00'),(1,'2025-03-01 09:40:00'),(1,'2025-03-01 09:50:00'),(1,'2025-03-01 10:30:00'),
 (2,'2025-03-01 10:00:00'),(2,'2025-03-01 10:00:00'),(2,'2025-03-01 10:29:59'),(2,'2025-03-01 11:00:00'),
 (3,'2025-03-01 12:00:00');
```

**SQL answer:** `sql` in the Code block: `l` computes the gap with `strftime('%s', event_ts) - strftime('%s', LAG(event_ts) OVER (PARTITION BY user_id ORDER BY event_ts))` (whole seconds, so there is no floating point rounding at the boundary), `f` makes the flag, `s` runs `SUM(new_sess) OVER (... ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`, `per` counts events per session, and the final query counts sessions and averages.

**pandas answer:** sort by user and time, `gap = groupby('user_id')['ts'].diff()`, `new_sess = gap.isna() | (gap >= pd.Timedelta(minutes=30))`, `groupby('user_id')['new_sess'].cumsum()` for the session id, then size per (user, session) and aggregate.

**Example:** by hand.
- User 1: 09:00, 09:10 (gap 10 min, same session), 09:40 (gap exactly 30:00, new session), 09:50 (10 min, same), 10:30 (40 min, new). Sessions: {09:00, 09:10}, {09:40, 09:50}, {10:30} = 3 sessions, 5 events, 5/3 = 1.67.
- User 2: 10:00, 10:00 (gap 0, same), 10:29:59 (29:59 after 10:00, same), 11:00:00 (30:01, new). Sessions: {3 events}, {1 event} = 2 sessions, 4 events, 2.00.
- User 3: one event: 1 session, 1 event, 1.00.

**Code:** run with `python3 -I`.
```python
# Q19: sessions per user with a 30-minute timeout (a gap of exactly 30:00 starts a new session)
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE events(user_id INTEGER, event_ts TEXT);
INSERT INTO events VALUES
 (1,'2025-03-01 09:00:00'),(1,'2025-03-01 09:10:00'),(1,'2025-03-01 09:40:00'),(1,'2025-03-01 09:50:00'),(1,'2025-03-01 10:30:00'),
 (2,'2025-03-01 10:00:00'),(2,'2025-03-01 10:00:00'),(2,'2025-03-01 10:29:59'),(2,'2025-03-01 11:00:00'),
 (3,'2025-03-01 12:00:00');
""")
sql = """
WITH l AS (
  SELECT user_id, event_ts,
         strftime('%s', event_ts) - strftime('%s', LAG(event_ts) OVER (PARTITION BY user_id ORDER BY event_ts)) AS gap_s
  FROM events),
f AS (SELECT user_id, event_ts, CASE WHEN gap_s IS NULL OR gap_s >= 1800 THEN 1 ELSE 0 END AS new_sess FROM l),
s AS (SELECT user_id, SUM(new_sess) OVER (PARTITION BY user_id ORDER BY event_ts ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS sess FROM f),
per AS (SELECT user_id, sess, COUNT(*) AS n FROM s GROUP BY user_id, sess)
SELECT user_id, COUNT(*) AS sessions, SUM(n) AS events, ROUND(1.0 * SUM(n) / COUNT(*), 2) AS avg_events_per_session
FROM per GROUP BY user_id ORDER BY user_id
"""
a = pd.read_sql(sql, con)
print("SQL"); print(a.to_string(index=False))

e = pd.read_sql("SELECT * FROM events", con)
e["ts"] = pd.to_datetime(e.event_ts)
e = e.sort_values(["user_id", "ts"])
gap = e.groupby("user_id")["ts"].diff()
e["new_sess"] = gap.isna() | (gap >= pd.Timedelta(minutes=30))
e["sess"] = e.groupby("user_id")["new_sess"].cumsum()
per = e.groupby(["user_id", "sess"]).size().rename("n").reset_index()
p = per.groupby("user_id").agg(sessions=("sess", "size"), events=("n", "sum")).reset_index()
p["avg_events_per_session"] = (p.events / p.sessions).round(2)
print("\npandas"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(a, p, check_dtype=False)
print("\nassert passed: equal, rows ordered by user_id")

# boundary check: > 1800 instead of >= 1800 would merge user 1's second session into the first
print("\nif the rule were gap > 30 min (strict), user 1 would have",
      int(((gap.isna()) | (gap > pd.Timedelta(minutes=30)))[e.user_id == 1].groupby(e.user_id).sum().iloc[0]), "sessions")
```

**Output (my run):**
```text
SQL
 user_id  sessions  events  avg_events_per_session
       1         3       5                    1.67
       2         2       4                    2.00
       3         1       1                    1.00

pandas
 user_id  sessions  events  avg_events_per_session
       1         3       5                    1.67
       2         2       4                    2.00
       3         1       1                    1.00

assert passed: equal, rows ordered by user_id

if the rule were gap > 30 min (strict), user 1 would have 2 sessions
```

**Edge cases:**
- **Exactly 30:00 (user 1, 09:10 to 09:40):** counts as a new session because the test is `>= 1800`. The last line of the output shows that a strict `>` rule would give user 1 only 2 sessions. Say which rule you use; the prompt fixes it.
- **29:59 (user 2):** stays in the session.
- **Single event (user 3):** `LAG` is NULL, so the flag is 1; one session of one event.
- **Duplicate timestamps (user 2):** gap 0, same session; the `ROWS` frame (not the default `RANGE`) makes the running sum count each row once. With the default frame and `ORDER BY event_ts`, peers with the same timestamp would get the same running total, which here is harmless for the session id but would be wrong for any running count.
- **Out-of-order rows:** the window sorts them; sort first in pandas as well.
- **Events from several days:** a gap across midnight is handled the same way; sessions are not cut at midnight unless the product says so.
- **NULL timestamps:** would sort first and break the gap; filter them.

**Then explain:**
- **Why integer seconds:** `julianday` differences are floating point, so a boundary test such as `(julianday(b) - julianday(a)) * 1440 >= 30` is fragile at exactly 30:00 (I did not test whether it misfires on this data). Seconds from `strftime('%s', ...)` are integers, so the boundary is exact.
- **Average events per session:** total events divided by total sessions per user (not an average of per-day averages). Rounded half away from zero in SQLite's `ROUND` and to even in pandas, which only matters on exact halves; none occur in this data.
- **Dialects (not executed here):** PostgreSQL would compute the gap as `event_ts - LAG(event_ts) OVER (...) >= INTERVAL '30 minutes'` on timestamp columns; MySQL uses `TIMESTAMPDIFF(SECOND, prev, ts)`; BigQuery `TIMESTAMP_DIFF(ts, prev, SECOND)`.
- **Scoring note (Set F2, Q3 of 5, 20 pts):** about 8 points for the right sessions and averages on the seed, 4 for the boundary and single-event handling (30:00 is new, 29:59 is not), 4 for pandas asserted equal, 2 for stating the rule and rounding, 2 for a check (the events column sums to the table's row count, 10).

**Follow-ups:**
- *Session length and duration?* `MIN` and `MAX` of `event_ts` per session; single-event sessions have zero duration, so say how you treat them.
- *Also cap sessions at 4 hours?* Add a second flag when the time since the session start exceeds the cap; that is harder in plain SQL (it needs a recursive CTE), so mention it as a limit.
- *Why not a self join?* It is quadratic; `LAG` is one ordered pass.

**Common mistakes:**
- Using `>` instead of `>=` at the boundary.
- Float date arithmetic that misses the exact boundary.
- A default `RANGE` frame for the running flag.
- Averaging per-session counts incorrectly (average of averages).
- Forgetting the first event of each user (NULL gap).

### Q20 ⭐⭐ 🟡 [Set F2, Q2 of 5, 8 min, 20 pts] Second most searched term per category (Part 4 Q5, Q46). searches(search_id, category, term). Return the second highest distinct count of searches per category and the term(s) at that rank, showing categories with only one distinct count as NULL rather than dropping them. Seed 3 categories with a tie for the top, a tie for second and a category with a single term. SQL and pandas.
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Count searches per (category, term), `DENSE_RANK()` those counts per category in descending order, and `LEFT JOIN` the list of categories to the rows with rank 2, so a category with fewer than two distinct counts still appears, with NULL.

**Schema and sample data:** (assumption: "second most searched" means the second highest distinct count, so ties for first do not use up rank 2; terms tied at that count are all returned, one row each.) The 24 search rows are generated in the Code block from the counts below.
```sql
CREATE TABLE searches(search_id INTEGER PRIMARY KEY, category TEXT, term TEXT);
```
| category | term: searches |
|---|---|
| shoes | A: 5, B: 5, C: 3, D: 3, E: 1 |
| phones | X: 4, Y: 2 |
| books | novel: 3 |

**SQL answer:** `sql` in the Code block: `c` counts per (category, term), `r` adds `DENSE_RANK() OVER (PARTITION BY category ORDER BY n DESC)`, `cats` lists the distinct categories, and `cats LEFT JOIN r ON r.category = cats.category AND r.rk = 2` keeps every category. The condition `rk = 2` sits in `ON`, not in `WHERE`.

**pandas answer:** group and count, `rank(method='dense', ascending=False)` per category, take the rank-2 rows, and `merge(..., how='left')` them onto the unique categories.

**Example:** by hand.
- shoes: counts 5, 5, 3, 3, 1. Distinct counts: 5, 3, 1. Dense ranks: A and B are 1, C and D are 2, E is 3. Second highest distinct count = 3 and the terms are C and D (two rows).
- phones: X = 4 (rank 1), Y = 2 (rank 2): one row, (phones, 2, Y).
- books: one term, one distinct count, no rank 2: (books, NULL, NULL).
- A plain `LIMIT 1 OFFSET 1` or `ROW_NUMBER() = 2` over the terms would return one arbitrary term per category (for shoes, the second of the two tied leaders, B), not C and D, and nothing sensible for books.

**Code:** run with `python3 -I`.
```python
# Q20: second highest DISTINCT search count per category and the terms at that rank, NULL if none
import sqlite3
import pandas as pd

def norm(df):
    return df.astype(object).where(df.notna(), None)

con = sqlite3.connect(":memory:")
con.executescript("CREATE TABLE searches(search_id INTEGER PRIMARY KEY, category TEXT, term TEXT);")
rows = []
sid = 0
for cat, term, n in [("shoes", "A", 5), ("shoes", "B", 5), ("shoes", "C", 3), ("shoes", "D", 3), ("shoes", "E", 1),
                     ("phones", "X", 4), ("phones", "Y", 2), ("books", "novel", 3)]:
    for _ in range(n):
        sid += 1
        rows.append((sid, cat, term))
con.executemany("INSERT INTO searches VALUES (?,?,?)", rows)

sql = """
WITH c AS (SELECT category, term, COUNT(*) AS n FROM searches GROUP BY category, term),
r AS (SELECT *, DENSE_RANK() OVER (PARTITION BY category ORDER BY n DESC) AS rk FROM c),
cats AS (SELECT DISTINCT category FROM searches)
SELECT cats.category, r.n AS second_count, r.term
FROM cats LEFT JOIN r ON r.category = cats.category AND r.rk = 2
ORDER BY cats.category, r.term
"""
a = pd.read_sql(sql, con)
print("SQL"); print(a.to_string(index=False))
print("\ninner-join version (drops books):", [r[0] for r in con.execute(sql.replace("LEFT JOIN r ON r.category = cats.category AND r.rk = 2", "JOIN r ON r.category = cats.category AND r.rk = 2"))])

s = pd.read_sql("SELECT * FROM searches", con)
c = s.groupby(["category", "term"]).size().rename("n").reset_index()
c["rk"] = c.groupby("category")["n"].rank(method="dense", ascending=False)
cats = c[["category"]].drop_duplicates()
second = c[c.rk == 2][["category", "n", "term"]].rename(columns={"n": "second_count"})
p = cats.merge(second, on="category", how="left").sort_values(["category", "term"]).reset_index(drop=True)
print("\npandas"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(norm(a), norm(p), check_dtype=False)
print("\nassert passed: equal, rows ordered by category, term")
```

**Output (my run):**
```text
SQL
category  second_count term
   books           NaN  NaN
  phones           2.0    Y
   shoes           3.0    C
   shoes           3.0    D

inner-join version (drops books): ['phones', 'shoes', 'shoes']

pandas
category  second_count term
   books           NaN  NaN
  phones           2.0    Y
   shoes           3.0    C
   shoes           3.0    D

assert passed: equal, rows ordered by category, term
```

**Edge cases:**
- **Tie for the top (A, B):** dense rank keeps rank 2 for the next count (3), not skipping it; with `RANK` the next rank after two ties would be 3 and shoes would come back with nothing.
- **Tie for second (C, D):** both returned, two rows for shoes.
- **Single distinct count (books):** appears with NULL for count and term. The printed `inner-join version` line shows that an inner join silently drops books.
- **A category with several terms but all the same count:** also only one distinct count, so also NULL.
- **Order of output:** NULL term sorts first in SQLite ascending, last in some engines; the output here has one row for books so the order is not affected, but say it.
- **Empty table:** no categories, no rows.

**Then explain:**
- **Where the filter goes:** a `WHERE r.rk = 2` after the join would turn the left join into an inner join and drop books; the condition belongs in `ON`.
- **Dense vs plain rank for "second highest":** the same idea as the second highest salary question (Part 4 Q5 and Q46, the per-department version with NULL for a single distinct salary), with ties handled by rank on distinct values.
- **pandas detail:** `rank` returns floats; the comparison `rk == 2` works on them. The merged `second_count` is float with NaN, and the Code block compares after turning NaN and NULL into None.
- **Dialects (not executed here):** standard on PostgreSQL, MySQL 8, SQL Server, BigQuery and Snowflake; `QUALIFY` on BigQuery and Snowflake would shorten the rank filter (not executed).
- **Scoring note (Set F2, Q2 of 5, 20 pts):** about 8 points for the four right rows (shoes C and D, phones Y, books NULL), 4 for the seeded edge cases (both ties and the NULL category), 4 for pandas asserted equal, 2 for saying "second highest distinct count" and why it is dense, 2 for a check (every returned count is below the category maximum). Dropping books earns no edge-case points.

**Follow-ups:**
- *Top N distinct counts per category?* Change `rk = 2` to `rk <= N`.
- *Also return the first place?* Return both ranks with `rk IN (1, 2)` and keep the category list via the left join.
- *What if terms differ only by case?* Normalise with `LOWER(TRIM(term))` before counting (Part 10).

**Common mistakes:**
- `RANK` instead of `DENSE_RANK`.
- `LIMIT 1 OFFSET 1`, which returns one arbitrary tied term.
- `WHERE rk = 2` after a left join.
- Counting search rows when the question means distinct users; here each row is one search, as the prompt says.
