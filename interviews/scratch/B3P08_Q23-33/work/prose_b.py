P = {}

P[28] = dict(
say="Count March events per user, take the mean with `AVG` and the median from `ROW_NUMBER` and `COUNT(*) OVER ()` (SQLite has no MEDIAN), cut `NTILE(10)` over users ordered by event count with a `user_id` tie-breaker, and divide the top decile's events by all events; whether zero-event users are in the population changes every one of these numbers, so say which one you use.",
schema_note="thirteen users (user 13 is a test user, user 12 and user 11 have no March events). The `events` rows are generated in the Code block: March counts per user are 1, 1, 2, 2, 3, 4, 5, 8, 20, 60 for users 1 to 10 (106 events), plus four rows that must be ignored: a February event for user 1, an April 1st event for user 2 (the upper bound is exclusive), a February event for user 11 and a March event for test user 13. Dates and counts are toy values.",
schema="SCHEMA",
sqlnote="`SQL_TEMPLATE` in the Code block, with `{JOIN}` replaced by `JOIN` (active users only, `SQL_ACTIVE`) or `LEFT JOIN` (all non-test registered users, `SQL_ALL`). The median is the average of the rows at positions `(cnt + 1) / 2` and `(cnt + 2) / 2` (integer division, see Part 4 Q38 for the median pattern in full). `SQL_TEMPLATE`:",
sqls=["SQL_TEMPLATE"],
sqlafter="NTILE itself is explained in Part 4 Q21 and pandas `qcut` versus NTILE in Part 4 Q33; here pandas needs a hand-written NTILE (`ntile` in the function below), because `qcut` splits by value, not by position.",
pdnote="the same logic (`keep_zero` is the INNER versus LEFT join choice; `ntile` reproduces positional NTILE):",
example="""- Active users only (users 1 to 10; users 11 and 12 and test user 13 excluded): total 106 events, mean 106/10 = 10.6. Sorted counts are 1, 1, 2, 2, 3, 4, 5, 8, 20, 60; the median is the average of the 5th and 6th, (3 + 4)/2 = 3.5. NTILE(10) over 10 rows gives one user per decile, so the top decile is user 10 with 60 events, 60/106 = 56.60 percent.
- All 12 non-test users (zero-event users 11 and 12 kept): same 106 events, mean 106/12 = 8.83, median is the average of the 6th and 7th of 0, 0, 1, 1, 2, 2, 3, 4, 5, 8, 20, 60, that is (2 + 3)/2 = 2.5. NTILE(10) over 12 rows makes the first two buckets hold two users each (12 = 10 x 1 + 2 extra), so the top decile is users 10 and 9 with 80 events, 80/106 = 75.47 percent.
- Decile boundary and ties: users 3 and 4 both have 2 events, yet user 3 is in decile 5 and user 4 in decile 6 because NTILE is positional and the `user_id` tie-breaker decides. Without a tie-breaker the split of tied users would be arbitrary and could change between runs.
- The mean (10.6) is three times the median (3.5): the two heaviest users make most of the volume.""",
edge="""- Zero-event users: included or excluded changes users, mean, median, the decile sizes and the top share (all four printed). 'Events per active user' by definition excludes them.
- Even count: median averages two middle rows; odd count: both positions point at the same row, so the average is that row.
- Fewer than 10 users: NTILE(10) makes buckets of size 1 or 0 (the pandas helper falls back to `range(1, n+1)` in that case, matching NTILE for 10 or fewer rows).
- Ties at the decile boundary: add a deterministic tie-breaker and state that equal users can land in different deciles; alternatives are `PERCENT_RANK` or rank-based cuts that keep ties together (Part 4 Q36).
- Test users and the date range: the range uses `>= '2024-03-01' AND < '2024-04-01'`, so the whole of March 31 is included whatever the time part.""",
explain="""- Mean versus median: usage is skewed (a few heavy users), so the mean is pulled up and says little about a typical user. Report the median and a high percentile, or the share held by the top decile.
- NTILE(10) splits by position, not by value: with 12 rows two buckets get an extra row. Top decile is therefore 'the first 10 percent of users in rank order', not 'users above the 90th percentile value'.
- Power-user share: top-decile events over all events (56.6 percent active-only, 75.47 percent with zero users). This is a concentration measure; the Pareto version with revenue is in Part 4 Q49.
- Median without MEDIAN: `ROW_NUMBER() OVER (ORDER BY n)` and `COUNT(*) OVER ()`; SQLite integer division makes `(cnt + 1) / 2` the lower middle position (12 gives 6 and 7, confirmed in my run). PostgreSQL has `PERCENTILE_CONT(0.5)` and BigQuery `PERCENTILE_CONT` as a window function (not executed here).
- Population choice belongs in the definition: say 'active users in March, non-test'.""",
fu="""- Show the whole decile table? `SQL_DECILES` in the Code block prints every user's decile.
- Top 1 percent instead? Use `NTILE(100)`, but note small populations make that meaningless.
- Median events per user per day? Compute per user-day first, then the median; the grain changes.""",
mist="""- Reporting the mean as the typical user.
- NTILE without a tie-breaker, so tied users move between runs.
- Mixing populations: mean over active users and top-decile share over all registered users.
- Forgetting the test-user filter, or using `<= '2024-03-31'` on a timestamp and losing most of March 31.
- Using `qcut` as if it were NTILE (it cuts by value quantiles, can raise on duplicate edges unless told to drop them, and does not break ties by position).""",
)

P[29] = dict(
say="Compute revenue at line-item grain (`qty * unit_price`) from completed orders only, aggregate to product, add `SUM(revenue) OVER (PARTITION BY category)` for the share and `DENSE_RANK` within category, then keep rank 2 or better; with `DENSE_RANK` a tie at second place returns three products, which is the intended 'ties kept' behaviour.",
schema_note="eight products (product 7 has no category, product 8 is alone in its category), five orders (order 4 is cancelled) and thirteen line items. The last item references product 99, which is not in `products`. Electronics is built so that products 2 and 3 tie at 200.",
schema="SCHEMA",
sqlnote="`SQL_MAIN` in the Code block (`SQL_WRONG` is the order-total-on-every-row version):",
sqls=["SQL_MAIN"],
sqlafter="",
pdnote="the same logic, identical to the Code block (`rank(method='dense', ascending=False)` is `DENSE_RANK`):",
example="""- Completed line items only: order 4 (cancelled) is excluded, which removes 10 units of product 4 (500) and leaves the Charger at 50.
- Electronics: Phone 2 x 500 = 1000, Case 2 + 2 units x 50 = 200 (4 units), Cable 100 + 100 = 200 (2 units), Charger 50. Category total 1450. Dense ranks: Phone 1, Case and Cable 2 (tie), Charger 3. The top-2 filter keeps Phone, Cable and Case: three rows. Shares: 1000/1450 = 68.97, 200/1450 = 13.79 each.
- Books: Novel 3 x 20 = 60, Notebook 5 x 10 = 50, so ranks 1 and 2, shares 54.55 and 45.45.
- Product 7 (Gift card) has no category and goes to an explicit 'Uncategorised' group with share 100; Home has one product (Lamp, 80), so it returns one row, not two.
- The item for product 99 is dropped by the inner join to `products`.
- Wrong version: joining an order total onto every item row makes product revenue 880 for Cable (the whole order 2 and order 5 totals) instead of 200, and 1260 for Phone instead of 1000, because every product in the order is credited with the order's total.""",
edge="""- Cancelled orders: excluded here (status filter). Returned or partially refunded lines would need a refunds table; not in this question.
- NULL category: `COALESCE(category, 'Uncategorised')` makes it a group; leaving it NULL would still group it (GROUP BY and window PARTITION BY treat NULLs as one group) but print NULL.
- Category with fewer than two products: returns what it has (Home: one row). No padding.
- Ties: `DENSE_RANK` keeps all tied products, so the result can exceed 2 rows per category; `ROW_NUMBER` would pick one arbitrarily unless a tie-breaker is added (Part 4 Q2 and Q12).
- Products with no completed sales are absent (inner join on items); to list them with 0, start from `products` and LEFT JOIN.
- Share uses the category total before the top-2 filter, so shares of the shown rows need not add to 100.""",
explain="""- Grain: revenue belongs to the order line, so multiply and sum at that grain. An order-level total joined to lines is repeated once per line.
- Window functions run after GROUP BY, so aggregate to product first, then rank and take shares in the same query (ranking aggregates is Part 4 Q13).
- The rank filter has to be in an outer query or CTE because window results cannot be used in WHERE.
- Units and revenue come from the same filtered rows; do not mix completed-only revenue with all-status units.
- Dialect: Snowflake and BigQuery have `QUALIFY` to filter on the rank directly (not executed here).""",
fu="""- Top 2 per category with exactly two rows? Use `ROW_NUMBER` with a tie-breaker (`name`), and say which product is dropped.
- Net of discounts? Needs a discount column; subtract at line level.
- Share of total company revenue as well? Add a second window `SUM(revenue) OVER ()`.""",
mist="""- Joining an order total (or order amount) to each item and summing it.
- Including cancelled orders in revenue or units.
- Using `RANK` and then filtering `<= 2`, which behaves like `DENSE_RANK` only until a tie occurs before the cut (a tie at rank 1 skips rank 2).
- Dropping uncategorised products silently through an inner join on a category table.
- Taking share after the top-2 filter, so shares add to 100 by accident.""",
)

P[30] = dict(
say="`pivot_table` and `pd.crosstab` both drop NaN keys by default and `value_counts` drops NaN unless `dropna=False`, so a NaN channel silently disappears from all three; a SQL `GROUP BY` keeps a NULL group, which is why I fill the key (`'unknown'`) first and then assert the pandas shares equal the SQL result.",
schema_note="ten orders for five users. Three orders have a NULL channel (orders 6, 7, 8). `users.signup_channel` is complete and is used for a fallback rule at the end. Everything here is made-up toy data.",
schema="SCHEMA",
sqlnote="`SQL_COUNTS` in the Code block (NULL channel shown as 'unknown' with `COALESCE`, which turns the NULL group into a labelled row):",
sqls=["SQL_COUNTS"],
sqlafter="",
pdnote="there is no single function here; the pandas steps are printed in the Code block. The core calls are `pd.pivot_table(orders, index=\"channel\", columns=\"status\", values=\"order_id\", aggfunc=\"count\", fill_value=0)` for counts, `pd.crosstab(orders[\"channel_f\"], orders[\"status\"], normalize=\"index\")` for row shares and `orders[\"channel\"].value_counts(normalize=True, dropna=False)` for the mix, where `channel_f` is `channel.fillna(\"unknown\")`.",
example="""- SQL on the ten orders: ads 3 orders (2 completed, 1 cancelled), organic 2 (both completed), referral 2 (1 and 1), NULL 3 (2 completed, 1 cancelled). Completed share is 0.6667, 1.0, 0.5 and 0.6667; channel mix is 0.3, 0.2, 0.2, 0.3.
- pandas `pivot_table` default: the NaN-channel rows are gone, 7 of 10 rows are counted and there is no 'unknown' row.
- `crosstab(..., normalize='index')` default: the same three rows only; normalising by `'all'` makes the shares add to 1.0 but over the 7 kept rows, not over 10.
- `value_counts(normalize=True)` default gives ads 0.4286, organic 0.2857, referral 0.2857: shares of 7, so ads looks like 43 percent of orders instead of 30 percent. With `dropna=False` the NaN row appears with 0.3 and every share matches SQL.
- After `fillna('unknown')` the pivot, the crosstab and the mix all match SQL, which the Code block asserts (compared after sorting by channel).
- Fallback rule: filling the NaN order channel from the user's signup channel (merge, then `fillna`) leaves no NaN: ads 5, organic 3, referral 2. That is a different, defined attribution rule, not the same as 'unknown'.""",
edge="""- Default aggfunc: `pivot_table` defaults to `aggfunc='mean'`. On `order_id` it printed means such as 5.5, not counts, and an NaN cell for organic cancelled; always pass `aggfunc='count'` (non-null values) or `'size'`.
- `aggfunc='count'` counts non-null values of `values`; if the values column has NaN the counts are short. Use a never-null column such as the order id.
- Unused categories: with a categorical channel that has an unused category 'affiliate', `pivot_table` omitted it (the `observed=True` default in pandas 3.0, as run here) and `observed=False` showed it; `crosstab` omitted it by default and `dropna=False` showed it. Whether this matches older pandas versions I did not test.
- `fill_value=0` fills empty cells (organic, cancelled) but does not recreate NaN-key rows.
- Dtype: with pandas 3.0 the channel column is the string dtype and missing values are NaN; the behaviours above were run on 3.0.5.""",
explain="""- Which one silently loses the NaN-channel rows: all three pandas calls by default (`pivot_table`, `crosstab`, `value_counts`); SQL `GROUP BY` does not, it returns the NULL group, so SQL and pandas disagree by 3 of 10 rows until you fill or set `dropna=False`.
- `crosstab(normalize='index')` rows add to 1 over the kept rows; the dropped rows silently change the denominators of `'all'` and `'columns'` normalisation, but not of `'index'` for the channels kept.
- `value_counts(normalize=True)` divides by the non-null count by default, so shares change when NaN is dropped. This is the one that changes the mix, not only the table.
- Counts versus mean: forgetting `aggfunc` gives averages of an id column and looks like a table of numbers.
- Safer habit: make missing an explicit value (`fillna('unknown')`) before any pivot, or pass `dropna=False` where the function supports it, and assert row totals equal `len(orders)`.""",
fu="""- Does `groupby` behave the same? It also drops NaN keys unless `dropna=False` (Q31 runs it).
- How do you add row and column totals? `margins=True` on both functions; check the margin label does not clash with a real category.
- Same table in SQL with columns per status? `SUM(status = 'completed')` conditional aggregation, as in `SQL_COUNTS`; SQLite has no PIVOT.""",
mist="""- Relying on the default `aggfunc='mean'`.
- Not noticing that NaN-key rows vanished (7 of 10).
- Comparing pandas shares to SQL shares computed over a different row set.
- Using `normalize=True` on `crosstab` and reading it as row shares (it is `'all'`).
- Filling with 0 instead of a label, which merges unknown orders with a real channel called 0.""",
)
