**Say this first (1 line):** `rolling(3).min() == 1` is True only on the last row of each three-in-a-row window; to mark every row of the run, spread it back over the previous two rows with a reversed window (or a forward window), or skip rolling and group by the run key and test the run size.

**Schema and sample data:** a 0/1 Series of 13 positions, `[1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1]`: runs of ones of length 2 (positions 0-1), 3 (positions 3-5), 4 (positions 7-10) and 1 (position 12). The same data is loaded into SQLite as `f(pos, flag)` so the rolling check can be compared with a window-frame query.
```sql
CREATE TABLE f(pos INTEGER, flag INTEGER);
INSERT INTO f VALUES (0,1),(1,1),(2,0),(3,1),(4,1),(5,1),(6,0),(7,1),(8,1),(9,1),(10,1),(11,0),(12,1);
```

**SQL answer:** `SQL_MAIN` in the Code block, the same rolling check as a window frame. `COUNT(flag) OVER w3 = 3` makes the first two rows (frames with fewer than three rows) fail, and the outer `MAX(end3) OVER (... ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING)` spreads each qualifying window end back over the two rows before it:
{{SQL:SQL_MAIN}}

**pandas answer:** same logic, identical to the Code block:
{{PD}}
The Code block also runs the other three methods (`np.diff` on the zero-padded array, `itertools.groupby`, and `FixedForwardWindowIndexer`) and asserts they agree.

**Example:** positions 0 to 12 with values 1 1 0 1 1 1 0 1 1 1 1 0 1.
- `rolling(3).min()` is 1 where the window of three ending at that row is all ones: position 5 (positions 3-5), position 9 (7-9) and position 10 (8-10). So `end3` has True at 5, 9 and 10 only, which marks one row of the first run and two of the second.
- Spreading back: a row is inside a run if a qualifying window ends at that row or at one of the next two rows. Position 3 sees the window ending at 5; positions 7 and 8 see the windows ending at 9 and 10; and so on. Result: True at 3, 4, 5 and 7, 8, 9, 10.
- Run key `(s != s.shift()).cumsum()` gives run sizes 2, 1, 3, 1, 4, 1, 1; `s.eq(1) & size >= 3` is True on exactly the same seven positions.
- `np.diff` of `[0] + flags + [0]` has `+1` at run starts and `-1` after run ends: runs (start, length) = (0,2), (3,3), (7,4), (12,1). `itertools.groupby` gives the same runs as (value, length) pairs, with 4 the longest.

**Code:** run with `python3 -I`. All methods are asserted equal on the mask (compared position by position) and on the longest run; the timing line is measured on this machine on 1,000,000 random flags and will differ on yours.
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Edge cases:**
- NaN and `min_periods`: with the default (`min_periods` equal to the window size), any window containing a NaN gives NaN, so the first two rows and any window touching a NaN are never True: the mask is conservative. With `min_periods=1`, `rolling(3, min_periods=1).min()` is computed over the non-NaN values that are present, so a single 1 in position 1 (after a NaN) gives 1 and the check says "three in a row" at row 1: wrong, as my run shows (`[0, 1, 1, 1, 1, ...]`). Use `min_periods=1` only on the spreading step (`.max()`), never on the qualifying `.min()`.
- NaN in a flag Series forces float64; a boolean Series also comes back as float64 from `rolling(3).min()` in my run, so compare with `== 1` or `.astype(bool)`.
- The mask of "inside a run" differs from "end of a run": the first form needs the spreading step.
- Single run shorter than 3 (position 12) and runs of exactly 3 (positions 3-5, the boundary): included correctly.
- Ties for the longest run: `np.diff` and `itertools.groupby` return every run; pick the first or last explicitly.
- Empty Series: `rolling(3).min()` returns an empty Series; `itertools.groupby` yields nothing, so `max` needs `default=0` (not tested beyond that note).

**Then explain:**
- Rolling asks "is this window all ones", which is local; the run-key approach asks "how long is the run that contains me", which is global. Rolling is neat for a fixed N and awkward for "longest run" or for arbitrary N.
- To mark all rows of a run, combine the window ending at the row, the window starting at the row and the centred window, or spread the ends with a reversed `rolling(3, min_periods=1).max()`. I verified the three-window OR equals the run-size mask.
- Speed, measured here only: the last printed line of the Output block is the best of three runs on one million random 0/1 flags (about 70% ones), in milliseconds, for the rolling approach, the shift-key groupby, `np.diff` and `itertools.groupby` (longest run only, after `tolist()`). In my runs `np.diff` was clearly the fastest and the other three were within a small factor of each other, but the numbers move between runs and machines, and depend on the pandas and NumPy build and the data density, so treat the ranking as indicative and re-measure before relying on it. I did not measure memory or any size other than one million.
- The SQL window frame above is the same idea: a three-row frame plus a forward frame.
- Dialects (not executed here): `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` and `CURRENT ROW AND 2 FOLLOWING` are standard window syntax in PostgreSQL, MySQL 8 and others.

**Follow-ups:**
- At least N in a row, N a variable? `rolling(N)` with `min_periods=N`, or the run-size test, which is independent of N.
- Run lengths per group? Add `groupby('entity')` to both the shift and the key, as in Q5.
- Longest run of zeros? Invert the flag first.

**Common mistakes:**
- Setting `min_periods=1` on the qualifying `min()` (marks a false run at the start).
- Reading `rolling(3).min() == 1` as "this row is in a run" when it only marks the window end.
- Using `groupby(s)` directly instead of the run key (merges separate runs).
- Forgetting that float NaN turns a 0/1 column into float64.
- Measuring speed on a tiny Series and generalising.
