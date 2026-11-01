**Say this first (1 line):** Flag every row whose plan differs from the previous row of the same customer (first row counts as a change), take a running SUM of the flag as the range id, then `GROUP BY customer_id, range_id` with `MIN(date)` as `valid_from` and `MAX(date)` as `valid_to`, turning the last range into NULL when it is still current.

**Schema and sample data:** daily snapshots up to a fixed as-of date of 2024-03-10 (the latest snapshot date in the table, never today). C1 goes basic, premium, basic and has an exact duplicate row; C2 has no snapshot on 3 March; C3 has a single snapshot; C4 stops on 3 March (churned, not current); C5 has NULL plans. Rows are inserted unsorted.
{{SCHEMA}}

**SQL answer:** `SQL_MAIN` in the Code block. `LAG(snapshot_date) IS NULL` marks the customer's first row, and `plan IS NOT LAG(plan)` is the NULL-safe "changed" test (plain `<>` would drop the NULL rows). The current range gets `valid_to = NULL` only when its last snapshot is the as-of date; a customer whose last snapshot is older keeps a real end date.
{{SQL:SQL_MAIN}}
The strict variant `SQL_STRICT` adds `OR julianday(snapshot_date) - julianday(LAG(snapshot_date) OVER w) > 1` to the flag, so a missing snapshot day starts a new range. `SQL_WRONG` is the tempting `GROUP BY customer_id, plan`.

**pandas answer:** same logic, identical to the Code block:
{{PD}}

**Example:** C1 after `DISTINCT` has basic 1-3 March, premium 4-6 March, basic 7-10 March.
- Change flags by day: 1 (first), 0, 0, 1 (premium), 0, 0, 1 (basic again), 0, 0, 0. Running sum: 1, 1, 1, 2, 2, 2, 3, 3, 3, 3.
- Group 1 is basic 03-01 to 03-03, group 2 premium 03-04 to 03-06, group 3 basic from 03-07; its last snapshot is 03-10, the as-of date, so `valid_to` is NULL.
- `GROUP BY customer_id, plan` instead gives basic 03-01 to 03-10 and premium 03-04 to 03-06: the premium period is nested inside the basic one, which is wrong.
- C2 (1, 2, 4, 5 March, same plan): the main query gives one range 03-01 to 03-05 (the missing 3 March does not change the plan); the strict query gives 03-01 to 03-02 and 03-04 to 03-05.
- C4 ends on 03-03, which is before the as-of date, so `valid_to` is `2024-03-03`, not NULL.

**Code:** run with `python3 -I`. The assert compares after sorting by `customer_id, valid_from`, with NULL and None mapped to the same text.
{{CODE}}

**Output (my run):** pandas prints a NULL as `NaN`.
{{OUTPUT}}

**Edge cases:**
- Missing snapshot day, the decision: I assume the snapshot table is a sampling of a state, so the same plan on both sides of a missing day is the same range (main query). If a missing day means "no data, unknown state" (an outage in the pipeline) use the strict variant. Say which one you assume, because the two give different row counts for C2.
- Plan changes across a missing day: both variants start a new range at the first snapshot with the new plan, so `valid_to` of the earlier range is its last observed day, not the day before the new one. If ranges must tile with no holes, set `valid_to = LEAD(valid_from) - 1 day` instead (a follow-up, not shown).
- Duplicates: an exact duplicate row is removed by `DISTINCT`. Two rows for one day with different plans cannot be resolved by SQL; agree a rule (latest loaded wins) and apply it first.
- NULL plan: C5's NULL plan forms its own range of two days because `IS NOT` treats NULL as a value that equals NULL. With `<>` the transition into and out of NULL would be missed.
- Single row (C3): one range with `valid_from = 2024-03-10`, `valid_to` NULL.
- Unsorted input is handled by the explicit window `ORDER BY`.
- pandas: the `==` comparison gives False for NaN against NaN, so the NaN-safe test is written explicitly as `(plan == prev) | (plan.isna() & prev.isna())`.

**Then explain:**
- Collapsing equal consecutive rows is run-length encoding by a state, the same machinery as Q13; the only SCD-specific parts are the end-date convention and the open-ended current row.
- `valid_to = last day with that plan` is inclusive. Many warehouses prefer a half-open `[valid_from, valid_to)` with `valid_to = next valid_from`; the same grouping works, only the end expression changes.
- NULL for the current row follows the usual "open-ended" convention; some teams use `9999-12-31`, which is easier for range joins (`BETWEEN`) but a magic value.
- The as-of date must be a parameter or the table maximum, never `date('now')`, or the result changes every day.
- Dialects (not executed here): PostgreSQL and others support `IS DISTINCT FROM` as the NULL-safe test (SQLite 3.45.1 also does, probed in Q38 of this part), and `DATEDIFF` or date subtraction replaces `julianday`.

**Follow-ups:**
- Join facts to the dimension? `fact.date BETWEEN valid_from AND COALESCE(valid_to, '9999-12-31')`.
- Count plan switches per customer? Sum of the flag minus 1.
- Why not `GROUP BY customer_id, plan`? Shown above: a plan that returns later is merged into the earlier range.

**Common mistakes:**
- `GROUP BY customer_id, plan` (collapses the second basic into the first).
- Using `<>` and silently losing transitions involving NULL.
- Forgetting `SELECT DISTINCT`, so a duplicate row is carried into the range counts.
- Marking every customer's last range as open even when the customer stopped appearing.
- Hard-coding today's date for the open end.
