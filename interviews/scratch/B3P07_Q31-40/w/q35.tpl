**Say this first (1 line):** Keep games with `points >= 30`, deduplicate, and group by `game_no - ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY game_no)`; keep groups with at least 3 games; the key uses `game_no`, not row position, so a missing game number ends the streak.

**Schema and sample data:** eight players, 33 rows, inserted unsorted. P1 has two streaks (one of 3 and one of 4 games, split by a 10-point game). P2 has no game 4. P3 has one game. P4 has 29, 30, 31. P5 scores exactly 30 three times. P6 has a NULL in game 2. P7 has game 2 twice. P8 has a 4-game streak tying P1's longest.
{{SCHEMA}}

**SQL answer:** `SQL_MAIN` in the Code block:
{{SQL:SQL_MAIN}}
The longest-streak player is `SQL_LONGEST`, which wraps `SQL_MAIN` as `s` and keeps rows where `length = (SELECT MAX(length) FROM s)`, so ties are all returned:
{{SQL:SQL_LONGEST}}
The comparison queries in the Code block are `SQL_ROWORDER` (row order instead of `game_no`), `SQL_NODEDUP` (no `DISTINCT`) and `SQL_GT30` (`> 30`).

**pandas answer:** same logic, identical to the Code block:
{{PD}}

**Example:**
- P1 games 1-8 have points 35, 30, 41, 10, 32, 33, 34, 36. Game 4 (10 points) is filtered out. Hot games are 1, 2, 3, 5, 6, 7, 8 with row numbers 1 to 7, so `game_no - rn` is 0 for games 1-3 and 1 for games 5-8: streak 1-3 (3 games, average (35 + 30 + 41) / 3 = 35.33) and streak 5-8 (4 games, average (32 + 33 + 34 + 36) / 4 = 33.75).
- P2 has games 1, 2, 3, 5, 6, all 40 points. Keys: 1 - 1 = 0, 0, 0, then 5 - 4 = 1, 1. Streak 1-3 (3 games) and 5-6 (2 games, below 3, discarded). Using row position instead (`SQL_ROWORDER`) merges them into one 5-game streak 1-6, which is wrong because game 4 is missing.
- P5 has exactly 30 points three times, so with `>= 30` it is a 3-game streak; with `> 30` it vanishes.
- P6: game 2 has NULL points, `NULL >= 30` is not true, so it is dropped and games 3-5 form a streak of 3 (game 1 is alone).
- P7 has game 2 twice. After `DISTINCT` it is one streak 1-3. Without `DISTINCT` the key sequence is 0, 0, -1, -1 and the run splits into two pairs, so P7 disappears.
- P1 (last streak 4) and P8 (1-4, 4 games) tie for the longest: both are returned.

**Code:** run with `python3 -I`. The asserts compare the pandas streak table and the longest-streak table with SQL after sorting by `player_id, start_game`.
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Edge cases:**
- Exactly 30: included by `>=`; the question says "at least 30", so the boundary belongs inside (P5, and game 2 of P1). Using `>` dropped P5 from the result in my run (the players left were P1, P2, P6, P7, P8); P1 also loses its 1-3 streak by the same logic, but keeps its 5-8 streak.
- Missing `game_no` (P2): only the `game_no`-based key splits there. A row-order key (`rn_all - rn_hot`, which is what you get when you number rows and then compare with a second ROW_NUMBER) merges across the hole. If the numbering can have gaps for a reason that should not break a streak (a game with no data), say so and use row order deliberately.
- Duplicate `game_no` (P7): dedupe first. Two rows for one game with different points would need a rule (take the max, or reject), which SQL cannot guess.
- NULL points (P6): not hot; this ends the streak, which is the safe reading ("unknown" is not 30 or more).
- Single-row player (P3) and a player whose longest streak is 2 (P4, 30 and 31): no output row.
- Ties for longest: `SQL_LONGEST` returns every tied player. `LIMIT 1` would pick one arbitrarily unless you add a tie-break.
- Players with no hot streak do not appear at all; if the output must list all players, `LEFT JOIN` from a players table.
- Unsorted input is fine because the window orders by `game_no`.

**Then explain:**
- A streak is a property of consecutive game numbers, so the key must be built from the numbers: the difference `game_no - rn` is constant exactly when `game_no` grows by one with each hot row.
- Filter first (`WHERE points >= 30`), then number: the numbering must run along the hot rows only.
- `HAVING COUNT(*) >= 3` turns islands into streaks; the length threshold is a parameter.
- Dialects (not executed here): the same SQL runs on PostgreSQL and MySQL 8; MySQL 5.7 has no window functions.

**Follow-ups:**
- Longest streak per player only? Rank streaks per player (Part 4 style) and keep rank 1.
- Different threshold (at least 4 games)? Change the `HAVING`.
- Current hot streak? Q15 logic on game numbers.

**Common mistakes:**
- `points > 30`.
- `ROW_NUMBER() OVER (ORDER BY game_no)` without `PARTITION BY player_id`, so keys leak across players.
- Using row position instead of `game_no` (shown: P2 becomes a 5-game streak).
- Not deduplicating (shown: P7 vanishes).
- Taking `MAX(length)` in a plain `GROUP BY`, which loses the start and end.
