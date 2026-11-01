**Say this first (1 line):** Keep only `is_active = 1` rows (deduplicated), number them per user, and group by `julianday(snap_date) - ROW_NUMBER()` to get each active period; filter before numbering, because numbering all rows and filtering afterwards merges periods across inactive days.

**Schema and sample data:** one row per user per snapshot day, 1 to 6 March 2024, no as-of date is needed, so nothing depends on today. U1 has an inactive day (4 March) between active days and a duplicate row; U2 has a missing snapshot (3 March); U3 is never active; U4 has one active day; U5 has a NULL `is_active`. Rows are inserted unsorted.
{{SCHEMA}}

**SQL answer:** `SQL_MAIN` in the Code block (filter, `DISTINCT`, then the date-minus-row-number key):
{{SQL:SQL_MAIN}}
The resubscription count is `SQL_RESUB` in the Code block: the same query wrapped as `p`, `LEFT JOIN`ed from all users so that U3 (no periods) appears with 0, and `MAX(COUNT(p.user_id) - 1, 0)` (SQLite scalar `MAX` with two arguments) so that nobody gets -1.
{{SQL:SQL_RESUB}}
The two alternatives are `SQL_ROWBASED` (row numbers over all rows minus row numbers over the active rows, so missing snapshot rows do not break a period) and `SQL_WRONG` (all-rows row number, then filter).

**pandas answer:** same logic, identical to the Code block:
{{PD}}

**Example:** active days after filtering and `DISTINCT`:
- U1: 1, 2, 3, 5, 6 March (the 0 on 4 March is gone). Day numbers minus row numbers: the first three share one key, the key increases by one at 5 March (a day is missing from the filtered list), so periods 1-3 March (3 days) and 5-6 March (2 days). Periods 2, resubscribed 1.
- U2: 1, 2, 4 March: 3 March has no row, so two periods (2 days and 1 day). Periods 2, resubscribed 1.
- U3: nothing survives the filter, so no period rows; the `LEFT JOIN` still gives periods 0 and resubscribed 0.
- U4: one period of 1 day, resubscribed 0.
- U5: 1 March active, 2 March NULL (not `= 1`, so dropped), 3 and 4 March active: periods 1 March and 3-4 March, resubscribed 1.
- Row-numbering all rows and filtering after (`SQL_WRONG`): day-number minus all-rows row number is constant for U1 across the whole table, so the inactive day does not split it and U1 becomes one 5-day period 1-6 March, and U5 becomes one 3-day period; both are wrong.

**Code:** run with `python3 -I`. The asserts compare the pandas frames with the SQL frames after sorting by `user_id, active_from` (periods) and by `user_id` (summary).
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Edge cases:**
- Missing snapshot day (U2): the main query ends the period, because the filtered list has no 3 March and the day number jumps. The row-based variant (`SQL_ROWBASED`) merges U2 into one 3-row period (1 to 4 March, 3 days) because it only looks at row order. Choose by what a missing row means: if it means "no information, treat the state as unknown", the date-based key is right; if the table is sparse because unchanged days are omitted, the row-based variant (or a state-change table) is right. I assume daily snapshots with no omission, so the main query.
- Inactive day between two active days (U1): always splits, in both variants, because the inactive row is not active.
- NULL `is_active` (U5): `= 1` drops it, so it behaves as inactive. Decide whether NULL means "unknown, keep the period open"; that would need a different rule.
- Duplicates (U1 on 2 March): without `DISTINCT` the duplicate gets its own row number and splits the period; here it is removed first.
- Users with no active days (U3) vanish from the island output, so anything that must list all users needs a `LEFT JOIN` from a users source.
- Single row (U4) and unsorted input are handled.

**Then explain:**
- Filter before numbering when the numbering is meant to run along the filtered rows (the key is `date - rn` with both measured on the same rows). Number all rows first only when you then compare row positions, as in `SQL_ROWBASED`, where the difference of two row numbers is the key. The wrong combination is a row number over all rows used with a date key after filtering.
- The date-based key makes the day line the truth and tolerates nothing missing; the row-number-difference key makes the row order the truth and tolerates missing rows.
- Resubscribed = periods - 1, floored at 0 for users who never subscribed.
- Dialects (not executed here): the two-argument scalar `MAX(a, 0)` is SQLite; PostgreSQL and MySQL write `GREATEST(a, 0)` and Postgres can subtract dates directly.

**Follow-ups:**
- Time to resubscribe? Gap days between consecutive periods with `LAG(active_to)`.
- Churn events? The day after each `active_to` that is not the last snapshot date.
- Only the current period? Q15 logic.

**Common mistakes:**
- `ROW_NUMBER()` over all rows, then `WHERE is_active = 1` (merges across inactive days; shown for U1 and U5).
- Missing `DISTINCT` on repeated snapshots.
- Treating NULL as active.
- Counting resubscriptions as the number of periods (a first subscription is not a resubscription).
- Using `julianday` differences with an assumed integer type; the key is a float here and equal values compare exactly because all values are whole day numbers.
