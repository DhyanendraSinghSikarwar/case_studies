**Pattern:** Interval DP on a polygon (the matrix-chain shape). The state is a range of consecutive vertices, the split point is the apex of the triangle that sits on the closing edge.

**Say this first (1 line):** "`dp[i][j]` is the cheapest triangulation of the sub-polygon i, i+1, ..., j; the edge (i, j) belongs to exactly one triangle, with some third vertex k strictly between, so `dp[i][j] = min over k of dp[i][k] + dp[k][j] + v[i]*v[k]*v[j]`, O(n^3)."

**Brute force:** Plain recursion over the apex of the triangle on the edge (first, last): try every k, recurse on the two sub-polygons `vs[:k+1]` and `vs[k:]`. It visits every triangulation: there are Catalan(n-2) of them (1, 2, 5, 14, 42, 132 for n = 3..8, checked in the code), so it is exponential. The oracle for n <= 8. The code also enumerates all triangulations explicitly and scores each as a second oracle.

**Optimal:**
- State: `dp[i][j]` for i < j = minimum total score of a triangulation of the convex sub-polygon with vertices i, i+1, ..., j, closed by the chord (i, j).
- Base: `dp[i][i+1] = 0`: two vertices form an edge, no triangle. A triangle (j = i + 2) has one triangle: `dp[i][i+2] = v[i]*v[i+1]*v[i+2]`, which falls out of the recurrence with k = i + 1.
- Why the edge (i, j) belongs to exactly one triangle: in any triangulation of a polygon, each edge is a side of precisely one of its triangles, and that triangle's third vertex k lies on the polygon side between i and j (i < k < j). Cutting along the new chords (i, k) and (k, j) splits the problem into two smaller convex polygons that are triangulated independently. Every triangulation is counted once, by its k.
- Transition: `dp[i][j] = min(dp[i][k] + dp[k][j] + v[i]*v[k]*v[j])` over i < k < j.
- Fill by increasing gap `j - i` (2, 3, ..., n-1); the answer is `dp[0][n-1]`.
- Memoised version: `f(i, j)` with `lru_cache`. Recursion depth is at most n <= 100 (each call shrinks the range by at least one), so it is safe under the default limit of 1000 (the code runs n = 100 both ways).
- Space: the cell reads `dp[i][k]` and `dp[k][j]` for all k, so the whole upper triangle is live, O(n^2); there is no row-by-row reduction.
- A tempting greedy, "fan every triangle from the smallest label", is wrong: it differs from the optimum on 78 of 500 random polygons in the code.

**Complexity:** Time O(n^3): about n^2/2 cells times up to n apexes, exactly C(n,3) = 161,700 inner steps at n = 100. Space O(n^2).

**Dry run:** `values = [3, 7, 4, 5]` (the run also prints `[1, 2, 3]`, the first example: only `dp[0][2] = 1*2*3 = 6`).

| cell | options over k | value |
|---|---|---|
| dp[0][2] (3,7,4) | k=1: 0 + 0 + 3*7*4 = 84 | 84 |
| dp[1][3] (7,4,5) | k=2: 0 + 0 + 7*4*5 = 140 | 140 |
| dp[0][3] (all four) | k=1: 0 + 140 + 3*7*5 = 245; k=2: 84 + 0 + 3*4*5 = 144 | 144 |

The two triangulations of a quadrilateral are the two diagonals; 144 uses the diagonal 0-2 (triangles 3,7,4 and 3,4,5). For the first example of the prompt `[1,2,3]` there is a single triangle, so the answer is 6.

**Code:**
<<CODE>>

**Output (my run):**
<<OUTPUT>>

**Edge cases:**
- n = 3: one triangle, the product of the three labels (`[1,2,3]` gives 6).
- n = 4: two triangulations; take the cheaper (144 for `[3,7,4,5]`).
- All labels equal to v: every triangulation costs (n-2) * v^3 (24 for five 2's).
- Labels as large as 100, n = 100: the answer fits easily, and Python has no overflow anyway.
- The polygon is circular, but the DP fixes the chord (0, n-1) as the closing edge, which is also a real edge, so no rotation is needed.

**Follow-ups:**
- Why is it the same as matrix-chain multiplication? A chain of n - 1 matrices with dimensions `d` is the same recurrence with the product `d[i]*d[k]*d[j]`.
- Return the diagonals too? Store the best k per cell and recurse: the chord (i, k) and (k, j) are emitted for each triple.
- Maximum score instead? Swap `min` for `max`; the triangle product structure is the same.

**Common mistakes:**
- Choosing k from the whole range instead of strictly between i and j (a triangle with a repeated vertex).
- Treating the polygon as a line and forgetting that edge (0, n-1) closes it; it is already included as the outer edge of the sub-polygon.
- Fan greedy from the smallest label.
- Filling `dp` by row order so `dp[k][j]` has not been computed; fill by gap.
