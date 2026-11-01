T = {}
T[1] = """**Say this first (1 line):** DAU, WAU and MAU are each a distinct-user count over a window ending at the as-of date (1, 7 and 30 days, inclusive of the as-of day), so I use `COUNT(DISTINCT user_id)` with the as-of date as a parameter, and I assume UTC timestamps, no week start (WAU is a rolling 7 days, not a calendar week) and test users removed.

**Conventions I state before writing anything:** as-of date 2024-03-31 is a parameter, never `CURRENT_DATE`, so the report can be re-run and reconciled. A "day" is the UTC date of the stored timestamp text (if the business runs on IST I convert first, see Q19 and Q36 in this part for the time-zone cases). WAU is the 7 days ending on the as-of date, so it starts on as-of minus 6 days (2024-03-25) and MAU starts on as-of minus 29 days (2024-03-02); this is a trailing window, so there is no week-start question, but if someone asks for the calendar week I ask whether it starts Monday or Sunday. "Active" means any event; a stricter definition (an intent event only) is a one-line `WHERE` change. Test users are excluded with `is_test = 0`. This schema has no bot flag, so bots are not filtered here; if a user-agent column or bot list exists it is excluded in the same place as test users (see Q37). Events whose user is missing from `users` drop out of the inner join; I would count them separately before trusting the number.

**Schema and sample data:** seven real users and one test user. User 1 has four events (three on the as-of day, one on 03-29). User 4 is active only on 03-24 at 23:59:59 (one second outside the 7-day window). User 6 is active at 2024-03-01 23:59:59 (one second outside the 30-day window). User 5 is active at 2024-03-02 00:00:00 (the first instant inside it). User 7 has an event on 2024-04-01, after the as-of date. One event has a NULL `user_id`.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES
 (1,'2024-01-05','IN',0),(2,'2024-01-20','IN',0),(3,'2024-02-01','US',0),
 (4,'2024-02-10','IN',0),(5,'2024-02-15','IN',0),(6,'2024-02-20','IN',0),
 (7,'2024-03-01','US',0),(99,'2024-01-01','IN',1);
INSERT INTO events VALUES
 (1,'2024-03-31 00:05:00','open'),(1,'2024-03-31 09:00:00','click'),(1,'2024-03-31 23:59:59','click'),
 (2,'2024-03-31 10:00:00','open'),
 (3,'2024-03-25 08:00:00','open'),
 (4,'2024-03-24 23:59:59','open'),
 (5,'2024-03-02 00:00:00','open'),
 (6,'2024-03-01 23:59:59','open'),
 (7,'2024-04-01 00:00:00','open'),
 (99,'2024-03-31 12:00:00','open'),
 (NULL,'2024-03-31 12:30:00','open'),
 (1,'2024-03-29 10:00:00','open');
```

**SQL answer:** `SQL_MAIN` in the Code block. One scan, three conditional distinct counts, half-open windows `[start, as_of + 1 day)` so the whole as-of day is included whatever its time of day:
```sql
{SQL:SQL_MAIN}
```

**pandas answer:** same logic, shown once and identical to the Code block:
```py
{PD}
```

**Example:** non-test events in the windows.
- DAU (03-31): users 1 (three events) and 2. User 99 is test, the NULL-user event never joins. DAU = 2.
- WAU (03-25 to 03-31): add user 3 (03-25) and user 1's 03-29 event (user 1 is already counted). User 4 at 03-24 23:59:59 is one second out. WAU = 3.
- MAU (03-02 to 03-31): add user 4 (03-24) and user 5 (03-02 00:00:00, first instant in). User 6 (03-01 23:59:59) is out, user 7 (04-01) is after the as-of date. MAU = 5.
- `COUNT(*)` instead of `COUNT(DISTINCT)` gives 4 for DAU (user 1 has three events) and 6 for WAU, which is why it is the wrong tool: it measures events, not people.

**Code:** run with `python3 -I`. One row each side; the assert compares the two one-row frames.
```python
{CODE}
```

**Output (my run):**
```text
{OUT}
```

**Edge cases:**
- Boundaries: `BETWEEN :as_of AND :as_of` on timestamp text returned 0 in my run, because `'2024-03-31 10:00:00'` sorts after `'2024-03-31'`. Use `>= as_of` and `< as_of + 1 day` (half-open) on timestamp columns.
- Date arithmetic: `date(:as_of, '-6 days')` and `date(unixepoch(:as_of) - 6*86400, 'unixepoch')` both gave 2024-03-25, and both gave 2024-03-02 for 29 days, in my run. Either works for whole days; never multiply `julianday` by a constant for sub-day windows (Part 7 Q11).
- NULL `user_id`: `COUNT(DISTINCT)` and pandas `nunique()` both skip it (8 and 8 in my run), but `len(set(...))` counted the NaN as a value (9). In pandas, NaN ids merge to nothing here because `users` has none.
- A window with no events returns 0, not NULL, because `COUNT(DISTINCT ...)` of nothing is 0 (my run printed `(0, 0, 0)` for 2023-01-01).
- Incomplete as-of day: if the pipeline has not finished loading 03-31, the DAU is understated. Fix the as-of to the last complete day.
- Test users with `is_test` NULL fail `= 0` and vanish; decide whether NULL means real and use `COALESCE(is_test, 0) = 0` if so.

**Then explain:**
- A user is a person; an event is an action. DAU, WAU and MAU count people, so every one is `COUNT(DISTINCT user_id)`, and a heavy user must count once however many events they fire.
- The as-of date is a parameter so the number is reproducible: run it tomorrow for the same date and get the same answer (late data aside). `CURRENT_DATE` makes yesterday's report change under you and makes tests impossible.
- A 7-day window ending on D inclusive starts on D minus 6; a 30-day window starts on D minus 29. Using minus 7 or minus 30 silently gives an 8-day or 31-day window.
- WAU is at most MAU and DAU is at most WAU by construction, which is a cheap sanity check on any dashboard.
- Dialects (not executed here): PostgreSQL would use `COUNT(DISTINCT user_id) FILTER (WHERE ...)` and `event_ts >= DATE '2024-03-31' - 6`; BigQuery `COUNT(DISTINCT IF(...))` or `COUNTIF` for non-distinct; MySQL `DATE_SUB(:as_of, INTERVAL 6 DAY)`.

**Follow-ups:**
- Calendar-month MAU instead of trailing 30 days? Window `[month_start, next_month_start)`; the two differ (Q15).
- DAU for every day of a month? Needs a date spine so zero days appear (Q15, Q33).
- Why not sum DAU over 7 days to get WAU? Because one person active on three days is counted three times; distinct counts are not additive.

**Common mistakes:**
- `COUNT(*)` (events) instead of `COUNT(DISTINCT user_id)`.
- `BETWEEN '2024-03-25' AND '2024-03-31'` on timestamp text, which drops most of the last day.
- Off-by-one windows (7 days ending D starting D minus 7).
- `CURRENT_DATE` in the query.
- Forgetting test users, or joining with a LEFT JOIN so orphan events inflate the count.
- Summing daily distinct counts to get a weekly number.
"""
T[2] = """**Say this first (1 line):** One scan with `COUNT(DISTINCT CASE WHEN event_name = ... THEN user_id END)` per step gives users per step; step-to-step conversion is each step over the previous one, overall conversion is each step over view users, and this any-order version only checks that a user did each thing at least once, not in order, not within a window, and not that they passed the earlier step.

**Schema and sample data:** eight users. User 1 views twice. User 4 carts twice and purchases twice. User 5 purchases with no view or cart (express checkout or a tracking gap). User 6 carts before viewing (an order violation). User 7 only views, three times.
```sql
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1,'2024-03-01 10:00:00','view'),(1,'2024-03-01 10:01:00','view'),(1,'2024-03-01 10:05:00','cart'),(1,'2024-03-01 10:10:00','purchase'),
 (2,'2024-03-01 11:00:00','view'),(2,'2024-03-01 11:05:00','cart'),
 (3,'2024-03-01 12:00:00','view'),
 (4,'2024-03-02 09:00:00','view'),(4,'2024-03-02 09:05:00','cart'),(4,'2024-03-02 09:06:00','cart'),
 (4,'2024-03-02 09:10:00','purchase'),(4,'2024-03-02 09:11:00','purchase'),
 (5,'2024-03-02 13:00:00','purchase'),
 (6,'2024-03-02 14:00:00','cart'),(6,'2024-03-02 14:05:00','view'),(6,'2024-03-02 14:10:00','purchase'),
 (7,'2024-03-03 08:00:00','view'),(7,'2024-03-03 08:01:00','view'),(7,'2024-03-03 08:02:00','view'),
 (8,'2024-03-03 15:00:00','view'),(8,'2024-03-03 15:05:00','cart');
```

**SQL answer:** `SQL_MAIN` in the Code block. The `s` CTE is the single scan; the three-row result is built from it. `NULLIF` guards a zero denominator.
```sql
{SQL:SQL_MAIN}
```

**pandas answer:** shown once, identical to the Code block:
```py
{PD}
```

**Example:** users per step, any order.
- View: users 1, 2, 3, 4, 6, 7, 8 = 7 (user 5 never viewed).
- Cart: users 1, 2, 4, 6, 8 = 5.
- Purchase: users 1, 4, 5, 6 = 4.
- Cart over view = 5/7 = 71.4%. Purchase over cart = 4/5 = 80.0%. Overall = 4/7 = 57.1%.
- Counting rows gives 10 views, 6 carts and 5 purchases: cart over view 60.0%, purchase over cart 83.3%, overall 50.0%. Every one of those is wrong, because users 1, 4 and 7 repeat events.

**Code:** run with `python3 -I`. Rows are in step order (view, cart, purchase) on both sides; the missing first step conversion is NULL in SQL and NaN in pandas, which `assert_frame_equal` treats as equal.
```python
{CODE}
```

**Output (my run):**
```text
{OUT}
```

**Edge cases:**
- Honest weakness of the any-order version: the 80.0% purchase over cart is contaminated. User 5 purchased without carting, so the 4 purchasers include someone who is not among the 5 carters. Only users 1, 4 and 6 are carters who purchased, which is 3 of 5, or 60.0%. The cumulative fix is Q9 and Q35; the ordered fix is Q7.
- Order is not checked: user 6 carted before viewing and still counts in all three steps.
- No time window: a view in January and a purchase in March count as one converted user.
- Empty table: every `COUNT(DISTINCT ...)` is 0 and `NULLIF` turns the rates into NULL, not a division error (my run printed all NULL rates).
- Rounding: SQLite `ROUND` rounds half away from zero, Python, numpy and pandas `round` round half to even. In my run `ROUND(6.25,1)` gave 6.3 but Python `round(6.25, 1)` and `Series.round(1)` gave 6.2. The sample percentages here are not ties, so the assert passes, but a real tie would differ between the two engines.
- The funnel is only as good as the event names: a renamed event shows up as a sudden drop.

**Then explain:**
- `COUNT(*)` counts events, so a user who views five times counts five times and any step with more repeaters looks bigger. Distinct users is the funnel unit.
- Conditional aggregation computes all steps in one pass over `events`; the alternative of one subquery per step scans the table three times.
- Step-to-step shows where people drop; overall shows how many of the top of the funnel got to the end. Report both with the counts, not only the percentages.
- What it does not check: order, a time window, that earlier steps happened for the same user, session boundaries, and duplicate tracking events.
- Dialects (not executed here): BigQuery `COUNT(DISTINCT IF(event_name = 'view', user_id, NULL))`; PostgreSQL `COUNT(DISTINCT user_id) FILTER (WHERE event_name = 'view')`.

**Follow-ups:**
- Make it ordered? First-of-each or chained timestamps (Q7).
- Add a time window? Q17 (7 days after the first view).
- Per channel? Q8.

**Common mistakes:**
- `COUNT(*)` for steps (60.0, 83.3 and 50.0 above).
- Dividing by the wrong step (overall over the previous step).
- Treating this as a proper funnel when it is a presence table.
- Integer division: `c / v` in SQLite is integer division when both are integers; multiply by `100.0` first.
- Rounding before dividing, or comparing rounded percentages in tests.
"""
T[3] = """**Say this first (1 line):** There is no single paid conversion rate: I ask whether the numerator is users or orders, whether the denominator is all signups or a mature cohort, and over what window, then show (a) users with a completed order over non-test signups, (b) completed orders over orders, and (c) users who paid within 30 days of signup over signups old enough to have had 30 days, and the three differ.

**Clarifying questions and assumptions:** which population (non-test users only)? Does "paid" mean a completed order (cancelled does not count)? Is the denominator everyone who ever signed up, or only users whose window has finished? What window (ever, or 30 days after signup, days 0 to 30 inclusive)? As-of date fixed at 2024-06-30, and I assume data is complete through the end of that day. Time zone: dates are the stored dates; no conversion.

**Schema and sample data:** nine users, one is a test user (user 8, with a 500 order that must not leak in), user 6 signed up on 2024-06-10 (immature), user 9 signed up on 2024-05-31 (exactly 30 days before the as-of date, so mature, and paid on day 30). User 1 has several orders; user 7 never ordered.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, is_test INTEGER);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, order_ts TEXT, amount REAL, status TEXT);
INSERT INTO users VALUES
 (1,'2024-01-10',0),(2,'2024-02-01',0),(3,'2024-03-15',0),(4,'2024-04-01',0),
 (5,'2024-05-20',0),(6,'2024-06-10',0),(7,'2024-02-20',0),(8,'2024-01-05',1),(9,'2024-05-31',0);
INSERT INTO orders VALUES
 (101,1,'2024-01-12 10:00:00',100,'completed'),
 (102,1,'2024-04-02 10:00:00',50,'completed'),
 (103,1,'2024-04-03 10:00:00',70,'cancelled'),
 (104,2,'2024-04-15 10:00:00',80,'completed'),
 (105,3,'2024-03-20 10:00:00',60,'cancelled'),
 (106,3,'2024-03-25 10:00:00',90,'cancelled'),
 (107,4,'2024-04-20 10:00:00',40,'completed'),
 (108,4,'2024-04-21 10:00:00',40,'completed'),
 (109,5,'2024-06-05 10:00:00',55,'completed'),
 (110,6,'2024-06-12 10:00:00',30,'completed'),
 (111,8,'2024-01-06 10:00:00',500,'completed'),
 (113,1,'2024-05-01 10:00:00',25,'completed'),
 (114,9,'2024-06-30 15:00:00',35,'completed'),
 (115,9,'2024-06-02 10:00:00',20,'cancelled');
```

**SQL answer:** `SQL_MAIN` in the Code block, three scalar results side by side from CTEs that already exclude test users. The maturity rule is `signup_date <= date(:as_of, '-30 days')`, so the 30-day window has fully elapsed.
```sql
{SQL:SQL_MAIN}
```
The bug query `SQL_BUG` in the Code block divides a user count by an order count (and an order count by a user count) to show what the mixed-grain versions give.

**pandas answer:** shown once, identical to the Code block:
```py
{PD}
```

**Example:** non-test users are 1 to 7 and 9 (8 users); 13 non-test orders, 9 completed.
- (a) Users with a completed order: 1, 2, 4, 5, 6, 9 = 6 of 8 = 75.0%.
- (b) Completed orders 9 of 13 = 69.2%.
- (c) Mature users (signup on or before 2024-05-31): 1, 2, 3, 4, 5, 7, 9 = 7 (user 6 is excluded as immature). Paid within 30 days: user 1 (01-12, day 2), user 4 (04-20, day 19), user 5 (06-05, day 16), user 9 (06-30, day 30, inclusive) = 4 of 7 = 57.1%. User 2 paid on day 74, too late.
- Bug: 6 users over 13 orders = 46.2%, which answers no question; completed orders over users = 9/8 = 112.5%, a "conversion" above 100%.

**Code:** run with `python3 -I`. The assert compares one-row frames.
```python
{CODE}
```

**Output (my run):**
```text
{OUT}
```

**Edge cases:**
- The test user's completed 500 order is excluded from every numerator and denominator by joining to the non-test list first. Excluding test users only from the denominator would inflate every rate.
- Window boundary: user 9 pays on exactly day 30 and counts because the window is inclusive; the maturity cutoff `date(:as_of, '-30 days')` is 2024-05-31 in my run. If the cutoff were exclusive user 9 would move out of the cohort.
- Orders before signup (data errors) are excluded from (c) by the `>= signup_date` condition.
- Window arithmetic: `date(signup, '+30 days')` and a `unixepoch(...) + 30*86400` comparison matched on this data (7 rows each in my run).
- Cohort with no mature users: the denominator is 0 and the rate is NULL via the scalar division (SQLite returns NULL for division by zero).
- Immature users in (a) and (b) are included, which is why they look better than (c) for young products; see Part 6 Q13 for the immature-cohort trap.

**Then explain:**
- (a) is a user-level ever-converted rate: "what share of everyone who signed up has paid at least once", which keeps rising as cohorts age.
- (b) is an order-level success rate: "what share of orders complete"; it is closer to payment success or cancellation, not to conversion.
- (c) is a fixed-window cohort conversion and is comparable across cohorts, but only for mature ones.
- A numerator and denominator must have the same grain: users over users or orders over orders. 6 users over 13 orders is a ratio with no meaning, and orders over users exceeds 100%.
- Name the metric in the answer: "paid conversion, 30-day, mature, non-test".
- Dialects (not executed here): MySQL `DATE_ADD(signup_date, INTERVAL 30 DAY)` and `DATEDIFF`; PostgreSQL `signup_date + 30`.

**Follow-ups:**
- Per signup month? Group (c) by the cohort month, and report the cohort size and the excluded immature count.
- Why not use a rolling window (any time)? It is the "ever" rate and cannot be compared between cohorts of different age.
- What if cancelled orders were retried? Then a user's first completed order matters, and the rate counts the user once.

**Common mistakes:**
- User numerator over order denominator.
- Not excluding test users from both sides.
- Including users whose 30 days have not elapsed in (c) and calling the recent cohorts bad.
- Counting cancelled orders as paid.
- Using the wrong boundary (days 1 to 30 versus 0 to 30) without saying so.
"""
