FENCE = "`" * 3

def mk(say, sql_intro, sqls, pd_intro, pd_range, example, edge, explain, follow, mistakes, schema_label="**Schema and sample data:**", schema_fn=None):
    subs = {}
    sch = schema_fn or schema
    subs["SCHEMA"] = lambda c: sch(c)
    sql_parts = []
    for i, nm in enumerate(sqls):
        subs["SQL%d" % i] = (lambda nm: (lambda c: sqlvar(c, nm)))(nm)
        sql_parts.append("`%s` in the Code block:\n%ssql\n<<SQL%d>>\n%s" % (nm, FENCE, i, FENCE))
    subs["PD"] = lambda c: between(c, pd_range[0], pd_range[1])
    body = "\n".join([
        "**Say this first (1 line):** " + say, "",
        schema_label, FENCE + "sql", "<<SCHEMA>>", FENCE, "",
        "**SQL answer:** " + sql_intro, "\n".join(sql_parts), "",
        "**pandas answer:** " + pd_intro, FENCE + "py", "<<PD>>", FENCE, "",
        "**Example:** " + example, "",
        "**Code:** run with `python3 -I`. It builds the data, runs the SQL and the pandas version, asserts they are equal and prints everything.",
        FENCE + "python", "<<CODE>>", FENCE, "",
        "**Output (my run):**", FENCE + "text", "<<OUTPUT>>", FENCE, "",
        "**Edge cases:**", edge, "",
        "**Then explain:**", explain, "",
        "**Follow-ups:**", follow, "",
        "**Common mistakes:**", mistakes, ""])
    return dict(body=body, subs=subs)

# ---------------------------------------------------------------- Q1
Q[1] = mk(
 say="Make the friendship list symmetric with UNION ALL, self join it on the shared friend with `a < b` so each pair shows up once, drop pairs that are already friends with NOT EXISTS, and keep `HAVING COUNT(*) >= 2`.",
 sql_intro="the query is `sql` in the Code block (`naive` and `one` are the wrong and the excluded-pairs variants).",
 sqls=["sql"],
 pd_intro="the same steps with `concat`, a self `merge` on the shared friend, an anti-join through a left merge and `groupby().size()`.",
 pd_range=("e = pd.concat", "# compare in the same order"),
 example="Friendships: 1-2, 1-3, 2-4, 3-4, 2-5, 3-5, 4-5, 4-6, 5-6, 6-7, 1-7; user 8 has none. Friends of 2 are {1, 4, 5} and friends of 3 are {1, 4, 5}; 2 and 3 are not friends, and they share 1, 4 and 5, so (2, 3) has 3 mutual friends and tops the list. Friends of 1 are {2, 3, 7} and of 4 are {2, 3, 5, 6}: they share 2 and 3, so (1, 4) has 2. The same hand count gives (1, 5), (2, 6) and (3, 6) with 2 each. (1, 6) shares only 7, so it has exactly one mutual friend and is dropped by the HAVING. (4, 5) shares 2, 3 and 6 but they are already friends, so the NOT EXISTS removes them. Result: 5 rows, as in the output.",
 edge="""- **Each pair once:** the join condition `e1.p < e2.p` keeps (2, 3) and drops (3, 2), and it also drops the self pair (2, 2). With `<>` instead, my run returned 12 rows: the 5 real pairs twice plus the already-friends pair (4, 5) twice.
- **Already friends:** the friends table stores only `user_id < friend_id`, so the anti-join can test `(e1.p, e2.p)` directly because `e1.p < e2.p` has the same orientation. If a table stored both directions this check would still work, but the edge list would be doubled.
- **Duplicate friendship rows** would inflate the count (the same mutual friend counted twice). Use `UNION` instead of `UNION ALL` for the edge list, or `COUNT(DISTINCT e1.f)`.
- **User with no friends** (user 8) never appears in any join, so never in the output. A user with one friend can never be in a pair with 2 mutual friends.
- **Ties:** pairs with equal counts are ordered by a then b, so the output is deterministic.""",
 explain="""- **The symmetric list is the key idea.** One stored row (1, 4) means 1 is a friend of 4 and 4 is a friend of 1. `UNION ALL` of the table with its reverse gives (person, friend) rows in both directions, so one self join on `friend` finds everyone who shares that friend.
- **Why a < b stops duplicates:** the same two users meet on every shared friend, once as (a, b) and once as (b, a). Requiring the smaller id first keeps one of the two, and `GROUP BY a, b` then counts the shared friends.
- **Why the count is the mutual-friend count:** each shared friend produces exactly one joined row for the pair, so `COUNT(*)` after the join is the number of mutual friends (given no duplicate edges).
- **pandas:** `e.merge(e, on="f")` is the same self join; the anti-join is a left merge with a marker column, then keep rows where the marker is NaN.
- **Names:** `users` is only needed for display; the last lines of the Code block join it back (Bala and Chitra share 3 friends).
- **Other engines:** the same SQL works on PostgreSQL and MySQL 8 (not executed here, from memory). On a big graph the self join costs degree squared per user, which is the real scaling problem.
""" + scoring(25, "F1", "Q5 of 5", "symmetric edge list, `a < b`, anti-join, HAVING >= 2", "a query that returns every pair twice or includes existing friends loses most of the 10 query points but keeps edge-case and pandas credit if stated; getting only the symmetric list right is about half the query points"),
 follow="""- *Rank the suggestions per user, not per pair?* Make the pairs symmetric again (UNION ALL of (a, b) and (b, a)), then `ROW_NUMBER() OVER (PARTITION BY user ORDER BY mutual DESC, other)` and keep the top 3 (Part 4 style).
- *What if friendships are stored in both directions?* Then the UNION ALL is not needed (the table is already symmetric) but the `a < b` filter still is.
- *How would you make it faster?* An index on the friend column of the edge list, and skip users with very high degree or sample them; say it in one sentence, the plan itself is Part 11.""",
 mistakes="""- Joining on `e1.p <> e2.p` and returning each pair twice.
- Forgetting the already-friends filter, so (4, 5) is suggested to people who are already friends.
- Counting rows before the filter, or using `COUNT(DISTINCT ...)` on the wrong column.
- Using `NOT IN (SELECT ...)` against a column that may contain NULL (use NOT EXISTS).
- Not saying how the duplicate pair is avoided; the prompt asks for it.""")

# ---------------------------------------------------------------- Q2
Q[2] = mk(
 say="Sort each advertiser's ranges by start, compare each start with the running maximum of the earlier end dates (not the previous end), start a new island when the gap is more than one day, then merge by island and add up the days; I treat touching ranges (end 03-10, start 03-11) as one range because there is no uncovered day between them.",
 sql_intro="`merged_sql` and `days_sql` in the Code block (`naive_sql`, `strict_sql` and `lag_sql` are the comparison variants).",
 sqls=["merged_sql", "days_sql"],
 pd_intro="sort, `cummax().shift()` per advertiser, a flag, `cumsum` for the island id, then `groupby` with min and max.",
 pd_range=("fl = pd.read_sql(\"SELECT * FROM flights\"", "print(\"pandas merged ranges:\")"),
 example="Advertiser 1 has 11 (03-01 to 03-10), 12 (03-03 to 03-05, nested), 13 (03-08 to 03-15) and 14 (03-20 to 03-22). Sorted by start, the running max of earlier ends is NULL, 03-10, 03-10, 03-15. Campaign 11 starts an island (no earlier end); 12 starts 03-03, not after 03-11, so it joins; 13 starts 03-08, joins and pushes the end to 03-15; 14 starts 03-20, later than 03-16, so a new island. Merged ranges: 03-01 to 03-15 (15 days) and 03-20 to 03-22 (3 days), 18 live days; summing the campaign lengths would say 24. Advertiser 2: 21 ends 03-10 and 22 starts 03-11, no day between them, so one range 03-01 to 03-15 (15 days); 23 starts 03-17 and 03-16 is uncovered, so a second range of 2 days, total 17. Advertiser 3 is one range of 7 days.",
 edge="""- **Touching ranges:** my rule is `start > prev_max_end + 1 day` starts a new island, so touching merges. The overlap-only rule (`start > prev_max_end`) keeps 21 and 22 apart (3 ranges for advertiser 2 in my run). The live-day total is 17 either way, only the number of ranges changes, so say which one you chose.
- **Nested range:** campaign 12 lies inside 11. Because the comparison uses the running MAX of ends, it does not shorten the island. The wrong version with `LAG(end_date)` compares 13 with 12's end (03-05) and in my run produced two overlapping ranges for advertiser 1 (03-01 to 03-10 and 03-08 to 03-15).
- **Single range** (advertiser 3) works because the first row has no previous end (NULL), which is what starts the first island.
- **Ties on start_date:** ordering by `start_date, campaign_id` makes the order total, so the ROWS frame is deterministic.
- **Dates as text:** ISO `YYYY-MM-DD` text sorts and compares correctly, and `date(x, '+1 day')` stays text. NULL end dates (open campaigns) need a COALESCE to an as-of date before this runs; not seeded here.
- **Inclusive length:** days = end minus start plus 1, because both ends count.""",
 explain="""- **Why a running max and not LAG:** an island ends only after the latest end seen so far, and a nested campaign does not extend it. `MAX(end_date) OVER (... ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING)` is that latest end before the current row.
- **Why a cumulative flag:** the flag is 1 when a new island starts; `SUM(flag) OVER (ORDER BY ...)` turns it into an island id, the same trick as Part 7 Q16. Then ordinary `GROUP BY` takes `MIN(start)` and `MAX(end)`.
- **Distinct days:** once ranges are merged they cannot overlap, so summing their lengths counts each calendar day once. That is why you merge first instead of summing campaign lengths (24 versus 18 for advertiser 1).
- **pandas:** `groupby(...)["end_date"].cummax().shift()` is the running max of earlier ends; the island id is `groupby(...)["new_island"].cumsum()` (Part 7 Q28).
- **Other engines:** the same window SQL runs on PostgreSQL and others with their date arithmetic (`+ INTERVAL '1 day'`, not executed here).
""" + scoring(25, "F2", "Q5 of 5", "running-max island flag, merged ranges and live-day total", "using LAG of the previous end earns roughly half of the query points because nested ranges break; summing campaign lengths gets the day count wrong and loses the edge-case points; stating the touching rule is the 2.5 assumption points"),
 follow="""- *How do you count days per month?* Join the merged ranges to a day spine (recursive CTE) and count the days per month; or clip each range to the month and sum the lengths.
- *Open-ended campaigns (end NULL)?* `COALESCE(end_date, as_of_date)` before merging, and say it.
- *Is there a one-query alternative?* A day spine joined to flights with `EXISTS` counts distinct live days directly, but it is heavier for long ranges.""",
 mistakes="""- Comparing with the previous row's end instead of the running maximum.
- Summing `end - start + 1` over campaigns and double counting overlaps.
- Forgetting the `+ 1` for inclusive end dates.
- Not saying how touching ranges are treated.
- Starting the island flag for the first row incorrectly (NULL comparison is not true, so it must be tested with IS NULL).""")

# ---------------------------------------------------------------- Q3
Q[3] = mk(
 say="Build the (manager, any report below) pairs with a recursive CTE that starts from the direct edges and walks one level down each step, then count with `SUM(depth = 1)` for direct reports and `COUNT(*)` for all reports; the orphan row is listed by a separate NOT EXISTS query.",
 sql_intro="`sql` (roll-up) and `orphan_sql` in the Code block.",
 sqls=["sql", "orphan_sql"],
 pd_intro="an iterative walk: merge the current frame with the edge list on `emp` equal to `mgr`, collect each new level, stop when a merge returns nothing, then group.",
 pd_range=("emp = pd.read_sql(\"SELECT * FROM employees\"", "print(\"pandas roll-up:\")"),
 example="Rows: 1 CEO; 2 and 3 report to 1; 4, 5 report to 2; 6, 12 report to 3; 7, 8 report to 4; 9 reports to 5; 10, 11 report to 6; 13 has manager 99, which does not exist. Employee 1 has 2 direct reports and every other employee below, 11 (12 employees minus the CEO). Employee 2 has direct 4 and 5, and below them 7, 8 and 9, so 2 direct and 5 total. Employee 3 has direct 6 and 12, plus 10 and 11 below 6: 2 direct, 4 total. Employee 4 has 7 and 8 (2 and 2), 6 has 10 and 11 (2 and 2), 5 has just 9 (1 and 1). The leaves have no reports, so they are not managers and are not listed. Row 13 is printed by the orphan query.",
 edge="""- **Orphan:** the base query joins to `employees` on the manager id, so 13 (manager 99) is not walked and 99 never shows up as a phantom manager. If you skipped that join, 99 would appear as a manager with 1 report (by reasoning, not run). The orphan list uses NOT EXISTS; `NOT IN (SELECT emp_id ...)` also works here only because `emp_id` is a non-NULL key, so prefer NOT EXISTS.
- **CEO:** NULL `manager_id` is not an edge, so the CEO has no manager row and is never listed as someone's report.
- **Leaves:** they have 0 reports and are not returned. If the prompt wants every employee with 0, LEFT JOIN `employees` to the result and COALESCE.
- **Cycles:** a manager loop (A reports to B, B to A) makes `UNION ALL` recursion run forever in SQL; add a depth limit (`WHERE d.depth < 20`) or track the path. The pandas loop has the same risk, so the code asserts that the level never exceeds the row count.
- **An orphan's own reports** would still be rolled up under the orphan (it exists as a row), as a separate detached tree.
- **Output type:** `read_sql` gives integers here; in pandas the manager id first becomes a float because the column holds NULL, so the code casts it back before comparing.""",
 explain="""- **Recursive CTE shape:** an anchor (direct edges) plus a recursive step that joins the CTE to `employees` on `manager_id = d.emp`. The `mgr` column is carried unchanged, so every row says "this employee is somewhere below that manager".
- **Direct versus total:** `depth` starts at 1 in the anchor and grows by 1 per level, so `SUM(depth = 1)` counts direct reports and `COUNT(*)` counts everyone below. `SUM(CASE WHEN depth = 1 THEN 1 ELSE 0 END)` is the portable spelling of the same thing.
- **pandas walk:** the frame `cur` holds the pairs found at the latest level; merging it with the edges on `emp == mgr` yields the next level; concatenating all levels gives the same closure as the CTE. My run walked 3 levels of edges.
- **Order:** total reports descending then `emp_id`, as asked; both sides sort the same way before the assert.
- **Other engines:** PostgreSQL, MySQL 8 and SQL Server run recursive CTEs too (SQL Server without the RECURSIVE keyword); not executed here. Oracle also has CONNECT BY (hedged).
""" + scoring(25, "F3", "Q5 of 5", "closure CTE with direct and total counts", "counting only direct reports (a GROUP BY) earns about a quarter of the query points; a correct total but a phantom manager 99 loses the orphan edge-case points"),
 follow="""- *Employees per level?* `COUNT(*) GROUP BY depth` from the same CTE started at the CEO.
- *Path from an employee to the CEO?* Carry a text path in the recursive step (Part 9).
- *Many levels or millions of rows?* Say you would store a materialised path or closure table; the engine specifics are not executed here.""",
 mistakes="""- Counting only `COUNT(*) GROUP BY manager_id`, which is direct reports only.
- Starting the anchor from the CEO only, so subtrees are counted from one root instead of every manager.
- Letting a missing manager id appear as a manager row.
- No cycle guard.
- Using `UNION` and expecting depth to dedupe (different depths are different rows).""")

# ---------------------------------------------------------------- Q4
Q[4] = mk(
 say="Relational division: a customer qualifies when no featured product exists that they did not buy (double NOT EXISTS), or when the count of DISTINCT featured products they bought equals the number of featured products (GROUP BY and HAVING); both give customers 1 and 3 on the seed.",
 sql_intro="`not_exists` and `having` in the Code block (`wrong` shows the row-count trap).",
 sqls=["not_exists", "having"],
 pd_intro="`division()` in the Code block: merge to featured, drop duplicates, `nunique` per customer, compare with `len(featured)`.",
 pd_range=("# pandas\norders", "# empty featured list"),
 example="Featured products are 101, 102, 103. Customer 1 bought 101, 102 (order 1) and 102, 103 (order 2): all three, with 102 twice, so qualifies. Customer 2 has rows 101, 101, 102 and 101 again: 4 rows hit a featured product but only 2 distinct ones (103 is missing), so does not qualify. Customer 3 bought 101, 102, 103 and 999 in one order: qualifies. Customer 4 bought 555 only and customer 5 bought only 103. Answer: 1 and 3. A `COUNT(*) >= 3` check would wrongly pass customer 2 (4 rows) and the exact `= 3` check would wrongly fail customer 1 (4 rows), which is why DISTINCT matters.",
 edge="""- **Duplicates:** duplicate item rows and the same product in two orders must collapse, so count DISTINCT products (HAVING) or test existence (NOT EXISTS, naturally duplicate-proof).
- **Non-featured items** (999, 555) are ignored by the join to `featured`.
- **Customers with no featured purchase** (4) never appear in the HAVING version because the join removes them; the NOT EXISTS version enumerates candidates from `orders` and rejects them.
- **Empty featured list:** in my run NOT EXISTS returned all 5 customers (no featured product is missing, so everyone qualifies vacuously) while HAVING returned nobody (the join to an empty table leaves no groups). pandas split the same way: the merge and `nunique` version returned nobody and a set-subset test returned everybody. The business rule decides; I would say it out loud and probably return nobody ("bought every product on an empty list" is not a useful target), which means adding a guard `AND EXISTS (SELECT 1 FROM featured)` to the NOT EXISTS form.
- **Candidates:** both versions treat a customer as someone with at least one order. A customer without orders is not in the data, so they cannot be returned.""",
 explain="""- **Double NOT EXISTS reads as:** there is no featured product for which there is no purchase by this customer. It is the textbook division form and handles duplicates for free.
- **HAVING form:** join items to featured, group by customer, and compare `COUNT(DISTINCT f.product_id)` with `(SELECT COUNT(*) FROM featured)`. It is shorter and usually faster, but only correct with DISTINCT and fails differently on an empty list.
- **Which to pick:** HAVING when the list is a small stable table; NOT EXISTS when you must be vacuously correct or when the list is dynamic and you want the semantics to be obvious. Say both and the empty-list difference, which is what the prompt asks for.
- **pandas:** `drop_duplicates` before `nunique`, then compare with `len(featured)`; the set version `featured_set <= customer_set` is the NOT EXISTS reading.
- Part 3 Q14 and Q35 cover division in general; this question adds duplicates and the empty list.
""" + scoring(25, "F3", "Q4 of 5", "customers 1 and 3 by at least one of the two SQL forms", "the HAVING form without DISTINCT passes the wrong customers and loses most query points; giving only one of the two SQL forms loses a few; the empty-list explanation is where the 5 edge-case points sit"),
 follow="""- *Customers who bought at least two of the three?* Change HAVING to `>= 2`; NOT EXISTS no longer applies.
- *Within a time window?* Add the date filter in the join (or in the inner NOT EXISTS), not after the grouping.
- *What about a customer who returned a product?* Filter returns out before testing, and say what "bought" means.""",
 mistakes="""- `COUNT(*)` instead of `COUNT(DISTINCT product_id)` so duplicate rows pass or fail the wrong people.
- Comparing to a hard-coded 3 instead of `(SELECT COUNT(*) FROM featured)`.
- Putting the featured filter in WHERE after a LEFT JOIN, silently turning it into an inner join.
- Not thinking about the empty featured list.""")

# ---------------------------------------------------------------- Q5
Q[5] = mk(
 say="Keep only APPROVED rows, turn the timestamp text into integer seconds, and for each approved transaction count approved transactions of the same card between its time and its time plus 600 seconds, inclusive; flag cards where that count is 3 or more.",
 sql_intro="`windows_sql` in the Code block; `lag_sql` is the LAG offset 2 check and `range_sql` the RANGE frame over integer seconds.",
 sqls=["windows_sql", "lag_sql"],
 pd_intro="per card, `searchsorted` on the sorted times counts how many fall inside `[t, t + 600s]`; `shift(2)` gives the LAG(2) version.",
 pd_range=("# pandas: per card", "pd.testing.assert_frame_equal(w, p"),
 example="Card 1 approved at 10:00:00, 10:04:00, 10:10:00 and 10:10:30. From the 10:00:00 start the window ends 10:10:00 and contains 3 rows (10:10:00 is exactly 600 seconds later and counts), so a flag with count 3. From 10:04:00 the window ends 10:14:00 and holds 10:04, 10:10 and 10:10:30, another 3. From 10:10:00 only 2. Card 2 has 11:00:00, 11:05:00 and 11:10:01: the third is 601 seconds after the first, so no window reaches 3. Card 3 has two approved rows and a declined one in between; after removing the decline only 2 remain. Card 4 has 13:00, 13:01 and 13:02, so 3. Flagged cards: 1 (two overlapping windows, first start 10:00:00) and 4.",
 edge="""- **Boundary:** `BETWEEN x.s AND x.s + 600` is inclusive at both ends, so exactly 10:00 apart counts and 10:01 apart does not (card 2). Say the inclusive rule before coding.
- **Declined rows must be removed before windowing,** not just before counting, otherwise the decline would still sit between rows and LAG(2) would look at the wrong transactions (card 3).
- **Overlapping windows:** card 1 has two flagged start times. Return all of them, or take `MIN(window_start)` per card if the output must be one row per card (the LAG check does that).
- **Same-second duplicates:** two rows with the same timestamp are both counted from each other (the self join is not affected by ties); LAG(2) needs a deterministic tiebreak such as txn_id.
- **Text timestamps:** the prompt's note: SQLite RANGE frames need a numeric ORDER BY. In my run `RANGE BETWEEN CURRENT ROW AND '10 minutes' FOLLOWING` over the text column raised `OperationalError: frame ending offset must be a non-negative number`; converting to integer seconds with `strftime('%s', ...)` made the RANGE frame work and match the self join. PostgreSQL has `RANGE BETWEEN CURRENT ROW AND INTERVAL '10 minutes' FOLLOWING` on timestamp columns (not executed here, from memory).
- **Time zones:** the text has no zone; assume one zone (UTC) for all cards.""",
 explain="""- **Self join version:** it gives exactly the three things asked for: card, window start and count. It is O(rows per card squared), fine for a seeded test, and an index on (card, time) helps at scale (Part 11).
- **LAG with offset 2:** `LAG(s, 2)` is the time of the transaction two rows earlier on the same card; if `s - LAG(s, 2) <= 600`, then three approved transactions lie within 10 minutes. It flags the card cheaply and its window start is the lagged time, but it does not tell you a count above 3, which is why the self join is the main answer.
- **RANGE over seconds:** `COUNT(*) OVER (PARTITION BY card_id ORDER BY s RANGE BETWEEN CURRENT ROW AND 600 FOLLOWING)` ran and matched. It is concise but needs the numeric column.
- **pandas:** `searchsorted(..., side="right")` on the sorted times gives the index of the first row after the window, so the count is that index minus the row's own position. `rolling("10min")` on a time index is trailing (window ends at the row), so it answers the mirror question "window end" rather than "window start"; I did not use it here.
- The window definition and the inclusive rule are this book's assumptions, not a vendor rule.
""" + scoring(25, "T1", "Q5 of 5", "APPROVED filter, inclusive 10-minute window, windows and counts", "a version that ignores the status filter, or uses a strict `<` at 10:00, loses most query points; LAG(2) with the right filter and boundary and no count is about three quarters of the query points"),
 follow="""- *Flag the card once with the first window?* `MIN(window_start)` per card, as `lag_sql` does.
- *Rolling 24-hour limit on amount?* Same self join with `s + 86400` and `SUM(amount)`.
- *What about a streaming system?* A per-card sorted state of the last 2 timestamps is enough for the LAG(2) rule; not executed here.""",
 mistakes="""- Counting declined transactions.
- Using `<` for the end of the window and missing the exact 10:00 case.
- Comparing text timestamps with arithmetic, or ordering by a non-ISO text.
- LAG(1) instead of LAG(2) for "3 or more".
- Reporting overlapping windows as separate fraud events without saying so.""")

# ---------------------------------------------------------------- Q6
Q[6] = mk(
 say="Collapse the bank file to one row per txn_id first, then FULL OUTER JOIN it to the ledger and label each txn_id with a CASE in a fixed order: missing in bank, missing in ledger, duplicate in bank, amount mismatch, matched.",
 sql_intro="`full_sql` (FULL OUTER JOIN, runs on SQLite 3.45) and `emul_sql` (LEFT JOIN plus UNION ALL anti-join, for engines without FULL JOIN) in the Code block.",
 sqls=["full_sql", "emul_sql"],
 pd_intro="aggregate the bank file, outer merge with `indicator=True`, then `np.select` in the same order as the CASE.",
 pd_range=("# pandas\nledger", "pd.testing.assert_frame_equal(s, p"),
 example="Ledger T1 to T8; bank has T1, T2, T3, T4, T5 (twice, B5 and B6), T6, T8 and T9. T1, T3, T4, T6, T8 have the same amount on both sides: MATCHED. T2 is 25000 in the ledger and 24500 in the bank: AMOUNT_MISMATCH. T5 appears twice in the bank: DUPLICATE_IN_BANK. T7 has no bank row: MISSING_IN_BANK. T9 has no ledger row: MISSING_IN_LEDGER. Counts: 5 matched, one of each other status, 9 txn_ids from 8 ledger and 9 bank rows (8 ledger ids plus T9).",
 edge="""- **Duplicates:** without pre-aggregating, T5 joins to two bank rows and appears twice (my run listed T5 with 2 rows out), which would double the reconciled amount. Collapse to one row per txn_id first, then test the count.
- **Order of the CASE matters:** a duplicate whose amounts also differ would be labelled DUPLICATE_IN_BANK because that test comes before the amount test. State that precedence. If duplicate rows can carry different amounts, add `COUNT(DISTINCT amount_paise)` to the aggregate.
- **NULL amounts:** `5 <> NULL` is NULL, so the CASE falls through to ELSE and says MATCHED (my run printed MATCHED for `<>` and AMOUNT_MISMATCH for `IS NOT`). Use `IS NOT` in SQLite (or `IS DISTINCT FROM` where available) if NULL amounts are possible; seed data has none.
- **Integers:** amounts are integer paise, so the compare is exact. With float rupees you would need a tolerance. The printed 10000.0 values in the output are only pandas turning integer columns into floats because the outer join created NaN.
- **Dates:** txn_date versus settled_date are different by design (settlement lag); they are not part of the status here. Late-arriving rows would show as MISSING_IN_BANK until they land.""",
 explain="""- **FULL OUTER JOIN:** SQLite supports it from 3.39 (I ran it on 3.45.1). PostgreSQL supports it; MySQL does not and needs the UNION emulation (not executed here, from memory). `emul_sql` is the portable fallback and my run asserted it equals the real FULL JOIN (Part 2 Q16, Q32; compare Q44).
- **Dedupe before compare:** the bank side is aggregated to `n_bank` and an amount per txn_id, so the join is one to one and the status is per txn_id, one row each.
- **pandas:** `how="outer", indicator=True` gives `left_only`, `right_only` and `both`, which are exactly MISSING_IN_BANK, MISSING_IN_LEDGER and the rest. `np.select` evaluates conditions in order, like CASE.
- **Check:** count by status (my run printed 5 / 1 / 1 / 1 / 1) and make sure the total equals the number of distinct txn_ids on both sides, 9.
- Reconciliation, duplicates and idempotency are a common fintech theme, but this exact question is an expert design, not a verified company question.
""" + scoring(25, "T1", "Q4 of 5", "one status per txn_id with all five statuses", "a plain INNER or LEFT JOIN that cannot show MISSING_IN_LEDGER loses about half the query points; forgetting to dedupe so T5 appears twice loses the duplicate status and the check points"),
 follow="""- *Report the money gap?* Add the signed difference `ledger - bank` per status and total per status.
- *Match on txn_id and date?* Add the date to the join key and decide whether a one-day settlement lag is allowed.
- *Idempotent re-load?* A unique constraint on `(bank_ref)` or on `txn_id` plus a dedupe step; the DDL is not executed here.""",
 mistakes="""- Joining without pre-aggregating the duplicate bank rows.
- LEFT JOIN only, which can never show bank rows missing from the ledger.
- Comparing amounts with `<>` when NULLs are possible.
- Putting the amount test before the duplicate test without saying it.
- Using `WHERE b.txn_id IS NULL OR l.txn_id IS NULL` and calling it a reconciliation (that shows only the missing ones).""")

# ---------------------------------------------------------------- Q7
Q[7] = mk(
 say="For each payment take the latest fx row of the same currency with `valid_from <= paid_on` (correlated subquery with ORDER BY valid_from DESC LIMIT 1, or a LEAD-based range join) and multiply; no earlier rate leaves NULL, and pandas does the same with `merge_asof(by=currency, direction='backward')`.",
 sql_intro="`corr` (correlated subquery) and `rng` (LEAD-based range join) in the Code block; both gave the same rows.",
 sqls=["corr", "rng"],
 pd_intro="`merge_asof` on the date columns with `by=\"currency\"`, both frames sorted on their key.",
 pd_range=("# pandas merge_asof", "print(); print(\"pandas merge_asof:\")"),
 example="USD rates: 83.0 from 01-01, 84.5 from 02-01, 85.25 from 03-01; EUR rates: 90.0 from 01-15, 91.5 from 02-15, 93.0 from 03-15. Payment 1 (USD, 01-10, 100) uses 83.0, so 8300. Payment 2 (USD, exactly 02-01, 200) uses the rate that starts that day, 84.5, so 16900. Payment 3 (USD, 02-28, 50) is still in the 84.5 period, 4225. Payment 4 (USD, 04-10, 10) is after the last row, so the last rate 85.25 applies, 852.5. Payment 5 (EUR, 01-10) is before the first EUR rate: NULL. Payment 6 (EUR, exactly 03-15, 40) uses 93.0, 3720. Payment 7 (GBP) has no rate rows at all: NULL.",
 edge="""- **Exact valid_from date:** the rate applies from that day, so the test is `valid_from <= paid_on` (not `<`). In pandas this is `allow_exact_matches=True` (the default); with `False` my run gave payment 2 the older rate 83.0.
- **No earlier rate:** the subquery returns NULL, and `amount * NULL` is NULL, so the amount stays NULL, not 0 (payments 5 and 7). A 0 would silently understate revenue.
- **After the last row:** the last rate carries on forever (payment 4). In a real system decide on a staleness limit.
- **Duplicate valid_from for the same currency:** the subquery's LIMIT 1 would pick arbitrarily and the range join would return two rows per payment; add a unique key on `(currency, valid_from)`.
- **Rounding:** `ROUND(x, 2)` in SQLite and `Series.round(2)` in pandas can differ on exact halves (Part 10 found 703.125 gives 703.13 in SQLite and 703.12 in pandas); none of these seven products sits on a half. Money should be integer paise in a real table.
- **Types:** `merge_asof` needs matching key dtypes (both datetime here) and both frames sorted on their keys.""",
 explain="""- **Correlated subquery:** the readable answer and it runs one lookup per payment. An index on `(currency, valid_from)` makes each lookup a seek (Part 11).
- **Range join:** `LEAD(valid_from)` turns the history into half-open ranges `[valid_from, valid_to)`; the payment matches the range that contains its date. A LEFT JOIN keeps unmatched payments with a NULL rate. It scales better when the payment table is large and the join can use the range.
- **pandas:** `merge_asof` is exactly the "nearest earlier" join (Part 2 Q36); the result order follows the sorted left frame, so the code sorts back by `payment_id` before comparing.
- **Why not a plain join:** an equality join on the date would match only payments made exactly on a rate change.
- **Other engines:** PostgreSQL, SQL Server and Snowflake accept the same correlated subquery (some prefer `TOP 1` or `FETCH FIRST 1 ROW ONLY`); ASOF JOIN exists in some engines (not executed here).
""" + scoring(25, "T2", "Q5 of 5", "all 7 payments with the right rate, NULL where none", "joining on equality earns little; a subquery that uses `<` instead of `<=` fails payments 2 and 6 and loses the exact-date edge points; returning 0 instead of NULL loses the NULL points"),
 follow="""- *Convert at the rate at month end instead?* Pick the rate with `valid_from <= month_end` and join on the month.
- *Payments in INR itself?* Add an `INR` row with rate 1.0 or a CASE; otherwise INR has no rate row and comes out NULL.
- *Many payments?* Index `(currency, valid_from)` and batch the lookup.""",
 mistakes="""- Equality join on the date.
- Using the next rate (`>=` with ASC) instead of the previous one.
- `<` instead of `<=` for the exact valid_from day.
- Showing 0 for missing rates.
- Calling `merge_asof` on unsorted or differently typed keys.""")

# ---------------------------------------------------------------- Q8
Q[8] = mk(
 say="(a) GROUP BY entry_id and keep entries where SUM(debit) differs from SUM(credit); (b) for WALLET compute the running SUM of credit minus debit with an explicit ROWS frame ordered by posted_at, entry_id, line_no and take the first row below zero; never RANGE, because tied rows would get the same balance and hide the dip.",
 sql_intro="`unbal_sql`, `run_sql` and `first_neg_sql` in the Code block (`range_sql` is the RANGE version for comparison).",
 sqls=["unbal_sql", "run_sql", "first_neg_sql"],
 pd_intro="a groupby for the balance check, then sort by the three keys, `cumsum` of credit minus debit and the first row below zero.",
 pd_range=("# pandas\njl =", "print(\"pandas unbalanced:\")"),
 example="Six entries of two lines each. Entry 5 has debit 100 and credit 90, so it is unbalanced by 10. WALLET lines: entry 1 credit 500 at 09:00, balance 500; entry 2 debit 200 at 10:00, balance 300; entry 3 debit 400 at 11:00:00 and entry 4 credit 300 at the same 11:00:00; entry 6 credit 50 at 13:00. With the tie broken by entry_id, the 400 debit comes first: 300 minus 400 gives minus 100, the first negative posting (entry 3, line 1), then plus 300 gives 200, then plus 50 gives 250. If the tie were applied together, the net is minus 100 plus 300, and the balance would go straight from 300 to 200 and never be negative.",
 edge="""- **Tie rule:** two WALLET lines share 11:00:00. I order by `(entry_id, line_no)` as the prompt says. That is deterministic but arbitrary: with the credit first the balance would never dip. In real ledgers state which rule you use, or compare after netting everything with the same timestamp.
- **RANGE hides it:** with `ORDER BY posted_at` and the default frame (RANGE, peers included) both tied rows showed 200 in my run and the minimum was 200. The dip to minus 100 disappears.
- **Never negative:** the LIMIT 1 query returns no row, and the pandas `head(1)` returns an empty frame, so handle an empty result as "never".
- **Unbalanced detection** uses SUM, which skips NULL; a line with NULL debit and NULL credit is invisible. COALESCE if lines can carry NULLs. Rounding is not an issue because the amounts are integer paise.
- **Entries with lines on different posted_at** are fine for (a), which groups by entry only.
- **The `account` table** is joined in the running-balance query to validate accounts; use LEFT JOIN if a line with an unknown account must not vanish silently.""",
 explain="""- **Why the ROWS frame:** ROWS counts physical rows in the order given, so each line gets its own running value. RANGE treats rows with the same ORDER BY value as one group (peers) and gives them the same value; the default frame when ORDER BY is present is RANGE UNBOUNDED PRECEDING, which is the usual trap (Part 5 Q6).
- **Why the order key has three parts:** `posted_at, entry_id, line_no` makes every row distinct, so the running balance is reproducible between runs.
- **(a) is plain aggregation:** `HAVING SUM(debit_paise) <> SUM(credit_paise)`; the difference column is debits minus credits (10 for entry 5).
- **pandas:** `cumsum` after `sort_values` is the ROWS frame; there is no RANGE behaviour to worry about unless you group by timestamp first.
- **Double entry:** every entry must sum debits equal to credits; this book's seed also keeps the sign rule (WALLET is a liability, so credits increase it) as a stated assumption.
""" + scoring(25, "T2", "Q4 of 5", "unbalanced entry 5 with diff 10 and the first negative WALLET posting at entry 3 line 1", "(a) only is about half of the query points; a RANGE or timestamp-only ORDER BY running balance finds no negative and loses the tie points; naming the tie rule is the assumption credit"),
 follow="""- *Which account balances are negative at the end of day?* Group the running balance per day, take the last row.
- *Enforce balance in the schema?* A deferred constraint or a check in the posting code; not executed here.
- *Net the tie instead?* Group by `posted_at` first, then cumulative sum; the dip would not be reported.""",
 mistakes="""- `ORDER BY posted_at` alone with the default RANGE frame.
- Adding debits and credits on the wrong sign for the account kind.
- Comparing SUM(debit) with SUM(credit) over the whole table instead of per entry.
- Forgetting to state the tie rule.
- Returning the lowest balance instead of the first posting that went below zero (a different question).""")

# ---------------------------------------------------------------- Q9
def q9_schema(code):
    return "-- the DataFrames in the Code block are loaded into SQLite with to_sql, which creates these tables:\n-- customers(customer_id INTEGER, city TEXT)\n-- txns(txn_id INTEGER, customer_id INTEGER, txn_date TEXT, amount INTEGER)\n" + between(code, "customers = pd.DataFrame", "con = sqlite3.connect")
Q[9] = mk(
 say="Start from the pandas frames: filter the transactions to 2025-06-01 to 2025-06-30, sum per customer, map onto the customers table so a customer with no transactions gets 0, divide by the city total and rank within city with `method='min'`; the SQL is a LEFT JOIN from customers to the pre-aggregated window plus SUM() OVER and RANK() OVER.",
 sql_intro="`sql` and `orphan_sql` in the Code block.",
 sqls=["sql", "orphan_sql"],
 pd_intro="the pandas version is written first in the Code block (pandas-first, as the prompt says).",
 pd_range=("# pandas first.", "print(\"window:\""),
 schema_fn=q9_schema, schema_label="**Schema and sample data (pandas DataFrames first; to_sql creates the SQLite tables):**",
 example="The window is 30 days ending 2025-06-30 inclusive: 2025-06-01 to 2025-06-30. Pune: customer 1 has 100 and 50 in the window (and a 777 on 07-01, outside) = 150; customer 2 has 150 in the window (and 999 on 05-31, outside) = 150; customer 3 has 100. City total 400, so shares 0.375, 0.375, 0.25. Customers 1 and 2 tie for rank 1 and customer 3 is rank 3 (RANK leaves a gap). Delhi: customer 4 has 60, 40 and a 0 amount = 100; customer 5 has 50; customer 6 has no transactions and shows 0. City total 150, shares 0.6667, 0.3333, 0.0. Transaction 10 belongs to customer 99, who is not in `customers`: it is not in any city table and is reported on its own (1 transaction, amount 300).",
 edge="""- **Orphan transaction:** it has no city, so it cannot be in a city share. I keep it out of the city table, and print it in a separate result so the 300 is not lost. The alternative is an UNKNOWN city row; say which you chose. A plain inner join would drop it silently and a customers-only LEFT JOIN would too, so it needs its own anti-join check.
- **Customer with no transactions** stays because the join starts from `customers`; the amount is filled with 0 (`COALESCE` in SQL, `fillna(0)` in pandas).
- **Window boundary:** `as-of minus 29 days` through the as-of date is 30 days. My off-by-one check with minus 30 days (31 days) pulled in 05-31 and gave customer 2 an amount of 1149 instead of 150.
- **Ties:** equal amounts share a rank and the next rank skips (1, 1, 3); `method='dense'` or DENSE_RANK would give 1, 1, 2. A zero-amount customer still gets a rank.
- **City total zero:** the share would divide by zero; `NULLIF` in SQL and `where(total != 0)` in pandas give NULL/NaN. Not seeded here, since both cities have transactions.
- **Rounding:** `ROUND(..., 4)` in SQLite and `.round(4)` in pandas can differ on exact halves (Part 10); none of these shares is on a half. `map` plus `fillna` makes the amount a float in pandas, so the code casts it back to int.""",
 explain="""- **Order of operations:** filter the window before aggregating; do the LEFT JOIN from the customers table after the aggregate, so customers without rows survive and the join cannot fan out.
- **Share:** `amount / SUM(amount) OVER (PARTITION BY city)`; the window function sees only the customer rows, not the orphan.
- **Rank:** `RANK() OVER (PARTITION BY city ORDER BY amount DESC)` equals `rank(method="min", ascending=False)` (Part 4 Q2 and Q14; pandas Part 4 Q31).
- **Equality of the two answers:** the assert compares the whole table in the order city, rank, customer_id, plus the orphan result.
- **Date handling:** pandas compares datetime values, SQL compares ISO text; both are right because ISO dates sort as text. If the column held timestamps, use `< as_of + 1 day` rather than `<= as_of`.
""" + scoring(25, "T3", "Q5 of 5", "the 6-row table with correct zero amounts, shares and tied ranks", "a table that loses customer 6 (inner join) or ranks with ROW_NUMBER loses most query points; the explicit orphan result is the edge-case credit; writing the pandas version first and the SQL second is graded on equality, not order"),
 follow="""- *Same table for a rolling 30 days each day?* Add a date spine and a range or self-join per day; the engine specifics are Part 5.
- *Orphans as a data-quality alert?* Run the orphan query on every load and fail on a threshold.
- *Dense rank instead?* Change `method="min"` to `"dense"` and `RANK` to `DENSE_RANK`.""",
 mistakes="""- Inner join, so a customer with no transactions disappears.
- Filtering the window in WHERE after a LEFT JOIN, which turns it into an inner join.
- Including the orphan in a city total by accident.
- Off-by-one on the 30 days.
- ROW_NUMBER instead of RANK, so tied customers get different ranks.""")

# ---------------------------------------------------------------- Q10
Q[10] = mk(
 say="Define the buckets first: new (first ever active month is this one), retained (active this month and last month), resurrected (active this month, not last month, but active in some earlier month), churned (active last month and not this month); then compute each from monthly distinct customer sets over a month spine.",
 sql_intro="`sql` in the Code block (a VALUES CTE for the spine, `am` for distinct customer-months, `fst` for first months).",
 sqls=["sql"],
 pd_intro="a dictionary of monthly sets, then set operations per month: `cur & prev`, `(cur - prev) & earlier`, `prev - cur`.",
 pd_range=("# pandas: monthly sets", "p = pd.DataFrame(rows)"),
 example="Active sets: Dec 2024 {1}; Jan {1, 2, 5}; Feb {1, 3}; Mar {1, 3, 4, 6}; Apr {2, 7}; May {2, 4, 7}; Jun {7, 8}. First months: customer 6 in Oct 2024 and customer 1 in Dec 2024, so neither is new in 2025. Jan: active 3, new {2, 5} = 2, retained {1} = 1 (active in Dec too), churned 0. Feb: active 2, new {3}, retained {1}, churned {2, 5} = 2. Mar: active 4, new {4}, retained {1, 3}, resurrected {6} (not in Feb, active back in Oct), churned 0. Apr: active 2, new {7}, resurrected {2} (seen in Jan), churned {1, 3, 4, 6} = 4. May: active 3, new 0, retained {2, 7}, resurrected {4}, churned 0. Jun: active 2, new {8}, retained {7}, churned {2, 4} = 2. The identity active = new + retained + resurrected holds every month.",
 edge="""- **Several rows per day or month:** `SELECT DISTINCT customer_id, substr(activity_date, 1, 7)` collapses them first; customer 1 has two January rows and counts once.
- **Activity before the spine:** customers 1 and 6 were active in Oct and Dec 2024. They are not new in 2025, and January retained and Mar resurrected need those earlier months, so the activity table must not be cut at January.
- **Churn is per event:** customer 4 is churned in April and resurrected in May; customer 2 churned in Feb (not active) and appears again in Apr. A customer can be counted in churned many times over the year.
- **Month spine:** a CTE with VALUES gives the six months even if one had no activity. Previous month is computed with `strftime('%Y-%m', m || '-01', '-1 month')`; anchoring on the first of the month avoids month-end rollover (Part 10 found DATE('2024-02-30') rolls over).
- **Churned reading:** it counts customers active last month and not this month, not customers inactive for N days.
- **Empty month:** `sets.get(m, set())` in pandas and COUNT over an empty subquery in SQL both give 0.""",
 explain="""- **Definitions:** new is about the first month ever; retained and resurrected are about the pair (this month, last month) plus earlier history; churned looks backwards from the last month. These four plus the identity let you check your own numbers.
- **SQL:** each bucket is a count of rows in `am` with an EXISTS or NOT EXISTS against the previous month or an earlier month. The correlated subqueries are small on this data; on a big table build one row per customer-month with LAG and a running first-month instead.
- **pandas:** monthly sets make the definitions almost literal. `(cur - prev) & earlier` is "not last month but earlier"; `earlier` is the union of all months before the previous one.
- **Sanity checks:** active this month equals new plus retained plus resurrected; and active last month equals retained plus churned. My run asserted the first on the SQL side.
- Part 6 Q33 and Q18 cover the building blocks; this question joins them.
""" + scoring(25, "T3", "Q4 of 5", "all four buckets for all six months", "new and retained only is about half of the query points; mixing up resurrected with new loses the edge points; the one-sentence definitions are the assumption credit and the identity is the one-line check"),
 follow="""- *Reactivation after 90 days of silence?* Compare each activity month with the gap since the previous one (LAG on months) instead of fixed previous-month sets.
- *Quick-ratio style metric?* (new + resurrected) divided by churned per month, with a NULLIF guard.
- *Daily instead of monthly?* Same logic over a date spine, but the sets get large; use LAG over distinct days.""",
 mistakes="""- Counting rows instead of distinct customers when there are several rows per month.
- Cutting the activity history at January so first months are wrong.
- Defining resurrected as 'new again' without the earlier-history test.
- Forgetting that prev for January is December of the previous year.
- Starting the spine from the first month with data, so empty months are missing.""")
