import re, subprocess, os
ROOT = "/home/user/case_studies/interviews"
part = open(f"{ROOT}/Book3_SQL/Book3_SQL_Part12.md", encoding="utf-8").read().split("\n")
def head(n):
    i = next(k for k, l in enumerate(part) if l.startswith(f"### Q{n} "))
    assert part[i + 1].startswith("**Asked at:**")
    return part[i], part[i + 1]
def var(src, name):
    m = re.search(name + r' = """(.*?)"""', src, re.S)
    return m.group(1).strip("\n")
def pandas_block(src):
    m = re.search(r"# PANDAS START\n(.*?)# PANDAS END", src, re.S)
    return m.group(1).rstrip("\n")

P = {}
def q(n, **kw): P[n] = kw
def sc(setn, pts_note): return pts_note

q(21,
say="Build a month spine (Jan to May) so April exists, LEFT JOIN the orders and `COALESCE` the sum to 0, then `LAG` the previous month and divide by `NULLIF(prev, 0)`, so growth is NULL when there is nothing to grow from.",
example="""Orders: Jan 100 + 50 = 150, Feb 200, Mar 150 + 50 = 200, Apr none, May 120. Spine row 2025-04 finds no orders, so the sum is NULL and `COALESCE` makes it 0. Growth Feb = (200 - 150) / 150 = 33.3 percent. Mar = (200 - 200) / 200 = 0.0. Apr = (0 - 200) / 200 = -100.0. May's previous month is 0, so `NULLIF(0, 0)` is NULL and the growth is NULL (not 0, not infinite). Jan has no previous row, so `LAG` gives NULL and growth is NULL too.""",
extra_sql_name=None,
edge="""- Missing month: without the spine the April row simply does not exist, and May's `LAG` would then point at March (growth 120 versus 200 would be wrong). In pandas, `resample("MS")` fills inner gaps with 0 for free, but it stops at the last month that has data; the run shows a series with only orders before May ending at 2025-03. So reindex to an explicit `date_range` when the report must have a fixed set of months.
- Division by zero: SQLite returns NULL for `100.0 * 120 / 0` (the run printed None), so the guard is not needed for SQLite, but keep `NULLIF` anyway: PostgreSQL raises a division-by-zero error for this (not executed here). pandas float division gives `inf` (the run printed inf), so mask the zero with `where`.
- Boundary dates: 2025-01-31 and 2025-03-01 land in January and March because the month key is `substr(date, 1, 7)`; a timestamp column with a time part would still work for the text key but not for a `BETWEEN` on dates.
- Rounding: growth is rounded to one decimal here; SQLite `ROUND` and pandas `round` can differ on exact halves (Part 10), none occurs in this data.""",
explain="""- Spine first, then join: the spine owns the months, the orders table only contributes numbers. This is the Part 6 Q6 pattern and the Part 5 Q16 `LAG` growth.
- `LAG` after the aggregation, never over raw orders: it must see one row per month.
- In an interview say the growth definition out loud: (this - previous) / previous, NULL when previous is 0.
- Scoring note (Set F3, Q3 of 5, 20 pts, part-header rubric): about 8 pts for a query that returns April as 0 and the right growth on the seed; 4 pts for May NULL and January NULL (and not 0 or an error); 4 pts for the pandas version matching (resample or reindex); 2 pts for stating the growth formula and that April is a real zero; 2 pts for a one-line check such as 5 rows and revenue total 670. Partial credit: a query without a spine that gets Jan, Feb, Mar, May right but drops April earns the correctness points only up to about half.""",
follow="""- Year-over-year? Same spine but `LAG(revenue, 12)` over a 12-month-plus spine (Part 6 Q6); with a gap-free spine the offset is exact. Not executed on other engines: PostgreSQL could build the spine with `generate_series` and `date_trunc` (not executed here).
- Why not `LAG` over a table with a missing month? Because `LAG` goes by row position, not by calendar, so May would compare with March.
- What if the first month should show 0 growth instead of NULL? Say that is a business choice; NULL means not defined.""",
mist="""- Joining orders to the spine with the filter in `WHERE`, which turns the LEFT JOIN back into an inner join and drops April.
- Using `COALESCE(growth, 0)` and hiding the undefined growth.
- Computing growth with integer division in engines that truncate (the `100.0` multiplier avoids it).
- Relying on `resample` to cover a range it does not know about.""")

q(22,
say="Aggregate units per category, month and product, then `RANK()` descending inside each (category, month) and keep rank 1; `RANK` (not `ROW_NUMBER`) keeps every tied product.",
example="""Jan books: product 1 sold 3 + 1 = 4, product 2 sold 2 + 2 = 4, so both rank 1 (tie). Jan toys: product 4 sold 1, product 5 sold 4, so product 5 wins. Feb books: only product 3 with 5. Feb toys: product 4 sold 2 + 0 = 2, product 5 sold 2, product 6 sold 1, so products 4 and 5 tie at 2. The March order (product 1, 9 units) is outside the date filter. That gives 6 rows: 2 for books Jan, 1 for books Feb, 1 for toys Jan, 2 for toys Feb.""",
edge="""- Ties: the run returns 6 rows with `RANK`, only 4 with `ROW_NUMBER` (one of each tied pair would be dropped, and which one is not defined without a tiebreaker).
- Date filter: `>= '2025-01-01' AND < '2025-03-01'` is a half-open range, so no end-of-month day is lost and March data (9 units of product 1) is excluded.
- Zero quantity rows (product 4 has a 0 line) add 0 and do not change the sum.
- A category with no sales in a month has no row at all (nothing to rank); add a spine if the report needs an empty line.
- pandas `rank(method="min", ascending=False)` matches `RANK`; `"dense"` would match `DENSE_RANK` and only differs beyond rank 1.""",
explain="""- Two steps: sum first (per product), rank second (per category and month); you cannot rank and sum in one pass without a window over an aggregate.
- The window is `PARTITION BY category, month ORDER BY units DESC`. Part 4 Q15 is the same shape.
- In engines with `QUALIFY` (Snowflake, BigQuery, not executed here) the rank filter can go in the same SELECT; in SQLite it needs the CTE.
- Scoring note (Set F3, Q2 of 5, 20 pts): about 8 pts for the right 6 rows; 4 pts for keeping both tied products (using `RANK`, not `ROW_NUMBER`) and excluding March; 4 pts for the pandas groupby and `rank(method="min")` matching; 2 pts for saying what ties mean for the business; 2 pts for a count check. Partial credit: `ROW_NUMBER` or `LIMIT 1` per group gets the structure right but loses the tie points.""",
follow="""- Top 2 products per category? `rnk <= 2` with `RANK` can return more than 2 rows on ties; with `DENSE_RANK` the ranks are consecutive (Part 4 Q4).
- Why not `MAX(units)` per group joined back? It also works and keeps ties; the window is shorter and extends to top N.
- A deterministic single winner? Add a tiebreaker such as `product_id` to the `ORDER BY` and use `ROW_NUMBER`.""",
mist="""- `ROW_NUMBER` silently drops one of two tied best sellers.
- Ranking raw order lines instead of per-product totals.
- Filtering the month in a way that includes 2025-03-01 or misses 2025-02-28 timestamps.
- In pandas, `rank()` default is `average`, which gives 1.5 for a tie and then `== 1` finds nothing.""")

q(23,
say="Compute the running balance with `SUM(...) OVER (PARTITION BY user ORDER BY txn_ts, txn_id ROWS ...)` and a `ROW_NUMBER()` in descending order of the same key, then keep row number 1; the `txn_id` in the order is the tiebreaker.",
example="""User 1: txn 1 adds 1000, txn 2 takes 300 and txn 3 takes 200 at the same second (10:00:00). Sorted by (timestamp, txn_id) the balances are 1000, 700, 500, so the latest row is txn 3 with 500. User 2: 500 then 250 gives 750 on txn 5. User 3 has one row, txn 6 with -40, so a negative balance is allowed. The result is one row per user: (1, 3, 500), (2, 5, 750), (3, 6, -40).""",
edge="""- Tie on timestamp: which row is "last" depends on the tiebreaker. With `txn_id` ascending as the posting order, txn 3 is last for user 1; if you broke the tie the other way txn 2 would be last. The final balance (500) is the same either way, the reported `last_txn_id` is not.
- Default frame trap: with `ORDER BY txn_ts` only, the default frame is `RANGE` and tied rows share one balance; the run shows user 1 as (1, 1000), (2, 500), (3, 500), so txn 2 appears to leave 500, not 700.
- A user with a single transaction works (rank 1 is that row). A user with no transactions has no row at all; join from a users table if you need them.
- Timestamps are text in ISO format, which sorts correctly as text.""",
explain="""- Two windows with the same partition and the same ordering key, one ascending (running sum) and one descending (pick the last). Part 4 Q9 gives the latest row, Part 5 Q12 the running balance.
- The sum must be computed over all rows before filtering to the last row, so both live in a CTE and the filter is outside.
- pandas: sort, `groupby.cumsum`, then `groupby.tail(1)`; sort first or `cumsum` runs in file order.
- Scoring note (Set T1, Q3 of 5, 20 pts): about 8 pts for three correct rows with balances; 4 pts for a deterministic tiebreak (txn_id) and naming the tie; 4 pts for pandas `cumsum` plus `tail(1)` matching; 2 pts for stating the tie rule; 2 pts for checking that the last balance equals the sum of all amounts per user. Partial credit: a correct latest row without the balance, or a balance from a tie-unsafe frame.""",
follow="""- Balance before the last transaction? Use `LAG(balance_after)` or subtract the amount.
- Why `ROWS` rather than `RANGE`? `RANGE` treats equal timestamps as one group; `ROWS` counts physical rows in the given order.
- Why not `MAX(txn_ts)` joined back? It returns both tied rows for user 1 and still has no balance.""",
mist="""- Filtering to the last row first and then summing (the balance becomes just that one amount).
- Ordering by timestamp only and trusting the engine's order for ties.
- In pandas, calling `cumsum` before sorting, or `groupby.last()` which skips NaN per column instead of returning a whole row.""")

q(24,
say="Partition by (user, merchant, amount), order by time, use `LAG` to get the previous matching payment and flag the row when the gap is 300 seconds or less; a self join over all earlier matches is the alternative but returns a pair for every earlier payment in the window.",
example="""User 1 pays merchant m1 an amount of 500 at 10:00:00 (payment 1), 10:02:00 (payment 2), 10:04:30 (payment 3) and 10:10:30 (payment 4). Payment 2 is 120 seconds after 1, so it duplicates 1. Payment 3 is 150 seconds after 2, so it duplicates 2. Payment 4 is 360 seconds (6 minutes) after 3, so it is not flagged. Payment 5 is another user, payment 6 another merchant and payment 7 another amount, so none of them join any chain. Result: (2 duplicates 1) and (3 duplicates 2).""",
edge="""- Triple duplicate: `LAG` links each payment to the previous matching one, so the triple gives 2 rows. A self join on every earlier match gives 3 pairs, (2,1), (3,1) and (3,2), because payment 3 is also within 5 minutes of payment 1 (270 seconds). Decide which one the business wants: one row per suspected duplicate payment (LAG) or every pair.
- Boundary: the rule is `<= 300` seconds, so a gap of exactly 5:00 is flagged; say so, since "within 5 minutes" is ambiguous. The 6:00 case (360 seconds) is not flagged.
- Chains: with `LAG` a stream of payments each 4 minutes apart is flagged all the way down, even though the first and last are far apart; that is usually what a fraud team wants, but say it.
- Same timestamp: `payment_id` breaks the tie so the earlier id is "earlier".
- Time arithmetic on text uses `strftime('%s', ts)` cast to integer seconds; on timestamp columns PostgreSQL would subtract directly (not executed here).""",
explain="""- Adjacent events in a group is a `LAG` problem (Part 7 Q26); the partition holds the equality conditions, the `ORDER BY` holds time.
- The 5-minute test is a difference in seconds so it has no calendar rounding.
- pandas: sort, `groupby(...).shift(1)` for the previous id and time, subtract timestamps.
- Scoring note (Set T1, Q2 of 5, 20 pts): about 8 pts for the two correct (later, earlier) pairs; 4 pts for rejecting the 6-minute payment and the different user, merchant and amount rows; 4 pts for pandas `shift` matching; 2 pts for stating inclusive or exclusive and LAG versus all-pairs; 2 pts for a count check (2 flagged of 7). Partial credit: a self join without the earlier-than condition returns each pair twice or pairs a row with itself.""",
follow="""- Count of duplicates per user? Group the flagged rows by user.
- Why not a `RANGE` window of 5 minutes? SQLite cannot do `RANGE` with an interval over text timestamps (Part 5 and the set note); PostgreSQL 11 and later accepts `RANGE BETWEEN INTERVAL '5 minutes' PRECEDING AND CURRENT ROW` on a timestamp column (not executed here).
- Make it idempotent for retries? That is a data-quality design point: a unique idempotency key beats detecting duplicates after the fact.""",
mist="""- Self join without `b.paid_at > a.paid_at` (each pair twice, plus a row paired with itself).
- Comparing text timestamps with `<` and forgetting the difference is not a number of minutes.
- Missing the amount (or merchant) in the partition.
- In pandas, shifting without sorting first, or shifting across groups instead of inside them.""")

q(25,
say="Compute days past due as the as-of date minus the due date for unpaid loans and map it with a CASE whose edges are 0, 30 and 60; paid loans are PAID_ON_TIME when `paid_date <= due_date`, else PAID_LATE.",
example="""As of 2025-06-30: loan 1 is due today (0 days) so CURRENT, loan 2 is due 2025-07-15 (-15) so CURRENT. Loan 3 is due 06-29 (1 day) so DPD_1_30, loan 4 due 05-31 is exactly 30 days so still DPD_1_30, loan 5 due 05-30 is 31 days so DPD_31_60, loan 6 due 05-01 is exactly 60 so DPD_31_60, loan 7 due 04-30 is 61 so DPD_61_PLUS. Loan 8 was paid on its due date so PAID_ON_TIME, loan 9 was paid a day later so PAID_LATE. Bucket counts: CURRENT 2, DPD_1_30 2, DPD_31_60 2, DPD_61_PLUS 1, one PAID_LATE, one PAID_ON_TIME.""",
edge="""- Boundary rule written down: 0 days is CURRENT (due today is not late yet), 1 to 30 inclusive is DPD_1_30, 31 to 60 inclusive is DPD_31_60, 61 and above is DPD_61_PLUS. The run puts day 30 in the first bucket and day 31 in the next, day 60 in DPD_31_60 and day 61 in DPD_61_PLUS.
- `pd.cut` is right-closed by default, so bins `(-inf, 0], (0, 30], (30, 60], (60, inf)` reproduce those edges; `right=False` would move every boundary day into the next bucket.
- Paid loans have no days-past-due value (NULL in SQL, NaN in pandas); the unpaid-only `dpd` column avoids mixing the two meanings.
- A future due date gives a negative number (-15), which is CURRENT.
- Not in the seed: a loan paid after the as-of date would need `paid_date > as_of` treated as unpaid at that date; say so rather than silently labelling it paid.
- `julianday` differences are whole numbers for date-only text; with times they would be fractions and `CAST` truncates.""",
explain="""- Order the CASE branches so the paid cases come first; a paid loan must never reach the days-past-due branches.
- The as-of date is a parameter, not `date('now')`, so results are reproducible. The SQL binds it by name (`:as_of`).
- Part 6 Q3 is the date difference, Part 1 Q10 the CASE bucketing.
- Scoring note (Set T2, Q3 of 5, 20 pts): about 8 pts for all 9 buckets right; 4 pts for the boundary days (30, 31, 60, 61) landing correctly and paid loans handled before the DPD branches; 4 pts for pandas `pd.cut` (or `np.select`) matching; 2 pts for stating the boundary rule first; 2 pts for a count check (9 loans, bucket counts add to 9). Partial credit: correct buckets for unpaid loans only.""",
follow="""- Weighted exposure per bucket? Sum the outstanding amount per bucket (Part 2 Q5 style).
- Why a parameter instead of today's date? Reproducible reports and tests.
- Month-end snapshots for every month? Cross join the loans with a spine of as-of dates, not executed here.""",
mist="""- Using `<` where the rule says `<=` and moving day 30 into the next bucket.
- Treating due-today as late.
- `pd.cut` with default `right=True` misread as left-closed.
- Letting paid loans fall into the DPD branches because the NULL check came last.""")

q(26,
say="Use `SUM(amount) OVER (PARTITION BY account ORDER BY txn_ts, txn_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`; ordering by the timestamp alone uses the default `RANGE` frame, which gives tied rows the same balance.",
example="""Account 1: +10000 at 09:00, then -2500 (txn 2) and -4000 (txn 3) both at 10:00:00, then +700 the next day. Deterministic order by (txn_ts, txn_id): 10000, 7500, 3500, 4200. With `ORDER BY txn_ts` only (default `RANGE` frame) rows 2 and 3 are peers, so both show 3500, the balance after the whole tie group; the intermediate 7500 never appears. Account 2: 3000 then -500 gives 3000, 2500 (no tie).""",
edge="""- Tie rule chosen: the ledger sequence `txn_id` ascending, because ids are assigned in posting order. If the tie were broken by `txn_id` DESC the run gives 10000, 3500, 6000, 4200 for account 1 (txn 3 first), so the intermediate balance changes while the end balance (4200) does not.
- A negative intermediate balance can appear or vanish depending on the tie order, which is why overdraft checks must use a defined order.
- RANGE-framed or ORDER BY txn_ts-only: peers share one value (shown in the last column). `ROWS` with only the timestamp in the order is a different trap: the order inside the tie is not defined, so I did not rely on it (not shown).
- Amounts are integer paise, so the sums are exact; floats would drift.
- pandas has no frame default: `cumsum` is always row by row after your sort, so it matches the `ROWS` column; the `RANGE` column needs `transform("last")` over the tied group.""",
explain="""- Same idea as Part 5 Q6: a running total needs a total order of rows, and timestamps alone are not one.
- `ROWS` counts physical rows; `RANGE` groups rows with equal ORDER BY values (peers). The standard's default frame when an ORDER BY is present is `RANGE UNBOUNDED PRECEDING` to `CURRENT ROW`, and PostgreSQL behaves the same (not executed here); SQLite showed it in the run.
- State the tie rule as a business rule, not a coincidence of `rowid` order.
- Scoring note (Set T2, Q2 of 5, 20 pts): about 8 pts for the correct deterministic running balance on all 6 rows; 4 pts for showing and explaining what the tie does under the default frame; 4 pts for pandas `cumsum` after a full sort matching (and, for a strong answer, the `transform("last")` for the peer behaviour); 2 pts for naming the tie rule; 2 pts for a check that the last balance per account equals the account total. Partial credit: a correct running sum that orders by timestamp only (right on the seed by luck, undefined on ties).""",
follow="""- Why does the default frame use RANGE? The standard says so; it is meant to treat equal sort keys as one position, which is surprising for ledgers.
- First moment the balance goes below zero? Filter the running balance (Part 5 Q22).
- What if two engines break ties differently? Then the results differ; only a total order (timestamp, id) is portable.""",
mist="""- `ORDER BY txn_ts` only, then reporting the same balance for two different transactions.
- Using floats for money.
- In pandas, sorting by timestamp only with an unstable sort and expecting a stable tie order (use a total key).
- Believing `ROWS` fixes ties by itself; it does not define the order inside the tie.""")

q(27,
say="Find each customer's first top-up month, count distinct active customers per (cohort, month offset) from a 0 to 2 offsets list, return 0 where nobody was active, and return NULL where the offset month is not finished by the as-of date.",
example="""January cohort: customers 1 to 5 (5 people). Active in January (offset 0): all 5. Active in February (offset 1): customers 1 and 4, so 2. Active in March (offset 2): customers 1 and 2, so 2. February cohort: customers 6, 7, 8 (3 people), offset 0 = 3, offset 1 (March) = customer 6 only = 1, offset 2 (April) = customers 6 and 7 = 2. As of 2025-04-30 that is 6 rows with no NULLs. The first run therefore shows the retention table; the second run (as of 2025-03-31) turns February offset 2 into NULL because April is not over; the third run deletes customers 1 and 4 to show a true zero (January offset 1 becomes 0).""",
edge="""- Premise check: the question asks for NULL for cohorts too young as of 2025-04-30, but with only January and February cohorts and offsets 0 to 2, every offset month (the latest is April, which ends on 04-30) is already finished, so no NULL appears. I show the NULL rule with an earlier as-of date (2025-03-31) where February offset 2 is NULL. With a March cohort in the data, March offset 2 (May) would be NULL on 2025-04-30.
- Zero versus NULL: zero means observed and nobody came back (third run: January offset 1 is 0); NULL means not observable yet. Mixing them makes young cohorts look like churn.
- Observable rule used: the offset month is complete when its last day is on or before the as-of date, written `date(cohort || '-01', '+k months', '-1 day') <= :as_of` (so a mid-month as-of date makes that month NULL).
- Duplicates: a customer topping up three times in a month counts once (`DISTINCT` over customer and month); customer 3 has two January rows.
- Data after the as-of date is ignored (customer 6's April top-up is excluded in the March run).
- pandas returns `None` for the unobservable cells; the comparison uses the nullable Float64 type so NaN equals NULL.""",
explain="""- Three small tables: first month per customer (cohort), distinct customer-months (activity), and the offsets list (0, 1, 2). The result is cohort times offset, not only the offsets that happen to have data.
- Month offset is calendar months between first top-up month and activity month (Part 6 Q10); in pandas a `Period` subtraction gives it.
- The `VALUES` common table expression for offsets is standard in SQLite (`WITH offs(month_offset) AS (VALUES (0), (1), (2))`).
- Scoring note (Set T3, Q3 of 5, 20 pts): about 8 pts for the correct counts (5, 2, 2 and 3, 1, 2); 4 pts for the zero versus NULL distinction and the observable-month rule; 4 pts for the pandas version matching on all scenarios; 2 pts for saying what a month offset means and that active means at least one top-up; 2 pts for a check (offset 0 equals cohort size). Partial credit: counts without NULL handling, or offsets that exist only where there is data.""",
follow="""- Retention percent? Divide by the offset 0 count; keep NULL for unobserved cells (Part 6 Q11).
- Month offset when the cohort is defined by signup, not first top-up? Same shape, different source of the cohort month.
- Why not `DATEDIFF` in months? SQLite has none; Postgres `age` or `DATE_DIFF` variants exist (not executed here).""",
mist="""- Returning no row for an offset nobody reached, which hides a zero.
- Treating a young cohort's missing future as 0 retention.
- Counting rows instead of distinct customers.
- Off-by-one on the offset (month 1 is the month after the first top-up, not the same month).""")

q(28,
say="Pre-aggregate the chargebacks to one row per payment before joining, then count payments with `COUNT(*)` and payments with a chargeback with `COUNT(cb.payment_id)`; joining the raw chargebacks repeats the payment and inflates its counts.",
example="""Payment 1 has two chargebacks (600 and 400). Naive join payment-to-chargeback: travel shows 5 payments instead of 4 because payment 1 appears twice. Pre-aggregated: travel has payments 1 to 4 (merchants 1 and 2), payments 1 and 3 have chargebacks, so 2 of 4 = 0.5 and the chargeback amount is 1000 + 500 = 1500. Grocery has payments 5 to 8, only payment 5 has a chargeback (300), so 1 of 4 = 0.25. Gaming has payment 9 with none: 0 of 1 = 0.00 and an amount of 0 (not NULL).""",
edge="""- Fan-out: the naive query reports 5 travel payments (the run) and the pandas naive merge gives 10 rows for 9 payments. The chargeback sum itself (1500) survives in this seed because each chargeback row is counted once, but any payment-side measure would be double counted.
- Categories with no chargeback: NULL in the naive output (gaming), 0 after `COALESCE` in SQL; in pandas `sum` of an all-NaN group is 0.0, so the column is float (0.0 versus integer 0 in SQL, compared with `check_dtype=False`).
- A payment with two chargebacks counts once in `payments_with_cb`; if the business wants chargeback events, count chargeback rows instead and say so.
- A merchant with no payments would not appear (join from payments); start from merchants if empty categories must show.""",
explain="""- This is Part 8 Q10: aggregate the many side to the grain of the one side before the join, so the join is one-to-one.
- `COUNT(cb.payment_id)` counts non-NULL, so payments without chargebacks are not counted.
- pandas: `groupby("payment_id").sum()` then a left merge, then named aggregation (`count` skips NaN, `size` does not).
- Scoring note (Set T3, Q2 of 5, 20 pts): about 8 pts for the correct pre-aggregated table (4, 2, 0.5, 1500 for travel); 4 pts for demonstrating the naive count (5) and explaining the fan-out; 4 pts for pandas matching; 2 pts for stating payments versus chargeback events as the unit; 2 pts for a check that the payment counts add up to 9. Partial credit: `COUNT(DISTINCT payment_id)` on the naive join gets the counts right but still double counts any payment amount.""",
follow="""- Chargeback amount as a percent of payment volume? Sum payment amounts on the payment side first, then divide; never `SUM(p.amount)` after the fan-out join.
- `COUNT(DISTINCT)` fix? Works for counts, not for sums; pre-aggregation fixes both.
- Time lag between payment and chargeback? Bucket by months since payment, a cohort-style cut (Part 6).""",
mist="""- `COUNT(*)` after a one-to-many join.
- `SUM(payment.amount)` after the join, which counts payment 1's amount twice.
- Inner joining chargebacks and losing categories with no chargebacks.
- Reporting NULL instead of 0 for the chargeback amount.""")

q(29,
say="Drop CANCELLED orders first, number each customer's remaining orders by date, take the first and second dates per customer, and divide customers with a second order by customers with at least one non-cancelled order; the average gap uses only those repeaters.",
example="""After dropping cancelled orders: customer 1 has 01-01 and 01-31 (30 days), customer 2 has two orders on 01-05 (0 days), customer 3 loses the cancelled 01-01 order and has 01-10 and 01-20 (10 days), customers 4 and 5 have one order each, customer 6 keeps only 03-01 (the second order was cancelled), customer 7 has 01-15, 02-14, 03-16 (first to second 30 days), customer 8 had only a cancelled order so disappears. That leaves 7 customers, 4 repeaters (1, 2, 3, 7), share 4/7 = 0.5714 and average (30 + 0 + 10 + 30) / 4 = 17.5 days.""",
edge="""- Denominator: customers with at least one non-cancelled order (7). Using all customers in the table (8, including the cancelled-only customer 8) gives 0.5, as the run prints. Say which one, since both are defensible.
- First order cancelled: customer 3 is a repeater measured from the first surviving order, not from the cancelled one.
- Same-day second order: customer 2 gives 0 days and still counts as a repeater; `order_id` breaks the tie between the two same-day orders.
- AVG over days ignores NULL (non-repeaters) in SQL and NaN in pandas; do not fill them with 0.
- A customer with orders on two dates but one cancelled is a single-order customer (customer 6).""",
explain="""- Part 6 Q20 and Part 8 Q21 are the model: first and second order per customer through `ROW_NUMBER` and conditional `MAX`.
- Filter before numbering; otherwise a cancelled order takes position 1 or 2.
- pandas: filter, sort, `groupby.cumcount()`, pick positions 1 and 2, subtract dates.
- Scoring note (Set E1, Q3 of 5, 20 pts): about 8 pts for 7 customers, 4 repeaters, 0.5714 and 17.5; 4 pts for the cancelled-first and same-day cases handled and the denominator named; 4 pts for pandas matching; 2 pts for stating the denominator out loud; 2 pts for a check (repeaters at most customers). Partial credit: right repeat share but days measured from the cancelled order.""",
follow="""- Repeat within 30 days only? Add `days <= 30` to the numerator; the denominator question gets sharper because young customers cannot have repeated yet (Part 6).
- Median days instead of average? SQLite has no median function; use a `ROW_NUMBER` or percentile in pandas (not run here).
- Repeat rate by acquisition month? Group the same table by the first-order month.""",
mist="""- Counting cancelled orders toward the order count.
- Dividing by all customers when the cancelled-only customer never really bought.
- Counting two same-day orders as one visit without saying so.
- Averaging days over non-repeaters as 0.""")

q(30,
say="Group by month with conditional aggregation: GMV is the sum over all orders, net revenue the sum over DELIVERED only, AOV is net revenue divided by delivered orders, and the cancelled share is cancelled orders divided by all orders.",
example="""January: 5 orders, 100 + 200 + 150 + 120 + 300 = 870 GMV. Delivered amounts are 100, 200, 300 so net revenue 600 over 3 delivered orders, AOV 200.00. One of 5 orders was cancelled: 0.2. February: 5 orders and 250 + 80 + 90 + 100 + 60 = 580 GMV, delivered 250 and 100 give net 350 over 2 orders, AOV 175.00, 2 of 5 cancelled = 0.4. The RETURNED orders are inside GMV but outside net revenue.""",
edge="""- Denominators differ by metric: GMV and the cancelled share use all orders (5 each month), AOV uses delivered orders (3 and 2). Dividing net revenue by all orders gives 120.00 and 70.00 instead, which is the common mistake (the run prints it).
- A month with no delivered orders: `NULLIF(..., 0)` makes AOV NULL (pandas masks the zero to NaN); it would be a 0 divided by 0 otherwise. Not in the seed.
- GMV definition varies by company (some exclude cancelled orders); here it is all orders as the question states, and RETURNED is kept in it.
- `SUM(CASE ... END)` with no ELSE is NULL when no row matches; I used `ELSE 0` for net revenue so it prints 0.
- Rounding: AOV is rounded to 2 decimals and the share to 4; the seed values are exact, so SQLite and pandas rounding agree.""",
explain="""- One scan with conditional aggregation (Part 8 Q4): `SUM(CASE WHEN status = ... THEN amount END)` and `COUNT(CASE WHEN ... THEN 1 END)`. PostgreSQL, SQLite 3.30 and later and others also have `FILTER (WHERE ...)` (I did not use it here; not executed).
- pandas named aggregation cannot take a condition, so add helper columns (`delivered`, `cancelled`, `net_amount`) first; booleans sum to counts.
- Say the denominator for each metric before coding, then the definitions are visible to the interviewer.
- Scoring note (Set E1, Q2 of 5, 20 pts): about 8 pts for the 2 correct rows (870, 600, 200.00, 0.2 and 580, 350, 175.00, 0.4); 4 pts for the right denominators and the NULL guard on AOV; 4 pts for pandas named aggregation matching; 2 pts for stating the GMV and net definitions; 2 pts for a check that GMV equals the sum of all amounts (1450). Partial credit: one scan with the right numerators but a single denominator for all metrics.""",
follow="""- AOV on all orders, or per customer? Different metrics; ask which the team uses.
- Return rate? RETURNED count over DELIVERED plus RETURNED, a definition to state first (Part 8).
- Month-over-month change in these metrics? Add a `LAG` over the monthly table as in Q21.""",
mist="""- Using `COUNT(*)` as the AOV denominator.
- Putting the status filter in `WHERE`, which also changes GMV and the cancelled share.
- Integer division for the share (the `1.0 *` avoids it).
- Silently excluding returned orders from GMV without saying so.""")

out = ["<!-- Book 3 Part 12 answers Q21-Q30 (Wave B). Generated; code blocks were run with python3 -I. -->\n"]
for n in range(21, 31):
    src = open(f"code/q{n}.py", encoding="utf-8").read()
    r = subprocess.run(["python3", "-I", f"code/q{n}.py"], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
    assert r.returncode == 0, (n, r.stderr)
    h, asked = head(n)
    d = P[n]
    ddl = var(src, "DDL")
    sqls = []
    if "SQL_NAIVE" in src:
        sqls.append(("Naive version (shows the fan-out):", var(src, "SQL_NAIVE")))
    sqls.append(("", var(src, "SQL")))
    sql_txt = ""
    for lab, s in sqls:
        sql_txt += (lab + "\n" if lab else "") + "```sql\n" + s + "\n```\n"
    if n == 24:
        sql_txt += "The all-pairs alternative is `SQL_ALL_PAIRS` in the Code block (a self join on the same keys with an earlier-than condition).\n"
    pd_txt = pandas_block(src)
    out.append(h + "\n" + asked)
    out.append(f"**Say this first (1 line):** {d['say']}\n")
    out.append("**Schema and sample data:**\n```sql\n" + ddl + "\n```\n")
    out.append("**SQL answer:** the `SQL` string in the Code block, shown here verbatim.\n" + sql_txt)
    out.append("**pandas answer:** the block between the PANDAS START and PANDAS END comments of the Code block, shown here verbatim.\n```py\n" + pd_txt + "\n```\n")
    out.append("**Example:** " + d["example"] + "\n")
    out.append("**Code:** run with `python3 -I`; the SQL and pandas results are asserted equal with `assert_frame_equal` (row order stated in the assert message).\n```python\n" + src.rstrip("\n") + "\n```\n")
    out.append("**Output (my run):**\n```text\n" + r.stdout.rstrip("\n") + "\n```\n")
    out.append("**Edge cases:**\n" + d["edge"] + "\n")
    out.append("**Then explain:**\n" + d["explain"] + "\n")
    out.append("**Follow-ups:**\n" + d["follow"] + "\n")
    out.append("**Common mistakes:**\n" + d["mist"] + "\n")
open("answers.md", "w", encoding="utf-8").write("\n".join(out))
print("written", len("\n".join(out)))
