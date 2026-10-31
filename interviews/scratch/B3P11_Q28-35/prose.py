P[28] = r'''
**Say this first (1 line):** Load fewer columns, give low-cardinality text a `category` dtype and numbers the smallest safe integer or float type, and read big files in chunks of decomposable aggregates; the price is overflow and precision risks you must check, and categoricals only pay off when there are far fewer distinct values than rows.

**Schema and sample data:** the pandas frame has `id`, `city` (20 distinct strings), `status` (4 values), `score` (int 0 to 100), `amount` (float) and `ts` (timestamp), 500,000 rows from `np.random.default_rng(28)`. The same data goes into SQLite as `t` for the cross-check, and a 6-row mini file for the hand walk-through:
```sql
CREATE TABLE t(id INTEGER, city TEXT, status TEXT, score INTEGER, amount REAL, ts TEXT);
-- mini example (written to a CSV in the run): city, amount
-- Pune 10, Delhi 20, Pune 30 | Pune 40, Delhi 50, Agra 60
```

**SQL answer:** the aggregation that the chunked pandas loop must reproduce (same text as `sql` in the Code block):
```sql
SELECT status, city, ROUND(SUM(amount), 2) AS sum, COUNT(*) AS count
FROM t GROUP BY status, city ORDER BY status, city
```
SQL has no memory-layout knobs of this kind in SQLite; the closest ideas are declared column types and reading only the columns you SELECT. Other engines' column types and columnar compression are not executed here.

**pandas answer:** the loading recipe is the `lean = pd.read_csv(path, usecols=[...], dtype={...}, parse_dates=["ts"])` call and the chunk loop in the Code block:
```py
for chunk in pd.read_csv(path, usecols=["city", "status", "amount"], dtype={"city": "category", "status": "category"},
                         chunksize=100_000):
    parts.append(chunk.groupby(["status", "city"], observed=True)["amount"].agg(["sum", "count"]))
```
Downcasting is `pd.to_numeric(s, downcast="unsigned")` or `"float"`, and `astype("category")` for the two text columns. Only sums and counts are combined across chunks; a mean is rebuilt as sum divided by count, and a distinct count cannot be combined this way.

**Example:** the mini file has six rows read with `chunksize=3`. Chunk 0 is Pune 10, Delhi 20, Pune 30, so its partial result is Delhi (sum 20, count 1) and Pune (sum 40, count 2). Chunk 1 is Pune 40, Delhi 50, Agra 60, giving Agra (60, 1), Delhi (50, 1), Pune (40, 1). Adding the partials by city gives Agra (60, 1), Delhi (70, 2), Pune (80, 3), the same as grouping all six rows at once. As a category the city column holds the sorted categories Agra, Delhi, Pune and the codes 2, 1, 2, 2, 1, 0, so each row costs one small integer instead of its own string.

**Code:** run with `python3 -I`.
{{CODE}}

**Output (my run):**
{{OUT}}

Reading the output: the two text columns were 28,000,000 and 27,249,606 bytes (the default `str` dtype in pandas 3.0.5, measured with `deep=True`) and became 501,120 and 500,218 bytes as categories (500,000 one-byte codes plus the 20 or 4 labels). Whole-frame memory went from 71,249,606 to 9,501,338 bytes, a ratio of 0.13. The `ts` column did not change. For 500,000 unique strings the category was larger (31,888,890 bytes against 29,888,890 for `str`), because it stores the codes and every label. The lean read used five columns and no `id`, so its 7,502,066 bytes against 101,249,606 for the plain read is not a like-for-like dtype comparison, it is dtypes plus fewer columns (the plain read also left `ts` as strings). The CSV itself was 25,293,568 bytes. The chunked groupby over 5 chunks gave 80 groups that equal the SQL result.

**Edge cases:**
- Overflow wraps silently: `np.array([100, 200, 300, 70000]).astype(np.int8)` gave `[100, -56, 44, 112]`. In this run (pandas 3.0.5) `pd.Series([100, 300]).astype("int8")` also returned `[100, 44]` with no error, so do not rely on `astype` to protect you. `pd.to_numeric(..., downcast=...)` chooses a type that fits the data it sees (int16 for `[100, 300]`, uint8 for `[100, 200]`), but a later batch with bigger values can still overflow a column you fixed at uint8.
- float32 loses precision: 16,777,217 became 16,777,216, `0.1 + 0.2` in float32 printed 0.30000001192092896, 480,164 of the 500,000 two-decimal amounts changed when round-tripped through float32, and the column sum moved from 50001499.66 (float64) to 50001504.00 (float32). Money columns should stay float64 or integer cents.
- Categories and missing values: NaN is not a category, it is code -1. A new value not in the categories cannot be assigned until you add the category.
- High cardinality: a category of 500,000 unique strings was bigger than the plain strings (see Output).
- Chunk boundaries: a group can span chunks, which is why partials are re-aggregated; the categories seen per chunk can differ, which is why the code casts to `str` before comparing with SQL.

**Then explain:**
- Why categoricals shrink low-cardinality text: the strings are stored once in the category index and each row holds a small integer code (int8 here for 20 categories), so memory is roughly rows times code size plus the labels.
- When they do not: when distinct values approach the row count, the codes plus the full label table cost more than the strings (shown above). They also help `groupby` and comparisons only while you stay in category land; converting back with `astype(str)` pays the cost again.
- `groupby` on a categorical, checked in pandas 3.0.5: with categories ordered c, b, a and data b, a, b, the default result was b = 4, a = 2: unobserved category c is dropped (the default is `observed=True` in this version) and `sort=True` follows the category order (b, then a), not alphabetical order. `observed=False` adds c with 0. `sort=False` on observed categories gave b then a. A plain string column sorted alphabetically (a, b), and with `sort=False` gave first-appearance order (b, a). Older pandas defaulted to `observed=False`, so pass it explicitly in code that must run on both.
- The pandas 'Scaling to large datasets' guide, for the ideas only: load less data (columns), use more efficient dtypes, and process in chunks. I use none of its numbers.
- Time zones and dates: `parse_dates` gives `datetime64` and is far smaller than leaving timestamps as text.

**Follow-ups:**
- What if the aggregate is a median or a distinct count across chunks? (Not decomposable: use a two-pass approach, a database, or an approximate sketch; not run here.)
- Parquet or another columnar format would store the same columns compressed and read only the columns asked for (not executed here, not benchmarked).
- When is `pyarrow`-backed `string[pyarrow]` an alternative? (Not tested here: pyarrow was not used in this run.)

**Common mistakes:**
- Quoting memory with `memory_usage()` without `deep=True`: for text it counts only pointers, not the strings.
- Downcasting before the data range is known, or downcasting money to float32.
- Using `category` on an id-like column.
- Forgetting `observed` and `sort` on categorical groupbys and being surprised by dropped or reordered groups.
- Summing means across chunks instead of sums and counts.
'''

P[29] = r'''
**Say this first (1 line):** Measure first (plan and VM steps), then change one thing at a time and re-check the result, because the fan-out through `order_items` both wastes work and makes the revenue wrong, while the index and date fixes only change cost.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT, segment TEXT);       -- 20,000 rows
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT, amount REAL);  -- 300,000 rows
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, qty INTEGER, price REAL); -- 900,000 rows
-- mini example used for the hand walk (run in the Code block):
-- orders: (1,c1,2026-06-10,delivered,100) (2,c1,2026-06-20,delivered,50) (3,c2,2026-03-01,delivered,70) (4,c2,2026-06-25,placed,999)
-- items: order 1 has 3 items, order 2 has 1, order 3 has 2, order 4 has none; both customers are in Pune
```
The big data is seeded (`default_rng(29)`): 40 cities, dates 2024-11-01 to 2026-10-31, about 60% of orders delivered, "last 6 months" anchored at 2026-05-01 so the run is repeatable.

**SQL answer:** the final query is `S5` in the Code block (the earlier steps are the variants `S0` to `S4a`, `S6`); it needs the index `ix_ord_cov ON orders(status, order_date, customer_id, amount)`:
```sql
{{S5}}
```
Revenue is `SUM(orders.amount)` over delivered orders; distinct customers per city and month is `COUNT(DISTINCT customer_id)`; the 10 cities are the top by six-month revenue.

**pandas answer:** the expected result in the Code block:
```py
o = orders[(orders.status == "delivered") & (orders.order_date >= CUT)].merge(cust[["customer_id", "city"]], on="customer_id")
o["month"] = o["order_date"].str[:7]
cm = o.groupby(["city", "month"]).agg(revenue=("amount", "sum"), customers=("customer_id", "nunique")).reset_index()
top = cm.groupby("city")["revenue"].sum().nlargest(10).index
exp = cm[cm.city.isin(top)].sort_values(["city", "month"]).reset_index(drop=True)
```

**Example:** in the mini data, the order-items join repeats each order once per item: order 1 (amount 100, three items) counts three times and order 2 (amount 50, one item) once, so the join gives June revenue 300 + 50 = 350 where the truth is 100 + 50 = 150. The distinct customer count is 1 in both. Order 3 is outside the six-month window and order 4 is not delivered. (The run prints 350.0 with the join and 150.0 without it.) On the big data the same effect inflated each city-month revenue by about 2.8 to 3.0 times (3 items per order on average) and, because orders with no items disappear in an inner join (14,971 of 300,000), it also changed the top-10 set.

**Code:** run with `python3 -I`. VM steps are counted with `set_progress_handler(cb, 1)`; seconds are one run each, machine-specific.
{{CODE}}

**Output (my run):**
{{OUT}}

VM steps by step: S0 baseline 9,512,523; S1 sargable date 8,972,842; S2 plus index on `order_items(order_id)` 4,835,519; S3 drop the unused join 2,479,765; S4a wide `SELECT` inside a CTE 2,479,765 (no change); S5 covering index 1,311,137; S6 pre-aggregation 2,415,360 (worse than S5). Final results S3, S4a, S5 and S6 equal the pandas frame (60 rows: 10 cities times 6 months, compared after sorting by city and month); S0 does not.

**Edge cases:**
- The baseline's wrong answer is silent: it returns 60 plausible rows with inflated revenue and a different top-10 set, so fix correctness (the fan-out) before arguing about speed.
- Tied revenue at the 10th city would make the top 10 ambiguous; with random amounts there are no ties here, and a real report needs a tie-breaker column in the sort.
- `COUNT(DISTINCT customer_id)` per month is not additive across months: a customer in two months counts twice if you sum the months.
- A city with no delivered orders in the window simply has no rows; a calendar of all six months per city would need a join to a months table.
- The comparison `order_date >= '2026-05-01'` works on ISO text dates only because that format sorts as text; a different string format would break it.

**Then explain:**
- The loop: (1) baseline, record the plan, VM steps or time, and the result; (2) read the plan for scans, sorts, temp b-trees, join order; (3) change one thing; (4) re-measure; (5) re-check that the result is unchanged (or, for a bug like the fan-out, that it now matches an independent computation). Stop when the remaining cost is not where the time goes.
- What each step showed here, in order. `strftime` on the date column (S1): replacing it with a range on the raw column saved little (9.5M to 9.0M steps) because there was no index on `order_date` to unlock; the rewrite matters once an index exists. Missing foreign-key index (S2): the plan changed from `SCAN i` driving the join to `SCAN o` with an index probe `SEARCH i USING COVERING INDEX ix_items_order`, roughly halving the steps. Fan-out (S3): removing the unneeded `order_items` join halved the steps again and fixed the revenue. Unused columns (S4a): SQLite flattened the CTE and the step count did not change; in a row store that ships wide rows to a client or in a columnar engine the effect can differ, not run here. Covering index (S5): the plan became `SEARCH o USING COVERING INDEX ix_ord_cov (status=? AND order_date>?)`, the lowest count. Pre-aggregation (S6): per customer and month first, then join `customers`, was slightly worse than S5 in this engine at this size (2,415,360 against 1,311,137 steps), because the extra materialisation outweighed the cheaper join; it can win when the join side is much larger. Sort for the top-N: every plan still shows `USE TEMP B-TREE FOR ORDER BY`, but it sorts about 240 city-month rows, so it is not the cost; I did not try to remove it.
- This SQLite run does not reproduce 2 seconds versus 40 seconds: the baseline took about a second here. The loop transfers; the numbers do not.
- What to ask in a real system: table sizes and growth rate (what changed since last year), existing indexes and statistics freshness, the engine and version and its plan tool, how often the report runs and what runs concurrently, whether the date column is a real date type, and whether an exact answer is needed (a pre-computed summary table or materialised view may be the right fix; not executed here).
- Other engines (not executed here): the plan tools differ (PostgreSQL `EXPLAIN (ANALYZE, BUFFERS)`, MySQL `EXPLAIN`, SQL Server plans); the sargability and fan-out points carry over, the exact plan shapes do not.

**Follow-ups:**
- What if the table also needs `ANALYZE`? (Statistics can change the join order; I did not test it on this dataset.)
- How would you keep the report fast as data grows? (Summary table or incremental aggregation, partitioning by date; see Q32.)
- How do you prove the fix did not change results? (Assert against an independent computation, as done here.)

**Common mistakes:**
- Adding indexes first and never reading the plan.
- Fixing the speed of a query that returns the wrong revenue.
- Changing three things at once, so nothing is attributable.
- Trusting one wall-clock timing instead of repeating it or using a deterministic counter.
- Joining a child table "just in case" and aggregating a parent column.
'''

P[30] = r'''
**Say this first (1 line):** At 500,000 rows most of these choices differ by milliseconds, so choose by correctness and clarity (map for one lookup column, observed and sort stated explicitly, `.loc` for writes, `nlargest` for top-k) and keep the speed arguments for when sizes are much larger.

**Schema and sample data:**
```sql
-- the SQL cross-check in the run: t(key INTEGER, cat TEXT, value REAL) with 500,000 rows and lk(key INTEGER, label TEXT) with 1,000 rows
-- mini example for the hand walk: df = key 1,2,1 ; lookup = (1,'x'), (2,'y')
```
pandas: `df` has `key` (0 to 999), `cat` (category: a, b, c, d) and `value` (float), seeded with `default_rng(30)`; `lookup` has 1,000 rows.

**SQL answer:** the SQL equivalents of the merge and the groupby are checked in the Code block:
```sql
SELECT t.key, lk.label FROM t LEFT JOIN lk ON lk.key = t.key
SELECT key, SUM(value) AS v FROM t GROUP BY key ORDER BY key
```
(SQL has no `query`/`eval`/`map` distinction; the engine plans the join and group itself.)

**pandas answer:** the comparisons are in the Code block. Core forms:
```py
df.merge(lookup, on="key", how="left")
df["key"].map(lookup.set_index("key")["label"])
df.groupby("key", sort=False)["value"].sum()
df.query("value > 0.5 and key < 500")
df.nlargest(10, "value")
d.loc[d.a > 0, "b"] = 1
```

**Example:** with `df.key = [1, 2, 1]` and a lookup of 1 to x and 2 to y, both `merge(how='left')` and `map` give x, y, x in the original row order. If the lookup had two rows for key 1, `merge` would return four rows (the extra row is silently added) and `map` would raise an error (`InvalidIndexError` in my run, because the mapping index is not unique), which is the practical difference. For the chained assignment, `d = {a: [-1, 2, 3], b: [0, 0, 0]}`: `d[d.a > 0]['b'] = 1` writes to a temporary copy, so `b` stays `[0, 0, 0]`; `d.loc[d.a > 0, 'b'] = 1` gives `[0, 1, 1]`.

**Code:** run with `python3 -I`. Timings are the median of 5 timed repeats after one warm-up call, machine-specific, and noisy at the millisecond level.
{{CODE}}

**Output (my run):**
{{OUT}}

**Edge cases:**
- Merge duplicates: a duplicate key in the lookup adds 513 rows to the result (500,000 rows over 1,000 keys, one duplicated key) while `map` raises. Missing keys give NaN in both.
- `groupby(sort=False)` returns groups in first-appearance order; the values equal the sorted result after `sort_index()` (asserted). In my run the two timings were about equal at 1,000 groups, so sorting 1,000 labels is not the cost.
- Categorical groupby in pandas 3.0.5: the default equals `observed=True`; `observed=False` only adds rows for unused categories (a zero row for an added category). In my run `observed=False` was faster than `observed=True` on a four-value category (2.66 against 5.90 ms), which I did not investigate; I would not choose between them on speed, choose on whether you need the empty groups.
- `query` and `eval` need the columns to be valid names and are strings, so refactoring tools cannot see them; both gave the same rows as the mask (asserted). Their documented purpose (the pandas 'Enhancing performance' guide, opened) is large frames: it gives roughly 100,000 rows as the size where `eval` starts to help. I did not reproduce that gain: at 500,000 rows my run had the mask at 3.17 ms against `query` 5.77 ms, and `eval('value * 2 + key')` at 3.42 ms against 1.82 ms for plain operators. numexpr is not installed here, so `eval` and `query` ran without that accelerator; the 100,000-row guidance assumes it is available, which may explain why I saw no gain.
- Alignment: `x + y` with a shuffled copy of the same labels aligned by label (correct, slower), the positional numpy add paired the wrong rows (results differ, asserted). With duplicate or missing labels alignment adds NaN or errors.
- `nlargest(10, "value")` with ties keeps the first by default (`keep="first"`), while `sort_values().head()` ties follow the sort's stability; the top values matched here (asserted).

**Then explain:**
- Merge versus map: `map` suits one lookup column with a unique key and returned the same labels in my run, faster here (8.50 against 29.74 ms); `merge` is for several columns or non-unique keys, and the row count change is the risk.
- `sort=True` versus `False`: use `sort=False` when order does not matter and the group count is large; keep `sort=True` when downstream code expects sorted keys.
- `nlargest(k)` avoids a full sort (6.21 against 28.97 ms here); for small k on big data it is the clearer choice.
- Which differences matter at which size: below about 100,000 rows none of the timings matter; at 500,000 rows the visible ones were map versus merge, nlargest versus full sort, and avoiding a string conversion before grouping (the groupby after a string conversion was several times slower than the category groupby in my run); the `query`, `eval` and sort choices were within a few milliseconds. At tens of millions of rows the algorithmic ones (sort versus partial sort, merge versus map memory) are the ones to revisit; I did not run that size.
- Chained assignment under pandas 3.0.5 copy-on-write: `d[d.a > 0]['b'] = 1` leaves `d` unchanged (`b` is still `[0, 0, 0]`) and emits a `ChainedAssignmentError` warning whose text says such chained assignment never works to update the original object. The `.loc` form updates the original (`[0, 1, 1]`). Writing to a filtered frame that you keep a name for changes only that copy. Earlier pandas versions sometimes updated the original and sometimes warned; that history is not run here.

**Follow-ups:**
- When would you use `merge_asof` or an index join instead? (Not run here.)
- How would `pd.Categorical` on `key` change the merge? (Not tested.)
- What changes at 50 million rows? (Memory first; consider a database or chunks, see Q28.)

**Common mistakes:**
- Treating a millisecond timing on one run as a real difference.
- A `merge` that silently multiplies rows because of a duplicate lookup key.
- Relying on `groupby` order when `sort=False`.
- Chained indexing for writes, which does nothing under copy-on-write.
- Assuming `query` is always faster than a boolean mask (it was slower at 500,000 rows here).
'''

P[31] = r'''
**Say this first (1 line):** A WITHOUT ROWID table stores the rows inside the primary-key b-tree (SQLite's clustered-index form), which here halved the file for a composite text key with small rows, but it does not help a lookup on a non-leading key column, and deleting rows does not shrink the file until `VACUUM`.

**Schema and sample data:**
```sql
CREATE TABLE kv(a TEXT, b INTEGER, c TEXT, PRIMARY KEY (a, b));                 -- rowid table
CREATE TABLE kv(a TEXT, b INTEGER, c TEXT, PRIMARY KEY (a, b)) WITHOUT ROWID;   -- clustered by (a, b)
-- 100,000 seeded rows: a is one of 2,000 text keys, b = 0 to 99,999 (unique), c is a 3-character text
```

**SQL answer:** the statements run in the Code block (the same text is used for both layouts):
```sql
SELECT c FROM kv WHERE a = 'key_0007' AND b = 12345
SELECT c FROM kv WHERE b = 12345
SELECT name, COUNT(*), SUM(pgsize) FROM dbstat WHERE name IN ('kv') OR name LIKE 'sqlite_autoindex%' GROUP BY name
DELETE FROM kv WHERE b % 2 = 1
VACUUM
```

**pandas answer:** pandas holds the same rows and answers the lookups by boolean mask; the Code block asserts both layouts return what pandas finds:
```py
exp = sorted(data.loc[mask, "c"])
```

**Example:** the rowid table keeps two b-trees: the table itself (580 pages) and the automatic index `sqlite_autoindex_kv_1` on (a, b) (548 pages), plus one header page, which is the 1,129 pages printed. The WITHOUT ROWID table has one b-tree of 564 pages plus the header, 565 pages: the key columns are stored once. A lookup on `a` and `b` therefore searches the index and then fetches the row by rowid in the first layout (`USING INDEX sqlite_autoindex_kv_1`) and goes straight to the row in the second (`USING PRIMARY KEY`).

**Code:** run with `python3 -I`.
{{CODE}}

**Output (my run):**
{{OUT}}

**Edge cases:**
- A lookup on `b` alone is `SCAN kv` in both layouts: `b` is not the leftmost column of the key, so neither b-tree can seek on it (queries on a trailing key column need their own index).
- Large rows: with a 300-byte `c` (20,000 rows) the WITHOUT ROWID table used more pages than the rowid table (1,916 against 1,773). That is the documented guidance showing up: WITHOUT ROWID suits small rows, because wide rows inside the key b-tree reduce how many keys fit per page, and the docs' rule of thumb is that rows over about one-twentieth of a page (about 200 bytes at 4,096) tend to do worse. I read this from the docs and checked the direction with one run, not the exact threshold.
- `DELETE` of half the rows left `page_count` unchanged (1,129 and 565) with only 21 and 29 free pages, because the pages are half empty, not free. `PRAGMA auto_vacuum` was 0 (NONE): with that default the file never shrinks by itself; with other `auto_vacuum` settings free pages can be released at commit (documented, not run here, and it does not defragment half-empty pages).
- After `VACUUM` the files shrank to 543 and 257 pages (2,224,128 and 1,052,672 bytes), freelist 0. `VACUUM` rewrites the whole file, needs temporary disk space and an exclusive lock, so it is a maintenance operation.
- A single `INTEGER PRIMARY KEY` is already the rowid, so WITHOUT ROWID adds nothing there (docs); do not add `AUTOINCREMENT` unless you need never-reused ids, and it is not available on WITHOUT ROWID tables.

**Then explain:**
- The docs' guidance (SQLite WITHOUT ROWID page, opened): a non-integer or composite primary key with small rows benefits; a single INTEGER primary key does not; no AUTOINCREMENT; the one-twentieth-of-a-page rule of thumb for row size.
- This is SQLite's clustered index: the table data is the primary-key b-tree, so range scans on the key read neighbouring rows from neighbouring pages. Other engines, described and not executed here: SQL Server has one clustered index per table (data ordered by that key) and nonclustered indexes pointing to it; MySQL InnoDB always clusters on the primary key and its secondary indexes carry the primary key value; PostgreSQL tables are heaps, and `CLUSTER` reorders a table once by an index without keeping it ordered afterwards.
- Why the rowid layout costs space: the key is stored in the table (as columns) and again in the autoindex, and every autoindex entry also carries the rowid.
- Space is not returned by `DELETE`: SQLite reuses free pages for new rows, so the file stays as large as the high-water mark until `VACUUM`.

**Follow-ups:**
- What does `dbstat` report for `freelist` pages? (Free pages are not part of any b-tree; `PRAGMA freelist_count` gave 21 and 29.)
- Would an extra index on `b` help the `b` lookup, and what does it cost in space? (Not run in this answer; an extra index would add pages and write cost.)
- How would you choose the page size? (Not run.)

**Common mistakes:**
- Using WITHOUT ROWID for wide rows or for a single integer key.
- Expecting `DELETE` to shrink the database file.
- Expecting a lookup on the second key column to use the composite primary key.
- Running `VACUUM` on a live database without budgeting the extra disk and the lock.
'''

P[32] = r'''
**Say this first (1 line):** Partitioning splits one logical table so the engine can skip whole pieces (pruning) and drop old data cheaply, but pruning only works when the query's predicate is on the partition key in a form the optimiser can evaluate; SQLite has no partitioning, and my monthly-table emulation shows it probes every branch of the view while a query that names the right table touches one.

**Schema and sample data:**
```sql
CREATE TABLE ev_2024_01(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_time TEXT, event_type TEXT);
CREATE INDEX ix_2024_01_time ON ev_2024_01(event_time);
CREATE INDEX ix_2024_01_user ON ev_2024_01(user_id);
-- the same for ev_2024_02 ... ev_2024_06; 60,000 seeded rows over six months
CREATE VIEW ev AS SELECT * FROM ev_2024_01 UNION ALL SELECT * FROM ev_2024_02 UNION ALL ... SELECT * FROM ev_2024_06;
```
The run builds this twice, once with `CHECK (event_time >= 'first of month' AND event_time < 'first of next month')` on each table.

**SQL answer:** the queries run in the Code block (same text as `one_view`, `cross_view`, `direct`, `by_user`):
```sql
SELECT COUNT(event_type) FROM ev WHERE event_time >= '2024-03-01' AND event_time < '2024-04-01'
SELECT COUNT(event_type) FROM ev WHERE event_time >= '2024-03-15' AND event_time < '2024-04-15'
SELECT COUNT(event_type) FROM ev_2024_03 WHERE event_time >= '2024-03-01' AND event_time < '2024-04-01'
SELECT COUNT(*) FROM ev WHERE user_id = 42
```

**pandas answer:** the expected counts come from the unpartitioned frame:
```py
exp_one = int(((ev.event_time >= "2024-03-01") & (ev.event_time < "2024-04-01")).sum())
```

**Example:** the six monthly tables hold 10,211, 9,606, 10,123, 9,811, 10,267 and 9,982 rows (60,000 in all). March has 10,123 rows, so the one-month query returns 10,123 whichever way it is written. Through the view the plan lists a `SEARCH` on all six tables (five of the ranges are empty); written against `ev_2024_03` directly there is one `SEARCH` and the cross-month query (15 March to 15 April) must touch two tables, which only the view or a `UNION ALL` of the two tables can do. The user query (`user_id = 42`) has no month in it, so every month has to be searched, with any layout; there are 10 such rows.

**Code:** run with `python3 -I`.
{{CODE}}

**Output (my run):**
{{OUT}}

**Edge cases:**
- What I observed: SQLite probes every branch of the view with that branch's own index, for both the one-month and the cross-month filter. The `CHECK` constraints made no difference to the plan or the step counts (identical in both runs), so SQLite did not use them to skip tables in this test; it is the view, not the planner, that lacks partition knowledge.
- The view costs more than naming the table: 162,039 VM steps through the view against 50,632 for the table named directly, for the same 10,123 rows. A view with only the March branch also took 50,632 steps, so the extra is not the five empty probes; it is the compound-query machinery moving every row through the view (my inference from that comparison, not a documented explanation).
- A filter that wraps the key in a function (`strftime(...)`, or `substr(event_time, 1, 7) = '2024-03'`) would defeat the index range in each branch; I did not run it in this answer (function-on-column plans are covered elsewhere in this part).
- Rows landing in the wrong monthly table are impossible for a real partitioned table, but a hand-made set of tables relies on the loader and the CHECK to be correct.

**Then explain:** (everything below that is not SQLite is not executed here, with no vendor numbers)
- Range, list and hash partitioning: range puts rows with key ranges (days, months) in separate partitions, list puts named values (a region) in each, and hash spreads rows evenly over a fixed number of partitions by hashing a key (good for even sizes and point lookups, useless for range pruning).
- What pruning needs: a predicate on the partition key that the optimiser can evaluate at planning or run time, such as a range on the date column. A function on the key (`WHERE DATE(event_time) = ...`), an implicit cast of the key to another type, or a condition on a different column can defeat it, so the engine reads every partition.
- Local versus global indexes: a local index is split along the same partitions (maintenance is per partition, a partition can be dropped or loaded with its index); a global index spans all partitions (efficient for lookups on a non-key column but heavier to maintain when a partition is dropped), and which engines offer which varies.
- The small-partitions problem: thousands of tiny partitions (per hour, per user) add planning overhead, metadata and many small files; choose a grain where partitions hold a meaningful amount of data.
- Deletes and retention: dropping or detaching an old partition is a metadata operation, whereas `DELETE ... WHERE event_time < ...` on a huge table writes and logs every row (and can bloat or lock; see Q35).
- Partitioning versus an index: an index is an extra ordered structure that lets the engine find rows fast within a table; partitioning is a physical layout that lets it skip whole chunks and manage them separately. They combine (a local index inside each partition), and a partition key with a query that does not use it gives no benefit.
- Clustering and sort keys: BigQuery clustering sorts data within a table or partition by chosen columns so filters on them read fewer blocks; Snowflake stores data in micro-partitions with min and max metadata, prunes by that metadata, and offers clustering keys for large tables; Redshift has sort keys and distribution keys (the latter chooses which node holds a row, which matters for joins). I describe these from general knowledge and did not run or benchmark any of them.
- Columnar storage and materialised views: columnar formats read only the needed columns and compress similar values well; a materialised view stores a precomputed query result that is refreshed on a schedule or incrementally, trading freshness and storage for speed. All not executed here.
- For 2 billion rows: partition by event date (retention and date filters), consider clustering or a secondary index on `user_id` for the user queries, and test with the real engine's plan tool, since this SQLite emulation shows the idea, not the engine behaviour.

**Follow-ups:**
- What if most queries filter on `user_id`? (Partition or cluster by it, or by a hash of it; date partitioning no longer helps those queries, as the `user_id` plan above shows.)
- How do you add next month's partition and drop old ones safely? (Create it ahead of time; detach or drop the oldest; automate and test.)
- What about skew? (A hot partition or a hash with few distinct values; not run here.)

**Common mistakes:**
- Partitioning by a column the queries do not filter on.
- Wrapping the partition key in a function or cast in the WHERE clause.
- Thousands of tiny partitions.
- Thinking SQLite prunes a UNION ALL view (it did not here), or that partitioning replaces indexes.
- Quoting vendor speed-ups without a measurement.
'''

P[33] = r'''
**Say this first (1 line):** Read a plan from the inside out and compare estimated with actual rows; the join algorithm (nested loop, hash, merge) follows from the sizes, the indexes and the sort order, and SQLite prints only a simple nested-loop family, so the other engines' plan reading below is described, not executed.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);   -- 2,000 rows, 4 cities
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);   -- 20,000 rows
CREATE INDEX ix_o_cust ON orders(customer_id);
CREATE TABLE a(x INTEGER, k INTEGER);   -- 3,000 rows, no index
CREATE TABLE b(y INTEGER, k INTEGER);   -- 3,000 rows, no index
```

**SQL answer:** four statements whose plans are printed in the Code block (same text as `q1` to `q4`):
```sql
SELECT c.name, o.amount FROM customers c JOIN orders o ON o.customer_id = c.customer_id WHERE c.city = 'Pune'
SELECT COUNT(*) FROM a JOIN b ON b.k = a.k
WITH t AS (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) SELECT t1.customer_id, t1.s FROM t t1 WHERE t1.s > (SELECT AVG(s) FROM t) ORDER BY t1.customer_id
SELECT customer_id, s FROM (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) WHERE s > 6000
```

**pandas answer:** pandas `merge` is the equivalent of the first two joins and a `groupby` the others; the Code block asserts they match:
```py
e1 = cust[cust.city == "Pune"].merge(orders, on="customer_id")[["name", "amount"]]
assert n2 == len(A.merge(B, on="k"))
```

**Example:** plan 1 is a plain nested loop: scan the (filtered) customers, and for each one probe the index `ix_o_cust` on `customer_id=?`; 5,010 order rows come back for the Pune customers. Plan 2 has no usable index on either side, so SQLite builds a temporary `AUTOMATIC COVERING INDEX` on `b(k)` for the duration of the query and probes it for each row of `a`, with a `BLOOM FILTER` in front to skip keys that cannot match (17,841 matching pairs). Plan 3 computes the grouped CTE once (`MATERIALIZE t`) because it is used twice, and plan 4 (grouped subquery used once) is a `CO-ROUTINE`: rows are produced on demand and not stored.

**Code:** run with `python3 -I`.
{{CODE}}

**Output (my run):**
{{OUT}}

**Edge cases:**
- In this run the plan for join 2 was the same before and after `ANALYZE`; the earlier research run (a different schema) saw a bloom filter appear only after `ANALYZE` in a different schema, so do not generalise from either.
- Plan text is not a stable interface: the SQLite documentation says the format may change between versions (this run is SQLite 3.45.1), and other engines' output differs by version and settings. Parse plans only for diagnosis, not in programs.
- `EXPLAIN QUERY PLAN` in SQLite does not execute the statement (the row count stayed 20,000 after explaining a `DELETE`), while `EXPLAIN ANALYZE` in PostgreSQL does execute it (next section).

**Then explain:** (everything about other engines is not executed here, with no vendor numbers)
- PostgreSQL `EXPLAIN (ANALYZE, BUFFERS)`: each plan node shows `cost=start..total`, estimated `rows` and `width` (average row bytes), and with ANALYZE also `actual time=first..last`, actual `rows` and `loops` (the node ran that many times, so multiply per-loop figures). `BUFFERS` adds `shared hit` (pages found in the cache) and `read` (pages fetched from outside it). The first thing to look at is the gap between estimated and actual rows: a large gap means stale or insufficient statistics and usually explains a bad join choice.
- MySQL `EXPLAIN`: per table, `type` (the access method: `const`, `eq_ref`, `ref`, `range`, `index`, `ALL`, from best to worst in general), `key` (index chosen) and `key_len` (how much of a composite index is used), `rows` (estimate), `filtered` (estimated percentage kept after other conditions) and `Extra` (for example `Using index` for covering, `Using filesort`, `Using temporary`, `Using where`). `EXPLAIN FORMAT=JSON` gives the same with cost details and nesting. I read these from the MySQL manual page, not by running MySQL.
- SQL Server graphical plan: operators read right to left; index seek (jumps to matching keys) versus scan (reads the structure), a key lookup (extra trip to the clustered index for columns the nonclustered index lacks), estimated versus actual rows on each operator, and spill warnings when sort or hash work exceeded its memory grant and went to disk.
- Nested loop, hash and merge joins: a nested loop does one probe of the inner side per outer row, so it wins when the outer side is small and the inner side has a good index (plan 1 above). A hash join builds a hash table on the smaller input and probes it with the other, so it wins on large unsorted inputs, uses memory proportional to the build side and can spill. A merge join walks two inputs sorted on the join key, so it wins when both are already sorted (from an index or a prior sort) and the output is large; it uses little memory but needs the order. SQLite implements nested loops only (with automatic indexes and bloom filters as substitutes for the hash idea).
- Bitmap index scans (PostgreSQL) combine several index conditions into a bitmap of pages and then read the table pages in physical order, a middle path between an index scan and a full scan; index-only scans return the answer from the index without table access when the visibility information allows it (the PostgreSQL docs concept; SQLite's equivalent is the `COVERING INDEX` line).
- Why `EXPLAIN ANALYZE` executes the statement: it needs real timings and row counts, so an `INSERT`, `UPDATE` or `DELETE` really happens. Wrap it in a transaction and roll back (`BEGIN; EXPLAIN ANALYZE ...; ROLLBACK;`). The Code block shows the SQLite version of the rollback idea: 20,000 rows, then 16,413 inside the transaction after a `DELETE`, then 20,000 after `ROLLBACK`.
- What SQLite prints that others differ on: `SCAN`/`SEARCH`, `USING INDEX` and `COVERING INDEX`, `AUTOMATIC` indexes, `BLOOM FILTER`, `MATERIALIZE`, `CO-ROUTINE` and `USE TEMP B-TREE`, with no cost or row estimates in the output.

**Follow-ups:**
- When would you force a hash join? (Usually you do not; fix the statistics or indexes first.)
- What does a large estimate gap look like in practice? (An estimate of 10 rows against thousands actual, with a nested loop chosen; not run.)
- How would you read plan 3's `SCALAR SUBQUERY`? (The `AVG` runs once, not once per row; checked only by reading the plan.)

**Common mistakes:**
- Running `EXPLAIN ANALYZE` on a write against production without a rollback.
- Reading only the cost number, not estimated versus actual rows.
- Treating one engine's plan vocabulary as another's.
- Parsing plan text in application code.
'''

P[34] = r'''
**Say this first (1 line):** In SQLite the plan follows the bound value and the index set, but Python's `sqlite3` statement cache can make an identical `EXPLAIN QUERY PLAN` text show a stale plan after a `DROP INDEX`, and hints (`INDEXED BY`, `NOT INDEXED`, unary plus) override the planner, so they should be a last resort backed by a measurement.

**Schema and sample data:**
```sql
CREATE TABLE t(id INTEGER PRIMARY KEY, cust INTEGER, name TEXT, status TEXT);
-- 50,000 seeded rows; status is 'a' for 98%, 'b' for 1.5% and 'c' for 0.5%; cust is 1 to 500
-- indexes are created and dropped during the run: ix_cust(cust), ix_name(name COLLATE NOCASE), ix_status(status)
```

**SQL answer:** the statements run in the Code block (the hint forms are the `H` template):
```sql
SELECT COUNT(*) FROM t WHERE cust = 7
SELECT COUNT(*) FROM t WHERE name LIKE ?
SELECT COUNT(*) FROM t {hint} WHERE status = 'c' AND cust > 100      -- hint is empty, INDEXED BY ix_cust, or NOT INDEXED
SELECT COUNT(*) FROM t WHERE +status = 'c' AND cust > 100
```

**pandas answer:** the counts are checked against pandas:
```py
exp_c = int(((df.status == "c") & (df.cust > 100)).sum())
exp = int(df["name"].str.lower().str.startswith("alp").sum())
```

**Example:** `cust = 7` matches 88 rows. With no index the plan is `SCAN t` (150,100 VM steps); after `CREATE INDEX` the same text runs as `SEARCH t USING COVERING INDEX ix_cust` (277 steps) with the same count 88. For `LIKE ?` on a NOCASE index, `'alp%'` is a range search (37,466 steps, 12,483 rows, which includes `Alpine...` because LIKE ignores case), `'%pha1'` has no usable prefix and scans the whole index (200,017 steps, 4 rows), and `'alp%'` again goes back to the range search: one statement text, three plans. For the status query the planner chose `ix_status` (1,469 steps), because `status = 'c'` is selective; forcing `ix_cust` (a range on `cust > 100`, most of the table) took 159,624 steps and `NOT INDEXED` 150,720, all with count 208.

**Code:** run with `python3 -I`.
{{CODE}}

**Output (my run):**
{{OUT}}

**Edge cases:**
- Stale plan: after `DROP INDEX`, `EXPLAIN QUERY PLAN` with the identical text still printed `SEARCH ... USING COVERING INDEX ix_cust`, while the same text with two trailing spaces, a fresh connection and a connection with `cached_statements=0` printed `SCAN t`. The real `SELECT` with the identical text still ran correctly (count 88, 150,100 steps, a full scan), so only the displayed plan was stale. In the opposite case (`CREATE INDEX` after the text was used) the identical text showed the new plan. I did not find the cause in the documentation; my guess is that the cached `EXPLAIN` statement is not re-prepared after the index disappears. Treat any plan you print as suspect after DDL on the same connection, and verify with a fresh connection or a changed text.
- `INDEXED BY ix_status ... WHERE cust = 7` did not error: it returned 88 rows (I did not print its plan in this run). `INDEXED BY no_such_index` raised `OperationalError: no such index: no_such_index`. I did not trigger the documented error for an existing index that cannot be used; do not rely on that error to detect a bad hint.
- The unary plus on `+status` disabled `ix_status` for that term, and the planner then picked `ix_cust` (159,624 steps), the same slow plan as `INDEXED BY ix_cust`.
- SQLite prepares a statement once and re-prepares it when the schema changes or when a bound parameter value would change the plan (the optimiser overview documents the `LIKE ?` case, which my run confirms).
- I did not measure whether string-built SQL defeats the statement cache: the trace callback shows expanded text, so it could not tell the two cases apart, and the claim below is the general reasoning, not a measurement.

**Then explain:** (everything below about other engines is not executed here, with no versions or numbers)
- The Python `sqlite3` module keeps a cache of prepared statements keyed by the SQL text (the `cached_statements` argument to `connect`; I set it to 0 above to switch it off), which is why a changed text or a fresh connection recompiles and an identical text can reuse an old compiled statement.
- SQL Server parameter sniffing: when a parameterised query or procedure is first compiled, the optimiser looks at the first parameter value and caches a plan built for it; later calls with very different values (a rare value, then a very common one) reuse a plan that may be wrong for them. Symptoms: the same procedure is fast for some inputs and slow for others, the slow plan appears after a restart or recompile, and the estimated row counts in the cached plan do not match the actuals for the slow call. Mitigations: `OPTION (RECOMPILE)` (compile each time, trading CPU for plan quality), plan guides, query hints, restructuring (for example separate procedures for the skewed cases), and newer parameter-sensitive plan features that keep several plans for one statement.
- PostgreSQL prepared statements: the server can plan a prepared statement for each execution with the actual values (a custom plan) or reuse one generic plan; it compares the cost and, after a few executions, may switch to the generic plan. A skewed parameter can make the generic plan poor.
- MySQL: optimizer hints in comments and index hints (`USE INDEX`, `FORCE INDEX`, `IGNORE INDEX`) to steer a plan.
- Why hints are a last resort: they freeze a decision while data and statistics change, hide the underlying problem (stale statistics, a missing index), and break when an index is renamed or dropped. Prefer fixing statistics, indexes and the query shape; keep a hint only with a comment, a measurement and a plan to revisit it. My SQLite run shows the risk: both hints made the status query about 100 times more VM steps than the planner's choice.
- String-built SQL: concatenating values into the text is open to injection and, because each value yields a different statement text, it prevents reuse of a cached plan or prepared statement (each text is compiled separately); bound parameters fix both, at the cost of the parameter-sniffing question above.

**Follow-ups:**
- How would you see whether SQLite chose a plan using statistics? (`ANALYZE` and `sqlite_stat1`; not run in this answer.)
- What is the safer alternative to `INDEXED BY`? (Fix the index or the predicate so the planner picks it itself.)
- How would you reproduce parameter sniffing without SQL Server? (You cannot exactly; the SQLite `LIKE ?` case is the nearest executable analogue.)

**Common mistakes:**
- Trusting a plan printed on a connection that has just changed the schema.
- Adding hints without measuring (they were far worse here).
- Building SQL by string concatenation.
- Assuming a plan for one parameter value is right for all values.
'''

P[35] = r'''
**Say this first (1 line):** In SQLite's default rollback-journal mode a reader holding an open read transaction stops a writer from committing, while in WAL mode the writer commits and the reader keeps its snapshot; other engines use row-level locks and MVCC, which SQLite does not have, and those parts below are described, not executed.

**Schema and sample data:**
```sql
CREATE TABLE acct(id INTEGER PRIMARY KEY, bal INTEGER);
INSERT INTO acct VALUES (1, 100);
-- a file-backed database in a temporary directory, three or more connections with timeout=0.1 (busy_timeout 100 ms)
```

**SQL answer:** the statements in the Code block (the transactions are sent by hand, `isolation_level=None`):
```sql
PRAGMA journal_mode=WAL;      -- or the default 'delete'
PRAGMA busy_timeout;
BEGIN; SELECT bal FROM acct WHERE id = 1;            -- reader, stays open
BEGIN; UPDATE acct SET bal = 150 WHERE id = 1; COMMIT;   -- writer
BEGIN IMMEDIATE;                                    -- second writer
```

**pandas answer:** the final table is read with pandas and compared with the expected frame:
```py
pd.testing.assert_frame_equal(o, pd.DataFrame({"id": [1], "bal": [expected[m]]}), check_dtype=False)
```

**Example:** the account starts at 100. In rollback-journal mode: the reader opens `BEGIN` and reads 100, which holds a shared lock for the whole transaction; the writer's `UPDATE` is accepted into its own transaction, but its `COMMIT` fails after the 100 ms timeout with `database is locked`, the reader still sees 100, and a `t.db-journal` file exists. After the reader commits, the writer retries and commits 150. In WAL mode: the same steps, but the writer's `COMMIT` succeeds, the reader inside its transaction still sees 100, files `t.db-wal` and `t.db-shm` exist, and after the reader commits it sees 150.

**Code:** run with `python3 -I`.
{{CODE}}

**Output (my run):**
{{OUT}}

In the output, the `final table` line holds 150 for the rollback-journal run and 151 for the WAL run: the WAL run does one more `+1` update in the stale-snapshot demo, so the expected frames differ by design.

**Edge cases:**
- Only one writer at a time in both modes: a second `BEGIN IMMEDIATE` while another writer was open gave `database is locked`. Readers do not block writers in WAL mode, but writers still queue behind each other.
- In WAL mode a reader whose snapshot went stale cannot upgrade to a writer: after another connection committed a change, the reader's `UPDATE` failed with `database is locked` (a snapshot conflict); the reader must roll back and retry on a fresh transaction.
- An uncommitted writer does not block readers: the research run saw a reader succeed during an uncommitted writer transaction in both modes; this run does not repeat that.
- `PRAGMA journal_mode` returns the mode in effect; WAL is persistent in the database file, while `busy_timeout` is per connection (the `timeout` argument sets it). The `-wal` and `-shm` files are the write-ahead log and its shared-memory index; the WAL is merged into the main file at a checkpoint.
- Reading inside versus outside a transaction: an autocommit reader saw 1 and then 2 for two SELECTs with a commit between them, while a reader inside `BEGIN` on a WAL database saw 2 and 2 even though another connection then committed 3. That is the SQLite version of non-repeatable reads (autocommit) versus a stable snapshot (inside a transaction).

**Then explain:** (everything below that is not SQLite is not executed here; no versions or numbers)
- Why long transactions hurt: they hold locks (blocking writers or other lockers), they stop cleanup (in MVCC engines old row versions cannot be removed, causing table bloat or undo-log growth), and they hold back replication or checkpointing (replication lag). Keep transactions short, do not wait for user input inside one, and batch large changes.
- The cost of `CREATE INDEX` on a live table: a plain build blocks writes (and sometimes reads) while it runs. Options exist to reduce that: PostgreSQL has `CREATE INDEX CONCURRENTLY` (slower, extra scans, cannot run inside a transaction block), SQL Server and MySQL have online index options (edition and storage-engine dependent). All described, not executed. SQLite builds the index under the write lock, so no concurrent write can commit.
- MVCC versus lock-based isolation: with MVCC, readers see a snapshot of committed versions and do not block writers (PostgreSQL, InnoDB, and SQLite's WAL snapshots in a limited form); with lock-based isolation, readers take shared locks that conflict with writers' exclusive locks, which is what the rollback-journal run showed at database level.
- Anomalies by isolation level, in general terms (exact behaviour differs by engine, so check the manual):

| Anomaly | Read uncommitted | Read committed | Repeatable read | Serializable |
|---|---|---|---|---|
| Dirty read (see another transaction's uncommitted write) | possible | not possible | not possible | not possible |
| Non-repeatable read (same row read twice gives different values) | possible | possible | not possible | not possible |
| Phantom read (same predicate returns different rows) | possible | possible | possible in the textbook definition; some engines prevent it | not possible |

- A deadlock in words: transaction A updates row 1 and then wants row 2; transaction B updated row 2 and now wants row 1; each waits for the other, so the engine detects the cycle and aborts one with an error that the application must retry. Prevent it by touching rows in a consistent order and keeping transactions short. SQLite avoids the classic form by returning `database is locked` (busy) instead of waiting forever, as the stale-snapshot upgrade showed.
- What SQLite does not provide: row-level locking (locks are at database level; WAL allows one writer plus many readers), a server process, or the isolation-level menu of server databases (I believe SQLite transactions behave as serializable; I did not test isolation levels here).

**Follow-ups:**
- How do you tune the wait? (`busy_timeout`, short transactions, `BEGIN IMMEDIATE` for writers; I used 100 ms only to keep the demo fast.)
- What happens to the WAL file when it grows? (Checkpointing; not run here.)
- How would you detect a long-running transaction on a server database? (The engine's activity view; not executed here.)

**Common mistakes:**
- Leaving a read transaction open in the application "just in case".
- Assuming WAL allows two concurrent writers.
- Reading `database is locked` as corruption instead of contention.
- Starting an online index build without checking its transaction restrictions.
- Treating the isolation-level table as identical across engines.
'''
