**Pattern:** Tree DP with a return value plus a side-channel answer. Each call returns the height, and a running best records the answer that "bends" at this node.

**Say this first (1 line):** "The longest path has a topmost node, and through that node it is left height plus right height in edges, so one post-order pass returns heights and keeps the max of that sum."

**Brute force:**
- For every node, compute the height of its left and right subtree from scratch, take `hl + hr`, and recurse into both children for the best.
- Each height call walks a whole subtree. On a chain of n nodes that is n + (n-1) + ... = O(n^2).
- Another brute force: BFS from every node, take the farthest distance. O(n^2) as well. I use it below as an independent check.

**Optimal:**
- `height(node)` returns the number of nodes on the longest downward path (empty = 0). It also does `best = max(best, l + r)`.
- Why `l + r`: any path has one topmost node. If that node is `n`, the path goes down the left side and down the right side. The height `l` (in nodes) of the left child equals the number of edges from `n` down to its deepest left node, and the same for `r`. So the longest path through `n` has `l + r` edges.
- The diameter is the best over all nodes as the top node, so the answer may skip the root.
- `best` is an int, and an inner function that rebinds it needs `nonlocal best` (or a one-element list holder like `best = [0]`). Without it Python makes `best` local and raises `UnboundLocalError`.
- The slow version recomputes heights inside every call, which is the O(n^2) trap.

**Complexity:** Time O(n): every node is visited once and does O(1) work. Space O(h) for the call stack: O(log n) balanced, O(n) on a chain. Slow version: O(n^2) worst case (the run shows n^2 + n height calls on a chain).

**Dry run:** `[1, 2, 3, 4, 5]`. Nodes 4 and 5 are leaves: height 1 each, and `l + r = 0` so best stays 0. At node 2: `l = 1, r = 1`, best = 2, return 2. Node 3 is a leaf: return 1. At root: `l = 2, r = 1`, best = max(2, 3) = 3. Answer 3 (path 4-2-1-3).

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Edge cases:**
- Empty tree and single node: 0.
- Two nodes: 1 (edges, not nodes). If the interviewer wants nodes, add 1 for non-empty trees.
- Path not through the root (the run prints one such tree).
- Chain of 10^4 nodes: the recursive version hits the default recursion limit of 1000 and raises `RecursionError`; the iterative post-order is fine.
- Negative or repeated values do not matter, only shape.

**Follow-ups:**
- Diameter in nodes instead of edges? Same code, answer `best + 1` for a non-empty tree.
- Weighted edges or node values (max path sum)? Same shape, return the best downward sum. That is Q17 in this part.
- Avoid recursion? Iterative post-order with a dict of heights keyed by `id(node)`, as in the code.

**Common mistakes:**
- Assuming the path goes through the root.
- Returning the diameter from the recursion instead of the height (the return value and the running best are different things).
- Forgetting `nonlocal`.
- Recomputing heights: O(n^2).
- Counting nodes when the question says edges.
