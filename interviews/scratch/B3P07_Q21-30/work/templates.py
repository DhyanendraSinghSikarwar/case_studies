T[21] = r'''
**Say this first (1 line):** Dedupe to one row per user and date, number each user's dates, subtract the number from the date to get an island key, group by user AND key to get one row per streak, then aggregate those streak rows per user (count, average, max, count of length at least 3).

**Schema and sample data:** fifteen login rows for five users, inserted out of date order on purpose. User 1 has dates 1, 2, 3, 5, 7, 8 January (streaks of 3, 1 and 2 days). User 2 has 1, 2, 3 January with 3 January duplicated. User 3 has a single login. User 4 has four consecutive days. User 5 has only a NULL date. Users 1 and 2 both start on 1 January, so they get the same island key, which is the trap.
@@SCHEMA@@

**SQL answer:** `SQL_MAIN` in the Code block. The island CTE `isl` has one row per (user, streak); the final SELECT is a plain GROUP BY on that CTE. Date arithmetic uses `date(login_date, '-' || rn || ' days')`, which yields an ISO date as the key.
@@SQL@@

**pandas answer:** identical logic, shown once here and the same text as in the Code block:
@@PD@@

**Example:** sorted and deduplicated, user 1 has dates 01, 02, 03, 05, 07, 08 with row numbers 1 to 6. Date minus row number gives 2023-12-31, 2023-12-31, 2023-12-31, 2024-01-01, 2024-01-02, 2024-01-02. Three distinct keys mean three streaks of lengths 3, 1 and 2, so streaks = 3, average = 6/3 = 2.0, longest = 3, streaks of at least 3 days = 1. User 2 (after dropping the duplicate) is 01, 02, 03 with a single key, so one streak of 3. User 3 has one row, key 2024-01-09, one streak of length 1, average 1.0, longest 1, zero long streaks. User 4 is one streak of 4. User 5 has no usable date, so no row at all.

**Code:** run with `python3 -I`. The assert compares the SQL and pandas frames after sorting both by `user_id`. The last query checks day-number arithmetic over a recursive-CTE date spine.
@@CODE@@

**Output (my run):**
@@OUT@@

**Edge cases:**
- Wrong answer 1, island grouped by key only: the key `2023-12-31` is produced by both user 1 and user 2, so grouping by key alone merges them into one 6-day island with `users_merged = 2` in my run. The key is only unique inside a user, so the user must be in the GROUP BY (and in the PARTITION BY of the ROW_NUMBER).
- Wrong answer 2, `COUNT(DISTINCT island_key)` over all users: 5 in my run, but the real number of (user, streak) pairs is 6, because the shared key is counted once. Per user it happens to be correct only when you also `GROUP BY user_id`.
- Wrong answer 3, no dedupe: user 2's duplicated 3 January takes row numbers 3 and 4, so its key moves by one day and the 3-day streak is counted as two keys (2 in my run instead of 1). `SELECT DISTINCT user_id, login_date` first, or use DENSE_RANK on the date.
- Single login (user 3): one island, `streaks = 1`, average 1.0, longest 1, `streaks_3plus = 0`. The window functions need no special case.
- NULL dates: user 5 vanishes from the result. If every user must appear (with 0 streaks), LEFT JOIN from a users table and wrap the counts in COALESCE.
- Unsorted input is harmless because both ROW_NUMBER and pandas `sort_values` order by date first.
- The streak definition is consecutive calendar days with at least one login each; I assume dates are plain days with no time zone shift.
- Day numbers: over a recursive-CTE date spine of 39,979 consecutive days (1900-01-01 to 2009-06-16) `julianday(d) - rn`, `CAST(julianday(d) AS INTEGER) - rn` and `date(d, '-' || rn || ' days')` each produced exactly one distinct key. Date-only values give half-integer Julian day numbers, which floats store exactly, so the subtraction is safe for dates. For timestamps with a time of day it is not (see Q25); take the date part first.

**Then explain:**
- A run of consecutive days has date and row number rising together, so their difference is constant inside a run and jumps when a day is skipped.
- Build the island CTE once and aggregate it twice (per island, then per user) instead of nesting subqueries; that is what "from one island CTE" means.
- Average streak length is the average of per-streak lengths (2.0 for user 1), not total logins divided by days.
- `SUM(len >= 3)` works in SQLite because a comparison returns 0 or 1. `COUNT(*) FILTER (WHERE len >= 3)` also runs on SQLite 3.45 (I ran a probe), and PostgreSQL accepts it too (not executed here); MySQL has no FILTER, so the portable form is `SUM(CASE WHEN len >= 3 THEN 1 ELSE 0 END)`. PostgreSQL also allows `login_date - rn::int` on a DATE, and MySQL uses `DATE_SUB(login_date, INTERVAL rn DAY)` (not executed here).
- The 'at least N' filter is the pattern of Q9 (LeetCode 1454); the general-N follow-up only changes the threshold.

**Follow-ups:**
- Current streak (the island that contains the as-of date)? Filter islands by `end_date = as_of`, as in Q15.
- Longest streak per user with the dates? Add MIN and MAX of login_date to the island CTE (Q7). Duplicates debugging is Q8.
- Users with no logins? LEFT JOIN from users and COALESCE to 0.

**Common mistakes:**
- Forgetting `PARTITION BY user_id` in ROW_NUMBER, so row numbers run across users.
- Grouping islands by the key alone (shown: 6-day island merging two users).
- Not deduplicating (user, date) pairs.
- Using `COUNT(DISTINCT key)` as the streak count without the user in the grouping.
- Using `RANK` on dates, which leaves gaps when dates tie.
'''

T[22] = r'''
**Say this first (1 line):** Order each player's matches by day, keep a running count of non-wins (a draw, a loss or an unknown result), so every win in the same streak shares one count; count wins per (player, running count), take the max per player, and LEFT JOIN from the list of players with COALESCE to 0.

**Schema and sample data:** seventeen match rows, five players, one player per interesting case. Player 1: W, W, W, Draw, W (longest 3). Player 2: only losses (0). Player 3: inserted out of order, sorted it is W, L, W, W, W, W, with a large calendar gap before the last win (longest 4; the streak is about consecutive matches, not consecutive days). Player 4: a single win. Player 5: Win, NULL result, Win. I assume `(player_id, match_day)` is unique, as in the LeetCode statement.
@@SCHEMA@@

**SQL answer:** `SQL_MAIN` in the Code block is the running count of non-wins method. `SQL_RN` is the two ROW_NUMBER method (a row number over all of a player's matches minus a row number inside the player's matches of the same result).
@@SQL@@
`SQL_RN` in the Code block replaces the running count with `ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY match_day) - ROW_NUMBER() OVER (PARTITION BY player_id, result ORDER BY match_day)` and groups the `result = 'Win'` rows by that difference.

**pandas answer:** same logic as the first method, identical to the Code block:
@@PD@@

**Example:** player 3 sorted: 03-01 W, 03-02 L, 03-04 W, 03-05 W, 03-06 W, 03-30 W. Non-wins so far: 0, 1, 1, 1, 1, 1. Wins with count 0: one (03-01). Wins with count 1: four (03-04, 03-05, 03-06, 03-30), so the longest is 4. Player 1: wins at counts 0, 0, 0 (three wins), the draw makes the count 1, and the last win has count 1 alone, so 3. Player 2 has no win rows, so it vanishes from the streak CTE and only the LEFT JOIN plus COALESCE brings it back as 0. By the two row number method for player 3: row number over all matches 1..6, row number among wins 1, 2, 3, 4, 5 for the five wins, differences 0 for the first win and 1, 1, 1, 1 for the four others (rows 3, 4, 5, 6 minus 2, 3, 4, 5), the same split.

**Code:** run with `python3 -I`. Both SQL methods are asserted equal, then pandas is asserted equal to SQL after sorting both by `player_id`.
@@CODE@@

**Output (my run):**
@@OUT@@

**Edge cases:**
- Players with no wins (player 2) disappear from any query that filters to wins. The INNER JOIN style (`SQL_INNER`) printed four rows in my run and lost player 2. LEFT JOIN from the players plus `COALESCE(MAX(streak_len), 0)` keeps the 0. There is no players table in the LeetCode statement, so I derive it with `SELECT DISTINCT player_id FROM matches`; a player with no matches at all is not in the data and cannot be returned.
- NULL result (player 5): with `result IS NOT 'Win'` the NULL counts as a streak breaker and the longest streak is 1. With `result <> 'Win'` the comparison is NULL, the SUM ignores it, the NULL row does not break the streak and the answer wrongly shows 2 (my run). State the rule: an unknown result is not a win.
- Ties on `match_day` for one player make the order arbitrary and the answer can change; the LeetCode problem guarantees unique days, otherwise add a match id to the ORDER BY.
- Unsorted input is fine; both methods order inside the window.
- A single-row player (player 4) gives streak 1 with a win and 0 with anything else.
- Gaps in calendar days do not break a streak here (player 3). If days without a match should break it, that is a different problem (add a calendar-day check as in Q6).

**Then explain:**
- A running count of non-wins is a streak label: it stays constant while wins continue and increments on each break.
- The two ROW_NUMBER difference only works if the compared rows are sorted the same way; here both use `match_day`, once over everything and once inside a result. Row numbers inside the 'Draw' or 'Lose' partitions are computed too but filtered away.
- The running count method needs one window and tolerates several result values naturally, which is why I prefer it; the two row number method generalises to "runs of the same result" when you drop the `WHERE result = 'Win'` filter.
- `SUM(result IS NOT 'Win')` relies on SQLite booleans being 0 or 1. The portable form is `SUM(CASE WHEN result = 'Win' THEN 0 ELSE 1 END)`. `IS NOT` with a string works in SQLite; PostgreSQL would use `IS DISTINCT FROM 'Win'` (not executed here).
- The LeetCode 2173 page returned HTTP 403 for Wave A, so the statement is as known from mirrors; I did not check the exact output order.

**Follow-ups:**
- Longest losing streak or longest streak of any result? Drop the filter and group by result too.
- Also return the start and end days? Add MIN and MAX of `match_day` to the streak CTE.
- Current winning streak? Take the streak that contains the player's latest match.

**Common mistakes:**
- INNER JOIN or filtering wins and losing the players without wins.
- Using `<>` and silently letting NULL results extend a streak.
- Subtracting row numbers that are not partitioned by player.
- Counting calendar days instead of matches.
- Taking `MAX(non_wins_so_far)` as the streak length instead of counting wins per group.
'''

T[23] = r'''
**Say this first (1 line):** Order by day, flag a row as up only when `close > LAG(close)`, so a flat day, a drop, a NULL close and the first row all get 0, then label streaks with the running count of non-up rows and aggregate the up rows per label; calendar gaps do not matter because consecutive rows, not consecutive dates, define the sequence.

**Schema and sample data:** fifteen trading-day rows inserted partly out of order, ISO dates, `close` REAL. Rows jump from Friday to Monday (03-08 to 03-11, 03-15 to 03-18, 03-22 ends the data). 03-11 is flat (104 after 104), 03-13 is NULL, 03-20 is a drop. Rules I assume: a day is up only when its close and the previous row's close are both non-NULL and strictly higher; the day after a NULL close cannot be judged, so it is not up. The alternative (carry the last known close forward) is mentioned below.
@@SCHEMA@@

**SQL answer:** `SQL_MAIN` in the Code block (it is the CTE chain `FLAGS` followed by the final SELECT). The streak length is the number of up days; the `start_day` is the first rising day, so the closing price on the day before it is the base.
@@SQL@@
`SQL_LONGEST` (Code block) returns the longest run and keeps all ties by comparing to `MAX(up_days)`.

**pandas answer:** identical to the Code block:
@@PD@@

**Example:** flags per row from the run: 03-04 first row (no previous, up 0), 03-05 to 03-08 up (101, 102, 103, 104 each above the previous), 03-11 flat so 0, 03-12 up (105 above 104), 03-13 NULL so 0, 03-14 follows the NULL so 0, 03-15 to 03-19 up (106, 107, 108 each above the previous: three days; 03-18 and 03-19 are Monday and Tuesday after the weekend), 03-20 down 0, 03-21 and 03-22 up. The running count of non-up rows (grp) is 1 for the first block, 2 for 03-11 and 03-12, 3 for 03-13, 4 for 03-14 to 03-19 and 5 from 03-20. Up rows grouped by grp: 4 days (03-05 to 03-08), 1 day (03-12), 3 days (03-15 to 03-19), 2 days (03-21 to 03-22). At least 3 days gives the first and third; the longest is the first with 4 up days (five closes).

**Code:** run with `python3 -I`. The assert compares the SQL and pandas streaks of at least 3 after sorting by `start_day`.
@@CODE@@

**Output (my run):**
@@OUT@@

**Edge cases:**
- Flat day: `close > prev` is false, so a flat day ends the streak (03-11 in the data). If your business rule says flat does not break a streak ("non-decreasing"), use `>=` and say so.
- NULL close: the comparison is NULL, the CASE falls to ELSE 0, and the next row also compares against NULL so it is 0 too (03-13 and 03-14 both 0). The streak resumes only at 03-15. Forward-filling the last known close would change that; I did not do it, and `LAST_VALUE(close IGNORE NULLS)` is a syntax error in SQLite 3.45.1 (I ran it); other engines support it (not executed here).
- Weekends: the table has one row per trading day, so Friday and Monday are adjacent rows and LAG compares them. A `julianday` difference of 1 would wrongly split every weekend; do not add it here. If the table could miss real trading days (a data gap), that is a data-quality question, not part of this streak definition.
- Exact duplicate rows: after inserting a second `2024-03-06,102` row, the duplicate compares as flat against the original, which breaks the first streak (only the 03-15 streak survives in my run). Deduplicate by day first (`SELECT DISTINCT`, or the latest row per day).
- Ties for the longest: `SQL_LONGEST` returns all of them; `ORDER BY ... LIMIT 1` would silently pick one.
- Single-row table: no up days, no streaks (0 rows in my run). Unsorted input is fine because LAG and the running count sort by day.
- pandas: `shift()` on an integer column upcasts to float64 (int64 to float64 in my run; `fill_value=0` kept int64). A comparison against NaN is False, which matches the SQL NULL rule here.

**Then explain:**
- `LAG(close)` gives the previous row, so up/non-up is a per-row flag; `SUM(1 - up)` counts non-up rows so far, which is constant over a run of up rows.
- The grouping label counts breaks, not days; the up rows of one label are exactly one streak, and the break row itself shares its label with the up rows that follow it (so filter `up = 1` before aggregating).
- The streak is measured in rising days; if you want the number of closes involved, add one and start from the previous day.
- Dialects (not executed here): `IGNORE NULLS` exists in some engines (Oracle, BigQuery, Snowflake as I remember it); the SQL above avoids it.

**Follow-ups:**
- Down-streaks or flat-streaks? Change the flag; the pattern is identical.
- Include the base day in start and end? Take the previous row's day with `LAG(day)` for the first up day.
- Per ticker? Add `ticker` to PARTITION BY and to the GROUP BY.

**Common mistakes:**
- Using `julianday(day) - julianday(prev_day) = 1` and splitting every weekend.
- Treating NULL as 0 or as 'not changed' and letting a streak span a missing close.
- Forgetting to filter `up = 1` before counting, so the break row is counted in the next streak.
- `LIMIT 1` for the longest streak without a tie rule.
- Not removing duplicate rows per day.
'''

T[24] = r'''
**Say this first (1 line):** Turn the reset flag into a group key with a running SUM of `is_reset` (every reset row starts a new group, including itself), then take a running SUM of `amount` partitioned by account and that key; a rule that resets when the running total crosses a threshold depends on its own earlier output, so it needs a recursive CTE (Part 9) or a loop, not one window pass.

**Schema and sample data:** thirteen rows for three accounts, inserted out of order for account 1. Account 1: txn 1 to 7 with resets at txn 4 and txn 6. Account 2: a single row that is itself a reset. Account 3: has NULL amounts (txn 2 and 5) and a NULL `is_reset` (txn 3), and a reset at txn 4. For running total mechanics (frames, ROWS versus RANGE, ties) see Part 5; this question only adds the group key.
@@SCHEMA@@

**SQL answer:** `SQL_MAIN` in the Code block. The first window builds `grp`; the second restarts at each new `(acct_id, grp)`. A window function cannot sit inside another window's PARTITION BY (SQLite raised `misuse of window function SUM()` when I tried), so `grp` has to come from a CTE. `COALESCE` makes NULL amounts and NULL flags count as 0.
@@SQL@@

**pandas answer:** identical to the Code block:
@@PD@@

**Example:** account 1 sorted by txn_id: amounts 10, 20, 30, 5(reset), 7, 8(reset), 1. Running SUM of `is_reset` gives grp 0, 0, 0, 1, 1, 2, 2. Running totals inside each group: 10, 30, 60 | 5, 12 | 8, 9. The reset row restarts with its own amount (5, not 0 and not 65). Account 2: one row, grp 1, total 50. Account 3: amounts 9, NULL, 4, 6(reset), NULL with a NULL flag at txn 3 treated as 0: grp 0, 0, 0, 1, 1; totals 9, 9 (NULL counted as 0), 13, 6, 6.

**Code:** run with `python3 -I`. The assert compares `acct_id, txn_id, grp, running_since_reset` after ordering both by `acct_id, txn_id`. The end of the script runs the threshold variant as a plain loop to show why it is different.
@@CODE@@

**Output (my run):**
@@OUT@@

**Edge cases:**
- A reset row belongs to the new group, so it starts with its own amount. If instead the total should restart after the reset row, shift the key by one row (`SUM(is_reset) OVER (... ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING)`); not run here.
- Rows before the first reset form group 0, and a reset row first in an account (account 2) starts group 1 with no group 0.
- NULL `is_reset`: SUM ignores it, so it is the same as 0 unless wrapped in COALESCE (here wrapped). NULL amount: `SUM(amount)` ignores the NULL in the total, but a row sequence of only NULLs returns NULL in SQLite (the check printed `None`). I wrapped amounts in COALESCE so the output is a number.
- pandas difference: `groupby().cumsum()` on a raw NaN amount returns NaN on that row (account 3, txn 2 and 5 in my run), while SQL SUM returns the total so far. Filling with 0 first makes them match, which is what the main answer does.
- Ties in `txn_id` make the order and therefore the totals undefined; the window needs a unique ordering. I assume `txn_id` is unique per account.
- Single-row account: group key and total are the row itself (account 2). Unsorted input is fine because both windows order by `txn_id`.
- ROWS versus the default RANGE frame only matters with ties; I spell out ROWS.

**Then explain:**
- The key counts resets seen so far, so every row between two resets has the same key; this is the same running-count idea as islands, applied to flags instead of date gaps.
- The threshold variant (reset when the running total exceeds a limit) cannot be written as one SUM window, because whether a row resets depends on the total after the previous reset, which is the output you are computing. In my loop with limit 100 over 40, 30, 50, 10, 60, 20, 90 the totals are 40, 70, 120, 10, 70, 90, 180, while a plain running total is 40, 70, 120, 130, 190, 210, 300. Use a recursive CTE that carries the running total row by row; that answer is in Part 9, I only point to it here.
- Dialects (not executed here): the same two-window form works in PostgreSQL, MySQL 8, BigQuery and Snowflake; MySQL 5.7 has no window functions.

**Follow-ups:**
- Reset by threshold? Recursive CTE or a procedural loop (Part 9).
- Reset by calendar month? Replace the key with `strftime('%Y-%m', date)`; no running SUM needed.
- Cap the running total instead of resetting it? Also state-dependent, same answer as the threshold variant.

**Common mistakes:**
- Putting the group-key window and the total window in one SELECT (not allowed; use a CTE).
- Starting the new group on the row after the reset flag.
- Forgetting COALESCE when `is_reset` or `amount` can be NULL.
- Believing one window pass can reset on a threshold.
- Partitioning by the group key only, without the account.
'''

T[25] = r'''
**Say this first (1 line):** I assume a gap of more than 30 minutes starts a new session (convention A, exactly 30 minutes stays in the session); I flag new sessions with LAG, number them with a running SUM, aggregate to one row per session, and assign each session to the date of its first event, so a 23:50 to 00:20 session counts once, on its start day; I also show convention B (`>=`, exactly 30 minutes starts a new session).

**Schema and sample data:** sixteen event rows inserted out of order. User 1: 09:00, 09:10, 09:40 (a gap of exactly 30 minutes between 09:10 and 09:40) and a separate 15:00 event. User 2: 23:50 on 1 March, then 00:05 and 00:20 on 2 March (the midnight crossing), then 10:00 on 2 March. User 3: two events at the identical timestamp 12:00:00 plus 12:20. User 4: one event. User 5: a NULL timestamp (dropped) and one real event. User 6: 10:00 and 10:30:01 (one second over the threshold). Timestamps are ISO text in one time zone.
@@SCHEMA@@

**SQL answer:** `SQL_A` in the Code block (convention A). `SQL_B` is the same text with `>=` instead of `>` on the line `t - LAG(t) ... > 1800`. Seconds come from `unixepoch()`, not `julianday()`.
@@SQL@@

**pandas answer:** the Code block defines `sessions_pandas(events, ge)`; its body is identical to this text (`ge=False` is convention A, `ge=True` is B):
@@PD@@

**Example:** convention A. User 1: 09:00, 09:10, 09:40 are chained by gaps of 10 and 30 minutes (30 is not greater than 30), so session 1 has 3 events; 15:00 is 5 h 20 min later, session 2 has 1 event. Day 2024-03-01: 2 sessions, average (3+1)/2 = 2.0, bounce sessions 1. Convention B: the 30-minute gap starts a new session, so sessions are {09:00, 09:10}, {09:40}, {15:00}: 3 sessions, average 4/3 = 1.33, 2 bounces. User 2: gaps are 15, 15 minutes, so 23:50, 00:05, 00:20 form one session of 3 events that starts on 1 March, so 2024-03-01 gets 1 session with 3 events and 0 bounces, and the 10:00 event on 2 March is a separate bounce session dated 2024-03-02. Counting events by the event date instead would put 1 event on 1 March and 3 on 2 March, which is wrong for sessions.

**Code:** run with `python3 -I`. Both conventions are computed in SQL and pandas; the asserts compare each pair after sorting by `user_id, day`.
@@CODE@@

**Output (my run):**
@@OUT@@

**Edge cases:**
- Exactly 30 minutes (user 1): convention A gives 2 sessions, convention B gives 3 for the same data, so the choice changes the answer. Dataiku's tutorial uses `>=`, other guides use `>`; there is no standard, so state yours. A gap of 30 minutes and 1 second (user 6) starts a new session under both.
- Midnight crossing (user 2): the session belongs to the date of its start (`date(MIN(event_ts))`); it is one session, not two. A session spanning two days is not split by this rule; splitting at midnight is a different requirement.
- Same timestamp (user 3): the two 12:00:00 events have a gap of 0 and stay in one session regardless of their order, so the session count and size are stable. The order within the tie only matters if you pick the first event name; add an event id to the ORDER BY then.
- NULL `event_ts` (user 5): filtered out before LAG; otherwise NULL would sort first and break the gap arithmetic. User 5 still has one real event, so one bounce session.
- Single event (user 4): LAG is NULL, the first-row test flags it as a session start, and it is a bounce session. A bounce is a session with exactly one event, so a user with two events at the same timestamp is not a bounce.
- Unsorted input is fine, SQL and pandas both sort by time.
- julianday versus unixepoch: I generated 20,001 pairs exactly 30 minutes apart (one `+30 minutes` from a spread of timestamps). `(julianday(b) - julianday(a)) * 1440` was greater than 30 in 13,333 pairs, less than 30 in 6,668 and equal to 30 in none, while `unixepoch(b) - unixepoch(a) = 1800` held in all 20,001. A threshold test with julianday would therefore misclassify the exact-30-minute case in either direction; use integer seconds.
- Time zones: SQLite does no zone conversion here; daylight saving transitions are not modelled (not tested).

**Then explain:**
- Sessionization is three steps: flag (LAG gap above the timeout), label (running SUM of flags per user), aggregate (one row per session). Day-level metrics come from the session rows, so a session is dated once.
- Average events per session is the average of per-session counts, not events divided by days.
- `SUM(n_events = 1)` counts bounce sessions in SQLite; `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` is the portable form.
- Dialects (not executed here): PostgreSQL would use `EXTRACT(EPOCH FROM ts)` or `ts - LAG(ts) > INTERVAL '30 minutes'`; MySQL `TIMESTAMPDIFF(SECOND, prev, ts)`; BigQuery `TIMESTAMP_DIFF`.

**Follow-ups:**
- Session duration? `MAX(t) - MIN(t)` per session (Q11 and Q12 cover the session id and the boundary).
- Daily active users based on session start? `COUNT(DISTINCT user_id)` on the session start dates.
- Session split at midnight? Add `date(event_ts)` to the PARTITION BY of the flag and label windows.

**Common mistakes:**
- Using `julianday` float arithmetic for the threshold.
- Assigning a session to the date of each event so one session appears on two days.
- Not stating the `>` versus `>=` convention.
- Not filtering NULL timestamps.
- Counting a user as a bounce user rather than a bounce session.
'''

T[26] = r'''
**Say this first (1 line):** Compare each event to the previous event of the same user with `LAG(event_name)` and keep the row when `event_name IS NOT prev_name` (or it is the user's first row); `DISTINCT` and `GROUP BY event_name` remove repeats everywhere, not only back-to-back, so A, A, B, A would become A, B.

**Schema and sample data:** I add an `event_id` to the stated columns as the tie-breaker (without one, same-timestamp rows have no defined order). Fourteen rows, inserted out of order. User 1: A, A, B, A, A, A by time (ids 1 to 6, id 6 inserted first). User 2: single row. User 3: B, B, C all at the same timestamp, ordered by id. User 4: NULL, NULL, A, NULL names.
@@SCHEMA@@

**SQL answer:** `SQL_MAIN` in the Code block. `rn = 1` is the guard that keeps a user's first row even if its name is NULL (`NULL IS NOT NULL` is false).
@@SQL@@

**pandas answer:** identical to the Code block:
@@PD@@

**Example:** user 1 by time: A(1), A(2), B(3), A(4), A(5), A(6). Previous names: none, A, A, B, A, A. Event 1 is first, event 2 equals its previous A (dropped), event 3 is B after A (kept), event 4 is A after B (kept), events 5 and 6 repeat A (dropped). Kept A, B, A, which is the required result and the second A is kept because it follows B. `SELECT DISTINCT user_id, event_name` gives only A and B for user 1. User 3: B(8) is first, B(9) repeats, C(10) differs, so B and C are kept. User 4: NULL(11) is kept by the first-row guard, NULL(12) repeats a NULL and is dropped, A(13) is kept, NULL(14) after A is kept.

**Code:** run with `python3 -I`. The assert compares SQL and pandas after ordering both by `user_id, event_ts, event_id`.
@@CODE@@

**Output (my run):**
@@OUT@@

**Edge cases:**
- NULL event names: `!=` against a NULL is NULL, so the row is dropped (`SQL_NEQ` lost user 1's first row, user 2's only row and every NULL row in my run). `IS NOT` is NULL-safe. Without the `rn = 1` guard a user's first row is lost when its name is NULL (user 4's first NULL event disappeared in `SQL_NOGUARD`).
- pandas: `s.ne(s.shift())` treats NaN as different from NaN, so a run of NULL names is not collapsed (user 4 kept ids 11, 12, 13, 14 instead of 11, 13, 14 in my run). The main answer therefore adds `| (isna & isna)` to the equality test and a separate first-row test.
- Ties on `event_ts` (user 3): ordering needs the extra column; the result for B, B, C depends on `event_id`. Without it, which row is first is arbitrary.
- Single-row user: kept by the first-row rule. Unsorted input is fine because both versions sort by time and id first.
- Exact duplicates (same user, time and name twice) are removed as repeats of the previous row, which is the intended behaviour here.
- A resend that is not adjacent (A, B, A) is deliberately kept; if you must drop resends within a time window instead, that is a different rule (compare timestamps too).

**Then explain:**
- Keeping the first of each run is "keep the rows that start a run", the same idea as island starts. `DISTINCT` asks "which names occurred", not "which rows changed".
- `GROUP BY user_id, event_name` with `MIN(event_ts)` also collapses the second A; it answers a first-occurrence question.
- `IS NOT` is NULL-safe in SQLite; `IS DISTINCT FROM` is the standard spelling (it also runs in SQLite 3.45.1, see Q27); PostgreSQL has `IS DISTINCT FROM` but, as I remember it, not a general `IS NOT` for non-boolean values, and MySQL uses `NOT (a <=> b)` (not executed here).
- The pandas version uses `groupby("user_id")["event_name"].shift()` so previous values never cross users.

**Follow-ups:**
- Keep the last of each run instead? Compare with `LEAD`.
- Collapse runs into one row with a count and the first and last time? Use the run key (running SUM of the change flag) and aggregate; see Q13.
- Only drop repeats within 5 seconds? Add a timestamp-gap condition to the keep test.

**Common mistakes:**
- `SELECT DISTINCT` or `GROUP BY event_name` (loses the second A).
- `!=` instead of `IS NOT` (drops first rows and NULL rows).
- Missing the first-row guard.
- No tie-breaker in the ORDER BY.
- In pandas, `shift()` without a groupby, so one user's last event is compared to the next user's first.
'''

T[27] = r'''
**Say this first (1 line):** Use `LAG(state)` per device and keep the rows where the state differs with a NULL-safe test (`IS NOT`, or `IS DISTINCT FROM` which SQLite 3.45.1 also accepts) plus each device's first row; `!=` silently drops every row touching a NULL, and in pandas `!=` goes the opposite way because NaN != NaN is True, so every NaN row looks like a new run.

**Schema and sample data:** twelve rows, four devices, inserted out of order for device 1. Device 1: on, on, off, on, off (three transitions after the first row). Device 2: NULL, NULL, on, NULL, on. Device 3: a single row. Device 4: a single NULL row. A run is a maximal sequence of consecutive rows with the same state, and I treat NULL as a state of its own ("unknown"), so consecutive NULLs form one run. The transition rows and the run starts are the same set of rows, so one query answers both.
@@SCHEMA@@

**SQL answer:** `SQL_MAIN` in the Code block. `SQL_DISTINCT_FROM` replaces `state IS NOT prev_state` with `state IS DISTINCT FROM prev_state` and gives the same rows (asserted).
@@SQL@@

**pandas answer:** identical to the Code block:
@@PD@@

**Example:** device 1 by time: on, on, off, on, off. Previous states: none, on, on, off, on. Rows kept: the first (on), 00:02 (on to off), 00:03 (off to on), 00:04 (on to off); 00:01 repeats on and is dropped. Device 2: NULL (first row, kept), NULL (same unknown state, dropped), on (kept, NULL to on), NULL (kept, on to NULL), on (kept, NULL to on). Device 3 and 4 each keep their one row. With `!=` only device 1's three transitions survive: the first rows have a NULL previous state and every comparison with NULL is NULL.

**Code:** run with `python3 -I`. The assert compares SQL and pandas after ordering both by `device_id, ts`. The extra lines check `IS DISTINCT FROM`, NaN comparisons, groupby with NaN keys and `itertools.groupby` on NaN.
@@CODE@@

**Output (my run):**
@@OUT@@

**Edge cases:**
- NULL on either side: `NULL != x` and `NULL != NULL` are both NULL, so a WHERE clause drops those rows. The probe printed `(None, 0, 0, 1)` for `NULL != NULL`, `NULL IS NOT NULL`, `NULL IS DISTINCT FROM NULL` and `1 IS NOT NULL`.
- First row of each device (devices 3 and 4): LAG returns NULL, so a plain `IS NOT` would drop a first row whose state is NULL (device 4); the `rn = 1` guard keeps it. Whether the first row counts as a transition is a choice; the `kind` column separates 'first row' from 'transition'.
- pandas NaN: `np.nan != np.nan` is True and `Series.ne` returned `[True]`, so the naive `s.ne(s.shift())` kept 5 rows for device 2 instead of 4 (my run). The main answer uses `ne(prev) & ~(both NaN)`.
- pandas `groupby("state")` drops NaN keys by default (counts of 'off' 3 and 'on' 5 only, 8 of 12 rows); `dropna=False` keeps the NaN group (4 rows). A run-length count by state would otherwise lose the NULL runs.
- `itertools.groupby` run lengths: three NaN values of the same object `np.nan` gave one run of 3 (the identity shortcut), but three separate float objects or `Series.tolist()` values gave runs of 1, 1, 1 in my run. Do not rely on it for NaN; map NaN to a sentinel first.
- Duplicate timestamps within a device make the order ambiguous; add an id to the ORDER BY. Unsorted input is fine, both versions sort first.
- Time gaps between rows are ignored; only consecutive rows are compared.

**Then explain:**
- `IS NOT` (a SQLite spelling that works on any values) and `IS DISTINCT FROM` (the SQL standard form, runs in SQLite 3.45.1) are the NULL-safe inequality. PostgreSQL supports `IS DISTINCT FROM` and MySQL uses `NOT (a <=> b)` as I remember it; I did not run those.
- A transition row is by definition the first row of a new run, so "transitions" and "run starts" are one result.
- pandas and SQL disagree on NaN/NULL: SQL says unknown, pandas says unequal. Always decide what NULL means (a state of its own, or missing data to skip) before choosing the comparison.
- If NULL means "missing reading, carry on with the last state", forward-fill first (`ffill()` in pandas; SQLite has no `IGNORE NULLS`).

**Follow-ups:**
- Duration of each run? Add a run key and use `MAX(ts) - MIN(ts)`, or LEAD of the start rows.
- Count transitions per device? `COUNT(*) - 1` of the start rows, or sum the change flag.
- Treat NULL as missing? Forward-fill, then compare.

**Common mistakes:**
- `WHERE state != prev_state`, which drops the first row and every row next to a NULL.
- pandas `s != s.shift()` for runs of NaN, which makes every NaN row a new run.
- `groupby("state")` without `dropna=False`, which silently drops the NULL group.
- `shift()` across devices because the `groupby` was left out.
- Assuming `itertools.groupby` collapses NaNs.
'''

T[28] = r'''
**Say this first (1 line):** Sort by room and start, compute the running maximum end of all earlier bookings in the room (`groupby("room_id")["end_ts"].cummax()` then shifted by one), start a new block when the start is strictly greater than that maximum, cumsum the flags into a block key, and aggregate min start and max end; strict `>` means touching intervals merge, and the running maximum (not just the previous end) is what keeps a contained interval from shrinking the block.

**Schema and sample data:** thirteen rows, inserted out of order, `TEXT` timestamps in one format so text order equals time order. Room 1: 09:00-12:00 contains 10:00-11:00; 11:30-12:30 overlaps the first; 12:30-12:45 touches it (starts exactly at 12:30); 13:00-14:00 is separate; 16:00-17:00 appears twice (exact duplicate). Room 2: 09:00-10:00 and 10:00-11:00 touch; 11:01-12:00 is one minute later. Room 3: a single booking. Room 4: a booking with a NULL end (open-ended) and one normal booking.
@@SCHEMA@@

**SQL answer:** `SQL_MAIN` in the Code block. Spelled out: running MAX of `end_ts` over all earlier rows, a flag, a running SUM of the flag, then min and max per block. `ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING` ran on SQLite 3.45.1 and returns NULL for each room's first row, which the flag treats as a new block.
@@SQL@@

**pandas answer:** identical to the body of `merge_pandas` in the Code block:
@@PD@@

**Example:** room 1 sorted by start then end: 09:00-12:00, 10:00-11:00, 11:30-12:30, 12:30-12:45, 13:00-14:00, 16:00-17:00, 16:00-17:00. Previous maximum end: none, 12:00, 12:00, 12:30, 12:45, 14:00, 17:00. Start versus previous maximum: first row is new; 10:00 not greater than 12:00 (merge, contained); 11:30 not greater than 12:00 (merge); 12:30 is not strictly greater than 12:30 (merge, touching); 13:00 is greater than 12:45 (new); 16:00 is greater than 14:00 (new); the duplicate 16:00 is not greater than 17:00 (merge). Blocks: 09:00-12:45 (4 bookings), 13:00-14:00, 16:00-17:00 (2 bookings). Room 2: 10:00 equals the previous end 10:00 so it merges (09:00-11:00); 11:01 is later than 11:00 so it stays separate.

**Code:** run with `python3 -I`. The assert compares SQL and pandas after ordering both by `room_id, start_ts`. The script also prints the touching-stays-separate variant, the wrong LAG version and the checks for `cummax` in groupby and sort stability.
@@CODE@@

**Output (my run):**
@@OUT@@

**Edge cases:**
- Touching intervals: the strict `>` merges them (room 2 gives 09:00-11:00). With `>=` they stay separate (room 2 printed three rows). Pick one rule and say it; for rooms an end time normally equals the next start (half-open), so many schedulers want them separate.
- Contained interval: 10:00-11:00 inside 09:00-12:00 must not pull the end back. Using `LAG(end_ts)` (the previous row's end only) made the block end at 12:00 instead of 12:45 and split room 1 in two wrong blocks in my run; the running maximum fixes it.
- Exact duplicates (room 1, 16:00-17:00 twice) merge into one block with `n_merged = 2`.
- NULL `end_ts` (room 4): I filter those rows out in both versions, so room 4's open booking disappears and only its normal booking is returned. Without the filter, `MAX` ignores NULL and `start > NULL` is NULL, which would merge the open booking with the next one by accident. An open end needs an explicit rule (for example an as-of date or infinity).
- Single-row room: the shifted maximum is NaT or NULL, so the flag is 1 and the room returns its booking.
- Unsorted input: the sort puts bookings in order; ties on start are broken by end for a deterministic order. The pandas default `sort_values` on one key with ties is not guaranteed stable: on 2000 random rows with ties, `sort_values("k")` did not equal `kind="stable"` (False in my run), whereas sorting on two keys `["k", "i"]` matched the stable order (True). I sort on all three columns so no tie is left to chance.
- `groupby().cummax()` on datetimes keeps `datetime64` (the dtype printed `datetime64[us]`), and `shift()` fills each group's first row with NaT (one NaT in the two-row check).
- Timestamps as text work in SQL only because the format is fixed; mixed formats or time zones break the text comparison.

**Then explain:**
- The block starts when the next booking starts after everything seen so far has ended. That is the running maximum, not the previous row.
- `cummax` then `shift` equals SQL's `MAX(...) ... AND 1 PRECEDING`: the maximum of all earlier rows, excluding the current one.
- The key is a running count of block starts, the same idea as islands (date minus row number is not needed because ranges are compared explicitly).
- Dialects (not executed here): the running MAX window works in PostgreSQL, MySQL 8, BigQuery and Snowflake as I remember it; the oneuptime article I read shows ClickHouse syntax for the same idea. Dates would use `DATE` columns.

**Follow-ups:**
- Merge ranges with inclusive end dates (Q16)? Compare `start > date(prev_max_end, '+1 day')` to also merge adjacent days.
- Total booked time per room after merging? Sum the block lengths, which avoids double counting overlaps.
- Free time between blocks? The gap is block start minus the previous block end (Q37 covers coverage gaps).

**Common mistakes:**
- Comparing to the previous row's end instead of the running maximum (contained intervals shrink the block).
- Using `>=` and merging or not merging touching intervals without saying so.
- Not sorting by start (and end) before `cummax`.
- Running `cummax` without `groupby("room_id")`, so rooms leak into each other.
- Leaving NULL ends in the data.
'''

T[29] = r'''
**Say this first (1 line):** Turn each session into two events, +1 at login and -1 at logout, sort them by time with the -1 events first at equal times, take a running sum (the number of open sessions after each event), then the max of the running sum is the peak and the earliest time it equals the peak is when it first happens; sorting by time alone leaves the order of tied events to chance.

**Schema and sample data:** seven sessions, inserted out of order, half-open intervals [login, logout): a session that ends at 10:00 is not open at 10:00 for a session starting at 10:00. Users 1 and 7 both log in at 09:00 and out at 10:00 (an identical duplicate), user 2 is 09:30 to 10:30, user 3 is 10:00 to 11:00, user 4 is 10:00 to 10:15, so at 10:00 two sessions end and two start while one stays open. User 5 has a NULL logout and an as-of time of 12:30 (fixed, not today). User 6 is a zero-length session at 13:00.
@@SCHEMA@@

**SQL answer:** `SQL_MAIN` in the Code block. The window uses `ORDER BY ts, delta` so a -1 comes before a +1 at the same timestamp.
@@SQL@@

**pandas answer:** the body of `peak_pandas` in the Code block (default arguments are the correct ordering):
@@PD@@

**Example:** events in order (ends before starts at 10:00): 09:00 +1 (1), 09:00 +1 (2), 09:30 +1 (3), 10:00 -1 (2), 10:00 -1 (1), 10:00 +1 (2), 10:00 +1 (3), 10:15 -1 (2), 10:30 -1 (1), 11:00 -1 (0), 12:00 +1 (1), 12:30 -1 for the open session (0), 13:00 -1 then +1 for the zero-length one (-1 then 0). The maximum is 3, first reached at 09:30 (and again at 10:00 after the tie). If starts were placed before ends at 10:00 the sum would reach 3 + 2 = 5 before the ends are applied, which is wrong: sessions that end exactly at 10:00 are not open together with those that start at 10:00.

**Code:** run with `python3 -I`. The assert compares the SQL and pandas results (peak and first time; scalar pair, no row order). The remaining lines run the tie variants.
@@CODE@@

**Output (my run):**
@@OUT@@

**Edge cases:**
- Ties at one timestamp: with `ORDER BY ts, delta DESC` (starts first) SQL returned a peak of 5 at 10:00, and `ORDER BY ts` with a ROWS frame also returned 5 in my run, which is arbitrary tie order and not guaranteed. With a RANGE frame and `ORDER BY ts` ties are netted together (3 at 09:30), which is correct here but only because the frame treats equal timestamps as one group.
- pandas: sorting by `ts` only with `kind="stable"` keeps the concatenation order, so concatenating starts first gave 5 and ends first gave 3. The default `sort_values` kind on one key also gave 5 in this run, which is not a guarantee either way (see Q28 for the stability test). Sorting by `["ts", "delta"]` gave 3 for both concatenation orders.
- NULL logout (user 5): `COALESCE` to the fixed as-of time; without it the -1 event would have a NULL time (sorted first in SQLite) and the sum would be wrong. NaT would not sort the same way in pandas (`sort_values` puts NaT last by default), so fill it.
- Zero-length session (user 6): the -1 sorts before its +1, so the running sum dips to -1 for an instant (visible in the trace); the peak is unaffected. Remove zero-length sessions first if the dip matters.
- Duplicate sessions (users 1 and 7) count twice, as they should if they are two sessions.
- Single session: peak 1, first reached at its login (checked on one row in the script). Unsorted input is fine since the events are sorted.
- First time reached: `MIN(ts)` among events whose running sum equals the peak. If the peak is reached again later, only the first is reported.

**Then explain:**
- The running sum after an event is the number of open sessions at that moment; the max over events is the peak because the count only changes at events.
- Convention: half-open intervals (end excluded) are why -1 goes first; with closed intervals (a logout at 10:00 still counts at 10:00) the order would flip. State it.
- Equal-timestamp events form a group; the count inside that group is not meaningful, only the count after the whole group.
- `pd.concat` keeps the frame order, which matters for ties; `ignore_index=True` avoids duplicate index labels.
- The self-join alternative counts sessions overlapping each login and is O(n squared) (Q17 has the SQL version in this part).

**Follow-ups:**
- Peak per day or per room? Add the key to PARTITION BY (SQL) or groupby (pandas).
- All times when the count equals the peak? Return every row whose running sum equals the max.
- Count of concurrent sessions at a given instant? `COUNT(*) WHERE login <= t AND (logout IS NULL OR logout > t)`.

**Common mistakes:**
- Sorting by time only and letting ties decide the peak.
- Putting starts before ends for half-open intervals (peak overstated, 5 instead of 3 in the data).
- Forgetting `ignore_index=True` after `concat`.
- Leaving NULL logouts unfilled.
- Reporting the last, not the first, time the peak is reached.
'''

T[30] = r'''
**Say this first (1 line):** Two bookings in the same room overlap when `a.start < b.end AND b.start < a.end` (half-open intervals, so one ending exactly when the other starts is not a conflict), and `a.booking_id < b.booking_id` keeps each unordered pair once and drops the pairing of a booking with itself.

**Schema and sample data:** nine bookings inserted out of order. Room 1: booking 1 is 09:00-11:00; booking 2 is 11:00-12:00 (starts exactly when 1 ends); booking 3 is 09:30-10:00 (inside booking 1); booking 4 is 10:30-11:30 (overlaps both 1 and 2); booking 5 is 12:00-13:00 (starts exactly when 2 ends); booking 9 has a NULL end. Room 2: bookings 6 and 7 are identical 09:00-10:00. Room 3: a single booking. A second table `stays` uses inclusive end dates: stay 1 is 1 to 3 March, stay 2 is 3 to 5 March (they share the night of the 3rd), stay 3 is 6 to 7 March.
@@SCHEMA@@

**SQL answer:** `SQL_MAIN` in the Code block.
@@SQL@@

**pandas answer:** identical to the Code block (a merge on `room_id` is the self join):
@@PD@@

**Example:** pairs in room 1 with `a.id < b.id`. (1, 2): 09:00 < 12:00 is true, but 11:00 < 11:00 is false, so touching is not a conflict. (1, 3): 09:00 < 10:00 and 09:30 < 11:00, a conflict (3 is inside 1). (1, 4): 09:00 < 11:30 and 10:30 < 11:00, a conflict. (2, 4): 11:00 < 11:30 and 10:30 < 12:00, a conflict. (2, 5): 11:00 < 13:00 but 12:00 < 12:00 is false, not a conflict. (3, 4): 09:30 < 11:30 but 10:30 < 10:00 is false. Room 2: (6, 7) are identical, 09:00 < 10:00 both ways, a conflict. Booking 9 has a NULL end, so every comparison with it is NULL and it never matches. Result: (1,3), (1,4), (2,4), (6,7).

**Code:** run with `python3 -I`. The assert compares SQL and pandas after ordering both by `booking_a, booking_b`.
@@CODE@@

**Output (my run):**
@@OUT@@

**Edge cases:**
- Why `a.booking_id < b.booking_id`: without it the join pairs every booking with itself (always overlapping itself) and returns each real conflict twice, once as (a, b) and once as (b, a): 16 rows in my run (8 self pairs plus 4 conflicts in both directions) instead of 4. `<>` would remove self pairs but still return mirrored pairs.
- Why the half-open test is the right one: `a.start < b.end AND b.start < a.end` is the negation of "a ends before b starts or b ends before a starts" when an end is exclusive. It covers partial overlap, containment (booking 3 inside booking 1) and identical intervals in one condition, with no case analysis.
- Touching (booking 1 ends at 11:00, booking 2 starts at 11:00): not a conflict under half-open. The inclusive `<=` test (`SQL_INCLUSIVE_TS`) turned it into a conflict, and also added (2, 5), in my run.
- Inclusive end dates (`stays`): stay 1 covers 3 March and stay 2 starts on 3 March, so they conflict, and the inclusive test `a.start <= b.end AND b.start <= a.end` finds (1, 2). The half-open test returned no rows, so it misses that conflict. A safe habit is to normalise to half-open: `date(end_date, '+1 day')` as the exclusive end, which returned (1, 2) as well. State which convention the table uses.
- Duplicates: identical bookings (6 and 7) conflict; identical `booking_id` values would make `<` skip them, so the id must be unique.
- NULL end (booking 9): never returned, in SQL (NULL comparison) and in pandas (NaT comparison is False). If an open booking should conflict with everything after its start, use `COALESCE(end_ts, '9999-12-31')`.
- Single booking room (room 3): no pairs. Unsorted input does not matter, a join has no order.
- Performance: the self join is quadratic within each room; an index on `(room_id, start_ts)` helps, and a running-MAX window finds whether any conflict exists without listing pairs (not benchmarked here).

**Then explain:**
- Overlap is easier to reason about as the opposite of "disjoint": two intervals are disjoint when one ends before (or when, for half-open) the other starts.
- The id condition is a de-duplication of unordered pairs; it is the same trick as `a.id < b.id` in other self joins.
- With timestamps, half-open is the norm; with whole days written as inclusive start and end dates, the inclusive form is natural. The two forms must not be mixed.
- Dialects (not executed here): PostgreSQL has range types with `&&` and exclusion constraints that can prevent conflicts at insert time; MySQL and SQL Server need the explicit test.

**Follow-ups:**
- Only list bookings that conflict with at least one other? `EXISTS` with the same condition.
- Prevent conflicts at insert time? A constraint or a locking check, not a query (engine specific).
- Merge the conflicting bookings into blocks? See Q28 and Q16.

**Common mistakes:**
- Omitting the id condition and getting self pairs and mirrored pairs.
- Using `<=` for timestamp intervals so back-to-back bookings conflict.
- Using the half-open test on inclusive end dates and missing conflicts that share a day.
- Writing only one of the two comparisons, which misses containment or partial overlaps.
- Forgetting `a.room_id = b.room_id`.
'''
