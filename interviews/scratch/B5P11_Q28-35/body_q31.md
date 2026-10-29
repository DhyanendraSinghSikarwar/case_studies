**Pattern:** Bitmask DP basics: a set of at most about 20 items is stored as an integer, one bit per task, so "which tasks are already taken" becomes a table index. Assignment problem by subset DP.

**Say this first (1 line):** "Worker index is the number of set bits in the mask, so the state is just the mask: `f[mask]` is the cheapest way for the remaining workers to take the remaining tasks; fill from the full mask down, then walk forward taking the smallest task that keeps the total optimal. O(2^n * n) time, O(2^n) space."

**Brute force:** Try every permutation of the tasks, n! of them (5,040 for n = 7), cost each, and keep the smallest `(cost, list)` pair; comparing the pair gives the lexicographic tie rule for free. It is the oracle for n <= 7 and is hopeless at n = 15 (1.3 * 10^12).

**Optimal:**
- Encoding: bit t of `mask` is 1 when task t is already taken. Workers are served in order 0, 1, 2, ..., so the next worker is `w = popcount(mask)`; the mask alone says who is next.
- State: `f[mask]` = minimum cost for workers `popcount(mask)`, ..., n-1 to take exactly the tasks NOT in `mask`, one each.
- Base: `f[full] = 0` (full = 2^n - 1): every task is taken, nothing left to pay.
- Transition: worker w picks a free task t: `f[mask] = min over free t of cost[w][t] + f[mask | 1<<t]`. `mask | 1<<t` is larger than `mask`, so iterating masks from `full - 1` down to 0 always finds the right-hand side final.
- Answer: `f[0]`.
- Reconstruction with the fixed tie rule (lexicographically smallest list): start at mask 0; for worker w = 0, 1, ..., scan tasks t in increasing order and take the first free t with `cost[w][t] + f[mask | 1<<t] == f[mask]`. Why this is the lexicographically smallest optimal list: `f` is exact, so every task that passes the test can start some optimal completion, and the smallest such t for worker 0 gives the smallest first entry; given that choice, the same argument applies to worker 1, and so on. Verified against the permutation oracle using the same `(cost, list)` order.
- Memoised version: `g(mask)` with `lru_cache`; the recursion depth is n + 1 <= 16, far under 1000, so there is no recursion-limit issue at this size. Bottom-up avoids call overhead.
- Space: `f` holds 2^n values. Computing only the value could be done layer by layer (masks with k bits depend only on masks with k+1 bits), but reconstruction needs `f` for every mask, so keep the whole array.
- Why n is capped near 20: states double with every extra task. n = 15 gives 32,768 masks and 491,520 transitions; n = 20 gives 1,048,576 masks and 20,971,520 transitions; n = 25 gives 838,860,800 transitions and a table of 33 million entries. Python's int lists make n = 20 slow and heavy; n = 15 is tiny (the code times it).

**Complexity:** Time O(2^n * n): each mask loops over n tasks; the `popcount` is O(1) in practice via `int.bit_count`. Space O(2^n). Compare n!: n = 15 gives 1.3 * 10^12 permutations against 491,520 transitions.

**Dry run:** `cost = [[9,2,7,8],[6,4,3,7],[5,8,1,8],[7,6,9,4]]`. A mask is written with bit 3 on the left (`0101` = tasks 0 and 2 taken). Selected rows of the table (the run prints all 16):

| mask | next worker | f | how |
|---|---|---|---|
| 1111 | | 0 | base |
| 0111 | 3 | 4 | only task 3 free: 4 + 0 |
| 1011 | 3 | 9 | only task 2 free: 9 + 0 |
| 0011 | 2 | 5 | t2: 1 + f[0111]=4 gives 5; t3: 8 + f[1011]=9 gives 17 |
| 0001 | 1 | 9 | t1: 4 + f[0011]=5 gives 9; t2: 3 + 12; t3: 7 + 7 |
| 0000 | 0 | 13 | t0: 9 + 9 = 18; t1: 2 + f[0010]=11 gives 13; t2: 7 + 13; t3: 8 + 12 |

Walk forward from mask 0000 with `f[0] = 13`: worker 0 tries t0 (9 + 9 = 18, not 13), then t1 (2 + 11 = 13, yes), so take 1. Mask is 0010. Worker 1 tries t0: 6 + f[0011]=5 gives 11 = f[0010], yes, take 0. Worker 2 takes 2 (1 + 4 = 5 = f[0011]), worker 3 takes 3. Result `[13, [1, 0, 2, 3]]`, as in the prompt. (Mask 0001 is "task 0 taken", so `f[0001] = 9` is the cost for workers 1..3 to take tasks 1, 2, 3.)

**Code:**
<<CODE>>

**Output (my run):**
<<OUTPUT>>

**Edge cases:**
- n = 1: `[cost[0][0], [0]]`.
- All entries equal: every assignment ties, so the identity list `[0, 1, ..., n-1]` is returned.
- Zero costs: same, the smallest list wins.
- Ties between different optimal assignments, such as `[[3,1],[1,3]]`: both `[0,1]` (cost 6) and `[1,0]` (cost 2) exist, only the second is optimal here, so the answer is `[2, [1, 0]]`; for `[[1,1],[1,1]]` both tie and `[0, 1]` wins by the rule.
- Fill direction: iterate masks downward, or the right-hand side is not ready (for the top-down version, recursion handles the order).

**Follow-ups:**
- Hungarian algorithm? It solves the same problem in O(n^3), which wins at n beyond 20; the bitmask DP is the answer when a short, easy-to-prove solution is wanted for n <= about 20.
- Maximise instead of minimise? Replace `min` by `max` and use `-inf` initial values; the tie rule is unchanged.
- More tasks than workers, or some pairs forbidden? Forbid by infinite cost; with more tasks than workers the mask has more bits than workers and the base case is `popcount == workers`.

**Common mistakes:**
- Iterating masks upward when the transition goes to `mask | bit`: the cell is read before it is final.
- Storing the worker index in the state as well (a factor n wasted).
- Greedy per worker (cheapest free task): worse on 206 of 300 random 5 x 5 matrices in the code.
- Tie rule: choosing the first task that is merely cheap for this worker, not one for which `cost + f[next] == f[mask]`. Only the latter preserves optimality.
