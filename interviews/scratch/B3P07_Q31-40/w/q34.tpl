**Say this first (1 line):** Both are runs: for zeros, flag `value = 0` and group by the running count of non-zero rows (or subtract two ROW_NUMBERs); for increases, flag `value > LAG(value)` and group by the running count of non-increase rows, so each group is a starting reading followed by its rises; and NULL breaks both because every comparison with NULL is not true.

**Schema and sample data:** sixteen hourly readings on 2024-03-01 (hour 0 to 15). The Code block inserts these rows in reverse order (built from a Python list), so the input is unsorted.
```sql
CREATE TABLE readings(ts TEXT, value INTEGER);
INSERT INTO readings VALUES
 ('2024-03-01 00:00',0),('2024-03-01 01:00',0),('2024-03-01 02:00',3),('2024-03-01 03:00',0),
 ('2024-03-01 04:00',0),('2024-03-01 05:00',0),('2024-03-01 06:00',NULL),('2024-03-01 07:00',0),
 ('2024-03-01 08:00',0),('2024-03-01 09:00',1),('2024-03-01 10:00',2),('2024-03-01 11:00',2),
 ('2024-03-01 12:00',5),('2024-03-01 13:00',6),('2024-03-01 14:00',7),('2024-03-01 15:00',3);
```

**SQL answer:** the three queries are `SQL_ZEROS`, `SQL_ZEROS_FLAG` and `SQL_UP` in the Code block. Zeros by ROW_NUMBER difference (the partition is the 0/1 flag, with `COALESCE` turning a NULL comparison into 0):
{{SQL:SQL_ZEROS}}
Zeros by flag and group:
{{SQL:SQL_ZEROS_FLAG}}
Increasing runs by flag and group. A group starts at every row that is not a rise and holds the following rises, so `COUNT(*)` counts readings (a run of k rises has k + 1 readings), and `HAVING COUNT(*) >= 2` removes groups with no rise at all:
{{SQL:SQL_UP}}

**pandas answer:** same logic, identical to the Code block (`eq(0)` and `gt(shift())` give False for NaN, as the COALESCE does in SQL):
{{PD}}

**Example:** zeros are at hours 0-1, 3-5, 7-8, with a NULL at hour 6.
- Flag-and-group for zeros: the running count of non-zero rows goes up at hour 2 (value 3) and at hour 6 (the NULL counts as non-zero), so hours 0-1 are one group, hours 3-5 another and hours 7-8 a third (each group also holds the non-zero row that opened it, which the `WHERE is_zero = 1` filter removes). The largest group has 3 zero rows, hours 3 to 5. Because the NULL row splits 3-5 from 7-8, the answer is 3; if NULL were ignored they would join into a run of 5.
- Increases: the values 0 (hour 8), 1, 2 rise twice (a run of 3 readings, hours 8-10); hour 11 repeats the value 2, which is not a rise, so a new group starts at hour 11; 2, 5, 6, 7 rise three times, a run of 4 readings from hour 11 to hour 14; hour 15 (value 3) falls. The longest is 4 readings, 11:00 to 14:00. The earlier pair at hours 1-2 (0 then 3) is a run of 2.
- Answer: zeros `03:00` to `05:00` (3 readings); increasing `11:00` to `14:00` (4 readings).

**Code:** run with `python3 -I`. The asserts compare the two SQL zero methods, the pandas results with SQL (tuples of start, end, readings), and nine edge-case tables in SQL and pandas. Ties are broken by the earliest start.
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Edge cases:**
- NULL: breaks a zero run (`0, NULL, 0` gives runs of 1, not 2) and breaks an increasing run (`1, 2, NULL, 3, 4` gives a run of 2, not 4), because `NULL > x`, `x > NULL` and `NULL = 0` are not true. If NULLs are sensor dropouts that should be skipped, filter them out first, but then the run no longer means consecutive readings.
- Equal readings (`4, 4, 4`) are not increases: no increasing run is returned. A repeated value ends a run and starts the next one.
- Single-row table: a lone `0` is a zero run of 1; a lone non-zero or a lone NULL returns no zero run; no table of one reading has an increasing run (I require at least two readings, so it returns nothing).
- Empty table: both queries return no row (checked in SQL and pandas); do not expect a row of zeros.
- Ties between equally long runs (`1, 2, 3` then `0, 5, 6`): `ORDER BY readings DESC, run_start` picks the earliest; say the rule or return all tied runs.
- All-NULL column: pandas receives an object column of `None` from `read_sql_query` and `gt` raised `TypeError` in my first run, so the code casts the column with `astype("float64")` before comparing.
- Timestamps are assumed to be one per time step; a missing hour is not detected. If a missing reading should break a run, add the day-number check from Q40.

**Then explain:**
- Flag-and-group turns "consecutive rows with a property" into a running count of the rows without it; the same pattern covers Q13 (status runs) and Q23 (stock up-streaks).
- The ROW_NUMBER difference needs the two numberings to advance together inside a run: all-rows numbering minus numbering within the partition `value = 0`. It is shorter for equality-based runs but cannot express "greater than the previous row", which depends on a neighbour, so increases use LAG.
- A run of k rises has k + 1 readings; decide whether "length" is rises or readings and state it (I report readings).
- Dialects (not executed here): window functions as written are standard; `COALESCE(value = 0, 0)` relies on SQLite treating a comparison as an integer, while PostgreSQL, as I remember it, wants `CASE WHEN value = 0 THEN 1 ELSE 0 END` because its comparison returns a boolean, not an integer.

**Follow-ups:**
- Longest non-decreasing run? Use `>=` in the flag; equal readings then continue the run.
- All runs of zeros of at least 3 readings? Drop `LIMIT 1` and add `HAVING COUNT(*) >= 3`.
- Per sensor? Add `PARTITION BY sensor_id` to every window and the sensor to the group key.

**Common mistakes:**
- Ignoring NULL and gluing runs across a dropout.
- Counting rises instead of readings (off by one) or the other way round without saying so.
- Using `GROUP BY value` and merging separate zero runs.
- Forgetting the first row has no previous value (`NULL > x` is not a rise, which is right, but write it explicitly).
- Assuming `value > LAG(value)` is a valid integer in every dialect.
