**Say this first (1 line):** Collapse to one row per room per hour, turn each slot into an integer hour number, keep only the free rows, and group by `hour_number - ROW_NUMBER()` per room; a missing slot row makes the hour number jump, so it breaks the run, and `HAVING COUNT(*) >= 3` keeps ranges of at least three hours.

**Schema and sample data:** hourly slots on 2024-03-04 (R2 runs across midnight), inserted unsorted. R1 has a duplicate row at 11:00, a busy hour at 12:00 and no row at all for 15:00. R2 is free from 22:00 to 01:00. R3 has one free slot. R4 has exactly three free hours then a busy hour and two free hours. R5 has a NULL `is_free`. R6 has a conflicting duplicate at 10:00 (free and busy).
{{SCHEMA}}

**SQL answer:** `SQL_MAIN` in the Code block. `BASE` (two CTEs, `s` and `h`) collapses duplicates with `MIN(is_free)`, so a slot that is both free and busy counts as busy, and computes the hour number `CAST(ROUND(julianday(slot_start) * 24) AS INTEGER)`. `free_to` is the end of the last free hour (`datetime(MAX(slot_start), '+1 hour')`), so `hours` equals the length of the range:
{{SQL:SQL_MAIN}}
The LAG-flag alternative on all rows, `SQL_LAG` (also `BASE`, then `l` and `g`): a row continues a run only when it is free, the previous row is free, and the hour number is exactly one more; otherwise the flag is 1 and a new group starts. Group, filter to free rows, and apply the same `HAVING`:
{{SQL:SQL_LAG}}
`SQL_ROWORDER` in the Code block is the wrong version that numbers rows instead of using the hour number.

**pandas answer:** same logic, identical to the Code block:
{{PD}}

**Example:**
- R1: after dedup, 09:00, 10:00, 11:00 are free (hour numbers h, h+1, h+2), 12:00 is busy, 13:00 and 14:00 are free, 15:00 has no row, 16:00, 17:00, 18:00 are free. Free rows in order get row numbers 1 to 8. Keys `hr - rn`: the first three share one key; 13:00 and 14:00 are the next two rows but their hour numbers jumped by 2 (past the busy 12:00), so the key is larger and shared by those two; 16:00 jumped again (the missing 15:00 row), so the key rises again and is shared by 16, 17, 18. Groups of 3, 2 and 3: ranges 09:00-12:00 (3 hours) and 16:00-19:00 (3 hours); the 2-hour group is dropped.
- With row order instead of hour numbers (`SQL_ROWORDER`) the missing 15:00 row is invisible, 13:00, 14:00, 16:00, 17:00, 18:00 look consecutive and the output shows a bogus 5-hour range starting 13:00.
- R2: 22:00, 23:00, 00:00, 01:00 have consecutive hour numbers across midnight: one range of 4 hours, 22:00 to 02:00 the next day.
- R3 (one slot) and R6 (the 10:00 duplicate resolves to busy, leaving 09:00 alone and 11:00-12:00, a 2-hour group) return nothing.
- R4: exactly 3 free hours, 09:00-12:00: returned, so the threshold is inclusive. The later 2-hour group is dropped.
- R5: the NULL slot is neither free nor busy; `is_free = 1` drops it and the hour numbers jump, so 09:00 alone and 11:00-12:00 (2 hours) both fall short.

**Code:** run with `python3 -I`. The asserts check that the two SQL methods return identical frames and that pandas equals SQL after sorting by `room_id, free_from`. The block also tests how `julianday * 24` behaves, and a few small tables.
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Edge cases:**
- Missing slot row (R1 15:00): it is absent data, not a busy hour; the hour-number key breaks the run, which is the safe choice (an unknown hour must not be reported as free). Row-order keys miss it, as the wrong version shows.
- Busy hour (R1 12:00) also breaks the run because it is filtered out and the hour number jumps. In the LAG version it breaks because `is_free = 1` fails.
- Duplicates: exact duplicates collapse; conflicting duplicates take `MIN(is_free)`, so any busy row wins. If you prefer "any free wins" use `MAX`. SQL `MIN` skips NULLs, so a free row plus a NULL row resolves to free; state that rule.
- NULL `is_free` (R5): not free (it does not equal 1). Decide whether unknown should be treated as busy; this answer does.
- Single-row room, and a room with exactly 2 or 3 free hours: the code ran an empty table, one slot, two slots and exactly three slots; only three returned a row.
- Midnight (R2): the hour number is continuous across the date change; a key built from the date or the hour of day would break.
- Precision: hour number from `julianday` needs `ROUND` before `CAST`. Over 96,432 hourly stamps (2020 to 2030) `CAST(julianday * 24 AS INTEGER)` happened to equal the rounded value every time, and `ROUND(julianday * 24)` minus `unixepoch / 3600` was the same constant for every row. At minute granularity in 2024 (527,040 stamps) truncating `julianday * 1440` differed from the rounded value for 70,272 stamps (the printed counts), although the value itself was never off by more than 0.001 minute. So always `ROUND`, or use integer `unixepoch(slot_start) / 3600`, which is exact.
- Time zones and DST: slot times are assumed to be in one fixed zone; across a DST change a local day has 23 or 25 hours and the hour numbers of local timestamps would repeat or skip (not executed in SQLite; see Q39).

**Then explain:**
- This is the seat-availability problem (Q18) with time instead of seat ids: the number line is the hour number, and a missing or busy hour is a gap in it.
- Filtering before `ROW_NUMBER` is what lets the hour number and the row number advance together; any row that is not free must leave the numbered set.
- The LAG version keeps all rows and flags run boundaries explicitly. It is longer but makes the missing-row check visible (`hr - ph = 1`) and does not depend on filter-then-number ordering; both gave identical rows here.
- `free_to` is exclusive (the end of the last hour), so a range 16:00 to 19:00 means the room is free from 16:00 until 19:00.
- Dialects (not executed here): PostgreSQL would compute the hour number with `EXTRACT(EPOCH FROM slot_start) / 3600` and could use `generate_series` to complete the grid; MySQL uses `UNIX_TIMESTAMP(slot_start) DIV 3600`.

**Follow-ups:**
- Rooms free for at least 3 hours that start on the hour, between 09:00 and 18:00? Add a filter on the hour of day before numbering.
- Find a slot common to two rooms? Intersect the free hour numbers per room first.
- Thirty-minute slots? Use `unixepoch / 1800` as the number.

**Common mistakes:**
- `ROW_NUMBER()` difference on row position, so a missing slot row looks consecutive.
- `CAST(julianday(...) * 24 AS INTEGER)` without `ROUND`.
- Treating NULL as free.
- Using `>= 3` hours but counting rows that include duplicates.
- Forgetting `PARTITION BY room_id`, so runs leak across rooms.
