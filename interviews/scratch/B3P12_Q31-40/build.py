import re, subprocess, pathlib
root = pathlib.Path(__file__).parent
part = pathlib.Path("/home/user/case_studies/interviews/Book3_SQL/Book3_SQL_Part12.md").read_text().split("\n")

def head(n):
    i = next(k for k, l in enumerate(part) if l.startswith(f"### Q{n} "))
    assert part[i+1].startswith("**Asked at:**")
    return part[i] + "\n" + part[i+1]

def pts(p):
    if p == 10: return "4 for a correct query, 2 for the seeded edge case, 2 for the pandas version, 1 for stating the assumption, 1 for the check"
    return "8 for a correct query, 4 for the seeded edge case, 4 for the pandas version, 2 for stating the assumption, 2 for the check"

def score(setname, p, full, partial):
    return (f"- **Scoring note (Set {setname}, {p} pts; this book's own rubric, not a company's):** {pts(p)}. "
            f"Full marks: {full} Partial: {partial}")

Q = {}
Q[31] = dict(set="E2", p=20,
say="Join on the coupon code only (in ON), keep every order, then decide the status with a CASE that compares the order date to the coupon window with inclusive ends; the date test never goes in WHERE.",
schema="""```sql
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
Orders 1 and 2 sit exactly on the start and end date of SAVE10, order 5 is on the last day of FLASH, order 3 is one day before the window and order 4 one day after.""",
sql="sql_answer",
sqlnote="The code match is the only join condition, so an order with a bad or missing code keeps its row and `c.code` is NULL. The date test is in the CASE (and inside the discount expression), not in WHERE. `BETWEEN` is inclusive on both ends, which is what makes the start and end dates VALID. ISO date text compares correctly as text; in a real schema the columns are DATE.",
example="Order 1 is on 2025-03-01: the join finds SAVE10, `order_date < start_date` is false and `order_date > end_date` is false, so VALID, and 100 * (100 - 10) / 100.0 = 90. Order 2 on 2025-03-31 is the end date, not after it, so VALID, 180. Order 3 (02-28) is before the start: NOT_STARTED. Order 4 (04-01) is after the end: EXPIRED. Order 5 (FLASH, 03-12) is VALID, 80 * 0.75 = 60. Order 6's code BOGUS finds no coupon row: UNKNOWN_CODE. Order 7 has a NULL code: NO_COUPON, which must be tested first because the join then also has no coupon row.",
edge="""- **WHERE instead of ON:** putting the date test in WHERE turns the LEFT JOIN into an inner join: only 3 of the 7 orders survive (orders 1, 2, 5). Cross-reference Part 2 Q3.
- **Date test inside ON:** it keeps all 7 rows but the coupon columns come back NULL for orders 3, 4 and 6 alike, so you cannot tell EXPIRED or NOT_STARTED from UNKNOWN_CODE. Put the code match in ON and classify afterwards.
- **Order of the CASE:** NO_COUPON before UNKNOWN_CODE, because both have a NULL `c.code`.
- **Duplicate code rows:** `code` is the primary key here. If a code could have several windows (re-runs of a campaign) the join would duplicate orders; then join on the window too and treat no match as the not-valid case, or pick one window per order with a window function.
- **Timestamps:** an `order_date` that carries a time of day breaks an inclusive `BETWEEN` against a pure date end (the end day after 00:00 would look expired). Compare against `end_date + 1 day` with `<` for timestamps (not executed here).
- **Case or spaces in codes:** 'save10' would be UNKNOWN_CODE; clean with `UPPER(TRIM())` if the data is user-typed (UPPER is ASCII-only in SQLite).""",
explain=lambda: ["- **The WHERE-versus-ON rule:** a condition on the right table in WHERE removes the NULL-extended rows; a condition in ON only decides what matches. Here the code match belongs in ON and the classification is a CASE over the joined columns.",
 "- **Inclusive ends** are the whole point of the seed: `<` and `>` for the invalid sides, so the boundary dates fall through to VALID.",
 "- **pandas:** `merge(how=\"left\")` then `np.select` with conditions in the same order as the CASE (first true wins, like CASE). The discount is `where(status == VALID)`, which gives NaN like the CASE without ELSE.",
 score("E2", 20, "all five statuses are right on the seeded boundary dates (orders 1, 2, 5 VALID), the join keeps 7 rows, and you say why the test is not in WHERE.", "a correct VALID/EXPIRED split but an inner join (the NO_COUPON and UNKNOWN_CODE orders lost) is about half of the query marks; date test in ON gets the rows but not the reasons.")],
fups="""- *What if the discount must be capped?* Wrap in `MIN(discount, cap)` using the scalar two-argument `MIN` in SQLite (a different function from the aggregate; other engines use `LEAST`, not executed here).
- *What if an order can carry several coupons?* Move codes to an `order_coupons` table; then the join fans out, so decide whether to stack or choose the best and aggregate per order.
- *How do you check the result?* Row count out equals row count in (7), and the VALID count equals the count from an inner join with the dates in ON.""",
mistakes="""- Date condition in WHERE, silently dropping the orders without a valid coupon.
- Using `BETWEEN` for the exclusive sides or `<=` on the end, making the boundary dates EXPIRED.
- Testing `coupon_code = NULL` instead of `IS NULL`.
- Computing the discount as `amount * pct_off / 100` (that is the discount, not the discounted amount) or with integer division.""")

Q[32] = dict(set="E2", p=20,
say="De-duplicate to distinct (order, product) first, self join on the same order with `a.product_id < b.product_id` so each pair appears once, group by the pair and keep `COUNT(*) >= 2`.",
schema="""```sql
CREATE TABLE order_items(order_id INTEGER, product_id TEXT);
INSERT INTO order_items VALUES
 (1,'A'),(1,'B'),(1,'C'),
 (2,'A'),(2,'B'),
 (3,'A'),(3,'B'),(3,'B'),
 (4,'B'),(4,'C'),
 (5,'A'),(5,'C'),
 (6,'D');
```
Order 3 holds product B twice (the duplicate row); order 6 has a single item.""",
sql="sql_answer",
sqlnote="`DISTINCT` in the CTE makes one row per product per order, so every joined row is one order containing both products and `COUNT(*)` is the number of orders. The `<` condition keeps (A, B) and drops (B, A) and (A, A).",
example="Distinct items: order 1 {A,B,C}, 2 {A,B}, 3 {A,B}, 4 {B,C}, 5 {A,C}, 6 {D}. Pairs per order: order 1 gives AB, AC, BC; order 2 gives AB; order 3 gives AB; order 4 gives BC; order 5 gives AC; order 6 gives none. Totals: AB 3, AC 2, BC 2, all at least 2. Without the DISTINCT, order 3's two B rows pair with its A row twice, so AB becomes 4: the naive query overstates by exactly the duplicate.",
edge="""- **Duplicate rows:** the seeded duplicate moves AB from 3 to 4 without DISTINCT (shown in the output). Alternative: count `COUNT(DISTINCT a.order_id)` and skip the CTE.
- **Single-item orders** (order 6) create no pair, which is correct; they just do not appear.
- **Ties:** AC and BC both have 2, so the secondary sort `p1, p2` makes the order deterministic.
- **Scale:** the self join makes k*(k-1)/2 rows per order of k items, so a 50-item basket gives 1,225 rows; cap basket size or sample before running this on real data.
- **Empty result:** if no pair reaches 2 the query returns zero rows, not a row of zeros.""",
explain=lambda: ["- **Why `<` and not `<>`:** `<>` returns both (A, B) and (B, A), doubling every count and needing a later de-duplication; `<` is a canonical ordering of the pair (Part 2 Q37).",
 "- **Why distinct first:** the unit being counted is an order, and a duplicate line must not count twice.",
 "- **pandas:** `drop_duplicates()`, merge the table with itself on `order_id`, filter `product_id_1 < product_id_2`, `groupby(...).size()`, then filter and sort. The assertion compares in the stated order: count descending, then p1, p2 (no re-sorting needed).",
 "- **Alternative (not run):** `itertools.combinations` over each order's sorted distinct products and a `Counter`; same answer, better memory behaviour for big baskets.",
 score("E2", 20, "the pair list is AB 3, AC 2, BC 2 in that order, each pair once, with the duplicate handled and said aloud.", "a self join that returns both (A,B) and (B,A), or counts AB as 4, keeps most of the query marks but loses the edge-case marks.")],
fups="""- *What would you add for recommendations?* Support and lift: pair count divided by the number of orders containing each product (orders with A: 4, with B: 4 here), not just raw counts.
- *How do you make it faster?* An index on `(order_id, product_id)` and a pre-filter to products with at least 2 orders, since a pair needs both products to qualify.
- *Triples?* Add a third alias with `b.product_id < c.product_id`; the same duplicate rule applies.""",
mistakes="""- `a.product_id <> b.product_id`, which doubles the counts.
- Counting rows instead of distinct orders, so duplicates inflate the pair.
- Putting `COUNT(*) >= 2` in WHERE instead of HAVING.
- Forgetting the tie-break, so the printed order changes between runs.""")

Q[33] = dict(set="F1", p=10,
say="Inner join events to the non-test users, take `COUNT(DISTINCT user_id)` per day, and LEFT JOIN that onto a generated calendar so a day with only test users shows 0; an unknown user_id is excluded and I say so.",
schema="""```sql
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
Users 3 and 5 are test accounts; user 99 is not in `users`.""",
sql="sql_answer",
sqlnote="The recursive CTE builds the 5-day calendar (Part 9 shape; a calendar table does the same). The join to `users` with `is_test = 0` is an inner join, so unknown users are dropped as well as test users. `date(event_ts)` cuts the text timestamp to the day.",
example="2025-06-01: events from users 1 (three of them) and 2, so 2 distinct users. 06-02: test user 3 is out, user 4 stays: 1. 06-03: only test users 3 and 5 are active, so after the filter no event is left and the LEFT JOIN from the calendar gives 0. 06-04: users 4 and 1: 2. 06-05: user 99 is unknown and dropped, user 6 stays: 1.",
edge="""- **Several events per user per day:** `COUNT(DISTINCT user_id)`; plain `COUNT(*)` would give 4 for 06-01.
- **Day with no real activity:** the calendar LEFT JOIN is what produces the 0 for 06-03; without it the day is missing.
- **Unknown user_id (my decision):** excluded, because I cannot show it is not a test account. The alternative `LEFT JOIN users ... WHERE u.is_test IS NOT 1` keeps user 99 and gives 2 for 06-05 (printed in the output); say which you chose. A NULL `is_test` falls in the same fork: `is_test = 0` excludes it, `IS NOT 1` keeps it.
- **Time zones:** `date(event_ts)` cuts the stored text, so the day is whatever zone the text is in (assume UTC here).
- **Filter in ON, not WHERE:** the `is_test = 0` test is inside the inner join; putting a right-table filter in WHERE after the calendar LEFT JOIN would drop the zero day.""",
explain=lambda: ["- **DAU definition:** distinct users with at least one event in the day (Part 8 Q1), not event count.",
 "- **pandas:** inner `merge` to non-test users, `nunique` per day string, then `reindex` on a full `date_range` with `fill_value=0`; `reindex` is the pandas version of the calendar LEFT JOIN.",
 score("F1", 10, "DAU 2, 1, 0, 2, 1 with the zero day present, and the unknown-user decision stated.", "correct counts but a missing 06-03 row (no calendar) loses the edge-case marks; counting events instead of users fails the main query.")],
fups="""- *How would you do MAU?* Same shape on a month key, or a rolling 30-day distinct count (Part 8 Q7 style; windows with DISTINCT are not available in SQLite, so a self join or a pre-deduplicated day table is needed).
- *How do you flag unknown ids?* A separate query: events where `user_id NOT IN` (or NOT EXISTS) users, reported to the data owners.""",
mistakes="""- `COUNT(user_id)` instead of `COUNT(DISTINCT user_id)`.
- Filtering test users in WHERE after the calendar join, which deletes the zero days.
- Silently keeping unknown ids because a LEFT JOIN plus `is_test <> 1` ignores NULLs (NULL <> 1 is NULL, so the row disappears, the opposite of what many expect).""")

Q[34] = dict(set="F2", p=10,
say="LEFT JOIN clicks onto impressions, `COALESCE(clicks, 0)` for the missing click row, divide by `NULLIF(impressions, 0)` so zero impressions gives NULL, then round to 4 decimals.",
schema="""```sql
CREATE TABLE impressions(campaign_id INTEGER, impressions INTEGER);
CREATE TABLE clicks(campaign_id INTEGER, clicks INTEGER);
INSERT INTO impressions VALUES (1,1000),(2,500),(3,0),(4,200),(5,7),(6,0);
INSERT INTO clicks VALUES (1,37),(3,0),(4,5),(5,3);
```
Campaign 2 has no click row; campaigns 3 and 6 have 0 impressions (6 also has no click row).""",
sql="sql_answer",
sqlnote="`* 1.0` forces real division (integer division would give 0). Zero impressions makes `NULLIF` return NULL and the whole ratio NULL; a missing click row becomes 0 via `COALESCE`, which only affects the numerator.",
example="Campaign 1: 37 / 1000 = 0.037, printed 0.0370. Campaign 2: no click row, COALESCE gives 0, 0 / 500 = 0. Campaign 3: 0 impressions, so 0 / NULL = NULL. Campaign 4: 5 / 200 = 0.025. Campaign 5: 3 / 7 = 0.428571, rounded 0.4286. Campaign 6: no click row and 0 impressions: NULL (impressions rule wins).",
edge="""- **Zero impressions:** SQLite returns NULL for `x / 0` (shown: `3*1.0/0` and `0*1.0/0` both NULL); Postgres raises "division by zero" and MySQL returns NULL in default mode (both not executed here), so the `NULLIF` guard is the portable version.
- **No click row versus 0 clicks:** both end up 0; a missing row is an absent fact, and treating it as 0 is an assumption to say aloud.
- **Several click rows per campaign:** the join would duplicate impression rows; aggregate clicks per campaign first (Part 8 Q10).
- **Rounding:** `ROUND` in SQLite and pandas can differ on exact halves (Part 10 lesson: 703.125 rounds to 703.13 in SQLite and 703.12 in pandas); no seeded value here is a half, so the assertion is safe.""",
explain=lambda: ["- **Why NULL, not 0, for no impressions:** the rate is undefined, and 0 would say the campaign performed badly (Part 1 Q6).",
 "- **pandas difference:** `3.0 / 0.0` gives `inf`, not NaN (printed), so zero is replaced with NaN before dividing; `0/0` is NaN. SQL gives NULL for both without help.",
 score("F2", 10, "both guards in the right places (NULLIF on the denominator, COALESCE on the numerator) with 0.0370, 0, NULL, 0.0250, 0.4286, NULL.", "forgetting the `* 1.0` (all zeros) or a COALESCE on the whole ratio (returns 0 for zero impressions) is partial.")],
fups="""- *Why not `WHERE impressions > 0`?* It drops the campaign instead of reporting it as undefined.
- *CTR across campaigns?* Sum clicks over sum impressions (a weighted rate), not the mean of the per-campaign CTRs.""",
mistakes="""- Integer division giving 0.
- `COALESCE(ctr, 0)` around the ratio, hiding the undefined case as 0.
- Inner joining clicks, losing campaign 2.""")

Q[35] = dict(set="F3", p=10,
say="`NOT EXISTS` with the 2025 date range inside the subquery returns the right customers; `NOT IN` returns nothing as soon as the subquery contains one NULL, because `x NOT IN (..., NULL)` is never true.",
schema="""```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER, customer_id INTEGER, order_date TEXT);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Esha'),(6,'Farid');
INSERT INTO orders VALUES
 (1, 1, '2025-01-10'), (2, 2, '2025-06-01'), (3, 3, '2024-12-31'),
 (4, NULL, '2025-03-03'), (5, 1, '2025-07-07'), (6, 5, '2026-01-01');
```
Order 4 is a 2025 order with a NULL customer_id.""",
sql="sql_answer",
sqlnote="The `NOT IN` version and its repaired form are in the Code block as `sql_not_in` and `sql_not_in_fixed`. The date range is `>= '2025-01-01' AND < '2026-01-01'` so it also works if `order_date` has a time part.",
example="2025 orders belong to customers 1 (two orders), 2 and NULL. So Asha and Ben have orders; Chitra's order is 2024-12-31 and Esha's is 2026-01-01, both outside 2025; Dev and Farid have none. The answer is Chitra, Dev, Esha, Farid. With NOT IN the list is (1, 2, NULL, 1): for Chitra, `3 NOT IN (1,2,NULL)` is `3<>1 AND 3<>2 AND 3<>NULL`, which is TRUE AND TRUE AND UNKNOWN = UNKNOWN, so no row is returned for anyone.",
edge="""- **NULL in the subquery:** NOT IN returns 0 rows (printed); filtering `customer_id IS NOT NULL` inside the subquery fixes it (4 rows).
- **Empty subquery:** NOT IN on an empty list is TRUE for everyone, so the NULL trap only appears when there is data.
- **NULL on the outer side:** a customer with NULL id would also never match NOT IN; here the key is a primary key.
- **pandas:** `~isin` treats NaN as an ordinary value and does not poison the test, so pandas returns the right 4 rows even with the NaN in the list, a difference from SQL (printed). The column is float64 because read_sql turns a NULL integer into NaN.
- **Year boundary:** 2024-12-31 and 2026-01-01 are excluded by the range; a `BETWEEN '2025-01-01' AND '2025-12-31'` would miss 2025-12-31 18:00 on a timestamp column.""",
explain=lambda: ["- **Three-valued logic:** NOT IN expands to a chain of `<>` joined by AND; one UNKNOWN makes the whole chain UNKNOWN, and WHERE keeps only TRUE (Part 2 Q2, Part 3 Q3).",
 "- **NOT EXISTS** compares per row and ignores the NULL row because `o.customer_id = c.customer_id` is UNKNOWN for it, so it never matches.",
 "- **Alternative:** `LEFT JOIN ... WHERE o.order_id IS NULL` with the 2025 test in ON (not run here separately).",
 score("F3", 10, "the 4 correct customers by NOT EXISTS, the demonstration that NOT IN returns 0 rows, and the one-line reason.", "the right customers but no explanation of the NULL, or a NOT IN answer that happens to work only because the seed has no NULL, is partial.")],
fups="""- *Can you keep NOT IN?* Yes if the subquery column is NOT NULL by constraint or filtered with `IS NOT NULL`, but NOT EXISTS is safer.
- *Performance?* Modern planners often turn NOT EXISTS into an anti-join; confirm with EXPLAIN (Part 11), engine-specific, not executed here for other engines.""",
mistakes="""- Using NOT IN on a nullable column.
- Putting the year filter in the outer WHERE instead of the subquery, which changes the meaning.
- Using `BETWEEN` with a year-end date on timestamps.""")

Q[36] = dict(set="T1", p=10,
say="Conditional aggregation: `COUNT(*)` for attempts, `SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END)` for successes, then divide by `COUNT(*)` (NULL counted as not success) and by `NULLIF(COUNT(status), 0)` (NULL excluded).",
schema="""```sql
CREATE TABLE payments(payment_id INTEGER, merchant_id TEXT, status TEXT);
INSERT INTO payments VALUES
 (1,'m1','SUCCESS'),(2,'m1','SUCCESS'),(3,'m1','FAILED'),(4,'m1',NULL),
 (5,'m2','SUCCESS'),(6,'m2','FAILED'),
 (7,'m3',NULL),(8,'m3',NULL);
```
Merchant m3 has only NULL statuses.""",
sql="sql_answer",
sqlnote="`COUNT(*)` counts rows, `COUNT(status)` counts non-NULL statuses. The CASE has an ELSE 0 so NULL status counts as not success (without ELSE the SUM would still ignore NULL; the ELSE makes the intent visible and keeps an all-NULL merchant at 0 instead of NULL).",
example="m1: 4 attempts, successes = 2, rate_all = 2 / 4 = 0.5, known statuses = 3 (the NULL is out) so rate_known = 2 / 3 = 0.6667. m2: 2 attempts, 1 success, both rates 0.5. m3: 2 attempts, 0 successes, rate_all = 0 / 2 = 0, rate_known = 0 / NULLIF(0, 0) = NULL.",
edge="""- **NULL status:** a pending or unknown payment; the two columns are the two policies, and which one is right is a business decision (say it).
- **All-NULL merchant:** rate_all 0.0 but rate_known undefined (NULL/NaN), a distinction the output shows.
- **The trap:** `WHERE status <> 'SUCCESS'` returns only the 2 FAILED rows; the 3 NULL-status rows vanish because NULL <> 'SUCCESS' is UNKNOWN (printed).
- **Case or spelling** of status values ('Success') would count as not success; normalise first if the data is messy.""",
explain=lambda: ["- **Denominators:** attempts (all rows) versus decided payments (non-NULL). Reporting both is the safe answer (Part 1 Q10).",
 "- **pandas:** a 0/1 helper column, `agg` with named aggregations, `size` for rows and `count` for non-NaN; `count` on a column already excludes NaN, which is the pandas mirror of `COUNT(status)`. Zero is replaced by NaN before dividing, as in Q34.",
 score("T1", 10, "attempts 4/2/2, successes 2/1/0, both rate columns right including the NULL for m3.", "one rate column correct and the other wrong denominator, or ignoring the NULL status trap, is partial.")],
fups="""- *Where would failed-versus-pending matter?* In a payments funnel the NULL could mean in-flight; exclude payments newer than the settlement window rather than counting them as failures.
- *Can you use FILTER?* `COUNT(*) FILTER (WHERE status = 'SUCCESS')` runs on SQLite 3.30 and later and on PostgreSQL; MySQL has no FILTER (not executed here).""",
mistakes="""- `AVG(status = 'SUCCESS')`, which ignores NULL rows silently and gives the second policy by accident.
- Integer division in the rate.
- Dropping NULL rows in WHERE before counting attempts.""")

Q[37] = dict(set="T2", p=10,
say="Aggregate repayments to one row per loan first, LEFT JOIN that to loans, `COALESCE(paid, 0)`, outstanding is principal minus paid and a loan is overpaid when paid is greater than principal.",
schema="""```sql
CREATE TABLE loans(loan_id INTEGER PRIMARY KEY, principal INTEGER);
CREATE TABLE repayments(repayment_id INTEGER, loan_id INTEGER, amount INTEGER);
INSERT INTO loans VALUES (1,1000),(2,500),(3,800),(4,600),(5,300);
INSERT INTO repayments VALUES (1,1,400),(2,1,300),(3,3,800),(4,4,700),(5,5,100),(6,99,50);
```
Loan 2 has no repayment, loan 4 is overpaid, and repayment 6 refers to a loan that does not exist.""",
sql="sql_answer",
sqlnote="The inner subquery makes one row per loan, so the join cannot multiply loans. `COALESCE` turns the missing aggregate for loan 2 into 0. The outstanding amount is negative for the overpaid loan; the flag marks it.",
example="Loan 1: repayments 400 + 300 = 700, outstanding 1000 - 700 = 300. Loan 2: no row, paid 0, outstanding 500. Loan 3: 800, outstanding 0, not overpaid (equal is fully paid). Loan 4: 700 against 600, outstanding -100, overpaid 1. Loan 5: 100, outstanding 200. The orphan repayment for loan 99 matches no loan and disappears from a LEFT JOIN starting at loans.",
edge="""- **Fan-out:** joining raw repayments to loans repeats loan 1's principal on two rows, so `SUM(principal)` becomes 4,200 instead of 3,200 (printed). Pre-aggregation avoids it (Part 8 Q11).
- **No repayments:** loan 2 gets 0, not NULL, thanks to COALESCE; `principal - NULL` would otherwise be NULL.
- **Exactly paid:** paid equals principal is not overpaid (strict `>`).
- **Orphan rows:** repayment 99 is excluded here; reconciling it is a separate check (anti-join from repayments to loans).
- **Money types:** integers here; real money should be integer minor units or DECIMAL, not floats.""",
explain=lambda: ["- **Why pre-aggregate:** the question wants one row per loan; aggregate the many side before the join (Part 2 Q5).",
 "- **pandas:** `groupby.sum`, left `merge`, `fillna(0).astype(int)` (the merge makes `paid` float because of NaN), then vectorised arithmetic.",
 score("T2", 10, "all five loans including loan 2 at 0 paid and loan 4 flagged, without fan-out.", "correct numbers but NULL instead of 0 for loan 2, or an unflagged overpayment, is partial.")],
fups="""- *How do you find repayments for missing loans?* `LEFT JOIN repayments to loans WHERE l.loan_id IS NULL` (loan 99, amount 50).
- *Time-aware balance?* Add a running sum of repayments by date (Part 5), as of a cut-off date.""",
mistakes="""- Joining raw repayments and summing principal.
- Inner join, dropping unpaid loans.
- Using `>=` for overpaid.""")

Q[38] = dict(set="T3", p=10,
say="Reduce to distinct (customer, month), get each customer's first month, then per month count customers whose month equals the first month (new) and those where it is later (returning).",
schema="""```sql
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
16 rows, 12 distinct customer-months, with duplicate rows on the same day and customer 2 silent in February.""",
sql="sql_answer",
sqlnote="`SUBSTR(activity_date, 1, 7)` gives the 'YYYY-MM' key; the month strings sort correctly as text. `DISTINCT` removes the duplicate rows so a customer counts once per month.",
example="Distinct customer-months: January {1, 2, 6}, February {1, 3, 4, 6}, March {1, 2, 4, 5, 7}. First months: 1, 2 and 6 in January; 3 and 4 in February; 5 and 7 in March. January: 3 new, 0 returning. February: 3 and 4 are new, 1 and 6 are returning: 2 and 2. March: 5 and 7 are new, 1, 2 and 4 are returning (customer 2 skipped February and still counts as returning): 2 and 3.",
edge="""- **Duplicates:** 16 rows collapse to 12 customer-months; the sanity line shows new + returning also totals 12.
- **Gap months:** customer 2 returns in March after a silent February; "returning" means active earlier, not active last month.
- **Month boundary:** customer 6 is active on 01-31 and 02-01, so one in each month.
- **First activity outside the window:** with only Jan to Mar data, a customer whose real first activity was in 2024 would be labelled new in January; the "first ever" needs full history, not just the window.
- **A month with no activity** would not appear; join to a month calendar if zero rows are needed (as in Q33).""",
explain=lambda: ["- **Definition:** new = first ever activity month equals this month; returning = first month earlier than this month (Part 6 Q14).",
 "- **pandas:** `drop_duplicates`, `groupby(...).transform('min')` for each customer's first month, two 0/1 helper columns and a grouped sum. `transform` keeps the row count, which is what a window `MIN() OVER` gives in SQL.",
 score("T3", 10, "3/0, 2/2, 2/3 with duplicates removed and customer 2 counted as returning in March.", "a count that includes duplicate rows, or a returning definition that requires activity in the previous month, is partial.")],
fups="""- *Retention rate?* Returning customers in month m divided by active customers in month m-1 (a different definition, Part 6 Q10).
- *Why use the month text and not a date function?* Text `YYYY-MM` is portable and sorts; `DATE_TRUNC` exists in PostgreSQL, BigQuery and Snowflake but not in SQLite (not executed here).""",
mistakes="""- Counting rows instead of distinct customers.
- Calling someone new in every month because the first-month lookup is done per month instead of overall.
- Using the min over the filtered window only.""")

Q[39] = dict(set="E1", p=10,
say="`COUNT(*)` counts rows, `COUNT(amount)` counts non-NULL amounts, `SUM` and `AVG` skip NULLs, so the average is over the orders that have an amount, not over all orders.",
schema="""```sql
CREATE TABLE orders(order_id INTEGER, customer_id INTEGER, status TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'DELIVERED',100),(2,2,'DELIVERED',200),(3,3,'DELIVERED',NULL),
 (4,4,'CANCELLED',NULL),(5,5,'CANCELLED',50),(6,6,'CANCELLED',NULL),
 (7,7,'RETURNED',80),
 (8,8,'SHIPPED',NULL);
```
SHIPPED has a single order with a NULL amount.""",
sql="sql_answer",
sqlnote="No CASE needed: the aggregates' NULL rules do the work. The SHIPPED group is the one where every amount is NULL.",
example="DELIVERED: 3 orders, 2 with an amount (100, 200), revenue 300, average 300 / 2 = 150 (not 300 / 3 = 100). CANCELLED: 3 orders, 1 amount (50), revenue 50, average 50. RETURNED: 1 order, 80, 80. SHIPPED: 1 order, 0 amounts, SUM and AVG are NULL (no value, not 0).",
edge="""- **All-NULL group:** SQL `SUM` is NULL and `AVG` is NULL for SHIPPED; pandas plain `sum()` gives 0.0 (printed). The assertion therefore uses `sum(min_count=1)`.
- **Wrong average:** `SUM / COUNT(*)` gives 100 for DELIVERED instead of 150 (printed); that treats a missing amount as 0, a decision, not a default.
- **Zero versus NULL:** an order with amount 0 would be counted by COUNT(amount) and lower the average; NULL would not.
- **pandas `mean(skipna=False)`** over the whole column gives NaN (printed), as one NULL poisons the result.""",
explain=lambda: ["- **SQL rule:** aggregates ignore NULL inputs except `COUNT(*)`; with no non-NULL input `SUM` and `AVG` return NULL and `COUNT(col)` returns 0 (Part 1 Q4).",
 "- **pandas:** `size` counts rows, `count` counts non-NaN (the `COUNT(*)` and `COUNT(col)` pair); `mean` skips NaN by default; `sum` skips NaN but returns 0.0 for an all-NaN group unless `min_count=1`.",
 score("E1", 10, "orders 3/3/1/1, with-amount 2/1/1/0, revenue 300/50/80/NULL, averages 150/50/80/NULL and the reason the DELIVERED average is 150.", "right counts but an average computed over all rows, or a 0 for SHIPPED revenue without comment, is partial.")],
fups="""- *How would you treat NULL as 0 on purpose?* `AVG(COALESCE(amount, 0))`, only if the business says a missing amount means free.
- *Why do the status groups not add to 8 with amounts?* Four orders have no amount; orders_with_amount sums to 4.""",
mistakes="""- Dividing `SUM` by `COUNT(*)`.
- Reading NULL revenue as 0 in a report.
- In pandas, using `len` or `size` when `count` is meant, or trusting `sum()` for an all-NaN group.""")

Q[40] = dict(set="E2", p=10,
say="Per session take the first add_to_cart time and first purchase time with conditional aggregation; among sessions with an add, abandoned means no purchase at all and the anomaly means the first purchase is earlier than the first add.",
schema="""```sql
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
8 sessions: s6 never adds anything, s7 purchases without an add, s4 buys before it adds, s8 adds and buys at the same second.""",
sql="sql_answer",
sqlnote="The denominator is sessions with at least one add_to_cart (6). Abandoned = no purchase event at all in the session; the EXISTS formulation (`sql_exists` in the Code block) gives the same counts.",
example="Sessions with an add: s1, s2, s3, s4, s5, s8 = 6. s2 and s3 never purchase: abandoned 2, rate 2 / 6 = 0.3333 (s3's two adds still count as one session). s4's first purchase (09:00) is before its first add (09:30): 1 anomaly, 1 / 6 = 0.1667. s5 buys at 10:30 after its first add at 10:00 and re-adds at 10:40: not an anomaly. s8's add and purchase share a timestamp, a tie, so not counted as before. s6 and s7 have no add and stay out of the denominator.",
edge="""- **Denominator:** only sessions with an add; including s6 and s7 would give 2 / 8 = 0.25, a different metric.
- **Repeat adds:** `MIN` per session means a session counts once.
- **Purchase before add (s4):** it has a purchase, so it is not abandoned under this definition; it is a separate anomaly, probably clock skew or missing events, and I report it rather than fix it.
- **Ties:** equal timestamps are not "before" (strict `<`).
- **Purchase between adds (s5):** a later add after the purchase is allowed; the first-add rule ignores it.
- **Timestamps as text:** the same-format ISO text compares correctly; mixed formats would not.""",
explain=lambda: ["- **Two equivalent forms:** conditional aggregation over a per-session CTE (above) or `EXISTS` for the purchase test; the EXISTS output matches (printed). I would pick the CTE when I also need the anomaly, as it computes both in one pass.",
 "- **pandas:** put the timestamp in two helper columns with `where`, `groupby.agg(min)`, then boolean sums. `min` ignores NaN, like SQL `MIN`.",
 "- **Say aloud:** abandonment means no purchase in the same session, not within some time window (Part 8 Q27).",
 score("E2", 10, "6 carts, 2 abandoned (0.3333), 1 anomaly (0.1667) with the denominator stated.", "right abandoned count on all 8 sessions as the denominator, or the anomaly missing, is partial.")],
fups="""- *What about a time window?* Count a purchase only if it falls within, say, 24 hours of the first add; then the test becomes a timestamp difference, not just IS NULL (date arithmetic differs by engine, not executed here).
- *How do you quantify the anomaly?* Report it separately and check the instrumentation before cleaning.""",
mistakes="""- Using all sessions as the denominator.
- Counting events instead of sessions (s3 would count twice).
- Treating purchase-before-add as a normal conversion without a flag.""")

def sqlvar(code, name):
    m = re.search(rf'^{name} = """(.*?)"""', code, re.S | re.M)
    return m.group(1).strip("\n")

out = ["# B3 Part 12, Q31-Q40 answers (Wave B)", ""]
for n in range(31, 41):
    d = Q[n]
    f = root / "code" / f"q{n}.py"
    code = f.read_text()
    r = subprocess.run(["python3", "-I", str(f)], capture_output=True, text=True, cwd=str(root / "code"))
    assert r.returncode == 0, r.stderr
    output = r.stdout.rstrip("\n")
    pd_code = code.split("# --- pandas\n")[1].split("# --- end pandas")[0].rstrip("\n")
    out += [head(n), f"**Say this first (1 line):** {d['say']}", "",
            "**Schema and sample data:**", d["schema"], "",
            "**SQL answer:** the query below is the `" + d["sql"] + "` string in the Code block (same text).",
            "```sql", sqlvar(code, d["sql"]), "```", d["sqlnote"], "",
            "**pandas answer:** the same text as the pandas part of the Code block.",
            "```py", pd_code, "```", "",
            "**Example:** " + d["example"], "",
            "**Code:** run with `python3 -I`; it creates the data, runs the SQL and the pandas version and asserts they are equal.",
            "```python", code.rstrip("\n"), "```", "",
            "**Output (my run):**", "```text", output, "```", "",
            "**Edge cases:**", d["edge"], "",
            "**Then explain:**"] + d["explain"]() + ["",
            "**Follow-ups:**", d["fups"], "",
            "**Common mistakes:**", d["mistakes"], "", ""]
(root / "answers.md").write_text("\n".join(out))
print("ok")
