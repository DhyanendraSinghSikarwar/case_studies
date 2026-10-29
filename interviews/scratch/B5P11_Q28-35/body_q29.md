**Pattern:** Top-down grid DP with `lru_cache`, analysed instead of just run. Three numbers describe one memoised recursion: its answer, its cache size and its nesting depth. Only one of them can break the program.

**Say this first (1 line):** "Every call at cell (i, j) sits at depth i + j + 1 because each call moves one step right or down; the cache holds the cells that some call reaches, and the answer is a forward path count. The depth is what raises RecursionError, not the cache size and not the (huge) answer."

**Brute force:** Run the real recursion with an instrumented `lru_cache` (a depth counter incremented on entry and decremented in `finally`, and `cache_info().currsize` afterwards). Exact, but it fails on big grids with RecursionError, and it is the oracle for m, n <= 12.

**Optimal:** No recursion at all, a forward table row by row.
- `called[i][j]`: some call of `f` reaches (i, j). (0,0) is called; (i, j) is called when the cell above or the cell to its left is **expanded**.
- `expanded[i][j]` = called, not blocked and not the bottom-right cell (those two return immediately and call nothing).
- `entries` = number of called cells. Blocked cells that are called count (they enter the cache), and so does a blocked end cell. Cells behind a wall are never called, so they are not counted.
- `depth` = max over called cells of `i + j + 1`. Why: the call tree starts at depth 1 for (0,0), and every call goes to (i+1, j) or (i, j+1), so a call at cell (i, j) is always exactly at depth i + j + 1, however it got there. The deepest call is therefore the called cell with the largest i + j.
- `paths`: `w[0][0] = 1` if (0,0) is not blocked; for other cells `w = w[above] + w[left]` and `w = 0` for a blocked cell. This counts right/down paths through open cells, which equals `f(0,0)`: `f` sums the two neighbours, a blocked cell returns 0, the end returns 1. The count is the exact integer (no modulus in this prompt); Python integers have no overflow.
- Only two rows of `w` and of the `expanded` flags are kept, so memory is O(n).
- Which one raises RecursionError: the **depth**. With no blocked cells and m = n = 600 the depth is 1199, past the default limit of 1000. The path count is a 359-digit integer, which Python handles fine, and 360,000 cache entries are only memory, not stack. In the sandbox on Python 3.13 the memoised 400 x 400 run (depth 799) worked and 600 x 600 raised RecursionError; the exact failing depth depends on version and call path, so treat the pass/fail as an observation, not a rule, and keep clear of the boundary. The fix is bottom-up, not `sys.setrecursionlimit`.
- Cache key must be hashable: the cache is a dict, and the key `(i, j)` is hashed. A tuple is hashable, a list is not (`lru_cache` raises `TypeError: unhashable type: 'list'`, shown in the code). Hashable also means immutable by convention: a key that could change after insertion would corrupt lookups.

**Complexity:** Forward table: time O(m*n) cell visits (each adds two integers, which for the big counts costs O(digits)), space O(n) with two rolling rows. Blocked cells are looked up in a per-row set, built in O(B), B <= 10^4. The recursion would be O(m*n) time too, O(m*n) cache, but O(m+n) stack depth, and that stack depth is the problem.

**Dry run:** `m = 3, n = 3, blocked = []`, expected `[6, 9, 5]`.

| cell depth `i+j+1` | | | paths from start `w` | | |
|---|---|---|---|---|---|
| 1 | 2 | 3 | 1 | 1 | 1 |
| 2 | 3 | 4 | 1 | 2 | 3 |
| 3 | 4 | 5 | 1 | 3 | 6 |

- All 9 cells are called, so `entries = 9`.
- The largest depth is at (2,2): 2 + 2 + 1 = 5.
- `w[2][2] = 3 + 3 = 6` (above 3, left 3).

Second example, `blocked = [[1,1]]`: the centre is called (entries still 9) but returns 0 and calls nothing; `w` becomes `[1,1,1],[1,0,1],[1,1,2]`, so paths = 2; depth is still 5 because (2,2) is reached through (0,2) then (1,2). Third example `m=2, n=4, blocked=[[0,0]]`: the start is blocked, so `f(0,0)` returns 0 straight away: entries 1, depth 1, paths 0.

**Code:**
<<CODE>>

**Output (my run):**
<<OUTPUT>>

**Edge cases:**
- Start blocked: answer `[0, 1, 1]`, no further cells are called.
- End blocked but start open: the end is still called (it counts in `entries`) and returns 0 (`[0, 4, 3]` for 2 x 2 in the code).
- A wall across an anti-diagonal: the cells behind it are never called, so `entries` and `depth` are smaller than in the open grid (21 entries, depth 6 in the code's 10 x 10 wall example).
- One row or one column: a straight chain, depth m + n - 1 = the number of cells.
- 1 x 1: `[1, 1, 1]`, or `[0, 1, 1]` when the single cell is blocked.
- The blocked list may include the end cell; membership is checked before the end test.

**Follow-ups:**
- What about the cache size at 1500 x 1500? Up to 2.25 million tuple entries (the code's 10^4-blocked run has 2,238,582 called cells); the forward version with two rows holds none of them.
- Does `sys.setrecursionlimit(10**6)` fix it? It may let the recursion run, but a very deep recursion risks exhausting the real C stack (a crash, not a clean exception), which I did not test here; the portable fix is the loop.
- How would you add a modulus? Reduce `w` after each addition if a modulus is requested; it changes nothing about depth or entries.

**Common mistakes:**
- Blaming the cache size or the big integer for RecursionError. Only the nesting depth counts.
- Counting a blocked called cell out of `entries`, or counting cells behind a wall.
- Saying depth = m * n; it is m + n - 1 at most (1199 for 600 x 600), not 360,000.
- Using a list `[i, j]` as the key, which raises `TypeError`.
- Forgetting that a blocked end cell returns 0 before the end test (blocked is checked first).
