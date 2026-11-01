# B3 Part 12, Q31-Q40 answers (Wave B)

### Q31 ⭐⭐ 🟡 [Set E2, Q3 of 5, 8 min, 20 pts] Valid coupon on the order date (Part 6 Q39). coupons(code, start_date, end_date, pct_off) and orders(order_id, order_date, coupon_code, amount). Return each order with the coupon status VALID, EXPIRED, NOT_STARTED, UNKNOWN_CODE or NO_COUPON, and the discounted amount for valid ones. Seed 7 orders on the start and end dates (inclusive). SQL with a LEFT JOIN condition in ON, not WHERE (Part 2 Q3), and pandas.
**Asked at:** E-commerce SQL prep pages (Let's Data Science e-commerce and marketplace list, a Dev Genius article, user-uploaded Scribd question sets; search snippets only, not opened); editorial guides and uploads of unknown provenance, not verified candidate reports; analyst and data scientist rounds at Indian and global e-commerce firms
**Say this first (1 line):** Join on the coupon code only (in ON), keep every order, then decide the status with a CASE that compares the order date to the coupon window with inclusive ends; the date test never goes in WHERE.

**Schema and sample data:**
```sql
CREATE TABLE coupons(code TEXT PRIMARY KEY, start_date TEXT, end_date TEXT, pct_off INTEGER);
CREATE TABLE orders(order_id INTEGER, order_date TEXT, coupon_code TEXT, amount INTEGER);
INSERT INTO coupons VALUES ('SAVE10', '2025-03-01', '2025-03-31', 10), ('FLASH', '2025-03-10', '2025-03-12', 25);
INSERT INTO orders VALUES
 (1, '2025-03-01', 'SAVE10', 100),
 (2, '2025-03-31', 'SAVE10', 200),
 (3, '2025-02-28', 'SAVE10', 150),
 (4, '2025-04-01', 'SAVE10', 120),
 (5, '2025-03-12', 'FLASH',   80),
 (6, '2025-03-05', 'BOGUS',   90),
 (7, '2025-03-05', NULL,      60);
```
Orders 1 and 2 sit exactly on the start and end date of SAVE10, order 5 is on the last day of FLASH, order 3 is one day before the window and order 4 one day after.

**SQL answer:** the query below is the `sql_answer` string in the Code block (same text).
```sql
SELECT o.order_id, o.order_date, o.coupon_code,
       CASE WHEN o.coupon_code IS NULL THEN 'NO_COUPON'
            WHEN c.code IS NULL THEN 'UNKNOWN_CODE'
            WHEN o.order_date < c.start_date THEN 'NOT_STARTED'
            WHEN o.order_date > c.end_date THEN 'EXPIRED'
            ELSE 'VALID' END AS status,
       CASE WHEN o.order_date BETWEEN c.start_date AND c.end_date
            THEN ROUND(o.amount * (100 - c.pct_off) / 100.0, 2) END AS discounted
FROM orders o
LEFT JOIN coupons c ON c.code = o.coupon_code
ORDER BY o.order_id
```
The code match is the only join condition, so an order with a bad or missing code keeps its row and `c.code` is NULL. The date test is in the CASE (and inside the discount expression), not in WHERE. `BETWEEN` is inclusive on both ends, which is what makes the start and end dates VALID. ISO date text compares correctly as text; in a real schema the columns are DATE.

**pandas answer:** the same text as the pandas part of the Code block.
```py
orders = pd.read_sql("SELECT * FROM orders", con)
coupons = pd.read_sql("SELECT * FROM coupons", con)
m = orders.merge(coupons, how="left", left_on="coupon_code", right_on="code")
od, sd, ed = (pd.to_datetime(m[c]) for c in ("order_date", "start_date", "end_date"))
m["status"] = np.select(
    [m.coupon_code.isna(), m.code.isna(), od < sd, od > ed],
    ["NO_COUPON", "UNKNOWN_CODE", "NOT_STARTED", "EXPIRED"], default="VALID")
m["discounted"] = (m.amount * (100 - m.pct_off) / 100).where(m.status == "VALID").round(2)
want = m[["order_id", "order_date", "coupon_code", "status", "discounted"]]
```

**Example:** Order 1 is on 2025-03-01: the join finds SAVE10, `order_date < start_date` is false and `order_date > end_date` is false, so VALID, and 100 * (100 - 10) / 100.0 = 90. Order 2 on 2025-03-31 is the end date, not after it, so VALID, 180. Order 3 (02-28) is before the start: NOT_STARTED. Order 4 (04-01) is after the end: EXPIRED. Order 5 (FLASH, 03-12) is VALID, 80 * 0.75 = 60. Order 6's code BOGUS finds no coupon row: UNKNOWN_CODE. Order 7 has a NULL code: NO_COUPON, which must be tested first because the join then also has no coupon row.

**Code:** run with `python3 -I`; it creates the data, runs the SQL and the pandas version and asserts they are equal.
```python
# Q31: coupon status on the order date (LEFT JOIN with the code match in ON), discounted amount for valid ones.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE coupons(code TEXT PRIMARY KEY, start_date TEXT, end_date TEXT, pct_off INTEGER);
CREATE TABLE orders(order_id INTEGER, order_date TEXT, coupon_code TEXT, amount INTEGER);
INSERT INTO coupons VALUES ('SAVE10', '2025-03-01', '2025-03-31', 10), ('FLASH', '2025-03-10', '2025-03-12', 25);
INSERT INTO orders VALUES
 (1, '2025-03-01', 'SAVE10', 100),
 (2, '2025-03-31', 'SAVE10', 200),
 (3, '2025-02-28', 'SAVE10', 150),
 (4, '2025-04-01', 'SAVE10', 120),
 (5, '2025-03-12', 'FLASH',   80),
 (6, '2025-03-05', 'BOGUS',   90),
 (7, '2025-03-05', NULL,      60);
""")

sql_answer = """
SELECT o.order_id, o.order_date, o.coupon_code,
       CASE WHEN o.coupon_code IS NULL THEN 'NO_COUPON'
            WHEN c.code IS NULL THEN 'UNKNOWN_CODE'
            WHEN o.order_date < c.start_date THEN 'NOT_STARTED'
            WHEN o.order_date > c.end_date THEN 'EXPIRED'
            ELSE 'VALID' END AS status,
       CASE WHEN o.order_date BETWEEN c.start_date AND c.end_date
            THEN ROUND(o.amount * (100 - c.pct_off) / 100.0, 2) END AS discounted
FROM orders o
LEFT JOIN coupons c ON c.code = o.coupon_code
ORDER BY o.order_id
"""
# the two wrong versions, to show what they lose
sql_where = """
SELECT COUNT(*) FROM orders o LEFT JOIN coupons c ON c.code = o.coupon_code
WHERE o.order_date BETWEEN c.start_date AND c.end_date
"""
sql_date_in_on = """
SELECT o.order_id, c.code IS NOT NULL AS matched
FROM orders o LEFT JOIN coupons c
  ON c.code = o.coupon_code AND o.order_date BETWEEN c.start_date AND c.end_date
ORDER BY o.order_id
"""
got = pd.read_sql(sql_answer, con)
print(got.to_string(index=False))
print("\nwith the date test in WHERE, rows left:", con.execute(sql_where).fetchone()[0], "of 7")
print("date test in ON, code match flag (cannot tell EXPIRED from UNKNOWN_CODE):",
      pd.read_sql(sql_date_in_on, con).matched.tolist())

# --- pandas
orders = pd.read_sql("SELECT * FROM orders", con)
coupons = pd.read_sql("SELECT * FROM coupons", con)
m = orders.merge(coupons, how="left", left_on="coupon_code", right_on="code")
od, sd, ed = (pd.to_datetime(m[c]) for c in ("order_date", "start_date", "end_date"))
m["status"] = np.select(
    [m.coupon_code.isna(), m.code.isna(), od < sd, od > ed],
    ["NO_COUPON", "UNKNOWN_CODE", "NOT_STARTED", "EXPIRED"], default="VALID")
m["discounted"] = (m.amount * (100 - m.pct_off) / 100).where(m.status == "VALID").round(2)
want = m[["order_id", "order_date", "coupon_code", "status", "discounted"]]
# --- end pandas
print()
print(want.to_string(index=False))
pd.testing.assert_frame_equal(got.sort_values("order_id").reset_index(drop=True),
                              want.sort_values("order_id").reset_index(drop=True), check_dtype=False)
assert len(want) == len(orders) == 7
print("assert passed: SQL equals pandas after sorting by order_id; 7 rows in, 7 rows out")
```

**Output (my run):**
```text
 order_id order_date coupon_code       status  discounted
        1 2025-03-01      SAVE10        VALID        90.0
        2 2025-03-31      SAVE10        VALID       180.0
        3 2025-02-28      SAVE10  NOT_STARTED         NaN
        4 2025-04-01      SAVE10      EXPIRED         NaN
        5 2025-03-12       FLASH        VALID        60.0
        6 2025-03-05       BOGUS UNKNOWN_CODE         NaN
        7 2025-03-05         NaN    NO_COUPON         NaN

with the date test in WHERE, rows left: 3 of 7
date test in ON, code match flag (cannot tell EXPIRED from UNKNOWN_CODE): [1, 1, 0, 0, 1, 0, 0]

 order_id order_date coupon_code       status  discounted
        1 2025-03-01      SAVE10        VALID        90.0
        2 2025-03-31      SAVE10        VALID       180.0
        3 2025-02-28      SAVE10  NOT_STARTED         NaN
        4 2025-04-01      SAVE10      EXPIRED         NaN
        5 2025-03-12       FLASH        VALID        60.0
        6 2025-03-05       BOGUS UNKNOWN_CODE         NaN
        7 2025-03-05         NaN    NO_COUPON         NaN
assert passed: SQL equals pandas after sorting by order_id; 7 rows in, 7 rows out
```

**Edge cases:**
- **WHERE instead of ON:** putting the date test in WHERE turns the LEFT JOIN into an inner join: only 3 of the 7 orders survive (orders 1, 2, 5). Cross-reference Part 2 Q3.
- **Date test inside ON:** it keeps all 7 rows but the coupon columns come back NULL for orders 3, 4 and 6 alike, so you cannot tell EXPIRED or NOT_STARTED from UNKNOWN_CODE. Put the code match in ON and classify afterwards.
- **Order of the CASE:** NO_COUPON before UNKNOWN_CODE, because both have a NULL `c.code`.
- **Duplicate code rows:** `code` is the primary key here. If a code could have several windows (re-runs of a campaign) the join would duplicate orders; then join on the window too and treat no match as the not-valid case, or pick one window per order with a window function.
- **Timestamps:** an `order_date` that carries a time of day breaks an inclusive `BETWEEN` against a pure date end (the end day after 00:00 would look expired). Compare against `end_date + 1 day` with `<` for timestamps (not executed here).
- **Case or spaces in codes:** 'save10' would be UNKNOWN_CODE; clean with `UPPER(TRIM())` if the data is user-typed (UPPER is ASCII-only in SQLite).

**Then explain:**
- **The WHERE-versus-ON rule:** a condition on the right table in WHERE removes the NULL-extended rows; a condition in ON only decides what matches. Here the code match belongs in ON and the classification is a CASE over the joined columns.
- **Inclusive ends** are the whole point of the seed: `<` and `>` for the invalid sides, so the boundary dates fall through to VALID.
- **pandas:** `merge(how="left")` then `np.select` with conditions in the same order as the CASE (first true wins, like CASE). The discount is `where(status == VALID)`, which gives NaN like the CASE without ELSE.
- **Scoring note (Set E2, 20 pts; this book's own rubric, not a company's):** 8 for a correct query, 4 for the seeded edge case, 4 for the pandas version, 2 for stating the assumption, 2 for the check. Full marks: all five statuses are right on the seeded boundary dates (orders 1, 2, 5 VALID), the join keeps 7 rows, and you say why the test is not in WHERE. Partial: a correct VALID/EXPIRED split but an inner join (the NO_COUPON and UNKNOWN_CODE orders lost) is about half of the query marks; date test in ON gets the rows but not the reasons.

**Follow-ups:**
- *What if the discount must be capped?* Wrap in `MIN(discount, cap)` using the scalar two-argument `MIN` in SQLite (a different function from the aggregate; other engines use `LEAST`, not executed here).
- *What if an order can carry several coupons?* Move codes to an `order_coupons` table; then the join fans out, so decide whether to stack or choose the best and aggregate per order.
- *How do you check the result?* Row count out equals row count in (7), and the VALID count equals the count from an inner join with the dates in ON.

**Common mistakes:**
- Date condition in WHERE, silently dropping the orders without a valid coupon.
- Using `BETWEEN` for the exclusive sides or `<=` on the end, making the boundary dates EXPIRED.
- Testing `coupon_code = NULL` instead of `IS NULL`.
- Computing the discount as `amount * pct_off / 100` (that is the discount, not the discounted amount) or with integer division.


### Q32 ⭐⭐ 🟡 [Set E2, Q2 of 5, 8 min, 20 pts] Frequently bought together pairs (Part 2 Q37). order_items(order_id, product_id) with duplicate rows possible for the same product in one order. Return the pairs of products bought together in at least 2 orders, each pair once with its order count, ordered by count descending. Seed 6 orders with a duplicate row. SQL (self join on a.product_id < b.product_id with DISTINCT orders) and pandas (merge or combinations). Assert equal.
**Asked at:** E-commerce SQL prep pages (Let's Data Science e-commerce and marketplace list, a Dev Genius article, user-uploaded Scribd question sets; search snippets only, not opened); editorial guides and uploads of unknown provenance, not verified candidate reports; analyst and data scientist rounds at Indian and global e-commerce firms
**Say this first (1 line):** De-duplicate to distinct (order, product) first, self join on the same order with `a.product_id < b.product_id` so each pair appears once, group by the pair and keep `COUNT(*) >= 2`.

**Schema and sample data:**
```sql
CREATE TABLE order_items(order_id INTEGER, product_id TEXT);
INSERT INTO order_items VALUES
 (1,'A'),(1,'B'),(1,'C'),
 (2,'A'),(2,'B'),
 (3,'A'),(3,'B'),(3,'B'),
 (4,'B'),(4,'C'),
 (5,'A'),(5,'C'),
 (6,'D');
```
Order 3 holds product B twice (the duplicate row); order 6 has a single item.

**SQL answer:** the query below is the `sql_answer` string in the Code block (same text).
```sql
WITH d AS (SELECT DISTINCT order_id, product_id FROM order_items)
SELECT a.product_id AS p1, b.product_id AS p2, COUNT(*) AS orders_together
FROM d a
JOIN d b ON b.order_id = a.order_id AND a.product_id < b.product_id
GROUP BY a.product_id, b.product_id
HAVING COUNT(*) >= 2
ORDER BY orders_together DESC, p1, p2
```
`DISTINCT` in the CTE makes one row per product per order, so every joined row is one order containing both products and `COUNT(*)` is the number of orders. The `<` condition keeps (A, B) and drops (B, A) and (A, A).

**pandas answer:** the same text as the pandas part of the Code block.
```py
items = pd.read_sql("SELECT * FROM order_items", con).drop_duplicates()
pairs = items.merge(items, on="order_id", suffixes=("_1", "_2"))
pairs = pairs[pairs.product_id_1 < pairs.product_id_2]
want = (pairs.groupby(["product_id_1", "product_id_2"]).size().rename("orders_together").reset_index()
        .rename(columns={"product_id_1": "p1", "product_id_2": "p2"}))
want = (want[want.orders_together >= 2]
        .sort_values(["orders_together", "p1", "p2"], ascending=[False, True, True]).reset_index(drop=True))
```

**Example:** Distinct items: order 1 {A,B,C}, 2 {A,B}, 3 {A,B}, 4 {B,C}, 5 {A,C}, 6 {D}. Pairs per order: order 1 gives AB, AC, BC; order 2 gives AB; order 3 gives AB; order 4 gives BC; order 5 gives AC; order 6 gives none. Totals: AB 3, AC 2, BC 2, all at least 2. Without the DISTINCT, order 3's two B rows pair with its A row twice, so AB becomes 4: the naive query overstates by exactly the duplicate.

**Code:** run with `python3 -I`; it creates the data, runs the SQL and the pandas version and asserts they are equal.
```python
# Q32: frequently bought together pairs, each pair once, distinct orders.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE order_items(order_id INTEGER, product_id TEXT);
INSERT INTO order_items VALUES
 (1,'A'),(1,'B'),(1,'C'),
 (2,'A'),(2,'B'),
 (3,'A'),(3,'B'),(3,'B'),
 (4,'B'),(4,'C'),
 (5,'A'),(5,'C'),
 (6,'D');
""")

sql_answer = """
WITH d AS (SELECT DISTINCT order_id, product_id FROM order_items)
SELECT a.product_id AS p1, b.product_id AS p2, COUNT(*) AS orders_together
FROM d a
JOIN d b ON b.order_id = a.order_id AND a.product_id < b.product_id
GROUP BY a.product_id, b.product_id
HAVING COUNT(*) >= 2
ORDER BY orders_together DESC, p1, p2
"""
sql_naive = """
SELECT a.product_id AS p1, b.product_id AS p2, COUNT(*) AS orders_together
FROM order_items a
JOIN order_items b ON b.order_id = a.order_id AND a.product_id < b.product_id
GROUP BY a.product_id, b.product_id
HAVING COUNT(*) >= 2
ORDER BY orders_together DESC, p1, p2
"""
got = pd.read_sql(sql_answer, con)
print("SQL answer"); print(got.to_string(index=False))
print("\nnaive (no DISTINCT), duplicate row counted twice"); print(pd.read_sql(sql_naive, con).to_string(index=False))

# --- pandas
items = pd.read_sql("SELECT * FROM order_items", con).drop_duplicates()
pairs = items.merge(items, on="order_id", suffixes=("_1", "_2"))
pairs = pairs[pairs.product_id_1 < pairs.product_id_2]
want = (pairs.groupby(["product_id_1", "product_id_2"]).size().rename("orders_together").reset_index()
        .rename(columns={"product_id_1": "p1", "product_id_2": "p2"}))
want = (want[want.orders_together >= 2]
        .sort_values(["orders_together", "p1", "p2"], ascending=[False, True, True]).reset_index(drop=True))
# --- end pandas
print("\npandas"); print(want.to_string(index=False))
pd.testing.assert_frame_equal(got, want, check_dtype=False)
print("assert passed: same rows in the same order (count desc, p1, p2)")
```

**Output (my run):**
```text
SQL answer
p1 p2  orders_together
 A  B                3
 A  C                2
 B  C                2

naive (no DISTINCT), duplicate row counted twice
p1 p2  orders_together
 A  B                4
 A  C                2
 B  C                2

pandas
p1 p2  orders_together
 A  B                3
 A  C                2
 B  C                2
assert passed: same rows in the same order (count desc, p1, p2)
```

**Edge cases:**
- **Duplicate rows:** the seeded duplicate moves AB from 3 to 4 without DISTINCT (shown in the output). Alternative: count `COUNT(DISTINCT a.order_id)` and skip the CTE.
- **Single-item orders** (order 6) create no pair, which is correct; they just do not appear.
- **Ties:** AC and BC both have 2, so the secondary sort `p1, p2` makes the order deterministic.
- **Scale:** the self join makes k*(k-1)/2 rows per order of k items, so a 50-item basket gives 1,225 rows; cap basket size or sample before running this on real data.
- **Empty result:** if no pair reaches 2 the query returns zero rows, not a row of zeros.

**Then explain:**
- **Why `<` and not `<>`:** `<>` returns both (A, B) and (B, A), doubling every count and needing a later de-duplication; `<` is a canonical ordering of the pair (Part 2 Q37).
- **Why distinct first:** the unit being counted is an order, and a duplicate line must not count twice.
- **pandas:** `drop_duplicates()`, merge the table with itself on `order_id`, filter `product_id_1 < product_id_2`, `groupby(...).size()`, then filter and sort. The assertion compares in the stated order: count descending, then p1, p2 (no re-sorting needed).
- **Alternative (not run):** `itertools.combinations` over each order's sorted distinct products and a `Counter`; same answer, better memory behaviour for big baskets.
- **Scoring note (Set E2, 20 pts; this book's own rubric, not a company's):** 8 for a correct query, 4 for the seeded edge case, 4 for the pandas version, 2 for stating the assumption, 2 for the check. Full marks: the pair list is AB 3, AC 2, BC 2 in that order, each pair once, with the duplicate handled and said aloud. Partial: a self join that returns both (A,B) and (B,A), or counts AB as 4, keeps most of the query marks but loses the edge-case marks.

**Follow-ups:**
- *What would you add for recommendations?* Support and lift: pair count divided by the number of orders containing each product (orders with A: 4, with B: 4 here), not just raw counts.
- *How do you make it faster?* An index on `(order_id, product_id)` and a pre-filter to products with at least 2 orders, since a pair needs both products to qualify.
- *Triples?* Add a third alias with `b.product_id < c.product_id`; the same duplicate rule applies.

**Common mistakes:**
- `a.product_id <> b.product_id`, which doubles the counts.
- Counting rows instead of distinct orders, so duplicates inflate the pair.
- Putting `COUNT(*) >= 2` in WHERE instead of HAVING.
- Forgetting the tie-break, so the printed order changes between runs.


### Q33 ⭐ 🟢 [Set F1, Q1 of 5, 5 min, 10 pts] Daily active users excluding test accounts (Part 8 Q1). users(user_id, is_test), events(user_id, event_ts TEXT). Return DAU per day for 5 days with days that only have test users shown as 0. Seed 6 users and 12 events including a user with several events per day and an event whose user_id is not in users (decide and state). SQL and pandas.
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** Inner join events to the non-test users, take `COUNT(DISTINCT user_id)` per day, and LEFT JOIN that onto a generated calendar so a day with only test users shows 0; an unknown user_id is excluded and I say so.

**Schema and sample data:**
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT);
INSERT INTO users VALUES (1,0),(2,0),(3,1),(4,0),(5,1),(6,0);
INSERT INTO events VALUES
 (1,'2025-06-01 09:00:00'),(1,'2025-06-01 15:00:00'),(1,'2025-06-01 18:00:00'),
 (2,'2025-06-01 10:00:00'),
 (3,'2025-06-02 11:00:00'),(3,'2025-06-03 12:00:00'),
 (4,'2025-06-02 08:00:00'),(4,'2025-06-04 09:00:00'),
 (1,'2025-06-04 10:00:00'),
 (5,'2025-06-03 13:00:00'),
 (99,'2025-06-05 10:00:00'),
 (6,'2025-06-05 12:00:00');
```
Users 3 and 5 are test accounts; user 99 is not in `users`.

**SQL answer:** the query below is the `sql_answer` string in the Code block (same text).
```sql
WITH RECURSIVE days(d) AS (
  SELECT '2025-06-01' UNION ALL SELECT date(d, '+1 day') FROM days WHERE d < '2025-06-05'
), real_events AS (
  SELECT e.user_id, date(e.event_ts) AS d
  FROM events e JOIN users u ON u.user_id = e.user_id AND u.is_test = 0
)
SELECT days.d AS day, COUNT(DISTINCT r.user_id) AS dau
FROM days LEFT JOIN real_events r ON r.d = days.d
GROUP BY days.d
ORDER BY days.d
```
The recursive CTE builds the 5-day calendar (Part 9 shape; a calendar table does the same). The join to `users` with `is_test = 0` is an inner join, so unknown users are dropped as well as test users. `date(event_ts)` cuts the text timestamp to the day.

**pandas answer:** the same text as the pandas part of the Code block.
```py
users = pd.read_sql("SELECT * FROM users", con)
events = pd.read_sql("SELECT * FROM events", con)
real = events.merge(users[users.is_test == 0], on="user_id", how="inner")
real["day"] = real.event_ts.str[:10]
want = (real.groupby("day").user_id.nunique()
        .reindex(pd.date_range("2025-06-01", "2025-06-05").strftime("%Y-%m-%d"), fill_value=0)
        .rename_axis("day").rename("dau").reset_index())
```

**Example:** 2025-06-01: events from users 1 (three of them) and 2, so 2 distinct users. 06-02: test user 3 is out, user 4 stays: 1. 06-03: only test users 3 and 5 are active, so after the filter no event is left and the LEFT JOIN from the calendar gives 0. 06-04: users 4 and 1: 2. 06-05: user 99 is unknown and dropped, user 6 stays: 1.

**Code:** run with `python3 -I`; it creates the data, runs the SQL and the pandas version and asserts they are equal.
```python
# Q33: DAU excluding test accounts, zero-filled calendar, unknown user_id decision.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE users(user_id INTEGER PRIMARY KEY, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT);
INSERT INTO users VALUES (1,0),(2,0),(3,1),(4,0),(5,1),(6,0);
INSERT INTO events VALUES
 (1,'2025-06-01 09:00:00'),(1,'2025-06-01 15:00:00'),(1,'2025-06-01 18:00:00'),
 (2,'2025-06-01 10:00:00'),
 (3,'2025-06-02 11:00:00'),(3,'2025-06-03 12:00:00'),
 (4,'2025-06-02 08:00:00'),(4,'2025-06-04 09:00:00'),
 (1,'2025-06-04 10:00:00'),
 (5,'2025-06-03 13:00:00'),
 (99,'2025-06-05 10:00:00'),
 (6,'2025-06-05 12:00:00');
""")

sql_answer = """
WITH RECURSIVE days(d) AS (
  SELECT '2025-06-01' UNION ALL SELECT date(d, '+1 day') FROM days WHERE d < '2025-06-05'
), real_events AS (
  SELECT e.user_id, date(e.event_ts) AS d
  FROM events e JOIN users u ON u.user_id = e.user_id AND u.is_test = 0
)
SELECT days.d AS day, COUNT(DISTINCT r.user_id) AS dau
FROM days LEFT JOIN real_events r ON r.d = days.d
GROUP BY days.d
ORDER BY days.d
"""
got = pd.read_sql(sql_answer, con)
print(got.to_string(index=False))
print("\nwith unknown user 99 kept (LEFT JOIN users, is_test IS NOT 1):")
print(con.execute("""SELECT date(e.event_ts), COUNT(DISTINCT e.user_id) FROM events e
  LEFT JOIN users u ON u.user_id = e.user_id WHERE u.is_test IS NOT 1 GROUP BY 1 ORDER BY 1""").fetchall())

# --- pandas
users = pd.read_sql("SELECT * FROM users", con)
events = pd.read_sql("SELECT * FROM events", con)
real = events.merge(users[users.is_test == 0], on="user_id", how="inner")
real["day"] = real.event_ts.str[:10]
want = (real.groupby("day").user_id.nunique()
        .reindex(pd.date_range("2025-06-01", "2025-06-05").strftime("%Y-%m-%d"), fill_value=0)
        .rename_axis("day").rename("dau").reset_index())
# --- end pandas
print("\npandas"); print(want.to_string(index=False))
pd.testing.assert_frame_equal(got, want, check_dtype=False)
print("assert passed: 5 rows, ordered by day; day 2025-06-03 is 0 because only test user 3 and 5 were active")
```

**Output (my run):**
```text
       day  dau
2025-06-01    2
2025-06-02    1
2025-06-03    0
2025-06-04    2
2025-06-05    1

with unknown user 99 kept (LEFT JOIN users, is_test IS NOT 1):
[('2025-06-01', 2), ('2025-06-02', 1), ('2025-06-04', 2), ('2025-06-05', 2)]

pandas
       day  dau
2025-06-01    2
2025-06-02    1
2025-06-03    0
2025-06-04    2
2025-06-05    1
assert passed: 5 rows, ordered by day; day 2025-06-03 is 0 because only test user 3 and 5 were active
```

**Edge cases:**
- **Several events per user per day:** `COUNT(DISTINCT user_id)`; plain `COUNT(*)` would give 4 for 06-01.
- **Day with no real activity:** the calendar LEFT JOIN is what produces the 0 for 06-03; without it the day is missing.
- **Unknown user_id (my decision):** excluded, because I cannot show it is not a test account. The alternative `LEFT JOIN users ... WHERE u.is_test IS NOT 1` keeps user 99 and gives 2 for 06-05 (printed in the output); say which you chose. A NULL `is_test` falls in the same fork: `is_test = 0` excludes it, `IS NOT 1` keeps it.
- **Time zones:** `date(event_ts)` cuts the stored text, so the day is whatever zone the text is in (assume UTC here).
- **Filter in ON, not WHERE:** the `is_test = 0` test is inside the inner join; putting a right-table filter in WHERE after the calendar LEFT JOIN would drop the zero day.

**Then explain:**
- **DAU definition:** distinct users with at least one event in the day (Part 8 Q1), not event count.
- **pandas:** inner `merge` to non-test users, `nunique` per day string, then `reindex` on a full `date_range` with `fill_value=0`; `reindex` is the pandas version of the calendar LEFT JOIN.
- **Scoring note (Set F1, 10 pts; this book's own rubric, not a company's):** 4 for a correct query, 2 for the seeded edge case, 2 for the pandas version, 1 for stating the assumption, 1 for the check. Full marks: DAU 2, 1, 0, 2, 1 with the zero day present, and the unknown-user decision stated. Partial: correct counts but a missing 06-03 row (no calendar) loses the edge-case marks; counting events instead of users fails the main query.

**Follow-ups:**
- *How would you do MAU?* Same shape on a month key, or a rolling 30-day distinct count (Part 8 Q7 style; windows with DISTINCT are not available in SQLite, so a self join or a pre-deduplicated day table is needed).
- *How do you flag unknown ids?* A separate query: events where `user_id NOT IN` (or NOT EXISTS) users, reported to the data owners.

**Common mistakes:**
- `COUNT(user_id)` instead of `COUNT(DISTINCT user_id)`.
- Filtering test users in WHERE after the calendar join, which deletes the zero days.
- Silently keeping unknown ids because a LEFT JOIN plus `is_test <> 1` ignores NULLs (NULL <> 1 is NULL, so the row disappears, the opposite of what many expect).


### Q34 ⭐ 🟢 [Set F2, Q1 of 5, 5 min, 10 pts] Click-through rate with a zero guard (Part 1 Q6). impressions(campaign_id, impressions), clicks(campaign_id, clicks) where one campaign has no click row and one has 0 impressions. Return CTR per campaign rounded to 4 decimals, NULL when impressions are 0, and 0 when there is no click row. SQL (LEFT JOIN, COALESCE, NULLIF) and pandas, assert equal.
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** LEFT JOIN clicks onto impressions, `COALESCE(clicks, 0)` for the missing click row, divide by `NULLIF(impressions, 0)` so zero impressions gives NULL, then round to 4 decimals.

**Schema and sample data:**
```sql
CREATE TABLE impressions(campaign_id INTEGER, impressions INTEGER);
CREATE TABLE clicks(campaign_id INTEGER, clicks INTEGER);
INSERT INTO impressions VALUES (1,1000),(2,500),(3,0),(4,200),(5,7),(6,0);
INSERT INTO clicks VALUES (1,37),(3,0),(4,5),(5,3);
```
Campaign 2 has no click row; campaigns 3 and 6 have 0 impressions (6 also has no click row).

**SQL answer:** the query below is the `sql_answer` string in the Code block (same text).
```sql
SELECT i.campaign_id,
       ROUND(COALESCE(c.clicks, 0) * 1.0 / NULLIF(i.impressions, 0), 4) AS ctr
FROM impressions i
LEFT JOIN clicks c ON c.campaign_id = i.campaign_id
ORDER BY i.campaign_id
```
`* 1.0` forces real division (integer division would give 0). Zero impressions makes `NULLIF` return NULL and the whole ratio NULL; a missing click row becomes 0 via `COALESCE`, which only affects the numerator.

**pandas answer:** the same text as the pandas part of the Code block.
```py
imp = pd.read_sql("SELECT * FROM impressions", con)
clk = pd.read_sql("SELECT * FROM clicks", con)
m = imp.merge(clk, on="campaign_id", how="left")
m["ctr"] = (m.clicks.fillna(0) / m.impressions.replace(0, np.nan)).round(4)
want = m[["campaign_id", "ctr"]]
```

**Example:** Campaign 1: 37 / 1000 = 0.037, printed 0.0370. Campaign 2: no click row, COALESCE gives 0, 0 / 500 = 0. Campaign 3: 0 impressions, so 0 / NULL = NULL. Campaign 4: 5 / 200 = 0.025. Campaign 5: 3 / 7 = 0.428571, rounded 0.4286. Campaign 6: no click row and 0 impressions: NULL (impressions rule wins).

**Code:** run with `python3 -I`; it creates the data, runs the SQL and the pandas version and asserts they are equal.
```python
# Q34: CTR per campaign with zero guards.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE impressions(campaign_id INTEGER, impressions INTEGER);
CREATE TABLE clicks(campaign_id INTEGER, clicks INTEGER);
INSERT INTO impressions VALUES (1,1000),(2,500),(3,0),(4,200),(5,7),(6,0);
INSERT INTO clicks VALUES (1,37),(3,0),(4,5),(5,3);
""")

sql_answer = """
SELECT i.campaign_id,
       ROUND(COALESCE(c.clicks, 0) * 1.0 / NULLIF(i.impressions, 0), 4) AS ctr
FROM impressions i
LEFT JOIN clicks c ON c.campaign_id = i.campaign_id
ORDER BY i.campaign_id
"""
got = pd.read_sql(sql_answer, con)
print(got.to_string(index=False, na_rep="NULL"))
print("\nunguarded division in SQLite, 3 / 0 and 0 / 0:", con.execute("SELECT 3*1.0/0, 0*1.0/0").fetchone())

# --- pandas
imp = pd.read_sql("SELECT * FROM impressions", con)
clk = pd.read_sql("SELECT * FROM clicks", con)
m = imp.merge(clk, on="campaign_id", how="left")
m["ctr"] = (m.clicks.fillna(0) / m.impressions.replace(0, np.nan)).round(4)
want = m[["campaign_id", "ctr"]]
# --- end pandas
print("\npandas"); print(want.to_string(index=False, na_rep="NaN"))
print("unguarded pandas division 3 / 0 and 0 / 0:",
      (pd.Series([3.0, 0.0]) / pd.Series([0.0, 0.0])).tolist())
pd.testing.assert_frame_equal(got, want, check_dtype=False)
print("assert passed: NULL in SQL equals NaN in pandas for campaigns 3 and 6")
```

**Output (my run):**
```text
 campaign_id    ctr
           1 0.0370
           2 0.0000
           3   NULL
           4 0.0250
           5 0.4286
           6   NULL

unguarded division in SQLite, 3 / 0 and 0 / 0: (None, None)

pandas
 campaign_id    ctr
           1 0.0370
           2 0.0000
           3    NaN
           4 0.0250
           5 0.4286
           6    NaN
unguarded pandas division 3 / 0 and 0 / 0: [inf, nan]
assert passed: NULL in SQL equals NaN in pandas for campaigns 3 and 6
```

**Edge cases:**
- **Zero impressions:** SQLite returns NULL for `x / 0` (shown: `3*1.0/0` and `0*1.0/0` both NULL); Postgres raises "division by zero" and MySQL returns NULL in default mode (both not executed here), so the `NULLIF` guard is the portable version.
- **No click row versus 0 clicks:** both end up 0; a missing row is an absent fact, and treating it as 0 is an assumption to say aloud.
- **Several click rows per campaign:** the join would duplicate impression rows; aggregate clicks per campaign first (Part 8 Q10).
- **Rounding:** `ROUND` in SQLite and pandas can differ on exact halves (Part 10 lesson: 703.125 rounds to 703.13 in SQLite and 703.12 in pandas); no seeded value here is a half, so the assertion is safe.

**Then explain:**
- **Why NULL, not 0, for no impressions:** the rate is undefined, and 0 would say the campaign performed badly (Part 1 Q6).
- **pandas difference:** `3.0 / 0.0` gives `inf`, not NaN (printed), so zero is replaced with NaN before dividing; `0/0` is NaN. SQL gives NULL for both without help.
- **Scoring note (Set F2, 10 pts; this book's own rubric, not a company's):** 4 for a correct query, 2 for the seeded edge case, 2 for the pandas version, 1 for stating the assumption, 1 for the check. Full marks: both guards in the right places (NULLIF on the denominator, COALESCE on the numerator) with 0.0370, 0, NULL, 0.0250, 0.4286, NULL. Partial: forgetting the `* 1.0` (all zeros) or a COALESCE on the whole ratio (returns 0 for zero impressions) is partial.

**Follow-ups:**
- *Why not `WHERE impressions > 0`?* It drops the campaign instead of reporting it as undefined.
- *CTR across campaigns?* Sum clicks over sum impressions (a weighted rate), not the mean of the per-campaign CTRs.

**Common mistakes:**
- Integer division giving 0.
- `COALESCE(ctr, 0)` around the ratio, hiding the undefined case as 0.
- Inner joining clicks, losing campaign 2.


### Q35 ⭐ 🟢 [Set F3, Q1 of 5, 5 min, 10 pts] Customers with no orders in 2025 (Part 2 Q2, Part 3 Q3). customers(customer_id, name) and orders(order_id, customer_id, order_date) where one order row has customer_id NULL. Return customers with no 2025 orders using NOT EXISTS, show that NOT IN returns nothing because of the NULL, and give the pandas version. Seed 6 customers.
**Asked at:** Editorial interview-prep guides on FAANG-style SQL rounds (Interview Query Amazon/Google/Meta SQL pages, Glassdoor and 1point3acres thread listings; search snippets only, not opened); guides and anecdotal listings, not verified candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** `NOT EXISTS` with the 2025 date range inside the subquery returns the right customers; `NOT IN` returns nothing as soon as the subquery contains one NULL, because `x NOT IN (..., NULL)` is never true.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER, customer_id INTEGER, order_date TEXT);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Esha'),(6,'Farid');
INSERT INTO orders VALUES
 (1, 1, '2025-01-10'), (2, 2, '2025-06-01'), (3, 3, '2024-12-31'),
 (4, NULL, '2025-03-03'), (5, 1, '2025-07-07'), (6, 5, '2026-01-01');
```
Order 4 is a 2025 order with a NULL customer_id.

**SQL answer:** the query below is the `sql_answer` string in the Code block (same text).
```sql
SELECT c.customer_id, c.name
FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o
                  WHERE o.customer_id = c.customer_id
                    AND o.order_date >= '2025-01-01' AND o.order_date < '2026-01-01')
ORDER BY c.customer_id
```
The `NOT IN` version and its repaired form are in the Code block as `sql_not_in` and `sql_not_in_fixed`. The date range is `>= '2025-01-01' AND < '2026-01-01'` so it also works if `order_date` has a time part.

**pandas answer:** the same text as the pandas part of the Code block.
```py
customers = pd.read_sql("SELECT * FROM customers", con)
orders = pd.read_sql("SELECT * FROM orders", con)
in_2025 = orders[(orders.order_date >= "2025-01-01") & (orders.order_date < "2026-01-01")]
want = customers[~customers.customer_id.isin(in_2025.customer_id)].reset_index(drop=True)
```

**Example:** 2025 orders belong to customers 1 (two orders), 2 and NULL. So Asha and Ben have orders; Chitra's order is 2024-12-31 and Esha's is 2026-01-01, both outside 2025; Dev and Farid have none. The answer is Chitra, Dev, Esha, Farid. With NOT IN the list is (1, 2, NULL, 1): for Chitra, `3 NOT IN (1,2,NULL)` is `3<>1 AND 3<>2 AND 3<>NULL`, which is TRUE AND TRUE AND UNKNOWN = UNKNOWN, so no row is returned for anyone.

**Code:** run with `python3 -I`; it creates the data, runs the SQL and the pandas version and asserts they are equal.
```python
# Q35: customers with no orders in 2025: NOT EXISTS vs NOT IN with a NULL in the subquery.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER, customer_id INTEGER, order_date TEXT);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Esha'),(6,'Farid');
INSERT INTO orders VALUES
 (1, 1, '2025-01-10'), (2, 2, '2025-06-01'), (3, 3, '2024-12-31'),
 (4, NULL, '2025-03-03'), (5, 1, '2025-07-07'), (6, 5, '2026-01-01');
""")

sql_answer = """
SELECT c.customer_id, c.name
FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o
                  WHERE o.customer_id = c.customer_id
                    AND o.order_date >= '2025-01-01' AND o.order_date < '2026-01-01')
ORDER BY c.customer_id
"""
sql_not_in = """
SELECT c.customer_id, c.name FROM customers c
WHERE c.customer_id NOT IN (SELECT customer_id FROM orders
                            WHERE order_date >= '2025-01-01' AND order_date < '2026-01-01')
ORDER BY c.customer_id
"""
sql_not_in_fixed = sql_not_in.replace(
    "WHERE order_date >= '2025-01-01'", "WHERE customer_id IS NOT NULL AND order_date >= '2025-01-01'")
got = pd.read_sql(sql_answer, con)
print("NOT EXISTS"); print(got.to_string(index=False))
print("\nNOT IN with the NULL row inside 2025, rows returned:", len(pd.read_sql(sql_not_in, con)))
fixed = pd.read_sql(sql_not_in_fixed, con)
print("NOT IN with customer_id IS NOT NULL added, rows returned:", len(fixed))

# --- pandas
customers = pd.read_sql("SELECT * FROM customers", con)
orders = pd.read_sql("SELECT * FROM orders", con)
in_2025 = orders[(orders.order_date >= "2025-01-01") & (orders.order_date < "2026-01-01")]
want = customers[~customers.customer_id.isin(in_2025.customer_id)].reset_index(drop=True)
# --- end pandas
print("\npandas ~isin (the NaN in the list does not poison it)"); print(want.to_string(index=False))
print("customer_id dtype after read_sql:", orders.customer_id.dtype, "(float because of the NULL)")
pd.testing.assert_frame_equal(got, want, check_dtype=False)
pd.testing.assert_frame_equal(got, fixed, check_dtype=False)
print("assert passed: NOT EXISTS = pandas ~isin = guarded NOT IN, ordered by customer_id")
```

**Output (my run):**
```text
NOT EXISTS
 customer_id   name
           3 Chitra
           4    Dev
           5   Esha
           6  Farid

NOT IN with the NULL row inside 2025, rows returned: 0
NOT IN with customer_id IS NOT NULL added, rows returned: 4

pandas ~isin (the NaN in the list does not poison it)
 customer_id   name
           3 Chitra
           4    Dev
           5   Esha
           6  Farid
customer_id dtype after read_sql: float64 (float because of the NULL)
assert passed: NOT EXISTS = pandas ~isin = guarded NOT IN, ordered by customer_id
```

**Edge cases:**
- **NULL in the subquery:** NOT IN returns 0 rows (printed); filtering `customer_id IS NOT NULL` inside the subquery fixes it (4 rows).
- **Empty subquery:** NOT IN on an empty list is TRUE for everyone, so the NULL trap only appears when there is data.
- **NULL on the outer side:** a customer with NULL id would also never match NOT IN; here the key is a primary key.
- **pandas:** `~isin` treats NaN as an ordinary value and does not poison the test, so pandas returns the right 4 rows even with the NaN in the list, a difference from SQL (printed). The column is float64 because read_sql turns a NULL integer into NaN.
- **Year boundary:** 2024-12-31 and 2026-01-01 are excluded by the range; a `BETWEEN '2025-01-01' AND '2025-12-31'` would miss 2025-12-31 18:00 on a timestamp column.

**Then explain:**
- **Three-valued logic:** NOT IN expands to a chain of `<>` joined by AND; one UNKNOWN makes the whole chain UNKNOWN, and WHERE keeps only TRUE (Part 2 Q2, Part 3 Q3).
- **NOT EXISTS** compares per row and ignores the NULL row because `o.customer_id = c.customer_id` is UNKNOWN for it, so it never matches.
- **Alternative:** `LEFT JOIN ... WHERE o.order_id IS NULL` with the 2025 test in ON (not run here separately).
- **Scoring note (Set F3, 10 pts; this book's own rubric, not a company's):** 4 for a correct query, 2 for the seeded edge case, 2 for the pandas version, 1 for stating the assumption, 1 for the check. Full marks: the 4 correct customers by NOT EXISTS, the demonstration that NOT IN returns 0 rows, and the one-line reason. Partial: the right customers but no explanation of the NULL, or a NOT IN answer that happens to work only because the seed has no NULL, is partial.

**Follow-ups:**
- *Can you keep NOT IN?* Yes if the subquery column is NOT NULL by constraint or filtered with `IS NOT NULL`, but NOT EXISTS is safer.
- *Performance?* Modern planners often turn NOT EXISTS into an anti-join; confirm with EXPLAIN (Part 11), engine-specific, not executed here for other engines.

**Common mistakes:**
- Using NOT IN on a nullable column.
- Putting the year filter in the outer WHERE instead of the subquery, which changes the meaning.
- Using `BETWEEN` with a year-end date on timestamps.


### Q36 ⭐ 🟢 [Set T1, Q1 of 5, 5 min, 10 pts] Payment success rate by merchant (Part 1 Q10). payments(payment_id, merchant_id, status) with status SUCCESS, FAILED or NULL. Return per merchant attempts, successes, and success rate counting NULL status as not success and in a second column excluding NULL from the denominator. Seed 8 payments over 3 merchants. SQL (conditional aggregation) and pandas.
**Asked at:** Fintech prep pages (Brex interview guide on techinterview.org, DBS data analyst guide on Interview Query, Dataford transactions list, Let's Data Science Stripe practice set; search snippets only, not opened); editorial guides, not candidate reports; payments and banking analyst and data rounds
**Say this first (1 line):** Conditional aggregation: `COUNT(*)` for attempts, `SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END)` for successes, then divide by `COUNT(*)` (NULL counted as not success) and by `NULLIF(COUNT(status), 0)` (NULL excluded).

**Schema and sample data:**
```sql
CREATE TABLE payments(payment_id INTEGER, merchant_id TEXT, status TEXT);
INSERT INTO payments VALUES
 (1,'m1','SUCCESS'),(2,'m1','SUCCESS'),(3,'m1','FAILED'),(4,'m1',NULL),
 (5,'m2','SUCCESS'),(6,'m2','FAILED'),
 (7,'m3',NULL),(8,'m3',NULL);
```
Merchant m3 has only NULL statuses.

**SQL answer:** the query below is the `sql_answer` string in the Code block (same text).
```sql
SELECT merchant_id,
       COUNT(*) AS attempts,
       SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) AS successes,
       ROUND(SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 4) AS rate_all,
       ROUND(SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) * 1.0 / NULLIF(COUNT(status), 0), 4) AS rate_known
FROM payments
GROUP BY merchant_id
ORDER BY merchant_id
```
`COUNT(*)` counts rows, `COUNT(status)` counts non-NULL statuses. The CASE has an ELSE 0 so NULL status counts as not success (without ELSE the SUM would still ignore NULL; the ELSE makes the intent visible and keeps an all-NULL merchant at 0 instead of NULL).

**pandas answer:** the same text as the pandas part of the Code block.
```py
p = pd.read_sql("SELECT * FROM payments", con)
p["ok"] = (p.status == "SUCCESS").astype(int)
g = p.groupby("merchant_id").agg(attempts=("payment_id", "size"), successes=("ok", "sum"),
                                 known=("status", "count")).reset_index()
g["rate_all"] = (g.successes / g.attempts).round(4)
g["rate_known"] = (g.successes / g.known.replace(0, np.nan)).round(4)
want = g[["merchant_id", "attempts", "successes", "rate_all", "rate_known"]]
```

**Example:** m1: 4 attempts, successes = 2, rate_all = 2 / 4 = 0.5, known statuses = 3 (the NULL is out) so rate_known = 2 / 3 = 0.6667. m2: 2 attempts, 1 success, both rates 0.5. m3: 2 attempts, 0 successes, rate_all = 0 / 2 = 0, rate_known = 0 / NULLIF(0, 0) = NULL.

**Code:** run with `python3 -I`; it creates the data, runs the SQL and the pandas version and asserts they are equal.
```python
# Q36: payment success rate by merchant, NULL status counted two ways.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE payments(payment_id INTEGER, merchant_id TEXT, status TEXT);
INSERT INTO payments VALUES
 (1,'m1','SUCCESS'),(2,'m1','SUCCESS'),(3,'m1','FAILED'),(4,'m1',NULL),
 (5,'m2','SUCCESS'),(6,'m2','FAILED'),
 (7,'m3',NULL),(8,'m3',NULL);
""")

sql_answer = """
SELECT merchant_id,
       COUNT(*) AS attempts,
       SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) AS successes,
       ROUND(SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 4) AS rate_all,
       ROUND(SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) * 1.0 / NULLIF(COUNT(status), 0), 4) AS rate_known
FROM payments
GROUP BY merchant_id
ORDER BY merchant_id
"""
got = pd.read_sql(sql_answer, con)
print(got.to_string(index=False, na_rep="NULL"))
print("\ntrap: WHERE status <> 'SUCCESS' returns", con.execute(
    "SELECT COUNT(*) FROM payments WHERE status <> 'SUCCESS'").fetchone()[0],
    "rows (FAILED only), the 3 NULL rows vanish")

# --- pandas
p = pd.read_sql("SELECT * FROM payments", con)
p["ok"] = (p.status == "SUCCESS").astype(int)
g = p.groupby("merchant_id").agg(attempts=("payment_id", "size"), successes=("ok", "sum"),
                                 known=("status", "count")).reset_index()
g["rate_all"] = (g.successes / g.attempts).round(4)
g["rate_known"] = (g.successes / g.known.replace(0, np.nan)).round(4)
want = g[["merchant_id", "attempts", "successes", "rate_all", "rate_known"]]
# --- end pandas
print("\npandas"); print(want.to_string(index=False, na_rep="NaN"))
pd.testing.assert_frame_equal(got, want, check_dtype=False)
print("assert passed: ordered by merchant_id; m3 has rate_all 0.0 and rate_known NULL/NaN")
```

**Output (my run):**
```text
merchant_id  attempts  successes  rate_all  rate_known
         m1         4          2       0.5      0.6667
         m2         2          1       0.5      0.5000
         m3         2          0       0.0        NULL

trap: WHERE status <> 'SUCCESS' returns 2 rows (FAILED only), the 3 NULL rows vanish

pandas
merchant_id  attempts  successes  rate_all  rate_known
         m1         4          2       0.5      0.6667
         m2         2          1       0.5      0.5000
         m3         2          0       0.0         NaN
assert passed: ordered by merchant_id; m3 has rate_all 0.0 and rate_known NULL/NaN
```

**Edge cases:**
- **NULL status:** a pending or unknown payment; the two columns are the two policies, and which one is right is a business decision (say it).
- **All-NULL merchant:** rate_all 0.0 but rate_known undefined (NULL/NaN), a distinction the output shows.
- **The trap:** `WHERE status <> 'SUCCESS'` returns only the 2 FAILED rows; the 3 NULL-status rows vanish because NULL <> 'SUCCESS' is UNKNOWN (printed).
- **Case or spelling** of status values ('Success') would count as not success; normalise first if the data is messy.

**Then explain:**
- **Denominators:** attempts (all rows) versus decided payments (non-NULL). Reporting both is the safe answer (Part 1 Q10).
- **pandas:** a 0/1 helper column, `agg` with named aggregations, `size` for rows and `count` for non-NaN; `count` on a column already excludes NaN, which is the pandas mirror of `COUNT(status)`. Zero is replaced by NaN before dividing, as in Q34.
- **Scoring note (Set T1, 10 pts; this book's own rubric, not a company's):** 4 for a correct query, 2 for the seeded edge case, 2 for the pandas version, 1 for stating the assumption, 1 for the check. Full marks: attempts 4/2/2, successes 2/1/0, both rate columns right including the NULL for m3. Partial: one rate column correct and the other wrong denominator, or ignoring the NULL status trap, is partial.

**Follow-ups:**
- *Where would failed-versus-pending matter?* In a payments funnel the NULL could mean in-flight; exclude payments newer than the settlement window rather than counting them as failures.
- *Can you use FILTER?* `COUNT(*) FILTER (WHERE status = 'SUCCESS')` runs on SQLite 3.30 and later and on PostgreSQL; MySQL has no FILTER (not executed here).

**Common mistakes:**
- `AVG(status = 'SUCCESS')`, which ignores NULL rows silently and gives the second policy by accident.
- Integer division in the rate.
- Dropping NULL rows in WHERE before counting attempts.


### Q37 ⭐ 🟢 [Set T2, Q1 of 5, 5 min, 10 pts] Outstanding balance per loan (Part 2 Q5). loans(loan_id, principal) and repayments(repayment_id, loan_id, amount). Return every loan including those with no repayment, the paid total (0 not NULL) and the outstanding amount, and mark overpaid loans. Seed 5 loans. SQL (LEFT JOIN with COALESCE, pre-aggregated to avoid fan-out) and pandas.
**Asked at:** Fintech prep pages (Brex interview guide on techinterview.org, DBS data analyst guide on Interview Query, Dataford transactions list, Let's Data Science Stripe practice set; search snippets only, not opened); editorial guides, not candidate reports; payments and banking analyst and data rounds
**Say this first (1 line):** Aggregate repayments to one row per loan first, LEFT JOIN that to loans, `COALESCE(paid, 0)`, outstanding is principal minus paid and a loan is overpaid when paid is greater than principal.

**Schema and sample data:**
```sql
CREATE TABLE loans(loan_id INTEGER PRIMARY KEY, principal INTEGER);
CREATE TABLE repayments(repayment_id INTEGER, loan_id INTEGER, amount INTEGER);
INSERT INTO loans VALUES (1,1000),(2,500),(3,800),(4,600),(5,300);
INSERT INTO repayments VALUES (1,1,400),(2,1,300),(3,3,800),(4,4,700),(5,5,100),(6,99,50);
```
Loan 2 has no repayment, loan 4 is overpaid, and repayment 6 refers to a loan that does not exist.

**SQL answer:** the query below is the `sql_answer` string in the Code block (same text).
```sql
SELECT l.loan_id, l.principal,
       COALESCE(r.paid, 0) AS paid,
       l.principal - COALESCE(r.paid, 0) AS outstanding,
       CASE WHEN COALESCE(r.paid, 0) > l.principal THEN 1 ELSE 0 END AS overpaid
FROM loans l
LEFT JOIN (SELECT loan_id, SUM(amount) AS paid FROM repayments GROUP BY loan_id) r
       ON r.loan_id = l.loan_id
ORDER BY l.loan_id
```
The inner subquery makes one row per loan, so the join cannot multiply loans. `COALESCE` turns the missing aggregate for loan 2 into 0. The outstanding amount is negative for the overpaid loan; the flag marks it.

**pandas answer:** the same text as the pandas part of the Code block.
```py
loans = pd.read_sql("SELECT * FROM loans", con)
rep = pd.read_sql("SELECT * FROM repayments", con)
paid = rep.groupby("loan_id").amount.sum().rename("paid").reset_index()
want = loans.merge(paid, on="loan_id", how="left")
want["paid"] = want.paid.fillna(0).astype(int)
want["outstanding"] = want.principal - want.paid
want["overpaid"] = (want.paid > want.principal).astype(int)
want = want.sort_values("loan_id").reset_index(drop=True)
```

**Example:** Loan 1: repayments 400 + 300 = 700, outstanding 1000 - 700 = 300. Loan 2: no row, paid 0, outstanding 500. Loan 3: 800, outstanding 0, not overpaid (equal is fully paid). Loan 4: 700 against 600, outstanding -100, overpaid 1. Loan 5: 100, outstanding 200. The orphan repayment for loan 99 matches no loan and disappears from a LEFT JOIN starting at loans.

**Code:** run with `python3 -I`; it creates the data, runs the SQL and the pandas version and asserts they are equal.
```python
# Q37: outstanding balance per loan with pre-aggregated repayments.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE loans(loan_id INTEGER PRIMARY KEY, principal INTEGER);
CREATE TABLE repayments(repayment_id INTEGER, loan_id INTEGER, amount INTEGER);
INSERT INTO loans VALUES (1,1000),(2,500),(3,800),(4,600),(5,300);
INSERT INTO repayments VALUES (1,1,400),(2,1,300),(3,3,800),(4,4,700),(5,5,100),(6,99,50);
""")

sql_answer = """
SELECT l.loan_id, l.principal,
       COALESCE(r.paid, 0) AS paid,
       l.principal - COALESCE(r.paid, 0) AS outstanding,
       CASE WHEN COALESCE(r.paid, 0) > l.principal THEN 1 ELSE 0 END AS overpaid
FROM loans l
LEFT JOIN (SELECT loan_id, SUM(amount) AS paid FROM repayments GROUP BY loan_id) r
       ON r.loan_id = l.loan_id
ORDER BY l.loan_id
"""
sql_fanout = """
SELECT SUM(l.principal) FROM loans l LEFT JOIN repayments r ON r.loan_id = l.loan_id
"""
got = pd.read_sql(sql_answer, con)
print(got.to_string(index=False))
print("\ntotal principal, correct:", con.execute("SELECT SUM(principal) FROM loans").fetchone()[0],
      "| after joining raw repayments (fan-out):", con.execute(sql_fanout).fetchone()[0])

# --- pandas
loans = pd.read_sql("SELECT * FROM loans", con)
rep = pd.read_sql("SELECT * FROM repayments", con)
paid = rep.groupby("loan_id").amount.sum().rename("paid").reset_index()
want = loans.merge(paid, on="loan_id", how="left")
want["paid"] = want.paid.fillna(0).astype(int)
want["outstanding"] = want.principal - want.paid
want["overpaid"] = (want.paid > want.principal).astype(int)
want = want.sort_values("loan_id").reset_index(drop=True)
# --- end pandas
print("\npandas"); print(want.to_string(index=False))
pd.testing.assert_frame_equal(got, want, check_dtype=False)
assert 99 not in want.loan_id.values
print("assert passed: 5 loans, ordered by loan_id; orphan repayment for loan 99 appears in neither")
```

**Output (my run):**
```text
 loan_id  principal  paid  outstanding  overpaid
       1       1000   700          300         0
       2        500     0          500         0
       3        800   800            0         0
       4        600   700         -100         1
       5        300   100          200         0

total principal, correct: 3200 | after joining raw repayments (fan-out): 4200

pandas
 loan_id  principal  paid  outstanding  overpaid
       1       1000   700          300         0
       2        500     0          500         0
       3        800   800            0         0
       4        600   700         -100         1
       5        300   100          200         0
assert passed: 5 loans, ordered by loan_id; orphan repayment for loan 99 appears in neither
```

**Edge cases:**
- **Fan-out:** joining raw repayments to loans repeats loan 1's principal on two rows, so `SUM(principal)` becomes 4,200 instead of 3,200 (printed). Pre-aggregation avoids it (Part 8 Q11).
- **No repayments:** loan 2 gets 0, not NULL, thanks to COALESCE; `principal - NULL` would otherwise be NULL.
- **Exactly paid:** paid equals principal is not overpaid (strict `>`).
- **Orphan rows:** repayment 99 is excluded here; reconciling it is a separate check (anti-join from repayments to loans).
- **Money types:** integers here; real money should be integer minor units or DECIMAL, not floats.

**Then explain:**
- **Why pre-aggregate:** the question wants one row per loan; aggregate the many side before the join (Part 2 Q5).
- **pandas:** `groupby.sum`, left `merge`, `fillna(0).astype(int)` (the merge makes `paid` float because of NaN), then vectorised arithmetic.
- **Scoring note (Set T2, 10 pts; this book's own rubric, not a company's):** 4 for a correct query, 2 for the seeded edge case, 2 for the pandas version, 1 for stating the assumption, 1 for the check. Full marks: all five loans including loan 2 at 0 paid and loan 4 flagged, without fan-out. Partial: correct numbers but NULL instead of 0 for loan 2, or an unflagged overpayment, is partial.

**Follow-ups:**
- *How do you find repayments for missing loans?* `LEFT JOIN repayments to loans WHERE l.loan_id IS NULL` (loan 99, amount 50).
- *Time-aware balance?* Add a running sum of repayments by date (Part 5), as of a cut-off date.

**Common mistakes:**
- Joining raw repayments and summing principal.
- Inner join, dropping unpaid loans.
- Using `>=` for overpaid.


### Q38 ⭐ 🟢 [Set T3, Q1 of 5, 5 min, 10 pts] New versus returning active customers per month (Part 6 Q14). wallet_activity(customer_id, activity_date) over Jan to Mar 2025. For each month return customers whose first ever activity month is that month (new) and those active earlier (returning). Seed 7 customers with duplicate rows per day. SQL and pandas.
**Asked at:** Fintech prep pages (Brex interview guide on techinterview.org, DBS data analyst guide on Interview Query, Dataford transactions list, Let's Data Science Stripe practice set; search snippets only, not opened); editorial guides, not candidate reports; payments and banking analyst and data rounds
**Say this first (1 line):** Reduce to distinct (customer, month), get each customer's first month, then per month count customers whose month equals the first month (new) and those where it is later (returning).

**Schema and sample data:**
```sql
CREATE TABLE wallet_activity(customer_id INTEGER, activity_date TEXT);
INSERT INTO wallet_activity VALUES
 (1,'2025-01-05'),(1,'2025-01-05'),(1,'2025-02-10'),(1,'2025-03-02'),
 (2,'2025-01-20'),(2,'2025-03-15'),
 (3,'2025-02-01'),(3,'2025-02-01'),(3,'2025-02-14'),
 (4,'2025-02-20'),(4,'2025-03-01'),
 (5,'2025-03-05'),(5,'2025-03-05'),
 (6,'2025-01-31'),(6,'2025-02-01'),
 (7,'2025-03-30');
```
16 rows, 12 distinct customer-months, with duplicate rows on the same day and customer 2 silent in February.

**SQL answer:** the query below is the `sql_answer` string in the Code block (same text).
```sql
WITH m AS (
  SELECT DISTINCT customer_id, SUBSTR(activity_date, 1, 7) AS ym FROM wallet_activity
), f AS (
  SELECT customer_id, MIN(ym) AS first_ym FROM m GROUP BY customer_id
)
SELECT m.ym,
       SUM(CASE WHEN m.ym = f.first_ym THEN 1 ELSE 0 END) AS new_customers,
       SUM(CASE WHEN m.ym > f.first_ym THEN 1 ELSE 0 END) AS returning_customers
FROM m JOIN f ON f.customer_id = m.customer_id
GROUP BY m.ym
ORDER BY m.ym
```
`SUBSTR(activity_date, 1, 7)` gives the 'YYYY-MM' key; the month strings sort correctly as text. `DISTINCT` removes the duplicate rows so a customer counts once per month.

**pandas answer:** the same text as the pandas part of the Code block.
```py
w = pd.read_sql("SELECT * FROM wallet_activity", con)
w["ym"] = w.activity_date.str[:7]
m = w[["customer_id", "ym"]].drop_duplicates()
m["first_ym"] = m.groupby("customer_id").ym.transform("min")
m["is_new"] = (m.ym == m.first_ym).astype(int)
m["is_ret"] = (m.ym > m.first_ym).astype(int)
want = (m.groupby("ym").agg(new_customers=("is_new", "sum"), returning_customers=("is_ret", "sum"))
        .reset_index())
```

**Example:** Distinct customer-months: January {1, 2, 6}, February {1, 3, 4, 6}, March {1, 2, 4, 5, 7}. First months: 1, 2 and 6 in January; 3 and 4 in February; 5 and 7 in March. January: 3 new, 0 returning. February: 3 and 4 are new, 1 and 6 are returning: 2 and 2. March: 5 and 7 are new, 1, 2 and 4 are returning (customer 2 skipped February and still counts as returning): 2 and 3.

**Code:** run with `python3 -I`; it creates the data, runs the SQL and the pandas version and asserts they are equal.
```python
# Q38: new vs returning active customers per month.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE wallet_activity(customer_id INTEGER, activity_date TEXT);
INSERT INTO wallet_activity VALUES
 (1,'2025-01-05'),(1,'2025-01-05'),(1,'2025-02-10'),(1,'2025-03-02'),
 (2,'2025-01-20'),(2,'2025-03-15'),
 (3,'2025-02-01'),(3,'2025-02-01'),(3,'2025-02-14'),
 (4,'2025-02-20'),(4,'2025-03-01'),
 (5,'2025-03-05'),(5,'2025-03-05'),
 (6,'2025-01-31'),(6,'2025-02-01'),
 (7,'2025-03-30');
""")

sql_answer = """
WITH m AS (
  SELECT DISTINCT customer_id, SUBSTR(activity_date, 1, 7) AS ym FROM wallet_activity
), f AS (
  SELECT customer_id, MIN(ym) AS first_ym FROM m GROUP BY customer_id
)
SELECT m.ym,
       SUM(CASE WHEN m.ym = f.first_ym THEN 1 ELSE 0 END) AS new_customers,
       SUM(CASE WHEN m.ym > f.first_ym THEN 1 ELSE 0 END) AS returning_customers
FROM m JOIN f ON f.customer_id = m.customer_id
GROUP BY m.ym
ORDER BY m.ym
"""
got = pd.read_sql(sql_answer, con)
print(got.to_string(index=False))
print("\nsanity: raw rows", con.execute("SELECT COUNT(*) FROM wallet_activity").fetchone()[0],
      "| distinct customer-months", con.execute(
      "SELECT COUNT(*) FROM (SELECT DISTINCT customer_id, SUBSTR(activity_date,1,7) FROM wallet_activity)").fetchone()[0],
      "| sum of new + returning", int(got.new_customers.sum() + got.returning_customers.sum()))

# --- pandas
w = pd.read_sql("SELECT * FROM wallet_activity", con)
w["ym"] = w.activity_date.str[:7]
m = w[["customer_id", "ym"]].drop_duplicates()
m["first_ym"] = m.groupby("customer_id").ym.transform("min")
m["is_new"] = (m.ym == m.first_ym).astype(int)
m["is_ret"] = (m.ym > m.first_ym).astype(int)
want = (m.groupby("ym").agg(new_customers=("is_new", "sum"), returning_customers=("is_ret", "sum"))
        .reset_index())
# --- end pandas
print("\npandas"); print(want.to_string(index=False))
pd.testing.assert_frame_equal(got, want, check_dtype=False)
print("assert passed: 3 rows ordered by month")
```

**Output (my run):**
```text
     ym  new_customers  returning_customers
2025-01              3                    0
2025-02              2                    2
2025-03              2                    3

sanity: raw rows 16 | distinct customer-months 12 | sum of new + returning 12

pandas
     ym  new_customers  returning_customers
2025-01              3                    0
2025-02              2                    2
2025-03              2                    3
assert passed: 3 rows ordered by month
```

**Edge cases:**
- **Duplicates:** 16 rows collapse to 12 customer-months; the sanity line shows new + returning also totals 12.
- **Gap months:** customer 2 returns in March after a silent February; "returning" means active earlier, not active last month.
- **Month boundary:** customer 6 is active on 01-31 and 02-01, so one in each month.
- **First activity outside the window:** with only Jan to Mar data, a customer whose real first activity was in 2024 would be labelled new in January; the "first ever" needs full history, not just the window.
- **A month with no activity** would not appear; join to a month calendar if zero rows are needed (as in Q33).

**Then explain:**
- **Definition:** new = first ever activity month equals this month; returning = first month earlier than this month (Part 6 Q14).
- **pandas:** `drop_duplicates`, `groupby(...).transform('min')` for each customer's first month, two 0/1 helper columns and a grouped sum. `transform` keeps the row count, which is what a window `MIN() OVER` gives in SQL.
- **Scoring note (Set T3, 10 pts; this book's own rubric, not a company's):** 4 for a correct query, 2 for the seeded edge case, 2 for the pandas version, 1 for stating the assumption, 1 for the check. Full marks: 3/0, 2/2, 2/3 with duplicates removed and customer 2 counted as returning in March. Partial: a count that includes duplicate rows, or a returning definition that requires activity in the previous month, is partial.

**Follow-ups:**
- *Retention rate?* Returning customers in month m divided by active customers in month m-1 (a different definition, Part 6 Q10).
- *Why use the month text and not a date function?* Text `YYYY-MM` is portable and sorts; `DATE_TRUNC` exists in PostgreSQL, BigQuery and Snowflake but not in SQLite (not executed here).

**Common mistakes:**
- Counting rows instead of distinct customers.
- Calling someone new in every month because the first-month lookup is done per month instead of overall.
- Using the min over the filtered window only.


### Q39 ⭐ 🟢 [Set E1, Q1 of 5, 5 min, 10 pts] Orders and revenue by status (Part 1 Q4). orders(order_id, customer_id, status, amount) with some NULL amounts. Return orders, orders with an amount, revenue and average amount per status, showing how COUNT(*), COUNT(amount) and AVG treat the NULLs. Seed 8 orders. SQL and pandas (count versus size, mean skipna).
**Asked at:** E-commerce SQL prep pages (Let's Data Science e-commerce and marketplace list, a Dev Genius article, user-uploaded Scribd question sets; search snippets only, not opened); editorial guides and uploads of unknown provenance, not verified candidate reports; analyst and data scientist rounds at Indian and global e-commerce firms
**Say this first (1 line):** `COUNT(*)` counts rows, `COUNT(amount)` counts non-NULL amounts, `SUM` and `AVG` skip NULLs, so the average is over the orders that have an amount, not over all orders.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER, customer_id INTEGER, status TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'DELIVERED',100),(2,2,'DELIVERED',200),(3,3,'DELIVERED',NULL),
 (4,4,'CANCELLED',NULL),(5,5,'CANCELLED',50),(6,6,'CANCELLED',NULL),
 (7,7,'RETURNED',80),
 (8,8,'SHIPPED',NULL);
```
SHIPPED has a single order with a NULL amount.

**SQL answer:** the query below is the `sql_answer` string in the Code block (same text).
```sql
SELECT status,
       COUNT(*) AS orders,
       COUNT(amount) AS orders_with_amount,
       SUM(amount) AS revenue,
       AVG(amount) AS avg_amount
FROM orders
GROUP BY status
ORDER BY status
```
No CASE needed: the aggregates' NULL rules do the work. The SHIPPED group is the one where every amount is NULL.

**pandas answer:** the same text as the pandas part of the Code block.
```py
o = pd.read_sql("SELECT * FROM orders", con)
want = (o.groupby("status").agg(orders=("order_id", "size"), orders_with_amount=("amount", "count"),
                                revenue=("amount", lambda s: s.sum(min_count=1)),
                                avg_amount=("amount", "mean"))
        .reset_index())
```

**Example:** DELIVERED: 3 orders, 2 with an amount (100, 200), revenue 300, average 300 / 2 = 150 (not 300 / 3 = 100). CANCELLED: 3 orders, 1 amount (50), revenue 50, average 50. RETURNED: 1 order, 80, 80. SHIPPED: 1 order, 0 amounts, SUM and AVG are NULL (no value, not 0).

**Code:** run with `python3 -I`; it creates the data, runs the SQL and the pandas version and asserts they are equal.
```python
# Q39: orders and revenue by status with NULL amounts.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER, customer_id INTEGER, status TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'DELIVERED',100),(2,2,'DELIVERED',200),(3,3,'DELIVERED',NULL),
 (4,4,'CANCELLED',NULL),(5,5,'CANCELLED',50),(6,6,'CANCELLED',NULL),
 (7,7,'RETURNED',80),
 (8,8,'SHIPPED',NULL);
""")

sql_answer = """
SELECT status,
       COUNT(*) AS orders,
       COUNT(amount) AS orders_with_amount,
       SUM(amount) AS revenue,
       AVG(amount) AS avg_amount
FROM orders
GROUP BY status
ORDER BY status
"""
got = pd.read_sql(sql_answer, con)
print(got.to_string(index=False, na_rep="NULL"))
print("\nwrong average, SUM / COUNT(*) for DELIVERED:",
      con.execute("SELECT SUM(amount) * 1.0 / COUNT(*) FROM orders WHERE status = 'DELIVERED'").fetchone()[0],
      "vs AVG:", con.execute("SELECT AVG(amount) FROM orders WHERE status = 'DELIVERED'").fetchone()[0])

# --- pandas
o = pd.read_sql("SELECT * FROM orders", con)
want = (o.groupby("status").agg(orders=("order_id", "size"), orders_with_amount=("amount", "count"),
                                revenue=("amount", lambda s: s.sum(min_count=1)),
                                avg_amount=("amount", "mean"))
        .reset_index())
# --- end pandas
print("\npandas (sum with min_count=1)"); print(want.to_string(index=False, na_rep="NaN"))
plain = o.groupby("status").amount.sum()
print("\npandas plain sum() for SHIPPED:", plain["SHIPPED"], "(SQL SUM gives NULL; pandas gives 0.0)")
print("amount.count() =", o.amount.count(), "| len(o) =", len(o), "| mean(skipna=False) =", o.amount.mean(skipna=False))
pd.testing.assert_frame_equal(got, want, check_dtype=False)
print("assert passed: ordered by status; SHIPPED revenue NULL equals NaN only with min_count=1")
```

**Output (my run):**
```text
   status  orders  orders_with_amount  revenue  avg_amount
CANCELLED       3                   1     50.0        50.0
DELIVERED       3                   2    300.0       150.0
 RETURNED       1                   1     80.0        80.0
  SHIPPED       1                   0     NULL        NULL

wrong average, SUM / COUNT(*) for DELIVERED: 100.0 vs AVG: 150.0

pandas (sum with min_count=1)
   status  orders  orders_with_amount  revenue  avg_amount
CANCELLED       3                   1     50.0        50.0
DELIVERED       3                   2    300.0       150.0
 RETURNED       1                   1     80.0        80.0
  SHIPPED       1                   0      NaN         NaN

pandas plain sum() for SHIPPED: 0.0 (SQL SUM gives NULL; pandas gives 0.0)
amount.count() = 4 | len(o) = 8 | mean(skipna=False) = nan
assert passed: ordered by status; SHIPPED revenue NULL equals NaN only with min_count=1
```

**Edge cases:**
- **All-NULL group:** SQL `SUM` is NULL and `AVG` is NULL for SHIPPED; pandas plain `sum()` gives 0.0 (printed). The assertion therefore uses `sum(min_count=1)`.
- **Wrong average:** `SUM / COUNT(*)` gives 100 for DELIVERED instead of 150 (printed); that treats a missing amount as 0, a decision, not a default.
- **Zero versus NULL:** an order with amount 0 would be counted by COUNT(amount) and lower the average; NULL would not.
- **pandas `mean(skipna=False)`** over the whole column gives NaN (printed), as one NULL poisons the result.

**Then explain:**
- **SQL rule:** aggregates ignore NULL inputs except `COUNT(*)`; with no non-NULL input `SUM` and `AVG` return NULL and `COUNT(col)` returns 0 (Part 1 Q4).
- **pandas:** `size` counts rows, `count` counts non-NaN (the `COUNT(*)` and `COUNT(col)` pair); `mean` skips NaN by default; `sum` skips NaN but returns 0.0 for an all-NaN group unless `min_count=1`.
- **Scoring note (Set E1, 10 pts; this book's own rubric, not a company's):** 4 for a correct query, 2 for the seeded edge case, 2 for the pandas version, 1 for stating the assumption, 1 for the check. Full marks: orders 3/3/1/1, with-amount 2/1/1/0, revenue 300/50/80/NULL, averages 150/50/80/NULL and the reason the DELIVERED average is 150. Partial: right counts but an average computed over all rows, or a 0 for SHIPPED revenue without comment, is partial.

**Follow-ups:**
- *How would you treat NULL as 0 on purpose?* `AVG(COALESCE(amount, 0))`, only if the business says a missing amount means free.
- *Why do the status groups not add to 8 with amounts?* Four orders have no amount; orders_with_amount sums to 4.

**Common mistakes:**
- Dividing `SUM` by `COUNT(*)`.
- Reading NULL revenue as 0 in a report.
- In pandas, using `len` or `size` when `count` is meant, or trusting `sum()` for an all-NaN group.


### Q40 ⭐ 🟢 [Set E2, Q1 of 5, 5 min, 10 pts] Cart abandonment rate (Part 8 Q27). events(session_id, event_name, event_ts) with add_to_cart and purchase events. Return the share of sessions with an add_to_cart that never reached purchase, and the share where purchase happened before add_to_cart (data anomaly). Seed 8 sessions. SQL (EXISTS or conditional aggregation) and pandas.
**Asked at:** E-commerce SQL prep pages (Let's Data Science e-commerce and marketplace list, a Dev Genius article, user-uploaded Scribd question sets; search snippets only, not opened); editorial guides and uploads of unknown provenance, not verified candidate reports; analyst and data scientist rounds at Indian and global e-commerce firms
**Say this first (1 line):** Per session take the first add_to_cart time and first purchase time with conditional aggregation; among sessions with an add, abandoned means no purchase at all and the anomaly means the first purchase is earlier than the first add.

**Schema and sample data:**
```sql
CREATE TABLE events(session_id TEXT, event_name TEXT, event_ts TEXT);
INSERT INTO events VALUES
 ('s1','add_to_cart','2025-05-01 10:00:00'),('s1','purchase','2025-05-01 10:05:00'),
 ('s2','add_to_cart','2025-05-01 11:00:00'),
 ('s3','add_to_cart','2025-05-01 12:00:00'),('s3','add_to_cart','2025-05-01 12:02:00'),
 ('s4','purchase','2025-05-01 09:00:00'),('s4','add_to_cart','2025-05-01 09:30:00'),
 ('s5','add_to_cart','2025-05-01 10:00:00'),('s5','purchase','2025-05-01 10:30:00'),('s5','add_to_cart','2025-05-01 10:40:00'),
 ('s6','page_view','2025-05-01 13:00:00'),
 ('s7','purchase','2025-05-01 14:00:00'),
 ('s8','add_to_cart','2025-05-01 15:00:00'),('s8','purchase','2025-05-01 15:00:00');
```
8 sessions: s6 never adds anything, s7 purchases without an add, s4 buys before it adds, s8 adds and buys at the same second.

**SQL answer:** the query below is the `sql_answer` string in the Code block (same text).
```sql
WITH s AS (
  SELECT session_id,
         MIN(CASE WHEN event_name = 'add_to_cart' THEN event_ts END) AS first_add,
         MIN(CASE WHEN event_name = 'purchase' THEN event_ts END) AS first_purchase
  FROM events GROUP BY session_id
)
SELECT COUNT(*) AS carts,
       SUM(CASE WHEN first_purchase IS NULL THEN 1 ELSE 0 END) AS abandoned,
       ROUND(SUM(CASE WHEN first_purchase IS NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 4) AS abandonment_rate,
       SUM(CASE WHEN first_purchase < first_add THEN 1 ELSE 0 END) AS purchase_before_add,
       ROUND(SUM(CASE WHEN first_purchase < first_add THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 4) AS anomaly_rate
FROM s
WHERE first_add IS NOT NULL
```
The denominator is sessions with at least one add_to_cart (6). Abandoned = no purchase event at all in the session; the EXISTS formulation (`sql_exists` in the Code block) gives the same counts.

**pandas answer:** the same text as the pandas part of the Code block.
```py
e = pd.read_sql("SELECT * FROM events", con)
s = (e.assign(add=e.event_ts.where(e.event_name == "add_to_cart"),
              buy=e.event_ts.where(e.event_name == "purchase"))
     .groupby("session_id").agg(first_add=("add", "min"), first_purchase=("buy", "min")))
carts = s[s.first_add.notna()]
abandoned = int(carts.first_purchase.isna().sum())
anomaly = int((carts.first_purchase < carts.first_add).sum())
want = pd.DataFrame({"carts": [len(carts)], "abandoned": [abandoned],
                     "abandonment_rate": [round(abandoned / len(carts), 4)],
                     "purchase_before_add": [anomaly], "anomaly_rate": [round(anomaly / len(carts), 4)]})
```

**Example:** Sessions with an add: s1, s2, s3, s4, s5, s8 = 6. s2 and s3 never purchase: abandoned 2, rate 2 / 6 = 0.3333 (s3's two adds still count as one session). s4's first purchase (09:00) is before its first add (09:30): 1 anomaly, 1 / 6 = 0.1667. s5 buys at 10:30 after its first add at 10:00 and re-adds at 10:40: not an anomaly. s8's add and purchase share a timestamp, a tie, so not counted as before. s6 and s7 have no add and stay out of the denominator.

**Code:** run with `python3 -I`; it creates the data, runs the SQL and the pandas version and asserts they are equal.
```python
# Q40: cart abandonment rate and purchase-before-add anomaly.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE events(session_id TEXT, event_name TEXT, event_ts TEXT);
INSERT INTO events VALUES
 ('s1','add_to_cart','2025-05-01 10:00:00'),('s1','purchase','2025-05-01 10:05:00'),
 ('s2','add_to_cart','2025-05-01 11:00:00'),
 ('s3','add_to_cart','2025-05-01 12:00:00'),('s3','add_to_cart','2025-05-01 12:02:00'),
 ('s4','purchase','2025-05-01 09:00:00'),('s4','add_to_cart','2025-05-01 09:30:00'),
 ('s5','add_to_cart','2025-05-01 10:00:00'),('s5','purchase','2025-05-01 10:30:00'),('s5','add_to_cart','2025-05-01 10:40:00'),
 ('s6','page_view','2025-05-01 13:00:00'),
 ('s7','purchase','2025-05-01 14:00:00'),
 ('s8','add_to_cart','2025-05-01 15:00:00'),('s8','purchase','2025-05-01 15:00:00');
""")

sql_answer = """
WITH s AS (
  SELECT session_id,
         MIN(CASE WHEN event_name = 'add_to_cart' THEN event_ts END) AS first_add,
         MIN(CASE WHEN event_name = 'purchase' THEN event_ts END) AS first_purchase
  FROM events GROUP BY session_id
)
SELECT COUNT(*) AS carts,
       SUM(CASE WHEN first_purchase IS NULL THEN 1 ELSE 0 END) AS abandoned,
       ROUND(SUM(CASE WHEN first_purchase IS NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 4) AS abandonment_rate,
       SUM(CASE WHEN first_purchase < first_add THEN 1 ELSE 0 END) AS purchase_before_add,
       ROUND(SUM(CASE WHEN first_purchase < first_add THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 4) AS anomaly_rate
FROM s
WHERE first_add IS NOT NULL
"""
# second formulation with EXISTS, same two counts
sql_exists = """
SELECT COUNT(*) AS carts,
       SUM(NOT EXISTS (SELECT 1 FROM events p WHERE p.session_id = a.session_id AND p.event_name = 'purchase')) AS abandoned,
       SUM(EXISTS (SELECT 1 FROM events p WHERE p.session_id = a.session_id AND p.event_name = 'purchase'
                   AND p.event_ts < a.first_add)) AS purchase_before_add
FROM (SELECT session_id, MIN(event_ts) AS first_add FROM events WHERE event_name = 'add_to_cart' GROUP BY session_id) a
"""
got = pd.read_sql(sql_answer, con)
print(got.to_string(index=False))
ex = pd.read_sql(sql_exists, con)
print("\nEXISTS version"); print(ex.to_string(index=False))

# --- pandas
e = pd.read_sql("SELECT * FROM events", con)
s = (e.assign(add=e.event_ts.where(e.event_name == "add_to_cart"),
              buy=e.event_ts.where(e.event_name == "purchase"))
     .groupby("session_id").agg(first_add=("add", "min"), first_purchase=("buy", "min")))
carts = s[s.first_add.notna()]
abandoned = int(carts.first_purchase.isna().sum())
anomaly = int((carts.first_purchase < carts.first_add).sum())
want = pd.DataFrame({"carts": [len(carts)], "abandoned": [abandoned],
                     "abandonment_rate": [round(abandoned / len(carts), 4)],
                     "purchase_before_add": [anomaly], "anomaly_rate": [round(anomaly / len(carts), 4)]})
# --- end pandas
print("\npandas"); print(want.to_string(index=False))
pd.testing.assert_frame_equal(got, want, check_dtype=False)
assert (ex.iloc[0].tolist() == got[["carts", "abandoned", "purchase_before_add"]].iloc[0].tolist())
print("assert passed: one-row result equal in SQL (CASE and EXISTS) and pandas; 8 sessions, 6 with an add_to_cart")
```

**Output (my run):**
```text
 carts  abandoned  abandonment_rate  purchase_before_add  anomaly_rate
     6          2            0.3333                    1        0.1667

EXISTS version
 carts  abandoned  purchase_before_add
     6          2                    1

pandas
 carts  abandoned  abandonment_rate  purchase_before_add  anomaly_rate
     6          2            0.3333                    1        0.1667
assert passed: one-row result equal in SQL (CASE and EXISTS) and pandas; 8 sessions, 6 with an add_to_cart
```

**Edge cases:**
- **Denominator:** only sessions with an add; including s6 and s7 would give 2 / 8 = 0.25, a different metric.
- **Repeat adds:** `MIN` per session means a session counts once.
- **Purchase before add (s4):** it has a purchase, so it is not abandoned under this definition; it is a separate anomaly, probably clock skew or missing events, and I report it rather than fix it.
- **Ties:** equal timestamps are not "before" (strict `<`).
- **Purchase between adds (s5):** a later add after the purchase is allowed; the first-add rule ignores it.
- **Timestamps as text:** the same-format ISO text compares correctly; mixed formats would not.

**Then explain:**
- **Two equivalent forms:** conditional aggregation over a per-session CTE (above) or `EXISTS` for the purchase test; the EXISTS output matches (printed). I would pick the CTE when I also need the anomaly, as it computes both in one pass.
- **pandas:** put the timestamp in two helper columns with `where`, `groupby.agg(min)`, then boolean sums. `min` ignores NaN, like SQL `MIN`.
- **Say aloud:** abandonment means no purchase in the same session, not within some time window (Part 8 Q27).
- **Scoring note (Set E2, 10 pts; this book's own rubric, not a company's):** 4 for a correct query, 2 for the seeded edge case, 2 for the pandas version, 1 for stating the assumption, 1 for the check. Full marks: 6 carts, 2 abandoned (0.3333), 1 anomaly (0.1667) with the denominator stated. Partial: right abandoned count on all 8 sessions as the denominator, or the anomaly missing, is partial.

**Follow-ups:**
- *What about a time window?* Count a purchase only if it falls within, say, 24 hours of the first add; then the test becomes a timestamp difference, not just IS NULL (date arithmetic differs by engine, not executed here).
- *How do you quantify the anomaly?* Report it separately and check the instrumentation before cleaning.

**Common mistakes:**
- Using all sessions as the denominator.
- Counting events instead of sessions (s3 would count twice).
- Treating purchase-before-add as a normal conversion without a flag.

