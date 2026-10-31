**Say this first (1 line):** Build a calendar of working days only (weekdays minus holidays), number it 1, 2, 3, ..., join attendance to it, and use `working_day_number - ROW_NUMBER()` as the island key, so Friday to Monday is consecutive and a holiday is simply a day that has no number.

**Schema and sample data:** one month of calendar (a recursive CTE builds it inside the query), one holiday (Thursday 2024-03-14), six employees. Rows are inserted unsorted, E1 has a duplicate day, and the last two rows are a NULL employee and a NULL date.
{{SCHEMA}}

**SQL answer:** `SQL_MAIN` in the Code block. The calendar is a date spine (a recursive CTE, pointer to Part 9 for the mechanics) filtered to weekdays with `strftime('%w', d) NOT IN ('0','6')` (0 is Sunday, 6 is Saturday) and `NOT EXISTS` against `holidays`; `ROW_NUMBER()` over what is left gives `wd_no`.
{{SQL:SQL_MAIN}}
`CAL_CTE` is the `WITH RECURSIVE ...` prefix shown in the Code block (spine, `cal`, deduplicated `a`, and `j`, which joins attendance to the calendar and numbers each employee's attended working days). The calendar-day contrast is `SQL_CALDAY`: the same island query on raw dates with `julianday(work_date) - rn`.

**pandas answer:** same logic, identical to the Code block:
{{PD}}

**Example:** working-day numbers around the holiday (from the printed calendar): Wed 6 Mar = 4, Thu 7 = 5, Fri 8 = 6, Mon 11 = 7, Tue 12 = 8, Wed 13 = 9, Fri 15 = 10 (Thu 14 is a holiday, so it has no number), Mon 18 = 11.
- E1 attended 7, 8, 11, 12, 13, 15 March (plus a duplicate 8 March that `DISTINCT` removes). Their numbers are 5, 6, 7, 8, 9, 10 and the row numbers are 1 to 6, so `wd_no - rn` is 4 for all six: one streak of 6 working days from 7 to 15 March. The weekend and the holiday did not break it.
- On raw calendar days the same employee splits into 7-8 (2 days), 11-13 (3 days) and 15 (1 day), because the weekend and the holiday are gaps in the date line.
- E2 attended 4, 5, 7, 8 March: numbers 2, 3, 5, 6 (Wed 6 March, number 4, is a working day E2 did not attend), so the key `wd_no - rn` goes from 1 to 2 at the missing Wednesday: two streaks of 2.
- E4 attended Fri 8 and Tue 12: numbers 6 and 8 (Monday 11 is number 7 and was skipped), so two streaks of 1. Friday then Tuesday is not consecutive.
- E5 attended Wed 13, Thu 14 (holiday), Fri 15 and Sat 16. The holiday and the Saturday rows find no calendar row and drop out in the inner join, leaving 13 and 15 (numbers 9 and 10): one streak of 2. The calendar-day version reports 4 days.

**Code:** run with `python3 -I`. The assert compares the pandas frame with the SQL frame after both are sorted by `emp_id, streak_start`.
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Edge cases:**
- Duplicates: E1's repeated 8 March row would give two row numbers to one day and split the run, so the attendance is `SELECT DISTINCT` first.
- NULLs: a NULL `emp_id` or `work_date` is dropped in the `WHERE`. A NULL date would otherwise never match the calendar anyway (the inner join drops it), but a NULL employee would form its own group. A NULL in `holidays` breaks `NOT IN` (every comparison becomes NULL, so no day passes and the calendar goes empty; a probe of `'2024-03-04' NOT IN (SELECT '2024-03-14' UNION ALL SELECT NULL)` returned NULL); `NOT EXISTS` is immune, and the run with a NULL holiday inserted returned the same 8 rows.
- Single-row groups: E3 and E6 each get a streak of 1.
- Attendance on a non-working day (E5's holiday and Saturday rows): this answer drops them. If those days should count (someone really worked), add them to the calendar as working days or build the calendar from "weekday or attended", and say so.
- Exact threshold: Friday to Monday differs by one working-day number, so it continues; Friday to Tuesday differs by two, so it breaks (E4).
- Unsorted input is harmless because every window orders explicitly.
- The calendar must cover the attendance range (here March 2024); dates outside it silently disappear. Generate the spine from `MIN` and `MAX` of the data in production.

**Then explain:**
- The island trick needs a gap-free number line. Calendar days are that line only for a seven-day business. For a five-day business with holidays the line is the working-day calendar, so you number the working days yourself instead of using `julianday`.
- A holiday in the middle is treated as if it did not exist: it has no number, so the days on either side are neighbours. This is a policy choice (nobody can be absent on a holiday). If the business wants a holiday to break a streak, give it a number (do not exclude it from the calendar) and then an employee who skipped it has a gap.
- Holidays that fall on a weekend are removed twice, which is harmless.
- Dialects (not executed here): PostgreSQL would use `generate_series` for the spine and `EXTRACT(ISODOW FROM d) < 6`; MySQL 8 uses a recursive CTE and `WEEKDAY(d) < 5`. In `strftime('%w')` Sunday is 0 in SQLite.
- Per-employee or per-country holiday calendars are the same query with the calendar keyed by region.

**Follow-ups:**
- Longest working-day streak per employee? Reduce the islands as in Q7.
- Current streak as of a date? Q15 logic on the working-day numbers: the island whose end is the last working day on or before the as-of date.
- Half-days or shift workers? Then the calendar is per employee (a roster table) and the same numbering applies to that roster.

**Common mistakes:**
- Using `julianday(work_date) - ROW_NUMBER()` and reporting a Friday-Monday run as two streaks (shown: E1 splits into three).
- Keeping holidays in the calendar and then expecting them to be skipped.
- Joining attendance with a LEFT JOIN, which creates NULL day numbers for attendance on non-working days and a NULL group.
- Forgetting `DISTINCT`, or numbering the calendar before filtering out weekends.
- Using `NOT IN` against a holiday table that can contain NULL.
