**Pattern:** 2D grid DP with a second table. One table optimises (minimum cost into each cell), one counts (how many paths achieve that minimum). It is "optimise, then count the optimal ones" on a DAG.

**Say this first (1 line):** "Two tables: `cost[i][j]` is the cheapest sum of a path into the cell, `ways[i][j]` is how many paths reach that cost; ties add the counts, a strictly cheaper predecessor hands over its count, and only the count is taken modulo 10^9 + 7. O(m*n) time, O(n) space."

**Brute force:** Enumerate every right/down path: choose which `m + n - 2` moves are Down, that is C(m+n-2, m-1) paths (70 for 5 x 5, but about 10^58 for 100 x 100). Take the minimum and count how often it occurs. It is the oracle for m, n <= 5.

**Optimal:**
- State: `cost[i][j]` = minimum sum over paths from (0,0) to (i,j) inclusive; `ways[i][j]` = number of paths that achieve exactly that sum (mod p).
- Transition: the last move came from above or from the left. `best = min(cost[i-1][j], cost[i][j-1])`, then `cost[i][j] = best + grid[i][j]`.
- Count merge, three cases:
  - Both predecessors have cost == best (a tie): `ways = ways[up] + ways[left]`. Both families of paths are optimal and disjoint (different last move).
  - Exactly one predecessor has cost == best: `ways` is copied from that one. The other predecessor's paths are strictly worse into this cell, so they do not count.
  - Border cell (first row or column): only one predecessor exists, so the count is copied from it.
- Base: `cost[0][0] = grid[0][0]`, `ways[0][0] = 1` (the empty path is one path). Missing predecessors are treated as cost infinity, which never ties with a real number.
- Why the modulus touches the count only: the count is compared with nothing, it is only added, and it grows like a binomial coefficient (the all-zero 100 x 100 grid has C(198,99), a 59-digit number of optimal paths, hence the modulus). The cost is compared with `min` and `==` at every cell, so it must stay the true value. A reduced cost can make a worse path look cheaper or break a tie. In this prompt the cost is at most 9 * 199 = 1791, far below 10^9 + 7, so reducing it would happen to be harmless here; the rule matters as soon as values are large, and the code shows the damage with an artificial modulus of 5.
- Memoised version: `f(i, j)` returns the best `(cost, ways)` of a path from (i,j) to the end (the other direction). Its recursion nests m + n - 1 deep, at most 199 for 100 x 100, which is under CPython's default limit of 1000 (observed on 3.13: the 100 x 100 run is fine). If the grid size were not capped, a depth of m + n - 1 above the limit would fail (Q29 measures exactly that), so bottom-up is the safe default.
- Space: row i reads row i-1 (same column) and the cell to its left, so one row of `cost` and one row of `ways`, updated left to right, is enough: O(n).

**Complexity:** Time O(m*n), each cell does O(1) work. Space O(m*n) for two full tables, O(n) with the single-row version. Reconstructing one optimal path would need the full table (or a parent pointer), counting does not.

**Dry run:** the first example, `grid = [[1,3,1],[1,5,1],[4,2,1]]`.

| cell | cost | ways | why |
|---|---|---|---|
| (0,0) | 1 | 1 | base |
| (0,1), (0,2) | 4, 5 | 1, 1 | first row, one predecessor |
| (1,0), (2,0) | 2, 6 | 1, 1 | first column |
| (1,1) | 7 | 1 | up 4, left 2: left is strictly cheaper, copy its count, 2 + 5 = 7 |
| (1,2) | 6 | 1 | up 5, left 7: up wins, 5 + 1 = 6 |
| (2,1) | 8 | 1 | up 7, left 6: left wins, 6 + 2 = 8 |
| (2,2) | 7 | 1 | up 6, left 8: up wins, 6 + 1 = 7 |

Answer `[7, 1]`. No tie occurs here, so the ways table is all ones. A tie appears in the fourth example `[[1,2],[2,1]]`: both predecessors of (1,1) cost 3, so `ways = 1 + 1 = 2` and the answer is `[4, 2]` (the run prints that table).

**Code:**
<<CODE>>

**Output (my run):**
<<OUTPUT>>

**Edge cases:**
- 1 x 1: the cost is the single value and the count is 1.
- A single row or a single column: exactly one path, count 1.
- All zeros: every path ties, the count is C(m+n-2, m-1) mod p (the code checks 100 x 100 against `math.comb`).
- A true count that is a multiple of 10^9 + 7 would show as 0 after the modulus, so never use `ways == 0` to mean "unreachable" (here every cell is reachable, so it does not come up).
- Compare costs before adding the cell value: adding `grid[i][j]` to both candidates does not change which is smaller, but the tie test must use the predecessors' costs.

**Follow-ups:**
- Print one optimal path? Keep the full cost table and walk back from the end, going to a predecessor whose cost equals `cost[i][j] - grid[i][j]`; for a fixed tie rule choose up or left consistently.
- Obstacles? Treat a blocked cell as cost infinity and count 0; its neighbours then read infinity and never tie.
- Count paths with sum divisible by k (not minimum)? Then the state grows by the remainder; counting all paths needs no cost table at all.

**Common mistakes:**
- Adding both predecessors' counts always (wrong 485 times in 500 random grids in the code).
- Taking the count from the first minimum only and losing the tied one (wrong 214 of 500).
- Reducing the cost modulo the prime (or any modulus): comparisons lie (450 of 500 wrong with an artificial modulus of 5; harmless here only because 10^9 + 7 is far above the cost bound 1791).
- Using `<=` instead of `==` for the count test: a strictly worse predecessor must contribute nothing.
