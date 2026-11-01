**Pattern:** Interval DP over boundary points. The state is a pair of boundaries (l, r), smaller intervals are solved first, and the transition scans every split point, so it is O(k^3) for k boundary points.

**Say this first (1 line):** "Sort the cuts, add 0 and n, let `dp[l][r]` be the cheapest way to make every cut strictly between points l and r, and choose which cut comes FIRST in that piece: it costs the whole piece, `points[r] - points[l]`, and leaves two independent sub-intervals."

**Brute force:** Try every order of the cuts: `len(cuts)!` orders (720 for 6 cuts), simulate the pieces and add the length of the piece each cut lands in. It is the oracle for at most 6 cuts, and exponential beyond that.

**Optimal:**
- Points: `pts = [0] + sorted(cuts) + [n]`, k = len(cuts) + 2 points. The cut positions are the only things that matter; n itself (up to 10^6) is never iterated.
- State: `dp[l][r]` (l < r) = minimum total cost to make all cuts strictly between `pts[l]` and `pts[r]`, assuming the piece `[pts[l], pts[r]]` exists as one stick.
- Base: `dp[l][l+1] = 0` (no cut inside) and the whole table starts at 0.
- Transition: pick the first cut m (`l < m < r`) in this piece. It costs the length of the piece, `pts[r] - pts[l]`, and then the two new pieces are independent: `dp[l][r] = pts[r] - pts[l] + min over m of (dp[l][m] + dp[m][r])`.
- Why FIRST and not last: the first cut in a piece has a known cost, the full length, no matter what else happens. If you chose the last cut instead, the piece it cuts is bounded by the nearest cuts already made, which are not determined by (l, r), so the cost would not be a function of the state. (In burst balloons it is the other way round: the first burst changes neighbours, so you think of the last burst, whose neighbours are the fixed ends. Same interval shape, opposite time direction.)
- Order of filling: increasing gap `r - l`, because `dp[l][r]` reads `dp[l][m]` and `dp[m][r]` with smaller gaps.
- Answer: `dp[0][k-1]`; no cuts gives k = 2 and 0.
- Memoised version: `f(l, r)` with `lru_cache`; its recursion depth is at most k <= 102, so it is safe at default limit 1000 (the code runs the largest size, 100 cuts, with the memo and gets the same answer). No setrecursionlimit is needed here.
- Space: the full triangle is read by every cell (`dp[l][m]` and `dp[m][r]` for all m), so there is no simple 1D reduction; O(k^2) memory is fine for k <= 102. (Knuth's optimisation could bring O(k^3) to O(k^2) time, not needed here and not checked.)

**Complexity:** Time O(k^3): about k^2/2 intervals times up to k split points (exactly C(k,3) inner steps, 171,700 for k = 102). Space O(k^2). Independent of n.

**Dry run:** `n = 7, cuts = [1,3,4,5]`, points `[0,1,3,4,5,7]` (indices 0..5). Entry dp[l][r], width = r - l:

| l \ r | 2 | 3 | 4 | 5 |
|---|---|---|---|---|
| 0 | 3 | 7 | 10 | 16 |
| 1 |  | 3 | 6 | 12 |
| 2 |  |  | 2 | 6 |
| 3 |  |  |  | 3 |

(entries with r = l + 1 are 0 and omitted.)
- `dp[0][2]` (cut at 1 inside 0..3): the only cut is 1, cost 3 - 0 = 3.
- `dp[2][4]` (3..5, cut at 4): cost 2. `dp[3][5]` (4..7, cut at 5): cost 3.
- `dp[0][5]` (whole stick, length 7): try first cut m = 1: 0 + 12, m = 2: 3 + 6, m = 3: 7 + 3, m = 4: 10 + 0. The minimum of the sums is 9, so the cost is 7 + 9 = 16, which matches the prompt. (m = 2 means cutting at 3 first, then 1 on the left piece 0..3 for 3, and 4 then 5 on 3..7 for 6.)
- Costs over all 24 orders range from 16 to 20, so order really matters.

**Code:**
<<CODE>>

**Output (my run):**
<<OUTPUT>>

**Edge cases:**
- No cuts: 0 (just the two boundaries).
- One cut: n (the full stick is cut once).
- n = 2 with the single cut at 1: 2.
- Cuts given unsorted (example 2 is): sorting first is required, since the intervals are by position.
- Cuts are distinct and strictly inside (1..n-1); a cut at 0 or n would cost a piece for nothing and is excluded by the prompt.
- n up to 10^6 changes nothing: only the number of cuts sets the work.

**Follow-ups:**
- Return the order too? Store the best m per cell and read the cuts off recursively (first cut at the root, then the left and right halves).
- Why is this the same as optimal merging of pieces? Reverse time: the last cut is the first merge, and each merge of adjacent pieces costs the merged length, which is the same interval shape as matrix-chain multiplication.
- Greedy "cut near the middle"? Wrong: it differs from the optimum on 32 of 400 random cases in the code.

**Common mistakes:**
- Forgetting to sort the cuts, or forgetting the 0 and n boundaries.
- Letting the memo depend on n instead of the cut positions (a table of size n would be 10^6 x 10^6).
- Filling the table by `l` then `r` in row order, so a cell reads an unfilled smaller interval; fill by increasing gap.
- Choosing the last cut and still charging `pts[r] - pts[l]`.
