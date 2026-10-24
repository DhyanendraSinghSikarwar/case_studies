@@Q35
**Say this first (1 line):** `merge` never casts a key for you: `int64` against `str` or `object` raises `ValueError`, but text against text, or a mixed `object` column, matches silently wrong, and a `float64` key (because of NaN) merges fine while the NaN rows can never match; so clean the key to one dtype (`str.strip`, `to_numeric`, `astype('Int64')`) and always check the unmatched rows after the merge.

**Schema and sample data:** customers has an `int64` key. The orders CSV has a trailing space on one key (`2 `), a blank key, and an unknown customer (7).
```text
order_id,customer_id
10,1
11,2 
12,3
13,
14,3
15,7
```
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders_raw(order_id INTEGER, customer_id TEXT);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders_raw VALUES (10,'1'),(11,'2 '),(12,'3'),(13,NULL),(14,'3'),(15,'7');
```

**SQL answer:** SQL has no dtype error to catch you here, so the point is the explicit cast. `SQL_IMPLICIT` is the lazy join and `SQL_FIX` is the safe one (both run in the Code block):
```sql
SELECT o.order_id, c.name FROM orders_raw o LEFT JOIN customers c ON c.customer_id = o.customer_id
ORDER BY o.order_id
```
```sql
SELECT o.order_id, CAST(NULLIF(TRIM(o.customer_id), '') AS INTEGER) AS customer_id, c.name,
       CASE WHEN c.customer_id IS NULL THEN 'left_only' ELSE 'both' END AS _merge
FROM orders_raw o
LEFT JOIN customers c ON c.customer_id = CAST(NULLIF(TRIM(o.customer_id), '') AS INTEGER)
ORDER BY o.order_id
```
`NULLIF(..., '')` matters: in SQLite `CAST('' AS INTEGER)` and `CAST('x' AS INTEGER)` both give 0 (see the output), so without it a blank or junk key silently becomes key 0.

**pandas answer:** read, strip, convert, merge with `indicator=True`, then look at what did not match (same lines as in the Code block):
```py
orders["customer_id"] = pd.to_numeric(orders["customer_id"].str.strip(), errors="coerce").astype("Int64")
p = orders.merge(customers, on="customer_id", how="left", indicator=True)
unmatched = p[p["_merge"] != "both"]
```

**Example:** walk the six order rows through the fixed join. 10 has key 1, so Asha. 11 has `'2 '`, which strips to 2, so Ben. 12 has 3, so Chitra. 13 is blank, so NaN, so no match. 14 is 3 again, so Chitra. 15 has key 7, and there is no customer 7, so no match. Unmatched orders are therefore 13 and 15. Without the strip, text against text also loses order 11, giving 11, 13 and 15, and nothing warns you.

**Code:** run with `python3 -I`; the SQL and pandas fixed results are compared sorted by `order_id` with `assert_frame_equal`.
{{CODE:q35}}

**Output (my run):**
{{OUT:q35}}

**Edge cases:**
- **int64 against str or object:** `ValueError: You are trying to merge on int64 and str columns ...` (the message says `object` when the column really is object dtype). On pandas 3.0.5 a text column read from CSV with `dtype=str` shows as `str`; both raised in my run.
- **Silent wrong results, no error:** text against text with a stray space (`'2 '` does not equal `'2'`), and an `object` column holding both ints and strings (the string `'2'` did not match the int 2 and the row fell out of the match, with no error).
- **float64 key because of NaN:** int64 against float64 merges without error and `1.0` matches `1`. The NaN row simply finds no partner. If a float key holds a non-integer value (2.5), pandas only emits a `UserWarning` (seen in my run). And `astype('Int64')` on a column containing 1.5 raised `TypeError`, which is the safe behaviour.
- **Leading and trailing spaces and the numeric cast:** in my run `to_numeric` and `astype('Int64')` both accepted `' 2'` without strip (Python's `int()` tolerates spaces). So the strip is essential for text keys that stay text (names, codes, ids with letters), and a good habit for numeric ones, but do not claim the cast fails without it.
- **Leading zeros:** `'01'` and `'1'` are different text keys but the same number. Decide which meaning you want before choosing text or integer.
- **NaN keys on both sides do match in pandas:** with NaN in both frames, an inner merge joined the NaN row to the NaN row (`Unknown` with order 13 in my run), while the SQL join `NULL = NULL` returned 0 rows. In this question's fixed merge only orders has a missing key, so that row is just `left_only`, but if the customer table also had a NaN key you would get false matches; drop or flag missing keys before merging.

**Then explain:**
- **Why pandas raises for int against str:** it refuses to guess a cast, because the guess could hide a data problem. `object` columns are the dangerous case: they can hold anything, so a mismatch may not be caught.
- **The fix order:** strip, then convert, with `errors="coerce"` so bad values become NaN rather than crash, then `Int64` (capital I) so the key keeps integers and still allows missing values. Plain `int64` cannot hold NaN.
- **The check that matters:** `indicator=True` and look at `left_only`, or compare the row count and the number of matched keys. A merge that silently matches fewer rows than expected is the real risk.
- **SQL implicit casting (ran on SQLite 3.45.1):** joining a TEXT column to an INTEGER column did match (`'2 '` matched 2 and Ben appeared), because SQLite applies numeric affinity to the text side. A bare literal comparison `1 = '1'` gave 0 in the same engine, so the rule depends on column affinity. This is engine dependent and I only ran SQLite.
- **Other engines, not executed here:** PostgreSQL normally errors on `integer = text` for columns (`operator does not exist`), MySQL converts strings to numbers silently (and that conversion can stop an index being used), SQL Server converts by data type precedence and fails with a conversion error on a bad value like `'x'`. Check the manual of your engine.

**Follow-ups:**
- *How do you stop this at load time?* Pass `dtype={"customer_id": "Int64"}` or convert explicitly right after `read_csv`, and assert `df["customer_id"].notna().all()` where blanks are not allowed.
- *Should the key be int or str?* If ids are codes (leading zeros, letters), keep them as stripped text on both sides; if they are numbers, use `Int64`.
- *How do you find which values break the cast?* `bad = s[pd.to_numeric(s.str.strip(), errors="coerce").isna() & s.notna()]`.

**Common mistakes:**
- Casting with `astype(int)` on a column with NaN and getting an error, then dropping rows to make it pass.
- Trusting a merge that did not raise: no error does not mean all rows matched.
- Using `COALESCE(key, 0)` or `CAST('' AS INTEGER)` and creating a fake customer 0.
- Fixing the dtype on one frame only, so the other side still holds text.

@@Q36
**Say this first (1 line):** `pd.merge_asof` is the "latest quote at or before the trade" join (backward direction by default, both frames sorted by time, `by="ticker"`), and the portable SQL is a LEFT JOIN with a correlated `MAX(quote_time)` subquery in the ON clause; SQLite 3.45 has no `ASOF JOIN`.

**Schema and sample data:**
```sql
{{VAR:q36:SCHEMA}}
```

**SQL answer:** `SQL_MAIN` (the three variants `SQL_MAIN`, `SQL_TOL` for a 30 second tolerance and `SQL_STRICT` for strictly earlier are all in the Code block; `SQL_STRICT` is `SQL_MAIN` with `<=` changed to `<`):
```sql
{{VAR:q36:SQL_MAIN}}
```
The subquery finds, per trade, the latest quote time for the same ticker that is not after the trade. The outer join then fetches that quote row. LEFT JOIN keeps trades that have no earlier quote (they get NULL).

Not executed: DuckDB, Snowflake and ClickHouse, to my knowledge, have a native `ASOF JOIN` (syntax differs by engine), which does this in one clause. SQLite 3.45 rejected it in my run (`near "ASOF": syntax error`).

**pandas answer:** (same text as in the Code block)
```py
out = pd.merge_asof(trades.sort_values("trade_time"), quotes.sort_values("quote_time"),
                    left_on="trade_time", right_on="quote_time", by="ticker", **kw)
```
Here `**kw` is empty for the plain case, `tolerance=pd.Timedelta("30s")` for the tolerance case, `allow_exact_matches=False` for strictly earlier, and `direction="forward"` or `"nearest"` for the other directions. The `asof` helper in the Code block then restores the order by `trade_id`.

**Example:** quotes for A at 09:00:02 (10.0), 09:00:10 (10.5), 09:00:12 (11.0); for B at 09:00:03 (20.0) and 09:00:08 (21.0).
- Trade 1 (A, 09:00:05): latest A quote at or before is 09:00:02, so bid 10.0.
- Trade 2 (A, 09:00:10): there is a quote at exactly 09:00:10, so bid 10.5. With `allow_exact_matches=False` it would take the 09:00:02 quote, bid 10.0.
- Trade 3 (B, 09:00:07): B quote at 09:00:03, so 20.0 (the 09:00:08 quote is in the future).
- Trade 4 (A, 09:00:01): no quote before it, so NULL.
- Trade 5 (B, 09:01:30): latest quote is 09:00:08 (82 seconds old), so 21.0, or NULL with a 30 second tolerance.

**Code:** run with `python3 -I`; each of the three SQL variants is compared with its `merge_asof` call after sorting by `trade_id`.
{{CODE:q36}}

**Output (my run):**
{{OUT:q36}}

**Edge cases:**
- **Unsorted input:** `merge_asof` raised `ValueError: left keys must be sorted` in my run. Sort both frames on the time key (globally, not per ticker; `by` handles the ticker).
- **Duplicate quote timestamps:** with two quotes for A at 09:00:12 (11.0 and 11.2) the SQL returned two rows for the trade at 09:00:20 (`[11.0, 11.2]`), but `merge_asof` returned one (`[11.2]`, the later row). This is an honest difference: SQL needs a tie-break (a quote id or sequence number) to pick one row, `merge_asof` took the last of the tied rows (11.2).
- **No earlier quote:** NULL in SQL, NaN and NaT in pandas.
- **Tolerance:** in pandas it applies to the chosen quote, and a stale quote gives NaN; in SQL I put the age test in the ON clause, so the trade row is kept with NULLs (do not move it to WHERE, which would drop the trade).
- **Direction:** `forward` and `nearest` have no one-line SQL form; you would need a `MIN(quote_time) ... >=` subquery or a comparison of two subqueries.
- **Time zones and text timestamps:** my SQL compares ISO 8601 text (`YYYY-MM-DD HH:MM:SS`), which sorts correctly as text. Mixed formats or time zones would break that, and in pandas make both columns the same tz-aware or tz-naive dtype.

**Then explain:**
- **Why an equality join does not work:** quotes and trades almost never share a timestamp, so you need "the nearest one before".
- **The SQL idea:** a correlated subquery returns the right quote time, then an equality join on it. A window-function version also exists (Parts 4 and 5), not used here.
- **Cost:** the correlated subquery is fast only with an index on `(ticker, quote_time)`; `merge_asof` is a sorted merge scan and is typically much faster on large frames (concept; I did not benchmark).
- **`by`:** matches the ticker exactly, then finds the nearest time within it.
- **`allow_exact_matches=False`:** turns `<=` into `<`, which is what you want if a quote at the same instant may have been caused by the trade.

**Follow-ups:**
- *What if quotes arrive after the trade but you want the next one?* `direction="forward"`, which in SQL is `MIN(quote_time)` with `>=`.
- *What if the quotes table is huge?* Index `(ticker, quote_time)` for the SQL version, or pre-filter the day.
- *How would you handle ties in quote_time?* Add a sequence column and pick by `MAX(seq)`; in pandas sort by the time then the sequence before `merge_asof`.

**Common mistakes:**
- Forgetting to sort, or sorting by ticker then time (the key `on` must be sorted globally).
- Putting the tolerance condition in WHERE, which drops the unmatched trades.
- Using `BETWEEN` or `<=` on the join without a `MAX`, which returns every older quote for every trade (a fan-out).
- Merging on `ticker` first with a normal merge and then filtering (a huge intermediate result).

@@Q37
**Say this first (1 line):** Join the table to itself on `order_id` with `a.product_id < b.product_id` so each pair appears once, `GROUP BY` the pair and `COUNT(*)` orders, but dedupe the lines first, or an order that has the same product on two lines counts a pair twice.

**Schema and sample data:**
```sql
{{VAR:q37:SCHEMA}}
```

**SQL answer:** `SQL_MAIN` in the Code block (derived tables, no CTE, because CTEs are Part 3):
```sql
{{VAR:q37:SQL_MAIN}}
```
`SQL_NAIVE` in the Code block is the same query on `order_items` directly (no `DISTINCT`), kept to show the inflation.

**pandas answer:** (same text as in the Code block)
```py
basket = items.drop_duplicates()
pairs = basket.merge(basket, on="order_id", suffixes=("_1", "_2"))
pairs = pairs[pairs["product_id_1"] < pairs["product_id_2"]]
counts = pairs[["product_id_1", "product_id_2"]].value_counts()      # a Series indexed by the pair
```
After that the Code block renames the columns and sorts by count descending then the two ids, so ties come out in a fixed order, then takes `head(10)`.

**Example:** six orders. Order 1 has A, B, C, so pairs AB, AC, BC. Order 2 has A, B, so AB. Order 3 has A, C, so AC. Order 4 has B, C, A, so AB, AC, BC. Order 5 has A, B, B (B twice), so AB after deduplication. Order 6 has only D, so no pair. Totals: AB in orders 1, 2, 4 and 5 is 4; AC in 1, 3, 4 is 3; BC in 1 and 4 is 2. Without the dedupe, order 5 produces AB twice (A with each B line), giving 5, which is wrong.

**Code:** run with `python3 -I`; the SQL result and the pandas result are compared in the order `n_orders` descending, then `p1`, then `p2`.
{{CODE:q37}}

**Output (my run):**
{{OUT:q37}}

**Edge cases:**
- **Only three pairs exist in my toy data, so "top ten" returns three rows.** `LIMIT 10` is an upper bound, not a promise of ten.
- **Duplicate lines:** the naive version gave AB = 5 instead of 4. The fix is `SELECT DISTINCT order_id, product_id` on both sides (or a unique constraint on `(order_id, product_id)`).
- **Ties at the cut-off:** `LIMIT 10` cuts arbitrarily among equal counts unless the `ORDER BY` has a tie-break, which is why the query sorts by `p1, p2` after the count.
- **Single-item orders (D):** they produce no pair rows, which is correct.
- **`<` versus `<>`:** `<>` would give both (A,B) and (B,A), doubling every count; `<` also removes the (A,A) self pair.

**Then explain:**
- **Row growth:** an order with n distinct products creates n(n-1)/2 pair rows (3, 45 and 4950 rows for baskets of 3, 10 and 100 products in my run). One very large order (a bulk or test order) can dominate the join. Cap basket size, or filter out baskets above a limit, before the self join.
- **Why filter products first for scale:** keep only products with some minimum frequency before self-joining, since a pair cannot be common if one of its items is rare (this is the idea behind support thresholds; I describe it, I did not run it).
- **Count meaning:** `COUNT(*)` after the dedupe is the number of orders containing both products, which is what "bought together" means. It is not the units sold.
- **pandas:** the self-merge makes the same row blow-up in memory; `value_counts` on two columns counts each pair, and ties come out in no guaranteed order, so I sort explicitly before `head`.

**Follow-ups:**
- *How would you add lift or confidence?* Divide the pair count by the product counts (each from `COUNT(DISTINCT order_id)` on one product); that is a second aggregation joined back on.
- *Triples?* A three-way self join with `a < b < c`; growth is cubic, so filter first.
- *Can you avoid the self join?* Not easily in pure SQL; some engines allow array aggregation then unnesting, which is outside this part.

**Common mistakes:**
- Using `<>`, which doubles every pair.
- Not deduping duplicate lines, inflating counts.
- No tie-break in `ORDER BY ... LIMIT`.
- Running the self join on the full line table with huge baskets and wondering why it crawls.

@@Q38
**Say this first (1 line):** The bridge table `enrollments` holds one row per student and course; "no course" is an anti-join, "every course" is `GROUP BY student HAVING COUNT(DISTINCT course_id) = (SELECT COUNT(*) FROM courses)`, and "pairs sharing a course" is a self join on `course_id` with `a.student_id < b.student_id`, always on de-duplicated enrolment rows.

**Schema and sample data:**
```sql
{{VAR:q38:SCHEMA}}
```
Ben has a duplicated row (course 10 twice); Dev has no enrolment.

**SQL answer:** the queries are `SQL_NONE`, `SQL_ALL`, `SQL_ALL_WRONG` (the trap) and `SQL_PAIRS` in the Code block.
```sql
{{VAR:q38:SQL_NONE}}
```
```sql
{{VAR:q38:SQL_ALL}}
```
```sql
{{VAR:q38:SQL_PAIRS}}
```

**pandas answer:** (same text as in the Code block)
```py
none_p = students.loc[~students["student_id"].isin(enr["student_id"]), "name"].tolist()
valid = enr.drop_duplicates().merge(courses[["course_id"]], on="course_id")           # drop dups, keep real courses
n_courses = valid.groupby("student_id")["course_id"].nunique()
all_ids = n_courses[n_courses == len(courses)].index
d = enr.drop_duplicates()
pp = d.merge(d, on="course_id", suffixes=("_1", "_2"))
pp = pp[pp["student_id_1"] < pp["student_id_2"]]
```

**Example:** Courses are 10, 20, 30. Asha: 10, 20, 30, so all three. Ben: 10, 10, 20, so two distinct (three rows). Chitra: 10, 20, 30, so all three. Dev: nothing. Esha: 30 only.
- No enrolment: Dev.
- Every course: Asha and Chitra. Ben's three rows would pass `COUNT(*) = 3`, which is wrong; `COUNT(DISTINCT course_id)` gives 2 and rejects him.
- Pairs: course 10 has Asha, Ben, Chitra, giving (1,2), (1,3), (2,3); course 20 gives the same three; course 30 has Asha, Chitra, Esha, giving (1,3), (1,5), (3,5). Shared courses per pair: (1,2) 2, (1,3) 3, (2,3) 2, (1,5) 1, (3,5) 1.

**Code:** run with `python3 -I`; pairs are compared sorted by `s1, s2`, and the two name lists are compared in `student_id` order.
{{CODE:q38}}

**Output (my run):**
{{OUT:q38}}

**Edge cases:**
- **Duplicate enrolments:** `COUNT(e.course_id)` returned Ben as enrolled in every course (output line "COUNT(e.course_id) instead of DISTINCT (wrong)"). The pairs query without the `DISTINCT` inflated (1,2), (2,3) from 2 to 3 shared courses.
- **Enrolments for a course that does not exist:** the division query joins to `courses`, so an orphan `course_id` cannot make a student look complete. In pandas the same is the merge with `courses`.
- **No courses at all:** mathematically everyone "took every course" (an empty set), but the `GROUP BY` form returned nobody (empty output in my run), because it only sees students who have enrolments. Decide what you want if the courses table can be empty.
- **A student with no rows in `enrollments`:** not in the division result unless you start from `students`; they are in the "no course" result.
- **Pairs sharing no course:** do not appear; to list all pairs you would need a cross join and an anti-join.

**Then explain:**
- **Bridge table:** many-to-many is stored as a third table with one row per (student, course), and ideally a primary key on the pair, which would also stop duplicate rows at the source.
- **Relational division by counting:** "has every course" equals "has as many distinct courses as exist", valid only if each counted row is a real course, so join to `courses` first and count distinct.
- **Other forms (not run):** a double `NOT EXISTS` expresses division without counting and is robust to duplicates; I did not run it here.
- **Pair self join:** `a.student_id < b.student_id` removes mirror pairs and self pairs; the join on `course_id` gives one row per shared course, so `COUNT(*)` is the number of shared courses.

**Follow-ups:**
- *Students enrolled in exactly the same courses as another student?* Compare the sets; that is harder, and in SQL you would compare `COUNT(*)` of shared courses to each student's total.
- *Students with at least two courses?* `HAVING COUNT(DISTINCT course_id) >= 2`.
- *How do you stop duplicates?* `PRIMARY KEY (student_id, course_id)` on the bridge table.

**Common mistakes:**
- `COUNT(*)` or `COUNT(course_id)` without `DISTINCT` in the division.
- Comparing with a hard-coded course count instead of `(SELECT COUNT(*) FROM courses)`.
- Using an INNER JOIN from `students` for the "no course" case (it cannot show the missing rows).
- Using `<>` for the pair join and returning each pair twice.

@@Q39
**Say this first (1 line):** In a FULL OUTER JOIN on `a.id = b.key`, `a.id` is NULL for right-only rows and `b.key` is NULL for left-only rows, so neither column is the full key set; select `COALESCE(a.id, b.key)` (or use `USING` where it exists), and group by that, never by one side.

**Schema and sample data:**
```sql
{{VAR:q39:SCHEMA}}
```

**SQL answer:** the queries are `SQL_RAW`, `SQL_MAIN`, `SQL_USING`, `SQL_GROUP_WRONG` and `SQL_GROUP_RIGHT` in the Code block.
```sql
{{VAR:q39:SQL_MAIN}}
```
```sql
{{VAR:q39:SQL_GROUP_RIGHT}}
```
SQLite 3.45 ran `FULL OUTER JOIN` and `USING`. `USING` needs a column with the same name on both sides, which is why `b2` repeats `b` with the key renamed to `id`. In engines that support USING (not executed: PostgreSQL, MySQL for the inner and left/right forms), the `USING` column is merged into one output column.

**pandas answer:** (same text as in the Code block)
```py
m_lr = a.merge(b, left_on="id", right_on="key", how="outer")
m_on = a.merge(b.rename(columns={"key": "id"}), on="id", how="outer")
m_lr["id"] = m_lr["id"].fillna(m_lr["key"])
```

**Example:** `a` has ids 1, 2, 3; `b` has keys 2, 3, 4, 5. The matched pairs are 2 and 3. Left-only is 1 (so `b.key` is NULL). Right-only are 4 and 5 (so `a.id` is NULL). Reading only `a.id` you would see 1, 2, 3, NULL, NULL and lose 4 and 5. `COALESCE(a.id, b.key)` gives 1, 2, 3, 4, 5. Grouping by `a.id` collapses 4 and 5 into one NULL group (2 rows, sum of y = 40 + 50 = 90); grouping by the coalesced key gives five groups.

**Code:** run with `python3 -I`; the coalesced SQL result is compared with both pandas forms (sorted by `id`), and the grouped totals are compared too.
{{CODE:q39}}

**Output (my run):**
{{OUT:q39}}

**Edge cases:**
- **Both sides NULL:** if a row in `a` has `id = NULL`, `COALESCE` returns the other side's key (also NULL if it is unmatched), and NULL keys never match each other in a SQL join (see Q6).
- **Sums over missing:** SQL `SUM(b.y)` for key 1 is NULL (no `b` rows). pandas `sum()` of an all-NaN group gives 0.0, which my first run showed as a mismatch against SQL; the Code block uses `sum(min_count=1)` to get NaN like SQL.
- **pandas groupby drops NaN keys:** `groupby("id")` on the uncoalesced column dropped the NaN group (keys 4 and 5 vanished from the totals); `dropna=False` kept them as one NaN group, like SQL.
- **dtypes:** with `left_on`/`right_on` the key columns became `float64` (NaN needs float); with `on=` the key stayed `int64`.
- **Which column is "right"?** `a.id` is the left key and `b.key` the right key; with `on=` pandas fills both into one column.

**Then explain:**
- **Why:** a full join keeps unmatched rows from both sides; for each unmatched row the other side's columns are NULL, including its key column.
- **SQL fixes:** `COALESCE(a.id, b.key)` in SELECT, GROUP BY and any later join; or `USING (id)` where supported.
- **pandas:** `on="id"` (same name on both sides) returns one key column, filled from whichever side has it; `left_on`/`right_on` returns both, like SQL's raw output.
- **Downstream GROUP BY:** group by the coalesced expression. In my run, `GROUP BY a.id` gave 4 groups (one NULL group of 2 rows summing 90) where the coalesced version gave 5.
- **Dialect (not executed):** in SQLite `SELECT l.id, r.id` with USING in a FULL JOIN kept the sides separate (see Q43 for the run), while `SELECT id` was coalesced; other engines differ in details, so check the manual.

**Follow-ups:**
- *What does `SELECT *` return for USING versus ON?* One key column versus both (verified for SQLite in Q43).
- *Can you ORDER BY the key?* Order by the coalesced expression (or its alias), otherwise NULL keys sort together.
- *What if the key names differ in pandas but you want one column?* Rename before the merge, or merge with `left_on`/`right_on` and then `fillna` as in the Code block.

**Common mistakes:**
- Selecting `a.id` and reporting the right-only rows with a NULL id.
- `GROUP BY a.id` after a full join.
- `WHERE a.id IS NULL` to find "only in b", when that is correct but then using `a.id` as the display key.
- Expecting `merge(left_on=..., right_on=...)` to merge the key columns for you.

@@Q40
**Say this first (1 line):** If 1,000 rows became 1,400, the join key is not unique on the side you added: define the expected grain, compare `COUNT(*)` with `COUNT(DISTINCT key)` before and after, find the duplicated keys with `GROUP BY ... HAVING COUNT(*) > 1`, test the join in isolation, then fix the data and add a guard.

**Schema and sample data:** 1,000 orders, 10 per customer for customers 1 to 100 (amount 10 each, so revenue is 10,000). `customer_dim` is a type 2 style table with an `is_current` flag. Customers 1 to 40 wrongly have two current rows, customers 41 to 60 have one old row and one current row (normal), and customers 61 to 100 have one current row. The Code block builds the data with a loop; the tables are:
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
CREATE TABLE customer_dim(customer_id INTEGER, segment TEXT, valid_from TEXT, is_current INTEGER);
```

**SQL answer:** the diagnosis queries run in the Code block, in order; the join that breaks and the fix are:
```sql
SELECT o.order_id, o.customer_id, o.amount, d.segment
FROM orders o JOIN customer_dim d ON d.customer_id = o.customer_id AND d.is_current = 1
```
```sql
SELECT customer_id, COUNT(*) AS n FROM customer_dim WHERE is_current = 1
GROUP BY customer_id HAVING COUNT(*) > 1 ORDER BY customer_id
```
```sql
SELECT o.order_id, o.customer_id, o.amount, d.segment
FROM orders o
JOIN customer_dim d
  ON d.customer_id = o.customer_id AND d.is_current = 1
 AND d.valid_from = (SELECT MAX(d2.valid_from) FROM customer_dim d2
                     WHERE d2.customer_id = d.customer_id AND d2.is_current = 1)
ORDER BY o.order_id
```
The fix picks the latest `valid_from` among the current rows, which is a business rule I chose for the example (the right rule depends on your data); it is better to repair the dimension at the source.

**pandas answer:** (same text as in the Code block)
```py
cur = cdim[cdim["is_current"] == 1]
orders.merge(cur, on="customer_id", validate="many_to_one")
latest = cur.sort_values("valid_from").drop_duplicates("customer_id", keep="last")
```

**Example:** the arithmetic is checkable by hand. 40 customers have two current rows, so each of their 10 orders matches twice: 40 customers x 10 orders x 1 extra row = 400 extra rows, 1,000 + 400 = 1,400. `SUM(amount)` goes from 10,000 to 14,000. Customers 41 to 60 do not add rows because their old row has `is_current = 0` and is filtered out in the join.

**Code:** run with `python3 -I`; the fixed SQL and fixed pandas results are compared sorted by `order_id`, and the row count is asserted to be 1,000.
{{CODE:q40}}

**Output (my run):**
{{OUT:q40}}

**Edge cases:**
- **Row count unchanged but totals wrong:** a join can also drop one row and duplicate another, so also compare `SUM` and `COUNT(DISTINCT order_id)`, not only `COUNT(*)`.
- **A LEFT JOIN with no match:** keeps the row once, so shrinking row counts point to an INNER JOIN or a filter in WHERE.
- **NULL keys:** orders with a NULL key match nothing and are not duplicated.
- **The unique index guard:** my partial unique index on `customer_id WHERE is_current = 1` made the duplicate insert fail with `IntegrityError`. Partial indexes exist in SQLite and PostgreSQL; MySQL and others differ (hedged, not executed).
- **pandas `MergeError` message:** it lists the duplicated key values (it printed customers 1 to 5 and `...`).

**Then explain:**
- **Step 1, grain:** say it out loud: one row per order. Check the base: 1,000 rows, 1,000 distinct `order_id`.
- **Step 2, after the join:** 1,400 rows but still 1,000 distinct `order_id` means fan-out (some orders repeated).
- **Step 3, find it:** group the joined table's key by `HAVING COUNT(*) > 1` (40 keys with 2 rows).
- **Step 4, isolate:** look at one key (customer 1 has two current rows), and run the join alone without other joins.
- **Step 5, guards:** a unique or partial unique index in the table, a row-count assertion after the join, `validate="many_to_one"` in pandas, and a dimension test in the pipeline.
- **Fix at the source versus in the query:** a query fix hides bad data and has to be repeated everywhere; fix the dimension load and keep the query guard as a second line.

**Follow-ups:**
- *What if the row count went down?* Look for an INNER JOIN or a WHERE on the right table; compare `left_only` rows.
- *Which is faster to detect, count or sum?* Both; sums catch duplicated rows that still keep distinct counts looking fine.
- *How would a dbt style test express this?* A unique test on the dimension key (a concept; not run here).

**Common mistakes:**
- Papering over it with `SELECT DISTINCT`, which hides the cause and can delete legitimate duplicates.
- Checking only the row count of the final query.
- Joining before checking uniqueness of the lookup table.
- Fixing the query but leaving the bad dimension for the next report.

@@Q41
**Say this first (1 line):** A join is a nested loop, a hash join or a merge join; indexes on the join columns (especially the foreign key side) let the engine look up matches instead of scanning, filters before the join shrink the inputs, functions on join columns hide the column from the index, and a missing `ON` is a Cartesian product; deeper plan reading is Part 11.

**Schema and sample data:** 200 customers (4 cities, an email in mixed case), 2,000 orders (10 per customer), 100 leads with lower-case emails. The Code block creates them with loops; the tables are:
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, email TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
CREATE TABLE leads(lead_id INTEGER PRIMARY KEY, email TEXT);
```

**SQL answer:** the Code block runs `EXPLAIN QUERY PLAN` (SQLite's plan output, enough for concepts; Part 11 is the proper place) on the foreign key join before and after `CREATE INDEX ix_orders_customer ON orders(customer_id)`, on the `LOWER()` join before and after an expression index, and counts the rows of a join with no `ON`. The filter-first comparison uses these two queries, which return the same result:
```sql
SELECT c.city, SUM(o.amount) AS total FROM customers c JOIN orders o ON o.customer_id = c.customer_id
WHERE o.amount >= 25 GROUP BY c.city ORDER BY c.city
```
```sql
SELECT c.city, SUM(o.amount) AS total FROM customers c
JOIN (SELECT customer_id, amount FROM orders WHERE amount >= 25) o ON o.customer_id = c.customer_id
GROUP BY c.city ORDER BY c.city
```

**pandas answer:** filter, then merge (same text as in the Code block):
```py
p = (customers.merge(orders[orders["amount"] >= 25][["customer_id", "amount"]], on="customer_id")
     .groupby("city", as_index=False).agg(total=("amount", "sum")).sort_values("city").reset_index(drop=True))
```

**Example:** the three join algorithms in plain words.
- **Nested loop:** for each row of the outer table, look up matching rows in the inner table. With an index on the inner join column each lookup is cheap; without one, it scans the inner table every time. Good for small outer inputs.
- **Hash join:** build an in-memory hash table on the smaller input, then stream the larger one and probe it. Good for large unsorted inputs and equality joins; needs memory.
- **Merge join:** sort both inputs on the key (or read them already sorted from an index) and walk through them together. Good when both sides are sorted or very large.
- In my run: 200 customers x 2,000 orders with no `ON` gave 400,000 rows.

**Code:** run with `python3 -I`; the SQL variants are compared with each other and with the pandas filter-then-merge result.
{{CODE:q41}}

**Output (my run):**
{{OUT:q41}}

**Edge cases:**
- **What I ran versus what I know:** the plans above are SQLite's. SQLite's plans only show scans and index searches (nested-loop style), which is why I describe hash and merge joins from general knowledge of other engines (PostgreSQL, SQL Server, Oracle, MySQL 8 and others differ in which algorithms exist and when they choose them); not executed here.
- **The planner can change the join order:** before the index SQLite scanned `orders` and looked up each customer by primary key; after the index it scanned the (city filtered) customers and used the index on `orders.customer_id`. The same query got a different plan, which is the point of indexing the foreign key.
- **Primary keys are indexed, foreign keys usually are not** (in most engines a foreign key column does not get an index automatically); the many side (`orders.customer_id`) is where joins and deletes need one.
- **Functions on join columns:** `LOWER(c.email) = LOWER(l.email)` scanned both tables (two `SCAN` lines). An index on the expression `LOWER(email)` let SQLite search customers; engines that support expression or function-based indexes behave similarly, others need a stored normalised column (hedged).
- **Casts and mismatched types** have the same effect as functions on the column (Q35).
- **Small tables:** a full scan can be the best plan; do not index everything.

**Then explain:**
- **Why an index on the foreign key helps:** the join asks "which orders belong to this customer", and without an index on `orders.customer_id` the engine must read all orders for each customer or build a temporary structure.
- **Why filter before the join (when it is safe):** fewer rows go into the join and the aggregation; in an INNER JOIN the optimiser usually pushes the filter down itself, so the written order often does not matter (my run gave the same result both ways; I did not time it). For a LEFT JOIN, moving a filter changes the result (Q3).
- **Fewer columns:** wide rows cost memory in sorts and hash tables; select only what you need.
- **Missing ON:** the result is the Cartesian product, 200 x 2,000 = 400,000 rows here, and pandas `how="cross"` made the same 400,000 rows.
- **Where it goes next:** reading `EXPLAIN`, statistics, join hints and partitioning are Part 11.

**Follow-ups:**
- *When is a hash join better than a nested loop?* When there is no useful index and both inputs are large.
- *What about a composite index?* Put the equality columns first; order matters (concept; Part 11).
- *Does `SELECT *` matter for joins?* Yes: it blocks covering-index plans and moves extra bytes.

**Common mistakes:**
- Indexing the primary key and forgetting the foreign key.
- Wrapping join columns in `LOWER`, `CAST` or `DATE`.
- Joining first, filtering later, on a LEFT JOIN where the filter changes meaning.
- Claiming one join algorithm is always best.

@@Q42
**Say this first (1 line):** `JOIN` returns one row per match, so it duplicates a customer who has several orders; `EXISTS` and `IN` only test for existence and return the customer once; `NOT IN` silently returns nothing if the subquery has a NULL; and `NOT EXISTS` or a `LEFT JOIN ... IS NULL` is the safe "does not exist" form.

**Schema and sample data:**
```sql
{{VAR:q42:SCHEMA}}
```
`orders` has several rows for customer 1 and a NULL customer (guest). `orders_clean` has one row per customer and no NULL.

**SQL answer:** the Code block builds six queries per table with `queries(t)`: `JOIN`, `EXISTS`, `IN`, `NOT EXISTS`, `NOT IN` and `LEFT JOIN IS NULL`. With `t` standing for the table name (`orders` or `orders_clean`), the text in the code is:
```sql
SELECT c.name FROM customers c JOIN {t} o ON o.customer_id = c.customer_id ORDER BY c.customer_id
```
```sql
SELECT c.name FROM customers c WHERE EXISTS (SELECT 1 FROM {t} o WHERE o.customer_id = c.customer_id) ORDER BY c.customer_id
```
```sql
SELECT c.name FROM customers c WHERE c.customer_id NOT IN (SELECT customer_id FROM {t}) ORDER BY c.customer_id
```
The Code block fills `{t}` with an f-string; `NOT EXISTS`, `IN` and `LEFT JOIN IS NULL` follow the same pattern in `queries`.

**pandas answer:** (same text as in the Code block)
```py
p_join = customers.merge(orders, on="customer_id").sort_values(["customer_id", "order_id"])["name"].tolist()
p_in = customers.loc[customers["customer_id"].isin(orders["customer_id"]), "name"].tolist()
p_not = customers.loc[~customers["customer_id"].isin(orders["customer_id"]), "name"].tolist()
```

**Example:** customers Asha (1), Ben (2), Chitra (3), Dev (4); orders 101, 102, 103 belong to Asha, 104 to Ben, 105 has a NULL customer.
- "Customers who ordered": `JOIN` gives Asha, Asha, Asha, Ben (4 rows, one per order). `EXISTS` and `IN` give Asha, Ben.
- "Customers who never ordered": `NOT EXISTS` and `LEFT JOIN ... IS NULL` give Chitra, Dev. `NOT IN` gives nothing, because the subquery contains the NULL from order 105, so `3 NOT IN (1, 2, NULL)` is UNKNOWN, not TRUE.
- Where they agree: in `orders_clean` (one order per customer, no NULL) `JOIN`, `EXISTS` and `IN` all give Asha, Ben, and the three "never ordered" forms all give Chitra, Dev.

**Code:** run with `python3 -I`; the asserts check each claim above and compare the pandas lists with the SQL form named in the label, in `customer_id` order.
{{CODE:q42}}

**Output (my run):**
{{OUT:q42}}

**Edge cases:**
- **JOIN duplicates are a feature when you need columns from orders** (for example the order amount), and a bug when you only need the customer.
- **`IN` with NULL on the positive side is fine** (it can still be TRUE); only `NOT IN` breaks.
- **`SELECT DISTINCT` after a JOIN** fixes the duplicates for existence checks but costs a sort or hash, and it hides fan-out when you also select other columns.
- **Empty subquery:** `NOT IN` returns every customer, `NOT EXISTS` also.
- **pandas:** `~isin` ignores the NULL problem and returns Chitra and Dev (it matches `NOT EXISTS`, not the SQL `NOT IN`), which is why SQL and pandas answers differ in the trap case. NaN in `isin` is covered in Part 1 Q13.

**Then explain:**
- **Rule 1:** if you only need to test whether a related row exists, use `EXISTS` (or `NOT EXISTS`); it is NULL-safe and cannot duplicate rows.
- **Rule 2:** if you need columns from the other table, use a `JOIN`, and make sure you know the grain (one row per match) or aggregate first.
- **Rule 3:** use `IN` when the subquery column is `NOT NULL`, or filter NULLs in it; avoid `NOT IN` unless you can guarantee that.
- **Performance:** the optimiser often turns these into the same semi-join or anti-join plan, but that is engine specific (hedged, not executed); correctness differences matter first.
- **pandas idioms:** `merge` is the JOIN (duplicates included), `isin` or a merge on `drop_duplicates()` keys is the semi-join, `~isin` or `merge(..., indicator=True)` with `left_only` is the anti-join.

**Follow-ups:**
- *Is `EXISTS` slower than `IN`?* Not necessarily; a modern optimiser usually plans both as a semi-join (hedged, engine dependent).
- *What about `<> ALL`?* It is the same as `NOT IN` and has the same NULL problem.
- *How do you return one row per customer with the latest order amount?* That needs a join plus a selection rule (Part 4); `EXISTS` alone cannot return columns.

**Common mistakes:**
- Using `JOIN` for an existence check and then counting customers with `COUNT(*)`.
- Using `NOT IN` against a nullable column.
- Believing the three are always interchangeable.
- Fixing duplicates with `DISTINCT` and not noticing the fan-out in other columns.

@@Q43
**Say this first (1 line):** On SQLite 3.45.1 I ran INNER, LEFT, RIGHT, FULL, CROSS (both spellings), INTERSECT, EXCEPT, USING and NATURAL; MINUS, `<=>` and LATERAL failed there; everything about PostgreSQL, MySQL, Oracle, SQL Server, BigQuery and Snowflake in the table is from memory and not executed.

**Schema and sample data:** `l` has ids 1, 2, 3 and `r` has ids 2, 3, 4, so there are two matches, one left-only row and one right-only row.
```sql
CREATE TABLE l(id INTEGER, v TEXT);
CREATE TABLE r(id INTEGER, w TEXT);
INSERT INTO l VALUES (1,'l1'),(2,'l2'),(3,'l3');
INSERT INTO r VALUES (2,'r2'),(3,'r3'),(4,'r4');
```

**SQL answer:** the queries run in the Code block, with `attempt()` catching errors so a failing feature prints its error instead of stopping the script. The two columns the question asks for:

| Feature | Verified by running on SQLite 3.45.1 | Hedged, not executed |
|---|---|---|
| RIGHT JOIN | works; 3 rows; same rows as the LEFT JOIN with the tables swapped | PostgreSQL, SQL Server, Oracle, MySQL, BigQuery and Snowflake support it, to my knowledge; I believe SQLite added it in 3.39 (from memory; I only ran 3.45.1) |
| FULL OUTER JOIN | works; 4 rows | PostgreSQL, SQL Server, Oracle, BigQuery and Snowflake support it; MySQL has no FULL OUTER JOIN (the MySQL 8.4 join page shows only LEFT and RIGHT) |
| EXCEPT versus MINUS | `EXCEPT` works (returned 1); `MINUS` gave a syntax error | Oracle uses `MINUS` (older versions have no `EXCEPT`, as I recall); PostgreSQL, SQL Server, BigQuery and Snowflake use `EXCEPT` (Snowflake also accepts `MINUS`) |
| INTERSECT | works (returned 2 and 3) | MySQL support depends on version (added in 8.0.31 from memory; check your version) |
| USING | `SELECT *` returned `id, v, w` (one `id`); also worked with RIGHT and FULL JOIN | PostgreSQL and MySQL support it, with differences in how a qualified `l.id` behaves after an outer join; SQL Server does not support USING; check each manual |
| NATURAL JOIN | worked, same columns as USING (`id, v, w`) | supported in PostgreSQL, MySQL, Oracle and others (not SQL Server); it joins on all same-named columns (Q21) |
| Joined-column output order | ON: `id, v, id, w` (both keys, left columns then right); USING and NATURAL: the shared key first, then the rest | the standard puts the USING/NATURAL columns first; MySQL's join page documents the same coalesced order; I did not run MySQL |
| Cross join syntax | `CROSS JOIN` and the comma form both gave 9 rows | both are standard SQL and accepted widely; some engines or modes treat a comma join differently with precedence against explicit JOINs (hedged) |
| LATERAL | `LATERAL` gave a syntax error in SQLite | PostgreSQL, MySQL 8.0.14 and later and Snowflake support `LATERAL` (SQL Server uses `CROSS APPLY`); the lateral idea is not covered here |
| Null-safe equality | `IS NOT DISTINCT FROM` worked (returned 1) and `NULL IS NULL` returned 1; `<=>` gave a syntax error | PostgreSQL has `IS NOT DISTINCT FROM`; MySQL has `<=>`; others vary |

**pandas answer:** the parallels, run in the same Code block and compared by row count against the SQL result:
```py
l.merge(r, on="id", how="inner")
l.merge(r, on="id", how="outer")
l.merge(r, how="cross")
```
`how="right"` and `how="left"` map to the RIGHT and LEFT joins, `how="cross"` is CROSS JOIN, `on="id"` returns one key column like USING, and `left_on`/`right_on` returns both columns like ON. pandas has no NATURAL join (and `merge` with no `on` joins on all common column names by default, which is the same trap as NATURAL JOIN).

**Example:** by hand, INNER gives ids 2 and 3 (2 rows); LEFT adds id 1 (3 rows); RIGHT adds id 4 instead (3 rows); FULL has both unmatched rows (4 rows); CROSS is 3 x 3 = 9 rows. `l INTERSECT r` gives 2 and 3, and `l EXCEPT r` gives 1.

**Code:** run with `python3 -I`; it asserts the SQLite row counts equal the pandas counts, that RIGHT JOIN equals the swapped LEFT JOIN, and that INTERSECT and EXCEPT equal Python set operations on the ids.
{{CODE:q43}}

**Output (my run):**
{{OUT:q43}}

**Edge cases:**
- **Qualified key after a FULL JOIN with USING:** in my run `SELECT l.id, r.id ... FULL JOIN ... USING (id)` returned the left and right keys separately, with NULLs on the unmatched side, while `SELECT id` (or `*`) returned the coalesced value. Use the unqualified name.
- **MINUS error message:** SQLite parsed `MINUS` as an alias, so the error is a confusing `near "SELECT": syntax error`.
- **Set operators and NULLs:** `INTERSECT` and `EXCEPT` treat NULLs as equal and remove duplicates (Q29).
- **pandas:** `merge` without `on` uses every common column name, so it behaves like NATURAL JOIN unless you pass `on`.

**Then explain:**
- **Portable subset:** `INNER JOIN`, `LEFT JOIN`, `CROSS JOIN` and `ON` work everywhere; for FULL JOIN emulate with `LEFT JOIN ... UNION ALL` plus an anti-join (Q32) when the engine lacks it.
- **Where I am sure and where not:** what is in the left result column was executed; the right column is from general knowledge and manuals as I remember them, and versions matter (MySQL INTERSECT and EXCEPT, SQLite RIGHT and FULL JOIN). Always check the engine's current documentation.
- **Lateral:** the idea (a subquery in FROM that can see columns of earlier FROM items) is outside this part; SQLite does not have it.

**Follow-ups:**
- *Why avoid RIGHT JOIN?* Swap the tables and use LEFT JOIN; readers think left to right.
- *How do you port a FULL JOIN to MySQL?* LEFT JOIN, then `UNION ALL` the right-only rows via an anti-join (Q32).
- *Does `UNION` behave like `INTERSECT` on NULL?* Both treat NULLs as equal for de-duplication (Q29).

**Common mistakes:**
- Assuming every engine supports FULL JOIN, USING or INTERSECT.
- Assuming `SELECT *` from a USING join gives two key columns.
- Using NATURAL JOIN in shared code.
- Writing `MINUS` in an engine that expects `EXCEPT`.

@@Q44
**Say this first (1 line):** Aggregate the payments to one row per order first, then LEFT JOIN that to orders and classify with a CASE, because joining orders straight to payments repeats each order once per payment and inflates every order total; list orphan payments with a separate anti-join on the payments side.

**Schema and sample data:**
```sql
{{VAR:q44:SCHEMA}}
```

**SQL answer:** the Code block holds `SQL_MAIN` (status per order), `SQL_ORPHANS`, `SQL_WRONG` (the fan-out bug) and `SQL_FULL` (the one-pass FULL JOIN structure).
```sql
{{VAR:q44:SQL_MAIN}}
```
```sql
{{VAR:q44:SQL_ORPHANS}}
```
`SQL_FULL` does both in one statement: a FULL JOIN of orders to the aggregated payments, with `COALESCE(o.order_id, p.order_id)` as the key and a status of `orphan` when the order side is missing. Its limit: the payments aggregate has one row per `order_id`, so all payments with a NULL `order_id` collapse into one row (25 here) and you lose the payment-level detail, which is why I use the anti-join for the orphan list.

**pandas answer:** (same text as in the Code block)
```py
paid = payments.groupby("order_id", as_index=False).agg(paid=("paid_amount", "sum"))     # NaN order_id group is dropped by default
m = orders.merge(paid, on="order_id", how="left", validate="one_to_one")
chk = payments.merge(orders[["order_id"]], on="order_id", how="left", indicator=True)
```
The Code block then fills the missing paid values with 0, sets the status with four `loc` assignments (default overpaid, then paid, partial and unpaid overwrite it), and builds the orphan list from the `left_only` rows of `chk`.

**Example:** orders 1 to 5 have amounts 100, 200, 50, 80, 120.
- Order 1: one payment of 100, so paid 100 = amount, status paid.
- Order 2: payments 120 and 50, so 170 < 200, partial.
- Order 3: payment 60 > 50, overpaid.
- Order 4: no payment, paid 0, unpaid (the aggregate has no row, so `p.paid IS NULL`).
- Order 5: payments 70 and 50 sum to 120 = amount, paid (two payments, one order).
- Orphans: payment 7 (order 99 does not exist) and payment 8 (NULL order id).
- Tie-out: all payments 515 = matched 450 (100 + 170 + 60 + 0 + 120) + orphan 65 (40 + 25).
- The fan-out bug: summing `o.amount` after joining directly to payments gave 790 against a true order total of 550, because orders 2 and 5 are counted twice.

**Code:** run with `python3 -I`; the status table is compared sorted by `order_id`, the orphan list sorted by `payment_id`, and the tie-out is asserted in both SQL and pandas.
{{CODE:q44}}

**Output (my run):**
{{OUT:q44}}

**Edge cases:**
- **Status boundaries:** equality on integers is safe; on money stored as floats compare with a rounded difference (`ABS(paid - amount) < 0.005`) or store cents as integers. My toy data uses integers.
- **NULL `order_id` payments:** an INNER or LEFT join to orders never matches a NULL key, so they are orphans in the anti-join. The pandas `groupby` dropped the NaN group by default, so the grouped total (490) was 25 short of the 515 total; the orphan list built from the raw payments is what restores the tie-out.
- **Zero-amount or negative payments (refunds):** `SUM` nets them, so an order can be partial after a refund; decide if refunds belong here.
- **Order with amount 0 and no payment:** status unpaid by my CASE (since `paid IS NULL`), though arguably paid; define the rule.
- **Duplicate payment rows (same payment loaded twice):** the sum doubles; check `payment_id` uniqueness first.
- **pandas dtype:** `payments.order_id` came back `float64` because of the NULL, which is harmless for the merge (see Q35).

**Then explain:**
- **Why aggregate first:** the merge between orders and payments is one-to-many; aggregating payments to one row per `order_id` makes it one-to-one, which `validate="one_to_one"` proves in pandas.
- **Structure:** LEFT JOIN from orders answers "what is the status of every order"; the anti-join from payments answers "which payments have no order". A FULL JOIN can do both, at the cost of losing payment-level detail for NULL-key orphans.
- **Tie-out as a test:** total payments must equal matched plus orphan payments; assert it, because a mismatch means a dropped NULL group or a double count.
- **Status rules written down:** unpaid (no payments), partial (0 < paid < amount), paid (equal), overpaid (greater). State what you do for an amount of 0.

**Follow-ups:**
- *What if a payment can reference several orders?* Then you need an allocation table; the join becomes many-to-many (Q45).
- *How do you find which payment caused the overpayment?* That needs a running total ordered by date (Part 5, windows).
- *How would you monitor this daily?* Run the tie-out as a scheduled check and alert if orphan totals grow (a concept, not run).

**Common mistakes:**
- Joining payments directly and summing order amounts.
- Using an INNER JOIN and losing unpaid orders.
- Writing the status CASE in the wrong order, so overpaid is tested after paid with `>=`.
- Ignoring NULL `order_id` payments and finding the totals do not tie.

@@Q45
**Say this first (1 line):** First de-duplicate the promo rows to one row per (code, customer), then choose and state a policy because a customer's orders belong to several codes: count the full order in each code (overlapping, does not add up to total revenue), split each order equally across the customer's codes, or pick one code per customer (both tie to the order total); check that the totals tie in every policy.

**Schema and sample data:**
```sql
{{VAR:q45:SCHEMA}}
```
Customer 1 has `SAVE10` (loaded twice) and `VIP`; customer 2 has `SAVE10`; customer 3 has `VIP` and `FEST`; customer 4 has no code.

**SQL answer:** the Code block holds `SQL_NAIVE` and the three policies `SQL_ONCE`, `SQL_SPLIT` and `SQL_PICK`; `DEDUP` is the derived table `(SELECT DISTINCT code, customer_id FROM promo_codes)` used by the first two (an f-string in the code, so I describe it instead of pasting the rendered text).
```sql
{{VAR:q45:SQL_NAIVE}}
```
```sql
{{VAR:q45:SQL_PICK}}
```
`SQL_ONCE` is the naive query with `promo_codes` replaced by `DEDUP`. `SQL_SPLIT` joins `DEDUP` to a per-customer count of codes (`COUNT(*) ... GROUP BY customer_id` over `DEDUP`) and sums `o.amount * 1.0 / n.n_codes`. `SQL_PICK` takes `MIN(code)` per customer as the chosen code; "alphabetically first" is only a placeholder rule, so use a business rule (first used, highest priority) in real work.

**pandas answer:** (same text as in the Code block)
```py
pd_dedup = promo.drop_duplicates()
once = orders.merge(pd_dedup, on="customer_id", validate="many_to_many")          # many-to-many on purpose, after de-duplication
p_once = once.groupby("code")["amount"].sum()
pick = promo.groupby("customer_id", as_index=False).agg(code=("code", "min"))
pk = orders.merge(pick, on="customer_id", validate="many_to_one")
```
The split policy merges `once` with the per-customer code counts and sums `amount / n_codes` per code.

**Example:** orders: customer 1 has 100 and 50 (150), customer 2 has 80, customer 3 has 60 and 40 (100), customer 4 has 30. Total 360; orders of customers who hold a code: 330.
- Naive join (duplicates not removed): SAVE10 380, VIP 250, FEST 100, sum 730 against 330 for customers with a code: customer 1's duplicate SAVE10 row doubles 150, and the overlaps add more.
- Once per code: SAVE10 = 150 + 80 = 230, VIP = 150 + 100 = 250, FEST = 100; sum 580. It is 250 more than 330 because customer 1 (150) and customer 3 (100) sit in two codes each. This is right for "revenue touched by each code" but the codes must not be added up.
- Split equally: SAVE10 = 75 + 80 = 155, VIP = 75 + 50 = 125, FEST = 50; sum 330, which ties.
- Pick one (the alphabetically first code): customer 1 gets SAVE10, customer 2 SAVE10, customer 3 FEST; SAVE10 230, FEST 100, VIP has nothing; sum 330, which ties.
- Customer 4 (30) has no code and sits outside all policies; 330 + 30 = 360.

**Code:** run with `python3 -I`; each policy is compared between SQL and pandas as a code-to-revenue mapping, and the tie-out is asserted.
{{CODE:q45}}

**Output (my run):**
{{OUT:q45}}

**Edge cases:**
- **Duplicate promo rows:** one duplicate (`SAVE10`, customer 1) doubled that customer's orders in the naive query; fix it with `DISTINCT` or a unique constraint on `(code, customer_id)`.
- **Customers without a code:** an INNER JOIN drops them, so the totals do not reach 360; add a "no code" bucket with a LEFT JOIN if you need the grand total to tie.
- **Customer with codes but no orders:** contributes nothing; use a LEFT JOIN from codes if you want codes with 0 revenue to appear.
- **Float rounding in the split:** 1.0 multiplication keeps decimals, so sums can differ in the last digit; round at the end or store cents (my data splits cleanly).
- **Time:** a code may apply only to orders after it was issued; this table has no dates, so the example ignores that, but in real data the join needs a date condition.
- **pandas `validate`:** `many_to_one` on the promo side raised `MergeError`, which is exactly what you want to see before deduplicating; `many_to_many` is accepted but checks nothing, so I use it only after the dedupe, on purpose.

**Then explain:**
- **Why it fans out:** orders and promo codes are both many per customer, so joining them on `customer_id` is many-to-many: every order is repeated once per code row (and once more per duplicate row).
- **Policy choice:** the join cannot decide for you. Count in each code (marketing wants "revenue influenced"), split (finance wants totals that add up), or pick one (a rule such as last touch or priority). Say which one you used next to the number.
- **Tie-out:** split and pick must sum to the revenue of customers with a code (330), and plus the no-code bucket to the order total (360); once-per-code must exceed it by the overlap (580 against 330 here).
- **Order of operations:** de-duplicate, decide allocation, then join and group; never aggregate after a many-to-many join without knowing the policy.
- **True attribution:** a promo is normally attached to the order (an `order_promos` table), not the customer; if you have that, join on `order_id` and the fan-out shrinks (a design point, not run).

**Follow-ups:**
- *What if one order really uses two codes?* Then the grain is (order, code) and you split by a rule or weight; the check is still that the allocated amounts sum to the order amount.
- *How do you show the overlap?* Count orders in more than one code (a `COUNT(DISTINCT code)` per customer greater than 1).
- *Can `COUNT(DISTINCT order_id)` fix this?* It would fix a count of orders per code, but not a `SUM` (Q13).

**Common mistakes:**
- Summing revenue across codes and presenting it as the total.
- Leaving duplicate promo rows in the join.
- Not saying which allocation policy was used.
- Using `SUM(DISTINCT amount)`, which drops legitimate equal amounts.

