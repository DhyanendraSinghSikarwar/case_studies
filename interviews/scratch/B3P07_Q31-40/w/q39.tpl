**Say this first (1 line):** A streak needs a definition of "day", so first convert each UTC timestamp to the calendar day you agreed on (IST is UTC plus 330 minutes, applied with `date(login_ts_utc, '+330 minutes')`), deduplicate to one row per user per day, and only then use the day-number minus ROW_NUMBER key; the same data can merge or split streaks depending on that choice.

**Schema and sample data:** timestamps are UTC ISO text (`YYYY-MM-DD HH:MM:SS`). U1 has a login at 20:00 UTC on 5 March, which is 01:30 on 6 March in IST. U2 straddles the IST midnight exactly (18:29:59 and 18:30:00 UTC). U3 has two logins on one UTC day that fall on different IST days. U4 has a single login. U5 has a NULL and a malformed timestamp. Rows are unsorted.
{{SCHEMA}}

**SQL answer:** one query, `SQL_MAIN` in the Code block, run twice with a bound parameter `:shift` of `'+330 minutes'` (IST) and `'+0 minutes'` (UTC). It converts, drops rows where `date()` returns NULL (a NULL or unparseable timestamp), deduplicates days, and uses `unixepoch(day) / 86400` (an integer day number) minus `ROW_NUMBER()` as the key:
{{SQL:SQL_MAIN}}

**pandas answer:** same logic, identical to the Code block (`errors="coerce"` turns a bad timestamp into NaT, which `dropna` removes, matching the SQL `IS NOT NULL` filter):
{{PD}}

**Example:**
- U1: UTC logins on 3, 4, 5 and 7 March (the 5 March one at 20:00). UTC days 3, 4, 5, 7 give streaks 3-5 (3 days) and 7 (1 day). In IST the 20:00 UTC login is 01:30 on 6 March, so the IST days are 3, 4, 6, 7: streaks 3-4 and 6-7 (2 days each). Same four logins, one 3-day streak became two 2-day streaks: the 5 March login moved to 6 March, leaving 5 March empty and gluing it to 7 March instead.
- U2: 18:29:59 UTC on 4 March is 23:59:59 IST on 4 March; 18:30:00 UTC on 5 March is 00:00:00 IST on 6 March. UTC days 4 and 5: one 2-day streak. IST days 4 and 6: two streaks of 1 day. One second of difference at the boundary decides it.
- U3: logins 10:00 and 19:00 UTC on 4 March and 10:00 on 6 March (twice). UTC days 4 and 6: two streaks. 19:00 UTC is 00:30 IST on 5 March, so IST days are 4, 5, 6: one 3-day streak. Here IST merges what UTC splits.
- U5: the NULL and the malformed text give `date()` NULL and are dropped; one valid login remains.

**Code:** run with `python3 -I`. The asserts compare the pandas frames with the SQL frames for both IST and UTC after sorting by `user_id, streak_start`. The DST part is pandas only.
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Edge cases:**
- Boundary second: 18:30:00 UTC is the first instant of the next IST day (U2); an `end < 18:30:00` style filter on UTC is the same boundary.
- Duplicate days: two logins on one IST day (U3's 6 March) are collapsed by `DISTINCT` on the converted day; the duplicate would otherwise split the streak.
- NULL and malformed timestamps: `date(NULL, ...)` and `date('not a timestamp', ...)` both return NULL in SQLite, so the filter on `IS NOT NULL` is what keeps them out; a NULL group would otherwise appear. Strings like `2024-03-05T20:00:00Z` are also accepted by `datetime()` in this version (my check returned `2024-03-06 01:30:00`).
- Single-row user (U4) and unsorted insertion are handled.
- The day number uses `unixepoch(day) / 86400` (integer seconds, whole days) instead of `julianday`, so there are no floating-point day numbers.

**Then explain:**
- India has no daylight saving, so a fixed offset of +5:30 is exact all year. A zone with DST (New York, London, Berlin) is not a fixed offset: the same UTC instant maps to different local days depending on the date. SQLite has no time zone database, so the fixed-modifier approach is wrong there; do not run it on a DST zone. In pandas I did run a demonstration (above): 04:30 UTC on 11 March 2024 is 00:30 EDT on 11 March in `America/New_York`, whereas a fixed UTC-5 offset gives 23:30 on 10 March, a different day; and the local day of 10 March 2024 is 23 hours long. In SQL engines with zone support, convert with `AT TIME ZONE` in PostgreSQL or `CONVERT_TZ` in MySQL (not executed here, from memory) and store the zone, not the offset.
- Which day is it? Agree with the product team: the user's local day, the company's reporting day (often IST or UTC), or a rolling 24 hours. A user who travels changes local day; a fixed reporting zone is simplest and reproducible. Whatever the choice, compute it once in a conformed `login_day` column.
- Streak length differs between definitions, so any dashboard comparing streaks across time zones must use the same definition.
- Storing UTC and converting at query time keeps the raw data unambiguous; storing local time loses the instant at the DST hour that happens twice.

**Follow-ups:**
- Streak by each user's own zone? Join to a users table with a stored `tz_offset_minutes`, valid only for fixed-offset zones; for DST zones convert in the warehouse with real zone rules.
- Month or year boundaries? Day arithmetic through `unixepoch` handles them; string arithmetic does not (Q6).
- How do you test the boundary? Keep fixture rows at 18:29:59 and 18:30:00 UTC, as U2 does.

**Common mistakes:**
- Using `date(login_ts_utc)` for an Indian audience and calling it daily activity.
- Applying a fixed offset to a DST zone.
- Forgetting to deduplicate after the conversion (two UTC days can collapse onto one local day, or one UTC day can fall on two).
- Converting inside the key but grouping on the raw UTC day.
- Not agreeing the definition of a day before comparing numbers.
