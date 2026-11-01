**Pattern:** DP over time with two agents moving in lock-step. Two walkers that move at the same pace share a "step number" k, so their columns follow from their rows and the state is (k, r1, r2).

**Say this first (1 line):** "The trip back is the same as a second walker going down-right at the same time, so run both at once: `dp[k][r1][r2]` is the most cherries the pair has picked after k moves, with columns `k - r1` and `k - r2`; four predecessor choices, a shared cell counts once, O(n^3)."

**Brute force:** Enumerate every right/down path (C(2n-2, n-1) of them, 70 for n = 5), keep those without thorns, and for every pair of paths add the cherries on the **union** of their cells (a shared cell once). The code also checks, for n <= 3, the statement read literally: pick a path, remove its cherries, then pick the best return path, and shows the two readings agree. Oracle for n <= 5.

**Optimal:**
- Why the return trip is a second down-right walker: a left/up path from the bottom-right to the top-left, read backwards, is a right/down path from the top-left to the bottom-right. Picking the cherries "on the way back" is then picking the cherries of a second right/down path, with the rule that a cherry already picked (a cell on both paths) is counted once. So the answer is the best union over a pair of right/down paths.
- State: after k moves each (k = 0..2n-2), walker 1 is at row r1 and column `k - r1`, walker 2 at row r2 and column `k - r2`. `dp[k][r1][r2]` = max cherries picked by the pair so far, or -infinity if the pair cannot be there (thorn, off-grid or unreachable).
- Base: `dp[0][0][0] = grid[0][0]` (0 or 1; -1 means no path and the answer is 0).
- Transition: each walker came from above (row - 1, same k - 1) or from the left (same row at k - 1). Four predecessor pairs: `(r1, r2)`, `(r1-1, r2)`, `(r1, r2-1)`, `(r1-1, r2-1)` at step k - 1. So `dp[k][r1][r2] = max(four predecessors) + grid[r1][k-r1] + (grid[r2][k-r2] if r1 != r2 else 0)`; skip any pair that stands on a thorn.
- Shared cell: when `r1 == r2` the columns are equal too (same k), so the walkers are on the same cell; add its cherry once.
- Answer: `max(0, dp[2n-2][n-1][n-1])`: if no pair arrives (thorns cut every path) the value is -infinity and the answer is 0.
- Symmetry: swapping the two walkers changes nothing, so only `r1 <= r2` is stored (about half the states); the code does this.
- Space: step k reads only step k - 1, so two n x n layers suffice: O(n^2) (the code keeps one rolling layer).
- Memoised version: `f(k, r1, r2)` = best from here to the end, depth 2n - 1 = 99 at n = 50, which is below the default limit of 1000, so memoisation is safe (the code runs n = 50 both ways). Bottom-up is still preferred.
- Why two separate greedy trips fail: taking the best single trip first can use up cherries and force a poor return. The smallest counterexample the code found: `[[0,1,0],[0,1,1],[1,1,0]]`: the greedy two-trip total is 4 but the best is 5. It is wrong on 34 of 500 random small grids.

**Complexity:** Time O(n^3): 2n - 1 steps times at most n^2/2 row pairs, 4 predecessors each. Space O(n^2) with rolling layers. At n = 50 that is about 99 * 1,250 * 4 operations.

**Dry run:** `grid = [[0,1,-1],[1,0,-1],[1,1,1]]`, pairs `(r1, r2)` kept with r1 <= r2 (the run prints this):

| k | reachable pairs (r1, r2): value | note |
|---|---|---|
| 0 | (0,0): 0 | start cell value 0 |
| 1 | (0,0): 1, (0,1): 2, (1,1): 1 | (0,0) means both on cell (0,1), counted once; (0,1) means one on (0,1), one on (1,0): 1 + 1 |
| 2 | (1,1): 2, (1,2): 3, (2,2): 2 | (0,2) is a thorn, so no pair uses row 0; (1,2) = cells (1,1)=0 and (2,0)=1 on top of the best earlier 2 |
| 3 | (2,2): 4 | cell (2,1) = 1; (1,2) is a thorn; best predecessor 3 |
| 4 | (2,2): 5 | cell (2,2) = 1 counted once |

Answer 5. The pair of paths: down, down, right, right and right, down, down, right (so both pass (2,1)). The second example has thorns that cut every route: no pair reaches k = 4, so the answer is 0.

**Code:**
<<CODE>>

**Output (my run):**
<<OUTPUT>>

**Edge cases:**
- n = 1: the cell value if it is not a thorn (the walkers are the same cell, counted once), else 0.
- Thorn at the start or the end: 0.
- Thorns that disconnect the corners: 0, never a negative number.
- All zeros: 0.
- All ones: the two paths share only the corners, so 4n - 4 for n >= 2 (12 for n = 4), not the sum of two full paths (the code asserts it).
- A cell on both paths counted twice is the standard bug: only when `r1 == r2`.

**Follow-ups:**
- Why does only the row pair matter, not the columns? Same step count k makes `c = k - r` for both walkers.
- Return the actual two paths? Keep the full 3D table (or a parent choice per state) and walk back from `(2n-2, n-1, n-1)`.
- Why not just rows and columns of both walkers (four coordinates)? The step number ties them together, so one coordinate per walker is redundant: n^4 states drop to n^3.

**Common mistakes:**
- Running the best path twice (greedy) and removing the cherries between trips.
- Counting a shared cell twice (add the second cherry only when `r1 != r2`).
- Allowing a walker to step on a thorn, or treating -infinity as 0 and returning a positive total for an unreachable end.
- Returning -infinity instead of 0 when no path exists.
