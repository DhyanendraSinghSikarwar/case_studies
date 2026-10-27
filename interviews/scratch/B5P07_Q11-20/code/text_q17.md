**Pattern:** Tree DP with "return one thing, record another": the return value is the best path going DOWN from a node (so a parent can extend it), the running best is the best path that BENDS at a node.

**Say this first (1 line):** "At each node I compute the best downward gain from each child, dropping any negative gain. The best path bending here is left + val + right. I return val + the better side, because a parent can only continue one branch."

**Brute force:** Try every pair of nodes as the two ends and sum the values on the unique path between them. In the code: a DFS from each node over the undirected tree. O(n^2) time. Right answer, too slow for n = 3 * 10^4.

**Optimal:**
- `gain(n)`: `l = max(gain(left), 0)`, `r = max(gain(right), 0)`. The `max(..., 0)` means "take nothing from this side".
- `best = max(best, l + n.val + r)`: the path that bends at `n` and uses both sides.
- `return n.val + max(l, r)`: the best path that starts at `n` and goes down one side. Returning `l + n.val + r` would let a parent use both branches of the child, and then the path would fork, which is not a path.
- Why the clamp is right for the returned value: if a branch has negative gain, a path that ends at `n` is better than one that continues into it.
- Why `best` must not start at 0: the path must have at least one node. With all values negative the answer is the largest single node (`[-1, -2, -3]` gives -1, and `best = 0` would wrongly return 0). Start at `float("-inf")`, or at `root.val`.
- Without the clamp the bending sum can include a negative branch. The run shows `[1, -5, 3]`: unclamped code answers 3, the correct answer is 4 (1 + 3).

**Complexity:** Time O(n), one visit per node. Space O(h) recursion (n on a chain; the iterative version keeps a dict of n gains).

**Dry run:** `[-10, 9, 20, null, null, 15, 7]`. Leaves: 9 gives gain 9, best 9. 15 gives 15, 7 gives 7. At 20: `l = 15, r = 7`, bend = 42, best = 42, returns 35. At -10: `l = 9, r = 35`, bend = 34 (less than 42), best stays 42. Answer 42 (path 15-20-7).

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Edge cases:**
- Single negative node: its own value.
- All negative: the largest (closest to zero) single node, never an empty path.
- A zero-valued or negative root that the best path avoids entirely.
- Chain of 30000 nodes: recursion raises `RecursionError`; iterative post-order is fine. Sums are exact because Python ints do not overflow.

**Follow-ups:**
- Return the path itself, not only the sum? Store the best node and which child you used at each node, or keep `(gain, child_choice)`; rebuild after the pass.
- Path must go from root to a leaf? That is a simpler downward-only problem.
- Same shape in other problems? Diameter (Q11) is the same pattern with every value 1 (path sum then counts nodes, so the diameter in edges is that sum minus 1).

**Common mistakes:**
- Initialising `best = 0`.
- Forgetting the clamp, or clamping the `best` computation but not the return value (or vice versa).
- Returning `l + val + r` upward (a forked path).
- Using a plain int `best` inside the helper without `nonlocal`.
