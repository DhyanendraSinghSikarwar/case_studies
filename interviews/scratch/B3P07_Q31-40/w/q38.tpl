**Say this first (1 line):** The same island logic behaves differently in SQL and pandas in five places, and I ran a tiny reproduction of each: duplicates break the row-number key in both, NULL comparisons are NULL in SQL but `NaN != NaN` is True in pandas, `shift` turns integers into floats, tied sort keys have no guaranteed order unless you add a second key or `kind='stable'`, and `groupby` drops NaN keys where `GROUP BY` keeps NULL.

**Schema and sample data:** five small tables created inside the Code block, one per row of the table below (a `logins` table with a duplicate day, a four-row `st` state table with NULLs, a `tie` table, a `g` table with NULL keys, and in-memory pandas Series for the rest). The data is shown with each demonstration.
```sql
CREATE TABLE logins(user_id TEXT, login_date TEXT);
INSERT INTO logins VALUES ('u','2024-03-01'),('u','2024-03-02'),('u','2024-03-02'),('u','2024-03-03');
CREATE TABLE st(ts INTEGER, state TEXT);
INSERT INTO st VALUES (1,'up'),(2,NULL),(3,NULL),(4,'up');
CREATE TABLE tie(ts INTEGER, ev INTEGER);
INSERT INTO tie VALUES (1,2),(1,1),(1,3);
CREATE TABLE g(k TEXT, v INTEGER);
INSERT INTO g VALUES ('a',1),(NULL,2),('a',3),(NULL,4);
```

**SQL answer:** the SQL for each row is in the Code block; the island query used in row 1 is `SQL_ISLANDS` (with `{src}` replaced by `logins` or by `(SELECT DISTINCT login_date FROM logins)`):
{{SQL:SQL_ISLANDS}}
The translation table (every row was run; the output is below):

| Topic | SQL (SQLite 3.45.1) | pandas 3.0.5 | What I saw |
|---|---|---|---|
| Duplicate dates | `date - ROW_NUMBER()` splits the run (two islands of 2 days instead of one of 3); `DISTINCT` first | same with `cumcount` as the row number; `drop_duplicates()` first | both split into two islands raw, one island of 3 days after dedup |
| NULL / NaN in a `!=` run flag | `NULL != 1` and `NULL != NULL` are NULL; `IS NOT` is NULL-safe (`NULL IS NOT NULL` is 0); `IS DISTINCT FROM` also works on 3.45.1 | `np.nan != np.nan` is True; `x != x.shift()` is True on every NaN row; nullable `Int64` with `pd.NA` gives `<NA>` | with `<>` the transition into NULL was lost and a spurious start appeared; `IS NOT` gave 1, 2, 4 |
| Shift / LAG | `LAG` gives NULL for the first row; SQLite does not change column types | `shift()` makes integers float64 (NaN), datetimes get `NaT`; `fill_value=0` keeps int64; `diff().dt.days` gives floats | float64 versus int64 shown |
| Ties in the ordering column | `ORDER BY ts` with ties has no specified order; add `, ev` | `sort_values` default kind is `quicksort`, not stable; `kind='stable'` or a second key makes the order deterministic | on 2,000 rows with 5 distinct keys the default order differed from the stable order; a second key matched |
| NULL / NaN group keys | `GROUP BY k` keeps one NULL group (sum 6) | `groupby('k')` drops NaN keys (only `a` remains); `dropna=False` keeps them | shown |

**pandas answer:** the pandas side of each row is in the Code block; there is no single pandas query. The reusable pieces are the island key `day_number - cumcount()`, the NaN-safe run flag `(x != x.shift())` replaced by `(x != x.shift()) & ~(x.isna() & x.shift().isna())` when NaN should equal NaN, `shift(fill_value=...)`, `sort_values(..., kind="stable")` or a second key, and `groupby(..., dropna=False)`.

**Example:** walk the five rows with the tiny data.
- Duplicates: `u` has 1, 2, 2, 3 March. Row numbers 1, 2, 3, 4, day numbers D, D+1, D+1, D+2, so the keys are D-1, D-1, D-2, D-2: two islands of 2 rows (1-2 March and 2-3 March). After `DISTINCT` the rows are 1, 2, 3 March with keys D-1 for all: one island of 3 days.
- NULL: `st` has up, NULL, NULL, up. With `LAG(state)`: previous values are NULL, up, NULL, NULL. Test "first row or `state <> previous`": ts 1 (previous NULL, first) yes; ts 2 (`NULL <> 'up'` is NULL) no; ts 3 (previous NULL) yes (it is accepted as a first row by mistake); ts 4 (previous NULL) yes. Result 1, 3, 4. The NULL-safe `state IS NOT previous`: ts 1 (`'up' IS NOT NULL` true), ts 2 (`NULL IS NOT 'up'` true), ts 3 (`NULL IS NOT NULL` false), ts 4 (`'up' IS NOT NULL` true). Result 1, 2, 4, which are the true run starts.
- Shift: `[1, 2, 3].shift()` is `[NaN, 1.0, 2.0]` (float64); with `fill_value=0` it is `[0, 1, 2]` (int64).
- Ties: three rows with the same ts have no promised order in SQL, so add `ev` to the `ORDER BY`; in pandas a small input came back in original order (`a, b, c`) (I did not investigate why; short inputs may take a different code path inside NumPy), but 2,000 rows with five distinct keys did not match the stable order. The default `kind` in the signature is `quicksort`.
- Groups: `g` has keys a, NULL, a, NULL. SQL gives groups NULL (6) and a (4); pandas default gives only a (4).

**Code:** run with `python3 -I`. Most claims in the table are asserted; the 2,000-row sort-order result (which depends on the NumPy build), the nullable-`Int64` output and the `.dt.days` values are only printed.
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Edge cases:**
- Tie order: the unstable default is observed behaviour on this machine's pandas 3.0.5 and NumPy build for 2,000 rows; it is not a documented promise either way for other sizes or builds, so the safe habit is an explicit stable sort or a unique second key.
- `diff()` on datetimes gives a `Timedelta` with NaT on the first row; `.dt.days` of NaT is NaN, so a comparison `== 1` is False for the first row, which is the desired "first row starts a streak".
- A nullable `Int64` column avoids the float upcast but then `pd.NA` makes comparisons `<NA>`, and I printed that `<NA>` result only; I did not test it as a boolean mask.
- Group order: SQL `ORDER BY k` put the NULL group first in SQLite in my run; with `dropna=False` the NaN key sits in its own group in the dictionary printed above.
- Not executed here, from memory: PostgreSQL puts NULLs last in an ascending `ORDER BY` where SQLite puts them first; `IS DISTINCT FROM` is the SQL-standard NULL-safe test, while `IS NOT` between two values is SQLite syntax and MySQL spells it `<=>`.

**Then explain:**
- SQL is three-valued: NULL comparisons give NULL and a `WHERE` or `CASE WHEN` treats NULL as false. pandas follows IEEE floating point: NaN compared with anything, including itself, is unequal, so `!=` is True. The same flag expression therefore gives different run starts on the same data.
- Neither engine promises an order for ties unless told; pandas happens to be stable on tiny inputs, which hides the bug in tests.
- The type upcast is the quiet one: integer IDs or days that go through `shift` become floats, so a join or an equality against an integer column can fail later; use `fill_value`, `Int64` or cast back.
- The fix list: dedupe before the key, NULL-safe comparisons (`IS NOT` or explicit `isna` tests), `fill_value`, a tie-breaker column, `dropna=False`.

**Follow-ups:**
- Which row is most dangerous in production? Duplicates and ties, because the code runs without errors and the numbers are just wrong.
- Other differences worth checking? How each engine treats NULL or NaN inside aggregates; test it with a fixture rather than assume.
- How would you test it? Put a duplicate, a NULL, a tie and a single-row group into the fixture, as this answer does.

**Common mistakes:**
- Assuming `NaN != NaN` is False, or `NULL != NULL` is true.
- Trusting the order of tied rows because it looked right in a small test.
- Letting `shift` change a column to float and then merging on it.
- Forgetting `dropna=False` and silently losing rows with missing keys.
- Skipping `DISTINCT` and checking only one clean user.
