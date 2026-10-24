**Say this first (1 line):** Clip every shift to the 09:00-18:00 window, drop shifts that become empty, add two zero-length sentinel intervals at 09:00 and 18:00, merge overlaps with a running MAX of the end (new block when the start is strictly greater), and the gaps are the spaces between consecutive merged blocks; covered minutes are the window minus the gap minutes.

**Schema and sample data:** one day, 2024-03-04, window `09:00` to `18:00` (540 minutes). Nine shift rows: g1 starts before the window, g2 overlaps g1, g3 is contained in g2, g4 starts exactly when g2 ends (touching), g5 appears twice (exact duplicate), g6 ends after the window, g7 is entirely before the window, g8 has a NULL end (still on shift, unknown).
{{SCHEMA}}

**SQL answer:** `SQL_MAIN` in the Code block, with the window passed as named parameters `:ws` and `:we`. `clipped` uses SQLite's two-argument scalar `MAX` and `MIN` (a NULL argument would make the result NULL, so rows with NULLs are filtered first); `pieces` adds the sentinels; `ordered` computes the running MAX of the earlier rows' ends with `ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING`, which is NULL for the first row; `merged` groups by the running block id; `nxt` takes `LEAD` of the next block's start:
{{SQL:SQL_MAIN}}
The coverage figures are `SQL_SUMMARY` in the Code block, which wraps `SQL_MAIN` as `g` and subtracts the sum of gap minutes from the window length (with `COALESCE(SUM(minutes), 0)` for the no-gap case):
{{SQL:SQL_SUMMARY}}

**pandas answer:** same logic, identical to the Code block:
{{PD}}

**Example:** after clipping (g7 vanishes, g8 is dropped for the NULL end) the intervals are g1 09:00-11:00, g2 10:00-12:00, g3 11:30-11:45, g4 12:00-13:00, g5 14:00-15:00 (twice), g6 16:00-18:00, plus the sentinels 09:00-09:00 and 18:00-18:00.
- Sorted by start, end: sentinel 09:00, g1 09:00-11:00, g2 10:00-12:00, g3 11:30-11:45, g4 12:00-13:00, g5 14:00, g5 14:00, g6 16:00-18:00, sentinel 18:00.
- Running max of earlier ends: NULL, 09:00, 11:00, 12:00, 12:00, 12:00 (g3 ended 11:45, so the max stays 12:00, a contained interval cannot shrink it), 13:00, 15:00, 18:00 (g6's end).
- New block where start > running max (or NULL): sentinel (first), g1 no (09:00 > 09:00 false), g2 no, g3 no, g4 no (12:00 > 12:00 false, touching merges), g5 yes (14:00 > 13:00), duplicate g5 no, g6 yes (16:00 > 15:00), final sentinel no (18:00 > 18:00 false).
- Merged blocks: 09:00-13:00, 14:00-15:00, 16:00-18:00. Gaps: 13:00-14:00 and 15:00-16:00, 60 minutes each. Uncovered 120, covered 420 of 540 = 77.8 per cent.

**Code:** run with `python3 -I`. The asserts compare the gaps frame (after sorting by `gap_start`) and the summary tuple with SQL; the edge cases run in SQL only except the no-shift case, which also runs in pandas.
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Edge cases:**
- No shifts at all: the sentinels alone form two blocks 09:00-09:00 and 18:00-18:00, so one gap equal to the whole window, 540 minutes, 0 per cent covered (SQL and pandas both returned it). Without the sentinels the query would return nothing for an empty day, which is wrong for a coverage report.
- Shifts only outside the window (06:00-08:30 and 18:00-20:00): after clipping the start is not before the end, so they are dropped and the whole window is one gap.
- One shift covering everything: no gaps, 100 per cent.
- Touching shifts (g2 ends 12:00, g4 starts 12:00): merged because the test is strict `>`. If a hand-over takes a minute of cover you can lose, use `>=` and the touching pair stays two blocks with a zero-minute gap; zero-length gaps are filtered by `gap_end > gap_start` anyway.
- Contained shift (g3): does not shrink the block because the running max keeps 12:00.
- Duplicates (g5 twice): harmless for merging (the duplicate's start is not greater than the max); they do not double the covered minutes because coverage is computed from gaps, not from summing shift lengths.
- NULL end (g8) or NULL start: excluded and stated; if NULL means "still on shift", substitute the window end (`COALESCE(end_ts, :we)`) instead of dropping it, which changes the answer for g8 (17:00 to 18:00 would count as covered).
- The first row's running max is NULL (empty frame), which is why the flag tests `prev_max IS NULL OR st > prev_max`; the frame `ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING` with `MAX` ran on SQLite 3.45.1 here.
- Timestamps are ISO text in one day so string comparison orders correctly; multi-day windows need the day in the window parameters (they have it here) and a partition per day.

**Then explain:**
- Gaps are the complement of the merged union, so the work is: clip, merge, then look between neighbours. The sentinels turn the two open ends of the window into ordinary neighbours so no special case is needed.
- Minutes come from `unixepoch` integer seconds divided by 60: exact for whole minutes, and no floating-point rounding (see the julianday test in Q40).
- Coverage percentage is covered over window length; state the denominator (the window, not the shifts).
- Dialects (not executed here): PostgreSQL would compute minutes with `EXTRACT(EPOCH FROM (b - a)) / 60` and could use range types (`tsrange`) with a union aggregate; MySQL uses `TIMESTAMPDIFF(MINUTE, a, b)`; the clipping uses `GREATEST` and `LEAST` there.

**Follow-ups:**
- Gaps per guard-location or per day? Add the partition key to every window and the day to the join.
- Minimum number of guards at any time (not just one)? That is the +1/-1 sweep of Q17 with a threshold.
- Pages of data too large for a self-contained sort? The same logic scales with an index on `start_ts`.

**Common mistakes:**
- Summing the shift lengths for coverage (double counts overlaps and out-of-window time).
- Merging by comparing with the previous row's end instead of the running max (a contained shift shrinks the block and creates a false gap).
- Forgetting to clip, so a gap before 09:00 appears or the coverage exceeds 100 per cent.
- No sentinels, so the empty day returns no rows.
- Using scalar `MIN`/`MAX` on a NULL end (the result is NULL).
