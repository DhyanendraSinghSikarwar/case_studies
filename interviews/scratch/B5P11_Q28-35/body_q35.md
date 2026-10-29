**Pattern:** Bitmask DP basics (Held-Karp). The set of visited cities is an integer mask; the state adds the current city; transitions extend the path by one unvisited city.

**Say this first (1 line):** "`f[mask][last]` is the cheapest path that starts at city 0, visits exactly the cities in mask and ends at last; extend by one unvisited city, close the tour back to 0 at the end: O(2^n * n^2) time, O(2^n * n) space, against (n-1)! for trying all orders."

**Brute force:** Try every permutation of cities 1..n-1 as the visiting order, add the distances along `0 -> p1 -> ... -> p(n-1) -> 0` and take the minimum: (n-1)! tours (5,040 for n = 8, the oracle size). Distances may be asymmetric, so a tour and its reverse can differ and both are tried.

**Optimal:**
- State: bit c of `mask` is 1 when city c is visited; bit 0 is always set (the tour starts there). `f[mask][last]` = minimum cost of a path that starts at 0, visits exactly the cities in `mask` and ends at `last`.
- Base: `f[1][0] = 0` (only city 0, standing on it). Everything else is infinity until reached.
- Transition: from `(mask, last)` go to any city `nxt` not in the mask: `f[mask | 1<<nxt][nxt] = min(..., f[mask][last] + dist[last][nxt])`. Masks are processed in increasing numeric order, and a target mask is always larger than its source, so every state is final when it is read.
- Answer: close the tour: `min over last != 0 of f[full][last] + dist[last][0]`, where `full = 2^n - 1`. For n = 1 the answer is 0.
- Why O(2^n * n^2): there are 2^n masks times n values of `last` (about 2^(n-1) * n states reached) and each tries up to n next cities. Space O(2^n * n) for the table.
- Space reduction: city 0 is always in the mask, so leave it out and index by the other n - 1 cities (2^(n-1) masks instead of 2^n); the code does this as a second solver and checks it. Reconstructing a tour needs the whole table, the code recovers one tour by walking the table backwards.
- Memoised version: `g(mask, last)` = cheapest way to finish from here (the other direction), depth at most n <= 12, so no recursion-limit issue, and it agrees in the code.
- Why (n-1)! is hopeless beyond n around 11: the number of tours grows factorially. In the table printed by the run: 8 cities give 5,040 tours, 10 give 362,880, 11 give 3,628,800, 12 give 39,916,800, 13 give 479,001,600 and 15 give about 8.7 * 10^10. The DP step count at the same sizes is 16,384, 102,400, 247,808, 589,824, 1,384,448 and 7,372,800. In the sandbox the permutation search took 0.35 s at n = 10 against a few milliseconds for the DP (timings are sandbox-only, not proof; the growth is reasoned from the counts above). The cutoff of "about 11" is relative to an interview time limit of roughly a second or so; the DP handles n = 12 as a trivial case.
- What the DP buys: it notices that two different orders of the same set ending at the same city have the same future, so only the cheaper one is kept: subsets and an endpoint replace whole orders.

**Complexity:** Time O(2^n * n^2), space O(2^n * n) (halved by dropping city 0 from the mask). For n = 12: 4,096 masks * 12 endpoints = 49,152 states, under 600,000 transitions.

**Dry run:** `dist = [[0,10,15,20],[10,0,35,25],[15,35,0,30],[20,25,30,0]]`. Masks list the visited cities, always including 0; entry = cost ending at the given city (the run prints all of them):

| mask (cities) | f by ending city |
|---|---|
| {0} | 0 at city 0 |
| {0,1} | city 1: 10 |
| {0,2} | city 2: 15 |
| {0,3} | city 3: 20 |
| {0,1,2} | city 1: 15 + 35 = 50 (via 2); city 2: 10 + 35 = 45 (via 1) |
| {0,1,3} | city 1: 20 + 25 = 45; city 3: 10 + 25 = 35 |
| {0,2,3} | city 2: 20 + 30 = 50; city 3: 15 + 30 = 45 |
| {0,1,2,3} | city 1: 70 (from {0,2,3} ending 3: 45 + 25; ending 2 would give 50 + 35 = 85); city 2: 65 (from {0,1,3} ending 3: 35 + 30; ending 1 gives 45 + 35 = 80); city 3: 75 (from {0,1,2} ending 1: 50 + 25, or ending 2: 45 + 30, a tie) |

Closing the tour: ending at 1: 70 + 10 = 80; at 2: 65 + 15 = 80; at 3: 75 + 20 = 95. The minimum is 80, as in the prompt. One optimal tour is 0 -> 2 -> 3 -> 1 -> 0 (15 + 30 + 25 + 10).

**Code:**
<<CODE>>

**Output (my run):**
<<OUTPUT>>

**Edge cases:**
- n = 1: 0, no travel (the code special-cases it, since there is no `last != 0`).
- n = 2: `dist[0][1] + dist[1][0]` (`[[0,3],[5,0]]` gives 8: the matrix is asymmetric).
- Asymmetric distances: the direction matters; `[[0,1,9],[9,0,1],[1,9,0]]` gives 3 by going 0 -> 1 -> 2 -> 0 and would be 27 the other way round (0 -> 2 -> 1 -> 0: 9 + 9 + 9).
- All distances 0 or all equal: the answer is 0 or n * d.
- Zero-cost edges are fine (costs are only required to be non-negative by the prompt).
- Mask must always contain bit 0; starting from `f[0][0]` or a mask without bit 0 breaks the closing step.

**Follow-ups:**
- Print the tour? Walk the table backwards from the best `last` (the code does it): at each step find the previous city whose value plus the edge equals the current value.
- Dropping the return to city 0 (Hamiltonian path)? Answer `min over last of f[full][last]` and let every city be the start.
- n = 20? 2^20 * 20^2 = 4.2 * 10^8 steps is too slow in plain Python; use bit tricks or another language, or a heuristic when exactness is not required.

**Common mistakes:**
- Forgetting to add `dist[last][0]` for the return leg.
- Letting `last` equal 0 in the closing minimum for n > 1 (a path that visited everything must not end at 0 before closing).
- Iterating masks in the wrong order: transitions go to a larger mask, so ascending order is correct.
- Assuming symmetry: `dist[a][b] != dist[b][a]` is allowed.
